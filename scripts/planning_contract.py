"""Validate canonical planning artifact blocks against closed-world v1 schemas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, TypeAlias, cast

import yaml
from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError
from yaml.constructor import ConstructorError
from yaml.events import (
    AliasEvent,
    MappingEndEvent,
    MappingStartEvent,
    ScalarEvent,
    SequenceEndEvent,
    SequenceStartEvent,
)
from yaml.nodes import MappingNode, ScalarNode


SUPPORTED_SCHEMAS: Final = (
    "planning-current/v1",
    "planning-finding/v1",
    "planning-dispatch/v1",
    "planning-runway/v1",
    "planning-closeout/v1",
)
_SCHEMA_PATHS: Final = {
    name: Path("schemas") / f"{name.replace('/', '-')}.schema.json"
    for name in SUPPORTED_SCHEMAS
}
_OPERATIONAL_HEADING: Final = "## Operational Contract"
_H2: Final = re.compile(r"^##(?: |$)")
_FENCE_OPEN: Final = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
_YAML_FENCE: Final = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})yaml[ \t]*$")
_PROSE_ASSIGNMENT: Final = re.compile(
    r"^ {0,3}(?:[-*+] )?(?:\*\*)?"
    r"(?P<label>[A-Za-z][A-Za-z0-9_. -]*?)"
    r"(?:(?:\*\*)?:|:(?:\*\*)?)[ \t]+(?P<value>\S.*)$"
)
_LEGACY_LABELS: Final = {
    "Program slug": "program",
    "Current ledger": "ledger",
    "Selected dispatch path": "selected_dispatch",
    "Active Batch Runway spec path": "active_runway",
    "Queued batch path or ID": "queued_runway",
    "Latest closeout path": "latest_closeout",
}

JsonValue: TypeAlias = (
    str | int | float | bool | None | dict[str, "JsonValue"] | list["JsonValue"]
)
JsonObject: TypeAlias = dict[str, JsonValue]


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys at every depth."""

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
    """One deterministic path-qualified contract finding."""

    path: str
    location: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.location}: {self.code}: {self.message}"


@dataclass(frozen=True)
class ProducerIdentity:
    """Explicit expected producer identity; process state is never evidence."""

    toolchain_generation: str
    toolchain_commit: str
    schema_version: str


@dataclass(frozen=True)
class ParsedPlanningContract:
    """A schema-valid canonical planning contract and its source path."""

    path: Path
    contract: Mapping[str, JsonValue]


@dataclass(frozen=True)
class LegacyCurrentState:
    """Narrow read-only projection of the active pre-v1 CURRENT format."""

    path: Path
    program: str
    ledger: str
    selected_dispatch: str | None
    queued_runway: str | None
    active_runway: str | None
    latest_closeout: str | None


@dataclass(frozen=True)
class ReadOnlyCompatibility:
    """Caller-scoped allowlist for active old-format CURRENT documents."""

    active_current_paths: frozenset[Path]


