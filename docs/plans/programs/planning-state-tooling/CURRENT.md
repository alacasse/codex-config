# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`
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

- Batch: `planning-state-finding-pending-status`
- Status: completed; PST-19 is closed with reusable Pending finding lifecycle
  vocabulary, update-rule regression coverage, validation, clean review, feature
  metadata alignment, and pointer-first closeout evidence.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-finding-pending-status/completed-slices.md`
- Notes: Architecture Program Runway now distinguishes `Pending` findings from
  raw `Open` intake and requires explicit closeout, amendment, supersession,
  abandonment, split, or follow-up evidence for Pending scope changes.

## Queued Batch

- Batch: `planning-state-projection-language-and-migration`.
- Status: queued; PST-20 and PST-21 are Pending under the co-located dispatch
  and runway artifacts.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`
- Notes: this batch clarifies projection-backed reporting language and
  adoption/migration guidance while preserving Markdown/JSON as canonical and
  SQLite as command-only reporting projection.

## Next Safe Action

Execute or hand off
`docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`
when asked to work on the planning-state-tooling batch. Do not select another
planning-state-tooling batch while this runway is queued.

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
