"""Validate explicit contract-first skill documents against skill-contract/v1."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

import yaml
from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError, ValidationError
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode


SCHEMA_VERSION: Final = "skill-contract/v1"
SCHEMA_RELATIVE_PATH: Final = Path("schemas/skill-contract-v1.schema.json")
_CONTRACT_HEADING: Final = re.compile(r"^## Contract[ \t]*$")
_FENCE_OPEN: Final = re.compile(
    r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)$",
)
_HUMAN_WORKFLOW_DECISIONS: Final = frozenset(
    {
        "candidate_selection",
        "closeout_interpretation",
        "dispatch_definition",
        "execution_acceptance",
        "finding_intake",
        "runway_specification",
        "scope_shaping",
        "successor_selection",
        "validation_profile_selection",
    }
)
_EVIDENCE_FORBIDDEN_STATE: Final = frozenset(
    {
        "active_runway",
        "batch_selection",
        "candidate_selection",
        "closeout",
        "closeout_interpretation",
        "closeout_state",
        "execution_acceptance",
        "execution_state",
        "finding_selection",
        "queue_state",
        "queued_runway",
        "same_batch_reconciliation",
        "selected_dispatch",
        "successor_selection",
    }
)


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys at every depth."""

    def construct_mapping(
        self,
        node: MappingNode,
        deep: bool = False,
    ) -> dict[Hashable, Any]:
        seen: set[Hashable] = set()
        for key_node, _ in node.value:
            key = cast(Any, self).construct_object(key_node, deep=deep)
            if not isinstance(key, Hashable):
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable key",
                    key_node.start_mark,
                )
            if key in seen:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


@dataclass(frozen=True, order=True)
class Diagnostic:
    """One deterministic, path-qualified validation finding."""

    path: str
    location: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.location}: {self.code}: {self.message}"


@dataclass(frozen=True)
class ProducerIdentity:
    """Caller-supplied producer identity; it is never inferred from process state."""

    toolchain_generation: str
    toolchain_commit: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class SharedMechanismPolicy:
    """Explicit durable facts allowed to have more than one structured owner."""

    authorized_durable_facts: frozenset[str]


@dataclass(frozen=True)
class ExternalMechanismPolicy:
    """Explicit mechanism targets allowed to resolve outside the catalog."""

    allowed_mechanisms: frozenset[str]


@dataclass(frozen=True)
class ParsedSkillContract:
    """A schema-valid contract and its source document."""

    path: Path
    contract: Mapping[str, object]


