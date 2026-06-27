"""Observed execution metadata for architecture runner phases."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


CODEX_SESSION_ID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class PhaseExecutionObservation:
    exit_code: int
    stdout_bytes: int
    stderr_bytes: int
    codex_session_id: str | None
    codex_session_path: str | None

    def as_execution_meta(self) -> dict[str, int | str | None]:
        return {
            "exit_code": self.exit_code,
            "stdout_bytes": self.stdout_bytes,
            "stderr_bytes": self.stderr_bytes,
            "codex_session_id": self.codex_session_id,
            "codex_session_path": self.codex_session_path,
        }


def build_phase_execution_observation(
    *,
    exit_code: int,
    stdout: str,
    stderr: str,
    subprocess_env: Mapping[str, str] | None = None,
    codex_home_env: Mapping[str, str] | None = None,
) -> PhaseExecutionObservation:
    session_id = extract_codex_session_id(f"{stdout}\n{stderr}")
    return PhaseExecutionObservation(
        exit_code=exit_code,
        stdout_bytes=len(stdout.encode("utf-8")),
        stderr_bytes=len(stderr.encode("utf-8")),
        codex_session_id=session_id,
        codex_session_path=discover_codex_session_path(
            session_id,
            codex_home_env if codex_home_env is not None else subprocess_env,
        ),
    )


def extract_codex_session_id(text: str) -> str | None:
    match = CODEX_SESSION_ID_RE.search(text)
    return match.group(0) if match else None


def discover_codex_session_path(
    session_id: str | None, subprocess_env: Mapping[str, str] | None = None
) -> str | None:
    if not session_id:
        return None
    codex_home = effective_codex_home(subprocess_env)
    sessions_root = codex_home / "sessions"
    try:
        if not sessions_root.exists():
            return None
        matches = [
            path
            for path in sessions_root.rglob("*.jsonl")
            if path.is_file() and session_id.lower() in path.name.lower()
        ]
    except (OSError, RuntimeError):
        return None
    if len(matches) != 1:
        return None
    return str(matches[0])


def effective_codex_home(subprocess_env: Mapping[str, str] | None = None) -> Path:
    if subprocess_env is not None:
        value = subprocess_env.get("CODEX_HOME")
        if value:
            return Path(value).expanduser()
    return Path.home() / ".codex"
