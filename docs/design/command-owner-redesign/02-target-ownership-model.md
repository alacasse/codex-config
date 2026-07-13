# Target Ownership Model

## Target Decision

The target architecture has three human-facing workflow owners:

```text
add-to-ledger  owns intake
plan-batch     owns planning
work-batch     owns execution and same-batch closeout
```

Shared components are narrow mechanisms or evidence producers. They may apply,
validate, serialize, inspect, render, delegate, or report an explicit decision.
They may not independently reinterpret the human request or become an alternate
owner of the same workflow.

## Dependency Graph

```text
add-to-ledger
├── planning-state.inspect
├── planning-artifacts.resolve
├── ledger-store.upsert
└── legacy-removal [optional evidence only]

plan-batch
├── planning-state.inspect
├── planning-artifacts.resolve
├── ledger-store.read
├── artifact-schema.validate
├── validation-profile-catalog
└── planning-state.apply-transition

work-batch
├── planning-state.inspect
├── planning-artifacts.resolve
├── worker agent
├── reviewer agent
├── optional specialist evidence reviews
├── validation command mechanism
├── commit mechanism
├── artifact-schema.validate
├── ledger-store.reconcile
└── planning-state.apply-transition

planning-state
├── structured artifact parsers
├── lifecycle model and invariants
├── transition validation and receipts
└── optional reporting projection adapter

planning-artifacts
├── canonical path resolution
├── artifact lineage rules
└── artifact type and placement validation
```

## Decision Ownership Matrix

| Decision or responsibility | Target owner | Allowed mechanism or evidence input |
|---|---|---|
| Fresh finding intake | `add-to-ledger` | planning diagnostic |
| Source identity preservation | `add-to-ledger` | ledger schema validator |
| Finding normalization | `add-to-ledger` | normalization helpers |
| Duplicate, merge, create, or no-op decision | `add-to-ledger` | ledger reader |
| Canonical ledger mutation decision | `add-to-ledger` | ledger-store applies mutation |
| Current-state diagnosis | `planning-state` | parser and validator |
| Candidate eligibility | `plan-batch` | canonical ledger reader |
| Candidate ranking and selection | `plan-batch` | no alternate workflow owner |
| Grouping into one bounded batch | `plan-batch` | contract and scenario evidence |
| Scope splitting, blocking, or narrowing | `plan-batch` | optional legacy or dead-surface evidence |
| Batch kind and slice risk selection | `plan-batch` | supported-value schemas |
| Approval-gate definition | `plan-batch` | risk policy catalog |
| Selected dispatch content | `plan-batch` | artifact renderer and validator |
| Runway slice design | `plan-batch` | runway schema and reference contracts |
| Validation-profile selection | `plan-batch` | validation profile catalog |
| Transition to selected or queued | `plan-batch` | planning-state applies transition |
| Current slice selection | `work-batch` | runway progress reader |
| Worker delegation | `work-batch` | registered worker agent |
| Focused and profile validation decision | `work-batch` | validation command mechanism |
| Specialist review trigger | `work-batch` | evidence review catalog |
| Final reviewer delegation and acceptance | `work-batch` | registered reviewer agent |
| Commit acceptance | `work-batch` | Git commit mechanism |
| Recovery action | `work-batch` | recovery contract |
| Resume decision | `work-batch` | durable execution evidence |
| Final validation and completion decision | `work-batch` | validation and closeout validators |
| Finding closeout interpretation | `work-batch` | closeout evidence |
| Same-batch ledger reconciliation | `work-batch` | ledger-store applies reconciliation |
| Lifecycle transition to completed | `work-batch` | planning-state applies transition |
| Successor-selection stopping boundary | `work-batch` | no mechanism may override it |
| Artifact placement | `planning-artifacts` | path resolver |
| Lifecycle serialization | `planning-state` | atomic serializer |
| Artifact schema validation | schema tooling | no semantic workflow decision |
| Legacy compatibility classification | `legacy-removal` | optional dead-surface evidence |
| Deletion-test evidence status | `dead-surface-audit` | static and dynamic inspection |
| Test-quality evidence | `test-quality-review` | tests and production contract evidence |
| Multi-command loop policy | runner or explicit human request | public plan/work command protocols |

## Command Interfaces

### `add-to-ledger`

```yaml
interface: add-to-ledger/v1
inputs:
  - normalized planning diagnostic
  - fresh source request or explicitly named source
outputs:
  - ledger mutation receipt
  - canonical finding identity
  - resulting ledger revision
owns:
  - intake eligibility
  - source identity
  - finding normalization
  - duplicate and merge decision
  - ledger mutation decision
forbids:
  - batch selection
  - dispatch creation
  - runway creation
  - implementation
  - finding closeout without evidence
```

