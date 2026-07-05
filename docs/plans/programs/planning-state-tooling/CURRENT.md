# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `planning-state-skill-interface`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/closeout.md`
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
- Update authority: `command`

## Latest Completed Batch

- Batch: `planning-state-sqlite-projection`
- Status: completed; SQLite projection rebuild/report commands are optional,
  delete-safe, policy-checked, and bounded to command/report interfaces.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/closeout.md`
- Notes: `rebuild-projection` writes only an explicit policy-compatible
  database target, `report-projection` answers planning and runner summary
  questions from validated projection rows, and Markdown/JSON state remains
  canonical when no database exists.

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. The queued `planning-state-skill-interface` batch should
execute from
`docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/runway.md`
when implementation work starts.

## Stop Conditions

- Stop if work would implicitly render or rewrite root/program
  `CURRENT.md`, `LEDGER.md`, `dispatch.md`, or `runway.md` from tool state.
- Stop if closeout rendering would write anywhere other than stdout or an
  explicit registered `closeout.md` target path.
- Stop if work would add SQLite or write transition state without an
  explicit state/receipt target.
- Stop if work would choose a durable JSON state or SQLite projection location
  as a generic default instead of resolving project policy.
- Stop if work would add Graphify-specific paths or validation commands to
  generic code instead of using fixture data.
