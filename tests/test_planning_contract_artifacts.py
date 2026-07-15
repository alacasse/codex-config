from __future__ import annotations

import hashlib
import shutil
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from scripts.planning_contract import (
    ArtifactLineage,
    InjectedStoreFailure,
    PlanningStoreError,
    ProducerIdentity,
    read_artifact_document,
    validate_planning_contracts,
    write_closeout_artifact,
    write_dispatch_artifact,
    write_runway_artifact,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/planning-contracts/artifacts"
VALID_LINEAGE = FIXTURES / "valid-lineage"
EMPTY_HASH = hashlib.sha256(b"").hexdigest()
COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _thaw(value: object) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(child) for key, child in value.items()}
    if isinstance(value, tuple | list):
        return [_thaw(child) for child in value]
    return value


def _fixture_contracts() -> dict[str, dict[str, Any]]:
    result = validate_planning_contracts([VALID_LINEAGE], toolchain_root=REPO_ROOT)
    assert result.is_valid
    return {
        str(parsed.contract["schema"]): _thaw(parsed.contract)
        for parsed in result.contracts
    }


def _set(contract: dict[str, Any], path: tuple[str, ...], value: object) -> None:
    target = contract
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def _workspace(
    tmp_path: Path,
) -> tuple[ArtifactLineage, dict[str, dict[str, Any]]]:
    planning_root = tmp_path / "plans"
    planning_root.mkdir()
    ledger_path = planning_root / "LEDGER.md"
    dispatch_path = planning_root / "dispatch.md"
    runway_path = planning_root / "runway.md"
    closeout_path = planning_root / "closeout.md"
    ledger_path.write_text("fixture ledger\n")
    contracts = _fixture_contracts()
    dispatch = contracts["planning-dispatch/v1"]
    runway = contracts["planning-runway/v1"]
    closeout = contracts["planning-closeout/v1"]
    dispatch["execution_context"] = {
        "toolchain_source_root": str(tmp_path / "stable"),
        "canonical_planning_repository_root": str(tmp_path),
        "implementation_target_root": str(tmp_path / "candidate"),
    }
    runway["execution"]["implementation_target_root"] = str(tmp_path / "candidate")
    closeout["execution_context"] = {
        "canonical_planning_repository_root": str(tmp_path),
        "implementation_target_root": str(tmp_path / "candidate"),
    }
    lineage = ArtifactLineage(
        planning_root=planning_root,
        program="codex-config",
        batch_id="ccfg-21-artifacts",
        included_finding_ids=("CCFG-21",),
        deferred_finding_ids=(),
        batch_kind="migration",
        ledger_path=ledger_path,
        ledger_revision="b" * 64,
        dispatch_path=dispatch_path,
        dispatch_revision="a" * 64,
        runway_path=runway_path,
        closeout_path=closeout_path,
        toolchain_source_root=tmp_path / "stable",
        canonical_planning_repository_root=tmp_path,
        implementation_target_root=tmp_path / "candidate",
        dispatch_producer=ProducerIdentity("stable", COMMIT, "planning-dispatch/v1"),
        runway_producer=ProducerIdentity("stable", COMMIT, "planning-runway/v1"),
        closeout_producer=ProducerIdentity("stable", COMMIT, "planning-closeout/v1"),
    )
    return lineage, contracts


def _write_dispatch(
    lineage: ArtifactLineage,
    contracts: Mapping[str, Mapping[str, object]],
    *,
    idempotency_key: str = "dispatch-create",
) -> None:
    result = write_dispatch_artifact(
        lineage.dispatch_path,
        toolchain_root=REPO_ROOT,
        expected_revision=0,
        expected_file_hash=EMPTY_HASH,
        contract=contracts["planning-dispatch/v1"],
        lineage=lineage,
        idempotency_key=idempotency_key,
    )
    assert result.outcome == "applied"


def _write_runway(
    lineage: ArtifactLineage,
    contracts: Mapping[str, Mapping[str, object]],
    *,
    idempotency_key: str = "runway-create",
) -> None:
    result = write_runway_artifact(
        lineage.runway_path,
        toolchain_root=REPO_ROOT,
        expected_revision=0,
        expected_file_hash=EMPTY_HASH,
        expected_dispatch_file_hash=_artifact_hash(lineage.dispatch_path),
        contract=contracts["planning-runway/v1"],
        lineage=lineage,
        idempotency_key=idempotency_key,
    )
    assert result.outcome == "applied"


