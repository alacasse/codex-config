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
        routing_contract = (REPO_ROOT / "docs/skill-routing-contract.md").read_text(
            encoding="utf-8"
        )

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
                self.assertIn("## Agent-Facing Support", skill_text)
                self.assertIn("docs/skill-routing-contract.md", skill_text)
                self.assertIn(f"Use ${skill_name}", ui_text)

        self.assertIn("## Routing Table", routing_contract)
        self.assertIn("## Conflict Rule", routing_contract)
        self.assertIn("## Stop Rule", routing_contract)
        self.assertIn("## Bridge-State Rule", routing_contract)

    def test_command_owner_input_contracts_are_explicit(self) -> None:
        routing_contract = (REPO_ROOT / "docs/skill-routing-contract.md").read_text(
            encoding="utf-8"
        )
        add_to_ledger = (REPO_ROOT / "skills/add-to-ledger/SKILL.md").read_text(
            encoding="utf-8"
        )
        plan_batch = (REPO_ROOT / "skills/plan-batch/SKILL.md").read_text(
            encoding="utf-8"
        )
        work_batch = (REPO_ROOT / "skills/work-batch/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("## Command Input Contract", routing_contract)
        self.assertIn("fresh user-provided work/finding text", add_to_ledger)
        self.assertIn("existing ledger state/work", plan_batch)
        self.assertIn("must not silently create new ledger findings", plan_batch)
        self.assertIn("current queued or active runway", work_batch)

    def test_manifest_catalog_distinguishes_user_and_agent_facing_skills(
        self,
    ) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]

        for skill_name in (
            "add-to-ledger",
            "plan-batch",
            "work-batch",
            "port-by-contract",
        ):
            with self.subTest(skill=skill_name):
                description = features[skill_name]["description"]
                self.assertIn("User-facing command-owner skill", description)

        for skill_name in (
            "batch-runway",
            "architecture-program-runway",
            "test-quality-review",
            "dead-surface-audit",
            "legacy-removal",
            "planning-artifacts",
            "planning-state",
        ):
            with self.subTest(skill=skill_name):
                self.assertIn("Agent-facing", features[skill_name]["description"])

        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Skills", readme)
        self.assertIn("### User-Facing Workflow Commands", readme)
        self.assertIn("### Agent-Facing Support And Runtime Surfaces", readme)
        self.assertIn("not the preferred direct commands", readme)
        self.assertIn("docs/skill-routing-contract.md", readme)

    def test_port_by_contract_is_not_general_rewrite_shortcut(self) -> None:
        skill_text = (REPO_ROOT / "skills/port-by-contract/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("not a general cleanup or rewrite shortcut", skill_text)
        self.assertIn("contracts before creating a runway", skill_text)
        self.assertIn("docs/skill-routing-contract.md", skill_text)

    def test_direct_request_prompts_preserve_command_owner_boundary(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]
        primary_command_owners = {
            "add-to-ledger",
            "plan-batch",
            "work-batch",
            "port-by-contract",
        }
        directly_requestable_support = {"test-quality-review"}

        manifest_command_owners = {
            feature_name
            for feature_name, feature in features.items()
            if feature["description"].startswith("User-facing command-owner skill")
        }
        direct_prompt_skills = set()
        for prompt_file in (REPO_ROOT / "skills").glob("*/agents/openai.yaml"):
            if "Use $" in prompt_file.read_text(encoding="utf-8"):
                direct_prompt_skills.add(prompt_file.parents[1].name)

        self.assertEqual(manifest_command_owners, primary_command_owners)
        self.assertEqual(
            direct_prompt_skills,
            primary_command_owners | directly_requestable_support,
        )
        self.assertIn("Agent-facing", features["test-quality-review"]["description"])

    def test_agent_facing_support_skills_are_not_ui_commands(self) -> None:
        support_skills = (
            "batch-runway",
            "architecture-program-runway",
            "legacy-removal",
            "dead-surface-audit",
        )

        for skill_name in support_skills:
            with self.subTest(skill=skill_name):
                skill_text = (
                    REPO_ROOT / f"skills/{skill_name}/SKILL.md"
                ).read_text(encoding="utf-8")
                ui_text = (
                    REPO_ROOT / f"skills/{skill_name}/agents/openai.yaml"
                ).read_text(encoding="utf-8")
                frontmatter = skill_text.split("---", 2)[1]

                self.assertIn("Agent-facing", frontmatter)
                self.assertNotIn("Use when the user asks", frontmatter)
                self.assertNotIn(f"Use ${skill_name}", ui_text)

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
