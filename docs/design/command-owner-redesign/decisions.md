# Decision Register

## Purpose

This register separates accepted target decisions from superseded, open,
deferred, and rejected alternatives.

Authority order:

```text
accepted decisions
-> live ledger item and local intake on master
-> current migration phase
-> stable behavior contracts
-> target ownership model
-> selected dispatch and runway
-> source evidence
-> historical plans, issues, and conversations
```

An agent must not silently revive a superseded or rejected choice.

## Accepted Decisions

### DEC-001 — Human command owners own the workflows

```yaml
id: DEC-001
status: accepted
decision: >-
  add-to-ledger owns intake, plan-batch owns planning, and work-batch owns
  execution plus same-batch closeout.
consequences:
  - architecture-program-runway is decomposed and deleted
  - batch-runway is split and deleted
  - command owners may delegate mechanisms but retain semantic decisions
```

### DEC-002 — Delegation is allowed; duplicate ownership is not

```yaml
id: DEC-002
status: accepted
decision: >-
  Command owners may delegate diagnostics, state application, path resolution,
  validation, worker execution, review, and commit mechanics. A delegated
  surface may not independently reinterpret the human workflow.
```

### DEC-003 — `planning-state` is a narrow state-machine authority

```yaml
id: DEC-003
status: accepted
decision: >-
  planning-state owns normalized diagnostics, lifecycle invariants, explicit
  transition validation, revision checks, serialization, and receipts. It does
  not select findings, shape batches, design slices, choose recovery, or select
  successors.
```

### DEC-004 — `planning-artifacts` owns structure, not lifecycle

```yaml
id: DEC-004
status: accepted
decision: >-
  planning-artifacts owns canonical paths, artifact types, co-location, lineage,
  archives, and reference resolution. It does not own lifecycle transitions or
  semantic workflow decisions.
```

### DEC-005 — Architecture Program Runway has no target role

```yaml
id: DEC-005
status: accepted
decision: >-
  architecture-program-runway is source implementation to decompose, not a
  permanent program owner or compatibility wrapper.
removal_target: skills/architecture-program-runway
```

### DEC-006 — Batch Runway is split and deleted

```yaml
id: DEC-006
status: accepted
decision: >-
  Runway specification and validation selection move to plan-batch. Execution,
  recovery, finalization, and closeout move to work-batch. Surviving references
  move under those owners, then skills/batch-runway is deleted.
removal_target: skills/batch-runway
```

### DEC-007 — Dispatch remains a separate durable artifact

```yaml
id: DEC-007
status: accepted
decision: >-
  Keep a separate dispatch between ledger selection and runway specification.
  It records the stable selection and scope decision without requiring a
  separate workflow owner.
```

### DEC-008 — Use contract-first hybrid Markdown

```yaml
id: DEC-008
status: accepted
decision: >-
  Skills and active planning artifacts use one versioned structured contract
  plus concise Markdown procedure, rationale, and context.
source_proposals:
  - GitHub issue #48
  - GitHub issue #50
```

### DEC-009 — Operational contracts do not move into discovery frontmatter

```yaml
id: DEC-009
status: accepted
decision: >-
  Preserve minimal discovery frontmatter and place the operational contract
  under a stable Contract heading.
```

### DEC-010 — One canonical structured owner per machine fact

```yaml
id: DEC-010
status: accepted
decision: >-
  Each machine-relevant fact has one canonical structured owner. Prose and
  projections may explain or render but may not independently redefine it.
consequences:
  - duplicate operational values are invalid
  - derived artifacts identify source artifact and revision
  - SQLite remains derived and rebuildable
```

### DEC-011 — No permanent parallel skill catalog

```yaml
id: DEC-011
status: accepted
decision: >-
  Do not create permanent skills-v2, skills-next, or version-suffixed human
  commands. Candidate skills occupy final skills/<name>/ paths in an isolated
  candidate clone with a separate CODEX_HOME.
```

### DEC-013 — Limit `port-by-contract` during bootstrap

```yaml
id: DEC-013
status: accepted
decision: >-
  Use intake-source, distill-contract, and design-target reasoning. Do not use
  create-port-runway during redesign bootstrap because current runway skills are
  source implementation being replaced.
```

