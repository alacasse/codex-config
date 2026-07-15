from __future__ import annotations

import importlib.util
import json
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

from scripts.command_owner_scenarios import build_report, validate_catalog


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "command-owner-scenarios"
CURRENTNESS_IDS = (
    "planning-selected-current",
    "planning-queued-current",
    "planning-active-current",
    "planning-invalid-blocked",
    "planning-stale-state-blocked",
    "planning-head-advanced-ready",
    "implementation-moved-blocked",
    "preparation-movement-blocked",
    "protected-handoff-ready",
    "wrong-root-write-blocked",
    "wrong-generation-blocked",
    "mixed-generation-result-blocked",
    "stale-review-basis-blocked",
    "reused-worker-reviewer-lease-blocked",
    "missing-receipt-blocked",
    "stale-receipt-revision-blocked",
    "unrelated-commit-content-blocked",
    "partial-reconciliation-blocked",
    "unexpected-workspace-write-blocked",
    "untracked-implementation-write-blocked",
    "undeclared-planning-write-blocked",
)


def test_command_owner_scenario_currentness_families_are_green() -> None:
    validation = validate_catalog(FIXTURE_ROOT)
    assert validation.is_valid
    assert validation.catalog is not None

    report = build_report(validation.catalog)
    families = {
        cast(str, family["id"]): cast(str, family["status"])
        for family in cast(list[Mapping[str, object]], report["families"])
    }
    scenarios = {
        cast(str, scenario["id"]): scenario
        for scenario in cast(list[Mapping[str, object]], report["scenarios"])
    }

    assert families["planning-state-ledger"] == "green"
    assert families["execution-currentness"] == "green"
    assert {scenario_id: scenarios[scenario_id]["status"] for scenario_id in CURRENTNESS_IDS} == {
        scenario_id: "green" for scenario_id in CURRENTNESS_IDS
    }


@pytest.mark.parametrize("scenario_id", CURRENTNESS_IDS)
def test_command_owner_scenario_currentness_cases_match_observable_effects(
    tmp_path: Path, scenario_id: str
) -> None:
    adapter = _load_adapter()
    scenario = _scenario(scenario_id)
    workspace = tmp_path / "workspace"

    observation = adapter.run_scenario(scenario, FIXTURE_ROOT, workspace)

    assert observation["transition"] == scenario["expected_transition"]
    assert observation["writes"] == scenario["expected_writes"]
    assert observation["stop_reason"] == scenario["expected_stop_reason"]
    assert all(path.is_relative_to(tmp_path) for path in workspace.rglob("*"))
    assert not (tmp_path / "outside").exists()


def test_invalid_planning_state_blocks_before_mechanical_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    adapter = _load_adapter()
    scenario = _scenario("planning-invalid-blocked")
    invoked = False

    def fail_if_invoked(_payload: Mapping[str, object]) -> None:
        nonlocal invoked
        invoked = True
        raise AssertionError("mechanical helper must not run for invalid semantic state")

    monkeypatch.setattr(adapter.context_owner, "parse_cross_checkout_context", fail_if_invoked)

    adapter.run_scenario(scenario, FIXTURE_ROOT, tmp_path / "workspace")
    outcome = _read_outcome(tmp_path)

    assert invoked is False
    assert outcome == {
        "helper_invoked": False,
        "reason": "Planning State validation blocked before lease preparation",
        "semantic_state": None,
        "status": "blocked",
    }


def test_stale_planning_state_blocks_before_mechanical_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    adapter = _load_adapter()
    invoked = False

    def fail_if_invoked(_payload: Mapping[str, object]) -> None:
        nonlocal invoked
        invoked = True
        raise AssertionError("mechanical helper must not run for stale semantic state")

    monkeypatch.setattr(adapter.context_owner, "parse_cross_checkout_context", fail_if_invoked)

    adapter.run_scenario(
        _scenario("planning-stale-state-blocked"),
        FIXTURE_ROOT,
        tmp_path / "workspace",
    )
    current = json.loads((tmp_path / "workspace" / "current.json").read_text())
    validate = json.loads((tmp_path / "workspace" / "validate.json").read_text())
    outcome = _read_outcome(tmp_path)

    assert invoked is False
    assert current["protocol"]["command"] == "current"
    assert validate["protocol"]["command"] == "validate"
    assert {blocker["code"] for blocker in current["blockers"]} == {
        "migrated_state_mismatch"
    }
    assert {blocker["code"] for blocker in validate["blockers"]} == {
        "migrated_state_mismatch"
    }
    assert validate["exit"]["code"] == 1
    assert outcome == {
        "helper_invoked": False,
        "reason": "Planning State reports stale state before lease preparation",
        "semantic_state": None,
        "status": "blocked",
    }


