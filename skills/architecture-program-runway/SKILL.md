---
name: architecture-program-runway
description: Agent-facing program-ledger support used by add-to-ledger, plan-batch, and work-batch for broad finding intake, grouping, sequencing, selected dispatch packets, queue state, and closeout reconciliation.
---

# Architecture Program Runway

Agent-facing program-ledger support for `add-to-ledger`, `plan-batch`, and
`work-batch`. Do not present this as the normal human command for ledger
intake, batch planning, or batch closeout; use the command-owner skill first,
then apply this workflow when program-level grouping, sequencing, selected
dispatch packets, queue state, or closeout reconciliation are needed.
`batch-runway` owns the concrete execution spec, semantic slice boundaries, and
per-slice execution workflow.

Use `../planning-artifacts/SKILL.md` for Planning Artifact Layout v1 placement,
naming, active-state file shape, batch directories, archives, and run/output
roots. Use `../planning-state/SKILL.md` for Diagnostic-First Pickup,
current/validate ordering, target-policy checks, and projection routing.
`planning-state` provides validated operational facts; this skill still owns
program selection, grouping, sequencing, queue state, selected dispatch packets,
handoff to `batch-runway`, and closeout reconciliation.

## Core Rule

Do not turn a broad findings document into one giant batch. Preserve the
overarching ledger, maintain a compact batch queue, dispatch one selected batch
with a bounded brief, and leave unselected findings visible with status and
rationale.

The long-lived program ledger is durable context across batches. The live agent
context is only for the current mode and, at most, the current selected batch.
Do not require future fresh agents to re-read the raw findings document or
re-derive grouping from scratch after the ledger and batch queue exist.

## Agent Model

- The main agent owns `architecture-program-runway` decisions and edits.
- This skill manages program-level state: durable ledger, finding grouping,
  batch queue, selected dispatch packet, and closeout reconciliation.
- `batch-runway` owns the concrete spec, semantic slice shape, and execution
  workflow for exactly one selected batch.
- Slice implementation and review stay delegated through `batch-runway` to
  `runway_worker` and `runway_reviewer`.
- Fresh spec-creation agents do not own global program prioritization. They
  consume one selected dispatch packet and produce one concrete Batch Runway
  spec.

## Program/Runway Handoff Boundary

Keep program ledgers and concrete runway ledgers separate.
`architecture-program-runway` owns the program ledger and program-level ledger
updates when a finding is grouped, selected, queued, superseded, split,
prepared, or closed. It also owns the selected dispatch packet and the batch
queue state that point a fresh `batch-runway create-spec` pass at exactly one
selected batch.

`batch-runway` owns the concrete runway artifact after that selected dispatch
is handed off: the semantically sliced spec, validation profile selection,
slice active ledger, completed-slice archive, review routing, commit receipts,
and per-slice execution workflow. It may name covered and deferred program
findings in the runway for traceability, but it does not reselect the program
batch or mutate the program findings ledger as part of routine spec creation or
slice execution.

The normal flow is:

1. This skill selects one batch and writes or refreshes `dispatch.md`.
2. A fresh `batch-runway create-spec` pass consumes that dispatch and writes
   `runway.md`.
3. `batch-runway execute-spec` completes slices, validation, review, commits,
   and the concrete execution ledger/archive.
4. This skill consumes compact closeout evidence from the completed concrete
   runway and reconciles the program ledger. If invoked by `work-batch`, this
   closeout is limited to the just-completed batch and must stop before
   selecting another batch.

## Required First Steps

1. Read applicable repo instructions and local overlays.
2. If Layout v1 or a ledger-driven planning root is active, use
   `planning-state` Diagnostic-First Pickup and projection-reporting guidance
   for the operational state facts before broader exploration.
3. For placement, naming, active-state file shape, batch directory, archive, or
   run/output-root questions, follow `planning-artifacts`.
4. Read the findings, review, PRD, ADR, selected dispatch packet, or planning
   document needed for the chosen mode.
5. Read active or recently completed related runway specs only enough to know
   what is already closed, prepared, or open.
6. Check the worktree before editing planning files.
7. Decide the mode: `intake-findings`, `group-batches`, `select-next-batch`,
   `create-next-runway`, `closeout-runway`, or `reprioritize`.

