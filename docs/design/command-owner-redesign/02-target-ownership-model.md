# Target Ownership Model

## Target Decision

The target architecture has three human-facing workflow owners:

```text
add-to-ledger  owns intake
plan-batch     owns planning
work-batch     owns execution and same-batch closeout
```

Shared components are narrow mechanisms or evidence producers. They may inspect,
validate, resolve, serialize, apply an explicit caller decision, execute a
command, commit accepted work, or report evidence. They may not reinterpret the
human request or become an alternate owner of the same workflow.

## Pre-Cutover Root Topology

```yaml
toolchain_source_root:
  physical_owner: stable checkout on authoritative master
  authority:
    - loaded stable skills
    - controlling scripts
    - schemas and references used by the stable controller
    - worker and reviewer contracts used by the stable controller

canonical_planning_repository_root:
  physical_owner: stable checkout on authoritative master
  authority:
    - CURRENT.md
    - LEDGER.md
    - selected dispatch
    - queued or active runway
    - closeout
    - reconciliation receipts

implementation_target_root:
  physical_owner: separate candidate clone
  authority:
    - candidate source
    - candidate schemas and scripts
    - candidate tests and fixtures
    - migration implementation commits
```

Every command records all roots and exact Git revisions. No root is inferred only
from current working directory.

## Decision Ownership Matrix

| Decision or responsibility | Target owner | Allowed mechanism or evidence |
|---|---|---|
| Fresh finding intake | `add-to-ledger` | normalized diagnostic |
| Source identity and provenance | `add-to-ledger` | schema validation |
| Normalize a finding | `add-to-ledger` | normalization helpers |
| Create, update, merge, or no-op | `add-to-ledger` | ledger reader |
| Canonical ledger mutation decision | `add-to-ledger` | `ledger-store` applies explicit mutation |
| Current-state diagnosis | `planning-state` | structured parser and validator |
| Candidate eligibility and ranking | `plan-batch` | canonical ledger reader |
| Grouping into one bounded batch | `plan-batch` | behavior contracts and evidence |
| Split, block, or narrow | `plan-batch` | optional evidence skills |
| Batch kind and risk | `plan-batch` | supported-value catalogs |
| Approval gates | `plan-batch` | risk policy catalog |
| Dispatch content | `plan-batch` | renderer and validator |
| Runway design | `plan-batch` | schema and planning references |
| Validation-profile choice | `plan-batch` | validation catalog |
| Selected and queued transition decision | `plan-batch` | `planning-state` applies transition |
| Current slice choice | `work-batch` | runway progress reader |
| Worker delegation | `work-batch` | registered worker |
| Validation acceptance | `work-batch` | validation command mechanism |
| Specialist review trigger | `work-batch` | evidence review catalog |
| Reviewer delegation and verdict acceptance | `work-batch` | registered reviewer |
| Commit acceptance | `work-batch` | commit mechanism |
| Recovery and resume | `work-batch` | recovery contract and receipts |
| Final completion | `work-batch` | validation and closeout validators |
| Finding closeout interpretation | `work-batch` | execution evidence |
| Same-batch ledger reconciliation | `work-batch` | `ledger-store` applies mutation |
| Completed transition | `work-batch` | `planning-state` applies transition |
| Successor-selection stop boundary | `work-batch` | no mechanism may override it |
| Path and artifact placement | `planning-artifacts` | deterministic resolver |
| Lifecycle validation and serialization | `planning-state` | explicit transition request |
| Root and generation enforcement | temporary cross-checkout bridge | explicit execution context |
| Loop count and process lifecycle | runner | public command results |

## Command Interfaces

### `add-to-ledger`

```yaml
interface: add-to-ledger/v1
inputs:
  - normalized planning diagnostic
  - one or more explicit source requests
outputs:
  - canonical finding identities
  - ledger mutation receipt
owns:
  - intake eligibility
  - source identity
  - normalization
  - duplicate and merge decision
  - ledger mutation decision
forbids:
  - batch selection
  - dispatch creation
  - runway creation
  - implementation
  - closeout without evidence
```

### `plan-batch`

```yaml
interface: plan-batch/v1
inputs:
  - normalized planning diagnostic
  - canonical ledger
  - optional explicit existing finding
  - explicit root and generation context
outputs:
  one_of:
    - existing-state report
    - one selected dispatch and one queued runway
    - blocked result
owns:
  - state branch decision
  - eligibility and selection
  - grouping and scope shaping
  - dispatch definition
  - runway specification
  - risk and validation profile
forbids:
  - fresh intake
  - external backlog discovery
  - implementation
  - multiple runnable batches
  - successor planning during another command
```

### `work-batch`

```yaml
interface: work-batch/v1
inputs:
  - normalized planning diagnostic
  - exactly one queued or active runway
  - explicit root and generation context
outputs:
  - durable slice evidence
  - implementation commits
  - closeout
  - same-batch reconciliation receipt
owns:
  - execution lifecycle
  - current slice choice
  - worker and reviewer lifecycle
  - validation acceptance
  - recovery and resume
  - commit acceptance
  - finalization
  - same-batch reconciliation
forbids:
  - intake
  - new batch selection
  - unrelated scope expansion
  - successor selection
```

## `planning-state` Target Role

`planning-state` is the lifecycle state-machine authority, not a workflow engine.

It owns:

- parsing canonical structured planning facts;
- normalized diagnostics;
- lifecycle invariants;
- expected revision and file-hash checks;
- legal transition validation;
- atomic serialization;
- transition receipts;
- optional derived projections through a separated adapter.

It does not own:

