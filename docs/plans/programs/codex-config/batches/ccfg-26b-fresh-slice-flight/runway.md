# CCFG-26B Fresh Slice Flight Runway

Status: `queued after clean independent planning review`

## Purpose

Move one complete successful implementation-slice flight to the permanent
candidate `work-batch` command owner. A fresh coordinator process must consume
the current queued or active runway, execute exactly the next pending slice,
accept focused validation and an independent exact-diff review, commit and
archive that slice, persist one unique `batch-execution-flight/v1` result, and
end. A `continue_same_batch` result may cause the runner to launch another fresh
`work-batch` process for the same batch; it must not reuse the completed
coordinator context or select successor work.

This runway covers only CCFG-26B. CCFG-26C owns recovery/advisor behavior,
CCFG-26D owns final validation/finalization, and CCFG-26E owns closeout,
reconciliation, no-successor proof, and final displaced-owner narrowing.

## Source Contract

- Selected dispatch: `dispatch.md`
- Program ledger: `../../LEDGER.md`, CCFG-26 only
- Execution carry-forward:
  `../../findings/command-owner-redesign-planning-execution-carry-forward.md`
- Temporary stable policy:
  `../../notes/stable-runway-dogfooding-policy.md`
- CCFG-34 intake:
  `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Completed planning predecessor:
  `../ccfg-26a-permanent-vertical-runway-contract/closeout.md`
- Completed slice-shape predecessor:
  `../ccfg-26-slice-shape-policy-correction/closeout.md`
- Corrected reusable shape authority:
  `../ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`
- GitHub issue #61:
  `https://github.com/alacasse/codex-config/issues/61`
- COR-009 accepted snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slice 1 risk: `migration`.
- Slice 1 selected shape: `vertical`.
- Slice 1 shape override reason: `null`.
- Approval gate: none beyond the existing CCFG-26/COR-009 and issue #61
  authority. The slice preserves supported behavior while migrating one exact
  scenario. Contract narrowing, destructive cleanup, recovery-policy changes,
  finalization, closeout, and successor behavior require later reviewed work.

## Current Baseline And Assumptions

- Stable planning/toolchain checkout:
  `/home/alacasse/projects/codex-config`
- Stable planning/toolchain commit at plan time:
  `8aec9c2bcf87f619012b6dfc748ef46387515298`
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Candidate branch: `implementation/command-owner-redesign`
- Candidate baseline:
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`
- Both worktrees were clean before planning edits.
- Planning State `current` and `validate` passed with no selected dispatch,
  queued batch, active runway, blocker, or obligation.
- The candidate's focused runner baseline passed `72 tests` and `22 subtests`.
- The command-owner catalog validated `82 scenarios`.
- The exact two declared later-CCFG-26 diagnostic tests failed with no
  additional failure; they remain `known-red-baseline` and are not silently
  promoted by CCFG-26B.
- Current candidate execution still routes the serialized `execute` phase to
  `$batch-runway execute-spec`, uses one `03-execute.json` receipt path, and
  records receipt state by phase. Those are the exact happy-path callers this
  slice migrates.
- Existing `runway_worker` and `runway_reviewer` role authority is correct and
  remains unchanged unless a focused failing test proves a mechanical result-
  echo adjustment is required.

## Whole-Batch Non-Goals

- No blocker recovery, recovery advisor, runway amendment, or same-slice repair
  behavior from issue #59 or CCFG-26C.
- No final validation, candidate installation orchestration, exact acceptance
  orchestration, finalization flight, or CCFG-26D behavior.
- No closeout, same-batch reconciliation, partial-closeout recovery, final
  displaced-owner narrowing, or CCFG-26E behavior.
- No successor selection, dispatch, queueing, preparation, or readiness
  inference.
- No migration or removal of serialized `select-dispatch`, `create-spec`,
  `execute`, or `closeout` identities; CCFG-27 owns that decision.
- No physical deletion, default-generation switch, cross-checkout bridge
  removal, stable-policy removal, or final integration.
- No second runner, launcher, execution store, compatibility dialect, fallback
  semantic owner, `scripts/work_batch.py`, or broad runner redesign.
- No change to Batch Runway or Architecture Program Runway semantic contracts;
  their remaining displacement is reconciled in CCFG-26E.

## Flight Result And Fresh-Context Contract

`work-batch` owns and links
`skills/work-batch/references/batch-execution-flight-v1.schema.json`. The v1
schema has this complete required shape; every field is present, values marked
`null` are explicitly nullable, and arrays are present even when empty:

```yaml
interface: batch-execution-flight/v1
receipt_path: string
batch_id: string
slice_id: string | null
status: completed | blocked | failed
candidate_before: full-git-sha
candidate_after: full-git-sha | null
validation_summary: string | null
review_summary: string | null
commit_receipt: string | null
orchestration_anomalies: []
bounded_inputs:
  planning_state_diagnostic: {path: string, sha256: string}
  active_runway: {path: string, sha256: string, slice_id: string | null}
  validation_profile: {path: string, sha256: string}
  candidate_head: full-git-sha
  candidate_worktree_status: string
  prior_commit_receipt: {path: string, sha256: string} | null
  unresolved_orchestration_anomalies: []
  retained_migration_facts: []
  strict_execution_lease: {interface: cross-checkout-context/v1, sha256: string}
