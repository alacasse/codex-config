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
        if contains_path(source, resolved) or contains_path(target, original_absolute):
            return {
                "path": str(original),
                "resolved_path": str(resolved),
                "owned": True,
                "owner": "codex-config",
                "repo_root": str(repo_root),
                "feature": link["feature"],
                "version": link["version"],
                "source": str(source),
                "target": str(target),
                "changelog_required": True,
                "git_status_required": True,
            }

    return {
        "path": str(original),
        "resolved_path": str(resolved),
        "owned": False,
        "owner": None,
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
        if result["owned"]:
            print("owner: codex-config")
            print(f"repo_root: {result['repo_root']}")
            print(f"feature: {result['feature']} {result['version']}")
            print(f"source: {result['source']}")
            print(f"target: {result['target']}")
            print("changelog_required: true")
            print("git_status_required: true")
        else:
            print("owner: external-or-unmanaged")
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
