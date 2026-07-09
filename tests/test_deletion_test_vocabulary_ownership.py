from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

UNSUPPORTED_DELETION_TEST_LABELS = (
    "no-op",
    "sediment",
    "obsolete skill surface",
    "deletion-safe evidence",
)

CLEANUP_RESIDUE_STYLE_LABELS = (
    "sediment",
    "obsolete skill surface",
)


def assert_generated_text_has_supported_deletion_test_vocabulary(
    test_case: unittest.TestCase,
    text: str,
) -> None:
    compact_text = " ".join(text.split()).lower()

    for label in UNSUPPORTED_DELETION_TEST_LABELS:
        with test_case.subTest(label=label):
            if label not in compact_text:
                continue

            local_definition = (
                f"`{label}` is a local non-canonical label"
                in compact_text
                or f"{label} is a local non-canonical label" in compact_text
            )
            test_case.assertTrue(
                local_definition,
                f"{label!r} must be locally defined before generated artifacts "
                "can use it.",
            )

            if label in CLEANUP_RESIDUE_STYLE_LABELS:
                has_concrete_reason = (
                    f"`{label}` reason:" in compact_text
                    or f"{label} reason:" in compact_text
                )
                has_removal_condition_or_owner = (
                    f"`{label}` removal condition:" in compact_text
                    or f"{label} removal condition:" in compact_text
                    or f"`{label}` follow-up owner:" in compact_text
                    or f"{label} follow-up owner:" in compact_text
                )
                test_case.assertTrue(
                    has_concrete_reason,
                    f"{label!r} local labels must name a concrete reason.",
                )
                test_case.assertTrue(
                    has_removal_condition_or_owner,
                    f"{label!r} retained or deferred local labels must name a "
                    "removal condition or follow-up owner.",
                )


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

    def test_legacy_removal_consumes_deletion_test_statuses_for_decisions(
        self,
    ) -> None:
        legacy_removal = self.read("skills/legacy-removal/SKILL.md")

        self.assertIn("Deletion-test evidence vocabulary boundary", legacy_removal)
        self.assertIn(
            "consumes the\ncanonical deletion-test evidence statuses",
            legacy_removal,
        )
        self.assertIn("produced by `dead-surface-audit`", legacy_removal)
        self.assertIn("must not redefine those evidence categories", legacy_removal)

        for status in (
            "keep",
            "delete-now",
            "migrate-tests-first",
            "keep-thin-entrypoint",
            "human-contract-decision",
        ):
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", legacy_removal)

        for decision_owner in (
            "legacy compatibility decision",
            "cleanup-residue\nclassification",
            "canonical-model decision",
            "dispatch handoff material",
        ):
            with self.subTest(decision_owner=decision_owner):
                self.assertIn(decision_owner, legacy_removal)

        self.assertNotIn(
            "Deletion-test evidence vocabulary owner",
            legacy_removal,
        )

    def test_generated_artifact_consumers_require_canonical_or_local_labels(
        self,
    ) -> None:
        architecture_runway = self.read("skills/architecture-program-runway/SKILL.md")
        create_spec = self.read("skills/batch-runway/references/create-spec.md")

        for name, text in (
            ("architecture-program-runway", architecture_runway),
            ("batch-runway create-spec", create_spec),
        ):
            compact_text = " ".join(text.split())
            with self.subTest(consumer=name):
                self.assertIn(
                    "canonical deletion-test evidence statuses owned by "
                    "`dead-surface-audit`",
                    compact_text,
                )
                self.assertIn("local non-canonical labels inline", compact_text)
                self.assertRegex(
                    compact_text,
                    r"must not (?:make|invent).*unsupported",
                )
                self.assertIn("approval gates", compact_text)
                self.assertIn("cleanup decisions", compact_text)
                self.assertIn("contract-narrowing decisions", compact_text)

    def test_ccfg_like_generated_text_rejects_unsupported_deletion_categories(
        self,
    ) -> None:
        generated_dispatch = """
        ## Candidate Findings

        - Status: delete-now
          Evidence: dead-surface-audit found tests only protecting old shape.
        - Status: sediment
          Evidence: CCFG-like generated label with no local definition.
        """
        generated_runway = """
        ## Execution Ledger

        | Slice | Status | Risk class | Notes |
        |---|---|---|---|
        | 1. Remove stale alias | Pending | deletion-safe evidence | invented |
        """

        for name, text in (
            ("generated dispatch", generated_dispatch),
            ("generated runway", generated_runway),
        ):
            with self.subTest(artifact=name):
                with self.assertRaisesRegex(AssertionError, "locally defined"):
                    assert_generated_text_has_supported_deletion_test_vocabulary(
                        self,
                        text,
                    )

    def test_ccfg_like_generated_text_allows_local_noncanonical_labels(
        self,
    ) -> None:
        generated_dispatch = """
        ## Local Labels

        `sediment` is a local non-canonical label.
        `sediment` reason: groups old notes that still reference the retired
        issue template during CCFG ledger review.
        `sediment` removal condition: remove after those notes are either
        archived or rewritten under canonical cleanup-residue classifications.
        It is not a deletion-test evidence status, approval gate, cleanup
        decision, migration decision, demotion decision, or contract-narrowing
        decision.

        ## Candidate Findings

        - Status: migrate-tests-first
          Evidence: ordinary behavior tests can move to the canonical owner.
        - Label: sediment
          Evidence: local grouping label with the inline definition above.
        """

        assert_generated_text_has_supported_deletion_test_vocabulary(
            self,
            generated_dispatch,
        )

    def test_ccfg_like_generated_text_rejects_unowned_residue_labels(
        self,
    ) -> None:
        generated_dispatch = """
        ## Local Labels

        `sediment` is a local non-canonical label used only to group old notes;
        it is not a deletion-test evidence status, approval gate, cleanup
        decision, migration decision, demotion decision, or contract-narrowing
        decision.

        ## Candidate Findings

        - Label: sediment
          Evidence: local grouping label with the inline definition above.
        """

        with self.assertRaisesRegex(AssertionError, "concrete reason"):
            assert_generated_text_has_supported_deletion_test_vocabulary(
                self,
                generated_dispatch,
            )


if __name__ == "__main__":
    unittest.main()
