# Planning-State Tooling Plan

## Purpose

Move fragile planning coordination out of agent memory and ad hoc Markdown
editing into a small tool-owned state layer. The tool should let agents ask
workflow-level questions and perform workflow-level transitions without
manually inferring active state from filenames, historical plans, or broad file
searches.

This is planning work for a future implementation batch. It does not replace
the existing architecture-program runner, Batch Runway, or Planning Artifact
Layout v1.

## Source Context

- GitHub issue #22: tool-owned planning state behind workflow-level commands.
- GitHub issue #8: optional SQLite operational index for runner artifacts.
- GitHub issue #10: generic phase-runner product idea.
- GitHub issue #12: phase-runner repo split and dogfooding boundary.
- Planning Artifact Layout v1 in `skills/planning-artifacts/SKILL.md`.
- Planning-state tooling ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Architecture Program Runway guidance in
  `skills/architecture-program-runway/SKILL.md`.
- Current runner state, receipt, artifact, telemetry, and input-inventory owners
  under `scripts/architecture_program_runner*.py`.
- First real active-state fixture: Graphify local planning root at
  `/home/alacasse/projects/graphify/my-docs/plans/`, where root/program
  `CURRENT.md` files are authoritative while old flat files, redirect ledgers,
  and stale pickup notes remain as compatibility context.

## Source-Of-Truth Model

Markdown and JSON remain canonical.

- Markdown stays the human and agent-readable coordination surface:
  `CURRENT.md`, `LEDGER.md`, `dispatch.md`, `runway.md`, `closeout.md`, and
  `completed-slices.md`.
- JSON state is allowed for tool-owned active state because it is explicit,
  strict, easy to validate, and easy to render back into Markdown.
- SQLite, if added, is an optional rebuildable projection for reporting and
  queries. It is not canonical storage.
- If the SQLite database is deleted, the workflow must still be understandable
  and recoverable from Markdown, JSON state, runner receipts, manifests,
  telemetry, and commits.

Agents should use commands and rendered summaries, not SQL or direct database
mutation.

## Model-Facing Command Surface

The first useful tool is intentionally small. The read-only commands are
available as direct script subcommands:

```text
python scripts/planning_state.py current --root <planning-root>
python scripts/planning_state.py validate --root <planning-root>
```

Future write commands remain planned, not implemented:

```text
planning-state create-program <slug> --title "<title>"
planning-state select-batch <program> <batch-id>
planning-state register-artifact --type <dispatch|runway|closeout|receipt|output> --path <path>
planning-state close-batch <batch-id> --status completed
planning-state render-current
planning-state render-ledger
```

The exact CLI shape can change during implementation, but the tool contract
should preserve these behaviors:

- Resolve active programs, selected batch, queued runway, latest closeout, and
  allowed next actions.
- Validate that active Markdown files and tool-owned JSON state agree.
- Later, allocate or validate canonical batch/artifact paths.
- Later, register artifacts without agents hand-editing state tables.
- Later, close a batch only when closeout evidence and required obligations are
  reconciled.
- Later, render compact Markdown views for humans and future agents.

When a planning root has Layout v1 `CURRENT.md` files, agents should run the
read-only diagnostics before broad planning tree scans or historical filename
searches. `current` reports the root/program active state and stale-context
warnings; `validate` checks the same state without mutating Markdown, JSON,
SQLite, or downstream project files.

## State Boundaries

The tool should own:

- active program registry;
- selected, queued, active, completed, blocked, and deferred batch state;
- canonical artifact paths for dispatch, runway, closeout, receipts, run
  artifacts, and generated outputs;
- cross-batch obligations with IDs, owners, and close conditions;
- latest closeout pointers and allowed next actions;
- validation that rendered `CURRENT.md` files match state.

The tool should not own:

- architecture decisions;
- finding prioritization;
- Batch Runway slice design;
- implementation code changes;
- worker/reviewer delegation;
- project-specific validation commands;
- Graphify-specific paths, cache settings, or local overlays;
- full transcripts, long logs, or prompt/session reconstruction.

## Migration Approach

Migrate active pickup safety before historical neatness.

1. Use read-only `current` and `validate` diagnostics over the Graphify
   active-state fixture and the codex-config Layout v1 plus redirect
   compatibility fixture.
2. Bootstrap tool state from existing `CURRENT.md` files and program ledgers.
3. Render `CURRENT.md` from tool state, then validate round trips.
4. Move batch selection and artifact registration behind tool commands.
5. Add cross-batch obligations and closeout evidence checks.
6. Pilot write transitions on `docs/plans/` only after the read-only Graphify
   fixture proves active-state precedence and stale-context warnings.
7. Add SQLite reporting only after state and rendering are stable.

Existing Markdown-only workflows must keep working during migration. A project
without `.planning-state/state.json` or equivalent tool state should still be
usable through current Planning Artifact Layout v1 rules.

## SQLite Projection Boundary

SQLite can help answer operational questions that are awkward to answer by
recursively scanning receipts and telemetry:

- latest run for a program;
- failed phases by reason;
- context pressure by phase;
- batch to dispatch/spec/receipt/commit-range lookup;
- pending executable batches;
- missing closeout evidence.

SQLite must be:

- optional;
- rebuildable from canonical artifacts;
- safe to delete;
- hidden behind tool/report commands;
- limited to paths, metadata, compact summaries, statuses, and hashes.

SQLite must not store canonical program ledgers, dispatch packet prose, Batch
Runway specs, closeout decisions, full prompts, long logs, or transcripts.

## Non-Goals

- Do not create a new `phase-runner` repository in this workstream.
- Do not require SQLite for active-state resolution.
- Do not expose SQL to normal agent workflows.
- Do not replace human-readable Markdown planning artifacts.
- Do not make downstream projects depend on Graphify-specific paths or
  assumptions.
- Do not implement a full orchestration runner as part of planning-state v1.
- Do not change Batch Runway execution semantics.

## Initial Success Criteria

- A fresh agent can run one command to see active program state and allowed next
  actions.
- A fresh agent can run one command to validate whether state, `CURRENT.md`,
  ledgers, batch directories, and runner artifacts agree.
- For the Graphify fixture, active state resolves from root/program
  `CURRENT.md` files and warns about stale pickup notes or historical flat files
  without treating them as selected work.
- For the codex-config fixture, active state resolves from `docs/plans/CURRENT.md`
  and old flat ledger paths are treated as redirects, not active sources.
- Batch and artifact paths are allocated or checked by code.
- Cross-batch obligations cannot disappear into old closeout prose.
- Completed batches have bounded closeout evidence indexes.
- SQLite reporting can be added later without changing the canonical contract.
