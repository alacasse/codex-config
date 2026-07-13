# Migration Program

## Program Contract

```yaml
schema: command-owner-migration-program/v1

source_baseline:
  repository: alacasse/codex-config
  commit: 86db50f91b0df4c00d5fa26beda0091796a43e81

target_environment:
  branch: architecture/command-owner-redesign
  recommended_worktree: ../codex-config-contract-first
  recommended_candidate_codex_home: ~/.codex-contract-first

phase_order:
  - phase-0-isolation-and-baseline
  - phase-1-contract-distillation
  - phase-2-contract-formats-and-validators
  - phase-3-behavioral-scenario-harness
  - phase-4-add-to-ledger-transfer
  - phase-5-plan-batch-transfer
  - phase-6-work-batch-transfer
  - phase-7-runner-and-installation-cutover
  - phase-8-legacy-owner-deletion
  - phase-9-skill-authoring-meta-skill

execution_policy:
  one_phase_active: true
  one_batch_active: true
  future_phase_implementation: forbidden
  phase_completion_requires:
    - acceptance_criteria_passed
    - required_behavioral_scenarios_passed
    - legacy_ownership_reduced
    - temporary_bridges_registered
    - no_unowned_compatibility
```

## Program Rules

- The phase order is dependency-significant and must not be rearranged without
  an accepted decision recorded in `decisions.md`.
- Design, decomposition, and implementation occur in separate fresh sessions.
- A phase may contain more than one bounded batch when necessary, but only one
  batch may be selected at a time.
- A target surface must not become authoritative while the old owner remains an
  equally valid normal route.
- Every implementation phase must remove or narrow named legacy ownership.
- A phase is not complete merely because target and legacy paths both work.
- No batch may preserve a topology test solely because it currently passes.
- No active old-format artifact may be abandoned or silently reinterpreted.
- Same-batch closeout may reconcile the completed batch but may not select the
  next batch.
- Rollback uses Git history and the stable installation lane, not permanent
  runtime duplication.

## Temporary Bridge Record

Every temporary bridge must be recorded in the selected batch and closeout:

```yaml
bridge:
  id: BRIDGE-<stable-id>
  caller: exact caller
  reason: concrete migration need
  owner: migration phase or batch
  allowed_scope:
    - exact operation or artifact class
  introduced_in: commit-or-batch
  deletion_condition:
    - measurable condition
  status: proposed | active | removed
```

A bridge without these fields is an architectural defect.

## Phase 0 — Isolation and Baseline

### Objective

Create a stable execution lane and an isolated candidate lane before changing
skills that are currently installed and used to perform the migration.

### Required work

- Create or confirm a dedicated branch or Git worktree for the candidate target.
- Use final canonical `skills/<name>/` paths inside the candidate lane.
- Configure a separate candidate `CODEX_HOME`.
- Confirm the stable installation still points at the stable checkout.
- Freeze and record the source baseline commit.
- Confirm no selected, queued, or active old-format batch will be disrupted.
- Confirm no resumable runner state requires the current runtime owners.
- Establish rollback instructions based on Git and installation switching.

### Forbidden work

- No target skill implementation.
- No active ledger mutation.
- No batch selection.
- No creation of `skills-v2/`, `skills-next/`, or version-suffixed human
  commands.
- No in-place mutation of a checkout currently used by active coordinator,
  worker, or reviewer sessions.

### Entry gate

```yaml
required:
  - source repository accessible
  - stable installation identifiable
```

### Exit gate

```yaml
stable_lane_unchanged: true
candidate_lane_operational: true
source_commit_frozen: true
candidate_codex_home_isolated: true
selected_old_format_dispatch: null
queued_old_format_runway: null
active_old_format_runway: null
resumable_old_runner_state: false
```

### Validation

- inspect installation state and symlink targets;
- run candidate install dry-run;
- start a fresh candidate session that can list installed candidate features;
- verify the stable session still reads stable skills.

## Phase 1 — Contract Distillation

### Objective

Extract source behavior and target ownership through `port-by-contract`
reasoning before implementation.

### Allowed modes

```text
intake-source
distill-contract
design-target
```

### Forbidden mode

```text
create-port-runway
```

The current runway skills are source implementation, not migration authority.

### Required work

- Verify and complete the behavior contracts in
  `01-source-behavior-contracts.md`.
- Verify and complete the target ownership model.
- Map source tests to behavior contracts.
- Identify accidental source structure.
- Record unresolved decisions without guessing.
- Confirm each workflow decision has exactly one target owner.

### Forbidden work

- No target skill rewrite.
- No schema or parser implementation.
- No program ledger mutation.
- No implementation runway.

### Entry gate

