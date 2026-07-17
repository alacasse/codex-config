"""Change Allowance ownership for architecture-program runner dirty paths."""

from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Callable, Iterable, cast

try:
    from scripts import architecture_program_runner_state as _runner_state
    from scripts import planning_contract as _planning_contract
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback.
    import architecture_program_runner_state as _runner_state
    import planning_contract as _planning_contract

RunnerError = _runner_state.RunnerError
project_relative = _runner_state.project_relative
read_json_object = _runner_state.read_json_object
resolve_project_path = _runner_state.resolve_project_path
PlanningStoreError = _planning_contract.PlanningStoreError
ProducerIdentity = _planning_contract.ProducerIdentity
read_artifact_document = _planning_contract.read_artifact_document
read_current_document = _planning_contract.read_current_document
validate_planning_contracts = _planning_contract.validate_planning_contracts


_TOOLCHAIN_ROOT = Path(__file__).resolve().parents[1]


_COMPLETE_SELECTION_EXTENSION_ORDER = (
    "dispatch_observed",
    "selected_input",
    "selected_observed",
    "runway_input",
    "runway_observed",
    "queued_input",
    "queued_observed",
)


def git_status_lines(project: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=project,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RunnerError(f"git status failed in {project}: {completed.stderr.strip()}")
    return [line for line in completed.stdout.splitlines() if line]


def dirty_paths_from_status(lines: Iterable[str]) -> list[str]:
    paths: list[str] = []
    for line in lines:
        if len(line) < 4:
            continue
        raw = line[3:].strip()
        if " -> " in raw:
            before, after = raw.split(" -> ", 1)
            paths.extend([before.strip('"'), after.strip('"')])
        else:
            paths.append(raw.strip('"'))
    return paths


def _project_path(config: Any, value: object) -> str | None:
    if not isinstance(value, str | Path) or not str(value):
        return None
    resolved = resolve_project_path(config.project, str(value)).resolve()
    try:
        return resolved.relative_to(config.project.resolve()).as_posix()
    except ValueError:
        return None


def _string_mapping(value: object) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    mapping = cast(Mapping[object, object], value)
    if not all(isinstance(key, str) for key in mapping):
        return None
    return cast(Mapping[str, Any], mapping)


def _planning_transaction_record(
    path: Path,
) -> tuple[Mapping[str, Any], Any] | None:
    result = validate_planning_contracts([path], toolchain_root=_TOOLCHAIN_ROOT)
    if not result.is_valid or len(result.contracts) != 1:
        return None
    parsed = result.contracts[0]
    if parsed.path.resolve() != path.resolve():
        return None
    record = _string_mapping(cast(object, parsed.contract))
    if record is None or record.get("schema") != "planning-selection-transaction/v1":
        return None
    producer = _string_mapping(cast(object, record.get("producer")))
    if producer is None:
        return None
    generation = producer.get("toolchain_generation")
    commit = producer.get("toolchain_commit")
    schema = producer.get("schema_version")
    if (
        generation not in {"stable", "candidate"}
        or not isinstance(commit, str)
        or len(commit) != 40
        or schema != "planning-selection-transaction/v1"
    ):
        return None
    producer_identity = ProducerIdentity(generation, commit, schema)
    producer_result = validate_planning_contracts(
        [path],
        toolchain_root=_TOOLCHAIN_ROOT,
        expected_producer_identity=producer_identity,
    )
    if not producer_result.is_valid or len(producer_result.contracts) != 1:
        return None
    extensions_value = cast(object, record.get("extensions"))
    if not isinstance(extensions_value, Sequence) or isinstance(
        extensions_value, str | bytes
    ):
        return None
    extensions: list[Mapping[str, Any]] = []
    for value in cast(Sequence[object], extensions_value):
        extension = _string_mapping(value)
        if extension is None:
            return None
        extensions.append(extension)
    if tuple(item.get("type") for item in extensions) != (
        _COMPLETE_SELECTION_EXTENSION_ORDER
    ):
        return None
    for extension_type in (
        "dispatch_observed",
        "selected_observed",
        "runway_observed",
        "queued_observed",
    ):
        extension = next(
            (
                item
                for item in extensions
                if isinstance(item, dict) and item.get("type") == extension_type
            ),
            None,
        )
        if extension is None or extension.get("validation_result") != "passed":
            return None
    return record, producer_identity


def _transaction_extension(
    record: Mapping[str, Any], extension_type: str
) -> Mapping[str, Any] | None:
    extensions_value = cast(object, record.get("extensions"))
    if not isinstance(extensions_value, Sequence) or isinstance(
        extensions_value, str | bytes
    ):
        return None
    for value in cast(Sequence[object], extensions_value):
        extension = _string_mapping(value)
        if extension is not None and extension.get("type") == extension_type:
            return extension
    return None


def _completed_planning_transaction_paths(
    config: Any, state: dict[str, Any], phase: str
) -> set[str]:
    if (
        phase != "create-spec"
        or state.get("active_phase") != "create-spec"
        or state.get("last_phase_status") != "completed"
        or not state.get("last_receipt_path")
    ):
        return set()
    try:
        receipt = read_json_object(
            resolve_project_path(config.project, state["last_receipt_path"])
        )
    except RunnerError:
        return set()
    receipt_path = _project_path(config, receipt.get("receipt_path"))
    state_receipt_path = _project_path(config, state.get("last_receipt_path"))
    receipt_ledger = _project_path(config, receipt.get("program_ledger"))
    config_ledger = _project_path(config, config.program_ledger)
    if (
        receipt.get("phase") != "select-dispatch"
        or receipt.get("status") != "completed"
        or receipt.get("next_phase") != "create-spec"
        or receipt_path is None
        or receipt_path != state_receipt_path
        or receipt_ledger is None
        or receipt_ledger != config_ledger
        or receipt.get("batch_id") != state.get("active_batch_id")
        or receipt.get("dispatch_path") != state.get("dispatch_path")
        or receipt.get("spec_path") != state.get("spec_path")
    ):
        return set()

    evidence_paths_value = cast(object, receipt.get("evidence_paths"))
    if not isinstance(evidence_paths_value, list):
        return set()
    matches: list[tuple[str, Mapping[str, Any], Any]] = []
    for evidence_path in cast(list[object], evidence_paths_value):
        relative = _project_path(config, evidence_path)
        if relative is None:
            continue
        transaction = _planning_transaction_record(config.project / relative)
        if transaction is not None:
            record, producer = transaction
            matches.append((relative, record, producer))
    if len(matches) != 1:
        return set()

    transaction_path, record, producer = matches[0]
    initial_intent = _string_mapping(cast(object, record.get("initial_intent")))
    if initial_intent is None:
        return set()
    ledger_path = _project_path(config, initial_intent.get("ledger_path"))
    current_path = _project_path(config, initial_intent.get("state_path"))
    dispatch_path = _project_path(config, initial_intent.get("dispatch_path"))
    runway_path = _project_path(config, initial_intent.get("runway_path"))
    canonical_current_path = _project_path(
        config, Path(config.program_ledger).parent / "CURRENT.md"
    )
    receipt_dispatch = _project_path(config, receipt.get("dispatch_path"))
    receipt_runway = _project_path(config, receipt.get("spec_path"))
    if (
        ledger_path is None
        or ledger_path != config_ledger
        or current_path is None
        or current_path != canonical_current_path
        or dispatch_path is None
        or runway_path is None
        or dispatch_path != receipt_dispatch
        or runway_path != receipt_runway
        or record.get("batch_id") != receipt.get("batch_id")
    ):
        return set()
    dispatch_observed = _transaction_extension(record, "dispatch_observed")
    selected_observed = _transaction_extension(record, "selected_observed")
    runway_input = _transaction_extension(record, "runway_input")
    runway_observed = _transaction_extension(record, "runway_observed")
    queued_input = _transaction_extension(record, "queued_input")
    queued_observed = _transaction_extension(record, "queued_observed")
    if any(
        value is None
        for value in (
        dispatch_observed,
        selected_observed,
        runway_input,
        runway_observed,
        queued_input,
        queued_observed,
        )
    ):
        return set()
    assert dispatch_observed is not None
    assert selected_observed is not None
    assert runway_input is not None
    assert runway_observed is not None
    assert queued_input is not None
    assert queued_observed is not None
    if (
        _project_path(config, queued_input.get("dispatch_path")) != dispatch_path
        or _project_path(config, queued_input.get("runway_path")) != runway_path
        or runway_input.get("dispatch_revision")
        != dispatch_observed.get("dispatch_revision")
        or runway_input.get("dispatch_file_hash")
        != dispatch_observed.get("dispatch_file_hash")
        or queued_input.get("dispatch_revision")
        != dispatch_observed.get("dispatch_revision")
        or queued_input.get("dispatch_file_hash")
        != dispatch_observed.get("dispatch_file_hash")
        or queued_input.get("runway_revision")
        != runway_observed.get("runway_revision")
        or queued_input.get("runway_file_hash")
        != runway_observed.get("runway_file_hash")
        or queued_input.get("expected_state_revision")
        != selected_observed.get("state_revision")
        or queued_input.get("expected_state_file_hash")
        != selected_observed.get("state_file_hash")
    ):
        return set()

    dispatch_producer = ProducerIdentity(
        producer.toolchain_generation,
        producer.toolchain_commit,
        "planning-dispatch/v1",
    )
    runway_producer = ProducerIdentity(
        producer.toolchain_generation,
        producer.toolchain_commit,
        "planning-runway/v1",
    )
    try:
        current = read_current_document(
            config.project / current_path, toolchain_root=_TOOLCHAIN_ROOT
        )
        dispatch = read_artifact_document(
            config.project / dispatch_path,
            toolchain_root=_TOOLCHAIN_ROOT,
            expected_schema="planning-dispatch/v1",
            expected_producer_identity=dispatch_producer,
        )
        runway = read_artifact_document(
            config.project / runway_path,
            toolchain_root=_TOOLCHAIN_ROOT,
            expected_schema="planning-runway/v1",
            expected_producer_identity=runway_producer,
        )
    except (OSError, PlanningStoreError):
        return set()
    current_ledger = current.contract.get("ledger")
    current_ledger_path = (
        _project_path(config, (config.project / current_path).parent / current_ledger)
        if isinstance(current_ledger, str)
        else None
    )
    dispatch_runway = _string_mapping(
        cast(object, dispatch.contract.get("runway"))
    )
    dispatch_artifact = _string_mapping(
        cast(object, dispatch.contract.get("artifact"))
    )
    runway_artifact = _string_mapping(cast(object, runway.contract.get("artifact")))
    runway_batch = _string_mapping(cast(object, runway.contract.get("batch")))
    if (
        current.logical_revision != queued_observed.get("state_revision")
        or current.file_hash != queued_observed.get("state_file_hash")
        or current_ledger_path != config_ledger
        or current.contract.get("program") != record.get("program")
        or current.contract.get("selected_dispatch") is not None
        or dispatch_runway is None
        or current.contract.get("queued_runway")
        != dispatch_runway.get("expected_path")
        or current.contract.get("active_runway") is not None
        or dispatch_artifact is None
        or dispatch_artifact.get("id") != receipt.get("batch_id")
        or dispatch_artifact.get("program") != record.get("program")
        or runway_artifact is None
        or runway_artifact.get("id") != receipt.get("batch_id")
        or runway_batch is None
        or runway_batch.get("status") != "queued"
        or dispatch.logical_revision != dispatch_observed.get("dispatch_revision")
        or dispatch.file_hash != dispatch_observed.get("dispatch_file_hash")
        or runway.logical_revision != runway_observed.get("runway_revision")
        or runway.file_hash != runway_observed.get("runway_file_hash")
    ):
        return set()
    return {current_path, dispatch_path, runway_path, transaction_path}


def expected_change_allowance_paths(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    extra_paths: Iterable[str] = (),
) -> set[str]:
    expected: set[str] = {project_relative(config.project, config.state_path)}
    if state.get("artifact_root"):
        expected.add(str(state["artifact_root"]))
    for field in (
        "run_manifest_path",
        "batch_manifest_path",
        "active_batch_artifact_root",
    ):
        if state.get(field):
            expected.add(str(state[field]))
    for value in extra_paths:
        expected.add(
            project_relative(config.project, resolve_project_path(config.project, value))
        )

    for field in ("last_receipt_path",):
        if state.get(field):
            expected.add(
                project_relative(
                    config.project, resolve_project_path(config.project, state[field])
                )
            )
    if state.get("last_receipt_path"):
        try:
            receipt = read_json_object(
                resolve_project_path(config.project, state["last_receipt_path"])
            )
        except RunnerError:
            receipt = {}
        if (
            receipt.get("status") == "stopped"
            and receipt.get("phase") == phase
            and isinstance(receipt.get("evidence_paths"), list)
        ):
            for value in receipt["evidence_paths"]:
                if isinstance(value, str):
                    expected.add(
                        project_relative(
                            config.project, resolve_project_path(config.project, value)
                        )
                    )

    if phase == "select-dispatch":
        for field in ("dispatch_path",):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    elif phase == "create-spec":
        for field in ("dispatch_path", "spec_path"):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
        expected.update(_completed_planning_transaction_paths(config, state, phase))
    elif phase == "execute":
        for field in ("spec_path", "dispatch_path"):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    elif phase == "closeout":
        expected.add(config.program_ledger)
        for field in ("spec_path", "last_receipt_path"):
            if state.get(field):
                expected.add(
                    project_relative(
                        config.project, resolve_project_path(config.project, state[field])
                    )
                )
    return {path for path in expected if path and path != "."}


def expected_dirty_paths(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    extra_paths: Iterable[str] = (),
) -> set[str]:
    return expected_change_allowance_paths(config, state, phase, extra_paths=extra_paths)


def check_change_allowance_path(path: str, expected: set[str]) -> bool:
    normalized = path.rstrip("/")
    for candidate in expected:
        candidate = candidate.rstrip("/")
        if normalized == candidate:
            return True
        if normalized.startswith(candidate + "/"):
            return True
        if candidate.startswith(normalized + "/"):
            return True
    return False


def path_is_expected(path: str, expected: set[str]) -> bool:
    return check_change_allowance_path(path, expected)


def check_change_allowance(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
    extra_paths: Iterable[str] = (),
) -> None:
    dirty = dirty_paths_from_status(status_reader(config.project))
    if not dirty:
        return
    expected = expected_change_allowance_paths(config, state, phase, extra_paths=extra_paths)
    transaction_paths = _completed_planning_transaction_paths(config, state, phase)
    ordinary_expected = expected - transaction_paths

    def allowed(path: str) -> bool:
        normalized = path.rstrip("/")
        if normalized in transaction_paths:
            return True
        if any(candidate.startswith(normalized + "/") for candidate in transaction_paths):
            return False
        return check_change_allowance_path(normalized, ordinary_expected)

    unexpected = [path for path in dirty if not allowed(path)]
    if unexpected:
        raise RunnerError(
            "dirty files cannot be classified as expected for "
            f"{phase}: {', '.join(unexpected)}"
        )


def check_worktree(
    config: Any,
    state: dict[str, Any],
    phase: str,
    *,
    status_reader: Callable[[Path], list[str]] = git_status_lines,
    extra_paths: Iterable[str] = (),
) -> None:
    check_change_allowance(
        config,
        state,
        phase,
        status_reader=status_reader,
        extra_paths=extra_paths,
    )
