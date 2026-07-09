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
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/closeout.md`
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
- Active rows: CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11.
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
- Latest completed batch: `ccfg-17-absolute-runway-reference-paths`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/closeout.md`
- Covers: CCFG-17, completed as Batch Runway generated reference-path guidance,
  focused create-spec contract coverage, and an active-runway artifact guard.
  Historical completed runways were not rewritten.

## Next Safe Action

No batch is selected, queued, or active. CCFG-17 has concrete closeout evidence
and same-batch program reconciliation is complete. Do not select successor work
until a future explicit `plan-batch` request asks for another batch.

CCFG-11 remains open, but its displaced runway is superseded planning evidence;
do not execute it as active state without a future regenerated or amended runway
that includes validation-command status classes, batch kind, slice risk
classes, approval gates where required, and a CCFG-15 split, block, or
narrow-scope decision before selected dispatch and concrete runway creation.
Future CCFG-11 planning must also use the CCFG-16 deletion-test vocabulary owner
and generated-artifact consumer rules, or define any non-canonical labels
locally as labels only.

## Stop Conditions

- Stop if work would select from archived APR/PST ledgers instead of the
  canonical codex-config ledger.
- Stop if work would select successor work, create another dispatch, or create
  another runway without a future explicit `plan-batch` request.
- Stop if work would execute the displaced CCFG-11 runway as active state
  without a future regenerated or amended runway.
- Stop if work would regenerate or execute CCFG-11 without validation-command
  status classes, batch kind, slice risk classes, and approval gates where
  required.
- Stop if work would plan CCFG-11 from the displaced artifact without first
  splitting, blocking, or narrowing its vague mixed-risk scope under the
  CCFG-15 guard.
- Stop if work would replan or execute CCFG-11 using ambiguous deletion-test
  labels such as `no-op`, `sediment`, `obsolete skill surface`, or
  `deletion-safe evidence` without applying the CCFG-16 canonical vocabulary or
  locally defining those labels as non-canonical labels only.
- Stop if CCFG-1 closeout text would imply runner extraction, package/runtime
  selection, repository/scaffold creation, adapter implementation, or CCFG-2
  through CCFG-5 work is complete.
- Stop if work would copy closed APR/PST history into the active ledger
  row-by-row.
- Stop if work would add project-specific paths, validation commands, cache
  locations, or local planning layouts to a generic reusable skill.
