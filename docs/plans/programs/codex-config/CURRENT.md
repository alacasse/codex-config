# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/runway.md`
- Queued batch execution status: `Queued and executable; no slice started`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/closeout.md`
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
  CCFG-25 through CCFG-29.
- Pending ledger row: CCFG-24.
- Closed ledger rows: CCFG-18 through CCFG-23 and CCFG-30 through CCFG-33.
  CCFG-21 closes all six COR-004 planning-contract acceptance keys without live
  planning migration or command integration.
  CCFG-22 closes all nine COR-005 authoring acceptance keys with candidate-only
  installation and no command-owner runtime dependency.
  CCFG-23 closes all six COR-006 behavioral-harness acceptance keys and six
  aliases across all 31 immutable contracts without production ownership
  transfer or real cutover.
- Live CCFG-24 two-batch amendment:
  `docs/plans/programs/codex-config/findings/ccfg-24-two-batch-execution-amendment.md`
- Accepted CCFG-24A decision amendment:
  `docs/plans/programs/codex-config/findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`
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
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/runway.md`
- Queued batch execution status: `Queued and executable; no slice started`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/dispatch.md`
- Superseded CCFG-24 planning evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/superseded.md`
- Superseded CCFG-24A blocked attempt:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/superseded.md`
- Expected CCFG-24B cutover batch: unselected; no dispatch or runway exists.
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-33-acceptance-execution-simplification`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/closeout.md`

## Next Safe Action

A later explicit `work-batch` request may execute only the current two-slice
CCFG-24A runway. Start from Planning State, require a fresh ready strict
cross-checkout preflight, consume the accepted CCFG-24A decision amendment, and
use only temporary or fixture ledgers from candidate execution. Do not resume
`blocked-runway.md`. Keep CCFG-24 `Pending` until same-batch closeout, and keep
CCFG-24B and CCFG-25 unselected.

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
- Stop if work treats closed CCFG-33 or its completed runway as active work.
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
- Stop if CCFG-33 restores removed code solely because an import, identity,
  topology, source-hash, or migration-retention test fails.
- Stop if CCFG-33 edits the three known-red manifest tests, production skills or
  docs, manifest dependencies, installed homes, bridge code, or CCFG-24+
  ownership.
- Stop if CCFG-33 introduces a permanent cache, public raw-outcome seam,
  permanent receipt schema, committed generated receipt, or CI workflow.
- Stop if CCFG-33 closeout lacks preserved COR-006 behavior, one evidence-pytest
  process, process-local evaluation reuse, pure reporting, removal of
  per-function source-hash authority, unchanged known-red manifest diagnostics,
  or before/after cost evidence.
- Stop if work executes, resumes, or closes the superseded
  `ccfg-24-intake-ownership-transfer` dispatch or runway.
- Stop if CCFG-24A removes or narrows APR, `legacy-removal`, or retained intake
  fixtures instead of classifying them for later reassessment.
- Stop if CCFG-24A leaves the target owner prose-only, fixture-only, or not
  candidate-installed.
- Stop if CCFG-24A moves semantic intake decisions into `ledger-store/v1`,
  mutates stable installed state, or lets the candidate mutate canonical
  planning state.
- Stop if work executes `blocked-runway.md`, recreates its decision slice, or
  requires a store/schema semantic change instead of consuming the accepted
  CCFG-24A decision amendment.
- Stop if CCFG-24A closeout marks CCFG-24 `Closed`, selects or creates CCFG-24B,
  or selects or prepares CCFG-25.
- Stop if final CCFG-24 cutover leaves APR or `legacy-removal` as a normal intake
  owner, removes CCFG-25 planning or CCFG-26 closeout responsibilities, or lacks
  complete COR-007 acceptance.
- Stop if any CCFG-24 closeout selects or prepares successor work.
- Stop if CCFG-24 through CCFG-29 retain replaced CCFG-23 fixtures or tests
  without a named caller, reason, owner, and removal condition.
