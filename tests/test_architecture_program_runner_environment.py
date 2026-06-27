from __future__ import annotations

import unittest

from scripts import architecture_program_runner_command as command_owner

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

        self.assertEqual(
            runner.phase_receipt_path(state, "execute"),
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/batches/batch-1/receipts/03-execute.json",
        )
        self.assertEqual(
            runner.phase_input_inventory_path(state, "execute"),
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

        prompt = command_owner.build_prompt(config, state, "execute")

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


if __name__ == "__main__":
    unittest.main()
