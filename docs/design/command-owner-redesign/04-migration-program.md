# Migration Program

## Program Contract

```yaml
schema: command-owner-migration-program/v2
repository: alacasse/codex-config
original_design_snapshot: b3f31c44a1fc3287c33dd2955489f194afef66f6
live_intake_commit_on_master: 7356a3fd9d8d487be8562af11cad56170f300616
work_items:
  - CCFG-18
  - CCFG-19
  - CCFG-20
  - CCFG-21
  - CCFG-22
  - CCFG-23
  - CCFG-24
  - CCFG-25
  - CCFG-26
  - CCFG-27
  - CCFG-28
  - CCFG-29
execution_policy:
  one_selected_batch: true
  one_toolchain_generation_per_batch: true
  future_item_selection_during_closeout: forbidden
  permanent_parallel_skill_catalog: forbidden
```

The work items are durable ledger findings, not preselected batches. `plan-batch`
retains authority to split, narrow, block, group, or defer one eligible item.

## Program Rules

- Use `add-to-ledger -> plan-batch -> work-batch`.
- Every batch records the controlling generation and all three roots.
- Planning state remains canonical on `master` before cutover.
- Candidate code lives in a separate clone.
- Candidate sessions are fixture-only before cutover.
- An ownership-transfer batch removes the matching legacy decision route.
- Every temporary bridge has a deletion condition.
- No real batch crosses controlling generations.
- Cutover occurs only at quiescent state.
- Rollback after candidate canonical writes restores one compatible bundle.
- Same-batch closeout stops before successor planning.

## Pre-Plan Gate for CCFG-18

Before invoking `plan-batch CCFG-18`, perform only these manual and documentary
checks:

```yaml
stable_checkout:
  branch: master
  contains_current_intake: true
  clean_or_classified: true
installed_generation:
  default_codex_home_resolves_to_stable_checkout: true
  required_skills_resolve_to_one_stable_commit: true
  candidate_links: 0
planning_state:
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  resumable_runner_state: false
project_values:
  stable_checkout_path: known
  candidate_clone_path: known
  candidate_codex_home_path: known
  accepted_design_commit: known
```

The clone, implementation branch, candidate `CODEX_HOME`, bridge, and mechanical
generation fingerprint belong inside CCFG-18. Requiring them before planning
would be circular.

## CCFG-18 — Establish Stable and Candidate Generations

### Objective

Establish and prove a stable control plane that can plan and execute migration
work against a separate candidate clone without loading candidate contracts,
writing planning state into the wrong repository, or allowing candidate sessions
to control real planning state.

### Included scope

- record stable checkout, commit, default `CODEX_HOME`, and resolved installed
  links;
- declare `toolchain_source_root`, `canonical_planning_repository_root`, and
  `implementation_target_root`;
- create the candidate clone from latest authoritative `master`;
- create an implementation branch;
- merge the accepted design history with preserved ancestry;
- verify the imported design tree before further amendments;
- freeze the design branch as provenance after integration;
- create a separate candidate `CODEX_HOME`;
- implement narrow temporary cross-checkout root and generation enforcement;
- resolve controlling scripts, references, schemas, workers, and reviewers from
  the stable toolchain root;
- run implementation operations, validation, Git diff, and commits under the
  candidate root;
- keep planning reads/writes under the canonical stable root;
- produce cross-repository receipts;
- prove worker and reviewer generation identity;
- prove a fresh candidate session is fixture-only and cannot mutate canonical
  planning state;
- inventory selected, queued, active, and resumable old-generation state;
- prove pre-cutover rollback.

### Excluded scope

- no command-owner migration;
- no `skill-contract/v1` implementation;
- no active planning format migration;
- no candidate-controlled real planning mutation;
- no default `CODEX_HOME` switch;
- no APR or Batch Runway deletion;
- no ownership change;
- no parallel execution.

### Fresh-session boundary

