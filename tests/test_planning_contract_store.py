from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from scripts.planning_contract import (
    InjectedStoreFailure,
    PlanningStoreError,
    apply_current_document,
    apply_ledger_decision,
    compare_ledger_layouts,
    read_current_document,
    read_ledger_document,
    validate_planning_contracts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/planning-contracts"
CURRENT = FIXTURES / "current/valid/CURRENT.md"
CURRENT_BEFORE_FAULT = FIXTURES / "current/fault-before-replace/CURRENT.md"
CURRENT_RECOVERY_FAULT = FIXTURES / "current/recover-after-replace/CURRENT.md"
LEDGER = FIXTURES / "ledger/per-finding-valid/LEDGER.md"
LEDGER_FAULT = FIXTURES / "ledger/fault-multi-item/LEDGER.md"


def _copy_fixture(source: Path, tmp_path: Path) -> Path:
    target = tmp_path / source.name
    shutil.copy2(source, target)
    return target


def _thaw(value: object) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(child) for key, child in value.items()}
    if isinstance(value, tuple | list):
        return [_thaw(child) for child in value]
    return value


def _current_replacement(path: Path) -> dict[str, Any]:
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _thaw(snapshot.contract)
    replacement["revision"] = snapshot.logical_revision + 1
    replacement["queued_runway"] = "batches/ccfg-21/runway.md"
    return replacement


def _finding_replacement(path: Path, finding_id: str, *, status: str) -> dict[str, Any]:
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    replacement = _thaw(snapshot.findings[finding_id])
    replacement["revision"] += 1
    replacement["lifecycle"]["status"] = status
    return replacement


def test_reads_current_with_logical_revision_full_hash_and_immutable_contract() -> None:
    snapshot = read_current_document(CURRENT, toolchain_root=REPO_ROOT)

    assert snapshot.logical_revision == 1
    assert len(snapshot.file_hash) == 64
    with pytest.raises(TypeError):
        snapshot.contract["program"] = "other"  # type: ignore[index]


@pytest.mark.parametrize(
    ("revision_delta", "hash_value", "code"),
    [
        (1, None, "store.revision_mismatch"),
        (0, "0" * 64, "store.file_hash_mismatch"),
    ],
)
def test_current_cas_mismatch_rejects_without_write(
    tmp_path: Path,
    revision_delta: int,
    hash_value: str | None,
    code: str,
) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    before = path.read_bytes()
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)

    with pytest.raises(PlanningStoreError) as caught:
        apply_current_document(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=snapshot.logical_revision + revision_delta,
            expected_file_hash=hash_value or snapshot.file_hash,
            replacement_contract=_current_replacement(path),
            idempotency_key="current-cas",
        )

    assert caught.value.code == code
    assert path.read_bytes() == before


def test_current_apply_preserves_prose_and_emits_replayable_receipt(tmp_path: Path) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _current_replacement(path)

    result = apply_current_document(
        path,
        toolchain_root=REPO_ROOT,
        expected_revision=snapshot.logical_revision,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key="current-apply",
    )
    after = read_current_document(path, toolchain_root=REPO_ROOT)

    assert result.outcome == "applied"
    assert result.receipt.before_revision == 1
    assert result.receipt.after_revision == 2
    assert after.logical_revision == 2
    assert after.contract["queued_runway"] == "batches/ccfg-21/runway.md"
    assert "This prose survives current-state replacement." in path.read_text()
    assert "current-store/v1" in path.read_text()


def test_current_failure_before_replace_preserves_original(tmp_path: Path) -> None:
    path = _copy_fixture(CURRENT_BEFORE_FAULT, tmp_path)
    before = path.read_bytes()
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)

    with pytest.raises(InjectedStoreFailure, match="before_replace"):
        apply_current_document(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash=snapshot.file_hash,
            replacement_contract=_current_replacement(path),
            idempotency_key="current-before",
            fault="before_replace",
        )

    assert path.read_bytes() == before
    assert not tuple(path.parent.glob(f".{path.name}.*"))


