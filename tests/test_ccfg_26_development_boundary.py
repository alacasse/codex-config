from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTEXT = REPO_ROOT / "CONTEXT.md"
INSTRUCTIONS = REPO_ROOT / "AGENTS.md"
ADR_0003 = REPO_ROOT / "docs/adr/0003-canonical-batch-execution-state.md"
ADR_0004 = (
    REPO_ROOT / "docs/adr/0004-single-generation-command-owner-development-boundary.md"
)
PROGRAM_ROOT = REPO_ROOT / "docs/plans/programs/codex-config"
CURRENT = PROGRAM_ROOT / "CURRENT.md"
LEDGER = PROGRAM_ROOT / "LEDGER.md"
SUPERSESSION = (
    PROGRAM_ROOT / "batches/ccfg-26-execution-state-foundation/superseded.md"
)


def normalized_text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).strip()


def markdown_section(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\n(.*?)(?=^## |\Z)",
        text,
    )
    if match is None:
        raise AssertionError(f"missing {heading!r} in {path}")
    return re.sub(r"\s+", " ", match.group(1)).strip()


def ledger_row(prefix: str) -> str:
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line
    raise AssertionError(f"missing ledger row starting with {prefix!r}")


class Ccfg26DevelopmentBoundaryTests(unittest.TestCase):
    def test_current_state_has_an_empty_queue_and_planning_only_next_action(
        self,
    ) -> None:
        current = CURRENT.read_text(encoding="utf-8")

        for field in (
            "- Selected dispatch path: `None`",
            "- Active Batch Runway spec path: `None`",
            "- Queued batch path or ID: `None`",
        ):
            with self.subTest(field=field):
                self.assertIn(field, current)

        next_action = markdown_section(CURRENT, "## Next Safe Action")
        for fragment in (
            "`plan-batch CCFG-26`",
            "COR-009",
            "ADR 0004",
            "current candidate implementation seam",
            "planning-only",
            "do not implement candidate code",
            "independently reviewed and queued",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, next_action)

    def test_single_generation_boundary_is_active_in_adr_and_instructions(
        self,
    ) -> None:
        adr = normalized_text(ADR_0004)
        instructions = normalized_text(INSTRUCTIONS)

        self.assertIn("## Status Accepted.", adr)
        for fragment in (
            "development integrity boundary, not a product runtime interface",
            "One real batch is controlled by one toolchain generation",
            "stable and candidate do not import, invoke, synchronize with, or "
            "share runtime execution state with one another",
            "controller under construction does not control its own "
            "implementation batch",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment.lower(), adr.lower())
                self.assertIn(fragment.lower(), instructions.lower())

    def test_execution_state_foundation_and_adr_are_historical(self) -> None:
        adr = normalized_text(ADR_0003)
        supersession = normalized_text(SUPERSESSION)
        batch_row = ledger_row("| `ccfg-26-execution-state-foundation` |")

        self.assertTrue(SUPERSESSION.is_file())
        self.assertIn("## Status Superseded by", adr)
        self.assertIn("It is not current CCFG-26 architecture", adr)
        self.assertIn("historical evidence", supersession)
        self.assertIn("| superseded |", batch_row)
        self.assertIn("superseded.md", batch_row)

    def test_active_ccfg26_instructions_reject_the_speculative_runtime_model(
        self,
    ) -> None:
        next_action = markdown_section(CURRENT, "## Next Safe Action")
        finding_row = ledger_row("| CCFG-26. Transfer Execution")
        active_pickup = f"{next_action}\n{finding_row}".lower()

        for rejected_requirement in (
            "batch execution state",
            "automatic same-batch continuation",
            "anchored filesystem",
            "namespace substitution",
            "win32",
            "nt backend",
        ):
            with self.subTest(rejected_requirement=rejected_requirement):
                self.assertNotIn(rejected_requirement, active_pickup)

        boundary = normalized_text(ADR_0004)
        self.assertIn(
            "CCFG-26 does not assume a new canonical Batch Execution State",
            boundary,
        )
        self.assertIn(
            "late namespace substitution is not an implicit requirement",
            boundary,
        )

    def test_canonical_vocabulary_does_not_promote_rejected_runtime_concepts(
        self,
    ) -> None:
        context = CONTEXT.read_text(encoding="utf-8")

        for rejected_concept in (
            "Execution Flight",
            "Execution Attempt",
            "Flight Reservation",
            "Attempt Resolution",
            "Completed Slice Prefix",
            "Batch Execution State",
            "Execution Transition Receipt",
            "Execution Flight Result",
            "Execution Next Action",
            "Automatic Same-Batch Continuation",
        ):
            with self.subTest(rejected_concept=rejected_concept):
                self.assertNotIn(rejected_concept, context)

        for established_concept in (
            "**Batch**:",
            "**Slice**:",
            "**Planning State Diagnostic**:",
            "**Run State**:",
            "**Phase Result**:",
            "**Phase Receipt**:",
        ):
            with self.subTest(established_concept=established_concept):
                self.assertIn(established_concept, context)


if __name__ == "__main__":
    unittest.main()
