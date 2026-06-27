from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
from typing import Any
from unittest import mock

from scripts import architecture_program_runner_change_allowance as change_allowance_owner
from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner
from scripts import architecture_program_runner_phase_contract as phase_contract_owner
from scripts import architecture_program_runner_transition as transition_owner
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
