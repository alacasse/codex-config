from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "install.sh"
MANIFEST = json.loads((REPO_ROOT / "codex-features.json").read_text(encoding="utf-8"))
STATE_RELATIVE = Path("codex-config/installed-features.json")


def run_installer(codex_home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(INSTALLER), "--codex-home", str(codex_home), *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def write_state(
    codex_home: Path,
    features: dict[str, object],
    *,
    repo_root: Path = REPO_ROOT,
) -> Path:
    path = codex_home / STATE_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "repo_root": str(repo_root),
                "manifest": str(REPO_ROOT / "codex-features.json"),
                "features": features,
            }
        ),
        encoding="utf-8",
    )
    return path


def stale_feature(target: str = "skills/retired-tool") -> dict[str, object]:
    return {
        "retired-feature": {
            "version": "1.0.0",
            "links": [{"source": "skills/retired-tool", "target": target}],
        }
    }


def test_fresh_default_install_uses_only_default_manifest_features() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"

        completed = run_installer(codex_home)

        assert completed.returncode == 0, completed.stderr
        state = json.loads((codex_home / STATE_RELATIVE).read_text(encoding="utf-8"))
        expected = {
            name
            for name, feature in MANIFEST["features"].items()
            if feature.get("default_enabled", True) is not False
        }
        assert set(state["features"]) == expected
        assert not (codex_home / "hooks.json").exists()

        for name in expected:
            for link in MANIFEST["features"][name]["links"]:
                target = codex_home / link["target"]
                source = REPO_ROOT / link["source"]
                assert target.is_symlink()
                assert target.resolve() == source.resolve()


