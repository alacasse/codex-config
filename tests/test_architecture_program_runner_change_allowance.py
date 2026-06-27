from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerChangeAllowanceTests(ArchitectureProgramRunnerTestCase):
    def test_dirty_status_parser_includes_both_sides_of_renames(self) -> None:
        dirty = runner.dirty_paths_from_status(
            [
                " M graphify/core.py",
                "R  docs/old.md -> docs/new.md",
                'R  "docs/quoted old.md" -> "docs/quoted new.md"',
            ]
        )

        self.assertEqual(
            dirty,
            [
                "graphify/core.py",
                "docs/old.md",
                "docs/new.md",
                "docs/quoted old.md",
                "docs/quoted new.md",
            ],
        )

    def test_preflight_dirty_worktree_allows_expected_state_path(self) -> None:
        state = runner.initial_state(self.config)

        runner.check_worktree(
            self.config,
            state,
            "select-dispatch",
            status_reader=lambda project: ["?? project-notes/"],
        )

    def test_preflight_dirty_worktree_allows_structured_artifact_root(self) -> None:
        config = self.structured_config()
        state = runner.initial_state(config)

        runner.check_worktree(
            config,
            state,
            "select-dispatch",
            status_reader=lambda project: [
                "?? project-notes/architecture/architecture-program-runs/program/"
                "run-20260626-204812/"
            ],
        )

    def test_preflight_dirty_worktree_allows_stopped_phase_evidence_paths(self) -> None:
        state = runner.initial_state(self.config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "project-notes/architecture/dispatch/batch-1.md"
        state["spec_path"] = "project-notes/architecture/batch-1-spec.md"
        state["last_phase_status"] = "stopped"
        state["last_receipt_path"] = "project-notes/architecture/receipts/execute.json"
        receipt = self.make_result(
            "execute",
            "stopped",
            status="stopped",
            stop_reason="validation blocked",
            receipt_path=state["last_receipt_path"],
            evidence_paths=[
                "tests/install_sandbox/test_install_target_selection.py",
                "tests/install_sandbox/test_install_target_harness_policy.py",
            ],
        )
        self.write_receipt(receipt)

        runner.check_worktree(
            self.config,
            state,
            "execute",
            status_reader=lambda project: [
                " M tests/install_sandbox/test_install_target_selection.py",
                " M tests/install_sandbox/test_install_target_harness_policy.py",
            ],
        )

    def test_execute_to_closeout_post_check_rejects_unexpected_project_files(self) -> None:
        result = self.make_result("execute", "closeout")
        self.write_receipt(result)
        state = runner.initial_state(self.config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = result["dispatch_path"]
        state["spec_path"] = result["spec_path"]
        self.touch_project_path(result["dispatch_path"], "dispatch\n")
        self.touch_project_path(result["spec_path"], "spec\n")
        runner.write_state(self.config.state_path, state)

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            return result

        status_calls = 0

        def status_reader(project: Path) -> list[str]:
            nonlocal status_calls
            status_calls += 1
            if status_calls == 1:
                return []
            return [" M graphify/core.py"]

        with self.assertRaisesRegex(runner.RunnerError, "dirty files"):
            runner.run(
                runner.RunnerConfig(**{**self.config.__dict__, "resume": True}),
                phase_executor=fake_executor,
                status_reader=status_reader,
            )
        self.assertEqual(status_calls, 2)

    def test_expected_directory_prefix_does_not_allow_unrelated_sibling(self) -> None:
        expected = {
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812"
        }

        self.assertTrue(
            runner.path_is_expected(
                "project-notes/architecture/architecture-program-runs/program/"
                "run-20260626-204812/telemetry/run-telemetry.json",
                expected,
            )
        )
        self.assertFalse(
            runner.path_is_expected(
                "project-notes/architecture/architecture-program-runs/program/"
                "run-20260626-204812-sibling/telemetry/run-telemetry.json",
                expected,
            )
        )
