"""Prompt, command, sandbox, env, and dry-run helpers for the architecture runner."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_state as _runner_state

RunnerError = _runner_state.RunnerError
RUNNER_VERSION = _runner_state.RUNNER_VERSION
batch_artifact_root = _runner_state.batch_artifact_root
batch_manifest_path = _runner_state.batch_manifest_path
phase_input_inventory_path = _runner_state.phase_input_inventory_path
phase_receipt_path = _runner_state.phase_receipt_path
run_manifest_path = _runner_state.run_manifest_path


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

CONTEXT_BUDGETS = {
    "select-dispatch": (50_000, 80_000),
    "create-spec": (60_000, 90_000),
    "execute": (120_000, 180_000),
    "closeout": (40_000, 70_000),
}


def build_prompt(config: Any, state: dict[str, Any], phase: str) -> str:
    expected_receipt_path = phase_receipt_path(state, phase)
    expected_input_inventory_path = phase_input_inventory_path(state, phase)
    lines = [
        f"Use {phase_skill_instruction(phase)}.",
        f"Follow {RUNNER_REFERENCE_PATH}.",
        "",
        "Run one local architecture-program runner phase only.",
        f"Project path: {config.project}",
        f"Program ledger: {config.program_ledger}",
        f"State path: {config.state_path}",
        f"Batch limit: {batch_limit_label(config.max_batches)}",
        f"Current phase: {phase}",
        f"Output schema path: {SCHEMA_PATH}",
        "",
        "Single-level phase boundary:",
        "- You are already running inside the runner-launched phase process.",
        "- Do not run codex exec from inside this phase.",
        "- Do not launch the local architecture program runner from inside this phase.",
        "- Do not probe nested Codex availability or create temporary CODEX_HOME workarounds.",
    ]
    if config.env_overrides:
        lines.append(f"Runner env override keys: {env_override_key_label(config)}")
        lines.append("Do not disclose runner env override values.")
        lines.append(
            "Before validation that depends on these keys, run a coordinator-shell "
            "environment probe and record only key-present/readable-path booleans."
        )
    lines.extend(
        [
            "",
            "Expected artifact paths from current state:",
            f"- active_batch_id: {state.get('active_batch_id')}",
            f"- artifact_root: {state.get('artifact_root')}",
            f"- active_batch_artifact_root: {state.get('active_batch_artifact_root')}",
            f"- dispatch_path: {state.get('dispatch_path')}",
            f"- spec_path: {state.get('spec_path')}",
            f"- last_receipt_path: {state.get('last_receipt_path')}",
            f"- run_manifest_path: {run_manifest_path(state)}",
            f"- batch_manifest_path: {state.get('batch_manifest_path')}",
            "",
            "Return schema-valid JSON as the final response.",
            "Write the same JSON object to a compact phase receipt file.",
            "Return the receipt path in receipt_path.",
            "Use compact strings or null for validation_summary and review_summary.",
            "Do not parse or edit runner state directly.",
        ]
    )
    if expected_receipt_path is not None:
        lines.extend(
            [
                "",
                "Expected receipt path for this phase:",
                expected_receipt_path,
                "Write the phase receipt to exactly this path and return exactly this path in receipt_path.",
            ]
        )
    if expected_input_inventory_path is not None:
        lines.extend(
            [
                "",
                "Expected input inventory path for this phase:",
                expected_input_inventory_path,
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
    config: Any, phase: str, prompt: str, output_last_message: Path
) -> list[str]:
    command = [
        "codex",
        "exec",
        "--cd",
        str(config.project),
        "--sandbox",
        sandbox_for_phase(config, phase),
        "--output-schema",
        str(SCHEMA_PATH),
        "--output-last-message",
        str(output_last_message),
    ]
    if config.model:
        command.extend(["--model", config.model])
    command.append(prompt)
    return command


def sandbox_for_phase(config: Any, phase: str) -> str:
    if phase == "execute" and config.execute_sandbox:
        return config.execute_sandbox
    return config.sandbox


def build_subprocess_env(
    overrides: Iterable[tuple[str, str]],
    *,
    base_env: Mapping[str, str] | None = None,
) -> dict[str, str]:
    env = dict(os.environ if base_env is None else base_env)
    for key, value in overrides:
        env[key] = value
    return env


def env_override_key_label(config: Any) -> str:
    keys = [key for key, _value in config.env_overrides]
    return ", ".join(dict.fromkeys(keys))


def print_dry_run(config: Any, state: dict[str, Any]) -> None:
    phase = state["active_phase"]
    prompt = build_prompt(config, state, phase)
    command = build_codex_command(config, phase, prompt, Path("<tmp-result>"))
    print("Command:")
    print(shell_join(command))
    if config.execute_sandbox:
        print(f"Base sandbox: {config.sandbox}")
        print(f"Execute sandbox: {config.execute_sandbox}")
    if config.env_overrides:
        print(f"Env override keys: {env_override_key_label(config)}")
    print()
    print("Prompt:")
    print(prompt)


def batch_limit_label(max_batches: int | None) -> str:
    if max_batches is None:
        return "all executable batches until stop condition"
    if max_batches == 1:
        return "1 batch"
    return f"{max_batches} batches"


def shell_join(command: Iterable[str]) -> str:
    return " ".join(quote_for_display(part) for part in command)


def quote_for_display(value: str) -> str:
    if not value:
        return "''"
    if all(ch.isalnum() or ch in "-_./:=<>" for ch in value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"
