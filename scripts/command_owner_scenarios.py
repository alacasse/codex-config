"""Validate and report topology-independent command-owner scenario catalogs."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import sys
from collections import Counter
from collections.abc import Callable, Hashable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType, ModuleType
from typing import Any, Final, cast

import yaml
from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode


SCHEMA_VERSION: Final = "command-owner-scenario/v1"
SCHEMA_RELATIVE_PATH: Final = Path(
    "schemas/command-owner-scenario-v1.schema.json"
)
CATALOG_FILENAME: Final = "catalog.yaml"
_OBSERVATION_FIELDS: Final = frozenset(
    {
        "transition",
        "writes",
        "forbidden_writes",
        "stop_reason",
        "generation_and_roots",
        "validation",
    }
)
_RUNTIME_STATUSES: Final = (
    "declared",
    "bound",
    "green",
    "blocked",
    "unavailable",
)
_VOCABULARY_TOKEN: Final = re.compile(r"[a-z0-9]+")


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
    """One deterministic, path-qualified catalog diagnostic."""

    path: str
    location: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.location}: {self.code}: {self.message}"


@dataclass(frozen=True)
class Catalog:
    """One schema-valid scenario catalog and its fixture root."""

    path: Path
    root: Path
    document: Mapping[str, object]


@dataclass(frozen=True)
class CatalogValidation:
    """Catalog parsing result with stable diagnostics."""

    catalog: Catalog | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def is_valid(self) -> bool:
        return self.catalog is not None and not self.diagnostics


@dataclass(frozen=True)
class ObservationMismatch:
    """One exact expected-versus-observed field mismatch."""

    field: str
    expected: object
    actual: object


@dataclass(frozen=True)
class ScenarioEvaluation:
    """Runtime binding state for one scenario."""

    scenario_id: str
    family: str
    contracts: tuple[str, ...]
    status: str
    adapter: str | None
    reason: str | None
    mismatches: tuple[ObservationMismatch, ...]


Adapter = Callable[[Mapping[str, object], Path], Mapping[str, object] | None]


def validate_catalog(path: str | Path) -> CatalogValidation:
    """Load and validate one catalog without invoking fixture adapters."""

    catalog_path = _catalog_path(path)
    diagnostics: list[Diagnostic] = []
    document = _load_yaml_mapping(catalog_path, diagnostics)
    if document is None:
        return CatalogValidation(None, tuple(sorted(diagnostics)))

    validator = _load_schema_validator(catalog_path, diagnostics)
    if validator is None:
        return CatalogValidation(None, tuple(sorted(diagnostics)))

    schema_errors = list(cast(Any, validator).iter_errors(document))
    for error in sorted(schema_errors, key=_schema_error_key):
        diagnostics.append(
            Diagnostic(
                path=str(catalog_path),
                location=_json_location(error.absolute_path),
                code=f"schema.{error.validator}",
                message=error.message,
            )
        )

    if not diagnostics:
        _validate_catalog_semantics(catalog_path, document, diagnostics)

    if diagnostics:
        return CatalogValidation(None, tuple(sorted(diagnostics)))
    return CatalogValidation(
        Catalog(
            path=catalog_path,
            root=catalog_path.parent,
            document=MappingProxyType(document),
        ),
        (),
    )


def compare_observation(
    scenario: Mapping[str, object],
    observation: Mapping[str, object],
) -> tuple[ObservationMismatch, ...]:
    """Compare one observation exactly without executing or mutating anything."""

    actual = _validated_observation(observation)
    expected: Mapping[str, object] = {
        "transition": scenario["expected_transition"],
        "writes": scenario["expected_writes"],
        "forbidden_writes": scenario["forbidden_writes"],
        "stop_reason": scenario["expected_stop_reason"],
        "generation_and_roots": scenario["generation_and_roots"],
        "validation": scenario["validation"],
    }
    mismatches = [
        ObservationMismatch(field=field, expected=expected[field], actual=actual[field])
        for field in (
            "transition",
            "writes",
            "forbidden_writes",
            "stop_reason",
            "generation_and_roots",
            "validation",
        )
        if expected[field] != actual[field]
    ]
    return tuple(mismatches)


def evaluate_catalog(catalog: Catalog) -> tuple[ScenarioEvaluation, ...]:
    """Evaluate declared bindings without ever executing semantic command labels."""

    scenarios = cast(list[Mapping[str, object]], catalog.document["scenarios"])
    return tuple(
        _evaluate_scenario(catalog, scenario)
        for scenario in sorted(scenarios, key=lambda item: cast(str, item["id"]))
    )


def build_report(catalog: Catalog) -> Mapping[str, object]:
    """Build deterministic coverage and runtime-status evidence."""

    evaluations = evaluate_catalog(catalog)
    required_contracts = tuple(
        sorted(cast(list[str], catalog.document["required_contracts"]))
    )
    required_families = tuple(
        sorted(cast(list[str], catalog.document["required_families"]))
    )
    declared_contracts = frozenset(
        contract for evaluation in evaluations for contract in evaluation.contracts
    )
    green_contracts = frozenset(
        contract
        for evaluation in evaluations
        if evaluation.status == "green"
        for contract in evaluation.contracts
    )
    status_counts = Counter(evaluation.status for evaluation in evaluations)
    family_reports = [
        _family_report(family, evaluations) for family in required_families
    ]
    scenario_reports = [_scenario_report(evaluation) for evaluation in evaluations]
    return {
        "schema": SCHEMA_VERSION,
        "provenance": dict(cast(Mapping[str, object], catalog.document["provenance"])),
        "catalog_valid": True,
        "status_counts": {
            status: status_counts.get(status, 0) for status in _RUNTIME_STATUSES
        },
        "contracts": {
            "required": list(required_contracts),
            "declared": sorted(declared_contracts),
            "green": sorted(green_contracts),
            "undeclared": sorted(set(required_contracts) - declared_contracts),
            "not_green": sorted(set(required_contracts) - green_contracts),
        },
        "families": family_reports,
        "scenarios": scenario_reports,
        "acceptance": {
            "all_required_contracts_declared": (
                set(required_contracts) == declared_contracts
            ),
            "all_required_contracts_green": (
                set(required_contracts) == green_contracts
            ),
            "all_required_families_green": all(
                report["status"] == "green" for report in family_reports
            ),
            "only_bound_green_observations_count": True,
        },
    }


def _catalog_path(path: str | Path) -> Path:
    candidate = Path(path).resolve()
    return candidate / CATALOG_FILENAME if candidate.is_dir() else candidate


def _load_yaml_mapping(
    path: Path,
    diagnostics: list[Diagnostic],
) -> dict[str, object] | None:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        diagnostics.append(
            Diagnostic(str(path), "$", "catalog.read", str(error))
        )
        return None
    try:
        loaded = cast(object, yaml.load(source, Loader=_UniqueKeyLoader))
    except yaml.YAMLError as error:
        diagnostics.append(
            Diagnostic(str(path), "$", "catalog.invalid_yaml", str(error))
        )
        return None
    if not isinstance(loaded, dict):
        diagnostics.append(
            Diagnostic(
                str(path),
                "$",
                "catalog.mapping_required",
                "catalog must be a string-keyed mapping",
            )
        )
        return None
    loaded_mapping = cast(dict[object, object], loaded)
    if not all(isinstance(key, str) for key in loaded_mapping):
        diagnostics.append(
            Diagnostic(
                str(path),
                "$",
                "catalog.mapping_required",
                "catalog must be a string-keyed mapping",
            )
        )
        return None
    return cast(dict[str, object], loaded_mapping)


def _load_schema_validator(
    catalog_path: Path,
    diagnostics: list[Diagnostic],
) -> Draft7Validator | None:
    schema_path = Path(__file__).resolve().parents[1] / SCHEMA_RELATIVE_PATH
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft7Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, SchemaError) as error:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                "$",
                "schema.unavailable",
                f"{schema_path}: {error}",
            )
        )
        return None
    return Draft7Validator(schema)


def _schema_error_key(error: Any) -> tuple[str, str]:
    return (_json_location(error.absolute_path), error.message)


def _json_location(parts: Sequence[object]) -> str:
    location = "$"
    for part in parts:
        location += f"[{part}]" if isinstance(part, int) else f".{part}"
    return location


def _validate_catalog_semantics(
    path: Path,
    document: Mapping[str, object],
    diagnostics: list[Diagnostic],
) -> None:
    required_contracts = frozenset(cast(list[str], document["required_contracts"]))
    required_families = frozenset(cast(list[str], document["required_families"]))
    forbidden_terms = tuple(cast(list[str], document["forbidden_target_terms"]))
    scenarios = cast(list[Mapping[str, object]], document["scenarios"])
    seen_ids: dict[str, int] = {}
    covered_families: set[str] = set()

    for index, scenario in enumerate(scenarios):
        location = f"$.scenarios[{index}]"
        scenario_id = cast(str, scenario["id"])
        if scenario_id in seen_ids:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    f"{location}.id",
                    "catalog.duplicate_scenario_id",
                    f"scenario id {scenario_id!r} also appears at index {seen_ids[scenario_id]}",
                )
            )
        else:
            seen_ids[scenario_id] = index

        family = cast(str, scenario["family"])
        covered_families.add(family)
        if family not in required_families:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    f"{location}.family",
                    "catalog.unknown_family",
                    f"scenario family {family!r} is not declared",
                )
            )

        for contract_index, contract in enumerate(
            cast(list[str], scenario["contracts"])
        ):
            if contract not in required_contracts:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{location}.contracts[{contract_index}]",
                        "catalog.unknown_contract",
                        f"contract {contract!r} is not in required_contracts",
                    )
                )

        for field in ("initial_artifacts", "expected_writes", "forbidden_writes"):
            for path_index, fixture_path in enumerate(cast(list[str], scenario[field])):
                if not _is_safe_relative_path(fixture_path):
                    diagnostics.append(
                        Diagnostic(
                            str(path),
                            f"{location}.{field}[{path_index}]",
                            "catalog.unsafe_path",
                            f"path {fixture_path!r} must be a safe fixture-relative path",
                        )
                    )
        roots = cast(
            list[Mapping[str, object]],
            cast(Mapping[str, object], scenario["generation_and_roots"])["roots"],
        )
        seen_roles: set[str] = set()
        for root_index, root in enumerate(roots):
            role = cast(str, root["role"])
            if role in seen_roles:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{location}.generation_and_roots.roots[{root_index}].role",
                        "catalog.duplicate_root_role",
                        f"root role {role!r} is duplicated",
                    )
                )
            seen_roles.add(role)
            root_path = cast(str, root["path"])
            if not _is_safe_relative_path(root_path):
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{location}.generation_and_roots.roots[{root_index}].path",
                        "catalog.unsafe_path",
                        f"path {root_path!r} must be a safe fixture-relative path",
                    )
                )

        binding = cast(Mapping[str, object], scenario["binding"])
        adapter = binding["adapter"]
        if isinstance(adapter, str):
            _validate_adapter_reference(path, location, adapter, diagnostics)

        if scenario["evidence_kind"] != "source_characterization":
            for term in forbidden_terms:
                if _mapping_contains_term(scenario, term):
                    diagnostics.append(
                        Diagnostic(
                            str(path),
                            location,
                            "catalog.forbidden_target_topology",
                            f"target assertion contains forbidden topology term {term!r}",
                        )
                    )

    for family in sorted(required_families - covered_families):
        diagnostics.append(
            Diagnostic(
                str(path),
                "$.required_families",
                "catalog.uncovered_family",
                f"required family {family!r} has no scenario record",
            )
        )


def _is_safe_relative_path(value: str) -> bool:
    if not value or value.startswith(("/", "~")) or "\\" in value:
        return False
    parts = PurePosixPath(value).parts
    return bool(parts) and all(part not in {"", ".", ".."} for part in parts)


def _validate_adapter_reference(
    catalog_path: Path,
    scenario_location: str,
    reference: str,
    diagnostics: list[Diagnostic],
) -> None:
    module_path, _, _ = reference.partition(":")
    if not _is_safe_relative_path(module_path):
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{scenario_location}.binding.adapter",
                "catalog.unsafe_adapter",
                f"adapter module {module_path!r} must be fixture-relative",
            )
        )


def _mapping_contains_term(value: object, term: str) -> bool:
    if isinstance(value, str):
        return _contains_vocabulary_phrase(value, term)
    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, object], value)
        return any(_mapping_contains_term(item, term) for item in mapping.values())
    if isinstance(value, list):
        values = cast(list[object], value)
        return any(_mapping_contains_term(item, term) for item in values)
    return False


def _contains_vocabulary_phrase(value: str, term: str) -> bool:
    """Match exact vocabulary tokens across display/runtime separators."""

    haystack = tuple(_VOCABULARY_TOKEN.findall(value.casefold()))
    needle = tuple(_VOCABULARY_TOKEN.findall(term.casefold()))
    if not needle or len(needle) > len(haystack):
        return False
    width = len(needle)
    return any(
        haystack[index : index + width] == needle
        for index in range(len(haystack) - width + 1)
    )


def _immutable_adapter_input(scenario: Mapping[str, object]) -> Mapping[str, object]:
    """Detach and recursively freeze expectations before adapter invocation."""

    detached = copy.deepcopy(dict(scenario))
    return cast(Mapping[str, object], _freeze_value(detached))


def _freeze_value(value: object) -> object:
    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, object], value)
        return MappingProxyType(
            {key: _freeze_value(item) for key, item in mapping.items()}
        )
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in cast(list[object], value))
    return value


def _validated_observation(
    observation: Mapping[str, object],
) -> Mapping[str, object]:
    fields = frozenset(observation)
    if fields != _OBSERVATION_FIELDS:
        missing = sorted(_OBSERVATION_FIELDS - fields)
        unknown = sorted(fields - _OBSERVATION_FIELDS)
        raise ValueError(
            f"observation fields must be exact; missing={missing}, unknown={unknown}"
        )
    transition = observation["transition"]
    stop_reason = observation["stop_reason"]
    if transition is not None and not isinstance(transition, str):
        raise ValueError("observation.transition must be a string or null")
    if stop_reason is not None and not isinstance(stop_reason, str):
        raise ValueError("observation.stop_reason must be a string or null")
    for field in ("writes", "forbidden_writes"):
        values = observation[field]
        if not isinstance(values, list):
            raise ValueError(f"observation.{field} must contain safe relative paths")
        path_values = cast(list[object], values)
        if not all(
            isinstance(item, str) and _is_safe_relative_path(item)
            for item in path_values
        ):
            raise ValueError(f"observation.{field} must contain safe relative paths")
        typed_paths = cast(list[str], path_values)
        if len(typed_paths) != len(set(typed_paths)):
            raise ValueError(f"observation.{field} must not contain duplicates")
    validation = observation["validation"]
    if not isinstance(validation, list):
        raise ValueError("observation.validation must be a string list")
    validation_items = cast(list[object], validation)
    if not all(isinstance(item, str) for item in validation_items):
        raise ValueError("observation.validation must be a string list")
    generation_and_roots = observation["generation_and_roots"]
    if not isinstance(generation_and_roots, Mapping):
        raise ValueError("observation.generation_and_roots must be a mapping")
    root_facts = cast(Mapping[object, object], generation_and_roots)
    if frozenset(root_facts) != {"generation", "roots"}:
        raise ValueError("observation.generation_and_roots fields must be exact")
    typed_root_facts = cast(Mapping[str, object], root_facts)
    generation = typed_root_facts["generation"]
    roots = typed_root_facts["roots"]
    if generation is not None and not isinstance(generation, str):
        raise ValueError("observation generation must be a string or null")
    if not isinstance(roots, list):
        raise ValueError("observation roots must be a list")
    for root in cast(list[object], roots):
        if not isinstance(root, Mapping):
            raise ValueError("observation root fields must be exactly role and path")
        root_mapping = cast(Mapping[object, object], root)
        if frozenset(root_mapping) != {"role", "path"}:
            raise ValueError("observation root fields must be exactly role and path")
        typed_root = cast(Mapping[str, object], root_mapping)
        if not isinstance(typed_root["role"], str) or not isinstance(
            typed_root["path"], str
        ):
            raise ValueError("observation root role and path must be strings")
        if not _is_safe_relative_path(cast(str, typed_root["path"])):
            raise ValueError("observation root path must be fixture-relative")
    return observation


def _evaluate_scenario(
    catalog: Catalog,
    scenario: Mapping[str, object],
) -> ScenarioEvaluation:
    scenario_id = cast(str, scenario["id"])
    family = cast(str, scenario["family"])
    contracts = tuple(cast(list[str], scenario["contracts"]))
    binding = cast(Mapping[str, object], scenario["binding"])
    status = cast(str, binding["status"])
    adapter_reference = cast(str | None, binding["adapter"])
    reason = cast(str | None, binding["reason"])
    if status != "bound":
        return ScenarioEvaluation(
            scenario_id, family, contracts, status, adapter_reference, reason, ()
        )
    if adapter_reference is None:
        return ScenarioEvaluation(
            scenario_id,
            family,
            contracts,
            "blocked",
            None,
            "bound scenario has no adapter",
            (),
        )
    try:
        canonical_scenario = copy.deepcopy(dict(scenario))
        adapter = _load_adapter(catalog.root, adapter_reference)
        observation = adapter(_immutable_adapter_input(canonical_scenario), catalog.root)
        if observation is None:
            return ScenarioEvaluation(
                scenario_id,
                family,
                contracts,
                "bound",
                adapter_reference,
                reason,
                (),
            )
        mismatches = compare_observation(canonical_scenario, observation)
    except Exception as error:  # fixture adapters become blocked evidence
        return ScenarioEvaluation(
            scenario_id,
            family,
            contracts,
            "blocked",
            adapter_reference,
            f"adapter failed: {type(error).__name__}: {error}",
            (),
        )
    return ScenarioEvaluation(
        scenario_id,
        family,
        contracts,
        "green" if not mismatches else "blocked",
        adapter_reference,
        None if not mismatches else "observation mismatch",
        mismatches,
    )


def _load_adapter(root: Path, reference: str) -> Adapter:
    module_name, separator, function_name = reference.partition(":")
    if separator != ":" or not function_name:
        raise ValueError(f"invalid adapter reference {reference!r}")
    module_path = (root / module_name).resolve()
    if not module_path.is_relative_to(root.resolve()):
        raise ValueError(f"adapter path escapes fixture root: {module_name!r}")
    if not module_path.is_file():
        raise FileNotFoundError(module_path)
    import_name = f"_command_owner_scenario_adapter_{abs(hash(module_path))}"
    spec = importlib.util.spec_from_file_location(import_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load adapter module {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[import_name] = module
    spec.loader.exec_module(module)
    adapter = getattr(cast(ModuleType, module), function_name, None)
    if not callable(adapter):
        raise TypeError(f"adapter {reference!r} is not callable")
    return cast(Adapter, adapter)


def _family_report(
    family: str,
    evaluations: tuple[ScenarioEvaluation, ...],
) -> Mapping[str, object]:
    members = tuple(item for item in evaluations if item.family == family)
    statuses = tuple(item.status for item in members)
    if statuses and all(status == "green" for status in statuses):
        status = "green"
    elif "blocked" in statuses:
        status = "blocked"
    elif "bound" in statuses:
        status = "bound"
    elif "unavailable" in statuses:
        status = "unavailable"
    else:
        status = "declared"
    return {
        "id": family,
        "status": status,
        "scenarios": [item.scenario_id for item in members],
    }


def _scenario_report(evaluation: ScenarioEvaluation) -> Mapping[str, object]:
    mismatches: list[Mapping[str, object]] = [
        {
            "field": mismatch.field,
            "expected": mismatch.expected,
            "actual": mismatch.actual,
        }
        for mismatch in evaluation.mismatches
    ]
    report: dict[str, object] = {
        "id": evaluation.scenario_id,
        "family": evaluation.family,
        "contracts": list(evaluation.contracts),
        "status": evaluation.status,
        "adapter": evaluation.adapter,
        "reason": evaluation.reason,
        "mismatches": mismatches,
    }
    return report


def _render_text_report(report: Mapping[str, object]) -> str:
    status_counts = cast(Mapping[str, int], report["status_counts"])
    contracts = cast(Mapping[str, list[str]], report["contracts"])
    families = cast(list[Mapping[str, object]], report["families"])
    lines = [
        f"schema: {report['schema']}",
        "statuses: "
        + ", ".join(
            f"{status}={status_counts[status]}" for status in _RUNTIME_STATUSES
        ),
        (
            "contracts: "
            f"required={len(contracts['required'])}, "
            f"declared={len(contracts['declared'])}, "
            f"green={len(contracts['green'])}"
        ),
        "families:",
    ]
    lines.extend(
        f"- {family['id']}: {family['status']}" for family in families
    )
    return "\n".join(lines) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("catalog")
    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("catalog")
    report_parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the non-installed catalog validation and report CLI."""

    arguments = _build_parser().parse_args(argv)
    result = validate_catalog(arguments.catalog)
    if not result.is_valid:
        for diagnostic in result.diagnostics:
            print(diagnostic, file=sys.stderr)
        return 1
    catalog = cast(Catalog, result.catalog)
    if arguments.subcommand == "validate":
        scenarios = cast(list[object], catalog.document["scenarios"])
        print(f"valid: {catalog.path} ({len(scenarios)} scenarios)")
        return 0
    report = build_report(catalog)
    if arguments.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_render_text_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
