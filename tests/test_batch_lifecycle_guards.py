from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXECUTION_CONTRACT = REPO_ROOT / "skills/batch-runway/references/execution-contract-v1.md"
FINALIZE_BATCH = REPO_ROOT / "skills/batch-runway/references/finalize-batch-v1.md"
LEDGER_RETENTION = REPO_ROOT / "skills/batch-runway/references/ledger-retention-v1.md"
CROSS_CHECKOUT_CONTEXT = (
    REPO_ROOT / "skills/batch-runway/references/cross-checkout-context-v1.md"
)


class BatchLifecycleGuardTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def normalized(self, relative_path: str) -> str:
        return " ".join(self.read(relative_path).split())

    def normalized_path(self, path: Path) -> str:
        return " ".join(path.read_text(encoding="utf-8").split())

    def test_active_batch_artifacts_do_not_keep_unresolved_commit_placeholders(
        self,
    ) -> None:
        banned_placeholders = (
            "pending coordinator " "commit",
            "commit " "pending",
            "pending commit " "receipt",
            "Coordinator review " "pending",
        )
        active_batch_root = REPO_ROOT / "docs/plans/programs"
        artifact_names = {"runway.md", "closeout.md", "completed-slices.md"}

        violations: list[str] = []
        for path in active_batch_root.glob("*/batches/**/*"):
            if not path.is_file() or path.name not in artifact_names:
                continue

            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                for placeholder in banned_placeholders:
                    if placeholder in line:
                        relative = path.relative_to(REPO_ROOT)
                        violations.append(f"{relative}:{line_number}: {placeholder}")

        self.assertEqual([], violations)

    def test_batch_runway_documents_final_closeout_commit_placeholder_policy(
        self,
    ) -> None:
        execution_contract = self.normalized_path(EXECUTION_CONTRACT)
        finalize_batch = self.normalized_path(FINALIZE_BATCH)
        ledger_retention = self.normalized_path(LEDGER_RETENTION)

        self.assertIn("Ordinary slice commits record exact commit hashes", execution_contract)
        self.assertIn("self-referential final closeout commit", execution_contract)
        self.assertIn("`this closeout commit`", execution_contract)

        self.assertIn("stale-placeholder scan", finalize_batch)
        self.assertIn("pending coordinator reviews", finalize_batch)
        self.assertIn("`this closeout commit`", finalize_batch)

        self.assertIn("must not retain unresolved operational placeholders", ledger_retention)
        self.assertIn("`this closeout commit`", ledger_retention)

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

    def test_cross_checkout_contract_defines_four_lifecycle_concepts(self) -> None:
        text = " ".join(
            CROSS_CHECKOUT_CONTEXT.read_text(encoding="utf-8").split()
        )

        self.assertIn(
            "A **planning snapshot** is the complete validated plan-time payload "
            "and canonical planning root persisted in the queued runway.",
            text,
        )
        self.assertIn(
            "**Startup reconciliation** is the workflow decision made once before "
            "`work-batch` consumes queued work.",
            text,
        )
        self.assertIn(
            "A **live execution lease** is a short-lived complete context prepared "
            "from live repository facts and accepted by strict context parsing.",
            text,
        )
        self.assertIn(
            "An **execution receipt** is durable, immutable evidence of an "
            "accepted action.",
            text,
        )
        self.assertIn(
            "must be exact for one worker or reviewer handoff",
            text,
        )
        self.assertIn(
            "Before every worker or final-reviewer delegation, the execution "
            "coordinator must revalidate the payload with the installed helper",
            text,
        )
        self.assertIn(
            "The coordinator must reject a missing, null, or mismatched identity",
            text,
        )
        self.assertIn(
            "Repository movement invalidates the lease rather than changing the "
            "planning snapshot.",
            text,
        )

    def test_cross_checkout_planning_producers_persist_immutable_snapshots(
        self,
    ) -> None:
        producer_paths = (
            "skills/plan-batch/SKILL.md",
            "skills/batch-runway/references/create-spec.md",
        )

        for relative_path in producer_paths:
            text = self.normalized(relative_path)
            with self.subTest(path=relative_path):
                self.assertIn("cross-checkout-context-v1.md", text)
                self.assertIn(
                    "complete validated plan-time payload and canonical planning "
                    "root",
                    text,
                )
                self.assertIn("**planning snapshot**", text)
                self.assertIn("immutable historical planning evidence", text)
                self.assertIn("not a live execution lease", text)
                self.assertIn("future live `HEAD`", text)
                self.assertIn("same selected scope", text)
                self.assertIn("fresh live lease", text)
                self.assertIn("do not hand-edit its revisions", text.lower())
                self.assertIn("commit that contains", text)

        create_spec = self.normalized(
            "skills/batch-runway/references/create-spec.md"
        )
        self.assertIn("required planning-snapshot section", create_spec)

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
