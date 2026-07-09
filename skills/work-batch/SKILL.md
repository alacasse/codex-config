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

- Do not create ledger findings.
- Do not select a new batch.
- Do not select new ledger work.
- Do not create a new runway spec unless recovery instructions explicitly
  require replanning.
- Do not broaden slice scope beyond the active runway.
- Do not reconcile the program ledger after closeout unless explicitly asked.
- If program reconciliation remains after closeout, report it as an explicit
  post-closeout handoff instead of silently updating program state.

## Post-Closeout Handoff

`work-batch` executes the current queued or active runway and records concrete
closeout evidence. It must not reconcile the program ledger after closeout
unless the user explicitly asks for that reconciliation.

When execution completes and program reconciliation is not explicitly
authorized, the final report must include a post-closeout handoff with:

- completed batch id or runway path;
- closeout path;
- completed finding or ledger row if known;
- whether program `CURRENT.md`, program `LEDGER.md`, or batch queue metadata may
  still need reconciliation;
- the exact next user-facing request to run if reconciliation is desired;
- a statement that no new batch was selected.

The handoff must not select new work, create a dispatch, create a runway, or
scan external backlog sources.

## Agent-Facing Support

Use `../batch-runway/SKILL.md` in execute-spec mode as runtime support for the
current queued or active runway behind this command.
