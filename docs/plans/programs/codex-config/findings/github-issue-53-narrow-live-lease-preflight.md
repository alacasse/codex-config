# GitHub Issue 53: Narrow Ready/Blocked Live-Lease Preflight

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/53
- Title: Simplify CCFG-30 to a narrow ready/blocked live-lease preflight
- State when ingested: open
- Labels when ingested: `ready-for-agent`
- Created: 2026-07-14
- Updated when ingested: 2026-07-14
- Source identity: GitHub issue #53, authored by `alacasse`

## Summary

CCFG-30 fixed the self-referential queue-startup failure by separating immutable
planning evidence from exact live execution identity, but the issue reports that
the implementation expanded the narrow failure into a large coordinator-facing
protocol. The added movement classifications, general commit-range review,
broad controlled-path derivation, repeated lifecycle prose, and Markdown
topology assertions now affect every cross-checkout batch until CCFG-29 removes
the temporary bridge.

This is a simplification and deletion finding. It does not reopen the CCFG-30
historical batch or authorize another lifecycle redesign.

## Source Evidence

- `docs/plans/programs/codex-config/notes/cross-flight-execution-baseline-plan.md`
- `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md`
- `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/closeout.md`
- Issue-reported CCFG-30 implementation range: `6de7789..e5ed7db`
- The issue reports a seven-commit, 20-file change adding roughly 2,247 lines.

## Authoritative Outcome

Replace general startup reconciliation with one narrow mechanical live-lease
preflight whose normal caller-visible result is exactly:

```yaml
status: ready | blocked
reason: string
live_context: object | null
```

- `live_context` is present only for `ready` and must pass the existing strict
  parser at the current live revisions.
- `reason` is diagnostic evidence only. It must not become a movement
  classification, coordinator decision table, lifecycle state, or compatibility
  taxonomy.
- `work-batch` retains currentness, proceed/stop, recovery, delegation, commit,
  receipt, and closeout authority.
- The helper remains mechanical: it validates exact identity and movement,
  produces a fresh strict context only when every condition is proven, and does
  not interpret business scope or mutate planning state.

## Ready/Blocked Boundary

Return `ready` only when all of these are proven:

1. The same queued runway, selected scope, and source work remain current.
2. Stable roots, branches, revisions, generation role, helper identity, and
   `CODEX_HOME` match the planning snapshot and active generation without cwd
   inference.
3. The implementation repository revision has not moved.
4. Canonical planning movement is either absent or limited to the exact current
   batch's queue-establishment transaction.
5. The allowed transaction paths are supplied by current state or the current
   planning transaction and contain only the exact dispatch, runway, and program
   state artifacts written for this batch.
6. A fresh context at the current live revisions passes the strict parser and is
   returned for immediate handoff.

Any missing proof, ambiguity, implementation movement, unrelated planning or
source movement, identity mismatch, stale scope, or arbitrary compatible-range
claim returns `blocked` before delegation.

## Safety Properties To Preserve

- Queued context remains immutable historical planning evidence, not a reusable
  live handoff context.
- A fresh lease is acquired immediately before every worker and reviewer
  handoff and is never reused.
- Movement after lease preparation invalidates the lease before delegation or
  acceptance.
- Strict root, branch, revision, generation, helper, `CODEX_HOME`, result echo,
  and write-scope validation remains fail-closed.
- Accepted-action and commit receipts record the actual live lease and validated
  scope.
- Unrelated dirty files remain preserved and excluded from this change's
  staging, commits, cleanup, and rewrites.

## Required Simplification

Remove or consolidate from the normal path:

- the three movement classifications and their decision table;
- general compatible-range review;
- broad controlled-path derivation and repository-wide path taxonomies;
- startup reconciliation as a fourth durable lifecycle concept or artifact;
- duplicated lifecycle exposition across planning, execution, and recovery
  consumers;
- exact-prose, classification-count, and Markdown-topology tests that do not
  protect observable safety behavior.

`skills/batch-runway/references/cross-checkout-context-v1.md` remains the single
canonical temporary bridge contract. Consumers should keep only their
owner-specific obligations and reference that contract. Do not create a
parallel `v2` compatibility path.

## Scope And Planning Constraints

- Dependencies: none; the issue states that it is independent of #51, #52, and
  #54 and may start immediately.
- Prefer one or two semantic slices and never exceed three. Issue #54 owns the
  permanent removal of generic fixed slice-count guidance.
- Add no new agent, lifecycle state, durable planning artifact or schema,
  movement taxonomy, generalized compatibility engine, repository scanner,
  public command, or reusable abstraction beyond the narrow helper seam.
- Historical CCFG-30 planning artifacts are read-only evidence and must remain
  unchanged.
- The command-owner redesign candidate and CCFG-21 through CCFG-29 remain out
  of scope.
- CCFG-29 remains the sole owner for deleting the cross-checkout bridge.
- Behavioral confidence should come primarily from temporary-repository runtime
  tests and exact runtime facts, with independent `test-quality-review` before
  closeout.

## Intake Decision

- Ledger identity: `CCFG-31`.
- Finding status: `Open`.
- No batch is selected, queued, or active by this intake.
- A future explicit `plan-batch` request owns bounded selection and must honor
  the issue's deletion goal, ownership boundary, preserved safety invariants,
  and three-slice maximum.
