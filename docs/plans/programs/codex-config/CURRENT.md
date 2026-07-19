# Codex Config Current State

## Program

- Program slug: `codex-config`
- Purpose: maintain one canonical active program ledger for codex-config
  workflow, runner, planning-state, and skill-cleanup work.
- Current ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Selected dispatch path: `None`
- Active Batch Runway spec path: `None`
- Queued batch path or ID:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md`
- Active batch execution status:
  `blocked in Slice 1 final review; candidate work remains uncommitted at 5c5ec9d; stable work-batch remains the real-batch controller; no successor selected`
- Latest closeout path:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/closeout.md`
- Run artifact location: `None`; the real implementation batch has no Batch
  Execution State. Fixture roots are allocated at execution time and are not
  durable planning state.
- Program archive location: `docs/plans/archive/`

## Project State Policy

- Planning root: `docs/plans/`
- Slice-shape policy path: notes/slice-shape-policy.yaml
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
- Pending ledger row: CCFG-26. Its first bounded execution-foundation batch is
  selected and queued but blocked in Slice 1 final review. The uncommitted
  candidate implementation passed its last focused local baseline, but the
  final path-based filesystem effects remain vulnerable to namespace
  substitution. A reviewed amendment or superseding replan must authorize one
  cross-platform anchored-filesystem mechanism and Windows validation path
  before implementation resumes. The batch still has two vertical Slices; the
  stable controller owns both real Slices, and Slice 2 remains unstarted. No
  implementation Slice is accepted or committed, and no successor is selected.
  CCFG-26C through CCFG-26E remain unselected conceptual evidence, not a
  successor chain.
- Closed ledger rows: CCFG-18 through CCFG-25 and CCFG-30 through CCFG-34.
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
- CCFG-34 closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/closeout.md`
- Live CCFG-34 intake and CCFG-26 replanning amendment:
  `docs/plans/programs/codex-config/findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Completed CCFG-26A dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/dispatch.md`
- Completed CCFG-26A runway:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/runway.md`
- CCFG-26A planning review and bounded amendment evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/review.md`
- CCFG-26A completed-slice evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/completed-slices.md`
- CCFG-26A closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/closeout.md`
- Completed CCFG-26 slice-shape correction dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/dispatch.md`
- Completed CCFG-26 slice-shape correction runway:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/runway.md`
- Clean CCFG-26 slice-shape correction planning review:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/review.md`
- CCFG-26 slice-shape correction completed-slice evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/completed-slices.md`
- CCFG-26 slice-shape correction closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/closeout.md`
- CCFG-26 slice-shape correction post-closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`
- Superseded CCFG-26B dispatch, historical evidence only:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/dispatch.md`
- Historical CCFG-26B planning review:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/review.md`
- Historical CCFG-26B bounded amendment:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/amendment.md`
- Historical CCFG-26B amendment review:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/amendment-review.md`
- Historical CCFG-26B progression-authority correction, exact SHA-256
  `b7dbe71f2b8eaa0bff76c14a21a1e08fb5c73c8b2d1b015741b37766ce06cf2a`:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-authority-correction.md`
- Historical CCFG-26B progression-authority review, exact SHA-256
  `7044c8afd1119919902e26cd22e1974a8b52b6549f347c1c85942fa99775dfce`:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-authority-review.md`
- Historical CCFG-26B unresolved-attempt barrier correction, exact SHA-256
  `94388b089bd1da22d570576735c567f08bb994cf7ddba809f0c2f013f445a3ad`:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-attempt-barrier-correction.md`
- Historical CCFG-26B unresolved-attempt barrier review, exact SHA-256
  `386694d7c06db5c6bb1f55018dc623be2d0bfcf40d733972ab826ac6ba5ac433`:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/progression-attempt-barrier-review.md`
- Superseded CCFG-26B runway, historical evidence only:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md`
- CCFG-26B supersession notice:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/superseded.md`
- Accepted CCFG-26 execution-state direction amendment:
  `docs/plans/programs/codex-config/findings/ccfg-26-execution-state-authority-direction.md`
- CCFG-26 replan analysis and ChatGPT Pro handoff:
  `docs/plans/programs/codex-config/notes/ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`
- Accepted CCFG-26 execution-state design contract:
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-contract.md`
- Clean CCFG-26 execution-state design review:
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-review.md`
- Accepted canonical batch execution-state ADR:
  `docs/adr/0003-canonical-batch-execution-state.md`
- CCFG-26 slice-shape policy direction from GitHub issue #66:
  `docs/plans/programs/codex-config/findings/slice-shape-policy-direction.md`
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
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md`
- Active batch execution status:
  `blocked in Slice 1 final review; preserve the uncommitted candidate worktree; no implementation commit, closeout, or successor selected`
- Queued CCFG-26 execution-state foundation dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/dispatch.md`
- Historical original planning review; insufficient by itself to authorize
  execution:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/review.md`
