#!/usr/bin/env python3
"""Resolve whether a path is owned by this codex-config repository."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


MANIFEST_NAME = "codex-features.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report whether paths resolve into this codex-config repo."
    )
    parser.add_argument("paths", nargs="+", help="Paths to inspect.")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root. Defaults to the parent of this script directory.",
    )
    parser.add_argument(
        "--codex-home",
        default=os.environ.get("CODEX_HOME", "~/.codex"),
        help="Codex home directory. Default: CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON.",
    )
    return parser.parse_args()


def repo_root_from_args(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def load_manifest(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root / MANIFEST_NAME).read_text(encoding="utf-8"))


def resolve_loose(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def absolute_loose(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path.expanduser())))


def contains_path(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def installed_status(target: Path, source: Path) -> tuple[str, str]:
    if target.is_symlink():
        link_target = Path(os.readlink(target))
        if not link_target.is_absolute():
            link_target = target.parent / link_target
        try:
            resolved_link = link_target.resolve(strict=True)
            resolved_source = source.resolve(strict=True)
        except FileNotFoundError:
            return (
                "wrong_symlink",
                "Target is a symlink, but it does not resolve to the declared source.",
            )
        if resolved_link == resolved_source:
            return "linked", "Target is linked to the declared source."
        return (
            "wrong_symlink",
            "Target is a symlink, but it resolves somewhere other than the declared source.",
        )

    if not target.exists():
        return "missing", "Target does not exist."

    if target.is_file() and source.is_dir():
        return (
            "conflict_file",
            "Target exists as a file, but the declared source is a directory.",
        )
    if target.is_dir() and source.is_file():
        return (
            "conflict_directory",
            "Target exists as a directory, but the declared source is a file.",
        )
    if target.is_file() or target.is_dir():
        return (
            "unlinked_copy",
            "Target exists and matches a managed feature path, but is not linked to the declared source.",
        )
    return (
        "unlinked_copy",
        "Target exists and matches a managed feature path, but is not linked to the declared source.",
    )


def build_owned_links(
    repo_root: Path, codex_home: Path, manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    links: list[dict[str, Any]] = []
    for feature_name, feature in manifest.get("features", {}).items():
        for link in feature.get("links", []):
            source = resolve_loose(repo_root / link["source"])
            target = absolute_loose(codex_home / link["target"])
            links.append(
                {
                    "feature": feature_name,
                    "version": feature.get("version", "unversioned"),
                    "source": source,
                    "target": target,
                }
            )
    return links


def inspect_path(path: Path, links: list[dict[str, Any]], repo_root: Path) -> dict[str, Any]:
    original = path.expanduser()
    original_absolute = absolute_loose(original)
    resolved = resolve_loose(original_absolute)

    for link in links:
        source = link["source"]
        target = link["target"]
        path_in_source = contains_path(source, original_absolute) or contains_path(
            source, resolved
        )
        path_in_target = contains_path(target, original_absolute)
        if path_in_source or path_in_target:
            status, reason = installed_status(target, source)
            installed_owner = "codex-config" if status == "linked" else None
            owner = "codex-config" if path_in_source or installed_owner else None
            owned = owner == "codex-config"
            return {
                "path": str(original),
                "resolved_path": str(resolved),
                "owned": owned,
                "owner": owner,
                "manifest_owner": "codex-config",
                "installed_owner": installed_owner,
                "status": status,
                "reason": reason,
                "repo_root": str(repo_root),
                "feature": link["feature"],
                "version": link["version"],
                "source": str(source),
                "target": str(target),
                "changelog_required": owned,
                "git_status_required": owned,
            }

    return {
        "path": str(original),
        "resolved_path": str(resolved),
        "owned": False,
        "owner": None,
        "manifest_owner": None,
        "installed_owner": None,
        "status": "unmanaged",
        "reason": "Path does not match a codex-config manifest link.",
        "repo_root": None,
        "feature": None,
        "version": None,
        "source": None,
        "target": None,
        "changelog_required": False,
        "git_status_required": False,
    }


def print_text(results: list[dict[str, Any]]) -> None:
    for result in results:
        print(f"path: {result['path']}")
        print(f"resolved_path: {result['resolved_path']}")
        if result["manifest_owner"]:
            print(f"manifest_owner: {result['manifest_owner']}")
            print(f"installed_owner: {result['installed_owner'] or 'none'}")
            print(f"status: {result['status']}")
            print(f"reason: {result['reason']}")
            print(f"owner: {result['owner'] or 'external-or-unmanaged'}")
            print(f"repo_root: {result['repo_root']}")
            print(f"feature: {result['feature']} {result['version']}")
            print(f"source: {result['source']}")
            print(f"target: {result['target']}")
            print(f"changelog_required: {str(result['changelog_required']).lower()}")
            print(f"git_status_required: {str(result['git_status_required']).lower()}")
        else:
            print("owner: external-or-unmanaged")
            print(f"status: {result['status']}")
            print(f"reason: {result['reason']}")
        print()


def main() -> int:
    args = parse_args()
    repo_root = repo_root_from_args(args.repo_root)
    codex_home = Path(args.codex_home).expanduser()
    manifest = load_manifest(repo_root)
    links = build_owned_links(repo_root, codex_home, manifest)
    results = [inspect_path(Path(path), links, repo_root) for path in args.paths]

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        print_text(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
