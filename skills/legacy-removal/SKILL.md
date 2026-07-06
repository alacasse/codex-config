---
name: legacy-removal
description: Identify, scope, and track project-agnostic legacy-removal work before concrete implementation planning, optionally using dead-surface-audit for test-retained surface evidence. Use when a repository or workstream shows obsolete internal design such as compatibility shims, deprecated aliases, fallback branches for removed behavior, dual old/new paths, transitional wrappers, obsolete entry points, stale names, tests or docs preserving superseded behavior, or agents preserving compatibility the user did not request; also use before internal breaking refactors, migration cleanup, module/API consolidation, temporary compatibility-layer removal, canonical-model replacement, or Batch Runway planning when legacy-cleanup scope is still unclear. Do not use for ordinary bug fixes, small features, already scoped runway execution, explicitly required public API compatibility, required phased migration compatibility, broad deletion without evidence, style-only cleanup, or speculative rewrites.
---

# Legacy Removal

Use this skill as discovery and scoping before concrete execution planning. It
produces legacy findings, evidence, decisions, and optionally one selected
dispatch packet.

When project instructions, local overlays, or active planning docs select
Planning Artifact Layout v1, read `../planning-artifacts/SKILL.md` before
writing or reorganizing the legacy ledger, selected dispatch packet, runner
artifacts, generated outputs, archives, or active-state files.

Use `../planning-state/SKILL.md` before creating, consuming, validating, or
reorganizing Layout v1 legacy-removal ledgers, selected dispatch packets, or
active planning state. Run the Planning State Diagnostic hot path with the
project's resolved planning root:

```bash
python scripts/planning_state.py current --root <planning-root>
python scripts/planning_state.py validate --root <planning-root>
```

Carry forward only compact handoff facts such as selected paths, queued batch,
blockers, redirect warnings, and next safe action. Planning-state diagnostics
do not decide the old model, canonical model, evidence value, compatibility
decision, cleanup-residue classification, or whether legacy code is kept or
removed.

Read `../planning-state/references/projection-reporting.md` before broad
historical scans for supported legacy-removal history/reporting questions such
as pending-batch inventory, missing closeout evidence, batch evidence, bounded
backlog/history reports, or runner summaries that affect handoff context. Use
policy-compatible `report-projection` command output as the normal route before
broad historical scans when `projection_usage` and
`projection_rebuild_authority` permit it. Missing, blocked, stale, or
policy-incompatible projection reports are blockers, warnings, or explicit
fallback decisions before scanning. Projection output is read-only
planning-state context; agents must not query SQLite directly, and projection
output must not decide the old model, canonical model, evidence value,
compatibility decision, cleanup-residue classification, handoff target, or
whether legacy code is kept or removed.

Responsibility boundary:

```text
legacy-removal
  owns: ledger, scope, canonical model, compatibility decisions, batch candidates, selected dispatch packet

planning-state
  owns: current/validate diagnostics, active-state handoff facts, target-policy status, optional projection/report commands

dead-surface-audit
  owns: evidence about surfaces kept alive by tests, import topology, aliases, facades, wrappers, or old module shape

architecture-program-runway
  owns: grouping, prioritization, multi-batch program state, selected batch brief

batch-runway
  owns: concrete 3-5 slice spec creation and execution workflow
```

Do not use this skill to implement code, execute slices, make commits, or
orchestrate workers/reviewers.

## Core Principles

- Do not delete code merely because it looks old.
- Do not delete tests merely because they are inconvenient.
- Do not preserve compatibility merely because it existed before.
- Speculative compatibility is a defect.
- Require scope and evidence before deletion.
- Require a concrete reason before keeping compatibility.
- Report uncertainty instead of inventing callers or contracts.
- Prefer one canonical path per behavior.
- Prefer failing loudly over silently supporting obsolete internal behavior.
- Make tests describe the canonical model instead of protecting obsolete
  behavior.
- Classify cleanup residues instead of letting them become invisible
  compatibility.
