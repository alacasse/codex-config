from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from scripts.skill_contract import (
    ExternalMechanismPolicy,
    SharedMechanismPolicy,
    validate_skill_contracts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests/fixtures/skill-contracts/catalog"
VALID_CATALOG = FIXTURES / "valid-ownership"
VALID_REFERENCES = FIXTURES / "valid-references"
REFERENCE_CYCLE = FIXTURES / "invalid-reference-cycle"


def _contract(name: str, audience: str) -> dict[str, Any]:
    return {
        "schema": "skill-contract/v1",
        "identity": {"name": name, "audience": audience},
        "producer": {
            "toolchain_generation": "candidate",
            "toolchain_commit": "3" * 40,
            "schema_version": "skill-contract/v1",
        },
        "purpose": f"Validate {name}.",
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


def _write_contract(root: Path, contract: dict[str, Any]) -> Path:
    path = root / str(contract["identity"]["name"]) / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "# Fixture\n\n## Contract\n\n```yaml\n"
        f"{yaml.safe_dump(contract, sort_keys=False)}```\n",
        encoding="utf-8",
    )
    return path


def _write_catalog(root: Path, *contracts: dict[str, Any]) -> tuple[Path, ...]:
    return tuple(_write_contract(root, contract) for contract in contracts)


def _fixture_paths(root: Path) -> tuple[Path, ...]:
    return tuple(sorted(root.rglob("SKILL.md")))


def _toolchain_root(tmp_path: Path) -> Path:
    root = tmp_path / "toolchain"
    schema_path = root / "schemas/skill-contract-v1.schema.json"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(
        (REPO_ROOT / "schemas/skill-contract-v1.schema.json").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    return root


def _codes(result: object) -> set[str]:
    return {item.code for item in result.diagnostics}  # type: ignore[attr-defined]


def test_valid_catalog_exercises_every_audience_profile() -> None:
    result = validate_skill_contracts(
        _fixture_paths(VALID_CATALOG),
        toolchain_root=REPO_ROOT,
    )

    assert result.is_valid
    assert {
        contract.contract["identity"]["audience"]
        for contract in result.contracts
    } == {
        "human-command-owner",
        "support-mechanism",
        "evidence-skill",
        "authoring-support",
    }


def test_add_to_ledger_and_architecture_program_contracts_have_one_intake_owner(
) -> None:
    result = validate_skill_contracts(
        (
            REPO_ROOT / "skills/add-to-ledger/SKILL.md",
            REPO_ROOT / "skills/architecture-program-runway/SKILL.md",
        ),
        toolchain_root=REPO_ROOT,
        external_mechanism_policy=ExternalMechanismPolicy(
            allowed_mechanisms=frozenset(
                {
                    "planning_contract_store",
                    "planning-artifacts",
                    "planning-state",
                }
            )
        ),
        complete_catalog=True,
    )

    assert result.is_valid
    contracts = {
        contract.contract["identity"]["name"]: contract.contract
        for contract in result.contracts
    }
    add_to_ledger = contracts["add-to-ledger"]
    architecture = contracts["architecture-program-runway"]

    assert add_to_ledger["requires"] == {
        "mechanisms": ["planning_contract_store"],
        "evidence_skills": [],
    }
    assert add_to_ledger["delegates"] == [
        {
            "responsibility": "atomic_ledger_application",
            "target": "planning_contract_store",
        }
    ]
    assert architecture["requires"] == {
        "mechanisms": ["planning-artifacts", "planning-state"],
        "evidence_skills": [],
    }
    assert architecture["delegates"] == []

    assert "finding_normalization" in add_to_ledger["owns"]["decisions"]
    assert "atomic_planning_finding_mutation" in add_to_ledger["writes"]
    assert "finding_normalization" not in architecture["owns"]["decisions"]
    assert "atomic_planning_finding_mutation" not in architecture["writes"]
    assert "finding_normalization" in architecture["forbids"]
    assert "atomic_planning_finding_mutation" in architecture["forbids"]
    assert set(architecture["owns"]["decisions"]) == {
        "finding_grouping",
        "finding_prioritization",
        "finding_sequencing",
        "vague_row_disposition",
        "program_batch_selection",
        "program_lifecycle_reconciliation",
    }
    assert set(architecture["owns"]["durable_facts"]) == {
        "grouped_finding_state",
        "selected_dispatch",
        "queue_state",
        "finding_lifecycle_state",
    }
    assert set(architecture["writes"]) == {
        "program_grouping_mutation",
        "selected_dispatch_mutation",
        "queue_state_mutation",
        "program_lifecycle_mutation",
        "same_batch_closeout_reconciliation",
    }
    assert set(architecture["outputs"]["one_of"]) == {
        "grouped_program_state",
        "selected_dispatch_packet",
        "queue_state_update",
        "program_lifecycle_update",
        "same_batch_reconciliation_result",
    }


def test_legacy_removal_contract_is_evidence_only() -> None:
    result = validate_skill_contracts(
        (REPO_ROOT / "skills/legacy-removal/SKILL.md",),
        toolchain_root=REPO_ROOT,
        external_mechanism_policy=ExternalMechanismPolicy(
            allowed_mechanisms=frozenset({"planning-artifacts", "planning-state"})
        ),
        complete_catalog=True,
    )

    assert result.is_valid
    contract = result.contracts[0].contract
    assert contract["identity"] == {
        "name": "legacy-removal",
        "audience": "evidence-skill",
    }
    assert set(contract["owns"]["decisions"]) == {
        "legacy_evidence_classification",
        "canonical_model_decision",
        "compatibility_decision",
        "cleanup_residue_classification",
    }
    assert contract["owns"]["durable_facts"] == [
        "legacy_evidence",
        "compatibility_evidence",
        "cleanup_residue_evidence",
    ]
    assert contract["reads"] == {
        "required": [
            "target_surface",
            "project_instructions",
            "external_compatibility_commitments",
        ],
        "conditional": [
            "planning_state_diagnostic",
            "existing_program_context",
            "dead_surface_evidence",
        ],
    }
    assert set(contract["writes"]) == {
        "legacy_evidence_artifact",
        "legacy_evidence_handoff",
    }
    assert contract["requires"] == {
        "mechanisms": ["planning-artifacts", "planning-state"],
        "evidence_skills": [],
    }
    assert contract["delegates"] == []
    assert {
        "program_ledger_mutation",
        "batch_selection",
        "queue_state",
        "queue_state_mutation",
        "selected_dispatch",
        "selected_dispatch_mutation",
        "dispatch_creation",
        "runway_creation",
        "execution_state",
        "program_lifecycle_state",
        "program_lifecycle_reconciliation",
        "program_lifecycle_mutation",
        "same_batch_closeout_reconciliation",
        "closeout_state",
        "planning_state_mutation",
    } <= set(contract["forbids"])
    assert contract["outputs"] == {
        "one_of": [
            "legacy_evidence_report",
            "canonical_model_evidence",
            "compatibility_decision_evidence",
            "cleanup_residue_evidence",
            "batch_candidate_evidence",
            "dispatch_handoff_evidence",
            "blocked_evidence_result",
        ]
    }
    assert {
        "batch_candidate_evidence",
        "dispatch_handoff_evidence",
        "compatibility_decision_evidence",
        "cleanup_residue_evidence",
    } <= set(contract["outputs"]["one_of"])
    assert contract["stops_when"] == [
        "missing_scope_or_evidence",
        "unresolved_external_compatibility",
        "workflow_state_mutation_requested",
        "owning_program_workflow_not_identified",
    ]


def test_rejects_owned_decisions_and_writes_that_are_also_forbidden(
    tmp_path: Path,
) -> None:
    conflicting = _contract("conflicting", "human-command-owner")
    conflicting["owns"]["decisions"] = ["state_transition"]
    conflicting["writes"] = ["state_transition"]
    conflicting["forbids"] = ["state_transition"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, conflicting),
        toolchain_root=REPO_ROOT,
    )

    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "ownership.owned_and_forbidden",
        "ownership.owned_and_forbidden",
    ]
    assert {diagnostic.location for diagnostic in result.diagnostics} == {
        "$.owns.decisions[0]",
        "$.writes[0]",
    }