@dataclass(frozen=True)
class ValidationResult:
    """Validated canonical contracts, compatibility reads, and diagnostics."""

    contracts: tuple[ParsedPlanningContract, ...]
    compatibility_reads: tuple[LegacyCurrentState, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def is_valid(self) -> bool:
        return not self.diagnostics


@dataclass(frozen=True)
class _ExtractedBlock:
    source: str
    fence_start: int
    fence_end: int


@dataclass(frozen=True)
class _YamlBlock:
    source: str
    fence_start: int
    fence_end: int


@dataclass(frozen=True)
class _SecondaryYamlParse:
    mapping: JsonObject | None
    error: str | None


@dataclass(frozen=True)
class _SecondaryYamlInspection:
    top_level_keys: tuple[str, ...]
    schema_value: str | None


def validate_planning_contracts(
    contract_paths: Iterable[str | Path],
    *,
    toolchain_root: str | Path,
    expected_producer_identity: ProducerIdentity | None = None,
    compatibility: ReadOnlyCompatibility | None = None,
) -> ValidationResult:
    """Validate an explicit catalog through the five canonical schema owners."""

    root = Path(toolchain_root).resolve()
    diagnostics: list[Diagnostic] = []
    validators, schemas = _load_validators(root, diagnostics)
    paths = _expand_paths(contract_paths, diagnostics)
    allowed_legacy: frozenset[Path] = (
        frozenset(path.resolve() for path in compatibility.active_current_paths)
        if compatibility is not None
        else frozenset()
    )
    contracts: list[ParsedPlanningContract] = []
    compatibility_reads: list[LegacyCurrentState] = []

    for path in paths:
        text = _read_text(path, diagnostics)
        if text is None:
            continue
        block = _extract_operational_block(
            path,
            text,
            diagnostics,
            allow_absent=path.resolve() in allowed_legacy,
        )
        if block is None:
            if path.resolve() in allowed_legacy:
                legacy = _parse_legacy_current(path, text, diagnostics)
                if legacy is not None:
                    compatibility_reads.append(legacy)
            continue
        loaded = _load_contract_yaml(path, block.source, diagnostics)
        if loaded is None:
            continue
        schema_name = loaded.get("schema")
        if not isinstance(schema_name, str):
            diagnostics.append(
                Diagnostic(str(path), "$.schema", "contract.schema", "schema must be a string")
            )
            continue
        validator = validators.get(schema_name)
        if validator is None:
            code = (
                "schema.unsupported_version"
                if schema_name.rsplit("/", 1)[0] in {item.rsplit("/", 1)[0] for item in SUPPORTED_SCHEMAS}
                else "schema.unsupported"
            )
            diagnostics.append(
                Diagnostic(str(path), "$.schema", code, f"unsupported schema {schema_name!r}")
            )
            continue
        schema = schemas[schema_name]
        schema_errors = sorted(
            validator.iter_errors(cast(Any, loaded)),  # pyright: ignore[reportUnknownMemberType]
            key=lambda error: (tuple(str(part) for part in error.absolute_path), error.validator, error.message),
        )
        for error in schema_errors:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    _json_location(error.absolute_path),
                    f"schema.{error.validator}",
                    error.message,
                )
            )
        if schema_errors:
            continue
        _validate_canonical_machine_owner(
            path,
            text,
            canonical_block=block,
            contract=loaded,
            diagnostics=diagnostics,
        )
        _validate_prose_does_not_redefine_contract(
            path,
            text,
            contract=loaded,
            diagnostics=diagnostics,
        )
        _validate_expected_producer(
            path,
            loaded,
            expected_producer_identity,
            diagnostics,
        )
        if not any(item.path == str(path) for item in diagnostics):
            ordered = _order_by_schema(loaded, schema, schema)
            contracts.append(ParsedPlanningContract(path=path, contract=ordered))

    return ValidationResult(
        contracts=tuple(contracts),
        compatibility_reads=tuple(compatibility_reads),
        diagnostics=tuple(sorted(diagnostics)),
    )


def render_planning_contract(
    contract: Mapping[str, object],
    *,
    toolchain_root: str | Path,
    expected_producer_identity: ProducerIdentity | None = None,
) -> str:
    """Render one validated v1 contract; compatibility projections are unwritable."""

    if not isinstance(contract, Mapping):
        raise TypeError("only canonical mapping contracts can be rendered")
    root = Path(toolchain_root).resolve()
    diagnostics: list[Diagnostic] = []
    validators, schemas = _load_validators(root, diagnostics)
    if diagnostics:
        raise ValueError(str(diagnostics[0]))
    schema_name = contract.get("schema")
    if not isinstance(schema_name, str) or schema_name not in validators:
        raise ValueError(f"unsupported schema {schema_name!r}")
    errors = sorted(
        validators[schema_name].iter_errors(cast(Any, contract)),  # pyright: ignore[reportUnknownMemberType]
        key=lambda error: error.json_path,
    )
    if errors:
        raise ValueError(f"{errors[0].json_path}: {errors[0].message}")
    local_diagnostics: list[Diagnostic] = []
    _validate_expected_producer(
        Path("<render>"), contract, expected_producer_identity, local_diagnostics
    )
    if local_diagnostics:
        raise ValueError(str(local_diagnostics[0]))
    ordered = _order_by_schema(contract, schemas[schema_name], schemas[schema_name])
    body = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True)
    return f"{_OPERATIONAL_HEADING}\n\n```yaml\n{body}```\n"


