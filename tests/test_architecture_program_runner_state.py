from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts import architecture_program_runner_state as state_owner


SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "architecture_program_runner.py"
)


def load_runner_module() -> object:
    spec = importlib.util.spec_from_file_location("architecture_program_runner", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["architecture_program_runner"] = module
    spec.loader.exec_module(module)
    return module


class ArchitectureProgramRunnerStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name) / "project"
        self.project.mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def config(self, artifact_root: Path | None = None) -> SimpleNamespace:
        return SimpleNamespace(
            project=self.project,
            program_ledger="project-notes/architecture/program.md",
            max_batches=1,
            execute_batches=True,
            artifact_root=artifact_root,
        )

    def test_runner_reexports_owner_path_and_state_helpers(self) -> None:
        runner = load_runner_module()

        self.assertIs(runner.resolve_state_path, state_owner.resolve_state_path)
        self.assertIs(runner.initial_state, state_owner.initial_state)
        self.assertIs(runner.phase_receipt_path, state_owner.phase_receipt_path)
        self.assertIs(runner.RunnerError, state_owner.RunnerError)

    def test_slug_and_run_id_helpers_preserve_path_component_contract(self) -> None:
        self.assertEqual(state_owner.slugify_path_component(" Batch #1: API/IO "), "Batch-1-API-IO")
        self.assertEqual(state_owner.slugify_path_component("..."), "unnamed")
        self.assertEqual(state_owner.ledger_slug("notes/architecture/findings.md"), "findings")
        self.assertRegex(
            state_owner.new_run_id("Batch #1: API/IO"),
            r"^run-\d{8}-\d{6}-Batch-1-API-IO$",
        )

    def test_state_resolution_prefers_latest_structured_run_then_legacy(self) -> None:
        older = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-100000"
            / "run-state.json"
        )
        newer = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-110000"
            / "run-state.json"
        )
        older.parent.mkdir(parents=True)
        older.write_text("{}\n", encoding="utf-8")
        newer.parent.mkdir(parents=True)
        newer.write_text("{}\n", encoding="utf-8")

        state_path, artifact_root = state_owner.resolve_state_path(
            self.project, "project-notes/architecture/program.md", None, resume=True
        )

        self.assertEqual(state_path, newer)
        self.assertEqual(artifact_root, newer.parent)

    def test_state_resolution_keeps_legacy_flat_resume_compatible(self) -> None:
        legacy = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-run-state.json"
        )
        legacy.parent.mkdir(parents=True)
        legacy.write_text("{}\n", encoding="utf-8")

        state_path, artifact_root = state_owner.resolve_state_path(
            self.project, "project-notes/architecture/program.md", None, resume=True
        )

        self.assertEqual(state_path, legacy)
        self.assertIsNone(artifact_root)

    def test_structured_state_artifact_paths_keep_existing_strings(self) -> None:
        artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        runner_state = state_owner.initial_state(self.config(artifact_root))

        self.assertEqual(
            runner_state["artifact_root"],
            "project-notes/architecture/architecture-program-runs/program/run-20260626-204812",
        )
        self.assertEqual(
            state_owner.phase_receipt_path(runner_state, "select-dispatch"),
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/receipts/01-select-dispatch.json",
        )
        runner_state["active_batch_id"] = "Batch #1: API/IO"
        self.assertEqual(
            state_owner.batch_artifact_root(runner_state, "Batch #1: API/IO"),
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/batches/Batch-1-API-IO",
        )
        self.assertEqual(
            state_owner.phase_input_inventory_path(runner_state, "execute"),
            "project-notes/architecture/architecture-program-runs/program/"
            "run-20260626-204812/telemetry/phases/01-execute.input-inventory.json",
        )

    def test_state_write_load_round_trips_validated_json(self) -> None:
        state_path = self.project / "state" / "run-state.json"
        runner_state = state_owner.initial_state(self.config())

        state_owner.write_state(state_path, runner_state)
        loaded = state_owner.load_state(state_path)

        self.assertEqual(loaded["runner_version"], state_owner.RUNNER_VERSION)
        self.assertEqual(loaded["active_phase"], "select-dispatch")
        self.assertIsInstance(loaded["updated_at"], str)


if __name__ == "__main__":
    unittest.main()
