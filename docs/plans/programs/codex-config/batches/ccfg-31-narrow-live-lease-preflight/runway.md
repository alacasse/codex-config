# CCFG-31 Narrow Live-Lease Preflight Runway

## Purpose

Replace CCFG-30's broad startup classifications and controlled-path protocol
with the smallest mechanical live-lease preflight that returns only `ready` or
`blocked`. Keep the helper mechanical and fail-closed, keep semantic authority
in `work-batch`, preserve exact short-lived leases for every worker and
reviewer handoff, and delete prose/topology tests that do not protect observable
safety behavior.

This runway covers only CCFG-31. It stops before implementation in the planning
session that creates it.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1 risk: `migration`; add and prove the narrow mechanical preflight
  while retaining the strict refresh operation used for later handoffs.
- Slice 2 risk: `contract-narrowing`; migrate consumers and delete the broad
  classification, range/path-review, prose, and topology-test protocol.
- Authorized narrowing: replace the broad coordinator-facing startup protocol
  with `status: ready | blocked`, `reason: string`, and
  `live_context: object | null`; remove the three movement classifications,
  general compatible-range review, broad controlled-path taxonomy, duplicated
  lifecycle exposition, and exact-prose/classification-count/topology tests.
- Preserved contract: strict context parsing, exact identity, fresh
  worker/reviewer leases, post-lease movement rejection, result echo,
  write-scope validation, actual-lease receipts, and fail-closed ambiguity.
- Slice 2 approval gate: GitHub issue #53, authored by the repository owner and
  labeled `ready-for-agent`, is the explicit deletion authorization. Before execution,
  Planning State must still identify this exact runway as the sole queued or
  active batch, CCFG-31 must remain `Pending`, and no amendment, supersession,
  abandonment, or issue change may have withdrawn the authorization.

## Current Baseline And Assumptions

- Planning State `current --root docs/plans` and `validate --root docs/plans`
  passed before selection with no selected, queued, or active batch.
- CCFG-31 is sourced by
  `docs/plans/programs/codex-config/findings/github-issue-53-narrow-live-lease-preflight.md`
  and GitHub issue #53. The issue was open, `ready-for-agent`, and last updated
  at `2026-07-14T19:22:11Z` when planned.
- The planning worktree was clean before dispatch/runway creation.
- `scripts/cross_checkout_context.py` currently exports
  `CrossCheckoutRefreshPreparation` and
  `prepare_cross_checkout_context_refresh(...)`, which refresh live revisions
  but leave the broad acceptance decision to prose in `work-batch`.
- `skills/work-batch/SKILL.md` and the shared bridge contract currently define
  three movement classifications and broad controlled-path/review rules.
- `tests/test_batch_lifecycle_guards.py` and
  `tests/test_codex_features_manifest.py` currently contain exact wording,
  classification-count, section-topology, and duplicated-consumer assertions
  in addition to real lease/receipt safety checks.
- Historical CCFG-30 planning artifacts are evidence only and remain unchanged.
- This is ordinary single-root execution in
  `/home/alacasse/projects/codex-config`. The batch edits the temporary bridge
  contract but does not itself use a strict cross-checkout execution context.

## Batch Non-Goals

- Do not weaken or replace the strict context parser.
- Do not accept ancestry, approximate identity, stale revisions, arbitrary
  compatible ranges, or unknown movement.
- Do not move planning-currentness or business-scope authority into the helper.
- Do not redesign Planning State, planning transactions, dirty-file policy,
  agent result contracts, execution receipts, or command ownership beyond the
  minimum deletion required by CCFG-31.
- Do not add a parallel bridge version, lifecycle state, movement taxonomy,
  compatibility matrix, repository scanner, public command, agent, durable
  planning artifact, planning schema, or reusable abstraction beyond the
  narrow helper seam.
