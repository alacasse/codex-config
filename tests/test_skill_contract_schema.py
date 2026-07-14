from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from scripts.skill_contract import ProducerIdentity, validate_skill_contracts


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/skill-contracts/schema"
VALID_SKILL = FIXTURES / "valid/example/SKILL.md"
FULL_SHA = "0123456789abcdef0123456789abcdef01234567"


def _valid_contract() -> dict[str, Any]:
    loaded = yaml.safe_load(_valid_contract_yaml())
    assert isinstance(loaded, dict)
    return loaded


def _valid_contract_yaml() -> str:
    source = VALID_SKILL.read_text(encoding="utf-8")
    return source.split("```yaml\n", 1)[1].split("```", 1)[0]


def _write_contract(path: Path, contract: object) -> Path:
    path.write_text(
        "# Fixture\n\n## Contract\n\n```yaml\n"
        f"{yaml.safe_dump(contract, sort_keys=False)}```\n",
        encoding="utf-8",
    )
    return path


def _diagnostic_codes(result: object) -> set[str]:
    return {item.code for item in result.diagnostics}  # type: ignore[attr-defined]


def test_canonical_schema_is_draft_07_and_closed_world() -> None:
    schema = json.loads(
        (REPO_ROOT / "schemas/skill-contract-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["additionalProperties"] is False
    assert schema["properties"]["identity"]["additionalProperties"] is False
    assert schema["properties"]["producer"]["additionalProperties"] is False
    assert schema["properties"]["owns"]["additionalProperties"] is False
    assert schema["properties"]["delegates"]["items"]["additionalProperties"] is False
    assert schema["properties"]["references"]["items"]["additionalProperties"] is False


def test_valid_fixture_catalog_parses_through_public_interface() -> None:
    result = validate_skill_contracts([VALID_SKILL], toolchain_root=REPO_ROOT)

    assert result.is_valid
    assert result.diagnostics == ()
    assert len(result.contracts) == 1
    assert result.contracts[0].contract["purpose"] == (
        "Validate the closed-world skill contract fixture."
    )


def test_all_contract_collections_may_be_empty(tmp_path: Path) -> None:
    contract = _valid_contract()
    contract["owns"] = {"decisions": [], "durable_facts": []}
    contract["reads"] = {"required": [], "conditional": []}
    contract["writes"] = []
    contract["requires"] = {"mechanisms": [], "evidence_skills": []}
    contract["delegates"] = []
    contract["forbids"] = []
    contract["outputs"] = {"one_of": []}
    contract["stops_when"] = []
    contract["references"] = []
    path = _write_contract(tmp_path / "empty-collections.md", contract)

    result = validate_skill_contracts([path], toolchain_root=REPO_ROOT)

    assert result.is_valid


def test_requires_exactly_one_contract_yaml_block(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"
    missing.write_text("# No contract\n", encoding="utf-8")
    duplicate = tmp_path / "duplicate.md"
    block = VALID_SKILL.read_text(encoding="utf-8").split("## Contract\n", 1)[1]
    duplicate.write_text(
        f"# Duplicate\n\n## Contract\n{block}\n## Contract\n{block}",
        encoding="utf-8",
    )

    result = validate_skill_contracts(
        [duplicate, missing],
        toolchain_root=REPO_ROOT,
    )

    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "contract.block_count",
        "contract.block_count",
    ]
    assert "found 2" in str(result.diagnostics[0])
    assert "found 0" in str(result.diagnostics[1])


def test_contract_examples_inside_markdown_fences_are_not_canonical(
    tmp_path: Path,
) -> None:
    example = tmp_path / "example-only.md"
    example.write_text(
        "# Example only\n\n````markdown\n## Contract\n\n```yaml\n"
        f"{_valid_contract_yaml()}```\n````\n",
        encoding="utf-8",
    )
    result = validate_skill_contracts([example], toolchain_root=REPO_ROOT)

    assert _diagnostic_codes(result) == {"contract.block_count"}
    assert "found 0" in str(result.diagnostics[0])


def test_real_contract_is_canonical_beside_a_fenced_example(tmp_path: Path) -> None:
    document = tmp_path / "real-and-example.md"
    document.write_text(
        "# Real and example\n\n````markdown\n## Contract\n\n```yaml\n"
        f"{_valid_contract_yaml()}```\n````\n\n## Contract\n\n```yaml\n"
        f"{_valid_contract_yaml()}```\n",
        encoding="utf-8",
    )
    result = validate_skill_contracts([document], toolchain_root=REPO_ROOT)

    assert result.is_valid
    assert len(result.contracts) == 1


def test_duplicate_yaml_keys_fail_at_top_level_and_nested_producer(
    tmp_path: Path,
) -> None:
    duplicate_schema = _valid_contract_yaml().replace(
        "schema: skill-contract/v1\n",
        "schema: skill-contract/v1\nschema: skill-contract/v1\n",
        1,
    )
    duplicate_producer = _valid_contract_yaml().replace(
        "  schema_version: skill-contract/v1\n",
        "  schema_version: skill-contract/v1\n"
        "  schema_version: skill-contract/v1\n",
        1,
    )
    paths = []
    for name, contract_yaml in (
        ("duplicate-schema.md", duplicate_schema),
        ("duplicate-producer.md", duplicate_producer),
    ):
        path = tmp_path / name
        path.write_text(
            f"# Duplicate\n\n## Contract\n\n```yaml\n{contract_yaml}```\n",
            encoding="utf-8",
        )
        paths.append(path)

    result = validate_skill_contracts(paths, toolchain_root=REPO_ROOT)

    assert _diagnostic_codes(result) == {"contract.invalid_yaml"}
    assert all("found duplicate key" in diagnostic.message for diagnostic in result.diagnostics)
    assert any("'schema'" in diagnostic.message for diagnostic in result.diagnostics)
    assert any("'schema_version'" in diagnostic.message for diagnostic in result.diagnostics)


def test_requires_every_accepted_top_level_field_including_producer(
    tmp_path: Path,
) -> None:
    required = {
        "schema",
        "identity",
        "producer",
        "purpose",
        "owns",
        "reads",
        "writes",
        "requires",
        "delegates",
        "forbids",
        "outputs",
        "stops_when",
        "references",
    }

    for field in sorted(required):
        contract = _valid_contract()
        contract.pop(field)
        path = _write_contract(tmp_path / f"missing-{field}.md", contract)
        result = validate_skill_contracts([path], toolchain_root=REPO_ROOT)

        assert "schema.required" in _diagnostic_codes(result), field


def test_rejects_unknown_fields_at_each_v1_object_depth(tmp_path: Path) -> None:
    mutations = {
        "top": lambda contract: contract.__setitem__("unknown", True),
        "identity": lambda contract: contract["identity"].__setitem__(
            "unknown", True
        ),
        "producer": lambda contract: contract["producer"].__setitem__(
            "unknown", True
        ),
        "owns": lambda contract: contract["owns"].__setitem__("unknown", True),
        "reads": lambda contract: contract["reads"].__setitem__("unknown", True),
        "requires": lambda contract: contract["requires"].__setitem__(
            "unknown", True
        ),
        "delegate": lambda contract: contract["delegates"][0].__setitem__(
            "unknown", True
        ),
        "outputs": lambda contract: contract["outputs"].__setitem__(
            "unknown", True
        ),
        "reference": lambda contract: contract["references"][0].__setitem__(
            "unknown", True
        ),
    }

    for label, mutate in mutations.items():
        contract = copy.deepcopy(_valid_contract())
        mutate(contract)
        path = _write_contract(tmp_path / f"unknown-{label}.md", contract)
        result = validate_skill_contracts([path], toolchain_root=REPO_ROOT)

        assert _diagnostic_codes(result) == {"schema.additionalProperties"}, label


def test_rejects_unknown_version_audience_and_invalid_producer(tmp_path: Path) -> None:
    mutations = {
        "version": ("schema.const", ("schema", "skill-contract/v2")),
        "audience": ("schema.enum", ("identity", "audience", "operator")),
        "generation": (
            "schema.enum",
            ("producer", "toolchain_generation", "local"),
        ),
        "commit": ("schema.pattern", ("producer", "toolchain_commit", "HEAD")),
        "producer-version": (
            "schema.const",
            ("producer", "schema_version", "skill-contract/v2"),
        ),
    }

    for label, (expected_code, mutation) in mutations.items():
        contract = _valid_contract()
        *parents, key, value = mutation
        target = contract
        for parent in parents:
            target = target[parent]
        target[key] = value
        path = _write_contract(tmp_path / f"invalid-{label}.md", contract)
        result = validate_skill_contracts([path], toolchain_root=REPO_ROOT)

        assert expected_code in _diagnostic_codes(result), label


def test_checks_only_caller_supplied_expected_producer_identity() -> None:
    matching = validate_skill_contracts(
        [VALID_SKILL],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=ProducerIdentity(
            toolchain_generation="candidate",
            toolchain_commit=FULL_SHA,
        ),
    )
    mismatching = validate_skill_contracts(
        [VALID_SKILL],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=ProducerIdentity(
            toolchain_generation="stable",
            toolchain_commit="f" * 40,
        ),
    )

    assert matching.is_valid
    assert [diagnostic.location for diagnostic in mismatching.diagnostics] == [
        "$.producer.toolchain_commit",
        "$.producer.toolchain_generation",
    ]
    assert _diagnostic_codes(mismatching) == {"producer.identity_mismatch"}


def test_diagnostics_are_path_qualified_and_stably_sorted(tmp_path: Path) -> None:
    first = _write_contract(tmp_path / "b.md", {"schema": "skill-contract/v2"})
    second = _write_contract(tmp_path / "a.md", {"schema": "skill-contract/v2"})

    result = validate_skill_contracts([first, second], toolchain_root=REPO_ROOT)

    assert result.diagnostics == tuple(sorted(result.diagnostics))
    assert all(str(diagnostic).startswith(str(tmp_path)) for diagnostic in result.diagnostics)
    assert {Path(diagnostic.path).name for diagnostic in result.diagnostics} == {
        "a.md",
        "b.md",
    }


def test_interface_rejects_directory_instead_of_discovering_implicit_paths() -> None:
    result = validate_skill_contracts(
        [FIXTURES / "valid"],
        toolchain_root=REPO_ROOT,
    )

    assert not result.is_valid
    assert _diagnostic_codes(result) == {"document.unavailable"}


def test_comparison_inputs_fail_closed_until_migration_slice() -> None:
    result = validate_skill_contracts(
        [VALID_SKILL],
        toolchain_root=REPO_ROOT,
        before_contract_paths=[VALID_SKILL],
    )

    assert _diagnostic_codes(result) == {"comparison.not_available"}


def test_cli_exit_codes_distinguish_findings_from_usage_errors() -> None:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts/skill_contract.py"),
        "validate",
        "--toolchain-root",
        str(REPO_ROOT),
    ]

    valid = subprocess.run(
        [*command, str(FIXTURES / "valid")],
        check=False,
        text=True,
        capture_output=True,
    )
    invalid = subprocess.run(
        [*command, str(FIXTURES / "invalid-unknown-field")],
        check=False,
        text=True,
        capture_output=True,
    )
    usage = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
    )

    assert valid.returncode == 0
    assert valid.stderr == ""
    assert invalid.returncode == 1
    assert "schema.additionalProperties" in invalid.stderr
    assert "$.identity" in invalid.stderr
    assert usage.returncode == 2


def test_cli_catalog_ignores_referenced_markdown_files(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog"
    references = catalog / "references"
    references.mkdir(parents=True)
    (catalog / "SKILL.md").write_text(
        VALID_SKILL.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (references / "details.md").write_text(
        "# Reference\n\nThis is not a skill contract document.\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts/skill_contract.py"),
            "validate",
            "--toolchain-root",
            str(REPO_ROOT),
            str(catalog),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""


def test_cli_fails_closed_for_directory_without_contract_documents(
    tmp_path: Path,
) -> None:
    catalog = tmp_path / "empty-catalog"
    catalog.mkdir()
    (catalog / "README.md").write_text("# Not a contract\n", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts/skill_contract.py"),
            "validate",
            "--toolchain-root",
            str(REPO_ROOT),
            str(catalog),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 1
    assert "catalog.empty" in completed.stderr
    assert str(catalog.resolve()) in completed.stderr
