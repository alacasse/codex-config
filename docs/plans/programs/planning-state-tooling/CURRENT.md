# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/closeout.md`
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

- Batch: `planning-state-project-policy`
- Status: completed; project-owned state/projection policy is explicit before
  durable JSON or SQLite targets are selected.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-project-policy/closeout.md`
- Notes: `current`/`validate` report project policy, write/preflight commands
  enforce state-file and projection target policy, and codex-config committed
  docs plus ignored-local overlay examples are documented without making either
  a universal default.

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. The next safe implementation action is to execute the
queued SQLite projection runway, which must consume resolved project policy
before choosing any durable state or projection target:

`docs/plans/programs/planning-state-tooling/batches/planning-state-sqlite-projection/runway.md`

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
