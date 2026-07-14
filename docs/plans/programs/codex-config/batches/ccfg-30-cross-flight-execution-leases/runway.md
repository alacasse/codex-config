# CCFG-30 Cross-Flight Execution Leases Runway

## Purpose

Separate durable cross-checkout planning snapshots from short-lived live
execution leases. `work-batch` must reconcile the same queued runway against
reviewed repository movement before execution, then use exact helper-validated
live revisions before every worker and reviewer handoff.

This runway covers CCFG-30 only. Closeout may mark CCFG-30 `Closed` only when
all ten source-note regression scenarios, installed-state checks, focused
validation, and independent review are green. Otherwise preserve the concrete
blocker and stop without selecting a successor.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slices 1 through 4 risk: `migration`.
- Authorized migration: introduce explicit planning-snapshot, startup-
  reconciliation, execution-lease, and execution-receipt semantics across the
  current temporary cross-checkout bridge.
- Supported behavior to preserve: exact validation of roots, repository
  identity, generation, revisions, active Codex home, mutation policy, and
  write scope before every delegated handoff.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Approval gates: none; no destructive or contract-narrowing work is in scope.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Planning-state `current` and `validate` pass with no blockers and only the two
  known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable implementation checkout:
  `/home/alacasse/projects/codex-config`, branch `master`, planning baseline
  `7220a2e78a7ad50550cd7bc7ffcfd328301d8e7f`.
- The stable worktree was clean before planning.
- The installed helper
  `/home/alacasse/.codex/scripts/cross_checkout_context.py` resolves to the
  stable repo-owned helper and is owned by `batch-runway 1.5.1`.
- `./install.sh --status` and `./install.sh --dry-run` pass before planning.
- The redesign candidate is read-only evidence at
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, exact `HEAD`
  `3e54155964e92d3a4dced8268cc683baaab9be1c`.
- This is an ordinary single-root execution batch. It does not use
  `cross-checkout-context/v1` as its own execution mode. Worker and reviewer
  results keep `verified_cross_checkout_context: null`.
- The queueing artifacts are expected stable coordination state and may be
  committed between this planning flight and execution. They remain historical
  plan evidence and are not a reason to rewrite this runway's baseline.
- Current required-green baselines are 21 cross-checkout tests plus 31 subtests,
  5 lifecycle-guard tests, Ruff, and basedpyright.
- The full manifest has the accepted diagnostic baseline of 3 failures,
  18 passes, and 202 subtests in the three unrelated exact-wording assertions
  recorded below.

## Batch Non-Goals

- Do not change the redesign candidate checkout.
- Do not implement CCFG-21 through CCFG-29 or accelerate ownership transfer,
  cutover, convergence, or bridge deletion.
- Do not change CCFG-19 or CCFG-20 dispatch, runway, closeout, or candidate
  implementation evidence.
- Do not accept stale revisions in `parse_cross_checkout_context` or replace
  exact delegation checks with ancestry checks.
- Do not let helper code classify compatible changes, select scope, authorize
  execution, mutate planning state, or record closeout.
- Do not rewrite a queued runway's snapshot after its containing commit exists.
- Do not treat arbitrary intervening commits or dirty files as compatible.
- Do not encode codex-config-specific paths, commands, caches, labels, or
  planning layout in reusable skill logic.
- Do not remediate the three unrelated manifest wording failures in this batch.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`.
- Execution repository: `/home/alacasse/projects/codex-config`.
- Cross-checkout execution context for this batch: not applicable; ordinary
  single-root execution.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway`.
- Integration harness: temporary Git repositories exercised by
  `tests/test_cross_checkout_context.py`, plus lifecycle and manifest contract
  tests.
- Harness output: temporary directories and stdout/stderr only; no durable
  generated output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused stable-repository commit per accepted slice;
  record exact hashes in the concrete execution ledger. Queue artifacts and
  same-batch program receipts remain coordinator-owned planning state.
