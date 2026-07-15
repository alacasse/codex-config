---
name: skill-authoring
description: Agent-facing support for creating, migrating, and auditing contract-first hybrid skills.
---

# Skill Authoring

Apply this authoring-time support when an agent must create, migrate, or audit a
hybrid skill against accepted ownership and canonicality rules. It owns the
contract-first shape of that work. Generic writing, scaffolding, examples, and
presentation mechanics remain outside this skill.

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: skill-authoring
  audience: authoring-support
producer:
  toolchain_generation: candidate
  toolchain_commit: 596fc7e5e153bb1a89a94010d272efa4ce4ce0ce
  schema_version: skill-contract/v1
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
reads:
  required:
    - accepted_behavior
    - accepted_ownership
    - accepted_audience
    - accepted_canonicality
    - accepted_output_contract
  conditional:
    - migration_request
    - before_contract_catalog
    - after_contract_catalog
    - accepted_migration_policy
writes:
  - authored_skill_document
  - authoring_audit
requires:
  mechanisms:
    - skill_contract_validator
  evidence_skills: []
delegates:
  - responsibility: contract_validation
    target: skill_contract_validator
  - responsibility: migration_comparison
    target: skill_contract_validator
forbids:
  - workflow_execution
  - planning_state_mutation
  - silent_ownership_resolution
  - unapproved_schema_fields
  - preservation_of_source_prose_by_default
  - yaml_presence_as_migration_success
outputs:
  one_of:
    - authored_skill_result
    - audited_skill_result
    - ambiguity_block
    - migration_block
stops_when:
  - missing_accepted_decision
  - ownership_conflict
  - contract_validation_failure
  - migration_guard_failure
references: []
```

## Procedure

1. Collect the accepted behavior, ownership, audience, canonicality, migration,
   and output facts supplied by the caller or its authoritative artifacts.
   Treat any required fact that is absent or contradictory as unresolved; do
   not invent a default.
2. Extract exactly one closed-world `skill-contract/v1` contract. Record only
   accepted fields and decisions, and keep the frontmatter name, contract
   identity, audience, producer identity, and declared outputs consistent.
3. Compare every claimed decision, durable fact, write, requirement, and
   delegation with the accepted owners. Report conflicting claims and missing
   owner decisions before writing prose.
4. Design the document so the canonical contract, normal procedure, conditional
   branches, rationale, and reference-loading explanation remain distinct.
   References may deepen the procedure but may not redefine the contract.
5. Author only the requested hybrid-skill document or audit. Preserve accepted
   behavior, but do not preserve source wording or source topology merely
   because it already exists.
6. Delegate structural validation to the existing `skill_contract_validator`
   mechanism. Supply the explicit toolchain root and document paths to its
   public validate operation; do not copy its schema or validation rules into
   this skill.
7. When the request is a migration, apply the migration guards below through
   the same validator before reporting success.
8. Return the authored or audited result and validation evidence. Never execute
   the workflow described by the authored skill.

## Branches

- If an accepted required decision is missing, return an `ambiguity_block` that
  names the missing decision and the authority that must supply it.
- If two sources claim incompatible ownership, return an `ambiguity_block` that
  names both claims. Never choose an owner silently.
- If a migration lacks a complete before catalog, complete after catalog, or
  accepted migration policy, return a `migration_block` without claiming
  progress from newly present YAML.
- If contract or migration validation fails, return the corresponding block
  with the validator diagnostics and leave the failed claim unaccepted.
- Otherwise return one `authored_skill_result` or `audited_skill_result` with
  the validated contract path and the decisions applied.

Blocked results identify the status, reason, unresolved decisions or conflicts,
and the named authority or evidence needed to resume. They do not mutate
planning state or settle the missing decision.

## Migration Guards

Migration validation requires all three inputs: an explicit before catalog, an
explicit after catalog, and an accepted migration policy. Pass those catalogs
and policy to the existing validator's public comparison operation.

Success requires the comparison to prove the accepted ownership transfers,
absence of forbidden retained-owner dependencies, uniqueness of durable facts,
and meaningful contract change for any rename. A new YAML block, a new path, or
successful parsing alone is never migration success. Block when the catalogs
are incomplete, the policy is unavailable or ambiguous, an expected transfer
did not occur, or validation reports unresolved ownership.

## Rationale

Contract extraction precedes prose so ownership and canonicality remain
mechanically reviewable. Keeping procedure, branches, rationale, and references
separate prevents explanatory text from becoming a second contract or a silent
decision surface. Using the existing validator keeps schema interpretation and
migration comparison under one deterministic owner.

This skill is authoring support, not a workflow command or runtime dependency of
the skills it produces. It does not execute authored procedures, write planning
state, resolve ownership ambiguity, or take over generic prose and scaffolding.
Project-specific paths, caches, issue policies, planning layouts, and validation
commands must come from project instructions or an active specification rather
than from this reusable core.

## Reference Loading

The contract's `references[*].load_when` entries are the only canonical loading
triggers. Reference prose may explain those triggers but cannot add another
trigger list or redefine core ownership, canonicality, procedure, or stopping
rules. Examples are explanatory only and can never become a second canonical
contract.

This core has no conditional references. Its canonical `references` list is
therefore empty, and no reference may be inferred or loaded until that list is
changed under the same accepted contract version.
