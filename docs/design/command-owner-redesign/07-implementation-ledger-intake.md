# Command-Owner Redesign Implementation Ledger Intake

## Purpose

This document is the durable intake packet for implementing the accepted
command-owner redesign.

It defines **individually addressable work items**. It does not define selected
batches, dispatches, runways, slices, or implementation commits.

The normal workflow is:

```text
this packet
  -> add-to-ledger ingests all items
  -> each item remains unselected
  -> plan-batch selects and shapes at most one eligible item
  -> work-batch executes only the resulting current runway
  -> same-batch closeout and stop
```

`plan-batch` may split, block, narrow, group, or defer an item when current
repository state, risk, owner seams, validation profiles, or acceptance
boundaries require it.

## Intake Contract

```yaml
schema: command-owner-implementation-intake/v1
program: codex-config
source_design_root: docs/design/command-owner-redesign
source_branch: architecture/command-owner-redesign

intake:
  command: add-to-ledger
  mode: multi-item
  select_after_intake: false
  create_dispatch: false
  create_runway: false
  execute_work: false

required_ledger_fields:
  - stable_work_item_id
  - title
  - status
  - exact_source_section
  - dependencies
  - relevant_decisions
  - relevant_behavior_contracts
  - acceptance_summary

initial_status: Open
```

## Global Constraints

Every item inherits these constraints:

- use the accepted decisions in `decisions.md`;
- use the phase order and two-generation protocol in
  `04-migration-program.md`;
- preserve behavior contracts rather than legacy skill topology;
- do not create permanent parallel command names or `skills-v2` directories;
- do not let candidate-generation skills control canonical planning state before
  cutover;
- use `skill-authoring` v1 before migrating target command-owner skills;
- remove corresponding legacy ownership in the same ownership-transfer batch;
- name every temporary bridge and its deletion condition;
- stop after same-batch closeout without selecting successor work;
- do not implement future parallel scheduling.

## Dependency Overview

```text
COR-001  Isolate stable and candidate generations
  -> COR-002  Verify contracts and blocking decisions
       -> COR-003  Skill contract schema and validators
       -> COR-004  Planning artifact schemas and validators
            COR-003 + COR-004
              -> COR-005  Finalize skill-authoring v1
                   COR-004 + COR-005
                     -> COR-006  Behavioral scenario harness
                          -> COR-007  Transfer add-to-ledger ownership
                               -> COR-008  Transfer plan-batch ownership
                                    -> COR-009  Transfer work-batch ownership
                                         -> COR-010  Runner and installation cutover
                                              -> COR-011  Delete legacy owners
                                                   -> COR-012  Authoring convergence
```

Items with the same satisfied dependencies may both be eligible, but only one
batch may be selected at a time.

---

## COR-001 — Establish Stable and Candidate Generations

### Purpose

Create a proven control boundary before modifying skills that are actively used
to plan and execute the migration.

### Included scope

- identify the stable checkout used by the default `CODEX_HOME`;
- create a separate candidate checkout of
  `architecture/command-owner-redesign`;
- use a separate clone as the default candidate implementation;
- create a separate candidate `CODEX_HOME`;
- prove stable and candidate fresh sessions report their generation and source
  paths;
- prove the stable toolchain can edit the candidate checkout without changing
  its own installed source;
- document installation switching and rollback;
- inspect selected, queued, active, and resumable planning state;
- optionally evaluate a worktree only as a bounded experiment.

### Excluded scope

- no target skill rewrite;
- no schema implementation;
- no ledger-format migration;
- no candidate-generation mutation of canonical planning state;
- no cutover to candidate skills.

### Dependencies

```yaml
depends_on: []
```

### Relevant decisions

- `DEC-011`
- `DEC-025`
- `DEC-026`

### Relevant behavior contracts

- `STATE-DIAG-001`
- `STATE-TRANSITION-002`
- `STATE-HISTORY-004`

### Acceptance evidence

```yaml
acceptance:
  stable_checkout_unchanged: true
  stable_generation_identity_proven: true
  candidate_checkout_isolated: true
  candidate_codex_home_isolated: true
  candidate_generation_identity_proven: true
  stable_can_edit_candidate_without_self_mutation: true
  selected_old_generation_dispatch: null
  queued_old_generation_runway: null
  active_old_generation_runway: null
  resumable_old_runner_state: false
  rollback_documented: true
```