def _load_validators(
    root: Path,
    diagnostics: list[Diagnostic],
) -> tuple[dict[str, Draft7Validator], dict[str, Mapping[str, JsonValue]]]:
    validators: dict[str, Draft7Validator] = {}
    schemas: dict[str, Mapping[str, JsonValue]] = {}
    for name, relative_path in _SCHEMA_PATHS.items():
        path = root / relative_path
        try:
            loaded = cast(object, json.loads(path.read_text(encoding="utf-8")))
            if not isinstance(loaded, dict):
                raise ValueError("schema root must be an object")
            loaded_mapping = cast(dict[object, object], loaded)
            if not all(isinstance(key, str) for key in loaded_mapping):
                raise ValueError("schema root must be a string-keyed object")
            schema = cast(JsonObject, loaded)
            Draft7Validator.check_schema(cast(Any, schema))
        except (OSError, json.JSONDecodeError, SchemaError, ValueError) as error:
            diagnostics.append(
                Diagnostic(str(path), "$", "schema.not_available", str(error))
            )
            continue
        schemas[name] = schema
        validators[name] = Draft7Validator(cast(Any, schema))
    return validators, schemas


def _expand_paths(
    values: Iterable[str | Path], diagnostics: list[Diagnostic]
) -> tuple[Path, ...]:
    expanded: set[Path] = set()
    for value in values:
        path = Path(value)
        if path.is_dir():
            matches = tuple(path.rglob("*.md"))
            if not matches:
                diagnostics.append(
                    Diagnostic(str(path), "$", "catalog.empty", "directory contains no Markdown contracts")
                )
            expanded.update(matches)
        elif path.is_file():
            expanded.add(path)
        else:
            diagnostics.append(
                Diagnostic(str(path), "$", "path.not_found", "contract path does not exist")
            )
    return tuple(sorted(expanded, key=lambda item: item.as_posix()))


def _read_text(path: Path, diagnostics: list[Diagnostic]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        diagnostics.append(Diagnostic(str(path), "$", "document.unreadable", str(error)))
        return None


def _extract_operational_block(
    path: Path,
    text: str,
    diagnostics: list[Diagnostic],
    *,
    allow_absent: bool = False,
) -> _ExtractedBlock | None:
    lines = text.splitlines()
    headings = _top_level_h2_indices(lines)
    matches = [index for index in headings if lines[index].strip() == _OPERATIONAL_HEADING]
    if not matches and allow_absent:
        return None
    if len(matches) != 1:
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.block_count", f"expected exactly one operational block; found {len(matches)}")
        )
        return None
    start = matches[0]
    if not headings or start != headings[0]:
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.location", "operational contract must be the first level-two section")
        )
        return None
    cursor = start + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    if cursor >= len(lines) or (fence := _YAML_FENCE.match(lines[cursor])) is None:
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.fence", "operational contract must contain one immediate yaml fence")
        )
        return None
    marker = fence.group("marker")
    end = cursor + 1
    while end < len(lines) and lines[end].strip() != marker:
        end += 1
    if end >= len(lines):
        diagnostics.append(Diagnostic(str(path), "$", "contract.fence", "operational yaml fence is unclosed"))
        return None
    section_end = next((index for index in headings if index > start), len(lines))
    if any(line.strip() for line in lines[end + 1 : section_end]):
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.second_owner", "operational section may contain only the canonical yaml block")
        )
        return None
    return _ExtractedBlock(
        source="\n".join(lines[cursor + 1 : end]),
        fence_start=cursor,
        fence_end=end,
    )


def _top_level_h2_indices(lines: Sequence[str]) -> list[int]:
    headings: list[int] = []
    active_marker: str | None = None
    for index, line in enumerate(lines):
        if active_marker is not None:
            stripped = line.strip()
            if stripped.startswith(active_marker) and not stripped[len(active_marker) :].strip():
                active_marker = None
            continue
        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            active_marker = fence.group("marker")
            continue
        if _H2.match(line):
            headings.append(index)
    return headings


def _top_level_yaml_blocks(lines: Sequence[str]) -> tuple[_YamlBlock, ...]:
    blocks: list[_YamlBlock] = []
    active_marker: str | None = None
    active_info = ""
    active_start = -1
    for index, line in enumerate(lines):
        if active_marker is not None:
            if line.strip() == active_marker:
                if active_info == "yaml":
                    blocks.append(
                        _YamlBlock(
                            source="\n".join(lines[active_start + 1 : index]),
                            fence_start=active_start,
                            fence_end=index,
                        )
                    )
                active_marker = None
            continue
        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            active_marker = fence.group("marker")
            active_info = fence.group("info").strip().lower()
            active_start = index
    return tuple(blocks)


