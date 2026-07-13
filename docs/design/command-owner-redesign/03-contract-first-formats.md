# Contract-First Formats

## Purpose

This document defines the accepted representation for hybrid skills and active
planning artifacts. Representation is subordinate to ownership: adding YAML does
not make a bridge skill a real owner.

Success requires both:

```yaml
representation:
  contracts_parseable: true
  machine_facts_canonical: true
  prose_not_authoritative: true

ownership:
  duplicate_workflow_decisions: 0
  broad_runtime_owner_dependencies: 0
  old_owner_deletion_test: passed
```

## Design Principles

- YAML holds stable operational facts.
- Numbered steps hold the normal procedure.
- Explicit IF/THEN rules hold branching and stopping.
- Short prose explains dangerous or non-obvious rationale.
- Rare cases, examples, compatibility detail, and long procedures live in
  trigger-loaded references.
- One machine fact has one structured owner.
- Do not create a dense repository-specific DSL.
- Do not convert narrative prose into YAML-shaped prose.
- Keep contracts versioned and mechanically validated.
- Keep active artifacts readable in ordinary Git review.
- Keep SQLite derived and rebuildable.

## Skill Representation

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

Only dangerous or non-obvious invariants.
```

Discovery frontmatter remains minimal. The operational contract lives under one
stable `## Contract` heading.

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
  conditional: []

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

Required top-level fields:

```text
schema
identity
purpose
owns
reads
writes
requires
delegates
forbids
outputs
stops_when
references
```

Empty collections are allowed. Missing fields are not.

## Audience Profiles

The common shape supports distinct audience profiles:

```text
human-command-owner
support-mechanism
evidence-skill
authoring-support
```

Profile validators enforce different ownership constraints without inventing
separate dialects.

## Ownership and Dependency Validation

A deterministic validator rejects or reports:

- a skill owning and forbidding the same decision or write;
- two command owners owning the same decision;
- two skills owning the same durable fact without an accepted shared mechanism;
- a support mechanism owning a human workflow decision;
- an unknown delegated target;
- a dependency cycle;
- a missing referenced file;
- a command owner depending on a retired broad owner;
- an evidence skill owning queue, selection, execution, or closeout state;
- multiple canonical contract blocks for one skill;
- a reference cycle;
- a reference outside the allowed toolchain root;
- a per-command schema or ownership dialect.

Mechanical validation may detect explicit structured contradictions and known
migration residues. It must not claim to understand arbitrary prose semantics.
Broader cosmetic migration and prose contradiction findings remain independent
review evidence unless expressed through controlled identifiers.

## Schema Evolution

```yaml
schema_compatibility:
  writer_emits: v1
  reader_accepts:
    - v1
  unknown_schema_version: block
  unknown_fields_within_v1: reject_unless_explicitly_allowed
  optional_field_addition:
    requires: accepted_compatible_decision
  required_field_change:
    requires: new_schema_version
  semantic_ownership_change:
    requires:
      - new_schema_version
      - accepted_architecture_decision
  deprecation:
    minimum_read_support: named_migration_condition
```

Equivalent policies apply to every planning-artifact schema.

Every emitted active contract records:

```yaml
producer:
  toolchain_generation: stable | candidate
  toolchain_commit: full-sha
  schema_version: string
```

## Procedure and Decision Rules

The contract states authority and invariants. Numbered procedure states normal
order. Decision rules state branches.

Example normal path:

```text
1. Validate root and generation context.
2. Inspect current planning state.
3. Resolve the canonical ledger.
4. Branch on selected, queued, or active state.
5. Select exactly one eligible finding when idle.
6. Split, block, or narrow when required.
7. Create and validate the dispatch.
8. Create and validate the runway.
9. Apply explicit state transitions.
10. Stop before implementation.
```

Example branch:

```text
IF the selected dispatch source revision is stale:
  block without partial writes.
```

## References

`references[*].load_when` is the single canonical machine representation of
reference loading. A Markdown reference-loading section may explain it but may
not define a second trigger list.

A reference may deepen procedure but may not redefine the main contract.

## `skill-authoring` v1

`skill-authoring` is complete and authoritative before command-owner migrations.
It has one core skill and optional conditionally loaded references under the same
version.

```yaml
schema: skill-contract/v1
identity:
  name: skill-authoring
  audience: authoring-support
purpose: >-
  Create, migrate, and audit contract-first hybrid skills using accepted
  ownership, canonicality, procedure, reference, and ambiguity rules.
owns:
  decisions:
    - contract_extraction
    - skill_structure_design
    - ownership_conflict_reporting
    - reference_split_recommendations
  durable_facts: []
forbids:
  - workflow_execution
  - planning_state_mutation
  - silent_ownership_resolution
  - unapproved_schema_fields
  - preservation_of_source_prose_by_default
  - yaml_presence_as_migration_success
```

Core prerequisites:

```text
accepted skill-contract/v1
accepted ownership vocabulary
accepted skill canonicality
accepted reference-loading rules
deterministic validators
```

The core does not require complete planning-artifact schema implementation.
Planning guidance lives at:

```text
skills/skill-authoring/references/planning-artifact-authoring.md
```

It loads only when a task creates or modifies a supported planning artifact and
must declare supported schema names and versions. An unsupported schema blocks.
It may not redefine core ownership or canonicality.

Required trials:

1. one narrow evidence or analysis skill;
2. one command-like skill with normal procedure, multiple branches, stop
   conditions, and delegated mechanisms.

