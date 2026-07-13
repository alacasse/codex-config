# Command-Owner Workflow Redesign

## Status

```yaml
status: design-bootstrap
implementation_authorized: false
active_migration_phase: phase-0-isolation-and-baseline
source_baseline:
  repository: alacasse/codex-config
  commit: 86db50f91b0df4c00d5fa26beda0091796a43e81
design_branch: architecture/command-owner-redesign
```

This package defines the target architecture and controlled migration for the
ledger and batch workflow skills in `codex-config`.

It is a design authority, not an implementation runway. Creating these files
does not authorize skill rewrites, state migration, ledger mutation, batch
selection, or execution.

## Objective

Replace the current bridge architecture with a simpler ownership model in
which:

- `add-to-ledger` owns fresh work intake and canonical ledger mutation;
- `plan-batch` owns bounded selection, scope shaping, dispatch creation, runway
  specification, and validation-profile selection;
- `work-batch` owns execution, recovery, commit evidence, finalization,
  closeout, and same-batch reconciliation;
- shared support components apply narrow deterministic mechanisms without
  making human workflow decisions;
- `architecture-program-runway` and `batch-runway` are ultimately deleted as
  broad workflow owners;
- skills and durable planning artifacts use contract-first hybrid Markdown;
- `skill-authoring` v1 is finalized before the target command-owner skills are
  migrated and then refined compatibly through dogfooding;
- migration safety is demonstrated through behavior contracts and scenario
  tests rather than preservation of historical topology.

## Architectural Verdict

The current command-owner skills expose the correct user-facing commands, but
they remain bridge owners over older workflow owners:

```text
add-to-ledger
  -> planning-state
  -> planning-artifacts
  -> architecture-program-runway

plan-batch
  -> planning-state
  -> planning-artifacts
  -> architecture-program-runway
  -> batch-runway create-spec

work-batch
  -> planning-state
  -> planning-artifacts
  -> batch-runway execute-spec
  -> architecture-program-runway closeout-runway
```

The target preserves delegation while eliminating duplicate workflow
ownership:

```text
human-facing command owner
  -> normalized state diagnostic
  -> narrow artifact/state mechanism
  -> narrow worker, reviewer, validation, and commit mechanisms
```

## Evidence Classification

Use these labels in all design and migration work:

- `verified-current`: directly supported by current repository behavior,
  source, tests, or active artifacts;
- `documented-intent`: stated by an ADR or normative repository document;
- `inference`: a conclusion derived from multiple verified facts;
- `target-decision`: an accepted target architecture rule;
- `open-decision`: requires explicit human resolution;
- `historical-evidence`: useful source context that is not current authority.

Do not silently promote an inference or historical rule into a target decision.

## Required Reading Order

Every fresh agent working on this redesign must read:

1. this file;
2. [`decisions.md`](decisions.md);
3. the current phase in
   [`04-migration-program.md`](04-migration-program.md);
4. only the contract and scenario sections named by the current task;
5. the selected implementation artifact, when implementation is later
   authorized;
6. the minimum source implementation needed to answer a specific evidence
   question.

Do not begin with historical batches or broad repository scans when this
package answers the current question.

## Package Contents

| Document | Authority |
|---|---|
| [`01-source-behavior-contracts.md`](01-source-behavior-contracts.md) | Implementation-neutral behaviors that the target must preserve or deliberately change. |
| [`02-target-ownership-model.md`](02-target-ownership-model.md) | Single-owner target architecture, interfaces, allowed dependencies, and forbidden dependencies. |
| [`03-contract-first-formats.md`](03-contract-first-formats.md) | Contract-first skill and planning-artifact representation, including the early authoritative `skill-authoring` v1 workflow. |
| [`04-migration-program.md`](04-migration-program.md) | Required phase order, entry gates, exit gates, bridge rules, authoring bootstrap, and cutover strategy. |
| [`05-behavioral-test-matrix.md`](05-behavioral-test-matrix.md) | Scenario matrix that proves workflow behavior independently from legacy skill names and prose. |
| [`06-deletion-conditions.md`](06-deletion-conditions.md) | Measurable removal conditions for legacy owners, modes, routing, tests, fixtures, and vocabulary. |
| [`decisions.md`](decisions.md) | Accepted, superseded, deferred, rejected, and open decisions. |

