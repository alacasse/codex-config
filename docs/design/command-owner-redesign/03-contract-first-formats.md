# Contract-First Formats

## Purpose

This document incorporates the design intent of GitHub issues #48, #49, and #50
into one representation strategy for skills and durable planning artifacts.

The representation work is subordinate to the ownership model. A skill does not
become a real owner merely because it contains a parseable YAML block. A
migration succeeds only when both representation and responsibility move.

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
- Finalize the repository-specific authoring workflow before migrating target
  command-owner skills.
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

Do not place the full operational contract in frontmatter. Frontmatter is an
integration and discovery surface; the contract block is the versioned workflow
interface.

## `skill-contract/v1`

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

Every target contract-first skill requires:

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
Optional fields may be added only through accepted schema evolution.

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

## `skill-authoring` v1

GitHub issue #49 proposes a meta-skill for creating, migrating, and reviewing
contract-first skills. The target adopts it as an early authoring authority.

`skill-authoring` v1 must be complete before `add-to-ledger`, `plan-batch`, or
`work-batch` are migrated. It is finalized after `skill-contract/v1` and its
validators are accepted, then validated on `port-by-contract` or an equivalent
representative skill.

### Contract

```yaml
schema: skill-contract/v1

identity:
  name: skill-authoring
  audience: authoring-support

purpose: >-
  Create, migrate, or audit skills against accepted contract-first formats
  without preserving accidental source prose or duplicate ownership.

owns:
  decisions:
    - skill_contract_extraction
    - skill_structure_design
    - instruction_classification
    - ownership_conflict_reporting
    - reference_split_recommendation
  durable_facts: []

reads:
  required:
    - accepted_skill_contract_schema
    - target_skill_purpose
    - intended_owner_boundaries
    - expected_inputs_and_outputs
  conditional:
    - source_skill
    - source_behavior_contract_ids
    - generic_skill_authoring_guidance

writes:
  - target_skill_draft_or_patch
  - ambiguity_report
  - ownership_report
  - validation_checklist

requires:
  mechanisms:
    - skill-contract-schema-validator
    - ownership-conflict-validator
    - reference-validator
  evidence_skills: []

delegates:
  - responsibility: schema_validation
    target: skill-contract-schema-validator
  - responsibility: ownership_validation
    target: ownership-conflict-validator

forbids:
  - workflow_execution
  - durable_planning_state_mutation
  - resolving_ownership_conflicts_silently
  - inventing_unapproved_schema_fields
  - preserving_source_prose_by_default
  - treating_yaml_presence_as_successful_migration
  - hiding_operational_rules_in_rationale

outputs:
  required:
    - contract_first_skill_draft_or_patch
    - ambiguity_report
    - ownership_report
    - validation_result

stops_when:
  - ownership_cannot_be_determined
  - purpose_conflicts_with_another_skill
  - required_inputs_or_outputs_are_unknown
  - requested_change_creates_overlapping_ownership
  - schema_change_requires_human_decision

references:
  - path: references/classification-rules.md
    load_when:
      - migrating_existing_skill
      - auditing_ambiguous_skill
```

### Authoring procedure

```text
1. Identify the skill's externally meaningful purpose.
2. Extract behavior contracts before preserving source structure.
3. Name the exact decisions and durable facts the skill owns.
4. Separate delegated mechanisms from owned decisions.
5. Define reads, writes, outputs, forbidden actions, and stop conditions.
6. Convert the normal path into numbered procedure steps.
7. Convert branches and stops into explicit IF/THEN rules.
8. Keep only dangerous or non-obvious rationale in the main skill.
9. Move rare detail into trigger-loaded references.
10. Run schema, ownership, reference, and cosmetic-migration validation.
11. Report unresolved ambiguity instead of guessing.
```

### Relationship to generic skill-writing guidance

The agent may still use its generic skill-writing skill for universal mechanics
such as:

- discovery frontmatter;
- trigger accuracy;
- concise descriptions;
- progressive disclosure;
- reference organization;
- general Codex skill compatibility.

For repository-specific operational structure and ownership, this document and
`skill-authoring` v1 are authoritative.

```text
repository-specific contract-first rules
  outrank
agent-generic skill-writing conventions
```

The generic guidance must not normalize a target skill back to a
narrative-first structure or silently remove required contract fields.

### Completion gate before owner migration

```yaml
skill_authoring_v1:
  schema_valid: true
  authoritative: true
  validators_green: true
  validated_on:
    - port-by-contract_or_equivalent_representative_skill
  installed_in_candidate_codex_home: true
  runtime_dependency_of_command_owners: false
```

Stable before dogfooding:

- ownership semantics;
- required contract sections;
- canonicality rules;
- ambiguity and cosmetic-migration guards;
- validator interfaces.

May evolve compatibly after dogfooding:

- optional fields;
- report layout;
- size heuristics;
- reference-loading recommendations;
- additional non-breaking validation checks.

A semantic change to `owns`, canonicality, or required boundaries requires an
explicit schema-version decision rather than an undocumented edit.

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
  commit_profile: focused-per-slice
  successor_selection: forbidden
slices:
  - id: slice-1
    depends_on: []
    owner_role: worker
    allowed_read_paths: []
    allowed_write_paths:
      - skills/plan-batch/**
    risk_class: migration
    approval_gate: null
    validation:
      - command: python -m pytest tests/test_plan_batch_workflow.py -q
        class: required-green
review:
  final_gate_role: reviewer
closeout:
  required_artifacts:
    - closeout
    - completed-slices
    - commit-receipts
  required_transition: active-to-completed
  reconcile_same_batch_only: true
```

## `planning-closeout/v1`

```yaml
schema: planning-closeout/v1
artifact:
  type: closeout
  batch_id: ccfg-20-example
  source_runway_revision: sha256:...
result:
  status: completed
  commits:
    - abc1234
evidence:
  validation:
    status: passed
    artifacts: []
  review:
    status: clean
    diff_basis: abc1234
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

Lightweight tooling must:

- locate exactly one structured contract block;
- validate schema version and required fields;
- reject unknown lifecycle transitions;
- validate artifact lineage and source revisions;
- reject unknown slice dependencies and dependency cycles;
- detect unsupported validation classifications and risk classes;
- validate approval gates when required;
- detect declared overlapping write scopes where applicable;
- reject retired broad-owner dependencies;
- report compact actionable errors before delegation;
- preserve readable Git diffs.

Schema validation proves structure. Behavioral scenario tests prove workflow
meaning. Neither replaces independent review.

## Legacy Compatibility

- Historical archived artifacts may remain Markdown-only.
- New active artifacts use the accepted hybrid schemas after cutover.
- A legacy parser is read-only, caller-scoped, and temporary.
- No new artifact may be emitted in a legacy format after its target schema is
  authoritative.
- A legacy parser must name active callers and a measurable deletion condition.

## Acceptance Criteria

The contract-first representation is ready for command-owner migration only
when:

```yaml
acceptance:
  skill_contract_v1:
    parseable: true
    ownership_validation: proven
    reference_validation: proven
  skill_authoring_v1:
    complete: true
    authoritative: true
    validated_on_representative_skill: true
    installed_in_candidate_lane: true
  planning_artifacts_v1:
    dispatch_parseable: true
    runway_parseable: true
    closeout_parseable: true
    canonicality_rules_enforced: true
  migration_safety:
    prototypes_non_authoritative: true
    historical_artifacts_not_bulk_migrated: true
    command_owner_ownership_not_yet_transferred: true
```
