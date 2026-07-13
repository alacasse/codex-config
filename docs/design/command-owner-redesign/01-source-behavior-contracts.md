# Source Behavior Contracts

## Purpose

This document extracts implementation-neutral behavior from the current ledger
and batch workflow system. The target architecture must preserve these
contracts unless a later accepted decision explicitly changes one.

The contracts describe externally meaningful behavior, durable state, failure
semantics, and operational safety. They do not preserve current skill names,
mode names, routing chains, file splits, or text assertions.

## Contract Record Shape

```yaml
id: stable-contract-id
status: current | target-only | deprecated | unknown
classification: verified-current | documented-intent | inference | target-decision
contract: implementation-neutral rule
target_implication: required target behavior
validation:
  - scenario or mechanical proof
source_evidence:
  - repository path
```

## Intake Contracts

### INTAKE-SOURCE-001 — Fresh work crosses one explicit ingestion boundary

```yaml
id: INTAKE-SOURCE-001
status: current
classification: verified-current
contract: >-
  Fresh user text, GitHub issues, tickets, ADR follow-ups, review findings,
  transcripts, and external skill outputs are candidate work or evidence until
  an explicit intake operation records selected work in the canonical program
  ledger.
target_implication: >-
  plan-batch and work-batch must never silently convert fresh external material
  into executable backlog.
validation:
  - fresh-finding-intake
  - requested-missing-finding
source_evidence:
  - skills/add-to-ledger/SKILL.md
  - skills/plan-batch/SKILL.md
  - docs/skill-routing-contract.md
```

### INTAKE-IDENTITY-002 — Preserve source identity

```yaml
id: INTAKE-IDENTITY-002
status: current
classification: verified-current
contract: >-
  Intake preserves enough source identity to distinguish, revisit, and merge the
  finding without inventing a new identity in a later session.
target_implication: >-
  The intake contract must represent source type, external identifier when
  present, title, URL or path, and compact evidence pointers.
validation:
  - fresh-finding-intake
  - duplicate-finding-intake
source_evidence:
  - skills/add-to-ledger/SKILL.md
  - docs/workflow-guide.md
```

### INTAKE-NORMALIZE-003 — Produce an individually addressable finding

```yaml
id: INTAKE-NORMALIZE-003
status: current
classification: verified-current
contract: >-
  A durable finding must be individually addressable and contain enough scope,
  status, evidence, and next-action context for later planning.
target_implication: >-
  Intake may normalize wording and structure, but it must not silently authorize
  destructive, migration, demotion, or contract-narrowing work that the source
  did not authorize.
validation:
  - fresh-finding-intake
  - vague-mixed-risk-finding
source_evidence:
  - skills/add-to-ledger/SKILL.md
  - skills/architecture-program-runway/SKILL.md
```

### INTAKE-MUTATE-004 — Apply one canonical ledger mutation

```yaml
id: INTAKE-MUTATE-004
status: current
classification: inference
contract: >-
  Intake creates, updates, merges, or no-ops against one canonical program
  ledger without creating a competing executable backlog.
target_implication: >-
  The target needs an explicit ledger mutation contract with duplicate detection,
  revision checks, idempotence, and a compact mutation receipt.
validation:
  - fresh-finding-intake
  - duplicate-finding-intake
  - stale-ledger-revision
source_evidence:
  - docs/plans/programs/codex-config/LEDGER.md
  - docs/workflow-guide.md
```

### INTAKE-STOP-005 — Intake stops before planning

```yaml
id: INTAKE-STOP-005
status: current
classification: verified-current
contract: >-
  Intake does not select a batch, create a dispatch, create a runway, execute a
  slice, or close a finding without closeout evidence.
target_implication: >-
  Successful intake leaves the finding in ledger state and ends the command.
validation:
  - fresh-finding-intake
source_evidence:
  - skills/add-to-ledger/SKILL.md
```

## Planning Contracts

### PLAN-SOURCE-001 — The canonical ledger is the executable backlog

```yaml
id: PLAN-SOURCE-001
status: current
classification: verified-current
contract: >-
  plan-batch reads executable work only from the canonical current program
  ledger or from already selected, queued, or active state rooted in that ledger.
target_implication: >-
  External sources may supply evidence only when the selected ledger finding
  points to them.
validation:
  - empty-ledger
  - one-eligible-finding
  - requested-missing-finding
source_evidence:
  - skills/plan-batch/SKILL.md
  - docs/skill-routing-contract.md
```

