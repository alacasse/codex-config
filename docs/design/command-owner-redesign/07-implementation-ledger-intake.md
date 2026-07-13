# Command-Owner Redesign Implementation Ledger Intake

## Purpose

This is the durable source packet for twelve individually addressable work items.
It is not a dispatch, runway, batch map, or slice plan.

`add-to-ledger` has already ingested these items as CCFG-18 through CCFG-29 on
`master`. Future changes amend those existing findings; they do not create new
identities or repeat intake.

## Source and Authority

```yaml
source_ids: COR-001 through COR-012
original_design_snapshot: b3f31c44a1fc3287c33dd2955489f194afef66f6
accepted_design_source: final immutable commit of architecture/command-owner-redesign after post-review amendments
live_intake_commit_on_master: 7356a3fd9d8d487be8562af11cad56170f300616
live_planning_authority:
  - docs/plans/programs/codex-config/CURRENT.md
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md
```

Authoritative links use immutable commit URLs. Mutable branch links are navigation
only.

## Program Rules Inherited by Every Item

- preserve `add-to-ledger -> plan-batch -> work-batch`;
- keep items individually addressable;
- let `plan-batch` shape at most one runnable batch;
- preserve explicit dependencies and stop conditions;
- use stable control and candidate validation generations before cutover;
- record all three roots and the controlling generation;
- remove matching legacy ownership during transfer work;
- name every temporary bridge and deletion condition;
- stop closeout before successor selection;
- do not create permanent `skills-v2`, versioned commands, or parallel execution;
- do not rewrite archived historical artifacts by default.

## Ledger Mapping

| Source | Ledger | Dependencies |
|---|---|---|
| COR-001 | CCFG-18 | None |
| COR-002 | CCFG-19 | CCFG-18 |
| COR-003 | CCFG-20 | CCFG-19 |
| COR-004 | CCFG-21 | CCFG-19 |
| COR-005 | CCFG-22 | CCFG-20; relevant CCFG-21 schemas only for optional planning-artifact reference |
| COR-006 | CCFG-23 | CCFG-21 and CCFG-22 |
| COR-007 | CCFG-24 | CCFG-22 and CCFG-23 |
| COR-008 | CCFG-25 | CCFG-24 and resolved planning transaction |
| COR-009 | CCFG-26 | CCFG-25 |
| COR-010 | CCFG-27 | CCFG-26 |
| COR-011 | CCFG-28 | CCFG-27 |
| COR-012 | CCFG-29 | CCFG-28 |

---

## COR-001 / CCFG-18 — Establish Stable and Candidate Generations

### Purpose

Establish and prove a stable control plane capable of planning and executing work
against a separate candidate clone without loading candidate contracts, writing
planning state to the wrong checkout, or allowing candidate sessions to control
real planning state.

### Included scope

- fingerprint stable checkout, commit, default `CODEX_HOME`, and resolved links;
- declare:
  - `toolchain_source_root`;
  - `canonical_planning_repository_root`;
  - `canonical_planning_root`;
  - `implementation_target_root`;
  - `candidate_codex_home`;
- create candidate clone from latest authoritative `master`;
- create implementation branch;
- merge the accepted design history with preserved ancestry;
- verify imported design tree before amendments;
- freeze design branch as provenance after integration;
- create candidate `CODEX_HOME`;
- add narrow temporary cross-checkout root/generation enforcement;
- resolve stable helpers, references, schemas, workers, and reviewers from the
  stable toolchain root;
- run code operations and implementation commits under the candidate root;
- keep planning reads/writes under the stable canonical root;
- produce cross-repository receipts;
- prove worker/reviewer generation identity;
- prove candidate fixture-only validation and canonical-write rejection;
- inventory old selected, queued, active, and resumable state;
- prove pre-cutover rollback.

### Excluded scope

- no command-owner migration;
- no `skill-contract/v1` implementation;
- no `CURRENT.md` or ledger format migration;
- no candidate-controlled canonical planning write;
- no default generation switch;
- no APR or Batch Runway deletion;
- no ownership transfer;
- no parallel execution.

### Acceptance evidence

```yaml
stable_control:
  checkout_on_authoritative_master: true
  toolchain_commit_recorded: true
  default_codex_home_recorded: true
  required_links_resolve_to_one_stable_generation: true
root_topology:
  all_three_roots_explicit: true
  cwd_inference_required: false
  planning_write_outside_canonical_root_rejected: true
  implementation_write_outside_candidate_root_rejected: true
candidate_branch:
  based_on_latest_authoritative_master: true
  accepted_design_history_merged: true
  imported_design_tree_verified: true
candidate_installation:
  separate_codex_home: true
  fresh_fixture_only_session_green: true
  canonical_planning_mutation_rejected: true
cross_checkout_control:
  stable_helper_resolution_independent_of_candidate_cwd: true
  worker_generation_matches_controller: true
  reviewer_generation_matches_controller: true
  planning_and_implementation_receipts_distinct: true
quiescence:
  selected: null
  queued: null
  active: null
  resumable_old_runner_state: false
rollback:
  stable_restore_rehearsal_green: true
  candidate_canonical_write_occurred: false
```

