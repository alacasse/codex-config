# Skill Routing Contract

This document defines how agents route human workflow intent to command-owner,
runtime, and support skills during the command-owner skill migration.

Command-owner skills own human intent, semantic workflow decisions, mutations,
and stop conditions. Runtime and support skills provide execution mechanics,
diagnostics, layout rules, closeout reconciliation, review support, evidence
classification, or validation guidance without becoming alternate owners.

## Owner Split

Keep human-facing command decisions separate from runtime mechanics:

- `add-to-ledger`, `plan-batch`, and `work-batch` own the user-visible command
  routes and stop points.
- `add-to-ledger` owns fresh ledger and external-source intake.
- `planning-state` owns current/validate ordering, target-policy checks, and
  projection routing.
- `planning-artifacts` owns Planning Artifact Layout v1 placement, naming,
  active-state file shape, batch directory, archive, and state vocabulary.
- `plan-batch` owns one-finding selection, proportional scope, independent
  planning review, dispatch/runway creation, approvals, validation-profile
  selection, and the DEC-038 queue transaction.
- `architecture-program-runway` owns evidence-bound same-batch closeout
  reconciliation only; it has no planning or queue authority.
- `batch-runway` owns execution of an already queued or active runway: slice
  ledgers, validation/review loops, recovery, completed-slice archives,
  finalization, and commit receipt mechanics.
- `legacy-removal` owns legacy evidence and classification only. Its batch
  candidates and dispatch handoffs are evidence for public `plan-batch`, never
  program, queue, dispatch, runway, lifecycle, execution, or closeout state.

Command-owner skills may reference those runtime/support owners, but should not
duplicate their procedure details.

## Skill Audiences

- **Human-facing command-owner skill**: the primary skill that owns the user's
  workflow intent, routing choice, and stopping point.
- **Runtime workflow skill**: an agent-facing skill that owns a detailed
  procedure after a command-owner skill selects it.
- **Agent-facing support skill**: a narrow diagnostic, layout, review,
  evidence, or validation helper used inside another workflow.
- **Default workflow obligation**: a rule normal implementation or review work
  must enforce without requiring a separate user command.

## Command Input Contract

`add-to-ledger` is the normal command-owner skill that turns fresh
user-provided work/finding text into a new or updated ledger finding.

`plan-batch` consumes existing ledger state. It owns the human "create the next
specs batch" decision: use an existing selected dispatch, report queued or
active runway state without replacing it, or select bounded work from the
current program ledger when nothing is selected. It may accept user preference
about which existing finding to prioritize, but it must not silently create new
ledger findings. If no suitable ledger finding exists, stop and report that
`add-to-ledger` must run first.

`work-batch` consumes the current queued or active runway. It must not create
new ledger findings, select new ledger work, or create a new runway unless
explicit recovery instructions require replanning. After concrete closeout
evidence exists, it may reconcile same-batch program state through
`architecture-program-runway closeout-runway`, but it must stop before
successor selection.

## Executable Work Source

The program ledger is the only normal executable backlog source for
`plan-batch`. External sources are candidate work or evidence until
`add-to-ledger` records selected work in the ledger. `plan-batch` consumes
ledger state; it must not discover new work by scanning external sources.

For this repository, the active program ledger is
`docs/plans/programs/codex-config/LEDGER.md`.

## Routing Table

| User command/input | Primary skill | Input source | Output | Runtime/support skills |
| --- | --- | --- | --- | --- |
| Capture fresh work/finding text, review results, bugs, cleanup needs, or work requests | `add-to-ledger` | User-provided work/finding text plus project planning state | New or updated ledger finding | `planning-contracts` atomic store mechanism |
| Plan the next bounded batch/spec from existing ledger work | `plan-batch` | Existing ledger state, selected dispatch, or user preference pointing at existing ledger work | One independently reviewed dispatch/runway and DEC-038 queue result; no implementation | `planning-state`, `planning-artifacts`, planning contracts, and registered planning roles |
| Execute the current queued or active batch runway | `work-batch` | Current queued or active runway state | Executed slices, validation/review evidence, commits, closeout evidence, and same-batch program reconciliation | `planning-state`, `planning-artifacts`, then `batch-runway` in `execute-spec` mode, then `architecture-program-runway` in `closeout-runway` mode for the completed batch only |
| Extract behavior contracts before a rewrite, migration, or port | `port-by-contract` | Current implementation and durable domain context | Implementation-neutral contract artifacts and planning evidence | Public `plan-batch` only after contract artifacts exist |

## Conflict Rule

When a command-owner skill and a runtime/support skill both appear applicable,
the command owner retains the semantic decision and mutation. Support may be
used only for its declared evidence, layout, execution, or closeout boundary.

## Stop Rule

If the agent cannot name the user intent, primary command-owner skill,
runtime/support skills, and stopping point, it must stop before editing files.

## Compatibility Label Rule

The architecture runner temporarily preserves serialized `select-dispatch`
and `create-spec` labels. They do not restore APR or Batch Runway planning:
the first invokes public `plan-batch` once, and the second only observes and
advances the completed result. CCFG-27 owns their migration/removal decision;
CCFG-29 is the final cleanup deadline if they remain.

## Anti-Patterns

- Invoking `batch-runway` directly for a human "work on the batch" request
  unless the command-owner route has selected it.
- Reselecting a program batch during `work-batch`.
- Treating `work-batch` same-batch closeout reconciliation as permission to
  select, dispatch, refresh, create, or prepare successor work.
- Skipping `architecture-program-runway closeout-runway` after concrete
  `work-batch` closeout and leaving stale `CURRENT.md`, `LEDGER.md`, or queue
  state for the completed batch.
- Using `port-by-contract` as a general skill rewrite excuse before contracts
  exist.
- Preserving old runtime names forever by accident.
- Treating `legacy-removal` evidence or handoff material as selected work or
  active planning state.
- Marking the migration complete without stating whether it is
  interface-complete or architecture-complete.
