from __future__ import annotations

import ast
import copy
import hashlib
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
    build_observed_report,
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
EXPECTED_AGGREGATE_EVIDENCE = {
    "source_characterization_green": {
        "aliases": ["source_characterization_green"],
        "scenarios": [
            "intake-fresh-atomic",
            "planning-single-slice-queued",
            "execution-validated-reviewed-committed",
            "closeout-same-batch-no-successor",
        ],
        "tests": [
            {
                "node": "tests/test_command_owner_behavioral_scenarios.py::test_workflow_catalog_keeps_slice_two_families_green",
                "source_sha256": "8a72760a9b41110774c7cd007bc965bbdcdf97df25fb74b0e5627f5437a39df5",
                "scenarios": [
                    "intake-fresh-atomic",
                    "planning-single-slice-queued",
                    "execution-validated-reviewed-committed",
                    "closeout-same-batch-no-successor",
                ],
            }
        ],
    },
    "target_interfaces_green": {
        "aliases": ["target_interface_scenarios_green"],
        "scenarios": [
            "quality-cohesive-single-slice",
            "planning-selected-current",
            "protected-handoff-ready",
            "candidate-child-generation-ready",
            "history-readable-nonauthoritative",
        ],
        "tests": [
            {
                "node": "tests/test_command_owner_behavioral_scenarios.py::test_planning_quality_scenarios_cover_semantic_scope_approval_and_drafts",
                "source_sha256": "6f64b5a8674c61ba6923035119d188bb9db2d3f9c4bacf6babd84c5576071825",
                "scenarios": ["quality-cohesive-single-slice"],
            },
            {
                "node": "tests/test_command_owner_scenario_currentness.py::test_current_and_validate_are_the_semantic_state_authority",
                "source_sha256": "4d98938f2bda3e3a43e313c3b287da37b1812599cad26b1ccf843f2353aff90a",
                "scenarios": ["planning-selected-current"],
            },
            {
                "node": "tests/test_command_owner_scenario_currentness.py::test_protected_handoff_binds_lease_scope_receipt_and_reviewer_base",
                "source_sha256": "095a27802c9b0e5ded43fc8380722361428acefdc919eefe7b3bf1a586e9fa21",
                "scenarios": ["protected-handoff-ready"],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_lineage_and_child_generation_use_observed_repository_and_process_facts",
                "source_sha256": "d8521115f19610b6724b2ce247bd1c34edc3064fdf0cc1ce0f0c4b40852da673",
                "scenarios": ["candidate-child-generation-ready"],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_bridge_absence_is_synthetic_and_history_never_becomes_pickup_authority",
                "source_sha256": "55bd674d01b146f3dff464cd0ca932ce4b2a27c734c8dae2a6165d569763be91",
                "scenarios": ["history-readable-nonauthoritative"],
            },
        ],
    },
    "bootstrap_cutover_green": {
        "aliases": ["bootstrap_and_cutover_scenarios_green"],
        "scenarios": [
            "root-three-way-ready",
            "branch-lineage-ready",
            "installer-clean-ready",
            "cutover-atomic-switch-ready",
            "cutover-rollback-ready",
            "cutover-quiescence-ready",
            "cutover-bridge-minimum-ready",
            "physical-synthetic-absence-ready",
        ],
        "tests": [
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_root_and_generation_faults_fail_closed_without_canonical_write",
                "source_sha256": "3aa284915384093bad5963f659df79319f5940e541cd191551889490fb71b88e",
                "scenarios": ["root-three-way-ready"],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_lineage_and_child_generation_use_observed_repository_and_process_facts",
                "source_sha256": "d8521115f19610b6724b2ce247bd1c34edc3064fdf0cc1ce0f0c4b40852da673",
                "scenarios": ["branch-lineage-ready"],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_install_switch_rollback_and_quiescence_are_disposable_and_atomic",
                "source_sha256": "89daa20824ff5fe38b4d128f7c933975d7b091473a55726227dad9f2aaa1d463",
                "scenarios": [
                    "installer-clean-ready",
                    "cutover-atomic-switch-ready",
                    "cutover-rollback-ready",
                    "cutover-quiescence-ready",
                ],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_bridge_absence_is_synthetic_and_history_never_becomes_pickup_authority",
                "source_sha256": "55bd674d01b146f3dff464cd0ca932ce4b2a27c734c8dae2a6165d569763be91",
                "scenarios": [
                    "cutover-bridge-minimum-ready",
                    "physical-synthetic-absence-ready",
                ],
            },
        ],
    },
    "fault_injection_green": {
        "aliases": ["fault_injection_scenarios_green"],
        "scenarios": [
            "planning-partial-selection-resumes",
            "implementation-moved-blocked",
            "missing-receipt-blocked",
            "root-canonical-write-blocked",
            "root-mixed-generation-blocked",
            "installer-partial-blocked",
            "installer-stale-link-blocked",
            "cutover-switch-failure-preserves-stable",
            "cutover-quiescence-blocked",
        ],
        "tests": [
            {
                "node": "tests/test_command_owner_behavioral_scenarios.py::test_public_store_scenarios_expose_atomic_recovery_and_no_successor_effects",
                "source_sha256": "684786f4aa3bf84306d597c245f22125226480a4a9db62230d0c10226e5a3c64",
                "scenarios": ["planning-partial-selection-resumes"],
            },
            {
                "node": "tests/test_command_owner_scenario_currentness.py::test_movement_faults_cross_distinct_observation_boundaries",
                "source_sha256": "8219cefcfa86088a6058ecb79454f5dee4fe53963b0514615d551fe9f6f2327f",
                "scenarios": ["implementation-moved-blocked"],
            },
            {
                "node": "tests/test_command_owner_scenario_currentness.py::test_each_independent_handoff_consumer_fails_closed",
                "source_sha256": "4173010dc3171231363d309d6addd4af25b893e302d20dee06d7da7526e8c25f",
                "scenarios": ["missing-receipt-blocked"],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_root_and_generation_faults_fail_closed_without_canonical_write",
                "source_sha256": "3aa284915384093bad5963f659df79319f5940e541cd191551889490fb71b88e",
                "scenarios": [
                    "root-canonical-write-blocked",
                    "root-mixed-generation-blocked",
                ],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_install_switch_rollback_and_quiescence_are_disposable_and_atomic",
                "source_sha256": "89daa20824ff5fe38b4d128f7c933975d7b091473a55726227dad9f2aaa1d463",
                "scenarios": [
                    "installer-partial-blocked",
                    "installer-stale-link-blocked",
                    "cutover-switch-failure-preserves-stable",
                    "cutover-quiescence-blocked",
                ],
            },
        ],
    },
    "contract_coverage_complete": {
        "aliases": ["contract_id_coverage_report_complete"],
        "scenarios": [
            "intake-fresh-atomic",
            "planning-single-slice-queued",
            "execution-validated-reviewed-committed",
            "closeout-same-batch-no-successor",
            "planning-selected-current",
            "history-readable-nonauthoritative",
            "contract-format-topology-independent",
        ],
        "tests": [
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_contract_coverage_evidence_is_exact_and_green",
                "source_sha256": "77faa3e7ce38096c165abd4850d8151c9cc6cff361bec8da949e1fe7fa2c00fd",
                "scenarios": [
                    "intake-fresh-atomic",
                    "planning-single-slice-queued",
                    "execution-validated-reviewed-committed",
                    "closeout-same-batch-no-successor",
                    "planning-selected-current",
                    "history-readable-nonauthoritative",
                    "contract-format-topology-independent",
                ],
            }
        ],
    },
    "legacy_topology_not_required": {
        "aliases": ["legacy_skill_names_not_required_except_migration_fixtures"],
        "scenarios": [
            "contract-format-topology-independent",
            "physical-synthetic-absence-ready",
        ],
        "tests": [
            {
                "node": "tests/test_command_owner_behavioral_scenarios.py::test_scenario_command_is_a_semantic_label_not_an_executable_dispatch",
                "source_sha256": "947f5237127ca1713e343b36fd34d677bf8708ca3379bbd32f1b6deb7671d85e",
                "scenarios": ["contract-format-topology-independent"],
            },
            {
                "node": "tests/test_command_owner_scenario_cutover.py::test_bridge_absence_is_synthetic_and_history_never_becomes_pickup_authority",
                "source_sha256": "55bd674d01b146f3dff464cd0ca932ce4b2a27c734c8dae2a6165d569763be91",
                "scenarios": ["physical-synthetic-absence-ready"],
            },
        ],
    },
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


