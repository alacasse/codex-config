from __future__ import annotations

import hashlib
import shutil
from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts.planning_contract import (
    ArtifactLineage,
    PlanningStoreError,
    ProducerIdentity,
    SelectionTransactionRequest,
    read_artifact_document,
    read_current_document,
    render_planning_contract,
    simulate_selection_transaction,
    validate_planning_contracts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/planning-contracts"
ARTIFACT_FIXTURE = FIXTURES / "artifacts/valid-lineage"
CURRENT_FIXTURE = FIXTURES / "current/valid/CURRENT.md"
COMMIT = "0123456789abcdef0123456789abcdef01234567"
EXTENSION_ORDER = (
    "dispatch_observed",
    "selected_input",
    "selected_observed",
    "runway_input",
    "runway_observed",
    "queued_input",
    "queued_observed",
)


@dataclass(frozen=True)
class InterruptedExpectation:
    prefix_length: int
    current_state: str
    dispatch_exists: bool
    runway_exists: bool
    current_replay_stages: tuple[str, ...]
    transaction_receipt_stages: tuple[str, ...]


FAULT_EXPECTATIONS = {
    "after_transaction_record_append": InterruptedExpectation(0, "idle", False, False, (), ()),
    "before_dispatch_write": InterruptedExpectation(0, "idle", False, False, (), ()),
    "after_dispatch_write_before_validation": InterruptedExpectation(
        0, "idle", True, False, (), ()
    ),
    "after_dispatch_validation": InterruptedExpectation(1, "idle", True, False, (), ()),
    "before_idle_to_selected_cas": InterruptedExpectation(2, "idle", True, False, (), ()),
    "after_idle_to_selected_cas_before_receipt": InterruptedExpectation(
        2, "selected", True, False, ("selected",), ()
    ),
    "after_selected_transition_receipt": InterruptedExpectation(
        3, "selected", True, False, ("selected",), ("selected",)
    ),
    "before_runway_write": InterruptedExpectation(
        4, "selected", True, False, ("selected",), ("selected",)
    ),
    "after_runway_write_before_validation": InterruptedExpectation(
        4, "selected", True, True, ("selected",), ("selected",)
    ),
    "after_runway_validation": InterruptedExpectation(
        5, "selected", True, True, ("selected",), ("selected",)
    ),
    "before_selected_to_queued_cas": InterruptedExpectation(
        6, "selected", True, True, ("selected",), ("selected",)
    ),
    "after_selected_to_queued_cas_before_receipt": InterruptedExpectation(
        6, "queued", True, True, ("selected", "queued"), ("selected",)
    ),
    "after_queued_transition_receipt": InterruptedExpectation(
        7,
        "queued",
        True,
        True,
        ("selected", "queued"),
        ("selected", "queued"),
    ),
}


@dataclass(frozen=True)
class ArtifactEvidence:
    content: bytes
    revision: int
    file_hash: str


@dataclass(frozen=True)
class DurableEvidence:
    transaction_content: bytes
    transaction_record: dict[str, Any]
    current_content: bytes
    current_contract: dict[str, Any]
    current_revision: int
    current_file_hash: str
    current_replay_records: tuple[dict[str, Any], ...]
    dispatch: ArtifactEvidence | None
    runway: ArtifactEvidence | None


def _thaw(value: object) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(child) for key, child in value.items()}
    if isinstance(value, tuple | list):
        return [_thaw(child) for child in value]
    return value


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_contracts() -> dict[str, dict[str, Any]]:
    result = validate_planning_contracts([ARTIFACT_FIXTURE], toolchain_root=REPO_ROOT)
    assert result.is_valid
    return {
        str(parsed.contract["schema"]): _thaw(parsed.contract)
        for parsed in result.contracts
    }


def _transaction_record(path: Path) -> dict[str, Any]:
    result = validate_planning_contracts([path], toolchain_root=REPO_ROOT)
    assert result.is_valid, result.diagnostics
    assert len(result.contracts) == 1
    return _thaw(result.contracts[0].contract)


