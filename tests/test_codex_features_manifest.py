from __future__ import annotations

import json
import tomllib
from argparse import Namespace
from pathlib import Path
from typing import Any

import pytest

from scripts.install_codex_config import (
    InstallError,
    expand_feature_dependencies,
    load_manifest,
    selected_feature_names,
    validate_manifest,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "codex-features.json"


def manifest() -> dict[str, Any]:
    return load_manifest(MANIFEST_PATH)


def test_manifest_is_complete_and_all_sources_exist() -> None:
    data = manifest()
    validate_manifest(REPO_ROOT, data)
    features = data["features"]

    assert set(features) == {
        "global-instructions",
        "port-by-contract",
        "test-quality-review",
        "custom-agents",
        "dead-surface-audit",
        "agent-notifications",
    }

    targets: list[str] = []
    for feature in features.values():
        for link in feature["links"]:
            source = Path(link["source"])
            target = Path(link["target"])
            assert not source.is_absolute()
            assert not target.is_absolute()
            assert ".." not in source.parts
            assert ".." not in target.parts
            assert (REPO_ROOT / source).exists()
            targets.append(str(target))
    assert len(targets) == len(set(targets))


def test_default_and_all_feature_selection() -> None:
    data = manifest()
    default_args = Namespace(feature=[], all_features=False)
    all_args = Namespace(feature=[], all_features=True)

    defaults = selected_feature_names(default_args, data)
    all_features = selected_feature_names(all_args, data)

    assert "agent-notifications" not in defaults
    assert set(all_features) == set(data["features"])


def test_dependency_expansion_is_ordered_and_fails_closed() -> None:
    available = {
        "base": {"requires": []},
        "middle": {"requires": ["base"]},
        "top": {"requires": ["middle"]},
    }
    assert expand_feature_dependencies(["top"], available) == [
        "base",
        "middle",
        "top",
    ]

    with pytest.raises(InstallError, match="unknown feature"):
        expand_feature_dependencies(["top"], {"top": {"requires": ["missing"]}})
    with pytest.raises(InstallError, match="circular"):
        expand_feature_dependencies(
            ["first"],
            {
                "first": {"requires": ["second"]},
                "second": {"requires": ["first"]},
            },
        )


def test_surviving_skill_metadata_matches_directory_names() -> None:
    for skill_dir in sorted((REPO_ROOT / "skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert f"\nname: {skill_dir.name}\n" in text


def test_surviving_skills_keep_independent_behavioral_lenses() -> None:
    port = (REPO_ROOT / "skills" / "port-by-contract" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    quality = (REPO_ROOT / "skills" / "test-quality-review" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    dead = (REPO_ROOT / "skills" / "dead-surface-audit" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "implementation-neutral behavior contracts" in port
    assert "Design from contract responsibilities" in port
    assert "behavioral confidence" in quality
    assert "Do not optimize for coverage percentages" in quality
    assert "`behavioral`" in dead
    assert "`topology-assertion`" in dead


def test_surviving_agent_configs_parse_and_are_read_only() -> None:
    agent_paths = sorted((REPO_ROOT / "agents").glob("*.toml"))
    assert {path.name for path in agent_paths} == {
        "codebase_investigator.toml",
        "import_topology_reviewer.toml",
    }
    for path in agent_paths:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        assert data["name"] == path.stem
        assert "read-only" in instructions.lower()
        assert "Never spawn, delegate to, or wait" in instructions


def test_manifest_json_is_stable() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert json.loads(json.dumps(data, sort_keys=True)) == data