def _simple_evidence_hash(source: str) -> str:
    tree = ast.parse(source)
    function = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == "test_evidence"
    )
    lines = source.splitlines(keepends=True)
    definition = "".join(lines[function.lineno - 1 : function.end_lineno])
    grounded = json.dumps(
        {
            "collected_test_definition": definition,
            "module_collection_controls": [],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(grounded.encode()).hexdigest()


def _bind_all_gates_to_test(
    root: Path,
    *,
    source: str,
    node: str = "tests/test_evidence.py::test_evidence",
) -> None:
    document = _document(root)
    for gate in document["aggregate_evidence"]["gates"]:
        gate["tests"] = [
            {
                "node": node,
                "source_sha256": _simple_evidence_hash(source),
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
    assert _evidence(tmp_path / "root-three-way-ready", "root-three-way-ready")[
        "status"
    ] == "ready"
    assert _evidence(
        tmp_path / "root-canonical-write-blocked", "root-canonical-write-blocked"
    )["status"] == "blocked"
    assert _evidence(
        tmp_path / "root-mixed-generation-blocked", "root-mixed-generation-blocked"
    )["worker_generation"] == "fixture-candidate-child"


def test_lineage_and_child_generation_use_observed_repository_and_process_facts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
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


def test_final_report_emits_exact_green_keys_aliases_contracts_and_families() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    first = build_observed_report(validation.catalog)
    aggregate = first["aggregate_evidence"]
    assert isinstance(aggregate, dict)
    declared_gates = {
        gate["key"]: {
            "aliases": gate["aliases"],
            "scenarios": gate["scenarios"],
            "tests": gate["tests"],
        }
        for gate in _document()["aggregate_evidence"]["gates"]
    }
    expected_report_evidence = {
        key: {"scenarios": value["scenarios"], "tests": value["tests"]}
        for key, value in EXPECTED_AGGREGATE_EVIDENCE.items()
    }
    expected_alias_targets = {
        alias: key
        for key, value in EXPECTED_AGGREGATE_EVIDENCE.items()
        for alias in value["aliases"]
    }

    assert declared_gates == EXPECTED_AGGREGATE_EVIDENCE
    assert aggregate["keys"] == {key: True for key in ACCEPTANCE_KEYS}
    assert aggregate["aliases"] == {key: True for key in ACCEPTANCE_ALIASES}
    assert aggregate["alias_targets"] == expected_alias_targets
    assert aggregate["test_outcomes"] == {
        test["node"]: "passed"
        for gate in EXPECTED_AGGREGATE_EVIDENCE.values()
        for test in gate["tests"]
    }
    assert aggregate["evidence"] == expected_report_evidence
    assert len(first["contracts"]["required"]) == 31  # type: ignore[index]
    assert first["contracts"]["green"] == first["contracts"]["required"]  # type: ignore[index]
    assert first["contracts"]["not_green"] == []  # type: ignore[index]
    assert all(family["status"] == "green" for family in first["families"])
    assert first["acceptance"] == {
        "all_required_contracts_declared": True,
        "all_required_contracts_green": True,
        "all_required_families_green": True,
        "only_bound_green_observations_count": True,
    }


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
        ("unrelated-test-node", "catalog.test_evidence_source_mismatch"),
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
    elif mutation == "unrelated-test-node":
        gates[0]["tests"][0]["node"] = (
            "tests/test_command_owner_scenario_cutover.py::"
            "test_report_cli_emits_the_same_exact_aggregate_evidence"
        )
    else:
        gates[0]["tests"][0]["scenarios"] = []
    _write_document(root, document)

    validation = validate_catalog(root)

    assert not validation.is_valid
    assert expected_code in {item.code for item in validation.diagnostics}


@pytest.mark.parametrize(
    ("mark", "expected_code"),
    (
        ("skip", "catalog.disabled_test_evidence_decorator"),
        ("skipif", "catalog.disabled_test_evidence_decorator"),
        ("xfail", "catalog.disabled_test_evidence_decorator"),
        ("module-xfail", "catalog.disabled_test_evidence_module"),
        ("module-disabled", "catalog.disabled_test_evidence_module"),
    ),
)
def test_test_evidence_rejects_disabled_function_and_module_collection(
    tmp_path: Path, mark: str, expected_code: str
) -> None:
    harness, root, project = _temporary_harness(tmp_path)
    test_path = project / "tests/test_command_owner_behavioral_scenarios.py"
    source = test_path.read_text(encoding="utf-8")
    if mark in {"skip", "skipif", "xfail"}:
        arguments = (
            "True, reason='negative evidence fixture'"
            if mark == "skipif"
            else "reason='negative evidence fixture'"
        )
        source = source.replace(
            "def test_workflow_catalog_keeps_slice_two_families_green() -> None:",
            f"@pytest.mark.{mark}({arguments})\n"
            "def test_workflow_catalog_keeps_slice_two_families_green() -> None:",
            1,
        )
    else:
        control = (
            "pytestmark = pytest.mark.xfail(reason='negative evidence fixture')"
            if mark == "module-xfail"
            else "__test__ = False"
        )
        source = source.replace(
            "from __future__ import annotations\n",
            f"from __future__ import annotations\n\n{control}\n",
            1,
        )
    test_path.write_text(source, encoding="utf-8")

    validation = harness.validate_catalog(root)

    assert not validation.is_valid
    assert expected_code in {item.code for item in validation.diagnostics}


def test_fixture_local_test_shadow_cannot_replace_candidate_evidence(
    tmp_path: Path,
) -> None:
    root = _copy_fixtures(tmp_path)
    shadow = tmp_path / "tests/test_command_owner_behavioral_scenarios.py"
    shadow.write_text(
        "import pytest\n\n"
        "def test_workflow_catalog_keeps_slice_two_families_green():\n"
        "    pytest.skip('fixture-local shadow must never count')\n",
        encoding="utf-8",
    )

    validation = validate_catalog(root)

    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None


@pytest.mark.parametrize(
    "mode",
    (
        "runtime-skip",
        "runtime-xfail",
        "runtime-xpass",
        "collection-hook",
        "deselected",
        "assertion-failure",
        "setup-error",
    ),
)
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
        "assertion-failure": "assert False",
        "setup-error": "assert True",
    }[mode]
    parameters = "missing_fixture" if mode == "setup-error" else ""
    source = (
        "import pytest\n\n"
        f"def test_evidence({parameters}):\n"
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
            "import pytest\n\n"
            "def pytest_collection_modifyitems(items):\n"
            + hook_body,
            encoding="utf-8",
        )
    _bind_all_gates_to_test(root, source=source)
    validation = harness.validate_catalog(root)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    with pytest.raises(RuntimeError, match="did not pass exclusively"):
        harness.build_observed_report(validation.catalog)


def test_observed_aggregate_runtime_uses_sanitized_candidate_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness, root, project = _temporary_harness(tmp_path)
    source = (
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n\n"
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
    _bind_all_gates_to_test(root, source=source)
    validation = harness.validate_catalog(root)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None
    monkeypatch.setenv("PYTHONHOME", "/tmp/foreign-python-home")
    monkeypatch.setenv("PYTHONPATH", "/tmp/foreign-python-path")
    monkeypatch.setenv("PYTEST_ADDOPTS", "--deselect=tests/test_evidence.py")
    monkeypatch.setenv("PYTEST_PLUGINS", "foreign_plugin")
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "0")

    outcomes = harness._observe_aggregate_test_outcomes(validation.catalog)

    assert set(outcomes.values()) == {"passed"}


@pytest.mark.parametrize("provenance", ("missing", "foreign"))
def test_observed_aggregate_rejects_missing_or_foreign_candidate_interpreter(
    tmp_path: Path,
    provenance: str,
) -> None:
    harness, root, project = _temporary_harness(tmp_path)
    source = "def test_evidence():\n    assert True\n"
    (project / "tests/test_evidence.py").write_text(source, encoding="utf-8")
    _bind_all_gates_to_test(root, source=source)
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
        harness.build_observed_report(validation.catalog)


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


def test_direct_report_without_observed_pytest_outcomes_stays_non_green() -> None:
    validation = validate_catalog(FIXTURES)
    assert validation.is_valid, validation.diagnostics
    assert validation.catalog is not None

    aggregate = build_report(validation.catalog)["aggregate_evidence"]

    assert isinstance(aggregate, dict)
    assert aggregate["keys"] == {key: False for key in ACCEPTANCE_KEYS}
    assert aggregate["aliases"] == {key: False for key in ACCEPTANCE_ALIASES}
    assert set(aggregate["test_outcomes"].values()) == {"not-observed"}

    with pytest.raises(TypeError):
        build_report(
            validation.catalog,
            observed_test_outcomes={"caller-controlled": "passed"},  # type: ignore[call-arg]
        )


def test_report_cli_emits_the_same_exact_aggregate_evidence() -> None:
    process = subprocess.run(
        [
            str(REPO_ROOT / ".venv/bin/python"),
            str(REPO_ROOT / "scripts/command_owner_scenarios.py"),
            "report",
            str(FIXTURES),
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert process.returncode == 0, process.stderr
    aggregate = json.loads(process.stdout)["aggregate_evidence"]
    assert aggregate["keys"] == {key: True for key in ACCEPTANCE_KEYS}
    assert aggregate["aliases"] == {key: True for key in ACCEPTANCE_ALIASES}