- Authoritative fixture-only bootstrap amendment:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/amendment.md`
- Clean bootstrap amendment review:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/amendment-review.md`
- Blocked Slice 1 execution report:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/execution-report.md`
- Superseded CCFG-26B evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/superseded.md`
- Accepted CCFG-26 direction:
  `docs/plans/programs/codex-config/findings/ccfg-26-execution-state-authority-direction.md`
- Durable CCFG-26 design handoff:
  `docs/plans/programs/codex-config/notes/ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`
- Accepted CCFG-26 execution-state design contract:
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-contract.md`
- Clean CCFG-26 execution-state design review:
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-review.md`
- Completed CCFG-26 slice-shape correction dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/dispatch.md`
- Completed CCFG-26 slice-shape correction review:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/review.md`
- Completed CCFG-26 slice-shape correction runway:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/runway.md`
- Completed CCFG-26 slice-shape correction closeout:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/closeout.md`
- CCFG-26 slice-shape correction post-closeout evidence:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`
- Completed CCFG-26A dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/dispatch.md`
- Completed CCFG-26A review:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/review.md`
- Completed CCFG-26A runway:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/runway.md`
- Completed CCFG-26A closeout:
  `docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/closeout.md`
- Completed CCFG-34 dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/dispatch.md`
- Completed CCFG-34 review evidence:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/review.md`
- Completed CCFG-34 closeout:
  `docs/plans/programs/codex-config/batches/ccfg-34-stable-runway-dogfooding-bootstrap/closeout.md`
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
- Latest completed batch: `ccfg-26-slice-shape-policy-correction`
- Latest completed dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/dispatch.md`
- Latest completed runway:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/runway.md`
- Latest closeout:
  `docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/closeout.md`

## Next Safe Action

Do not resume implementation under the current Slice 1 scope. Preserve the
uncommitted candidate worktree and read
`batches/ccfg-26-execution-state-foundation/execution-report.md`. Use a reviewed
planning amendment or superseding replan to choose and authorize exactly one
cross-platform anchored-filesystem mechanism, its dependency or native-backend
boundary, and its Windows validation path. Only then refresh Planning State and
the strict live lease, delegate the authorized correction, rerun all Slice 1
validation and reviews, and request a fresh exact-diff runway review. Do not
start Slice 2, create real Batch Execution State, close the batch, resume
CCFG-26B, select CCFG-26C through CCFG-26E, or select any successor.

## Stop Conditions

- Stop if the queued runway or original review is consumed without the exact
  bootstrap amendment and its clean amendment review.
- Stop if candidate machinery controls, selects, reserves, launches, resolves,
  or derives either real implementation Slice of this batch.
- Stop if execution creates a real Batch Execution State or durable temporary
  run-artifact root for this implementation batch.
- Stop if execution resumes without reviewed authority for a cross-platform
  final-effect confinement mechanism and its Windows validation path.
- Stop if execution imports the stable completed prefix into candidate state or
  adds a legacy-prefix initialization or migration event.
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
- Stop if any CCFG-26B artifact is treated as queued, active, executable,
  resumable, amendable, or authoritative for a future slice sequence.
- Stop if work treats closed CCFG-21, CCFG-22, CCFG-23, CCFG-30, CCFG-31,
  CCFG-32, CCFG-33, or CCFG-34 as active work.
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
- Stop if work selects, dispatches, queues, refreshes, or prepares superseded
  CCFG-26B under any condition.
- Stop if work selects, dispatches, queues, refreshes, or prepares CCFG-26C
  through CCFG-26E, or selects replacement CCFG-26 work without a later explicit
  stable `plan-batch` based on the accepted execution-state design contract.
- Stop if CCFG-34 closeout is treated as permission to select or prepare a
  successor batch.
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
- Stop if replacement CCFG-26 work or CCFG-26C through CCFG-26E are planned
  without the permanent candidate behavior from GitHub issues #59, #60, and
  #61, or if that planning changes COR-009 identity.
- Stop if future work reopens CCFG-26A, adds compatibility for historical
  CCFG-26B progression artifacts, or treats CCFG-26C through CCFG-26E as an
  already accepted successor map.
- Stop if work treats the completed `ccfg-26-slice-shape-policy-correction`
  runway as selected, queued, active, resumable, or executable.
- Stop if CCFG-26A is widened beyond permanent candidate vertical-planning
  behavior from issue #60 or pulls issue #59/#61 execution behavior into its
  single slice.
- Stop if CCFG-26A execution selects, dispatches, queues, refreshes, or prepares
  CCFG-26B through CCFG-26E or any later finding.
- Stop if CCFG-34 builds a second complete runway framework, permanent public
  protocol, persistent execution store, or lifecycle framework instead of the
  bounded temporary bootstrap authorized by issue #62.