@pytest.mark.parametrize(
    ("scenario_id", "semantic_state"),
    (
        ("planning-selected-current", "selected"),
        ("planning-queued-current", "queued"),
        ("planning-active-current", "active"),
    ),
)
def test_current_and_validate_are_the_semantic_state_authority(
    tmp_path: Path, scenario_id: str, semantic_state: str
) -> None:
    adapter = _load_adapter()

    adapter.run_scenario(_scenario(scenario_id), FIXTURE_ROOT, tmp_path / "workspace")
    current = json.loads((tmp_path / "workspace" / "current.json").read_text())
    validate = json.loads((tmp_path / "workspace" / "validate.json").read_text())
    outcome = _read_outcome(tmp_path)

    assert current["protocol"]["command"] == "current"
    assert validate["protocol"]["command"] == "validate"
    assert validate["blockers"] == []
    assert outcome["semantic_state"] == semantic_state
    assert outcome["helper_invoked"] is True
    assert "historical_batch_artifact" in {
        warning["code"] for warning in current["warnings"]
    }


def test_protected_handoff_binds_lease_scope_receipt_and_reviewer_base(
    tmp_path: Path,
) -> None:
    adapter = _load_adapter()

    adapter.run_scenario(
        _scenario("protected-handoff-ready"), FIXTURE_ROOT, tmp_path / "workspace"
    )
    workspace = tmp_path / "workspace"
    receipt = json.loads((workspace / "lease-receipt.json").read_text())
    reviewer_receipt = json.loads(
        (workspace / "reviewer-lease-receipt.json").read_text()
    )
    reviewer_preparation = json.loads(
        (workspace / "reviewer-lease-preparation.json").read_text()
    )
    worker = json.loads((workspace / "worker-result.json").read_text())
    commit = json.loads((workspace / "commit-evidence.json").read_text())
    review = json.loads((workspace / "review-result.json").read_text())
    reconciliation = json.loads(
        (workspace / "reconciliation-result.json").read_text()
    )
    outcome = _read_outcome(tmp_path)

    assert receipt["interface"] == "cross-checkout-receipt/v1"
    assert receipt["allowed_scope"]["planning_paths"] == []
    assert receipt["allowed_scope"]["implementation_paths"] == [
        str((workspace / "implementation-repo" / "allowed.txt").resolve())
    ]
    assert worker["verified_context"] != review["verified_context"]
    assert receipt["repository_revisions"]["implementation_commit_before"] == commit[
        "base"
    ]
    assert worker["verified_context"]["implementation_commit_before"] == commit["base"]
    assert reviewer_preparation["payload"]["implementation_commit_before"] == commit[
        "head"
    ]
    assert review["verified_context"] == reviewer_preparation["payload"]
    assert reviewer_receipt["repository_revisions"][
        "implementation_commit_before"
    ] == commit["head"]
    assert reviewer_receipt["allowed_scope"] == receipt["allowed_scope"]
    assert commit["paths"] == ["allowed.txt"]
    assert review["base"] == outcome["base"]
    assert review["commit"] == outcome["commit"]
    assert reconciliation["validate"]["blockers"] == []
    assert reconciliation["current"]["programs"][0]["queued_batch"]["value"].endswith(
        "/runway.md"
    )