### DEC-014 — Ownership-transfer work removes legacy ownership

```yaml
id: DEC-014
status: accepted
decision: >-
  A transfer is incomplete if it only adds a target surface while the old owner
  remains an equally valid normal path.
```

### DEC-015 — Behavior tests outrank topology tests

```yaml
id: DEC-015
status: accepted
decision: >-
  Preserve externally meaningful behavior, schemas, state, file effects, and
  integration. Rewrite or delete tests that only preserve old skill names,
  modes, dependency lists, phrases, aliases, or wrappers.
```

### DEC-016 — Temporary compatibility expires

```yaml
id: DEC-016
status: accepted
decision: >-
  Every temporary bridge or legacy parser names a caller, reason, owner, allowed
  scope, and measurable deletion condition. Coexistence is not completion.
```

### DEC-017 — Runner orchestrates public commands only

```yaml
id: DEC-017
status: accepted
decision: >-
  The runner may invoke plan-batch and work-batch, enforce explicit loop bounds,
  and own process, sandbox, telemetry, and stop-policy concerns. It does not own
  selection, slice design, execution acceptance, closeout meaning, or successor
  readiness.
target_protocol:
  - invoke_plan_batch
  - optionally_invoke_work_batch
  - evaluate_explicit_loop_bound
  - optionally_invoke_fresh_plan_batch
```

### DEC-018 — Same-batch closeout never selects a successor

```yaml
id: DEC-018
status: accepted
decision: >-
  work-batch reconciles only the completed batch and stops. A later explicit
  plan-batch invocation owns successor planning.
```

### DEC-019 — Specialized review skills remain evidence producers

```yaml
id: DEC-019
status: accepted
decision: >-
  legacy-removal, dead-surface-audit, and test-quality-review own evidence, not
  queue, selection, execution, commit, or closeout state.
```

### DEC-020 — Worker and reviewer authority remains separate

```yaml
id: DEC-020
status: accepted
decision: >-
  The implementation worker cannot review or commit its own work. The reviewer
  remains read-only. work-batch owns lifecycle coordination.
```

### DEC-022 — Historical artifacts are not rewritten by default

```yaml
id: DEC-022
status: accepted
decision: >-
  Archived artifacts may retain old names and formats. Active pickup and new
  artifacts use target contracts. Legacy readers are temporary and read-only.
```

### DEC-023 — Parallel execution is outside this program

```yaml
id: DEC-023
status: accepted
decision: >-
  Schemas may record dependencies and write scopes for future conservative
  parallelism, but this migration does not implement parallel batches, slices,
  worktree scheduling, locking, or merge policy.
```

### DEC-024 — Finalize `skill-authoring` before owner migrations

```yaml
id: DEC-024
status: accepted
supersedes:
  - DEC-021
decision: >-
  Define, implement, validate, and treat skill-authoring v1 as authoritative
  before add-to-ledger, plan-batch, or work-batch are migrated.
```

### DEC-025 — Implementation enters through ledger intake

```yaml
id: DEC-025
status: accepted
decision: >-
  Convert the design into individually addressable work items, ingest them
  together through add-to-ledger, leave them unselected, and let plan-batch shape
  at most one runnable batch at a time.
```

### DEC-026 — Stable skills control candidate migration before cutover

```yaml
id: DEC-026
status: accepted
supersedes:
  - DEC-012
decision: >-
  Use the untouched stable checkout and default CODEX_HOME as the control plane
  for canonical planning and migration execution against a separate candidate
  clone. Candidate skills remain validation-only until cutover.
```

### DEC-027 — Explicit three-root pre-cutover topology

```yaml
id: DEC-027
status: accepted
refines:
  - DEC-026
decision: >-
  Before cutover, the stable checkout on authoritative master is both the
  toolchain source root and canonical planning repository root. A separate
  candidate clone is the implementation target root.
topology:
  toolchain_source_root: stable_checkout_on_authoritative_master
  canonical_planning_repository_root: stable_checkout_on_authoritative_master
  implementation_target_root: separate_candidate_clone
rules:
  - every operation records all three roots
  - roots are not inferred only from current working directory
  - planning writes occur only under canonical_planning_repository_root
  - implementation writes, validation, diffs, and commits occur only under implementation_target_root
  - stable controlling scripts, references, schemas, workers, and reviewers resolve from toolchain_source_root
  - root or generation mismatch blocks before writes or delegation
  - changed stable control code is consumed only by a fresh stable session
required_receipts:
  - root_binding
  - toolchain_generation
  - planning_revision
  - implementation_revision
  - cross_repository_commit_and_closeout
```

