# Cross-Flight Execution Baseline Plan

## Status And Ownership

- Finding: `CCFG-30`.
- Status: proposed implementation plan and intake evidence; not a selected
  dispatch or concrete Batch Runway spec.
- Human-facing owner: `work-batch` owns the decision to start execution from a
  queued runway after time and repository history have advanced.
- Runtime owner during the bridge state: Batch Runway owns the detailed
  reconciliation and delegation mechanics behind `work-batch`.
- Mechanical identity owner: `scripts/cross_checkout_context.py` continues to
  own root, generation, revision, and write-scope validation.
- Current-batch boundary: do not widen or rewrite the queued CCFG-20 runway.
  CCFG-30 remains unselected until a later explicit `plan-batch` request.

## Problem

An explicitly cross-checkout `plan-batch` validates a complete
`cross-checkout-context/v1` payload and persists its exact revisions in the
queued runway. Committing the generated `CURRENT.md`, `LEDGER.md`, `dispatch.md`,
and `runway.md` then advances the stable repository `HEAD` by construction.

At the next `work-batch` flight, the installed helper correctly rejects the
persisted revisions because they no longer equal live `HEAD`. Generic recovery
then treats the queue-establishing planning commit as unexpected repository
movement even though that commit is the normal handoff between the two flights.

The same lifecycle occurred twice:

- CCFG-19 persisted stable revision `e1946ad`, was queued by planning commit
  `bb5701f`, and executed successfully only after regenerating the strict
  context from live revisions.
- CCFG-20 persisted stable revision `7c1c027`, was queued by planning commit
  `9833e92`, and reproduced the same startup mismatch before Slice 1.

The defect is not the helper's exact revision check. That check is useful after
execution has acquired a live context and before a worker or reviewer acts. The
defect is treating a durable plan-time snapshot as the execution-time lease for
a later flight.

## Desired Outcome

Separate four lifecycle concepts and give each one explicit semantics:

| Concept | Lifetime | Purpose | Revision rule |
|---|---|---|---|
| Planning snapshot | Durable in the queued runway | Record the roots, generation, scope, and revisions used to create the plan | Historical evidence; it may differ from a later live `HEAD` |
| Startup reconciliation | Once when `work-batch` consumes queued work | Review all changes since the planning snapshot and decide whether the runway is still executable | Compatible ancestry may advance; conflicting drift stops |
| Execution lease | Short-lived and regenerated from live repositories | Bind one worker or reviewer handoff to exact roots and revisions | Every revision must equal live `HEAD` |
| Execution receipt | Durable after an accepted action | Record the exact lease and scope actually used | Immutable evidence for that action |

The queued runway remains authoritative for selected scope. Repository movement
between flights does not silently broaden, replace, or invalidate that selection.

## Decisions

### 1. Preserve Exact Validation

Keep `parse_cross_checkout_context` fail-closed. A strict
`cross-checkout-context/v1` used for delegation must continue to require exact
live repository revisions, generation binding, Codex home identity, and write
scope.

Do not weaken exact revision comparison to ancestry-only comparison. Ancestry
is sufficient for startup reconciliation, not for an active execution lease.

### 2. Treat Persisted Context As A Planning Snapshot

`plan-batch` and Batch Runway create-spec guidance must state that the complete
payload persisted in a runway proves the planning baseline. It is not promised
to remain a valid strict context after the plan artifacts are committed or
after other between-flight commits land.

Do not update the queued runway merely to replace its recorded revisions with
the commit that contains the runway. That creates another commit and repeats the
self-reference problem.

### 3. Add Normal Startup Reconciliation

Before parsing a queued runway's stored payload as the live execution context,
`work-batch` must:

1. Confirm through Planning State Diagnostic that the same runway is still the
   only queued or active batch.
2. Capture stable and implementation `HEAD`, branch, worktree status, installed
   helper path, active Codex home, and generation role.
3. Compare each live revision with the corresponding planning-snapshot revision.
4. Inspect every intervening commit and changed path when a revision advanced.
5. Classify the movement using the rules below.
6. Stop before delegation if the classification is conflicting or unknown.
7. Ask the helper to prepare and validate a fresh strict payload from the live
   revisions after the movement is accepted.

This is the normal queued-to-executing transition. It must run before generic
unexpected-movement recovery.

### 4. Use Three Startup Classifications

Classify revision movement as exactly one of:

- `expected-queue-establishment`: the stable range changes only the canonical
  active-state files and the same queued batch's `dispatch.md` and `runway.md`,
  and Planning State Diagnostic still identifies that runway. Adopt live
  revisions without recording an orchestration anomaly.
- `compatible-between-flight-change`: any number of commits may exist, but the
  reviewed ranges do not change the selected runway, its source finding or
  acceptance contract, the installed helper or execution-contract owners, the
  declared repository/generation roots, or files inside pending implementation
  scope. Adopt live revisions and record a compact startup reconciliation note.
- `conflicting-between-flight-change`: a change alters or overlaps any of those
  controlled surfaces, changes repository identity or generation binding,
  invalidates a declared baseline, introduces a dirty-file conflict, or cannot
  be classified confidently. Stop and require an explicit runway amendment or
  replanning decision.

Derive controlled paths from the active planning state, queued runway, manifest,
installed helper ownership, and active slice allowlists. Generic skills must not
hard-code codex-config paths or project-specific command names.

### 5. Add Helper-Owned Refresh Preparation

Extend `scripts/cross_checkout_context.py` with a mechanical refresh-preparation
operation. It must:

- validate the payload's exact shape, absolute roots, repository identities,
  generation binding, Codex home, and mutation policy without pretending stale
  revisions equal live `HEAD`;
