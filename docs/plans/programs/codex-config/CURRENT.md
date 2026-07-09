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
- Active rows: CCFG-2 through CCFG-6 and CCFG-8 through CCFG-11.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Batch State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch: `None`
- Latest closed batch: `ccfg-8-ledger-dispatch-rule-dedupe`
- Latest closed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/dispatch.md`
- Latest closed runway:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/runway.md`
- Latest closed closeout:
  `docs/plans/programs/codex-config/batches/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest closed result: abandoned before execution; CCFG-8 remains backlog.
- Latest completed batch: `ccfg-1-runner-contract-fixtures`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/closeout.md`
- Covers: CCFG-1, completed as contract/fixture preparation only. Closeout did
  not authorize code moves, repository creation, package scaffolding, hidden
  `planning_state.py` dependencies, archived-ledger archaeology, or extraction
  implementation.

## Next Safe Action

No batch is selected, queued, or active. Stop until the user explicitly asks for
`plan-batch` to select successor work from the active codex-config ledger. Do
not infer new work from archived APR/PST ledgers, CCFG-1 closeout evidence, or
the abandoned CCFG-8 dispatch/runway pair.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would select successor work, create another dispatch, or create
  another runway without an explicit `plan-batch` request.
- Stop if CCFG-1 closeout text would imply runner extraction, package/runtime
  selection, repository/scaffold creation, adapter implementation, or CCFG-2
  through CCFG-5 work is complete.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