def _validate_canonical_machine_owner(
    path: Path,
    text: str,
    *,
    canonical_block: _ExtractedBlock,
    contract: Mapping[str, object],
    diagnostics: list[Diagnostic],
) -> None:
    canonical_fields = set(contract) - {"schema"}
    supported_bases = {name.rsplit("/", 1)[0] for name in SUPPORTED_SCHEMAS}
    for block in _top_level_yaml_blocks(text.splitlines()):
        if block.fence_start == canonical_block.fence_start:
            continue
        inspection = _inspect_secondary_yaml(block.source)
        raw_fields = frozenset(inspection.top_level_keys)
        raw_schema = inspection.schema_value
        recognizable_raw_schema = raw_schema is not None and (
            raw_schema in SUPPORTED_SCHEMAS
            or raw_schema.rsplit("/", 1)[0] in supported_bases
        )
        recognizable_raw_fields = bool(canonical_fields.intersection(raw_fields))
        parsed = _parse_secondary_yaml(block.source)
        if parsed.error is not None:
            if recognizable_raw_schema or recognizable_raw_fields:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"$.line[{block.fence_start + 1}]",
                        "contract.invalid_secondary_yaml",
                        "recognizable secondary operational yaml is invalid: "
                        f"{parsed.error}",
                    )
                )
            continue
        loaded = parsed.mapping
        if loaded is None:
            continue
        schema_name = loaded.get("schema")
        recognizable_schema = isinstance(schema_name, str) and (
            schema_name in SUPPORTED_SCHEMAS
            or schema_name.rsplit("/", 1)[0] in supported_bases
        )
        overlapping_fields = sorted(canonical_fields.intersection(loaded))
        if not recognizable_schema and not overlapping_fields:
            continue
        reason = (
            f"supported planning schema {schema_name!r}"
            if recognizable_schema
            else f"operational field(s) {overlapping_fields!r}"
        )
        diagnostics.append(
            Diagnostic(
                str(path),
                f"$.line[{block.fence_start + 1}]",
                "contract.second_owner",
                f"top-level yaml block outside the canonical section defines {reason}",
            )
        )


