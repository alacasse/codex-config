# CCFG-26A Permanent Vertical Runway Contract Closeout

## Outcome

- Batch: `ccfg-26a-permanent-vertical-runway-contract`
- Status: completed
- Covered finding: CCFG-26
- Finding lifecycle result: `Prepared`
- Dispatch: `dispatch.md`
- Runway: `runway.md`
- Completed-slice archive: `completed-slices.md`
- Candidate baseline: `89671eceb9103039e7e6660e73837827c167a3a1`
- Candidate implementation commit:
  `a0835f146857612dcd5a95053d67c53f32449012`
- Stable execution-receipt commit:
  `5935b43` (`docs(ccfg-26a): record vertical contract slice receipt`)
- Final closeout commit: `this closeout commit`
- Canonical planning root: `/home/alacasse/projects/codex-config/docs/plans`
- Implementation root:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Successor selected: no

CCFG-26A completes permanent issue #60 vertical-planning behavior in the
candidate generation. `plan-batch`, `batch_planner`, `batch_plan_reviewer`, the
deterministic queue gate, and `planning-runway/v1` now share one exact
`risk: migration` applicability predicate, vertical slice contract, and caller
migration matrix. Candidate planning is integration-ready but remains
non-authoritative for canonical planning until CCFG-29.

CCFG-26 remains `Prepared`, not `Closed`. CCFG-26B through CCFG-26E retain the
fresh execution-flight, bounded recovery, finalization, and closeout ownership
work from issues #59/#61 and COR-009. They remain unselected and require later
explicit stable `plan-batch` invocations under the temporary CCFG-34 policy.

## Commit

| Slice | Commit | Outcome |
|---|---|---|
| 1. Queue one permanently vertical migration plan | `a0835f1` | Added the permanent candidate vertical planning contract, exact deterministic and schema gates, planner/reviewer ownership, focused behavioral scenarios, and feature metadata. |

Implementation range:
`89671eceb9103039e7e6660e73837827c167a3a1..a0835f146857612dcd5a95053d67c53f32449012`.

The range changes 19 paths with 934 insertions and 17 deletions. Its binary
diff SHA-256 is
`6c4c4f7c4459b0943c5c801748ad517e146042034a39cc0ea601d7dadf930b02`.

## Validation And Review

- Focused final validation passed 141 tests and 173 subtests.
- The selected manifest boundary passed 2 tests and 27 subtests.
- The command-owner catalog validated all 76 scenarios.
- Ruff passed; configured production BasedPyright reported zero findings for
  `scripts/plan_batch.py`; exact-range whitespace validation passed.
- The declared known-red diagnostic reproduced exactly the two later CCFG-26
  ownership assertions with no additional failure.
- Delta-only test-quality review first identified missing explicit
  `migration_matrix` coverage. The paired deterministic and schema regressions
  were added, and the final delta-only review was clean.
- Independent runway review first identified empty-list drift between
  `planning-runway/v1` and the deterministic gate. The schema and paired tests
  were corrected; final exact-commit review was clean with no residual risk or
  required fix.
- Exact acceptance bound clean commit `a0835f1`, used one evidence-pytest
  process, passed 25 tests, and reported 76 scenarios, 31 required contracts,
  and 17 families green. The canonical result report SHA-256 is
  `b20bf563084788e27da2a2b204063d58173fbe5a7c635ddce24393bb0992f1e8`;
  generated `report.json` SHA-256 is
  `4af80be825f83f54db7d432b5c7baff0b1c5510e41ebce0bc413d2b57e83df15`.

## Installation Evidence

- A fresh `/tmp` Codex home installed all default candidate features and a
  post-install dry run reported every managed link `ok`.
- The isolated candidate home converged at `planning-contracts 1.1.0`,
  `custom-agents 1.6.0`, and `plan-batch 2.1.0`; every post-install dry-run link
  was `ok`.
- Stable-home status was byte-for-byte unchanged before and after candidate
  installation, with SHA-256
  `5037e782b9140f4a5b818a79f6f0afc03bbf376ae7476451eedda5710119619a`.
