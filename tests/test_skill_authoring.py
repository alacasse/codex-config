from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from scripts.skill_contract import ProducerIdentity, validate_skill_contracts


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPO_ROOT / "skills/skill-authoring/SKILL.md"
UI_PATH = REPO_ROOT / "skills/skill-authoring/agents/openai.yaml"
REFERENCE_PATH = (
    REPO_ROOT
    / "skills/skill-authoring/references/planning-artifact-authoring.md"
)
NARROW_TRIAL_PATH = (
    REPO_ROOT / "tests/fixtures/skill-authoring/narrow-evidence/SKILL.md"
)
BRANCHING_TRIAL_ROOT = (
    REPO_ROOT / "tests/fixtures/skill-authoring/branching-command"
)
BRANCHING_COMMAND_PATH = BRANCHING_TRIAL_ROOT / "command/SKILL.md"
BRANCHING_SUPPORT_PATH = BRANCHING_TRIAL_ROOT / "support/SKILL.md"
PRE_SLICE_COMMIT = "7ff339c76430347fff57edc5ffbdda44a0bb43e5"
TRIAL_PRODUCER_COMMIT = "23db635dba08d7d1641fccfa0652ff5d3df0d2f6"
SUPPORTED_PLANNING_SCHEMAS = [
    "planning-current/v1",
    "planning-finding/v1",
    "planning-dispatch/v1",
    "planning-runway/v1",
    "planning-closeout/v1",
    "planning-selection-transaction/v1",
]


def _skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


def _normalized_skill_text() -> str:
    return " ".join(_skill_text().split())


def _reference_text() -> str:
    return REFERENCE_PATH.read_text(encoding="utf-8")


def _normalized_reference_text() -> str:
    return " ".join(_reference_text().split())


def _support_policies() -> list[dict[str, Any]]:
    policies = []
    for source in re.findall(r"```yaml\n(.*?)```", _reference_text(), re.DOTALL):
        loaded = yaml.safe_load(source)
        if isinstance(loaded, dict) and "supported_schemas" in loaded:
            policies.append(loaded)
    return policies


def _frontmatter() -> dict[str, Any]:
    loaded = yaml.safe_load(_skill_text().split("---", 2)[1])
    assert isinstance(loaded, dict)
    return loaded


def _contract() -> dict[str, Any]:
    contract_section = _skill_text().split("## Contract\n", 1)[1]
    loaded = yaml.safe_load(contract_section.split("```yaml\n", 1)[1].split("```", 1)[0])
    assert isinstance(loaded, dict)
    return loaded


