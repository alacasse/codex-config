#!/usr/bin/env python3
"""Bounded ``add-to-ledger/v1`` command owner.

The JSON transport is private to the installed skill.  Human callers never
provide CAS facts, idempotency keys, request identifiers, or source digests.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast


_INVOCATION_ROOT = Path(__file__).parent.parent.absolute()
if str(_INVOCATION_ROOT) not in sys.path:
    sys.path.insert(0, str(_INVOCATION_ROOT))

from scripts.planning_contract import (  # noqa: E402
    FaultPoint,
    PlanningStoreError,
    StoreApplyResult,
    apply_ledger_decision,
    read_ledger_document,
)


INTERFACE = "add-to-ledger/v1"
_HEX_40 = re.compile(r"^[0-9a-f]{40}$")
_FINDING_ID = re.compile(r"^(?P<prefix>[A-Z][A-Z0-9]*)-(?P<number>[0-9]+)$")
_GITHUB_COMPONENT = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,99})$")
_ASCII_WHITESPACE = re.compile(r"[\t\n\v\f\r ]+")
_CONTEXT_FIELDS = frozenset(
    {
        "toolchain_generation",
        "toolchain_commit",
        "toolchain_root",
        "canonical_planning_repository_root",
        "canonical_planning_commit",
        "planning_root",
        "ledger_path",
        "operation_root_kind",
        "canonical_state_mutation_allowed",
        "project_namespace",
    }
)
_INPUT_FIELDS = frozenset(
    {
        "source",
        "title",
        "scope",
        "evidence_pointers",
        "next_action",
        "explicit_target_finding_id",
        "non_intake_changes",
    }
)
_SCOPE_FIELDS = frozenset({"summary", "included", "excluded"})
_NEXT_ACTION_FIELDS = frozenset({"command", "condition"})

JsonValue = str | int | float | bool | None | dict[str, "JsonValue"] | list["JsonValue"]
JsonObject = dict[str, JsonValue]
Action = Literal["create", "update", "no-op"]


@dataclass(frozen=True)
class _BoundContext:
    toolchain_generation: Literal["stable", "candidate"]
    toolchain_commit: str
    toolchain_root: Path
    canonical_planning_repository_root: Path
    canonical_planning_commit: str
    planning_root: Path
    ledger_path: Path
    ledger_relative_path: str
    operation_root_kind: Literal["canonical", "temporary", "fixture"]
    canonical_state_mutation_allowed: bool
    project_namespace: str | None


@dataclass(frozen=True)
class _CanonicalInput:
    index: int
    source_identity: str
    source_revision: str
    source_location: str
    title: str
    scope_summary: str
    included: tuple[str, ...]
    excluded: tuple[str, ...]
    evidence_pointers: tuple[str, ...]
    next_action_command: str
    next_action_condition: str
    explicit_target_finding_id: str | None

    def semantic_key(self) -> tuple[object, ...]:
        return (
            self.source_identity,
            self.source_revision,
            self.source_location,
            self.title,
            self.scope_summary,
            self.included,
            self.excluded,
            self.evidence_pointers,
            self.next_action_command,
            self.next_action_condition,
            self.explicit_target_finding_id,
        )


@dataclass(frozen=True)
class _InputDecision:
    index: int
    source_identity: str
    action: Action
    finding_id: str


@dataclass(frozen=True)
class _PreparedOperation:
    context: _BoundContext
    expected_revision: int
    expected_file_hash: str
    decisions: tuple[_InputDecision, ...]
    mutations: tuple[JsonObject, ...]
    touched_finding_revisions: Mapping[str, int | None]
    store_action: Literal["create", "update", "reconcile"] | None
    private_operation_digest: str | None
    idempotency_key: str | None


class IntakeBlocked(ValueError):
    """Expected fail-closed command outcome with no store invocation."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        input_indices: Sequence[int] = (),
        observed_revision: int | None = None,
        observed_file_hash: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.input_indices = tuple(input_indices)
        self.observed_revision = observed_revision
        self.observed_file_hash = observed_file_hash

    def with_observed(self, *, revision: int, file_hash: str) -> IntakeBlocked:
        return IntakeBlocked(
            self.code,
            str(self),
            input_indices=self.input_indices,
            observed_revision=revision,
            observed_file_hash=file_hash,
        )


