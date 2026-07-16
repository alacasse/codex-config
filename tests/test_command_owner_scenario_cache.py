from __future__ import annotations

import shutil
from collections.abc import Mapping
from pathlib import Path

import pytest
import yaml

import scripts.command_owner_scenarios as harness


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/command-owner-scenarios"
VALID_RUNTIME = FIXTURES / "self-test/valid-runtime"


def test_scenario_evaluation_is_cached_per_immutable_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture_root = tmp_path / "runtime"
    shutil.copytree(VALID_RUNTIME, fixture_root)
    validation = harness.validate_catalog(fixture_root)
    assert validation.catalog is not None
    original = harness._evaluate_scenario
    calls: list[str] = []

    def counted(
        catalog: harness.Catalog,
        scenario: Mapping[str, object],
    ) -> harness.ScenarioEvaluation:
        calls.append(str(scenario["id"]))
        return original(catalog, scenario)

    monkeypatch.setattr(harness, "_evaluate_scenario", counted)
    first = harness.evaluate_catalog(validation.catalog)
    second = harness.evaluate_catalog(validation.catalog)

    assert first == second
    assert len(calls) == len(validation.catalog.document["scenarios"])
    assert len(calls) == len(set(calls))


def test_dot_path_segments_are_not_valid_fixture_paths(tmp_path: Path) -> None:
    fixture_root = tmp_path / "fixtures"
    shutil.copytree(
        FIXTURES,
        fixture_root,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    catalog_path = fixture_root / "catalog.yaml"
    document = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    document["scenarios"][0]["expected_writes"] = ["."]
    catalog_path.write_text(
        yaml.safe_dump(document, sort_keys=False),
        encoding="utf-8",
    )

    validation = harness.validate_catalog(fixture_root)

    assert not validation.is_valid
    assert {diagnostic.code for diagnostic in validation.diagnostics} == {
        "schema.pattern"
    }
