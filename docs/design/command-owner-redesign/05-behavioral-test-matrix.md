# Behavioral Test Matrix

## Purpose

This matrix defines behavior evidence independently from legacy skill names and
routing topology. Each scenario records:

```yaml
scenario:
  id: stable-id
  contracts: []
  initial_artifacts: []
  command: string
  expected_transition: string
  expected_writes: []
  forbidden_writes: []
  expected_stop_reason: string | null
  generation_and_roots: {}
  validation: []
```

## Intake Scenarios

| ID | Behavior |
|---|---|
| fresh-finding-intake | One source becomes one individually addressable finding; no selection. |
| multi-item-intake | Many caller-decided findings apply atomically in one ledger transaction. |
| duplicate-finding-intake | Caller-decided merge/update/no-op is idempotent. |
| duplicate-identities-in-one-request | Conflicting source identity blocks without partial write. |
| stale-ledger-revision | Expected file hash mismatch blocks. |
| receipt-write-failure-after-ledger-render | Original ledger remains or retry is deterministic. |
| intake-stops-before-planning | No selected dispatch or runway is created. |

## Planning Scenarios

| ID | Behavior |
|---|---|
| empty-ledger | Report no eligible work. |
| one-eligible-finding | Select exactly one bounded item. |
| multiple-eligible-findings | Select at most one; deferred items remain visible. |
| explicitly-requested-finding | Use requested existing item or block. |
| requested-missing-finding | Require add-to-ledger; do not infer external work. |
| vague-mixed-risk-finding | Split, block, or narrow before dispatch. |
| destructive-work-without-approval | Block before runnable runway. |
| selected-dispatch-exists | Do not select different work. |
| queued-runway-exists | Report and stop. |
| active-runway-exists | Report and stop. |
| stale-dispatch-source-revision | Block without creating a runway. |
| exactly-one-runway | One invocation creates at most one concrete runway. |
| planning-stops-before-implementation | No worker, code write, validation commit, or successor selection. |

## Planning Transaction Fault Injection

| ID | Failure boundary | Expected recovery |
|---|---|---|
| dispatch-write-before-selected-transition-failure | Dispatch exists, state transition fails | Diagnostic identifies recoverable selected preparation; retry is idempotent. |
| selected-transition-before-runway-write-failure | Selected state exists, runway absent | Next plan-batch resumes same dispatch only. |
| runway-write-before-queued-transition-failure | Runway exists, queue transition fails | Retry validates same runway and completes transition. |
| stale-runway-dispatch-revision | Runway source revision differs | Block; do not queue. |
| retry-after-partial-planning | Any supported partial state | No duplicate dispatch or runway. |

## Execution Scenarios

| ID | Behavior |
|---|---|
| start-queued-batch | Transition queued to active and execute current runway only. |
| resume-active-batch | Resume next incomplete slice without replay. |
| invalid-multiple-active-state | Block before worker delegation. |
| successful-slice | Scoped worker, focused validation, independent review, focused commit. |
| worker-scope-violation | Block and preserve unrelated files. |
| validation-failure | No review acceptance or commit. |
| review-failure | Recover in scope or stop. |
| stale-review-basis | Reviewer blocks. |
| dirty-file-conflict | Stop without reverting user work. |
| unexpected-head-movement | Recompute trusted diff or block. |
| missing-agent-support | Durable blocked result. |
| trigger-test-quality-review | Evidence review is integrated but not lifecycle owner. |

## Commit and Receipt Fault Injection

| ID | Failure boundary | Expected recovery |
|---|---|---|
| review-clean-then-head-changed | HEAD changes after clean review | Review becomes stale; no acceptance. |
| commit-succeeds-receipt-write-fails | Git commit exists, receipt missing | Recovery discovers exact commit and writes one idempotent receipt. |
| receipt-written-commit-missing | Receipt references absent commit | Block and reject evidence. |
| commit-in-wrong-repository | Commit occurs outside implementation target | Reject and stop. |
| unrelated-dirty-file-in-commit | Commit includes unowned change | Reject acceptance. |

## Closeout Scenarios

| ID | Behavior |
|---|---|
| successful-closeout | Final validation, review, commit, and closeout evidence exist. |
| missing-closeout-evidence | Do not clear queued/active state. |
| same-batch-reconciliation | Mutate only covered findings and pointers. |
| closeout-without-execution-evidence | Block. |
| no-successor-selection | Selected, queued, active successor remain null. |
| closeout-from-wrong-batch | Reject lineage mismatch. |
| closeout-from-wrong-generation | Reject generation mismatch. |
| retry-same-closeout | Idempotent receipt and state. |

## Closeout Fault Injection

| ID | Failure boundary | Expected recovery |
|---|---|---|
| closeout-written-reconciliation-fails | Closeout exists, ledger/pointers unchanged | Retry consumes same closeout exactly once. |
| ledger-reconciled-pointer-cleanup-fails | Findings updated, pointer cleanup fails | Diagnostic exposes partial state; retry is idempotent. |
| pointer-cleared-ledger-update-fails | Pointer mutation precedes finding mutation | Transaction design must reject or repair without losing batch identity. |

## Three-Root and Generation Isolation Scenarios