If the planning location, active ledger, status vocabulary, or relationship to
`batch-runway` is unclear, stop and ask for the missing value instead of
creating a speculative plan.

## Active-State Handoff

Use `planning-state` Diagnostic-First Pickup for normal ledger-driven pickup
and batch-currentness questions when Planning Artifact Layout v1 is active.
After that handoff, this skill makes the semantic program decision:

- If a selected dispatch, active runway, or queued batch is present, stop
  selection and report, create the missing concrete spec, or execute the queued
  runway according to the request.
- If no selected or queued batch is present, choose the relevant program from
  the diagnostic facts and request language, then read the minimum ledger row
  and source packet needed to select exactly one next batch.
- Write or update the co-located batch directory for that one selected batch:
  `dispatch.md` first, then `runway.md` only in `create-next-runway` mode.
- Update the program `CURRENT.md` and `LEDGER.md`, then stop before coding
  unless the user explicitly asked to execute.

Knowledge-graph queries, broad `find` or repository-wide `rg` scans over the
planning tree, old flat dispatch/runway filenames, generated reports,
historical redirect ledgers, recent commits, or source modules are escalation
reads only after the Planning State Diagnostic and active ledger expose a
specific unresolved evidence question. State that question before continuing.

## Modes

- `intake-findings`: normalize an architecture review or messy notes into a
  durable findings ledger. Keep findings individually addressable.
- `group-batches`: cluster findings into future runway candidates by owner
  seam, validation profile, dependency, risk, and likely file area.
- `select-next-batch`: choose exactly one next batch, explain why it is next,
  state why the other candidates wait, and write or update a compact selected
  batch brief.
- `create-next-runway`: create one concrete `batch-runway` spec for the selected
  group from the selected batch brief. Read and follow the `batch-runway` skill
  in create-spec mode.
- `closeout-runway`: after execution, update the program ledger. Mark findings
  `Closed`, `Prepared`, `Open`, `Split`, or `Superseded` based on evidence from
  commits, validation, review, and the completed runway archive. When this mode
  is invoked from `work-batch`, reconcile only the just-completed batch and do
  not select, refresh, dispatch, create, or prepare successor work. For `/goal`
  or other runner-driven work, also record a compact goal-run evaluation
  receipt.
  `closeout-runway` must not clear a queued dispatch/runway before execution
  unless the user explicitly requests cancellation or abandonment, or the
  closeout evidence documents a blocker that makes execution unsafe. A
  dispatch/runway pair alone is not closeout evidence.
- `reprioritize`: reassess remaining findings after the codebase or constraints
  changed. Update ordering without hiding deferred work.

For `/goal` or prompt-driven bounded runner use, read
`references/goal-runner-v1.md` before starting the loop. For the split-phase
local CLI runner, read `references/local-runner-v1.md`.

For active legacy-removal programs, classify targeted legacy surfaces in the
program ledger or selected dispatch packet. Workers execute already-classified
slice instructions, reviewers flag unclassified preservation, aliases,
wrappers, fallback paths, and cleanup scaffolding, and closeout keeps deferred
or unreconciled legacy visible instead of marking it `Closed`.

## Local Runner Usage

If the user asks to run the local architecture program runner, read
`references/local-runner-v1.md` and invoke the runner CLI. Do not manually
perform the runner phases in the current conversation.

Use the runner's final state and receipt output for the user-facing summary.

Infer the narrowest useful mode from the user request. If the user asks to
"create the batch/spec", use `select-next-batch` briefly, then
`create-next-runway`.

## Grouping Heuristics

Group findings into the same future batch only when most of these are true:

- They share one owner seam or closely adjacent seams.
- They use the same validation profile and harness expectations.
- Each slice can be independently validated and committed.
- Earlier slices create a boundary consumed by later slices, without requiring a
  broad behavior migration.
- The work can be expressed through cohesive semantic slice boundaries without
  carrying unrelated context.

Do not use a target slice count as a grouping heuristic. A cohesive batch may
produce one slice, while a complex batch may produce more than five when every
boundary is independently justified. Group and split on ownership, risk,
validation, sequencing, and acceptance boundaries instead.

