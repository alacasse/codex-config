---
name: work-batch
description: Execute the current planned batch runway without selecting a different batch or creating a new spec.
---

# Work Batch

Use this skill when the user asks to work on the batch, execute the current
runway, or continue a queued or active batch through its implementation slices.

This skill owns execution of the current planned batch: confirm the active or
queued runway, execute its slices under the runway contract, keep changes within
slice scope, run focused validation, and stop on blockers that make the active
batch unsafe to continue.

Before consuming Layout v1 planning state, use `../planning-state/SKILL.md` to
run the current and validate hot path. Use `../planning-artifacts/SKILL.md`
when interpreting active-state files or completed-slice archives.

## Stops

- Do not select a new batch.
- Do not create a new runway spec unless recovery instructions explicitly
  require replanning.
- Do not broaden slice scope beyond the active runway.
- Do not reconcile the program ledger after closeout unless explicitly asked.

## Copy-First Bridge

Until this command has a fully separate execution procedure, use
`../batch-runway/SKILL.md` in execute-spec mode for the current queued or active
runway.
