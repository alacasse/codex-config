"""Prompt, command, sandbox, env, and dry-run helpers for the architecture runner."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from scripts import architecture_program_runner_environment as _runner_environment
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_environment as _runner_environment
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
    lines = [
        f"Use {phase_skill_instruction(phase)}.",
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
        "- You are already running inside the runner-launched phase process.",
        "- Do not run codex exec from inside this phase.",
        "- Do not launch the local architecture program runner from inside this phase.",
        "- Do not probe nested Codex availability or create temporary CODEX_HOME workarounds.",
    ]
    if config.env_overrides:
        lines.append(f"Runner env override keys: {environment.env_override_key_label}")
        lines.append("Do not disclose runner env override values.")
        lines.append(
            "Before validation that depends on these keys, run a coordinator-shell "
            "environment probe and record only key-present/readable-path booleans."
        )
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
            "Return schema-valid JSON as the final response.",
            "Write the same JSON object to a compact phase receipt file.",
            "Return the receipt path in receipt_path.",
            "Use compact strings or null for validation_summary and review_summary.",
            "Do not parse or edit runner state directly.",
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
                "If you perform broad source reads, large file reads, or consume subagent reports, write a compact input inventory there and include it in evidence_paths.",
                "Prefer compact dispatch, receipt, manifest, and telemetry artifacts before rereading broad source or planning files.",
            ]
        )

    if phase == "select-dispatch":
        lines.extend(
            [
                "",
                "Phase requirements:",
                "- Select exactly one next executable batch.",
                "- Create or refresh one compact dispatch packet.",
                "- Do not create a Batch Runway spec.",
                "- Do not execute code.",
                "- Use next_phase=create-spec when completed.",
            ]
        )
    elif phase == "create-spec":
        lines.extend(
            [
                "",
                "Phase requirements:",
                "- Read the dispatch packet as primary input.",
                "- Read only minimum ledger context needed for status and evidence.",
                "- Create exactly one concrete Batch Runway spec.",
                "- Do not execute code.",
                f"- Use next_phase={'execute' if config.execute_batches else 'done'} when completed.",
            ]
        )
    elif phase == "execute":
        lines.extend(
            [
                "",
                "Phase requirements:",
                "- Read and execute exactly the generated Batch Runway spec.",
                "- Preserve normal runway_worker and runway_reviewer delegation.",
                "- Stop on validation, review, dirty-file conflict, or active spec stop conditions.",
                "- Run canonical validation from the execute coordinator shell; do not treat subagent-only validation output as canonical when runner env overrides are involved.",
                "- If validation stops, summarize exact canonical command lines attempted, whether runner env override keys were present in the command environment, whether path-like override values were readable without disclosing values, fallback validation attempted/passed, likely failure class, and dirty files remaining.",
                "- Use next_phase=closeout when completed.",
            ]
        )
    elif phase == "closeout":
        lines.extend(
            [
                "",
                "Phase requirements:",
                "- Reconcile compact execution evidence back into the program ledger.",
                "- Do not paste execution logs into the ledger.",
                "- Write or update compact closeout telemetry as project file evidence.",
                "- Use existing state, receipt, ledger, and evidence files only.",
                "- Update telemetry without launching another Codex process.",
                "- Use next_phase=select-dispatch only when another batch is allowed and ready.",
                "- Use next_phase=select-dispatch when another safe executable batch is ready and the batch limit permits it.",
                "- Use next_phase=done when the batch limit is reached or no next batch is ready.",
            ]
        )

    return "\n".join(lines)


def phase_skill_instruction(phase: str) -> str:
    if phase == "select-dispatch":
        return "$architecture-program-runway in select-next-batch mode"
    if phase == "create-spec":
        return "$architecture-program-runway in create-next-runway mode"
    if phase == "execute":
        return "$batch-runway execute-spec"
    if phase == "closeout":
        return "$architecture-program-runway closeout-runway"
    raise RunnerError(f"unknown phase: {phase}")


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
