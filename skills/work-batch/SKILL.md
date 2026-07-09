---
name: work-batch
description: Execute the current planned batch runway without selecting a different batch or creating a new spec.
---

# Work Batch

Use this skill when the user asks to work on the batch, execute the current
runway, or continue a queued or active batch through its implementation slices.

This skill consumes the current queued or active runway. It executes that
runway only; it does not create ledger findings, select new ledger work, or
create a new runway unless explicit recovery instructions require replanning.

This skill owns execution of the current planned batch: confirm the active or
queued runway, execute its slices under the runway contract, keep changes within
slice scope, run focused validation, and stop on blockers that make the active
batch unsafe to continue.

This skill owns the user's request to execute the current batch. It must not
select a new batch, and it must not create a new runway unless explicit
recovery instructions require replanning. Use `../planning-state/SKILL.md` first
when Layout v1 state is involved, then use `../batch-runway/SKILL.md` in
`execute-spec` mode for the detailed execution procedure. After closeout
evidence exists, use `../architecture-program-runway/SKILL.md` in
`closeout-runway` mode to reconcile same-batch program state, then stop. When
routing ambiguity exists, follow `../../docs/skill-routing-contract.md`.

During normal execution, unsupported legacy preservation is a default
implementation and review defect. Remove unsupported compatibility, or keep it
only with a named external contract, explicit user instruction, or temporary
removal condition. Use legacy and dead-surface support only for exceptional
residue investigations that the active runway or review route requires.

Before consuming Layout v1 planning state, use `../planning-state/SKILL.md` to
run the current and validate hot path. Use `../planning-artifacts/SKILL.md`
when interpreting active-state files or completed-slice archives.

## Stops

- Do not create ledger findings.
- Do not select a new batch.
- Do not select new ledger work.
- Do not create a new runway spec unless recovery instructions explicitly
  require replanning.
- Do not broaden slice scope beyond the active runway.
- Do not select, dispatch, refresh, create, or prepare successor work.
- Do not use same-batch closeout reconciliation as a reason to scan backlog
  sources or choose the next batch.
- Do reconcile the just-completed batch's program state after concrete closeout
  evidence exists.

## Same-Batch Closeout Reconciliation

`work-batch` executes the current queued or active runway and records concrete
closeout evidence. Same-batch program reconciliation is part of `work-batch`
closeout: after `batch-runway execute-spec` completes, route to
`architecture-program-runway closeout-runway` for the just-completed batch only.

The closeout reconciliation may update the relevant program `CURRENT.md`,
program `LEDGER.md`, selected dispatch state, and batch queue metadata only as
needed to reflect the completed batch's evidence. It may mark covered findings
closed, prepared, split, superseded, or still open according to the
`closeout-runway` contract.

The closeout reconciliation must not select successor work, refresh the
program queue for next selection, create a new dispatch, create a new runway,
or prepare the next batch. Successor selection remains owned by a later explicit
`plan-batch` request.

The final report must include:

- completed batch id or runway path;
- closeout path;
- same-batch program state reconciled;
- a statement that no new batch was selected.

## Agent-Facing Support

Use `../batch-runway/SKILL.md` in execute-spec mode as runtime support for the
current queued or active runway behind this command. After concrete closeout
evidence exists, use `../architecture-program-runway/SKILL.md` in
`closeout-runway` mode only for same-batch program reconciliation.
