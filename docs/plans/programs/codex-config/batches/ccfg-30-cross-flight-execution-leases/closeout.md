# CCFG-30 Cross-Flight Execution Leases Closeout

## Outcome

- Batch: `ccfg-30-cross-flight-execution-leases`
- Status: completed
- Covered finding: CCFG-30
- Finding lifecycle result: `Closed`
- Dispatch: `dispatch.md`
- Runway: `runway.md`
- Completed-slice archive: `completed-slices.md`
- Final closeout commit: `this closeout commit`
- Successor selected: no

Cross-checkout planning snapshots are now durable historical evidence rather
than future live leases. `work-batch` owns one normal startup reconciliation
with exactly three classifications, accepts only reviewed queue-establishment
or compatible movement, and obtains a fresh exact helper-validated lease before
every worker and reviewer handoff. Conflicting, unknown, or post-lease movement
remains fail-closed. The redesign candidate, default generation, and installed
link targets were not changed, and no successor work was selected or prepared.

## Repository Identity And Commits

```yaml
stable_generation:
  repository_root: /home/alacasse/projects/codex-config
  branch: master
  planning_baseline: 7220a2e78a7ad50550cd7bc7ffcfd328301d8e7f
  queued_planning_commit: 61871e6abf269f0e0e53f5a47db9a9cc242318ac
  canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
  codex_home: /home/alacasse/.codex
  canonical_state_mutation_allowed: true
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  unchanged_head: 3e54155964e92d3a4dced8268cc683baaab9be1c
  default_generation: false
default_generation_switched: false
installation_performed: false
```

| Work item | Commit | Outcome |
|---|---|---|
| 1. Helper refresh preparation | `d8f39528197d64a39d31b3ff6f141a60be23ef8b` | Mechanical planned/live facts, strict refreshed parsing, and temporary-repository proof |
| 2. Planning snapshot contract | `387e108d3c944a4146843145adfb445eb6f19cc5` | Immutable planning-snapshot vocabulary and producer guards |
| 3. Startup reconciliation and live leases | `a5a464bc81dee85c543208b81790cbbb3002fe96` | Exactly three classifications, reviewed-path acceptance, live leases, receipts, and recovery routing |
| 4. Joined routing and metadata | `afbe95f910c257fa7486759c1e6b91138e8c88e4` | Joined manifest proof, feature versions, workflow guide, and changelog |
| Final-range scenario-1 repair | `7917ace241f57ae6e5b5dc4e65e7cfa0548588d8` | Narrow validated uncommitted queue-artifact startup case; other controlled dirty paths remain conflicting |

Implementation range:
`d8f39528197d64a39d31b3ff6f141a60be23ef8b^..7917ace241f57ae6e5b5dc4e65e7cfa0548588d8`.

## Regression Scenario Evidence

| Scenario | Result | Evidence |
|---|---|---|
| 1. Uncommitted queued runway at unchanged `HEAD` | Passed | Narrow Planning-State-validated queue-artifact case in `work-batch`; direct lifecycle guard |
| 2. Queue-establishing planning commit | Passed | Startup reconciliation classifies only active-state plus same-batch dispatch/runway movement as `expected-queue-establishment` |
| 3. Reviewed compatible commits | Passed | `compatible-between-flight-change` requires complete commit-range and changed-path review before refresh |
| 4. Helper or execution-contract owner changed | Passed | Controlled-owner overlap routes to `conflicting-between-flight-change` and stops |
| 5. Pending implementation allowlist overlap | Passed | Pending allowlists are controlled paths and fail closed on overlap |
| 6. Unrelated versus conflicting dirty files | Passed | Unrelated dirt is preserved; only the bounded queue-artifact exception is allowed among controlled dirty paths |
| 7. Strict lease immediately after refresh | Passed | `prepare_cross_checkout_context_refresh(...)` reparses the refreshed payload through the unchanged strict parser |
| 8. Movement after lease preparation | Passed | Temporary-repository test rejects post-preparation movement before delegation |
| 9. Fresh reviewer lease after accepted commit | Passed | Execution core and `work-batch` require refresh immediately before every worker and reviewer handoff |
| 10. Historical CCFG-19/CCFG-20 payload shape | Passed | Candidate-shaped historical payload test treats v1 data as planning evidence, never as a current lease |

