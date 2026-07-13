# Deletion Conditions

## Purpose

This document defines measurable conditions for narrowing and deleting legacy
workflow owners, modes, routing references, metadata, tests, fixtures, parsers,
and duplicated vocabulary.

Deletion is part of the target architecture, not optional cleanup after the
migration. A transfer is incomplete while the old surface remains a valid normal
owner of the same decision.

## General Deletion Rules

- Historical references in clearly archived artifacts do not block deletion.
- Active docs, skills, manifests, prompts, tests, and generated artifacts do
  block deletion when they still require the old owner.
- A failing topology test after behavior has moved is evidence to classify the
  test, not automatic evidence to restore the old surface.
- A compatibility path may block deletion only when it names a current caller,
  reason, owner, allowed scope, and removal condition.
- No permanent wrapper may exist solely to preserve an internal skill name or
  mode.
- Physical deletion followed by the full target scenario suite is the final
  deletion test.

## `architecture-program-runway`

```yaml
architecture_program_runway:
  human_facing_callers: 0
  command_owner_manifest_dependencies: 0
  runner_prompt_references: 0
  active_skill_references: 0
  active_doc_routing_references: 0

  intake_decisions_owned: 0
  finding_normalization_owned: 0
  ledger_mutation_decisions_owned: 0
  grouping_decisions_owned: 0
  candidate_selection_owned: 0
  scope_shaping_owned: 0
  dispatch_definition_owned: 0
  queue_preparation_owned: 0
  closeout_decisions_owned: 0
  same_batch_reconciliation_owned: 0

  old_mode_callers:
    intake_findings: 0
    group_batches: 0
    select_next_batch: 0
    create_next_runway: 0
    closeout_runway: 0
    reprioritize: 0

  active_artifacts_requiring_skill_contract: 0
  resumable_runner_states_requiring_skill: 0
  compatibility_only_references: 0
  tests_requiring_presence: 0
  migration_fixtures_requiring_presence: 0

  allowed_remaining_references:
    - clearly archived historical artifacts
    - historical changelog entries
    - source-baseline design evidence

  final_action: delete_directory
  final_path: skills/architecture-program-runway
```

### Deletion proof

1. Remove the directory in a candidate commit.
2. Run command manifest and installation tests.
3. Run intake, planning, execution, closeout, and runner scenario suites.
4. Search active files for the old skill name and modes.
5. Classify every remaining match as active defect or allowed historical
   evidence.
6. Reject any attempt to restore a wrapper without an accepted external
   compatibility decision.

## `batch-runway`

```yaml
batch_runway:
  human_facing_callers: 0
  plan_batch_dependencies: 0
  work_batch_dependencies: 0
  command_owner_manifest_dependencies: 0
  runner_prompt_references: 0
  active_doc_routing_references: 0

  create_spec_callers: 0
  execute_spec_callers: 0
  mode_inference_callers: 0

  planning_decisions_owned: 0
  slice_design_owned: 0
  validation_profile_selection_owned: 0
  execution_lifecycle_owned: 0
  recovery_owned: 0
  finalization_owned: 0
  closeout_owned: 0

  surviving_planning_references_moved_to: skills/plan-batch/references
  surviving_execution_references_moved_to: skills/work-batch/references

  active_specs_requiring_old_contract: 0
  agent_result_schema_dependencies_on_old_skill_path: 0
  compatibility_only_references: 0
  tests_requiring_presence: 0
  migration_fixtures_requiring_presence: 0

  allowed_remaining_references:
    - clearly archived historical artifacts
    - historical changelog entries
    - source-baseline design evidence

  final_action: delete_directory
  final_path: skills/batch-runway
```

### Deletion proof

1. Remove the directory in a candidate commit.
2. Verify target planning and execution references resolve.
3. Run worker and reviewer result-contract tests.
4. Run plan and work scenario suites.
5. Run active artifact scans for old paths and modes.
6. Confirm completed historical artifacts remain readable without becoming
   current pickup state.

## Old Mode Names

```yaml
old_mode_names:
  active_skill_references: 0
  active_docs_references: 0
  manifest_references: 0
  default_prompt_references: 0
  runner_generated_prompt_references: 0
  new_artifact_references: 0
  active_test_expectations: 0
  active_fixture_expectations: 0

  names:
    - intake-findings
    - group-batches
    - select-next-batch
    - create-next-runway
    - closeout-runway
    - reprioritize
    - create-spec
    - execute-spec

  allowed_remaining_references:
    - archived historical artifacts
    - source architecture analysis
```

A public target operation may use a descriptive transition name such as
`select_batch` or `queue_batch` when it is a narrow state operation, but it must
not preserve a broad legacy mode that interprets human workflow intent.

## Old Routing References

```yaml
old_routing_references:
  add_to_ledger_to_apr_edges: 0
  plan_batch_to_apr_edges: 0
  plan_batch_to_batch_runway_edges: 0
  work_batch_to_batch_runway_edges: 0
  work_batch_to_apr_edges: 0
  runner_to_apr_mode_edges: 0
  runner_to_batch_runway_mode_edges: 0
  support_to_legacy_owner_edges: 0
  bridge_state_sections_in_active_routing_docs: 0
```

Target routing docs may retain a historical migration note only when it cannot
be interpreted as current routing authority.

## Direct-Command and Feature Metadata

```yaml
old_direct_command_metadata:
  installed_old_owner_features: 0
  old_owner_display_commands: 0
  old_owner_default_prompts: 0
  old_owner_command_descriptions: 0
  command_owner_requires_old_owner: 0
  old_owner_install_links: 0

runner_feature:
  installed_through_apr_feature: false
  public_command_protocols_only: true
```

