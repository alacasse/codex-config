# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/closeout.md`
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

## Active Ledger

- Ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Active rows: CCFG-2 through CCFG-6, CCFG-9 through CCFG-11, and CCFG-14.
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Batch State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch:
  `docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-13-validation-command-status`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/closeout.md`
- Covers: CCFG-13, completed as validation-command status classification for
  Batch Runway create-spec guidance and focused contract tests.
  Runtime behavior did not change.

## Next Safe Action

CCFG-14 is queued at
`docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/runway.md`.
A future explicit `work-batch` request owns execution from that runway.

CCFG-11 remains open, but its displaced runway is superseded planning evidence;
do not execute it as active state without a future regenerated or amended
runway.

CCFG-14 is the Batch Runway create-spec prerequisite before CCFG-11 is
regenerated or executed. It should add batch-kind and destructive-slice risk
gates rather than patching only the displaced CCFG-11 artifact.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would select successor work, create another dispatch, or create
  another runway without an explicit `plan-batch` request.
- Stop if work would execute the displaced CCFG-11 runway as active state
  without a future regenerated or amended runway.
- Stop if work would regenerate or execute CCFG-11 without first handling or
  explicitly superseding the CCFG-14 batch-kind and destructive-slice risk
  boundary.
- Stop if CCFG-1 closeout text would imply runner extraction, package/runtime
  selection, repository/scaffold creation, adapter implementation, or CCFG-2
  through CCFG-5 work is complete.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
