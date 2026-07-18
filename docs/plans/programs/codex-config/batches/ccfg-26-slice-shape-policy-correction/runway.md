# CCFG-26 Slice-Shape Policy Correction Runway

Status: `implementation and final validation complete; closeout pending`

## Purpose

Decouple planning-slice shape from mutation risk before CCFG-26 execution
ownership begins moving. The candidate `plan-batch` command, planning author,
independent planning reviewer, deterministic gate, and `planning-runway/v1`
artifact must consume one project-owned policy and persist every new slice's
selected shape. Migration ownership evidence remains complete but no longer
activates or represents verticality.

This runway covers only the issue #66 correction under CCFG-26. CCFG-26A
remains completed historical evidence. CCFG-26B through CCFG-26E remain
unselected and blocked on this batch's closeout.

## Source Contract

- Selected dispatch: `dispatch.md`
- Program ledger: `../../LEDGER.md`, CCFG-26 only
- Accepted direction: `../../findings/slice-shape-policy-direction.md`
- Temporary execution policy:
  `../../notes/stable-runway-dogfooding-policy.md`
- Completed predecessor evidence:
  `../ccfg-26a-permanent-vertical-runway-contract/closeout.md`
- COR-009 accepted snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1 risk: `contract-narrowing`.
- Slice 1 selected shape: `vertical`.
- Approval gate: issue #66, the amended CCFG-26 ledger row, the accepted
  direction note, and the explicit request to plan this correction authorize
  direct replacement of the current migration-coupled runway representation.
  Historical runways remain readable at their original commits but receive no
  compatibility reader, migration, second dialect, or fallback.
- The gate does not authorize any execution-owner, runner, bridge,
  default-generation, physical-deletion, or successor action.

## Resolved Policy Boundary

The project-owned policy instance will live at:

```text
docs/plans/programs/codex-config/notes/slice-shape-policy.md
```

The active program context will reference it from:

```text
docs/plans/programs/codex-config/CURRENT.md
```

Its complete initial payload is:

```yaml
schema: slice-shape-policy/v1
default_shape: vertical
allow_override: true
require_override_reason: true
```

`plan-batch` resolves this project-owned instance once and supplies the exact
same payload to `batch_planner`, `batch_plan_reviewer`, deterministic queue
validation, and artifact validation. The reusable skill must not hard-code the
codex-config path. Planning State remains the diagnostic and project-policy
source reporter; it does not become a generic configuration loader or slice-
shape decision owner.

Every newly produced `planning-runway/v1` slice persists:

```yaml
shape:
  selected: vertical | horizontal
  override_reason: null | non-empty string
```

The schema validates this representation. The deterministic gate additionally
checks it against the resolved policy. Independent review decides whether a
non-empty override reason is architecturally persuasive.

Migration-specific evidence uses `migration_evidence` plus
`migration_matrix`, required only for `risk: migration` regardless of selected
shape. The object preserves the complete CCFG-26A field set:

```yaml
migration_evidence:
  starting_scenario: string
  durable_result: string
  owner_before: string
  owner_after: string
  migrated_callers: [non-empty strings]
  focused_validation: [non-empty strings]
  independently_usable_state: string
  rollback_boundary: string
  temporary_residue: [strings]
  ownership_coexistence: none | temporary
migration_matrix: {}
```

`ownership_coexistence: temporary` requires a complete non-empty matrix whose
rows retain `current_owner`, `future_owner`, `reason`, `status`, and
`removal_slice_or_condition`. `ownership_coexistence: none` requires an explicit
empty matrix. The old misleading `vertical_slice` name is not retained.

## Current Baseline And Assumptions

- Stable planning/toolchain checkout:
  `/home/alacasse/projects/codex-config`
- Stable planning/toolchain commit at plan time:
  `90cb96e03c2be9eef100f23d768860f07ab8e2af`
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Candidate branch: `implementation/command-owner-redesign`
- Candidate baseline:
  `a0835f146857612dcd5a95053d67c53f32449012`
- Candidate worktree was clean at planning time.
- Stable canonical planning had only the issue #66 intake changes in
  `CURRENT.md`, `LEDGER.md`, and `findings/slice-shape-policy-direction.md`;
  those intentional edits are preserved.
- Planning State `current` and `validate` passed with no selected dispatch,
  queued batch, active runway, blocker, or obligation before this queue
  transition.
