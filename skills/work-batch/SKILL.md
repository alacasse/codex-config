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
A queued runway produced by `plan-batch` is expected live state, not stale or
accidental residue.

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

## Cross-Checkout Ready/Blocked Preflight

When the queued or active runway carries a `cross-checkout-context/v1`
planning snapshot, `work-batch` owns the normal queued-to-executing transition.
Run the canonical bridge's mechanical preflight before treating the persisted
payload as a live execution lease or entering generic unexpected-movement
recovery. This lane does not apply to ordinary single-root work or to
`cross-checkout-precreation/v1` before its validated strict transition.

1. Use the Planning State Diagnostic to confirm that `current` and `validate`
   are safe to consume and that the same runway is still the only queued or
   active batch. Stop if selection or scope changed.
2. Resolve the exact queue-establishment transaction from current state: the
   canonical active-state paths plus this same batch's dispatch and runway that
   the current transaction wrote. Supply only those exact paths; do not infer a
   project-wide path taxonomy or accept a general compatible range.
3. Apply `../batch-runway/references/cross-checkout-context-v1.md` to resolve the
   installed helper, active Codex home, explicit canonical planning root, and
   immutable planning snapshot. Preserve unrelated dirty files.
4. Call `preflight_cross_checkout_live_lease(...)` with the immutable snapshot,
   explicit planning root, and exact queue-transaction paths. Proceed only when
   it returns `status: ready` and a non-null, strictly parsed `live_context`.
   Treat `status: blocked`, a null context, or helper failure as a stop before
   delegation; report the diagnostic reason without reclassifying it.
5. Validate the intended handoff paths with `validate_write_scope(...)`
   separately. `work-batch` retains every proceed, stop, recovery, delegation,
   commit, receipt, closeout, and successor decision; the helper remains
   mechanical and does not mutate planning state.

Record only compact preflight evidence: the runway path, `ready` or `blocked`
status, diagnostic reason, and the exact live context used when ready. Do not
rewrite the planning snapshot or create a separate lifecycle artifact.

## Explicit Cross-Checkout Pre-Creation Execution

When the queued or active runway explicitly names
`cross-checkout-precreation/v1`, read
`../batch-runway/references/cross-checkout-precreation-v1.md`. Revalidate the
complete payload and exact intended creation targets with the installed helper
before every applicable worker or reviewer delegation, propagate the required
mechanical context, and reject missing, null, or mismatched
`verified_cross_checkout_precreation` facts in the agent result.
For that handoff, `verified_cross_checkout_context` remains `null`.

After candidate establishment, require the helper-produced versioned transition
receipt and a green strict `cross-checkout-context/v1` payload before further
implementation. Subsequent delegations use the strict contract and must not
reinterpret pre-creation verification as strict identity;
`verified_cross_checkout_precreation` remains `null` for those strict results.

This conditional bridge authorizes no install, reload, generation switch,
execution acceptance, closeout decision, or successor selection. It adds no
step for ordinary single-root or strict cross-checkout batches.

## Explicit Strict Cross-Checkout Execution

When the queued or active runway explicitly names
`cross-checkout-context/v1` or explicitly declares separate existing toolchain,
canonical-planning, and implementation repository roots, read
`../batch-runway/references/cross-checkout-context-v1.md`. Complete the
ready/blocked preflight immediately before the first strict handoff and use only
its ready `live_context`. Immediately before every later worker and reviewer
delegation, call `prepare_cross_checkout_context_refresh(...)` again, validate
the intended write scope separately, and propagate that newly prepared exact
live execution lease, the canonical planning root, and the installed helper
path. Never pass the planning snapshot as the handoff lease. Reject missing,
null, or mismatched verified identity in the agent result and stop before
delegation on any validation failure.

After an accepted worker or reviewer action, an exact coordinator commit may
advance a repository. Before the next handoff, verify that movement against the
accepted commit and intended paths, then prepare a new lease. Repository
movement between lease preparation and handoff, or movement not explained by an
accepted coordinator action, is fail-closed unexpected movement and routes to
`../batch-runway/references/execute-recovery-v1.md`.

For each accepted action, keep an execution receipt that identifies the exact
live lease and validated scope used for that handoff. The receipt must not use
planning-snapshot revisions as though they were live action evidence.

When the runway names `cross-checkout-precreation/v1`, use the separate
pre-creation contract above until its validated transition; the pre-creation
result field cannot satisfy this strict post-creation contract.

This conditional bridge does not authorize a generation switch, install,
reload, workflow acceptance, closeout decision, or successor selection. It adds
no step for ordinary single-root batches.

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
