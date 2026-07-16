# CCFG-24B Intake Ownership Cutover Dispatch

## Selection

- Batch ID: `ccfg-24b-intake-ownership-cutover`
- Batch state: `queued`
- Covered finding: CCFG-24, Transfer Intake Ownership to `add-to-ledger`
- Finding state entering the batch: `Prepared`
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Split boundary:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`
- Bounded owner decision:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`
- Preparation evidence: `../ccfg-24a-intake-owner-preparation/closeout.md`
- Current runway: `runway.md`

## Reassessment Result

CCFG-24A proved the candidate-installed `add-to-ledger/v1` owner for
`plain_text` and `github_issue` and left a complete retained-surface inventory.
The smallest credible final cutover is the four bounded workstreams below.

1. Remove only obsolete CCFG-23 intake migration residue:
   - delete `_new_finding` after a fresh zero-caller check;
   - replace the temporary exact-69-ID topology assertion with behavioral
     completeness evidence;
   - retain installed-owner scenario adapters only where they remain real
     behavioral harness callers and do not duplicate owner semantics.
2. Remove APR intake, normalization, and normal ledger-mutation authority while
   preserving grouping, selection, queue, dispatch, planning, execution-support,
   closeout, and reconciliation responsibilities still owned by CCFG-25/26.
3. Make `legacy-removal` evidence-only by removing its program-owner and lifecycle
   state escape hatches while preserving evidence, compatibility decisions,
   cleanup-residue classification, and deletion/dead-surface vocabulary.
4. Reconcile manifest, routing, docs, tests, candidate installation, and final
   COR-007 acceptance.

## Goal

Make `add-to-ledger/v1` the sole intake and canonical ledger-mutation decision
owner, remove the exact replaced ownership and migration surfaces, and close
CCFG-24 without entering CCFG-25.

## Explicit Preservation

- `ledger-store/v1`, DEC-037, `scripts/planning_contract.py`, and planning schemas
  remain unchanged and apply-only.
- `add-to-ledger/v1` remains bounded to `plain_text` and `github_issue`.
- APR continues to support CCFG-25 planning ownership transfer and CCFG-26
  execution/closeout ownership transfer.
- `legacy-removal` remains an evidence and classification producer.
- The four intake scenarios continue to execute the installed owner on fresh
  non-canonical ledgers.
- Stable Codex-home ownership and the default generation remain unchanged.

## Explicitly Deferred

- Generic tickets, file ingestion, cross-source merge, fuzzy matching, and any
  other expansion of `add-to-ledger`.
- APR planning/selection/queue ownership removal, owned by CCFG-25.
- APR and Batch Runway execution/closeout ownership removal, owned by CCFG-26.
- Default-generation switch, bridge removal, and CCFG-27 through CCFG-29 work.
- Any CCFG-25 dispatch, runway, refresh, or successor selection.

## Batch Kind And Slice Shape

- Batch kind: `mixed-risk`.
- Slice 1: `destructive-cleanup` — remove proven obsolete CCFG-23 intake residue
  and migrate topology-only tests.
- Slice 2: `contract-narrowing` — remove APR intake and normal mutation authority.
- Slice 3: `contract-narrowing` — make `legacy-removal` evidence-only.
- Slice 4: `migration` — reconcile metadata, routing, installation, tests, and
  final COR-007 acceptance.

`1 -> 2`: fixture/test cleanup has a separate deletion gate and rollback boundary
from APR public ownership narrowing.

`2 -> 3`: APR and `legacy-removal` retain different future responsibilities and
require independent preservation reviews.

`3 -> 4`: final installation and exact acceptance must consume the completed
semantic topology rather than partially narrowed owners.

## Approval Gates

- Slice 1 may delete only after current caller evidence confirms the target is
  zero-caller or topology-only and replacement behavioral evidence is green.
- Slice 2 may narrow APR only after installed-owner intake scenarios are green and
  every preserved CCFG-25/26 responsibility is named and directly tested.
- Slice 3 may narrow `legacy-removal` only after an evidence-no-state-writes test
  is green and evidence/classification output remains usable.
- Any newly discovered unclassified deletion, contract narrowing, or owner seam
  blocks the affected slice for explicit replanning.

## Cross-Checkout Context

- Interface: `cross-checkout-context/v1`
- Stable toolchain and canonical planning repository:
  `/home/alacasse/projects/codex-config`
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Stable Codex home: `/home/alacasse/.codex`
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`

Every startup and handoff requires a fresh ready strict preflight and exact write
scope. Candidate processes must not mutate canonical planning state.

## Validation And Review

- Runway density: `lean-runway` with explicit risk gates.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`
- Every slice receives independent review and delta-only `test-quality-review`.
- Slices 1 through 3 receive targeted `dead-surface-audit` evidence.
- Slices 2, 3, and the final range receive `import_topology_reviewer` where owner
  or import topology changes.

## Closeout Contract

Successful closeout must:

- prove complete COR-007 acceptance;
- mark CCFG-24 `Closed`;
- record exact removed and preserved surfaces;
- leave `add-to-ledger/v1` as the sole intake/mutation decision owner;
- leave only the three named CCFG-25/26 manifest diagnostics red;
- record final candidate range, installation links, exact acceptance, diff and
  runtime evidence;
- clear selected, queued, and active same-batch state;
- stop without selecting or preparing CCFG-25.

## Stop Conditions

- Stop on any new adapter, merge behavior, store/schema change, or public retry
  identity.
- Stop if a deletion lacks current caller and replacement evidence.
- Stop if APR planning/queue or execution/closeout support would be removed.
- Stop if `legacy-removal` evidence, classification, or deletion vocabulary would
  be removed.
- Stop on stable-home mutation, canonical candidate write, or strict-context
  mismatch.
- Stop if CCFG-24 cannot close without entering CCFG-25 through CCFG-29.