Deleting a feature entry must not remove runner files that have become an
independent feature. Separate the runner before APR feature deletion.

## Topology and Text-Contract Tests

```yaml
old_topology_tests:
  tests_asserting_apr_presence: 0
  tests_asserting_batch_runway_presence: 0
  tests_asserting_old_requires_lists: 0
  tests_asserting_old_mode_phrases: 0
  tests_asserting_runtime_owner_descriptions: 0
  tests_asserting_bridge_state_sections: 0

replacement_proof:
  behavioral_scenarios_green: true
  schema_contract_tests_green: true
  forbidden_dependency_tests_green: true
  physical_deletion_test_green: true
```

### Test deletion decision rule

Delete or rewrite a test when:

- its only failure after migration is absence of an old skill, mode, dependency,
  heading, phrase, alias, or wrapper;
- it does not prove a named external compatibility contract;
- target behavioral and schema tests protect the useful rule.

Retain a compatibility test only when it records:

```yaml
compatibility_contract:
  external_caller: exact caller
  promised_surface: exact supported surface
  reason: current requirement
  owner: named owner
  removal_condition: measurable condition
```

## Temporary Transition Fixtures

```yaml
temporary_transition_fixtures:
  selected_legacy_dispatches: 0
  queued_legacy_runways: 0
  active_legacy_runways: 0
  resumable_legacy_runner_states: 0
  old_parser_only_fixtures: 0
  fixtures_without_owner: 0
  fixtures_without_removal_condition: 0
  final_migration_scenarios_green: true
```

Fixtures retained only as historical test data must move under an explicitly
historical fixture area and must not be consumed by current pickup logic.

## Legacy Artifact Parsers

```yaml
legacy_artifact_parsers:
  normal_new_artifact_writes: 0
  mutation_operations: 0
  active_legacy_artifacts: 0
  resumable_legacy_runs: 0
  callers: 0
  tests_requiring_parser: 0
  remaining_role: deleted
```

A legacy parser is read-only during migration. It may not emit new old-format
artifacts or silently upgrade them during a state mutation.

## Duplicated Rules and Vocabulary

```yaml
duplicated_rules_and_vocabulary:
  intake_rule_owners: 1
  candidate_selection_owners: 1
  scope_shaping_owners: 1
  dispatch_definition_owners: 1
  runway_specification_owners: 1
  validation_profile_selection_owners: 1
  execution_lifecycle_owners: 1
  recovery_owners: 1
  closeout_reconciliation_owners: 1
  lifecycle_vocabulary_authorities: 1
  artifact_vocabulary_authorities: 1
  deletion_test_status_owners: 1
  support_skills_with_program_owner_escape_hatch: 0
```

The same rule may be summarized by callers, but summaries must point to the
canonical owner and must not independently define procedure or values.

## Legacy References in Agents

```yaml
agent_contracts:
  worker_description_requires_batch_runway_name: false
  reviewer_description_requires_batch_runway_name: false
  result_schema_paths_require_batch_runway: false
  worker_lifecycle_authority: false
  reviewer_lifecycle_authority: false
```

Renaming `runway_worker` and `runway_reviewer` is not required for deletion if
their contracts no longer depend on the deleted skill path or imply that Batch
Runway remains the workflow owner.

## Planning-State Narrowing Conditions

`planning-state` survives, but its role must be measurable:

```yaml
planning_state:
  candidate_selection_decisions: 0
  scope_shaping_decisions: 0
  dispatch_content_decisions: 0
  slice_design_decisions: 0
  validation_profile_selection_decisions: 0
  recovery_decisions: 0
  commit_acceptance_decisions: 0
  successor_selection_decisions: 0

  normalized_diagnostic_interface: versioned
  transition_interface: explicit
  expected_revision_validation: true
  transition_receipts: true
  projection_is_derived: true
```

If planning-state gains a high-level operation that makes one of the forbidden
decisions, it has become a replacement broad workflow owner and the migration
must stop.

## Planning-Artifacts Narrowing Conditions

```yaml
planning_artifacts:
  lifecycle_transition_decisions: 0
  finding_status_decisions: 0
  candidate_selection_decisions: 0
  execution_decisions: 0

  canonical_path_resolution: true
  artifact_type_validation: true
  lineage_validation: true
  archive_placement: true
```

## Final Cutover Conditions

```yaml
final_cutover:
  accepted_design_decisions_open_blockers: 0
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  resumable_old_runner_run: false

  add_to_ledger_target_scenarios_green: true
  plan_batch_target_scenarios_green: true
  work_batch_target_scenarios_green: true
  closeout_target_scenarios_green: true
  runner_target_scenarios_green: true

  architecture_program_runway_deletion_conditions_met: true
  batch_runway_deletion_conditions_met: true
  old_mode_deletion_conditions_met: true
  old_topology_test_deletion_conditions_met: true
  legacy_parser_deletion_conditions_met: true

  candidate_installation_green: true
  stable_rollback_available: true
```

## Final Deletion Test

The architecture is complete only after this sequence succeeds:

```text
remove architecture-program-runway
remove batch-runway
remove expired parsers, fixtures, modes, metadata, and topology tests
install the candidate feature set
run schema and dependency validation
run all target behavioral scenarios
run full repository tests
run a controlled end-to-end intake -> plan -> work -> closeout workflow
confirm no successor was selected
```

If only old topology or text-contract tests fail, classify and remove those
tests. Do not restore the old owners unless an explicit supported external
contract is demonstrated.
