from __future__ import annotations

import json
import subprocess

import pytest

from scripts.setup_github_labels import (
    CREATABLE_LABELS,
    RETAINED_LABELS,
    ExistingLabel,
    LabelSpec,
    apply_plan,
    inspect_labels,
    label_create_command,
    label_list_command,
    main,
    parse_labels,
    plan_labels,
)


REPO = "alacasse/codex-config"


def completed(command: list[str], stdout: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")


def label_json(names: set[str]) -> str:
    return json.dumps(
        [
            {
                "name": name,
                "description": f"live metadata for {name}",
                "color": "ffffff",
            }
            for name in sorted(names)
        ]
    )


def test_commands_are_explicit_and_creation_metadata_is_exact() -> None:
    assert label_list_command(REPO) == [
        "gh",
        "label",
        "list",
        "--repo",
        REPO,
        "--limit",
        "200",
        "--json",
        "name,description,color",
    ]
    assert CREATABLE_LABELS == (
        LabelSpec("needs-triage", "Maintainer needs to evaluate this issue", "fbca04"),
        LabelSpec(
            "needs-info", "Waiting on reporter for more information", "d876e3"
        ),
        LabelSpec("ready-for-human", "Requires human implementation", "1d76db"),
        LabelSpec(
            "wayfinder:map",
            "Wayfinder map for a multi-session planning effort",
            "5319e7",
        ),
        LabelSpec(
            "wayfinder:research", "Wayfinder AFK research ticket", "0075ca"
        ),
        LabelSpec(
            "wayfinder:prototype", "Wayfinder HITL prototype ticket", "a2eeef"
        ),
        LabelSpec(
            "wayfinder:grilling",
            "Wayfinder HITL decision interview ticket",
            "d876e3",
        ),
        LabelSpec("wayfinder:task", "Wayfinder prerequisite task ticket", "fbca04"),
    )
    for spec in CREATABLE_LABELS:
        assert label_create_command(REPO, spec) == [
            "gh",
            "label",
            "create",
            spec.name,
            "--repo",
            REPO,
            "--description",
            spec.description,
            "--color",
            spec.color,
        ]


def test_parse_labels_preserves_existing_live_metadata() -> None:
    labels = parse_labels(
        '[{"name":"bug","description":"live bug","color":"d73a4a"}]'
    )

    assert labels == {
        "bug": ExistingLabel("bug", "live bug", "d73a4a"),
    }


def test_inspection_detects_the_eight_creatable_labels() -> None:
    def execute(command: list[str]) -> subprocess.CompletedProcess[str]:
        return completed(command, label_json(set(RETAINED_LABELS)))

    plan = inspect_labels(REPO, execute)

    assert plan.missing_retained == ()
    assert plan.create == CREATABLE_LABELS


def test_check_mode_never_creates_labels() -> None:
    calls: list[list[str]] = []

    def execute(command: list[str]) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return completed(command, label_json(set(RETAINED_LABELS)))

    assert main(["--repo", REPO], execute) == 1
    assert calls == [label_list_command(REPO)]


def test_existing_names_are_idempotent_without_metadata_changes() -> None:
    all_names = set(RETAINED_LABELS) | {spec.name for spec in CREATABLE_LABELS}
    existing = parse_labels(label_json(all_names))

    assert plan_labels(existing).complete


def test_apply_creates_only_missing_approved_labels_and_verifies() -> None:
    existing_names = set(RETAINED_LABELS)
    calls: list[list[str]] = []

    def execute(command: list[str]) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command == label_list_command(REPO):
            return completed(command, label_json(existing_names))
        created_name = command[3]
        existing_names.add(created_name)
        return completed(command)

    assert main(["--repo", REPO, "--apply"], execute) == 0
    expected_creates = [label_create_command(REPO, spec) for spec in CREATABLE_LABELS]
    assert calls == [label_list_command(REPO), *expected_creates, label_list_command(REPO)]
    assert not any("--force" in command or "edit" in command for command in calls)


def test_missing_retained_label_is_never_created() -> None:
    existing = {
        spec.name: ExistingLabel(spec.name, spec.description, spec.color)
        for spec in CREATABLE_LABELS
    }
    plan = plan_labels(existing)
    calls: list[list[str]] = []

    def execute(command: list[str]) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return completed(command)

    apply_plan(REPO, plan, execute)

    assert plan.missing_retained == RETAINED_LABELS
    assert calls == []


def test_apply_treats_a_same_name_creation_race_as_idempotent() -> None:
    spec = CREATABLE_LABELS[0]
    plan = plan_labels({})
    calls: list[list[str]] = []

    def execute(command: list[str]) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command == label_create_command(REPO, spec):
            return subprocess.CompletedProcess(
                command,
                1,
                stdout="",
                stderr="label already exists",
            )
        if command == label_list_command(REPO):
            return completed(command, label_json({spec.name}))
        return completed(command)

    apply_plan(REPO, plan, execute)

    assert calls[:2] == [
        label_create_command(REPO, spec),
        label_list_command(REPO),
    ]


def test_gh_failures_propagate_from_inspection_and_apply() -> None:
    def fail(command: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="gh failed")

    with pytest.raises(subprocess.CalledProcessError):
        inspect_labels(REPO, fail)

    plan = plan_labels({})
    with pytest.raises(subprocess.CalledProcessError):
        apply_plan(REPO, plan, fail)