- CCFG-26A's exact candidate baseline remains green for focused planning tests,
  installed candidate features, and command-owner scenario acceptance.
- The known later-CCFG-26 execution-ownership failures remain diagnostic only
  and are not owned by this correction.

## Whole-Batch Non-Goals

- No `work-batch` execution, recovery, finalization, closeout, or reconciliation
  ownership implementation.
- No CCFG-26B through CCFG-26E selection or preparation.
- No CCFG-26A rewrite or historical artifact migration.
- No new generic configuration framework, policy inheritance, bundled strategy
  set, automatic shape classifier, numeric threshold, approval tier, or plugin
  system.
- No new planning store, lifecycle state, persistent draft, queue transaction,
  public command, or alternate artifact identity.
- No runner protocol, worker/reviewer execution role, bridge, stable-home,
  default-generation, physical deletion, or final integration change.

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
  toolchain_commit: 90cb96e03c2be9eef100f23d768860f07ab8e2af
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 90cb96e03c2be9eef100f23d768860f07ab8e2af
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: a0835f146857612dcd5a95053d67c53f32449012
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Plan-time validation receipt:

```yaml
interface: cross-checkout-receipt/v1
caller: plan-batch
reason: CCFG-26 slice-shape policy correction selection and queue transition
generation_role: stable
canonical_state_mutation_allowed: true
canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
repository_revisions:
  toolchain_commit: 90cb96e03c2be9eef100f23d768860f07ab8e2af
  canonical_planning_commit_before: 90cb96e03c2be9eef100f23d768860f07ab8e2af
  implementation_commit_before: a0835f146857612dcd5a95053d67c53f32449012
planning_paths:
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/notes/slice-shape-policy.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/dispatch.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/runway.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/review.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/completed-slices.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-slice-shape-policy-correction/closeout.md
implementation_paths:
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/plan-batch
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/batch_planner.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/batch_plan_reviewer.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/plan_batch.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/planning_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/schemas/slice-shape-policy-v1.schema.json
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

This planning snapshot is immutable historical plan-time evidence, not a live
execution lease. Do not edit its revisions after the containing planning
change. Before the first delegated handoff, `work-batch` must confirm this same
selected scope through Planning State and pass the strict ready/blocked
preflight for a fresh live lease.

## Project Values

- Planning Artifact Layout: Planning Artifact Layout v1.
- Planning location: this batch directory.
- Program root: `docs/plans/programs/codex-config`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`; use fresh explicit outputs under `/tmp`.
- Output root: `None`; use fresh explicit outputs under `/tmp`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: `scripts/command_owner_scenarios.py accept` with fresh
  result, JSON report, and text report paths.
- Summary artifact: the generated acceptance result and text report.
- Index refresh: none.
- Candidate commit requirement: one focused candidate implementation commit.
- Canonical project-policy/reference and execution-receipt changes remain
  separate stable planning commits; the final self-referential closeout uses
  `this closeout commit`.
- Preserve unrelated dirt and stop on task-scope overlap.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2; registered agent TOMLs
own their exact result schemas.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status and
receipt summaries.
Use Batch Runway Orchestration Anomaly Log v1 only for suspicious coordinator
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

- Apply the temporary stable-runway dogfooding policy. One `work-batch`
  invocation executes exactly the next incomplete implementation slice; this
  runway contains one implementation slice.
- The one worker handoff may change only the validated canonical project-policy
  paths and candidate implementation paths declared in the fresh live lease.
  Canonical queue, ledger, receipt, and closeout updates remain coordinator-owned.
- After test changes, run delta-only `test-quality-review` before final
  implementation review.
- Workers do not run candidate installation or exact-commit project acceptance.
  The coordinator owns those final gates and reads their summary artifacts.

## Validation Profile And Status Classes

Selected profile: `project-harness-production`.

### Current Green Baselines

These commands are `required-green`; they passed at candidate baseline
`a0835f1` and Slice 1 owns keeping them green while adding the new cases:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_custom_agent_contracts.py \
  tests/test_planning_contract_schema.py \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_catalog.py

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py -k plan_batch

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  scripts/command_owner_scenarios.py validate \
  tests/fixtures/command-owner-scenarios
```

### Known-Red Diagnostics

The following exact command is `known-red-baseline`. Its two later-CCFG-26
ownership failures do not gate this correction and must gain no new failures:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_work_batch_reconciles_same_batch_closeout \
  tests/test_batch_lifecycle_guards.py::BatchLifecycleGuardTests::test_architecture_program_closeout_rejects_dispatch_runway_only_evidence
```

