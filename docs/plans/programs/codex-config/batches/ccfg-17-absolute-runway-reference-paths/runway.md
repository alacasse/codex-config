# CCFG-17 Runway: Absolute Runway Reference Paths

## Purpose

Stop Batch Runway create-spec guidance from generating local absolute paths for
repo-owned skill references, and add focused safeguards so newly selected,
queued, or active runways use repo-relative or skill-relative reference paths.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`
- Risk posture: generated-artifact contract guidance changes are authorized;
  destructive cleanup, historical bulk rewrite, runtime execution behavior
  changes, and broad absolute-path bans are not authorized.
- Risky slices: Slice 1 is `contract-narrowing`; Slices 2 through 4 are
  `migration` or `none`.
- Approval gate for Slice 1: the CCFG-17 ledger row and GitHub issue #32
  authorize narrowing generated runway guidance away from local absolute
  repo-owned skill reference paths. Before execution, the slice must preserve
  explicit allowances for absolute paths in user-provided local values,
  project-specific paths, subagent spec paths, repository cwd handoffs, and
  runtime handoff values that are not reusable repo-owned skill references.

## Current Baseline And Assumptions

- Planning root: `docs/plans/`
- Program root: `docs/plans/programs/codex-config/`
- Selected dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/dispatch.md`
- Queued runway:
  `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md`
- `planning_state.py current --root docs/plans` reported no selected, queued,
  or active batch before this spec was created.
- `planning_state.py validate --root docs/plans` passed with redirect-ledger
  warnings only.
- CCFG-17 source finding:
  `docs/plans/programs/codex-config/findings/github-issue-32-absolute-runway-reference-paths.md`
- Existing green baseline:
  `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  produced `13 passed`.
- Existing known-red diagnostic baseline:
  `python -m pytest tests/test_codex_features_manifest.py -q` produced
  `15 passed, 3 failed` in unrelated command-owner wording expectations.
- `python -m ruff --version` currently fails with `No module named ruff`.
- `python -m json.tool codex-features.json` passed.
- `git diff --check` passed.

## Non-Goals

- Do not bulk-rewrite completed runways or archived historical artifacts.
- Do not update the displaced CCFG-11 runway except as read-only evidence.
- Do not ban legitimate absolute paths for local user values, project-specific
  paths, subagent prompts, repository cwd handoffs, or runtime handoffs.
- Do not change Batch Runway execution mechanics.
- Do not add project-specific paths, validation commands, cache locations, or
  local planning layouts to reusable skill guidance.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is being
produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v1.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`

Overrides:

- None.

## Validation Profile

Selected profile: `test-only-topology`

Profile reference:
`skills/batch-runway/references/validation-profiles/test-only-topology.md`

Focused validation commands:

- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
  - Status class: `required-green`
  - Baseline: passed with `13 passed`.
- `python -m pytest tests/test_codex_features_manifest.py -q`
  - Status class: `known-red-baseline`
  - Baseline: currently fails in unrelated command-owner wording expectations.
    Use diagnostically if Slice 4 touches manifest metadata, but do not block
    CCFG-17 unless the slice explicitly remediates and promotes this command.
- `python -m pytest tests/test_batch_runway_create_spec_contract.py tests/test_codex_features_manifest.py -q`
  - Status class: `conditional`
  - Trigger: run when Slice 4 changes `codex-features.json` or release metadata.
    The existing manifest-test failures remain known-red unless remediated.
- `python -m json.tool codex-features.json`
  - Status class: `required-green`
  - Baseline: passed.
- `python -m ruff check tests/test_batch_runway_create_spec_contract.py`
  - Status class: `known-red-baseline`
  - Baseline: `python -m ruff --version` fails because `ruff` is not installed.
    Use an available project-approved ruff runner only if the executor can do
    so without installing dependencies.
- `git diff --check`
  - Status class: `required-green`
  - Baseline: passed.

## Execution Ledger

