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

## Startup Classifications And Controlled Paths

`work-batch` owns startup reconciliation and must classify repository movement
as exactly one of these three values, with no fourth or implicit fallback:

- `expected-queue-establishment` means revisions are unchanged. If revisions
  advanced, it accepts movement only when the sole advanced repository is the
  canonical planning repository, every changed path is a canonical active-state
  path or the same batch's dispatch or runway, while Planning State Diagnostic
  still reports that runway as the only queued or active batch.
- `compatible-between-flight-change` means every intervening commit and changed
  path was reviewed and none overlaps or changes a controlled owner, replaces
  selected scope, or invalidates a declared baseline.
- `conflicting-between-flight-change` means controlled overlap, repository root
  or branch drift, generation identity drift, a dirty-file conflict, an
  invalidated baseline, or evidence that cannot be classified confidently.
  Unknown evidence uses this classification and stops before delegation.

Derive controlled paths from the current Planning State Diagnostic and planning
layout, the queued runway and same batch's dispatch, the source finding and
source note, the runway's acceptance contract, the manifest and its declared
owners, the resolved installed helper owner, declared roots and baselines, and
pending slice allowlists. Do not hard-code project paths, commands, cache
locations, issue names, or planning layout in reusable workflow text.

Accepted startup movement must route through the installed helper's
`prepare_cross_checkout_context_refresh(...)` operation. The helper returns
planned and live revision facts plus a strictly parsed refreshed payload; it
does not classify or accept movement. Validate the intended write scope
separately. Accepted startup movement is normal execution evidence, not an
orchestration anomaly.

## Lease Renewal And Execution Receipts

Prepare a new exact live execution lease immediately before every worker and
reviewer handoff, even when the repository revisions have not changed since the
prior handoff. If an accepted coordinator commit advanced a repository after an
accepted action, verify that exact commit and intended path set before renewal.
Movement between lease preparation and handoff, or movement not explained by an
accepted coordinator action, invalidates the lease and enters fail-closed
recovery.

Startup evidence records the runway path, classification, planned and accepted
live stable and implementation revisions, reviewed commit ranges, and
changed-path basis. Each execution receipt records the exact live lease and
validated scope used for its accepted action. Never use planning-snapshot
revisions as the execution receipt for a later action.

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
4. At plan time or for a live execution lease, load that helper and call
   `parse_cross_checkout_context` with the complete payload. At
   `work-batch` startup, do not strict-parse the historical planning snapshot
   before reconciliation. After `work-batch` accepts movement, call
   `prepare_cross_checkout_context_refresh(...)`; its refreshed payload must
   pass the unchanged strict parser. Treat every applicable validation error as
   a blocker before writes or agent delegation.
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

Before every worker or reviewer delegation, the execution coordinator must
revalidate the payload with the installed helper by calling
`prepare_cross_checkout_context_refresh(...)` against the immutable planning
snapshot. It must use the helper's strictly parsed refreshed payload as the
new live execution lease, validate the handoff's write scope separately, and
include in the handoff:

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
