"""Validate, accept, and report topology-independent command-owner scenarios."""

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
import time
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
ACCEPTANCE_RECEIPT_VERSION: Final = "command-owner-acceptance-receipt/v1"
SCHEMA_RELATIVE_PATH: Final = Path("schemas/command-owner-scenario-v1.schema.json")
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
_DESELECTED_COUNT: Final = re.compile(r"(?P<count>\d+)\s+deselected\b")
_EXPLICIT_NON_PASS: Final = re.compile(r"\b(?:XFAIL|XPASS)\b")
_EVALUATION_CACHE: dict[tuple[str, str, str], "ScenarioEvaluation"] = {}


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


def evaluate_scenarios(
    catalog: Catalog,
    scenario_ids: Sequence[str] | None = None,
) -> tuple[ScenarioEvaluation, ...]:
    """Evaluate each immutable scenario at most once per process/input identity."""

    scenarios = {
        cast(str, scenario["id"]): scenario
        for scenario in cast(list[Mapping[str, object]], catalog.document["scenarios"])
    }
    selected = tuple(sorted(scenarios if scenario_ids is None else scenario_ids))
    unknown = sorted(set(selected) - set(scenarios))
    if unknown:
        raise ValueError(f"unknown scenario id(s): {', '.join(unknown)}")

    fingerprint = _catalog_runtime_fingerprint(catalog)
    path_key = str(catalog.path.resolve())
    evaluations: list[ScenarioEvaluation] = []
    for scenario_id in selected:
        key = (path_key, fingerprint, scenario_id)
        evaluation = _EVALUATION_CACHE.get(key)
        if evaluation is None:
            evaluation = _evaluate_scenario(catalog, scenarios[scenario_id])
            _EVALUATION_CACHE[key] = evaluation
        evaluations.append(evaluation)
    return tuple(evaluations)


def evaluate_catalog(catalog: Catalog) -> tuple[ScenarioEvaluation, ...]:
    """Evaluate the complete declared catalog through the shared scenario cache."""

    return evaluate_scenarios(catalog)


def build_report(catalog: Catalog) -> Mapping[str, object]:
    """Build an unobserved report whose aggregate gates remain false."""

    return _build_report(catalog, evaluate_catalog(catalog), observed_test_outcomes={})


def run_acceptance(
    catalog: Catalog,
    receipt_path: str | Path,
) -> Mapping[str, object]:
    """Run one exact-commit acceptance flight and persist its reusable receipt."""

    candidate_root = _candidate_repository_root()
    destination = Path(receipt_path).resolve()
    _require_external_receipt_path(destination, candidate_root)
    before = _acceptance_identity(catalog)
    if not before["worktree_clean"]:
        raise RuntimeError("candidate worktree must be clean before acceptance")

    interpreter = _candidate_interpreter(candidate_root)
    evidence = _run_evidence_nodes(catalog, interpreter)
    evaluations = evaluate_catalog(catalog)
    report = _build_report(
        catalog,
        evaluations,
        observed_test_outcomes=cast(Mapping[str, str], evidence["node_outcomes"]),
    )

    after = _acceptance_identity(catalog)
    if before != after:
        raise RuntimeError("candidate acceptance inputs moved during execution")

    payload: dict[str, object] = {
        "schema": ACCEPTANCE_RECEIPT_VERSION,
        "candidate_commit": before["candidate_commit"],
        "catalog_sha256": before["catalog_sha256"],
        "sources_sha256": before["sources_sha256"],
        "nodes": before["nodes"],
        "interpreter": evidence["interpreter"],
        "safe_path": evidence["safe_path"],
        "counts": evidence["counts"],
        "deselected": evidence["deselected"],
        "node_outcomes": evidence["node_outcomes"],
        "junit_sha256": evidence["junit_sha256"],
        "duration_ms": evidence["duration_ms"],
        "report": report,
    }
    payload["receipt_sha256"] = _mapping_sha256(payload)
    _write_json_atomic(destination, payload)
    return payload