def _store_replay_records(path: Path) -> tuple[dict[str, Any], ...]:
    marker = "## Store Metadata\n\n```yaml\n"
    _, separator, remainder = path.read_text(encoding="utf-8").partition(marker)
    if not separator:
        return ()
    source, closing, _ = remainder.partition("\n```")
    assert closing
    loaded = yaml.safe_load(source)
    assert isinstance(loaded, dict)
    records = loaded["replay_records"]
    assert isinstance(records, list)
    return tuple(_thaw(record) for record in records)


def _artifact_evidence(
    path: Path,
    *,
    schema: str,
    producer: ProducerIdentity,
) -> ArtifactEvidence | None:
    if not path.exists():
        return None
    snapshot = read_artifact_document(
        path,
        toolchain_root=REPO_ROOT,
        expected_schema=schema,
        expected_producer_identity=producer,
    )
    return ArtifactEvidence(
        content=path.read_bytes(),
        revision=snapshot.logical_revision,
        file_hash=snapshot.file_hash,
    )


def _durable_evidence(request: SelectionTransactionRequest) -> DurableEvidence:
    transaction_record = _transaction_record(request.transaction_path)
    current = read_current_document(request.current_path, toolchain_root=REPO_ROOT)
    return DurableEvidence(
        transaction_content=request.transaction_path.read_bytes(),
        transaction_record=transaction_record,
        current_content=request.current_path.read_bytes(),
        current_contract=_thaw(current.contract),
        current_revision=current.logical_revision,
        current_file_hash=current.file_hash,
        current_replay_records=_store_replay_records(request.current_path),
        dispatch=_artifact_evidence(
            request.lineage.dispatch_path,
            schema="planning-dispatch/v1",
            producer=request.lineage.dispatch_producer,
        ),
        runway=_artifact_evidence(
            request.lineage.runway_path,
            schema="planning-runway/v1",
            producer=request.lineage.runway_producer,
        ),
    )


def _expected_current_contract(
    request: SelectionTransactionRequest,
    state: str,
) -> dict[str, Any]:
    expected = _thaw(request.initial_current_contract)
    if state == "idle":
        return expected
    expected["revision"] = request.expected_initial_state_revision + 1
    expected["selected_dispatch"] = "dispatch.md"
    if state == "selected":
        return expected
    expected["revision"] = request.expected_initial_state_revision + 2
    expected["selected_dispatch"] = None
    expected["queued_runway"] = "runway.md"
    return expected


def _receipt_stage(record: Mapping[str, object]) -> str:
    key = record["idempotency_key"]
    assert isinstance(key, str)
    return key.rsplit(":", 1)[-1]


