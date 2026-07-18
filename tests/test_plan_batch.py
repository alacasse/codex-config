# pyright: reportMissingImports=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportArgumentType=false, reportIndexIssue=false, reportOptionalSubscript=false, reportCallIssue=false
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from scripts.plan_batch import execute_plan_batch
from scripts.planning_contract import (
    ProducerIdentity,
    apply_current_document,
    apply_ledger_decision,
    read_current_document,
    read_ledger_document,
    validate_planning_contracts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_FIXTURES = REPO_ROOT / "tests/fixtures/planning-contracts"
CURRENT_FIXTURE = CONTRACT_FIXTURES / "current/valid/CURRENT.md"
LEDGER_FIXTURE = CONTRACT_FIXTURES / "ledger/per-finding-valid/LEDGER.md"
ARTIFACT_FIXTURE = CONTRACT_FIXTURES / "artifacts/valid-lineage"
VALIDATION_PROFILE_ID = "project-harness-production"
INSTALLED_CODEX_HOME = Path(
    os.environ.get(
        "COMMAND_OWNER_CANDIDATE_CODEX_HOME",
        "/home/alacasse/.codex-command-owner-redesign",
    )
)
INSTALLED_PLAN_BATCH = INSTALLED_CODEX_HOME / "scripts/plan_batch.py"
SELECTION_FAULT_POINTS = (
    "after_transaction_record_append",
    "before_dispatch_write",
    "after_dispatch_write_before_validation",
    "after_dispatch_validation",
    "before_idle_to_selected_cas",
    "after_idle_to_selected_cas_before_receipt",
    "after_selected_transition_receipt",
    "before_runway_write",
    "after_runway_write_before_validation",
    "after_runway_validation",
    "before_selected_to_queued_cas",
    "after_selected_to_queued_cas_before_receipt",
    "after_queued_transition_receipt",
)


def _thaw(value: object) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(child) for key, child in value.items()}
    if isinstance(value, tuple | list):
        return [_thaw(child) for child in value]
    return copy.deepcopy(value)


def _head(root: Path = REPO_ROOT) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _contracts() -> dict[str, dict[str, Any]]:
    result = validate_planning_contracts([ARTIFACT_FIXTURE], toolchain_root=REPO_ROOT)
    assert result.is_valid, result.diagnostics
    return {
        str(parsed.contract["schema"]): _thaw(parsed.contract)
        for parsed in result.contracts
    }


def _producer(schema: str, commit: str) -> dict[str, str]:
    return {
        "toolchain_generation": "candidate",
        "toolchain_commit": commit,
        "schema_version": schema,
    }


def _vertical_contract(
    coexistence: str = "none",
) -> tuple[dict[str, object], dict[str, object]]:
    vertical: dict[str, object] = {
        "starting_scenario": "one caller still uses the previous planning owner",
        "durable_result": "that caller uses the permanent planning owner",
        "owner_before": "previous planning owner",
        "owner_after": "permanent plan-batch owner",
        "migrated_callers": ["fixture planning caller"],
        "focused_validation": ["fixture.vertical.green"],
        "independently_usable_state": "the migrated caller queues reviewed plans",
        "rollback_boundary": "revert the caller migration",
        "temporary_residue": [],
        "ownership_coexistence": coexistence,
    }
    matrix: dict[str, object] = {}
    if coexistence == "temporary":
        matrix["fixture planning caller"] = {
            "current_owner": "previous planning owner",
            "future_owner": "permanent plan-batch owner",
            "reason": "the caller migrates in this bounded slice",
            "status": "pending",
            "removal_slice_or_condition": "focused vertical tests are green",
        }
    return vertical, matrix


def _state(current_path: Path) -> dict[str, object]:
    current = read_current_document(current_path, toolchain_root=REPO_ROOT)
    selected = current.contract["selected_dispatch"]
    queued = current.contract["queued_runway"]
    active = current.contract["active_runway"]
    semantic = "active" if active else "queued" if queued else "selected" if selected else "idle"
    return {
        "current_status": "valid",
        "validate_status": "valid",
        "semantic_state": semantic,
        "current_revision": current.logical_revision,
        "current_file_hash": current.file_hash,
        "selected_dispatch": selected,
        "queued_runway": queued,
        "active_runway": active,
    }


