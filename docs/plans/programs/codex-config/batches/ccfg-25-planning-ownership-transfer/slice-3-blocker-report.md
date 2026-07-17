# CCFG-25 Slice 3 Blocker Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
slice: 3
status: resolved
blocker_class: required-green-changed-file-command-scope
stable_planning_commit_before_amendment: e72eeecc4f7eb087dce6fa98b2907de7bfbfb875
candidate_commit: 89671eceb9103039e7e6660e73837827c167a3a1
candidate_worktree: clean
first_amended_runway_sha256: 67a7640e289e185efde8c99a4b62a7389b13503b14e66a13ba61958d9d7d0081
second_amended_runway_sha256: 832fd594b9093f13933026d6b3bdac1778f17e74fd1f1fe7117b4e67361c601e
independent_planning_review: clean-on-second-amendment
installation_run: false
exact_acceptance_run: false
final_reviews_run: false
closeout_created: false
successor_selected: false
```

## Resolution

The first changed-Python-files amendment was rejected because explicit arguments
expanded analysis into tests and a fixture outside the configured project. The
second validation-only amendment replaces it with the exact configured-project
changed-script gate:

```sh
.venv/bin/basedpyright \
  scripts/architecture_program_runner_change_allowance.py \
  scripts/architecture_program_runner_phase_contract.py \
  scripts/plan_batch.py
```

At candidate `89671eceb9103039e7e6660e73837827c167a3a1`, the corrected
command exits `0` with zero errors, zero warnings, and zero notes. A fresh
independent planning review against amended runway SHA-256
`832fd594b9093f13933026d6b3bdac1778f17e74fd1f1fe7117b4e67361c601e`
is clean.

Repository `pyrightconfig.json` includes only `scripts`. The bare
repository-wide command therefore does not analyze the changed tests or fixture,
while explicit file arguments do. The prior zero-changed-file-diagnostics
evidence intersected repository-wide default diagnostics with the changed path
set; it did not prove that explicitly analyzing every changed Python file was
green.

Changed tests and the fixture remain outside the configured BasedPyright project
and continue under pytest and Ruff. No configuration, policy, test, fixture, or
unchanged owner was modified. The bare configured-project audit remains a separate
known-red-baseline diagnostic.

## Preserved Repository-Wide Evidence

The original repository-wide comparison remains valid for its configured scope:

| Basis | Errors | Warnings | Exit |
|---|---:|---:|---:|
| Batch baseline `91179e84c7cfed666be224575db7000ca0ea01b3` | 314 | 16 | 1 |
| Candidate `89671eceb9103039e7e6660e73837827c167a3a1` | 311 | 16 | 1 |

The candidate introduces no new repository-wide diagnostics and removes three.
That evidence did not make the first amendment's explicit
all-changed-Python-files command green.

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
- Candidate worktree remains clean at the reviewed Slice 3 commit.

## Next Safe Action

Resume the same Slice 3 and run the complete amended required-green suite and
retained diagnostics. If green, continue directly through fresh and isolated
installation, stable-home comparison, exact acceptance, final exact-range reviews,
and required same-batch closeout. Stop after closing CCFG-25 without selecting or
preparing a successor.
