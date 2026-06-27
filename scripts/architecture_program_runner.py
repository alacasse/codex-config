#!/usr/bin/env python3
"""Run architecture-program phases through fresh Codex exec processes."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

_OS_ENVIRON = os.environ

try:
    from scripts import architecture_program_runner_artifacts as _runner_artifacts
    from scripts import architecture_program_runner_change_allowance as _runner_change_allowance
    from scripts import architecture_program_runner_command as _runner_command
    from scripts import architecture_program_runner_environment as _runner_environment
    from scripts import architecture_program_runner_phase_observation as _phase_observation
    from scripts import architecture_program_runner_phase_contract as _phase_contract
    from scripts import architecture_program_runner_state as _runner_state
    from scripts import architecture_program_runner_transition as _runner_transition
    from scripts import architecture_program_runner_validation as _runner_validation
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_artifacts as _runner_artifacts
    import architecture_program_runner_change_allowance as _runner_change_allowance
    import architecture_program_runner_command as _runner_command
    import architecture_program_runner_environment as _runner_environment
    import architecture_program_runner_phase_observation as _phase_observation
    import architecture_program_runner_phase_contract as _phase_contract
    import architecture_program_runner_state as _runner_state
    import architecture_program_runner_transition as _runner_transition
    import architecture_program_runner_validation as _runner_validation

PHASE_RECEIPT_NAMES = _runner_state.PHASE_RECEIPT_NAMES
PHASES = _runner_state.PHASES
RUNNER_VERSION = _runner_state.RUNNER_VERSION
RunnerError = _runner_state.RunnerError
artifact_root_from_state_path = _runner_state.artifact_root_from_state_path
batch_artifact_root = _runner_state.batch_artifact_root
batch_manifest_path = _runner_state.batch_manifest_path
default_artifact_root = _runner_state.default_artifact_root
discover_resume_state_path = _runner_state.discover_resume_state_path
initial_state = _runner_state.initial_state
ledger_slug = _runner_state.ledger_slug
legacy_state_path = _runner_state.legacy_state_path
load_state = _runner_state.load_state
new_run_id = _runner_state.new_run_id
next_phase_telemetry_path = _runner_state.next_phase_telemetry_path
phase_input_inventory_path = _runner_state.phase_input_inventory_path
phase_receipt_path = _runner_state.phase_receipt_path
project_relative = _runner_state.project_relative
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path
resolve_state_path = _runner_state.resolve_state_path
run_manifest_path = _runner_state.run_manifest_path
run_telemetry_path = _runner_state.run_telemetry_path
slugify_path_component = _runner_state.slugify_path_component
structured_artifacts_enabled = _runner_state.structured_artifacts_enabled
utc_now = _runner_state.utc_now
validate_state = _runner_state.validate_state
write_json_object = _runner_state.write_json_object
write_state = _runner_state.write_state
NEXT_PHASES = _runner_validation.NEXT_PHASES
REQUIRED_RESULT_FIELDS = _runner_validation.REQUIRED_RESULT_FIELDS
STATUSES = _runner_validation.STATUSES
UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS = _runner_validation.UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS
expected_next_phases = _runner_validation.expected_next_phases
schema_keyword_paths = _runner_validation.schema_keyword_paths
schema_subset_violations = _runner_validation.schema_subset_violations
validate_expected_receipt_path = _runner_validation.validate_expected_receipt_path
validate_nullable_string = _runner_validation.validate_nullable_string
validate_phase_result = _runner_validation.validate_phase_result
validate_receipt = _runner_validation.validate_receipt
validate_required_string = _runner_validation.validate_required_string
validate_result_against_state = _runner_validation.validate_result_against_state
validate_summary = _runner_validation.validate_summary
CONTEXT_BUDGETS = _runner_command.CONTEXT_BUDGETS
PhaseContract = _phase_contract.PhaseContract
SCHEMA_PATH = _runner_environment.SCHEMA_PATH
RUNNER_REFERENCE_PATH = _runner_environment.RUNNER_REFERENCE_PATH
build_codex_command = _runner_command.build_codex_command
build_phase_contract = _phase_contract.build_phase_contract
build_prompt = _runner_command.build_prompt
phase_skill_instruction = _runner_command.phase_skill_instruction
print_dry_run = _runner_command.print_dry_run
quote_for_display = _runner_command.quote_for_display
shell_join = _runner_command.shell_join
batch_limit_label = _runner_environment.batch_limit_label
build_phase_environment = _runner_environment.build_phase_environment
build_subprocess_env = _runner_environment.build_subprocess_env
env_override_key_label = _runner_environment.env_override_key_label
sandbox_for_phase = _runner_environment.sandbox_for_phase
PhaseExecutionObservation = _phase_observation.PhaseExecutionObservation
build_phase_execution_observation = _phase_observation.build_phase_execution_observation
discover_codex_session_path = _phase_observation.discover_codex_session_path
effective_codex_home = _phase_observation.effective_codex_home
extract_codex_session_id = _phase_observation.extract_codex_session_id
apply_execution_meta_to_state = _runner_artifacts.apply_execution_meta_to_state
artifact_batch_entry = _runner_artifacts.artifact_batch_entry
artifact_size_entries = _runner_artifacts.artifact_size_entries
build_batch_index = _runner_artifacts.build_batch_index
build_batch_manifest = _runner_artifacts.build_batch_manifest
build_phase_telemetry = _runner_artifacts.build_phase_telemetry
build_run_manifest = _runner_artifacts.build_run_manifest
build_run_telemetry = _runner_artifacts.build_run_telemetry
context_budget_summary = _runner_artifacts.context_budget_summary
context_pressure = _runner_artifacts.context_pressure
int_or_none = _runner_artifacts.int_or_none
latest_receipt_field = _runner_artifacts.latest_receipt_field
max_numeric = _runner_artifacts.max_numeric
missing_token_summary = _runner_artifacts.missing_token_summary
pop_phase_execution_meta = _runner_artifacts.pop_phase_execution_meta
record_artifact_batch = _runner_artifacts.record_artifact_batch
record_phase_telemetry_path = _runner_artifacts.record_phase_telemetry_path
relative_project_link = _runner_artifacts.relative_project_link
sum_numeric = _runner_artifacts.sum_numeric
summarize_token_events = _runner_artifacts.summarize_token_events
telemetry_path_for_phase = _runner_artifacts.telemetry_path_for_phase
write_artifact_manifests = _runner_artifacts.write_artifact_manifests
write_batch_artifacts = _runner_artifacts.write_batch_artifacts
write_phase_telemetry = _runner_artifacts.write_phase_telemetry
write_run_telemetry = _runner_artifacts.write_run_telemetry
apply_phase_result = _runner_transition.apply_phase_transition
apply_phase_transition = _runner_transition.apply_phase_transition
is_terminal_completed_state = _runner_transition.is_terminal_phase_transition_state
is_terminal_phase_transition_state = _runner_transition.is_terminal_phase_transition_state
check_change_allowance = _runner_change_allowance.check_change_allowance
check_change_allowance_path = _runner_change_allowance.check_change_allowance_path
check_worktree = _runner_change_allowance.check_worktree
dirty_paths_from_status = _runner_change_allowance.dirty_paths_from_status
expected_change_allowance_paths = _runner_change_allowance.expected_change_allowance_paths
expected_dirty_paths = _runner_change_allowance.expected_dirty_paths
git_status_lines = _runner_change_allowance.git_status_lines
path_is_expected = _runner_change_allowance.path_is_expected


REPO_ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class RunnerConfig:
    project: Path
    program_ledger: str
    max_batches: int | None
    execute_batches: bool
    state_path: Path
    sandbox: str
    execute_sandbox: str | None
    model: str | None
    env_overrides: tuple[tuple[str, str], ...]
    dry_run: bool
    resume: bool
    stop_after_phase: str | None
    artifact_root: Path | None = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run split-phase architecture-program batches through codex exec."
    )
    parser.add_argument("--project", required=True, help="Project path for codex exec --cd.")
    parser.add_argument(
        "--program-ledger",
        required=True,
        help="Project-relative program ledger path.",
    )
    parser.add_argument(
        "--max-batches",
        type=positive_int,
        default=None,
        help="Maximum closeouts to complete. Default: 1 unless --all-batches is set.",
    )
    parser.add_argument(
        "--all-batches",
        action="store_true",
        help=(
            "Run until no safe executable batch remains or a stop condition is hit. "
            "Cannot be combined with --max-batches."
        ),
    )
    parser.add_argument(
        "--execute-batches",
        action="store_true",
        help="Execute generated Batch Runway specs after creation.",
    )
    parser.add_argument(
        "--state",
        default=None,
        help="Project-relative or absolute JSON state path.",
    )
    parser.add_argument(
        "--sandbox",
        default="workspace-write",
        help="Codex sandbox value. Default: workspace-write.",
    )
    parser.add_argument(
        "--execute-sandbox",
        default=None,
        help=(
            "Optional Codex sandbox value for the execute phase only. "
            "Use when Batch Runway execution must commit and the default sandbox "
            "cannot write Git metadata."
        ),
    )
    parser.add_argument("--model", default=None, help="Optional codex exec model.")
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        type=env_override,
        help=(
            "Environment variable override passed to every nested codex exec phase. "
            "Repeat for multiple values."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned phase command and prompt without writing state.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Load existing state and resume from active_phase.",
    )
    parser.add_argument(
        "--stop-after-phase",
        choices=PHASES,
        default=None,
        help=(
            "Run and complete the named phase, persist receipt and state, "
            "then stop before launching the next phase."
        ),
    )
    args = parser.parse_args(argv)
    if args.all_batches and args.max_batches is not None:
        parser.error("--all-batches cannot be combined with --max-batches")
    return args


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def env_override(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("must use KEY=VALUE")
    key, env_value = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("environment key must be non-empty")
    return key, env_value


def config_from_args(args: argparse.Namespace) -> RunnerConfig:
    project = Path(args.project).expanduser().resolve()
    state_path, artifact_root = resolve_state_path(
        project, args.program_ledger, args.state, resume=args.resume
    )
    max_batches = None if args.all_batches else args.max_batches or 1
    return RunnerConfig(
        project=project,
        program_ledger=args.program_ledger,
        max_batches=max_batches,
        execute_batches=args.execute_batches,
        state_path=state_path,
        sandbox=args.sandbox,
        execute_sandbox=args.execute_sandbox,
        model=args.model,
        env_overrides=tuple(args.env),
        dry_run=args.dry_run,
        resume=args.resume,
        stop_after_phase=args.stop_after_phase,
        artifact_root=artifact_root,
    )


def execute_codex_phase(config: RunnerConfig, state: dict[str, Any], phase: str) -> dict[str, Any]:
    environment = build_phase_environment(config, state, phase)
    prompt = build_prompt(config, state, phase, environment=environment)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", prefix="architecture-program-runner-", suffix=".json"
    ) as handle:
        output_last_message = Path(handle.name)
        command = build_codex_command(
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
        state["_phase_execution_meta"] = build_phase_execution_observation(
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            subprocess_env=subprocess_env,
            codex_home_env=codex_home_env,
        ).as_execution_meta()
        if completed.returncode != 0:
            raise RunnerError(
                "codex exec failed for "
                f"{phase} with exit {completed.returncode}\n{completed.stderr.strip()}"
            )
        return read_json_object(output_last_message)


def check_required_artifacts(config: RunnerConfig, state: dict[str, Any]) -> None:
    phase = state["active_phase"]
    if phase in {"create-spec", "execute", "closeout"}:
        dispatch_path = state.get("dispatch_path")
        if not dispatch_path:
            raise RunnerError(f"{phase} requires dispatch_path in runner state")
        if not resolve_project_path(config.project, dispatch_path).exists():
            raise RunnerError(f"{phase} dispatch_path does not exist: {dispatch_path}")
    if phase in {"execute", "closeout"}:
        spec_path = state.get("spec_path")
        if not spec_path:
            raise RunnerError(f"{phase} requires spec_path in runner state")
        if not resolve_project_path(config.project, spec_path).exists():
            raise RunnerError(f"{phase} spec_path does not exist: {spec_path}")
    receipt_path = state.get("last_receipt_path")
    if state.get("last_phase_status") == "completed" and receipt_path:
        receipt = read_json_object(resolve_project_path(config.project, receipt_path))
        validate_phase_result(receipt)


def run(
    config: RunnerConfig,
    *,
    phase_executor: Callable[[RunnerConfig, dict[str, Any], str], dict[str, Any]] = execute_codex_phase,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
) -> dict[str, Any]:
    state = load_state(config.state_path) if config.resume else initial_state(config)
    validate_state_matches_config(state, config)

    if config.dry_run:
        print_dry_run(config, state)
        return state

    while True:
        if is_terminal_completed_state(state):
            return state
        if (
            config.max_batches is not None
            and state["batches_completed"] >= config.max_batches
        ):
            state["stop_reason"] = "max_batches_reached"
            write_state(config.state_path, state)
            return state

        phase = state["active_phase"]
        phase_telemetry_path: str | None = None
        phase_started_at: str | None = None
        phase_start_monotonic: float | None = None
        phase_prompt_bytes = 0
        result: dict[str, Any] | None = None
        try:
            check_required_artifacts(config, state)
            check_worktree(config, state, phase, status_reader=status_reader)
            phase_telemetry_path = next_phase_telemetry_path(state, phase)
            phase_started_at = utc_now()
            phase_start_monotonic = time.monotonic()
            environment = build_phase_environment(config, state, phase)
            phase_prompt_bytes = len(
                build_prompt(config, state, phase, environment=environment).encode("utf-8")
            )
            result = phase_executor(config, state, phase)
            execution_meta = pop_phase_execution_meta(state)
            apply_execution_meta_to_state(state, execution_meta)
            validate_phase_result(result, current_phase=phase, state=state)
            validate_receipt(result, config, state)
            if phase == "execute":
                check_worktree(
                    config,
                    state,
                    "closeout",
                    status_reader=status_reader,
                    extra_paths=[result["receipt_path"], *result["evidence_paths"]],
                )
        except RunnerError as exc:
            execution_meta = pop_phase_execution_meta(state)
            apply_execution_meta_to_state(state, execution_meta)
            state["last_phase_status"] = "failed"
            state["stop_reason"] = str(exc)
            if phase_telemetry_path and phase_started_at and phase_start_monotonic is not None:
                telemetry = build_phase_telemetry(
                    config,
                    state,
                    phase,
                    started_at=phase_started_at,
                    elapsed_seconds=round(time.monotonic() - phase_start_monotonic, 3),
                    prompt_bytes=phase_prompt_bytes,
                    result=result,
                    status="failed",
                    error=str(exc),
                    execution_meta=execution_meta,
                )
                write_phase_telemetry(config, phase_telemetry_path, telemetry)
                record_phase_telemetry_path(state, phase_telemetry_path, result)
                write_run_telemetry(config, state)
                write_artifact_manifests(config, state, result)
            write_state(config.state_path, state)
            raise

        apply_phase_result(state, result)
        if phase_telemetry_path and phase_started_at and phase_start_monotonic is not None:
            telemetry = build_phase_telemetry(
                config,
                state,
                phase,
                started_at=phase_started_at,
                elapsed_seconds=round(time.monotonic() - phase_start_monotonic, 3),
                prompt_bytes=phase_prompt_bytes,
                result=result,
                status=result["status"],
                error=None,
                execution_meta=execution_meta,
            )
            write_phase_telemetry(config, phase_telemetry_path, telemetry)
            record_phase_telemetry_path(state, phase_telemetry_path, result)
            write_run_telemetry(config, state)
        write_state(config.state_path, state)
        write_artifact_manifests(config, state, result)

        if config.stop_after_phase == phase:
            return state
        if result["status"] != "completed" or result["next_phase"] in {"done", "stopped"}:
            return state


def validate_state_matches_config(state: dict[str, Any], config: RunnerConfig) -> None:
    if Path(str(state.get("project"))).expanduser().resolve() != config.project:
        raise RunnerError("state project contradicts CLI project")
    if state.get("program_ledger") != config.program_ledger:
        raise RunnerError("state program_ledger contradicts CLI program-ledger")
    if state.get("max_batches") != config.max_batches:
        raise RunnerError("state max_batches contradicts CLI max-batches")
    if state.get("execute_batches") != config.execute_batches:
        raise RunnerError("state execute_batches contradicts CLI execute-batches")


def build_final_summary(state: dict[str, Any], config: RunnerConfig) -> dict[str, Any]:
    receipt: dict[str, Any] = {}
    receipt_path = state.get("last_receipt_path")
    if isinstance(receipt_path, str) and receipt_path:
        try:
            receipt = read_json_object(resolve_project_path(config.project, receipt_path))
        except RunnerError:
            receipt = {}

    return {
        "state_path": str(config.state_path),
        "artifact_root": state.get("artifact_root"),
        "run_telemetry_path": run_telemetry_path(state),
        "last_phase_telemetry_path": state.get("last_phase_telemetry_path"),
        "last_receipt_path": receipt_path,
        "stop_reason": state.get("stop_reason"),
        "batches_completed": state.get("batches_completed"),
        "active_batch": state.get("active_batch_id"),
        "dispatch_path": state.get("dispatch_path"),
        "spec_path": state.get("spec_path"),
        "commit_range": receipt.get("commit_range"),
        "validation_summary": receipt.get("validation_summary"),
        "review_summary": receipt.get("review_summary"),
    }


def print_final_summary(state: dict[str, Any], config: RunnerConfig) -> None:
    print("Final summary:")
    print(json.dumps(build_final_summary(state, config), indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = config_from_args(args)
    try:
        state = run(config)
    except RunnerError as exc:
        print(f"runner error: {exc}", file=sys.stderr)
        try:
            state = load_state(config.state_path)
        except RunnerError:
            state = initial_state(config)
            state["stop_reason"] = str(exc)
        print_final_summary(state, config)
        return 1
    if not config.dry_run:
        print_final_summary(state, config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
