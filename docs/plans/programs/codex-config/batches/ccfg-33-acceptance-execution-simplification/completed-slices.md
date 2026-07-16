# CCFG-33 Completed Slices

## Slice 1: Simplify Exact-Commit Acceptance Execution

- Status: completed.
- Commit: `b38570b` (`refactor: simplify command-owner acceptance execution`).
- Files: exactly the nine declared schema, harness, catalog, focused-test,
  configuration, and changelog paths.
- Validation: the fast gate passed with 14 tests and one deselection; the
  acceptance-marker gate passed with 14 tests and 30 deselections; catalog
  validation accepted all 69 scenarios; Ruff passed; BasedPyright reported
  zero errors with five dependency-source warnings; and range whitespace
  passed.
- Final focused suite: 115 passed in 60.02 seconds, versus 123 passed in 814.32
  seconds at baseline, a 13.6x speedup and 92.6% wall-time reduction.
- Exact-commit acceptance: one coordinator-owned execution completed in 48.03
  seconds total and 29.894864 seconds inside its evidence run. It launched one
  evidence-pytest process for all 13 declared nodes and recorded 25 passing
  tests with no failures, errors, skips, deselections, xfail, or xpass.
- Preserved behavior: 69 scenario meanings, 31 required and green contracts,
  17 families, six keys, six aliases, negative-runtime outcomes, and provenance
  checks remained green. JSON and text rendered from the same accepted report
  with zero formatting subprocesses.
- Cost evidence: evidence-pytest processes per report fell from 13 to one;
  catalog evaluations per report fell from four to one process-local,
  input-bound evaluation. External child-process counting was unavailable, so
  no replacement count was inferred for the approximately 41,125-process suite
  baseline.
- Known-red diagnostic: exactly the same three named failures remained, with
  18 passes and 202 passing subtests.
- Deletion evidence: per-function `source_sha256`, AST/source extraction,
  offline result ingestion, reporter-owned recursive pytest, and their
  topology-preserving tests were removed. The private generated result retains
  only exact input/environment identity, exclusive pytest outcomes, one process
  count, duration, and a digest binding to its same-process report.
- Size: the schema, harness, catalog, and focused tests changed by 822 additions
  and 861 deletions, net negative 39 lines. The full nine-file commit changed by
  844 additions and 861 deletions, net negative 17 lines.
- Reviews: post-commit exact-range test-quality review was clean. The final
  independent reviewer was clean across behavior, contract, test, import
  topology, cleanup, and validation/reporting lenses; its timing-only residual
  was resolved when the parallel test-quality result arrived clean.
- Outcome: acceptance now has one exact-commit execution owner, evaluation
  reuse is process-local and input-bound, report formatting is pure, raw caller
  outcomes cannot self-certify, and no permanent cache, public outcome seam,
  receipt schema, committed receipt, CI workflow, production transfer, or
  cutover change was introduced.