def load_acceptance_receipt(
    catalog: Catalog,
    receipt_path: str | Path,
) -> Mapping[str, object]:
    """Load and verify an exact-commit acceptance receipt without running pytest."""

    path = Path(receipt_path).resolve()
    try:
        loaded = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"acceptance receipt is unreadable: {path}: {error}") from error
    if not isinstance(loaded, dict):
        raise RuntimeError("acceptance receipt must be a JSON object")
    receipt = cast(dict[str, object], loaded)
    _verify_acceptance_receipt(catalog, receipt)
    return receipt


def report_from_receipt(
    catalog: Catalog,
    receipt_path: str | Path,
) -> Mapping[str, object]:
    """Return the accepted report embedded in one verified receipt."""

    receipt = load_acceptance_receipt(catalog, receipt_path)
    report = receipt["report"]
    if not isinstance(report, Mapping):
        raise RuntimeError("acceptance receipt report must be a mapping")
    return cast(Mapping[str, object], report)


def render_json_report(report: Mapping[str, object]) -> str:
    """Render one already-built report deterministically as JSON."""

    return json.dumps(_jsonable(report), indent=2, sort_keys=True) + "\n"


def render_text_report(report: Mapping[str, object]) -> str:
    """Render one already-built report deterministically as compact text."""

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
    lines.extend(f"- {family['id']}: {family['status']}" for family in families)
    aggregate = report.get("aggregate_evidence")
    if isinstance(aggregate, Mapping):
        keys = cast(Mapping[str, bool], aggregate["keys"])
        lines.append("aggregate:")
        lines.extend(f"- {key}: {str(value).lower()}" for key, value in sorted(keys.items()))
    return "\n".join(lines) + "\n"