telemetry:
  input_tokens: integer | null
  output_tokens: integer | null
  compaction_count: integer | null
  files_changed: integer
  lines_added: integer
  lines_removed: integer
  validation_command_count: integer
  validation_command_breadth: []
  support_agents: []
  review_lenses: []
  duration_seconds: number | null
  blocker_recovery_transitions: []
next_action:
  kind: continue_same_batch | finalize_same_batch | closeout_same_batch | require_user
  next_slice_id: string | null
```

The coordinator writes the durable receipt at the runner-provided exact
`receipt_path` before process termination and returns the same JSON object as
its structured command result. The runner validates byte-equivalent parsed
content before transition; it may not synthesize missing fields or infer a
different action.

CCFG-26B implements authorship only for a successful implementation slice:
`status=completed`, a non-null `slice_id`, a non-null accepted
`candidate_after`, and either `continue_same_batch` with the exact non-null
next pending slice ID or `finalize_same_batch` with `next_slice_id=null` after
the last implementation slice. The schema reserves `blocked`, `failed`,
`closeout_same_batch`, and `require_user` now so CCFG-26C through CCFG-26E do
not mutate v1 or introduce another dialect; their behavior remains deferred.

CCFG-26B adds conditional validation for exactly these two authored
combinations:

| Status | Next action | Slice ID | Candidate after | Commit receipt | Next slice ID | CCFG-26B behavior |
|---|---|---|---|---|---|---|
| `completed` | `continue_same_batch` | non-null | non-null | non-null | non-null | mechanically launch a fresh same-batch process |
| `completed` | `finalize_same_batch` | non-null | non-null | non-null | `null` | stop at the durable future-finalization handoff |

Every other field-level-valid combination using reserved `blocked`, `failed`,
`closeout_same_batch`, or `require_user` values is structurally v1-valid but
unsupported by CCFG-26B. The runner must persist and surface it, then stop
without transition, relaunch, finalization, closeout, recovery, or inferred
correction. CCFG-26C through CCFG-26E may add behavioral combination rules
under this unchanged field/enum/nullability shape; they must not rename v1 or
add another dialect.

Every fresh slice coordinator may read only the `bounded_inputs` facts above
and the exact current slice section they identify. It must not reload full
prior-slice chronology, raw validation logs, prior worker transcripts, already
accepted review detail, or resolved anomaly history. Unavailable token,
compaction, or duration measurements are explicit `null`; no telemetry field is
silently omitted. More than one compaction in a slice is retained as a future
planning-quality warning, not interpreted by the runner as lifecycle state.

## Planning Snapshot

Interface: `cross-checkout-context/v1`.

Installed helper:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Resolved helper:

```text
/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated plan-time payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 8aec9c2bcf87f619012b6dfc748ef46387515298
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 8aec9c2bcf87f619012b6dfc748ef46387515298
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Plan-time validation receipt:

```yaml
interface: cross-checkout-receipt/v1
caller: plan-batch
reason: CCFG-26B fresh slice-flight selection and queue transition
allowed_scope:
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  planning_paths:
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/dispatch.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/review.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/completed-slices.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/execution-report.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/closeout.md
  implementation_paths:
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/work-batch
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/architecture-program-runway/references/local-runner-v1.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/architecture-program-runway/references/local-runner-phase-result.schema.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_artifacts.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_environment.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_phase_contract.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_state.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_transition.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_validation.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_command.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_workers.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/agents/runway_worker.toml
    - /home/alacasse/projects/codex-config-command-owner-redesign/agents/runway_reviewer.toml
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/architecture_program_runner_test_support.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_work_batch_flight_contract.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_artifacts.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_command.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_environment.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_phase_contract.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_run_loop.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_state.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_transition.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_validation.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_custom_agent_contracts.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_behavioral_scenarios.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codex_features_manifest.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_batch_lifecycle_guards.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_routing_rule_ownership.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/docs/skill-routing-contract.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/docs/workflow-guide.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/README.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/codex-features.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md
generation_identity:
  generation_role: stable
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 8aec9c2bcf87f619012b6dfc748ef46387515298
  codex_home: /home/alacasse/.codex
  canonical_state_mutation_allowed: true
repository_revisions:
  toolchain_commit: 8aec9c2bcf87f619012b6dfc748ef46387515298
  canonical_planning_commit_before: 8aec9c2bcf87f619012b6dfc748ef46387515298
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
deletion_condition: CCFG-29 final integration
```

This planning snapshot is immutable historical plan-time evidence, not a live
execution lease. Do not edit its revisions after the containing planning
change. Before the first delegated handoff, `work-batch` must confirm the same
selected scope through Planning State, pass the ready/blocked preflight, and
acquire a fresh live lease. Later worker and reviewer handoffs require new
leases and separately validated write scopes.

## Project Values

- Planning Artifact Layout: Planning Artifact Layout v1.
- Planning location: this batch directory.
- Program root: `docs/plans/programs/codex-config`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`; candidate and final harnesses use explicit fresh
  `/tmp` outputs.
- Output root: `None`; generated evidence stays under explicit fresh `/tmp`
  roots and is summarized in durable planning artifacts.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: candidate `scripts/command_owner_scenarios.py accept`
  with a fresh output root and the isolated candidate Codex home.
- Summary artifacts: fresh `acceptance-result.json`, `report.json`, and
  `report.txt`; read the result and text report before reporting acceptance.
- Index refresh: none.
- Commit strategy: one focused candidate implementation commit for Slice 1;
  stable planning artifacts are not implementation commits.
- Dirty-file constraint: both worktrees must remain free of unrelated dirt.
- Cross-checkout mode: strict `cross-checkout-context/v1` with canonical writes
  only under the validated stable planning root and implementation writes only
  under the candidate ceiling.

## Write-Path Ceiling

### Canonical Planning Paths

- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/dispatch.md`
- `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/runway.md`
- `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/review.md`
- `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/completed-slices.md`
- `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/execution-report.md`
- `docs/plans/programs/codex-config/batches/ccfg-26b-fresh-slice-flight/closeout.md`

