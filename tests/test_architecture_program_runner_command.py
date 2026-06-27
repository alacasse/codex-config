from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts import architecture_program_runner as runner
from scripts import architecture_program_runner_command as command_owner


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

    def test_runner_reexports_command_owner_helpers_for_compatibility(self) -> None:
        self.assertIs(runner.build_prompt, command_owner.build_prompt)
        self.assertIs(runner.build_codex_command, command_owner.build_codex_command)
        self.assertIs(runner.sandbox_for_phase, command_owner.sandbox_for_phase)
        self.assertIs(runner.print_dry_run, command_owner.print_dry_run)

    def test_prompt_guardrails_and_phase_contracts_are_built_by_owner(self) -> None:
        state = runner.initial_state(self.config)

        prompts = {
            phase: command_owner.build_prompt(self.config, state, phase)
            for phase in runner.PHASES
        }

        self.assertIn("select-next-batch", prompts["select-dispatch"])
        self.assertIn("create-next-runway", prompts["create-spec"])
        self.assertIn("$batch-runway execute-spec", prompts["execute"])
        self.assertIn("closeout-runway", prompts["closeout"])
        for prompt in prompts.values():
            self.assertIn("Do not run codex exec", prompt)
            self.assertIn("Do not launch the local architecture program runner", prompt)
            self.assertIn("Return schema-valid JSON", prompt)
            self.assertIn("receipt_path", prompt)

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
        self.assertEqual(
            command_owner.batch_limit_label(None),
            "all executable batches until stop condition",
        )
        self.assertEqual(command_owner.batch_limit_label(1), "1 batch")
        self.assertEqual(command_owner.batch_limit_label(3), "3 batches")

    def test_execute_sandbox_applies_to_execute_phase_only(self) -> None:
        config = runner.RunnerConfig(
            **{**self.config.__dict__, "execute_sandbox": "danger-full-access"}
        )

        self.assertEqual(
            command_owner.sandbox_for_phase(config, "select-dispatch"),
            "workspace-write",
        )
        self.assertEqual(command_owner.sandbox_for_phase(config, "execute"), "danger-full-access")

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

    def test_subprocess_environment_applies_runner_overrides(self) -> None:
        env = command_owner.build_subprocess_env(
            (("OVERRIDE_ME", "new"), ("ADDED", "value")),
            base_env={"KEEP_ME": "yes", "OVERRIDE_ME": "old"},
        )

        self.assertEqual(env["KEEP_ME"], "yes")
        self.assertEqual(env["OVERRIDE_ME"], "new")
        self.assertEqual(env["ADDED"], "value")

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
            command_owner.print_dry_run(config, runner.initial_state(config))

        text = output.getvalue()
        self.assertIn("Env override keys: CACHE_TOKEN, UV_CACHE_DIR", text)
        self.assertIn("Execute sandbox: danger-full-access", text)
        self.assertNotIn(secret_value, text)
        self.assertNotIn(cache_path, text)

    def test_display_quoting_is_shell_like_without_exposing_env_values(self) -> None:
        joined = command_owner.shell_join(["codex", "exec", "prompt with 'quote'"])

        self.assertEqual(joined, "codex exec 'prompt with '\"'\"'quote'\"'\"''")