- capture current revisions for the three declared repository roles;
- return both the planned and live revision sets;
- build a refreshed context and pass it through the existing strict parser
  before returning it; and
- expose the exact refreshed payload for worker and reviewer handoffs.

The helper must not decide whether intervening commits are compatible, select
work, accept execution, authorize writes, or record closeout. Those lifecycle
decisions remain with the coordinator behind `work-batch`.

### 6. Recheck The Lease Before Every Handoff

After startup reconciliation, keep the current behavior of validating immediately
before each worker and reviewer handoff. Candidate slice commits and stable
planning-receipt commits intentionally move revisions, so the coordinator must
prepare a new live lease for the next handoff.

Movement after a lease was prepared, or movement that is not explained by an
accepted coordinator commit, remains unexpected. Freeze delegation and use the
existing recovery lane in that case.

### 7. Keep Receipts Honest

Execution receipts must record the live execution lease, not the plan-time
snapshot. Startup reconciliation evidence must record:

- planned stable and implementation revisions;
- accepted live stable and implementation revisions;
- classification;
- reviewed commit ranges and changed-path basis; and
- the queued runway path.

Keep this evidence compact in the concrete execution ledger or completed-slice
archive. Do not rewrite historical planning snapshots.

## Implementation Surfaces

The future batch should limit changes to these owners unless planning finds a
concrete dependency:

- `skills/work-batch/SKILL.md`
  - own the queued-to-executing reconciliation decision and stop behavior.
- `skills/plan-batch/SKILL.md`
  - label persisted revision data as a planning snapshot.
- `skills/batch-runway/references/cross-checkout-context-v1.md`
  - define snapshot, startup reconciliation, live lease, and receipt semantics.
- `skills/batch-runway/references/create-spec.md`
  - require planning-snapshot wording without self-referential refreshes.
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
  - route normal startup refresh and per-handoff lease regeneration.
- `skills/batch-runway/references/execute-recovery-v1.md`
  - reserve anomaly treatment for post-lease or unclassified movement.
- `scripts/cross_checkout_context.py`
  - provide helper-owned refresh preparation while preserving strict parsing.
- `tests/test_cross_checkout_context.py`
  - exercise mechanical refresh preparation and unchanged strict rejection.
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_codex_features_manifest.py`
  - protect the cross-flight ownership and routing contract.
- `docs/workflow-guide.md`
  - explain that committing a queued plan is a normal flight boundary.
- `codex-features.json`, `CHANGELOG.md`, and installed-state metadata required by
  the affected feature versions.

## Regression Scenarios

The implementation must prove all of these cases:

1. An uncommitted queued runway whose snapshot still equals `HEAD` starts
   normally.
2. A single commit containing only `CURRENT.md`, `LEDGER.md`, `dispatch.md`, and
   `runway.md` is classified as `expected-queue-establishment`.
3. Several compatible commits between flights are reviewed, adopted, and
   represented in the live lease.
4. A stable commit changing the installed helper or execution-contract owner
   stops before refresh acceptance.
5. An implementation commit overlapping a pending slice's allowed files stops
   for amendment or replanning.
6. Unrelated dirty files are preserved when they do not conflict; conflicting
   dirty files stop execution.
7. A live lease passes strict parsing immediately after refresh.
8. A repository moving after lease preparation fails closed before delegation.
9. A candidate slice commit followed by a reviewer handoff uses a newly prepared
   lease rather than the original planning snapshot.
10. Historical CCFG-19 and CCFG-20 payload shapes remain readable as planning
    evidence without being mistaken for current execution leases.

## Validation

The future implementation batch must run:

- focused cross-checkout unit tests;
- batch lifecycle and manifest contract tests;
- Ruff over changed Python tests and helper code;
- basedpyright over `scripts/cross_checkout_context.py`;
- `git diff --check` including explicit review of every new untracked file;
- `./install.sh --status` and `./install.sh --dry-run`; and
- an end-to-end temporary-repository repro covering plan snapshot, plan commit,
  startup reconciliation, live lease, and post-lease movement rejection.

No new validation may silently replace the accepted known-red manifest baseline
with a required-green gate unless the future runway owns that remediation.

## Acceptance Criteria

- A plan-artifact commit no longer causes a false unexpected-`HEAD` anomaly.
- Between-flight commits are permitted after explicit compatible/conflicting
  classification; there is no blanket requirement that live `HEAD` equal the
  prior work-batch closeout commit.
- The queued runway remains the sole selected scope throughout reconciliation.
- Exact revision validation still guards every write-bearing or review handoff.
- The coordinator never hand-edits revision fields by inspection.
- Planning snapshots and execution receipts remain durable and distinguishable.
- Generic reusable skills remain project-neutral.
- CCFG-20 is not widened, replaced, or reopened by this finding.

## Non-Goals

- Do not weaken strict root, revision, generation, Codex home, or write-scope
  validation.
- Do not make arbitrary intervening changes automatically safe.
- Do not infer a new batch from this note or select CCFG-30 during intake.
- Do not modify the current CCFG-20 dispatch, runway, implementation checkout,
  or closeout state.
- Do not accelerate CCFG-26 ownership transfer or CCFG-29 bridge deletion.
- Do not add codex-config-specific paths or commands to reusable skill logic.

## Stop Conditions

- Stop planning if the future batch would relax strict delegation-time identity
  instead of adding the missing lifecycle transition.
- Stop execution if a changed range cannot be classified from concrete paths
  and commits.
- Stop if the fix requires rewriting an active queued runway's historical
  revisions to chase `HEAD`.
- Stop if the work overlaps CCFG-20 before its same-batch closeout.
- Stop if helper refresh preparation acquires selection, compatibility,
  execution-acceptance, or closeout authority.
