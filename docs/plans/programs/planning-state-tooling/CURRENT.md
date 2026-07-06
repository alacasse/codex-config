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
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/closeout.md`
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

- Batch: `planning-state-projection-language-and-migration`
- Status: completed; PST-20 and PST-21 are closed with projection-reporting
  wording tightened across reusable workflow skills, reusable adoption guidance
  for Layout v1 roots, fixture coverage, feature metadata alignment, validation,
  clean review evidence for implementation slices, and pointer-first closeout
  evidence.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-projection-language-and-migration/completed-slices.md`
- Notes: Projection-backed reporting is now described as the policy-gated
  normal route for supported history/reporting questions while `current` and
  `validate` remain SQLite-independent.

## Queued Batch

- Batch: `None`
- Status: no planning-state-tooling batch is currently selected, queued, or
  active.
- Notes: do not select a successor batch unless explicitly asked.

## Next Safe Action

No planning-state-tooling batch is selected or queued. If asked for new
planning-state-tooling work, start from this `CURRENT.md` and
`docs/plans/programs/planning-state-tooling/LEDGER.md` before creating exactly
one successor batch.

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
