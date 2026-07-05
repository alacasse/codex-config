"""Read-only Planning Artifact Layout v1 state model."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from dataclasses import replace
from datetime import datetime
from datetime import timezone
import json
from pathlib import Path
from pathlib import PurePosixPath
import re
import sqlite3
import sys
import tempfile
from typing import Any, Iterable


NONE_VALUES = {"", "none", "none selected", "n/a", "tbd"}
FIELD_PATTERN = re.compile(r"^(?:-\s*)?([^:|]+):\s*(.*)$")
PLANNING_STATE_PROTOCOL_NAME = "planning-state-facts"
PLANNING_STATE_PROTOCOL_VERSION = 1
STATE_FIXTURE_SCHEMA_NAME = "planning-state-tool-state"
RECEIPT_FIXTURE_SCHEMA_NAME = "planning-state-transition-receipt"
CLOSEOUT_EVIDENCE_INDEX_SCHEMA_NAME = "planning-state-closeout-evidence-index"
PROJECTION_SCHEMA_NAME = "planning-state-sqlite-projection"
SUPPORTED_SCHEMA_VERSION = 1
PROJECTION_SCHEMA_VERSION = 1
ARTIFACT_REGISTRATION_PROTOCOL_NAME = "planning-state-artifact-registration"
TRANSITION_RECEIPT_PROTOCOL_NAME = "planning-state-transition"
CLOSEOUT_VALIDATION_PROTOCOL_NAME = "planning-state-closeout-validation"
CLOSEOUT_RENDERING_PROTOCOL_NAME = "planning-state-closeout-rendering"
STATE_FILE_POLICIES = {
    "committed",
    "external",
    "generated-only",
    "ignored-local",
    "none",
}
PROJECTION_POLICIES = {
    "external",
    "generated-only",
    "ignored-local",
    "none",
}
COMMITTED_PROJECTION_POLICY = "committed"
UPDATE_AUTHORITIES = {
    "ask-first",
    "command",
    "read-only",
}
PROJECT_POLICY_REQUIREMENTS = {
    "none",
    "state-file",
    "projection",
    "all",
}
STATE_FILE_PATH_POLICIES = {"committed", "external", "ignored-local"}
PROJECTION_PATH_POLICIES = {"committed", "external", "ignored-local"}
BOOTSTRAP_SOURCE_MARKDOWN_LAYOUT_V1 = "layout-v1-markdown"
BOOTSTRAP_SELECTION_PRECEDENCE = "root/program CURRENT.md active-first"
SUPPORTED_ARTIFACT_TYPES = {
    "dispatch",
    "runway",
    "closeout",
    "completed-slices",
    "receipt",
    "output",
}
BATCH_LOCAL_ARTIFACTS = {
    "dispatch": "dispatch.md",
    "runway": "runway.md",
    "closeout": "closeout.md",
    "completed-slices": "completed-slices.md",
}
BOOTSTRAP_MARKDOWN_OWNED_FIELDS = {
    "root.current",
    "program.current",
    "program.ledger",
    "program.dispatch",
    "program.runway",
    "program.closeout",
    "program.completed_slices",
}
BOOTSTRAP_JSON_STATE_FIELDS = {
    "root",
    "programs.slug",
    "programs.current",
    "programs.ledger",
    "programs.selected_dispatch",
    "programs.active_runway",
    "programs.queued_batch",
    "programs.latest_closeout",
    "programs.artifacts",
    "obligations",
}
BOOTSTRAP_COMPATIBILITY_EVIDENCE_CODES = {
    "redirect_ledger",
    "historical_batch_artifact",
    "stale_pickup_note",
    "stale_pickup_contradiction",
}
CLOSEOUT_REQUIRED_ARTIFACT_TYPES = {
    "closeout",
    "completed-slices",
    "dispatch",
    "runway",
}
CLOSEOUT_BANNED_SECTION_TERMS = {
    "chat transcript",
    "command transcript",
    "debug log",
    "full log",
    "raw log",
    "terminal transcript",
    "transcript",
}
CLOSEOUT_MAX_SECTION_ITEMS = 20
CLOSEOUT_MAX_SECTION_TEXT_CHARS = 1200
CLOSEOUT_MAX_SUMMARY_TEXT_CHARS = CLOSEOUT_MAX_SECTION_TEXT_CHARS
CLOSEOUT_MAX_SECTIONS = 8
CLOSEOUT_MAX_VALIDATION_EVIDENCE_ITEMS = 8
CLOSEOUT_MAX_REVIEW_EVIDENCE_ITEMS = 8
CLOSEOUT_MAX_TRANSITION_RECEIPTS = 8
CLOSEOUT_MAX_CLEANUP_RESIDUE_EVIDENCE_ITEMS = 8
CLOSEOUT_MAX_COMMITS = 20
CLOSEOUT_MAX_COMMIT_REF_CHARS = 80
CLOSEOUT_MAX_ARTIFACT_PATH_CHARS = 512
CLOSEOUT_EVIDENCE_ITEM_LIMITS = {
    "validation_evidence": CLOSEOUT_MAX_VALIDATION_EVIDENCE_ITEMS,
    "review_evidence": CLOSEOUT_MAX_REVIEW_EVIDENCE_ITEMS,
    "transition_receipts": CLOSEOUT_MAX_TRANSITION_RECEIPTS,
}
PROJECTION_SCHEMA_TABLES = {
    "projection_metadata",
    "source_artifacts",
    "report_facts",
}
PROJECTION_DATABASE_SUFFIXES = {".db", ".sqlite", ".sqlite3"}
PROJECTION_REPORT_FACT_TYPES = {
    "artifact_pointer",
    "batch_evidence_lookup",
    "closeout_evidence_status",
    "obligation",
    "pending_batch",
    "runner_summary",
}
PROJECTION_REPORT_FACT_FIELDS = {
    "artifact_type",
    "batch_id",
    "close_condition",
    "code",
    "count",
    "duration_ms",
    "evidence_path",
    "fact_type",
    "finished_at",
    "message",
    "obligation_id",
    "owner",
    "path",
    "phase",
    "program",
    "root",
    "run_id",
    "severity",
    "source_batch",
    "started_at",
    "status",
    "summary",
    "target_batch",
    "value",
}
PROJECTION_FORBIDDEN_FACT_FIELDS = {
    "body",
    "content",
    "log",
    "markdown",
    "prompt",
    "raw_log",
    "text",
    "transcript",
}
PROJECTION_BANNED_TEXT_TERMS = {
    *CLOSEOUT_BANNED_SECTION_TERMS,
    "chat history",
    "command output",
    "developer message",
    "full markdown",
    "ignore previous instructions",
    "instructions:",
    "prompt:",
    "raw telemetry",
    "system prompt",
    "you are chatgpt",
}
PROJECTION_MAX_TEXT_CHARS = CLOSEOUT_MAX_SUMMARY_TEXT_CHARS


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
class ObligationRecord:
    id: str
    owner: str | None
    source_batch: str
    target_batch: str | None
    close_condition: str | None
    status: str
    evidence_path: str | None


@dataclass(frozen=True)
class ProjectPolicy:
    planning_root: str
    run_artifact_root: str | None
    output_root: str | None
    state_file_policy: str
    state_file_path: str | None
    projection_policy: str
    projection_path: str | None
    update_authority: str
    committed_projection_exception: str | None
    source_path: Path


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
    project_policy: ProjectPolicy | None = None
    obligations: tuple[ObligationRecord, ...] = ()
    redirects: tuple[RedirectEvidence, ...] = ()
    warnings: tuple[StateWarning, ...] = ()
    validation_messages: tuple[ValidationMessage, ...] = ()


class ProtocolValidationError(ValueError):
    """Raised when a machine-readable planning-state object is malformed."""


def load_planning_state(
    root: str | Path,
    state_file: str | Path | None = None,
    *,
    require_project_policy: str = "none",
) -> PlanningState:
    """Load Planning Artifact Layout v1 state without mutating files."""

    root_path = Path(root)
    state_fixture_path = Path(state_file) if state_file is not None else None
    if require_project_policy not in PROJECT_POLICY_REQUIREMENTS:
        raise ProtocolValidationError(
            f"unsupported project policy requirement: {require_project_policy}"
        )
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
    policy, policy_messages = _resolve_project_policy(
        root_state,
        root_fields,
        programs,
        state_fixture=None,
    )
    redirects = tuple(_redirects(root_path))
    warnings = tuple(_warnings(root_path, root_state, programs, redirects))
    state_fixture = (
        _load_state_fixture(
            state_fixture_path,
            expected_root=_planning_root_prefix_for(root_state),
            allow_malformed_project_policy=True,
        )
        if state_fixture_path is not None
        else None
    )
    if state_fixture is not None:
        policy, policy_messages = _resolve_project_policy(
            root_state,
            root_fields,
            programs,
            state_fixture=state_fixture,
            state_fixture_path=state_fixture_path,
        )
    obligations = tuple(_obligations_from_fixture(state_fixture))
    validation_messages = tuple(
        _validation_messages(
            root_state,
            programs,
            redirects,
            state_fixture,
            policy,
            policy_messages,
            require_project_policy=require_project_policy,
        )
    )
    return PlanningState(
        root=root_state,
        programs=programs,
        project_policy=policy,
        obligations=obligations,
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
    lines.extend(_format_project_policy(state.project_policy))
    lines.extend(_format_obligations(state.obligations))
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
        "  project_policy:",
        "  errors:",
    ]
    if state.project_policy is None:
        lines.insert(-1, "    []")
    else:
        lines[-1:-1] = _format_project_policy_body(state.project_policy)
    lines.extend(_format_validation_messages(errors))
    lines.append("  warnings:")
    lines.extend(_format_validation_warnings(warnings))
    lines.append("  obligations:")
    lines.extend(_format_obligation_validation(state.obligations))
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
    fixture_root = _require_string(data, "root")
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
        artifacts = program_data.get("artifacts", [])
        if not isinstance(artifacts, list):
            raise ProtocolValidationError("artifacts must be an array")
        for artifact_index, artifact in enumerate(artifacts):
            artifact_data = _require_object(
                artifact,
                f"programs[{index}].artifacts[{artifact_index}]",
            )
            _require_supported_artifact_type(artifact_data, "type")
            _require_string(artifact_data, "batch_id")
            _require_string(artifact_data, "path")
    _validate_fixture_obligation_schema(data)
    _validate_bootstrap_contract_schema(data)
    _validate_project_policy_schema(data, expected_root=fixture_root)
    return data


def validate_project_policy_object(value: object) -> dict[str, Any]:
    """Validate the project-owned planning-state policy contract."""

    data = _require_object(value, "project_policy")
    _validate_project_policy_object(data, "project_policy")
    return data


def validate_receipt_fixture_object(value: object) -> dict[str, Any]:
    """Validate the minimal future write-transition receipt fixture schema."""

    data = _require_object(value, "receipt fixture")
    _require_protocol(data, RECEIPT_FIXTURE_SCHEMA_NAME, "receipt fixture")
    _require_string(data, "root")
    _require_string(data, "transition")
    _require_string(data, "status")
    _require_optional_string(data, "program")
    _require_optional_string(data, "batch_id")
    artifacts = data.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ProtocolValidationError("artifacts must be an array")
    for index, artifact in enumerate(artifacts):
        artifact_data = _require_object(artifact, f"artifacts[{index}]")
        _require_supported_artifact_type(artifact_data, "type")
        _require_string(artifact_data, "batch_id")
        _require_string(artifact_data, "path")
    warnings = data.get("warnings", [])
    if not isinstance(warnings, list):
        raise ProtocolValidationError("warnings must be an array")
    blockers = data.get("blockers", [])
    if not isinstance(blockers, list):
        raise ProtocolValidationError("blockers must be an array")
    messages = _require_array(data, "messages")
    for collection_name, collection in (
        ("messages", messages),
        ("warnings", warnings),
        ("blockers", blockers),
    ):
        for index, message in enumerate(collection):
            message_data = _require_object(message, f"{collection_name}[{index}]")
            _require_string(message_data, "severity")
            _require_string(message_data, "code")
            _require_string(message_data, "message")
            _require_optional_string(message_data, "source_path")
    obligations = data.get("obligations", [])
    if not isinstance(obligations, list):
        raise ProtocolValidationError("obligations must be an array")
    for index, obligation in enumerate(obligations):
        _validate_obligation_object(
            _require_object(obligation, f"obligations[{index}]"),
            f"obligations[{index}]",
        )
    return data


def validate_closeout_evidence_index_object(
    value: object,
    *,
    state_fixture: dict[str, Any] | None = None,
    planning_state: PlanningState | None = None,
    paths: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Validate the bounded closeout evidence-index data contract."""

    data = _require_object(value, "closeout evidence index")
    _require_protocol(data, CLOSEOUT_EVIDENCE_INDEX_SCHEMA_NAME, "closeout evidence index")
    root = _require_string(data, "root")
    program = _require_string(data, "program")
    batch_id = _require_string(data, "batch_id")
    status = _require_string(data, "status")
    if status not in {"closed", "completed"}:
        raise ProtocolValidationError("status must be 'closed' or 'completed'")
    fixture = (
        validate_state_fixture_object(state_fixture)
        if state_fixture is not None
        else None
    )
    if fixture is not None:
        _validate_closeout_fixture_binding(root, program, batch_id, fixture)
    _validate_closeout_known_batch(batch_id, fixture)
    fixture_program = (
        _fixture_program_for_closeout(fixture, program)
        if fixture is not None
        else None
    )
    _validate_closeout_artifacts(
        data,
        batch_id,
        fixture_program,
        planning_state=planning_state,
        paths=paths,
    )
    _validate_commit_evidence(_require_object(data.get("commit_evidence"), "commit_evidence"))
    _validate_closeout_evidence_items(
        data,
        "validation_evidence",
        batch_id,
        fixture_program,
        planning_state=planning_state,
        paths=paths,
    )
    _validate_closeout_evidence_items(
        data,
        "review_evidence",
        batch_id,
        fixture_program,
        planning_state=planning_state,
        paths=paths,
    )
    if "transition_receipts" in data:
        _validate_closeout_evidence_items(
            data,
            "transition_receipts",
            batch_id,
            fixture_program,
            planning_state=planning_state,
            paths=paths,
        )
    _validate_closeout_obligations(data, batch_id, fixture)
    _validate_cleanup_residue(
        _require_object(data.get("cleanup_residue"), "cleanup_residue")
    )
    _validate_bounded_closeout_sections(data)
    return data


def validate_projection_contract_object(value: object) -> dict[str, Any]:
    """Validate the bounded SQLite projection contract fixture."""

    data = _require_object(value, "projection contract")
    _require_protocol(data, PROJECTION_SCHEMA_NAME, "projection contract")
    metadata = _require_object(data.get("metadata"), "metadata")
    schema_version = metadata.get("schema_version")
    if schema_version != PROJECTION_SCHEMA_VERSION:
        raise ProtocolValidationError(
            f"metadata.schema_version must be {PROJECTION_SCHEMA_VERSION}"
        )
    planning_root = _require_string(metadata, "planning_root")
    _validate_projection_text(_require_string(metadata, "build_command"), "build_command")
    _validate_projection_text(_require_string(metadata, "built_at"), "built_at")
    _require_exact_string_set(metadata, "tables", PROJECTION_SCHEMA_TABLES)
    source_identity = _require_object(metadata.get("source_identity"), "source_identity")
    _validate_projection_source_identity(source_identity, "source_identity")
    if source_identity["planning_root"] != planning_root:
        raise ProtocolValidationError(
            "metadata.planning_root must match "
            "metadata.source_identity.planning_root"
        )
    state_fixture_identity = metadata.get("state_fixture_identity")
    if state_fixture_identity is not None:
        _validate_projection_source_artifact(
            _require_object(state_fixture_identity, "state_fixture_identity"),
            "state_fixture_identity",
        )
    _require_exact_string_set(
        data,
        "allowed_report_fact_types",
        PROJECTION_REPORT_FACT_TYPES,
    )
    report_facts = _require_array(data, "report_facts")
    for index, fact in enumerate(report_facts):
        _validate_projection_report_fact(
            _require_object(fact, f"report_facts[{index}]"),
            f"report_facts[{index}]",
        )
    return data