### Planning authority

`plan-batch` may split this into environment creation and validation only when
one bounded runway would otherwise mix unrelated machine setup and repository
verification. A worktree must not be selected by assumption; a separate clone is
the default.

---

## COR-002 — Verify Source Contracts and Resolve Blocking Decisions

### Purpose

Verify that the accepted behavior contracts and target ownership model are
complete enough to guide implementation without preserving accidental topology.

### Included scope

- review current skills, tests, manifests, agents, state tooling, and active
  artifacts against `01-source-behavior-contracts.md`;
- verify target ownership in `02-target-ownership-model.md`;
- classify current tests as behavioral, schema/protocol, integration, or
  migration-retention topology;
- identify accidental structure and duplicate rule ownership;
- resolve open decisions that block contract schemas or state mutation;
- leave non-blocking naming and presentation decisions open.

### Excluded scope

- no target skill rewrite;
- no parser or schema implementation;
- no active ledger mutation beyond same-item closeout;
- no implementation of later phases.

### Dependencies

```yaml
depends_on:
  - COR-001
```

### Relevant decisions

- `DEC-001` through `DEC-010`
- `DEC-013` through `DEC-020`
- `DEC-022` through `DEC-026`
- `OPEN-001`
- `OPEN-002`
- `OPEN-003`

### Relevant behavior contracts

- all contracts in `01-source-behavior-contracts.md`

### Acceptance evidence

```yaml
acceptance:
  external_behavior_contracts_have_ids: true
  each_target_decision_has_one_owner: true
  accidental_source_structure_identified: true
  test_classification_complete_enough_for_harness: true
  blocking_open_decisions_resolved_or_explicitly_gated: true
```

### Planning authority

`plan-batch` may narrow this to one blocking decision or one evidence gap when
full verification would require unresolved implementation discovery.

---

## COR-003 — Implement `skill-contract/v1` Schema and Validators

### Purpose

Create the mechanically enforceable contract foundation used by hybrid skills
and by `skill-authoring` v1.

### Included scope

- define `skill-contract/v1`;
- locate and parse the canonical `## Contract` YAML block;
- validate required sections and supported values;
- validate `owns`, `delegates`, `requires`, `writes`, `forbids`, `outputs`,
  `stops_when`, and references;
- detect duplicate decision or durable-fact ownership;
- detect unknown delegated targets and dependency cycles;
- detect command-owner dependencies on retired broad owners;
- add malformed, missing-field, duplicate-owner, reference, and cosmetic-
  migration tests;
- provide compact actionable validation errors.

### Excluded scope

- no migration of `add-to-ledger`, `plan-batch`, or `work-batch`;
- no planning-artifact parser;
- no candidate-generation control of real migration work.

### Dependencies

```yaml
depends_on:
  - COR-002
```

### Relevant decisions

- `DEC-001`
- `DEC-002`
- `DEC-008`
- `DEC-009`
- `DEC-010`
- `DEC-015`
- `DEC-024`

### Relevant behavior contracts

- `STATE-CANONICAL-003`
- ownership implications across all intake, planning, execution, and closeout
  contracts

### Acceptance evidence

```yaml
acceptance:
  skill_contract_v1_parseable: true
  required_field_validation: green
  ownership_conflict_detection: green
  dependency_and_reference_validation: green
  retired_owner_dependency_detection: green
  cosmetic_migration_detection: green
```

### Planning authority

`plan-batch` may split parser/schema work from repository-wide ownership checks
when they form independently testable seams. It must preserve the dependency
that `skill-authoring` follows a working schema and core validator.

---

## COR-004 — Implement Planning Artifact Schemas and Validators

### Purpose

Represent active dispatch, runway, execution evidence, and closeout facts as
canonical structured contracts inside readable Markdown artifacts.

### Included scope

- define `planning-dispatch/v1`;
- define `planning-runway/v1`;
- define `planning-closeout/v1`;
- locate and parse embedded operational contract blocks;
- validate artifact identity, lineage, revisions, lifecycle state, dependencies,
  risks, approvals, write scopes, validation classes, result contracts, recovery,
  and closeout requirements;
