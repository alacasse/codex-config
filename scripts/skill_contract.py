"""Validate explicit contract-first skill documents against skill-contract/v1."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Hashable, Iterable, Mapping, Sequence
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
    before_contract_paths: Iterable[str | Path] | None = None,
    after_contract_paths: Iterable[str | Path] | None = None,
    migration_policy: Mapping[str, object] | None = None,
) -> ValidationResult:
    """Validate explicit document paths through the canonical schema.

    Comparison inputs reserve the single public seam for the migration guards
    added by a later slice. Supplying them before that behavior exists fails
    closed instead of silently ignoring caller intent.
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
