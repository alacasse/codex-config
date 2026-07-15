# CCFG-32 Planning-State Queue Currentness Runway

## Purpose

Make Planning State the sole authority for queue currentness and remove the
remaining Git archaeology that asks the cross-checkout helper to reconstruct a
semantic planning transaction. Keep only the material first-handoff checks
needed to produce a fresh strict live context, preserve exact later handoff
leases and receipts, and reduce the temporary bridge rather than replacing the
deleted logic with a stronger transaction protocol.

This runway covers only CCFG-32. It stops before implementation in the planning
session that creates it.

## Batch Kind And Slice Risk Contract

- Batch kind: `destructive-cleanup`.
- Slice 1 risk: `contract-narrowing`; remove `queue_transaction_paths`, Git
  commit-range and worktree path inference, planning-file fingerprints,
  workflow obligations that supply or interpret those facts, and tests whose
  only purpose is to preserve those semantics.
- Authorized narrowing: GitHub issue #55, authored by the repository owner and
  ingested with `ready-for-agent`, explicitly authorizes the deletion. Issue
  #54 is recorded in the source packet as permitting the one-slice shape.
- Approval gate: immediately before execution, Planning State must identify
  this exact runway as the sole queued or active batch, CCFG-32 must remain
  `Pending`, and no amendment, supersession, abandonment, or source change may
  have withdrawn the authorization.
- Preserved contract: strict context parsing, exact repository roots,
  generation and active `CODEX_HOME`, expected implementation baseline,
  current live revisions, movement-during-preparation rejection, fresh leases
  for every worker/reviewer handoff, separate write-scope validation, verified
  result echo, accepted-action receipts, and exact reviewer diff bases.

## Current Baseline And Assumptions

- Planning State `current --root docs/plans --format json` and
  `validate --root docs/plans --format json` passed with no selected, queued, or
  active batch before selection and only the two accepted redirect warnings.
- CCFG-32 is sourced by
  `docs/plans/programs/codex-config/findings/github-issue-55-planning-state-queue-currentness.md`.
- The planning baseline is stable `master` commit
  `6ede5b2d56bf27939a6ccc0526a0178ee6a58eea`.
- The pre-existing planning worktree contains only the CCFG-32 intake edits to
  program `CURRENT.md`, `LEDGER.md`, and the source finding. They are in-scope
  planning state and must be preserved.
- `scripts/cross_checkout_context.py` currently exports
  `preflight_cross_checkout_live_lease(...)` with caller-supplied queue paths
  and uses commit-range paths, worktree paths, and file fingerprints to decide
  whether planning movement is an exact queue transaction.
- `work-batch` is the sole current startup consumer of that preflight.
  `prepare_cross_checkout_context_refresh(...)` remains separately required for
  later handoffs because accepted coordinator commits may legitimately advance
  the implementation repository between leases.
- This is ordinary single-root execution in
  `/home/alacasse/projects/codex-config`; no strict cross-checkout planning
  snapshot applies to this batch.
- `graphify-out/graph.json` is absent, so no graph generation or graph refresh
  belongs to this planning-only or execution scope.

## Batch Non-Goals

- Do not change `scripts/planning_state.py`, its schemas, or its CLI.
- Do not add transaction IDs, digests, same-path mutation schemas, branch
  fields, or stronger planning-currentness protocols; CCFG-21 and CCFG-25 own
  future planning contract work.
- Do not delete `cross-checkout-context/v1`, its strict parser, pre-creation
  transition behavior, receipt types, or the complete helper; CCFG-29 owns
  final bridge removal.
- Do not weaken first-handoff implementation-baseline checks, movement during
  preparation checks, later per-handoff refresh, write-scope validation,
  verified result echo, accepted-action receipts, or reviewer diff bases.
- Do not modify historical CCFG-30/CCFG-31 artifacts, the command-owner redesign
  candidate, agent TOMLs, installer implementation, installed runtime state, or
  default generation.
- Do not absorb unrelated known-red manifest wording tests.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-32-planning-state-queue-currentness/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`.
- Execution repository: `/home/alacasse/projects/codex-config`.
- Cross-checkout execution context for this batch: not applicable; ordinary
  single-root execution.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway` because this narrows an installed helper API and
  fail-closed execution-safety contract.
- Integration harness: temporary Git repositories in
  `tests/test_cross_checkout_context.py`, joined lifecycle ownership guards,
  and focused manifest/installer routing checks.
- Harness output: temporary directories and stdout/stderr only; no durable
  generated output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused stable-repository implementation commit,
  followed by coordinator-owned same-batch closeout artifacts if validation and
  review are accepted.
