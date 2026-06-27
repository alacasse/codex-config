"""Path, artifact, and state helpers for the architecture program runner."""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


RUNNER_VERSION = "local-runner-v1"
PHASES = ("select-dispatch", "create-spec", "execute", "closeout")
PHASE_RECEIPT_NAMES = {
    "create-spec": "02-create-spec.json",
    "execute": "03-execute.json",
    "closeout": "04-closeout.json",
}


class RunnerError(RuntimeError):
    """Raised for runner failures that should stop safely."""


def resolve_state_path(
    project: Path, program_ledger: str, value: str | None, *, resume: bool = False
) -> tuple[Path, Path | None]:
    if value:
        path = Path(value).expanduser()
        state_path = path if path.is_absolute() else project / path
        artifact_root = artifact_root_from_state_path(state_path)
        return state_path, artifact_root
    if resume:
        discovered = discover_resume_state_path(project, program_ledger)
        if discovered is not None:
            artifact_root = artifact_root_from_state_path(discovered)
            return discovered, artifact_root
    run_id = new_run_id()
    artifact_root = default_artifact_root(project, program_ledger, run_id)
    return artifact_root / "run-state.json", artifact_root


def legacy_state_path(project: Path, program_ledger: str) -> Path:
    return project / Path(program_ledger).parent / "architecture-program-run-state.json"


def artifact_root_from_state_path(state_path: Path) -> Path | None:
    if state_path.name != "run-state.json":
        return None
    if "architecture-program-runs" not in state_path.parts:
        return None
    return state_path.parent


def discover_resume_state_path(project: Path, program_ledger: str) -> Path | None:
    root = project / Path(program_ledger).parent / "architecture-program-runs" / ledger_slug(
        program_ledger
    )
    candidates = sorted(root.glob("run-*/run-state.json")) if root.exists() else []
    if candidates:
        return candidates[-1]
    legacy = legacy_state_path(project, program_ledger)
    return legacy if legacy.exists() else None


def default_artifact_root(project: Path, program_ledger: str, run_id: str) -> Path:
    return project / Path(program_ledger).parent / "architecture-program-runs" / ledger_slug(
        program_ledger
    ) / run_id


def ledger_slug(program_ledger: str) -> str:
    return slugify_path_component(Path(program_ledger).stem)


def new_run_id(initial_batch_id: str | None = None) -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    if initial_batch_id:
        return f"run-{timestamp}-{slugify_path_component(initial_batch_id)}"
    return f"run-{timestamp}"


