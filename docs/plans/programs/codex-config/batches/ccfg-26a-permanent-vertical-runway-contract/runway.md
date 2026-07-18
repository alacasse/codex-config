# CCFG-26A Permanent Vertical Runway Contract

## Purpose

Install and prove the permanent candidate planning behavior needed for eventual
parity on vertical CCFG-26 ownership-transfer planning. This batch implements
issue #60 in the candidate `plan-batch` command, planner, reviewer, deterministic
queue gate, and planning-runway contract. It does not make candidate generation
authoritative for canonical planning and does not transfer any execution or
closeout ownership. Until CCFG-29 integrates the candidate and changes the
default generation, stable `plan-batch` under the temporary CCFG-34 repository
policy remains the canonical planning path for CCFG-26B through CCFG-26E.

## Source Contract

- Selected dispatch: `dispatch.md`
- Program ledger: `../../LEDGER.md`, CCFG-26 only
- COR-009 accepted snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Live amendments:
  - `../../findings/command-owner-redesign-planning-execution-carry-forward.md`
  - `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`
- Temporary execution policy:
  `../../notes/stable-runway-dogfooding-policy.md`
- Permanent requirements: GitHub issues #59, #60, and #61
- Superseded historical evidence only:
  `../ccfg-26-execution-closeout-ownership-transfer/`

This runway covers CCFG-26A only. CCFG-26 remains open after this preparation
batch and may become `Prepared` at closeout. CCFG-26B through CCFG-26E remain
unselected.

## CCFG-26 Vertical Sequence

| Child batch | Starting scenario | Durable result | State |
|---|---|---|---|
| CCFG-26A | candidate planning receives a migration or ownership-transfer finding | permanent vertical plan and independent review contract | queued by this runway |
| CCFG-26B | one queued slice is ready to execute | fresh coordinator completes worker, focused validation, review, commit, and durable flight receipt | deferred |
| CCFG-26C | an eligible mechanical blocker stops a slice | one read-only advisor classifies it, a bounded amendment is independently reviewed, and the same slice resumes fresh | deferred |
| CCFG-26D | the last implementation-slice receipt is durable | separate final validation/finalization flight and receipt | deferred |
| CCFG-26E | finalization receipt is durable | separate closeout/reconciliation/no-successor flight and removal of last displaced semantic owners | deferred |

CCFG-26B depends on successful CCFG-26A completion as a program sequencing and
candidate-parity boundary, not because candidate planning becomes authoritative
after CCFG-26A. A later explicit stable `plan-batch` invocation owns selection
and planning of CCFG-26B. CCFG-26C through CCFG-26E remain subject to the same
stable canonical-planning path until CCFG-29.

CCFG-27 retains the serialized runner-protocol decision, CCFG-28 retains
physical legacy deletion and default switch, and CCFG-29 retains final
integration, bridge removal, and removal of the temporary CCFG-34 policy.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1 risk: `migration`.
- Approval gate: issue #60 plus the CCFG-26 ledger row and this explicit
  `plan-batch` request authorize permanent rejection of migration or
  ownership-transfer runways that omit vertical fields or ambiguous-caller
  removal conditions. The exact dispatch and runway still require clean
  independent planning review before queueing and the exact candidate diff
  requires independent implementation review before commit.
- No other destructive, migration, demotion, or narrowing action is approved.

### Vertical Contract Applicability

```yaml
vertical_contract_applicability:
  applies_when:
    slice_risk: migration
  prose_inference: forbidden
```

Every implementation slice with the exact machine-readable value
`risk: migration` must carry the complete `vertical_slice` object below.
Ownership-transfer work must therefore classify its implementation slice as
`risk: migration`. A `mixed-risk` batch is not subject to the contract in full:
only its `migration` slices are. Non-migration slices remain valid without
vertical migration fields. Applicability never depends on free-form prose.

The following owners must use this exact predicate without alternate inference:

- `batch_planner`;
- `batch_plan_reviewer`;
- `plan-batch`;
- `scripts/plan_batch.py`; and
- `planning-runway/v1`.

```yaml
vertical_slice_field_contract:
  ownership_coexistence:
    enum:
      - none
      - temporary
    other_values: forbidden
migration_matrix_rule:
  when_ownership_coexistence_is_temporary:
    matrix_required: true
    matrix_must_be_non_empty: true
  when_ownership_coexistence_is_none:
    matrix_required: true
    matrix_must_be_empty: true
```

