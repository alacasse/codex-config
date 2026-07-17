---
name: planning-artifacts
description: Define project-agnostic placement and naming conventions for durable planning docs, program ledgers, dispatch packets, Batch Runway specs, runner receipts, generated outputs, active-state files, and archives. Use when creating, reorganizing, migrating, or interpreting planning roots and workflow artifacts.
---

# Planning Artifacts

Use this skill when a workflow needs to decide where durable planning artifacts
belong. The convention is project-agnostic: project instructions, local
overlays, active specs, or explicit user direction choose the actual root path.
This skill defines placement, naming, file shape, batch directory conventions,
archives, run artifact roots, and output roots under that root.

For operational pickup, validation, target policy, and projection routing, use
Planning State Diagnostic-First Pickup through `../planning-state/SKILL.md`
first when it is available. Planning State consumes the layout described here;
this skill does not replace its pickup diagnostic.

Do not hard-code a downstream project name, local path, validation command, or
personal overlay into reusable skills. If a project has not declared a planning
root and the placement matters, stop and ask instead of creating loose artifacts
under `plans/`, `planning/`, or the repository root.

## Layout Version

Use **Planning Artifact Layout v1** unless project instructions explicitly name
another convention.

## Root Discovery

Resolve these values before writing artifacts:

- `planning_root`: durable human-readable planning documents.
- `run_artifact_root`: runner-owned JSON state, receipts, manifests, and
  telemetry. If omitted, derive it from the project rule or stop before writing
  runner artifacts.
- `output_root`: generated tool outputs that are not durable planning docs.
- `state_file_policy`: whether durable JSON planning state is `committed`,
  `ignored-local`, `external`, `generated-only`, or `none`.
- `state_file_path`: required only when `state_file_policy` selects a durable
  project-owned state file.
- `projection_policy`: whether rebuildable reporting/query projections are
  `ignored-local`, `external`, `generated-only`, or `none`. A committed
  projection is valid only when project instructions explicitly declare that
  exception.
- `projection_path`: required only when `projection_policy` selects a durable
  projection target.
- `update_authority`: whether workflow commands may update the target directly,
  must ask first, or may only validate/read it.

`planning_root` is required. Projects should declare it in repository
instructions or a local overlay such as `AGENTS.md`, for example:

```markdown
## Planning artifacts

- Layout: Planning Artifact Layout v1
- Planning root: `my-docs/planning`
- Run artifact root: `my-docs/runs`
- Output root: `my-docs/outputs`
- State file policy: `ignored-local`
- State file path: `my-docs/runs/planning-state/state.json`
- Projection policy: `generated-only`
- Projection path: `None`
- Update authority: `ask-first`
- One-shot intake: `my-docs/planning/intake` or `None`
```

If no planning root is declared and the task needs durable coordination state,
stop and ask for the project value. Do not infer a root from another project or
create loose files under `plans/`, `planning/`, or the repository root.

If a command needs to write durable JSON state or projections and the project
has not declared a compatible policy, stop before writing. Read-only diagnostics
may still operate from Markdown-only planning roots. Generic skills must not
bake in `codex-config` committed paths, ignored local overlay paths from another
project, or any other project-specific state location as a reusable default.

Preferred discovery order:

1. Explicit user direction for the current task.
2. Repository instructions or local overlays.
3. Existing active-state files such as `CURRENT.md`.
4. Existing adjacent ledger/spec paths named by the user.
5. A documented repo-owned default.

If the task is only a trivial one-shot note and no durable coordination state is
needed, a project may allow a small intake area. Without that project rule, do
not invent one.

## Canonical Shape

Use a program/workstream layout for durable ledger-driven work:

```text
<planning-root>/
  CURRENT.md

  programs/
    <program-slug>/
      CURRENT.md
      LEDGER.md

      findings/
      notes/

      batches/
        <batch-id>-<batch-slug>/
          dispatch.md
          runway.md
          closeout.md
          completed-slices.md

      archive/
        completed/
        superseded/
        abandoned/

  intake/
    README.md

<run-artifact-root>/
  <runner-name>/
    <program-slug>/
      <run-id>/
        run-state.json
        run-manifest.json
        telemetry/
        receipts/
        batches/

<output-root>/
  <tool-or-output-name>/
```

Projects may place these roots under one parent or split them. The important
boundary is semantic:

- `planning_root` contains human-authored or human-readable coordination docs.
- `run_artifact_root` contains operational runner evidence and machine state.
- `output_root` contains generated products, reports, indexes, or other tool
  outputs.
