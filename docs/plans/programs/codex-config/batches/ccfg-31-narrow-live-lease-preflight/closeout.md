# CCFG-31 Narrow Live-Lease Preflight Closeout

## Outcome

- Batch: `ccfg-31-narrow-live-lease-preflight`
- Status: completed
- Covered finding: CCFG-31
- Finding lifecycle result: `Closed`
- Dispatch: `dispatch.md`
- Runway: `runway.md`
- Completed-slice archive: `completed-slices.md`
- Final closeout commit: `this closeout commit`
- Successor selected: no

The normal coordinator-visible startup result is now exactly:

```yaml
status: ready | blocked
reason: string
live_context: object | null
```

The helper proves exact repository identity and same-batch queue movement,
returns a freshly parsed strict context only for `ready`, and blocks ambiguity
or any unrelated movement. `work-batch` retains planning currentness and every
proceed, stop, recovery, delegation, commit, receipt, closeout, and successor
decision. Strict per-handoff refresh, result echo, separate scope validation,
and actual-lease receipts remain fail-closed.

## Commits

| Slice | Commit | Outcome |
|---|---|---|
| 1. Mechanical ready/blocked preflight | `cdcb05e657246cef5d1a8ad193fec2abc533fddb` | Three-field mechanical result, exact queue transaction proof, deterministic worktree fingerprints, and temporary-repository behavior matrix |
| 2. Consumer collapse and broad-protocol deletion | `401a468158465210130caca8f7d677c135e20b24` | One canonical bridge, thin owner-specific consumers, behavioral test migration, versions, workflow guide, and changelog |

Implementation range:
`284d800deafe1f55c9d10254a4532219b163d9ae..401a468158465210130caca8f7d677c135e20b24`.

## Before And After Complexity

| Surface | Before | After |
|---|---|---|
| Normal startup decision | Three named movement classifications and a compatible-range table | One mechanical `ready` or `blocked` result |
| General movement acceptance | Coordinator commit-range and compatibility review | Any non-transaction movement blocks |
| Path ownership | Broad controlled-path taxonomy | Exact caller-supplied same-batch queue paths |
| Durable lifecycle exposition | Planning snapshot, startup reconciliation, live lease, and receipt | Planning snapshot, live lease, and receipt; no startup lifecycle artifact |
| Consumer contracts | Full lifecycle/classification prose repeated across command, planning, execution, slice, and recovery surfaces | One canonical temporary bridge plus owner-specific obligations |
| Tests | Exact prose, classification-count, section-topology, and broad taxonomy locks | Temporary-repository behavior, schema, ownership, routing, and installation checks |

Slice 2 removed 947 lines while adding 290. Across both implementation commits,
the larger behavioral proof for the new helper is offset by deletion of the
caller-visible protocol and its topology locks; no parallel bridge, status,
taxonomy, scanner, schema, agent, or lifecycle state was added.

## Validation And Review

- Cross-checkout suite: 39 passed and 46 subtests passed.
- Lifecycle guards: 12 passed and 27 subtests passed.
- Focused manifest routing: 3 passed, 18 deselected, and 31 subtests passed.
- Ruff: passed over every runway-named Python and test file.
- basedpyright: zero errors, warnings, or notes for
  `scripts/cross_checkout_context.py`.
- `git diff --check`: passed. The untracked completed-slice archive also had no
  whitespace errors under `git diff --no-index --check`.
- `./install.sh --status` and `./install.sh --dry-run`: every target remains
  linked to this stable checkout; no install or installed-state write occurred.
  Source metadata is now `plan-batch` `1.0.7`, `work-batch` `1.0.8`, and
  `batch-runway` `1.5.4`; installed version records remain at their prior
  values pending separate install authority.
- Full manifest diagnostic: the same three accepted baseline test names remain
  red at 3 failed and 18 passed. The 96 subtests reflect authorized removal of
  old prose and topology locks, not a new failure class.
- Dead-surface audit: every deleted or migrated assertion was classified; no
  `human-contract-decision` remained under issue #53's authorization.
- Test-quality review: delta-only Slice 1 and focused Slice 2/final-range reviews
  were clean after bounded recovery added missing fail-closed behavior tests.
- Independent slice reviews: both clean after the Slice 1 same-path rewrite
  defect was corrected and re-reviewed.
- Independent implementation-range review: clean over
  `284d800d..401a4681`, with only the accepted known-red manifest baseline as a
  residual risk.
- The redesign candidate remained clean and unchanged at
  `3e54155964e92d3a4dced8268cc683baaab9be1c`.

## Cleanup And Temporary Surfaces

- Removed: the three movement classifications, compatible-range acceptance,
  broad controlled-owner taxonomy, fourth startup lifecycle concept, copied
  lifecycle/classification obligations, and exact wording/count/topology tests.
- Kept with reason: `cross-checkout-context/v1` and the linked helper remain the
  one temporary bridge used by strict cross-checkout workflows.
- Removal condition: CCFG-29 final integration remains the sole owner for
  deleting that bridge after candidate cutover and convergence.
- Deferred: CCFG-21 through CCFG-29, installation, generation switching, the
  unrelated approval-rule edit, and the three known-red manifest wording tests
  remain outside CCFG-31 and unselected.
- Excluded surfaces unchanged: historical CCFG-30 artifacts, redesign finding
  packets, agents, installer implementation, and candidate checkout.

## Same-Batch Program Reconciliation

- CCFG-31 is `Closed` from the two implementation commits, final validation,
  clean focused test-quality review, and clean exact-range review.
- Selected dispatch, queued batch, and active runway are `None` after
  reconciliation.
- `latest_closeout` points to this file.
- `ccfg-31-narrow-live-lease-preflight` is completed in the batch queue.
- No successor batch, dispatch, runway, refresh, or preparation occurred.

## Orchestration Anomalies

```yaml
orchestration_anomalies:
  - slice: 1
    severity: low
    category: approval_rule_side_effect
    observed: "Git write approval appended git add and git commit allowances to rules/default.rules."
    impact: "The unrelated tracked rule file became dirty after review."
    action_taken: "Preserved it and excluded it from both CCFG-31 implementation commits and this closeout."
    follow_up: "Review or commit the approval-rule change separately from CCFG-31."
```

## Convergence Assessment

- Phase: closure.
- Scope trend: shrinking.
- Closed this batch: the narrow live-lease preflight, exact queue-transaction
  proof, consumer routing, broad-protocol deletion, behavioral migration,
  versions, guide, and changelog.
- Newly discovered: Slice 1 review exposed missing fail-closed coverage and a
  same-path content rewrite defect; bounded recovery closed both within Slice 1.
- Deferred out of scope: CCFG-21 through CCFG-29, installation, generation
  switching, bridge removal, approval-rule changes, and known-red wording tests.
- Remaining unknowns: none for CCFG-31.
- Temporary compatibility paths: the canonical strict bridge remains until
  CCFG-29.
- Cleanup residues: none without a named reason and removal condition.
- Blockers: none.
- Completion forecastable: complete.
- Forecast: no CCFG-31 implementation work remains.
- Evidence: `completed-slices.md`, both implementation commits, final validation,
  linked-state checks, focused test-quality review, and exact-range review.
- Next proof required: none for CCFG-31. A later explicit `plan-batch` request
  owns any successor selection.
