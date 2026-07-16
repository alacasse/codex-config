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
INSTALLED_PLANNING_CONTRACT = CANDIDATE_CODEX_HOME / "scripts/planning_contract.py"

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
    if mode == "guard":
        _seed_existing_state(request, case, repo_root)
        before = _snapshot(workspace)
        stop_reason = _planning_stop_reason(case, request, repo_root)
        if stop_reason is None:
            raise AssertionError("guard case did not produce a stop decision")
        return (
            "planning:blocked",
            _changed_paths(before, workspace),
            stop_reason,
            ["planning.guard.green", "planning.no-queue-mutation.green"],
        )
    before = _snapshot(workspace)
    if mode == "roles":
        collaborators = planning_collaborators or _planning_collaborators(case)
        boundary = _evaluate_planning_boundary(case, collaborators)
        if not boundary.accepted:
            return (
                "planning:blocked",
                _changed_paths(before, workspace),
                boundary.stop_reason,
                ["planning.guard.green", "planning.no-queue-mutation.green"],
            )
        assert boundary.review is not None
        _write_json(workspace / "planner-result.json", boundary.plan)
        _write_json(workspace / "reviewer-result.json", boundary.review)
        _write_json(
            workspace / "role-invocations.json", list(boundary.invocations)
        )
    if cast(bool, case.get("residual_complexity", False)):
        approval = cast(Mapping[str, object], case["approval"])
        _write_json(workspace / "approval-decision.json", dict(approval))
    if mode == "recover":
        try:
            simulate_selection_transaction(
                request,
                toolchain_root=repo_root,
                fault="after_idle_to_selected_cas_before_receipt",
            )
        except RuntimeError:
            pass
        else:
            raise AssertionError("selection fault was not injected")
        result = simulate_selection_transaction(request, toolchain_root=repo_root)
        replay = simulate_selection_transaction(request, toolchain_root=repo_root)
        assert result.outcome == "completed"
        assert replay.outcome == "exact_replay"
        validation = [
            "planning.transaction.green",
            "planning.recovery.green",
            "planning.idempotence.green",
        ]
    else:
        result = simulate_selection_transaction(request, toolchain_root=repo_root)
        assert result.outcome == "completed"
        validation = ["planning.transaction.green", "planning.quality.green"]
        if mode == "roles":
            validation.append("planning.fixture-role-boundary.green")
        if cast(bool, case.get("residual_complexity", False)):
            validation.append("planning.approval-scoped.green")
    current = read_current_document(request.current_path, toolchain_root=repo_root)
    assert current.contract["queued_runway"] == "runway.md"
    assert current.contract["selected_dispatch"] is None
    return (
        "planning:queued",
        _changed_paths(before, workspace),
        "planning stops before implementation",
        validation,
    )


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
    contracts = _artifact_contracts(repo_root)
    dispatch = contracts["planning-dispatch/v1"]
    runway = contracts["planning-runway/v1"]
    dispatch["artifact"]["id"] = "fixture-batch"
    dispatch["source"]["finding_ids"] = ["CCFG-1"]
    dispatch["scope"]["included_finding_ids"] = ["CCFG-1"]
    dispatch["execution_context"] = {
        "toolchain_source_root": str(workspace / "stable"),
        "canonical_planning_repository_root": str(workspace.parent),
        "implementation_target_root": str(workspace / "candidate"),
    }
    runway["artifact"]["id"] = "fixture-batch"
    runway["execution"]["implementation_target_root"] = str(workspace / "candidate")
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
    lineage = ArtifactLineage(
        planning_root=workspace,
        program="codex-config",
        batch_id="fixture-batch",
        included_finding_ids=("CCFG-1",),
        deferred_finding_ids=(),
        batch_kind="migration",
        ledger_path=ledger_path,
        ledger_revision="b" * 64,
        dispatch_path=workspace / "dispatch.md",
        dispatch_revision="a" * 64,
        runway_path=workspace / "runway.md",
        closeout_path=workspace / "closeout.md",
        toolchain_source_root=workspace / "stable",
        canonical_planning_repository_root=workspace.parent,
        implementation_target_root=workspace / "candidate",
        dispatch_producer=ProducerIdentity("stable", COMMIT, "planning-dispatch/v1"),
        runway_producer=ProducerIdentity("stable", COMMIT, "planning-runway/v1"),
        closeout_producer=ProducerIdentity("stable", COMMIT, "planning-closeout/v1"),
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
            "stable", COMMIT, "planning-selection-transaction/v1"
        ),
    )


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


def _new_finding(template: Mapping[str, object], finding_id: str) -> dict[str, Any]:
    finding = _thaw(template)
    finding["id"] = finding_id
    finding["revision"] = 1
    finding["title"] = f"Fixture finding {finding_id}"
    finding["provenance"] = {
        "source_id": f"SRC-{finding_id}",
        "source_commit": "3" * 40,
        "source_section": f"source.md#{finding_id.casefold()}",
    }
    finding["lifecycle"]["status"] = "open"
    finding["dependencies"] = []
    return finding


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
