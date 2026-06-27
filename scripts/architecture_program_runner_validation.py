"""Phase-result, receipt, and schema-adjacent validation for the runner."""

from __future__ import annotations

from typing import Any

try:
    from scripts import architecture_program_runner_input_inventory as _input_inventory
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_input_inventory as _input_inventory
    import architecture_program_runner_state as _runner_state

PHASES = _runner_state.PHASES
RunnerError = _runner_state.RunnerError
phase_receipt_path = _runner_state.phase_receipt_path
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path
resolve_project_relative_input_path = _input_inventory.resolve_project_relative_path
validate_expected_input_inventory_path = (
    _input_inventory.validate_expected_input_inventory_path
)
validate_input_inventory = _input_inventory.validate_input_inventory
validate_input_inventory_evidence = _input_inventory.validate_input_inventory_evidence
validate_input_inventory_file = _input_inventory.validate_input_inventory_file

NEXT_PHASES = (*PHASES, "done", "stopped")
STATUSES = ("completed", "stopped", "failed")
REQUIRED_RESULT_FIELDS = (
    "status",
    "phase",
    "next_phase",
    "stop_reason",
    "program_ledger",
    "batch_id",
    "dispatch_path",
    "spec_path",
    "receipt_path",
    "commit_range",
    "validation_summary",
    "review_summary",
    "evidence_paths",
)
UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS = {
    "allOf",
    "anyOf",
    "oneOf",
    "not",
    "if",
    "then",
    "else",
}


def validate_phase_result(
    result: dict[str, Any],
    *,
    current_phase: str | None = None,
    state: dict[str, Any] | None = None,
) -> None:
    missing = [field for field in REQUIRED_RESULT_FIELDS if field not in result]
    if missing:
        raise RunnerError(f"phase result missing required field(s): {', '.join(missing)}")

    extra = sorted(set(result) - set(REQUIRED_RESULT_FIELDS))
    if extra:
        raise RunnerError(f"phase result has unsupported field(s): {', '.join(extra)}")

    if result["status"] not in STATUSES:
        raise RunnerError(f"invalid phase status: {result['status']!r}")
    if result["phase"] not in PHASES:
        raise RunnerError(f"invalid phase: {result['phase']!r}")
    if result["next_phase"] not in NEXT_PHASES:
        raise RunnerError(f"invalid next_phase: {result['next_phase']!r}")

    if current_phase is not None and result["phase"] != current_phase:
        raise RunnerError(
            f"phase result phase {result['phase']!r} does not match active phase {current_phase!r}"
        )

    validate_nullable_string(result, "stop_reason")
    validate_required_string(result, "program_ledger")
    validate_nullable_string(result, "batch_id")
    validate_nullable_string(result, "dispatch_path")
    validate_nullable_string(result, "spec_path")
    validate_required_string(result, "receipt_path")
    validate_nullable_string(result, "commit_range")
    validate_summary(result, "validation_summary")
    validate_summary(result, "review_summary")

    evidence_paths = result["evidence_paths"]
    if not isinstance(evidence_paths, list) or not all(
        isinstance(path, str) for path in evidence_paths
    ):
        raise RunnerError("evidence_paths must be an array of strings")

    status = result["status"]
    next_phase = result["next_phase"]
    if status in {"stopped", "failed"} and next_phase != "stopped":
        raise RunnerError(f"status={status} must use next_phase=stopped")
    if status == "completed" and next_phase == "stopped":
        raise RunnerError("status=completed must not use next_phase=stopped")

    if state is not None:
        validate_result_against_state(result, state)


def validate_required_string(result: dict[str, Any], field: str) -> None:
    value = result[field]
    if not isinstance(value, str) or not value:
        raise RunnerError(f"{field} must be a non-empty string")


def validate_nullable_string(result: dict[str, Any], field: str) -> None:
    value = result[field]
    if value is not None and not isinstance(value, str):
        raise RunnerError(f"{field} must be a string or null")


def validate_summary(result: dict[str, Any], field: str) -> None:
    value = result[field]
    if value is not None and not isinstance(value, str):
        raise RunnerError(f"{field} must be a string or null")


def validate_result_against_state(result: dict[str, Any], state: dict[str, Any]) -> None:
    if result["program_ledger"] != state["program_ledger"]:
        raise RunnerError("phase result program_ledger contradicts runner state")

    if result["batch_id"] and state.get("active_batch_id"):
        if result["batch_id"] != state["active_batch_id"]:
            raise RunnerError("phase result batch_id contradicts runner state")
    if result["dispatch_path"] and state.get("dispatch_path"):
        if result["dispatch_path"] != state["dispatch_path"]:
            raise RunnerError("phase result dispatch_path contradicts runner state")
    if result["spec_path"] and state.get("spec_path"):
        if result["spec_path"] != state["spec_path"]:
            raise RunnerError("phase result spec_path contradicts runner state")

    status = result["status"]
    if status != "completed":
        return

    expected = expected_next_phases(result["phase"], state)
    if result["next_phase"] not in expected:
        allowed = ", ".join(sorted(expected))
        raise RunnerError(
            f"phase {result['phase']} cannot advance to {result['next_phase']}; "
            f"expected one of: {allowed}"
        )


def expected_next_phases(phase: str, state: dict[str, Any]) -> set[str]:
    if phase == "select-dispatch":
        return {"create-spec"}
    if phase == "create-spec":
        return {"execute"} if state.get("execute_batches") else {"done"}
    if phase == "execute":
        return {"closeout"}
    if phase == "closeout":
        max_batches = state.get("max_batches")
        completed = int(state.get("batches_completed", 0)) + 1
        if max_batches is not None and completed >= int(max_batches):
            return {"done"}
        return {"select-dispatch", "done"}
    raise RunnerError(f"unknown phase: {phase}")


def validate_expected_receipt_path(
    result: dict[str, Any], config: Any, state: dict[str, Any]
) -> None:
    expected = phase_receipt_path(state, result["phase"])
    if expected is None:
        return
    expected_path = resolve_project_path(config.project, expected).resolve()
    actual_path = resolve_project_path(config.project, result["receipt_path"]).resolve()
    if actual_path != expected_path:
        raise RunnerError(
            "phase result receipt_path must match runner-provided expected path: "
            f"{expected}"
        )


def validate_receipt(result: dict[str, Any], config: Any, state: dict[str, Any]) -> None:
    validate_expected_receipt_path(result, config, state)
    receipt_path = resolve_project_path(config.project, result["receipt_path"])
    receipt = read_json_object(receipt_path)
    validate_phase_result(receipt, current_phase=result["phase"], state=state)
    if receipt != result:
        raise RunnerError("receipt content does not match final phase result")
    validate_input_inventory_evidence(config.project, result, state)


def schema_keyword_paths(value: Any, path: str = "$") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS:
                paths.append(child_path)
            paths.extend(schema_keyword_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(schema_keyword_paths(child, f"{path}[{index}]"))
    return paths


def schema_subset_violations(value: Any, path: str = "$") -> list[str]:
    violations: list[str] = []
    if isinstance(value, dict):
        schema_type = value.get("type")
        schema_types = schema_type if isinstance(schema_type, list) else [schema_type]
        if "object" in schema_types and value.get("additionalProperties") is not False:
            violations.append(f"{path}: object schemas must set additionalProperties=false")
        if "array" in schema_types and "items" not in value:
            violations.append(f"{path}: array schemas must define items")
        for key, child in value.items():
            violations.extend(schema_subset_violations(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            violations.extend(schema_subset_violations(child, f"{path}[{index}]"))
    return violations
