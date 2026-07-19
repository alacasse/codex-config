# Slice-Shape Policy Direction

## Status

- Decision status: accepted historical direction; the bounded correction was
  completed and reconciled; richer policy design remains deferred.
- Program: `codex-config`.
- Related finding: CCFG-26.
- Original policy issue: GitHub issue #60.
- Ledger intake issue: GitHub issue #66.
- Related completed batch: `ccfg-26a-permanent-vertical-runway-contract`.
- Completed corrective batch: `ccfg-26-slice-shape-policy-correction`.
- Historical sequencing constraint: this direction was resolved by the completed
  slice-shape correction before the later, now-superseded CCFG-26B planning
  attempt. It no longer authorizes CCFG-26B.

This document records the reasoning that followed the completion of CCFG-26A. It is not an executable runway and does not select, queue, or authorize implementation work.

## Context

GitHub issue #60 was created after CCFG-25 demonstrated that several so-called slices were effectively mini-batches. They grouped broad owner construction, caller migration, legacy removal, repository-wide validation, and installation into large horizontal phases. Individual slices crossed too many seams and required too much coordinator context before a durable commit could be produced.

The original intent was broader than migration work. The desired planning behavior was to prefer slices that take one concrete scenario through a complete path to a durable, independently understandable result. Migration and ownership-transfer work provided the immediate example, but they were not meant to define the only place where slice direction matters.

CCFG-26A implemented a narrower contract. It made the full vertical-slice contract apply only when a slice has the exact machine-readable value `risk: migration`. The same predicate was added to the candidate planner, reviewer, deterministic queue gate, and `planning-runway/v1` schema. Migration work now receives useful protection, including owner movement, caller migration, coexistence, rollback, and removal evidence.

The implementation is internally consistent, but it couples two independent concerns:

1. **Risk** describes the mutation or ownership hazard of the work.
2. **Shape** describes how the work is decomposed into executable increments.

A migration may be vertical or, in an exceptional case, legitimately horizontal. A non-migration feature, refactor, validation change, or cleanup may also benefit from vertical decomposition. Therefore, `risk: migration` is not a sound selector for slice direction.

## What We Learned

### Verticality should remain a bias, not become an unquestioned law

Vertical slices are a strong default because agents naturally plan by implementation layer:

1. build schemas and foundations;
2. build implementation;
3. migrate callers;
4. update tests and documentation;
5. run final convergence.

That decomposition is easy to describe but frequently produces oversized slices with no independently useful intermediate result.

A vertical bias pushes planning toward a different question:

> What is the smallest complete scenario that can be implemented, validated, reviewed, and committed as a durable result?

However, the team has not yet accumulated enough experience to claim that every implementation slice must always be vertical. Some work may have an indivisible contract boundary, no valid partially migrated state, or a genuinely mechanical cross-cutting change where forcing a vertical scenario would create artificial prose rather than improve execution.

The current decision is therefore:

> Prefer vertical slices by default, while allowing an explicitly justified horizontal override.

This is a planning policy, not a property of migration risk.

### The policy should not be copied into every owner

The repository is expected to evolve toward reusable and potentially open-source workflow tooling. Future users may have different project structures, risk tolerances, planning styles, or execution environments. Encoding `vertical` independently in planner instructions, reviewer instructions, schema conditionals, deterministic validation, and tests would make the policy difficult to change and easy to drift.

The reusable workflow should consume one resolved policy. A project should be able to choose or override that policy through an external project-owned configuration surface.

This follows an existing repository principle: reusable skills remain project-neutral, while project-specific behavior belongs in project instructions, a local overlay, an active specification, or a reference document.

### Historical runway compatibility is not required

Planning runways in this repository are execution artifacts and historical evidence, not a public compatibility API. The skill library is still evolving, and the candidate generation has not completed integration.

No implementation should be added to parse or preserve obsolete slice-shape representations merely because old runways exist in Git history. Historical artifacts remain readable at their original commits. Current schemas, fixtures, and validators may change directly.