def execute_add_to_ledger(
    request: Mapping[str, object],
    *,
    fault: FaultPoint | None = None,
) -> JsonObject:
    """Evaluate one complete request and invoke the store at most once."""

    try:
        prepared = _prepare_operation(request)
        return _apply_prepared_operation(prepared, fault=fault)
    except IntakeBlocked as error:
        return _blocked_result(error)
    except PlanningStoreError as error:
        return _blocked_result(
            IntakeBlocked(f"store.{error.code}", str(error))
        )


def _prepare_operation(request: Mapping[str, object]) -> _PreparedOperation:
    _require_exact_fields(request, {"interface", "context", "inputs"}, "request")
    if request.get("interface") != INTERFACE:
        raise IntakeBlocked("request.interface", f"interface must be {INTERFACE!r}")
    context = _bind_context(_require_mapping(request, "context"))
    raw_inputs = _require_sequence(request, "inputs")
    if not raw_inputs:
        raise IntakeBlocked("request.inputs_empty", "inputs must contain at least one item")

    try:
        snapshot = read_ledger_document(
            context.ledger_path,
            toolchain_root=context.toolchain_root,
        )
    except (OSError, PlanningStoreError) as error:
        raise IntakeBlocked("ledger.invalid", str(error)) from error

    try:
        canonical_inputs = tuple(
            _canonicalize_input(_mapping_item(value, index), index=index)
            for index, value in enumerate(raw_inputs)
        )
        unique_inputs = _coalesce_inputs(canonical_inputs)
        source_index = _source_index(snapshot.findings)
        namespace, maximum = _resolve_namespace(
            snapshot.findings,
            explicit_namespace=context.project_namespace,
        )
        decisions_by_source, mutations, touched = _decide(
            unique_inputs,
            findings=snapshot.findings,
            source_index=source_index,
            namespace=namespace,
            maximum=maximum,
            context=context,
        )
    except IntakeBlocked as error:
        raise error.with_observed(
            revision=snapshot.logical_revision,
            file_hash=snapshot.file_hash,
        ) from error

    decisions = tuple(
        _InputDecision(
            index=item.index,
            source_identity=item.source_identity,
            action=decisions_by_source[item.source_identity].action,
            finding_id=decisions_by_source[item.source_identity].finding_id,
        )
        for item in canonical_inputs
    )
    action_set = {decision.action for decision in decisions_by_source.values()}
    store_action: Literal["create", "update", "reconcile"] | None
    if not mutations:
        store_action = None
    elif action_set == {"create"}:
        store_action = "create"
    elif action_set == {"update"}:
        store_action = "update"
    else:
        store_action = "reconcile"

    digest: str | None = None
    key: str | None = None
    if store_action is not None:
        sorted_mutations = sorted(
            mutations,
            key=lambda mutation: cast(str, mutation["id"]),
        )
        prepared_request: JsonObject = {
            "ledger_path": context.ledger_relative_path,
            "expected_revision": snapshot.logical_revision,
            "expected_file_hash": snapshot.file_hash,
            "action": store_action,
            "finding_mutations": cast(list[JsonValue], sorted_mutations),
            "touched_finding_revisions": {
                key: touched[key] for key in sorted(touched)
            },
        }
        digest = _sha256(_canonical_json(prepared_request))
        key = f"add-to-ledger/v1:{digest}"

    return _PreparedOperation(
        context=context,
        expected_revision=snapshot.logical_revision,
        expected_file_hash=snapshot.file_hash,
        decisions=decisions,
        mutations=tuple(sorted(mutations, key=lambda item: cast(str, item["id"]))),
        touched_finding_revisions=dict(sorted(touched.items())),
        store_action=store_action,
        private_operation_digest=digest,
        idempotency_key=key,
    )