### DEC-028 — Accepted design integration and branch authority

```yaml
id: DEC-028
status: accepted
decision: >-
  Create the implementation branch from the latest authoritative master and
  merge the accepted design history with preserved ancestry. The original
  snapshot b3f31c44a1fc3287c33dd2955489f194afef66f6 remains provenance; the
  final accepted tip of architecture/command-owner-redesign is the design
  snapshot imported by CCFG-18.
integration:
  base: latest_authoritative_master
  preferred_method: merge_no_ff_of_final_accepted_design_tip
  verify_before_merge:
    - source_history_contains_only_accepted_design_lineage
  verify_after_merge:
    - implementation_branch_has_master_and_design_ancestry
    - imported_design_tree_matches_accepted_snapshot
branch_authority:
  before_CCFG_18:
    master: canonical_planning_authority
    architecture_command_owner_redesign: accepted_design_authority
  after_CCFG_18_merge_before_cutover:
    master: canonical_planning_authority
    implementation_branch: live_candidate_design_and_code_authority
    architecture_command_owner_redesign: frozen_provenance_branch
links:
  authoritative: immutable_commit_urls_only
  mutable_branch_links: navigation_only
```

### DEC-029 — Generation boundary and compatible rollback

```yaml
id: DEC-029
status: accepted
refines:
  - DEC-026
decision: >-
  No real batch is controlled by more than one toolchain generation. Stable
  batches close before candidate-controlled canonical work begins. Cutover occurs
  at quiescent state, and the first candidate canonical write starts in a new
  post-cutover batch.
before_first_candidate_write:
  installation_only_rollback_allowed_when:
    - no_candidate_format_canonical_state_written
    - no_candidate_selected_queued_or_active_state
    - planning_state_remains_stable_readable
after_first_candidate_write:
  installation_only_rollback: forbidden
  restore_together:
    - toolchain_installation
    - toolchain_source_code
    - canonical_planning_state
    - active_planning_artifacts
    - required_run_and_transition_state
minimum_checkpoint:
  - stable_master_commit
  - candidate_implementation_commit
  - canonical_planning_file_hashes
  - active_artifact_inventory_and_hashes
  - selected_queued_active_and_resumable_state
  - stable_and_candidate_install_manifests
  - resolved_link_maps
  - validation_and_fresh_session_receipts
  - restore_procedure
```

### DEC-030 — Cutover preparation and final cutover are separate

```yaml
id: DEC-030
status: accepted
refines:
  - DEC-017
  - DEC-026
decision: >-
  CCFG-27 prepares and rehearses cutover without changing the default
  generation. CCFG-28 removes APR and Batch Runway from the candidate,
  proves a clean installation with no legacy route, and performs the final
  default-generation switch.
CCFG_27:
  purpose: prepare_and_rehearse_cutover
  default_switch: forbidden
  requires:
    - command_owner_legacy_dependencies_zero
    - runner_public_protocols_only
    - agents_independent_of_legacy_paths
    - clean_generation_install_rehearsal
    - atomic_switch_rehearsal
    - rollback_rehearsal
CCFG_28:
  purpose: remove_legacy_owners_and_commit_final_cutover
  performs:
    - physical_legacy_owner_deletion
    - clean_candidate_installation
    - direct_legacy_invocation_negative_tests
    - final_default_codex_home_switch
    - fresh_candidate_read_only_diagnostic
cutover_controller:
  generation: stable_pinned_session
  fresh_candidate_before_stable_closeout: validation_only
  candidate_canonical_writes_before_new_batch: forbidden
cutover_committed_when:
  - fresh_candidate_diagnostic_green
  - CCFG_28_same_batch_closeout_complete
  - stable_controller_stopped
```

### DEC-031 — Layered but single-version `skill-authoring` v1

