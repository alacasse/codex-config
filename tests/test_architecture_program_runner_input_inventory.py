from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts import architecture_program_runner_artifacts as artifacts
from scripts import architecture_program_runner_command as command_owner
from scripts import architecture_program_runner_environment as environment_owner
from scripts import architecture_program_runner_input_inventory as input_inventory
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

    def write_input_inventory(
        self,
        state: dict[str, Any],
        phase: str = "execute",
        inventory: dict[str, Any] | None = None,
    ) -> str:
        input_inventory_path = runner_state.phase_input_inventory_path(state, phase)
        assert input_inventory_path is not None
        inventory_file = runner_state.resolve_project_path(
            self.config.project,
            input_inventory_path,
        )
        inventory_file.parent.mkdir(parents=True, exist_ok=True)
        inventory_file.write_text(
            json.dumps(inventory or self.minimal_inventory(phase)),
            encoding="utf-8",
        )
        return input_inventory_path

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

    def test_input_inventory_evidence_requires_expected_path(self) -> None:
        state = self.state_with_active_batch()
        result = self.make_phase_receipt_result()
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")
        self.write_input_inventory(state)

        self.assertNotIn(input_inventory_path, result["evidence_paths"])
        with self.assertRaisesRegex(runner_state.RunnerError, "evidence_paths"):
            validation.validate_input_inventory_evidence(self.project, result, state)

    def test_input_inventory_evidence_requires_expected_file(self) -> None:
        state = self.state_with_active_batch()
        input_inventory_path = runner_state.phase_input_inventory_path(state, "execute")
        result = self.make_phase_receipt_result()
        result["evidence_paths"].append(input_inventory_path)

        inventory_file = runner_state.resolve_project_path(
            self.config.project,
            input_inventory_path,
        )
        self.assertFalse(inventory_file.exists())
        with self.assertRaisesRegex(runner_state.RunnerError, "input inventory"):
            validation.validate_input_inventory_evidence(self.project, result, state)

    def test_input_inventory_evidence_validates_expected_file_shape(self) -> None:
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

        with self.assertRaisesRegex(runner_state.RunnerError, "input inventory"):
            validation.validate_input_inventory_evidence(self.project, result, state)

    def test_input_inventory_evidence_accepts_valid_expected_file(self) -> None:
        state = self.state_with_active_batch()
        input_inventory_path = self.write_input_inventory(state)
        result = self.make_phase_receipt_result()
        result["evidence_paths"].append(input_inventory_path)

        validation.validate_input_inventory_evidence(self.project, result, state)

    def minimal_inventory(self, phase: str = "execute") -> dict[str, Any]:
        return {
            "schema_version": 1,
            "phase": phase,
            "primary_inputs": [],
            "broad_reads": [],
            "large_file_reads": [],
            "subagent_reports": [],
        }

    def test_input_inventory_owner_accepts_minimal_empty_inventory(self) -> None:
        input_inventory.validate_input_inventory(
            self.minimal_inventory(),
            active_phase="execute",
        )

    def test_input_inventory_owner_accepts_compact_entries(self) -> None:
        inventory = self.minimal_inventory()
        inventory["primary_inputs"].append(
            {
                "path": "project-notes/architecture/program.md",
                "reason": "active ledger",
            }
        )
        inventory["broad_reads"].append(
            {
                "path": "scripts/architecture_program_runner.py",
                "command": "sed -n '1,80p' scripts/architecture_program_runner.py",
                "reason": "runner compatibility surface",
            }
        )
        inventory["large_file_reads"].append(
            {
                "path": "plans/codex-config-architecture-program-runner.md",
                "byte_count": 1024,
                "reason": "slice spec",
            }
        )
        inventory["subagent_reports"].append(
            {
                "path": "plans/reviews/slice-2.md",
                "role": "reviewer",
                "reason": "review evidence",
            }
        )

        input_inventory.validate_input_inventory(inventory, active_phase="execute")

    def test_input_inventory_owner_rejects_top_level_shape_errors(self) -> None:
        with self.assertRaisesRegex(runner_state.RunnerError, "JSON object"):
            input_inventory.validate_input_inventory([], active_phase="execute")

        missing = self.minimal_inventory()
        del missing["primary_inputs"]
        with self.assertRaisesRegex(runner_state.RunnerError, "missing required"):
            input_inventory.validate_input_inventory(missing, active_phase="execute")

        extra = {**self.minimal_inventory(), "transcript": "session.jsonl"}
        with self.assertRaisesRegex(runner_state.RunnerError, "unsupported field"):
            input_inventory.validate_input_inventory(extra, active_phase="execute")

    def test_input_inventory_owner_rejects_wrong_phase_and_non_array_sections(self) -> None:
        with self.assertRaisesRegex(runner_state.RunnerError, "active phase"):
            input_inventory.validate_input_inventory(
                self.minimal_inventory("create-spec"),
                active_phase="execute",
            )

        inventory = self.minimal_inventory()
        inventory["phase"] = 1
        with self.assertRaisesRegex(runner_state.RunnerError, "phase must be a string"):
            input_inventory.validate_input_inventory(inventory, active_phase="execute")

        inventory = self.minimal_inventory()
        inventory["broad_reads"] = {"path": "README.md"}
        with self.assertRaisesRegex(runner_state.RunnerError, "broad_reads must be an array"):
            input_inventory.validate_input_inventory(inventory, active_phase="execute")

        inventory = self.minimal_inventory()
        inventory["broad_reads"] = ["README.md"]
        with self.assertRaisesRegex(runner_state.RunnerError, r"broad_reads\[0\]"):
            input_inventory.validate_input_inventory(inventory, active_phase="execute")

    def test_input_inventory_owner_rejects_non_integer_schema_version(self) -> None:
        for schema_version in ("1", True):
            inventory = self.minimal_inventory()
            inventory["schema_version"] = schema_version
            with self.subTest(schema_version=schema_version):
                with self.assertRaisesRegex(runner_state.RunnerError, "schema_version"):
                    input_inventory.validate_input_inventory(
                        inventory,
                        active_phase="execute",
                    )

    def test_input_inventory_owner_rejects_invalid_entry_fields_without_dumping_content(
        self,
    ) -> None:
        inventory = self.minimal_inventory()
        inventory["broad_reads"].append(
            {
                "path": "README.md",
                "command": ["rg", "needle"],
                "reason": "needle unique secret",
            }
        )

        with self.assertRaisesRegex(
            runner_state.RunnerError,
            r"broad_reads\[0\]\.command",
        ) as error:
            input_inventory.validate_input_inventory(inventory, active_phase="execute")

        self.assertNotIn("needle unique secret", str(error.exception))

    def test_input_inventory_owner_rejects_absolute_and_parent_escaping_paths(
        self,
    ) -> None:
        for bad_path, expected in (
            ("/tmp/outside.md", "project-relative"),
            ("~/outside.md", "project-relative"),
            ("~root/outside.md", "project-relative"),
            ("../outside.md", "must not escape"),
            ("plans/../outside.md", "must not escape"),
        ):
            inventory = self.minimal_inventory()
            inventory["primary_inputs"].append({"path": bad_path})
            with self.subTest(path=bad_path):
                with self.assertRaisesRegex(runner_state.RunnerError, expected):
                    input_inventory.validate_input_inventory(
                        inventory,
                        active_phase="execute",
                    )

    def test_input_inventory_resolver_rejects_tilde_paths(self) -> None:
        with self.assertRaisesRegex(runner_state.RunnerError, "project-relative"):
            input_inventory.resolve_project_relative_path(
                self.project,
                "~/outside.md",
            )

    def test_input_inventory_owner_rejects_non_integer_byte_count(self) -> None:
        for byte_count in ("1024", True):
            inventory = self.minimal_inventory()
            inventory["large_file_reads"].append(
                {
                    "path": "README.md",
                    "byte_count": byte_count,
                }
            )
            with self.subTest(byte_count=byte_count):
                with self.assertRaisesRegex(runner_state.RunnerError, "byte_count"):
                    input_inventory.validate_input_inventory(
                        inventory,
                        active_phase="execute",
                    )

    def test_input_inventory_file_loader_resolves_project_relative_paths(self) -> None:
        inventory_path = "project-notes/architecture/input-inventory.json"
        resolved = self.project / inventory_path
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(json.dumps(self.minimal_inventory()), encoding="utf-8")

        loaded = input_inventory.validate_input_inventory_file(
            self.project,
            inventory_path,
            active_phase="execute",
        )

        self.assertEqual(loaded["phase"], "execute")
        self.assertEqual(
            input_inventory.resolve_project_relative_path(
                self.project,
                inventory_path,
            ),
            resolved,
        )

    def test_input_inventory_expected_path_helper(self) -> None:
        expected = "project-notes/architecture/run/input-inventory.json"

        input_inventory.validate_expected_input_inventory_path(expected, expected)

        with self.assertRaisesRegex(runner_state.RunnerError, "expected path"):
            input_inventory.validate_expected_input_inventory_path(
                "project-notes/architecture/other.json",
                expected,
            )

    def test_input_inventory_owner_direct_script_import_fallback(self) -> None:
        code = (
            "import architecture_program_runner_input_inventory as inv; "
            "inv.validate_input_inventory({"
            "'schema_version': 1, "
            "'phase': 'execute', "
            "'primary_inputs': [], "
            "'broad_reads': [], "
            "'large_file_reads': [], "
            "'subagent_reports': []"
            "}, active_phase='execute')"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1] / "scripts",
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
