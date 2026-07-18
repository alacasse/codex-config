"""Disposable behavioral adapters for command-owner scenario fixtures."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.planning_contract import (  # noqa: E402
    ArtifactLineage,
    InjectedStoreFailure,
    PlanningStoreError,
    ProducerIdentity,
    SelectionTransactionRequest,
    apply_current_document,
    apply_ledger_decision,
    read_current_document,
    read_ledger_document,
    simulate_selection_transaction,
    validate_planning_contracts,
    write_closeout_artifact,
)


COMMIT = "0123456789abcdef0123456789abcdef01234567"
EMPTY_HASH = hashlib.sha256(b"").hexdigest()
FORBIDDEN_WRITES = ["outside/canonical-planning", "outside/installed-home"]
CANDIDATE_CODEX_HOME = Path(
    os.environ.get(
        "COMMAND_OWNER_CANDIDATE_CODEX_HOME",
        "/home/alacasse/.codex-command-owner-redesign",
    )
)
CANONICAL_REPOSITORY_ROOT = Path(
    os.environ.get(
        "COMMAND_OWNER_CANONICAL_REPOSITORY_ROOT",
        "/home/alacasse/projects/codex-config",
    )
)
INSTALLED_INTAKE_OWNER = CANDIDATE_CODEX_HOME / "scripts/add_to_ledger.py"
INSTALLED_PLANNING_OWNER = CANDIDATE_CODEX_HOME / "scripts/plan_batch.py"
INSTALLED_PLANNING_CONTRACT = CANDIDATE_CODEX_HOME / "scripts/planning_contract.py"
PLANNING_OWNER_PROCESS_INVOCATIONS: list[Path] = []
PLANNING_SELECTION_FAULT_POINTS = (
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

FixtureCallable = Callable[[Mapping[str, object]], Mapping[str, object] | None]


@dataclass(frozen=True)
class PlanningCollaborators:
    """Separately injected fixture planner and reviewer boundaries."""

    planner: FixtureCallable
    reviewer: FixtureCallable


@dataclass(frozen=True)
class ExecutionCollaborators:
    """Injected execution collaborators consumed by the fixture state machine."""

    worker: FixtureCallable
    validator: FixtureCallable
    reviewer: FixtureCallable
    committer: FixtureCallable


@dataclass(frozen=True)
class PlanningBoundaryResult:
    plan: Mapping[str, object]
    review: Mapping[str, object] | None
    invocations: tuple[Mapping[str, object], ...]
    accepted: bool
    stop_reason: str | None


@dataclass(frozen=True)
class IntakeCaseResult:
    """One installed-owner intake observation."""

    transition: str
    writes: list[str]
    stop_reason: str | None
    validation: list[str]


def observe_intake(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    return _observe_family(scenario, fixture_root, "intake")


def observe_planning(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    return _observe_family(scenario, fixture_root, cast(str, scenario["family"]))


def observe_execution(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    return _observe_family(scenario, fixture_root, cast(str, scenario["family"]))


def observe_closeout(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    return _observe_family(scenario, fixture_root, cast(str, scenario["family"]))


def observe_contract_format(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    return _observe_family(scenario, fixture_root, "contract-first-format")


def run_scenario(
    scenario: Mapping[str, object],
    fixture_root: Path,
    workspace: Path,
    *,
    planning_collaborators: PlanningCollaborators | None = None,
    execution_collaborators: ExecutionCollaborators | None = None,
) -> Mapping[str, object]:
    """Run one fixture case in a caller-owned disposable workspace."""

    cases = _load_mapping(fixture_root / "workflow-cases.yaml")
    scenario_id = cast(str, scenario["id"])
    case = cast(Mapping[str, object], cases[scenario_id])
    operation = cast(str, case["operation"])
    workspace.mkdir(parents=True, exist_ok=True)
    if operation == "intake":
        intake = _run_intake(case, workspace, fixture_root)
        transition = intake.transition
        writes = intake.writes
        stop_reason = intake.stop_reason
        validation = intake.validation
        generation_and_roots = {
            "generation": "candidate-installed",
            "roots": [
                {"role": "workspace", "path": "workspace"},
                {"role": "installed-owner", "path": "installed/scripts/add_to_ledger.py"},
            ],
        }
    elif operation == "planning":
        transition, writes, stop_reason, validation = _run_planning(
            case,
            workspace,
            fixture_root,
            planning_collaborators=planning_collaborators,
        )
    elif operation == "execution":
        transition, writes, stop_reason, validation = _run_execution(
            case,
            workspace,
            collaborators=execution_collaborators,
        )
    elif operation == "closeout":
        transition, writes, stop_reason, validation = _run_closeout(
            case, workspace, fixture_root
        )
    elif operation == "contract-format":
        transition, writes, stop_reason, validation = _run_contract_format(
            workspace, fixture_root
        )
    else:
        raise ValueError(f"unsupported fixture operation {operation!r}")

    _assert_forbidden_paths_absent(workspace)
    return {
        "transition": transition,
        "writes": writes,
        "forbidden_writes": FORBIDDEN_WRITES,
        "stop_reason": stop_reason,
        "generation_and_roots": generation_and_roots
        if operation == "intake"
        else {
            "generation": "fixture",
            "roots": [{"role": "workspace", "path": "workspace"}],
        },
        "validation": validation,
    }


def _observe_family(
    scenario: Mapping[str, object], fixture_root: Path, expected_family: str
) -> Mapping[str, object]:
    if scenario["family"] != expected_family:
        raise ValueError(
            f"adapter expected family {expected_family!r}; got {scenario['family']!r}"
        )
    with tempfile.TemporaryDirectory(prefix="command-owner-scenario-") as directory:
        return run_scenario(scenario, fixture_root, Path(directory) / "workspace")


def _run_intake(
    case: Mapping[str, object], workspace: Path, fixture_root: Path
) -> IntakeCaseResult:
    repo_root = _repo_root(fixture_root)
    owner_path = _require_installed_intake_owner(repo_root)
    ledger_path = workspace / "LEDGER.md"
    shutil.copy2(
        repo_root / "tests/fixtures/planning-contracts/ledger/per-finding-valid/LEDGER.md",
        ledger_path,
    )
    canonical_before = _snapshot(CANONICAL_REPOSITORY_ROOT / "docs/plans")
    mode = cast(str, case["mode"])
    if mode == "create-update":
        result = _run_intake_create_update(repo_root, ledger_path, workspace)
    elif mode == "multi-create":
        result = _run_intake_multi_create(repo_root, ledger_path, workspace)
    elif mode == "exact-retry-and-semantic-no-op":
        result = _run_intake_retry_and_no_op(repo_root, ledger_path, workspace)
    elif mode == "blocked-matrix":
        result = _run_intake_blocked_matrix(repo_root, ledger_path, workspace)
    else:
        raise AssertionError(f"unsupported intake fixture mode {mode!r}")
    if _snapshot(CANONICAL_REPOSITORY_ROOT / "docs/plans") != canonical_before:
        raise AssertionError("candidate-installed intake mutated canonical planning state")
    _assert_no_downstream_intake_effects(workspace)
    assert owner_path.resolve() == repo_root / "scripts/add_to_ledger.py"
    return result


def _run_intake_create_update(
    repo_root: Path, ledger_path: Path, workspace: Path
) -> IntakeCaseResult:
    created = _invoke_installed_intake_owner(
        _intake_request(
            repo_root,
            workspace,
            ledger_path,
            [_plain_intake_input("fixture create-update", title="Initial intake")],
        )
    )
    before = _snapshot(workspace)
    updated = _invoke_installed_intake_owner(
        _intake_request(
            repo_root,
            workspace,
            ledger_path,
            [
                _plain_intake_input(
                    "fixture create-update",
                    title="Updated intake",
                    evidence=["evidence/updated.md"],
                )
            ],
        )
    )
    after = read_ledger_document(ledger_path, toolchain_root=repo_root)
    finding_id = cast(str, cast(list[dict[str, object]], created["inputs"])[0]["finding_id"])
    assert created["outcome"] == "applied"
    assert cast(list[dict[str, object]], created["inputs"])[0]["action"] == "create"
    assert updated["outcome"] == "applied"
    assert cast(list[dict[str, object]], updated["inputs"])[0]["action"] == "update"
    assert after.findings[finding_id]["title"] == "Updated intake"
    return IntakeCaseResult(
        transition="intake:recorded",
        writes=_changed_paths(before, workspace),
        stop_reason="intake stops before planning",
        validation=[
            "ledger.store.green",
            "intake.installed-owner.green",
            "intake.create.green",
            "intake.update.green",
            "intake.atomicity.green",
            "intake.stop.green",
        ],
    )


def _run_intake_multi_create(
    repo_root: Path, ledger_path: Path, workspace: Path
) -> IntakeCaseResult:
    plain_text = "fixture plain source"
    plain_digest = "e2df174b180787401cf4e43aaa3ef36937400f6ede438b0a53c04fb21df2e697"
    github_revision_inputs = {
        "owner": "openai",
        "repository": "codex",
        "number": 42,
        "title": "Reproducible issue",
        "body": "Fixture issue body.",
    }
    github_digest = "7bd6323b3edeb32ae2b83aa2f982b83d8ab9ff15338cc37136184a3c1b68e382"
    assert hashlib.sha256(plain_text.encode()).hexdigest() == plain_digest
    assert hashlib.sha256(
        json.dumps(
            github_revision_inputs,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    ).hexdigest() == github_digest
    before = _snapshot(workspace)
    result = _invoke_installed_intake_owner(
        _intake_request(
            repo_root,
            workspace,
            ledger_path,
            [
                _plain_intake_input(plain_text, title="Plain intake"),
                _github_intake_input(),
            ],
        )
    )
    inputs = cast(list[dict[str, object]], result["inputs"])
    source_identities = [cast(str, item["source_identity"]) for item in inputs]
    after = read_ledger_document(ledger_path, toolchain_root=repo_root)
    assert result["outcome"] == "applied"
    assert [item["action"] for item in inputs] == ["create", "create"]
    assert source_identities[0].startswith("text:sha256:")
    assert source_identities[1] == "github-issue:github.com/openai/codex#42"
    assert cast(dict[str, object], result["store"])["outcome"] == "applied"
    assert all(cast(str, item["finding_id"]) in after.findings for item in inputs)
    plain_finding = after.findings[cast(str, inputs[0]["finding_id"])]
    github_finding = after.findings[cast(str, inputs[1]["finding_id"])]
    assert plain_finding["provenance"] == {
        "source_id": f"text:sha256:{plain_digest}",
        "source_commit": plain_digest[:40],
        "source_section": "inline-text",
    }
    assert github_finding["provenance"] == {
        "source_id": "github-issue:github.com/openai/codex#42",
        "source_commit": github_digest[:40],
        "source_section": "https://github.com/openai/codex/issues/42",
    }
    return IntakeCaseResult(
        transition="intake:recorded",
        writes=_changed_paths(before, workspace),
        stop_reason="intake stops before planning",
        validation=[
            "ledger.store.green",
            "intake.installed-owner.green",
            "intake.plain-text-adapter.green",
            "intake.github-issue-adapter.green",
            "intake.multi-create.green",
            "intake.atomicity.green",
            "intake.stop.green",
        ],
    )


def _run_intake_retry_and_no_op(
    repo_root: Path, ledger_path: Path, workspace: Path
) -> IntakeCaseResult:
    request = _intake_request(
        repo_root,
        workspace,
        ledger_path,
        [_plain_intake_input("fixture retry source", title="Retry intake")],
    )
    owner = _canonical_intake_owner_module(repo_root)
    prepared = owner._prepare_operation(request)
    try:
        owner._apply_prepared_operation(
            prepared, fault="after_replace_before_return"
        )
    except InjectedStoreFailure:
        pass
    else:
        raise AssertionError("installed owner did not expose interrupted apply")
    before = _snapshot(workspace)
    replay = owner._apply_prepared_operation(prepared)
    semantic = _invoke_installed_intake_owner(request)
    assert replay["outcome"] == "exact_replay"
    assert replay["write_status"] == "exact_replay"
    assert replay["private_operation_digest"] is not None
    assert semantic["outcome"] == "no-op"
    assert semantic["write_status"] == "not_written"
    assert semantic["private_operation_digest"] is None
    return IntakeCaseResult(
        transition="intake:replayed",
        writes=_changed_paths(before, workspace),
        stop_reason="intake stops after the existing finding is confirmed",
        validation=[
            "ledger.store.green",
            "intake.installed-owner.green",
            "intake.exact-retry.green",
            "intake.semantic-no-op.green",
            "intake.identity-distinction.green",
            "intake.stop.green",
        ],
    )


def _run_intake_blocked_matrix(
    repo_root: Path, ledger_path: Path, workspace: Path
) -> IntakeCaseResult:
    unsupported = _plain_intake_input("fixture unsupported", title="Unsupported")
    unsupported["source"] = {"type": "external_ticket", "id": "EXT-1"}
    before_unsupported = ledger_path.read_bytes()
    unsupported_result = _invoke_installed_intake_owner(
        _intake_request(
            repo_root,
            workspace,
            ledger_path,
            [
                _plain_intake_input("fixture valid sibling", title="Valid sibling"),
                unsupported,
            ],
        )
    )
    assert unsupported_result["outcome"] == "blocked"
    assert unsupported_result["write_status"] == "not_written"
    assert unsupported_result["affected_finding_ids"] == []
    assert unsupported_result["store"] is None
    assert [
        item["code"]
        for item in cast(list[dict[str, object]], unsupported_result["blockers"])
    ] == ["source.unsupported"]
    assert ledger_path.read_bytes() == before_unsupported

    ambiguous_result = _invoke_installed_intake_owner(
        _intake_request(
            repo_root,
            workspace,
            ledger_path,
            [
                _plain_intake_input("fixture ambiguous", title="First meaning"),
                _plain_intake_input("fixture ambiguous", title="Second meaning"),
            ],
        )
    )
    assert ambiguous_result["outcome"] == "blocked"
    assert ambiguous_result["write_status"] == "not_written"
    assert ambiguous_result["affected_finding_ids"] == []
    assert ambiguous_result["store"] is None
    assert [
        item["code"]
        for item in cast(list[dict[str, object]], ambiguous_result["blockers"])
    ] == ["input.duplicate_source_conflict"]
    assert ledger_path.read_bytes() == before_unsupported

    owner = _canonical_intake_owner_module(repo_root)
    stale_request = _intake_request(
        repo_root,
        workspace,
        ledger_path,
        [_plain_intake_input("fixture stale", title="Stale intake")],
    )
    prepared = owner._prepare_operation(stale_request)
    concurrent = _invoke_installed_intake_owner(
        _intake_request(
            repo_root,
            workspace,
            ledger_path,
            [_plain_intake_input("fixture concurrent", title="Concurrent intake")],
        )
    )
    assert concurrent["outcome"] == "applied"
    before_stale = _snapshot(workspace)
    before_stale_bytes = ledger_path.read_bytes()
    stale = owner._apply_prepared_operation(prepared)
    blocker_codes = [
        cast(str, item["code"])
        for item in cast(list[dict[str, object]], stale["blockers"])
    ]
    assert stale["outcome"] == "blocked"
    assert stale["write_status"] == "not_written"
    assert stale["affected_finding_ids"] == []
    assert stale["store"] is None
    assert any(code.endswith("revision_mismatch") for code in blocker_codes)
    assert ledger_path.read_bytes() == before_stale_bytes
    return IntakeCaseResult(
        transition="intake:blocked",
        writes=_changed_paths(before_stale, workspace),
        stop_reason="stale intake revision",
        validation=[
            "ledger.store.green",
            "intake.installed-owner.green",
            "intake.unsupported-block.green",
            "intake.ambiguous-block.green",
            "intake.stale-cas.green",
            "intake.atomicity.green",
            "intake.stop.green",
        ],
    )


def _require_installed_intake_owner(repo_root: Path) -> Path:
    expected = (repo_root / "scripts/add_to_ledger.py").resolve(strict=True)
    expected_store = (repo_root / "scripts/planning_contract.py").resolve(strict=True)
    if not INSTALLED_INTAKE_OWNER.is_symlink():
        raise AssertionError(f"installed intake owner is not a link: {INSTALLED_INTAKE_OWNER}")
    if INSTALLED_INTAKE_OWNER.resolve(strict=True) != expected:
        raise AssertionError("installed intake owner does not resolve to candidate source")
    if not INSTALLED_PLANNING_CONTRACT.is_symlink():
        raise AssertionError(
            f"installed planning contract is not a link: {INSTALLED_PLANNING_CONTRACT}"
        )
    if INSTALLED_PLANNING_CONTRACT.resolve(strict=True) != expected_store:
        raise AssertionError(
            "installed planning contract does not resolve to candidate source"
        )
    return INSTALLED_INTAKE_OWNER


def _canonical_intake_owner_module(repo_root: Path) -> Any:
    path = _require_installed_intake_owner(repo_root)
    expected = path.resolve(strict=True)
    cached = sys.modules.get("scripts.add_to_ledger")
    if cached is not None:
        cached_path = Path(cast(str, getattr(cached, "__file__", ""))).resolve()
        if cached_path != expected:
            raise ImportError(
                f"cached scripts.add_to_ledger resolves to {cached_path}, expected {expected}"
            )
    module = importlib.import_module("scripts.add_to_ledger")
    if Path(cast(str, module.__file__)).resolve() != expected:
        raise ImportError("canonical intake owner module has foreign provenance")
    store = importlib.import_module("scripts.planning_contract")
    if Path(cast(str, store.__file__)).resolve() != (
        repo_root / "scripts/planning_contract.py"
    ).resolve():
        raise ImportError("canonical planning store module has foreign provenance")
    if module.apply_ledger_decision is not store.apply_ledger_decision:
        raise ImportError("canonical intake owner does not use canonical planning store")
    return module


def _invoke_installed_intake_owner(request: Mapping[str, object]) -> dict[str, object]:
    repo_root = Path(cast(str, cast(Mapping[str, object], request["context"])["toolchain_root"]))
    owner_path = _require_installed_intake_owner(repo_root)
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONHOME", "PYTHONPATH"}
    }
    env["PYTHONSAFEPATH"] = "1"
    process = subprocess.run(
        [sys.executable, "-P", str(owner_path)],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    if process.returncode != 0 or process.stderr:
        raise AssertionError(
            f"installed intake owner failed: {process.returncode}: {process.stderr}"
        )
    loaded = json.loads(process.stdout)
    if not isinstance(loaded, dict):
        raise AssertionError("installed intake owner returned a non-object")
    return cast(dict[str, object], loaded)


def _intake_request(
    repo_root: Path,
    planning_root: Path,
    ledger_path: Path,
    inputs: list[dict[str, object]],
) -> dict[str, object]:
    candidate_head = subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True
    ).strip()
    canonical_head = subprocess.check_output(
        ["git", "-C", str(CANONICAL_REPOSITORY_ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    return {
        "interface": "add-to-ledger/v1",
        "context": {
            "toolchain_generation": "candidate",
            "toolchain_commit": candidate_head,
            "toolchain_root": str(repo_root),
            "canonical_planning_repository_root": str(CANONICAL_REPOSITORY_ROOT),
            "canonical_planning_commit": canonical_head,
            "planning_root": str(planning_root),
            "ledger_path": str(ledger_path),
            "operation_root_kind": "fixture",
            "canonical_state_mutation_allowed": False,
            "project_namespace": None,
        },
        "inputs": inputs,
    }


def _plain_intake_input(
    text: str,
    *,
    title: str,
    evidence: list[str] | None = None,
) -> dict[str, object]:
    return {
        "source": {"type": "plain_text", "text": text},
        "title": title,
        "scope": {
            "summary": "Bounded fixture intake",
            "included": ["installed owner behavior"],
            "excluded": ["downstream planning"],
        },
        "evidence_pointers": evidence or [],
        "next_action": {"command": "plan-batch", "condition": "explicit_request"},
        "explicit_target_finding_id": None,
        "non_intake_changes": [],
    }


def _github_intake_input() -> dict[str, object]:
    value = _plain_intake_input(
        "unused GitHub transport placeholder", title="GitHub issue intake"
    )
    value["source"] = {
        "type": "github_issue",
        "owner": "OpenAI",
        "repository": "Codex",
        "number": 42,
        "title": "Reproducible issue",
        "body": "Fixture issue body.",
    }
    return value


def _assert_no_downstream_intake_effects(workspace: Path) -> None:
    forbidden = {
        "CURRENT.md",
        "dispatch.md",
        "runway.md",
        "selection.md",
        "closeout.md",
    }
    present = {path.name for path in workspace.rglob("*") if path.is_file()}
    if present & forbidden:
        raise AssertionError(f"intake produced downstream effects: {sorted(present & forbidden)}")


def _run_planning(
    case: Mapping[str, object],
    workspace: Path,
    fixture_root: Path,
    *,
    planning_collaborators: PlanningCollaborators | None,
) -> tuple[str, list[str], str | None, list[str]]:
    repo_root = _repo_root(fixture_root)
    request = _selection_workspace(workspace, repo_root, case)
    mode = cast(str, case["mode"])
    if mode == "guard" and case.get("existing_state") is not None:
        _seed_existing_state(request, case, repo_root)
    before = _snapshot(workspace)
    boundary: PlanningBoundaryResult | None = None
    if mode == "roles":
        collaborators = planning_collaborators or _planning_collaborators(case)
        boundary = _evaluate_planning_boundary(case, collaborators)
        if boundary.accepted:
            assert boundary.review is not None
            _write_json(workspace / "planner-result.json", boundary.plan)
            _write_json(workspace / "reviewer-result.json", boundary.review)
            _write_json(
                workspace / "role-invocations.json", list(boundary.invocations)
            )
    if cast(bool, case.get("residual_complexity", False)):
        approval = case.get("approval")
        if isinstance(approval, Mapping):
            _write_json(
                workspace / "approval-decision.json",
                dict(cast(Mapping[str, object], approval)),
            )
    owner_request = _planning_owner_request(
        request,
        case,
        repo_root,
        boundary=boundary,
    )
    if mode == "recover":
        try:
            _invoke_installed_planning_owner(
                owner_request,
                repo_root,
                fault="after_idle_to_selected_cas_before_receipt",
            )
        except RuntimeError:
            pass
        else:
            raise AssertionError("selection fault was not injected")
        _refresh_planning_owner_state(owner_request, request, repo_root)
        result = _invoke_installed_planning_owner(owner_request, repo_root)
        _refresh_planning_owner_state(owner_request, request, repo_root)
        replay = _invoke_installed_planning_owner(owner_request, repo_root)
        assert result["outcome"] == "queued"
        replay_transaction = cast(Mapping[str, object], replay["transaction"])
        assert replay_transaction["outcome"] == "exact_replay"
        validation = [
            "planning.transaction.green",
            "planning.recovery.green",
            "planning.idempotence.green",
            "planning.installed-owner.green",
        ]
    else:
        result = _invoke_installed_planning_owner(owner_request, repo_root)
        if result["outcome"] == "blocked":
            stop_reason = (
                boundary.stop_reason
                if boundary is not None and not boundary.accepted
                else _planning_stop_reason(case, request, repo_root)
            )
            if stop_reason is None:
                blockers = cast(list[Mapping[str, object]], result["blockers"])
                stop_reason = cast(str, blockers[0]["message"])
            blocked_validation = [
                "planning.guard.green",
                "planning.no-queue-mutation.green",
                "planning.installed-owner.green",
            ]
            if case.get("vertical_case") is not None:
                blocked_validation.append("planning.vertical-contract.green")
            return (
                "planning:blocked",
                _changed_paths(before, workspace),
                stop_reason,
                blocked_validation,
            )
        assert result["outcome"] == "queued"
        validation = [
            "planning.transaction.green",
            "planning.quality.green",
            "planning.installed-owner.green",
        ]
        if mode == "roles":
            validation.append("planning.fixture-role-boundary.green")
        if cast(bool, case.get("residual_complexity", False)):
            validation.append("planning.approval-scoped.green")
        if case.get("vertical_case") is not None:
            validation.append("planning.vertical-contract.green")
    current = read_current_document(request.current_path, toolchain_root=repo_root)
    assert current.contract["queued_runway"] == "runway.md"
    assert current.contract["selected_dispatch"] is None
    return (
        "planning:queued",
        _changed_paths(before, workspace),
        "planning stops before implementation",
        validation,
    )


def exercise_repeated_planning_correction(
    workspace: Path, fixture_root: Path
) -> Mapping[str, object]:
    """Exercise the installed owner's unchanged-draft correction-loop stop."""

    workspace.mkdir(parents=True, exist_ok=True)
    repo_root = _repo_root(fixture_root)
    transaction = _selection_workspace(
        workspace,
        repo_root,
        {"slice_boundaries": ["owner-seam"]},
    )
    owner_request = _planning_owner_request(
        transaction,
        {"slice_boundaries": ["owner-seam"]},
        repo_root,
        boundary=None,
    )
    correction = "narrow the owner seam"
    reviewer_result = cast(dict[str, object], owner_request["reviewer_result"])
    reviewer_result["verdict"] = "correction_required"
    reviewer_result["corrections"] = [correction]
    draft = cast(
        Mapping[str, object],
        cast(Mapping[str, object], owner_request["planner_result"])["draft"],
    )
    owner_request["correction_history"] = [
        {
            "draft_sha256": _mapping_digest(draft),
            "correction": correction,
            "material": True,
        }
    ]
    _refresh_planning_review_evidence(owner_request)
    before = _snapshot(workspace)
    result = _invoke_installed_planning_owner(owner_request, repo_root)
    return {
        "result": result,
        "writes": _changed_paths(before, workspace),
        "planner_invocation": _thaw(owner_request["planner_invocation"]),
        "reviewer_invocation": _thaw(owner_request["reviewer_invocation"]),
    }


