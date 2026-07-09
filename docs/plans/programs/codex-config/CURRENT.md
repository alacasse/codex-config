# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/closeout.md`
- Run artifact location: `None selected`
- Program archive location: `docs/plans/archive/`

## Project State Policy

- Planning root: `docs/plans/`
- Run artifact root: `None`
- Output root: `None`
- State file policy: `generated-only`
- State file path: `None`
- Projection policy: `generated-only`
- Projection path: `None`
- Projection usage: `caller-directed`
- Projection rebuild authority: `command`
- Update authority: `command`

## Active Ledger

- Ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Active rows: CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Batch State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch: `None`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-15-vague-ledger-row-splitting`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/closeout.md`
- Covers: CCFG-15, completed as split, block, or narrow-scope guidance for
  vague or mixed-risk ledger rows before selected dispatch and concrete runway
  creation, with focused text-contract tests and CCFG-11 planning evidence.
  Runtime behavior did not change.

## Next Safe Action

No batch is currently selected, queued, or active. A future explicit
`plan-batch` request can select one bounded batch from the canonical
codex-config ledger.

CCFG-11 remains open, but its displaced runway is superseded planning evidence;
do not execute it as active state without a future regenerated or amended runway
that includes validation-command status classes, batch kind, slice risk
classes, approval gates where required, and a CCFG-15 split, block, or
narrow-scope decision before selected dispatch and concrete runway creation.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would select successor work, create another dispatch, or create
  another runway without an explicit future `plan-batch` request.
- Stop if work would execute the displaced CCFG-11 runway as active state
  without a future regenerated or amended runway.
- Stop if work would regenerate or execute CCFG-11 without validation-command
  status classes, batch kind, slice risk classes, and approval gates where
  required.
- Stop if work would plan CCFG-11 from the displaced artifact without first
  splitting, blocking, or narrowing its vague mixed-risk scope under the
  CCFG-15 guard.
- Stop if CCFG-1 closeout text would imply runner extraction, package/runtime
  selection, repository/scaffold creation, adapter implementation, or CCFG-2
  through CCFG-5 work is complete.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
