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
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/closeout.md`
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

- Batch: `planning-state-projection-routing`
- Status: completed; planning-state diagnostics now expose projection usage and
  rebuild-authority routing for history/reporting questions while preserving
  SQLite-independent `current` and `validate` active-state checks.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-routing/closeout.md`
- Notes: PST-14 and PST-15 are closed with completed commits, validation,
  review, and projection smoke evidence. PST-16 and PST-17 remain open for the
  next candidate batch, `planning-state-projection-consumers`.

## Next Safe Action

Use `planning-state-projection-consumers` as the next candidate only when asked
to create the next planning-state-tooling batch. Do not create it as part of the
projection-routing closeout.

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