- Dirty-file constraints: preserve queueing artifacts and unrelated user
  changes; stage only active-slice paths. Stop on overlap with an active slice.
- Test quality review: `delta-only` for every test-changing slice.

## Owner Seam And Slice Handoff

`scripts/cross_checkout_context.py` remains the sole mechanical owner for
cross-checkout shape, repository identity, revision capture, generation,
Codex-home, mutation-policy, write-scope, refreshed-payload, and receipt facts.
It may prepare a fresh payload but may not accept repository movement.

The deep refresh seam is:

```python
prepare_cross_checkout_context_refresh(
    payload: Mapping[str, object],
) -> CrossCheckoutRefreshPreparation
```

`CrossCheckoutRefreshPreparation` contains
`planned_revisions: RepositoryRevisions`,
`live_revisions: RepositoryRevisions`, the exact `refreshed_payload`, and the
strictly parsed `refreshed_context: CrossCheckoutContext`. The operation accepts
no caller revision overrides or compatibility decision. Existing
`validate_write_scope(...)` remains the sole path-scope validator and consumes
the refreshed context separately.

`skills/work-batch/SKILL.md` owns the semantic queued-to-executing decision.
It consumes active planning state, reviewed commit ranges, changed paths, the
queued runway, and helper output to classify movement and either stop or adopt
a fresh live lease.

`skills/batch-runway/references/cross-checkout-context-v1.md` owns the shared
vocabulary and propagation contract. Planning and execution references consume
that contract; they must not copy helper validation logic or invent parallel
classification owners.

Slice 1 establishes the helper refresh interface. Slice 2 establishes planning
snapshot semantics. Slice 3 consumes both to define startup reconciliation and
per-handoff lease renewal. Slice 4 proves the joined contract and publishes the
linked feature versions. Stop if a later slice bypasses or duplicates the
owners established earlier.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker, reviewer, specialist, investigator, and Spark result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its other non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior.
Use the expanded convergence template only for expanding scope, significant
uncertainty, blockers, or final batch reporting.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/test-quality-review.md`

Overrides:

- None. The batch's ordinary single-root topology is a project value, not an
  execution-contract deviation.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

Required-green current baselines:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py`
  - Planning result: 21 passed and 31 subtests passed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_batch_lifecycle_guards.py`
  - Planning result: 5 passed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'cross_checkout_helper_is_installed_only_by_batch_runway or cross_checkout_consumers_share_the_temporary_runtime_contract or cross_checkout_generic_surfaces_remain_project_neutral'`
  - Planning result: 3 passed, 18 deselected, and 137 subtests passed.
- `.venv/bin/ruff check scripts/cross_checkout_context.py tests/test_cross_checkout_context.py tests/test_batch_lifecycle_guards.py tests/test_codex_features_manifest.py`
  - Planning result: passed.
- `.venv/bin/basedpyright scripts/cross_checkout_context.py`
  - Planning result: zero errors, warnings, or notes.
- `./install.sh --status`
  - Planning result: passed; all affected features are linked to this checkout.
- `./install.sh --dry-run`
  - Planning result: passed without writing installed state.
- `git diff --check`
  - Planning result: passed on the clean baseline.

Implementation-created proof, promoted to required-green by its creating slice:

- Slice 1 adds temporary-repository cases to
  `tests/test_cross_checkout_context.py` for planned/live revision capture,
  refreshed strict parsing, unchanged strict stale rejection, and movement
  after lease preparation.
- Slices 2 and 3 add lifecycle contract cases to
  `tests/test_batch_lifecycle_guards.py` for the four lifecycle concepts, three
  startup classifications, project-neutral controlled-path derivation,
  receipt fields, and recovery routing.
- Slice 4 adds implementation-created lifecycle assertions to the already
  required-green focused cross-checkout manifest subset. The command stays
  required-green before and after those assertions are added.

