#!/usr/bin/env python3
"""Run architecture-program phases through fresh Codex exec processes."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping


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

RUNNER_VERSION = "local-runner-v1"
PHASES = ("select-dispatch", "create-spec", "execute", "closeout")
NEXT_PHASES = (*PHASES, "done", "stopped")
STATUSES = ("completed", "stopped", "failed")
REQUIRED_RESULT_FIELDS = (
    "status",
    "phase",
    "next_phase",
    "stop_reason",
    "program_ledger",
    "batch_id",
    "dispatch_path",
    "spec_path",
    "receipt_path",
    "commit_range",
    "validation_summary",
    "review_summary",
    "evidence_paths",
)


class RunnerError(RuntimeError):
    """Raised for runner failures that should stop safely."""


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
    state_path = resolve_state_path(project, args.program_ledger, args.state)
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
    )


def resolve_state_path(project: Path, program_ledger: str, value: str | None) -> Path:
    if value:
        path = Path(value).expanduser()
        return path if path.is_absolute() else project / path
    ledger_dir = Path(program_ledger).parent
    return project / ledger_dir / "architecture-program-run-state.json"


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def initial_state(config: RunnerConfig) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "runner_version": RUNNER_VERSION,
        "project": str(config.project),
        "program_ledger": config.program_ledger,
        "max_batches": config.max_batches,
        "execute_batches": config.execute_batches,
        "batches_completed": 0,
        "active_phase": "select-dispatch",
        "active_batch_id": None,
        "dispatch_path": None,
        "spec_path": None,
        "last_receipt_path": None,
        "last_codex_session": None,
        "last_phase_status": None,
        "stop_reason": None,
        "updated_at": None,
    }


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunnerError(f"state file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunnerError(f"state file is not valid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"state file must contain a JSON object: {path}")
    validate_state(data)
    return data


def validate_state(state: dict[str, Any]) -> None:
    if state.get("schema_version") != 1:
        raise RunnerError("state schema_version must be 1")
    if state.get("runner_version") != RUNNER_VERSION:
        raise RunnerError(f"state runner_version must be {RUNNER_VERSION}")
    if state.get("active_phase") not in PHASES:
        raise RunnerError("state active_phase is invalid")
    max_batches = state.get("max_batches")
    if max_batches is not None:
        if not isinstance(max_batches, int) or max_batches < 1:
            raise RunnerError("state max_batches must be a positive integer or null")
    if not isinstance(state.get("batches_completed"), int):
        raise RunnerError("state batches_completed must be an integer")
    if state["batches_completed"] < 0:
        raise RunnerError("state batches_completed must be non-negative")


def write_state(path: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        tmp_path = Path(handle.name)
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp_path, path)


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunnerError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunnerError(f"JSON file is malformed: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"JSON file must contain an object: {path}")
    return data


def validate_phase_result(
    result: dict[str, Any],
    *,
    current_phase: str | None = None,
    state: dict[str, Any] | None = None,
) -> None:
    missing = [field for field in REQUIRED_RESULT_FIELDS if field not in result]
    if missing:
        raise RunnerError(f"phase result missing required field(s): {', '.join(missing)}")

    extra = sorted(set(result) - set(REQUIRED_RESULT_FIELDS))
    if extra:
        raise RunnerError(f"phase result has unsupported field(s): {', '.join(extra)}")

    if result["status"] not in STATUSES:
        raise RunnerError(f"invalid phase status: {result['status']!r}")
    if result["phase"] not in PHASES:
        raise RunnerError(f"invalid phase: {result['phase']!r}")
    if result["next_phase"] not in NEXT_PHASES:
        raise RunnerError(f"invalid next_phase: {result['next_phase']!r}")

    if current_phase is not None and result["phase"] != current_phase:
        raise RunnerError(
            f"phase result phase {result['phase']!r} does not match active phase {current_phase!r}"
        )

    validate_nullable_string(result, "stop_reason")
    validate_required_string(result, "program_ledger")
    validate_nullable_string(result, "batch_id")
    validate_nullable_string(result, "dispatch_path")
    validate_nullable_string(result, "spec_path")
    validate_required_string(result, "receipt_path")
    validate_nullable_string(result, "commit_range")
    validate_summary(result, "validation_summary")
    validate_summary(result, "review_summary")

    evidence_paths = result["evidence_paths"]
    if not isinstance(evidence_paths, list) or not all(
        isinstance(path, str) for path in evidence_paths
    ):
        raise RunnerError("evidence_paths must be an array of strings")

    status = result["status"]
    next_phase = result["next_phase"]
    if status in {"stopped", "failed"} and next_phase != "stopped":
        raise RunnerError(f"status={status} must use next_phase=stopped")
    if status == "completed" and next_phase == "stopped":
        raise RunnerError("status=completed must not use next_phase=stopped")

    if state is not None:
        validate_result_against_state(result, state)


def validate_required_string(result: dict[str, Any], field: str) -> None:
    value = result[field]
    if not isinstance(value, str) or not value:
        raise RunnerError(f"{field} must be a non-empty string")


def validate_nullable_string(result: dict[str, Any], field: str) -> None:
    value = result[field]
    if value is not None and not isinstance(value, str):
        raise RunnerError(f"{field} must be a string or null")


def validate_summary(result: dict[str, Any], field: str) -> None:
    value = result[field]
    if value is not None and not isinstance(value, str):
        raise RunnerError(f"{field} must be a string or null")


def validate_result_against_state(result: dict[str, Any], state: dict[str, Any]) -> None:
    if result["program_ledger"] != state["program_ledger"]:
        raise RunnerError("phase result program_ledger contradicts runner state")

    if result["batch_id"] and state.get("active_batch_id"):
        if result["batch_id"] != state["active_batch_id"]:
            raise RunnerError("phase result batch_id contradicts runner state")
    if result["dispatch_path"] and state.get("dispatch_path"):
        if result["dispatch_path"] != state["dispatch_path"]:
            raise RunnerError("phase result dispatch_path contradicts runner state")
    if result["spec_path"] and state.get("spec_path"):
        if result["spec_path"] != state["spec_path"]:
            raise RunnerError("phase result spec_path contradicts runner state")

    status = result["status"]
    if status != "completed":
        return

    expected = expected_next_phases(result["phase"], state)
    if result["next_phase"] not in expected:
        allowed = ", ".join(sorted(expected))
        raise RunnerError(
            f"phase {result['phase']} cannot advance to {result['next_phase']}; "
            f"expected one of: {allowed}"
        )


def expected_next_phases(phase: str, state: dict[str, Any]) -> set[str]:
    if phase == "select-dispatch":
        return {"create-spec"}
    if phase == "create-spec":
        return {"execute"} if state.get("execute_batches") else {"done"}
    if phase == "execute":
        return {"closeout"}
    if phase == "closeout":
        max_batches = state.get("max_batches")
        completed = int(state.get("batches_completed", 0)) + 1
        if max_batches is not None and completed >= int(max_batches):
            return {"done"}
        return {"select-dispatch", "done"}
    raise RunnerError(f"unknown phase: {phase}")


def resolve_project_path(project: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else project / path


def project_relative(project: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(project.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def validate_receipt(result: dict[str, Any], config: RunnerConfig, state: dict[str, Any]) -> None:
    receipt_path = resolve_project_path(config.project, result["receipt_path"])
    receipt = read_json_object(receipt_path)
    validate_phase_result(receipt, current_phase=result["phase"], state=state)
    if receipt != result:
        raise RunnerError("receipt content does not match final phase result")


def build_prompt(config: RunnerConfig, state: dict[str, Any], phase: str) -> str:
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
            f"- dispatch_path: {state.get('dispatch_path')}",
            f"- spec_path: {state.get('spec_path')}",
            f"- last_receipt_path: {state.get('last_receipt_path')}",
            "",
            "Return schema-valid JSON as the final response.",
            "Write the same JSON object to a compact phase receipt file.",
            "Return the receipt path in receipt_path.",
            "Use compact strings or null for validation_summary and review_summary.",
            "Do not parse or edit runner state directly.",
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
                "- Update runner telemetry receipt.",
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
    config: RunnerConfig, phase: str, prompt: str, output_last_message: Path
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


def sandbox_for_phase(config: RunnerConfig, phase: str) -> str:
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


def env_override_key_label(config: RunnerConfig) -> str:
    keys = [key for key, _value in config.env_overrides]
    return ", ".join(dict.fromkeys(keys))


def execute_codex_phase(config: RunnerConfig, state: dict[str, Any], phase: str) -> dict[str, Any]:
    prompt = build_prompt(config, state, phase)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", prefix="architecture-program-runner-", suffix=".json"
    ) as handle:
        output_last_message = Path(handle.name)
        command = build_codex_command(config, phase, prompt, output_last_message)
        completed = subprocess.run(
            command,
            cwd=config.project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=build_subprocess_env(config.env_overrides),
        )
        if completed.returncode != 0:
            raise RunnerError(
                "codex exec failed for "
                f"{phase} with exit {completed.returncode}\n{completed.stderr.strip()}"
            )
        return read_json_object(output_last_message)


def print_dry_run(config: RunnerConfig, state: dict[str, Any]) -> None:
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


def git_status_lines(project: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=project,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RunnerError(f"git status failed in {project}: {completed.stderr.strip()}")
    return [line for line in completed.stdout.splitlines() if line]


def dirty_paths_from_status(lines: Iterable[str]) -> list[str]:
    paths: list[str] = []
    for line in lines:
        if len(line) < 4:
            continue
        raw = line[3:].strip()
        if " -> " in raw:
            before, after = raw.split(" -> ", 1)
            paths.extend([before.strip('"'), after.strip('"')])
        else:
            paths.append(raw.strip('"'))
    return paths


def expected_dirty_paths(
    config: RunnerConfig,
    state: dict[str, Any],
    phase: str,
    *,
    extra_paths: Iterable[str] = (),
) -> set[str]:
    expected: set[str] = {project_relative(config.project, config.state_path)}
    for value in extra_paths:
        expected.add(project_relative(config.project, resolve_project_path(config.project, value)))

    for field in ("last_receipt_path",):
        if state.get(field):
            expected.add(
                project_relative(config.project, resolve_project_path(config.project, state[field]))
            )
    if state.get("last_receipt_path"):
        try:
            receipt = read_json_object(
                resolve_project_path(config.project, state["last_receipt_path"])
            )
        except RunnerError:
            receipt = {}
        if (
            receipt.get("status") == "stopped"
            and receipt.get("phase") == phase
            and isinstance(receipt.get("evidence_paths"), list)
        ):
            for value in receipt["evidence_paths"]:
                if isinstance(value, str):
                    expected.add(
                        project_relative(config.project, resolve_project_path(config.project, value))
                    )

    if phase == "select-dispatch":
        for field in ("dispatch_path",):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    elif phase == "create-spec":
        for field in ("dispatch_path", "spec_path"):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    elif phase == "execute":
        for field in ("spec_path", "dispatch_path"):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    elif phase == "closeout":
        expected.add(config.program_ledger)
        for field in ("spec_path", "last_receipt_path"):
            if state.get(field):
                expected.add(
                    project_relative(config.project, resolve_project_path(config.project, state[field]))
                )
    return {path for path in expected if path and path != "."}


def check_worktree(
    config: RunnerConfig,
    state: dict[str, Any],
    phase: str,
    *,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
    extra_paths: Iterable[str] = (),
) -> None:
    dirty = dirty_paths_from_status(status_reader(config.project))
    if not dirty:
        return
    expected = expected_dirty_paths(config, state, phase, extra_paths=extra_paths)
    unexpected = [path for path in dirty if not path_is_expected(path, expected)]
    if unexpected:
        raise RunnerError(
            "dirty files cannot be classified as expected for "
            f"{phase}: {', '.join(unexpected)}"
        )


def path_is_expected(path: str, expected: set[str]) -> bool:
    normalized = path.rstrip("/")
    for candidate in expected:
        candidate = candidate.rstrip("/")
        if normalized == candidate:
            return True
        if normalized.startswith(candidate + "/"):
            return True
        if candidate.startswith(normalized + "/"):
            return True
    return False


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


def apply_phase_result(state: dict[str, Any], result: dict[str, Any]) -> None:
    phase = result["phase"]
    state["last_receipt_path"] = result["receipt_path"]
    state["last_phase_status"] = result["status"]
    state["stop_reason"] = result["stop_reason"]

    if result["batch_id"]:
        state["active_batch_id"] = result["batch_id"]
    if result["dispatch_path"]:
        state["dispatch_path"] = result["dispatch_path"]
    if result["spec_path"]:
        state["spec_path"] = result["spec_path"]

    if result["status"] != "completed":
        state["stop_reason"] = result["stop_reason"] or result["status"]
        return

    if phase == "closeout":
        state["batches_completed"] += 1
        if result["next_phase"] == "select-dispatch":
            state["active_batch_id"] = None
            state["dispatch_path"] = None
            state["spec_path"] = None

    if result["next_phase"] in PHASES:
        state["active_phase"] = result["next_phase"]
    else:
        state["stop_reason"] = result["next_phase"]


def is_terminal_completed_state(state: dict[str, Any]) -> bool:
    return state.get("last_phase_status") == "completed" and state.get(
        "stop_reason"
    ) in {"done", "max_batches_reached"}


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
        try:
            check_required_artifacts(config, state)
            check_worktree(config, state, phase, status_reader=status_reader)
            result = phase_executor(config, state, phase)
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
            state["last_phase_status"] = "failed"
            state["stop_reason"] = str(exc)
            write_state(config.state_path, state)
            raise

        apply_phase_result(state, result)
        write_state(config.state_path, state)

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
