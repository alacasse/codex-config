from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts import architecture_program_runner_artifacts as artifacts
from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner
from scripts import architecture_program_runner_state as runner_state
from scripts import architecture_program_runner_validation as validation
from tests.architecture_program_runner_test_support import runner


class ArchitectureProgramRunnerInputInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name) / "project"
        self.project.mkdir()
        self.artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        self.config = runner.RunnerConfig(
            project=self.project.resolve(),
            program_ledger="project-notes/architecture/program.md",
            max_batches=1,
            execute_batches=True,
            state_path=self.artifact_root / "run-state.json",
            sandbox="workspace-write",
            execute_sandbox=None,
            model=None,
            env_overrides=(),
            dry_run=False,
            resume=False,
            stop_after_phase=None,
            artifact_root=self.artifact_root,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def state_with_active_batch(self) -> dict[str, Any]:
        state = runner.initial_state(self.config)
        state["active_batch_id"] = "batch-1"
        state["active_batch_artifact_root"] = runner.batch_artifact_root(state, "batch-1")
        state["batch_manifest_path"] = runner.batch_manifest_path(state, "batch-1")
        return state

    def make_phase_receipt_result(self, phase: str = "execute") -> dict[str, Any]:
        state = self.state_with_active_batch()
        return {
            "status": "completed",
            "phase": phase,
            "next_phase": "closeout",
            "stop_reason": None,
            "program_ledger": self.config.program_ledger,
            "batch_id": "batch-1",
            "dispatch_path": "project-notes/architecture/dispatch/batch-1.md",
            "spec_path": "project-notes/architecture/batch-1-spec.md",
            "receipt_path": runner_state.phase_receipt_path(state, phase),
            "commit_range": "HEAD~1..HEAD",
            "validation_summary": "pytest passed",
            "review_summary": "clean",
            "evidence_paths": [
                "project-notes/architecture/dispatch/batch-1.md",
                "project-notes/architecture/batch-1-spec.md",
            ],
        }

    def test_input_inventory_path_is_phase_environment_fact_and_prompt_guidance(
        self,
    ) -> None:
        state = self.state_with_active_batch()
        environment = environment_owner.build_phase_environment(
            self.config,
            state,
            "execute",
        )

        prompt = command_owner.build_prompt(
            self.config,
            state,
            "execute",
            environment=environment,
        )

        self.assertEqual(
            environment.expected_input_inventory_path,
            (
                "project-notes/architecture/architecture-program-runs/program/"
                "run-20260626-204812/telemetry/phases/"
                "01-execute.input-inventory.json"
            ),
        )
        self.assertIn("Expected input inventory path for this phase:", prompt)
        self.assertIn(environment.expected_input_inventory_path, prompt)
        self.assertIn("include it in evidence_paths", prompt)

    def test_phase_observation_lists_input_inventory_as_artifact_size_candidate(
        self,
    ) -> None:
        state = self.state_with_active_batch()
        result = self.make_phase_receipt_result()
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")

        telemetry = artifacts.build_phase_telemetry(
            self.config,
            state,
            "execute",
            started_at="2026-06-26T20:48:12Z",
            elapsed_seconds=0.25,
            prompt_bytes=12,
            result=result,
            status="completed",
            error=None,
            execution_meta={"exit_code": 0},
        )

        sizes = {entry["path"]: entry for entry in telemetry["artifact_sizes"]}
        self.assertEqual(telemetry["input_inventory_path"], input_inventory_path)
        self.assertIn(input_inventory_path, sizes)
        self.assertFalse(sizes[input_inventory_path]["exists"])

    def test_phase_result_validation_does_not_yet_enforce_input_inventory_evidence(
        self,
    ) -> None:
        state = self.state_with_active_batch()
        result = self.make_phase_receipt_result()
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")

        self.assertNotIn(input_inventory_path, result["evidence_paths"])
        validation.validate_phase_result(result, current_phase="execute", state=state)
        validation.validate_expected_receipt_path(result, self.config, state)

    def test_phase_result_validation_does_not_yet_enforce_input_inventory_file_exists(
        self,
    ) -> None:
        state = self.state_with_active_batch()
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")
        result = self.make_phase_receipt_result()
        result["evidence_paths"].append(input_inventory_path)

        inventory_file = runner_state.resolve_project_path(
            self.config.project,
            input_inventory_path,
        )
        self.assertFalse(inventory_file.exists())
        validation.validate_phase_result(result, current_phase="execute", state=state)
        validation.validate_expected_receipt_path(result, self.config, state)

    def test_phase_result_validation_does_not_yet_enforce_input_inventory_shape(
        self,
    ) -> None:
        state = self.state_with_active_batch()
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")
        inventory_file = runner_state.resolve_project_path(
            self.config.project,
            input_inventory_path,
        )
        inventory_file.parent.mkdir(parents=True, exist_ok=True)
        inventory_file.write_text('{"not": "an input inventory"}\n', encoding="utf-8")
        result = self.make_phase_receipt_result()
        result["evidence_paths"].append(input_inventory_path)

        validation.validate_phase_result(result, current_phase="execute", state=state)
        validation.validate_expected_receipt_path(result, self.config, state)


if __name__ == "__main__":
    unittest.main()
