import json
from pathlib import Path
import re
import subprocess
import sys

from scripts.planning_state import (
    CLOSEOUT_MAX_ARTIFACT_PATH_CHARS,
    CLOSEOUT_MAX_CLEANUP_RESIDUE_EVIDENCE_ITEMS,
    CLOSEOUT_MAX_COMMITS,
    CLOSEOUT_MAX_COMMIT_REF_CHARS,
    CLOSEOUT_MAX_REVIEW_EVIDENCE_ITEMS,
    CLOSEOUT_MAX_SECTIONS,
    CLOSEOUT_MAX_TRANSITION_RECEIPTS,
    CLOSEOUT_MAX_VALIDATION_EVIDENCE_ITEMS,
    ProtocolValidationError,
    format_current_state,
    format_protocol_report,
    format_validation_report,
    load_planning_state,
    validate_closeout_evidence_index_object,
    validate_receipt_fixture_object,
    validate_state_fixture_object,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PLANNING_STATE_SCRIPT = REPO_ROOT / "scripts" / "planning_state.py"


def test_loads_codex_config_layout_v1_root_and_program_state(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    state = load_planning_state(root)

    assert state.root.layout == "Planning Artifact Layout v1"
    assert state.root.planning_root == "docs/plans/"
    assert [program.slug for program in state.programs] == [
        "architecture-program-runner",
        "planning-state-tooling",
    ]
    planning_program = state.programs[1]
    assert planning_program.ledger.value == (
        "docs/plans/programs/planning-state-tooling/LEDGER.md"
    )
    assert planning_program.queued_batch.value == (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-readonly-core/runway.md"
    )
    assert planning_program.queued_batch.exists is True
    assert planning_program.selected_dispatch.value is None
    assert planning_program.next_safe_action is not None


def test_loads_graphify_style_layout_v1_program_state(tmp_path: Path) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)

    state = load_planning_state(root)

    assert state.root.planning_root == "my-docs/plans/"
    assert state.root.one_shot_intake == "my-docs/plans/intake/"
    assert [program.slug for program in state.programs] == [
        "install-sandbox-test-quality-architecture",
        "install-sandbox-legacy-removal",
    ]
    tqa_program = state.programs[0]
    assert tqa_program.latest_closeout.value == (
        "my-docs/plans/programs/install-sandbox-test-quality-architecture/"
        "batches/tqa-b11-target-selection-diagnostic-wording/runway.md"
    )
    assert tqa_program.run_artifact_location.value == (
        "my-docs/runs/batch-runway/install-sandbox-test-quality-architecture/"
    )
    assert tqa_program.queued_batch.value is None


def test_redirect_ledgers_are_evidence_not_active_sources(tmp_path: Path) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)

    state = load_planning_state(root)

    redirect_paths = {redirect.source_path.name for redirect in state.redirects}
    assert redirect_paths == {
        "install-sandbox-legacy-removal-ledger.md",
        "install-sandbox-test-quality-architecture-ledger.md",
    }
    assert {
        warning.code for warning in state.warnings if warning.source_path is not None
    } >= {"redirect_ledger"}
    assert all(
        program.ledger.source_path.name == "CURRENT.md" for program in state.programs
    )


def test_historical_batch_artifacts_warn_without_overriding_current_state(
    tmp_path: Path,
) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)

    state = load_planning_state(root)

    warning_codes = {warning.code for warning in state.warnings}
    assert "historical_batch_artifact" in warning_codes
    assert "stale_pickup_note" in warning_codes
    assert "stale_pickup_contradiction" in warning_codes
    assert all(program.queued_batch.value is None for program in state.programs)
    assert all(program.active_runway.value is None for program in state.programs)


def test_reports_missing_program_current_without_scanning_historical_files(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)
    (root / "CURRENT.md").write_text(
        """# Planning Current State

- Layout: Planning Artifact Layout v1

## Active Programs

| Program | Current state |
|---|---|
| `missing-program` | `docs/plans/programs/missing-program/CURRENT.md` |
""",
        encoding="utf-8",
    )
    (root / "missing-program-runway.md").write_text("# Historical\n", encoding="utf-8")

    state = load_planning_state(root)

    assert [message.code for message in state.validation_messages] == [
        "missing_program_current"
    ]
    assert state.programs[0].slug == "missing-program"
    assert state.programs[0].active_runway.value is None
    assert "historical_batch_artifact" in {warning.code for warning in state.warnings}


def test_formats_current_for_codex_config_programs_from_current_files(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    output = format_current_state(load_planning_state(root))

    assert "layout: Planning Artifact Layout v1" in output
    assert "planning_root: docs/plans/" in output
    assert "slug: architecture-program-runner" in output
    assert "slug: planning-state-tooling" in output
    assert (
        "queued_batch: docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-readonly-core/runway.md"
    ) in output
    assert "selected_dispatch: None" in output
    assert "blockers:\n    []" in output


def test_current_command_reports_graphify_current_without_historical_selection(
    tmp_path: Path,
) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)

    output = _run_current(root)

    assert "planning_root: my-docs/plans/" in output
    assert "slug: install-sandbox-test-quality-architecture" in output
    assert "slug: install-sandbox-legacy-removal" in output
    assert "queued_batch: None" in output
    assert "active_runway: None" in output
    assert "redirect_ledger:" in output
    assert "historical_batch_artifact:" in output
    assert "stale_pickup_contradiction:" in output


def test_current_command_reports_missing_current_blocker_without_old_runway_pickup(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)
    (root / "CURRENT.md").write_text(
        """# Planning Current State

- Layout: Planning Artifact Layout v1

## Active Programs

| Program | Current state |
|---|---|
| `missing-program` | `docs/plans/programs/missing-program/CURRENT.md` |
""",
        encoding="utf-8",
    )
    (root / "missing-program-runway.md").write_text("# Historical\n", encoding="utf-8")

    output = _run_current(root)

    assert "slug: missing-program" in output
    assert "active_runway: None" in output
    assert "blockers:" in output
    assert "missing_program_current:" in output
    assert "historical_batch_artifact:" in output


def test_current_command_reports_validation_warnings(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)
    (root / "CURRENT.md").write_text(
        """# Planning Current State

- Layout: Legacy Planning Layout
""",
        encoding="utf-8",
    )

    output = _run_current(root)

    assert "warnings:" in output
    assert "unknown_layout:" in output
    assert "no_active_programs:" in output
    assert "blockers:\n    []" in output


def test_current_json_protocol_reports_root_program_warning_and_exit_facts(
    tmp_path: Path,
) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)

    result = _run_current_json(root)
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["protocol"] == {
        "name": "planning-state-facts",
        "version": 1,
        "command": "current",
    }
    assert payload["exit"]["code"] == 0
    assert payload["exit"]["meaning"] == "success"
    assert payload["exit"]["semantics"]["1"] == (
        "validate completed and found blockers"
    )
    assert payload["root"]["planning_root"] == "my-docs/plans/"
    assert payload["programs"][0]["slug"] == (
        "install-sandbox-test-quality-architecture"
    )
    assert payload["programs"][0]["queued_batch"]["value"] is None
    assert {warning["code"] for warning in payload["warnings"]} >= {
        "redirect_ledger",
        "stale_pickup_note",
        "historical_batch_artifact",
    }
    assert payload["blockers"] == []
    assert all("severity" in message for message in payload["validation_messages"])


