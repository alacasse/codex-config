# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`
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
- Active rows: CCFG-1 through CCFG-12.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Queued Batch

- Batch: `ccfg-12-plan-batch-deepening`
- Status: queued; selected from CCFG-12 by explicit user request.
- Dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/dispatch.md`
- Runway:
  `docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md`
- Notes: execute only with `work-batch`; do not select another batch while this
  runway is queued.

## Next Safe Action

Use `work-batch` to execute the queued
`docs/plans/programs/codex-config/batches/ccfg-12-plan-batch-deepening/runway.md`
when explicitly requested. Do not select another `CCFG-N` row while this runway
is queued.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would create another dispatch or runway while
  `ccfg-12-plan-batch-deepening` is queued.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