def test_rejects_duplicate_human_command_owner_decisions(tmp_path: Path) -> None:
    first = _contract("first", "human-command-owner")
    second = _contract("second", "human-command-owner")
    first["owns"]["decisions"] = ["candidate_selection"]
    second["owns"]["decisions"] = ["candidate_selection"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, first, second),
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"ownership.duplicate_command_decision"}
    assert len(result.diagnostics) == 2


def test_shared_mechanism_policy_explicitly_authorizes_named_durable_fact(
    tmp_path: Path,
) -> None:
    first = _contract("first", "support-mechanism")
    second = _contract("second", "support-mechanism")
    first["owns"]["durable_facts"] = ["shared_projection"]
    second["owns"]["durable_facts"] = ["shared_projection"]
    paths = _write_catalog(tmp_path, first, second)

    rejected = validate_skill_contracts(paths, toolchain_root=REPO_ROOT)
    accepted = validate_skill_contracts(
        paths,
        toolchain_root=REPO_ROOT,
        shared_mechanism_policy=SharedMechanismPolicy(
            authorized_durable_facts=frozenset({"shared_projection"})
        ),
    )

    assert _codes(rejected) == {"ownership.duplicate_durable_fact"}
    assert len(rejected.diagnostics) == 2
    assert accepted.is_valid


