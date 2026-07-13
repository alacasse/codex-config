# Migration Program

## Program Contract

```yaml
schema: command-owner-migration-program/v2

source_baseline:
  repository: alacasse/codex-config
  commit: 86db50f91b0df4c00d5fa26beda0091796a43e81

design_branch: architecture/command-owner-redesign
implementation_intake_packet: docs/design/command-owner-redesign/07-implementation-ledger-intake.md

control_model:
  before_cutover: stable_generation_controls_real_work
  candidate_generation: validation_only
  after_cutover: candidate_generation_becomes_current

phase_order:
  - phase-0-isolation-and-baseline
  - phase-1-contract-distillation
  - phase-2-contract-formats-validators-and-skill-authoring
  - phase-3-behavioral-scenario-harness
  - phase-4-add-to-ledger-transfer
  - phase-5-plan-batch-transfer
  - phase-6-work-batch-transfer
  - phase-7-runner-and-installation-cutover
  - phase-8-legacy-owner-deletion
  - phase-9-contract-first-authoring-convergence

execution_policy:
  intake_many_items_at_once: true
  plan_at_most_one_batch: true
  execute_only_current_runway: true
  successor_selection_during_closeout: false
  future_phase_implementation: forbidden
```

## Planning Vocabulary

The program uses four distinct levels:

| Level | Meaning | Owner |
|---|---|---|
| Phase | Architectural dependency order and broad acceptance boundary. | This design package and accepted decisions. |
| Work item | Individually addressable durable implementation need linked from `07-implementation-ledger-intake.md`. | `add-to-ledger` records it in the canonical ledger. |
| Batch | One bounded selection or narrowing of eligible ledger work with one dispatch and one runway. | `plan-batch`. |
| Slice | One independently executable row inside the current runway. | `work-batch` coordinates execution. |

A phase is not a preselected batch. One phase may require several ledger items or
several sequential batches. `plan-batch` decides the runnable boundary from
current state and may split, block, narrow, group, or defer an item.

## Program Entry Protocol

Before implementation begins:

1. create or update `07-implementation-ledger-intake.md`;
2. invoke `add-to-ledger` once with the complete packet;
3. create or update all individually addressable work items in the canonical
   `codex-config` program ledger;
4. preserve each item's dependencies and exact source-section link;
5. leave every item unselected;
6. stop without creating a dispatch or runway.

After intake, the normal loop is:

```text
fresh plan-batch
  -> choose one eligible item or bounded grouping
  -> produce one selected dispatch and one queued runway
  -> stop

fresh work-batch
  -> execute only that runway
  -> reconcile only that batch
  -> stop without selecting a successor
```

A design-only implementation batch map is forbidden because it would bypass the
normal selection and scope-shaping authority of `plan-batch`.

## Two-Generation Bootstrap Protocol

### Stable control lane

```yaml
toolchain_generation: stable
toolchain_source_checkout: stable checkout used by default CODEX_HOME
target_repository_checkout: separate candidate checkout
canonical_planning_state_mutation_allowed: true
```

The stable lane:

- performs the multi-item `add-to-ledger` intake;
- selects real migration work through the current `plan-batch`;
- executes real migration batches through the current `work-batch`;
- edits files only in the candidate checkout;
- produces canonical ledger, dispatch, runway, commit, and closeout state;
- remains unchanged and available for rollback until cutover.

### Candidate validation lane

```yaml
toolchain_generation: candidate
toolchain_source_checkout: candidate checkout
target_repository_checkout: candidate checkout or isolated fixture checkout
codex_home: separate candidate CODEX_HOME
canonical_planning_state_mutation_allowed: false
```

Before cutover, the candidate lane may:

- validate schemas and contract blocks;
- run topology-independent behavioral fixtures;
- run controlled trials of candidate skills;
- verify fresh-session loading and installation identity;
- return compact evidence to the stable controlling batch.

Before cutover, the candidate lane may not:

- mutate the canonical program ledger;
- select, queue, execute, recover, or close a real migration batch;
- change toolchain generation midway through a command;
- treat successful fixture behavior as authorization to self-host real work.

### Candidate checkout choice

The default candidate checkout is a **separate clone**. It is familiar, visibly
independent, and does not rely on unproven agent behavior around worktrees.

A Git worktree is permitted only when the isolation work item proves all of the
following:

