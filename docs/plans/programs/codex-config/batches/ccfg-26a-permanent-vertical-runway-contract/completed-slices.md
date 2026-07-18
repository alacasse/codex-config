# CCFG-26A Completed Slices

## Slice 1: Queue One Permanently Vertical Migration Plan

- Status: completed.
- Candidate commit: `a0835f146857612dcd5a95053d67c53f32449012`
  (`feat(plan-batch): require vertical migration runways`).
- Implementation range:
  `89671eceb9103039e7e6660e73837827c167a3a1..a0835f146857612dcd5a95053d67c53f32449012`.
- Exact range: 19 changed paths, 934 insertions, 17 deletions, binary diff
  SHA-256
  `6c4c4f7c4459b0943c5c801748ad517e146042034a39cc0ea601d7dadf930b02`.
- Durable result: candidate `plan-batch`, `batch_planner`,
  `batch_plan_reviewer`, the deterministic queue gate, and
  `planning-runway/v1` now use the exact `risk: migration` predicate and one
  compatible vertical contract. Temporary coexistence requires a complete
  non-empty migration matrix; no coexistence requires an explicit empty
  matrix; non-migration slices remain unaffected.
- Focused validation: 141 tests and 173 subtests passed; the selected manifest
  boundary passed 2 tests and 27 subtests; the command-owner catalog validated
  76 scenarios; Ruff passed; configured production BasedPyright reported zero
  findings; `git diff --check` passed.
- Known-red diagnostic: exactly the two declared later CCFG-26 ownership
  assertions remained red with no new failure.
- Reviews: the first delta-only test-quality pass found a missing explicit
  `migration_matrix` regression and the first runway review found empty-list
  schema drift. Both were corrected within Slice 1. Final delta-only
  test-quality and exact-commit runway reviews were clean with no residual risk
  or required fix.
- Installation: a fresh `/tmp` Codex home installed and converged all default
  candidate features. The isolated candidate home converged at
  `planning-contracts 1.1.0`, `custom-agents 1.6.0`, and `plan-batch 2.1.0`;
  every post-install dry-run link was `ok`. Stable-home status SHA-256 remained
  `5037e782b9140f4a5b818a79f6f0afc03bbf376ae7476451eedda5710119619a`.
- Exact acceptance: one evidence-pytest process passed 25 tests and reported
  all 76 scenarios, 31 required contracts, and 17 families green. The canonical
  result report SHA-256 is
  `b20bf563084788e27da2a2b204063d58173fbe5a7c635ddce24393bb0992f1e8`;
  generated `report.json` SHA-256 is
  `4af80be825f83f54db7d432b5c7baff0b1c5510e41ebce0bc413d2b57e83df15`.
- Proportionality: the boundary remained one atomic migration-planning
  scenario across the command, planner, reviewer, deterministic gate, schema,
  and focused proof. Formatter-only churn was removed before acceptance; no
  coordinator compaction occurred.
- Temporary residue: the stable CCFG-34 policy and root hook remain until
  CCFG-29; execution flights and telemetry remain with CCFG-26B through
  CCFG-26E; `work-batch`, Batch Runway, and APR execution/closeout ownership is
  unchanged.
- Successor selected: no.
