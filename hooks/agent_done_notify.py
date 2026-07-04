#!/usr/bin/env python3
"""Send a compact phone notification when a Codex turn or subagent stops."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_MESSAGE_CHARS = 1400
MAX_LAST_MESSAGE_CHARS = 420
DEFAULT_NTFY_SERVER = "https://ntfy.sh"


@dataclass(frozen=True)
class GitContext:
    repo_root: Path | None
    project: str
    branch: str | None
    commit: str | None
    dirty_count: int | None
    cwd_display: str


@dataclass(frozen=True)
class Notification:
    title: str
    message: str
    tags: str
    priority: str


def run_git(cwd: Path, args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def git_context(cwd: Path) -> GitContext:
    root_raw = run_git(cwd, ["rev-parse", "--show-toplevel"])
    repo_root = Path(root_raw) if root_raw else None
    context_root = repo_root or cwd

    branch = run_git(context_root, ["branch", "--show-current"])
    commit = run_git(context_root, ["rev-parse", "--short", "HEAD"])
    status = run_git(context_root, ["status", "--porcelain=v1"])
    dirty_count = len(status.splitlines()) if status is not None else None

    try:
        cwd_display = str(cwd.relative_to(context_root))
    except ValueError:
        cwd_display = str(cwd)
    if cwd_display == ".":
        cwd_display = "./"

    return GitContext(
        repo_root=repo_root,
        project=context_root.name or str(context_root),
        branch=branch,
        commit=commit,
        dirty_count=dirty_count,
        cwd_display=cwd_display,
    )


def first_line(value: object, *, limit: int) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = " ".join(value.split())
    if not normalized:
        return None
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "..."


def short_id(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value[:12]


def add_line(lines: list[str], label: str, value: object) -> None:
    if value is None or value == "":
        return
    lines.append(f"{label}: {value}")


def build_notification(payload: dict[str, Any]) -> Notification:
    cwd = Path(str(payload.get("cwd") or os.getcwd())).expanduser()
    git = git_context(cwd)
    event = str(payload.get("hook_event_name") or "Codex")
    is_subagent = event == "SubagentStop"

    title_parts = ["Codex"]
    title_parts.append("subagent done" if is_subagent else "done")
    title_parts.append(git.project)
    if git.branch:
        title_parts.append(f"({git.branch})")
    title = " ".join(title_parts)

    lines: list[str] = []
    add_line(lines, "event", event)
    add_line(lines, "project", git.project)
    if git.branch or git.commit:
        ref = " ".join(part for part in (git.branch, git.commit) if part)
        add_line(lines, "ref", ref)
    if git.dirty_count is not None:
        add_line(lines, "dirty", f"{git.dirty_count} file(s)")
    add_line(lines, "cwd", git.cwd_display)
    add_line(lines, "host", socket.gethostname())
    add_line(lines, "model", payload.get("model"))
    add_line(lines, "mode", payload.get("permission_mode"))
    add_line(lines, "session", short_id(payload.get("session_id")))
    add_line(lines, "turn", short_id(payload.get("turn_id")))

    if is_subagent:
        add_line(lines, "agent", payload.get("agent_type"))
        add_line(lines, "agent_id", short_id(payload.get("agent_id")))

    last = first_line(payload.get("last_assistant_message"), limit=MAX_LAST_MESSAGE_CHARS)
    add_line(lines, "last", last)
    add_line(lines, "time", datetime.now(timezone.utc).isoformat(timespec="seconds"))

    message = "\n".join(lines)
    if len(message) > MAX_MESSAGE_CHARS:
        message = message[: MAX_MESSAGE_CHARS - 1].rstrip() + "..."

    return Notification(
        title=title,
        message=message,
        tags="white_check_mark" if not is_subagent else "robot",
        priority=os.environ.get("CODEX_AGENT_NOTIFY_PRIORITY", "default"),
    )


def post_ntfy(notification: Notification) -> bool:
    topic_url = os.environ.get("CODEX_AGENT_NOTIFY_NTFY_URL")
    topic = os.environ.get("CODEX_AGENT_NOTIFY_NTFY_TOPIC")
    if not topic_url and topic:
        server = os.environ.get("CODEX_AGENT_NOTIFY_NTFY_SERVER", DEFAULT_NTFY_SERVER).rstrip("/")
        topic_url = f"{server}/{urllib.parse.quote(topic)}"
    if not topic_url:
        return False

    request = urllib.request.Request(
        topic_url,
        data=notification.message.encode("utf-8"),
        method="POST",
        headers={
            "Title": notification.title,
            "Tags": notification.tags,
            "Priority": notification.priority,
        },
    )
    token = os.environ.get("CODEX_AGENT_NOTIFY_NTFY_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request, timeout=5):
        return True


def post_pushover(notification: Notification) -> bool:
    token = os.environ.get("CODEX_AGENT_NOTIFY_PUSHOVER_TOKEN")
    user = os.environ.get("CODEX_AGENT_NOTIFY_PUSHOVER_USER")
    if not token or not user:
        return False

    body = urllib.parse.urlencode(
        {
            "token": token,
            "user": user,
            "title": notification.title,
            "message": notification.message,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.pushover.net/1/messages.json",
        data=body,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5):
        return True


def post_apprise(notification: Notification) -> bool:
    target = os.environ.get("CODEX_AGENT_NOTIFY_APPRISE_URL")
    if not target:
        return False
    completed = subprocess.run(
        ["apprise", "-t", notification.title, "-b", notification.message, target],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=10,
    )
    return completed.returncode == 0


def notify(notification: Notification) -> None:
    errors: list[str] = []
    for sender in (post_ntfy, post_pushover, post_apprise):
        try:
            if sender(notification):
                return
        except Exception as exc:  # noqa: BLE001 - notification hooks must not break Codex.
            errors.append(f"{sender.__name__}: {exc}")

    if errors:
        log_path = Path(os.environ.get("CODEX_AGENT_NOTIFY_LOG", "/tmp/codex-agent-notify.log"))
        try:
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write("\n".join(errors) + "\n")
        except OSError:
            pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        notify(build_notification(payload))
    except Exception as exc:  # noqa: BLE001 - never make Stop hooks noisy or blocking.
        log_path = Path(os.environ.get("CODEX_AGENT_NOTIFY_LOG", "/tmp/codex-agent-notify.log"))
        try:
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(f"agent_done_notify failed: {exc}\n")
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
