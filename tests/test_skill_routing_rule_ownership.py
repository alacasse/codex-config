from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts.skill_contract import validate_skill_contracts


REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTING_CONTRACT = REPO_ROOT / "docs/skill-routing-contract.md"
RUNWAY = (
    REPO_ROOT
    / "docs/plans/programs/codex-config/batches/"
    "ccfg-8-ledger-dispatch-rule-dedupe/runway.md"
)
ADD_TO_LEDGER = REPO_ROOT / "skills/add-to-ledger/SKILL.md"
PLAN_BATCH = REPO_ROOT / "skills/plan-batch/SKILL.md"
WORK_BATCH = REPO_ROOT / "skills/work-batch/SKILL.md"
ARCHITECTURE_PROGRAM_RUNWAY = (
    REPO_ROOT / "skills/architecture-program-runway/SKILL.md"
)
BATCH_RUNWAY = REPO_ROOT / "skills/batch-runway/SKILL.md"
PLANNING_STATE = REPO_ROOT / "skills/planning-state/SKILL.md"
PLANNING_ARTIFACTS = REPO_ROOT / "skills/planning-artifacts/SKILL.md"
ARCHITECTURE_PROGRAM_AGENT = (
    REPO_ROOT / "skills/architecture-program-runway/agents/openai.yaml"
)
ARCHITECTURE_PROGRAM_TEMPLATE = (
    REPO_ROOT
    / "skills/architecture-program-runway/references/program-ledger-template.md"
)


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