def _apply_prepared_operation(
    prepared: _PreparedOperation,
    *,
    fault: FaultPoint | None = None,
) -> JsonObject:
    if prepared.store_action is None:
        return _success_result(prepared, store_result=None)
    if prepared.idempotency_key is None or prepared.private_operation_digest is None:
        raise RuntimeError("prepared store operation lacks its private identity")
    try:
        result = apply_ledger_decision(
            prepared.context.ledger_path,
            toolchain_root=prepared.context.toolchain_root,
            expected_revision=prepared.expected_revision,
            expected_file_hash=prepared.expected_file_hash,
            action=prepared.store_action,
            finding_mutations=prepared.mutations,
            touched_finding_revisions=prepared.touched_finding_revisions,
            idempotency_key=prepared.idempotency_key,
            fault=fault,
        )
    except PlanningStoreError as error:
        return _blocked_result(
            IntakeBlocked(
                f"store.{error.code}",
                str(error),
                observed_revision=prepared.expected_revision,
                observed_file_hash=prepared.expected_file_hash,
            )
        )
    return _success_result(prepared, store_result=result)


def _bind_context(raw: Mapping[str, object]) -> _BoundContext:
    _require_exact_fields(raw, _CONTEXT_FIELDS, "context")
    generation = _require_string(raw, "toolchain_generation")
    if generation not in {"stable", "candidate"}:
        raise IntakeBlocked("context.generation", "unsupported toolchain generation")
    toolchain_commit = _require_commit(raw, "toolchain_commit")
    canonical_commit = _require_commit(raw, "canonical_planning_commit")
    toolchain_root = _require_root(raw, "toolchain_root")
    canonical_root = _require_root(raw, "canonical_planning_repository_root")
    if _git_head(toolchain_root) != toolchain_commit:
        raise IntakeBlocked("context.toolchain_commit", "toolchain commit does not match HEAD")
    if _git_head(canonical_root) != canonical_commit:
        raise IntakeBlocked(
            "context.canonical_commit",
            "canonical planning repository commit does not match HEAD",
        )

    planning_root = _require_root(raw, "planning_root")
    ledger_path = _require_path(raw, "ledger_path").resolve(strict=True)
    if not ledger_path.is_file() or not ledger_path.is_relative_to(planning_root):
        raise IntakeBlocked(
            "context.ledger_scope",
            "ledger path must resolve to a file below the declared planning root",
        )
    relative = ledger_path.relative_to(planning_root).as_posix()
    kind = _require_string(raw, "operation_root_kind")
    if kind not in {"canonical", "temporary", "fixture"}:
        raise IntakeBlocked("context.root_kind", "unsupported operation root kind")
    mutation_allowed = _require_bool(raw, "canonical_state_mutation_allowed")

    if generation == "candidate" and mutation_allowed:
        raise IntakeBlocked(
            "authority.candidate_canonical_authorization",
            "candidate generation cannot carry canonical mutation authorization",
        )
    planning_is_canonical = planning_root.is_relative_to(canonical_root)
    if kind == "canonical":
        if generation != "stable":
            raise IntakeBlocked(
                "authority.canonical_candidate_write",
                "candidate generation cannot write a canonical ledger",
            )
        if not mutation_allowed or not planning_is_canonical:
            raise IntakeBlocked(
                "authority.canonical_write",
                "canonical mutation requires stable authorization and a canonical planning root",
            )
    elif mutation_allowed or planning_is_canonical:
        raise IntakeBlocked(
            "authority.noncanonical_write",
            "temporary and fixture mutations require canonical mutation disabled and an external planning root",
        )

    namespace_value = raw.get("project_namespace")
    namespace: str | None
    if namespace_value is None:
        namespace = None
    elif isinstance(namespace_value, str) and re.fullmatch(r"[A-Z][A-Z0-9]*", namespace_value):
        namespace = namespace_value
    else:
        raise IntakeBlocked("context.namespace", "project namespace is malformed")

    return _BoundContext(
        toolchain_generation=cast(Literal["stable", "candidate"], generation),
        toolchain_commit=toolchain_commit,
        toolchain_root=toolchain_root,
        canonical_planning_repository_root=canonical_root,
        canonical_planning_commit=canonical_commit,
        planning_root=planning_root,
        ledger_path=ledger_path,
        ledger_relative_path=relative,
        operation_root_kind=cast(Literal["canonical", "temporary", "fixture"], kind),
        canonical_state_mutation_allowed=mutation_allowed,
        project_namespace=namespace,
    )


