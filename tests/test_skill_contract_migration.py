from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from scripts.skill_contract import validate_skill_contracts


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/skill-contracts/migration"
FULL_SHA = "5" * 40


def _contract(name: str, audience: str = "human-command-owner") -> dict[str, Any]:
    return {
        "schema": "skill-contract/v1",
        "identity": {"name": name, "audience": audience},
        "producer": {
            "toolchain_generation": "candidate",
            "toolchain_commit": FULL_SHA,
            "schema_version": "skill-contract/v1",
        },
        "purpose": f"Validate the migration contract for {name}.",
        "owns": {"decisions": [], "durable_facts": []},
        "reads": {"required": [], "conditional": []},
        "writes": [],
        "requires": {"mechanisms": [], "evidence_skills": []},
        "delegates": [],
        "forbids": [],
        "outputs": {"one_of": []},
        "stops_when": [],
        "references": [],
    }


def _write_contract(root: Path, directory: str, contract: dict[str, Any]) -> Path:
    path = root / directory / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "# Fixture\n\n## Contract\n\n```yaml\n"
        f"{yaml.safe_dump(contract, sort_keys=False)}```\n",
        encoding="utf-8",
    )
    return path


def _paths(root: Path) -> tuple[Path, ...]:
    return tuple(sorted(root.rglob("SKILL.md")))


def _empty_policy() -> dict[str, object]:
    return {
        "interface": "skill-contract-migration-policy/v1",
        "retired_broad_owners": [],
        "expected_ownership_transfers": [],
    }


def _transfer_policy() -> dict[str, object]:
    return {
        "interface": "skill-contract-migration-policy/v1",
        "retired_broad_owners": ["legacy-owner"],
        "expected_ownership_transfers": [
            {
                "key": "selection_decision",
                "field": "decision",
                "from_owner": "legacy-owner",
                "to_owner": "command-owner",
            }
        ],
    }


def _validate(
    before: tuple[Path, ...],
    after: tuple[Path, ...],
    policy: dict[str, object],
) -> object:
    return validate_skill_contracts(
        after,
        toolchain_root=REPO_ROOT,
        complete_catalog=False,
        before_contract_paths=before,
        after_contract_paths=after,
        migration_policy=policy,
    )


def _codes(result: object) -> list[str]:
    return [item.code for item in result.diagnostics]  # type: ignore[attr-defined]


def test_fixture_catalog_proves_valid_explicit_migration() -> None:
    result = _validate(
        _paths(FIXTURES / "before"),
        _paths(FIXTURES / "after-valid"),
        yaml.safe_load((FIXTURES / "policy.json").read_text(encoding="utf-8")),
    )

    assert result.is_valid  # type: ignore[attr-defined]
    assert result.diagnostics == ()  # type: ignore[attr-defined]


def test_retained_broad_owner_dependency_is_path_qualified() -> None:
    result = _validate(
        _paths(FIXTURES / "before"),
        _paths(FIXTURES / "after-retained-owner"),
        _transfer_policy(),
    )

    assert _codes(result) == ["migration.retained_broad_owner_dependency"]
    diagnostic = result.diagnostics[0]  # type: ignore[attr-defined]
    assert diagnostic.path.endswith("after-retained-owner/command-owner/SKILL.md")
    assert diagnostic.location == "$.requires.mechanisms[0]"


def test_expected_ownership_must_move_to_the_declared_target(tmp_path: Path) -> None:
    before = _contract("legacy-owner")
    before["owns"]["decisions"] = ["selection_decision"]
    after = _contract("command-owner")

    result = _validate(
        (_write_contract(tmp_path / "before", "legacy", before),),
        (_write_contract(tmp_path / "after", "command", after),),
        _transfer_policy(),
    )

    assert _codes(result) == ["migration.ownership_not_moved"]
    assert result.diagnostics[0].location == "$.owns.decisions"  # type: ignore[attr-defined]


def test_after_catalog_must_not_duplicate_durable_facts(tmp_path: Path) -> None:
    before = _contract("before")
    first = _contract("first", "support-mechanism")
    second = _contract("second", "support-mechanism")
    first["owns"]["durable_facts"] = ["durable_result"]
    second["owns"]["durable_facts"] = ["durable_result"]

    result = _validate(
        (_write_contract(tmp_path / "before", "before", before),),
        (
            _write_contract(tmp_path / "after", "first", first),
            _write_contract(tmp_path / "after", "second", second),
        ),
        _empty_policy(),
    )

    assert _codes(result) == [
        "migration.duplicated_durable_fact",
        "migration.duplicated_durable_fact",
    ]
    assert {item.location for item in result.diagnostics} == {  # type: ignore[attr-defined]
        "$.owns.durable_facts[0]"
    }


def test_identity_rename_requires_another_structured_contract_change(
    tmp_path: Path,
) -> None:
    before = _contract("old-name")
    after = copy.deepcopy(before)
    after["identity"]["name"] = "new-name"
    after["producer"]["toolchain_commit"] = "6" * 40

    result = _validate(
        (_write_contract(tmp_path / "before", "old", before),),
        (_write_contract(tmp_path / "after", "new", after),),
        _empty_policy(),
    )

    assert _codes(result) == ["migration.rename_without_contract_change"]
    assert result.diagnostics[0].location == "$.identity.name"  # type: ignore[attr-defined]


def test_same_transfer_key_with_different_policy_fails_closed(tmp_path: Path) -> None:
    before = _contract("legacy-owner")
    after = _contract("command-owner")
    policy = _transfer_policy()
    transfers = policy["expected_ownership_transfers"]
    assert isinstance(transfers, list)
    transfers.append(
        {
            "key": "selection_decision",
            "field": "decision",
            "from_owner": "legacy-owner",
            "to_owner": "different-owner",
        }
    )

    result = _validate(
        (_write_contract(tmp_path / "before", "legacy", before),),
        (_write_contract(tmp_path / "after", "command", after),),
        policy,
    )

    assert _codes(result) == ["migration.policy_key_conflict"]
    assert result.diagnostics[0].path == "<migration-policy>"  # type: ignore[attr-defined]


def test_ambiguous_catalog_identity_fails_deterministically(tmp_path: Path) -> None:
    duplicate = _contract("duplicate")
    after = _contract("after")

    result = _validate(
        (
            _write_contract(tmp_path / "before", "a", duplicate),
            _write_contract(tmp_path / "before", "b", duplicate),
        ),
        (_write_contract(tmp_path / "after", "after", after),),
        _empty_policy(),
    )

    assert _codes(result) == [
        "migration.ambiguous_catalog_identity",
        "migration.ambiguous_catalog_identity",
    ]
    assert [item.location for item in result.diagnostics] == [  # type: ignore[attr-defined]
        "$.identity.name",
        "$.identity.name",
    ]
    assert [item.path for item in result.diagnostics] == sorted(  # type: ignore[attr-defined]
        item.path for item in result.diagnostics  # type: ignore[attr-defined]
    )


def test_compare_cli_uses_the_public_migration_interface() -> None:
    command = [
        sys.executable,
        "scripts/skill_contract.py",
        "compare",
        "--toolchain-root",
        ".",
        "--policy",
        str(FIXTURES / "policy.json"),
        str(FIXTURES / "before"),
    ]
    valid = subprocess.run(
        [*command, str(FIXTURES / "after-valid")],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    retained = subprocess.run(
        [*command, str(FIXTURES / "after-retained-owner")],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert valid.returncode == 0, valid.stderr
    assert valid.stderr == ""
    assert retained.returncode == 1
    assert "migration.retained_broad_owner_dependency" in retained.stderr
