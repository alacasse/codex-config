"""Phase environment facts for the architecture program runner."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_state as _runner_state


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    REPO_ROOT
    / "skills"
    / "architecture-program-runway"
    / "references"
    / "local-runner-phase-result.schema.json"
)
RUNNER_REFERENCE_PATH = (
    REPO_ROOT
    / "skills"
    / "architecture-program-runway"
    / "references"
    / "local-runner-v1.md"
)


@dataclass(frozen=True)
class PhaseEnvironment:
    phase: str
    schema_path: Path
    runner_reference_path: Path
    batch_limit_label: str
    env_override_key_label: str
    sandbox: str
    expected_receipt_path: str | None
    expected_input_inventory_path: str | None
    artifact_facts: Mapping[str, Any]

    def subprocess_env(
        self,
        overrides: Iterable[tuple[str, str]],
        *,
        base_env: Mapping[str, str] | None = None,
    ) -> dict[str, str]:
        env = dict(os.environ if base_env is None else base_env)
        for key, value in overrides:
            env[key] = value
        return env


def build_phase_environment(config: Any, state: dict[str, Any], phase: str) -> PhaseEnvironment:
    return PhaseEnvironment(
        phase=phase,
        schema_path=SCHEMA_PATH,
        runner_reference_path=RUNNER_REFERENCE_PATH,
        batch_limit_label=batch_limit_label(config.max_batches),
        env_override_key_label=env_override_key_label(config),
        sandbox=sandbox_for_phase(config, phase),
        expected_receipt_path=_runner_state.phase_receipt_path(state, phase),
        expected_input_inventory_path=_runner_state.phase_input_inventory_path(state, phase),
        artifact_facts={
            "active_batch_id": state.get("active_batch_id"),
            "artifact_root": state.get("artifact_root"),
            "active_batch_artifact_root": state.get("active_batch_artifact_root"),
            "dispatch_path": state.get("dispatch_path"),
            "spec_path": state.get("spec_path"),
            "last_receipt_path": state.get("last_receipt_path"),
            "run_manifest_path": _runner_state.run_manifest_path(state),
            "batch_manifest_path": state.get("batch_manifest_path"),
        },
    )


def sandbox_for_phase(config: Any, phase: str) -> str:
    if phase == "execute" and config.execute_sandbox:
        return config.execute_sandbox
    return config.sandbox


def batch_limit_label(max_batches: int | None) -> str:
    if max_batches is None:
        return "all executable batches until stop condition"
    if max_batches == 1:
        return "1 batch"
    return f"{max_batches} batches"


def env_override_key_label(config: Any) -> str:
    keys = [key for key, _value in config.env_overrides]
    return ", ".join(dict.fromkeys(keys))


def build_subprocess_env(
    overrides: Iterable[tuple[str, str]],
    *,
    base_env: Mapping[str, str] | None = None,
) -> dict[str, str]:
    return PhaseEnvironment(
        phase="",
        schema_path=SCHEMA_PATH,
        runner_reference_path=RUNNER_REFERENCE_PATH,
        batch_limit_label="",
        env_override_key_label="",
        sandbox="",
        expected_receipt_path=None,
        expected_input_inventory_path=None,
        artifact_facts={},
    ).subprocess_env(overrides, base_env=base_env)