def projection_staleness_blockers(
    projection_metadata: dict[str, Any],
    expected_source_identity: dict[str, Any],
) -> tuple[ValidationMessage, ...]:
    """Return stable blockers when projection source metadata is stale."""

    actual = projection_metadata.get("source_identity")
    if actual == expected_source_identity:
        return ()
    return (
        ValidationMessage(
            "error",
            "projection_database_stale",
            "projection database source identity does not match current planning state",
            None,
        ),
    )


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
    current_parser.add_argument(
        "--state-file",
        type=Path,
        help="Optional explicit JSON state fixture with obligation records.",
    )
    current_parser.add_argument(
        "--require-project-policy",
        choices=tuple(sorted(PROJECT_POLICY_REQUIREMENTS)),
        default="none",
        help="Report blockers as if a durable state/projection write is being preflighted.",
    )
    current_parser.add_argument(
        "--projection-target",
        type=Path,
        help="Optional projection target to preflight without writing projection data.",
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
    validate_parser.add_argument(
        "--state-file",
        type=Path,
        help="Optional explicit JSON state fixture with obligation records.",
    )
    validate_parser.add_argument(
        "--require-project-policy",
        choices=tuple(sorted(PROJECT_POLICY_REQUIREMENTS)),
        default="none",
        help="Require declared policy for a durable state/projection preflight.",
    )
    validate_parser.add_argument(
        "--projection-target",
        type=Path,
        help="Optional projection target to preflight without writing projection data.",
    )
    bootstrap_parser = subparsers.add_parser(
        "bootstrap-state",
        help="Generate explicit planning-state JSON from Layout v1 Markdown.",
    )
    bootstrap_parser.add_argument("--root", type=Path, required=True)
    bootstrap_parser.add_argument(
        "--program",
        help="Optional active program slug to include. Defaults to all active programs.",
    )
    bootstrap_parser.add_argument(
        "--state-file",
        type=Path,
        help="Explicit JSON fixture target. Omit to print without writing.",
    )
    bootstrap_parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
        help="Output format. Only json is currently supported.",
    )
    rebuild_projection_parser = subparsers.add_parser(
        "rebuild-projection",
        help="Rebuild an explicit SQLite projection from canonical planning facts.",
    )
    rebuild_projection_parser.add_argument("--root", type=Path, required=True)
    rebuild_projection_parser.add_argument(
        "--database",
        type=Path,
        required=True,
        help="Explicit SQLite target to replace after a successful rebuild.",
    )
    rebuild_projection_parser.add_argument(
        "--state-file",
        type=Path,
        help="Optional explicit JSON state fixture with artifact and obligation facts.",
    )
    rebuild_projection_parser.add_argument(
        "--program",
        help="Optional active program slug to project. Defaults to all active programs.",
    )
    rebuild_projection_parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
        help="Output format. Only json is currently supported.",
    )
    allocate_parser = subparsers.add_parser(
        "allocate-batch",
        help="Compute canonical Layout v1 paths for a program batch.",
    )
    allocate_parser.add_argument("--root", type=Path, required=True)
    allocate_parser.add_argument("--program", required=True)
    allocate_parser.add_argument("--batch-id", required=True)
    allocate_parser.add_argument(
        "--format",
        choices=("json",),
        default="json",
        help="Output format. Only json is currently supported.",
    )
    register_parser = subparsers.add_parser(
        "register-artifact",
        help="Validate and register a planning artifact path.",
    )
    register_parser.add_argument("--root", type=Path, required=True)
    register_parser.add_argument("--program", required=True)
    register_parser.add_argument("--batch-id", required=True)
    register_parser.add_argument("--type", required=True)
    register_parser.add_argument("--path", required=True)
    register_parser.add_argument(
        "--state-file",
        type=Path,
        help="Explicit JSON state fixture to update. Omit for dry-run output.",
    )
    register_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print registration facts without writing state.",
    )
    select_parser = subparsers.add_parser(
        "select-batch",
        help="Select a registered dispatch in explicit planning-state JSON.",
    )
    select_parser.add_argument("--root", type=Path, required=True)
    select_parser.add_argument("--program", required=True)
    select_parser.add_argument("--batch-id", required=True)
    select_parser.add_argument("--dispatch", required=True)
    select_parser.add_argument("--state-file", type=Path, required=True)
    select_parser.add_argument("--receipt-file", type=Path)
    queue_parser = subparsers.add_parser(
        "queue-batch",
        help="Queue a registered runway in explicit planning-state JSON.",
    )
    queue_parser.add_argument("--root", type=Path, required=True)
    queue_parser.add_argument("--program", required=True)
    queue_parser.add_argument("--batch-id", required=True)
    queue_parser.add_argument("--dispatch", required=True)
    queue_parser.add_argument("--runway", required=True)
    queue_parser.add_argument("--state-file", type=Path, required=True)
    queue_parser.add_argument("--receipt-file", type=Path)
    closeout_parser = subparsers.add_parser(
        "validate-closeout",
        help="Validate a registered closeout evidence index.",
    )
    closeout_parser.add_argument("--root", type=Path, required=True)
    closeout_parser.add_argument("--program", required=True)
    closeout_parser.add_argument("--batch-id", required=True)
    closeout_parser.add_argument("--closeout", required=True)
    closeout_parser.add_argument("--state-file", type=Path, required=True)
    render_closeout_parser = subparsers.add_parser(
        "render-closeout",
        help="Render a bounded registered closeout evidence index.",
    )
    render_closeout_parser.add_argument("--root", type=Path, required=True)
    render_closeout_parser.add_argument("--program", required=True)
    render_closeout_parser.add_argument("--batch-id", required=True)
    render_closeout_parser.add_argument("--state-file", type=Path, required=True)
    render_closeout_parser.add_argument("--completed-slices-summary", required=True)
    render_closeout_parser.add_argument("--validation-artifact", required=True)
    render_closeout_parser.add_argument("--validation-summary", required=True)
    render_closeout_parser.add_argument("--review-artifact", required=True)
    render_closeout_parser.add_argument("--review-summary", required=True)
    render_closeout_parser.add_argument("--cleanup-classification", required=True)
    render_closeout_parser.add_argument("--cleanup-evidence", action="append", default=[])
    render_closeout_parser.add_argument("--commit", action="append", default=[])
    render_closeout_parser.add_argument("--commit-range-from")
    render_closeout_parser.add_argument("--commit-range-to")
    render_closeout_parser.add_argument("--transition-receipt-artifact", action="append", default=[])
    render_closeout_parser.add_argument("--transition-receipt-summary", action="append", default=[])
    render_closeout_parser.add_argument(
        "--target",
        help="Registered closeout.md path to write. Omit to render Markdown to stdout.",
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "current":
            state = load_planning_state(
                args.root,
                args.state_file,
                require_project_policy=args.require_project_policy,
            )
            state = _state_with_projection_preflight(state, args.projection_target)
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
            state = load_planning_state(
                args.root,
                args.state_file,
                require_project_policy=args.require_project_policy,
            )
            state = _state_with_projection_preflight(state, args.projection_target)
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
        if args.command == "bootstrap-state":
            state = load_planning_state(args.root)
            document = bootstrap_state(
                state,
                program_slug=args.program,
                state_file=args.state_file,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0
        if args.command == "rebuild-projection":
            state = load_planning_state(
                args.root,
                args.state_file,
            )
            document = rebuild_projection(
                state,
                database=args.database,
                state_file=args.state_file,
                program_slug=args.program,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0 if document["status"] == "rebuilt" else 1
        if args.command == "allocate-batch":
            state = load_planning_state(args.root)
            document = allocate_batch_paths(
                state,
                program_slug=args.program,
                batch_id=args.batch_id,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0
        if args.command == "register-artifact":
            state = load_planning_state(args.root)
            document = register_artifact(
                state,
                program_slug=args.program,
                batch_id=args.batch_id,
                artifact_type=args.type,
                artifact_path=args.path,
                state_file=args.state_file,
                dry_run=args.dry_run,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0
        if args.command == "select-batch":
            state = load_planning_state(args.root)
            document = select_batch(
                state,
                program_slug=args.program,
                batch_id=args.batch_id,
                dispatch_path=args.dispatch,
                state_file=args.state_file,
                receipt_file=args.receipt_file,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0 if document["status"] == "applied" else 1
        if args.command == "queue-batch":
            state = load_planning_state(args.root)
            document = queue_batch(
                state,
                program_slug=args.program,
                batch_id=args.batch_id,
                dispatch_path=args.dispatch,
                runway_path=args.runway,
                state_file=args.state_file,
                receipt_file=args.receipt_file,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0 if document["status"] == "applied" else 1
        if args.command == "validate-closeout":
            state = load_planning_state(args.root)
            document = validate_closeout(
                state,
                program_slug=args.program,
                batch_id=args.batch_id,
                closeout_path=args.closeout,
                state_file=args.state_file,
            )
            sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0 if document["status"] == "passed" else 1
        if args.command == "render-closeout":
            state = load_planning_state(args.root)
            document = render_closeout(
                state,
                program_slug=args.program,
                batch_id=args.batch_id,
                state_file=args.state_file,
                completed_slices_summary=args.completed_slices_summary,
                validation_artifact_path=args.validation_artifact,
                validation_summary=args.validation_summary,
                review_artifact_path=args.review_artifact,
                review_summary=args.review_summary,
                cleanup_classification=args.cleanup_classification,
                cleanup_evidence=args.cleanup_evidence,
                commits=args.commit,
                commit_range_from=args.commit_range_from,
                commit_range_to=args.commit_range_to,
                transition_receipt_artifacts=args.transition_receipt_artifact,
                transition_receipt_summaries=args.transition_receipt_summary,
                target_path=args.target,
            )
            markdown = document.pop("markdown")
            if args.target is None:
                sys.stdout.write(markdown)
            else:
                sys.stdout.write(json.dumps(document, indent=2, sort_keys=True) + "\n")
            return 0
    except ProtocolValidationError as error:
        parser.exit(2, f"{parser.prog}: error: {error}\n")
    parser.error(f"unknown command: {args.command}")
    return 2


def allocate_batch_paths(
    state: PlanningState,
    *,
    program_slug: str,
    batch_id: str,
) -> dict[str, Any]:
    """Return canonical Layout v1 paths without creating directories."""

    program = _find_program(state, program_slug)
    paths = _canonical_batch_paths(state, program, batch_id)
    _validate_batch_not_exists(state, paths["batch_directory"])
    return {
        "protocol": {
            "name": ARTIFACT_REGISTRATION_PROTOCOL_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
            "command": "allocate-batch",
        },
        "root": _planning_root_prefix(state),
        "program": program.slug,
        "batch_id": batch_id,
        "batch_directory": paths["batch_directory"],
        "artifacts": {
            artifact_type: paths[artifact_type]
            for artifact_type in BATCH_LOCAL_ARTIFACTS
        },
    }


def rebuild_projection(
    state: PlanningState,
    *,
    database: Path,
    state_file: Path | None,
    program_slug: str | None,
) -> dict[str, Any]:
    """Rebuild an explicit SQLite projection from bounded planning facts."""

    state_fixture = (
        _load_state_fixture(state_file, expected_root=_planning_root_prefix(state))
        if state_file is not None
        else None
    )
    blockers = list(
        _projection_rebuild_blockers(
            state,
            database=database,
            state_fixture=state_fixture,
        )
    )
    if blockers:
        return _projection_rebuild_result(
            state,
            database=database,
            status="rejected",
            blockers=blockers,
            projection=None,
        )
    programs = _bootstrap_programs(state, program_slug)
    projection = _projection_document(
        state,
        programs=programs,
        program_slug=program_slug,
        database=database,
        state_file=state_file,
        state_fixture=state_fixture,
    )
    validate_projection_contract_object(projection)
    _write_projection_database(database, projection)
    return _projection_rebuild_result(
        state,
        database=database,
        status="rebuilt",
        blockers=[],
        projection=projection,
    )


def register_artifact(
    state: PlanningState,
    *,
    program_slug: str,
    batch_id: str,
    artifact_type: str,
    artifact_path: str,
    state_file: Path | None,
    dry_run: bool,
) -> dict[str, Any]:
    """Validate and optionally record a planning artifact in a state fixture."""

    artifact_type = _normalize_artifact_type(artifact_type)
    program = _find_program(state, program_slug)
    paths = _canonical_batch_paths(state, program, batch_id)
    _validate_registered_path(
        state,
        artifact_type=artifact_type,
        artifact_path=artifact_path,
        paths=paths,
    )
    data = (
        _load_state_fixture(state_file, expected_root=_planning_root_prefix(state))
        if state_file is not None
        else None
    )
    if data is not None:
        _validate_state_file_target_policy(
            state,
            state_file,
            state_fixture=data,
            operation="register-artifact --state-file",
        )
    registration = {
        "type": artifact_type,
        "batch_id": batch_id,
        "path": artifact_path,
    }
    status = "dry-run"
    if data is not None:
        _register_artifact_in_fixture(
            data,
            program_slug=program.slug,
            registration=registration,
        )
        if not dry_run:
            _write_state_fixture(state_file, data)
            status = "registered"
    return {
        "protocol": {
            "name": ARTIFACT_REGISTRATION_PROTOCOL_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
            "command": "register-artifact",
        },
        "status": status,
        "root": _planning_root_prefix(state),
        "program": program.slug,
        "batch_id": batch_id,
        "batch_directory": paths["batch_directory"],
        "artifact": registration,
        "would_write_state_file": str(state_file) if state_file and not dry_run else None,
    }


def bootstrap_state(
    state: PlanningState,
    *,
    program_slug: str | None,
    state_file: Path | None,
) -> dict[str, Any]:
    """Generate a v1 explicit state fixture from Layout v1 Markdown facts."""

    messages = list(_bootstrap_blockers(state))
    programs = _bootstrap_programs(state, program_slug)
    document = {
        "protocol": {
            "name": STATE_FIXTURE_SCHEMA_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
        },
        "root": _planning_root_prefix(state),
        "bootstrap": _bootstrap_contract_object(),
        "programs": [_bootstrap_program_object(state, program) for program in programs],
        "obligations": [],
    }
    if messages:
        raise ProtocolValidationError(_format_bootstrap_blockers(messages))
    validate_state_fixture_object(document)
    if state_file is not None:
        _validate_bootstrap_state_target(state, state_file)
        _validate_state_file_target_policy(
            state,
            state_file,
            operation="bootstrap-state --state-file",
        )
        _write_state_fixture(state_file, document)
    return document


def select_batch(
    state: PlanningState,
    *,
    program_slug: str,
    batch_id: str,
    dispatch_path: str,
    state_file: Path,
    receipt_file: Path | None,
) -> dict[str, Any]:
    """Select a registered dispatch in an explicit state fixture."""

    program = _find_program(state, program_slug)
    paths = _canonical_batch_paths(state, program, batch_id)
    data = _load_state_fixture(state_file, expected_root=_planning_root_prefix(state))
    _validate_state_file_target_policy(
        state,
        state_file,
        state_fixture=data,
        operation="select-batch --state-file",
    )
    messages: list[dict[str, str | None]] = []
    _validate_transition_artifact(
        state,
        artifact_type="dispatch",
        artifact_path=dispatch_path,
        paths=paths,
        messages=messages,
    )
    program_data = _fixture_program(data, program.slug)
    _validate_no_active_transition_state(program, program_data, messages)
    _validate_registered_artifact(
        program_data,
        artifact_type="dispatch",
        batch_id=batch_id,
        artifact_path=dispatch_path,
        messages=messages,
    )
    _validate_batch_known_to_ledger(program, batch_id, messages)
    _append_obligation_messages(data, messages)
    obligations = _obligations_for_batch(data, batch_id)
    receipt = _transition_receipt(
        state,
        transition="select-batch",
        program=program.slug,
        batch_id=batch_id,
        artifacts=[
            {
                "type": "dispatch",
                "batch_id": batch_id,
                "path": dispatch_path,
            }
        ],
        obligations=obligations,
        messages=messages,
    )
    if receipt["status"] == "applied":
        program_data["selected_dispatch"] = dispatch_path
        _write_state_fixture(state_file, data)
    _write_receipt_fixture(receipt_file, receipt)
    return receipt


def queue_batch(
    state: PlanningState,
    *,
    program_slug: str,
    batch_id: str,
    dispatch_path: str,
    runway_path: str,
    state_file: Path,
    receipt_file: Path | None,
) -> dict[str, Any]:
    """Queue a registered runway in an explicit state fixture."""

    program = _find_program(state, program_slug)
    paths = _canonical_batch_paths(state, program, batch_id)
    data = _load_state_fixture(state_file, expected_root=_planning_root_prefix(state))
    _validate_state_file_target_policy(
        state,
        state_file,
        state_fixture=data,
        operation="queue-batch --state-file",
    )
    messages: list[dict[str, str | None]] = []
    for artifact_type, artifact_path in (
        ("dispatch", dispatch_path),
        ("runway", runway_path),
    ):
        _validate_transition_artifact(
            state,
            artifact_type=artifact_type,
            artifact_path=artifact_path,
            paths=paths,
            messages=messages,
        )
    program_data = _fixture_program(data, program.slug)
    _validate_queue_transition_state(program, program_data, dispatch_path, messages)
    for artifact_type, artifact_path in (
        ("dispatch", dispatch_path),
        ("runway", runway_path),
    ):
        _validate_registered_artifact(
            program_data,
            artifact_type=artifact_type,
            batch_id=batch_id,
            artifact_path=artifact_path,
            messages=messages,
        )
    _validate_batch_known_to_ledger(program, batch_id, messages)
    _append_obligation_messages(data, messages)
    obligations = _obligations_for_batch(data, batch_id)
    receipt = _transition_receipt(
        state,
        transition="queue-batch",
        program=program.slug,
        batch_id=batch_id,
        artifacts=[
            {
                "type": "dispatch",
                "batch_id": batch_id,
                "path": dispatch_path,
            },
            {
                "type": "runway",
                "batch_id": batch_id,
                "path": runway_path,
            },
        ],
        obligations=obligations,
        messages=messages,
    )
    if receipt["status"] == "applied":
        program_data["selected_dispatch"] = None
        program_data["queued_batch"] = runway_path
        _write_state_fixture(state_file, data)
    _write_receipt_fixture(receipt_file, receipt)
    return receipt


def validate_closeout(
    state: PlanningState,
    *,
    program_slug: str,
    batch_id: str,
    closeout_path: str,
    state_file: Path,
) -> dict[str, Any]:
    """Validate a named closeout evidence index against explicit state facts."""

    program = _find_program(state, program_slug)
    paths = _canonical_batch_paths(state, program, batch_id)
    data = _load_state_fixture(state_file, expected_root=_planning_root_prefix(state))
    _validate_state_file_target_policy(
        state,
        state_file,
        state_fixture=data,
        operation="validate-closeout --state-file",
    )
    messages: list[dict[str, str | None]] = []
    _validate_closeout_path(
        state,
        artifact_path=closeout_path,
        paths=paths,
        messages=messages,
    )
    if not _has_message_codes(
        messages,
        {"invalid_closeout_path", "missing_closeout", "non_file_closeout"},
    ):
        program_data = _fixture_program(data, program.slug)
        _validate_registered_artifact(
            program_data,
            artifact_type="closeout",
            batch_id=batch_id,
            artifact_path=closeout_path,
            messages=messages,
        )
        closeout = _read_closeout_evidence_index(state, closeout_path, messages)
        if closeout is not None:
            _append_closeout_preflight_messages(
                closeout,
                program=program.slug,
                batch_id=batch_id,
                closeout_path=closeout_path,
                state_fixture=data,
                messages=messages,
            )
            _append_closeout_pointer_contract_messages(
                closeout,
                batch_id=batch_id,
                planning_state=state,
                paths=paths,
                source_path=closeout_path,
                messages=messages,
            )
            if not _has_message_errors(messages):
                try:
                    validate_closeout_evidence_index_object(
                        closeout,
                        state_fixture=data,
                        planning_state=state,
                        paths=paths,
                    )
                except ProtocolValidationError as error:
                    _append_message(
                        messages,
                        severity="error",
                        code="invalid_closeout_contract",
                        message=str(error),
                        source_path=closeout_path,
                    )
    blockers = [message for message in messages if message["severity"] == "error"]
    warnings = [message for message in messages if message["severity"] == "warning"]
    result = {
        "protocol": {
            "name": CLOSEOUT_VALIDATION_PROTOCOL_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
            "command": "validate-closeout",
        },
        "root": _planning_root_prefix(state),
        "status": "failed" if blockers else "passed",
        "program": program.slug,
        "batch_id": batch_id,
        "closeout": closeout_path,
        "warnings": warnings,
        "blockers": blockers,
        "messages": messages,
    }
    return result


def render_closeout(
    state: PlanningState,
    *,
    program_slug: str,
    batch_id: str,
    state_file: Path,
    completed_slices_summary: str,
    validation_artifact_path: str,
    validation_summary: str,
    review_artifact_path: str,
    review_summary: str,
    cleanup_classification: str,
    cleanup_evidence: list[str],
    commits: list[str],
    commit_range_from: str | None,
    commit_range_to: str | None,
    transition_receipt_artifacts: list[str],
    transition_receipt_summaries: list[str],
    target_path: str | None,
) -> dict[str, Any]:
    """Render a bounded closeout evidence index from explicit inputs."""

    program = _find_program(state, program_slug)
    paths = _canonical_batch_paths(state, program, batch_id)
    data = _load_state_fixture(state_file, expected_root=_planning_root_prefix(state))
    _validate_state_file_target_policy(
        state,
        state_file,
        state_fixture=data,
        operation="render-closeout --state-file",
    )
    program_data = _fixture_program(data, program.slug)
    closeout_path = _registered_artifact_path(
        program_data,
        artifact_type="closeout",
        batch_id=batch_id,
    )
    if closeout_path is None:
        raise ProtocolValidationError(f"closeout is not registered for {batch_id}")
    _validate_registered_path(
        state,
        artifact_type="closeout",
        artifact_path=closeout_path,
        paths=paths,
    )
    if target_path is not None and target_path != closeout_path:
        raise ProtocolValidationError(
            f"target path must be registered closeout path: {closeout_path}"
        )
    transition_receipts = _render_closeout_evidence_items(
        state,
        program_data,
        batch_id=batch_id,
        paths=paths,
        artifact_type="receipt",
        artifact_paths=transition_receipt_artifacts,
        summaries=transition_receipt_summaries,
        field_name="transition-receipt",
    )
    closeout = _render_closeout_index(
        state,
        program=program.slug,
        batch_id=batch_id,
        state_fixture=data,
        closeout_path=closeout_path,
        completed_slices_summary=completed_slices_summary,
        validation_artifact_path=validation_artifact_path,
        validation_summary=validation_summary,
        review_artifact_path=review_artifact_path,
        review_summary=review_summary,
        cleanup_classification=cleanup_classification,
        cleanup_evidence=cleanup_evidence,
        commits=commits,
        commit_range_from=commit_range_from,
        commit_range_to=commit_range_to,
        transition_receipts=transition_receipts,
    )
    validate_closeout_evidence_index_object(
        closeout,
        state_fixture=data,
        planning_state=state,
        paths=paths,
    )
    markdown = _format_closeout_markdown(closeout)
    if target_path is not None:
        target = _resolve_pointer(state.root.root_path, target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(markdown, encoding="utf-8")
    return {
        "protocol": {
            "name": CLOSEOUT_RENDERING_PROTOCOL_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
            "command": "render-closeout",
        },
        "root": _planning_root_prefix(state),
        "status": "rendered",
        "program": program.slug,
        "batch_id": batch_id,
        "closeout": closeout_path,
        "target": target_path,
        "markdown": markdown,
    }


def _render_closeout_index(
    state: PlanningState,
    *,
    program: str,
    batch_id: str,
    state_fixture: dict[str, Any],
    closeout_path: str,
    completed_slices_summary: str,
    validation_artifact_path: str,
    validation_summary: str,
    review_artifact_path: str,
    review_summary: str,
    cleanup_classification: str,
    cleanup_evidence: list[str],
    commits: list[str],
    commit_range_from: str | None,
    commit_range_to: str | None,
    transition_receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    program_data = _fixture_program(state_fixture, program)
    artifacts = _render_required_closeout_artifacts(program_data, batch_id)
    validation_artifact = _registered_evidence_artifact(
        state,
        program_data,
        batch_id=batch_id,
        artifact_path=validation_artifact_path,
        paths=_canonical_batch_paths(state, _find_program(state, program), batch_id),
    )
    review_artifact = _registered_evidence_artifact(
        state,
        program_data,
        batch_id=batch_id,
        artifact_path=review_artifact_path,
        paths=_canonical_batch_paths(state, _find_program(state, program), batch_id),
    )
    closeout = {
        "protocol": {
            "name": CLOSEOUT_EVIDENCE_INDEX_SCHEMA_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
        },
        "root": _planning_root_prefix(state),
        "program": program,
        "batch_id": batch_id,
        "status": "closed",
        "artifacts": artifacts,
        "commit_evidence": _render_commit_evidence(
            commits,
            commit_range_from,
            commit_range_to,
        ),
        "validation_evidence": [
            {
                "artifact": validation_artifact,
                "summary": validation_summary,
            }
        ],
        "review_evidence": [
            {
                "artifact": review_artifact,
                "summary": review_summary,
            }
        ],
        "obligations": _render_obligations(state_fixture, batch_id),
        "cleanup_residue": {
            "classification": cleanup_classification,
            "evidence": cleanup_evidence,
        },
        "sections": [
            {
                "title": "Completed Slices",
                "items": [completed_slices_summary],
            }
        ],
    }
    if transition_receipts:
        closeout["transition_receipts"] = transition_receipts
    _validate_rendered_closeout_path(closeout, closeout_path)
    return closeout


def _render_required_closeout_artifacts(
    program_data: dict[str, Any],
    batch_id: str,
) -> list[dict[str, str]]:
    artifacts = []
    for artifact_type in ("closeout", "completed-slices", "dispatch", "runway"):
        path = _registered_artifact_path(
            program_data,
            artifact_type=artifact_type,
            batch_id=batch_id,
        )
        if path is None:
            raise ProtocolValidationError(
                f"{artifact_type} is not registered for {batch_id}"
            )
        artifacts.append(
            {
                "batch_id": batch_id,
                "path": path,
                "type": artifact_type,
            }
        )
    return artifacts


def _registered_evidence_artifact(
    state: PlanningState,
    program_data: dict[str, Any],
    *,
    batch_id: str,
    artifact_path: str,
    paths: dict[str, str],
) -> dict[str, str]:
    artifacts = program_data.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ProtocolValidationError("artifacts must be an array")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get("batch_id") != batch_id or artifact.get("path") != artifact_path:
            continue
        artifact_type = _normalize_artifact_type(str(artifact.get("type") or ""))
        _validate_registered_path(
            state,
            artifact_type=artifact_type,
            artifact_path=artifact_path,
            paths=paths,
        )
        return {
            "batch_id": batch_id,
            "path": artifact_path,
            "type": artifact_type,
        }
    raise ProtocolValidationError(f"artifact is not registered for {batch_id}: {artifact_path}")


def _render_commit_evidence(
    commits: list[str],
    commit_range_from: str | None,
    commit_range_to: str | None,
) -> dict[str, Any]:
    has_range = commit_range_from is not None or commit_range_to is not None
    if commits and has_range:
        raise ProtocolValidationError("commit evidence must use commits or range, not both")
    if commits:
        return {"commits": commits}
    if has_range:
        if commit_range_from is None or commit_range_to is None:
            raise ProtocolValidationError("commit range requires from and to values")
        return {"range": {"from": commit_range_from, "to": commit_range_to}}
    raise ProtocolValidationError("commit evidence is required")


def _render_obligations(
    state_fixture: dict[str, Any],
    batch_id: str,
) -> dict[str, list[dict[str, str | None]]]:
    rendered = {"closed": [], "open": []}
    for obligation in _obligations_from_fixture(state_fixture):
        if obligation.source_batch != batch_id and obligation.target_batch != batch_id:
            continue
        key = "closed" if obligation.status == "closed" else "open"
        rendered[key].append(_obligation_object(obligation))
    return rendered


def _render_closeout_evidence_items(
    state: PlanningState,
    program_data: dict[str, Any],
    *,
    batch_id: str,
    paths: dict[str, str],
    artifact_type: str,
    artifact_paths: list[str],
    summaries: list[str],
    field_name: str,
) -> list[dict[str, Any]]:
    if len(artifact_paths) != len(summaries):
        raise ProtocolValidationError(
            f"{field_name} artifacts and summaries must have the same count"
        )
    items = []
    for artifact_path, summary in zip(artifact_paths, summaries, strict=True):
        artifact = _registered_evidence_artifact(
            state,
            program_data,
            batch_id=batch_id,
            artifact_path=artifact_path,
            paths=paths,
        )
        if artifact["type"] != artifact_type:
            raise ProtocolValidationError(
                f"{field_name} artifact must be registered as {artifact_type}"
            )
        items.append({"artifact": artifact, "summary": summary})
    return items


def _registered_artifact_path(
    program_data: dict[str, Any],
    *,
    artifact_type: str,
    batch_id: str,
) -> str | None:
    artifacts = program_data.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ProtocolValidationError("artifacts must be an array")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get("type") == artifact_type and artifact.get("batch_id") == batch_id:
            path = artifact.get("path")
            if isinstance(path, str):
                return path
    return None


def _validate_rendered_closeout_path(
    closeout: dict[str, Any],
    closeout_path: str,
) -> None:
    artifacts = _closeout_artifacts_by_type(closeout)
    closeout_artifact = artifacts.get("closeout")
    if closeout_artifact is None or closeout_artifact.get("path") != closeout_path:
        raise ProtocolValidationError("rendered closeout path does not match registration")


def _format_closeout_markdown(closeout: dict[str, Any]) -> str:
    lines = [
        f"# Closeout: {closeout['batch_id']}",
        "",
        f"- Program: `{closeout['program']}`",
        f"- Status: `{closeout['status']}`",
        "- Evidence index: fenced JSON below",
        "",
        "```json",
        json.dumps(closeout, indent=2, sort_keys=True),
        "```",
        "",
    ]
    return "\n".join(lines)


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


def _resolve_project_policy(
    root_state: RootState,
    root_fields: dict[str, str],
    programs: tuple[ProgramState, ...],
    *,
    state_fixture: dict[str, Any] | None,
    state_fixture_path: Path | None = None,
) -> tuple[ProjectPolicy | None, tuple[ValidationMessage, ...]]:
    if state_fixture is not None and state_fixture.get("project_policy") is not None:
        source_path = state_fixture_path or root_state.current_path
        try:
            policy_data = validate_project_policy_object(state_fixture["project_policy"])
            _validate_project_policy_object(
                policy_data,
                "project_policy",
                expected_root=_planning_root_prefix_for(root_state),
            )
        except ProtocolValidationError as error:
            return None, (
                ValidationMessage(
                    "error",
                    "malformed_project_policy",
                    str(error),
                    source_path,
                ),
            )
        return _project_policy_from_data(policy_data, source_path), ()

    candidates: list[tuple[dict[str, str], Path]] = [(root_fields, root_state.current_path)]
    for program in programs:
        if program.current_path.exists():
            candidates.append((_field_map(_read_text(program.current_path)), program.current_path))
    candidates.extend(_project_instruction_policy_candidates(root_state))
    candidates.extend(_active_spec_policy_candidates(root_state, programs))

    messages: list[ValidationMessage] = []
    for fields, source_path in candidates:
        if not _has_project_policy_fields(fields):
            continue
        try:
            return _project_policy_from_fields(
                fields,
                source_path,
                expected_root=_planning_root_prefix_for(root_state),
            ), ()
        except ProtocolValidationError as error:
            return None, (
                ValidationMessage(
                    "error",
                    "malformed_project_policy",
                    str(error),
                    source_path,
                ),
            )
    return None, tuple(messages)


def _project_instruction_policy_candidates(
    root_state: RootState,
) -> list[tuple[dict[str, str], Path]]:
    root_path = root_state.root_path
    project_roots = []
    if len(root_path.parents) >= 2:
        project_roots.append(root_path.parents[1])
    if root_path.parent not in project_roots:
        project_roots.append(root_path.parent)
    candidates: list[tuple[dict[str, str], Path]] = []
    seen: set[Path] = set()
    for project_root in project_roots:
        for instruction_path in (
            project_root / "AGENTS.md",
            project_root / ".codex" / "AGENTS.md",
        ):
            if instruction_path in seen or not instruction_path.exists():
                continue
            seen.add(instruction_path)
            candidates.append((_field_map(_read_text(instruction_path)), instruction_path))
    return candidates


def _active_spec_policy_candidates(
    root_state: RootState,
    programs: tuple[ProgramState, ...],
) -> list[tuple[dict[str, str], Path]]:
    candidates: list[tuple[dict[str, str], Path]] = []
    seen: set[Path] = set()
    for program in programs:
        policy_candidate_values = (
            program.active_runway.value,
            _active_spec_queued_batch_value(root_state, program),
            program.selected_dispatch.value,
        )
        for value in policy_candidate_values:
            if value is None:
                continue
            path = _resolve_pointer(root_state.root_path, value)
            if path in seen or not path.exists() or path.suffix != ".md":
                continue
            seen.add(path)
            candidates.append((_field_map(_read_text(path)), path))
    return candidates


def _active_spec_queued_batch_value(
    root_state: RootState,
    program: ProgramState,
) -> str | None:
    try:
        return _migrated_queued_batch_value(root_state, program)
    except ProtocolValidationError:
        return None


def _has_project_policy_fields(fields: dict[str, str]) -> bool:
    return any(
        field in fields
        for field in (
            "state file policy",
            "state_file_policy",
            "projection policy",
            "projection_policy",
            "state file path",
            "state_file_path",
            "projection path",
            "projection_path",
            "update authority",
            "update_authority",
        )
    )


def _project_policy_from_fields(
    fields: dict[str, str],
    source_path: Path,
    *,
    expected_root: str,
) -> ProjectPolicy:
    data = {
        "planning_root": _policy_field(fields, "planning root", "planning_root"),
        "run_artifact_root": _policy_none_to_null(
            _policy_field(fields, "run artifact root", "run_artifact_root")
        ),
        "output_root": _policy_none_to_null(_policy_field(fields, "output root", "output_root")),
        "state_file_policy": _policy_field(fields, "state file policy", "state_file_policy"),
        "state_file_path": _policy_none_to_null(
            _policy_field(fields, "state file path", "state_file_path")
        ),
        "projection_policy": _policy_field(fields, "projection policy", "projection_policy"),
        "projection_path": _policy_none_to_null(
            _policy_field(fields, "projection path", "projection_path")
        ),
        "update_authority": _policy_field(fields, "update authority", "update_authority"),
    }
    committed_exception = _policy_none_to_null(
        _policy_field(
            fields,
            "committed projection exception",
            "committed_projection_exception",
        )
    )
    if committed_exception is not None:
        data["committed_projection_exception"] = committed_exception
    validate_project_policy_object(data)
    _validate_project_policy_object(data, "project_policy", expected_root=expected_root)
    return _project_policy_from_data(data, source_path)


def _project_policy_from_data(
    data: dict[str, Any],
    source_path: Path,
) -> ProjectPolicy:
    return ProjectPolicy(
        planning_root=data["planning_root"],
        run_artifact_root=data.get("run_artifact_root"),
        output_root=data.get("output_root"),
        state_file_policy=data["state_file_policy"],
        state_file_path=data.get("state_file_path"),
        projection_policy=data["projection_policy"],
        projection_path=data.get("projection_path"),
        update_authority=data["update_authority"],
        committed_projection_exception=data.get("committed_projection_exception"),
        source_path=source_path,
    )


def _policy_field(fields: dict[str, str], *keys: str) -> str | None:
    return next((fields[key] for key in keys if key in fields), None)


def _policy_none_to_null(value: str | None) -> str | None:
    return _none_to_null(value)


def _validation_messages(
    root_state: RootState,
    programs: tuple[ProgramState, ...],
    redirects: tuple[RedirectEvidence, ...],
    state_fixture: dict[str, Any] | None,
    project_policy: ProjectPolicy | None,
    project_policy_messages: tuple[ValidationMessage, ...],
    *,
    require_project_policy: str,
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
    yield from project_policy_messages
    yield from _project_policy_requirement_messages(
        root_state,
        project_policy,
        project_policy_messages,
        require_project_policy,
    )
    if state_fixture is not None:
        yield from _state_fixture_validation_messages(root_state, programs, state_fixture)
        yield from _obligation_validation_messages(state_fixture)


def _project_policy_requirement_messages(
    root_state: RootState,
    project_policy: ProjectPolicy | None,
    project_policy_messages: tuple[ValidationMessage, ...],
    require_project_policy: str,
) -> Iterable[ValidationMessage]:
    if require_project_policy == "none":
        return
    if project_policy_messages:
        return
    if project_policy is None:
        yield ValidationMessage(
            "error",
            "missing_project_policy",
            f"project policy is required before durable {require_project_policy} writes",
            root_state.current_path,
        )
        return
    if require_project_policy in {"state-file", "all"} and (
        project_policy.state_file_policy in {"generated-only", "none"}
    ):
        yield ValidationMessage(
            "error",
            "state_file_policy_not_durable",
            f"state-file policy {project_policy.state_file_policy!r} has no durable target",
            project_policy.source_path,
        )
    if require_project_policy in {"projection", "all"} and (
        project_policy.projection_policy in {"generated-only", "none"}
    ):
        yield ValidationMessage(
            "error",
            "projection_policy_not_durable",
            f"projection policy {project_policy.projection_policy!r} has no durable target",
            project_policy.source_path,
        )


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


def _format_project_policy(policy: ProjectPolicy | None) -> list[str]:
    lines = ["  project_policy:"]
    if policy is None:
        return [*lines, "    []"]
    return [*lines, *_format_project_policy_body(policy)]


def _format_project_policy_body(policy: ProjectPolicy) -> list[str]:
    return [
        f"    source: {policy.source_path}",
        f"    planning_root: {policy.planning_root}",
        f"    run_artifact_root: {_display_value(policy.run_artifact_root)}",
        f"    output_root: {_display_value(policy.output_root)}",
        f"    state_file_policy: {policy.state_file_policy}",
        f"    state_file_path: {_display_value(policy.state_file_path)}",
        f"    projection_policy: {policy.projection_policy}",
        f"    projection_path: {_display_value(policy.projection_path)}",
        f"    update_authority: {policy.update_authority}",
    ]


def _format_obligations(obligations: tuple[ObligationRecord, ...]) -> list[str]:
    lines = ["  obligations:"]
    if not obligations:
        return [*lines, "    []"]
    for obligation in obligations:
        target = obligation.target_batch or obligation.close_condition
        evidence = _display_value(obligation.evidence_path)
        lines.append(
            "    - "
            f"id: {obligation.id}; status: {obligation.status}; "
            f"owner: {_display_value(obligation.owner)}; "
            f"source_batch: {obligation.source_batch}; "
            f"target_or_close_condition: {_display_value(target)}; "
            f"evidence_path: {evidence}"
        )
    return lines


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


def _format_obligation_validation(obligations: tuple[ObligationRecord, ...]) -> list[str]:
    if not obligations:
        return ["    []"]
    lines = []
    for obligation in obligations:
        target = obligation.target_batch or obligation.close_condition
        lines.append(
            "    - "
            f"{obligation.status}: {obligation.id} "
            f"(owner: {_display_value(obligation.owner)}, "
            f"source_batch: {obligation.source_batch}, "
            f"target_or_close_condition: {_display_value(target)}, "
            f"evidence_path: {_display_value(obligation.evidence_path)})"
        )
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
        "project_policy": _project_policy_object(state.project_policy),
        "obligations": [
            _obligation_object(obligation) for obligation in state.obligations
        ],
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


def _project_policy_object(policy: ProjectPolicy | None) -> dict[str, Any] | None:
    if policy is None:
        return None
    return {
        "planning_root": policy.planning_root,
        "run_artifact_root": policy.run_artifact_root,
        "output_root": policy.output_root,
        "state_file_policy": policy.state_file_policy,
        "state_file_path": policy.state_file_path,
        "projection_policy": policy.projection_policy,
        "projection_path": policy.projection_path,
        "update_authority": policy.update_authority,
        "committed_projection_exception": policy.committed_projection_exception,
        "source_path": str(policy.source_path),
    }


def _artifact_pointer_object(pointer: ArtifactPointer) -> dict[str, Any]:
    return {
        "label": pointer.label,
        "value": pointer.value,
        "source_path": str(pointer.source_path),
        "exists": pointer.exists,
    }


def _obligation_object(obligation: ObligationRecord) -> dict[str, Any]:
    return {
        "id": obligation.id,
        "owner": obligation.owner,
        "source_batch": obligation.source_batch,
        "target_batch": obligation.target_batch,
        "close_condition": obligation.close_condition,
        "status": obligation.status,
        "evidence_path": obligation.evidence_path,
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


def _require_supported_artifact_type(data: dict[str, Any], key: str) -> str:
    value = _require_string(data, key)
    return _normalize_artifact_type(value)


def _validate_fixture_obligation_schema(data: dict[str, Any]) -> None:
    obligations = data.get("obligations", [])
    if not isinstance(obligations, list):
        raise ProtocolValidationError("obligations must be an array")
    for index, obligation in enumerate(obligations):
        try:
            _validate_obligation_object(
                _require_object(obligation, f"obligations[{index}]"),
                f"obligations[{index}]",
            )
        except ProtocolValidationError as error:
            raise ProtocolValidationError(
                f"malformed_obligation_record: {error}"
            ) from error


def _validate_bootstrap_contract_schema(data: dict[str, Any]) -> None:
    contract = data.get("bootstrap")
    if contract is None:
        return
    contract_data = _require_object(contract, "bootstrap")
    source = _require_string(contract_data, "source")
    if source != BOOTSTRAP_SOURCE_MARKDOWN_LAYOUT_V1:
        raise ProtocolValidationError(
            f"bootstrap.source must be {BOOTSTRAP_SOURCE_MARKDOWN_LAYOUT_V1!r}"
        )
    precedence = _require_string(contract_data, "selection_precedence")
    if precedence != BOOTSTRAP_SELECTION_PRECEDENCE:
        raise ProtocolValidationError(
            "bootstrap.selection_precedence must be "
            f"{BOOTSTRAP_SELECTION_PRECEDENCE!r}"
        )
    if contract_data.get("writes_markdown") is not False:
        raise ProtocolValidationError("bootstrap.writes_markdown must be false")
    _require_exact_string_set(
        contract_data,
        "markdown_owned",
        BOOTSTRAP_MARKDOWN_OWNED_FIELDS,
    )
    _require_exact_string_set(
        contract_data,
        "json_state_fields",
        BOOTSTRAP_JSON_STATE_FIELDS,
    )
    _require_exact_string_set(
        contract_data,
        "registered_artifact_types",
        set(BATCH_LOCAL_ARTIFACTS),
    )
    _require_exact_string_set(
        contract_data,
        "compatibility_evidence",
        BOOTSTRAP_COMPATIBILITY_EVIDENCE_CODES,
    )


def _validate_project_policy_schema(
    data: dict[str, Any],
    *,
    expected_root: str,
) -> None:
    policy = data.get("project_policy")
    if policy is None:
        return
    _validate_project_policy_object(
        _require_object(policy, "project_policy"),
        "project_policy",
        expected_root=expected_root,
    )


def _validate_project_policy_object(
    data: dict[str, Any],
    context: str,
    *,
    expected_root: str | None = None,
) -> None:
    planning_root = _require_string(data, "planning_root")
    if expected_root is not None and _normalize_policy_root(
        planning_root
    ) != _normalize_policy_root(expected_root):
        raise ProtocolValidationError(
            f"{context}.planning_root must match fixture root {expected_root!r}"
        )
    _require_optional_string(data, "run_artifact_root")
    _require_optional_string(data, "output_root")
    state_file_policy = _require_string(data, "state_file_policy")
    if state_file_policy not in STATE_FILE_POLICIES:
        raise ProtocolValidationError(
            f"{context}.state_file_policy is unsupported: {state_file_policy}"
        )
    state_file_path = _require_optional_string(data, "state_file_path")
    _validate_policy_path(
        context,
        policy_field="state_file_policy",
        policy_value=state_file_policy,
        path_field="state_file_path",
        path_value=state_file_path,
        durable_path_policies=STATE_FILE_PATH_POLICIES,
    )
    projection_policy = _require_string(data, "projection_policy")
    if projection_policy == COMMITTED_PROJECTION_POLICY:
        if not _require_optional_string(data, "committed_projection_exception"):
            raise ProtocolValidationError(
                f"{context}.committed_projection_exception must explain committed "
                "projection policy"
            )
    elif projection_policy not in PROJECTION_POLICIES:
        raise ProtocolValidationError(
            f"{context}.projection_policy is unsupported: {projection_policy}"
        )
    projection_path = _require_optional_string(data, "projection_path")
    _validate_policy_path(
        context,
        policy_field="projection_policy",
        policy_value=projection_policy,
        path_field="projection_path",
        path_value=projection_path,
        durable_path_policies=PROJECTION_PATH_POLICIES,
    )
    update_authority = _require_string(data, "update_authority")
    if update_authority not in UPDATE_AUTHORITIES:
        raise ProtocolValidationError(
            f"{context}.update_authority is unsupported: {update_authority}"
        )


def _normalize_policy_root(value: str) -> str:
    normalized = value.strip()
    while normalized != "/" and normalized.endswith("/"):
        normalized = normalized[:-1]
    return normalized


def _validate_policy_path(
    context: str,
    *,
    policy_field: str,
    policy_value: str,
    path_field: str,
    path_value: str | None,
    durable_path_policies: set[str],
) -> None:
    if path_value == "":
        raise ProtocolValidationError(
            f"{context}.{path_field} must be null or a non-empty string"
        )
    if policy_value in durable_path_policies:
        if not path_value:
            raise ProtocolValidationError(
                f"{context}.{path_field} is required when {policy_field} is "
                f"{policy_value!r}"
            )
        return
    if path_value:
        raise ProtocolValidationError(
            f"{context}.{path_field} must be null when {policy_field} is "
            f"{policy_value!r}"
        )


def _require_exact_string_set(
    data: dict[str, Any],
    field_name: str,
    expected_values: set[str],
) -> list[str]:
    values = _require_array(data, field_name)
    if not values:
        raise ProtocolValidationError(f"{field_name} must be a non-empty array")
    seen_values: set[str] = set()
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value:
            raise ProtocolValidationError(
                f"{field_name}[{index}] must be a non-empty string"
            )
        if value not in expected_values:
            raise ProtocolValidationError(
                f"{field_name}[{index}] is not a supported bootstrap fact: {value}"
            )
        seen_values.add(value)
    missing = sorted(expected_values - seen_values)
    extra = sorted(seen_values - expected_values)
    if missing or extra or len(values) != len(seen_values):
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("extra: " + ", ".join(extra))
        if len(values) != len(seen_values):
            details.append("duplicates are not allowed")
        raise ProtocolValidationError(
            f"{field_name} must exactly match the bootstrap contract"
            f" ({'; '.join(details)})"
        )
    return values


def _validate_obligation_object(data: dict[str, Any], context: str) -> None:
    _require_string(data, "id")
    _require_optional_string(data, "owner")
    _require_string(data, "source_batch")
    _require_optional_string(data, "target_batch")
    _require_optional_string(data, "close_condition")
    status = _require_string(data, "status")
    if status not in {"open", "closed"}:
        raise ProtocolValidationError(
            f"invalid_obligation_record: {context}.status must be 'open' or 'closed'"
        )
    _require_optional_string(data, "evidence_path")


def _validate_projection_source_identity(
    data: dict[str, Any],
    context: str,
) -> None:
    _require_string(data, "planning_root")
    sources = _require_array(data, "sources")
    if not sources:
        raise ProtocolValidationError(f"{context}.sources must be a non-empty array")
    for index, source in enumerate(sources):
        _validate_projection_source_artifact(
            _require_object(source, f"{context}.sources[{index}]"),
            f"{context}.sources[{index}]",
        )


def _validate_projection_source_artifact(
    data: dict[str, Any],
    context: str,
) -> None:
    _validate_projection_text(_require_string(data, "kind"), f"{context}.kind")
    _validate_projection_text(_require_string(data, "path"), f"{context}.path")
    sha256 = _require_optional_string(data, "sha256")
    mtime_ns = data.get("mtime_ns")
    if sha256 is not None:
        if re.fullmatch(r"[0-9a-f]{64}", sha256) is None:
            raise ProtocolValidationError(f"{context}.sha256 must be a hex sha256")
    if mtime_ns is not None and (
        not isinstance(mtime_ns, int) or isinstance(mtime_ns, bool) or mtime_ns < 0
    ):
        raise ProtocolValidationError(f"{context}.mtime_ns must be a non-negative integer")
    if sha256 is None and mtime_ns is None:
        raise ProtocolValidationError(f"{context} must include sha256 or mtime_ns")


def _validate_projection_report_fact(
    data: dict[str, Any],
    context: str,
) -> None:
    fact_type = _require_string(data, "fact_type")
    if fact_type not in PROJECTION_REPORT_FACT_TYPES:
        raise ProtocolValidationError(f"{context}.fact_type is unsupported: {fact_type}")
    for key, value in data.items():
        if key in PROJECTION_FORBIDDEN_FACT_FIELDS:
            raise ProtocolValidationError(f"{context}.{key} is canonical or unbounded")
        if key not in PROJECTION_REPORT_FACT_FIELDS:
            raise ProtocolValidationError(f"{context}.{key} is not a projection fact field")
        _validate_projection_scalar(value, f"{context}.{key}")


def _validate_projection_scalar(value: object, context: str) -> None:
    if value is None:
        return
    if isinstance(value, bool):
        raise ProtocolValidationError(f"{context} must be a bounded scalar")
    if isinstance(value, int):
        if value < 0:
            raise ProtocolValidationError(f"{context} must be non-negative")
        return
    if isinstance(value, str):
        _validate_projection_text(value, context)
        return
    raise ProtocolValidationError(f"{context} must be a bounded scalar")


def _validate_projection_text(value: object, context: str) -> None:
    if not isinstance(value, str) or not value:
        raise ProtocolValidationError(f"{context} must be a non-empty string")
    if len(value) > PROJECTION_MAX_TEXT_CHARS:
        raise ProtocolValidationError(f"{context} exceeds bounded projection text limit")
    lowered = value.lower()
    if "\n" in value or "\r" in value or any(
        term in lowered for term in PROJECTION_BANNED_TEXT_TERMS
    ):
        raise ProtocolValidationError(f"{context} is canonical or unbounded")


def _validate_closeout_known_batch(
    batch_id: str,
    state_fixture: dict[str, Any] | None,
) -> None:
    if state_fixture is None:
        return
    fixture = validate_state_fixture_object(state_fixture)
    if batch_id not in _fixture_batch_ids(fixture):
        raise ProtocolValidationError(f"unknown closeout batch_id: {batch_id}")


def _validate_closeout_fixture_binding(
    root: str,
    program_slug: str,
    batch_id: str,
    state_fixture: dict[str, Any],
) -> None:
    fixture_root = _require_string(state_fixture, "root")
    if root != fixture_root:
        raise ProtocolValidationError(
            f"closeout root must match state fixture root {fixture_root!r}"
        )
    program = _fixture_program_for_closeout(state_fixture, program_slug)
    if batch_id not in _fixture_program_batch_ids(program):
        if batch_id in _fixture_batch_ids(state_fixture):
            raise ProtocolValidationError(
                f"closeout program {program_slug!r} does not own batch_id {batch_id!r}"
            )
        raise ProtocolValidationError(f"unknown closeout batch_id: {batch_id}")


def _fixture_program_for_closeout(
    state_fixture: dict[str, Any],
    program_slug: str,
) -> dict[str, Any]:
    programs = _require_array(state_fixture, "programs")
    for index, program in enumerate(programs):
        program_data = _require_object(program, f"programs[{index}]")
        if program_data.get("slug") == program_slug:
            return program_data
    raise ProtocolValidationError(f"unknown closeout program: {program_slug}")


def _validate_closeout_artifacts(
    data: dict[str, Any],
    batch_id: str,
    fixture_program: dict[str, Any] | None,
    *,
    planning_state: PlanningState | None = None,
    paths: dict[str, str] | None = None,
) -> None:
    artifacts = _require_array(data, "artifacts")
    artifacts_by_type: dict[str, dict[str, Any]] = {}
    for index, artifact in enumerate(artifacts):
        artifact_data = _validate_closeout_artifact_pointer(
            artifact,
            f"artifacts[{index}]",
            batch_id=batch_id,
            fixture_program=fixture_program,
            planning_state=planning_state,
            paths=paths,
        )
        artifact_type = artifact_data["type"]
        if artifact_type in artifacts_by_type:
            raise ProtocolValidationError(f"artifacts contains duplicate {artifact_type}")
        artifacts_by_type[artifact_type] = artifact_data
    missing = sorted(CLOSEOUT_REQUIRED_ARTIFACT_TYPES - artifacts_by_type.keys())
    if missing:
        raise ProtocolValidationError(
            "closeout artifacts missing required pointers: " + ", ".join(missing)
        )


def _validate_closeout_artifact_pointer(
    value: object,
    context: str,
    *,
    batch_id: str,
    fixture_program: dict[str, Any] | None,
    planning_state: PlanningState | None = None,
    paths: dict[str, str] | None = None,
) -> dict[str, Any]:
    artifact = _require_object(value, context)
    artifact_type = _require_supported_artifact_type(artifact, "type")
    artifact_batch = _require_string(artifact, "batch_id")
    artifact_path = _require_string(artifact, "path")
    _validate_bounded_closeout_artifact_path(artifact_path, f"{context}.path")
    if artifact_batch != batch_id:
        raise ProtocolValidationError(
            f"{context}.batch_id must match closeout batch_id {batch_id!r}"
        )
    if planning_state is not None and paths is not None:
        _validate_registered_path(
            planning_state,
            artifact_type=artifact_type,
            artifact_path=artifact_path,
            paths=paths,
        )
    if fixture_program is not None and (
        artifact_type,
        artifact_batch,
        artifact_path,
    ) not in _fixture_program_artifact_keys(fixture_program):
        raise ProtocolValidationError(
            f"{context} must reference a registered artifact"
        )
    return artifact


def _validate_commit_evidence(commit_evidence: dict[str, Any]) -> None:
    commits = commit_evidence.get("commits")
    commit_range = commit_evidence.get("range")
    if commits is not None:
        if not isinstance(commits, list) or not commits:
            raise ProtocolValidationError("commit_evidence.commits must be a non-empty array")
        if len(commits) > CLOSEOUT_MAX_COMMITS:
            raise ProtocolValidationError(
                "commit_evidence.commits exceeds bounded evidence item limit"
            )
        for index, commit in enumerate(commits):
            _validate_bounded_commit_ref(
                commit,
                f"commit_evidence.commits[{index}]",
            )
            if not _looks_like_commit_hash(commit):
                raise ProtocolValidationError(
                    f"commit_evidence.commits[{index}] must be a commit hash"
                )
    if commit_range is not None:
        range_data = _require_object(commit_range, "commit_evidence.range")
        for key in ("from", "to"):
            commit = range_data.get(key)
            _validate_bounded_commit_ref(commit, f"commit_evidence.range.{key}")
            if not _looks_like_commit_hash(commit):
                raise ProtocolValidationError(
                    f"commit_evidence.range.{key} must be a commit hash"
                )
    if not commits and commit_range is None:
        raise ProtocolValidationError(
            "commit_evidence must include commits or range"
        )


def _validate_closeout_evidence_items(
    data: dict[str, Any],
    key: str,
    batch_id: str,
    fixture_program: dict[str, Any] | None,
    *,
    planning_state: PlanningState | None = None,
    paths: dict[str, str] | None = None,
) -> None:
    items = _require_array(data, key)
    if not items:
        raise ProtocolValidationError(f"{key} must not be empty")
    limit = CLOSEOUT_EVIDENCE_ITEM_LIMITS[key]
    if len(items) > limit:
        raise ProtocolValidationError(f"{key} exceeds bounded evidence item limit")
    for index, item in enumerate(items):
        item_data = _require_object(item, f"{key}[{index}]")
        _validate_bounded_closeout_summary(
            item_data.get("summary"),
            f"{key}[{index}].summary",
        )
        artifact = _require_object(item_data.get("artifact"), f"{key}[{index}].artifact")
        _validate_closeout_artifact_pointer(
            artifact,
            f"{key}[{index}].artifact",
            batch_id=batch_id,
            fixture_program=fixture_program,
            planning_state=planning_state,
            paths=paths,
        )


def _validate_closeout_obligations(
    data: dict[str, Any],
    batch_id: str,
    state_fixture: dict[str, Any] | None,
) -> None:
    obligations = _require_object(data.get("obligations"), "obligations")
    closed = _require_array(obligations, "closed")
    open_obligations = _require_array(obligations, "open")
    fixture_obligations = None
    if state_fixture is not None:
        fixture_obligations = {
            _obligation_fact_key(_obligation_object(obligation))
            for obligation in _obligations_from_fixture(state_fixture)
        }
    for collection_name, collection in (
        ("closed", closed),
        ("open", open_obligations),
    ):
        for index, obligation in enumerate(collection):
            obligation_data = _require_object(
                obligation,
                f"obligations.{collection_name}[{index}]",
            )
            _validate_obligation_object(
                obligation_data,
                f"obligations.{collection_name}[{index}]",
            )
            if collection_name == "closed":
                if obligation_data["status"] != "closed":
                    raise ProtocolValidationError(
                        f"obligations.closed[{index}].status must be 'closed'"
                    )
                evidence_path = obligation_data.get("evidence_path")
                if not isinstance(evidence_path, str) or not evidence_path:
                    raise ProtocolValidationError(
                        f"obligations.closed[{index}].evidence_path must be a non-empty string"
                    )
            if collection_name == "open" and obligation_data["status"] != "open":
                raise ProtocolValidationError(
                    f"obligations.open[{index}].status must be 'open'"
                )
            if (
                obligation_data["source_batch"] != batch_id
                and obligation_data.get("target_batch") != batch_id
            ):
                raise ProtocolValidationError(
                    f"obligations.{collection_name}[{index}] must reference {batch_id}"
                )
            if (
                fixture_obligations is not None
                and _obligation_fact_key(obligation_data) not in fixture_obligations
            ):
                raise ProtocolValidationError(
                    f"obligations.{collection_name}[{index}] must match a state fixture obligation"
                )


def _validate_closeout_path(
    state: PlanningState,
    *,
    artifact_path: str,
    paths: dict[str, str],
    messages: list[dict[str, str | None]],
) -> None:
    try:
        _validate_registered_path(
            state,
            artifact_type="closeout",
            artifact_path=artifact_path,
            paths=paths,
        )
    except ProtocolValidationError as error:
        _append_message(
            messages,
            severity="error",
            code="invalid_closeout_path",
            message=str(error),
            source_path=artifact_path,
        )
        return
    resolved_path = _resolve_pointer(state.root.root_path, artifact_path)
    if not resolved_path.exists():
        _append_message(
            messages,
            severity="error",
            code="missing_closeout",
            message=f"{artifact_path} is missing",
            source_path=artifact_path,
        )
        return
    if not resolved_path.is_file():
        _append_message(
            messages,
            severity="error",
            code="non_file_closeout",
            message=f"{artifact_path} is not a file",
            source_path=artifact_path,
        )


def _read_closeout_evidence_index(
    state: PlanningState,
    closeout_path: str,
    messages: list[dict[str, str | None]],
) -> dict[str, Any] | None:
    path = _resolve_pointer(state.root.root_path, closeout_path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = _json_from_fenced_block(text)
        if data is None:
            _append_message(
                messages,
                severity="error",
                code="invalid_closeout_json",
                message=f"{closeout_path} does not contain a JSON evidence index",
                source_path=closeout_path,
            )
            return None
    if not isinstance(data, dict):
        _append_message(
            messages,
            severity="error",
            code="invalid_closeout_json",
            message=f"{closeout_path} evidence index must be a JSON object",
            source_path=closeout_path,
        )
        return None
    return data


def _json_from_fenced_block(text: str) -> object | None:
    match = re.search(r"```json\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if match is None:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def _append_closeout_preflight_messages(
    closeout: dict[str, Any],
    *,
    program: str,
    batch_id: str,
    closeout_path: str,
    state_fixture: dict[str, Any],
    messages: list[dict[str, str | None]],
) -> None:
    if closeout.get("program") != program:
        _append_message(
            messages,
            severity="error",
            code="closeout_program_mismatch",
            message=f"closeout program does not match {program}",
            source_path=closeout_path,
        )
    if closeout.get("batch_id") != batch_id:
        _append_message(
            messages,
            severity="error",
            code="closeout_batch_mismatch",
            message=f"closeout batch_id does not match {batch_id}",
            source_path=closeout_path,
        )
    artifacts_by_type = _closeout_artifacts_by_type(closeout)
    closeout_artifact = artifacts_by_type.get("closeout")
    if closeout_artifact is not None and closeout_artifact.get("path") != closeout_path:
        _append_message(
            messages,
            severity="error",
            code="closeout_path_mismatch",
            message=f"closeout artifact path does not match {closeout_path}",
            source_path=closeout_path,
        )
    for artifact_type in CLOSEOUT_REQUIRED_ARTIFACT_TYPES:
        if artifact_type not in artifacts_by_type:
            _append_message(
                messages,
                severity="error",
                code=f"missing_{artifact_type.replace('-', '_')}_pointer",
                message=f"closeout is missing {artifact_type} artifact pointer",
                source_path=closeout_path,
            )
    for key, code in (
        ("validation_evidence", "missing_validation_evidence"),
        ("review_evidence", "missing_review_evidence"),
    ):
        value = closeout.get(key)
        if not isinstance(value, list) or not value:
            _append_message(
                messages,
                severity="error",
                code=code,
                message=f"closeout {key} must not be empty",
                source_path=closeout_path,
            )
    _append_missing_closed_obligation_messages(
        closeout,
        batch_id=batch_id,
        state_fixture=state_fixture,
        source_path=closeout_path,
        messages=messages,
    )


def _closeout_artifacts_by_type(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        return {}
    by_type: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        if isinstance(artifact, dict) and isinstance(artifact.get("type"), str):
            by_type[artifact["type"]] = artifact
    return by_type


def _append_missing_closed_obligation_messages(
    closeout: dict[str, Any],
    *,
    batch_id: str,
    state_fixture: dict[str, Any],
    source_path: str,
    messages: list[dict[str, str | None]],
) -> None:
    closeout_obligations = closeout.get("obligations")
    closeout_closed = []
    if isinstance(closeout_obligations, dict):
        closed_value = closeout_obligations.get("closed")
        if isinstance(closed_value, list):
            closeout_closed = [
                obligation
                for obligation in closed_value
                if isinstance(obligation, dict)
            ]
    closed_by_id = {
        obligation.get("id"): obligation
        for obligation in closeout_closed
        if isinstance(obligation.get("id"), str)
    }
    for obligation in _obligations_from_fixture(state_fixture):
        if obligation.status != "closed":
            continue
        if obligation.source_batch != batch_id and obligation.target_batch != batch_id:
            continue
        closeout_obligation = closed_by_id.get(obligation.id)
        evidence_path = (
            closeout_obligation.get("evidence_path")
            if isinstance(closeout_obligation, dict)
            else None
        )
        if not isinstance(evidence_path, str) or not evidence_path:
            _append_message(
                messages,
                severity="error",
                code="missing_closed_obligation_evidence",
                message=f"closed obligation {obligation.id} lacks closeout evidence",
                source_path=source_path,
            )


def _append_closeout_pointer_contract_messages(
    closeout: dict[str, Any],
    *,
    batch_id: str,
    planning_state: PlanningState,
    paths: dict[str, str],
    source_path: str,
    messages: list[dict[str, str | None]],
) -> None:
    for context, artifact in _present_closeout_artifact_pointers(closeout):
        try:
            _validate_closeout_artifact_pointer(
                artifact,
                context,
                batch_id=batch_id,
                fixture_program=None,
                planning_state=planning_state,
                paths=paths,
            )
        except ProtocolValidationError as error:
            _append_message(
                messages,
                severity="error",
                code="invalid_closeout_contract",
                message=str(error),
                source_path=source_path,
            )


def _present_closeout_artifact_pointers(
    closeout: dict[str, Any],
) -> Iterable[tuple[str, object]]:
    artifacts = closeout.get("artifacts")
    if isinstance(artifacts, list):
        for index, artifact in enumerate(artifacts):
            if isinstance(artifact, dict):
                yield f"artifacts[{index}]", artifact
    for key in ("validation_evidence", "review_evidence", "transition_receipts"):
        items = closeout.get(key)
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if isinstance(item, dict) and "artifact" in item:
                yield f"{key}[{index}].artifact", item["artifact"]


def _validate_cleanup_residue(cleanup_residue: dict[str, Any]) -> None:
    classification = _require_string(cleanup_residue, "classification")
    if classification not in {"none", "intentional", "deferred"}:
        raise ProtocolValidationError(
            "cleanup_residue.classification must be 'none', 'intentional', or 'deferred'"
        )
    if "evidence" in cleanup_residue:
        evidence = cleanup_residue["evidence"]
        if not isinstance(evidence, list):
            raise ProtocolValidationError("cleanup_residue.evidence must be an array")
        if len(evidence) > CLOSEOUT_MAX_CLEANUP_RESIDUE_EVIDENCE_ITEMS:
            raise ProtocolValidationError(
                "cleanup_residue.evidence exceeds bounded evidence item limit"
            )
        for index, item in enumerate(evidence):
            _validate_bounded_closeout_summary(
                item,
                f"cleanup_residue.evidence[{index}]",
            )


def _validate_bounded_closeout_summary(value: object, context: str) -> None:
    if not isinstance(value, str) or not value:
        raise ProtocolValidationError(f"{context} must be a non-empty string")
    if len(value) > CLOSEOUT_MAX_SUMMARY_TEXT_CHARS:
        raise ProtocolValidationError(f"{context} exceeds bounded evidence limit")
    lowered = value.lower()
    if "\n" in value or any(term in lowered for term in CLOSEOUT_BANNED_SECTION_TERMS):
        raise ProtocolValidationError(f"{context} is transcript-like or unbounded")


def _validate_bounded_commit_ref(value: object, context: str) -> None:
    if not isinstance(value, str) or not value:
        raise ProtocolValidationError(f"{context} must be a non-empty string")
    if len(value) > CLOSEOUT_MAX_COMMIT_REF_CHARS:
        raise ProtocolValidationError(f"{context} exceeds bounded evidence limit")
    lowered = value.lower()
    if "\n" in value or any(term in lowered for term in CLOSEOUT_BANNED_SECTION_TERMS):
        raise ProtocolValidationError(f"{context} is transcript-like or unbounded")


def _validate_bounded_closeout_artifact_path(value: object, context: str) -> None:
    if not isinstance(value, str) or not value:
        raise ProtocolValidationError(f"{context} must be a non-empty string")
    if len(value) > CLOSEOUT_MAX_ARTIFACT_PATH_CHARS:
        raise ProtocolValidationError(f"{context} exceeds bounded artifact path limit")
    lowered = value.lower()
    if "\n" in value or "\r" in value or any(
        term in lowered for term in CLOSEOUT_BANNED_SECTION_TERMS
    ):
        raise ProtocolValidationError(f"{context} is transcript-like or unbounded")


def _looks_like_commit_hash(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{7,40}", value) is not None


def _validate_bounded_closeout_sections(data: dict[str, Any]) -> None:
    sections = data.get("sections", [])
    if not isinstance(sections, list):
        raise ProtocolValidationError("sections must be an array")
    if len(sections) > CLOSEOUT_MAX_SECTIONS:
        raise ProtocolValidationError("sections exceeds bounded evidence item limit")
    for index, section in enumerate(sections):
        section_data = _require_object(section, f"sections[{index}]")
        title = _require_string(section_data, "title")
        if len(title) > CLOSEOUT_MAX_SECTION_TEXT_CHARS:
            raise ProtocolValidationError(
                f"sections[{index}].title exceeds bounded evidence limit"
            )
        normalized_title = title.strip().lower()
        if "\n" in title or any(
            term in normalized_title for term in CLOSEOUT_BANNED_SECTION_TERMS
        ):
            raise ProtocolValidationError(
                f"sections[{index}].title is transcript-like or unbounded"
            )
        items = _require_array(section_data, "items")
        if len(items) > CLOSEOUT_MAX_SECTION_ITEMS:
            raise ProtocolValidationError(
                f"sections[{index}].items exceeds bounded evidence limit"
            )
        for item_index, item in enumerate(items):
            if not isinstance(item, str) or not item:
                raise ProtocolValidationError(
                    f"sections[{index}].items[{item_index}] must be a non-empty string"
                )
            if len(item) > CLOSEOUT_MAX_SECTION_TEXT_CHARS:
                raise ProtocolValidationError(
                    f"sections[{index}].items[{item_index}] exceeds bounded evidence limit"
                )
            lowered = item.lower()
            if "\n" in item or any(term in lowered for term in CLOSEOUT_BANNED_SECTION_TERMS):
                raise ProtocolValidationError(
                    f"sections[{index}].items[{item_index}] is transcript-like or unbounded"
                )


def _fixture_program_artifact_keys(program: dict[str, Any]) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    artifacts = program.get("artifacts", [])
    if not isinstance(artifacts, list):
        return keys
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_type = artifact.get("type")
        batch_id = artifact.get("batch_id")
        path = artifact.get("path")
        if (
            isinstance(artifact_type, str)
            and isinstance(batch_id, str)
            and isinstance(path, str)
        ):
            keys.add((artifact_type, batch_id, path))
    return keys


def _bootstrap_programs(
    state: PlanningState,
    program_slug: str | None,
) -> tuple[ProgramState, ...]:
    if program_slug is None:
        for program in state.programs:
            _safe_path_segment(program.slug, "program slug")
        return state.programs
    _safe_path_segment(program_slug, "program slug")
    return (_find_program(state, program_slug),)


def _bootstrap_program_object(
    state: PlanningState,
    program: ProgramState,
) -> dict[str, Any]:
    artifacts = _bootstrap_artifacts(state, program)
    queued_batch = _bootstrap_queued_batch_value(state, program)
    return {
        "slug": program.slug,
        "current": _path_under_planning_root(state, program.current_path),
        "ledger": program.ledger.value,
        "selected_dispatch": program.selected_dispatch.value,
        "active_runway": program.active_runway.value,
        "queued_batch": queued_batch,
        "latest_closeout": program.latest_closeout.value,
        "artifacts": artifacts,
    }


def _bootstrap_artifacts(
    state: PlanningState,
    program: ProgramState,
) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for pointer, artifact_type in (
        (program.selected_dispatch, "dispatch"),
        (program.active_runway, "runway"),
        (program.queued_batch, "queued-runway"),
        (program.latest_closeout, "closeout"),
    ):
        if pointer.value is None:
            continue
        batch_id = (
            _batch_id_from_queued_batch_value(pointer.value)
            if artifact_type == "queued-runway"
            else _batch_id_from_path(pointer.value)
        )
        if not batch_id:
            continue
        _append_existing_batch_local_artifacts(
            state,
            program=program,
            batch_id=batch_id,
            artifacts=artifacts,
            seen=seen,
        )
        if pointer.exists is True and artifact_type != "queued-runway":
            _append_bootstrap_artifact(
                artifacts,
                seen,
                artifact_type=artifact_type,
                batch_id=batch_id,
                path=pointer.value,
            )
    return artifacts


def _bootstrap_queued_batch_value(
    state: PlanningState,
    program: ProgramState,
) -> str | None:
    return _migrated_queued_batch_value(state.root, program)


def _migrated_queued_batch_value(
    root_state: RootState,
    program: ProgramState,
) -> str | None:
    value = program.queued_batch.value
    if value is None:
        return None
    batch_id = _batch_id_from_path(value)
    if batch_id:
        return value
    _safe_path_segment(value, "queued batch id")
    _safe_path_segment(program.slug, "program slug")
    return str(
        PurePosixPath(
            _planning_root_prefix_for(root_state),
            "programs",
            program.slug,
            "batches",
            value,
            "runway.md",
        )
    )


def _batch_id_from_queued_batch_value(value: str) -> str:
    batch_id = _batch_id_from_path(value)
    if batch_id:
        return batch_id
    _safe_path_segment(value, "queued batch id")
    return value


def _append_existing_batch_local_artifacts(
    state: PlanningState,
    *,
    program: ProgramState,
    batch_id: str,
    artifacts: list[dict[str, str]],
    seen: set[tuple[str, str, str]],
) -> None:
    paths = _canonical_batch_paths(state, program, batch_id)
    for artifact_type in BATCH_LOCAL_ARTIFACTS:
        artifact_path = paths[artifact_type]
        if _resolve_pointer(state.root.root_path, artifact_path).exists():
            _append_bootstrap_artifact(
                artifacts,
                seen,
                artifact_type=artifact_type,
                batch_id=batch_id,
                path=artifact_path,
            )


def _append_bootstrap_artifact(
    artifacts: list[dict[str, str]],
    seen: set[tuple[str, str, str]],
    *,
    artifact_type: str,
    batch_id: str,
    path: str,
) -> None:
    key = (artifact_type, batch_id, path)
    if key in seen:
        return
    if any(artifact["path"] == path for artifact in artifacts):
        return
    seen.add(key)
    artifacts.append(
        {
            "batch_id": batch_id,
            "path": path,
            "type": artifact_type,
        }
    )


def _bootstrap_contract_object() -> dict[str, Any]:
    return {
        "source": BOOTSTRAP_SOURCE_MARKDOWN_LAYOUT_V1,
        "selection_precedence": BOOTSTRAP_SELECTION_PRECEDENCE,
        "writes_markdown": False,
        "markdown_owned": sorted(BOOTSTRAP_MARKDOWN_OWNED_FIELDS),
        "json_state_fields": sorted(BOOTSTRAP_JSON_STATE_FIELDS),
        "registered_artifact_types": sorted(BATCH_LOCAL_ARTIFACTS),
        "compatibility_evidence": sorted(BOOTSTRAP_COMPATIBILITY_EVIDENCE_CODES),
    }


def _projection_document(
    state: PlanningState,
    *,
    programs: tuple[ProgramState, ...],
    program_slug: str | None,
    database: Path,
    state_file: Path | None,
    state_fixture: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = {
        "schema_version": PROJECTION_SCHEMA_VERSION,
        "planning_root": _planning_root_prefix(state),
        "source_identity": _projection_source_identity(state, programs),
        "state_fixture_identity": (
            _projection_source_artifact("state-fixture", state_file)
            if state_file is not None
            else None
        ),
        "build_command": _projection_build_command(
            state,
            database,
            state_file,
            program_slug=program_slug,
        ),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "tables": sorted(PROJECTION_SCHEMA_TABLES),
    }
    return {
        "protocol": {
            "name": PROJECTION_SCHEMA_NAME,
            "version": PROJECTION_SCHEMA_VERSION,
        },
        "metadata": metadata,
        "allowed_report_fact_types": sorted(PROJECTION_REPORT_FACT_TYPES),
        "report_facts": _projection_report_facts(
            state,
            programs=programs,
            state_fixture=state_fixture,
        ),
    }


def _projection_source_identity(
    state: PlanningState,
    programs: tuple[ProgramState, ...],
) -> dict[str, Any]:
    sources = [_projection_source_artifact("root-current", state.root.current_path)]
    for program in programs:
        sources.append(
            _projection_source_artifact(
                f"program-current:{program.slug}",
                program.current_path,
            )
        )
        if program.ledger.value is not None and program.ledger.exists is True:
            sources.append(
                _projection_source_artifact(
                    f"program-ledger:{program.slug}",
                    _resolve_pointer(state.root.root_path, program.ledger.value),
                )
            )
    return {
        "planning_root": _planning_root_prefix(state),
        "sources": sorted(sources, key=lambda source: (source["kind"], source["path"])),
    }


def _projection_source_artifact(kind: str, path: Path | None) -> dict[str, Any]:
    if path is None:
        raise ProtocolValidationError("projection source path is required")
    try:
        data = path.read_bytes()
        stat = path.stat()
    except FileNotFoundError as error:
        raise ProtocolValidationError(f"projection source is missing: {path}") from error
    if not path.is_file():
        raise ProtocolValidationError(f"projection source is not a file: {path}")
    return {
        "kind": kind,
        "path": str(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "mtime_ns": stat.st_mtime_ns,
    }


def _projection_build_command(
    state: PlanningState,
    database: Path,
    state_file: Path | None,
    *,
    program_slug: str | None,
) -> str:
    parts = [
        "planning_state.py",
        "rebuild-projection",
        "--root",
        _planning_root_prefix(state),
        "--database",
        str(database),
    ]
    if state_file is not None:
        parts.extend(["--state-file", str(state_file)])
    if program_slug is not None:
        parts.extend(["--program", program_slug])
    return " ".join(parts)


def _projection_report_facts(
    state: PlanningState,
    *,
    programs: tuple[ProgramState, ...],
    state_fixture: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for program in programs:
        _append_program_projection_facts(state, facts, program)
    if state_fixture is not None:
        _append_fixture_projection_facts(facts, state_fixture, programs=programs)
    included_batches = _projection_program_batch_ids(programs)
    for obligation in state.obligations:
        if obligation.source_batch in included_batches or (
            obligation.target_batch is not None
            and obligation.target_batch in included_batches
        ):
            facts.append(
                {
                    "fact_type": "obligation",
                    "obligation_id": obligation.id,
                    "owner": obligation.owner,
                    "source_batch": obligation.source_batch,
                    "target_batch": obligation.target_batch,
                    "close_condition": obligation.close_condition,
                    "status": obligation.status,
                    "evidence_path": obligation.evidence_path,
                }
            )
    return sorted(
        facts,
        key=lambda fact: (
            str(fact.get("program") or ""),
            str(fact.get("batch_id") or ""),
            str(fact.get("fact_type") or ""),
            str(fact.get("artifact_type") or ""),
            str(fact.get("path") or ""),
            str(fact.get("obligation_id") or ""),
        ),
    )


def _append_program_projection_facts(
    state: PlanningState,
    facts: list[dict[str, Any]],
    program: ProgramState,
) -> None:
    current_pointer = ArtifactPointer(
        "current",
        _path_under_planning_root(state, program.current_path),
        program.current_path,
        True,
    )
    for pointer_name, pointer in (
        ("current", current_pointer),
        ("ledger", program.ledger),
        ("selected_dispatch", program.selected_dispatch),
        ("active_runway", program.active_runway),
        ("queued_batch", program.queued_batch),
        ("latest_closeout", program.latest_closeout),
    ):
        if pointer.value is None:
            continue
        facts.append(
            {
                "fact_type": "artifact_pointer",
                "program": program.slug,
                "batch_id": _batch_id_from_path(pointer.value),
                "artifact_type": pointer_name,
                "path": pointer.value,
                "status": "exists" if pointer.exists is True else "missing",
            }
        )
    for pointer in (program.selected_dispatch, program.active_runway, program.queued_batch):
        if pointer.value is None:
            continue
        facts.append(
            {
                "fact_type": "pending_batch",
                "program": program.slug,
                "batch_id": _batch_id_from_queued_batch_value(pointer.value),
                "path": (
                    _migrated_queued_batch_value(state.root, program)
                    if pointer is program.queued_batch
                    else pointer.value
                ),
                "status": pointer.label,
            }
        )
    if program.latest_closeout.value is not None:
        facts.append(
            {
                "fact_type": "closeout_evidence_status",
                "program": program.slug,
                "batch_id": _batch_id_from_path(program.latest_closeout.value),
                "path": program.latest_closeout.value,
                "status": "exists" if program.latest_closeout.exists is True else "missing",
                "summary": "latest closeout pointer",
            }
        )


def _append_fixture_projection_facts(
    facts: list[dict[str, Any]],
    state_fixture: dict[str, Any],
    *,
    programs: tuple[ProgramState, ...],
) -> None:
    included_programs = {program.slug for program in programs}
    for program_data in state_fixture.get("programs", []):
        if not isinstance(program_data, dict):
            continue
        slug = program_data.get("slug")
        if slug not in included_programs:
            continue
        for artifact in program_data.get("artifacts", []):
            if not isinstance(artifact, dict):
                continue
            artifact_type = artifact.get("type")
            batch_id = artifact.get("batch_id")
            path = artifact.get("path")
            if not all(isinstance(value, str) for value in (artifact_type, batch_id, path)):
                continue
            facts.append(
                {
                    "fact_type": "artifact_pointer",
                    "program": slug,
                    "batch_id": batch_id,
                    "artifact_type": artifact_type,
                    "path": path,
                    "status": "registered",
                }
            )
            facts.append(
                {
                    "fact_type": "batch_evidence_lookup",
                    "program": slug,
                    "batch_id": batch_id,
                    "artifact_type": artifact_type,
                    "path": path,
                    "status": "registered",
                }
            )
            if artifact_type == "closeout":
                facts.append(
                    {
                        "fact_type": "closeout_evidence_status",
                        "program": slug,
                        "batch_id": batch_id,
                        "path": path,
                        "status": "registered",
                        "summary": "registered closeout evidence pointer",
                    }
                )
            if artifact_type == "receipt":
                facts.append(
                    {
                        "fact_type": "batch_evidence_lookup",
                        "program": slug,
                        "batch_id": batch_id,
                        "artifact_type": "receipt",
                        "path": path,
                        "status": "registered",
                        "summary": "transition receipt pointer",
                    }
                )
    for obligation in state_fixture.get("obligations", []):
        if not isinstance(obligation, dict):
            continue
        facts.append(
            {
                "fact_type": "obligation",
                "obligation_id": obligation.get("id"),
                "owner": obligation.get("owner"),
                "source_batch": obligation.get("source_batch"),
                "target_batch": obligation.get("target_batch"),
                "close_condition": obligation.get("close_condition"),
                "status": obligation.get("status"),
                "evidence_path": obligation.get("evidence_path"),
            }
        )


def _projection_program_batch_ids(programs: tuple[ProgramState, ...]) -> set[str]:
    batch_ids: set[str] = set()
    for program in programs:
        for value in (
            program.selected_dispatch.value,
            program.active_runway.value,
            program.queued_batch.value,
            program.latest_closeout.value,
        ):
            if value:
                batch_ids.add(_batch_id_from_queued_batch_value(value))
    return batch_ids


def _write_projection_database(database: Path, projection: dict[str, Any]) -> None:
    temp_path = database.with_name(f".{database.name}.tmp")
    if temp_path.exists():
        temp_path.unlink()
    try:
        with sqlite3.connect(temp_path) as connection:
            _initialize_projection_database(connection, projection)
        temp_path.replace(database)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _initialize_projection_database(
    connection: sqlite3.Connection,
    projection: dict[str, Any],
) -> None:
    connection.execute(
        "create table projection_metadata (key text primary key, value text not null)"
    )
    connection.execute(
        "create table source_artifacts ("
        "kind text not null, path text not null, sha256 text, mtime_ns integer)"
    )
    connection.execute(
        "create table report_facts ("
        "id integer primary key, fact_type text not null, program text, "
        "batch_id text, payload_json text not null)"
    )
    metadata = projection["metadata"]
    for key in sorted(metadata):
        connection.execute(
            "insert into projection_metadata (key, value) values (?, ?)",
            (key, json.dumps(metadata[key], sort_keys=True)),
        )
    sources = list(metadata["source_identity"]["sources"])
    state_fixture_identity = metadata.get("state_fixture_identity")
    if state_fixture_identity is not None:
        sources.append(state_fixture_identity)
    for source in sources:
        connection.execute(
            "insert into source_artifacts (kind, path, sha256, mtime_ns) "
            "values (?, ?, ?, ?)",
            (
                source["kind"],
                source["path"],
                source.get("sha256"),
                source.get("mtime_ns"),
            ),
        )
    for index, fact in enumerate(projection["report_facts"], start=1):
        connection.execute(
            "insert into report_facts (id, fact_type, program, batch_id, payload_json) "
            "values (?, ?, ?, ?, ?)",
            (
                index,
                fact["fact_type"],
                fact.get("program"),
                fact.get("batch_id"),
                json.dumps(fact, sort_keys=True),
            ),
        )
    connection.commit()


def _bootstrap_blockers(state: PlanningState) -> Iterable[ValidationMessage]:
    for message in state.validation_messages:
        if message.severity == "error":
            yield message


def _format_bootstrap_blockers(messages: list[ValidationMessage]) -> str:
    details = ", ".join(f"{message.code}: {message.message}" for message in messages)
    return f"bootstrap blocked by existing active-state contradictions: {details}"


def _validate_state_file_target_policy(
    state: PlanningState,
    target: Path | None,
    *,
    state_fixture: dict[str, Any] | None = None,
    operation: str,
) -> None:
    if target is None:
        return
    policy = _effective_project_policy(state, state_fixture, target)
    _validate_policy_target(
        state,
        target,
        target_kind="state-file",
        policy=policy,
        policy_value=policy.state_file_policy if policy is not None else "missing",
        policy_path=policy.state_file_path if policy is not None else None,
        source_path=policy.source_path if policy is not None else state.root.current_path,
        operation=operation,
    )


def _validate_projection_preflight_target(
    state: PlanningState,
    target: Path | None,
) -> None:
    if target is None:
        return
    policy = state.project_policy
    _validate_policy_target(
        state,
        target,
        target_kind="projection",
        policy=policy,
        policy_value=policy.projection_policy if policy is not None else "missing",
        policy_path=policy.projection_path if policy is not None else None,
        source_path=policy.source_path if policy is not None else state.root.current_path,
        operation="projection target preflight",
    )


def _state_with_projection_preflight(
    state: PlanningState,
    target: Path | None,
) -> PlanningState:
    messages = tuple(_projection_preflight_messages(state, target))
    if not messages:
        return state
    return replace(
        state,
        validation_messages=(*state.validation_messages, *messages),
    )


def _projection_preflight_messages(
    state: PlanningState,
    target: Path | None,
) -> Iterable[ValidationMessage]:
    if target is None:
        return
    try:
        _validate_projection_preflight_target(state, target)
    except ProtocolValidationError as error:
        yield ValidationMessage(
            "error",
            "projection_target_policy_conflict",
            str(error),
            target,
        )


def _projection_rebuild_blockers(
    state: PlanningState,
    *,
    database: Path,
    state_fixture: dict[str, Any] | None,
) -> Iterable[ValidationMessage]:
    for message in state.validation_messages:
        if message.severity == "error":
            yield message
    try:
        _validate_projection_database_target(
            state,
            database,
            state_fixture=state_fixture,
        )
    except ProtocolValidationError as error:
        yield ValidationMessage(
            "error",
            "projection_target_policy_conflict",
            str(error),
            database,
        )


def _validate_projection_database_target(
    state: PlanningState,
    target: Path,
    *,
    state_fixture: dict[str, Any] | None,
) -> None:
    if ".." in target.parts:
        raise ProtocolValidationError("projection target must not contain dot segments")
    if target.suffix not in PROJECTION_DATABASE_SUFFIXES:
        suffixes = ", ".join(sorted(PROJECTION_DATABASE_SUFFIXES))
        raise ProtocolValidationError(
            f"projection target must use one of these suffixes: {suffixes}"
        )
    if not target.parent.exists():
        raise ProtocolValidationError(f"projection target parent is missing: {target.parent}")
    if target.exists() and target.is_dir():
        raise ProtocolValidationError(f"projection target is a directory: {target}")
    policy = _effective_project_policy(state, state_fixture, target)
    _validate_policy_target(
        state,
        target,
        target_kind="projection",
        policy=policy,
        policy_value=policy.projection_policy if policy is not None else "missing",
        policy_path=policy.projection_path if policy is not None else None,
        source_path=policy.source_path if policy is not None else state.root.current_path,
        operation="rebuild-projection --database",
    )


def _projection_rebuild_result(
    state: PlanningState,
    *,
    database: Path,
    status: str,
    blockers: list[ValidationMessage],
    projection: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = projection["metadata"] if projection is not None else None
    return {
        "protocol": {
            "name": PROJECTION_SCHEMA_NAME,
            "version": PROJECTION_SCHEMA_VERSION,
            "command": "rebuild-projection",
        },
        "status": status,
        "root": _planning_root_prefix(state),
        "database": str(database),
        "metadata": metadata,
        "rows": _projection_row_counts(projection) if projection is not None else None,
        "blockers": [_validation_message_object(message) for message in blockers],
    }


def _projection_row_counts(projection: dict[str, Any]) -> dict[str, int]:
    metadata = projection["metadata"]
    source_identity = metadata["source_identity"]
    state_fixture_identity = metadata.get("state_fixture_identity")
    source_artifact_count = len(source_identity["sources"])
    if state_fixture_identity is not None:
        source_artifact_count += 1
    return {
        "projection_metadata": len(metadata),
        "source_artifacts": source_artifact_count,
        "report_facts": len(projection["report_facts"]),
    }


def _effective_project_policy(
    state: PlanningState,
    state_fixture: dict[str, Any] | None,
    state_fixture_path: Path,
) -> ProjectPolicy | None:
    if state_fixture is not None and state_fixture.get("project_policy") is not None:
        return _project_policy_from_data(state_fixture["project_policy"], state_fixture_path)
    return state.project_policy


def _validate_policy_target(
    state: PlanningState,
    target: Path,
    *,
    target_kind: str,
    policy: ProjectPolicy | None,
    policy_value: str,
    policy_path: str | None,
    source_path: Path,
    operation: str,
) -> None:
    if _is_explicit_temp_proof_target(state, target):
        return
    if policy is None:
        raise ProtocolValidationError(
            _policy_target_error(
                target_kind,
                target,
                policy_value="missing",
                source_path=source_path,
                operation=operation,
                expected=(
                    "declare project policy in the planning root, project "
                    "instructions, active spec, or state fixture; use stdout or "
                    "/tmp proof output for generated-only checks"
                ),
            )
        )
    if policy_value in {"generated-only", "none"}:
        raise ProtocolValidationError(
            _policy_target_error(
                target_kind,
                target,
                policy_value=policy_value,
                source_path=source_path,
                operation=operation,
                expected=(
                    f"{target_kind} path is not declared by policy; use stdout "
                    "or /tmp proof output"
                ),
            )
        )
    if not policy_path:
        raise ProtocolValidationError(
            _policy_target_error(
                target_kind,
                target,
                policy_value=policy_value,
                source_path=source_path,
                operation=operation,
                expected=f"declare {target_kind} path in project policy",
            )
        )
    expected_target = _resolve_policy_target(state, policy_path)
    actual_target = _resolve_policy_target(state, str(target))
    if actual_target != expected_target:
        raise ProtocolValidationError(
            _policy_target_error(
                target_kind,
                target,
                policy_value=policy_value,
                source_path=source_path,
                operation=operation,
                expected=f"expected target from project policy: {policy_path}",
            )
        )


def _policy_target_error(
    target_kind: str,
    target: Path,
    *,
    policy_value: str,
    source_path: Path,
    operation: str,
    expected: str,
) -> str:
    return (
        f"{operation} target {target} conflicts with {target_kind} policy "
        f"{policy_value!r}; expected source of project value: {source_path}; "
        f"{expected}"
    )


def _resolve_policy_target(state: PlanningState, value: str) -> Path:
    return _resolve_pointer(state.root.root_path, value).resolve()


def _is_explicit_temp_proof_target(state: PlanningState, target: Path) -> bool:
    try:
        resolved_target = target.resolve()
        planning_root = state.root.root_path.resolve()
        temp_root = Path(tempfile.gettempdir()).resolve()
    except OSError:
        return False
    if resolved_target == planning_root or planning_root in resolved_target.parents:
        return False
    return resolved_target == temp_root or temp_root in resolved_target.parents


def _validate_bootstrap_state_target(state: PlanningState, target: Path) -> None:
    if ".." in target.parts:
        raise ProtocolValidationError("state-file target must not contain dot segments")
    if target.suffix != ".json":
        raise ProtocolValidationError("state-file target must use a .json suffix")
    target_parent = target.parent
    if not target_parent.exists():
        raise ProtocolValidationError(f"state-file parent is missing: {target_parent}")
    planning_root = state.root.root_path.resolve()
    resolved_target = (target_parent / target.name).resolve()
    policy = state.project_policy
    if (
        policy is None
        and (resolved_target == planning_root or planning_root in resolved_target.parents)
    ):
        raise ProtocolValidationError(
            "state-file target must not be inside the planning root"
        )


def _path_under_planning_root(state: PlanningState, path: Path) -> str:
    return _path_under_root_state(state.root, path)


def _path_under_root_state(root_state: RootState, path: Path) -> str:
    root = root_state.root_path
    try:
        relative = path.relative_to(root)
    except ValueError:
        return path.as_posix()
    return str(PurePosixPath(_planning_root_prefix_for(root_state), *relative.parts))


def _fixture_artifact_keys(data: dict[str, Any]) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    programs = data.get("programs", [])
    if not isinstance(programs, list):
        return keys
    for program in programs:
        if not isinstance(program, dict):
            continue
        keys.update(_fixture_program_artifact_keys(program))
    return keys


def _fixture_program_batch_ids(program: dict[str, Any]) -> set[str]:
    batch_ids: set[str] = set()
    for key in ("selected_dispatch", "active_runway", "queued_batch", "latest_closeout"):
        value = program.get(key)
        if isinstance(value, str):
            batch_id = _batch_id_from_path(value)
            if batch_id:
                batch_ids.add(batch_id)
    artifacts = program.get("artifacts", [])
    if not isinstance(artifacts, list):
        return batch_ids
    for artifact in artifacts:
        if isinstance(artifact, dict) and isinstance(artifact.get("batch_id"), str):
            batch_ids.add(artifact["batch_id"])
    return batch_ids


def _obligation_fact_key(data: dict[str, Any]) -> tuple[str, str | None, str, str | None, str | None, str, str | None]:
    return (
        str(data.get("id") or ""),
        data.get("owner"),
        str(data.get("source_batch") or ""),
        data.get("target_batch"),
        data.get("close_condition"),
        str(data.get("status") or ""),
        data.get("evidence_path"),
    )


def _obligations_from_fixture(
    state_fixture: dict[str, Any] | None,
) -> Iterable[ObligationRecord]:
    if state_fixture is None:
        return
    obligations = state_fixture.get("obligations", [])
    if not isinstance(obligations, list):
        return
    for obligation in obligations:
        if not isinstance(obligation, dict):
            continue
        yield ObligationRecord(
            id=str(obligation.get("id") or ""),
            owner=obligation.get("owner"),
            source_batch=str(obligation.get("source_batch") or ""),
            target_batch=obligation.get("target_batch"),
            close_condition=obligation.get("close_condition"),
            status=str(obligation.get("status") or ""),
            evidence_path=obligation.get("evidence_path"),
        )


def _state_fixture_validation_messages(
    root_state: RootState,
    programs: tuple[ProgramState, ...],
    state_fixture: dict[str, Any],
) -> Iterable[ValidationMessage]:
    markdown_programs = {program.slug: program for program in programs}
    seen_programs: set[str] = set()
    duplicate_programs: set[str] = set()
    fixture_programs = state_fixture.get("programs", [])
    if not isinstance(fixture_programs, list):
        return
    for fixture_program in fixture_programs:
        if not isinstance(fixture_program, dict):
            continue
        slug = fixture_program.get("slug")
        if not isinstance(slug, str):
            continue
        if slug in seen_programs and slug not in duplicate_programs:
            duplicate_programs.add(slug)
            yield ValidationMessage(
                "error",
                "duplicate_fixture_program",
                f"state fixture defines program {slug} more than once",
            )
        seen_programs.add(slug)
        program = markdown_programs.get(slug)
        if program is None:
            yield ValidationMessage(
                "error",
                "unknown_fixture_program",
                f"state fixture program {slug} is not active in root CURRENT.md",
            )
            continue
        yield from _fixture_program_consistency_messages(
            root_state,
            program,
            fixture_program,
        )


def _fixture_program_consistency_messages(
    root_state: RootState,
    program: ProgramState,
    fixture_program: dict[str, Any],
) -> Iterable[ValidationMessage]:
    for field_name, expected in (
        ("current", _path_under_root_state(root_state, program.current_path)),
        ("ledger", program.ledger.value),
        ("selected_dispatch", program.selected_dispatch.value),
        ("active_runway", program.active_runway.value),
        ("queued_batch", _migrated_queued_batch_value(root_state, program)),
        ("latest_closeout", program.latest_closeout.value),
    ):
        actual = fixture_program.get(field_name)
        if actual != expected:
            yield ValidationMessage(
                "error",
                "migrated_state_mismatch",
                (
                    f"state fixture {program.slug}.{field_name} "
                    "does not match CURRENT.md"
                ),
                program.current_path,
            )
    if len(_fixture_active_values(fixture_program)) > 1:
        yield ValidationMessage(
            "error",
            "fixture_active_state_conflict",
            "state fixture selects more than one dispatch, active runway, or queued batch",
        )
    yield from _fixture_artifact_duplicate_messages(fixture_program)
    for field_name, artifact_type in (
        ("selected_dispatch", "dispatch"),
        ("active_runway", "runway"),
        ("queued_batch", "runway"),
    ):
        pointer = fixture_program.get(field_name)
        if isinstance(pointer, str) and not _fixture_registers_active_pointer(
            fixture_program,
            artifact_type=artifact_type,
            pointer=pointer,
        ):
            yield ValidationMessage(
                "error",
                "unregistered_active_batch_pointer",
                (
                    f"state fixture {program.slug}.{field_name} "
                    "does not reference a registered artifact"
                ),
            )


def _fixture_artifact_duplicate_messages(
    fixture_program: dict[str, Any],
) -> Iterable[ValidationMessage]:
    seen: set[tuple[str, str, str]] = set()
    duplicate_keys: set[tuple[str, str, str]] = set()
    artifacts_by_identity: dict[tuple[str, str], str] = {}
    collided_identities: set[tuple[str, str]] = set()
    artifacts_by_path: dict[str, tuple[str, str]] = {}
    collided_paths: set[str] = set()
    artifacts = fixture_program.get("artifacts", [])
    if not isinstance(artifacts, list):
        return
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_type = artifact.get("type")
        batch_id = artifact.get("batch_id")
        path = artifact.get("path")
        if not (
            isinstance(artifact_type, str)
            and isinstance(batch_id, str)
            and isinstance(path, str)
        ):
            continue
        key = (artifact_type, batch_id, path)
        if key in seen and key not in duplicate_keys:
            duplicate_keys.add(key)
            yield ValidationMessage(
                "error",
                "duplicate_artifact_registration",
                f"state fixture duplicates {artifact_type} for {batch_id}",
            )
        seen.add(key)
        identity = (artifact_type, batch_id)
        previous_path = artifacts_by_identity.get(identity)
        if (
            previous_path is not None
            and previous_path != path
            and identity not in collided_identities
        ):
            collided_identities.add(identity)
            yield ValidationMessage(
                "error",
                "artifact_registration_collision",
                (
                    f"state fixture registers {artifact_type} for {batch_id} "
                    "with more than one path"
                ),
            )
        artifacts_by_identity.setdefault(identity, path)
        previous_identity = artifacts_by_path.get(path)
        if (
            previous_identity is not None
            and previous_identity != identity
            and path not in collided_paths
        ):
            collided_paths.add(path)
            yield ValidationMessage(
                "error",
                "artifact_path_collision",
                f"state fixture registers {path} for more than one artifact",
            )
        artifacts_by_path.setdefault(path, identity)


def _fixture_registers_active_pointer(
    fixture_program: dict[str, Any],
    *,
    artifact_type: str,
    pointer: str,
) -> bool:
    artifacts = fixture_program.get("artifacts", [])
    if not isinstance(artifacts, list):
        return False
    batch_id = _batch_id_from_path(pointer)
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get("type") != artifact_type:
            continue
        if artifact.get("path") == pointer:
            return True
        if batch_id is None and artifact.get("batch_id") == pointer:
            return True
    return False


def _obligation_validation_messages(
    state_fixture: dict[str, Any],
) -> Iterable[ValidationMessage]:
    known_batches = _fixture_batch_ids(state_fixture)
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for obligation in _obligations_from_fixture(state_fixture):
        if obligation.id in seen_ids and obligation.id not in duplicate_ids:
            duplicate_ids.add(obligation.id)
            yield ValidationMessage(
                "error",
                "duplicate_obligation_id",
                f"obligation {obligation.id} is defined more than once",
            )
        seen_ids.add(obligation.id)
        if not obligation.owner:
            yield ValidationMessage(
                "error",
                "missing_obligation_owner",
                f"obligation {obligation.id} has no owner",
            )
        if not obligation.target_batch and not obligation.close_condition:
            yield ValidationMessage(
                "error",
                "missing_obligation_close_condition",
                f"obligation {obligation.id} has no target batch or close condition",
            )
        if obligation.status == "closed" and not obligation.evidence_path:
            yield ValidationMessage(
                "error",
                "missing_obligation_evidence",
                f"closed obligation {obligation.id} has no evidence path",
            )
        if obligation.source_batch not in known_batches:
            yield ValidationMessage(
                "error",
                "orphaned_obligation",
                f"obligation {obligation.id} source batch is not registered",
            )
        yield ValidationMessage(
            "info",
            f"{obligation.status}_obligation",
            f"obligation {obligation.id} is {obligation.status}",
        )


def _fixture_batch_ids(state_fixture: dict[str, Any]) -> set[str]:
    batch_ids: set[str] = set()
    programs = state_fixture.get("programs", [])
    if not isinstance(programs, list):
        return batch_ids
    for program in programs:
        if not isinstance(program, dict):
            continue
        for key in ("selected_dispatch", "active_runway", "queued_batch"):
            value = program.get(key)
            if isinstance(value, str):
                batch_id = _batch_id_from_path(value)
                if batch_id:
                    batch_ids.add(batch_id)
        artifacts = program.get("artifacts", [])
        if not isinstance(artifacts, list):
            continue
        for artifact in artifacts:
            if isinstance(artifact, dict) and isinstance(artifact.get("batch_id"), str):
                batch_ids.add(artifact["batch_id"])
    return batch_ids


def _batch_id_from_path(value: str) -> str | None:
    parts = PurePosixPath(value).parts
    if "batches" not in parts:
        return None
    index = parts.index("batches") + 1
    if index >= len(parts):
        return None
    return parts[index]


def _normalize_artifact_type(value: str) -> str:
    artifact_type = value.strip()
    if artifact_type not in SUPPORTED_ARTIFACT_TYPES:
        raise ProtocolValidationError(f"unsupported artifact type: {value}")
    return artifact_type


def _find_program(state: PlanningState, slug: str) -> ProgramState:
    for program in state.programs:
        if program.slug == slug:
            if not program.current_path.exists():
                raise ProtocolValidationError(f"program root is missing: {slug}")
            _safe_path_segment(program.slug, "program slug")
            return program
    raise ProtocolValidationError(f"program root is missing: {slug}")


def _canonical_batch_paths(
    state: PlanningState,
    program: ProgramState,
    batch_id: str,
) -> dict[str, str]:
    if not batch_id or "/" in batch_id or "\\" in batch_id or batch_id in {".", ".."}:
        raise ProtocolValidationError("batch-id must be a single path segment")
    if ".." in Path(batch_id).parts:
        raise ProtocolValidationError("batch-id must not escape the batch directory")
    root = _planning_root_prefix(state)
    batch_directory = f"{root}/programs/{program.slug}/batches/{batch_id}"
    paths = {"batch_directory": batch_directory}
    paths.update(
        {
            artifact_type: f"{batch_directory}/{filename}"
            for artifact_type, filename in BATCH_LOCAL_ARTIFACTS.items()
        }
    )
    return paths


def _planning_root_prefix(state: PlanningState) -> str:
    return _planning_root_prefix_for(state.root)


def _planning_root_prefix_for(root_state: RootState) -> str:
    root = (root_state.planning_root or "").strip().rstrip("/")
    if not root:
        raise ProtocolValidationError("planning root is missing")
    _safe_relative_path(root, "planning root")
    return root


def _safe_path_segment(value: str, label: str) -> str:
    if (
        not value
        or "/" in value
        or "\\" in value
        or value in {".", ".."}
    ):
        raise ProtocolValidationError(f"{label} must be a single path segment")
    return value


def _safe_relative_path(value: str, label: str) -> str:
    if "\\" in value:
        raise ProtocolValidationError(f"{label} must use relative POSIX paths")
    path = PurePosixPath(value)
    if path.is_absolute():
        raise ProtocolValidationError(f"{label} must be relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ProtocolValidationError(f"{label} must not contain dot segments")
    return value


def _validate_registered_path(
    state: PlanningState,
    *,
    artifact_type: str,
    artifact_path: str,
    paths: dict[str, str],
) -> None:
    path = Path(artifact_path)
    if path.is_absolute():
        raise ProtocolValidationError("artifact path must be relative to the workspace")
    if ".." in path.parts:
        raise ProtocolValidationError("artifact path must not escape the planning root")
    planning_root = _planning_root_prefix(state)
    if path.parts[: len(Path(planning_root).parts)] != Path(planning_root).parts:
        raise ProtocolValidationError("artifact path must be under the planning root")
    if artifact_type in BATCH_LOCAL_ARTIFACTS and artifact_path != paths[artifact_type]:
        raise ProtocolValidationError(
            f"{artifact_type} must be co-located at {paths[artifact_type]}"
        )
    batch_directory = Path(paths["batch_directory"])
    if (
        artifact_type not in BATCH_LOCAL_ARTIFACTS
        and path.parts[: len(batch_directory.parts)] != batch_directory.parts
    ):
        raise ProtocolValidationError("artifact path must be co-located with the batch")


def _validate_batch_not_exists(state: PlanningState, batch_directory: str) -> None:
    if _resolve_pointer(state.root.root_path, batch_directory).exists():
        raise ProtocolValidationError(f"batch directory already exists: {batch_directory}")


def _load_state_fixture(
    path: Path | None,
    *,
    expected_root: str,
    allow_malformed_project_policy: bool = False,
) -> dict[str, Any]:
    if path is None:
        raise ProtocolValidationError("state-file is required")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ProtocolValidationError(f"state-file is missing: {path}") from error
    except json.JSONDecodeError as error:
        raise ProtocolValidationError(f"state-file is not valid JSON: {path}") from error
    if allow_malformed_project_policy and "project_policy" in data:
        validation_data = dict(data)
        validation_data.pop("project_policy")
        validate_state_fixture_object(validation_data)
    else:
        data = validate_state_fixture_object(data)
    _validate_state_fixture_root(data, expected_root=expected_root)
    return data


def _validate_state_fixture_root(
    data: dict[str, Any],
    *,
    expected_root: str,
) -> None:
    fixture_root = data["root"].strip().rstrip("/")
    if fixture_root != expected_root:
        raise ProtocolValidationError(
            "state_file_root_mismatch: state-file root does not match planning root: "
            f"{fixture_root} != {expected_root}"
        )


def _write_state_fixture(path: Path | None, data: dict[str, Any]) -> None:
    if path is None:
        raise ProtocolValidationError("state-file is required")
    if not path.parent.exists():
        raise ProtocolValidationError(f"state-file parent is missing: {path.parent}")
    temp_path = path.with_name(f".{path.name}.tmp")
    temp_path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(path)


def _write_receipt_fixture(path: Path | None, data: dict[str, Any]) -> None:
    if path is None:
        return
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _register_artifact_in_fixture(
    data: dict[str, Any],
    *,
    program_slug: str,
    registration: dict[str, str],
) -> None:
    programs = _require_array(data, "programs")
    program_data = next(
        (
            _require_object(program, "program")
            for program in programs
            if isinstance(program, dict) and program.get("slug") == program_slug
        ),
        None,
    )
    if program_data is None:
        raise ProtocolValidationError(f"program root is missing: {program_slug}")
    artifacts = program_data.setdefault("artifacts", [])
    if not isinstance(artifacts, list):
        raise ProtocolValidationError("artifacts must be an array")
    for artifact in artifacts:
        artifact_data = _require_object(artifact, "artifact")
        if (
            artifact_data.get("batch_id") == registration["batch_id"]
            and artifact_data.get("type") == registration["type"]
        ):
            if artifact_data.get("path") == registration["path"]:
                raise ProtocolValidationError("artifact is already registered")
            raise ProtocolValidationError("artifact registration collides with existing path")
        if artifact_data.get("path") == registration["path"]:
            raise ProtocolValidationError("artifact path collides with existing registration")
    artifacts.append(registration)


def _fixture_program(data: dict[str, Any], program_slug: str) -> dict[str, Any]:
    programs = _require_array(data, "programs")
    program_data = next(
        (
            _require_object(program, "program")
            for program in programs
            if isinstance(program, dict) and program.get("slug") == program_slug
        ),
        None,
    )
    if program_data is None:
        raise ProtocolValidationError(f"program root is missing: {program_slug}")
    return program_data


def _validate_transition_artifact(
    state: PlanningState,
    *,
    artifact_type: str,
    artifact_path: str,
    paths: dict[str, str],
    messages: list[dict[str, str | None]],
) -> None:
    try:
        _validate_registered_path(
            state,
            artifact_type=artifact_type,
            artifact_path=artifact_path,
            paths=paths,
        )
    except ProtocolValidationError as error:
        _append_message(
            messages,
            severity="error",
            code="invalid_artifact_path",
            message=str(error),
            source_path=artifact_path,
        )
        return
    if not _resolve_pointer(state.root.root_path, artifact_path).exists():
        _append_message(
            messages,
            severity="error",
            code=f"missing_{artifact_type}",
            message=f"{artifact_path} is missing",
            source_path=artifact_path,
        )


def _validate_no_active_transition_state(
    program: ProgramState,
    program_data: dict[str, Any],
    messages: list[dict[str, str | None]],
) -> None:
    if _fixture_active_values(program_data):
        _append_message(
            messages,
            severity="error",
            code="fixture_active_state_conflict",
            message=(
                "state fixture already selects a dispatch, active runway, "
                "or queued batch"
            ),
            source_path=program_data.get("current"),
        )
    if any(
        pointer.value is not None
        for pointer in (
            program.selected_dispatch,
            program.active_runway,
            program.queued_batch,
        )
    ):
        _append_message(
            messages,
            severity="error",
            code="markdown_active_state_conflict",
            message=(
                "CURRENT.md already selects a dispatch, active runway, "
                "or queued batch"
            ),
            source_path=str(program.current_path),
        )


def _validate_queue_transition_state(
    program: ProgramState,
    program_data: dict[str, Any],
    dispatch_path: str,
    messages: list[dict[str, str | None]],
) -> None:
    active_runway = program_data.get("active_runway")
    queued_batch = program_data.get("queued_batch")
    selected_dispatch = program_data.get("selected_dispatch")
    if active_runway or queued_batch:
        _append_message(
            messages,
            severity="error",
            code="fixture_active_state_conflict",
            message="state fixture already has an active runway or queued batch",
            source_path=program_data.get("current"),
        )
    if selected_dispatch != dispatch_path:
        _append_message(
            messages,
            severity="error",
            code="stale_selected_dispatch",
            message=(
                "state fixture selected dispatch does not match the queued "
                "dispatch"
            ),
            source_path=selected_dispatch,
        )
    if (
        program.active_runway.value is not None
        or program.queued_batch.value is not None
    ):
        _append_message(
            messages,
            severity="error",
            code="markdown_active_state_conflict",
            message="CURRENT.md already has an active runway or queued batch",
            source_path=str(program.current_path),
        )
    if (
        program.selected_dispatch.value is not None
        and program.selected_dispatch.value != dispatch_path
    ):
        _append_message(
            messages,
            severity="error",
            code="markdown_selected_dispatch_conflict",
            message="CURRENT.md selected dispatch does not match the queued dispatch",
            source_path=str(program.current_path),
        )


def _fixture_active_values(program_data: dict[str, Any]) -> list[Any]:
    return [
        program_data.get(key)
        for key in ("selected_dispatch", "active_runway", "queued_batch")
        if program_data.get(key) is not None
    ]


def _validate_registered_artifact(
    program_data: dict[str, Any],
    *,
    artifact_type: str,
    batch_id: str,
    artifact_path: str,
    messages: list[dict[str, str | None]],
) -> None:
    artifacts = program_data.get("artifacts", [])
    if not isinstance(artifacts, list):
        _append_message(
            messages,
            severity="error",
            code="invalid_state_fixture",
            message="artifacts must be an array",
            source_path=program_data.get("current"),
        )
        return
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if (
            artifact.get("type") == artifact_type
            and artifact.get("batch_id") == batch_id
            and artifact.get("path") == artifact_path
        ):
            return
    _append_message(
        messages,
        severity="error",
        code=f"unregistered_{artifact_type}",
        message=f"{artifact_type} is not registered for {batch_id}",
        source_path=artifact_path,
    )


def _validate_batch_known_to_ledger(
    program: ProgramState,
    batch_id: str,
    messages: list[dict[str, str | None]],
) -> None:
    if program.ledger.value is None or program.ledger.exists is False:
        return
    ledger_root = program.current_path.parent.parent.parent
    ledger_text = _read_text(_resolve_pointer(ledger_root, program.ledger.value))
    batch_rows = [
        line
        for line in ledger_text.splitlines()
        if line.lstrip().startswith("|") and "/batches/" in line
    ]
    known_batch_ids: set[str] = set()
    for row in batch_rows:
        for code_value in re.findall(r"`([^`]+)`", row):
            path = PurePosixPath(code_value)
            parts = path.parts
            if "batches" not in parts:
                continue
            batch_index = parts.index("batches") + 1
            if batch_index >= len(parts):
                continue
            known_batch_ids.add(parts[batch_index])
    if batch_rows and batch_id not in known_batch_ids:
        _append_message(
            messages,
            severity="error",
            code="unknown_ledger_batch",
            message=f"{batch_id} does not match a known program ledger batch row",
            source_path=program.ledger.value,
        )


def _append_obligation_messages(
    data: dict[str, Any],
    messages: list[dict[str, str | None]],
) -> None:
    for message in _obligation_validation_messages(data):
        _append_message(
            messages,
            severity=message.severity,
            code=message.code,
            message=message.message,
            source_path=message.source_path,
        )


def _obligations_for_batch(
    data: dict[str, Any],
    batch_id: str,
) -> list[dict[str, str | None]]:
    obligations = []
    for obligation in _obligations_from_fixture(data):
        if obligation.source_batch == batch_id or obligation.target_batch == batch_id:
            obligations.append(_obligation_object(obligation))
    return obligations


def _transition_receipt(
    state: PlanningState,
    *,
    transition: str,
    program: str,
    batch_id: str,
    artifacts: list[dict[str, str]],
    obligations: list[dict[str, str | None]],
    messages: list[dict[str, str | None]],
) -> dict[str, Any]:
    blockers = [message for message in messages if message["severity"] == "error"]
    warnings = [message for message in messages if message["severity"] == "warning"]
    receipt = {
        "protocol": {
            "name": RECEIPT_FIXTURE_SCHEMA_NAME,
            "version": SUPPORTED_SCHEMA_VERSION,
            "transition_protocol": TRANSITION_RECEIPT_PROTOCOL_NAME,
        },
        "root": _planning_root_prefix(state),
        "transition": transition,
        "status": "rejected" if blockers else "applied",
        "program": program,
        "batch_id": batch_id,
        "artifacts": artifacts,
        "obligations": obligations,
        "warnings": warnings,
        "blockers": blockers,
        "messages": messages,
    }
    validate_receipt_fixture_object(receipt)
    return receipt


def _append_message(
    messages: list[dict[str, str | None]],
    *,
    severity: str,
    code: str,
    message: str,
    source_path: object | None,
) -> None:
    messages.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "source_path": str(source_path) if source_path is not None else None,
        }
    )


def _has_validation_errors(state: PlanningState) -> bool:
    return any(message.severity == "error" for message in state.validation_messages)


def _has_message_errors(messages: Iterable[dict[str, str | None]]) -> bool:
    return any(message.get("severity") == "error" for message in messages)


def _has_message_codes(
    messages: Iterable[dict[str, str | None]],
    codes: set[str],
) -> bool:
    return any(message.get("code") in codes for message in messages)


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
