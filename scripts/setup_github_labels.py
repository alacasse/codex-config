#!/usr/bin/env python3
"""Check or create the GitHub labels required by repository tracker adapters."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import cast


@dataclass(frozen=True)
class LabelSpec:
    """Approved metadata for one label this script may create."""

    name: str
    description: str
    color: str


@dataclass(frozen=True)
class ExistingLabel:
    """Live metadata returned by GitHub for an existing label."""

    name: str
    description: str | None
    color: str


@dataclass(frozen=True)
class LabelPlan:
    """Missing presence-only labels and approved label creations."""

    missing_retained: tuple[str, ...]
    create: tuple[LabelSpec, ...]

    @property
    def complete(self) -> bool:
        return not self.missing_retained and not self.create


class LabelSetupError(RuntimeError):
    """Raised when GitHub returns malformed label data."""


Executor = Callable[[list[str]], subprocess.CompletedProcess[str]]

RETAINED_LABELS = (
    "bug",
    "enhancement",
    "ready-for-agent",
    "wontfix",
)

CREATABLE_LABELS = (
    LabelSpec(
        "needs-triage",
        "Maintainer needs to evaluate this issue",
        "fbca04",
    ),
    LabelSpec(
        "needs-info",
        "Waiting on reporter for more information",
        "d876e3",
    ),
    LabelSpec(
        "ready-for-human",
        "Requires human implementation",
        "1d76db",
    ),
    LabelSpec(
        "wayfinder:map",
        "Wayfinder map for a multi-session planning effort",
        "5319e7",
    ),
    LabelSpec(
        "wayfinder:research",
        "Wayfinder AFK research ticket",
        "0075ca",
    ),
    LabelSpec(
        "wayfinder:prototype",
        "Wayfinder HITL prototype ticket",
        "a2eeef",
    ),
    LabelSpec(
        "wayfinder:grilling",
        "Wayfinder HITL decision interview ticket",
        "d876e3",
    ),
    LabelSpec(
        "wayfinder:task",
        "Wayfinder prerequisite task ticket",
        "fbca04",
    ),
)


def explicit_repository(value: str) -> str:
    """Require an explicit OWNER/REPO identifier."""
    parts = value.split("/")
    if len(parts) != 2 or not all(parts) or any(char.isspace() for char in value):
        raise argparse.ArgumentTypeError("repository must use the form OWNER/REPO")
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check or create labels required by codex-config tracker adapters."
    )
    parser.add_argument(
        "--repo",
        required=True,
        type=explicit_repository,
        help="Explicit GitHub repository in OWNER/REPO form.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create missing labels that have approved metadata.",
    )
    return parser.parse_args(argv)


def label_list_command(repo: str) -> list[str]:
    return [
        "gh",
        "label",
        "list",
        "--repo",
        repo,
        "--limit",
        "200",
        "--json",
        "name,description,color",
    ]


def label_create_command(repo: str, spec: LabelSpec) -> list[str]:
    return [
        "gh",
        "label",
        "create",
        spec.name,
        "--repo",
        repo,
        "--description",
        spec.description,
        "--color",
        spec.color,
    ]


def execute_gh(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def checked_output(command: list[str], execute: Executor) -> str:
    completed = execute(command)
    if completed.returncode != 0:
        raise subprocess.CalledProcessError(
            completed.returncode,
            command,
            output=completed.stdout,
            stderr=completed.stderr,
        )
    return completed.stdout


def parse_labels(raw_json: str) -> dict[str, ExistingLabel]:
    try:
        raw: object = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise LabelSetupError(f"GitHub label output is not valid JSON: {exc}") from exc
    if not isinstance(raw, list):
        raise LabelSetupError("GitHub label output must be a JSON array")

    labels: dict[str, ExistingLabel] = {}
    for raw_item in cast(list[object], raw):
        if not isinstance(raw_item, dict):
            raise LabelSetupError("each GitHub label must be a JSON object")
        item = cast(dict[str, object], raw_item)
        name = item.get("name")
        description = item.get("description")
        color = item.get("color")
        if not isinstance(name, str) or not name:
            raise LabelSetupError("each GitHub label must have a name")
        if description is not None and not isinstance(description, str):
            raise LabelSetupError(f"label {name} has an invalid description")
        if not isinstance(color, str) or not color:
            raise LabelSetupError(f"label {name} has an invalid color")
        labels[name] = ExistingLabel(name, description, color)
    return labels


def plan_labels(existing: dict[str, ExistingLabel]) -> LabelPlan:
    missing_retained = tuple(name for name in RETAINED_LABELS if name not in existing)
    create = tuple(spec for spec in CREATABLE_LABELS if spec.name not in existing)
    return LabelPlan(missing_retained=missing_retained, create=create)


def inspect_labels(repo: str, execute: Executor) -> LabelPlan:
    return plan_labels(read_labels(repo, execute))


def read_labels(repo: str, execute: Executor) -> dict[str, ExistingLabel]:
    raw_json = checked_output(label_list_command(repo), execute)
    return parse_labels(raw_json)


def apply_plan(repo: str, plan: LabelPlan, execute: Executor) -> None:
    for spec in plan.create:
        try:
            checked_output(label_create_command(repo, spec), execute)
        except subprocess.CalledProcessError:
            if spec.name in read_labels(repo, execute):
                continue
            raise


def print_plan(repo: str, plan: LabelPlan, *, applying: bool) -> None:
    if plan.complete:
        print(f"labels complete for {repo}")
        return
    for name in plan.missing_retained:
        print(f"missing retained label: {name}")
    verb = "create" if applying else "would create"
    for spec in plan.create:
        command = shlex.join(label_create_command(repo, spec))
        print(f"{verb}: {command}")


def main(argv: Sequence[str] | None = None, execute: Executor = execute_gh) -> int:
    args = parse_args(argv)
    repo = cast(str, args.repo)
    applying = cast(bool, args.apply)
    try:
        plan = inspect_labels(repo, execute)
        print_plan(repo, plan, applying=applying)
        if not applying:
            return 0 if plan.complete else 1

        apply_plan(repo, plan, execute)
        final_plan = inspect_labels(repo, execute)
        if not final_plan.complete:
            print_plan(repo, final_plan, applying=False)
            return 1
        print(f"labels complete for {repo}")
        return 0
    except (LabelSetupError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