- Do not modify CCFG-30 historical dispatch/runway/closeout evidence, CCFG-21
  through CCFG-29, the redesign candidate checkout, installed state, default
  generation, or the final CCFG-29 bridge-removal boundary.
- Do not fix the unrelated known-red full manifest assertions.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/`.
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
- Runway density: `full-runway` because this changes public workflow behavior,
  an installed helper surface, destructive contract semantics, and fail-closed
  execution safety.
- Integration harness: temporary Git repositories in
  `tests/test_cross_checkout_context.py`, joined lifecycle guards, and focused
  manifest/installer routing checks.
- Harness output: temporary directories and stdout/stderr only; no durable
  generated output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused stable-repository commit per accepted slice,
  followed by coordinator-owned same-batch closeout artifacts if execution and
  review are accepted.
- Dirty-file constraints: preserve queueing artifacts and unrelated user
  changes; stage only active-slice paths and stop on overlap.

## Owner Seam And Slice Shape

`scripts/cross_checkout_context.py` is the sole mechanical owner for repository
identity, exact revision capture, generation and Codex-home binding, strict
payload construction/parsing, movement proof, and write-scope facts. Its normal
preflight result exposes only `ready` or `blocked`; it never decides business
currentness, scope replacement, recovery, or delegation.

`skills/work-batch/SKILL.md` remains the semantic owner. It confirms the same
queued runway and source scope through Planning State, supplies the exact
same-batch queue transaction paths, treats `blocked` as a stop, and retains all
proceed, recovery, delegation, commit, receipt, closeout, and successor-stop
authority.

The shared bridge reference is the one canonical temporary consumer contract.
Planning, execution, and recovery consumers keep only their owner-specific
obligations and a link to that contract.

`slice_shape`: two slices. `1 -> 2` is a producer/consumer boundary: Slice 1
adds a narrow preflight beside the still-required strict refresh operation and
proves the new API with temporary repositories. That intermediate is valid and
testable while existing consumers retain their current behavior. Slice 2 then
adopts the new API, deletes the old protocol and test-retained topology, and
updates installed metadata. No third slice has an independent owner, risk,
validation, or rollback boundary.

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

- The approval gate above must be rechecked before destructive execution.
- Slice 1 uses delta-only `test-quality-review`; Slice 2 and final closeout use
  focused `test-quality-review`. Any material
  preserved-safety gap is blocking until corrected and re-reviewed.
- The batch's ordinary single-root topology is a project value, not an
  execution-contract deviation.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

Required-green current baselines:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py`
  - Planning result: 27 passed and 32 subtests passed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_batch_lifecycle_guards.py`
  - Planning result: 12 passed and 29 subtests passed.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'cross_checkout_helper_is_installed_only_by_batch_runway or cross_checkout_consumers_share_the_temporary_runtime_contract or cross_checkout_generic_surfaces_remain_project_neutral'`
  - Planning result: 3 passed, 18 deselected, and 164 subtests passed.
- `.venv/bin/ruff check scripts/cross_checkout_context.py tests/test_cross_checkout_context.py tests/test_batch_lifecycle_guards.py tests/test_codex_features_manifest.py`
  - Planning result: passed.
- `.venv/bin/basedpyright scripts/cross_checkout_context.py`
  - Planning result: zero errors, warnings, or notes.
- `./install.sh --status`
  - Planning result: exited successfully. Installed version metadata already
    trails the manifest for `architecture-program-runway`, `legacy-removal`,
    `batch-runway`, `plan-batch`, `work-batch`, and `port-by-contract`; this is
    not a no-drift assertion and execution must report, not silently repair,
    that state.
- `./install.sh --dry-run`
  - Planning result: exited successfully, reported every target link as `ok`,
    surfaced the same pre-existing version updates, and did not write installed
    state.
- `git diff --check`
  - Planning result: passed on the clean baseline.

Implementation-created proof, promoted to required-green by Slice 1:

- Temporary-repository tests for unchanged, committed, uncommitted, and combined
  same-batch queue establishment returning `ready` with a fresh strict context.
