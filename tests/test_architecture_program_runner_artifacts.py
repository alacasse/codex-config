from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts import architecture_program_runner as runner
from scripts import architecture_program_runner_artifacts as artifacts


class ArchitectureProgramRunnerArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / "project-notes" / "architecture").mkdir(parents=True)
        (self.project / "project-notes" / "architecture" / "program.md").write_text(
            "# Program\n", encoding="utf-8"
        )
        self.artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        self.config = runner.RunnerConfig(
            project=self.project.resolve(),
            program_ledger="project-notes/architecture/program.md",
            max_batches=1,
            execute_batches=True,
            state_path=self.artifact_root / "run-state.json",
            sandbox="workspace-write",
            execute_sandbox=None,
            model=None,
            env_overrides=(),
            dry_run=False,
            resume=False,
            stop_after_phase=None,
            artifact_root=self.artifact_root,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def touch_project_path(self, value: str, content: str = "artifact\n") -> None:
        path = runner.resolve_project_path(self.project, value)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def make_result(self, phase: str = "select-dispatch") -> dict[str, Any]:
        return {
            "status": "completed",
            "phase": phase,
            "next_phase": "create-spec",
            "stop_reason": None,
            "program_ledger": self.config.program_ledger,
            "batch_id": "batch-1",
            "dispatch_path": "project-notes/architecture/dispatch/batch-1.md",
            "spec_path": "project-notes/architecture/batch-1-spec.md",
            "receipt_path": f"project-notes/architecture/receipts/{phase}.json",
            "commit_range": None,
            "validation_summary": None,
            "review_summary": None,
            "evidence_paths": [],
        }

    def write_session_jsonl(self, name: str, *records: dict[str, Any]) -> str:
        path = self.root / name
        path.write_text(
            "\n".join(json.dumps(record) for record in records),
            encoding="utf-8",
        )
        return str(path)

    def test_batch_manifest_records_receipts_and_telemetry(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result()

        runner.apply_phase_result(state, result)
        telemetry_path = runner.next_phase_telemetry_path(state, "select-dispatch")
        artifacts.record_phase_telemetry_path(state, telemetry_path, result)
        manifest = artifacts.build_batch_manifest(state, "batch-1")

        self.assertEqual(manifest["dispatch_path"], result["dispatch_path"])
        self.assertEqual(manifest["receipts"]["select-dispatch"], result["receipt_path"])
        expected_telemetry = (
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/telemetry/phases/01-select-dispatch.telemetry.json"
        )
        self.assertEqual(
            manifest["telemetry"]["select-dispatch"],
            expected_telemetry,
        )
        self.assertEqual(manifest["status"], "completed")

    def test_token_summaries_cover_missing_and_context_pressure(self) -> None:
        missing = artifacts.summarize_token_events(self.root / "missing.jsonl")
        self.assertEqual(missing["status"], "missing")
        self.assertEqual(missing["context_pressure"], "missing")

        session = self.root / "session.jsonl"
        session.write_text(
            json.dumps(
                {
                    "payload": {
                        "type": "token_count",
                        "last_token_usage": {"input_tokens": 900, "cached_input_tokens": 20},
                        "total_token_usage": {
                            "input_tokens": 1000,
                            "output_tokens": 50,
                            "reasoning_output_tokens": 30,
                        },
                        "model_context_window": 1000,
                    }
                }
            ),
            encoding="utf-8",
        )

        summary = artifacts.summarize_token_events(session)

        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["max_context_used_percent"], 90.0)
        self.assertEqual(summary["context_pressure"], "context_stop_recommended")
        self.assertEqual(artifacts.context_budget_summary("execute", summary)["status"], "ok")

    def test_phase_telemetry_includes_artifact_size_entries(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result()
        self.touch_project_path(result["dispatch_path"], "dispatch\n")

        telemetry = artifacts.build_phase_telemetry(
            self.config,
            state,
            "select-dispatch",
            started_at="2026-06-26T20:48:12Z",
            elapsed_seconds=0.25,
            prompt_bytes=12,
            result=result,
            status="completed",
            error=None,
            execution_meta={"exit_code": 0},
        )

        sizes = {entry["path"]: entry for entry in telemetry["artifact_sizes"]}
        self.assertTrue(sizes[self.config.program_ledger]["exists"])
        self.assertEqual(sizes[result["dispatch_path"]]["bytes"], len("dispatch\n"))
        self.assertFalse(sizes[result["receipt_path"]]["exists"])

    def test_phase_telemetry_consumes_supplied_observation_metadata(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result("execute")
        session_path = self.write_session_jsonl(
            "execute-session.jsonl",
            {
                "payload": {
                    "type": "token_count",
                    "last_token_usage": {
                        "input_tokens": 6000,
                        "cached_input_tokens": 800,
                    },
                    "total_token_usage": {
                        "input_tokens": 6500,
                        "output_tokens": 250,
                        "reasoning_output_tokens": 75,
                    },
                    "model_context_window": 10000,
                }
            },
            {
                "payload": {
                    "type": "token_count",
                    "last_token_usage": {
                        "input_tokens": 8400,
                        "cached_input_tokens": 1200,
                    },
                    "total_token_usage": {
                        "input_tokens": 9000,
                        "output_tokens": 500,
                        "reasoning_output_tokens": 100,
                    },
                    "model_context_window": 10000,
                }
            },
        )

        telemetry = artifacts.build_phase_telemetry(
            self.config,
            state,
            "execute",
            started_at="2026-06-27T12:00:00Z",
            elapsed_seconds=1.25,
            prompt_bytes=512,
            result=result,
            status="completed",
            error=None,
            execution_meta={
                "exit_code": 0,
                "stdout_bytes": 42,
                "stderr_bytes": 7,
                "codex_session_id": "019f0679-3875-7601-a4f8-a2a22303f3c7",
                "codex_session_path": session_path,
            },
        )

        self.assertEqual(telemetry["codex_session_path"], session_path)
        self.assertEqual(telemetry["token_summary"]["status"], "ok")
        self.assertEqual(telemetry["token_summary"]["turn_count"], 2)
        self.assertEqual(telemetry["token_summary"]["max_input_tokens"], 8400)
        self.assertEqual(telemetry["token_summary"]["max_context_used_percent"], 84.0)
        self.assertEqual(telemetry["token_summary"]["context_pressure"], "context_pressure")
        self.assertEqual(telemetry["context_budget"]["max_input_tokens"], 8400)

    def test_phase_telemetry_keeps_missing_session_attribution_non_fatal(self) -> None:
        state = runner.initial_state(self.config)
        result = self.make_result("execute")

        telemetry = artifacts.build_phase_telemetry(
            self.config,
            state,
            "execute",
            started_at="2026-06-27T12:00:00Z",
            elapsed_seconds=1.25,
            prompt_bytes=512,
            result=result,
            status="completed",
            error=None,
            execution_meta={
                "exit_code": 0,
                "stdout_bytes": 0,
                "stderr_bytes": 0,
                "codex_session_id": None,
                "codex_session_path": None,
            },
        )

        self.assertIsNone(telemetry["codex_session_id"])
        self.assertIsNone(telemetry["codex_session_path"])
        self.assertEqual(telemetry["token_summary"]["status"], "missing")
        self.assertEqual(telemetry["token_summary"]["context_pressure"], "missing")
        self.assertEqual(telemetry["context_budget"]["status"], "missing")

    def test_run_telemetry_aggregates_session_ids_and_token_summaries(self) -> None:
        state = runner.initial_state(self.config)
        select_result = self.make_result("select-dispatch")
        execute_result = self.make_result("execute")
        select_session_path = self.write_session_jsonl(
            "select-session.jsonl",
            {
                "payload": {
                    "type": "token_count",
                    "last_token_usage": {"input_tokens": 3500},
                    "total_token_usage": {"input_tokens": 3500, "output_tokens": 20},
                    "model_context_window": 10000,
                }
            },
        )
        execute_session_path = self.write_session_jsonl(
            "execute-session.jsonl",
            {
                "payload": {
                    "type": "token_count",
                    "last_token_usage": {"input_tokens": 9100},
                    "total_token_usage": {"input_tokens": 9100, "output_tokens": 80},
                    "model_context_window": 10000,
                }
            },
        )
        cases = [
            (
                "select-dispatch",
                select_result,
                "019f0679-3875-7601-a4f8-a2a22303f3d0",
                select_session_path,
            ),
            (
                "execute",
                execute_result,
                "019f0679-3875-7601-a4f8-a2a22303f3d1",
                execute_session_path,
            ),
        ]

        for phase, result, session_id, session_path in cases:
            telemetry = artifacts.build_phase_telemetry(
                self.config,
                state,
                phase,
                started_at="2026-06-27T12:00:00Z",
                elapsed_seconds=1.0,
                prompt_bytes=512,
                result=result,
                status="completed",
                error=None,
                execution_meta={
                    "exit_code": 0,
                    "stdout_bytes": 0,
                    "stderr_bytes": 0,
                    "codex_session_id": session_id,
                    "codex_session_path": session_path,
                },
            )
            telemetry_path = runner.next_phase_telemetry_path(state, phase)
            artifacts.write_phase_telemetry(self.config, telemetry_path, telemetry)
            artifacts.record_phase_telemetry_path(state, telemetry_path, result)

        artifacts.write_run_telemetry(self.config, state)

        run_telemetry = runner.read_json_object(
            self.artifact_root / "telemetry" / "run-telemetry.json"
        )
        self.assertEqual(run_telemetry["phase_count"], 2)
        self.assertEqual(run_telemetry["max_input_tokens"], 9100)
        self.assertEqual(run_telemetry["max_context_used_percent"], 91.0)
        self.assertEqual(run_telemetry["context_pressure"], "context_stop_recommended")
        self.assertEqual(
            [phase["codex_session_id"] for phase in run_telemetry["phases"]],
            [
                "019f0679-3875-7601-a4f8-a2a22303f3d0",
                "019f0679-3875-7601-a4f8-a2a22303f3d1",
            ],
        )
        self.assertEqual(
            [phase["max_input_tokens"] for phase in run_telemetry["phases"]],
            [3500, 9100],
        )

    def test_runner_error_refreshes_manifests_when_active_batch_exists(self) -> None:
        state = runner.initial_state(self.config)
        select_result = self.make_result()
        self.touch_project_path(select_result["dispatch_path"])
        runner.write_json_object(
            runner.resolve_project_path(self.project, select_result["receipt_path"]),
            select_result,
        )
        runner.apply_phase_result(state, select_result)
        runner.write_state(self.config.state_path, state)
        resume_config = runner.RunnerConfig(**{**self.config.__dict__, "resume": True})

        def failing_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            state["_phase_execution_meta"] = {
                "exit_code": 1,
                "stdout_bytes": 0,
                "stderr_bytes": 18,
                "codex_session_id": "019f0679-3875-7601-a4f8-a2a22303f3c4",
                "codex_session_path": None,
            }
            raise runner.RunnerError("forced create-spec failure")

        with self.assertRaisesRegex(runner.RunnerError, "forced create-spec failure"):
            runner.run(
                resume_config,
                phase_executor=failing_executor,
                status_reader=lambda project: [],
            )

        run_manifest = runner.read_json_object(self.artifact_root / "run-manifest.json")
        batch_manifest = runner.read_json_object(
            self.artifact_root / "batches" / "batch-1" / "batch-manifest.json"
        )

        self.assertEqual(run_manifest["batches"][0]["batch_id"], "batch-1")
        self.assertEqual(batch_manifest["status"], "completed")
        expected_telemetry = (
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/telemetry/phases/01-create-spec.telemetry.json"
        )
        self.assertEqual(
            batch_manifest["telemetry"]["create-spec"],
            expected_telemetry,
        )
        self.assertTrue(
            (self.artifact_root / "batches" / "batch-1" / "index.md").exists()
        )

    def test_malformed_failure_result_uses_active_batch_for_telemetry(self) -> None:
        state = runner.initial_state(self.config)
        select_result = self.make_result()
        self.touch_project_path(select_result["dispatch_path"])
        runner.write_json_object(
            runner.resolve_project_path(self.project, select_result["receipt_path"]),
            select_result,
        )
        runner.apply_phase_result(state, select_result)
        runner.write_state(self.config.state_path, state)
        resume_config = runner.RunnerConfig(**{**self.config.__dict__, "resume": True})

        def malformed_executor(config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
            state["_phase_execution_meta"] = {
                "exit_code": 0,
                "stdout_bytes": 7,
                "stderr_bytes": 0,
                "codex_session_id": "019f0679-3875-7601-a4f8-a2a22303f3c4",
                "codex_session_path": None,
            }
            return {
                "status": "completed",
                "batch_id": None,
                "receipt_path": "project-notes/architecture/receipts/malformed.json",
            }

        with self.assertRaisesRegex(runner.RunnerError, "phase result missing"):
            runner.run(
                resume_config,
                phase_executor=malformed_executor,
                status_reader=lambda project: [],
            )

        saved_state = runner.load_state(self.config.state_path)
        batch_manifest = runner.read_json_object(
            self.artifact_root / "batches" / "batch-1" / "batch-manifest.json"
        )
        phase_telemetry = runner.read_json_object(
            self.artifact_root
            / "telemetry"
            / "phases"
            / "01-create-spec.telemetry.json"
        )

        expected_telemetry = (
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/telemetry/phases/01-create-spec.telemetry.json"
        )
        self.assertEqual(saved_state["last_phase_status"], "failed")
        self.assertIn("phase result missing", saved_state["stop_reason"])
        self.assertEqual(phase_telemetry["batch_id"], "batch-1")
        self.assertEqual(batch_manifest["telemetry"]["create-spec"], expected_telemetry)


if __name__ == "__main__":
    unittest.main()