def _transaction_receipt_stages(record: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(
        str(extension["type"]).removesuffix("_observed")
        for extension in record["extensions"]
        if "receipt" in extension
    )


def _assert_interrupted_evidence(
    request: SelectionTransactionRequest,
    evidence: DurableEvidence,
    expected: InterruptedExpectation,
) -> None:
    extensions = evidence.transaction_record["extensions"]
    assert tuple(item["type"] for item in extensions) == EXTENSION_ORDER[
        : expected.prefix_length
    ]
    assert evidence.transaction_content == render_planning_contract(
        evidence.transaction_record,
        toolchain_root=REPO_ROOT,
        expected_producer_identity=request.producer,
    ).encode()
    assert evidence.current_contract == _expected_current_contract(
        request,
        expected.current_state,
    )
    expected_revision = request.expected_initial_state_revision + {
        "idle": 0,
        "selected": 1,
        "queued": 2,
    }[expected.current_state]
    assert evidence.current_revision == expected_revision
    assert evidence.current_file_hash == hashlib.sha256(evidence.current_content).hexdigest()
    replay_stages = tuple(map(_receipt_stage, evidence.current_replay_records))
    assert len(replay_stages) == len(expected.current_replay_stages)
    assert set(replay_stages) == set(expected.current_replay_stages)
    replay_by_stage = {
        _receipt_stage(record): record for record in evidence.current_replay_records
    }
    for stage, offsets in {"selected": (0, 1), "queued": (1, 2)}.items():
        if stage not in replay_by_stage:
            continue
        replay = replay_by_stage[stage]
        receipt = replay["receipt"]
        assert replay["idempotency_key"] == f"{request.transaction_id}:{stage}"
        assert replay["request_hash"] == receipt["request_hash"]
        assert receipt["idempotency_key"] == replay["idempotency_key"]
        assert receipt["before_revision"] == (
            request.expected_initial_state_revision + offsets[0]
        )
        assert receipt["after_revision"] == (
            request.expected_initial_state_revision + offsets[1]
        )
        assert receipt["touched_finding_ids"] == []
    assert _transaction_receipt_stages(evidence.transaction_record) == (
        expected.transaction_receipt_stages
    )
    assert (evidence.dispatch is not None) is expected.dispatch_exists
    assert (evidence.runway is not None) is expected.runway_exists
    for artifact in (evidence.dispatch, evidence.runway):
        if artifact is not None:
            assert artifact.revision == 1
            assert artifact.file_hash == hashlib.sha256(artifact.content).hexdigest()
    extensions_by_type = {
        extension["type"]: extension
        for extension in evidence.transaction_record["extensions"]
    }
    if "dispatch_observed" in extensions_by_type:
        assert evidence.dispatch is not None
        assert extensions_by_type["dispatch_observed"]["dispatch_revision"] == 1
        assert extensions_by_type["dispatch_observed"]["dispatch_file_hash"] == (
            evidence.dispatch.file_hash
        )
    if "runway_observed" in extensions_by_type:
        assert evidence.runway is not None
        assert extensions_by_type["runway_observed"]["runway_revision"] == 1
        assert extensions_by_type["runway_observed"]["runway_file_hash"] == (
            evidence.runway.file_hash
        )
    for stage in expected.transaction_receipt_stages:
        observed = extensions_by_type[f"{stage}_observed"]
        assert observed["receipt"] == replay_by_stage[stage]["receipt"]


def _assert_completed_evidence(
    request: SelectionTransactionRequest,
    interrupted: DurableEvidence,
) -> None:
    completed = _durable_evidence(request)
    prefix_length = len(interrupted.transaction_record["extensions"])
    assert completed.transaction_record["initial_intent"] == (
        interrupted.transaction_record["initial_intent"]
    )
    assert completed.transaction_record["extensions"][:prefix_length] == (
        interrupted.transaction_record["extensions"]
    )
    reconstructed_prefix = _thaw(completed.transaction_record)
    reconstructed_prefix["extensions"] = reconstructed_prefix["extensions"][
        :prefix_length
    ]
    assert render_planning_contract(
        reconstructed_prefix,
        toolchain_root=REPO_ROOT,
        expected_producer_identity=request.producer,
    ).encode() == interrupted.transaction_content
    assert tuple(item["type"] for item in completed.transaction_record["extensions"]) == (
        EXTENSION_ORDER
    )
    assert completed.current_contract == _expected_current_contract(request, "queued")
    assert completed.current_revision == request.expected_initial_state_revision + 2
    replays = {
        _receipt_stage(record): record for record in completed.current_replay_records
    }
    assert set(replays) == {"selected", "queued"}
    assert len(completed.current_replay_records) == 2
    selected_replay = replays["selected"]
    queued_replay = replays["queued"]
    for interrupted_replay in interrupted.current_replay_records:
        stage = _receipt_stage(interrupted_replay)
        assert replays[stage] == interrupted_replay
    assert selected_replay["receipt"]["before_revision"] == (
        request.expected_initial_state_revision
    )
    assert selected_replay["receipt"]["after_revision"] == (
        request.expected_initial_state_revision + 1
    )
    assert queued_replay["receipt"]["before_revision"] == (
        request.expected_initial_state_revision + 1
    )
    assert queued_replay["receipt"]["after_revision"] == (
        request.expected_initial_state_revision + 2
    )
    selected_observed = completed.transaction_record["extensions"][2]
    queued_observed = completed.transaction_record["extensions"][6]
    assert selected_observed["receipt"] == selected_replay["receipt"]
    assert queued_observed["receipt"] == queued_replay["receipt"]
    assert completed.dispatch is not None
    assert completed.dispatch.revision == 1
    assert completed.runway is not None
    assert completed.runway.revision == 1
    if interrupted.dispatch is not None:
        assert completed.dispatch == interrupted.dispatch
    if interrupted.runway is not None:
        assert completed.runway == interrupted.runway
    if interrupted.current_contract == _expected_current_contract(request, "queued"):
        assert completed.current_content == interrupted.current_content


def _workspace(tmp_path: Path) -> SelectionTransactionRequest:
    planning_root = tmp_path / "plans"
    planning_root.mkdir()
    current_path = planning_root / "CURRENT.md"
    shutil.copy2(CURRENT_FIXTURE, current_path)
    ledger_path = planning_root / "LEDGER.md"
    ledger_path.write_text("fixture ledger\n", encoding="utf-8")
    initial = read_current_document(current_path, toolchain_root=REPO_ROOT)
    contracts = _artifact_contracts()
    dispatch = contracts["planning-dispatch/v1"]
    runway = contracts["planning-runway/v1"]
    dispatch["execution_context"] = {
        "toolchain_source_root": str(tmp_path / "stable"),
        "canonical_planning_repository_root": str(tmp_path),
        "implementation_target_root": str(tmp_path / "candidate"),
    }
    runway["execution"]["implementation_target_root"] = str(tmp_path / "candidate")
    lineage = ArtifactLineage(
        planning_root=planning_root,
        program="codex-config",
        batch_id="ccfg-21-artifacts",
        included_finding_ids=("CCFG-21",),
        deferred_finding_ids=(),
        batch_kind="migration",
        ledger_path=ledger_path,
        ledger_revision="b" * 64,
        dispatch_path=planning_root / "dispatch.md",
        dispatch_revision="a" * 64,
        runway_path=planning_root / "runway.md",
        closeout_path=planning_root / "closeout.md",
        toolchain_source_root=tmp_path / "stable",
        canonical_planning_repository_root=tmp_path,
        implementation_target_root=tmp_path / "candidate",
        dispatch_producer=ProducerIdentity("stable", COMMIT, "planning-dispatch/v1"),
        runway_producer=ProducerIdentity("stable", COMMIT, "planning-runway/v1"),
        closeout_producer=ProducerIdentity("stable", COMMIT, "planning-closeout/v1"),
    )
    return SelectionTransactionRequest(
        transaction_id="selection-001",
        transaction_path=planning_root / "selection-001.md",
        current_path=current_path,
        expected_initial_state_revision=initial.logical_revision,
        expected_initial_state_file_hash=initial.file_hash,
        initial_current_contract=_thaw(initial.contract),
        lineage=lineage,
        dispatch_contract=dispatch,
        runway_contract=runway,
        command_owner_version="ccfg-21-slice-4",
        producer=ProducerIdentity(
            "stable",
            COMMIT,
            "planning-selection-transaction/v1",
        ),
    )


def _durable_bytes(request: SelectionTransactionRequest) -> dict[str, bytes]:
    paths = (
        request.transaction_path,
        request.current_path,
        request.lineage.dispatch_path,
        request.lineage.runway_path,
    )
    return {path.name: path.read_bytes() for path in paths if path.exists()}


def _lineage_drift(
    request: SelectionTransactionRequest,
    case: str,
) -> SelectionTransactionRequest:
    initial = _thaw(request.initial_current_contract)
    dispatch = _thaw(request.dispatch_contract)
    runway = _thaw(request.runway_contract)
    lineage = request.lineage
    if case == "program":
        initial["program"] = "other-program"
        dispatch["artifact"]["program"] = "other-program"
        lineage = replace(lineage, program="other-program")
    elif case == "finding":
        dispatch["source"]["finding_ids"] = ["CCFG-99"]
        dispatch["scope"]["included_finding_ids"] = ["CCFG-99"]
        lineage = replace(lineage, included_finding_ids=("CCFG-99",))
    elif case == "batch":
        dispatch["artifact"]["id"] = "other-batch"
        runway["artifact"]["id"] = "other-batch"
        lineage = replace(lineage, batch_id="other-batch")
    elif case == "root":
        broader_root = lineage.planning_root.parent
        initial["ledger"] = "plans/LEDGER.md"
        dispatch["source"]["ledger_path"] = "plans/LEDGER.md"
        dispatch["runway"]["expected_path"] = "plans/runway.md"
        runway["artifact"]["source_dispatch"] = "plans/dispatch.md"
        lineage = replace(lineage, planning_root=broader_root)
    elif case == "path":
        alternate_dispatch = lineage.planning_root / "alternate-dispatch.md"
        runway["artifact"]["source_dispatch"] = alternate_dispatch.name
        lineage = replace(lineage, dispatch_path=alternate_dispatch)
    else:
        raise AssertionError(f"unknown drift case {case}")
    return replace(
        request,
        initial_current_contract=initial,
        lineage=lineage,
        dispatch_contract=dispatch,
        runway_contract=runway,
    )


def _replace_store_replay_records(
    path: Path,
    records: list[dict[str, Any]],
) -> None:
    marker = "## Store Metadata\n\n```yaml\n"
    before, separator, remainder = path.read_text(encoding="utf-8").partition(marker)
    assert separator
    source, closing, after = remainder.partition("\n```")
    assert closing
    metadata = yaml.safe_load(source)
    assert isinstance(metadata, dict)
    metadata["replay_records"] = records
    rendered = yaml.safe_dump(metadata, sort_keys=False).rstrip()
    path.write_text(
        before + marker + rendered + "\n```" + after,
        encoding="utf-8",
    )


def test_selection_transaction_completes_and_exact_retry_is_byte_stable(
    tmp_path: Path,
) -> None:
    request = _workspace(tmp_path)

    completed = simulate_selection_transaction(request, toolchain_root=REPO_ROOT)
    first_bytes = _durable_bytes(request)
    replayed = simulate_selection_transaction(request, toolchain_root=REPO_ROOT)

    assert completed.outcome == "completed"
    assert replayed.outcome == "exact_replay"
    assert replayed.transaction_file_hash == completed.transaction_file_hash
    assert _durable_bytes(request) == first_bytes
    assert completed.current_revision == request.expected_initial_state_revision + 2
    assert completed.selected_receipt.before_revision == request.expected_initial_state_revision
    assert completed.queued_receipt.after_revision == completed.current_revision
    record = _transaction_record(request.transaction_path)
    assert tuple(item["type"] for item in record["extensions"]) == EXTENSION_ORDER
    current = read_current_document(request.current_path, toolchain_root=REPO_ROOT)
    assert current.contract["selected_dispatch"] is None
    assert current.contract["queued_runway"] == "runway.md"


@pytest.mark.parametrize(
    ("fault", "expected"),
    [pytest.param(fault, expected, id=fault) for fault, expected in FAULT_EXPECTATIONS.items()],
)
def test_every_durable_boundary_resumes_without_duplicate_effects(
    tmp_path: Path,
    fault: str,
    expected: InterruptedExpectation,
) -> None:
    request = _workspace(tmp_path)

    with pytest.raises(RuntimeError):
        simulate_selection_transaction(
            request,
            toolchain_root=REPO_ROOT,
            fault=fault,  # type: ignore[arg-type]
        )

    interrupted = _durable_evidence(request)
    _assert_interrupted_evidence(request, interrupted, expected)

    recovered = simulate_selection_transaction(request, toolchain_root=REPO_ROOT)

    expected_outcome = (
        "exact_replay"
        if expected.prefix_length == len(EXTENSION_ORDER)
        else "completed"
    )
    assert recovered.outcome == expected_outcome
    assert recovered.current_revision == request.expected_initial_state_revision + 2
    _assert_completed_evidence(request, interrupted)


def test_reused_transaction_id_rejects_changed_immutable_intent(tmp_path: Path) -> None:
    request = _workspace(tmp_path)
    with pytest.raises(RuntimeError):
        simulate_selection_transaction(
            request,
            toolchain_root=REPO_ROOT,
            fault="after_dispatch_validation",
        )
    evidence = _durable_bytes(request)
    changed_dispatch = _thaw(request.dispatch_contract)
    changed_dispatch["scope"]["goal"] = "A different batch goal."

    with pytest.raises(PlanningStoreError, match="transaction.reused_id_mismatch"):
        simulate_selection_transaction(
            replace(request, dispatch_contract=changed_dispatch),
            toolchain_root=REPO_ROOT,
        )

    assert _durable_bytes(request) == evidence


@pytest.mark.parametrize(
    ("case", "original", "replacement"),
    [
        pytest.param(
            "blockers",
            "blockers: []",
            "blockers:\n- external-blocker",
            id="blockers",
        ),
        pytest.param(
            "latest-closeout",
            "latest_closeout: null",
            "latest_closeout: prior-closeout.md",
            id="latest-closeout",
        ),
    ],
)
def test_same_id_rejects_valid_initial_state_drift_before_further_mutation(
    tmp_path: Path,
    case: str,
    original: str,
    replacement: str,
) -> None:
    request = _workspace(tmp_path)
    with pytest.raises(RuntimeError):
        simulate_selection_transaction(
            request,
            toolchain_root=REPO_ROOT,
            fault="before_idle_to_selected_cas",
        )
    request.current_path.write_text(
        request.current_path.read_text(encoding="utf-8").replace(
            original,
            replacement,
        ),
        encoding="utf-8",
    )
    validation = validate_planning_contracts(
        [request.current_path],
        toolchain_root=REPO_ROOT,
    )
    assert validation.is_valid, (case, validation.diagnostics)
    before = _durable_bytes(request)
    before_current = read_current_document(request.current_path, toolchain_root=REPO_ROOT)
    assert before_current.logical_revision == request.expected_initial_state_revision

    with pytest.raises(PlanningStoreError, match="store.file_hash_mismatch"):
        simulate_selection_transaction(request, toolchain_root=REPO_ROOT)

    assert _durable_bytes(request) == before
    assert read_current_document(
        request.current_path,
        toolchain_root=REPO_ROOT,
    ) == before_current


@pytest.mark.parametrize("case", ["program", "finding", "batch", "root", "path"])
def test_same_id_rejects_valid_lineage_drift_before_further_mutation(
    tmp_path: Path,
    case: str,
) -> None:
    request = _workspace(tmp_path)
    with pytest.raises(RuntimeError):
        simulate_selection_transaction(
            request,
            toolchain_root=REPO_ROOT,
            fault="after_dispatch_validation",
        )
    drifted = _lineage_drift(request, case)
    before = _durable_bytes(request)
    before_record = _transaction_record(request.transaction_path)
    before_current = read_current_document(request.current_path, toolchain_root=REPO_ROOT)

    with pytest.raises(PlanningStoreError, match="transaction.reused_id_mismatch"):
        simulate_selection_transaction(drifted, toolchain_root=REPO_ROOT)

    assert _durable_bytes(request) == before
    assert _transaction_record(request.transaction_path) == before_record
    assert read_current_document(
        request.current_path,
        toolchain_root=REPO_ROOT,
    ) == before_current
    if drifted.lineage.dispatch_path != request.lineage.dispatch_path:
        assert not drifted.lineage.dispatch_path.exists()


def test_partial_transaction_rejects_ambiguous_selected_replay_evidence(
    tmp_path: Path,
) -> None:
    request = _workspace(tmp_path)
    with pytest.raises(RuntimeError):
        simulate_selection_transaction(
            request,
            toolchain_root=REPO_ROOT,
            fault="after_idle_to_selected_cas_before_receipt",
        )
    transaction = _transaction_record(request.transaction_path)
    assert tuple(item["type"] for item in transaction["extensions"]) == (
        "dispatch_observed",
        "selected_input",
    )
    records = list(_store_replay_records(request.current_path))
    assert len(records) == 1
    assert records[0]["receipt"]["after_revision"] == (
        request.expected_initial_state_revision + 1
    )
    _replace_store_replay_records(request.current_path, [records[0], _thaw(records[0])])
    before = _durable_bytes(request)

    with pytest.raises(PlanningStoreError, match="store.ambiguous_replay"):
        simulate_selection_transaction(request, toolchain_root=REPO_ROOT)

    assert _durable_bytes(request) == before
    assert _transaction_record(request.transaction_path) == transaction
    dispatch = read_artifact_document(
        request.lineage.dispatch_path,
        toolchain_root=REPO_ROOT,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=request.lineage.dispatch_producer,
    )
    assert dispatch.logical_revision == 1
    assert not request.lineage.runway_path.exists()


def test_unexplained_state_movement_blocks_resume_and_preserves_evidence(
    tmp_path: Path,
) -> None:
    request = _workspace(tmp_path)
    with pytest.raises(RuntimeError):
        simulate_selection_transaction(
            request,
            toolchain_root=REPO_ROOT,
            fault="before_idle_to_selected_cas",
        )
    request.current_path.write_text(
        request.current_path.read_text(encoding="utf-8").replace("revision: 1", "revision: 9"),
        encoding="utf-8",
    )
    transaction_bytes = request.transaction_path.read_bytes()

    with pytest.raises(PlanningStoreError, match="store.revision_mismatch"):
        simulate_selection_transaction(request, toolchain_root=REPO_ROOT)

    assert request.transaction_path.read_bytes() == transaction_bytes


def test_transaction_schema_rejects_unknown_fields(tmp_path: Path) -> None:
    request = _workspace(tmp_path)
    simulate_selection_transaction(request, toolchain_root=REPO_ROOT)
    request.transaction_path.write_text(
        request.transaction_path.read_text(encoding="utf-8").replace(
            "producer:\n",
            "unexpected: true\nproducer:\n",
        ),
        encoding="utf-8",
    )

    result = validate_planning_contracts(
        [request.transaction_path],
        toolchain_root=REPO_ROOT,
    )

    assert not result.is_valid
    assert result.diagnostics[0].code == "schema.additionalProperties"
    assert "Additional properties are not allowed" in result.diagnostics[0].message


def test_transaction_reader_rejects_valid_events_out_of_order(tmp_path: Path) -> None:
    request = _workspace(tmp_path)
    simulate_selection_transaction(request, toolchain_root=REPO_ROOT)
    record = _transaction_record(request.transaction_path)
    record["extensions"][0], record["extensions"][1] = (
        record["extensions"][1],
        record["extensions"][0],
    )
    request.transaction_path.write_text(
        render_planning_contract(
            record,
            toolchain_root=REPO_ROOT,
            expected_producer_identity=request.producer,
        ),
        encoding="utf-8",
    )

    with pytest.raises(PlanningStoreError, match="transaction.sequence"):
        simulate_selection_transaction(request, toolchain_root=REPO_ROOT)
