from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest import mock

from scripts import architecture_program_runner_change_allowance as change_allowance_owner
from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner
from scripts import architecture_program_runner_phase_observation as observation_owner
from scripts import architecture_program_runner_phase_contract as phase_contract_owner
from scripts import architecture_program_runner_transition as transition_owner
from scripts import architecture_program_runner_workers as worker_owner
from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerIntegrationTests(ArchitectureProgramRunnerTestCase):
    def test_runner_facade_reexports_public_helpers_for_compatibility(self) -> None:
        self.assertIs(runner.build_prompt, command_owner.build_prompt)
        self.assertIs(runner.build_codex_command, command_owner.build_codex_command)
        self.assertIs(runner.print_dry_run, command_owner.print_dry_run)
        self.assertIs(runner.shell_join, command_owner.shell_join)
        self.assertIs(runner.quote_for_display, command_owner.quote_for_display)
        self.assertIs(runner.phase_skill_instruction, command_owner.phase_skill_instruction)
        self.assertIs(runner.PhaseContract, phase_contract_owner.PhaseContract)
        self.assertIs(runner.build_phase_contract, phase_contract_owner.build_phase_contract)
        self.assertIs(runner.SCHEMA_PATH, environment_owner.SCHEMA_PATH)
        self.assertIs(runner.RUNNER_REFERENCE_PATH, environment_owner.RUNNER_REFERENCE_PATH)
        self.assertIs(runner.build_phase_environment, environment_owner.build_phase_environment)
        self.assertIs(runner.sandbox_for_phase, environment_owner.sandbox_for_phase)
        self.assertIs(runner.batch_limit_label, environment_owner.batch_limit_label)
        self.assertIs(runner.build_subprocess_env, environment_owner.build_subprocess_env)
        self.assertIs(runner.env_override_key_label, environment_owner.env_override_key_label)
        self.assertIs(
            runner.PhaseExecutionObservation,
            observation_owner.PhaseExecutionObservation,
        )
        self.assertIs(
            runner.build_phase_execution_observation,
            observation_owner.build_phase_execution_observation,
        )
        self.assertIs(
            runner.discover_codex_session_path,
            observation_owner.discover_codex_session_path,
        )
        self.assertIs(
            runner.extract_codex_session_id,
            observation_owner.extract_codex_session_id,
        )
        self.assertIs(runner.apply_phase_result, transition_owner.apply_phase_transition)
        self.assertIs(runner.apply_phase_transition, transition_owner.apply_phase_transition)
        self.assertIs(
            runner.is_terminal_completed_state,
            transition_owner.is_terminal_phase_transition_state,
        )
        self.assertIs(runner.check_worktree, change_allowance_owner.check_worktree)
        self.assertIs(
            runner.check_change_allowance,
            change_allowance_owner.check_change_allowance,
        )
        self.assertIs(runner.CodexExecWorker, worker_owner.CodexExecWorker)
        self.assertIs(runner.execute_phase_with_worker, worker_owner.execute_phase_with_worker)

    def test_cli_defaults_and_state_path(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(config.max_batches, 1)
        self.assertFalse(config.execute_batches)
        self.assertEqual(config.sandbox, "workspace-write")
        self.assertIsNone(config.execute_sandbox)
        self.assertEqual(config.env_overrides, ())
        self.assertRegex(
            config.state_path.as_posix(),
            (
                r"/project-notes/architecture/architecture-program-runs/program/"
                r"run-\d{8}-\d{6}/run-state\.json$"
            ),
        )
        self.assertEqual(config.artifact_root, config.state_path.parent)

    def test_all_batches_cli_sets_unbounded_mode(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
                "--all-batches",
            ]
        )
        config = runner.config_from_args(args)

        self.assertIsNone(config.max_batches)

    def test_all_batches_conflicts_with_numeric_max(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runner.parse_args(
                    [
                        "--project",
                        str(self.project),
                        "--program-ledger",
                        "project-notes/architecture/program.md",
                        "--all-batches",
                        "--max-batches",
                        "1",
                    ]
                )

    def test_numeric_batch_count_sets_max_batches(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
                "--max-batches",
                "3",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(config.max_batches, 3)

    def test_direct_script_dry_run_preserves_facade_without_state_writes(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "architecture_program_runner.py",
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
                "--dry-run",
                "--env",
                "CACHE_TOKEN=secret-value",
            ],
            cwd=Path(runner.__file__).parent,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Command:\n", completed.stdout)
        self.assertIn("Prompt:\n", completed.stdout)
        self.assertIn("Env override keys: CACHE_TOKEN", completed.stdout)
        self.assertNotIn("secret-value", completed.stdout)
        self.assertNotIn("Final summary:", completed.stdout)
        self.assertFalse(
            (
                self.project
                / "project-notes"
                / "architecture"
                / "architecture-program-runs"
            ).exists()
        )
        self.assertFalse(
            (
                self.project
                / "project-notes"
                / "architecture"
                / "architecture-program-run-state.json"
            ).exists()
        )

    def test_execute_sandbox_overrides_execute_phase_only(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
                "--sandbox",
                "workspace-write",
                "--execute-sandbox",
                "danger-full-access",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(config.sandbox, "workspace-write")
        self.assertEqual(config.execute_sandbox, "danger-full-access")

    def test_cli_parses_one_env_override(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
                "--env",
                "CACHE_DIR=/tmp/project-cache",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(config.env_overrides, (("CACHE_DIR", "/tmp/project-cache"),))

    def test_cli_parses_multiple_env_overrides(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "project-notes/architecture/program.md",
                "--env",
                "CACHE_DIR=/tmp/project-cache",
                "--env",
                "EMPTY_VALUE=",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(
            config.env_overrides,
            (("CACHE_DIR", "/tmp/project-cache"), ("EMPTY_VALUE", "")),
        )

    def test_cli_rejects_malformed_env_overrides(self) -> None:
        for value in ("CACHE_DIR", "=/tmp/project-cache"):
            with self.subTest(value=value):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        runner.parse_args(
                            [
                                "--project",
                                str(self.project),
                                "--program-ledger",
                                "project-notes/architecture/program.md",
                                "--env",
                                value,
                            ]
                        )

    def test_execute_codex_phase_passes_env_overrides_to_subprocess(self) -> None:
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "env_overrides": (("OVERRIDE_ME", "new"), ("ADDED", "value")),
            }
        )
        state = runner.initial_state(config)
        result = self.make_result("select-dispatch", "create-spec")
        captured: dict[str, Any] = {}

        def fake_run(command: list[str], **kwargs: Any) -> Any:
            captured["env"] = kwargs["env"]
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text(json.dumps(result), encoding="utf-8")
            return runner.subprocess.CompletedProcess(command, 0, "", "")

        with mock.patch.dict(
            runner.os.environ,
            {"KEEP_ME": "yes", "OVERRIDE_ME": "old"},
            clear=True,
        ):
            with mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
                returned = runner.execute_codex_phase(config, state, "select-dispatch")

        self.assertEqual(returned, result)
        self.assertEqual(captured["env"]["KEEP_ME"], "yes")
        self.assertEqual(captured["env"]["OVERRIDE_ME"], "new")
        self.assertEqual(captured["env"]["ADDED"], "value")
        self.assertGreater(state["_phase_execution_meta"]["prompt_bytes"], 0)

    def test_execute_codex_phase_routes_through_worker_adapter(self) -> None:
        class FakeWorker:
            def __init__(self) -> None:
                self.calls: list[tuple[runner.RunnerConfig, dict[str, Any], str]] = []

            def run_phase(
                self,
                config: runner.RunnerConfig,
                state: dict[str, Any],
                phase: str,
            ) -> dict[str, Any]:
                self.calls.append((config, state, phase))
                return self_result

        state = runner.initial_state(self.config)
        self_result = self.make_result("select-dispatch", "create-spec")
        worker = FakeWorker()

        returned = runner.execute_codex_phase(
            self.config,
            state,
            "select-dispatch",
            worker=worker,
        )

        self.assertEqual(returned, self_result)
        self.assertEqual(worker.calls, [(self.config, state, "select-dispatch")])

    def test_shell_worker_result_uses_existing_validation_receipt_and_transition(
        self,
    ) -> None:
        config = self.structured_config()
        state = runner.initial_state(config)
        receipt_path = runner.phase_receipt_path(state, "select-dispatch")
        inventory_path = runner.phase_input_inventory_path(state, "select-dispatch")
        self.assertIsNotNone(receipt_path)
        self.assertIsNotNone(inventory_path)
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path=receipt_path,
            evidence_paths=[inventory_path],
        )
        script = self.project / "write_shell_phase_result.py"
        script.write_text(
            "\n".join(
                [
                    "import json, os",
                    "from pathlib import Path",
                    "result = json.loads(os.environ['PHASE_RESULT_JSON'])",
                    "output = Path(os.environ['ARCHITECTURE_PROGRAM_PHASE_RESULT_PATH'])",
                    "output.write_text(json.dumps(result), encoding='utf-8')",
                    "receipt = Path(os.environ['ARCHITECTURE_PROGRAM_PROJECT']) / result['receipt_path']",
                    "receipt.parent.mkdir(parents=True, exist_ok=True)",
                    "receipt.write_text(json.dumps(result), encoding='utf-8')",
                    "inventory = Path(os.environ['ARCHITECTURE_PROGRAM_PROJECT']) / os.environ['ARCHITECTURE_PROGRAM_EXPECTED_INPUT_INVENTORY_PATH']",
                    "inventory.parent.mkdir(parents=True, exist_ok=True)",
                    "inventory.write_text(json.dumps({'schema_version': 1, 'phase': os.environ['ARCHITECTURE_PROGRAM_PHASE'], 'primary_inputs': [], 'broad_reads': [], 'large_file_reads': [], 'subagent_reports': []}), encoding='utf-8')",
                ]
            ),
            encoding="utf-8",
        )
        shell_config = runner.RunnerConfig(
            **{
                **config.__dict__,
                "env_overrides": (("PHASE_RESULT_JSON", json.dumps(result)),),
            }
        )
        worker = worker_owner.ShellCommandWorker([sys.executable, str(script)])

        returned = worker.run_phase(shell_config, state, "select-dispatch")
        runner.validate_phase_result(returned, current_phase="select-dispatch", state=state)
        runner.validate_receipt(returned, shell_config, state)
        runner.apply_phase_result(state, returned)

        self.assertEqual(returned, result)
        self.assertEqual(state["active_phase"], "create-spec")
        self.assertEqual(state["active_batch_id"], "batch-1")

    def test_run_loop_shell_worker_does_not_need_codex_prompt_or_command(self) -> None:
        config = self.structured_config()
        state = runner.initial_state(config)
        receipt_path = runner.phase_receipt_path(state, "select-dispatch")
        inventory_path = runner.phase_input_inventory_path(state, "select-dispatch")
        self.assertIsNotNone(receipt_path)
        self.assertIsNotNone(inventory_path)
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path=receipt_path,
            evidence_paths=[inventory_path],
        )
        script = self.project / "write_shell_phase_result.py"
        script.write_text(
            "\n".join(
                [
                    "import json, os",
                    "from pathlib import Path",
                    "result = json.loads(os.environ['PHASE_RESULT_JSON'])",
                    "output = Path(os.environ['ARCHITECTURE_PROGRAM_PHASE_RESULT_PATH'])",
                    "output.write_text(json.dumps(result), encoding='utf-8')",
                    "receipt = Path(os.environ['ARCHITECTURE_PROGRAM_PROJECT']) / result['receipt_path']",
                    "receipt.parent.mkdir(parents=True, exist_ok=True)",
                    "receipt.write_text(json.dumps(result), encoding='utf-8')",
                    "inventory = Path(os.environ['ARCHITECTURE_PROGRAM_PROJECT']) / os.environ['ARCHITECTURE_PROGRAM_EXPECTED_INPUT_INVENTORY_PATH']",
                    "inventory.parent.mkdir(parents=True, exist_ok=True)",
                    "inventory.write_text(json.dumps({'schema_version': 1, 'phase': os.environ['ARCHITECTURE_PROGRAM_PHASE'], 'primary_inputs': [], 'broad_reads': [], 'large_file_reads': [], 'subagent_reports': []}), encoding='utf-8')",
                ]
            ),
            encoding="utf-8",
        )
        shell_config = runner.RunnerConfig(
            **{
                **config.__dict__,
                "env_overrides": (("PHASE_RESULT_JSON", json.dumps(result)),),
                "stop_after_phase": "select-dispatch",
            }
        )
        worker = worker_owner.ShellCommandWorker([sys.executable, str(script)])

        def phase_executor(
            config: runner.RunnerConfig,
            state: dict[str, Any],
            phase: str,
        ) -> dict[str, Any]:
            return worker.run_phase(config, state, phase)

        with (
            mock.patch.object(
                runner,
                "build_prompt",
                side_effect=AssertionError("prompt should not be built"),
            ),
            mock.patch.object(
                command_owner,
                "build_prompt",
                side_effect=AssertionError("prompt should not be built"),
            ),
            mock.patch.object(
                runner,
                "build_codex_command",
                side_effect=AssertionError("codex command should not be built"),
            ),
            mock.patch.object(
                command_owner,
                "build_codex_command",
                side_effect=AssertionError("codex command should not be built"),
            ),
        ):
            final_state = runner.run(
                shell_config,
                phase_executor=phase_executor,
                status_reader=lambda project: [],
            )

        self.assertEqual(final_state["active_phase"], "create-spec")
        self.assertEqual(final_state["last_phase_status"], "completed")

    def test_execute_codex_phase_uses_execute_sandbox_for_execute_only(self) -> None:
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "execute_sandbox": "danger-full-access",
            }
        )
        state = runner.initial_state(config)
        result = self.make_result("execute", "closeout")
        captured: list[list[str]] = []

        def fake_run(command: list[str], **kwargs: Any) -> Any:
            captured.append(command)
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text(json.dumps(result), encoding="utf-8")
            return runner.subprocess.CompletedProcess(command, 0, "", "")

        with mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
            returned = runner.execute_codex_phase(config, state, "execute")

        command = captured[0]
        self.assertEqual(returned, result)
        self.assertEqual(command[command.index("--sandbox") + 1], "danger-full-access")

    def test_dry_run_mentions_env_keys_without_values(self) -> None:
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "env_overrides": (("CACHE_TOKEN", "secret-value"),),
            }
        )
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            runner.print_dry_run(config, runner.initial_state(config))

        text = output.getvalue()
        self.assertIn("CACHE_TOKEN", text)
        self.assertNotIn("secret-value", text)

if __name__ == "__main__":
    import unittest

    unittest.main()
