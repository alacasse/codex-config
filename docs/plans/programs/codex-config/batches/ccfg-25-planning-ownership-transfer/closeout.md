# CCFG-25 Planning Ownership Transfer Closeout

## Outcome

- Batch: `ccfg-25-planning-ownership-transfer`
- Status: completed
- Covered finding: CCFG-25
- Finding lifecycle result: `Closed`
- Dispatch: `dispatch.md`
- Runway: `runway.md`
- Completed-slice archive: `completed-slices.md`
- Controlling stable commit before closeout:
  `203320ea0cba1d7525f2dd271e65701ce91aeb77`
- Candidate baseline: `91179e84c7cfed666be224575db7000ca0ea01b3`
- Final candidate commit: `89671eceb9103039e7e6660e73837827c167a3a1`
- Final closeout commit: `this closeout commit`
- Canonical planning root: `/home/alacasse/projects/codex-config/docs/plans`
- Implementation root:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Successor selected: no

CCFG-25 completed the COR-008 transfer. One complete public `plan-batch`
invocation now owns selection, independent planning review, proportionality,
approval, and the DEC-038 queue transaction. Architecture Program Runway and
Batch Runway no longer own planning decisions. The serialized
`select-dispatch` and `create-spec` labels remain temporary compatibility
observations only; CCFG-27 owns their migration/removal decision and CCFG-29 is
the final physical-cleanup deadline. Every CCFG-26 execution and closeout
responsibility remains explicit and tested. Candidate installation converged
without changing the stable Codex home, and no successor was selected or
prepared.

## Commits

| Slice | Commit | Outcome |
|---|---|---|
| 1. Implement installed `plan-batch` owner | `5aa5add` | Added the public command owner, independent planner/reviewer roles, proportionality gates, and DEC-038 transaction ownership. |
| 2. Remove displaced planning ownership | `12f7072` | Removed APR and Batch Runway planning authority, routed support-skill handoffs to `plan-batch`, and preserved serialized compatibility and all CCFG-26 responsibilities. |
| 3. Converge installation and final acceptance | `89671ec` | Converged installed manifests and documentation, passed corrected validation, real installations, exact acceptance, and all final exact-range reviews. |

Implementation range:
`91179e84c7cfed666be224575db7000ca0ea01b3..89671eceb9103039e7e6660e73837827c167a3a1`.
The cumulative binary diff SHA-256 is
`c5dee2c8d0f0fc65ed758360dd8dad51fbf66cf3fe9ed387d218197d8b283ae4`.

## Validation And Review

- Slice 3 core validation passed 244 tests and 18 subtests. The filtered
  manifest passed 21 tests and 210 subtests with one deselection; the filtered
  deletion/projection gate passed 7 tests and 20 subtests with 18 deselections.
- All 69 scenarios validated. Both single-document structural skill checks,
  Ruff, and candidate-range whitespace validation passed.
- The exact configured-project BasedPyright gate passed the three changed
  `scripts` files with zero errors, warnings, or notes.
- Known-red diagnostics remained bounded: the complete manifest retained only
  the one CCFG-26 failure, the broad deletion/projection suite retained the six
  preclassified deletion-vocabulary failures, and bare configured-project
  BasedPyright improved from 314 errors and 16 warnings to 311 errors and 16
  warnings with no new diagnostic.
- Exact CCFG-33 acceptance bound candidate `89671ec`, used one evidence-pytest
  process, passed 25 tests, and reported all 69 scenarios, 31 required
  contracts, 17 families, six evidence keys, and six aliases green. Evidence
  time was 38.73486 seconds.
- The acceptance-result file SHA-256 is
  `c582fa56526c8857d01e8746ba7dd3c2733e7641fb8924d82e55a3e74f6f4796`;
  the generated JSON report file SHA-256 is
  `65a3a1ced0b005ee331f5dedb45db0b4189bfdfae323255b5a9699ce34c7082f`;
  the acceptance result's canonical `report_sha256` is
  `2d40bb4fe2354840f88c1358e2162e509bad5a13bff6cfb677b088cfc3d26472`.
- Explicit generated outputs were
  `/tmp/ccfg-25-acceptance.2pWwJ4/acceptance-result.json`,
  `/tmp/ccfg-25-acceptance.2pWwJ4/report.json`, and
  `/tmp/ccfg-25-acceptance.2pWwJ4/report.txt`. They are disposable run evidence,
  not committed state or a permanent cache.
- Final exact-range independent, import-topology, dead-surface, and delta-only
  test-quality reviews were clean on the cumulative diff SHA-256 above.

## Installation Evidence

- A fresh empty candidate home and the fixed isolated candidate home both
  converged with `plan-batch 2.0.0`, `architecture-program-runway 3.0.0`,
  `batch-runway 2.0.0`, `custom-agents 1.5.0`, `legacy-removal 1.0.9`,
  `planning-contracts 1.0.0`, and `planning-state 1.1.0`.
- Both candidate homes reported every managed feature at the candidate version;
  their post-install dry runs were clean.
- Stable-home status was byte-for-byte identical before and after installation,
  with SHA-256
  `fbd80311285b450d58b147a1a233ac96f36fc234c90a2c62dfc3f4e6b5ce75d7`.
  Stable `plan-batch 1.0.5`, `architecture-program-runway 1.1.7`, and
  `batch-runway 1.5.1` remained unchanged.
- Candidate code did not mutate canonical planning state, and no default
  generation switch occurred.

## Cost Evidence

