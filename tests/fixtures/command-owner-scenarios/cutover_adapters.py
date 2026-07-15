"""Disposable generation, installer, cutover, and history observations."""

from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if not sys.path or sys.path[0] != str(REPO_ROOT):
    sys.path.insert(0, str(REPO_ROOT))


def _require_candidate_module(name: str, relative_path: str) -> object:
    """Import one canonical project module and reject cached foreign provenance."""

    expected = (REPO_ROOT / relative_path).resolve()
    cached = sys.modules.get(name)
    if cached is not None:
        cached_file = getattr(cached, "__file__", None)
        if cached_file is None or Path(cached_file).resolve() != expected:
            raise ImportError(
                f"cached {name} does not resolve to candidate source {expected}"
            )
    module = importlib.import_module(name)
    resolved = Path(cast(str, getattr(module, "__file__", ""))).resolve()
    if resolved != expected:
        raise ImportError(f"{name} resolved to {resolved}, expected {expected}")
    return module


installer = cast(
    object,
    _require_candidate_module(
        "scripts.install_codex_config", "scripts/install_codex_config.py"
    ),
)
context_owner = cast(
    object,
    _require_candidate_module(
        "scripts.cross_checkout_context", "scripts/cross_checkout_context.py"
    ),
)


FORBIDDEN_WRITES = ["outside/canonical-planning", "outside/installed-home"]
STABLE_ROOTS = {
    "generation": "fixture-stable-controller",
    "roots": [
        {"role": "toolchain-source", "path": "workspace/toolchain-source"},
        {"role": "canonical-planning", "path": "workspace/canonical-planning"},
        {"role": "implementation-target", "path": "workspace/implementation-target"},
    ],
}
CANDIDATE_ROOTS = {
    **STABLE_ROOTS,
    "generation": "fixture-candidate-child",
}
Publisher = Callable[..., None]


class FixtureBoundaryError(RuntimeError):
    """One fail-closed disposable boundary observation."""


@dataclass
class PublicationProbe:
    """Independent filesystem-operation evidence for one visible publication."""

    events: list[str] = field(default_factory=list)

    def stage(self, replacement: Path, target: Path) -> None:
        self.events.append("stage-replacement")
        replacement.symlink_to(target)

    def replace_visible(self, replacement: Path, default: Path) -> None:
        self.events.append("replace-visible-route")
        os.replace(replacement, default)

    def unlink_visible(self, default: Path) -> None:
        self.events.append("unlink-visible-route")
        default.unlink()

    def relink_visible(self, default: Path, target: Path) -> None:
        self.events.append("relink-visible-route")
        default.symlink_to(target)


def observe_cutover(
    scenario: Mapping[str, object], fixture_root: Path
) -> Mapping[str, object]:
    """Observe one case in an adapter-owned disposable workspace."""

    with tempfile.TemporaryDirectory(prefix="command-owner-cutover-") as directory:
        return run_scenario(scenario, fixture_root, Path(directory) / "workspace")


