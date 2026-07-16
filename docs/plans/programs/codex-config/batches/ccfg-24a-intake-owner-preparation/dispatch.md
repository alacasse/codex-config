# CCFG-24A Intake Owner Preparation Dispatch

## Selection

- Batch ID: `ccfg-24a-intake-owner-preparation`
- Batch state: `queued`
- Source finding: CCFG-24, Transfer Intake Ownership to `add-to-ledger`
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Two-batch boundary:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`
- Accepted decision amendment:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`
- Historical blocked attempt: `blocked-dispatch.md`, `blocked-runway.md`, and
  `execution-report.md`
- Current runway: `runway.md`

## Replacement Decision

This dispatch supersedes only the blocked CCFG-24A planning attempt. It does not
replace the historical execution report or change the finding boundary.

The original attempt treated different complete upstream intake requests as if
DEC-037 required `ledger-store/v1` to distinguish them after they collapsed to
the same mechanical apply request. The accepted amendment resolves that
contract-layer mismatch: the command owner reevaluates source semantics against
the current ledger, prepares the exact store operation, and derives the store
idempotency key internally. The apply-only store continues to bind exact apply
replay and remains unchanged.

## Goal

Prepare and prove one bounded candidate `add-to-ledger/v1` owner that:

- accepts supported source material without public digest or replay fields;
- binds explicit root, generation, ledger, CAS, and mutation-authority facts;
- owns source canonicalization, exact duplicate/update/merge/no-op/block
  decisions, complete-snapshot ID allocation, and internal key derivation;
- calls the unchanged apply-only `ledger-store/v1`;
- is candidate-installed and exercised only against temporary or fixture
  ledgers;
- binds the relevant CCFG-23 intake scenarios to the installed owner;
- leaves compact cost and retained-surface evidence for a later reassessment.

Successful closeout leaves CCFG-24 `Prepared`, not `Closed`.

## Included Work

1. Implement the real command owner from the accepted decision amendment,
   including focused direct behavior and failure-path tests.
2. Register and candidate-install only the required `add-to-ledger` and neutral
   planning-contract feature links after clean source review.
3. Bind installed-owner scenarios for create, atomic multi-create, semantic
   no-op, update, controlled merge/block behavior, stale CAS, unsupported
   source, exact prepared-operation retry, and no downstream planning effects.
4. Inventory every retained APR, `legacy-removal`, and CCFG-23 intake surface
   with caller, reason, removal owner, and removal condition.
5. Record execution time, coordinator context when available, test-process
   count, changed-file count, line delta, and diff-size evidence.

## Explicitly Deferred

- Fixture or helper deletion.
- APR intake, normalization, or mutation-authority narrowing.
- `legacy-removal` narrowing.
- Final source-boundary migration guards.
- Canonical planning mutation by candidate code or candidate-installed tests.
- Stable-home installation or default-generation changes.
- Final CCFG-24 cutover or complete COR-007 acceptance.
- Any CCFG-24B dispatch or runway.
- Any CCFG-25 work.

## Batch Kind And Slice Shape

- Batch kind: `migration`.
- Slice 1: `migration` — implement, directly prove, register, and
  candidate-install the bounded owner over the unchanged store.
- Slice 2: `migration` — bind the installed owner to behavioral scenarios and
  collect preparation and retained-surface evidence.

`1 -> 2`: Slice 1 produces one reviewed candidate-installed owner and direct
behavior boundary. Slice 2 consumes that exact installed owner in the broader
scenario harness and produces a separately reviewable integration/evidence
commit. The intermediate state is valid: the owner works against temporary
ledgers while old intake paths remain unchanged.

No decision-only, contract-narrowing, or destructive-cleanup slice remains.

## Owner And Store Boundaries

- `add-to-ledger/v1` owns source identity, normalization, semantic duplicate
  handling, finding allocation, mutation preparation, and command receipts.
- `ledger-store/v1` owns only exact apply replay, CAS, revision validation,
  deterministic rendering, and atomic replacement.
- `scripts/planning_contract.py`, planning schemas, APR, `legacy-removal`,
  `plan-batch`, `work-batch`, and Batch Runway support remain semantically
  unchanged.
- No public SHA-256 digest, idempotency key, request ID, or replay token may be
  added to the human-facing command.

## Cross-Checkout Guardrails

- Toolchain and canonical planning repository:
  `/home/alacasse/projects/codex-config`
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Stable Codex home: `/home/alacasse/.codex`
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`
- Interface: `cross-checkout-context/v1`

At execution startup, `work-batch` must confirm this exact queued runway through
Planning State, obtain a fresh ready live-lease preflight, and validate exact
write scope before every worker or reviewer handoff. Candidate work and
candidate-installed execution use only temporary or fixture ledgers with
canonical mutation false. Candidate code and the candidate-installed command
must not read for mutation or write canonical planning state. Stable-home and
product-command canonical mutations remain forbidden until cutover; the stable
coordinator may update only this batch's execution ledger, closeout artifacts,
`CURRENT.md`, and `LEDGER.md` when the controlling `work-batch` contract and a
fresh strict-context scope authorize those writes.

## Validation Class

- Runway density: `full-runway` because the batch changes a human-facing
  command owner and spans candidate installation.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Existing planning-store, schema, skill-contract, behavioral/catalog,
  routing, strict cross-checkout, installer, Ruff, BasedPyright, and whitespace
  baselines are `required-green` or retain their explicitly recorded existing
  baseline class.
- Every test-changing slice receives independent review followed by delta-only
  `test-quality-review`.
- Slice 1 and final range require `import_topology_reviewer`.
- Slice 2 and final range require `dead-surface-audit` only for inventory and
  retention classification; deletion is forbidden.

## Closeout Contract

Closeout must record:

- accepted decision record path;
- candidate implementation commit range and installed links;
- direct and scenario validation results;
- create, multi-create, no-op, update/merge/block, stale, unsupported, recovery,
  and no-downstream-effect evidence;
- execution duration, context when available, test-process count, changed-file
  count, line delta, and diff size;
- retained-surface caller/reason/removal-owner/removal-condition inventory;
- CCFG-24 as `Prepared` with selected, queued, and active same-batch state
  cleared;
- no selected or created successor.

## Stop Conditions

- Stop if implementation requires a public caller-supplied replay identity.
- Stop if DEC-037 or `ledger-store/v1` semantics must change.
- Stop if supported source mapping, ID allocation, or duplicate/merge behavior
  requires policy beyond the accepted amendment.
- Stop if candidate code or validation can mutate canonical planning state.
- Stop on stable-home mutation, strict-context mismatch, or repository movement.
- Stop if old intake routes must be deleted or narrowed to turn validation green.
- Stop if retained surfaces cannot be classified completely.
- Stop if work enters CCFG-24B or CCFG-25.
- Stop after same-batch closeout with CCFG-24 `Prepared`.
