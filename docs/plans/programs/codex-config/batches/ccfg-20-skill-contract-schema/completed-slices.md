# CCFG-20 Skill Contract Schema Completed Slices

## Slice 1: Establish Closed-World Schema And Interface

- Candidate commit: `2f8f7a8fedcac925016867596158251564470d88`.
- Candidate files: `schemas/skill-contract-v1.schema.json`,
  `scripts/skill_contract.py`, `tests/test_skill_contract_schema.py`, the two
  schema fixture catalogs, `pyproject.toml`, and `uv.lock`.
- Contract result: one Draft-07 schema owns the accepted closed-world
  `skill-contract/v1` shape, including producer identity; one deep Python
  interface owns extraction, YAML loading, schema application, deterministic
  diagnostics, and CLI adaptation.
- Fail-closed result: duplicate YAML keys reject at every mapping depth,
  Contract examples inside Markdown fences are ignored, directory catalogs
  discover only `SKILL.md`, and empty catalogs reject.
- Validation: 17 schema tests passed; Ruff passed; basedpyright reported zero
  errors; the valid CLI catalog exited 0; the invalid unknown-field catalog
  exited 1 under a successful expected-failure harness; `git diff --check`
  passed.
- Review correction: the first independent review found duplicate-key,
  fenced-example, and empty/non-skill catalog gaps. The worker added regression
  coverage and repeat independent review was clean over the full seven-file
  task-scoped diff.
- Behavior changed: yes, the candidate now exposes the repo-local schema and
  validator contract. No current skill, installed feature, manifest entry, or
  later finding changed.
- Cleanup residue: none.

### Orchestration Anomaly

```yaml
- slice: 1
  severity: low
  category: unexpected_head_change
  observed: Stable HEAD moved from 7c1c027 to 9833e92 during preflight because the queued CCFG-20 planning artifacts were committed concurrently.
  impact: The first strict-context payload became stale before delegation; no candidate write had started.
  action_taken: Frozen delegation, inspected the commit, regenerated the payload from the clean current heads, and revalidated every Slice 1 handoff.
  follow_up: Treat the reconciled 9833e92 planning commit as the stable baseline for subsequent slice receipts.
```

### Slice 1 Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 1 skill contract schema and interface",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/schemas/skill-contract-v1.schema.json",
        "/home/alacasse/projects/codex-config-command-owner-redesign/scripts/skill_contract.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_schema.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/schema/valid/example/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/schema/invalid-unknown-field/example/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/pyproject.toml",
        "/home/alacasse/projects/codex-config-command-owner-redesign/uv.lock"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "canonical_planning_commit_before": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "implementation_commit_before": "2f8f7a8fedcac925016867596158251564470d88"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 1 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/completed-slices.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "canonical_planning_commit_before": "9833e92ea94bea481c36235a54a3f938aefe280b",
      "implementation_commit_before": "2f8f7a8fedcac925016867596158251564470d88"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```

## Slice 2: Validate Catalog Ownership And Audience Profiles

- Candidate commit: `dfc5fadbc654d5f81683cd23da8fcf4105d35f16`.
- Candidate files: `scripts/skill_contract.py`,
  `tests/test_skill_contract_catalog.py`, and six catalog fixture contracts.
- Ownership result: controlled decisions and durable facts have one
  deterministic owner unless an explicit shared-mechanism policy names the
  fact; owns/forbids conflicts and unknown delegated targets reject.
- Audience result: human command owners, support mechanisms, evidence skills,
  and authoring support use one schema with profile-specific structured rules.
  No project name or prose interpretation enters validation.
- Validation: 26 schema and catalog tests passed; both Slice 2 CLI harnesses
  passed; Ruff passed; basedpyright reported zero errors; `git diff --check`
  passed.
- Review correction: the first review found that a one-contract catalog could
  bypass unknown-delegation validation. The worker added a one-delegator
  regression and repeat independent review was clean.
- Behavior changed: yes, the candidate validator now applies catalog ownership
  and audience-profile rules through `validate_skill_contracts`.
- Cleanup residue: none.

### Slice 2 Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 2 catalog ownership and audience profiles",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/scripts/skill_contract.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_catalog.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-ownership/command-owner/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-ownership/support/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-ownership/evidence/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-ownership/authoring/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/invalid-duplicate-owner/first/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/invalid-duplicate-owner/second/SKILL.md"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "5341385f273618e80c684990fba051cadb9f339d",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "5341385f273618e80c684990fba051cadb9f339d",
      "canonical_planning_commit_before": "5341385f273618e80c684990fba051cadb9f339d",
      "implementation_commit_before": "dfc5fadbc654d5f81683cd23da8fcf4105d35f16"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 2 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/completed-slices.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "5341385f273618e80c684990fba051cadb9f339d",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "5341385f273618e80c684990fba051cadb9f339d",
      "canonical_planning_commit_before": "5341385f273618e80c684990fba051cadb9f339d",
      "implementation_commit_before": "dfc5fadbc654d5f81683cd23da8fcf4105d35f16"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```

## Slice 3: Validate Delegation, Dependencies, And References

- Candidate commit: `82e67ba08128f117b008718a78cc9e0a19b9c983`.
- Candidate files: `scripts/skill_contract.py`,
  `tests/test_skill_contract_catalog.py`, five contract/reference fixtures.
- Graph result: delegation, required mechanisms, and required evidence skills
  resolve against the explicit catalog or an explicit external-mechanism
  policy; dependency and reference cycles reject deterministically.
- Reference result: only `references[*].path` creates an edge; `load_when`
  remains trigger data. Missing, non-file, outside-root, symlink, and `..`
  escapes reject after strict resolution against the explicit toolchain root.
