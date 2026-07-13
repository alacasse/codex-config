# Behavioral Test Matrix

## Purpose

This matrix defines the workflow evidence required before and after ownership
migration. It proves externally meaningful behavior, state transitions, file
effects, and stop conditions without depending on current broad skill names,
mode names, routing prose, or manifest topology.

## Test Classifications

Use these classifications when reviewing current or new tests:

| Classification | Meaning | Default disposition |
|---|---|---|
| `behavioral` | Proves externally observable command, state, file, commit, or artifact behavior. | Preserve or rewrite against target interfaces. |
| `schema-contract` | Proves parseable versioned data, required fields, and supported values. | Preserve and extend. |
| `integration-workflow` | Proves multiple components cooperate through public interfaces. | Preserve or add. |
| `compatibility-contract` | Protects a named supported external compatibility promise. | Preserve only while the promise remains explicit. |
| `migration-retention` | Keeps a temporary old parser, wrapper, mode, or route alive. | Require caller and deletion condition; delete at cutover. |
| `topology-assertion` | Protects skill presence, dependency lists, paths, aliases, or implementation shape without proving behavior. | Rewrite or delete. |
| `text-contract` | Searches for expected phrases or headings. | Use only for small format checks; never as primary workflow proof. |
| `projection-reporting` | Proves derived reporting and staleness behavior. | Keep separate from canonical state proof. |

## Current Test Disposition

| Current test area | Classification | Target action |
|---|---|---|
| `tests/test_planning_state.py` current/validate protocol, blockers, path validation, stale projections | behavioral, schema-contract, projection-reporting | Preserve and adapt to final canonical structured artifacts and transition API. |
| Manifest link existence and dependency expansion | schema-contract | Preserve; update expected target dependencies. |
| Manifest assertions requiring command owners to depend on APR or Batch Runway | topology-assertion, migration-retention | Delete or rewrite as forbidden-dependency assertions. |
| `tests/test_skill_routing_rule_ownership.py` owner phrases and legacy owner presence | text-contract, topology-assertion | Retain only during early characterization; delete after target behavior tests exist. |
| `tests/test_batch_runway_create_spec_contract.py` active artifact relative-path rules | behavioral artifact invariant | Move to target artifact schema and active-artifact tests. |
| The same file's Batch Runway mode and reference phrase assertions | text-contract, topology-assertion | Delete or rewrite against `plan-batch` and `work-batch` contracts. |
| `tests/test_batch_lifecycle_guards.py` stale operational placeholder scan | behavioral repository invariant | Preserve. |
| The same file's exact old closeout-routing prose | text-contract, migration-retention | Delete after closeout behavior scenarios protect the target. |
| Worker and reviewer TOML result schema checks | schema-contract | Preserve and make mechanically validated where possible. |

## Fixture Rules

- Use temporary planning roots and repositories.
- Never run migration characterization against the active `docs/plans/` tree.
- Each fixture declares its canonical artifact format and revision.
- Tests must assert both expected writes and forbidden writes.
- Tests must identify the public command interface invoked.
- Scenario names remain stable even when implementation changes.
- Legacy-mode names appear only in migration-retention fixtures.
- Each scenario links to at least one behavior contract ID.

Recommended fixture layout:

```text
tests/fixtures/command-owner-workflows/
  empty-ledger/
  one-eligible-finding/
  multiple-eligible-findings/
  explicit-finding/
  vague-mixed-risk/
  selected-dispatch/
  queued-runway/
  active-runway/
  invalid-state/
  partial-execution/
  successful-closeout/
```

## Scenario Record Shape

```yaml
scenario: stable-name
contracts: []
initial_artifacts: []
command:
  interface: command-name/version
  input: {}
expected_transition: string | none
expected_writes: []
forbidden_writes: []
expected_stop:
  code: stable-code
  blocking: true | false
validation_evidence: []
```

## Intake Scenarios

### `fresh-finding-intake`

```yaml
scenario: fresh-finding-intake
contracts:
  - INTAKE-SOURCE-001
  - INTAKE-IDENTITY-002
  - INTAKE-NORMALIZE-003
  - INTAKE-MUTATE-004
  - INTAKE-STOP-005
initial_artifacts:
  - valid planning diagnostic
  - canonical ledger without the source identity
command:
  interface: add-to-ledger/v1
  input:
    source_type: github_issue
    source_identity: github:alacasse/codex-config#48
expected_transition: ledger_revision_increment
expected_writes:
  - one new finding or normalized merge
  - source identity and evidence pointer
  - ledger mutation receipt
forbidden_writes:
  - selected dispatch
  - runway
  - implementation files
  - closeout
expected_stop:
  code: intake_recorded
  blocking: false
validation_evidence:
  - resulting ledger schema valid
  - source identity is queryable
  - no selected, queued, or active state
```