- the agent resolves the intended checkout consistently;
- the installer links the intended skill source paths;
- the runner and validation commands operate in the intended checkout;
- branch and dirty-worktree diagnostics remain unambiguous;
- rollback instructions are tested.

Worktree support is not assumed by this program.

### Required generation record

Every planning, execution, or candidate-validation report records:

```yaml
toolchain_generation: stable | candidate
toolchain_source_checkout: absolute path
target_repository_checkout: absolute path
codex_home: absolute path
canonical_planning_state_mutation_allowed: true | false
```

Missing or contradictory generation evidence is a stop condition.

## Program Rules

- The phase order is dependency-significant and may change only through an
  accepted decision.
- Implementation work must already exist in the canonical ledger before
  `plan-batch` may select it.
- One `add-to-ledger` request may ingest the complete program packet.
- One `plan-batch` invocation produces at most one dispatch and one runway.
- One `work-batch` invocation consumes only the current queued or active runway.
- A target surface must not become authoritative while the old owner remains an
  equally valid normal route.
- Every ownership-transfer batch removes or narrows named legacy ownership.
- A phase is not complete merely because target and legacy paths both work.
- No batch preserves a topology test solely because it currently passes.
- No active old-format artifact is abandoned or silently reinterpreted.
- Same-batch closeout does not select the next batch.
- Rollback uses Git history and the stable installation lane, not permanent
  runtime duplication.
- `skill-authoring` v1 is complete and authoritative before any target command
  owner is migrated.
- Dogfood findings may refine compatible guidance; semantic changes to ownership
  or canonicality require an explicit schema decision.

## Temporary Bridge Record

Every temporary bridge must be recorded in the selected dispatch, runway, and
closeout:

```yaml
bridge:
  id: BRIDGE-<stable-id>
  caller: exact caller
  reason: concrete migration need
  owner: migration work item or batch
  allowed_scope:
    - exact operation or artifact class
  introduced_in: commit-or-batch
  deletion_condition:
    - measurable condition
  status: proposed | active | removed
```

A bridge without these fields is an architectural defect.

# Phase Contracts

## Phase 0 — Isolation and Baseline

### Ledger item

`COR-001` in `07-implementation-ledger-intake.md`.

### Objective

Establish a stable control lane and an isolated candidate validation lane before
changing skills that are currently installed and used to perform the migration.

### Required work

- confirm the stable checkout and default `CODEX_HOME` source paths;
- create a separate candidate clone at the design branch by default;
- create a separate candidate `CODEX_HOME`;
- prove a fresh session can report which generation it loaded;
- confirm the stable lane edits the candidate checkout rather than itself;
- confirm no selected, queued, active, or resumable state will be disrupted;
- document installation switching and rollback;
- evaluate a worktree only as an optional experiment, not a prerequisite.

### Forbidden work

- no target skill rewrite;
- no active ledger-format migration;
- no candidate-generation mutation of canonical state;
- no permanent `skills-v2/`, `skills-next/`, or version-suffixed commands.

### Exit gate

```yaml
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

## Phase 1 — Contract Distillation

### Ledger item

`COR-002`.

### Objective

Verify source behavior and target ownership before implementation.

### Required work

- verify and complete `01-source-behavior-contracts.md`;
- verify the target ownership model;
- map source tests to behavior contracts;
- identify accidental source topology;
- resolve or preserve open decisions explicitly;
- confirm every workflow decision has one target owner.

### Allowed `port-by-contract` modes

```text
intake-source
distill-contract
design-target
```

### Forbidden work

- no target skill rewrite;
- no schema implementation;
- no use of `create-port-runway` as migration authority;
- no new program selection.

### Exit gate

```yaml
external_behavior_contracts_have_ids: true
each_target_decision_has_one_owner: true
accidental_source_structure_identified: true
test_classification_complete_enough_for_harness: true
open_human_decisions_explicit: true
```

## Phase 2 — Contract Formats, Validators, and `skill-authoring` v1

Phase 2 is intentionally represented by several ledger items so `plan-batch`
can bound them independently.

### COR-003 — Skill contract schema and validators

Required outcomes:

- `skill-contract/v1` schema;
- block location and parsing;
- required-field validation;
- ownership, delegation, dependency, and reference checks;
- malformed, duplicate-owner, cosmetic-migration, and retired-dependency tests.

### COR-004 — Planning artifact schemas and validators

Required outcomes:

- `planning-dispatch/v1`;
- `planning-runway/v1`;
- `planning-closeout/v1`;
- canonicality and lineage validation;
- synthetic dispatch/runway/receipt/closeout chain;
- explicit handling of unresolved transaction and storage decisions.

### COR-005 — Finalize `skill-authoring` v1

Required outcomes:

```yaml
skill_authoring_v1:
  complete: true
  authoritative_for:
    - hybrid_skill_structure
    - ownership_contracts
    - canonicality
    - migration_rules
    - ambiguity_reporting
  validated_by:
    - schema_tests
    - malformed_contract_tests
    - ownership_conflict_tests
    - cosmetic_migration_tests
    - representative_skill_migration_or_audit
  runtime_dependency_of_command_owners: false
