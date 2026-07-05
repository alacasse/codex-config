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

    def test_architecture_program_keeps_authority_over_program_state(self) -> None:
        entrypoint = self.read("skills/architecture-program-runway/SKILL.md")

        self.assertIn("Planning State Diagnostic", entrypoint)
        self.assertIn("current", entrypoint)
        self.assertIn("validate", entrypoint)
        self.assertIn("must not select batches", entrypoint)
        self.assertIn("replace program ledgers or selected", entrypoint)
        self.assertIn("close findings", entrypoint)

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

    def test_legacy_removal_keeps_authority_over_legacy_decisions(self) -> None:
        entrypoint = self.read("skills/legacy-removal/SKILL.md")

        self.assertIn("Planning State Diagnostic", entrypoint)
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


if __name__ == "__main__":
    unittest.main()
