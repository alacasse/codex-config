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
- Prepared ledger row: CCFG-18. The stable control bootstrap is complete; its
  candidate-generation remainder remains under the same finding identity.
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

No batch is selected, queued, or active. CCFG-18 is `Prepared`, not `Closed`.

Continue only in a fresh stable session loaded from the exact `master` commit
that contains this closeout. In that session:

1. Verify every repo-owned installed link resolves to this stable checkout and
   that candidate links remain zero.
2. Install the committed stable feature set so the new helper link and feature
   versions are present; then verify installed state and reload before using the
   changed control for real work.
3. Rerun `planning_state.py current` and `validate` against `docs/plans`.
4. Invoke a new explicit `plan-batch CCFG-18` for only the remaining candidate
   clone, candidate `CODEX_HOME`, lineage, identity, fixture-only, and rollback
   scope.

Do not select CCFG-19.

## Stop Conditions

- Stop if the next session is not freshly loaded from the exact stable `master`
  commit containing this closeout.
- Stop if any installed link resolves to the redesign branch or candidate clone.
- Stop if selected dispatch, queued batch, active runway, or resumable state
  appears before the next explicit `plan-batch CCFG-18` request.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
- Stop if the stable helper link or committed feature versions are missing after
  the fresh-session install and reload.
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
