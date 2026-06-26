# Program Ledger Template

Use this template when creating or restructuring a broad architecture findings
ledger that feeds future Batch Runway specs.

````markdown
# <Area> Architecture Findings

## Purpose

Keep broad findings visible across multiple future runways. This document is
the program ledger above individual Batch Runway specs.

## Current Direction

- <Guardrail or target direction>
- <Boundary that should remain stable>
- <Public contract that must not change unless explicitly reclassified>

## Source Context

- Review source: `<path or summary>`
- Completed runways: `<paths>` or `None`
- Current baseline: `<commit or date>`
- Related ADRs/docs: `<paths>`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| 1. <finding> | Open | None | <next concrete action> | <main files, risk, guardrails> |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| <name> | <ids> | Ready | <shared seam/profile> | <dependency or None> | <profile> | <path or TBD> | TBD |

## Selected Batch Brief / Dispatch Packet

Use this section to point to the dispatch packet for the next fresh
`batch-runway create-spec` session.

For single-batch programs, the dispatch packet may live here.

For multi-batch programs, write the dispatch packet to a nearby file such as:

- `dispatch/<batch-id>-selected-brief.md`
- `dispatch/<batch-id>-dispatch.md`

Then put that path in the Batch Queue `Dispatch` column instead of duplicating
the full packet here.

Current dispatch:

- Batch: `<batch-id or None>`
- Dispatch: `<path or None>`
- Status: `<Ready | In runway | Completed | Blocked>`
- Notes: `<one-line note>`

## Dispatch Packet Template

Use this shape inside the separate dispatch file when a multi-batch program
needs a bounded handoff artifact.

```yaml
batch_id: <stable-name>
source_program_ledger: <this file>
included_findings:
  - id: <finding-id>
    title: <short title>
excluded_findings:
  - id: <finding-id>
    reason: <why it waits>
goal: <one-sentence target outcome>
owner_seam: <module/package/boundary>
validation_class: <profile or harness expectation>
guardrails:
  - <public contract, behavior, or ownership rule to preserve>
dependencies_satisfied:
  - <evidence or None>
dependencies_blocking:
  - <blocking dependency or None>
suggested_slices:
  - <slice-sized step, not a full execution contract>
stop_conditions:
  - <condition that should stop spec creation or execution>
expected_spec_path: <local plan path or naming convention>
```

## Recommended Work Order

1. <Next batch and why>
2. <Next candidate and dependency>
3. <Later cleanup or opportunistic work>

## Planning Rules

- Create one concrete Batch Runway spec at a time unless explicitly asked for
  multiple.
- Create or update a selected batch brief before invoking `batch-runway`
  create-spec from a broad program ledger.
- Future fresh spec-creation agents should consume the selected batch brief and
  minimum ledger excerpt, not the full raw findings source.
- If a later agent needs the raw findings source, it must state the specific
  missing question before reopening it.
- Every generated runway must name which findings it covers and which remain
  open.
- Mark a finding `Prepared` when tests or seams improve but the production
  finding remains.
- Mark a finding `Closed` only after implementation, validation, review, and
  ledger closeout are complete.
- Keep unrelated deferred findings visible.
- Keep only compact closeout evidence in this ledger: dispatch path, spec path,
  commit range, validation result, review result, and unresolved follow-ups.
````

## Batch Queue Statuses

- `Candidate`: plausible but not selected.
- `Ready`: selected or ready to become the next concrete runway.
- `In runway`: concrete spec exists and is active.
- `Completed`: concrete runway closed and ledger reconciled.
- `Deferred`: intentionally delayed.
- `Blocked`: waiting on a decision, dependency, or external constraint.

## Closeout Checklist

After a concrete runway finishes:

1. Read the completed slice archive, commits, validation notes, and review
   result.
2. For each covered finding, decide: `Closed`, `Prepared`, `Open`, `Split`, or
   `Superseded`.
3. Update `Covered by` with spec path and commit evidence.
4. Update the batch queue row to `Completed` or explain remaining work.
5. Select or refresh the next `Ready` batch only if evidence supports it.