### Stop boundary

- stop before consuming changed stable control code in the same session;
- stop if sandbox cannot distinguish both repositories;
- stop if stable helper resolves from candidate checkout;
- stop if candidate can mutate canonical planning state;
- stop after same-batch closeout without selecting CCFG-19.

---

## COR-002 / CCFG-19 — Verify Source Contracts and Resolve Blocking Decisions

### Purpose

Complete source behavior verification and resolve decisions that block schemas,
state transitions, and ownership transfer.

### Included scope

- contract-to-source, owner, and scenario matrix;
- source-versus-accidental-structure classification;
- schema evolution and unknown-field policy;
- narrow `ledger-store` apply-only contract;
- runner public-command and no-successor-readiness boundary;
- generation and branch topology verification;
- multi-artifact planning transaction decision or explicit blocker;
- test classification;
- remaining user decisions recorded rather than guessed.

### Acceptance

```yaml
contract_to_owner_map_complete: true
contract_to_scenario_map_complete: true
blocking_ownership_conflicts: 0
schema_evolution_policy_accepted: true
ledger_store_boundary_accepted: true
runner_target_protocol_accepted: true
planning_transaction_ready_or_explicitly_blocked: true
```

---

## COR-003 / CCFG-20 — Implement `skill-contract/v1` Schema and Validators

### Purpose

Implement the hybrid skill schema, audience profiles, and deterministic
validators.

### Included scope

- exactly-one contract block;
- required fields and audience profiles;
- ownership, delegation, dependency, and reference validation;
- reference-root and cycle validation;
- schema evolution;
- generation/source identity;
- deterministic migration guards;
- explicit limit: no claim to semantically understand arbitrary prose.

### Acceptance

```yaml
schema_green: true
ownership_conflict_tests_green: true
delegation_reference_tests_green: true
schema_compatibility_tests_green: true
deterministic_migration_guard_green: true
```

---

## COR-004 / CCFG-21 — Implement Planning Artifact Schemas and Validators

### Purpose

Implement and prototype canonical active planning formats.

### Included scope

- `planning-current/v1` in one canonical `CURRENT.md` block;
- `planning-finding/v1` per finding in `LEDGER.md`;
- derived index validation;
- comparison with one global ledger block;
- `planning-dispatch/v1`, `planning-runway/v1`, `planning-closeout/v1`;
- expected revision and file hash;
- atomic replace and receipts;
- generation identity and lineage;
- old-format read-only compatibility when active state requires it;
- fault injection;
- multi-artifact planning transaction decision or blocker.

### Acceptance

```yaml
current_schema_and_atomicity_green: true
finding_schema_and_multi_item_atomicity_green: true
per_finding_default_confirmed_or_superseded: true
dispatch_runway_closeout_schemas_green: true
lineage_generation_validation_green: true
fault_injection_green: true
```

---

## COR-005 / CCFG-22 — Finalize and Validate `skill-authoring` v1

### Dependencies

Hard dependency: CCFG-20.

CCFG-21 is required only for the conditionally loaded planning-artifact reference
and only for the schema versions that reference claims to support.

### Purpose

Create one complete authoritative hybrid-skill authoring workflow.

### Included scope

- contract extraction;
- ownership and ambiguity reporting;
- procedure, branches, rationale, and reference separation;
- deterministic migration guards;
- generic skill-writing boundary;
- one conditionally loaded planning-artifact reference under the same v1;
- narrow evidence/analysis skill trial;
- branching command-like skill trial.

### Acceptance

```yaml
core_complete: true
one_skill_path: true
one_contract_version: true
narrow_skill_trial_green: true
branching_command_trial_green: true
planning_reference_declares_supported_schemas: true
unsupported_schema_blocks: true
candidate_only_installation_green: true
runtime_dependency_from_command_owners: false
```

---

## COR-006 / CCFG-23 — Build the Topology-Independent Behavioral Harness

### Purpose

Prove behavior independently from legacy owners and exact prose.

### Required families

- intake and multi-item idempotence;
- planning and scope guards;
- execution, validation, review, commit, recovery, resume;
- closeout and no successor;
- three-root and generation isolation;
- branch lineage and candidate fixture-only behavior;
- planning, commit, and closeout fault injection;
- installer, switch, and rollback;
- physical deletion and historical readability;
- contract ID coverage report.