def run_scenario(
    scenario: Mapping[str, object],
    fixture_root: Path,
    workspace: Path,
    *,
    publisher: Publisher | None = None,
) -> Mapping[str, object]:
    """Run one cutover case with every mutable path below ``workspace``."""

    cases = _load_mapping(fixture_root / "cutover-cases.yaml")
    scenario_id = cast(str, scenario["id"])
    case = cast(Mapping[str, object], cases[scenario_id])
    workspace.mkdir(parents=True)
    roots = _seed_roots(workspace)
    protected_before = _protected_fingerprints(roots)
    operation = cast(str, case["operation"])
    fault = cast(str | None, case["fault"])
    if operation == "root-guard":
        outcome = _observe_root_guard(workspace, roots, fault)
    elif operation == "branch-lineage":
        outcome = _observe_branch_lineage(workspace)
    elif operation == "child-generation":
        outcome = _observe_child_generation(workspace)
    elif operation == "install":
        outcome = _observe_install(workspace, fault)
    elif operation == "switch":
        outcome = _observe_switch(workspace, fault, publisher=publisher)
    elif operation == "rollback":
        outcome = _observe_rollback(workspace, publisher=publisher)
    elif operation == "quiescence":
        outcome = _observe_quiescence(workspace, fault)
    elif operation == "bridge":
        outcome = _observe_bridge(workspace)
    elif operation == "physical-absence":
        outcome = _observe_physical_absence(workspace, fixture_root)
    elif operation == "history":
        outcome = _observe_history(workspace)
    else:  # pragma: no cover - schema-backed fixture inventory controls this
        raise AssertionError(f"unknown cutover operation {operation!r}")
    _assert_protected_unchanged(roots, protected_before)
    evidence_path = workspace / "evidence" / f"{scenario_id}.json"
    _write_json(evidence_path, outcome["evidence"])
    return {
        "transition": outcome["transition"],
        "writes": [evidence_path.relative_to(workspace.parent).as_posix()],
        "forbidden_writes": FORBIDDEN_WRITES,
        "stop_reason": outcome["stop_reason"],
        "generation_and_roots": (
            CANDIDATE_ROOTS if operation == "child-generation" else STABLE_ROOTS
        ),
        "validation": outcome["validation"],
    }


def _seed_roots(workspace: Path) -> Mapping[str, Path]:
    roots = {
        "toolchain": workspace / "toolchain-source",
        "planning": workspace / "canonical-planning",
        "implementation": workspace / "implementation-target",
    }
    for name, root in roots.items():
        root.mkdir()
        (root / "identity.json").write_text(
            json.dumps({"root": name}, sort_keys=True) + "\n", encoding="utf-8"
        )
    return roots


def _observe_root_guard(
    workspace: Path, roots: Mapping[str, Path], fault: str | None
) -> Mapping[str, object]:
    _initialize_repository(roots["planning"])
    _initialize_repository(roots["implementation"])
    codex_home = workspace / "strict-codex-home"
    codex_home.mkdir()
    planning_commit = _git(roots["planning"], "rev-parse", "HEAD")
    implementation_commit = _git(roots["implementation"], "rev-parse", "HEAD")
    execution = {
        "toolchain_source_root": str(roots["implementation"].resolve()),
        "toolchain_commit": implementation_commit,
        "canonical_planning_repository_root": str(roots["planning"].resolve()),
        "canonical_planning_commit_before": planning_commit,
        "implementation_target_root": str(roots["implementation"].resolve()),
        "implementation_commit_before": implementation_commit,
        "codex_home": str(codex_home.resolve()),
        "generation_role": "candidate",
        "canonical_state_mutation_allowed": False,
    }
    payload = {"interface": "cross-checkout-context/v1", "execution_context": execution}
    context = context_owner.parse_cross_checkout_context(payload)
    allowed_path = roots["implementation"] / "allowed.txt"
    allowed_scope = context_owner.validate_write_scope(
        context,
        canonical_planning_root=roots["planning"] / "docs" / "plans",
        implementation_paths=(allowed_path,),
    )
    outside_path = workspace / "outside" / "forbidden.txt"
    outside_rejected = False
    try:
        context_owner.validate_write_scope(
            context,
            canonical_planning_root=roots["planning"] / "docs" / "plans",
            implementation_paths=(outside_path,),
        )
    except context_owner.CrossCheckoutContextError:
        outside_rejected = True
    if not outside_rejected:
        raise FixtureBoundaryError("strict scope accepted an outside destination")

    declared = {
        "toolchain": roots["toolchain"].resolve(),
        "planning": roots["planning"].resolve(),
        "implementation": roots["implementation"].resolve(),
        "controller_generation": "fixture-stable-controller",
        "worker_generation": "fixture-stable-controller",
    }
    status = "ready"
    reason = None
    if fault == "canonical-write":
        requested = roots["planning"] / "candidate-write.json"
        try:
            context_owner.validate_write_scope(
                context,
                canonical_planning_root=roots["planning"] / "docs" / "plans",
                planning_paths=(requested,),
            )
        except context_owner.CrossCheckoutContextError:
            status = "blocked"
            reason = "candidate generation cannot write canonical planning"
        else:
            raise FixtureBoundaryError("candidate strict context accepted a planning write")
    elif fault == "mixed-generation":
        declared["worker_generation"] = "fixture-candidate-child"
        mixed_execution = dict(execution)
        mixed_execution.update(
            {
                "toolchain_source_root": str(roots["planning"].resolve()),
                "toolchain_commit": planning_commit,
            }
        )
        try:
            context_owner.parse_cross_checkout_context(
                {
                    "interface": "cross-checkout-context/v1",
                    "execution_context": mixed_execution,
                }
            )
        except context_owner.CrossCheckoutContextError:
            status = "blocked"
            reason = "controller and worker generations differ"
        else:
            raise FixtureBoundaryError("strict context accepted mixed generation roots")
    if len({declared[name] for name in ("toolchain", "planning", "implementation")}) != 3:
        raise AssertionError("three declared roots must be distinct")
    return {
        "transition": f"root-guard:{status}",
        "stop_reason": reason,
        "validation": [
            "root-guard.three-roots.green",
            "root-guard.single-generation.green",
            "root-guard.canonical-write-boundary.green",
        ],
        "evidence": {
            "status": status,
            "reason": reason,
            "roots": {name: str(value) for name, value in declared.items() if name in roots},
            "controller_generation": declared["controller_generation"],
            "worker_generation": declared["worker_generation"],
            "canonical_write_occurred": (roots["planning"] / "candidate-write.json").exists(),
            "allowed_implementation_paths": [
                str(path) for path in allowed_scope.implementation_paths
            ],
            "outside_destination_rejected": outside_rejected,
            "strict_module_origin": str(
                Path(cast(str, getattr(context_owner, "__file__"))).resolve()
            ),
        },
    }


