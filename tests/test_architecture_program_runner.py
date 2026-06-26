from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
from typing import Any


SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "architecture_program_runner.py"
)
REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_RESULT_SCHEMA = (
    REPO_ROOT
    / "skills"
    / "architecture-program-runway"
    / "references"
    / "local-runner-phase-result.schema.json"
)
UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS = {
    "allOf",
    "anyOf",
    "oneOf",
    "not",
    "if",
    "then",
    "else",
}
spec = importlib.util.spec_from_file_location("architecture_program_runner", SCRIPT)
assert spec is not None
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["architecture_program_runner"] = runner
spec.loader.exec_module(runner)


def schema_keyword_paths(value: Any, path: str = "$") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS:
                paths.append(child_path)
            paths.extend(schema_keyword_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(schema_keyword_paths(child, f"{path}[{index}]"))
    return paths


def schema_subset_violations(value: Any, path: str = "$") -> list[str]:
    violations: list[str] = []
    if isinstance(value, dict):
        schema_type = value.get("type")
        schema_types = schema_type if isinstance(schema_type, list) else [schema_type]
        if "object" in schema_types and value.get("additionalProperties") is not False:
            violations.append(f"{path}: object schemas must set additionalProperties=false")
        if "array" in schema_types and "items" not in value:
            violations.append(f"{path}: array schemas must define items")
        for key, child in value.items():
            violations.extend(schema_subset_violations(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            violations.extend(schema_subset_violations(child, f"{path}[{index}]"))
    return violations


class ArchitectureProgramRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / "my-docs" / "plans").mkdir(parents=True)
        (self.project / "my-docs" / "plans" / "program.md").write_text(
            "# Program\n", encoding="utf-8"
        )
        self.config = runner.RunnerConfig(
            project=self.project.resolve(),
            program_ledger="my-docs/plans/program.md",
            max_batches=1,
            execute_batches=True,
            state_path=self.project / "my-docs" / "plans" / "run-state.json",
            sandbox="workspace-write",
            model=None,
            env_overrides=(),
            dry_run=False,
            resume=False,
            stop_after_phase=None,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def make_result(self, phase: str, next_phase: str, **overrides: Any) -> dict[str, Any]:
        result = {
            "status": "completed",
            "phase": phase,
            "next_phase": next_phase,
            "stop_reason": None,
            "program_ledger": self.config.program_ledger,
            "batch_id": "batch-1",
            "dispatch_path": "my-docs/plans/dispatch/batch-1.md",
            "spec_path": "my-docs/plans/batch-1-spec.md",
            "receipt_path": f"my-docs/plans/receipts/{phase}.json",
            "commit_range": None,
            "validation_summary": None,
            "review_summary": None,
            "evidence_paths": [],
        }
        result.update(overrides)
        return result

    def write_receipt(self, result: dict[str, Any]) -> None:
        path = runner.resolve_project_path(self.config.project, result["receipt_path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result), encoding="utf-8")

    def touch_project_path(self, value: str, content: str = "artifact\n") -> None:
        path = runner.resolve_project_path(self.config.project, value)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_cli_defaults_and_state_path(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "my-docs/plans/program.md",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(config.max_batches, 1)
        self.assertFalse(config.execute_batches)
        self.assertEqual(config.sandbox, "workspace-write")
        self.assertEqual(config.env_overrides, ())
        self.assertEqual(
            config.state_path,
            self.project.resolve()
            / "my-docs"
            / "plans"
            / "architecture-program-run-state.json",
        )

    def test_all_batches_cli_sets_unbounded_mode(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "my-docs/plans/program.md",
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
                        "my-docs/plans/program.md",
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
                "my-docs/plans/program.md",
                "--max-batches",
                "3",
            ]
        )
        config = runner.config_from_args(args)

        self.assertEqual(config.max_batches, 3)

    def test_cli_parses_one_env_override(self) -> None:
        args = runner.parse_args(
            [
                "--project",
                str(self.project),
                "--program-ledger",
                "my-docs/plans/program.md",
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
                "my-docs/plans/program.md",
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

    def test_cli_rejects_env_override_without_separator(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runner.parse_args(
                    [
                        "--project",
                        str(self.project),
                        "--program-ledger",
                        "my-docs/plans/program.md",
                        "--env",
                        "CACHE_DIR",
                    ]
                )

    def test_cli_rejects_env_override_with_empty_key(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                runner.parse_args(
                    [
                        "--project",
                        str(self.project),
                        "--program-ledger",
                        "my-docs/plans/program.md",
                        "--env",
                        "=/tmp/project-cache",
                    ]
                )

    def test_env_overrides_preserve_base_environment(self) -> None:
        env = runner.build_subprocess_env(
            (("OVERRIDE_ME", "new"), ("ADDED", "value")),
            base_env={"KEEP_ME": "yes", "OVERRIDE_ME": "old"},
        )

        self.assertEqual(env["KEEP_ME"], "yes")
        self.assertEqual(env["OVERRIDE_ME"], "new")
        self.assertEqual(env["ADDED"], "value")

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

    def test_state_round_trip_uses_json(self) -> None:
        state = runner.initial_state(self.config)

        runner.write_state(self.config.state_path, state)
        loaded = runner.load_state(self.config.state_path)

        self.assertEqual(loaded["runner_version"], "local-runner-v1")
        self.assertEqual(loaded["active_phase"], "select-dispatch")
        self.assertIsInstance(loaded["updated_at"], str)

    def test_prompt_generation_names_all_phase_contracts(self) -> None:
        state = runner.initial_state(self.config)

        prompts = {phase: runner.build_prompt(self.config, state, phase) for phase in runner.PHASES}

        self.assertIn("select-next-batch", prompts["select-dispatch"])
        self.assertIn("create-next-runway", prompts["create-spec"])
        self.assertIn("$batch-runway execute-spec", prompts["execute"])
        self.assertIn("closeout-runway", prompts["closeout"])
        for prompt in prompts.values():
            self.assertIn("Return schema-valid JSON", prompt)
            self.assertIn("receipt_path", prompt)

    def test_prompt_generation_names_all_batches_limit(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        state = runner.initial_state(config)

        prompt = runner.build_prompt(config, state, "select-dispatch")

        self.assertIn("Batch limit: all executable batches", prompt)

    def test_phase_result_schema_uses_codex_output_subset(self) -> None:
        schema = json.loads(PHASE_RESULT_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(
            schema["required"],
            list(runner.REQUIRED_RESULT_FIELDS),
        )
        self.assertEqual(schema["additionalProperties"], False)
        self.assertEqual(
            schema_keyword_paths(schema),
            [],
        )
        self.assertEqual(
            schema_subset_violations(schema),
            [],
        )

    def test_local_runner_invocation_rule_lives_in_protocol(self) -> None:
        text = (
            REPO_ROOT
            / "skills"
            / "architecture-program-runway"
            / "references"
            / "local-runner-v1.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Local Runner Invocation Rule", text)
        self.assertIn("Invoke the local", text)
        self.assertIn("runner CLI instead", text)
        self.assertIn("--all-batches", text)
        self.assertIn("Final Summary Contract", text)

    def test_skill_points_local_runner_usage_to_protocol(self) -> None:
        text = (
            REPO_ROOT / "skills" / "architecture-program-runway" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("If the user asks to run the local architecture program runner", text)
        self.assertIn("references/local-runner-v1.md", text)
        self.assertIn("Do not manually", text)

    def test_nullable_early_stopped_result_is_valid(self) -> None:
        result = self.make_result(
            "select-dispatch",
            "stopped",
            status="stopped",
            stop_reason="no ready batch",
            batch_id=None,
            dispatch_path=None,
            spec_path=None,
            commit_range=None,
            validation_summary=None,
            review_summary=None,
            evidence_paths=[],
        )

        runner.validate_phase_result(result, current_phase="select-dispatch")

    def test_invalid_status_and_next_phase_combination_fails(self) -> None:
        result = self.make_result("execute", "execute", status="failed")

        with self.assertRaisesRegex(runner.RunnerError, "status=failed"):
            runner.validate_phase_result(result, current_phase="execute")

    def test_invalid_next_phase_for_state_fails(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result("select-dispatch", "execute")

        with self.assertRaisesRegex(runner.RunnerError, "cannot advance"):
            runner.validate_phase_result(result, current_phase="select-dispatch", state=state)

    def test_missing_required_schema_field_fails(self) -> None:
        result = self.make_result("select-dispatch", "create-spec")
        del result["receipt_path"]

        with self.assertRaisesRegex(runner.RunnerError, "missing required"):
            runner.validate_phase_result(result)

    def test_invalid_summary_type_fails(self) -> None:
        result = self.make_result("execute", "closeout", validation_summary=7)

        with self.assertRaisesRegex(runner.RunnerError, "validation_summary"):
            runner.validate_phase_result(result)

    def test_structured_summary_type_fails(self) -> None:
        result = self.make_result("execute", "closeout", review_summary={"status": "clean"})

        with self.assertRaisesRegex(runner.RunnerError, "review_summary"):
            runner.validate_phase_result(result)

    def test_receipt_must_match_final_phase_result(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result("select-dispatch", "create-spec")
        self.write_receipt({**result, "batch_id": "different"})

        with self.assertRaisesRegex(runner.RunnerError, "does not match"):
            runner.validate_receipt(result, self.config, state)

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

        final_state = runner.run(config, phase_executor=fake_executor, status_reader=lambda project: [])

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
            receipt_path="my-docs/plans/receipts/select-dispatch-2.json",
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

        final_state = runner.run(config, phase_executor=fake_executor, status_reader=lambda project: [])

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

        final_state = runner.run(config, phase_executor=fake_executor, status_reader=lambda project: [])

        self.assertEqual(final_state["stop_reason"], "malformed ledger state")
        self.assertEqual(final_state["last_phase_status"], "failed")

    def test_unbounded_mode_stops_on_validation_blocker(self) -> None:
        config = runner.RunnerConfig(**{**self.config.__dict__, "max_batches": None})
        state = runner.initial_state(config)
        state["active_phase"] = "execute"
        state["active_batch_id"] = "batch-1"
        state["dispatch_path"] = "my-docs/plans/dispatch/batch-1.md"
        state["spec_path"] = "my-docs/plans/batch-1-spec.md"
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
            status_reader=lambda project: ["?? my-docs/"],
        )

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
        state["dispatch_path"] = "my-docs/plans/dispatch/missing.md"
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
        state["dispatch_path"] = "my-docs/plans/dispatch/batch-1.md"
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            dispatch_path="my-docs/plans/dispatch/other.md",
        )

        with self.assertRaisesRegex(runner.RunnerError, "dispatch_path contradicts"):
            runner.validate_phase_result(result, current_phase="select-dispatch", state=state)


if __name__ == "__main__":
    unittest.main()
