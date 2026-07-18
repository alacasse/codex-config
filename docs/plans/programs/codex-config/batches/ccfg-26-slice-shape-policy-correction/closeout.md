# CCFG-26 Slice-Shape Policy Correction Closeout

## Outcome

- Batch: `ccfg-26-slice-shape-policy-correction`
- Status: completed
- Covered finding: CCFG-26
- Finding lifecycle result: `Prepared`
- Dispatch: `dispatch.md`
- Runway: `runway.md`
- Completed-slice archive: `completed-slices.md`
- Candidate baseline: `a0835f146857612dcd5a95053d67c53f32449012`
- Candidate implementation commit:
  `8a9331947ffc8b0b28b8c75ecf6fc60f8b3c2fcd`
- Canonical policy/reference commit:
  `f5cb753b86f64c2a5ee351c68473540ead82da01`
- Stable execution-receipt commit:
  `66cb6d4` (`docs(ccfg-26): record slice-shape execution receipt`)
- Final closeout commit: `this closeout commit`
- Canonical planning root: `/home/alacasse/projects/codex-config/docs/plans`
- Implementation root:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Successor selected: no

This batch closes the issue #66 correction before CCFG-26 execution ownership
begins moving. The active program declares one human-maintained
`slice-shape-policy/v1` YAML file. Candidate `plan-batch`, `batch_planner`,
`batch_plan_reviewer`, deterministic validation, and `planning-runway/v1` bind
the same exact policy identity and persist shape independently from mutation
risk. Migration evidence remains complete and independently risk-gated.

CCFG-26 remains `Prepared`, not `Closed`. CCFG-26B through CCFG-26E retain the
fresh execution-flight, bounded recovery, finalization, and closeout ownership
work. They remain unselected and require later explicit stable `plan-batch`
invocations under the temporary CCFG-34 policy.

## Commit

| Slice | Candidate commit | Canonical policy commit | Outcome |
|---|---|---|---|
| 1. Resolve and enforce the project slice-shape policy end to end | `8a93319` | `f5cb753` | Added fail-closed YAML policy resolution and identity, per-slice shape persistence, independent migration evidence, exact agent/schema gates, and focused scenario proof. |

Implementation range:
`a0835f146857612dcd5a95053d67c53f32449012..8a9331947ffc8b0b28b8c75ecf6fc60f8b3c2fcd`.

The candidate range changes 20 paths with 1,237 insertions and 209 deletions.
Its binary diff SHA-256 is
`c87ed3577880e564d668f11995a00b8e89bc23b298b1b9e87b52a1985ae75915`.
The canonical policy range changes two paths with five insertions; its binary
diff SHA-256 is
`5147efa0b292eebf600cc8478177f0b56bb0ff5e7cc5104f27959349a2a77a24`.

## Validation And Review

- Focused final validation passed 191 tests and 183 subtests.
- The selected manifest boundary passed 2 tests and 28 subtests.
- The command-owner catalog validated all 82 scenarios.
- Ruff passed; configured production BasedPyright reported zero errors and five
  unresolved-source warnings; Planning State `current` and `validate` passed;
  both exact commit ranges passed whitespace validation.
- The declared known-red diagnostic reproduced exactly the two later CCFG-26
  execution-owner assertions with no additional failure.
- Delta-only test-quality review found six regression-strength gaps across two
  bounded passes. All were corrected test-only, including persisted shape,
  duplicate YAML keys, independent reviewer checks, policy identity, and
  migration-risk plus horizontal-shape independence. Final exact-range review
  was clean.
- Independent runway review found one missing `planning-contracts` feature
  version bump. The manifest, exact test, and changelog were corrected to
  `planning-contracts 1.2.0`; final exact-commit review was clean with no
  residual risk or required fix.
- Exact acceptance bound clean commit `8a93319`, used one evidence-pytest
  process, passed 25 tests, and reported 82 scenarios, 31 required contracts,
  and 17 families green. The acceptance result SHA-256 is
  `25125fd290e6b45e3a1b83fa3bceffb187bf0d2695d45db6a0c1daffebd61c5e`;
  generated `report.json` SHA-256 is
  `d905bfd9f0ff2493e5f593d97e5fc60a2abf0943461e0711a1337f1aae0d806a`;
  generated `report.txt` SHA-256 is
  `4b784c812577a04c9d8679e7270de5aa14b2f2f94bdf78ee06540e60ae0ed23b`.

## Installation Evidence