- Temporary-repository tests for every issue-listed identity, scope, movement,
  ambiguity, and stale-selection condition returning `blocked` before
  delegation.
- Runtime tests proving post-preflight movement, stale lease reuse, mismatched
  result echo, write-scope violation, and dishonest receipt evidence remain
  fail-closed.
- The narrow preflight's exact result schema and mechanical owner boundary.

Implementation-created proof, promoted to required-green by Slice 2:

- Contract tests proving consumers reference one canonical bridge, keep only
  owner-specific obligations, and do not preserve the old classification table
  or full lifecycle topology.
- Feature-version and installation-routing checks for expected manifest
  versions `plan-batch` `1.0.7`, `work-batch` `1.0.8`, and `batch-runway`
  `1.5.4`.

Known-red baseline, diagnostic only:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py`
  - Planning baseline: 3 failed, 18 passed, and 229 subtests passed.
  - Expected failures:
    `test_executable_work_source_boundary_is_explicit`,
    `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
    `test_work_batch_reconciles_same_batch_closeout`.
  - These unrelated exact-wording failures are not CCFG-31 remediation scope and
    must not be silently promoted or absorbed.

No slice worker may run a package install, installer mutation, candidate
checkout command, generation switch, full project suite, generated-doc refresh,
graph/index refresh, or final validation unless the slice explicitly assigns
that command.

## Deletion Evidence And Test Quality

Before removing a test assertion, classify it using the canonical
`dead-surface-audit` evidence vocabulary. Exact wording, classification-count,
and Markdown-section topology assertions with no external behavioral contract
may be `delete-now`; behavioral assertions that currently import the old shape
are `migrate-tests-first`; strict parsing, runtime repository facts,
per-handoff lease, post-lease rejection, result echo, scope, and receipt proofs
are `keep` or must receive a behavioral replacement first. Any
`human-contract-decision` result stops deletion pending explicit direction.

Test quality review: `delta-only` for Slice 1 and `focused` for Slice 2. After
both slices pass, invoke focused `$test-quality-review` independently across the
exact two-commit range before closeout. The review must confirm that every
preserved invariant has behavioral regression coverage and that no material
safety assertion was deleted without replacement. Record compact findings in
review evidence; material gaps block closeout.

## Shared Worker And Reviewer Briefs

Worker brief:

- The spawned `runway_worker` is already the required coding subagent for its
  assigned slice. It must implement only that slice and must not spawn, delegate to, or wait
  on additional subagents.
- Read this runway and dispatch, then make the smallest deletion-biased change
  that satisfies the authoritative outcome.
- Preserve unrelated dirty files, historical CCFG-30 artifacts, candidate work,
  CCFG-21 through CCFG-29, and the CCFG-29 deletion boundary.
- Do not run coordinator-owned final validation, independent review, ledger
  updates, commits, installs, or cleanup.
- Return the registered v2 worker result with
  `verified_cross_checkout_context: null` because this is ordinary single-root
  work.

Reviewer brief:

- The coordinator must provide the exact task-scoped worktree diff before
  commit or the exact implementation commit hash after commit. The spawned
  `runway_reviewer` must echo that `diff_basis` in compact YAML.
- Review for one narrow `ready`/`blocked` interface, mechanical helper versus
  semantic command-owner separation, fail-closed ambiguity, exact same-batch
  transaction scope, fresh strict per-handoff leases, honest receipts,
  deletion-biased complexity, project neutrality, and no historical/candidate
  drift.
- Reject parallel compatibility paths, weakened strict checks, generalized
  range acceptance, broad scanners/taxonomies, copied lifecycle exposition, or
  tests that merely relock wording/topology.
- Return `verified_cross_checkout_context: null` because review is ordinary
  single-root work.

## Active Ledger

| Slice | Risk | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|
| _No pending slices._ | | | | | | Final validation and closeout | Both declared slices are archived in `completed-slices.md`. |