If stable control code must be changed, stop before consuming it. Resume in a
fresh stable session that verifies the new stable generation.

### Exit gate

```yaml
stable_control:
  one_stable_generation_proven: true
  helper_resolution_independent_of_candidate_cwd: true
root_topology:
  all_three_roots_explicit: true
  planning_write_outside_canonical_root_rejected: true
  implementation_write_outside_candidate_root_rejected: true
candidate_branch:
  based_on_latest_master: true
  accepted_design_history_merged: true
  design_tree_verified: true
candidate_installation:
  separate_codex_home: true
  fixture_only_session_green: true
  canonical_mutation_rejected: true
cross_checkout:
  worker_generation_matches_controller: true
  reviewer_generation_matches_controller: true
  receipts_distinguish_planning_and_implementation_revisions: true
quiescence:
  selected: null
  queued: null
  active: null
  resumable_old_runner_state: false
rollback:
  stable_restore_rehearsal_green: true
  candidate_canonical_write_occurred: false
```

Stop after CCFG-18 closeout without selecting CCFG-19.

## CCFG-19 — Verify Source Contracts and Resolve Blocking Decisions

### Objective

Complete source behavior verification and resolve decisions that block schemas,
state transitions, and ownership transfer.

### Required work

- map every behavior contract to source evidence, target owner, and scenario;
- verify the three-root model against current scripts, agents, installer, and
  runner;
- resolve or explicitly gate the multi-artifact planning transaction;
- define schema compatibility and unknown-field policy;
- define the narrow `ledger-store` apply-only contract;
- define runner removal of successor-readiness semantics;
- classify current tests as behavioral, schema, integration, migration-retention,
  topology, text-contract, or historical;
- keep unresolved non-blocking module and naming choices explicit.

### Exit gate

```yaml
contract_to_owner_map_complete: true
contract_to_scenario_map_complete: true
blocking_ownership_conflicts: 0
schema_evolution_policy_accepted: true
ledger_store_boundary_accepted: true
runner_target_protocol_accepted: true
planning_transaction_decision_ready_for_CCFG_21_or_explicitly_blocked: true
```

## CCFG-20 — Implement `skill-contract/v1` and Validators

### Objective

Implement the stable hybrid skill schema and deterministic validators.

### Required work

- schema parsing and exactly-one-block enforcement;
- audience profiles;
- ownership, delegation, dependency, and reference validation;
- controlled canonicality checks;
- schema evolution and unknown-field behavior;
- generation/source identity fields;
- deterministic cosmetic-migration guards limited to known evidence:
  - broad-owner dependency remains;
  - ownership did not move;
  - durable facts are explicitly duplicated;
  - skill was renamed without contract change.

### Forbidden work

Do not claim semantic understanding of arbitrary prose.

### Exit gate

```yaml
skill_contract_v1_schema_green: true
ownership_conflict_tests_green: true
delegation_and_reference_tests_green: true
schema_compatibility_tests_green: true
deterministic_migration_guard_green: true
```

## CCFG-21 — Implement Planning Artifact Schemas and Validators

### Objective

Implement and prototype `planning-current/v1`, `planning-finding/v1`,
`planning-dispatch/v1`, `planning-runway/v1`, and `planning-closeout/v1`.

### Required work

- canonical block parsing and rendering;
- expected revision and file-hash checks;
- atomic replace and receipts;
- per-finding ledger prototype versus one global block;
- derived index validation;
- dispatch/runway/closeout lineage;
- producer generation identity;
- compatibility readers for active old-format state when explicitly required;
- fault-injection around current and ledger writes;
- explicit decision or blocker for the dispatch -> selected -> runway -> queued
  transaction.

### Exit gate

```yaml
current_schema_green: true
finding_schema_green: true
dispatch_schema_green: true
runway_schema_green: true
closeout_schema_green: true
current_atomicity_and_rollback_green: true
ledger_multi_item_atomicity_green: true
per_finding_default_confirmed_or_superseded_by_decision: true
lineage_and_generation_validation_green: true
```

