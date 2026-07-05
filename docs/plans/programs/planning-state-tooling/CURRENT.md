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
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/closeout.md`
- Run artifact location: `None selected`
- Program archive location: `docs/plans/archive/`

## Latest Completed Batch

- Batch: `planning-state-migration-pilot`
- Status: completed; migration bootstrap generation and migrated-fixture
  validation are available while Markdown remains the human-readable planning
  surface.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-migration-pilot/closeout.md`
- Notes: `bootstrap-state` can generate v1 companion JSON state from Layout v1
  Markdown, and `current`/`validate --state-file` can reject migrated fixture
  drift before runner or reporting layers consume it.

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. PST-5 is closed with validation, review, and closeout
evidence. The next safe planning action is to create a concrete spec for
deferred PST-6 SQLite projection only if the user requests more planning-state
work.

## Stop Conditions

- Stop if work would implicitly render or rewrite root/program
  `CURRENT.md`, `LEDGER.md`, `dispatch.md`, or `runway.md` from tool state.
- Stop if closeout rendering would write anywhere other than stdout or an
  explicit registered `closeout.md` target path.
- Stop if work would add SQLite or write transition state without an
  explicit state/receipt target.
- Stop if work would add Graphify-specific paths or validation commands to
  generic code instead of using fixture data.