- Phase 0 complete.
- Source baseline unchanged or explicitly refreshed through a decision record.

### Exit gate

```yaml
external_behavior_contracts_have_ids: true
each_target_decision_has_one_owner: true
accidental_source_structure_identified: true
test_classification_complete_enough_for_harness: true
open_human_decisions_explicit: true
implementation_started: false
```

### Validation

- architecture review against current skills, tests, manifests, agents, and
  tooling;
- deletion-test thought experiment for APR and Batch Runway;
- human review of accepted and open decisions.

## Phase 2 — Contract Formats and Validators

### Objective

Validate the contract-first representation before broad workflow migration.

### Required work

- Define and validate `skill-contract/v1`.
- Define and validate `planning-dispatch/v1`.
- Define and validate `planning-runway/v1`.
- Define and validate `planning-closeout/v1`.
- Implement lightweight block location, parsing, and schema validation.
- Implement ownership conflict and reference checks.
- Prototype the skill format on `port-by-contract` or a non-runtime copy of it.
- Prototype one synthetic dispatch, runway, execution receipt, and closeout
  chain.
- Compare readability, ambiguity, context size, and validation coverage.

### Forbidden work

- No production transfer of plan or work ownership.
- No new normal command names.
- No installation of prototypes as runtime skills.
- No `skill-authoring` meta-skill yet.
- No migration of historical artifacts.

### Entry gate

- Phase 1 complete.
- No unresolved decision blocks the initial schemas.

### Exit gate

```yaml
skill_contract_v1_parseable: true
planning_dispatch_v1_parseable: true
planning_runway_v1_parseable: true
planning_closeout_v1_parseable: true
ownership_conflict_detection_proven: true
reference_validation_proven: true
canonicality_rules_documented: true
prototype_runtime_authority: false
```

### Validation

- schema unit tests;
- malformed and missing-field tests;
- duplicate-owner tests;
- unknown-reference tests;
- structured/prose contradiction fixtures where mechanically detectable;
- human review of representative diffs.

## Phase 3 — Behavioral Scenario Harness

### Objective

Create topology-independent proof of source and target workflow behavior before
moving ownership.

### Required work

Create temporary planning-root fixtures for at least:

- empty ledger;
- one eligible finding;
- multiple eligible findings;
- explicitly requested finding;
- missing requested finding;
- vague mixed-risk finding;
- selected dispatch;
- queued runway;
- active runway;
- invalid or stale state;
- validation failure;
- review failure;
- dirty-file conflict;
- partial execution;
- resume after interruption;
- successful closeout;
- same-batch reconciliation;
- no successor selection;
- unsupported legacy discovery;
- triggered test-quality review.

Each scenario must assert:

- initial canonical artifacts;
- invoked public command;
- expected state transition;
- expected files written;
- forbidden writes;
- stable stop reason;
- validation evidence.

### Forbidden work

- Do not make old skill names part of expected output unless the scenario is
  explicitly testing a migration bridge.
- Do not rely on exact prose in `SKILL.md`.
- Do not mutate the active repository planning root.

### Entry gate

- Phase 2 schemas and validators accepted.
- Contract IDs stable enough to label scenarios.

### Exit gate

```yaml
source_characterization_scenarios_green: true
target_scenario_interface_defined: true
scenario_expectations_independent_of_legacy_skill_names: true
active_planning_root_untouched: true
```

### Validation

- fixture isolation test;
- file-effect assertions;
- structured transition assertions;
- negative write assertions;
- source behavior review for any failing characterization.

## Phase 4 — `add-to-ledger` Ownership Transfer

### Objective

Make `add-to-ledger` the sole owner of intake and canonical ledger mutation.

### Responsibilities introduced or completed

- source identity preservation;
- finding normalization;
- create, update, merge, or no-op decision;
- revision-checked ledger mutation;
- intake receipt;
- stop-before-planning boundary.

### Legacy ownership removed in the same phase

- APR intake mode;
- APR finding normalization authority;
- APR normal ledger mutation authority;
- legacy-removal program-owner exception.

### Required work

- Migrate `add-to-ledger` to `skill-contract/v1`.
- Introduce or complete the narrow ledger-store interface.
- Add behavioral intake and idempotence tests.
- Remove command manifest dependencies on APR for intake.
- Rewrite or delete text/topology tests that require APR intake ownership.
- Keep any old-format ledger reader read-only and caller-scoped.

### Entry gate

```yaml
required_phases:
  - phase-3-behavioral-scenario-harness
required_scenarios:
  - fresh-finding-intake
  - duplicate-finding-intake
  - requested-missing-finding
  - stale-ledger-revision
```

### Exit gate