### Acceptance

```yaml
source_characterization_green: true
target_interfaces_green: true
bootstrap_cutover_green: true
fault_injection_green: true
contract_coverage_complete: true
legacy_topology_not_required: true
```

---

## COR-007 / CCFG-24 — Transfer Intake Ownership to `add-to-ledger`

### Purpose

Make `add-to-ledger` the sole owner of intake and canonical ledger mutation
semantics.

### Same-work removal

- APR intake and normalization authority;
- APR normal ledger mutation route;
- `legacy-removal` program-owner escape hatch.

### Acceptance

- multi-item atomic intake;
- source identity and idempotence;
- stale revision refusal;
- no selection or runway;
- no broad owner dependency.

---

## COR-008 / CCFG-25 — Transfer Planning Ownership to `plan-batch`

### Purpose

Make `plan-batch` the sole owner of selection, scope shaping, dispatch, runway,
risk, approvals, and validation profiles.

### Same-work removal

- APR grouping, ranking, selection, dispatch, and queue preparation;
- Batch Runway `create-spec` semantic ownership.

### Acceptance

- resolved planning transaction;
- exactly one runnable runway;
- stale lineage and partial failure recovery;
- no broad owner dependency;
- planning stops before implementation.

---

## COR-009 / CCFG-26 — Transfer Execution and Closeout Ownership to `work-batch`

### Purpose

Make `work-batch` the sole owner of execution, recovery, validation acceptance,
review coordination, commits, finalization, closeout, and same-batch
reconciliation.

### Same-work removal

- Batch Runway `execute-spec`, recovery, and finalization ownership;
- APR closeout and reconciliation ownership.

### Acceptance

- worker/reviewer contracts no longer depend on Batch Runway paths;
- commit/receipt and partial-closeout recovery;
- old-format active-state policy;
- no successor selection;
- no broad owner dependency.

---

## COR-010 / CCFG-27 — Prepare and Rehearse Candidate Cutover

### Purpose

Make candidate cutover-ready without changing the default generation.

### Included scope

- runner public protocols only;
- remove successor-readiness interpretation;
- manifests, agents, result contracts, and installer independent of old paths;
- clean generation install from empty directory;
- omitted feature and stale-link removal;
- atomic switch rehearsal;
- rollback checkpoint and rehearsal;
- fresh candidate fixture workflows;
- default generation remains stable;
- legacy source directories may remain but are not installed normal routes.

### Acceptance

```yaml
default_generation_switched: false
command_owner_legacy_dependencies: 0
runner_old_modes: 0
runner_successor_readiness_decisions: 0
agent_legacy_path_dependencies: 0
clean_install_rehearsal_green: true
legacy_routes_installed: 0
atomic_switch_rehearsal_green: true
rollback_rehearsal_green: true
candidate_fixture_workflow_green: true
canonical_candidate_writes: 0
```

---

## COR-011 / CCFG-28 — Remove Legacy Owners and Commit Final Cutover

### Purpose

Delete APR and Batch Runway from candidate source, prove clean absence, switch the
default generation, validate it read-only, close CCFG-28 under the pinned stable
controller, and stop.

### Included scope

- physical deletion;
- removal of old modes, topology-only tests, expired fixtures and parsers;
- reproducible active/historical scan;
- clean install and negative direct invocation;
- full validation and archived-history proof;
- final checkpoint;
- atomic default switch;
- fresh candidate read-only diagnostic;
- stable same-batch closeout and stop.

### Acceptance

```yaml
legacy_directories_absent: true
legacy_installed_routes: 0
legacy_commands_callable: false
target_and_full_tests_green: true
atomic_switch_green: true
fresh_candidate_read_only_diagnostic_green: true
stable_controller_generation_unchanged: true
stable_same_batch_closeout_complete: true
stable_controller_stopped: true
candidate_canonical_write_before_new_batch: false
resulting_selected_queued_active: null
```

---

## COR-012 / CCFG-29 — Contract-First Convergence and Final Integration

### Purpose

Converge one contract-first dialect and restore one integrated long-term source on
`master`.

### Included scope

- audit migrated skills and planning references;
- integrate compatible dogfood refinements;
- remove temporary authoring exceptions;
- merge implementation branch into latest `master` at quiescent state;
- verify target toolchain content and contracts after merge;
- rebind default `CODEX_HOME` to `master`;
- run fresh master-bound validation;
- remove temporary cross-checkout bridge;
- retire candidate and design branches when safe.

### Acceptance

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

## Intake and Planning Boundary

All items remain unselected until a future explicit `plan-batch` invocation.
Planning may split or narrow an item when its current scope cannot form one safe
batch. It must preserve source identity, dependencies, and deferred work.