def _artifact_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_catalog_validation_checks_complete_lineage() -> None:
    valid = validate_planning_contracts([VALID_LINEAGE], toolchain_root=REPO_ROOT)
    invalid = validate_planning_contracts(
        [FIXTURES / "invalid-lineage"],
        toolchain_root=REPO_ROOT,
    )

    assert valid.is_valid
    assert {parsed.contract["schema"] for parsed in valid.contracts} == {
        "planning-dispatch/v1",
        "planning-runway/v1",
        "planning-closeout/v1",
    }
    assert [diagnostic.code for diagnostic in invalid.diagnostics] == [
        "artifact.lineage"
    ]
    assert "catalog dispatch revision" in invalid.diagnostics[0].message


@pytest.mark.parametrize(
    ("field", "original", "replacement"),
    [
        ("generation", "toolchain_generation: stable", "toolchain_generation: candidate"),
        (
            "commit",
            f"toolchain_commit: {COMMIT}",
            f"toolchain_commit: {'f' * 40}",
        ),
    ],
)
def test_catalog_rejects_closeout_producer_lineage_mismatch(
    tmp_path: Path,
    field: str,
    original: str,
    replacement: str,
) -> None:
    catalog = tmp_path / "lineage"
    shutil.copytree(VALID_LINEAGE, catalog)
    closeout_path = catalog / "closeout.md"
    before = {path.name: path.read_bytes() for path in catalog.iterdir()}
    text = closeout_path.read_text()
    changed = text.replace(original, replacement, 1)
    assert changed != text
    closeout_path.write_text(changed)
    expected = {**before, "closeout.md": changed.encode()}

    result = validate_planning_contracts([catalog], toolchain_root=REPO_ROOT)

    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "artifact.lineage"
    ]
    assert f"catalog closeout producer {field}" in result.diagnostics[0].message
    assert {path.name: path.read_bytes() for path in catalog.iterdir()} == expected


