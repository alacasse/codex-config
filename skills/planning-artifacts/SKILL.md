---
name: planning-artifacts
description: Define project-agnostic placement and naming conventions for durable planning docs, program ledgers, dispatch packets, Batch Runway specs, batch-local runtime state, runner artifacts, generated outputs, active-state files, and archives.
---

# Planning Artifacts

Use this skill when a workflow needs to decide where durable planning artifacts
or workflow runtime state belong. The convention is project-agnostic: project
instructions, local overlays, active specs, or explicit user direction choose
the actual planning root.

This skill defines placement, naming, file shape, batch directory conventions,
batch-local runtime layout, optional runner-artifact roots, output roots, and
archives. For operational pickup, use Planning State Diagnostic-First Pickup
through `../planning-state/SKILL.md` first when it is available. Planning State
consumes the layout described here; this layout handoff does not replace its
pickup diagnostic, does not create a competing pickup algorithm, and grants no
queue, dispatch, runway, or lifecycle mutation authority.

Do not hard-code a downstream project name, local path, validation command,
cache location, or personal overlay into reusable skills. If the project has not
declared a planning root and placement matters, stop instead of inventing one.

## Layout Version

Use **Planning Artifact Layout v1** unless project instructions explicitly name
another convention.

## Root Discovery

Resolve these values before writing artifacts:

- `planning_root`: required; contains durable coordination documents and program
  batch directories.
- `batch_runtime_policy`: normally `batch-local`; small state owned by one batch
  lives under that batch directory.
- `run_artifact_root`: optional; reserved for runner-global state, telemetry,
  bulky receipts/logs, or an explicitly configured external backend. It is not a
  mandatory second root for one batch's canonical state.
- `output_root`: optional generated products or reports that do not belong with
  one batch.
- `state_file_policy`: whether JSON state is `committed`, `ignored-local`,
  `external`, `generated-only`, or `none`.
- `projection_policy`: whether rebuildable projections are `ignored-local`,
  `external`, `generated-only`, or `none`.
- `update_authority`: whether workflow commands may update the target directly,
  must ask first, or may only validate/read it.

Preferred discovery order:

1. Explicit user direction for the current task.
2. Repository instructions or local overlays.
3. Existing active-state files such as `CURRENT.md`.
4. The ledger, dispatch, runway, or batch directory already selected.
5. A documented repo-owned default.

The user-selected planning root is sufficient to locate a program ledger and its
batch directories. Do not require the user to choose another root for small
batch-specific runtime state.

If a project needs runner-global artifacts and no optional `run_artifact_root`
is configured, stop only before writing those runner-global artifacts. Do not
block batch-local state that has an accepted batch directory and compatible
state policy.

Temporary directories are for tests and disposable acceptance runs. Allocate
them at execution time through the host platform's temporary-directory facility.
Do not persist a generated temporary path in `CURRENT.md`, a ledger, a dispatch,
or a runway as the durable location of a real batch.

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
          .runtime/
            execution-state.json
            execution-state.lock
            receipts/
          closeout.md
          completed-slices.md

      archive/
        completed/
        superseded/
        abandoned/

  intake/
    README.md
```

Optional separate roots may coexist:

```text
<run-artifact-root>/
  <runner-name>/
    <program-slug>/
      <run-id>/
        run-state.json
        run-manifest.json
        telemetry/
        receipts/

<output-root>/
  <tool-or-output-name>/
```

The semantic boundaries are:

- `planning_root` contains human-readable coordination and the directories that
  define program and batch identity.
- a batch's `.runtime/` directory contains small machine state whose identity and
  lifecycle are exactly that batch;
- `run_artifact_root`, when configured, contains state or evidence whose identity
  is one runner run or an external operational backend rather than one batch;
- `output_root` contains generated products not owned by a batch;
- archives contain inactive planning evidence.

Do not separate a small batch-owned state file merely because it is JSON. Do not
co-locate raw logs, large telemetry, caches, indexes, or bulky generated output
with active planning unless a project explicitly chooses that tradeoff.

## Product And Dogfood Boundary

Storage layout follows the product's user model, not the current repository's
installer or dogfood harness.

The following do not influence generic batch placement unless explicitly
promoted into a product requirement:

- `CODEX_HOME` or `.codex` layout;
- symlink or manifest installation;
- stable/candidate repositories or generations;
- cross-checkout bridge paths or receipts;
- developer-specific absolute paths.

A dogfood adapter may locate or launch the implementation through those values,
but the ledger, batch directory, and batch-local runtime layout remain usable
without them.

## Active-State Files

`CURRENT.md` files are compact fresh-agent handoffs, not ledgers, transcripts,
or a competing pickup algorithm.

The root `CURRENT.md` should include:

- layout version and planning root;
- batch runtime policy;
- optional run-artifact and output roots, or `None`;
- active programs with paths to their program `CURRENT.md` files;
- allowed one-shot intake location, or `None`;
- temporary exceptions and expiry conditions.

Each program `CURRENT.md` should include:

- program slug and purpose;
- current ledger path;
- selected dispatch, queued batch, and active runway, or `None`;
- latest closeout, if any;
- batch runtime policy;
- next safe action;
- blockers and explicit user-owned worktree constraints.

Do not turn `CURRENT.md` into a historical evidence index. Put history in the
ledger, batch directory, or archive.

## Program Ledgers

Every long-lived ledger owns a program directory unless project instructions
define an equivalent workstream root:

```text
<planning-root>/programs/<program-slug>/LEDGER.md
```

The ledger is the executable backlog source. Nearby `findings/` and `notes/`
provide supporting context, not competing work queues.

## Batch Directories

Co-locate one batch's durable planning documents and small batch-owned runtime
state:

```text
<program-root>/batches/<batch-id>-<batch-slug>/
  dispatch.md
  runway.md
  .runtime/
  closeout.md
  completed-slices.md
```

The path encodes lineage:

```text
program ledger -> batch directory -> dispatch -> runway -> runtime state -> closeout
```

Use one batch directory per selected batch. Do not scatter one batch across
global dispatch, runway, state, and closeout directories unless an explicit
backend or compatibility contract requires it.

Batch runtime state should normally be ignored or generated rather than
committed. Its required durability is process-to-process continuity, not Git
history. The project chooses whether `.runtime/` is ignored-local,
externalized, or generated-only.

## Naming And Safety

Use stable lowercase ASCII slugs for program and batch directory names. Validate
path components before constructing batch-local paths. Reject parent traversal,
absolute path injection, ambiguous separators, and collisions under the target
platform's normal filesystem rules.

Version 1 layout safety does not imply protection against a hostile same-user
process replacing namespace entries during a system call. Such a security claim
requires an explicit threat model and feasible implementation primitive.

## Migration And Compatibility

Existing projects with a separate `run_artifact_root` may retain it. Migration to
batch-local state is not mandatory when the separate backend reflects a real
user requirement.

Historical artifacts retain their original paths and meanings. Superseded
planning stays readable but is not active pickup state. New work should not add a
second root solely to preserve an accidental development topology.

## Agent-Facing Handoff

This skill defines placement, naming, file shape, and semantic ownership of
artifact locations. It does not select work, create a dispatch, approve a
runway, execute a batch, reconcile a ledger, or choose a successor.