def exercise_planning_recovery_fault(
    workspace: Path,
    fixture_root: Path,
    fault: str,
) -> Mapping[str, object]:
    """Exercise one installed-owner recovery without manufacturing a rereview."""

    if fault not in PLANNING_SELECTION_FAULT_POINTS:
        raise AssertionError(f"unsupported planning selection fault: {fault}")
    workspace.mkdir(parents=True, exist_ok=True)
    repo_root = _repo_root(fixture_root)
    transaction = _selection_workspace(
        workspace,
        repo_root,
        {"slice_boundaries": ["recovery"]},
    )
    owner_request = _planning_owner_request(
        transaction,
        {"slice_boundaries": ["recovery"]},
        repo_root,
        boundary=None,
    )
    original_lineage = _planning_review_lineage_snapshot(owner_request)

    try:
        _invoke_installed_planning_owner(owner_request, repo_root, fault=fault)
    except RuntimeError:
        pass
    else:
        raise AssertionError("selection fault was not injected")
    assert _planning_review_lineage_snapshot(owner_request) == original_lineage

    _refresh_planning_owner_state(owner_request, transaction, repo_root)
    assert _planning_review_lineage_snapshot(owner_request) == original_lineage
    resumed = _invoke_installed_planning_owner(owner_request, repo_root)
    assert _planning_review_lineage_snapshot(owner_request) == original_lineage
    completed = _snapshot(workspace)

    _refresh_planning_owner_state(owner_request, transaction, repo_root)
    assert _planning_review_lineage_snapshot(owner_request) == original_lineage
    replayed = _invoke_installed_planning_owner(owner_request, repo_root)
    assert _planning_review_lineage_snapshot(owner_request) == original_lineage
    assert _snapshot(workspace) == completed

    resumed_transaction = cast(Mapping[str, object], resumed["transaction"])
    replayed_transaction = cast(Mapping[str, object], replayed["transaction"])
    return {
        "resumed_outcome": resumed["outcome"],
        "resumed_transaction_outcome": resumed_transaction["outcome"],
        "replayed_outcome": replayed["outcome"],
        "replayed_transaction_outcome": replayed_transaction["outcome"],
        "review_lineage_sha256": hashlib.sha256(original_lineage).hexdigest(),
        "review_lineage_immutable": True,
    }


