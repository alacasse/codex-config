# Changelog

## 2026-08-31 - Explicit port-by-contract invocation

### Problem

Automatic invocation repeatedly restarted contract extraction during rewrite,
migration, replacement, and behavior-preservation work even when an accepted
contract already existed as the durable authority.

### Decision

- Disable implicit invocation for `port-by-contract` while preserving explicit
  `$port-by-contract` use.
- Publish `port-by-contract` version 2.0.2.

### Expected effect

Agents consume accepted contracts during ordinary design and implementation
work, while users can still explicitly invoke the skill to produce or revalidate
an implementation-neutral contract.

## 2026-08-20 - Documentation and target repository roles

### Problem

When local project documentation lived in an independent repository, an agent
could confuse the repository that owned the documents with the repository where
the documented implementation and branch workflow applied. Moving that
workflow into global configuration would instead leak one project's topology
into every repository.

### Decision

- Require agents to identify a separate documentation repository and target
  repository before acting.
- Apply implementation, branch, pull-request, test, and release instructions
  only to the repository they name, without mirroring the target's branch
  structure into the documentation repository.
- Keep project-specific repository names and workflows in selected project
  documentation while global configuration remains project-neutral.
- Publish global instructions version 3.3.0.

### Expected effect

Independent documentation repositories retain their own simple workflow,
project-specific implementation policy stays with the project it describes,
and global Codex guidance prevents scope transfer without imposing one
project's branch model everywhere.

## 2026-08-20 - Fail-closed instruction-file ownership

### Problem

An agent could follow a local instruction overlay yet still write a local
workflow policy into a public repository instruction file. Reading the
instruction chain alone did not force the agent to identify the target's scope
and owner before editing it.

### Decision

- Before editing `AGENTS.md` or `CLAUDE.md`, require classification of the
  target as global configuration, public repository guidance, or a local
  overlay.
- Require commentary to name the exact target, owner, and governing instruction
  before writing, then route the change to that owner.
- Require explicit authorization naming a public repository instruction file
  before changing it.
- Publish global instructions version 3.2.0.

### Expected effect

Instruction-file edits fail closed at the ownership boundary, local workflow
policy stays with its established local owner, and public repository guidance
changes only when the user deliberately authorizes that exact surface.

## 2026-08-19 - Repository-local project documentation root

### Problem

Codex discovers project instructions only from the repository root down to the
current working directory. A session started at the root therefore cannot use a
documentation index nested under `docs`, while choosing between multiple
documentation directories by their mere presence creates ambiguous authority.

### Decision

- Resolve one documentation root for status, planning, decision, and
  architecture questions from the local Git setting `codex.docs-root`, with
  `docs` as the implicit default.
- Accept only existing repository-relative directories that resolve within the
  repository.
- Treat the selected `AGENTS.md` as a documentation index without replacing the
  normal Codex instruction chain.
- Publish global instructions version 3.1.0.

### Expected effect

Repositories keep a conventional `docs` default, local clones can select a
private documentation root without changing tracked files, and maintainer-owned
instructions remain distinct from the selected documentation context.

## 2026-08-13 - Repository-owned GitHub label setup

### Problem

The tracker adapters named triage and Wayfinder labels without a repository
command to verify or provision them, and the documented external-PR query used
a GitHub CLI field unsupported by the installed command.

### Decision

- Add an explicit, check-only-by-default label setup command with offline unit
  tests and an approval-gated `--apply` mode.
- Create only labels with approved metadata and never overwrite an existing
  same-name label.
- Discover external pull requests through paginated REST data and inspect each
  selected pull request with `gh pr view --comments`.

### Expected effect

Repository-local tracker adapters can be verified reproducibly before use,
label creation remains idempotent and reviewable, and external pull-request
triage uses fields provided by GitHub's REST response.

## 2026-08-13 - Current instruction and skill authority

### Problem

An orphaned nested instruction file and transition-era wording still described
deleted configuration responsibilities. Three surviving skills also carried
scope language about execution machinery unrelated to their current behavior.

### Decision

- Keep durable global preferences in `global/AGENTS.md` and current repository
  development contracts in the root `AGENTS.md`; remove `.codex/AGENTS.md`.
- Describe repository ownership positively and keep optional indexes
  non-authoritative without an activation policy.
- Describe the focused skills directly and publish patch versions for global
  instructions, dead-surface audit, test-quality review, and port by contract.

### Expected effect

Only applicable instruction surfaces remain active, repository scope is clear,
and installed metadata advertises the cleaned skill behavior without reviving
legacy vocabulary through tests.

## 2026-08-13 - Conflict-safe installation preflight

### Problem

Installation classified and changed targets one at a time, so a conflict on a
later target could leave an earlier managed symlink partially retargeted.
Lexically relative manifest sources could also escape the repository through a
symlink.

### Decision

- Preflight every selected target before applying any symlink or backup change.
- Reject manifest sources whose resolved paths are outside the repository.
- Preserve managed retargeting, foreign-conflict protection, forced backups,
  dry runs, pruning, and installed-state convergence.

### Expected effect

Known target conflicts fail without partial installation, installed metadata
still converges on version-only upgrades, and every installed source remains
owned by this repository.

## 2026-08-13 - Global and repository instruction separation

### Problem

The repository root `AGENTS.md` was both the source installed into every Codex
home and the development guide for `codex-config`. Repository paths, issue
policy, and validation rules therefore leaked into unrelated projects, while
work in this repository could load the same content twice.

### Decision

- Install global operating preferences from `global/AGENTS.md` and keep the
  root `AGENTS.md` repository-local.
- Install the ownership helper as `bin/codex-owner` so the global guard does not
  depend on a checkout-specific path.
- Safely retarget a changed feature source when the existing symlink exactly
  matches the source recorded by the previous installed state.
- Publish global instructions version 3.0.0.

### Expected effect

Codex receives project-neutral defaults globally and `codex-config` guidance
only while working in this repository. Existing managed installations upgrade
without weakening conflict protection or requiring `--force`.

## 2026-07-25 - Codex commit attribution

### Problem

Codex-assisted commits were not consistently attributed across repositories.

### Decision

Require commits to include the standard Codex co-author trailer exactly once
when Codex materially contributes, and publish global instructions version
2.0.1.

### Expected effect

Future Codex-assisted commits use consistent GitHub-compatible attribution
without marking human-only commits.

## 2026-07-21 - Native-first restoration candidate

### Problem

The repository had grown into a second planner and agent-execution runtime,
while its independently useful configuration installer and focused guidance
were difficult to separate from that machinery.

### Decision

- Preserve the complete experimental lineages in the following archival
  branches: `archive/batch-runway-master-20260721`,
  `archive/command-owner-redesign-20260721`,
  `archive/batch-runway-rogue-master-20260721`, and the two
  `archive/batch-runway-stash-20260721-*` branches.
- Remove the custom planning, queue, runner, and mandatory worker/reviewer
  system from the restoration candidate.
- Retain the generic installer, ownership inspection, independent skills,
  focused read-only agents, and opt-in notification hook.
- Add generic stale managed-link reporting and safe pruning to support upgrades
  from older installed manifests.

### Expected effect

`codex-config` again has one coherent purpose: install and document personal
Codex configuration without duplicating native Codex orchestration.
