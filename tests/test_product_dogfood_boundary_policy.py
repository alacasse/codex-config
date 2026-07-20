from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "AGENTS.md"
CONTEXT = REPO_ROOT / "CONTEXT.md"
PLAN_BATCH = REPO_ROOT / "skills/plan-batch/SKILL.md"
PLANNING_ARTIFACTS = REPO_ROOT / "skills/planning-artifacts/SKILL.md"
ROOT_CURRENT = REPO_ROOT / "docs/plans/CURRENT.md"
PROGRAM_CURRENT = REPO_ROOT / "docs/plans/programs/codex-config/CURRENT.md"
PROGRAM_LEDGER = REPO_ROOT / "docs/plans/programs/codex-config/LEDGER.md"
ADR_0003 = REPO_ROOT / "docs/adr/0003-canonical-batch-execution-state.md"
ADR_0004 = REPO_ROOT / "docs/adr/0004-extraction-first-batch-local-execution.md"
RESET_DIRECTION = (
    REPO_ROOT
    / "docs/plans/programs/codex-config/findings/ccfg-26-product-dogfood-reset.md"
)
SUPERSEDED_FOUNDATION = (
    REPO_ROOT
    / "docs/plans/programs/codex-config/batches/"
    "ccfg-26-execution-state-foundation/superseded.md"
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def queued_runway_path() -> Path | None:
    current = PROGRAM_CURRENT.read_text(encoding="utf-8")
    match = re.search(
        r"^- Queued batch path or ID:\s*`?([^`\n]+)`?\s*$",
        current,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError(
            "program CURRENT.md must declare Queued batch path or ID"
        )
    value = match.group(1).strip()
    if value.lower() in {"none", "none selected"}:
        return None
    return REPO_ROOT / value


class ProductDogfoodBoundaryPolicyTests(unittest.TestCase):
    def test_global_instructions_define_the_one_way_dependency(self) -> None:
        instructions = normalized(AGENTS)

        for required in (
            "Product and dogfood separation",
            "A dogfood adapter may depend on the product",
            "the product must not depend on the adapter",
            "Product Boundary",
            "Dogfood Boundary",
            "Threat Model",
            "Guarantee Feasibility",
            (
                "Uncommitted work preserved under user control is not accepted "
                "implementation"
            ),
        ):
            with self.subTest(required=required):
                self.assertIn(required, instructions)

    def test_canonical_context_uses_product_terms_not_superseded_flight_terms(
        self,
    ) -> None:
        context = normalized(CONTEXT)

        for required in (
            "Product Boundary",
            "Dogfood Adapter",
            "Batch-Local Runtime State",
            "Threat Model",
            "Guarantee Feasibility",
            "Preserved User Worktree",
        ):
            with self.subTest(required=required):
                self.assertIn(required, context)

        for superseded_term in (
            "Execution Flight",
            "Flight Reservation",
            "Execution Transition Receipt",
            "Automatic Same-Batch Continuation",
        ):
            with self.subTest(superseded_term=superseded_term):
                self.assertNotIn(superseded_term, context)

    def test_plan_batch_requires_concrete_boundary_and_feasibility_sections(
        self,
    ) -> None:
        contract = normalized(PLAN_BATCH)

        for required in (
            "Product, Dogfood, Threat, And Feasibility Gate",
            "Product Boundary",
            "Dogfood Boundary",
            "Threat Model",
            "Guarantee Feasibility",
            "implementation primitive or bounded dependency",
            "small disposable feasibility experiment",
            "temporary path is persisted as durable project or batch state",
            "preserved uncommitted work is treated as accepted implementation",
        ):
            with self.subTest(required=required):
                self.assertIn(required, contract)

    def test_layout_defaults_small_batch_state_to_the_batch_directory(
        self,
    ) -> None:
        layout = normalized(PLANNING_ARTIFACTS)
        root_current = normalized(ROOT_CURRENT)

        for required in (
            "batch_runtime_policy",
            "normally `batch-local`",
            ".runtime/",
            "run_artifact_root`: optional",
            "not a mandatory second root for one batch's canonical state",
            "Temporary directories are for tests and disposable acceptance runs",
        ):
            with self.subTest(required=required):
                self.assertIn(required, layout)

        self.assertIn("Batch runtime policy: `batch-local`", root_current)

    def test_ccfg26_reset_is_canonical_and_old_design_is_historical(
        self,
    ) -> None:
        current = normalized(PROGRAM_CURRENT)
        ledger = normalized(PROGRAM_LEDGER)
        old_adr = normalized(ADR_0003)
        new_adr = normalized(ADR_0004)
        reset = normalized(RESET_DIRECTION)
        superseded = normalized(SUPERSEDED_FOUNDATION)

        self.assertIn("Queued batch path or ID: `None`", current)
        self.assertIn("ccfg-26-execution-state-foundation is superseded", current)
        self.assertIn("CCFG-26: `Ready`", ledger)
        self.assertIn("Queued batch: `None`", ledger)
        self.assertIn("Superseded", old_adr)
        self.assertIn("supersedes ADR 0003", new_adr)
        self.assertIn("preserved under the user's control", reset)
        self.assertIn(
            "not executable, resumable, amendable, closable",
            superseded,
        )

        for forbidden in ("/tmp/tmp.", "Run artifact location: `/tmp"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, current)
                self.assertNotIn(forbidden, ledger)

    def test_future_queued_migration_runway_must_include_all_four_boundaries(
        self,
    ) -> None:
        runway_path = queued_runway_path()
        if runway_path is None:
            return

        runway = runway_path.read_text(encoding="utf-8")
        normalized_runway = " ".join(runway.split())
        migration_plan = bool(
            re.search(
                r"Batch kind(?: And Slice Risk Contract)?:.*migration",
                normalized_runway,
                re.IGNORECASE,
            )
        )
        if not migration_plan:
            return

        for heading in (
            "## Product Boundary",
            "## Dogfood Boundary",
            "## Threat Model",
            "## Guarantee Feasibility",
        ):
            with self.subTest(runway=str(runway_path), heading=heading):
                self.assertIn(heading, runway)


if __name__ == "__main__":
    unittest.main()
