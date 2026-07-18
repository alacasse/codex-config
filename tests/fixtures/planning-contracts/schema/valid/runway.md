# CCFG-21 Runway

## Operational Contract

```yaml
schema: planning-runway/v1
artifact:
  id: ccfg-21-planning-artifact-contracts
  source_dispatch: docs/plans/programs/codex-config/batches/ccfg-21/dispatch.md
  source_dispatch_revision: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
batch:
  kind: migration
  status: queued
execution:
  result_contract: registered-agent/v2
  branch_policy: explicit
  dirty_worktree_policy: strict
  successor_selection: forbidden
  implementation_target_root: /work/candidate
slices:
  - id: schema-validation
    title: Establish schemas and read-only validation
    risk: migration
    status: pending
    allowed_paths:
      - schemas/**
    validation:
      - pytest tests/test_planning_contract_schema.py
    vertical_slice:
      starting_scenario: planning artifacts lack schema validation
      durable_result: planning artifacts validate through one schema owner
      owner_before: prose-only planning contracts
      owner_after: planning-runway schema validation
      migrated_callers:
        - planning contract validator
      focused_validation:
        - pytest tests/test_planning_contract_schema.py
      independently_usable_state: schema validation is usable before later artifact writes
      rollback_boundary: revert the schema-validation slice
      temporary_residue: []
      ownership_coexistence: none
    migration_matrix: {}
review:
  final_gate: registered-reviewer
closeout:
  same_batch_only: true
  required_artifacts:
    - closeout.md
producer:
  toolchain_generation: stable
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: planning-runway/v1
```
