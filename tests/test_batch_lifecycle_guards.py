from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXECUTION_CONTRACT = REPO_ROOT / "skills/batch-runway/references/execution-contract-v1.md"
FINALIZE_BATCH = REPO_ROOT / "skills/batch-runway/references/finalize-batch-v1.md"
LEDGER_RETENTION = REPO_ROOT / "skills/batch-runway/references/ledger-retention-v1.md"
CROSS_CHECKOUT_CONTEXT = (
    REPO_ROOT / "skills/batch-runway/references/cross-checkout-context-v1.md"
)
WORK_BATCH = REPO_ROOT / "skills/work-batch/SKILL.md"
EXECUTE_SPEC = REPO_ROOT / "skills/batch-runway/references/execute-spec.md"
EXECUTE_SLICE_CORE = (
    REPO_ROOT / "skills/batch-runway/references/execute-slice-core-v1.md"
)
EXECUTE_RECOVERY = (
    REPO_ROOT / "skills/batch-runway/references/execute-recovery-v1.md"
)


class BatchLifecycleGuardTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def normalized(self, relative_path: str) -> str:
        return " ".join(self.read(relative_path).split())

    def normalized_path(self, path: Path) -> str:
        return " ".join(path.read_text(encoding="utf-8").split())

    def markdown_section(self, path: Path, heading: str) -> str:
        text = path.read_text(encoding="utf-8")
        marker = f"## {heading}\n"
        section_start = text.index(marker) + len(marker)
        next_heading = re.search(r"^## ", text[section_start:], flags=re.MULTILINE)
        section_end = (
            section_start + next_heading.start() if next_heading is not None else len(text)
        )
        return text[section_start:section_end]

    def normalized_section(self, path: Path, heading: str) -> str:
        return " ".join(self.markdown_section(path, heading).split())

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
            "Before every worker or reviewer delegation, the execution "
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

    def test_cross_checkout_startup_has_exactly_three_classifications(self) -> None:
        expected = {
            "expected-queue-establishment",
            "compatible-between-flight-change",
            "conflicting-between-flight-change",
        }
        classification_sections = (
            (WORK_BATCH, "Cross-Checkout Startup Reconciliation"),
            (CROSS_CHECKOUT_CONTEXT, "Startup Classifications And Controlled Paths"),
        )

        for path, heading in classification_sections:
            section = self.markdown_section(path, heading)
            found = set(
                re.findall(r"^\s*- `([^`]+)`", section, flags=re.MULTILINE)
            )
            with self.subTest(path=path.relative_to(REPO_ROOT), heading=heading):
                self.assertEqual(expected, found)

        work_batch = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Startup Reconciliation",
        )
        self.assertIn("`work-batch` owns the normal queued-to-executing transition", work_batch)
        self.assertIn("before generic unexpected-movement recovery", work_batch)
        self.assertIn(
            "the same runway is still the only queued or active batch",
            work_batch,
        )
        self.assertIn(
            "`expected-queue-establishment` when revisions are unchanged",
            work_batch,
        )
        self.assertIn("there is no fourth or implicit fallback", work_batch)

    def test_unchanged_head_uncommitted_queue_establishment_is_narrowly_expected(
        self,
    ) -> None:
        startup = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Startup Reconciliation",
        )
        expected_case = startup[
            startup.index("- `expected-queue-establishment`") : startup.index(
                "- `compatible-between-flight-change`"
            )
        ]
        conflicting_case = startup[
            startup.index("- `conflicting-between-flight-change`") : startup.index(
                "Derive controlled paths"
            )
        ]

        for requirement in (
            "unchanged-HEAD uncommitted queue establishment",
            "Planning State Diagnostic",
            "same runway as the only queued or active batch",
            "review of the complete dirty diff",
            "canonical active-state path",
            "same current batch's dispatch or runway",
            "selected scope",
            "planning snapshot facts",
            "source finding and source note",
            "acceptance, validation and stop contract",
            "every other controlled owner",
            "match their accepted basis",
        ):
            self.assertIn(requirement, expected_case)

        for conflict in (
            "arbitrary dirty controlled path",
            "untracked source path that is not one of the allowed queue artifacts",
            "pending implementation allowlist overlap",
            "helper or contract owner edit",
            "evidence that cannot be classified confidently",
            "stops before delegation",
        ):
            self.assertIn(conflict, conflicting_case)

        self.assertIn(
            "Use the Planning State Diagnostic to confirm that `current` and "
            "`validate` are safe to consume",
            startup,
        )
        self.assertIn(
            "The uncommitted queue exception is content-scoped, not a blanket "
            "exemption for controlled paths.",
            startup,
        )
        self.assertIn(
            "stop if any non-queue content or unknown path is present",
            startup,
        )

    def test_startup_reconciliation_derives_project_neutral_controlled_paths(
        self,
    ) -> None:
        work_batch = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Startup Reconciliation",
        )

        capture_facts = (
            "declared repository roots, branches, live revisions, and worktree status",
            "installed helper path, active Codex home, and generation role",
            "complete intervening commit range and its changed paths",
        )
        for fact in capture_facts:
            self.assertIn(fact, work_batch)

        controlled_sources = (
            "canonical active-state paths resolved by the Planning State Diagnostic",
            "queued runway and same batch's dispatch",
            "source finding and source note",
            "acceptance, validation, and stop contract",
            "manifest and its declared contract owners",
            "resolved installed helper owner",
            "declared roots and baselines",
            "pending slice allowlist",
        )
        for source in controlled_sources:
            self.assertIn(source, work_batch)

        reusable_surfaces = (
            WORK_BATCH,
            CROSS_CHECKOUT_CONTEXT,
            EXECUTE_SPEC,
            EXECUTE_SLICE_CORE,
            EXECUTE_RECOVERY,
        )
        project_specific_values = (
            "/home/",
            "CCFG-",
            "codex-config",
            ".venv",
            "UV_CACHE_DIR",
        )
        for path in reusable_surfaces:
            text = path.read_text(encoding="utf-8")
            for value in project_specific_values:
                with self.subTest(path=path.relative_to(REPO_ROOT), value=value):
                    self.assertNotIn(value, text)

    def test_cross_checkout_execution_renews_live_leases_and_receipts(self) -> None:
        startup = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Startup Reconciliation",
        )
        strict_execution = self.normalized_section(
            WORK_BATCH,
            "Explicit Strict Cross-Checkout Execution",
        )
        helper_bootstrap = self.normalized_section(
            CROSS_CHECKOUT_CONTEXT,
            "Stable Helper Bootstrap",
        )

        accepted_route = re.search(
            r"After (?P<classifications>.+?) is accepted, call the installed "
            r"helper's `prepare_cross_checkout_context_refresh\(\.\.\.\)`",
            startup,
        )
        if accepted_route is None:
            self.fail("startup reconciliation does not route accepted classifications")
        self.assertEqual(
            1,
            startup.count("prepare_cross_checkout_context_refresh(...)"),
        )
        accepted_classifications = set(
            re.findall(r"`([^`]+)`", accepted_route.group("classifications"))
        )
        self.assertEqual(
            {
                "expected-queue-establishment",
                "compatible-between-flight-change",
            },
            accepted_classifications,
        )
        self.assertIn(
            "A conflicting classification, refresh failure, or scope failure "
            "stops before delegation",
            startup,
        )
        self.assertIn("validate_write_scope(...)` separately", startup)
        self.assertIn(
            "Immediately before every worker and reviewer delegation, call "
            "`prepare_cross_checkout_context_refresh(...)` again",
            strict_execution,
        )
        self.assertIn(
            "newly prepared exact live execution lease",
            strict_execution,
        )
        self.assertIn(
            "do not strict-parse the historical planning snapshot before "
            "reconciliation",
            helper_bootstrap,
        )
        self.assertIn("Never pass the planning snapshot as the handoff lease", strict_execution)
        self.assertIn(
            "The helper supplies planned and live facts; it does not choose the "
            "classification or accept movement.",
            startup,
        )

        startup_evidence = startup[startup.index("Record compact startup") :]
        for fact in (
            "runway path",
            "classification",
            "planned and accepted live stable and implementation revisions",
            "reviewed commit ranges",
            "changed-path basis",
        ):
            self.assertIn(fact, startup_evidence)

        self.assertIn(
            "execution receipt that identifies the exact live lease and validated "
            "scope used for that handoff",
            strict_execution,
        )
        self.assertIn(
            "The receipt must not use planning-snapshot revisions as though they "
            "were live action evidence.",
            strict_execution,
        )

    def test_cross_checkout_recovery_starts_after_normal_reconciliation(self) -> None:
        execute_spec = self.normalized_section(
            EXECUTE_SPEC,
            "Cross-Checkout Startup Routing",
        )
        recovery = self.normalized_section(
            EXECUTE_RECOVERY,
            "Cross-Checkout Movement Boundary",
        )

        self.assertIn(
            "route through `work-batch` startup reconciliation before strict "
            "delegation validation and before unexpected-movement recovery",
            execute_spec,
        )
        self.assertIn("is not, by itself, a recovery trigger", recovery)
        accepted_recovery_route = recovery[
            recovery.index("Movement accepted as") : recovery.index(
                "without an orchestration anomaly"
            )
        ]
        self.assertEqual(
            {
                "expected-queue-establishment",
                "compatible-between-flight-change",
            },
            set(re.findall(r"`([^`]+)`", accepted_recovery_route)),
        )
        self.assertEqual(1, recovery.count("without an orchestration anomaly"))
        self.assertIn(
            "If the reviewed startup evidence cannot be classified confidently, "
            "record `conflicting-between-flight-change`",
            recovery,
        )
        self.assertIn(
            "Use this recovery lane only to freeze delegation, preserve the "
            "evidence, and report the amendment or replanning blocker.",
            recovery,
        )
        self.assertIn("Recovery cannot accept the movement or replace the queued runway", recovery)
        self.assertIn("moves between lease preparation and handoff", recovery)
        self.assertIn("No post-lease movement may reach delegation on the old lease", recovery)

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
