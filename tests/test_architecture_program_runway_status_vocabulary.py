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


if __name__ == "__main__":
    unittest.main()
