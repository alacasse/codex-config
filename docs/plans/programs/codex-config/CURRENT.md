# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/runway.md`
- Queued batch execution status: `Queued; strict preflight required before execution`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/closeout.md`
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
- CCFG-24A closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/closeout.md`
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
  `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/runway.md`
- Queued batch execution status: `Queued; strict preflight required before execution`
- Queued dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/dispatch.md`
- Superseded CCFG-24 planning evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/superseded.md`
- Superseded CCFG-24A blocked attempt:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/superseded.md`
- Completed preparation batch:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/closeout.md`
- CCFG-25 remains unselected and has no dispatch or runway.
- Abandoned-state correction archived:
  `docs/plans/archive/abandoned/ccfg-8-ledger-dispatch-rule-dedupe/closeout.md`
- Latest completed batch: `ccfg-24a-intake-owner-preparation`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/closeout.md`

## Next Safe Action

A later explicit `work-batch` request may execute only the queued four-slice
CCFG-24B runway. Start from Planning State, pass the immutable planning snapshot
through the installed ready/blocked strict preflight, and proceed only on
`ready`. CCFG-24 remains `Pending` until same-batch closeout. Do not select or
prepare CCFG-25.

## Stop Conditions

- Stop if work treats closed CCFG-18 or its completed runway as active work.
- Stop if planning weakens strict `cross-checkout-context/v1` or treats the
  planning snapshot as a live execution lease.
- Stop if any default stable-home installed link resolves to the redesign branch
  or candidate clone.
- Stop if selected dispatch, active runway, or a second queued batch appears.
- Stop if planning would write outside the canonical stable planning repository.
- Stop if candidate code or helpers would control canonical state before final
  integration.
- Stop if work would repeat command-owner redesign intake or create new
  identities instead of amending CCFG-18 through CCFG-29.
- Stop if work treats CCFG-19 or CCFG-20 as active after completed closeout.
- Stop if work would select from archived APR/PST ledgers instead of the canonical
  codex-config ledger.
- Stop if work would execute the displaced CCFG-11 runway without replanning.
- Stop if work would copy archived history into the active ledger row-by-row.
- Stop if a generic reusable skill receives project-specific paths, commands,
  caches, or planning layouts.
- Stop if work treats closed CCFG-21, CCFG-22, CCFG-23, CCFG-30, CCFG-31,
  CCFG-32, or CCFG-33 as active work.
- Stop if CCFG-32 execution semantics, Git-derived queue currentness, or broad
  live-lease protocol topology are restored.
- Stop if CCFG-22 or CCFG-23 behavior is widened into production ownership beyond
  their accepted closeouts.
- Stop if CCFG-33 exact-commit acceptance restores source-hash authority, nested
  reporter pytest, a permanent cache, committed generated receipt, or CI workflow.
- Stop if work executes, resumes, or closes the superseded
  `ccfg-24-intake-ownership-transfer` dispatch or runway.
- Stop if work executes or reopens CCFG-24A rather than consuming its closeout.
- Stop if CCFG-24B adds an adapter, merge behavior, store/schema change, or public
  retry identity.
- Stop if CCFG-24B deletes a surface without current caller and replacement
  evidence.
- Stop if CCFG-24B removes APR responsibilities reserved for CCFG-25 or CCFG-26.
- Stop if CCFG-24B removes `legacy-removal` evidence, compatibility decisions,
  cleanup-residue classification, or deletion/dead-surface vocabulary.
- Stop if CCFG-24B mutates the stable Codex home or candidate code mutates
  canonical planning state.
- Stop if CCFG-24B closeout does not leave `add-to-ledger/v1` as the sole intake
  and normal ledger-mutation decision owner with complete COR-007 evidence.
- Stop if any CCFG-24 closeout selects or prepares successor work.
- Stop if CCFG-24 through CCFG-29 retain replaced CCFG-23 fixtures or tests
  without a named caller, reason, owner, and removal condition.
