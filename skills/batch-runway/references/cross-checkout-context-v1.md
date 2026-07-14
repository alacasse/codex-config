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

## Lifecycle Vocabulary

Use these four concepts throughout cross-checkout planning and execution:

- A **planning snapshot** is the complete validated plan-time payload and
  canonical planning root persisted in the queued runway. It is durable,
  immutable historical planning evidence for the selected scope, roots,
  generation, and revisions used to create the plan. It may differ from live
  `HEAD` after the containing plan commit or later between-flight commits and
  is not a live execution lease. Never rewrite it to chase `HEAD` or to embed
  the commit that contains the runway.
- **Startup reconciliation** is the workflow decision made once before
  `work-batch` consumes queued work. It compares the immutable planning
  snapshot with live repository facts, preserves the same selected scope, and
  decides whether execution may acquire a fresh live lease. It does not mutate
  the planning snapshot or grant the helper lifecycle authority.
- A **live execution lease** is a short-lived complete context prepared from
  live repository facts and accepted by strict context parsing. Its roots,
  revisions, generation, Codex home, mutation policy, and write scope must be
  exact for one worker or reviewer handoff. Repository movement invalidates
  the lease rather than changing the planning snapshot.
- An **execution receipt** is durable, immutable evidence of an accepted
  action. It records the exact live execution lease and scope actually used;
  it neither rewrites nor substitutes for the planning snapshot.

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
4. Load that helper and call `parse_cross_checkout_context` with the complete
   payload. Treat every validation error as a blocker before writes or agent
   delegation.
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

Before every worker or final-reviewer delegation, the execution coordinator
must revalidate the payload with the installed helper and include in the
handoff:

- the exact context payload;
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
