from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = REPO_ROOT / "hooks" / "agent_done_notify.py"


def load_hook_module():
    spec = importlib.util.spec_from_file_location("agent_done_notify", HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load agent_done_notify.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentDoneNotifyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_hook_module()

    def fake_run_git(self, cwd: Path, args: list[str]) -> str | None:
        del cwd
        if args == ["rev-parse", "--show-toplevel"]:
            return "/work/graphify"
        if args == ["branch", "--show-current"]:
            return "feature/hooks"
        if args == ["rev-parse", "--short", "HEAD"]:
            return "abc1234"
        if args == ["status", "--porcelain=v1"]:
            return " M a.py\n?? b.py"
        return None

    def test_stop_notification_contains_project_context(self) -> None:
        payload = {
            "hook_event_name": "Stop",
            "cwd": "/work/graphify/tools/install_sandbox",
            "model": "gpt-5",
            "permission_mode": "default",
            "session_id": "0123456789abcdef",
            "turn_id": "turn-abcdef123456789",
            "last_assistant_message": "Finished validation and updated the ledger.",
        }

        with (
            mock.patch.object(self.module, "run_git", side_effect=self.fake_run_git),
            mock.patch.object(self.module.socket, "gethostname", return_value="devbox"),
        ):
            notification = self.module.build_notification(payload)

        self.assertEqual(notification.title, "Codex done graphify (feature/hooks)")
        self.assertIn("event: Stop", notification.message)
        self.assertIn("project: graphify", notification.message)
        self.assertIn("ref: feature/hooks abc1234", notification.message)
        self.assertIn("dirty: 2 file(s)", notification.message)
        self.assertIn("cwd: tools/install_sandbox", notification.message)
        self.assertIn("host: devbox", notification.message)
        self.assertIn("last: Finished validation", notification.message)

    def test_subagent_notification_contains_agent_context(self) -> None:
        payload = {
            "hook_event_name": "SubagentStop",
            "cwd": "/work/graphify",
            "agent_type": "runway_reviewer",
            "agent_id": "agent-1234567890abcdef",
            "last_assistant_message": "No blocking findings.",
        }

        with mock.patch.object(self.module, "run_git", side_effect=self.fake_run_git):
            notification = self.module.build_notification(payload)

        self.assertEqual(notification.title, "Codex subagent done graphify (feature/hooks)")
        self.assertIn("agent: runway_reviewer", notification.message)
        self.assertIn("agent_id: agent-123456", notification.message)
        self.assertEqual(notification.tags, "robot")

    def test_hook_exits_quietly_without_configured_backend(self) -> None:
        payload = {
            "hook_event_name": "Stop",
            "cwd": str(REPO_ROOT),
            "last_assistant_message": "Done.",
        }

        completed = subprocess.run(
            [sys.executable, str(HOOK_PATH)],
            input=json.dumps(payload),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "")

    def test_manifest_feature_is_opt_in(self) -> None:
        manifest = json.loads((REPO_ROOT / "codex-features.json").read_text(encoding="utf-8"))
        feature = manifest["features"]["agent-notifications"]

        self.assertIs(feature["default_enabled"], False)
        self.assertEqual(feature["version"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
