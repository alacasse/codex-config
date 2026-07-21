#!/usr/bin/env python3
"""Install versioned Codex config features from codex-features.json."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast


STATE_RELATIVE_PATH = Path("codex-config/installed-features.json")
MANIFEST_NAME = "codex-features.json"


class InstallError(RuntimeError):
    """Raised for user-correctable install failures."""


@dataclass(frozen=True)
class StaleLink:
    """One previously managed link absent from the current manifest."""

    feature: str
    source: Path | None
    target: Path
    remove_target: bool


class LinkRecord(TypedDict):
    """One source-to-target link in the manifest or installed state."""

    source: str
    target: str


class FeatureRecord(TypedDict, total=False):
    """Validated feature fields used by the installer."""

    version: str
    description: str
    default_enabled: bool
    owner: str
    requires: list[str]
    links: list[LinkRecord]


class Manifest(TypedDict):
    """Validated installer manifest."""

    schema_version: int
    features: dict[str, FeatureRecord]


class InstalledFeatureRecord(TypedDict, total=False):
    """Persisted state for one installed feature."""

    version: str
    description: str
    links: list[LinkRecord]


class InstallState(TypedDict, total=False):
    """Persisted installer state."""

    schema_version: int
    installed_at: str
    reconciled_at: str
    repo_root: str
    manifest: str
    features: dict[str, InstalledFeatureRecord]


class Arguments(argparse.Namespace):
    """Typed command-line arguments."""

    repo_root: str | None
    manifest: str
    codex_home: str
    feature: list[str]
    all_features: bool
    list: bool
    status: bool
    prune: bool
    dry_run: bool
    force: bool


def parse_args() -> Arguments:
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
        help="Show installed feature versions and stale managed links, then exit.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove stale links that still match their recorded managed sources.",
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
    return cast(Arguments, parser.parse_args())


def repo_root_from_args(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def resolve_manifest(repo_root: Path, manifest_arg: str) -> Path:
    manifest = Path(manifest_arg).expanduser()
    if not manifest.is_absolute():
        manifest = repo_root / manifest
    return manifest.resolve()


def load_manifest(path: Path) -> Manifest:
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InstallError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InstallError(f"manifest is not valid JSON: {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise InstallError("manifest root must be an object")
    data = cast(dict[str, object], raw)
    if data.get("schema_version") != 1:
        raise InstallError("unsupported manifest schema_version; expected 1")
    features = data.get("features")
    if not isinstance(features, dict) or not features:
        raise InstallError("manifest must contain a non-empty features object")
    return cast(Manifest, data)


def selected_feature_names(args: Arguments, manifest: Manifest) -> list[str]:
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
    return expand_feature_dependencies(names, available)


def expand_feature_dependencies(
    names: list[str], available: dict[str, FeatureRecord]
) -> list[str]:
    expanded: list[str] = []
    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            raise InstallError(f"circular feature dependency involving {name}")
        feature = available[name]
        raw_requires = feature.get("requires", [])
        if not isinstance(raw_requires, list) or not all(
            isinstance(item, str) for item in raw_requires
        ):
            raise InstallError(
                f"feature {name} requires must be a list of feature names"
            )
        missing = [required for required in raw_requires if required not in available]
        if missing:
            raise InstallError(
                f"feature {name} requires unknown feature(s): {', '.join(missing)}"
            )
        visiting.add(name)
        for required in raw_requires:
            visit(required)
        visiting.remove(name)
        visited.add(name)
        expanded.append(name)

    for name in names:
        visit(name)
    return expanded


def state_path(codex_home: Path) -> Path:
    return codex_home / STATE_RELATIVE_PATH


def load_state(codex_home: Path) -> InstallState:
    path = state_path(codex_home)
    if not path.exists():
        return {"features": {}}
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InstallError(f"installed state is not valid JSON: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise InstallError(f"installed state root must be an object: {path}")
    data = cast(dict[str, object], raw)
    if not isinstance(data.get("features"), dict):
        raise InstallError(f"installed state must contain a features object: {path}")
    return cast(InstallState, data)


def write_state(codex_home: Path, state: InstallState) -> None:
    path = state_path(codex_home)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def print_feature_list(manifest: Manifest) -> None:
    for name, feature in manifest["features"].items():
        version = feature.get("version", "unversioned")
        description = feature.get("description", "")
        install_mode = "default" if feature.get("default_enabled", True) is not False else "opt-in"
        owner = feature.get("owner")
        owner_suffix = f", owner: {owner}" if owner else ""
        print(f"{name} {version} [{install_mode}{owner_suffix}] - {description}")


def print_status(codex_home: Path, manifest: Manifest) -> None:
    state = load_state(codex_home)
    installed = state.get("features", {})
    if not installed:
        print(f"No installed feature state found at {state_path(codex_home)}")
        return

    for name, details in sorted(installed.items()):
        if not isinstance(details, dict):
            raise InstallError(f"installed state for feature {name} is invalid")
        installed_version = details.get("version", "unknown")
        manifest_feature = manifest["features"].get(name)
        manifest_version = (
            manifest_feature.get("version") if manifest_feature is not None else None
        )
        suffix = ""
        if manifest_version is None:
            suffix = " [stale feature]"
        elif manifest_version != installed_version:
            suffix = f" (manifest: {manifest_version})"
        print(f"{name} {installed_version}{suffix}")

    stale, unresolved = stale_managed_links(codex_home, manifest, state)
    for item in stale:
        source = str(item.source) if item.source is not None else "unknown source"
        kind = "stale-link" if item.remove_target else "stale-record"
        print(f"{kind} {item.feature} {item.target} -> {source}")
    for feature in unresolved:
        print(f"stale-state {feature}: previous link inventory is unavailable")


def validate_relative_path(value: str, field_name: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise InstallError(f"{field_name} must be relative: {value}")
    if any(part == ".." for part in path.parts):
        raise InstallError(f"{field_name} must not contain '..': {value}")
    return path


def validate_manifest(repo_root: Path, manifest: Manifest) -> None:
    features = manifest["features"]
    seen_targets: dict[Path, str] = {}

    for name, feature in features.items():
        if not isinstance(name, str) or not name:
            raise InstallError("feature names must be non-empty strings")
        if not isinstance(feature, dict):
            raise InstallError(f"feature {name} must be an object")
        version = feature.get("version")
        if not isinstance(version, str) or not version:
            raise InstallError(f"feature {name} must define a non-empty version")
        links = feature.get("links")
        if not isinstance(links, list) or not links:
            raise InstallError(f"feature {name} must define at least one link")

        for link in links:
            if not isinstance(link, dict):
                raise InstallError(f"feature {name} has an invalid link entry")
            source_value = link.get("source")
            target_value = link.get("target")
            if not isinstance(source_value, str) or not source_value:
                raise InstallError(f"feature {name} has an invalid source")
            if not isinstance(target_value, str) or not target_value:
                raise InstallError(f"feature {name} has an invalid target")
            source = validate_relative_path(source_value, "source")
            target = validate_relative_path(target_value, "target")
            if not (repo_root / source).exists():
                raise InstallError(f"source does not exist: {repo_root / source}")
            prior_owner = seen_targets.get(target)
            if prior_owner is not None:
                raise InstallError(
                    f"target {target} is declared by both {prior_owner} and {name}"
                )
            seen_targets[target] = name

    expand_feature_dependencies(list(features), features)


def current_manifest_targets(manifest: Manifest) -> set[Path]:
    return {
        Path(link["target"])
        for feature in manifest["features"].values()
        for link in feature.get("links", [])
    }


def manifest_targets_by_feature(manifest: Manifest) -> dict[str, set[Path]]:
    return {
        name: {Path(link["target"]) for link in feature.get("links", [])}
        for name, feature in manifest["features"].items()
    }


def stale_managed_links(
    codex_home: Path,
    manifest: Manifest,
    state: InstallState | None = None,
) -> tuple[list[StaleLink], list[str]]:
    installed_state = state if state is not None else load_state(codex_home)
    installed = installed_state.get("features", {})
    if not isinstance(installed, dict):
        raise InstallError("installed feature state is invalid")

    raw_repo_root = installed_state.get("repo_root")
    recorded_root = (
        Path(raw_repo_root).expanduser().resolve(strict=False)
        if isinstance(raw_repo_root, str) and raw_repo_root
        else None
    )
    expected_by_feature = manifest_targets_by_feature(manifest)
    expected_targets = current_manifest_targets(manifest)
    stale: list[StaleLink] = []
    unresolved: list[str] = []

    for feature_name, details in sorted(installed.items()):
        if not isinstance(details, dict):
            raise InstallError(
                f"installed state for feature {feature_name} is invalid"
            )
        recorded_links = details.get("links")
        feature_removed = feature_name not in manifest["features"]
        if not isinstance(recorded_links, list):
            if feature_removed:
                unresolved.append(feature_name)
            continue

        for link in recorded_links:
            if not isinstance(link, dict):
                raise InstallError(
                    f"installed link state for feature {feature_name} is invalid"
                )
            source_value = link.get("source")
            target_value = link.get("target")
            if not isinstance(target_value, str) or not target_value:
                raise InstallError(
                    f"installed link target for feature {feature_name} is invalid"
                )
            target_rel = validate_relative_path(target_value, "installed target")
            if target_rel in expected_by_feature.get(feature_name, set()):
                continue
            source = None
            if isinstance(source_value, str) and source_value and recorded_root:
                source_rel = validate_relative_path(source_value, "installed source")
                source = (recorded_root / source_rel).resolve(strict=False)
            stale.append(
                StaleLink(
                    feature=feature_name,
                    source=source,
                    target=codex_home / target_rel,
                    remove_target=target_rel not in expected_targets,
                )
            )

    return stale, unresolved


def resolved_symlink_target(target: Path) -> Path | None:
    link_target = symlink_target(target)
    if link_target is None:
        return None
    if not link_target.is_absolute():
        link_target = target.parent / link_target
    return link_target.resolve(strict=False)


def reconciled_features(
    installed: dict[str, InstalledFeatureRecord], manifest: Manifest
) -> dict[str, InstalledFeatureRecord]:
    expected_by_feature = manifest_targets_by_feature(manifest)
    reconciled: dict[str, InstalledFeatureRecord] = {}
    for feature_name, details in installed.items():
        if feature_name not in manifest["features"] or not isinstance(details, dict):
            continue
        links = details.get("links")
        if isinstance(links, list):
            expected_targets = expected_by_feature[feature_name]
            retained_links: list[LinkRecord] = [
                link
                for link in links
                if isinstance(link, dict)
                and isinstance(link.get("target"), str)
                and Path(link["target"]) in expected_targets
            ]
            details = cast(
                InstalledFeatureRecord,
                {**details, "links": retained_links},
            )
        reconciled[feature_name] = details
    return reconciled


def prune_stale_links(
    codex_home: Path, manifest: Manifest, *, dry_run: bool
) -> None:
    state = load_state(codex_home)
    stale, unresolved = stale_managed_links(codex_home, manifest, state)
    unsafe: list[str] = []

    for item in stale:
        if not item.remove_target:
            continue
        if item.source is None:
            unsafe.append(f"{item.target}: recorded source is unavailable")
        elif item.target.is_symlink():
            observed = resolved_symlink_target(item.target)
            if observed != item.source:
                unsafe.append(
                    f"{item.target}: symlink points to {observed}, expected {item.source}"
                )
        elif item.target.exists():
            unsafe.append(f"{item.target}: target is not a symlink")

    unsafe.extend(
        f"feature {feature}: previous link inventory is unavailable"
        for feature in unresolved
    )
    if unsafe:
        for reason in unsafe:
            print(f"preserve {reason}")
        raise InstallError("stale managed links require manual resolution")

    if not stale:
        print("No stale managed links found.")
        return

    for item in stale:
        if not item.remove_target:
            print(f"retain  {item.target}: target is claimed by the current manifest")
        elif item.target.is_symlink():
            print(f"prune   {item.target} -> {item.source}")
        else:
            print(f"missing {item.target}")

    if dry_run:
        print("dry-run: stale links and installed feature state were not changed")
        return

    for item in stale:
        if item.remove_target and item.target.is_symlink():
            item.target.unlink()

    installed = state.get("features", {})
    if not isinstance(installed, dict):
        raise InstallError("installed feature state is invalid")
    state["features"] = reconciled_features(installed, manifest)
    state["reconciled_at"] = (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    write_state(codex_home, state)
    print(f"state   {state_path(codex_home)}")


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
    manifest: Manifest,
    names: list[str],
    *,
    dry_run: bool,
    force: bool,
) -> None:
    previous_state = load_state(codex_home)
    previous_features = previous_state.get("features", {})
    stale, unresolved = stale_managed_links(codex_home, manifest, previous_state)
    if stale or unresolved:
        raise InstallError(
            "stale managed links are recorded; run --status and --prune before installing"
        )
    installed_features: dict[str, InstalledFeatureRecord] = {}

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

        installed_links: list[LinkRecord] = []
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

    state: InstallState = {
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
    write_state(codex_home, state)
    print(f"state   {state_path(codex_home)}")


def main() -> int:
    args = parse_args()
    try:
        repo_root = repo_root_from_args(args.repo_root)
        manifest_path = resolve_manifest(repo_root, args.manifest)
        codex_home = Path(args.codex_home).expanduser()
        manifest = load_manifest(manifest_path)
        validate_manifest(repo_root, manifest)

        action_count = int(args.list) + int(args.status) + int(args.prune)
        if action_count > 1:
            raise InstallError("choose only one of --list, --status, or --prune")
        if (args.list or args.status or args.prune) and (
            args.feature or args.all_features or args.force
        ):
            raise InstallError(
                "--list, --status, and --prune cannot select features or use --force"
            )

        if args.list:
            print_feature_list(manifest)
            return 0
        if args.status:
            print_status(codex_home, manifest)
            return 0
        if args.prune:
            prune_stale_links(codex_home, manifest, dry_run=args.dry_run)
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
