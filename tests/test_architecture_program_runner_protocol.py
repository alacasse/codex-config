from __future__ import annotations

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    REPO_ROOT,
)


class ArchitectureProgramRunnerProtocolTests(ArchitectureProgramRunnerTestCase):
    def test_local_runner_invocation_rule_lives_in_protocol(self) -> None:
        text = (
            REPO_ROOT
            / "skills"
            / "architecture-program-runway"
            / "references"
            / "local-runner-v1.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Local Runner Invocation Rule", text)
        self.assertIn("Invoke the local", text)
        self.assertIn("runner CLI instead", text)
        self.assertIn("--all-batches", text)
        self.assertIn("Final Summary Contract", text)
        self.assertIn("phase coordinator shell", text)
        self.assertIn("Subagent-only validation output", text)
        self.assertIn("command environment", text)
        self.assertIn("--execute-sandbox", text)
        self.assertIn("commit-capable Batch Runway execution", text)
        self.assertIn("single-level", text)
        self.assertIn("Do not run `codex exec`", text)
        self.assertIn("file-based closeout telemetry", text)
        self.assertIn("## Input Inventory Contract", text)
        self.assertIn("evidence_paths", text)
        self.assertIn("not reconstruct", text)

    def test_skill_points_local_runner_usage_to_protocol(self) -> None:
        text = (
            REPO_ROOT / "skills" / "architecture-program-runway" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("If the user asks to run the local architecture program runner", text)
        self.assertIn("references/local-runner-v1.md", text)
        self.assertIn("Do not manually", text)

if __name__ == "__main__":
    import unittest

    unittest.main()
