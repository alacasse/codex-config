from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner
from scripts import architecture_program_runner_phase_contract as phase_contract_owner
from tests.architecture_program_runner_test_support import runner


class ArchitectureProgramRunnerCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name) / "project"
        self.project.mkdir()
        self.config = runner.RunnerConfig(
            project=self.project.resolve(),
            program_ledger="project-notes/architecture/program.md",
            max_batches=1,
            execute_batches=True,
            state_path=self.project / "project-notes" / "architecture" / "run-state.json",
            sandbox="workspace-write",
            execute_sandbox=None,
            model=None,
            env_overrides=(),
            dry_run=False,
            resume=False,
            stop_after_phase=None,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_prompt_and_command_reuse_owner_produced_environment(self) -> None:
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "max_batches": None,
                "execute_sandbox": "danger-full-access",
            }
        )
        state = runner.initial_state(config)
        environment = environment_owner.build_phase_environment(config, state, "execute")

        with mock.patch.object(
            command_owner,
            "build_phase_environment",
            side_effect=AssertionError("environment should be supplied by caller"),
        ):
            prompt = command_owner.build_prompt(
                config,
                state,
                "execute",
                environment=environment,
            )
            command = command_owner.build_codex_command(
                config,
                "execute",
                prompt,
                Path("/tmp/result.json"),
                environment=environment,
            )

        self.assertIn("Batch limit: all executable batches", prompt)
        self.assertEqual(command[command.index("--sandbox") + 1], "danger-full-access")
        self.assertEqual(
            command[command.index("--output-schema") + 1],
            str(environment.schema_path),
        )

    def test_prompt_renders_phase_contract_with_phase_environment_facts(
        self,
    ) -> None:
        state = runner.initial_state(self.config)
        contract = phase_contract_owner.build_phase_contract("execute")

        prompt = command_owner.build_prompt(self.config, state, "execute")

        self.assertIn(f"Use {contract.skill_instruction}.", prompt)
        self.assertIn(contract.single_level_boundary_obligations[0], prompt)
        self.assertIn(contract.shared_result_obligations[0], prompt)
        self.assertIn(contract.phase_requirements[-1], prompt)
        self.assertIn("Batch limit: 1 batch", prompt)
        self.assertIn(f"Project path: {self.config.project}", prompt)

    def test_structured_prompt_names_expected_receipt_and_inventory_paths(self) -> None:
        artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "state_path": artifact_root / "run-state.json",
                "artifact_root": artifact_root,
            }
        )
        state = runner.initial_state(config)
        state["active_batch_id"] = "batch-1"
        state["active_batch_artifact_root"] = runner.batch_artifact_root(state, "batch-1")
        state["batch_manifest_path"] = runner.batch_manifest_path(state, "batch-1")

        prompt = command_owner.build_prompt(config, state, "execute")

        self.assertIn("Expected receipt path for this phase:", prompt)
        self.assertIn("Expected input inventory path for this phase:", prompt)
        self.assertIn(
            "batches/batch-1/receipts/03-execute.json",
            prompt,
        )
        self.assertIn("Prefer compact dispatch, receipt, manifest, and telemetry artifacts", prompt)

    def test_prompt_with_env_overrides_requires_coordinator_shell_probe(self) -> None:
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "env_overrides": (("UV_CACHE_DIR", "/tmp/graphify-uv-cache"),),
            }
        )
        prompt = command_owner.build_prompt(config, runner.initial_state(config), "execute")

        self.assertIn("Runner env override keys: UV_CACHE_DIR", prompt)
        self.assertNotIn("/tmp/graphify-uv-cache", prompt)
        self.assertIn("coordinator-shell environment probe", prompt)
        self.assertIn("key-present/readable-path booleans", prompt)
        self.assertIn("exact canonical command lines attempted", prompt)
        self.assertIn("present in the command environment", prompt)
        self.assertIn("path-like override values were readable", prompt)
        self.assertIn("do not treat subagent-only validation output as canonical", prompt)

    def test_prompt_generation_names_all_batches_limit(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        state = runner.initial_state(config)

        prompt = command_owner.build_prompt(config, state, "select-dispatch")

        self.assertIn("Batch limit: all executable batches", prompt)

    def test_codex_command_includes_schema_output_model_and_prompt(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "model": "gpt-5-codex"})

        command = command_owner.build_codex_command(
            config,
            "create-spec",
            "phase prompt",
            Path("/tmp/result.json"),
        )

        self.assertEqual(command[:4], ["codex", "exec", "--cd", str(config.project)])
        self.assertEqual(command[command.index("--sandbox") + 1], "workspace-write")
        self.assertEqual(command[command.index("--output-schema") + 1], str(runner.SCHEMA_PATH))
        self.assertEqual(command[command.index("--output-last-message") + 1], "/tmp/result.json")
        self.assertEqual(command[command.index("--model") + 1], "gpt-5-codex")
        self.assertEqual(command[-1], "phase prompt")

    def test_codex_command_uses_execute_only_sandbox_and_optional_model_flag(
        self,
    ) -> None:
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "execute_sandbox": "danger-full-access",
                "model": None,
            }
        )

        create_command = command_owner.build_codex_command(
            config,
            "create-spec",
            "create prompt",
            Path("/tmp/create-result.json"),
        )
        execute_command = command_owner.build_codex_command(
            config,
            "execute",
            "execute prompt",
            Path("/tmp/execute-result.json"),
        )

        self.assertEqual(
            create_command[create_command.index("--sandbox") + 1],
            "workspace-write",
        )
        self.assertEqual(
            execute_command[execute_command.index("--sandbox") + 1],
            "danger-full-access",
        )
        self.assertNotIn("--model", create_command)
        self.assertNotIn("--model", execute_command)
        self.assertEqual(
            execute_command[execute_command.index("--output-last-message") + 1],
            "/tmp/execute-result.json",
        )

    def test_dry_run_displays_env_keys_without_values(self) -> None:
        secret_value = "secret-value"
        cache_path = "/tmp/cache-path-sentinel"
        config = runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "execute_sandbox": "danger-full-access",
                "env_overrides": (
                    ("CACHE_TOKEN", secret_value),
                    ("UV_CACHE_DIR", cache_path),
                ),
            }
        )
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            with mock.patch.object(
                command_owner,
                "build_phase_environment",
                wraps=command_owner.build_phase_environment,
            ) as build_environment:
                command_owner.print_dry_run(config, runner.initial_state(config))

        text = output.getvalue()
        self.assertEqual(build_environment.call_count, 1)
        self.assertIn("Env override keys: CACHE_TOKEN, UV_CACHE_DIR", text)
        self.assertIn("Execute sandbox: danger-full-access", text)
        self.assertNotIn(secret_value, text)
        self.assertNotIn(cache_path, text)

    def test_display_quoting_is_shell_like_without_exposing_env_values(self) -> None:
        joined = command_owner.shell_join(["codex", "exec", "prompt with 'quote'"])

        self.assertEqual(joined, "codex exec 'prompt with '\"'\"'quote'\"'\"''")