Do not create:

- a compatibility reader for prior runway shapes;
- a second runway dialect solely for this correction;
- migration code for archived or completed runways;
- fallback behavior that silently accepts the old coupling.

## Accepted Direction

### 1. Decouple slice risk from slice shape

`risk` and `shape` become orthogonal dimensions.

Conceptually:

```yaml
risk: migration
shape:
  selected: vertical
```

or:

```yaml
risk: low
shape:
  selected: horizontal
  override_reason: >-
    The contract and all consumers must change atomically because no valid
    intermediate state exists.
```

Migration-specific ownership evidence remains conditional on migration risk. Slice-shape policy does not.

### 2. Externalize the default and override rule

The minimum useful policy surface contains only the behavior that has actually been decided:

```yaml
schema: slice-shape-policy/v1
default_shape: vertical
allow_override: true
require_override_reason: true
```

The exact path, discovery mechanism, and artifact integration remain implementation decisions for the corrective batch. The likely direction is a project-owned policy referenced from the active program context, rather than a hard-coded constant in reusable workflow code.

The initial policy must remain deliberately small. It should not yet define:

- changed-line or changed-file thresholds;
- categories of approved horizontal work;
- a plugin system;
- policy inheritance;
- multiple bundled planning strategies;
- automatic shape selection heuristics;
- human-approval tiers;
- a complete theory of vertical and horizontal slices.

### 3. Persist the selected shape on each new slice

A planned slice should record the shape selected under the resolved policy.

Minimum conceptual form:

```yaml
shape:
  selected: vertical
  override_reason: null
```

Horizontal exception:

```yaml
shape:
  selected: horizontal
  override_reason: >-
    Splitting the contract change would create an unsupported intermediate
    state with two incompatible representations.
```

The persisted decision is useful for review, execution telemetry, future analysis, and later policy redesign. It also prevents shape from being inferred indirectly from risk labels or free-form prose.

### 4. Keep deterministic enforcement narrow

The deterministic boundary should verify policy consistency, not attempt to decide architecture quality.

It may verify that:

- a resolved policy exists;
- the selected shape is valid;
- the default shape requires no override;
- a non-default shape is allowed;
- a required override reason is present and non-empty;
- migration-specific evidence remains complete when `risk: migration`.

It should not decide whether the override reason is persuasive. That remains a planning and independent-review judgment.

### 5. Preserve migration-specific protections

CCFG-26A added useful migration evidence. The correction must not discard it.

Migration and ownership-transfer work should continue to identify, where applicable:

- owner before and owner after;
- migrated callers or scenarios;
- ownership coexistence;
- retained routes and their reasons;
- removal slice or condition;
- a complete migration matrix;
- rollback-safe ownership boundaries.

These requirements become a migration extension layered beside slice shape, rather than the mechanism that activates vertical planning.

## Minimum Corrective Work (Historical)

This section records the scope that the completed slice-shape correction was
required to satisfy before the historical CCFG-26B planning attempt. Its
`should` and `must` statements govern that closed correction only; they do not
authorize current or future CCFG-26B work. CCFG-26A remains completed historical
evidence and must not be reopened or rewritten.

The minimum batch should produce one complete planning scenario:

```text
project policy
  -> plan-batch resolves the policy
  -> batch_planner selects the default vertical shape
  -> batch_plan_reviewer checks the shape decision independently
  -> deterministic validation proves policy consistency
  -> planning-runway/v1 persists the selected shape
  -> a justified horizontal override is accepted
  -> an invalid or unjustified override is rejected
```

Likely candidate surfaces include:

- project-owned policy configuration and its active-program reference;
- `skills/plan-batch/**`;
- `agents/batch_planner.toml`;
- `agents/batch_plan_reviewer.toml`;
- `scripts/plan_batch.py`;
- `schemas/planning-runway-v1.schema.json`;
- focused planning-contract and behavioral-scenario tests;
- associated feature metadata and changelog entry when required.