Known-red baseline, diagnostic only:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py`
  - Planning baseline: 3 failed, 18 passed, and 202 subtests passed.
  - Expected failures:
    `test_executable_work_source_boundary_is_explicit`,
    `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
    `test_work_batch_reconciles_same_batch_closeout`.
  - This command cannot block CCFG-30 and must not be promoted silently.

No slice worker may run a package install, installer mutation, candidate
checkout command, full project suite, generated-doc refresh, graph/index
refresh, or final validation unless its slice explicitly assigns that work.

## Shared Worker And Reviewer Briefs

Worker brief for every slice:

- You are the already-required `runway_worker`. Implement only the active slice
  from this runway; do not spawn, delegate to, or wait on another agent.
- Work only in `/home/alacasse/projects/codex-config` and only on active-slice
  allowed files. Keep the redesign candidate and unrelated planning artifacts
  read-only.
- Preserve exact strict handoff validation and the single helper/work-batch
  ownership boundary. Do not add a second parser, classifier, refresh helper,
  or lifecycle owner.
- Keep reusable skill text project-neutral. Use active state and explicit
  handoff values instead of codex-config paths or commands.
- Run only the focused validation assigned to the slice and return the
  registered v2 worker result with `verified_cross_checkout_context: null`.

Reviewer brief for every slice:

- The coordinator supplies the exact commit hash or task-scoped worktree diff
  basis. Echo it as `diff_basis` in the registered v2 reviewer result.
- Review only the active-slice diff against this runway and the CCFG-30 source
  note. Keep the redesign candidate read-only.
- Reject weakened exact parsing, ancestry-as-lease logic, self-referential
  runway refreshes, helper-owned compatibility decisions, project-specific
  reusable logic, silent scope replacement, or recovery that treats normal
  startup reconciliation as an anomaly.
- Check that tests protect observable lifecycle behavior and fail-closed
  boundaries instead of exact internal helper topology.
- Return the registered v2 reviewer result with
  `verified_cross_checkout_context: null` and a clear accept/fix/block verdict.

## Active Ledger

| Slice | Risk | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|
| 1. Helper refresh preparation | migration | Pending | None | Pending | Pending | Helper and temporary-repository proof | Preserve exact strict parser |
| 2. Planning snapshot contract | migration | Pending | None | Pending | Pending | Snapshot lifecycle guards | No self-referential rewrite |
| 3. Startup reconciliation and live leases | migration | Pending | None | Pending | Pending | Three classifications and receipt proof | `work-batch` owns acceptance |
| 4. Integrated routing and linked metadata | migration | Pending | None | Pending | Pending | Manifest, docs, installer checks, final validation | No candidate changes |

## Completed Slice Archive

None. Create `completed-slices.md` during execution and move each accepted slice
there after its commit receipt is complete.

## Slice 1: Add Helper-Owned Refresh Preparation

Risk: `migration`.

Scope:

- Extend `scripts/cross_checkout_context.py` with
  `prepare_cross_checkout_context_refresh(...)` and the immutable
  `CrossCheckoutRefreshPreparation` result described in the owner seam.
- Preserve the complete original payload facts while substituting only
  helper-captured live revisions in the refreshed payload.
- Pass the refreshed payload through `parse_cross_checkout_context` before
  returning it.
- Add temporary-repository tests covering the helper portion of the ten source
  scenarios.

Allowed files:

- `scripts/cross_checkout_context.py`
- `tests/test_cross_checkout_context.py`

Non-goals:

- No compatibility classification, planning-state reads, changed-path policy,
  execution acceptance, delegation, or closeout behavior.
- No skill, manifest, workflow-guide, installer, candidate, or planning-artifact
  edits.

Acceptance criteria:

- `parse_cross_checkout_context` still rejects any planned revision that does
  not equal the corresponding live `HEAD`.
