"""Prompt, command, sandbox, env, and dry-run helpers for the architecture runner."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from scripts import architecture_program_runner_environment as _runner_environment
    from scripts import architecture_program_runner_phase_contract as _phase_contract
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_environment as _runner_environment
    import architecture_program_runner_phase_contract as _phase_contract
    import architecture_program_runner_state as _runner_state

RunnerError = _runner_state.RunnerError
RUNNER_VERSION = _runner_state.RUNNER_VERSION
batch_artifact_root = _runner_state.batch_artifact_root
batch_manifest_path = _runner_state.batch_manifest_path
phase_input_inventory_path = _runner_state.phase_input_inventory_path
phase_receipt_path = _runner_state.phase_receipt_path
run_manifest_path = _runner_state.run_manifest_path


SCHEMA_PATH = _runner_environment.SCHEMA_PATH
RUNNER_REFERENCE_PATH = _runner_environment.RUNNER_REFERENCE_PATH
PhaseEnvironment = _runner_environment.PhaseEnvironment
build_phase_environment = _runner_environment.build_phase_environment

CONTEXT_BUDGETS = {
    "select-dispatch": (50_000, 80_000),
    "create-spec": (60_000, 90_000),
    "execute": (120_000, 180_000),
    "closeout": (40_000, 70_000),
}


def build_prompt(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    environment: PhaseEnvironment | None = None,
) -> str:
    environment = environment or build_phase_environment(config, state, phase)
    contract = _phase_contract.build_phase_contract(
        phase, execute_batches=config.execute_batches
    )
    lines = [
        f"Use {contract.skill_instruction}.",
        f"Follow {environment.runner_reference_path}.",
        "",
        "Run one local architecture-program runner phase only.",
        f"Project path: {config.project}",
        f"Program ledger: {config.program_ledger}",
        f"State path: {config.state_path}",
        f"Batch limit: {environment.batch_limit_label}",
        f"Current phase: {phase}",
        f"Output schema path: {environment.schema_path}",
        "",
        "Single-level phase boundary:",
        *contract.single_level_boundary_obligations,
    ]
    if config.env_overrides:
        lines.append(f"Runner env override keys: {environment.env_override_key_label}")
        lines.extend(contract.env_override_validation_obligations)
    lines.extend(
        [
            "",
            "Expected artifact paths from current state:",
            f"- active_batch_id: {environment.artifact_facts['active_batch_id']}",
            f"- artifact_root: {environment.artifact_facts['artifact_root']}",
            f"- active_batch_artifact_root: {environment.artifact_facts['active_batch_artifact_root']}",
            f"- dispatch_path: {environment.artifact_facts['dispatch_path']}",
            f"- spec_path: {environment.artifact_facts['spec_path']}",
            f"- last_receipt_path: {environment.artifact_facts['last_receipt_path']}",
            f"- run_manifest_path: {environment.artifact_facts['run_manifest_path']}",
            f"- batch_manifest_path: {environment.artifact_facts['batch_manifest_path']}",
            "",
            *contract.shared_result_obligations,
        ]
    )
    if environment.expected_receipt_path is not None:
        lines.extend(
            [
                "",
                "Expected receipt path for this phase:",
                environment.expected_receipt_path,
                "Write the phase receipt to exactly this path and return exactly this path in receipt_path.",
            ]
        )
    if environment.expected_input_inventory_path is not None:
        lines.extend(
            [
                "",
                "Expected input inventory path for this phase:",
                environment.expected_input_inventory_path,
                "Write a compact input inventory to exactly this path and include that path in evidence_paths.",
                "Use empty inventory arrays when the phase consumed no broad reads, large files, or subagent reports.",
                "Prefer compact dispatch, receipt, manifest, and telemetry artifacts before rereading broad source or planning files.",
            ]
        )

    lines.extend(["", "Phase requirements:", *contract.phase_requirements])

    return "\n".join(lines)


def phase_skill_instruction(phase: str) -> str:
    return _phase_contract.phase_skill_instruction(phase)


def build_codex_command(
    config: Any,
    phase: str,
    prompt: str,
    output_last_message: Path,
    *,
    environment: PhaseEnvironment | None = None,
) -> list[str]:
    environment = environment or build_phase_environment(config, {}, phase)
    command = [
        "codex",
        "exec",
        "--cd",
        str(config.project),
        "--sandbox",
        environment.sandbox,
        "--output-schema",
        str(environment.schema_path),
        "--output-last-message",
        str(output_last_message),
    ]
    if config.model:
        command.extend(["--model", config.model])
    command.append(prompt)
    return command


def sandbox_for_phase(config: Any, phase: str) -> str:
    return _runner_environment.sandbox_for_phase(config, phase)


def build_subprocess_env(
    overrides: Iterable[tuple[str, str]],
    *,
    base_env: Mapping[str, str] | None = None,
) -> dict[str, str]:
    return _runner_environment.build_subprocess_env(overrides, base_env=base_env)


def env_override_key_label(config: Any) -> str:
    return _runner_environment.env_override_key_label(config)


def print_dry_run(config: Any, state: dict[str, Any]) -> None:
    phase = state["active_phase"]
    environment = build_phase_environment(config, state, phase)
    prompt = build_prompt(config, state, phase, environment=environment)
    command = build_codex_command(
        config,
        phase,
        prompt,
        Path("<tmp-result>"),
        environment=environment,
    )
    print("Command:")
    print(shell_join(command))
    if config.execute_sandbox:
        print(f"Base sandbox: {config.sandbox}")
        print(f"Execute sandbox: {config.execute_sandbox}")
    if config.env_overrides:
        print(f"Env override keys: {environment.env_override_key_label}")
    print()
    print("Prompt:")
    print(prompt)


def batch_limit_label(max_batches: int | None) -> str:
    return _runner_environment.batch_limit_label(max_batches)


def shell_join(command: Iterable[str]) -> str:
    return " ".join(quote_for_display(part) for part in command)


def quote_for_display(value: str) -> str:
    if not value:
        return "''"
    if all(ch.isalnum() or ch in "-_./:=<>" for ch in value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"
