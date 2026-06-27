from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from scripts import architecture_program_runner_state as runner_state
from scripts import architecture_program_runner_validation as validation


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_RESULT_SCHEMA = (
    REPO_ROOT
    / "skills"
    / "architecture-program-runway"
    / "references"
    / "local-runner-phase-result.schema.json"
)


class ArchitectureProgramRunnerValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name) / "project"
        self.project.mkdir()
        self.config = SimpleNamespace(
            project=self.project.resolve(),
            program_ledger="project-notes/architecture/program.md",
            max_batches=1,
            execute_batches=True,
            artifact_root=None,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def make_result(self, phase: str, next_phase: str, **overrides: Any) -> dict[str, Any]:
        result = {
            "status": "completed",
            "phase": phase,
            "next_phase": next_phase,
            "stop_reason": None,
            "program_ledger": self.config.program_ledger,
            "batch_id": "batch-1",
            "dispatch_path": "project-notes/architecture/dispatch/batch-1.md",
            "spec_path": "project-notes/architecture/batch-1-spec.md",
            "receipt_path": f"project-notes/architecture/receipts/{phase}.json",
            "commit_range": None,
            "validation_summary": None,
            "review_summary": None,
            "evidence_paths": [],
        }
        result.update(overrides)
        return result

    def initial_state(self) -> dict[str, Any]:
        return runner_state.initial_state(self.config)

    def structured_state_and_config(self) -> tuple[dict[str, Any], SimpleNamespace]:
        artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        config = SimpleNamespace(**{**self.config.__dict__, "artifact_root": artifact_root})
        state = runner_state.initial_state(config)
        state["active_batch_id"] = "batch-1"
        state["active_batch_artifact_root"] = runner_state.batch_artifact_root(
            state,
            "batch-1",
        )
        state["batch_manifest_path"] = runner_state.batch_manifest_path(state, "batch-1")
        return state, config

    def write_receipt(self, result: dict[str, Any]) -> None:
        path = runner_state.resolve_project_path(self.config.project, result["receipt_path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result), encoding="utf-8")

    def write_input_inventory(self, state: dict[str, Any], phase: str = "execute") -> str:
        inventory_path = runner_state.phase_input_inventory_path(state, phase)
        self.assertIsNotNone(inventory_path)
        resolved = runner_state.resolve_project_path(self.config.project, inventory_path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "phase": phase,
                    "primary_inputs": [],
                    "broad_reads": [],
                    "large_file_reads": [],
                    "subagent_reports": [],
                }
            ),
            encoding="utf-8",
        )
        return str(inventory_path)

    def test_phase_result_schema_uses_supported_codex_output_subset(self) -> None:
        schema = json.loads(PHASE_RESULT_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(schema["required"], list(validation.REQUIRED_RESULT_FIELDS))
        self.assertEqual(schema["additionalProperties"], False)
        self.assertEqual(validation.schema_keyword_paths(schema), [])
        self.assertEqual(validation.schema_subset_violations(schema), [])

    def test_nullable_stopped_result_is_valid(self) -> None:
        result = self.make_result(
            "select-dispatch",
            "stopped",
            status="stopped",
            stop_reason="no ready batch",
            batch_id=None,
            dispatch_path=None,
            spec_path=None,
            commit_range=None,
            validation_summary=None,
            review_summary=None,
            evidence_paths=[],
        )

        validation.validate_phase_result(result, current_phase="select-dispatch")

    def test_invalid_status_and_next_phase_combination_fails(self) -> None:
        result = self.make_result("execute", "closeout", status="failed")

        with self.assertRaisesRegex(runner_state.RunnerError, "status=failed"):
            validation.validate_phase_result(result, current_phase="execute")

    def test_state_dependent_next_phase_fails_when_create_spec_would_stop(self) -> None:
        config = SimpleNamespace(**{**self.config.__dict__, "execute_batches": False})
        state = runner_state.initial_state(config)
        result = self.make_result("create-spec", "execute")

        with self.assertRaisesRegex(runner_state.RunnerError, "cannot advance"):
            validation.validate_phase_result(result, current_phase="create-spec", state=state)

    def test_required_fields_and_summary_shape_are_validated(self) -> None:
        missing = self.make_result("select-dispatch", "create-spec")
        del missing["receipt_path"]
        with self.assertRaisesRegex(runner_state.RunnerError, "missing required"):
            validation.validate_phase_result(missing)

        summary = self.make_result("execute", "closeout", review_summary={"status": "clean"})
        with self.assertRaisesRegex(runner_state.RunnerError, "review_summary"):
            validation.validate_phase_result(summary)

    def test_receipt_content_must_match_phase_result(self) -> None:
        state = self.initial_state()
        result = self.make_result("select-dispatch", "create-spec")
        self.write_receipt({**result, "batch_id": "different"})

        with self.assertRaisesRegex(runner_state.RunnerError, "does not match"):
            validation.validate_receipt(result, self.config, state)

    def test_structured_receipt_requires_input_inventory_evidence(self) -> None:
        state, config = self.structured_state_and_config()
        expected_receipt = runner_state.phase_receipt_path(state, "execute")
        result = self.make_result("execute", "closeout", receipt_path=expected_receipt)
        self.write_receipt(result)

        with self.assertRaisesRegex(runner_state.RunnerError, "evidence_paths"):
            validation.validate_receipt(result, config, state)

    def test_structured_receipt_requires_input_inventory_file(self) -> None:
        state, config = self.structured_state_and_config()
        expected_receipt = runner_state.phase_receipt_path(state, "execute")
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")
        result = self.make_result(
            "execute",
            "closeout",
            receipt_path=expected_receipt,
            evidence_paths=[input_inventory_path],
        )
        self.write_receipt(result)

        with self.assertRaisesRegex(runner_state.RunnerError, "input inventory"):
            validation.validate_receipt(result, config, state)

    def test_structured_receipt_accepts_valid_input_inventory_evidence(self) -> None:
        state, config = self.structured_state_and_config()
        expected_receipt = runner_state.phase_receipt_path(state, "execute")
        input_inventory_path = self.write_input_inventory(state, "execute")
        result = self.make_result(
            "execute",
            "closeout",
            receipt_path=expected_receipt,
            evidence_paths=[input_inventory_path],
        )
        self.write_receipt(result)

        validation.validate_receipt(result, config, state)

    def test_structured_receipt_path_must_match_runner_expected_path(self) -> None:
        artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        config = SimpleNamespace(**{**self.config.__dict__, "artifact_root": artifact_root})
        state = runner_state.initial_state(config)
        expected = runner_state.phase_receipt_path(state, "select-dispatch")
        self.assertIsNotNone(expected)
        result = self.make_result(
            "select-dispatch",
            "create-spec",
            receipt_path="project-notes/architecture/receipts/select-dispatch.json",
        )

        with self.assertRaisesRegex(runner_state.RunnerError, "expected path"):
            validation.validate_expected_receipt_path(result, config, state)

        matching = {**result, "receipt_path": expected}
        validation.validate_expected_receipt_path(matching, config, state)

    def test_validation_owner_exposes_input_inventory_helpers(self) -> None:
        inventory = {
            "schema_version": 1,
            "phase": "execute",
            "primary_inputs": [],
            "broad_reads": [],
            "large_file_reads": [],
            "subagent_reports": [],
        }

        validation.validate_input_inventory(inventory, active_phase="execute")
        self.assertEqual(
            validation.resolve_project_relative_input_path(self.project, "README.md"),
            self.project / "README.md",
        )


if __name__ == "__main__":
    unittest.main()