- Refresh preparation validates exact payload shape, absolute roots, repository
  identities, generation binding, active Codex home, and mutation policy without
  pretending stale revisions are current.
- The result records planned and live revision sets and exposes a refreshed
  payload that passes the unchanged strict parser immediately.
- The operation accepts no caller revision, root, generation, Codex-home,
  mutation-policy, or write-scope override fields. Existing
  `validate_write_scope(...)` remains separate and unchanged.
- Tests prove unchanged-head refresh, queue-establishment advancement,
  implementation advancement, and post-lease movement rejection.
- Representative CCFG-19/CCFG-20-shaped v1 payloads remain readable as planning
  snapshot inputs; after repository movement they are not accepted as current
  execution leases without refresh preparation and strict reparse.
- The helper offers facts only; no boolean or enum in its result claims that an
  intervening range is compatible or accepted.

Validation:

- Run the required-green cross-checkout test command.
- Run Ruff on the two allowed files.
- Run basedpyright on `scripts/cross_checkout_context.py`.
- Run `git diff --check` and explicitly inspect every new untracked file with
  `git diff --no-index /dev/null <path>`.
- Test quality review: `delta-only`.

Commit message: `feat: prepare live cross-checkout leases`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
confirm exact strict rejection is unchanged and the helper has no lifecycle
authority.

Stop conditions:

- Stop if refresh requires weakening or bypassing the strict parser.
- Stop if the helper must inspect planning state or decide compatibility.
- Stop if a second payload schema or manual revision editor appears.

## Slice 2: Define Planning Snapshot Semantics

Risk: `migration`.

Scope:

- Update the shared cross-checkout contract to distinguish planning snapshot,
  startup reconciliation, live execution lease, and execution receipt.
- Require `plan-batch` and create-spec guidance to label persisted revisions as
  historical planning evidence rather than a promise about future live `HEAD`.
- Forbid rewriting the queued runway merely to embed the commit that contains
  the runway.
- Add lifecycle guard tests for the producer-side contract.

Allowed files:

- `skills/plan-batch/SKILL.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/create-spec.md`
- `tests/test_batch_lifecycle_guards.py`

Non-goals:

- No startup classification or execution-routing change yet.
- No helper, manifest, workflow-guide, candidate, or active planning-artifact
  edits.

Acceptance criteria:

- Cross-checkout create-spec persists the complete validated plan-time payload
  and canonical planning root as a `planning snapshot`.
- The snapshot remains immutable historical evidence after its containing plan
  commit or compatible between-flight commits advance `HEAD`.
- No instruction promises that a persisted snapshot remains a valid live lease.
- No instruction tells the coordinator to hand-edit revisions or commit an
  endless self-referential refresh.
- Strict context routing remains conditional and adds no step to ordinary
  single-root work.
- Reusable text contains no codex-config-specific path, command, cache, or
  finding name.

Validation:

- Run the required-green lifecycle-guard command.
- Run the required-green focused manifest subset from the validation section;
  Slice 4 owns its new assertions and version changes.
- Run Ruff on `tests/test_batch_lifecycle_guards.py`.
- Run `git diff --check` and explicit untracked-file review.
- Test quality review: `delta-only`.

Commit message: `docs: define cross-checkout planning snapshots`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
trace every producer statement to the shared vocabulary and reject duplicated
revision semantics.

Stop conditions:

- Stop if the snapshot can silently change selected scope.
- Stop if producer guidance weakens delegation-time exactness.
- Stop if the implementation introduces project-specific routing.

## Slice 3: Reconcile Startup And Renew Live Leases

Risk: `migration`.

Scope:

- Make `work-batch` own normal queued-to-executing startup reconciliation before
  generic unexpected-movement recovery.
- Define exactly three classifications:
  `expected-queue-establishment`, `compatible-between-flight-change`, and
  `conflicting-between-flight-change`.
- Route accepted movement through the Slice 1 helper refresh operation, then
  require a new strict lease before every worker and reviewer handoff.
