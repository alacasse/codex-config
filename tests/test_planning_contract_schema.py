from __future__ import annotations

import copy
import json
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts.planning_contract import (
    ProducerIdentity,
    ReadOnlyCompatibility,
    render_planning_contract,
    validate_planning_contracts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/planning-contracts"
VALID = FIXTURES / "schema/valid"
FULL_SHA = "0123456789abcdef0123456789abcdef01234567"
SCHEMA_NAMES = (
    "planning-current/v1",
    "planning-finding/v1",
    "planning-dispatch/v1",
    "planning-runway/v1",
    "planning-closeout/v1",
)


def _schema_path(name: str) -> Path:
    return REPO_ROOT / "schemas" / f"{name.replace('/', '-')}.schema.json"


def _assert_objects_are_closed_world(node: object, path: str = "$") -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False, path
        for key, value in node.items():
            _assert_objects_are_closed_world(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _assert_objects_are_closed_world(value, f"{path}[{index}]")


def _contract_from_fixture(name: str) -> dict[str, Any]:
    source = (VALID / f"{name}.md").read_text(encoding="utf-8")
    loaded = yaml.safe_load(source.split("```yaml\n", 1)[1].split("```", 1)[0])
    assert isinstance(loaded, dict)
    return loaded


def _write_contract(path: Path, contract: Mapping[str, object]) -> Path:
    path.write_text(
        "# Fixture\n\n## Operational Contract\n\n```yaml\n"
        f"{yaml.safe_dump(dict(contract), sort_keys=False)}```\n",
        encoding="utf-8",
    )
    return path


def _validate_runway_contract(tmp_path: Path, contract: Mapping[str, object]) -> object:
    return validate_planning_contracts(
        [_write_contract(tmp_path / "runway.md", contract)],
        toolchain_root=REPO_ROOT,
    )


def _migration_matrix_row() -> dict[str, str]:
    return {
        "current_owner": "previous planning owner",
        "future_owner": "permanent plan-batch owner",
        "reason": "the caller migrates in this bounded slice",
        "status": "pending",
        "removal_slice_or_condition": "focused vertical tests are green",
    }


def _codes(result: object) -> set[str]:
    return {item.code for item in result.diagnostics}  # type: ignore[attr-defined]


def test_all_five_schemas_are_draft_07_and_recursively_closed_world() -> None:
    for name in SCHEMA_NAMES:
        schema = json.loads(_schema_path(name).read_text(encoding="utf-8"))
        assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
        assert schema["properties"]["schema"]["const"] == name
        assert schema["definitions"]["producer"]["required"] == [
            "toolchain_generation",
            "toolchain_commit",
            "schema_version",
        ]
        assert schema["definitions"]["producer"]["properties"][
            "schema_version"
        ]["const"] == name
        _assert_objects_are_closed_world(schema)


def test_valid_fixture_catalog_parses_through_one_public_interface() -> None:
    result = validate_planning_contracts([VALID], toolchain_root=REPO_ROOT)

    assert result.is_valid
    assert result.diagnostics == ()
    assert {item.contract["schema"] for item in result.contracts} == set(SCHEMA_NAMES)


def test_accepts_migration_with_complete_vertical_contract_and_no_coexistence(
    tmp_path: Path,
) -> None:
    result = _validate_runway_contract(tmp_path, _contract_from_fixture("runway"))

    assert result.is_valid  # type: ignore[attr-defined]


def test_accepts_migration_with_temporary_coexistence_and_complete_matrix(
    tmp_path: Path,
) -> None:
    contract = _contract_from_fixture("runway")
    slice_item = contract["slices"][0]
    slice_item["vertical_slice"]["ownership_coexistence"] = "temporary"
    slice_item["migration_matrix"] = {"fixture caller": _migration_matrix_row()}

    result = _validate_runway_contract(tmp_path, contract)

    assert result.is_valid  # type: ignore[attr-defined]


def test_rejects_migration_missing_vertical_slice(tmp_path: Path) -> None:
    contract = _contract_from_fixture("runway")
    del contract["slices"][0]["vertical_slice"]

    result = _validate_runway_contract(tmp_path, contract)

    assert not result.is_valid  # type: ignore[attr-defined]


def test_rejects_migration_missing_matrix_as_required(tmp_path: Path) -> None:
    contract = _contract_from_fixture("runway")
    del contract["slices"][0]["migration_matrix"]

    result = _validate_runway_contract(tmp_path, contract)

    assert _codes(result) == {"schema.required"}


@pytest.mark.parametrize("field", ["migrated_callers", "focused_validation"])
def test_rejects_empty_required_vertical_string_lists(
    tmp_path: Path, field: str
) -> None:
    contract = _contract_from_fixture("runway")
    contract["slices"][0]["vertical_slice"][field] = []

    result = _validate_runway_contract(tmp_path, contract)

    assert _codes(result) == {"schema.minItems"}


@pytest.mark.parametrize("matrix_case", ["empty", "incomplete"])
def test_rejects_temporary_coexistence_with_empty_or_incomplete_matrix(
    tmp_path: Path, matrix_case: str
) -> None:
    contract = _contract_from_fixture("runway")
    slice_item = contract["slices"][0]
    slice_item["vertical_slice"]["ownership_coexistence"] = "temporary"
    matrix = {"fixture caller": _migration_matrix_row()}
    if matrix_case == "empty":
        matrix = {}
    else:
        del matrix["fixture caller"]["removal_slice_or_condition"]
    slice_item["migration_matrix"] = matrix

    result = _validate_runway_contract(tmp_path, contract)

    assert not result.is_valid  # type: ignore[attr-defined]


def test_rejects_no_coexistence_with_retained_matrix_rows(tmp_path: Path) -> None:
    contract = _contract_from_fixture("runway")
    contract["slices"][0]["migration_matrix"] = {
        "fixture caller": _migration_matrix_row()
    }

    result = _validate_runway_contract(tmp_path, contract)

    assert not result.is_valid  # type: ignore[attr-defined]


def test_accepts_non_migration_without_vertical_contract(tmp_path: Path) -> None:
    contract = _contract_from_fixture("runway")
    slice_item = contract["slices"][0]
    slice_item["risk"] = "evidence-only"
    del slice_item["vertical_slice"]
    del slice_item["migration_matrix"]

    result = _validate_runway_contract(tmp_path, contract)

    assert result.is_valid  # type: ignore[attr-defined]


def test_applies_mixed_risk_contract_only_to_migration_slices(
    tmp_path: Path,
) -> None:
    contract = _contract_from_fixture("runway")
    migration_slice = contract["slices"][0]
    evidence_slice = copy.deepcopy(migration_slice)
    evidence_slice["id"] = "evidence"
    evidence_slice["risk"] = "evidence-only"
    del evidence_slice["vertical_slice"]
    del evidence_slice["migration_matrix"]
    contract["batch"]["kind"] = "mixed-risk"
    contract["slices"] = [evidence_slice, migration_slice]

    result = _validate_runway_contract(tmp_path, contract)

    assert result.is_valid  # type: ignore[attr-defined]


@pytest.mark.parametrize("name", ["current", "finding", "dispatch", "runway", "closeout"])
def test_each_schema_rejects_missing_required_and_unknown_fields(
    name: str, tmp_path: Path
) -> None:
    contract = _contract_from_fixture(name)
    required_field = next(field for field in contract if field not in {"schema", "producer"})
    missing = copy.deepcopy(contract)
    missing.pop(required_field)
    unknown = copy.deepcopy(contract)
    unknown["unknown_v1_field"] = True

    missing_result = validate_planning_contracts(
        [_write_contract(tmp_path / f"{name}-missing.md", missing)],
        toolchain_root=REPO_ROOT,
    )
    unknown_result = validate_planning_contracts(
        [_write_contract(tmp_path / f"{name}-unknown.md", unknown)],
        toolchain_root=REPO_ROOT,
    )

    assert _codes(missing_result) == {"schema.required"}
    assert _codes(unknown_result) == {"schema.additionalProperties"}


def test_zero_multiple_and_misplaced_operational_blocks_fail_deterministically(
    tmp_path: Path,
) -> None:
    misplaced = tmp_path / "misplaced.md"
    misplaced.write_text(
        "# Misplaced\n\n## Context\n\nFirst.\n\n## Operational Contract\n\n"
        "```yaml\nschema: planning-current/v1\n```\n",
        encoding="utf-8",
    )
    result = validate_planning_contracts(
        [
            FIXTURES / "schema/invalid-missing-block",
            FIXTURES / "schema/invalid-multiple-blocks",
            misplaced,
        ],
        toolchain_root=REPO_ROOT,
    )

    assert [item.code for item in result.diagnostics] == [
        "contract.block_count",
        "contract.block_count",
        "contract.location",
    ]
    assert all(item.path.endswith("current.md") or item.path == str(misplaced) for item in result.diagnostics)


def test_fenced_markdown_example_does_not_create_a_second_machine_owner(
    tmp_path: Path,
) -> None:
    source = (VALID / "current.md").read_text(encoding="utf-8")
    path = tmp_path / "example.md"
    path.write_text(
        source
        + "\n````markdown\n## Operational Contract\n\n```yaml\n"
        + '"schema": planning-current/v1\n"program": [unterminated\n```\n````\n',
        encoding="utf-8",
    )

    result = validate_planning_contracts([path], toolchain_root=REPO_ROOT)

    assert result.is_valid
    assert len(result.contracts) == 1


def test_malformed_top_level_yaml_without_operational_fields_is_non_owner(
    tmp_path: Path,
) -> None:
    source = (VALID / "current.md").read_text(encoding="utf-8")
    path = tmp_path / "non-owner-example.md"
    path.write_text(
        source
        + "\n## Unrelated Example\n\n```yaml\n"
        + '"unrelated_example": [unterminated\n```\n',
        encoding="utf-8",
    )

    result = validate_planning_contracts([path], toolchain_root=REPO_ROOT)

    assert result.is_valid
    assert len(result.contracts) == 1


def test_supported_yaml_contract_outside_canonical_section_is_second_owner() -> None:
    result = validate_planning_contracts(
        [FIXTURES / "schema/invalid-second-owner.md"], toolchain_root=REPO_ROOT
    )

    assert _codes(result) == {"contract.second_owner"}
    assert result.contracts == ()
    diagnostic = result.diagnostics[0]
    assert diagnostic.location == "$.line[23]"
    assert "planning-current/v1" in diagnostic.message


def test_schema_less_yaml_with_operational_fields_is_second_owner(
    tmp_path: Path,
) -> None:
    source = (FIXTURES / "schema/invalid-second-owner.md").read_text(
        encoding="utf-8"
    )
    path = tmp_path / "schema-less-shadow.md"
    path.write_text(
        source.replace("schema: planning-current/v1\nprogram: another-program\n", "program: another-program\n", 1),
        encoding="utf-8",
    )

    result = validate_planning_contracts([path], toolchain_root=REPO_ROOT)

    assert _codes(result) == {"contract.second_owner"}
    assert "['program']" in result.diagnostics[0].message


def test_producer_only_yaml_is_a_conflicting_machine_fact_owner() -> None:
    result = validate_planning_contracts(
        [FIXTURES / "schema/invalid-secondary-producer-only.md"],
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"contract.second_owner"}
    assert result.contracts == ()
    diagnostic = result.diagnostics[0]
    assert diagnostic.location == "$.line[23]"
    assert "['producer']" in diagnostic.message


@pytest.mark.parametrize(
    ("fixture_name", "message_fragment"),
    [
        ("invalid-secondary-duplicate.md", "found duplicate key 'program'"),
        ("invalid-secondary-malformed.md", "expected ',' or ']'"),
        (
            "invalid-secondary-quoted-duplicate.md",
            "found duplicate key 'program'",
        ),
        ("invalid-secondary-quoted-malformed.md", "expected ',' or ']'"),
    ],
)
def test_invalid_recognizable_secondary_yaml_is_not_silently_ignored(
    fixture_name: str,
    message_fragment: str,
) -> None:
    result = validate_planning_contracts(
        [FIXTURES / "schema" / fixture_name],
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"contract.invalid_secondary_yaml"}
    assert result.contracts == ()
    assert result.diagnostics[0].location == "$.line[23]"
    assert message_fragment in result.diagnostics[0].message


def test_explicit_prose_assignment_cannot_redefine_operational_program() -> None:
    result = validate_planning_contracts(
        [FIXTURES / "schema/invalid-prose-redefinition.md"],
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"contract.prose_redefinition"}
    assert result.contracts == ()
    diagnostic = result.diagnostics[0]
    assert diagnostic.location == "$.line[23]"
    assert "'program'" in diagnostic.message


def test_duplicate_yaml_keys_fail_at_top_level_and_nested(tmp_path: Path) -> None:
    top_level = FIXTURES / "schema/invalid-duplicate-key/current.md"
    nested = (VALID / "current.md").read_text(encoding="utf-8").replace(
        "  toolchain_generation: stable\n",
        "  toolchain_generation: stable\n  toolchain_generation: candidate\n",
    )
    nested_path = tmp_path / "nested.md"
    nested_path.write_text(nested, encoding="utf-8")

    result = validate_planning_contracts([top_level, nested_path], toolchain_root=REPO_ROOT)

    assert _codes(result) == {"contract.invalid_yaml"}
    assert all("found duplicate key" in item.message for item in result.diagnostics)


def test_unknown_schema_version_blocks_without_fallback() -> None:
    result = validate_planning_contracts(
        [FIXTURES / "schema/invalid-unknown-version"], toolchain_root=REPO_ROOT
    )

    assert _codes(result) == {"schema.unsupported_version"}
    assert result.contracts == ()
    assert result.compatibility_reads == ()


def test_explicit_producer_expectations_are_checked_without_cwd_identity() -> None:
    matching = ProducerIdentity("stable", FULL_SHA, "planning-current/v1")
    mismatching = ProducerIdentity("candidate", "f" * 40, "planning-current/v1")

    assert validate_planning_contracts(
        [VALID / "current.md"],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=matching,
    ).is_valid
    result = validate_planning_contracts(
        [VALID / "current.md"],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=mismatching,
    )

    assert _codes(result) == {"producer.mismatch"}
    assert {item.location for item in result.diagnostics} == {
        "$.producer.toolchain_commit",
        "$.producer.toolchain_generation",
    }


def test_renderer_uses_schema_order_and_round_trips(tmp_path: Path) -> None:
    contract = _contract_from_fixture("current")
    reverse_order = dict(reversed(tuple(contract.items())))

    rendered = render_planning_contract(reverse_order, toolchain_root=REPO_ROOT)
    path = tmp_path / "rendered.md"
    path.write_text(f"# Rendered\n\n{rendered}\n## Context\n\nExplanation.\n", encoding="utf-8")
    result = validate_planning_contracts([path], toolchain_root=REPO_ROOT)

    assert rendered.index("schema:") < rendered.index("program:") < rendered.index("revision:")
    assert result.is_valid
    assert result.contracts[0].contract == contract


def test_compatibility_reader_is_explicit_scoped_and_read_only() -> None:
    legacy = FIXTURES / "compatibility/active-current/CURRENT.md"

    default_result = validate_planning_contracts([legacy], toolchain_root=REPO_ROOT)
    explicit_result = validate_planning_contracts(
        [legacy],
        toolchain_root=REPO_ROOT,
        compatibility=ReadOnlyCompatibility(frozenset({legacy})),
    )

    assert _codes(default_result) == {"contract.block_count"}
    assert explicit_result.is_valid
    assert explicit_result.contracts == ()
    assert explicit_result.compatibility_reads[0].program == "codex-config"
    assert explicit_result.compatibility_reads[0].selected_dispatch is None
    with pytest.raises(TypeError, match="canonical mapping"):
        render_planning_contract(  # type: ignore[arg-type]
            explicit_result.compatibility_reads[0], toolchain_root=REPO_ROOT
        )


def test_compatibility_does_not_infer_arbitrary_prose_or_read_archives(
    tmp_path: Path,
) -> None:
    prose = FIXTURES / "compatibility/prose-only/CURRENT.md"
    archive = tmp_path / "archive" / "CURRENT.md"
    archive.parent.mkdir()
    archive.write_text(
        (FIXTURES / "compatibility/active-current/CURRENT.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    result = validate_planning_contracts(
        [prose, archive],
        toolchain_root=REPO_ROOT,
        compatibility=ReadOnlyCompatibility(frozenset({prose, archive})),
    )

    assert _codes(result) == {
        "compatibility.archive_forbidden",
        "compatibility.unrecognized",
    }
    assert result.compatibility_reads == ()


def test_cli_exit_codes_distinguish_valid_contract_findings_and_usage() -> None:
    valid = subprocess.run(
        [
            sys.executable,
            "scripts/planning_contract.py",
            "validate",
            "--toolchain-root",
            ".",
            str(VALID),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    invalid = subprocess.run(
        [
            sys.executable,
            "scripts/planning_contract.py",
            "validate",
            "--toolchain-root",
            ".",
            str(FIXTURES / "schema/invalid-unknown-field"),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    usage = subprocess.run(
        [sys.executable, "scripts/planning_contract.py", "validate"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert valid.returncode == 0
    assert "validated 5 planning contract(s)" in valid.stdout
    assert invalid.returncode == 1
    assert "schema.additionalProperties" in invalid.stderr
    assert usage.returncode == 2