- Dirty-file constraints: preserve the queueing artifacts and unrelated user
  changes; stage only active-slice paths and stop on overlap.

## Owner Seam And Slice Shape

Planning State `current` and `validate` own semantic currentness: selected or
queued batch identity, current dispatch/runway/source scope, amendment,
replacement, supersession, abandonment, replanning, and permission to consume
that planning state.

`scripts/cross_checkout_context.py` remains the mechanical owner for exact
roots, revisions, generation/Codex-home binding, strict parsing, movement
during preparation, write scope, and receipt facts. Its startup preflight keeps
the existing `ready | blocked` result but no longer accepts or reconstructs
queue paths. It compares the implementation repository to the expected
historical baseline, prepares current toolchain/planning revisions, rechecks
movement during preparation, and returns a strict context only when ready.

Retain both public helper APIs. `work-batch` is the named current caller of
`preflight_cross_checkout_live_lease(...)` before the first strict handoff;
later handoffs use `prepare_cross_checkout_context_refresh(...)` after exact
accepted coordinator actions. Folding the startup wrapper into refresh would
either move the first-handoff baseline comparison into workflow prose or
weaken later refresh semantics. CCFG-29 final integration remains the removal
condition for both APIs.

`slice_shape`: one slice. The helper deletion, contract rewrite, behavioral
test migration, release metadata, and changelog have one owner, risk,
validation, rollback, and acceptance boundary. There is no valid independently
shippable intermediate in which the helper and installed workflow contracts
disagree.

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
- `skills/dead-surface-audit/SKILL.md`

Overrides:

- The approval gate above must be rechecked before destructive execution.
- Slice 1 and final-range review require focused `test-quality-review`.
  Material preserved-safety gaps block commit or closeout until corrected and
  re-reviewed.
- The batch's ordinary single-root topology is a project value, not an
  execution-contract deviation.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

