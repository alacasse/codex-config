# Contract-First Formats

## Purpose

This document incorporates the design intent of GitHub issues #48, #49, and #50
into one representation strategy for skills and durable planning artifacts.

The representation work is subordinate to the ownership model. A skill does not
become a real owner merely because it contains a parseable YAML block. A
migration is successful only when both representation and responsibility move.

```yaml
representation_success:
  contracts_parseable: true
  machine_facts_canonical: true
  prose_not_authoritative: true

ownership_success:
  duplicate_workflow_decisions: 0
  broad_runtime_owner_dependencies: 0
  old_owner_deletion_test: passed
```

## Design Principles

- Use YAML for stable operational facts.
- Use numbered procedure steps for the normal path.
- Use explicit `IF`/`THEN` rules for branching and stopping.
- Use short prose for rationale, danger, and non-obvious architectural context.
- Move rare edge cases, examples, compatibility details, and long procedures to
  references.
- Do not create a dense repository-specific DSL.
- Do not convert narrative prose into YAML-shaped prose.
- Do not define the same machine-relevant fact independently in prose and YAML.
- Keep contracts versioned and mechanically validated.
- Keep active artifacts readable in ordinary Git review.
- Keep SQLite optional and derived.

## Skill Representation

### Chosen form

Keep the existing minimal frontmatter for Codex discovery and place one
canonical operational contract block under a stable heading:

```markdown
---
name: plan-batch
description: Select one bounded ledger batch and produce one queued runway.
---

# Plan Batch

## Contract

```yaml
schema: skill-contract/v1
...
```

## Procedure

1. ...
2. ...

## Decision Rules

```text
IF an active runway exists:
  report it and stop.
```

## Rationale

Short explanation of dangerous or non-obvious invariants.

## Reference Loading

```yaml
load:
  references/runway-specification.md:
    when:
      - creating_runway
```
```

Do not place the full operational contract in frontmatter. The frontmatter is an
integration surface; the contract block is the versioned workflow interface.

### `skill-contract/v1`

```yaml
schema: skill-contract/v1

identity:
  name: plan-batch
  audience: human-command-owner

purpose: >-
  Select exactly one bounded batch from canonical ledger state and produce at
  most one concrete queued runway.

owns:
  decisions:
    - candidate_selection
    - scope_shaping
    - dispatch_definition
    - runway_specification
    - validation_profile_selection
  durable_facts:
    - selected_dispatch_content
    - runway_execution_contract

reads:
  required:
    - normalized_planning_diagnostic
    - canonical_program_ledger
  conditional:
    - selected_dispatch
    - source_evidence_referenced_by_selected_finding

writes:
  - selected_dispatch
  - concrete_runway

requires:
  mechanisms:
    - planning-state
    - planning-artifacts
    - ledger-store
    - artifact-schema-validation
  evidence_skills: []

delegates:
  - responsibility: transition_application
    target: planning-state
  - responsibility: path_resolution
    target: planning-artifacts

forbids:
  - fresh_finding_intake
  - external_backlog_discovery
  - slice_implementation
  - multiple_batch_creation
  - successor_selection

outputs:
  one_of:
    - existing_state_report
    - selected_dispatch_and_queued_runway
    - blocked_result

stops_when:
  - invalid_planning_state
  - active_runway_exists
  - queued_runway_exists
  - no_eligible_finding
  - unresolved_human_decision

references:
  - path: references/runway-specification.md
    load_when:
      - creating_runway
```

### Required fields

Every contract-first target skill requires:

- `schema`
- `identity`
- `purpose`
- `owns`
- `reads`
- `writes`
- `requires`
- `delegates`
- `forbids`
- `outputs`
- `stops_when`
- `references`

Empty collections are allowed when semantically correct. Missing fields are not.

### Ownership validation

A validator must reject or report:

- one skill owning and forbidding the same decision or write;
- two human command skills owning the same decision;
- two skills owning the same durable fact without a declared shared mechanism;
- a support mechanism owning a human workflow decision;
- an unknown delegated target;
- a dependency cycle;
- a referenced file that does not exist;
- a command owner depending on a retired broad owner;
- an evidence skill declaring queue, selected-state, execution, or closeout
  ownership;
- a main `SKILL.md` that exceeds the selected size budget without an explicit
  justification.

The size budget is a review signal, not an automatic architecture rule. It must
not force dangerous invariants into hidden references.

## Procedure and Decision Rules

A contract states authority and invariants. It does not replace readable
execution order.

Use numbered procedure steps for the normal path:

```text
1. Inspect and validate current state.
2. Resolve the canonical ledger.
3. Branch on active lifecycle state.
4. Select exactly one bounded finding when idle.
5. Write and validate the dispatch.
6. Write and validate the runway.
7. Apply the queued transition.
8. Stop before implementation.
```