The planning step must derive the exact path and ownership boundary from current repository contracts rather than treating this list as pre-authorized implementation scope.

## Minimum Acceptance Behavior

The corrective batch should prove at least these behaviors:

1. A non-migration slice uses the configured vertical default.
2. A migration slice uses the same shape policy rather than deriving shape from risk.
3. A permitted horizontal override with a non-empty reason is accepted.
4. A horizontal override is rejected when overrides are disabled.
5. A horizontal override is rejected when the policy requires a reason and none is supplied.
6. Migration ownership evidence remains required independently of selected shape.
7. Planner, reviewer, deterministic validation, and the persisted runway consume one resolved policy without contradictory hard-coded defaults.
8. Completed and archived runways are not migrated or supported through compatibility code.
9. Final-range validation remains a batch gate and is not disguised as an implementation slice.

## Explicit Non-Goals

The corrective batch must not:

- implement or transfer `work-batch` execution, recovery, finalization, closeout, or reconciliation ownership;
- select or prepare CCFG-26B through CCFG-26E;
- reopen CCFG-26A;
- create a new generic configuration framework;
- define universal thresholds for slice size;
- claim that horizontal slices are inherently invalid;
- define every field that a future vertical slice must contain;
- build automatic architecture classification;
- add backward compatibility for historical runways;
- introduce a permanent public policy API beyond the minimum project-owned boundary needed now;
- settle the final open-source configuration design before the command-owner refactor is complete.

## Deferred Design Questions

After the larger refactor and additional dogfooding, revisit:

- whether `vertical` and `horizontal` are sufficient shape values;
- which fields form the durable semantic definition of a vertical slice;
- whether an override requires only reviewer approval or explicit human approval;
- whether policy belongs at repository, program, batch, or invocation scope;
- whether multiple policy profiles should be shipped;
- how execution telemetry should influence later planning decisions;
- whether coordinator compaction, changed paths, line deltas, review lenses, and validation breadth should generate warnings;
- what defaults are appropriate for an extracted open-source project;
- whether the policy format should remain configuration data or become a replaceable strategy interface.

These questions are intentionally deferred. The immediate objective is to preserve the option to answer them later without leaving the current migration-only coupling in place.

## Sequencing Decision (Historical)

This sequence governed the slice-shape correction and is now historical:

1. the correction was captured in the canonical ledger under CCFG-26;
2. one bounded corrective preparation batch was planned;
3. the externalized minimum slice-shape policy was implemented and validated;
4. CCFG-26 was reconciled while later execution-flight children remained
   unselected;
5. the permitted later continuation to CCFG-26B was never implemented.

On 2026-07-19, CCFG-26B was explicitly superseded before implementation and the
canonical queue was cleared. This historical sequencing decision no longer
authorizes selection, preparation, execution, resumption, or amendment of
CCFG-26B. Current direction is
`ccfg-26-execution-state-authority-direction.md`.

## Decision Summary

The accepted direction is:

- `risk` does not determine slice direction;
- vertical is the initial project default;
- horizontal remains available as an explicitly justified override;
- the default and override rule are external project policy, not duplicated constants;
- every newly planned slice persists its selected shape;
- migration-specific ownership evidence remains separate and intact;
- deterministic validation checks policy consistency while independent review judges architectural quality;
- no backward compatibility is required for historical runways;
- richer policy design is deferred until after the command-owner refactor and more practical experience.

## Intake Decision (Historical)

- Ledger identity: `CCFG-26`.
- Parent finding status at intake: `Prepared`; CCFG-26A remained completed
  historical evidence.
- Candidate work at intake: one bounded slice-shape policy correction before the
  now-superseded CCFG-26B.
- No dispatch was selected, no batch was queued, and no runway was active by
  this intake.
- The corrective preparation batch was later selected, completed, and
  reconciled. Current CCFG-26 status and next action come only from canonical
  `CURRENT.md`, `LEDGER.md`, and
  `ccfg-26-execution-state-authority-direction.md`.
