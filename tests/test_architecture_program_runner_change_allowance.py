from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts import architecture_program_runner_change_allowance as change_allowance
from scripts.plan_batch import execute_plan_batch
from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)
from tests.test_plan_batch import _request


class ArchitectureProgramRunnerChangeAllowanceTests(ArchitectureProgramRunnerTestCase):
    def prepare_completed_planning_transaction(
        self,
    ) -> tuple[Any, dict[str, Any], set[str], dict[str, Any]]:
        request = _request(self.project)
        queued = execute_plan_batch(request)
        self.assertEqual(queued["outcome"], "queued")
        transaction = request["transaction"]
        lineage = transaction["lineage"]

        def relative(value: object) -> str:
            self.assertIsInstance(value, str)
            return Path(str(value)).resolve().relative_to(self.project.resolve()).as_posix()

        current_path = relative(transaction["current_path"])
        transaction_path = relative(transaction["transaction_path"])
        dispatch_path = relative(lineage["dispatch_path"])
        runway_path = relative(lineage["runway_path"])
        ledger_path = relative(lineage["ledger_path"])
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "program_ledger": ledger_path,
            }
        )
        receipt = self.make_result(
            "select-dispatch",
            "create-spec",
            program_ledger=ledger_path,
            batch_id=lineage["batch_id"],
            dispatch_path=dispatch_path,
            spec_path=runway_path,
            evidence_paths=[transaction_path],
        )
        self.write_receipt(receipt)
        state = runner.initial_state(config)
        state["active_phase"] = "create-spec"
        state["active_batch_id"] = receipt["batch_id"]
        state["dispatch_path"] = dispatch_path
        state["spec_path"] = runway_path
        state["last_phase_status"] = "completed"
        state["last_receipt_path"] = receipt["receipt_path"]
        return (
            config,
            state,
            {current_path, dispatch_path, runway_path, transaction_path},
            request,
        )

    def test_change_allowance_owner_exposes_named_path_api(self) -> None:
        state = runner.initial_state(self.config)

        expected = change_allowance.expected_change_allowance_paths(
            self.config, state, "select-dispatch"
        )

        self.assertIn("project-notes/architecture/run-state.json", expected)
        self.assertIs(
            runner.expected_change_allowance_paths,
            change_allowance.expected_change_allowance_paths,
        )
        self.assertIs(runner.expected_dirty_paths, change_allowance.expected_dirty_paths)
        self.assertIs(runner.check_change_allowance, change_allowance.check_change_allowance)
        self.assertIs(
            runner.check_change_allowance_path,
            change_allowance.check_change_allowance_path,
        )
        self.assertIs(runner.check_worktree, change_allowance.check_worktree)
        self.assertIs(runner.git_status_lines, change_allowance.git_status_lines)

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

    def test_complete_plan_batch_transition_reaches_compatibility_create_spec(
        self,
    ) -> None:
        config, _, transaction_paths, request = (
            self.prepare_completed_planning_transaction()
        )
        transaction = request["transaction"]
        lineage = transaction["lineage"]

        def relative(value: object) -> str:
            return Path(str(value)).resolve().relative_to(self.project.resolve()).as_posix()

        selection = self.make_result(
            "select-dispatch",
            "create-spec",
            program_ledger=config.program_ledger,
            batch_id=lineage["batch_id"],
            dispatch_path=relative(lineage["dispatch_path"]),
            spec_path=relative(lineage["runway_path"]),
            evidence_paths=[relative(transaction["transaction_path"])],
        )
        observation = self.make_result(
            "create-spec",
            "execute",
            program_ledger=config.program_ledger,
            batch_id=lineage["batch_id"],
            dispatch_path=relative(lineage["dispatch_path"]),
            spec_path=relative(lineage["runway_path"]),
        )
        calls: list[str] = []

        def executor(config: Any, current: dict[str, Any], phase: str) -> dict[str, Any]:
            calls.append(phase)
            result = selection if phase == "select-dispatch" else observation
            self.write_receipt(result)
            return result

        status_calls = 0

        def status_reader(project: Path) -> list[str]:
            nonlocal status_calls
            status_calls += 1
            if status_calls == 1:
                return []
            return [f" M {path}" for path in sorted(transaction_paths)]

        config = runner.RunnerConfig(**{**config.__dict__, "stop_after_phase": "create-spec"})
        runner.write_state(config.state_path, runner.initial_state(config))
        final_state = runner.run(
            config,
            phase_executor=executor,
            status_reader=status_reader,
        )

        self.assertEqual(calls, ["select-dispatch", "create-spec"])
        self.assertEqual(final_state["active_phase"], "execute")

    def test_create_spec_accepts_only_exact_transaction_owned_planning_paths(
        self,
    ) -> None:
        config, state, expected, _ = self.prepare_completed_planning_transaction()

        self.assertTrue(
            expected.issubset(
                runner.expected_change_allowance_paths(config, state, "create-spec")
            )
        )
        runner.check_worktree(
            config,
            state,
            "create-spec",
            status_reader=lambda project: [f" M {path}" for path in sorted(expected)],
        )

    def test_create_spec_rejects_unrelated_planning_and_project_paths(self) -> None:
        config, state, _, _ = self.prepare_completed_planning_transaction()

        for unexpected in (
            "project-notes/architecture/unrelated.md",
            "graphify/core.py",
            "plans/",
        ):
            with self.subTest(unexpected=unexpected), self.assertRaisesRegex(
                runner.RunnerError, "dirty files"
            ):
                runner.check_worktree(
                    config,
                    state,
                    "create-spec",
                    status_reader=lambda project, path=unexpected: [f" M {path}"],
                )

    def test_schema_valid_transaction_cannot_nominate_unrelated_current_file(
        self,
    ) -> None:
        config, state, _, request = self.prepare_completed_planning_transaction()
        transaction = request["transaction"]
        canonical_current = Path(transaction["current_path"])
        canonical_transaction = Path(transaction["transaction_path"])
        unrelated_current = self.project / "README.md"
        unrelated_current.write_bytes(canonical_current.read_bytes())
        arbitrary_transaction = self.project / "plans" / "arbitrary.md"
        arbitrary_transaction.write_text(
            canonical_transaction.read_text(encoding="utf-8").replace(
                str(canonical_current), str(unrelated_current)
            ),
            encoding="utf-8",
        )
        self.assertIsNotNone(
            change_allowance._planning_transaction_record(arbitrary_transaction)
        )
        receipt_path = self.project / state["last_receipt_path"]
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["evidence_paths"] = ["plans/arbitrary.md"]
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

        with self.assertRaisesRegex(runner.RunnerError, "dirty files"):
            runner.check_worktree(
                config,
                state,
                "create-spec",
                status_reader=lambda project: [" M README.md"],
            )

    def test_execute_and_closeout_allowances_remain_unchanged(self) -> None:
        state = runner.initial_state(self.config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "project-notes/architecture/dispatch/batch-1.md"
        state["spec_path"] = "project-notes/architecture/batch-1-spec.md"
        state["last_phase_status"] = "stopped"
        state["last_receipt_path"] = "project-notes/architecture/receipts/execute.json"
        evidence_path = "tests/install_sandbox/test_install_target_selection.py"
        self.write_receipt(
            self.make_result(
                "execute",
                "stopped",
                status="stopped",
                stop_reason="validation blocked",
                receipt_path=state["last_receipt_path"],
                evidence_paths=[evidence_path],
            )
        )

        runner.check_worktree(
            self.config,
            state,
            "execute",
            status_reader=lambda project: [f" M {evidence_path}"],
        )
        closeout = runner.expected_change_allowance_paths(
            self.config, state, "closeout"
        )
        self.assertIn(self.config.program_ledger, closeout)
        self.assertIn(state["spec_path"], closeout)
        self.assertIn(state["last_receipt_path"], closeout)

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
