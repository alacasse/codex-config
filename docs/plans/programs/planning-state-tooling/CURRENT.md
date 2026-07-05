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
  `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/closeout.md`
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

- Batch: `planning-state-consumer-integration`
- Status: completed; Batch Runway, Architecture Program Runway, and Legacy
  Removal now consume the shared `planning-state` diagnostic interface before
  Layout v1 ledger or active-state pickup while preserving each workflow's
  semantic ownership.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-consumer-integration/closeout.md`
- Notes: consumer features now depend on both `planning-artifacts` for placement
  conventions and `planning-state` for operational diagnostics. PST-12 and
  PST-13 are closed with completed-slice, validation, review, and closeout
  evidence.

## Next Safe Action

No planning-state-tooling batch is selected or queued. Use the ledger before
creating any new batch.

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
