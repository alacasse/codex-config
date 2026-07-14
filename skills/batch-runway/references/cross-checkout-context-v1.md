# Cross-Checkout Context v1 Consumer Contract

Use this temporary contract only when a selected dispatch or runway explicitly
names `cross-checkout-context/v1` or explicitly declares separate toolchain,
canonical-planning, and implementation roots. Do not infer cross-checkout mode
from the current working directory, a dirty worktree, or the existence of
another checkout.

The mechanism is a temporary bridge with a project-owned deletion condition.
The installed `scripts/cross_checkout_context.py` helper owns parsing, root and
revision validation, generation binding, write-scope validation, generation
identity, and receipt data. Skills and agents consume that owner; they must not
copy its validation rules or acquire workflow lifecycle authority.

Explicitly cross-checkout execution requires Standard Execution Contract v2
and Registered Agent Result Contract v2 so both delegated roles can report the
verified identity. Stop rather than reinterpret a v1 result schema.

## Planning Snapshot And Live Lease

- A **planning snapshot** is the complete validated plan-time payload and
  canonical planning root persisted in the queued runway. It is durable,
  immutable historical planning evidence for the selected scope, roots,
  generation, and revisions used to create the plan. It may differ from live
  `HEAD` after the containing plan commit or later between-flight commits and
  is not a live execution lease. Never rewrite it to chase `HEAD` or to embed
  the commit that contains the runway.
- A **live execution lease** is a short-lived complete context prepared from
  live repository facts and accepted by strict context parsing. Its roots,
  revisions, generation, Codex home, mutation policy, and write scope must be
  exact for one worker or reviewer handoff. Repository movement invalidates
  the lease rather than changing the planning snapshot.
- An **execution receipt** is durable, immutable evidence of an accepted
  action. It records the exact live execution lease and scope actually used;
  it neither rewrites nor substitutes for the planning snapshot.

Before the first strict handoff, `work-batch` must confirm through Planning
State that the same runway and selected scope remain current. It supplies the
exact current batch's queue-transaction paths and calls the installed helper's
`preflight_cross_checkout_live_lease(...)` with the immutable planning snapshot
and explicit canonical planning root. The transaction paths come only from the
current planning transaction or current state and name the exact active-state,
dispatch, and runway paths written to establish this batch.

The preflight result contains only `status`, diagnostic `reason`, and
`live_context`. Proceed only on `status: ready`, whose `live_context` is a fresh
strictly parsed context. `status: blocked` has a null context and stops before
delegation; consumers must not reinterpret its reason. The helper validates
mechanical identity and exact movement only. `work-batch` retains currentness,
scope, proceed, stop, recovery, delegation, commit, receipt, closeout, and
successor authority. Validate intended write scope separately.

## Lease Renewal And Receipts

Prepare a new exact live execution lease immediately before every worker and
reviewer handoff, even when the repository revisions have not changed since the
prior handoff. If an accepted coordinator commit advanced a repository after an
accepted action, verify that exact commit and intended path set before renewal.
Movement between lease preparation and handoff, or movement not explained by an
accepted coordinator action, invalidates the lease and enters fail-closed
recovery.

Each execution receipt records the exact live lease and validated scope used
for its accepted action. Never use planning-snapshot revisions as the execution
receipt for a later action.

## Stable Helper Bootstrap

For an explicitly cross-checkout operation:

1. Require the complete context payload and an explicit canonical planning root.
   Stop if either is missing; do not infer a root from cwd.
2. Resolve `scripts/cross_checkout_context.py` from the active session's Codex
   home, not from cwd or the implementation checkout.
3. Before loading it, require that installed helper path to resolve exactly to
   `scripts/cross_checkout_context.py` below the payload's declared
   `toolchain_source_root`. Require the payload's `codex_home` to match the
   active session's Codex home. Stop on either mismatch.
4. At plan time, load that helper and call `parse_cross_checkout_context` with
   the complete payload. At `work-batch` startup, pass the historical planning
   snapshot through `preflight_cross_checkout_live_lease(...)`; do not treat the
   snapshot itself as a live lease. Before later handoffs, call
   `prepare_cross_checkout_context_refresh(...)`. Every returned live context
   must pass the unchanged strict parser. Treat every validation error or
   blocked preflight as a blocker before writes or agent delegation.
5. Before a write-bearing slice handoff, call `validate_write_scope` with the
   explicit canonical planning root and all intended planning and
   implementation paths. Candidate and stable read-only contexts must not
   declare planning writes.

These bootstrap comparisons only select the already-installed validator. They
do not replace its full validation and do not authorize an install, reload,
generation switch, write, delegation, execution acceptance, closeout, or
successor decision.

## Planning And Propagation

`create-spec` must preserve the complete validated plan-time payload and
canonical planning root in the generated runway as its planning snapshot. The
snapshot remains immutable historical evidence after the containing plan
commit or later between-flight commits advance `HEAD`; it is not a promise that
the payload remains a valid live execution lease. Do not hand-edit its
revisions, rewrite it to chase `HEAD`, or create a self-referential series of
plan commits. It must not synthesize project-specific absolute paths inside
reusable skill text.

Immediately before the first worker or reviewer delegation, the execution
coordinator must run the ready/blocked preflight and use its ready
`live_context`. Before every later delegation, call
`prepare_cross_checkout_context_refresh(...)` against the immutable planning
snapshot. Use only a newly prepared, strictly parsed context as the live
execution lease, validate the handoff's write scope separately, and include in
the handoff:

- the exact live execution lease payload, never the planning snapshot;
- the explicit canonical planning root;
- the absolute installed helper path used for validation; and
- whether the current handoff is write-bearing or read-only.

The worker and reviewer independently validate those mechanical facts before
acting and populate their v2 `verified_cross_checkout_context` result field.
The coordinator must reject a missing, null, or mismatched identity for an
explicitly cross-checkout handoff. For non-cross-checkout work, the result field
stays `null` and this contract adds no extra workflow step.

The coordinator remains the owner of selection, scope shaping, execution
acceptance, review acceptance, commits, closeout, and successor decisions.