Required-green current baselines:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py`
  - Planning result: 39 passed and 46 subtests passed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_batch_lifecycle_guards.py`
  - Planning result: 12 passed and 27 subtests passed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'cross_checkout_helper_is_installed_only_by_batch_runway or cross_checkout_consumers_share_the_temporary_runtime_contract or cross_checkout_generic_surfaces_remain_project_neutral'`
  - Planning result: 3 passed, 18 deselected, and 31 subtests passed.
- `.venv/bin/ruff check scripts/cross_checkout_context.py tests/test_cross_checkout_context.py tests/test_batch_lifecycle_guards.py tests/test_codex_features_manifest.py`
  - Planning result: passed.
- `.venv/bin/basedpyright scripts/cross_checkout_context.py`
  - Planning result: zero errors, warnings, or notes.
- `./install.sh --status`
  - Planning result: exited successfully. Installed version metadata already
    trails the manifest for several repo-owned skills; execution must report,
    not silently repair, that pre-existing state.
- `./install.sh --dry-run`
  - Planning result: exited successfully, reported every target link as `ok`,
    surfaced the pre-existing version updates, and did not write installed
    state.
- `git diff --check`
  - Planning result: passed on tracked intake edits.

Slice-owned acceptance outcomes required before the existing validation
commands can remain `required-green`:

- Startup preflight has no canonical-planning-root or queue-transaction-path
  input and still returns exactly `status`, diagnostic `reason`, and
  `live_context`.
- Green Planning State plus unchanged implementation baseline can produce a
  fresh strict context when toolchain or canonical-planning `HEAD` advanced
  after the planning snapshot.
- Implementation movement without an accepted prior action, identity/binding
  mismatch, and repository movement during preparation remain blocked.
- Strict parsing, fresh later handoffs, post-lease movement rejection,
  write-scope validation, result echo, and receipts remain behaviorally proven.
- Queue commit-range collection, worktree path classification, file
  fingerprinting, and their now-unused helpers/imports are absent.
- Workflow contracts make Planning State the sole semantic currentness owner,
  name `work-batch` as the startup-preflight caller, and retain CCFG-29 as the
  removal condition.
- `codex-features.json` publishes `work-batch` `1.0.9` and `batch-runway`
  `1.5.5`; `plan-batch` remains `1.0.7` because its planning-snapshot contract
  does not change.
- Combined production-helper and reusable workflow-contract code has a negative
  line delta against baseline
  `6ede5b2d56bf27939a6ccc0526a0178ee6a58eea`.

Known-red baseline, diagnostic only:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py`
  - Planning baseline: 3 failed, 18 passed, and 96 subtests passed.
  - Expected failures:
    `test_executable_work_source_boundary_is_explicit`,
    `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
    `test_work_batch_reconciles_same_batch_closeout`.
  - These unrelated exact-wording failures are not CCFG-32 remediation scope
    and must not be silently promoted or absorbed.

No slice worker may run a package install, installer mutation, candidate
checkout command, generation switch, full project suite, generated-doc refresh,
graph/index refresh, or coordinator-owned final validation.

## Deletion Evidence And Test Quality

Apply the canonical `dead-surface-audit` vocabulary before deleting assertions:

- `delete-now`: committed/uncommitted/combined queue-shape readiness, exact
  queue-path matching, planning-path fingerprint/rewrite detection, unmerged
  planning-path classification, and prose asserting caller-supplied queue
  transactions. These protect the removed Git-derived planning semantics, not
  an external contract.
- `migrate-tests-first`: startup implementation-baseline mismatch, strict
  identity/binding mismatch, movement during preparation, context expiry, and
  Planning State versus mechanical-helper ownership. Rewrite these around the
  narrowed preflight before deleting old queue-shaped fixtures.
- `keep`: strict parsing, roots, generation/Codex-home binding, later refresh,
  write scope, result echo, receipts, reviewer diff bases, pre-creation
  transition, and project-neutral routing behavior.
- `human-contract-decision`: none is expected under issue #55. If any deleted
  test exposes undocumented external support, stop for user direction.

Test quality review: `focused` for Slice 1 and the final implementation range.
The review must confirm that every preserved invariant has behavioral
regression coverage and that no material handoff-safety assertion was deleted
without replacement.

## Shared Worker And Reviewer Briefs

Worker brief:

- The spawned `runway_worker` is already the required coding subagent for this
  slice. It must implement only this slice and must not spawn, delegate to, or
  wait on additional subagents.
- Read this runway and dispatch, make the smallest deletion-biased change that
  satisfies the accepted outcome, and retain both helper APIs for their named
  current callers and CCFG-29 removal condition.
- Preserve the queueing artifacts, unrelated dirty files, historical CCFG-30/
  CCFG-31 artifacts, candidate work, CCFG-21/CCFG-25/CCFG-29 ownership, and
  installed runtime state.
- Do not run coordinator-owned final validation, independent review, ledger
  updates, commits, installs, or cleanup.
- Return the registered v2 worker result with
  `verified_cross_checkout_context: null` because this is ordinary single-root
  work.

Reviewer brief:

- The coordinator must provide the exact task-scoped worktree diff before
  commit or exact implementation commit hash after commit. The spawned
  `runway_reviewer` must echo that `diff_basis` in compact YAML.
- Review for Planning State as the sole currentness owner, absence of Git-
  derived queue semantics, preserved material startup and per-handoff safety,
  one named caller/removal condition per retained API, negative combined code
  delta, project neutrality, and no historical/candidate drift.
- Reject new planning schemas, digests, transaction IDs, movement taxonomies,
  scanners, compatibility paths, queue fingerprints, weakened implementation-
  baseline checks, or topology-only tests.
- Return `verified_cross_checkout_context: null` because review is ordinary
  single-root work.

## Active Ledger

| Slice | Risk | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|
| _No pending slices._ | | | | | | Final closeout commit | Slice 1 is archived in `completed-slices.md`. |

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Delete Git-derived queue currentness | `7ef07dc` | success | `completed-slices.md`; focused and final validation; clean test-quality, dead-surface, and exact-range reviews |

## Slice 1: Delete Git-Derived Queue Currentness

### Scope

Delete queue-transaction inputs and inference from the helper and reusable
workflow contracts. Retain the first-handoff `ready | blocked` wrapper only for
material execution integrity, migrate behavioral coverage, and publish the two
affected feature versions.

### Allowed Files

- `scripts/cross_checkout_context.py`
- `skills/work-batch/SKILL.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `tests/test_cross_checkout_context.py`
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_codex_features_manifest.py`
- `codex-features.json`
- `CHANGELOG.md`

### Non-Goals

- No Planning State implementation/schema change.
- No complete bridge deletion or pre-creation behavior change.
- No candidate, historical planning, agent, installer implementation, runtime
  installation, generation, or unrelated manifest-baseline change.
- No compatibility wrapper, deprecated queue argument, or fallback inference.

### Acceptance Criteria

- `preflight_cross_checkout_live_lease(...)` accepts only the immutable strict
  planning snapshot and has no queue-path or planning-root parameter.
- The preflight retains the exact three-field result, blocks unexpected
  implementation-baseline movement, prepares current toolchain/planning
  revisions, and detects repository movement during preparation.
- Later accepted implementation movement remains supported only through
  `prepare_cross_checkout_context_refresh(...)` plus the existing exact
  accepted-action and receipt workflow.
- `_capture_queue_transaction_paths`, `_capture_worktree_paths`,
  `_fingerprint_queue_transaction_state`, `_run_git_paths`, `_run_git_bytes`,
  `hashlib`, `stat`, and imports used only by them are deleted.
  `_require_ancestor` remains because pre-creation candidate validation still
  uses it.
- Workflow prose requires green Planning State before mechanical helper use and
  never asks Git or the caller to establish semantic queue currentness.
- Tests delete queue-shape classifications and behaviorally preserve every
  material handoff invariant listed above.
- `work-batch` is the named startup caller; CCFG-29 final integration is the
  removal condition for both retained helper APIs.
- `work-batch` is version `1.0.9`, `batch-runway` is version `1.5.5`, linked
  installation routing remains unchanged, and no install occurs.
- Combined production-helper and reusable workflow-contract code has a negative
  line delta against the recorded baseline.
- `CHANGELOG.md` records the problem, decision, and expected effect.

### Validation

Status: all commands below are `required-green` except the explicitly named
diagnostic-only full manifest baseline.

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py`
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_batch_lifecycle_guards.py`
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'cross_checkout_helper_is_installed_only_by_batch_runway or cross_checkout_consumers_share_the_temporary_runtime_contract or cross_checkout_generic_surfaces_remain_project_neutral'`
- `.venv/bin/ruff check scripts/cross_checkout_context.py tests/test_cross_checkout_context.py tests/test_batch_lifecycle_guards.py tests/test_codex_features_manifest.py`
- `.venv/bin/basedpyright scripts/cross_checkout_context.py`
- `./install.sh --status`
- `./install.sh --dry-run`
- `git diff --check`
- `git diff --numstat 6ede5b2d56bf27939a6ccc0526a0178ee6a58eea -- scripts/cross_checkout_context.py skills/work-batch/SKILL.md skills/batch-runway/references/cross-checkout-context-v1.md skills/batch-runway/references/execute-spec.md skills/batch-runway/references/execute-slice-core-v1.md skills/batch-runway/references/execute-recovery-v1.md | awk 'BEGIN { added = 0; deleted = 0 } { added += $1; deleted += $2 } END { print "added=" added, "deleted=" deleted; exit !(deleted > added) }'`
  - Required-green interpretation: the production helper plus the five
    reusable workflow-contract files have more deleted than added lines.