def _observe_branch_lineage(workspace: Path) -> Mapping[str, object]:
    repository = workspace / "lineage-repository"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.name", "Fixture")
    _git(repository, "config", "user.email", "fixture@example.invalid")
    _commit_file(repository, "base.txt", "authoritative base\n", "base")
    base = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "-q", "-b", "accepted-design")
    _commit_file(repository, "design.txt", "accepted design\n", "design")
    design = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "-q", "-b", "implementation", base)
    _commit_file(repository, "candidate.txt", "candidate work\n", "candidate")
    _git(repository, "merge", "-q", "--no-ff", "accepted-design", "-m", "merge design")
    head = _git(repository, "rev-parse", "HEAD")
    base_green = _git_code(repository, "merge-base", "--is-ancestor", base, head) == 0
    design_green = _git_code(repository, "merge-base", "--is-ancestor", design, head) == 0
    if not base_green or not design_green:
        raise FixtureBoundaryError("candidate lineage lost required ancestry")
    return {
        "transition": "branch-lineage:ready",
        "stop_reason": None,
        "validation": [
            "branch-lineage.authoritative-base.green",
            "branch-lineage.accepted-design.green",
        ],
        "evidence": {
            "base": base,
            "accepted_design": design,
            "candidate_head": head,
            "base_is_ancestor": base_green,
            "accepted_design_is_ancestor": design_green,
        },
    }