`vertical_slice.ownership_coexistence` is required for every applicable slice
and accepts exactly `none` or `temporary`; every other value is rejected.
Each non-empty matrix row must contain exactly the caller or scenario key plus
`current_owner`, `future_owner`, `reason`, `status`, and
`removal_slice_or_condition`; `status` is `pending` or `migrated`.

## Current Baseline And Assumptions

- Stable planning/toolchain checkout:
  `/home/alacasse/projects/codex-config`
- Stable planning/toolchain commit at plan time:
  `0ff5dea39cc80c5a313c5f70076d22b3d0973f62`
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Candidate branch: `implementation/command-owner-redesign`
- Candidate baseline:
  `89671eceb9103039e7e6660e73837827c167a3a1`
- Both worktrees were clean at planning time.
- Planning State `current` and `validate` passed with no selected dispatch,
  queued batch, active runway, blocker, or obligation before this queue
  transition.
- Focused candidate baseline was green:
  - 66 focused plan-batch, agent-contract, and behavioral-scenario tests;
  - 27 planning-schema/manifest tests plus 20 subtests; and
  - command-owner catalog validation for 69 scenarios.
- The two existing CCFG-26 ownership assertions remain known red and are not
  owned by CCFG-26A.
- The installed strict helper resolves to the stable toolchain helper.

## Whole-Batch Non-Goals

- No work-batch execution kernel, recovery, lease, finalization, closeout, or
  reconciliation transfer.
- No Batch Runway or APR execution/closeout narrowing.
- No worker/reviewer execution-role change.
- No recovery-advisor agent or contract.
- No execution-flight process, schema, receipt, state, launcher, or telemetry.
- No serialized runner phase identity or public runner protocol change.
- No candidate bridge, stable bridge, candidate installation-root, stable home,
  default generation, or canonical planning authority change.
- No physical legacy deletion, final integration, or successor selection.

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
  toolchain_commit: 0ff5dea39cc80c5a313c5f70076d22b3d0973f62
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 0ff5dea39cc80c5a313c5f70076d22b3d0973f62
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 89671eceb9103039e7e6660e73837827c167a3a1
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Plan-time validation receipt:

```yaml
interface: cross-checkout-receipt/v1
caller: plan-batch
reason: CCFG-26A permanent vertical-runway contract selection and queue transition
generation_role: stable
canonical_state_mutation_allowed: true
canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
repository_revisions:
  toolchain_commit: 0ff5dea39cc80c5a313c5f70076d22b3d0973f62
  canonical_planning_commit_before: 0ff5dea39cc80c5a313c5f70076d22b3d0973f62
  implementation_commit_before: 89671eceb9103039e7e6660e73837827c167a3a1
planning_paths:
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/dispatch.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/runway.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26a-permanent-vertical-runway-contract/review.md
implementation_paths:
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/plan-batch
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/batch_planner.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/batch_plan_reviewer.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/plan_batch.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/planning_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/schemas/planning-runway-v1.schema.json
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_plan_batch.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_planning_contract_schema.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_custom_agent_contracts.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codex_features_manifest.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_behavioral_scenarios.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_scenario_catalog.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/planning-contracts
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/catalog.yaml
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/workflow-cases.yaml
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/workflow_adapters.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/codex-features.json
  - /home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md
deletion_condition: CCFG-29 final integration
```

This immutable planning snapshot is historical plan-time evidence, not a live
execution lease. Do not edit its revisions after the containing planning commit.
Before the first worker handoff, `work-batch` must confirm the same selected
scope through Planning State and pass the strict ready/blocked preflight to
obtain a fresh live lease.

## Project Values

- Planning Artifact Layout: Planning Artifact Layout v1.
- Planning location: this batch directory.
- Program root: `docs/plans/programs/codex-config`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`; use explicit temporary outputs under `/tmp`.
- Output root: `None`; use explicit temporary outputs under `/tmp`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: `scripts/command_owner_scenarios.py accept` with explicit
  result, JSON report, and text report paths.
- Summary artifact: generated text report and result JSON from the exact
  acceptance invocation.
- Index refresh: none.
- Candidate commit requirement: one focused candidate commit for Slice 1.
- Canonical planning receipts and final same-batch closeout are separate stable
  commits; self-referential final closeout fields use `this closeout commit`.
- Preserve unrelated dirt and stop on task-scope overlap.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2; registered agent TOMLs own
their exact result schemas.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status and
receipt summaries.
Use Batch Runway Orchestration Anomaly Log v1 only for suspicious coordination
or subagent-lifecycle behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine execution.
Use the strict cross-checkout context v1 consumer contract for every handoff.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md` only on deviation
- `skills/batch-runway/references/finalize-batch-v1.md` only at finalization