def _canonicalize_input(raw: Mapping[str, object], *, index: int) -> _CanonicalInput:
    _require_exact_fields(raw, _INPUT_FIELDS, f"inputs[{index}]")
    non_intake = _normalize_list(raw.get("non_intake_changes", []), f"inputs[{index}].non_intake_changes")
    if non_intake:
        raise IntakeBlocked(
            "input.non_intake_change",
            "lifecycle, dependency, destructive, migration, demotion, and contract-narrowing changes are not intake-owned",
            input_indices=(index,),
        )

    source = _require_mapping(raw, "source")
    source_type = _require_string(source, "type")
    if source_type == "plain_text":
        _require_exact_fields(source, {"type", "text"}, f"inputs[{index}].source")
        canonical_text = _normalize_plain_text(_require_string(source, "text"))
        if not canonical_text:
            raise IntakeBlocked("source.empty_text", "plain text source is empty", input_indices=(index,))
        full_digest = _sha256(canonical_text.encode())
        source_identity = f"text:sha256:{full_digest}"
        source_location = "inline-text"
        source_revision = full_digest[:40]
    elif source_type == "github_issue":
        _require_exact_fields(
            source,
            {"type", "owner", "repository", "number", "title", "body"},
            f"inputs[{index}].source",
        )
        owner = _github_component(_require_string(source, "owner"), "owner", index).lower()
        repository = _github_component(
            _require_string(source, "repository"), "repository", index
        ).lower()
        number = source.get("number")
        if isinstance(number, bool) or not isinstance(number, int) or number < 1:
            raise IntakeBlocked(
                "source.github_number",
                "GitHub issue number must be a positive integer",
                input_indices=(index,),
            )
        issue_title = _normalize_single_line(_require_string(source, "title"), "source title")
        issue_body = _normalize_plain_text(_require_string(source, "body"))
        source_identity = f"github-issue:github.com/{owner}/{repository}#{number}"
        source_location = f"https://github.com/{owner}/{repository}/issues/{number}"
        revision_payload: JsonObject = {
            "owner": owner,
            "repository": repository,
            "number": number,
            "title": issue_title,
            "body": issue_body,
        }
        source_revision = _sha256(_canonical_json(revision_payload))[:40]
    else:
        raise IntakeBlocked(
            "source.unsupported",
            f"unsupported source type {source_type!r}",
            input_indices=(index,),
        )

    scope = _require_mapping(raw, "scope")
    _require_exact_fields(scope, _SCOPE_FIELDS, f"inputs[{index}].scope")
    next_action = _require_mapping(raw, "next_action")
    _require_exact_fields(next_action, _NEXT_ACTION_FIELDS, f"inputs[{index}].next_action")
    explicit_target = raw.get("explicit_target_finding_id")
    if explicit_target is not None and not isinstance(explicit_target, str):
        raise IntakeBlocked("input.explicit_target", "explicit target must be a string", input_indices=(index,))

    return _CanonicalInput(
        index=index,
        source_identity=source_identity,
        source_revision=source_revision,
        source_location=source_location,
        title=_normalize_single_line(_require_string(raw, "title"), "title"),
        scope_summary=_normalize_single_line(_require_string(scope, "summary"), "scope summary"),
        included=_normalize_list(_require_sequence(scope, "included"), "scope included"),
        excluded=_normalize_list(_require_sequence(scope, "excluded"), "scope excluded"),
        evidence_pointers=_normalize_list(
            _require_sequence(raw, "evidence_pointers"), "evidence pointers"
        ),
        next_action_command=_normalize_single_line(
            _require_string(next_action, "command"), "next action command"
        ),
        next_action_condition=_normalize_single_line(
            _require_string(next_action, "condition"), "next action condition"
        ),
        explicit_target_finding_id=explicit_target,
    )


