from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class BatchLifecycleGuardTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def normalized(self, relative_path: str) -> str:
        return " ".join(self.read(relative_path).split())

    def test_work_batch_preserves_queued_plan_batch_output_without_closeout(
        self,
    ) -> None:
        text = self.normalized("skills/work-batch/SKILL.md")

        self.assertIn(
            "A queued runway produced by `plan-batch` is expected live state",
            text,
        )
        self.assertIn("not stale or accidental residue", text)
        self.assertIn(
            "Same-batch program reconciliation requires concrete execution "
            "closeout evidence.",
            text,
        )
        self.assertIn("preserve the queued runway", text)
        self.assertIn("explicitly asks to cancel or abandon it", text)
        self.assertIn("documented blocker makes execution unsafe", text)

    def test_architecture_program_closeout_rejects_dispatch_runway_only_evidence(
        self,
    ) -> None:
        text = self.normalized("skills/architecture-program-runway/SKILL.md")

        self.assertIn(
            "`closeout-runway` must not clear a queued dispatch/runway before "
            "execution",
            text,
        )
        self.assertIn(
            "unless the user explicitly requests cancellation or abandonment",
            text,
        )
        self.assertIn(
            "closeout evidence documents a blocker that makes execution unsafe",
            text,
        )
        self.assertIn(
            "A dispatch/runway pair alone is not closeout evidence.",
            text,
        )

    def test_workflow_guide_routes_queued_runway_to_work_batch(self) -> None:
        text = self.normalized("docs/workflow-guide.md")

        self.assertIn("`plan-batch` normally leaves a queued runway", text)
        self.assertIn("That queued state is not residue", text)
        self.assertIn("consume it with `work-batch`", text)
        self.assertIn(
            "without explicit cancellation or documented blocker evidence",
            text,
        )


if __name__ == "__main__":
    unittest.main()