```

`skill-authoring` is validated on `port-by-contract` or an equivalent
representative skill and installed only in the candidate `CODEX_HOME` before
cutover.

### Phase 2 exit gate

```yaml
skill_contract_v1_parseable: true
planning_dispatch_v1_parseable: true
planning_runway_v1_parseable: true
planning_closeout_v1_parseable: true
ownership_conflict_detection_proven: true
canonicality_rules_documented: true
skill_authoring_v1_complete: true
skill_authoring_v1_authoritative: true
candidate_generation_still_validation_only: true
```

## Phase 3 — Behavioral Scenario Harness

### Ledger item

`COR-006`.

### Objective

Create topology-independent proof of source and target workflow behavior before
moving ownership.

### Required scenarios

- empty ledger;
- one and multiple eligible findings;
- explicitly requested or missing finding;
- vague mixed-risk finding;
- selected dispatch, queued runway, and active runway;
- invalid or stale state;
- validation and review failure;
- dirty-file conflict;
- partial execution and resume;
- successful closeout;
- same-batch reconciliation;
- no successor selection;
- unsupported legacy discovery;
- triggered test-quality review.

Each scenario asserts initial canonical facts, invoked public command, expected
transition, expected writes, forbidden writes, stop reason, and evidence.

### Exit gate

```yaml
source_characterization_scenarios_green: true
target_scenario_interface_defined: true
scenario_expectations_independent_of_legacy_skill_names: true
active_planning_root_untouched: true
```

## Phase 4 — `add-to-ledger` Ownership Transfer

### Ledger item

`COR-007`.

### Objective

Make `add-to-ledger` the sole owner of intake and canonical ledger mutation.

### Required work

- use `skill-authoring` v1 to migrate `add-to-ledger`;
- implement or complete the narrow ledger-store interface;
- preserve source identity and idempotence;
- remove APR intake and normalization authority;
- remove the `legacy-removal` program-owner escape hatch;
- remove command dependencies and tests that require APR intake ownership.

### Entry gate

```yaml
requires:
  - COR-005 closed
  - COR-006 closed
  - fresh-finding-intake green
  - duplicate-finding-intake green
  - stale-ledger-revision green
```

### Exit gate

```yaml
add_to_ledger:
  owns_intake_decisions: true
  broad_workflow_dependencies: 0
  contract_validates: true
architecture_program_runway:
  intake_decisions_owned: 0
legacy_removal:
  program_owner_escape_hatch: false
```

## Phase 5 — `plan-batch` Ownership Transfer

### Ledger item

`COR-008`.

### Objective

Make `plan-batch` the sole owner of semantic planning and runway specification.

### Required work

- use `skill-authoring` v1 to migrate `plan-batch`;
- move planning references under `skills/plan-batch/references/`;
- produce hybrid dispatch and runway artifacts;
- remove APR grouping, selection, dispatch, and normal queue-preparation authority;
- remove Batch Runway `create-spec` and semantic planning authority;
- rewrite or delete topology tests;
- retain only caller-scoped read-only compatibility required by active artifacts.

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
  contract_validates: true
architecture_program_runway:
  planning_decisions_owned: 0
batch_runway:
  create_spec_callers: 0
  planning_decisions_owned: 0
new_active_artifact_format: hybrid_v1_only
```

## Phase 6 — `work-batch` Ownership Transfer

### Ledger item

`COR-009`.

### Objective

Make `work-batch` the sole owner of execution, recovery, finalization, and
same-batch closeout.

### Required work

