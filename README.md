# Codex Config

Personal Codex configuration, workflows, skills, agents, and operating procedures.

This repository contains the source-controlled portion of my Codex environment. It is intended to capture reusable agent behavior, workflow evolution, and operational knowledge while keeping runtime state, logs, caches, sessions, and secrets outside version control.

## Purpose

This repository serves as:

* The source of truth for personal Codex skills and agents.
* A versioned history of workflow improvements.
* A place to evolve agent orchestration patterns.
* A reproducible configuration that can be installed on a new machine.

It is not intended to store runtime state.

## Philosophy

Treat agent workflows as software.

Skills, agents, prompts, execution contracts, validation profiles, and operating procedures are maintained, reviewed, versioned, and improved like any other codebase.

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