def test_support_mechanism_rejects_only_controlled_human_decisions(
    tmp_path: Path,
) -> None:
    support = _contract("support", "support-mechanism")
    support["owns"]["decisions"] = ["candidate_selection", "local_bookkeeping"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, support),
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"audience.support_owns_human_decision"}
    assert len(result.diagnostics) == 1
    assert "candidate_selection" in result.diagnostics[0].message


def test_evidence_skill_rejects_controlled_workflow_state_in_each_owner_field(
    tmp_path: Path,
) -> None:
    evidence = _contract("evidence", "evidence-skill")
    evidence["owns"]["decisions"] = ["candidate_selection", "evidence_sorting"]
    evidence["owns"]["durable_facts"] = ["queued_runway", "review_findings"]
    evidence["writes"] = ["closeout", "review_report"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, evidence),
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"audience.evidence_owns_workflow_state"}
    assert {diagnostic.location for diagnostic in result.diagnostics} == {
        "$.owns.decisions[0]",
        "$.owns.durable_facts[0]",
        "$.writes[0]",
    }


def test_authoring_support_has_no_extra_audience_restrictions(tmp_path: Path) -> None:
    authoring = _contract("authoring", "authoring-support")
    authoring["owns"]["decisions"] = ["candidate_selection"]
    authoring["owns"]["durable_facts"] = ["queued_runway"]
    authoring["writes"] = ["closeout"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, authoring),
        toolchain_root=REPO_ROOT,
    )

    assert result.is_valid


def test_rejects_unknown_delegated_target_at_catalog_validation(
    tmp_path: Path,
) -> None:
    delegator = _contract("delegator", "human-command-owner")
    delegator["delegates"] = [
        {"responsibility": "path_resolution", "target": "missing-target"}
    ]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, delegator),
        toolchain_root=REPO_ROOT,
        complete_catalog=True,
    )

    assert _codes(result) == {"catalog.unknown_delegate_target"}
    assert len(result.contracts) == 1
    assert result.diagnostics[0].location == "$.delegates[0].target"
    assert result.diagnostics[0].path == str(
        (tmp_path / "delegator/SKILL.md").resolve()
    )


def test_catalog_diagnostics_are_sorted_and_path_qualified(tmp_path: Path) -> None:
    first = _contract("zeta", "human-command-owner")
    second = _contract("alpha", "human-command-owner")
    first["owns"]["decisions"] = ["candidate_selection"]
    second["owns"]["decisions"] = ["candidate_selection"]

    result = validate_skill_contracts(
        reversed(_write_catalog(tmp_path, first, second)),
        toolchain_root=REPO_ROOT,
    )

    assert result.diagnostics == tuple(sorted(result.diagnostics))
    assert all(Path(diagnostic.path).is_absolute() for diagnostic in result.diagnostics)


def test_valid_structured_references_ignore_load_when_and_prose_edges() -> None:
    result = validate_skill_contracts(
        _fixture_paths(VALID_REFERENCES),
        toolchain_root=REPO_ROOT,
    )

    assert result.is_valid
    alpha = next(
        contract
        for contract in result.contracts
        if contract.contract["identity"]["name"] == "reference-alpha"
    )
    assert alpha.contract["references"][0]["load_when"] == ["../beta/SKILL.md"]


def test_external_mechanism_policy_is_required_for_external_targets(
    tmp_path: Path,
) -> None:
    contract = _contract("delegator", "human-command-owner")
    contract["requires"]["mechanisms"] = ["external-mechanism"]
    contract["delegates"] = [
        {"responsibility": "external_operation", "target": "external-mechanism"}
    ]
    paths = _write_catalog(tmp_path, contract)

    rejected = validate_skill_contracts(
        paths,
        toolchain_root=REPO_ROOT,
        complete_catalog=True,
    )
    accepted = validate_skill_contracts(
        paths,
        toolchain_root=REPO_ROOT,
        external_mechanism_policy=ExternalMechanismPolicy(
            allowed_mechanisms=frozenset({"external-mechanism"})
        ),
        complete_catalog=True,
    )

    assert _codes(rejected) == {
        "catalog.unknown_delegate_target",
        "catalog.unknown_required_mechanism",
    }
    assert accepted.is_valid