def _coalesce_inputs(inputs: Sequence[_CanonicalInput]) -> tuple[_CanonicalInput, ...]:
    grouped: dict[str, list[_CanonicalInput]] = defaultdict(list)
    for item in inputs:
        grouped[item.source_identity].append(item)
    unique: list[_CanonicalInput] = []
    for source_identity in sorted(grouped):
        items = grouped[source_identity]
        first = items[0]
        if any(item.semantic_key() != first.semantic_key() for item in items[1:]):
            raise IntakeBlocked(
                "input.duplicate_source_conflict",
                f"multiple inputs for {source_identity!r} are not equivalent",
                input_indices=tuple(item.index for item in items),
            )
        unique.append(first)
    return tuple(unique)


def _source_index(
    findings: Mapping[str, Mapping[str, object]],
) -> Mapping[str, tuple[str, ...]]:
    index: dict[str, list[str]] = defaultdict(list)
    for finding_id, finding in findings.items():
        provenance = finding.get("provenance")
        if not isinstance(provenance, Mapping):
            raise IntakeBlocked("ledger.provenance", f"finding {finding_id!r} has invalid provenance")
        source_id = cast(Mapping[str, object], provenance).get("source_id")
        if not isinstance(source_id, str):
            raise IntakeBlocked("ledger.provenance", f"finding {finding_id!r} has no source identity")
        index[source_id].append(finding_id)
    return {source_id: tuple(sorted(ids)) for source_id, ids in index.items()}


def _resolve_namespace(
    findings: Mapping[str, Mapping[str, object]],
    *,
    explicit_namespace: str | None,
) -> tuple[str, int]:
    if not findings:
        if explicit_namespace is None:
            raise IntakeBlocked(
                "ledger.empty_namespace",
                "an empty ledger requires a project-authorized namespace",
            )
        return explicit_namespace, 0
    prefixes: set[str] = set()
    slots: set[int] = set()
    maximum = 0
    for finding_id in findings:
        match = _FINDING_ID.fullmatch(finding_id)
        if match is None:
            raise IntakeBlocked(
                "ledger.malformed_namespace",
                f"finding id {finding_id!r} does not match PREFIX-positive-integer",
            )
        prefix = match.group("prefix")
        number = int(match.group("number"))
        if number < 1:
            raise IntakeBlocked(
                "ledger.zero_numeric_slot",
                f"finding id {finding_id!r} uses zero instead of a positive integer",
            )
        if number in slots:
            raise IntakeBlocked("ledger.duplicate_numeric_slot", f"duplicate finding number {number}")
        prefixes.add(prefix)
        slots.add(number)
        maximum = max(maximum, number)
    if len(prefixes) != 1:
        raise IntakeBlocked("ledger.mixed_namespace", "ledger contains mixed finding namespaces")
    namespace = next(iter(prefixes))
    if explicit_namespace is not None and explicit_namespace != namespace:
        raise IntakeBlocked("ledger.namespace_mismatch", "configured namespace does not match ledger")
    return namespace, maximum


