# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
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

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. When the user asks for the next planning-state batch,
create or select a new Batch Runway spec for `planning-state-write-transitions`
rather than implementing write behavior directly.

## Stop Conditions

- Stop if the batch would write canonical state, rendered Markdown, or SQLite.
- Stop if the batch would add Graphify-specific paths or validation commands to
  generic code instead of using fixture data.