## Source Implementation Scope

Treat the following as the source implementation to analyze through
`port-by-contract` reasoning:

- `skills/add-to-ledger/`
- `skills/plan-batch/`
- `skills/work-batch/`
- `skills/port-by-contract/`
- `skills/architecture-program-runway/`
- `skills/batch-runway/`
- `skills/planning-state/`
- `skills/planning-artifacts/`
- `skills/legacy-removal/`
- `skills/dead-surface-audit/`
- `skills/test-quality-review/`
- `scripts/planning_state.py`
- architecture-program runner modules and contracts where they consume the
  workflow;
- `codex-features.json`, `skills-lock.json`, and agent metadata;
- schemas, fixtures, active planning state, relevant completed batches, and
  tests.

The source implementation is evidence. Its file split, skill names, mode names,
routing chain, and compatibility tests are not automatically target contracts.

## Port-by-Contract Use

Use these modes conceptually or explicitly:

1. `intake-source`
2. `distill-contract`
3. `design-target`

Do not use `create-port-runway` for the redesign bootstrap. The current runway
skills are part of the source implementation being replaced and must not become
the architecture authority for their own replacement.

## Bootstrap Safety

The current installed skills are linked to their source checkout. Development
must therefore use an isolated candidate lane:

```text
stable source checkout + default CODEX_HOME
  performs and reviews migration work

candidate branch/worktree + separate CODEX_HOME
  contains and tests target skills
```

Do not modify the installed stable checkout in place while a coordinator,
worker, or reviewer is relying on its current skill contracts.

Do not introduce a permanent `skills-v2/`, `skills-next/`, or version-suffixed
human command set. Candidate skills should occupy their final `skills/<name>/`
paths on an isolated branch or worktree.

## Authoring Bootstrap

The target command-owner migrations must not invent the hybrid format while
performing their own ownership transfers.

Before `add-to-ledger`, `plan-batch`, or `work-batch` is migrated:

1. `skill-contract/v1` must be accepted and mechanically validated;
2. `skill-authoring` v1 must be complete at `skills/skill-authoring/SKILL.md`;
3. its ownership, canonicality, ambiguity, and cosmetic-migration rules must be
   authoritative;
4. it must be validated on `port-by-contract` or an equivalent representative
   skill;
5. it must be installed and tested in the candidate `CODEX_HOME`;
6. the agent's generic skill-writing guidance may supply universal mechanics,
   but repository-specific contract-first rules take precedence.

Dogfooding may produce compatible v1 refinements. It must not create separate
contract dialects for each migrated skill.

## Program Invariants

- Exactly one migration phase may be active.
- Exactly one implementation batch may be selected.
- No implementation batch may begin before its entry gate is satisfied.
- `skill-authoring` v1 must be authoritative before target skill migration.
- A phase must remove legacy ownership, not only add target surfaces.
- No temporary bridge may exist without a named caller, reason, owner, allowed
  scope, and deletion condition.
- Old tests do not justify retaining old topology.
- Temporary coexistence is not architectural completion.
- `work-batch` closeout must stop before successor selection.
- Historical artifacts may retain old names when clearly archived; new active
  artifacts may not create new dependencies on retired owners.
- GitHub issues #48, #49, and #50 are source proposals incorporated through the
  accepted decisions in this package. They are not independent execution
  authorities.

## Current Next Safe Action

Review this design package for contradictions and unresolved decisions. After
human acceptance, a fresh design-only session may decompose the migration into
ordered implementation batches. It must not implement those batches in the
same session.