```yaml
add_to_ledger:
  owns_intake_decisions: true
  broad_workflow_dependencies: 0
  behavior_scenarios_green: true
architecture_program_runway:
  intake_decisions_owned: 0
legacy_removal:
  program_owner_escape_hatch: false
```

### Rollback boundary

Rollback the complete intake transfer as one unit. Do not restore APR as a
second normal intake path while retaining the target path.

## Phase 5 — `plan-batch` Ownership Transfer

### Objective

Make `plan-batch` the sole owner of semantic planning and runway specification.

### Responsibilities introduced or completed

- current-state branch decision;
- candidate eligibility and selection;
- grouping into one bounded batch;
- split, block, or narrow decision;
- dispatch definition;
- batch kind, risk, and approval gates;
- runway slice design;
- validation-profile selection;
- selected and queued transition requests;
- stop-before-implementation boundary.

### Legacy ownership removed in the same phase

From APR:

- grouping;
- prioritization;
- candidate selection;
- selected dispatch creation;
- split, block, or narrow workflow ownership;
- normal queue preparation.

From Batch Runway:

- `create-spec` mode;
- semantic slice design;
- validation-profile selection during planning;
- planning-mode inference from human language.

### Required work

- Migrate `plan-batch` to `skill-contract/v1`.
- Move planning references under `skills/plan-batch/references/`.
- Produce and validate hybrid dispatch and runway artifacts.
- Replace APR and Batch Runway planning dependencies with narrow mechanisms.
- Update runner planning invocation to the public plan command protocol when
  useful without completing runner cutover early.
- Remove or rewrite tests that require APR and Batch Runway planning topology.
- Preserve a read-only old-format spec parser only if active artifacts require
  it.

### Entry gate

```yaml
required_phases:
  - phase-4-add-to-ledger-transfer
required_scenarios:
  - empty-ledger
  - one-eligible-finding
  - multiple-eligible-findings
  - explicitly-requested-finding
  - vague-mixed-risk-finding
  - selected-dispatch-exists
  - queued-runway-exists
  - active-runway-exists
required_schemas:
  - planning-dispatch/v1
  - planning-runway/v1
forbidden_state:
  - active_old_format_runway
```

### Exit gate

```yaml
plan_batch:
  owns_candidate_selection: true
  owns_scope_shaping: true
  owns_dispatch_definition: true
  owns_runway_specification: true
  owns_validation_profile_selection: true
  architecture_program_runway_dependency: false
  batch_runway_dependency: false
architecture_program_runway:
  planning_decisions_owned: 0
batch_runway:
  create_spec_callers: 0
  planning_decisions_owned: 0
new_active_artifact_format: hybrid_v1_only
```

### Rollback boundary

Rollback the whole planning transfer. Do not keep both target plan-batch and APR
selection as valid normal routes.

## Phase 6 — `work-batch` Ownership Transfer

### Objective

Make `work-batch` the sole owner of execution, recovery, finalization, and
same-batch closeout.

### Responsibilities introduced or completed

- queued-to-active transition request;
- next incomplete slice choice;
- worker and reviewer lifecycle;
- validation acceptance;
- specialist review routing;
- commit acceptance and evidence;
- recovery and resume;
- final validation;
- closeout evidence;
- finding reconciliation decision;
- active-to-completed transition request;
- no-successor boundary.

### Legacy ownership removed in the same phase

From Batch Runway:

- `execute-spec` mode;
- execution lifecycle ownership;
- recovery ownership;
- finalization ownership;
- commit and evidence ownership as workflow decisions.

From APR:

- `closeout-runway` mode;
- same-batch reconciliation ownership;
- completed-batch queue-clearing decision.

### Required work

- Migrate `work-batch` to `skill-contract/v1`.
- Move execution, recovery, finalization, and retention references under
  `skills/work-batch/references/`.
- Retain worker and reviewer as narrow independent agent mechanisms.
- Produce and validate hybrid execution receipts and closeout artifacts.
- Replace APR and Batch Runway dependencies with narrow mechanisms.
- Remove or rewrite topology tests.
- Complete any active old-format batch under its named contract or explicitly
  migrate it before cutover.

### Entry gate

```yaml
required_phases:
  - phase-5-plan-batch-transfer
required_scenarios:
  - start-queued-batch
  - validation-failure
  - review-failure
  - dirty-file-conflict
  - partial-execution
  - resume-after-interruption
  - successful-closeout
  - same-batch-reconciliation
  - no-successor-selection
required_schema:
  - planning-closeout/v1
```

### Exit gate

```yaml
work_batch:
  owns_execution_lifecycle: true
  owns_recovery: true
  owns_closeout: true
  owns_same_batch_reconciliation: true
  architecture_program_runway_dependency: false
  batch_runway_dependency: false
batch_runway:
  execute_spec_callers: 0
  execution_decisions_owned: 0
architecture_program_runway:
  closeout_decisions_owned: 0
```