def _decide(
    inputs: Sequence[_CanonicalInput],
    *,
    findings: Mapping[str, Mapping[str, object]],
    source_index: Mapping[str, tuple[str, ...]],
    namespace: str,
    maximum: int,
    context: _BoundContext,
) -> tuple[Mapping[str, _InputDecision], list[JsonObject], dict[str, int | None]]:
    creates = [item for item in inputs if not source_index.get(item.source_identity)]
    allocated = {
        item.source_identity: f"{namespace}-{maximum + offset}"
        for offset, item in enumerate(sorted(creates, key=lambda value: value.source_identity), start=1)
    }
    decisions: dict[str, _InputDecision] = {}
    mutations: list[JsonObject] = []
    touched: dict[str, int | None] = {}
    for item in inputs:
        matching_ids = source_index.get(item.source_identity, ())
        if len(matching_ids) > 1:
            raise IntakeBlocked(
                "decision.duplicate_source_identity",
                f"source identity maps to multiple findings: {item.source_identity}",
                input_indices=(item.index,),
            )
        if item.explicit_target_finding_id is not None:
            target = item.explicit_target_finding_id
            if target not in findings:
                raise IntakeBlocked(
                    "decision.missing_explicit_target",
                    f"explicit target {target!r} does not exist",
                    input_indices=(item.index,),
                )
            if not matching_ids or matching_ids[0] != target:
                raise IntakeBlocked(
                    "decision.cross_source_merge",
                    "explicit-target cross-source merge is unsupported in add-to-ledger/v1",
                    input_indices=(item.index,),
                )
        if not matching_ids:
            finding_id = allocated[item.source_identity]
            mutation = _new_finding(item, finding_id=finding_id, context=context)
            action: Action = "create"
            mutations.append(mutation)
            touched[finding_id] = None
        else:
            finding_id = matching_ids[0]
            existing = findings[finding_id]
            replacement_finding = _updated_finding(item, existing=existing)
            if replacement_finding is None:
                action = "no-op"
            else:
                action = "update"
                mutations.append(replacement_finding)
                revision = existing.get("revision")
                if not isinstance(revision, int):
                    raise IntakeBlocked("ledger.finding_revision", f"finding {finding_id!r} has invalid revision")
                touched[finding_id] = revision
        decisions[item.source_identity] = _InputDecision(
            index=item.index,
            source_identity=item.source_identity,
            action=action,
            finding_id=finding_id,
        )
    return decisions, mutations, touched


def _new_finding(item: _CanonicalInput, *, finding_id: str, context: _BoundContext) -> JsonObject:
    return {
        "schema": "planning-finding/v1",
        "id": finding_id,
        "revision": 1,
        "title": item.title,
        "provenance": {
            "source_id": item.source_identity,
            "source_commit": item.source_revision,
            "source_section": item.source_location,
        },
        "lifecycle": {"status": "Pending"},
        "dependencies": [],
        "scope": {
            "summary": item.scope_summary,
            "included": list(item.included),
            "excluded": list(item.excluded),
        },
        "evidence": {"pointers": list(item.evidence_pointers)},
        "next_action": {
            "command": item.next_action_command,
            "condition": item.next_action_condition,
        },
        "producer": {
            "toolchain_generation": context.toolchain_generation,
            "toolchain_commit": context.toolchain_commit,
            "schema_version": "planning-finding/v1",
        },
    }


def _updated_finding(
    item: _CanonicalInput,
    *,
    existing: Mapping[str, object],
) -> JsonObject | None:
    current = _json_copy(existing)
    revision = current.get("revision")
    if not isinstance(revision, int):
        raise IntakeBlocked("ledger.finding_revision", "existing finding revision is invalid")
    provenance = _require_json_object(current, "provenance")
    scope = _require_json_object(current, "scope")
    evidence = _require_json_object(current, "evidence")
    next_action = _require_json_object(current, "next_action")
    current_pointers = _normalize_list(
        _require_json_sequence(evidence, "pointers"), "existing evidence pointers"
    )
    merged_evidence = tuple(sorted(set(current_pointers) | set(item.evidence_pointers)))
    current_intake: JsonObject = {
        "provenance": {
            "source_id": provenance.get("source_id"),
            "source_commit": provenance.get("source_commit"),
            "source_section": provenance.get("source_section"),
        },
        "title": _normalize_single_line(
            _require_json_string(current, "title"), "existing title"
        ),
        "scope": {
            "summary": _normalize_single_line(
                _require_json_string(scope, "summary"), "existing scope summary"
            ),
            "included": list(
                _normalize_list(
                    _require_json_sequence(scope, "included"),
                    "existing scope included",
                )
            ),
            "excluded": list(
                _normalize_list(
                    _require_json_sequence(scope, "excluded"),
                    "existing scope excluded",
                )
            ),
        },
        "next_action": {
            "command": _normalize_single_line(
                _require_json_string(next_action, "command"),
                "existing next action command",
            ),
            "condition": _normalize_single_line(
                _require_json_string(next_action, "condition"),
                "existing next action condition",
            ),
        },
    }
    desired: JsonObject = {
        "provenance": {
            "source_id": item.source_identity,
            "source_commit": item.source_revision,
            "source_section": item.source_location,
        },
        "title": item.title,
        "scope": {
            "summary": item.scope_summary,
            "included": list(item.included),
            "excluded": list(item.excluded),
        },
        "evidence": {"pointers": list(merged_evidence)},
        "next_action": {
            "command": item.next_action_command,
            "condition": item.next_action_condition,
        },
    }
    evidence_is_superset = set(item.evidence_pointers).issubset(current_pointers)
    if (
        current_intake["provenance"] == desired["provenance"]
        and current_intake["title"] == desired["title"]
        and current_intake["scope"] == desired["scope"]
        and current_intake["next_action"] == desired["next_action"]
        and evidence_is_superset
    ):
        return None
    current.update(desired)
    current["revision"] = revision + 1
    return current