- Record compact startup reconciliation and execution-receipt facts.
- Add lifecycle guard tests for classification, routing, project neutrality,
  and recovery boundaries.

Allowed files:

- `skills/work-batch/SKILL.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `tests/test_batch_lifecycle_guards.py`

Non-goals:

- No automated arbitrary-change acceptance or source-code compatibility engine.
- No selection, dispatch, replanning, closeout, or successor behavior.
- No helper, manifest, workflow-guide, candidate, or active planning-artifact
  edits.

Acceptance criteria:

- Startup first confirms through Planning State Diagnostic that the same runway
  is still the only queued or active batch.
- The coordinator captures live roots, branches, revisions, worktree status,
  helper path, Codex home, and generation before classification.
- `expected-queue-establishment` accepts only canonical active-state files and
  the same batch's dispatch/runway while that runway remains current.
- `compatible-between-flight-change` requires reviewed commit ranges and paths
  that do not alter controlled owners, the queued runway, its source finding or
  source note, its acceptance contract, helper/contract owners, declared roots,
  baselines, or pending implementation allowlists.
- `conflicting-between-flight-change` stops on overlap, identity drift, dirty
  conflict, invalidated baseline, or unknown classification.
- Controlled paths are derived from active state, the queued runway and its
  source finding/note, manifest ownership, installed helper ownership, and
  slice allowlists.
- Accepted startup movement is not an orchestration anomaly; post-lease or
  unexplained movement remains fail-closed recovery.
- Every subsequent worker and reviewer handoff receives a newly prepared exact
  live lease after any accepted coordinator commit.
- Startup evidence records planned and accepted live stable/implementation
  revisions, classification, reviewed ranges, changed-path basis, and runway
  path. Execution receipts record the live lease, never the planning snapshot.

Validation:

- Run the required-green lifecycle-guard command.
- Run the required-green cross-checkout test command to protect the helper seam.
- Run Ruff on `tests/test_batch_lifecycle_guards.py`.
- Run `git diff --check` and explicit untracked-file review.
- Test quality review: `delta-only`.

Commit message: `feat: reconcile queued cross-checkout execution`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
verify `work-batch` owns semantic acceptance, helper refresh remains mechanical,
and recovery starts only after normal reconciliation cannot proceed.

Stop conditions:

- Stop if a fourth classification or implicit fallback is introduced.
- Stop if compatibility is inferred without reviewing commits and paths.
- Stop if accepted movement can broaden or replace the queued runway.
- Stop if post-lease movement can reach delegation without a fresh strict lease.

## Slice 4: Join Routing, Metadata, And User Guidance

Risk: `migration`.

Scope:

- Extend the focused manifest contract to join helper ownership, consumer
  routing, planning snapshots, startup reconciliation, live leases, receipts,
  project neutrality, and the temporary CCFG-29 deletion condition.
- Update linked feature versions for affected installed surfaces.
- Explain the normal plan-commit flight boundary in the workflow guide.
- Record the meaningful installed workflow change in the changelog.
- Run linked installed-state and final validation without installing or
  switching generations.

Allowed files:

- `tests/test_codex_features_manifest.py`
- `codex-features.json`
- `docs/workflow-guide.md`
- `CHANGELOG.md`

Expected feature versions:

- `plan-batch`: `1.0.6`.
- `work-batch`: `1.0.7`.
- `batch-runway`: `1.5.2`.

Non-goals:

- No `install.sh` implementation change, installation mutation, candidate
  installation, default-generation switch, or CCFG-29 bridge deletion.
- No remediation of unrelated manifest wording assertions.
- No helper or skill-contract redesign beyond integration defects found by the
  joined proof; route such defects back to the owning prior slice.

Acceptance criteria:

- Manifest assertions fail if any affected consumer loses the joined lifecycle
  vocabulary, helper ownership, project-neutral rule, or deletion condition.
- Feature versions and manifest tests agree exactly.
- The workflow guide states that committing a queued plan is a normal flight
  boundary, that startup classifies movement, and that delegation still uses an
  exact live lease.
- The changelog names the behavior change without embedding project-local
  runtime values in reusable contracts.
- `./install.sh --status` confirms all affected features remain linked to the
  stable checkout.
- `./install.sh --dry-run` reports no required installed-state mutation.
- The redesign candidate worktree and revision remain unchanged by this batch.

Validation:

- Extend and run the already required-green focused manifest subset with the new
  Slice 4 lifecycle assertions.
- Run the required-green cross-checkout and lifecycle-guard commands.
- Run Ruff on all changed Python and test files.
- Run basedpyright on `scripts/cross_checkout_context.py`.
- Run `./install.sh --status` and `./install.sh --dry-run`.
- Run the full manifest command as known-red diagnostic only and compare its
  failures with the planning baseline.
- Run `git diff --check` and explicit untracked-file review.
- Test quality review: `delta-only`.

Commit message: `docs: publish cross-flight execution lifecycle`.

Subagent briefs: use the shared worker and reviewer briefs. Final review must
cover the exact Slice 1 through 4 commit range plus the linked installed-state
evidence and confirm the candidate checkout was untouched.

Stop conditions:

- Stop if version bumps imply a candidate install or generation switch.
- Stop if the focused manifest contract becomes an exact-prose topology lock
  instead of protecting lifecycle ownership and observable routing.
- Stop if the known-red full manifest is silently promoted or its unrelated
  failures are absorbed.

## Final Validation

Run from `/home/alacasse/projects/codex-config` after all four accepted slice
commits:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_batch_lifecycle_guards.py`
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'cross_checkout_helper_is_installed_only_by_batch_runway or cross_checkout_consumers_share_the_temporary_runtime_contract or cross_checkout_generic_surfaces_remain_project_neutral'`
- `.venv/bin/ruff check scripts/cross_checkout_context.py tests/test_cross_checkout_context.py tests/test_batch_lifecycle_guards.py tests/test_codex_features_manifest.py`
- `.venv/bin/basedpyright scripts/cross_checkout_context.py`
- `./install.sh --status`
- `./install.sh --dry-run`
- `git diff --check`
- Explicit `git diff --no-index /dev/null <path>` review for every new untracked
  file before it is committed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py` as known-red diagnostic only.

