---
name: plan-batch
description: Select bounded ledger work when needed and write one concrete batch runway spec without executing it.
---

# Plan Batch

Use this skill when the user asks to create the next specs batch, plan a batch,
turn selected ledger work into a runway, or prepare implementation slices.

This skill consumes existing ledger state/work. It may accept a user preference
pointing at an existing finding, selected dispatch, queued batch, or active
runway, but it must not silently create new ledger findings from fresh user work
text. If no suitable ledger finding exists, stop and report that
`add-to-ledger` must run first.

This skill reads executable work only from the current program ledger, selected
dispatch, queued batch, or active runway. External specs, ADRs, GitHub issues,
issue tracker tickets, CONTEXT.md updates, archived plans, chat transcripts,
review notes, and external engineering-skill outputs are evidence only when an
existing ledger row points to them.

Do not scan external sources to discover new work. If useful work exists
outside the ledger, stop and report that `add-to-ledger` must ingest it first.

This skill owns the planning decision for one batch: inspect current planning
state, use the selected dispatch when one exists, select bounded ledger work
only when none is already selected, and write one concrete runway spec with
clear scope, validation, allowed files, and slice boundaries.

## Command Contract

`plan-batch` is the human-facing command contract for "create the next specs
batch". It owns the caller-visible decisions, ledger-source rule, one-spec
output rule, and stop-before-implementation boundary. Runtime mechanics remain
behind the support skills named below.

Use this state table when answering the command:

| Current state | `plan-batch` decision | Output |
|---|---|---|
| No selected work exists | Select bounded work from the current program ledger through `architecture-program-runway`. | One selected dispatch, then one concrete runway spec. |
| Selected dispatch exists | Do not select different work. Use that dispatch. | One concrete runway spec for the selected dispatch. |
| Queued runway exists | Do not create another spec or replace the queue. | Report the queued runway and stop before implementation. |
| Active runway exists | Do not create another spec or execute it. | Report the active runway and stop before implementation. |
| User requests an existing ledger row | Use the requested row only when it exists in the current program ledger and is suitable for bounded planning. | One selected dispatch, then one concrete runway spec. |
| No suitable ledger row exists | Do not infer work from external text or sources. | Stop and report that `add-to-ledger` must ingest the work first. |

The command result is at most one concrete batch runway spec. It never begins
slice implementation, never creates new findings from fresh request text, and
never treats external specs, ADRs, GitHub issues, archived plans, review notes,
or external engineering-skill outputs as executable work unless the current
program ledger points to them.

This skill owns the user's request to plan one bounded batch. Use
`../planning-state/SKILL.md` first for current state,
`../architecture-program-runway/SKILL.md` only for program selection and
dispatch ownership, and `../batch-runway/SKILL.md` only in `create-spec` mode
for the concrete spec procedure. Stop before implementation. When routing
ambiguity exists, follow `../../docs/skill-routing-contract.md`.

Before consuming Layout v1 planning state, use `../planning-state/SKILL.md` to
run the current and validate hot path. Use `../planning-artifacts/SKILL.md`
when choosing planning locations or interpreting Layout v1 artifacts.

## Stops

- Do not implement any slice.
- Do not create more than one batch spec.
- Do not create new ledger findings from fresh user work text.
- Do not bypass an existing selected dispatch, queued batch, or active runway.
- Do not run project-level integration harnesses unless the spec explicitly
  assigns them.

## Agent-Facing Support

Use `../architecture-program-runway/SKILL.md` for selected-dispatch mechanics
when ledger work still needs grouping or queue-state updates. Use
`../batch-runway/SKILL.md` in create-spec mode only as runtime support for
writing exactly one concrete runway behind this command.