def _success_result(
    prepared: _PreparedOperation,
    *,
    store_result: StoreApplyResult | None,
) -> JsonObject:
    affected = sorted(cast(str, item["id"]) for item in prepared.mutations)
    if store_result is None:
        outcome = "no-op"
        write_status = "not_written"
        store: JsonValue = None
    else:
        outcome = store_result.outcome
        write_status = "written" if store_result.outcome == "applied" else "exact_replay"
        receipt = store_result.receipt
        store = {
            "outcome": store_result.outcome,
            "receipt": {
                "interface": receipt.interface,
                "store_interface": receipt.store_interface,
                "before_revision": receipt.before_revision,
                "after_revision": receipt.after_revision,
                "touched_finding_ids": list(receipt.touched_finding_ids),
            },
        }
    return cast(JsonObject, {
        "interface": INTERFACE,
        "outcome": outcome,
        "inputs": cast(list[JsonValue], [
            {
                "input_index": decision.index,
                "source_identity": decision.source_identity,
                "action": decision.action,
                "finding_id": decision.finding_id,
            }
            for decision in prepared.decisions
        ]),
        "affected_finding_ids": affected,
        "observed_ledger": {
            "revision": prepared.expected_revision,
            "file_hash": prepared.expected_file_hash,
        },
        "private_operation_digest": prepared.private_operation_digest,
        "store": store,
        "write_status": write_status,
        "blockers": [],
    })


def _blocked_result(error: IntakeBlocked) -> JsonObject:
    observed: JsonValue = None
    if error.observed_revision is not None and error.observed_file_hash is not None:
        observed = {
            "revision": error.observed_revision,
            "file_hash": error.observed_file_hash,
        }
    return {
        "interface": INTERFACE,
        "outcome": "blocked",
        "inputs": [],
        "affected_finding_ids": [],
        "observed_ledger": observed,
        "private_operation_digest": None,
        "store": None,
        "write_status": "not_written",
        "blockers": [
            {
                "code": error.code,
                "message": str(error),
                "input_indices": list(error.input_indices),
            }
        ],
    }


