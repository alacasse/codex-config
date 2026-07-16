# CCFG-24 Two-Batch Execution Amendment

## Decision

CCFG-24 remains one durable finding mapped to COR-007. Its implementation is
split across two separately planned and executed batches to bound coordinator
context and create a deliberate reassessment point.

Do not create a `CCFG-24.5` finding. Batch identity and finding identity are
separate. Batch A left CCFG-24 `Prepared`; only Batch B may close it.

## Superseded Planning

The original five-slice `ccfg-24-intake-ownership-transfer` dispatch and runway
are superseded as executable planning. Their source analysis remains historical
evidence and they must not be selected or executed.

The first CCFG-24A attempt also stopped before implementation. Its facts remain
in `batches/ccfg-24a-intake-owner-preparation/execution-report.md` and commits
`33f7adf`, `c087024`, and `199f4a9`. It must not be resumed.

## Batch A: Intake Owner Preparation

Batch ID: `ccfg-24a-intake-owner-preparation`.

Status: completed by
`batches/ccfg-24a-intake-owner-preparation/closeout.md` in candidate range
`b38570b..3b0941a`.

Batch A completed the expand/preparation side:

1. implemented and candidate-installed the real `add-to-ledger/v1` owner over the
   unchanged apply-only store;
2. bounded v1 to `plain_text` and `github_issue`;
3. bound the four CCFG-23 intake scenarios to that installed owner;
4. recorded validation, runtime, diff, and retained-surface evidence.

Batch A closed with CCFG-24 `Prepared`, cleared same-batch state, and selected no
successor.

## Mandatory Reassessment

The explicit CCFG-24B planning request consumed the compact Batch A closeout and
confirmed the smallest credible cutover. It did not reopen deferred adapter
families or assume the superseded five-slice runway remained authoritative.

The controlling retained-surface decisions are:

- delete `_new_finding` after a fresh zero-caller check;
- migrate the temporary exact-69-scenario topology/count assertion to behavioral
  completeness evidence;
- retain installed-owner scenario adapters only where they are real harness
  callers and do not duplicate owner semantics;
- remove APR intake, normalization, and normal ledger-mutation authority while
  preserving CCFG-25 planning and CCFG-26 execution/closeout responsibilities;
- remove the `legacy-removal` state-owner escape hatch while preserving evidence,
  compatibility decisions, residue classification, and deletion vocabulary;
- reconcile final metadata, routing, installation, tests, and COR-007 acceptance.

## Batch B: Intake Ownership Cutover

Batch ID: `ccfg-24b-intake-ownership-cutover`.

Status: queued.

- Dispatch:
  `batches/ccfg-24b-intake-ownership-cutover/dispatch.md`
- Runway:
  `batches/ccfg-24b-intake-ownership-cutover/runway.md`

Batch B owns only the final cutover side:

1. remove proven obsolete CCFG-23 intake migration residue and topology-only
   tests;
2. remove APR intake, normalization, normal ledger-mutation authority, and any
   remaining `add-to-ledger -> architecture-program-runway` dependency;
3. make `legacy-removal` evidence-only;
4. reconcile manifest, routing, docs, candidate installation, migration guards,
   and complete COR-007 acceptance.

Batch B must preserve APR grouping, selection, queue, dispatch, planning,
execution-support, closeout, and reconciliation responsibilities reserved for
CCFG-25/26. It must preserve `legacy-removal` evidence and classification
semantics.

Batch B may close CCFG-24 only when `add-to-ledger/v1` is the sole intake and
canonical mutation-decision owner, the store remains apply-only, replacement
behavior is green, candidate installation converges, and the final closeout
selects no successor.

CCFG-25 remains blocked until that closeout.

## Context And Orchestration Boundary

The split creates two fresh execution coordinator contexts.

- Batch B consumes the compact Batch A closeout inventory by default.
- It does not reread Batch A worker transcripts or broad redesign history unless
  a named contradiction requires it.
- Every startup and handoff uses strict cross-checkout validation and exact write
  scope.
- Candidate processes cannot mutate canonical planning state.
- Stable Codex-home ownership and default generation remain unchanged.
- Same-batch closeout stops without successor selection.

## Status Effect

- CCFG-24: `Pending`, controlled by queued Batch B.
- Original `ccfg-24-intake-ownership-transfer`: `superseded`.
- Failed CCFG-24A attempt: historical evidence only.
- `ccfg-24a-intake-owner-preparation`: completed.
- `ccfg-24b-intake-ownership-cutover`: queued.
- CCFG-25 through CCFG-29: unchanged and unselected.