def _request(tmp_path: Path, *, boundaries: tuple[str, ...] = ("owner-seam",)) -> dict[str, Any]:
    planning_root = tmp_path / "plans"
    planning_root.mkdir(parents=True)
    current_path = planning_root / "CURRENT.md"
    ledger_path = planning_root / "LEDGER.md"
    shutil.copy2(CURRENT_FIXTURE, current_path)
    shutil.copy2(LEDGER_FIXTURE, ledger_path)
    current = read_current_document(current_path, toolchain_root=REPO_ROOT)
    commit = _head()
    contracts = _contracts()
    dispatch = contracts["planning-dispatch/v1"]
    runway = contracts["planning-runway/v1"]
    dispatch["artifact"]["id"] = "fixture-batch"
    dispatch["artifact"]["program"] = "codex-config"
    dispatch["source"]["ledger_path"] = "LEDGER.md"
    dispatch["source"]["finding_ids"] = ["CCFG-1"]
    dispatch["scope"]["included_finding_ids"] = ["CCFG-1"]
    dispatch["scope"]["deferred_finding_ids"] = []
    dispatch["producer"] = _producer("planning-dispatch/v1", commit)
    dispatch["execution_context"] = {
        "toolchain_source_root": str(REPO_ROOT),
        "canonical_planning_repository_root": str(tmp_path),
        "implementation_target_root": str(tmp_path / "candidate"),
    }
    runway["artifact"]["id"] = "fixture-batch"
    runway["artifact"]["source_dispatch"] = "dispatch.md"
    runway["artifact"]["source_dispatch_revision"] = dispatch["artifact"]["revision"]
    runway["batch"]["status"] = "queued"
    runway["producer"] = _producer("planning-runway/v1", commit)
    runway["execution"]["implementation_target_root"] = str(tmp_path / "candidate")
    runway["slices"] = [
        {
            "id": f"slice-{index}",
            "title": boundary.replace("-", " ").title(),
            "risk": "evidence-only",
            "status": "pending",
            "allowed_paths": [f"fixture/{boundary}"],
            "validation": [f"fixture.{boundary}.green"],
        }
        for index, boundary in enumerate(boundaries, start=1)
    ]
    quality = {
        "minimum_viable_scope": True,
        "scope_expansions": [],
        "proportionality": {
            "observed_failure": "plan-batch ownership is not independently executable",
            "invariants": [
                "queue exactly one reviewed finding",
                "stop before implementation",
            ],
            "minimum_viable_change": "validate and queue one reviewed draft",
            "proposed_change": "validate and queue one reviewed draft",
            "additions_beyond_minimum": [],
            "simpler_alternatives_rejected": [
                {
                    "alternative": "retain prose-only planning",
                    "reason": "it cannot prove deterministic queue gates",
                }
            ],
            "verdict": "proportionate",
        },
        "slice_rationales": [
            {
                "slice_id": item["id"],
                "kind": "cohesive" if len(boundaries) == 1 else "producer-consumer",
                "reason": f"separate {boundary} responsibility",
            }
            for item, boundary in zip(runway["slices"], boundaries, strict=True)
        ],
        "unresolved_decisions": [],
        "residual_complexity": [],
        "destructive_actions": [],
        "implementation_started": False,
    }
    draft = {
        "dispatch": dispatch,
        "runway": runway,
        "basis": {
            "current_revision": current.logical_revision,
            "current_file_hash": current.file_hash,
            "ledger_path": str(ledger_path),
            "ledger_file_hash": _hash(ledger_path),
            "finding_id": "CCFG-1",
            "finding_revision": 1,
        },
        "quality": quality,
        "validation_profile": VALIDATION_PROFILE_ID,
    }
    dispatch_producer = _producer("planning-dispatch/v1", commit)
    runway_producer = _producer("planning-runway/v1", commit)
    closeout_producer = _producer("planning-closeout/v1", commit)
    request = {
        "interface": "plan-batch/v1",
        "context": {
            "toolchain_generation": "candidate",
            "toolchain_commit": commit,
            "toolchain_root": str(REPO_ROOT),
            "canonical_planning_repository_root": str(REPO_ROOT),
            "canonical_planning_commit": commit,
            "planning_root": str(planning_root),
            "operation_root_kind": "fixture",
            "canonical_state_mutation_allowed": False,
        },
        "planning_state": _state(current_path),
        "planner_invocation": {
            "role": "batch_planner",
            "caller": "plan-batch",
            "direct": True,
            "invocation_id": "planner-1",
        },
        "planner_result": {
            "interface": "batch-plan-draft/v1",
            "status": "ready",
            "draft": draft,
            "blockers": [],
        },
        "reviewer_invocation": {
            "role": "batch_plan_reviewer",
            "caller": "plan-batch",
            "direct": True,
            "invocation_id": "reviewer-1",
        },
        "reviewer_result": {
            "interface": "batch-plan-review/v1",
            "verdict": "clean",
            "review_basis": {
                "selected_dispatch_sha256": _digest(dispatch),
                "draft_sha256": _digest(draft),
                "approvals_sha256": _digest([]),
                "evidence_packet_sha256": "0" * 64,
            },
            "checks": {
                "currentness": "pass",
                "selection": "pass",
                "scope": "pass",
                "proportionality": "pass",
                "lineage": "pass",
                "approval_scope": "pass",
                "semantic_slices": "pass",
                "vertical_contract": "pass",
                "stop_boundary": "pass",
            },
            "corrections": [],
            "blockers": [],
            "implementation_started": False,
        },
        "approvals": [],
        "review_evidence": {},
        "validation_catalog": [VALIDATION_PROFILE_ID],
        "correction_history": [],
        "transaction": {
            "transaction_id": "fixture-selection",
            "transaction_path": str(planning_root / "selection.md"),
            "current_path": str(current_path),
            "expected_initial_state_revision": current.logical_revision,
            "expected_initial_state_file_hash": current.file_hash,
            "initial_current_contract": _thaw(current.contract),
            "lineage": {
                "planning_root": str(planning_root),
                "program": "codex-config",
                "batch_id": "fixture-batch",
                "included_finding_ids": ["CCFG-1"],
                "deferred_finding_ids": [],
                "batch_kind": "migration",
                "ledger_path": str(ledger_path),
                "ledger_revision": dispatch["source"]["ledger_revision"],
                "dispatch_path": str(planning_root / "dispatch.md"),
                "dispatch_revision": dispatch["artifact"]["revision"],
                "runway_path": str(planning_root / "runway.md"),
                "closeout_path": str(planning_root / "closeout.md"),
                "toolchain_source_root": str(REPO_ROOT),
                "canonical_planning_repository_root": str(tmp_path),
                "implementation_target_root": str(tmp_path / "candidate"),
                "dispatch_producer": dispatch_producer,
                "runway_producer": runway_producer,
                "closeout_producer": closeout_producer,
            },
            "command_owner_version": "plan-batch-v1",
            "producer": _producer("planning-selection-transaction/v1", commit),
        },
    }
    _redraft(request)
    return request