@pytest.mark.parametrize(
    ("scenario_id", "boundary"),
    (
        ("implementation-moved-blocked", "unexpected_implementation_movement"),
        ("preparation-movement-blocked", "movement_during_preparation"),
    ),
)
def test_movement_faults_cross_distinct_observation_boundaries(
    tmp_path: Path, scenario_id: str, boundary: str
) -> None:
    adapter = _load_adapter()

    adapter.run_scenario(_scenario(scenario_id), FIXTURE_ROOT, tmp_path / "workspace")
    preparation = json.loads(
        (tmp_path / "workspace" / "lease-preparation.json").read_text()
    )
    outcome = _read_outcome(tmp_path)

    assert preparation["error"] == boundary
    assert outcome["boundary"] == boundary
    if boundary == "unexpected_implementation_movement":
        assert (
            preparation["planned"]["implementation_commit"]
            != preparation["before_hook"]["implementation_commit"]
        )
        assert preparation["before_hook"] == preparation["after_hook"]
    else:
        assert preparation["planned"] == preparation["before_hook"]
        assert (
            preparation["before_hook"]["implementation_commit"]
            != preparation["after_hook"]["implementation_commit"]
        )


def test_between_observations_hook_is_the_preparation_race_boundary(
    tmp_path: Path,
) -> None:
    adapter = _load_adapter()
    invocations = 0

    def move_between(
        _workspace: Path, _planning: Path, implementation: Path
    ) -> None:
        nonlocal invocations
        invocations += 1
        adapter._commit_file(implementation, "unexpected.txt", "hook movement\n")

    adapter.run_scenario(
        _scenario("preparation-movement-blocked"),
        FIXTURE_ROOT,
        tmp_path / "workspace",
        between_observations=move_between,
    )

    assert invocations == 1
    assert _read_outcome(tmp_path)["boundary"] == "movement_during_preparation"


@pytest.mark.parametrize(
    ("scenario_id", "boundary"),
    (
        ("mixed-generation-result-blocked", "worker_result"),
        ("missing-receipt-blocked", "receipt"),
        ("stale-receipt-revision-blocked", "receipt_revisions"),
        ("unrelated-commit-content-blocked", "commit_range"),
        ("reused-worker-reviewer-lease-blocked", "reviewer_lease"),
        ("stale-review-basis-blocked", "reviewer_basis"),
        ("partial-reconciliation-blocked", "reconciliation_state"),
        ("unexpected-workspace-write-blocked", "workspace_writes"),
        ("untracked-implementation-write-blocked", "workspace_writes"),
        ("undeclared-planning-write-blocked", "workspace_writes"),
    ),
)
def test_each_independent_handoff_consumer_fails_closed(
    tmp_path: Path, scenario_id: str, boundary: str
) -> None:
    adapter = _load_adapter()

    adapter.run_scenario(_scenario(scenario_id), FIXTURE_ROOT, tmp_path / "workspace")

    assert _read_outcome(tmp_path)["boundary"] == boundary


def test_handoff_consumers_are_independently_injected(tmp_path: Path) -> None:
    adapter = _load_adapter()
    defaults = adapter._default_consumers()
    observed: list[str] = []

    def record(
        name: str, consumer: Callable[[Mapping[str, object]], None]
    ) -> Callable[[Mapping[str, object]], None]:
        def wrapped(request: Mapping[str, object]) -> None:
            observed.append(name)
            consumer(request)

        return wrapped

    consumers = adapter.HandoffConsumers(
        worker_result=record("worker_result", defaults.worker_result),
        receipt=record("receipt", defaults.receipt),
        commit=record("commit", defaults.commit),
        reviewer_receipt=record("reviewer_receipt", defaults.reviewer_receipt),
        reviewer=record("reviewer", defaults.reviewer),
        reconciliation=record("reconciliation", defaults.reconciliation),
        workspace=record("workspace", defaults.workspace),
    )

    adapter.run_scenario(
        _scenario("protected-handoff-ready"),
        FIXTURE_ROOT,
        tmp_path / "workspace",
        handoff_consumers=consumers,
    )

    assert observed == [
        "worker_result",
        "receipt",
        "commit",
        "reviewer_receipt",
        "reviewer",
        "reconciliation",
        "workspace",
    ]


def test_complete_workspace_diff_detects_unexpected_in_workspace_write(
    tmp_path: Path,
) -> None:
    adapter = _load_adapter()
    scenario = _scenario("unexpected-workspace-write-blocked")

    observation = adapter.run_scenario(
        scenario, FIXTURE_ROOT, tmp_path / "workspace"
    )
    outcome = _read_outcome(tmp_path)

    assert observation["writes"] == scenario["expected_writes"]
    assert "workspace/unexpected-workspace.txt" in observation["writes"]
    assert outcome["evidence"]["unexpected_paths"] == [
        "workspace/unexpected-workspace.txt"
    ]


