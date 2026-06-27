from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts import architecture_program_runner_artifacts as artifacts
from scripts import architecture_program_runner_phase_observation as observation_owner
from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


PHASE_OBSERVATION_EXECUTION_META_KEYS = {
    "exit_code",
    "stdout_bytes",
    "stderr_bytes",
    "codex_session_id",
    "codex_session_path",
}


class ArchitectureProgramRunnerPhaseObservationTests(ArchitectureProgramRunnerTestCase):
    def write_codex_session_file(self, codex_home: Path, relative_path: str) -> str:
        path = codex_home / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
        return str(path)

    def write_session_jsonl(self, *records: dict[str, Any]) -> str:
        path = self.root / "codex-session.jsonl"
        path.write_text(
            "\n".join(json.dumps(record) for record in records),
            encoding="utf-8",
        )
        return str(path)

    def build_telemetry(self, execution_meta: dict[str, Any]) -> dict[str, Any]:
        config = self.structured_config()
        state = runner.initial_state(config)
        result = self.make_result("execute", "closeout")
        return artifacts.build_phase_telemetry(
            config,
            state,
            "execute",
            started_at="2026-06-27T12:00:00Z",
            elapsed_seconds=1.25,
            prompt_bytes=512,
            result=result,
            status="completed",
            error=None,
            execution_meta=execution_meta,
        )

    def test_phase_observation_parses_exact_codex_session_id_from_stdout(self) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3c4"

        self.assertEqual(
            observation_owner.extract_codex_session_id(
                f"codex exec started session {session_id}\n"
            ),
            session_id,
        )

    def test_phase_observation_parses_exact_codex_session_id_from_stderr(self) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3c5"

        self.assertEqual(
            observation_owner.extract_codex_session_id(f"warning: resumed session {session_id}\n"),
            session_id,
        )

    def test_phase_observation_parses_exact_codex_session_id_from_combined_output(self) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3c6"
        stdout = "select-dispatch phase complete"
        stderr = f"codex session: {session_id}"

        self.assertEqual(
            observation_owner.extract_codex_session_id(f"{stdout}\n{stderr}"),
            session_id,
        )

    def test_phase_observation_owner_builds_execution_metadata_with_exact_session_path(
        self,
    ) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3c9"
        codex_home = self.root / "codex-home"
        session_path = self.write_codex_session_file(
            codex_home,
            f"sessions/2026/06/27/rollout-2026-06-27T12-00-00-{session_id}.jsonl",
        )

        observation = observation_owner.build_phase_execution_observation(
            exit_code=0,
            stdout=f"started {session_id}\n",
            stderr="warning avoided\n",
            subprocess_env={"CODEX_HOME": str(codex_home)},
        )

        self.assertEqual(observation.exit_code, 0)
        self.assertEqual(observation.stdout_bytes, len(f"started {session_id}\n".encode()))
        self.assertEqual(observation.stderr_bytes, len("warning avoided\n".encode()))
        self.assertEqual(observation.codex_session_id, session_id)
        self.assertEqual(observation.codex_session_path, session_path)
        self.assertEqual(
            observation.as_execution_meta(),
            {
                "exit_code": 0,
                "stdout_bytes": observation.stdout_bytes,
                "stderr_bytes": observation.stderr_bytes,
                "codex_session_id": session_id,
                "codex_session_path": session_path,
            },
        )

    def test_phase_observation_path_discovery_returns_none_when_no_match(self) -> None:
        codex_home = self.root / "codex-home"
        (codex_home / "sessions" / "2026" / "06" / "27").mkdir(parents=True)

        self.assertIsNone(
            observation_owner.discover_codex_session_path(
                "019f0679-3875-7601-a4f8-a2a22303f3ca",
                {"CODEX_HOME": str(codex_home)},
            )
        )

    def test_phase_observation_path_discovery_returns_none_when_ambiguous(self) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3cb"
        codex_home = self.root / "codex-home"
        self.write_codex_session_file(
            codex_home,
            f"sessions/2026/06/27/rollout-2026-06-27T12-00-00-{session_id}.jsonl",
        )
        self.write_codex_session_file(
            codex_home,
            f"sessions/2026/06/28/rollout-2026-06-28T12-00-00-{session_id}.jsonl",
        )

        self.assertIsNone(
            observation_owner.discover_codex_session_path(
                session_id,
                {"CODEX_HOME": str(codex_home)},
            )
        )

    def test_runner_facade_reexports_phase_observation_owner_for_compatibility(self) -> None:
        self.assertIs(
            runner.PhaseExecutionObservation,
            observation_owner.PhaseExecutionObservation,
        )
        self.assertIs(
            runner.build_phase_execution_observation,
            observation_owner.build_phase_execution_observation,
        )
        self.assertIs(runner.extract_codex_session_id, observation_owner.extract_codex_session_id)

    def test_phase_observation_missing_session_attribution_is_non_fatal(self) -> None:
        telemetry = self.build_telemetry(
            {
                "exit_code": 0,
                "stdout_bytes": 0,
                "stderr_bytes": 0,
                "codex_session_id": None,
                "codex_session_path": None,
            }
        )

        self.assertIsNone(telemetry["codex_session_id"])
        self.assertIsNone(telemetry["codex_session_path"])
        self.assertEqual(telemetry["token_summary"]["status"], "missing")
        self.assertEqual(telemetry["token_summary"]["context_pressure"], "missing")
        self.assertEqual(telemetry["context_budget"]["status"], "missing")

    def test_phase_observation_exact_session_path_summarizes_token_events(self) -> None:
        session_path = self.write_session_jsonl(
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

        telemetry = self.build_telemetry(
            {
                "exit_code": 0,
                "stdout_bytes": 42,
                "stderr_bytes": 7,
                "codex_session_id": "019f0679-3875-7601-a4f8-a2a22303f3c7",
                "codex_session_path": session_path,
            }
        )

        self.assertEqual(telemetry["codex_session_path"], session_path)
        self.assertEqual(telemetry["token_summary"]["status"], "ok")
        self.assertEqual(telemetry["token_summary"]["turn_count"], 2)
        self.assertEqual(telemetry["token_summary"]["max_input_tokens"], 8400)
        self.assertEqual(telemetry["token_summary"]["max_context_used_percent"], 84.0)
        self.assertEqual(telemetry["token_summary"]["context_pressure"], "context_pressure")
        self.assertEqual(telemetry["context_budget"]["max_input_tokens"], 8400)

    def test_phase_observation_is_launch_session_metadata_not_environment_or_contract(self) -> None:
        telemetry = self.build_telemetry(
            {
                "exit_code": 0,
                "stdout_bytes": 42,
                "stderr_bytes": 7,
                "codex_session_id": "019f0679-3875-7601-a4f8-a2a22303f3c8",
                "codex_session_path": None,
            }
        )

        self.assertEqual(
            PHASE_OBSERVATION_EXECUTION_META_KEYS,
            {"exit_code", "stdout_bytes", "stderr_bytes", "codex_session_id", "codex_session_path"},
        )
        for key in PHASE_OBSERVATION_EXECUTION_META_KEYS:
            self.assertIn(key, telemetry)
        self.assertNotIn("phase_environment", telemetry)
        self.assertNotIn("phase_contract", telemetry)