def _parse_secondary_yaml(source: str) -> _SecondaryYamlParse:
    try:
        loaded = yaml.load(source, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as error:
        problem = cast(object, getattr(error, "problem", None))
        message = problem if isinstance(problem, str) else "malformed yaml"
        return _SecondaryYamlParse(mapping=None, error=message)
    if not isinstance(loaded, dict):
        return _SecondaryYamlParse(
            mapping=None,
            error="root is not a string-keyed mapping",
        )
    loaded_mapping = cast(dict[object, object], loaded)
    if not all(isinstance(key, str) for key in loaded_mapping):
        return _SecondaryYamlParse(
            mapping=None,
            error="root is not a string-keyed mapping",
        )
    return _SecondaryYamlParse(mapping=cast(JsonObject, loaded), error=None)


def _inspect_secondary_yaml(source: str) -> _SecondaryYamlInspection:
    try:
        node = cast(
            object,
            yaml.compose(  # pyright: ignore[reportUnknownMemberType]
                source,
                Loader=yaml.SafeLoader,
            ),
        )
    except yaml.YAMLError:
        return _inspect_partial_yaml_events(source)
    if not isinstance(node, MappingNode):
        return _SecondaryYamlInspection(top_level_keys=(), schema_value=None)
    keys: list[str] = []
    schema_value: str | None = None
    for key_node, value_node in node.value:
        if not isinstance(key_node, ScalarNode):
            continue
        key = key_node.value
        keys.append(key)
        if key == "schema" and isinstance(value_node, ScalarNode):
            schema_value = value_node.value
    return _SecondaryYamlInspection(
        top_level_keys=tuple(keys),
        schema_value=schema_value,
    )


def _inspect_partial_yaml_events(source: str) -> _SecondaryYamlInspection:
    keys: list[str] = []
    schema_value: str | None = None
    collection_stack: list[str] = []
    root_expects_key = False
    current_root_key: str | None = None
    try:
        events = cast(
            Iterable[object],
            yaml.parse(  # pyright: ignore[reportUnknownMemberType]
                source,
                Loader=yaml.SafeLoader,
            ),
        )
        for event in events:
            if isinstance(event, MappingStartEvent):
                if len(collection_stack) == 1 and not root_expects_key:
                    root_expects_key = True
                collection_stack.append("mapping")
                if len(collection_stack) == 1:
                    root_expects_key = True
                continue
            if isinstance(event, SequenceStartEvent):
                if len(collection_stack) == 1 and not root_expects_key:
                    root_expects_key = True
                collection_stack.append("sequence")
                continue
            if isinstance(event, (MappingEndEvent, SequenceEndEvent)):
                if collection_stack:
                    collection_stack.pop()
                continue
            if isinstance(event, AliasEvent):
                if len(collection_stack) == 1 and not root_expects_key:
                    root_expects_key = True
                continue
            if not isinstance(event, ScalarEvent):
                continue
            if collection_stack != ["mapping"]:
                continue
            if root_expects_key:
                current_root_key = event.value
                keys.append(event.value)
                root_expects_key = False
                continue
            if current_root_key == "schema":
                schema_value = event.value
            root_expects_key = True
    except yaml.YAMLError:
        pass
    return _SecondaryYamlInspection(
        top_level_keys=tuple(keys),
        schema_value=schema_value,
    )


def _validate_prose_does_not_redefine_contract(
    path: Path,
    text: str,
    *,
    contract: Mapping[str, object],
    diagnostics: list[Diagnostic],
) -> None:
    field_labels = _contract_field_labels(contract)
    active_marker: str | None = None
    for index, line in enumerate(text.splitlines()):
        if active_marker is not None:
            if line.strip() == active_marker:
                active_marker = None
            continue
        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            active_marker = fence.group("marker")
            continue
        assignment = _PROSE_ASSIGNMENT.match(line)
        if assignment is None:
            continue
        label = _normalize_field_label(assignment.group("label"))
        if label not in field_labels:
            continue
        diagnostics.append(
            Diagnostic(
                str(path),
                f"$.line[{index + 1}]",
                "contract.prose_redefinition",
                f"prose explicitly redefines operational field {label!r}",
            )
        )


def _contract_field_labels(
    value: object,
    prefix: str = "",
) -> frozenset[str]:
    labels: set[str] = set()
    if isinstance(value, Mapping):
        typed_value = cast(Mapping[object, object], value)
        for raw_key, child in typed_value.items():
            if not isinstance(raw_key, str):
                continue
            key = _normalize_field_label(raw_key)
            labels.add(key)
            dotted = f"{prefix}.{key}" if prefix else key
            labels.add(dotted)
            labels.update(_contract_field_labels(child, dotted))
    elif isinstance(value, list):
        for child in cast(list[object], value):
            labels.update(_contract_field_labels(child, prefix))
    return frozenset(labels)


def _normalize_field_label(value: str) -> str:
    normalized = re.sub(r"[ -]+", "_", value.strip().lower())
    return normalized.strip("_")


def _load_contract_yaml(
    path: Path, source: str, diagnostics: list[Diagnostic]
) -> JsonObject | None:
    try:
        loaded = yaml.load(source, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as error:
        diagnostics.append(Diagnostic(str(path), "$", "contract.invalid_yaml", str(error)))
        return None
    if not isinstance(loaded, dict):
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.root_type", "operational contract must be a string-keyed mapping")
        )
        return None
    loaded_mapping = cast(dict[object, object], loaded)
    if not all(isinstance(key, str) for key in loaded_mapping):
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.root_type", "operational contract must be a string-keyed mapping")
        )
        return None
    return cast(JsonObject, loaded)


def _validate_expected_producer(
    path: Path,
    contract: Mapping[str, object],
    expected: ProducerIdentity | None,
    diagnostics: list[Diagnostic],
) -> None:
    if expected is None:
        return
    producer = cast(Mapping[str, object], contract["producer"])
    for field in ("toolchain_generation", "toolchain_commit", "schema_version"):
        actual = producer[field]
        wanted = getattr(expected, field)
        if actual != wanted:
            diagnostics.append(
                Diagnostic(str(path), f"$.producer.{field}", "producer.mismatch", f"expected {wanted!r}; got {actual!r}")
            )