- enforce one canonical owner for each machine fact;
- prototype a synthetic dispatch, runway, execution receipt, and closeout chain;
- define read-only compatibility policy for active old-format artifacts.

### Excluded scope

- no migration of historical archives;
- no parallel execution;
- no SQLite canonical state;
- no transfer of planning or execution ownership.

### Dependencies

```yaml
depends_on:
  - COR-002
```

### Relevant decisions

- `DEC-007`
- `DEC-008`
- `DEC-010`
- `DEC-016`
- `DEC-022`
- `DEC-023`
- `OPEN-001`
- `OPEN-002`
- `OPEN-003`
- `OPEN-004`
- `OPEN-005`

### Relevant behavior contracts

- `PLAN-DISPATCH-005`
- `PLAN-RUNWAY-006`
- `PLAN-RISK-007`
- `EXEC-RESUME-002`
- `EXEC-VALIDATE-004`
- `EXEC-REVIEW-005`
- `EXEC-COMMIT-006`
- `CLOSE-FINAL-001`
- `CLOSE-RECONCILE-002`
- `STATE-TRANSITION-002`
- `STATE-CANONICAL-003`

### Acceptance evidence

```yaml
acceptance:
  planning_dispatch_v1_parseable: true
  planning_runway_v1_parseable: true
  planning_closeout_v1_parseable: true
  canonicality_validation: green
  lineage_and_dependency_validation: green
  synthetic_vertical_chain: green
  old_format_compatibility_policy: explicit_and_read_only
```

### Planning authority

`plan-batch` may split dispatch, runway, and closeout schema work when one runway
would be too broad, but it must preserve compatible versioning and the vertical
prototype requirement.

---

## COR-005 — Finalize and Validate `skill-authoring` v1

### Purpose

Provide the repository-specific authoring workflow before any target command
owner is migrated.

### Included scope

- create `skills/skill-authoring/SKILL.md` at its final canonical path;
- make it authoritative for hybrid skill structure, ownership contracts,
  canonicality, procedure/decision/rationale separation, ambiguity reporting,
  migration rules, and reference splitting;
- define its boundary with the agent's generic skill-writing skill;
- invoke the schema and validators rather than duplicating them in prose;
- prevent cosmetic migration and silent conflict resolution;
- validate it by migrating or auditing `port-by-contract` or an equivalent
  representative skill;
- install and test it only in the candidate `CODEX_HOME` before cutover.

### Excluded scope

- no migration of `add-to-ledger`, `plan-batch`, or `work-batch`;
- no runtime dependency from command owners to `skill-authoring`;
- no implicit inheritance or hidden include system.

### Dependencies

```yaml
depends_on:
  - COR-003
  - COR-004
```

### Relevant decisions

- `DEC-008`
- `DEC-009`
- `DEC-010`
- `DEC-024`
- `DEC-026`

### Relevant behavior contracts

- `STATE-CANONICAL-003`
- target ownership implications across all command contracts

### Acceptance evidence

```yaml
acceptance:
  skill_authoring_v1_complete: true
  skill_authoring_v1_schema_valid: true
  generic_authoring_boundary_documented: true
  ambiguity_and_conflict_reporting: green
  cosmetic_migration_guard: green
  representative_skill_trial: green
  installed_only_in_candidate_codex_home: true
  canonical_state_mutation_during_trial: false
```

### Planning authority

`plan-batch` may narrow the representative trial but must not select a command-
owner migration before the full v1 completion standard is met.

---

## COR-006 — Build the Topology-Independent Behavioral Scenario Harness

### Purpose

Prove workflow behavior independently from legacy skill names, prose, modes, and
dependency topology.

### Included scope

- create isolated planning-root fixtures;
- cover intake, selection, scope shaping, dispatch, runway, execution, validation,
  review, commit, recovery, resume, closeout, reconciliation, and no-successor
  behavior;
- assert initial canonical facts, invoked public command, transitions, writes,
  forbidden writes, stop reasons, and evidence;
- characterize current behavior and define the target-compatible interface;
- run candidate-generation scenarios without touching the canonical planning
  root.

### Excluded scope

