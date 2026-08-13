# Codex Config

Source-controlled Codex configuration delivered by a manifest-driven installer.
The repository configures Codex; it does not implement a task-execution runtime.

## What this repository owns

- a generic feature installer with isolated-home, dry-run, status, and stale
  managed-link cleanup support;
- distinct global operating instructions and repository-local development
  guidance;
- ownership inspection for repository-managed Codex paths;
- focused, optional skills for test-quality review, contract-first ports, and
  dead-surface audits;
- read-only investigation and import-topology review agents;
- an opt-in completion-notification hook;
- compact repository-specific issue and triage configuration.

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
symlink during installation. When a feature changes the source for an existing
target, the installer retargets it without `--force` only if the current symlink
still matches the source recorded in installed state.

The repository root `AGENTS.md` contains development instructions for this
repository. The separate `global/AGENTS.md` is installed as the Codex-home
`AGENTS.md`, so repository paths and policies do not leak into other projects.

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

After upgrading `global-instructions` from 2.0.1 to 3.0.1, preview and apply the
managed source migration:

```bash
./install.sh --dry-run
./install.sh
```

The second command safely retargets the previously managed `AGENTS.md` and
installs `bin/codex-owner`. It does not require `--force` while the old link
still matches its recorded source.

## Ownership inspection

Check whether a repository source or installed target is owned by this
configuration:

```bash
./scripts/codex_owner.py ~/.codex/skills/test-quality-review
./scripts/codex_owner.py --json ~/.codex/AGENTS.md
~/.codex/bin/codex-owner ~/.codex/AGENTS.md
```

The installed command belongs to the default `global-instructions` feature; use
the equivalent path under `CODEX_HOME` when a non-default home is active. The
ownership tool uses the current manifest. Use installer `--status` and `--prune`
for links recorded by an older manifest.

## GitHub tracker setup

Check the triage and Wayfinder label adapter against an explicit repository:

```bash
./scripts/setup_github_labels.py --repo alacasse/codex-config
```

`--apply` creates only missing labels with approved metadata and never edits an
existing same-name label. It changes external GitHub state and should be run
only after the reported operations are approved.

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