### PLAN-ACTIVE-002 — Existing active state has precedence

```yaml
id: PLAN-ACTIVE-002
status: current
classification: verified-current
contract: >-
  A selected dispatch, queued runway, or active runway prevents selection of a
  different batch.
target_implication: >-
  The planning command must branch from a normalized current-state diagnostic
  before reading backlog candidates.
validation:
  - selected-dispatch-exists
  - queued-runway-exists
  - active-runway-exists
source_evidence:
  - skills/plan-batch/SKILL.md
  - skills/planning-state/SKILL.md
```

### PLAN-SELECT-003 — Select at most one bounded batch

```yaml
id: PLAN-SELECT-003
status: current
classification: verified-current
contract: >-
  One invocation selects at most one bounded set of ledger work and never emits
  multiple runnable batches.
target_implication: >-
  Candidate ranking and grouping are semantic decisions owned by plan-batch,
  while state and artifact mechanisms only validate and persist the decision.
validation:
  - one-eligible-finding
  - multiple-eligible-findings
  - explicitly-requested-finding
source_evidence:
  - skills/plan-batch/SKILL.md
  - skills/architecture-program-runway/SKILL.md
```

### PLAN-SCOPE-004 — Unsafe ambiguity is split, blocked, or narrowed

```yaml
id: PLAN-SCOPE-004
status: current
classification: verified-current
contract: >-
  A finding that mixes discovery, classification, decisions, migration,
  demotion, cleanup, deletion, or contract narrowing without explicit owner,
  risk, approval, and acceptance boundaries must be split, blocked, or narrowed
  before dispatch or runway creation.
target_implication: >-
  Exactly one target owner must make this decision. The target owner is
  plan-batch.
validation:
  - vague-mixed-risk-finding
  - destructive-work-without-approval
source_evidence:
  - skills/plan-batch/SKILL.md
  - skills/architecture-program-runway/SKILL.md
  - docs/plans/programs/codex-config/batches/ccfg-15-vague-ledger-row-splitting/closeout.md
```

### PLAN-DISPATCH-005 — Selection produces a durable dispatch contract

```yaml
id: PLAN-DISPATCH-005
status: current
classification: verified-current
contract: >-
  The selected batch has a compact durable handoff that identifies its source
  ledger, included and deferred findings, goal, owner seam, risk, dependencies,
  stop conditions, and expected runway path.
target_implication: >-
  The dispatch remains a separate artifact, but its existence must not imply a
  separate workflow owner.
validation:
  - one-eligible-finding
  - selected-dispatch-exists
source_evidence:
  - skills/architecture-program-runway/SKILL.md
  - skills/architecture-program-runway/references/program-ledger-template.md
  - skills/planning-artifacts/SKILL.md
```

### PLAN-RUNWAY-006 — Produce one concrete execution contract

```yaml
id: PLAN-RUNWAY-006
status: current
classification: verified-current
contract: >-
  Planning produces exactly one concrete runway for the selected dispatch. The
  runway defines bounded slices, sequencing, allowed scope, validation,
  delegation, risk, review, commits, recovery, and closeout expectations.
target_implication: >-
  Runway specification belongs to plan-batch. A renderer or schema validator may
  apply the decision but may not design the batch.
validation:
  - selected-dispatch-exists
  - one-eligible-finding
source_evidence:
  - skills/batch-runway/SKILL.md
  - skills/batch-runway/references/create-spec.md
```

### PLAN-RISK-007 — Risk and validation are explicit before execution

```yaml
id: PLAN-RISK-007
status: current
classification: verified-current
contract: >-
  New dispatches and runways declare a batch kind, relevant slice risk classes,
  required approval gates, validation commands, and validation status classes
  before execution begins.
target_implication: >-
  plan-batch owns selection of these values; schemas and profile catalogs verify
  supported values and completeness.
validation:
  - destructive-work-without-approval
  - validation-classification
source_evidence:
  - skills/batch-runway/references/create-spec.md
  - docs/plans/programs/codex-config/batches/ccfg-13-validation-command-status/closeout.md
  - docs/plans/programs/codex-config/batches/ccfg-14-batch-kind-slice-risk/closeout.md
```