The final coordinator must read the temporary-repository scenario assertions,
focused manifest result, installed-state output, completed-slice archive, and
independent final review before producing `closeout.md`.

## Final Acceptance And Closeout

- All ten CCFG-30 regression scenarios are represented by behavioral or
  contract tests and pass on their required-green surfaces.
- Exact strict delegation validation remains fail-closed.
- Queue-establishment commits and explicitly reviewed compatible movement no
  longer enter generic anomaly recovery.
- Conflicting or unknown movement stops before delegation.
- Every handoff receipt identifies a current live lease.
- The queued runway remains the only selected scope throughout execution.
- Reusable workflow contracts remain project-neutral.
- The stable linked feature versions are coherent and require no installation.
- The redesign candidate remains unchanged.
- Program closeout reconciles CCFG-30 only and selects no successor.

## Stop Conditions

- Stop on any weakened strict root, revision, generation, Codex-home, or
  write-scope validation.
- Stop if helper refresh preparation acquires semantic lifecycle authority.
- Stop if startup reconciliation accepts an unreviewed or unclassifiable range.
- Stop if a queued snapshot is rewritten to chase `HEAD`.
- Stop if selected scope changes during reconciliation.
- Stop on candidate checkout mutation, installed-state mutation, generation
  switch, or CCFG-21 through CCFG-29 scope.
- Stop if a test preserves internal helper topology instead of observable
  lifecycle behavior without a documented external contract.
- Stop closeout before selecting or preparing successor work.
