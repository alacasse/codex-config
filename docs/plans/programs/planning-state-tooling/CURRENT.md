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
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`
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

- Batch: `command-owner-skill-migration`
- Status: completed; PST-26 through PST-29 are closed with user-facing
  command-owner skills, preserved runtime workflow surfaces, narrow
  agent-facing support roles, manifest/catalog alignment, validation, and
  pointer-first closeout evidence.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/runway.md`
- Closeout:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/closeout.md`
- Completed slices:
  `docs/plans/programs/planning-state-tooling/batches/command-owner-skill-migration/completed-slices.md`
- Notes: `add-to-ledger`, `plan-batch`, `work-batch`, and `port-by-contract`
  are the preferred direct user-facing command set. Existing names such as
  `architecture-program-runway`, `batch-runway`, `legacy-removal`,
  `dead-surface-audit`, and `test-quality-review` remain installed as
  agent-facing support/runtime dependencies behind those commands, not as
  preferred direct user commands. Bridge-state routing and stop rules now live
  in `docs/skill-routing-contract.md`; the command-owner migration is
  interface-complete, not architecture-complete.

## Queued Batch

- Batch: `None`
- Status: no successor planning-state-tooling batch is selected.
- Notes: select a successor only when explicitly requested.

## Next Safe Action

No planning-state-tooling successor batch is selected. Choose one only after an
explicit request.

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