def test_current_after_replace_failure_recovers_exact_receipt_without_reapply(
    tmp_path: Path,
) -> None:
    path = _copy_fixture(CURRENT_RECOVERY_FAULT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _current_replacement(path)
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key="current-recover",
    )
    with pytest.raises(InjectedStoreFailure, match="after_replace"):
        apply_current_document(path, **request, fault="after_replace_before_return")

    recovered = apply_current_document(path, **request)

    assert recovered.outcome == "exact_replay"
    assert recovered.receipt.after_revision == 2
    assert read_current_document(path, toolchain_root=REPO_ROOT).logical_revision == 2


def test_reusing_current_key_with_different_payload_blocks(tmp_path: Path) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _current_replacement(path)
    apply_current_document(
        path,
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key="current-key",
    )
    replacement["blockers"] = ["different"]

    with pytest.raises(PlanningStoreError) as caught:
        apply_current_document(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash=snapshot.file_hash,
            replacement_contract=replacement,
            idempotency_key="current-key",
        )

    assert caught.value.code == "store.idempotency_mismatch"


def test_ambiguous_current_replay_evidence_blocks(tmp_path: Path) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _current_replacement(path)
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key="current-ambiguous",
    )
    apply_current_document(path, **request)
    text = path.read_text()
    metadata_tail = text.split("## Store Metadata", 1)[1]
    path.write_text(text.rstrip() + "\n\n## Store Metadata" + metadata_tail)

    with pytest.raises(PlanningStoreError) as caught:
        apply_current_document(path, **request)

    assert caught.value.code == "store.metadata_count"


def test_current_store_revision_mismatch_blocks_before_exact_replay(
    tmp_path: Path,
) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _current_replacement(path)
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key="current-revision-corrupt",
    )
    apply_current_document(path, **request)
    path.write_text(path.read_text().replace("store_revision: 2", "store_revision: 3", 1))

    with pytest.raises(PlanningStoreError) as caught:
        apply_current_document(path, **request)

    assert caught.value.code == "store.receipt_chain"


def test_current_corrupt_receipt_revision_chain_blocks_replay(tmp_path: Path) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    replacement = _current_replacement(path)
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=replacement,
        idempotency_key="current-chain-corrupt",
    )
    apply_current_document(path, **request)
    path.write_text(path.read_text().replace("before_revision: 1", "before_revision: 0", 1))

    with pytest.raises(PlanningStoreError) as caught:
        apply_current_document(path, **request)

    assert caught.value.code == "store.receipt_chain"


def test_current_tampered_receipt_result_blocks_exact_replay(tmp_path: Path) -> None:
    path = _copy_fixture(CURRENT, tmp_path)
    snapshot = read_current_document(path, toolchain_root=REPO_ROOT)
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        replacement_contract=_current_replacement(path),
        idempotency_key="current-result-corrupt",
    )
    apply_current_document(path, **request)
    original = path.read_text()
    tampered = original.replace(
        "touched_finding_ids: []",
        "touched_finding_ids: [CCFG-1]",
        1,
    )
    assert tampered != original
    path.write_text(tampered)

    with pytest.raises(PlanningStoreError) as caught:
        apply_current_document(path, **request)

    assert caught.value.code == "store.replay_result_mismatch"


def test_reads_ledger_and_rejects_invalid_derived_index() -> None:
    snapshot = read_ledger_document(LEDGER, toolchain_root=REPO_ROOT)
    invalid = validate_planning_contracts(
        [FIXTURES / "ledger/invalid-derived-index"],
        toolchain_root=REPO_ROOT,
    )

    assert snapshot.logical_revision == 1
    assert set(snapshot.findings) == {"CCFG-1", "CCFG-2"}
    assert {item.code for item in invalid.diagnostics} == {
        "ledger.derived_index_mismatch"
    }


def test_ledger_multi_item_apply_is_atomic_and_receipt_names_all_touched(
    tmp_path: Path,
) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    one = _finding_replacement(path, "CCFG-1", status="closed")
    two = _finding_replacement(path, "CCFG-2", status="blocked")

    result = apply_ledger_decision(
        path,
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        action="reconcile",
        finding_mutations=[two, one],
        touched_finding_revisions={"CCFG-1": 1, "CCFG-2": 1},
        idempotency_key="ledger-multi",
    )
    after = read_ledger_document(path, toolchain_root=REPO_ROOT)

    assert result.receipt.touched_finding_ids == ("CCFG-1", "CCFG-2")
    assert after.logical_revision == 2
    assert after.findings["CCFG-1"]["revision"] == 2
    assert after.findings["CCFG-2"]["lifecycle"]["status"] == "blocked"  # type: ignore[index]


