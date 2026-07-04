# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/dispatch.md`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
- Latest closeout path: `None`
- Run artifact location: `None selected`
- Program archive location: `docs/plans/archive/`

## Selected Batch

- Batch: `planning-state-readonly-core`
- Status: selected for Batch Runway spec creation; execution has not started.
- Runway path to create:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md`

## Next Safe Action

Create the `planning-state-readonly-core` Batch Runway spec from the selected
dispatch. Do not implement code during spec creation.

## Stop Conditions

- Stop if the batch would write canonical state, rendered Markdown, or SQLite.
- Stop if the batch would add Graphify-specific paths or validation commands to
  generic code instead of using fixture data.