- Diagnostic only:
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py`.
- Test quality review: `focused`.

The worker must not run project-level installs, candidate commands, generation
switches, full suites, graph/index refreshes, or coordinator-owned final
validation.

### Commit

- Commit message: `refactor: make planning state own queue currentness`
- Commit only after focused validation, focused test-quality review, and an
  independent clean `runway_reviewer` result.

### Stop Conditions

Stop if the Planning State gate is not exact; any queue-currentness inference
survives without a named external contract; material identity, baseline,
movement, lease, scope, result, receipt, or reviewer-diff safety weakens; a
retained surface needs `human-contract-decision`; the combined code delta is not
negative without explicit user approval; validation reveals a new regression;
or any file outside the allowed set must change.

## Final Validation

After the slice commit and before closeout, the coordinator must:

1. Re-run both focused pytest suites, the focused manifest routing filter,
   Ruff, basedpyright, `./install.sh --status`, `./install.sh --dry-run`, and
   `git diff --check`.
2. Re-run the full manifest suite as diagnostic-only evidence and confirm no
   new failure class beyond the named three-test baseline.
3. Confirm through static search that queue-transaction inputs, capture,
   classification, and fingerprint machinery are absent from active helper and
   workflow-contract surfaces.
4. Confirm exact feature versions and unchanged symlink routing without
   installing or writing runtime state.
5. Confirm the negative combined production-helper/workflow-contract line
   delta against the recorded baseline.
6. Run focused `test-quality-review` and independent final `runway_reviewer`
   review over the exact implementation commit range.
7. Re-run Planning State `current` and `validate`, write same-batch closeout
   evidence, reconcile CCFG-32 only, and stop without selecting a successor.

## Stop Conditions

- Stop on scope drift, unresolved ambiguity, dirty-file overlap, withdrawn
  authorization, new validation regression, missing subagent support, or a
  material preserved-safety gap.
- Stop if implementation starts in the planning session that created this
  runway.
- Stop if closeout selects, dispatches, refreshes, creates, or prepares any
  successor work.
