# CCFG-26 Work-Batch Owner Transfer Runway

## Execution Status

- Batch ID: `ccfg-26-work-batch-owner-transfer`
- Covered finding: CCFG-26
- Batch state after planning gate: `queued`
- Implementation status: not started
- Active slice: none
- Pending slices: 1 through 4
- Dispatch: `dispatch.md`
- Planning review: `review.md`
- Completed-slice archive: `completed-slices.md`
- Blocked-slice report target: `execution-report.md`
- Closeout target: `closeout.md`
- Successor selection: forbidden

This exact runway becomes executable only after an independent planning review
records a clean verdict in `review.md` and canonical Planning State points to
this runway as the sole queued batch. Planning itself implements no candidate
code.

## Purpose

Transfer execution and closeout ownership from the current broad support owners
to installed `work-batch`, satisfying COR-009 without creating a second runtime
state model or allowing the candidate generation to control its own development
batch.

The result must be one installed command owner that consumes the current queued
or active runway and owns execution through same-batch reconciliation. Narrow
Planning State, Planning Artifacts, planning-contract store, strict cross-
checkout, and registered-agent mechanisms remain mechanisms only.

## Authority

- Canonical CCFG-26 row: `../../LEDGER.md`.
- Accepted COR-009 source:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Single-generation development boundary:
  `../../../../../adr/0004-single-generation-command-owner-development-boundary.md`.
- Live carry-forward:
  `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- Completed slice-shape behavior:
  `../../findings/slice-shape-policy-direction.md` and the correction closeout
  plus post-closeout correction.
- Temporary stable controller policy:
  `../../notes/stable-runway-dogfooding-policy.md`.
- Exact candidate inspection baseline:
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.

Superseded CCFG-26 execution-state and CCFG-26B artifacts are not authority and
must not be resumed, amended, or used to prescribe this implementation.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slice 1: `migration`.
- Slice 2: `migration`.
- Slice 3: `migration`.
- Slice 4: `migration`.
- Shape: `vertical` for every slice under the current project policy.
- Horizontal override: none.

The approval gate is COR-009 plus the canonical `Ready` row and this explicit
`plan-batch CCFG-26` request. It authorizes transfer and removal of displaced
semantic ownership, but no new state model, candidate canonical write, default
generation switch, physical legacy deletion, bridge deletion, or successor
selection.

## Baseline

### Stable controller and canonical planning

- Repository: `/home/alacasse/projects/codex-config`
- Branch: `master`
- Planning-snapshot commit:
  `6b575614983e72456a25875264ebab7e39ea0a72`
- Codex home: `/home/alacasse/.codex`
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`
- Planning State before queue mutation: valid and idle; selected dispatch,
  queued batch, and active runway are `None`.

### Candidate implementation

- Repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Branch: `implementation/command-owner-redesign`
- Planning-snapshot commit:
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`
- Worktree at inspection: clean.

At that candidate commit, `work-batch` routes execution to Batch Runway and
reconciliation to Architecture Program Runway. The fixture catalog already
contains accepted execution, recovery, currentness, closeout, no-successor, and
fault scenarios, but no installed `scripts/work_batch.py` owns them.

### Focused baseline

The following combined candidate command currently reports 70 passed, 16
subtests passed, and one known-red transitional APR wording assertion:

```sh
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_currentness.py \
  tests/test_batch_lifecycle_guards.py \
  tests/test_skill_routing_rule_ownership.py
```

The failing assertion is owned by Slice 4 and must not gate Slices 1 through 3.
No additional failure is accepted.

## Project Values

- Planning Artifact Layout: Planning Artifact Layout v1.
- Planning location: this batch directory.
- Program root: `docs/plans/programs/codex-config`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`; validation outputs use fresh explicit `/tmp`
  directories.
- Output root: `None`; generated acceptance outputs use fresh explicit `/tmp`
  directories.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: candidate
  `scripts/command_owner_scenarios.py validate|accept` with explicit inputs and
  fresh output paths for `accept`.
- Summary artifacts: acceptance result JSON and text report.
- Index/graph refresh: none. Graphify is suspended and must not be invoked.
- Candidate commit strategy: one focused candidate implementation commit after
  each accepted slice.
- Canonical receipt/closeout commits remain separate stable commits. The final
  self-referential closeout may use `this closeout commit`.
- Preserve unrelated dirt and stop on task-scope overlap.

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
  toolchain_commit: 6b575614983e72456a25875264ebab7e39ea0a72
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 6b575614983e72456a25875264ebab7e39ea0a72
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The installed helper validated this payload and exact write scope for eight
canonical planning paths and thirty-two candidate implementation paths before
this runway was created.

Validated canonical planning path ceiling:

```yaml
planning_paths:
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/dispatch.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/runway.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/review.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/completed-slices.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/execution-report.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-work-batch-owner-transfer/closeout.md
```

Validated candidate implementation path ceiling:

```yaml
implementation_paths:
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/work-batch
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/work_batch.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/runway_worker.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/runway_reviewer.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/batch-runway
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/architecture-program-runway
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_phase_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_change_allowance.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/command_owner_scenarios.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/docs/skill-routing-contract.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/docs/workflow-guide.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/README.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/codex-features.json
  - /home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_work_batch.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_behavioral_scenarios.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_scenario_currentness.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_scenario_catalog.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_batch_lifecycle_guards.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codex_features_manifest.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_custom_agent_contracts.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codebase_investigator_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_planning_state_consumer_projection_routing.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_routing_rule_ownership.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_catalog.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_phase_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_change_allowance.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_planning_contract_artifacts.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_planning_state.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/catalog.yaml
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/workflow_adapters.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/currentness_adapters.py
```

This planning snapshot is immutable historical plan-time evidence, not a live
execution lease. Do not edit its revisions after the containing planning
change. Before the first delegated handoff, `work-batch` must confirm this same
selected scope through Planning State and pass the strict ready/blocked
preflight for a fresh live lease. Every later handoff requires a newly prepared
lease and separately validated write scope.

## Target Ownership Boundary

### Command owner

`skills/work-batch/` owns human-facing orchestration and
`scripts/work_batch.py` is the installed deterministic `work-batch/v1` boundary.
Together they own the COR-009 decisions. Later slices must extend that same owner
and must not create a second executor, recovery engine, finalizer, closeout
owner, or reconciliation owner.

### Mechanisms

- Planning State supplies semantic currentness diagnostics.
- Planning Artifacts supplies placement and vocabulary.
- `scripts/planning_contract.py` supplies existing lineage-bound artifact and
  CAS store mechanisms.
- Strict cross-checkout helpers supply mechanical identity, lease, and scope
  validation only.
- Registered worker/reviewer TOMLs own exact result schemas and remain separate
  delegated roles.

Mechanisms do not decide proceed, stop, recovery, validation acceptance, review
acceptance, commits, closeout disposition, reconciliation, or successors.

### Development controller boundary

The stable generation uses its current Batch Runway execution contract to build
and close this real batch. That is development bookkeeping under ADR 0004, not a
candidate product dependency. The candidate `work-batch` owner is exercised
only against fixtures, temporary planning roots, and isolated candidate
installation until cutover. It must not control or close its own implementation
batch in canonical stable planning.

## Batch Scope

Included:

- one installed `work-batch/v1` owner;
- current queued/active runway consumption;
- clean execution, recovery/resume, validation/review, commit/receipt,
  finalization, closeout, reconciliation, and no-successor behavior;
- currentness, strict lease, write-scope, exact diff/review basis, movement, and
  receipt guards already required by CCFG-23/30/31/32 behavior;
- old-format active-state refusal or explicit stable-completion boundary;
- worker/reviewer result contracts independent of Batch Runway paths;
- installed dependency and caller migration away from displaced owners;
- runner compatibility in which serialized `execute` invokes one complete
  public `work-batch` flight and serialized `closeout` observes that result;
- focused docs, metadata, tests, fixtures, candidate install, and exact
  acceptance.

Deferred and preserved:

- CCFG-27 runner public phase-model migration/removal and candidate cutover
  rehearsal;
- CCFG-28 physical APR/Batch Runway source deletion and default switch;
- CCFG-29 bridge deletion, final integration, and temporary-policy removal;
- read-only historical active-state vocabulary until its explicit migration or
  zero-live-state deletion condition;
- `runway_worker` / `runway_reviewer` names when they remain registered role
  identities; their contracts may not retain Batch Runway path dependencies;
- telemetry and coordinator-compaction policy questions.

## Batch Non-Goals

- No production `execution-state.json`, run database, canonical Batch Execution
  State, reservation, flight, attempt, or new lifecycle protocol.
- No cross-generation runtime imports, invocations, synchronization, or shared
  state.
- No Planning State semantic changes or Git-derived queue currentness.
- No new public command, planning schema family, queue transaction, closeout
  schema, compatibility dialect, or store.
- No candidate canonical planning write or self-hosting.
- No CCFG-27 through CCFG-29 implementation, deletion, cutover, integration, or
  successor preparation.
- No physical deletion of historical APR/Batch Runway source directories.
- No Graphify use or generated graph authority.

## Execution Contract

Use Batch Runway Standard Execution Contract v2 for the stable controlling
generation that executes this development batch.
Use Batch Runway Registered Agent Result Contract v2; registered agent TOMLs
own their exact result schemas.
Use Batch Runway Compact Report Contract v1 only for stable coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status and
receipt summaries.
Use Batch Runway Orchestration Anomaly Log v1 only for suspicious coordinator
or subagent-lifecycle behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine stable-controller slice
execution.

References:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`

Overrides:

- The stable controller may consume the current temporary vertical-planning and
  bounded-recovery policy but must not restore the removed one-slice-per-
  invocation requirement.
- Candidate target code must not treat these stable Batch Runway references as
  permanent `work-batch` product dependencies. Each slice removes the target
  dependency it replaces.
- The stable controller alone writes canonical execution receipts and same-
  batch closeout for this real development batch.

## Slice Shape

```yaml
slice_shape:
  selected: vertical
  override_reason: null
  rationale:
    1_to_2: >-
      Slice 1 leaves a clean accepted-slice path independently usable; Slice 2
      adds distinct recovery/currentness risk against that stable owner.
    2_to_3: >-
      Slice 2 leaves normal and interrupted slices committed with durable
      evidence; Slice 3 consumes that evidence at the separate finalization and
      closeout-production boundary.
    3_to_4: >-
      Slice 3 produces a complete closeout while APR still reconciles it; Slice
      4 transfers the different canonical-current/ledger mutation boundary and
      removes normal legacy callers.
  final_validation_is_slice: false
```

## Migration Matrix

```yaml
migration_matrix:
  accepted_slice_execution:
    current_owner: batch-runway
    future_owner: work-batch
    status: pending
    removal_slice_or_condition: Slice 1 accepted commit
  worker_reviewer_result_path_dependency:
    current_owner: batch-runway references
    future_owner: registered agents plus work-batch
    status: pending
    removal_slice_or_condition: Slice 1 accepted commit
  recovery_and_resume:
    current_owner: batch-runway
    future_owner: work-batch
    status: pending
    removal_slice_or_condition: Slice 2 accepted commit
  execution_currentness_and_handoff_acceptance:
    current_owner: batch-runway coordinator
    future_owner: work-batch using strict mechanical helpers
    status: pending
    removal_slice_or_condition: Slice 2 accepted commit
  finalization_and_closeout_production:
    current_owner: batch-runway
    future_owner: work-batch using planning-closeout/v1 mechanisms
    status: pending
    removal_slice_or_condition: Slice 3 accepted commit
  same_batch_program_reconciliation:
    current_owner: architecture-program-runway
    future_owner: work-batch using planning-contract CAS mechanisms
    status: pending
    removal_slice_or_condition: Slice 4 accepted commit
  local_runner_execute_route:
    current_owner: serialized batch-runway execute-spec phase route
    future_owner: serialized execute phase invoking one complete work-batch flight
    status: pending
    removal_slice_or_condition: Slice 4 accepted commit
  local_runner_closeout_route:
    current_owner: serialized APR closeout-runway phase route
    future_owner: observation-only compatibility phase after work-batch reconciliation
    status: pending
    removal_slice_or_condition: Slice 4 accepted commit; phase-model removal remains CCFG-27
  physical_legacy_source_directories:
    current_owner: retained candidate source
    future_owner: none
    status: pending
    removal_slice_or_condition: CCFG-28 physical deletion after CCFG-27 rehearsal
  cross_checkout_bridge:
    current_owner: temporary development-integrity helper
    future_owner: none
    status: pending
    removal_slice_or_condition: CCFG-29 final integration
```

Every retained route must keep the caller, reason, future owner, and removal
condition visible. No silent fallback is allowed.

## Validation Contract

### Required-green current baseline

```yaml
focused_validation:
  - command: >-
      .venv/bin/python -B -m pytest -q -p no:cacheprovider
      tests/test_command_owner_behavioral_scenarios.py::test_execution_review_commit_and_resume_are_observable_fixture_effects
      tests/test_command_owner_behavioral_scenarios.py::test_execution_state_machine_rejects_gate_receipt_scope_and_resume_regressions
    status: required-green
  - command: >-
      .venv/bin/python -B -m pytest -q -p no:cacheprovider
      tests/test_command_owner_scenario_currentness.py::test_protected_handoff_binds_lease_scope_receipt_and_reviewer_base
      tests/test_command_owner_scenario_currentness.py::test_worker_lease_cannot_be_reused_for_reviewer_handoff
    status: required-green
  - command: >-
      .venv/bin/python -B -m pytest -q -p no:cacheprovider
      tests/test_planning_contract_artifacts.py tests/test_planning_state.py -k closeout
    status: required-green
  - command: >-
      .venv/bin/python -B scripts/command_owner_scenarios.py validate
      tests/fixtures/command-owner-scenarios
    status: required-green
```

### Implementation-created gate

```yaml
- command: >-
    .venv/bin/python -B -m pytest -q -p no:cacheprovider
    tests/test_work_batch.py
  status: implementation-created
  owner_slice: Slice 1 creates the installed-owner contract tests
```

### Known-red baseline and promotion

```yaml
- command: >-
    .venv/bin/python -B -m pytest -q -p no:cacheprovider
    tests/test_command_owner_behavioral_scenarios.py
    tests/test_command_owner_scenario_currentness.py
    tests/test_batch_lifecycle_guards.py
    tests/test_skill_routing_rule_ownership.py
  status: known-red-baseline
  exact_failure: >-
    tests/test_batch_lifecycle_guards.py::BatchLifecycleGuardTests::test_architecture_program_closeout_rejects_dispatch_runway_only_evidence
  promotion_owner: Slice 4 replaces the transitional APR-topology assertion and makes the command required-green
