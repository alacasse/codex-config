# CCFG-31 Completed Slices

## Slice 1: Add The Mechanical Ready/Blocked Preflight

- Status: completed.
- Commit: `cdcb05e` (`feat: add narrow live-lease preflight`).
- Files: `scripts/cross_checkout_context.py`, `tests/test_cross_checkout_context.py`.
- Validation: focused cross-checkout suite passed with 39 tests and 46
  subtests; Ruff passed; basedpyright reported zero errors, warnings, or notes;
  `git diff --check` passed.
- Test-quality review: delta-only review clean after behaviorally covering
  repository and same-path worktree movement during preflight, observed dirty
  source movement, and unmerged Git state.
- Independent review: clean against the exact worktree diff from
  `284d800deafe1f55c9d10254a4532219b163d9ae`.
- Outcome: the helper now returns only `ready` or `blocked` with a fresh strict
  context on success, while exact queue-transaction evidence and deterministic
  worktree fingerprints keep ambiguous or changing state fail-closed.

## Slice 2: Collapse Consumers And Delete The Broad Protocol

- Status: completed.
- Commit: `401a468` (`refactor: collapse cross-checkout startup protocol`).
- Files: the 12 declared Slice 2 consumer, focused-test, feature metadata,
  workflow guide, and changelog paths.
- Validation: cross-checkout suite passed with 39 tests and 46 subtests;
  lifecycle guards passed with 12 tests and 27 subtests; focused manifest
  routing passed with 3 tests, 18 deselected, and 31 subtests; Ruff passed;
  basedpyright reported zero errors, warnings, or notes; `git diff --check`
  passed; installer status and dry-run confirmed linked ownership without an
  install.
- Known-red diagnostic: the full manifest retained the same three baseline
  failure names at 3 failed and 18 passed; the subtest count fell to 96 because
  authorized prose and topology locks were deleted.
- Dead-surface audit: old movement classifications, compatible-range routing,
  startup-reconciliation lifecycle topology, broad path taxonomy, and copied
  prose locks were deleted or behaviorally migrated; strict parser, snapshot,
  fresh lease, scope, result echo, receipt, pre-creation, project-neutrality,
  and canonical-bridge behavior were retained.
- Test-quality review: focused review clean.
- Independent review: clean against the exact 12-file diff from `cdcb05e`.
- Outcome: command/runtime consumers now keep only their owner-specific
  obligations around one canonical ready/blocked bridge; feature versions are
  `plan-batch` `1.0.7`, `work-batch` `1.0.8`, and `batch-runway` `1.5.4`.
