"""Disposable Planning State and protected-handoff scenario adapters."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import cross_checkout_context as context_owner  # noqa: E402


FORBIDDEN_WRITES = ["outside/canonical-planning", "outside/installed-home"]
ROOT_FACTS = {
    "generation": "fixture-stable",
    "roots": [
        {"role": "planning-toolchain", "path": "workspace/planning-repo"},
        {"role": "implementation", "path": "workspace/implementation-repo"},
    ],
}
Evidence = Mapping[str, object]
Producer = Callable[[Evidence], Mapping[str, object] | None]
Consumer = Callable[[Evidence], None]
Hook = Callable[[Path, Path, Path], None]


@dataclass(frozen=True)
class RepositoryObservation:
    """One independently observed pair of repository identities."""

    planning_commit: str
    implementation_commit: str


@dataclass(frozen=True)
class HandoffProducers:
    """Fixture producers kept separate from handoff acceptance consumers."""

    worker: Producer
    receipt: Producer
    commit: Producer
    reviewer_receipt: Producer
    reviewer: Producer
    reconciliation: Producer


@dataclass(frozen=True)
class HandoffConsumers:
    """Independently injected consumers for every protected boundary."""

    worker_result: Consumer
    receipt: Consumer
    commit: Consumer
    reviewer_receipt: Consumer
    reviewer: Consumer
    reconciliation: Consumer
    workspace: Consumer


class BoundaryViolation(RuntimeError):
    """Structured fail-closed evidence from one observed boundary."""

    def __init__(self, code: str, reason: str, evidence: Mapping[str, object]) -> None:
        super().__init__(reason)
        self.code = code
        self.reason = reason
        self.evidence = dict(evidence)


def observe_currentness(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    """Observe one case entirely inside a disposable workspace."""

    with tempfile.TemporaryDirectory(prefix="command-owner-currentness-") as directory:
        return run_scenario(scenario, fixture_root, Path(directory) / "workspace")


def run_scenario(
    scenario: Mapping[str, object],
    fixture_root: Path,
    workspace: Path,
    *,
    handoff_producers: HandoffProducers | None = None,
    handoff_consumers: HandoffConsumers | None = None,
    between_observations: Hook | None = None,
    workspace_hook: Hook | None = None,
) -> Mapping[str, object]:
    """Run one currentness case in caller-owned isolated roots."""

    cases = _load_mapping(fixture_root / "currentness-cases.yaml")
    scenario_id = cast(str, scenario["id"])
    case = cast(Mapping[str, object], cases[scenario_id])
    initial_state = (
        cast(str, case["state"])
        if case["operation"] == "planning-currentness"
        else "queued"
    )
    workspace.mkdir(parents=True)
    planning_repo, implementation_repo, planning_root = _seed_roots(
        workspace, initial_state
    )
    before = _snapshot_workspace(workspace)
    baseline = _observe_repositories(planning_repo, implementation_repo)
    checkpoints: list[str] = []
    operation = cast(str, case["operation"])
    try:
        if operation == "planning-currentness":
            outcome = _planning_currentness(
                workspace,
                planning_root,
                planning_repo,
                implementation_repo,
                initial_state,
                checkpoints,
            )
        elif operation == "lease":
            outcome = _lease_outcome(
                workspace,
                planning_root,
                planning_repo,
                implementation_repo,
                baseline,
                cast(str, case["fault"]),
                checkpoints,
                between_observations=between_observations,
            )
        else:
            outcome = _handoff_outcome(
                workspace,
                planning_root,
                planning_repo,
                implementation_repo,
                baseline,
                cast(str | None, case["fault"]),
                checkpoints,
                producers=handoff_producers,
                consumers=handoff_consumers,
                workspace_hook=workspace_hook,
                before=before,
            )
    except BoundaryViolation as error:
        outcome = {
            "status": "blocked",
            "reason": error.reason,
            "boundary": error.code,
            "evidence": error.evidence,
        }
    expected = cast(str, case["expected"])
    if outcome["status"] != expected:
        raise AssertionError(f"{scenario_id} expected {expected}, got {outcome}")
    _write_json(workspace / "outcome.json", outcome)
    return {
        "transition": f"currentness:{expected}",
        "writes": _workspace_changes(before, workspace),
        "forbidden_writes": FORBIDDEN_WRITES,
        "stop_reason": None if expected == "ready" else cast(str, outcome["reason"]),
        "generation_and_roots": ROOT_FACTS,
        "validation": checkpoints,
    }


def _planning_currentness(
    workspace: Path,
    planning_root: Path,
    planning_repo: Path,
    implementation_repo: Path,
    state: str,
    checkpoints: list[str],
) -> dict[str, object]:
    state_file = (
        _write_stale_state_fixture(workspace) if state == "stale" else None
    )
    current = _run_planning_state(planning_root, "current", state_file=state_file)
    validate = _run_planning_state(planning_root, "validate", state_file=state_file)
    _write_json(workspace / "current.json", current)
    _write_json(workspace / "validate.json", validate)
    checkpoints.append(
        "planning-state.current.blocked"
        if state == "stale"
        else "planning-state.current.green"
    )
    if validate["exit"]["code"] != 0:
        checkpoints.extend(
            [
                "planning-state.validate.blocked",
                "currentness.helper-not-invoked.green",
            ]
        )
        return {
            "status": "blocked",
            "reason": (
                "Planning State reports stale state before lease preparation"
                if state == "stale"
                else "Planning State validation blocked before lease preparation"
            ),
            "helper_invoked": False,
            "semantic_state": None,
        }
    program = cast(list[Mapping[str, object]], current["programs"])[0]
    semantic = _semantic_state(program)
    if semantic != state:
        raise AssertionError(f"Planning State reported {semantic!r}, expected {state!r}")
    context_owner.parse_cross_checkout_context(
        _payload(
            planning_repo,
            implementation_repo,
            workspace / "codex-home",
            _observe_repositories(planning_repo, implementation_repo),
        )
    )
    checkpoints.extend(
        [
            "planning-state.validate.green",
            "currentness.semantic-owner.green",
        ]
    )
    return {
        "status": "ready",
        "reason": None,
        "helper_invoked": True,
        "semantic_state": semantic,
    }


def _lease_outcome(
    workspace: Path,
    planning_root: Path,
    planning_repo: Path,
    implementation_repo: Path,
    planned: RepositoryObservation,
    fault: str,
    checkpoints: list[str],
    *,
    between_observations: Hook | None,
) -> dict[str, object]:
    _require_green_planning_state(workspace, planning_root)
    before_observation: Hook | None = None
    between = between_observations
    if fault == "planning-head-advanced":
        before_observation = _advance_planning
    elif fault == "implementation-moved":
        before_observation = _advance_implementation
    elif fault == "preparation-movement" and between is None:
        between = _advance_implementation
    context, observed = _prepare_lease(
        workspace,
        planning_root,
        planning_repo,
        implementation_repo,
        planned,
        checkpoints,
        before_observation=before_observation,
        between_observations=between,
    )
    scope = context_owner.validate_write_scope(
        context,
        canonical_planning_root=planning_root,
        implementation_paths=(implementation_repo / "allowed.txt",),
    )
    return {
        "status": "ready",
        "reason": None,
        "planning_commit": observed.planning_commit,
        "implementation_commit": observed.implementation_commit,
        "scope": [str(path) for path in scope.implementation_paths],
    }


def _prepare_lease(
    workspace: Path,
    planning_root: Path,
    planning_repo: Path,
    implementation_repo: Path,
    planned: RepositoryObservation,
    checkpoints: list[str],
    *,
    before_observation: Hook | None = None,
    between_observations: Hook | None = None,
    evidence_filename: str = "lease-preparation.json",
    checkpoint_codes: tuple[str, ...] = (
        "currentness.material-integrity.green",
        "currentness.fresh-lease.green",
    ),
) -> tuple[context_owner.CrossCheckoutContext, RepositoryObservation]:
    if before_observation is not None:
        before_observation(workspace, planning_repo, implementation_repo)
    first = _observe_repositories(planning_repo, implementation_repo)
    if between_observations is not None:
        between_observations(workspace, planning_repo, implementation_repo)
    second = _observe_repositories(planning_repo, implementation_repo)
    evidence = {
        "planned": _observation_dict(planned),
        "before_hook": _observation_dict(first),
        "after_hook": _observation_dict(second),
    }
    checkpoints.extend(checkpoint_codes)
    if first != second:
        _write_json(
            workspace / evidence_filename,
            {**evidence, "status": "blocked", "error": "movement_during_preparation"},
        )
        raise BoundaryViolation(
            "movement_during_preparation",
            "repository moved during lease preparation",
            evidence,
        )
    if first.implementation_commit != planned.implementation_commit:
        _write_json(
            workspace / evidence_filename,
            {**evidence, "status": "blocked", "error": "unexpected_implementation_movement"},
        )
        raise BoundaryViolation(
            "unexpected_implementation_movement",
            "unexpected implementation movement",
            evidence,
        )
    payload = _payload(
        planning_repo,
        implementation_repo,
        workspace / "codex-home",
        second,
    )
    context = context_owner.parse_cross_checkout_context(payload)
    _write_json(
        workspace / evidence_filename,
        {**evidence, "status": "ready", "payload": _context_echo(payload)},
    )
    context_owner.validate_write_scope(
        context,
        canonical_planning_root=planning_root,
        implementation_paths=(implementation_repo / "allowed.txt",),
    )
    return context, second


def _handoff_outcome(
    workspace: Path,
    planning_root: Path,
    planning_repo: Path,
    implementation_repo: Path,
    baseline: RepositoryObservation,
    fault: str | None,
    checkpoints: list[str],
    *,
    producers: HandoffProducers | None,
    consumers: HandoffConsumers | None,
    workspace_hook: Hook | None,
    before: Mapping[str, str],
) -> dict[str, object]:
    _require_green_planning_state(workspace, planning_root)
    context, lease_observation = _prepare_lease(
        workspace,
        planning_root,
        planning_repo,
        implementation_repo,
        baseline,
        checkpoints,
    )
    payload = _payload(
        planning_repo,
        implementation_repo,
        workspace / "codex-home",
        lease_observation,
    )
    if fault == "wrong-generation":
        execution = cast(dict[str, object], payload["execution_context"])
        execution["generation_role"] = "candidate"
        execution["canonical_state_mutation_allowed"] = False
        try:
            context_owner.parse_cross_checkout_context(payload)
        except context_owner.CrossCheckoutContextError as error:
            checkpoints.append("currentness.generation-identity.green")
            raise BoundaryViolation(
                "generation_identity",
                "generation identity mismatch",
                {"error": str(error)},
            ) from error
        raise AssertionError("wrong generation unexpectedly validated")
    allowed = implementation_repo / "allowed.txt"
    requested = workspace / "outside" / "escape.txt" if fault == "wrong-root" else allowed
    try:
        scope = context_owner.validate_write_scope(
            context,
            canonical_planning_root=planning_root,
            implementation_paths=(requested,),
        )
    except context_owner.CrossCheckoutContextError as error:
        checkpoints.append("currentness.write-scope.green")
        raise BoundaryViolation(
            "write_scope",
            "write scope escapes the implementation root",
            {"error": str(error), "requested": str(requested)},
        ) from error
    checkpoints.append("currentness.write-scope.green")
    active_producers = producers or _producers_for_fault(fault)
    active_consumers = consumers or _default_consumers()
    request: dict[str, object] = {
        "workspace": workspace,
        "planning_root": planning_root,
        "planning_repo": planning_repo,
        "implementation_repo": implementation_repo,
        "context": context,
        "lease": _context_echo(payload),
        "lease_observation": lease_observation,
        "scope": scope,
        "allowed_path": allowed,
        "before": before,
        "checkpoints": checkpoints,
    }
    worker_result = active_producers.worker(request)
    _write_optional_json(workspace / "worker-result.json", worker_result)
    active_consumers.worker_result({**request, "worker_result": worker_result})
    receipt = active_producers.receipt(request)
    _write_optional_json(workspace / "lease-receipt.json", receipt)
    active_consumers.receipt({**request, "receipt": receipt})
    commit = active_producers.commit(request)
    _write_optional_json(workspace / "commit-evidence.json", commit)
    active_consumers.commit({**request, "receipt": receipt, "commit": commit})
    reviewer_planned = _observe_repositories(planning_repo, implementation_repo)
    reviewer_context, reviewer_observation = _prepare_lease(
        workspace,
        planning_root,
        planning_repo,
        implementation_repo,
        reviewer_planned,
        checkpoints,
        evidence_filename="reviewer-lease-preparation.json",
        checkpoint_codes=("currentness.reviewer-fresh-lease.green",),
    )
    reviewer_payload = _payload(
        planning_repo,
        implementation_repo,
        workspace / "codex-home",
        reviewer_observation,
    )
    reviewer_scope = context_owner.validate_write_scope(
        reviewer_context,
        canonical_planning_root=planning_root,
        implementation_paths=(allowed,),
    )
    review_request = {
        **request,
        "commit": commit,
        "reviewer_context": reviewer_context,
        "reviewer_lease": _context_echo(reviewer_payload),
        "reviewer_observation": reviewer_observation,
        "reviewer_scope": reviewer_scope,
    }
    reviewer = active_producers.reviewer(review_request)
    _write_optional_json(workspace / "review-result.json", reviewer)
    reviewer_receipt = active_producers.reviewer_receipt(
        {**review_request, "reviewer": reviewer}
    )
    _write_optional_json(
        workspace / "reviewer-lease-receipt.json", reviewer_receipt
    )
    active_consumers.reviewer_receipt(
        {**review_request, "reviewer_receipt": reviewer_receipt}
    )
    active_consumers.reviewer(
        {
            **review_request,
            "reviewer_receipt": reviewer_receipt,
            "reviewer": reviewer,
        }
    )
    reconciliation = active_producers.reconciliation(request)
    active_consumers.reconciliation(
        {**request, "reconciliation": reconciliation}
    )
    if workspace_hook is not None:
        workspace_hook(workspace, planning_repo, implementation_repo)
    elif fault == "unexpected-workspace-write":
        _write_unexpected_workspace_path(workspace, planning_repo, implementation_repo)
    elif fault == "untracked-implementation-write":
        _write_untracked_implementation_path(
            workspace, planning_repo, implementation_repo
        )
    elif fault == "undeclared-planning-write":
        _write_undeclared_planning_path(workspace, planning_repo, implementation_repo)
    active_consumers.workspace({**request, "before": before, "commit": commit})
    assert commit is not None
    return {
        "status": "ready",
        "reason": None,
        "base": commit["base"],
        "commit": commit["head"],
        "receipt_interface": cast(Mapping[str, object], receipt)["interface"],
    }


def _default_producers() -> HandoffProducers:
    return HandoffProducers(
        worker=_produce_worker_result,
        receipt=_produce_receipt,
        commit=_produce_commit,
        reviewer_receipt=_produce_reviewer_receipt,
        reviewer=_produce_review,
        reconciliation=_produce_reconciliation,
    )


def _producers_for_fault(fault: str | None) -> HandoffProducers:
    defaults = _default_producers()
    return HandoffProducers(
        worker=_produce_mixed_worker if fault == "mixed-generation" else defaults.worker,
        receipt=(
            _produce_missing_receipt
            if fault == "missing-receipt"
            else _produce_stale_receipt
            if fault == "stale-receipt-revision"
            else defaults.receipt
        ),
        commit=(
            _produce_unrelated_commit
            if fault == "unrelated-commit-content"
            else defaults.commit
        ),
        reviewer_receipt=defaults.reviewer_receipt,
        reviewer=(
            _produce_stale_review
            if fault == "stale-review-basis"
            else _produce_reused_worker_lease_review
            if fault == "reused-worker-reviewer-lease"
            else defaults.reviewer
        ),
        reconciliation=(
            _produce_partial_reconciliation
            if fault == "partial-reconciliation"
            else defaults.reconciliation
        ),
    )


def _default_consumers() -> HandoffConsumers:
    return HandoffConsumers(
        worker_result=_consume_worker_result,
        receipt=_consume_receipt,
        commit=_consume_commit,
        reviewer_receipt=_consume_reviewer_receipt,
        reviewer=_consume_reviewer,
        reconciliation=_consume_reconciliation,
        workspace=_consume_workspace,
    )


def _produce_worker_result(request: Evidence) -> Mapping[str, object]:
    return {"verified_context": dict(cast(Mapping[str, object], request["lease"]))}


def _produce_mixed_worker(request: Evidence) -> Mapping[str, object]:
    result = dict(_produce_worker_result(request))
    echo = dict(cast(Mapping[str, object], result["verified_context"]))
    echo["generation_role"] = "candidate"
    result["verified_context"] = echo
    return result


def _consume_worker_result(request: Evidence) -> None:
    _record_checkpoint(request, "currentness.lease-echo.green")
    result = request["worker_result"]
    lease = request["lease"]
    if not isinstance(result, Mapping) or result.get("verified_context") != lease:
        raise BoundaryViolation(
            "worker_result",
            "result generation does not match the lease",
            {"lease": lease, "worker_result": result},
        )


def _produce_receipt(request: Evidence) -> Mapping[str, object]:
    receipt = context_owner.build_cross_repository_receipt(
        cast(context_owner.CrossCheckoutContext, request["context"]),
        caller="fixture-worker",
        reason="protect fixture handoff",
        canonical_planning_root=cast(Path, request["planning_root"]),
        implementation_paths=cast(context_owner.AllowedWriteScope, request["scope"]).implementation_paths,
    )
    return context_owner.cross_repository_receipt_to_dict(receipt)


def _produce_missing_receipt(_request: Evidence) -> None:
    return None


def _produce_stale_receipt(request: Evidence) -> Mapping[str, object]:
    receipt = copy.deepcopy(dict(_produce_receipt(request)))
    revisions = cast(dict[str, object], receipt["repository_revisions"])
    revisions["implementation_commit_before"] = "0" * 40
    return receipt


def _consume_receipt(request: Evidence) -> None:
    _record_checkpoint(request, "currentness.receipt.green")
    receipt = request["receipt"]
    if not isinstance(receipt, Mapping):
        raise BoundaryViolation(
            "receipt",
            "durable handoff receipt is missing",
            {"receipt": receipt},
        )
    observed = _observe_repositories(
        cast(Path, request["planning_repo"]),
        cast(Path, request["implementation_repo"]),
    )
    revisions = cast(Mapping[str, object], receipt["repository_revisions"])
    scope = cast(Mapping[str, object], receipt["allowed_scope"])
    allowed = str(cast(Path, request["allowed_path"]).resolve())
    if revisions != {
        "toolchain_commit": observed.planning_commit,
        "canonical_planning_commit_before": observed.planning_commit,
        "implementation_commit_before": observed.implementation_commit,
    }:
        raise BoundaryViolation(
            "receipt_revisions",
            "receipt revisions do not match independently observed repositories",
            {"receipt_revisions": revisions, "observed": _observation_dict(observed)},
        )
    if scope["planning_paths"] != [] or scope["implementation_paths"] != [allowed]:
        raise BoundaryViolation(
            "receipt_scope",
            "receipt scope does not match the validated handoff paths",
            {"allowed_scope": scope, "expected_implementation_path": allowed},
        )


def _produce_commit(request: Evidence) -> Mapping[str, object]:
    return _commit_observed_paths(request, ("allowed.txt",))


def _produce_unrelated_commit(request: Evidence) -> Mapping[str, object]:
    return _commit_observed_paths(request, ("allowed.txt", "unrelated.txt"))


def _commit_observed_paths(
    request: Evidence, paths: tuple[str, ...]
) -> Mapping[str, object]:
    root = cast(Path, request["implementation_repo"])
    base = _git(root, "rev-parse", "HEAD")
    for path in paths:
        (root / path).write_text(f"content for {path}\n", encoding="utf-8")
    _git(root, "add", *paths)
    _git(root, "commit", "--quiet", "-m", "Produce fixture implementation")
    head = _git(root, "rev-parse", "HEAD")
    changed = _git(root, "diff", "--name-only", f"{base}..{head}").splitlines()
    return {"base": base, "head": head, "paths": changed}


def _consume_commit(request: Evidence) -> None:
    _record_checkpoint(request, "currentness.commit-range.green")
    commit = request["commit"]
    receipt = cast(Mapping[str, object], request["receipt"])
    if not isinstance(commit, Mapping):
        raise BoundaryViolation("commit", "commit evidence is missing", {"commit": commit})
    root = cast(Path, request["implementation_repo"])
    independently_observed_head = _git(root, "rev-parse", "HEAD")
    base = cast(str, commit["base"])
    head = cast(str, commit["head"])
    independently_observed_paths = _git(
        root, "diff", "--name-only", f"{base}..{head}"
    ).splitlines()
    lease = cast(RepositoryObservation, request["lease_observation"])
    receipt_revisions = cast(Mapping[str, object], receipt["repository_revisions"])
    evidence = {
        "base": base,
        "head": head,
        "observed_head": independently_observed_head,
        "paths": independently_observed_paths,
        "receipt_revision": receipt_revisions["implementation_commit_before"],
    }
    if (
        base != lease.implementation_commit
        or head != independently_observed_head
        or receipt_revisions["implementation_commit_before"] != base
        or independently_observed_paths != ["allowed.txt"]
        or commit["paths"] != independently_observed_paths
    ):
        raise BoundaryViolation(
            "commit_range",
            "accepted commit range contains unrelated or mismatched content",
            evidence,
        )


def _produce_review(request: Evidence) -> Mapping[str, object]:
    commit = cast(Mapping[str, object], request["commit"])
    return {
        "base": commit["base"],
        "commit": commit["head"],
        "verified_context": dict(
            cast(Mapping[str, object], request["reviewer_lease"])
        ),
    }


def _produce_stale_review(request: Evidence) -> Mapping[str, object]:
    result = dict(_produce_review(request))
    result["base"] = result["commit"]
    return result


def _produce_reused_worker_lease_review(request: Evidence) -> Mapping[str, object]:
    result = dict(_produce_review(request))
    result["verified_context"] = dict(
        cast(Mapping[str, object], request["lease"])
    )
    return result


def _produce_reviewer_receipt(request: Evidence) -> Mapping[str, object]:
    receipt = context_owner.build_cross_repository_receipt(
        cast(context_owner.CrossCheckoutContext, request["reviewer_context"]),
        caller="fixture-reviewer",
        reason="protect fixture reviewer handoff",
        canonical_planning_root=cast(Path, request["planning_root"]),
        implementation_paths=cast(
            context_owner.AllowedWriteScope, request["reviewer_scope"]
        ).implementation_paths,
    )
    return context_owner.cross_repository_receipt_to_dict(receipt)


def _consume_reviewer_receipt(request: Evidence) -> None:
    _record_checkpoint(request, "currentness.reviewer-receipt.green")
    receipt = request["reviewer_receipt"]
    if not isinstance(receipt, Mapping):
        raise BoundaryViolation(
            "reviewer_receipt",
            "durable reviewer handoff receipt is missing",
            {"reviewer_receipt": receipt},
        )
    observed = _observe_repositories(
        cast(Path, request["planning_repo"]),
        cast(Path, request["implementation_repo"]),
    )
    prepared = cast(RepositoryObservation, request["reviewer_observation"])
    revisions = cast(Mapping[str, object], receipt["repository_revisions"])
    scope = cast(Mapping[str, object], receipt["allowed_scope"])
    allowed = str(cast(Path, request["allowed_path"]).resolve())
    expected_revisions = {
        "toolchain_commit": observed.planning_commit,
        "canonical_planning_commit_before": observed.planning_commit,
        "implementation_commit_before": observed.implementation_commit,
    }
    if observed != prepared or revisions != expected_revisions:
        raise BoundaryViolation(
            "reviewer_receipt_revisions",
            "reviewer receipt does not match the independently observed repositories",
            {
                "receipt_revisions": revisions,
                "prepared": _observation_dict(prepared),
                "observed": _observation_dict(observed),
            },
        )
    if scope["planning_paths"] != [] or scope["implementation_paths"] != [allowed]:
        raise BoundaryViolation(
            "reviewer_receipt_scope",
            "reviewer receipt scope does not match the independently validated paths",
            {"allowed_scope": scope, "expected_implementation_path": allowed},
        )


def _consume_reviewer(request: Evidence) -> None:
    reviewer = request["reviewer"]
    commit = cast(Mapping[str, object], request["commit"])
    reviewer_lease = request["reviewer_lease"]
    observed = _observe_repositories(
        cast(Path, request["planning_repo"]),
        cast(Path, request["implementation_repo"]),
    )
    prepared = cast(RepositoryObservation, request["reviewer_observation"])
    _record_checkpoint(request, "currentness.reviewer-lease-echo.green")
    if (
        not isinstance(reviewer, Mapping)
        or reviewer.get("verified_context") != reviewer_lease
        or observed != prepared
    ):
        raise BoundaryViolation(
            "reviewer_lease",
            "reviewer result reuses the stale worker lease",
            {
                "worker_lease": request["lease"],
                "reviewer_lease": reviewer_lease,
                "reviewer": reviewer,
                "prepared": _observation_dict(prepared),
                "observed": _observation_dict(observed),
            },
        )
    _record_checkpoint(request, "currentness.review-basis.green")
    expected = {
        "base": commit["base"],
        "commit": commit["head"],
        "verified_context": reviewer_lease,
    }
    if reviewer != expected:
        raise BoundaryViolation(
            "reviewer_basis",
            "review basis is stale",
            {"expected": expected, "reviewer": reviewer},
        )


def _produce_reconciliation(_request: Evidence) -> Mapping[str, object]:
    return {"mode": "observe-current"}


def _produce_partial_reconciliation(request: Evidence) -> Mapping[str, object]:
    planning_root = cast(Path, request["planning_root"])
    (planning_root / "programs" / "fixture" / "CURRENT.md").write_text(
        "# Partial reconciliation\n", encoding="utf-8"
    )
    return {"mode": "partial-current-only"}


def _consume_reconciliation(request: Evidence) -> None:
    _record_checkpoint(request, "currentness.reconciliation.green")
    workspace = cast(Path, request["workspace"])
    planning_root = cast(Path, request["planning_root"])
    current = _run_planning_state(planning_root, "current")
    validate = _run_planning_state(planning_root, "validate")
    evidence = {"current": current, "validate": validate}
    _write_json(workspace / "reconciliation-result.json", evidence)
    programs = cast(list[Mapping[str, object]], current["programs"])
    try:
        semantic = _semantic_state(programs[0]) if programs else None
    except AssertionError:
        semantic = None
    if validate["exit"]["code"] != 0 or semantic != "queued":
        raise BoundaryViolation(
            "reconciliation_state",
            "same-batch reconciliation is partial",
            {"semantic_state": semantic, "blockers": validate["blockers"]},
        )


def _consume_workspace(request: Evidence) -> None:
    _record_checkpoint(request, "currentness.workspace-writes.green")
    workspace = cast(Path, request["workspace"])
    before = cast(Mapping[str, str], request["before"])
    changed = _workspace_changes(before, workspace)
    allowed_root_evidence = {
        "workspace/commit-evidence.json",
        "workspace/lease-preparation.json",
        "workspace/lease-receipt.json",
        "workspace/reconciliation-result.json",
        "workspace/review-result.json",
        "workspace/reviewer-lease-preparation.json",
        "workspace/reviewer-lease-receipt.json",
        "workspace/validate.json",
        "workspace/worker-result.json",
    }
    root_unexpected = [
        path
        for path in changed
        if not path.startswith("workspace/planning-repo/")
        and not path.startswith("workspace/implementation-repo/")
        and path not in allowed_root_evidence
    ]
    commit = cast(Mapping[str, object], request["commit"])
    expected_implementation = {
        f"workspace/implementation-repo/{path}"
        for path in cast(list[str], commit["paths"])
    }
    observed_implementation = {
        path
        for path in changed
        if path.startswith("workspace/implementation-repo/")
    }
    observed_planning = sorted(
        path for path in changed if path.startswith("workspace/planning-repo/")
    )
    implementation_repo = cast(Path, request["implementation_repo"])
    planning_repo = cast(Path, request["planning_repo"])
    implementation_status = _git(
        implementation_repo, "status", "--porcelain", "--untracked-files=all"
    ).splitlines()
    planning_status = _git(
        planning_repo, "status", "--porcelain", "--untracked-files=all"
    ).splitlines()
    lease = cast(RepositoryObservation, request["lease_observation"])
    planning_head = _git(planning_repo, "rev-parse", "HEAD")
    if (
        root_unexpected
        or observed_implementation != expected_implementation
        or observed_planning
        or implementation_status
        or planning_status
        or planning_head != lease.planning_commit
    ):
        raise BoundaryViolation(
            "workspace_writes",
            "workspace contains an unexpected write",
            {
                "changed_paths": changed,
                "unexpected_paths": sorted(
                    set(root_unexpected)
                    | (observed_implementation - expected_implementation)
                    | set(observed_planning)
                ),
                "expected_implementation_paths": sorted(expected_implementation),
                "implementation_status": implementation_status,
                "planning_status": planning_status,
                "planning_head": planning_head,
                "expected_planning_head": lease.planning_commit,
            },
        )


def _record_checkpoint(request: Evidence, code: str) -> None:
    cast(list[str], request["checkpoints"]).append(code)


def _seed_roots(workspace: Path, state: str) -> tuple[Path, Path, Path]:
    planning_repo = workspace / "planning-repo"
    implementation_repo = workspace / "implementation-repo"
    planning_root = planning_repo / "docs" / "plans"
    (workspace / "codex-home").mkdir()
    _init_repo(planning_repo)
    _init_repo(implementation_repo)
    _set_planning_state(planning_root, state)
    _git(planning_repo, "add", ".")
    _git(planning_repo, "commit", "--quiet", "-m", "Seed planning state")
    return planning_repo.resolve(), implementation_repo.resolve(), planning_root.resolve()


def _set_planning_state(root: Path, state: str) -> None:
    program = root / "programs" / "fixture"
    batch = program / "batches" / "fixture-batch"
    batch.mkdir(parents=True, exist_ok=True)
    (program / "LEDGER.md").write_text("# Fixture Ledger\n", encoding="utf-8")
    (batch / "dispatch.md").write_text("# Dispatch\n", encoding="utf-8")
    (batch / "runway.md").write_text("# Runway\n", encoding="utf-8")
    (root / "historical-batch-runway.md").write_text(
        "# Historical evidence only\n", encoding="utf-8"
    )
    if state == "stale":
        replaced = program / "batches" / "replaced-batch"
        replaced.mkdir(parents=True)
        (replaced / "dispatch.md").write_text("# Replaced Dispatch\n", encoding="utf-8")
    if state == "invalid":
        (root / "CURRENT.md").write_text(
            "# Planning Current State\n\n- Layout: Planning Artifact Layout v1\n\n"
            "## Active Programs\n\n| Program | Current state |\n|---|---|\n"
            "| `fixture` | `docs/plans/programs/missing/CURRENT.md` |\n",
            encoding="utf-8",
        )
        return
    effective_state = "queued" if state == "stale" else state
    selected = (
        "docs/plans/programs/fixture/batches/fixture-batch/dispatch.md"
        if effective_state == "selected"
        else "None"
    )
    active = (
        "docs/plans/programs/fixture/batches/fixture-batch/runway.md"
        if effective_state == "active"
        else "None"
    )
    queued = (
        "docs/plans/programs/fixture/batches/fixture-batch/runway.md"
        if effective_state == "queued"
        else "None"
    )
    root.mkdir(parents=True, exist_ok=True)
    (root / "CURRENT.md").write_text(
        "# Planning Current State\n\n- Layout: Planning Artifact Layout v1\n"
        "- Planning root: `docs/plans/`\n\n## Active Programs\n\n"
        "| Program | Current state |\n|---|---|\n"
        "| `fixture` | `docs/plans/programs/fixture/CURRENT.md` |\n",
        encoding="utf-8",
    )
    (program / "CURRENT.md").write_text(
        "# Fixture Current State\n\nProgram slug: `fixture`\n\n"
        "- Current ledger: `docs/plans/programs/fixture/LEDGER.md`\n"
        f"- Selected dispatch path: `{selected}`\n"
        f"- Active Batch Runway spec path: `{active}`\n"
        f"- Queued batch path or ID: `{queued}`\n"
        "- Latest closeout: `None`\n",
        encoding="utf-8",
    )


def _run_planning_state(
    root: Path, command: str, *, state_file: Path | None = None
) -> dict[str, object]:
    arguments = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "planning_state.py"),
        command,
        "--root",
        str(root),
        "--format",
        "json",
    ]
    if state_file is not None:
        arguments.extend(["--state-file", str(state_file)])
    completed = subprocess.run(
        arguments,
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    return cast(dict[str, object], json.loads(completed.stdout))


def _write_stale_state_fixture(workspace: Path) -> Path:
    path = workspace / "stale-state.json"
    _write_json(
        path,
        {
            "protocol": {"name": "planning-state-tool-state", "version": 1},
            "root": "docs/plans",
            "programs": [
                {
                    "slug": "fixture",
                    "current": "docs/plans/programs/fixture/CURRENT.md",
                    "ledger": "docs/plans/programs/fixture/LEDGER.md",
                    "selected_dispatch": (
                        "docs/plans/programs/fixture/batches/"
                        "replaced-batch/dispatch.md"
                    ),
                    "active_runway": None,
                    "queued_batch": None,
                    "latest_closeout": None,
                    "artifacts": [
                        {
                            "batch_id": "replaced-batch",
                            "path": (
                                "docs/plans/programs/fixture/batches/"
                                "replaced-batch/dispatch.md"
                            ),
                            "type": "dispatch",
                        }
                    ],
                }
            ],
        },
    )
    return path


def _require_green_planning_state(workspace: Path, planning_root: Path) -> None:
    validate = _run_planning_state(planning_root, "validate")
    _write_json(workspace / "validate.json", validate)
    if validate["exit"]["code"] != 0:
        raise AssertionError("fixture Planning State must be green before lease work")


def _semantic_state(program: Mapping[str, object]) -> str:
    for name in ("selected_dispatch", "queued_batch", "active_runway"):
        pointer = cast(Mapping[str, object], program[name])
        if pointer["value"] is not None:
            return {
                "selected_dispatch": "selected",
                "queued_batch": "queued",
                "active_runway": "active",
            }[name]
    raise AssertionError("Planning State reported no executable state")


def _payload(
    planning_repo: Path,
    implementation_repo: Path,
    codex_home: Path,
    observation: RepositoryObservation,
) -> dict[str, object]:
    return {
        "interface": context_owner.INTERFACE,
        "execution_context": {
            "toolchain_source_root": str(planning_repo),
            "toolchain_commit": observation.planning_commit,
            "canonical_planning_repository_root": str(planning_repo),
            "canonical_planning_commit_before": observation.planning_commit,
            "implementation_target_root": str(implementation_repo),
            "implementation_commit_before": observation.implementation_commit,
            "codex_home": str(codex_home.resolve()),
            "generation_role": "stable",
            "canonical_state_mutation_allowed": True,
        },
    }


def _context_echo(payload: Mapping[str, object]) -> dict[str, object]:
    execution = cast(Mapping[str, object], payload["execution_context"])
    return {"interface": payload["interface"], **dict(execution)}


def _observe_repositories(
    planning_repo: Path, implementation_repo: Path
) -> RepositoryObservation:
    return RepositoryObservation(
        planning_commit=_git(planning_repo, "rev-parse", "HEAD"),
        implementation_commit=_git(implementation_repo, "rev-parse", "HEAD"),
    )


def _observation_dict(observation: RepositoryObservation) -> dict[str, str]:
    return {
        "planning_commit": observation.planning_commit,
        "implementation_commit": observation.implementation_commit,
    }


def _advance_planning(_workspace: Path, planning: Path, _implementation: Path) -> None:
    _commit_file(planning, "planning-movement.txt", "accepted planning movement\n")


def _advance_implementation(
    _workspace: Path, _planning: Path, implementation: Path
) -> None:
    _commit_file(implementation, "unexpected.txt", "unexpected movement\n")


def _write_unexpected_workspace_path(
    workspace: Path, _planning: Path, _implementation: Path
) -> None:
    (workspace / "unexpected-workspace.txt").write_text(
        "unexpected fixture write\n", encoding="utf-8"
    )


def _write_untracked_implementation_path(
    _workspace: Path, _planning: Path, implementation: Path
) -> None:
    (implementation / "untracked.txt").write_text(
        "untracked implementation write\n", encoding="utf-8"
    )


def _write_undeclared_planning_path(
    _workspace: Path, planning: Path, _implementation: Path
) -> None:
    (planning / "undeclared.txt").write_text(
        "undeclared planning write\n", encoding="utf-8"
    )


def _init_repo(root: Path) -> None:
    root.mkdir()
    _git(root, "init", "--quiet")
    _git(root, "config", "user.email", "fixtures@example.invalid")
    _git(root, "config", "user.name", "Currentness Fixtures")
    (root / "identity.txt").write_text(f"{root.name}\n", encoding="utf-8")
    _git(root, "add", "identity.txt")
    _git(root, "commit", "--quiet", "-m", "Initialize fixture")


def _commit_file(root: Path, name: str, content: str) -> None:
    (root / name).write_text(content, encoding="utf-8")
    _git(root, "add", name)
    _git(root, "commit", "--quiet", "-m", f"Update {name}")


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, check=True, text=True, capture_output=True
    )
    return completed.stdout.strip()


def _snapshot_workspace(workspace: Path) -> dict[str, str]:
    return {
        path.relative_to(workspace).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in workspace.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(workspace).parts
    }


def _workspace_changes(before: Mapping[str, str], workspace: Path) -> list[str]:
    after = _snapshot_workspace(workspace)
    changed = {
        path
        for path in before.keys() | after.keys()
        if before.get(path) != after.get(path)
    }
    return sorted(f"workspace/{path}" for path in changed)


def _load_mapping(path: Path) -> Mapping[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError(f"expected mapping in {path}")
    return cast(Mapping[str, object], value)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_optional_json(path: Path, value: object | None) -> None:
    if value is not None:
        _write_json(path, value)