```yaml
id: DEC-031
status: accepted
refines:
  - DEC-024
decision: >-
  skill-authoring v1 has a complete authoritative core for hybrid skills.
  Planning-artifact authoring is a conditionally loaded reference governed by
  the same skill and contract version.
core_prerequisites:
  - accepted_skill_contract_v1
  - accepted_ownership_vocabulary
  - accepted_skill_canonicality_rules
  - accepted_reference_loading_rules
  - deterministic_validators
requires_full_planning_artifact_schema_closeout: false
planning_extension:
  path: skills/skill-authoring/references/planning-artifact-authoring.md
  supported_schemas_must_be_declared: true
  unsupported_schema_behavior: block
single_dialect_guards:
  skill_path_count: 1
  skill_contract_version_count: 1
  per_command_dialects: forbidden
required_trials:
  - narrow_evidence_or_analysis_skill
  - branching_command_skill_with_stops_and_delegations
runtime_dependency_of_command_owners: false
```

### DEC-032 — Canonical structured state lives in `CURRENT.md`

```yaml
id: DEC-032
status: accepted
resolves:
  - OPEN-001
decision: >-
  Each active program CURRENT.md contains exactly one canonical structured state
  block for machine-relevant lifecycle facts plus concise prose that may explain
  but may not redefine those facts.
canonical_facts:
  - program_identity
  - state_revision
  - canonical_ledger_pointer
  - selected_dispatch_pointer
  - queued_runway_pointer
  - active_runway_pointer
  - latest_closeout_pointer
  - machine_relevant_blockers
write_contract:
  expected_revision_required: true
  expected_file_hash_required: true
  atomic_replace_required: true
  reread_and_validate_required: true
  before_and_after_receipt_required: true
prototype_must_prove:
  - atomic_update
  - stale_revision_rejection
  - fresh_session_readability
  - rollback_behavior
  - localized_git_diff
  - no_duplicate_authority
```

### DEC-033 — Canonical ledger uses per-finding structured records

```yaml
id: DEC-033
status: accepted
resolves:
  - OPEN-002
decision: >-
  LEDGER.md uses one canonical structured block per finding. A compact summary or
  index is derived from or mechanically validated against those blocks and is
  never a second authority.
finding_block_owns:
  - identity
  - title
  - provenance
  - lifecycle_status
  - dependencies
  - scope
  - evidence_pointers
  - next_action
  - finding_revision_when_required
ledger_transaction:
  expected_file_hash_required: true
  parse_all_blocks_before_mutation: true
  validate_unique_identity_and_provenance: true
  apply_multi_item_changes_in_memory: true
  regenerate_or_validate_index: true
  atomic_whole_file_replace: true
  transaction_receipt_required: true
prototype_comparison:
  compare_against: single_global_structured_block
  criteria:
    - multi_item_intake
    - duplicate_detection
    - transaction_atomicity
    - git_diff_quality
    - merge_conflicts
    - parsing
    - sqlite_projection
    - derived_index_consistency
default_after_prototype: per_finding_blocks
```

### DEC-034 — Post-cutover authority converges back to `master`

```yaml
id: DEC-034
status: accepted
decision: >-
  After CCFG-28, the implementation branch may remain the candidate toolchain
  source while master remains the canonical planning repository. CCFG-29 owns a
  final quiescent integration into latest master, proof of identical toolchain
  content, rebinding of the default CODEX_HOME to master, and retirement of the
  candidate branch and cross-checkout bootstrap support.
CCFG_29_additional_scope:
  - merge_implementation_branch_into_latest_master
  - verify_candidate_toolchain_content_unchanged_by_merge
  - rebind_default_toolchain_to_master_checkout
  - fresh_session_identity_and_behavior_check
  - remove_temporary_cross_checkout_bridge
  - freeze_or_delete_implementation_branch_when_safe
```

### DEC-035 — Cross-checkout bridge is narrow, versioned, and temporary