## Orchestration Anomalies

orchestration_anomalies:
  - slice: 1
    severity: low
    category: approval_rule_side_effect
    observed: "Git write approval appended git add and git commit allowances to rules/default.rules."
    impact: "The unrelated tracked rule file became dirty after Slice 1 review and before commit finalization."
    action_taken: "Preserved the file, excluded it from both implementation commits, and carried it as unrelated dirty state."
    follow_up: "Review or commit the approval-rule change separately from CCFG-31."

## Completed Slice Archive

After each commit, move the completed row to `completed-slices.md` with the exact
commit, outcome, focused validation, test-quality review, and independent review
references. Do not leave commit-pending placeholders in final artifacts.

## Slice 1: Add The Mechanical Ready/Blocked Preflight

Risk: `migration`.

Scope:

- Add one mechanical preflight seam to `scripts/cross_checkout_context.py` whose
  normal result contains only `status`, `reason`, and `live_context`.
- Accept the immutable planning snapshot plus exact caller-supplied current
  queue-transaction evidence; do not discover a project-wide controlled-path
  taxonomy.
- Prove unchanged and exact same-batch committed, uncommitted, and combined
  queue establishment with temporary Git repositories.
- Prove all unrelated, ambiguous, stale-identity, implementation-movement, and
  post-preparation movement cases fail closed.
- Keep `prepare_cross_checkout_context_refresh(...)` as the strict live-context
  producer for subsequent handoffs; do not create a parallel bridge version or
  compatibility layer.

Allowed files:

- `scripts/cross_checkout_context.py`
- `tests/test_cross_checkout_context.py`

Non-goals:

- No consumer, skill, planning reference, manifest, documentation, changelog,
  agent, installer, or planning-state change.
- No interpretation of selected scope, current batch authority, recovery,
  delegation, or closeout inside the helper.
- No change to pre-creation transition semantics, strict parser behavior,
  mutation policy, write-scope validation, result schemas, or receipt schemas.
- No generic repository scanner, compatibility engine, movement taxonomy, or
  project-specific default.

Acceptance criteria:

- The preflight result has exactly three fields and exposes only `ready` or
  `blocked`; `reason` remains free diagnostic text, while `live_context`
  contains a strictly parsed context for `ready` and is `null` for `blocked`.
- A `ready` live context is created from current revisions and passes the
  existing strict parser.
- Unchanged state and exact current-batch committed, uncommitted, and combined
  queue-establishment movement can return `ready` when the caller supplies
  complete exact transaction paths.
- Implementation movement; unrelated planning, source, skill, agent, test,
  configuration, or documentation movement; another batch's artifacts;
  identity mismatch; incomplete transaction proof; arbitrary compatible-range
  claims; and ambiguity return `blocked`.
- The helper uses caller-supplied exact paths and facts, does not infer current
  business scope, and does not mutate planning state or authorize delegation.
- Existing strict root, branch, revision, generation, helper, Codex-home,
  write-scope, result-echo, receipt, and post-preparation movement tests remain
  green.
- No old public helper surface is deleted in this producer slice; Slice 2 owns
  consumer migration and destructive cleanup.

Validation:

- Run the required-green cross-checkout test command.
- Run Ruff on `scripts/cross_checkout_context.py` and
  `tests/test_cross_checkout_context.py`.
- Run basedpyright on `scripts/cross_checkout_context.py`.
- Run `git diff --check`, `git status --short`, and explicit untracked-file
  review.
- Test quality review: `delta-only`.

Commit message: `feat: add narrow live-lease preflight`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
verify the new helper boundary and temporary-repository matrix without applying
Slice 2 consumer expectations.

Stop conditions:

- Stop if the result needs another status, enumerated reason taxonomy, durable
  lifecycle state, or generalized compatibility decision.
