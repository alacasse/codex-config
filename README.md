# Codex Config

Source-controlled Codex configuration delivered by a manifest-driven installer.
The repository configures Codex; it does not implement a task-execution runtime.

## What this repository owns

- a generic feature installer with isolated-home, dry-run, status, and stale
  managed-link cleanup support;
- distinct global operating instructions and repository-local development
  guidance;
- a project-neutral documentation-root selector with a repository-local
  override;
- ownership inspection for repository-managed Codex paths;
- focused, optional skills for test-quality review, contract-first ports, and
  dead-surface audits;
- read-only investigation, general review, and import-topology review agents;
- completion-notification resources with the active `Stop` hook disabled;
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

## Project documentation roots

Global instructions use `docs` as the default documentation root for questions
about project status, plans, decisions, or architecture. A repository can select
a different root without changing tracked files:

```bash
git config --local codex.docs-root project-docs
```

The selector accepts only an existing repository-relative directory whose
resolved path stays inside the repository. Its `AGENTS.md`, when present, is a
documentation index; normally discovered Codex instructions retain their usual
scope and precedence.

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

After upgrading `global-instructions` from 2.0.1 to 3.1.0, preview and apply the
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

## Subagent model routing

Ordinary subagents use the native defaults in the user's `config.toml`:

```toml
[agents]
default_subagent_model = "gpt-6.1-sol"
default_subagent_reasoning_effort = "low"
```

Merge only these two keys into an existing `[agents]` table, preserving its
other settings. Do not add a second table or replace the personal config.
Back up the file before editing it. These central defaults cover native agents
and `codebase_investigator`; an explicit spawn model or effort can override
them. The installer deliberately does not own or rewrite `config.toml`.

Register the custom role layers in that same personal config, using the
canonical absolute checkout path reported by `codex-owner`:

```toml
[agents.codebase_investigator]
config_file = "/absolute/checkout/agents/codebase_investigator.toml"

[agents.reviewer]
config_file = "/absolute/checkout/agents/reviewer.toml"

[agents.import_topology_reviewer]
config_file = "/absolute/checkout/agents/import_topology_reviewer.toml"
```

Replace `/absolute/checkout` with the resolved repository directory. This is
needed by the desktop CLI `0.159.0-alpha.12.1`: discovery finds the installed
role symlinks, but applying a role from a symlink fails with `Symbolic link loop`.
The native `config_file` declarations refer directly to the regular source
files, preserving the installer's managed symlinks without relaxing filesystem
security. Recheck these three paths if the checkout is moved. Keep role
instructions in their source files instead of copying them into personal config.

The ordinary agents inherit the parent's service tier. In the approved personal
setup the principal already uses `service_tier = "priority"`, which requests
Fast. Leave its model, effort and tier unchanged. Codex has no documented
`agents.default_subagent_service_tier`; do not invent that key. If the parent's
tier is changed later, revisit this inherited choice explicitly.

Use `reviewer` for general diff review and `import_topology_reviewer` for its
existing specialist lens. Both explicitly select `gpt-6-astra`, `medium`, and
`service_tier = "fast"`. These are the only model exceptions. Native standalone
agent files have no documented shared review-profile inheritance, so changing
the review selection requires updating those two files together. All three
custom agents enforce `sandbox_mode = "read-only"` and
`approval_policy = "never"`; blocked checks are reported rather than escalating
or applying fixes. Native workers retain their parent's permissions.

Install or upgrade the role files through the existing path:

```bash
./install.sh --feature custom-agents --dry-run
./install.sh --feature custom-agents
```

The feature neither activates notifications nor changes principal settings.
Start a new session after changing defaults. Existing threads retain their
session selections. This policy governs named subagents, not `/review` or
`codex review`; it does not set `review_model` or change the separate approval
reviewer configured by `approvals_reviewer`.

The installed desktop CLI `0.159.0-alpha.12.1` recognizes these native settings. Confirm
the selected models are available to the signed-in account before adopting the
policy elsewhere; do not silently substitute an unavailable model. Fast is a
requested tier (`fast` normalizes to `priority`), not proof of the tier served
by the backend or a latency guarantee. See the official
[subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
and [profile limitations](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles).

## GitHub tracker setup

Check the triage and Wayfinder label adapter against an explicit repository:

```bash
./scripts/setup_github_labels.py --repo alacasse/codex-config
```

`--apply` creates only missing labels with approved metadata and never edits an
existing same-name label. It changes external GitHub state and should be run
only after the reported operations are approved.

## Completion notification hook (disabled)

The `agent-notifications` feature installs the notification implementation and
an active `hooks.json` that does not register a `Stop` hook. The former
registration remains in `hooks/agent_done_hooks.example.json` as an explicit
reference if completion notifications are intentionally restored later:

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