def _build_report(
    catalog: Catalog,
    evaluations: tuple[ScenarioEvaluation, ...],
    *,
    observed_test_outcomes: Mapping[str, str],
) -> Mapping[str, object]:
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
            "all_required_contracts_green": set(required_contracts) == green_contracts,
            "all_required_families_green": all(
                family["status"] == "green" for family in family_reports
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


def _run_evidence_nodes(
    catalog: Catalog,
    interpreter: Path,
) -> Mapping[str, object]:
    nodes = _aggregate_test_nodes(catalog)
    if not nodes:
        return {
            "interpreter": str(interpreter),
            "safe_path": True,
            "counts": {"tests": 0, "failures": 0, "errors": 0, "skipped": 0},
            "deselected": 0,
            "node_outcomes": {},
            "junit_sha256": hashlib.sha256(b"").hexdigest(),
            "duration_ms": 0,
        }

    candidate_root = _candidate_repository_root()
    with tempfile.TemporaryDirectory(prefix="command-owner-acceptance-") as temporary:
        temporary_root = Path(temporary)
        junit_path = temporary_root / "acceptance.xml"
        runtime_home = temporary_root / "home"
        runtime_home.mkdir()
        environment = {
            "HOME": str(runtime_home),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": os.defpath,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        }
        command = [
            str(interpreter),
            "-P",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "-rxX",
            f"--junitxml={junit_path}",
            *nodes,
        ]
        started = time.monotonic()
        process = subprocess.run(
            command,
            cwd=candidate_root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        duration_ms = round((time.monotonic() - started) * 1000)
        result = _require_combined_pytest_pass(nodes, process, junit_path)
        return {
            "interpreter": str(interpreter),
            "safe_path": True,
            "counts": result["counts"],
            "deselected": result["deselected"],
            "node_outcomes": {node: "passed" for node in nodes},
            "junit_sha256": hashlib.sha256(junit_path.read_bytes()).hexdigest(),
            "duration_ms": duration_ms,
        }


def _require_combined_pytest_pass(
    nodes: tuple[str, ...],
    process: subprocess.CompletedProcess[str],
    junit_path: Path,
) -> Mapping[str, object]:
    combined_output = f"{process.stdout}\n{process.stderr}"
    try:
        root = ElementTree.parse(junit_path).getroot()
    except (OSError, ElementTree.ParseError) as error:
        raise RuntimeError(
            f"aggregate test evidence produced no readable JUnit result: {error}"
        ) from error

    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    if not suites:
        suites = list(root.iter("testsuite"))
    counts = {
        field: sum(int(suite.attrib.get(field, "0")) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    deselected_matches = [
        int(match.group("count")) for match in _DESELECTED_COUNT.finditer(combined_output)
    ]
    deselected = max(deselected_matches, default=0)
    observed_names = {
        cast(str, testcase.attrib.get("name", "")).split("[", 1)[0]
        for testcase in root.iter("testcase")
    }
    expected_functions = {node.partition("::")[2] for node in nodes}
    missing_functions = sorted(expected_functions - observed_names)
    exclusive_pass = (
        process.returncode == 0
        and counts["tests"] > 0
        and counts["failures"] == 0
        and counts["errors"] == 0
        and counts["skipped"] == 0
        and deselected == 0
        and _EXPLICIT_NON_PASS.search(combined_output) is None
        and not missing_functions
    )
    if not exclusive_pass:
        summary = " ".join(combined_output.split())[-800:]
        raise RuntimeError(
            "aggregate test evidence did not pass exclusively "
            f"(exit={process.returncode}, counts={counts}, deselected={deselected}, "
            f"missing={missing_functions}): {summary}"
        )
    return {"counts": counts, "deselected": deselected}


def _candidate_interpreter(candidate_root: Path) -> Path:
    interpreter = candidate_root / ".venv/bin/python"
    if not interpreter.is_file():
        raise RuntimeError(f"candidate pytest interpreter is missing: {interpreter}")
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


def _acceptance_identity(catalog: Catalog) -> Mapping[str, object]:
    candidate_root = _candidate_repository_root()
    commit = _git(candidate_root, "rev-parse", "HEAD")
    status = _git(
        candidate_root,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    )
    return {
        "candidate_commit": commit,
        "worktree_clean": not status,
        "catalog_sha256": hashlib.sha256(catalog.path.read_bytes()).hexdigest(),
        "sources_sha256": _acceptance_sources_sha256(catalog),
        "nodes": list(_aggregate_test_nodes(catalog)),
    }


def _acceptance_sources_sha256(catalog: Catalog) -> str:
    candidate_root = _candidate_repository_root()
    paths: set[Path] = {
        Path(__file__).resolve(),
        (candidate_root / SCHEMA_RELATIVE_PATH).resolve(),
        catalog.path.resolve(),
    }
    for path in catalog.root.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            paths.add(path.resolve())
    for node in _aggregate_test_nodes(catalog):
        relative_name = node.partition("::")[0]
        paths.add((candidate_root / relative_name).resolve())

    digest = hashlib.sha256()
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f"acceptance source is missing: {path}")
        try:
            label = path.relative_to(candidate_root).as_posix()
        except ValueError:
            label = str(path)
        digest.update(label.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _verify_acceptance_receipt(
    catalog: Catalog,
    receipt: Mapping[str, object],
) -> None:
    required = {
        "schema",
        "candidate_commit",
        "catalog_sha256",
        "sources_sha256",
        "nodes",
        "interpreter",
        "safe_path",
        "counts",
        "deselected",
        "node_outcomes",
        "junit_sha256",
        "duration_ms",
        "report",
        "receipt_sha256",
    }
    if set(receipt) != required:
        raise RuntimeError(
            "acceptance receipt fields must be exact; "
            f"missing={sorted(required - set(receipt))}, "
            f"unknown={sorted(set(receipt) - required)}"
        )
    if receipt["schema"] != ACCEPTANCE_RECEIPT_VERSION:
        raise RuntimeError("unsupported acceptance receipt schema")
    digest_payload = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if receipt["receipt_sha256"] != _mapping_sha256(digest_payload):
        raise RuntimeError("acceptance receipt digest does not match its payload")

    identity = _acceptance_identity(catalog)
    if not identity["worktree_clean"]:
        raise RuntimeError("candidate worktree must be clean to reuse acceptance evidence")
    for field in ("candidate_commit", "catalog_sha256", "sources_sha256", "nodes"):
        if receipt[field] != identity[field]:
            raise RuntimeError(f"acceptance receipt {field} does not match current inputs")

    counts = receipt["counts"]
    outcomes = receipt["node_outcomes"]
    if not isinstance(counts, Mapping) or set(counts) != {
        "tests",
        "failures",
        "errors",
        "skipped",
    }:
        raise RuntimeError("acceptance receipt counts are invalid")
    if (
        not isinstance(outcomes, Mapping)
        or set(outcomes) != set(cast(list[str], receipt["nodes"]))
        or set(outcomes.values()) != {"passed"}
        or not isinstance(counts["tests"], int)
        or counts["tests"] <= 0
        or counts["failures"] != 0
        or counts["errors"] != 0
        or counts["skipped"] != 0
        or receipt["deselected"] != 0
        or receipt["safe_path"] is not True
    ):
        raise RuntimeError("acceptance receipt does not prove an exclusive pass")
    if receipt["interpreter"] != str(_candidate_interpreter(_candidate_repository_root())):
        raise RuntimeError("acceptance receipt interpreter does not match candidate")
    if not isinstance(receipt["duration_ms"], int) or receipt["duration_ms"] < 0:
        raise RuntimeError("acceptance receipt duration is invalid")
    if not isinstance(receipt["junit_sha256"], str) or not re.fullmatch(
        r"[0-9a-f]{64}", receipt["junit_sha256"]
    ):
        raise RuntimeError("acceptance receipt JUnit digest is invalid")
    report = receipt["report"]
    if not isinstance(report, Mapping):
        raise RuntimeError("acceptance receipt report must be a mapping")
    aggregate = report.get("aggregate_evidence")
    if not isinstance(aggregate, Mapping):
        raise RuntimeError("acceptance receipt report has no aggregate evidence")
    if not all(cast(Mapping[str, bool], aggregate["keys"]).values()):
        raise RuntimeError("acceptance receipt report contains a false acceptance key")
    if not all(cast(Mapping[str, bool], aggregate["aliases"]).values()):
        raise RuntimeError("acceptance receipt report contains a false acceptance alias")


def _jsonable(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _mapping_sha256(value: Mapping[str, object]) -> str:
    encoded = json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _write_json_atomic(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(render_json_report(value), encoding="utf-8")
    os.replace(temporary, path)


def _require_external_receipt_path(path: Path, candidate_root: Path) -> None:
    root = candidate_root.resolve()
    if path == root or path.is_relative_to(root):
        raise RuntimeError("acceptance receipt path must be outside the candidate repository")


def _aggregate_test_nodes(catalog: Catalog) -> tuple[str, ...]:
    aggregate = catalog.document.get("aggregate_evidence")
    if not isinstance(aggregate, Mapping):
        return ()
    return tuple(
        sorted(
            {
                cast(str, test["node"])
                for gate in cast(list[Mapping[str, object]], aggregate["gates"])
                for test in cast(list[Mapping[str, object]], gate["tests"])
            }
        )
    )


def _build_aggregate_evidence_report(
    aggregate: Mapping[str, object],
    evaluations: tuple[ScenarioEvaluation, ...],
    observed_test_outcomes: Mapping[str, str],
) -> Mapping[str, object]:
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
        tests = cast(list[Mapping[str, object]], gate["tests"])
        test_nodes = [cast(str, test["node"]) for test in tests]
        tests_green = all(
            observed_test_outcomes.get(node) == "passed" for node in test_nodes
        )
        keys[key] = tests_green
        evidence[key] = {
            "scenarios": list(scenario_ids),
            "tests": [
                {
                    "node": cast(str, test["node"]),
                    "scenarios": list(cast(list[str], test["scenarios"])),
                }
                for test in tests
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
        diagnostics.append(Diagnostic(str(path), "$", "catalog.read", str(error)))
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
    schema_path = _candidate_repository_root() / SCHEMA_RELATIVE_PATH
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
        for contract_index, contract in enumerate(cast(list[str], scenario["contracts"])):
            if contract not in required_contracts:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"{location}.contracts[{contract_index}]",
                        "catalog.unknown_contract",
                        f"contract {contract!r} is not in required_contracts",
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
    if isinstance(aggregate, Mapping):
        _validate_aggregate_evidence(
            path,
            cast(Mapping[str, object], aggregate),
            set(seen_ids),
            diagnostics,
        )


def _validate_aggregate_evidence(
    catalog_path: Path,
    aggregate: Mapping[str, object],
    scenario_ids: set[str],
    diagnostics: list[Diagnostic],
) -> None:
    gates = cast(list[Mapping[str, object]], aggregate["gates"])
    seen_keys: dict[str, int] = {}
    seen_aliases: dict[str, tuple[int, str]] = {}
    seen_functions: dict[str, str] = {}
    for gate_index, gate in enumerate(gates):
        location = f"$.aggregate_evidence.gates[{gate_index}]"
        key = cast(str, gate["key"])
        if key in seen_keys:
            diagnostics.append(
                Diagnostic(
                    str(catalog_path),
                    f"{location}.key",
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
                        str(catalog_path),
                        f"{location}.aliases[{alias_index}]",
                        "catalog.duplicate_evidence_alias",
                        f"evidence alias {alias!r} also appears at gate {previous[0]}",
                    )
                )
            else:
                seen_aliases[alias] = (gate_index, key)

        gate_scenarios = set(cast(list[str], gate["scenarios"]))
        for index, scenario_id in enumerate(cast(list[str], gate["scenarios"])):
            if scenario_id not in scenario_ids:
                diagnostics.append(
                    Diagnostic(
                        str(catalog_path),
                        f"{location}.scenarios[{index}]",
                        "catalog.unknown_evidence_scenario",
                        f"evidence scenario {scenario_id!r} is not declared",
                    )
                )

        coverage: set[str] = set()
        seen_nodes: dict[str, int] = {}
        for test_index, test in enumerate(cast(list[Mapping[str, object]], gate["tests"])):
            test_location = f"{location}.tests[{test_index}]"
            node = cast(str, test["node"])
            if node in seen_nodes:
                diagnostics.append(
                    Diagnostic(
                        str(catalog_path),
                        f"{test_location}.node",
                        "catalog.duplicate_test_evidence",
                        f"test evidence {node!r} also appears at index {seen_nodes[node]}",
                    )
                )
            else:
                seen_nodes[node] = test_index
            function_name = _validate_test_evidence_node(
                catalog_path, node, test_location, diagnostics
            )
            if function_name is not None:
                prior_node = seen_functions.get(function_name)
                if prior_node is not None and prior_node != node:
                    diagnostics.append(
                        Diagnostic(
                            str(catalog_path),
                            f"{test_location}.node",
                            "catalog.ambiguous_test_evidence_function",
                            f"test function {function_name!r} is also referenced by {prior_node!r}",
                        )
                    )
                else:
                    seen_functions[function_name] = node
            evidence_scenarios = set(cast(list[str], test["scenarios"]))
            unknown = evidence_scenarios - scenario_ids
            unrelated = evidence_scenarios - gate_scenarios
            for scenario_id in sorted(unknown):
                diagnostics.append(
                    Diagnostic(
                        str(catalog_path),
                        f"{test_location}.scenarios",
                        "catalog.unknown_test_evidence_scenario",
                        f"test evidence scenario {scenario_id!r} is not declared",
                    )
                )
            for scenario_id in sorted(unrelated - unknown):
                diagnostics.append(
                    Diagnostic(
                        str(catalog_path),
                        f"{test_location}.scenarios",
                        "catalog.unrelated_test_evidence_scenario",
                        f"test evidence scenario {scenario_id!r} is outside gate {key!r}",
                    )
                )
            coverage.update(evidence_scenarios & gate_scenarios)
        missing = gate_scenarios - coverage
        if missing:
            diagnostics.append(
                Diagnostic(
                    str(catalog_path),
                    f"{location}.tests",
                    "catalog.missing_test_evidence_coverage",
                    "gate scenarios lack test evidence: " + ", ".join(sorted(missing)),
                )
            )

    all_keys = set(seen_keys)
    for alias, (gate_index, target_key) in seen_aliases.items():
        if alias in all_keys and alias != target_key:
            diagnostics.append(
                Diagnostic(
                    str(catalog_path),
                    f"$.aggregate_evidence.gates[{gate_index}].aliases",
                    "catalog.evidence_alias_key_collision",
                    f"evidence alias {alias!r} collides with another gate key",
                )
            )


def _validate_test_evidence_node(
    catalog_path: Path,
    node: str,
    location: str,
    diagnostics: list[Diagnostic],
) -> str | None:
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
        return None
    candidate_root = _candidate_repository_root()
    unresolved = candidate_root / relative_name
    if not unresolved.is_file():
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.missing_test_evidence_node",
                f"test evidence node {node!r} does not resolve to a file",
            )
        )
        return None
    test_path = unresolved.resolve()
    if not test_path.is_relative_to(candidate_root) or test_path != unresolved:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.foreign_test_evidence_path",
                f"test evidence node {node!r} escapes the candidate harness root",
            )
        )
        return None
    try:
        tree = ast.parse(test_path.read_text(encoding="utf-8"), filename=str(test_path))
    except (OSError, SyntaxError) as error:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.invalid_test_evidence_source",
                f"could not inspect test evidence {node!r}: {error}",
            )
        )
        return None
    declared = {
        item.name
        for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if function_name not in declared:
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.node",
                "catalog.missing_test_evidence_function",
                f"test evidence function {function_name!r} is not declared in {test_path}",
            )
        )
        return None
    return function_name


def _validate_adapter_reference(
    catalog_path: Path,
    location: str,
    reference: str,
    diagnostics: list[Diagnostic],
) -> None:
    module_name, separator, function_name = reference.partition(":")
    if separator != ":" or not function_name or not _is_safe_relative_path(module_name):
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.binding.adapter",
                "catalog.invalid_adapter_reference",
                f"invalid adapter reference {reference!r}",
            )
        )
        return
    module_path = (catalog_path.parent / module_name).resolve()
    if not module_path.is_relative_to(catalog_path.parent.resolve()) or not module_path.is_file():
        diagnostics.append(
            Diagnostic(
                str(catalog_path),
                f"{location}.binding.adapter",
                "catalog.missing_adapter",
                f"adapter module {module_name!r} is unavailable",
            )
        )


