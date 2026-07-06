# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/closeout.md`
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

- Batch: `planning-state-projection-consumers`
- Status: completed; PST-16 and PST-17 are closed with completed consumer
  routing updates, focused regression coverage, final validation, clean review,
  and pointer-first closeout evidence.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-consumers/completed-slices.md`
- Notes: Batch Runway, Architecture Program Runway, and Legacy Removal now route
  supported history/reporting questions through policy-compatible projection
  reports before broad historical scans while preserving their own semantic
  decisions.

## Queued Batch

- Batch: `batch-runway-create-spec-output-contract`
- Status: queued; covers PST-18 only.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md`
- Notes: This batch fixes the Batch Runway create-spec output contract so
  session-local mode history does not appear in durable execution `Overrides`.
  PST-19 Pending-status modeling remains a separate candidate.

## Next Safe Action

Execute the queued
`docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md`
batch if asked to work on the planning-state-tooling batch. Do not select
another planning-state-tooling batch until this queued batch closes or is
explicitly superseded.

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