- Keep durable records compact and actionable.
- Do not collapse unrelated legacy findings into one batch.
- Do not load auxiliary skills unless they materially improve the decision.

A cleanup residue is a test-only compatibility marker, historical-evidence
bucket, migration guard, old-vocabulary taxonomy, alias, facade, or temporary
scaffold left behind during or after a refactor. A concrete reason for keeping
compatibility or cleanup residue must name at least one external caller, public
API contract, documented migration requirement, production compatibility
constraint, still-valid test requirement, explicit user instruction, or
temporary transition period with a removal condition.

## Workflow

1. Read applicable repository instructions, local overlays, domain docs, ADRs,
   existing plans, and public compatibility commitments.
   If Planning Artifact Layout v1 is active, use `planning-state` `current` and
   `validate` diagnostics before reading active ledgers or selected dispatch
   state as authoritative. For next-task, next-batch, selected-dispatch, or
   queued-work requests, follow `planning-state` Diagnostic-First Pickup before
   broader exploration.
   For supported history/reporting questions not answered by active-state
   diagnostics, use planning-state projection-reporting guidance and
   policy-compatible `report-projection` command output as the normal route
   before broad historical scans.
2. Define the old model and candidate canonical model. If either is unclear,
   record the uncertainty instead of deleting or preserving by default.
3. Inventory evidence across code, tests, docs, configs, generated artifacts,
   entrypoints, public contracts, and known external callers. Load
   `dead-surface-audit` only when test-retained liveness or import-topology
   evidence would materially improve the decision.
4. Classify legacy patterns: shim, alias, fallback, dual path, legacy test,
   stale name, obsolete entrypoint, transitional wrapper, obsolete doc, cleanup
   residue, or another explicit pattern.
5. Decide compatibility and cleanup residue item by item. `keep` and `defer`
   require named reasons; `defer` also requires a removal condition; `remove`
   requires evidence that the behavior is obsolete or internal.
6. Group findings into batch candidates only far enough to expose scope,
   sequencing, risk, validation class, and likely slice shape.
7. Create the selected dispatch packet only when one next batch is clear.
8. Hand off:
   - Use `architecture-program-runway` when the ledger spans multiple findings,
     seams, risk classes, or possible batches.
   - Use `batch-runway create-spec` when exactly one clear selected batch is
     ready for a concrete 3-5 slice runway spec.

## Test preservation rules

Tests are evidence, not authority. A failing test is not automatically evidence
that production behavior is broken, and it is not automatically a requirement.
Classify affected tests before preserving code to satisfy them.

Existing tests may preserve obsolete internal surfaces. Do not preserve obsolete
production code only to keep obsolete tests passing. During legacy removal,
tests that assert legacy topology, importability, aliases, wrappers, or
compatibility shape must be updated or deleted unless they protect a named
external contract.

The goal is not for all old tests to keep passing unchanged. The goal is for the
remaining tests to describe the canonical model. A test may be deleted when its
only purpose was to preserve an obsolete internal surface.

Classify tests affected by legacy removal as:

- `behavioral`: protects externally observable behavior such as CLI output, API
  response, file effects, persisted state, generated artifacts, report fields,
  or runtime behavior.
- `compatibility-contract`: protects a documented public old path or
  compatibility promise that users still rely on.
- `migration-retention`: keeps a temporary facade, wrapper, alias, old import
  path, or transition surface alive after a canonical owner already exists.
- `topology-assertion`: asserts module presence, importability, alias identity,
  `find_spec`, `__all__`, root topology, wrapper existence, or old
  implementation shape without proving externally observable behavior.

Use this decision rule before preserving code because a test fails:

- `behavioral` tests are preservation signals by default.
- `compatibility-contract` tests are preservation signals only when they name or
  link to the external contract.
- `migration-retention` tests are cleanup candidates unless a concrete
  transition requirement remains.
- `topology-assertion` tests are suspect by default and should usually be
  updated or deleted during legacy removal.