def _observe_child_generation(workspace: Path) -> Mapping[str, object]:
    candidate_home = workspace / "candidate-home"
    candidate_home.mkdir()
    _write_json(candidate_home / "generation.json", {"generation": "fixture-candidate-child"})
    expected_module = (REPO_ROOT / "scripts" / "install_codex_config.py").resolve()
    code = "\n".join(
        (
            "import importlib, json, os, pathlib",
            "home = pathlib.Path(os.environ['FIXTURE_CODEX_HOME'])",
            "module = importlib.import_module('scripts.install_codex_config')",
            "origin = pathlib.Path(module.__file__).resolve()",
            "expected = pathlib.Path(os.environ['EXPECTED_PROJECT_MODULE']).resolve()",
            "if origin != expected: raise SystemExit(f'foreign module: {origin}')",
            "payload = json.loads((home / 'generation.json').read_text())",
            "payload['module_origin'] = str(origin)",
            "print(json.dumps(payload, sort_keys=True))",
        )
    )
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONHOME", "PYTHONPATH"}
    }
    env.update(
        {
            "FIXTURE_CODEX_HOME": str(candidate_home),
            "EXPECTED_PROJECT_MODULE": str(expected_module),
            "PYTHONPATH": str(REPO_ROOT),
            "PYTHONSAFEPATH": "1",
        }
    )
    process = subprocess.run(
        [sys.executable, "-P", "-c", code],
        cwd=workspace,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    observed = json.loads(process.stdout)
    if (
        process.returncode != 0
        or observed["generation"] != "fixture-candidate-child"
        or Path(cast(str, observed["module_origin"])).resolve() != expected_module
    ):
        raise FixtureBoundaryError("child did not resolve the candidate generation")
    return {
        "transition": "candidate-child:ready",
        "stop_reason": None,
        "validation": ["candidate-child.explicit-home.green", "candidate-child.generation.green"],
        "evidence": {
            "exit_code": process.returncode,
            "resolved_generation": observed["generation"],
            "explicit_home": str(candidate_home),
            "module_origin": observed["module_origin"],
            "sanitized_pythonpath": str(REPO_ROOT),
        },
    }


def _observe_install(workspace: Path, fault: str | None) -> Mapping[str, object]:
    source, manifest_path, manifest = _seed_manifest(workspace, fault)
    _stable, _candidate, default = _seed_visible_generations(workspace)
    default_before = _visible_generation(default)
    staging = workspace / "install-staging"
    published = workspace / "generations" / "candidate"
    error: str | None = None
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            installer.install_features(
                source,
                staging,
                manifest_path,
                manifest,
                ["fixture"],
                dry_run=False,
                force=False,
            )
        except installer.InstallError as exception:
            error = str(exception)
    staged_link_observed = (staging / "skills" / "fixture").is_symlink()
    if error is None:
        published.parent.mkdir()
        os.replace(staging, published)
        linked = published / "skills" / "fixture"
        state = installer.load_state(published)
        if not linked.is_symlink() or "fixture" not in state["features"]:
            raise FixtureBoundaryError("published generation lacks link or state evidence")
        status = "ready"
        reason = None
    else:
        shutil.rmtree(staging, ignore_errors=True)
        status = "blocked"
        reason = (
            "partial install did not publish a generation"
            if fault == "partial"
            else "stale link did not publish a generation"
        )
    default_after = _visible_generation(default)
    if (default_before, default_after) != ("stable", "stable"):
        raise FixtureBoundaryError("installation changed the visible generation")
    return {
        "transition": f"installer:{status}",
        "stop_reason": reason,
        "validation": [
            "installer.disposable-root.green",
            "installer.publish-atomic.green",
            "installer.failure-closed.green",
        ],
        "evidence": {
            "status": status,
            "installer_error": error,
            "published": published.exists(),
            "staged_link_observed": staged_link_observed,
            "staging_removed": not staging.exists(),
            "default_generation_before": default_before,
            "default_generation_after": default_after,
            "default_generation_unchanged": default_before == default_after,
            "installer_module_origin": str(
                Path(cast(str, getattr(installer, "__file__"))).resolve()
            ),
        },
    }


def _seed_manifest(
    workspace: Path, fault: str | None
) -> tuple[Path, Path, dict[str, object]]:
    source = workspace / "install-source"
    (source / "skills" / "fixture").mkdir(parents=True)
    (source / "skills" / "fixture" / "SKILL.md").write_text("fixture\n", encoding="utf-8")
    links = [{"source": "skills/fixture", "target": "skills/fixture"}]
    if fault == "partial":
        links.append({"source": "skills/missing", "target": "skills/missing"})
    manifest: dict[str, object] = {
        "schema_version": 1,
        "features": {
            "fixture": {
                "version": "1",
                "description": "disposable fixture",
                "links": links,
            }
        },
    }
    manifest_path = source / "manifest.json"
    _write_json(manifest_path, manifest)
    if fault == "stale-link":
        staging_target = workspace / "install-staging" / "skills" / "fixture"
        staging_target.parent.mkdir(parents=True)
        staging_target.symlink_to(workspace / "stale-source")
    return source, manifest_path, manifest


def _seed_visible_generations(workspace: Path) -> tuple[Path, Path, Path]:
    stable = workspace / "visible-generations" / "stable"
    candidate = workspace / "visible-generations" / "candidate"
    for root, generation in ((stable, "stable"), (candidate, "candidate")):
        root.mkdir(parents=True)
        _write_json(root / "generation.json", {"generation": generation})
    default = workspace / "default-generation"
    default.symlink_to(stable)
    return stable, candidate, default


def _visible_generation(default: Path) -> str:
    return cast(str, json.loads((default / "generation.json").read_text())["generation"])


def _atomic_bind(
    default: Path,
    target: Path,
    *,
    probe: PublicationProbe,
    before_replace: Callable[[], None] | None = None,
    after_replace: Callable[[], None] | None = None,
) -> None:
    replacement = default.with_name(f"{default.name}.next")
    probe.stage(replacement, target)
    if before_replace is not None:
        before_replace()
    probe.replace_visible(replacement, default)
    if after_replace is not None:
        after_replace()


def _require_atomic_publication(
    probe: PublicationProbe, *, expected_publications: int
) -> None:
    if any(
        event in {"unlink-visible-route", "relink-visible-route"}
        for event in probe.events
    ):
        raise FixtureBoundaryError("visible route was unlinked or relinked")
    if probe.events.count("replace-visible-route") != expected_publications:
        raise FixtureBoundaryError(
            "visible route publication did not use exactly one replacement boundary"
        )


def _observe_switch(
    workspace: Path, fault: str | None, *, publisher: Publisher | None
) -> Mapping[str, object]:
    _stable, candidate, default = _seed_visible_generations(workspace)
    before = _visible_generation(default)
    reader_observations: list[str] = []
    missing_route_observations = 0
    probe = PublicationProbe()
    bind = publisher or _atomic_bind

    def read_visible() -> None:
        nonlocal missing_route_observations
        if not default.exists():
            missing_route_observations += 1
            return
        reader_observations.append(_visible_generation(default))

    def before_replace() -> None:
        read_visible()
        if fault == "before-publish":
            raise FixtureBoundaryError("switch interrupted before publish")

    status = "switched"
    reason = None
    try:
        bind(
            default,
            candidate,
            probe=probe,
            before_replace=before_replace,
            after_replace=read_visible,
        )
    except FixtureBoundaryError as error:
        default.with_name(f"{default.name}.next").unlink(missing_ok=True)
        status = "blocked"
        reason = str(error)
        read_visible()
    _require_atomic_publication(probe, expected_publications=0 if fault else 1)
    after = _visible_generation(default)
    expected_after = "stable" if fault else "candidate"
    if (before, after) != ("stable", expected_after):
        raise FixtureBoundaryError("atomic switch did not expose one complete generation")
    return {
        "transition": f"cutover:{status}",
        "stop_reason": reason,
        "validation": ["cutover.atomic-visible-generation.green", "cutover.stable-controller.green"],
        "evidence": {
            "before": before,
            "after": after,
            "controller": "stable",
            "reader_observations": reader_observations,
            "missing_route_observations": missing_route_observations,
            "publication_events": probe.events,
        },
    }


def _observe_rollback(
    workspace: Path, *, publisher: Publisher | None
) -> Mapping[str, object]:
    stable, candidate, default = _seed_visible_generations(workspace)
    reader_observations: list[str] = []
    missing_route_observations = 0
    switch_probe = PublicationProbe()
    rollback_probe = PublicationProbe()
    bind = publisher or _atomic_bind

    def read_visible() -> None:
        nonlocal missing_route_observations
        if not default.exists():
            missing_route_observations += 1
            return
        reader_observations.append(_visible_generation(default))

    before = _visible_generation(default)
    bind(
        default,
        candidate,
        probe=switch_probe,
        before_replace=read_visible,
        after_replace=read_visible,
    )
    _require_atomic_publication(switch_probe, expected_publications=1)
    switched = _visible_generation(default)
    bind(
        default,
        stable,
        probe=rollback_probe,
        before_replace=read_visible,
        after_replace=read_visible,
    )
    _require_atomic_publication(rollback_probe, expected_publications=1)
    restored = _visible_generation(default)
    if (before, switched, restored) != ("stable", "candidate", "stable"):
        raise FixtureBoundaryError("rollback did not restore the recorded generation")
    return {
        "transition": "cutover:rolled-back",
        "stop_reason": None,
        "validation": ["cutover.rollback-checkpoint.green", "cutover.atomic-visible-generation.green"],
        "evidence": {
            "before": before,
            "switched": switched,
            "restored": restored,
            "reader_observations": reader_observations,
            "missing_route_observations": missing_route_observations,
            "publication_events": [switch_probe.events, rollback_probe.events],
        },
    }


def _observe_quiescence(workspace: Path, fault: str | None) -> Mapping[str, object]:
    state = {"selected": None, "queued": None, "active": None}
    if fault == "active-work":
        state["active"] = "fixture-runway"
    _write_json(workspace / "quiescence-state.json", state)
    ready = all(value is None for value in state.values())
    return {
        "transition": f"quiescence:{'ready' if ready else 'blocked'}",
        "stop_reason": None if ready else "cutover requires quiescent planning state",
        "validation": ["cutover.quiescence.green", "cutover.stable-controller.green"],
        "evidence": {"ready": ready, "state": state, "controller": "stable"},
    }


def _observe_bridge(workspace: Path) -> Mapping[str, object]:
    planning = workspace / "canonical-planning" / "CURRENT.md"
    planning.write_text("authority: master\n", encoding="utf-8")
    bridge = workspace / "temporary-control" / "strict-context.json"
    _write_json(
        bridge,
        {"interface": "cross-checkout-context/v1", "planning_authority": "master"},
    )
    receipt = json.loads(bridge.read_text())
    if receipt["planning_authority"] != "master":
        raise FixtureBoundaryError("temporary control lost canonical planning authority")
    return {
        "transition": "cutover:pre-cutover-ready",
        "stop_reason": None,
        "validation": ["cutover.minimum-control.green", "cutover.master-planning.green"],
        "evidence": {
            "control_interface": receipt["interface"],
            "planning_authority": receipt["planning_authority"],
            "scope": "root-generation-and-receipt-only",
        },
    }


def _observe_physical_absence(
    workspace: Path, fixture_root: Path
) -> Mapping[str, object]:
    target = workspace / "synthetic-target"
    target.mkdir()
    (target / "command-owner.md").write_text(
        "target behavior is owned by the command surface\n", encoding="utf-8"
    )
    catalog = _load_mapping(fixture_root / "catalog.yaml")
    forbidden_tokens = set(cast(list[str], catalog["forbidden_target_terms"]))
    content = "\n".join(path.read_text() for path in target.rglob("*") if path.is_file())
    present = sorted(token for token in forbidden_tokens if token in content)
    bridge_present = (target / "temporary-control").exists()
    if present or bridge_present:
        raise FixtureBoundaryError("synthetic target retains forbidden topology")
    return {
        "transition": "physical-absence:synthetic-ready",
        "stop_reason": None,
        "validation": ["physical-absence.synthetic-only.green", "physical-absence.target-independent.green"],
        "evidence": {
            "synthetic_fixture": True,
            "real_deletion_claimed": False,
            "bridge_present": bridge_present,
            "forbidden_target_terms": present,
        },
    }


def _observe_history(workspace: Path) -> Mapping[str, object]:
    planning_root = workspace / "canonical-planning" / "docs" / "plans"
    program = planning_root / "programs" / "fixture"
    live_batch = program / "batches" / "live-batch"
    live_batch.mkdir(parents=True)
    (live_batch / "dispatch.md").write_text("# Live Dispatch\n", encoding="utf-8")
    (program / "LEDGER.md").write_text("# Fixture Ledger\n", encoding="utf-8")
    planning_root.mkdir(parents=True, exist_ok=True)
    (planning_root / "CURRENT.md").write_text(
        "# Planning Current State\n\n- Layout: Planning Artifact Layout v1\n"
        "- Planning root: `docs/plans/`\n\n## Active Programs\n\n"
        "| Program | Current state |\n|---|---|\n"
        "| `fixture` | `docs/plans/programs/fixture/CURRENT.md` |\n",
        encoding="utf-8",
    )
    live_selected = (
        "docs/plans/programs/fixture/batches/live-batch/dispatch.md"
    )
    (program / "CURRENT.md").write_text(
        "# Fixture Current State\n\nProgram slug: `fixture`\n\n"
        "- Current ledger: `docs/plans/programs/fixture/LEDGER.md`\n"
        f"- Selected dispatch path: `{live_selected}`\n"
        "- Active Batch Runway spec path: `None`\n"
        "- Queued batch path or ID: `None`\n"
        "- Latest closeout: `None`\n",
        encoding="utf-8",
    )
    archive = planning_root / "archive" / "historical-active-runway.md"
    archive.parent.mkdir()
    archive.write_text(
        "# Historical Current\n\n"
        "selected_dispatch: archived-dispatch\n"
        "active_runway: archived-runway\n",
        encoding="utf-8",
    )
    script = (REPO_ROOT / "scripts" / "planning_state.py").resolve()
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONHOME", "PYTHONPATH"}
    }
    env["PYTHONPATH"] = str(REPO_ROOT)
    completed = subprocess.run(
        [
            sys.executable,
            "-P",
            str(script),
            "current",
            "--root",
            str(planning_root),
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise FixtureBoundaryError(
            f"Planning State current failed: {completed.stderr.strip()}"
        )
    current = cast(dict[str, object], json.loads(completed.stdout))
    programs = cast(list[Mapping[str, object]], current["programs"])
    selected = cast(
        Mapping[str, object], programs[0]["selected_dispatch"]
    )["value"]
    historical_text = archive.read_text(encoding="utf-8")
    if selected != live_selected or "archived-runway" not in historical_text:
        raise FixtureBoundaryError("Planning State did not preserve live pickup authority")
    return {
        "transition": "history:readable-nonauthoritative",
        "stop_reason": None,
        "validation": ["history.readable.green", "history.current-only-pickup.green"],
        "evidence": {
            "historical": {
                "selected_dispatch": "archived-dispatch",
                "active_runway": "archived-runway",
            },
            "pickup": selected,
            "authority": "planning-state-current",
            "planning_state_origin": str(script),
            "archive_readable": True,
        },
    }


def _protected_fingerprints(roots: Mapping[str, Path]) -> Mapping[str, str]:
    return {name: _digest(root / "identity.json") for name, root in roots.items()}


def _assert_protected_unchanged(
    roots: Mapping[str, Path], before: Mapping[str, str]
) -> None:
    after = _protected_fingerprints(roots)
    if after != before:
        raise FixtureBoundaryError("scenario mutated a protected root identity")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_mapping(path: Path) -> Mapping[str, object]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise TypeError(f"{path} must contain a mapping")
    return cast(Mapping[str, object], loaded)


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=repository, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def _git_code(repository: Path, *arguments: str) -> int:
    return subprocess.run(
        ["git", *arguments], cwd=repository, capture_output=True, check=False
    ).returncode


def _initialize_repository(repository: Path) -> None:
    _git(repository, "init", "-q")
    _git(repository, "config", "user.name", "Fixture")
    _git(repository, "config", "user.email", "fixture@example.invalid")
    (repository / "docs" / "plans").mkdir(parents=True)
    (repository / "docs" / "plans" / ".keep").write_text("fixture\n", encoding="utf-8")
    _git(repository, "add", ".")
    _git(repository, "commit", "-q", "-m", "fixture identity")


def _commit_file(repository: Path, name: str, content: str, message: str) -> None:
    (repository / name).write_text(content, encoding="utf-8")
    _git(repository, "add", name)
    _git(repository, "commit", "-q", "-m", message)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
