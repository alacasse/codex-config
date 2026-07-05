# Planning-State Tooling Current State

## Program

- Program slug: `planning-state-tooling`
- Purpose: add tool-owned planning-state diagnostics and later state
  transitions while keeping Markdown and JSON canonical.
- Current ledger: `docs/plans/programs/planning-state-tooling/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `planning-state-migration-pilot`
- Latest closeout path:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/closeout.md`
- Run artifact location: `None selected`
- Program archive location: `docs/plans/archive/`

## Latest Completed Batch

- Batch: `planning-state-closeout-contract`
- Status: completed; bounded closeout evidence-index validation and rendering
  are available.
- Dispatch:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/dispatch.md`
- Runway:
  `docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/runway.md`
- Closeout contract: `closeout.md` is a bounded pointer-first evidence index.
  It should point to commits, completed slices, validation, review, receipts
  when present, obligations, and cleanup residue evidence instead of embedding
  transcripts or long logs.

## Next Safe Action

Use `python scripts/planning_state.py current --root docs/plans` and
`python scripts/planning_state.py validate --root docs/plans` before broad
planning tree scans. When the user asks for the next planning-state specs
batch, create one concrete `planning-state-migration-pilot` dispatch and
runway for PST-5, then stop before implementation.

## Stop Conditions

- Stop if work would implicitly render or rewrite root/program
  `CURRENT.md`, `LEDGER.md`, `dispatch.md`, or `runway.md` from tool state.
- Stop if closeout rendering would write anywhere other than stdout or an
  explicit registered `closeout.md` target path.
- Stop if work would add SQLite or write transition state without an
  explicit state/receipt target.
- Stop if work would add Graphify-specific paths or validation commands to
  generic code instead of using fixture data.
