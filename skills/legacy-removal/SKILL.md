---
name: legacy-removal
description: Identify, scope, and track project-agnostic legacy-removal work before concrete implementation planning. Use when a repository or workstream shows obsolete internal design such as compatibility shims, deprecated aliases, fallback branches for removed behavior, dual old/new paths, transitional wrappers, obsolete entry points, stale names, tests or docs preserving superseded behavior, or agents repeatedly preserving compatibility the user did not request; also use before internal breaking refactors, migration cleanup, module/API consolidation, temporary compatibility-layer removal, canonical-model replacement, or Batch Runway planning when legacy-cleanup scope is still unclear. Do not use for ordinary bug fixes, small features, already scoped runway execution, explicitly required public API compatibility, production-safe phased migrations where compatibility is required, broad deletion without evidence, style-only cleanup, or speculative rewrites.
---

# Legacy Removal

Use this skill as discovery and scoping before concrete execution planning. It
produces legacy findings, evidence, decisions, and optionally one selected
dispatch packet.

Responsibility boundary:

```text
legacy-removal
  -> produces legacy findings, evidence, decisions, and optional selected dispatch packet

architecture-program-runway
  -> owns multi-batch program ledger, grouping, prioritization, and selected batch dispatch

batch-runway
  -> owns concrete 3-5 slice spec creation and execution workflow
```

Do not use this skill to implement code, execute slices, make commits, or
orchestrate workers/reviewers.

## Core Principles

- Do not delete code merely because it looks old.
- Do not preserve compatibility merely because it existed before.
- Treat speculative compatibility as a defect.
- Require scope and evidence before deletion.
- Require a concrete reason before keeping compatibility.
- Prefer one canonical path per behavior.
- Prefer failing loudly over silently supporting obsolete internal behavior.
- Make tests describe the canonical model instead of protecting obsolete
  behavior.
- Keep durable records compact and actionable.

A concrete reason for keeping compatibility must name at least one external
caller, public API contract, documented migration requirement, production
compatibility constraint, still-valid test requirement, explicit user
instruction, or temporary transition period with a removal condition.

## Workflow

1. Read applicable repository instructions, local overlays, domain docs, ADRs,
   existing plans, and public compatibility commitments.
2. Define the old model and candidate canonical model. If either is unclear,
   record the uncertainty instead of deleting or preserving by default.
3. Inventory evidence across code, tests, docs, configs, generated artifacts,
   entrypoints, public contracts, and known external callers.
4. Classify legacy patterns: shim, alias, fallback, dual path, legacy test,
   stale name, obsolete entrypoint, transitional wrapper, obsolete doc, or
   another explicit pattern.
5. Decide compatibility item by item. `keep` and `defer` require named reasons;
   `remove` requires evidence that the behavior is obsolete or internal.
6. Group findings into batch candidates only far enough to expose scope,
   sequencing, risk, validation class, and likely slice shape.
7. Create the selected dispatch packet only when one next batch is clear.
8. Hand off:
   - Use `architecture-program-runway` when the ledger spans multiple findings,
     seams, risk classes, or possible batches.
   - Use `batch-runway create-spec` when exactly one clear selected batch is
     ready for a concrete 3-5 slice runway spec.

## Ledger Rules

Write a durable Markdown ledger in the target repository's planning location.
If no planning location is defined, ask or use the smallest repo-local location
consistent with project instructions.

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

## Scope boundary

- Old model being evaluated:
- Candidate canonical model:
- In scope:
- Out of scope:
- Explicitly forbidden compatibility:
- Explicitly required compatibility:
- Destructive-change boundaries:

## Evidence inventory

| ID | Evidence type | Location | Observation | Implication |
| --- | --- | --- | --- | --- |
| E1 | code/test/doc/caller/config | path or symbol | what was found | why it matters |

## Legacy findings

| ID | Status | Severity | Location | Legacy pattern | Why it matters | Recommended action |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | Open | blocker/major/minor | path or symbol | shim/alias/fallback/dual-path/legacy-test/stale-name/etc. | impact on conceptual surface area | delete/rename/update-test/defer/keep-with-justification |

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