def _refresh_state(request: dict[str, Any]) -> None:
    request["planning_state"] = _state(Path(request["transaction"]["current_path"]))


def _redraft(request: dict[str, Any]) -> None:
    draft = request["planner_result"]["draft"]
    source_content = "Authoritative source evidence for CCFG-1."
    packet = {
        "source_evidence": [
            {
                "source_id": "SRC-1",
                "source_commit": "1" * 40,
                "source_section": "source.md#one",
                "content": source_content,
                "sha256": hashlib.sha256(source_content.encode()).hexdigest(),
            }
        ],
        "user_constraints": ["stop before implementation"],
        "planning_state_diagnostics": {
            "current_sha256": _digest(
                {"command": "current", "planning_state": request["planning_state"]}
            ),
            "validate_sha256": _digest(
                {"command": "validate", "planning_state": request["planning_state"]}
            ),
        },
        "proportionality": copy.deepcopy(draft["quality"]["proportionality"]),
        "approvals": copy.deepcopy(request["approvals"]),
        "draft": copy.deepcopy(draft),
        "selected_dispatch": copy.deepcopy(draft["dispatch"]),
        "invocation_lineage": {
            "planner": copy.deepcopy(request["planner_invocation"]),
            "reviewer": copy.deepcopy(request["reviewer_invocation"]),
        },
    }
    packet_sha256 = _digest(packet)
    request["review_evidence"] = {
        "packet": packet,
        "packet_sha256": packet_sha256,
    }
    request["reviewer_result"]["review_basis"] = {
        "selected_dispatch_sha256": _digest(draft["dispatch"]),
        "draft_sha256": _digest(draft),
        "approvals_sha256": _digest(request["approvals"]),
        "evidence_packet_sha256": packet_sha256,
    }


