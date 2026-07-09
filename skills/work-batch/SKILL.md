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

This skill owns execution intent for the current planned batch: confirm the
active or queued runway, route execution through the runway contract, and stop
on blockers that make the active batch unsafe to continue.

This skill owns the user's request to execute the current batch. It must not
select a new batch, and it must not create a new runway unless explicit
recovery instructions require replanning. Use `../planning-state/SKILL.md` for
current/validate diagnostics, `../planning-artifacts/SKILL.md` for Layout v1
artifact vocabulary, and `../batch-runway/SKILL.md` in `execute-spec` mode for
execution mechanics. After closeout evidence exists, use
`../architecture-program-runway/SKILL.md` in `closeout-runway` mode to reconcile
same-batch program state, then stop. When routing ambiguity exists, follow
`../../docs/skill-routing-contract.md`.

During normal execution, unsupported legacy preservation is a default
implementation and review defect. Remove unsupported compatibility, or keep it
only with a named external contract, explicit user instruction, or temporary
removal condition. Use legacy and dead-surface support only for exceptional
residue investigations that the active runway or review route requires.

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
closeout evidence. After `batch-runway execute-spec` completes, route to
`architecture-program-runway closeout-runway` for the just-completed batch only.

Same-batch program reconciliation requires concrete execution closeout evidence.
If no execution closeout exists, preserve the queued runway unless the user
explicitly asks to cancel or abandon it, or a documented blocker makes execution
unsafe.

`architecture-program-runway closeout-runway` owns the mechanics for updating
program `CURRENT.md`, program `LEDGER.md`, selected dispatch state, batch queue
metadata, and covered-finding lifecycle status. `work-batch` owns the stop: the
closeout reconciliation must not select successor work, refresh the queue for
next selection, create a new dispatch, create a new runway, or prepare the next
batch.

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
