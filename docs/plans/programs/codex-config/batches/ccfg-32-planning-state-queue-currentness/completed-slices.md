# CCFG-32 Completed Slices

## Slice 1: Delete Git-Derived Queue Currentness

- Status: completed.
- Commit: `7ef07dc` (`refactor: make planning state own queue currentness`).
- Files: the 11 declared helper, workflow-contract, behavioral-test, feature
  metadata, and changelog paths.
- Validation: cross-checkout tests passed with 32 tests and 37 subtests;
  lifecycle guards passed with 12 tests and 31 subtests; focused manifest
  routing passed with 3 tests, 18 deselected, and 31 subtests; Ruff passed;
  basedpyright reported zero errors, warnings, or notes; installer status and
  dry-run confirmed unchanged linked routing without installation; and
  `git diff --check` passed.
- Known-red diagnostic: the full manifest retained exactly the three named
  baseline failures at 3 failed, 18 passed, and 96 subtests.
- Deletion evidence: queue paths, commit-range and worktree classification,
  planning fingerprints, compatibility arguments, and their preserving tests
  are deleted. Material baseline, identity, movement, lease, scope, result,
  receipt, reviewer-basis, pre-creation, and project-neutral behavior remains.
- Test-quality review: focused review was clean after bounded recovery added
  implementation, toolchain, and independent canonical-planning movement
  during preparation.
- Dead-surface audit: clean; no unsupported compatibility or topology residue.
  Both retained helper APIs have named callers and CCFG-29 as their removal
  condition.
- Independent review: clean before commit and clean over exact range
  `6ede5b2d56bf27939a6ccc0526a0178ee6a58eea..7ef07dc`.
- Outcome: Planning State is the sole semantic queue-currentness authority; the
  helper retains only mechanical first-handoff and later lease integrity. The
  combined helper/workflow-contract delta is 45 additions and 277 deletions.