- no command-owner migration;
- no exact-prose preservation;
- no requirement that retired owners remain installed;
- no active planning-root mutation.

### Dependencies

```yaml
depends_on:
  - COR-004
  - COR-005
```

### Relevant decisions

- `DEC-015`
- `DEC-018`
- `DEC-019`
- `DEC-020`
- `DEC-026`

### Relevant behavior contracts

- all contracts in `01-source-behavior-contracts.md`

### Acceptance evidence

```yaml
acceptance:
  source_characterization_scenarios_green: true
  target_scenario_interface_defined: true
  expectations_independent_of_legacy_skill_names: true
  negative_write_assertions_present: true
  active_planning_root_untouched: true
```

### Planning authority

`plan-batch` may split the harness by command family when fixtures and validation
remain composable and the eventual deletion test covers the full workflow.

---

## COR-007 — Transfer Intake Ownership to `add-to-ledger`

### Purpose

Make `add-to-ledger` the sole owner of intake semantics and canonical ledger
mutation.

### Included scope

- use `skill-authoring` v1 to migrate `add-to-ledger`;
- preserve source identity, individually addressable findings, idempotence, and
  revision-checked mutation;
- implement or complete a narrow ledger-store mechanism;
- remove APR intake and normalization authority;
- remove the `legacy-removal` program-owner escape hatch;
- remove APR command dependency for intake;
- rewrite or delete topology tests that preserve APR intake ownership.

### Excluded scope

- no batch selection;
- no dispatch or runway creation;
- no migration of planning or execution ownership.

### Dependencies

```yaml
depends_on:
  - COR-005
  - COR-006
```

### Relevant decisions

- `DEC-001`
- `DEC-002`
- `DEC-014`
- `DEC-015`
- `DEC-016`
- `DEC-019`
- `DEC-024`

### Relevant behavior contracts

- `INTAKE-SOURCE-001`
- `INTAKE-IDENTITY-002`
- `INTAKE-NORMALIZE-003`
- `INTAKE-MUTATE-004`
- `INTAKE-STOP-005`
- `STATE-TRANSITION-002`

### Acceptance evidence

```yaml
acceptance:
  add_to_ledger_owns_intake_decisions: true
  add_to_ledger_broad_workflow_dependencies: 0
  add_to_ledger_contract_validates: true
  apr_intake_decisions_owned: 0
  legacy_removal_program_owner_escape_hatch: false
  intake_behavior_scenarios: green
```

### Planning authority

This item may be split only if the ledger-store mechanism is a separately useful
prerequisite. No split may leave APR and target intake as two normal owners.

---

## COR-008 — Transfer Planning Ownership to `plan-batch`

### Purpose

Make `plan-batch` the sole owner of selection, scope shaping, dispatch, runway
specification, risk, and validation-profile decisions.

### Included scope

- use `skill-authoring` v1 to migrate `plan-batch`;
- move planning references under `skills/plan-batch/references/`;
- produce hybrid dispatch and runway artifacts;
- replace APR and Batch Runway planning dependencies with narrow mechanisms;
- remove APR grouping, prioritization, selection, dispatch, and normal queue
  preparation authority;
- remove Batch Runway `create-spec`, semantic slice design, and validation-profile
  selection authority;
- rewrite or delete topology tests;
- retain only caller-scoped read-only compatibility required by active artifacts.

### Excluded scope

- no slice execution;
- no closeout ownership transfer;
- no runner cutover;
- no migration of historical archives.

### Dependencies

```yaml
depends_on:
  - COR-007
```

### Relevant decisions

- `DEC-001`
- `DEC-002`
- `DEC-005`
- `DEC-006`
- `DEC-007`
- `DEC-014`
- `DEC-015`
- `DEC-016`
- `DEC-024`
- `DEC-025`

### Relevant behavior contracts

- `PLAN-SOURCE-001`
- `PLAN-ACTIVE-002`
- `PLAN-SELECT-003`
- `PLAN-SCOPE-004`
- `PLAN-DISPATCH-005`
- `PLAN-RUNWAY-006`
- `PLAN-RISK-007`
- `PLAN-STOP-008`
- `STATE-DIAG-001`
- `STATE-TRANSITION-002`