### `duplicate-finding-intake`

```yaml
scenario: duplicate-finding-intake
contracts:
  - INTAKE-IDENTITY-002
  - INTAKE-MUTATE-004
initial_artifacts:
  - canonical ledger already containing the same stable source identity
command:
  interface: add-to-ledger/v1
  input:
    same_source_identity: true
expected_transition: merge_update_or_noop
expected_writes:
  - at most one existing finding update
  - mutation receipt identifying merge or no-op
forbidden_writes:
  - duplicate finding identity
  - selected dispatch
  - runway
expected_stop:
  code: duplicate_resolved
  blocking: false
validation_evidence:
  - exactly one canonical source identity remains
  - repeated invocation is idempotent
```

### `stale-ledger-revision`

```yaml
scenario: stale-ledger-revision
contracts:
  - INTAKE-MUTATE-004
  - STATE-TRANSITION-002
initial_artifacts:
  - canonical ledger revision newer than the caller's expected revision
command:
  interface: add-to-ledger/v1
  input:
    expected_revision: stale
expected_transition: none
expected_writes: []
forbidden_writes:
  - partial ledger update
  - selected state
expected_stop:
  code: stale_ledger_revision
  blocking: true
validation_evidence:
  - canonical ledger unchanged
  - actionable current revision returned
```

## Planning Scenarios

### `empty-ledger`

```yaml
scenario: empty-ledger
contracts:
  - PLAN-SOURCE-001
  - PLAN-SELECT-003
initial_artifacts:
  - valid idle state
  - canonical ledger with no eligible findings
command:
  interface: plan-batch/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - dispatch
  - runway
  - new finding
expected_stop:
  code: no_eligible_finding
  blocking: true
validation_evidence:
  - state revision unchanged
  - ledger revision unchanged
```

### `one-eligible-finding`

```yaml
scenario: one-eligible-finding
contracts:
  - PLAN-SOURCE-001
  - PLAN-SELECT-003
  - PLAN-DISPATCH-005
  - PLAN-RUNWAY-006
  - PLAN-RISK-007
  - PLAN-STOP-008
initial_artifacts:
  - valid idle state
  - one precise eligible ledger finding
command:
  interface: plan-batch/v1
  input: {}
expected_transition: idle_to_selected_to_queued
expected_writes:
  - one planning-dispatch/v1 artifact
  - one planning-runway/v1 artifact
  - selected and queued transition receipts
  - current-state projection or updated canonical pointer state
forbidden_writes:
  - second dispatch
  - second runway
  - implementation source changes
  - commits
expected_stop:
  code: runway_queued
  blocking: false
validation_evidence:
  - dispatch source revision matches ledger
  - runway source revision matches dispatch
  - all slices and validations schema-valid
  - successor selection absent
```

### `multiple-eligible-findings`

```yaml
scenario: multiple-eligible-findings
contracts:
  - PLAN-SELECT-003
  - PLAN-DISPATCH-005
initial_artifacts:
  - valid idle state
  - multiple eligible ledger findings
command:
  interface: plan-batch/v1
  input: {}
expected_transition: idle_to_selected_to_queued
expected_writes:
  - exactly one dispatch
  - exactly one runway
  - explicit deferred finding IDs or rationale
forbidden_writes:
  - multiple selected batches
  - hidden closure of unselected findings
expected_stop:
  code: runway_queued
  blocking: false
validation_evidence:
  - one selected batch identity
  - unselected findings remain visible
```

### `explicitly-requested-finding`

```yaml
scenario: explicitly-requested-finding
contracts:
  - PLAN-SOURCE-001
  - PLAN-SELECT-003
initial_artifacts:
  - valid idle state
  - requested finding exists and is eligible
command:
  interface: plan-batch/v1
  input:
    requested_finding_id: CCFG-X
expected_transition: idle_to_selected_to_queued
expected_writes:
  - dispatch covering requested finding
  - runway for the same dispatch
forbidden_writes:
  - silent substitution of another finding
expected_stop:
  code: runway_queued
  blocking: false
validation_evidence:
  - dispatch lineage includes requested finding
```