def slugify_path_component(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip(".-")
    return slug or "unnamed"


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def initial_state(config: Any) -> dict[str, Any]:
    state: dict[str, Any] = {
        "schema_version": 1,
        "runner_version": RUNNER_VERSION,
        "project": str(config.project),
        "program_ledger": config.program_ledger,
        "max_batches": config.max_batches,
        "execute_batches": config.execute_batches,
        "batches_completed": 0,
        "active_phase": "select-dispatch",
        "active_batch_id": None,
        "dispatch_path": None,
        "spec_path": None,
        "last_receipt_path": None,
        "last_codex_session": None,
        "last_phase_status": None,
        "stop_reason": None,
        "updated_at": None,
    }
    if config.artifact_root is not None:
        artifact_root = project_relative(config.project, config.artifact_root)
        state.update(
            {
                "run_id": config.artifact_root.name,
                "artifact_root": artifact_root,
                "active_batch_artifact_root": None,
                "run_manifest_path": f"{artifact_root}/run-manifest.json",
                "batch_manifest_path": None,
                "run_telemetry_path": f"{artifact_root}/telemetry/run-telemetry.json",
                "last_phase_telemetry_path": None,
                "phase_telemetry_paths": [],
                "artifact_batches": [],
            }
        )
    return state


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunnerError(f"state file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunnerError(f"state file is not valid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"state file must contain a JSON object: {path}")
    validate_state(data)
    return data


def validate_state(state: dict[str, Any]) -> None:
    if state.get("schema_version") != 1:
        raise RunnerError("state schema_version must be 1")
    if state.get("runner_version") != RUNNER_VERSION:
        raise RunnerError(f"state runner_version must be {RUNNER_VERSION}")
    if state.get("active_phase") not in PHASES:
        raise RunnerError("state active_phase is invalid")
    max_batches = state.get("max_batches")
    if max_batches is not None:
        if not isinstance(max_batches, int) or max_batches < 1:
            raise RunnerError("state max_batches must be a positive integer or null")
    if not isinstance(state.get("batches_completed"), int):
        raise RunnerError("state batches_completed must be an integer")
    if state["batches_completed"] < 0:
        raise RunnerError("state batches_completed must be non-negative")
    for field in (
        "run_id",
        "artifact_root",
        "active_batch_artifact_root",
        "run_manifest_path",
        "batch_manifest_path",
        "run_telemetry_path",
        "last_phase_telemetry_path",
    ):
        value = state.get(field)
        if value is not None and not isinstance(value, str):
            raise RunnerError(f"state {field} must be a string or null")
    for field in ("artifact_batches", "phase_telemetry_paths"):
        value = state.get(field)
        if value is not None and not isinstance(value, list):
            raise RunnerError(f"state {field} must be an array when present")


def write_state(path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    write_json_object(path, state)


def write_json_object(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        tmp_path = Path(handle.name)
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp_path, path)


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunnerError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunnerError(f"JSON file is malformed: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"JSON file must contain an object: {path}")
    return data


def resolve_project_path(project: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else project / path


def project_relative(project: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(project.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def structured_artifacts_enabled(state: dict[str, Any]) -> bool:
    return bool(state.get("artifact_root"))


def run_manifest_path(state: dict[str, Any]) -> str | None:
    artifact_root = state.get("artifact_root")
    if not isinstance(artifact_root, str) or not artifact_root:
        return None
    value = state.get("run_manifest_path")
    if isinstance(value, str) and value:
        return value
    return f"{artifact_root}/run-manifest.json"


def batch_artifact_root(state: dict[str, Any], batch_id: str) -> str | None:
    artifact_root = state.get("artifact_root")
    if not isinstance(artifact_root, str) or not artifact_root:
        return None
    return f"{artifact_root}/batches/{slugify_path_component(batch_id)}"


def batch_manifest_path(state: dict[str, Any], batch_id: str) -> str | None:
    root = batch_artifact_root(state, batch_id)
    return f"{root}/batch-manifest.json" if root else None


def run_telemetry_path(state: dict[str, Any]) -> str | None:
    artifact_root = state.get("artifact_root")
    if not isinstance(artifact_root, str) or not artifact_root:
        return None
    value = state.get("run_telemetry_path")
    if isinstance(value, str) and value:
        return value
    return f"{artifact_root}/telemetry/run-telemetry.json"


def next_phase_telemetry_path(state: dict[str, Any], phase: str) -> str | None:
    artifact_root = state.get("artifact_root")
    if not isinstance(artifact_root, str) or not artifact_root:
        return None
    paths = state.get("phase_telemetry_paths")
    sequence = len(paths) + 1 if isinstance(paths, list) else 1
    return f"{artifact_root}/telemetry/phases/{sequence:02d}-{phase}.telemetry.json"


def phase_receipt_path(state: dict[str, Any], phase: str) -> str | None:
    artifact_root = state.get("artifact_root")
    if not isinstance(artifact_root, str) or not artifact_root:
        return None
    if phase == "select-dispatch" and not state.get("active_batch_id"):
        select_index = int(state.get("batches_completed", 0)) + 1
        return f"{artifact_root}/receipts/{select_index:02d}-select-dispatch.json"

    batch_id = state.get("active_batch_id")
    if not isinstance(batch_id, str) or not batch_id:
        return None
    if phase == "select-dispatch":
        receipt_name = "01-select-dispatch.json"
    else:
        receipt_name = PHASE_RECEIPT_NAMES[phase]
    root = batch_artifact_root(state, batch_id)
    return f"{root}/receipts/{receipt_name}" if root else None


def phase_input_inventory_path(state: dict[str, Any], phase: str) -> str | None:
    telemetry_path = next_phase_telemetry_path(state, phase)
    if telemetry_path is None:
        return None
    return telemetry_path.replace(".telemetry.json", ".input-inventory.json")