def _changed_files(root: Path) -> set[str]:
    return {path.name for path in root.rglob("*") if path.is_file()}


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _review_lineage_snapshot(request: dict[str, Any]) -> bytes:
    return json.dumps(
        {
            "review_evidence": request["review_evidence"],
            "reviewer_invocation": request["reviewer_invocation"],
            "reviewer_result": request["reviewer_result"],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()


def test_queues_one_reviewed_batch_and_exact_replay_is_idempotent(tmp_path: Path) -> None:
    request = _request(tmp_path)
    review_lineage = _review_lineage_snapshot(request)

    queued = execute_plan_batch(request)
    first = {
        path.name: path.read_bytes()
        for path in (tmp_path / "plans").iterdir()
        if path.is_file()
    }
    _refresh_state(request)
    assert _review_lineage_snapshot(request) == review_lineage
    replayed = execute_plan_batch(request)

    assert queued["outcome"] == "queued"
    assert queued["next_action"] == "stop_before_implementation"
    assert queued["implementation_started"] is False
    assert replayed["outcome"] == "queued"
    assert replayed["transaction"]["outcome"] == "exact_replay"
    assert _review_lineage_snapshot(request) == review_lineage
    assert {
        path.name: path.read_bytes()
        for path in (tmp_path / "plans").iterdir()
        if path.is_file()
    } == first


@pytest.mark.parametrize("state", ["selected", "queued", "active"])
def test_existing_selected_queued_or_active_work_refuses_new_queue_mutation(
    tmp_path: Path, state: str
) -> None:
    request = _request(tmp_path)
    current_path = Path(request["transaction"]["current_path"])
    current = read_current_document(current_path, toolchain_root=REPO_ROOT)
    replacement = _thaw(current.contract)
    replacement["revision"] = current.logical_revision + 1
    replacement[{"selected": "selected_dispatch", "queued": "queued_runway", "active": "active_runway"}[state]] = f"existing-{state}.md"
    apply_current_document(
        current_path,
        toolchain_root=REPO_ROOT,
        expected_revision=current.logical_revision,
        expected_file_hash=current.file_hash,
        replacement_contract=replacement,
        idempotency_key=f"seed-{state}",
    )
    _refresh_state(request)
    before = _changed_files(tmp_path / "plans")

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert result["next_action"] == "report_existing_state"
    assert _changed_files(tmp_path / "plans") == before
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_current_and_validate_must_be_green_and_exact(tmp_path: Path) -> None:
    request = _request(tmp_path)
    request["planning_state"]["validate_status"] = "blocked"

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "planning_state.invalid"
    assert not Path(request["transaction"]["transaction_path"]).exists()


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("candidate-canonical-write", "context.canonical_authority"),
        ("fixture-inside-canonical", "context.root_kind_bypass"),
        ("temporary-inside-canonical", "context.root_kind_bypass"),
    ],
)
def test_root_authorization_fails_closed_without_writes(
    tmp_path: Path, case: str, expected_code: str
) -> None:
    request = _request(tmp_path)
    if case == "candidate-canonical-write":
        request["context"]["operation_root_kind"] = "canonical"
        request["context"]["canonical_state_mutation_allowed"] = True
    else:
        request["context"]["operation_root_kind"] = case.split("-", 1)[0]
        request["context"]["planning_root"] = str(REPO_ROOT / "tests/fixtures")
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == expected_code
    assert _file_snapshot(planning_root) == before
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_selection_is_exactly_one_open_ledger_finding(tmp_path: Path) -> None:
    request = _request(tmp_path)
    request["transaction"]["lineage"]["included_finding_ids"] = ["CCFG-1", "CCFG-2"]

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "selection.one_finding"
    assert not Path(request["transaction"]["transaction_path"]).exists()


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("missing", "selection.missing_finding"),
        ("closed", "selection.ineligible_finding"),
        ("repeated", "request.string_list"),
        ("selected-and-deferred", "selection.repeated_finding"),
        ("duplicate-deferred", "request.string_list"),
        ("deferred-binding", "selection.deferred_binding"),
    ],
)
def test_invalid_one_finding_lineage_refuses_without_writes(
    tmp_path: Path, case: str, expected_code: str
) -> None:
    request = _request(tmp_path)
    draft = request["planner_result"]["draft"]
    lineage = request["transaction"]["lineage"]
    if case == "missing":
        lineage["included_finding_ids"] = ["CCFG-404"]
        draft["basis"]["finding_id"] = "CCFG-404"
        draft["dispatch"]["source"]["finding_ids"] = ["CCFG-404"]
        draft["dispatch"]["scope"]["included_finding_ids"] = ["CCFG-404"]
    elif case == "closed":
        ledger_path = Path(lineage["ledger_path"])
        ledger = read_ledger_document(ledger_path, toolchain_root=REPO_ROOT)
        finding = _thaw(ledger.findings["CCFG-1"])
        finding["revision"] = 2
        finding["lifecycle"]["status"] = "closed"
        apply_ledger_decision(
            ledger_path,
            toolchain_root=REPO_ROOT,
            expected_revision=ledger.logical_revision,
            expected_file_hash=ledger.file_hash,
            action="reconcile",
            finding_mutations=[finding],
            touched_finding_revisions={"CCFG-1": 1},
            idempotency_key="close-selected-finding",
        )
        draft["basis"]["finding_revision"] = 2
        draft["basis"]["ledger_file_hash"] = _hash(ledger_path)
    elif case == "repeated":
        lineage["included_finding_ids"] = ["CCFG-1", "CCFG-1"]
    elif case == "selected-and-deferred":
        lineage["deferred_finding_ids"] = ["CCFG-1"]
        draft["dispatch"]["scope"]["deferred_finding_ids"] = ["CCFG-1"]
    elif case == "duplicate-deferred":
        lineage["deferred_finding_ids"] = ["CCFG-2", "CCFG-2"]
        draft["dispatch"]["scope"]["deferred_finding_ids"] = [
            "CCFG-2",
            "CCFG-2",
        ]
    elif case == "deferred-binding":
        lineage["deferred_finding_ids"] = ["CCFG-2"]
        draft["dispatch"]["scope"]["deferred_finding_ids"] = []
    else:
        raise AssertionError(f"unknown case {case}")
    _redraft(request)
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == expected_code
    assert _file_snapshot(planning_root) == before
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_cohesive_single_slice_and_justified_multi_slice_both_queue(tmp_path: Path) -> None:
    single = _request(tmp_path / "single")
    multiple = _request(tmp_path / "multiple", boundaries=("producer", "consumer"))

    assert execute_plan_batch(single)["outcome"] == "queued"
    assert execute_plan_batch(multiple)["outcome"] == "queued"


