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
            "skills/batch-runway/references/create-spec.md",
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
        create_spec = self.read("skills/batch-runway/references/create-spec.md")
        execute_spec = self.read("skills/batch-runway/references/execute-spec.md")

        for surface, text in {
            "entrypoint": entrypoint,
            "create-spec": create_spec,
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

    def test_architecture_program_keeps_authority_over_program_state(self) -> None:
        entrypoint = self.read("skills/architecture-program-runway/SKILL.md")

        self.assertIn("Planning State Diagnostic", entrypoint)
        self.assertIn("Diagnostic-First Pickup", entrypoint)
        self.assertIn("current", entrypoint)
        self.assertIn("validate", entrypoint)
        self.assertIn("must not select batches", entrypoint)
        self.assertIn("replace program ledgers", entrypoint)
        self.assertIn("selected dispatch", entrypoint)
        self.assertIn("close findings", entrypoint)

    def test_program_and_runway_handoff_has_one_ledger_owner_per_layer(self) -> None:
        architecture = self.read("skills/architecture-program-runway/SKILL.md")
        batch = self.read("skills/batch-runway/SKILL.md")

        self.assertIn("## Program/Runway Handoff Boundary", architecture)
        self.assertIn("program-level ledger\nupdates", architecture)
        self.assertIn("selected dispatch packet", architecture)
        self.assertIn("closeout reconciliation", architecture)
        self.assertIn("does not reselect the program batch", architecture)
        self.assertIn("program findings ledger", architecture)

        self.assertIn("## Architecture Program Handoff", batch)
        self.assertIn("concrete execution state", batch)
        self.assertIn("concrete execution-ledger updates", batch)
        self.assertIn("completed-slice archives", batch)
        self.assertIn("Architecture Program Runway owns program state", batch)
        self.assertIn("program-level ledger updates", batch)
        self.assertIn("closeout reconciliation across batches", batch)
        self.assertIn("Do not use Batch Runway routine execution to reselect", batch)

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
            "skills/batch-runway/references/create-spec.md",
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
        self.assertIn("semantic program decision", architecture)
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
            version_tuple("1.0.4"),
        )

    def test_specialized_discovery_skills_do_not_create_parallel_planning_systems(
        self,
    ) -> None:
        legacy = self.read("skills/legacy-removal/SKILL.md")
        dead_surface = self.read("skills/dead-surface-audit/SKILL.md")

        self.assertIn("evidence producer", legacy)
        self.assertIn("handoff source", legacy)
        self.assertIn("explicitly selected program owner", legacy)
        self.assertIn("before writing\ndurable ledgers", legacy)
        self.assertIn("does not create\ndurable program queue state", legacy)
        self.assertIn("selected-batch state", legacy)
        self.assertIn("parallel program\nledgers", legacy)
        self.assertIn("program owner for", legacy)
        self.assertIn("selection", legacy)

        self.assertIn("evidence producer only", dead_surface)
        self.assertIn("does not create durable program ledgers", dead_surface)
        self.assertIn("selected-batch\nstate", dead_surface)
        self.assertIn("evidence\nhandoff material", dead_surface)

    def test_legacy_removal_gates_selected_dispatch_and_batch_runway_handoff(
        self,
    ) -> None:
        legacy = self.read("skills/legacy-removal/SKILL.md")

        self.assertNotIn(
            "Use this section only if one next batch is clear.",
            legacy,
        )
        self.assertNotIn(
            "Use `batch-runway create-spec` after this skill only when the "
            "selected dispatch\npacket identifies exactly one bounded batch.",
            legacy,
        )
        self.assertIn("dispatch handoff material for the program owner", legacy)
        self.assertIn("Do\nnot treat it as queued or selected program state", legacy)
        self.assertIn("Use it as a selected dispatch packet only when", legacy)
        self.assertIn("explicitly the\nprogram owner", legacy)
        self.assertIn("already accepted or selected", legacy)
        self.assertIn("Use `batch-runway create-spec` after this skill only when", legacy)
        self.assertIn("another program owner has already accepted or selected", legacy)


if __name__ == "__main__":
    unittest.main()