| Slice | Status | Risk class | Commit | Validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Create-spec reference guidance | Completed | contract-narrowing | `bc4175c` | `tests/test_batch_runway_create_spec_contract.py` passed; `git diff --check` passed | clean | Archived in `completed-slices.md`. |
| 2. Create-spec contract tests | Completed | migration | `70324f8` | `tests/test_batch_runway_create_spec_contract.py` passed; `git diff --check` passed; `python -m ruff` unavailable as known-red baseline | clean | Archived in `completed-slices.md`. |
| 3. Active-runway artifact guard | Pending | migration |  |  |  | Ignore completed and archived historical evidence. |
| 4. Metadata and final validation | Pending | none |  |  |  | Update release metadata and closeout evidence only. |

## Slice 1: Create-Spec Reference Guidance

Risk class: `contract-narrowing`

Approval gate:

- CCFG-17 source issue and ledger row authorize narrowing generated runway
  guidance away from local absolute repo-owned skill reference paths.
- Before completing this slice, preserve explicit absolute-path allowances for
  user-provided local values, project-specific paths, subagent spec paths,
  repository cwd handoffs, and runtime handoff values that are not reusable
  repo-owned skill references.

Scope:

- Update lean-runway reference examples in
  `skills/batch-runway/references/create-spec.md` to use repo-relative or
  skill-relative paths for repo-owned Batch Runway references.
- Clarify that generated runway artifacts should not embed local absolute paths
  for reusable repo-owned skill references.
- Preserve allowed absolute-path use in subagent handoffs and project-specific
  runtime values.

Allowed files or areas:

- `skills/batch-runway/references/create-spec.md`
- Focused tests under `tests/` only when needed to lock the wording in this
  slice.

Non-goals:

- Do not edit completed or archived runways.
- Do not change `subagent-briefs.md` or `execute-slice-core-v1.md` absolute
  spec-path handoff examples unless a focused test proves they conflict with
  the new generated-artifact rule.

Acceptance criteria:

- The lean spec reference block no longer uses
  the old absolute Batch Runway reference placeholder for repo-owned
  references.
- The guidance names repo-relative or skill-relative references as the desired
  generated artifact shape.
- The guidance keeps legitimate absolute runtime handoffs allowed.

Validation:

- Run the selected `test-only-topology` profile.
- Run `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`.
- Run `git diff --check`.

Commit message:

`Use relative Batch Runway reference paths in generated specs`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 1, do not spawn or wait on additional subagents,
and preserve project-neutral guidance.

Review subagent brief:

Review the exact task-scoped diff basis provided by the coordinator. Confirm
that generated runway references are repo-relative or skill-relative and that
legitimate absolute runtime handoffs remain allowed.

Stop conditions:

- Stop if the guidance would ban required absolute paths for subagent prompts,
  repository cwd handoffs, project-specific values, or user-provided local
  paths.

## Slice 2: Create-Spec Contract Tests

Risk class: `migration`

Scope:

- Extend `tests/test_batch_runway_create_spec_contract.py` with focused
  assertions that create-spec guidance does not require absolute paths for
  reusable Batch Runway skill references.
- Assert the desired repo-relative or skill-relative examples stay present.
- Keep the test scoped to create-spec guidance; do not scan historical planning
  artifacts in this slice.

Allowed files or areas:

- `tests/test_batch_runway_create_spec_contract.py`
- `skills/batch-runway/references/create-spec.md` only for minimal wording
  alignment if Slice 1 left a gap.

Non-goals:

- Do not add broad repository path bans.
- Do not make tests fail on old completed runways.

Acceptance criteria:

- A regression in create-spec guidance back to
  the old absolute Batch Runway reference placeholder fails focused tests.
- Desired relative reference examples are asserted.
- Existing create-spec contract tests remain green.

Validation:

- Run `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`.
- Run `git diff --check`.

Commit message:

`Test generated Batch Runway reference path guidance`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 2 and do not delegate. Keep assertions focused on
the create-spec contract.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm the tests protect generated
reference guidance without banning unrelated absolute path uses.

Stop conditions:

- Stop if the tests require rewriting completed or archived planning evidence.

## Slice 3: Active-Runway Artifact Guard

Risk class: `migration`

Scope:

- Add a scoped guard that checks selected, queued, or active runway artifacts
  under `docs/plans/programs/**/batches/**/runway.md` for the local
  codex-config skill-path prefix named in the source finding.