### Rollback boundary

Rollback the complete execution ownership transfer. Do not restore an old
closeout owner while leaving target work-batch finalization authoritative.

## Phase 7 — Runner and Installation Cutover

### Objective

Make installation, manifests, agents, and the runner consume only public target
command protocols and narrow mechanisms.

### Required work

- Remove APR and Batch Runway from command-owner feature dependencies.
- Separate runner installation from APR.
- Replace runner phase instructions that name old modes with public plan and work
  command protocols.
- Keep runner-owned concerns limited to process lifecycle, bounds, environment,
  sandbox, telemetry, and explicit loop policy.
- Update active docs, prompts, manifests, and feature descriptions.
- Install and run the candidate toolchain in the isolated `CODEX_HOME`.
- Run a complete candidate plan and work workflow on a controlled fixture.

### Forbidden work

- The runner may not choose findings or design slices.
- The runner may not reinterpret closeout or select a successor through
  work-batch.
- No direct-command metadata for retired owners.

### Entry gate

- Phase 6 complete.
- No active old-format execution state.

### Exit gate

```yaml
command_owner_manifest_legacy_dependencies: 0
runner_prompts_using_old_modes: 0
runner_installation_owned_by_apr_feature: false
candidate_full_workflow_green: true
stable_rollback_available: true
```

## Phase 8 — Legacy Owner Deletion

### Objective

Physically remove the broad legacy owners and migration-only topology.

### Required work

- Delete `skills/architecture-program-runway/`.
- Delete `skills/batch-runway/` after moving surviving references to their target
  owners.
- Delete old modes and direct-command metadata.
- Delete migration-retention and topology tests that protect retired structure.
- Delete expired transition fixtures and parsers.
- Remove duplicated rules and vocabulary.
- Run the target behavior suite after physical deletion.
- Preserve clearly archived historical artifacts without rewriting them.

### Entry gate

- Phase 7 complete.
- All conditions in `06-deletion-conditions.md` satisfied or explicitly waived
  by an accepted human decision.

### Exit gate

```yaml
architecture_program_runway_directory_exists: false
batch_runway_directory_exists: false
active_old_mode_references: 0
tests_requiring_old_owner_presence: 0
active_legacy_artifacts: 0
target_behavioral_scenarios_green: true
```

### Rollback boundary

Rollback is the pre-deletion commit and stable installation. Do not recreate
permanent compatibility wrappers.

## Phase 9 — Skill-Authoring Meta-Skill

### Objective

Implement GitHub issue #49 only after the contract-first format and target
owners have proven the authoring rules.

### Required work

- Create `skill-authoring` or the accepted final name.
- Encode extraction, ownership conflict detection, procedure/rationale split,
  reference loading, and validation guidance.
- Invoke schema and ownership validators rather than duplicating them in prose.
- Validate the meta-skill on a new skill and an audit of an existing target
  skill.

### Forbidden work

- No runtime dependency from command owners.
- No ownership of planning state or workflow execution.
- No implicit inheritance or hidden include system.
- No cosmetic migration that preserves source prose by default.

### Entry gate

```yaml
skill_contract_v1_validated_on:
  - port-by-contract
  - add-to-ledger
  - plan-batch
  - work-batch
planning_artifact_v1_chain_validated: true
open_schema_questions: 0
```

### Exit gate

```yaml
meta_skill_runtime_dependencies: 0
meta_skill_ownership_conflict_detection_proven: true
cosmetic_migration_guard_proven: true
```

## Implementation Decomposition Rules

After this program is accepted, a separate design-only session may create the
ordered implementation batches.

Each batch must declare:

```yaml
batch:
  phase: phase-id
  satisfies_contracts: []
  introduces_target_responsibilities: []
  removes_legacy_responsibilities: []
  temporary_bridges: []
  required_scenarios: []
  entry_gate: []
  exit_gate: []
  rollback_boundary: string
```

A batch is invalid when it:

- adds a new owner but removes no corresponding legacy ownership;
- combines multiple migration phases without a dependency reason;
- preserves old tests without classifying them;
- introduces a compatibility route without a deletion condition;
- creates more than one selected implementation batch;
- authorizes future phase work;
- treats coexistence as completion.

## Handoff Boundaries

Use three separate fresh-session handoffs:

1. **Architecture package review:** validate contracts, decisions, and phase
   order; no implementation.
2. **Implementation decomposition:** create ordered bounded batches and only the
   first dispatch/runway; no implementation.
3. **Batch execution:** execute only the selected batch, close and reconcile the
   same batch, then stop.