- Stop if the helper would interpret current planning scope or gain semantic
  proceed/stop/recovery/delegation authority.
- Stop if exact caller-supplied transaction evidence cannot distinguish
  same-batch queue establishment from unrelated movement.
- Stop if strict parsing, later per-handoff refresh, scope validation, result
  echo, receipt truth, or post-preparation rejection weakens.
- Stop on any file outside the two-file allowlist or any unrelated dirty-file
  overlap.

## Slice 2: Collapse Consumers And Delete The Broad Protocol

Risk: `contract-narrowing`.

Approval gate:

- Re-run Planning State `current` and `validate`.
- Confirm this runway is the sole queued or active batch and CCFG-31 is still
  `Pending`.
- Confirm GitHub issue #53 remains the unwithdrawn repository-owner
  authorization. Stop on amendment, supersession, abandonment, or conflicting
  direction.
- Confirm the accepted Slice 1 commit and green helper API are the exact producer
  basis consumed by this slice.

Scope:

- Make `work-batch` supply current batch identity and exact queue-transaction
  paths, invoke the Slice 1 preflight, proceed only on `ready`, and stop on
  `blocked` while retaining all semantic authority.
- Keep the shared bridge as the one canonical temporary contract and reduce
  planning, execution, and recovery consumers to owner-specific obligations and
  references.
- Apply the dead-surface classifications from planning evidence: delete the
  three classification names and count assertions (`delete-now`); migrate broad
  controlled-path, lifecycle-count, lease/receipt prose, and recovery tests to
  runtime behavior (`migrate-tests-first`); keep the canonical bridge and
  planning-snapshot safety; keep command/runtime consumers as thin entrypoints.
- Preserve the project-neutral reusable-surface guard while detaching it from
  the obsolete controlled-owner taxonomy.
- Update expected feature versions, focused manifest routing, compact workflow
  guidance, and the changelog without installing or switching generations.
- Produce a concise before/after complexity inventory for closeout.

Allowed files:

- `skills/plan-batch/SKILL.md`
- `skills/work-batch/SKILL.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/references/execute-spec.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_codex_features_manifest.py`
- `codex-features.json`
- `docs/workflow-guide.md`
- `CHANGELOG.md`

Non-goals:

- No Slice 1 helper or test correction hidden inside this consumer slice; route
  a producer defect back through recovery against the Slice 1 boundary.
- No deletion of planning-snapshot persistence, strict parsing, pre-creation
  transition behavior, live per-handoff refresh, write-scope validation, result
  echo, receipt truth, final bridge, or CCFG-29 deletion ownership.
- No project-specific paths, commands, cache locations, issue IDs, or planning
  layout embedded in reusable skills or helper defaults.
- No edits to historical planning artifacts, other findings, candidate files,
  installer implementation/state, agent TOMLs, or planning-state code.
- No unrelated full-manifest wording repair.

Acceptance criteria:

- `work-batch` checks planning currentness, supplies the exact same-batch queue
  transaction, consumes the helper result, proceeds only on `ready`, and stops
  before delegation on `blocked` without reclassifying the reason.
- The helper remains mechanical; `work-batch` owns all proceed, stop, recovery,
  delegation, commit, receipt, closeout, and successor-stop decisions.
- Planning producers keep immutable planning-snapshot persistence but refer to
  the narrow preflight instead of preserving startup reconciliation as a
  separate durable lifecycle concept.
- The three old classifications, general compatible-range review, broad
  controlled-path taxonomy, duplicated full consumer exposition, and
  non-behavioral wording/count/topology assertions are removed.
- Runtime behavior protects exact same-batch paths, blocked unrelated movement,
  fresh strict worker/reviewer leases, post-lease invalidation, independent
  result echo, separate scope validation, and receipts bound to the actual
  lease.
- The bridge remains one canonical temporary contract; no v2 or parallel path
  exists, and CCFG-29 remains the sole deletion owner.