def _mapping_contains_term(value: object, term: str) -> bool:
    expected = _VOCABULARY_TOKEN.findall(term.lower())
    if not expected:
        return False
    for text in _iter_strings(value):
        tokens = _VOCABULARY_TOKEN.findall(text.lower())
        width = len(expected)
        if any(tokens[index : index + width] == expected for index in range(len(tokens) - width + 1)):
            return True
    return False


def _iter_strings(value: object) -> Sequence[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str):
                strings.append(key)
            strings.extend(_iter_strings(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            strings.extend(_iter_strings(item))
    return strings


def _catalog_runtime_fingerprint(catalog: Catalog) -> str:
    digest = hashlib.sha256()
    digest.update(
        json.dumps(_jsonable(catalog.document), sort_keys=True, separators=(",", ":")).encode()
    )
    for path in sorted(catalog.root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        digest.update(path.relative_to(catalog.root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _validated_observation(observation: Mapping[str, object]) -> Mapping[str, object]:
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
        typed = cast(list[object], values)
        if not all(isinstance(item, str) and _is_safe_relative_path(item) for item in typed):
            raise ValueError(f"observation.{field} must contain safe relative paths")
        if len(typed) != len(set(cast(list[str], typed))):
            raise ValueError(f"observation.{field} must not contain duplicates")
    validation = observation["validation"]
    if not isinstance(validation, list) or not all(
        isinstance(item, str) for item in cast(list[object], validation)
    ):
        raise ValueError("observation.validation must be a string list")
    roots_value = observation["generation_and_roots"]
    if not isinstance(roots_value, Mapping) or frozenset(roots_value) != {
        "generation",
        "roots",
    }:
        raise ValueError("observation.generation_and_roots fields must be exact")
    roots_mapping = cast(Mapping[str, object], roots_value)
    generation = roots_mapping["generation"]
    roots = roots_mapping["roots"]
    if generation is not None and not isinstance(generation, str):
        raise ValueError("observation generation must be a string or null")
    if not isinstance(roots, list):
        raise ValueError("observation roots must be a list")
    for root in cast(list[object], roots):
        if not isinstance(root, Mapping) or frozenset(root) != {"role", "path"}:
            raise ValueError("observation root fields must be exactly role and path")
        typed_root = cast(Mapping[str, object], root)
        if not isinstance(typed_root["role"], str) or not isinstance(typed_root["path"], str):
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
    import_name = f"_command_owner_scenario_adapter_{hashlib.sha256(str(module_path).encode()).hexdigest()[:16]}"
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


def _immutable_adapter_input(
    scenario: Mapping[str, object],
) -> Mapping[str, object]:
    detached = copy.deepcopy(dict(scenario))
    return cast(Mapping[str, object], _freeze_value(detached))


def _freeze_value(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _freeze_value(item) for key, item in value.items()}
        )
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    return value


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
    return {
        "id": evaluation.scenario_id,
        "family": evaluation.family,
        "contracts": list(evaluation.contracts),
        "status": evaluation.status,
        "adapter": evaluation.adapter,
        "reason": evaluation.reason,
        "mismatches": [
            {
                "field": mismatch.field,
                "expected": mismatch.expected,
                "actual": mismatch.actual,
            }
            for mismatch in evaluation.mismatches
        ],
    }


def _is_safe_relative_path(value: str) -> bool:
    if not value or value.startswith(("/", "~")) or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _candidate_repository_root() -> Path:
    """Return the repository root that owns this exact harness source."""

    return Path(__file__).resolve().parents[1]


def _git(root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "git command failed"
        raise RuntimeError(f"could not inspect candidate Git state: {detail}")
    return process.stdout.strip()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("catalog")

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("catalog")
    report_parser.add_argument("--receipt")
    report_parser.add_argument("--format", choices=("text", "json"), default="text")

    accept_parser = subparsers.add_parser("accept")
    accept_parser.add_argument("catalog")
    accept_parser.add_argument("--receipt", required=True)
    accept_parser.add_argument("--format", choices=("text", "json"), default="json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run catalog validation, exact-commit acceptance, or pure reporting."""

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
        if arguments.subcommand == "accept":
            receipt = run_acceptance(catalog, arguments.receipt)
            report = cast(Mapping[str, object], receipt["report"])
        elif arguments.receipt:
            report = report_from_receipt(catalog, arguments.receipt)
        else:
            report = build_report(catalog)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"{arguments.subcommand} failed: {error}", file=sys.stderr)
        return 1

    if arguments.format == "json":
        print(render_json_report(report), end="")
    else:
        print(render_text_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
