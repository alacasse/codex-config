# Changelog

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