- A fresh `/tmp` Codex home installed all default candidate features and every
  post-install dry-run link reported `ok`.
- The isolated candidate home converged at `planning-contracts 1.2.0`,
  `custom-agents 1.7.0`, and `plan-batch 2.2.0`; every post-install dry-run link
  was `ok`.
- Stable-home status was byte-for-byte unchanged before and after candidate
  installation, with SHA-256
  `5037e782b9140f4a5b818a79f6f0afc03bbf376ae7476451eedda5710119619a`.
- No default-generation switch or canonical queue mutation occurred during
  installation or acceptance.

## Removed And Preserved Surfaces

| Surface | Classification | Evidence and condition |
|---|---|---|
| Current `vertical_slice` shape-selection representation | removed | Current candidate owners, schema, fixtures, and scenarios use required `shape` plus independently risk-gated `migration_evidence`; no compatibility reader or second dialect accepts the old representation. Historical commits remain readable only as history. |
| Stable CCFG-34 policy and root hook | kept temporarily | Stable CCFG-26 through CCFG-29 planning and execution still require the temporary policy. CCFG-29 removes it only after permanent parity and integration. |
| Candidate planning authority | kept non-authoritative | Stable `plan-batch` remains the canonical planning path until CCFG-29. Candidate installation is isolated proof only. |
| CCFG-26B through CCFG-26E execution ownership | deferred | Later explicit batches own execution flights, recovery, finalization, closeout, and final ownership transfer. |

No unclassified cleanup residue or compatibility path remains in this batch.

## Same-Batch Program Reconciliation

- `ccfg-26-slice-shape-policy-correction` is completed from candidate commit
  `8a93319`, canonical policy commit `f5cb753`, stable receipt commit `66cb6d4`,
  final validation, installation evidence, exact acceptance, and clean final
  reviews.
- Parent finding CCFG-26 is `Prepared`, not `Closed`.
- Selected dispatch, queued batch, and active runway are `None`.
- `latest_closeout` points to this file.
- This batch is completed in the batch queue.
- CCFG-26B through CCFG-26E remain candidate batches with no dispatch or runway.
- CCFG-27 through CCFG-29 remain open and unselected.
- No successor batch, dispatch, runway, refresh, queue transaction, or
  preparation occurred.

## Orchestration Anomalies

```yaml
orchestration_anomalies:
  - slice: 1
    severity: medium
    category: premature_reviewer_lease_handoff
    observed: The coordinator sent one delta-only re-review handoff before calling the mandatory later-handoff lease refresh.
    impact: The reviewer was interrupted before its result was accepted; no files, commits, or repository revisions moved.
    action_taken: The reviewer was stopped, the strict lease and empty read-only scope were refreshed and validated, and the review was restarted from the unchanged diff.
    follow_up: Resolved in this batch; all accepted later reviews carry freshly prepared exact leases.
```

## Convergence Assessment

### Phase

`closure`

### Scope trend

`shrinking`

### Closed this slice

- Project-owned YAML policy resolution, exact identity binding, slice-shape
  authoring and persistence, independent review, deterministic and schema
  validation, focused proof, installation, and exact acceptance.

### Newly discovered

- The initial tests did not fully protect persisted shape, duplicate YAML keys,
  independent reviewer checks, exact policy identity, or shape-risk
  independence.
- The initial feature metadata did not bump the owner of the changed runway
  schema.

All gaps were corrected and independently re-reviewed within Slice 1.

### Deferred out of scope

- CCFG-26B through CCFG-26E execution flights, recovery, finalization,
  closeout, and ownership transfer.
- CCFG-27 runner protocol decisions, CCFG-28 deletion/default switch, and
  CCFG-29 final integration and temporary-policy removal.

### Remaining unknowns

- None for this corrective batch.

### Temporary compatibility paths

- None introduced by this batch.

### Cleanup residues

- The stable CCFG-34 policy and root hook remain with CCFG-29 as removal owner
  and permanent parity plus integration as the removal condition.

### Blockers

- None.

### Completion forecastable

`yes`

### Forecast

- This corrective batch is complete; no implementation or closeout work
  remains in it.

### Evidence

- `8a93319`, `f5cb753`, `66cb6d4`, `runway.md`, `completed-slices.md`, exact
  acceptance, installation comparison, and clean final reviews.

### Next proof required

- None for this batch. A later explicit stable `plan-batch` invocation may
  select one bounded next batch; this closeout selected or prepared no
  successor.
