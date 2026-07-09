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

This skill reads executable work only from the current program ledger or current
selected/queued/active batch state. External sources are evidence only when an
existing ledger row points to them. Do not scan external sources to discover new
work. If useful work exists outside the ledger, stop and report that
`add-to-ledger` must ingest it first.

This skill owns the planning decision for one batch: use current state, respect
selected/queued/active work, and produce at most one concrete runway spec.

Requested ledger rows are suitable for direct planning only when the row is
precise enough for one bounded selected dispatch. A row is not suitable when it
mixes evidence gathering, classification, decisions, destructive cleanup,
migration, demotion, or contract narrowing without clear owner, risk, and
acceptance boundaries. In that case, route through
`architecture-program-runway` to split, block, or narrow the scope before any
concrete runway spec is created.

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
never treats external sources as executable work unless the current program
ledger points to them.

This skill owns the user's request to plan one bounded batch. Use
`../planning-state/SKILL.md` for current/validate diagnostics,
`../planning-artifacts/SKILL.md` for Layout v1 locations and vocabulary,
`../architecture-program-runway/SKILL.md` for program selection and dispatch
ownership, and `../batch-runway/SKILL.md` only in `create-spec` mode for the
concrete spec procedure. Stop before implementation. When routing ambiguity
exists, follow `../../docs/skill-routing-contract.md`.

## Stops

- Do not implement any slice.
- Do not create more than one batch spec.
- Do not create new ledger findings from fresh user work text.
- Do not bypass an existing selected dispatch, queued batch, or active runway.
- Do not run project-level integration harnesses unless the spec explicitly
  assigns them.

## Agent-Facing Support

Use `../architecture-program-runway/SKILL.md` for selected-dispatch and queue
mechanics. Use `../batch-runway/SKILL.md` in create-spec mode only as runtime
support for writing exactly one concrete runway behind this command.