def test_installed_owner_command_recognizes_the_global_instructions() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        installed = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
        )
        command = codex_home / "bin" / "codex-owner"

        inspected = subprocess.run(
            [
                str(command),
                "--codex-home",
                str(codex_home),
                str(codex_home / "AGENTS.md"),
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        assert installed.returncode == 0, installed.stderr
        assert inspected.returncode == 0, inspected.stderr
        assert "owner: codex-config" in inspected.stdout
        assert "feature: global-instructions 3.1.0" in inspected.stdout


def test_dry_run_does_not_create_the_codex_home() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "not-created"

        completed = run_installer(codex_home, "--dry-run")

        assert completed.returncode == 0, completed.stderr
        assert "dry-run: installed feature state was not written" in completed.stdout
        assert not codex_home.exists()


def test_all_installs_the_opt_in_notification_feature() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"

        completed = run_installer(codex_home, "--all")

        assert completed.returncode == 0, completed.stderr
        assert (codex_home / "hooks.json").is_symlink()
        state = json.loads((codex_home / STATE_RELATIVE).read_text(encoding="utf-8"))
        assert set(state["features"]) == set(MANIFEST["features"])
        for feature in MANIFEST["features"].values():
            for link in feature["links"]:
                target = codex_home / link["target"]
                source = REPO_ROOT / link["source"]
                assert target.is_symlink()
                assert target.resolve() == source.resolve()


def test_status_identifies_removed_features_and_links() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        write_state(codex_home, stale_feature())

        completed = run_installer(codex_home, "--status")

        assert completed.returncode == 0, completed.stderr
        assert "retired-feature 1.0.0 [stale feature]" in completed.stdout
        assert "stale-link retired-feature" in completed.stdout
        assert str(codex_home / "skills" / "retired-tool") in completed.stdout


def test_prune_removes_only_an_exact_recorded_symlink() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(codex_home, stale_feature())
        target = codex_home / "skills" / "retired-tool"
        target.parent.mkdir(parents=True)
        target.symlink_to(REPO_ROOT / "skills" / "retired-tool")

        completed = run_installer(codex_home, "--prune")

        assert completed.returncode == 0, completed.stderr
        assert not target.is_symlink()
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["features"] == {}
        assert "reconciled_at" in state


def test_prune_dry_run_preserves_link_and_state() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(codex_home, stale_feature())
        original_state = state_path.read_text(encoding="utf-8")
        target = codex_home / "skills" / "retired-tool"
        target.parent.mkdir(parents=True)
        target.symlink_to(REPO_ROOT / "skills" / "retired-tool")

        completed = run_installer(codex_home, "--prune", "--dry-run")

        assert completed.returncode == 0, completed.stderr
        assert target.is_symlink()
        assert state_path.read_text(encoding="utf-8") == original_state


def test_prune_refuses_retargeted_symlink_before_any_change() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        codex_home = root / "codex-home"
        state_path = write_state(codex_home, stale_feature())
        original_state = state_path.read_text(encoding="utf-8")
        foreign = root / "foreign"
        foreign.mkdir()
        target = codex_home / "skills" / "retired-tool"
        target.parent.mkdir(parents=True)
        target.symlink_to(foreign)

        completed = run_installer(codex_home, "--prune")

        assert completed.returncode == 1
        assert "stale managed links require manual resolution" in completed.stderr
        assert target.is_symlink()
        assert target.resolve() == foreign.resolve()
        assert state_path.read_text(encoding="utf-8") == original_state


def test_prune_reconciles_a_removed_link_inside_a_surviving_feature() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        current_links = MANIFEST["features"]["custom-agents"]["links"]
        old_links = [
            *current_links,
            {"source": "agents/retired_agent.toml", "target": "agents/retired_agent.toml"},
        ]
        state_path = write_state(
            codex_home,
            {
                "custom-agents": {
                    "version": "1.0.0",
                    "links": old_links,
                }
            },
        )
        stale_target = codex_home / "agents" / "retired_agent.toml"
        stale_target.parent.mkdir(parents=True)
        stale_target.symlink_to(REPO_ROOT / "agents" / "retired_agent.toml")

        completed = run_installer(codex_home, "--prune")

        assert completed.returncode == 0, completed.stderr
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["features"]["custom-agents"]["links"] == current_links
        assert not stale_target.is_symlink()


def test_install_blocks_before_stale_state_can_be_overwritten() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(codex_home, stale_feature())
        original_state = state_path.read_text(encoding="utf-8")

        completed = run_installer(codex_home)

        assert completed.returncode == 1
        assert "run --status and --prune" in completed.stderr
        assert state_path.read_text(encoding="utf-8") == original_state


def test_existing_invalid_state_fails_closed_without_installing() -> None:
    invalid_states = (
        "not json\n",
        "[]\n",
        "{}\n",
        '{"features": []}\n',
    )
    for raw_state in invalid_states:
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory) / "codex-home"
            state_path = codex_home / STATE_RELATIVE
            state_path.parent.mkdir(parents=True)
            state_path.write_text(raw_state, encoding="utf-8")

            completed = run_installer(codex_home)

            assert completed.returncode == 1
            assert "installed state" in completed.stderr
            assert state_path.read_text(encoding="utf-8") == raw_state
            assert not (codex_home / "AGENTS.md").exists()


def test_install_retargets_an_exact_previously_managed_source() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(
            codex_home,
            {
                "global-instructions": {
                    "version": "2.0.1",
                    "links": [{"source": "AGENTS.md", "target": "AGENTS.md"}],
                }
            },
        )
        target = codex_home / "AGENTS.md"
        target.symlink_to(REPO_ROOT / "AGENTS.md")

        completed = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
        )

        assert completed.returncode == 0, completed.stderr
        assert "global-instructions 2.0.1 -> 3.1.0" in completed.stdout
        assert "retarget" in completed.stdout
        assert target.resolve() == (REPO_ROOT / "global" / "AGENTS.md").resolve()
        assert (codex_home / "bin" / "codex-owner").is_symlink()
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["features"]["global-instructions"]["links"] == [
            {"source": "global/AGENTS.md", "target": "AGENTS.md"},
            {"source": "scripts/codex_owner.py", "target": "bin/codex-owner"},
        ]


def test_retarget_dry_run_preserves_the_previous_link_and_state() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(
            codex_home,
            {
                "global-instructions": {
                    "version": "2.0.1",
                    "links": [{"source": "AGENTS.md", "target": "AGENTS.md"}],
                }
            },
        )
        original_state = state_path.read_text(encoding="utf-8")
        target = codex_home / "AGENTS.md"
        target.symlink_to(REPO_ROOT / "AGENTS.md")

        completed = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
            "--dry-run",
        )

        assert completed.returncode == 0, completed.stderr
        assert "retarget" in completed.stdout
        assert target.resolve() == (REPO_ROOT / "AGENTS.md").resolve()
        assert not (codex_home / "bin" / "codex-owner").exists()
        assert state_path.read_text(encoding="utf-8") == original_state


def test_install_refuses_to_retarget_a_foreign_symlink() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        codex_home = root / "codex-home"
        state_path = write_state(
            codex_home,
            {
                "global-instructions": {
                    "version": "2.0.1",
                    "links": [{"source": "AGENTS.md", "target": "AGENTS.md"}],
                }
            },
        )
        original_state = state_path.read_text(encoding="utf-8")
        foreign = root / "foreign"
        foreign.mkdir()
        target = codex_home / "AGENTS.md"
        target.symlink_to(foreign)

        completed = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
        )

        assert completed.returncode == 1
        assert "not managed by this manifest" in completed.stderr
        assert target.resolve() == foreign.resolve()
        assert state_path.read_text(encoding="utf-8") == original_state
        assert not (codex_home / "bin" / "codex-owner").exists()