Split findings into separate batches when they touch different owner modules,
mix test-only and production-harness work, require different stop conditions,
change public contracts, or would make one slice depend on unresolved discovery
from another workstream.

Use characterization slices sparingly. A characterization slice belongs in a
batch only when it directly reduces risk for that batch. Otherwise, keep it as a
separate candidate.

## Vague Row Selection Guard

Before writing a selected dispatch, confirm that each requested ledger row can
be shaped into one bounded batch with clear owner seam, risk class, acceptance
criteria, and stop conditions. Do not let a vague or mixed-risk row silently
expand into unrelated discovery, decisions, cleanup, migration, demotion, or
contract-narrowing work.

If a row mixes evidence gathering, classification, decisions, destructive
cleanup, migration, demotion, or contract narrowing without enough owner, risk,
or acceptance boundaries, choose one of these outcomes before creating
`dispatch.md`:

- Split the row into smaller program findings when the source row already
  authorizes distinct bounded work.
- Block the row when a decision, owner, risk class, acceptance boundary, or
  approval gate is missing.
- Narrow the selected dispatch to characterization-only or evidence-only work
  when the row mentions deletion, demotion, migration, cleanup, or narrowing
  but does not precisely authorize that risky implementation.

Record the split, block, or narrow-scope rationale in the program ledger and
selected dispatch packet. Newly discovered destructive, migration, demotion, or
contract-narrowing work must become explicit follow-up ledger work unless the
source row already authorized that risk with precise boundaries.

## Ledger Statuses

Use these finding lifecycle statuses unless a project already defines its own.
Keep them separate from batch artifact state such as a selected dispatch,
queued runway, or active concrete spec:

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

Do not mark a finding `Closed` because a related spec exists. Close only from
completed implementation evidence.

Do not widen or rewrite a `Pending` finding through ordinary source-ledger
edits after selected, queued, or active batch artifacts control its scope.
Allowed scope changes must be explicit: closeout evidence, supersession,
abandonment, split, a named amendment, or a new follow-up finding. If the
selected dispatch or concrete runway no longer matches the source finding,
record the amendment or follow-up before continuing; do not hide the change in
narrative notes.

## Program Ledger Shape

For a detailed reusable template, read
`references/program-ledger-template.md` when creating or reorganizing a ledger.

Every program ledger should make these things visible:

- Current direction and guardrails.
- Planning root, program root, program archive root, run artifact root, and
  output root when Planning Artifact Layout v1 is active.
- Findings ledger with status, covered-by evidence, next action, and notes.
- Batch queue with grouping rationale, dependencies, validation class, dispatch
  path, and spec path.
- Recommended next batch and explicit deferred candidates.
- Selected dispatch packet path, or inline single-batch dispatch, for the next
  fresh `batch-runway create-spec` pass.
- Closeout rules for updating findings after a concrete runway completes.
- Goal-run evaluation receipts when `/goal`, an automation, or a local runner
  drives one or more program batches.

## Selected Batch Brief

The selected batch brief is the dispatch packet and primary input contract
between program planning and a fresh concrete runway-spec creation session. It
should be small enough that a new agent can create the next `batch-runway` spec
without loading the whole raw findings document or replaying the full grouping
rationale.

Create or refresh the brief whenever `select-next-batch` chooses a batch or
`create-next-runway` would otherwise need broad program context. For
single-batch programs, the brief may live inside the program ledger. For
multi-batch programs, write a separate dispatch file near the ledger, such as
`dispatch/<batch-id>-selected-brief.md` or
`dispatch/<batch-id>-dispatch.md`, and link to it from the batch queue instead
of duplicating the full content in the ledger.

When Planning Artifact Layout v1 is active and one selected batch is known,
prefer:

```text
<program-root>/batches/<batch-id>-<batch-slug>/dispatch.md
```

The corresponding Batch Runway spec should be
`<program-root>/batches/<batch-id>-<batch-slug>/runway.md`.

The brief should include:

- Batch ID and source program ledger path.
- Included finding IDs and short finding titles.
- Explicitly excluded or deferred finding IDs with one-line rationale.
- Goal, owner seam, validation class, and required guardrails.
- Dependencies already satisfied and dependencies still blocking.
- Optional `slice_shape` rationale, if known, describing semantic boundaries
  without full execution contracts or a target count.
