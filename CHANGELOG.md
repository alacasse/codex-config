# Changelog

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
  focused read-only agents, rules, and opt-in notification hook.
- Add generic stale managed-link reporting and safe pruning to support upgrades
  from older installed manifests.

### Expected effect

`codex-config` again has one coherent purpose: install and document personal
Codex configuration without duplicating native Codex orchestration.