- candidate selection;
- grouping or scope shaping;
- dispatch content;
- runway design;
- validation-profile selection;
- worker or reviewer choice;
- recovery policy;
- commit acceptance;
- finding closeout interpretation;
- successor selection.

Allowed form:

```text
planning-state inspect --planning-root <absolute-root>
planning-state validate --planning-root <absolute-root>
planning-state apply-transition --operation <explicit-operation> --payload <caller-decision>
```

Forbidden form:

```text
planning-state plan-next-batch
planning-state choose-best-finding
planning-state recover-current-slice
planning-state select-successor
```

## `planning-artifacts` Target Role

It owns structural conventions only:

- artifact types and canonical locations;
- program and batch lineage;
- archive placement;
- structured-block location;
- reference resolution;
- detection that a planning write resolves under the canonical planning root.

It does not own lifecycle mutation, selection, execution, or closeout decisions.

## `ledger-store` Apply-Only Contract

`ledger-store` is a narrow revision-checked storage mechanism.

```yaml
interface: ledger-store/v1
read:
  inputs:
    - ledger_path
  outputs:
    - parsed_findings
    - file_revision

apply:
  inputs:
    - ledger_path
    - expected_file_revision
    - caller_decision:
        action: create | update | merge | no-op | reconcile
        finding_mutations: []
        touched_finding_revisions: {}
        idempotency_key: string
  outputs:
    - applied: true | false
    - before_revision
    - after_revision
    - touched_finding_ids
    - receipt
```

It may validate:

- schema and identity uniqueness;
- expected revision;
- caller-supplied mutation shape;
- dependency references;
- idempotency key replay;
- resulting deterministic rendering.

It may not decide:

- whether findings are semantically duplicates;
- which finding is selected;
- how scope is shaped;
- whether evidence closes a finding;
- which successor should be planned.

## Temporary Cross-Checkout Bridge

The bridge exists only for self-hosted migration before final convergence.

```yaml
interface: cross-checkout-context/v1
owns:
  - root_binding_validation
  - repository_identity_validation
  - write_scope_validation
  - generation_identity_capture
  - cross_repository_receipt_format
forbids:
  - intake_decisions
  - selection
  - scope_shaping
  - runway_design
  - execution_acceptance
  - closeout_interpretation
  - successor_selection
```

Required context:

```yaml
execution_context:
  toolchain_source_root: absolute-path
  toolchain_commit: full-sha
  canonical_planning_repository_root: absolute-path
  canonical_planning_commit_before: full-sha
  implementation_target_root: absolute-path
  implementation_commit_before: full-sha
  codex_home: absolute-path
  generation_role: stable | candidate
  canonical_state_mutation_allowed: true | false
```

Planning writes outside the planning root and implementation writes outside the
candidate root are rejected.

## Worker and Reviewer Contracts

Worker:

- implements only the delegated slice under `implementation_target_root`;
- runs assigned focused validation there;
- may not review, commit, mutate planning state, select work, or spawn agents;
- returns its verified generation and repository identity.

Reviewer:

- remains read-only;
- reviews the exact candidate diff basis;
- verifies generation and repository identity;
- may return clean, findings, or blocked;
- may not modify, commit, delegate, or mutate lifecycle state.

`work-batch` remains the only lifecycle coordinator.

## Runner Boundary

Target runner protocol:

```text
invoke fresh plan-batch
-> optionally invoke work-batch
-> evaluate explicit loop bound
-> optionally invoke another fresh plan-batch
```

The runner owns:

- process lifecycle;
- environment and sandbox selection;
- run bounds;
- command result schema validation;
- telemetry and receipts.

The runner does not own:

- candidate eligibility;
- successor readiness;
- dispatch content;
- runway design;
- slice acceptance;
- closeout meaning.

Closeout reports only same-batch completion. A later `plan-batch` decides whether
eligible work remains.

## Allowed Dependency Directions

```text
command owner -> narrow mechanism
command owner -> evidence producer
command owner -> registered worker/reviewer
stable controller -> temporary root-binding bridge
runner -> public command protocol
schema validator -> schema and artifact input
projection adapter -> canonical structured state
```

## Forbidden Dependency Directions

```text
add-to-ledger -> plan-batch or work-batch
plan-batch -> work-batch, APR, or Batch Runway
work-batch -> plan-batch, APR, Batch Runway, or successor selection
planning-state -> semantic command decision
planning-artifacts -> lifecycle mutation
ledger-store -> semantic duplicate, selection, scope, closeout, or successor decision
cross-checkout bridge -> semantic workflow decision
runner -> eligibility or successor-readiness decision
worker -> reviewer, commit, planning mutation, or delegation
reviewer -> implementation, commit, or lifecycle mutation
```

## Post-Cutover Authority

After CCFG-28:

```text
implementation branch
  = candidate toolchain source

master checkout
  = canonical planning repository
```

CCFG-29 owns final quiescent convergence:

```text
merge implementation branch into latest master
-> verify toolchain content and contracts
-> rebind default CODEX_HOME to master
-> verify fresh session
-> remove cross-checkout bridge
-> retire candidate branch when safe
```

## Real Ownership Transfer Acceptance

A command-owner transfer is complete only when:

1. the command performs its workflow without loading another broad owner;
2. dependencies contain only narrow mechanisms and evidence producers;
3. behavior scenarios pass after disabling or deleting the old path;
4. the old owner no longer contains the transferred decision as a normal route;
5. topology tests no longer require the old dependency;
6. state mechanisms receive explicit decisions;
7. new active artifacts use target formats;
8. temporary readers and bridges have explicit deletion conditions;
9. the batch records source ownership removed, not only target surface added.