def _normalize_plain_text(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip(" \t") for line in normalized.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def _normalize_single_line(value: str, label: str) -> str:
    normalized = _ASCII_WHITESPACE.sub(" ", unicodedata.normalize("NFC", value)).strip()
    if not normalized:
        raise IntakeBlocked("input.empty_value", f"{label} must not be empty")
    return normalized


def _normalize_list(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        raise IntakeBlocked("input.list", f"{label} must be a list")
    normalized: list[str] = []
    for index, item in enumerate(cast(Sequence[object], value)):
        if not isinstance(item, str):
            raise IntakeBlocked("input.list_item", f"{label}[{index}] must be a string")
        normalized.append(_normalize_single_line(item, f"{label}[{index}]"))
    return tuple(sorted(set(normalized)))


def _github_component(value: str, label: str, index: int) -> str:
    normalized = unicodedata.normalize("NFC", value).strip()
    if _GITHUB_COMPONENT.fullmatch(normalized) is None:
        raise IntakeBlocked(
            "source.github_component",
            f"GitHub {label} is malformed",
            input_indices=(index,),
        )
    return normalized


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise IntakeBlocked("context.repository", f"cannot resolve repository HEAD for {root}") from error


def _require_exact_fields(raw: Mapping[str, object], expected: set[str] | frozenset[str], label: str) -> None:
    actual = set(raw)
    if actual != set(expected):
        raise IntakeBlocked(
            "request.fields",
            f"{label} fields must be exactly {sorted(expected)}; got {sorted(actual)}",
        )


def _require_mapping(raw: Mapping[str, object], key: str) -> Mapping[str, object]:
    value = raw.get(key)
    if not isinstance(value, Mapping):
        raise IntakeBlocked("request.mapping", f"{key} must be an object")
    return cast(Mapping[str, object], value)


def _require_sequence(raw: Mapping[str, object], key: str) -> Sequence[object]:
    value = raw.get(key)
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        raise IntakeBlocked("request.sequence", f"{key} must be a list")
    return cast(Sequence[object], value)


def _mapping_item(value: object, index: int) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise IntakeBlocked("request.input", f"inputs[{index}] must be an object", input_indices=(index,))
    return cast(Mapping[str, object], value)


def _require_string(raw: Mapping[str, object], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str):
        raise IntakeBlocked("request.string", f"{key} must be a string")
    return value


def _require_commit(raw: Mapping[str, object], key: str) -> str:
    value = _require_string(raw, key)
    if _HEX_40.fullmatch(value) is None:
        raise IntakeBlocked("context.commit", f"{key} must be a full lowercase commit")
    return value


def _require_bool(raw: Mapping[str, object], key: str) -> bool:
    value = raw.get(key)
    if not isinstance(value, bool):
        raise IntakeBlocked("request.boolean", f"{key} must be a boolean")
    return value


def _require_path(raw: Mapping[str, object], key: str) -> Path:
    value = _require_string(raw, key)
    path = Path(value)
    if not path.is_absolute():
        raise IntakeBlocked("context.path", f"{key} must be absolute")
    return path


def _require_root(raw: Mapping[str, object], key: str) -> Path:
    try:
        path = _require_path(raw, key).resolve(strict=True)
    except OSError as error:
        raise IntakeBlocked("context.root", f"{key} does not resolve") from error
    if not path.is_dir():
        raise IntakeBlocked("context.root", f"{key} must resolve to a directory")
    return path


def _json_copy(value: Mapping[str, object]) -> JsonObject:
    return cast(JsonObject, _thaw_json(value))


def _thaw_json(value: object) -> JsonValue:
    if isinstance(value, Mapping):
        typed = cast(Mapping[object, object], value)
        return {
            str(key): _thaw_json(child)
            for key, child in typed.items()
            if isinstance(key, str)
        }
    if isinstance(value, tuple | list):
        return [_thaw_json(child) for child in cast(Sequence[object], value)]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise IntakeBlocked("ledger.json_type", f"unsupported JSON value {type(value).__name__}")


def _require_json_object(raw: JsonObject, key: str) -> JsonObject:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise IntakeBlocked("ledger.object", f"existing {key} must be an object")
    return value


def _require_json_sequence(raw: JsonObject, key: str) -> Sequence[object]:
    value = raw.get(key)
    if not isinstance(value, list):
        raise IntakeBlocked("ledger.list", f"existing {key} must be a list")
    return cast(Sequence[object], value)


def _require_json_string(raw: JsonObject, key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str):
        raise IntakeBlocked("ledger.string", f"existing {key} must be a string")
    return value


def main() -> int:
    try:
        raw = json.load(sys.stdin)
        if not isinstance(raw, Mapping):
            raise IntakeBlocked("request.object", "stdin JSON must be an object")
        result = execute_add_to_ledger(cast(Mapping[str, object], raw))
    except (json.JSONDecodeError, IntakeBlocked) as error:
        blocked = error if isinstance(error, IntakeBlocked) else IntakeBlocked("request.json", str(error))
        result = _blocked_result(blocked)
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