def test_accepts_migration_with_complete_vertical_contract_and_no_coexistence(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    slice_item = request["planner_result"]["draft"]["runway"]["slices"][0]
    vertical, matrix = _vertical_contract()
    slice_item.update(
        risk="migration", vertical_slice=vertical, migration_matrix=matrix
    )
    _redraft(request)

    assert execute_plan_batch(request)["outcome"] == "queued"


def test_accepts_migration_with_temporary_coexistence_and_complete_matrix(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    slice_item = request["planner_result"]["draft"]["runway"]["slices"][0]
    vertical, matrix = _vertical_contract("temporary")
    slice_item.update(
        risk="migration", vertical_slice=vertical, migration_matrix=matrix
    )
    _redraft(request)

    assert execute_plan_batch(request)["outcome"] == "queued"


def test_rejects_migration_missing_vertical_slice(tmp_path: Path) -> None:
    request = _request(tmp_path)
    request["planner_result"]["draft"]["runway"]["slices"][0]["risk"] = "migration"
    _redraft(request)

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "quality.vertical_contract"
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_rejects_migration_missing_matrix_without_queue_mutation(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    slice_item = request["planner_result"]["draft"]["runway"]["slices"][0]
    vertical, matrix = _vertical_contract()
    slice_item.update(
        risk="migration", vertical_slice=vertical, migration_matrix=matrix
    )
    del slice_item["migration_matrix"]
    _redraft(request)
    planning_root = tmp_path / "plans"
    state_before = _state(Path(request["transaction"]["current_path"]))
    files_before = _file_snapshot(planning_root)

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "quality.vertical_contract"
    assert _state(Path(request["transaction"]["current_path"])) == state_before
    assert _file_snapshot(planning_root) == files_before
    assert not Path(request["transaction"]["transaction_path"]).exists()


@pytest.mark.parametrize("matrix_case", ["empty", "incomplete"])
def test_rejects_temporary_coexistence_with_empty_or_incomplete_matrix(
    tmp_path: Path, matrix_case: str
) -> None:
    request = _request(tmp_path)
    slice_item = request["planner_result"]["draft"]["runway"]["slices"][0]
    vertical, matrix = _vertical_contract("temporary")
    if matrix_case == "empty":
        matrix = {}
    else:
        del matrix["fixture planning caller"]["removal_slice_or_condition"]
    slice_item.update(
        risk="migration", vertical_slice=vertical, migration_matrix=matrix
    )
    _redraft(request)

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "quality.vertical_contract"
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_rejects_no_coexistence_with_retained_matrix_rows(tmp_path: Path) -> None:
    request = _request(tmp_path)
    slice_item = request["planner_result"]["draft"]["runway"]["slices"][0]
    vertical, matrix = _vertical_contract("temporary")
    vertical["ownership_coexistence"] = "none"
    slice_item.update(
        risk="migration", vertical_slice=vertical, migration_matrix=matrix
    )
    _redraft(request)

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "quality.vertical_contract"
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_accepts_non_migration_without_vertical_contract(tmp_path: Path) -> None:
    request = _request(tmp_path)

    assert execute_plan_batch(request)["outcome"] == "queued"


def test_applies_mixed_risk_contract_only_to_migration_slices(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path, boundaries=("evidence", "migration"))
    draft = request["planner_result"]["draft"]
    draft["dispatch"]["scope"]["batch_kind"] = "mixed-risk"
    draft["runway"]["batch"]["kind"] = "mixed-risk"
    request["transaction"]["lineage"]["batch_kind"] = "mixed-risk"
    migration_slice = draft["runway"]["slices"][1]
    vertical, matrix = _vertical_contract()
    migration_slice.update(
        risk="migration", vertical_slice=vertical, migration_matrix=matrix
    )
    _redraft(request)

    assert execute_plan_batch(request)["outcome"] == "queued"


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda request: request["planner_result"]["draft"]["quality"][
                "slice_rationales"
            ][0].update({"kind": "filler"}),
            "quality.filler_slice",
        ),
        (
            lambda request: request["planner_result"]["draft"]["quality"].update(
                {"scope_expansions": ["unrelated cleanup"]}
            ),
            "quality.scope_expansion",
        ),
        (
            lambda request: request["planner_result"]["draft"]["quality"].update(
                {"unresolved_decisions": ["choose migration policy"]}
            ),
            "quality.unresolved_decisions",
        ),
    ],
)
def test_filler_expansion_and_unresolved_decisions_block_before_queue(
    tmp_path: Path, mutation: Any, code: str
) -> None:
    request = _request(tmp_path, boundaries=("producer", "consumer"))
    mutation(request)
    _redraft(request)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == code
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_over_specified_proposal_blocks_until_narrowed_to_minimum(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    proportionality = request["planner_result"]["draft"]["quality"][
        "proportionality"
    ]
    proportionality["proposed_change"] = "replace planning and execution owners"
    proportionality["additions_beyond_minimum"] = [
        {
            "addition": "replace execution ownership",
            "prevented_failure": "none within the selected planning finding",
            "minimum_insufficient_reason": "the minimum is sufficient",
        }
    ]
    proportionality["verdict"] = "over-specified"
    _redraft(request)
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    blocked = execute_plan_batch(request)

    assert blocked["blockers"][0]["code"] == "quality.proportionality"
    assert _file_snapshot(planning_root) == before
    proportionality["proposed_change"] = proportionality["minimum_viable_change"]
    proportionality["additions_beyond_minimum"] = []
    proportionality["verdict"] = "proportionate"
    _redraft(request)
    assert execute_plan_batch(request)["outcome"] == "queued"


def test_complete_proportionality_record_is_mechanically_required(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    proportionality = request["planner_result"]["draft"]["quality"][
        "proportionality"
    ]
    del proportionality["simpler_alternatives_rejected"]
    _redraft(request)
    before = _file_snapshot(tmp_path / "plans")

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "request.fields"
    assert _file_snapshot(tmp_path / "plans") == before


def test_residual_complexity_requires_fresh_review_of_exact_approval(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    request["planner_result"]["draft"]["quality"]["residual_complexity"] = [
        {"id": "bridge", "scope": "fixture-batch:bridge"}
    ]
    _redraft(request)

    blocked = execute_plan_batch(request)
    request["approvals"] = [
        {"scope": "fixture-batch:bridge", "decision": "approved"}
    ]
    stale_review = execute_plan_batch(request)
    _redraft(request)
    queued = execute_plan_batch(request)

    assert blocked["blockers"][0]["code"] == "quality.approval_scope"
    assert stale_review["blockers"][0]["code"] == "review_evidence.binding"
    assert queued["outcome"] == "queued"


@pytest.mark.parametrize("mutation", ["add", "change"])
def test_approval_record_changes_after_review_require_fresh_review(
    tmp_path: Path, mutation: str
) -> None:
    request = _request(tmp_path)
    if mutation == "change":
        request["planner_result"]["draft"]["dispatch"]["approval_gates"] = [
            "fixture-batch:original"
        ]
        request["approvals"] = [
            {"scope": "fixture-batch:original", "decision": "approved"}
        ]
        _redraft(request)
        request["planner_result"]["draft"]["dispatch"]["approval_gates"] = [
            "fixture-batch:changed"
        ]
        request["approvals"][0]["scope"] = "fixture-batch:changed"
    else:
        request["planner_result"]["draft"]["dispatch"]["approval_gates"] = [
            "fixture-batch:added"
        ]
        request["approvals"].append(
            {"scope": "fixture-batch:added", "decision": "approved"}
        )
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    blocked = execute_plan_batch(request)

    assert blocked["blockers"][0]["code"] == "review_evidence.binding"
    assert _file_snapshot(planning_root) == before
    _redraft(request)
    assert execute_plan_batch(request)["outcome"] == "queued"


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("missing-dispatch-gate", "quality.approval_scope"),
        ("unrelated", "quality.approval_unrelated"),
    ],
)
def test_approvals_reconcile_exactly_with_declared_gates(
    tmp_path: Path, case: str, expected_code: str
) -> None:
    request = _request(tmp_path)
    if case == "missing-dispatch-gate":
        request["planner_result"]["draft"]["dispatch"]["approval_gates"] = [
            "fixture-batch:gate"
        ]
    else:
        request["approvals"] = [
            {"scope": "fixture-batch:unrelated", "decision": "approved"}
        ]
    _redraft(request)
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == expected_code
    assert _file_snapshot(planning_root) == before


def test_reversed_otherwise_correct_approvals_refuse_without_writes(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    first = "fixture-batch:first-gate"
    second = "fixture-batch:second-gate"
    request["planner_result"]["draft"]["dispatch"]["approval_gates"] = [
        first,
        second,
    ]
    request["approvals"] = [
        {"scope": second, "decision": "approved"},
        {"scope": first, "decision": "approved"},
    ]
    _redraft(request)
    before = _file_snapshot(tmp_path / "plans")

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "quality.approval_order"
    assert _file_snapshot(tmp_path / "plans") == before


def test_roles_are_direct_and_reviewer_correction_routes_to_planner(tmp_path: Path) -> None:
    indirect = _request(tmp_path / "indirect")
    indirect["reviewer_invocation"]["direct"] = False
    correction = _request(tmp_path / "correction")
    correction["reviewer_result"]["verdict"] = "correction_required"
    correction["reviewer_result"]["corrections"] = ["narrow the second slice"]

    indirect_result = execute_plan_batch(indirect)
    correction_result = execute_plan_batch(correction)

    assert indirect_result["blockers"][0]["code"] == "roles.direct_invocation"
    assert correction_result["blockers"][0]["code"] == "review.correction_required"
    assert correction_result["next_action"] == "return_to_batch_planner"


@pytest.mark.parametrize("review_state", ["missing", "failed"])
def test_independent_review_must_check_the_exact_vertical_contract(
    tmp_path: Path, review_state: str
) -> None:
    request = _request(tmp_path)
    checks = request["reviewer_result"]["checks"]
    if review_state == "missing":
        del checks["vertical_contract"]
    else:
        checks["vertical_contract"] = "fail"

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] in {"request.fields", "review.checks"}
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_repeated_material_correction_against_unchanged_draft_stops(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    correction = "narrow the second slice"
    request["reviewer_result"]["verdict"] = "correction_required"
    request["reviewer_result"]["corrections"] = [correction]
    draft_sha256 = _digest(request["planner_result"]["draft"])
    request["correction_history"] = [
        {
            "draft_sha256": draft_sha256,
            "correction": correction,
            "material": True,
        }
    ]
    _redraft(request)
    before = _file_snapshot(tmp_path / "plans")

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "review.repeated_correction"
    assert result["next_action"] == "stop"
    assert _file_snapshot(tmp_path / "plans") == before


@pytest.mark.parametrize("basis", ["selected_dispatch_sha256", "draft_sha256"])
def test_review_must_bind_exact_dispatch_and_draft(tmp_path: Path, basis: str) -> None:
    request = _request(tmp_path)
    request["reviewer_result"]["review_basis"][basis] = "0" * 64

    result = execute_plan_batch(request)

    assert result["outcome"] == "blocked"
    assert not Path(request["transaction"]["transaction_path"]).exists()


def test_stale_draft_basis_blocks_before_transaction(tmp_path: Path) -> None:
    request = _request(tmp_path)
    request["planner_result"]["draft"]["basis"]["ledger_file_hash"] = "0" * 64
    _redraft(request)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "draft.stale"
    assert not Path(request["transaction"]["transaction_path"]).exists()


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("source-digest", "review_evidence.source_digest"),
        ("source-lineage", "review_evidence.source_lineage"),
        ("user-constraints", "review_evidence.user_constraints"),
        ("planning-state", "review_evidence.planning_state"),
        ("invocation-lineage", "review_evidence.invocation_lineage"),
        ("selected-dispatch", "review_evidence.binding"),
        ("complete-draft", "review_evidence.binding"),
        ("proportionality", "review_evidence.binding"),
        ("packet-digest", "review_evidence.digest"),
        ("review-basis", "review.evidence_basis"),
    ],
)
def test_independent_review_evidence_packet_mismatches_block_without_writes(
    tmp_path: Path, case: str, expected_code: str
) -> None:
    request = _request(tmp_path)
    packet = request["review_evidence"]["packet"]
    if case == "source-digest":
        packet["source_evidence"][0]["sha256"] = "0" * 64
    elif case == "source-lineage":
        packet["source_evidence"][0]["source_commit"] = "2" * 40
    elif case == "user-constraints":
        packet["user_constraints"] = []
    elif case == "planning-state":
        packet["planning_state_diagnostics"]["current_sha256"] = "0" * 64
    elif case == "invocation-lineage":
        packet["invocation_lineage"]["reviewer"]["invocation_id"] = "foreign-review"
    elif case == "selected-dispatch":
        packet["selected_dispatch"]["scope"]["goal"] = "foreign selected scope"
    elif case == "complete-draft":
        packet["draft"]["runway"]["batch"]["kind"] = "foreign-kind"
    elif case == "proportionality":
        packet["proportionality"]["observed_failure"] = "foreign failure"
    elif case == "packet-digest":
        request["review_evidence"]["packet_sha256"] = "0" * 64
    elif case == "review-basis":
        request["reviewer_result"]["review_basis"][
            "evidence_packet_sha256"
        ] = "0" * 64
    else:
        raise AssertionError(f"unknown case {case}")
    if case not in {"packet-digest", "review-basis"}:
        packet_sha256 = _digest(packet)
        request["review_evidence"]["packet_sha256"] = packet_sha256
        request["reviewer_result"]["review_basis"][
            "evidence_packet_sha256"
        ] = packet_sha256
    before = _file_snapshot(tmp_path / "plans")

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == expected_code
    assert _file_snapshot(tmp_path / "plans") == before


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("unknown", "validation_profile.selection"),
        ("non-opaque", "validation_profile.catalog"),
        ("duplicate", "validation_profile.duplicate"),
        ("multiple-selected", "request.string"),
    ],
)
def test_exactly_one_catalogued_validation_profile_is_required(
    tmp_path: Path, case: str, expected_code: str
) -> None:
    request = _request(tmp_path)
    if case == "unknown":
        request["planner_result"]["draft"]["validation_profile"] = "unknown"
    elif case == "non-opaque":
        request["validation_catalog"][0] = {"id": VALIDATION_PROFILE_ID}
    elif case == "duplicate":
        request["validation_catalog"].append(request["validation_catalog"][0])
    elif case == "multiple-selected":
        request["planner_result"]["draft"]["validation_profile"] = [
            VALIDATION_PROFILE_ID,
            "another-profile",
        ]
    else:
        raise AssertionError(f"unknown case {case}")
    _redraft(request)
    before = _file_snapshot(tmp_path / "plans")

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == expected_code
    assert _file_snapshot(tmp_path / "plans") == before