### `requested-missing-finding`

```yaml
scenario: requested-missing-finding
contracts:
  - INTAKE-SOURCE-001
  - PLAN-SOURCE-001
initial_artifacts:
  - valid idle state
  - requested finding absent from canonical ledger
command:
  interface: plan-batch/v1
  input:
    requested_finding_id: missing
expected_transition: none
expected_writes: []
forbidden_writes:
  - new ledger finding
  - dispatch
  - runway
expected_stop:
  code: intake_required
  blocking: true
validation_evidence:
  - add-to-ledger named as the separate next command
  - no automatic intake performed
```

### `vague-mixed-risk-finding`

```yaml
scenario: vague-mixed-risk-finding
contracts:
  - PLAN-SCOPE-004
  - PLAN-RISK-007
initial_artifacts:
  - idle state
  - finding mixing discovery, decision, migration, and deletion without approval
command:
  interface: plan-batch/v1
  input:
    requested_finding_id: vague-row
expected_transition: blocked_or_ledger_refinement_only
expected_writes:
  - optional explicit split, block, or narrow decision receipt
  - optional ledger refinement with revision check
forbidden_writes:
  - runnable destructive dispatch
  - runnable destructive runway
  - implementation changes
expected_stop:
  code: unsafe_scope_requires_shaping
  blocking: true
validation_evidence:
  - no approval gate invented
  - no destructive work silently authorized
```

### `destructive-work-without-approval`

```yaml
scenario: destructive-work-without-approval
contracts:
  - PLAN-SCOPE-004
  - PLAN-RISK-007
initial_artifacts:
  - otherwise precise finding requiring destructive cleanup
  - no valid approval gate
command:
  interface: plan-batch/v1
  input: {}
expected_transition: none_or_blocked
expected_writes:
  - blocker receipt
forbidden_writes:
  - queued destructive runway
expected_stop:
  code: missing_approval_gate
  blocking: true
validation_evidence:
  - finding remains open or blocked
```

### `selected-dispatch-exists`

```yaml
scenario: selected-dispatch-exists
contracts:
  - PLAN-ACTIVE-002
  - PLAN-DISPATCH-005
  - PLAN-RUNWAY-006
initial_artifacts:
  - valid selected dispatch
  - no runway for that dispatch
command:
  interface: plan-batch/v1
  input: {}
expected_transition: selected_to_queued
expected_writes:
  - exactly one runway for the existing dispatch
  - queue transition receipt
forbidden_writes:
  - new selection
  - replacement dispatch
expected_stop:
  code: runway_queued
  blocking: false
validation_evidence:
  - runway source revision matches existing dispatch
```

### `queued-runway-exists`

```yaml
scenario: queued-runway-exists
contracts:
  - PLAN-ACTIVE-002
  - PLAN-STOP-008
initial_artifacts:
  - valid queued runway
command:
  interface: plan-batch/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - replacement runway
  - second batch
  - implementation
expected_stop:
  code: queued_runway_exists
  blocking: false
validation_evidence:
  - queued artifact unchanged
```

### `active-runway-exists`

```yaml
scenario: active-runway-exists
contracts:
  - PLAN-ACTIVE-002
  - PLAN-STOP-008
initial_artifacts:
  - valid active runway
command:
  interface: plan-batch/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - replacement runway
  - second selection
  - execution changes
expected_stop:
  code: active_runway_exists
  blocking: false
validation_evidence:
  - active artifact unchanged
```

## State Scenarios

### `current-state-diagnostic`

```yaml
scenario: current-state-diagnostic
contracts:
  - STATE-DIAG-001
initial_artifacts:
  - valid hybrid current state and canonical artifacts
command:
  interface: planning-state/inspect-v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - any durable file
expected_stop:
  code: diagnostic_ready
  blocking: false
validation_evidence:
  - normalized program, ledger, selected, queued, active, blockers, and policy
```

### `invalid-multiple-active-state`

```yaml
scenario: invalid-multiple-active-state
contracts:
  - STATE-DIAG-001
  - STATE-TRANSITION-002
initial_artifacts:
  - selected dispatch and active runway both declared current
command:
  interface: planning-state/inspect-v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - automatic conflict repair
expected_stop:
  code: multiple_active_artifacts
  blocking: true
validation_evidence:
  - both conflicting sources identified
```

### `illegal-state-transition`

