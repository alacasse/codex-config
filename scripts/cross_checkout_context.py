"""Parse and validate the temporary cross-checkout execution context."""

from __future__ import annotations

import hashlib
import re
import stat
import subprocess
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Final, Literal, TypeAlias, TypeVar, cast
from urllib.parse import urlsplit


INTERFACE: Final = "cross-checkout-context/v1"
RECEIPT_INTERFACE: Final = "cross-checkout-receipt/v1"
PRECREATION_INTERFACE: Final = "cross-checkout-precreation/v1"
TRANSITION_RECEIPT_INTERFACE: Final = "cross-checkout-transition-receipt/v1"
DELETION_CONDITION: Final = "CCFG-29 final integration"
_TOP_LEVEL_FIELDS: Final = frozenset({"interface", "execution_context"})
_EXECUTION_CONTEXT_FIELDS: Final = frozenset(
    {
        "toolchain_source_root",
        "toolchain_commit",
        "canonical_planning_repository_root",
        "canonical_planning_commit_before",
        "implementation_target_root",
        "implementation_commit_before",
        "codex_home",
        "generation_role",
        "canonical_state_mutation_allowed",
    }
)
_PRECREATION_TOP_LEVEL_FIELDS: Final = frozenset(
    {"interface", "stable_control", "candidate_intent", "creation_authority"}
)
_STABLE_CONTROL_FIELDS: Final = frozenset(
    {
        "toolchain_source_root",
        "toolchain_commit",
        "canonical_planning_repository_root",
        "canonical_planning_commit_before",
        "canonical_planning_root",
        "codex_home",
        "generation_role",
        "canonical_state_mutation_allowed",
    }
)
_CANDIDATE_INTENT_FIELDS: Final = frozenset(
    {
        "implementation_target_root",
        "expected_repository_state",
        "candidate_codex_home",
        "expected_codex_home_state",
        "base_repository",
        "base_commit",
        "implementation_branch",
        "accepted_design_snapshot",
    }
)
_CREATION_AUTHORITY_FIELDS: Final = frozenset(
    {
        "repository_creation_allowed",
        "candidate_codex_home_creation_allowed",
        "allowed_creation_roots",
    }
)
_FULL_GIT_SHA: Final = re.compile(r"[0-9a-f]{40}")
_REPOSITORY_IDENTITY: Final = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")

GenerationRole: TypeAlias = Literal["stable", "candidate"]
_LiteralString = TypeVar("_LiteralString", bound=str)

__all__ = [
    "INTERFACE",
    "RECEIPT_INTERFACE",
    "PRECREATION_INTERFACE",
    "TRANSITION_RECEIPT_INTERFACE",
    "DELETION_CONDITION",
    "GenerationRole",
    "CrossCheckoutContextError",
    "ExecutionContext",
    "CrossCheckoutContext",
    "GenerationIdentity",
    "AllowedWriteScope",
    "RepositoryRevisions",
    "CrossCheckoutRefreshPreparation",
    "CrossCheckoutLiveLeasePreflight",
    "CrossRepositoryReceipt",
    "PrecreationStableControl",
    "CandidateIntent",
    "CreationAuthority",
    "CrossCheckoutPrecreationContext",
    "AuthorizedCreationScope",
    "CreatedCandidateIdentity",
    "CrossCheckoutTransitionReceipt",
    "parse_cross_checkout_context",
    "prepare_cross_checkout_context_refresh",
    "preflight_cross_checkout_live_lease",
    "parse_cross_checkout_precreation",
    "capture_generation_identity",
    "validate_write_scope",
    "validate_precreation_creation_targets",
    "build_cross_repository_receipt",
    "build_cross_checkout_transition_receipt",
    "cross_repository_receipt_to_dict",
    "cross_checkout_precreation_to_dict",
    "cross_checkout_transition_receipt_to_dict",
]


class CrossCheckoutContextError(ValueError):
    """Raised when a cross-checkout context fails closed validation."""


@dataclass(frozen=True)
class ExecutionContext:
    """Validated root, revision, generation, and mutation facts."""

    toolchain_source_root: Path
    toolchain_commit: str
    canonical_planning_repository_root: Path
    canonical_planning_commit_before: str
    implementation_target_root: Path
    implementation_commit_before: str
    codex_home: Path
    generation_role: GenerationRole
    canonical_state_mutation_allowed: bool


@dataclass(frozen=True)
class CrossCheckoutContext:
    """Validated ``cross-checkout-context/v1`` payload."""

    interface: str
    execution_context: ExecutionContext


@dataclass(frozen=True)
class GenerationIdentity:
    """Mechanical identity of the toolchain generation using the context."""

    generation_role: GenerationRole
    toolchain_source_root: Path
    toolchain_commit: str
    codex_home: Path
    canonical_state_mutation_allowed: bool


@dataclass(frozen=True)
class AllowedWriteScope:
    """Normalized write paths proven to stay inside their declared roots."""

    canonical_planning_repository_root: Path
    canonical_planning_root: Path
    implementation_target_root: Path
    planning_paths: tuple[Path, ...]
    implementation_paths: tuple[Path, ...]


@dataclass(frozen=True)
class RepositoryRevisions:
    """Distinct revisions bound to the three repository roles."""

    toolchain_commit: str
    canonical_planning_commit_before: str
    implementation_commit_before: str


@dataclass(frozen=True)
class CrossCheckoutRefreshPreparation:
    """Mechanical planned and live facts for one refreshed strict payload."""

    planned_revisions: RepositoryRevisions
    live_revisions: RepositoryRevisions
    refreshed_payload: Mapping[str, object]
    refreshed_context: CrossCheckoutContext


@dataclass(frozen=True)
class CrossCheckoutLiveLeasePreflight:
    """Mechanical readiness result for one fresh strict execution lease."""

    status: Literal["ready", "blocked"]
    reason: str
    live_context: CrossCheckoutContext | None


@dataclass(frozen=True)
class CrossRepositoryReceipt:
    """Versioned evidence for one caller-declared cross-repository scope."""

    interface: str
    caller: str
    reason: str
    allowed_scope: AllowedWriteScope
    generation_identity: GenerationIdentity
    repository_revisions: RepositoryRevisions
    deletion_condition: str


@dataclass(frozen=True)
class PrecreationStableControl:
    """Validated identity of the stable generation authorizing creation."""

    toolchain_source_root: Path
    toolchain_commit: str
    canonical_planning_repository_root: Path
    canonical_planning_commit_before: str
    canonical_planning_root: Path
    codex_home: Path
    generation_role: Literal["stable"]
    canonical_state_mutation_allowed: Literal[True]


@dataclass(frozen=True)
class CandidateIntent:
    """Exact absent paths and lineage intended for the candidate generation."""

    implementation_target_root: Path
    expected_repository_state: Literal["absent"]
    candidate_codex_home: Path
    expected_codex_home_state: Literal["absent"]
    base_repository: str
    base_commit: str
    implementation_branch: str
    accepted_design_snapshot: str


@dataclass(frozen=True)
class CreationAuthority:
    """Narrow authority for creating the two declared candidate roots."""

    repository_creation_allowed: Literal[True]
    candidate_codex_home_creation_allowed: Literal[True]
    allowed_creation_roots: tuple[Path, Path]


@dataclass(frozen=True)
class CrossCheckoutPrecreationContext:
    """Validated ``cross-checkout-precreation/v1`` payload."""

    interface: str
    stable_control: PrecreationStableControl
    candidate_intent: CandidateIntent
    creation_authority: CreationAuthority


@dataclass(frozen=True)
class AuthorizedCreationScope:
    """Caller-requested roots proven to equal declared creation targets."""

    creation_roots: tuple[Path, ...]


@dataclass(frozen=True)
class CreatedCandidateIdentity:
    """Observed candidate identity after repository and environment creation."""

    implementation_target_root: Path
    implementation_commit: str
    implementation_branch: str
    candidate_codex_home: Path
    base_repository: str
    base_commit: str
    accepted_design_snapshot: str


@dataclass(frozen=True)
class CrossCheckoutTransitionReceipt:
    """Evidence binding pre-creation intent to created and strict identities."""

    interface: str
    precreation_context: CrossCheckoutPrecreationContext
    created_candidate_identity: CreatedCandidateIdentity
    strict_context: CrossCheckoutContext
    deletion_condition: str


