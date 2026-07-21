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
PLAN_BATCH = REPO_ROOT / "skills/plan-batch/SKILL.md"
ARCHITECTURE_PROGRAM_RUNWAY = (
    REPO_ROOT / "skills/architecture-program-runway/SKILL.md"
)
STATE_FIXTURES = (
    REPO_ROOT / "skills/planning-state/references/state-fixtures.md"
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

    def test_cross_checkout_contract_keeps_the_narrow_safety_boundary(self) -> None:
        text = " ".join(
            CROSS_CHECKOUT_CONTEXT.read_text(encoding="utf-8").split()
        )

        self.assertIn(
            "A **planning snapshot** is the complete validated plan-time payload "
            "and canonical planning root persisted in the queued runway.",
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
            "Immediately before the first worker or reviewer delegation, the "
            "execution coordinator must run the ready/blocked preflight",
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
        self.assertIn("preflight_cross_checkout_live_lease(...)`", text)
        self.assertIn("Proceed only on `status: ready`", text)
        self.assertIn("`status: blocked` has a null context", text)
        self.assertIn("consumers must not reinterpret its reason", text)
        self.assertIn("Planning State alone decides semantic currentness", text)
        self.assertIn(
            "`preflight_cross_checkout_live_lease(...)` with only the immutable "
            "planning snapshot",
            text,
        )
        self.assertIn(
            "The helper's project-owned `DELETION_CONDITION` is the removal "
            "condition for both temporary APIs.",
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

    def test_cross_checkout_startup_has_one_ready_blocked_preflight(self) -> None:
        work_batch = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Ready/Blocked Preflight",
        )

        self.assertIn("`work-batch` owns the normal queued-to-executing transition", work_batch)
        self.assertIn("the same runway is still the only queued or active batch", work_batch)
        self.assertIn("Planning State alone owns semantic currentness", work_batch)
        self.assertIn("`preflight_cross_checkout_live_lease(...)`", work_batch)
        self.assertIn("with only the immutable snapshot", work_batch)
        self.assertIn("Proceed only when it returns `status: ready`", work_batch)
        self.assertIn("Treat `status: blocked`", work_batch)
        self.assertIn("without reclassifying it", work_batch)

    def test_planning_state_is_the_only_queue_currentness_owner(
        self,
    ) -> None:
        preflight = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Ready/Blocked Preflight",
        )

        self.assertIn("Planning State Diagnostic", preflight)
        self.assertIn("same runway is still the only queued or active batch", preflight)
        self.assertIn("Planning State alone owns semantic currentness", preflight)
        self.assertIn("amendment, replacement, supersession, abandonment", preflight)
        self.assertIn("with only the immutable snapshot", preflight)
        self.assertIn("does not mutate planning state", preflight)
        for removed_contract in (
            "queue_transaction_paths",
            "queue-transaction paths",
            "queue transaction paths",
            "queue-establishment transaction",
        ):
            with self.subTest(removed_contract=removed_contract):
                self.assertNotIn(removed_contract, preflight)

    def test_cross_checkout_preflight_consumers_remain_project_neutral(
        self,
    ) -> None:
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
        preflight = self.normalized_section(
            WORK_BATCH,
            "Cross-Checkout Ready/Blocked Preflight",
        )
        strict_execution = self.normalized_section(
            WORK_BATCH,
            "Explicit Strict Cross-Checkout Execution",
        )
        helper_bootstrap = self.normalized_section(
            CROSS_CHECKOUT_CONTEXT,
            "Stable Helper Bootstrap",
        )

        self.assertIn("`preflight_cross_checkout_live_lease(...)`", preflight)
        self.assertIn("non-null, strictly parsed `live_context`", preflight)
        self.assertIn("`validate_write_scope(...)` separately", preflight)
        self.assertIn(
            "Immediately before every later worker and reviewer delegation, call "
            "`prepare_cross_checkout_context_refresh(...)` again",
            strict_execution,
        )
        self.assertIn(
            "newly prepared exact live execution lease",
            strict_execution,
        )
        self.assertIn(
            "do not treat the snapshot itself as a live lease",
            helper_bootstrap,
        )
        self.assertIn("Never pass the planning snapshot as the handoff lease", strict_execution)
        self.assertIn(
            "the helper remains mechanical and does not mutate planning state",
            preflight,
        )

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

    def test_cross_checkout_recovery_preserves_blocked_preflight(self) -> None:
        execute_spec = self.normalized_section(
            EXECUTE_SPEC,
            "Cross-Checkout Preflight Routing",
        )
        recovery = self.normalized_section(
            EXECUTE_RECOVERY,
            "Cross-Checkout Movement Boundary",
        )

        self.assertIn(
            "route through the `work-batch` ready/blocked preflight before strict "
            "delegation validation and before unexpected-movement recovery",
            execute_spec,
        )
        self.assertIn("is not, by itself, a recovery trigger", recovery)
        self.assertIn("A ready result supplies the first strictly parsed live context", recovery)
        self.assertIn("A blocked result, null context, or helper failure", recovery)
        self.assertIn("without reinterpreting the helper's reason", recovery)
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

    def test_plan_batch_requires_fresh_independent_review_before_queueing(
        self,
    ) -> None:
        plan_batch = self.normalized_path(PLAN_BATCH)

        self.assertIn(
            "plan -> exact drafts -> independent review -> fail-closed "
            "authorization -> queue",
            plan_batch,
        )
        self.assertIn(
            "delegate one fresh, read-only independent planning review",
            plan_batch,
        )
        self.assertIn("directly inspect both draft files", plan_batch)
        self.assertIn("supporting evidence", plan_batch)
        self.assertIn("`approve | revise | block`", plan_batch)
        self.assertIn("Planner self-attestation is insufficient", plan_batch)
        self.assertIn("exact repo-relative dispatch and runway paths", plan_batch)
        self.assertIn("SHA-256 hash of each inspected draft", plan_batch)
        self.assertIn("at least one nonblank evidence reference", plan_batch)
        self.assertIn("Any edit to either draft after review invalidates", plan_batch)
        self.assertIn("delegate another fresh independent review", plan_batch)

    def test_queue_owners_and_mechanical_authorization_boundary_stay_separate(
        self,
    ) -> None:
        plan_batch = self.normalized_path(PLAN_BATCH)
        architecture = self.normalized_path(ARCHITECTURE_PROGRAM_RUNWAY)
        fixtures = self.normalized_path(STATE_FIXTURES)

        self.assertIn(
            "Architecture Program Runway remains the semantic queue owner",
            fixtures,
        )
        self.assertIn(
            "`batch-runway` remains the semantic owner of the concrete runway plan",
            architecture,
        )
        self.assertIn(
            "must not mark a runway queued until `plan-batch` has completed the "
            "independent planning review",
            architecture,
        )
        for text in (plan_batch, architecture, fixtures):
            with self.subTest(surface=text[:40]):
                self.assertIn("does not authenticate", text)
                self.assertIn("judge evidence relevance or sufficiency", text)

    def test_state_fixture_guidance_declares_exact_queue_authorization_facts(
        self,
    ) -> None:
        fixtures = self.normalized_path(STATE_FIXTURES)

        for flag in (
            "--planner-decision plan",
            "--reviewer-decision approve",
            "--reviewed-dispatch",
            "--reviewed-dispatch-sha256",
            "--reviewed-runway",
            "--reviewed-runway-sha256",
            "--review-evidence",
        ):
            with self.subTest(flag=flag):
                self.assertIn(flag, fixtures)
        self.assertIn("lowercase 64-hex SHA-256 values", fixtures)
        self.assertIn("rejects the transition without changing state", fixtures)


if __name__ == "__main__":
    unittest.main()
