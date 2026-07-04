# Architecture Program Runner Current State

## Program

- Program slug: `architecture-program-runner`
- Purpose: continue concept-owner and extraction planning for the
  architecture-program runner without replaying archived runway specs.
- Current ledger: `docs/plans/programs/architecture-program-runner/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
- Latest closeout path: `None`
- Run artifact location:
  `docs/plans/programs/architecture-program-runner/architecture-program-runs/`
- Program archive location: `docs/plans/archive/`

## Current Candidate

- Batch: `phase-runner-business-logic-extraction`
- Status: candidate; dispatch has not been selected or written.
- Source contract:
  `docs/plans/phase-runner-business-logic-contract.md`

## Next Safe Action

Create a compact dispatch packet for
`phase-runner-business-logic-extraction` only if this is the requested program.
Then create one co-located Batch Runway spec under:

`docs/plans/programs/architecture-program-runner/batches/phase-runner-business-logic-extraction/`

## Stop Conditions

- Stop if a selected dispatch or active runway appears before creating another
  batch.
- Stop if the requested work belongs to `planning-state-tooling`; use that
  program's `CURRENT.md` instead.