def parse_cross_checkout_context(payload: Mapping[str, object]) -> CrossCheckoutContext:
    """Return a validated context or raise before any caller can act on it."""

    interface, execution_context = _parse_cross_checkout_context_fields(payload)
    _validate_execution_context_identity(execution_context)
    return CrossCheckoutContext(
        interface=interface,
        execution_context=execution_context,
    )


def prepare_cross_checkout_context_refresh(
    payload: Mapping[str, object],
) -> CrossCheckoutRefreshPreparation:
    """Prepare live revision facts without deciding whether movement is accepted."""

    _, execution_context = _parse_cross_checkout_context_fields(payload)
    _validate_root_roles(
        toolchain_source_root=execution_context.toolchain_source_root,
        canonical_planning_repository_root=(
            execution_context.canonical_planning_repository_root
        ),
        implementation_target_root=execution_context.implementation_target_root,
        codex_home=execution_context.codex_home,
    )
    live_revisions = _capture_live_repository_revisions(execution_context)
    _validate_generation_binding(execution_context)

    raw_execution_context = cast(
        Mapping[str, object], payload["execution_context"]
    )
    refreshed_execution_context = dict(raw_execution_context)
    refreshed_execution_context.update(
        {
            "toolchain_commit": live_revisions.toolchain_commit,
            "canonical_planning_commit_before": (
                live_revisions.canonical_planning_commit_before
            ),
            "implementation_commit_before": (
                live_revisions.implementation_commit_before
            ),
        }
    )
    refreshed_payload: Mapping[str, object] = MappingProxyType(
        {
            "interface": payload["interface"],
            "execution_context": MappingProxyType(refreshed_execution_context),
        }
    )
    refreshed_context = parse_cross_checkout_context(refreshed_payload)
    return CrossCheckoutRefreshPreparation(
        planned_revisions=_repository_revisions(execution_context),
        live_revisions=live_revisions,
        refreshed_payload=refreshed_payload,
        refreshed_context=refreshed_context,
    )


def preflight_cross_checkout_live_lease(
    planning_snapshot: Mapping[str, object],
    *,
    canonical_planning_root: str | Path,
    queue_transaction_paths: Iterable[str | Path],
) -> CrossCheckoutLiveLeasePreflight:
    """Return a fresh strict context only for exact queue-establishment movement."""

    try:
        _, execution_context = _parse_cross_checkout_context_fields(planning_snapshot)
        planning_root = _normalize_scope_root(
            canonical_planning_root,
            field="canonical_planning_root",
            repository_root=execution_context.canonical_planning_repository_root,
        )
        raw_declared_paths = _materialize_write_paths(
            queue_transaction_paths,
            field="queue_transaction_paths",
        )
        normalized_declared_paths = _normalize_write_paths(
            raw_declared_paths,
            field="queue_transaction_paths",
            root_field="canonical_planning_root",
            root=planning_root,
        )
        declared_paths = frozenset(normalized_declared_paths)
        if len(declared_paths) != len(normalized_declared_paths):
            raise CrossCheckoutContextError(
                "queue_transaction_paths must not contain duplicate paths"
            )

        preparation = prepare_cross_checkout_context_refresh(planning_snapshot)
        live_revisions = preparation.live_revisions
        if (
            live_revisions.implementation_commit_before
            != execution_context.implementation_commit_before
        ):
            raise CrossCheckoutContextError(
                "implementation repository HEAD moved since the planning snapshot"
            )
        observed_paths, observed_fingerprint = _capture_queue_transaction_paths(
            execution_context,
            live_revisions=live_revisions,
            planning_root=planning_root,
        )
        if observed_paths != declared_paths:
            raise CrossCheckoutContextError(
                "current canonical planning changes do not exactly match the "
                "caller-supplied queue transaction paths; "
                f"observed={sorted(map(str, observed_paths))}, "
                f"declared={sorted(map(str, declared_paths))}"
            )
        if (
            live_revisions.canonical_planning_commit_before
            != execution_context.canonical_planning_commit_before
            and not observed_paths
        ):
            raise CrossCheckoutContextError(
                "canonical planning HEAD moved without an exact queue transaction path"
            )

        if _capture_live_repository_revisions(execution_context) != live_revisions:
            raise CrossCheckoutContextError(
                "repository revisions moved during live-lease preflight"
            )
        final_observed_paths, final_fingerprint = _capture_queue_transaction_paths(
            execution_context,
            live_revisions=live_revisions,
            planning_root=planning_root,
        )
        if (
            final_observed_paths != observed_paths
            or final_fingerprint != observed_fingerprint
        ):
            raise CrossCheckoutContextError(
                "canonical planning changes moved during live-lease preflight"
            )
    except CrossCheckoutContextError as error:
        return CrossCheckoutLiveLeasePreflight(
            status="blocked",
            reason=str(error),
            live_context=None,
        )

    return CrossCheckoutLiveLeasePreflight(
        status="ready",
        reason="current repository facts exactly match the supplied queue transaction",
        live_context=preparation.refreshed_context,
    )


def _parse_cross_checkout_context_fields(
    payload: Mapping[str, object],
) -> tuple[str, ExecutionContext]:
    _require_exact_fields(payload, _TOP_LEVEL_FIELDS, "context")
    interface = _require_string(payload, "interface", "context")
    if interface != INTERFACE:
        raise CrossCheckoutContextError(
            f"context.interface must be exactly {INTERFACE!r}; got {interface!r}"
        )

    raw_execution_context = payload["execution_context"]
    if not isinstance(raw_execution_context, Mapping):
        raise CrossCheckoutContextError("context.execution_context must be an object")
    execution_payload = cast(Mapping[str, object], raw_execution_context)
    _require_exact_fields(
        execution_payload,
        _EXECUTION_CONTEXT_FIELDS,
        "context.execution_context",
    )

    toolchain_source_root = _require_absolute_directory(
        execution_payload, "toolchain_source_root"
    )
    canonical_planning_repository_root = _require_absolute_directory(
        execution_payload, "canonical_planning_repository_root"
    )
    implementation_target_root = _require_absolute_directory(
        execution_payload, "implementation_target_root"
    )
    codex_home = _require_absolute_directory(execution_payload, "codex_home")

    toolchain_commit = _require_full_git_sha(execution_payload, "toolchain_commit")
    canonical_planning_commit_before = _require_full_git_sha(
        execution_payload, "canonical_planning_commit_before"
    )
    implementation_commit_before = _require_full_git_sha(
        execution_payload, "implementation_commit_before"
    )
    generation_role = _require_generation_role(execution_payload)
    canonical_state_mutation_allowed = _require_bool(
        execution_payload, "canonical_state_mutation_allowed"
    )
    if generation_role == "candidate" and canonical_state_mutation_allowed:
        raise CrossCheckoutContextError(
            "context.execution_context.canonical_state_mutation_allowed must be "
            "false for generation_role 'candidate'"
        )

    execution_context = ExecutionContext(
        toolchain_source_root=toolchain_source_root,
        toolchain_commit=toolchain_commit,
        canonical_planning_repository_root=canonical_planning_repository_root,
        canonical_planning_commit_before=canonical_planning_commit_before,
        implementation_target_root=implementation_target_root,
        implementation_commit_before=implementation_commit_before,
        codex_home=codex_home,
        generation_role=generation_role,
        canonical_state_mutation_allowed=canonical_state_mutation_allowed,
    )
    return interface, execution_context


