from __future__ import annotations

import json
import re
import tomllib
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "agents"
MANIFEST_PATH = REPO_ROOT / "codex-features.json"
REPORTING_CONTRACT = (
    REPO_ROOT / "skills/batch-runway/references/reporting-contracts-v1.md"
)
AGENT_RESULT_V2 = (
    REPO_ROOT / "skills/batch-runway/references/agent-result-contract-v2.md"
)
EXECUTION_V1 = REPO_ROOT / "skills/batch-runway/references/execution-contract-v1.md"
EXECUTION_V2 = REPO_ROOT / "skills/batch-runway/references/execution-contract-v2.md"
EXECUTE_CORE = REPO_ROOT / "skills/batch-runway/references/execute-slice-core-v1.md"
SUBAGENT_BRIEFS = REPO_ROOT / "skills/batch-runway/references/subagent-briefs.md"
BATCH_RUNWAY = REPO_ROOT / "skills/batch-runway/SKILL.md"
BATCH_REFERENCES = REPO_ROOT / "skills/batch-runway/references"


class CustomAgentContractTests(unittest.TestCase):
    def load_agent(self, name: str) -> dict[str, Any]:
        return tomllib.loads(
            (AGENTS_DIR / f"{name}.toml").read_text(encoding="utf-8")
        )

    def instructions(self, name: str) -> str:
        instructions = self.load_agent(name)["developer_instructions"]
        self.assertIsInstance(instructions, str)
        return " ".join(instructions.split())

    def test_active_agent_inventory_and_models_are_intentional(self) -> None:
        required = {
            "codebase_investigator.toml",
            "import_topology_reviewer.toml",
            "runway_reviewer.toml",
            "runway_worker.toml",
            "spark.toml",
        }
        on_disk = {path.name for path in AGENTS_DIR.glob("*.toml")}
        self.assertTrue(required.issubset(on_disk))

        expected_models = {
            "import_topology_reviewer": ("gpt-5.6-terra", "low"),
            "runway_reviewer": ("gpt-5.6-sol", "high"),
            "runway_worker": ("gpt-5.6-terra", "medium"),
            "spark": ("gpt-5.3-codex-spark", "low"),
        }
        for name, (model, effort) in expected_models.items():
            with self.subTest(agent=name):
                agent = self.load_agent(name)
                self.assertEqual(agent["name"], name)
                self.assertEqual(agent["model"], model)
                self.assertEqual(agent["model_reasoning_effort"], effort)

    def test_manifest_registers_the_complete_inventory(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        links = manifest["features"]["custom-agents"]["links"]
        registered = {Path(link["source"]).name for link in links}
        on_disk = {path.name for path in AGENTS_DIR.glob("*.toml")}

        self.assertEqual(registered, on_disk)
        self.assertTrue(all(link["source"] == link["target"] for link in links))

    def test_spark_is_bounded_support_with_explicit_edit_and_escalation_rules(self) -> None:
        instructions = self.instructions("spark")

        for required in (
            "one fast, low-risk support task",
            "explicitly requested tiny mechanical edit",
            "This is not a general implementation, investigation, or review agent",
            "Never spawn, delegate to, or wait on additional agents",
            "Speed never justifies inventing an answer",
            "Stop before editing, or stop with partial results",
            "Do not commit, update ledgers, make final workflow decisions",
            "status: answered | changed | partial | blocked | failed",
            "evidence_checked: []",
            "uncertainty: []",
            "escalation: []",
            "Every field is required",
        ):
            with self.subTest(requirement=required):
                self.assertIn(required, instructions)

    def test_worker_owns_slice_scope_lifecycle_and_failure_contract(self) -> None:
        instructions = self.instructions("runway_worker")

        for required in (
            "status: success | partial | blocked | failed",
            "Modify only files and areas allowed by the handoff",
            "Preserve unrelated dirty work",
            "Preserve behavior, interfaces, compatibility, and contracts",
            "Never spawn, delegate to, or wait on additional agents",
            "Do not review or approve your own work, commit changes, update ledgers",
            "Run focused, non-destructive validation",
            "File changes or passing focused tests alone do not establish success",
            "blockers: []",
            "Every v2 field is required",
            "Concision governs presentation, not coverage",
            "Compact Report Contract v1",
            "Do not add v2-only fields to a v1 result",
        ):
            with self.subTest(requirement=required):
                self.assertIn(required, instructions)

    def test_final_reviewer_requires_independent_current_evidence(self) -> None:
        instructions = self.instructions("runway_reviewer")

        for required in (
            "status: clean | findings | blocked",
            "Do not rely on the worker's report or specialist findings",
            "exact task-scoped diff basis",
            "stale, missing, or materially incomplete diff",
            "critical | high | medium | low",
            "evidence: direct | inference | uncertainty",
            "Treat triggered specialist findings as inputs",
            "Remain read-only",
            "spawn or wait on other agents",
            "Include every material finding regardless of report length",
            "Compact Report Contract v1",
            "Do not add the v2-only finding `evidence` field",
        ):
            with self.subTest(requirement=required):
                self.assertIn(required, instructions)

    def test_worker_and_reviewer_report_verified_cross_checkout_identity(self) -> None:
        worker = self.instructions("runway_worker")
        reviewer = self.instructions("runway_reviewer")

        for role, instructions in (("worker", worker), ("reviewer", reviewer)):
            with self.subTest(role=role):
                for required in (
                    "verified_cross_checkout_context: null",
                    "interface: cross-checkout-context/v1",
                    "generation_role",
                    "toolchain_source_root",
                    "toolchain_commit",
                    "canonical_planning_repository_root",
                    "canonical_planning_commit_before",
                    "implementation_target_root",
                    "implementation_commit_before",
                    "codex_home",
                    "canonical_state_mutation_allowed",
                    "ordinary single-root work",
                    "infer no identity from cwd",
                    "missing or mismatched context",
                ):
                    with self.subTest(role=role, requirement=required):
                        self.assertIn(required, instructions)

        self.assertIn(
            "grants no selection, acceptance, closeout, or successor authority",
            worker,
        )
        self.assertIn(
            "grants no review acceptance, commit, closeout, or successor authority",
            reviewer,
        )
        worker_requirements = (
            "independently validate the complete payload, canonical planning root, "
            "installed helper identity, generation binding, repository revisions, "
            "and intended write scope before editing",
            "Stop with `blocked` on missing or mismatched context",
            "If validation fails, return `blocked` with this field `null`",
        )
        reviewer_requirements = (
            "independently validate the complete payload, canonical planning root, "
            "installed helper identity, generation binding, and repository "
            "revisions before review",
            "Use `blocked` on missing or mismatched context",
            "If validation fails, return `blocked` with this field `null`",
        )
        for role, instructions, requirements in (
            ("worker", worker, worker_requirements),
            ("reviewer", reviewer, reviewer_requirements),
        ):
            for requirement in requirements:
                with self.subTest(role=role, normalized_requirement=requirement):
                    self.assertIn(requirement, instructions)

    def test_import_reviewer_stays_inside_triggered_project_local_lens(self) -> None:
        instructions = self.instructions("import_topology_reviewer")

        for required in (
            "status: clean | findings | blocked",
            "project-local imports, module entry behavior, path manipulation",
            "Supported direct entrypoints are documented external contracts",
            "ordinary optional third-party imports",
            "aliases, wrappers, re-exports, or fallback branches",
            "topology-only tests",
            "Do not broaden into general architecture",
            "handoff to the final `runway_reviewer`",
            "evidence: direct | inference | uncertainty",
            "Remain read-only",
        ):
            with self.subTest(requirement=required):
                self.assertIn(required, instructions)

    def test_v1_contracts_remain_compatible_and_v2_owns_current_results(self) -> None:
        reporting = REPORTING_CONTRACT.read_text(encoding="utf-8")
        agent_v2 = AGENT_RESULT_V2.read_text(encoding="utf-8")
        execution_v1 = EXECUTION_V1.read_text(encoding="utf-8")
        execution_v2 = EXECUTION_V2.read_text(encoding="utf-8")
        execute_core = EXECUTE_CORE.read_text(encoding="utf-8")
        briefs = SUBAGENT_BRIEFS.read_text(encoding="utf-8")
        batch_runway = BATCH_RUNWAY.read_text(encoding="utf-8")

        for owner in (
            "agents/runway_worker.toml",
            "agents/runway_reviewer.toml",
            "agents/import_topology_reviewer.toml",
            "agents/codebase_investigator.toml",
            "agents/spark.toml",
        ):
            with self.subTest(owner=owner):
                self.assertIn(owner, agent_v2)

        self.assertIn("Do not reinterpret", execution_v1)
        self.assertIn("`Compact Report Contract v1`", execution_v1)
        self.assertNotIn("Registered Agent Result Contract v2", execution_v1)
        self.assertIn("Worker report:", reporting)
        self.assertIn("Reviewer report:", reporting)
        self.assertIn("Registered Agent Result Contract v2", execution_v2)
        self.assertIn(
            "Existing specs that name `Standard Execution Contract v1`",
            execution_v2,
        )
        self.assertIn("Standard Execution Contract v2 for new work", batch_runway)
        self.assertIn("Result contract: <Registered Agent Result Contract v2", execute_core)
        self.assertIn("Compact Report Contract v1 when the existing spec names v1", execute_core)
        self.assertIn("registered import_topology_reviewer result contract", briefs)

    def test_worker_and_reviewer_handoffs_select_v1_or_v2_schemas(self) -> None:
        reporting = REPORTING_CONTRACT.read_text(encoding="utf-8")
        execute_core = EXECUTE_CORE.read_text(encoding="utf-8")
        briefs = SUBAGENT_BRIEFS.read_text(encoding="utf-8")
        worker = self.instructions("runway_worker")
        reviewer = self.instructions("runway_reviewer")

        for handoff in (execute_core, briefs):
            normalized_handoff = " ".join(handoff.split())
            with self.subTest(handoff=str(handoff[:40])):
                self.assertIn(
                    "Result contract: <Registered Agent Result Contract v2",
                    handoff,
                )
                self.assertIn(
                    "Compact Report Contract v1 when the existing spec names v1",
                    handoff,
                )
                self.assertIn(
                    "Stop if it conflicts with the spec",
                    normalized_handoff,
                )

        worker_v1 = reporting.split("Worker report:", 1)[1].split(
            "Reviewer report:", 1
        )[0]
        reviewer_v1 = reporting.split("Reviewer report:", 1)[1].split(
            "Commit receipt:", 1
        )[0]

        self.assertNotIn("blockers:", worker_v1)
        self.assertIn("blockers: []", worker)
        self.assertNotIn("evidence:", reviewer_v1)
        self.assertIn("evidence: direct | inference | uncertainty", reviewer)
        self.assertIn("reporting-contracts-v1.md", worker)
        self.assertIn("reporting-contracts-v1.md", reviewer)

    def test_active_workflow_references_do_not_copy_v2_agent_schemas(self) -> None:
        allowed_v1_schema_owner = REPORTING_CONTRACT.resolve()
        copied_schema_patterns = (
            re.compile(r"status:\s+success\s+files_changed:", re.DOTALL),
            re.compile(r"status:\s+clean\s+diff_basis:", re.DOTALL),
            re.compile(r"status:\s+answered\s*\|\s*changed", re.DOTALL),
        )

        for path in BATCH_REFERENCES.glob("*.md"):
            if path.resolve() == allowed_v1_schema_owner:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in copied_schema_patterns:
                with self.subTest(path=path.name, pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(text))

        active_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (BATCH_RUNWAY, EXECUTE_CORE, SUBAGENT_BRIEFS)
        )
        self.assertNotIn("12 lines or fewer", active_text)
        self.assertNotIn("10 lines or fewer", active_text)


if __name__ == "__main__":
    unittest.main()