Target command owners do not depend on `skill-authoring` at runtime.

## Active Planning Artifact Representation

Each active Markdown artifact has exactly one structured operational block near
the beginning plus human-readable context.

```markdown
# Batch CCFG-20

## Operational Contract

```yaml
schema: planning-runway/v1
...
```

## Objective

Human-readable context.
```

Companion YAML, generated Markdown, and full contract frontmatter remain rejected
as the initial default.

## Canonical Program State in `CURRENT.md`

Each active program `CURRENT.md` contains exactly one canonical block:

```yaml
schema: planning-current/v1
program: codex-config
revision: 1
ledger: docs/plans/programs/codex-config/LEDGER.md
selected_dispatch: null
queued_runway: null
active_runway: null
latest_closeout: path-or-null
blockers: []
producer:
  toolchain_generation: stable
  toolchain_commit: full-sha
```

The block owns all machine lifecycle pointers and blockers. Prose may explain but
may not redefine them.

Write contract:

```yaml
expected_revision_required: true
expected_file_hash_required: true
write_temp_adjacent: true
atomic_replace_required: true
reread_and_validate_required: true
before_and_after_receipt_required: true
```

Prototype proof:

- stale revision rejects without partial write;
- fresh session reads state without prose scanning;
- rollback restores a compatible recorded revision;
- unrelated prose does not churn;
- duplicate pointer definitions are rejected.

## Canonical Ledger in `LEDGER.md`

Default representation: one canonical structured block per finding.

```yaml
schema: planning-finding/v1
id: CCFG-18
revision: 1
title: Establish Stable and Candidate Generations
provenance:
  source_id: COR-001
  source_commit: immutable-sha
  source_section: immutable-url
lifecycle:
  status: open
dependencies: []
scope:
  summary: string
  included: []
  excluded: []
evidence:
  pointers: []
next_action:
  command: plan-batch
  condition: explicit_request
```

A compact index or table is derived from or mechanically validated against the
finding blocks. It has no semantic authority.

Multi-item intake transaction:

```text
read whole file at expected hash
-> parse all finding blocks
-> apply caller-decided mutations in memory
-> validate IDs, provenance, dependencies, and revisions
-> regenerate or validate derived index
-> render deterministically
-> write adjacent temporary file
-> atomic replace
-> reread and validate
-> emit one receipt naming all touched findings
```

The prototype compares per-finding blocks with one global block for:

- multi-item atomicity;
- duplicate detection;
- diff locality;
- merge conflicts;
- parsing and error locality;
- per-finding revisions;
- derived index consistency;
- SQLite projection equality.

Changing the default to one global block requires blocking prototype evidence and
an explicit accepted decision.

## Planning Artifact Schemas

### `planning-dispatch/v1`

```yaml
schema: planning-dispatch/v1
artifact:
  id: ccfg-example
  program: codex-config
  revision: sha256
source:
  ledger_path: absolute-or-canonical-relative-path
  ledger_revision: sha256
  finding_ids: []
selection:
  outcome: selected
  rationale_code: string
scope:
  goal: string
  included_finding_ids: []
  deferred_finding_ids: []
  owner_seam: string
  batch_kind: string
  risk_summary: []
approval_gates: []
dependencies:
  satisfied: []
  blocking: []
runway:
  expected_path: path
execution_context:
  toolchain_source_root: absolute-path
  canonical_planning_repository_root: absolute-path
  implementation_target_root: absolute-path
stops_when: []
producer:
  toolchain_generation: stable
  toolchain_commit: full-sha
```

### `planning-runway/v1`

```yaml
schema: planning-runway/v1
artifact:
  id: ccfg-example
  source_dispatch: path
  source_dispatch_revision: sha256
batch:
  kind: migration
  status: queued
execution:
  result_contract: registered-agent/v2
  branch_policy: explicit
  dirty_worktree_policy: strict
  successor_selection: forbidden
  implementation_target_root: absolute-path
slices: []
review:
  final_gate: registered-reviewer
closeout:
  same_batch_only: true
  required_artifacts: []
producer:
  toolchain_generation: stable
  toolchain_commit: full-sha
```

### `planning-closeout/v1`

```yaml
schema: planning-closeout/v1
artifact:
  batch_id: ccfg-example
result:
  status: completed
  implementation_commits: []
evidence:
  validation: {}
  review: {}
reconciliation:
  finding_mutations: []
  selected_dispatch_after: null
  queued_runway_after: null
  active_runway_after: null
  successor_selected: false
execution_context:
  canonical_planning_repository_root: absolute-path
  implementation_target_root: absolute-path
producer:
  toolchain_generation: stable | candidate
  toolchain_commit: full-sha
```

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
      - define_second_status
      - define_second_dependency_graph
  derived_artifacts:
    must_declare:
      - source_artifact
      - source_revision
```

## Compatibility Policy

- New active artifacts use accepted target schemas after their cutover gate.
- Old active artifacts complete under stable contracts or are explicitly migrated.
- Archived historical artifacts are not rewritten.
- Legacy readers are read-only, caller-scoped, and removed when active and
  resumable legacy state reaches zero.
- Unknown schema versions block rather than fall back to prose inference.

## Non-Goals

- no parallel execution;
- no custom inheritance system;
- no canonical SQLite planning state;
- no automatic semantic interpretation of arbitrary prose;
- no migration of all historical artifacts;
- no permanent compatibility layer.
