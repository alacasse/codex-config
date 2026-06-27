from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "architecture_program_runner.py"
)
REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("architecture_program_runner", SCRIPT)
assert spec is not None
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["architecture_program_runner"] = runner
spec.loader.exec_module(runner)


class ArchitectureProgramRunnerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / "project-notes" / "architecture").mkdir(parents=True)
        (self.project / "project-notes" / "architecture" / "program.md").write_text(
            "# Program\n", encoding="utf-8"
        )
        self.config = runner.RunnerConfig(
            project=self.project.resolve(),
            program_ledger="project-notes/architecture/program.md",
            max_batches=1,
            execute_batches=True,
            state_path=self.project / "project-notes" / "architecture" / "run-state.json",
            sandbox="workspace-write",
            execute_sandbox=None,
            model=None,
            env_overrides=(),
            dry_run=False,
            resume=False,
            stop_after_phase=None,
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

    def structured_config(self) -> Any:
        artifact_root = (
            self.project
            / "project-notes"
            / "architecture"
            / "architecture-program-runs"
            / "program"
            / "run-20260626-204812"
        )
        return runner.RunnerConfig(
            **{
                **self.config.__dict__,
                "state_path": artifact_root / "run-state.json",
                "artifact_root": artifact_root,
            }
        )

    def write_receipt(self, result: dict[str, Any]) -> None:
        path = runner.resolve_project_path(self.config.project, result["receipt_path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result), encoding="utf-8")

    def touch_project_path(self, value: str, content: str = "artifact\n") -> None:
        path = runner.resolve_project_path(self.config.project, value)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