def test_json_protocol_normalizes_wrapped_live_style_fields(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    (root / "CURRENT.md").write_text(
        """# Planning Current State

## Layout

- Layout: Planning Artifact Layout v1
- Planning root: `docs/plans/`
- Run artifact root: `<program-root>/architecture-program-runs/` when a program
  uses the architecture-program runner; otherwise `None selected`
- Output root: `None selected`
- One-shot intake: `None`
- Program archive root: `docs/plans/archive/`

## Active Programs

| Program | Current state |
|---|---|
| `planning-state-tooling` | `docs/plans/programs/planning-state-tooling/CURRENT.md` |
""",
        encoding="utf-8",
    )
    (root / "programs" / "planning-state-tooling" / "CURRENT.md").write_text(
        """# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md`
- Latest closeout path: `None`
- Run artifact location: `None selected`
- Program archive location: `docs/plans/archive/`
""",
        encoding="utf-8",
    )

    result = _run_validate_json(root)
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["root"]["run_artifact_root"] == (
        "<program-root>/architecture-program-runs/ when a program uses the "
        "architecture-program runner; otherwise None selected"
    )
    assert payload["programs"][0]["purpose"] == (
        "add tool-owned planning-state diagnostics and later state transitions "
        "while keeping Markdown and JSON canonical."
    )
    assert payload["programs"][0]["queued_batch"]["value"] == (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-readonly-core/runway.md"
    )
    assert "`" not in payload["root"]["run_artifact_root"]
    assert "`" not in payload["programs"][0]["purpose"]


def test_validate_json_protocol_reports_blockers_and_exit_facts(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)

    result = _run_validate_json(root)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["protocol"]["command"] == "validate"
    assert payload["exit"]["code"] == 1
    assert payload["exit"]["meaning"] == "validation_failed"
    assert payload["blockers"] == [
        {
            "severity": "error",
            "code": "missing_root_current",
            "message": "root CURRENT.md is missing",
            "source_path": str(root / "CURRENT.md"),
        }
    ]


def test_json_protocol_rejects_unsupported_versions(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    result = subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "current",
            "--root",
            str(root),
            "--format",
            "json",
            "--protocol-version",
            "2",
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "unsupported planning-state protocol version: 2" in result.stderr


def test_protocol_formatter_rejects_unsupported_versions(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    try:
        format_protocol_report(
            load_planning_state(root),
            command="current",
            exit_code=0,
            protocol_version=2,
        )
    except ProtocolValidationError as error:
        assert "unsupported planning-state protocol version: 2" in str(error)
    else:
        raise AssertionError("expected unsupported protocol version to fail")


def test_state_fixture_schema_rejects_malformed_objects() -> None:
    valid_state = {
        "protocol": {
            "name": "planning-state-tool-state",
            "version": 1,
        },
        "root": "docs/plans",
        "programs": [
            {
                "slug": "planning-state-tooling",
                "current": "docs/plans/programs/planning-state-tooling/CURRENT.md",
                "ledger": "docs/plans/programs/planning-state-tooling/LEDGER.md",
                "selected_dispatch": None,
                "active_runway": None,
                "queued_batch": None,
                "latest_closeout": None,
            }
        ],
    }

    assert validate_state_fixture_object(valid_state) == valid_state
    malformed_state = {**valid_state, "protocol": {"name": "wrong", "version": 1}}
    try:
        validate_state_fixture_object(malformed_state)
    except ProtocolValidationError as error:
        assert "state fixture.protocol.name" in str(error)
    else:
        raise AssertionError("expected malformed state fixture to fail")


def test_receipt_fixture_schema_rejects_malformed_objects() -> None:
    valid_receipt = {
        "protocol": {
            "name": "planning-state-transition-receipt",
            "version": 1,
        },
        "root": "docs/plans",
        "transition": "select-batch",
        "status": "rejected",
        "messages": [
            {
                "severity": "error",
                "code": "missing_runway",
                "message": "runway path is missing",
                "source_path": None,
            }
        ],
    }

    assert validate_receipt_fixture_object(valid_receipt) == valid_receipt
    malformed_receipt = {**valid_receipt, "messages": [{"severity": "error"}]}
    try:
        validate_receipt_fixture_object(malformed_receipt)
    except ProtocolValidationError as error:
        assert "code must be a non-empty string" in str(error)
    else:
        raise AssertionError("expected malformed receipt fixture to fail")


def test_state_fixture_schema_accepts_first_class_obligations() -> None:
    valid_state = {
        "protocol": {
            "name": "planning-state-tool-state",
            "version": 1,
        },
        "root": "docs/plans",
        "programs": [
            {
                "slug": "planning-state-tooling",
                "current": "docs/plans/programs/planning-state-tooling/CURRENT.md",
                "ledger": "docs/plans/programs/planning-state-tooling/LEDGER.md",
                "selected_dispatch": None,
                "active_runway": None,
                "queued_batch": None,
                "latest_closeout": None,
                "artifacts": [
                    {
                        "batch_id": "planning-state-write-transitions",
                        "path": (
                            "docs/plans/programs/planning-state-tooling/batches/"
                            "planning-state-write-transitions/runway.md"
                        ),
                        "type": "runway",
                    }
                ],
            }
        ],
        "obligations": [
            {
                "id": "PST-OBL-001",
                "owner": "next-closeout-slice",
                "source_batch": "planning-state-write-transitions",
                "target_batch": None,
                "close_condition": "closeout records bounded evidence",
                "status": "open",
                "evidence_path": None,
            }
        ],
    }

    assert validate_state_fixture_object(valid_state) == valid_state
    malformed_state = {
        **valid_state,
        "obligations": [{**valid_state["obligations"][0], "status": "pending"}],
    }
    try:
        validate_state_fixture_object(malformed_state)
    except ProtocolValidationError as error:
        assert "status must be 'open' or 'closed'" in str(error)
    else:
        raise AssertionError("expected malformed obligation to fail")


def test_validate_state_file_reports_obligation_statuses_and_blockers(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    _write_transition_batch(root)
    state_file = tmp_path / "state.json"
    _write_state_fixture(
        state_file,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": (
                    "docs/plans/programs/planning-state-tooling/batches/"
                    "planning-state-write-transitions/runway.md"
                ),
                "type": "runway",
            }
        ],
        obligations=[
            {
                "id": "PST-OBL-001",
                "owner": "next-closeout-slice",
                "source_batch": "planning-state-write-transitions",
                "target_batch": None,
                "close_condition": "closeout records bounded evidence",
                "status": "open",
                "evidence_path": None,
            },
            {
                "id": "PST-OBL-002",
                "owner": "runner-interop",
                "source_batch": "planning-state-write-transitions",
                "target_batch": "planning-state-closeout-contract",
                "close_condition": None,
                "status": "closed",
                "evidence_path": (
                    "docs/plans/programs/planning-state-tooling/notes/"
                    "runner-interop-obligation.md"
                ),
            },
            {
                "id": "PST-OBL-002",
                "owner": None,
                "source_batch": "missing-batch",
                "target_batch": None,
                "close_condition": None,
                "status": "closed",
                "evidence_path": None,
            },
        ],
    )

    text_result = _run_validate(root, "--state-file", str(state_file))
    json_result = _run_validate_json(root, "--state-file", str(state_file))
    payload = json.loads(json_result.stdout)

    assert text_result.returncode == 1
    assert "open: PST-OBL-001" in text_result.stdout
    assert "closed: PST-OBL-002" in text_result.stdout
    assert json_result.returncode == 1
    assert [obligation["id"] for obligation in payload["obligations"]] == [
        "PST-OBL-001",
        "PST-OBL-002",
        "PST-OBL-002",
    ]
    assert {message["code"] for message in payload["validation_messages"]} >= {
        "open_obligation",
        "closed_obligation",
        "duplicate_obligation_id",
        "missing_obligation_owner",
        "missing_obligation_close_condition",
        "missing_obligation_evidence",
        "orphaned_obligation",
    }


def test_closeout_evidence_index_accepts_bounded_registered_evidence() -> None:
    state_fixture = _closeout_state_fixture()
    closeout = _closeout_evidence_index()

    assert validate_closeout_evidence_index_object(
        closeout,
        state_fixture=state_fixture,
    ) == closeout
    assert closeout["artifacts"] == [
        {
            "batch_id": "planning-state-write-transitions",
            "path": (
                "docs/plans/programs/planning-state-tooling/batches/"
                "planning-state-write-transitions/closeout.md"
            ),
            "type": "closeout",
        },
        {
            "batch_id": "planning-state-write-transitions",
            "path": (
                "docs/plans/programs/planning-state-tooling/batches/"
                "planning-state-write-transitions/completed-slices.md"
            ),
            "type": "completed-slices",
        },
        {
            "batch_id": "planning-state-write-transitions",
            "path": (
                "docs/plans/programs/planning-state-tooling/batches/"
                "planning-state-write-transitions/dispatch.md"
            ),
            "type": "dispatch",
        },
        {
            "batch_id": "planning-state-write-transitions",
            "path": (
                "docs/plans/programs/planning-state-tooling/batches/"
                "planning-state-write-transitions/runway.md"
            ),
            "type": "runway",
        },
    ]
    assert closeout["obligations"]["closed"][0]["status"] == "closed"
    assert closeout["obligations"]["open"][0]["status"] == "open"
    assert closeout["obligations"]["open"][0]["target_batch"] == "next-batch"


def test_closeout_evidence_index_rejects_missing_required_pointers() -> None:
    closeout = _closeout_evidence_index()
    closeout["artifacts"] = [
        artifact
        for artifact in closeout["artifacts"]
        if artifact["type"] != "completed-slices"
    ]

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "missing required pointers: completed-slices" in str(error)
    else:
        raise AssertionError("expected missing completed-slices pointer to fail")


def test_closeout_evidence_index_rejects_unknown_batch_ids() -> None:
    closeout = _closeout_evidence_index(batch_id="unknown-batch")

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "unknown closeout batch_id: unknown-batch" in str(error)
    else:
        raise AssertionError("expected unknown closeout batch to fail")


def test_closeout_evidence_index_rejects_mismatched_fixture_root() -> None:
    closeout = _closeout_evidence_index()
    closeout["root"] = "my-docs/plans"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "closeout root must match state fixture root 'docs/plans'" in str(error)
    else:
        raise AssertionError("expected mismatched fixture root to fail")


def test_closeout_evidence_index_rejects_unknown_fixture_program() -> None:
    closeout = _closeout_evidence_index()
    closeout["program"] = "unknown-program"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "unknown closeout program: unknown-program" in str(error)
    else:
        raise AssertionError("expected unknown fixture program to fail")


def test_closeout_evidence_index_rejects_mismatched_fixture_program() -> None:
    closeout = _closeout_evidence_index()
    closeout["program"] = "architecture-program-runner"
    state_fixture = _closeout_state_fixture()
    state_fixture["programs"].append(
        {
            "slug": "architecture-program-runner",
            "current": "docs/plans/programs/architecture-program-runner/CURRENT.md",
            "ledger": "docs/plans/programs/architecture-program-runner/LEDGER.md",
            "selected_dispatch": None,
            "active_runway": None,
            "queued_batch": None,
            "latest_closeout": None,
            "artifacts": [],
        }
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=state_fixture,
        )
    except ProtocolValidationError as error:
        assert (
            "closeout program 'architecture-program-runner' does not own batch_id "
            "'planning-state-write-transitions'"
        ) in str(error)
    else:
        raise AssertionError("expected mismatched fixture program to fail")


def test_closeout_evidence_index_rejects_cross_program_same_batch_artifacts() -> None:
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    closeout_artifact = closeout["artifacts"][0]
    planning_program = state_fixture["programs"][0]
    planning_program["artifacts"] = [
        artifact
        for artifact in planning_program["artifacts"]
        if artifact != closeout_artifact
    ]
    state_fixture["programs"].append(
        {
            "slug": "architecture-program-runner",
            "current": "docs/plans/programs/architecture-program-runner/CURRENT.md",
            "ledger": "docs/plans/programs/architecture-program-runner/LEDGER.md",
            "selected_dispatch": None,
            "active_runway": None,
            "queued_batch": None,
            "latest_closeout": None,
            "artifacts": [closeout_artifact],
        }
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=state_fixture,
        )
    except ProtocolValidationError as error:
        assert "artifacts[0] must reference a registered artifact" in str(error)
    else:
        raise AssertionError("expected cross-program artifact pointer to fail")


def test_closeout_evidence_index_rejects_multiline_top_level_artifact_path() -> None:
    closeout = _closeout_evidence_index()
    closeout["artifacts"][0]["path"] = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions/closeout.md\npytest output"
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "artifacts[0].path is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected multiline artifact path to fail")


