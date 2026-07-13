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

`create-spec` must preserve the complete validated payload and canonical
planning root in the generated runway. It must not synthesize project-specific
absolute paths inside reusable skill text.

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
