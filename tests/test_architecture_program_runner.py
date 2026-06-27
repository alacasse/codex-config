from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
from typing import Any
from unittest import mock

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerIntegrationTests(ArchitectureProgramRunnerTestCase):
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
        self.assertEqual(runner.sandbox_for_phase(config, "select-dispatch"), "workspace-write")
        self.assertEqual(runner.sandbox_for_phase(config, "execute"), "danger-full-access")

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

if __name__ == "__main__":
    import unittest

    unittest.main()
