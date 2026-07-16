from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from scripts.command_owner_scenarios import (
    build_report,
    compare_observation,
    render_json_report,
    render_text_report,
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


def test_schema_is_closed_world_and_source_hash_is_not_acceptance_authority() -> None:
    schema = json.loads(
        (REPO_ROOT / "schemas/command-owner-scenario-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["properties"]["schema"]["const"] == "command-owner-scenario/v1"
    _assert_objects_are_closed_world(schema)
    evidence = schema["definitions"]["testEvidence"]
    assert evidence["required"] == ["node", "scenarios"]
    assert "Deprecated non-authoritative" in evidence["properties"]["source_sha256"][
        "description"
    ]


def test_catalog_preserves_exact_contract_identity_and_families() -> None:
    result = validate_catalog(FIXTURES)

    assert result.is_valid, result.diagnostics
    assert result.catalog is not None
    document = result.catalog.document
    assert document["provenance"] == {
        "accepted_snapshot": "caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c",
        "source": "command-owner redesign accepted contract-to-scenario map",
    }
    assert set(document["required_contracts"]) == EXPECTED_CONTRACT_IDS
    assert len(document["required_contracts"]) == 31
    assert set(document["required_families"]) == EXPECTED_FAMILIES


def test_live_catalog_report_is_green_but_cannot_self_certify_aggregate() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.catalog is not None

    report = build_report(validation.catalog)
    scenarios = report["scenarios"]
    families = report["families"]
    aggregate = report["aggregate_evidence"]
    observed_green_contracts = {
        contract
        for scenario in scenarios
        if scenario["status"] == "green"
        for contract in scenario["contracts"]
    }

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
    assert report["acceptance"] == {
        "all_required_contracts_declared": True,
        "all_required_contracts_green": True,
        "all_required_families_green": True,
        "only_bound_green_observations_count": True,
    }
    assert set(aggregate["keys"].values()) == {False}
    assert set(aggregate["aliases"].values()) == {False}
    assert set(aggregate["test_outcomes"].values()) == {"not-observed"}
    assert all(
        "source_sha256" not in test
        for evidence in aggregate["evidence"].values()
        for test in evidence["tests"]
    )


def test_runtime_report_distinguishes_every_evidence_status() -> None:
    result = validate_catalog(VALID_RUNTIME)
    assert result.catalog is not None

    report = build_report(result.catalog)
    scenarios = {item["id"]: item for item in report["scenarios"]}

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


def test_mutating_adapter_cannot_change_expectation_or_turn_green(tmp_path: Path) -> None:
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
    observed = report["scenarios"][0]
    canonical = result.catalog.document["scenarios"][0]

    assert observed["status"] == "blocked"
    assert observed["mismatches"][0]["field"] == "writes"
    assert report["acceptance"]["all_required_contracts_green"] is False
    assert canonical["expected_writes"] == ["results/evidence.json"]


def test_observation_comparison_is_exact_pure_and_order_sensitive() -> None:
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


def test_report_rendering_is_pure_and_cli_validation_is_deterministic(
    tmp_path: Path,
) -> None:
    result = validate_catalog(VALID_RUNTIME)
    assert result.catalog is not None
    report = build_report(result.catalog)

    first_json = render_json_report(report)
    second_json = render_json_report(report)
    first_text = render_text_report(report)
    second_text = render_text_report(report)

    assert first_json == second_json
    assert json.loads(first_json)["catalog_valid"] is True
    assert first_text == second_text
    assert first_text.startswith("schema: command-owner-scenario/v1\n")

    invalid = _document()
    invalid["scenarios"].append(copy.deepcopy(invalid["scenarios"][0]))
    invalid_catalog = _write_catalog(tmp_path, invalid)
    validate_command = [
        sys.executable,
        "scripts/command_owner_scenarios.py",
        "validate",
    ]
    valid = subprocess.run(
        [*validate_command, str(FIXTURES)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    invalid_first = subprocess.run(
        [*validate_command, str(invalid_catalog)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    invalid_second = subprocess.run(
        [*validate_command, str(invalid_catalog)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert valid.returncode == 0
    assert valid.stdout.startswith("valid:")
    assert invalid_first.returncode == invalid_second.returncode == 1
    assert invalid_first.stdout == invalid_second.stdout == ""
    assert invalid_first.stderr == invalid_second.stderr
    assert "catalog.duplicate_scenario_id" in invalid_first.stderr


def test_duplicate_scenario_ids_fail_deterministically(tmp_path: Path) -> None:
    document = _document()
    document["scenarios"].append(copy.deepcopy(document["scenarios"][0]))

    result = validate_catalog(_write_catalog(tmp_path, document))

    assert _codes(result) == {"catalog.duplicate_scenario_id"}
    assert "also appears at index 0" in result.diagnostics[0].message


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


def test_uncovered_required_family_is_rejected(tmp_path: Path) -> None:
    document = _document()
    document["required_families"].append("missing-family")

    result = validate_catalog(_write_catalog(tmp_path, document))

    assert _codes(result) == {"catalog.uncovered_family"}


def test_unsafe_paths_and_shell_like_command_labels_are_rejected(
    tmp_path: Path,
) -> None:
    document = _document()
    document["scenarios"][0]["expected_writes"] = ["../outside"]
    document["scenarios"][0]["command"] = "echo arbitrary-command"

    result = validate_catalog(_write_catalog(tmp_path, document))

    assert _codes(result) == {"schema.pattern"}


def test_target_assertions_cannot_name_forbidden_topology(tmp_path: Path) -> None:
    for index, spelling in enumerate(
        ("batch-runway", "Batch Runway", "batch_runway", "batch.runway")
    ):
        document = _document()
        target = document["scenarios"][2]
        assert target["evidence_kind"] == "fault_injection"
        target["expected_transition"] = f"{spelling} topology is present"

        result = validate_catalog(_write_catalog(tmp_path / str(index), document))

        assert _codes(result) == {"catalog.forbidden_target_topology"}

    near_miss = _document()
    near_miss["scenarios"][2]["expected_transition"] = (
        "batch-runwayish topology is present"
    )
    assert validate_catalog(_write_catalog(tmp_path / "near-miss", near_miss)).is_valid


def test_missing_unknown_and_unsupported_content_fail_closed(tmp_path: Path) -> None:
    missing = _document()
    del missing["scenarios"][0]["expected_transition"]
    unknown = _document()
    unknown["scenarios"][0]["unknown_v1_field"] = True
    unsupported = _document()
    unsupported["schema"] = "command-owner-scenario/v2"

    assert _codes(validate_catalog(_write_catalog(tmp_path / "missing", missing))) == {
        "schema.required"
    }
    assert _codes(validate_catalog(_write_catalog(tmp_path / "unknown", unknown))) == {
        "schema.additionalProperties"
    }
    assert _codes(
        validate_catalog(_write_catalog(tmp_path / "unsupported", unsupported))
    ) == {"schema.const"}


def test_duplicate_yaml_keys_and_malformed_observations_fail_closed(
    tmp_path: Path,
) -> None:
    duplicate_path = tmp_path / "duplicate.yaml"
    duplicate_path.write_text(
        "schema: command-owner-scenario/v1\nschema: command-owner-scenario/v1\n",
        encoding="utf-8",
    )
    scenario = _document(VALID_RUNTIME / "catalog.yaml")["scenarios"][2]

    assert _codes(validate_catalog(duplicate_path)) == {"catalog.invalid_yaml"}
    try:
        compare_observation(scenario, {"transition": "observed"})
    except ValueError as error:
        assert "observation fields must be exact" in str(error)
    else:
        raise AssertionError("malformed observation was accepted")