def test_closeout_evidence_index_rejects_oversized_top_level_artifact_path() -> None:
    closeout = _closeout_evidence_index()
    closeout["artifacts"][0]["path"] = "x" * (CLOSEOUT_MAX_ARTIFACT_PATH_CHARS + 1)

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "artifacts[0].path exceeds bounded artifact path limit" in str(error)
    else:
        raise AssertionError("expected oversized artifact path to fail")


def test_closeout_evidence_index_rejects_multiline_evidence_artifact_path() -> None:
    closeout = _closeout_evidence_index()
    closeout["validation_evidence"][0]["artifact"]["path"] = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions/outputs/pytest.json\nraw output"
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "validation_evidence[0].artifact.path is transcript-like" in str(error)
    else:
        raise AssertionError("expected multiline evidence artifact path to fail")


def test_closeout_evidence_index_rejects_oversized_evidence_artifact_path() -> None:
    closeout = _closeout_evidence_index()
    closeout["review_evidence"][0]["artifact"]["path"] = (
        "x" * (CLOSEOUT_MAX_ARTIFACT_PATH_CHARS + 1)
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "review_evidence[0].artifact.path exceeds bounded artifact path limit" in str(
            error
        )
    else:
        raise AssertionError("expected oversized evidence artifact path to fail")


def test_closeout_evidence_index_rejects_fixture_registered_bad_artifact_path() -> None:
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    bad_path = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions/closeout.md\ncommand transcript"
    )
    closeout["artifacts"][0]["path"] = bad_path
    state_fixture["programs"][0]["artifacts"][0]["path"] = bad_path

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=state_fixture,
        )
    except ProtocolValidationError as error:
        assert "artifacts[0].path is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected fixture-backed bad artifact path to fail")


def test_closeout_evidence_index_rejects_fixture_registered_oversized_artifact_path() -> None:
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    bad_path = "x" * (CLOSEOUT_MAX_ARTIFACT_PATH_CHARS + 1)
    closeout["validation_evidence"][0]["artifact"]["path"] = bad_path
    state_fixture["programs"][0]["artifacts"][3]["path"] = bad_path

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=state_fixture,
        )
    except ProtocolValidationError as error:
        assert "validation_evidence[0].artifact.path exceeds bounded artifact path limit" in str(
            error
        )
    else:
        raise AssertionError("expected fixture-backed oversized artifact path to fail")


def test_closeout_evidence_index_rejects_oversized_commit_arrays() -> None:
    closeout = _closeout_evidence_index()
    closeout["commit_evidence"]["commits"] = [
        f"{index:07x}" for index in range(CLOSEOUT_MAX_COMMITS + 1)
    ]

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "commit_evidence.commits exceeds bounded evidence item limit" in str(
            error
        )
    else:
        raise AssertionError("expected oversized commit array to fail")


def test_closeout_evidence_index_rejects_multiline_commit_evidence() -> None:
    closeout = _closeout_evidence_index()
    closeout["commit_evidence"]["commits"][0] = "abc1234\npytest output"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "commit_evidence.commits[0] is transcript-like or unbounded" in str(
            error
        )
    else:
        raise AssertionError("expected multiline commit evidence to fail")


def test_closeout_evidence_index_rejects_overlong_commit_hashes() -> None:
    closeout = _closeout_evidence_index()
    closeout["commit_evidence"]["commits"][0] = (
        "a" * (CLOSEOUT_MAX_COMMIT_REF_CHARS + 1)
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "commit_evidence.commits[0] exceeds bounded evidence limit" in str(error)
    else:
        raise AssertionError("expected overlong commit hash to fail")


def test_closeout_evidence_index_rejects_transcript_like_commit_range() -> None:
    closeout = _closeout_evidence_index()
    closeout["commit_evidence"] = {
        "range": {
            "from": "abc1234",
            "to": "raw log copied into commit range",
        }
    }

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "commit_evidence.range.to is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected transcript-like commit range to fail")


def test_closeout_evidence_index_rejects_overlong_commit_range() -> None:
    closeout = _closeout_evidence_index()
    closeout["commit_evidence"] = {
        "range": {
            "from": "abc1234",
            "to": "a" * (CLOSEOUT_MAX_COMMIT_REF_CHARS + 1),
        }
    }

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "commit_evidence.range.to exceeds bounded evidence limit" in str(error)
    else:
        raise AssertionError("expected overlong commit range to fail")


def test_closeout_evidence_index_rejects_non_fixture_obligations() -> None:
    closeout = _closeout_evidence_index()
    closeout["obligations"]["closed"][0] = {
        **closeout["obligations"]["closed"][0],
        "id": "PST-OBL-FABRICATED",
    }

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "obligations.closed[0] must match a state fixture obligation" in str(error)
    else:
        raise AssertionError("expected non-fixture obligation to fail")


def test_closeout_evidence_index_rejects_closed_obligation_without_evidence() -> None:
    closeout = _closeout_evidence_index()
    closeout["obligations"]["closed"][0]["evidence_path"] = None

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "obligations.closed[0].evidence_path must be a non-empty string" in str(
            error
        )
    else:
        raise AssertionError("expected closed obligation without evidence to fail")


def test_closeout_evidence_index_rejects_closed_obligation_in_open_list() -> None:
    closeout = _closeout_evidence_index()
    closeout["obligations"]["open"][0] = dict(closeout["obligations"]["closed"][0])

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "obligations.open[0].status must be 'open'" in str(error)
    else:
        raise AssertionError("expected closed obligation in open list to fail")


def test_closeout_evidence_index_rejects_transcript_like_sections() -> None:
    closeout = _closeout_evidence_index()
    closeout["sections"].append(
        {
            "title": "Command Transcript",
            "items": ["pytest output copied from the terminal"],
        }
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected transcript-like section to fail")


def test_closeout_evidence_index_rejects_non_exact_transcript_like_sections() -> None:
    closeout = _closeout_evidence_index()
    closeout["sections"].append(
        {
            "title": "Command Transcript Excerpt",
            "items": ["pytest output summary"],
        }
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected non-exact transcript-like section to fail")


def test_closeout_evidence_index_rejects_multiline_section_titles() -> None:
    closeout = _closeout_evidence_index()
    closeout["sections"][0]["title"] = "Evidence Index\nRaw Output"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "sections[0].title is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected multiline section title to fail")


def test_closeout_evidence_index_rejects_multiline_section_items() -> None:
    closeout = _closeout_evidence_index()
    closeout["sections"][0]["items"][0] = "validation started\nvalidation passed"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "sections[0].items[0] is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected multiline section item to fail")


def test_closeout_evidence_index_rejects_unbounded_log_sections() -> None:
    closeout = _closeout_evidence_index()
    closeout["sections"].append(
        {
            "title": "Validation Evidence",
            "items": [f"line {index}" for index in range(25)],
        }
    )

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "exceeds bounded evidence limit" in str(error)
    else:
        raise AssertionError("expected unbounded section to fail")


def test_closeout_evidence_index_rejects_oversized_split_log_sections() -> None:
    closeout = _closeout_evidence_index()
    closeout["sections"] = [
        {
            "title": f"Split Log Pointer {index}",
            "items": [f"artifact pointer {index}"],
        }
        for index in range(CLOSEOUT_MAX_SECTIONS + 1)
    ]

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "sections exceeds bounded evidence item limit" in str(error)
    else:
        raise AssertionError("expected oversized split-log sections to fail")


