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

## Open Ledger

- Ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Open ledger rows: CCFG-2 through CCFG-6, CCFG-9 through CCFG-11, and
  CCFG-18 through CCFG-29.
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
- Latest completed batch: `ccfg-17-absolute-runway-reference-paths`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/closeout.md`

## Next Safe Action

No batch is selected, queued, or active. CCFG-18 through CCFG-29 remain open and
unselected. CCFG-18 is the first dependency-free command-owner redesign item.

Before an explicit `plan-batch CCFG-18` request, verify in a fresh stable session:

```yaml
stable_checkout:
  branch: master
  clean_or_classified: true
installed_generation:
  default_codex_home_resolves_to_stable_checkout: true
  required_skills_resolve_to_one_stable_commit: true
  candidate_links: 0
planning_state:
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  resumable_runner_state: false
project_values:
  stable_checkout_path: known
  candidate_clone_path: known
  candidate_codex_home_path: known
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
```

`plan-batch` may then select or narrow CCFG-18 only. CCFG-18 owns creation of the
candidate clone, implementation branch, merge of the accepted design history,
candidate `CODEX_HOME`, temporary cross-checkout control support, mechanical
generation identity, fixture-only candidate validation, and pre-cutover rollback
proof.

Do not require those implementation results before planning CCFG-18; doing so
would create a circular prerequisite.

CCFG-11 remains open, but its displaced runway is superseded planning evidence.
Do not execute it without a future regenerated or amended runway that applies the
CCFG-13 validation status, CCFG-14 risk gates, CCFG-15 vague-row guard, and
CCFG-16 deletion-test vocabulary rules.

## Stop Conditions

- Stop if installed skills do not resolve to one stable `master` generation.
- Stop if any installed link resolves to the redesign branch or candidate clone.
- Stop if selected, queued, active, or resumable state appears before CCFG-18
  planning.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before cutover.
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
