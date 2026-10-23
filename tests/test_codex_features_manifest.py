from __future__ import annotations

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
    sources: set[Path] = set()
    for feature in features.values():
        for link in feature["links"]:
            source = Path(link["source"])
            target = Path(link["target"])
            assert not source.is_absolute()
            assert not target.is_absolute()
            assert ".." not in source.parts
            assert ".." not in target.parts
            assert (REPO_ROOT / source).exists()
            assert (REPO_ROOT / source).resolve().is_relative_to(REPO_ROOT.resolve())
            assert source.parts[0] not in {".agents", ".codex"}
            sources.add(source)
            targets.append(str(target))
    assert len(targets) == len(set(targets))
    assert Path("AGENTS.md") not in sources
    assert not (REPO_ROOT / ".codex" / "AGENTS.md").exists()


def test_manifest_rejects_a_source_symlink_that_escapes_the_repository(
    tmp_path: Path,
) -> None:
    external_source = tmp_path / "external-source"
    external_source.write_text("external\n", encoding="utf-8")
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "escaped-source").symlink_to(external_source)
    data = {
        "schema_version": 1,
        "features": {
            "escaped": {
                "version": "1.0.0",
                "links": [
                    {"source": "escaped-source", "target": "escaped-target"}
                ],
            }
        },
    }

    with pytest.raises(InstallError, match="resolves outside the repository"):
        validate_manifest(repository, data)


def test_default_and_all_feature_selection() -> None:
    data = manifest()
    default_args = Namespace(feature=[], all_features=False)
    all_args = Namespace(feature=[], all_features=True)

    defaults = selected_feature_names(default_args, data)
    all_features = selected_feature_names(all_args, data)

    assert "agent-notifications" not in defaults
    assert set(all_features) == set(data["features"])


def test_global_feature_installs_personal_instructions_and_owner_command() -> None:
    data = manifest()
    global_feature = data["features"]["global-instructions"]

    assert global_feature["links"] == [
        {"source": "global/AGENTS.md", "target": "AGENTS.md"},
        {"source": "scripts/codex_owner.py", "target": "bin/codex-owner"},
    ]


def test_port_by_contract_requires_explicit_invocation() -> None:
    config = (
        REPO_ROOT / "skills" / "port-by-contract" / "agents" / "openai.yaml"
    ).read_text(encoding="utf-8")

    assert "\npolicy:\n  allow_implicit_invocation: false\n" in config


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


def test_surviving_agent_configs_parse_and_are_read_only() -> None:
    agent_paths = sorted((REPO_ROOT / "agents").glob("*.toml"))
    assert {path.name for path in agent_paths} == {
        "codebase_investigator.toml",
        "import_topology_reviewer.toml",
        "reviewer.toml",
    }
    for path in agent_paths:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        assert data["name"] == path.stem
        assert data["sandbox_mode"] == "read-only"
        assert data["approval_policy"] == "never"


def test_custom_agents_use_native_defaults_and_explicit_review_exceptions() -> None:
    investigator = tomllib.loads(
        (REPO_ROOT / "agents/codebase_investigator.toml").read_text(encoding="utf-8")
    )
    assert "model" not in investigator
    assert "model_reasoning_effort" not in investigator
    for name in ("reviewer", "import_topology_reviewer"):
        reviewer = tomllib.loads(
            (REPO_ROOT / "agents" / f"{name}.toml").read_text(encoding="utf-8")
        )
        assert reviewer["model"] == "gpt-6-astra"
        assert reviewer["model_reasoning_effort"] == "medium"
        assert reviewer["service_tier"] == "fast"
