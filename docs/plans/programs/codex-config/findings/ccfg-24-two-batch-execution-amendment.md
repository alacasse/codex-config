# CCFG-24 Two-Batch Execution Amendment

## Decision

CCFG-24 remains one durable finding mapped to COR-007. Its implementation is
split across two separately planned and executed batches to bound coordinator
context, create a deliberate reassessment point, and avoid combining target-owner
design, production implementation, behavioral migration, destructive cleanup,
legacy-owner narrowing, installation convergence, and final acceptance in one
execute context.

Do not create a new `CCFG-24.5` finding. Batch identity and finding identity are
separate. The first batch may close with CCFG-24 `Prepared`; only the second batch
may close CCFG-24 as `Closed`.

## Superseded Planning

The following five-slice batch is superseded as executable planning evidence:

- `batches/ccfg-24-intake-ownership-transfer/dispatch.md`
- `batches/ccfg-24-intake-ownership-transfer/runway.md`

Its source analysis, guardrails, acceptance mappings, and preserved-owner
constraints remain evidence. It must not be executed or used as active queue
state.

## Batch A: Intake Owner Preparation

Expected batch ID: `ccfg-24a-intake-owner-preparation`.

This batch owns the expand side of the migration:

1. consume the accepted command-to-script, source-identity, normalization,
   idempotency, allocation, authority, and semantic-decision rules in
   `ccfg-24a-add-to-ledger-v1-decision-amendment.md`, then implement and
   candidate-install the real `add-to-ledger/v1` owner and neutral
   `planning-contracts` mechanism over the unchanged apply-only store;
2. bind the CCFG-23 intake scenarios to that installed production owner and
   measure implementation and validation cost.

The original three-slice CCFG-24A attempt stopped before implementation and is
preserved as historical evidence in the batch directory. Its executable
planning is superseded by the current two-slice dispatch and runway; the
blocked runway must not be resumed.

Batch A must preserve the existing APR intake route, `legacy-removal` lifecycle
surface, and disposable intake helpers as explicitly temporary rollback and
comparison surfaces. They must not remain the primary acceptance owner after the
production scenarios are bound.

Batch A closeout must:

- mark CCFG-24 `Prepared`, not `Closed`;
- clear selected, queued, and active state;
- record the candidate commit range and installed feature links;
- record the final source mapping and semantic decision matrix;
- record test duration, acceptance duration, changed-file count, and line delta;
- classify every retained APR, `legacy-removal`, and CCFG-23 intake surface with a
  caller, reason, owner, and removal condition;
- stop without selecting or creating Batch B.

## Mandatory Reassessment

After Batch A closeout, a fresh explicit `plan-batch` request must review:

- the implemented command-to-script contract;
- the source identity mapping for direct text, GitHub issues, external tickets,
  and file/path sources actually supported by v1;
- the implemented create/update/merge/no-op/block matrix;
- the changed-file and line counts;
- focused and exact-acceptance runtime;
- retained migration surfaces and caller inventory;
- any implementation discovery that changes the smallest credible cleanup.

The follow-up plan may narrow, split, or block the remaining work. It must not
assume that the superseded five-slice runway remains proportionate.

## Batch B: Intake Ownership Cutover

Expected but unselected batch ID: `ccfg-24b-intake-ownership-cutover`.

Batch B is not planned or queued by this amendment. A later explicit
`plan-batch` request may create it after the mandatory reassessment.

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

The split intentionally creates two fresh execute coordinator contexts. Batch A
must not carry cleanup and cutover instructions that it cannot execute. Batch B
must consume compact Batch A closeout evidence instead of rereading the full
Batch A runway, worker transcripts, or broad repository history by default.

Both batches retain the existing strict cross-checkout safety model:

- stable checkout and default Codex home remain authoritative before cutover;
- candidate work is limited to the command-owner redesign checkout and candidate
  Codex home;
- candidate processes must not mutate canonical planning state;
- every execution startup and handoff requires fresh Planning State and strict
  cross-checkout validation;
- same-batch closeout stops without successor selection.

## Status Effect

After this planning amendment:

- CCFG-24: `Pending`, controlled by queued Batch A;
- original `ccfg-24-intake-ownership-transfer`: `superseded`;
- `ccfg-24a-intake-owner-preparation`: queued for execution; CCFG-24 itself
  remains `Pending`;
- expected Batch B: unselected and without dispatch or runway;
- CCFG-25 through CCFG-29: unchanged and unselected.