| Measure | Result |
|---|---:|
| Candidate files changed | 38 |
| Insertions | 5,223 |
| Deletions | 1,602 |
| Net lines | +3,621 |
| Diff size | 375,544 bytes |
| Slice 3 core tests | 244 passed plus 18 subtests |
| Final exact acceptance | 25 passed; 38.73486 s evidence; 62.16 s CLI elapsed |
| Evidence-pytest processes | 1 |
| Context usage | unavailable; not persisted or estimated |

## Removed And Preserved Surfaces

| Surface | Classification | Evidence and condition |
|---|---|---|
| APR planning, selection, and queue authority | removed | Public planning routes through one complete `plan-batch` transaction; focused manifest, routing, migration, and behavioral tests are green. |
| Batch Runway `create-spec` planning authority | removed | Planning ownership and draft creation moved to `plan-batch`; Batch Runway retains execution contracts only. |
| Support-skill planning handoffs | migrated | `planning-artifacts`, `legacy-removal`, `port-by-contract`, and `dead-surface-audit` route planning handoffs to `plan-batch` while retaining evidence, layout, classification, and contract-distillation responsibilities. |
| Duplicate Batch Runway cross-checkout-helper installation | removed | Planning State remains the single installed helper owner. |
| Serialized `select-dispatch` and `create-spec` labels | kept | Compatibility observations for receipt/resume consumers only; CCFG-27 owns the migration/removal decision and CCFG-29 owns final cleanup if retained. |
| Runner facade | kept-thin-entrypoint | The CLI remains a thin shell over phase ownership and preserves the existing transition graph and receipt compatibility. |
| APR closeout and Batch Runway execution responsibilities | kept | All proceed/stop, delegation, recovery, validation, review, commit, receipt, execution-ledger, finalization, closeout, reconciliation, no-successor, and strict cross-checkout responsibilities remain for CCFG-26. |

No unclassified planning caller or runner owner remains. Retained temporary
surfaces have named callers, reasons, future owners, and removal conditions.

## Same-Batch Program Reconciliation

- CCFG-25 is `Closed`.
- Selected dispatch, active runway, queued batch, and queued dispatch are
  `None` after reconciliation.
- `latest_closeout` points to this file.
- `ccfg-25-planning-ownership-transfer` is completed in the batch queue.
- CCFG-26 through CCFG-29 remain open and unselected. CCFG-26 has no dispatch or
  runway and remains responsible for execution and closeout ownership transfer.
- No successor batch, dispatch, runway, refresh, queue transaction, or
  preparation occurred.

## Orchestration Anomalies

```yaml
orchestration_anomalies:
  - slice: 2
    severity: low
    category: interrupted_worker_late_completion
    observed: "An interrupted worker completed two in-scope edits after interruption."
    impact: "A retry detected overlap and stopped; no change was lost or duplicated."
    action_taken: "Reconciled exact authorship and lease identity before resuming."
    follow_up: "Resolved before Slice 2 acceptance."
  - slice: 3
    severity: low
    category: repository_wide_gate_baseline_mismatch
    observed: "The original repository-wide BasedPyright required-green command reproduced 311 historical errors and 16 warnings."
    impact: "Slice 3 stopped before installation, acceptance, final review, or closeout."
    action_taken: "Recorded baseline non-regression and obtained a bounded validation-only amendment."
    follow_up: "Resolved without editing unchanged owners or BasedPyright policy."
  - slice: 3
    severity: low
    category: explicit_file_scope_expansion
    observed: "The first amendment explicitly analyzed changed tests and a fixture outside the configured scripts project and produced 120 errors and 3 warnings."
    impact: "Independent planning review returned findings; no execution step began."
    action_taken: "A second authorized amendment aligned the gate with the configured scripts scope and received a fresh clean review."
    follow_up: "Resolved by the exact three-script zero-diagnostic gate."
```

## Convergence Assessment

### Phase

`closure`

### Scope trend

`shrinking`

### Closed this slice

- Final configured-project validation, converged candidate installation, exact
  acceptance, exact-range reviews, and COR-008 ownership reconciliation.

### Newly discovered

- Repository-wide BasedPyright was a known-red configured-project diagnostic,
  and explicit arguments widened analysis into out-of-project tests and a
  fixture. Both scope mismatches were resolved through reviewed validation-only
  amendments without semantic changes.

### Deferred out of scope

- CCFG-26 execution/closeout ownership transfer; CCFG-27 runner public-protocol
  decision; CCFG-28 cutover; CCFG-29 integration and final compatibility cleanup;
  stable installation and default-generation switching.

### Remaining unknowns

- None for CCFG-25. Later owner transfers retain their own explicit gates.

### Temporary compatibility paths

- Serialized `select-dispatch` and `create-spec` remain observation/advance
  labels only. CCFG-27 decides migration or removal; CCFG-29 is the physical
  cleanup deadline if they remain.

### Cleanup residues

- The named serialized labels and CCFG-26 execution/closeout surfaces are
  intentional, classified, and protected. No unclassified residue remains.

### Blockers

- None.

### Completion forecastable

`yes`

### Forecast

- CCFG-25 is complete; no CCFG-25 implementation or closeout work remains.

### Evidence

- `completed-slices.md`, candidate range `91179e8..89671ec`, converged fresh and
  isolated candidate installations, exact acceptance outputs, and clean final
  reviews.

### Next proof required

- A later explicit `plan-batch` request may select exactly one bounded ledger
  row. This closeout does not select, dispatch, queue, or prepare CCFG-26.
