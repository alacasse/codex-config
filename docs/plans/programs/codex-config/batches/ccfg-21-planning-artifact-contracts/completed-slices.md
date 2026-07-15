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

## Slice 2: Add Revisioned Current And Ledger Stores

- Candidate commit: `3d2ac7ad64d3b10494ff615af65662fca2306ec6`.
- Outcome: current and ledger stores now enforce expected logical revisions and
  full-file hashes, deterministic rendering, adjacent atomic replacement,
  reread validation, recoverable receipts, exact idempotent replay, and
  apply-only `ledger-store/v1` caller decisions.
- Validation: the combined Slice 1+2 suite passed 51 tests; Ruff passed;
  basedpyright reported zero errors and six import-source warnings; the layout
  comparison reported equivalent semantic/projection output with duplicate,
  diff-locality, error-locality, revision, and source-identity measurements
  green; invalid derived-index validation produced the expected exit 1; staged
  `git diff --cached --check` passed.
- Review: clean after the recovery loop bound durable replay metadata and
  results to the exact caller request and replaced self-reported comparison
  flags with fixture-derived measurements. Delta-only test-quality review found
  no remaining actionable issue.
- Compatibility: per-finding ledgers remain the measured default; the global
  fixture is retained only as an equivalent comparison shape.
- Cleanup residue: none.

### Slice 2 Execution Receipt

```yaml
runway: docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md
live_lease:
  interface: cross-checkout-context/v1
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: f408ed3ee2f127f8f074c69bf5f3cfaf1bd1d756
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: f408ed3ee2f127f8f074c69bf5f3cfaf1bd1d756
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 5b610e5b612f9fe9b535e25e4de102f5672d0f49
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
validated_scope:
  planning_paths: []
  implementation_paths:
    - scripts/planning_contract.py
    - tests/test_planning_contract_store.py
    - tests/fixtures/planning-contracts/current/
    - tests/fixtures/planning-contracts/ledger/
worker_verification: matched
reviewer_verification: matched
```

### Stable Planning Receipt

```json
{
  "interface": "cross-checkout-receipt/v1",
  "caller": "work-batch",
  "reason": "CCFG-21 Slice 2 stable planning receipt",
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
    "toolchain_commit": "f408ed3ee2f127f8f074c69bf5f3cfaf1bd1d756",
    "codex_home": "/home/alacasse/.codex",
    "canonical_state_mutation_allowed": true
  },
  "repository_revisions": {
    "toolchain_commit": "f408ed3ee2f127f8f074c69bf5f3cfaf1bd1d756",
    "canonical_planning_commit_before": "f408ed3ee2f127f8f074c69bf5f3cfaf1bd1d756",
    "implementation_commit_before": "3d2ac7ad64d3b10494ff615af65662fca2306ec6"
  },
  "deletion_condition": "CCFG-29 final integration"
}
```

## Slice 3: Add Revisioned Artifact Lineage Writes

- Candidate commit: `d9a3306a02b9e27c2ab3ae39e6c3b281ce1ae9ca`.
- Outcome: dispatch, runway, and closeout writes now reuse the revisioned store
  primitives while enforcing canonical containment, immutable predecessor
  lineage, producer generation identity, exact source revisions, same-batch
  closeout fields, cleared pointers, and recoverable exact replay.
- Validation: the combined Slice 1-3 suite passed 72 tests; Ruff passed;
  basedpyright reported zero errors and six import-source warnings; the valid
  lineage catalog exited 0; invalid lineage exited 1 under the successful
  expected-failure wrapper; staged `git diff --cached --check` passed.
- Review: the first pass found two high-severity gaps: closeout producer
  generation/commit was not cross-bound to dispatch/runway, and replay compared
  only parsed contract content. The recovery bound all three producer
  identities, required full canonical persisted-byte equality, added
  before-persistence and prose-tamper regressions, and returned clean on
  independent re-review. Delta-only test-quality review was clean.
- Compatibility: no live artifacts or command integrations were migrated.
- Cleanup residue: none.

### Slice 3 Execution Receipt