Only behavioral tests and documented compatibility-contract tests justify
preserving behavior by default. Migration-retention and topology-assertion tests
should usually be migrated, narrowed, or deleted unless they protect a concrete
external contract, public API commitment, production migration requirement, or
explicit user instruction.

## Relationship to dead-surface-audit

`dead-surface-audit` is an optional auxiliary evidence skill. Load it only when
useful; do not load it for ordinary legacy findings where direct inspection
already gives enough caller, contract, and compatibility evidence.

Use `dead-surface-audit` when a legacy finding involves signals such as:

- tests that assert importability, `find_spec`, `__all__`, alias identity,
  module presence, or root topology
- compatibility facades with unclear production callers
- root modules that mostly re-export owner modules
- deprecated wrappers whose only known callers appear to be tests
- old/new module paths that coexist for possible migration retention
- test-only preservation of old import paths, aliases, or topology
- uncertainty about whether a surface is externally supported or only
  test-retained

Use `dead-surface-audit` when test classification requires deeper evidence about
whether a surface is truly alive. It is especially useful for importability
tests, alias identity tests, root topology tests, compatibility facades, wrapper
surfaces, and test-only callers.

`dead-surface-audit` answers evidence questions, not planning questions. It can
answer:

- production/runtime caller evidence
- CLI or public entrypoint evidence
- docs, ADR, or generated artifact contract evidence
- test-only liveness
- whether tests preserve behavior or only shape/topology
- whether a surface is a deletion candidate, test-migration candidate, valid
  entrypoint, or human contract decision

Convert useful `dead-surface-audit` conclusions into compact legacy-removal
ledger rows. Do not paste the full dead-surface report unless a blocker decision
requires it.

Ambiguous dead-surface results are not automatic deletion. If the audit finds
possible external compatibility but no clear contract, record it as a
Compatibility decision, Open question, `human-contract-decision`, or deferred
finding for `architecture-program-runway`.

## Ledger Rules

Write a durable Markdown ledger in the target repository's planning location.
If no planning location is defined, ask or use the smallest repo-local location
consistent with project instructions.

Under Planning Artifact Layout v1, a legacy-removal effort that spans more than
one finding, decision, or possible batch should own a program directory:

```text
<planning-root>/programs/<program-slug>/LEDGER.md
```

When one next batch is clear, put its selected dispatch packet under:

```text
<program-root>/batches/<batch-id>-<batch-slug>/dispatch.md
```

Do not create loose legacy ledgers or dispatch packets directly under generic
`plans/` or `planning/` unless project instructions explicitly allow that
layout.

Before consuming or updating Layout v1 ledger or dispatch state, use
`planning-state` diagnostics to confirm the current root, program, queued batch,
selected dispatch, blockers, redirects, and safe next action. Treat those
diagnostics as active-state intake only; keep legacy-removal findings and
compatibility decisions evidence-based.

Read `planning-state` target-policy or projection guidance only when the task
needs durable JSON state, generated state fixtures, SQLite projections,
generated projection reports, or target-policy proof. Ordinary Markdown ledger
or dispatch work should not invent durable state locations, generated outputs,
projection databases, cache paths, or downstream project defaults.
Projection reports are planning-state context only. They may help locate
pending work, missing closeout evidence, or batch evidence, but they do not
classify a legacy surface and do not prove liveness or deadness, justify keeping
compatibility, choose a canonical model, or close cleanup residue.

Do not paste long logs or raw transcripts. Link to artifacts or quote only the
evidence needed to justify decisions.

Use this structure:

```markdown
# Legacy Removal Ledger: <title>

## Purpose

<one paragraph describing why legacy-removal scoping is needed>

## Target context

- Target repository:
- Target area:
- Language/runtime/framework, if relevant:
- Current goal:
- Source request or review:
- Related plans/specs/ledgers:
- Planning root:
- Program root:
- Run artifact root:
- Output root:

## Scope boundary

- Old model being evaluated:
- Candidate canonical model:
- In scope:
- Out of scope:
- Explicitly forbidden compatibility:
- Explicitly required compatibility:
- Destructive-change boundaries:

## Evidence inventory

| ID | Evidence type | Source | Location | Test class | Observation | Implication |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | code/doc/caller/config | ordinary inspection | path or symbol | n/a | what was found | why it matters |
| E2 | test evidence | inspection | path::test_name | topology-assertion | Test asserts old import shape only | Candidate for deletion or rewrite |
| E3 | test-retained surface | dead-surface-audit | path or symbol | migration-retention/topology-assertion | Tests assert import shape only | Candidate for deletion or test migration |

## Legacy findings

| ID | Status | Severity | Location | Legacy pattern | Test class | Why it matters | Recommended action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | Open | blocker/major/minor | path or symbol | shim/alias/fallback/dual-path/legacy-test/stale-name/etc. | n/a or behavioral/compatibility-contract/migration-retention/topology-assertion | impact on conceptual surface area | delete/rename/update-test/defer/keep-with-justification |
| L2 | Open | major | path or symbol | test-retained legacy surface | topology-assertion | Old surface is kept alive by shape tests only | delete surface and update/delete tests |

## Canonical model decision

- Canonical owner:
- Canonical API/path/concept:
- Behaviors that must remain:
- Behaviors that may be removed:
- Names that should survive:
- Names that should disappear:
- Tests that should define the new model:

## Compatibility decisions

| Item | Decision | Reason | Required by |
| --- | --- | --- | --- |
| <symbol/path/behavior> | remove/keep/defer | concrete reason | external caller/public contract/test/user requirement/none |
| <ambiguous surface> | defer | possible external compatibility but no clear contract | human-contract-decision/open question |

## Cleanup residue decisions

Use this section when a refactor introduced or left behind test-only
compatibility markers, historical-evidence buckets, migration guards,
old-vocabulary taxonomy, aliases, facades, or temporary scaffolding.

| Item | Decision | Reason | Removal condition |
| --- | --- | --- | --- |
| <marker/path/test taxonomy> | remove-now/keep-with-reason/defer-with-removal-condition | concrete reason | required for every deferred residue |

## Batch candidates

| Batch ID | Goal | Included findings | Deferred findings | Validation class | Risk | Suggested slice shape |
| --- | --- | --- | --- | --- | --- | --- |
| LR-B1 | <goal> | L1, L2 | L3 | focused/unit/harness/docs/manual | low/medium/high | 3-5 compact slice ideas |

## Selected dispatch packet

Use this section only if one next batch is clear.

- Batch ID:
- Source ledger path:
- Included finding IDs:
- Explicitly deferred finding IDs:
- Goal:
- Owner seam:
- Validation class:
- Guardrails:
- Suggested 3-5 slice shape:
- Stop conditions:
- Expected Batch Runway spec path or naming convention:

## Open questions

- <question that blocks safe dispatch, if any>

## Closeout rules

When concrete implementation work closes, update each finding as:

- Closed: removed with validation/review evidence
- Prepared: tests, seams, or caller evidence improved but legacy remains
- Deferred: intentionally left for a later batch
- Superseded: made irrelevant by another accepted change
- Blocked: cannot proceed without a named decision or dependency

Do not mark a legacy-removal finding `Closed` while unclassified cleanup
residue remains. Remove it, keep it with a named reason, or defer it with a
removal condition and follow-up owner.
```

## Relationship To Other Runway Skills

Use `architecture-program-runway` after this skill when the legacy ledger needs
program-level grouping, prioritization, sequencing, or multi-batch closeout
reconciliation. The legacy ledger is source evidence; the architecture-program
ledger owns the batch queue and selected dispatch state.

Use `batch-runway create-spec` after this skill only when the selected dispatch
packet identifies exactly one bounded batch. The Batch Runway spec owns
execution contracts, slice boundaries, validation profile details, delegation,
commits, and closeout workflow.

Do not duplicate full Architecture Program Runway or Batch Runway contracts in
the legacy ledger. Preserve only enough evidence and decision context for those
skills to consume safely.
