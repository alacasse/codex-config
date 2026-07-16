# CCFG-24 Two-Batch Execution Amendment

## Decision

CCFG-24 remains one durable finding mapped to COR-007. Its implementation is
split across two separately planned and executed batches to bound coordinator
context and create a deliberate reassessment point.

Do not create a `CCFG-24.5` finding. Batch identity and finding identity are
separate. Batch A may leave CCFG-24 `Prepared`; only Batch B may close it.

## Superseded Planning

The original five-slice `ccfg-24-intake-ownership-transfer` dispatch and runway
are superseded as executable planning. Their source analysis remains historical
evidence and they must not be selected or executed.

The first CCFG-24A attempt also stopped before implementation. Its facts remain
in `batches/ccfg-24a-intake-owner-preparation/execution-report.md` and commits
`33f7adf`, `c087024`, and `199f4a9`. It must not be resumed.

## Batch A: Intake Owner Preparation

Batch ID: `ccfg-24a-intake-owner-preparation`.

Batch A owns only the expand/preparation side:

1. implement and candidate-install the real `add-to-ledger/v1` owner over the
   unchanged apply-only store;
2. support only `plain_text` and `github_issue` in CCFG-24A v1;
3. bind relevant CCFG-23 intake scenarios to that installed owner;
4. measure implementation, validation, context, and retained-surface cost.

Batch A explicitly defers generic tickets, file ingestion, cross-source merge,
fuzzy duplicate detection, fixture deletion, APR narrowing, `legacy-removal`
narrowing, final cutover, and successor planning.

Old intake paths remain available as temporary rollback and comparison surfaces,
but they must not remain the primary acceptance path after scenario migration.

Batch A closeout must:

- mark CCFG-24 `Prepared`, not `Closed`;
- clear selected, queued, and active same-batch state;
- record candidate commits and installed feature links;
- record direct and scenario validation;
- record duration, context when available, changed-file count, line delta, diff
  size, and test-process count;
- classify every retained APR, `legacy-removal`, and CCFG-23 intake surface with
  caller, reason, owner, and removal condition;
- stop without selecting or creating Batch B.

## Mandatory Reassessment

After Batch A closeout, a fresh explicit `plan-batch` request must review only
compact closeout evidence:

- the implemented command-to-script boundary;
- the two implemented source mappings;
- the create/update/no-op/block matrix;
- implementation and test size;
- focused and exact-acceptance runtime;
- retained migration surfaces;
- any implementation discovery that changes the smallest credible cutover.

The follow-up may narrow, split, or block remaining work. It must not assume the
superseded five-slice runway remains proportionate or automatically add deferred
adapter families.

## Batch B: Intake Ownership Cutover

Expected but unselected batch ID: `ccfg-24b-intake-ownership-cutover`.

Batch B has no dispatch or runway. A later explicit `plan-batch` request may
create it only after the mandatory reassessment.

Its expected contract side is:

1. remove replaced CCFG-23 intake helpers and topology-preserving tests after a
   current caller inventory;
2. remove APR intake, normalization, normal ledger-mutation authority, and the
   `add-to-ledger -> architecture-program-runway` runtime dependency while
   preserving CCFG-25 planning and CCFG-26 closeout responsibilities;
3. make `legacy-removal` evidence-only while preserving classification and
   deletion/dead-surface vocabulary;
4. reconcile final manifest, routing, docs, candidate installation, migration
   guards, and complete COR-007 acceptance.

Only Batch B may close CCFG-24. CCFG-25 remains blocked until that closeout.

## Context And Orchestration Boundary

The split intentionally creates two fresh execute coordinator contexts.

- Batch A must not carry cleanup or cutover instructions it cannot execute.
- Batch B must consume compact Batch A closeout evidence instead of rereading the
  Batch A runway, worker transcripts, or broad repository history by default.
- Active CCFG-24A execution should read current state, its dispatch/runway, the
  compact decision amendment, and the active slice only.

Both batches retain strict cross-checkout safety: stable control before cutover,
candidate-only implementation and install, no canonical planning mutation by
candidate processes, fresh validation at startup and every handoff, and no
successor selection during same-batch closeout.

## Status Effect

- CCFG-24: `Pending`, controlled by queued Batch A.
- Original `ccfg-24-intake-ownership-transfer`: `superseded`.
- Failed CCFG-24A attempt: historical evidence only.
- Current `ccfg-24a-intake-owner-preparation`: queued for execution.
- Expected Batch B: unselected and without dispatch or runway.
- CCFG-25 through CCFG-29: unchanged and unselected.
