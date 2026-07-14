from __future__ import annotations

import json
import tomllib
import unittest
from argparse import Namespace
from pathlib import Path
from typing import Any

from scripts import cross_checkout_context as context_owner
from scripts import install_codex_config


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "codex-features.json"
SKILLS_LOCK = REPO_ROOT / "skills-lock.json"


class CodexFeaturesManifestTests(unittest.TestCase):
    def load_manifest(self) -> dict[str, Any]:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def markdown_section(self, text: str, heading: str) -> str:
        marker = f"## {heading}\n"
        start = text.index(marker) + len(marker)
        end = text.find("\n## ", start)
        if end == -1:
            end = len(text)
        return " ".join(text[start:end].split())

    def bounded_text(self, text: str, start_marker: str, end_marker: str) -> str:
        start = text.index(start_marker)
        end = text.index(end_marker, start + len(start_marker))
        return " ".join(text[start:end].split())

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

    def test_cross_checkout_helper_is_installed_only_by_batch_runway(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]
        helper_link = {
            "source": "scripts/cross_checkout_context.py",
            "target": "scripts/cross_checkout_context.py",
        }

        helper_source = (REPO_ROOT / helper_link["source"]).resolve()
        helper_target = Path(helper_link["target"])
        helper_installations = [
            (feature_name, link)
            for feature_name, feature in features.items()
            for link in feature["links"]
            if (REPO_ROOT / link["source"]).resolve() == helper_source
            or Path(link["target"]) == helper_target
        ]
        self.assertEqual(
            helper_installations,
            [("batch-runway", helper_link)],
        )
        for consumer in ("plan-batch", "work-batch"):
            with self.subTest(consumer=consumer):
                self.assertIn("batch-runway", features[consumer]["requires"])
        installed_agent_sources = {
            link["source"] for link in features["custom-agents"]["links"]
        }
        for agent_source in (
            "agents/runway_worker.toml",
            "agents/runway_reviewer.toml",
        ):
            with self.subTest(agent_source=agent_source):
                self.assertIn(agent_source, installed_agent_sources)
                agent = tomllib.loads(
                    (REPO_ROOT / agent_source).read_text(encoding="utf-8")
                )
                instructions = agent["developer_instructions"]
                self.assertIn(
                    "verified_cross_checkout_precreation: null",
                    instructions,
                )
                self.assertIn(
                    "verified_cross_checkout_context: null",
                    instructions,
                )
        self.assertEqual(
            {
                name: features[name]["version"]
                for name in (
                    "plan-batch",
                    "work-batch",
                    "batch-runway",
                    "custom-agents",
                )
            },
            {
                "plan-batch": "1.0.7",
                "work-batch": "1.0.8",
                "batch-runway": "1.5.4",
                "custom-agents": "1.4.1",
            },
        )
        self.assertEqual(
            context_owner.DELETION_CONDITION,
            "CCFG-29 final integration",
        )

    def test_cross_checkout_consumers_share_the_temporary_runtime_contract(
        self,
    ) -> None:
        surfaces = {
            name: (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for name, relative_path in {
                "plan-batch": "skills/plan-batch/SKILL.md",
                "work-batch": "skills/work-batch/SKILL.md",
                "create-spec": "skills/batch-runway/references/create-spec.md",
                "execute-spec": "skills/batch-runway/references/execute-spec.md",
                "execute-core": (
                    "skills/batch-runway/references/execute-slice-core-v1.md"
                ),
                "execute-recovery": (
                    "skills/batch-runway/references/execute-recovery-v1.md"
                ),
            }.items()
        }
        bridge = (
            REPO_ROOT / "skills/batch-runway/references/cross-checkout-context-v1.md"
        ).read_text(encoding="utf-8")
        precreation = " ".join(
            (
                REPO_ROOT
                / "skills/batch-runway/references/cross-checkout-precreation-v1.md"
            )
            .read_text(encoding="utf-8")
            .split()
        )

        for owner, text in surfaces.items():
            with self.subTest(canonical_bridge_consumer=owner):
                self.assertIn("cross-checkout-context-v1.md", text)

        self.assertIn("temporary bridge", bridge)
        self.assertIn("project-owned deletion condition", bridge)
        self.assertIn("scripts/cross_checkout_context.py", bridge)
        self.assertIn("preflight_cross_checkout_live_lease(...)", bridge)
        self.assertIn("The preflight result contains only `status`", bridge)
        self.assertIn("diagnostic `reason`, and", bridge)
        self.assertIn("`live_context`", bridge)
        self.assertIn("Proceed only on `status: ready`", bridge)
        self.assertIn("`status: blocked` has a null context", bridge)
        self.assertIn("consumers must not reinterpret its reason", bridge)
        self.assertIn("Validate intended write scope separately", bridge)
        self.assertIn("Before every later delegation", bridge)
        self.assertIn("prepare_cross_checkout_context_refresh(...)", bridge)
        self.assertIn("verified_cross_checkout_context", bridge)
        self.assertIn("execution receipt", bridge)
        self.assertIn("Never use planning-snapshot revisions", bridge)
        self.assertIn("The coordinator remains the owner", bridge)

        plan_strict = self.markdown_section(
            surfaces["plan-batch"], "Explicit Strict Cross-Checkout Planning"
        )
        create_strict = self.bounded_text(
            surfaces["create-spec"],
            "When the selected dispatch explicitly names `cross-checkout-context/v1`",
            "The spec must include:",
        )
        for producer, text in (
            ("plan-batch", plan_strict),
            ("create-spec", create_strict),
        ):
            with self.subTest(snapshot_producer=producer):
                self.assertIn("planning snapshot", text.lower())
                self.assertIn("immutable historical planning evidence", text.lower())
                self.assertIn("not a live execution lease", text.lower())
                self.assertIn("same selected scope", text.lower())
                self.assertIn("ready/blocked preflight", text.lower())

        work_preflight = self.markdown_section(
            surfaces["work-batch"], "Cross-Checkout Ready/Blocked Preflight"
        )
        self.assertIn("same runway is still the only queued or active batch", work_preflight)
        self.assertIn("exact queue-establishment transaction", work_preflight)
        self.assertIn("preflight_cross_checkout_live_lease(...)", work_preflight)
        self.assertIn("Proceed only when it returns `status: ready`", work_preflight)
        self.assertIn("Treat `status: blocked`", work_preflight)
        self.assertIn("without reclassifying it", work_preflight)
        self.assertIn("validate_write_scope(...)", work_preflight)
        self.assertIn("retains every proceed, stop, recovery", work_preflight)
        self.assertIn("does not mutate planning state", work_preflight)

        execute_preflight = self.markdown_section(
            surfaces["execute-spec"], "Cross-Checkout Preflight Routing"
        )
        self.assertIn("same runway as the only queued or active batch", execute_preflight)
        self.assertIn("exact current queue transaction paths", execute_preflight)
        self.assertIn("Proceed only on `status: ready`", execute_preflight)
        self.assertIn("`status: blocked`", execute_preflight)
        self.assertIn("without reinterpreting the diagnostic reason", execute_preflight)

        core = " ".join(surfaces["execute-core"].split())
        self.assertIn("ready/blocked preflight before the", core)
        self.assertIn("live context for that immediate first handoff", core)
        self.assertIn("preparing a new exact live", core)
        self.assertIn("execution lease before every later", core)
        self.assertIn("validating write scope separately", core)
        self.assertIn("rejecting missing, null, or mismatched verified identity", core)
        self.assertIn("prepare_cross_checkout_context_refresh(...)", core)

        recovery = self.markdown_section(
            surfaces["execute-recovery"], "Cross-Checkout Movement Boundary"
        )
        self.assertIn("A ready result supplies the first strictly parsed live context", recovery)
        self.assertIn("A blocked result, null context, helper failure", recovery)
        self.assertIn("without reinterpreting the helper's reason", recovery)
        self.assertIn("No post-lease movement may reach delegation on the old lease", recovery)

        for owner in ("plan-batch", "work-batch", "create-spec", "execute-core"):
            with self.subTest(precreation_consumer=owner):
                self.assertIn("cross-checkout-precreation/v1", surfaces[owner])
        self.assertIn("parse_cross_checkout_precreation", precreation)
        self.assertIn("validate_precreation_creation_targets", precreation)
        self.assertIn("build_cross_checkout_transition_receipt", precreation)
        self.assertIn("cross_checkout_transition_receipt_to_dict", precreation)
        self.assertIn("Planning must not create either root", precreation)
        self.assertIn("pre-creation result satisfy a strict handoff", precreation)

    def test_cross_checkout_generic_surfaces_remain_project_neutral(self) -> None:
        generic_surfaces = (
            "agents/runway_worker.toml",
            "agents/runway_reviewer.toml",
            "skills/plan-batch/SKILL.md",
            "skills/work-batch/SKILL.md",
            "skills/batch-runway/SKILL.md",
            "skills/batch-runway/references/agent-result-contract-v2.md",
            "skills/batch-runway/references/create-spec.md",
            "skills/batch-runway/references/cross-checkout-context-v1.md",
            "skills/batch-runway/references/cross-checkout-precreation-v1.md",
            "skills/batch-runway/references/execute-spec.md",
            "skills/batch-runway/references/execute-recovery-v1.md",
            "skills/batch-runway/references/execute-slice-core-v1.md",
            "skills/batch-runway/references/execution-contract-v2.md",
            "skills/batch-runway/references/project-values.md",
            "skills/batch-runway/references/subagent-briefs.md",
        )
        forbidden_fragments = (
            "/home/alacasse/",
            "codex-config",
            "command-owner-redesign",
            "CCFG-",
        )

        for relative_path in generic_surfaces:
            text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                for fragment in forbidden_fragments:
                    self.assertNotIn(fragment, text)

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
                "architecture-program-runway",
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

                skill_text = (REPO_ROOT / f"skills/{skill_name}/SKILL.md").read_text(
                    encoding="utf-8"
                )
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

    def test_work_batch_reconciles_same_batch_closeout(self) -> None:
        manifest = self.load_manifest()
        work_batch_feature = manifest["features"]["work-batch"]
        work_batch = (REPO_ROOT / "skills/work-batch/SKILL.md").read_text(
            encoding="utf-8"
        )
        workflow_guide = (REPO_ROOT / "docs/workflow-guide.md").read_text(
            encoding="utf-8"
        )
        routing_contract = (REPO_ROOT / "docs/skill-routing-contract.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "architecture-program-runway",
            work_batch_feature.get("requires", []),
        )
        self.assertIn("## Same-Batch Closeout Reconciliation", work_batch)
        self.assertIn("`closeout-runway` mode", work_batch)
        self.assertIn("same-batch program reconciliation", work_batch)
        self.assertIn("just-completed batch only", work_batch)
        self.assertIn("Successor selection remains owned", work_batch)
        self.assertIn("same-batch program-state", workflow_guide)
        self.assertIn("Successor planning still requires", workflow_guide)
        self.assertIn(
            "`architecture-program-runway` in `closeout-runway` mode",
            routing_contract,
        )
        self.assertIn("completed batch only", routing_contract)
        self.assertIn(
            "same-batch closeout reconciliation as permission to",
            routing_contract,
        )
        self.assertIn(
            "select, dispatch, refresh, create, or prepare successor work",
            work_batch,
        )
        self.assertNotIn(
            "must not reconcile the program ledger after closeout\n"
            "unless the user explicitly asks",
            work_batch,
        )
        self.assertNotIn("Post-Closeout Handoff", work_batch)
        self.assertNotIn("post-closeout handoff", work_batch)
        self.assertNotIn(
            "program-state reconciliation is a separate\n  explicit request",
            workflow_guide,
        )
        self.assertIn("no new batch was selected", work_batch)

    def test_plan_batch_command_owner_runtime_boundaries_are_explicit(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]
        plan_batch_feature = features["plan-batch"]
        plan_batch = (REPO_ROOT / "skills/plan-batch/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "User-facing command-owner skill",
            plan_batch_feature["description"],
        )
        self.assertEqual(
            plan_batch_feature.get("requires", []),
            [
                "planning-artifacts",
                "planning-state",
                "architecture-program-runway",
                "batch-runway",
            ],
        )
        self.assertEqual(
            {link["source"] for link in plan_batch_feature["links"]},
            {"skills/plan-batch"},
        )

        for runtime_owner in ("architecture-program-runway", "batch-runway"):
            with self.subTest(runtime_owner=runtime_owner):
                self.assertIn(
                    "Agent-facing",
                    features[runtime_owner]["description"],
                )
                self.assertNotIn(
                    "deprecated",
                    features[runtime_owner]["description"].lower(),
                )

        self.assertIn("ledger-source rule", plan_batch)
        self.assertIn("stop-before-implementation boundary", plan_batch)
        self.assertIn(
            "This skill reads executable work only from the current program ledger",
            plan_batch,
        )
        self.assertIn("Do not scan external sources to discover new work", plan_batch)
        self.assertIn("Select bounded work from the current program ledger", plan_batch)
        self.assertIn("Do not select different work. Use that dispatch.", plan_batch)
        self.assertIn("Do not create another spec or replace the queue.", plan_batch)
        self.assertIn("Do not create another spec or execute it.", plan_batch)
        self.assertIn("Stop and report that `add-to-ledger` must ingest", plan_batch)
        self.assertIn("at most one concrete batch runway spec", plan_batch)
        self.assertIn("Stop before implementation", plan_batch)
        self.assertIn("## Agent-Facing Support", plan_batch)
        self.assertIn("`../architecture-program-runway/SKILL.md`", plan_batch)
        self.assertIn("only for program selection", plan_batch)
        self.assertIn("dispatch ownership", plan_batch)
        self.assertIn(
            "`../batch-runway/SKILL.md` only in `create-spec` mode",
            plan_batch,
        )
        self.assertIn("runtime support", plan_batch)

    def test_executable_work_source_boundary_is_explicit(self) -> None:
        routing_contract = (REPO_ROOT / "docs/skill-routing-contract.md").read_text(
            encoding="utf-8"
        )
        add_to_ledger = (REPO_ROOT / "skills/add-to-ledger/SKILL.md").read_text(
            encoding="utf-8"
        )
        plan_batch = (REPO_ROOT / "skills/plan-batch/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("## Executable Work Source", routing_contract)
        self.assertIn(
            "program ledger is the only normal executable backlog source for\n"
            "`plan-batch`",
            routing_contract,
        )
        self.assertIn("explicit ingestion boundary", add_to_ledger)
        self.assertIn("GitHub issues", add_to_ledger)
        self.assertIn("external tickets", add_to_ledger)
        self.assertIn("Do not scan external sources to discover new work", plan_batch)
        self.assertIn(
            "evidence only when an\nexisting ledger row points to them",
            plan_batch,
        )

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
        workflow_guide = (REPO_ROOT / "docs/workflow-guide.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Skills", readme)
        self.assertIn("docs/workflow-guide.md", readme)
        self.assertIn("### User-Facing Workflow Commands", readme)
        self.assertIn("### Agent-Facing Support And Runtime Surfaces", readme)
        self.assertIn("not the preferred direct commands", readme)
        self.assertIn("## Canonical Pipeline", workflow_guide)
        self.assertIn("-> add-to-ledger", workflow_guide)
        self.assertIn("-> program ledger", workflow_guide)
        self.assertIn("-> plan-batch", workflow_guide)
        self.assertIn("-> work-batch", workflow_guide)
        self.assertIn(
            "program ledger is the only normal executable backlog source",
            workflow_guide,
        )
        self.assertIn(
            "External skills and GitHub issues are candidate/evidence sources",
            workflow_guide,
        )
        self.assertIn("docs/skill-routing-contract.md", readme)

    def test_external_skill_lock_blocks_implement_skill(self) -> None:
        skills_lock = json.loads(SKILLS_LOCK.read_text(encoding="utf-8"))
        workflow_guide = (REPO_ROOT / "docs/workflow-guide.md").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("implement", skills_lock["skills"])
        self.assertNotIn("- `implement`", workflow_guide)

    def test_repository_root_plans_directory_is_not_recreated(self) -> None:
        self.assertFalse(
            (REPO_ROOT / "plans").exists(),
            "repository-root plans/ is retired; use docs/plans/CURRENT.md",
        )

        current = (REPO_ROOT / "docs/plans/CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("Repository-root `plans/` is retired", current)
        self.assertIn("docs/plans/archive/compatibility/root-plans/", current)

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
        direct_prompt_skills: set[str] = set()
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
                skill_text = (REPO_ROOT / f"skills/{skill_name}/SKILL.md").read_text(
                    encoding="utf-8"
                )
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
