# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/runway.md`
- Latest closeout path: `None`
- Run artifact location: `None selected`
- Program archive location: `docs/plans/archive/`

## Latest Completed Batch

- Batch: `planning-state-readonly-core`
- Status: completed; read-only diagnostics are available.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md`

## Queued Batch

- Batch: `planning-state-write-transitions`
- Status: queued; implementation has not started.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-write-transitions/runway.md`

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. When the user asks to work on the planning-state batch,
execute the queued `planning-state-write-transitions` runway from its first
pending ledger row.

## Stop Conditions

- Stop if the batch would render or rewrite live planning Markdown from tool
  state, add SQLite, or write transition state without an explicit
  state/receipt target.
- Stop if the batch would add Graphify-specific paths or validation commands to
  generic code instead of using fixture data.