### Acceptance evidence

```yaml
acceptance:
  plan_batch_owns_candidate_selection: true
  plan_batch_owns_scope_shaping: true
  plan_batch_owns_dispatch_definition: true
  plan_batch_owns_runway_specification: true
  plan_batch_owns_validation_profile_selection: true
  plan_batch_apr_dependency: false
  plan_batch_batch_runway_dependency: false
  apr_planning_decisions_owned: 0
  batch_runway_create_spec_callers: 0
  target_planning_scenarios: green
```

### Planning authority

`plan-batch` may narrow this to preparatory mechanism work only when the selected
dispatch states the immediate ownership transfer still required. A batch is not
complete while the old owner remains an equally valid normal route.

---

## COR-009 — Transfer Execution and Closeout Ownership to `work-batch`

### Purpose

Make `work-batch` the sole owner of execution lifecycle, recovery, acceptance,
finalization, closeout, and same-batch reconciliation.

### Included scope

- use `skill-authoring` v1 to migrate `work-batch`;
- move execution, recovery, finalization, and retention references under
  `skills/work-batch/references/`;
- retain worker and reviewer as narrow independent agents;
- produce hybrid execution receipts and closeout artifacts;
- remove Batch Runway `execute-spec`, recovery, finalization, and commit-workflow
  authority;
- remove APR `closeout-runway` and same-batch reconciliation authority;
- preserve the no-successor boundary;
- rewrite or delete topology tests;
- complete or explicitly migrate active old-format execution state before
  cutover.

### Excluded scope

- no new work intake;
- no successor planning;
- no runner installation cutover;
- no physical deletion of all legacy directories yet.

### Dependencies

```yaml
depends_on:
  - COR-008
```

### Relevant decisions

- `DEC-001`
- `DEC-002`
- `DEC-006`
- `DEC-014`
- `DEC-015`
- `DEC-016`
- `DEC-018`
- `DEC-019`
- `DEC-020`
- `DEC-024`

### Relevant behavior contracts

- `EXEC-CURRENT-001`
- `EXEC-RESUME-002`
- `EXEC-WORKER-003`
- `EXEC-VALIDATE-004`
- `EXEC-REVIEW-005`
- `EXEC-COMMIT-006`
- `EXEC-RECOVER-007`
- `EXEC-STOP-008`
- `CLOSE-FINAL-001`
- `CLOSE-RECONCILE-002`
- `CLOSE-NEXT-003`
- `STATE-TRANSITION-002`

### Acceptance evidence

```yaml
acceptance:
  work_batch_owns_execution_lifecycle: true
  work_batch_owns_recovery: true
  work_batch_owns_closeout: true
  work_batch_owns_same_batch_reconciliation: true
  work_batch_apr_dependency: false
  work_batch_batch_runway_dependency: false
  batch_runway_execute_spec_callers: 0
  apr_closeout_decisions_owned: 0
  target_execution_and_closeout_scenarios: green
```

### Planning authority

This item may be split by execution seam only when each batch removes a named
legacy decision and the remaining dual ownership is explicitly blocked from
normal use.

---

## COR-010 — Cut Over Runner, Manifest, Agents, and Installation

### Purpose

Make all installed surfaces consume public target commands and safely switch the
default toolchain from stable to candidate generation.

### Included scope

- remove APR and Batch Runway from command-owner feature dependencies;
- separate runner installation from APR;
- replace runner instructions that name old modes with public plan/work command
  protocols;
- update active docs, feature descriptions, agent metadata, and installation;
- run complete candidate fixture workflows;
- verify stable rollback;
- confirm no selected, queued, active, or resumable old-generation state;
- perform the installation switch as the final controlled action;
- finish the controlling stable session without changing its loaded generation;
- start a fresh candidate-generation diagnostic after cutover.

### Excluded scope

- no backlog selection semantics in the runner;
- no slice-design semantics in the runner;
- no physical deletion of all legacy owner directories until the target
  generation is proven current.

### Dependencies

```yaml
depends_on:
  - COR-009
```

### Relevant decisions

- `DEC-011`
- `DEC-016`
- `DEC-017`
- `DEC-018`
- `DEC-026`

### Relevant behavior contracts

