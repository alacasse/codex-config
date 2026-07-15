"""Validate canonical planning artifact blocks against closed-world v1 schemas."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final, Literal, TypeAlias, cast

import yaml
from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError
from yaml.constructor import ConstructorError
from yaml.events import (
    AliasEvent,
    MappingEndEvent,
    MappingStartEvent,
    ScalarEvent,
    SequenceEndEvent,
    SequenceStartEvent,
)
from yaml.nodes import MappingNode, ScalarNode


SUPPORTED_SCHEMAS: Final = (
    "planning-current/v1",
    "planning-finding/v1",
    "planning-dispatch/v1",
    "planning-runway/v1",
    "planning-closeout/v1",
    "planning-selection-transaction/v1",
)
_SCHEMA_PATHS: Final = {
    name: Path("schemas") / f"{name.replace('/', '-')}.schema.json"
    for name in SUPPORTED_SCHEMAS
}
_OPERATIONAL_HEADING: Final = "## Operational Contract"
_H2: Final = re.compile(r"^##(?: |$)")
_FENCE_OPEN: Final = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
_YAML_FENCE: Final = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})yaml[ \t]*$")
_PROSE_ASSIGNMENT: Final = re.compile(
    r"^ {0,3}(?:[-*+] )?(?:\*\*)?"
    r"(?P<label>[A-Za-z][A-Za-z0-9_. -]*?)"
    r"(?:(?:\*\*)?:|:(?:\*\*)?)[ \t]+(?P<value>\S.*)$"
)
_LEGACY_LABELS: Final = {
    "Program slug": "program",
    "Current ledger": "ledger",
    "Selected dispatch path": "selected_dispatch",
    "Active Batch Runway spec path": "active_runway",
    "Queued batch path or ID": "queued_runway",
    "Latest closeout path": "latest_closeout",
}
_CURRENT_STORE_INTERFACE: Final = "current-store/v1"
_LEDGER_STORE_INTERFACE: Final = "ledger-store/v1"
_ARTIFACT_STORE_INTERFACE: Final = "artifact-store/v1"
_STORE_RECEIPT_INTERFACE: Final = "planning-store-receipt/v1"
_DERIVED_INDEX_INTERFACE: Final = "planning-derived-index/v1"
_GLOBAL_LEDGER_INTERFACE: Final = "planning-ledger-global-comparison/v1"
_STORE_ACTIONS: Final = frozenset({"create", "update", "merge", "no-op", "reconcile"})
_ARTIFACT_SCHEMAS: Final = frozenset(
    {
        "planning-dispatch/v1",
        "planning-runway/v1",
        "planning-closeout/v1",
    }
)
_EMPTY_FILE_HASH: Final = hashlib.sha256(b"").hexdigest()
_TRANSACTION_SCHEMA: Final = "planning-selection-transaction/v1"
_SELECTION_STAGE_PLAN: Final = (
    "write_and_validate_dispatch",
    "cas_idle_to_selected_and_persist_transition_receipt",
    "write_and_validate_runway",
    "cas_selected_to_queued_and_persist_transition_receipt",
)
_TRANSACTION_EXTENSION_ORDER: Final = (
    "dispatch_observed",
    "selected_input",
    "selected_observed",
    "runway_input",
    "runway_observed",
    "queued_input",
    "queued_observed",
)

JsonValue: TypeAlias = (
    str | int | float | bool | None | dict[str, "JsonValue"] | list["JsonValue"]
)
JsonObject: TypeAlias = dict[str, JsonValue]
FaultPoint: TypeAlias = Literal[
    "before_replace",
    "after_replace_before_validation",
    "after_replace_before_return",
]
SelectionFaultPoint: TypeAlias = Literal[
    "after_transaction_record_append",
    "before_dispatch_write",
    "after_dispatch_write_before_validation",
    "after_dispatch_validation",
    "before_idle_to_selected_cas",
    "after_idle_to_selected_cas_before_receipt",
    "after_selected_transition_receipt",
    "before_runway_write",
    "after_runway_write_before_validation",
    "after_runway_validation",
    "before_selected_to_queued_cas",
    "after_selected_to_queued_cas_before_receipt",
    "after_queued_transition_receipt",
]


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys at every depth."""

    def construct_mapping(
        self,
        node: MappingNode,
        deep: bool = False,
    ) -> dict[Hashable, Any]:
        seen: set[Hashable] = set()
        for key_node, _ in node.value:
            key = cast(Any, self).construct_object(key_node, deep=deep)
            if not isinstance(key, Hashable):
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable key",
                    key_node.start_mark,
                )
            if key in seen:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


@dataclass(frozen=True, order=True)
class Diagnostic:
    """One deterministic path-qualified contract finding."""

    path: str
    location: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.location}: {self.code}: {self.message}"


@dataclass(frozen=True)
class ProducerIdentity:
    """Explicit expected producer identity; process state is never evidence."""

    toolchain_generation: str
    toolchain_commit: str
    schema_version: str


@dataclass(frozen=True)
class ParsedPlanningContract:
    """A schema-valid canonical planning contract and its source path."""

    path: Path
    contract: Mapping[str, JsonValue]


@dataclass(frozen=True)
class LegacyCurrentState:
    """Narrow read-only projection of the active pre-v1 CURRENT format."""

    path: Path
    program: str
    ledger: str
    selected_dispatch: str | None
    queued_runway: str | None
    active_runway: str | None
    latest_closeout: str | None


@dataclass(frozen=True)
class ReadOnlyCompatibility:
    """Caller-scoped allowlist for active old-format CURRENT documents."""

    active_current_paths: frozenset[Path]