def _fixture_contract(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    contract_section = source.split("## Contract\n", 1)[1]
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
    assert contract["references"] == [
        {
            "path": "references/planning-artifact-authoring.md",
            "load_when": ["create_or_modify_supported_planning_artifact"],
        }
    ]


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
    assert "one conditional planning-artifact reference" in normalized


def test_planning_reference_declares_exact_supported_schema_list() -> None:
    policies = _support_policies()

    assert len(policies) == 1
    assert policies[0] == {"supported_schemas": SUPPORTED_PLANNING_SCHEMAS}
    for schema_name in SUPPORTED_PLANNING_SCHEMAS:
        schema_path = REPO_ROOT / "schemas" / f"{schema_name.replace('/', '-')}.schema.json"
        loaded = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        assert loaded["properties"]["schema"]["const"] == schema_name


def test_planning_reference_loads_only_for_supported_artifact_changes() -> None:
    contract = _contract()
    text = _reference_text()

    assert contract["references"] == [
        {
            "path": "references/planning-artifact-authoring.md",
            "load_when": ["create_or_modify_supported_planning_artifact"],
        }
    ]
    assert (
        "| Create or modify an artifact with one exact supported schema | "
        "Load this reference, then continue authoring. |"
    ) in text
    assert (
        "| Ordinary hybrid-skill authoring | Do not load this reference. |"
    ) in text


def test_unsupported_schema_and_missing_identity_block_before_authoring() -> None:
    text = _reference_text()

    for unsupported_case in (
        "missing schema identity",
        "an unknown schema name",
        "an unsupported schema version",
    ):
        assert (
            f"| Create or modify an artifact with {unsupported_case} | "
            "Block before authoring or mutation. |"
        ) in text
    assert "Never guess a schema identity" in text
    assert "upgrade or downgrade a version" in _normalized_reference_text()


def test_planning_reference_consumes_layout_without_redefining_core() -> None:
    text = _reference_text()
    lower = text.lower()

    assert "Planning Artifact Layout v1" in text
    assert "existing schema and planning validator/store owner" in text
    assert "It owns no planning root, schema, workflow decision" in text
    assert "introduces no second skill contract block" in text
    assert "## Contract" not in text
    assert "skill-contract/v" not in text
    assert "/home/" not in text
    assert "codex-config" not in lower


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


def test_narrow_trial_is_standalone_evidence_catalog() -> None:
    result = validate_skill_contracts(
        [NARROW_TRIAL_PATH],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=ProducerIdentity(
            toolchain_generation="candidate",
            toolchain_commit=TRIAL_PRODUCER_COMMIT,
        ),
        complete_catalog=True,
    )
    contract = _fixture_contract(NARROW_TRIAL_PATH)

    assert result.is_valid, tuple(str(item) for item in result.diagnostics)
    assert contract["schema"] == "skill-contract/v1"
    assert contract["identity"] == {
        "name": "fixture-evidence-classifier",
        "audience": "evidence-skill",
    }
    assert contract["owns"] == {
        "decisions": ["evidence_classification"],
        "durable_facts": ["evidence_output"],
    }
    assert contract["writes"] == ["evidence_output"]
    assert contract["requires"] == {"mechanisms": [], "evidence_skills": []}
    assert contract["delegates"] == []
    assert contract["forbids"] == [
        "planning_state_mutation",
        "workflow_decisions",
        "workflow_execution",
    ]
    assert contract["outputs"]["one_of"] == [
        "classified_evidence",
        "insufficient_evidence",
    ]


def test_branching_trial_catalog_has_one_command_owner_and_mechanical_support() -> None:
    result = validate_skill_contracts(
        [BRANCHING_COMMAND_PATH, BRANCHING_SUPPORT_PATH],
        toolchain_root=REPO_ROOT,
        expected_producer_identity=ProducerIdentity(
            toolchain_generation="candidate",
            toolchain_commit=TRIAL_PRODUCER_COMMIT,
        ),
        complete_catalog=True,
    )
    command = _fixture_contract(BRANCHING_COMMAND_PATH)
    support = _fixture_contract(BRANCHING_SUPPORT_PATH)

    assert result.is_valid, tuple(str(item) for item in result.diagnostics)
    assert command["identity"]["audience"] == "human-command-owner"
    assert command["owns"] == {
        "decisions": ["bounded_route_selection"],
        "durable_facts": [],
    }
    assert command["writes"] == []
    assert command["delegates"] == [
        {
            "responsibility": "route_inspection",
            "target": "fixture-route-inspector",
        }
    ]
    assert command["requires"] == {
        "mechanisms": ["fixture-route-inspector"],
        "evidence_skills": [],
    }
    assert support["identity"] == {
        "name": "fixture-route-inspector",
        "audience": "support-mechanism",
    }
    assert support["owns"]["decisions"] == []
    assert support["writes"] == []
    assert "bounded_route_selection" in support["forbids"]


def test_branching_trial_exposes_normal_alternate_blocked_outcomes_and_stops() -> None:
    contract = _fixture_contract(BRANCHING_COMMAND_PATH)
    text = " ".join(
        BRANCHING_COMMAND_PATH.read_text(encoding="utf-8").split()
    )

    assert contract["outputs"]["one_of"] == [
        "normal_route_selected",
        "alternate_route_selected",
        "blocked_route_result",
    ]
    assert contract["stops_when"] == [
        "missing_explicit_request",
        "blocking_constraint",
    ]
    assert "## Normal Procedure" in text
    assert (
        "- Normal: when the request is complete and no alternate or blocker "
        "applies, return `normal_route_selected`."
    ) in text
    assert (
        "- Alternate: when the request explicitly selects the allowed alternate "
        "and no blocker applies, return `alternate_route_selected`."
    ) in text
    assert (
        "- Blocked: when the request is missing or inspection reports a blocking "
        "constraint, return `blocked_route_result` without selecting a route."
    ) in text
    assert "## Stop Conditions" in text
    assert (
        "Return one route-selection result without executing that route."
    ) in text


def test_trial_catalogs_share_one_version_and_fixture_local_dependencies() -> None:
    paths = [NARROW_TRIAL_PATH, BRANCHING_COMMAND_PATH, BRANCHING_SUPPORT_PATH]
    result = validate_skill_contracts(
        paths,
        toolchain_root=REPO_ROOT,
        expected_producer_identity=ProducerIdentity(
            toolchain_generation="candidate",
            toolchain_commit=TRIAL_PRODUCER_COMMIT,
        ),
        complete_catalog=True,
    )
    contracts = [_fixture_contract(path) for path in paths]

    assert result.is_valid, tuple(str(item) for item in result.diagnostics)
    assert {contract["schema"] for contract in contracts} == {"skill-contract/v1"}
    assert {
        contract["producer"]["toolchain_commit"] for contract in contracts
    } == {TRIAL_PRODUCER_COMMIT}
    assert {
        contract["producer"]["schema_version"] for contract in contracts
    } == {"skill-contract/v1"}
    assert {
        dependency
        for contract in contracts
        for dependency in contract["requires"]["mechanisms"]
    } <= {"fixture-route-inspector"}
