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
                "plan-batch": "1.0.6",
                "work-batch": "1.0.7",
                "batch-runway": "1.5.2",
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
        plan_batch = (REPO_ROOT / "skills/plan-batch/SKILL.md").read_text(
            encoding="utf-8"
        )
        work_batch = (REPO_ROOT / "skills/work-batch/SKILL.md").read_text(
            encoding="utf-8"
        )
        batch_runway = (REPO_ROOT / "skills/batch-runway/SKILL.md").read_text(
            encoding="utf-8"
        )
        create_spec = (
            REPO_ROOT / "skills/batch-runway/references/create-spec.md"
        ).read_text(encoding="utf-8")
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
        execute_spec = (
            REPO_ROOT / "skills/batch-runway/references/execute-spec.md"
        ).read_text(encoding="utf-8")
        execute_recovery = (
            REPO_ROOT / "skills/batch-runway/references/execute-recovery-v1.md"
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
        work_startup = self.markdown_section(
            work_batch, "Cross-Checkout Startup Reconciliation"
        )
        lifecycle_vocabulary = self.markdown_section(
            consumer_contract, "Lifecycle Vocabulary"
        )
        startup_contract = self.markdown_section(
            consumer_contract, "Startup Classifications And Controlled Paths"
        )
        receipt_contract = self.markdown_section(
            consumer_contract, "Lease Renewal And Execution Receipts"
        )
        execute_startup = self.markdown_section(
            execute_spec, "Cross-Checkout Startup Routing"
        )
        recovery_boundary = self.markdown_section(
            execute_recovery, "Cross-Checkout Movement Boundary"
        )
        helper_owner_boundary = self.bounded_text(
            consumer_contract,
            "The mechanism is a temporary bridge",
            "## Lifecycle Vocabulary",
        )
        coordinator_owner_boundary = self.markdown_section(
            consumer_contract, "Planning And Propagation"
        )
        batch_precreation = " ".join(
            (
                self.markdown_section(batch_runway, "Required First Steps"),
                self.markdown_section(batch_runway, "Core Contract"),
            )
        )
        create_precreation = self.bounded_text(
            create_spec,
            "When the selected dispatch explicitly names\n"
            "`cross-checkout-precreation/v1`",
            "When the selected dispatch explicitly names `cross-checkout-context/v1`",
        )
        create_strict = self.bounded_text(
            create_spec,
            "When the selected dispatch explicitly names `cross-checkout-context/v1`",
            "The spec must include:",
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
                    "cross-checkout-precreation-v1.md",
                    "installed helper from the active Codex home",
                    "validate the complete payload and exact intended creation "
                    "targets while they are absent",
                    "must not create either candidate root",
                    "no step for ordinary single-root or strict cross-checkout batches",
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
            "create-spec": (
                create_precreation,
                (
                    "cross-checkout-precreation-v1.md",
                    "installed helper from the active Codex home",
                    "complete payload and exact intended creation targets while they "
                    "are absent",
                    "Planning must not create either target",
                    "must not appear in ordinary single-root or strict cross-checkout "
                    "runways",
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
                    "../batch-runway/references/cross-checkout-context-v1.md",
                    "Require the complete context payload and canonical planning "
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
                    "Complete startup reconciliation before the first strict handoff",
                    "Immediately before every worker and reviewer delegation",
                    "`prepare_cross_checkout_context_refresh(...)` again",
                    "newly prepared exact live execution lease",
                    "Never pass the planning snapshot as the handoff lease",
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
                    "require `work-batch` startup reconciliation before the first "
                    "strict handoff",
                    "new exact live execution lease immediately before every worker "
                    "and reviewer delegation",
                    "validating write scope separately",
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
            "create-spec": (
                create_strict,
                (
                    "explicitly names `cross-checkout-context/v1` or explicitly "
                    "declares separate existing toolchain, canonical-planning, and "
                    "implementation repository roots",
                    "complete payload and canonical planning root with the installed "
                    "helper",
                    "`cross-checkout-precreation/v1` does not use this strict branch",
                    "validated helper-produced transition receipt plus green strict "
                    "context",
                    "pre-transition strict verification remains `null`",
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
        self.assertIn(
            "`prepare_cross_checkout_context_refresh(...)` operation",
            startup_contract,
        )
        for mechanical_fact in (
            "helper owns parsing",
            "root and revision validation",
            "generation binding",
            "write-scope validation",
            "receipt data",
        ):
            with self.subTest(mechanical_fact=mechanical_fact):
                self.assertIn(mechanical_fact, helper_owner_boundary)
        self.assertIn("workflow lifecycle authority", helper_owner_boundary)

        for semantic_owner, contract in (
            ("work-batch", work_startup),
            ("shared-contract", startup_contract),
        ):
            normalized_contract = contract.lower()
            sentences = normalized_contract.split(". ")
            with self.subTest(semantic_owner=semantic_owner):
                self.assertIn("`work-batch` owns", contract)
                self.assertIn("planned and live", normalized_contract)
                self.assertIn("strictly parsed refreshed payload", normalized_contract)
                self.assertTrue(
                    any(
                        "helper" in sentence
                        and "does not" in sentence
                        and "classif" in sentence
                        and "accept" in sentence
                        for sentence in sentences
                    ),
                    f"{semantic_owner} must deny classification and acceptance "
                    "authority to helper output",
                )

        normalized_coordinator_ownership = coordinator_owner_boundary.lower()
        for authority in (
            "selection",
            "execution acceptance",
            "closeout",
        ):
            with self.subTest(coordinator_authority=authority):
                self.assertIn(authority, normalized_coordinator_ownership)
        self.assertIn("coordinator remains the owner", normalized_coordinator_ownership)

        lifecycle_terms = (
            "planning snapshot",
            "startup reconciliation",
            "live execution lease",
            "execution receipt",
        )
        normalized_lifecycle = lifecycle_vocabulary.lower()
        for term in lifecycle_terms:
            with self.subTest(lifecycle_term=term):
                self.assertIn(term, normalized_lifecycle)

        for producer, contract in (
            ("plan-batch", plan_strict),
            ("create-spec", create_strict),
        ):
            normalized_contract = contract.lower()
            with self.subTest(producer=producer):
                self.assertIn("planning snapshot", normalized_contract)
                self.assertIn(
                    "immutable historical planning evidence",
                    normalized_contract,
                )
                self.assertIn("not a live execution lease", normalized_contract)
                self.assertIn("same selected scope", normalized_contract)
                self.assertIn("fresh live lease", normalized_contract)
                self.assertIn("commit that contains", normalized_contract)

        expected_classifications = {
            "expected-queue-establishment",
            "compatible-between-flight-change",
            "conflicting-between-flight-change",
        }
        for owner, contract in (
            ("work-batch", work_startup),
            ("shared-contract", startup_contract),
        ):
            found = {
                classification
                for classification in expected_classifications
                if classification in contract
            }
            with self.subTest(startup_owner=owner):
                self.assertEqual(expected_classifications, found)
                self.assertIn("runway", contract)
                self.assertIn("changed path", contract)
                self.assertIn("prepare_cross_checkout_context_refresh(...)", contract)

        self.assertIn(
            "`work-batch` owns the normal queued-to-executing transition",
            work_startup,
        )
        self.assertIn("before generic unexpected-movement recovery", work_startup)
        self.assertIn("immutable planning snapshot", work_startup)
        self.assertIn("strictly parsed refreshed payload", work_startup)
        self.assertIn("validate_write_scope(...)` separately", work_startup)
        self.assertIn(
            "do not rewrite the planning snapshot or record accepted startup "
            "movement as an orchestration anomaly",
            work_startup,
        )

        for consumer, contract in (
            ("work-batch", work_strict),
            ("batch-runway", execute_precreation),
        ):
            normalized_contract = contract.lower()
            with self.subTest(lease_consumer=consumer):
                self.assertIn(
                    "immediately before every worker and reviewer delegation",
                    normalized_contract,
                )
                self.assertIn("exact live execution lease", normalized_contract)
                self.assertIn("planning snapshot", normalized_contract)

        for receipt_owner, contract in (
            ("work-batch", work_strict),
            ("shared-contract", receipt_contract),
        ):
            normalized_contract = contract.lower().replace("-", " ")
            sentences = normalized_contract.split(". ")
            with self.subTest(receipt_owner=receipt_owner):
                self.assertTrue(
                    any(
                        all(
                            term in sentence
                            for term in (
                                "execution receipt",
                                "accepted action",
                                "exact live lease",
                                "validated scope",
                            )
                        )
                        for sentence in sentences
                    ),
                    f"{receipt_owner} must tie each accepted-action receipt to "
                    "its exact live lease and validated scope",
                )
                self.assertTrue(
                    any(
                        ("must not" in sentence or "never use" in sentence)
                        and "planning snapshot revisions" in sentence
                        and (
                            "later action" in sentence
                            or "live action evidence" in sentence
                        )
                        for sentence in sentences
                    ),
                    f"{receipt_owner} must reject planning-snapshot revisions "
                    "as later action provenance",
                )

        self.assertIn("before unexpected-movement recovery", execute_startup)
        self.assertIn("is not, by itself, a recovery trigger", recovery_boundary)
        self.assertIn("conflicting-between-flight-change", recovery_boundary)
        self.assertIn(
            "No post-lease movement may reach delegation on the old lease",
            recovery_boundary,
        )

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