```yaml
scenario: illegal-state-transition
contracts:
  - STATE-TRANSITION-002
initial_artifacts:
  - idle lifecycle state
command:
  interface: planning-state/apply-transition-v1
  input:
    operation: active_to_completed
expected_transition: rejected
expected_writes: []
forbidden_writes:
  - partial state update
expected_stop:
  code: illegal_transition
  blocking: true
validation_evidence:
  - current state unchanged
```

### `historical-artifact-does-not-override-current`

```yaml
scenario: historical-artifact-does-not-override-current
contracts:
  - STATE-HISTORY-004
initial_artifacts:
  - current state declares no queued runway
  - historical archived runway exists
command:
  interface: planning-state/inspect-v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - historical runway promotion
expected_stop:
  code: diagnostic_ready_with_warning
  blocking: false
validation_evidence:
  - queued runway remains null
  - historical artifact reported only as evidence or warning
```

## Execution Scenarios

### `start-queued-batch`

```yaml
scenario: start-queued-batch
contracts:
  - EXEC-CURRENT-001
  - STATE-TRANSITION-002
initial_artifacts:
  - valid queued runway
command:
  interface: work-batch/v1
  input: {}
expected_transition: queued_to_active
expected_writes:
  - active transition receipt
  - execution state for first pending slice
forbidden_writes:
  - new dispatch
  - new runway
  - successor selection
expected_stop:
  code: execution_started_or_completed
  blocking: false
validation_evidence:
  - same runway identity remains current
```

### `successful-slice`

```yaml
scenario: successful-slice
contracts:
  - EXEC-WORKER-003
  - EXEC-VALIDATE-004
  - EXEC-REVIEW-005
  - EXEC-COMMIT-006
initial_artifacts:
  - active runway with one pending routine slice
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_remains_or_completes
expected_writes:
  - worker result
  - validation evidence
  - independent reviewer result
  - focused commit
  - commit receipt
  - updated remaining-work state
forbidden_writes:
  - unrelated dirty files in commit
  - worker-authored commit
  - worker self-review
expected_stop:
  code: slice_committed_or_batch_completed
  blocking: false
validation_evidence:
  - exact commit hash
  - exact reviewer diff basis
```

### `validation-failure`

```yaml
scenario: validation-failure
contracts:
  - EXEC-VALIDATE-004
  - EXEC-RECOVER-007
  - EXEC-STOP-008
initial_artifacts:
  - active runway
  - worker result with changed files
  - required validation fails
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_unchanged
expected_writes:
  - failure evidence
  - optional delegated in-scope fix attempt evidence
forbidden_writes:
  - accepted commit while required validation fails
  - next slice execution
expected_stop:
  code: validation_failed
  blocking: true
validation_evidence:
  - failing command and status class recorded
```

### `review-failure`

```yaml
scenario: review-failure
contracts:
  - EXEC-REVIEW-005
  - EXEC-RECOVER-007
initial_artifacts:
  - active runway
  - required validation green
  - reviewer returns required findings
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_unchanged
expected_writes:
  - reviewer findings
  - optional delegated fix-loop evidence
forbidden_writes:
  - accepted commit before clean re-review
  - next slice execution
expected_stop:
  code: review_findings
  blocking: true
validation_evidence:
  - reviewer diff basis matches current diff
```

### `stale-review-basis`

```yaml
scenario: stale-review-basis
contracts:
  - EXEC-REVIEW-005
  - EXEC-RECOVER-007
initial_artifacts:
  - reviewer result references an old commit or diff
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_unchanged
expected_writes:
  - stale-review anomaly or blocker evidence
forbidden_writes:
  - commit acceptance
expected_stop:
  code: stale_review_basis
  blocking: true
validation_evidence:
  - current HEAD and diff basis recorded
```

### `dirty-file-conflict`

```yaml
scenario: dirty-file-conflict
contracts:
  - EXEC-COMMIT-006
  - EXEC-RECOVER-007
initial_artifacts:
  - active slice overlaps unrelated dirty user work
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_unchanged
expected_writes:
  - conflict classification evidence
forbidden_writes:
  - revert of user work
  - mixed commit
expected_stop:
  code: dirty_file_conflict
  blocking: true
validation_evidence:
  - conflicting paths named
```

### `partial-execution`

```yaml
scenario: partial-execution
contracts:
  - EXEC-RESUME-002
  - EXEC-COMMIT-006
initial_artifacts:
  - active runway
  - earlier slices committed and archived
  - later slice pending
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_remains_or_completes
expected_writes:
  - evidence only for next incomplete slice
forbidden_writes:
  - rerun or duplicate commit for completed slices
expected_stop:
  code: next_slice_processed
  blocking: false
validation_evidence:
  - completed commit lineage preserved
```

