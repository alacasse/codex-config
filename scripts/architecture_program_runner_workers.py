"""Worker adapters for architecture-program phase execution."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any, Protocol

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
            if completed.returncode != 0:
                raise RunnerError(
                    "codex exec failed for "
                    f"{phase} with exit {completed.returncode}\n{completed.stderr.strip()}"
                )
            return read_json_object(output_last_message)


def execute_phase_with_worker(
    config: Any,
    state: dict[str, Any],
    phase: str,
    worker: PhaseWorker,
) -> dict[str, Any]:
    return worker.run_phase(config, state, phase)