def test_closeout_evidence_index_rejects_oversized_split_log_evidence_arrays() -> None:
    limits = {
        "validation_evidence": CLOSEOUT_MAX_VALIDATION_EVIDENCE_ITEMS,
        "review_evidence": CLOSEOUT_MAX_REVIEW_EVIDENCE_ITEMS,
        "transition_receipts": CLOSEOUT_MAX_TRANSITION_RECEIPTS,
    }
    for key, limit in limits.items():
        closeout = _closeout_evidence_index()
        template = dict(closeout[key][0])
        closeout[key] = [
            {
                "artifact": template["artifact"],
                "summary": f"split log artifact pointer {index}",
            }
            for index in range(limit + 1)
        ]

        try:
            validate_closeout_evidence_index_object(
                closeout,
                state_fixture=_closeout_state_fixture(),
            )
        except ProtocolValidationError as error:
            assert f"{key} exceeds bounded evidence item limit" in str(error)
        else:
            raise AssertionError(f"expected oversized {key} to fail")


def test_closeout_evidence_index_rejects_transcript_like_validation_summary() -> None:
    closeout = _closeout_evidence_index()
    closeout["validation_evidence"][0]["summary"] = "raw log copied into summary"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "validation_evidence[0].summary is transcript-like or unbounded" in str(
            error
        )
    else:
        raise AssertionError("expected transcript-like validation summary to fail")


def test_closeout_evidence_index_rejects_multiline_review_summary() -> None:
    closeout = _closeout_evidence_index()
    closeout["review_evidence"][0]["summary"] = "review started\nreview passed"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "review_evidence[0].summary is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected multiline review summary to fail")


def test_closeout_evidence_index_rejects_long_transition_receipt_summary() -> None:
    closeout = _closeout_evidence_index()
    closeout["transition_receipts"][0]["summary"] = "x" * 1201

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "transition_receipts[0].summary exceeds bounded evidence limit" in str(
            error
        )
    else:
        raise AssertionError("expected long transition receipt summary to fail")


def test_closeout_evidence_index_rejects_transcript_like_cleanup_evidence() -> None:
    closeout = _closeout_evidence_index()
    closeout["cleanup_residue"]["evidence"][0] = "command transcript copied here"

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "cleanup_residue.evidence[0] is transcript-like or unbounded" in str(error)
    else:
        raise AssertionError("expected transcript-like cleanup evidence to fail")


def test_closeout_evidence_index_rejects_oversized_split_log_cleanup_evidence() -> None:
    closeout = _closeout_evidence_index()
    closeout["cleanup_residue"]["evidence"] = [
        f"cleanup residue artifact pointer {index}"
        for index in range(CLOSEOUT_MAX_CLEANUP_RESIDUE_EVIDENCE_ITEMS + 1)
    ]

    try:
        validate_closeout_evidence_index_object(
            closeout,
            state_fixture=_closeout_state_fixture(),
        )
    except ProtocolValidationError as error:
        assert "cleanup_residue.evidence exceeds bounded evidence item limit" in str(
            error
        )
    else:
        raise AssertionError("expected oversized cleanup residue evidence to fail")


def test_validate_closeout_command_accepts_registered_fixture(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["protocol"] == {
        "command": "validate-closeout",
        "name": "planning-state-closeout-validation",
        "version": 1,
    }
    assert payload["status"] == "passed"
    assert payload["blockers"] == []


def test_validate_closeout_command_reports_stable_blockers(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    closeout["artifacts"] = [
        artifact
        for artifact in closeout["artifacts"]
        if artifact["type"] != "completed-slices"
    ]
    closeout["validation_evidence"] = []
    closeout["review_evidence"] = []
    closeout["obligations"]["closed"][0]["evidence_path"] = None
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["status"] == "failed"
    assert {blocker["code"] for blocker in payload["blockers"]} == {
        "missing_completed_slices_pointer",
        "missing_validation_evidence",
        "missing_review_evidence",
        "missing_closed_obligation_evidence",
    }


def test_validate_closeout_command_rejects_unregistered_closeout(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    state_fixture = _closeout_state_fixture()
    state_fixture["programs"][0]["artifacts"] = [
        artifact
        for artifact in state_fixture["programs"][0]["artifacts"]
        if artifact["type"] != "closeout"
    ]
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "unregistered_closeout"
    ]


def test_validate_closeout_command_rejects_batch_and_path_mismatch(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    closeout["batch_id"] = "planning-state-readonly-core"
    closeout["artifacts"][0]["path"] = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-readonly-core/closeout.md"
    )
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert {blocker["code"] for blocker in payload["blockers"]} == {
        "closeout_batch_mismatch",
        "closeout_path_mismatch",
        "invalid_closeout_contract",
    }


def test_validate_closeout_command_rejects_existing_absolute_path_without_reading(
    tmp_path: Path,
) -> None:
    root, state_file, _closeout_path = _write_closeout_validation_fixture(tmp_path)
    outside_closeout = tmp_path / "outside-closeout.md"
    outside_closeout.write_text("not json\n", encoding="utf-8")

    result = _run_validate_closeout(root, state_file, str(outside_closeout))
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert payload["status"] == "failed"
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "invalid_closeout_path"
    ]


def test_validate_closeout_command_rejects_canonical_directory_without_traceback(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout_file = root / Path(closeout_path).relative_to("docs/plans")
    closeout_file.unlink()
    closeout_file.mkdir()

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert payload["status"] == "failed"
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "non_file_closeout"
    ]


def test_validate_closeout_command_rejects_registered_wrong_batch_required_artifact(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    bad_path = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "other-batch/completed-slices.md"
    )
    closeout["artifacts"][1]["path"] = bad_path
    _replace_registered_artifact_path(
        state_fixture,
        "completed-slices",
        bad_path,
    )
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["status"] == "failed"
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "invalid_closeout_contract"
    ]
    assert "completed-slices must be co-located at" in payload["blockers"][0]["message"]


def test_validate_closeout_command_rejects_registered_out_of_root_validation_artifact(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    bad_path = "tmp/pytest.json"
    closeout["validation_evidence"][0]["artifact"]["path"] = bad_path
    _replace_registered_artifact_path(state_fixture, "output", bad_path)
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "invalid_closeout_contract"
    ]
    assert "artifact path must be under the planning root" in payload["blockers"][0]["message"]


def test_validate_closeout_command_rejects_registered_absolute_review_artifact(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    bad_path = str(tmp_path / "review-receipt.json")
    bad_artifact = dict(closeout["review_evidence"][0]["artifact"])
    bad_artifact["path"] = bad_path
    closeout["review_evidence"][0]["artifact"] = bad_artifact
    _replace_registered_artifact_path(state_fixture, "receipt", bad_path)
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "invalid_closeout_contract"
    ]
    assert "artifact path must be relative to the workspace" in payload["blockers"][0]["message"]