```

### Conditional checks

- Ruff on exact changed Python/TOML-aware test surfaces: `conditional`; run when
  Python or test files change.
- Configured production BasedPyright: `conditional`; run when production Python
  changes and preserve any declared unresolved-source baseline exactly.
- Candidate manifest/catalog tests: `conditional`; run in every slice that
  changes features, links, agent contracts, scenarios, or routing.
- `git diff --check`: `required-green` for every slice and final candidate/stable
  planning ranges.
- Delta-only `test-quality-review`: `conditional`; run after each slice that
  changes or adds tests.

Workers run only focused slice tests assigned below. The stable coordinator owns
the broader focused command, scenario catalog validation, independent review,
commits, installation, exact acceptance, and final validation.

## Execution Ledger

| Slice | State | Candidate commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|
| 1. Accepted-slice execution owner | pending | None | pending | pending | Establish installed clean path |
| 2. Recovery and currentness | pending | None | pending | pending | Extend same owner; no new state |
| 3. Finalization and closeout production | pending | None | pending | pending | Produce lineage-bound closeout |
| 4. Reconciliation and caller cutover | pending | None | pending | pending | Remove normal legacy dependencies; no successor |

Move completed details to `completed-slices.md`; keep this table compact.

## Slice 1: Accepted-Slice Execution Through Installed Work-Batch

### Risk And Vertical Contract

```yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
vertical_slice:
  starting_scenario: A valid queued runway has one clean implementation slice ready.
  durable_result: Installed work-batch owns the slice through validated, independently reviewed commit receipt.
  owner_before: batch-runway execute-spec and its execution references
  owner_after: skills/work-batch plus installed scripts/work_batch.py work-batch/v1 boundary
  migrated_callers:
    - public work-batch clean execution route
    - execution-validated-reviewed-committed target scenario
    - runway_worker and runway_reviewer result-contract path selection
  focused_validation:
    - tests/test_work_batch.py clean-path contract
    - execution review/commit behavioral scenarios
    - exact registered-agent and manifest assertions
  independently_usable_state: Normal clean slices execute without loading Batch Runway semantics.
  rollback_boundary: Revert the Slice 1 candidate commit and restore the prior clean-path route.
  temporary_residue:
    - Batch Runway recovery and finalization remain until Slices 2 and 3.
    - APR reconciliation remains until Slice 4.
  ownership_coexistence: Explicit clean-path migration only; no fallback or dual decision is allowed.
