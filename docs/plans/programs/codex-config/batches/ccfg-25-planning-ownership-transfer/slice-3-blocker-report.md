# CCFG-25 Slice 3 Blocker Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
slice: 3
status: blocked
blocker_class: required-green-validation-command-contract
stable_planning_commit: a83fbfd7521441b2d3b875ae77bb54977b72e499
candidate_commit: 89671eceb9103039e7e6660e73837827c167a3a1
candidate_worktree: clean
installation_run: false
exact_acceptance_run: false
final_reviews_run: false
closeout_created: false
successor_selected: false
```

## Blocker

The Slice 3 required-green command below is repository-wide and exits `1`:

```sh
.venv/bin/basedpyright
```

The failure is not introduced by CCFG-25:

| Basis | Errors | Warnings | Exit |
|---|---:|---:|---:|
| Batch baseline `91179e84c7cfed666be224575db7000ca0ea01b3` | 314 | 16 | 1 |
| Candidate `89671eceb9103039e7e6660e73837827c167a3a1` | 311 | 16 | 1 |

The exact candidate range has zero BasedPyright diagnostics in changed files.
All current diagnostics occur in ten unchanged modules, including runner,
Planning State, planning-contract, and skill-contract owners that are read-only
or outside the Slice 3 semantic ceiling. CCFG-25 removes three baseline
diagnostics and adds none.

## Green Evidence Before The Stop

- Core pytest: `244 passed, 18 subtests passed`.
- Filtered manifest: `21 passed, 1 deselected, 210 subtests passed`.
- Filtered deletion/projection: `7 passed, 18 deselected, 20 subtests passed`.
- Scenario catalog: 69 scenarios valid.
- Both single-document structural skill validations: passed.
- Ruff: passed.
- Range `git diff --check`: passed.
- Known-red diagnostics: exactly the declared one CCFG-26 manifest failure and
  six preclassified deletion-vocabulary failures.

## Smallest Safe Decision

Authorize a bounded validation-only runway amendment after deciding the intended
BasedPyright scope or status classification. Obtain a fresh independent planning
review against the exact amendment before resuming this same Slice 3. Do not chase
the 311 diagnostics through read-only owners, silently reclassify the gate, run
installation or exact acceptance, create closeout, or select a successor.