- Validation: 34 schema and catalog tests passed; both Slice 3 CLI harnesses
  passed; Ruff passed; basedpyright reported zero errors; `git diff --check`
  passed.
- Review: independent strict-context review was clean over the complete
  task-scoped diff and actual resolved fixture paths.
- Behavior changed: yes, structured dependency and reference graph validation
  now runs through the same `validate_skill_contracts` interface.
- Cleanup residue: none.

### Orchestration Anomaly

```yaml
- slice: 3
  severity: low
  category: unexpected_head_change
  observed: Stable HEAD moved from 90ca7aa to 6de7789 after the worker lease and before reviewer delegation because the unrelated CCFG-30 intake was committed.
  impact: The prepared reviewer payload became stale; the candidate diff and Slice 3 scope were unchanged.
  action_taken: Froze review, inspected the exact stable commit, confirmed it changed only the unselected CCFG-30 row and note, then regenerated and revalidated the reviewer lease.
  follow_up: Preserve CCFG-30 as unselected intake and continue exact per-handoff lease checks.
```

### Slice 3 Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 3 delegation dependency and reference validation",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/scripts/skill_contract.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_catalog.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/invalid-reference-cycle/first/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/invalid-reference-cycle/second/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-references/alpha/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-references/alpha/references/details.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/catalog/valid-references/beta/SKILL.md"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "6de7789ff3f9677bbae3bd8fb081c8f9c5bb39c7",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "6de7789ff3f9677bbae3bd8fb081c8f9c5bb39c7",
      "canonical_planning_commit_before": "6de7789ff3f9677bbae3bd8fb081c8f9c5bb39c7",
      "implementation_commit_before": "82e67ba08128f117b008718a78cc9e0a19b9c983"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 3 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/completed-slices.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "6de7789ff3f9677bbae3bd8fb081c8f9c5bb39c7",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "6de7789ff3f9677bbae3bd8fb081c8f9c5bb39c7",
      "canonical_planning_commit_before": "6de7789ff3f9677bbae3bd8fb081c8f9c5bb39c7",
      "implementation_commit_before": "82e67ba08128f117b008718a78cc9e0a19b9c983"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```

## Slice 4: Add Migration Guards And Integration Proof

- Candidate commit: `3e54155964e92d3a4dced8268cc683baaab9be1c`.
- Candidate files: `CHANGELOG.md`, `scripts/skill_contract.py`,
  `tests/test_skill_contract_migration.py`, and six migration policy/catalog
  fixtures.
- Migration result: explicit before/after catalogs and policy inputs detect a
  retained broad-owner dependency, expected ownership that did not move,
  duplicated durable facts, and a rename without contract change. Ambiguous
  catalog identity and same-key/different-policy comparisons fail closed.
- CLI result: `compare` uses the same deep validation interface and preserves
  deterministic success, finding, and usage exit classes.
- Validation: all 42 skill-contract tests passed; Ruff passed; basedpyright
  reported zero errors; both current required-green baselines passed; every
  Slice 1 through 4 CLI harness passed; `git diff --check` passed.
- Diagnostic baseline: the manifest suite remained exactly the documented
  three failures and 18 passes; no new failure entered the set.
- Review: independent strict-context review was clean over explicit
  before/after evidence, policy, CLI behavior, and changelog scope.
- Behavior changed: yes, the candidate validator now exposes deterministic
  migration comparison guards. `codex-features.json`, current skills, and
  installed state remain unchanged; CCFG-22 owns future runtime consumption.
- Cleanup residue: none.

### Slice 4 Cross-Repository Receipts

Exact helper-produced `cross_repository_receipt_to_dict` results:

```json
{
  "candidate_implementation_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 4 migration guards and integration proof",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [],
      "implementation_paths": [
        "/home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/scripts/skill_contract.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_migration.py",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/migration/policy.json",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/migration/before/legacy-owner/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/migration/after-valid/command-owner/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/migration/after-valid/support-mechanism/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/migration/after-retained-owner/command-owner/SKILL.md",
        "/home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/skill-contracts/migration/after-retained-owner/support-mechanism/SKILL.md"
      ]
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "5eb57d581d92681ec6757616511e4c5668a2e9bb",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "5eb57d581d92681ec6757616511e4c5668a2e9bb",
      "canonical_planning_commit_before": "5eb57d581d92681ec6757616511e4c5668a2e9bb",
      "implementation_commit_before": "3e54155964e92d3a4dced8268cc683baaab9be1c"
    },
    "deletion_condition": "CCFG-29 final integration"
  },
  "stable_planning_receipt": {
    "interface": "cross-checkout-receipt/v1",
    "caller": "work-batch",
    "reason": "CCFG-20 Slice 4 stable planning receipt",
    "allowed_scope": {
      "canonical_planning_repository_root": "/home/alacasse/projects/codex-config",
      "canonical_planning_root": "/home/alacasse/projects/codex-config/docs/plans",
      "implementation_target_root": "/home/alacasse/projects/codex-config-command-owner-redesign",
      "planning_paths": [
        "/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/completed-slices.md"
      ],
      "implementation_paths": []
    },
    "generation_identity": {
      "generation_role": "stable",
      "toolchain_source_root": "/home/alacasse/projects/codex-config",
      "toolchain_commit": "5eb57d581d92681ec6757616511e4c5668a2e9bb",
      "codex_home": "/home/alacasse/.codex",
      "canonical_state_mutation_allowed": true
    },
    "repository_revisions": {
      "toolchain_commit": "5eb57d581d92681ec6757616511e4c5668a2e9bb",
      "canonical_planning_commit_before": "5eb57d581d92681ec6757616511e4c5668a2e9bb",
      "implementation_commit_before": "3e54155964e92d3a4dced8268cc683baaab9be1c"
    },
    "deletion_condition": "CCFG-29 final integration"
  }
}
```
