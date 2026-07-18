# CCFG-21 Runway

## Operational Contract

```yaml
schema: planning-runway/v1
artifact:
  id: ccfg-21-artifacts
  source_dispatch: dispatch.md
  source_dispatch_revision: cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
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
- id: artifacts
  title: Add artifact lineage writes
  risk: migration
  status: pending
  allowed_paths:
  - scripts/planning_contract.py
  validation:
  - pytest tests/test_planning_contract_artifacts.py
  vertical_slice:
    starting_scenario: planning artifacts need revisioned lineage writes
    durable_result: artifact lineage writes bind the selected dispatch and runway
    owner_before: unversioned planning artifact writes
    owner_after: revisioned artifact lineage store
    migrated_callers:
    - planning selection transaction
    focused_validation:
    - pytest tests/test_planning_contract_artifacts.py
    independently_usable_state: revisioned lineage writes work before closeout reconciliation
    rollback_boundary: revert the artifact-lineage slice
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