@pytest.mark.parametrize("fault", SELECTION_FAULT_POINTS)
def test_every_dec_038_fault_resumes_and_exactly_replays_without_duplicates(
    tmp_path: Path, fault: str
) -> None:
    request = _request(tmp_path)
    initial_revision = request["transaction"]["expected_initial_state_revision"]
    review_lineage = _review_lineage_snapshot(request)

    with pytest.raises(RuntimeError):
        execute_plan_batch(request, fault=fault)
    assert _review_lineage_snapshot(request) == review_lineage
    _refresh_state(request)
    assert _review_lineage_snapshot(request) == review_lineage
    resumed = execute_plan_batch(request)
    completed = _file_snapshot(tmp_path / "plans")
    assert _review_lineage_snapshot(request) == review_lineage
    _refresh_state(request)
    assert _review_lineage_snapshot(request) == review_lineage
    replayed = execute_plan_batch(request)
    current = read_current_document(
        Path(request["transaction"]["current_path"]), toolchain_root=REPO_ROOT
    )

    assert resumed["outcome"] == "queued"
    assert resumed["transaction"]["outcome"] in {"completed", "exact_replay"}
    assert replayed["transaction"]["outcome"] == "exact_replay"
    assert current.logical_revision == initial_revision + 2
    assert current.contract["selected_dispatch"] is None
    assert current.contract["queued_runway"] == "runway.md"
    assert _file_snapshot(tmp_path / "plans") == completed
    assert _review_lineage_snapshot(request) == review_lineage


