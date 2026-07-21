# Codex Config

Personal, source-controlled Codex configuration with a manifest-driven
installer. The repository configures and guides Codex; native Codex owns
task-internal planning, delegation, review correction, and integration.

## What survives here

- a generic feature installer with isolated-home, dry-run, status, and stale
  managed-link cleanup support;
- ownership inspection for repository-managed Codex paths;
- focused, optional skills for test-quality review, contract-first ports, and
  dead-surface audits;
- read-only investigation and import-topology review agents;
- an opt-in completion-notification hook;
- compact repository-specific issue and triage configuration.

The historical planning and execution experiment is preserved in Git archive
branches rather than installed or maintained on the active line.

## Install

Preview the default installation without writing:

```bash
./install.sh --dry-run
```

Install the default feature set:

```bash
./install.sh
```

Use an isolated Codex home for tests or evaluation:

```bash
./install.sh --codex-home /tmp/codex-home
```

List or select features:

```bash
./install.sh --list
./install.sh --feature test-quality-review
./install.sh --all
```

The manifest at `codex-features.json` is the source of truth for feature names,
versions, dependencies, and repo-owned source-to-target links. Default-enabled
features install unless `--feature` or `--all` selects another set.

Targets are symlinks. Existing real files and foreign symlinks are preserved;
`--force` is required to back up a real-file conflict or replace a conflicting
symlink during installation.

## Status and stale managed links

Installed state is recorded under the selected Codex home at:

```text
codex-config/installed-features.json
```

After upgrading to a manifest that removes a feature or one of its links, first
inspect and prune stale managed links:

```bash
./install.sh --status
./install.sh --prune --dry-run
./install.sh --prune
./install.sh
```

Pruning only removes a target that is still a symlink to the exact source
recorded in the previous installed state. Missing targets are reconciled.
Retargeted symlinks and real files are reported and preserved, and the prune
fails before changing anything.

## Ownership inspection

Check whether a repository source or installed target is owned by this
configuration:

```bash
./scripts/codex_owner.py ~/.codex/skills/test-quality-review
./scripts/codex_owner.py --json ~/.codex/AGENTS.md
```

The ownership tool uses the current manifest. Use installer `--status` and
`--prune` for links recorded by an older manifest.

## Optional notification hook

The `agent-notifications` feature installs the principal-agent `Stop` hook. It
is opt-in because it may replace an existing `hooks.json` target:

```bash
./install.sh --feature agent-notifications
```

See `hooks/README.md` for backend configuration.

## Development validation

```bash
UV_CACHE_DIR=/tmp/codex-config-uv-cache uv run --frozen pytest -q
UV_CACHE_DIR=/tmp/codex-config-uv-cache uv run --frozen ruff check scripts hooks tests
UV_CACHE_DIR=/tmp/codex-config-uv-cache uv run --frozen basedpyright
git diff --check
```

Never point validation installs at the real active Codex home.