- Drive the guard from active planning state or current ledger queue status so
  completed, superseded, abandoned, and archived historical runways are not
  rewritten or failed.
- Ensure the currently queued CCFG-17 runway uses repo-relative references.

Allowed files or areas:

- `tests/test_batch_runway_create_spec_contract.py` or a focused adjacent test
  file under `tests/`
- `docs/plans/programs/codex-config/LEDGER.md` only if queue-status wording
  needs a minimal alignment for the guard
- `docs/plans/programs/codex-config/batches/ccfg-17-absolute-runway-reference-paths/runway.md`
  only for generated artifact wording in this active queued runway

Non-goals:

- Do not scan every completed runway as a failure target.
- Do not modify completed or archived historical runways.
- Do not ban project-specific absolute values outside reusable skill
  references.

Acceptance criteria:

- The guard fails if an active selected, queued, or active runway embeds
  the local codex-config skill-path prefix named in the source finding.
- Existing completed CCFG runways with historical absolute paths remain
  evidence and do not fail the guard.
- The CCFG-17 queued runway stays free of local absolute repo-owned skill
  references.

Validation:

- Run `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`.
- Run `git diff --check`.

Commit message:

`Guard active runways against local skill reference paths`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 3, do not delegate, and keep the guard scoped to
active generated artifacts.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm historical completed runways
are not made blocking and active generated artifacts are protected.

Stop conditions:

- Stop if the only available guard would require bulk historical runway
  rewrites.

## Slice 4: Metadata And Final Validation

Risk class: `none`

Scope:

- Update `codex-features.json` for the Batch Runway guidance change if any
  behavior-significant skill metadata version bump is required.
- Update `CHANGELOG.md` with a compact Unreleased entry for absolute runway
  reference path guidance.
- Run final focused validation and prepare closeout evidence.

Allowed files or areas:

- `codex-features.json`
- `CHANGELOG.md`
- CCFG-17 `runway.md`, `completed-slices.md`, and `closeout.md`
- Program `CURRENT.md` and `LEDGER.md` only during closeout reconciliation

Non-goals:

- Do not remediate unrelated existing command-owner wording failures in
  `tests/test_codex_features_manifest.py` unless the user explicitly selects
  that work.
- Do not install dependencies just to run ruff.

Acceptance criteria:

- Batch Runway metadata reflects the changed guidance when required by repo
  convention.
- Changelog names the problem, decision, and expected effect.
- Focused tests and JSON validation are recorded with status classes.
- Closeout preserves CCFG-17 as generated-guidance work only.

Validation:

- Run `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`.
- Run `python -m json.tool codex-features.json`.
- Run `git diff --check`.
- Optionally run `python -m pytest tests/test_codex_features_manifest.py -q`
  as known-red diagnostic evidence if metadata changed.

Commit message:

`Record Batch Runway reference path guidance release`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only Slice 4, do not spawn additional agents, and keep release
metadata compact.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm metadata and changelog changes
match the guidance/test changes and do not imply historical runway rewrites.

Stop conditions:

- Stop if final validation failures are unrelated command-owner baseline
  failures and the only fix would widen CCFG-17 beyond reference-path guidance.

## Final Validation

Required before closeout:

- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`
- `python -m json.tool codex-features.json`
- `git diff --check`

Diagnostic or conditional:

- `python -m pytest tests/test_codex_features_manifest.py -q` remains
  known-red unless a slice explicitly remediates unrelated command-owner
  wording expectations.
- `python -m ruff check tests/test_batch_runway_create_spec_contract.py` remains
  known-red while `python -m ruff --version` fails in this environment.

## Stop Conditions

- Stop if implementation would rewrite completed or archived historical
  runways.
- Stop if implementation would ban legitimate local absolute paths outside
  reusable repo-owned skill references.
- Stop if active-artifact tests cannot distinguish queued or active runways
  from completed historical evidence.
- Stop if reusable skill guidance would need project-specific paths, cache
  locations, validation commands, or local planning layouts.
- Stop before successor selection; `plan-batch` has produced this one queued
  runway only.
