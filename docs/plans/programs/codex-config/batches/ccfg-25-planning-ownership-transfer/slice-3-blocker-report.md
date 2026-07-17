# CCFG-25 Slice 3 Blocker Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
slice: 3
status: blocked
blocker_class: required-green-changed-file-command-scope
stable_planning_commit_before_amendment: e72eeecc4f7eb087dce6fa98b2907de7bfbfb875
candidate_commit: 89671eceb9103039e7e6660e73837827c167a3a1
candidate_worktree: clean
amended_runway_sha256: 67a7640e289e185efde8c99a4b62a7389b13503b14e66a13ba61958d9d7d0081
independent_planning_review: findings
installation_run: false
exact_acceptance_run: false
final_reviews_run: false
closeout_created: false
successor_selected: false
```

## Blocker

The authorized changed-Python-files required-green command does not pass:

```sh
git diff --name-only -z --diff-filter=ACMR \
  91179e84c7cfed666be224575db7000ca0ea01b3 HEAD \
  -- '*.py' \
  | xargs -0 -r .venv/bin/basedpyright
```

At candidate `89671eceb9103039e7e6660e73837827c167a3a1`, it exits `123`
with 120 errors and 3 warnings. The exact range contains 14 changed Python
paths: three production scripts, ten tests, and one scenario fixture.

Repository `pyrightconfig.json` includes only `scripts`. The bare
repository-wide command therefore does not analyze the changed tests or fixture,
while explicit file arguments do. The prior zero-changed-file-diagnostics
evidence intersected repository-wide default diagnostics with the changed path
set; it did not prove that explicitly analyzing every changed Python file was
green.

The amendment's command consequently expands analysis beyond the configured
repository scope and conflicts with its own required-green classification. The
fresh independent planning review is `findings`, so the amendment is not released
for execution.

## Preserved Repository-Wide Evidence

The original repository-wide comparison remains valid for its configured scope:

| Basis | Errors | Warnings | Exit |
|---|---:|---:|---:|
| Batch baseline `91179e84c7cfed666be224575db7000ca0ea01b3` | 314 | 16 | 1 |
| Candidate `89671eceb9103039e7e6660e73837827c167a3a1` | 311 | 16 | 1 |

The candidate introduces no new repository-wide diagnostics and removes three.
That evidence does not make the newly explicit all-changed-Python-files command
green.

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

## Smallest Safe Decision

Authorize another validation-only amendment that makes one explicit scope choice:

1. limit changed-file non-regression to changed Python files inside the
   repository-configured BasedPyright project scope; or
2. classify the diagnostics produced by explicitly analyzing changed tests and
   fixtures without requiring out-of-scope cleanup.

The required-green command and its acceptance condition must use the same scope,
and the exact amended runway must receive another fresh independent planning
review. Do not modify BasedPyright configuration, edit unchanged owners or tests
to chase historical diagnostics, run installation or exact acceptance, create
closeout, or select a successor.