### PLAN-STOP-008 — Planning stops before implementation

```yaml
id: PLAN-STOP-008
status: current
classification: verified-current
contract: >-
  Planning never executes a slice, commits implementation, or selects successor
  work after producing or reporting the current batch state.
target_implication: >-
  A successful new plan ends in queued state.
validation:
  - one-eligible-finding
  - queued-runway-exists
source_evidence:
  - skills/plan-batch/SKILL.md
```

## Execution Contracts

### EXEC-CURRENT-001 — Execute only the current runway

```yaml
id: EXEC-CURRENT-001
status: current
classification: verified-current
contract: >-
  work-batch consumes exactly the current queued or active runway. It does not
  create findings, select different ledger work, or create a new runway except
  through an explicitly authorized recovery replan.
target_implication: >-
  Execution begins from normalized state and a validated runway identity.
validation:
  - start-queued-batch
  - resume-active-batch
  - invalid-multiple-active-state
source_evidence:
  - skills/work-batch/SKILL.md
```

### EXEC-RESUME-002 — Resume at the next incomplete slice

```yaml
id: EXEC-RESUME-002
status: current
classification: verified-current
contract: >-
  After interruption, clarification, approval, permission change, or fresh
  session pickup, execution resumes the same runway at the next incomplete
  ledger row rather than restarting completed work.
target_implication: >-
  Completed-slice evidence and remaining-work state must be durable and
  independently readable.
validation:
  - partial-execution
  - resume-after-interruption
source_evidence:
  - skills/batch-runway/SKILL.md
  - skills/batch-runway/references/execute-recovery-v1.md
```

### EXEC-WORKER-003 — Implementation is delegated to a scoped worker

```yaml
id: EXEC-WORKER-003
status: current
classification: verified-current
contract: >-
  Each implementation slice is delegated to a coding worker constrained by the
  selected slice, allowed files, dirty-file policy, validation scope, and stop
  conditions.
target_implication: >-
  The worker remains a narrow mechanism and owns no batch lifecycle, commit,
  review, ledger, or successor decisions.
validation:
  - successful-slice
  - worker-scope-violation
source_evidence:
  - agents/runway_worker.toml
  - skills/batch-runway/references/execute-slice-core-v1.md
```

### EXEC-VALIDATE-004 — Validation gates acceptance

```yaml
id: EXEC-VALIDATE-004
status: current
classification: verified-current
contract: >-
  Focused and selected-profile validation is evaluated before review and commit.
  Failed, unavailable, conditional, diagnostic-only, and known-red results are
  reported according to their declared status rather than silently treated as
  green.
target_implication: >-
  No commit may be accepted while required validation remains failed or
  unresolved.
validation:
  - validation-failure
  - validation-classification
source_evidence:
  - skills/batch-runway/references/create-spec.md
  - skills/batch-runway/references/execute-slice-core-v1.md
```

### EXEC-REVIEW-005 — Independent review gates commit

```yaml
id: EXEC-REVIEW-005
status: current
classification: verified-current
contract: >-
  A reviewer distinct from the implementation worker inspects the exact current
  diff basis and required evidence before a slice is accepted.
target_implication: >-
  A stale, missing, or materially incomplete review basis blocks acceptance.
validation:
  - review-failure
  - stale-review-basis
  - successful-slice
source_evidence:
  - agents/runway_reviewer.toml
  - skills/batch-runway/references/execute-slice-core-v1.md
```

### EXEC-COMMIT-006 — Commit focused accepted slices

```yaml
id: EXEC-COMMIT-006
status: current
classification: verified-current
contract: >-
  A clean, validated, reviewed slice is committed as a focused unit. Commit
  evidence records the exact commit or accepted range and excludes unrelated
  dirty work.
target_implication: >-
  Commit handling is a narrow mechanism invoked by work-batch after the command
  owner accepts the slice.
validation:
  - successful-slice
  - dirty-file-conflict
source_evidence:
  - skills/batch-runway/SKILL.md
  - skills/batch-runway/references/execute-slice-core-v1.md
```

