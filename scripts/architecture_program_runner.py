#!/usr/bin/env python3
"""Run architecture-program phases through fresh Codex exec processes."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

try:
    from scripts import architecture_program_runner_command as _runner_command
    from scripts import architecture_program_runner_state as _runner_state
    from scripts import architecture_program_runner_validation as _runner_validation
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_command as _runner_command
    import architecture_program_runner_state as _runner_state
    import architecture_program_runner_validation as _runner_validation

PHASE_RECEIPT_NAMES = _runner_state.PHASE_RECEIPT_NAMES
PHASES = _runner_state.PHASES
RUNNER_VERSION = _runner_state.RUNNER_VERSION
RunnerError = _runner_state.RunnerError
artifact_root_from_state_path = _runner_state.artifact_root_from_state_path
batch_artifact_root = _runner_state.batch_artifact_root
batch_manifest_path = _runner_state.batch_manifest_path
default_artifact_root = _runner_state.default_artifact_root
discover_resume_state_path = _runner_state.discover_resume_state_path
initial_state = _runner_state.initial_state
ledger_slug = _runner_state.ledger_slug
legacy_state_path = _runner_state.legacy_state_path
load_state = _runner_state.load_state
new_run_id = _runner_state.new_run_id
next_phase_telemetry_path = _runner_state.next_phase_telemetry_path
phase_input_inventory_path = _runner_state.phase_input_inventory_path
phase_receipt_path = _runner_state.phase_receipt_path
project_relative = _runner_state.project_relative
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path
resolve_state_path = _runner_state.resolve_state_path
run_manifest_path = _runner_state.run_manifest_path
run_telemetry_path = _runner_state.run_telemetry_path
slugify_path_component = _runner_state.slugify_path_component
structured_artifacts_enabled = _runner_state.structured_artifacts_enabled
utc_now = _runner_state.utc_now
validate_state = _runner_state.validate_state
write_json_object = _runner_state.write_json_object
write_state = _runner_state.write_state
NEXT_PHASES = _runner_validation.NEXT_PHASES
REQUIRED_RESULT_FIELDS = _runner_validation.REQUIRED_RESULT_FIELDS
STATUSES = _runner_validation.STATUSES
UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS = _runner_validation.UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS
expected_next_phases = _runner_validation.expected_next_phases
schema_keyword_paths = _runner_validation.schema_keyword_paths
schema_subset_violations = _runner_validation.schema_subset_violations
validate_expected_receipt_path = _runner_validation.validate_expected_receipt_path
validate_nullable_string = _runner_validation.validate_nullable_string
validate_phase_result = _runner_validation.validate_phase_result
validate_receipt = _runner_validation.validate_receipt
validate_required_string = _runner_validation.validate_required_string
validate_result_against_state = _runner_validation.validate_result_against_state
validate_summary = _runner_validation.validate_summary
CONTEXT_BUDGETS = _runner_command.CONTEXT_BUDGETS
SCHEMA_PATH = _runner_command.SCHEMA_PATH
RUNNER_REFERENCE_PATH = _runner_command.RUNNER_REFERENCE_PATH
batch_limit_label = _runner_command.batch_limit_label
build_codex_command = _runner_command.build_codex_command
build_prompt = _runner_command.build_prompt
build_subprocess_env = _runner_command.build_subprocess_env
env_override_key_label = _runner_command.env_override_key_label
phase_skill_instruction = _runner_command.phase_skill_instruction
print_dry_run = _runner_command.print_dry_run
quote_for_display = _runner_command.quote_for_display
sandbox_for_phase = _runner_command.sandbox_for_phase
shell_join = _runner_command.shell_join


REPO_ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class RunnerConfig:
    project: Path
    program_ledger: str
    max_batches: int | None
    execute_batches: bool
    state_path: Path
    sandbox: str
    execute_sandbox: str | None
    model: str | None
    env_overrides: tuple[tuple[str, str], ...]
    dry_run: bool
    resume: bool
    stop_after_phase: str | None
    artifact_root: Path | None = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run split-phase architecture-program batches through codex exec."
    )
    parser.add_argument("--project", required=True, help="Project path for codex exec --cd.")
    parser.add_argument(
        "--program-ledger",
        required=True,
        help="Project-relative program ledger path.",
    )
    parser.add_argument(
        "--max-batches",
        type=positive_int,
        default=None,
        help="Maximum closeouts to complete. Default: 1 unless --all-batches is set.",
    )
    parser.add_argument(
        "--all-batches",
        action="store_true",
        help=(
            "Run until no safe executable batch remains or a stop condition is hit. "
            "Cannot be combined with --max-batches."
        ),
    )
    parser.add_argument(
        "--execute-batches",
        action="store_true",
        help="Execute generated Batch Runway specs after creation.",
    )
    parser.add_argument(
        "--state",
        default=None,
        help="Project-relative or absolute JSON state path.",
    )
    parser.add_argument(
        "--sandbox",
        default="workspace-write",
        help="Codex sandbox value. Default: workspace-write.",
    )
    parser.add_argument(
        "--execute-sandbox",
        default=None,
        help=(
            "Optional Codex sandbox value for the execute phase only. "
            "Use when Batch Runway execution must commit and the default sandbox "
            "cannot write Git metadata."
        ),
    )
    parser.add_argument("--model", default=None, help="Optional codex exec model.")
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        type=env_override,
        help=(
            "Environment variable override passed to every nested codex exec phase. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned phase command and prompt without writing state.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Load existing state and resume from active_phase.",
    )
    parser.add_argument(
        "--stop-after-phase",
        choices=PHASES,
        default=None,
        help=(
            "Run and complete the named phase, persist receipt and state, "
            "then stop before launching the next phase."
        ),
    )
    args = parser.parse_args(argv)
    if args.all_batches and args.max_batches is not None:
        parser.error("--all-batches cannot be combined with --max-batches")
    return args


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def env_override(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("must use KEY=VALUE")
    key, env_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("environment key must be non-empty")
    return key, env_value


def config_from_args(args: argparse.Namespace) -> RunnerConfig:
    project = Path(args.project).expanduser().resolve()
    state_path, artifact_root = resolve_state_path(
        project, args.program_ledger, args.state, resume=args.resume
    )
    max_batches = None if args.all_batches else args.max_batches or 1
    return RunnerConfig(
        project=project,
        program_ledger=args.program_ledger,
        max_batches=max_batches,
        execute_batches=args.execute_batches,
        state_path=state_path,
        sandbox=args.sandbox,
        execute_sandbox=args.execute_sandbox,
        model=args.model,
        env_overrides=tuple(args.env),
        dry_run=args.dry_run,
        resume=args.resume,
        stop_after_phase=args.stop_after_phase,
        artifact_root=artifact_root,
    )


def execute_codex_phase(config: RunnerConfig, state: dict[str, Any], phase: str) -> dict[str, Any]:
    prompt = build_prompt(config, state, phase)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", prefix="architecture-program-runner-", suffix=".json"
    ) as handle:
        output_last_message = Path(handle.name)
        command = build_codex_command(config, phase, prompt, output_last_message)
        completed = subprocess.run(
            command,
            cwd=config.project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=build_subprocess_env(config.env_overrides),
        )
        state["_phase_execution_meta"] = {
            "exit_code": completed.returncode,
            "stdout_bytes": len(completed.stdout.encode("utf-8")),
            "stderr_bytes": len(completed.stderr.encode("utf-8")),
            "codex_session_id": extract_codex_session_id(
                f"{completed.stdout}\n{completed.stderr}"
            ),
            "codex_session_path": None,
        }
        if completed.returncode != 0:
            raise RunnerError(
                "codex exec failed for "
                f"{phase} with exit {completed.returncode}\n{completed.stderr.strip()}"
            )
        return read_json_object(output_last_message)


def extract_codex_session_id(text: str) -> str | None:
    match = re.search(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        text,
        flags=re.IGNORECASE,
    )
    return match.group(0) if match else None


def git_status_lines(project: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=project,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RunnerError(f"git status failed in {project}: {completed.stderr.strip()}")
    return [line for line in completed.stdout.splitlines() if line]


def dirty_paths_from_status(lines: Iterable[str]) -> list[str]:
    paths: list[str] = []
    for line in lines:
        if len(line) < 4:
            continue
        raw = line[3:].strip()
        if " -> " in raw:
            before, after = raw.split(" -> ", 1)
            paths.extend([before.strip('"'), after.strip('"')])
        else:
            paths.append(raw.strip('"'))
    return paths


def expected_dirty_paths(
    config: RunnerConfig,
    state: dict[str, Any],
    phase: str,
    *,
    extra_paths: Iterable[str] = (),
) -> set[str]:
    expected: set[str] = {project_relative(config.project, config.state_path)}
    if state.get("artifact_root"):
        expected.add(str(state["artifact_root"]))
    for field in ("run_manifest_path", "batch_manifest_path", "active_batch_artifact_root"):
        if state.get(field):
            expected.add(str(state[field]))
    for value in extra_paths:
        expected.add(project_relative(config.project, resolve_project_path(config.project, value)))

    for field in ("last_receipt_path",):
        if state.get(field):
            expected.add(
                project_relative(config.project, resolve_project_path(config.project, state[field]))
            )
    if state.get("last_receipt_path"):
        try:
            receipt = read_json_object(
                resolve_project_path(config.project, state["last_receipt_path"])
            )
        except RunnerError:
            receipt = {}
        if (
            receipt.get("status") == "stopped"
            and receipt.get("phase") == phase
            and isinstance(receipt.get("evidence_paths"), list)
        ):
            for value in receipt["evidence_paths"]:
                if isinstance(value, str):
                    expected.add(
                        project_relative(config.project, resolve_project_path(config.project, value))
                    )

    if phase == "select-dispatch":
        for field in ("dispatch_path",):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    elif phase == "create-spec":
        for field in ("dispatch_path", "spec_path"):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    elif phase == "execute":
        for field in ("spec_path", "dispatch_path"):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    elif phase == "closeout":
        expected.add(config.program_ledger)
        for field in ("spec_path", "last_receipt_path"):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    return {path for path in expected if path and path != "."}


def check_worktree(
    config: RunnerConfig,
    state: dict[str, Any],
    phase: str,
    *,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
    extra_paths: Iterable[str] = (),
) -> None:
    dirty = dirty_paths_from_status(status_reader(config.project))
    if not dirty:
        return
    expected = expected_dirty_paths(config, state, phase, extra_paths=extra_paths)
    unexpected = [path for path in dirty if not path_is_expected(path, expected)]
    if unexpected:
        raise RunnerError(
            "dirty files cannot be classified as expected for "
            f"{phase}: {', '.join(unexpected)}"
        )


def path_is_expected(path: str, expected: set[str]) -> bool:
    normalized = path.rstrip("/")
    for candidate in expected:
        candidate = candidate.rstrip("/")
        if normalized == candidate:
            return True
        if normalized.startswith(candidate + "/"):
            return True
        if candidate.startswith(normalized + "/"):
            return True
    return False


def check_required_artifacts(config: RunnerConfig, state: dict[str, Any]) -> None:
    phase = state["active_phase"]
    if phase in {"create-spec", "execute", "closeout"}:
        dispatch_path = state.get("dispatch_path")
        if not dispatch_path:
            raise RunnerError(f"{phase} requires dispatch_path in runner state")
        if not resolve_project_path(config.project, dispatch_path).exists():
            raise RunnerError(f"{phase} dispatch_path does not exist: {dispatch_path}")
    if phase in {"execute", "closeout"}:
        spec_path = state.get("spec_path")
        if not spec_path:
            raise RunnerError(f"{phase} requires spec_path in runner state")
        if not resolve_project_path(config.project, spec_path).exists():
            raise RunnerError(f"{phase} spec_path does not exist: {spec_path}")
    receipt_path = state.get("last_receipt_path")
    if state.get("last_phase_status") == "completed" and receipt_path:
        receipt = read_json_object(resolve_project_path(config.project, receipt_path))
        validate_phase_result(receipt)


def apply_phase_result(state: dict[str, Any], result: dict[str, Any]) -> None:
    phase = result["phase"]
    state["last_receipt_path"] = result["receipt_path"]
    state["last_phase_status"] = result["status"]
    state["stop_reason"] = result["stop_reason"]

    if result["batch_id"]:
        state["active_batch_id"] = result["batch_id"]
        if structured_artifacts_enabled(state):
            state["active_batch_artifact_root"] = batch_artifact_root(state, result["batch_id"])
            state["batch_manifest_path"] = batch_manifest_path(state, result["batch_id"])
    if result["dispatch_path"]:
        state["dispatch_path"] = result["dispatch_path"]
    if result["spec_path"]:
        state["spec_path"] = result["spec_path"]
    record_artifact_batch(state, result)

    if result["status"] != "completed":
        state["stop_reason"] = result["stop_reason"] or result["status"]
        return

    if phase == "closeout":
        state["batches_completed"] += 1
        if result["next_phase"] == "select-dispatch":
            state["active_batch_id"] = None
            state["dispatch_path"] = None
            state["spec_path"] = None
            state["active_batch_artifact_root"] = None
            state["batch_manifest_path"] = None

    if result["next_phase"] in PHASES:
        state["active_phase"] = result["next_phase"]
    else:
        state["stop_reason"] = result["next_phase"]


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
    entry["status"] = result["status"]


def write_artifact_manifests(
    config: RunnerConfig, state: dict[str, Any], result: dict[str, Any]
) -> None:
    if not structured_artifacts_enabled(state):
        return
    manifest_path = run_manifest_path(state)
    if manifest_path:
        write_json_object(
            resolve_project_path(config.project, manifest_path),
            build_run_manifest(config, state),
        )
    batch_id = result.get("batch_id") or state.get("active_batch_id")
    if isinstance(batch_id, str) and batch_id:
        write_batch_artifacts(config, state, batch_id)


def build_run_manifest(config: RunnerConfig, state: dict[str, Any]) -> dict[str, Any]:
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


def write_batch_artifacts(config: RunnerConfig, state: dict[str, Any], batch_id: str) -> None:
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


def build_batch_index(
    config: RunnerConfig, state: dict[str, Any], batch_id: str, batch_root: Path
) -> str:
    entry = artifact_batch_entry(state, batch_id)
    lines = [
        f"# {batch_id} Runner Artifacts",
        "",
        f"- Program ledger: {relative_project_link(config, batch_root, state['program_ledger'])}",
    ]
    dispatch_path = entry.get("dispatch_path") or state.get("dispatch_path")
    spec_path = entry.get("spec_path") or state.get("spec_path")
    if dispatch_path:
        lines.append(f"- Dispatch packet: {relative_project_link(config, batch_root, dispatch_path)}")
    if spec_path:
        lines.append(f"- Runway spec: {relative_project_link(config, batch_root, spec_path)}")
    lines.extend(
        [
            f"- Run state: {relative_project_link(config, batch_root, project_relative(config.project, config.state_path))}",
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


def relative_project_link(config: RunnerConfig, from_dir: Path, value: str) -> str:
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
    config: RunnerConfig,
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
        "batch_id": result.get("batch_id") if result else state.get("active_batch_id"),
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
    config: RunnerConfig, state: dict[str, Any], result: dict[str, Any] | None
) -> list[dict[str, Any]]:
    values = [state.get("program_ledger"), state.get("dispatch_path"), state.get("spec_path")]
    if result:
        values.extend([result.get("dispatch_path"), result.get("spec_path"), result.get("receipt_path")])
    inventory = phase_input_inventory_path(state, result["phase"]) if result else None
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
    if result and result.get("batch_id"):
        entry = artifact_batch_entry(state, result["batch_id"])
        telemetry = entry.setdefault("telemetry", {})
        if isinstance(telemetry, dict):
            telemetry[result["phase"]] = path


def write_phase_telemetry(config: RunnerConfig, path: str, telemetry: dict[str, Any]) -> None:
    write_json_object(resolve_project_path(config.project, path), telemetry)


def write_run_telemetry(config: RunnerConfig, state: dict[str, Any]) -> None:
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


def build_run_telemetry(
    config: RunnerConfig, state: dict[str, Any], phases: list[dict[str, Any]]
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


def is_terminal_completed_state(state: dict[str, Any]) -> bool:
    return state.get("last_phase_status") == "completed" and state.get(
        "stop_reason"
    ) in {"done", "max_batches_reached"}


def run(
    config: RunnerConfig,
    *,
    phase_executor: Callable[[RunnerConfig, dict[str, Any], str], dict[str, Any]] = execute_codex_phase,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
) -> dict[str, Any]:
    state = load_state(config.state_path) if config.resume else initial_state(config)
    validate_state_matches_config(state, config)

    if config.dry_run:
        print_dry_run(config, state)
        return state

    while True:
        if is_terminal_completed_state(state):
            return state
        if (
            config.max_batches is not None
            and state["batches_completed"] >= config.max_batches
        ):
            state["stop_reason"] = "max_batches_reached"
            write_state(config.state_path, state)
            return state

        phase = state["active_phase"]
        phase_telemetry_path: str | None = None
        phase_started_at: str | None = None
        phase_start_monotonic: float | None = None
        phase_prompt_bytes = 0
        result: dict[str, Any] | None = None
        try:
            check_required_artifacts(config, state)
            check_worktree(config, state, phase, status_reader=status_reader)
            phase_telemetry_path = next_phase_telemetry_path(state, phase)
            phase_started_at = utc_now()
            phase_start_monotonic = time.monotonic()
            phase_prompt_bytes = len(build_prompt(config, state, phase).encode("utf-8"))
            result = phase_executor(config, state, phase)
            execution_meta = pop_phase_execution_meta(state)
            apply_execution_meta_to_state(state, execution_meta)
            validate_phase_result(result, current_phase=phase, state=state)
            validate_receipt(result, config, state)
            if phase == "execute":
                check_worktree(
                    config,
                    state,
                    "closeout",
                    status_reader=status_reader,
                    extra_paths=[result["receipt_path"], *result["evidence_paths"]],
                )
        except RunnerError as exc:
            execution_meta = pop_phase_execution_meta(state)
            apply_execution_meta_to_state(state, execution_meta)
            state["last_phase_status"] = "failed"
            state["stop_reason"] = str(exc)
            if phase_telemetry_path and phase_started_at and phase_start_monotonic is not None:
                telemetry = build_phase_telemetry(
                    config,
                    state,
                    phase,
                    started_at=phase_started_at,
                    elapsed_seconds=round(time.monotonic() - phase_start_monotonic, 3),
                    prompt_bytes=phase_prompt_bytes,
                    result=result,
                    status="failed",
                    error=str(exc),
                    execution_meta=execution_meta,
                )
                write_phase_telemetry(config, phase_telemetry_path, telemetry)
                record_phase_telemetry_path(state, phase_telemetry_path, result)
                write_run_telemetry(config, state)
            write_state(config.state_path, state)
            raise

        apply_phase_result(state, result)
        if phase_telemetry_path and phase_started_at and phase_start_monotonic is not None:
            telemetry = build_phase_telemetry(
                config,
                state,
                phase,
                started_at=phase_started_at,
                elapsed_seconds=round(time.monotonic() - phase_start_monotonic, 3),
                prompt_bytes=phase_prompt_bytes,
                result=result,
                status=result["status"],
                error=None,
                execution_meta=execution_meta,
            )
            write_phase_telemetry(config, phase_telemetry_path, telemetry)
            record_phase_telemetry_path(state, phase_telemetry_path, result)
            write_run_telemetry(config, state)
        write_state(config.state_path, state)
        write_artifact_manifests(config, state, result)

        if config.stop_after_phase == phase:
            return state
        if result["status"] != "completed" or result["next_phase"] in {"done", "stopped"}:
            return state


def validate_state_matches_config(state: dict[str, Any], config: RunnerConfig) -> None:
    if Path(str(state.get("project"))).expanduser().resolve() != config.project:
        raise RunnerError("state project contradicts CLI project")
    if state.get("program_ledger") != config.program_ledger:
        raise RunnerError("state program_ledger contradicts CLI program-ledger")
    if state.get("max_batches") != config.max_batches:
        raise RunnerError("state max_batches contradicts CLI max-batches")
    if state.get("execute_batches") != config.execute_batches:
        raise RunnerError("state execute_batches contradicts CLI execute-batches")


def build_final_summary(state: dict[str, Any], config: RunnerConfig) -> dict[str, Any]:
    receipt: dict[str, Any] = {}
    receipt_path = state.get("last_receipt_path")
    if isinstance(receipt_path, str) and receipt_path:
        try:
            receipt = read_json_object(resolve_project_path(config.project, receipt_path))
        except RunnerError:
            receipt = {}

    return {
        "state_path": str(config.state_path),
        "artifact_root": state.get("artifact_root"),
        "run_telemetry_path": run_telemetry_path(state),
        "last_phase_telemetry_path": state.get("last_phase_telemetry_path"),
        "last_receipt_path": receipt_path,
        "stop_reason": state.get("stop_reason"),
        "batches_completed": state.get("batches_completed"),
        "active_batch": state.get("active_batch_id"),
        "dispatch_path": state.get("dispatch_path"),
        "spec_path": state.get("spec_path"),
        "commit_range": receipt.get("commit_range"),
        "validation_summary": receipt.get("validation_summary"),
        "review_summary": receipt.get("review_summary"),
    }


def print_final_summary(state: dict[str, Any], config: RunnerConfig) -> None:
    print("Final summary:")
    print(json.dumps(build_final_summary(state, config), indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = config_from_args(args)
    try:
        state = run(config)
    except RunnerError as exc:
        print(f"runner error: {exc}", file=sys.stderr)
        try:
            state = load_state(config.state_path)
        except RunnerError:
            state = initial_state(config)
            state["stop_reason"] = str(exc)
        print_final_summary(state, config)
        return 1
    if not config.dry_run:
        print_final_summary(state, config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