- use `skill-authoring` v1 to migrate `work-batch`;
- move execution, recovery, finalization, and retention references under
  `skills/work-batch/references/`;
- retain worker and reviewer as narrow independent agents;
- produce hybrid execution receipts and closeout artifacts;
- remove Batch Runway `execute-spec`, recovery, and finalization authority;
- remove APR `closeout-runway` and same-batch reconciliation authority;
- remove or rewrite topology tests;
- complete or explicitly migrate any active old-format batch before cutover.

### Exit gate

```yaml
work_batch:
  owns_execution_lifecycle: true
  owns_recovery: true
  owns_closeout: true
  owns_same_batch_reconciliation: true
  architecture_program_runway_dependency: false
  batch_runway_dependency: false
  contract_validates: true
batch_runway:
  execute_spec_callers: 0
  execution_decisions_owned: 0
architecture_program_runway:
  closeout_decisions_owned: 0
```

## Phase 7 — Runner and Installation Cutover

### Ledger item

`COR-010`.

### Objective

Make manifests, agents, installation, and the runner consume only public target
commands and narrow mechanisms, then switch toolchain generations safely.

### Required work

- remove APR and Batch Runway from command-owner feature dependencies;
- separate runner installation from APR;
- replace old-mode runner instructions with public plan/work protocols;
- install the full candidate toolchain in the candidate `CODEX_HOME`;
- run complete candidate workflows on controlled fixtures;
- verify rollback to stable installation;
- confirm no selected, queued, active, or resumable old-generation state;
- perform the installation cutover as the final controlled action;
- finish the controlling stable session without switching its loaded generation;
- start a fresh candidate-generation diagnostic after cutover.

### Exit gate

```yaml
command_owner_manifest_legacy_dependencies: 0
runner_prompts_using_old_modes: 0
runner_installation_owned_by_apr_feature: false
candidate_full_fixture_workflow_green: true
no_old_generation_active_state: true
rollback_to_stable_proven: true
fresh_candidate_generation_diagnostic_green: true
default_toolchain_generation: candidate
```

The first real candidate-controlled `plan-batch` invocation may occur only after
this exit gate is satisfied.

## Phase 8 — Legacy Owner Deletion

### Ledger item

`COR-011`.

### Objective

Physically remove broad legacy owners and migration-only topology.

### Required work

- delete `skills/architecture-program-runway/`;
- delete `skills/batch-runway/` after moving surviving references;
- delete old modes, direct-command metadata, topology tests, expired fixtures,
  and expired parsers;
- remove duplicated rules and vocabulary;
- preserve clearly archived historical artifacts without rewriting them;
- run target behavior scenarios after physical deletion.

### Exit gate

```yaml
architecture_program_runway_directory_exists: false
batch_runway_directory_exists: false
active_old_mode_references: 0
tests_requiring_old_owner_presence: 0
active_legacy_artifacts: 0
target_behavioral_scenarios_green: true
```

## Phase 9 — Contract-First Authoring Convergence

### Ledger item

`COR-012`.

### Objective

Audit and refine the already-authoritative `skill-authoring` v1 after dogfooding.
This phase does not create the meta-skill.

### Required work

- audit `port-by-contract`, `add-to-ledger`, `plan-batch`, and `work-batch`;
- collect dogfood findings from ownership-transfer phases;
- integrate compatible improvements to optional fields, report layout, size
  heuristics, reference loading, and non-breaking validation;
- remove temporary authoring exceptions and per-skill dialects;
- require an explicit versioned decision for semantic contract changes.

### Exit gate

```yaml
contract_first_target_skills_consistent: true
temporary_authoring_exceptions: 0
per_skill_contract_dialects: 0
skill_authoring_v1_convergence_audit: passed
```

## Per-Item Planning Requirements

When `plan-batch` selects a redesign item, the dispatch and runway must name:

```yaml
source_work_item: COR-xxx
source_section: docs/design/command-owner-redesign/07-implementation-ledger-intake.md#...
phase: phase-id
satisfies_contracts: []
introduces_target_responsibilities: []
removes_legacy_responsibilities: []
temporary_bridges: []
required_scenarios: []
entry_gate: []
exit_gate: []
rollback_boundary: string
toolchain_generation: stable | candidate
```

Before phase 7 cutover, every real migration dispatch uses
`toolchain_generation: stable`. Candidate-generation work is validation evidence,
not an independently selected real batch.
