"""Parse and validate the temporary cross-checkout execution context."""

from __future__ import annotations

import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, TypeAlias, cast


INTERFACE: Final = "cross-checkout-context/v1"
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
    "GenerationRole",
    "CrossCheckoutContextError",
    "ExecutionContext",
    "CrossCheckoutContext",
    "parse_cross_checkout_context",
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

    _validate_root_roles(
        toolchain_source_root=toolchain_source_root,
        canonical_planning_repository_root=canonical_planning_repository_root,
        implementation_target_root=implementation_target_root,
        codex_home=codex_home,
    )
    _validate_repository_revision(
        "toolchain_source_root",
        toolchain_source_root,
        "toolchain_commit",
        toolchain_commit,
    )
    _validate_repository_revision(
        "canonical_planning_repository_root",
        canonical_planning_repository_root,
        "canonical_planning_commit_before",
        canonical_planning_commit_before,
    )
    _validate_repository_revision(
        "implementation_target_root",
        implementation_target_root,
        "implementation_commit_before",
        implementation_commit_before,
    )

    return CrossCheckoutContext(
        interface=interface,
        execution_context=ExecutionContext(
            toolchain_source_root=toolchain_source_root,
            toolchain_commit=toolchain_commit,
            canonical_planning_repository_root=canonical_planning_repository_root,
            canonical_planning_commit_before=canonical_planning_commit_before,
            implementation_target_root=implementation_target_root,
            implementation_commit_before=implementation_commit_before,
            codex_home=codex_home,
            generation_role=generation_role,
            canonical_state_mutation_allowed=canonical_state_mutation_allowed,
        ),
    )


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
