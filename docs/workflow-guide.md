# Workflow Guide

## Purpose

This guide explains how external engineering skills and codex-config
command-owner skills work together without creating multiple executable backlog
sources.

## Canonical Pipeline

```text
external shaping / candidate source
-> add-to-ledger
-> program ledger
-> plan-batch
-> dispatch/runway
-> work-batch
-> closeout / follow-up ingestion
```

## Skill Families

### External Engineering / Shaping Skills

External engineering skills may clarify intent, research options, model a
domain, write ADRs, produce specs or tickets, or review code. Their output is
candidate work or evidence. It does not define executable backlog until selected
work is ingested into the program ledger.

Examples from `skills-lock.json` include:

- `grill-with-docs`
- `domain-modeling`
- `research`
- `to-spec`
- `to-tickets`
- `triage`
- `wayfinder`
- `code-review`

### Codex-Config Command-Owner Skills

- `add-to-ledger`: the explicit ingestion boundary for selected candidate work.
- `plan-batch`: consumes existing ledger work and creates one dispatch/runway.
- `work-batch`: executes the current queued or active runway.
- `port-by-contract`: extracts behavior contracts before a rewrite or port; it
  is not a general cleanup shortcut.

### Agent-Facing Support Skills

These skills support command-owner workflows behind the scenes. They are not
the normal direct commands for the ledger-driven workflow.

- `planning-state`
- `planning-artifacts`
- `architecture-program-runway`
- `batch-runway`
- `legacy-removal`
- `dead-surface-audit`
- `test-quality-review`

## Common Workflows

### Vague idea to executable work

1. Use `grill-with-docs`, `domain-modeling`, `research`, or `wayfinder` to
   clarify the idea.
2. Use `add-to-ledger` to ingest selected work.
3. Use `plan-batch`.
4. Use `work-batch`.

### GitHub tickets to ledger

1. Ask `add-to-ledger` to ingest named GitHub tickets.
2. Preserve issue number, URL, title, labels/status, and evidence pointers.
3. Then `plan-batch` may consume the ledger rows.

### ADR or CONTEXT follow-up to execution

1. Use the external skill or document as evidence.
2. Ingest selected follow-up through `add-to-ledger`.
3. Plan and execute through the ledger/runway path.

### Review finding to follow-up

1. Use `code-review` or `test-quality-review` for evidence.
2. Use `add-to-ledger` for follow-up work that should become executable
   backlog.

## Rules

- The program ledger is the only normal executable backlog source for
  `plan-batch`; in this repo it is
  `docs/plans/programs/codex-config/LEDGER.md`.
- External skills and GitHub issues are candidate/evidence sources until
  ingested.
- `plan-batch` must not discover new work by scanning external sources.
- `work-batch` must not select new work.
- If useful work exists outside the ledger, use `add-to-ledger` first.

## Anti-Patterns

- Running `plan-batch` and letting it search GitHub, ADRs, CONTEXT.md, specs,
  or tickets for work.
- Treating Matt Pocock tickets as executable backlog before ingestion.
- Having both GitHub issues and the program ledger act as active backlogs.
- Using `work-batch` to reselect or replan work.
- Using `port-by-contract` as a general refactor shortcut.

## Related Contracts

- [Skill Routing Contract](skill-routing-contract.md)
- [README](../README.md)
- [add-to-ledger](../skills/add-to-ledger/SKILL.md)
- [plan-batch](../skills/plan-batch/SKILL.md)
- [work-batch](../skills/work-batch/SKILL.md)
- [port-by-contract](../skills/port-by-contract/SKILL.md)