Normal sequence:

```text
inspect state
-> resolve canonical ledger
-> preserve source identity
-> normalize finding
-> detect create, merge, update, or no-op
-> apply revision-checked mutation
-> validate resulting state
-> stop
```

### `plan-batch`

```yaml
interface: plan-batch/v1
inputs:
  - normalized planning diagnostic
  - canonical program ledger
  - optional explicit existing finding preference
  - optional current selected dispatch
outputs:
  - existing-state report
  - or one selected dispatch and one queued runway
owns:
  - state branch decision
  - candidate selection
  - scope shaping
  - dispatch definition
  - runway specification
  - validation profile selection
forbids:
  - fresh finding intake
  - external backlog discovery
  - slice implementation
  - multiple batch creation
  - successor planning during another command
```

Normal sequence:

```text
inspect state
-> active? report and stop
-> queued? report and stop
-> selected? validate and specify that dispatch
-> otherwise select exactly one bounded ledger candidate
-> split, block, or narrow when required
-> define dispatch
-> transition idle to selected
-> define runway
-> transition selected to queued
-> stop before implementation
```

### `work-batch`

```yaml
interface: work-batch/v1
inputs:
  - normalized planning diagnostic
  - exactly one queued or active runway
outputs:
  - durable slice evidence
  - focused commits
  - closeout
  - same-batch reconciliation receipt
owns:
  - execution lifecycle
  - current slice choice
  - worker and reviewer lifecycle
  - validation acceptance
  - recovery
  - commit acceptance
  - finalization
  - same-batch reconciliation
forbids:
  - fresh finding intake
  - new batch selection
  - unrelated scope expansion
  - successor selection after closeout
```

Normal sequence:

```text
inspect state
-> validate one queued or active runway
-> queued to active when required
-> select next incomplete slice
-> delegate worker
-> validate
-> delegate independent review
-> recover or stop when required
-> accept and commit clean slice
-> persist evidence and remaining work
-> repeat
-> final validation
-> create closeout
-> reconcile same batch
-> active to completed
-> stop without successor selection
```

## `planning-state` Target Role

`planning-state` is the lifecycle state-machine authority and normalized
persistence interface. It is not a workflow engine.

It owns:

- parsing canonical structured planning facts;
- normalized current-state diagnostics;
- lifecycle invariants;
- legal transition validation;
- expected-revision checks;
- pointer and artifact-lineage validation;
- transition application;
- atomic state serialization;
- transition receipts;
- optional derived reporting through a separated projection adapter.

It does not own:

- which finding should be selected;
- whether findings belong in one batch;
- split, block, or narrow decisions;
- dispatch content;
- slice design;
- validation-profile choice;
- worker or reviewer selection;
- recovery policy;
- commit acceptance;
- finding closeout interpretation;
- successor selection.

Allowed interface style:

```text
planning-state inspect
planning-state validate
planning-state apply-transition --operation <explicit-operation> --payload <decision>
```

Forbidden interface style:

```text
planning-state plan-next-batch
planning-state choose-best-finding
planning-state recover-current-slice
planning-state select-successor
```

The first style applies a decision. The second style hides a workflow owner
behind a narrow name.

## `planning-artifacts` Target Role

`planning-artifacts` owns structural conventions only:

- artifact type names;
- canonical path calculation;
- program and batch lineage;
- co-location rules;
- archive placement;
- human-readable and structured-block location conventions;
- reference resolution.

It does not own lifecycle state transitions, finding status changes, candidate
selection, execution, or closeout decisions.

Lifecycle vocabulary belongs in a versioned state schema. Artifact vocabulary
belongs in the artifact layout contract. The two must not be conflated.

## Specialized Evidence Skills

### `legacy-removal`

Target role:

- classify legacy surfaces and compatibility commitments;
- identify canonical model candidates;
- classify cleanup residue;
- produce compact planning evidence.

Forbidden target role:

- owning a program ledger workflow;
- mutating queue or selected state;
- selecting a batch;
- creating an execution runway as an alternate owner;
- approving deletion;
- executing cleanup;
- closing findings.

The current exception that permits legacy-removal to become a program owner is
removed.

### `dead-surface-audit`

Retain its evidence-only boundary. It owns deletion-test evidence vocabulary
and caller evidence, not planning or execution authority.

### `test-quality-review`

