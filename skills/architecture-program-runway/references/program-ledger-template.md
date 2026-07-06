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

Optional for active legacy-removal programs:

```yaml
legacy_removal_policy:
  active: true
  default_classification: remove_now
  rule: "Documented/tested legacy is evidence of legacy, not proof of current support."
legacy_surfaces:
  - surface: "<legacy surface>"
    classification: remove_now | defer_with_explicit_removal_batch | keep_as_current_contract
    reason: "<short reason>"
    affected_contract: "<internal | CLI | schema | artifact | API | import | none>"
    follow_up_batch: "<required for deferred legacy>"
    forbidden_scaffolding:
      - "<alias/wrapper/fallback/test/registry that must not be added>"
temporary_migration_guards: []
deferred_legacy_followups: []
```

## Source Context

- Review source: `<path or summary>`
- Completed runways: `<paths>` or `None`
- Current baseline: `<commit or date>`
- Related ADRs/docs: `<paths>`

## Planning Layout

- Layout version: `Planning Artifact Layout v1` or `<project-specific value>`
- Planning root: `<path>`
- Program root: `<path>`
- Program current file: `<path to CURRENT.md or None>`
- Program archive root: `<path>`
- Run artifact root: `<path>`
- Output root: `<path>`
- One-shot intake allowed: `<path or None>`
- Compatibility exceptions: `<short note or None>`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| 1. <finding> | Open | None | <next concrete action> | <main files, risk, guardrails> |

## Finding Lifecycle Statuses

Keep finding lifecycle status separate from batch artifact state. A selected
dispatch packet, queued runway, or active concrete spec can control a finding
without making `Pending` a batch queue status.

- `Open`: real finding, not yet assigned to selected, queued, or active batch
  artifacts.
- `Ready`: near-selected for the next runway, but not yet controlled by a
  selected, queued, or active batch artifact.
- `Pending`: cut or active batch work controlled by selected, queued, or active
  batch artifacts until closeout, amendment, supersession, split, abandonment,
  or follow-up.
- `Blocked`: waiting on another finding, decision, or external constraint.
- `Prepared`: tests, seams, or caller evidence improved, but the production
  finding is not closed.
- `In runway`: covered by an active concrete runway spec.
- `Closed`: implementation, validation, review, and ledger closeout are done.
- `Superseded`: made irrelevant by a different accepted change.
- `Split`: decomposed into smaller findings.

Do not widen or rewrite a `Pending` finding through ordinary source-ledger
edits after selected, queued, or active batch artifacts control its scope.
Allowed scope changes must be explicit: closeout evidence, supersession,
abandonment, split, a named amendment, or a new follow-up finding. If the
selected dispatch or concrete runway no longer matches the source finding,
record the amendment or follow-up before continuing; do not hide the change in
narrative notes.

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
- `batches/<batch-id>-<batch-slug>/dispatch.md` when Planning Artifact Layout
  v1 is active

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
legacy_removal:
  active: true
  surfaces:
    - name: "<legacy surface>"
      classification: remove_now | defer_with_explicit_removal_batch | keep_as_current_contract
      reason: "<short reason>"
      forbidden_scaffolding:
        - "<alias/wrapper/fallback/test/registry that must not be added>"
  stop_conditions:
    - "A slice discovers an unclassified legacy surface."
    - "A worker would need to preserve legacy not classified as keep/deferred."
  closeout_note: "Reconcile temporary migration guards and deferred legacy before marking findings Closed."