- `program_archive_root` contains inactive program planning documents retained
  for reference.

Do not put raw JSON run state, receipts, telemetry, generated indexes, or bulky
tool output inside the active planning tree unless a project explicitly declares
that exception.

## Active-State Files

`CURRENT.md` files are for fresh-agent handoff. Keep them compact and current;
they are not ledgers, transcripts, or a competing pickup algorithm.

This section defines the required shape of active-state files. For operational
pickup order, validation, target policy, and projection routing, use
`planning-state`; do not infer active work from old filenames while a Layout v1
`CURRENT.md` path exists.

The root `CURRENT.md` should include:

- planning layout version
- planning root, run artifact root, and output root
- active programs with paths to their `CURRENT.md` files
- allowed one-shot intake location, or `None`
- migration exceptions and expiry condition, if any

Each program `CURRENT.md` should include:

- program slug and one-line purpose
- current ledger path
- selected dispatch path, or `None`
- active Batch Runway spec path, or `None`
- queued batch path or ID, if any
- latest closeout path, if any
- run artifact location for the program
- program archive location
- next safe action
- blockers or stop conditions

## Program Ledgers

Every long-lived ledger owns a program directory unless project instructions
define an equivalent workstream root. A program ledger should live at:

```text
<planning-root>/programs/<program-slug>/LEDGER.md
```

Use nearby `findings/` and `notes/` only for supporting durable context. Do not
bury the active ledger in a notes folder.

## Batch Directories

Co-locate the selected dispatch packet, concrete Batch Runway spec, closeout,
and completed-slice archive for one batch:

```text
<program-root>/batches/<batch-id>-<batch-slug>/
  dispatch.md
  runway.md
  closeout.md
  completed-slices.md
```

The path encodes lineage:

```text
program ledger -> batch directory -> dispatch -> runway -> closeout
```

Use one batch directory per selected batch. Do not scatter one batch across
global `dispatch/`, `runways/`, and `closeout/` directories unless an existing
project convention explicitly requires that compatibility shape.

## Naming

Use stable, lowercase ASCII slugs:

- `program-slug`: short noun phrase, hyphen-separated.
- `batch-id`: stable program-local identifier such as `b1`, `apr-21`, or
  `lr-b3`; preserve existing ledger IDs when they already exist.
- `batch-slug`: short goal phrase, hyphen-separated.
- `run-id`: timestamp or runner-generated opaque ID that is unique within the
  runner/program directory.

Names should describe the workstream, not the agent session. Avoid dates in
program and batch slugs unless the date is part of the domain fact.

## State Vocabulary

Use these batch states unless a project defines its own:

- `candidate`: plausible future batch, not selected.
- `selected`: dispatch packet is current input for spec creation.
- `queued`: concrete runway spec exists but execution has not started.
- `active`: execution is in progress.
- `completed`: implementation, validation, review, and closeout are done.
- `superseded`: replaced by a newer accepted plan.
- `abandoned`: intentionally stopped and not expected to resume.
- `blocked`: waiting on a named decision, dependency, or external condition.

Record state in the program ledger and program `CURRENT.md`; do not infer it
only from filenames.

## One-Shot Planning

For small notes that do not belong to a long-lived program, use an explicitly
allowed intake area:

```text
<planning-root>/intake/<short-slug>.md
```

An intake note must either be promoted to a program/batch, archived, or left with
a short reason why it remains standalone. The intake area must not become the
default home for ledgers, dispatch packets, runway specs, or closeout reports.

## Archives

Archive by semantic reason:

```text
<program-root>/archive/completed/
<program-root>/archive/superseded/
<program-root>/archive/abandoned/
```

The program archive root is `<program-root>/archive/` unless project
instructions declare a different program-local archive location. Archive
completed or superseded planning docs when they should remain readable but
should not be treated as active coordination state. Keep active-state files
pointing at current artifacts only.

## Migration Guidance

Do not migrate downstream project artifacts as part of applying this reusable
skill unless the user explicitly asks for that project migration.

For a large existing planning root, migrate active coordination state first and
historical material second. A good migration preserves pickup safety before it
improves visual tidiness.

### Migration Inventory

Before moving files, write or update a compact migration inventory in the old or
new planning root. The inventory should classify each artifact as one of:

- `active-ledger`: current source of truth for selecting work.
- `active-dispatch`: selected packet for the next spec creation pass.
- `active-runway`: spec that may still be executed or resumed.
- `closeout`: completed batch report or reconciliation evidence.
- `historical-runway`: completed or superseded spec retained for reference.
- `finding-note`: review, audit, characterization, or design note.
- `runner-artifact`: JSON state, receipts, manifests, telemetry, or inventories.
- `generated-output`: generated reports, indexes, summaries, or tool products.
- `unknown`: requires human review before moving.

For each row, record:

- old path
- target path or `leave-in-place`
- classification
- active status: `active`, `historical`, `superseded`, `abandoned`, or `unknown`
- owning program slug, if known
- redirect needed: `yes` or `no`
- blocker, if any

Do not move `unknown` rows into an active program path. Either classify them or
place them in a dated/quarantined migration archive with a note that they are
not active coordination state.

### Active-First Sequence

Use this sequence when the old root has an active ledger plus substantial
history:

1. Declare the new `planning_root`, `run_artifact_root`, and `output_root` in
   project instructions or local overlay before moving files.
2. Create the root `CURRENT.md`.
3. Identify each active long-lived ledger and create one program directory for
   each active workstream.
4. Move or copy active ledgers into program `LEDGER.md` files. Prefer moving
   when project tooling and references can be updated immediately; otherwise
   leave a short redirect note at the old path.
5. Create each program `CURRENT.md` and name the current ledger, selected
   dispatch packet, active runway spec, next safe action, and known blockers.
6. Move active dispatch/runway/closeout sets into batch directories, preserving
   their lineage.
7. Move runner JSON, receipts, manifests, telemetry, and input inventories to
   `run_artifact_root`; keep only links or summaries in planning docs.
8. Move generated outputs to `output_root`; keep only links or summaries in
   planning docs.
9. Move historical runways, closeouts, and notes into program archives only
   after active pickup paths are correct.
10. Update project instructions, README files, ledgers, and active specs so new
    agents stop writing loose artifacts to the old root.

### History Retention

Historical artifacts should remain findable but not look active.

- Completed or superseded dispatch/runway/closeout sets belong under
  `<program-root>/archive/completed/` or
  `<program-root>/archive/superseded/`.
- Abandoned work belongs under `<program-root>/archive/abandoned/` with a short
  reason.
- Historical notes that do not clearly belong to one program may stay in a
  root-level migration archive if the project declares one, but they must not be
  treated as selected dispatch or active queue state.
- Keep old filenames when they carry useful search value, but rely on
  `CURRENT.md` and ledgers for active state.
- Prefer redirect notes over duplicate copies when old paths may still be
  referenced by humans, docs, or tools. Each redirect note should name the new
  path and whether the old path is retained only for compatibility.

### Validation

After migration, validate by reading the files, not by trusting the move:

- root `CURRENT.md` points to every active program.
- each active program `CURRENT.md` names exactly one active ledger and at most
  one selected dispatch and active runway.
- every active batch directory has the expected dispatch/runway/closeout files
  or explicitly records which are absent.
- old active paths are either absent, ignored by project rules, or contain
  redirect notes.
- runner JSON and generated outputs are outside active planning docs unless a
  project explicitly declares an exception.
- project instructions name the new root and forbid new loose planning artifacts
  in the old root except for documented compatibility paths.

## Consumer Rules

For `legacy-removal`:

- Place a legacy evidence artifact under an existing program root only when
  project policy or public `plan-batch` supplies that evidence target.
- Keep dispatch handoff material as evidence for public `plan-batch`; do not
  create a selected batch directory, selected dispatch packet, queue state,
  lifecycle state, runway, or closeout.
- Keep evidence inventories compact; put generated outputs outside planning and
  never create runner artifacts from an evidence-only workflow.

For `architecture-program-runway`:

- Resolve the existing program ledger, `CURRENT.md`, and just-completed batch
  directory for same-batch closeout reconciliation only.
- Do not treat layout ownership as grouping, selection, dispatch, runway,
  queue, lifecycle-planning, or successor authority.
- Keep runner receipts and JSON state in the run artifact root, not in the
  program ledger.

For `batch-runway`:

- Resolve the already queued or active runway at
  `<program-root>/batches/<batch-id>-<batch-slug>/runway.md` for execution.
- Keep `dispatch.md`, `runway.md`, `closeout.md`, and completed-slice archives
  co-located.

For public `plan-batch`:

- Supply Layout v1 paths and names while `plan-batch` retains every semantic
  selection, review, approval, dispatch, runway, and queue decision.
- This layout handoff grants no queue, dispatch, runway, or lifecycle mutation
  authority.
