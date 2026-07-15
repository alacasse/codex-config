from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from scripts.skill_contract import ProducerIdentity, validate_skill_contracts


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPO_ROOT / "skills/skill-authoring/SKILL.md"
UI_PATH = REPO_ROOT / "skills/skill-authoring/agents/openai.yaml"
PRE_SLICE_COMMIT = "596fc7e5e153bb1a89a94010d272efa4ce4ce0ce"


def _skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


def _normalized_skill_text() -> str:
    return " ".join(_skill_text().split())


def _frontmatter() -> dict[str, Any]:
    loaded = yaml.safe_load(_skill_text().split("---", 2)[1])
    assert isinstance(loaded, dict)
    return loaded


def _contract() -> dict[str, Any]:
    contract_section = _skill_text().split("## Contract\n", 1)[1]
    loaded = yaml.safe_load(contract_section.split("```yaml\n", 1)[1].split("```", 1)[0])
    assert isinstance(loaded, dict)
    return loaded


def test_core_frontmatter_and_agent_metadata_are_agent_facing() -> None:
    frontmatter = _frontmatter()
    ui = yaml.safe_load(UI_PATH.read_text(encoding="utf-8"))

    assert frontmatter == {
        "name": "skill-authoring",
        "description": (
            "Agent-facing support for creating, migrating, and auditing "
            "contract-first hybrid skills."
        ),
    }
    assert ui["interface"]["display_name"] == "Skill Authoring"
    assert "For agents:" in ui["interface"]["default_prompt"]
    assert "Use $skill-authoring" not in UI_PATH.read_text(encoding="utf-8")


def test_contract_is_one_valid_closed_world_authoring_contract() -> None:
    result = validate_skill_contracts(
        [SKILL_PATH],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=ProducerIdentity(
            toolchain_generation="candidate",
            toolchain_commit=PRE_SLICE_COMMIT,
        ),
    )
    contract = _contract()

    assert result.is_valid, tuple(str(item) for item in result.diagnostics)
    assert len(result.contracts) == 1
    assert contract["schema"] == "skill-contract/v1"
    assert contract["identity"] == {
        "name": "skill-authoring",
        "audience": "authoring-support",
    }
    assert contract["purpose"] == (
        "Create, migrate, and audit contract-first hybrid skills using accepted "
        "ownership, canonicality, procedure, reference, and ambiguity rules."
    )
    assert contract["producer"] == {
        "toolchain_generation": "candidate",
        "toolchain_commit": PRE_SLICE_COMMIT,
        "schema_version": "skill-contract/v1",
    }
    assert contract["owns"] == {
        "decisions": [
            "contract_extraction",
            "skill_structure_design",
            "ownership_conflict_reporting",
            "reference_split_recommendations",
        ],
        "durable_facts": [],
    }
    assert contract["reads"] == {
        "required": [
            "accepted_behavior",
            "accepted_ownership",
            "accepted_audience",
            "accepted_canonicality",
            "accepted_output_contract",
        ],
        "conditional": [
            "migration_request",
            "before_contract_catalog",
            "after_contract_catalog",
            "accepted_migration_policy",
        ],
    }
    assert contract["writes"] == ["authored_skill_document", "authoring_audit"]
    assert contract["delegates"] == [
        {
            "responsibility": "contract_validation",
            "target": "skill_contract_validator",
        },
        {
            "responsibility": "migration_comparison",
            "target": "skill_contract_validator",
        },
    ]
    assert contract["references"] == []


def test_contract_prohibitions_and_outputs_define_observable_boundaries() -> None:
    contract = _contract()

    assert contract["forbids"] == [
        "workflow_execution",
        "planning_state_mutation",
        "silent_ownership_resolution",
        "unapproved_schema_fields",
        "preservation_of_source_prose_by_default",
        "yaml_presence_as_migration_success",
    ]
    assert contract["outputs"]["one_of"] == [
        "authored_skill_result",
        "audited_skill_result",
        "ambiguity_block",
        "migration_block",
    ]
    assert contract["requires"] == {
        "mechanisms": ["skill_contract_validator"],
        "evidence_skills": [],
    }
    assert set(contract["stops_when"]) == {
        "missing_accepted_decision",
        "ownership_conflict",
        "contract_validation_failure",
        "migration_guard_failure",
    }


def test_structure_separates_contract_procedure_branches_rationale_and_references() -> None:
    text = _skill_text()
    normalized = _normalized_skill_text()
    headings = [
        "## Contract",
        "## Procedure",
        "## Branches",
        "## Migration Guards",
        "## Rationale",
        "## Reference Loading",
    ]

    assert text.count("## Contract") == 1
    assert text.count("```yaml") == 1
    assert [text.index(heading) for heading in headings] == sorted(
        text.index(heading) for heading in headings
    )
    assert "`references[*].load_when` entries are the only canonical" in normalized
    assert "Examples are explanatory only" in normalized
    assert "references` list is therefore empty" in normalized


def test_ambiguity_and_missing_decisions_block_without_silent_resolution() -> None:
    text = _normalized_skill_text()

    assert "If an accepted required decision is missing" in text
    assert "return an `ambiguity_block`" in text
    assert "If two sources claim incompatible ownership" in text
    assert "Never choose an owner silently" in text
    assert "named authority or evidence needed to resume" in text
    assert "do not mutate planning state or settle the missing decision" in text


def test_contract_migration_guards_require_catalogs_policy_and_comparison() -> None:
    text = _normalized_skill_text()

    assert "an explicit before catalog" in text
    assert "an explicit after catalog" in text
    assert "an accepted migration policy" in text
    assert "existing validator's public comparison operation" in text
    assert "successful parsing alone is never migration success" in text
    assert "expected transfer did not occur" in text


def test_generic_boundary_is_project_neutral_and_authoring_only() -> None:
    text = _skill_text()
    normalized = _normalized_skill_text()
    lower = text.lower()

    assert "Generic writing, scaffolding, examples, and" in normalized
    assert "Never execute the workflow described by the authored skill" in normalized
    assert "not a workflow command or runtime dependency" in normalized
    assert "project instructions or an active specification" in normalized
    assert "/home/" not in text
    assert "codex-config" not in lower
    assert ".venv" not in text
    assert "pytest" not in lower