Overrides:

- Apply the repository-local stable-runway dogfooding policy. One
  `work-batch` invocation executes at most the next incomplete implementation
  slice; this runway contains exactly one implementation slice.
- Execution writes occur only in the candidate repository. Stable canonical
  planning writes remain coordinator-owned.
- After test changes, run delta-only `test-quality-review` before final runway
  review.
- Do not run project-level acceptance from a worker. The coordinator owns the
  exact final candidate acceptance and output summary read.

## Validation Profile And Status Classes

Selected profile: `project-harness-production`.

### Current Green Baselines

These commands are `required-green`; they passed at candidate baseline
`89671ec` and Slice 1 owns keeping them green while adding the new cases:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_custom_agent_contracts.py \
  tests/test_planning_contract_schema.py \
  tests/test_command_owner_behavioral_scenarios.py

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_plan_batch_roles_are_registered_with_disjoint_exact_results \
  tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_plan_batch_command_owner_runtime_boundaries_are_explicit

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  scripts/command_owner_scenarios.py validate \
  tests/fixtures/command-owner-scenarios
```

### CCFG-26 Known-Red Diagnostics

The following exact command is `known-red-baseline`. It currently has two
failures owned by later CCFG-26 child batches and must not gate CCFG-26A:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_work_batch_reconciles_same_batch_closeout \
  tests/test_batch_lifecycle_guards.py::BatchLifecycleGuardTests::test_architecture_program_closeout_rejects_dispatch_runway_only_evidence
```

### Conditional Gates

- Ruff over changed Python and test files: `conditional` when Python changes.
- Configured-project BasedPyright over exact changed Python files:
  `conditional` when typed Python changes; the repository-wide configured
  project remains diagnostic and must not be silently promoted.
- Planning contract schema fixture validation: `conditional` when the runway
  JSON Schema or `scripts/planning_contract.py` changes.
- Candidate installation and exact-commit scenario acceptance:
  `required-green` at final validation, not per worker.
- `git diff --check`: `required-green` after Slice 1 and at final validation.
- Delta-only `test-quality-review`: `required-green` after changed tests and
  before the final implementation review.

## Implementation Write-Path Ceiling

Required candidate paths:

- `skills/plan-batch/**`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- `schemas/planning-runway-v1.schema.json`
- `tests/test_plan_batch.py`
- `tests/test_planning_contract_schema.py`
- `tests/test_custom_agent_contracts.py`
- `tests/test_codex_features_manifest.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/fixtures/planning-contracts/**`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/fixtures/command-owner-scenarios/workflow-cases.yaml`
- `tests/fixtures/command-owner-scenarios/workflow_adapters.py`
- `codex-features.json`
- `CHANGELOG.md`

Conditional candidate path:

- `scripts/planning_contract.py`, only when the existing planning-runway
  artifact validator must directly consume the new fields and a focused failing
  schema test records that need before the edit.

No other candidate path is authorized. Exact allowed paths are an upper ceiling,
not a requirement to touch every file.

## Proportionality And Slice Shape

```yaml
slice_shape:
  initial_count: 1
  final_count: 1
  rationale: one complete migration-planning scenario requires the command owner, planner, reviewer, deterministic gate, schema, and focused proof to change atomically; splitting authoring from independent enforcement would leave a queueable but unreviewed intermediate contract
smaller_alternative_analysis:
  alternative: split planner/schema authoring from reviewer/deterministic-gate enforcement
  rejected_because: the intermediate state would allow one side of the planning transaction to accept a plan the other side cannot author or independently verify
  advisory_recheck: before implementation review, record changed-file count, line delta, primary production surfaces, ownership boundaries, migration kinds, specialist lenses, and whether coordinator compaction occurred; if the boundary is clearly oversized, stop for a reviewed smaller alternative
