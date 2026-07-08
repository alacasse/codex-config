# Codex Config

Personal Codex configuration, workflows, skills, agents, and operating procedures.

This repository contains the source-controlled portion of my Codex environment.
It captures reusable agent behavior, workflow evolution, and operational
knowledge while keeping runtime state, logs, caches, sessions, and secrets
outside version control.

The repo is not a generic starter kit. It is a working configuration system for
agent-assisted software development: skills, custom agents, rules, hooks,
planning conventions, validation protocols, and installer metadata that can be
reviewed and improved like production code.

## Purpose

This repository exists to make agent-assisted engineering more explicit,
repeatable, and inspectable.

It serves as:

* The source of truth for personal Codex skills and agents.
* A versioned history of workflow improvements.
* A place to evolve agent orchestration patterns.
* A reproducible configuration that can be installed on a new machine.
* A durable record of decisions about validation, delegation, planning, and
  recovery behavior.

It is intentionally not a place for runtime state, private credentials, model
caches, local sessions, or generated logs.

## Principles

### Treat agent workflows as software

Skills, agents, prompts, execution contracts, validation profiles, and operating
procedures are maintained, reviewed, versioned, and improved like any other
codebase.

### Prefer durable process over repeated instruction

When a useful behavior is repeatedly explained to an agent, it should become a
skill, rule, validation check, planning artifact, or documented protocol.
The system should accumulate reusable procedures instead of rediscovering them
from chat context.

### Keep reusable workflows project-neutral

Repo-owned skills are reusable workflow code. They should not hard-code one
project's paths, commands, cache locations, issue policy, or planning layout.
Project-specific behavior belongs in that project's instructions, local overlay,
active spec, or reference document.

### Separate source-controlled behavior from runtime state

This repo tracks configuration and workflow contracts. The live Codex runtime is
kept separate so local sessions, secrets, generated databases, and caches do not
become hidden dependencies of the source tree.

### Make validation part of the workflow

Changes should leave behind enough evidence for another agent or human reader to
understand what changed, why it changed, and how the behavior was checked.

### Optimize for resumption

Planning state, ledgers, closeout notes, and changelog entries are used so work
can be resumed without relying on a single conversation transcript.

## Repository Contents

The repository is organized around the parts of my Codex setup that are stable
enough to version and reuse:

* reusable skills for multi-slice implementation, review, planning, porting,
  legacy cleanup, and test-quality review
* custom agents for focused exploration, implementation, and review roles
* ownership tooling for distinguishing repo-owned Codex files from vendor-owned
  or unmanaged runtime files
* planning-state tooling for active work discovery, queueing, closeout evidence,
  and optional reporting projections
* architecture-runner and planning-runner contracts that are being shaped here
  before extraction into a reusable implementation
* installation tooling that links repo-owned features into `~/.codex` while
  preserving ownership boundaries
* changelog discipline focused on problem, decision, and expected effect

## Skills

Repo-owned skills live under `skills/` and are installed into Codex through the
feature manifest. They are written as reusable workflows: each skill defines
when it should be used, what context it must read, what it owns, and where it
must stop instead of guessing.

During the command-owner migration, use
`docs/skill-routing-contract.md` to resolve human intent ownership, runtime
support routing, conflict rules, and stop conditions.

For end-to-end workflow usage, including how external engineering skills feed
the canonical ledger-driven workflow, see `docs/workflow-guide.md`.

### User-Facing Workflow Commands

These are the preferred command-owner skills to invoke directly for the main
planning and execution workflow.

| Skill | Purpose | How it is used |
| --- | --- | --- |
| `add-to-ledger` | Adds findings and work requests to a durable planning ledger. | Used when the user wants to capture a new issue, improvement, or investigation request without selecting a batch yet. |
| `plan-batch` | Selects bounded ledger work and writes one concrete batch spec. | Used when the user wants the next executable batch planned from current ledger state, then wants the agent to stop before implementation. |
| `work-batch` | Executes the current queued or active batch runway. | Used when the user wants the agent to resume planned batch work through implementation, validation, review, and closeout. |
| `port-by-contract` | Extracts implementation-neutral behavior contracts before a rewrite, migration, or port. | Used directly when moving behavior across languages, runtimes, or product boundaries without copying accidental source structure. |

### Agent-Facing Support And Runtime Surfaces

These skills remain installed because command-owner workflows use them as
agent-facing support. They are not the preferred direct commands for the main
ledger and batch workflow.

| Skill | Purpose | How it is used |
| --- | --- | --- |
| `batch-runway` | Provides bounded multi-slice runway spec mechanics, per-slice validation, commits, ledger updates, and implementation/review delegation. | Invoked behind `plan-batch` or `work-batch` when a command-owned batch needs concrete spec creation or execution contracts. |
| `architecture-program-runway` | Provides program-ledger grouping, sequencing, selected dispatch, queue state, and closeout reconciliation. | Invoked behind `add-to-ledger` or `plan-batch` when broad findings need durable grouping or selected-batch state. |
| `test-quality-review` | Reviews tests for behavioral confidence, regression protection, assertion strength, fixture friction, and design signals. | Invoked by review routes or directly for focused test audits where coverage percentage is not the main question. |
| `dead-surface-audit` | Finds code surfaces kept alive by tests that assert imports, aliases, topology, or compatibility shape rather than behavior. | Invoked as evidence support when legacy, review, or planning work needs proof about test-retained dead surfaces. |
| `legacy-removal` | Scopes evidence-backed legacy cleanup before implementation planning. | Invoked only for exceptional obsolete paths, fallback behavior, stale names, compatibility shims, or cleanup residues that need classification and a removal handoff. |
| `planning-artifacts` | Defines project-agnostic placement and naming conventions for durable planning docs, ledgers, dispatch packets, run artifacts, outputs, and archives. | Used when creating, migrating, or interpreting planning roots and workflow artifacts across projects. |
| `planning-state` | Discovers, validates, bootstraps, projects, and reports current planning state before ledger-driven workflows consume it. | Used as the diagnostic hot path for active work pickup, queued batches, closeout evidence, and safe state/projection target checks. |

