"""Phase contract obligations for the architecture program runner."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_state as _runner_state


RunnerError = _runner_state.RunnerError


@dataclass(frozen=True)
class PhaseContract:
    phase: str
    skill_instruction: str
    single_level_boundary_obligations: tuple[str, ...]
    shared_result_obligations: tuple[str, ...]
    env_override_validation_obligations: tuple[str, ...]
    phase_requirements: tuple[str, ...]


SINGLE_LEVEL_BOUNDARY_OBLIGATIONS = (
    "- You are already running inside the runner-launched phase process.",
    "- Do not run codex exec from inside this phase.",
    "- Do not launch the local architecture program runner from inside this phase.",
    "- Do not probe nested Codex availability or create temporary CODEX_HOME workarounds.",
)

SHARED_RESULT_OBLIGATIONS = (
    "Return schema-valid JSON as the final response.",
    "Write the same JSON object to a compact phase receipt file.",
    "Return the receipt path in receipt_path.",
    "When the prompt names an expected input inventory path, include it in evidence_paths.",
    "Use compact strings or null for validation_summary and review_summary.",
    "Do not parse or edit runner state directly.",
)

ENV_OVERRIDE_VALIDATION_OBLIGATIONS = (
    "Do not disclose runner env override values.",
    (
        "Before validation that depends on these keys, run a coordinator-shell "
        "environment probe and record only key-present/readable-path booleans."
    ),
)


def build_phase_contract(phase: str, *, execute_batches: bool = True) -> PhaseContract:
    return PhaseContract(
        phase=phase,
        skill_instruction=phase_skill_instruction(phase),
        single_level_boundary_obligations=SINGLE_LEVEL_BOUNDARY_OBLIGATIONS,
        shared_result_obligations=SHARED_RESULT_OBLIGATIONS,
        env_override_validation_obligations=ENV_OVERRIDE_VALIDATION_OBLIGATIONS,
        phase_requirements=phase_requirements(phase, execute_batches=execute_batches),
    )


def phase_skill_instruction(phase: str) -> str:
    if phase == "select-dispatch":
        return "$plan-batch once for the complete planning flight"
    if phase == "create-spec":
        return "the prior plan-batch receipt in compatibility-observation mode"
    if phase == "execute":
        return "$batch-runway execute-spec"
    if phase == "closeout":
        return "$architecture-program-runway closeout-runway"
    raise RunnerError(f"unknown phase: {phase}")


def phase_requirements(phase: str, *, execute_batches: bool = True) -> tuple[str, ...]:
    if phase == "select-dispatch":
        return (
            "- Invoke public plan-batch exactly once for selection, independent review, and DEC-038.",
            "- Treat its dispatch, runway, and transaction receipt as the complete planning result.",
            "- Do not repeat selection, proportionality, review, or queue decisions.",
            "- Do not execute code.",
            "- Use next_phase=create-spec when completed.",
        )
    if phase == "create-spec":
        return (
            "- Read the prior select-dispatch receipt and queued dispatch/runway as primary input.",
            "- Confirm the complete plan-batch result is present without invoking plan-batch again.",
            "- Do not create or modify a planning draft, dispatch, runway, or planning decision.",
            "- Do not execute code.",
            f"- Use next_phase={'execute' if execute_batches else 'done'} when completed.",
        )
    if phase == "execute":
        return (
            "- Read and execute exactly the generated Batch Runway spec.",
            "- Preserve normal runway_worker and runway_reviewer delegation.",
            "- Stop on validation, review, dirty-file conflict, or active spec stop conditions.",
            (
                "- Run canonical validation from the execute coordinator shell; do not "
                "treat subagent-only validation output as canonical when runner env "
                "overrides are involved."
            ),
            (
                "- If validation stops, summarize exact canonical command lines "
                "attempted, whether runner env override keys were present in the "
                "command environment, whether path-like override values were readable "
                "without disclosing values, fallback validation attempted/passed, "
                "likely failure class, and dirty files remaining."
            ),
            "- Use next_phase=closeout when completed.",
        )
    if phase == "closeout":
        return (
            "- Reconcile compact execution evidence back into the program ledger.",
            "- Do not paste execution logs into the ledger.",
            "- Write or update compact closeout telemetry as project file evidence.",
            "- Use existing state, receipt, ledger, and evidence files only.",
            "- Update telemetry without launching another Codex process.",
            "- Use next_phase=select-dispatch only when another batch is allowed and ready.",
            (
                "- Use next_phase=select-dispatch when another safe executable batch is "
                "ready and the batch limit permits it."
            ),
            "- Use next_phase=done when the batch limit is reached or no next batch is ready.",
        )
    raise RunnerError(f"unknown phase: {phase}")