def test_manufactured_live_state_rereview_is_rejected_and_unnecessary(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path)
    immutable_review = {
        key: copy.deepcopy(request[key])
        for key in ("review_evidence", "reviewer_invocation", "reviewer_result")
    }
    review_lineage = _review_lineage_snapshot(request)

    with pytest.raises(RuntimeError):
        execute_plan_batch(
            request,
            fault="after_idle_to_selected_cas_before_receipt",
        )
    _refresh_state(request)
    partial = _file_snapshot(tmp_path / "plans")
    _redraft(request)
    assert _review_lineage_snapshot(request) != review_lineage

    rejected = execute_plan_batch(request)

    assert rejected["blockers"][0]["code"] == "review_evidence.planning_state"
    assert _file_snapshot(tmp_path / "plans") == partial
    for key, value in immutable_review.items():
        request[key] = value
    assert _review_lineage_snapshot(request) == review_lineage
    resumed = execute_plan_batch(request)
    assert resumed["outcome"] == "queued"
    assert _review_lineage_snapshot(request) == review_lineage


@pytest.mark.parametrize("binding", ["transaction", "dispatch", "runway"])
def test_foreign_producer_bindings_block_before_queue_mutation(
    tmp_path: Path, binding: str
) -> None:
    request = _request(tmp_path)
    foreign_commit = "0" * 40
    if binding == "transaction":
        request["transaction"]["producer"]["toolchain_commit"] = foreign_commit
    else:
        lineage_producer = request["transaction"]["lineage"][
            f"{binding}_producer"
        ]
        draft_producer = request["planner_result"]["draft"][binding]["producer"]
        lineage_producer["toolchain_commit"] = foreign_commit
        draft_producer["toolchain_commit"] = foreign_commit
        _redraft(request)
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "producer.lineage"
    assert _file_snapshot(planning_root) == before
    assert not Path(request["transaction"]["transaction_path"]).exists()


