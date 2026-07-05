---
name: planning-state
description: Discover, validate, bootstrap, project, and report project planning state before ledger-driven skills consume it. Use when agents need to inspect active planning state, validate Layout v1 handoff files, choose safe state/projection write targets, rebuild optional reporting projections, or collect closeout evidence without scraping historical planning filenames.
---

# Planning State

Use this skill when a workflow needs a current, validated view of project
planning state before creating, executing, or closing ledger-driven work. It is
the shared interface for planning-state discovery, validation, state bootstrap,
optional projection rebuild/reporting, closeout evidence checks, and target
policy.

`scripts/planning_state.py` is the integration boundary. Invoke its commands as
a CLI. Do not import `scripts.planning_state` internals, query SQLite directly,
or scrape historical planning filenames to infer current state.

Use `../planning-artifacts/SKILL.md` for Planning Artifact Layout v1 placement,
active-state file shape, program/batch directory conventions, archive
semantics, run artifact roots, output roots, and state/projection target
policies. This skill validates and reports state; it does not redefine artifact
layout.

## Routine Hot Path

1. Read applicable repository instructions and local overlays.
2. Resolve the project planning root from explicit user direction, project
   instructions, local overlays, active specs, or documented repo-owned
   defaults.
3. If Planning Artifact Layout v1 is active, read
   `../planning-artifacts/SKILL.md` before interpreting placement or writing
   artifacts.
4. Run the read-only current-state command:

   ```bash
   python scripts/planning_state.py current --root <planning-root>
   ```

5. Run validation before consuming ledger state:

   ```bash
   python scripts/planning_state.py validate --root <planning-root>
   ```

6. Inspect the selected dispatch, queued batch, active runway, blockers, and
   next safe action reported by the commands.
7. Stop before durable writes when the project has no compatible
   `state_file_policy`, `state_file_path`, `projection_policy`,
   `projection_path`, or `update_authority` for the requested operation.

Read-only diagnostics may operate from Markdown planning roots. Durable JSON
state writes and SQLite projection writes require explicit project policy or
caller-provided temporary proof targets. Temporary proof targets must be
explicit paths supplied for the current run, not reusable defaults baked into
this skill.

## Progressive Disclosure

Read only the reference needed for the current task. Treat missing optional
reference files as unavailable guidance, not permission to invent
project-specific behavior.

- `references/state-fixtures.md`: read before creating or updating sample state
  fixtures, bootstrap examples, transition receipts, or fixture-consuming
  command examples.
- `references/target-policy.md`: read before writing JSON state, rebuilding a
  SQLite projection, choosing persistent state/projection targets, or proving
  a generated-only workflow with stdout or `/tmp`.
- `references/projection-reporting.md`: read before rebuilding projections or
  using generated projection reports.
- `references/closeout-evidence.md`: read before collecting or validating
  closeout evidence for completed batches.

## Write Boundaries

Do not write durable JSON planning state, SQLite projections, runner artifacts,
generated reports, closeout files, ledgers, `CURRENT.md`, or downstream project
planning roots unless the caller and project policy authorize the specific
target.

If target policy is missing, incompatible, or ambiguous, stop with the missing
policy value instead of selecting a location. Generic skills must not hard-code
downstream project paths, cache paths, local overlay paths, or validation
commands as defaults.

## Handoff

After `current` and `validate`, pass compact command results, selected paths,
blockers, and target-policy status to the consuming workflow. Do not pass raw
historical scans, SQL query results, or inferred state from filenames.