- Stop conditions that should prevent spec creation or execution.
- Expected runway spec path or naming convention.
- For active legacy-removal programs, classified legacy surfaces, forbidden
  scaffolding, and stop conditions for unclassified legacy discoveries.

If the selected dispatch uses deletion-test evidence, it must consume the
canonical deletion-test evidence statuses owned by `dead-surface-audit`, or it
must define any local non-canonical labels inline as labels only. A selected
dispatch must not make unsupported generated terms behave like evidence
categories, approval gates, cleanup decisions, migration decisions, demotion
decisions, or contract-narrowing decisions.

After the brief exists, future `create-next-runway` work should consume the
brief plus the minimum ledger excerpt needed for statuses and evidence. Do not
re-open the original broad review unless the brief is missing, contradicted by
new evidence, stale, or explicitly insufficient for a specific stated question.

## Context Compression

- After a durable program ledger and batch queue exist, do not require fresh
  agents to read the full raw findings source.
- Do not paste completed runway logs into the program ledger.
- Preserve only compact evidence in the program ledger: dispatch path, spec
  path, commit range, validation result, review result, and unresolved
  follow-ups.
- Archive detailed execution history in the concrete runway spec or
  completed-slice archive.
- If raw findings are needed later, state the specific missing question before
  reopening the raw source.

## Goal-Run Evaluation

Use this only when a `/goal`, automation, local runner, or similar orchestration
loop drives program progress. Do not require it for ordinary one-shot manual
planning unless the user asks for telemetry.

After a bounded runner pass stops, append or update one compact evaluation
receipt near the program ledger closeout evidence. The receipt is for tuning the
orchestration workflow, not for replacing finding-level closeout.

Include:

- Run ID, runner type, goal prompt or prompt path, start/end timestamps if known.
- Configured bounds such as `max_batches`, allowed modes, and stop policy.
- Batches selected, specs created, batches started, and batches completed.
- Final stop reason: completed bound, blocked, validation failed, review failed,
  stale dispatch, dirty-file conflict, missing project value, context pressure,
  permission issue, user stop, or other.
- Whether the runner used the selected dispatch packet instead of reloading broad
  raw findings unnecessarily.
- Whether it preserved `architecture-program-runway` versus `batch-runway`
  responsibilities.
- Whether the program ledger, dispatch packet, spec ledger, validation evidence,
  review result, and commit receipts were updated consistently.
- Context-management observations, orchestration anomalies, and tuning notes.

Keep this as structured bullets or YAML. Do not paste transcripts, long command
logs, full review text, or implementation chronology into the program ledger.

## Relationship To Batch Runway

When creating the selected concrete batch:

1. Load and follow `batch-runway` in create-spec mode.
2. If Planning Artifact Layout v1 is active, start from Planning State
   Diagnostic facts and the selected dispatch packet. Do not reselect a batch
   while a selected dispatch, active runway, or queued runway already exists.
3. Start from the selected batch brief, not from the full raw findings source,
   unless the brief is missing or stale.
4. Create exactly one local runway spec unless the user explicitly asks for
   multiple.
5. The generated spec must name which program findings it covers and which
   findings remain open.
6. Keep execution contracts in `batch-runway`; do not duplicate full execution
   details in the program ledger.
7. Stop before coding unless the user explicitly asked to execute.

When a concrete runway closes under Layout v1, use Planning State Diagnostic
facts and focused closeout evidence before reading historical plans or broad
generated outputs. Then update the program ledger for the completed batch.
Preserve compact evidence and dispatch information; archive detailed runway
execution history in the concrete runway spec or completed-slice archive, not
in the program ledger. If the route came from `work-batch`, stop there; a later
explicit `plan-batch` request owns successor selection.

## Output Guidance

For planning-only answers, be direct:

- Recommendation: one batch or split.
- Next batch: selected findings and why.
- Deferred: findings that wait and why.
- Dispatch: selected batch brief path or exact section.
- Ledger update needed: exact rows or sections to update.

When editing files, keep the program ledger compact. Prefer tables and short
decision notes over narrative transcripts.
