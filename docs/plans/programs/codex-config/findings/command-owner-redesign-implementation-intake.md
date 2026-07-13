# Command-Owner Redesign Implementation Intake

## Source

```yaml
source_identity: COR-001 through COR-012
original_design_snapshot: b3f31c44a1fc3287c33dd2955489f194afef66f6
accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
initial_intake_commit: 7356a3fd9d8d487be8562af11cad56170f300616
state: CCFG-18 candidate-generation runway queued; CCFG-19 remains unselected
```

- Accepted immutable design packet:
  `https://github.com/alacasse/codex-config/tree/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign`
- Accepted implementation intake source:
  `https://github.com/alacasse/codex-config/blob/caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c/docs/design/command-owner-redesign/07-implementation-ledger-intake.md`
- Live bootstrap decisions:
  `command-owner-redesign-bootstrap-decisions.md`
- Mutable branch links are navigation only and carry no independent authority.

## Intake Boundary

This note preserves twelve individually addressable program findings. It is not a
batch map, dispatch, runway, slice list, or implementation plan.

A future `plan-batch` retains authority to select, split, narrow, group, block, or
defer at most one eligible finding from current ledger state.

Every item inherits these constraints:

- use accepted decisions and phase order;
- preserve behavior contracts rather than legacy topology;
- keep stable generation in control before cutover;
- record toolchain, planning, and implementation roots;
- finalize `skill-authoring` before command-owner migrations;
- remove corresponding legacy ownership in transfer work;
- name every temporary bridge and deletion condition;
- stop after same-batch closeout without selecting successor work;
- do not add permanent parallel commands, `skills-v2`, or parallel execution.

## Ledger Mapping

| Source | Ledger | Dependencies |
|---|---|---|
| COR-001 | CCFG-18 | None |
| COR-002 | CCFG-19 | CCFG-18 |
| COR-003 | CCFG-20 | CCFG-19 |
| COR-004 | CCFG-21 | CCFG-19 |
| COR-005 | CCFG-22 | CCFG-20; relevant CCFG-21 schemas only for optional planning reference |
| COR-006 | CCFG-23 | CCFG-21 and CCFG-22 |
| COR-007 | CCFG-24 | CCFG-22 and CCFG-23 |
| COR-008 | CCFG-25 | CCFG-24 and resolved planning transaction |
| COR-009 | CCFG-26 | CCFG-25 |
| COR-010 | CCFG-27 | CCFG-26 |
| COR-011 | CCFG-28 | CCFG-27 |
| COR-012 | CCFG-29 | CCFG-28 |

## COR-001 / CCFG-18 — Establish Stable and Candidate Generations

### Purpose

Establish and prove a stable control plane capable of planning and executing
migration work against a separate candidate clone without loading candidate
contracts, writing planning state to the wrong checkout, or allowing candidate
sessions to control real planning state.

### Live pre-creation amendment

The strict `cross-checkout-context/v1` contract is post-creation only: it
requires `implementation_target_root` to be an existing Git repository at the
declared `implementation_commit_before`. CCFG-18 requires that repository to be
created during execution, while `plan-batch` cannot create it during planning.

Preserve the strict contract unchanged and add the separate temporary
`cross-checkout-precreation/v1` interface defined in
`command-owner-redesign-bootstrap-decisions.md`. It binds the existing stable
generation and canonical planning revision to absent intended candidate paths,
the authoritative base commit, implementation branch, accepted design snapshot,
and exact creation authority. It grants no workflow lifecycle authority and
does not require a candidate commit before the repository exists.

After repository lineage and candidate environment creation are verified,
execution must emit a versioned transition receipt and validate the existing
strict `cross-checkout-context/v1` before any further implementation work.

### Included

- fingerprint stable checkout, commit, default `CODEX_HOME`, and resolved links;
- declare toolchain, canonical planning, and implementation roots;
- implement and validate `cross-checkout-precreation/v1` in a single-root stable
  control batch, then install and reload it in a fresh stable session;
- create candidate clone from latest authoritative `master`;
- create implementation branch;
- merge accepted design history ending at `caf343a...` with preserved ancestry;
- verify imported design tree before amendments;
- freeze the design branch as provenance after integration;
- create separate candidate `CODEX_HOME`;
- preserve strict `cross-checkout-context/v1` post-creation enforcement and
  transition to it after candidate lineage and environment establishment;
- resolve stable helpers, references, schemas, workers, and reviewers from the
  stable toolchain root;
- execute code operations and commits under the candidate root;
- keep planning reads and writes under the stable canonical root;
- produce cross-repository receipts;
- prove worker/reviewer generation identity;
- prove candidate fixture-only validation and canonical-write rejection;
- inventory selected, queued, active, and resumable old-generation state;
- prove pre-cutover rollback.

### Excluded

- no command-owner migration;
- no `skill-contract/v1` implementation;
- no planning-format migration;
- no candidate-controlled canonical write;
- no default generation switch;
- no APR or Batch Runway deletion;
- no ownership transfer;
- no parallel execution.

### Acceptance

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
  precreation_interface: cross-checkout-precreation/v1
  strict_postcreation_interface: cross-checkout-context/v1
  strict_repository_and_revision_validation_preserved: true
  absent_candidate_paths_validated_before_creation: true
  exact_candidate_creation_targets_only: true
  authoritative_base_commit_recorded: true
  accepted_design_snapshot_recorded: true
  versioned_transition_receipt_green: true
  strict_context_validated_before_further_implementation: true
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
- stop if pre-creation support weakens `cross-checkout-context/v1`;
- stop if the stable pre-creation support batch creates either candidate path;
- stop after that stable-support closeout until installation and fresh-session
  reload complete;
