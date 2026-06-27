from __future__ import annotations

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerWorktreeTests(ArchitectureProgramRunnerTestCase):
    def test_preflight_dirty_worktree_rejects_unexpected_path(self) -> None:
        state = runner.initial_state(self.config)

        with self.assertRaisesRegex(runner.RunnerError, "dirty files"):
            runner.check_worktree(
                self.config,
                state,
                "select-dispatch",
                status_reader=lambda project: [" M graphify/core.py"],
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

    def test_preflight_dirty_worktree_allows_stopped_receipt_after_preflight_failure(
        self,
    ) -> None:
        state = runner.initial_state(self.config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "project-notes/architecture/dispatch/batch-1.md"
        state["spec_path"] = "project-notes/architecture/batch-1-spec.md"
        state["last_phase_status"] = "failed"
        state["last_receipt_path"] = "project-notes/architecture/receipts/execute.json"
        receipt = self.make_result(
            "execute",
            "stopped",
            status="stopped",
            stop_reason="validation blocked",
            receipt_path=state["last_receipt_path"],
            evidence_paths=["tests/install_sandbox/test_install_target_selection.py"],
        )
        self.write_receipt(receipt)

        runner.check_worktree(
            self.config,
            state,
            "execute",
            status_reader=lambda project: [
                " M tests/install_sandbox/test_install_target_selection.py",
            ],
        )

if __name__ == "__main__":
    import unittest

    unittest.main()