@pytest.mark.parametrize(
    ("scenario_id", "unexpected_path", "status_field"),
    (
        (
            "untracked-implementation-write-blocked",
            "workspace/implementation-repo/untracked.txt",
            "implementation_status",
        ),
        (
            "undeclared-planning-write-blocked",
            "workspace/planning-repo/undeclared.txt",
            "planning_status",
        ),
    ),
)
def test_repository_local_workspace_writes_fail_exact_scope_checks(
    tmp_path: Path, scenario_id: str, unexpected_path: str, status_field: str
) -> None:
    adapter = _load_adapter()
    scenario = _scenario(scenario_id)

    observation = adapter.run_scenario(
        scenario, FIXTURE_ROOT, tmp_path / "workspace"
    )
    outcome = _read_outcome(tmp_path)

    assert observation["writes"] == scenario["expected_writes"]
    assert outcome["boundary"] == "workspace_writes"
    assert outcome["evidence"]["unexpected_paths"] == [unexpected_path]
    assert outcome["evidence"][status_field]


def test_validation_codes_come_from_executed_checkpoints_not_expectations(
    tmp_path: Path,
) -> None:
    adapter = _load_adapter()
    scenario = dict(_scenario("protected-handoff-ready"))
    scenario["validation"] = ["expectation.must-not-be-copied"]

    observation = adapter.run_scenario(
        scenario, FIXTURE_ROOT, tmp_path / "workspace"
    )

    assert observation["validation"] == [
        "currentness.material-integrity.green",
        "currentness.fresh-lease.green",
        "currentness.write-scope.green",
        "currentness.lease-echo.green",
        "currentness.receipt.green",
        "currentness.commit-range.green",
        "currentness.reviewer-fresh-lease.green",
        "currentness.reviewer-receipt.green",
        "currentness.reviewer-lease-echo.green",
        "currentness.review-basis.green",
        "currentness.reconciliation.green",
        "currentness.workspace-writes.green",
    ]


def test_worker_lease_cannot_be_reused_for_reviewer_handoff(tmp_path: Path) -> None:
    adapter = _load_adapter()

    adapter.run_scenario(
        _scenario("reused-worker-reviewer-lease-blocked"),
        FIXTURE_ROOT,
        tmp_path / "workspace",
    )
    workspace = tmp_path / "workspace"
    worker = json.loads((workspace / "worker-result.json").read_text())
    commit = json.loads((workspace / "commit-evidence.json").read_text())
    reviewer_preparation = json.loads(
        (workspace / "reviewer-lease-preparation.json").read_text()
    )
    reviewer_receipt = json.loads(
        (workspace / "reviewer-lease-receipt.json").read_text()
    )
    reviewer = json.loads((workspace / "review-result.json").read_text())
    outcome = _read_outcome(tmp_path)

    assert worker["verified_context"]["implementation_commit_before"] == commit["base"]
    assert reviewer_preparation["payload"]["implementation_commit_before"] == commit[
        "head"
    ]
    assert reviewer_receipt["repository_revisions"][
        "implementation_commit_before"
    ] == commit["head"]
    assert reviewer["verified_context"] == worker["verified_context"]
    assert outcome["boundary"] == "reviewer_lease"
    assert outcome["evidence"]["reviewer_lease"] == reviewer_preparation["payload"]


def _scenario(scenario_id: str) -> Mapping[str, object]:
    validation = validate_catalog(FIXTURE_ROOT)
    assert validation.catalog is not None
    scenarios = cast(
        list[Mapping[str, object]], validation.catalog.document["scenarios"]
    )
    return next(scenario for scenario in scenarios if scenario["id"] == scenario_id)


def _load_adapter() -> ModuleType:
    path = FIXTURE_ROOT / "currentness_adapters.py"
    name = f"_currentness_adapter_test_{id(path)}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _read_outcome(tmp_path: Path) -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((tmp_path / "workspace" / "outcome.json").read_text()),
    )