Use decision rules for branching:

```text
IF an active runway exists:
  report it and stop without writes.

IF a queued runway exists:
  report it and stop without writes.

IF a selected dispatch exists and its source revision is current:
  create or validate only that dispatch's runway.

IF a candidate mixes evidence gathering and destructive cleanup without an
approval boundary:
  block, split, or narrow before dispatch creation.
```

Avoid embedding extensive rationale inside procedure steps.

## Rationale

Rationale belongs in the main skill only when misunderstanding it could cause a
material safety or ownership defect.

Suitable examples:

- why fresh external work cannot become executable backlog without intake;
- why same-batch reconciliation cannot select a successor;
- why state mechanisms must apply explicit decisions rather than infer intent;
- why a worker cannot review or commit its own slice.

Long examples and rare compatibility cases belong in references.

## Reference Loading

References must be trigger-loaded:

```yaml
load:
  references/recovery.md:
    when:
      - validation_failed
      - review_findings
      - dirty_file_conflict
      - stale_diff_basis
  references/finalization.md:
    when:
      - all_intended_slices_complete
      - final_report_requested
```

A reference may deepen a procedure but may not contradict or independently
redefine the main contract.

## Skill-Authoring Meta-Skill

GitHub issue #49 proposes a meta-skill for creating, migrating, and reviewing
contract-first skills. The target accepts the idea but defers implementation
until the format has been validated on real owners.

### Target role

```yaml
name: skill-authoring
purpose: Create, migrate, or audit skills against accepted contract-first formats.
owns:
  - contract_extraction
  - skill_structure_design
  - ownership_conflict_detection
  - reference_split_recommendations
forbids:
  - workflow_execution
  - durable_planning_state_mutation
  - resolving_ownership_conflicts_silently
  - inventing_unapproved_schema_fields
```

### Required creation gate

Do not implement `skill-authoring` until:

```yaml
skill_contract_schema:
  accepted_version: 1
  validated_on:
    - port-by-contract
    - add-to-ledger
    - plan-batch
    - work-batch
planning_artifact_schemas:
  accepted_versions:
    - planning-dispatch/v1
    - planning-runway/v1
    - planning-closeout/v1
open_schema_questions: 0
```

The meta-skill guides design and invokes validators. It is not a runtime
dependency of command owners.

## Planning Artifact Representation

### Chosen form

Use one canonical embedded YAML block near the beginning of each active
Markdown artifact:

```markdown
# Batch CCFG-20

## Operational Contract

```yaml
schema: planning-runway/v1
...
```

## Objective

Human-readable objective and context.

## Architectural Rationale

Human-readable explanation of non-obvious decisions.
```

This form keeps structured facts and rationale co-located without requiring a
companion file that can drift independently.

### Rejected as the initial default

- **Companion YAML file:** creates two independently movable and editable
  artifacts.
- **Generated Markdown from structured source:** adds generator and review
  friction before the format is proven.
- **Full frontmatter contract:** becomes unwieldy for slices and evidence.
- **Custom DSL:** unnecessary and difficult for fresh agents and ordinary tools.

A future accepted decision may revisit generated views after the embedded form
is proven.

## Canonical Fact Ownership

| Fact | Canonical owner |
|---|---|
| Finding identity, provenance, lifecycle, and next action | structured ledger finding entry |
| Selected, queued, and active artifact pointers | structured program current-state block |
| Batch selection, included findings, exclusions, and scope | structured dispatch contract |
| Slices, dependencies, risks, validation, and delegation | structured runway contract |
| Slice completion and commit evidence | structured execution receipts and runway progress state |
| Final completion evidence and same-batch reconciliation result | structured closeout contract |
| Architectural context, rationale, and unresolved tradeoffs | prose in the owning artifact |
| Historical reports and inventory | derived projection |
| Runner telemetry | separate runtime JSON artifacts |

No second artifact or prose section may independently redefine these facts.

## Canonicality Rules

```yaml
canonicality:
  machine_relevant_facts:
    source: structured_contract_only

  prose:
    may:
      - explain
      - justify
      - link
      - summarize_without_redefining
    must_not:
      - override
      - duplicate_operational_values
      - define_a_second_status
      - define_a_second_dependency_graph
      - define_a_second_validation_class

  derived_artifacts:
    must_declare:
      - source_artifact
      - source_revision
```

Allowed prose:

```text
This batch requires explicit approval because `batch.kind` is
`destructive-cleanup`.
```

Forbidden prose when the structured contract disagrees:

```text
This is a behavior-preserving batch.
```

## `planning-dispatch/v1`