```

The slice count is a semantic output. No numeric threshold is a hard limit and
no filler slice may be added to satisfy one.

## Execution Ledger

| Slice | Status | Commit | Review | Notes |
|---|---|---|---|---|
| 1. Queue one permanently vertical migration plan | Pending | None | Pending | One planning scenario; no execution-owner change. |

Move the completed row to `completed-slices.md` after its clean focused
candidate commit. The active ledger keeps only pending or active work.

## Slice 1 — Queue One Permanently Vertical Migration Plan

### Vertical Slice

```yaml
risk: migration
vertical_slice:
  starting_scenario: candidate plan-batch receives one migration or ownership-transfer finding
  durable_result: the queued planning-runway/v1 artifact and exact independent review prove every implementation slice has a starting scenario, durable result, explicit ownership movement, focused validation, rollback-safe intermediate state, and named residue
  owner_before: candidate plan-batch generic semantic-slice and proportionality checks plus temporary stable manual policy
  owner_after: permanent candidate plan-batch with batch_planner authoring, batch_plan_reviewer enforcement, and scripts/plan_batch.py deterministic rejection
  migrated_callers:
    - skills/plan-batch/SKILL.md generated-plan gate
    - agents/batch_planner.toml draft result
    - agents/batch_plan_reviewer.toml exact review result
    - scripts/plan_batch.py deterministic queue validation
    - planning-runway/v1 migration and ownership-transfer artifacts
  focused_validation:
    - focused plan-batch, schema, agent, manifest, and behavioral-scenario tests
    - command-owner scenario catalog validation
    - delta-only test-quality review
    - independent exact-diff runway review
  independently_usable_state: candidate planning behavior is complete, testable, and integration-ready for eventual parity while stable plan-batch plus the temporary CCFG-34 policy remain canonical until CCFG-29
  rollback_boundary: one focused candidate commit back to 89671ec; stable planning and default Codex home remain unchanged
  temporary_residue:
    - stable CCFG-34 policy and root instruction hook until CCFG-29
    - work-batch, Batch Runway, and APR execution/closeout ownership until CCFG-26B through CCFG-26E
    - per-flight execution telemetry until later CCFG-26 child batches
  ownership_coexistence: temporary
```

### Migration Matrix

```yaml
migration_matrix_rule:
  when_ownership_coexistence_is_temporary:
    matrix_required: true
    matrix_must_be_non_empty: true
  when_ownership_coexistence_is_none:
    matrix_required: true
    matrix_must_be_empty: true
migration_matrix:
  planner_draft:
    current_owner: batch_planner generic semantic rationale
    future_owner: batch_planner required vertical_slice and migration_matrix authoring
    reason: the planner must author one complete scenario and durable ownership result before review
    status: pending
    removal_slice_or_condition: Slice 1 focused tests and review are green
  independent_review:
    current_owner: batch_plan_reviewer generic semantic and proportionality checks
    future_owner: batch_plan_reviewer vertical ownership, residue, rollback, and smaller-alternative enforcement
    reason: exact independent review must reject ambiguous callers and avoidable horizontal phases
    status: pending
    removal_slice_or_condition: Slice 1 focused tests and review are green
  plan_batch_command_contract:
    current_owner: plan-batch generated-plan checklist and command stop boundary
    future_owner: plan-batch permanent vertical migration-plan requirement
    reason: the human-facing command must require the same vertical evidence its planner, reviewer, and deterministic gate consume
    status: pending
    removal_slice_or_condition: Slice 1 focused tests and review are green
  queue_validation:
    current_owner: scripts/plan_batch.py semantic rationale validation
    future_owner: scripts/plan_batch.py permanent vertical planning validation
    reason: incomplete vertical evidence must fail mechanically before DEC-038 queue mutation
    status: pending
    removal_slice_or_condition: Slice 1 exact acceptance is green
  planning_runway_artifact:
    current_owner: planning-runway/v1 generic slice fields
    future_owner: planning-runway/v1 required vertical_slice fields and caller migration matrix
    reason: the durable runway must preserve exact ownership, residue, validation, and rollback evidence for later execution
    status: pending
    removal_slice_or_condition: Slice 1 exact acceptance is green
  stable_temporary_policy:
    current_owner: root AGENTS.md plus stable-runway dogfooding policy
    future_owner: integrated candidate planning behavior
    reason: stable agents still need automatic instruction discovery until integrated candidate parity is proven
    status: pending
    removal_slice_or_condition: CCFG-29 candidate parity and integration gate
  execution_metrics:
    current_owner: temporary manual evidence only
    future_owner: later CCFG-26 work-batch flight contracts
    reason: durable per-flight metrics require the execution-flight owner deferred to later CCFG-26 child batches
    status: pending
    removal_slice_or_condition: final CCFG-26 closeout