def _parse_legacy_current(
    path: Path, text: str, diagnostics: list[Diagnostic]
) -> LegacyCurrentState | None:
    if "archive" in {part.lower() for part in path.parts}:
        diagnostics.append(
            Diagnostic(str(path), "$", "compatibility.archive_forbidden", "compatibility reads active CURRENT documents only")
        )
        return None
    lines = text.splitlines()
    try:
        start = lines.index("## Program") + 1
    except ValueError:
        diagnostics.append(
            Diagnostic(str(path), "$", "compatibility.unrecognized", "missing exact legacy Program section")
        )
        return None
    end = next((index for index in range(start, len(lines)) if _H2.match(lines[index])), len(lines))
    section_lines = lines[start:end]
    parsed_fields = _parse_legacy_program_fields(section_lines)
    values: dict[str, str | None] = {}
    for field in _LEGACY_LABELS.values():
        raw_value = parsed_fields.get(field)
        if raw_value is None:
            diagnostics.append(
                Diagnostic(str(path), f"$.{field}", "compatibility.unrecognized", f"missing exact legacy field {field!r}")
            )
            continue
        value = raw_value[1:-1] if raw_value.startswith("`") and raw_value.endswith("`") else raw_value
        values[field] = None if value in {"None", "None selected"} else value
    if len(values) != len(_LEGACY_LABELS):
        return None
    program = values["program"]
    ledger = values["ledger"]
    if program is None or ledger is None:
        diagnostics.append(
            Diagnostic(str(path), "$", "compatibility.unrecognized", "program and ledger cannot be None")
        )
        return None
    return LegacyCurrentState(
        path=path,
        program=program,
        ledger=ledger,
        selected_dispatch=values["selected_dispatch"],
        queued_runway=values["queued_runway"],
        active_runway=values["active_runway"],
        latest_closeout=values["latest_closeout"],
    )


def _parse_legacy_program_fields(lines: Sequence[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    active_field: str | None = None
    for line in lines:
        if line.startswith("- ") and ":" in line:
            label, value = line[2:].split(":", 1)
            active_field = _LEGACY_LABELS.get(label)
            if active_field is not None:
                parsed[active_field] = value.strip()
            continue
        if active_field is not None and line.startswith("  ") and line.strip():
            parsed[active_field] = f"{parsed[active_field]}{line.strip()}"
            continue
        if line.strip():
            active_field = None
    return parsed


def _json_location(parts: Iterable[object]) -> str:
    location = "$"
    for part in parts:
        location += f"[{part}]" if isinstance(part, int) else f".{part}"
    return location


def _order_by_schema(
    value: object,
    node: Mapping[str, JsonValue],
    root: Mapping[str, JsonValue],
) -> Any:
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/definitions/"):
        definitions = cast(JsonObject, root["definitions"])
        node = cast(JsonObject, definitions[ref.rsplit("/", 1)[1]])
    if isinstance(value, Mapping):
        properties = node.get("properties")
        if not isinstance(properties, dict):
            return dict(cast(Mapping[str, object], value))
        typed_properties = cast(JsonObject, properties)
        ordered: dict[str, Any] = {}
        typed_value = cast(Mapping[str, object], value)
        for key, child_schema in typed_properties.items():
            if key in typed_value and isinstance(child_schema, dict):
                ordered[key] = _order_by_schema(
                    typed_value[key], cast(JsonObject, child_schema), root
                )
        return ordered
    if isinstance(value, list):
        item_schema = node.get("items")
        if isinstance(item_schema, dict):
            return [
                _order_by_schema(item, cast(JsonObject, item_schema), root)
                for item in cast(list[object], value)
            ]
    return cast(object, value)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="validate planning contracts")
    validate_parser.add_argument("--toolchain-root", required=True, type=Path)
    validate_parser.add_argument("paths", nargs="+", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command != "validate":
        return 2
    result = validate_planning_contracts(args.paths, toolchain_root=args.toolchain_root)
    for diagnostic in result.diagnostics:
        print(diagnostic, file=sys.stderr)
    if result.is_valid:
        print(f"validated {len(result.contracts)} planning contract(s)")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
