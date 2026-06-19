#!/usr/bin/env python3
"""Install versioned Codex config features from codex-features.json."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


STATE_RELATIVE_PATH = Path("codex-config/installed-features.json")
MANIFEST_NAME = "codex-features.json"


class InstallError(RuntimeError):
    """Raised for user-correctable install failures."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install versioned Codex features from this repository."
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root. Defaults to the parent of this script directory.",
    )
    parser.add_argument(
        "--manifest",
        default=MANIFEST_NAME,
        help=f"Feature manifest path, relative to repo root by default. Default: {MANIFEST_NAME}",
    )
    parser.add_argument(
        "--codex-home",
        default=os.environ.get("CODEX_HOME", "~/.codex"),
        help="Codex home directory. Default: CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--feature",
        action="append",
        default=[],
        help="Feature to install. May be repeated or comma-separated. Defaults to default-enabled features.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_features",
        help="Install all manifest features.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List manifest features and exit.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show installed feature versions and exit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without changing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace conflicting targets after backing up non-symlink files.",
    )
    return parser.parse_args()


def repo_root_from_args(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def resolve_manifest(repo_root: Path, manifest_arg: str) -> Path:
    manifest = Path(manifest_arg).expanduser()
    if not manifest.is_absolute():
        manifest = repo_root / manifest
    return manifest.resolve()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InstallError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InstallError(f"manifest is not valid JSON: {path}: {exc}") from exc

    if data.get("schema_version") != 1:
        raise InstallError("unsupported manifest schema_version; expected 1")
    features = data.get("features")
    if not isinstance(features, dict) or not features:
        raise InstallError("manifest must contain a non-empty features object")
    return data


def selected_feature_names(args: argparse.Namespace, manifest: dict[str, Any]) -> list[str]:
    available = manifest["features"]
    requested: list[str] = []
    for raw in args.feature:
        requested.extend(part.strip() for part in raw.split(",") if part.strip())

    if requested:
        names = requested
    elif args.all_features:
        names = list(available.keys())
    else:
        names = [
            name
            for name, feature in available.items()
            if feature.get("default_enabled", True) is not False
        ]

    missing = [name for name in names if name not in available]
    if missing:
        known = ", ".join(sorted(available))
        raise InstallError(f"unknown feature(s): {', '.join(missing)}. Known: {known}")
    return names


def state_path(codex_home: Path) -> Path:
    return codex_home / STATE_RELATIVE_PATH


def load_state(codex_home: Path) -> dict[str, Any]:
    path = state_path(codex_home)
    if not path.exists():
        return {"features": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"features": {}}
    if not isinstance(data, dict):
        return {"features": {}}
    if not isinstance(data.get("features"), dict):
        data["features"] = {}
    return data


def print_feature_list(manifest: dict[str, Any]) -> None:
    for name, feature in manifest["features"].items():
        version = feature.get("version", "unversioned")
        description = feature.get("description", "")
        install_mode = "default" if feature.get("default_enabled", True) is not False else "opt-in"
        owner = feature.get("owner")
        owner_suffix = f", owner: {owner}" if owner else ""
        print(f"{name} {version} [{install_mode}{owner_suffix}] - {description}")


def print_status(codex_home: Path, manifest: dict[str, Any]) -> None:
    state = load_state(codex_home)
    installed = state.get("features", {})
    if not installed:
        print(f"No installed feature state found at {state_path(codex_home)}")
        return

    for name, details in sorted(installed.items()):
        installed_version = details.get("version", "unknown")
        manifest_version = manifest["features"].get(name, {}).get("version")
        suffix = ""
        if manifest_version and manifest_version != installed_version:
            suffix = f" (manifest: {manifest_version})"
        print(f"{name} {installed_version}{suffix}")


def validate_relative_path(value: str, field_name: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise InstallError(f"{field_name} must be relative: {value}")
    if any(part == ".." for part in path.parts):
        raise InstallError(f"{field_name} must not contain '..': {value}")
    return path


def symlink_target(path: Path) -> Path | None:
    if not path.is_symlink():
        return None
    return Path(os.readlink(path))


def target_matches(target: Path, source: Path) -> bool:
    if not target.is_symlink():
        return False
    link_target = symlink_target(target)
    if link_target is None:
        return False
    if not link_target.is_absolute():
        link_target = target.parent / link_target
    return link_target.resolve() == source.resolve()


def backup_target(target: Path, dry_run: bool) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target.with_name(f"{target.name}.backup-{stamp}")
    counter = 1
    while backup.exists() or backup.is_symlink():
        backup = target.with_name(f"{target.name}.backup-{stamp}-{counter}")
        counter += 1
    if not dry_run:
        shutil.move(str(target), str(backup))
    return backup


def link_one(source: Path, target: Path, *, dry_run: bool, force: bool) -> str:
    if not source.exists():
        raise InstallError(f"source does not exist: {source}")

    if target_matches(target, source):
        return f"ok      {target} -> {source}"

    target_exists = target.exists() or target.is_symlink()
    if target_exists:
        if not force:
            raise InstallError(
                f"target already exists and is not managed by this manifest: {target}\n"
                "Use --force to replace symlink conflicts or back up real files."
            )
        if target.is_symlink():
            if not dry_run:
                target.unlink()
            action = "replace"
        else:
            backup = backup_target(target, dry_run)
            action = f"backup  {target} -> {backup}\nlink"
    else:
        action = "link"

    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)
    return f"{action:<7} {target} -> {source}"


def install_features(
    repo_root: Path,
    codex_home: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    names: list[str],
    *,
    dry_run: bool,
    force: bool,
) -> None:
    previous_state = load_state(codex_home)
    previous_features = previous_state.get("features", {})
    installed_features: dict[str, Any] = {}

    for name in names:
        feature = manifest["features"][name]
        version = str(feature.get("version", "unversioned"))
        previous_version = previous_features.get(name, {}).get("version")
        if previous_version == version:
            print(f"feature {name} {version}")
        elif previous_version:
            print(f"feature {name} {previous_version} -> {version}")
        else:
            print(f"feature {name} {version}")

        links = feature.get("links")
        if not isinstance(links, list) or not links:
            raise InstallError(f"feature {name} must define at least one link")

        installed_links: list[dict[str, str]] = []
        for link in links:
            if not isinstance(link, dict):
                raise InstallError(f"feature {name} has an invalid link entry")
            source_rel = validate_relative_path(str(link.get("source", "")), "source")
            target_rel = validate_relative_path(str(link.get("target", "")), "target")
            source = (repo_root / source_rel).resolve()
            target = codex_home / target_rel
            print(link_one(source, target, dry_run=dry_run, force=force))
            installed_links.append({"source": str(source_rel), "target": str(target_rel)})

        installed_features[name] = {
            "version": version,
            "description": feature.get("description", ""),
            "links": installed_links,
        }

    if dry_run:
        print("dry-run: installed feature state was not written")
        return

    state = {
        "schema_version": 1,
        "installed_at": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "repo_root": str(repo_root),
        "manifest": str(manifest_path),
        "features": {
            **previous_features,
            **installed_features,
        },
    }
    path = state_path(codex_home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"state   {path}")


def main() -> int:
    args = parse_args()
    try:
        repo_root = repo_root_from_args(args.repo_root)
        manifest_path = resolve_manifest(repo_root, args.manifest)
        codex_home = Path(args.codex_home).expanduser()
        manifest = load_manifest(manifest_path)

        if args.list:
            print_feature_list(manifest)
            return 0
        if args.status:
            print_status(codex_home, manifest)
            return 0

        names = selected_feature_names(args, manifest)
        install_features(
            repo_root,
            codex_home,
            manifest_path,
            manifest,
            names,
            dry_run=args.dry_run,
            force=args.force,
        )
    except InstallError as exc:
        print(f"install error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