### Conditional And Implementation-Created Gates

- `schemas/slice-shape-policy-v1.schema.json` validation tests are
  `implementation-created` by Slice 1 and become required-green before its
  review.
- Ruff over exact changed Python and test files is `conditional` when Python
  changes; use `--no-cache` in the read-only candidate environment.
- Configured BasedPyright over exact changed production Python files is
  `conditional` when typed Python changes.
- `scripts/planning_contract.py` tests are `conditional` only if the focused
  failing test justifies changing that file.
- `git diff --check` is `required-green` after Slice 1 and at final validation.
- Planning State `current` and `validate` are `required-green` after the
  canonical policy/reference change and before the stable receipt commit.
- Delta-only `test-quality-review` is `required-green` after changed tests and
  before final implementation review.
- Candidate installation and exact-commit scenario acceptance are
  `required-green` at final validation, not worker-owned per-slice work.

## Write-Path Ceiling

Required canonical planning paths:

- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/notes/slice-shape-policy.md`

Coordinator-owned canonical lifecycle paths:

- `docs/plans/programs/codex-config/LEDGER.md`
- this batch's `dispatch.md`, `runway.md`, `review.md`,
  `completed-slices.md`, and `closeout.md`

Required candidate paths:

- `skills/plan-batch/**`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `scripts/plan_batch.py`
- `schemas/slice-shape-policy-v1.schema.json`
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

- `scripts/planning_contract.py`, only when a focused failing artifact test
  proves the existing validator must directly consume the new fields.

No other implementation path is authorized. The ceiling does not require every
listed file to change.

## Proportionality And Slice Shape

```yaml
shape:
  selected: vertical
  override_reason: null
slice_shape:
  initial_count: 1
  final_count: 1
  rationale: policy resolution, authoring, independent review, deterministic enforcement, artifact persistence, and focused proof form one transaction; splitting them leaves an inert or contradictory intermediate contract
smaller_alternative_analysis:
  alternative: split project policy and schema declaration from planner, reviewer, and deterministic enforcement
  rejected_because: the first intermediate state would either be unused or allow owners to author and validate different representations
  advisory_recheck: before implementation review, record changed-file count, line delta, production surfaces, ownership boundaries, specialist lenses, and whether coordinator compaction occurred; stop for a reviewed smaller alternative if the boundary becomes clearly oversized
```

The slice count is a semantic output. No numeric threshold is a hard limit and
no filler slice may be added.

## Execution Ledger

No pending or active implementation slices remain. Slice 1 is archived in
`completed-slices.md` with its exact candidate and canonical commits, strict
execution receipts, validation, installation, acceptance, and review evidence.

## Slice 1 Commit Receipt

```yaml
slice: 1
candidate_commit: 8a9331947ffc8b0b28b8c75ecf6fc60f8b3c2fcd
candidate_subject: "feat(plan-batch): decouple slice shape from risk"
canonical_policy_commit: f5cb753b86f64c2a5ee351c68473540ead82da01
canonical_policy_subject: "docs(ccfg-26): add slice-shape policy config"
status: committed
implementation_range: a0835f146857612dcd5a95053d67c53f32449012..8a9331947ffc8b0b28b8c75ecf6fc60f8b3c2fcd
candidate_diff_sha256: c87ed3577880e564d668f11995a00b8e89bc23b298b1b9e87b52a1985ae75915
canonical_diff_sha256: 5147efa0b292eebf600cc8478177f0b56bb0ff5e7cc5104f27959349a2a77a24
files_changed:
  candidate: 20
  canonical: 2
line_delta:
  candidate: "+1237/-209"
  canonical: "+5/-0"
validation: "191 focused tests and 183 subtests; manifest 2 tests and 28 subtests; 82-scenario catalog; Ruff, production BasedPyright, Planning State, and range diff checks green; exact two known-red CCFG-26 assertions unchanged"
review: "final exact-range delta-only test-quality and runway reviews clean"
installation: "fresh temporary and isolated candidate homes converged; stable-home status SHA-256 unchanged"
acceptance: "one pytest process; 25 tests; 82 scenarios; 31 required contracts; 17 families green"
convergence:
  phase: closure
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: same-batch CCFG-26 closeout reconciliation
```

## Orchestration Anomalies

```yaml
orchestration_anomalies:
  - slice: 1
    severity: medium
    category: premature_reviewer_lease_handoff
    observed: The coordinator sent one delta-only re-review handoff before calling the mandatory later-handoff lease refresh.
    impact: The reviewer was interrupted before its result was accepted; no files, commits, or repository revisions moved.
    action_taken: The reviewer was stopped, the strict lease and empty read-only scope were refreshed and validated, and the review was restarted from the unchanged diff.
    follow_up: Resolved in this batch; all accepted later reviews carry freshly prepared exact leases.
```

## Completed Slice Archive

Slice 1 is archived in `completed-slices.md`. The execution ledger retains no
completed implementation chronology and no pending or active row.

## Slice 1 — Resolve And Enforce The Project Slice-Shape Policy End To End

### Shape And Vertical Ownership Evidence

```yaml
risk: contract-narrowing
shape:
  selected: vertical
  override_reason: null
vertical_slice:
  starting_scenario: candidate plan-batch receives one selected finding and an active-program reference to slice-shape-policy/v1
  durable_result: the queued planning-runway/v1 artifact persists every slice's policy-consistent shape while migration evidence remains independent and complete
  owner_before: duplicated risk migration predicate across plan-batch, batch_planner, batch_plan_reviewer, scripts/plan_batch.py, and planning-runway/v1
  owner_after: one project-owned slice-shape-policy/v1 resolved by plan-batch and consumed identically by authoring, independent review, deterministic validation, and artifact validation
  migrated_callers:
    - skills/plan-batch/SKILL.md policy resolution and generated-plan gate
    - agents/batch_planner.toml shape authoring
    - agents/batch_plan_reviewer.toml independent policy and shape review
    - scripts/plan_batch.py deterministic request, evidence, and queue validation
    - planning-runway/v1 current artifact schema and fixtures
    - command-owner scenario adapters and exact acceptance catalog
  focused_validation:
    - focused plan-batch, schema, agent, manifest, and behavioral-scenario tests
    - command-owner scenario catalog validation
    - delta-only test-quality review
    - independent exact-diff implementation review
  independently_usable_state: candidate planning behavior can queue vertical defaults and justified horizontal overrides while preserving migration evidence, ready for later integration without making the candidate authoritative now
  rollback_boundary: revert the one focused candidate commit and paired canonical policy/reference change; stable default generation and CCFG-26 child selection remain unchanged
  temporary_residue:
    - stable CCFG-34 policy and root hook remain until CCFG-29
    - candidate generation remains non-authoritative for canonical planning until CCFG-29
    - work-batch execution ownership remains with CCFG-26B through CCFG-26E
```

### Migration Matrix

```yaml
migration_matrix:
  project_policy_resolution:
    current_owner: accepted issue #66 direction plus temporary stable repository policy
    future_owner: active-program reference to project-owned slice-shape-policy/v1 consumed by integrated plan-batch
    reason: project-specific defaults must remain outside reusable workflow code while one exact resolved value reaches every planning owner
    status: pending
    removal_slice_or_condition: Slice 1 focused and final policy-resolution proof is green
  planner_authoring:
    current_owner: batch_planner risk migration predicate plus vertical_slice authoring
    future_owner: batch_planner policy-selected shape authoring plus independent migration_evidence
    reason: the author must persist shape for every slice without deriving it from mutation risk
    status: pending
    removal_slice_or_condition: Slice 1 focused registered-agent and plan-batch tests are green
  independent_review:
    current_owner: batch_plan_reviewer risk migration vertical-contract check
    future_owner: batch_plan_reviewer policy-consistency and architectural override judgment plus independent migration-evidence review
    reason: the reviewer must receive the same resolved policy yet retain independent judgment over horizontal justification
    status: pending
    removal_slice_or_condition: Slice 1 focused registered-agent and exact-diff reviews are green
  deterministic_queue_gate:
    current_owner: scripts/plan_batch.py hard-coded migration shape predicate
    future_owner: scripts/plan_batch.py exact resolved-policy consistency checks with no architectural persuasion judgment
    reason: DEC-038 must fail closed when persisted shape conflicts with policy without duplicating reviewer judgment
    status: pending
    removal_slice_or_condition: Slice 1 focused deterministic and exact acceptance gates are green
  planning_runway_artifact:
    current_owner: planning-runway/v1 risk-gated vertical_slice plus migration_matrix representation
    future_owner: planning-runway/v1 required per-slice shape plus independently risk-gated migration_evidence with the complete retained field set and coexistence-consistent migration_matrix
    reason: the durable artifact must expose shape directly and preserve migration protection without semantic contradiction
    status: pending
    removal_slice_or_condition: Slice 1 schema, fixture, and artifact validation is green
  stable_temporary_policy:
    current_owner: root AGENTS.md plus stable-runway dogfooding policy
    future_owner: integrated candidate plan-batch consuming the project-owned policy
    reason: stable agents still need the temporary planning rule until candidate parity and integration are proven
    status: pending
    removal_slice_or_condition: CCFG-29 candidate parity, integration, and policy-removal gate
  execution_ownership:
    current_owner: existing stable work-batch, Batch Runway, and Architecture Program Runway contracts
    future_owner: CCFG-26B through CCFG-26E fresh execution, recovery, finalization, and closeout flights
    reason: this correction is planning-only preparation and must not absorb issue #59 or #61 behavior
    status: pending
    removal_slice_or_condition: final CCFG-26 closeout after CCFG-26B through CCFG-26E
```

Every retained route has a caller or scenario, current owner, future owner,
reason, status, and removal condition. No silent fallback is authorized.

### Scope

- Add the four-field project-owned policy instance and active-program reference.
- Make `plan-batch` resolve one exact policy and pass it unchanged through the
  planner, reviewer evidence, deterministic request, and schema validation.
- Require every new runway slice to persist `shape.selected` and
  `shape.override_reason`.
- Accept the vertical default for migration and non-migration work.
- Accept a horizontal override only when policy allows it and a required reason
  is non-empty; reject disabled, absent, or blank reasons mechanically.
- Keep persuasiveness of the reason in independent planning review.
- Rename and preserve the migration-specific evidence extension beside shape,
  conditional only on `risk: migration`.
- Replace the current artifact representation directly and add no historical
  compatibility.
- Update focused fixtures, scenarios, installed feature metadata, and changelog
  only as required by the changed owners.

### Allowed Files

Only the required and conditional paths under the Write-Path Ceiling.

### Non-Goals

- No execution, recovery, finalization, closeout, reconciliation, runner,
  worker, bridge, default-generation, or successor change.
- No second runway dialect, compatibility parser, archived artifact migration,
  auto-classifier, numeric threshold, strategy framework, or policy inheritance.
- No Planning State semantic expansion or project path hard-coded into reusable
  skills.

### Acceptance Criteria

1. A non-migration slice uses the configured vertical default and persists
   `shape.selected: vertical` with a null override reason.
2. A migration slice uses the same shape policy and independently requires
   complete migration evidence and the coexistence-consistent migration matrix.
3. A permitted horizontal override with a non-empty reason is accepted and
   persisted.
4. A horizontal override is rejected when `allow_override` is false.
5. A horizontal override is rejected when a required reason is absent, blank,
   or null.
6. Planner, reviewer, deterministic validation, and artifact validation consume
   one exact resolved policy; any digest, value, or lineage mismatch fails before
   queue mutation.
7. Deterministic validation checks consistency only; independent review judges
   architectural persuasiveness.
8. The old risk-coupled `vertical_slice` representation is absent from current
   candidate owners, schemas, fixtures, and scenarios except historical source
   evidence; no compatibility route accepts it.
9. Completed and archived runways are not modified or migrated.
10. Final-range validation remains a batch gate and no filler implementation
    slice exists.
11. Candidate installed feature versions move together for every changed
    installed surface; stable-home status and default generation remain
    unchanged.
12. CCFG-26A remains completed and CCFG-26B through CCFG-26E remain unselected.

### Focused Validation

Run all current-green baselines, the implementation-created policy/schema
tests, conditional Ruff and BasedPyright, catalog validation, Planning State
validation for the policy reference, and `git diff --check`. Do not run exact-
commit acceptance or installations from the worker.

Because tests change, run delta-only `test-quality-review` after focused tests
are green. Then request a fresh independent `runway_reviewer` on the exact
task-scoped diff.

### Commit

`feat(plan-batch): decouple slice shape from risk`

### Worker Brief

You are the registered `runway_worker` and already the required coding
subagent for Slice 1. Revalidate fresh strict context and exact write scope.
Implement only the project policy/reference and candidate planning correction.
Do not spawn, delegate to, or wait on other agents. Do not edit execution,
recovery, finalization, closeout, reconciliation, runner, bridge, stable-home,
default-generation, or successor surfaces. Do not run installations or exact-
commit project acceptance unless the coordinator explicitly assigns a focused
command.

### Reviewer Brief

Independently review the exact task-scoped diff or commit supplied by the
coordinator and echo `diff_basis` plus verified strict identity. Verify one
resolved policy, per-slice shape persistence, override rules, independent
migration evidence, direct current-schema replacement, exact approval scope,
write-path ceiling, test quality, and absence of execution-owner or historical-
compatibility changes. Do not edit or spawn agents.

### Slice Stop Conditions

- Stop if any consumer receives a different policy value or lineage.
- Stop if the project-owned policy cannot be resolved without hard-coding this
  repository path in a reusable owner or expanding Planning State into a new
  generic configuration owner.
- Stop if migration evidence is weakened or still determines shape.
- Stop if deterministic validation must decide architectural persuasion.
- Stop if a compatibility reader, second dialect, or archived-runway migration
  appears necessary.
- Stop if the candidate cannot enforce the correction without touching
  execution-owner, runner, bridge, or default-generation behavior.
- Stop on a path outside the exact ceiling, unrelated dirt, failed strict
  context, or clearly oversized boundary without a reviewed smaller alternative.
- Stop after the one clean slice commit, receipt, execution-ledger update, and
  completed-slice archive. Do not begin another implementation slice.

## Final Validation

After Slice 1 has a clean focused candidate commit and the canonical policy
instance/reference are durable:

1. refresh the strict lease from this immutable planning snapshot and accepted
   repository movement;
2. rerun all Slice 1 focused gates, conditional Ruff and BasedPyright, Planning
   State `current` and `validate`, catalog validation, and `git diff --check`;
3. prove the exact two later-CCFG-26 known-red failures gained no new failure;
4. install the candidate into a fresh `/tmp` Codex home and the isolated
   candidate home `/home/alacasse/.codex-command-owner-redesign`, then compare
   stable-home status before and after;
5. run exact-commit command-owner acceptance once with fresh outputs:

   ```sh
   ccfg26_shape_acceptance_root="$(mktemp -d /tmp/ccfg-26-shape-acceptance.XXXXXX)"
   COMMAND_OWNER_CANDIDATE_CODEX_HOME=/home/alacasse/.codex-command-owner-redesign \
   PYTHONDONTWRITEBYTECODE=1 \
     .venv/bin/python scripts/command_owner_scenarios.py accept \
     tests/fixtures/command-owner-scenarios \
     --result-output "$ccfg26_shape_acceptance_root/acceptance-result.json" \
     --json-report-output "$ccfg26_shape_acceptance_root/report.json" \
     --text-report-output "$ccfg26_shape_acceptance_root/report.txt"
   ```

6. read the result and text report and record their hashes;
7. run delta-only `test-quality-review` over the final test range;
8. request final independent `runway_reviewer` and only actually triggered
   specialist reviews; and
9. confirm the candidate range and canonical planning changes contain no
   unrelated path, historical compatibility, or successor selection.

All final gates are `required-green`. Final validation is not an implementation
slice.

## Batch Stop Conditions

- Stop on any hard-coded shape default outside the project policy, policy-value
  drift, missing lineage, or failed exact review binding.
- Stop on any execution/closeout owner, recovery advisor, runner protocol,
  bridge, default-generation, physical-deletion, or final-integration change.
- Stop if candidate installation changes the stable home or canonical queue
  state.
- Stop if final acceptance is not bound to the clean exact candidate commit.
- Stop if CCFG-26A is reopened or any CCFG-26 successor is selected or prepared.

## Closeout Contract

Closeout may:

- complete only `ccfg-26-slice-shape-policy-correction` and record its candidate
  commit, canonical policy/reference evidence, focused validation,
  installations, exact acceptance, test-quality review, and independent review;
- return parent CCFG-26 to `Prepared`, not `Closed`;
- record the corrected planning-policy behavior as the required predecessor for
  CCFG-26B;
- clear only this batch's selected, queued, and active state; and
- preserve CCFG-26B through CCFG-26E as unselected candidate batches.

Closeout must not select, dispatch, queue, create, refresh, or prepare CCFG-26B
or any successor. A later explicit stable `plan-batch` invocation owns that
selection.