### EXEC-RECOVER-007 — Recovery preserves scope and evidence integrity

```yaml
id: EXEC-RECOVER-007
status: current
classification: verified-current
contract: >-
  Validation failure, review findings, dirty-file conflict, unexpected HEAD or
  diff movement, missing agents, insufficient handoff, or unresolved ambiguity
  enters an explicit recovery path. Recovery does not widen scope silently or
  discard user work.
target_implication: >-
  work-batch owns the recovery decision. Workers may implement in-scope fixes;
  mechanisms report evidence and enforce invariants.
validation:
  - validation-failure
  - review-failure
  - dirty-file-conflict
  - unexpected-head-movement
source_evidence:
  - skills/batch-runway/references/execute-recovery-v1.md
```

### EXEC-STOP-008 — Unsafe execution stops durably

```yaml
id: EXEC-STOP-008
status: current
classification: verified-current
contract: >-
  Execution stops on unresolved ambiguity, scope drift, repeatedly unresolved
  validation, untrusted review evidence, missing required agents, missing
  project values, approval blockers, or conflicting dirty files.
target_implication: >-
  The stop result records the current slice, touched files, validation and review
  state, blocker, and next safe action.
validation:
  - invalid-planning-state
  - validation-failure
  - missing-agent-support
source_evidence:
  - skills/batch-runway/SKILL.md
  - skills/batch-runway/references/execute-recovery-v1.md
```

## Closeout Contracts

### CLOSE-FINAL-001 — Final validation and evidence are required

```yaml
id: CLOSE-FINAL-001
status: current
classification: verified-current
contract: >-
  Completion requires final validation, known review state, commit evidence,
  closeout evidence, completed-slice evidence, cleanup-residue classification,
  and removal of unresolved operational placeholders.
target_implication: >-
  A batch is not complete merely because all implementation slices ran.
validation:
  - successful-closeout
  - missing-closeout-evidence
  - stale-placeholder-closeout
source_evidence:
  - skills/batch-runway/references/finalize-batch-v1.md
  - tests/test_batch_lifecycle_guards.py
```

### CLOSE-RECONCILE-002 — Reconcile the same batch

```yaml
id: CLOSE-RECONCILE-002
status: current
classification: verified-current
contract: >-
  After concrete execution closeout exists, the completed batch's findings,
  selected or queued pointers, active state, queue metadata, and latest closeout
  are reconciled from that evidence.
target_implication: >-
  work-batch owns the closeout decision and invokes explicit state and ledger
  mechanisms to apply it.
validation:
  - same-batch-reconciliation
  - closeout-without-execution-evidence
source_evidence:
  - skills/work-batch/SKILL.md
  - skills/architecture-program-runway/SKILL.md
```

### CLOSE-NEXT-003 — Do not select successor work

```yaml
id: CLOSE-NEXT-003
status: current
classification: verified-current
contract: >-
  Same-batch reconciliation must not select, dispatch, refresh, create, or prepare
  successor work. A later explicit plan-batch request owns successor selection.
target_implication: >-
  Completed closeout ends in no selected, queued, or active successor created by
  work-batch.
validation:
  - no-successor-selection
source_evidence:
  - skills/work-batch/SKILL.md
  - docs/workflow-guide.md
```

## Durable State Contracts

### STATE-DIAG-001 — Fresh agents receive normalized current facts

```yaml
id: STATE-DIAG-001
status: current
classification: verified-current
contract: >-
  A fresh session can determine the planning root, active program, canonical
  ledger, selected dispatch, queued runway, active runway, blockers, policy,
  latest closeout, and next safe action without historical filename inference.
target_implication: >-
  Command owners consume a versioned normalized diagnostic before making
  semantic decisions.
validation:
  - current-state-diagnostic
  - missing-current-file
  - historical-artifact-does-not-override-current
source_evidence:
  - skills/planning-state/SKILL.md
  - scripts/planning_state.py
  - tests/test_planning_state.py
```

### STATE-TRANSITION-002 — State changes are explicit and validated

