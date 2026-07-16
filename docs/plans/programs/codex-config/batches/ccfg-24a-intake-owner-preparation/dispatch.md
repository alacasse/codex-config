# CCFG-24A Intake Owner Preparation Dispatch

## Selection

- Batch ID: `ccfg-24a-intake-owner-preparation`
- Source finding: CCFG-24, Transfer Intake Ownership to `add-to-ledger`
- Accepted source: COR-007 at commit
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Live amendment:
  `docs/plans/programs/codex-config/findings/ccfg-24-two-batch-execution-amendment.md`
- Superseded planning evidence:
  `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/`
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-24a-intake-owner-preparation/runway.md`

## Selection Decision

Select only the preparation half of CCFG-24. This batch creates an installed,
behaviorally proven target owner and closes the unresolved v1 intake decisions.
It does not remove legacy ownership or close COR-007.

The original five-slice runway combined target design, implementation,
behavioral migration, destructive fixture cleanup, APR narrowing,
`legacy-removal` narrowing, installation convergence, and final acceptance in
one execute coordinator context. That plan is superseded to reduce context
pressure and create a mandatory evidence-based reassessment before destructive
cutover work.

## Goal

Leave the candidate generation with:

- one explicit and deterministic internal contract between the human-facing
  `add-to-ledger` skill and `scripts/add_to_ledger.py`;
- a bounded v1 source-identity and normalization policy;
- an explicit create/update/merge/no-op/block decision matrix;
- a real `add-to-ledger/v1` production owner using the existing apply-only
  `ledger-store/v1` mechanism;
- a neutral candidate-installed `planning-contracts` feature;
- the stable intake scenarios bound to the installed production owner;
- measured implementation and validation cost;
- retained legacy paths classified for a later separately planned cutover batch.

CCFG-24 remains `Prepared` after this batch. CCFG-25 remains ineligible.

## Included Contracts

- `INTAKE-SOURCE-001`
- `INTAKE-IDENTITY-002`
- `INTAKE-NORMALIZE-003`
- `INTAKE-MUTATE-004`
- `INTAKE-STOP-005`
- DEC-037 apply-only `ledger-store/v1`

This batch proves the target owner against those contracts but does not claim
that legacy ownership has been removed.

## Included Work

1. Produce one durable implementation decision record covering:
   - command-to-script invocation;
   - supported source types and field mapping;
   - deterministic duplicate/update/merge/no-op/block rules;
   - success and blocked result shapes;
   - unsupported or ambiguous cases that fail closed.
2. Implement and candidate-install `add-to-ledger/v1` plus the neutral
   `planning-contracts` mechanism.
3. Bind the four stable intake scenarios and focused negative paths to the
   installed production owner using temporary schema-valid ledgers.
4. Measure focused tests, exact intake acceptance, installation checks, changed
   files, and line delta.
5. Produce a current inventory and removal conditions for every retained intake
   fixture and legacy-owner route.

## Explicitly Deferred

A later explicit `plan-batch` request owns all remaining CCFG-24 work. This batch
must not:

- delete `_run_intake`, `_new_finding`, or related migration surfaces;
- remove APR intake, normalization, or normal ledger mutation authority;
- remove the `add-to-ledger -> architecture-program-runway` dependency;
- narrow `legacy-removal` lifecycle ownership;
- migrate the CCFG-24 half of shared manifest source-boundary assertions to final
  cutover state;
- claim complete COR-007 acceptance;
- close CCFG-24;
- create, select, dispatch, or queue Batch B;
- start CCFG-25.

## Batch Kind And Slice Shape

- Batch kind: `migration-with-decision-gate`
- Slice 1: `evidence-only` — close the v1 owner decisions and define the smallest
  supported behavior.
- Slice 2: `migration` — implement and candidate-install the target owner and
  neutral mechanism.
- Slice 3: `migration` — bind production scenarios, measure cost, and classify
  retained migration surfaces.

The three slices form one vertical preparation path. Slice 2 is blocked until
Slice 1 decisions are explicit and reviewable. Slice 3 is blocked until the
candidate-installed owner is green.

## Required Intermediate States

- After Slice 1: no production change; one accepted deterministic implementation
  contract exists.
- After Slice 2: the candidate home can invoke the new owner against a temporary
  ledger; old routes remain available but are not changed.
- After Slice 3: stable intake scenarios exercise the installed target owner and
  compact cost/removal evidence is ready for a fresh follow-up plan.

## Guardrails

- Stable planning repository:
  `/home/alacasse/projects/codex-config`
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Stable Codex home:
  `/home/alacasse/.codex`
- Candidate Codex home:
  `/home/alacasse/.codex-command-owner-redesign`
- Do not install, refresh, unlink, or rebind the stable home.
- Candidate processes must not mutate canonical planning state.
- `scripts/planning_contract.py` and planning schemas remain mechanically
  apply-only and read-only unless a focused proof exposes a blocking gap; stop
  for replan before semantic widening.
- Do not make `skill-authoring`, APR, or `legacy-removal` a runtime mechanism of
  the new owner.
- Do not create a general public intake framework, durable intake queue, second
  store, second ledger, or public request schema without a separately approved
  decision.
- Unsupported source or semantic cases block; they do not trigger scope growth.

## Context Budget

The execute coordinator must prefer this dispatch, the active slice section,
compact receipts, and current closeout evidence over broad rereads. Record the
execute phase context telemetry when available.

- Soft execute budget: 120,000 input tokens.
- Hard warning: 180,000 input tokens.
- Stop and amend rather than silently compacting through unresolved scope when
  context pressure coincides with new semantic decisions or broad source reads.

## Validation Class

- Runway density: `bounded-full-runway`
- Validation profile: `project-harness-production`
- Every test-changing slice requires delta-only `test-quality-review` after
  independent review.
- Slice 2 and final range require `import_topology_reviewer`.
- Slice 3 and final range require `dead-surface-audit` only for retained intake
  fixtures and caller/removal classification; no deletion is authorized.
- Run the CCFG-33 exact-commit acceptance owner once at final validation, focused
  on proving the intake family remains green without repeating reporter-owned
  recursive execution.

## Planning And Execution Context

The validated strict snapshot in the superseded runway remains historical
planning evidence for roots and generation separation. It is not a live lease
for this replacement runway.

At execution startup, `work-batch` must:

1. confirm this exact queued batch through Planning State;
2. obtain a fresh ready preflight;
3. validate the current stable and candidate revisions, roots, generation role,
   Codex home, and exact write scope through `cross-checkout-context/v1`;
4. repeat fresh strict validation before every worker or reviewer handoff.

Null, stale, mismatched, or differently scoped identity blocks execution.

## Closeout Contract

The batch closeout must:

- leave CCFG-24 `Prepared`;
- clear this batch's selected, queued, and active pointers;
- record the candidate commit range and candidate-installed link targets;
- record the final decision record path;
- record focused and exact acceptance durations, test counts, changed-file count,
  and line delta;
- classify retained APR, `legacy-removal`, and CCFG-23 intake surfaces with
  caller, reason, owner, and removal condition;
- state what Batch B must reassess without creating its dispatch or runway;
- stop without successor selection.

## Stop Conditions

- Stop if the v1 source mapping or semantic decision matrix remains ambiguous.
- Stop if the target owner cannot be invoked through the candidate-installed
  command surface.
- Stop if semantic intake decisions move into `ledger-store/v1`.
- Stop if candidate code can mutate canonical planning state.
- Stop if implementation requires deleting or narrowing legacy owners in this
  batch.
- Stop if a retained migration surface cannot be given a caller, reason, owner,
  and removal condition.
- Stop if work expands into CCFG-25 or creates Batch B planning.
- Stop after same-batch closeout with CCFG-24 `Prepared` and no successor selected.
