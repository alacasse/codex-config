from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest import mock

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

    def test_phase_observation_path_discovery_returns_none_on_filesystem_errors(
        self,
    ) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3cd"
        codex_home = self.root / "codex-home"
        (codex_home / "sessions").mkdir(parents=True)

        with mock.patch.object(Path, "rglob", side_effect=PermissionError("blocked")):
            self.assertIsNone(
                observation_owner.discover_codex_session_path(
                    session_id,
                    {"CODEX_HOME": str(codex_home)},
                )
            )

    def test_runner_routes_execution_metadata_through_phase_observation_owner(self) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3cc"
        config = self.structured_config()
        codex_home = self.root / "codex-home"
        session_path = self.write_codex_session_file(
            codex_home,
            f"sessions/2026/06/27/rollout-2026-06-27T12-00-00-{session_id}.jsonl",
        )
        config = runner.RunnerConfig(**{**config.__dict__, "stop_after_phase": "select-dispatch"})
        initial_state = runner.initial_state(config)
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path=runner.phase_receipt_path(initial_state, "select-dispatch"),
        )
        self.touch_project_path(result["receipt_path"], json.dumps(result))

        def fake_run(command: list[str], **kwargs: Any) -> Any:
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text(json.dumps(result), encoding="utf-8")
            return runner.subprocess.CompletedProcess(
                command,
                0,
                f"started codex session {session_id}\n",
                "warning avoided\n",
            )

        with mock.patch.dict(runner.os.environ, {"CODEX_HOME": str(codex_home)}, clear=True):
            with mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
                final_state = runner.run(config, status_reader=lambda project: [])

        telemetry = runner.read_json_object(
            config.artifact_root / "telemetry" / "phases" / "01-select-dispatch.telemetry.json"
        )
        telemetry_text = json.dumps(telemetry)

        self.assertEqual(final_state["last_codex_session"], session_id)
        self.assertEqual(telemetry["exit_code"], 0)
        self.assertEqual(
            telemetry["stdout_bytes"],
            len(f"started codex session {session_id}\n".encode("utf-8")),
        )
        self.assertEqual(telemetry["stderr_bytes"], len("warning avoided\n".encode("utf-8")))
        self.assertEqual(telemetry["codex_session_id"], session_id)
        self.assertEqual(telemetry["codex_session_path"], session_path)
        self.assertNotIn("CODEX_HOME", telemetry_text)

    def test_runner_does_not_persist_env_override_values_in_execution_telemetry(
        self,
    ) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3ce"
        config = self.structured_config()
        override_codex_home = self.root / "codex-home-override-secret"
        self.write_codex_session_file(
            override_codex_home,
            f"sessions/2026/06/27/rollout-2026-06-27T12-00-00-{session_id}.jsonl",
        )
        config = runner.RunnerConfig(
            **{
                **config.__dict__,
                "env_overrides": (
                    ("CODEX_HOME", str(override_codex_home)),
                    ("SECRET_TOKEN", "hidden-secret-value"),
                ),
                "stop_after_phase": "select-dispatch",
            }
        )
        initial_state = runner.initial_state(config)
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path=runner.phase_receipt_path(initial_state, "select-dispatch"),
        )
        self.touch_project_path(result["receipt_path"], json.dumps(result))

        def fake_run(command: list[str], **kwargs: Any) -> Any:
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text(json.dumps(result), encoding="utf-8")
            return runner.subprocess.CompletedProcess(
                command,
                0,
                f"started codex session {session_id}\n",
                "warning avoided\n",
            )

        with mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
            final_state = runner.run(config, status_reader=lambda project: [])

        telemetry = runner.read_json_object(
            config.artifact_root / "telemetry" / "phases" / "01-select-dispatch.telemetry.json"
        )
        telemetry_text = json.dumps(telemetry)

        self.assertEqual(final_state["last_codex_session"], session_id)
        self.assertEqual(telemetry["codex_session_id"], session_id)
        self.assertIsNone(telemetry["codex_session_path"])
        self.assertEqual(telemetry["token_summary"]["status"], "missing")
        self.assertNotIn(str(override_codex_home), telemetry_text)
        self.assertNotIn("hidden-secret-value", telemetry_text)

    def test_runner_writes_missing_token_telemetry_when_session_path_access_fails(
        self,
    ) -> None:
        session_id = "019f0679-3875-7601-a4f8-a2a22303f3cf"
        config = self.structured_config()
        codex_home = self.root / "codex-home"
        (codex_home / "sessions").mkdir(parents=True)
        config = runner.RunnerConfig(**{**config.__dict__, "stop_after_phase": "select-dispatch"})
        initial_state = runner.initial_state(config)
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path=runner.phase_receipt_path(initial_state, "select-dispatch"),
        )
        self.touch_project_path(result["receipt_path"], json.dumps(result))

        def fake_run(command: list[str], **kwargs: Any) -> Any:
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text(json.dumps(result), encoding="utf-8")
            return runner.subprocess.CompletedProcess(
                command,
                0,
                f"started codex session {session_id}\n",
                "",
            )

        with mock.patch.dict(runner.os.environ, {"CODEX_HOME": str(codex_home)}, clear=True):
            with mock.patch.object(Path, "rglob", side_effect=PermissionError("blocked")):
                with mock.patch.object(runner.subprocess, "run", side_effect=fake_run):
                    runner.run(config, status_reader=lambda project: [])

        telemetry = runner.read_json_object(
            config.artifact_root / "telemetry" / "phases" / "01-select-dispatch.telemetry.json"
        )

        self.assertEqual(telemetry["codex_session_id"], session_id)
        self.assertIsNone(telemetry["codex_session_path"])
        self.assertEqual(telemetry["token_summary"]["status"], "missing")
        self.assertEqual(telemetry["context_budget"]["status"], "missing")

    def test_phase_observation_is_launch_session_metadata_not_environment_or_contract(self) -> None:
        self.assertEqual(
            PHASE_OBSERVATION_EXECUTION_META_KEYS,
            {"exit_code", "stdout_bytes", "stderr_bytes", "codex_session_id", "codex_session_path"},
        )
