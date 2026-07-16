from __future__ import annotations

import importlib.util
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/command-owner-scenarios"
pytestmark = pytest.mark.acceptance


def _document() -> Mapping[str, object]:
    loaded = yaml.safe_load((FIXTURES / "catalog.yaml").read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _scenario(scenario_id: str) -> Mapping[str, object]:
    scenarios = _document()["scenarios"]
    assert isinstance(scenarios, list)
    return next(
        scenario
        for scenario in scenarios
        if isinstance(scenario, dict) and scenario["id"] == scenario_id
    )


def _adapter_module() -> ModuleType:
    path = FIXTURES / "cutover_adapters.py"
    name = f"_cutover_regression_adapters_{id(path)}"
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


def test_adapter_rejects_foreign_cached_project_module(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    foreign = ModuleType("scripts.install_codex_config")
    foreign.__file__ = "/tmp/foreign-checkout/scripts/install_codex_config.py"
    monkeypatch.setitem(sys.modules, "scripts.install_codex_config", foreign)

    with pytest.raises(ImportError, match="does not resolve to candidate source"):
        _adapter_module()


def test_failed_installation_cleans_staging_and_preserves_default(
    tmp_path: Path,
) -> None:
    adapter = _adapter_module()
    ids = ("installer-partial-blocked", "installer-stale-link-blocked")
    evidence: dict[str, Mapping[str, object]] = {}
    for scenario_id in ids:
        workspace = tmp_path / scenario_id
        adapter.run_scenario(_scenario(scenario_id), FIXTURES, workspace)
        evidence[scenario_id] = _evidence(workspace, scenario_id)

    assert all(item["published"] is False for item in evidence.values())
    assert all(item["staging_removed"] is True for item in evidence.values())
    assert all(item["staged_link_observed"] is True for item in evidence.values())
    assert all(item["default_generation_unchanged"] is True for item in evidence.values())
    assert all(
        (item["default_generation_before"], item["default_generation_after"])
        == ("stable", "stable")
        for item in evidence.values()
    )


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