def test_validate_closeout_command_checks_present_artifact_paths_with_preflight_blockers(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    bad_artifact = dict(closeout["review_evidence"][0]["artifact"])
    bad_artifact["path"] = str(tmp_path / "review-receipt.json")
    closeout["review_evidence"][0]["artifact"] = bad_artifact
    closeout["validation_evidence"] = []
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    blocker_codes = [blocker["code"] for blocker in payload["blockers"]]
    assert "missing_validation_evidence" in blocker_codes
    assert "invalid_closeout_contract" in blocker_codes
    assert any(
        "artifact path must be relative to the workspace" in blocker["message"]
        for blocker in payload["blockers"]
    )


def test_validate_closeout_command_checks_artifact_paths_when_closeout_unregistered(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    state_fixture = _closeout_state_fixture()
    state_fixture["programs"][0]["artifacts"] = [
        artifact
        for artifact in state_fixture["programs"][0]["artifacts"]
        if artifact["type"] != "closeout"
    ]
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")
    closeout = _closeout_evidence_index()
    bad_artifact = dict(closeout["review_evidence"][0]["artifact"])
    bad_artifact["path"] = str(tmp_path / "review-receipt.json")
    closeout["review_evidence"][0]["artifact"] = bad_artifact
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    blocker_codes = [blocker["code"] for blocker in payload["blockers"]]
    assert "unregistered_closeout" in blocker_codes
    assert "invalid_closeout_contract" in blocker_codes
    assert any(
        "artifact path must be relative to the workspace" in blocker["message"]
        for blocker in payload["blockers"]
    )


def test_validate_closeout_command_collects_multiple_invalid_artifact_pointers(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    closeout["artifacts"][1]["path"] = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "other-batch/completed-slices.md"
    )
    closeout["validation_evidence"][0]["artifact"]["path"] = "tmp/pytest.json"
    bad_review_artifact = dict(closeout["review_evidence"][0]["artifact"])
    bad_review_artifact["path"] = str(tmp_path / "review-receipt.json")
    closeout["review_evidence"][0]["artifact"] = bad_review_artifact
    bad_transition_artifact = dict(closeout["transition_receipts"][0]["artifact"])
    bad_transition_artifact["path"] = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "other-batch/receipts/queue-batch.json"
    )
    closeout["transition_receipts"][0]["artifact"] = bad_transition_artifact
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    invalid_contract_messages = [
        blocker["message"]
        for blocker in payload["blockers"]
        if blocker["code"] == "invalid_closeout_contract"
    ]
    assert len(invalid_contract_messages) == 4
    assert any(
        "completed-slices must be co-located at" in message
        for message in invalid_contract_messages
    )
    assert any(
        "artifact path must be under the planning root" in message
        for message in invalid_contract_messages
    )
    assert any(
        "artifact path must be relative to the workspace" in message
        for message in invalid_contract_messages
    )
    assert any(
        "artifact path must be co-located with the batch" in message
        for message in invalid_contract_messages
    )


def test_render_closeout_command_outputs_stable_pointer_first_markdown(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)

    result = _run_render_closeout(root, state_file)
    closeout = _json_from_markdown(result.stdout)

    assert result.returncode == 0
    assert result.stdout.startswith("# Closeout: planning-state-write-transitions\n")
    assert "pytest output copied from the terminal" not in result.stdout
    assert closeout["artifacts"][0] == {
        "batch_id": "planning-state-write-transitions",
        "path": closeout_path,
        "type": "closeout",
    }
    assert closeout["sections"] == [
        {
            "items": ["completed-slices.md summarizes all completed slices"],
            "title": "Completed Slices",
        }
    ]
    assert closeout["validation_evidence"][0]["artifact"]["path"].endswith(
        "/outputs/pytest.json"
    )
    assert closeout["review_evidence"][0]["artifact"]["path"].endswith(
        "/receipts/queue-batch.json"
    )


def test_render_closeout_command_writes_only_registered_closeout_path(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    target = root / Path(closeout_path).relative_to("docs/plans")
    target.unlink()

    result = _run_render_closeout(root, state_file, "--target", closeout_path)
    validate_result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["status"] == "rendered"
    assert payload["target"] == closeout_path
    assert target.exists()
    assert validate_result.returncode == 0
    assert json.loads(validate_result.stdout)["status"] == "passed"


def test_render_closeout_command_rejects_unregistered_target_path(
    tmp_path: Path,
) -> None:
    root, state_file, _closeout_path = _write_closeout_validation_fixture(tmp_path)
    bad_target = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions/outputs/closeout.md"
    )

    result = _run_render_closeout(root, state_file, "--target", bad_target)

    assert result.returncode == 2
    assert "target path must be registered closeout path" in result.stderr


def test_render_closeout_command_rejects_missing_closed_obligation_evidence(
    tmp_path: Path,
) -> None:
    root, state_file, _closeout_path = _write_closeout_validation_fixture(tmp_path)
    state_fixture = _closeout_state_fixture()
    state_fixture["obligations"][0]["evidence_path"] = None
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")

    result = _run_render_closeout(root, state_file)

    assert result.returncode == 2
    assert "obligations.closed[0].evidence_path must be a non-empty string" in (
        result.stderr
    )


def test_validate_closeout_command_rejects_registered_wrong_batch_transition_receipt(
    tmp_path: Path,
) -> None:
    root, state_file, closeout_path = _write_closeout_validation_fixture(tmp_path)
    closeout = _closeout_evidence_index()
    state_fixture = _closeout_state_fixture()
    bad_path = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "other-batch/receipts/queue-batch.json"
    )
    bad_artifact = dict(closeout["transition_receipts"][0]["artifact"])
    bad_artifact["path"] = bad_path
    closeout["transition_receipts"][0]["artifact"] = bad_artifact
    state_fixture["programs"][0]["artifacts"].append(
        {
            "batch_id": "planning-state-write-transitions",
            "path": bad_path,
            "type": "receipt",
        }
    )
    state_file.write_text(json.dumps(state_fixture), encoding="utf-8")
    _write_closeout_file(root, closeout_path, closeout)

    result = _run_validate_closeout(root, state_file, closeout_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert [blocker["code"] for blocker in payload["blockers"]] == [
        "invalid_closeout_contract"
    ]
    assert "artifact path must be co-located with the batch" in payload["blockers"][0]["message"]


def test_validate_rejects_state_file_from_different_planning_root(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    state_file = tmp_path / "foreign-state.json"
    _write_state_fixture(state_file, root_value="my-docs/plans")

    result = _run_validate(root, "--state-file", str(state_file))

    assert result.returncode == 2
    assert "state-file root does not match planning root" in result.stderr
    assert "my-docs/plans != docs/plans" in result.stderr


def test_allocate_batch_command_reports_canonical_layout_v1_paths(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    result = subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "allocate-batch",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-write-transitions",
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["batch_directory"] == (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions"
    )
    assert payload["artifacts"] == {
        "closeout": (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/closeout.md"
        ),
        "completed-slices": (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/completed-slices.md"
        ),
        "dispatch": (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/dispatch.md"
        ),
        "runway": (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/runway.md"
        ),
    }


def test_allocate_batch_command_rejects_existing_batch_directory(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    result = subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "allocate-batch",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-readonly-core",
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "batch directory already exists:" in result.stderr


def test_allocate_batch_command_rejects_malformed_planning_roots(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    (root / "CURRENT.md").write_text(
        (root / "CURRENT.md")
        .read_text(encoding="utf-8")
        .replace("Planning root: `docs/plans/`", "Planning root: `/tmp/plans/`"),
        encoding="utf-8",
    )
    absolute = _run_allocate_batch(root, "planning-state-tooling")
    (root / "CURRENT.md").write_text(
        (root / "CURRENT.md")
        .read_text(encoding="utf-8")
        .replace("Planning root: `/tmp/plans/`", "Planning root: `docs/../plans/`"),
        encoding="utf-8",
    )
    escaped = _run_allocate_batch(root, "planning-state-tooling")

    assert absolute.returncode == 2
    assert "planning root must be relative" in absolute.stderr
    assert escaped.returncode == 2
    assert "planning root must not contain dot segments" in escaped.stderr


def test_allocate_batch_command_rejects_malformed_program_slugs(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    current = root / "programs" / "planning-state-tooling" / "CURRENT.md"
    current.write_text(
        current.read_text(encoding="utf-8").replace(
            "Program slug: `planning-state-tooling`",
            "Program slug: `planning/state-tooling`",
        ),
        encoding="utf-8",
    )

    result = _run_allocate_batch(root, "planning/state-tooling")

    assert result.returncode == 2
    assert "program slug must be a single path segment" in result.stderr


def test_register_artifact_dry_run_is_usable_without_state_file(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    result = _run_register_artifact(
        root,
        "dispatch",
        (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/dispatch.md"
        ),
        "--dry-run",
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["status"] == "dry-run"
    assert payload["artifact"] == {
        "batch_id": "planning-state-write-transitions",
        "path": (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/dispatch.md"
        ),
        "type": "dispatch",
    }


def test_register_artifact_dry_run_supports_all_artifact_types(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    batch_root = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions"
    )
    paths = {
        "closeout": f"{batch_root}/closeout.md",
        "completed-slices": f"{batch_root}/completed-slices.md",
        "dispatch": f"{batch_root}/dispatch.md",
        "output": f"{batch_root}/outputs/summary.json",
        "receipt": f"{batch_root}/receipts/receipt.json",
        "runway": f"{batch_root}/runway.md",
    }

    results = {
        artifact_type: _run_register_artifact(root, artifact_type, path)
        for artifact_type, path in paths.items()
    }

    assert {artifact_type: result.returncode for artifact_type, result in results.items()} == {
        "closeout": 0,
        "completed-slices": 0,
        "dispatch": 0,
        "output": 0,
        "receipt": 0,
        "runway": 0,
    }
    assert {
        artifact_type: json.loads(result.stdout)["artifact"]["path"]
        for artifact_type, result in results.items()
    } == paths


def test_register_artifact_updates_explicit_state_fixture(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    state_file = tmp_path / "state.json"
    _write_state_fixture(state_file)

    result = _run_register_artifact(
        root,
        "runway",
        (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/runway.md"
        ),
        "--state-file",
        str(state_file),
    )
    payload = json.loads(result.stdout)
    state = json.loads(state_file.read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert payload["status"] == "registered"
    assert state["programs"][0]["artifacts"] == [
        {
            "batch_id": "planning-state-write-transitions",
            "path": (
                "docs/plans/programs/planning-state-tooling/batches/"
                "planning-state-write-transitions/runway.md"
            ),
            "type": "runway",
        }
    ]


def test_register_artifact_rejects_missing_program_root(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    result = subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "register-artifact",
            "--root",
            str(root),
            "--program",
            "missing-program",
            "--batch-id",
            "planning-state-write-transitions",
            "--type",
            "dispatch",
            "--path",
            (
                "docs/plans/programs/missing-program/batches/"
                "planning-state-write-transitions/dispatch.md"
            ),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "program root is missing: missing-program" in result.stderr


def test_register_artifact_rejects_collisions(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    state_file = tmp_path / "state.json"
    _write_state_fixture(
        state_file,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": (
                    "docs/plans/programs/planning-state-tooling/batches/"
                    "planning-state-write-transitions/dispatch.md"
                ),
                "type": "dispatch",
            }
        ],
    )

    result = _run_register_artifact(
        root,
        "dispatch",
        (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/dispatch.md"
        ),
        "--state-file",
        str(state_file),
    )

    assert result.returncode == 2
    assert "artifact is already registered" in result.stderr


def test_register_artifact_rejects_unsupported_type_and_unsafe_paths(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    unsupported = _run_register_artifact(
        root,
        "summary",
        (
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-write-transitions/summary.md"
        ),
    )
    outside_root = _run_register_artifact(
        root,
        "dispatch",
        "tmp/dispatch.md",
    )
    escaped = _run_register_artifact(
        root,
        "dispatch",
        "docs/plans/../dispatch.md",
    )
    absolute = _run_register_artifact(
        root,
        "dispatch",
        str(tmp_path / "dispatch.md"),
    )
    wrong_batch_dir = _run_register_artifact(
        root,
        "dispatch",
        (
            "docs/plans/programs/planning-state-tooling/batches/"
            "other-batch/dispatch.md"
        ),
    )

    assert unsupported.returncode == 2
    assert "unsupported artifact type: summary" in unsupported.stderr
    assert outside_root.returncode == 2
    assert "artifact path must be under the planning root" in outside_root.stderr
    assert escaped.returncode == 2
    assert "artifact path must not escape the planning root" in escaped.stderr
    assert absolute.returncode == 2
    assert "artifact path must be relative to the workspace" in absolute.stderr
    assert wrong_batch_dir.returncode == 2
    assert "dispatch must be co-located at" in wrong_batch_dir.stderr


def test_select_batch_updates_explicit_state_and_writes_receipt(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root)
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "select-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    _write_state_fixture(
        state_file,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            }
        ],
    )

    result = _run_select_batch(root, state_file, receipt_file)
    payload = json.loads(result.stdout)
    state = json.loads(state_file.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert payload["status"] == "applied"
    assert payload["transition"] == "select-batch"
    assert payload["program"] == "planning-state-tooling"
    assert payload["batch_id"] == "planning-state-write-transitions"
    assert payload["artifacts"] == [
        {
            "batch_id": "planning-state-write-transitions",
            "path": dispatch,
            "type": "dispatch",
        }
    ]
    assert payload["warnings"] == []
    assert payload["blockers"] == []
    assert state["programs"][0]["selected_dispatch"] == dispatch
    assert receipt == payload


def test_select_batch_rejects_active_conflicts_before_state_mutation(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root)
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "select-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    _write_state_fixture(
        state_file,
        selected_dispatch="docs/plans/programs/planning-state-tooling/batches/old/dispatch.md",
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            }
        ],
    )

    result = _run_select_batch(root, state_file, receipt_file)
    state = json.loads(state_file.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert state["programs"][0]["selected_dispatch"] == (
        "docs/plans/programs/planning-state-tooling/batches/old/dispatch.md"
    )
    assert receipt["status"] == "rejected"
    assert [blocker["code"] for blocker in receipt["blockers"]] == [
        "fixture_active_state_conflict"
    ]


def test_queue_batch_requires_selected_registered_dispatch_and_runway(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root)
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "queue-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    runway = f"{batch_root}/runway.md"
    _write_state_fixture(
        state_file,
        selected_dispatch=dispatch,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            },
            {
                "batch_id": "planning-state-write-transitions",
                "path": runway,
                "type": "runway",
            },
        ],
    )

    result = _run_queue_batch(root, state_file, receipt_file)
    state = json.loads(state_file.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert receipt["status"] == "applied"
    assert receipt["transition"] == "queue-batch"
    assert state["programs"][0]["selected_dispatch"] is None
    assert state["programs"][0]["queued_batch"] == runway


def test_queue_batch_receipt_includes_runner_consumable_obligations(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root)
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "queue-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    runway = f"{batch_root}/runway.md"
    _write_state_fixture(
        state_file,
        selected_dispatch=dispatch,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            },
            {
                "batch_id": "planning-state-write-transitions",
                "path": runway,
                "type": "runway",
            },
        ],
        obligations=[
            {
                "id": "PST-OBL-QUEUE-001",
                "owner": "closeout-slice",
                "source_batch": "planning-state-write-transitions",
                "target_batch": None,
                "close_condition": "closeout evidence index records receipt path",
                "status": "open",
                "evidence_path": None,
            }
        ],
    )

    result = _run_queue_batch(root, state_file, receipt_file)
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 0
    assert receipt["status"] == "applied"
    assert receipt["obligations"] == [
        {
            "close_condition": "closeout evidence index records receipt path",
            "evidence_path": None,
            "id": "PST-OBL-QUEUE-001",
            "owner": "closeout-slice",
            "source_batch": "planning-state-write-transitions",
            "status": "open",
            "target_batch": None,
        }
    ]
    assert {
        "protocol",
        "root",
        "transition",
        "status",
        "program",
        "batch_id",
        "artifacts",
        "obligations",
        "warnings",
        "blockers",
        "messages",
    } <= receipt.keys()


def test_queue_batch_rejects_foreign_state_file_before_mutation(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root)
    state_file = tmp_path / "foreign-state.json"
    receipt_file = tmp_path / "queue-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    runway = f"{batch_root}/runway.md"
    _write_state_fixture(
        state_file,
        root_value="foreign/plans",
        selected_dispatch=dispatch,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            },
            {
                "batch_id": "planning-state-write-transitions",
                "path": runway,
                "type": "runway",
            },
        ],
        obligations=[
            {
                "id": "FOREIGN-OBL-001",
                "owner": "foreign-runner",
                "source_batch": "planning-state-write-transitions",
                "target_batch": None,
                "close_condition": "foreign closeout",
                "status": "open",
                "evidence_path": None,
            }
        ],
    )
    before = state_file.read_text(encoding="utf-8")

    result = _run_queue_batch(root, state_file, receipt_file)

    assert result.returncode == 2
    assert "state-file root does not match planning root" in result.stderr
    assert state_file.read_text(encoding="utf-8") == before
    assert not receipt_file.exists()


def test_queue_batch_rejects_bypass_missing_and_stale_selected_dispatches(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root, write_runway=False)
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "queue-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    _write_state_fixture(
        state_file,
        selected_dispatch="docs/plans/programs/planning-state-tooling/batches/old/dispatch.md",
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            }
        ],
    )

    result = _run_queue_batch(root, state_file, receipt_file)
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert {blocker["code"] for blocker in receipt["blockers"]} == {
        "missing_runway",
        "stale_selected_dispatch",
        "unregistered_runway",
    }


