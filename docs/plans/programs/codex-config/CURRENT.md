# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID: `None`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/closeout.md`
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
- Pending ledger row: `None`.
- Closed ledger rows: CCFG-18 through CCFG-20, CCFG-30, and CCFG-31. CCFG-31
  replaces broad startup reconciliation with one narrow mechanical
  `ready`/`blocked` preflight while preserving strict per-handoff leases.
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
- Queued batch: `None`
- Queued dispatch: `None`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-31-narrow-live-lease-preflight`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/closeout.md`

## Next Safe Action

No batch is selected, queued, or active. Wait for an explicit `plan-batch`
request before selecting successor work; do not infer it during closeout.

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
- Stop if work treats closed CCFG-31 or its completed runway as active work.
