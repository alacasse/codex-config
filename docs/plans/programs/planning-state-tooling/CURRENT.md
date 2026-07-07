# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`
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

- Batch: `workflow-skill-interface-deepening`
- Status: completed; PST-22 through PST-25 are closed with single-owner pickup
  guidance, layout-vs-pickup separation, program-vs-runway ledger boundaries,
  discovery-skill role boundaries, feature metadata alignment, validation, and
  pointer-first closeout evidence.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/workflow-skill-interface-deepening/completed-slices.md`
- Notes: Reusable workflow skills now route Layout v1 pickup through Planning
  State, keep artifact placement in Planning Artifacts, split program ledgers
  from concrete runway ledgers, and prevent discovery skills from becoming
  parallel planning systems by default.

## Queued Batch

- Batch: `command-owner-skill-migration`
- Status: queued; PST-26 through PST-29 are cut for copy-first migration to
  human-facing command-owner skills.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md`
- Notes: execute only when the user asks to work the queued batch.

## Next Safe Action

Run the queued `command-owner-skill-migration` batch only if asked to work the
batch. Do not select a successor batch until this queued batch closes or is
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