def parse_cross_checkout_precreation(
    payload: Mapping[str, object],
) -> CrossCheckoutPrecreationContext:
    """Return an exact, validated pre-creation context without creating paths."""

    _require_exact_fields(payload, _PRECREATION_TOP_LEVEL_FIELDS, "precreation")
    interface = _require_labeled_string(payload, "interface", "precreation")
    if interface != PRECREATION_INTERFACE:
        raise CrossCheckoutContextError(
            "precreation.interface must be exactly "
            f"{PRECREATION_INTERFACE!r}; got {interface!r}"
        )

    stable_payload = _require_mapping(payload, "stable_control", "precreation")
    _require_exact_fields(
        stable_payload,
        _STABLE_CONTROL_FIELDS,
        "precreation.stable_control",
    )
    candidate_payload = _require_mapping(payload, "candidate_intent", "precreation")
    _require_exact_fields(
        candidate_payload,
        _CANDIDATE_INTENT_FIELDS,
        "precreation.candidate_intent",
    )
    authority_payload = _require_mapping(
        payload,
        "creation_authority",
        "precreation",
    )
    _require_exact_fields(
        authority_payload,
        _CREATION_AUTHORITY_FIELDS,
        "precreation.creation_authority",
    )

    stable_control = PrecreationStableControl(
        toolchain_source_root=_require_labeled_absolute_directory(
            stable_payload,
            "toolchain_source_root",
            "precreation.stable_control",
        ),
        toolchain_commit=_require_labeled_full_git_sha(
            stable_payload,
            "toolchain_commit",
            "precreation.stable_control",
        ),
        canonical_planning_repository_root=_require_labeled_absolute_directory(
            stable_payload,
            "canonical_planning_repository_root",
            "precreation.stable_control",
        ),
        canonical_planning_commit_before=_require_labeled_full_git_sha(
            stable_payload,
            "canonical_planning_commit_before",
            "precreation.stable_control",
        ),
        canonical_planning_root=_require_labeled_absolute_directory(
            stable_payload,
            "canonical_planning_root",
            "precreation.stable_control",
        ),
        codex_home=_require_labeled_absolute_directory(
            stable_payload,
            "codex_home",
            "precreation.stable_control",
        ),
        generation_role=_require_exact_literal(
            stable_payload,
            "generation_role",
            "stable",
            "precreation.stable_control",
        ),
        canonical_state_mutation_allowed=_require_true(
            stable_payload,
            "canonical_state_mutation_allowed",
            "precreation.stable_control",
        ),
    )
    candidate_intent = CandidateIntent(
        implementation_target_root=_require_absent_absolute_path(
            candidate_payload,
            "implementation_target_root",
            "precreation.candidate_intent",
        ),
        expected_repository_state=_require_exact_literal(
            candidate_payload,
            "expected_repository_state",
            "absent",
            "precreation.candidate_intent",
        ),
        candidate_codex_home=_require_absent_absolute_path(
            candidate_payload,
            "candidate_codex_home",
            "precreation.candidate_intent",
        ),
        expected_codex_home_state=_require_exact_literal(
            candidate_payload,
            "expected_codex_home_state",
            "absent",
            "precreation.candidate_intent",
        ),
        base_repository=_require_repository_identity(
            candidate_payload,
            "base_repository",
            "precreation.candidate_intent",
        ),
        base_commit=_require_labeled_full_git_sha(
            candidate_payload,
            "base_commit",
            "precreation.candidate_intent",
        ),
        implementation_branch=_require_branch_name(
            candidate_payload,
            "implementation_branch",
            "precreation.candidate_intent",
            stable_control.toolchain_source_root,
        ),
        accepted_design_snapshot=_require_labeled_full_git_sha(
            candidate_payload,
            "accepted_design_snapshot",
            "precreation.candidate_intent",
        ),
    )
    creation_authority = _parse_creation_authority(
        authority_payload,
        candidate_intent,
    )
    context = CrossCheckoutPrecreationContext(
        interface=interface,
        stable_control=stable_control,
        candidate_intent=candidate_intent,
        creation_authority=creation_authority,
    )
    _validate_precreation_context(context, require_absent=True)
    return context


def capture_generation_identity(context: CrossCheckoutContext) -> GenerationIdentity:
    """Capture the validated mechanical identity of the controlling generation."""

    execution_context = context.execution_context
    _validate_execution_context_identity(execution_context)
    return GenerationIdentity(
        generation_role=execution_context.generation_role,
        toolchain_source_root=execution_context.toolchain_source_root,
        toolchain_commit=execution_context.toolchain_commit,
        codex_home=execution_context.codex_home,
        canonical_state_mutation_allowed=(
            execution_context.canonical_state_mutation_allowed
        ),
    )


def validate_write_scope(
    context: CrossCheckoutContext,
    *,
    canonical_planning_root: str | Path,
    planning_paths: Iterable[str | Path] = (),
    implementation_paths: Iterable[str | Path] = (),
) -> AllowedWriteScope:
    """Validate caller-declared paths without writing or invoking callbacks."""

    capture_generation_identity(context)
    return _validate_write_scope_paths(
        context,
        canonical_planning_root=canonical_planning_root,
        planning_paths=planning_paths,
        implementation_paths=implementation_paths,
    )


def validate_precreation_creation_targets(
    context: CrossCheckoutPrecreationContext,
    *,
    creation_targets: Iterable[str | Path],
) -> AuthorizedCreationScope:
    """Revalidate pre-creation facts and authorize only exact declared roots."""

    _validate_precreation_context(context, require_absent=True)
    targets = _materialize_creation_targets(creation_targets)
    if not targets:
        raise CrossCheckoutContextError(
            "precreation creation_targets must contain at least one declared root"
        )

    normalized: list[Path] = []
    allowed = context.creation_authority.allowed_creation_roots
    for index, value in enumerate(targets):
        target = _normalize_requested_creation_target(value, index=index)
        if target in normalized:
            raise CrossCheckoutContextError(
                f"precreation creation_targets[{index}] duplicates {str(target)!r}"
            )
        if target not in allowed:
            raise CrossCheckoutContextError(
                f"precreation creation_targets[{index}] is not an exact authorized "
                f"root: {str(target)!r}"
            )
        normalized.append(target)
    return AuthorizedCreationScope(creation_roots=tuple(normalized))


def build_cross_repository_receipt(
    context: CrossCheckoutContext,
    *,
    caller: str,
    reason: str,
    canonical_planning_root: str | Path,
    planning_paths: Iterable[str | Path] = (),
    implementation_paths: Iterable[str | Path] = (),
) -> CrossRepositoryReceipt:
    """Build receipt data only after generation and path validation succeeds."""

    caller = _require_receipt_text("caller", caller)
    reason = _require_receipt_text("reason", reason)
    generation_identity = capture_generation_identity(context)
    allowed_scope = _validate_write_scope_paths(
        context,
        canonical_planning_root=canonical_planning_root,
        planning_paths=planning_paths,
        implementation_paths=implementation_paths,
    )
    execution_context = context.execution_context
    return CrossRepositoryReceipt(
        interface=RECEIPT_INTERFACE,
        caller=caller,
        reason=reason,
        allowed_scope=allowed_scope,
        generation_identity=generation_identity,
        repository_revisions=RepositoryRevisions(
            toolchain_commit=execution_context.toolchain_commit,
            canonical_planning_commit_before=(
                execution_context.canonical_planning_commit_before
            ),
            implementation_commit_before=(
                execution_context.implementation_commit_before
            ),
        ),
        deletion_condition=DELETION_CONDITION,
    )


def build_cross_checkout_transition_receipt(
    precreation_context: CrossCheckoutPrecreationContext,
    strict_context: CrossCheckoutContext,
) -> CrossCheckoutTransitionReceipt:
    """Bind validated pre-creation intent to observed and strict identities."""

    _validate_precreation_context(precreation_context, require_absent=False)
    if strict_context.interface != INTERFACE:
        raise CrossCheckoutContextError(
            "transition strict_context.interface must be exactly "
            f"{INTERFACE!r}; got {strict_context.interface!r}"
        )
    capture_generation_identity(strict_context)

    stable = precreation_context.stable_control
    intent = precreation_context.candidate_intent
    execution = strict_context.execution_context
    _validate_transition_strict_binding(stable, intent, execution)

    candidate_root = intent.implementation_target_root
    actual_repository_identity = _validated_repository_identity(
        candidate_root,
        "precreation.candidate_intent.implementation_target_root",
        intent.base_repository,
    )
    actual_branch = _run_precreation_git(
        candidate_root,
        "precreation.candidate_intent.implementation_target_root",
        "branch",
        "--show-current",
    )
    if actual_branch != intent.implementation_branch:
        raise CrossCheckoutContextError(
            "created candidate branch does not match "
            "precreation.candidate_intent.implementation_branch: "
            f"expected {intent.implementation_branch!r}, got {actual_branch!r}"
        )
    _require_ancestor(
        candidate_root,
        intent.base_commit,
        execution.implementation_commit_before,
        field="precreation.candidate_intent.base_commit",
    )
    _require_ancestor(
        candidate_root,
        intent.accepted_design_snapshot,
        execution.implementation_commit_before,
        field="precreation.candidate_intent.accepted_design_snapshot",
    )
    candidate_codex_home = _validate_created_candidate_home(intent.candidate_codex_home)

    created_identity = CreatedCandidateIdentity(
        implementation_target_root=candidate_root,
        implementation_commit=execution.implementation_commit_before,
        implementation_branch=actual_branch,
        candidate_codex_home=candidate_codex_home,
        base_repository=actual_repository_identity,
        base_commit=intent.base_commit,
        accepted_design_snapshot=intent.accepted_design_snapshot,
    )
    return CrossCheckoutTransitionReceipt(
        interface=TRANSITION_RECEIPT_INTERFACE,
        precreation_context=precreation_context,
        created_candidate_identity=created_identity,
        strict_context=strict_context,
        deletion_condition=DELETION_CONDITION,
    )


