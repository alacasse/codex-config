from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerRunLoopTests(ArchitectureProgramRunnerTestCase):
    def test_create_spec_done_when_execute_batches_false(self) -> None:
        config = runner.RunnerConfig(
            **{**self.config.__dict__, "execute_batches": False}
        )
        state = runner.initial_state(config)
        result = self.make_result("create-spec", "done")

        runner.validate_phase_result(result, current_phase="create-spec", state=state)

    def test_batches_completed_increments_only_after_closeout(self) -> None:
        state = runner.initial_state(self.config)
        execute_result = self.make_result("execute", "closeout")
        closeout_result = self.make_result("closeout", "done")

        runner.apply_phase_result(state, execute_result)
        self.assertEqual(state["batches_completed"], 0)

        runner.apply_phase_result(state, closeout_result)
        self.assertEqual(state["batches_completed"], 1)

    def test_final_summary_uses_state_and_last_receipt(self) -> None:
        result = self.make_result(
            "execute",
            "closeout",
            commit_range="abc123..def456",
            validation_summary="tests passed",
            review_summary="review clean",
        )
        self.write_receipt(result)
        state = runner.initial_state(self.config)
        state["last_receipt_path"] = result["receipt_path"]
        state["stop_reason"] = "done"
        state["batches_completed"] = 1
        state["active_batch_id"] = result["batch_id"]
        state["dispatch_path"] = result["dispatch_path"]
        state["spec_path"] = result["spec_path"]

        summary = runner.build_final_summary(state, self.config)

        self.assertEqual(summary["state_path"], str(self.config.state_path))
        self.assertIsNone(summary["artifact_root"])
        self.assertEqual(summary["last_receipt_path"], result["receipt_path"])
        self.assertEqual(summary["commit_range"], "abc123..def456")
        self.assertEqual(summary["validation_summary"], "tests passed")
        self.assertEqual(summary["review_summary"], "review clean")

    def test_unbounded_mode_stops_when_closeout_reports_no_next_batch(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        results = [
            self.make_result("select-dispatch", "create-spec"),
            self.make_result("create-spec", "execute"),
            self.make_result("execute", "closeout"),
            self.make_result("closeout", "done"),
        ]
        for result in results:
            self.write_receipt(result)

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            result = results.pop(0)
            if result["dispatch_path"]:
                self.touch_project_path(result["dispatch_path"])
            if result["spec_path"]:
                self.touch_project_path(result["spec_path"])
            return result

        final_state = runner.run(
            config,
            phase_executor=fake_executor,
            status_reader=lambda project: [],
        )

        self.assertEqual(final_state["batches_completed"], 1)
        self.assertEqual(final_state["stop_reason"], "done")

    def test_unbounded_mode_continues_after_closeout_when_next_batch_ready(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        first = self.make_result("select-dispatch", "create-spec", batch_id="batch-1")
        closeout = self.make_result("closeout", "select-dispatch", batch_id="batch-1")
        second = self.make_result(
            "select-dispatch",
            "stopped",
            status="stopped",
            stop_reason="no safe executable batch remains",
            batch_id=None,
            dispatch_path=None,
            spec_path=None,
            receipt_path="project-notes/architecture/receipts/select-dispatch-2.json",
        )
        sequence = [
            first,
            self.make_result("create-spec", "execute", batch_id="batch-1"),
            self.make_result("execute", "closeout", batch_id="batch-1"),
            closeout,
            second,
        ]
        for result in sequence:
            self.write_receipt(result)

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            result = sequence.pop(0)
            if result["dispatch_path"]:
                self.touch_project_path(result["dispatch_path"])
            if result["spec_path"]:
                self.touch_project_path(result["spec_path"])
            return result

        final_state = runner.run(
            config,
            phase_executor=fake_executor,
            status_reader=lambda project: [],
        )

        self.assertEqual(final_state["batches_completed"], 1)
        self.assertEqual(final_state["active_phase"], "select-dispatch")
        self.assertEqual(final_state["stop_reason"], "no safe executable batch remains")

    def test_unbounded_mode_stops_on_phase_failure(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        result = self.make_result(
            "select-dispatch",
            "stopped",
            status="failed",
            stop_reason="malformed ledger state",
            batch_id=None,
            dispatch_path=None,
            spec_path=None,
        )
        self.write_receipt(result)

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            return result

        final_state = runner.run(
            config,
            phase_executor=fake_executor,
            status_reader=lambda project: [],
        )

        self.assertEqual(final_state["stop_reason"], "malformed ledger state")
        self.assertEqual(final_state["last_phase_status"], "failed")

    def test_unbounded_mode_stops_on_validation_blocker(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        state = runner.initial_state(config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "project-notes/architecture/dispatch/batch-1.md"
        state["spec_path"] = "project-notes/architecture/batch-1-spec.md"
        self.touch_project_path(state["dispatch_path"])
        self.touch_project_path(state["spec_path"])
        runner.write_state(config.state_path, state)
        result = self.make_result(
            "execute",
            "stopped",
            status="stopped",
            stop_reason="validation failed",
            validation_summary="unit tests failed",
        )
        self.write_receipt(result)

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            return result

        final_state = runner.run(
            runner.RunnerConfig(**{**config.__dict__, "resume": True}),
            phase_executor=fake_executor,
            status_reader=lambda project: [],
        )

        self.assertEqual(final_state["stop_reason"], "validation failed")
        self.assertEqual(final_state["last_phase_status"], "stopped")

    def test_resume_terminal_done_state_does_not_rewrite_stop_reason(self) -> None:
        state = runner.initial_state(self.config)
        state["batches_completed"] = 1
        state["active_phase"] = "closeout"
        state["last_phase_status"] = "completed"
        state["stop_reason"] = "done"
        runner.write_state(self.config.state_path, state)

        def fail_if_called(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            self.fail("terminal state should not launch another phase")

        final_state = runner.run(
            runner.RunnerConfig(**{**self.config.__dict__, "resume": True}),
            phase_executor=fail_if_called,
            status_reader=lambda project: [],
        )

        self.assertEqual(final_state["stop_reason"], "done")
        self.assertEqual(
            runner.load_state(self.config.state_path)["stop_reason"],
            "done",
        )

    def test_stop_after_phase_runs_named_phase_then_persists_next_phase(self) -> None:
        result = self.make_result("select-dispatch", "create-spec")
        self.write_receipt(result)
        calls: list[str] = []

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            calls.append(phase)
            return result

        config = runner.RunnerConfig(
            **{**self.config.__dict__, "stop_after_phase": "select-dispatch"}
        )

        final_state = runner.run(
            config,
            phase_executor=fake_executor,
            status_reader=lambda project: [],
        )

        self.assertEqual(calls, ["select-dispatch"])
        self.assertEqual(final_state["active_phase"], "create-spec")
        self.assertEqual(runner.load_state(config.state_path)["active_phase"], "create-spec")

    def test_missing_receipt_stops_safely_and_persists_state(self) -> None:
        result = self.make_result("select-dispatch", "create-spec")

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            return result

        with self.assertRaisesRegex(runner.RunnerError, "not found"):
            runner.run(
                self.config,
                phase_executor=fake_executor,
                status_reader=lambda project: [],
            )

        state = runner.load_state(self.config.state_path)
        self.assertEqual(state["last_phase_status"], "failed")
        self.assertIn("not found", state["stop_reason"])

    def test_post_execute_unexpected_dirty_project_file_stops_before_closeout(self) -> None:
        result = self.make_result("execute", "closeout")
        self.write_receipt(result)
        state = runner.initial_state(self.config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = result["dispatch_path"]
        state["spec_path"] = result["spec_path"]
        runner.resolve_project_path(self.config.project, result["dispatch_path"]).parent.mkdir(
            parents=True, exist_ok=True
        )
        runner.resolve_project_path(self.config.project, result["dispatch_path"]).write_text(
            "dispatch\n", encoding="utf-8"
        )
        runner.resolve_project_path(self.config.project, result["spec_path"]).write_text(
            "spec\n", encoding="utf-8"
        )
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

    def test_resume_missing_dispatch_artifact_stops(self) -> None:
        state = runner.initial_state(self.config)
        state["active_phase"] = "create-spec"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "project-notes/architecture/dispatch/missing.md"
        runner.write_state(self.config.state_path, state)

        with self.assertRaisesRegex(runner.RunnerError, "dispatch_path does not exist"):
            runner.run(
                runner.RunnerConfig(**{**self.config.__dict__, "resume": True}),
                phase_executor=lambda config, state, phase: {},
                status_reader=lambda project: [],
            )
        stopped = runner.load_state(self.config.state_path)
        self.assertEqual(stopped["last_phase_status"], "failed")

    def test_resume_matching_artifact_can_continue(self) -> None:
        result = self.make_result("create-spec", "execute")
        self.write_receipt(result)
        dispatch = runner.resolve_project_path(self.config.project, result["dispatch_path"])
        dispatch.parent.mkdir(parents=True, exist_ok=True)
        dispatch.write_text("dispatch\n", encoding="utf-8")
        state = runner.initial_state(self.config)
        state["active_phase"] = "create-spec"
        state["active_batch_id"] = result["batch_id"]
        state["dispatch_path"] = result["dispatch_path"]
        runner.write_state(self.config.state_path, state)

        def fake_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            return result

        final_state = runner.run(
            runner.RunnerConfig(
                **{**self.config.__dict__, "resume": True, "stop_after_phase": "create-spec"}
            ),
            phase_executor=fake_executor,
            status_reader=lambda project: [],
        )

        self.assertEqual(final_state["active_phase"], "execute")

    def test_resume_contradictory_artifact_state_stops(self) -> None:
        state = runner.initial_state(self.config)
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "project-notes/architecture/dispatch/batch-1.md"
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            dispatch_path="project-notes/architecture/dispatch/other.md",
        )

        with self.assertRaisesRegex(runner.RunnerError, "dispatch_path contradicts"):
            runner.validate_phase_result(result, current_phase="select-dispatch", state=state)

if __name__ == "__main__":
    import unittest

    unittest.main()