## Validation And Review

- Helper and lifecycle final suite: 39 passed and 61 subtests passed.
- Joined focused manifest subset: 3 passed, 18 deselected, and 164 subtests
  passed.
- Ruff: passed over every runway-named Python and test file.
- basedpyright: zero errors, warnings, or notes for
  `scripts/cross_checkout_context.py`.
- `git diff --check`: passed, including explicit `git diff --no-index` review
  of the new completed-slice archive.
- `./install.sh --status`: every affected installed surface remains linked to
  the stable checkout.
- `./install.sh --dry-run`: no installed state was written; it reported only
  the declared source version advances (`plan-batch` 1.0.6, `work-batch`
  1.0.7, and `batch-runway` 1.5.2).
- Full manifest diagnostic remained exactly the accepted three failures and
  18 passes, with 229 subtests. The same unrelated exact-wording tests failed:
  `test_executable_work_source_boundary_is_explicit`,
  `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
  `test_work_batch_reconciles_same_batch_closeout`.
- Every test-changing slice and the final repair received delta-only
  test-quality review. All final specialist verdicts were clean.
- Every slice received independent final review. Review findings were corrected
  in bounded loops and re-reviewed clean.
- Independent final review over the exact complete range plus concrete receipts
  was clean with no findings, residual risks, or required fixes.
- The redesign candidate remained clean and unchanged at
  `3e54155964e92d3a4dced8268cc683baaab9be1c`.

## Cleanup And Temporary Surface Classification

- Removed: no unsupported alias, fallback parser, parallel classifier,
  project-specific reusable routing, or receipt topology lock remains.
- Kept intentionally: `cross-checkout-context/v1` and the stable linked helper
  remain the temporary bridge required by current cross-checkout workflows.
  CCFG-29 is the explicit removal condition.
- Kept intentionally: installed registry version metadata remains at its prior
  values because installation was outside this batch. The linked content is
  current; a later explicitly authorized install may record the three source
  version advances without changing ownership or generation.
- Deferred: CCFG-21 through CCFG-29, candidate cutover, default-generation
  switching, bridge deletion, and the three unrelated manifest wording
  failures remain outside this batch and unselected.

## Same-Batch Program Reconciliation

- CCFG-30 is `Closed` from the implementation commits, all ten regression
  scenarios, final validation, and clean independent range review.
- Selected dispatch, queued batch, and active runway are `None` after
  reconciliation.
- `latest_closeout` points to this file.
- `ccfg-30-cross-flight-execution-leases` is completed in the batch queue.
- No successor batch, dispatch, runway, refresh, or preparation occurred.

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

Review findings and their bounded fix loops followed the normal recovery
contract; no unexpected agent, workspace, `HEAD`, index, or diff-basis movement
occurred.

## Convergence Assessment

- Phase: closure.
- Scope trend: shrinking.
- Closed this batch: planning-snapshot semantics, normal startup
  reconciliation, helper-owned refresh preparation, exact per-handoff leases,
  execution receipts, recovery routing, joined manifest proof, and user-facing
  guidance.
- Newly discovered: the final-range review exposed the uncommitted queue-artifact
  scenario; commit `7917ace` closed it without widening scope.
- Deferred out of scope: CCFG-21 through CCFG-29, candidate cutover, bridge
  deletion, installation, and unrelated known-red wording assertions.
- Remaining unknowns: none for CCFG-30.
- Temporary compatibility paths: the strict cross-checkout bridge remains until
  CCFG-29.
- Cleanup residues: none without a named reason and removal condition.
- Blockers: none.
- Completion forecastable: complete.
- Forecast: no CCFG-30 implementation work remains.
- Evidence: `completed-slices.md`, the five implementation commits, final
  validation, linked-state checks, and the clean exact-range review.
- Next proof required: none for CCFG-30. A later explicit `plan-batch` request
  owns any successor selection.
