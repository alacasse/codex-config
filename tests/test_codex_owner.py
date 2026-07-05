from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "codex_owner.py"


class CodexOwnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.repo_root = self.root / "repo"
        self.codex_home = self.root / "codex-home"
        self.source = self.repo_root / "skills" / "batch-runway"
        self.target = self.codex_home / "skills" / "batch-runway"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text("# Batch Runway\n", encoding="utf-8")
        (self.repo_root / "codex-features.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "features": {
                        "batch-runway": {
                            "version": "1.0.0",
                            "links": [
                                {
                                    "source": "skills/batch-runway",
                                    "target": "skills/batch-runway",
                                }
                            ],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_planning_state_manifest(self) -> tuple[Path, Path]:
        skill_source = self.repo_root / "skills" / "planning-state"
        script_source = self.repo_root / "scripts" / "planning_state.py"
        skill_source.mkdir(parents=True)
        script_source.parent.mkdir(parents=True)
        (skill_source / "SKILL.md").write_text("# Planning State\n", encoding="utf-8")
        script_source.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        (self.repo_root / "codex-features.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "features": {
                        "planning-state": {
                            "version": "1.0.0",
                            "requires": ["planning-artifacts"],
                            "links": [
                                {
                                    "source": "skills/planning-state",
                                    "target": "skills/planning-state",
                                },
                                {
                                    "source": "scripts/planning_state.py",
                                    "target": "scripts/planning_state.py",
                                },
                            ],
                        },
                        "planning-artifacts": {
                            "version": "1.0.0",
                            "links": [
                                {
                                    "source": "skills/planning-artifacts",
                                    "target": "skills/planning-artifacts",
                                }
                            ],
                        },
                    },
                }
            ),
            encoding="utf-8",
        )
        return skill_source, script_source

    def inspect(self, path: Path) -> dict[str, object]:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--json",
                "--repo-root",
                str(self.repo_root),
                "--codex-home",
                str(self.codex_home),
                str(path),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        return json.loads(completed.stdout)[0]

    def test_linked_target_reports_installed_owner(self) -> None:
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.source)

        result = self.inspect(self.target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertEqual(result["installed_owner"], "codex-config")
        self.assertEqual(result["owner"], "codex-config")
        self.assertEqual(result["status"], "linked")
        self.assertTrue(result["changelog_required"])
        self.assertTrue(result["git_status_required"])

    def test_missing_target_reports_manifest_owner_only(self) -> None:
        result = self.inspect(self.target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertIsNone(result["installed_owner"])
        self.assertIsNone(result["owner"])
        self.assertEqual(result["status"], "missing")
        self.assertFalse(result["changelog_required"])
        self.assertFalse(result["git_status_required"])

    def test_unlinked_directory_copy_reports_manifest_owner_only(self) -> None:
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text("# Batch Runway\n", encoding="utf-8")

        result = self.inspect(self.target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertIsNone(result["installed_owner"])
        self.assertIsNone(result["owner"])
        self.assertEqual(result["status"], "unlinked_copy")
        self.assertIn("not linked", str(result["reason"]))

    def test_wrong_symlink_reports_manifest_owner_only(self) -> None:
        other = self.root / "other"
        other.mkdir()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(other)

        result = self.inspect(self.target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertIsNone(result["installed_owner"])
        self.assertEqual(result["status"], "wrong_symlink")

    def test_file_at_directory_target_reports_file_conflict(self) -> None:
        self.target.parent.mkdir(parents=True)
        self.target.write_text("not a directory\n", encoding="utf-8")

        result = self.inspect(self.target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertEqual(result["status"], "conflict_file")
        self.assertIsNone(result["installed_owner"])

    def test_directory_at_file_target_reports_directory_conflict(self) -> None:
        file_source = self.repo_root / "AGENTS.md"
        file_source.write_text("instructions\n", encoding="utf-8")
        (self.repo_root / "codex-features.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "features": {
                        "global-instructions": {
                            "version": "1.0.0",
                            "links": [{"source": "AGENTS.md", "target": "AGENTS.md"}],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        target = self.codex_home / "AGENTS.md"
        target.mkdir(parents=True)

        result = self.inspect(target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertEqual(result["status"], "conflict_directory")
        self.assertIsNone(result["installed_owner"])

    def test_repo_source_path_remains_repo_owned(self) -> None:
        result = self.inspect(self.source)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertEqual(result["owner"], "codex-config")
        self.assertEqual(result["status"], "missing")
        self.assertTrue(result["changelog_required"])
        self.assertTrue(result["git_status_required"])

    def test_planning_state_linked_skill_reports_installed_owner(self) -> None:
        skill_source, _ = self.write_planning_state_manifest()
        target = self.codex_home / "skills" / "planning-state"
        target.parent.mkdir(parents=True)
        target.symlink_to(skill_source)

        result = self.inspect(target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertEqual(result["installed_owner"], "codex-config")
        self.assertEqual(result["owner"], "codex-config")
        self.assertEqual(result["feature"], "planning-state")
        self.assertEqual(result["status"], "linked")

    def test_planning_state_linked_script_reports_installed_owner(self) -> None:
        _, script_source = self.write_planning_state_manifest()
        target = self.codex_home / "scripts" / "planning_state.py"
        target.parent.mkdir(parents=True)
        target.symlink_to(script_source)

        result = self.inspect(target)

        self.assertEqual(result["manifest_owner"], "codex-config")
        self.assertEqual(result["installed_owner"], "codex-config")
        self.assertEqual(result["owner"], "codex-config")
        self.assertEqual(result["feature"], "planning-state")
        self.assertEqual(result["status"], "linked")


if __name__ == "__main__":
    unittest.main()
