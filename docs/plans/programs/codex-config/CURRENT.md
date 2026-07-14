# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/closeout.md`
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
  CCFG-21 through CCFG-29.
- Pending ledger row: CCFG-30.
- Closed ledger rows: CCFG-18 through CCFG-20. CCFG-20 implements the accepted
  `skill-contract/v1` schema, deterministic validators, explicit fixture
  catalogs, and migration guards without installing or migrating current
  skills.
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
  `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/dispatch.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-20-skill-contract-schema`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/closeout.md`

## Next Safe Action

Execute only
`docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md`
through `work-batch`. Keep CCFG-21 through CCFG-29 and all older open rows
unselected, preserve exact strict handoff validation, and stop after CCFG-30
same-batch closeout without preparing a successor.

## Stop Conditions

- Stop if work treats closed CCFG-18 or its completed runway as active work.
- Stop if planning weakens strict `cross-checkout-context/v1` or treats
  pre-creation verification as strict identity.
- Stop if any default stable-home installed link resolves to the redesign branch
  or candidate clone.
- Stop if selected dispatch, active runway, or queued batch appears without a
  new explicit `plan-batch` request.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
- Stop if work would repeat command-owner redesign intake or create new
  identities instead of amending CCFG-18 through CCFG-29.
- Stop if work treats CCFG-19 as active after its completed closeout.
- Stop if work treats CCFG-20 as active after its completed closeout.
- Stop if work would select from archived APR/PST ledgers instead of the canonical
  codex-config ledger.
- Stop if work would execute the displaced CCFG-11 runway without replanning.
- Stop if work would copy archived history into the active ledger row-by-row.
- Stop if a generic reusable skill receives project-specific paths, commands,
  caches, or planning layouts.
- Stop if CCFG-19 closeout selects or prepares any successor dispatch or runway.
- Stop if CCFG-20 closeout selects or prepares any successor dispatch or runway.
- Stop if CCFG-30 execution targets the redesign candidate, weakens exact strict
  handoff validation, or lets helper refresh preparation decide compatibility.
- Stop if CCFG-30 closeout selects or prepares any successor dispatch or runway.
