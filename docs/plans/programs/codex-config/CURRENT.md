# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/runway.md`
- Active batch execution status: `queued`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/closeout.md`
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
  CCFG-27 through CCFG-29.
- Pending ledger row: CCFG-34, reviewed and queued for a later explicit
  `work-batch` invocation.
- Blocked ledger row: CCFG-26, waiting for CCFG-34 closeout and fresh
  replanning.
- Closed ledger rows: CCFG-18 through CCFG-25 and CCFG-30 through CCFG-33.
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
- CCFG-24B closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/closeout.md`
- CCFG-25 closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/closeout.md`
- Live CCFG-34 intake and CCFG-26 replanning amendment:
  `docs/plans/programs/codex-config/findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Live CCFG-25 planning-quality amendment:
  `docs/plans/programs/codex-config/findings/ccfg-25-planning-quality-amendment.md`
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
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/runway.md`
- Active batch execution status: `queued`
- Queued CCFG-34 dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/dispatch.md`
- Queued CCFG-34 independent planning review:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/review.md`
- Superseded CCFG-24 planning evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/superseded.md`
- Superseded CCFG-24A blocked attempt:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/superseded.md`
- Completed preparation batch:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/closeout.md`
- Completed intake-ownership cutover:
  `docs/plans/programs/codex-config/batches/ccfg-24b-intake-ownership-cutover/closeout.md`
- Completed planning-ownership transfer:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/closeout.md`
- Superseded CCFG-26 planning evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-closeout-ownership-transfer/superseded.md`
- Latest completed batch: `ccfg-25-planning-ownership-transfer`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/closeout.md`

## Next Safe Action

CCFG-34 is the sole reviewed, queued batch. A later explicit `work-batch`
invocation may execute exactly
`batches/ccfg-34-stable-runway-dogfooding-bootstrap/runway.md`. CCFG-26 remains
blocked until CCFG-34 closeout, then must be replanned from fresh canonical
state. Do not select, dispatch, queue, refresh, or prepare CCFG-26 through
CCFG-29 during this queue transition.

## Stop Conditions

- Stop if work treats closed CCFG-18 or its completed runway as active work.
- Stop if planning weakens strict `cross-checkout-context/v1` or treats the
  planning snapshot as a live execution lease.
- Stop if any default stable-home installed link resolves to the redesign branch
  or candidate clone.
- Stop if work treats the completed CCFG-24B dispatch or runway as active state.
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
- Stop if work reopens CCFG-24 or treats its closeout as authority to select or
  prepare CCFG-25 without the explicit request already recorded in this dispatch.
- Stop if future work restores an APR intake route, a `legacy-removal` state-owner
  escape hatch, or stable-home ownership from the candidate generation.
- Stop if CCFG-24 through CCFG-29 retain replaced CCFG-23 fixtures or tests
  without a named caller, reason, owner, and removal condition.
- Stop if the superseded CCFG-26 dispatch, review, or runway is treated as
  selected, queued, active, resumable, or executable.
- Stop if planning bypasses CCFG-34 or selects CCFG-26 before CCFG-34 closeout
  and a fresh CCFG-26 replan.
- Stop if any other batch becomes selected, queued, or active while CCFG-34 is
  queued, or if this planning flight begins CCFG-34 implementation.
- Stop if CCFG-25 introduces a new planning schema, store, queue transaction,
  lifecycle state, public command, persistent draft store, helper behavior,
  runner protocol, or compatibility layer.
- Stop if planner/reviewer independence is not direct and mechanically evidenced.
- Stop if CCFG-25 removes or narrows any proceed/stop, delegation, recovery,
  validation, review, commit, receipt, finalization, closeout, reconciliation, or
  strict execution-safety responsibility reserved for CCFG-26.
- Stop if another live planning caller or runner semantic owner requiring an edit
  is discovered outside the exact amended Slice 2 ceiling.
- Preserve `select-dispatch`, `create-spec`, `execute`, and `closeout` as serialized
  compatibility identities through CCFG-25. CCFG-27 owns their migration/removal
  decision; final physical cleanup is due no later than CCFG-29.
- Stop if CCFG-25 closeout selects, dispatches, queues, or prepares CCFG-26.
- Stop if pickup infers queue state from the superseded CCFG-26 runway or treats
  its reviewed planning snapshot as a live execution lease.
- Stop if CCFG-26 restores Git, ancestry, path sets, fingerprints, or dirty files
  as semantic batch-lifecycle or queue authority.
- Stop if CCFG-26 changes or removes the serialized `select-dispatch`,
  `create-spec`, `execute`, or `closeout` identities reserved for CCFG-27,
  physically deletes legacy-owner directories reserved for CCFG-28, or changes
  the temporary bridge reserved for CCFG-29.
- Stop if CCFG-26 is replanned without the permanent candidate behavior from
  GitHub issues #59, #60, and #61, or if that replan changes COR-009 identity.
- Stop if CCFG-34 builds a second complete runway framework, permanent public
  protocol, persistent execution store, or lifecycle framework instead of the
  bounded temporary bootstrap authorized by issue #62.
