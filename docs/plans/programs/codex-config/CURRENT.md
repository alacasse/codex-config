# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/closeout.md`
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
  CCFG-19 through CCFG-29.
- Pending ledger row: CCFG-18. The installed stable pre-creation controller now
  governs one queued candidate-generation runway.
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
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/dispatch.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-18-stable-precreation-support`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/closeout.md`

## Next Safe Action

Use `work-batch` to execute
`docs/plans/programs/codex-config/batches/ccfg-18-candidate-generation/runway.md`.
Revalidate the complete installed-helper pre-creation payload before creating
either exact candidate root, transition to strict context immediately after
repository/environment establishment, and stop after same-batch CCFG-18
closeout. CCFG-19 remains unselected.

## Stop Conditions

- Stop if execution bypasses the queued CCFG-18 candidate-generation runway.
- Stop if planning weakens strict `cross-checkout-context/v1` or treats
  pre-creation verification as strict identity.
- Stop if work creates the candidate repository or candidate `CODEX_HOME`
  before the queued runway revalidates exact pre-creation authority.
- Stop if any default stable-home installed link resolves to the redesign branch
  or candidate clone.
- Stop if selected dispatch, active runway, or a second queued batch appears.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
- Stop if the stable helper link, installed feature versions, or stable revision
  no longer match the queued runway's validated baseline.
- Stop if work would repeat command-owner redesign intake or create new identities
  instead of amending CCFG-18 through CCFG-29.
- Stop if work would select successor work, create another dispatch, or create
  another runway without an explicit future `plan-batch` request.
- Stop if work would select from archived APR/PST ledgers instead of the canonical
  codex-config ledger.
- Stop if work would execute the displaced CCFG-11 runway without replanning.
- Stop if work would copy archived history into the active ledger row-by-row.
- Stop if a generic reusable skill receives project-specific paths, commands,
  caches, or planning layouts.
- Stop if execution selects CCFG-19 or marks CCFG-18 `Closed` without complete
  candidate lineage, transition, identity, fixture-isolation, quiescence, and
  rollback evidence.
