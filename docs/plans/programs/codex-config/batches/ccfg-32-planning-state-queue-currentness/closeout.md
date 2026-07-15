# CCFG-32 Planning-State Queue Currentness Closeout

## Outcome

- Batch: `ccfg-32-planning-state-queue-currentness`
- Status: completed
- Covered finding: CCFG-32
- Finding lifecycle result: `Closed`
- Dispatch: `dispatch.md`
- Runway: `runway.md`
- Completed-slice archive: `completed-slices.md`
- Implementation commit: `7ef07dc`
- Final closeout commit: `this closeout commit`
- Successor selected: no

Planning State `current` and `validate` are now the sole semantic gate for
selected and queued batch currentness. The cross-checkout helper no longer
accepts queue paths, walks Git history, classifies worktree planning paths, or
fingerprints planning files. It retains mechanical repository identity,
implementation-baseline, strict parsing and binding, fresh-revision, and
movement-during-preparation checks for the first handoff. Later accepted
actions still require exact refreshed leases, write-scope validation, result
echo, receipts, and reviewer diff bases.

## Commit

| Slice | Commit | Outcome |
|---|---|---|
| 1. Delete Git-derived queue currentness | `7ef07dc` | Removed Git-derived queue semantics, migrated behavioral protection, published `work-batch` `1.0.9` and `batch-runway` `1.5.5`, and recorded the ownership correction |

Implementation range:
`6ede5b2d56bf27939a6ccc0526a0178ee6a58eea..7ef07dc`.

Combined production-helper and reusable workflow-contract delta: 45 additions
and 277 deletions.

## Validation And Review

- Cross-checkout suite: 32 passed and 37 subtests passed.
- Lifecycle guards: 12 passed and 31 subtests passed.
- Focused manifest routing: 3 passed, 18 deselected, and 31 subtests passed.
- Ruff passed; basedpyright reported zero errors, warnings, or notes.
- `git diff --check` passed. Removed queue-currentness symbols were absent from
  the active helper and workflow-contract surfaces.
- `./install.sh --status` and `./install.sh --dry-run` passed. Every target link
  still resolves to this stable checkout; no installation or installed-state
  write occurred. Installed version records retain their pre-existing lag.
- Full manifest diagnostic: the documented baseline remains exactly 3 failed,
  18 passed, and 96 subtests, with no new failure class.
- Focused test-quality review: clean after bounded recovery added missing
  toolchain and independent canonical-planning movement coverage.
- Dead-surface audit: clean; all delete, migrate, and keep classifications were
  satisfied without unsupported compatibility or topology residue.
- Independent slice review: clean before commit.
- Independent final range review: clean over `6ede5b2d..7ef07dc`, with no
  findings, residual risks, or required fixes.

## Cleanup And Temporary Surfaces

- Removed: queue-transaction parameters, commit-range path collection,
  worktree-path classification, planning fingerprints, helper-only Git
  utilities/imports, copied workflow obligations, and topology-preserving
  tests.
- Kept with reason: `preflight_cross_checkout_live_lease(...)` remains the
  named `work-batch` first-handoff mechanical integrity check.
- Kept with reason: `prepare_cross_checkout_context_refresh(...)` remains the
  later worker/reviewer lease producer after accepted coordinator actions.
- Removal condition: CCFG-29 final integration owns deletion of both temporary
  helper APIs and the strict bridge.
- Deferred out of scope: CCFG-21, CCFG-25, CCFG-29, installation, generation
  switching, the redesign candidate, and the three known-red manifest wording
  tests remain unchanged and unselected.

## Same-Batch Program Reconciliation

- CCFG-32 is `Closed` from implementation commit `7ef07dc`, final validation,
  clean focused test-quality and dead-surface reviews, and clean exact-range
  review.
- Selected dispatch, queued batch, and active runway are `None` after
  reconciliation.
- `latest_closeout` points to this file.
- `ccfg-32-planning-state-queue-currentness` is completed in the batch queue.
- No successor batch, dispatch, runway, refresh, or preparation occurred.

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Convergence Assessment

- Phase: closure.
- Scope trend: shrinking.
- Closed this batch: Git-derived queue currentness, its workflow obligations,
  topology, and preserving tests.
- Newly discovered: focused test-quality review found missing toolchain and
  independent canonical-planning movement coverage; bounded recovery closed it.
- Deferred out of scope: CCFG-21, CCFG-25, CCFG-29, installation, generation
  switching, candidate work, and known-red wording tests.
- Remaining unknowns: none for CCFG-32.
- Temporary compatibility paths: none. The two retained mechanical APIs are
  current workflow surfaces with named callers and a CCFG-29 removal condition.
- Cleanup residues: none without a named reason and removal condition.
- Blockers: none.
- Completion forecastable: complete.
- Forecast: no CCFG-32 implementation work remains.
- Evidence: `completed-slices.md`, `7ef07dc`, final validation, install-link
  checks, focused test-quality/dead-surface reviews, and exact-range review.
- Next proof required: none for CCFG-32. A later explicit `plan-batch` request
  owns any successor selection.
