#!/usr/bin/env python3
"""Deterministic ``plan-batch/v1`` validation and DEC-038 apply boundary.

The installed skill owns agent orchestration and planning decisions.  This
module accepts the two direct role results, proves their exact lineage and
quality gates, and only then delegates the already-decided four-stage mutation
to the planning contract store.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Literal, cast


_INVOCATION_ROOT = Path(__file__).parent.parent.absolute()
_INVOCATION_ROOT_TEXT = str(_INVOCATION_ROOT)
sys.path[:] = [entry for entry in sys.path if entry != _INVOCATION_ROOT_TEXT]
sys.path.insert(0, _INVOCATION_ROOT_TEXT)
_SCRIPTS_ROOT = str(_INVOCATION_ROOT / "scripts")
_scripts_package = sys.modules.get("scripts")
if _scripts_package is None:
    _scripts_package = ModuleType("scripts")
    sys.modules["scripts"] = _scripts_package
setattr(_scripts_package, "__path__", [_SCRIPTS_ROOT])
_loaded_store = sys.modules.get("scripts.planning_contract")
if _loaded_store is not None:
    _loaded_store_path = getattr(_loaded_store, "__file__", None)
    if (
        not isinstance(_loaded_store_path, str)
        or Path(_loaded_store_path).resolve(strict=False)
        != (_INVOCATION_ROOT / "scripts/planning_contract.py").resolve(strict=False)
    ):
        del sys.modules["scripts.planning_contract"]

from scripts.planning_contract import (  # noqa: E402
    ArtifactLineage,
    PlanningStoreError,
    ProducerIdentity,
    SelectionFaultPoint,
    SelectionTransactionRequest,
    read_current_document,
    read_ledger_document,
    simulate_selection_transaction,
)


INTERFACE = "plan-batch/v1"
RESULT_INTERFACE = "plan-batch-result/v1"
PLANNER_INTERFACE = "batch-plan-draft/v1"
REVIEWER_INTERFACE = "batch-plan-review/v1"
_HEX_40_LENGTH = 40
_HEX_64_LENGTH = 64
_CONTEXT_FIELDS = frozenset(
    {
        "toolchain_generation",
        "toolchain_commit",
        "toolchain_root",
        "canonical_planning_repository_root",
        "canonical_planning_commit",
        "planning_root",
        "operation_root_kind",
        "canonical_state_mutation_allowed",
    }
)
_STATE_FIELDS = frozenset(
    {
        "current_status",
        "validate_status",
        "semantic_state",
        "current_revision",
        "current_file_hash",
        "selected_dispatch",
        "queued_runway",
        "active_runway",
    }
)
_TRANSACTION_FIELDS = frozenset(
    {
        "transaction_id",
        "transaction_path",
        "current_path",
        "expected_initial_state_revision",
        "expected_initial_state_file_hash",
        "initial_current_contract",
        "lineage",
        "command_owner_version",
        "producer",
    }
)
_LINEAGE_FIELDS = frozenset(
    {
        "planning_root",
        "program",
        "batch_id",
        "included_finding_ids",
        "deferred_finding_ids",
        "batch_kind",
        "ledger_path",
        "ledger_revision",
        "dispatch_path",
        "dispatch_revision",
        "runway_path",
        "closeout_path",
        "toolchain_source_root",
        "canonical_planning_repository_root",
        "implementation_target_root",
        "dispatch_producer",
        "runway_producer",
        "closeout_producer",
    }
)
_PRODUCER_FIELDS = frozenset(
    {"toolchain_generation", "toolchain_commit", "schema_version"}
)
_PLANNER_FIELDS = frozenset({"interface", "status", "draft", "blockers"})
_DRAFT_FIELDS = frozenset(
    {"dispatch", "runway", "basis", "quality", "validation_profile"}
)
_BASIS_FIELDS = frozenset(
    {
        "current_revision",
        "current_file_hash",
        "ledger_path",
        "ledger_file_hash",
        "finding_id",
        "finding_revision",
    }
)
_QUALITY_FIELDS = frozenset(
    {
        "minimum_viable_scope",
        "scope_expansions",
        "proportionality",
        "slice_rationales",
        "unresolved_decisions",
        "residual_complexity",
        "destructive_actions",
        "implementation_started",
    }
)
_RATIONALE_FIELDS = frozenset({"slice_id", "kind", "reason"})
_APPROVAL_NEED_FIELDS = frozenset({"id", "scope"})
_APPROVAL_FIELDS = frozenset({"scope", "decision"})
_PROPORTIONALITY_FIELDS = frozenset(
    {
        "observed_failure",
        "invariants",
        "minimum_viable_change",
        "proposed_change",
        "additions_beyond_minimum",
        "simpler_alternatives_rejected",
        "verdict",
    }
)
_PROPORTIONALITY_ADDITION_FIELDS = frozenset(
    {"addition", "prevented_failure", "minimum_insufficient_reason"}
)
_SIMPLER_ALTERNATIVE_FIELDS = frozenset({"alternative", "reason"})
_REVIEW_EVIDENCE_FIELDS = frozenset({"packet", "packet_sha256"})
_EVIDENCE_PACKET_FIELDS = frozenset(
    {
        "source_evidence",
        "user_constraints",
        "planning_state_diagnostics",
        "proportionality",
        "approvals",
        "draft",
        "selected_dispatch",
        "invocation_lineage",
    }
)
_SOURCE_EVIDENCE_FIELDS = frozenset(
    {"source_id", "source_commit", "source_section", "content", "sha256"}
)
_DIAGNOSTIC_IDENTITY_FIELDS = frozenset({"current_sha256", "validate_sha256"})
_INVOCATION_LINEAGE_FIELDS = frozenset({"planner", "reviewer"})
_CORRECTION_HISTORY_FIELDS = frozenset({"draft_sha256", "correction", "material"})
_INVOCATION_FIELDS = frozenset({"role", "caller", "direct", "invocation_id"})
_REVIEW_FIELDS = frozenset(
    {
        "interface",
        "verdict",
        "review_basis",
        "checks",
        "corrections",
        "blockers",
        "implementation_started",
    }
)
_REVIEW_BASIS_FIELDS = frozenset(
    {
        "selected_dispatch_sha256",
        "draft_sha256",
        "approvals_sha256",
        "evidence_packet_sha256",
    }
)
_REVIEW_CHECK_FIELDS = frozenset(
    {
        "currentness",
        "selection",
        "scope",
        "proportionality",
        "lineage",
        "approval_scope",
        "semantic_slices",
        "stop_boundary",
    }
)
_SEMANTIC_SLICE_KINDS = frozenset(
    {
        "cohesive",
        "producer-consumer",
        "risk-boundary",
        "validation-boundary",
        "migration-boundary",
        "contract-boundary",
    }
)

JsonValue = str | int | float | bool | None | dict[str, "JsonValue"] | list["JsonValue"]
JsonObject = dict[str, JsonValue]
OperationRootKind = Literal["canonical", "temporary", "fixture"]


@dataclass(frozen=True)
class _BoundContext:
    toolchain_generation: Literal["stable", "candidate"]
    toolchain_commit: str
    toolchain_root: Path
    canonical_planning_repository_root: Path
    canonical_planning_commit: str
    planning_root: Path
    operation_root_kind: OperationRootKind
    canonical_state_mutation_allowed: bool


@dataclass(frozen=True)
class _PreparedPlan:
    context: _BoundContext
    transaction: SelectionTransactionRequest
    finding_id: str
    dispatch_sha256: str
    draft_sha256: str
    approvals_sha256: str
    evidence_packet_sha256: str


class PlanBatchBlocked(ValueError):
    """Expected fail-closed owner result produced before queue mutation."""

    def __init__(self, code: str, message: str, *, next_action: str = "stop") -> None:
        super().__init__(message)
        self.code = code
        self.next_action = next_action


def execute_plan_batch(
    request: Mapping[str, object],
    *,
    fault: SelectionFaultPoint | None = None,
) -> JsonObject:
    """Validate one exact reviewed plan and apply DEC-038 at most once."""

    try:
        prepared = _prepare_plan(request)
        result = simulate_selection_transaction(
            prepared.transaction,
            toolchain_root=prepared.context.toolchain_root,
            fault=fault,
        )
    except PlanBatchBlocked as error:
        return _blocked_result(error)
    except PlanningStoreError as error:
        return _blocked_result(
            PlanBatchBlocked(f"transaction.{error.code}", str(error), next_action="resume")
        )

    return cast(
        JsonObject,
        {
            "interface": RESULT_INTERFACE,
            "outcome": "queued",
            "write_status": "queued",
            "selected_finding_ids": [prepared.finding_id],
            "dispatch_path": str(prepared.transaction.lineage.dispatch_path),
            "runway_path": str(prepared.transaction.lineage.runway_path),
            "transaction_path": str(prepared.transaction.transaction_path),
            "transaction": {
                "outcome": result.outcome,
                "current_revision": result.current_revision,
                "dispatch_revision": result.dispatch_revision,
                "runway_revision": result.runway_revision,
                "transaction_file_hash": result.transaction_file_hash,
            },
            "review_basis": {
                "selected_dispatch_sha256": prepared.dispatch_sha256,
                "draft_sha256": prepared.draft_sha256,
                "approvals_sha256": prepared.approvals_sha256,
                "evidence_packet_sha256": prepared.evidence_packet_sha256,
            },
            "blockers": [],
            "next_action": "stop_before_implementation",
            "implementation_started": False,
        },
    )


def _prepare_plan(request: Mapping[str, object]) -> _PreparedPlan:
    _require_exact_fields(
        request,
        {
            "interface",
            "context",
            "planning_state",
            "planner_invocation",
            "planner_result",
            "reviewer_invocation",
            "reviewer_result",
            "approvals",
            "review_evidence",
            "validation_catalog",
            "correction_history",
            "transaction",
        },
        "request",
    )
    if request.get("interface") != INTERFACE:
        raise PlanBatchBlocked("request.interface", f"interface must be {INTERFACE!r}")

    context = _bind_context(_require_mapping(request, "context", "request"))
    transaction_raw = _require_mapping(request, "transaction", "request")
    transaction = _bind_transaction(transaction_raw, context)
    planning_state = _require_mapping(request, "planning_state", "request")
    _validate_planning_state(planning_state, transaction, context)

    planner_invocation = _require_mapping(request, "planner_invocation", "request")
    _validate_invocation(
        planner_invocation,
        role="batch_planner",
    )
    planner = _require_mapping(request, "planner_result", "request")
    draft = _validate_planner_result(planner)
    reviewer_invocation = _require_mapping(request, "reviewer_invocation", "request")
    _validate_invocation(
        reviewer_invocation,
        role="batch_plan_reviewer",
    )

    finding_id, source_id, source_commit, source_section = (
        _validate_selection_and_basis(draft, transaction, context)
    )
    approvals = _require_sequence(request, "approvals", "request")
    _validate_quality(draft, approvals)
    _validate_validation_profile(
        draft,
        _require_sequence(request, "validation_catalog", "request"),
    )
    dispatch = _require_mapping(draft, "dispatch", "planner_result.draft")
    runway = _require_mapping(draft, "runway", "planner_result.draft")
    dispatch_sha256 = _mapping_digest(dispatch)
    draft_sha256 = _mapping_digest(draft)
    approvals_sha256 = _value_digest(approvals)
    evidence_packet_sha256 = _validate_review_evidence(
        _require_mapping(request, "review_evidence", "request"),
        transaction=transaction,
        planner_invocation=planner_invocation,
        reviewer_invocation=reviewer_invocation,
        draft=draft,
        approvals=approvals,
        selected_source_id=source_id,
        selected_source_commit=source_commit,
        selected_source_section=source_section,
    )
    _validate_review(
        _require_mapping(request, "reviewer_result", "request"),
        dispatch_sha256=dispatch_sha256,
        draft_sha256=draft_sha256,
        approvals_sha256=approvals_sha256,
        evidence_packet_sha256=evidence_packet_sha256,
        correction_history=_require_sequence(
            request, "correction_history", "request"
        ),
    )
    _validate_transaction_contracts(transaction, dispatch, runway)
    transaction = SelectionTransactionRequest(
        transaction_id=transaction.transaction_id,
        transaction_path=transaction.transaction_path,
        current_path=transaction.current_path,
        expected_initial_state_revision=transaction.expected_initial_state_revision,
        expected_initial_state_file_hash=transaction.expected_initial_state_file_hash,
        initial_current_contract=transaction.initial_current_contract,
        lineage=transaction.lineage,
        dispatch_contract=_json_copy(dispatch),
        runway_contract=_json_copy(runway),
        command_owner_version=transaction.command_owner_version,
        producer=transaction.producer,
    )
    return _PreparedPlan(
        context=context,
        transaction=transaction,
        finding_id=finding_id,
        dispatch_sha256=dispatch_sha256,
        draft_sha256=draft_sha256,
        approvals_sha256=approvals_sha256,
        evidence_packet_sha256=evidence_packet_sha256,
    )


def _bind_context(raw: Mapping[str, object]) -> _BoundContext:
    _require_exact_fields(raw, _CONTEXT_FIELDS, "context")
    generation = _require_string(raw, "toolchain_generation", "context")
    if generation not in {"stable", "candidate"}:
        raise PlanBatchBlocked("context.generation", "unsupported toolchain generation")
    toolchain_root = _require_root(raw, "toolchain_root", "context")
    canonical_root = _require_root(
        raw, "canonical_planning_repository_root", "context"
    )
    planning_root = _require_root(raw, "planning_root", "context")
    toolchain_commit = _require_hash(
        raw, "toolchain_commit", "context", length=_HEX_40_LENGTH
    )
    canonical_commit = _require_hash(
        raw, "canonical_planning_commit", "context", length=_HEX_40_LENGTH
    )
    if _git_head(toolchain_root) != toolchain_commit:
        raise PlanBatchBlocked("context.toolchain_moved", "toolchain HEAD moved")
    if _git_head(canonical_root) != canonical_commit:
        raise PlanBatchBlocked("context.canonical_moved", "canonical planning HEAD moved")
    kind = _require_string(raw, "operation_root_kind", "context")
    if kind not in {"canonical", "temporary", "fixture"}:
        raise PlanBatchBlocked("context.root_kind", "unsupported operation root kind")
    mutation_allowed = _require_bool(
        raw, "canonical_state_mutation_allowed", "context"
    )
    if kind == "canonical":
        if generation != "stable" or not mutation_allowed:
            raise PlanBatchBlocked(
                "context.canonical_authority",
                "canonical planning writes require stable mutation authority",
            )
        _require_within(planning_root, canonical_root, "context.planning_root")
    elif mutation_allowed:
        raise PlanBatchBlocked(
            "context.noncanonical_authority",
            "temporary and fixture roots cannot claim canonical mutation authority",
        )
    elif _path_is_within(planning_root, canonical_root):
        raise PlanBatchBlocked(
            "context.root_kind_bypass",
            "temporary and fixture planning roots must be outside the canonical planning repository",
        )
    return _BoundContext(
        toolchain_generation=cast(Literal["stable", "candidate"], generation),
        toolchain_commit=toolchain_commit,
        toolchain_root=toolchain_root,
        canonical_planning_repository_root=canonical_root,
        canonical_planning_commit=canonical_commit,
        planning_root=planning_root,
        operation_root_kind=cast(OperationRootKind, kind),
        canonical_state_mutation_allowed=mutation_allowed,
    )


def _bind_transaction(
    raw: Mapping[str, object], context: _BoundContext
) -> SelectionTransactionRequest:
    _require_exact_fields(raw, _TRANSACTION_FIELDS, "transaction")
    lineage_raw = _require_mapping(raw, "lineage", "transaction")
    _require_exact_fields(lineage_raw, _LINEAGE_FIELDS, "transaction.lineage")
    lineage = ArtifactLineage(
        planning_root=_require_path(lineage_raw, "planning_root", "transaction.lineage"),
        program=_require_string(lineage_raw, "program", "transaction.lineage"),
        batch_id=_require_string(lineage_raw, "batch_id", "transaction.lineage"),
        included_finding_ids=tuple(
            _require_string_list(
                lineage_raw, "included_finding_ids", "transaction.lineage"
            )
        ),
        deferred_finding_ids=tuple(
            _require_string_list(
                lineage_raw, "deferred_finding_ids", "transaction.lineage"
            )
        ),
        batch_kind=_require_string(lineage_raw, "batch_kind", "transaction.lineage"),
        ledger_path=_require_path(lineage_raw, "ledger_path", "transaction.lineage"),
        ledger_revision=_require_hash(
            lineage_raw, "ledger_revision", "transaction.lineage", length=_HEX_64_LENGTH
        ),
        dispatch_path=_require_path(
            lineage_raw, "dispatch_path", "transaction.lineage"
        ),
        dispatch_revision=_require_hash(
            lineage_raw,
            "dispatch_revision",
            "transaction.lineage",
            length=_HEX_64_LENGTH,
        ),
        runway_path=_require_path(lineage_raw, "runway_path", "transaction.lineage"),
        closeout_path=_require_path(
            lineage_raw, "closeout_path", "transaction.lineage"
        ),
        toolchain_source_root=_require_path(
            lineage_raw, "toolchain_source_root", "transaction.lineage"
        ),
        canonical_planning_repository_root=_require_path(
            lineage_raw,
            "canonical_planning_repository_root",
            "transaction.lineage",
        ),
        implementation_target_root=_require_path(
            lineage_raw, "implementation_target_root", "transaction.lineage"
        ),
        dispatch_producer=_bind_producer(
            _require_mapping(lineage_raw, "dispatch_producer", "transaction.lineage"),
            label="transaction.lineage.dispatch_producer",
            schema="planning-dispatch/v1",
        ),
        runway_producer=_bind_producer(
            _require_mapping(lineage_raw, "runway_producer", "transaction.lineage"),
            label="transaction.lineage.runway_producer",
            schema="planning-runway/v1",
        ),
        closeout_producer=_bind_producer(
            _require_mapping(lineage_raw, "closeout_producer", "transaction.lineage"),
            label="transaction.lineage.closeout_producer",
            schema="planning-closeout/v1",
        ),
    )
    transaction = SelectionTransactionRequest(
        transaction_id=_require_string(raw, "transaction_id", "transaction"),
        transaction_path=_require_path(raw, "transaction_path", "transaction"),
        current_path=_require_path(raw, "current_path", "transaction"),
        expected_initial_state_revision=_require_int(
            raw, "expected_initial_state_revision", "transaction"
        ),
        expected_initial_state_file_hash=_require_hash(
            raw,
            "expected_initial_state_file_hash",
            "transaction",
            length=_HEX_64_LENGTH,
        ),
        initial_current_contract=_json_copy(
            _require_mapping(raw, "initial_current_contract", "transaction")
        ),
        lineage=lineage,
        dispatch_contract={},
        runway_contract={},
        command_owner_version=_require_string(
            raw, "command_owner_version", "transaction"
        ),
        producer=_bind_producer(
            _require_mapping(raw, "producer", "transaction"),
            label="transaction.producer",
            schema="planning-selection-transaction/v1",
        ),
    )
    for label, producer in (
        ("transaction.producer", transaction.producer),
        ("transaction.lineage.dispatch_producer", lineage.dispatch_producer),
        ("transaction.lineage.runway_producer", lineage.runway_producer),
    ):
        _require_producer_context(producer, context, label=label)
    if lineage.planning_root.resolve(strict=False) != context.planning_root:
        raise PlanBatchBlocked(
            "transaction.planning_root", "transaction planning root does not match context"
        )
    for label, path in (
        ("current_path", transaction.current_path),
        ("ledger_path", lineage.ledger_path),
        ("dispatch_path", lineage.dispatch_path),
        ("runway_path", lineage.runway_path),
        ("closeout_path", lineage.closeout_path),
        ("transaction_path", transaction.transaction_path),
    ):
        _require_within(path, context.planning_root, f"transaction.{label}")
    if (
        context.operation_root_kind == "canonical"
        and lineage.canonical_planning_repository_root.resolve(strict=False)
        != context.canonical_planning_repository_root
    ):
        raise PlanBatchBlocked(
            "transaction.canonical_root",
            "transaction canonical planning repository root does not match context",
        )
    if lineage.toolchain_source_root.resolve(strict=False) != context.toolchain_root:
        raise PlanBatchBlocked(
            "transaction.toolchain_root",
            "transaction toolchain source root does not match context",
        )
    return transaction


def _validate_planning_state(
    raw: Mapping[str, object],
    transaction: SelectionTransactionRequest,
    context: _BoundContext,
) -> None:
    _require_exact_fields(raw, _STATE_FIELDS, "planning_state")
    if raw.get("current_status") != "valid" or raw.get("validate_status") != "valid":
        raise PlanBatchBlocked(
            "planning_state.invalid",
            "planning_state current and validate must both be valid",
        )
    try:
        current = read_current_document(
            transaction.current_path, toolchain_root=context.toolchain_root
        )
    except (OSError, PlanningStoreError) as error:
        raise PlanBatchBlocked("planning_state.current", str(error)) from error
    observed_revision = _require_int(raw, "current_revision", "planning_state")
    observed_hash = _require_hash(
        raw, "current_file_hash", "planning_state", length=_HEX_64_LENGTH
    )
    if observed_revision != current.logical_revision or observed_hash != current.file_hash:
        raise PlanBatchBlocked(
            "planning_state.stale",
            "planning_state evidence is stale relative to CURRENT.md",
        )
    transaction_started = (
        transaction.transaction_path.is_file()
        and transaction.transaction_path.stat().st_size > 0
    )
    initial_state_matches = (
        transaction.expected_initial_state_revision == current.logical_revision
        and transaction.expected_initial_state_file_hash == current.file_hash
        and _json_copy(current.contract) == _json_copy(transaction.initial_current_contract)
    )
    pointers = {
        "selected_dispatch": current.contract["selected_dispatch"],
        "queued_runway": current.contract["queued_runway"],
        "active_runway": current.contract["active_runway"],
    }
    for key, value in pointers.items():
        if raw.get(key) != value:
            raise PlanBatchBlocked(
                "planning_state.pointer_mismatch",
                f"planning_state {key} does not match CURRENT.md",
            )
    state = _require_string(raw, "semantic_state", "planning_state")
    expected_state = next((name for name, value in pointers.items() if value is not None), "idle")
    expected_state = {
        "selected_dispatch": "selected",
        "queued_runway": "queued",
        "active_runway": "active",
        "idle": "idle",
    }[expected_state]
    if state != expected_state:
        raise PlanBatchBlocked(
            "planning_state.semantic_state",
            "planning_state semantic state does not match active pointers",
        )
    if state == "active" or (state != "idle" and not transaction_started):
        raise PlanBatchBlocked(
            f"planning_state.{state}",
            f"existing {state} work must be reported without queue mutation",
            next_action="report_existing_state",
        )
    if not initial_state_matches and not transaction_started:
        raise PlanBatchBlocked(
            "planning_state.transaction_basis",
            "transaction initial state does not equal current Planning State evidence",
        )


def _validate_invocation(raw: Mapping[str, object], *, role: str) -> None:
    _require_exact_fields(raw, _INVOCATION_FIELDS, f"{role}_invocation")
    if raw.get("role") != role or raw.get("caller") != "plan-batch":
        raise PlanBatchBlocked(
            "roles.direct_invocation",
            f"{role} must be directly invoked by plan-batch",
        )
    if raw.get("direct") is not True:
        raise PlanBatchBlocked(
            "roles.direct_invocation", f"{role} invocation must be direct"
        )
    _require_string(raw, "invocation_id", f"{role}_invocation")


def _validate_planner_result(raw: Mapping[str, object]) -> Mapping[str, object]:
    _require_exact_fields(raw, _PLANNER_FIELDS, "planner_result")
    if raw.get("interface") != PLANNER_INTERFACE:
        raise PlanBatchBlocked("planner.interface", "planner result interface is invalid")
    blockers = _require_string_list(raw, "blockers", "planner_result")
    status = raw.get("status")
    if status == "blocked":
        if raw.get("draft") is not None:
            raise PlanBatchBlocked(
                "planner.blocked_draft", "blocked planner result must not carry a draft"
            )
        if not blockers:
            raise PlanBatchBlocked(
                "planner.blocked_without_reason", "blocked planner result needs blockers"
            )
        raise PlanBatchBlocked(
            "planner.blocked", blockers[0], next_action="resolve_planning_blocker"
        )
    if status != "ready" or blockers:
        raise PlanBatchBlocked("planner.status", "planner result is not ready")
    draft = _require_mapping(raw, "draft", "planner_result")
    _require_exact_fields(draft, _DRAFT_FIELDS, "planner_result.draft")
    return draft


def _validate_selection_and_basis(
    draft: Mapping[str, object],
    transaction: SelectionTransactionRequest,
    context: _BoundContext,
) -> tuple[str, str, str, str]:
    lineage = transaction.lineage
    if len(lineage.included_finding_ids) != 1:
        raise PlanBatchBlocked(
            "selection.one_finding",
            "plan-batch selects exactly one existing finding per transaction",
        )
    finding_id = lineage.included_finding_ids[0]
    if finding_id in lineage.deferred_finding_ids:
        raise PlanBatchBlocked(
            "selection.repeated_finding", "selected finding cannot also be deferred"
        )
    if len(set(lineage.deferred_finding_ids)) != len(lineage.deferred_finding_ids):
        raise PlanBatchBlocked(
            "selection.repeated_finding", "deferred finding identities must be unique"
        )
    basis = _require_mapping(draft, "basis", "planner_result.draft")
    _require_exact_fields(basis, _BASIS_FIELDS, "planner_result.draft.basis")
    if basis.get("finding_id") != finding_id:
        raise PlanBatchBlocked("selection.finding", "draft basis finding does not match lineage")
    if _require_int(basis, "current_revision", "planner_result.draft.basis") != (
        transaction.expected_initial_state_revision
    ):
        raise PlanBatchBlocked("draft.stale", "draft current revision is stale")
    if _require_hash(
        basis,
        "current_file_hash",
        "planner_result.draft.basis",
        length=_HEX_64_LENGTH,
    ) != transaction.expected_initial_state_file_hash:
        raise PlanBatchBlocked("draft.stale", "draft current hash is stale")
    ledger_path = _require_path(basis, "ledger_path", "planner_result.draft.basis")
    if ledger_path.resolve(strict=False) != lineage.ledger_path.resolve(strict=False):
        raise PlanBatchBlocked("draft.ledger", "draft ledger path does not match lineage")
    ledger_hash = _file_hash(ledger_path)
    if _require_hash(
        basis,
        "ledger_file_hash",
        "planner_result.draft.basis",
        length=_HEX_64_LENGTH,
    ) != ledger_hash:
        raise PlanBatchBlocked("draft.stale", "draft ledger hash is stale")
    try:
        ledger = read_ledger_document(ledger_path, toolchain_root=context.toolchain_root)
    except (OSError, PlanningStoreError) as error:
        raise PlanBatchBlocked("selection.ledger", str(error)) from error
    finding = ledger.findings.get(finding_id)
    if finding is None:
        raise PlanBatchBlocked(
            "selection.missing_finding", "selected finding is absent from the canonical ledger"
        )
    finding_revision = finding.get("revision")
    if (
        isinstance(finding_revision, bool)
        or not isinstance(finding_revision, int)
        or basis.get("finding_revision") != finding_revision
    ):
        raise PlanBatchBlocked("draft.stale", "draft finding revision is stale")
    lifecycle = finding.get("lifecycle")
    if not isinstance(lifecycle, Mapping) or cast(
        Mapping[str, object], lifecycle
    ).get("status") != "open":
        raise PlanBatchBlocked(
            "selection.ineligible_finding", "selected finding must be open"
        )
    provenance = finding.get("provenance")
    if not isinstance(provenance, Mapping):
        raise PlanBatchBlocked(
            "selection.source_evidence", "selected finding provenance is unavailable"
        )
    source_id = cast(Mapping[str, object], provenance).get("source_id")
    if not isinstance(source_id, str) or not source_id.strip():
        raise PlanBatchBlocked(
            "selection.source_evidence", "selected finding source identity is unavailable"
        )
    typed_provenance = cast(Mapping[str, object], provenance)
    source_commit = typed_provenance.get("source_commit")
    source_section = typed_provenance.get("source_section")
    if (
        not isinstance(source_commit, str)
        or len(source_commit) != _HEX_40_LENGTH
        or any(character not in "0123456789abcdef" for character in source_commit)
        or not isinstance(source_section, str)
        or not source_section.strip()
    ):
        raise PlanBatchBlocked(
            "selection.source_evidence",
            "selected finding source commit or section is unavailable",
        )
    dispatch = _require_mapping(draft, "dispatch", "planner_result.draft")
    source = _require_mapping(dispatch, "source", "planner_result.draft.dispatch")
    scope = _require_mapping(dispatch, "scope", "planner_result.draft.dispatch")
    if source.get("finding_ids") != [finding_id] or scope.get("included_finding_ids") != [
        finding_id
    ]:
        raise PlanBatchBlocked(
            "selection.dispatch_binding",
            "dispatch must bind the same single selected finding",
        )
    if scope.get("deferred_finding_ids") != list(lineage.deferred_finding_ids):
        raise PlanBatchBlocked(
            "selection.deferred_binding",
            "dispatch deferred finding identities do not match lineage",
        )
    return finding_id, source_id, source_commit, source_section


def _validate_quality(
    draft: Mapping[str, object], raw_approvals: Sequence[object]
) -> None:
    quality = _require_mapping(draft, "quality", "planner_result.draft")
    _require_exact_fields(quality, _QUALITY_FIELDS, "planner_result.draft.quality")
    if quality.get("minimum_viable_scope") is not True:
        raise PlanBatchBlocked(
            "quality.minimum_viable_scope",
            "draft expands beyond the minimum viable change",
        )
    expansions = _require_string_list(
        quality, "scope_expansions", "planner_result.draft.quality"
    )
    if expansions:
        raise PlanBatchBlocked(
            "quality.scope_expansion", "draft contains unrelated scope expansion"
        )
    proportionality = _require_mapping(
        quality, "proportionality", "planner_result.draft.quality"
    )
    _validate_proportionality(proportionality)
    unresolved = _require_string_list(
        quality, "unresolved_decisions", "planner_result.draft.quality"
    )
    if unresolved:
        raise PlanBatchBlocked(
            "quality.unresolved_decisions",
            "draft has unresolved user decisions",
            next_action="ask_user",
        )
    if quality.get("implementation_started") is not False:
        raise PlanBatchBlocked(
            "quality.stop_boundary", "planning must stop before implementation"
        )
    runway = _require_mapping(draft, "runway", "planner_result.draft")
    slices = _require_sequence(runway, "slices", "planner_result.draft.runway")
    if not slices:
        raise PlanBatchBlocked("quality.slices", "runway needs at least one semantic slice")
    raw_rationales = _require_sequence(
        quality, "slice_rationales", "planner_result.draft.quality"
    )
    if len(raw_rationales) != len(slices):
        raise PlanBatchBlocked(
            "quality.slice_rationales", "every slice needs one semantic rationale"
        )
    slice_ids: list[str] = []
    for index, value in enumerate(slices):
        slice_item = _mapping_item(value, index, "planner_result.draft.runway.slices")
        slice_ids.append(_require_string(slice_item, "id", f"runway.slices[{index}]"))
    rationale_ids: list[str] = []
    for index, value in enumerate(raw_rationales):
        rationale = _mapping_item(value, index, "quality.slice_rationales")
        _require_exact_fields(
            rationale,
            _RATIONALE_FIELDS,
            f"quality.slice_rationales[{index}]",
        )
        rationale_ids.append(
            _require_string(rationale, "slice_id", f"quality.slice_rationales[{index}]")
        )
        kind = _require_string(rationale, "kind", f"quality.slice_rationales[{index}]")
        if kind not in _SEMANTIC_SLICE_KINDS:
            raise PlanBatchBlocked(
                "quality.filler_slice", "slice rationale is not a semantic boundary"
            )
        if len(slices) > 1 and kind == "cohesive":
            raise PlanBatchBlocked(
                "quality.filler_slice",
                "multi-slice plans require justified producer/consumer or risk boundaries",
            )
        _require_string(rationale, "reason", f"quality.slice_rationales[{index}]")
    if slice_ids != rationale_ids or len(set(slice_ids)) != len(slice_ids):
        raise PlanBatchBlocked(
            "quality.slice_rationales", "slice rationales must bind every unique slice in order"
        )
    dispatch = _require_mapping(draft, "dispatch", "planner_result.draft")
    required_scopes = [
        *_require_string_list(dispatch, "approval_gates", "planner_result.draft.dispatch"),
        *(
            item["scope"]
            for item in (
                *_approval_needs(quality, "residual_complexity"),
                *_approval_needs(quality, "destructive_actions"),
            )
        ),
    ]
    if len(required_scopes) != len(set(required_scopes)):
        raise PlanBatchBlocked(
            "quality.approval_declaration_duplicate",
            "approval scopes must be declared exactly once across dispatch and quality",
        )
    approvals = _approval_scopes(raw_approvals)
    missing = sorted(set(required_scopes) - set(approvals))
    if missing:
        raise PlanBatchBlocked(
            "quality.approval_scope",
            f"required narrowly scoped approval is missing: {missing[0]}",
            next_action="ask_user",
        )
    unrelated = sorted(set(approvals) - set(required_scopes))
    if unrelated:
        raise PlanBatchBlocked(
            "quality.approval_unrelated",
            f"approval is unrelated to a declared gate: {unrelated[0]}",
            next_action="ask_user",
        )
    if approvals != required_scopes:
        raise PlanBatchBlocked(
            "quality.approval_order",
            "approval records must follow declared gate order exactly",
            next_action="ask_user",
        )


def _validate_proportionality(raw: Mapping[str, object]) -> None:
    _require_exact_fields(raw, _PROPORTIONALITY_FIELDS, "proportionality")
    _require_string(raw, "observed_failure", "proportionality")
    invariants = _require_string_list(raw, "invariants", "proportionality")
    if not invariants:
        raise PlanBatchBlocked(
            "quality.proportionality",
            "proportionality must preserve at least one explicit invariant",
        )
    minimum = _require_string(raw, "minimum_viable_change", "proportionality")
    proposed = _require_string(raw, "proposed_change", "proportionality")
    additions = _require_sequence(
        raw, "additions_beyond_minimum", "proportionality"
    )
    for index, value in enumerate(additions):
        item = _mapping_item(value, index, "proportionality.additions_beyond_minimum")
        _require_exact_fields(
            item,
            _PROPORTIONALITY_ADDITION_FIELDS,
            f"proportionality.additions_beyond_minimum[{index}]",
        )
        _require_string(item, "addition", f"proportionality.additions_beyond_minimum[{index}]")
        _require_string(
            item,
            "prevented_failure",
            f"proportionality.additions_beyond_minimum[{index}]",
        )
        _require_string(
            item,
            "minimum_insufficient_reason",
            f"proportionality.additions_beyond_minimum[{index}]",
        )
    alternatives = _require_sequence(
        raw, "simpler_alternatives_rejected", "proportionality"
    )
    for index, value in enumerate(alternatives):
        item = _mapping_item(
            value, index, "proportionality.simpler_alternatives_rejected"
        )
        _require_exact_fields(
            item,
            _SIMPLER_ALTERNATIVE_FIELDS,
            f"proportionality.simpler_alternatives_rejected[{index}]",
        )
        _require_string(
            item,
            "alternative",
            f"proportionality.simpler_alternatives_rejected[{index}]",
        )
        _require_string(
            item,
            "reason",
            f"proportionality.simpler_alternatives_rejected[{index}]",
        )
    if minimum == proposed and additions:
        raise PlanBatchBlocked(
            "quality.proportionality",
            "a minimum proposal cannot declare additions beyond minimum",
        )
    if minimum != proposed and not additions:
        raise PlanBatchBlocked(
            "quality.proportionality",
            "a proposal beyond minimum must justify every addition",
        )
    if raw.get("verdict") != "proportionate":
        raise PlanBatchBlocked(
            "quality.proportionality",
            "over-specified proposals must be narrowed before review",
        )


def _validate_review(
    raw: Mapping[str, object],
    *,
    dispatch_sha256: str,
    draft_sha256: str,
    approvals_sha256: str,
    evidence_packet_sha256: str,
    correction_history: Sequence[object],
) -> None:
    _require_exact_fields(raw, _REVIEW_FIELDS, "reviewer_result")
    if raw.get("interface") != REVIEWER_INTERFACE:
        raise PlanBatchBlocked("review.interface", "reviewer result interface is invalid")
    if raw.get("implementation_started") is not False:
        raise PlanBatchBlocked("review.stop_boundary", "review started implementation")
    basis = _require_mapping(raw, "review_basis", "reviewer_result")
    _require_exact_fields(basis, _REVIEW_BASIS_FIELDS, "reviewer_result.review_basis")
    if basis.get("selected_dispatch_sha256") != dispatch_sha256:
        raise PlanBatchBlocked(
            "review.dispatch_basis", "review is not bound to the exact selected dispatch"
        )
    if basis.get("draft_sha256") != draft_sha256:
        raise PlanBatchBlocked(
            "review.draft_basis", "review is not bound to the exact planner draft"
        )
    if basis.get("approvals_sha256") != approvals_sha256:
        raise PlanBatchBlocked(
            "review.approval_basis",
            "review is not bound to the exact approval record",
        )
    if basis.get("evidence_packet_sha256") != evidence_packet_sha256:
        raise PlanBatchBlocked(
            "review.evidence_basis",
            "review is not bound to the exact independent evidence packet",
        )
    verdict = raw.get("verdict")
    corrections = _require_string_list(raw, "corrections", "reviewer_result")
    blockers = _require_string_list(raw, "blockers", "reviewer_result")
    repeated = _repeated_material_correction(
        correction_history,
        draft_sha256=draft_sha256,
        corrections=corrections,
    )
    checks = _require_mapping(raw, "checks", "reviewer_result")
    _require_exact_fields(checks, _REVIEW_CHECK_FIELDS, "reviewer_result.checks")
    failed = sorted(key for key, value in checks.items() if value != "pass")
    if verdict == "correction_required":
        if not corrections:
            raise PlanBatchBlocked(
                "review.correction_shape", "correction verdict requires corrections"
            )
        if repeated is not None:
            raise PlanBatchBlocked(
                "review.repeated_correction",
                f"material correction repeated against unchanged draft: {repeated}",
            )
        raise PlanBatchBlocked(
            "review.correction_required",
            corrections[0],
            next_action="return_to_batch_planner",
        )
    if verdict == "blocked":
        if not blockers:
            raise PlanBatchBlocked("review.blocked_shape", "blocked review needs blockers")
        raise PlanBatchBlocked(
            "review.blocked", blockers[0], next_action="resolve_review_blocker"
        )
    if verdict != "clean" or corrections or blockers:
        raise PlanBatchBlocked("review.verdict", "independent review is not clean")
    if failed:
        raise PlanBatchBlocked(
            "review.checks", f"review check did not pass: {failed[0]}"
        )


def _validate_validation_profile(
    draft: Mapping[str, object],
    catalog: Sequence[object],
) -> None:
    selected = _require_string(draft, "validation_profile", "planner_result.draft")
    if not catalog:
        raise PlanBatchBlocked(
            "validation_profile.catalog", "validation catalog must not be empty"
        )
    entries: list[str] = []
    for index, value in enumerate(catalog):
        if not isinstance(value, str) or not value.strip():
            raise PlanBatchBlocked(
                "validation_profile.catalog",
                f"validation_catalog[{index}] must be an opaque non-empty identifier",
            )
        profile_id = value
        if profile_id in entries:
            raise PlanBatchBlocked(
                "validation_profile.duplicate",
                "validation catalog profile identities must be unique",
            )
        entries.append(profile_id)
    if selected not in entries:
        raise PlanBatchBlocked(
            "validation_profile.selection",
            "planner selected a validation profile absent from the supplied catalog",
        )


def _validate_review_evidence(
    raw: Mapping[str, object],
    *,
    transaction: SelectionTransactionRequest,
    planner_invocation: Mapping[str, object],
    reviewer_invocation: Mapping[str, object],
    draft: Mapping[str, object],
    approvals: Sequence[object],
    selected_source_id: str,
    selected_source_commit: str,
    selected_source_section: str,
) -> str:
    _require_exact_fields(raw, _REVIEW_EVIDENCE_FIELDS, "review_evidence")
    packet = _require_mapping(raw, "packet", "review_evidence")
    _require_exact_fields(packet, _EVIDENCE_PACKET_FIELDS, "review_evidence.packet")
    sources = _require_sequence(packet, "source_evidence", "review_evidence.packet")
    source_ids: list[str] = []
    for index, value in enumerate(sources):
        item = _mapping_item(value, index, "review_evidence.packet.source_evidence")
        _require_exact_fields(
            item,
            _SOURCE_EVIDENCE_FIELDS,
            f"review_evidence.packet.source_evidence[{index}]",
        )
        source_id = _require_string(
            item, "source_id", f"review_evidence.packet.source_evidence[{index}]"
        )
        _require_hash(
            item,
            "source_commit",
            f"review_evidence.packet.source_evidence[{index}]",
            length=_HEX_40_LENGTH,
        )
        _require_string(
            item,
            "source_section",
            f"review_evidence.packet.source_evidence[{index}]",
        )
        content = _require_string(
            item, "content", f"review_evidence.packet.source_evidence[{index}]"
        )
        digest = _require_hash(
            item,
            "sha256",
            f"review_evidence.packet.source_evidence[{index}]",
            length=_HEX_64_LENGTH,
        )
        if hashlib.sha256(content.encode()).hexdigest() != digest:
            raise PlanBatchBlocked(
                "review_evidence.source_digest",
                f"source evidence {source_id!r} content digest does not match",
            )
        source_ids.append(source_id)
    if len(source_ids) != len(set(source_ids)) or selected_source_id not in source_ids:
        raise PlanBatchBlocked(
            "review_evidence.source_lineage",
            "review evidence must bind each source once and include the selected finding source",
        )
    selected_source = next(
        cast(Mapping[str, object], item)
        for item in sources
        if cast(Mapping[str, object], item).get("source_id") == selected_source_id
    )
    if (
        selected_source.get("source_commit") != selected_source_commit
        or selected_source.get("source_section") != selected_source_section
    ):
        raise PlanBatchBlocked(
            "review_evidence.source_lineage",
            "review evidence source commit and section do not match selected finding provenance",
        )
    constraints = _require_string_list(
        packet, "user_constraints", "review_evidence.packet"
    )
    if not constraints:
        raise PlanBatchBlocked(
            "review_evidence.user_constraints",
            "review evidence must carry explicit user constraints",
        )
    diagnostics = _require_mapping(
        packet, "planning_state_diagnostics", "review_evidence.packet"
    )
    _require_exact_fields(
        diagnostics, _DIAGNOSTIC_IDENTITY_FIELDS, "planning_state_diagnostics"
    )
    reviewed_planning_state = _reviewed_planning_state(transaction)
    for command in ("current", "validate"):
        expected = _diagnostic_identity(command, reviewed_planning_state)
        if diagnostics.get(f"{command}_sha256") != expected:
            raise PlanBatchBlocked(
                "review_evidence.planning_state",
                f"{command} diagnostic identity is stale or mismatched",
            )
    quality = _require_mapping(draft, "quality", "planner_result.draft")
    proportionality = _require_mapping(
        quality, "proportionality", "planner_result.draft.quality"
    )
    exact_bindings: tuple[tuple[str, object, object], ...] = (
        ("proportionality", packet.get("proportionality"), proportionality),
        ("approvals", packet.get("approvals"), approvals),
        ("draft", packet.get("draft"), draft),
        (
            "selected_dispatch",
            packet.get("selected_dispatch"),
            _require_mapping(draft, "dispatch", "planner_result.draft"),
        ),
    )
    for label, observed, expected in exact_bindings:
        if _thaw_json(observed) != _thaw_json(expected):
            raise PlanBatchBlocked(
                "review_evidence.binding",
                f"review evidence {label} does not match the command request",
            )
    lineage = _require_mapping(packet, "invocation_lineage", "review_evidence.packet")
    _require_exact_fields(
        lineage, _INVOCATION_LINEAGE_FIELDS, "review_evidence.invocation_lineage"
    )
    if _thaw_json(lineage.get("planner")) != _thaw_json(planner_invocation) or (
        _thaw_json(lineage.get("reviewer")) != _thaw_json(reviewer_invocation)
    ):
        raise PlanBatchBlocked(
            "review_evidence.invocation_lineage",
            "review evidence does not bind both direct invocation records",
        )
    packet_sha256 = _mapping_digest(packet)
    if raw.get("packet_sha256") != packet_sha256:
        raise PlanBatchBlocked(
            "review_evidence.digest",
            "review evidence packet digest does not match its exact contents",
        )
    return packet_sha256


def _reviewed_planning_state(
    transaction: SelectionTransactionRequest,
) -> Mapping[str, object]:
    """Reconstruct the immutable Planning State basis reviewed before DEC-038."""

    initial = transaction.initial_current_contract
    selected = initial.get("selected_dispatch")
    queued = initial.get("queued_runway")
    active = initial.get("active_runway")
    semantic = "active" if active else "queued" if queued else "selected" if selected else "idle"
    return {
        "current_status": "valid",
        "validate_status": "valid",
        "semantic_state": semantic,
        "current_revision": transaction.expected_initial_state_revision,
        "current_file_hash": transaction.expected_initial_state_file_hash,
        "selected_dispatch": selected,
        "queued_runway": queued,
        "active_runway": active,
    }


def _repeated_material_correction(
    history: Sequence[object],
    *,
    draft_sha256: str,
    corrections: Sequence[str],
) -> str | None:
    seen: set[tuple[str, str]] = set()
    for index, value in enumerate(history):
        item = _mapping_item(value, index, "correction_history")
        _require_exact_fields(
            item, _CORRECTION_HISTORY_FIELDS, f"correction_history[{index}]"
        )
        historical_digest = _require_hash(
            item,
            "draft_sha256",
            f"correction_history[{index}]",
            length=_HEX_64_LENGTH,
        )
        correction = _require_string(
            item, "correction", f"correction_history[{index}]"
        )
        material = _require_bool(item, "material", f"correction_history[{index}]")
        identity = (historical_digest, correction)
        if identity in seen:
            raise PlanBatchBlocked(
                "review.correction_history",
                "correction history identities must be unique",
            )
        seen.add(identity)
        if material and historical_digest == draft_sha256 and correction in corrections:
            return correction
    return None


def _validate_transaction_contracts(
    transaction: SelectionTransactionRequest,
    dispatch: Mapping[str, object],
    runway: Mapping[str, object],
) -> None:
    lineage = transaction.lineage
    artifact = _require_mapping(dispatch, "artifact", "planner_result.draft.dispatch")
    if artifact.get("id") != lineage.batch_id or artifact.get("program") != lineage.program:
        raise PlanBatchBlocked(
            "transaction.dispatch_lineage", "dispatch identity does not match transaction"
        )
    if artifact.get("revision") != lineage.dispatch_revision:
        raise PlanBatchBlocked(
            "transaction.dispatch_revision", "dispatch revision does not match lineage"
        )
    runway_artifact = _require_mapping(
        runway, "artifact", "planner_result.draft.runway"
    )
    if (
        runway_artifact.get("id") != lineage.batch_id
        or runway_artifact.get("source_dispatch")
        != _relative_to(lineage.dispatch_path, lineage.planning_root)
        or runway_artifact.get("source_dispatch_revision") != lineage.dispatch_revision
    ):
        raise PlanBatchBlocked(
            "transaction.runway_lineage", "runway does not bind the exact dispatch"
        )
    batch = _require_mapping(runway, "batch", "planner_result.draft.runway")
    if batch.get("status") != "queued" or batch.get("kind") != lineage.batch_kind:
        raise PlanBatchBlocked(
            "transaction.runway_state", "runway must be the exact queued batch"
        )
    execution = _require_mapping(runway, "execution", "planner_result.draft.runway")
    if execution.get("successor_selection") != "forbidden":
        raise PlanBatchBlocked(
            "transaction.successor", "runway must forbid successor selection"
        )
    dispatch_producer = _require_mapping(dispatch, "producer", "dispatch")
    runway_producer = _require_mapping(runway, "producer", "runway")
    if _json_copy(dispatch_producer) != _producer_object(lineage.dispatch_producer):
        raise PlanBatchBlocked(
            "transaction.dispatch_producer", "dispatch producer does not match lineage"
        )
    if _json_copy(runway_producer) != _producer_object(lineage.runway_producer):
        raise PlanBatchBlocked(
            "transaction.runway_producer", "runway producer does not match lineage"
        )


def _bind_producer(
    raw: Mapping[str, object], *, label: str, schema: str
) -> ProducerIdentity:
    _require_exact_fields(raw, _PRODUCER_FIELDS, label)
    generation = _require_string(raw, "toolchain_generation", label)
    if generation not in {"stable", "candidate"}:
        raise PlanBatchBlocked("producer.generation", f"{label} has invalid generation")
    commit = _require_hash(raw, "toolchain_commit", label, length=_HEX_40_LENGTH)
    if raw.get("schema_version") != schema:
        raise PlanBatchBlocked("producer.schema", f"{label} must use {schema}")
    return ProducerIdentity(cast(Literal["stable", "candidate"], generation), commit, schema)


def _require_producer_context(
    producer: ProducerIdentity, context: _BoundContext, *, label: str
) -> None:
    if (
        producer.toolchain_generation != context.toolchain_generation
        or producer.toolchain_commit != context.toolchain_commit
    ):
        raise PlanBatchBlocked(
            "producer.lineage",
            f"{label} must bind the exact command-owner generation and commit",
        )


def _approval_needs(
    quality: Mapping[str, object], key: str
) -> tuple[dict[str, str], ...]:
    raw = _require_sequence(quality, key, "planner_result.draft.quality")
    needs: list[dict[str, str]] = []
    for index, value in enumerate(raw):
        item = _mapping_item(value, index, f"quality.{key}")
        _require_exact_fields(item, _APPROVAL_NEED_FIELDS, f"quality.{key}[{index}]")
        needs.append(
            {
                "id": _require_string(item, "id", f"quality.{key}[{index}]"),
                "scope": _require_string(item, "scope", f"quality.{key}[{index}]"),
            }
        )
    return tuple(needs)


def _approval_scopes(values: Sequence[object]) -> list[str]:
    scopes: list[str] = []
    for index, value in enumerate(values):
        item = _mapping_item(value, index, "approvals")
        _require_exact_fields(item, _APPROVAL_FIELDS, f"approvals[{index}]")
        scope = _require_string(item, "scope", f"approvals[{index}]")
        if item.get("decision") != "approved":
            raise PlanBatchBlocked(
                "quality.approval_decision", "approval decision must be approved"
            )
        if scope in set(scopes):
            raise PlanBatchBlocked(
                "quality.approval_duplicate", "approval scopes must be unique"
            )
        scopes.append(scope)
    return scopes


def _blocked_result(error: PlanBatchBlocked) -> JsonObject:
    return cast(
        JsonObject,
        {
            "interface": RESULT_INTERFACE,
            "outcome": "blocked",
            "write_status": "not_written",
            "selected_finding_ids": [],
            "dispatch_path": None,
            "runway_path": None,
            "transaction_path": None,
            "transaction": None,
            "review_basis": None,
            "blockers": [{"code": error.code, "message": str(error)}],
            "next_action": error.next_action,
            "implementation_started": False,
        },
    )


def _require_exact_fields(
    raw: Mapping[str, object], expected: set[str] | frozenset[str], label: str
) -> None:
    actual = set(raw)
    if actual != set(expected):
        raise PlanBatchBlocked(
            "request.fields",
            f"{label} fields must be exactly {sorted(expected)!r}; got {sorted(actual)!r}",
        )


def _require_mapping(
    raw: Mapping[str, object], key: str, label: str
) -> Mapping[str, object]:
    value = raw.get(key)
    if not isinstance(value, Mapping):
        raise PlanBatchBlocked("request.object", f"{label}.{key} must be an object")
    return cast(Mapping[str, object], value)


def _require_sequence(
    raw: Mapping[str, object], key: str, label: str
) -> Sequence[object]:
    value = raw.get(key)
    if not isinstance(value, list):
        raise PlanBatchBlocked("request.list", f"{label}.{key} must be a list")
    return cast(Sequence[object], value)


def _mapping_item(value: object, index: int, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise PlanBatchBlocked("request.object", f"{label}[{index}] must be an object")
    return cast(Mapping[str, object], value)


def _require_string(raw: Mapping[str, object], key: str, label: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PlanBatchBlocked("request.string", f"{label}.{key} must be non-empty")
    return value


def _require_string_list(
    raw: Mapping[str, object], key: str, label: str
) -> list[str]:
    values = _require_sequence(raw, key, label)
    result: list[str] = []
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            raise PlanBatchBlocked(
                "request.string_list", f"{label}.{key}[{index}] must be non-empty"
            )
        result.append(value)
    if len(result) != len(set(result)):
        raise PlanBatchBlocked(
            "request.string_list", f"{label}.{key} values must be unique"
        )
    return result


def _require_bool(raw: Mapping[str, object], key: str, label: str) -> bool:
    value = raw.get(key)
    if not isinstance(value, bool):
        raise PlanBatchBlocked("request.bool", f"{label}.{key} must be boolean")
    return value


def _require_int(raw: Mapping[str, object], key: str, label: str) -> int:
    value = raw.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise PlanBatchBlocked(
            "request.integer", f"{label}.{key} must be a non-negative integer"
        )
    return value


def _require_hash(
    raw: Mapping[str, object], key: str, label: str, *, length: int
) -> str:
    value = _require_string(raw, key, label)
    if len(value) != length or any(character not in "0123456789abcdef" for character in value):
        raise PlanBatchBlocked(
            "request.hash", f"{label}.{key} must be a lowercase {length}-digit hex hash"
        )
    return value


def _require_path(raw: Mapping[str, object], key: str, label: str) -> Path:
    value = _require_string(raw, key, label)
    path = Path(value)
    if not path.is_absolute():
        raise PlanBatchBlocked("request.path", f"{label}.{key} must be absolute")
    return path.resolve(strict=False)


def _require_root(raw: Mapping[str, object], key: str, label: str) -> Path:
    try:
        path = _require_path(raw, key, label).resolve(strict=True)
    except OSError as error:
        raise PlanBatchBlocked("context.root", f"{label}.{key} does not resolve") from error
    if not path.is_dir():
        raise PlanBatchBlocked("context.root", f"{label}.{key} must be a directory")
    return path


def _require_within(path: Path, root: Path, label: str) -> None:
    normalized = path.resolve(strict=False)
    try:
        normalized.relative_to(root)
    except ValueError as error:
        raise PlanBatchBlocked(
            "context.write_scope", f"{label} must stay within the planning root"
        ) from error


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def _git_head(root: Path) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise PlanBatchBlocked("context.git", f"cannot read Git HEAD for {root}")
    return process.stdout.strip()


def _mapping_digest(value: Mapping[str, object]) -> str:
    return _value_digest(value)


def _value_digest(value: object) -> str:
    encoded = json.dumps(
        _thaw_json(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _diagnostic_identity(command: str, planning_state: Mapping[str, object]) -> str:
    return _value_digest({"command": command, "planning_state": planning_state})


def _file_hash(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise PlanBatchBlocked("request.file", f"cannot read {path}") from error


def _relative_to(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    except ValueError as error:
        raise PlanBatchBlocked("transaction.path", "artifact path escapes planning root") from error


def _producer_object(producer: ProducerIdentity) -> JsonObject:
    return cast(
        JsonObject,
        {
            "toolchain_generation": producer.toolchain_generation,
            "toolchain_commit": producer.toolchain_commit,
            "schema_version": producer.schema_version,
        },
    )


def _json_copy(value: Mapping[str, object]) -> JsonObject:
    return cast(JsonObject, _thaw_json(value))


def _thaw_json(value: object) -> JsonValue:
    if isinstance(value, Mapping):
        typed = cast(Mapping[object, object], value)
        if not all(isinstance(key, str) for key in typed):
            raise PlanBatchBlocked("request.json", "JSON object keys must be strings")
        return {cast(str, key): _thaw_json(child) for key, child in typed.items()}
    if isinstance(value, tuple | list):
        return [_thaw_json(child) for child in cast(Sequence[object], value)]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise PlanBatchBlocked(
        "request.json", f"unsupported JSON value {type(value).__name__}"
    )


def main() -> int:
    try:
        raw = json.load(sys.stdin)
        if not isinstance(raw, Mapping):
            raise PlanBatchBlocked("request.object", "stdin JSON must be an object")
        result = execute_plan_batch(cast(Mapping[str, object], raw))
    except (json.JSONDecodeError, PlanBatchBlocked) as error:
        blocked = (
            error
            if isinstance(error, PlanBatchBlocked)
            else PlanBatchBlocked("request.json", str(error))
        )
        result = _blocked_result(blocked)
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
