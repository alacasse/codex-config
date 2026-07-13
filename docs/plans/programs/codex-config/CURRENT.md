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
- Blocked ledger row: CCFG-18. Stable pre-creation support is committed, but
  the changed feature set must be installed and loaded in a fresh stable
  session before candidate creation can be planned.
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
- Latest completed batch: `ccfg-18-stable-precreation-support`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/closeout.md`

## Next Safe Action

Install the exact committed stable feature set, verify installed versions and
stable-checkout links, then start a fresh stable session. In that fresh session,
rerun planning-state `current` and `validate`; only then may an explicit
`plan-batch CCFG-18` plan the remaining candidate-creation scope. No successor
is selected now, and CCFG-19 remains unselected.

## Stop Conditions

- Stop if remaining CCFG-18 planning begins before the committed feature set is
  installed and loaded in a fresh stable session.
- Stop if planning weakens strict `cross-checkout-context/v1` or treats
  pre-creation verification as strict identity.
- Stop if work creates the candidate repository or candidate `CODEX_HOME`
  before a new explicit CCFG-18 batch authorizes those exact paths.
- Stop if any installed link resolves to the redesign branch or candidate clone.
- Stop if selected dispatch, active runway, queued batch, or resumable state
  appears before a new explicit `plan-batch CCFG-18` request.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
- Stop if the stable helper link or installed feature versions do not match the
  exact closeout commit.
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