def test_required_evidence_skill_must_resolve_in_explicit_catalog(
    tmp_path: Path,
) -> None:
    contract = _contract("consumer", "human-command-owner")
    contract["requires"]["evidence_skills"] = ["missing-evidence"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, contract),
        toolchain_root=REPO_ROOT,
        complete_catalog=True,
    )

    assert _codes(result) == {"catalog.unknown_required_evidence_skill"}
    assert result.diagnostics[0].location == "$.requires.evidence_skills[0]"


def test_dependency_cycle_uses_only_structured_catalog_edges(tmp_path: Path) -> None:
    first = _contract("first", "human-command-owner")
    second = _contract("second", "support-mechanism")
    first["delegates"] = [
        {"responsibility": "second_operation", "target": "second"}
    ]
    second["requires"]["mechanisms"] = ["first"]

    result = validate_skill_contracts(
        _write_catalog(tmp_path, first, second),
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"dependency.cycle"}
    assert len(result.diagnostics) == 1
    assert result.diagnostics[0].message == "dependency cycle: first -> second -> first"
    assert result.diagnostics[0].location == "$.requires.mechanisms[0]"


def test_reference_cycle_is_stable_and_path_qualified() -> None:
    result = validate_skill_contracts(
        _fixture_paths(REFERENCE_CYCLE),
        toolchain_root=REPO_ROOT,
    )

    assert _codes(result) == {"reference.cycle"}
    assert len(result.diagnostics) == 1
    assert result.diagnostics[0].location == "$.references[0].path"
    assert result.diagnostics[0].message == (
        "reference cycle: "
        "tests/fixtures/skill-contracts/catalog/invalid-reference-cycle/first/SKILL.md"
        " -> "
        "tests/fixtures/skill-contracts/catalog/invalid-reference-cycle/second/SKILL.md"
        " -> "
        "tests/fixtures/skill-contracts/catalog/invalid-reference-cycle/first/SKILL.md"
    )


def test_missing_and_non_file_references_fail_closed(tmp_path: Path) -> None:
    root = _toolchain_root(tmp_path)
    contract = _contract("owner", "authoring-support")
    contract["references"] = [
        {"path": "missing.md", "load_when": ["missing_probe"]},
        {"path": "reference-dir", "load_when": ["directory_probe"]},
    ]
    path = _write_contract(root, contract)
    (path.parent / "reference-dir").mkdir()

    result = validate_skill_contracts(
        [path],
        toolchain_root=root,
        complete_catalog=True,
    )

    assert _codes(result) == {"reference.missing", "reference.not_file"}
    assert {diagnostic.location for diagnostic in result.diagnostics} == {
        "$.references[0].path",
        "$.references[1].path",
    }


def test_dotdot_and_symlink_escapes_fail_after_strict_resolution(
    tmp_path: Path,
) -> None:
    root = _toolchain_root(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    contract = _contract("owner", "authoring-support")
    contract["references"] = [
        {"path": "../../outside.md", "load_when": ["dotdot_probe"]},
        {"path": "outside-link.md", "load_when": ["symlink_probe"]},
    ]
    path = _write_contract(root, contract)
    (path.parent / "outside-link.md").symlink_to(outside)

    result = validate_skill_contracts(
        [path],
        toolchain_root=root,
        complete_catalog=True,
    )

    assert _codes(result) == {"reference.outside_toolchain_root"}
    assert len(result.diagnostics) == 2


def test_reference_resolution_uses_document_and_explicit_root_not_cwd(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    root = _toolchain_root(tmp_path)
    contract = _contract("owner", "authoring-support")
    contract["references"] = [
        {"path": "details.md", "load_when": ["details_probe"]}
    ]
    path = _write_contract(root, contract)
    (path.parent / "details.md").write_text("# Details\n", encoding="utf-8")
    unrelated_cwd = tmp_path / "unrelated-cwd"
    unrelated_cwd.mkdir()
    monkeypatch.chdir(unrelated_cwd)

    result = validate_skill_contracts(
        [path],
        toolchain_root=root,
        complete_catalog=True,
    )

    assert result.is_valid