### `resume-after-interruption`

```yaml
scenario: resume-after-interruption
contracts:
  - EXEC-RESUME-002
initial_artifacts:
  - active runway with durable receipts and incomplete slice
command:
  interface: work-batch/v1
  input:
    fresh_session: true
expected_transition: active_remains_or_completes
expected_writes:
  - new evidence from next incomplete slice only
forbidden_writes:
  - reset of runway progress
  - new batch selection
expected_stop:
  code: resumed_same_runway
  blocking: false
validation_evidence:
  - prior receipts consumed without transcript replay
```

### `missing-agent-support`

```yaml
scenario: missing-agent-support
contracts:
  - EXEC-STOP-008
initial_artifacts:
  - active runway requiring worker and reviewer
  - registered agent support unavailable
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_unchanged
expected_writes:
  - blocker evidence
forbidden_writes:
  - coordinator fallback implementation
  - commit
expected_stop:
  code: required_agent_unavailable
  blocking: true
validation_evidence:
  - missing role named
```

## Closeout Scenarios

### `successful-closeout`

```yaml
scenario: successful-closeout
contracts:
  - CLOSE-FINAL-001
  - CLOSE-RECONCILE-002
  - CLOSE-NEXT-003
initial_artifacts:
  - active runway with all intended slices clean and committed
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_to_completed
expected_writes:
  - planning-closeout/v1 artifact
  - completed-slice evidence
  - final validation and review evidence
  - finding reconciliation mutation
  - lifecycle completion receipt
forbidden_writes:
  - successor dispatch
  - successor runway
expected_stop:
  code: batch_completed
  blocking: false
validation_evidence:
  - no unresolved operational placeholders
  - `successor_selected` is false
```

### `missing-closeout-evidence`

```yaml
scenario: missing-closeout-evidence
contracts:
  - CLOSE-FINAL-001
initial_artifacts:
  - implementation appears complete
  - required final validation or review evidence absent
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_unchanged
expected_writes:
  - blocker evidence
forbidden_writes:
  - completed transition
  - finding closure
expected_stop:
  code: incomplete_closeout_evidence
  blocking: true
validation_evidence:
  - missing evidence types named
```

### `closeout-without-execution-evidence`

```yaml
scenario: closeout-without-execution-evidence
contracts:
  - CLOSE-RECONCILE-002
initial_artifacts:
  - selected dispatch and queued runway
  - no execution closeout evidence
command:
  interface: work-batch/v1
  input:
    requested_action: closeout
expected_transition: none
expected_writes:
  - blocker evidence
forbidden_writes:
  - queued pointer clearing
  - finding closure
expected_stop:
  code: execution_evidence_required
  blocking: true
validation_evidence:
  - queued runway remains current
```

### `same-batch-reconciliation`

```yaml
scenario: same-batch-reconciliation
contracts:
  - CLOSE-RECONCILE-002
initial_artifacts:
  - valid completed closeout evidence
  - covered findings still pending
  - active pointers reference the completed batch
command:
  interface: work-batch/v1
  input: {}
expected_transition: active_to_completed
expected_writes:
  - exact covered finding updates
  - selected, queued, and active pointer cleanup for the same batch
  - latest closeout pointer
  - reconciliation receipt
forbidden_writes:
  - unrelated finding mutation
  - successor selection
expected_stop:
  code: same_batch_reconciled
  blocking: false
validation_evidence:
  - closeout source revision and batch identity match
```

### `no-successor-selection`

```yaml
scenario: no-successor-selection
contracts:
  - CLOSE-NEXT-003
initial_artifacts:
  - successful same-batch closeout
  - other open findings remain in ledger
command:
  interface: work-batch/v1
  input: {}
expected_transition: completed_idle
expected_writes: []
forbidden_writes:
  - selected successor dispatch
  - queued successor runway
expected_stop:
  code: batch_completed_no_successor_selected
  blocking: false
validation_evidence:
  - selected, queued, and active pointers are null
  - open findings remain visible
```

## Specialized Evidence Scenarios

### `legacy-evidence-no-state-writes`