- Reusable skills remain project-neutral and consumer tests assert ownership and
  observable routing rather than Markdown topology.
- Expected manifest versions are `plan-batch` `1.0.7`, `work-batch` `1.0.8`,
  and `batch-runway` `1.5.4`; `custom-agents` remains unchanged and installer
  links remain correctly owned without a real install.
- Focused test-quality review confirms every preserved invariant is covered and
  no material safety assertion was removed without behavioral replacement.
- Historical CCFG-30 artifacts, the redesign candidate, CCFG-21 through
  CCFG-29, unrelated dirty files, and installed state remain unchanged.
- The closeout inventory shows fewer caller-visible concepts,
  classifications, duplicated obligations, and wording/topology locks.

Validation:

- Run every required-green command from the validation section.
- Run the full manifest command as known-red diagnostic only and compare its
  failures with the planning baseline; do not absorb unrelated repairs.
- Run `git diff --check`, `git status --short`, and explicit untracked-file
  review.
- Test quality review: `focused`, preceded by the declared dead-surface evidence
  check for every deleted or migrated assertion.
- Do not run a real install or mutate installed state.

Commit message: `refactor: collapse cross-checkout startup protocol`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
verify the Slice 1 API consumption, every destructive deletion, and the exact
task-scoped diff basis.

Stop conditions:

- Stop if the approval gate is no longer satisfied or Slice 1 is not a stable,
  green producer boundary.
- Stop if a supported external caller requires any old classification or broad
  protocol surface and no explicit contract decision exists.
- Stop if `ready` can include arbitrary movement, implementation movement,
  unrelated paths, incomplete evidence, or ambiguity.
- Stop if strict parsing, planning-snapshot persistence, per-handoff freshness,
  post-lease rejection, result echo, write-scope validation, or receipt truth
  weakens.
- Stop if a taxonomy, scanner, lifecycle concept, durable artifact, schema,
  agent, public command, parallel bridge, or project-specific generic default
  is introduced.
- Stop if any allowed-file edit would absorb unrelated known-red manifest work.
- Stop on historical, candidate, other-finding, installer-state, or unrelated
  dirty-file overlap.

## Final Validation

After Slices 1 and 2 are accepted and committed:

- Re-run every required-green command.
- Re-run the full manifest command as known-red diagnostic and account for the
  exact baseline delta without silently promoting it.
- Confirm `./install.sh --status` and `./install.sh --dry-run` report correct
  linked ownership and expected version metadata without a real install.
- Run focused `$test-quality-review` against the exact implementation diff and
  retain its compact findings.
- Delegate independent final review over the exact two-slice commit range and any
  coordinator-owned closeout diff.
- Inspect both slice commits and the exact range with `git show --stat <hash>`,
  `git show <hash>`, and the corresponding range commands.
- Confirm no historical CCFG-30, candidate, CCFG-21 through CCFG-29, installed
  state, or unrelated dirty path changed.

## Final Acceptance And Closeout

Close CCFG-31 only when the final evidence proves the issue's full ready/blocked
matrix, preserved per-handoff invariants, mechanical/semantic ownership split,
single canonical bridge, focused test-quality approval, version consistency,
and unchanged excluded surfaces.

The closeout must enumerate the removed classifications, duplicated
obligations, lifecycle concept, broad path/range machinery, and wording/topology
tests; show the final coordinator-visible result; record exact commits,
validation, test-quality review, independent review, and installed-link status;
reconcile only CCFG-31; clear the same-batch queue; and stop without selecting a
successor.

## Stop Conditions

- Stop on scope drift, approval withdrawal, dirty-file conflict, missing project
  value, unresolved validation or review failure, missing required subagent
  support, or any slice stop condition.
- Do not implement a third slice as filler. If a genuine independent boundary
  appears, stop and amend or split through program-runway ownership; never
  exceed the issue's three-slice cap.
- Do not execute, select, dispatch, or prepare successor work from this planning
  session.