```yaml
schema: planning-dispatch/v1

artifact:
  type: dispatch
  id: ccfg-20-example
  program: codex-config
  revision: sha256:...

source:
  ledger_path: docs/plans/programs/codex-config/LEDGER.md
  ledger_revision: sha256:...
  finding_ids:
    - CCFG-20

selection:
  outcome: selected
  rationale_code: bounded-owner-seam

scope:
  goal: Transfer planning ownership into plan-batch.
  owner_seam: plan-batch
  batch_kind: migration
  included_finding_ids:
    - CCFG-20
  deferred_finding_ids: []
  risk_summary:
    - ownership-transfer

approval_gates: []

dependencies:
  satisfied: []
  blocking: []

runway:
  expected_path: docs/plans/programs/codex-config/batches/ccfg-20-example/runway.md

stops_when:
  - ledger_revision_stale
  - unresolved_human_decision
```

## `planning-runway/v1`

```yaml
schema: planning-runway/v1

artifact:
  type: runway
  id: ccfg-20-example
  program: codex-config
  source_dispatch: docs/plans/programs/codex-config/batches/ccfg-20-example/dispatch.md
  source_dispatch_revision: sha256:...

batch:
  kind: migration
  status: queued

execution:
  result_contract: registered-agent/v2
  branch_policy: dedicated
  dirty_worktree_policy: strict
  successor_selection: forbidden

slices:
  - id: slice-1
    depends_on: []
    allowed_read_paths:
      - skills/plan-batch/**
      - tests/**
    allowed_write_paths:
      - skills/plan-batch/**
      - tests/test_plan_batch_workflow.py
    risk_class: migration
    approval_gate: null
    validation:
      - command: python -m pytest tests/test_plan_batch_workflow.py -q
        class: required-green
        trigger: always

review:
  final_gate: runway_reviewer

closeout:
  required_artifacts:
    - closeout
    - completed-slices
    - commit-receipts
  required_transition: active_to_completed
  reconcile_same_batch_only: true
```

## `planning-closeout/v1`

```yaml
schema: planning-closeout/v1

artifact:
  type: closeout
  batch_id: ccfg-20-example
  program: codex-config
  source_runway: docs/plans/programs/codex-config/batches/ccfg-20-example/runway.md
  source_runway_revision: sha256:...

result:
  status: completed
  commits:
    - abc1234

validation:
  status: passed
  evidence: []

review:
  status: clean
  diff_basis: abc1234
  evidence: []

cleanup_residue:
  removed: []
  kept: []
  deferred: []

reconciliation:
  findings:
    closed:
      - CCFG-20
    open: []
  lifecycle:
    selected_dispatch: null
    queued_runway: null
    active_runway: null
  successor_selected: false
```

## Validation Tooling

The design expects lightweight executable validators, not prose-only checks.
Candidate final placement:

```text
schemas/
  skill-contract-v1.schema.json
  planning-dispatch-v1.schema.json
  planning-runway-v1.schema.json
  planning-closeout-v1.schema.json

scripts/contracts/
  validate_skill_contracts.py
  validate_planning_artifacts.py
```

The exact implementation split remains subject to implementation design, but
the validators must cover:

- locating exactly one canonical contract block;
- schema version and required fields;
- unknown references and artifact paths;
- duplicate durable-fact ownership;
- unsupported lifecycle state or transition;
- unknown slice dependencies and dependency cycles;
- unsupported risk and validation classes;
- required approval gates;
- result-contract compatibility;
- source revision binding;
- overlapping declared write scopes where applicable;
- closeout consistency and `successor_selected: false`;
- active artifacts using retired skill names after cutover.

## Legacy Markdown Compatibility

Existing Markdown-only artifacts follow this migration policy:

```yaml
legacy_artifacts:
  creation_after_cutover: forbidden
  reading: allowed_only_through_named_read_only_parser
  mutation: forbidden_unless_migrated_first
  active_artifact_handling:
    - complete_under_named_old_contract
    - or migrate_with_explicit_validation
  historical_archive_rewrite: not_required
  parser_removal_condition:
    - no selected legacy dispatch
    - no queued legacy runway
    - no active legacy runway
    - no resumable legacy runner state
```

Historical artifacts may retain old terminology when clearly inactive. New
active artifacts may not create new dependencies on retired owners or modes.

## Prototype Policy

Representation prototypes may live temporarily under:

```text
prototypes/contract-first/
```

They must declare:

```yaml
prototype:
  installed: false
  canonical: false
  runtime_references_allowed: false
  removal_condition:
    - accepted content moved to canonical locations
    - rejected alternatives deleted
```

Do not create a permanent `skills-v2/` or parallel command catalog.
