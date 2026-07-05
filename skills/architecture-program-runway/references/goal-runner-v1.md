# Architecture Program Goal Runner v1

Use this reference when `/goal`, an automation, a local runner, or another
bounded orchestration loop should drive one or more architecture-program batches.

This protocol is a runner wrapper around `architecture-program-runway` and
`batch-runway`. It does not replace the program ledger, selected dispatch
packet, Batch Runway spec, validation evidence, review evidence, or commits as
the source of truth.

## Required Inputs

- `program_ledger`: path to the durable architecture findings ledger.
- `max_batches`: positive integer. Default to `1` if not explicitly supplied.
- `allowed_modes`: default to `select-next-batch`, `create-next-runway`,
  `closeout-runway`, and `reprioritize`.
- `execute_batches`: whether concrete Batch Runway specs may be executed.
  Default to `false` unless the user explicitly asks for implementation.

Stop instead of guessing when the program ledger path, planning location,
status vocabulary, dispatch path, expected spec path, validation profile, or
relationship to `batch-runway` is unclear.

## Goal Prompt Shape

Use a short `/goal` prompt that points at this file instead of pasting the full
protocol into the composer:

```text
/goal Use $architecture-program-runway. Follow skills/architecture-program-runway/references/goal-runner-v1.md with program_ledger=<path>, max_batches=1, and execute_batches=<false|true>.
```

For exploratory trials, prefer `max_batches=1`. Raise to `2` only after a
previous run produced clean closeout and useful goal-run evaluation telemetry.
Do not set an unbounded goal.

## Loop

For each batch until `max_batches` is reached:

1. Read applicable repo instructions and local overlays.
2. Read `program_ledger`.
3. For runner-summary, pending-batch inventory, missing closeout evidence, or
   bounded backlog/history questions, read
   `../../planning-state/references/projection-reporting.md` and use
   policy-compatible `report-projection` output before broad historical scans
   when `projection_usage` and `projection_rebuild_authority` allow it. Treat
   missing, blocked, stale, or policy-incompatible projection reports as
   explicit blockers, warnings, or fallback decisions; do not let projection
   reports select batches, replace the program ledger or selected dispatch
   packet, or close findings.
4. Read active or recently completed related runway specs only enough to know
   what is already closed, prepared, or open.
5. Check the worktree and preserve unrelated dirty files.
6. Use `select-next-batch` to choose exactly one next executable batch or
   confirm the selected dispatch packet is still ready.
7. Create or refresh the selected batch dispatch packet if it is missing,
   stale, contradicted by evidence, or too broad for a fresh spec-creation
   agent.
8. Use `create-next-runway` to create exactly one concrete Batch Runway spec
   from the selected dispatch packet.
9. If `execute_batches=false`, stop after spec creation, update runner telemetry,
   and report the next command/prompt to execute the spec.
10. If `execute_batches=true`, follow `batch-runway` in `execute-spec` mode for
   the selected spec. Keep implementation delegated to `runway_worker` and
   review delegated to `runway_reviewer`.
11. After execution, use `closeout-runway` to reconcile completed evidence into
    the program ledger.
12. Write or update one compact goal-run evaluation receipt.
13. Reassess remaining findings only enough to choose whether a next batch is
    ready. Do not start the next batch if `max_batches` has been reached.

## Completion Criteria

The runner goal is complete when one of these is true:

- `max_batches` selected batches have been created and, when `execute_batches`
  is true, executed and closed out.
- A concrete stop condition prevents safe selection, spec creation, execution,
  or closeout.
- The runner created the requested spec and `execute_batches=false`.

Completion requires a compact final report that names:

- program ledger path;
- selected batch IDs;
- created spec paths;
- executed spec paths, if any;
- commit range or commit receipts, if any;
- validation and review evidence, if any;
- stop reason;
- goal-run evaluation receipt location.

## Stop Conditions

Stop before creating or executing another batch when any condition applies:

- `max_batches` reached.
- No `Ready` or defensible next batch exists.
- Selected dispatch packet is missing, stale, too broad, or contradicted by
  current ledger/spec/commit evidence and cannot be refreshed safely.
- Existing concrete spec conflicts with the program ledger's selected batch.
- Required project values, validation profile, harness command, planning
  location, status vocabulary, output path, or summary artifact is missing.
- Worktree has unrelated dirty files that conflict with the selected batch.
- Required `runway_worker`, `runway_reviewer`, or subagent tooling is
  unavailable for an execution pass.
- Validation fails repeatedly or the required fix expands beyond the active
  slice or selected batch.
- Review finds unresolved correctness, scope, or test-quality issues.
- Permission, Docker, network, or sandbox approval remains blocked.
- The next action would change public contracts, CLI behavior, schema, report
  fields, summary fields, generated artifact shape, or installer behavior
  without explicit reclassification.
- Live context is under pressure after closeout; stop and let a fresh runner
  resume from disk artifacts.
- The user asks to pause, stop, or change scope.

## Source Of Truth

Use disk artifacts as durable state between phases and batches:

- program ledger;
- selected dispatch packet;
- concrete Batch Runway spec;
- active spec ledger and completed-slice archive;
- validation logs and summary artifacts;
- review summaries;
- commit receipts and Git history;
- goal-run evaluation receipt.

Do not rely on conversation memory, transcript summaries, or previous live
agent context as the durable source of truth.

## Goal-Run Evaluation Receipt

After the runner stops, append or update the compact receipt described in the
`architecture-program-runway` skill and `program-ledger-template.md`.

The receipt should make later tuning possible without bloating the ledger:

- Did the runner stay within `max_batches`?
- Did it use the selected dispatch packet?
- Did it avoid unbounded raw findings reloads?
- Did it preserve the `architecture-program-runway` / `batch-runway` boundary?
- Did implementation and review delegation remain unchanged?
- Were program ledger, dispatch packet, spec ledger, validation evidence, review
  evidence, and commit receipts updated consistently?
- What context-management problems or orchestration anomalies appeared?
- What should be tuned before the next runner pass?