@dataclass(frozen=True)
class ValidationResult:
    """Parsed contracts and stable diagnostics for an explicit catalog."""

    contracts: tuple[ParsedSkillContract, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def is_valid(self) -> bool:
        return not self.diagnostics


def validate_skill_contracts(
    contract_paths: Iterable[str | Path],
    *,
    toolchain_root: str | Path,
    expected_producer_identity: ProducerIdentity | None = None,
    shared_mechanism_policy: SharedMechanismPolicy | None = None,
    external_mechanism_policy: ExternalMechanismPolicy | None = None,
    complete_catalog: bool | None = None,
    before_contract_paths: Iterable[str | Path] | None = None,
    after_contract_paths: Iterable[str | Path] | None = None,
    migration_policy: Mapping[str, object] | None = None,
) -> ValidationResult:
    """Validate explicit document paths through the canonical schema.

    Comparison inputs reserve the single public seam for the migration guards
    added by a later slice. Supplying them before that behavior exists fails
    closed instead of silently ignoring caller intent. Set ``complete_catalog``
    when a one-document input is the entire catalog rather than a structural
    document-validation subset.
    """

    root = Path(toolchain_root).resolve()
    schema_path = root / SCHEMA_RELATIVE_PATH
    diagnostics: list[Diagnostic] = []

    if any(
        value is not None
        for value in (before_contract_paths, after_contract_paths, migration_policy)
    ):
        diagnostics.append(
            Diagnostic(
                path="<comparison>",
                location="$",
                code="comparison.not_available",
                message="before/after migration comparison is not available in this slice",
            )
        )

    validator = _load_validator(schema_path, diagnostics)
    if validator is None:
        return ValidationResult(contracts=(), diagnostics=tuple(sorted(diagnostics)))

    parsed_contracts: list[ParsedSkillContract] = []
    normalized_paths = sorted({Path(path).resolve() for path in contract_paths})
    for path in normalized_paths:
        parsed = _validate_document(
            path,
            validator,
            expected_producer_identity=expected_producer_identity,
            diagnostics=diagnostics,
        )
        if parsed is not None:
            parsed_contracts.append(parsed)

    if len(parsed_contracts) == len(normalized_paths):
        _validate_catalog(
            parsed_contracts,
            toolchain_root=root,
            shared_mechanism_policy=shared_mechanism_policy,
            external_mechanism_policy=external_mechanism_policy,
            validate_relationships=(
                complete_catalog
                if complete_catalog is not None
                else len(parsed_contracts) > 1
            ),
            diagnostics=diagnostics,
        )

    return ValidationResult(
        contracts=tuple(parsed_contracts),
        diagnostics=tuple(sorted(diagnostics)),
    )


def _load_validator(
    schema_path: Path,
    diagnostics: list[Diagnostic],
) -> Draft7Validator | None:
    try:
        raw_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        diagnostics.append(
            Diagnostic(
                path=str(schema_path),
                location="$",
                code="schema.unavailable",
                message=str(error),
            )
        )
        return None

    if not isinstance(raw_schema, dict):
        diagnostics.append(
            Diagnostic(
                path=str(schema_path),
                location="$",
                code="schema.invalid",
                message="canonical schema must be a JSON object",
            )
        )
        return None

    schema = cast(dict[str, Any], raw_schema)
    try:
        Draft7Validator.check_schema(schema)
    except SchemaError as error:
        diagnostics.append(
            Diagnostic(
                path=str(schema_path),
                location=_json_location(error.absolute_path),
                code="schema.invalid",
                message=error.message,
            )
        )
        return None
    return Draft7Validator(schema)


def _validate_document(
    path: Path,
    validator: Draft7Validator,
    *,
    expected_producer_identity: ProducerIdentity | None,
    diagnostics: list[Diagnostic],
) -> ParsedSkillContract | None:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        diagnostics.append(
            Diagnostic(
                path=str(path),
                location="$",
                code="document.unavailable",
                message=str(error),
            )
        )
        return None

    blocks = _extract_contract_blocks(source)
    if len(blocks) != 1:
        diagnostics.append(
            Diagnostic(
                path=str(path),
                location="$",
                code="contract.block_count",
                message=f"expected exactly one ## Contract YAML block; found {len(blocks)}",
            )
        )
        return None

    contract = _load_contract_yaml(path, blocks[0], diagnostics)
    if contract is None:
        return None

    schema_errors = cast(
        list[ValidationError],
        sorted(cast(Any, validator).iter_errors(contract), key=_schema_error_key),
    )
    for error in schema_errors:
        diagnostics.append(
            Diagnostic(
                path=str(path),
                location=_json_location(error.absolute_path),
                code=f"schema.{error.validator}",
                message=error.message,
            )
        )
    if schema_errors:
        return None

    if expected_producer_identity is not None:
        _validate_expected_producer(
            path,
            contract,
            expected_producer_identity,
            diagnostics,
        )
    return ParsedSkillContract(path=path, contract=contract)


def _load_contract_yaml(
    path: Path,
    source: str,
    diagnostics: list[Diagnostic],
) -> Mapping[str, object] | None:
    try:
        loaded = yaml.load(source, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        problem = getattr(error, "problem", None)
        location = "$"
        if mark is not None:
            location = f"line {mark.line + 1}, column {mark.column + 1}"
        diagnostics.append(
            Diagnostic(
                path=str(path),
                location=location,
                code="contract.invalid_yaml",
                message=str(problem or "invalid YAML"),
            )
        )
        return None

    if not isinstance(loaded, dict):
        diagnostics.append(
            Diagnostic(
                path=str(path),
                location="$",
                code="contract.not_object",
                message="Contract YAML must contain one object",
            )
        )
        return None
    return cast(dict[str, object], loaded)


def _validate_expected_producer(
    path: Path,
    contract: Mapping[str, object],
    expected: ProducerIdentity,
    diagnostics: list[Diagnostic],
) -> None:
    producer = cast(Mapping[str, object], contract["producer"])
    expected_fields = {
        "toolchain_generation": expected.toolchain_generation,
        "toolchain_commit": expected.toolchain_commit,
        "schema_version": expected.schema_version,
    }
    for field, expected_value in expected_fields.items():
        actual = producer[field]
        if actual != expected_value:
            diagnostics.append(
                Diagnostic(
                    path=str(path),
                    location=f"$.producer.{field}",
                    code="producer.identity_mismatch",
                    message=f"expected {expected_value!r}; got {actual!r}",
                )
            )


@dataclass(frozen=True)
class _ContractView:
    parsed: ParsedSkillContract
    name: str
    audience: str
    decisions: tuple[str, ...]
    durable_facts: tuple[str, ...]
    writes: tuple[str, ...]
    forbids: tuple[str, ...]
    required_mechanisms: tuple[str, ...]
    required_evidence_skills: tuple[str, ...]
    delegates: tuple[Mapping[str, object], ...]
    references: tuple[Mapping[str, object], ...]


@dataclass(frozen=True)
class _GraphEdge:
    target: str
    path: Path
    location: str


def _validate_catalog(
    contracts: Sequence[ParsedSkillContract],
    *,
    toolchain_root: Path,
    shared_mechanism_policy: SharedMechanismPolicy | None,
    external_mechanism_policy: ExternalMechanismPolicy | None,
    validate_relationships: bool,
    diagnostics: list[Diagnostic],
) -> None:
    views = tuple(_contract_view(contract) for contract in contracts)
    known_targets = frozenset(view.name for view in views)

    for view in views:
        _validate_owned_forbidden_conflicts(view, diagnostics)
        _validate_audience_profile(view, diagnostics)

    if not validate_relationships:
        return

    external_mechanisms: frozenset[str] = (
        external_mechanism_policy.allowed_mechanisms
        if external_mechanism_policy is not None
        else frozenset()
    )
    dependency_edges: dict[str, tuple[_GraphEdge, ...]] = {}
    for view in views:
        dependency_edges[view.name] = _validate_dependency_targets(
            view,
            known_targets=known_targets,
            external_mechanisms=external_mechanisms,
            diagnostics=diagnostics,
        )

    _validate_duplicate_command_decisions(views, diagnostics)
    _validate_duplicate_durable_facts(
        views,
        shared_mechanism_policy=shared_mechanism_policy,
        diagnostics=diagnostics,
    )
    _validate_cycles(
        dependency_edges,
        code="dependency.cycle",
        label="dependency cycle",
        display=lambda value: value,
        diagnostics=diagnostics,
    )
    _validate_reference_graph(
        views,
        toolchain_root=toolchain_root,
        diagnostics=diagnostics,
    )


def _contract_view(parsed: ParsedSkillContract) -> _ContractView:
    contract = parsed.contract
    identity = cast(Mapping[str, object], contract["identity"])
    owns = cast(Mapping[str, object], contract["owns"])
    requires = cast(Mapping[str, object], contract["requires"])
    return _ContractView(
        parsed=parsed,
        name=cast(str, identity["name"]),
        audience=cast(str, identity["audience"]),
        decisions=tuple(cast(list[str], owns["decisions"])),
        durable_facts=tuple(cast(list[str], owns["durable_facts"])),
        writes=tuple(cast(list[str], contract["writes"])),
        forbids=tuple(cast(list[str], contract["forbids"])),
        required_mechanisms=tuple(cast(list[str], requires["mechanisms"])),
        required_evidence_skills=tuple(
            cast(list[str], requires["evidence_skills"])
        ),
        delegates=tuple(cast(list[Mapping[str, object]], contract["delegates"])),
        references=tuple(cast(list[Mapping[str, object]], contract["references"])),
    )


def _validate_owned_forbidden_conflicts(
    view: _ContractView,
    diagnostics: list[Diagnostic],
) -> None:
    forbidden = frozenset(view.forbids)
    for field, owned_values in (
        ("decisions", view.decisions),
        ("writes", view.writes),
    ):
        for index, identifier in _unique_indexed(owned_values):
            if identifier in forbidden:
                diagnostics.append(
                    Diagnostic(
                        path=str(view.parsed.path),
                        location=(
                            f"$.owns.decisions[{index}]"
                            if field == "decisions"
                            else f"$.writes[{index}]"
                        ),
                        code="ownership.owned_and_forbidden",
                        message=(
                            f"{field[:-1]} {identifier!r} is both owned and forbidden"
                        ),
                    )
                )


def _validate_audience_profile(
    view: _ContractView,
    diagnostics: list[Diagnostic],
) -> None:
    if view.audience == "support-mechanism":
        for index, decision in _unique_indexed(view.decisions):
            if decision in _HUMAN_WORKFLOW_DECISIONS:
                diagnostics.append(
                    Diagnostic(
                        path=str(view.parsed.path),
                        location=f"$.owns.decisions[{index}]",
                        code="audience.support_owns_human_decision",
                        message=(
                            "support mechanism may not own human workflow decision "
                            f"{decision!r}"
                        ),
                    )
                )
    elif view.audience == "evidence-skill":
        for location_prefix, identifiers in (
            ("$.owns.decisions", view.decisions),
            ("$.owns.durable_facts", view.durable_facts),
            ("$.writes", view.writes),
        ):
            for index, identifier in _unique_indexed(identifiers):
                if identifier in _EVIDENCE_FORBIDDEN_STATE:
                    diagnostics.append(
                        Diagnostic(
                            path=str(view.parsed.path),
                            location=f"{location_prefix}[{index}]",
                            code="audience.evidence_owns_workflow_state",
                            message=(
                                "evidence skill may not own workflow state "
                                f"{identifier!r}"
                            ),
                        )
                    )


def _validate_dependency_targets(
    view: _ContractView,
    *,
    known_targets: frozenset[str],
    external_mechanisms: frozenset[str],
    diagnostics: list[Diagnostic],
) -> tuple[_GraphEdge, ...]:
    edges: list[_GraphEdge] = []
    for index, delegation in enumerate(view.delegates):
        target = cast(str, delegation["target"])
        location = f"$.delegates[{index}].target"
        if target in known_targets:
            edges.append(
                _GraphEdge(target=target, path=view.parsed.path, location=location)
            )
        elif target not in external_mechanisms:
            diagnostics.append(
                Diagnostic(
                    path=str(view.parsed.path),
                    location=location,
                    code="catalog.unknown_delegate_target",
                    message=(
                        f"delegated target {target!r} is neither in the catalog nor "
                        "an allowed external mechanism"
                    ),
                )
            )

    for index, target in _unique_indexed(view.required_mechanisms):
        location = f"$.requires.mechanisms[{index}]"
        if target in known_targets:
            edges.append(
                _GraphEdge(target=target, path=view.parsed.path, location=location)
            )
        elif target not in external_mechanisms:
            diagnostics.append(
                Diagnostic(
                    path=str(view.parsed.path),
                    location=location,
                    code="catalog.unknown_required_mechanism",
                    message=(
                        f"required mechanism {target!r} is neither in the catalog nor "
                        "explicitly allowed externally"
                    ),
                )
            )

    for index, target in _unique_indexed(view.required_evidence_skills):
        location = f"$.requires.evidence_skills[{index}]"
        if target in known_targets:
            edges.append(
                _GraphEdge(target=target, path=view.parsed.path, location=location)
            )
        else:
            diagnostics.append(
                Diagnostic(
                    path=str(view.parsed.path),
                    location=location,
                    code="catalog.unknown_required_evidence_skill",
                    message=f"required evidence skill {target!r} is not in the catalog",
                )
            )
    return tuple(sorted(edges, key=lambda edge: (edge.target, edge.location)))


def _validate_reference_graph(
    views: Sequence[_ContractView],
    *,
    toolchain_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    contract_paths = frozenset(view.parsed.path for view in views)
    edges: dict[str, tuple[_GraphEdge, ...]] = {}
    for view in views:
        view_edges: list[_GraphEdge] = []
        for index, reference in enumerate(view.references):
            raw_path = cast(str, reference["path"])
            location = f"$.references[{index}].path"
            candidate = Path(raw_path)
            if not candidate.is_absolute():
                candidate = view.parsed.path.parent / candidate
            try:
                resolved = candidate.resolve(strict=True)
            except FileNotFoundError:
                diagnostics.append(
                    Diagnostic(
                        path=str(view.parsed.path),
                        location=location,
                        code="reference.missing",
                        message=f"referenced path {raw_path!r} does not exist",
                    )
                )
                continue
            except (OSError, RuntimeError) as error:
                diagnostics.append(
                    Diagnostic(
                        path=str(view.parsed.path),
                        location=location,
                        code="reference.unavailable",
                        message=f"cannot resolve referenced path {raw_path!r}: {error}",
                    )
                )
                continue

            if not resolved.is_relative_to(toolchain_root):
                diagnostics.append(
                    Diagnostic(
                        path=str(view.parsed.path),
                        location=location,
                        code="reference.outside_toolchain_root",
                        message=(
                            f"referenced path {raw_path!r} resolves outside the explicit "
                            f"toolchain root: {resolved}"
                        ),
                    )
                )
                continue
            if not resolved.is_file():
                diagnostics.append(
                    Diagnostic(
                        path=str(view.parsed.path),
                        location=location,
                        code="reference.not_file",
                        message=f"referenced path {raw_path!r} is not a file",
                    )
                )
                continue
            if resolved in contract_paths:
                view_edges.append(
                    _GraphEdge(
                        target=str(resolved),
                        path=view.parsed.path,
                        location=location,
                    )
                )
        edges[str(view.parsed.path)] = tuple(
            sorted(view_edges, key=lambda edge: (edge.target, edge.location))
        )

    _validate_cycles(
        edges,
        code="reference.cycle",
        label="reference cycle",
        display=lambda value: str(Path(value).relative_to(toolchain_root)),
        diagnostics=diagnostics,
    )


def _validate_cycles(
    edges: Mapping[str, Sequence[_GraphEdge]],
    *,
    code: str,
    label: str,
    display: Callable[[str], str],
    diagnostics: list[Diagnostic],
) -> None:
    state: dict[str, int] = {}
    stack: list[str] = []
    emitted: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for edge in edges.get(node, ()):
            target_state = state.get(edge.target, 0)
            if target_state == 0:
                visit(edge.target)
            elif target_state == 1:
                start = stack.index(edge.target)
                cycle = _canonical_cycle(tuple(stack[start:]))
                if cycle not in emitted:
                    emitted.add(cycle)
                    shown = (*cycle, cycle[0])
                    diagnostics.append(
                        Diagnostic(
                            path=str(edge.path),
                            location=edge.location,
                            code=code,
                            message=f"{label}: {' -> '.join(display(item) for item in shown)}",
                        )
                    )
        stack.pop()
        state[node] = 2

    for node in sorted(edges):
        if state.get(node, 0) == 0:
            visit(node)


def _canonical_cycle(cycle: tuple[str, ...]) -> tuple[str, ...]:
    rotations = tuple(cycle[index:] + cycle[:index] for index in range(len(cycle)))
    return min(rotations)


def _validate_duplicate_command_decisions(
    views: Sequence[_ContractView],
    diagnostics: list[Diagnostic],
) -> None:
    owners: dict[str, list[tuple[_ContractView, int]]] = {}
    for view in views:
        if view.audience != "human-command-owner":
            continue
        for index, decision in _unique_indexed(view.decisions):
            owners.setdefault(decision, []).append((view, index))

    for decision, decision_owners in sorted(owners.items()):
        if len(decision_owners) < 2:
            continue
        owner_names = tuple(sorted(view.name for view, _ in decision_owners))
        for view, index in decision_owners:
            other_names = tuple(name for name in owner_names if name != view.name)
            diagnostics.append(
                Diagnostic(
                    path=str(view.parsed.path),
                    location=f"$.owns.decisions[{index}]",
                    code="ownership.duplicate_command_decision",
                    message=(
                        f"command decision {decision!r} is also owned by "
                        f"{', '.join(other_names)!r}"
                    ),
                )
            )


def _validate_duplicate_durable_facts(
    views: Sequence[_ContractView],
    *,
    shared_mechanism_policy: SharedMechanismPolicy | None,
    diagnostics: list[Diagnostic],
) -> None:
    authorized: frozenset[str] = (
        shared_mechanism_policy.authorized_durable_facts
        if shared_mechanism_policy is not None
        else frozenset()
    )
    owners: dict[str, list[tuple[_ContractView, int]]] = {}
    for view in views:
        for index, fact in _unique_indexed(view.durable_facts):
            owners.setdefault(fact, []).append((view, index))

    for fact, fact_owners in sorted(owners.items()):
        if len(fact_owners) < 2 or fact in authorized:
            continue
        owner_names = tuple(sorted(view.name for view, _ in fact_owners))
        for view, index in fact_owners:
            other_names = tuple(name for name in owner_names if name != view.name)
            diagnostics.append(
                Diagnostic(
                    path=str(view.parsed.path),
                    location=f"$.owns.durable_facts[{index}]",
                    code="ownership.duplicate_durable_fact",
                    message=(
                        f"durable fact {fact!r} is also owned by "
                        f"{', '.join(other_names)!r}"
                    ),
                )
            )


def _unique_indexed(values: Sequence[str]) -> tuple[tuple[int, str], ...]:
    seen: set[str] = set()
    unique: list[tuple[int, str]] = []
    for index, value in enumerate(values):
        if value not in seen:
            seen.add(value)
            unique.append((index, value))
    return tuple(unique)


def _schema_error_key(error: ValidationError) -> tuple[str, str, str]:
    return (_json_location(error.absolute_path), str(error.validator), error.message)


def _json_location(parts: Iterable[object]) -> str:
    location = "$"
    for part in parts:
        if isinstance(part, int):
            location += f"[{part}]"
        else:
            location += f".{part}"
    return location


def _extract_contract_blocks(source: str) -> tuple[str, ...]:
    """Return canonical Contract YAML blocks outside surrounding Markdown fences."""

    lines = source.splitlines()
    blocks: list[str] = []
    enclosing_fence: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if enclosing_fence is not None:
            if _is_fence_close(line, enclosing_fence):
                enclosing_fence = None
            index += 1
            continue

        if _CONTRACT_HEADING.fullmatch(line):
            opening_index = index + 1
            while opening_index < len(lines) and not lines[opening_index].strip():
                opening_index += 1
            if opening_index < len(lines):
                opening = _FENCE_OPEN.fullmatch(lines[opening_index])
                if opening is not None and opening.group("info").strip() in {
                    "yaml",
                    "yml",
                }:
                    marker = opening.group("marker")
                    closing_index = opening_index + 1
                    while closing_index < len(lines) and not _is_fence_close(
                        lines[closing_index], marker
                    ):
                        closing_index += 1
                    if closing_index < len(lines):
                        blocks.append("\n".join(lines[opening_index + 1 : closing_index]))
                        index = closing_index + 1
                        continue

        opening = _FENCE_OPEN.fullmatch(line)
        if opening is not None:
            enclosing_fence = opening.group("marker")
        index += 1
    return tuple(blocks)


def _is_fence_close(line: str, opening_marker: str) -> bool:
    stripped = line.lstrip(" ")
    indentation = len(line) - len(stripped)
    if indentation > 3 or not stripped:
        return False
    marker_character = opening_marker[0]
    marker_length = len(stripped) - len(stripped.lstrip(marker_character))
    return (
        marker_length >= len(opening_marker)
        and not stripped[marker_length:].strip()
    )


@dataclass(frozen=True)
class _CatalogExpansion:
    paths: tuple[Path, ...]
    diagnostics: tuple[Diagnostic, ...]


def _expand_cli_paths(raw_paths: Sequence[str]) -> _CatalogExpansion:
    paths: set[Path] = set()
    diagnostics: list[Diagnostic] = []
    for raw_path in raw_paths:
        path = Path(raw_path)
        if path.is_dir():
            contract_paths = tuple(
                candidate for candidate in path.rglob("SKILL.md") if candidate.is_file()
            )
            if not contract_paths:
                diagnostics.append(
                    Diagnostic(
                        path=str(path.resolve()),
                        location="$",
                        code="catalog.empty",
                        message="directory contains no contract documents named SKILL.md",
                    )
                )
            paths.update(contract_paths)
        else:
            paths.add(path)
    return _CatalogExpansion(
        paths=tuple(sorted(paths)),
        diagnostics=tuple(sorted(diagnostics)),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser(
        "validate",
        help="validate explicit skill documents or fixture catalogs",
    )
    validate_parser.add_argument("--toolchain-root", required=True)
    validate_parser.add_argument("paths", nargs="+")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command != "validate":
        raise AssertionError(f"unhandled command: {args.command}")

    expansion = _expand_cli_paths(cast(list[str], args.paths))
    result = validate_skill_contracts(
        expansion.paths,
        toolchain_root=cast(str, args.toolchain_root),
    )
    diagnostics = tuple(sorted((*expansion.diagnostics, *result.diagnostics)))
    for diagnostic in diagnostics:
        print(diagnostic, file=sys.stderr)
    return 0 if not diagnostics else 1


if __name__ == "__main__":
    raise SystemExit(main())
