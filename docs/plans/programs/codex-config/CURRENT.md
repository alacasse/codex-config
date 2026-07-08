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
- Open/candidate rows: CCFG-1 through CCFG-11.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Queued Batch

- Batch: `None`
- Status: no successor batch is selected.
- Notes: do not create a dispatch or runway unless explicitly requested.

## Next Safe Action

Use `docs/plans/programs/codex-config/LEDGER.md` as the only active program
ledger. Select at most one `CCFG-N` row for a future batch only after an
explicit request.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would create a dispatch or runway without an explicit planning
  request.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