```

### Scope

- Extend the existing planning-runway artifact shape compatibly so every slice
  whose exact risk value is `migration` carries the complete `vertical_slice`
  object and required `migration_matrix`. Ownership-transfer work must use that
  risk. Temporary coexistence requires a non-empty matrix; `none` requires an
  explicit empty matrix. Every retained route must name its caller, current
  owner, retention reason, future owner, status, and removal condition.
- Make `batch_planner` start from one complete behavioral scenario, declare
  rollback-safe independently usable state, name all temporary residue, and
  derive count from semantic boundaries.
- Make `batch_plan_reviewer` reject ambiguous ownership, silent fallbacks,
  horizontal phase decomposition when a smaller vertical sequence exists, and
  clearly oversized boundaries without a smaller-alternative analysis.
- Make `plan-batch` and `scripts/plan_batch.py` mechanically bind those fields
  and exact review checks before queue mutation.
- Preserve final-range validation outside implementation slices and preserve
  advisory rather than arbitrary hard numeric proportionality thresholds.
- Add focused target scenarios and exact contract tests.
- Update feature version/installation metadata and changelog only as required
  for this behavior.

### Allowed Files

Only the required and conditional paths under the Implementation Write-Path
Ceiling.

### Non-Goals

- No execution, recovery, flight, finalization, closeout, reconciliation,
  runner, worker, reviewer, bridge, or default-generation behavior change.
- No new planning artifact identity, store, transaction, queue path, persistent
  draft, source adapter, or compatibility wrapper.
- No arbitrary numeric slice-count or diff-size rejection.
- No test that preserves the temporary stable policy as a permanent candidate
  dependency.

### Acceptance Criteria

- A `migration` slice cannot queue without every required `vertical_slice`
  field, including explicit `ownership_coexistence`.
- Temporary coexistence cannot queue without a complete non-empty caller
  migration matrix including the retention reason and removal condition;
  migrated callers cannot silently fall back.
- `ownership_coexistence: none` requires an explicit empty migration matrix.
- Non-migration slices remain valid without vertical migration fields, including
  non-migration slices in a `mixed-risk` batch.
- Planner authoring, independent review, deterministic queue validation, and
  artifact validation use the same exact
  `vertical_contract_applicability.applies_when.slice_risk: migration`
  predicate and never infer applicability from prose.
- The planner starts from one scenario and one durable result and derives slice
  count from independently useful boundaries.
- The reviewer rejects horizontal phases and missing ownership/residue evidence
  and requires a smaller-alternative analysis for a clearly oversized boundary.
- Focused validation is slice-local while final-range validation stays separate.
- One-slice plans remain valid when the owner, risk, validation, review, and
  rollback boundary is cohesive.
- The exact CCFG-26A implementation diff records advisory proportionality facts
  without turning advisory numbers into hard limits.
- Candidate installation contains the updated command and registered roles;
  stable installation and default generation are unchanged.
- CCFG-26 work-batch ownership assertions remain known red and no later child
  batch is selected.

### Required Future Predicate Tests

1. `accepts_migration_with_complete_vertical_contract_and_no_coexistence` — a
   `migration` slice with all vertical fields and `ownership_coexistence: none`
   is accepted with an explicit empty matrix.
2. `accepts_migration_with_temporary_coexistence_and_complete_matrix` — a
   `migration` slice with temporary coexistence and a complete non-empty matrix
   is accepted.
3. `rejects_migration_missing_vertical_slice` — a `migration` slice without
   `vertical_slice` is rejected.
4. `rejects_temporary_coexistence_with_empty_or_incomplete_matrix` — temporary
   coexistence with an empty matrix or a row missing any required field is
   rejected.
5. `rejects_no_coexistence_with_retained_matrix_rows` —
   `ownership_coexistence: none` with retained rows is rejected.
6. `accepts_non_migration_without_vertical_contract` — a non-migration slice
   remains valid without vertical migration fields.
7. `applies_mixed_risk_contract_only_to_migration_slices` — a `mixed-risk`
   batch applies the contract only to slices whose exact risk is `migration`.

### Focused Validation

Run the Current Green Baselines, all new/changed focused tests, conditional
Ruff/type/schema checks, command-owner catalog validation, and
`git diff --check`. Do not run exact-commit acceptance from the worker.

Because tests change, run delta-only `test-quality-review` after focused tests
are green. Then request a fresh independent `runway_reviewer` on the exact
task-scoped diff.

### Commit

`feat(plan-batch): require vertical migration runways`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 1. Revalidate fresh strict context, implement only the one planning
scenario in the candidate repository, and return the exact v2 result. Do not
spawn, delegate to, or wait on other agents. Do not edit any execution-owner,
runner, recovery, finalization, closeout, reconciliation, bridge, or stable
planning surface. Do not run candidate installation or project-wide exact
acceptance unless the coordinator explicitly assigns a focused command.

### Reviewer Brief

Independently review the exact task-scoped candidate diff or commit supplied by
the coordinator and echo `diff_basis` plus verified strict identity. Verify the
vertical fields, migration matrix, smaller-alternative contract, exact queue
gate, behavioral proof, contract-narrowing approval, write-path ceiling, and
absence of runtime ownership changes. Do not edit or spawn agents.

### Slice Stop Conditions

- Stop if a second implementation scenario is required.
- Stop if the planning-runway identity, planning store, queue transaction,
  lifecycle state, persistent draft, source adapter, or compatibility layer
  must change.
- Stop if the candidate cannot enforce the contract without changing
  work-batch, Batch Runway, APR, runner, execution-role, or bridge behavior.
- Stop if one side of planner/reviewer/deterministic validation would accept a
  plan the others cannot author or verify.
- Stop if a clearly oversized diff lacks a reviewed smaller alternative.
- Stop on any path outside the exact ceiling or any stable-home/canonical-
  planning/default-generation mutation.

## Final Validation

After Slice 1 has a clean focused candidate commit:

1. refresh the strict lease from the immutable planning snapshot and accepted
   candidate movement;
2. rerun all Slice 1 focused gates plus affected planning-contract and command-
   owner test subsets;
3. run the command-owner catalog validator;
4. run a clean candidate installation into a fresh `/tmp` Codex home and the
   isolated candidate Codex home; compare stable-home status before and after;
5. run exact-commit command-owner scenario acceptance with fresh result, JSON
   report, and text report outputs under `/tmp`;
6. read the text report and record hashes for the result and JSON report;
7. run delta-only `test-quality-review` if the final range adds test changes;
8. request final independent `runway_reviewer` and triggered specialist reviews
   only for actually changed surfaces; and
9. run `git diff --check` and confirm both worktrees have no unrelated dirt.

All final gates are `required-green`. The two declared later CCFG-26 known-red
assertions may remain only with the same exact failures and no new failures.

## Batch Stop Conditions

- Stop on any execution/closeout owner, recovery advisor, fresh-flight runtime,
  runner protocol, worker/reviewer execution role, bridge, default generation,
  or physical legacy change.
- Stop if candidate installation changes the stable home or canonical planning
  state.
- Stop if final acceptance is not bound to the clean exact candidate commit.
- Stop if the temporary stable policy becomes a permanent candidate dependency
  instead of behavior migrated under candidate owners.
- Stop if issue #59 or #61 implementation is pulled into CCFG-26A.
- Stop if CCFG-26B through CCFG-26E are selected, queued, prepared, or begun.

## Closeout Contract

Closeout may:

- complete CCFG-26A and record its candidate commit, focused validation,
  installation, exact acceptance, test-quality review, and independent review;
- mark the parent CCFG-26 finding `Prepared`, not `Closed`;
- record that permanent issue #60 planning behavior is complete while issues
  #59, #61, and COR-009 execution/closeout ownership remain open;
- clear only the CCFG-26A selected/queued/active state; and
- preserve CCFG-26B through CCFG-26E as unselected candidate batches.

Closeout must not select, dispatch, queue, create, refresh, or prepare a later
child batch or any successor finding. A later explicit stable `plan-batch`
invocation owns selection and planning of CCFG-26B; candidate behavior remains
integration-ready but non-authoritative until CCFG-29.
