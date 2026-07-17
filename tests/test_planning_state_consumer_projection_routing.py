from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


class PlanningStateConsumerProjectionRoutingTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def section_between(
        self,
        text: str,
        start: str,
        end: str | None,
    ) -> str:
        section_start = text.index(start)
        section_end = len(text) if end is None else text.index(end, section_start)
        return text[section_start:section_end]

    def test_batch_runway_routes_supported_reports_through_projection_guidance(
        self,
    ) -> None:
        surfaces = [
            "skills/batch-runway/SKILL.md",
            "skills/batch-runway/references/execute-spec.md",
            "skills/batch-runway/references/finalize-batch-v1.md",
        ]

        for surface in surfaces:
            with self.subTest(surface=surface):
                text = self.read(surface)
                self.assertIn("projection-reporting.md", text)
                self.assertIn("report-projection", text)
                self.assertIn("projection_usage", text)
                self.assertIn("projection_rebuild_authority", text)
                self.assertIn("broad historical", text)
                self.assertIn("scans", text)
                self.assertIn("normal route", text)
                self.assertRegex(text, r"fallback\s+decision")
                self.assertRegex(text, r"command\s+output")

    def test_architecture_program_closeout_and_runner_history_blocks_are_gated(
        self,
    ) -> None:
        ledger_template = self.read(
            "skills/architecture-program-runway/references/program-ledger-template.md"
        )
        local_runner = self.read(
            "skills/architecture-program-runway/references/local-runner-v1.md"
        )
        closeout = self.section_between(
            ledger_template,
            "## Closeout Checklist",
            None,
        )
        runner_history = self.section_between(
            local_runner,
            "## Final Summary Contract",
            "The summary contains:",
        )

        for surface, text in {
            "closeout-checklist": closeout,
            "runner-history": runner_history,
        }.items():
            with self.subTest(surface=surface):
                self.assertIn("projection-reporting", text)
                self.assertIn("projection_usage", text)
                self.assertIn("projection_rebuild_authority", text)
                self.assertIn("report-projection", text)
                self.assertRegex(text, r"command\s+output")
                self.assertIn("normal route", text)
                self.assertIn("broad historical scans", text)
                self.assertRegex(text, r"fallback\s+decisions before scanning")
                self.assertRegex(text, r"Do not query SQLite\s+directly")

    def test_batch_runway_keeps_active_pickup_on_planning_state_diagnostic(
        self,
    ) -> None:
        entrypoint = self.read("skills/batch-runway/SKILL.md")
        execute_spec = self.read("skills/batch-runway/references/execute-spec.md")

        for surface, text in {
            "entrypoint": entrypoint,
            "execute-spec": execute_spec,
        }.items():
            with self.subTest(surface=surface):
                self.assertIn("Planning State Diagnostic", text)
                self.assertIn("Diagnostic-First Pickup", text)
                self.assertIn("current", text)
                self.assertIn("validate", text)

    def test_batch_runway_feature_depends_on_planning_state(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / "codex-features.json").read_text(encoding="utf-8")
        )

        self.assertIn(
            "planning-state",
            manifest["features"]["batch-runway"].get("requires", []),
        )

    def test_architecture_program_routes_supported_reports_through_projection_guidance(
        self,
    ) -> None:
        surfaces = [
            "skills/architecture-program-runway/references/program-ledger-template.md",
            "skills/architecture-program-runway/references/goal-runner-v1.md",
            "skills/architecture-program-runway/references/local-runner-v1.md",
        ]

        entrypoint = self.read("skills/architecture-program-runway/SKILL.md")
        self.assertIn("../planning-state/references/projection-reporting.md", entrypoint)
        self.assertNotIn(
            "../../planning-state/references/projection-reporting.md",
            entrypoint,
        )

        for surface in surfaces:
            with self.subTest(surface=surface):
                text = self.read(surface)
                self.assertIn(
                    "../../planning-state/references/projection-reporting.md",
                    text,
                )
                self.assertNotIn(
                    "`../planning-state/references/projection-reporting.md",
                    text,
                )
                self.assertIn("report-projection", text)
                self.assertIn("projection_usage", text)
                self.assertIn("projection_rebuild_authority", text)
                self.assertIn("broad historical", text)
                self.assertIn("scans", text)
                self.assertIn("normal route", text)
                self.assertRegex(text, r"fallback\s+decision")
                self.assertIn("command output", text)

    def test_architecture_program_keeps_closeout_authority_only(self) -> None:
        entrypoint = self.read("skills/architecture-program-runway/SKILL.md")

        self.assertIn("Planning State Diagnostic", entrypoint)
        self.assertIn("Diagnostic-First Pickup", entrypoint)
        self.assertIn("current", entrypoint)
        self.assertIn("validate", entrypoint)
        self.assertIn("same-batch closeout reconciliation", entrypoint)
        self.assertIn("must not group open findings", entrypoint)
        self.assertIn("prepare a queue transaction", entrypoint)
        self.assertIn("successor planning", entrypoint)

    def test_program_and_runway_handoff_has_one_ledger_owner_per_layer(self) -> None:
        architecture = self.read("skills/architecture-program-runway/SKILL.md")
        batch = self.read("skills/batch-runway/SKILL.md")
        architecture_boundary = " ".join(
            self.section_between(
                architecture,
                "## Boundary",
                "## Required First Steps",
            ).split()
        )
        batch_handoff = " ".join(
            self.section_between(
                batch,
                "## Architecture Program Handoff",
                "## Execute-Spec Summary",
            ).split()
        )

        self.assertIn("existing, just-completed batch", architecture_boundary)
        self.assertIn("reconcile that batch's existing ledger row", architecture_boundary)
        self.assertIn("must not group open findings", architecture_boundary)
        self.assertIn("prepare a queue transaction", architecture_boundary)
        self.assertIn("public `plan-batch`", architecture_boundary)

        self.assertIn("Public `plan-batch` supplies", batch_handoff)
        self.assertIn("concrete execution state", batch_handoff)
        self.assertIn("execution-ledger updates", batch_handoff)
        self.assertIn("completed-slice archive", batch_handoff)
        self.assertIn("Do not use Batch Runway execution to reselect", batch_handoff)
        self.assertIn("just-completed batch only", batch_handoff)
        self.assertIn("must not select or prepare a successor", batch_handoff)

    def test_architecture_program_feature_depends_on_planning_state(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / "codex-features.json").read_text(encoding="utf-8")
        )

        self.assertIn(
            "planning-state",
            manifest["features"]["architecture-program-runway"].get("requires", []),
        )
        self.assertGreaterEqual(
            version_tuple(
                manifest["features"]["architecture-program-runway"]["version"]
            ),
            version_tuple("1.1.2"),
        )

    def test_legacy_removal_routes_supported_reports_through_projection_guidance(
        self,
    ) -> None:
        entrypoint = self.read("skills/legacy-removal/SKILL.md")

        self.assertIn("../planning-state/references/projection-reporting.md", entrypoint)
        self.assertIn("report-projection", entrypoint)
        self.assertIn("projection_usage", entrypoint)
        self.assertIn("projection_rebuild_authority", entrypoint)
        self.assertIn("broad historical", entrypoint)
        self.assertIn("scans", entrypoint)
        self.assertIn("normal route", entrypoint)
        self.assertRegex(entrypoint, r"fallback\s+decisions before scanning")
        self.assertIn("command output", entrypoint)

    def test_planning_state_projection_reporting_contract_keeps_sqlite_noncanonical(
        self,
    ) -> None:
        entrypoint = self.read("skills/planning-state/SKILL.md")
        reference = self.read("skills/planning-state/references/projection-reporting.md")

        for surface, text in {
            "entrypoint": entrypoint,
            "projection-reporting": reference,
        }.items():
            with self.subTest(surface=surface):
                self.assertIn("current", text)
                self.assertIn("validate", text)
                self.assertIn("active-state hot path", text)
                self.assertIn("projection_usage", text)
                self.assertIn("projection_rebuild_authority", text)
                self.assertIn("report-projection", text)
                self.assertIn("normal route", text)
                self.assertRegex(
                    text,
                    r"[Bb]road\s+historical\s+scans are a fallback",
                )
                self.assertIn("Do not", text)
                self.assertIn("query SQLite directly", text)

    def test_legacy_removal_keeps_authority_over_legacy_decisions(self) -> None:
        entrypoint = self.read("skills/legacy-removal/SKILL.md")

        self.assertIn("Planning State Diagnostic", entrypoint)
        self.assertIn("Diagnostic-First Pickup", entrypoint)
        self.assertIn("current", entrypoint)
        self.assertIn("validate", entrypoint)
        self.assertIn("old model", entrypoint)
        self.assertIn("canonical model", entrypoint)
        self.assertIn("evidence value", entrypoint)
        self.assertIn("compatibility decision", entrypoint)
        self.assertIn("cleanup-residue classification", entrypoint)
        self.assertIn("handoff target", entrypoint)
        self.assertIn("planning-state context only", entrypoint)
        self.assertIn("classify a legacy surface", entrypoint)
        self.assertIn("prove liveness or deadness", entrypoint)

    def test_consumer_pickup_guidance_keeps_planning_state_single_owner(self) -> None:
        surfaces = [
            "skills/batch-runway/SKILL.md",
            "skills/batch-runway/references/execute-spec.md",
            "skills/architecture-program-runway/SKILL.md",
            "skills/legacy-removal/SKILL.md",
        ]

        for surface in surfaces:
            with self.subTest(surface=surface):
                text = self.read(surface)
                self.assertIn("Diagnostic-First Pickup", text)
                self.assertIn("current", text)
                self.assertIn("validate", text)
                if "broader exploration" in text:
                    self.assertLess(
                        text.index("Diagnostic-First Pickup"),
                        text.index("broader exploration"),
                    )

        architecture = self.read("skills/architecture-program-runway/SKILL.md")
        self.assertIn("same_batch_closeout_disposition", architecture)
        self.assertNotIn(
            "run its read-only `current` and `validate` commands",
            architecture,
        )

        legacy = self.read("skills/legacy-removal/SKILL.md")
        self.assertNotIn("python scripts/planning_state.py current --root", legacy)
        self.assertIn("old model", legacy)

    def test_planning_artifacts_and_state_keep_layout_pickup_boundary(self) -> None:
        artifacts = self.read("skills/planning-artifacts/SKILL.md")
        state = self.read("skills/planning-state/SKILL.md")

        self.assertIn("placement, naming, file shape", artifacts)
        self.assertIn("Planning State Diagnostic-First Pickup", artifacts)
        self.assertIn("competing pickup algorithm", artifacts)
        self.assertNotIn("first navigation path", artifacts)
        self.assertNotIn("before broad exploration", artifacts)

        self.assertIn("For pickup questions, use this skill first", state)
        self.assertIn("does not redefine artifact layout", state)
        self.assertIn("operational ordering for pickup", state)
        self.assertIn("target-policy checks", state)
        self.assertIn("projection routing", state)

    def test_legacy_removal_feature_depends_on_planning_state(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / "codex-features.json").read_text(encoding="utf-8")
        )

        self.assertIn(
            "planning-state",
            manifest["features"]["legacy-removal"].get("requires", []),
        )
        self.assertGreaterEqual(
            version_tuple(manifest["features"]["legacy-removal"]["version"]),
            version_tuple("1.0.9"),
        )

    def test_specialized_discovery_skills_do_not_create_parallel_planning_systems(
        self,
    ) -> None:
        legacy = self.read("skills/legacy-removal/SKILL.md")
        dead_surface = self.read("skills/dead-surface-audit/SKILL.md")

        self.assertIn("evidence producer", legacy)
        self.assertIn("handoff source", legacy)
        self.assertIn("never becomes a program owner", legacy)
        self.assertIn("parallel planning\nsystem", legacy)
        self.assertIn("never write selection or queue state", legacy)
        self.assertIn("never queued or selected program state", legacy)
        self.assertIn("public `plan-batch`", legacy)
        self.assertNotIn("explicitly selected program owner", legacy)
        self.assertNotIn("owning program workflow", legacy)

        self.assertIn("evidence producer only", dead_surface)
        self.assertIn("does not create durable program ledgers", dead_surface)
        self.assertIn("selected-batch state", dead_surface)
        self.assertIn("public\n`plan-batch` handoffs", dead_surface)

    def test_legacy_removal_hands_off_evidence_without_selecting_or_creating_runways(
        self,
    ) -> None:
        legacy = self.read("skills/legacy-removal/SKILL.md")

        self.assertIn("## Dispatch handoff evidence", legacy)
        self.assertIn("It is never queued or selected program state", legacy)
        self.assertIn("Only\n`plan-batch` decides whether to accept it", legacy)
        self.assertIn("Do not invoke Batch Runway planning", legacy)
        self.assertIn("Use public `plan-batch` after this skill", legacy)
        self.assertNotIn("## Dispatch handoff or selected dispatch packet", legacy)
        self.assertNotIn("Use it as a selected dispatch packet", legacy)

    def test_legacy_removal_evidence_artifact_rejects_self_owned_state_synonyms(
        self,
    ) -> None:
        legacy = self.read("skills/legacy-removal/SKILL.md")
        evidence_artifact = self.section_between(
            legacy,
            "## Evidence Artifact Rules",
            "## Relationship To Other Runway Skills",
        )
        normalized_artifact = " ".join(evidence_artifact.split())

        for state_synonym in (
            "Legacy Removal Ledger",
            "evidence ledger",
            "legacy-removal ledger rows",
            "legacy ledger",
            "| ID | Status |",
            "| L1 | Open |",
        ):
            with self.subTest(state_synonym=state_synonym):
                self.assertNotIn(state_synonym, evidence_artifact)

        for self_owned_work in (
            "when the ledger spans",
            "ordinary markdown ledger or dispatch work",
            "write the ledger",
            "update the ledger",
            "create a dispatch packet",
        ):
            with self.subTest(self_owned_work=self_owned_work):
                self.assertNotIn(self_owned_work, normalized_artifact.lower())

        self.assertIn("# Legacy Removal Evidence Report", evidence_artifact)
        self.assertIn("Canonical program ledger (read-only)", evidence_artifact)
        self.assertIn(
            "`work-batch` same-batch closeout applies lifecycle state",
            normalized_artifact,
        )
        self.assertIn(
            "read-only planning-state or canonical program-ledger context",
            normalized_artifact,
        )
        self.assertIn(
            "produces evidence reports and dispatch handoff evidence only",
            normalized_artifact,
        )

    def test_test_quality_review_is_review_support_not_primary_planning_command(
        self,
    ) -> None:
        entrypoint = self.read("skills/test-quality-review/SKILL.md")
        integration = self.read("skills/batch-runway/references/test-quality-review.md")
        execute_spec = self.read("skills/batch-runway/references/execute-spec.md")
        execute_core = self.read(
            "skills/batch-runway/references/execute-slice-core-v1.md"
        )

        self.assertIn("agent-facing review support skill", entrypoint)
        self.assertRegex(entrypoint, r"not a primary human planning\s+command")
        self.assertRegex(entrypoint, r"directly\s+requestable for focused audits")

        self.assertIn("triggered specialist-review routing", execute_spec)
        compact_execute_core = " ".join(execute_core.split())
        self.assertIn(
            "`test-quality-review.md` when tests trigger that review",
            compact_execute_core,
        )
        self.assertIn("review information only", integration)
        self.assertRegex(
            integration,
            r"Do not\s+automatically modify execution flow",
        )

    def test_work_batch_and_review_reject_unsupported_legacy_preservation_by_default(
        self,
    ) -> None:
        work_batch = self.read("skills/work-batch/SKILL.md")
        reviewer_guidance = self.read(
            "skills/batch-runway/references/subagent-briefs.md"
        )
        legacy = self.read("skills/legacy-removal/SKILL.md")
        dead_surface = self.read("skills/dead-surface-audit/SKILL.md")

        for surface, text in {
            "work-batch": work_batch,
            "subagent-briefs": reviewer_guidance,
            "legacy-removal": legacy,
        }.items():
            with self.subTest(surface=surface):
                self.assertRegex(text, r"default\s+implementation and review")
                self.assertIn("external contract", text)
                self.assertIn("removal condition", text)

        self.assertIn("not a normal human-facing cleanup command", legacy)
        self.assertIn("exceptional residue", dead_surface)
        self.assertRegex(dead_surface, r"does not create\s+durable program ledgers")
        self.assertRegex(dead_surface, r"human-facing cleanup\s+command")


if __name__ == "__main__":
    unittest.main()
