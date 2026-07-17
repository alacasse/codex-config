# Cross-Checkout Pre-Creation v1 Consumer Contract

Use this temporary contract only when a selected dispatch, runway, or handoff
explicitly names `cross-checkout-precreation/v1`. It exists for the bounded
state in which stable control is present and both declared candidate roots are
absent. Do not infer pre-creation mode from cwd, missing paths, another checkout,
or a request that merely discusses future cross-checkout work.

The installed `scripts/cross_checkout_context.py` helper is the single
mechanical owner of payload parsing, stable identity and revision validation,
absent-target validation, exact creation authority, and transition receipt
data. Skills and agents consume that owner. They must not copy its validation
rules or acquire intake, selection, scope-shaping, execution-acceptance,
review-acceptance, commit, closeout, or successor authority.

Explicit pre-creation work requires Standard Execution Contract v2 and
Registered Agent Result Contract v2. Stop rather than interpret a strict
`cross-checkout-context/v1` result as pre-creation verification or use a v1
result schema.

## Stable Helper Bootstrap

For an explicit pre-creation operation:

1. Require the complete `cross-checkout-precreation/v1` payload. Stop when it
   is missing or incomplete; do not synthesize paths or identity from cwd.
2. Resolve `scripts/cross_checkout_context.py` from the active session's Codex
   home, not from cwd or an intended candidate path.
3. Before loading it, require the installed helper path to resolve exactly to
   `scripts/cross_checkout_context.py` below the payload's declared
   `stable_control.toolchain_source_root`. Require the payload's
   `stable_control.codex_home` to match the active session's Codex home. Stop on
   either mismatch.
4. Load the helper and call `parse_cross_checkout_precreation` with the complete
   payload. Treat every validation error as a blocker before planning output,
   writes, creation, or agent delegation.
5. Before a creation-bearing handoff, call
   `validate_precreation_creation_targets` with every intended creation target.
   The returned scope is mechanical evidence only; it grants no workflow
   lifecycle authority.

These bootstrap comparisons select the already-installed owner. They do not
authorize installation, reload, generation switching, path creation,
delegation, execution acceptance, closeout, or successor selection.

## Planning And Propagation

Public `plan-batch` may validate and preserve a complete pre-creation payload
while the candidate roots are absent. Planning must not
create either root. The generated runway must preserve the complete payload,
the absolute installed helper path used to validate it, and explicit
pre-creation mode without adding these fields to ordinary single-root or strict
cross-checkout runways.

Before every applicable worker or reviewer delegation while the declared roots
remain absent, the execution coordinator must resolve the installed helper
again, re-run the bootstrap validation, and include in the handoff:

- the exact pre-creation payload;
- the absolute installed helper path used for validation;
- the exact intended creation targets for a creation-bearing handoff; and
- whether the handoff is creation-bearing or read-only.

The worker and reviewer independently use the installed helper before acting
and populate their v2 `verified_cross_checkout_precreation` result field. The
coordinator rejects a missing, null, or mismatched field for an explicit
pre-creation handoff. For such a handoff,
`verified_cross_checkout_context` remains `null`. For ordinary single-root and
strict cross-checkout handoffs, `verified_cross_checkout_precreation` remains
`null` and this contract adds no step.

An explicit `cross-checkout-precreation/v1` handoff is not a strict handoff
merely because it is cross-checkout. It stays outside strict verification, with
`verified_cross_checkout_context` `null`, until the validated helper-produced
transition receipt plus green strict context required below exists.

## Mandatory Transition To Strict Context

Before delegating candidate creation, the coordinator must retain the validated
pre-creation context returned by the installed helper. Once repository and
environment establishment is reported, it must:

1. parse the complete post-creation `cross-checkout-context/v1` payload with the
   same installed helper;
2. call `build_cross_checkout_transition_receipt` with the retained validated
   pre-creation context and the validated strict context;
3. persist or propagate the exact dictionary returned by
   `cross_checkout_transition_receipt_to_dict`; and
4. require the transition receipt and strict context to remain green before any
   implementation beyond repository and environment establishment continues.

Do not re-run the absent-state parser after candidate creation and do not let a
pre-creation result satisfy a strict handoff. After the transition, subsequent
worker and reviewer handoffs follow `cross-checkout-context-v1.md`, populate
`verified_cross_checkout_context`, and leave
`verified_cross_checkout_precreation` null.

The coordinator retains all lifecycle decisions throughout planning,
pre-creation, transition, strict execution, review, commit, and closeout.
