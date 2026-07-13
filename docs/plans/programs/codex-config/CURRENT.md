# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/closeout.md`
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
- Projection usage: `caller-directed`
- Projection rebuild authority: `command`
- Update authority: `command`

## Open Ledger

- Ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Open ledger rows: CCFG-2 through CCFG-6, CCFG-9 through CCFG-11, and
  CCFG-20 through CCFG-29.
- Pending ledger row: CCFG-19. It is controlled by the queued design-only
  dispatch and runway below.
- Closed ledger row: CCFG-18. Candidate lineage, strict transition, isolated
  generation install, fixture isolation, quiescence, and rollback are complete.
- Accepted command-owner redesign snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Live redesign decisions:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-bootstrap-decisions.md`
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Batch State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch:
  `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/dispatch.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-18-candidate-generation`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/closeout.md`

## Next Safe Action

Execute the queued
`docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md`
through an explicit `work-batch` request. CCFG-19 is a strict cross-checkout,
design-only decision batch. Do not select, dispatch, queue, refresh, or prepare
CCFG-20 or any other successor during execution or same-batch closeout.

## Stop Conditions

- Stop if work treats closed CCFG-18 or its completed runway as active work.
- Stop if planning weakens strict `cross-checkout-context/v1` or treats
  pre-creation verification as strict identity.
- Stop if any default stable-home installed link resolves to the redesign branch
  or candidate clone.
- Stop if selected dispatch or active runway appears alongside the queued
  CCFG-19 runway.
- Stop if a different queued batch appears or CCFG-19's dispatch/runway lineage
  does not match the canonical ledger.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
- Stop if work would repeat command-owner redesign intake or create new
  identities instead of amending CCFG-18 through CCFG-29.
- Stop if CCFG-19 execution would implement schemas, `ledger-store`, planning
  transactions, runner changes, ownership transfer, or other CCFG-20 through
  CCFG-29 work.
- Stop if work would select successor work, create another dispatch, or create
  another runway during CCFG-19 execution or closeout.
- Stop if work would select from archived APR/PST ledgers instead of the canonical
  codex-config ledger.
- Stop if work would execute the displaced CCFG-11 runway without replanning.
- Stop if work would copy archived history into the active ledger row-by-row.
- Stop if a generic reusable skill receives project-specific paths, commands,
  caches, or planning layouts.
- Stop if CCFG-19 closeout selects or prepares any successor dispatch or runway.
