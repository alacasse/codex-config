"""Artifact manifests and telemetry helpers for the architecture runner."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any, Iterable

try:
    from scripts import architecture_program_runner_command as _runner_command
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_command as _runner_command
    import architecture_program_runner_state as _runner_state

CONTEXT_BUDGETS = _runner_command.CONTEXT_BUDGETS
sandbox_for_phase = _runner_command.sandbox_for_phase
PHASES = _runner_state.PHASES
RUNNER_VERSION = _runner_state.RUNNER_VERSION
RunnerError = _runner_state.RunnerError
batch_artifact_root = _runner_state.batch_artifact_root
batch_manifest_path = _runner_state.batch_manifest_path
phase_input_inventory_path = _runner_state.phase_input_inventory_path
project_relative = _runner_state.project_relative
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path
run_manifest_path = _runner_state.run_manifest_path
run_telemetry_path = _runner_state.run_telemetry_path
structured_artifacts_enabled = _runner_state.structured_artifacts_enabled
utc_now = _runner_state.utc_now
write_json_object = _runner_state.write_json_object


def record_artifact_batch(state: dict[str, Any], result: dict[str, Any]) -> None:
    if not structured_artifacts_enabled(state) or not result.get("batch_id"):
        return
    batch_id = result["batch_id"]
    batches = state.setdefault("artifact_batches", [])
    if not isinstance(batches, list):
        return
    entry = next(
        (
            item
            for item in batches
            if isinstance(item, dict) and item.get("batch_id") == batch_id
        ),
        None,
    )
    if entry is None:
        entry = {
            "batch_id": batch_id,
            "batch_artifact_root": batch_artifact_root(state, batch_id),
            "dispatch_path": None,
            "spec_path": None,
            "last_receipt_path": None,
            "receipts": {},
            "input_inventories": {},
            "status": None,
        }
        batches.append(entry)
    if result.get("dispatch_path"):
        entry["dispatch_path"] = result["dispatch_path"]
    if result.get("spec_path"):
        entry["spec_path"] = result["spec_path"]
    entry["last_receipt_path"] = result["receipt_path"]
    if isinstance(entry.get("receipts"), dict):
        entry["receipts"][result["phase"]] = result["receipt_path"]
    phase = result.get("phase")
    inventory_path = phase_input_inventory_path(state, phase) if isinstance(phase, str) else None
    if inventory_path and isinstance(entry.get("input_inventories"), dict):
        entry["input_inventories"][phase] = inventory_path
    entry["status"] = result["status"]


def write_artifact_manifests(
    config: Any, state: dict[str, Any], result: dict[str, Any] | None = None
) -> None:
    if not structured_artifacts_enabled(state):
        return
    manifest_path = run_manifest_path(state)
    if manifest_path:
        write_json_object(
            resolve_project_path(config.project, manifest_path),
            build_run_manifest(config, state),
        )
    batch_id = result.get("batch_id") or state.get("active_batch_id") if result else state.get("active_batch_id")
    if isinstance(batch_id, str) and batch_id:
        write_batch_artifacts(config, state, batch_id)


def build_run_manifest(config: Any, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "runner_version": RUNNER_VERSION,
        "run_id": state.get("run_id"),
        "project": str(config.project),
        "program_ledger": state.get("program_ledger"),
        "state_path": project_relative(config.project, config.state_path),
        "run_telemetry_path": run_telemetry_path(state),
        "phase_telemetry_paths": state.get("phase_telemetry_paths", []),
        "max_batches": state.get("max_batches"),
        "execute_batches": state.get("execute_batches"),
        "batches": state.get("artifact_batches", []),
    }


def write_batch_artifacts(config: Any, state: dict[str, Any], batch_id: str) -> None:
    root_value = batch_artifact_root(state, batch_id)
    manifest_value = batch_manifest_path(state, batch_id)
    if root_value is None or manifest_value is None:
        return
    root = resolve_project_path(config.project, root_value)
    write_json_object(
        resolve_project_path(config.project, manifest_value),
        build_batch_manifest(state, batch_id),
    )
    index_path = root / "index.md"
    index_path.write_text(build_batch_index(config, state, batch_id, root), encoding="utf-8")


def build_batch_manifest(state: dict[str, Any], batch_id: str) -> dict[str, Any]:
    entry = artifact_batch_entry(state, batch_id)
    return {
        "schema_version": 1,
        "batch_id": batch_id,
        "program_ledger": state.get("program_ledger"),
        "dispatch_path": entry.get("dispatch_path") or state.get("dispatch_path"),
        "spec_path": entry.get("spec_path") or state.get("spec_path"),
        "receipts": entry.get("receipts", {}),
        "input_inventories": entry.get("input_inventories", {}),
        "telemetry": entry.get("telemetry", {}),
        "commit_range": latest_receipt_field(state, "commit_range"),
        "validation_summary": latest_receipt_field(state, "validation_summary"),
        "review_summary": latest_receipt_field(state, "review_summary"),
        "status": entry.get("status"),
    }


def artifact_batch_entry(state: dict[str, Any], batch_id: str) -> dict[str, Any]:
    batches = state.get("artifact_batches")
    if isinstance(batches, list):
        for entry in batches:
            if isinstance(entry, dict) and entry.get("batch_id") == batch_id:
                return entry
    return {}


def latest_receipt_field(state: dict[str, Any], field: str) -> Any:
    receipt_path = state.get("last_receipt_path")
    project = state.get("project")
    if not isinstance(receipt_path, str) or not isinstance(project, str):
        return None
    try:
        receipt = read_json_object(resolve_project_path(Path(project), receipt_path))
    except RunnerError:
        return None
    return receipt.get(field)


def build_batch_index(config: Any, state: dict[str, Any], batch_id: str, batch_root: Path) -> str:
    entry = artifact_batch_entry(state, batch_id)
    lines = [
        f"# {batch_id} Runner Artifacts",
        "",
        f"- Program ledger: {relative_project_link(config, batch_root, state['program_ledger'])}",
    ]
    dispatch_path = entry.get("dispatch_path") or state.get("dispatch_path")
    spec_path = entry.get("spec_path") or state.get("spec_path")
    if dispatch_path:
        lines.append(
            f"- Dispatch packet: {relative_project_link(config, batch_root, dispatch_path)}"
        )
    if spec_path:
        lines.append(f"- Runway spec: {relative_project_link(config, batch_root, spec_path)}")
    state_path = project_relative(config.project, config.state_path)
    lines.extend(
        [
            f"- Run state: {relative_project_link(config, batch_root, state_path)}",
            "- Receipts:",
        ]
    )
    receipts = entry.get("receipts", {})
    if isinstance(receipts, dict) and receipts:
        for phase in PHASES:
            path = receipts.get(phase)
            if isinstance(path, str):
                lines.append(f"  - {phase}: {relative_project_link(config, batch_root, path)}")
    else:
        lines.append("  - none recorded yet")
    lines.append("")
    return "\n".join(lines)


def relative_project_link(config: Any, from_dir: Path, value: str) -> str:
    path = resolve_project_path(config.project, value)
    return os.path.relpath(path, start=from_dir).replace(os.sep, "/")


def pop_phase_execution_meta(state: dict[str, Any]) -> dict[str, Any]:
    value = state.pop("_phase_execution_meta", {})
    return value if isinstance(value, dict) else {}


def apply_execution_meta_to_state(state: dict[str, Any], execution_meta: dict[str, Any]) -> None:
    session_id = execution_meta.get("codex_session_id")
    if isinstance(session_id, str) and session_id:
        state["last_codex_session"] = session_id


def build_phase_telemetry(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    started_at: str,
    elapsed_seconds: float,
    prompt_bytes: int,
    result: dict[str, Any] | None,
    status: str,
    error: str | None,
    execution_meta: dict[str, Any],
) -> dict[str, Any]:
    session_path = execution_meta.get("codex_session_path")
    token_summary = summarize_token_events(Path(session_path)) if isinstance(
        session_path, str
    ) else missing_token_summary()
    budget = context_budget_summary(phase, token_summary)
    return {
        "schema_version": 1,
        "runner_version": RUNNER_VERSION,
        "run_id": state.get("run_id"),
        "batch_id": result.get("batch_id") or state.get("active_batch_id")
        if result
        else state.get("active_batch_id"),
        "phase": phase,
        "status": status,
        "error": error,
        "started_at": started_at,
        "ended_at": utc_now(),
        "elapsed_seconds": elapsed_seconds,
        "model": config.model,
        "sandbox": sandbox_for_phase(config, phase),
        "exit_code": execution_meta.get("exit_code"),
        "stdout_bytes": execution_meta.get("stdout_bytes"),
        "stderr_bytes": execution_meta.get("stderr_bytes"),
        "prompt_bytes": prompt_bytes,
        "prompt_chars": prompt_bytes,
        "codex_session_id": execution_meta.get("codex_session_id"),
        "codex_session_path": execution_meta.get("codex_session_path"),
        "token_summary": token_summary,
        "context_budget": budget,
        "input_inventory_path": phase_input_inventory_path(state, phase),
        "artifact_sizes": artifact_size_entries(config, state, result),
    }


def missing_token_summary() -> dict[str, Any]:
    return {
        "status": "missing",
        "turn_count": 0,
        "max_input_tokens": None,
        "max_context_used_percent": None,
        "final_input_tokens": None,
        "total_input_tokens": None,
        "total_tokens": None,
        "cached_input_tokens": None,
        "context_pressure": "missing",
    }


def summarize_token_events(path: Path) -> dict[str, Any]:
    if not path.exists():
        return missing_token_summary()
    turn_count = 0
    max_input_tokens: int | None = None
    final_input_tokens: int | None = None
    cached_input_tokens: int | None = None
    total_input_tokens: int | None = None
    total_tokens: int | None = None
    context_window: int | None = None
    max_context_percent: float | None = None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return missing_token_summary()
    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = record.get("payload") if isinstance(record, dict) else None
        if not isinstance(payload, dict):
            payload = record if isinstance(record, dict) else {}
        if payload.get("type") != "token_count":
            continue
        usage = payload.get("last_token_usage")
        if not isinstance(usage, dict):
            usage = payload
        total_usage = payload.get("total_token_usage")
        if not isinstance(total_usage, dict):
            total_usage = {}
        input_tokens = int_or_none(usage.get("input_tokens"))
        if input_tokens is not None:
            max_input_tokens = max(input_tokens, max_input_tokens or 0)
            final_input_tokens = input_tokens
        cached_input_tokens = int_or_none(usage.get("cached_input_tokens"))
        total_input_tokens = int_or_none(total_usage.get("input_tokens"))
        output_tokens = int_or_none(total_usage.get("output_tokens")) or 0
        reasoning_tokens = int_or_none(total_usage.get("reasoning_output_tokens")) or 0
        if total_input_tokens is not None:
            total_tokens = total_input_tokens + output_tokens + reasoning_tokens
        context_window = int_or_none(payload.get("model_context_window")) or context_window
        turn_count += 1
    if turn_count == 0:
        return missing_token_summary()
    if max_input_tokens is not None and context_window:
        max_context_percent = round((max_input_tokens / context_window) * 100, 1)
    return {
        "status": "ok",
        "turn_count": turn_count,
        "max_input_tokens": max_input_tokens,
        "max_context_used_percent": max_context_percent,
        "final_input_tokens": final_input_tokens,
        "total_input_tokens": total_input_tokens,
        "total_tokens": total_tokens,
        "cached_input_tokens": cached_input_tokens,
        "context_pressure": context_pressure(max_context_percent),
    }


def int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return int(value)
    return None


def context_pressure(percent: float | None) -> str:
    if percent is None:
        return "missing"
    if percent < 50:
        return "context_ok"
    if percent < 70:
        return "context_watch"
    if percent < 85:
        return "context_pressure"
    return "context_stop_recommended"


def context_budget_summary(phase: str, token_summary: dict[str, Any]) -> dict[str, Any]:
    soft, hard = CONTEXT_BUDGETS[phase]
    max_input = token_summary.get("max_input_tokens")
    if not isinstance(max_input, int):
        status = "missing"
    elif max_input > hard:
        status = "hard_warning"
    elif max_input > soft:
        status = "soft_warning"
    else:
        status = "ok"
    return {
        "soft_budget_tokens": soft,
        "hard_warning_tokens": hard,
        "max_input_tokens": max_input if isinstance(max_input, int) else None,
        "status": status,
    }


def artifact_size_entries(
    config: Any, state: dict[str, Any], result: dict[str, Any] | None
) -> list[dict[str, Any]]:
    values = [
        state.get("program_ledger"),
        state.get("dispatch_path"),
        state.get("spec_path"),
    ]
    if result:
        values.extend(
            [result.get("dispatch_path"), result.get("spec_path"), result.get("receipt_path")]
        )
    result_phase = result.get("phase") if result else None
    inventory = phase_input_inventory_path(state, result_phase) if isinstance(result_phase, str) else None
    if inventory:
        values.append(inventory)
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str) or not value or value in seen:
            continue
        seen.add(value)
        path = resolve_project_path(config.project, value)
        try:
            stat = path.stat()
        except OSError:
            entries.append({"path": value, "exists": False, "bytes": None})
        else:
            entries.append({"path": value, "exists": True, "bytes": stat.st_size})
    return entries


def record_phase_telemetry_path(
    state: dict[str, Any], path: str, result: dict[str, Any] | None = None
) -> None:
    state["last_phase_telemetry_path"] = path
    paths = state.setdefault("phase_telemetry_paths", [])
    if isinstance(paths, list) and path not in paths:
        paths.append(path)
    batch_id = result.get("batch_id") or state.get("active_batch_id") if result else state.get("active_batch_id")
    if isinstance(batch_id, str) and batch_id:
        entry = artifact_batch_entry(state, batch_id)
        telemetry = entry.setdefault("telemetry", {})
        if isinstance(telemetry, dict):
            result_phase = result.get("phase") if result else None
            phase = result_phase if isinstance(result_phase, str) else state["active_phase"]
            telemetry[phase] = path


def write_phase_telemetry(config: Any, path: str, telemetry: dict[str, Any]) -> None:
    write_json_object(resolve_project_path(config.project, path), telemetry)


def write_run_telemetry(config: Any, state: dict[str, Any]) -> None:
    path = run_telemetry_path(state)
    if path is None:
        return
    phase_paths = state.get("phase_telemetry_paths")
    phases = []
    if isinstance(phase_paths, list):
        for index, value in enumerate(phase_paths):
            if not isinstance(value, str):
                continue
            try:
                phase = read_json_object(resolve_project_path(config.project, value))
                phase["_phase_index"] = index
                phases.append(phase)
            except RunnerError:
                phases.append({"path": value, "status": "missing", "_phase_index": index})
    write_json_object(
        resolve_project_path(config.project, path),
        build_run_telemetry(config, state, phases),
    )
    if should_refresh_failure_manifests(state):
        write_artifact_manifests(config, state)


def should_refresh_failure_manifests(state: dict[str, Any]) -> bool:
    if state.get("last_phase_status") != "failed":
        return False
    if not isinstance(state.get("active_batch_id"), str):
        return False
    stop_reason = state.get("stop_reason")
    if isinstance(stop_reason, str) and "input inventory" in stop_reason:
        return False
    return True


def build_run_telemetry(
    config: Any, state: dict[str, Any], phases: list[dict[str, Any]]
) -> dict[str, Any]:
    max_context_percent = max_numeric(
        phase.get("token_summary", {}).get("max_context_used_percent")
        for phase in phases
        if isinstance(phase.get("token_summary"), dict)
    )
    max_input_tokens = max_numeric(
        phase.get("token_summary", {}).get("max_input_tokens")
        for phase in phases
        if isinstance(phase.get("token_summary"), dict)
    )
    elapsed_seconds = sum_numeric(phase.get("elapsed_seconds") for phase in phases)
    return {
        "schema_version": 1,
        "runner_version": RUNNER_VERSION,
        "run_id": state.get("run_id"),
        "project": str(config.project),
        "program_ledger": state.get("program_ledger"),
        "state_path": project_relative(config.project, config.state_path),
        "stop_reason": state.get("stop_reason"),
        "phase_count": len(phases),
        "elapsed_seconds": elapsed_seconds,
        "max_input_tokens": max_input_tokens,
        "max_context_used_percent": max_context_percent,
        "context_pressure": context_pressure(max_context_percent),
        "phases": [
            {
                "phase": phase.get("phase"),
                "status": phase.get("status"),
                "telemetry_path": telemetry_path_for_phase(state, phase),
                "elapsed_seconds": phase.get("elapsed_seconds"),
                "prompt_bytes": phase.get("prompt_bytes"),
                "max_input_tokens": phase.get("token_summary", {}).get("max_input_tokens")
                if isinstance(phase.get("token_summary"), dict)
                else None,
                "context_budget_status": phase.get("context_budget", {}).get("status")
                if isinstance(phase.get("context_budget"), dict)
                else None,
                "codex_session_id": phase.get("codex_session_id"),
            }
            for phase in phases
        ],
    }


def telemetry_path_for_phase(state: dict[str, Any], phase: dict[str, Any]) -> str | None:
    paths = state.get("phase_telemetry_paths")
    if not isinstance(paths, list):
        return None
    index = phase.get("_phase_index")
    if isinstance(index, int) and 0 <= index < len(paths):
        value = paths[index]
        return value if isinstance(value, str) else None
    phase_name = phase.get("phase")
    for value in paths:
        if isinstance(value, str) and isinstance(phase_name, str) and phase_name in value:
            return value
    return None


def max_numeric(values: Iterable[Any]) -> int | float | None:
    numeric = [value for value in values if isinstance(value, (int, float))]
    return max(numeric) if numeric else None


def sum_numeric(values: Iterable[Any]) -> float:
    return round(sum(value for value in values if isinstance(value, (int, float))), 3)
