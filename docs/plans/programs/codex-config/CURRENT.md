# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-7-batch-runway-hot-path-pruning/closeout.md`
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
- Active rows: CCFG-1 through CCFG-6 and CCFG-8 through CCFG-11.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Queued Batch

- Batch: `ccfg-1-runner-contract-fixtures`
- Dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/dispatch.md`
- Runway:
  `docs/plans/programs/codex-config/batches/ccfg-1-runner-contract-fixtures/runway.md`
- Covers: CCFG-1

## Next Safe Action

Run `work-batch` only when explicitly requested to execute the queued CCFG-1
runway. Do not select another batch, create another dispatch/runway, or infer
new work from archived APR/PST ledgers while this queued runway exists.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would create another dispatch or runway without an explicit
  `plan-batch` request.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