def test_ledger_touched_revision_failure_preserves_every_finding(tmp_path: Path) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    before = path.read_bytes()
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)

    with pytest.raises(PlanningStoreError) as caught:
        apply_ledger_decision(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash=snapshot.file_hash,
            action="update",
            finding_mutations=[_finding_replacement(path, "CCFG-1", status="closed")],
            touched_finding_revisions={"CCFG-1": 9},
            idempotency_key="ledger-stale-finding",
        )

    assert caught.value.code == "ledger.finding_revision_mismatch"
    assert path.read_bytes() == before


def test_ledger_full_file_hash_mismatch_rejects_before_write(tmp_path: Path) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    before = path.read_bytes()

    with pytest.raises(PlanningStoreError) as caught:
        apply_ledger_decision(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash="0" * 64,
            action="update",
            finding_mutations=[_finding_replacement(path, "CCFG-1", status="closed")],
            touched_finding_revisions={"CCFG-1": 1},
            idempotency_key="ledger-hash",
        )

    assert caught.value.code == "store.file_hash_mismatch"
    assert path.read_bytes() == before


def test_one_stale_mutation_rejects_entire_multi_finding_decision(
    tmp_path: Path,
) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    before = path.read_bytes()
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)

    with pytest.raises(PlanningStoreError) as caught:
        apply_ledger_decision(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash=snapshot.file_hash,
            action="reconcile",
            finding_mutations=[
                _finding_replacement(path, "CCFG-1", status="closed"),
                _finding_replacement(path, "CCFG-2", status="blocked"),
            ],
            touched_finding_revisions={"CCFG-1": 1, "CCFG-2": 9},
            idempotency_key="ledger-all-or-nothing",
        )

    assert caught.value.code == "ledger.finding_revision_mismatch"
    assert path.read_bytes() == before


def test_ledger_failure_before_replace_preserves_whole_file(tmp_path: Path) -> None:
    path = _copy_fixture(LEDGER_FAULT, tmp_path)
    before = path.read_bytes()
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    with pytest.raises(InjectedStoreFailure, match="before_replace"):
        apply_ledger_decision(
            path,
            toolchain_root=REPO_ROOT,
            expected_revision=1,
            expected_file_hash=snapshot.file_hash,
            action="update",
            finding_mutations=[_finding_replacement(path, "CCFG-1", status="closed")],
            touched_finding_revisions={"CCFG-1": 1},
            idempotency_key="ledger-before",
            fault="before_replace",
        )

    assert path.read_bytes() == before


def test_ledger_after_replace_failure_recovers_without_second_application(
    tmp_path: Path,
) -> None:
    path = _copy_fixture(LEDGER_FAULT, tmp_path)
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    mutation = _finding_replacement(path, "CCFG-1", status="closed")
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        action="update",
        finding_mutations=[mutation],
        touched_finding_revisions={"CCFG-1": 1},
        idempotency_key="ledger-recover",
    )
    with pytest.raises(InjectedStoreFailure, match="after_replace"):
        apply_ledger_decision(path, **request, fault="after_replace_before_return")

    recovered = apply_ledger_decision(path, **request)
    after = read_ledger_document(path, toolchain_root=REPO_ROOT)

    assert recovered.outcome == "exact_replay"
    assert after.logical_revision == 2
    assert after.findings["CCFG-1"]["revision"] == 2


def test_reusing_ledger_key_with_different_payload_blocks(tmp_path: Path) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    mutation = _finding_replacement(path, "CCFG-1", status="closed")
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        action="update",
        finding_mutations=[mutation],
        touched_finding_revisions={"CCFG-1": 1},
        idempotency_key="ledger-key",
    )
    apply_ledger_decision(path, **request)
    changed = _thaw(mutation)
    changed["lifecycle"]["status"] = "blocked"

    with pytest.raises(PlanningStoreError) as caught:
        apply_ledger_decision(path, **{**request, "finding_mutations": [changed]})

    assert caught.value.code == "store.idempotency_mismatch"


