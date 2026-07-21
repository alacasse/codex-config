from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "codex_owner.py"


def write_manifest(repo_root: Path) -> tuple[Path, Path]:
    skill_source = repo_root / "skills" / "example-review"
    script_source = repo_root / "scripts" / "example_tool.py"
    skill_source.mkdir(parents=True)
    script_source.parent.mkdir(parents=True)
    (skill_source / "SKILL.md").write_text("# Example Review\n", encoding="utf-8")
    script_source.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    (repo_root / "codex-features.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "features": {
                    "example-tools": {
                        "version": "1.0.0",
                        "links": [
                            {
                                "source": "skills/example-review",
                                "target": "skills/example-review",
                            },
                            {
                                "source": "scripts/example_tool.py",
                                "target": "scripts/example_tool.py",
                            },
                        ],
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return skill_source, script_source


def inspect(repo_root: Path, codex_home: Path, path: Path) -> dict[str, object]:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--json",
            "--repo-root",
            str(repo_root),
            "--codex-home",
            str(codex_home),
            str(path),
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(completed.stdout)[0]


def test_linked_target_reports_installed_owner() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repo_root = root / "repo"
        codex_home = root / "codex-home"
        skill_source, _ = write_manifest(repo_root)
        target = codex_home / "skills" / "example-review"
        target.parent.mkdir(parents=True)
        target.symlink_to(skill_source)

        result = inspect(repo_root, codex_home, target)

        assert result["manifest_owner"] == "codex-config"
        assert result["installed_owner"] == "codex-config"
        assert result["owner"] == "codex-config"
        assert result["status"] == "linked"
        assert result["feature"] == "example-tools"
        assert result["changelog_required"] is True


def test_missing_target_reports_manifest_owner_only() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repo_root = root / "repo"
        codex_home = root / "codex-home"
        write_manifest(repo_root)
        target = codex_home / "skills" / "example-review"

        result = inspect(repo_root, codex_home, target)

        assert result["manifest_owner"] == "codex-config"
        assert result["installed_owner"] is None
        assert result["owner"] is None
        assert result["status"] == "missing"


def test_repo_source_path_remains_repo_owned() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repo_root = root / "repo"
        codex_home = root / "codex-home"
        skill_source, _ = write_manifest(repo_root)

        result = inspect(repo_root, codex_home, skill_source)

        assert result["owner"] == "codex-config"
        assert result["manifest_owner"] == "codex-config"
        assert result["git_status_required"] is True


def test_wrong_symlink_is_not_claimed_as_installed() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repo_root = root / "repo"
        codex_home = root / "codex-home"
        write_manifest(repo_root)
        other = root / "other"
        other.mkdir()
        target = codex_home / "skills" / "example-review"
        target.parent.mkdir(parents=True)
        target.symlink_to(other)

        result = inspect(repo_root, codex_home, target)

        assert result["installed_owner"] is None
        assert result["owner"] is None
        assert result["status"] == "wrong_symlink"


def test_unmanaged_path_is_reported_without_repo_claim() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repo_root = root / "repo"
        codex_home = root / "codex-home"
        write_manifest(repo_root)
        unmanaged = codex_home / "vendor" / "thing"

        result = inspect(repo_root, codex_home, unmanaged)

        assert result["owner"] is None
        assert result["manifest_owner"] is None
        assert result["status"] == "unmanaged"


def test_file_and_directory_conflicts_are_distinguished() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repo_root = root / "repo"
        codex_home = root / "codex-home"
        _, script_source = write_manifest(repo_root)

        directory_target = codex_home / "skills" / "example-review"
        directory_target.parent.mkdir(parents=True)
        directory_target.write_text("conflict\n", encoding="utf-8")
        file_target = codex_home / "scripts" / "example_tool.py"
        file_target.mkdir(parents=True)

        directory_result = inspect(repo_root, codex_home, directory_target)
        file_result = inspect(repo_root, codex_home, file_target)

        assert script_source.is_file()
        assert directory_result["status"] == "conflict_file"
        assert file_result["status"] == "conflict_directory"