```yaml
id: DEC-035
status: accepted
decision: >-
  The bootstrap cross-checkout support is a narrow versioned control-plane
  mechanism, not a prompt convention or broad orchestrator. It is consumed only
  by fresh stable sessions and removed after CCFG-29 final integration.
owns:
  - root_binding_validation
  - repository_identity_validation
  - write_scope_validation
  - generation_identity_capture
  - cross_repository_receipt_format
forbids:
  - finding_selection
  - scope_shaping
  - runway_design
  - execution_acceptance
  - closeout_interpretation
  - successor_selection
bridge_record:
  caller: stable_plan_and_work_control
  reason: self-hosted_migration_against_separate_candidate_clone
  allowed_scope: root_and_generation_enforcement_only
  deletion_condition: CCFG_29_final_integration_complete
```

### DEC-036 — Schema evolution is closed-world and reader-first

```yaml
id: DEC-036
status: accepted
refines:
  - DEC-008
  - DEC-010
  - DEC-031
approved_via:
  response: Approve all four
  planning_receipt_commit: 19e0746cdc7f681ebe4e6b0ab0be62640097ea6f
  planning_receipt_path: docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md
decision: >-
  While v1 is active, writers emit v1 and readers accept only explicitly
  supported versions and fields. Unknown versions block. Unknown v1 fields
  reject unless that schema names a bounded allowlist exception. Optional
  additions require an accepted compatibility decision and a coordinated
  reader-before-writer rollout. Required-field changes and semantic ownership
  changes require a new version.
v1_policy:
  writer_emits: v1
  reader_accepts:
    - v1
  unknown_schema_version: block
  unknown_fields: reject
  unknown_field_exception:
    requires:
      - schema_name
      - allowed_fields
      - accepted_compatibility_decision
      - bounded_scope
      - removal_condition
    may_not_override:
      - unknown_version_block
      - required_field_change_requires_new_version
      - semantic_ownership_change_requires_new_version
  optional_field_addition:
    requires:
      - accepted_compatibility_decision
      - readers_accept_before_writers_emit
  required_field_change:
    requires: new_schema_version
  semantic_ownership_change:
    requires:
      - new_schema_version
      - accepted_architecture_decision
  deprecation:
    v1_reader_support_required_until: named_migration_condition_satisfied
    silent_removal_within_v1: forbidden
producer_identity:
  required:
    - toolchain_generation
    - toolchain_commit
    - schema_version
implementation_owners:
  skill_contract_v1: CCFG-20
  planning_artifact_schemas: CCFG-21
  behavioral_scenarios: CCFG-23
```

### DEC-037 — `ledger-store/v1` applies caller decisions with whole-ledger CAS

```yaml
id: DEC-037
status: accepted
refines:
  - DEC-002
  - DEC-003
  - DEC-033
approved_via:
  response: Approve all four
  planning_receipt_commit: 19e0746cdc7f681ebe4e6b0ab0be62640097ea6f
  planning_receipt_path: docs/plans/programs/codex-config/batches/ccfg-19-source-contract-decisions/runway.md
decision: >-
  ledger-store/v1 is an apply-only storage mechanism. It reads and rewrites the
  whole ledger under file-level compare-and-swap, validates the revisions of
  every touched finding, binds each idempotency key to one exact caller payload,
  renders deterministically, replaces atomically, and makes a
  ledger-written/receipt-missing result recoverable without applying the
  mutation twice. Command owners retain every semantic workflow decision.
read:
  inputs:
    - ledger_path
  outputs:
    - parsed_findings
    - file_revision
apply:
  inputs:
    - ledger_path
    - expected_file_revision
    - caller_decision:
        action: create | update | merge | no-op | reconcile
        finding_mutations: []
        touched_finding_revisions: {}
        idempotency_key: string
  outputs:
    - outcome: applied | exact_replay
    - before_revision
    - after_revision
    - touched_finding_ids
    - receipt
cas:
  scope: whole_ledger
  expected_file_revision_mismatch: reject_without_write
  touched_finding_revision_mismatch: reject_without_write
idempotency:
  evaluation_order:
    - reject_existing_key_payload_mismatch
    - return_existing_exact_key_payload_result
    - validate_cas_for_new_key
  exact_key_and_payload_replay: return_same_result_without_reapplying
  same_key_different_payload: reject
  durable_binding:
    - idempotency_key
    - exact_apply_request
    - before_revision
    - after_revision
    - touched_finding_ids
write_contract:
  parse_and_apply_in_memory: required
  deterministic_rendering: required
  atomic_replacement: required
  reread_and_validate: required
receipt_recovery:
  ledger_written_receipt_missing: recover_same_receipt_from_durable_exact_replay_evidence
  reapply_mutation: forbidden
  missing_or_ambiguous_replay_evidence: block
allowed_mechanical_checks:
  - schema_and_identity_uniqueness
  - expected_file_revision
  - caller_payload_shape
  - dependency_references
  - touched_finding_revisions
  - exact_idempotency_replay
  - deterministic_resulting_render
forbidden_semantic_decisions:
  - duplicate_or_merge_meaning
  - finding_selection
  - scope_shaping
  - closeout_interpretation
  - successor_selection
semantic_decision_owners:
  intake_mutation: add-to-ledger
  same_batch_reconciliation: work-batch
implementation_owners:
  store_and_fault_injection: CCFG-21
  intake_integration: CCFG-24
  closeout_integration: CCFG-26
```

