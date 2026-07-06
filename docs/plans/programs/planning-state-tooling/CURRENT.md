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
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/closeout.md`
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

- Batch: `batch-runway-create-spec-output-contract`
- Status: completed; PST-18 is closed with tightened Batch Runway create-spec
  output guidance, focused regression coverage, bounded active/future runway
  scan evidence, final validation pointers, and pointer-first closeout evidence.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/batch-runway-create-spec-output-contract/completed-slices.md`
- Notes: Batch Runway create-spec guidance and regression coverage now keep
  session-local mode history out of durable execution `Overrides`. The bounded
  scan left only closed historical runway residue unchanged by design.

## Queued Batch

- Batch: `None`.
- Notes: PST-19 Pending-status modeling remains the next candidate, but it is
  not selected or queued.

## Next Safe Action

No planning-state-tooling batch is currently queued. PST-19 remains the next
candidate; create a new dispatch/runway for it only when explicitly asked to
select the next planning-state-tooling batch.

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