```

### Scope

Primary candidate surfaces:

- `skills/work-batch/**`
- new `scripts/work_batch.py`
- `agents/runway_worker.toml`
- `agents/runway_reviewer.toml`
- `codex-features.json`
- focused execution scenario adapters/catalog and exact tests
- directly associated docs/metadata/changelog

Batch Runway files may change only to remove or redirect the exact clean-path
ownership transferred here. Recovery and finalization content must remain
available for later slices without acting as a silent clean-path fallback.

### Work

1. Define one installed `work-batch/v1` deterministic boundary in
   `scripts/work_batch.py`. The skill remains the orchestration owner; the
   script validates the command-owner inputs/results and applies already-made
   decisions through narrow mechanisms.
2. Consume Planning State `current` and `validate` facts before execution and
   bind exactly one queued/active runway and next incomplete slice.
3. Directly coordinate a separate worker, focused validation acceptance, and a
   separate reviewer with exact diff basis; accept only a complete matching
   commit receipt.
4. Keep agent TOMLs as exact result-schema owners but remove Batch Runway naming
   and v1 path dependencies from the target contracts. Role names may remain.
5. Rebind the clean execution target scenario to the installed owner, not a
   fixture-only executor.
6. Install/link the new owner through the `work-batch` feature without switching
   the default generation or mutating the stable Codex home.

### Acceptance

- One installed owner controls the clean slice path.
- Planning State is the semantic currentness gate.
- Worker and reviewer are independent and exact result/diff bases are checked.
- Validation acceptance and commit receipt decisions belong to `work-batch`.
- The target scenario proves the installed owner, not Batch Runway or fixture
  topology.
- Worker/reviewer contracts contain no Batch Runway result-contract path.
- No recovery, finalization, closeout, reconciliation, state-store, bridge, or
  successor behavior is invented or weakened.

### Smaller-Alternative Analysis

Splitting the installed boundary, agent-contract path migration, and clean
scenario binding would leave either an uninstalled owner, a result contract with
no consumer, or a fixture claim with no production path. None is independently
usable or rollback-safer than this one clean-path commit.

### Focused Validation

- Implementation-created `tests/test_work_batch.py` clean-path tests become
  `required-green` in this slice.
- Required-green execution review/commit scenario nodes.
- Required-green registered-agent and work-batch manifest assertions.
- Required-green scenario catalog validation and `git diff --check`.
- Conditional Ruff, BasedPyright, and delta-only test-quality review.

### Commit Message

`feat(work-batch): own accepted slice execution`

### Worker Brief

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 1 in the candidate checkout from a fresh strict lease. Do not spawn,
delegate, or wait on additional agents. Do not run project-level acceptance,
installations, final validation, or canonical planning writes. Preserve the
later recovery/finalization/reconciliation rows explicitly.

### Reviewer Brief

Independently review the exact task-scoped diff or candidate commit. Verify the
installed owner is behaviorally real, agent roles remain independent, no Batch
Runway result path survives, temporary ownership is explicit, and no later
slice or state model leaked into the diff. Echo the exact `diff_basis` and fresh
verified strict context.

### Stop Conditions

- Stop if a second executor or new persistent state is required.
- Stop if clean execution still invokes Batch Runway semantics.
- Stop if agent contracts cannot lose Batch Runway paths without changing their
  exact v2 schema or adding another role.
- Stop if any runner, APR reconciliation, finalization, or canonical planning
  mutation is needed in this slice.

## Slice 2: Recovery, Currentness, And Legacy-State Refusal

### Risk And Vertical Contract

```yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
vertical_slice:
  starting_scenario: The current work-batch slice is interrupted or fails validation/review before acceptance.
  durable_result: Work-batch owns fail-closed recovery and resumes the same incomplete slice from durable evidence.
  owner_before: batch-runway recovery and coordinator currentness procedures
  owner_after: the same installed work-batch/v1 owner using Planning State and strict mechanical helpers
  migrated_callers:
    - validation-failure correction loop
    - review-finding correction loop
    - missing or stale receipt handling
    - strict first and later handoff lease paths
    - same-slice resume after interruption
  focused_validation:
    - execution recovery/resume behavioral scenarios
    - execution-currentness fault scenarios
    - legacy active-state refusal
  independently_usable_state: Clean and interrupted slices are owned end to end by work-batch.
  rollback_boundary: Revert Slice 2 while retaining the accepted Slice 1 clean path.
  temporary_residue:
    - Batch Runway finalization remains until Slice 3.
    - APR reconciliation remains until Slice 4.
  ownership_coexistence: Clean path is fully migrated; only the named finalization and reconciliation rows remain.
```

### Scope

- `skills/work-batch/**`
- `scripts/work_batch.py`
- exact migrated recovery/currentness references under `skills/batch-runway/**`
- worker/reviewer TOMLs only if recovery result validation needs their existing
  exact fields clarified
- currentness and behavioral scenario adapters/catalog/tests
- focused manifest/routing/docs metadata

`scripts/cross_checkout_context.py`, `scripts/planning_state.py`, runner modules,
planning contracts, and schemas are read-only in this slice.

### Work

1. Move proceed/stop, validation/review correction, recovery, resume, and exact
   result acceptance to the existing `work-batch/v1` owner.
2. Require Planning State current/validate success before the first helper call.
3. Preserve strict first-handoff implementation-baseline validation, fresh
   later leases, separate worker/reviewer leases, exact write scope, result echo,
   receipt, commit range, and review basis.
4. Treat unexpected implementation movement, movement during lease preparation,
   wrong roots/generation, stale/missing receipts, unrelated commit content, and
   unexpected workspace writes as fail-closed blockers.
5. Encode the old-format policy: stable completes already-live legacy state or a
   later explicit migration owns it; candidate `work-batch` may read and report
   but must not silently mutate old active state.
6. Remove the displaced Batch Runway recovery owner for migrated callers without
   introducing fallback or duplicate decision logic.

### Acceptance

- Recovery decisions and same-slice resume belong to `work-batch`.
- Planning State, not Git, decides semantic currentness.
- Git remains exact material-integrity evidence only.
- Fresh leases, write scopes, receipts, review bases, and accepted movement are
  preserved.
- Legacy active state is completed by stable or blocks for explicit migration;
  candidate does not silently rewrite it.
- No canonical execution state, reservation, attempt, flight, process boundary,
  or automatic cross-generation continuation is added.

### Smaller-Alternative Analysis

Splitting recovery from currentness would let one half accept an action without
the other's exact pickup, lease, receipt, and review-basis guarantees. Both are
the same interrupted-slice scenario and share one owner, validation, and
rollback boundary.

### Focused Validation

- Required-green recovery/resume scenario nodes.
- Required-green currentness protected-handoff and fault scenarios.
- Required-green new `tests/test_work_batch.py` recovery/legacy-state tests.
- Required-green scenario catalog validation and `git diff --check`.
- Conditional Ruff, BasedPyright, manifest tests, and delta-only test-quality
  review.

### Commit Message

`feat(work-batch): own recovery and currentness`

### Worker Brief

Extend only the Slice 1 owner. Do not create a sibling recovery engine or state
file. Use the existing Planning State and strict helper contracts as mechanisms.
Do not spawn agents, run final acceptance/installations, edit canonical
planning, or touch runner/closeout reconciliation surfaces.

### Reviewer Brief

Review every recovery branch and fail-closed condition against the exact diff.
Verify that lifecycle currentness remains Planning State-owned, Git is limited
to integrity, old-format state is not silently mutated, and all migrated paths
converge on the same `work-batch/v1` owner without fallback.

### Stop Conditions

- Stop if recovery needs a new state file, database, schema, reservation, flight,
  or cross-generation communication.
- Stop if helper mechanics acquire proceed/recovery authority.
- Stop if an accepted error path can skip exact reviewer basis, commit receipt,
  or implementation-baseline validation.
- Stop if finalization, APR reconciliation, or runner routing must change here.

## Slice 3: Final Validation And Durable Closeout Production

### Risk And Vertical Contract

```yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
vertical_slice:
  starting_scenario: The last implementation slice is accepted with complete commit and completed-slice evidence.
  durable_result: Work-batch runs final gates and produces one lineage-bound planning-closeout/v1 artifact.
  owner_before: batch-runway finalization, ledger retention, reporting, and closeout production
  owner_after: the same installed work-batch/v1 owner using existing planning-contract mechanisms
  migrated_callers:
    - final relevant validation
    - final review and convergence reporting
    - completed-slice and cleanup-residue checks
    - closeout artifact creation and exact replay recovery
  focused_validation:
    - planning-closeout/v1 artifact tests
    - closeout fault/replay scenarios
    - placeholder and cleanup-residue guards
  independently_usable_state: Work-batch executes a whole runway and produces complete closeout evidence.
  rollback_boundary: Revert Slice 3 while retaining per-slice execution and recovery from Slices 1 and 2.
  temporary_residue:
    - APR applies same-batch reconciliation until Slice 4.
  ownership_coexistence: Closeout production is migrated; APR is restricted to the one named apply boundary.
```

### Scope

- `skills/work-batch/**`
- `scripts/work_batch.py`
- exact finalization/reporting/ledger-retention references under
  `skills/batch-runway/**`
- `scripts/planning_contract.py` read-only mechanism
- `scripts/planning_state.py` read-only evidence mechanism
- planning-contract, closeout, lifecycle, and work-batch focused tests
- associated manifest/routing/docs metadata

No runner phase, APR reconciliation, Planning State semantic, planning schema,
or canonical program-state mutation changes are allowed here.

### Work

1. Move final relevant validation selection/acceptance, required final review,
   cleanup residue checks, completed-slice retention, compact reporting, and
   convergence decisions to `work-batch`.
2. Produce `planning-closeout/v1` through the existing lineage-bound
   `write_closeout_artifact` mechanism and use existing receipt/idempotency facts
   for exact replay after partial write.
3. Require complete slice commits, validation, independent reviews, receipts,
   final gates, and no unresolved placeholders before closeout success.
4. Preserve compact evidence for same-batch reconciliation without performing
   that reconciliation yet.
5. Remove displaced Batch Runway finalization/closeout-production ownership for
   migrated callers.

### Acceptance

- `work-batch` owns final validation and acceptance, final review coordination,
  finalization, cleanup residue, completed-slice evidence, and closeout creation.
- The closeout uses existing `planning-closeout/v1` lineage and store mechanics;
  no second schema/store/state exists.
- Partial closeout writes recover by exact replay and reject foreign batch
  identity.
- Closeout evidence is complete enough for reconciliation and selects no
  successor.
- APR is temporarily limited to applying same-batch program reconciliation.

### Smaller-Alternative Analysis

Final validation alone is not an implementation slice, and closeout production
without accepted final gates is unusable. Keeping those steps in one
last-slice-to-closeout scenario produces the smallest valid durable boundary.

### Focused Validation

- Required-green planning-contract closeout artifact tests.
- Required-green `tests/test_planning_state.py -k closeout` evidence checks.
- Required-green closeout exact-replay, foreign-batch, and no-placeholder tests.
- Required-green scenario catalog validation and `git diff --check`.
- Conditional Ruff, BasedPyright, manifest tests, and delta-only test-quality
  review.

### Commit Message

`feat(work-batch): own finalization and closeout production`

### Worker Brief

Extend the existing `work-batch/v1` owner from accepted last slice to durable
closeout evidence. Use planning-contract and Planning State functions only as
mechanisms. Do not mutate canonical CURRENT/LEDGER, change runner phases, remove
APR reconciliation, run final project acceptance/installations, or spawn agents.

### Reviewer Brief

Verify closeout lineage, completeness, exact replay, foreign-batch refusal,
placeholder cleanup, final validation/review gates, and no-successor behavior.
Reject any new execution state or any reconciliation decision leaking into APR
or a generic mechanism.

### Stop Conditions

- Stop if existing planning-closeout/store mechanisms cannot satisfy the
  behavior without semantic changes or a new schema/state surface.
- Stop if closeout can succeed with incomplete slice validation/review/receipt
  evidence or unresolved placeholders.
- Stop if canonical reconciliation, runner routing, physical legacy deletion,
  or successor preparation begins in this slice.

## Slice 4: Same-Batch Reconciliation And Caller Cutover

### Risk And Vertical Contract

```yaml
risk: migration
shape:
  selected: vertical
  override_reason: null
vertical_slice:
  starting_scenario: A complete lineage-bound closeout exists for the currently queued/active batch.
  durable_result: Work-batch reconciles that batch atomically, returns idle state, and stops without a successor.
  owner_before: architecture-program-runway closeout-runway plus Batch Runway/APR installed routes
  owner_after: work-batch using planning-contract CAS mechanisms
  migrated_callers:
    - program CURRENT and LEDGER same-batch mutation decisions
    - partial reconciliation exact replay
    - public workflow and routing docs
    - installed work-batch feature dependencies
    - local runner execute and closeout compatibility routes
  focused_validation:
    - same-batch closeout and partial-reconciliation scenarios
    - manifest and routing owner tests
    - runner phase-contract and change-allowance tests
    - full focused COR-009 owner suite
  independently_usable_state: Public work-batch owns execution through reconciled idle state and no successor.
  rollback_boundary: Revert Slice 4 to the Slice 3 checkpoint where complete closeout exists and APR still applies reconciliation.
  temporary_residue:
    - Physical APR and Batch Runway source remains for CCFG-28 deletion.
    - Fixed serialized runner phase model remains for CCFG-27 migration.
    - Strict cross-checkout bridge remains for CCFG-29 deletion.
  ownership_coexistence: none for CCFG-26 semantics after the accepted Slice 4 commit
```

### Scope

- `skills/work-batch/**`
- `scripts/work_batch.py`
- exact reconciliation ownership under `skills/architecture-program-runway/**`
- exact remaining execution ownership under `skills/batch-runway/**`
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_change_allowance.py`
- `codex-features.json`
- `docs/skill-routing-contract.md`, `docs/workflow-guide.md`, `README.md`, and
  associated changelog
- exact work-batch, lifecycle, manifest, routing, runner, Planning State
  consumer, agent-contract, scenario catalog, and fixture tests in the planning
  snapshot ceiling

Runner state, transition, validation, command, environment, and facade modules
remain read-only. Their fixed phase identities and APR-hosted reference files
remain explicit CCFG-27/28 residue.

### Work

1. Move closeout disposition, CURRENT/LEDGER mutation decisions, partial
   reconciliation recovery, exact replay, finding disposition, and no-successor
   enforcement to `work-batch`.
2. Use existing `apply_current_document` and `apply_ledger_decision` only as CAS
   mechanisms; do not move decision authority into the store.
3. Require one complete closeout for the same current batch and reject dispatch/
   runway-only evidence, foreign identity, partial evidence, or ambiguous state.
4. Remove `work-batch` installation dependencies on Batch Runway and
   Architecture Program Runway and update registered contract/routing/manifest
   tests to the target owner.
5. Rebind the local runner's serialized `execute` phase to one complete public
   `work-batch` flight. Make serialized `closeout` observation-only over the
   already reconciled result, mirroring CCFG-25's planning compatibility pattern.
6. Narrowly extend execute-phase change allowance to the exact transaction-owned
   CURRENT, LEDGER, closeout, completed-slice, and receipt paths. Do not allow the
   whole planning root or arbitrary Markdown.
7. Demote retained legacy source to explicit CCFG-27/28 residue with no normal
   `work-batch` caller or semantic ownership.

### Acceptance

- `work-batch` is the sole CCFG-26 semantic owner from pickup through same-batch
  reconciliation.
- Planning State shows the just-completed batch reconciled and no selected,
  queued, or active successor.
- Partial reconciliation resumes idempotently from the existing closeout and
  receipts.
- `work-batch` has no Batch Runway or APR feature dependency.
- Agent contracts have no Batch Runway path dependency.
- Runner `execute` invokes one complete `work-batch` flight and runner
  `closeout` only observes; fixed phase identities remain for CCFG-27.
- Target behavior tests do not require old owner paths or exact prompt prose.
- Physical legacy source, phase-model migration, bridge removal, and final
  integration remain with CCFG-27 through CCFG-29.

### Smaller-Alternative Analysis

Separating reconciliation from caller cutover would leave APR as a normal
semantic caller after `work-batch` claimed sole ownership. The program mutation,
installed dependency removal, and bounded runner compatibility route are one
observable same-batch-no-successor scenario and one rollback boundary.

### Focused Validation

- Promote the combined known-red command to `required-green` with zero failures.
- Required-green `tests/test_work_batch.py` full owner suite.
- Required-green manifest, routing, agent-contract, runner phase-contract,
  change-allowance, scenario catalog, Planning State consumer, and closeout
  tests listed by the exact changed-path impact.
- Required-green `scripts/command_owner_scenarios.py validate`.
- Required-green `git diff --check`.
- Conditional Ruff, BasedPyright, and delta-only test-quality review.

### Commit Message

`feat(work-batch): own same-batch reconciliation`

### Worker Brief

Complete only the ownership/reconciliation and caller cutover from the accepted
Slice 3 checkpoint. Preserve fixed runner phase identities and physical legacy
source. Do not widen change allowance to arbitrary planning paths, switch the
default generation, mutate canonical stable planning, select a successor, run
final acceptance/installations, or spawn agents.

### Reviewer Brief

Independently verify sole ownership, exact reconciliation evidence, atomic/idempotent
mutation decisions, runner compatibility, narrow change allowance, removal of
normal legacy dependencies, no successor, and explicit CCFG-27/28/29 residue.
Require the exact candidate commit/diff basis and fresh strict context.

### Stop Conditions

- Stop if reconciliation requires new planning-store or Planning State semantics.
- Stop if the runner phase model, state, transition graph, or public protocol
  must change rather than receive the bounded compatibility rebind.
- Stop if the old owners remain required by installed `work-batch` or any normal
  caller.
- Stop if change allowance broadens to the full planning root or unrelated files.
- Stop if physical deletion, default switch, bridge removal, candidate canonical
  writes, or successor selection begins.

## Final Validation

After all four slices have clean focused candidate commits:

1. Re-run every focused command in this runway and require the former known-red
   combined command to be green.
2. Run all exact affected manifest, routing, agent-contract, planning-contract,
   Planning State, runner compatibility, scenario catalog, and work-batch tests.
3. Run Ruff on exact changed Python/test files and configured production
   BasedPyright, preserving no new warning or error.
4. Run `git diff --check` over the exact candidate implementation range and
   stable planning/receipt range.
5. Run delta-only `test-quality-review` for the complete changed test range.
6. Install the exact candidate commit into a fresh `/tmp` Codex home and the
   isolated candidate home `/home/alacasse/.codex-command-owner-redesign`;
   require every post-install dry-run link to be `ok` and compare stable-home
   status before and after byte-for-byte.
7. Run exact-commit command-owner acceptance once with fresh outputs:

   ```sh
   ccfg26_acceptance_root="$(mktemp -d /tmp/ccfg-26-work-batch-acceptance.XXXXXX)"
   COMMAND_OWNER_CANDIDATE_CODEX_HOME=/home/alacasse/.codex-command-owner-redesign \
     .venv/bin/python -B scripts/command_owner_scenarios.py accept \
     tests/fixtures/command-owner-scenarios \
     --result-output "$ccfg26_acceptance_root/acceptance-result.json" \
     --json-report-output "$ccfg26_acceptance_root/report.json" \
     --text-report-output "$ccfg26_acceptance_root/report.txt"
   ```

8. Read the acceptance result and text report and record their hashes.
9. Request final independent `runway_reviewer` review over the exact candidate
   range and only actually triggered specialist reviews.
10. Prove the candidate target has no normal Batch Runway/APR dependency for
    work-batch execution or closeout, no new execution state, no candidate
    canonical write, and no successor selection.

All final gates are `required-green`. Final validation is not an implementation
slice.

## Same-Batch Closeout Under ADR 0004

The candidate target may prove COR-009 only in fixtures, temporary roots, and
isolated candidate installation during this batch. It must not control its own
development batch or mutate canonical stable planning.

After final candidate acceptance, the stable controller:

1. records exact candidate commits, validation, installation, acceptance,
   reviews, and strict receipts in `completed-slices.md`;
2. writes this batch's canonical `closeout.md`;
3. uses the current stable mechanism to reconcile CCFG-26 from completed
   evidence;
4. marks CCFG-26 `Closed` only when every COR-009 acceptance item is proven;
5. clears only this batch's selected/queued/active state; and
6. stops without selecting, dispatching, queuing, refreshing, or preparing
   CCFG-27 or any other row.

That stable closeout path is development bookkeeping, not retained target
product ownership or cross-generation runtime communication.

## Batch Stop Conditions

- Stop on any mismatch in Planning State currentness, strict context, canonical
  planning root, fresh lease, result echo, write scope, review basis, receipt,
  accepted movement, or exact candidate diff.
- Stop if candidate `work-batch` controls or closes this real development batch.
- Stop on any new execution-state file/store/schema, reservation, flight,
  attempt, process protocol, automatic cross-generation continuation, or shared
  runtime state.
- Stop if semantic queue currentness is inferred from Git or helpers rather than
  Planning State.
- Stop if a slice introduces a second executor/recovery/finalizer/reconciler,
  silent fallback, compatibility dialect, or broad owner dependency.
- Stop if an old-format active artifact is silently mutated by the candidate.
- Stop if a planning-contract, Planning State, schema, runner state/transition/
  validation, or bridge semantic change is required outside this ceiling.
- Stop on unexpected stable or candidate movement, unrelated dirty-file overlap,
  stable-home mutation, candidate canonical write, or unapproved scope expansion.
- Stop if final validation becomes an implementation slice.
- Stop if CCFG-27 through CCFG-29 or any unrelated finding is selected,
  prepared, dispatched, queued, activated, implemented, or closed.