def test_install_preflights_every_target_before_retargeting() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        codex_home = root / "codex-home"
        state_path = write_state(
            codex_home,
            {
                "global-instructions": {
                    "version": "2.0.1",
                    "links": [{"source": "AGENTS.md", "target": "AGENTS.md"}],
                }
            },
        )
        original_state = state_path.read_text(encoding="utf-8")
        instructions_target = codex_home / "AGENTS.md"
        instructions_target.symlink_to(REPO_ROOT / "AGENTS.md")
        foreign = root / "foreign-owner"
        foreign.write_text("foreign\n", encoding="utf-8")
        owner_target = codex_home / "bin" / "codex-owner"
        owner_target.parent.mkdir(parents=True)
        owner_target.symlink_to(foreign)

        completed = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
        )

        assert completed.returncode == 1
        assert "not managed by this manifest" in completed.stderr
        assert instructions_target.resolve() == (REPO_ROOT / "AGENTS.md").resolve()
        assert owner_target.resolve() == foreign.resolve()
        assert state_path.read_text(encoding="utf-8") == original_state
        assert not list(codex_home.rglob("*.backup-*"))


def test_install_refuses_a_malformed_previous_source_record() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(
            codex_home,
            {
                "global-instructions": {
                    "version": "2.0.1",
                    "links": [{"target": "AGENTS.md"}],
                }
            },
        )
        original_state = state_path.read_text(encoding="utf-8")
        target = codex_home / "AGENTS.md"
        target.symlink_to(REPO_ROOT / "AGENTS.md")

        completed = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
        )

        assert completed.returncode == 1
        assert "installed link source" in completed.stderr
        assert target.resolve() == (REPO_ROOT / "AGENTS.md").resolve()
        assert state_path.read_text(encoding="utf-8") == original_state
        assert not (codex_home / "bin" / "codex-owner").exists()


def test_install_converges_metadata_for_a_version_only_upgrade() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        codex_home = root / "codex-home"
        manifest = json.loads(json.dumps(MANIFEST))
        feature = manifest["features"]["global-instructions"]
        feature["version"] = "99.0.0"
        feature["description"] = "Updated global instructions metadata."
        manifest_path = root / "version-only-manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        state_path = write_state(
            codex_home,
            {
                "global-instructions": {
                    "version": "98.0.0",
                    "description": "Stale metadata.",
                    "links": feature["links"],
                }
            },
        )
        for link in feature["links"]:
            target = codex_home / link["target"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(REPO_ROOT / link["source"])

        completed = run_installer(
            codex_home,
            "--manifest",
            str(manifest_path),
            "--feature",
            "global-instructions",
        )

        assert completed.returncode == 0, completed.stderr
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["features"]["global-instructions"] == {
            "version": feature["version"],
            "description": feature["description"],
            "links": feature["links"],
        }


def test_prune_reconciles_a_target_adopted_by_another_feature() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        state_path = write_state(
            codex_home,
            {
                "retired-feature": {
                    "version": "1.0.0",
                    "links": [
                        {
                            "source": "skills/retired-tool",
                            "target": "AGENTS.md",
                        }
                    ],
                }
            },
        )
        target = codex_home / "AGENTS.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(REPO_ROOT / "global" / "AGENTS.md")

        pruned = run_installer(codex_home, "--prune")

        assert pruned.returncode == 0, pruned.stderr
        assert "target is claimed by the current manifest" in pruned.stdout
        assert target.is_symlink()
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["features"] == {}

        installed = run_installer(codex_home, "--feature", "global-instructions")
        assert installed.returncode == 0, installed.stderr
        assert target.resolve() == (REPO_ROOT / "global" / "AGENTS.md").resolve()


def test_force_backs_up_a_real_file_conflict() -> None:
    with tempfile.TemporaryDirectory() as directory:
        codex_home = Path(directory) / "codex-home"
        target = codex_home / "AGENTS.md"
        target.parent.mkdir(parents=True)
        target.write_text("local instructions\n", encoding="utf-8")

        blocked = run_installer(codex_home, "--feature", "global-instructions")
        forced = run_installer(
            codex_home,
            "--feature",
            "global-instructions",
            "--force",
        )

        assert blocked.returncode == 1
        assert forced.returncode == 0, forced.stderr
        assert target.is_symlink()
        backups = list(codex_home.glob("AGENTS.md.backup-*"))
        assert len(backups) == 1
        assert backups[0].read_text(encoding="utf-8") == "local instructions\n"
