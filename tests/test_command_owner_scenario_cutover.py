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
from typing import Any

import pytest
import yaml

from scripts.command_owner_scenarios import validate_catalog


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


def _document(root: Path = FIXTURES) -> dict[str, Any]:
    loaded = yaml.safe_load((root / "catalog.yaml").read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _scenario(scenario_id: str) -> Mapping[str, object]:
    return next(
        scenario
        for scenario in _document()["scenarios"]
        if scenario["id"] == scenario_id
    )


def _adapter_module() -> ModuleType:
    path = FIXTURES / "cutover_adapters.py"
    spec = importlib.util.spec_from_file_location("_cutover_scenario_adapters", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
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


def _temporary_harness(
    tmp_path: Path,
) -> tuple[ModuleType, Path, Path]:
    project = tmp_path / "candidate"
    venv.EnvBuilder(
        system_site_packages=True,
        with_pip=False,
    ).create(project / ".venv")
    (project / "scripts").mkdir(parents=True)
    (project / "schemas").mkdir()
    test_root = project / "tests"
    test_root.mkdir()
    shutil.copy2(REPO_ROOT / "tests/__init__.py", test_root / "__init__.py")
    fixture_root = test_root / "fixtures/command-owner-scenarios"
    shutil.copytree(FIXTURES, fixture_root)
    shutil.copy2(
        REPO_ROOT / "scripts/command_owner_scenarios.py",
        project / "scripts/command_owner_scenarios.py",
    )
    shutil.copy2(
        REPO_ROOT / "schemas/command-owner-scenario-v1.schema.json",
        project / "schemas/command-owner-scenario-v1.schema.json",
    )
    for name in (
        "test_command_owner_behavioral_scenarios.py",
        "test_command_owner_scenario_currentness.py",
        "test_command_owner_scenario_cutover.py",
    ):
        shutil.copy2(REPO_ROOT / "tests" / name, test_root / name)
    harness_path = project / "scripts/command_owner_scenarios.py"
    module_name = f"_temporary_command_owner_scenarios_{tmp_path.name}"
    spec = importlib.util.spec_from_file_location(module_name, harness_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module, fixture_root, project


def _commit_fixture(project: Path, message: str) -> None:
    subprocess.run(["git", "add", "."], cwd=project, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Scenario Test",
            "-c",
            "user.email=scenario@example.invalid",
            "commit",
            "-qm",
            message,
        ],
        cwd=project,
        check=True,
    )


def _temporary_acceptance_harness(
    tmp_path: Path,
) -> tuple[ModuleType, Path, Path]:
    harness, fixture_root, project = _temporary_harness(tmp_path)
    runtime_root = FIXTURES / "self-test/valid-runtime"
    document = _document(runtime_root)
    document["scenarios"] = [copy.deepcopy(document["scenarios"][2])]
    document["aggregate_evidence"] = {
        "gates": [
            {
                "key": "runtime_green",
                "aliases": ["runtime_green"],
                "scenarios": ["green-scenario"],
                "tests": [
                    {
                        "node": "tests/test_evidence.py::test_evidence_one",
                        "scenarios": ["green-scenario"],
                    },
                    {
                        "node": "tests/test_evidence.py::test_evidence_two",
                        "scenarios": ["green-scenario"],
                    },
                ],
            }
        ]
    }
    _write_document(fixture_root, document)
    shutil.copy2(runtime_root / "adapters.py", fixture_root / "adapters.py")
    shutil.copy2(REPO_ROOT / "pyproject.toml", project / "pyproject.toml")
    (project / "tests/test_evidence.py").write_text(
        "from pathlib import Path\n\n"
        "import pytest\n\n"
        "import scripts.command_owner_scenarios as harness\n\n"
        "FIXTURES = Path(__file__).parent / 'fixtures/command-owner-scenarios'\n\n"
        "evaluations = 0\n"
        "original_evaluate = harness._evaluate_scenario\n\n"
        "def counting_evaluate(*args, **kwargs):\n"
        "    global evaluations\n"
        "    evaluations += 1\n"
        "    return original_evaluate(*args, **kwargs)\n\n"
        "harness._evaluate_scenario = counting_evaluate\n\n"
        "def assert_green_once():\n"
        "    validation = harness.validate_catalog(FIXTURES)\n"
        "    assert validation.catalog is not None\n"
        "    assert harness.evaluate_catalog(validation.catalog)[0].status == 'green'\n"
        "    assert evaluations == 1\n\n"
        "@pytest.mark.command_owner_evidence\n"
        "def test_evidence_one():\n"
        "    assert_green_once()\n\n"
        "@pytest.mark.command_owner_evidence\n"
        "def test_evidence_two():\n"
        "    assert_green_once()\n",
        encoding="utf-8",
    )
    (project / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    _commit_fixture(project, "acceptance fixture")
    return harness, fixture_root, project


def _bind_all_gates_to_test(
    root: Path,
    *,
    node: str = "tests/test_evidence.py::test_evidence",
) -> None:
    document = _document(root)
    for gate in document["aggregate_evidence"]["gates"]:
        gate["tests"] = [
            {
                "node": node,
                "scenarios": list(gate["scenarios"]),
            }
        ]
    _write_document(root, document)


def _write_document(root: Path, document: Mapping[str, object]) -> None:
    (root / "catalog.yaml").write_text(
        yaml.safe_dump(dict(document), sort_keys=False), encoding="utf-8"
    )


@pytest.mark.parametrize("scenario_id", sorted(CUTOVER_SCENARIOS))
def test_every_cutover_scenario_matches_observed_disposable_effects(
    tmp_path: Path, scenario_id: str
) -> None:
    adapter = _adapter_module()
    workspace = tmp_path / "workspace"

    observation = adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)

    assert observation == {
        "transition": _scenario(scenario_id)["expected_transition"],
        "writes": _scenario(scenario_id)["expected_writes"],
        "forbidden_writes": _scenario(scenario_id)["forbidden_writes"],
        "stop_reason": _scenario(scenario_id)["expected_stop_reason"],
        "generation_and_roots": _scenario(scenario_id)["generation_and_roots"],
        "validation": _scenario(scenario_id)["validation"],
    }
    assert (workspace / "evidence" / f"{scenario_id}.json").is_file()
    assert all(path.is_relative_to(tmp_path) for path in workspace.rglob("*"))


@pytest.mark.command_owner_evidence
def test_root_and_generation_faults_fail_closed_without_canonical_write(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()
    for scenario_id in (
        "root-three-way-ready",
        "root-canonical-write-blocked",
        "root-mixed-generation-blocked",
    ):
        workspace = tmp_path / scenario_id
        adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)
        evidence = _evidence(workspace, scenario_id)
        roots = evidence["roots"]
        assert isinstance(roots, dict)
        assert len(set(roots.values())) == 3
        assert evidence["canonical_write_occurred"] is False
        assert evidence["outside_destination_rejected"] is True
        assert evidence["allowed_implementation_paths"] == [
            str((workspace / "implementation-target" / "allowed.txt").resolve())
        ]
        assert evidence["strict_module_origin"] == str(
            (REPO_ROOT / "scripts/cross_checkout_context.py").resolve()
        )
    assert (
        _evidence(tmp_path / "root-three-way-ready", "root-three-way-ready")["status"]
        == "ready"
    )
    assert (
        _evidence(
            tmp_path / "root-canonical-write-blocked", "root-canonical-write-blocked"
        )["status"]
        == "blocked"
    )
    assert (
        _evidence(
            tmp_path / "root-mixed-generation-blocked", "root-mixed-generation-blocked"
        )["worker_generation"]
        == "fixture-candidate-child"
    )


@pytest.mark.command_owner_evidence
def test_lineage_and_child_generation_use_observed_repository_and_process_facts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    adapter = _adapter_module()
    lineage_workspace = tmp_path / "lineage"
    child_workspace = tmp_path / "child"

    monkeypatch.setenv("PYTHONPATH", "/tmp/foreign-checkout")
    adapter.run_scenario(_scenario("branch-lineage-ready"), FIXTURES, lineage_workspace)
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
    assert child["module_origin"] == str(
        (REPO_ROOT / "scripts/install_codex_config.py").resolve()
    )
    assert child["sanitized_pythonpath"] == str(REPO_ROOT)


def test_adapter_rejects_foreign_cached_project_module(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    foreign = ModuleType("scripts.install_codex_config")
    foreign.__file__ = "/tmp/foreign-checkout/scripts/install_codex_config.py"
    monkeypatch.setitem(sys.modules, "scripts.install_codex_config", foreign)

    with pytest.raises(ImportError, match="does not resolve to candidate source"):
        _adapter_module()


@pytest.mark.command_owner_evidence
def test_install_switch_rollback_and_quiescence_are_disposable_and_atomic(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()
    scenario_ids = (
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
    for scenario_id in scenario_ids:
        workspace = tmp_path / scenario_id
        adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)
        evidence[scenario_id] = _evidence(workspace, scenario_id)

    assert evidence["installer-clean-ready"]["published"] is True
    assert evidence["installer-partial-blocked"]["published"] is False
    assert evidence["installer-stale-link-blocked"]["published"] is False
    assert evidence["installer-partial-blocked"]["staging_removed"] is True
    assert evidence["installer-stale-link-blocked"]["staging_removed"] is True
    assert evidence["installer-partial-blocked"]["staged_link_observed"] is True
    assert evidence["installer-stale-link-blocked"]["staged_link_observed"] is True
    assert all(
        item["default_generation_unchanged"] is True
        for key, item in evidence.items()
        if key.startswith("installer-")
    )
    assert all(
        (item["default_generation_before"], item["default_generation_after"])
        == ("stable", "stable")
        for key, item in evidence.items()
        if key.startswith("installer-")
    )
    assert all(
        item["installer_module_origin"]
        == str((REPO_ROOT / "scripts/install_codex_config.py").resolve())
        for key, item in evidence.items()
        if key.startswith("installer-")
    )
    assert evidence["cutover-atomic-switch-ready"] == {
        "after": "candidate",
        "before": "stable",
        "controller": "stable",
        "missing_route_observations": 0,
        "publication_events": ["stage-replacement", "replace-visible-route"],
        "reader_observations": ["stable", "candidate"],
    }
    assert evidence["cutover-switch-failure-preserves-stable"] == {
        "after": "stable",
        "before": "stable",
        "controller": "stable",
        "missing_route_observations": 0,
        "publication_events": ["stage-replacement"],
        "reader_observations": ["stable", "stable"],
    }
    assert evidence["cutover-rollback-ready"] == {
        "before": "stable",
        "missing_route_observations": 0,
        "publication_events": [
            ["stage-replacement", "replace-visible-route"],
            ["stage-replacement", "replace-visible-route"],
        ],
        "reader_observations": ["stable", "candidate", "candidate", "stable"],
        "restored": "stable",
        "switched": "candidate",
    }
    assert evidence["cutover-quiescence-blocked"]["ready"] is False
    assert evidence["cutover-quiescence-ready"]["ready"] is True


def test_visible_route_unlink_and_relink_cannot_masquerade_as_atomic_switch(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()

    def unsafe_publisher(
        default: Path,
        target: Path,
        *,
        probe: Any,
        before_replace: Any,
        after_replace: Any,
    ) -> None:
        before_replace()
        probe.unlink_visible(default)
        probe.relink_visible(default, target)
        after_replace()

    with pytest.raises(adapter.FixtureBoundaryError, match="unlinked or relinked"):
        adapter.run_scenario(
            _scenario("cutover-atomic-switch-ready"),
            FIXTURES,
            tmp_path / "unsafe-switch",
            publisher=unsafe_publisher,
        )


@pytest.mark.command_owner_evidence
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

    assert evidence["cutover-bridge-minimum-ready"] == {
        "control_interface": "cross-checkout-context/v1",
        "planning_authority": "master",
        "scope": "root-generation-and-receipt-only",
    }
    absence = evidence["physical-synthetic-absence-ready"]
    assert absence["synthetic_fixture"] is True
    assert absence["real_deletion_claimed"] is False
    assert absence["bridge_present"] is False
    assert absence["forbidden_target_terms"] == []
    history = evidence["history-readable-nonauthoritative"]
    assert history["historical"] == {
        "active_runway": "archived-runway",
        "selected_dispatch": "archived-dispatch",
    }
    assert history["pickup"].endswith("/live-batch/dispatch.md")
    assert history["authority"] == "planning-state-current"
    assert history["archive_readable"] is True
    assert history["planning_state_origin"] == str(
        (REPO_ROOT / "scripts/planning_state.py").resolve()
    )


@pytest.mark.command_owner_evidence
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
def test_aggregate_evidence_rejects_missing_duplicate_and_unknown_mappings(
    tmp_path: Path, mutation: str, expected_code: str
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


@pytest.mark.parametrize(
    "mode",
    (
        "runtime-skip",
        "runtime-xfail",
        "runtime-xpass",
        "collection-hook",
        "deselected",
        "missing-node",
        "unmarked-substitution",
        "assertion-failure",
        "setup-error",
    ),
)
@pytest.mark.command_owner_acceptance
def test_observed_aggregate_outcomes_reject_every_non_pass(
    tmp_path: Path,
    mode: str,
) -> None:
    harness, root, project = _temporary_harness(tmp_path)
    statement = {
        "runtime-skip": "pytest.skip('runtime skip')",
        "runtime-xfail": "pytest.xfail('runtime xfail')",
        "runtime-xpass": "assert True",
        "collection-hook": "assert True",
        "deselected": "assert True",
        "missing-node": "assert True",
        "unmarked-substitution": "assert True",
        "assertion-failure": "assert False",
        "setup-error": "assert True",
    }[mode]
    parameters = "missing_fixture" if mode == "setup-error" else ""
    marker = (
        ""
        if mode == "unmarked-substitution"
        else "@pytest.mark.command_owner_evidence\n"
    )
    function_name = "test_other" if mode == "missing-node" else "test_evidence"
    source = (
        "import pytest\n\n"
        f"{marker}"
        f"def {function_name}({parameters}):\n"
        f"    {statement}\n"
    )
    (project / "tests/test_evidence.py").write_text(source, encoding="utf-8")
    if mode in {"collection-hook", "runtime-xpass", "deselected"}:
        hook_body = {
            "collection-hook": (
                "    for item in items:\n"
                "        item.add_marker(pytest.mark.skip(reason='plugin collection skip'))\n"
            ),
            "runtime-xpass": (
                "    for item in items:\n"
                "        item.add_marker(pytest.mark.xfail(reason='plugin xpass', strict=False))\n"
            ),
            "deselected": (
                "    removed = list(items)\n"
                "    items[:] = []\n"
                "    items[0:0] = []\n"
                "    if removed:\n"
                "        removed[0].config.hook.pytest_deselected(items=removed)\n"
            ),
        }[mode]
        (project / "conftest.py").write_text(
            "import pytest\n\ndef pytest_collection_modifyitems(items):\n" + hook_body,
            encoding="utf-8",
        )
    _bind_all_gates_to_test(root)
    validation = harness.validate_catalog(root)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    with pytest.raises(RuntimeError, match="did not pass exclusively"):
        harness._execute_aggregate_test_evidence(validation.catalog)


@pytest.mark.command_owner_acceptance
def test_observed_aggregate_runtime_uses_sanitized_candidate_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness, root, project = _temporary_harness(tmp_path)
    source = (
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        "import pytest\n\n"
        "@pytest.mark.command_owner_evidence\n"
        "def test_evidence():\n"
        "    assert Path.cwd() == Path(" + repr(str(project)) + ")\n"
        "    assert sys.flags.safe_path\n"
        "    assert os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] == '1'\n"
        "    assert 'PYTHONHOME' not in os.environ\n"
        "    assert 'PYTHONPATH' not in os.environ\n"
        "    assert 'PYTEST_ADDOPTS' not in os.environ\n"
        "    assert 'PYTEST_PLUGINS' not in os.environ\n"
    )
    (project / "tests/test_evidence.py").write_text(source, encoding="utf-8")
    _bind_all_gates_to_test(root)
    validation = harness.validate_catalog(root)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None
    monkeypatch.setenv("PYTHONHOME", "/tmp/foreign-python-home")
    monkeypatch.setenv("PYTHONPATH", "/tmp/foreign-python-path")
    monkeypatch.setenv("PYTEST_ADDOPTS", "--deselect=tests/test_evidence.py")
    monkeypatch.setenv("PYTEST_PLUGINS", "foreign_plugin")
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "0")

    execution = harness._execute_aggregate_test_evidence(validation.catalog)

    assert set(execution.outcomes.values()) == {"passed"}


@pytest.mark.parametrize("provenance", ("missing", "foreign"))
@pytest.mark.command_owner_acceptance
def test_observed_aggregate_rejects_missing_or_foreign_candidate_interpreter(
    tmp_path: Path,
    provenance: str,
) -> None:
    harness, root, project = _temporary_harness(tmp_path)
    source = (
        "import pytest\n\n"
        "@pytest.mark.command_owner_evidence\n"
        "def test_evidence():\n"
        "    assert True\n"
    )
    (project / "tests/test_evidence.py").write_text(source, encoding="utf-8")
    _bind_all_gates_to_test(root)
    validation = harness.validate_catalog(root)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None
    if provenance == "missing":
        (project / ".venv/bin/python").unlink()
        expected = "interpreter is missing"
    else:
        (project / ".venv/pyvenv.cfg").unlink()
        expected = "foreign provenance"

    with pytest.raises(RuntimeError, match=expected):
        harness._execute_aggregate_test_evidence(validation.catalog)


@pytest.mark.command_owner_acceptance
def test_exact_commit_acceptance_uses_one_pytest_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    harness, root, _project = _temporary_acceptance_harness(tmp_path)
    validation = harness.validate_catalog(root)
    assert validation.catalog is not None
    pytest_commands: list[list[str]] = []
    real_run = harness.subprocess.run

    def record_run(*args: Any, **kwargs: Any) -> Any:
        command = args[0]
        if isinstance(command, list) and command[1:4] == ["-P", "-m", "pytest"]:
            pytest_commands.append(command)
        return real_run(*args, **kwargs)

    monkeypatch.setattr(harness.subprocess, "run", record_run)
    result_path = tmp_path / "acceptance-result.json"
    json_path = tmp_path / "acceptance-report.json"
    text_path = tmp_path / "acceptance-report.txt"

    returncode = harness.main(
        [
            "accept",
            str(root),
            "--result-output",
            str(result_path),
            "--json-report-output",
            str(json_path),
            "--text-report-output",
            str(text_path),
        ]
    )
    result = json.loads(result_path.read_text())
    nodes = harness._aggregate_test_nodes(
        validation.catalog.document["aggregate_evidence"]
    )
    report = json.loads(json_path.read_text())
    assert len(pytest_commands) == result["evidence_pytest_process_count"] == 1
    assert set(nodes).issubset(pytest_commands[0])
    assert result["pytest_outcome"]["tests"] == 2
    assert result["report_sha256"] == harness._sha256_json(report)
    assert report["aggregate_evidence"]["keys"] == {"runtime_green": True}
    assert text_path.read_text() == harness._render_text_report(report)
    assert returncode == 0 and capsys.readouterr().out.startswith("accepted:")


@pytest.mark.command_owner_acceptance
def test_evaluation_reuse_invalidates_every_semantic_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness, root, project = _temporary_acceptance_harness(tmp_path)
    validation = harness.validate_catalog(root)
    assert validation.catalog is not None
    catalog = validation.catalog
    evaluations = 0
    original = harness._evaluate_scenario

    def counting_evaluation(*args: Any, **kwargs: Any) -> object:
        nonlocal evaluations
        evaluations += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(harness, "_evaluate_scenario", counting_evaluation)
    first = harness.evaluate_catalog(catalog)
    assert harness.evaluate_catalog(catalog) is first
    assert evaluations == 1

    moving_files = (
        root / "catalog.yaml",
        project / "schemas/command-owner-scenario-v1.schema.json",
        root / "adapters.py",
        project / "tests/test_evidence.py",
    )
    for path in moving_files:
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        harness.evaluate_catalog(catalog)
    assert evaluations == 5

    monkeypatch.setattr(
        harness,
        "_evaluation_interpreter_identity",
        lambda: {"executable": "moved", "prefix": "moved", "version": "moved"},
    )
    harness.evaluate_catalog(catalog)
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "moved-codex-home"))
    harness.evaluate_catalog(catalog)
    _commit_fixture(project, "move evaluation inputs")
    harness.evaluate_catalog(catalog)
    assert evaluations == 8
