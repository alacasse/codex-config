"""Input inventory validation for architecture-program runner phases."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_state as _runner_state

RunnerError = _runner_state.RunnerError
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path

INVENTORY_SCHEMA_VERSION = 1
INVENTORY_FIELDS = (
    "schema_version",
    "phase",
    "primary_inputs",
    "broad_reads",
    "large_file_reads",
    "subagent_reports",
)
INVENTORY_SECTIONS = (
    "primary_inputs",
    "broad_reads",
    "large_file_reads",
    "subagent_reports",
)
SECTION_ENTRY_FIELDS = {
    "primary_inputs": frozenset(("path", "reason")),
    "broad_reads": frozenset(("path", "command", "reason")),
    "large_file_reads": frozenset(("path", "byte_count", "reason")),
    "subagent_reports": frozenset(("path", "role", "reason")),
}
STRING_ENTRY_FIELDS = frozenset(("path", "command", "reason", "role"))
INTEGER_ENTRY_FIELDS = frozenset(("byte_count",))
PROJECT_RELATIVE_ENTRY_FIELDS = frozenset(("path",))


def validate_input_inventory(inventory: Any, *, active_phase: str) -> None:
    """Validate a phase-reported input inventory object."""

    if not isinstance(inventory, dict):
        raise RunnerError("input inventory must be a JSON object")

    missing = [field for field in INVENTORY_FIELDS if field not in inventory]
    if missing:
        raise RunnerError(f"input inventory missing required field(s): {', '.join(missing)}")

    extra = sorted(set(inventory) - set(INVENTORY_FIELDS))
    if extra:
        raise RunnerError(f"input inventory has unsupported field(s): {', '.join(extra)}")

    if (
        type(inventory["schema_version"]) is not int
        or inventory["schema_version"] != INVENTORY_SCHEMA_VERSION
    ):
        raise RunnerError(
            f"input inventory schema_version must be {INVENTORY_SCHEMA_VERSION}"
        )
    if not isinstance(inventory["phase"], str):
        raise RunnerError("input inventory phase must be a string")
    if inventory["phase"] != active_phase:
        raise RunnerError("input inventory phase does not match active phase")

    for section in INVENTORY_SECTIONS:
        validate_inventory_section(section, inventory[section])


def validate_inventory_section(section: str, entries: Any) -> None:
    if not isinstance(entries, list):
        raise RunnerError(f"input inventory {section} must be an array")

    allowed_fields = SECTION_ENTRY_FIELDS[section]
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RunnerError(f"input inventory {section}[{index}] must be an object")

        extra = sorted(set(entry) - allowed_fields)
        if extra:
            raise RunnerError(
                f"input inventory {section}[{index}] has unsupported field(s): "
                f"{', '.join(extra)}"
            )

        for field, value in entry.items():
            field_path = f"{section}[{index}].{field}"
            if field in STRING_ENTRY_FIELDS:
                validate_string_field(field_path, value)
            if field in INTEGER_ENTRY_FIELDS:
                validate_integer_field(field_path, value)
            if field in PROJECT_RELATIVE_ENTRY_FIELDS:
                validate_project_relative_path(field_path, value)


def validate_string_field(field_path: str, value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise RunnerError(f"input inventory {field_path} must be a non-empty string")


def validate_integer_field(field_path: str, value: Any) -> None:
    if type(value) is not int:
        raise RunnerError(f"input inventory {field_path} must be an integer")


def validate_project_relative_path(field_path: str, value: str) -> None:
    path = Path(value)
    if path.parts and path.parts[0].startswith("~"):
        raise RunnerError(f"input inventory {field_path} must be project-relative")
    if path.is_absolute():
        raise RunnerError(f"input inventory {field_path} must be project-relative")
    if any(part == ".." for part in path.parts):
        raise RunnerError(f"input inventory {field_path} must not escape the project")


def resolve_project_relative_path(project: Path, value: str) -> Path:
    validate_project_relative_path("path", value)
    path = resolve_project_path(project, value)
    try:
        path.resolve().relative_to(project.resolve())
    except ValueError as exc:
        raise RunnerError("input inventory path must stay within the project") from exc
    return path


def validate_input_inventory_file(
    project: Path,
    inventory_path: str,
    *,
    active_phase: str,
) -> dict[str, Any]:
    inventory = read_json_object(resolve_project_relative_path(project, inventory_path))
    validate_input_inventory(inventory, active_phase=active_phase)
    return inventory


def validate_expected_input_inventory_path(
    actual_path: str | None,
    expected_path: str | None,
) -> None:
    if expected_path is None:
        return
    if actual_path != expected_path:
        raise RunnerError(
            "input inventory path must match runner-provided expected path: "
            f"{expected_path}"
        )
