# CCFG-21 Planning Artifact Contracts Completed Slices

## Slice 1: Establish Closed-World Schemas And Read-Only Validation

- Candidate commit: `5b610e5b612f9fe9b535e25e4de102f5672d0f49`.
- Outcome: five closed-world Draft-07 planning schemas and one
  `scripts/planning_contract.py` owner now provide duplicate-key-safe YAML
  parsing, deterministic diagnostics, canonical-owner validation, explicit
  read-only compatibility, and the thin validation CLI.
- Validation: 25 focused tests passed; Ruff passed; basedpyright reported zero
  errors and six import-source warnings; the valid catalog exited 0; the
  invalid unknown-field catalog exited 1 under a successful expected-failure
  wrapper; `git diff --check` passed.
- Review: clean after the recovery loop added PyYAML node/event handling for
  quoted, malformed, duplicate, and producer-only secondary owners. Delta-only
  test-quality review found no remaining actionable issue.
- Compatibility: the explicitly selected old-format reader remains read-only;
  nested fenced examples and unrelated malformed YAML remain non-operational.
- Cleanup residue: none.

### Slice 1 Execution Receipt

```yaml
runway: docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md
live_lease:
  interface: cross-checkout-context/v1
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 45bbd7d6c12e99a56466bd47df957060755a16d9
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 45bbd7d6c12e99a56466bd47df957060755a16d9
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 3e54155964e92d3a4dced8268cc683baaab9be1c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
validated_scope:
  planning_paths: []
  implementation_paths:
    - schemas/planning-current-v1.schema.json
    - schemas/planning-finding-v1.schema.json
    - schemas/planning-dispatch-v1.schema.json
    - schemas/planning-runway-v1.schema.json
    - schemas/planning-closeout-v1.schema.json
    - scripts/planning_contract.py
    - tests/test_planning_contract_schema.py
    - tests/fixtures/planning-contracts/schema/
    - tests/fixtures/planning-contracts/compatibility/
worker_verification: matched
reviewer_verification: matched
```

### Stable Planning Receipt

```json
{
  "interface": "cross-checkout-receipt/v1",
  "caller": "work-batch",
  "reason": "CCFG-21 Slice 1 stable planning receipt",
  "allowed_scope": {
    "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
    "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
    "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
    "planning_paths": [
      "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/completed-slices.md",
      "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md"
    ],
    "implementation_paths": []
  },
  "generation_identity": {
    "generation_role": "stable",
    "toolchain_source_root": "/home/alacasse/projects/codex-config",
    "toolchain_commit": "45bbd7d6c12e99a56466bd47df957060755a16d9",
    "codex_home": "/home/alacasse/.codex",
    "canonical_state_mutation_allowed": true
  },
  "repository_revisions": {
    "toolchain_commit": "45bbd7d6c12e99a56466bd47df957060755a16d9",
    "canonical_planning_commit_before": "45bbd7d6c12e99a56466bd47df957060755a16d9",
    "implementation_commit_before": "5b610e5b612f9fe9b535e25e4de102f5672d0f49"
  },
  "deletion_condition": "CCFG-29 final integration"
}
```