def test_transition_commands_reject_cross_program_paths_and_unknown_ledger_rows(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    wrong_dispatch = (
        "docs/plans/programs/architecture-program-runner/batches/"
        "planning-state-write-transitions/dispatch.md"
    )
    _write_transition_batch(
        root,
        program="architecture-program-runner",
    )
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "select-receipt.json"
    _write_state_fixture(
        state_file,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": wrong_dispatch,
                "type": "dispatch",
            }
        ],
    )
    (root / "programs" / "planning-state-tooling" / "LEDGER.md").write_text(
        """# Ledger

| Batch | Status |
|---|---|
| `docs/plans/programs/planning-state-tooling/batches/other-batch/runway.md` | Pending |
""",
        encoding="utf-8",
    )

    result = _run_select_batch(
        root,
        state_file,
        receipt_file,
        dispatch=wrong_dispatch,
    )
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert {blocker["code"] for blocker in receipt["blockers"]} == {
        "invalid_artifact_path",
        "unknown_ledger_batch",
    }


def test_transition_ledger_validation_rejects_similarly_named_batches(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="None",
        latest="None",
    )
    batch_root = _write_transition_batch(root)
    state_file = tmp_path / "state.json"
    receipt_file = tmp_path / "select-receipt.json"
    dispatch = f"{batch_root}/dispatch.md"
    _write_state_fixture(
        state_file,
        artifacts=[
            {
                "batch_id": "planning-state-write-transitions",
                "path": dispatch,
                "type": "dispatch",
            }
        ],
    )
    (root / "programs" / "planning-state-tooling" / "LEDGER.md").write_text(
        """# Ledger

| Batch | Status |
|---|---|
| `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions-extra/runway.md` | Pending |
""",
        encoding="utf-8",
    )

    result = _run_select_batch(root, state_file, receipt_file)
    receipt = json.loads(receipt_file.read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert [blocker["code"] for blocker in receipt["blockers"]] == [
        "unknown_ledger_batch"
    ]


def test_validate_command_passes_for_current_codex_fixture(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)

    result = _run_validate(root)

    assert result.returncode == 0
    assert "status: passed" in result.stdout
    assert "errors:\n    []" in result.stdout


def test_validate_reports_missing_root_current_as_fatal(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)

    result = _run_validate(root)

    assert result.returncode == 1
    assert "missing_root_current:" in result.stdout


def test_validate_reports_missing_listed_program_current_as_fatal(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)
    _write_root_current(root, "missing-program")

    result = _run_validate(root)

    assert result.returncode == 1
    assert "missing_program_current:" in result.stdout


def test_validate_reports_invalid_selected_dispatch_path_as_fatal(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        selected="docs/plans/programs/planning-state-tooling/batches/missing/dispatch.md",
        queued="None",
        latest="None",
    )

    result = _run_validate(root)

    assert result.returncode == 1
    assert "invalid_selected_dispatch_path:" in result.stdout


def test_validate_reports_invalid_queued_runway_path_as_fatal(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        queued="docs/plans/programs/planning-state-tooling/batches/missing/runway.md",
        latest="None",
    )

    result = _run_validate(root)

    assert result.returncode == 1
    assert "invalid_queued_runway_path:" in result.stdout


def test_validate_reports_markdown_active_state_conflict_without_json_state(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    batch_root = _write_transition_batch(root)
    _write_program_current(
        root,
        "planning-state-tooling",
        selected=f"{batch_root}/dispatch.md",
        queued=f"{batch_root}/runway.md",
        latest="None",
    )

    result = _run_validate(root)

    assert result.returncode == 1
    assert "multiple_active_artifacts:" in result.stdout


def test_validate_reports_redirect_without_target_as_fatal(tmp_path: Path) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)
    (root / "install-sandbox-legacy-removal-ledger.md").write_text(
        "# Redirect: Legacy Removal Ledger\n",
        encoding="utf-8",
    )

    result = _run_validate(root)

    assert result.returncode == 1
    assert "redirect_without_target:" in result.stdout


def test_validate_keeps_stale_pickup_notes_warning_only(tmp_path: Path) -> None:
    root = tmp_path / "my-docs" / "plans"
    _write_graphify_fixture(root)

    result = _run_validate(root)

    assert result.returncode == 0
    assert "status: passed" in result.stdout
    assert "errors:\n    []" in result.stdout
    assert "stale_pickup_note:" in result.stdout
    assert "historical_batch_artifact:" in result.stdout
    assert "2 total" in result.stdout


def test_validation_report_keeps_warnings_nonfatal(tmp_path: Path) -> None:
    root = tmp_path / "docs" / "plans"
    root.mkdir(parents=True)
    (root / "CURRENT.md").write_text(
        """# Planning Current State

- Layout: Legacy Planning Layout
""",
        encoding="utf-8",
    )

    report = format_validation_report(load_planning_state(root))

    assert "status: passed" in report
    assert "errors:\n    []" in report
    assert "unknown_layout:" in report
    assert "no_active_programs:" in report


def _write_codex_config_fixture(root: Path) -> None:
    (root / "programs" / "architecture-program-runner").mkdir(parents=True)
    (root / "programs" / "planning-state-tooling" / "batches" / "planning-state-readonly-core").mkdir(
        parents=True
    )
    (root / "CURRENT.md").write_text(
        """# Planning Current State

## Layout

- Layout: Planning Artifact Layout v1
- Planning root: `docs/plans/`
- Run artifact root: `<program-root>/architecture-program-runs/`
- Output root: `None selected`
- One-shot intake: `None`
- Program archive root: `docs/plans/archive/`

## Active Programs

| Program | Current state |
|---|---|
| `architecture-program-runner` | `docs/plans/programs/architecture-program-runner/CURRENT.md` |
| `planning-state-tooling` | `docs/plans/programs/planning-state-tooling/CURRENT.md` |

## Next Safe Action

Use the relevant program `CURRENT.md` before reading ledgers.
""",
        encoding="utf-8",
    )
    _write_program_current(
        root,
        "architecture-program-runner",
        queued="None",
        latest="None",
    )
    _write_program_current(
        root,
        "planning-state-tooling",
        queued=(
            "docs/plans/programs/planning-state-tooling/batches/"
            "planning-state-readonly-core/runway.md"
        ),
        latest="None",
    )
    (root / "programs" / "architecture-program-runner" / "LEDGER.md").write_text(
        "# Ledger\n",
        encoding="utf-8",
    )
    (root / "programs" / "planning-state-tooling" / "LEDGER.md").write_text(
        "# Ledger\n",
        encoding="utf-8",
    )
    (
        root
        / "programs"
        / "planning-state-tooling"
        / "batches"
        / "planning-state-readonly-core"
        / "runway.md"
    ).write_text("# Runway\n", encoding="utf-8")


def _write_graphify_fixture(root: Path) -> None:
    tqa = "install-sandbox-test-quality-architecture"
    legacy = "install-sandbox-legacy-removal"
    (root / "programs" / tqa / "batches" / "tqa-b11-target-selection-diagnostic-wording").mkdir(
        parents=True
    )
    (root / "programs" / legacy).mkdir(parents=True)
    (root / "dispatch").mkdir()
    (root / "CURRENT.md").write_text(
        """# Planning Current State

Layout: Planning Artifact Layout v1

## Roots

- Deepest local root: `my-docs/`
- Planning root: `my-docs/plans/`
- Run artifact root: `my-docs/runs/`
- Output root: `my-docs/outputs/`
- One-shot intake: `my-docs/plans/intake/`

## Active Programs

| Program | Current file |
| --- | --- |
| `install-sandbox-test-quality-architecture` | `my-docs/plans/programs/install-sandbox-test-quality-architecture/CURRENT.md` |
| `install-sandbox-legacy-removal` | `my-docs/plans/programs/install-sandbox-legacy-removal/CURRENT.md` |

## Migration State

Pickup note:
`my-docs/plans/planning-layout-migration-pickup.md`

Next safe action: select a new batch only from the relevant program `CURRENT.md`.
""",
        encoding="utf-8",
    )
    _write_program_current(
        root,
        tqa,
        queued="None",
        latest=(
            "my-docs/plans/programs/install-sandbox-test-quality-architecture/"
            "batches/tqa-b11-target-selection-diagnostic-wording/runway.md"
        ),
        run_artifact="my-docs/runs/batch-runway/install-sandbox-test-quality-architecture/",
    )
    _write_program_current(
        root,
        legacy,
        queued="None",
        latest="my-docs/plans/install-sandbox-install-target-catalog-concrete-type-runway.md",
        run_artifact="my-docs/runs/batch-runway/install-sandbox-legacy-removal/",
    )
    (root / "programs" / tqa / "LEDGER.md").write_text("# Ledger\n", encoding="utf-8")
    (root / "programs" / legacy / "LEDGER.md").write_text("# Ledger\n", encoding="utf-8")
    (root / "programs" / tqa / "batches" / "tqa-b11-target-selection-diagnostic-wording" / "runway.md").write_text(
        "# Closeout evidence\n",
        encoding="utf-8",
    )
    (root / "planning-layout-migration-pickup.md").write_text("# Pickup\n", encoding="utf-8")
    (root / "install-sandbox-install-target-catalog-concrete-type-runway.md").write_text(
        "# Historical runway\n",
        encoding="utf-8",
    )
    (root / "dispatch" / "install-target-catalog-concrete-type-dispatch.md").write_text(
        "# Historical dispatch\n",
        encoding="utf-8",
    )
    _write_redirect(root, legacy)
    _write_redirect(root, tqa)


def _write_program_current(
    root: Path,
    slug: str,
    *,
    queued: str,
    latest: str,
    selected: str = "None selected",
    run_artifact: str = "None selected",
) -> None:
    (root / "programs" / slug / "CURRENT.md").write_text(
        f"""# {slug} Current State

Program slug: `{slug}`

Purpose: fixture program.

## Active State

- Current ledger:
  `{_display_root(root)}/programs/{slug}/LEDGER.md`
- Selected dispatch path: `{selected}`
- Active Batch Runway spec path: `None selected`
- Queued batch path or ID: `{queued}`
- Latest closeout:
  `{latest}`
- Run artifact location:
  `{run_artifact}`
- Program archive location:
  `{_display_root(root)}/programs/{slug}/archive/`

## Next Safe Action

Use the current ledger only.

## Stop Conditions

- Stop on fixture contradiction.
""",
        encoding="utf-8",
    )


def _write_redirect(root: Path, slug: str) -> None:
    (root / f"{slug}-ledger.md").write_text(
        f"""# Redirect: {slug} Ledger

New path:
`my-docs/plans/programs/{slug}/LEDGER.md`

Program current state:
`my-docs/plans/programs/{slug}/CURRENT.md`
""",
        encoding="utf-8",
    )


def _display_root(root: Path) -> str:
    if root.parent.name == "docs":
        return "docs/plans"
    return "my-docs/plans"


def _run_current(root: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(PLANNING_STATE_SCRIPT), "current", "--root", str(root)],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def _run_current_json(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "current",
            "--root",
            str(root),
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_validate(root: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "validate",
            "--root",
            str(root),
            *extra_args,
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_validate_json(root: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "validate",
            "--root",
            str(root),
            "--format",
            "json",
            *extra_args,
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_allocate_batch(
    root: Path,
    program: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "allocate-batch",
            "--root",
            str(root),
            "--program",
            program,
            "--batch-id",
            "planning-state-write-transitions",
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_register_artifact(
    root: Path,
    artifact_type: str,
    artifact_path: str,
    *extra_args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "register-artifact",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-write-transitions",
            "--type",
            artifact_type,
            "--path",
            artifact_path,
            *extra_args,
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_select_batch(
    root: Path,
    state_file: Path,
    receipt_file: Path,
    *,
    dispatch: str | None = None,
) -> subprocess.CompletedProcess[str]:
    batch_root = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions"
    )
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "select-batch",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-write-transitions",
            "--dispatch",
            dispatch or f"{batch_root}/dispatch.md",
            "--state-file",
            str(state_file),
            "--receipt-file",
            str(receipt_file),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_queue_batch(
    root: Path,
    state_file: Path,
    receipt_file: Path,
) -> subprocess.CompletedProcess[str]:
    batch_root = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions"
    )
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "queue-batch",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-write-transitions",
            "--dispatch",
            f"{batch_root}/dispatch.md",
            "--runway",
            f"{batch_root}/runway.md",
            "--state-file",
            str(state_file),
            "--receipt-file",
            str(receipt_file),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_validate_closeout(
    root: Path,
    state_file: Path,
    closeout_path: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "validate-closeout",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-write-transitions",
            "--closeout",
            closeout_path,
            "--state-file",
            str(state_file),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _run_render_closeout(
    root: Path,
    state_file: Path,
    *extra_args: str,
) -> subprocess.CompletedProcess[str]:
    batch_root = (
        "docs/plans/programs/planning-state-tooling/batches/"
        "planning-state-write-transitions"
    )
    return subprocess.run(
        [
            sys.executable,
            str(PLANNING_STATE_SCRIPT),
            "render-closeout",
            "--root",
            str(root),
            "--program",
            "planning-state-tooling",
            "--batch-id",
            "planning-state-write-transitions",
            "--state-file",
            str(state_file),
            "--completed-slices-summary",
            "completed-slices.md summarizes all completed slices",
            "--validation-artifact",
            f"{batch_root}/outputs/pytest.json",
            "--validation-summary",
            "focused pytest, ruff, and diff checks passed",
            "--review-artifact",
            f"{batch_root}/receipts/queue-batch.json",
            "--review-summary",
            "reviewer marked the slice clean",
            "--cleanup-classification",
            "deferred",
            "--cleanup-evidence",
            "PST-OBL-OPEN remains assigned to next-batch",
            "--commit",
            "abc1234",
            "--transition-receipt-artifact",
            f"{batch_root}/receipts/queue-batch.json",
            "--transition-receipt-summary",
            "queue-batch receipt carried obligation facts",
            *extra_args,
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _json_from_markdown(markdown: str) -> dict[str, object]:
    match = re.search(r"```json\s*\n(.*?)\n```", markdown, flags=re.DOTALL)
    if match is None:
        raise AssertionError("missing JSON fence")
    data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise AssertionError("JSON fence is not an object")
    return data


def _write_transition_batch(
    root: Path,
    *,
    program: str = "planning-state-tooling",
    write_runway: bool = True,
) -> str:
    batch_root = root / "programs" / program / "batches" / "planning-state-write-transitions"
    batch_root.mkdir(parents=True)
    (batch_root / "dispatch.md").write_text("# Dispatch\n", encoding="utf-8")
    if write_runway:
        (batch_root / "runway.md").write_text("# Runway\n", encoding="utf-8")
    return f"docs/plans/programs/{program}/batches/planning-state-write-transitions"


def _write_closeout_validation_fixture(tmp_path: Path) -> tuple[Path, Path, str]:
    root = tmp_path / "docs" / "plans"
    _write_codex_config_fixture(root)
    batch_root = _write_transition_batch(root)
    for relative_path in (
        "completed-slices.md",
        "outputs/pytest.json",
        "receipts/queue-batch.json",
    ):
        path = (
            root
            / "programs"
            / "planning-state-tooling"
            / "batches"
            / "planning-state-write-transitions"
            / relative_path
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    closeout_path = f"{batch_root}/closeout.md"
    _write_closeout_file(root, closeout_path, _closeout_evidence_index())
    state_file = tmp_path / "planning-state.json"
    state_file.write_text(
        json.dumps(_closeout_state_fixture(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return root, state_file, closeout_path


def _write_closeout_file(
    root: Path,
    closeout_path: str,
    closeout: dict[str, object],
) -> None:
    path = root / Path(closeout_path).relative_to("docs/plans")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "```json\n"
        + json.dumps(closeout, indent=2, sort_keys=True)
        + "\n```\n",
        encoding="utf-8",
    )


def _write_state_fixture(
    path: Path,
    *,
    root_value: str = "docs/plans",
    artifacts: list[dict[str, str]] | None = None,
    obligations: list[dict[str, str | None]] | None = None,
    selected_dispatch: str | None = None,
    active_runway: str | None = None,
    queued_batch: str | None = None,
) -> None:
    path.write_text(
        json.dumps(
            {
                "protocol": {
                    "name": "planning-state-tool-state",
                    "version": 1,
                },
                "root": root_value,
                "programs": [
                    {
                        "slug": "planning-state-tooling",
                        "current": (
                            "docs/plans/programs/planning-state-tooling/CURRENT.md"
                        ),
                        "ledger": (
                            "docs/plans/programs/planning-state-tooling/LEDGER.md"
                        ),
                        "selected_dispatch": selected_dispatch,
                        "active_runway": active_runway,
                        "queued_batch": queued_batch,
                        "latest_closeout": None,
                        "artifacts": artifacts or [],
                    }
                ],
                "obligations": obligations or [],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _closeout_state_fixture() -> dict[str, object]:
    batch_id = "planning-state-write-transitions"
    batch_root = f"docs/plans/programs/planning-state-tooling/batches/{batch_id}"
    artifacts = [
        {"batch_id": batch_id, "path": f"{batch_root}/closeout.md", "type": "closeout"},
        {
            "batch_id": batch_id,
            "path": f"{batch_root}/completed-slices.md",
            "type": "completed-slices",
        },
        {"batch_id": batch_id, "path": f"{batch_root}/dispatch.md", "type": "dispatch"},
        {"batch_id": batch_id, "path": f"{batch_root}/outputs/pytest.json", "type": "output"},
        {
            "batch_id": batch_id,
            "path": f"{batch_root}/receipts/queue-batch.json",
            "type": "receipt",
        },
        {"batch_id": batch_id, "path": f"{batch_root}/runway.md", "type": "runway"},
    ]
    return {
        "protocol": {
            "name": "planning-state-tool-state",
            "version": 1,
        },
        "root": "docs/plans",
        "programs": [
            {
                "slug": "planning-state-tooling",
                "current": "docs/plans/programs/planning-state-tooling/CURRENT.md",
                "ledger": "docs/plans/programs/planning-state-tooling/LEDGER.md",
                "selected_dispatch": None,
                "active_runway": None,
                "queued_batch": None,
                "latest_closeout": f"{batch_root}/closeout.md",
                "artifacts": artifacts,
            }
        ],
        "obligations": [
            {
                "id": "PST-OBL-CLOSED",
                "owner": "planning-state-tooling",
                "source_batch": batch_id,
                "target_batch": None,
                "close_condition": "closeout evidence index exists",
                "status": "closed",
                "evidence_path": f"{batch_root}/closeout.md",
            },
            {
                "id": "PST-OBL-OPEN",
                "owner": "next-slice",
                "source_batch": batch_id,
                "target_batch": "next-batch",
                "close_condition": None,
                "status": "open",
                "evidence_path": None,
            },
        ],
    }


def _replace_registered_artifact_path(
    state_fixture: dict[str, object],
    artifact_type: str,
    path: str,
) -> None:
    for artifact in state_fixture["programs"][0]["artifacts"]:
        if artifact["type"] == artifact_type:
            artifact["path"] = path
            return
    raise AssertionError(f"missing registered artifact type: {artifact_type}")


def _closeout_evidence_index(
    *,
    batch_id: str = "planning-state-write-transitions",
) -> dict[str, object]:
    batch_root = f"docs/plans/programs/planning-state-tooling/batches/{batch_id}"
    output_artifact = {
        "batch_id": batch_id,
        "path": f"{batch_root}/outputs/pytest.json",
        "type": "output",
    }
    receipt_artifact = {
        "batch_id": batch_id,
        "path": f"{batch_root}/receipts/queue-batch.json",
        "type": "receipt",
    }
    return {
        "protocol": {
            "name": "planning-state-closeout-evidence-index",
            "version": 1,
        },
        "root": "docs/plans",
        "program": "planning-state-tooling",
        "batch_id": batch_id,
        "status": "closed",
        "artifacts": [
            {"batch_id": batch_id, "path": f"{batch_root}/closeout.md", "type": "closeout"},
            {
                "batch_id": batch_id,
                "path": f"{batch_root}/completed-slices.md",
                "type": "completed-slices",
            },
            {"batch_id": batch_id, "path": f"{batch_root}/dispatch.md", "type": "dispatch"},
            {"batch_id": batch_id, "path": f"{batch_root}/runway.md", "type": "runway"},
        ],
        "commit_evidence": {"commits": ["abc1234"]},
        "validation_evidence": [
            {
                "artifact": output_artifact,
                "summary": "focused pytest, ruff, and diff checks passed",
            }
        ],
        "review_evidence": [
            {
                "artifact": receipt_artifact,
                "summary": "reviewer marked the slice clean",
            }
        ],
        "transition_receipts": [
            {
                "artifact": receipt_artifact,
                "summary": "queue-batch receipt carried obligation facts",
            }
        ],
        "obligations": {
            "closed": [
                {
                    "id": "PST-OBL-CLOSED",
                    "owner": "planning-state-tooling",
                    "source_batch": batch_id,
                    "target_batch": None,
                    "close_condition": "closeout evidence index exists",
                    "status": "closed",
                    "evidence_path": f"{batch_root}/closeout.md",
                }
            ],
            "open": [
                {
                    "id": "PST-OBL-OPEN",
                    "owner": "next-slice",
                    "source_batch": batch_id,
                    "target_batch": "next-batch",
                    "close_condition": None,
                    "status": "open",
                    "evidence_path": None,
                }
            ],
        },
        "cleanup_residue": {
            "classification": "deferred",
            "evidence": ["PST-OBL-OPEN remains assigned to next-batch"],
        },
        "sections": [
            {
                "title": "Evidence Index",
                "items": [
                    "Pointers are registered artifacts, not inferred historical filenames",
                    "Validation and review evidence are summarized with artifact paths",
                ],
            }
        ],
    }


def _write_root_current(root: Path, slug: str) -> None:
    (root / "CURRENT.md").write_text(
        f"""# Planning Current State

- Layout: Planning Artifact Layout v1

## Active Programs

| Program | Current state |
|---|---|
| `{slug}` | `docs/plans/programs/{slug}/CURRENT.md` |
""",
        encoding="utf-8",
    )
