from __future__ import annotations

import json
import tomllib
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import install_codex_config


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "codex-features.json"


class CodexFeaturesManifestTests(unittest.TestCase):
    def load_manifest(self) -> dict[str, object]:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_links_point_to_repo_sources(self) -> None:
        manifest = self.load_manifest()

        for feature_name, feature in manifest["features"].items():
            with self.subTest(feature=feature_name):
                links = feature["links"]
                self.assertGreater(len(links), 0)
                for link in links:
                    source = Path(link["source"])
                    target = Path(link["target"])
                    self.assertFalse(source.is_absolute())
                    self.assertFalse(target.is_absolute())
                    self.assertNotIn("..", source.parts)
                    self.assertNotIn("..", target.parts)
                    self.assertTrue(
                        (REPO_ROOT / source).exists(),
                        f"missing manifest source: {source}",
                    )

    def test_manifest_feature_requirements_are_valid(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]

        for feature_name, feature in features.items():
            with self.subTest(feature=feature_name):
                requirements = feature.get("requires", [])
                self.assertIsInstance(requirements, list)
                for requirement in requirements:
                    self.assertIsInstance(requirement, str)
                    self.assertIn(requirement, features)

    def test_planning_artifact_consumers_install_shared_skill(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]

        for feature_name, feature in features.items():
            uses_planning_artifacts = False
            for link in feature["links"]:
                source = REPO_ROOT / link["source"]
                if not source.is_dir():
                    continue
                for skill_file in source.rglob("*.md"):
                    if "../planning-artifacts/SKILL.md" in skill_file.read_text(
                        encoding="utf-8"
                    ):
                        uses_planning_artifacts = True
                        break
                if uses_planning_artifacts:
                    break
            if uses_planning_artifacts:
                with self.subTest(feature=feature_name):
                    self.assertIn("planning-artifacts", feature.get("requires", []))

    def test_single_feature_install_expands_planning_state_consumer_dependencies(
        self,
    ) -> None:
        manifest = self.load_manifest()
        expected_dependencies = ["planning-artifacts", "planning-state"]

        for feature_name in (
            "batch-runway",
            "architecture-program-runway",
            "legacy-removal",
        ):
            with self.subTest(feature=feature_name):
                feature = manifest["features"][feature_name]
                self.assertEqual(feature.get("requires", []), expected_dependencies)

                args = Namespace(feature=[feature_name], all_features=False)
                selected = install_codex_config.selected_feature_names(args, manifest)

                self.assertEqual(selected, [*expected_dependencies, feature_name])

    def test_planning_state_installs_skill_and_command_boundary(self) -> None:
        manifest = self.load_manifest()
        planning_state = manifest["features"]["planning-state"]

        self.assertIn("planning-artifacts", planning_state.get("requires", []))
        self.assertEqual(
            {link["source"] for link in planning_state["links"]},
            {"skills/planning-state", "scripts/planning_state.py"},
        )

        args = Namespace(feature=["planning-state"], all_features=False)
        selected = install_codex_config.selected_feature_names(args, manifest)

        self.assertEqual(selected, ["planning-artifacts", "planning-state"])

    def test_command_owner_skills_are_directly_invokable(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]

        expected = {
            "add-to-ledger": [
                "planning-artifacts",
                "planning-state",
                "architecture-program-runway",
                "legacy-removal",
            ],
            "plan-batch": [
                "planning-artifacts",
                "planning-state",
                "architecture-program-runway",
                "batch-runway",
            ],
            "work-batch": [
                "planning-artifacts",
                "planning-state",
                "batch-runway",
            ],
        }

        for skill_name, required_features in expected.items():
            with self.subTest(skill=skill_name):
                feature = features[skill_name]
                self.assertEqual(feature.get("requires", []), required_features)
                self.assertEqual(
                    {link["source"] for link in feature["links"]},
                    {f"skills/{skill_name}"},
                )

                skill_text = (
                    REPO_ROOT / f"skills/{skill_name}/SKILL.md"
                ).read_text(encoding="utf-8")
                ui_text = (
                    REPO_ROOT / f"skills/{skill_name}/agents/openai.yaml"
                ).read_text(encoding="utf-8")

                self.assertIn(f"name: {skill_name}", skill_text)
                self.assertIn("## Stops", skill_text)
                self.assertIn("## Copy-First Bridge", skill_text)
                self.assertIn(f"Use ${skill_name}", ui_text)

    def test_custom_agent_toml_files_are_valid(self) -> None:
        manifest = self.load_manifest()
        custom_agents = manifest["features"]["custom-agents"]

        for link in custom_agents["links"]:
            source = Path(link["source"])
            if source.suffix != ".toml":
                continue
            with self.subTest(agent=str(source)):
                data = tomllib.loads((REPO_ROOT / source).read_text(encoding="utf-8"))
                self.assertIsInstance(data.get("name"), str)
                self.assertIsInstance(data.get("description"), str)
                self.assertIsInstance(data.get("developer_instructions"), str)

    def test_global_instructions_include_default_agent_delegation(self) -> None:
        manifest = self.load_manifest()
        global_instructions = manifest["features"]["global-instructions"]
        sources = {link["source"] for link in global_instructions["links"]}

        self.assertIn("AGENTS.md", sources)

        instructions = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("default/principal agent", instructions)
        self.assertIn("standing preference", instructions)
        self.assertIn("higher-priority runtime tool policy", instructions)


if __name__ == "__main__":
    unittest.main()
