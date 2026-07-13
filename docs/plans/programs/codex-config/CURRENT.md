# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/closeout.md`
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
- Pending ledger row: CCFG-18. The stable pre-creation support amendment is
  controlled by the queued batch. Strict `cross-checkout-context/v1` remains
  the post-creation contract, and candidate creation stays deferred.
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
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/dispatch.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-18-stable-control-bootstrap`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/closeout.md`

## Next Safe Action

Execute only the queued
`ccfg-18-stable-precreation-support` runway through `work-batch`.

The runway is a single-root stable-control migration. It adds and validates
separate `cross-checkout-precreation/v1` support while preserving strict
`cross-checkout-context/v1`. It must not create the candidate repository or
candidate `CODEX_HOME`, perform a real install, reload changed stable control,
or select CCFG-19.

After same-batch closeout, install and load the changed stable feature set in a
fresh stable session. A later explicit `plan-batch CCFG-18` may then plan the
remaining candidate-creation scope. No successor is selected now.

## Stop Conditions

- Stop if planning weakens strict `cross-checkout-context/v1` instead of adding
  separate `cross-checkout-precreation/v1` support.
- Stop if execution would create the candidate repository or candidate
  `CODEX_HOME` instead of implementing stable pre-creation support only.
- Stop if any installed link resolves to the redesign branch or candidate clone.
- Stop if selected dispatch, active runway, another queued batch, or resumable
  state appears outside the queued CCFG-18 batch.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
- Stop if the stable helper link or committed feature versions drift from the
  installed stable generation.
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
- Stop if follow-up planning would mark CCFG-18 `Closed`, select CCFG-19, or
  bypass the remaining CCFG-18 scope.