@pytest.mark.parametrize("path_binding", ["transaction", "closeout"])
def test_out_of_root_write_scope_blocks_without_external_effects(
    tmp_path: Path, path_binding: str
) -> None:
    request = _request(tmp_path)
    outside = tmp_path / "outside"
    if path_binding == "transaction":
        request["transaction"]["transaction_path"] = str(outside / "selection.md")
    else:
        request["transaction"]["lineage"]["closeout_path"] = str(
            outside / "closeout.md"
        )
    planning_root = tmp_path / "plans"
    before = _file_snapshot(planning_root)

    result = execute_plan_batch(request)

    assert result["blockers"][0]["code"] == "context.write_scope"
    assert _file_snapshot(planning_root) == before
    assert not outside.exists()


def test_cli_returns_one_deterministic_json_result(tmp_path: Path) -> None:
    request = _request(tmp_path)
    process = subprocess.run(
        [str(REPO_ROOT / ".venv/bin/python"), "-P", str(REPO_ROOT / "scripts/plan_batch.py")],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=False,
    )

    assert process.returncode == 0
    assert process.stderr == ""
    assert json.loads(process.stdout)["outcome"] == "queued"


def test_installed_cli_bootstrap_precedes_competing_project_root(
    tmp_path: Path,
) -> None:
    request = _request(tmp_path / "request")
    competing_root = tmp_path / "competing"
    competing_scripts = competing_root / "scripts"
    competing_scripts.mkdir(parents=True)
    (competing_scripts / "__init__.py").write_text("", encoding="utf-8")
    (competing_scripts / "planning_contract.py").write_text(
        'raise RuntimeError("foreign planning contract imported")\n',
        encoding="utf-8",
    )
    assert INSTALLED_PLAN_BATCH.is_symlink()
    assert INSTALLED_PLAN_BATCH.resolve(strict=True) == (
        REPO_ROOT / "scripts/plan_batch.py"
    ).resolve(strict=True)
    installed_root = INSTALLED_PLAN_BATCH.parent.parent
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(competing_root), str(installed_root)]
    )

    process = subprocess.run(
        [sys.executable, "-P", str(INSTALLED_PLAN_BATCH)],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )

    assert process.returncode == 0
    assert process.stderr == ""
    assert json.loads(process.stdout)["outcome"] == "queued"


def test_installed_cli_uses_opaque_profile_id_without_batch_runway_source(
    tmp_path: Path,
) -> None:
    isolated_codex_home = tmp_path / "isolated-codex-home"
    install = subprocess.run(
        [
            str(REPO_ROOT / "install.sh"),
            "--codex-home",
            str(isolated_codex_home),
            "--feature",
            "plan-batch",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert install.returncode == 0
    assert install.stderr == ""
    installed_state = json.loads(
        (isolated_codex_home / "codex-config/installed-features.json").read_text(
            encoding="utf-8"
        )
    )
    installed_features = installed_state["features"]
    assert set(installed_features) == {
        "planning-contracts",
        "planning-artifacts",
        "planning-state",
        "custom-agents",
        "plan-batch",
    }
    assert "batch-runway" not in installed_features
    assert not (isolated_codex_home / "skills/batch-runway").exists()
    assert not (isolated_codex_home / "skills/batch-runway").is_symlink()
    assert all(
        "batch-runway" not in link["target"]
        for feature in installed_features.values()
        for link in feature["links"]
    )
    isolated_owner = isolated_codex_home / "scripts/plan_batch.py"
    assert isolated_owner.is_symlink()
    assert isolated_owner.resolve(strict=True) == REPO_ROOT / "scripts/plan_batch.py"

    request = _request(tmp_path)
    opaque_profile = "isolated-project-validation"
    request["planner_result"]["draft"]["validation_profile"] = opaque_profile
    request["validation_catalog"] = [opaque_profile]
    _redraft(request)
    encoded_request = json.dumps(request)
    assert "batch-runway" not in encoded_request.casefold()
    assert "validation-profiles" not in encoded_request.casefold()

    process = subprocess.run(
        [sys.executable, "-P", str(isolated_owner)],
        input=encoded_request,
        text=True,
        capture_output=True,
        check=False,
    )

    assert process.returncode == 0
    assert process.stderr == ""
    result = json.loads(process.stdout)
    assert result["outcome"] == "queued"
    assert (tmp_path / "plans/dispatch.md").is_file()
    assert (tmp_path / "plans/runway.md").is_file()
    assert (tmp_path / "plans/selection.md").is_file()


def test_output_producer_shapes_match_existing_transaction_contract() -> None:
    commit = _head()
    producer = _producer("planning-selection-transaction/v1", commit)

    assert producer == {
        "toolchain_generation": "candidate",
        "toolchain_commit": commit,
        "schema_version": "planning-selection-transaction/v1",
    }
    assert ProducerIdentity(**producer) == ProducerIdentity(
        "candidate", commit, "planning-selection-transaction/v1"
    )
