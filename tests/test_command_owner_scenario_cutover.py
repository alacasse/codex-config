from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import venv
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType
from types import MappingProxyType
from typing import Any

import pytest
import yaml

from scripts.command_owner_scenarios import (
    Catalog,
    build_report,
    evaluate_catalog,
    validate_catalog,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/command-owner-scenarios"
CUTOVER_SCENARIOS = {
    "root-three-way-ready",
    "root-canonical-write-blocked",
    "root-mixed-generation-blocked",
    "branch-lineage-ready",
    "candidate-child-generation-ready",
    "installer-clean-ready",
    "installer-partial-blocked",
    "installer-stale-link-blocked",
    "cutover-atomic-switch-ready",
    "cutover-switch-failure-preserves-stable",
    "cutover-rollback-ready",
    "cutover-quiescence-blocked",
    "cutover-quiescence-ready",
    "cutover-bridge-minimum-ready",
    "physical-synthetic-absence-ready",
    "history-readable-nonauthoritative",
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


def _document(root: Path = FIXTURES) -> dict[str, Any]:
    loaded = yaml.safe_load((root / "catalog.yaml").read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_document(root: Path, document: Mapping[str, object]) -> None:
    (root / "catalog.yaml").write_text(
        yaml.safe_dump(dict(document), sort_keys=False), encoding="utf-8"
    )


def _scenario(scenario_id: str) -> Mapping[str, object]:
    return next(
        scenario
        for scenario in _document()["scenarios"]
        if scenario["id"] == scenario_id
    )


def _adapter_module() -> ModuleType:
    path = FIXTURES / "cutover_adapters.py"
    name = f"_cutover_scenario_adapters_{id(path)}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _evidence(workspace: Path, scenario_id: str) -> Mapping[str, object]:
    loaded = json.loads(
        (workspace / "evidence" / f"{scenario_id}.json").read_text(encoding="utf-8")
    )
    assert isinstance(loaded, dict)
    return loaded


def _copy_fixtures(tmp_path: Path) -> Path:
    target = tmp_path / "fixtures"
    shutil.copytree(FIXTURES, target)
    test_root = tmp_path / "tests"
    test_root.mkdir()
    for name in (
        "test_command_owner_behavioral_scenarios.py",
        "test_command_owner_scenario_currentness.py",
        "test_command_owner_scenario_cutover.py",
    ):
        shutil.copy2(REPO_ROOT / "tests" / name, test_root / name)
    return target


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


def _acceptance_document() -> dict[str, object]:
    return {
        "schema": "command-owner-scenario/v1",
        "provenance": {
            "accepted_snapshot": "0" * 40,
            "source": "acceptance runtime fixture",
        },
        "required_contracts": ["TEST-001"],
        "required_families": ["status-model"],
        "forbidden_target_terms": ["legacy-owner"],
        "aggregate_evidence": {
            "gates": [
                {
                    "key": "source_green",
                    "aliases": ["source_alias"],
                    "scenarios": ["green-scenario"],
                    "tests": [
                        {
                            "node": "tests/test_evidence.py::test_evidence",
                            "scenarios": ["green-scenario"],
                        }
                    ],
                }
            ]
        },
        "scenarios": [
            {
                "id": "green-scenario",
                "family": "status-model",
                "evidence_kind": "coverage",
                "contracts": ["TEST-001"],
                "initial_artifacts": [],
                "command": "status.green",
                "expected_transition": "observed",
                "expected_writes": ["results/evidence.json"],
                "forbidden_writes": ["outside/forbidden.txt"],
                "expected_stop_reason": None,
                "generation_and_roots": {
                    "generation": "candidate",
                    "roots": [{"role": "fixture", "path": "roots/fixture"}],
                },
                "validation": ["focused.green"],
                "binding": {
                    "status": "bound",
                    "adapter": "adapters.py:observe",
                    "reason": None,
                },
            }
        ],
    }


def _temporary_harness(
    tmp_path: Path,
    *,
    evidence_source: str = "def test_evidence():\n    assert True\n",
    conftest_source: str | None = None,
) -> tuple[ModuleType, Any, Path]:
    project = tmp_path / "candidate"
    venv.EnvBuilder(system_site_packages=True, with_pip=False).create(project / ".venv")
    (project / "scripts").mkdir(parents=True)
    (project / "schemas").mkdir()
    test_root = project / "tests"
    test_root.mkdir()
    fixture_root = test_root / "fixtures/command-owner-scenarios"
    fixture_root.mkdir(parents=True)
    shutil.copy2(
        REPO_ROOT / "scripts/command_owner_scenarios.py",
        project / "scripts/command_owner_scenarios.py",
    )
    shutil.copy2(
        REPO_ROOT / "schemas/command-owner-scenario-v1.schema.json",
        project / "schemas/command-owner-scenario-v1.schema.json",
    )
    (fixture_root / "adapters.py").write_text(
        "def observe(scenario, _root):\n"
        "    return {\n"
        "        'transition': scenario['expected_transition'],\n"
        "        'writes': list(scenario['expected_writes']),\n"
        "        'forbidden_writes': list(scenario['forbidden_writes']),\n"
        "        'stop_reason': scenario['expected_stop_reason'],\n"
        "        'generation_and_roots': {\n"
        "            'generation': scenario['generation_and_roots']['generation'],\n"
        "            'roots': [dict(item) for item in "
        "scenario['generation_and_roots']['roots']],\n"
        "        },\n"
        "        'validation': list(scenario['validation']),\n"
        "    }\n",
        encoding="utf-8",
    )
    _write_document(fixture_root, _acceptance_document())
    (test_root / "test_evidence.py").write_text(evidence_source, encoding="utf-8")
    if conftest_source is not None:
        (project / "conftest.py").write_text(conftest_source, encoding="utf-8")
    (project / ".gitignore").write_text(
        ".venv/\n__pycache__/\n.pytest_cache/\n", encoding="utf-8"
    )
    _git(project, "init", "--quiet")
    _git(project, "config", "user.name", "Fixture")
    _git(project, "config", "user.email", "fixture@example.invalid")
    _git(project, "add", ".")
    _git(project, "commit", "--quiet", "-m", "Initialize fixture")

    harness_path = project / "scripts/command_owner_scenarios.py"
    name = f"_temporary_command_owner_scenarios_{tmp_path.name}"
    spec = importlib.util.spec_from_file_location(name, harness_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    validation = module.validate_catalog(fixture_root)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None
    return module, validation.catalog, project


@pytest.mark.parametrize("scenario_id", sorted(CUTOVER_SCENARIOS))
def test_every_cutover_scenario_matches_observed_disposable_effects(
    tmp_path: Path,
    scenario_id: str,
) -> None:
    adapter = _adapter_module()
    workspace = tmp_path / "workspace"
    scenario = _scenario(scenario_id)

    observation = adapter.run_scenario(scenario, FIXTURES, workspace)

    assert observation == {
        "transition": scenario["expected_transition"],
        "writes": scenario["expected_writes"],
        "forbidden_writes": scenario["forbidden_writes"],
        "stop_reason": scenario["expected_stop_reason"],
        "generation_and_roots": scenario["generation_and_roots"],
        "validation": scenario["validation"],
    }
    assert (workspace / "evidence" / f"{scenario_id}.json").is_file()
    assert all(path.is_relative_to(tmp_path) for path in workspace.rglob("*"))


def test_root_and_generation_faults_fail_closed_without_canonical_write(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()
    ids = (
        "root-three-way-ready",
        "root-canonical-write-blocked",
        "root-mixed-generation-blocked",
    )
    evidence: dict[str, Mapping[str, object]] = {}
    for scenario_id in ids:
        workspace = tmp_path / scenario_id
        adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)
        evidence[scenario_id] = _evidence(workspace, scenario_id)

    assert all(len(set(item["roots"].values())) == 3 for item in evidence.values())
    assert all(item["canonical_write_occurred"] is False for item in evidence.values())
    assert all(item["outside_destination_rejected"] is True for item in evidence.values())
    assert evidence["root-three-way-ready"]["status"] == "ready"
    assert evidence["root-canonical-write-blocked"]["status"] == "blocked"
    assert (
        evidence["root-mixed-generation-blocked"]["worker_generation"]
        == "fixture-candidate-child"
    )


def test_lineage_and_child_generation_use_observed_repository_and_process_facts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = _adapter_module()
    lineage_workspace = tmp_path / "lineage"
    child_workspace = tmp_path / "child"

    monkeypatch.setenv("PYTHONPATH", "/tmp/foreign-checkout")
    adapter.run_scenario(
        _scenario("branch-lineage-ready"), FIXTURES, lineage_workspace
    )
    adapter.run_scenario(
        _scenario("candidate-child-generation-ready"), FIXTURES, child_workspace
    )
    lineage = _evidence(lineage_workspace, "branch-lineage-ready")
    child = _evidence(child_workspace, "candidate-child-generation-ready")

    assert lineage["base_is_ancestor"] is True
    assert lineage["accepted_design_is_ancestor"] is True
    assert len(str(lineage["candidate_head"])) == 40
    assert child["exit_code"] == 0
    assert child["resolved_generation"] == "fixture-candidate-child"
    assert Path(str(child["explicit_home"])).is_relative_to(tmp_path)
    assert child["sanitized_pythonpath"] == str(REPO_ROOT)


def test_install_switch_rollback_and_quiescence_are_disposable_and_atomic(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()
    ids = (
        "installer-clean-ready",
        "installer-partial-blocked",
        "installer-stale-link-blocked",
        "cutover-atomic-switch-ready",
        "cutover-switch-failure-preserves-stable",
        "cutover-rollback-ready",
        "cutover-quiescence-blocked",
        "cutover-quiescence-ready",
    )
    evidence: dict[str, Mapping[str, object]] = {}
    for scenario_id in ids:
        workspace = tmp_path / scenario_id
        adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)
        evidence[scenario_id] = _evidence(workspace, scenario_id)

    assert evidence["installer-clean-ready"]["published"] is True
    assert evidence["installer-partial-blocked"]["published"] is False
    assert evidence["installer-stale-link-blocked"]["published"] is False
    assert evidence["cutover-atomic-switch-ready"]["after"] == "candidate"
    assert evidence["cutover-atomic-switch-ready"]["missing_route_observations"] == 0
    assert evidence["cutover-switch-failure-preserves-stable"]["after"] == "stable"
    assert evidence["cutover-rollback-ready"]["restored"] == "stable"
    assert evidence["cutover-quiescence-blocked"]["ready"] is False
    assert evidence["cutover-quiescence-ready"]["ready"] is True


def test_bridge_absence_is_synthetic_and_history_never_becomes_pickup_authority(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()
    ids = (
        "cutover-bridge-minimum-ready",
        "physical-synthetic-absence-ready",
        "history-readable-nonauthoritative",
    )
    evidence: dict[str, Mapping[str, object]] = {}
    for scenario_id in ids:
        workspace = tmp_path / scenario_id
        adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)
        evidence[scenario_id] = _evidence(workspace, scenario_id)

    bridge = evidence["cutover-bridge-minimum-ready"]
    assert bridge["planning_authority"] == "master"
    assert bridge["scope"] == "root-generation-and-receipt-only"
    absence = evidence["physical-synthetic-absence-ready"]
    assert absence["synthetic_fixture"] is True
    assert absence["real_deletion_claimed"] is False
    assert absence["bridge_present"] is False
    history = evidence["history-readable-nonauthoritative"]
    assert history["authority"] == "planning-state-current"
    assert history["archive_readable"] is True
    assert history["pickup"].endswith("/live-batch/dispatch.md")


def test_contract_coverage_evidence_is_exact_and_green() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    evaluations = evaluate_catalog(validation.catalog)
    required = set(validation.catalog.document["required_contracts"])
    green = {
        contract
        for evaluation in evaluations
        if evaluation.status == "green"
        for contract in evaluation.contracts
    }

    assert len(required) == 31
    assert green == required


def test_aggregate_mapping_is_exact_but_function_source_hashes_are_not_authority() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    report = build_report(validation.catalog)
    aggregate = report["aggregate_evidence"]
    gates = _document()["aggregate_evidence"]["gates"]

    assert set(aggregate["keys"]) == ACCEPTANCE_KEYS
    assert set(aggregate["aliases"]) == ACCEPTANCE_ALIASES
    assert set(aggregate["keys"].values()) == {False}
    assert set(aggregate["test_outcomes"].values()) == {"not-observed"}
    assert all(
        set(test) == {"node", "scenarios"}
        for evidence in aggregate["evidence"].values()
        for test in evidence["tests"]
    )
    assert any("source_sha256" in test for gate in gates for test in gate["tests"])


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    (
        ("missing-scenarios", "schema.minItems"),
        ("duplicate-scenario", "schema.uniqueItems"),
        ("duplicate-key", "catalog.duplicate_evidence_key"),
        ("duplicate-alias", "catalog.duplicate_evidence_alias"),
        ("unknown-scenario", "catalog.unknown_evidence_scenario"),
        ("unrelated-green-substitution", "catalog.missing_test_evidence_coverage"),
        ("nonexistent-test-node", "catalog.missing_test_evidence_node"),
        ("missing-test-scenarios", "schema.minItems"),
    ),
)
def test_aggregate_evidence_rejects_invalid_mappings(
    tmp_path: Path,
    mutation: str,
    expected_code: str,
) -> None:
    root = _copy_fixtures(tmp_path)
    document = _document(root)
    gates = document["aggregate_evidence"]["gates"]
    if mutation == "missing-scenarios":
        gates[0]["scenarios"] = []
    elif mutation == "duplicate-scenario":
        gates[0]["scenarios"].append(gates[0]["scenarios"][0])
    elif mutation == "duplicate-key":
        gates[1]["key"] = gates[0]["key"]
    elif mutation == "duplicate-alias":
        gates[1]["aliases"] = list(gates[0]["aliases"])
    elif mutation == "unknown-scenario":
        gates[0]["scenarios"] = ["unknown-scenario"]
    elif mutation == "unrelated-green-substitution":
        gates[0]["scenarios"][0] = "quality-cohesive-single-slice"
    elif mutation == "nonexistent-test-node":
        gates[0]["tests"][0]["node"] = "tests/does-not-exist.py::test_missing"
    else:
        gates[0]["tests"][0]["scenarios"] = []
    _write_document(root, document)

    validation = validate_catalog(root)

    assert not validation.is_valid
    assert expected_code in {item.code for item in validation.diagnostics}


def test_aggregate_evidence_rejects_a_declared_but_non_green_scenario() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None
    document = copy.deepcopy(dict(validation.catalog.document))
    scenario = next(
        item
        for item in document["scenarios"]
        if item["id"] == "physical-synthetic-absence-ready"
    )
    scenario["binding"] = {
        "status": "unavailable",
        "adapter": None,
        "reason": "negative aggregate evidence fixture",
    }
    catalog = Catalog(
        path=FIXTURES / "catalog.yaml",
        root=FIXTURES,
        document=MappingProxyType(document),
    )

    with pytest.raises(ValueError, match="references non-green scenario"):
        build_report(catalog)


@pytest.mark.parametrize(
    "mode",
    (
        "runtime-skip",
        "runtime-xfail",
        "runtime-xpass",
        "collection-hook",
        "deselected",
        "module-disabled",
        "assertion-failure",
        "setup-error",
    ),
)
def test_acceptance_rejects_every_non_exclusive_pass(
    tmp_path: Path,
    mode: str,
) -> None:
    statement = {
        "runtime-skip": "pytest.skip('runtime skip')",
        "runtime-xfail": "pytest.xfail('runtime xfail')",
        "runtime-xpass": "assert True",
        "collection-hook": "assert True",
        "deselected": "assert True",
        "module-disabled": "assert True",
        "assertion-failure": "assert False",
        "setup-error": "assert True",
    }[mode]
    parameters = "missing_fixture" if mode == "setup-error" else ""
    module_control = "__test__ = False\n" if mode == "module-disabled" else ""
    source = (
        "import pytest\n\n"
        + module_control
        + f"def test_evidence({parameters}):\n"
        + f"    {statement}\n"
    )
    conftest = None
    if mode in {"collection-hook", "runtime-xpass", "deselected"}:
        hook = {
            "collection-hook": (
                "    for item in items:\n"
                "        item.add_marker(pytest.mark.skip(reason='collection skip'))\n"
            ),
            "runtime-xpass": (
                "    for item in items:\n"
                "        item.add_marker(pytest.mark.xfail(reason='xpass', strict=False))\n"
            ),
            "deselected": (
                "    removed = list(items)\n"
                "    items[:] = []\n"
                "    if removed:\n"
                "        removed[0].config.hook.pytest_deselected(items=removed)\n"
            ),
        }[mode]
        conftest = "import pytest\n\ndef pytest_collection_modifyitems(items):\n" + hook
    harness, catalog, project = _temporary_harness(
        tmp_path,
        evidence_source=source,
        conftest_source=conftest,
    )

    with pytest.raises(RuntimeError, match="did not pass exclusively"):
        harness.run_acceptance(catalog, tmp_path / "receipt.json")
    assert _git(project, "status", "--porcelain", "--untracked-files=all") == ""


def test_acceptance_uses_sanitized_candidate_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_literal = repr(str(tmp_path / "candidate"))
    source = (
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        "def test_evidence():\n"
        f"    assert Path.cwd() == Path({project_literal})\n"
        "    assert sys.flags.safe_path\n"
        "    assert os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] == '1'\n"
        "    assert 'PYTHONHOME' not in os.environ\n"
        "    assert 'PYTHONPATH' not in os.environ\n"
        "    assert 'PYTEST_ADDOPTS' not in os.environ\n"
        "    assert 'PYTEST_PLUGINS' not in os.environ\n"
    )
    harness, catalog, _project = _temporary_harness(tmp_path, evidence_source=source)
    monkeypatch.setenv("PYTHONHOME", "/tmp/foreign-python-home")
    monkeypatch.setenv("PYTHONPATH", "/tmp/foreign-python-path")
    monkeypatch.setenv("PYTEST_ADDOPTS", "--deselect=tests/test_evidence.py")
    monkeypatch.setenv("PYTEST_PLUGINS", "foreign_plugin")

    receipt = harness.run_acceptance(catalog, tmp_path / "receipt.json")

    assert receipt["node_outcomes"] == {
        "tests/test_evidence.py::test_evidence": "passed"
    }
    assert receipt["safe_path"] is True


@pytest.mark.parametrize("provenance", ("missing", "foreign"))
def test_acceptance_rejects_missing_or_foreign_candidate_interpreter(
    tmp_path: Path,
    provenance: str,
) -> None:
    harness, catalog, project = _temporary_harness(tmp_path)
    if provenance == "missing":
        (project / ".venv/bin/python").unlink()
        expected = "interpreter is missing"
    else:
        (project / ".venv/pyvenv.cfg").unlink()
        expected = "foreign provenance"

    with pytest.raises(RuntimeError, match=expected):
        harness.run_acceptance(catalog, tmp_path / "receipt.json")


@pytest.mark.acceptance
def test_exact_commit_receipt_is_reusable_and_invalidated_by_movement(
    tmp_path: Path,
) -> None:
    harness, catalog, project = _temporary_harness(tmp_path)
    receipt_path = tmp_path / "receipt.json"

    receipt = harness.run_acceptance(catalog, receipt_path)
    report = harness.report_from_receipt(catalog, receipt_path)

    assert receipt["schema"] == "command-owner-acceptance-receipt/v1"
    assert receipt["candidate_commit"] == _git(project, "rev-parse", "HEAD")
    assert receipt["counts"]["tests"] == 1
    assert receipt["counts"]["failures"] == 0
    assert receipt["deselected"] == 0
    assert report["aggregate_evidence"]["keys"] == {"source_green": True}
    assert report["aggregate_evidence"]["aliases"] == {"source_alias": True}
    assert "source_sha256" not in report["aggregate_evidence"]["evidence"][
        "source_green"
    ]["tests"][0]

    harness._run_evidence_nodes = lambda *_args: (_ for _ in ()).throw(  # type: ignore[attr-defined]
        AssertionError("receipt reuse must not run pytest")
    )
    assert harness.report_from_receipt(catalog, receipt_path) == report

    test_path = project / "tests/test_evidence.py"
    original = test_path.read_text(encoding="utf-8")
    test_path.write_text(original + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="worktree must be clean"):
        harness.report_from_receipt(catalog, receipt_path)
    test_path.write_text(original, encoding="utf-8")
    assert _git(project, "status", "--porcelain", "--untracked-files=all") == ""


def test_receipt_tampering_and_in_repository_destination_fail_closed(
    tmp_path: Path,
) -> None:
    harness, catalog, project = _temporary_harness(tmp_path)
    receipt_path = tmp_path / "receipt.json"
    harness.run_acceptance(catalog, receipt_path)
    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    payload["report"]["aggregate_evidence"]["keys"]["source_green"] = False
    receipt_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="digest does not match"):
        harness.report_from_receipt(catalog, receipt_path)
    with pytest.raises(RuntimeError, match="outside the candidate repository"):
        harness.run_acceptance(catalog, project / "receipt.json")
