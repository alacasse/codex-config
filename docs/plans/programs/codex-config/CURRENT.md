# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
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
- Active rows: CCFG-2 through CCFG-6, CCFG-9 through CCFG-11, and CCFG-13.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Batch State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-8-ledger-dispatch-rule-dedupe`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Covers: CCFG-8, completed as behavior-neutral skill routing rule dedupe.
  Runtime behavior did not change.

## Next Safe Action

Queued CCFG-13 batch replaces the previous CCFG-11 queue item to handle the
validation-gate root cause exposed by that runway. Execute
`docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md`
before planning or executing CCFG-11 again.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would select successor work, create another dispatch, or create
  another runway without an explicit `plan-batch` request.
- Stop if work would execute the displaced CCFG-11 runway before CCFG-13 is
  handled or explicitly superseded.
- Stop if CCFG-1 closeout text would imply runner extraction, package/runtime
  selection, repository/scaffold creation, adapter implementation, or CCFG-2
  through CCFG-5 work is complete.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