```yaml
id: STATE-TRANSITION-002
status: current
classification: inference
contract: >-
  Durable lifecycle mutations use named transitions, validate expected current
  state and artifact lineage, reject conflicts, and produce a receipt.
target_implication: >-
  planning-state becomes the state-machine authority but never chooses which
  finding, batch, slice, recovery action, or successor should be selected.
validation:
  - legal-state-transitions
  - illegal-state-transition
  - stale-state-revision
source_evidence:
  - scripts/planning_state.py
  - skills/planning-state/references/state-fixtures.md
```

### STATE-CANONICAL-003 — One canonical owner per machine fact

```yaml
id: STATE-CANONICAL-003
status: target-only
classification: target-decision
contract: >-
  Each machine-relevant fact has one canonical artifact or state owner. Prose,
  projections, and derived handoffs may explain or render that fact but may not
  independently redefine it.
target_implication: >-
  Hybrid planning artifacts must declare canonical structured facts and source
  revisions. SQLite remains derived and rebuildable.
validation:
  - duplicate-machine-fact-owner
  - structured-prose-contradiction
source_evidence:
  - GitHub issue #50
```

### STATE-HISTORY-004 — Historical artifacts are evidence, not pickup authority

```yaml
id: STATE-HISTORY-004
status: current
classification: verified-current
contract: >-
  Archived ledgers, completed runways, redirects, old flat filenames, and stale
  pickup notes may provide evidence but do not override current active state.
target_implication: >-
  Legacy parsers and historical references must be read-only and removable after
  active old-format state expires.
validation:
  - historical-artifact-does-not-override-current
source_evidence:
  - scripts/planning_state.py
  - tests/test_planning_state.py
```

## Specialized Evidence Contracts

### EVIDENCE-LEGACY-001 — Legacy classification does not own workflow state

```yaml
id: EVIDENCE-LEGACY-001
status: target-only
classification: target-decision
contract: >-
  legacy-removal may classify legacy compatibility, canonical models, and cleanup
  residues, but it never owns program queue state, selected work, dispatch,
  execution, or closeout.
target_implication: >-
  Remove the current exception that permits legacy-removal to become a program
  workflow owner.
validation:
  - legacy-evidence-no-state-writes
source_evidence:
  - skills/legacy-removal/SKILL.md
```

### EVIDENCE-DEAD-002 — Deletion-test status is evidence only

```yaml
id: EVIDENCE-DEAD-002
status: current
classification: verified-current
contract: >-
  dead-surface-audit owns canonical deletion-test evidence vocabulary but does
  not select, approve, queue, execute, or close cleanup work.
target_implication: >-
  Planning and execution consume its statuses without transferring workflow
  authority.
validation:
  - deletion-evidence-no-state-writes
source_evidence:
  - skills/dead-surface-audit/SKILL.md
```

### EVIDENCE-TEST-003 — Test-quality review is independent evidence

```yaml
id: EVIDENCE-TEST-003
status: current
classification: verified-current
contract: >-
  test-quality-review assesses behavioral confidence and design friction, returns
  bounded review evidence, and owns no implementation or lifecycle transition.
target_implication: >-
  work-batch may trigger it as an evidence mechanism while retaining final
  workflow authority.
validation:
  - test-quality-review-no-state-writes
source_evidence:
  - skills/test-quality-review/SKILL.md
```

## Accidental Source Structure

The following are not preservation requirements:

- `architecture-program-runway` as a skill or mode container;
- `batch-runway` as a skill or mode container;
- `intake-findings`, `group-batches`, `select-next-batch`,
  `create-next-runway`, `closeout-runway`, `create-spec`, or `execute-spec` mode
  names;
- the current `requires` arrays in `codex-features.json`;
- the current distribution of rules between command skills, runtime skills,
  references, and routing documents;
- exact prose or headings asserted by text-contract tests;
- the 3-5 slice count as a strict universal rule;
- v1/v2 compatibility contracts after no active artifact requires them;
- the current runner phase vocabulary;
- direct installation or discoverability of old runtime owners;
- historical absolute paths embedded in completed artifacts.

## Contract Change Procedure

A later implementation batch may intentionally change a contract only when it:

1. names the contract ID;
2. records the old and new behavior;
3. states the reason and caller impact;
4. updates the behavioral scenario matrix;
5. receives explicit human approval when the change narrows or removes supported
   behavior;
6. removes or updates obsolete source tests rather than preserving topology by
   default.