- `PLAN-STOP-008`
- `EXEC-CURRENT-001`
- `CLOSE-NEXT-003`
- `STATE-DIAG-001`
- `STATE-TRANSITION-002`
- `STATE-HISTORY-004`

### Acceptance evidence

```yaml
acceptance:
  command_owner_manifest_legacy_dependencies: 0
  runner_prompts_using_old_modes: 0
  runner_installation_owned_by_apr_feature: false
  candidate_full_fixture_workflow: green
  no_old_generation_active_state: true
  rollback_to_stable: proven
  fresh_candidate_generation_diagnostic: green
  default_toolchain_generation: candidate
```

### Planning authority

`plan-batch` may split preparatory manifest/runner work from the final switch.
The final switch must remain a bounded batch with explicit rollback and no active
old-generation state.

---

## COR-011 — Delete Architecture Program Runway and Batch Runway

### Purpose

Physically remove the retired broad owners and migration-only topology after the
target generation is current.

### Included scope

- delete `skills/architecture-program-runway/`;
- delete `skills/batch-runway/` after moving surviving references;
- delete old modes and direct-command metadata;
- delete topology tests, expired transition fixtures, and expired parsers;
- remove duplicated rules and vocabulary;
- preserve clearly archived historical artifacts without rewriting them;
- run target behavioral scenarios after physical deletion.

### Excluded scope

- no new compatibility wrapper;
- no historical archive rewrite;
- no behavior narrowing without an accepted decision.

### Dependencies

```yaml
depends_on:
  - COR-010
```

### Relevant decisions

- `DEC-005`
- `DEC-006`
- `DEC-014`
- `DEC-015`
- `DEC-016`
- `DEC-022`

### Relevant behavior contracts

- all target behavior contracts;
- `STATE-HISTORY-004`

### Acceptance evidence

```yaml
acceptance:
  architecture_program_runway_directory_exists: false
  batch_runway_directory_exists: false
  active_old_mode_references: 0
  tests_requiring_old_owner_presence: 0
  active_legacy_artifacts: 0
  target_behavioral_scenarios: green
```

### Planning authority

`plan-batch` may split deletion by owner only when the remaining owner has no
normal caller and has an immediate measurable deletion condition.

---

## COR-012 — Perform Contract-First Authoring Convergence

### Purpose

Audit the completed target skills and refine the already-authoritative
`skill-authoring` v1 after real dogfooding.

### Included scope

- audit `port-by-contract`, `add-to-ledger`, `plan-batch`, and `work-batch`;
- collect authoring findings from the migration;
- integrate compatible refinements to optional fields, report layout, size
  heuristics, reference loading, and non-breaking validation;
- remove temporary authoring exceptions and per-skill dialects;
- document any semantic change as a new explicit schema decision.

### Excluded scope

- no recreation of retired owners;
- no unrelated workflow redesign;
- no silent `skill-contract/v2` semantics.

### Dependencies

```yaml
depends_on:
  - COR-011
```

### Relevant decisions

- `DEC-008`
- `DEC-009`
- `DEC-010`
- `DEC-024`

### Relevant behavior contracts

- `STATE-CANONICAL-003`
- all command-owner behavior contracts as audit evidence

### Acceptance evidence

```yaml
acceptance:
  contract_first_target_skills_consistent: true
  temporary_authoring_exceptions: 0
  per_skill_contract_dialects: 0
  skill_authoring_v1_convergence_audit: passed
```

### Planning authority

`plan-batch` may split audit and compatible cleanup, but semantic contract
changes require a separate explicit ledger item and accepted decision.

---

## `add-to-ledger` Intake Instructions

When this packet is ready to enter the program, the intake request must:

1. use `add-to-ledger` as the explicit intake boundary;
2. create or update one ledger row for each `COR-001` through `COR-012`;
3. link each row to its exact heading in this file;
4. preserve dependencies exactly;
5. keep every row individually addressable;
6. leave every row unselected;
7. avoid grouping them into preselected batches;
8. stop without creating a dispatch, runway, or implementation change.

The final intake report must list every row created or updated and confirm:

```yaml
selected_dispatch: null
queued_runway: null
active_runway: null
implementation_started: false
```