def cross_repository_receipt_to_dict(
    receipt: CrossRepositoryReceipt,
) -> dict[str, object]:
    """Return the exact JSON-compatible ``cross-checkout-receipt/v1`` shape."""

    return {
        "interface": receipt.interface,
        "caller": receipt.caller,
        "reason": receipt.reason,
        "allowed_scope": {
            "canonical_planning_repository_root": str(
                receipt.allowed_scope.canonical_planning_repository_root
            ),
            "canonical_planning_root": str(
                receipt.allowed_scope.canonical_planning_root
            ),
            "implementation_target_root": str(
                receipt.allowed_scope.implementation_target_root
            ),
            "planning_paths": [
                str(path) for path in receipt.allowed_scope.planning_paths
            ],
            "implementation_paths": [
                str(path) for path in receipt.allowed_scope.implementation_paths
            ],
        },
        "generation_identity": {
            "generation_role": receipt.generation_identity.generation_role,
            "toolchain_source_root": str(
                receipt.generation_identity.toolchain_source_root
            ),
            "toolchain_commit": receipt.generation_identity.toolchain_commit,
            "codex_home": str(receipt.generation_identity.codex_home),
            "canonical_state_mutation_allowed": (
                receipt.generation_identity.canonical_state_mutation_allowed
            ),
        },
        "repository_revisions": {
            "toolchain_commit": receipt.repository_revisions.toolchain_commit,
            "canonical_planning_commit_before": (
                receipt.repository_revisions.canonical_planning_commit_before
            ),
            "implementation_commit_before": (
                receipt.repository_revisions.implementation_commit_before
            ),
        },
        "deletion_condition": receipt.deletion_condition,
    }


def cross_checkout_precreation_to_dict(
    context: CrossCheckoutPrecreationContext,
) -> dict[str, object]:
    """Return the exact JSON-compatible ``cross-checkout-precreation/v1`` shape."""

    stable = context.stable_control
    intent = context.candidate_intent
    authority = context.creation_authority
    return {
        "interface": context.interface,
        "stable_control": {
            "toolchain_source_root": str(stable.toolchain_source_root),
            "toolchain_commit": stable.toolchain_commit,
            "canonical_planning_repository_root": str(
                stable.canonical_planning_repository_root
            ),
            "canonical_planning_commit_before": (
                stable.canonical_planning_commit_before
            ),
            "canonical_planning_root": str(stable.canonical_planning_root),
            "codex_home": str(stable.codex_home),
            "generation_role": stable.generation_role,
            "canonical_state_mutation_allowed": (
                stable.canonical_state_mutation_allowed
            ),
        },
        "candidate_intent": {
            "implementation_target_root": str(intent.implementation_target_root),
            "expected_repository_state": intent.expected_repository_state,
            "candidate_codex_home": str(intent.candidate_codex_home),
            "expected_codex_home_state": intent.expected_codex_home_state,
            "base_repository": intent.base_repository,
            "base_commit": intent.base_commit,
            "implementation_branch": intent.implementation_branch,
            "accepted_design_snapshot": intent.accepted_design_snapshot,
        },
        "creation_authority": {
            "repository_creation_allowed": authority.repository_creation_allowed,
            "candidate_codex_home_creation_allowed": (
                authority.candidate_codex_home_creation_allowed
            ),
            "allowed_creation_roots": [
                str(root) for root in authority.allowed_creation_roots
            ],
        },
    }


def cross_checkout_transition_receipt_to_dict(
    receipt: CrossCheckoutTransitionReceipt,
) -> dict[str, object]:
    """Return JSON-compatible transition evidence without lifecycle claims."""

    created = receipt.created_candidate_identity
    execution = receipt.strict_context.execution_context
    return {
        "interface": receipt.interface,
        "precreation_context": cross_checkout_precreation_to_dict(
            receipt.precreation_context
        ),
        "created_candidate_identity": {
            "implementation_target_root": str(created.implementation_target_root),
            "implementation_commit": created.implementation_commit,
            "implementation_branch": created.implementation_branch,
            "candidate_codex_home": str(created.candidate_codex_home),
            "base_repository": created.base_repository,
            "base_commit": created.base_commit,
            "accepted_design_snapshot": created.accepted_design_snapshot,
        },
        "strict_context": {
            "interface": receipt.strict_context.interface,
            "execution_context": {
                "toolchain_source_root": str(execution.toolchain_source_root),
                "toolchain_commit": execution.toolchain_commit,
                "canonical_planning_repository_root": str(
                    execution.canonical_planning_repository_root
                ),
                "canonical_planning_commit_before": (
                    execution.canonical_planning_commit_before
                ),
                "implementation_target_root": str(execution.implementation_target_root),
                "implementation_commit_before": (
                    execution.implementation_commit_before
                ),
                "codex_home": str(execution.codex_home),
                "generation_role": execution.generation_role,
                "canonical_state_mutation_allowed": (
                    execution.canonical_state_mutation_allowed
                ),
            },
        },
        "deletion_condition": receipt.deletion_condition,
    }


