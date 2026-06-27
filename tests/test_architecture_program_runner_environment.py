from __future__ import annotations

import unittest

from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner

from tests.architecture_program_runner_test_support import (
    ArchitectureProgramRunnerTestCase,
    runner,
)


class ArchitectureProgramRunnerEnvironmentTests(ArchitectureProgramRunnerTestCase):
    def test_current_state_supplies_expected_receipt_and_input_inventory_paths(
        self,
    ) -> None:
        config = self.structured_config()
        state = runner.initial_state(config)
        state["active_batch_id"] = "batch-1"

        environment = environment_owner.build_phase_environment(config, state, "execute")

        self.assertEqual(
            environment.expected_receipt_path,
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/batches/batch-1/receipts/03-execute.json",
        )
        self.assertEqual(
            environment.expected_input_inventory_path,
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/telemetry/phases/01-execute.input-inventory.json",
        )

    def test_prompt_artifact_environment_facts_are_derived_from_current_state(
        self,
    ) -> None:
        config = self.structured_config()
        state = runner.initial_state(config)
        state["active_batch_id"] = "batch-1"
        state["active_batch_artifact_root"] = runner.batch_artifact_root(state, "batch-1")
        state["dispatch_path"] = "project-notes/architecture/dispatch/batch-1.md"
        state["spec_path"] = "project-notes/architecture/batch-1-spec.md"
        state["last_receipt_path"] = (
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/receipts/02-create-spec.json"
        )
        state["batch_manifest_path"] = runner.batch_manifest_path(state, "batch-1")

        environment = environment_owner.build_phase_environment(config, state, "execute")
        prompt = command_owner.build_prompt(config, state, "execute")

        self.assertEqual(environment.artifact_facts["active_batch_id"], "batch-1")
        self.assertEqual(
            environment.artifact_facts["run_manifest_path"],
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/run-manifest.json",
        )
        self.assertIn("- active_batch_id: batch-1", prompt)
        self.assertIn(
            "- artifact_root: project-notes/architecture/architecture-program-runs/"
            "program/run-20260626-204812",
            prompt,
        )
        self.assertIn(
            "- active_batch_artifact_root: "
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/batches/batch-1",
            prompt,
        )
        self.assertIn(
            "- dispatch_path: project-notes/architecture/dispatch/batch-1.md",
            prompt,
        )
        self.assertIn("- spec_path: project-notes/architecture/batch-1-spec.md", prompt)
        self.assertIn(
            "- last_receipt_path: project-notes/architecture/architecture-program-runs/"
            "program/run-20260626-204812/receipts/02-create-spec.json",
            prompt,
        )
        self.assertIn(
            "- run_manifest_path: project-notes/architecture/architecture-program-runs/"
            "program/run-20260626-204812/run-manifest.json",
            prompt,
        )
        self.assertIn(
            "- batch_manifest_path: project-notes/architecture/architecture-program-runs/"
            "program/run-20260626-204812/batches/batch-1/batch-manifest.json",
            prompt,
        )

    def test_environment_owner_supplies_launch_and_label_facts(self) -> None:
        config = self.structured_config()
        config = runner.RunnerConfig(
            **{
                **config.__dict__,
                "max_batches": None,
                "execute_sandbox": "danger-full-access",
                "env_overrides": (
                    ("UV_CACHE_DIR", "/tmp/cache-path"),
                    ("UV_CACHE_DIR", "/tmp/other-cache-path"),
                    ("TOKEN", "secret"),
                ),
            }
        )

        environment = environment_owner.build_phase_environment(
            config,
            runner.initial_state(config),
            "execute",
        )

        self.assertEqual(
            environment.schema_path,
            environment_owner.SCHEMA_PATH,
        )
        self.assertEqual(
            environment.runner_reference_path,
            environment_owner.RUNNER_REFERENCE_PATH,
        )
        self.assertEqual(
            environment.batch_limit_label,
            "all executable batches until stop condition",
        )
        self.assertEqual(environment.env_override_key_label, "UV_CACHE_DIR, TOKEN")
        self.assertEqual(environment.sandbox, "danger-full-access")

    def test_environment_owner_applies_subprocess_env_without_exposing_values(self) -> None:
        environment = environment_owner.build_phase_environment(
            self.config,
            runner.initial_state(self.config),
            "select-dispatch",
        )

        env = environment.subprocess_env(
            (("OVERRIDE_ME", "new"), ("ADDED", "value")),
            base_env={"KEEP_ME": "yes", "OVERRIDE_ME": "old"},
        )

        self.assertEqual(env["KEEP_ME"], "yes")
        self.assertEqual(env["OVERRIDE_ME"], "new")
        self.assertEqual(env["ADDED"], "value")


if __name__ == "__main__":
    unittest.main()
