from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "agents"
AGENT_PATH = AGENTS_DIR / "codebase_investigator.toml"
MANIFEST_PATH = REPO_ROOT / "codex-features.json"
BATCH_RUNWAY_FILES = (
    REPO_ROOT / "skills/batch-runway/SKILL.md",
    REPO_ROOT / "skills/batch-runway/references/subagent-briefs.md",
    REPO_ROOT / "skills/batch-runway/references/execute-slice-core-v1.md",
    REPO_ROOT / "skills/batch-runway/references/execute-spec.md",
)
OLD_AGENT_NAME = "fast_" + "explorer"


class CodebaseInvestigatorContractTests(unittest.TestCase):
    def load_agent(self) -> dict[str, object]:
        return tomllib.loads(AGENT_PATH.read_text(encoding="utf-8"))

    def test_registered_agent_has_expected_identity_and_model(self) -> None:
        self.assertTrue(AGENT_PATH.is_file())
        self.assertFalse((AGENTS_DIR / f"{OLD_AGENT_NAME}.toml").exists())

        agent = self.load_agent()

        self.assertEqual(agent["name"], "codebase_investigator")
        self.assertEqual(
            agent["description"],
            "Read-only codebase investigation agent for bounded technical questions.",
        )
        self.assertEqual(agent["model"], "gpt-5.6-terra")
        self.assertEqual(agent["model_reasoning_effort"], "low")

    def test_agent_owns_complete_yaml_investigation_contract(self) -> None:
        instructions = self.load_agent()["developer_instructions"]
        self.assertIsInstance(instructions, str)
        normalized_instructions = " ".join(instructions.split())

        required_schema_lines = (
            "status: answered | partial | blocked",
            "question_answered: string",
            "files_checked:",
            "findings:",
            "type: evidence | inference | uncertainty",
            "summary: string",
            "references:",
            "per_slice_notes: {}",
            "risks: []",
            "suggested_next_read: []",
        )
        for schema_line in required_schema_lines:
            with self.subTest(schema_line=schema_line):
                self.assertIn(schema_line, instructions)

        for boundary in (
            "without modifying files",
            "Answer the exact delegated question",
            "Stop when additional reading is unlikely to change the conclusion",
            "Do not invent missing behavior",
            "`partial` or `blocked` when evidence is insufficient",
            "Never replace a required implementation or review agent",
            "Never spawn, delegate to, or wait on additional agents",
            "never omit a material finding for concision",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, normalized_instructions)

    def test_manifest_registers_only_the_new_agent_path(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        links = manifest["features"]["custom-agents"]["links"]
        investigator_links = [
            link for link in links if "investigator" in link["source"]
        ]

        self.assertEqual(
            investigator_links,
            [
                {
                    "source": "agents/codebase_investigator.toml",
                    "target": "agents/codebase_investigator.toml",
                }
            ],
        )
        self.assertNotIn(
            OLD_AGENT_NAME,
            "\n".join(f"{link['source']} {link['target']}" for link in links),
        )

    def test_active_configuration_and_documentation_use_only_the_new_name(self) -> None:
        text_suffixes = {
            ".json",
            ".md",
            ".py",
            ".rules",
            ".sh",
            ".toml",
            ".txt",
            ".yaml",
            ".yml",
        }
        active_roots = (
            AGENTS_DIR,
            REPO_ROOT / ".codex",
            REPO_ROOT / "docs",
            REPO_ROOT / "hooks",
            REPO_ROOT / "rules",
            REPO_ROOT / "scripts",
            REPO_ROOT / "skills",
            REPO_ROOT / "tests",
        )
        excluded_parts = {"__pycache__", "archive"}
        active_paths = [
            path
            for root in active_roots
            for path in root.rglob("*")
            if path.is_file()
            and path.suffix in text_suffixes
            and not excluded_parts.intersection(path.relative_to(REPO_ROOT).parts)
        ]
        active_paths.extend(
            (REPO_ROOT / name)
            for name in ("AGENTS.md", "README.md", "codex-features.json")
        )

        stale_references = [
            str(path.relative_to(REPO_ROOT))
            for path in active_paths
            if OLD_AGENT_NAME in path.read_text(encoding="utf-8")
        ]

        self.assertEqual(stale_references, [])

    def test_batch_runway_keeps_orchestration_ownership(self) -> None:
        texts = {
            path.name: path.read_text(encoding="utf-8") for path in BATCH_RUNWAY_FILES
        }
        briefs = texts["subagent-briefs.md"]
        combined = "\n".join(texts.values())

        self.assertIn(
            "`agents/codebase_investigator.toml` owns the stable role behavior",
            briefs,
        )
        self.assertIn(
            "This Batch Runway reference owns invocation triggers",
            briefs,
        )
        self.assertIn("do not replace required `runway_worker`", briefs)
        self.assertIn("or\n  `runway_reviewer` agents", briefs)
        self.assertIn("Prefer one batch-scoped", combined)
        self.assertIn("genuinely independent", combined)
        self.assertIn("The coordinator owns support-agent lifecycle", combined)
        self.assertIn("Do not pass live support-agent", combined)
        self.assertIn("only compact findings", combined)
        self.assertIn('Use agent_type="codebase_investigator".', briefs)
        self.assertIn(
            "Return YAML only using the registered codebase investigator contract.",
            briefs,
        )
        self.assertNotIn("question_answered:", combined)
        self.assertNotIn("files_checked:", combined)


if __name__ == "__main__":
    unittest.main()