```yaml
runway: docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md
live_lease:
  interface: cross-checkout-context/v1
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 431870dd324703db1210b1632dacbad6769df857
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 431870dd324703db1210b1632dacbad6769df857
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 3d2ac7ad64d3b10494ff615af65662fca2306ec6
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
validated_scope:
  planning_paths: []
  implementation_paths:
    - scripts/planning_contract.py
    - tests/test_planning_contract_artifacts.py
    - tests/fixtures/planning-contracts/artifacts/
worker_verification: matched
reviewer_verification: matched
```

### Stable Planning Receipt

```json
{
  "interface": "cross-checkout-receipt/v1",
  "caller": "work-batch",
  "reason": "CCFG-21 Slice 3 stable planning receipt",
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
    "toolchain_commit": "431870dd324703db1210b1632dacbad6769df857",
    "codex_home": "/home/alacasse/.codex",
    "canonical_state_mutation_allowed": true
  },
  "repository_revisions": {
    "toolchain_commit": "431870dd324703db1210b1632dacbad6769df857",
    "canonical_planning_commit_before": "431870dd324703db1210b1632dacbad6769df857",
    "implementation_commit_before": "d9a3306a02b9e27c2ab3ae39e6c3b281ce1ae9ca"
  },
  "deletion_condition": "CCFG-29 final integration"
}
```

## Slice 4: Implement The DEC-038 Selection Saga And Fault Matrix

- Candidate commit: `596fc7e5e153bb1a89a94010d272efa4ce4ce0ce`.
- Outcome: the closed-world transaction schema and append-only four-stage
  selection prototype now compose the revisioned current store and artifact
  lineage store, resume at the first incomplete stage, preserve durable partial
  evidence, and block reused identities, unexplained movement, and ambiguous
  replay evidence without integrating live command ownership.
- Validation: the combined Slice 1-4 suite passed 98 tests; Ruff passed;
  basedpyright reported zero errors and six import-source warnings; complete and
  recover-after-selected-CAS simulations exited 0; reused-ID mismatch exited 1
  under the successful expected-failure wrapper; staged
  `git diff --cached --check` passed.
- Review: the first pass found two high-severity test-confidence gaps in
  checkpoint evidence and mismatch coverage. The recovery added exact
  transaction/current/artifact/receipt snapshots for all 13 fault boundaries,
  no-duplicate-effect assertions, two state drifts, five coherent lineage
  drifts, and ambiguous selected-replay evidence. No production defect was
  exposed; independent re-review and delta-only test-quality review were clean.
- Compatibility: the prototype remains intentionally unintegrated with
  `plan-batch` and live canonical planning mutation.
- Cleanup residue: none.

### Slice 4 Execution Receipt

```yaml
runway: docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md
live_lease:
  interface: cross-checkout-context/v1
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 1c5c33a25426d829c709d54e7c900331c405ecf2
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 1c5c33a25426d829c709d54e7c900331c405ecf2
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: d9a3306a02b9e27c2ab3ae39e6c3b281ce1ae9ca
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
validated_scope:
  planning_paths: []
  implementation_paths:
    - schemas/planning-selection-transaction-v1.schema.json
    - scripts/planning_contract.py
    - tests/test_planning_transaction.py
    - tests/fixtures/planning-contracts/transactions/
    - CHANGELOG.md
worker_verification: matched
reviewer_verification: matched
```

### Stable Planning Receipt

```json
{
  "interface": "cross-checkout-receipt/v1",
  "caller": "work-batch",
  "reason": "CCFG-21 Slice 4 stable planning receipt",
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
    "toolchain_commit": "1c5c33a25426d829c709d54e7c900331c405ecf2",
    "codex_home": "/home/alacasse/.codex",
    "canonical_state_mutation_allowed": true
  },
  "repository_revisions": {
    "toolchain_commit": "1c5c33a25426d829c709d54e7c900331c405ecf2",
    "canonical_planning_commit_before": "1c5c33a25426d829c709d54e7c900331c405ecf2",
    "implementation_commit_before": "596fc7e5e153bb1a89a94010d272efa4ce4ce0ce"
  },
  "deletion_condition": "CCFG-29 final integration"
}
```
