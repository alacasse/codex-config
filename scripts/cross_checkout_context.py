"""Parse and validate the temporary cross-checkout execution context."""

from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, TypeAlias, cast


INTERFACE: Final = "cross-checkout-context/v1"
RECEIPT_INTERFACE: Final = "cross-checkout-receipt/v1"
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
_FULL_GIT_SHA: Final = re.compile(r"[0-9a-f]{40}")

GenerationRole: TypeAlias = Literal["stable", "candidate"]

__all__ = [
    "INTERFACE",
    "RECEIPT_INTERFACE",
    "DELETION_CONDITION",
    "GenerationRole",
    "CrossCheckoutContextError",
    "ExecutionContext",
    "CrossCheckoutContext",
    "GenerationIdentity",
    "AllowedWriteScope",
    "RepositoryRevisions",
    "CrossRepositoryReceipt",
    "parse_cross_checkout_context",
    "capture_generation_identity",
    "validate_write_scope",
    "build_cross_repository_receipt",
    "cross_repository_receipt_to_dict",
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
class CrossRepositoryReceipt:
    """Versioned evidence for one caller-declared cross-repository scope."""

    interface: str
    caller: str
    reason: str
    allowed_scope: AllowedWriteScope
    generation_identity: GenerationIdentity
    repository_revisions: RepositoryRevisions
    deletion_condition: str


def parse_cross_checkout_context(payload: Mapping[str, object]) -> CrossCheckoutContext:
    """Return a validated context or raise before any caller can act on it."""

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
    _validate_execution_context_identity(execution_context)
    return CrossCheckoutContext(interface=interface, execution_context=execution_context)


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
    non_string_fields = sorted(repr(field) for field in actual if not isinstance(field, str))
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

    actual_revision = _run_git(root, root_field, "rev-parse", "HEAD")
    if actual_revision != expected_revision:
        raise CrossCheckoutContextError(
            f"context.execution_context.{revision_field} does not match HEAD for "
            f"{root_field}: expected {actual_revision}, got {expected_revision}"
        )


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
