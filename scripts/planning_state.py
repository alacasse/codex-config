"""Read-only Planning Artifact Layout v1 state model."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


NONE_VALUES = {"", "none", "none selected", "n/a", "tbd"}
FIELD_PATTERN = re.compile(r"^(?:-\s*)?([^:|]+):\s*(.*)$")
PLANNING_STATE_PROTOCOL_NAME = "planning-state-facts"
PLANNING_STATE_PROTOCOL_VERSION = 1
STATE_FIXTURE_SCHEMA_NAME = "planning-state-tool-state"
RECEIPT_FIXTURE_SCHEMA_NAME = "planning-state-transition-receipt"
SUPPORTED_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ArtifactPointer:
    label: str
    value: str | None
    source_path: Path
    exists: bool | None = None


@dataclass(frozen=True)
class RedirectEvidence:
    source_path: Path
    target_path: str | None
    current_state_path: str | None = None


@dataclass(frozen=True)
class StateWarning:
    code: str
    message: str
    source_path: Path | None = None


@dataclass(frozen=True)
class ValidationMessage:
    severity: str
    code: str
    message: str
    source_path: Path | None = None


@dataclass(frozen=True)
class ProgramState:
    slug: str
    current_path: Path
    purpose: str | None
    ledger: ArtifactPointer
    selected_dispatch: ArtifactPointer
    active_runway: ArtifactPointer
    queued_batch: ArtifactPointer
    latest_closeout: ArtifactPointer
    run_artifact_location: ArtifactPointer
    archive_location: ArtifactPointer
    next_safe_action: str | None
    stop_conditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class RootState:
    root_path: Path
    current_path: Path
    layout: str | None
    planning_root: str | None
    run_artifact_root: str | None
    output_root: str | None
    one_shot_intake: str | None
    program_archive_root: str | None
    active_programs: tuple[ArtifactPointer, ...]
    next_safe_action: str | None


@dataclass(frozen=True)
class PlanningState:
    root: RootState
    programs: tuple[ProgramState, ...]
    redirects: tuple[RedirectEvidence, ...] = ()
    warnings: tuple[StateWarning, ...] = ()
    validation_messages: tuple[ValidationMessage, ...] = ()


class ProtocolValidationError(ValueError):
    """Raised when a machine-readable planning-state object is malformed."""


def load_planning_state(root: str | Path) -> PlanningState:
    """Load Planning Artifact Layout v1 state without mutating files."""

    root_path = Path(root)
    root_current = root_path / "CURRENT.md"
    root_text = _read_text(root_current)
    root_fields = _field_map(root_text)
    active_programs = _active_programs(root_text, root_current)
    root_state = RootState(
        root_path=root_path,
        current_path=root_current,
        layout=root_fields.get("layout"),
        planning_root=root_fields.get("planning root"),
        run_artifact_root=root_fields.get("run artifact root"),
        output_root=root_fields.get("output root"),
        one_shot_intake=root_fields.get("one-shot intake"),
        program_archive_root=root_fields.get("program archive root"),
        active_programs=tuple(active_programs),
        next_safe_action=_next_safe_action(root_text, root_fields),
    )

    programs = tuple(_load_program(root_path, pointer) for pointer in active_programs)
    redirects = tuple(_redirects(root_path))
    warnings = tuple(_warnings(root_path, root_state, programs, redirects))
    validation_messages = tuple(_validation_messages(root_state, programs, redirects))
    return PlanningState(
        root=root_state,
        programs=programs,
        redirects=redirects,
        warnings=warnings,
        validation_messages=validation_messages,
    )


def _load_program(root_path: Path, pointer: ArtifactPointer) -> ProgramState:
    current_path = _resolve_pointer(root_path, pointer.value)
    text = _read_text(current_path)
    fields = _field_map(text)
    slug = fields.get("program slug") or pointer.label
    return ProgramState(
        slug=slug,
        current_path=current_path,
        purpose=fields.get("purpose"),
        ledger=_artifact("current ledger", fields, current_path, root_path),
        selected_dispatch=_artifact("selected dispatch path", fields, current_path, root_path),
        active_runway=_artifact("active batch runway spec path", fields, current_path, root_path),
        queued_batch=_artifact("queued batch path or id", fields, current_path, root_path),
        latest_closeout=_artifact(("latest closeout path", "latest closeout"), fields, current_path, root_path),
        run_artifact_location=_artifact("run artifact location", fields, current_path, root_path),
        archive_location=_artifact("program archive location", fields, current_path, root_path),
        next_safe_action=_next_safe_action(text, fields),
        stop_conditions=tuple(_list_items(_section_text(text, "Stop Conditions") or "")),
    )


def format_current_state(state: PlanningState) -> str:
    """Return compact agent-facing current-state text."""

    lines = [
        "planning_state:",
        f"  layout: {_display_value(state.root.layout)}",
        f"  planning_root: {_display_value(state.root.planning_root)}",
        f"  root: {state.root.root_path}",
        f"  current: {state.root.current_path}",
        f"  next_safe_action: {_display_value(state.root.next_safe_action)}",
        "  active_programs:",
    ]
    if not state.programs:
        lines.append("    []")
    for program in state.programs:
        lines.extend(_format_program(program))
    lines.extend(_format_warnings(state.warnings, state.validation_messages))
    lines.extend(_format_blockers(state.validation_messages))
    return "\n".join(lines) + "\n"


def format_validation_report(state: PlanningState) -> str:
    """Return a compact validation report for Planning Artifact Layout v1 state."""

    errors = [
        message for message in state.validation_messages if message.severity == "error"
    ]
    warnings = [
        *(
            ValidationMessage(
                "warning",
                warning.code,
                warning.message,
                warning.source_path,
            )
            for warning in state.warnings
        ),
        *(
            message
            for message in state.validation_messages
            if message.severity == "warning"
        ),
    ]
    lines = [
        "planning_state_validation:",
        f"  root: {state.root.root_path}",
        f"  status: {'failed' if errors else 'passed'}",
        "  errors:",
    ]
    lines.extend(_format_validation_messages(errors))
    lines.append("  warnings:")
    lines.extend(_format_validation_warnings(warnings))
    return "\n".join(lines) + "\n"


def format_protocol_report(
    state: PlanningState,
    *,
    command: str,
    exit_code: int,
    protocol_version: int = PLANNING_STATE_PROTOCOL_VERSION,
) -> str:
    """Return versioned machine-readable planning-state facts."""

    if protocol_version != PLANNING_STATE_PROTOCOL_VERSION:
        raise ProtocolValidationError(
            f"unsupported planning-state protocol version: {protocol_version}"
        )
    return json.dumps(
        _protocol_document(state, command=command, exit_code=exit_code),
        indent=2,
        sort_keys=True,
    ) + "\n"


def validate_state_fixture_object(value: object) -> dict[str, Any]:
    """Validate the minimal future write-transition state fixture schema."""

    data = _require_object(value, "state fixture")
    _require_protocol(data, STATE_FIXTURE_SCHEMA_NAME, "state fixture")
    _require_string(data, "root")
    programs = _require_array(data, "programs")
    for index, program in enumerate(programs):
        program_data = _require_object(program, f"programs[{index}]")
        _require_string(program_data, "slug")
        _require_optional_string(program_data, "current")
        _require_optional_string(program_data, "ledger")
        _require_optional_string(program_data, "selected_dispatch")
        _require_optional_string(program_data, "active_runway")
        _require_optional_string(program_data, "queued_batch")
        _require_optional_string(program_data, "latest_closeout")
    return data


def validate_receipt_fixture_object(value: object) -> dict[str, Any]:
    """Validate the minimal future write-transition receipt fixture schema."""

    data = _require_object(value, "receipt fixture")
    _require_protocol(data, RECEIPT_FIXTURE_SCHEMA_NAME, "receipt fixture")
    _require_string(data, "root")
    _require_string(data, "transition")
    _require_string(data, "status")
    messages = _require_array(data, "messages")
    for index, message in enumerate(messages):
        message_data = _require_object(message, f"messages[{index}]")
        _require_string(message_data, "severity")
        _require_string(message_data, "code")
        _require_string(message_data, "message")
        _require_optional_string(message_data, "source_path")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read Planning Artifact Layout v1 state without writing files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    current_parser = subparsers.add_parser(
        "current",
        help="Report active planning state from CURRENT.md files.",
    )
    current_parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Planning root containing CURRENT.md.",
    )
    current_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text for existing agent workflows.",
    )
    current_parser.add_argument(
        "--protocol-version",
        type=int,
        default=PLANNING_STATE_PROTOCOL_VERSION,
        help="Machine-readable protocol version for --format json.",
    )
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate active planning state without writing files.",
    )
    validate_parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Planning root containing CURRENT.md.",
    )
    validate_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text for existing agent workflows.",
    )
    validate_parser.add_argument(
        "--protocol-version",
        type=int,
        default=PLANNING_STATE_PROTOCOL_VERSION,
        help="Machine-readable protocol version for --format json.",
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "current":
            state = load_planning_state(args.root)
            exit_code = 0
            if args.format == "json":
                sys.stdout.write(
                    format_protocol_report(
                        state,
                        command="current",
                        exit_code=exit_code,
                        protocol_version=args.protocol_version,
                    )
                )
            else:
                sys.stdout.write(format_current_state(state))
            return exit_code
        if args.command == "validate":
            state = load_planning_state(args.root)
            exit_code = 1 if _has_validation_errors(state) else 0
            if args.format == "json":
                sys.stdout.write(
                    format_protocol_report(
                        state,
                        command="validate",
                        exit_code=exit_code,
                        protocol_version=args.protocol_version,
                    )
                )
            else:
                sys.stdout.write(format_validation_report(state))
            return exit_code
    except ProtocolValidationError as error:
        parser.exit(2, f"{parser.prog}: error: {error}\n")
    parser.error(f"unknown command: {args.command}")
    return 2


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _field_map(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()
        match = _field_match(line)
        if match:
            key = _normal_key(match.group(1))
            value_lines = [match.group(2).strip()]
            while index + 1 < len(lines):
                next_line = lines[index + 1].strip()
                if _ends_field_value(next_line):
                    break
                value_lines.append(next_line)
                index += 1
            value = _clean_value(" ".join(part for part in value_lines if part))
            fields[key] = value
        index += 1
    return fields


def _field_match(line: str) -> re.Match[str] | None:
    if line.startswith("|"):
        return None
    return FIELD_PATTERN.match(line)


def _ends_field_value(line: str) -> bool:
    return (
        not line
        or line.startswith("## ")
        or line.startswith("|")
        or _field_match(line) is not None
    )


def _active_programs(text: str, source_path: Path) -> list[ArtifactPointer]:
    programs: list[ArtifactPointer] = []
    in_table = False
    for line in text.splitlines():
        if line.strip().lower() == "## active programs":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.lstrip().startswith("|"):
            continue
        cells = [_clean_value(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in {"program", "---"}:
            continue
        programs.append(
            ArtifactPointer(
                label=cells[0],
                value=_none_to_null(cells[1]),
                source_path=source_path,
            )
        )
    return programs


def _artifact(
    label: str | tuple[str, ...],
    fields: dict[str, str],
    source_path: Path,
    root_path: Path,
) -> ArtifactPointer:
    labels = (label,) if isinstance(label, str) else label
    value = _none_to_null(next((fields[key] for key in labels if key in fields), None))
    exists = None
    if value is not None and "/" in value:
        exists = _resolve_pointer(root_path, value).exists()
    return ArtifactPointer(label=labels[0], value=value, source_path=source_path, exists=exists)


def _redirects(root_path: Path) -> Iterable[RedirectEvidence]:
    for path in sorted(root_path.glob("*.md")):
        if path.name in {"CURRENT.md", "README.md"}:
            continue
        text = _read_text(path)
        if not re.search(r"^#\s*Redirect:", text, re.MULTILINE):
            continue
        fields = _field_map(text)
        target = fields.get("new path") or _first_code_path_after(text, "moved to")
        current_state = fields.get("program current state")
        yield RedirectEvidence(path, target, current_state)


def _warnings(
    root_path: Path,
    root_state: RootState,
    programs: tuple[ProgramState, ...],
    redirects: tuple[RedirectEvidence, ...],
) -> Iterable[StateWarning]:
    active_paths = {root_state.current_path, *(program.current_path for program in programs)}
    for redirect in redirects:
        yield StateWarning(
            "redirect_ledger",
            f"{redirect.source_path.name} redirects to {redirect.target_path or 'an unknown target'}",
            redirect.source_path,
        )
    for path in sorted(root_path.glob("*pickup*.md")):
        if path not in active_paths:
            yield StateWarning(
                "stale_pickup_note",
                f"{path.name} is pickup evidence, not active state",
                path,
            )
    historical_patterns = ("*-runway.md", "dispatch/*.md")
    for pattern in historical_patterns:
        for path in sorted(root_path.glob(pattern)):
            if "programs" not in path.parts:
                yield StateWarning(
                    "historical_batch_artifact",
                    f"{path.relative_to(root_path)} is historical evidence, not active state",
                    path,
                )
    selected_values = [
        program.selected_dispatch.value or program.active_runway.value or program.queued_batch.value
        for program in programs
    ]
    if not any(selected_values) and any(root_path.glob("*pickup*.md")):
        yield StateWarning(
            "stale_pickup_contradiction",
            "pickup notes exist while CURRENT.md files select no active batch",
            root_path,
        )


def _validation_messages(
    root_state: RootState,
    programs: tuple[ProgramState, ...],
    redirects: tuple[RedirectEvidence, ...],
) -> Iterable[ValidationMessage]:
    if not root_state.current_path.exists():
        yield ValidationMessage("error", "missing_root_current", "root CURRENT.md is missing", root_state.current_path)
    if root_state.layout != "Planning Artifact Layout v1":
        yield ValidationMessage("warning", "unknown_layout", "layout is not Planning Artifact Layout v1", root_state.current_path)
    if not root_state.active_programs:
        yield ValidationMessage("warning", "no_active_programs", "root CURRENT.md lists no active programs", root_state.current_path)
    for pointer, program in zip(root_state.active_programs, programs, strict=False):
        if pointer.value and not program.current_path.exists():
            yield ValidationMessage("error", "missing_program_current", f"{pointer.value} is missing", root_state.current_path)
        if program.ledger.value and program.ledger.exists is False:
            yield ValidationMessage("error", "missing_program_ledger", f"{program.ledger.value} is missing", program.current_path)
        yield from _program_active_state_messages(program)
    for redirect in redirects:
        if not redirect.target_path:
            yield ValidationMessage("error", "redirect_without_target", "redirect has no target path", redirect.source_path)


def _format_program(program: ProgramState) -> list[str]:
    return [
        f"    - slug: {program.slug}",
        f"      current: {program.current_path}",
        f"      ledger: {_display_value(program.ledger.value)}",
        f"      selected_dispatch: {_display_value(program.selected_dispatch.value)}",
        f"      queued_batch: {_display_value(program.queued_batch.value)}",
        f"      active_runway: {_display_value(program.active_runway.value)}",
        f"      latest_closeout: {_display_value(program.latest_closeout.value)}",
        f"      next_safe_action: {_display_value(program.next_safe_action)}",
    ]


def _format_warnings(
    warnings: tuple[StateWarning, ...],
    messages: tuple[ValidationMessage, ...],
) -> list[str]:
    lines = ["  warnings:"]
    validation_warnings = [
        message for message in messages if message.severity == "warning"
    ]
    if not warnings and not validation_warnings:
        return [*lines, "    []"]
    grouped: dict[str, list[StateWarning]] = {}
    for warning in warnings:
        grouped.setdefault(warning.code, []).append(warning)
    for code, code_warnings in grouped.items():
        first = code_warnings[0]
        source = f" ({first.source_path})" if first.source_path else ""
        count = len(code_warnings)
        suffix = f"; {count} total" if count > 1 else ""
        lines.append(f"    - {code}: {first.message}{source}{suffix}")
    for message in validation_warnings:
        source = f" ({message.source_path})" if message.source_path else ""
        lines.append(f"    - {message.code}: {message.message}{source}")
    return lines


def _format_blockers(messages: tuple[ValidationMessage, ...]) -> list[str]:
    lines = ["  blockers:"]
    blockers = [message for message in messages if message.severity == "error"]
    if not blockers:
        return [*lines, "    []"]
    for message in blockers:
        source = f" ({message.source_path})" if message.source_path else ""
        lines.append(f"    - {message.code}: {message.message}{source}")
    return lines


def _format_validation_messages(messages: list[ValidationMessage]) -> list[str]:
    if not messages:
        return ["    []"]
    lines = []
    for message in messages:
        source = f" ({message.source_path})" if message.source_path else ""
        lines.append(f"    - {message.code}: {message.message}{source}")
    return lines


def _format_validation_warnings(messages: list[ValidationMessage]) -> list[str]:
    if not messages:
        return ["    []"]
    grouped: dict[str, list[ValidationMessage]] = {}
    for message in messages:
        grouped.setdefault(message.code, []).append(message)
    lines = []
    for code, code_messages in grouped.items():
        first = code_messages[0]
        source = f" ({first.source_path})" if first.source_path else ""
        count = len(code_messages)
        suffix = f"; {count} total" if count > 1 else ""
        lines.append(f"    - {code}: {first.message}{source}{suffix}")
    return lines


def _protocol_document(
    state: PlanningState,
    *,
    command: str,
    exit_code: int,
) -> dict[str, Any]:
    validation_messages = [
        _validation_message_object(message) for message in state.validation_messages
    ]
    blockers = [
        message
        for message in state.validation_messages
        if message.severity == "error"
    ]
    return {
        "protocol": {
            "name": PLANNING_STATE_PROTOCOL_NAME,
            "version": PLANNING_STATE_PROTOCOL_VERSION,
            "command": command,
        },
        "exit": {
            "code": exit_code,
            "meaning": _exit_code_meaning(exit_code),
            "semantics": {
                "0": "command completed; validate found no blockers",
                "1": "validate completed and found blockers",
                "2": "command usage or protocol negotiation failed",
            },
        },
        "root": {
            "path": str(state.root.root_path),
            "current": str(state.root.current_path),
            "layout": state.root.layout,
            "planning_root": state.root.planning_root,
            "run_artifact_root": state.root.run_artifact_root,
            "output_root": state.root.output_root,
            "one_shot_intake": state.root.one_shot_intake,
            "program_archive_root": state.root.program_archive_root,
            "active_programs": [
                _artifact_pointer_object(pointer)
                for pointer in state.root.active_programs
            ],
            "next_safe_action": state.root.next_safe_action,
        },
        "programs": [_program_object(program) for program in state.programs],
        "warnings": [
            _warning_object(warning) for warning in state.warnings
        ],
        "blockers": [
            _validation_message_object(message) for message in blockers
        ],
        "validation_messages": validation_messages,
    }


def _program_object(program: ProgramState) -> dict[str, Any]:
    return {
        "slug": program.slug,
        "current": str(program.current_path),
        "purpose": program.purpose,
        "ledger": _artifact_pointer_object(program.ledger),
        "selected_dispatch": _artifact_pointer_object(program.selected_dispatch),
        "active_runway": _artifact_pointer_object(program.active_runway),
        "queued_batch": _artifact_pointer_object(program.queued_batch),
        "latest_closeout": _artifact_pointer_object(program.latest_closeout),
        "run_artifact_location": _artifact_pointer_object(
            program.run_artifact_location
        ),
        "archive_location": _artifact_pointer_object(program.archive_location),
        "next_safe_action": program.next_safe_action,
        "stop_conditions": list(program.stop_conditions),
    }


def _artifact_pointer_object(pointer: ArtifactPointer) -> dict[str, Any]:
    return {
        "label": pointer.label,
        "value": pointer.value,
        "source_path": str(pointer.source_path),
        "exists": pointer.exists,
    }


def _warning_object(warning: StateWarning) -> dict[str, Any]:
    return {
        "severity": "warning",
        "code": warning.code,
        "message": warning.message,
        "source_path": _optional_path(warning.source_path),
    }


def _validation_message_object(message: ValidationMessage) -> dict[str, Any]:
    return {
        "severity": message.severity,
        "code": message.code,
        "message": message.message,
        "source_path": _optional_path(message.source_path),
    }


def _optional_path(path: Path | None) -> str | None:
    return str(path) if path is not None else None


def _exit_code_meaning(exit_code: int) -> str:
    if exit_code == 0:
        return "success"
    if exit_code == 1:
        return "validation_failed"
    return "usage_or_protocol_error"


def _require_protocol(data: dict[str, Any], name: str, context: str) -> None:
    protocol = _require_object(data.get("protocol"), f"{context}.protocol")
    actual_name = protocol.get("name")
    actual_version = protocol.get("version")
    if actual_name != name:
        raise ProtocolValidationError(
            f"{context}.protocol.name must be {name!r}"
        )
    if actual_version != SUPPORTED_SCHEMA_VERSION:
        raise ProtocolValidationError(
            f"{context}.protocol.version must be {SUPPORTED_SCHEMA_VERSION}"
        )


def _require_object(value: object, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolValidationError(f"{context} must be an object")
    return value


def _require_array(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ProtocolValidationError(f"{key} must be an array")
    return value


def _require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ProtocolValidationError(f"{key} must be a non-empty string")
    return value


def _require_optional_string(data: dict[str, Any], key: str) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ProtocolValidationError(f"{key} must be a string or null")
    return value


def _has_validation_errors(state: PlanningState) -> bool:
    return any(message.severity == "error" for message in state.validation_messages)


def _program_active_state_messages(program: ProgramState) -> Iterable[ValidationMessage]:
    active_pointers = (
        program.selected_dispatch,
        program.active_runway,
        program.queued_batch,
    )
    active_values = [pointer for pointer in active_pointers if pointer.value is not None]
    if len(active_values) > 1:
        yield ValidationMessage(
            "error",
            "multiple_active_artifacts",
            "program CURRENT.md selects more than one dispatch, runway, or queued batch",
            program.current_path,
        )
    yield from _required_existing_pointer(
        program.selected_dispatch,
        "invalid_selected_dispatch_path",
    )
    yield from _required_existing_pointer(
        program.active_runway,
        "invalid_active_runway_path",
    )
    yield from _required_existing_pointer(
        program.queued_batch,
        "invalid_queued_runway_path",
    )


def _required_existing_pointer(
    pointer: ArtifactPointer,
    code: str,
) -> Iterable[ValidationMessage]:
    if pointer.value is None or pointer.exists is not False:
        return
    yield ValidationMessage(
        "error",
        code,
        f"{pointer.value} is missing",
        pointer.source_path,
    )


def _resolve_pointer(root_path: Path, value: str | None) -> Path:
    if value is None:
        return root_path
    path = Path(value)
    if path.is_absolute():
        return path
    for width in range(min(len(path.parts), len(root_path.parts)), 0, -1):
        if path.parts[:width] == root_path.parts[-width:]:
            return root_path.joinpath(*path.parts[width:])
    return root_path / path


def _normal_key(value: str) -> str:
    return _clean_value(value).lower()


def _clean_value(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^`(.*)`$", r"\1", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _none_to_null(value: str | None) -> str | None:
    if value is None:
        return None
    value = _clean_value(value)
    if value.lower() in NONE_VALUES:
        return None
    return value


def _section_text(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    section_lines: list[str] = []
    in_section = False
    heading_marker = f"## {heading}".lower()
    for line in lines:
        if line.strip().lower() == heading_marker:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            section_lines.append(line)
    value = "\n".join(section_lines).strip()
    return value or None


def _next_safe_action(text: str, fields: dict[str, str]) -> str | None:
    return _section_text(text, "Next Safe Action") or fields.get("next safe action")


def _list_items(text: str) -> Iterable[str]:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            yield line[2:].strip()


def _first_code_path_after(text: str, marker: str) -> str | None:
    marker_index = text.lower().find(marker)
    if marker_index == -1:
        return None
    match = re.search(r"`([^`]+)`", text[marker_index:])
    if not match:
        return None
    return match.group(1)


def _display_value(value: str | None) -> str:
    return value if value is not None else "None"


if __name__ == "__main__":
    raise SystemExit(main())