```

## Recommended Work Order

1. <Next batch and why>
2. <Next candidate and dependency>
3. <Later cleanup or opportunistic work>

## Goal Run Evaluations

Use this section only when `/goal`, an automation, a local runner, or another
orchestration loop drives one or more program batches. Keep each receipt compact
so the program ledger stays readable.

```yaml
- run_id: <stable-id>
  runner: </goal | automation | local-runner | manual>
  goal_prompt: <inline summary or prompt file>
  bounds:
    max_batches: <number>
    allowed_modes:
      - <select-next-batch | create-next-runway | closeout-runway | reprioritize>
  batches:
    selected:
      - <batch-id>
    specs_created:
      - <path>
    started: <number>
    completed: <number>
  stop_reason: <completed-bound | blocked | validation-failed | review-failed | stale-dispatch | dirty-file-conflict | missing-project-value | context-pressure | permission-issue | user-stop | other>
  source_of_truth_check:
    used_dispatch_packet: <yes | no | partial>
    avoided_unbounded_raw_findings_reload: <yes | no | partial>
    ledger_updated: <yes | no | partial>
    validation_evidence_linked: <yes | no | partial>
    review_result_linked: <yes | no | partial>
    commit_receipts_linked: <yes | no | partial>
  responsibility_check:
    program_state_owned_by_architecture_program_runway: <yes | no | partial>
    concrete_batch_owned_by_batch_runway: <yes | no | partial>
    implementation_review_delegation_unchanged: <yes | no | partial>
  context_observations:
    - <short note or None>
  orchestration_anomalies:
    - <short note or None>
  tuning_notes:
    - <what to adjust before the next runner pass>
```

## Planning Rules

- Create one concrete Batch Runway spec at a time unless explicitly asked for
  multiple.
- When Planning Artifact Layout v1 is active, use `planning-state`
  current/validate diagnostics before consuming active-state files, selected
  dispatches, queued batches, active runways, blockers, closeout evidence, or
  target policy.
- Treat Planning State Diagnostic output as operational facts only. Program
  grouping, queue state, selected dispatch packets, and closeout reconciliation
  remain owned by `architecture-program-runway`; placement remains owned by
  `planning-artifacts`.
- For program history/reporting, pending-batch inventory, missing closeout
  evidence, runner summaries, or bounded backlog/history reports, read
  `../../planning-state/references/projection-reporting.md` and use
  policy-compatible `report-projection` output before broad historical planning
  scans when `projection_usage` and `projection_rebuild_authority` allow it.
  Missing, blocked, stale, or policy-incompatible projection reports must be
  recorded as explicit blockers, warnings, or fallback decisions.
- Projection reports are read-only planning-state context. They do not select
  architecture batches, replace the program ledger or selected dispatch packet,
  or close findings.
- Create or update a selected batch brief before invoking `batch-runway`
  create-spec from a broad program ledger.
- Future fresh spec-creation agents should consume the selected batch brief and
  minimum ledger excerpt, not the full raw findings source.
- If a later agent needs the raw findings source, it must state the specific
  missing question before reopening it.
- Every generated runway must name which findings it covers and which remain
  open.
- Do not widen or rewrite `Pending` finding scope through ordinary
  source-ledger edits; use closeout evidence, supersession, abandonment, split,
  a named amendment, or a new follow-up finding.
- Mark a finding `Prepared` when tests or seams improve but the production
  finding remains.
- Mark a finding `Closed` only after implementation, validation, review, and
  ledger closeout are complete.
- For active legacy-removal runways, do not mark a finding `Closed` while
  unclassified legacy, unreconciled temporary migration guards, or hidden
  deferred legacy remain.
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

1. If Planning Artifact Layout v1 is active, run or consume `planning-state`
   current/validate diagnostics for the planning root before expanding to older
   plans or generated outputs.
2. For missing closeout evidence, batch evidence, runner-summary, or bounded
   history/reporting questions, follow planning-state projection-reporting
   guidance and use policy-compatible `report-projection` output before broad
   historical scans; treat projection blockers as explicit closeout blockers,
   warnings, or fallback decisions.
3. Read the completed slice archive, commits, validation notes, and review
   result.
4. For each covered finding, decide: `Closed`, `Prepared`, `Open`, `Pending`,
   `Split`, or `Superseded`.
5. Update `Covered by` with spec path and commit evidence.
6. Update the batch queue row to `Completed` or explain remaining work.
7. Select or refresh the next `Ready` batch only if evidence supports it.
8. If a runner drove the work, add a compact goal-run evaluation receipt.
9. For active legacy-removal runways, record removed surfaces, deferred
   surfaces, temporary migration guards that remain, and required follow-up.
