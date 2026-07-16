from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml
import pytest

from scripts.command_owner_scenarios import build_report, validate_catalog


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/command-owner-scenarios"
BOUND_FAMILIES = {
    "intake",
    "planning",
    "planning-fault-injection",
    "planning-quality",
    "execution",
    "commit-receipt-fault-injection",
    "closeout",
    "closeout-fault-injection",
    "contract-first-format",
}
CURRENTNESS_CONTRACTS = {
    "STATE-DIAG-001",
    "STATE-TRANSITION-002",
    "STATE-CANONICAL-003",
    "STATE-HISTORY-004",
}


def _document() -> dict[str, Any]:
    loaded = yaml.safe_load((FIXTURES / "catalog.yaml").read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _scenario(scenario_id: str) -> dict[str, Any]:
    return next(
        item for item in _document()["scenarios"] if item["id"] == scenario_id
    )


def _adapter_module() -> ModuleType:
    path = FIXTURES / "workflow_adapters.py"
    spec = importlib.util.spec_from_file_location("_workflow_scenario_adapters", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


@pytest.mark.command_owner_evidence
def test_workflow_catalog_keeps_slice_two_families_green() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    report = build_report(validation.catalog)
    families = {item["id"]: item["status"] for item in report["families"]}

    assert all(families[family] == "green" for family in BOUND_FAMILIES)
    assert report["status_counts"]["blocked"] == 0
    assert report["status_counts"]["bound"] == 0


def test_workflow_contracts_remain_green_after_later_scenario_bindings() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.catalog is not None

    report = build_report(validation.catalog)
    required = set(report["contracts"]["required"])
    green = set(report["contracts"]["green"])
    workflow_scenarios = [
        scenario
        for scenario in report["scenarios"]
        if scenario["family"] in BOUND_FAMILIES
    ]
    workflow_contracts = {
        contract for scenario in workflow_scenarios for contract in scenario["contracts"]
    }

    assert workflow_contracts == required - CURRENTNESS_CONTRACTS
    assert all(scenario["status"] == "green" for scenario in workflow_scenarios)
    assert workflow_contracts <= green
    assert report["acceptance"]["all_required_contracts_declared"] is True


@pytest.mark.command_owner_evidence
def test_planning_quality_scenarios_cover_semantic_scope_approval_and_drafts() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.catalog is not None
    report = build_report(validation.catalog)
    scenarios = {item["id"]: item for item in report["scenarios"]}

    expected_ids = {
        "quality-cohesive-single-slice",
        "quality-semantic-multi-slice",
        "quality-minimum-viable-scope",
        "quality-filler-split-blocked",
        "quality-expansion-blocked",
        "quality-residual-complexity-approved",
        "quality-residual-complexity-unapproved",
        "quality-independent-planner-reviewer",
        "quality-planner-reviewer-coupling-blocked",
        "quality-stale-draft-non-executable",
        "quality-undecided-draft-non-executable",
    }
    family_ids = {
        item["id"]
        for item in report["scenarios"]
        if item["family"] == "planning-quality"
    }

    assert family_ids == expected_ids
    assert all(scenarios[item]["status"] == "green" for item in expected_ids)
    assert _scenario("quality-residual-complexity-approved")["expected_writes"] == [
        "workspace/CURRENT.md",
        "workspace/approval-decision.json",
        "workspace/dispatch.md",
        "workspace/runway.md",
        "workspace/selection.md",
    ]
    assert _scenario("quality-stale-draft-non-executable")[
        "expected_writes"
    ] == []
    assert _scenario("quality-undecided-draft-non-executable")[
        "expected_writes"
    ] == []


def test_fixture_planner_and_reviewer_are_injected_called_and_observed_independently(
    tmp_path: Path,
) -> None:
    module = _adapter_module()
    scenario = _scenario("quality-independent-planner-reviewer")
    workspace = tmp_path / "workspace"
    direct_calls: list[str] = []

    def planner(request: dict[str, object]) -> dict[str, object]:
        direct_calls.append("planner")
        boundaries = list(request["requested_boundaries"])  # type: ignore[arg-type]
        return {
            "interface": "fixture-plan/v1",
            "slice_boundaries": boundaries,
            "semantic_reasons": [f"separate {item} responsibility" for item in boundaries],
        }

    def reviewer(request: dict[str, object]) -> dict[str, object]:
        direct_calls.append("reviewer")
        plan = request["plan"]
        assert isinstance(plan, dict)
        return {
            "interface": "fixture-plan-review/v1",
            "plan_digest": _digest(plan),
            "verdict": "accept",
            "semantic_boundaries_verified": True,
        }

    collaborators = module.PlanningCollaborators(planner=planner, reviewer=reviewer)
    observation = module.run_scenario(
        scenario,
        FIXTURES,
        workspace,
        planning_collaborators=collaborators,
    )
    invocations = json.loads((workspace / "role-invocations.json").read_text())
    planner_artifact = json.loads((workspace / "planner-result.json").read_text())
    reviewer_artifact = json.loads((workspace / "reviewer-result.json").read_text())

    assert observation["transition"] == "planning:queued"
    assert direct_calls == ["planner", "reviewer"]
    assert [item["role"] for item in invocations] == [
        "batch_planner",
        "batch_plan_reviewer",
    ]
    assert all(
        item["boundary"] == "injected-fixture-collaborator"
        for item in invocations
    )
    assert all(item["caller"] == "fixture-command-owner" for item in invocations)
    assert all(item["direct"] is True for item in invocations)
    assert all(len(item["request_digest"]) == 64 for item in invocations)
    assert set(planner_artifact) == {
        "interface",
        "semantic_reasons",
        "slice_boundaries",
    }
    assert reviewer_artifact["plan_digest"] == _digest(planner_artifact)
    assert reviewer_artifact["semantic_boundaries_verified"] is True


def test_fixture_plan_boundary_rejects_semantic_coupling_and_review_regressions(
    tmp_path: Path,
) -> None:
    module = _adapter_module()
    scenario = _scenario("quality-independent-planner-reviewer")

    def should_not_review(_request: dict[str, object]) -> dict[str, object]:
        raise AssertionError("reviewer must not run for a malformed planner result")

    def coupled_planner(request: dict[str, object]) -> dict[str, object]:
        boundaries = list(request["requested_boundaries"])  # type: ignore[arg-type]
        return {
            "interface": "fixture-plan/v1",
            "slice_boundaries": boundaries,
            "semantic_reasons": ["real boundary"],
            "review_evidence": {"verdict": "accept"},
        }

    coupled = module.run_scenario(
        scenario,
        FIXTURES,
        tmp_path / "coupled",
        planning_collaborators=module.PlanningCollaborators(
            planner=coupled_planner,
            reviewer=should_not_review,
        ),
    )

    def reasonless_planner(request: dict[str, object]) -> dict[str, object]:
        return {
            "interface": "fixture-plan/v1",
            "slice_boundaries": list(request["requested_boundaries"]),  # type: ignore[arg-type]
            "semantic_reasons": [],
        }

    reasonless = module.run_scenario(
        scenario,
        FIXTURES,
        tmp_path / "reasonless",
        planning_collaborators=module.PlanningCollaborators(
            planner=reasonless_planner,
            reviewer=should_not_review,
        ),
    )

    def valid_planner(request: dict[str, object]) -> dict[str, object]:
        boundaries = list(request["requested_boundaries"])  # type: ignore[arg-type]
        return {
            "interface": "fixture-plan/v1",
            "slice_boundaries": boundaries,
            "semantic_reasons": ["independent owner seam" for _ in boundaries],
        }

    def rejecting_reviewer(request: dict[str, object]) -> dict[str, object]:
        plan = request["plan"]
        assert isinstance(plan, dict)
        return {
            "interface": "fixture-plan-review/v1",
            "plan_digest": _digest(plan),
            "verdict": "reject",
            "semantic_boundaries_verified": True,
        }

    rejected = module.run_scenario(
        scenario,
        FIXTURES,
        tmp_path / "rejected",
        planning_collaborators=module.PlanningCollaborators(
            planner=valid_planner,
            reviewer=rejecting_reviewer,
        ),
    )

    assert coupled["transition"] == "planning:blocked"
    assert coupled["stop_reason"] == "planner and reviewer roles are not independent"
    assert reasonless["transition"] == "planning:blocked"
    assert reasonless["stop_reason"] == "planner output lacks semantic slice boundaries"
    assert rejected["transition"] == "planning:blocked"
    assert rejected["stop_reason"] == "independent plan review did not accept the plan"
    for name in ("coupled", "reasonless", "rejected"):
        assert not (tmp_path / name / "selection.md").exists()
        assert not (tmp_path / name / "runway.md").exists()


@pytest.mark.command_owner_evidence
def test_scenario_command_is_a_semantic_label_not_an_executable_dispatch(
    tmp_path: Path,
) -> None:
    module = _adapter_module()
    scenario = _scenario("intake-fresh-atomic")
    relabeled = copy.deepcopy(scenario)
    relabeled["command"] = "untrusted.label"

    original = module.run_scenario(scenario, FIXTURES, tmp_path / "original")
    observed = module.run_scenario(relabeled, FIXTURES, tmp_path / "relabeled")

    assert observed == original


@pytest.mark.command_owner_evidence
def test_public_store_scenarios_expose_atomic_recovery_and_no_successor_effects(
    tmp_path: Path,
) -> None:
    module = _adapter_module()
    cases = (
        "intake-fresh-atomic",
        "intake-multi-atomic",
        "intake-duplicate-idempotent",
        "intake-stale-blocked",
        "planning-partial-selection-resumes",
        "closeout-partial-write-resumes",
        "closeout-lost-batch-identity-blocked",
    )
    observations = {
        scenario_id: module.run_scenario(
            _scenario(scenario_id), FIXTURES, tmp_path / scenario_id
        )
        for scenario_id in cases
    }

    installed_owner = module.INSTALLED_INTAKE_OWNER
    assert installed_owner.is_symlink()
    assert installed_owner.resolve() == REPO_ROOT / "scripts/add_to_ledger.py"
    for scenario_id in (
        "intake-fresh-atomic",
        "intake-multi-atomic",
        "intake-duplicate-idempotent",
        "intake-stale-blocked",
    ):
        assert observations[scenario_id]["generation_and_roots"] == {
            "generation": "candidate-installed",
            "roots": [
                {"role": "workspace", "path": "workspace"},
                {
                    "role": "installed-owner",
                    "path": "installed/scripts/add_to_ledger.py",
                },
            ],
        }
        assert not {
            "CURRENT.md",
            "dispatch.md",
            "runway.md",
            "selection.md",
            "closeout.md",
        } & {
            path.name
            for path in (tmp_path / scenario_id).rglob("*")
            if path.is_file()
        }

    assert {
        "intake.create.green",
        "intake.update.green",
    } <= set(observations["intake-fresh-atomic"]["validation"])
    assert {
        "intake.plain-text-adapter.green",
        "intake.github-issue-adapter.green",
        "intake.multi-create.green",
    } <= set(observations["intake-multi-atomic"]["validation"])
    assert {
        "intake.exact-retry.green",
        "intake.semantic-no-op.green",
        "intake.identity-distinction.green",
    } <= set(observations["intake-duplicate-idempotent"]["validation"])
    assert {
        "intake.unsupported-block.green",
        "intake.ambiguous-block.green",
        "intake.stale-cas.green",
    } <= set(observations["intake-stale-blocked"]["validation"])
    assert observations["intake-duplicate-idempotent"]["writes"] == []
    assert observations["intake-stale-blocked"]["writes"] == []
    assert observations["planning-partial-selection-resumes"]["validation"] == [
        "planning.transaction.green",
        "planning.recovery.green",
        "planning.idempotence.green",
    ]
    assert observations["closeout-partial-write-resumes"]["stop_reason"] == (
        "same-batch closeout stops without successor selection"
    )
    assert observations["closeout-lost-batch-identity-blocked"]["writes"] == []
    assert not (tmp_path / "outside").exists()


def test_execution_review_commit_and_resume_are_observable_fixture_effects() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.catalog is not None
    report = build_report(validation.catalog)
    scenarios = {item["id"]: item for item in report["scenarios"]}

    for scenario_id in (
        "execution-validated-reviewed-committed",
        "execution-recovery-resumes-same-slice",
        "execution-review-blocks-commit",
        "commit-missing-receipt-blocked",
        "commit-unrelated-content-blocked",
        "closeout-same-batch-no-successor",
    ):
        assert scenarios[scenario_id]["status"] == "green"
        assert scenarios[scenario_id]["mismatches"] == []

    assert "workspace/commit-receipt.json" not in _scenario(
        "commit-missing-receipt-blocked"
    )["expected_writes"]
    assert _scenario("closeout-same-batch-no-successor")[
        "expected_stop_reason"
    ] == "same-batch closeout stops without successor selection"


def test_execution_state_machine_rejects_gate_receipt_scope_and_resume_regressions(
    tmp_path: Path,
) -> None:
    module = _adapter_module()
    complete = _scenario("execution-validated-reviewed-committed")
    recovery = _scenario("execution-recovery-resumes-same-slice")

    def worker(request: dict[str, object]) -> dict[str, object]:
        fixture_input = request["input"]
        assert isinstance(fixture_input, dict)
        return {
            "status": "success",
            "changed_paths": list(fixture_input["worker_paths"]),
        }

    def validator(_request: dict[str, object]) -> dict[str, object]:
        return {"status": "passed"}

    def reviewer(_request: dict[str, object]) -> dict[str, object]:
        return {"verdict": "accept", "scope": "workflow"}

    def committer(request: dict[str, object]) -> dict[str, object]:
        return {"commit": "f" * 40, "paths": list(request["worker_paths"])}

    commit_calls: list[str] = []

    def should_not_commit(_request: dict[str, object]) -> dict[str, object]:
        commit_calls.append("called")
        return {"commit": "f" * 40, "paths": ["allowed/workflow"]}

    review_blocked = module.run_scenario(
        complete,
        FIXTURES,
        tmp_path / "review-blocked",
        execution_collaborators=module.ExecutionCollaborators(
            worker=worker,
            validator=validator,
            reviewer=lambda _request: {"verdict": "fix", "scope": "workflow"},
            committer=should_not_commit,
        ),
    )

    invalid_receipt = module.run_scenario(
        complete,
        FIXTURES,
        tmp_path / "invalid-receipt",
        execution_collaborators=module.ExecutionCollaborators(
            worker=worker,
            validator=validator,
            reviewer=reviewer,
            committer=lambda request: {
                "commit": "not-a-commit",
                "paths": list(request["worker_paths"]),
            },
        ),
    )

    unrelated_receipt = module.run_scenario(
        complete,
        FIXTURES,
        tmp_path / "unrelated-receipt",
        execution_collaborators=module.ExecutionCollaborators(
            worker=worker,
            validator=validator,
            reviewer=reviewer,
            committer=lambda request: {
                "commit": "f" * 40,
                "paths": [*list(request["worker_paths"]), "unrelated/file"],
            },
        ),
    )

    downstream_calls: list[str] = []

    def should_not_validate(_request: dict[str, object]) -> dict[str, object]:
        downstream_calls.append("validator")
        return {"status": "passed"}

    scope_blocked = module.run_scenario(
        complete,
        FIXTURES,
        tmp_path / "scope-blocked",
        execution_collaborators=module.ExecutionCollaborators(
            worker=lambda _request: {
                "status": "success",
                "changed_paths": ["outside/worker-change"],
            },
            validator=should_not_validate,
            reviewer=reviewer,
            committer=committer,
        ),
    )

    resume_calls: list[str] = []

    def should_not_review(_request: dict[str, object]) -> dict[str, object]:
        resume_calls.append("reviewer")
        return {"verdict": "accept", "scope": "workflow"}

    resume_blocked = module.run_scenario(
        recovery,
        FIXTURES,
        tmp_path / "resume-blocked",
        execution_collaborators=module.ExecutionCollaborators(
            worker=worker,
            validator=lambda _request: {"status": "failed"},
            reviewer=should_not_review,
            committer=committer,
        ),
    )

    assert review_blocked["stop_reason"] == (
        "review requires an in-scope fix before commit"
    )
    assert commit_calls == []
    assert not (tmp_path / "review-blocked/commit-receipt.json").exists()
    assert invalid_receipt["transition"] == "commit:blocked"
    assert invalid_receipt["stop_reason"] == "commit receipt is invalid"
    assert unrelated_receipt["transition"] == "commit:blocked"
    assert unrelated_receipt["stop_reason"] == "commit contains unrelated content"
    assert scope_blocked["stop_reason"] == "worker result escapes the allowed scope"
    assert downstream_calls == []
    assert resume_blocked["stop_reason"] == "validation did not pass after resume"
    assert resume_calls == []
    assert (tmp_path / "resume-blocked/recovery-decision.json").is_file()
    assert not (tmp_path / "resume-blocked/commit-receipt.json").exists()