| ID | Expected proof |
|---|---|
| stable-session-generation-fingerprint | Installed links, stable root, commit, and CODEX_HOME agree. |
| candidate-session-generation-fingerprint | Candidate root, commit, and CODEX_HOME agree. |
| stable-helper-independent-of-candidate-cwd | Stable controlling script resolves from toolchain root. |
| stable-reference-independent-of-candidate-cwd | Skill reference resolves from toolchain root. |
| planning-write-outside-canonical-root | Rejected before write. |
| implementation-write-outside-candidate-root | Rejected before write. |
| candidate-cannot-write-canonical-root | Rejected by mechanism, not prompt convention. |
| worker-generation-matches-controller | Verified identity round trip. |
| reviewer-generation-matches-controller | Verified identity round trip. |
| runner-phases-share-expected-generation | Child process inherits expected identity. |
| generation-switch-during-operation | Block; no mixed-generation continuation. |
| changed-stable-control-needs-fresh-session | Current session stops before consuming changed control code. |

## Branch and Design Lineage Scenarios

| ID | Expected proof |
|---|---|
| candidate-based-on-latest-master | Candidate contains current live intake. |
| accepted-design-history-merged | Implementation branch contains accepted design ancestry. |
| imported-design-tree-match | Tree equals accepted snapshot before amendments. |
| mutable-design-branch-drift | Does not alter immutable authoritative source. |
| master-advances-during-batch | Explicitly block, integrate, or record; never silently diverge. |
| final-integration-preserves-candidate-toolchain | Merge into master does not alter accepted target content. |

## Candidate Validation-Lane Scenarios

| ID | Expected proof |
|---|---|
| candidate-fixture-only-planning | Fixture root used; canonical root unavailable for mutation. |
| candidate-schema-validation | Candidate schema and contract tests pass. |
| candidate-skill-trial | Fresh candidate session reports identity and writes fixture only. |
| candidate-real-ledger-write-attempt | Rejected. |

## Installer and Cutover Scenarios

| ID | Expected proof |
|---|---|
| clean-candidate-codex-home-install | Empty generation directory becomes complete candidate generation. |
| omitted-feature-removed | Retired feature is absent, not retained from previous state. |
| partial-install-failure | Default binding remains stable and complete. |
| stale-legacy-symlink-detected | Scan fails before switch. |
| atomic-default-switch-rehearsal | One binding changes; no mixed visible generation. |
| rollback-before-first-candidate-write | Stable binding restored. |
| pre-cutover-quiescence | No selected, queued, active, resumable, or concurrent writer. |
| final-default-switch | Stable controller remains pinned; future default becomes candidate. |
| fresh-candidate-read-only-diagnostic | Candidate proves identity and no legacy routes. |
| candidate-write-before-new-batch | Rejected. |
| stable-controller-reloads-after-switch | Forbidden. |
| stable-controller-closeout-after-switch | Same loaded controller closes CCFG-28 and stops. |
| rollback-after-target-write | Restore full compatible bundle or fail safely. |

## Physical Deletion Scenarios

| ID | Expected proof |
|---|---|
| clean-install-without-apr | No installed APR route. |
| clean-install-without-batch-runway | No installed Batch Runway route. |
| direct-old-command-unavailable | Invocation fails as retired surface. |
| runner-public-protocols-only | No old modes or hidden successor decision. |
| worker-reviewer-resolve-after-deletion | Contracts no longer depend on old paths. |
| active-old-name-scan-zero | No active/runtime match. |
| historical-old-name-classified | Allowed only in archived evidence. |
| archived-artifact-readable | Historical evidence remains inspectable. |
| archived-artifact-not-pickup-authority | Cannot become selected/active state. |

## Contract-First Format Scenarios

| ID | Expected proof |
|---|---|
| one-skill-contract-block | Exactly one canonical block. |
| required-fields | Missing field rejects. |
| duplicate-decision-owner | Reject. |
| support-mechanism-owns-human-decision | Reject. |
| unknown-reference | Reject. |
| reference-cycle | Reject. |
| reference-outside-toolchain-root | Reject. |
| unsupported-schema-version | Block. |
| optional-compatible-field | Accepted only by policy. |
| arbitrary-prose-semantic-check | Not claimed as deterministic validation. |
| narrow-skill-authoring-trial | Green. |
| branching-command-authoring-trial | Green. |

## `CURRENT.md` and Ledger Scenarios

| ID | Expected proof |
|---|---|
| current-exactly-one-canonical-block | Green. |
| current-stale-hash | Reject. |
| current-atomic-replace | No partial write. |
| current-prose-does-not-own-pointers | Green. |
| ledger-per-finding-parse | Green. |
| ledger-global-block-comparison | Evidence produced. |
| ledger-multi-item-atomic | Green. |
| ledger-derived-index-mismatch | Validation error. |
| ledger-concurrent-different-findings | Compare conflict behavior. |
| sqlite-projection-equivalence | Same projection from selected representation. |

## Test Classification Rules

Retain or rewrite tests that prove:

- public command behavior;
- schemas and state transitions;
- root and generation isolation;
- file effects and rollback;
- worker/reviewer boundaries;
- no successor selection;
- historical artifacts not becoming active.

Delete after migration when tests only prove:

- APR or Batch Runway directory presence;
- old mode names;
- command-owner dependency lists containing old owners;
- exact bridge prose;
- compatibility aliases with expired callers.

## Program Exit Evidence

```yaml
test_matrix_exit:
  contract_id_coverage_complete: true
  behavior_scenarios_green: true
  root_and_generation_scenarios_green: true
  fault_injection_green: true
  clean_install_and_cutover_green: true
  physical_deletion_green: true
  archived_history_readability_green: true
  topology_only_target_tests: 0
```
