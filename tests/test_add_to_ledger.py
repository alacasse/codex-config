from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts.add_to_ledger import (
    _apply_prepared_operation,
    _prepare_operation,
    execute_add_to_ledger,
)
from scripts.planning_contract import (
    InjectedStoreFailure,
    apply_ledger_decision,
    read_ledger_document,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_FIXTURE = (
    REPO_ROOT / "tests/fixtures/planning-contracts/ledger/per-finding-valid/LEDGER.md"
)
HEAD = subprocess.check_output(
    ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"], text=True
).strip()


def _copy_ledger(tmp_path: Path) -> Path:
    path = tmp_path / "LEDGER.md"
    shutil.copy2(LEDGER_FIXTURE, path)
    return path


def _empty_ledger(tmp_path: Path) -> Path:
    path = tmp_path / "LEDGER.md"
    path.write_text(
        """# Planning Ledger

## Store Metadata

```yaml
interface: ledger-store/v1
store_revision: 0
replay_records: []
```

## Derived Index

```yaml
interface: planning-derived-index/v1
source_artifact: LEDGER.md
source_revision: 0
findings: []
```
"""
    )
    return path


def _context(
    tmp_path: Path,
    ledger: Path,
    *,
    namespace: str | None = None,
) -> dict[str, object]:
    return {
        "toolchain_generation": "candidate",
        "toolchain_commit": HEAD,
        "toolchain_root": str(REPO_ROOT),
        "canonical_planning_repository_root": str(REPO_ROOT),
        "canonical_planning_commit": HEAD,
        "planning_root": str(tmp_path),
        "ledger_path": str(ledger),
        "operation_root_kind": "temporary",
        "canonical_state_mutation_allowed": False,
        "project_namespace": namespace,
    }


def _plain_input(
    text: str,
    *,
    title: str = "Proposed finding",
    included: list[str] | None = None,
    evidence: list[str] | None = None,
    explicit_target: str | None = None,
) -> dict[str, object]:
    return {
        "source": {"type": "plain_text", "text": text},
        "title": title,
        "scope": {
            "summary": "Bounded scope",
            "included": included or ["implementation"],
            "excluded": ["follow-on work"],
        },
        "evidence_pointers": evidence or [],
        "next_action": {"command": "plan-batch", "condition": "explicit_request"},
        "explicit_target_finding_id": explicit_target,
        "non_intake_changes": [],
    }


def _github_input(
    *,
    owner: str = "OpenAI",
    repository: str = "Codex",
    issue_title: str = "  Reproducible\tbug  ",
    body: str = "Body with spaces.  \r\n\r\n",
) -> dict[str, object]:
    value = _plain_input("unused", title="GitHub-backed finding")
    value["source"] = {
        "type": "github_issue",
        "owner": owner,
        "repository": repository,
        "number": 42,
        "title": issue_title,
        "body": body,
    }
    return value


def _request(
    tmp_path: Path,
    ledger: Path,
    inputs: list[dict[str, object]],
    *,
    namespace: str | None = None,
) -> dict[str, object]:
    return {
        "interface": "add-to-ledger/v1",
        "context": _context(tmp_path, ledger, namespace=namespace),
        "inputs": inputs,
    }


def _thaw(value: Mapping[str, object]) -> dict[str, Any]:
    def thaw(child: object) -> Any:
        if isinstance(child, Mapping):
            return {str(key): thaw(item) for key, item in child.items()}
        if isinstance(child, tuple | list):
            return [thaw(item) for item in child]
        return child

    return thaw(value)


def _write_ledger_with_ids(tmp_path: Path, ids: tuple[str, str]) -> Path:
    snapshot = read_ledger_document(LEDGER_FIXTURE, toolchain_root=REPO_ROOT)
    id_map = {"CCFG-1": ids[0], "CCFG-2": ids[1]}
    findings: list[dict[str, Any]] = []
    for old_id in ("CCFG-1", "CCFG-2"):
        finding = _thaw(snapshot.findings[old_id])
        finding["id"] = id_map[old_id]
        finding["dependencies"] = [
            id_map.get(dependency, dependency)
            for dependency in finding["dependencies"]
        ]
        findings.append(finding)
    findings.sort(key=lambda finding: finding["id"])
    derived = {
        "interface": "planning-derived-index/v1",
        "source_artifact": "LEDGER.md",
        "source_revision": 1,
        "findings": [
            {
                "id": finding["id"],
                "revision": finding["revision"],
                "title": finding["title"],
                "status": finding["lifecycle"]["status"],
            }
            for finding in findings
        ],
    }
    sections = [
        "# Planning Ledger",
        "",
        "## Store Metadata",
        "",
        "```yaml",
        "interface: ledger-store/v1\nstore_revision: 1\nreplay_records: []",
        "```",
        "",
        "## Derived Index",
        "",
        "```yaml",
        yaml.safe_dump(derived, sort_keys=False).rstrip(),
        "```",
    ]
    for finding in findings:
        sections.extend(
            [
                "",
                f"## Finding {finding['id']}",
                "",
                "```yaml",
                yaml.safe_dump(finding, sort_keys=False).rstrip(),
                "```",
            ]
        )
    path = tmp_path / "LEDGER.md"
    path.write_text("\n".join(sections) + "\n")
    read_ledger_document(path, toolchain_root=REPO_ROOT)
    return path


def _initialize_git_repository(path: Path) -> str:
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(path),
            "-c",
            "user.name=Slice Test",
            "-c",
            "user.email=slice-test@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ],
        check=True,
    )
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def test_multi_create_allocates_consecutively_from_one_complete_snapshot(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    request = _request(
        tmp_path,
        ledger,
        [
            _plain_input("source z", title="Z", included=[" z ", "a", "a"]),
            _plain_input("source a", title="A"),
        ],
    )

    result = execute_add_to_ledger(request)
    after = read_ledger_document(ledger, toolchain_root=REPO_ROOT)

    assert result["outcome"] == "applied"
    assert result["write_status"] == "written"
    assert result["affected_finding_ids"] == ["CCFG-3", "CCFG-4"]
    assert set(after.findings) == {"CCFG-1", "CCFG-2", "CCFG-3", "CCFG-4"}
    created = [after.findings[finding_id] for finding_id in ("CCFG-3", "CCFG-4")]
    assert all(
        str(finding["provenance"]["source_id"]).startswith("text:sha256:")  # type: ignore[index]
        for finding in created
    )
    assert {finding["producer"]["toolchain_commit"] for finding in created} == {HEAD}  # type: ignore[index]
    assert after.logical_revision == 2


def test_mixed_create_update_and_no_op_apply_once_from_one_snapshot(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    initial = execute_add_to_ledger(
        _request(
            tmp_path,
            ledger,
            [
                _plain_input("update source", title="Update before"),
                _plain_input("no-op source", title="No-op stays"),
            ],
        )
    )
    initial_ids = {
        item["source_identity"]: item["finding_id"] for item in initial["inputs"]  # type: ignore[index]
    }
    before = read_ledger_document(ledger, toolchain_root=REPO_ROOT)
    no_op_source = hashlib.sha256(b"no-op source").hexdigest()
    no_op_id = initial_ids[f"text:sha256:{no_op_source}"]
    no_op_before = _thaw(before.findings[no_op_id])

    result = execute_add_to_ledger(
        _request(
            tmp_path,
            ledger,
            [
                _plain_input("create source", title="Created in mix"),
                _plain_input("update source", title="Updated in mix"),
                _plain_input("no-op source", title="No-op stays"),
            ],
        )
    )
    after = read_ledger_document(ledger, toolchain_root=REPO_ROOT)
    per_input = result["inputs"]  # type: ignore[assignment]
    create_id = per_input[0]["finding_id"]  # type: ignore[index]
    update_id = per_input[1]["finding_id"]  # type: ignore[index]

    assert [item["action"] for item in per_input] == ["create", "update", "no-op"]  # type: ignore[index]
    assert result["store"]["outcome"] == "applied"  # type: ignore[index]
    receipt = result["store"]["receipt"]  # type: ignore[index]
    assert receipt["before_revision"] == before.logical_revision
    assert receipt["after_revision"] == before.logical_revision + 1
    assert receipt["touched_finding_ids"] == sorted([create_id, update_id])
    assert after.logical_revision == before.logical_revision + 1
    assert after.findings[create_id]["title"] == "Created in mix"
    assert after.findings[update_id]["title"] == "Updated in mix"
    assert _thaw(after.findings[no_op_id]) == no_op_before


def test_plain_text_adapter_emits_exact_tokens_for_normalized_equivalents(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    canonical = "  Café\nline"
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    result = execute_add_to_ledger(
        _request(
            tmp_path,
            ledger,
            [
                _plain_input("\r\n  Cafe\u0301  \t\r\nline  \t\r\n\r\n"),
                _plain_input("\n  Café\nline\n"),
            ],
        )
    )
    after = read_ledger_document(ledger, toolchain_root=REPO_ROOT)
    finding_id = result["inputs"][0]["finding_id"]  # type: ignore[index]
    provenance = after.findings[finding_id]["provenance"]

    assert [item["source_identity"] for item in result["inputs"]] == [  # type: ignore[index]
        f"text:sha256:{digest}",
        f"text:sha256:{digest}",
    ]
    assert provenance == {
        "source_id": f"text:sha256:{digest}",
        "source_commit": digest[:40],
        "source_section": "inline-text",
    }


def test_github_adapter_canonicalizes_identity_and_coalesces_equivalent_inputs(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    request = _request(
        tmp_path,
        ledger,
        [
            _github_input(),
            _github_input(
                owner="openai",
                repository="codex",
                issue_title="Reproducible bug",
                body="Body with spaces.",
            ),
        ],
    )

    result = execute_add_to_ledger(request)
    after = read_ledger_document(ledger, toolchain_root=REPO_ROOT)

    assert result["outcome"] == "applied"
    assert result["affected_finding_ids"] == ["CCFG-3"]
    assert [item["finding_id"] for item in result["inputs"]] == ["CCFG-3", "CCFG-3"]  # type: ignore[index]
    provenance = after.findings["CCFG-3"]["provenance"]
    revision_payload = {
        "owner": "openai",
        "repository": "codex",
        "number": 42,
        "title": "Reproducible bug",
        "body": "Body with spaces.",
    }
    expected_revision = hashlib.sha256(
        json.dumps(
            revision_payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    ).hexdigest()[:40]
    assert provenance["source_id"] == "github-issue:github.com/openai/codex#42"  # type: ignore[index]
    assert provenance["source_section"] == "https://github.com/openai/codex/issues/42"  # type: ignore[index]
    assert provenance["source_commit"] == expected_revision  # type: ignore[index]


def test_github_issue_revision_change_updates_the_same_source_finding(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    first_request = _request(tmp_path, ledger, [_github_input(body="first body")])
    execute_add_to_ledger(first_request)
    before = read_ledger_document(ledger, toolchain_root=REPO_ROOT)

    changed = execute_add_to_ledger(
        _request(tmp_path, ledger, [_github_input(body="changed body")])
    )
    after = read_ledger_document(ledger, toolchain_root=REPO_ROOT)

    assert changed["inputs"][0]["action"] == "update"  # type: ignore[index]
    assert before.findings["CCFG-3"]["provenance"]["source_id"] == after.findings["CCFG-3"]["provenance"]["source_id"]  # type: ignore[index]
    assert before.findings["CCFG-3"]["provenance"]["source_commit"] != after.findings["CCFG-3"]["provenance"]["source_commit"]  # type: ignore[index]


def test_private_stdin_transport_returns_compact_json_without_raw_source(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    raw_source = "private raw source paragraph"
    request = _request(tmp_path, ledger, [_plain_input(raw_source)])

    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/add_to_ledger.py")],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=True,
    )
    result = json.loads(completed.stdout)

    assert result["outcome"] == "applied"
    assert raw_source not in completed.stdout
    assert result["private_operation_digest"]


def test_symlinked_command_imports_installed_planning_contracts_link(
    tmp_path: Path,
) -> None:
    installed_root = tmp_path / "installed"
    installed_scripts = installed_root / "scripts"
    installed_scripts.mkdir(parents=True)
    add_to_ledger_link = installed_scripts / "add_to_ledger.py"
    planning_contract_link = installed_scripts / "planning_contract.py"
    add_to_ledger_link.symlink_to(REPO_ROOT / "scripts/add_to_ledger.py")
    planning_contract_link.symlink_to(REPO_ROOT / "scripts/planning_contract.py")
    planning_root = tmp_path / "planning"
    planning_root.mkdir()
    ledger = _copy_ledger(planning_root)
    request = _request(
        planning_root,
        ledger,
        [_plain_input("installed topology source")],
    )
    environment = {**dict(os.environ), "PYTHONPATH": ""}

    installed = subprocess.run(
        [sys.executable, str(add_to_ledger_link)],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=True,
        cwd=installed_root,
        env=environment,
    )
    assert json.loads(installed.stdout)["outcome"] == "applied"
    assert planning_contract_link.resolve() == REPO_ROOT / "scripts/planning_contract.py"

    planning_contract_link.unlink()
    missing = subprocess.run(
        [sys.executable, str(add_to_ledger_link)],
        input=json.dumps(request),
        text=True,
        capture_output=True,
        check=False,
        cwd=installed_root,
        env=environment,
    )
    assert missing.returncode != 0
    assert "scripts.planning_contract" in missing.stderr


def test_same_source_create_update_and_later_no_op_reevaluate_current_ledger(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    initial = _request(tmp_path, ledger, [_plain_input("same source", title="Initial")])

    created = execute_add_to_ledger(initial)
    changed_request = _request(
        tmp_path,
        ledger,
        [_plain_input("same source", title="Changed", evidence=["evidence.md"])],
    )
    updated = execute_add_to_ledger(changed_request)
    no_op = execute_add_to_ledger(changed_request)
    after = read_ledger_document(ledger, toolchain_root=REPO_ROOT)

    assert created["outcome"] == "applied"
    assert updated["outcome"] == "applied"
    assert updated["inputs"][0]["action"] == "update"  # type: ignore[index]
    assert no_op["outcome"] == "no-op"
    assert no_op["write_status"] == "not_written"
    assert no_op["private_operation_digest"] is None
    assert after.findings["CCFG-3"]["revision"] == 2
    assert after.logical_revision == 3


def test_existing_evidence_superset_does_not_force_an_update(tmp_path: Path) -> None:
    ledger = _copy_ledger(tmp_path)
    first = _request(
        tmp_path,
        ledger,
        [_plain_input("evidence source", evidence=["b.md", "a.md"])],
    )
    execute_add_to_ledger(first)
    ledger.write_text(
        ledger.read_text().replace(
            "  pointers:\n  - a.md\n  - b.md",
            "  pointers:\n  - b.md\n  - a.md",
            1,
        )
    )

    subset = _request(
        tmp_path,
        ledger,
        [_plain_input("evidence source", evidence=["a.md"])],
    )
    result = execute_add_to_ledger(subset)

    assert result["outcome"] == "no-op"
    assert read_ledger_document(ledger, toolchain_root=REPO_ROOT).logical_revision == 2


@pytest.mark.parametrize("case", ["unsupported", "ambiguous", "cross_source"])
def test_unsupported_ambiguous_and_cross_source_inputs_block_atomically(
    tmp_path: Path,
    case: str,
) -> None:
    ledger = _copy_ledger(tmp_path)
    if case == "unsupported":
        item = _plain_input("unsupported")
        item["source"] = {"type": "external_ticket", "id": "ABC-1"}
        inputs = [_plain_input("valid but atomically blocked"), item]
    elif case == "ambiguous":
        inputs = [
            _plain_input("duplicate source", title="One"),
            _plain_input("duplicate source", title="Two"),
        ]
    else:
        inputs = [_plain_input("new source", explicit_target="CCFG-1")]
    before = ledger.read_bytes()

    result = execute_add_to_ledger(_request(tmp_path, ledger, inputs))

    assert result["outcome"] == "blocked"
    assert result["write_status"] == "not_written"
    assert result["store"] is None
    assert ledger.read_bytes() == before


def test_non_intake_change_blocks_before_store_invocation(tmp_path: Path) -> None:
    ledger = _copy_ledger(tmp_path)
    item = _plain_input("lifecycle request")
    item["non_intake_changes"] = ["demote lifecycle"]
    before = ledger.read_bytes()

    result = execute_add_to_ledger(_request(tmp_path, ledger, [item]))

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "input.non_intake_change"  # type: ignore[index]
    assert ledger.read_bytes() == before


def test_malformed_existing_namespace_blocks_all_creates(tmp_path: Path) -> None:
    ledger = _copy_ledger(tmp_path)
    ledger.write_text(ledger.read_text().replace("CCFG-2", "CCFG-X"))
    before = ledger.read_bytes()

    result = execute_add_to_ledger(
        _request(tmp_path, ledger, [_plain_input("new source")])
    )

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "ledger.malformed_namespace"  # type: ignore[index]
    assert ledger.read_bytes() == before


@pytest.mark.parametrize(
    ("ids", "namespace", "blocker"),
    [
        (("CCFG-1", "OTHER-2"), None, "ledger.mixed_namespace"),
        (("CCFG-1", "CCFG-01"), None, "ledger.duplicate_numeric_slot"),
        (("CCFG-0", "CCFG-2"), None, "ledger.zero_numeric_slot"),
        (None, "OTHER", "ledger.namespace_mismatch"),
    ],
)
def test_namespace_failures_are_precise_and_preserve_the_ledger(
    tmp_path: Path,
    ids: tuple[str, str] | None,
    namespace: str | None,
    blocker: str,
) -> None:
    ledger = (
        _write_ledger_with_ids(tmp_path, ids)
        if ids is not None
        else _copy_ledger(tmp_path)
    )
    before = ledger.read_bytes()

    result = execute_add_to_ledger(
        _request(
            tmp_path,
            ledger,
            [_plain_input("namespace source")],
            namespace=namespace,
        )
    )

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == blocker  # type: ignore[index]
    assert result["store"] is None
    assert ledger.read_bytes() == before


def test_empty_ledger_requires_and_uses_project_authorized_namespace(tmp_path: Path) -> None:
    ledger = _empty_ledger(tmp_path)
    request = _request(tmp_path, ledger, [_plain_input("first")])

    blocked = execute_add_to_ledger(request)
    request["context"]["project_namespace"] = "CCFG"  # type: ignore[index]
    created = execute_add_to_ledger(request)

    assert blocked["outcome"] == "blocked"
    assert blocked["blockers"][0]["code"] == "ledger.empty_namespace"  # type: ignore[index]
    assert created["affected_finding_ids"] == ["CCFG-1"]


def test_stale_complete_snapshot_is_rejected_without_overwriting_concurrent_write(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    prepared = _prepare_operation(
        _request(tmp_path, ledger, [_plain_input("prepared source")])
    )
    snapshot = read_ledger_document(ledger, toolchain_root=REPO_ROOT)
    mutation = _thaw(snapshot.findings["CCFG-1"])
    mutation["revision"] = 2
    mutation["title"] = "Concurrent title"
    apply_ledger_decision(
        ledger,
        toolchain_root=REPO_ROOT,
        expected_revision=snapshot.logical_revision,
        expected_file_hash=snapshot.file_hash,
        action="update",
        finding_mutations=[mutation],
        touched_finding_revisions={"CCFG-1": 1},
        idempotency_key="concurrent-test-write",
    )
    concurrent_bytes = ledger.read_bytes()

    result = _apply_prepared_operation(prepared)

    assert result["outcome"] == "blocked"
    assert "revision_mismatch" in result["blockers"][0]["code"]  # type: ignore[index]
    assert ledger.read_bytes() == concurrent_bytes


def test_exact_prepared_retry_reaches_store_exact_replay(tmp_path: Path) -> None:
    ledger = _copy_ledger(tmp_path)
    prepared = _prepare_operation(
        _request(tmp_path, ledger, [_plain_input("recoverable source")])
    )

    with pytest.raises(InjectedStoreFailure, match="after_replace"):
        _apply_prepared_operation(prepared, fault="after_replace_before_return")
    replayed = _apply_prepared_operation(prepared)

    assert replayed["outcome"] == "exact_replay"
    assert replayed["write_status"] == "exact_replay"
    assert replayed["private_operation_digest"] == prepared.private_operation_digest
    assert read_ledger_document(ledger, toolchain_root=REPO_ROOT).logical_revision == 2


def test_later_invocation_after_interrupted_retry_is_new_semantic_evaluation(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    request = _request(tmp_path, ledger, [_plain_input("later source")])
    prepared = _prepare_operation(request)
    with pytest.raises(InjectedStoreFailure):
        _apply_prepared_operation(prepared, fault="after_replace_before_return")

    later = execute_add_to_ledger(request)

    assert later["outcome"] == "no-op"
    assert later["observed_ledger"]["revision"] == 2  # type: ignore[index]
    assert later["private_operation_digest"] is None


def test_multiple_findings_for_one_source_identity_block_without_write(
    tmp_path: Path,
) -> None:
    ledger = _copy_ledger(tmp_path)
    source_text = "duplicate mapped source"
    source_id = f"text:sha256:{hashlib.sha256(source_text.encode()).hexdigest()}"
    ledger.write_text(
        ledger.read_text()
        .replace("source_id: SRC-1", f"source_id: {source_id}")
        .replace("source_id: SRC-2", f"source_id: {source_id}")
    )
    before = ledger.read_bytes()

    result = execute_add_to_ledger(
        _request(tmp_path, ledger, [_plain_input(source_text)])
    )

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "decision.duplicate_source_identity"  # type: ignore[index]
    assert ledger.read_bytes() == before


def test_candidate_generation_cannot_write_canonical_ledger(tmp_path: Path) -> None:
    canonical_repository = tmp_path / "canonical-repository"
    planning_root = canonical_repository / "docs/plans"
    planning_root.mkdir(parents=True)
    ledger = _copy_ledger(planning_root)
    canonical_commit = _initialize_git_repository(canonical_repository)
    context = {
        "toolchain_generation": "candidate",
        "toolchain_commit": HEAD,
        "toolchain_root": str(REPO_ROOT),
        "canonical_planning_repository_root": str(canonical_repository),
        "canonical_planning_commit": canonical_commit,
        "planning_root": str(planning_root),
        "ledger_path": str(ledger),
        "operation_root_kind": "canonical",
        "canonical_state_mutation_allowed": False,
        "project_namespace": None,
    }
    request = {
        "interface": "add-to-ledger/v1",
        "context": context,
        "inputs": [_plain_input("must not write")],
    }
    before = ledger.read_bytes()

    result = execute_add_to_ledger(request)

    assert result["outcome"] == "blocked"
    assert result["blockers"][0]["code"] == "authority.canonical_candidate_write"  # type: ignore[index]
    assert ledger.read_bytes() == before
