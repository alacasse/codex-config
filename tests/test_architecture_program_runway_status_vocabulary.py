from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills/architecture-program-runway/SKILL.md"
TEMPLATE = (
    REPO_ROOT / "skills/architecture-program-runway/references/program-ledger-template.md"
)


def section(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return match.group("body")


def normalized(markdown: str) -> str:
    return re.sub(r"\s+", " ", markdown)


class ArchitectureProgramRunwayStatusVocabularyTests(unittest.TestCase):
    def test_skill_defines_pending_as_finding_lifecycle_state(self) -> None:
        statuses = section(SKILL.read_text(encoding="utf-8"), "Ledger Statuses")

        self.assertIn(
            "`Open`: real finding, not yet assigned to selected, queued, or active "
            "batch\n  artifacts.",
            statuses,
        )
        self.assertIn(
            "`Pending`: cut or active batch work controlled by selected, queued, "
            "or active\n  batch artifacts until closeout, amendment, supersession, "
            "split, abandonment,\n  or follow-up.",
            statuses,
        )
        self.assertIn("Keep them separate from batch artifact state", statuses)

    def test_template_separates_finding_status_from_batch_queue_status(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        lifecycle = section(text, "Finding Lifecycle Statuses")
        queue_statuses = section(text, "Batch Queue Statuses")

        self.assertIn("Keep finding lifecycle status separate", lifecycle)
        self.assertIn("selected, queued, or active batch\n  artifacts.", lifecycle)
        self.assertIn("amendment, supersession, split, abandonment,\n  or follow-up", lifecycle)
        self.assertNotIn("`Pending`", queue_statuses)

    def test_pending_scope_changes_must_be_explicit(self) -> None:
        skill_statuses = section(SKILL.read_text(encoding="utf-8"), "Ledger Statuses")
        template_lifecycle = section(
            TEMPLATE.read_text(encoding="utf-8"), "Finding Lifecycle Statuses"
        )

        for source_name, text in (
            ("skill", skill_statuses),
            ("template", template_lifecycle),
        ):
            with self.subTest(source=source_name):
                self.assertIn(
                    "Do not widen or rewrite a `Pending` finding through ordinary "
                    "source-ledger\nedits",
                    text,
                )
                self.assertIn(
                    "Allowed scope changes must be explicit: closeout evidence, "
                    "supersession,\nabandonment, split, a named amendment, or a new "
                    "follow-up finding.",
                    text,
                )
                self.assertIn(
                    "record the amendment or follow-up before continuing; do not hide "
                    "the change in\nnarrative notes.",
                    text,
                )

    def test_selected_dispatch_requires_split_block_or_narrow_rationale(
        self,
    ) -> None:
        guard = section(SKILL.read_text(encoding="utf-8"), "Vague Row Selection Guard")
        compact_guard = normalized(guard)

        self.assertIn("Before writing a selected dispatch", guard)
        self.assertIn(
            "one bounded batch with clear owner seam, risk class, acceptance "
            "criteria, and stop conditions",
            compact_guard,
        )
        self.assertIn("Do not let a vague or mixed-risk row silently expand", compact_guard)
        self.assertIn(
            "choose one of these outcomes before creating `dispatch.md`", compact_guard
        )
        self.assertIn("Split the row into smaller program findings", guard)
        self.assertIn("Block the row when a decision, owner, risk class", guard)
        self.assertIn(
            "Narrow the selected dispatch to characterization-only or evidence-only",
            guard,
        )
        self.assertIn(
            "Record the split, block, or narrow-scope rationale in the program "
            "ledger and selected dispatch packet.",
            compact_guard,
        )

    def test_vague_row_guard_names_ccfg11_like_mixed_risk_expansion(
        self,
    ) -> None:
        guard = section(SKILL.read_text(encoding="utf-8"), "Vague Row Selection Guard")
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

        compact_guard = normalized(guard)

        self.assertIn("evidence gathering, classification, decisions", compact_guard)
        self.assertIn("destructive cleanup, migration, demotion", compact_guard)
        self.assertIn(
            "decision, owner, risk class, acceptance boundary", compact_guard
        )
        self.assertIn(
            "Newly discovered destructive, migration, demotion, or "
            "contract-narrowing work must become explicit follow-up ledger work",
            compact_guard,
        )


if __name__ == "__main__":
    unittest.main()
