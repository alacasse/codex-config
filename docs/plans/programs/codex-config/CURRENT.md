# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/closeout.md`
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
  CCFG-24 through CCFG-29.
- Pending ledger row: CCFG-33.
- Closed ledger rows: CCFG-18 through CCFG-23 and CCFG-30 through CCFG-32.
  CCFG-21 closes all six COR-004 planning-contract acceptance keys without live
  planning migration or command integration.
  CCFG-22 closes all nine COR-005 authoring acceptance keys with candidate-only
  installation and no command-owner runtime dependency.
  CCFG-23 closes all six COR-006 behavioral-harness acceptance keys and six
  aliases across all 31 immutable contracts without production ownership
  transfer or real cutover.
- Accepted command-owner redesign snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Live redesign decisions:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-bootstrap-decisions.md`
- Live planning and execution carry-forward amendment:
  `docs/plans/programs/codex-config/findings/command-owner-redesign-planning-execution-carry-forward.md`
- Archived APR source:
  `docs/plans/archive/program-ledgers/architecture-program-runner-LEDGER.md`
- Archived PST source:
  `docs/plans/archive/program-ledgers/planning-state-tooling-LEDGER.md`

## Batch State

- Selected dispatch: `None`
- Active runway: `None`
- Queued batch:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/dispatch.md`
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-23-behavioral-scenario-harness`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/closeout.md`

## Next Safe Action

Execute only the queued CCFG-33 runway through a later explicit `work-batch`
request. CCFG-24 waits for CCFG-33 closeout. Do not replace this runway, select
another batch, or infer successor work from its eventual closeout.

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
- Stop if work treats closed CCFG-32 or its completed runway as active work.
- Stop if work treats closed CCFG-21 or its completed runway as active work.
- Stop if work treats closed CCFG-22 or its completed runway as active work.
- Stop if work treats closed CCFG-23 or its completed runway as active work.
- Stop if CCFG-32 execution restores Git-derived queue currentness, weakens
  material live-handoff safety, touches the redesign candidate, or expands into
  CCFG-21, CCFG-25, or CCFG-29 ownership.
- Stop if CCFG-32 closeout selects or prepares any successor dispatch or runway.
- Stop if CCFG-22 execution changes the stable Codex home, migrates live command
  owners, weakens supported-schema blocking, or expands into CCFG-23+ ownership.
- Stop if CCFG-22 closeout selects or prepares any successor dispatch or runway.
- Stop if CCFG-23 execution changes production command-owner ownership, live
  planning state, a real installed generation, or the temporary bridge.
- Stop if CCFG-23 target scenarios require APR/Batch Runway topology, exact
  prompt prose, stable-only paths, historical helper names, or real cutover
  state to turn green.
- Stop if CCFG-23 closeout selects or prepares any successor dispatch or runway.
- Stop if CCFG-33 planning restores removed code solely because an import,
  identity, topology, or migration-retention test fails.
- Stop if CCFG-33 closeout lacks preserved COR-006 behavior, separate fast and
  acceptance gates, deletion or migration of obsolete preserving tests, or
  before/after duration and process evidence.
- Stop if CCFG-24 is selected before CCFG-33 closes.
- Stop if CCFG-24 through CCFG-29 retain replaced CCFG-23 fixtures or tests
  without a named caller, reason, owner, and removal condition.