## Superseded Decisions

```yaml
- id: DEC-012
  status: superseded
  superseded_by: DEC-026
- id: DEC-021
  status: superseded
  superseded_by: DEC-024
```

## Resolved Questions

```yaml
- id: OPEN-001
  status: resolved
  resolved_by: DEC-032
- id: OPEN-002
  status: resolved
  resolved_by: DEC-033
```

## Open Decisions

### OPEN-003 — Multi-artifact planning transaction

```yaml
id: OPEN-003
status: open
question: >-
  How should plan-batch recoverably apply dispatch creation, selected transition,
  runway creation, and queued transition?
blocks:
  - final_plan_batch_state_mutation_protocol
```

### OPEN-004 — One commit per accepted slice

```yaml
id: OPEN-004
status: open
question: >-
  Is one focused commit per accepted slice universal or a default execution
  profile with explicit overrides?
recommended_option: default_with_explicit_override
```

### OPEN-005 — Exact slice-count rule

```yaml
id: OPEN-005
status: open
question: >-
  Is 3-5 slices a hard constraint, warning, or heuristic?
recommended_option: warning_level_heuristic
```

### OPEN-006 — Final Python module split

```yaml
id: OPEN-006
status: open
question: >-
  What final module split implements diagnostics, transitions, ledger mutation,
  artifact parsing, validation, closeout, and projections?
recommended_option: decide_from_behavior_seams
```

### OPEN-007 — Worker and reviewer names

```yaml
id: OPEN-007
status: open
question: >-
  Should runway_worker and runway_reviewer be renamed after Batch Runway deletion?
recommended_option: defer_renaming
```

### OPEN-008 — Prototype directory retention

```yaml
id: OPEN-008
status: open
question: >-
  Should representation experiments live under prototypes/contract-first or only
  in tests and design documents?
recommended_option: use_only_when_reviewable_comparison_requires_it
```

## Deferred Ideas

```yaml
- id: FUTURE-001
  status: deferred
  topic: conservative_parallel_slice_scheduling
- id: FUTURE-002
  status: deferred
  topic: generated_markdown_views
- id: FUTURE-003
  status: deferred
  topic: stronger_transaction_store
```

## Rejected Approaches

```yaml
- id: REJECT-001
  approach: permanent_skills_v2_or_versioned_commands
- id: REJECT-002
  approach: retain_APR_and_Batch_Runway_as_final_owners
- id: REJECT-003
  approach: broad_replacement_workflow_service_behind_aliases
- id: REJECT-004
  approach: independently_edited_companion_yaml_default
- id: REJECT-005
  approach: preserve_every_current_test_unchanged
- id: REJECT-006
  approach: one_giant_redesign_batch
- id: REJECT-007
  approach: precompute_batches_before_ledger_intake
- id: REJECT-008
  approach: candidate_skills_control_real_migration_before_cutover
- id: REJECT-009
  approach: prompt_only_cross_checkout_routing
```

## Decision Change Procedure

To change an accepted decision:

1. add a new decision record;
2. mark the previous record superseded rather than rewriting history silently;
3. name affected contracts, work items, scenarios, and deletion conditions;
4. state whether behavior is broadened, narrowed, or preserved;
5. require explicit human approval for ownership changes or supported-behavior
   narrowing;
6. update the design package and live planning intake before implementation uses
   the changed decision.
