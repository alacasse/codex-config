from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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


if __name__ == "__main__":
    unittest.main()
