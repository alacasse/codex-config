from __future__ import annotations

import copy
import importlib
import json
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
import pytest

import scripts.command_owner_scenarios as scenario_harness

from scripts.command_owner_scenarios import (
    build_report,
    compare_observation,
    validate_catalog,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/command-owner-scenarios"
VALID_RUNTIME = FIXTURES / "self-test/valid-runtime"
EXPECTED_CONTRACT_IDS = {
    "INTAKE-SOURCE-001",
    "INTAKE-IDENTITY-002",
    "INTAKE-NORMALIZE-003",
    "INTAKE-MUTATE-004",
    "INTAKE-STOP-005",
    "PLAN-SOURCE-001",
    "PLAN-ACTIVE-002",
    "PLAN-SELECT-003",
    "PLAN-SCOPE-004",
    "PLAN-DISPATCH-005",
    "PLAN-RUNWAY-006",
    "PLAN-RISK-007",
    "PLAN-STOP-008",
    "EXEC-CURRENT-001",
    "EXEC-RESUME-002",
    "EXEC-WORKER-003",
    "EXEC-VALIDATE-004",
    "EXEC-REVIEW-005",
    "EXEC-COMMIT-006",
    "EXEC-RECOVER-007",
    "EXEC-STOP-008",
    "CLOSE-FINAL-001",
    "CLOSE-RECONCILE-002",
    "CLOSE-NEXT-003",
    "STATE-DIAG-001",
    "STATE-TRANSITION-002",
    "STATE-CANONICAL-003",
    "STATE-HISTORY-004",
    "EVIDENCE-LEGACY-001",
    "EVIDENCE-DEAD-002",
    "EVIDENCE-TEST-003",
}
EXPECTED_FAMILIES = {
    "intake",
    "planning",
    "planning-fault-injection",
    "execution",
    "commit-receipt-fault-injection",
    "closeout",
    "closeout-fault-injection",
    "root-generation-isolation",
    "branch-design-lineage",
    "candidate-validation",
    "installer-cutover",
    "physical-deletion",
    "contract-first-format",
    "planning-state-ledger",
    "planning-quality",
    "execution-currentness",
    "cutover-lifecycle",
}
REQUIRED_SCENARIO_IDS = {
    "branch-lineage-ready",
    "candidate-child-generation-ready",
    "closeout-lost-batch-identity-blocked",
    "closeout-partial-write-resumes",
    "closeout-same-batch-no-successor",
    "commit-missing-receipt-blocked",
    "commit-unrelated-content-blocked",
    "contract-format-topology-independent",
    "cutover-atomic-switch-ready",
    "cutover-bridge-minimum-ready",
    "cutover-quiescence-blocked",
    "cutover-quiescence-ready",
    "cutover-rollback-ready",
    "cutover-switch-failure-preserves-stable",
    "execution-recovery-resumes-same-slice",
    "execution-review-blocks-commit",
    "execution-validated-reviewed-committed",
    "history-readable-nonauthoritative",
    "implementation-moved-blocked",
    "installer-clean-ready",
    "installer-partial-blocked",
    "installer-stale-link-blocked",
    "intake-duplicate-idempotent",
    "intake-fresh-atomic",
    "intake-multi-atomic",
    "intake-stale-blocked",
    "missing-receipt-blocked",
    "mixed-generation-result-blocked",
    "partial-reconciliation-blocked",
    "physical-synthetic-absence-ready",
    "planning-active-current",
    "planning-destructive-unapproved-blocked",
    "planning-existing-active-blocked",
    "planning-existing-queued-blocked",
    "planning-existing-selected-blocked",
    "planning-head-advanced-ready",
    "planning-invalid-blocked",
    "planning-partial-selection-resumes",
    "planning-queued-current",
    "planning-selected-current",
    "planning-semantic-multi-slice-queued",
    "planning-single-slice-queued",
    "planning-stale-state-blocked",
    "planning-vague-scope-blocked",
    "preparation-movement-blocked",
    "protected-handoff-ready",
    "quality-cohesive-single-slice",
    "quality-expansion-blocked",
    "quality-filler-split-blocked",
    "quality-independent-planner-reviewer",
    "quality-minimum-viable-scope",
    "quality-planner-reviewer-coupling-blocked",
    "quality-residual-complexity-approved",
    "quality-residual-complexity-unapproved",
    "quality-semantic-multi-slice",
    "quality-stale-draft-non-executable",
    "quality-undecided-draft-non-executable",
    "reused-worker-reviewer-lease-blocked",
    "root-canonical-write-blocked",
    "root-mixed-generation-blocked",
    "root-three-way-ready",
    "stale-receipt-revision-blocked",
    "stale-review-basis-blocked",
    "undeclared-planning-write-blocked",
    "unexpected-workspace-write-blocked",
    "unrelated-commit-content-blocked",
    "untracked-implementation-write-blocked",
    "wrong-generation-blocked",
    "wrong-root-write-blocked",
}
ACCEPTANCE_KEYS = {
    "source_characterization_green",
    "target_interfaces_green",
    "bootstrap_cutover_green",
    "fault_injection_green",
    "contract_coverage_complete",
    "legacy_topology_not_required",
}
ACCEPTANCE_ALIASES = {
    "source_characterization_green",
    "target_interface_scenarios_green",
    "bootstrap_and_cutover_scenarios_green",
    "fault_injection_scenarios_green",
    "contract_id_coverage_report_complete",
    "legacy_skill_names_not_required_except_migration_fixtures",
}


def _document(path: Path = FIXTURES / "catalog.yaml") -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_catalog(tmp_path: Path, document: Mapping[str, object]) -> Path:
    path = tmp_path / "catalog.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    test_root = tmp_path / "tests"
    test_root.mkdir(exist_ok=True)
    for name in (
        "test_command_owner_behavioral_scenarios.py",
        "test_command_owner_scenario_currentness.py",
        "test_command_owner_scenario_cutover.py",
    ):
        shutil.copy2(REPO_ROOT / "tests" / name, test_root / name)
    path.write_text(yaml.safe_dump(dict(document), sort_keys=False), encoding="utf-8")
    return path


def _codes(result: object) -> set[str]:
    return {item.code for item in result.diagnostics}  # type: ignore[attr-defined]


def _assert_objects_are_closed_world(node: object, path: str = "$") -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False, path
        for key, value in node.items():
            _assert_objects_are_closed_world(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _assert_objects_are_closed_world(value, f"{path}[{index}]")


def test_schema_is_draft_07_closed_world_and_exactly_versioned() -> None:
    schema = json.loads(
        (REPO_ROOT / "schemas/command-owner-scenario-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["properties"]["schema"]["const"] == "command-owner-scenario/v1"
    assert schema["definitions"]["testEvidence"]["required"] == ["node", "scenarios"]
    assert "source_sha256" not in schema["definitions"]["testEvidence"]["properties"]
    _assert_objects_are_closed_world(schema)


def test_catalog_preserves_accepted_contract_identity_and_families() -> None:
    result = validate_catalog(FIXTURES)

    assert result.is_valid
    assert result.catalog is not None
    document = result.catalog.document
    assert document["provenance"] == {
        "accepted_snapshot": "caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c",
        "source": "command-owner redesign accepted contract-to-scenario map",
    }
    assert set(document["required_contracts"]) == EXPECTED_CONTRACT_IDS
    assert set(document["required_families"]) == EXPECTED_FAMILIES
    assert all(
        set(test) == {"node", "scenarios"}
        for gate in document["aggregate_evidence"]["gates"]
        for test in gate["tests"]
    )


def test_every_declared_evidence_node_resolves_to_a_collectable_marked_test() -> None:
    nodes = {
        test["node"]
        for gate in _document()["aggregate_evidence"]["gates"]
        for test in gate["tests"]
    }
    for node in nodes:
        relative, separator, function_name = node.partition("::")
        module_name = relative.removesuffix(".py").replace("/", ".")
        function = getattr(importlib.import_module(module_name), function_name, None)
        marks = getattr(function, "pytestmark", ())
        assert separator and function_name.startswith("test_") and callable(function)
        assert "command_owner_evidence" in {mark.name for mark in marks}


@pytest.mark.command_owner_evidence
def test_live_catalog_reports_final_green_only_from_matching_observations() -> None:
    result = validate_catalog(FIXTURES)
    assert result.catalog is not None

    report = build_report(result.catalog)
    scenarios = report["scenarios"]
    families = report["families"]
    scenarios_by_id = {scenario["id"]: scenario for scenario in scenarios}
    assert REQUIRED_SCENARIO_IDS <= set(scenarios_by_id)
    required_scenarios = [
        scenarios_by_id[scenario_id] for scenario_id in REQUIRED_SCENARIO_IDS
    ]
    assert {scenario["family"] for scenario in required_scenarios} == EXPECTED_FAMILIES
    assert {
        contract
        for scenario in required_scenarios
        for contract in scenario["contracts"]
    } == EXPECTED_CONTRACT_IDS
    assert all(scenario["status"] == "green" for scenario in required_scenarios)
    observed_green_contracts = {
        contract
        for scenario in scenarios
        if scenario["status"] == "green"
        for contract in scenario["contracts"]
    }
    assert report["contracts"]["declared"] == sorted(EXPECTED_CONTRACT_IDS)  # type: ignore[index]
    assert report["contracts"]["green"] == sorted(observed_green_contracts)  # type: ignore[index]
    assert observed_green_contracts == EXPECTED_CONTRACT_IDS
    assert all(scenario["status"] == "green" for scenario in scenarios)
    assert all(scenario["adapter"] is not None for scenario in scenarios)
    assert all(family["status"] == "green" for family in families)
    assert report["status_counts"] == {
        "declared": 0,
        "bound": 0,
        "green": len(scenarios),
        "blocked": 0,
        "unavailable": 0,
    }
    assert report["acceptance"]["all_required_contracts_declared"] is True  # type: ignore[index]
    assert report["acceptance"]["only_bound_green_observations_count"] is True  # type: ignore[index]
    assert report["acceptance"]["all_required_contracts_green"] is True  # type: ignore[index]
    assert report["acceptance"]["all_required_families_green"] is True  # type: ignore[index]


def test_unobserved_report_has_exactly_six_false_keys_and_aliases() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.catalog is not None
    aggregate = scenario_harness._build_unobserved_report(validation.catalog)[
        "aggregate_evidence"
    ]
    assert aggregate["keys"] == {key: False for key in ACCEPTANCE_KEYS}
    assert aggregate["aliases"] == {alias: False for alias in ACCEPTANCE_ALIASES}
    assert set(aggregate["test_outcomes"].values()) == {"not-observed"}
    with pytest.raises(TypeError):
        build_report(
            validation.catalog,
            observed_test_outcomes={"caller-controlled": "passed"},  # type: ignore[call-arg]
        )


def test_runtime_report_distinguishes_every_evidence_status() -> None:
    result = validate_catalog(VALID_RUNTIME)
    assert result.catalog is not None

    report = build_report(result.catalog)
    scenarios = {item["id"]: item for item in report["scenarios"]}  # type: ignore[assignment]

    assert report["status_counts"] == {
        "declared": 1,
        "bound": 1,
        "green": 1,
        "blocked": 2,
        "unavailable": 1,
    }
    assert scenarios["green-scenario"]["status"] == "green"
    assert scenarios["bound-scenario"]["status"] == "bound"
    assert scenarios["mismatch-scenario"]["status"] == "blocked"
    assert scenarios["mismatch-scenario"]["mismatches"] == [
        {
            "field": "writes",
            "expected": ["results/evidence.json"],
            "actual": ["results/wrong.json"],
        }
    ]


def test_acceptance_writes_same_process_reports_without_an_ingestion_api(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.catalog is not None
    catalog = validation.catalog
    aggregate = catalog.document["aggregate_evidence"]
    nodes = scenario_harness._aggregate_test_nodes(aggregate)
    report: dict[str, Any] = {
        "schema": "command-owner-scenario-v1",
        "status_counts": dict.fromkeys(
            ("declared", "bound", "blocked", "unavailable"), 0
        )
        | {"green": 1},
        "contracts": {"required": [], "declared": [], "green": []},
        "families": [{"id": "test", "status": "green"}],
        "aggregate_evidence": {
            "keys": {"complete": True},
            "aliases": {"complete": True},
            "test_outcomes": {node: "passed" for node in nodes},
        },
        "acceptance": {"complete": True},
    }
    outcome = {
        **dict.fromkeys(
            ("failures", "errors", "skipped", "deselected", "xfailed", "xpassed"),
            0,
        ),
        "returncode": 0,
        "tests": len(nodes),
    }
    monkeypatch.setattr(
        scenario_harness, "_require_clean_candidate_commit", lambda _root: "0" * 40
    )
    monkeypatch.setattr(
        scenario_harness,
        "_input_identity",
        lambda _catalog: {"files": {}, "sha256": "inputs"},
    )
    monkeypatch.setattr(
        scenario_harness,
        "_candidate_interpreter_identity",
        lambda _root: {"executable": "python", "prefix": "venv", "safe_path": True},
    )
    monkeypatch.setattr(
        scenario_harness,
        "_execute_aggregate_test_evidence",
        lambda _catalog: scenario_harness._EvidenceExecution(
            {node: "passed" for node in nodes}, outcome, 1.0, 1
        ),
    )
    monkeypatch.setattr(
        scenario_harness, "_build_report", lambda *_args, **_kwargs: report
    )
    monkeypatch.setattr(
        scenario_harness.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("formatting launched a subprocess"),
    )
    result_path, json_path, text_path = (
        tmp_path / "result.json",
        tmp_path / "report.json",
        tmp_path / "report.txt",
    )

    result = scenario_harness._write_acceptance_outputs(
        catalog, result_path, json_path, text_path
    )

    written_report = json.loads(json_path.read_text())
    assert json.loads(result_path.read_text()) == result
    assert written_report == report
    assert result["report_sha256"] == scenario_harness._sha256_json(written_report)
    assert text_path.read_text() == scenario_harness._render_text_report(written_report)
    with pytest.raises(SystemExit):
        scenario_harness._build_parser().parse_args(
            ["report", str(FIXTURES), "--result", str(result_path)]
        )


def test_mutating_adapter_cannot_change_canonical_expectation_or_turn_green(
    tmp_path: Path,
) -> None:
    document = _document(VALID_RUNTIME / "catalog.yaml")
    document["scenarios"] = [copy.deepcopy(document["scenarios"][2])]
    scenario = document["scenarios"][0]
    scenario["binding"]["adapter"] = "adapters.py:mutating_observation"
    catalog_path = _write_catalog(tmp_path, document)
    (tmp_path / "adapters.py").write_text(
        "def mutating_observation(scenario, _fixture_root):\n"
        "    try:\n"
        "        scenario['expected_writes'].append('results/tampered.json')\n"
        "    except (AttributeError, TypeError):\n"
        "        pass\n"
        "    return {\n"
        "        'transition': 'observed',\n"
        "        'writes': ['results/evidence.json', 'results/tampered.json'],\n"
        "        'forbidden_writes': ['outside/forbidden.txt'],\n"
        "        'stop_reason': None,\n"
        "        'generation_and_roots': {\n"
        "            'generation': 'candidate',\n"
        "            'roots': [{'role': 'fixture', 'path': 'roots/fixture'}],\n"
        "        },\n"
        "        'validation': ['focused.green'],\n"
        "    }\n",
        encoding="utf-8",
    )
    result = validate_catalog(catalog_path)
    assert result.catalog is not None

    report = build_report(result.catalog)
    reported_scenario = report["scenarios"][0]  # type: ignore[index]
    canonical_scenario = result.catalog.document["scenarios"][0]  # type: ignore[index]

    assert reported_scenario["status"] == "blocked"
    assert reported_scenario["mismatches"] == [
        {
            "field": "writes",
            "expected": ["results/evidence.json"],
            "actual": ["results/evidence.json", "results/tampered.json"],
        }
    ]
    assert report["acceptance"]["all_required_contracts_green"] is False  # type: ignore[index]
    assert canonical_scenario["expected_writes"] == ["results/evidence.json"]


def test_observation_comparison_is_exact_pure_and_does_not_normalize_order() -> None:
    scenario = _document(VALID_RUNTIME / "catalog.yaml")["scenarios"][2]
    observation = {
        "transition": "observed",
        "writes": ["results/evidence.json"],
        "forbidden_writes": ["outside/forbidden.txt"],
        "stop_reason": None,
        "generation_and_roots": {
            "generation": "candidate",
            "roots": [{"role": "fixture", "path": "roots/fixture"}],
        },
        "validation": ["focused.green"],
    }
    original_scenario = copy.deepcopy(scenario)

    assert compare_observation(scenario, observation) == ()
    observation["validation"] = ["focused.extra", "focused.green"]
    modified_observation = copy.deepcopy(observation)
    mismatches = compare_observation(scenario, observation)

    assert [item.field for item in mismatches] == ["validation"]
    assert scenario == original_scenario
    assert observation == modified_observation


def test_cli_validate_and_json_report_are_deterministic(tmp_path: Path) -> None:
    prefix = [sys.executable, "scripts/command_owner_scenarios.py"]
    json_command = [*prefix, "report", str(FIXTURES), "--format", "json"]
    text_command = [*prefix, "report", str(FIXTURES)]
    validate_command = [*prefix, "validate", str(FIXTURES)]

    def run(
        command: list[str], *, check: bool = False
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=check,
            capture_output=True,
            text=True,
        )

    json_reports = [run(json_command, check=True).stdout for _ in range(2)]
    text_reports = [run(text_command, check=True).stdout for _ in range(2)]
    validate = run(validate_command, check=True)
    invalid_document = _document()
    invalid_document["scenarios"].append(
        copy.deepcopy(invalid_document["scenarios"][0])
    )
    invalid_catalog = _write_catalog(tmp_path, invalid_document)
    invalid = [
        run([*prefix, subcommand, str(invalid_catalog)])
        for subcommand in ("validate", "report")
    ]

    assert json_reports[0] == json_reports[1]
    assert json.loads(json_reports[0])["catalog_valid"] is True
    assert text_reports[0] == text_reports[1]
    assert text_reports[0].startswith("schema: command-owner-scenario/v1\n")
    assert validate.stdout.startswith("valid:")
    assert {process.returncode for process in invalid} == {1}
    assert {process.stdout for process in invalid} == {""}
    assert len({process.stderr for process in invalid}) == 1
    assert "catalog.duplicate_scenario_id" in invalid[0].stderr


def test_unknown_contract_and_family_are_rejected(tmp_path: Path) -> None:
    document = _document()
    document["scenarios"][0]["contracts"].append("UNKNOWN-001")
    document["scenarios"][0]["family"] = "unknown-family"

    result = validate_catalog(_write_catalog(tmp_path, document))

    assert _codes(result) == {
        "catalog.unknown_contract",
        "catalog.unknown_family",
        "catalog.uncovered_family",
    }


def test_unsafe_paths_and_shell_like_command_labels_are_rejected(
    tmp_path: Path,
) -> None:
    document = _document()
    document["scenarios"][0]["expected_writes"] = ["../outside"]
    document["scenarios"][0]["command"] = "echo arbitrary-command"

    result = validate_catalog(_write_catalog(tmp_path, document))

    assert _codes(result) == {"schema.pattern"}


def test_target_assertions_cannot_name_catalog_forbidden_topology(
    tmp_path: Path,
) -> None:
    for index, spelling in enumerate(
        ("batch-runway", "Batch Runway", "batch_runway", "batch.runway")
    ):
        document = _document()
        target = document["scenarios"][2]
        assert target["evidence_kind"] == "fault_injection"
        target["expected_transition"] = f"{spelling} topology is present"

        result = validate_catalog(_write_catalog(tmp_path / str(index), document))

        assert _codes(result) == {"catalog.forbidden_target_topology"}


def test_missing_unknown_and_unsupported_content_fail_closed(tmp_path: Path) -> None:
    missing = _document()
    del missing["scenarios"][0]["expected_transition"]
    unknown = _document()
    unknown["scenarios"][0]["unknown_v1_field"] = True
    unsupported = _document()
    unsupported["schema"] = "command-owner-scenario/v2"

    missing_result = validate_catalog(_write_catalog(tmp_path / "missing", missing))
    unknown_result = validate_catalog(_write_catalog(tmp_path / "unknown", unknown))
    unsupported_result = validate_catalog(
        _write_catalog(tmp_path / "unsupported", unsupported)
    )

    assert _codes(missing_result) == {"schema.required"}
    assert _codes(unknown_result) == {"schema.additionalProperties"}
    assert _codes(unsupported_result) == {"schema.const"}


def test_duplicate_yaml_keys_and_malformed_observations_fail_closed(
    tmp_path: Path,
) -> None:
    duplicate_path = tmp_path / "duplicate.yaml"
    duplicate_path.write_text(
        "schema: command-owner-scenario/v1\nschema: command-owner-scenario/v1\n",
        encoding="utf-8",
    )
    scenario = _document(VALID_RUNTIME / "catalog.yaml")["scenarios"][2]

    duplicate_result = validate_catalog(duplicate_path)

    assert _codes(duplicate_result) == {"catalog.invalid_yaml"}
    try:
        compare_observation(scenario, {"transition": "observed"})
    except ValueError as error:
        assert "observation fields must be exact" in str(error)
    else:
        raise AssertionError("malformed observation was accepted")