def test_ledger_corrupt_receipt_chain_blocks_before_exact_replay(tmp_path: Path) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    mutation = _finding_replacement(path, "CCFG-1", status="closed")
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        action="update",
        finding_mutations=[mutation],
        touched_finding_revisions={"CCFG-1": 1},
        idempotency_key="ledger-chain-corrupt",
    )
    apply_ledger_decision(path, **request)
    path.write_text(path.read_text().replace("after_revision: 2", "after_revision: 4", 1))

    with pytest.raises(PlanningStoreError) as caught:
        apply_ledger_decision(path, **request)

    assert caught.value.code == "store.receipt_chain"


def test_ledger_tampered_receipt_result_blocks_exact_replay(tmp_path: Path) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    snapshot = read_ledger_document(path, toolchain_root=REPO_ROOT)
    mutation = _finding_replacement(path, "CCFG-1", status="closed")
    request = dict(
        toolchain_root=REPO_ROOT,
        expected_revision=1,
        expected_file_hash=snapshot.file_hash,
        action="update",
        finding_mutations=[mutation],
        touched_finding_revisions={"CCFG-1": 1},
        idempotency_key="ledger-result-corrupt",
    )
    apply_ledger_decision(path, **request)
    original = path.read_text()
    tampered = original.replace(
        "touched_finding_ids:\n    - CCFG-1",
        "touched_finding_ids:\n    - CCFG-2",
        1,
    )
    assert tampered != original
    path.write_text(tampered)

    with pytest.raises(PlanningStoreError) as caught:
        apply_ledger_decision(path, **request)

    assert caught.value.code == "store.replay_result_mismatch"


def test_ledger_derived_revision_must_match_embedded_store_revision(
    tmp_path: Path,
) -> None:
    path = _copy_fixture(LEDGER, tmp_path)
    path.write_text(path.read_text().replace("source_revision: 1", "source_revision: 9", 1))

    with pytest.raises(PlanningStoreError) as caught:
        read_ledger_document(path, toolchain_root=REPO_ROOT)

    assert caught.value.code == "ledger.derived_revision"


def test_comparison_proves_semantic_and_projection_equivalence() -> None:
    comparison = compare_ledger_layouts(
        FIXTURES / "ledger/per-finding-valid",
        FIXTURES / "ledger/global-equivalent",
        toolchain_root=REPO_ROOT,
    )

    assert comparison.equivalent
    assert comparison.semantic_equal
    assert comparison.projection_equal
    assert comparison.duplicate_detection_green
    assert comparison.diff_locality_green
    assert comparison.error_locality_green
    assert comparison.revision_behavior_green
    assert comparison.source_identity_green
    assert comparison.per_finding_changed_sections == (
        "Derived Index",
        "Finding CCFG-1",
        "Store Metadata",
    )
    assert comparison.global_changed_sections == ("Global Comparison",)


def test_comparison_fixtures_expose_duplicate_and_per_finding_error_locality() -> None:
    with pytest.raises(PlanningStoreError) as duplicate:
        read_ledger_document(
            FIXTURES / "ledger/per-finding-valid/duplicate.md",
            toolchain_root=REPO_ROOT,
        )
    with pytest.raises(PlanningStoreError) as invalid:
        read_ledger_document(
            FIXTURES / "ledger/per-finding-valid/invalid-locality.md",
            toolchain_root=REPO_ROOT,
        )

    assert duplicate.value.code == "ledger.duplicate_id"
    assert invalid.value.code == "schema.type"
    assert "CCFG-2" in str(invalid.value)
    assert "line" in str(invalid.value)


@pytest.mark.parametrize(
    "global_fixture",
    ["revision-divergence.md", "wrong-source.md"],
)
def test_compare_cli_exits_one_for_non_equivalent_or_wrong_source(
    global_fixture: str,
) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/planning_contract.py",
            "compare-ledger-layouts",
            "--toolchain-root",
            ".",
            "--per-finding",
            "tests/fixtures/planning-contracts/ledger/per-finding-valid",
            "--global",
            f"tests/fixtures/planning-contracts/ledger/global-equivalent/{global_fixture}",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