def _planning_review_lineage_snapshot(owner_request: Mapping[str, object]) -> bytes:
    return json.dumps(
        {
            "review_evidence": owner_request["review_evidence"],
            "reviewer_invocation": owner_request["reviewer_invocation"],
            "reviewer_result": owner_request["reviewer_result"],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()


def _require_installed_planning_owner(repo_root: Path) -> Path:
    expected = (repo_root / "scripts/plan_batch.py").resolve(strict=True)
    if not INSTALLED_PLANNING_OWNER.is_symlink():
        raise AssertionError(
            f"installed planning owner is not a link: {INSTALLED_PLANNING_OWNER}"
        )
    if INSTALLED_PLANNING_OWNER.resolve(strict=True) != expected:
        raise AssertionError("installed planning owner does not resolve to candidate source")
    if not INSTALLED_PLANNING_CONTRACT.is_symlink():
        raise AssertionError("installed planning contract is not a link")
    if INSTALLED_PLANNING_CONTRACT.resolve(strict=True) != (
        repo_root / "scripts/planning_contract.py"
    ).resolve(strict=True):
        raise AssertionError("installed planning contract has foreign provenance")
    return INSTALLED_PLANNING_OWNER


def _canonical_planning_owner_module(repo_root: Path) -> Any:
    expected = _require_installed_planning_owner(repo_root).resolve(strict=True)
    module = importlib.import_module("scripts.plan_batch")
    if Path(cast(str, module.__file__)).resolve(strict=True) != expected:
        raise ImportError("canonical planning owner module has foreign provenance")
    store = importlib.import_module("scripts.planning_contract")
    expected_store = INSTALLED_PLANNING_CONTRACT.resolve(strict=True)
    if Path(cast(str, store.__file__)).resolve(strict=True) != expected_store:
        raise ImportError("canonical planning store module has foreign provenance")
    if module.simulate_selection_transaction is not store.simulate_selection_transaction:
        raise ImportError("canonical planning owner does not use canonical planning store")
    return module


def _invoke_installed_planning_owner(
    request: Mapping[str, object],
    repo_root: Path,
    *,
    fault: str | None = None,
) -> dict[str, object]:
    if fault is None:
        owner_path = _require_installed_planning_owner(repo_root)
        PLANNING_OWNER_PROCESS_INVOCATIONS.append(owner_path)
        process = subprocess.run(
            [sys.executable, "-P", str(owner_path)],
            input=json.dumps(request),
            text=True,
            capture_output=True,
            check=False,
        )
        if process.returncode != 0 or process.stderr:
            raise AssertionError(
                "installed planning owner process failed: "
                f"returncode={process.returncode}; stderr={process.stderr!r}"
            )
        result = json.loads(process.stdout)
        if not isinstance(result, dict):
            raise AssertionError("installed planning owner returned non-object JSON")
        return cast(dict[str, object], result)
    owner = _canonical_planning_owner_module(repo_root)
    return cast(dict[str, object], owner.execute_plan_batch(request, fault=fault))


def _planning_owner_request(
    request: SelectionTransactionRequest,
    case: Mapping[str, object],
    repo_root: Path,
    *,
    boundary: PlanningBoundaryResult | None,
) -> dict[str, object]:
    current = read_current_document(request.current_path, toolchain_root=repo_root)
    commit = subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True
    ).strip()
    canonical_commit = subprocess.check_output(
        ["git", "-C", str(CANONICAL_REPOSITORY_ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    draft = _planning_draft(request, case, boundary=boundary)
    planner_status = "ready" if boundary is None or boundary.accepted else "blocked"
    planner_blockers = (
        []
        if planner_status == "ready"
        else [cast(str, boundary.stop_reason)]
    )
    approvals = []
    approval = case.get("approval")
    if isinstance(approval, Mapping):
        approvals.append(dict(cast(Mapping[str, object], approval)))
    owner_request: dict[str, object] = {
        "interface": "plan-batch/v1",
        "context": {
            "toolchain_generation": "candidate",
            "toolchain_commit": commit,
            "toolchain_root": str(repo_root),
            "canonical_planning_repository_root": str(CANONICAL_REPOSITORY_ROOT),
            "canonical_planning_commit": canonical_commit,
            "planning_root": str(request.lineage.planning_root),
            "operation_root_kind": "fixture",
            "canonical_state_mutation_allowed": False,
        },
        "planning_state": _planning_state_payload(current),
        "planner_invocation": {
            "role": "batch_planner",
            "caller": "plan-batch",
            "direct": True,
            "invocation_id": "fixture-planner",
        },
        "planner_result": {
            "interface": "batch-plan-draft/v1",
            "status": planner_status,
            "draft": draft if planner_status == "ready" else None,
            "blockers": planner_blockers,
        },
        "reviewer_invocation": {
            "role": "batch_plan_reviewer",
            "caller": "plan-batch",
            "direct": True,
            "invocation_id": "fixture-reviewer",
        },
        "reviewer_result": {
            "interface": "batch-plan-review/v1",
            "verdict": "clean",
            "review_basis": {
                "selected_dispatch_sha256": "0" * 64,
                "draft_sha256": "0" * 64,
                "approvals_sha256": "0" * 64,
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
        "approvals": approvals,
        "review_evidence": {},
        "validation_catalog": ["project-harness-production"],
        "correction_history": [],
        "transaction": _selection_transaction_payload(request),
    }
    if planner_status == "ready":
        _refresh_planning_review_evidence(owner_request)
    return owner_request


def _planning_draft(
    request: SelectionTransactionRequest,
    case: Mapping[str, object],
    *,
    boundary: PlanningBoundaryResult | None,
) -> dict[str, object]:
    slices = cast(list[Mapping[str, object]], request.runway_contract["slices"])
    reasons = (
        cast(list[str], boundary.plan["semantic_reasons"])
        if boundary is not None and boundary.accepted
        else [f"separate {item['id']} responsibility" for item in slices]
    )
    rationales = [
        {
            "slice_id": cast(str, item["id"]),
            "kind": "cohesive" if len(slices) == 1 else "producer-consumer",
            "reason": reason,
        }
        for item, reason in zip(slices, reasons, strict=True)
    ]
    if case.get("semantic_boundaries") is False:
        rationales[0]["kind"] = "filler"
    quality: dict[str, object] = {
        "minimum_viable_scope": case.get("scope_quality") != "vague",
        "scope_expansions": (
            [] if case.get("scope_expansion") is None else [case["scope_expansion"]]
        ),
        "proportionality": {
            "observed_failure": "planning behavior lacks one installed owner proof",
            "invariants": [
                "queue one reviewed finding",
                "stop before implementation",
            ],
            "minimum_viable_change": "validate and queue one reviewed draft",
            "proposed_change": "validate and queue one reviewed draft",
            "additions_beyond_minimum": [],
            "simpler_alternatives_rejected": [
                {
                    "alternative": "retain fixture-only planning",
                    "reason": "it does not prove the installed owner boundary",
                }
            ],
            "verdict": "proportionate",
        },
        "slice_rationales": rationales,
        "unresolved_decisions": (
            ["fixture user decision"] if case.get("draft_state") == "undecided" else []
        ),
        "residual_complexity": (
            [
                {
                    "id": "fixture-complexity",
                    "scope": "fixture-batch:dependency-and-validation-seams",
                }
            ]
            if cast(bool, case.get("residual_complexity", False))
            else []
        ),
        "destructive_actions": (
            [{"id": "fixture-destruction", "scope": "fixture-batch:destructive"}]
            if cast(bool, case.get("destructive", False))
            else []
        ),
        "implementation_started": False,
    }
    return {
        "dispatch": _thaw(request.dispatch_contract),
        "runway": _thaw(request.runway_contract),
        "basis": {
            "current_revision": request.expected_initial_state_revision,
            "current_file_hash": request.expected_initial_state_file_hash,
            "ledger_path": str(request.lineage.ledger_path),
            "ledger_file_hash": (
                "0" * 64
                if case.get("draft_state") == "stale"
                else _hash(request.lineage.ledger_path)
            ),
            "finding_id": request.lineage.included_finding_ids[0],
            "finding_revision": 1,
        },
        "quality": quality,
        "validation_profile": "project-harness-production",
    }


def _planning_state_payload(current: Any) -> dict[str, object]:
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


def _refresh_planning_owner_state(
    owner_request: dict[str, object],
    request: SelectionTransactionRequest,
    repo_root: Path,
) -> None:
    owner_request["planning_state"] = _planning_state_payload(
        read_current_document(request.current_path, toolchain_root=repo_root)
    )


def _refresh_planning_review_evidence(owner_request: dict[str, object]) -> None:
    planner_result = cast(dict[str, object], owner_request["planner_result"])
    draft = cast(dict[str, object], planner_result["draft"])
    quality = cast(dict[str, object], draft["quality"])
    source_content = "Authoritative scenario source evidence for CCFG-1."
    planning_state = cast(dict[str, object], owner_request["planning_state"])
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
            "current_sha256": _value_digest(
                {"command": "current", "planning_state": planning_state}
            ),
            "validate_sha256": _value_digest(
                {"command": "validate", "planning_state": planning_state}
            ),
        },
        "proportionality": _thaw(quality["proportionality"]),
        "approvals": _thaw(owner_request["approvals"]),
        "draft": _thaw(draft),
        "selected_dispatch": _thaw(draft["dispatch"]),
        "invocation_lineage": {
            "planner": _thaw(owner_request["planner_invocation"]),
            "reviewer": _thaw(owner_request["reviewer_invocation"]),
        },
    }
    packet_sha256 = _mapping_digest(packet)
    owner_request["review_evidence"] = {
        "packet": packet,
        "packet_sha256": packet_sha256,
    }
    reviewer_result = cast(dict[str, object], owner_request["reviewer_result"])
    reviewer_result["review_basis"] = {
        "selected_dispatch_sha256": _mapping_digest(
            cast(Mapping[str, object], draft["dispatch"])
        ),
        "draft_sha256": _mapping_digest(draft),
        "approvals_sha256": _value_digest(owner_request["approvals"]),
        "evidence_packet_sha256": packet_sha256,
    }


def _selection_transaction_payload(
    request: SelectionTransactionRequest,
) -> dict[str, object]:
    lineage = request.lineage

    def producer(value: ProducerIdentity) -> dict[str, str]:
        return {
            "toolchain_generation": value.toolchain_generation,
            "toolchain_commit": value.toolchain_commit,
            "schema_version": value.schema_version,
        }
    return {
        "transaction_id": request.transaction_id,
        "transaction_path": str(request.transaction_path),
        "current_path": str(request.current_path),
        "expected_initial_state_revision": request.expected_initial_state_revision,
        "expected_initial_state_file_hash": request.expected_initial_state_file_hash,
        "initial_current_contract": _thaw(request.initial_current_contract),
        "lineage": {
            "planning_root": str(lineage.planning_root),
            "program": lineage.program,
            "batch_id": lineage.batch_id,
            "included_finding_ids": list(lineage.included_finding_ids),
            "deferred_finding_ids": list(lineage.deferred_finding_ids),
            "batch_kind": lineage.batch_kind,
            "ledger_path": str(lineage.ledger_path),
            "ledger_revision": lineage.ledger_revision,
            "dispatch_path": str(lineage.dispatch_path),
            "dispatch_revision": lineage.dispatch_revision,
            "runway_path": str(lineage.runway_path),
            "closeout_path": str(lineage.closeout_path),
            "toolchain_source_root": str(lineage.toolchain_source_root),
            "canonical_planning_repository_root": str(
                lineage.canonical_planning_repository_root
            ),
            "implementation_target_root": str(lineage.implementation_target_root),
            "dispatch_producer": producer(lineage.dispatch_producer),
            "runway_producer": producer(lineage.runway_producer),
            "closeout_producer": producer(lineage.closeout_producer),
        },
        "command_owner_version": request.command_owner_version,
        "producer": producer(request.producer),
    }


def _run_execution(
    case: Mapping[str, object],
    workspace: Path,
    *,
    collaborators: ExecutionCollaborators | None,
) -> tuple[str, list[str], str | None, list[str]]:
    fixture_input = cast(Mapping[str, object], case["input"])
    _write_json(workspace / "execution-input.json", fixture_input)
    observed_input = cast(
        Mapping[str, object],
        json.loads((workspace / "execution-input.json").read_text(encoding="utf-8")),
    )
    initial_state = cast(str, observed_input["initial_state"])
    _write_json(
        workspace / "execution-state.json",
        {"slice": "workflow", "state": initial_state},
    )
    before = _snapshot(workspace)
    active = collaborators or _default_execution_collaborators()
    resumed = initial_state == "validation-failed"
    if resumed:
        _write_json(
            workspace / "recovery-decision.json",
            {"action": "resume-same-slice", "from_state": initial_state},
        )
        _write_execution_state(workspace, "resumed")

    worker_request = {
        "slice": "workflow",
        "allowed_paths": list(cast(list[str], observed_input["allowed_paths"])),
        "input": dict(observed_input),
    }
    worker_result = active.worker(worker_request)
    if worker_result is None:
        return _execution_blocked(
            workspace,
            before,
            "worker result is missing",
            ["execution.scope.green", "execution.stop.green"],
        )
    _write_json(workspace / "worker-result.json", worker_result)
    worker_paths = _valid_worker_paths(worker_result, worker_request)
    if worker_paths is None:
        return _execution_blocked(
            workspace,
            before,
            "worker result escapes the allowed scope",
            ["execution.scope.green", "execution.stop.green"],
        )

    validation_result = active.validator(
        {"slice": "workflow", "worker_result": dict(worker_result), "input": dict(observed_input)}
    )
    if validation_result is None:
        return _execution_blocked(
            workspace,
            before,
            "validation result is missing",
            ["execution.validation.green", "execution.stop.green"],
        )
    _write_json(workspace / "validation-result.json", validation_result)
    if validation_result != {"status": "passed"}:
        return _execution_blocked(
            workspace,
            before,
            "validation did not pass after resume" if resumed else "validation did not pass",
            ["execution.validation.green", "execution.stop.green"],
        )

    review_result = active.reviewer(
        {
            "slice": "workflow",
            "worker_result": dict(worker_result),
            "validation_result": dict(validation_result),
            "input": dict(observed_input),
        }
    )
    if review_result is None:
        return _execution_blocked(
            workspace,
            before,
            "review result is missing",
            ["execution.review.green", "execution.stop.green"],
        )
    _write_json(workspace / "review-result.json", review_result)
    if review_result != {"verdict": "accept", "scope": "workflow"}:
        return _execution_blocked(
            workspace,
            before,
            "review requires an in-scope fix before commit",
            ["execution.worker.green", "execution.validation.green", "execution.stop.green"],
        )

    commit_result = active.committer(
        {
            "slice": "workflow",
            "allowed_paths": list(cast(list[str], observed_input["allowed_paths"])),
            "worker_paths": worker_paths,
            "review_result": dict(review_result),
            "input": dict(observed_input),
        }
    )
    if commit_result is None:
        return _execution_blocked(
            workspace,
            before,
            "commit receipt is missing",
            ["commit.receipt-required.green", "execution.stop.green"],
            transition="commit:blocked",
        )
    _write_json(workspace / "commit-receipt.json", commit_result)
    receipt_error = _commit_receipt_error(
        commit_result,
        allowed_paths=cast(list[str], observed_input["allowed_paths"]),
        worker_paths=worker_paths,
    )
    if receipt_error is not None:
        validation = (
            ["commit.scope-check.green", "execution.stop.green"]
            if receipt_error == "commit contains unrelated content"
            else ["commit.receipt-validity.green", "execution.stop.green"]
        )
        return _execution_blocked(
            workspace,
            before,
            receipt_error,
            validation,
            transition="commit:blocked",
        )

    _write_execution_state(workspace, "committed")
    validation = [
        "execution.worker.green",
        "execution.validation.green",
        "execution.review.green",
        "execution.commit.green",
    ]
    if resumed:
        validation.extend(["execution.recovery.green", "execution.resume.green"])
    return "execution:committed", _changed_paths(before, workspace), None, validation


def _execution_blocked(
    workspace: Path,
    before: Mapping[str, bytes],
    stop_reason: str,
    validation: list[str],
    *,
    transition: str = "execution:blocked",
) -> tuple[str, list[str], str, list[str]]:
    _write_execution_state(workspace, "blocked")
    return transition, _changed_paths(before, workspace), stop_reason, validation


def _write_execution_state(workspace: Path, state: str) -> None:
    _write_json(workspace / "execution-state.json", {"slice": "workflow", "state": state})


def _valid_worker_paths(
    result: Mapping[str, object], request: Mapping[str, object]
) -> list[str] | None:
    if set(result) != {"status", "changed_paths"} or result["status"] != "success":
        return None
    changed_paths = result["changed_paths"]
    allowed_paths = cast(list[str], request["allowed_paths"])
    if not isinstance(changed_paths, list) or not all(
        isinstance(path, str) for path in changed_paths
    ):
        return None
    typed_paths = cast(list[str], changed_paths)
    if len(typed_paths) != len(set(typed_paths)) or not set(typed_paths) <= set(
        allowed_paths
    ):
        return None
    return typed_paths


def _commit_receipt_error(
    result: Mapping[str, object], *, allowed_paths: list[str], worker_paths: list[str]
) -> str | None:
    if set(result) != {"commit", "paths"}:
        return "commit receipt is invalid"
    commit = result["commit"]
    paths = result["paths"]
    if not isinstance(commit, str) or len(commit) != 40 or any(
        character not in "0123456789abcdef" for character in commit
    ):
        return "commit receipt is invalid"
    if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
        return "commit receipt is invalid"
    typed_paths = cast(list[str], paths)
    if set(typed_paths) - set(allowed_paths) or typed_paths != worker_paths:
        return "commit contains unrelated content"
    return None


def _default_execution_collaborators() -> ExecutionCollaborators:
    return ExecutionCollaborators(
        worker=_fixture_worker,
        validator=_fixture_validator,
        reviewer=_fixture_execution_reviewer,
        committer=_fixture_committer,
    )


def _fixture_worker(request: Mapping[str, object]) -> Mapping[str, object]:
    fixture_input = cast(Mapping[str, object], request["input"])
    return {
        "status": "success",
        "changed_paths": list(cast(list[str], fixture_input["worker_paths"])),
    }


def _fixture_validator(request: Mapping[str, object]) -> Mapping[str, object]:
    fixture_input = cast(Mapping[str, object], request["input"])
    return {"status": fixture_input["validation_status"]}


def _fixture_execution_reviewer(request: Mapping[str, object]) -> Mapping[str, object]:
    fixture_input = cast(Mapping[str, object], request["input"])
    return {"verdict": fixture_input["review_verdict"], "scope": "workflow"}


def _fixture_committer(
    request: Mapping[str, object],
) -> Mapping[str, object] | None:
    fixture_input = cast(Mapping[str, object], request["input"])
    receipt_fixture = fixture_input["commit_receipt"]
    if receipt_fixture == "missing":
        return None
    worker_paths = list(cast(list[str], request["worker_paths"]))
    if receipt_fixture == "unrelated-content":
        worker_paths.append("unrelated/file")
    return {"commit": "f" * 40, "paths": worker_paths}


def _run_closeout(
    case: Mapping[str, object], workspace: Path, fixture_root: Path
) -> tuple[str, list[str], str | None, list[str]]:
    repo_root = _repo_root(fixture_root)
    request = _selection_workspace(workspace, repo_root, {"slice_boundaries": ["closeout"]})
    simulate_selection_transaction(request, toolchain_root=repo_root)
    contracts = _artifact_contracts(repo_root)
    closeout = contracts["planning-closeout/v1"]
    closeout["artifact"]["batch_id"] = request.lineage.batch_id
    closeout["producer"] = {
        "toolchain_generation": request.lineage.closeout_producer.toolchain_generation,
        "toolchain_commit": request.lineage.closeout_producer.toolchain_commit,
        "schema_version": request.lineage.closeout_producer.schema_version,
    }
    closeout["execution_context"] = {
        "canonical_planning_repository_root": str(workspace.parent),
        "implementation_target_root": str(workspace / "candidate"),
    }
    before = _snapshot(workspace)
    if case["mode"] == "wrong-batch":
        closeout["artifact"]["batch_id"] = "other-batch"
        try:
            _write_closeout(request, closeout, repo_root)
        except PlanningStoreError as error:
            assert error.code == "artifact.lineage"
        else:
            raise AssertionError("foreign closeout batch unexpectedly wrote")
        return (
            "closeout:blocked",
            _changed_paths(before, workspace),
            "closeout batch identity does not match the queued batch",
            ["closeout.lineage.green", "closeout.stop.green"],
        )
    if case["mode"] == "recover":
        try:
            _write_closeout(
                request,
                closeout,
                repo_root,
                fault="after_replace_before_return",
            )
        except InjectedStoreFailure:
            pass
        else:
            raise AssertionError("closeout fault was not injected")
        recovered = _write_closeout(request, closeout, repo_root)
        assert recovered.outcome == "exact_replay"
        validation = ["closeout.store.green", "closeout.recovery.green"]
    else:
        result = _write_closeout(request, closeout, repo_root)
        assert result.outcome == "applied"
        validation = ["closeout.store.green"]
    _reconcile_closeout(request, repo_root)
    current = read_current_document(request.current_path, toolchain_root=repo_root)
    ledger = read_ledger_document(request.lineage.ledger_path, toolchain_root=repo_root)
    assert current.contract["queued_runway"] is None
    assert current.contract["latest_closeout"] == "closeout.md"
    assert ledger.findings["CCFG-1"]["lifecycle"]["status"] == "closed"
    validation.extend(["closeout.reconciliation.green", "closeout.no-successor.green"])
    return (
        "closeout:reconciled",
        _changed_paths(before, workspace),
        "same-batch closeout stops without successor selection",
        validation,
    )


def _run_contract_format(
    workspace: Path, fixture_root: Path
) -> tuple[str, list[str], None, list[str]]:
    before = _snapshot(workspace)
    catalog = _load_mapping(fixture_root / "catalog.yaml")
    scenarios = cast(list[Mapping[str, object]], catalog["scenarios"])
    forbidden = cast(list[str], catalog["forbidden_target_terms"])
    target_records = [
        item for item in scenarios if item["evidence_kind"] != "source_characterization"
    ]
    encoded = json.dumps(target_records).casefold()
    assert all(term.casefold() not in encoded for term in forbidden)
    _write_json(
        workspace / "contract-format-evidence.json",
        {
            "required_contracts": len(cast(list[object], catalog["required_contracts"])),
            "target_records": len(target_records),
            "legacy_topology_required": False,
        },
    )
    return (
        "evidence:topology-independent",
        _changed_paths(before, workspace),
        None,
        ["evidence.contract-format.green", "evidence.topology-independent.green"],
    )


def _selection_workspace(
    workspace: Path, repo_root: Path, case: Mapping[str, object]
) -> SelectionTransactionRequest:
    current_path = workspace / "CURRENT.md"
    ledger_path = workspace / "LEDGER.md"
    shutil.copy2(
        repo_root / "tests/fixtures/planning-contracts/current/valid/CURRENT.md",
        current_path,
    )
    shutil.copy2(
        repo_root / "tests/fixtures/planning-contracts/ledger/per-finding-valid/LEDGER.md",
        ledger_path,
    )
    initial = read_current_document(current_path, toolchain_root=repo_root)
    commit = subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True
    ).strip()
    contracts = _artifact_contracts(repo_root)
    dispatch = contracts["planning-dispatch/v1"]
    runway = contracts["planning-runway/v1"]
    dispatch["artifact"]["id"] = "fixture-batch"
    dispatch["source"]["finding_ids"] = ["CCFG-1"]
    dispatch["scope"]["included_finding_ids"] = ["CCFG-1"]
    dispatch["execution_context"] = {
        "toolchain_source_root": str(repo_root),
        "canonical_planning_repository_root": str(workspace.parent),
        "implementation_target_root": str(workspace / "candidate"),
    }
    dispatch["producer"] = {
        "toolchain_generation": "candidate",
        "toolchain_commit": commit,
        "schema_version": "planning-dispatch/v1",
    }
    runway["artifact"]["id"] = "fixture-batch"
    runway["execution"]["implementation_target_root"] = str(workspace / "candidate")
    runway["producer"] = {
        "toolchain_generation": "candidate",
        "toolchain_commit": commit,
        "schema_version": "planning-runway/v1",
    }
    boundaries = cast(list[str], case.get("slice_boundaries", ["workflow-seam"]))
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
    _apply_vertical_scenario(runway, case)
    batch_kind = cast(str, case.get("batch_kind", "migration"))
    cast(dict[str, object], runway["batch"])["kind"] = batch_kind
    cast(dict[str, object], dispatch["scope"])["batch_kind"] = batch_kind
    lineage = ArtifactLineage(
        planning_root=workspace,
        program="codex-config",
        batch_id="fixture-batch",
        included_finding_ids=("CCFG-1",),
        deferred_finding_ids=(),
        batch_kind=batch_kind,
        ledger_path=ledger_path,
        ledger_revision="b" * 64,
        dispatch_path=workspace / "dispatch.md",
        dispatch_revision="a" * 64,
        runway_path=workspace / "runway.md",
        closeout_path=workspace / "closeout.md",
        toolchain_source_root=repo_root,
        canonical_planning_repository_root=workspace.parent,
        implementation_target_root=workspace / "candidate",
        dispatch_producer=ProducerIdentity(
            "candidate", commit, "planning-dispatch/v1"
        ),
        runway_producer=ProducerIdentity(
            "candidate", commit, "planning-runway/v1"
        ),
        closeout_producer=ProducerIdentity(
            "candidate", commit, "planning-closeout/v1"
        ),
    )
    return SelectionTransactionRequest(
        transaction_id="fixture-selection",
        transaction_path=workspace / "selection.md",
        current_path=current_path,
        expected_initial_state_revision=initial.logical_revision,
        expected_initial_state_file_hash=initial.file_hash,
        initial_current_contract=_thaw(initial.contract),
        lineage=lineage,
        dispatch_contract=dispatch,
        runway_contract=runway,
        command_owner_version="fixture-command-owner-v1",
        producer=ProducerIdentity(
            "candidate", commit, "planning-selection-transaction/v1"
        ),
    )


def _apply_vertical_scenario(
    runway: dict[str, object], case: Mapping[str, object]
) -> None:
    scenario = case.get("vertical_case")
    if scenario is None or scenario == "non-migration":
        return

    slices = cast(list[dict[str, object]], runway["slices"])
    target = slices[-1] if scenario == "mixed-risk" else slices[0]
    target["risk"] = "migration"
    if scenario == "missing":
        return

    coexistence = (
        "temporary"
        if scenario
        in {
            "temporary",
            "temporary-incomplete",
        }
        else "none"
    )
    vertical, matrix = _vertical_scenario_contract(coexistence)
    if scenario == "temporary-incomplete":
        row = cast(dict[str, object], matrix["fixture planning caller"])
        del row["removal_slice_or_condition"]
    elif scenario == "none-with-rows":
        _, matrix = _vertical_scenario_contract("temporary")
    target["vertical_slice"] = vertical
    target["migration_matrix"] = matrix


def _vertical_scenario_contract(
    coexistence: str,
) -> tuple[dict[str, object], dict[str, object]]:
    vertical: dict[str, object] = {
        "starting_scenario": "one caller still uses the previous planning owner",
        "durable_result": "that caller uses the permanent planning owner",
        "owner_before": "previous planning owner",
        "owner_after": "permanent plan-batch owner",
        "migrated_callers": ["fixture planning caller"],
        "focused_validation": ["planning.vertical-contract.green"],
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


def _seed_existing_state(
    request: SelectionTransactionRequest,
    case: Mapping[str, object],
    repo_root: Path,
) -> None:
    existing_state = case.get("existing_state")
    if existing_state is None:
        return
    snapshot = read_current_document(request.current_path, toolchain_root=repo_root)
    replacement = _thaw(snapshot.contract)
    replacement["revision"] = snapshot.logical_revision + 1
    if existing_state == "selected":
        replacement["selected_dispatch"] = "existing-dispatch.md"
    elif existing_state == "queued":
        replacement["queued_runway"] = "existing-runway.md"
    elif existing_state == "active":
        replacement["active_runway"] = "existing-runway.md"
    else:
        raise ValueError(f"unknown existing state {existing_state!r}")
    apply_current_document(
        request.current_path,
        toolchain_root=repo_root,
        expected_revision=snapshot.logical_revision,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key=f"seed-{existing_state}",
    )


def _planning_stop_reason(
    case: Mapping[str, object],
    request: SelectionTransactionRequest,
    repo_root: Path,
) -> str | None:
    current = read_current_document(request.current_path, toolchain_root=repo_root)
    for field, reason in (
        ("selected_dispatch", "an existing dispatch is already selected"),
        ("queued_runway", "an existing runway is already queued"),
        ("active_runway", "an existing runway is already active"),
    ):
        if current.contract[field] is not None:
            return reason
    if case.get("scope_quality") == "vague":
        return "planning scope is missing or vague"
    if cast(bool, case.get("destructive", False)) and case.get("approval") is None:
        return "destructive work lacks explicit user approval"
    if case.get("semantic_boundaries") is False:
        return "multi-slice plan lacks semantic boundaries"
    if case.get("scope_expansion") is not None:
        return "plan expands beyond the minimum viable scope"
    if cast(bool, case.get("residual_complexity", False)) and case.get("approval") is None:
        return "residual material complexity lacks narrowly scoped approval"
    if case.get("draft_state") == "stale":
        return "stale draft is non-executable"
    if case.get("draft_state") == "undecided":
        return "draft with unresolved user decisions is non-executable"
    return None


def _planning_collaborators(case: Mapping[str, object]) -> PlanningCollaborators:
    planner_fixture = case.get("planner_fixture", "independent")
    planner = (
        _fixture_planner
        if planner_fixture == "independent"
        else _fixture_coupled_planner
    )
    return PlanningCollaborators(planner=planner, reviewer=_fixture_plan_reviewer)


def _evaluate_planning_boundary(
    case: Mapping[str, object], collaborators: PlanningCollaborators
) -> PlanningBoundaryResult:
    request: Mapping[str, object] = {
        "interface": "fixture-plan-request/v1",
        "requested_boundaries": list(cast(list[str], case["slice_boundaries"])),
    }
    plan = collaborators.planner(request)
    planner_invocation = {
        "role": "batch_planner",
        "boundary": "injected-fixture-collaborator",
        "caller": "fixture-command-owner",
        "direct": True,
        "request_digest": _mapping_digest(request),
    }
    if plan is None or set(plan) != {
        "interface",
        "slice_boundaries",
        "semantic_reasons",
    }:
        return PlanningBoundaryResult(
            plan=plan or {},
            review=None,
            invocations=(planner_invocation,),
            accepted=False,
            stop_reason="planner and reviewer roles are not independent",
        )
    boundaries = plan["slice_boundaries"]
    reasons = plan["semantic_reasons"]
    if (
        plan["interface"] != "fixture-plan/v1"
        or not isinstance(boundaries, list)
        or not isinstance(reasons, list)
        or not boundaries
        or len(boundaries) != len(reasons)
        or not all(isinstance(value, str) and value for value in boundaries)
        or not all(isinstance(value, str) and value for value in reasons)
        or len(set(cast(list[str], boundaries))) != len(boundaries)
    ):
        return PlanningBoundaryResult(
            plan=plan,
            review=None,
            invocations=(planner_invocation,),
            accepted=False,
            stop_reason="planner output lacks semantic slice boundaries",
        )
    review_request: Mapping[str, object] = {
        "interface": "fixture-plan-review-request/v1",
        "plan": dict(plan),
        "required_boundaries": list(cast(list[str], request["requested_boundaries"])),
    }
    review = collaborators.reviewer(review_request)
    reviewer_invocation = {
        "role": "batch_plan_reviewer",
        "boundary": "injected-fixture-collaborator",
        "caller": "fixture-command-owner",
        "direct": True,
        "request_digest": _mapping_digest(review_request),
    }
    invocations = (planner_invocation, reviewer_invocation)
    expected_digest = _mapping_digest(plan)
    if (
        review is None
        or set(review)
        != {"interface", "plan_digest", "verdict", "semantic_boundaries_verified"}
        or review.get("interface") != "fixture-plan-review/v1"
        or review.get("plan_digest") != expected_digest
        or review.get("verdict") != "accept"
        or review.get("semantic_boundaries_verified") is not True
    ):
        return PlanningBoundaryResult(
            plan=plan,
            review=review,
            invocations=invocations,
            accepted=False,
            stop_reason="independent plan review did not accept the plan",
        )
    return PlanningBoundaryResult(
        plan=plan,
        review=review,
        invocations=invocations,
        accepted=True,
        stop_reason=None,
    )


def _fixture_planner(request: Mapping[str, object]) -> Mapping[str, object]:
    boundaries = list(cast(list[str], request["requested_boundaries"]))
    return {
        "interface": "fixture-plan/v1",
        "slice_boundaries": boundaries,
        "semantic_reasons": [f"separate {boundary} responsibility" for boundary in boundaries],
    }


def _fixture_coupled_planner(request: Mapping[str, object]) -> Mapping[str, object]:
    plan = dict(_fixture_planner(request))
    plan["review_evidence"] = {"verdict": "accept"}
    return plan


def _fixture_plan_reviewer(
    request: Mapping[str, object],
) -> Mapping[str, object]:
    plan = cast(Mapping[str, object], request["plan"])
    boundaries = cast(list[str], plan["slice_boundaries"])
    reasons = cast(list[str], plan["semantic_reasons"])
    required = cast(list[str], request["required_boundaries"])
    semantic = boundaries == required and len(boundaries) == len(reasons) and all(
        isinstance(reason, str) and bool(reason) for reason in reasons
    )
    return {
        "interface": "fixture-plan-review/v1",
        "plan_digest": _mapping_digest(plan),
        "verdict": "accept" if semantic else "reject",
        "semantic_boundaries_verified": semantic,
    }


def _mapping_digest(value: Mapping[str, object]) -> str:
    return _value_digest(value)


def _value_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _write_closeout(
    request: SelectionTransactionRequest,
    contract: Mapping[str, object],
    repo_root: Path,
    *,
    fault: str | None = None,
) -> Any:
    kwargs: dict[str, Any] = {
        "toolchain_root": repo_root,
        "expected_revision": 0,
        "expected_file_hash": EMPTY_HASH,
        "expected_dispatch_file_hash": _hash(request.lineage.dispatch_path),
        "expected_runway_file_hash": _hash(request.lineage.runway_path),
        "contract": contract,
        "lineage": request.lineage,
        "idempotency_key": "fixture-closeout",
    }
    if fault is not None:
        kwargs["fault"] = fault
    return write_closeout_artifact(request.lineage.closeout_path, **kwargs)


def _reconcile_closeout(request: SelectionTransactionRequest, repo_root: Path) -> None:
    current = read_current_document(request.current_path, toolchain_root=repo_root)
    replacement = _thaw(current.contract)
    replacement["revision"] = current.logical_revision + 1
    replacement["selected_dispatch"] = None
    replacement["queued_runway"] = None
    replacement["active_runway"] = None
    replacement["latest_closeout"] = "closeout.md"
    apply_current_document(
        request.current_path,
        toolchain_root=repo_root,
        expected_revision=current.logical_revision,
        expected_file_hash=current.file_hash,
        replacement_contract=replacement,
        idempotency_key="fixture-closeout-current",
    )
    ledger = read_ledger_document(request.lineage.ledger_path, toolchain_root=repo_root)
    finding = _thaw(ledger.findings["CCFG-1"])
    finding["revision"] = cast(int, finding["revision"]) + 1
    finding["lifecycle"]["status"] = "closed"
    apply_ledger_decision(
        request.lineage.ledger_path,
        toolchain_root=repo_root,
        expected_revision=ledger.logical_revision,
        expected_file_hash=ledger.file_hash,
        action="reconcile",
        finding_mutations=[finding],
        touched_finding_revisions={"CCFG-1": 1},
        idempotency_key="fixture-closeout-ledger",
    )


def _artifact_contracts(repo_root: Path) -> dict[str, dict[str, Any]]:
    fixture = repo_root / "tests/fixtures/planning-contracts/artifacts/valid-lineage"
    result = validate_planning_contracts([fixture], toolchain_root=repo_root)
    if not result.is_valid:
        raise AssertionError(result.diagnostics)
    return {
        cast(str, item.contract["schema"]): _thaw(item.contract)
        for item in result.contracts
    }


def _repo_root(fixture_root: Path) -> Path:
    repo_root = fixture_root.resolve().parents[2]
    assert repo_root == REPO_ROOT
    return repo_root


def _load_mapping(path: Path) -> dict[str, object]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"fixture {path} must contain a mapping")
    return cast(dict[str, object], loaded)


def _thaw(value: object) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(child) for key, child in value.items()}
    if isinstance(value, tuple | list):
        return [_thaw(child) for child in value]
    return copy.deepcopy(value)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _changed_paths(before: Mapping[str, bytes], root: Path) -> list[str]:
    after = _snapshot(root)
    paths = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    return [f"workspace/{path}" for path in paths]


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_forbidden_paths_absent(workspace: Path) -> None:
    assert not (workspace.parent / "outside/canonical-planning").exists()
    assert not (workspace.parent / "outside/installed-home").exists()