## Future Runner Extraction

Some runner-related work currently lives in this repository because it is still
being shaped against the Codex workflow environment. The long-term direction is
to extract the reusable runner core into a separate Go project so it can support
other automation and orchestration use cases without depending on this personal
Codex configuration.

This repo should keep the contracts, planning artifacts, and Codex-specific
integration guidance needed to use that runner from Codex. The future Go project
should own the portable runner implementation, command surface, and reusable
runtime behavior.

The goal is to continuously reduce:

* repetitive coordination work
* procedural debt
* context reconstruction costs
* manual orchestration effort

while improving:

* reliability
* repeatability
* validation quality
* agent autonomy

## How To Read This Repo

Start with:

* `README.md` for the project model and install flow.
* `codex-features.json` for the manifest of repo-owned installable features.
* `skills/` for the reusable workflows listed above.
* `agents/` for custom role definitions.
* `rules/` for shared policy and guidance.
* `hooks/` for lifecycle automation.
* `docs/plans/` for durable planning-state and workflow design artifacts.
* `CHANGELOG.md` for the decision history behind meaningful workflow changes.

## Repository Structure

```text
codex-config/
├── AGENTS.md
├── CHANGELOG.md
├── codex-features.json
├── install.sh
├── scripts/
├── skills/
├── agents/
├── rules/
├── hooks/
├── docs/
├── tests/
└── .codex/
```

## Installing

Install the default versioned Codex features:

```bash
./install.sh
```

Default install only links features with `default_enabled` omitted or set to
`true` in `codex-features.json`. Vendor-owned items should be omitted from this
manifest and installed by their own provider.

Preview changes without writing to `~/.codex`:

```bash
./install.sh --dry-run
```

List available features:

```bash
./install.sh --list
```

Install one feature:

```bash
./install.sh --feature batch-runway
```

Feature dependencies declared with `requires` in `codex-features.json` are
installed first.

Install every manifest entry:

```bash
./install.sh --all
```

If a target already exists and is not the expected symlink, the installer stops.
Use `--force` only when you want conflicting symlinks replaced and real files
backed up before linking.

Installed feature versions are recorded in:

```text
~/.codex/codex-config/installed-features.json
```

The manifest in `codex-features.json` is the source of truth for feature names,
versions, default install mode, and source-to-target links owned by this repo.

It is not a full inventory of `~/.codex`. Vendor-owned skills, rules, and agents
should be installed by their own provider and left out of this manifest.

Repo-owned features are installed as symlinks. Editing the installed
`~/.codex/...` path edits this repository.

To check ownership for a `~/.codex` path:

```bash
scripts/codex_owner.py ~/.codex/AGENTS.md
```

The ownership check distinguishes manifest declaration from active
installation. A path can have `manifest_owner: codex-config` because it matches
`codex-features.json`, while `installed_owner: none` and a non-`linked` status
mean the runtime path is not currently backed by the repository symlink.

Install statuses include:

* `linked`
* `missing`
* `unlinked_copy`
* `wrong_symlink`
* `conflict_file`
* `conflict_directory`

### AGENTS.md

Global operating instructions used across projects.

Contains:

* workflow conventions
* orchestration preferences
* validation expectations
* execution policies

### skills/

Reusable skills.

Examples:

* batch-runway
* planning-artifacts
* planning workflows
* review workflows
* documentation workflows

### agents/

Custom agents.

Examples:

* runway_worker
* runway_reviewer

### rules/

Shared reusable guidance and policy files.

### CHANGELOG.md

Records meaningful workflow evolution.

Focus on:

* why a change was introduced
* what problem it solved
* expected impact

Do not use it as a commit log.

## Runtime Separation

The live Codex runtime is intentionally not stored in this repository.

Examples of runtime state:

```text
auth.json
cache/
sessions/
shell_snapshots/
*.sqlite
*.sqlite-shm
*.sqlite-wal
*.jsonl
logs/
tmp/
```

These belong to the local Codex installation and should never be committed.

## Workflow Evolution

This repository is expected to evolve.

New skills, agents, validation strategies, memory patterns, orchestration techniques, and execution protocols should be versioned here as they become stable enough to reuse.

The objective is not to create a perfect system.

The objective is to continuously improve how work is delegated, validated, resumed, and completed.

## Changelog Policy

Update `CHANGELOG.md` when a change meaningfully affects:

* agent behavior
* workflow behavior
* orchestration
* validation
* memory usage
* recovery behavior
* skill contracts
* execution protocols

For each entry, document:

* the problem
* the decision
* the expected effect

rather than implementation details.

## Design Principle

When a useful behavior is repeatedly explained to an agent, consider turning it into:

* a skill
* an agent
* a reusable rule
* a validation profile
* a documented protocol

The system should accumulate reusable procedures instead of repeatedly rediscovering them.