def test_writes_and_reads_complete_immutable_lineage(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    dispatch_hash = _artifact_hash(lineage.dispatch_path)
    _write_runway(lineage, contracts)
    runway_hash = _artifact_hash(lineage.runway_path)

    result = write_closeout_artifact(
        lineage.closeout_path,
        toolchain_root=REPO_ROOT,
        expected_revision=0,
        expected_file_hash=EMPTY_HASH,
        expected_dispatch_file_hash=dispatch_hash,
        expected_runway_file_hash=runway_hash,
        contract=contracts["planning-closeout/v1"],
        lineage=lineage,
        idempotency_key="closeout-create",
    )
    snapshots = (
        read_artifact_document(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_schema="planning-dispatch/v1",
            expected_producer_identity=lineage.dispatch_producer,
        ),
        read_artifact_document(
            lineage.runway_path,
            toolchain_root=REPO_ROOT,
            expected_schema="planning-runway/v1",
            expected_producer_identity=lineage.runway_producer,
        ),
        read_artifact_document(
            lineage.closeout_path,
            toolchain_root=REPO_ROOT,
            expected_schema="planning-closeout/v1",
            expected_producer_identity=lineage.closeout_producer,
        ),
    )

    assert result.outcome == "applied"
    assert result.receipt.store_interface == "artifact-store/v1"
    assert [snapshot.logical_revision for snapshot in snapshots] == [1, 1, 1]
    assert all("artifact-store/v1" in snapshot.path.read_text() for snapshot in snapshots)
    assert snapshots[1].contract["artifact"]["source_dispatch_revision"] == "a" * 64  # type: ignore[index]
    assert snapshots[2].contract["reconciliation"]["successor_selected"] is False  # type: ignore[index]


def test_dispatch_fault_recovery_replays_without_second_write(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=0,
        expected_file_hash=EMPTY_HASH,
        contract=contracts["planning-dispatch/v1"],
        lineage=lineage,
        idempotency_key="dispatch-recover",
    )
    with pytest.raises(InjectedStoreFailure, match="after_replace"):
        write_dispatch_artifact(
            lineage.dispatch_path,
            **request,
            fault="after_replace_before_return",
        )
    written = lineage.dispatch_path.read_bytes()

    recovered = write_dispatch_artifact(lineage.dispatch_path, **request)

    assert recovered.outcome == "exact_replay"
    assert recovered.receipt.before_revision == 0
    assert recovered.receipt.after_revision == 1
    assert lineage.dispatch_path.read_bytes() == written


def test_dispatch_failure_before_replace_preserves_empty_target(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)

    with pytest.raises(InjectedStoreFailure, match="before_replace"):
        write_dispatch_artifact(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            contract=contracts["planning-dispatch/v1"],
            lineage=lineage,
            idempotency_key="dispatch-before",
            fault="before_replace",
        )

    assert not lineage.dispatch_path.exists()
    assert not tuple(lineage.planning_root.glob(".dispatch.md.*"))


@pytest.mark.parametrize(
    ("expected_revision", "expected_file_hash", "code"),
    [
        (1, EMPTY_HASH, "store.revision_mismatch"),
        (0, "0" * 64, "store.file_hash_mismatch"),
    ],
)
def test_dispatch_target_cas_mismatch_rejects_without_creation(
    tmp_path: Path,
    expected_revision: int,
    expected_file_hash: str,
    code: str,
) -> None:
    lineage, contracts = _workspace(tmp_path)

    with pytest.raises(PlanningStoreError) as caught:
        write_dispatch_artifact(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=expected_revision,
            expected_file_hash=expected_file_hash,
            contract=contracts["planning-dispatch/v1"],
            lineage=lineage,
            idempotency_key="dispatch-cas",
        )

    assert caught.value.code == code
    assert not lineage.dispatch_path.exists()


def test_accepted_dispatch_rejects_a_second_lineage_write(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    snapshot = read_artifact_document(
        lineage.dispatch_path,
        toolchain_root=REPO_ROOT,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=lineage.dispatch_producer,
    )

    with pytest.raises(PlanningStoreError) as caught:
        write_dispatch_artifact(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash=snapshot.file_hash,
            contract=contracts["planning-dispatch/v1"],
            lineage=lineage,
            idempotency_key="dispatch-second-lineage",
        )

    assert caught.value.code == "artifact.immutable"


def test_reusing_dispatch_key_with_different_payload_blocks(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts, idempotency_key="dispatch-bound-key")
    changed = _thaw(contracts["planning-dispatch/v1"])
    changed["scope"]["goal"] = "Different caller payload."

    with pytest.raises(PlanningStoreError) as caught:
        write_dispatch_artifact(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            contract=changed,
            lineage=lineage,
            idempotency_key="dispatch-bound-key",
        )

    assert caught.value.code == "store.idempotency_mismatch"


def test_exact_replay_rejects_tampered_persisted_artifact_body(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts, idempotency_key="dispatch-body-bound")
    original = lineage.dispatch_path.read_text()
    tampered = original.replace(
        "goal: Prove revisioned artifact lineage writes.",
        "goal: Tampered persisted artifact body.",
        1,
    )
    assert tampered != original
    lineage.dispatch_path.write_text(tampered)

    with pytest.raises(PlanningStoreError) as caught:
        write_dispatch_artifact(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            contract=contracts["planning-dispatch/v1"],
            lineage=lineage,
            idempotency_key="dispatch-body-bound",
        )

    assert caught.value.code == "artifact.replay_artifact_mismatch"
    assert lineage.dispatch_path.read_text() == tampered


def test_exact_replay_rejects_non_contract_body_tamper(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts, idempotency_key="dispatch-prose-bound")
    original = lineage.dispatch_path.read_text()
    tampered = "# Injected non-contract prose\n\n" + original
    lineage.dispatch_path.write_text(tampered)
    parsed = read_artifact_document(
        lineage.dispatch_path,
        toolchain_root=REPO_ROOT,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=lineage.dispatch_producer,
    )
    assert parsed.contract["artifact"]["id"] == lineage.batch_id  # type: ignore[index]

    with pytest.raises(PlanningStoreError) as caught:
        write_dispatch_artifact(
            lineage.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            contract=contracts["planning-dispatch/v1"],
            lineage=lineage,
            idempotency_key="dispatch-prose-bound",
        )

    assert caught.value.code == "artifact.replay_artifact_mismatch"
    assert lineage.dispatch_path.read_text() == tampered


def test_dispatch_rejects_foreign_lineage_facts_before_write(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    dispatch = contracts["planning-dispatch/v1"]
    variants = (
        (("artifact", "program"), "foreign-program", "artifact.lineage"),
        (("artifact", "id"), "foreign-batch", "artifact.lineage"),
        (("source", "finding_ids"), ["CCFG-99"], "artifact.lineage"),
        (("source", "ledger_revision"), "c" * 64, "artifact.lineage"),
        (("runway", "expected_path"), "foreign-runway.md", "artifact.lineage"),
        (
            ("execution_context", "implementation_target_root"),
            "/foreign/candidate",
            "artifact.lineage",
        ),
        (("producer", "toolchain_generation"), "candidate", "artifact.invalid"),
    )
    for field_path, value, code in variants:
        changed = _thaw(dispatch)
        _set(changed, field_path, value)
        with pytest.raises(PlanningStoreError) as caught:
            write_dispatch_artifact(
                lineage.dispatch_path,
                toolchain_root=REPO_ROOT,
                expected_revision=0,
                expected_file_hash=EMPTY_HASH,
                contract=changed,
                lineage=lineage,
                idempotency_key=f"dispatch-foreign-{field_path[-1]}",
            )
        assert caught.value.code == code
        assert not lineage.dispatch_path.exists()


def test_dispatch_rejects_foreign_or_escaping_target_path(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    foreign = lineage.planning_root / "foreign.md"
    foreign.write_text("")
    with pytest.raises(PlanningStoreError) as caught:
        write_dispatch_artifact(
            foreign,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            contract=contracts["planning-dispatch/v1"],
            lineage=lineage,
            idempotency_key="dispatch-foreign-path",
        )
    assert caught.value.code == "artifact.path"
    assert foreign.read_bytes() == b""

    escaped = replace(lineage, dispatch_path=tmp_path.parent / "escaped.md")
    with pytest.raises(PlanningStoreError) as escaped_error:
        write_dispatch_artifact(
            escaped.dispatch_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            contract=contracts["planning-dispatch/v1"],
            lineage=escaped,
            idempotency_key="dispatch-escape",
        )
    assert escaped_error.value.code == "artifact.path_escape"


def test_runway_requires_exact_dispatch_lineage_and_hash(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    dispatch_hash = _artifact_hash(lineage.dispatch_path)
    changed = _thaw(contracts["planning-runway/v1"])
    changed["artifact"]["source_dispatch_revision"] = "c" * 64

    with pytest.raises(PlanningStoreError) as source_error:
        write_runway_artifact(
            lineage.runway_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            expected_dispatch_file_hash=dispatch_hash,
            contract=changed,
            lineage=lineage,
            idempotency_key="runway-source-revision",
        )
    assert source_error.value.code == "artifact.lineage"
    assert not lineage.runway_path.exists()

    with pytest.raises(PlanningStoreError) as hash_error:
        write_runway_artifact(
            lineage.runway_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            expected_dispatch_file_hash="0" * 64,
            contract=contracts["planning-runway/v1"],
            lineage=lineage,
            idempotency_key="runway-predecessor-hash",
        )
    assert hash_error.value.code == "artifact.predecessor_hash"
    assert not lineage.runway_path.exists()


def test_runway_rejects_foreign_predecessor_generation(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    foreign_lineage = replace(
        lineage,
        dispatch_producer=ProducerIdentity(
            "candidate",
            COMMIT,
            "planning-dispatch/v1",
        ),
    )

    with pytest.raises(PlanningStoreError) as caught:
        write_runway_artifact(
            lineage.runway_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            expected_dispatch_file_hash=_artifact_hash(lineage.dispatch_path),
            contract=contracts["planning-runway/v1"],
            lineage=foreign_lineage,
            idempotency_key="runway-foreign-generation",
        )

    assert caught.value.code == "artifact.producer_lineage"
    assert not lineage.runway_path.exists()


def test_runway_and_closeout_exact_replay_return_same_result(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    dispatch_hash = _artifact_hash(lineage.dispatch_path)
    runway_request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=0,
        expected_file_hash=EMPTY_HASH,
        expected_dispatch_file_hash=dispatch_hash,
        contract=contracts["planning-runway/v1"],
        lineage=lineage,
        idempotency_key="runway-replay",
    )
    first_runway = write_runway_artifact(lineage.runway_path, **runway_request)
    replayed_runway = write_runway_artifact(lineage.runway_path, **runway_request)
    runway_hash = _artifact_hash(lineage.runway_path)
    closeout_request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=0,
        expected_file_hash=EMPTY_HASH,
        expected_dispatch_file_hash=dispatch_hash,
        expected_runway_file_hash=runway_hash,
        contract=contracts["planning-closeout/v1"],
        lineage=lineage,
        idempotency_key="closeout-replay",
    )
    first_closeout = write_closeout_artifact(lineage.closeout_path, **closeout_request)
    replayed_closeout = write_closeout_artifact(lineage.closeout_path, **closeout_request)

    assert first_runway.outcome == "applied"
    assert replayed_runway.outcome == "exact_replay"
    assert replayed_runway.receipt == first_runway.receipt
    assert first_closeout.outcome == "applied"
    assert replayed_closeout.outcome == "exact_replay"
    assert replayed_closeout.receipt == first_closeout.receipt


def test_closeout_rejects_foreign_batch_root_and_uncleared_pointer(
    tmp_path: Path,
) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    _write_runway(lineage, contracts)
    dispatch_hash = _artifact_hash(lineage.dispatch_path)
    runway_hash = _artifact_hash(lineage.runway_path)
    closeout = contracts["planning-closeout/v1"]
    variants = (
        (("artifact", "batch_id"), "foreign-batch"),
        (
            ("execution_context", "canonical_planning_repository_root"),
            "/foreign/stable",
        ),
        (("reconciliation", "selected_dispatch_after"), "dispatch.md"),
    )
    for field_path, value in variants:
        changed = _thaw(closeout)
        _set(changed, field_path, value)
        with pytest.raises(PlanningStoreError) as caught:
            write_closeout_artifact(
                lineage.closeout_path,
                toolchain_root=REPO_ROOT,
                expected_revision=0,
                expected_file_hash=EMPTY_HASH,
                expected_dispatch_file_hash=dispatch_hash,
                expected_runway_file_hash=runway_hash,
                contract=changed,
                lineage=lineage,
                idempotency_key=f"closeout-foreign-{field_path[-1]}",
            )
        assert caught.value.code == "artifact.lineage"
        assert not lineage.closeout_path.exists()


@pytest.mark.parametrize(
    ("generation", "commit"),
    [
        ("candidate", COMMIT),
        ("stable", "f" * 40),
    ],
)
def test_closeout_rejects_producer_generation_or_commit_outside_lineage(
    tmp_path: Path,
    generation: str,
    commit: str,
) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    _write_runway(lineage, contracts)
    dispatch_before = lineage.dispatch_path.read_bytes()
    runway_before = lineage.runway_path.read_bytes()
    changed = _thaw(contracts["planning-closeout/v1"])
    changed["producer"]["toolchain_generation"] = generation
    changed["producer"]["toolchain_commit"] = commit
    foreign_lineage = replace(
        lineage,
        closeout_producer=ProducerIdentity(
            generation,
            commit,
            "planning-closeout/v1",
        ),
    )

    with pytest.raises(PlanningStoreError) as caught:
        write_closeout_artifact(
            lineage.closeout_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            expected_dispatch_file_hash=_artifact_hash(lineage.dispatch_path),
            expected_runway_file_hash=_artifact_hash(lineage.runway_path),
            contract=changed,
            lineage=foreign_lineage,
            idempotency_key=f"closeout-producer-{generation}-{commit[:4]}",
        )

    assert caught.value.code == "artifact.producer_lineage"
    assert not lineage.closeout_path.exists()
    assert lineage.dispatch_path.read_bytes() == dispatch_before
    assert lineage.runway_path.read_bytes() == runway_before


def test_closeout_rejects_wrong_predecessor_hash_before_write(tmp_path: Path) -> None:
    lineage, contracts = _workspace(tmp_path)
    _write_dispatch(lineage, contracts)
    _write_runway(lineage, contracts)

    with pytest.raises(PlanningStoreError) as caught:
        write_closeout_artifact(
            lineage.closeout_path,
            toolchain_root=REPO_ROOT,
            expected_revision=0,
            expected_file_hash=EMPTY_HASH,
            expected_dispatch_file_hash=_artifact_hash(lineage.dispatch_path),
            expected_runway_file_hash="0" * 64,
            contract=contracts["planning-closeout/v1"],
            lineage=lineage,
            idempotency_key="closeout-predecessor-hash",
        )

    assert caught.value.code == "artifact.predecessor_hash"
    assert not lineage.closeout_path.exists()
