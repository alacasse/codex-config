---
name: legacy-removal
description: Identify, scope, and track project-agnostic legacy-removal work before concrete implementation planning, optionally using dead-surface-audit for test-retained surface evidence. Use when a repository or workstream shows obsolete internal design such as compatibility shims, deprecated aliases, fallback branches for removed behavior, dual old/new paths, transitional wrappers, obsolete entry points, stale names, tests or docs preserving superseded behavior, or agents preserving compatibility the user did not request; also use before internal breaking refactors, migration cleanup, module/API consolidation, temporary compatibility-layer removal, canonical-model replacement, or Batch Runway planning when legacy-cleanup scope is still unclear. Do not use for ordinary bug fixes, small features, already scoped runway execution, explicitly required public API compatibility, required phased migration compatibility, broad deletion without evidence, style-only cleanup, or speculative rewrites.
---

# Legacy Removal

Use this skill as discovery and scoping before concrete execution planning. It
produces legacy findings, evidence, decisions, and optionally one selected
dispatch packet.

Responsibility boundary:

```text
legacy-removal
  owns: ledger, scope, canonical model, compatibility decisions, batch candidates, selected dispatch packet

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
- Do not preserve compatibility merely because it existed before.
- Speculative compatibility is a defect.
- Require scope and evidence before deletion.
- Require a concrete reason before keeping compatibility.
- Prefer one canonical path per behavior.
- Prefer failing loudly over silently supporting obsolete internal behavior.
- Make tests describe the canonical model instead of protecting obsolete
  behavior.
- Keep durable records compact and actionable.
- Do not collapse unrelated legacy findings into one batch.
- Do not load auxiliary skills unless they materially improve the decision.

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
   entrypoints, public contracts, and known external callers. Load
   `dead-surface-audit` only when test-retained liveness or import-topology
   evidence would materially improve the decision.
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

| ID | Evidence type | Source | Location | Observation | Implication |
| --- | --- | --- | --- | --- | --- |
| E1 | code/test/doc/caller/config | ordinary inspection/dead-surface-audit/etc. | path or symbol | what was found | why it matters |
| E2 | test-retained surface | dead-surface-audit | path or symbol | Tests assert import shape only | Candidate for deletion or test migration |

## Legacy findings

| ID | Status | Severity | Location | Legacy pattern | Why it matters | Recommended action |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | Open | blocker/major/minor | path or symbol | shim/alias/fallback/dual-path/legacy-test/stale-name/etc. | impact on conceptual surface area | delete/rename/update-test/defer/keep-with-justification |
| L2 | Open | major | path or symbol | test-retained compatibility surface | Tests preserve old shape without runtime caller evidence | delete or migrate tests first |

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
