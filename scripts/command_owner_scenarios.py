"""Validate and report topology-independent command-owner scenario catalogs."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ElementTree
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
    """Build an unobserved report whose aggregate gates remain false."""

    return _build_report(catalog, observed_test_outcomes={})


def build_observed_report(catalog: Catalog) -> Mapping[str, object]:
    """Build a report from internally observed candidate pytest outcomes."""

    outcomes = _observe_aggregate_test_outcomes(catalog)
    return _build_report(catalog, observed_test_outcomes=outcomes)


def _build_report(
    catalog: Catalog,
    *,
    observed_test_outcomes: Mapping[str, str],
) -> Mapping[str, object]:
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
    report: dict[str, object] = {
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
    aggregate = catalog.document.get("aggregate_evidence")
    if isinstance(aggregate, Mapping):
        report["aggregate_evidence"] = _build_aggregate_evidence_report(
            cast(Mapping[str, object], aggregate),
            evaluations,
            observed_test_outcomes,
        )
    return report


def _observe_aggregate_test_outcomes(catalog: Catalog) -> Mapping[str, str]:
    """Execute every aggregate evidence node under the exact harness root."""

    aggregate = catalog.document.get("aggregate_evidence")
    if not isinstance(aggregate, Mapping):
        return MappingProxyType({})
    nodes = sorted(
        {
            cast(str, test["node"])
            for gate in cast(list[Mapping[str, object]], aggregate["gates"])
            for test in cast(list[Mapping[str, object]], gate["tests"])
        }
    )
    candidate_root = _candidate_repository_root()
    interpreter = _candidate_interpreter(candidate_root)
    outcomes: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="command-owner-evidence-") as temporary:
        junit_root = Path(temporary)
        runtime_home = junit_root / "home"
        runtime_home.mkdir()
        environment = {
            "HOME": str(runtime_home),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": os.defpath,
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        }
        for index, node in enumerate(nodes):
            junit_path = junit_root / f"outcome-{index}.xml"
            process = subprocess.run(
                [
                    str(interpreter),
                    "-P",
                    "-m",
                    "pytest",
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    "-rxX",
                    f"--junitxml={junit_path}",
                    node,
                ],
                cwd=candidate_root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            _require_exclusive_pytest_pass(node, process, junit_path)
            outcomes[node] = "passed"
    return MappingProxyType(outcomes)


def _candidate_interpreter(candidate_root: Path) -> Path:
    interpreter = candidate_root / ".venv/bin/python"
    if not interpreter.is_file():
        raise RuntimeError(
            f"candidate pytest interpreter is missing: {interpreter}"
        )
    probe = subprocess.run(
        [
            str(interpreter),
            "-P",
            "-c",
            "import json,sys; print(json.dumps({'executable': sys.executable, "
            "'prefix': sys.prefix, 'safe_path': sys.flags.safe_path}))",
        ],
        cwd=candidate_root,
        env={
            "HOME": str(candidate_root),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": os.defpath,
        },
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        loaded_identity = cast(object, json.loads(probe.stdout))
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"candidate pytest interpreter identity is unreadable: {interpreter}"
        ) from error
    identity = (
        cast(dict[str, object], loaded_identity)
        if isinstance(loaded_identity, dict)
        else {}
    )
    expected_prefix = candidate_root / ".venv"
    if (
        probe.returncode != 0
        or not identity
        or Path(str(identity.get("executable"))) != interpreter
        or Path(str(identity.get("prefix"))).resolve() != expected_prefix.resolve()
        or identity.get("safe_path") is not True
    ):
        raise RuntimeError(
            f"candidate pytest interpreter has foreign provenance: {interpreter}"
        )
    return interpreter


def _require_exclusive_pytest_pass(
    node: str,
    process: subprocess.CompletedProcess[str],
    junit_path: Path,
) -> None:
    combined_output = f"{process.stdout}\n{process.stderr}"
    explicit_non_pass = re.search(r"\b(?:XFAIL|XPASS)\b", combined_output)
    try:
        root = ElementTree.parse(junit_path).getroot()
    except (OSError, ElementTree.ParseError) as error:
        raise RuntimeError(
            f"aggregate test evidence node {node!r} produced no readable JUnit "
            f"result: {error}"
        ) from error
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    counts = {
        field: sum(int(suite.attrib.get(field, "0")) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    exclusive_pass = (
        process.returncode == 0
        and counts["tests"] > 0
        and counts["failures"] == 0
        and counts["errors"] == 0
        and counts["skipped"] == 0
        and explicit_non_pass is None
    )
    if not exclusive_pass:
        summary = " ".join(combined_output.split())[-600:]
        raise RuntimeError(
            f"aggregate test evidence node {node!r} did not pass exclusively "
            f"(exit={process.returncode}, counts={counts}): {summary}"
        )


def _build_aggregate_evidence_report(
    aggregate: Mapping[str, object],
    evaluations: tuple[ScenarioEvaluation, ...],
    observed_test_outcomes: Mapping[str, str],
) -> Mapping[str, object]:
    """Compute caller-owned aggregate gates from concrete green scenarios."""

    by_id = {item.scenario_id: item for item in evaluations}
    gates = cast(list[Mapping[str, object]], aggregate["gates"])
    keys: dict[str, bool] = {}
    aliases: dict[str, bool] = {}
    alias_targets: dict[str, str] = {}
    evidence: dict[str, Mapping[str, object]] = {}
    for gate in gates:
        key = cast(str, gate["key"])
        scenario_ids = cast(list[str], gate["scenarios"])
        non_green = [
            scenario_id
            for scenario_id in scenario_ids
            if by_id[scenario_id].status != "green"
        ]
        if non_green:
            raise ValueError(
                f"aggregate evidence key {key!r} references non-green "
                f"scenario(s): {', '.join(non_green)}"
            )
        test_nodes = [
            cast(str, test["node"])
            for test in cast(list[Mapping[str, object]], gate["tests"])
        ]
        tests_green = all(
            observed_test_outcomes.get(node) == "passed" for node in test_nodes
        )
        keys[key] = tests_green
        evidence[key] = {
            "scenarios": list(scenario_ids),
            "tests": [
                {
                    "node": cast(str, test["node"]),
                    "source_sha256": cast(str, test["source_sha256"]),
                    "scenarios": list(cast(list[str], test["scenarios"])),
                }
                for test in cast(list[Mapping[str, object]], gate["tests"])
            ],
        }
        for alias in cast(list[str], gate["aliases"]):
            aliases[alias] = tests_green
            alias_targets[alias] = key
    return {
        "keys": keys,
        "aliases": aliases,
        "alias_targets": alias_targets,
        "test_outcomes": {
            node: observed_test_outcomes.get(node, "not-observed")
            for node in sorted(
                {
                    cast(str, test["node"])
                    for gate in gates
                    for test in cast(list[Mapping[str, object]], gate["tests"])
                }
            )
        },
        "evidence": evidence,
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

    if diagnostics:
        return

    aggregate = document.get("aggregate_evidence")
    if not isinstance(aggregate, Mapping):
        return
    aggregate = cast(Mapping[str, object], aggregate)
    gates = cast(list[Mapping[str, object]], aggregate["gates"])
    seen_keys: dict[str, int] = {}
    seen_aliases: dict[str, tuple[int, str]] = {}
    for gate_index, gate in enumerate(gates):
        gate_location = f"$.aggregate_evidence.gates[{gate_index}]"
        key = cast(str, gate["key"])
        if key in seen_keys:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    f"{gate_location}.key",
                    "catalog.duplicate_evidence_key",
                    f"evidence key {key!r} also appears at index {seen_keys[key]}",
                )
            )
        else:
            seen_keys[key] = gate_index
        for alias_index, alias in enumerate(cast(list[str], gate["aliases"])):
            previous = seen_aliases.get(alias)
            if previous is not None:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{gate_location}.aliases[{alias_index}]",
                        "catalog.duplicate_evidence_alias",
                        f"evidence alias {alias!r} also appears at gate {previous[0]}",
                    )
                )
            else:
                seen_aliases[alias] = (gate_index, key)
        for scenario_index, scenario_id in enumerate(
            cast(list[str], gate["scenarios"])
        ):
            if scenario_id not in seen_ids:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{gate_location}.scenarios[{scenario_index}]",
                        "catalog.unknown_evidence_scenario",
                        f"evidence scenario {scenario_id!r} is not declared",
                    )
                )
        gate_scenarios = set(cast(list[str], gate["scenarios"]))
        test_coverage: set[str] = set()
        seen_test_nodes: dict[str, int] = {}
        for test_index, test in enumerate(
            cast(list[Mapping[str, object]], gate["tests"])
        ):
            test_location = f"{gate_location}.tests[{test_index}]"
            node = cast(str, test["node"])
            if node in seen_test_nodes:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{test_location}.node",
                        "catalog.duplicate_test_evidence",
                        f"test evidence {node!r} also appears at index {seen_test_nodes[node]}",
                    )
                )
            else:
                seen_test_nodes[node] = test_index
            _validate_test_evidence_node(
                path,
                node,
                cast(str, test["source_sha256"]),
                test_location,
                diagnostics,
            )
            evidence_scenarios = set(cast(list[str], test["scenarios"]))
            unknown = evidence_scenarios - set(seen_ids)
            unrelated = evidence_scenarios - gate_scenarios
            for scenario_id in sorted(unknown):
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{test_location}.scenarios",
                        "catalog.unknown_test_evidence_scenario",
                        f"test evidence scenario {scenario_id!r} is not declared",
                    )
                )
            for scenario_id in sorted(unrelated - unknown):
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{test_location}.scenarios",
                        "catalog.unrelated_test_evidence_scenario",
                        f"test evidence scenario {scenario_id!r} is outside gate {key!r}",
                    )
                )
            test_coverage.update(evidence_scenarios & gate_scenarios)
        missing_test_coverage = gate_scenarios - test_coverage
        if missing_test_coverage:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    f"{gate_location}.tests",
                    "catalog.missing_test_evidence_coverage",
                    "gate scenarios lack test evidence: "
                    + ", ".join(sorted(missing_test_coverage)),
                )
            )

    all_keys = set(seen_keys)
    for alias, (gate_index, target_key) in seen_aliases.items():
        if alias in all_keys and alias != target_key:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    f"$.aggregate_evidence.gates[{gate_index}].aliases",
                    "catalog.evidence_alias_key_collision",
                    f"evidence alias {alias!r} collides with another gate key",
                )
            )


def _validate_test_evidence_node(
    catalog_path: Path,
    node: str,
    expected_sha256: str,
    location: str,
    diagnostics: list[Diagnostic],
) -> None:
    relative_name, separator, function_name = node.partition("::")
    if separator != "::" or not _is_safe_relative_path(relative_name):
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.invalid_test_evidence_node",
                f"test evidence node {node!r} must be a safe path and test function",
            )
        )
        return
    candidate_root = _candidate_repository_root()
    unresolved_test_path = candidate_root / relative_name
    if not unresolved_test_path.is_file():
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.missing_test_evidence_node",
                f"test evidence node {node!r} does not resolve to a file",
            )
        )
        return
    test_path = unresolved_test_path.resolve()
    if not test_path.is_relative_to(candidate_root) or test_path != unresolved_test_path:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.foreign_test_evidence_path",
                f"test evidence node {node!r} escapes the candidate harness root",
            )
        )
        return
    try:
        source = test_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(test_path))
    except (OSError, SyntaxError) as error:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.invalid_test_evidence_source",
                f"could not inspect test evidence {node!r}: {error}",
            )
        )
        return
    declared_functions = {
        item.name: item
        for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if function_name not in declared_functions:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.missing_test_evidence_function",
                f"test evidence function {function_name!r} is not declared in {test_path}",
            )
        )
        return
    function = declared_functions[function_name]
    disabled_decorators = sorted(
        mark
        for decorator in function.decorator_list
        if (mark := _disabled_pytest_mark(decorator)) is not None
    )
    if disabled_decorators:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.disabled_test_evidence_decorator",
                "test evidence uses disabling decorator(s): "
                + ", ".join(disabled_decorators),
            )
        )
    collection_controls = _module_collection_controls(tree)
    disabled_controls = sorted(
        control
        for control, node_value in collection_controls
        if _collection_control_disables(node_value)
    )
    if disabled_controls:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.disabled_test_evidence_module",
                "test module uses disabling collection control(s): "
                + ", ".join(disabled_controls),
            )
        )
    function_start = min(
        [function.lineno, *(decorator.lineno for decorator in function.decorator_list)]
    )
    source_lines = source.splitlines(keepends=True)
    function_source = "".join(source_lines[function_start - 1 : function.end_lineno])
    control_sources = [
        ast.get_source_segment(source, node_value)
        for _control, node_value in collection_controls
    ]
    if not function_source or any(item is None for item in control_sources):
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.unreadable_test_evidence_function",
                f"could not extract source for test evidence function {function_name!r}",
            )
        )
        return
    grounded_source = json.dumps(
        {
            "collected_test_definition": function_source,
            "module_collection_controls": control_sources,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    observed_sha256 = hashlib.sha256(grounded_source.encode()).hexdigest()
    if observed_sha256 != expected_sha256:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.source_sha256",
                "catalog.test_evidence_source_mismatch",
                f"test evidence source hash is {observed_sha256}, expected {expected_sha256}",
            )
        )


def _candidate_repository_root() -> Path:
    """Return the repository root that owns this exact harness source."""

    return Path(__file__).resolve().parents[1]


def _module_collection_controls(
    tree: ast.Module,
) -> list[tuple[str, ast.Assign | ast.AnnAssign]]:
    controls: list[tuple[str, ast.Assign | ast.AnnAssign]] = []
    names = {"__test__", "pytest_plugins", "pytestmark"}
    for item in tree.body:
        if isinstance(item, ast.Assign):
            assigned = {
                target.id for target in item.targets if isinstance(target, ast.Name)
            }
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            assigned = {item.target.id}
        else:
            continue
        for name in sorted(assigned & names):
            controls.append((name, item))
    return controls


def _disabled_pytest_mark(node: ast.AST) -> str | None:
    target = node.func if isinstance(node, ast.Call) else node
    parts: list[str] = []
    while isinstance(target, ast.Attribute):
        parts.append(target.attr)
        target = target.value
    if isinstance(target, ast.Name):
        parts.append(target.id)
    dotted = ".".join(reversed(parts))
    if dotted.endswith((".skip", ".skipif", ".xfail")):
        return dotted
    return None


def _collection_control_disables(node: ast.Assign | ast.AnnAssign) -> bool:
    if isinstance(node, ast.Assign):
        values = [node.value]
        if any(
            isinstance(target, ast.Name)
            and target.id == "__test__"
            and isinstance(node.value, ast.Constant)
            and node.value.value is False
            for target in node.targets
        ):
            return True
    else:
        values = [node.value] if node.value is not None else []
        if (
            isinstance(node.target, ast.Name)
            and node.target.id == "__test__"
            and isinstance(node.value, ast.Constant)
            and node.value.value is False
        ):
            return True
    return any(
        _disabled_pytest_mark(candidate) is not None
        for value in values
        for candidate in ast.walk(value)
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
    try:
        report = build_observed_report(catalog)
    except RuntimeError as error:
        print(f"aggregate evidence failed: {error}", file=sys.stderr)
        return 1
    if arguments.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_render_text_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
