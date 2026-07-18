from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = REPO_ROOT / "AGENTS.md"
POLICY = (
    REPO_ROOT
    / "docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md"
)
POLICY_LINK = (
    "docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md"
)


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


class StableRunwayDogfoodingPolicyTests(unittest.TestCase):
    def test_repository_instructions_load_the_temporary_policy(self) -> None:
        instructions = normalized(INSTRUCTIONS)

        self.assertIn("Before planning or executing CCFG-26 through CCFG-29", instructions)
        self.assertIn("read and apply", instructions)
        self.assertIn(f"({POLICY_LINK})", instructions)
        self.assertEqual(POLICY.resolve(), (INSTRUCTIONS.parent / POLICY_LINK).resolve())
        self.assertTrue(POLICY.is_file())
        self.assertIn(
            "This repository-local hook is temporary and CCFG-29 removes it "
            "only after the integrated candidate proves the policy's required "
            "behavior.",
            instructions,
        )

    def test_policy_is_limited_to_the_temporary_ccfg_range_and_removal_gate(
        self,
    ) -> None:
        policy = normalized(POLICY)

        self.assertIn("applies only", policy)
        self.assertIn("CCFG-26 through CCFG-29", policy)
        self.assertIn(
            "CCFG-29 must remove this policy and its root `AGENTS.md` hook "
            "only after the integrated candidate proves equivalent vertical "
            "planning, one-slice execution, bounded recovery escalation, and "
            "no-successor behavior.",
            policy,
        )
        self.assertIn(
            "Remove the focused regression test only after equivalent candidate "
            "scenarios pass.",
            policy,
        )

    def test_policy_requires_vertical_slices_and_explicit_migration_residue(
        self,
    ) -> None:
        policy = normalized(POLICY)
        vertical_slice_fields = (
            "starting_scenario",
            "durable_result",
            "owner_before",
            "owner_after",
            "migrated_callers",
            "focused_validation",
            "independently_usable_state",
            "rollback_boundary",
            "temporary_residue",
        )
        migration_matrix_fields = (
            "current_owner",
            "future_owner",
            "status",
            "removal_slice_or_condition",
        )

        for field in (*vertical_slice_fields, *migration_matrix_fields):
            with self.subTest(field=field):
                self.assertIn(f"{field}:", policy)

        self.assertIn("Do not leave caller ownership ambiguous", policy)
        self.assertIn("silent fallback", policy)
        self.assertIn(
            "retained legacy route must name its caller, reason, future owner, "
            "and removal condition",
            policy,
        )
        self.assertIn("validation and independent review focused", policy)
        self.assertIn("final range validation remains separate", policy)
        self.assertIn("Never choose a fixed slice count in advance", policy)
        self.assertIn("smaller-alternative analysis", policy)

    def test_policy_executes_one_implementation_slice_per_invocation(self) -> None:
        policy = normalized(POLICY)

        for fragment in (
            "consume the current queued or active runway",
            "execute exactly the next incomplete implementation slice",
            "worker implementation, focused validation, independent review",
            "already-authorized correction, commit, receipt, execution-ledger update",
            "completed-slice archive",
            "stop before beginning another implementation slice",
            "later explicit `work-batch` invocation",
            "resumes from the existing durable state",
            "no-successor-selection rule",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, policy)

        self.assertIn("Manual relaunch", policy)
        self.assertIn(
            "does not promise automatic continuation or a fresh process at each "
            "lifecycle boundary",
            policy,
        )
        self.assertIn(
            "this policy neither requires nor creates separate finalization or "
            "closeout processes",
            policy,
        )
        self.assertIn("no launcher", policy)
        self.assertIn("state field", policy)
        self.assertIn("telemetry", policy)

    def test_recovery_advice_is_once_read_only_and_non_authoritative(self) -> None:
        policy = normalized(POLICY)

        for fragment in (
            "existing read-only `codebase_investigator` exactly once",
            "remains unchanged and advisory",
            "active slice, stop condition, failing command or evidence",
            "current diff and worktree facts",
            "proposed smallest recovery",
            "already authorized by the active runway and existing recovery contract",
            "command invocation correction",
            "exact retry",
            "environment or cache repair",
            "refreshed diff or review basis",
            "already-authorized in-slice repair",
            "Stop for user direction or a reviewed amendment",
            "expand scope",
            "reclassify validation",
            "change semantics",
            "weaken safety",
            "destructive work",
            "add a lifecycle surface",
            "multiple material options",
            "proceed without enough evidence",
            "cannot edit, approve, commit, delegate, select, amend, or grant recovery authority",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, policy)


if __name__ == "__main__":
    unittest.main()