Retain its independent review role. It may be invoked by work-batch or directly
for a focused audit, but it owns no implementation or lifecycle decision.

## Worker and Reviewer Agents

The current worker and reviewer authority separation is a meaningful target
contract even if their historical names later change.

Worker:

- may implement only the delegated slice;
- may run assigned focused validation;
- may not review, commit, update ledger state, select work, or spawn agents.

Reviewer:

- remains read-only;
- validates the exact current diff basis and evidence;
- may return clean, findings, or blocked;
- may not modify, delegate, commit, or update lifecycle state.

`work-batch` remains the only lifecycle coordinator.

## Runner Boundary

The runner is an external orchestrator over public command protocols:

```text
invoke plan-batch
-> optionally invoke work-batch
-> evaluate explicit stop policy
-> optionally invoke plan-batch again
```

The runner may own:

- run bounds;
- fresh process lifecycle;
- environment and sandbox selection;
- command result validation;
- telemetry and run receipts;
- explicit multi-batch loop policy.

The runner may not own:

- candidate selection semantics;
- dispatch content;
- runway slice design;
- slice acceptance;
- same-batch reconciliation semantics.

It must not depend on retired skill names or modes.

## Allowed Dependency Directions

```text
command owner -> narrow mechanism
command owner -> evidence producer
command owner -> registered agent
runner -> public command protocol
evidence producer -> inspection mechanism
schema validator -> schema and artifact input
projection adapter -> canonical state input
```

## Forbidden Dependency Directions

```text
add-to-ledger -> plan-batch
add-to-ledger -> work-batch

plan-batch -> automatic add-to-ledger mutation
plan-batch -> work-batch
plan-batch -> architecture-program-runway
plan-batch -> batch-runway

work-batch -> plan-batch
work-batch -> architecture-program-runway
work-batch -> batch-runway
work-batch -> successor selection

planning-state -> command owner
planning-state -> candidate selection
planning-state -> scope shaping
planning-state -> slice design
planning-state -> recovery policy
planning-state -> successor selection

planning-artifacts -> lifecycle mutation
planning-artifacts -> candidate selection

legacy-removal -> queue or selected-state mutation
legacy-removal -> execution

dead-surface-audit -> queue or selected-state mutation
dead-surface-audit -> deletion approval

test-quality-review -> implementation
test-quality-review -> lifecycle transition

worker -> reviewer
worker -> commit
worker -> ledger mutation
worker -> agent delegation

reviewer -> implementation
reviewer -> commit
reviewer -> lifecycle transition
```

## Current Skill Disposition

| Current surface | Target disposition |
|---|---|
| `add-to-ledger` | Retain and deepen into the sole intake owner. |
| `plan-batch` | Retain and deepen into the sole planning owner. |
| `work-batch` | Retain and deepen into the sole execution and same-batch closeout owner. |
| `port-by-contract` | Retain; migrate to contract-first representation after the format is validated. |
| `architecture-program-runway` | Decompose and delete. No final replacement skill with equivalent breadth. |
| `batch-runway` | Split planning references into `plan-batch`, execution references into `work-batch`, then delete. |
| `planning-state` | Retain as a narrow state and transition interface; split projection code internally when useful. |
| `planning-artifacts` | Retain and narrow to artifact structure and path resolution. |
| `legacy-removal` | Retain as evidence support; remove program-owner escape hatch. |
| `dead-surface-audit` | Retain. |
| `test-quality-review` | Retain. |
| `runway_worker` | Retain authority contract; rename only if useful after ownership migration. |
| `runway_reviewer` | Retain authority contract; rename only if useful after ownership migration. |
| architecture-program runner | Retain only as an independent orchestrator over public command protocols. |

## Real Ownership Transfer Acceptance Criteria

A command-owner migration is complete only when all are true:

1. The command executes its workflow without loading another broad workflow
   skill.
2. Its manifest dependencies contain only narrow mechanisms and evidence
   producers.
3. The target scenario suite passes after physical removal or disabling of the
   old owner path for that responsibility.
4. The old owner no longer contains the transferred decision, even as a normal
   compatibility route.
5. Tests no longer require the old dependency or mode name.
6. State mechanisms receive explicit decisions rather than infer human intent.
7. New active artifacts are produced only in the target format.
8. A fresh agent reads the command contract, normalized state, and explicitly
   named artifacts without replaying the historical routing chain.
9. Any temporary old-format reader is read-only, caller-scoped, and has a
   deletion condition.
10. The batch records the exact source ownership removed, not only the target
    surface added.
