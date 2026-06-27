"""Change Allowance ownership for architecture-program runner dirty paths."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable, Iterable

try:
    from scripts import architecture_program_runner_state as _runner_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_state as _runner_state

RunnerError = _runner_state.RunnerError
project_relative = _runner_state.project_relative
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path


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


def expected_change_allowance_paths(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    extra_paths: Iterable[str] = (),
) -> set[str]:
    expected: set[str] = {project_relative(config.project, config.state_path)}
    if state.get("artifact_root"):
        expected.add(str(state["artifact_root"]))
    for field in (
        "run_manifest_path",
        "batch_manifest_path",
        "active_batch_artifact_root",
    ):
        if state.get(field):
            expected.add(str(state[field]))
    for value in extra_paths:
        expected.add(
            project_relative(config.project, resolve_project_path(config.project, value))
        )

    for field in ("last_receipt_path",):
        if state.get(field):
            expected.add(
                project_relative(
                    config.project, resolve_project_path(config.project, state[field])
                )
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
                        project_relative(
                            config.project, resolve_project_path(config.project, value)
                        )
                    )

    if phase == "select-dispatch":
        for field in ("dispatch_path",):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    elif phase == "create-spec":
        for field in ("dispatch_path", "spec_path"):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    elif phase == "execute":
        for field in ("spec_path", "dispatch_path"):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    elif phase == "closeout":
        expected.add(config.program_ledger)
        for field in ("spec_path", "last_receipt_path"):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    return {path for path in expected if path and path != "."}


def expected_dirty_paths(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    extra_paths: Iterable[str] = (),
) -> set[str]:
    return expected_change_allowance_paths(config, state, phase, extra_paths=extra_paths)


def check_change_allowance_path(path: str, expected: set[str]) -> bool:
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


def path_is_expected(path: str, expected: set[str]) -> bool:
    return check_change_allowance_path(path, expected)


def check_change_allowance(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
    extra_paths: Iterable[str] = (),
) -> None:
    dirty = dirty_paths_from_status(status_reader(config.project))
    if not dirty:
        return
    expected = expected_change_allowance_paths(config, state, phase, extra_paths=extra_paths)
    unexpected = [path for path in dirty if not check_change_allowance_path(path, expected)]
    if unexpected:
        raise RunnerError(
            "dirty files cannot be classified as expected for "
            f"{phase}: {', '.join(unexpected)}"
        )


def check_worktree(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
    extra_paths: Iterable[str] = (),
) -> None:
    check_change_allowance(
        config,
        state,
        phase,
        status_reader=status_reader,
        extra_paths=extra_paths,
    )