@dataclass(frozen=True)
class ValidationResult:
    """Validated canonical contracts, compatibility reads, and diagnostics."""

    contracts: tuple[ParsedPlanningContract, ...]
    compatibility_reads: tuple[LegacyCurrentState, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def is_valid(self) -> bool:
        return not self.diagnostics


class PlanningStoreError(ValueError):
    """Raised when a planning store rejects a request without semantic choice."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


class InjectedStoreFailure(RuntimeError):
    """Deterministic fault injected around the atomic replacement boundary."""


class InjectedSelectionFailure(RuntimeError):
    """Deterministic fault injected between durable selection-saga steps."""


@dataclass(frozen=True)
class StoreReceipt:
    """Immutable before/after evidence persisted through replay metadata."""

    interface: str
    store_interface: str
    idempotency_key: str
    request_hash: str
    before_revision: int
    after_revision: int
    touched_finding_ids: tuple[str, ...]


@dataclass(frozen=True)
class StoreApplyResult:
    """One applied or exact-replay store outcome."""

    outcome: Literal["applied", "exact_replay"]
    receipt: StoreReceipt


@dataclass(frozen=True)
class CurrentSnapshot:
    """Immutable parsed current document with its full-file CAS hash."""

    path: Path
    contract: Mapping[str, object]
    logical_revision: int
    file_hash: str


@dataclass(frozen=True)
class LedgerSnapshot:
    """Immutable whole-ledger projection and its full-file CAS facts."""

    path: Path
    findings: Mapping[str, Mapping[str, object]]
    logical_revision: int
    file_hash: str


@dataclass(frozen=True)
class LedgerLayoutComparison:
    """Mechanical per-finding/global representation comparison."""

    equivalent: bool
    semantic_equal: bool
    projection_equal: bool
    duplicate_detection_green: bool
    diff_locality_green: bool
    error_locality_green: bool
    revision_behavior_green: bool
    source_identity_green: bool
    per_finding_changed_sections: tuple[str, ...]
    global_changed_sections: tuple[str, ...]


@dataclass(frozen=True)
class ArtifactLineage:
    """Explicit immutable facts shared by one dispatch/runway/closeout lineage."""

    planning_root: Path
    program: str
    batch_id: str
    included_finding_ids: tuple[str, ...]
    deferred_finding_ids: tuple[str, ...]
    batch_kind: str
    ledger_path: Path
    ledger_revision: str
    dispatch_path: Path
    dispatch_revision: str
    runway_path: Path
    closeout_path: Path
    toolchain_source_root: Path
    canonical_planning_repository_root: Path
    implementation_target_root: Path
    dispatch_producer: ProducerIdentity
    runway_producer: ProducerIdentity
    closeout_producer: ProducerIdentity


@dataclass(frozen=True)
class ArtifactSnapshot:
    """Immutable parsed artifact plus its revision and full-file CAS facts."""

    path: Path
    schema_name: str
    contract: Mapping[str, object]
    logical_revision: int
    file_hash: str


@dataclass(frozen=True)
class SelectionTransactionRequest:
    """Caller-owned exact inputs for one DEC-038 selection transaction."""

    transaction_id: str
    transaction_path: Path
    current_path: Path
    expected_initial_state_revision: int
    expected_initial_state_file_hash: str
    initial_current_contract: Mapping[str, object]
    lineage: ArtifactLineage
    dispatch_contract: Mapping[str, object]
    runway_contract: Mapping[str, object]
    command_owner_version: str
    producer: ProducerIdentity


@dataclass(frozen=True)
class SelectionTransactionResult:
    """Completed exact selection saga evidence."""

    outcome: Literal["completed", "exact_replay"]
    transaction_path: Path
    transaction_file_hash: str
    current_revision: int
    dispatch_revision: int
    runway_revision: int
    selected_receipt: StoreReceipt
    queued_receipt: StoreReceipt


@dataclass(frozen=True)
class _ReplayRecord:
    idempotency_key: str
    request_hash: str
    receipt: StoreReceipt


@dataclass(frozen=True)
class _StoreMetadata:
    interface: str
    store_revision: int
    replay_records: tuple[_ReplayRecord, ...]


@dataclass(frozen=True)
class _MutableLedger:
    findings: Mapping[str, JsonObject]
    metadata: _StoreMetadata


@dataclass(frozen=True)
class _ExtractedBlock:
    source: str
    fence_start: int
    fence_end: int


@dataclass(frozen=True)
class _YamlBlock:
    source: str
    fence_start: int
    fence_end: int


@dataclass(frozen=True)
class _SecondaryYamlParse:
    mapping: JsonObject | None
    error: str | None


@dataclass(frozen=True)
class _SecondaryYamlInspection:
    top_level_keys: tuple[str, ...]
    schema_value: str | None


def read_current_document(
    path: str | Path,
    *,
    toolchain_root: str | Path,
) -> CurrentSnapshot:
    """Read one canonical CURRENT document with immutable CAS facts."""

    current_path = Path(path)
    result = validate_planning_contracts([current_path], toolchain_root=toolchain_root)
    if not result.is_valid:
        raise PlanningStoreError("current.invalid", str(result.diagnostics[0]))
    if len(result.contracts) != 1:
        raise PlanningStoreError("current.contract_count", "expected one current contract")
    contract = result.contracts[0].contract
    if contract.get("schema") != "planning-current/v1":
        raise PlanningStoreError("current.schema", "expected planning-current/v1")
    revision = contract.get("revision")
    if not isinstance(revision, int):
        raise PlanningStoreError("current.revision", "revision must be an integer")
    text = current_path.read_text(encoding="utf-8")
    metadata = _parse_store_metadata(
        current_path,
        text,
        interface=_CURRENT_STORE_INTERFACE,
        default_revision=revision,
    )
    if metadata.store_revision != revision:
        raise PlanningStoreError(
            "current.store_revision_mismatch",
            "canonical current revision does not match embedded store_revision",
        )
    return CurrentSnapshot(
        path=current_path,
        contract=cast(Mapping[str, object], _freeze_json(contract)),
        logical_revision=revision,
        file_hash=_file_hash(current_path),
    )


def apply_current_document(
    path: str | Path,
    *,
    toolchain_root: str | Path,
    expected_revision: int,
    expected_file_hash: str,
    replacement_contract: Mapping[str, object],
    idempotency_key: str,
    fault: FaultPoint | None = None,
) -> StoreApplyResult:
    """Apply one caller-supplied current contract under revision and file CAS."""

    current_path = Path(path)
    key = _require_idempotency_key(idempotency_key)
    original_text = current_path.read_text(encoding="utf-8")
    metadata = _parse_store_metadata(
        current_path,
        original_text,
        interface=_CURRENT_STORE_INTERFACE,
        default_revision=expected_revision,
    )
    replacement = _json_object_copy(replacement_contract, "replacement_contract")
    request_hash = _canonical_request_hash(
        {
            "operation": "apply_current_document",
            "expected_revision": expected_revision,
            "expected_file_hash": expected_file_hash,
            "replacement_contract": replacement,
            "idempotency_key": key,
        }
    )
    snapshot = read_current_document(current_path, toolchain_root=toolchain_root)
    replay = _evaluate_replay(
        metadata,
        key=key,
        request_hash=request_hash,
        store_interface=_CURRENT_STORE_INTERFACE,
        before_revision=expected_revision,
        after_revision=expected_revision + 1,
        touched_finding_ids=(),
    )
    if replay is not None:
        return StoreApplyResult(outcome="exact_replay", receipt=replay)

    _validate_cas(
        actual_revision=snapshot.logical_revision,
        actual_file_hash=snapshot.file_hash,
        expected_revision=expected_revision,
        expected_file_hash=expected_file_hash,
    )
    replacement_revision = replacement.get("revision")
    if replacement.get("schema") != "planning-current/v1":
        raise PlanningStoreError("current.schema", "replacement must use planning-current/v1")
    if replacement_revision != expected_revision + 1:
        raise PlanningStoreError(
            "current.revision_step",
            "replacement revision must equal expected revision plus one",
        )
    rendered_section = render_planning_contract(
        replacement,
        toolchain_root=toolchain_root,
    )
    receipt = StoreReceipt(
        interface=_STORE_RECEIPT_INTERFACE,
        store_interface=_CURRENT_STORE_INTERFACE,
        idempotency_key=key,
        request_hash=request_hash,
        before_revision=expected_revision,
        after_revision=cast(int, replacement_revision),
        touched_finding_ids=(),
    )
    updated_metadata = _with_replay_record(
        metadata,
        store_revision=cast(int, replacement_revision),
        receipt=receipt,
    )
    rendered = _replace_canonical_section(original_text, rendered_section)
    rendered = _replace_or_append_store_metadata(rendered, updated_metadata)
    _atomic_replace_and_validate(
        current_path,
        rendered,
        fault=fault,
        validate=lambda: read_current_document(
            current_path,
            toolchain_root=toolchain_root,
        ),
    )
    return StoreApplyResult(outcome="applied", receipt=receipt)


def read_ledger_document(
    path: str | Path,
    *,
    toolchain_root: str | Path,
) -> LedgerSnapshot:
    """Read and validate a whole per-finding ledger plus its derived index."""

    ledger_path = Path(path)
    text = ledger_path.read_text(encoding="utf-8")
    findings, metadata = _parse_per_finding_ledger(
        ledger_path,
        text,
        toolchain_root=Path(toolchain_root).resolve(),
    )
    frozen_findings = {
        finding_id: cast(Mapping[str, object], _freeze_json(contract))
        for finding_id, contract in findings.items()
    }
    return LedgerSnapshot(
        path=ledger_path,
        findings=MappingProxyType(frozen_findings),
        logical_revision=metadata.store_revision,
        file_hash=_file_hash(ledger_path),
    )


def apply_ledger_decision(
    path: str | Path,
    *,
    toolchain_root: str | Path,
    expected_revision: int,
    expected_file_hash: str,
    action: str,
    finding_mutations: Sequence[Mapping[str, object]],
    touched_finding_revisions: Mapping[str, int | None],
    idempotency_key: str,
    fault: FaultPoint | None = None,
) -> StoreApplyResult:
    """Apply one explicit caller decision through ledger-store/v1 mechanics."""

    if action not in _STORE_ACTIONS:
        raise PlanningStoreError("ledger.action", f"unsupported caller action {action!r}")
    ledger_path = Path(path)
    key = _require_idempotency_key(idempotency_key)
    original_text = ledger_path.read_text(encoding="utf-8")
    findings, metadata = _parse_per_finding_ledger(
        ledger_path,
        original_text,
        toolchain_root=Path(toolchain_root).resolve(),
    )
    mutations = tuple(
        _json_object_copy(value, f"finding_mutations[{index}]")
        for index, value in enumerate(finding_mutations)
    )
    touched_revisions = dict(touched_finding_revisions)
    request_hash = _canonical_request_hash(
        {
            "operation": "apply_ledger_decision",
            "expected_revision": expected_revision,
            "expected_file_hash": expected_file_hash,
            "action": action,
            "finding_mutations": list(mutations),
            "touched_finding_revisions": touched_revisions,
            "idempotency_key": key,
        }
    )
    requested_touched_ids = _requested_touched_finding_ids(
        mutations,
        touched_finding_revisions=touched_revisions,
    )
    replay = _evaluate_replay(
        metadata,
        key=key,
        request_hash=request_hash,
        store_interface=_LEDGER_STORE_INTERFACE,
        before_revision=expected_revision,
        after_revision=expected_revision + 1,
        touched_finding_ids=requested_touched_ids,
    )
    if replay is not None:
        return StoreApplyResult(outcome="exact_replay", receipt=replay)
    _validate_cas(
        actual_revision=metadata.store_revision,
        actual_file_hash=_file_hash(ledger_path),
        expected_revision=expected_revision,
        expected_file_hash=expected_file_hash,
    )
    resulting, touched_ids = _apply_finding_mutations(
        findings,
        mutations=mutations,
        touched_finding_revisions=touched_revisions,
        toolchain_root=Path(toolchain_root).resolve(),
    )
    after_revision = expected_revision + 1
    receipt = StoreReceipt(
        interface=_STORE_RECEIPT_INTERFACE,
        store_interface=_LEDGER_STORE_INTERFACE,
        idempotency_key=key,
        request_hash=request_hash,
        before_revision=expected_revision,
        after_revision=after_revision,
        touched_finding_ids=touched_ids,
    )
    updated_metadata = _with_replay_record(
        metadata,
        store_revision=after_revision,
        receipt=receipt,
    )
    rendered = _render_per_finding_ledger(
        ledger_path,
        resulting,
        updated_metadata,
        toolchain_root=Path(toolchain_root).resolve(),
    )
    _atomic_replace_and_validate(
        ledger_path,
        rendered,
        fault=fault,
        validate=lambda: read_ledger_document(
            ledger_path,
            toolchain_root=toolchain_root,
        ),
    )
    return StoreApplyResult(outcome="applied", receipt=receipt)


def read_artifact_document(
    path: str | Path,
    *,
    toolchain_root: str | Path,
    expected_schema: str,
    expected_producer_identity: ProducerIdentity,
) -> ArtifactSnapshot:
    """Read one validated dispatch, runway, or closeout with store CAS facts."""

    if expected_schema not in _ARTIFACT_SCHEMAS:
        raise PlanningStoreError(
            "artifact.schema",
            f"unsupported artifact schema {expected_schema!r}",
        )
    artifact_path = Path(path)
    result = validate_planning_contracts(
        [artifact_path],
        toolchain_root=toolchain_root,
        expected_producer_identity=expected_producer_identity,
    )
    if not result.is_valid:
        raise PlanningStoreError("artifact.invalid", str(result.diagnostics[0]))
    if len(result.contracts) != 1:
        raise PlanningStoreError("artifact.contract_count", "expected one artifact contract")
    contract = result.contracts[0].contract
    if contract.get("schema") != expected_schema:
        raise PlanningStoreError(
            "artifact.schema",
            f"expected {expected_schema!r}; got {contract.get('schema')!r}",
        )
    text = artifact_path.read_text(encoding="utf-8")
    metadata = _parse_store_metadata(
        artifact_path,
        text,
        interface=_ARTIFACT_STORE_INTERFACE,
        default_revision=0,
    )
    return ArtifactSnapshot(
        path=artifact_path,
        schema_name=expected_schema,
        contract=cast(Mapping[str, object], _freeze_json(contract)),
        logical_revision=metadata.store_revision,
        file_hash=_file_hash(artifact_path),
    )


def write_dispatch_artifact(
    path: str | Path,
    *,
    toolchain_root: str | Path,
    expected_revision: int,
    expected_file_hash: str,
    contract: Mapping[str, object],
    lineage: ArtifactLineage,
    idempotency_key: str,
    fault: FaultPoint | None = None,
) -> StoreApplyResult:
    """Write one immutable dispatch through the shared revisioned store."""

    _validate_lineage_paths(lineage)
    artifact_path = _require_lineage_target(path, lineage.dispatch_path)
    binding = _dispatch_lineage_binding(lineage)
    return _apply_artifact_document(
        artifact_path,
        toolchain_root=toolchain_root,
        expected_revision=expected_revision,
        expected_file_hash=expected_file_hash,
        contract=contract,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=lineage.dispatch_producer,
        lineage_binding=binding,
        validate_payload=lambda value: _validate_dispatch_lineage(value, lineage),
        idempotency_key=idempotency_key,
        fault=fault,
    )


def write_runway_artifact(
    path: str | Path,
    *,
    toolchain_root: str | Path,
    expected_revision: int,
    expected_file_hash: str,
    expected_dispatch_file_hash: str,
    contract: Mapping[str, object],
    lineage: ArtifactLineage,
    idempotency_key: str,
    fault: FaultPoint | None = None,
) -> StoreApplyResult:
    """Write one immutable runway bound to an exact validated dispatch."""

    _validate_lineage_paths(lineage)
    artifact_path = _require_lineage_target(path, lineage.runway_path)

    def validate_payload(value: Mapping[str, object]) -> None:
        _validate_dispatch_predecessor(
            lineage,
            toolchain_root=toolchain_root,
            expected_file_hash=expected_dispatch_file_hash,
        )
        _validate_runway_lineage(value, lineage)

    binding: JsonObject = {
        **_runway_lineage_binding(lineage),
        "expected_dispatch_file_hash": expected_dispatch_file_hash,
    }
    return _apply_artifact_document(
        artifact_path,
        toolchain_root=toolchain_root,
        expected_revision=expected_revision,
        expected_file_hash=expected_file_hash,
        contract=contract,
        expected_schema="planning-runway/v1",
        expected_producer_identity=lineage.runway_producer,
        lineage_binding=binding,
        validate_payload=validate_payload,
        idempotency_key=idempotency_key,
        fault=fault,
    )


def write_closeout_artifact(
    path: str | Path,
    *,
    toolchain_root: str | Path,
    expected_revision: int,
    expected_file_hash: str,
    expected_dispatch_file_hash: str,
    expected_runway_file_hash: str,
    contract: Mapping[str, object],
    lineage: ArtifactLineage,
    idempotency_key: str,
    fault: FaultPoint | None = None,
) -> StoreApplyResult:
    """Write one immutable same-batch closeout bound to exact predecessors."""

    _validate_lineage_paths(lineage)
    artifact_path = _require_lineage_target(path, lineage.closeout_path)

    def validate_payload(value: Mapping[str, object]) -> None:
        _validate_dispatch_predecessor(
            lineage,
            toolchain_root=toolchain_root,
            expected_file_hash=expected_dispatch_file_hash,
        )
        _validate_runway_predecessor(
            lineage,
            toolchain_root=toolchain_root,
            expected_file_hash=expected_runway_file_hash,
        )
        _validate_closeout_lineage(value, lineage)

    binding: JsonObject = {
        **_closeout_lineage_binding(lineage),
        "expected_dispatch_file_hash": expected_dispatch_file_hash,
        "expected_runway_file_hash": expected_runway_file_hash,
    }
    return _apply_artifact_document(
        artifact_path,
        toolchain_root=toolchain_root,
        expected_revision=expected_revision,
        expected_file_hash=expected_file_hash,
        contract=contract,
        expected_schema="planning-closeout/v1",
        expected_producer_identity=lineage.closeout_producer,
        lineage_binding=binding,
        validate_payload=validate_payload,
        idempotency_key=idempotency_key,
        fault=fault,
    )


def simulate_selection_transaction(
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
    fault: SelectionFaultPoint | None = None,
) -> SelectionTransactionResult:
    """Run or resume the exact four-stage DEC-038 selection transaction."""

    _validate_selection_request(request, toolchain_root=toolchain_root)
    transaction_path = request.transaction_path
    if transaction_path.is_file() and transaction_path.stat().st_size > 0:
        record = _read_transaction_record(
            transaction_path,
            toolchain_root=toolchain_root,
            expected_producer=request.producer,
        )
        _validate_transaction_binding(record, request)
        started_complete = len(_transaction_extensions(record)) == len(
            _TRANSACTION_EXTENSION_ORDER
        )
    else:
        current = read_current_document(request.current_path, toolchain_root=toolchain_root)
        _validate_initial_current(request, current)
        record = _initial_transaction_record(request)
        _persist_transaction_record(
            transaction_path,
            record,
            toolchain_root=toolchain_root,
            expected_file_hash=_EMPTY_FILE_HASH,
            expected_producer=request.producer,
        )
        started_complete = False
        _raise_selection_fault(fault, "after_transaction_record_append")

    record = _run_dispatch_stage(
        record,
        request,
        toolchain_root=toolchain_root,
        fault=fault,
    )
    record = _run_selected_stage(
        record,
        request,
        toolchain_root=toolchain_root,
        fault=fault,
    )
    record = _run_runway_stage(
        record,
        request,
        toolchain_root=toolchain_root,
        fault=fault,
    )
    record = _run_queued_stage(
        record,
        request,
        toolchain_root=toolchain_root,
        fault=fault,
    )
    return _selection_result(
        record,
        request,
        toolchain_root=toolchain_root,
        outcome="exact_replay" if started_complete else "completed",
    )


def compare_ledger_layouts(
    per_finding_path: str | Path,
    global_path: str | Path,
    *,
    toolchain_root: str | Path,
) -> LedgerLayoutComparison:
    """Compare the accepted per-finding default with one global prototype."""

    per_path = _single_markdown_path(Path(per_finding_path))
    global_document = _single_markdown_path(Path(global_path))
    per_snapshot = read_ledger_document(per_path, toolchain_root=toolchain_root)
    global_findings, global_revision = _parse_global_ledger(
        global_document,
        toolchain_root=Path(toolchain_root).resolve(),
        expected_source_artifact=per_path.name,
    )
    per_semantic = _semantic_findings(per_snapshot.findings)
    global_semantic = _semantic_findings(global_findings)
    semantic_equal = per_semantic == global_semantic
    projection_equal = (
        _derived_entries(per_snapshot.findings)
        == _derived_entries(global_findings)
        and per_snapshot.logical_revision == global_revision
    )
    per_changed_path = _required_variant(per_path, "one-finding-change.md")
    global_changed_path = _required_variant(global_document, "one-finding-change.md")
    per_changed = read_ledger_document(per_changed_path, toolchain_root=toolchain_root)
    global_changed, global_changed_revision = _parse_global_ledger(
        global_changed_path,
        toolchain_root=Path(toolchain_root).resolve(),
        expected_source_artifact=per_path.name,
    )
    changed_semantic_equal = (
        _semantic_findings(per_changed.findings)
        == _semantic_findings(global_changed)
    )
    changed_projection_equal = (
        _derived_entries(per_changed.findings) == _derived_entries(global_changed)
    )
    per_changed_sections = _changed_top_level_sections(per_path, per_changed_path)
    global_changed_sections = _changed_top_level_sections(
        global_document,
        global_changed_path,
    )
    diff_locality_green = (
        per_changed_sections
        == ("Derived Index", "Finding CCFG-1", "Store Metadata")
        and global_changed_sections == ("Global Comparison",)
    )
    per_duplicate = _capture_store_error(
        lambda: read_ledger_document(
            _required_variant(per_path, "duplicate.md"),
            toolchain_root=toolchain_root,
        )
    )
    global_duplicate = _capture_store_error(
        lambda: _parse_global_ledger(
            _required_variant(global_document, "duplicate.md"),
            toolchain_root=Path(toolchain_root).resolve(),
            expected_source_artifact=per_path.name,
        )
    )
    duplicate_detection_green = (
        per_duplicate is not None
        and per_duplicate.code == "ledger.duplicate_id"
        and global_duplicate is not None
        and global_duplicate.code == "ledger.duplicate_id"
    )
    per_error = _capture_store_error(
        lambda: read_ledger_document(
            _required_variant(per_path, "invalid-locality.md"),
            toolchain_root=toolchain_root,
        )
    )
    global_error = _capture_store_error(
        lambda: _parse_global_ledger(
            _required_variant(global_document, "invalid-locality.md"),
            toolchain_root=Path(toolchain_root).resolve(),
            expected_source_artifact=per_path.name,
        )
    )
    error_locality_green = (
        per_error is not None
        and "CCFG-2" in str(per_error)
        and "line" in str(per_error)
        and global_error is not None
        and "CCFG-2" in str(global_error)
        and "index 1" in str(global_error)
    )
    divergent_findings, divergent_revision = _parse_global_ledger(
        _required_variant(global_document, "revision-divergence.md"),
        toolchain_root=Path(toolchain_root).resolve(),
        expected_source_artifact=per_path.name,
    )
    revision_behavior_green = (
        per_changed.logical_revision == global_changed_revision
        and divergent_revision != per_snapshot.logical_revision
        and _semantic_findings(divergent_findings) == global_semantic
    )
    wrong_source = _capture_store_error(
        lambda: _parse_global_ledger(
            _required_variant(global_document, "wrong-source.md"),
            toolchain_root=Path(toolchain_root).resolve(),
            expected_source_artifact=per_path.name,
        )
    )
    source_identity_green = (
        wrong_source is not None and wrong_source.code == "ledger.global_source"
    )
    all_measures_green = all(
        (
            duplicate_detection_green,
            diff_locality_green,
            error_locality_green,
            revision_behavior_green,
            source_identity_green,
            changed_semantic_equal,
            changed_projection_equal,
        )
    )
    return LedgerLayoutComparison(
        equivalent=semantic_equal and projection_equal and all_measures_green,
        semantic_equal=semantic_equal,
        projection_equal=projection_equal,
        duplicate_detection_green=duplicate_detection_green,
        diff_locality_green=diff_locality_green,
        error_locality_green=error_locality_green,
        revision_behavior_green=revision_behavior_green,
        source_identity_green=source_identity_green,
        per_finding_changed_sections=per_changed_sections,
        global_changed_sections=global_changed_sections,
    )


def validate_planning_contracts(
    contract_paths: Iterable[str | Path],
    *,
    toolchain_root: str | Path,
    expected_producer_identity: ProducerIdentity | None = None,
    compatibility: ReadOnlyCompatibility | None = None,
) -> ValidationResult:
    """Validate an explicit catalog through the five canonical schema owners."""

    root = Path(toolchain_root).resolve()
    diagnostics: list[Diagnostic] = []
    validators, schemas = _load_validators(root, diagnostics)
    paths = _expand_paths(contract_paths, diagnostics)
    allowed_legacy: frozenset[Path] = (
        frozenset(path.resolve() for path in compatibility.active_current_paths)
        if compatibility is not None
        else frozenset()
    )
    contracts: list[ParsedPlanningContract] = []
    compatibility_reads: list[LegacyCurrentState] = []

    for path in paths:
        text = _read_text(path, diagnostics)
        if text is None:
            continue
        if _document_has_interface(text, _LEDGER_STORE_INTERFACE):
            try:
                ledger_findings, _ = _parse_per_finding_ledger(
                    path,
                    text,
                    toolchain_root=root,
                )
            except PlanningStoreError as error:
                diagnostics.append(
                    Diagnostic(str(path), "$", error.code, str(error))
                )
            else:
                contracts.extend(
                    ParsedPlanningContract(path=path, contract=contract)
                    for contract in ledger_findings.values()
                )
            continue
        block = _extract_operational_block(
            path,
            text,
            diagnostics,
            allow_absent=path.resolve() in allowed_legacy,
        )
        if block is None:
            if path.resolve() in allowed_legacy:
                legacy = _parse_legacy_current(path, text, diagnostics)
                if legacy is not None:
                    compatibility_reads.append(legacy)
            continue
        loaded = _load_contract_yaml(path, block.source, diagnostics)
        if loaded is None:
            continue
        schema_name = loaded.get("schema")
        if not isinstance(schema_name, str):
            diagnostics.append(
                Diagnostic(str(path), "$.schema", "contract.schema", "schema must be a string")
            )
            continue
        validator = validators.get(schema_name)
        if validator is None:
            code = (
                "schema.unsupported_version"
                if schema_name.rsplit("/", 1)[0] in {item.rsplit("/", 1)[0] for item in SUPPORTED_SCHEMAS}
                else "schema.unsupported"
            )
            diagnostics.append(
                Diagnostic(str(path), "$.schema", code, f"unsupported schema {schema_name!r}")
            )
            continue
        schema = schemas[schema_name]
        schema_errors = sorted(
            validator.iter_errors(cast(Any, loaded)),  # pyright: ignore[reportUnknownMemberType]
            key=lambda error: (tuple(str(part) for part in error.absolute_path), error.validator, error.message),
        )
        for error in schema_errors:
            diagnostics.append(
                Diagnostic(
                    str(path),
                    _json_location(error.absolute_path),
                    f"schema.{error.validator}",
                    error.message,
                )
            )
        if schema_errors:
            continue
        _validate_canonical_machine_owner(
            path,
            text,
            canonical_block=block,
            contract=loaded,
            diagnostics=diagnostics,
        )
        _validate_prose_does_not_redefine_contract(
            path,
            text,
            contract=loaded,
            diagnostics=diagnostics,
        )
        _validate_expected_producer(
            path,
            loaded,
            expected_producer_identity,
            diagnostics,
        )
        if not any(item.path == str(path) for item in diagnostics):
            ordered = _order_by_schema(loaded, schema, schema)
            contracts.append(ParsedPlanningContract(path=path, contract=ordered))

    _validate_artifact_catalog_lineage(contracts, diagnostics)

    return ValidationResult(
        contracts=tuple(contracts),
        compatibility_reads=tuple(compatibility_reads),
        diagnostics=tuple(sorted(diagnostics)),
    )


def _validate_artifact_catalog_lineage(
    contracts: Sequence[ParsedPlanningContract],
    diagnostics: list[Diagnostic],
) -> None:
    by_schema: dict[str, list[ParsedPlanningContract]] = {}
    for parsed in contracts:
        schema_name = parsed.contract.get("schema")
        if isinstance(schema_name, str) and schema_name in _ARTIFACT_SCHEMAS:
            by_schema.setdefault(schema_name, []).append(parsed)
    if any(len(by_schema.get(schema, ())) != 1 for schema in _ARTIFACT_SCHEMAS):
        return
    dispatch = by_schema["planning-dispatch/v1"][0]
    runway = by_schema["planning-runway/v1"][0]
    closeout = by_schema["planning-closeout/v1"][0]
    try:
        dispatch_artifact = _nested_mapping(dispatch.contract, "artifact")
        dispatch_source = _nested_mapping(dispatch.contract, "source")
        dispatch_scope = _nested_mapping(dispatch.contract, "scope")
        dispatch_runway = _nested_mapping(dispatch.contract, "runway")
        dispatch_execution = _nested_mapping(dispatch.contract, "execution_context")
        dispatch_producer = _nested_mapping(dispatch.contract, "producer")
        runway_artifact = _nested_mapping(runway.contract, "artifact")
        runway_batch = _nested_mapping(runway.contract, "batch")
        runway_execution = _nested_mapping(runway.contract, "execution")
        runway_producer = _nested_mapping(runway.contract, "producer")
        closeout_artifact = _nested_mapping(closeout.contract, "artifact")
        closeout_reconciliation = _nested_mapping(closeout.contract, "reconciliation")
        closeout_execution = _nested_mapping(closeout.contract, "execution_context")
        closeout_producer = _nested_mapping(closeout.contract, "producer")
        batch_id = dispatch_artifact.get("id")
        _expect_artifact_fact("catalog runway batch", runway_artifact.get("id"), batch_id)
        _expect_artifact_fact(
            "catalog closeout batch",
            closeout_artifact.get("batch_id"),
            batch_id,
        )
        _expect_artifact_fact(
            "catalog dispatch revision",
            runway_artifact.get("source_dispatch_revision"),
            dispatch_artifact.get("revision"),
        )
        _expect_artifact_fact(
            "catalog dispatch reference",
            Path(cast(str, runway_artifact.get("source_dispatch"))).name,
            dispatch.path.name,
        )
        _expect_artifact_fact(
            "catalog runway reference",
            Path(cast(str, dispatch_runway.get("expected_path"))).name,
            runway.path.name,
        )
        _expect_artifact_fact(
            "catalog batch kind",
            runway_batch.get("kind"),
            dispatch_scope.get("batch_kind"),
        )
        source_findings = tuple(
            sorted(cast(Sequence[str], dispatch_source.get("finding_ids")))
        )
        scoped_findings = tuple(
            sorted(
                (
                    *cast(Sequence[str], dispatch_scope.get("included_finding_ids")),
                    *cast(Sequence[str], dispatch_scope.get("deferred_finding_ids")),
                )
            )
        )
        _expect_artifact_fact("catalog finding scope", source_findings, scoped_findings)
        _expect_artifact_fact(
            "catalog implementation root",
            runway_execution.get("implementation_target_root"),
            dispatch_execution.get("implementation_target_root"),
        )
        _expect_artifact_fact(
            "catalog closeout implementation root",
            closeout_execution.get("implementation_target_root"),
            dispatch_execution.get("implementation_target_root"),
        )
        _expect_artifact_fact(
            "catalog canonical planning repository root",
            closeout_execution.get("canonical_planning_repository_root"),
            dispatch_execution.get("canonical_planning_repository_root"),
        )
        _expect_artifact_fact(
            "catalog dispatch/runway producer generation",
            runway_producer.get("toolchain_generation"),
            dispatch_producer.get("toolchain_generation"),
        )
        _expect_artifact_fact(
            "catalog dispatch/runway producer commit",
            runway_producer.get("toolchain_commit"),
            dispatch_producer.get("toolchain_commit"),
        )
        _expect_artifact_fact(
            "catalog closeout producer generation",
            closeout_producer.get("toolchain_generation"),
            dispatch_producer.get("toolchain_generation"),
        )
        _expect_artifact_fact(
            "catalog closeout producer commit",
            closeout_producer.get("toolchain_commit"),
            dispatch_producer.get("toolchain_commit"),
        )
        for field in (
            "selected_dispatch_after",
            "queued_runway_after",
            "active_runway_after",
        ):
            _expect_artifact_fact(
                f"catalog closeout {field}",
                closeout_reconciliation.get(field),
                None,
            )
    except PlanningStoreError as error:
        diagnostics.append(
            Diagnostic(
                str(runway.path),
                "$",
                error.code,
                str(error),
            )
        )


def render_planning_contract(
    contract: Mapping[str, object],
    *,
    toolchain_root: str | Path,
    expected_producer_identity: ProducerIdentity | None = None,
) -> str:
    """Render one validated v1 contract; compatibility projections are unwritable."""

    if not isinstance(contract, Mapping):
        raise TypeError("only canonical mapping contracts can be rendered")
    root = Path(toolchain_root).resolve()
    diagnostics: list[Diagnostic] = []
    validators, schemas = _load_validators(root, diagnostics)
    if diagnostics:
        raise ValueError(str(diagnostics[0]))
    schema_name = contract.get("schema")
    if not isinstance(schema_name, str) or schema_name not in validators:
        raise ValueError(f"unsupported schema {schema_name!r}")
    errors = sorted(
        validators[schema_name].iter_errors(cast(Any, contract)),  # pyright: ignore[reportUnknownMemberType]
        key=lambda error: error.json_path,
    )
    if errors:
        raise ValueError(f"{errors[0].json_path}: {errors[0].message}")
    local_diagnostics: list[Diagnostic] = []
    _validate_expected_producer(
        Path("<render>"), contract, expected_producer_identity, local_diagnostics
    )
    if local_diagnostics:
        raise ValueError(str(local_diagnostics[0]))
    ordered = _order_by_schema(contract, schemas[schema_name], schemas[schema_name])
    body = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True)
    return f"{_OPERATIONAL_HEADING}\n\n```yaml\n{body}```\n"


def _load_validators(
    root: Path,
    diagnostics: list[Diagnostic],
) -> tuple[dict[str, Draft7Validator], dict[str, Mapping[str, JsonValue]]]:
    validators: dict[str, Draft7Validator] = {}
    schemas: dict[str, Mapping[str, JsonValue]] = {}
    for name, relative_path in _SCHEMA_PATHS.items():
        path = root / relative_path
        try:
            loaded = cast(object, json.loads(path.read_text(encoding="utf-8")))
            if not isinstance(loaded, dict):
                raise ValueError("schema root must be an object")
            loaded_mapping = cast(dict[object, object], loaded)
            if not all(isinstance(key, str) for key in loaded_mapping):
                raise ValueError("schema root must be a string-keyed object")
            schema = cast(JsonObject, loaded)
            Draft7Validator.check_schema(cast(Any, schema))
        except (OSError, json.JSONDecodeError, SchemaError, ValueError) as error:
            diagnostics.append(
                Diagnostic(str(path), "$", "schema.not_available", str(error))
            )
            continue
        schemas[name] = schema
        validators[name] = Draft7Validator(cast(Any, schema))
    return validators, schemas


def _expand_paths(
    values: Iterable[str | Path], diagnostics: list[Diagnostic]
) -> tuple[Path, ...]:
    expanded: set[Path] = set()
    for value in values:
        path = Path(value)
        if path.is_dir():
            matches = tuple(path.rglob("*.md"))
            if not matches:
                diagnostics.append(
                    Diagnostic(str(path), "$", "catalog.empty", "directory contains no Markdown contracts")
                )
            expanded.update(matches)
        elif path.is_file():
            expanded.add(path)
        else:
            diagnostics.append(
                Diagnostic(str(path), "$", "path.not_found", "contract path does not exist")
            )
    return tuple(sorted(expanded, key=lambda item: item.as_posix()))


def _read_text(path: Path, diagnostics: list[Diagnostic]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        diagnostics.append(Diagnostic(str(path), "$", "document.unreadable", str(error)))
        return None


def _extract_operational_block(
    path: Path,
    text: str,
    diagnostics: list[Diagnostic],
    *,
    allow_absent: bool = False,
) -> _ExtractedBlock | None:
    lines = text.splitlines()
    headings = _top_level_h2_indices(lines)
    matches = [index for index in headings if lines[index].strip() == _OPERATIONAL_HEADING]
    if not matches and allow_absent:
        return None
    if len(matches) != 1:
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.block_count", f"expected exactly one operational block; found {len(matches)}")
        )
        return None
    start = matches[0]
    if not headings or start != headings[0]:
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.location", "operational contract must be the first level-two section")
        )
        return None
    cursor = start + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    if cursor >= len(lines) or (fence := _YAML_FENCE.match(lines[cursor])) is None:
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.fence", "operational contract must contain one immediate yaml fence")
        )
        return None
    marker = fence.group("marker")
    end = cursor + 1
    while end < len(lines) and lines[end].strip() != marker:
        end += 1
    if end >= len(lines):
        diagnostics.append(Diagnostic(str(path), "$", "contract.fence", "operational yaml fence is unclosed"))
        return None
    section_end = next((index for index in headings if index > start), len(lines))
    if any(line.strip() for line in lines[end + 1 : section_end]):
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.second_owner", "operational section may contain only the canonical yaml block")
        )
        return None
    return _ExtractedBlock(
        source="\n".join(lines[cursor + 1 : end]),
        fence_start=cursor,
        fence_end=end,
    )


def _top_level_h2_indices(lines: Sequence[str]) -> list[int]:
    headings: list[int] = []
    active_marker: str | None = None
    for index, line in enumerate(lines):
        if active_marker is not None:
            stripped = line.strip()
            if stripped.startswith(active_marker) and not stripped[len(active_marker) :].strip():
                active_marker = None
            continue
        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            active_marker = fence.group("marker")
            continue
        if _H2.match(line):
            headings.append(index)
    return headings


def _top_level_yaml_blocks(lines: Sequence[str]) -> tuple[_YamlBlock, ...]:
    blocks: list[_YamlBlock] = []
    active_marker: str | None = None
    active_info = ""
    active_start = -1
    for index, line in enumerate(lines):
        if active_marker is not None:
            if line.strip() == active_marker:
                if active_info == "yaml":
                    blocks.append(
                        _YamlBlock(
                            source="\n".join(lines[active_start + 1 : index]),
                            fence_start=active_start,
                            fence_end=index,
                        )
                    )
                active_marker = None
            continue
        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            active_marker = fence.group("marker")
            active_info = fence.group("info").strip().lower()
            active_start = index
    return tuple(blocks)


def _validate_canonical_machine_owner(
    path: Path,
    text: str,
    *,
    canonical_block: _ExtractedBlock,
    contract: Mapping[str, object],
    diagnostics: list[Diagnostic],
) -> None:
    canonical_fields = set(contract) - {"schema"}
    supported_bases = {name.rsplit("/", 1)[0] for name in SUPPORTED_SCHEMAS}
    for block in _top_level_yaml_blocks(text.splitlines()):
        if block.fence_start == canonical_block.fence_start:
            continue
        inspection = _inspect_secondary_yaml(block.source)
        raw_fields = frozenset(inspection.top_level_keys)
        raw_schema = inspection.schema_value
        recognizable_raw_schema = raw_schema is not None and (
            raw_schema in SUPPORTED_SCHEMAS
            or raw_schema.rsplit("/", 1)[0] in supported_bases
        )
        recognizable_raw_fields = bool(canonical_fields.intersection(raw_fields))
        parsed = _parse_secondary_yaml(block.source)
        if parsed.error is not None:
            if recognizable_raw_schema or recognizable_raw_fields:
                diagnostics.append(
                    Diagnostic(
                        str(path),
                        f"$.line[{block.fence_start + 1}]",
                        "contract.invalid_secondary_yaml",
                        "recognizable secondary operational yaml is invalid: "
                        f"{parsed.error}",
                    )
                )
            continue
        loaded = parsed.mapping
        if loaded is None:
            continue
        schema_name = loaded.get("schema")
        recognizable_schema = isinstance(schema_name, str) and (
            schema_name in SUPPORTED_SCHEMAS
            or schema_name.rsplit("/", 1)[0] in supported_bases
        )
        overlapping_fields = sorted(canonical_fields.intersection(loaded))
        if not recognizable_schema and not overlapping_fields:
            continue
        reason = (
            f"supported planning schema {schema_name!r}"
            if recognizable_schema
            else f"operational field(s) {overlapping_fields!r}"
        )
        diagnostics.append(
            Diagnostic(
                str(path),
                f"$.line[{block.fence_start + 1}]",
                "contract.second_owner",
                f"top-level yaml block outside the canonical section defines {reason}",
            )
        )


def _parse_secondary_yaml(source: str) -> _SecondaryYamlParse:
    try:
        loaded = yaml.load(source, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as error:
        problem = cast(object, getattr(error, "problem", None))
        message = problem if isinstance(problem, str) else "malformed yaml"
        return _SecondaryYamlParse(mapping=None, error=message)
    if not isinstance(loaded, dict):
        return _SecondaryYamlParse(
            mapping=None,
            error="root is not a string-keyed mapping",
        )
    loaded_mapping = cast(dict[object, object], loaded)
    if not all(isinstance(key, str) for key in loaded_mapping):
        return _SecondaryYamlParse(
            mapping=None,
            error="root is not a string-keyed mapping",
        )
    return _SecondaryYamlParse(mapping=cast(JsonObject, loaded), error=None)


def _inspect_secondary_yaml(source: str) -> _SecondaryYamlInspection:
    try:
        node = cast(
            object,
            yaml.compose(  # pyright: ignore[reportUnknownMemberType]
                source,
                Loader=yaml.SafeLoader,
            ),
        )
    except yaml.YAMLError:
        return _inspect_partial_yaml_events(source)
    if not isinstance(node, MappingNode):
        return _SecondaryYamlInspection(top_level_keys=(), schema_value=None)
    keys: list[str] = []
    schema_value: str | None = None
    for key_node, value_node in node.value:
        if not isinstance(key_node, ScalarNode):
            continue
        key = key_node.value
        keys.append(key)
        if key == "schema" and isinstance(value_node, ScalarNode):
            schema_value = value_node.value
    return _SecondaryYamlInspection(
        top_level_keys=tuple(keys),
        schema_value=schema_value,
    )


def _inspect_partial_yaml_events(source: str) -> _SecondaryYamlInspection:
    keys: list[str] = []
    schema_value: str | None = None
    collection_stack: list[str] = []
    root_expects_key = False
    current_root_key: str | None = None
    try:
        events = cast(
            Iterable[object],
            yaml.parse(  # pyright: ignore[reportUnknownMemberType]
                source,
                Loader=yaml.SafeLoader,
            ),
        )
        for event in events:
            if isinstance(event, MappingStartEvent):
                if len(collection_stack) == 1 and not root_expects_key:
                    root_expects_key = True
                collection_stack.append("mapping")
                if len(collection_stack) == 1:
                    root_expects_key = True
                continue
            if isinstance(event, SequenceStartEvent):
                if len(collection_stack) == 1 and not root_expects_key:
                    root_expects_key = True
                collection_stack.append("sequence")
                continue
            if isinstance(event, (MappingEndEvent, SequenceEndEvent)):
                if collection_stack:
                    collection_stack.pop()
                continue
            if isinstance(event, AliasEvent):
                if len(collection_stack) == 1 and not root_expects_key:
                    root_expects_key = True
                continue
            if not isinstance(event, ScalarEvent):
                continue
            if collection_stack != ["mapping"]:
                continue
            if root_expects_key:
                current_root_key = event.value
                keys.append(event.value)
                root_expects_key = False
                continue
            if current_root_key == "schema":
                schema_value = event.value
            root_expects_key = True
    except yaml.YAMLError:
        pass
    return _SecondaryYamlInspection(
        top_level_keys=tuple(keys),
        schema_value=schema_value,
    )


def _validate_prose_does_not_redefine_contract(
    path: Path,
    text: str,
    *,
    contract: Mapping[str, object],
    diagnostics: list[Diagnostic],
) -> None:
    field_labels = _contract_field_labels(contract)
    active_marker: str | None = None
    for index, line in enumerate(text.splitlines()):
        if active_marker is not None:
            if line.strip() == active_marker:
                active_marker = None
            continue
        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            active_marker = fence.group("marker")
            continue
        assignment = _PROSE_ASSIGNMENT.match(line)
        if assignment is None:
            continue
        label = _normalize_field_label(assignment.group("label"))
        if label not in field_labels:
            continue
        diagnostics.append(
            Diagnostic(
                str(path),
                f"$.line[{index + 1}]",
                "contract.prose_redefinition",
                f"prose explicitly redefines operational field {label!r}",
            )
        )


def _contract_field_labels(
    value: object,
    prefix: str = "",
) -> frozenset[str]:
    labels: set[str] = set()
    if isinstance(value, Mapping):
        typed_value = cast(Mapping[object, object], value)
        for raw_key, child in typed_value.items():
            if not isinstance(raw_key, str):
                continue
            key = _normalize_field_label(raw_key)
            labels.add(key)
            dotted = f"{prefix}.{key}" if prefix else key
            labels.add(dotted)
            labels.update(_contract_field_labels(child, dotted))
    elif isinstance(value, list):
        for child in cast(list[object], value):
            labels.update(_contract_field_labels(child, prefix))
    return frozenset(labels)


def _normalize_field_label(value: str) -> str:
    normalized = re.sub(r"[ -]+", "_", value.strip().lower())
    return normalized.strip("_")


def _load_contract_yaml(
    path: Path, source: str, diagnostics: list[Diagnostic]
) -> JsonObject | None:
    try:
        loaded = yaml.load(source, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as error:
        diagnostics.append(Diagnostic(str(path), "$", "contract.invalid_yaml", str(error)))
        return None
    if not isinstance(loaded, dict):
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.root_type", "operational contract must be a string-keyed mapping")
        )
        return None
    loaded_mapping = cast(dict[object, object], loaded)
    if not all(isinstance(key, str) for key in loaded_mapping):
        diagnostics.append(
            Diagnostic(str(path), "$", "contract.root_type", "operational contract must be a string-keyed mapping")
        )
        return None
    return cast(JsonObject, loaded)


def _validate_expected_producer(
    path: Path,
    contract: Mapping[str, object],
    expected: ProducerIdentity | None,
    diagnostics: list[Diagnostic],
) -> None:
    if expected is None:
        return
    producer = cast(Mapping[str, object], contract["producer"])
    for field in ("toolchain_generation", "toolchain_commit", "schema_version"):
        actual = producer[field]
        wanted = getattr(expected, field)
        if actual != wanted:
            diagnostics.append(
                Diagnostic(str(path), f"$.producer.{field}", "producer.mismatch", f"expected {wanted!r}; got {actual!r}")
            )


def _parse_legacy_current(
    path: Path, text: str, diagnostics: list[Diagnostic]
) -> LegacyCurrentState | None:
    if "archive" in {part.lower() for part in path.parts}:
        diagnostics.append(
            Diagnostic(str(path), "$", "compatibility.archive_forbidden", "compatibility reads active CURRENT documents only")
        )
        return None
    lines = text.splitlines()
    try:
        start = lines.index("## Program") + 1
    except ValueError:
        diagnostics.append(
            Diagnostic(str(path), "$", "compatibility.unrecognized", "missing exact legacy Program section")
        )
        return None
    end = next((index for index in range(start, len(lines)) if _H2.match(lines[index])), len(lines))
    section_lines = lines[start:end]
    parsed_fields = _parse_legacy_program_fields(section_lines)
    values: dict[str, str | None] = {}
    for field in _LEGACY_LABELS.values():
        raw_value = parsed_fields.get(field)
        if raw_value is None:
            diagnostics.append(
                Diagnostic(str(path), f"$.{field}", "compatibility.unrecognized", f"missing exact legacy field {field!r}")
            )
            continue
        value = raw_value[1:-1] if raw_value.startswith("`") and raw_value.endswith("`") else raw_value
        values[field] = None if value in {"None", "None selected"} else value
    if len(values) != len(_LEGACY_LABELS):
        return None
    program = values["program"]
    ledger = values["ledger"]
    if program is None or ledger is None:
        diagnostics.append(
            Diagnostic(str(path), "$", "compatibility.unrecognized", "program and ledger cannot be None")
        )
        return None
    return LegacyCurrentState(
        path=path,
        program=program,
        ledger=ledger,
        selected_dispatch=values["selected_dispatch"],
        queued_runway=values["queued_runway"],
        active_runway=values["active_runway"],
        latest_closeout=values["latest_closeout"],
    )


def _parse_legacy_program_fields(lines: Sequence[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    active_field: str | None = None
    for line in lines:
        if line.startswith("- ") and ":" in line:
            label, value = line[2:].split(":", 1)
            active_field = _LEGACY_LABELS.get(label)
            if active_field is not None:
                parsed[active_field] = value.strip()
            continue
        if active_field is not None and line.startswith("  ") and line.strip():
            parsed[active_field] = f"{parsed[active_field]}{line.strip()}"
            continue
        if line.strip():
            active_field = None
    return parsed


def _json_location(parts: Iterable[object]) -> str:
    location = "$"
    for part in parts:
        location += f"[{part}]" if isinstance(part, int) else f".{part}"
    return location


def _order_by_schema(
    value: object,
    node: Mapping[str, JsonValue],
    root: Mapping[str, JsonValue],
) -> Any:
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/definitions/"):
        definitions = cast(JsonObject, root["definitions"])
        node = cast(JsonObject, definitions[ref.rsplit("/", 1)[1]])
    if isinstance(value, Mapping):
        properties = node.get("properties")
        if not isinstance(properties, dict):
            return dict(cast(Mapping[str, object], value))
        typed_properties = cast(JsonObject, properties)
        ordered: dict[str, Any] = {}
        typed_value = cast(Mapping[str, object], value)
        for key, child_schema in typed_properties.items():
            if key in typed_value and isinstance(child_schema, dict):
                ordered[key] = _order_by_schema(
                    typed_value[key], cast(JsonObject, child_schema), root
                )
        return ordered
    if isinstance(value, list):
        item_schema = node.get("items")
        if isinstance(item_schema, dict):
            return [
                _order_by_schema(item, cast(JsonObject, item_schema), root)
                for item in cast(list[object], value)
            ]
    return cast(object, value)


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_request_hash(value: Mapping[str, object]) -> str:
    encoded = json.dumps(
        _thaw_json(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _freeze_json(value: object) -> object:
    if isinstance(value, Mapping):
        typed = cast(Mapping[object, object], value)
        return MappingProxyType(
            {
                str(key): _freeze_json(child)
                for key, child in typed.items()
                if isinstance(key, str)
            }
        )
    if isinstance(value, list | tuple):
        return tuple(_freeze_json(child) for child in cast(Sequence[object], value))
    return value


def _thaw_json(value: object) -> JsonValue:
    if isinstance(value, Mapping):
        typed = cast(Mapping[object, object], value)
        return {
            str(key): _thaw_json(child)
            for key, child in typed.items()
            if isinstance(key, str)
        }
    if isinstance(value, list | tuple):
        return [_thaw_json(child) for child in cast(Sequence[object], value)]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise PlanningStoreError("store.json_type", f"unsupported value {type(value).__name__}")


def _json_object_copy(value: Mapping[str, object], field: str) -> JsonObject:
    thawed = _thaw_json(value)
    if not isinstance(thawed, dict):
        raise PlanningStoreError("store.request", f"{field} must be an object")
    return thawed


def _require_idempotency_key(value: str) -> str:
    if not value.strip():
        raise PlanningStoreError("store.idempotency_key", "idempotency key cannot be empty")
    return value


def _validate_cas(
    *,
    actual_revision: int,
    actual_file_hash: str,
    expected_revision: int,
    expected_file_hash: str,
) -> None:
    if actual_revision != expected_revision:
        raise PlanningStoreError(
            "store.revision_mismatch",
            f"expected revision {expected_revision}; got {actual_revision}",
        )
    if actual_file_hash != expected_file_hash:
        raise PlanningStoreError(
            "store.file_hash_mismatch",
            f"expected full-file hash {expected_file_hash}; got {actual_file_hash}",
        )


def _evaluate_replay(
    metadata: _StoreMetadata,
    *,
    key: str,
    request_hash: str,
    store_interface: str,
    before_revision: int,
    after_revision: int,
    touched_finding_ids: tuple[str, ...],
) -> StoreReceipt | None:
    matches = [record for record in metadata.replay_records if record.idempotency_key == key]
    if len(matches) > 1:
        raise PlanningStoreError(
            "store.ambiguous_replay",
            f"idempotency key {key!r} has ambiguous durable evidence",
        )
    if not matches:
        return None
    record = matches[0]
    if record.request_hash != request_hash:
        raise PlanningStoreError(
            "store.idempotency_mismatch",
            f"idempotency key {key!r} is bound to a different request",
        )
    receipt = record.receipt
    if (
        receipt.interface != _STORE_RECEIPT_INTERFACE
        or receipt.store_interface != store_interface
        or receipt.idempotency_key != key
        or receipt.request_hash != request_hash
        or receipt.before_revision != before_revision
        or receipt.after_revision != after_revision
        or receipt.touched_finding_ids != touched_finding_ids
    ):
        raise PlanningStoreError(
            "store.replay_result_mismatch",
            f"idempotency key {key!r} has a receipt result inconsistent with its request",
        )
    return receipt


def _with_replay_record(
    metadata: _StoreMetadata,
    *,
    store_revision: int,
    receipt: StoreReceipt,
) -> _StoreMetadata:
    record = _ReplayRecord(
        idempotency_key=receipt.idempotency_key,
        request_hash=receipt.request_hash,
        receipt=receipt,
    )
    return _StoreMetadata(
        interface=metadata.interface,
        store_revision=store_revision,
        replay_records=tuple(
            sorted(
                (*metadata.replay_records, record),
                key=lambda item: item.idempotency_key,
            )
        ),
    )


def _document_has_interface(text: str, interface: str) -> bool:
    for block in _top_level_yaml_blocks(text.splitlines()):
        parsed = _parse_secondary_yaml(block.source)
        if parsed.mapping is not None and parsed.mapping.get("interface") == interface:
            return True
    return False


def _parse_store_metadata(
    path: Path,
    text: str,
    *,
    interface: str,
    default_revision: int,
) -> _StoreMetadata:
    candidates: list[JsonObject] = []
    for block in _top_level_yaml_blocks(text.splitlines()):
        parsed = _parse_secondary_yaml(block.source)
        if parsed.mapping is not None and parsed.mapping.get("interface") == interface:
            candidates.append(parsed.mapping)
    if not candidates:
        return _StoreMetadata(interface=interface, store_revision=default_revision, replay_records=())
    if len(candidates) != 1:
        raise PlanningStoreError(
            "store.metadata_count",
            f"{path} must contain at most one {interface} metadata block",
        )
    value = candidates[0]
    _require_exact_fields(
        value,
        {"interface", "store_revision", "replay_records"},
        "store metadata",
    )
    revision = value.get("store_revision")
    records = value.get("replay_records")
    if not isinstance(revision, int) or revision < 0:
        raise PlanningStoreError("store.metadata", "store_revision must be non-negative")
    if not isinstance(records, list):
        raise PlanningStoreError("store.metadata", "replay_records must be a list")
    parsed_records = tuple(_parse_replay_record(item) for item in records)
    keys = [record.idempotency_key for record in parsed_records]
    if len(keys) != len(set(keys)):
        raise PlanningStoreError("store.ambiguous_replay", "duplicate idempotency records")
    if any(
        record.receipt.interface != _STORE_RECEIPT_INTERFACE
        or record.receipt.store_interface != interface
        for record in parsed_records
    ):
        raise PlanningStoreError(
            "store.metadata",
            "replay receipt interface does not match its containing store",
        )
    _validate_receipt_chain(parsed_records, store_revision=revision)
    return _StoreMetadata(
        interface=interface,
        store_revision=revision,
        replay_records=parsed_records,
    )


def _validate_receipt_chain(
    records: Sequence[_ReplayRecord],
    *,
    store_revision: int,
) -> None:
    if not records:
        return
    ordered = sorted(records, key=lambda record: record.receipt.after_revision)
    after_revisions = [record.receipt.after_revision for record in ordered]
    if len(after_revisions) != len(set(after_revisions)):
        raise PlanningStoreError(
            "store.ambiguous_replay",
            "multiple receipts claim the same after revision",
        )
    for record in ordered:
        receipt = record.receipt
        if receipt.after_revision != receipt.before_revision + 1:
            raise PlanningStoreError(
                "store.receipt_chain",
                "receipt before/after revisions must advance exactly once",
            )
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if previous.receipt.after_revision != current.receipt.before_revision:
            raise PlanningStoreError(
                "store.receipt_chain",
                "persisted receipt revisions are not contiguous",
            )
    if ordered[-1].receipt.after_revision != store_revision:
        raise PlanningStoreError(
            "store.receipt_chain",
            "latest persisted receipt does not end at store_revision",
        )


def _parse_replay_record(value: object) -> _ReplayRecord:
    if not isinstance(value, dict):
        raise PlanningStoreError("store.metadata", "replay record must be an object")
    record = cast(JsonObject, value)
    _require_exact_fields(
        record,
        {"idempotency_key", "request_hash", "receipt"},
        "replay record",
    )
    key = record.get("idempotency_key")
    request_hash = record.get("request_hash")
    receipt_value = record.get("receipt")
    if not isinstance(key, str) or not key:
        raise PlanningStoreError("store.metadata", "replay key must be non-empty")
    if not isinstance(request_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", request_hash):
        raise PlanningStoreError("store.metadata", "request_hash must be sha256")
    receipt = _parse_store_receipt(receipt_value)
    if receipt.idempotency_key != key or receipt.request_hash != request_hash:
        raise PlanningStoreError("store.metadata", "replay record and receipt disagree")
    return _ReplayRecord(key, request_hash, receipt)


def _parse_store_receipt(value: object) -> StoreReceipt:
    if not isinstance(value, dict):
        raise PlanningStoreError("store.metadata", "receipt must be an object")
    receipt = cast(JsonObject, value)
    _require_exact_fields(
        receipt,
        {
            "interface",
            "store_interface",
            "idempotency_key",
            "request_hash",
            "before_revision",
            "after_revision",
            "touched_finding_ids",
        },
        "receipt",
    )
    touched = receipt.get("touched_finding_ids")
    if not isinstance(touched, list) or not all(isinstance(item, str) for item in touched):
        raise PlanningStoreError("store.metadata", "touched_finding_ids must be strings")
    touched_ids = cast(list[str], touched)
    if touched_ids != sorted(set(touched_ids)):
        raise PlanningStoreError(
            "store.metadata",
            "touched_finding_ids must be sorted and unique",
        )
    before = receipt.get("before_revision")
    after = receipt.get("after_revision")
    values = (
        receipt.get("interface"),
        receipt.get("store_interface"),
        receipt.get("idempotency_key"),
        receipt.get("request_hash"),
    )
    if not all(isinstance(item, str) for item in values):
        raise PlanningStoreError("store.metadata", "receipt identity fields must be strings")
    if not isinstance(before, int) or not isinstance(after, int):
        raise PlanningStoreError("store.metadata", "receipt revisions must be integers")
    return StoreReceipt(
        interface=cast(str, values[0]),
        store_interface=cast(str, values[1]),
        idempotency_key=cast(str, values[2]),
        request_hash=cast(str, values[3]),
        before_revision=before,
        after_revision=after,
        touched_finding_ids=tuple(touched_ids),
    )


def _require_exact_fields(value: Mapping[str, object], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise PlanningStoreError(
            "store.metadata",
            f"{label} fields must be {sorted(expected)!r}; got {sorted(actual)!r}",
        )


def _metadata_object(metadata: _StoreMetadata) -> JsonObject:
    return {
        "interface": metadata.interface,
        "store_revision": metadata.store_revision,
        "replay_records": [
            {
                "idempotency_key": record.idempotency_key,
                "request_hash": record.request_hash,
                "receipt": {
                    "interface": record.receipt.interface,
                    "store_interface": record.receipt.store_interface,
                    "idempotency_key": record.receipt.idempotency_key,
                    "request_hash": record.receipt.request_hash,
                    "before_revision": record.receipt.before_revision,
                    "after_revision": record.receipt.after_revision,
                    "touched_finding_ids": list(record.receipt.touched_finding_ids),
                },
            }
            for record in metadata.replay_records
        ],
    }


def _replace_canonical_section(text: str, rendered_section: str) -> str:
    lines = text.splitlines()
    headings = _top_level_h2_indices(lines)
    matches = [index for index in headings if lines[index].strip() == _OPERATIONAL_HEADING]
    if len(matches) != 1:
        raise PlanningStoreError("current.contract_count", "expected one operational section")
    start = matches[0]
    end = next((index for index in headings if index > start), len(lines))
    replacement = rendered_section.rstrip("\n").splitlines()
    updated = [*lines[:start], *replacement, *lines[end:]]
    return "\n".join(updated).rstrip() + "\n"


def _replace_or_append_store_metadata(text: str, metadata: _StoreMetadata) -> str:
    lines = text.splitlines()
    blocks = _top_level_yaml_blocks(lines)
    matching: list[_YamlBlock] = []
    for block in blocks:
        parsed = _parse_secondary_yaml(block.source)
        if parsed.mapping is not None and parsed.mapping.get("interface") == metadata.interface:
            matching.append(block)
    body = yaml.safe_dump(_metadata_object(metadata), sort_keys=False, allow_unicode=True).rstrip()
    if not matching:
        return text.rstrip() + f"\n\n## Store Metadata\n\n```yaml\n{body}\n```\n"
    if len(matching) != 1:
        raise PlanningStoreError("store.metadata_count", "multiple store metadata blocks")
    block = matching[0]
    updated = [*lines[: block.fence_start + 1], *body.splitlines(), *lines[block.fence_end :]]
    return "\n".join(updated).rstrip() + "\n"


def _atomic_replace_and_validate(
    path: Path,
    rendered: str,
    *,
    fault: FaultPoint | None,
    validate: Any,
) -> None:
    original = path.read_bytes() if path.exists() else None
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(rendered.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        if fault == "before_replace":
            raise InjectedStoreFailure("before_replace")
        os.replace(temporary, path)
        if fault == "after_replace_before_validation":
            raise InjectedStoreFailure("after_replace_before_validation")
        try:
            validate()
        except Exception:
            if original is None:
                path.unlink(missing_ok=True)
            else:
                _replace_bytes(path, original)
            raise
        if fault == "after_replace_before_return":
            raise InjectedStoreFailure("after_replace_before_return")
    finally:
        temporary.unlink(missing_ok=True)


def _replace_bytes(path: Path, content: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.rollback.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _apply_artifact_document(
    path: Path,
    *,
    toolchain_root: str | Path,
    expected_revision: int,
    expected_file_hash: str,
    contract: Mapping[str, object],
    expected_schema: str,
    expected_producer_identity: ProducerIdentity,
    lineage_binding: Mapping[str, object],
    validate_payload: Callable[[Mapping[str, object]], None],
    idempotency_key: str,
    fault: FaultPoint | None,
) -> StoreApplyResult:
    key = _require_idempotency_key(idempotency_key)
    artifact = _json_object_copy(contract, "contract")
    if artifact.get("schema") != expected_schema:
        raise PlanningStoreError(
            "artifact.schema",
            f"expected {expected_schema!r}; got {artifact.get('schema')!r}",
        )
    try:
        rendered_section = render_planning_contract(
            artifact,
            toolchain_root=toolchain_root,
            expected_producer_identity=expected_producer_identity,
        )
    except ValueError as error:
        raise PlanningStoreError("artifact.invalid", str(error)) from error
    validate_payload(artifact)
    original_text = path.read_text(encoding="utf-8") if path.is_file() else ""
    metadata = _parse_store_metadata(
        path,
        original_text,
        interface=_ARTIFACT_STORE_INTERFACE,
        default_revision=0,
    )
    request_hash = _canonical_request_hash(
        {
            "operation": "write_planning_artifact",
            "expected_schema": expected_schema,
            "expected_revision": expected_revision,
            "expected_file_hash": expected_file_hash,
            "contract": artifact,
            "lineage": dict(lineage_binding),
            "idempotency_key": key,
        }
    )
    replay = _evaluate_replay(
        metadata,
        key=key,
        request_hash=request_hash,
        store_interface=_ARTIFACT_STORE_INTERFACE,
        before_revision=expected_revision,
        after_revision=expected_revision + 1,
        touched_finding_ids=(),
    )
    if replay is not None:
        persisted = read_artifact_document(
            path,
            toolchain_root=toolchain_root,
            expected_schema=expected_schema,
            expected_producer_identity=expected_producer_identity,
        )
        if persisted.logical_revision != replay.after_revision:
            raise PlanningStoreError(
                "artifact.replay_artifact_mismatch",
                "persisted artifact revision does not match exact replay evidence",
            )
        if _thaw_json(persisted.contract) != artifact:
            raise PlanningStoreError(
                "artifact.replay_artifact_mismatch",
                "persisted artifact payload does not match exact caller replay",
            )
        expected_persisted_text = _replace_or_append_store_metadata(
            rendered_section,
            metadata,
        )
        if path.read_bytes() != expected_persisted_text.encode("utf-8"):
            raise PlanningStoreError(
                "artifact.replay_artifact_mismatch",
                "persisted artifact bytes do not match the canonical write result",
            )
        validate_payload(persisted.contract)
        return StoreApplyResult(outcome="exact_replay", receipt=replay)
    _validate_cas(
        actual_revision=metadata.store_revision,
        actual_file_hash=_file_hash(path) if path.is_file() else _EMPTY_FILE_HASH,
        expected_revision=expected_revision,
        expected_file_hash=expected_file_hash,
    )
    if metadata.store_revision != 0:
        raise PlanningStoreError(
            "artifact.immutable",
            "accepted artifact lineage cannot be replaced",
        )
    after_revision = expected_revision + 1
    receipt = StoreReceipt(
        interface=_STORE_RECEIPT_INTERFACE,
        store_interface=_ARTIFACT_STORE_INTERFACE,
        idempotency_key=key,
        request_hash=request_hash,
        before_revision=expected_revision,
        after_revision=after_revision,
        touched_finding_ids=(),
    )
    updated_metadata = _with_replay_record(
        metadata,
        store_revision=after_revision,
        receipt=receipt,
    )
    rendered = _replace_or_append_store_metadata(rendered_section, updated_metadata)

    def validate_written() -> None:
        snapshot = read_artifact_document(
            path,
            toolchain_root=toolchain_root,
            expected_schema=expected_schema,
            expected_producer_identity=expected_producer_identity,
        )
        if snapshot.logical_revision != after_revision:
            raise PlanningStoreError(
                "artifact.revision",
                "reread artifact revision does not match persisted result",
            )
        validate_payload(snapshot.contract)

    _atomic_replace_and_validate(
        path,
        rendered,
        fault=fault,
        validate=validate_written,
    )
    return StoreApplyResult(outcome="applied", receipt=receipt)


def _validate_lineage_paths(lineage: ArtifactLineage) -> None:
    planning_root = lineage.planning_root.resolve()
    canonical_root = lineage.canonical_planning_repository_root.resolve()
    if not planning_root.is_relative_to(canonical_root):
        raise PlanningStoreError(
            "artifact.planning_root",
            "planning root must be contained by the canonical planning repository",
        )
    for label, raw_path in (
        ("ledger", lineage.ledger_path),
        ("dispatch", lineage.dispatch_path),
        ("runway", lineage.runway_path),
        ("closeout", lineage.closeout_path),
    ):
        if not raw_path.resolve().is_relative_to(planning_root):
            raise PlanningStoreError(
                "artifact.path_escape",
                f"{label} path escapes the explicit planning root",
            )
    identities = (
        (lineage.dispatch_producer, "planning-dispatch/v1"),
        (lineage.runway_producer, "planning-runway/v1"),
        (lineage.closeout_producer, "planning-closeout/v1"),
    )
    for identity, expected_schema in identities:
        if identity.schema_version != expected_schema:
            raise PlanningStoreError(
                "artifact.producer",
                f"producer schema must be {expected_schema!r}",
            )
    producer_lineage = (
        lineage.dispatch_producer,
        lineage.runway_producer,
        lineage.closeout_producer,
    )
    for field in ("toolchain_generation", "toolchain_commit"):
        values = {getattr(identity, field) for identity in producer_lineage}
        if len(values) != 1:
            raise PlanningStoreError(
                "artifact.producer_lineage",
                f"dispatch, runway, and closeout producer {field} must match",
            )
    for label, value in (
        ("ledger_revision", lineage.ledger_revision),
        ("dispatch_revision", lineage.dispatch_revision),
    ):
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise PlanningStoreError("artifact.revision", f"{label} must be sha256")
    finding_ids = (*lineage.included_finding_ids, *lineage.deferred_finding_ids)
    if len(finding_ids) != len(set(finding_ids)):
        raise PlanningStoreError(
            "artifact.finding_ids",
            "included and deferred finding IDs must be disjoint and unique",
        )


def _require_lineage_target(path: str | Path, expected: Path) -> Path:
    actual = Path(path)
    if actual.resolve() != expected.resolve():
        raise PlanningStoreError(
            "artifact.path",
            f"artifact path {actual} does not match expected lineage path {expected}",
        )
    return actual


def _resolve_artifact_reference(value: object, planning_root: Path) -> Path:
    if not isinstance(value, str):
        raise PlanningStoreError("artifact.path", "artifact reference must be a string")
    path = Path(value)
    return path.resolve() if path.is_absolute() else (planning_root / path).resolve()


def _expect_artifact_fact(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise PlanningStoreError(
            "artifact.lineage",
            f"{label} expected {expected!r}; got {actual!r}",
        )


def _nested_mapping(value: Mapping[str, object], key: str) -> Mapping[str, object]:
    child = value.get(key)
    if not isinstance(child, Mapping):
        raise PlanningStoreError("artifact.invalid", f"{key} must be an object")
    return cast(Mapping[str, object], child)


def _validate_dispatch_lineage(
    contract: Mapping[str, object],
    lineage: ArtifactLineage,
) -> None:
    artifact = _nested_mapping(contract, "artifact")
    source = _nested_mapping(contract, "source")
    scope = _nested_mapping(contract, "scope")
    runway = _nested_mapping(contract, "runway")
    execution = _nested_mapping(contract, "execution_context")
    expected_finding_ids = tuple(
        sorted((*lineage.included_finding_ids, *lineage.deferred_finding_ids))
    )
    _expect_artifact_fact("dispatch batch", artifact.get("id"), lineage.batch_id)
    _expect_artifact_fact("dispatch program", artifact.get("program"), lineage.program)
    _expect_artifact_fact(
        "dispatch revision",
        artifact.get("revision"),
        lineage.dispatch_revision,
    )
    _expect_artifact_fact(
        "dispatch ledger path",
        _resolve_artifact_reference(source.get("ledger_path"), lineage.planning_root),
        lineage.ledger_path.resolve(),
    )
    _expect_artifact_fact(
        "dispatch ledger revision",
        source.get("ledger_revision"),
        lineage.ledger_revision,
    )
    _expect_artifact_fact(
        "dispatch finding IDs",
        tuple(sorted(cast(Sequence[str], source.get("finding_ids")))),
        expected_finding_ids,
    )
    _expect_artifact_fact(
        "dispatch included findings",
        tuple(cast(Sequence[str], scope.get("included_finding_ids"))),
        lineage.included_finding_ids,
    )
    _expect_artifact_fact(
        "dispatch deferred findings",
        tuple(cast(Sequence[str], scope.get("deferred_finding_ids"))),
        lineage.deferred_finding_ids,
    )
    _expect_artifact_fact("dispatch batch kind", scope.get("batch_kind"), lineage.batch_kind)
    _expect_artifact_fact(
        "dispatch runway path",
        _resolve_artifact_reference(runway.get("expected_path"), lineage.planning_root),
        lineage.runway_path.resolve(),
    )
    _expect_artifact_fact(
        "dispatch toolchain root",
        execution.get("toolchain_source_root"),
        str(lineage.toolchain_source_root),
    )
    _expect_artifact_fact(
        "dispatch canonical planning repository root",
        execution.get("canonical_planning_repository_root"),
        str(lineage.canonical_planning_repository_root),
    )
    _expect_artifact_fact(
        "dispatch implementation root",
        execution.get("implementation_target_root"),
        str(lineage.implementation_target_root),
    )


def _validate_runway_lineage(
    contract: Mapping[str, object],
    lineage: ArtifactLineage,
) -> None:
    artifact = _nested_mapping(contract, "artifact")
    batch = _nested_mapping(contract, "batch")
    execution = _nested_mapping(contract, "execution")
    _expect_artifact_fact("runway batch", artifact.get("id"), lineage.batch_id)
    _expect_artifact_fact(
        "runway dispatch path",
        _resolve_artifact_reference(artifact.get("source_dispatch"), lineage.planning_root),
        lineage.dispatch_path.resolve(),
    )
    _expect_artifact_fact(
        "runway dispatch revision",
        artifact.get("source_dispatch_revision"),
        lineage.dispatch_revision,
    )
    _expect_artifact_fact("runway batch kind", batch.get("kind"), lineage.batch_kind)
    _expect_artifact_fact("runway state", batch.get("status"), "queued")
    _expect_artifact_fact(
        "runway implementation root",
        execution.get("implementation_target_root"),
        str(lineage.implementation_target_root),
    )


def _validate_closeout_lineage(
    contract: Mapping[str, object],
    lineage: ArtifactLineage,
) -> None:
    artifact = _nested_mapping(contract, "artifact")
    reconciliation = _nested_mapping(contract, "reconciliation")
    execution = _nested_mapping(contract, "execution_context")
    _expect_artifact_fact("closeout batch", artifact.get("batch_id"), lineage.batch_id)
    for field in (
        "selected_dispatch_after",
        "queued_runway_after",
        "active_runway_after",
    ):
        _expect_artifact_fact(f"closeout {field}", reconciliation.get(field), None)
    _expect_artifact_fact(
        "closeout successor selection",
        reconciliation.get("successor_selected"),
        False,
    )
    _expect_artifact_fact(
        "closeout canonical planning repository root",
        execution.get("canonical_planning_repository_root"),
        str(lineage.canonical_planning_repository_root),
    )
    _expect_artifact_fact(
        "closeout implementation root",
        execution.get("implementation_target_root"),
        str(lineage.implementation_target_root),
    )


def _validate_dispatch_predecessor(
    lineage: ArtifactLineage,
    *,
    toolchain_root: str | Path,
    expected_file_hash: str,
) -> ArtifactSnapshot:
    snapshot = read_artifact_document(
        lineage.dispatch_path,
        toolchain_root=toolchain_root,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=lineage.dispatch_producer,
    )
    if snapshot.logical_revision != 1:
        raise PlanningStoreError(
            "artifact.predecessor_revision",
            "dispatch predecessor must be accepted revision 1",
        )
    if snapshot.file_hash != expected_file_hash:
        raise PlanningStoreError(
            "artifact.predecessor_hash",
            "dispatch predecessor hash does not match caller expectation",
        )
    _validate_dispatch_lineage(snapshot.contract, lineage)
    return snapshot


def _validate_runway_predecessor(
    lineage: ArtifactLineage,
    *,
    toolchain_root: str | Path,
    expected_file_hash: str,
) -> ArtifactSnapshot:
    snapshot = read_artifact_document(
        lineage.runway_path,
        toolchain_root=toolchain_root,
        expected_schema="planning-runway/v1",
        expected_producer_identity=lineage.runway_producer,
    )
    if snapshot.logical_revision != 1:
        raise PlanningStoreError(
            "artifact.predecessor_revision",
            "runway predecessor must be accepted revision 1",
        )
    if snapshot.file_hash != expected_file_hash:
        raise PlanningStoreError(
            "artifact.predecessor_hash",
            "runway predecessor hash does not match caller expectation",
        )
    _validate_runway_lineage(snapshot.contract, lineage)
    return snapshot


def _producer_binding(identity: ProducerIdentity) -> JsonObject:
    return {
        "toolchain_generation": identity.toolchain_generation,
        "toolchain_commit": identity.toolchain_commit,
        "schema_version": identity.schema_version,
    }


def _dispatch_lineage_binding(lineage: ArtifactLineage) -> JsonObject:
    return {
        "planning_root": str(lineage.planning_root),
        "program": lineage.program,
        "batch_id": lineage.batch_id,
        "included_finding_ids": list(lineage.included_finding_ids),
        "deferred_finding_ids": list(lineage.deferred_finding_ids),
        "batch_kind": lineage.batch_kind,
        "ledger_path": str(lineage.ledger_path),
        "ledger_revision": lineage.ledger_revision,
        "dispatch_path": str(lineage.dispatch_path),
        "dispatch_revision": lineage.dispatch_revision,
        "runway_path": str(lineage.runway_path),
        "toolchain_source_root": str(lineage.toolchain_source_root),
        "canonical_planning_repository_root": str(
            lineage.canonical_planning_repository_root
        ),
        "implementation_target_root": str(lineage.implementation_target_root),
        "producer": _producer_binding(lineage.dispatch_producer),
    }


def _runway_lineage_binding(lineage: ArtifactLineage) -> JsonObject:
    return {
        "planning_root": str(lineage.planning_root),
        "batch_id": lineage.batch_id,
        "batch_kind": lineage.batch_kind,
        "dispatch_path": str(lineage.dispatch_path),
        "dispatch_revision": lineage.dispatch_revision,
        "runway_path": str(lineage.runway_path),
        "implementation_target_root": str(lineage.implementation_target_root),
        "dispatch_producer": _producer_binding(lineage.dispatch_producer),
        "producer": _producer_binding(lineage.runway_producer),
    }


def _closeout_lineage_binding(lineage: ArtifactLineage) -> JsonObject:
    return {
        "planning_root": str(lineage.planning_root),
        "batch_id": lineage.batch_id,
        "dispatch_path": str(lineage.dispatch_path),
        "dispatch_revision": lineage.dispatch_revision,
        "runway_path": str(lineage.runway_path),
        "closeout_path": str(lineage.closeout_path),
        "canonical_planning_repository_root": str(
            lineage.canonical_planning_repository_root
        ),
        "implementation_target_root": str(lineage.implementation_target_root),
        "dispatch_producer": _producer_binding(lineage.dispatch_producer),
        "runway_producer": _producer_binding(lineage.runway_producer),
        "producer": _producer_binding(lineage.closeout_producer),
    }


def _parse_per_finding_ledger(
    path: Path,
    text: str,
    *,
    toolchain_root: Path,
) -> tuple[dict[str, JsonObject], _StoreMetadata]:
    metadata = _parse_store_metadata(
        path,
        text,
        interface=_LEDGER_STORE_INTERFACE,
        default_revision=0,
    )
    findings: dict[str, JsonObject] = {}
    derived_candidates: list[JsonObject] = []
    for block in _top_level_yaml_blocks(text.splitlines()):
        inspection = _inspect_secondary_yaml(block.source)
        parsed = _parse_secondary_yaml(block.source)
        if parsed.error is not None:
            if inspection.schema_value == "planning-finding/v1":
                raise PlanningStoreError(
                    "ledger.invalid_finding_yaml",
                    f"line {block.fence_start + 1}: {parsed.error}",
                )
            continue
        value = parsed.mapping
        if value is None:
            continue
        if value.get("interface") == _DERIVED_INDEX_INTERFACE:
            derived_candidates.append(value)
            continue
        if value.get("schema") != "planning-finding/v1":
            continue
        finding_id = value.get("id")
        if not isinstance(finding_id, str):
            raise PlanningStoreError("ledger.finding_id", "finding id must be a string")
        try:
            _validate_contract_object(value, "planning-finding/v1", toolchain_root)
        except PlanningStoreError as error:
            raise PlanningStoreError(
                error.code,
                f"finding {finding_id} at line {block.fence_start + 1}: {error}",
            ) from error
        if finding_id in findings:
            raise PlanningStoreError("ledger.duplicate_id", f"duplicate finding {finding_id!r}")
        findings[finding_id] = value
    if len(derived_candidates) != 1:
        raise PlanningStoreError(
            "ledger.derived_index_count",
            f"expected one derived index; found {len(derived_candidates)}",
        )
    _validate_dependency_references(findings)
    _validate_derived_index(path, derived_candidates[0], findings, metadata.store_revision)
    return dict(sorted(findings.items())), metadata


def _validate_contract_object(
    value: JsonObject,
    schema_name: str,
    toolchain_root: Path,
) -> None:
    diagnostics: list[Diagnostic] = []
    validators, _ = _load_validators(toolchain_root, diagnostics)
    if diagnostics:
        raise PlanningStoreError("schema.not_available", str(diagnostics[0]))
    errors = sorted(
        validators[schema_name].iter_errors(cast(Any, value)),  # pyright: ignore[reportUnknownMemberType]
        key=lambda error: error.json_path,
    )
    if errors:
        raise PlanningStoreError(
            f"schema.{errors[0].validator}",
            f"{errors[0].json_path}: {errors[0].message}",
        )


def _validate_dependency_references(findings: Mapping[str, JsonObject]) -> None:
    known = set(findings)
    for finding_id, finding in findings.items():
        dependencies = finding.get("dependencies")
        if not isinstance(dependencies, list):
            raise PlanningStoreError("ledger.dependencies", f"{finding_id} dependencies invalid")
        missing = sorted(
            dependency
            for dependency in dependencies
            if isinstance(dependency, str) and dependency not in known
        )
        if missing:
            raise PlanningStoreError(
                "ledger.dependency_reference",
                f"{finding_id} references missing dependencies {missing!r}",
            )


def _derived_entries(findings: Mapping[str, Mapping[str, object]]) -> list[JsonValue]:
    entries: list[JsonValue] = []
    for finding_id in sorted(findings):
        finding = findings[finding_id]
        lifecycle = finding.get("lifecycle")
        status = (
            cast(Mapping[str, object], lifecycle).get("status")
            if isinstance(lifecycle, Mapping)
            else None
        )
        entries.append(
            {
                "id": finding_id,
                "revision": cast(JsonValue, finding.get("revision")),
                "title": cast(JsonValue, finding.get("title")),
                "status": cast(JsonValue, status),
            }
        )
    return entries


def _validate_derived_index(
    path: Path,
    value: JsonObject,
    findings: Mapping[str, JsonObject],
    source_revision: int,
) -> None:
    _require_exact_fields(
        value,
        {"interface", "source_artifact", "source_revision", "findings"},
        "derived index",
    )
    if value.get("source_artifact") != path.name:
        raise PlanningStoreError(
            "ledger.derived_source",
            f"derived index source_artifact must be {path.name!r}",
        )
    if value.get("source_revision") != source_revision:
        raise PlanningStoreError(
            "ledger.derived_revision",
            "derived index source_revision does not match ledger revision",
        )
    if value.get("findings") != _derived_entries(findings):
        raise PlanningStoreError(
            "ledger.derived_index_mismatch",
            "derived index does not equal structured finding blocks",
        )


def _apply_finding_mutations(
    findings: Mapping[str, JsonObject],
    *,
    mutations: Sequence[JsonObject],
    touched_finding_revisions: Mapping[str, int | None],
    toolchain_root: Path,
) -> tuple[dict[str, JsonObject], tuple[str, ...]]:
    requested_touched_ids = _requested_touched_finding_ids(
        mutations,
        touched_finding_revisions=touched_finding_revisions,
    )
    mutation_by_id: dict[str, JsonObject] = {}
    for mutation in mutations:
        _validate_contract_object(mutation, "planning-finding/v1", toolchain_root)
        finding_id = cast(str, mutation.get("id"))
        mutation_by_id[finding_id] = mutation
    resulting = {key: _json_object_copy(value, key) for key, value in findings.items()}
    for finding_id, mutation in mutation_by_id.items():
        expected = touched_finding_revisions[finding_id]
        existing = findings.get(finding_id)
        new_revision = mutation.get("revision")
        if existing is None:
            if expected is not None or new_revision != 1:
                raise PlanningStoreError(
                    "ledger.finding_revision_mismatch",
                    f"new finding {finding_id!r} requires expected null and revision 1",
                )
        else:
            actual = existing.get("revision")
            if actual != expected:
                raise PlanningStoreError(
                    "ledger.finding_revision_mismatch",
                    f"{finding_id!r} expected revision {expected}; got {actual}",
                )
            if not isinstance(expected, int) or new_revision != expected + 1:
                raise PlanningStoreError(
                    "ledger.finding_revision_step",
                    f"{finding_id!r} replacement must increment revision once",
                )
        resulting[finding_id] = mutation
    _validate_dependency_references(resulting)
    return dict(sorted(resulting.items())), requested_touched_ids


def _requested_touched_finding_ids(
    mutations: Sequence[JsonObject],
    *,
    touched_finding_revisions: Mapping[str, int | None],
) -> tuple[str, ...]:
    finding_ids: list[str] = []
    for mutation in mutations:
        finding_id = mutation.get("id")
        if not isinstance(finding_id, str):
            raise PlanningStoreError("ledger.finding_id", "mutation id must be a string")
        if finding_id in finding_ids:
            raise PlanningStoreError(
                "ledger.duplicate_mutation",
                f"duplicate mutation {finding_id!r}",
            )
        finding_ids.append(finding_id)
    if set(finding_ids) != set(touched_finding_revisions):
        raise PlanningStoreError(
            "ledger.touched_set",
            "touched_finding_revisions must exactly name mutation ids",
        )
    return tuple(sorted(finding_ids))


def _render_contract_yaml(
    contract: Mapping[str, object],
    *,
    toolchain_root: Path,
) -> str:
    schema_name = contract.get("schema")
    if not isinstance(schema_name, str):
        raise PlanningStoreError("schema.missing", "contract schema missing")
    diagnostics: list[Diagnostic] = []
    _, schemas = _load_validators(toolchain_root, diagnostics)
    if diagnostics:
        raise PlanningStoreError("schema.not_available", str(diagnostics[0]))
    schema = schemas[schema_name]
    ordered = _order_by_schema(contract, schema, schema)
    return yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True).rstrip()


def _render_per_finding_ledger(
    path: Path,
    findings: Mapping[str, JsonObject],
    metadata: _StoreMetadata,
    *,
    toolchain_root: Path,
) -> str:
    derived: JsonObject = {
        "interface": _DERIVED_INDEX_INTERFACE,
        "source_artifact": path.name,
        "source_revision": metadata.store_revision,
        "findings": _derived_entries(findings),
    }
    sections = [
        "# Planning Ledger",
        "",
        "## Store Metadata",
        "",
        "```yaml",
        yaml.safe_dump(_metadata_object(metadata), sort_keys=False).rstrip(),
        "```",
        "",
        "## Derived Index",
        "",
        "```yaml",
        yaml.safe_dump(derived, sort_keys=False).rstrip(),
        "```",
    ]
    for finding_id, finding in sorted(findings.items()):
        sections.extend(
            [
                "",
                f"## Finding {finding_id}",
                "",
                "```yaml",
                _render_contract_yaml(finding, toolchain_root=toolchain_root),
                "```",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def _single_markdown_path(path: Path) -> Path:
    if path.is_file():
        return path
    canonical = path / "LEDGER.md"
    if canonical.is_file():
        return canonical
    matches = sorted(path.rglob("*.md"))
    if len(matches) != 1:
        raise PlanningStoreError(
            "ledger.catalog",
            f"expected one Markdown ledger below {path}; found {len(matches)}",
        )
    return matches[0]


def _parse_global_ledger(
    path: Path,
    *,
    toolchain_root: Path,
    expected_source_artifact: str,
) -> tuple[dict[str, JsonObject], int]:
    candidates: list[JsonObject] = []
    for block in _top_level_yaml_blocks(path.read_text(encoding="utf-8").splitlines()):
        parsed = _parse_secondary_yaml(block.source)
        if parsed.mapping is not None and parsed.mapping.get("interface") == _GLOBAL_LEDGER_INTERFACE:
            candidates.append(parsed.mapping)
    if len(candidates) != 1:
        raise PlanningStoreError("ledger.global_count", "expected one global comparison block")
    value = candidates[0]
    _require_exact_fields(
        value,
        {"interface", "source_artifact", "source_revision", "findings"},
        "global ledger",
    )
    revision = value.get("source_revision")
    raw_findings = value.get("findings")
    if value.get("source_artifact") != expected_source_artifact:
        raise PlanningStoreError(
            "ledger.global_source",
            f"global source_artifact must be {expected_source_artifact!r}",
        )
    if not isinstance(revision, int) or not isinstance(raw_findings, list):
        raise PlanningStoreError("ledger.global", "global revision/findings invalid")
    findings: dict[str, JsonObject] = {}
    for index, raw in enumerate(raw_findings):
        if not isinstance(raw, dict):
            raise PlanningStoreError("ledger.global", "global finding must be an object")
        finding = cast(JsonObject, raw)
        finding_id = finding.get("id")
        if not isinstance(finding_id, str):
            raise PlanningStoreError(
                "ledger.finding_id",
                f"global finding index {index} has no string id",
            )
        try:
            _validate_contract_object(finding, "planning-finding/v1", toolchain_root)
        except PlanningStoreError as error:
            raise PlanningStoreError(
                error.code,
                f"global finding index {index} id {finding_id}: {error}",
            ) from error
        if finding_id in findings:
            raise PlanningStoreError("ledger.duplicate_id", f"duplicate global id {finding_id!r}")
        findings[finding_id] = finding
    _validate_dependency_references(findings)
    return dict(sorted(findings.items())), revision


def _semantic_findings(
    findings: Mapping[str, Mapping[str, object]],
) -> JsonObject:
    return {
        finding_id: cast(JsonValue, _thaw_json(finding))
        for finding_id, finding in sorted(findings.items())
    }


def _required_variant(base: Path, name: str) -> Path:
    path = base.parent / name
    if not path.is_file():
        raise PlanningStoreError(
            "ledger.comparison_fixture",
            f"missing controlled comparison fixture {path}",
        )
    return path


def _capture_store_error(action: Any) -> PlanningStoreError | None:
    try:
        action()
    except PlanningStoreError as error:
        return error
    return None


def _changed_top_level_sections(before: Path, after: Path) -> tuple[str, ...]:
    before_sections = _top_level_sections(before.read_text(encoding="utf-8"))
    after_sections = _top_level_sections(after.read_text(encoding="utf-8"))
    names = set(before_sections) | set(after_sections)
    return tuple(
        sorted(
            name
            for name in names
            if before_sections.get(name) != after_sections.get(name)
        )
    )


def _top_level_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    headings = _top_level_h2_indices(lines)
    sections: dict[str, str] = {}
    for offset, start in enumerate(headings):
        end = headings[offset + 1] if offset + 1 < len(headings) else len(lines)
        name = lines[start].removeprefix("##").strip()
        sections[name] = "\n".join(lines[start:end]).strip()
    return sections


def _validate_selection_request(
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
) -> None:
    if not request.transaction_id.strip():
        raise PlanningStoreError(
            "transaction.id",
            "transaction_id cannot be empty",
        )
    if not request.command_owner_version.strip():
        raise PlanningStoreError(
            "transaction.command_version",
            "command_owner_version cannot be empty",
        )
    if not re.fullmatch(r"[0-9a-f]{64}", request.expected_initial_state_file_hash):
        raise PlanningStoreError(
            "transaction.state_hash",
            "expected initial state file hash must be sha256",
        )
    _validate_lineage_paths(request.lineage)
    planning_root = request.lineage.planning_root.resolve()
    for label, path in (
        ("transaction", request.transaction_path),
        ("current", request.current_path),
    ):
        if not path.resolve().is_relative_to(planning_root):
            raise PlanningStoreError(
                "transaction.path_escape",
                f"{label} path escapes the explicit planning root",
            )
    if (
        request.producer.schema_version != _TRANSACTION_SCHEMA
        or request.producer.toolchain_generation
        != request.lineage.dispatch_producer.toolchain_generation
        or request.producer.toolchain_commit
        != request.lineage.dispatch_producer.toolchain_commit
    ):
        raise PlanningStoreError(
            "transaction.producer",
            "transaction producer must match the accepted artifact lineage",
        )
    initial_current = _json_object_copy(
        request.initial_current_contract,
        "initial_current_contract",
    )
    if initial_current.get("schema") != "planning-current/v1":
        raise PlanningStoreError(
            "transaction.current_schema",
            "initial current contract must use planning-current/v1",
        )
    try:
        render_planning_contract(initial_current, toolchain_root=toolchain_root)
        render_planning_contract(
            request.dispatch_contract,
            toolchain_root=toolchain_root,
            expected_producer_identity=request.lineage.dispatch_producer,
        )
        render_planning_contract(
            request.runway_contract,
            toolchain_root=toolchain_root,
            expected_producer_identity=request.lineage.runway_producer,
        )
    except ValueError as error:
        raise PlanningStoreError("transaction.invalid_input", str(error)) from error
    _validate_dispatch_lineage(request.dispatch_contract, request.lineage)
    _validate_runway_lineage(request.runway_contract, request.lineage)
    _expect_artifact_fact(
        "transaction current program",
        initial_current.get("program"),
        request.lineage.program,
    )
    _expect_artifact_fact(
        "transaction initial state revision",
        initial_current.get("revision"),
        request.expected_initial_state_revision,
    )
    _expect_artifact_fact(
        "transaction current ledger",
        _resolve_artifact_reference(
            initial_current.get("ledger"),
            request.lineage.planning_root,
        ),
        request.lineage.ledger_path.resolve(),
    )


def _validate_initial_current(
    request: SelectionTransactionRequest,
    snapshot: CurrentSnapshot,
) -> None:
    if snapshot.logical_revision != request.expected_initial_state_revision:
        raise PlanningStoreError(
            "transaction.initial_state_revision",
            "current revision does not match exact initial intent",
        )
    if snapshot.file_hash != request.expected_initial_state_file_hash:
        raise PlanningStoreError(
            "transaction.initial_state_hash",
            "current file hash does not match exact initial intent",
        )
    if _thaw_json(snapshot.contract) != _json_object_copy(
        request.initial_current_contract,
        "initial_current_contract",
    ):
        raise PlanningStoreError(
            "transaction.initial_state_payload",
            "current payload does not match exact initial intent",
        )
    _require_current_state(snapshot.contract, expected="idle", request=request)


def _initial_transaction_record(request: SelectionTransactionRequest) -> JsonObject:
    state_payload_json = _canonical_json_text(request.initial_current_contract)
    dispatch_payload_json = _canonical_json_text(request.dispatch_contract)
    finding_ids = sorted(
        (
            *request.lineage.included_finding_ids,
            *request.lineage.deferred_finding_ids,
        )
    )
    return cast(JsonObject, {
        "schema": _TRANSACTION_SCHEMA,
        "transaction_id": request.transaction_id,
        "program": request.lineage.program,
        "finding_ids": finding_ids,
        "batch_id": request.lineage.batch_id,
        "initial_intent": {
            "ledger_path": str(request.lineage.ledger_path),
            "ledger_revision": request.lineage.ledger_revision,
            "state_path": str(request.current_path),
            "state_revision": request.expected_initial_state_revision,
            "state_file_hash": request.expected_initial_state_file_hash,
            "state_payload_json": state_payload_json,
            "state_payload_hash": _hash_text(state_payload_json),
            "expected_state": "idle",
            "dispatch_path": str(request.lineage.dispatch_path),
            "dispatch_payload_json": dispatch_payload_json,
            "dispatch_payload_hash": _hash_text(dispatch_payload_json),
            "runway_path": str(request.lineage.runway_path),
            "command_owner_version": request.command_owner_version,
            "schema_versions": {
                "current": "planning-current/v1",
                "dispatch": "planning-dispatch/v1",
                "runway": "planning-runway/v1",
                "transaction": _TRANSACTION_SCHEMA,
            },
            "stage_plan": list(_SELECTION_STAGE_PLAN),
        },
        "extensions": [],
        "producer": _producer_binding(request.producer),
    })


def _validate_transaction_binding(
    record: Mapping[str, object],
    request: SelectionTransactionRequest,
) -> None:
    expected = _initial_transaction_record(request)
    for field in (
        "schema",
        "transaction_id",
        "program",
        "finding_ids",
        "batch_id",
        "initial_intent",
        "producer",
    ):
        if _thaw_json(record.get(field)) != expected[field]:
            raise PlanningStoreError(
                "transaction.reused_id_mismatch",
                f"transaction {request.transaction_id!r} changed immutable field {field}",
            )
    _validate_transaction_extension_order(record)
    runway_input = _transaction_extension(record, "runway_input")
    if runway_input is not None:
        runway_payload_json = _canonical_json_text(request.runway_contract)
        if (
            runway_input.get("runway_payload_json") != runway_payload_json
            or runway_input.get("runway_payload_hash")
            != _hash_text(runway_payload_json)
        ):
            raise PlanningStoreError(
                "transaction.reused_id_mismatch",
                "transaction runway payload changed after it was bound",
            )


def _read_transaction_record(
    path: Path,
    *,
    toolchain_root: str | Path,
    expected_producer: ProducerIdentity,
) -> JsonObject:
    result = validate_planning_contracts(
        [path],
        toolchain_root=toolchain_root,
        expected_producer_identity=expected_producer,
    )
    if not result.is_valid:
        raise PlanningStoreError("transaction.invalid", str(result.diagnostics[0]))
    if len(result.contracts) != 1:
        raise PlanningStoreError(
            "transaction.contract_count",
            "expected one transaction contract",
        )
    contract = result.contracts[0].contract
    if contract.get("schema") != _TRANSACTION_SCHEMA:
        raise PlanningStoreError(
            "transaction.schema",
            f"expected {_TRANSACTION_SCHEMA!r}",
        )
    record = _json_object_copy(contract, "transaction record")
    _validate_transaction_extension_order(record)
    return record


def _persist_transaction_record(
    path: Path,
    record: JsonObject,
    *,
    toolchain_root: str | Path,
    expected_file_hash: str,
    expected_producer: ProducerIdentity,
) -> None:
    actual_file_hash = _file_hash(path) if path.is_file() else _EMPTY_FILE_HASH
    if actual_file_hash != expected_file_hash:
        raise PlanningStoreError(
            "transaction.file_hash_mismatch",
            "transaction record moved before append",
        )
    extensions = _transaction_extensions(record)
    if path.is_file() and path.stat().st_size > 0:
        existing = _read_transaction_record(
            path,
            toolchain_root=toolchain_root,
            expected_producer=expected_producer,
        )
        expected_prior = _json_object_copy(record, "transaction record")
        expected_prior["extensions"] = [
            _json_object_copy(item, "transaction extension")
            for item in extensions[:-1]
        ]
        if existing != expected_prior:
            raise PlanningStoreError(
                "transaction.concurrent_movement",
                "transaction record is not the immutable prefix being extended",
            )
    elif extensions:
        raise PlanningStoreError(
            "transaction.missing_prefix",
            "cannot append an extension without the durable initial record",
        )
    try:
        rendered = render_planning_contract(
            record,
            toolchain_root=toolchain_root,
            expected_producer_identity=expected_producer,
        )
    except ValueError as error:
        raise PlanningStoreError("transaction.invalid", str(error)) from error

    def validate_written() -> None:
        written = _read_transaction_record(
            path,
            toolchain_root=toolchain_root,
            expected_producer=expected_producer,
        )
        if written != record:
            raise PlanningStoreError(
                "transaction.reread_mismatch",
                "reread transaction does not equal appended record",
            )

    _atomic_replace_and_validate(
        path,
        rendered,
        fault=None,
        validate=validate_written,
    )


def _append_transaction_extension(
    record: JsonObject,
    extension: JsonObject,
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
) -> JsonObject:
    extensions = _transaction_extensions(record)
    if len(extensions) >= len(_TRANSACTION_EXTENSION_ORDER):
        raise PlanningStoreError(
            "transaction.sequence",
            "selection transaction already contains every legal extension",
        )
    expected_type = _TRANSACTION_EXTENSION_ORDER[len(extensions)]
    if extension.get("type") != expected_type:
        raise PlanningStoreError(
            "transaction.sequence",
            f"expected next extension {expected_type!r}",
        )
    updated = _json_object_copy(record, "transaction record")
    updated["extensions"] = [
        *[_json_object_copy(item, "transaction extension") for item in extensions],
        extension,
    ]
    _persist_transaction_record(
        request.transaction_path,
        updated,
        toolchain_root=toolchain_root,
        expected_file_hash=_file_hash(request.transaction_path),
        expected_producer=request.producer,
    )
    return updated


def _transaction_extensions(record: Mapping[str, object]) -> list[JsonObject]:
    raw = record.get("extensions")
    if not isinstance(raw, list):
        raise PlanningStoreError(
            "transaction.extensions",
            "extensions must be a list of objects",
        )
    extensions: list[JsonObject] = []
    for item in cast(list[object], raw):
        if not isinstance(item, dict):
            raise PlanningStoreError(
                "transaction.extensions",
                "extensions must be a list of objects",
            )
        extensions.append(cast(JsonObject, item))
    return extensions


def _validate_transaction_extension_order(record: Mapping[str, object]) -> None:
    extensions = _transaction_extensions(record)
    actual = tuple(item.get("type") for item in extensions)
    expected = _TRANSACTION_EXTENSION_ORDER[: len(actual)]
    if actual != expected:
        raise PlanningStoreError(
            "transaction.sequence",
            f"extensions must be the exact legal prefix {expected!r}; got {actual!r}",
        )


def _transaction_extension(
    record: Mapping[str, object],
    extension_type: str,
) -> JsonObject | None:
    matches = [
        item
        for item in _transaction_extensions(record)
        if item.get("type") == extension_type
    ]
    if len(matches) > 1:
        raise PlanningStoreError(
            "transaction.sequence",
            f"duplicate transaction extension {extension_type!r}",
        )
    return matches[0] if matches else None


def _run_dispatch_stage(
    record: JsonObject,
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
    fault: SelectionFaultPoint | None,
) -> JsonObject:
    observed = _transaction_extension(record, "dispatch_observed")
    if observed is not None:
        _verify_dispatch_observation(observed, request, toolchain_root=toolchain_root)
        return record
    _raise_selection_fault(fault, "before_dispatch_write")
    write_fault: FaultPoint | None = (
        "after_replace_before_validation"
        if fault == "after_dispatch_write_before_validation"
        else None
    )
    write_dispatch_artifact(
        request.lineage.dispatch_path,
        toolchain_root=toolchain_root,
        expected_revision=0,
        expected_file_hash=_EMPTY_FILE_HASH,
        contract=request.dispatch_contract,
        lineage=request.lineage,
        idempotency_key=f"{request.transaction_id}:dispatch",
        fault=write_fault,
    )
    snapshot = read_artifact_document(
        request.lineage.dispatch_path,
        toolchain_root=toolchain_root,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=request.lineage.dispatch_producer,
    )
    extension: JsonObject = {
        "type": "dispatch_observed",
        "dispatch_revision": snapshot.logical_revision,
        "dispatch_file_hash": snapshot.file_hash,
        "validation_result": "passed",
    }
    updated = _append_transaction_extension(
        record,
        extension,
        request,
        toolchain_root=toolchain_root,
    )
    _raise_selection_fault(fault, "after_dispatch_validation")
    return updated


def _run_selected_stage(
    record: JsonObject,
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
    fault: SelectionFaultPoint | None,
) -> JsonObject:
    dispatch_observed = _required_transaction_extension(record, "dispatch_observed")
    selected_contract = _selected_current_contract(request)
    selected_key = f"{request.transaction_id}:selected"
    selected_request_hash = _current_apply_request_hash(
        expected_revision=request.expected_initial_state_revision,
        expected_file_hash=request.expected_initial_state_file_hash,
        replacement_contract=selected_contract,
        idempotency_key=selected_key,
    )
    selected_input = _transaction_extension(record, "selected_input")
    expected_input: JsonObject = {
        "type": "selected_input",
        "expected_state": "idle",
        "expected_state_revision": request.expected_initial_state_revision,
        "expected_state_file_hash": request.expected_initial_state_file_hash,
        "dispatch_path": str(request.lineage.dispatch_path),
        "dispatch_revision": cast(int, dispatch_observed["dispatch_revision"]),
        "request_hash": selected_request_hash,
    }
    if selected_input is None:
        current = read_current_document(request.current_path, toolchain_root=toolchain_root)
        _validate_initial_current(request, current)
        record = _append_transaction_extension(
            record,
            expected_input,
            request,
            toolchain_root=toolchain_root,
        )
        selected_input = expected_input
    elif selected_input != expected_input:
        raise PlanningStoreError(
            "transaction.selected_input_mismatch",
            "persisted selected CAS input does not match the exact request",
        )
    selected_observed = _transaction_extension(record, "selected_observed")
    if selected_observed is not None:
        _validate_transition_observation(
            selected_observed,
            expected_key=selected_key,
            expected_request_hash=selected_request_hash,
            before_revision=request.expected_initial_state_revision,
            after_revision=request.expected_initial_state_revision + 1,
        )
        return record
    _raise_selection_fault(fault, "before_idle_to_selected_cas")
    apply_fault: FaultPoint | None = (
        "after_replace_before_return"
        if fault == "after_idle_to_selected_cas_before_receipt"
        else None
    )
    result = apply_current_document(
        request.current_path,
        toolchain_root=toolchain_root,
        expected_revision=request.expected_initial_state_revision,
        expected_file_hash=request.expected_initial_state_file_hash,
        replacement_contract=selected_contract,
        idempotency_key=selected_key,
        fault=apply_fault,
    )
    current = read_current_document(request.current_path, toolchain_root=toolchain_root)
    _require_current_payload(current, selected_contract, expected="selected", request=request)
    extension: JsonObject = {
        "type": "selected_observed",
        "state_revision": current.logical_revision,
        "state_file_hash": current.file_hash,
        "receipt": _store_receipt_object(result.receipt),
        "validation_result": "passed",
    }
    updated = _append_transaction_extension(
        record,
        extension,
        request,
        toolchain_root=toolchain_root,
    )
    _raise_selection_fault(fault, "after_selected_transition_receipt")
    return updated


def _run_runway_stage(
    record: JsonObject,
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
    fault: SelectionFaultPoint | None,
) -> JsonObject:
    dispatch_observed = _required_transaction_extension(record, "dispatch_observed")
    selected_observed = _required_transaction_extension(record, "selected_observed")
    runway_payload_json = _canonical_json_text(request.runway_contract)
    selected_receipt = _parse_store_receipt(selected_observed.get("receipt"))
    expected_input: JsonObject = {
        "type": "runway_input",
        "runway_payload_json": runway_payload_json,
        "runway_payload_hash": _hash_text(runway_payload_json),
        "dispatch_revision": cast(int, dispatch_observed["dispatch_revision"]),
        "dispatch_file_hash": cast(str, dispatch_observed["dispatch_file_hash"]),
        "selected_state_revision": cast(int, selected_observed["state_revision"]),
        "selected_state_file_hash": cast(str, selected_observed["state_file_hash"]),
        "selected_receipt_request_hash": selected_receipt.request_hash,
    }
    runway_input = _transaction_extension(record, "runway_input")
    if runway_input is None:
        current = read_current_document(request.current_path, toolchain_root=toolchain_root)
        _require_current_payload(
            current,
            _selected_current_contract(request),
            expected="selected",
            request=request,
        )
        record = _append_transaction_extension(
            record,
            expected_input,
            request,
            toolchain_root=toolchain_root,
        )
        runway_input = expected_input
    elif runway_input != expected_input:
        raise PlanningStoreError(
            "transaction.runway_input_mismatch",
            "persisted runway input does not match the exact request",
        )
    runway_observed = _transaction_extension(record, "runway_observed")
    if runway_observed is not None:
        _verify_runway_observation(runway_observed, request, toolchain_root=toolchain_root)
        return record
    current = read_current_document(request.current_path, toolchain_root=toolchain_root)
    _require_current_payload(
        current,
        _selected_current_contract(request),
        expected="selected",
        request=request,
    )
    _raise_selection_fault(fault, "before_runway_write")
    write_fault: FaultPoint | None = (
        "after_replace_before_validation"
        if fault == "after_runway_write_before_validation"
        else None
    )
    write_runway_artifact(
        request.lineage.runway_path,
        toolchain_root=toolchain_root,
        expected_revision=0,
        expected_file_hash=_EMPTY_FILE_HASH,
        expected_dispatch_file_hash=cast(
            str,
            dispatch_observed["dispatch_file_hash"],
        ),
        contract=request.runway_contract,
        lineage=request.lineage,
        idempotency_key=f"{request.transaction_id}:runway",
        fault=write_fault,
    )
    snapshot = read_artifact_document(
        request.lineage.runway_path,
        toolchain_root=toolchain_root,
        expected_schema="planning-runway/v1",
        expected_producer_identity=request.lineage.runway_producer,
    )
    extension: JsonObject = {
        "type": "runway_observed",
        "runway_revision": snapshot.logical_revision,
        "runway_file_hash": snapshot.file_hash,
        "validation_result": "passed",
    }
    updated = _append_transaction_extension(
        record,
        extension,
        request,
        toolchain_root=toolchain_root,
    )
    _raise_selection_fault(fault, "after_runway_validation")
    return updated


def _run_queued_stage(
    record: JsonObject,
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
    fault: SelectionFaultPoint | None,
) -> JsonObject:
    dispatch_observed = _required_transaction_extension(record, "dispatch_observed")
    selected_observed = _required_transaction_extension(record, "selected_observed")
    runway_observed = _required_transaction_extension(record, "runway_observed")
    selected_contract = _selected_current_contract(request)
    queued_contract = _queued_current_contract(request)
    queued_key = f"{request.transaction_id}:queued"
    queued_request_hash = _current_apply_request_hash(
        expected_revision=cast(int, selected_observed["state_revision"]),
        expected_file_hash=cast(str, selected_observed["state_file_hash"]),
        replacement_contract=queued_contract,
        idempotency_key=queued_key,
    )
    expected_input: JsonObject = {
        "type": "queued_input",
        "expected_state": "selected",
        "expected_state_revision": cast(int, selected_observed["state_revision"]),
        "expected_state_file_hash": cast(str, selected_observed["state_file_hash"]),
        "dispatch_path": str(request.lineage.dispatch_path),
        "dispatch_revision": cast(int, dispatch_observed["dispatch_revision"]),
        "dispatch_file_hash": cast(str, dispatch_observed["dispatch_file_hash"]),
        "runway_path": str(request.lineage.runway_path),
        "runway_revision": cast(int, runway_observed["runway_revision"]),
        "runway_file_hash": cast(str, runway_observed["runway_file_hash"]),
        "request_hash": queued_request_hash,
    }
    queued_input = _transaction_extension(record, "queued_input")
    if queued_input is None:
        current = read_current_document(request.current_path, toolchain_root=toolchain_root)
        _require_current_payload(
            current,
            selected_contract,
            expected="selected",
            request=request,
        )
        record = _append_transaction_extension(
            record,
            expected_input,
            request,
            toolchain_root=toolchain_root,
        )
        queued_input = expected_input
    elif queued_input != expected_input:
        raise PlanningStoreError(
            "transaction.queued_input_mismatch",
            "persisted queued CAS input does not match the exact request",
        )
    queued_observed = _transaction_extension(record, "queued_observed")
    if queued_observed is not None:
        _validate_transition_observation(
            queued_observed,
            expected_key=queued_key,
            expected_request_hash=queued_request_hash,
            before_revision=cast(int, selected_observed["state_revision"]),
            after_revision=cast(int, selected_observed["state_revision"]) + 1,
        )
        current = read_current_document(request.current_path, toolchain_root=toolchain_root)
        _require_current_payload(current, queued_contract, expected="queued", request=request)
        return record
    _raise_selection_fault(fault, "before_selected_to_queued_cas")
    apply_fault: FaultPoint | None = (
        "after_replace_before_return"
        if fault == "after_selected_to_queued_cas_before_receipt"
        else None
    )
    result = apply_current_document(
        request.current_path,
        toolchain_root=toolchain_root,
        expected_revision=cast(int, selected_observed["state_revision"]),
        expected_file_hash=cast(str, selected_observed["state_file_hash"]),
        replacement_contract=queued_contract,
        idempotency_key=queued_key,
        fault=apply_fault,
    )
    current = read_current_document(request.current_path, toolchain_root=toolchain_root)
    _require_current_payload(current, queued_contract, expected="queued", request=request)
    extension: JsonObject = {
        "type": "queued_observed",
        "state_revision": current.logical_revision,
        "state_file_hash": current.file_hash,
        "receipt": _store_receipt_object(result.receipt),
        "validation_result": "passed",
    }
    updated = _append_transaction_extension(
        record,
        extension,
        request,
        toolchain_root=toolchain_root,
    )
    _raise_selection_fault(fault, "after_queued_transition_receipt")
    return updated


def _selection_result(
    record: JsonObject,
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
    outcome: Literal["completed", "exact_replay"],
) -> SelectionTransactionResult:
    _validate_transaction_extension_order(record)
    if len(_transaction_extensions(record)) != len(_TRANSACTION_EXTENSION_ORDER):
        raise PlanningStoreError(
            "transaction.incomplete",
            "selection transaction did not reach queued observation",
        )
    dispatch = _required_transaction_extension(record, "dispatch_observed")
    selected = _required_transaction_extension(record, "selected_observed")
    runway = _required_transaction_extension(record, "runway_observed")
    queued = _required_transaction_extension(record, "queued_observed")
    _verify_dispatch_observation(dispatch, request, toolchain_root=toolchain_root)
    _verify_runway_observation(runway, request, toolchain_root=toolchain_root)
    current = read_current_document(request.current_path, toolchain_root=toolchain_root)
    _require_current_payload(
        current,
        _queued_current_contract(request),
        expected="queued",
        request=request,
    )
    if (
        current.logical_revision != queued.get("state_revision")
        or current.file_hash != queued.get("state_file_hash")
    ):
        raise PlanningStoreError(
            "transaction.queued_evidence_mismatch",
            "queued state does not match durable transaction evidence",
        )
    return SelectionTransactionResult(
        outcome=outcome,
        transaction_path=request.transaction_path,
        transaction_file_hash=_file_hash(request.transaction_path),
        current_revision=current.logical_revision,
        dispatch_revision=cast(int, dispatch["dispatch_revision"]),
        runway_revision=cast(int, runway["runway_revision"]),
        selected_receipt=_parse_store_receipt(selected.get("receipt")),
        queued_receipt=_parse_store_receipt(queued.get("receipt")),
    )


def _required_transaction_extension(
    record: Mapping[str, object],
    extension_type: str,
) -> JsonObject:
    extension = _transaction_extension(record, extension_type)
    if extension is None:
        raise PlanningStoreError(
            "transaction.sequence",
            f"required extension {extension_type!r} is missing",
        )
    return extension


def _verify_dispatch_observation(
    observed: Mapping[str, object],
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
) -> None:
    snapshot = read_artifact_document(
        request.lineage.dispatch_path,
        toolchain_root=toolchain_root,
        expected_schema="planning-dispatch/v1",
        expected_producer_identity=request.lineage.dispatch_producer,
    )
    if (
        snapshot.logical_revision != observed.get("dispatch_revision")
        or snapshot.file_hash != observed.get("dispatch_file_hash")
        or _thaw_json(snapshot.contract)
        != _json_object_copy(request.dispatch_contract, "dispatch_contract")
    ):
        raise PlanningStoreError(
            "transaction.dispatch_evidence_mismatch",
            "dispatch does not match durable transaction evidence",
        )


def _verify_runway_observation(
    observed: Mapping[str, object],
    request: SelectionTransactionRequest,
    *,
    toolchain_root: str | Path,
) -> None:
    snapshot = read_artifact_document(
        request.lineage.runway_path,
        toolchain_root=toolchain_root,
        expected_schema="planning-runway/v1",
        expected_producer_identity=request.lineage.runway_producer,
    )
    if (
        snapshot.logical_revision != observed.get("runway_revision")
        or snapshot.file_hash != observed.get("runway_file_hash")
        or _thaw_json(snapshot.contract)
        != _json_object_copy(request.runway_contract, "runway_contract")
    ):
        raise PlanningStoreError(
            "transaction.runway_evidence_mismatch",
            "runway does not match durable transaction evidence",
        )


def _validate_transition_observation(
    observed: Mapping[str, object],
    *,
    expected_key: str,
    expected_request_hash: str,
    before_revision: int,
    after_revision: int,
) -> StoreReceipt:
    receipt = _parse_store_receipt(observed.get("receipt"))
    if (
        receipt.store_interface != _CURRENT_STORE_INTERFACE
        or receipt.idempotency_key != expected_key
        or receipt.request_hash != expected_request_hash
        or receipt.before_revision != before_revision
        or receipt.after_revision != after_revision
        or receipt.touched_finding_ids
        or observed.get("state_revision") != after_revision
    ):
        raise PlanningStoreError(
            "transaction.receipt_mismatch",
            "transition observation does not match exact CAS input and result",
        )
    return receipt


def _selected_current_contract(request: SelectionTransactionRequest) -> JsonObject:
    selected = _json_object_copy(
        request.initial_current_contract,
        "initial_current_contract",
    )
    selected["revision"] = request.expected_initial_state_revision + 1
    selected["selected_dispatch"] = _relative_planning_path(
        request.lineage.dispatch_path,
        request.lineage.planning_root,
    )
    selected["queued_runway"] = None
    selected["active_runway"] = None
    return selected


def _queued_current_contract(request: SelectionTransactionRequest) -> JsonObject:
    queued = _selected_current_contract(request)
    queued["revision"] = request.expected_initial_state_revision + 2
    queued["selected_dispatch"] = None
    queued["queued_runway"] = _relative_planning_path(
        request.lineage.runway_path,
        request.lineage.planning_root,
    )
    queued["active_runway"] = None
    return queued


def _require_current_payload(
    snapshot: CurrentSnapshot,
    expected_contract: Mapping[str, object],
    *,
    expected: Literal["selected", "queued"],
    request: SelectionTransactionRequest,
) -> None:
    if _thaw_json(snapshot.contract) != _json_object_copy(
        expected_contract,
        "expected current contract",
    ):
        raise PlanningStoreError(
            "transaction.state_movement",
            f"current state does not match exact {expected} transaction result",
        )
    _require_current_state(snapshot.contract, expected=expected, request=request)


def _require_current_state(
    contract: Mapping[str, object],
    *,
    expected: Literal["idle", "selected", "queued"],
    request: SelectionTransactionRequest,
) -> None:
    dispatch = _relative_planning_path(
        request.lineage.dispatch_path,
        request.lineage.planning_root,
    )
    runway = _relative_planning_path(
        request.lineage.runway_path,
        request.lineage.planning_root,
    )
    states: dict[str, tuple[object, object, object]] = {
        "idle": (None, None, None),
        "selected": (dispatch, None, None),
        "queued": (None, runway, None),
    }
    actual = (
        contract.get("selected_dispatch"),
        contract.get("queued_runway"),
        contract.get("active_runway"),
    )
    if actual != states[expected]:
        raise PlanningStoreError(
            "transaction.state_movement",
            f"expected {expected} state; got pointers {actual!r}",
        )


def _current_apply_request_hash(
    *,
    expected_revision: int,
    expected_file_hash: str,
    replacement_contract: Mapping[str, object],
    idempotency_key: str,
) -> str:
    return _canonical_request_hash(
        {
            "operation": "apply_current_document",
            "expected_revision": expected_revision,
            "expected_file_hash": expected_file_hash,
            "replacement_contract": dict(replacement_contract),
            "idempotency_key": idempotency_key,
        }
    )


def _store_receipt_object(receipt: StoreReceipt) -> JsonObject:
    return {
        "interface": receipt.interface,
        "store_interface": receipt.store_interface,
        "idempotency_key": receipt.idempotency_key,
        "request_hash": receipt.request_hash,
        "before_revision": receipt.before_revision,
        "after_revision": receipt.after_revision,
        "touched_finding_ids": list(receipt.touched_finding_ids),
    }


def _canonical_json_text(value: Mapping[str, object]) -> str:
    return json.dumps(
        _thaw_json(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _relative_planning_path(path: Path, planning_root: Path) -> str:
    try:
        return path.resolve().relative_to(planning_root.resolve()).as_posix()
    except ValueError as error:
        raise PlanningStoreError(
            "transaction.path_escape",
            f"{path} escapes the explicit planning root",
        ) from error


def _raise_selection_fault(
    fault: SelectionFaultPoint | None,
    checkpoint: SelectionFaultPoint,
) -> None:
    if fault == checkpoint:
        raise InjectedSelectionFailure(checkpoint)


def _simulate_selection_fixture(
    scenario_path: Path,
    *,
    toolchain_root: Path,
) -> SelectionTransactionResult:
    scenario_file = scenario_path / "scenario.yaml"
    try:
        loaded = yaml.load(scenario_file.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as error:
        raise PlanningStoreError("simulation.fixture", str(error)) from error
    if not isinstance(loaded, dict):
        raise PlanningStoreError("simulation.fixture", "scenario.yaml must be an object")
    scenario = cast(dict[object, object], loaded)
    expected_fields = {
        "interface",
        "mode",
        "transaction_id",
        "command_owner_version",
        "current_fixture",
        "artifact_fixture",
    }
    if set(scenario) != expected_fields:
        raise PlanningStoreError(
            "simulation.fixture",
            f"scenario fields must be exactly {sorted(expected_fields)!r}",
        )
    if scenario["interface"] != "selection-simulation/v1":
        raise PlanningStoreError(
            "simulation.fixture",
            "scenario interface must be selection-simulation/v1",
        )
    mode = scenario["mode"]
    if mode not in {"complete", "recover-after-selected-cas", "invalid-reused-id"}:
        raise PlanningStoreError("simulation.fixture", f"unsupported mode {mode!r}")
    transaction_id = scenario["transaction_id"]
    command_owner_version = scenario["command_owner_version"]
    current_fixture = scenario["current_fixture"]
    artifact_fixture = scenario["artifact_fixture"]
    if not all(
        isinstance(value, str) and value.strip()
        for value in (
            transaction_id,
            command_owner_version,
            current_fixture,
            artifact_fixture,
        )
    ):
        raise PlanningStoreError(
            "simulation.fixture",
            "scenario identifiers and fixture paths must be non-empty strings",
        )
    current_source = (scenario_path / cast(str, current_fixture)).resolve()
    artifact_source = (scenario_path / cast(str, artifact_fixture)).resolve()
    artifact_result = validate_planning_contracts(
        [artifact_source],
        toolchain_root=toolchain_root,
    )
    if not artifact_result.is_valid:
        raise PlanningStoreError("simulation.fixture", str(artifact_result.diagnostics[0]))
    artifact_contracts = {
        str(parsed.contract["schema"]): _json_object_copy(
            parsed.contract,
            "fixture contract",
        )
        for parsed in artifact_result.contracts
    }
    try:
        dispatch = artifact_contracts["planning-dispatch/v1"]
        runway = artifact_contracts["planning-runway/v1"]
    except KeyError as error:
        raise PlanningStoreError(
            "simulation.fixture",
            "artifact fixture must contain dispatch and runway contracts",
        ) from error

    with tempfile.TemporaryDirectory(prefix="planning-selection-simulation-") as directory:
        workspace = Path(directory)
        planning_root = workspace / "plans"
        planning_root.mkdir()
        current_path = planning_root / "CURRENT.md"
        shutil.copy2(current_source, current_path)
        ledger_path = planning_root / "LEDGER.md"
        ledger_path.write_text("selection simulation fixture\n", encoding="utf-8")
        initial = read_current_document(current_path, toolchain_root=toolchain_root)
        dispatch["execution_context"] = {
            "toolchain_source_root": str(workspace / "stable"),
            "canonical_planning_repository_root": str(workspace),
            "implementation_target_root": str(workspace / "candidate"),
        }
        runway_execution = runway.get("execution")
        if not isinstance(runway_execution, dict):
            raise PlanningStoreError(
                "simulation.fixture",
                "runway fixture execution must be an object",
            )
        cast(JsonObject, runway_execution)["implementation_target_root"] = str(
            workspace / "candidate"
        )
        dispatch_producer = _producer_from_contract(dispatch)
        runway_producer = _producer_from_contract(runway)
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
            toolchain_source_root=workspace / "stable",
            canonical_planning_repository_root=workspace,
            implementation_target_root=workspace / "candidate",
            dispatch_producer=dispatch_producer,
            runway_producer=runway_producer,
            closeout_producer=ProducerIdentity(
                dispatch_producer.toolchain_generation,
                dispatch_producer.toolchain_commit,
                "planning-closeout/v1",
            ),
        )
        request = SelectionTransactionRequest(
            transaction_id=cast(str, transaction_id),
            transaction_path=planning_root / f"{transaction_id}.md",
            current_path=current_path,
            expected_initial_state_revision=initial.logical_revision,
            expected_initial_state_file_hash=initial.file_hash,
            initial_current_contract=initial.contract,
            lineage=lineage,
            dispatch_contract=dispatch,
            runway_contract=runway,
            command_owner_version=cast(str, command_owner_version),
            producer=ProducerIdentity(
                dispatch_producer.toolchain_generation,
                dispatch_producer.toolchain_commit,
                _TRANSACTION_SCHEMA,
            ),
        )
        if mode == "recover-after-selected-cas":
            try:
                simulate_selection_transaction(
                    request,
                    toolchain_root=toolchain_root,
                    fault="after_idle_to_selected_cas_before_receipt",
                )
            except InjectedStoreFailure:
                pass
            else:
                raise PlanningStoreError(
                    "simulation.fixture",
                    "selected-CAS fault did not interrupt the transaction",
                )
            return simulate_selection_transaction(request, toolchain_root=toolchain_root)
        if mode == "invalid-reused-id":
            try:
                simulate_selection_transaction(
                    request,
                    toolchain_root=toolchain_root,
                    fault="after_dispatch_validation",
                )
            except InjectedSelectionFailure:
                pass
            else:
                raise PlanningStoreError(
                    "simulation.fixture",
                    "dispatch-validation fault did not interrupt the transaction",
                )
            changed_dispatch = _json_object_copy(dispatch, "dispatch fixture")
            scope = changed_dispatch.get("scope")
            if not isinstance(scope, dict):
                raise PlanningStoreError(
                    "simulation.fixture",
                    "dispatch fixture scope must be an object",
                )
            cast(JsonObject, scope)["goal"] = "Conflicting reused transaction intent."
            return simulate_selection_transaction(
                replace(request, dispatch_contract=changed_dispatch),
                toolchain_root=toolchain_root,
            )
        return simulate_selection_transaction(request, toolchain_root=toolchain_root)


def _producer_from_contract(contract: Mapping[str, object]) -> ProducerIdentity:
    producer = contract.get("producer")
    if not isinstance(producer, Mapping):
        raise PlanningStoreError("simulation.fixture", "fixture producer must be an object")
    producer_object = cast(Mapping[str, object], producer)
    generation = producer_object.get("toolchain_generation")
    commit = producer_object.get("toolchain_commit")
    schema_version = producer_object.get("schema_version")
    if not all(isinstance(value, str) for value in (generation, commit, schema_version)):
        raise PlanningStoreError(
            "simulation.fixture",
            "fixture producer fields must be strings",
        )
    return ProducerIdentity(
        cast(str, generation),
        cast(str, commit),
        cast(str, schema_version),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="validate planning contracts")
    validate_parser.add_argument("--toolchain-root", required=True, type=Path)
    validate_parser.add_argument("paths", nargs="+", type=Path)
    compare_parser = subparsers.add_parser(
        "compare-ledger-layouts",
        help="compare per-finding and global ledger fixtures",
    )
    compare_parser.add_argument("--toolchain-root", required=True, type=Path)
    compare_parser.add_argument("--per-finding", required=True, type=Path)
    compare_parser.add_argument("--global", dest="global_path", required=True, type=Path)
    simulate_parser = subparsers.add_parser(
        "simulate-selection",
        help="run a bounded selection transaction fixture",
    )
    simulate_parser.add_argument("--toolchain-root", required=True, type=Path)
    simulate_parser.add_argument("scenario", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "validate":
        result = validate_planning_contracts(args.paths, toolchain_root=args.toolchain_root)
        for diagnostic in result.diagnostics:
            print(diagnostic, file=sys.stderr)
        if result.is_valid:
            print(f"validated {len(result.contracts)} planning contract(s)")
            return 0
        return 1
    if args.command == "compare-ledger-layouts":
        try:
            comparison = compare_ledger_layouts(
                args.per_finding,
                args.global_path,
                toolchain_root=args.toolchain_root,
            )
        except PlanningStoreError as error:
            print(error, file=sys.stderr)
            return 1
        print(json.dumps(comparison.__dict__, sort_keys=True))
        return 0 if comparison.equivalent else 1
    if args.command == "simulate-selection":
        try:
            result = _simulate_selection_fixture(
                args.scenario,
                toolchain_root=args.toolchain_root,
            )
        except PlanningStoreError as error:
            print(error, file=sys.stderr)
            return 1
        print(
            json.dumps(
                {
                    "outcome": result.outcome,
                    "transaction_file_hash": result.transaction_file_hash,
                    "current_revision": result.current_revision,
                    "dispatch_revision": result.dispatch_revision,
                    "runway_revision": result.runway_revision,
                },
                sort_keys=True,
            )
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
