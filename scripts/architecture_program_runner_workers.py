"""Worker adapters for architecture-program phase execution."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any, Protocol, Sequence

try:
    from scripts import architecture_program_runner_command as _runner_command
    from scripts import architecture_program_runner_environment as _runner_environment
    from scripts import architecture_program_runner_phase_observation as _phase_observation
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_command as _runner_command
    import architecture_program_runner_environment as _runner_environment
    import architecture_program_runner_phase_observation as _phase_observation
    import architecture_program_runner_state as _runner_state


RunnerError = _runner_state.RunnerError
read_json_object = _runner_state.read_json_object


class PhaseWorker(Protocol):
    """Internal adapter API for running one phase and returning its result."""

    def run_phase(self, config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
        """Run a phase and return the phase result dictionary."""


class CodexExecWorker:
    """Run a phase through the existing codex exec command path."""

    def run_phase(self, config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
        environment = _runner_environment.build_phase_environment(config, state, phase)
        prompt = _runner_command.build_prompt(config, state, phase, environment=environment)
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", prefix="architecture-program-runner-", suffix=".json"
        ) as handle:
            output_last_message = Path(handle.name)
            command = _runner_command.build_codex_command(
                config,
                phase,
                prompt,
                output_last_message,
                environment=environment,
            )
            codex_home_env = environment.subprocess_env(())
            subprocess_env = environment.subprocess_env(config.env_overrides)
            completed = subprocess.run(
                command,
                cwd=config.project,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                env=subprocess_env,
            )
            state["_phase_execution_meta"] = (
                _phase_observation.build_phase_execution_observation(
                    exit_code=completed.returncode,
                    stdout=completed.stdout,
                    stderr=completed.stderr,
                    subprocess_env=subprocess_env,
                    codex_home_env=codex_home_env,
                ).as_execution_meta()
            )
            state["_phase_execution_meta"]["prompt_bytes"] = len(prompt.encode("utf-8"))
            if completed.returncode != 0:
                raise RunnerError(
                    "codex exec failed for "
                    f"{phase} with exit {completed.returncode}\n{completed.stderr.strip()}"
                )
            return read_json_object(output_last_message)


class ShellCommandWorker:
    """Run an internal shell command that writes a compact phase result JSON file."""

    def __init__(self, command: Sequence[str]) -> None:
        if isinstance(command, str):
            raise TypeError("ShellCommandWorker command must be an argv sequence")
        self.command = tuple(command)

    def run_phase(self, config: Any, state: dict[str, Any], phase: str) -> dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="architecture-program-runner-shell-") as temp_dir:
            output_path = Path(temp_dir) / "phase-result.json"
            subprocess_env = _runner_environment.build_subprocess_env(config.env_overrides)
            subprocess_env.update(
                {
                    "ARCHITECTURE_PROGRAM_PHASE": phase,
                    "ARCHITECTURE_PROGRAM_PHASE_RESULT_PATH": str(output_path),
                    "ARCHITECTURE_PROGRAM_PROJECT": str(config.project),
                }
            )
            expected_receipt_path = _runner_state.phase_receipt_path(state, phase)
            if expected_receipt_path:
                subprocess_env["ARCHITECTURE_PROGRAM_EXPECTED_RECEIPT_PATH"] = (
                    expected_receipt_path
                )
            expected_inventory_path = _runner_state.phase_input_inventory_path(state, phase)
            if expected_inventory_path:
                subprocess_env["ARCHITECTURE_PROGRAM_EXPECTED_INPUT_INVENTORY_PATH"] = (
                    expected_inventory_path
                )
            completed = subprocess.run(
                self.command,
                cwd=config.project,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                env=subprocess_env,
                shell=False,
            )
            state["_phase_execution_meta"] = {
                "exit_code": completed.returncode,
                "stdout_bytes": len(completed.stdout.encode("utf-8")),
                "stderr_bytes": len(completed.stderr.encode("utf-8")),
                "codex_session_id": None,
                "codex_session_path": None,
                "prompt_bytes": 0,
            }
            if completed.returncode != 0:
                raise RunnerError(
                    "shell command failed for "
                    f"{phase} with exit {completed.returncode}\n{completed.stderr.strip()}"
                )
            return read_json_object(output_path)


def execute_phase_with_worker(
    config: Any,
    state: dict[str, Any],
    phase: str,
    worker: PhaseWorker,
) -> dict[str, Any]:
    return worker.run_phase(config, state, phase)
