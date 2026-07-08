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

This skill owns the user's request to execute the current batch. It must not
select a new batch, and it must not create a new runway unless recovery
instructions explicitly require replanning. Use `../planning-state/SKILL.md`
first when Layout v1 state is involved, then use `../batch-runway/SKILL.md` in
`execute-spec` mode for the detailed execution procedure. When routing
ambiguity exists, follow `../../docs/skill-routing-contract.md`.

During normal execution, unsupported legacy preservation is a default
implementation and review defect. Remove unsupported compatibility, or keep it
only with a named external contract, explicit user instruction, or temporary
removal condition. Use legacy and dead-surface support only for exceptional
residue investigations that the active runway or review route requires.

Before consuming Layout v1 planning state, use `../planning-state/SKILL.md` to
run the current and validate hot path. Use `../planning-artifacts/SKILL.md`
when interpreting active-state files or completed-slice archives.

## Stops

- Do not select a new batch.
- Do not create a new runway spec unless recovery instructions explicitly
  require replanning.
- Do not broaden slice scope beyond the active runway.
- Do not reconcile the program ledger after closeout unless explicitly asked.

## Agent-Facing Support

Use `../batch-runway/SKILL.md` in execute-spec mode as runtime support for the
current queued or active runway behind this command.