## CCFG-22 — Finalize and Validate `skill-authoring` v1

### Dependency

Hard dependency: CCFG-20.

Full closure of CCFG-21 is not required for the core. The conditionally loaded
planning-artifact reference may be added when the relevant planning schemas are
accepted.

### Objective

Create one complete authoritative `skill-authoring` v1 for hybrid skills.

### Required work

- contract extraction;
- ownership conflict reporting;
- procedure, branch, rationale, and reference separation;
- migration guards;
- generic skill-writing boundary;
- conditionally loaded planning-artifact authoring reference with declared
  supported schemas;
- trial on one narrow evidence/analysis skill;
- trial on one branching command-like skill.

### Exit gate

```yaml
skill_authoring_core_complete: true
single_skill_path_and_contract_version: true
narrow_skill_trial_green: true
branching_command_trial_green: true
planning_reference_blocks_on_unsupported_schema: true
runtime_dependency_from_command_owners: false
candidate_only_installation_green: true
```

## CCFG-23 — Build the Behavioral Scenario Harness

### Objective

Create topology-independent proof of source and target behavior.

### Required scenario families

- intake and idempotence;
- planning selection and scope guards;
- execution, validation, review, commit, recovery, and resume;
- closeout, reconciliation, and no successor;
- root and generation isolation;
- candidate write rejection;
- branch lineage and immutable design import;
- child-process generation inheritance;
- partial planning transactions;
- commit/receipt mismatch;
- partial closeout and idempotent retry;
- clean installation, partial install failure, stale links, atomic switch, and
  rollback;
- physical deletion and archived-history readability.

### Exit gate

```yaml
source_characterization_green: true
target_interface_scenarios_green: true
bootstrap_and_cutover_scenarios_green: true
fault_injection_scenarios_green: true
contract_id_coverage_report_complete: true
legacy_skill_names_not_required_except_migration_fixtures: true
```

## CCFG-24 — Transfer Intake Ownership

Make `add-to-ledger` the sole intake and ledger-mutation decision owner.

Same-phase removals:

- APR intake and normalization authority;
- APR normal ledger mutation route;
- `legacy-removal` program-owner exception.

Requires CCFG-22 and CCFG-23.

Completion requires multi-item atomic intake, duplicate and idempotence behavior,
stale revision refusal, and no selection.

## CCFG-25 — Transfer Planning Ownership

Make `plan-batch` the sole owner of selection, shaping, dispatch, runway, risk,
approval, and validation-profile decisions.

Same-phase removals:

- APR grouping, ranking, selection, dispatch, and queue-preparation ownership;
- Batch Runway `create-spec` semantic ownership.

Requires CCFG-24 and resolved multi-artifact planning transaction.

## CCFG-26 — Transfer Execution and Closeout Ownership

Make `work-batch` the sole owner of execution, recovery, validation acceptance,
review coordination, commits, finalization, closeout, and same-batch
reconciliation.

Same-phase removals:

- Batch Runway `execute-spec`, recovery, and finalization ownership;
- APR `closeout-runway` and reconciliation ownership.

Requires CCFG-25. Worker/reviewer result schemas and references must no longer
require Batch Runway paths.

## CCFG-27 — Prepare and Rehearse Candidate Cutover

### Objective

Make the candidate completely cutover-ready without changing the default
generation and without requiring physical deletion of legacy source directories.

### Included work

- runner uses public plan/work protocols only;
- runner no longer interprets successor readiness;
- manifests, agents, schemas, result contracts, and installer no longer require
  APR or Batch Runway paths;
- create a clean generation-specific `CODEX_HOME` from an empty directory;
- omitted features and stale links are removed;
- rehearse atomic default switch and rollback;
- generate checkpoint bundle;
- run fresh candidate fixture workflows;
- keep candidate sessions validation-only;
- keep default generation stable.

