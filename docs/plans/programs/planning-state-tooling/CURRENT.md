# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/closeout.md`
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

- Batch: `planning-state-skill-interface`
- Status: completed; the repo-owned `planning-state` skill now provides the
  safe agent interface for current/validate diagnostics, generated state
  fixtures, target-policy refusal, optional projection reporting, closeout
  evidence, and runner-artifact projection inputs.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-skill-interface/closeout.md`
- Notes: `planning-state` depends on `planning-artifacts`, keeps
  `scripts/planning_state.py` as the command/file boundary, and leaves consumer
  skill rewiring for the later `planning-state-consumer-integration` batch.

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. There is no selected, active, or queued
planning-state-tooling batch. Create or queue
`planning-state-consumer-integration` only when consumer skill rewiring is
requested.

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
