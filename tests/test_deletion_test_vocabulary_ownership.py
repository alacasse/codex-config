from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class DeletionTestVocabularyOwnershipTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_dead_surface_audit_owns_only_deletion_test_evidence_vocabulary(
        self,
    ) -> None:
        dead_surface = self.read("skills/dead-surface-audit/SKILL.md")

        self.assertIn("Deletion-test evidence vocabulary owner", dead_surface)
        self.assertIn("evidence producer only", dead_surface)
        self.assertIn("project-neutral evidence statuses", dead_surface)

        for status in (
            "keep",
            "delete-now",
            "migrate-tests-first",
            "keep-thin-entrypoint",
            "human-contract-decision",
        ):
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", dead_surface)

        for label in (
            "no-op",
            "sediment",
            "obsolete skill surface",
            "deletion-safe evidence",
        ):
            with self.subTest(label=label):
                self.assertIn(f"`{label}`", dead_surface)

        self.assertRegex(
            dead_surface,
            r"non-canonical\s+deletion-test evidence categories",
        )
        self.assertIn("unless a specific local artifact explicitly", dead_surface)
        self.assertIn("Do not use this vocabulary ownership", dead_surface)
        self.assertIn("queue batches", dead_surface)
        self.assertIn("execute cleanup", dead_surface)
        self.assertRegex(dead_surface, r"approve\s+deletions")


if __name__ == "__main__":
    unittest.main()