def section(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return match.group("body")


def table_rows(markdown: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for line in markdown.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] in {"Repeated rule category", "---"}:
            continue
        if len(cells) != 3:
            raise AssertionError(f"unexpected table row shape: {line}")
        rows[cells[0]] = (cells[1], cells[2])
    return rows


class SkillRoutingRuleOwnershipTests(unittest.TestCase):
    def test_runway_names_one_owner_for_each_repeated_rule_category(self) -> None:
        rows = table_rows(
            section(RUNWAY.read_text(encoding="utf-8"), "Rule Ownership Map")
        )

        expected_rows = {
            "Command routing and human-facing stop points": (
                "docs/skill-routing-contract.md"
            ),
            "Ledger and external-source intake": "add-to-ledger",
            (
                "Planning State Diagnostic ordering, target-policy checks, and "
                "projection routing"
            ): "planning-state",
            (
                "Planning Artifact Layout v1 placement, naming, active-state shape, "
                "and archive vocabulary"
            ): "planning-artifacts",
            (
                "Program dispatch, selected/queued/active batch artifact state, "
                "program queue mechanics, and finding lifecycle status"
            ): "architecture-program-runway",
            (
                "Concrete runway spec, slice ledger, validation/review loop, "
                "completed-slice archive, and commit receipt mechanics"
            ): "batch-runway",
            "Same-batch closeout reconciliation mechanics": "architecture-program-runway",
        }

        self.assertEqual(set(expected_rows), set(rows))
        for category, owner in expected_rows.items():
            with self.subTest(category=category):
                owner_cell, _boundary_cell = rows[category]
                self.assertEqual(f"`{owner}`", owner_cell)

        command_boundary = rows["Command routing and human-facing stop points"][1]
        self.assertIn("`add-to-ledger`", command_boundary)
        self.assertIn("`plan-batch`", command_boundary)
        self.assertIn("`work-batch`", command_boundary)

    def test_command_owner_skills_keep_human_facing_routing_decisions(self) -> None:
        routing = normalized(ROUTING_CONTRACT)
        plan_batch = normalized(PLAN_BATCH)
        work_batch = normalized(WORK_BATCH)
        add_to_ledger_result = validate_skill_contracts(
            (ADD_TO_LEDGER,),
            toolchain_root=REPO_ROOT,
            complete_catalog=False,
        )

        self.assertIn(
            "command-owner skill that turns fresh user-provided work/finding text",
            routing,
        )
        self.assertTrue(
            add_to_ledger_result.is_valid,
            "\n".join(
                str(diagnostic)
                for diagnostic in add_to_ledger_result.diagnostics
            ),
        )
        self.assertEqual(len(add_to_ledger_result.contracts), 1)
        add_to_ledger = add_to_ledger_result.contracts[0].contract
        self.assertEqual(add_to_ledger["identity"]["name"], "add-to-ledger")
        self.assertIn("intake_eligibility", add_to_ledger["owns"]["decisions"])
        self.assertIn("atomic_planning_finding_mutation", add_to_ledger["writes"])
        self.assertTrue(
            {
                "batch_selection",
                "dispatch_creation",
                "runway_creation",
                "implementation",
            }
            <= set(add_to_ledger["forbids"])
        )

        self.assertIn("owns the human \"create the next specs batch\" decision", routing)
        self.assertIn("Command Contract", plan_batch)
        self.assertIn("stop-before-implementation boundary", plan_batch)
        self.assertIn("If useful work exists outside the ledger", plan_batch)

        self.assertIn("Execute the current queued or active batch runway", routing)
        self.assertIn(
            "This skill owns the user's request to execute the current batch",
            work_batch,
        )
        self.assertIn("must not select a new batch", work_batch)
        self.assertIn(
            "Do not select, dispatch, refresh, create, or prepare successor work",
            work_batch,
        )

    def test_plan_batch_blocks_direct_planning_from_ccfg11_like_vague_rows(
        self,
    ) -> None:
        plan_batch = normalized(PLAN_BATCH)
        ccfg11_like_shape = (
            "evidence gathering plus classification plus decision or destructive "
            "cleanup in one vague row"
        )

        for signal in (
            "evidence gathering",
            "classification",
            "decision",
            "destructive cleanup",
            "vague row",
        ):
            with self.subTest(signal=signal):
                self.assertIn(signal, ccfg11_like_shape)

        self.assertIn(
            "Requested ledger rows are suitable for direct planning only when the "
            "row is precise enough for one bounded selected dispatch.",
            plan_batch,
        )
        self.assertIn(
            "A row is not suitable when it mixes evidence gathering, "
            "classification, decisions, destructive cleanup, migration, demotion, "
            "or contract narrowing without clear owner, risk, and acceptance "
            "boundaries.",
            plan_batch,
        )
        self.assertIn(
            "`plan-batch` must split, block, or narrow that scope before any "
            "concrete runway is queued.",
            plan_batch,
        )
        self.assertNotIn("route through `architecture-program-runway`", plan_batch)

    def test_runtime_and_support_skills_keep_procedure_ownership(self) -> None:
        architecture_program_runway = normalized(ARCHITECTURE_PROGRAM_RUNWAY)
        batch_runway = normalized(BATCH_RUNWAY)
        planning_state = normalized(PLANNING_STATE)
        planning_artifacts = normalized(PLANNING_ARTIFACTS)

        self.assertIn(
            "This skill manages program-level state: durable ledger, finding grouping, batch queue, selected dispatch packet, and closeout reconciliation.",
            architecture_program_runway,
        )
        self.assertIn(
            "owns the selected dispatch packet and the batch queue state",
            architecture_program_runway,
        )
        self.assertIn(
            "If invoked by `work-batch`, this closeout is limited to the just-completed batch",
            architecture_program_runway,
        )

        self.assertIn("Batch Runway owns concrete execution state", batch_runway)
        self.assertIn("concrete runway spec creation, execution orchestration", batch_runway)

        self.assertIn("Planning State Diagnostic", planning_state)
        self.assertIn(
            "This skill validates and reports state and target policy",
            planning_state,
        )
        self.assertIn("does not redefine artifact layout", planning_state)

        self.assertIn("defines placement, naming, file shape", planning_artifacts)
        self.assertIn("Planning Artifact Layout v1", planning_artifacts)
        self.assertIn("does not replace its pickup diagnostic", planning_artifacts)

    def test_architecture_program_excludes_intake_and_keeps_program_state(
        self,
    ) -> None:
        architecture = normalized(ARCHITECTURE_PROGRAM_RUNWAY)
        agent = normalized(ARCHITECTURE_PROGRAM_AGENT)
        template = normalized(ARCHITECTURE_PROGRAM_TEMPLATE)
        routing = normalized(ROUTING_CONTRACT)

        self.assertNotIn("`intake-findings`", architecture)
        self.assertNotIn("One-shot intake allowed", template)
        self.assertNotIn("$add-to-ledger", agent)
        self.assertIn("`planning-contracts` atomic store mechanism", routing)
        self.assertIn("selected dispatch packet", architecture)
        self.assertIn("queue state", architecture)
        self.assertIn("same_batch_closeout_reconciliation", architecture)
        self.assertIn("route that work through `add-to-ledger`", architecture)

    def test_finding_lifecycle_status_stays_separate_from_batch_artifact_state(
        self,
    ) -> None:
        architecture_program_runway = ARCHITECTURE_PROGRAM_RUNWAY.read_text(
            encoding="utf-8"
        )
        ledger_statuses = section(architecture_program_runway, "Ledger Statuses")
        owner_map = section(RUNWAY.read_text(encoding="utf-8"), "Rule Ownership Map")

        self.assertIn("Keep them separate from batch artifact state", ledger_statuses)
        self.assertIn("selected, queued, or active batch\n  artifacts", ledger_statuses)
        self.assertIn("finding lifecycle status", owner_map)
        self.assertIn("selected/queued/active batch artifact state", owner_map)


if __name__ == "__main__":
    unittest.main()
