from __future__ import annotations

from typing import Any

from scripts import architecture_program_runner_transition as transition_owner
from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerTransitionTests(ArchitectureProgramRunnerTestCase):
    def test_runner_facade_delegates_phase_transition_api_to_owner(self) -> None:
        self.assertIs(runner.apply_phase_result, transition_owner.apply_phase_transition)
        self.assertIs(runner.apply_phase_transition, transition_owner.apply_phase_transition)
        self.assertIs(
            runner.is_terminal_completed_state,
            transition_owner.is_terminal_phase_transition_state,
        )
        self.assertIs(
            runner.is_terminal_phase_transition_state,
            transition_owner.is_terminal_phase_transition_state,
        )

    def test_phase_transition_owner_does_not_own_validation_or_receipts(self) -> None:
        self.assertFalse(hasattr(transition_owner, "validate_phase_result"))
        self.assertFalse(hasattr(transition_owner, "expected_next_phases"))
        self.assertFalse(hasattr(transition_owner, "validate_receipt"))

    def test_execute_advances_to_closeout_without_completing_batch(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result("execute", "closeout")

        runner.apply_phase_result(state, result)

        self.assertEqual(state["active_phase"], "closeout")
        self.assertEqual(state["batches_completed"], 0)

    def test_closeout_advances_to_done_and_completes_batch(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result("closeout", "done")

        runner.apply_phase_result(state, result)

        self.assertEqual(state["batches_completed"], 1)
        self.assertEqual(state["stop_reason"], "done")

    def test_closeout_next_batch_resets_active_batch_paths(self) -> None:
        config = self.structured_config()
        state = runner.initial_state(config)
        select_result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path="project-notes/architecture/receipts/select-dispatch.json",
        )
        runner.apply_phase_result(state, select_result)

        closeout_result = self.make_result(
            "closeout",
            "select-dispatch",
            receipt_path="project-notes/architecture/receipts/closeout.json",
        )
        runner.apply_phase_result(state, closeout_result)

        self.assertEqual(state["batches_completed"], 1)
        self.assertEqual(state["active_phase"], "select-dispatch")
        self.assertIsNone(state["active_batch_id"])
        self.assertIsNone(state["dispatch_path"])
        self.assertIsNone(state["spec_path"])
        self.assertIsNone(state["active_batch_artifact_root"])
        self.assertIsNone(state["batch_manifest_path"])

    def test_resume_terminal_completed_states_do_not_launch_phase(self) -> None:
        for stop_reason in ("done", "max_batches_reached"):
            with self.subTest(stop_reason=stop_reason):
                state = runner.initial_state(self.config)
                state["batches_completed"] = 1
                state["active_phase"] = "closeout"
                state["last_phase_status"] = "completed"
                state["stop_reason"] = stop_reason
                runner.write_state(self.config.state_path, state)

                def fail_if_called(
                    config: Any, state: dict[str, Any], phase: str
                ) -> dict[str, Any]:
                    self.fail("terminal state should not launch another phase")

                final_state = runner.run(
                    runner.RunnerConfig(**{**self.config.__dict__, "resume": True}),
                    phase_executor=fail_if_called,
                    status_reader=lambda project: [],
                )

                self.assertEqual(final_state["stop_reason"], stop_reason)

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
