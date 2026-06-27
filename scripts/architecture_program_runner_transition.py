"""Phase Transition ownership for architecture-program runner state changes."""

from __future__ import annotations

from typing import Any

try:
    from scripts import architecture_program_runner_artifacts as _runner_artifacts
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_artifacts as _runner_artifacts
    import architecture_program_runner_state as _runner_state

PHASES = _runner_state.PHASES
batch_artifact_root = _runner_state.batch_artifact_root
batch_manifest_path = _runner_state.batch_manifest_path
structured_artifacts_enabled = _runner_state.structured_artifacts_enabled
record_artifact_batch = _runner_artifacts.record_artifact_batch


def apply_phase_transition(state: dict[str, Any], result: dict[str, Any]) -> None:
    """Apply a schema-valid Phase Result to Run State."""
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


def is_terminal_phase_transition_state(state: dict[str, Any]) -> bool:
    return state.get("last_phase_status") == "completed" and state.get(
        "stop_reason"
    ) in {"done", "max_batches_reached"}