- stop if sandbox cannot distinguish both repositories;
- stop if stable helper resolves from candidate checkout;
- stop if candidate can mutate canonical planning state;
- stop after same-batch closeout without selecting CCFG-19.

The accepted design package at
`caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` remains immutable. After candidate
lineage is verified, the implementation branch must receive this same
pre-creation amendment as an explicit live amendment before design evolution
continues.

## COR-002 / CCFG-19 — Verify Source Contracts and Resolve Blocking Decisions

Purpose: complete contract-to-source, owner, and scenario mapping and resolve
schema evolution, ledger-store, runner, and planning-transaction decisions that
block implementation.

Acceptance:

```yaml
contract_to_owner_map_complete: true
contract_to_scenario_map_complete: true
blocking_ownership_conflicts: 0
schema_evolution_policy_accepted: true
ledger_store_boundary_accepted: true
runner_target_protocol_accepted: true
planning_transaction_ready_or_explicitly_blocked: true
```

## COR-003 / CCFG-20 — Implement `skill-contract/v1` Schema and Validators

Purpose: implement exactly-one contract parsing, audience profiles, ownership,
delegation, reference, dependency, compatibility, and deterministic migration
validation without claiming arbitrary prose understanding.

Acceptance:

```yaml
schema_green: true
ownership_conflict_tests_green: true
delegation_reference_tests_green: true
schema_compatibility_tests_green: true
deterministic_migration_guard_green: true
```

## COR-004 / CCFG-21 — Implement Planning Artifact Schemas and Validators

Purpose: implement and prototype canonical `CURRENT.md`, per-finding ledger,
dispatch, runway, and closeout contracts with expected revisions, file hashes,
atomic replace, receipts, lineage, generation identity, old-format read-only
compatibility when required, and fault injection.

Acceptance:

```yaml
current_schema_and_atomicity_green: true
finding_schema_and_multi_item_atomicity_green: true
per_finding_default_confirmed_or_superseded: true
dispatch_runway_closeout_schemas_green: true
lineage_generation_validation_green: true
fault_injection_green: true
```

## COR-005 / CCFG-22 — Finalize and Validate `skill-authoring` v1

Hard dependency: CCFG-20.

CCFG-21 is required only for the conditionally loaded planning-artifact reference
and only for schema versions that reference supports.

Purpose: create one authoritative core, a conditional planning-artifact reference,
a narrow evidence/analysis skill trial, and a branching command-like skill trial.

Acceptance:

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

## COR-006 / CCFG-23 — Build the Topology-Independent Behavioral Harness

Purpose: prove intake, planning, execution, closeout, generation/root isolation,
branch lineage, partial-failure recovery, clean install, cutover, rollback,
deletion, historical readability, and contract-ID coverage independently of old
skill topology.

Acceptance:

```yaml
source_characterization_green: true
target_interfaces_green: true
bootstrap_cutover_green: true
fault_injection_green: true
contract_coverage_complete: true
legacy_topology_not_required: true
```

## COR-007 / CCFG-24 — Transfer Intake Ownership to `add-to-ledger`

Purpose: make `add-to-ledger` sole owner of intake and canonical ledger mutation
semantics while removing APR intake/normalization and the legacy-removal
program-owner escape hatch in the same work.

Acceptance includes multi-item atomic intake, source identity, idempotence, stale
revision refusal, no selection, and no broad owner dependency.

## COR-008 / CCFG-25 — Transfer Planning Ownership to `plan-batch`

Purpose: make `plan-batch` sole owner of selection, scope, dispatch, runway, risk,
approvals, and validation profiles while removing APR planning and Batch Runway
create-spec semantics.

Requires CCFG-24 and a resolved planning transaction.

## COR-009 / CCFG-26 — Transfer Execution and Closeout Ownership to `work-batch`

Purpose: make `work-batch` sole owner of execution, recovery, validation,
review, commit, finalization, closeout, and reconciliation while removing Batch
Runway execute-spec and APR closeout semantics.

Acceptance includes worker/reviewer independence from legacy paths, commit/receipt
recovery, partial-closeout recovery, old-format active-state policy, and no
successor selection.

## COR-010 / CCFG-27 — Prepare and Rehearse Candidate Cutover

Purpose: make candidate cutover-ready without changing the default generation.

Included:

- runner public protocols only and no successor-readiness decision;
- manifests, agents, result contracts, and installer independent of old paths;
- clean generation install from empty directory;
- omitted feature and stale-link removal;
- atomic switch rehearsal;
- rollback checkpoint and rehearsal;
- candidate fixture workflow;
- default generation remains stable;
- legacy directories may still exist but are not installed routes.

Acceptance:

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

## COR-011 / CCFG-28 — Remove Legacy Owners and Commit Final Cutover

Purpose: delete APR and Batch Runway from candidate source, prove clean absence,
switch the default generation, obtain a fresh candidate read-only diagnostic,
close CCFG-28 under the already-loaded stable controller, and stop.

Acceptance:

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

## COR-012 / CCFG-29 — Contract-First Convergence and Final Integration

Purpose: converge one contract-first dialect and restore one integrated long-term
source on `master`.

Included:

- audit migrated skills and planning references;
- compatible dogfood refinements;
- remove temporary authoring exceptions;
- merge implementation branch into latest `master` at quiescent state;
- verify target toolchain content after merge;
- rebind default `CODEX_HOME` to `master`;
- fresh master-bound validation;
- remove temporary cross-checkout bridge;
- retire candidate and design branches when safe.

Acceptance:

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

## No Selection Performed

This amendment changes scope, dependencies, and acceptance criteria only. No
redesign item is selected, queued, active, implemented, or closed.