### Exit gate

```yaml
default_generation_switched: false
command_owner_legacy_dependencies: 0
runner_old_modes: 0
runner_successor_readiness_decisions: 0
agent_legacy_path_dependencies: 0
clean_candidate_install_green: true
legacy_routes_installed: 0
atomic_switch_rehearsal_green: true
rollback_rehearsal_green: true
fresh_candidate_fixture_workflow_green: true
canonical_candidate_writes: 0
quiescence_protocol_green: true
```

## CCFG-28 — Remove Legacy Owners and Commit Final Cutover

### Objective

Delete APR and Batch Runway from the candidate implementation, prove their
absence in a clean installation, then switch the default generation.

### Included work

- physical deletion of legacy skill directories;
- removal of old modes, topology-only tests, expired fixtures and parsers;
- reproducible active-surface and stale-link scan;
- clean installation from empty directory;
- direct old-command invocation negative tests;
- full target and repository validation;
- archived-history readability and non-pickup proof;
- final checkpoint;
- atomic default `CODEX_HOME` switch;
- fresh candidate read-only diagnostic;
- same-batch closeout under the already-loaded stable controller;
- stable controller stop.

### Cutover transaction

```yaml
controlling_generation: stable_pinned_session
after_default_switch_before_closeout:
  candidate_session_authority: validation_only
  candidate_canonical_writes: forbidden
  stable_controller_may:
    - consume_candidate_diagnostic
    - rollback_default_binding_on_failure
    - close_and_reconcile_CCFG_28
    - stop
  stable_controller_forbids:
    - reload_default_skills
    - spawn_new_worker_or_reviewer
    - select_successor
cutover_committed_when:
  - candidate_diagnostic_green
  - CCFG_28_closeout_complete
  - stable_controller_stopped
```

The first candidate-controlled canonical write begins in a new batch.

## CCFG-29 — Authoring Convergence and Final Repository Integration

### Objective

Converge contract-first authoring and restore one integrated long-term repository
and toolchain source.

### Included work

- audit migrated skills for one v1 dialect;
- integrate compatible dogfood refinements;
- remove temporary authoring exceptions;
- merge implementation branch into latest `master` at quiescent state;
- resolve any planning-only master movement explicitly;
- prove candidate toolchain content and contracts survived integration;
- rebind default `CODEX_HOME` to the integrated master checkout;
- run a fresh session and behavior smoke test;
- remove temporary cross-checkout bridge;
- retire candidate and design branches when provenance remains reachable.

### Exit gate

```yaml
one_contract_first_dialect: true
temporary_authoring_exceptions: 0
implementation_merged_into_master: true
default_toolchain_source_is_master: true
fresh_master_bound_session_green: true
cross_checkout_bridge_removed: true
candidate_branch_retired_or_frozen: true
selected: null
queued: null
active: null
```

## Temporary Bridge Record

```yaml
bridge:
  id: stable-id
  caller: exact-caller
  reason: concrete-migration-need
  owner: work-item-or-batch
  allowed_scope: []
  introduced_in: commit-or-batch
  deletion_condition: []
  status: proposed | active | removed
```

A bridge without these fields is an architectural defect.

## Rollback Boundaries

### Before first candidate canonical write

Installation rollback is allowed only when no candidate-format canonical state or
candidate selected/queued/active work exists.

### After first candidate canonical write

Restore together:

- installation;
- toolchain code;
- canonical planning state;
- active artifacts;
- required run and transition state.

Changing only symlinks or `CODEX_HOME` is forbidden.

## Final Program Completion

The program is complete only when:

- command owners own their intended workflows;
- APR and Batch Runway are physically absent and uncallable;
- runner and mechanisms remain narrow;
- target scenarios pass;
- `master` contains integrated target code and canonical planning state;
- default toolchain resolves to `master`;
- temporary bridges and compatibility readers are removed;
- no successor work was selected during the final closeout.