```yaml
scenario: legacy-evidence-no-state-writes
contracts:
  - EVIDENCE-LEGACY-001
initial_artifacts:
  - active or idle planning state
command:
  interface: legacy-removal/evidence
  input:
    suspect_surface: example
expected_transition: none
expected_writes:
  - optional evidence artifact only
forbidden_writes:
  - program queue mutation
  - selected dispatch
  - runway
  - closeout
expected_stop:
  code: evidence_ready_or_blocked
  blocking: false
validation_evidence:
  - no lifecycle revision change
```

### `deletion-evidence-no-state-writes`

```yaml
scenario: deletion-evidence-no-state-writes
contracts:
  - EVIDENCE-DEAD-002
initial_artifacts:
  - suspect compatibility surface and tests
command:
  interface: dead-surface-audit/evidence
  input: {}
expected_transition: none
expected_writes:
  - evidence report only
forbidden_writes:
  - deletion
  - approval
  - queue mutation
expected_stop:
  code: evidence_classified
  blocking: false
validation_evidence:
  - canonical evidence status used
```

### `test-quality-review-no-state-writes`

```yaml
scenario: test-quality-review-no-state-writes
contracts:
  - EVIDENCE-TEST-003
initial_artifacts:
  - test diff and relevant behavior contract
command:
  interface: test-quality-review/v1
  input:
    mode: delta-only
expected_transition: none
expected_writes:
  - review evidence only
forbidden_writes:
  - implementation files
  - queue mutation
  - commit
expected_stop:
  code: review_complete
  blocking: false
validation_evidence:
  - compact result schema valid
```

## Contract-First Format Scenarios

### `duplicate-machine-fact-owner`

```yaml
scenario: duplicate-machine-fact-owner
contracts:
  - STATE-CANONICAL-003
initial_artifacts:
  - two skill contracts claiming the same durable fact
command:
  interface: validate-skill-contracts/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - automatic ownership resolution
expected_stop:
  code: duplicate_durable_fact_owner
  blocking: true
validation_evidence:
  - both claimants identified
```

### `structured-prose-contradiction`

```yaml
scenario: structured-prose-contradiction
contracts:
  - STATE-CANONICAL-003
initial_artifacts:
  - structured batch kind is destructive-cleanup
  - independently defined prose status says behavior-preserving
command:
  interface: validate-planning-artifacts/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - silent preference for prose
expected_stop:
  code: contradictory_operational_fact
  blocking: true
validation_evidence:
  - canonical structured field identified
```

### `unknown-slice-dependency`

```yaml
scenario: unknown-slice-dependency
contracts:
  - PLAN-RUNWAY-006
initial_artifacts:
  - runway with a dependency on a missing slice ID
command:
  interface: validate-planning-artifacts/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - queue transition
expected_stop:
  code: unknown_slice_dependency
  blocking: true
validation_evidence:
  - missing dependency ID named
```

### `write-scope-overlap`

```yaml
scenario: write-scope-overlap
contracts:
  - PLAN-RUNWAY-006
initial_artifacts:
  - independent parallel-candidate slices with overlapping declared write paths
command:
  interface: validate-planning-artifacts/v1
  input: {}
expected_transition: none
expected_writes: []
forbidden_writes:
  - parallel authorization
expected_stop:
  code: overlapping_write_scope
  blocking: true
validation_evidence:
  - conflicting slices and paths identified
```

This scenario validates future-safe data without authorizing parallel execution.

## Required Test Layers

### Unit tests

- parsing and contract block location;
- schema validation;
- lifecycle transitions;
- revision checks;
- path resolution;
- ledger mutation and idempotence;
- dependency graph validation;
- risk and validation class validation;
- closeout consistency.

### Command integration tests

- add-to-ledger against temporary ledger fixtures;
- plan-batch against each state branch;
- work-batch against fake or controlled agent and Git boundaries;
- stable structured stop results.

### End-to-end workflow tests

- fresh finding through intake, plan, work, and closeout;
- interruption and resume;
- validation and review failure;
- deletion test after old owner removal.

### Architecture dependency tests

- no command owner depends on APR or Batch Runway after its cutover phase;
- planning-state does not import or invoke workflow decisions;
- evidence skills cannot mutate planning lifecycle;
- no new active artifact uses retired mode names;
- only one owner claims each durable fact.

## Migration Test Expiry

Every migration-only test must declare:

```yaml
migration_test:
  caller_or_surface: exact legacy path
  reason: why temporary compatibility is needed
  removal_condition:
    - measurable condition
  owner: migration phase
```

A migration test without an expiry condition becomes topology sediment and must
be rejected.
