from __future__ import annotations

import json
import tomllib
import unittest
from argparse import Namespace
from pathlib import Path
from typing import Any

from scripts import install_codex_config
from scripts.skill_contract import validate_skill_contracts


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
            if feature_name == "skill-authoring":
                continue
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

        manifest_text = MANIFEST.read_text(encoding="utf-8")
        self.assertEqual(manifest_text.count('\n    "skill-authoring": {'), 1)
        self.assertEqual(
            manifest["features"]["skill-authoring"],
            {
                "version": "1.0.0",
                "description": (
                    "Agent-facing authoring support for creating, migrating, "
                    "and auditing contract-first hybrid skills."
                ),
                "links": [
                    {
                        "source": "skills/skill-authoring",
                        "target": "skills/skill-authoring",
                    },
                    {
                        "source": "scripts/skill_contract.py",
                        "target": "scripts/skill_contract.py",
                    },
                    {
                        "source": "schemas/skill-contract-v1.schema.json",
                        "target": "schemas/skill-contract-v1.schema.json",
                    },
                ],
            },
        )
        for link in manifest["features"]["skill-authoring"]["links"]:
            source = Path(link["source"])
            target = Path(link["target"])
            self.assertFalse(source.is_absolute())
            self.assertFalse(target.is_absolute())
            self.assertNotIn("..", source.parts)
            self.assertNotIn("..", target.parts)
            self.assertTrue(REPO_ROOT.joinpath(source).exists())

    def test_manifest_feature_requirements_are_valid(self) -> None:
        manifest = self.load_manifest()
        features = manifest["features"]

        for feature_name, feature in features.items():
            if feature_name == "skill-authoring":
                continue
            with self.subTest(feature=feature_name):
                requirements = feature.get("requires", [])
                self.assertIsInstance(requirements, list)
                for requirement in requirements:
                    self.assertIsInstance(requirement, str)
                    self.assertIn(requirement, features)

        self.assertEqual(
            {
                feature_name: feature.get("requires", [])
                for feature_name, feature in features.items()
                if "skill-authoring" in feature.get("requires", [])
            },
            {},
        )

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
            {
                "skills/planning-state",
                "scripts/planning_state.py",
                "scripts/cross_checkout_context.py",
            },
        )

        args = Namespace(feature=["planning-state"], all_features=False)
        selected = install_codex_config.selected_feature_names(args, manifest)

        self.assertEqual(selected, ["planning-artifacts", "planning-state"])

    def test_cross_checkout_helper_is_available_from_planning_state_during_transfer(
        self,
    ) -> None:
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
            [("planning-state", helper_link)],
        )
        self.assertNotIn("batch-runway", features["plan-batch"]["requires"])
        self.assertIn("planning-state", features["plan-batch"]["requires"])
        self.assertIn("batch-runway", features["work-batch"]["requires"])
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
        for agent_source in (
            "agents/batch_planner.toml",
            "agents/batch_plan_reviewer.toml",
        ):
            with self.subTest(agent_source=agent_source):
                self.assertIn(agent_source, installed_agent_sources)
                instructions = tomllib.loads(
                    (REPO_ROOT / agent_source).read_text(encoding="utf-8")
                )["developer_instructions"]
                self.assertIn("Do not", instructions)
        self.assertEqual(
            {
                name: features[name]["version"]
                for name in (
                    "planning-contracts",
                    "plan-batch",
                    "work-batch",
                    "batch-runway",
                    "custom-agents",
                )
            },
            {
                "planning-contracts": "1.2.0",
                "plan-batch": "2.2.0",
                "work-batch": "1.0.6",
                "batch-runway": "2.0.0",
                "custom-agents": "1.7.0",
            },
        )

    def test_cross_checkout_consumers_share_the_temporary_runtime_contract(
        self,
    ) -> None:
        plan_batch = (REPO_ROOT / "skills/plan-batch/SKILL.md").read_text(
            encoding="utf-8"
        )
        work_batch = (REPO_ROOT / "skills/work-batch/SKILL.md").read_text(
            encoding="utf-8"
        )
        batch_runway = (REPO_ROOT / "skills/batch-runway/SKILL.md").read_text(
            encoding="utf-8"
        )
        consumer_contract = (
            REPO_ROOT / "skills/batch-runway/references/cross-checkout-context-v1.md"
        ).read_text(encoding="utf-8")
        precreation_contract = (
            REPO_ROOT
            / "skills/batch-runway/references/cross-checkout-precreation-v1.md"
        ).read_text(encoding="utf-8")
        execute_core = (
            REPO_ROOT / "skills/batch-runway/references/execute-slice-core-v1.md"
        ).read_text(encoding="utf-8")
        execution_contract = (
            REPO_ROOT / "skills/batch-runway/references/execution-contract-v2.md"
        ).read_text(encoding="utf-8")
        agent_result_contract = (
            REPO_ROOT / "skills/batch-runway/references/agent-result-contract-v2.md"
        ).read_text(encoding="utf-8")
        project_values = (
            REPO_ROOT / "skills/batch-runway/references/project-values.md"
        ).read_text(encoding="utf-8")
        subagent_briefs = (
            REPO_ROOT / "skills/batch-runway/references/subagent-briefs.md"
        ).read_text(encoding="utf-8")

        plan_precreation = self.markdown_section(
            plan_batch, "Explicit Cross-Checkout Pre-Creation Planning"
        )
        work_precreation = self.markdown_section(
            work_batch, "Explicit Cross-Checkout Pre-Creation Execution"
        )
        plan_strict = self.markdown_section(
            plan_batch, "Explicit Strict Cross-Checkout Planning"
        )
        work_strict = self.markdown_section(
            work_batch, "Explicit Strict Cross-Checkout Execution"
        )
        batch_precreation = " ".join(
            (
                self.markdown_section(batch_runway, "Required First Steps"),
                self.markdown_section(batch_runway, "Core Contract"),
            )
        )
        execute_precreation = " ".join(
            (
                self.markdown_section(execute_core, "Source Map"),
                self.markdown_section(execute_core, "Coordinator Invariants"),
                self.markdown_section(execute_core, "Normal Slice Loop"),
            )
        )

        bounded_requirements: dict[str, tuple[str, tuple[str, ...]]] = {
            "plan-batch": (
                plan_precreation,
                (
                    "cross-checkout-precreation/v1",
                    "installed helper from the active Codex home",
                    "validate the complete payload and exact intended creation "
                    "targets while they are absent",
                    "must not create either candidate root",
                    "adds no step for ordinary single-root or strict cross-checkout "
                    "batches",
                ),
            ),
            "work-batch": (
                work_precreation,
                (
                    "cross-checkout-precreation-v1.md",
                    "complete payload and exact intended creation targets with the "
                    "installed helper",
                    "missing, null, or mismatched "
                    "`verified_cross_checkout_precreation`",
                    "`verified_cross_checkout_context` remains `null`",
                    "helper-produced versioned transition receipt",
                    "green strict `cross-checkout-context/v1` payload",
                    "`verified_cross_checkout_precreation` remains `null` for those "
                    "strict results",
                    "no step for ordinary single-root or strict cross-checkout batches",
                ),
            ),
            "batch-runway": (
                batch_precreation,
                (
                    "cross-checkout-precreation-v1.md",
                    "complete `cross-checkout-precreation/v1` payload and exact "
                    "intended creation targets with the installed helper",
                    "missing, null, or mismatched "
                    "`verified_cross_checkout_precreation`",
                    "helper-produced transition receipt and validated strict context",
                    "strict field remains `null` for a pre-creation handoff",
                    "pre-creation field remains `null` for strict handoffs",
                    "Both remain `null`",
                    "adds no step for ordinary single-root work",
                ),
            ),
            "execute-core": (
                execute_precreation,
                (
                    "cross-checkout-precreation-v1.md",
                    "absent targets, and exact creation scope",
                    "missing, null, or mismatched "
                    "`verified_cross_checkout_precreation`",
                    "retained validated pre-creation context",
                    "serialize the versioned transition receipt",
                    "newly validated strict context",
                    "Require `verified_cross_checkout_context`",
                    "require `verified_cross_checkout_precreation` to remain `null`",
                    "adds no step for ordinary single-root or strict cross-checkout "
                    "handoffs",
                ),
            ),
        }
        for consumer, (bounded_contract, requirements) in bounded_requirements.items():
            for requirement in requirements:
                with self.subTest(consumer=consumer, requirement=requirement):
                    self.assertIn(requirement, bounded_contract)

        strict_requirements: dict[str, tuple[str, tuple[str, ...]]] = {
            "plan-batch": (
                plan_strict,
                (
                    "cross-checkout-context/v1",
                    "require the complete context payload and canonical planning "
                    "root, validate them with the installed helper",
                    "preserve both verbatim in that runway",
                    "absent-target payload cannot satisfy this strict "
                    "post-creation contract",
                    "adds no step for ordinary single-root batches",
                ),
            ),
            "work-batch": (
                work_strict,
                (
                    "../batch-runway/references/cross-checkout-context-v1.md",
                    "Revalidate the exact payload and canonical planning root with "
                    "the installed helper",
                    "before every worker or reviewer delegation",
                    "propagate the required mechanical context in each handoff",
                    "pre-creation result field cannot satisfy this strict "
                    "post-creation contract",
                    "adds no step for ordinary single-root batches",
                ),
            ),
            "batch-runway": (
                batch_precreation,
                (
                    "references/cross-checkout-context-v1.md",
                    "validate the complete strict payload and canonical planning "
                    "root with the installed helper before delegation",
                    "propagate them in worker and reviewer handoffs",
                    "pre-creation verification cannot satisfy the strict result field",
                    "Ordinary single-root work uses neither bridge",
                ),
            ),
            "execute-core": (
                execute_precreation,
                (
                    "`cross-checkout-context-v1.md` for explicit strict "
                    "post-creation work",
                    "revalidate the complete strict payload, canonical planning "
                    "root, "
                    "generation identity, repository revisions, and intended "
                    "write scope with the installed helper",
                    "before every worker and reviewer delegation",
                    "Pre-creation verification cannot satisfy this strict invariant",
                    "invariant adds no step for ordinary single-root handoffs",
                ),
            ),
        }
        for consumer, (bounded_contract, requirements) in strict_requirements.items():
            for requirement in requirements:
                with self.subTest(
                    consumer=consumer,
                    strict_requirement=requirement,
                ):
                    self.assertIn(requirement, bounded_contract)

        execution_strict = self.bounded_text(
            execution_contract,
            "- A runway that explicitly names `cross-checkout-context/v1`",
            "- These delegation rules bind the coordinator",
        )
        result_strict = self.markdown_section(
            agent_result_contract,
            "Canonical Owners",
        )
        project_value_strict = self.bounded_text(
            project_values,
            "- `cross_checkout_context`:",
            "- `canonical_planning_root`:",
        )
        coding_handoff_strict = self.markdown_section(
            subagent_briefs,
            "Lean Coding Brief",
        )
        review_handoff_strict = self.markdown_section(
            subagent_briefs,
            "Lean Review Brief",
        )
        support_strict_requirements: dict[str, tuple[str, tuple[str, ...]]] = {
            "execution-contract": (
                execution_strict,
                (
                    "explicitly names `cross-checkout-context/v1` or explicitly "
                    "declares separate existing toolchain, canonical-planning, and "
                    "implementation repository roots",
                    "complete validated strict payload and canonical planning root",
                    "`cross-checkout-precreation/v1` runway remains outside this "
                    "strict branch",
                    "`verified_cross_checkout_context` null",
                    "validated helper-produced transition receipt plus green strict "
                    "context",
                ),
            ),
            "agent-result-contract": (
                result_strict,
                (
                    "explicitly names `cross-checkout-context/v1` or explicitly "
                    "declares separate existing toolchain, canonical-planning, and "
                    "implementation repository roots",
                    "`cross-checkout-precreation/v1` handoff stays outside that "
                    "strict branch",
                    "strict field `null` until a validated helper-produced "
                    "transition receipt plus green strict context exists",
                ),
            ),
            "project-values": (
                project_value_strict,
                (
                    "explicitly names that interface or explicitly declares separate "
                    "existing toolchain, canonical-planning, and implementation "
                    "repository roots",
                    "`cross-checkout-precreation/v1` remains outside this strict value",
                    "strict verification `null` until a validated helper-produced "
                    "transition receipt plus green strict context exists",
                ),
            ),
            "coding-handoff": (
                coding_handoff_strict,
                (
                    "explicitly names `cross-checkout-context/v1` or explicitly "
                    "declares separate existing toolchain, canonical-planning, and "
                    "implementation repository roots",
                    "`cross-checkout-precreation/v1` does not use this strict branch",
                    "validated helper-produced transition receipt plus green strict "
                    "context",
                    "before then its strict field remains null",
                ),
            ),
            "review-handoff": (
                review_handoff_strict,
                (
                    "explicitly names `cross-checkout-context/v1` or explicitly "
                    "declares separate existing toolchain, canonical-planning, and "
                    "implementation repository roots",
                    "`cross-checkout-precreation/v1` does not use this strict branch",
                    "validated helper-produced transition receipt plus green strict "
                    "context",
                    "before then its strict field remains null",
                ),
            ),
        }
        for surface, (
            bounded_contract,
            requirements,
        ) in support_strict_requirements.items():
            for requirement in requirements:
                with self.subTest(
                    strict_surface=surface,
                    routing_requirement=requirement,
                ):
                    self.assertIn(requirement, bounded_contract)

        strict_routing_surfaces = {
            **{
                consumer: bounded_contract
                for consumer, (bounded_contract, _) in strict_requirements.items()
            },
            **{
                surface: bounded_contract
                for surface, (bounded_contract, _) in (
                    support_strict_requirements.items()
                )
            },
        }
        overbroad_strict_triggers = (
            "an explicitly cross-checkout handoff",
            "an explicitly cross-checkout runway",
            "explicitly cross-checkout work",
            "runway is explicitly cross-checkout",
        )
        for surface, bounded_contract in strict_routing_surfaces.items():
            normalized_contract = bounded_contract.lower()
            for overbroad_trigger in overbroad_strict_triggers:
                with self.subTest(
                    strict_surface=surface,
                    rejected_trigger=overbroad_trigger,
                ):
                    self.assertNotIn(overbroad_trigger, normalized_contract)

        self.assertIn("installed helper", consumer_contract)
        self.assertIn("scripts/cross_checkout_context.py", consumer_contract)
        self.assertIn("temporary bridge", consumer_contract)
        self.assertIn("project-owned deletion condition", consumer_contract)

        normalized_precreation = " ".join(precreation_contract.split())
        self.assertIn(
            "installed `scripts/cross_checkout_context.py` helper", precreation_contract
        )
        self.assertIn("parse_cross_checkout_precreation", precreation_contract)
        self.assertIn("validate_precreation_creation_targets", precreation_contract)
        self.assertIn("build_cross_checkout_transition_receipt", precreation_contract)
        self.assertIn("cross_checkout_transition_receipt_to_dict", precreation_contract)
        self.assertIn("Planning must not create either root", normalized_precreation)
        self.assertIn(
            "For ordinary single-root and strict cross-checkout handoffs, "
            "`verified_cross_checkout_precreation` remains `null`",
            normalized_precreation,
        )
        self.assertIn(
            "pre-creation result satisfy a strict handoff",
            normalized_precreation,
        )
        self.assertIn(
            "not a strict handoff merely because it is cross-checkout",
            normalized_precreation,
        )
        self.assertIn(
            "`verified_cross_checkout_context` `null`, until the validated "
            "helper-produced transition receipt plus green strict context",
            normalized_precreation,
        )

    def test_plan_batch_roles_are_registered_with_disjoint_exact_results(self) -> None:
        features = self.load_manifest()["features"]
        installed = {
            link["source"] for link in features["custom-agents"]["links"]
        }
        planner = tomllib.loads(
            (REPO_ROOT / "agents/batch_planner.toml").read_text(encoding="utf-8")
        )
        reviewer = tomllib.loads(
            (REPO_ROOT / "agents/batch_plan_reviewer.toml").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("agents/batch_planner.toml", installed)
        self.assertIn("agents/batch_plan_reviewer.toml", installed)
        self.assertEqual(planner["name"], "batch_planner")
        self.assertEqual(reviewer["name"], "batch_plan_reviewer")

        planner_contract = planner["developer_instructions"]
        reviewer_contract = reviewer["developer_instructions"]
        for fragment in (
            "interface: batch-plan-draft/v1",
            "status: ready | blocked",
            "draft: null | object",
            "blockers: []",
            "validation_profile: exactly one opaque profile id",
            "Do not resolve it as a path, import another\n  workflow",
            "observed_failure, invariants",
            "additions_beyond_minimum",
            "simpler_alternatives_rejected",
            "exact machine-readable\n  value `risk: migration`",
            "ownership_coexistence: temporary",
            "ownership_coexistence: none",
            "smaller alternative and its rejection reason",
            "Do not review or approve the draft",
            "Do not review or approve the draft, choose review evidence, invoke or message\n  batch_plan_reviewer",
        ):
            with self.subTest(role="planner", fragment=fragment):
                self.assertIn(fragment, planner_contract)
        for fragment in (
            "interface: batch-plan-review/v1",
            "verdict: clean | correction_required | blocked",
            "selected_dispatch_sha256: string",
            "draft_sha256: string",
            "approvals_sha256: string",
            "evidence_packet_sha256: string",
            "canonical independent-review evidence packet",
            "exact\n  machine-readable value `risk: migration`",
            "slice_shape_policy: pass | fail",
            "migration_evidence: pass | fail",
            "Reject horizontal phase decomposition",
            "implementation_started: false",
            "Do not modify or produce a replacement draft",
        ):
            with self.subTest(role="reviewer", fragment=fragment):
                self.assertIn(fragment, reviewer_contract)

    def test_cross_checkout_generic_surfaces_remain_project_neutral(self) -> None:
        generic_surfaces = (
            "agents/batch_planner.toml",
            "agents/batch_plan_reviewer.toml",
            "agents/runway_worker.toml",
            "agents/runway_reviewer.toml",
            "skills/plan-batch/SKILL.md",
            "skills/work-batch/SKILL.md",
            "skills/batch-runway/SKILL.md",
            "skills/batch-runway/references/agent-result-contract-v2.md",
            "skills/batch-runway/references/cross-checkout-context-v1.md",
            "skills/batch-runway/references/cross-checkout-precreation-v1.md",
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
            "add-to-ledger": ["planning-contracts"],
            "plan-batch": [
                "planning-contracts",
                "planning-artifacts",
                "planning-state",
                "custom-agents",
            ],
            "work-batch": [
                "planning-artifacts",
                "planning-state",
                "batch-runway",
                "architecture-program-runway",
            ],
        }
        expected_links = {
            "add-to-ledger": {
                ("skills/add-to-ledger", "skills/add-to-ledger"),
                ("scripts/add_to_ledger.py", "scripts/add_to_ledger.py"),
            },
            "plan-batch": {
                ("skills/plan-batch", "skills/plan-batch"),
                ("scripts/plan_batch.py", "scripts/plan_batch.py"),
                (
                    "schemas/slice-shape-policy-v1.schema.json",
                    "schemas/slice-shape-policy-v1.schema.json",
                ),
            },
            "work-batch": {
                ("skills/work-batch", "skills/work-batch"),
            },
        }

        for skill_name, required_features in expected.items():
            with self.subTest(skill=skill_name):
                feature = features[skill_name]
                self.assertEqual(feature.get("requires", []), required_features)
                self.assertEqual(
                    {
                        (link["source"], link["target"])
                        for link in feature["links"]
                    },
                    expected_links[skill_name],
                )

                skill_path = REPO_ROOT / f"skills/{skill_name}/SKILL.md"
                skill_text = skill_path.read_text(encoding="utf-8")
                ui_text = (
                    REPO_ROOT / f"skills/{skill_name}/agents/openai.yaml"
                ).read_text(encoding="utf-8")

                self.assertIn(f"name: {skill_name}", skill_text)
                if "## Stops" not in skill_text:
                    result = validate_skill_contracts(
                        (skill_path,),
                        toolchain_root=REPO_ROOT,
                        complete_catalog=False,
                    )
                    self.assertTrue(
                        result.is_valid,
                        "\n".join(str(diagnostic) for diagnostic in result.diagnostics),
                    )
                    self.assertEqual(len(result.contracts), 1)
                    contract = result.contracts[0].contract
                    identity = contract["identity"]
                    self.assertIsInstance(identity, dict)
                    self.assertEqual(identity["name"], skill_name)
                    self.assertEqual(identity["audience"], "human-command-owner")
                    self.assertTrue(contract["stops_when"])
                else:
                    self.assertIn("## Agent-Facing Support", skill_text)
                    self.assertIn("docs/skill-routing-contract.md", skill_text)
                self.assertIn(f"Use ${skill_name}", ui_text)

        self.assertIn("## Routing Table", routing_contract)
        self.assertIn("## Conflict Rule", routing_contract)
        self.assertIn("## Stop Rule", routing_contract)
        self.assertIn("## Compatibility Label Rule", routing_contract)

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
        architecture_program_runway = (
            REPO_ROOT / "skills/architecture-program-runway/SKILL.md"
        ).read_text(encoding="utf-8")
        batch_runway = (REPO_ROOT / "skills/batch-runway/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "User-facing command-owner skill",
            plan_batch_feature["description"],
        )
        self.assertEqual(
            plan_batch_feature.get("requires", []),
            [
                "planning-contracts",
                "planning-artifacts",
                "planning-state",
                "custom-agents",
            ],
        )
        self.assertEqual(
            {link["source"] for link in plan_batch_feature["links"]},
            {
                "skills/plan-batch",
                "scripts/plan_batch.py",
                "schemas/slice-shape-policy-v1.schema.json",
            },
        )

        self.assertIn("complete human-facing planning command", plan_batch)
        self.assertIn("independent-review evidence packet", plan_batch)
        self.assertIn("DEC-038", plan_batch)
        self.assertIn("Do not route planning through a\nsecond workflow owner", plan_batch)
        self.assertNotIn("architecture-program-runway", plan_batch_feature["requires"])
        self.assertNotIn("batch-runway", plan_batch_feature["requires"])

        self.assertIn("same-batch program closeout reconciliation", features["architecture-program-runway"]["description"])
        self.assertIn("same_batch_closeout_reconciliation", architecture_program_runway)
        self.assertIn("- batch_selection", architecture_program_runway)
        self.assertIn("- queue_state_mutation", architecture_program_runway)
        self.assertIn("execution support", features["batch-runway"]["description"])
        self.assertIn("Batch Runway must not plan", batch_runway)
        self.assertFalse(
            (REPO_ROOT / "skills/batch-runway/references/create-spec.md").exists()
        )

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
        agent_facing_readme = self.bounded_text(
            readme,
            "### Agent-Facing Support And Runtime Surfaces",
            "## Future Runner Extraction",
        )
        workflow_guide = (REPO_ROOT / "docs/workflow-guide.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Skills", readme)
        self.assertIn("docs/workflow-guide.md", readme)
        self.assertIn("### User-Facing Workflow Commands", readme)
        self.assertIn("### Agent-Facing Support And Runtime Surfaces", readme)
        self.assertIn("not the preferred direct commands", agent_facing_readme)
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

        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        user_facing = self.bounded_text(
            readme,
            "### User-Facing Workflow Commands",
            "### Agent-Facing Support And Runtime Surfaces",
        )
        agent_facing = self.bounded_text(
            readme,
            "### Agent-Facing Support And Runtime Surfaces",
            "## Future Runner Extraction",
        )
        skill_text = (
            REPO_ROOT / "skills/skill-authoring/SKILL.md"
        ).read_text(encoding="utf-8")
        ui_text = (
            REPO_ROOT / "skills/skill-authoring/agents/openai.yaml"
        ).read_text(encoding="utf-8")

        self.assertNotIn("`skill-authoring`", user_facing)
        self.assertIn("`skill-authoring`", agent_facing)
        self.assertIn("not a primary human command", agent_facing)
        self.assertIn("Agent-facing", skill_text.split("---", 2)[1])
        self.assertNotIn("Use $skill-authoring", ui_text)

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