def _require_mapping(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> Mapping[str, object]:
    value = payload[field]
    if not isinstance(value, Mapping):
        raise CrossCheckoutContextError(f"{label}.{field} must be an object")
    return cast(Mapping[str, object], value)


def _require_labeled_string(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> str:
    value = payload[field]
    if not isinstance(value, str) or not value:
        raise CrossCheckoutContextError(f"{label}.{field} must be a non-empty string")
    return value


def _require_labeled_full_git_sha(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> str:
    value = _require_labeled_string(payload, field, label)
    if _FULL_GIT_SHA.fullmatch(value) is None:
        raise CrossCheckoutContextError(
            f"{label}.{field} must be a full 40-character lowercase Git SHA"
        )
    return value


def _require_labeled_absolute_directory(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> Path:
    value = _require_labeled_string(payload, field, label)
    path = Path(value)
    if not path.is_absolute():
        raise CrossCheckoutContextError(
            f"{label}.{field} must be an absolute path; got {value!r}"
        )
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            f"{label}.{field} does not resolve to an existing path: {value!r}"
        ) from error
    if not resolved.is_dir():
        raise CrossCheckoutContextError(
            f"{label}.{field} must resolve to a directory; got {str(resolved)!r}"
        )
    return resolved


def _require_exact_literal(
    payload: Mapping[str, object],
    field: str,
    expected: _LiteralString,
    label: str,
) -> _LiteralString:
    value = _require_labeled_string(payload, field, label)
    if value != expected:
        raise CrossCheckoutContextError(
            f"{label}.{field} must be exactly {expected!r}; got {value!r}"
        )
    return expected


def _require_true(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> Literal[True]:
    value = payload[field]
    if type(value) is not bool:
        raise CrossCheckoutContextError(f"{label}.{field} must be a boolean")
    if value is not True:
        raise CrossCheckoutContextError(f"{label}.{field} must be true")
    return True


def _require_absent_absolute_path(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> Path:
    value = _require_labeled_string(payload, field, label)
    path = Path(value)
    if not path.is_absolute():
        raise CrossCheckoutContextError(
            f"{label}.{field} must be an absolute path; got {value!r}"
        )
    if path.exists() or path.is_symlink():
        raise CrossCheckoutContextError(
            f"{label}.{field} must be absent; got existing path {value!r}"
        )
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise CrossCheckoutContextError(
            f"{label}.{field} could not be resolved: {value!r}"
        ) from error
    if resolved != path:
        raise CrossCheckoutContextError(
            f"{label}.{field} must equal its resolved absolute path; declared "
            f"{value!r}, resolved {str(resolved)!r}"
        )
    return resolved


def _require_repository_identity(
    payload: Mapping[str, object],
    field: str,
    label: str,
) -> str:
    value = _require_labeled_string(payload, field, label)
    if _REPOSITORY_IDENTITY.fullmatch(value) is None:
        raise CrossCheckoutContextError(
            f"{label}.{field} must be an exact owner/repository identity; got {value!r}"
        )
    return value


def _require_branch_name(
    payload: Mapping[str, object],
    field: str,
    label: str,
    repository_root: Path,
) -> str:
    value = _require_labeled_string(payload, field, label)
    _run_precreation_git(
        repository_root,
        f"{label}.{field}",
        "check-ref-format",
        "--branch",
        value,
    )
    return value


def _parse_creation_authority(
    payload: Mapping[str, object],
    candidate_intent: CandidateIntent,
) -> CreationAuthority:
    repository_allowed = _require_true(
        payload,
        "repository_creation_allowed",
        "precreation.creation_authority",
    )
    home_allowed = _require_true(
        payload,
        "candidate_codex_home_creation_allowed",
        "precreation.creation_authority",
    )
    raw_roots_value = payload["allowed_creation_roots"]
    if not isinstance(raw_roots_value, list):
        raise CrossCheckoutContextError(
            "precreation.creation_authority.allowed_creation_roots must be a list"
        )
    raw_roots = cast(list[object], raw_roots_value)
    if len(raw_roots) != 2:
        raise CrossCheckoutContextError(
            "precreation.creation_authority.allowed_creation_roots must contain "
            "exactly two roots"
        )
    roots = tuple(
        _normalize_declared_creation_root(value, index=index)
        for index, value in enumerate(raw_roots)
    )
    expected = (
        candidate_intent.implementation_target_root,
        candidate_intent.candidate_codex_home,
    )
    if roots != expected:
        raise CrossCheckoutContextError(
            "precreation.creation_authority.allowed_creation_roots must equal, in "
            "order, candidate_intent.implementation_target_root and "
            "candidate_intent.candidate_codex_home"
        )
    return CreationAuthority(
        repository_creation_allowed=repository_allowed,
        candidate_codex_home_creation_allowed=home_allowed,
        allowed_creation_roots=(roots[0], roots[1]),
    )


def _normalize_declared_creation_root(value: object, *, index: int) -> Path:
    label = f"precreation.creation_authority.allowed_creation_roots[{index}]"
    if not isinstance(value, str) or not value:
        raise CrossCheckoutContextError(f"{label} must be a non-empty string")
    path = Path(value)
    if not path.is_absolute():
        raise CrossCheckoutContextError(
            f"{label} must be an absolute path; got {value!r}"
        )
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise CrossCheckoutContextError(
            f"{label} could not be resolved: {value!r}"
        ) from error
    if resolved != path:
        raise CrossCheckoutContextError(
            f"{label} must equal its resolved absolute path; declared {value!r}, "
            f"resolved {str(resolved)!r}"
        )
    return resolved


def _validate_precreation_context(
    context: CrossCheckoutPrecreationContext,
    *,
    require_absent: bool,
) -> None:
    if context.interface != PRECREATION_INTERFACE:
        raise CrossCheckoutContextError(
            "precreation.interface must be exactly "
            f"{PRECREATION_INTERFACE!r}; got {context.interface!r}"
        )
    stable = context.stable_control
    intent = context.candidate_intent
    authority = context.creation_authority
    if stable.generation_role != "stable":
        raise CrossCheckoutContextError(
            "precreation.stable_control.generation_role must be exactly 'stable'"
        )
    if stable.canonical_state_mutation_allowed is not True:
        raise CrossCheckoutContextError(
            "precreation.stable_control.canonical_state_mutation_allowed must be true"
        )
    if intent.expected_repository_state != "absent":
        raise CrossCheckoutContextError(
            "precreation.candidate_intent.expected_repository_state must be "
            "exactly 'absent'"
        )
    if intent.expected_codex_home_state != "absent":
        raise CrossCheckoutContextError(
            "precreation.candidate_intent.expected_codex_home_state must be "
            "exactly 'absent'"
        )
    if authority.repository_creation_allowed is not True:
        raise CrossCheckoutContextError(
            "precreation.creation_authority.repository_creation_allowed must be true"
        )
    if authority.candidate_codex_home_creation_allowed is not True:
        raise CrossCheckoutContextError(
            "precreation.creation_authority.candidate_codex_home_creation_allowed "
            "must be true"
        )

    _validate_precreation_stable_control(stable, intent)
    _validate_precreation_candidate_paths(stable, intent, require_absent=require_absent)
    expected_roots = (
        intent.implementation_target_root,
        intent.candidate_codex_home,
    )
    if authority.allowed_creation_roots != expected_roots:
        raise CrossCheckoutContextError(
            "precreation.creation_authority.allowed_creation_roots exceed or differ "
            "from the two exact candidate intent roots"
        )


def _validate_precreation_stable_control(
    stable: PrecreationStableControl,
    intent: CandidateIntent,
) -> None:
    if stable.toolchain_source_root != stable.canonical_planning_repository_root:
        raise CrossCheckoutContextError(
            "precreation stable generation requires toolchain_source_root to equal "
            "canonical_planning_repository_root"
        )
    if stable.toolchain_commit != stable.canonical_planning_commit_before:
        raise CrossCheckoutContextError(
            "precreation stable generation requires toolchain_commit to equal "
            "canonical_planning_commit_before"
        )
    _reject_precreation_overlap(
        "stable_control.toolchain_source_root",
        stable.toolchain_source_root,
        "stable_control.codex_home",
        stable.codex_home,
    )
    _revalidate_existing_directory(
        stable.codex_home,
        "precreation.stable_control.codex_home",
    )
    _validate_precreation_repository_revision(
        stable.toolchain_source_root,
        "precreation.stable_control.toolchain_source_root",
        stable.toolchain_commit,
        "toolchain_commit",
    )
    _validate_precreation_repository_revision(
        stable.canonical_planning_repository_root,
        "precreation.stable_control.canonical_planning_repository_root",
        stable.canonical_planning_commit_before,
        "canonical_planning_commit_before",
    )
    planning_root = _revalidate_existing_directory(
        stable.canonical_planning_root,
        "precreation.stable_control.canonical_planning_root",
    )
    canonical_root = stable.canonical_planning_repository_root
    if planning_root != canonical_root and canonical_root not in planning_root.parents:
        raise CrossCheckoutContextError(
            "precreation.stable_control.canonical_planning_root must stay within "
            "canonical_planning_repository_root"
        )
    if intent.base_commit != stable.canonical_planning_commit_before:
        raise CrossCheckoutContextError(
            "precreation.candidate_intent.base_commit must equal the validated "
            "canonical_planning_commit_before"
        )
    _validated_repository_identity(
        canonical_root,
        "precreation.stable_control.canonical_planning_repository_root",
        intent.base_repository,
    )
    _validate_commit_object(
        canonical_root,
        intent.accepted_design_snapshot,
        "precreation.candidate_intent.accepted_design_snapshot",
    )
    _validate_branch_name(
        canonical_root,
        intent.implementation_branch,
        "precreation.candidate_intent.implementation_branch",
    )


def _validate_precreation_candidate_paths(
    stable: PrecreationStableControl,
    intent: CandidateIntent,
    *,
    require_absent: bool,
) -> None:
    candidate_roots = (
        (
            "candidate_intent.implementation_target_root",
            intent.implementation_target_root,
        ),
        ("candidate_intent.candidate_codex_home", intent.candidate_codex_home),
    )
    protected_roots = (
        ("stable_control.toolchain_source_root", stable.toolchain_source_root),
        (
            "stable_control.canonical_planning_repository_root",
            stable.canonical_planning_repository_root,
        ),
        ("stable_control.canonical_planning_root", stable.canonical_planning_root),
        ("stable_control.codex_home", stable.codex_home),
    )
    for candidate_field, candidate_root in candidate_roots:
        try:
            resolved = candidate_root.resolve(strict=False)
        except (OSError, RuntimeError) as error:
            raise CrossCheckoutContextError(
                f"precreation.{candidate_field} could not be resolved"
            ) from error
        if resolved != candidate_root:
            raise CrossCheckoutContextError(
                f"precreation.{candidate_field} no longer resolves to its declared "
                "target"
            )
        if require_absent and (candidate_root.exists() or candidate_root.is_symlink()):
            raise CrossCheckoutContextError(
                f"precreation.{candidate_field} must remain absent"
            )
        for protected_field, protected_root in protected_roots:
            _reject_precreation_overlap(
                candidate_field,
                candidate_root,
                protected_field,
                protected_root,
            )
    _reject_precreation_overlap(
        candidate_roots[0][0],
        candidate_roots[0][1],
        candidate_roots[1][0],
        candidate_roots[1][1],
    )


def _reject_precreation_overlap(
    left_field: str,
    left: Path,
    right_field: str,
    right: Path,
) -> None:
    if left == right or left in right.parents or right in left.parents:
        raise CrossCheckoutContextError(
            "precreation roots overlap: "
            f"{left_field}={str(left)!r}, {right_field}={str(right)!r}"
        )


def _validate_precreation_repository_revision(
    root: Path,
    root_label: str,
    expected_revision: str,
    revision_field: str,
) -> None:
    reported_root = _run_precreation_git(
        root, root_label, "rev-parse", "--show-toplevel"
    )
    try:
        canonical_reported_root = Path(reported_root).resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            f"{root_label} reported an invalid Git root: {reported_root!r}"
        ) from error
    if canonical_reported_root != root:
        raise CrossCheckoutContextError(
            f"{root_label} must be the Git repository root; got {str(root)!r}, "
            f"repository root is {str(canonical_reported_root)!r}"
        )
    actual_revision = _run_precreation_git(root, root_label, "rev-parse", "HEAD")
    if actual_revision != expected_revision:
        raise CrossCheckoutContextError(
            f"precreation.stable_control.{revision_field} does not match HEAD for "
            f"{root_label}: expected {actual_revision}, got {expected_revision}"
        )


def _validated_repository_identity(
    root: Path,
    root_label: str,
    expected_identity: str,
) -> str:
    remotes = _run_precreation_git(
        root,
        root_label,
        "remote",
        "get-url",
        "--all",
        "origin",
    ).splitlines()
    if len(remotes) != 1:
        raise CrossCheckoutContextError(
            f"{root_label} origin must declare exactly one repository URL"
        )
    remote = remotes[0]
    actual_identity = _repository_identity_from_remote(remote, root_label=root_label)
    if actual_identity != expected_identity:
        raise CrossCheckoutContextError(
            f"{root_label} origin identity does not match base_repository: expected "
            f"{expected_identity!r}, got {actual_identity!r}"
        )
    return actual_identity


def _repository_identity_from_remote(remote: str, *, root_label: str) -> str:
    if remote.startswith(("/", "./", "../", "~")):
        raise CrossCheckoutContextError(
            f"{root_label} origin does not declare an unambiguous repository identity"
        )
    if "://" in remote:
        parsed = urlsplit(remote)
        if parsed.scheme == "file" or not parsed.netloc:
            raise CrossCheckoutContextError(
                f"{root_label} origin does not declare an unambiguous repository "
                "identity"
            )
        repository_path = parsed.path
    else:
        scp_match = re.fullmatch(r"[^/@:]+@[^:]+:(.+)", remote)
        if scp_match is None:
            raise CrossCheckoutContextError(
                f"{root_label} origin does not declare an unambiguous repository "
                "identity"
            )
        repository_path = scp_match.group(1)
    repository_path = repository_path.strip("/")
    if repository_path.endswith(".git"):
        repository_path = repository_path[:-4]
    if _REPOSITORY_IDENTITY.fullmatch(repository_path) is None:
        raise CrossCheckoutContextError(
            f"{root_label} origin does not resolve to an exact owner/repository "
            f"identity: {remote!r}"
        )
    return repository_path


def _validate_commit_object(root: Path, revision: str, field: str) -> None:
    _run_precreation_git(root, field, "cat-file", "-e", f"{revision}^{{commit}}")


def _validate_branch_name(root: Path, branch: str, field: str) -> None:
    _run_precreation_git(root, field, "check-ref-format", "--branch", branch)


def _materialize_creation_targets(
    targets: Iterable[str | Path],
) -> tuple[str | Path, ...]:
    if isinstance(targets, (str, Path)):
        raise CrossCheckoutContextError(
            "precreation creation_targets must be an iterable of absolute paths, "
            "not one path"
        )
    return tuple(targets)


def _normalize_requested_creation_target(value: str | Path, *, index: int) -> Path:
    if not isinstance(value, (str, Path)):
        raise CrossCheckoutContextError(
            f"precreation creation_targets[{index}] must be a string or Path"
        )
    path = Path(value)
    if not path.is_absolute():
        raise CrossCheckoutContextError(
            f"precreation creation_targets[{index}] must be an absolute path; "
            f"got {str(path)!r}"
        )
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise CrossCheckoutContextError(
            f"precreation creation_targets[{index}] could not be resolved"
        ) from error
    if path.is_symlink() or resolved != path:
        raise CrossCheckoutContextError(
            f"precreation creation_targets[{index}] must be the exact declared path, "
            "not an alias"
        )
    return resolved


def _revalidate_existing_directory(path: Path, label: str) -> Path:
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            f"{label} no longer resolves to an existing directory"
        ) from error
    if not resolved.is_dir() or resolved != path:
        raise CrossCheckoutContextError(
            f"{label} no longer resolves to its declared directory"
        )
    return resolved


def _validate_transition_strict_binding(
    stable: PrecreationStableControl,
    intent: CandidateIntent,
    execution: ExecutionContext,
) -> None:
    if execution.canonical_planning_repository_root != (
        stable.canonical_planning_repository_root
    ):
        raise CrossCheckoutContextError(
            "strict context canonical planning repository does not match "
            "pre-creation stable control"
        )
    if execution.canonical_planning_commit_before != (
        stable.canonical_planning_commit_before
    ):
        raise CrossCheckoutContextError(
            "strict context canonical planning revision does not match pre-creation "
            "stable control"
        )
    if execution.implementation_target_root != intent.implementation_target_root:
        raise CrossCheckoutContextError(
            "strict context implementation target does not match pre-creation intent"
        )
    if execution.generation_role == "stable":
        expected_root = stable.toolchain_source_root
        expected_commit = stable.toolchain_commit
        expected_home = stable.codex_home
        expected_mutation = stable.canonical_state_mutation_allowed
    else:
        expected_root = intent.implementation_target_root
        expected_commit = execution.implementation_commit_before
        expected_home = intent.candidate_codex_home
        expected_mutation = False
    if (
        execution.toolchain_source_root != expected_root
        or execution.toolchain_commit != expected_commit
        or execution.codex_home != expected_home
        or execution.canonical_state_mutation_allowed is not expected_mutation
    ):
        raise CrossCheckoutContextError(
            "strict context generation identity does not match the corresponding "
            "pre-creation stable or created candidate identity"
        )


def _require_ancestor(
    root: Path,
    ancestor: str,
    descendant: str,
    *,
    field: str,
    descendant_label: str = "created candidate HEAD",
) -> None:
    try:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise CrossCheckoutContextError(
            f"could not inspect {field} ancestry with Git: {error}"
        ) from error
    if completed.returncode == 1:
        raise CrossCheckoutContextError(
            f"{field} is not an ancestor of the {descendant_label}"
        )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Git ancestry inspection failed"
        raise CrossCheckoutContextError(f"could not validate {field}: {detail}")


def _validate_created_candidate_home(path: Path) -> Path:
    if path.is_symlink():
        raise CrossCheckoutContextError(
            "created candidate CODEX_HOME must be the exact declared directory, not "
            "a symbolic link"
        )
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            "created candidate CODEX_HOME does not exist at the declared path"
        ) from error
    if not resolved.is_dir() or resolved != path:
        raise CrossCheckoutContextError(
            "created candidate CODEX_HOME must be the exact declared directory"
        )
    return resolved


def _run_precreation_git(root: Path, label: str, *git_args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *git_args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise CrossCheckoutContextError(
            f"could not inspect {label} with Git: {error}"
        ) from error
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Git command failed"
        raise CrossCheckoutContextError(f"could not validate {label}: {detail}")
    return completed.stdout.strip()


def _validate_generation_binding(execution_context: ExecutionContext) -> None:
    if execution_context.generation_role == "stable":
        expected_root_field = "canonical_planning_repository_root"
        expected_root = execution_context.canonical_planning_repository_root
        expected_commit_field = "canonical_planning_commit_before"
        expected_commit = execution_context.canonical_planning_commit_before
    else:
        expected_root_field = "implementation_target_root"
        expected_root = execution_context.implementation_target_root
        expected_commit_field = "implementation_commit_before"
        expected_commit = execution_context.implementation_commit_before

    if execution_context.toolchain_source_root != expected_root:
        raise CrossCheckoutContextError(
            f"generation_role {execution_context.generation_role!r} requires "
            f"toolchain_source_root to equal {expected_root_field}; got "
            f"{str(execution_context.toolchain_source_root)!r} and "
            f"{str(expected_root)!r}"
        )
    if execution_context.toolchain_commit != expected_commit:
        raise CrossCheckoutContextError(
            f"generation_role {execution_context.generation_role!r} requires "
            f"toolchain_commit to equal {expected_commit_field}; got "
            f"{execution_context.toolchain_commit} and {expected_commit}"
        )
    if (
        execution_context.generation_role == "candidate"
        and execution_context.canonical_state_mutation_allowed
    ):
        raise CrossCheckoutContextError(
            "canonical_state_mutation_allowed must be false for generation_role "
            "'candidate'"
        )


def _validate_execution_context_identity(execution_context: ExecutionContext) -> None:
    _validate_root_roles(
        toolchain_source_root=execution_context.toolchain_source_root,
        canonical_planning_repository_root=(
            execution_context.canonical_planning_repository_root
        ),
        implementation_target_root=execution_context.implementation_target_root,
        codex_home=execution_context.codex_home,
    )
    _validate_repository_revision(
        "toolchain_source_root",
        execution_context.toolchain_source_root,
        "toolchain_commit",
        execution_context.toolchain_commit,
    )
    _validate_repository_revision(
        "canonical_planning_repository_root",
        execution_context.canonical_planning_repository_root,
        "canonical_planning_commit_before",
        execution_context.canonical_planning_commit_before,
    )
    _validate_repository_revision(
        "implementation_target_root",
        execution_context.implementation_target_root,
        "implementation_commit_before",
        execution_context.implementation_commit_before,
    )
    _validate_generation_binding(execution_context)


def _repository_revisions(
    execution_context: ExecutionContext,
) -> RepositoryRevisions:
    return RepositoryRevisions(
        toolchain_commit=execution_context.toolchain_commit,
        canonical_planning_commit_before=(
            execution_context.canonical_planning_commit_before
        ),
        implementation_commit_before=execution_context.implementation_commit_before,
    )


def _capture_live_repository_revisions(
    execution_context: ExecutionContext,
) -> RepositoryRevisions:
    return RepositoryRevisions(
        toolchain_commit=_capture_repository_revision(
            "toolchain_source_root",
            execution_context.toolchain_source_root,
        ),
        canonical_planning_commit_before=_capture_repository_revision(
            "canonical_planning_repository_root",
            execution_context.canonical_planning_repository_root,
        ),
        implementation_commit_before=_capture_repository_revision(
            "implementation_target_root",
            execution_context.implementation_target_root,
        ),
    )


def _capture_queue_transaction_paths(
    execution_context: ExecutionContext,
    *,
    live_revisions: RepositoryRevisions,
    planning_root: Path,
) -> tuple[frozenset[Path], str]:
    canonical_root = execution_context.canonical_planning_repository_root
    implementation_dirty = _capture_worktree_paths(
        execution_context.implementation_target_root,
        root_field="implementation_target_root",
    )
    if implementation_dirty:
        raise CrossCheckoutContextError(
            "implementation repository has uncommitted movement: "
            f"{sorted(implementation_dirty)}"
        )

    planned_commit = execution_context.canonical_planning_commit_before
    live_commit = live_revisions.canonical_planning_commit_before
    committed_paths: tuple[str, ...] = ()
    if live_commit != planned_commit:
        _require_ancestor(
            canonical_root,
            planned_commit,
            live_commit,
            field="canonical planning snapshot commit",
            descendant_label="live canonical planning HEAD",
        )
        committed_paths = _run_git_paths(
            canonical_root,
            "canonical_planning_repository_root",
            "log",
            "--format=",
            "--name-only",
            "--no-renames",
            "-z",
            f"{planned_commit}..{live_commit}",
        )
    dirty_paths = _capture_worktree_paths(
        canonical_root,
        root_field="canonical_planning_repository_root",
    )
    unmerged_paths = _run_git_paths(
        canonical_root,
        "canonical_planning_repository_root",
        "diff",
        "--name-only",
        "--diff-filter=U",
        "-z",
    )
    if unmerged_paths:
        raise CrossCheckoutContextError(
            "canonical planning repository has ambiguous unmerged paths: "
            f"{sorted(unmerged_paths)}"
        )

    observed: dict[Path, str] = {}
    for relative_path in (*committed_paths, *dirty_paths):
        path = (canonical_root / relative_path).resolve(strict=False)
        if path != planning_root and planning_root not in path.parents:
            raise CrossCheckoutContextError(
                "canonical repository movement is outside canonical_planning_root: "
                f"{relative_path!r}"
            )
        observed[path] = relative_path
    observed_paths = frozenset(observed)
    return observed_paths, _fingerprint_queue_transaction_state(
        canonical_root,
        relative_paths=tuple(observed[path] for path in sorted(observed)),
    )


def _capture_worktree_paths(root: Path, *, root_field: str) -> tuple[str, ...]:
    unstaged = _run_git_paths(
        root,
        root_field,
        "diff",
        "--name-only",
        "--no-renames",
        "-z",
    )
    staged = _run_git_paths(
        root,
        root_field,
        "diff",
        "--cached",
        "--name-only",
        "--no-renames",
        "-z",
    )
    untracked = _run_git_paths(
        root,
        root_field,
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
    )
    return tuple(sorted({*unstaged, *staged, *untracked}))


def _fingerprint_queue_transaction_state(
    root: Path,
    *,
    relative_paths: tuple[str, ...],
) -> str:
    fingerprint = hashlib.sha256()
    fingerprint.update(
        _run_git_bytes(
            root,
            "canonical_planning_repository_root",
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
        )
    )
    if relative_paths:
        fingerprint.update(
            _run_git_bytes(
                root,
                "canonical_planning_repository_root",
                "ls-files",
                "--stage",
                "-z",
                "--",
                *relative_paths,
            )
        )
    for relative_path in relative_paths:
        fingerprint.update(relative_path.encode(errors="surrogateescape"))
        fingerprint.update(b"\0")
        path = root / relative_path
        try:
            path_stat = path.lstat()
            fingerprint.update(path_stat.st_mode.to_bytes(8, "big"))
            if path.is_symlink():
                fingerprint.update(
                    str(path.readlink()).encode(errors="surrogateescape")
                )
            elif stat.S_ISREG(path_stat.st_mode):
                with path.open("rb") as file:
                    for chunk in iter(lambda: file.read(65536), b""):
                        fingerprint.update(chunk)
        except FileNotFoundError:
            fingerprint.update(b"missing")
        except OSError as error:
            raise CrossCheckoutContextError(
                f"could not fingerprint canonical planning path {relative_path!r}: "
                f"{error}"
            ) from error
        fingerprint.update(b"\0")
    return fingerprint.hexdigest()


def _run_git_paths(root: Path, root_field: str, *git_args: str) -> tuple[str, ...]:
    stdout = _run_git_bytes(root, root_field, *git_args)
    return tuple(
        path.decode(errors="surrogateescape")
        for path in stdout.split(b"\0")
        if path
    )


def _run_git_bytes(root: Path, root_field: str, *git_args: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", *git_args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise CrossCheckoutContextError(
            f"could not inspect context.execution_context.{root_field} with Git: "
            f"{error}"
        ) from error
    if completed.returncode != 0:
        detail = completed.stderr.decode(errors="replace").strip()
        raise CrossCheckoutContextError(
            f"context.execution_context.{root_field} is not a readable Git "
            f"repository root: {detail or 'Git command failed'}"
        )
    return completed.stdout
def _validate_write_scope_paths(
    context: CrossCheckoutContext,
    *,
    canonical_planning_root: str | Path,
    planning_paths: Iterable[str | Path],
    implementation_paths: Iterable[str | Path],
) -> AllowedWriteScope:
    execution_context = context.execution_context
    declared_planning_paths = _materialize_write_paths(
        planning_paths,
        field="planning_paths",
    )
    if (
        declared_planning_paths
        and not execution_context.canonical_state_mutation_allowed
    ):
        raise CrossCheckoutContextError(
            "planning_paths require canonical_state_mutation_allowed=true; "
            f"generation_role {execution_context.generation_role!r} declared false"
        )
    planning_root = _normalize_scope_root(
        canonical_planning_root,
        field="canonical_planning_root",
        repository_root=execution_context.canonical_planning_repository_root,
    )
    return AllowedWriteScope(
        canonical_planning_repository_root=(
            execution_context.canonical_planning_repository_root
        ),
        canonical_planning_root=planning_root,
        implementation_target_root=execution_context.implementation_target_root,
        planning_paths=_normalize_write_paths(
            declared_planning_paths,
            field="planning_paths",
            root_field="canonical_planning_root",
            root=planning_root,
        ),
        implementation_paths=_normalize_write_paths(
            implementation_paths,
            field="implementation_paths",
            root_field="implementation_target_root",
            root=execution_context.implementation_target_root,
        ),
    )


def _materialize_write_paths(
    paths: Iterable[str | Path],
    *,
    field: str,
) -> tuple[str | Path, ...]:
    if isinstance(paths, (str, Path)):
        raise CrossCheckoutContextError(
            f"{field} must be an iterable of absolute paths, not one path"
        )
    return tuple(paths)


def _normalize_scope_root(
    value: str | Path,
    *,
    field: str,
    repository_root: Path,
) -> Path:
    if not isinstance(value, (str, Path)):
        raise CrossCheckoutContextError(f"{field} must be a string or Path")
    path = Path(value)
    if not path.is_absolute():
        raise CrossCheckoutContextError(
            f"{field} must be an absolute path; got {str(path)!r}"
        )
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            f"{field} does not resolve to an existing path: {str(path)!r}"
        ) from error
    if not resolved.is_dir():
        raise CrossCheckoutContextError(
            f"{field} must resolve to a directory; got {str(resolved)!r}"
        )
    if resolved != repository_root and repository_root not in resolved.parents:
        raise CrossCheckoutContextError(
            f"{field} must stay within canonical_planning_repository_root="
            f"{str(repository_root)!r}; got {str(resolved)!r}"
        )
    return resolved


def _normalize_write_paths(
    paths: Iterable[str | Path],
    *,
    field: str,
    root_field: str,
    root: Path,
) -> tuple[Path, ...]:
    if isinstance(paths, (str, Path)):
        raise CrossCheckoutContextError(
            f"{field} must be an iterable of absolute paths, not one path"
        )

    normalized: list[Path] = []
    for index, value in enumerate(paths):
        if not isinstance(value, (str, Path)):
            raise CrossCheckoutContextError(
                f"{field}[{index}] must be a string or Path"
            )
        path = Path(value)
        if not path.is_absolute():
            raise CrossCheckoutContextError(
                f"{field}[{index}] must be an absolute path; got {str(path)!r}"
            )
        try:
            resolved = path.resolve(strict=False)
        except (OSError, RuntimeError) as error:
            raise CrossCheckoutContextError(
                f"{field}[{index}] could not be resolved: {str(path)!r}"
            ) from error
        if resolved != root and root not in resolved.parents:
            raise CrossCheckoutContextError(
                f"{field}[{index}] must stay within {root_field}={str(root)!r}; "
                f"got {str(resolved)!r}"
            )
        normalized.append(resolved)
    return tuple(normalized)


def _require_receipt_text(field: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CrossCheckoutContextError(
            f"cross-repository receipt {field} must be a non-empty string"
        )
    return value


def _require_exact_fields(
    payload: Mapping[str, object], expected: frozenset[str], label: str
) -> None:
    actual = set(payload)
    non_string_fields = sorted(
        repr(field) for field in actual if not isinstance(field, str)
    )
    if non_string_fields:
        raise CrossCheckoutContextError(
            f"{label} contains non-string field names: {', '.join(non_string_fields)}"
        )
    missing = sorted(expected - actual)
    if missing:
        raise CrossCheckoutContextError(
            f"{label} is missing required fields: {', '.join(missing)}"
        )
    unsupported = sorted(actual - expected)
    if unsupported:
        raise CrossCheckoutContextError(
            f"{label} contains unsupported fields: {', '.join(unsupported)}"
        )


def _require_string(payload: Mapping[str, object], field: str, label: str) -> str:
    value = payload[field]
    if not isinstance(value, str) or not value:
        raise CrossCheckoutContextError(f"{label}.{field} must be a non-empty string")
    return value


def _require_absolute_directory(payload: Mapping[str, object], field: str) -> Path:
    value = _require_string(payload, field, "context.execution_context")
    path = Path(value)
    if not path.is_absolute():
        raise CrossCheckoutContextError(
            f"context.execution_context.{field} must be an absolute path; got {value!r}"
        )
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            f"context.execution_context.{field} does not resolve to an existing path: "
            f"{value!r}"
        ) from error
    if not resolved.is_dir():
        raise CrossCheckoutContextError(
            f"context.execution_context.{field} must resolve to a directory; got "
            f"{str(resolved)!r}"
        )
    return resolved


def _require_full_git_sha(payload: Mapping[str, object], field: str) -> str:
    value = _require_string(payload, field, "context.execution_context")
    if _FULL_GIT_SHA.fullmatch(value) is None:
        raise CrossCheckoutContextError(
            f"context.execution_context.{field} must be a full 40-character "
            "lowercase Git SHA"
        )
    return value


def _require_generation_role(payload: Mapping[str, object]) -> GenerationRole:
    value = _require_string(payload, "generation_role", "context.execution_context")
    if value not in ("stable", "candidate"):
        raise CrossCheckoutContextError(
            "context.execution_context.generation_role must be 'stable' or "
            f"'candidate'; got {value!r}"
        )
    return cast(GenerationRole, value)


def _require_bool(payload: Mapping[str, object], field: str) -> bool:
    value = payload[field]
    if type(value) is not bool:
        raise CrossCheckoutContextError(
            f"context.execution_context.{field} must be a boolean"
        )
    return cast(bool, value)


def _validate_root_roles(
    *,
    toolchain_source_root: Path,
    canonical_planning_repository_root: Path,
    implementation_target_root: Path,
    codex_home: Path,
) -> None:
    repository_roots = {
        "toolchain_source_root": toolchain_source_root,
        "canonical_planning_repository_root": canonical_planning_repository_root,
        "implementation_target_root": implementation_target_root,
    }

    _reject_overlap(
        "canonical_planning_repository_root",
        canonical_planning_repository_root,
        "implementation_target_root",
        implementation_target_root,
        allow_equal=False,
    )
    for field, root in repository_roots.items():
        _reject_overlap(field, root, "codex_home", codex_home, allow_equal=False)

    for field, root in repository_roots.items():
        if field == "toolchain_source_root":
            continue
        _reject_overlap(
            "toolchain_source_root",
            toolchain_source_root,
            field,
            root,
            allow_equal=True,
        )


def _reject_overlap(
    left_field: str,
    left: Path,
    right_field: str,
    right: Path,
    *,
    allow_equal: bool,
) -> None:
    if allow_equal and left == right:
        return
    if left == right or left in right.parents or right in left.parents:
        raise CrossCheckoutContextError(
            "context.execution_context root roles overlap: "
            f"{left_field}={str(left)!r}, {right_field}={str(right)!r}"
        )


def _validate_repository_revision(
    root_field: str,
    root: Path,
    revision_field: str,
    expected_revision: str,
) -> None:
    actual_revision = _capture_repository_revision(root_field, root)
    if actual_revision != expected_revision:
        raise CrossCheckoutContextError(
            f"context.execution_context.{revision_field} does not match HEAD for "
            f"{root_field}: expected {actual_revision}, got {expected_revision}"
        )


def _capture_repository_revision(root_field: str, root: Path) -> str:
    reported_root = _run_git(root, root_field, "rev-parse", "--show-toplevel")
    try:
        canonical_reported_root = Path(reported_root).resolve(strict=True)
    except OSError as error:
        raise CrossCheckoutContextError(
            f"context.execution_context.{root_field} reported an invalid Git root: "
            f"{reported_root!r}"
        ) from error
    if canonical_reported_root != root:
        raise CrossCheckoutContextError(
            f"context.execution_context.{root_field} must be the Git repository root; "
            f"got {str(root)!r}, repository root is {str(canonical_reported_root)!r}"
        )

    return _run_git(root, root_field, "rev-parse", "HEAD")


def _run_git(root: Path, root_field: str, *git_args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *git_args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise CrossCheckoutContextError(
            f"could not inspect context.execution_context.{root_field} with Git: {error}"
        ) from error
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Git command failed"
        raise CrossCheckoutContextError(
            f"context.execution_context.{root_field} is not a readable Git repository "
            f"root: {detail}"
        )
    return completed.stdout.strip()