### Candidate Required Paths

- `skills/work-batch/**`, including the owned
  `references/batch-execution-flight-v1.schema.json`
- `skills/architecture-program-runway/references/local-runner-v1.md`
- `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_artifacts.py`
- `scripts/architecture_program_runner_environment.py`
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_state.py`
- `scripts/architecture_program_runner_transition.py`
- `scripts/architecture_program_runner_validation.py`
- focused runner and work-batch flight tests named in the planning snapshot
- command-owner scenario fixtures and acceptance test
- `tests/test_codex_features_manifest.py`
- `tests/test_batch_lifecycle_guards.py`
- `codex-features.json`
- `CHANGELOG.md`

### Candidate Conditional Paths

- `scripts/architecture_program_runner_command.py` and its focused test only if
  a failing phase-contract or expected-path test proves prompt rendering must
  change outside the phase-contract owner.
- `scripts/architecture_program_runner_workers.py` only if a failing process-
  identity test proves the existing fresh `CodexExecWorker` boundary cannot
  relaunch the same serialized phase mechanically.
- `agents/runway_worker.toml`, `agents/runway_reviewer.toml`, and
  `tests/test_custom_agent_contracts.py` only if a focused failing result-echo
  test proves the current roles cannot preserve exact flight identity. Their
  authority and separation must not change.
- `tests/test_skill_routing_rule_ownership.py`, `docs/skill-routing-contract.md`,
  `docs/workflow-guide.md`, and `README.md` only when required to state the
  migrated happy-path ownership without pulling CCFG-26C through CCFG-26E
  semantics forward.

`skills/batch-runway/**`, `skills/architecture-program-runway/SKILL.md`, and all
other candidate paths are read-only in CCFG-26B. The ceiling is an upper bound,
not a requirement to touch every conditional file.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker, reviewer, specialist, investigator, and Spark result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for the stable execution of this runway.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`

Overrides:

- The temporary stable CCFG-34 policy applies: one `work-batch` invocation
  executes exactly one implementation slice and stops after its commit, receipt,
  ledger update, and completed-slice archival. Later final validation,
  finalization, and same-batch closeout retain their current stable owners.
- This execution-boundary override governs execution of CCFG-26B itself. It
  does not weaken the permanent candidate acceptance that later same-batch
  implementation slices run in separate fresh coordinator processes.
- The selected profile's installed exact-commit integration acceptance remains
  final-only because it must bind the clean accepted Slice 1 commit and an
  installed candidate home. Its per-slice substitute is the
  implementation-created two-flight behavioral test in the exact focused
  command below plus the required-green command-owner catalog validator. No
  project-harness output artifact is produced by that per-slice substitute.
- CCFG-26B does not implement the permanent finalization flight. After the one
  stable implementation-slice invocation stops, a later stable `work-batch`
  invocation performs this child batch's existing final validation and
  same-batch closeout. The candidate `finalize_same_batch` result tested here is
  only a durable handoff to future CCFG-26D behavior; it does not select, queue,
  activate, or execute CCFG-26D.

## Validation Profile And Baselines

Selected profile:
`skills/batch-runway/references/validation-profiles/project-harness-production.md`.

### Required-Green Current Baseline

The following existing candidate command is `required-green` and passed at plan
time with `72 tests` and `22 subtests`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_architecture_program_runner_phase_contract.py \
  tests/test_architecture_program_runner_state.py \
  tests/test_architecture_program_runner_validation.py \
  tests/test_architecture_program_runner_transition.py \
  tests/test_architecture_program_runner_run_loop.py \
  tests/test_architecture_program_runner_artifacts.py \
  tests/test_architecture_program_runner_environment.py \
  tests/test_architecture_program_runner_command.py
```

The following catalog validation is `required-green` and validated `82
scenarios` at plan time:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  scripts/command_owner_scenarios.py validate \
  tests/fixtures/command-owner-scenarios
```

### Known-Red Baseline

The following exact command is `known-red-baseline`. It produced only the two
declared later-CCFG-26 failures at plan time. CCFG-26B must gain no new failure
and must not silently promote either assertion unless its exact happy-path
ownership change directly satisfies it without pulling closeout work forward:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_work_batch_reconciles_same_batch_closeout \
  tests/test_batch_lifecycle_guards.py::BatchLifecycleGuardTests::test_architecture_program_closeout_rejects_dispatch_runway_only_evidence
```

### Implementation-Created And Conditional Gates

- The following exact post-change focused command is
  `implementation-created` by Slice 1 because
  `tests/test_work_batch_flight_contract.py` does not yet exist. Slice 1 creates
  that file and the new expectations in the listed existing tests; the complete
  command must then be green before independent review:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
    tests/test_work_batch_flight_contract.py \
    tests/test_architecture_program_runner_phase_contract.py \
    tests/test_architecture_program_runner_state.py \
    tests/test_architecture_program_runner_validation.py \
    tests/test_architecture_program_runner_transition.py \
    tests/test_architecture_program_runner_run_loop.py \
    tests/test_architecture_program_runner_artifacts.py \
    tests/test_architecture_program_runner_environment.py \
    tests/test_architecture_program_runner_command.py \
    tests/test_command_owner_behavioral_scenarios.py \
    tests/test_codex_features_manifest.py \
    tests/test_batch_lifecycle_guards.py
  ```

  It covers schema accept/reject cases, complete enum/nullability rules,
  bounded inputs, explicit telemetry nulls, unique ordered receipts,
  `continue_same_batch`, `finalize_same_batch`, missing/contradictory receipt
  failure, and a deterministic two-slice fresh-process boundary.
- Ruff over exact changed Python and test files is `conditional` when Python
  changes; use `--no-cache` in the candidate checkout.
- Configured BasedPyright over exact changed production Python files is
  `conditional` when typed Python changes. Do not silently promote the broader
  configured project beyond the proved changed-file scope.
- Agent-result tests are `conditional` only when a registered agent TOML changes.
- `git diff --check` is `required-green` after Slice 1 and at final validation.
- Candidate installation and exact-commit scenario acceptance are
  `required-green` final gates, not worker commands.

## Proportionality And Slice Shape

```yaml
shape:
  selected: vertical
  override_reason: null
slice_shape:
  initial_count: 1
  final_count: 1
  rationale: the work-batch owner, one flight result, the serialized execute caller, unique receipt state, mechanical relaunch, and focused behavioral proof form one complete queued-runway-to-durable-slice scenario; splitting any adjacent producer/consumer leaves an unusable or contradictory intermediate state
smaller_alternative_analysis:
  alternative: first add the flight schema, then migrate work-batch and runner callers in later slices
  rejected_because: a schema with no author and consumer is inert, while a caller migration without a validated durable receipt cannot safely end or resume a coordinator process
  advisory_recheck: before implementation review, record changed-file count, line delta, production surfaces, owner boundaries, review lenses, validation breadth, and coordinator compaction; require a reviewed smaller alternative if recovery, finalization, closeout, phase-label migration, or unrelated runner design enters the diff
```

There is one implementation slice because there is one independently usable
happy-path state. CCFG-26C through CCFG-26E remain separate because each starts
from a different durable condition and has different stop, recovery, and
acceptance boundaries.

## Execution Ledger

| Slice | Status | Risk | Shape | Depends on | Commit | Validation | Review |
|---|---|---|---|---|---|---|---|
| 1. Execute one successful implementation slice in a fresh work-batch flight | pending | migration | vertical | CCFG-26A and slice-shape correction closeouts | pending | pending | pending |

Completed slice details move to `completed-slices.md` during execution. The
active ledger retains only pending or active work.

## Slice 1 — Execute One Successful Implementation Slice In A Fresh Work-Batch Flight

### Shape And Vertical Ownership Evidence

```yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
vertical_slice:
  starting_scenario: Planning State identifies one queued multi-slice runway whose next implementation slice is pending, while the candidate still routes one serialized execute phase through a long-lived Batch Runway execute-spec coordinator
  durable_result: a fresh public work-batch coordinator executes exactly that slice through worker, focused validation, independent reviewer, commit, receipt, ledger update, and archival; a unique schema-valid batch-execution-flight/v1 result records the exact same-batch next action before the process ends
  owner_before: the local runner serialized execute phase plus Batch Runway execute-spec semantics coordinate the full batch in one process and one phase-keyed receipt slot
  owner_after: work-batch/v1 owns the successful single-slice lifecycle and authors its exact next action; the runner owns only fresh process launch, command-result validation, durable receipt and telemetry storage, explicit loop bounds, and mechanical same-batch relaunch
  migrated_callers:
    - public work-batch queued-or-active runway invocation
    - local runner serialized execute phase contract
    - runner execute result and receipt validation
    - runner state transition for continue_same_batch and finalize_same_batch
    - batch manifest receipt and telemetry retention for repeated execute flights
    - runway_worker and runway_reviewer handoffs under work-batch lifecycle authority
  focused_validation:
    - work-batch flight schema accept and reject cases
    - runner phase-contract, environment, state, validation, transition, run-loop, and artifact tests
    - two-slice fresh-process behavioral scenario with distinct session identities and unique receipts
    - commit-to-next-slice, last-slice-to-finalize stop, missing or contradictory receipt stop, and no-successor scenarios
    - command-owner catalog validation, Ruff, configured BasedPyright, git diff check, delta-only test-quality review, and independent exact-diff implementation review
  independently_usable_state: candidate execution can complete successive successful implementation slices with no shared live coordinator context, durable ordered receipts, exact worker/reviewer/commit evidence, and a safe stop at finalize_same_batch while recovery, finalization, and closeout remain deferred
  rollback_boundary: revert the one focused candidate commit to 5c5ec9d52dd9033daa45f3a200031c152363b62c; stable planning, stable Codex home, serialized phase identities, canonical state, and later child selection remain unchanged
  temporary_residue:
    - Batch Runway execution support and displaced semantic prose remain until CCFG-26E
    - Architecture Program Runway closeout and reconciliation support remains until CCFG-26E
    - blocker recovery and advisor behavior remains with CCFG-26C
    - final validation and finalization remains with CCFG-26D
    - closeout, reconciliation, no-successor proof, and final owner narrowing remains with CCFG-26E
    - serialized phase identities remain through the CCFG-27 decision and no later than CCFG-29
    - stable CCFG-34 policy and strict bridge remain until CCFG-29 parity and integration
  ownership_coexistence: temporary
migration_evidence:
  starting_scenario: Planning State identifies one queued multi-slice runway whose next implementation slice is pending, while the candidate still routes one serialized execute phase through a long-lived Batch Runway execute-spec coordinator
  durable_result: a fresh public work-batch coordinator executes exactly that slice through worker, focused validation, independent reviewer, commit, receipt, ledger update, and archival; a unique schema-valid batch-execution-flight/v1 result records the exact same-batch next action before the process ends
  owner_before: the local runner serialized execute phase plus Batch Runway execute-spec semantics coordinate the full batch in one process and one phase-keyed receipt slot
  owner_after: work-batch/v1 owns the successful single-slice lifecycle and authors its exact next action; the runner owns only fresh process launch, command-result validation, durable receipt and telemetry storage, explicit loop bounds, and mechanical same-batch relaunch
  migrated_callers:
    - public work-batch queued-or-active runway invocation
    - local runner serialized execute phase contract
    - runner execute result and receipt validation
    - runner state transition for continue_same_batch and finalize_same_batch
    - batch manifest receipt and telemetry retention for repeated execute flights
    - runway_worker and runway_reviewer handoffs under work-batch lifecycle authority
  focused_validation:
    - work-batch flight schema accept and reject cases
    - runner phase-contract, environment, state, validation, transition, run-loop, and artifact tests
    - two-slice fresh-process behavioral scenario with distinct session identities and unique receipts
    - commit-to-next-slice, last-slice-to-finalize stop, missing or contradictory receipt stop, and no-successor scenarios
    - command-owner catalog validation, Ruff, configured BasedPyright, git diff check, delta-only test-quality review, and independent exact-diff implementation review
  independently_usable_state: candidate execution can complete successive successful implementation slices with no shared live coordinator context, durable ordered receipts, exact worker/reviewer/commit evidence, and a safe stop at finalize_same_batch while recovery, finalization, and closeout remain deferred
  rollback_boundary: revert the one focused candidate commit to 5c5ec9d52dd9033daa45f3a200031c152363b62c; stable planning, stable Codex home, serialized phase identities, canonical state, and later child selection remain unchanged
  temporary_residue:
    - Batch Runway execution support and displaced semantic prose remain until CCFG-26E
    - Architecture Program Runway closeout and reconciliation support remains until CCFG-26E
    - blocker recovery and advisor behavior remains with CCFG-26C
    - final validation and finalization remains with CCFG-26D
    - closeout, reconciliation, no-successor proof, and final owner narrowing remains with CCFG-26E
    - serialized phase identities remain through the CCFG-27 decision and no later than CCFG-29
    - stable CCFG-34 policy and strict bridge remain until CCFG-29 parity and integration
  ownership_coexistence: temporary
```

### Migration Matrix

```yaml
migration_matrix:
  planning_currentness:
    current_owner: stable work-batch plus Planning State diagnostic
    future_owner: work-batch/v1 consuming normalized Planning State current and validate as the sole semantic execution-currentness gate
    reason: the fresh flight must confirm the same queued or active runway before mechanical helper or process work
    status: pending
    removal_slice_or_condition: Slice 1 currentness and stale-state behavioral tests are green
  public_work_batch_happy_path:
    current_owner: work-batch routes the whole runway to Batch Runway execute-spec
    future_owner: work-batch/v1 owns exactly one successful implementation-slice lifecycle and its authored next action
    reason: the human command owner must own current slice, proceed/stop, validation, review, commit, receipt, and archival decisions
    status: pending
    removal_slice_or_condition: Slice 1 focused and exact acceptance are green
  serialized_execute_caller:
    current_owner: architecture_program_runner_phase_contract routes execute to batch-runway execute-spec
    future_owner: the retained serialized execute phase launches public work-batch once per fresh implementation flight
    reason: the compatibility label may remain while its semantic command caller moves to the public owner
    status: pending
    removal_slice_or_condition: Slice 1 phase-contract and fresh-process scenarios are green; label migration remains CCFG-27
  flight_result_contract:
    current_owner: one generic local-runner phase result with no slice identity or work-batch-authored next action
    future_owner: work-batch-owned batch-execution-flight/v1 result validated mechanically by the runner
    reason: a fresh process must persist exact durable slice evidence and continuation intent before termination
    status: pending
    removal_slice_or_condition: Slice 1 schema, mismatch, and missing-receipt tests are green
  fresh_context_allowlist:
    current_owner: the serialized execute prompt and long-lived coordinator can accumulate the full runway and prior live chronology
    future_owner: work-batch/v1 selects only the complete bounded_inputs allowlist while the runner passes and hashes those inputs mechanically
    reason: a fresh process reduces stale context only when raw logs, transcripts, resolved history, and accepted prior review detail cannot silently re-enter
    status: pending
    removal_slice_or_condition: Slice 1 bounded-input accept/reject and two-flight no-shared-context tests are green
  per_flight_telemetry:
    current_owner: phase-keyed runner telemetry records one execute observation and can overwrite repeated execute evidence
    future_owner: the runner retains ordered per-flight raw counters and work-batch links the complete telemetry object without treating it as lifecycle state
    reason: issue #61 requires durable token, compaction, diff-size, validation-breadth, support-agent, review-lens, duration, and recovery-transition evidence for proportionality review
    status: pending
    removal_slice_or_condition: Slice 1 telemetry shape, explicit-null, ordered-retention, and overwrite tests are green
  execute_receipt_paths:
    current_owner: architecture_program_runner_state returns one 03-execute.json path for the batch
    future_owner: runner mechanism allocates unique ordered execute-flight receipt and input-inventory paths without interpreting their meaning
    reason: repeated fresh flights must not overwrite durable resume evidence
    status: pending
    removal_slice_or_condition: Slice 1 two-flight path and resume tests are green
  runner_transition:
    current_owner: runner validation always maps a completed execute result directly to closeout
    future_owner: runner validates the work-batch-authored continue_same_batch or finalize_same_batch action and mechanically relaunches or stops
    reason: the runner owns process lifecycle but must not infer slice acceptance, closeout meaning, or successor readiness
    status: pending
    removal_slice_or_condition: Slice 1 transition and no-inference tests are green
  receipt_and_telemetry_retention:
    current_owner: batch manifest and telemetry maps retain a single entry keyed only by execute phase
    future_owner: runner artifact mechanism retains ordered per-flight receipts, inventories, session identity, and telemetry without overwriting prior flights
    reason: fresh-process resume and later finalization need durable accepted evidence, not chat history
    status: pending
    removal_slice_or_condition: Slice 1 artifact and two-flight scenario tests are green
  worker_and_reviewer_handoffs:
    current_owner: Batch Runway coordinator invokes runway_worker and runway_reviewer
    future_owner: work-batch lifecycle invokes the same registered roles with unchanged implementation and read-only review authority
    reason: worker/reviewer independence must survive the coordinator-owner migration
    status: pending
    removal_slice_or_condition: Slice 1 exact diff-basis, result-echo, and role-contract tests are green
  batch_runway_residue:
    current_owner: Batch Runway retains execute-spec, recovery, and finalization semantic prose
    future_owner: work-batch/v1 is the only execution lifecycle owner
    reason: CCFG-26B migrates only the successful slice scenario; narrowing all displaced support before recovery, finalization, and closeout replacements exist would be unsafe
    status: pending
    removal_slice_or_condition: CCFG-26E final owner narrowing after CCFG-26C and CCFG-26D
  recovery_and_resume:
    current_owner: existing stable work-batch and Batch Runway recovery contracts
    future_owner: CCFG-26C work-batch bounded recovery flight with one read-only advisor and reviewed amendment
    reason: blocker recovery starts from a different durable state and has separate authority and review gates
    status: pending
    removal_slice_or_condition: CCFG-26C closeout
  finalization:
    current_owner: existing Batch Runway final validation and finalization path
    future_owner: CCFG-26D work-batch finalization flight
    reason: last-slice completion starts a distinct flight with broader validation and installation evidence
    status: pending
    removal_slice_or_condition: CCFG-26D closeout
  closeout_and_reconciliation:
    current_owner: work-batch routes closeout to Architecture Program Runway support
    future_owner: CCFG-26E work-batch closeout and same-batch reconciliation flight
    reason: closeout meaning, partial-closeout recovery, and no-successor proof require their own durable start state and acceptance boundary
    status: pending
    removal_slice_or_condition: CCFG-26E closeout
  serialized_phase_protocol:
    current_owner: local runner compatibility labels select-dispatch, create-spec, execute, and closeout
    future_owner: CCFG-27 decides their public migration or removal
    reason: CCFG-26B changes the execute caller, not the reserved serialized identities
    status: pending
    removal_slice_or_condition: CCFG-27 decision and no later than CCFG-29 physical cleanup
  stable_policy_and_bridge:
    current_owner: root AGENTS.md temporary policy plus strict cross-checkout bridge
    future_owner: integrated candidate behavior with no temporary stable overlay or bridge
    reason: stable remains canonical and controls this cross-checkout batch until permanent parity and integration
    status: pending
    removal_slice_or_condition: CCFG-29 parity and final integration gate
```

Every retained route names its exact caller or scenario, current owner, future
owner, reason, status, and removal condition. No silent fallback or ambiguous
dual ownership is authorized.

### Scope

- Add the work-batch-owned `batch-execution-flight/v1` result contract for one
  implementation slice with the complete v1 field, enum, nullability,
  bounded-input, telemetry, and next-action contract above.
- Make public `work-batch` own the successful single-slice lifecycle and author
  only the successful-slice `continue_same_batch` or `finalize_same_batch`
  outcomes from canonical slice evidence. Reserve `blocked`, `failed`,
  `closeout_same_batch`, and `require_user` in v1 without implementing their
  behavior. Do not add closeout behavior in CCFG-26B.
- Route the retained serialized `execute` phase to public `work-batch`, not
  directly to Batch Runway.
- Keep the runner mechanical: fresh process launch, expected-path supply,
  command-result and schema validation, durable receipt/inventory/telemetry
  retention, explicit loop bound, and relaunch or stop from the exact authored
  result.
- Allocate unique ordered execute-flight receipts and preserve every accepted
  flight in batch manifests and telemetry.
- Prove two successful implementation slices use distinct coordinator process
  identities, distinct fresh strict leases, distinct receipt paths, and no
  shared chat history.
- Preserve the existing worker/reviewer authority, exact reviewer diff basis,
  commit acceptance, active-ledger update, completed-slice archival, and
  no-successor stop.
- Update installed feature metadata and changelog only for changed permanent
  candidate behavior.

### Allowed Files

Only required or conditionally proved paths under the Write-Path Ceiling.

### Non-Goals

The Whole-Batch Non-Goals apply without exception. In particular, do not edit
Batch Runway or Architecture Program Runway skill semantics, do not implement
recovery/finalization/closeout, and do not infer next actions inside the runner.

### Acceptance Criteria

1. Planning State `current` and `validate` identify the same queued or active
   batch and are the sole semantic currentness gate before a fresh flight.
2. The retained serialized `execute` phase launches public `work-batch` in one
   fresh coordinator process; the phase identity itself remains unchanged.
3. `work-batch` selects exactly the next incomplete implementation slice and
   owns every proceed/stop, validation acceptance, review acceptance, commit,
   receipt, ledger-update, archival, and next-action decision for that flight.
4. The registered `runway_worker` implements and the separate read-only
   `runway_reviewer` reviews the exact diff basis; neither role gains lifecycle,
   commit, delegation, or successor authority.
5. A schema-valid `batch-execution-flight/v1` result is durably written before
   process termination and exactly matches the command result the runner
   validates.
6. Execute-flight receipt, input-inventory, and telemetry paths are unique and
   ordered; a later flight cannot overwrite earlier accepted evidence.
7. `continue_same_batch` ends the current coordinator process and causes only a
   fresh same-batch `work-batch` process to start from canonical state and a
   fresh strict lease.
8. A two-slice fixture proves different coordinator session IDs, distinct
   receipts, exact accepted commits, no shared live context, and rejection of
   full prior chronology, raw logs, prior worker transcripts, or already
   accepted review detail outside `bounded_inputs`.
9. Last implementation-slice completion authors `finalize_same_batch` and stops
   durably for CCFG-26D; it does not invoke current closeout or finalization.
10. Missing, malformed, stale, mismatched, or contradictory flight evidence
    stops safely before relaunch or state transition.
11. The runner validates and mechanically consumes `work-batch` output; it does
    not infer slice acceptance, closeout meaning, next-batch readiness, or
    successor identity.
12. Git is used only for material implementation baseline, exact accepted
    action movement, commit, rollback, and reviewer diff evidence. It is not
    batch lifecycle or queue authority.
13. Recovery/advisor, finalization, closeout/reconciliation, public phase-label
    migration, physical deletion, bridge removal, and successor selection are
    absent from the candidate diff.
14. Focused tests, catalog validation, conditional Ruff and BasedPyright,
    installation, exact-commit acceptance, delta-only test-quality review, and
    final independent review are green at their assigned gates.
15. Candidate installed feature versions move together for every changed
    installed surface; stable-home status and the default generation remain
    unchanged.
16. The complete v1 enum/nullability contract accepts reserved `blocked`,
    `failed`, `closeout_same_batch`, and `require_user` values without CCFG-26B
    authoring or transitioning on them. Conditional validation recognizes only
    the two tabled CCFG-26B combinations; every other structurally valid
    reserved combination is persisted and surfaced, then stops without any
    runner transition or inferred correction.
17. Every flight records input/output token counts, compaction count, file and
    line delta, validation command count and breadth, support agents, review
    lenses, duration, and blocker/recovery transitions; unavailable measurements
    are explicit `null` and empty collections are retained.
18. The candidate last-slice `finalize_same_batch` proof stops at a durable
    handoff only. The later stable final-validation/closeout invocation for this
    child batch neither implements nor activates permanent CCFG-26D behavior.

### Focused Validation

Run the current required-green runner baseline, the exact
`implementation-created` post-change focused command, the required-green
command-owner catalog validator, conditional Ruff and BasedPyright, and
`git diff --check`. Reproduce the exact known-red command and require no new
failure. The deterministic two-flight test plus catalog validation are the
durable per-slice integration-harness substitute. Do not run candidate
installation or exact-commit project acceptance from the worker.

Because tests change, run delta-only `test-quality-review` after focused tests
are green. Then request a fresh independent `runway_reviewer` on the exact
task-scoped diff.

### Commit

`feat(work-batch): add fresh slice flights`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 1. Revalidate fresh strict context and the exact write scope. Implement
only the successful queued-runway-to-one-slice flight. Preserve the serialized
phase names and existing worker/reviewer authority. Keep the runner mechanical;
`work-batch` must author lifecycle and next-action decisions. Do not spawn,
delegate to, or wait on other agents. Do not edit Batch Runway or Architecture
Program Runway skill semantics, add a second runner/store, implement recovery,
finalization, closeout, or successor behavior, or run installation/exact-
acceptance gates unless the coordinator explicitly assigns a focused command.

### Reviewer Brief

Independently review the exact task-scoped diff or commit supplied by the
coordinator and echo `diff_basis` plus verified strict identity. Verify sole
`work-batch` happy-path authority, one slice per fresh process, exact durable
result/receipt equality, unique ordered artifacts, mechanical runner behavior,
unchanged worker/reviewer authority, exact phase identities, no inference from
Git or chat history, test quality, and every deferred CCFG-26C through CCFG-26E
boundary. Reject silent fallback, overwritten evidence, runner-authored next
actions, scope expansion, or successor behavior. Do not edit or spawn agents.

### Slice Stop Conditions

- Stop if Planning State cannot prove the same current scope or the strict live
  lease preflight is blocked.
- Stop if one implementation slice cannot complete and persist its exact flight
  result without recovery, finalization, or closeout behavior.
- Stop if a fresh process cannot resume solely from canonical state, the active
  runway, immediately relevant prior receipt, retained migration facts, and a
  fresh lease.
- Stop if repeated execute flights overwrite receipts, inventories, manifests,
  telemetry, session identity, or commit evidence.
- Stop if the runner must author or infer the flight next action.
- Stop if any registered role's authority changes without a direct failing test
  and independent review.
- Stop if Batch Runway or Architecture Program Runway skill semantics, phase
  identities, recovery, finalization, closeout, bridge, stable home, default
  generation, or successor state would change.
- Stop on a path outside the validated ceiling, unrelated dirt, validation
  drift, or a clearly oversized boundary without a reviewed smaller alternative.
- After the one clean Slice 1 commit, receipt, ledger update, and completed-
  slice archive, stop this `work-batch` invocation before final validation or
  another implementation slice under the temporary stable policy.

## Final Validation

After Slice 1 has one clean candidate commit and its stable execution receipt is
durable, a later explicit `work-batch` invocation may run final validation and
close this batch under the existing stable finalization/closeout behavior:

1. refresh the strict live lease from this immutable planning snapshot and
   accepted candidate movement;
2. rerun this exact final focused suite and catalog validation as
   `required-green`, followed by triggered Ruff and BasedPyright plus
   `git diff --check`:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
     tests/test_work_batch_flight_contract.py \
     tests/test_architecture_program_runner_phase_contract.py \
     tests/test_architecture_program_runner_state.py \
     tests/test_architecture_program_runner_validation.py \
     tests/test_architecture_program_runner_transition.py \
     tests/test_architecture_program_runner_run_loop.py \
     tests/test_architecture_program_runner_artifacts.py \
     tests/test_architecture_program_runner_environment.py \
     tests/test_architecture_program_runner_command.py \
     tests/test_command_owner_behavioral_scenarios.py \
     tests/test_codex_features_manifest.py \
     tests/test_batch_lifecycle_guards.py

   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
     scripts/command_owner_scenarios.py validate \
     tests/fixtures/command-owner-scenarios
   ```

3. reproduce the exact known-red command and require no new failure;
4. run these exact candidate installation/status/dry-run commands and require
   the stable managed-feature status bytes to remain identical:

   ```sh
   ccfg26b_validation_root="$(mktemp -d /tmp/ccfg-26b-final.XXXXXX)"
   ccfg26b_fresh_codex_home="$ccfg26b_validation_root/fresh-codex-home"
   mkdir -p "$ccfg26b_fresh_codex_home"
   ./install.sh --codex-home /home/alacasse/.codex --status \
     > "$ccfg26b_validation_root/stable-status-before.txt"
   ./install.sh --codex-home "$ccfg26b_fresh_codex_home" --all
   ./install.sh --codex-home "$ccfg26b_fresh_codex_home" --status
   ./install.sh --codex-home "$ccfg26b_fresh_codex_home" --dry-run
   ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --all
   ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
   ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
   ./install.sh --codex-home /home/alacasse/.codex --status \
     > "$ccfg26b_validation_root/stable-status-after.txt"
   cmp "$ccfg26b_validation_root/stable-status-before.txt" \
     "$ccfg26b_validation_root/stable-status-after.txt"
   ```

5. run exact-commit command-owner acceptance once with fresh outputs:

   ```sh
   COMMAND_OWNER_CANDIDATE_CODEX_HOME=/home/alacasse/.codex-command-owner-redesign \
   PYTHONDONTWRITEBYTECODE=1 \
     .venv/bin/python scripts/command_owner_scenarios.py accept \
     tests/fixtures/command-owner-scenarios \
     --result-output "$ccfg26b_validation_root/acceptance-result.json" \
     --json-report-output "$ccfg26b_validation_root/report.json" \
     --text-report-output "$ccfg26b_validation_root/report.txt"
   ```

6. read the result and text report and record their hashes:

   ```sh
   sed -n '1,240p' "$ccfg26b_validation_root/report.txt"
   sha256sum "$ccfg26b_validation_root/acceptance-result.json" \
     "$ccfg26b_validation_root/report.json" \
     "$ccfg26b_validation_root/report.txt"
   ```
7. run delta-only `test-quality-review` over the final test range;
8. request final independent `runway_reviewer` and only actually triggered
   specialist reviews; and
9. confirm the exact candidate range and canonical planning changes contain no
   unrelated path, recovery/finalization/closeout behavior, phase-label change,
   stable-home mutation, or successor selection.

All final gates are `required-green` except the explicitly classified unchanged
known-red baseline. Final validation is not an implementation slice.

## Batch Stop Conditions

- Stop on any semantic currentness source other than Planning State.
- Stop if candidate code restores Git-derived lifecycle or queue inference.
- Stop if the happy path depends on chat chronology, old Batch Runway semantic
  ownership, or runner-authored slice decisions.
- Stop if candidate installation changes stable-home ownership or canonical
  queue state.
- Stop if exact acceptance is not bound to the clean candidate commit.
- Stop if CCFG-26C through CCFG-26E or any later finding is selected or prepared.

## Closeout Contract

Closeout may:

- complete only `ccfg-26b-fresh-slice-flight` and record its candidate commit,
  focused validation, ordered flight receipts, fresh-process proof,
  installation, exact acceptance, test-quality review, and independent review;
- keep parent CCFG-26 `Prepared`, not `Closed`;
- record CCFG-26B as the completed predecessor for CCFG-26C;
- clear only this batch's selected, queued, and active state; and
- preserve CCFG-26C through CCFG-26E and CCFG-27 through CCFG-29 as unselected.

Closeout must not select, dispatch, queue, create, refresh, or prepare CCFG-26C
or any successor. A later explicit stable `plan-batch` invocation owns that
selection.