- No default-generation switch or canonical-planning mutation occurred.

## Removed And Preserved Surfaces

| Surface | Classification | Evidence and condition |
|---|---|---|
| Formatter-only churn in six candidate Python/test files | removed | Surgical same-slice correction restored the pre-existing format before validation and review; the accepted diff is semantic-only. |
| Stable CCFG-34 policy and root hook | kept temporarily | Stable CCFG-26 through CCFG-29 planning/execution still requires the temporary policy. CCFG-29 removes it only after permanent #59/#60/#61 parity and integration. |
| `work-batch`, Batch Runway, and APR execution/closeout ownership | kept | CCFG-26A changes planning behavior only. CCFG-26B through CCFG-26E own execution flights, recovery, finalization, closeout, and the final ownership transfer. |
| Per-flight execution telemetry | deferred | CCFG-26B through CCFG-26E own durable flight evidence and final closeout. |

No unclassified cleanup residue or compatibility path remains in CCFG-26A.

## Same-Batch Program Reconciliation

- CCFG-26A is completed from candidate commit `a0835f1`, stable receipt commit
  `5935b43`, final validation, installation evidence, exact acceptance, and
  clean final reviews.
- Parent finding CCFG-26 is `Prepared`, not `Closed`.
- Selected dispatch, queued batch, and active runway are `None`.
- `latest_closeout` points to this file.
- `ccfg-26a-permanent-vertical-runway-contract` is completed in the batch queue.
- CCFG-26B through CCFG-26E remain candidate batches with no dispatch or runway.
- CCFG-27 through CCFG-29 remain open and unselected.
- No successor batch, dispatch, runway, refresh, queue transaction, or
  preparation occurred.

## Orchestration Anomalies

```yaml
orchestration_anomalies:
  - slice: 1
    severity: medium
    category: formatter_scope_churn
    observed: The first worker result contained formatter-only churn across six Python and test files, making the task diff disproportionate and review-hostile.
    impact: Slice acceptance and review were blocked before commit.
    action_taken: Delegated a six-file surgical correction that removed only formatter hunks, reran focused validation, and re-established a semantic-only diff.
    follow_up: Resolved before review and candidate commit.
  - slice: 1
    severity: low
    category: incomplete_specialist_identity_result
    observed: The first delta-only test-quality result omitted required strict-context root fields.
    impact: The result was not accepted as contract-complete.
    action_taken: Preserved its actionable test finding, fixed the gap, refreshed the strict lease, and required a complete-identity re-review.
    follow_up: Final delta-only test-quality results were complete and clean.
```

## Convergence Assessment

### Phase

`closure`

### Scope trend

`shrinking`

### Closed this slice

- Permanent candidate vertical migration-plan authoring, independent review,
  deterministic validation, artifact validation, focused proof, installation,
  and exact acceptance.

### Newly discovered

- The initial tests did not independently reject an omitted migration matrix.
- The initial schema allowed empty migrated-caller and focused-validation
  lists that the deterministic gate rejected.

Both gaps were corrected and independently re-reviewed within Slice 1.

### Deferred out of scope

- CCFG-26B through CCFG-26E execution flights, recovery, finalization,
  closeout, and ownership transfer.
- CCFG-27 runner public-protocol decision, CCFG-28 physical deletion/default
  switch, and CCFG-29 final integration and temporary-policy removal.

### Remaining unknowns

- None for CCFG-26A.

### Temporary compatibility paths

- None introduced by CCFG-26A.

### Cleanup residues

- The stable CCFG-34 policy and root hook remain with CCFG-29 as removal owner
  and permanent #59/#60/#61 parity plus integration as the removal condition.

### Blockers

- None.

### Completion forecastable

`yes`

### Forecast

- CCFG-26A is complete; no implementation or closeout work remains in this
  batch.

### Evidence

- `a0835f1`, `5935b43`, `runway.md`, `completed-slices.md`, exact acceptance,
  installation comparison, and clean final reviews.

### Next proof required

- None for CCFG-26A. A later explicit stable `plan-batch` invocation may select
  CCFG-26B; this closeout selected or prepared no successor.
