# CCFG-26 Execution-State Authority Direction

> **Historical evidence.** This rejected direction was superseded by
> [ADR 0004](../../../../adr/0004-single-generation-command-owner-development-boundary.md)
> and the
> [execution-state foundation supersession](../batches/ccfg-26-execution-state-foundation/superseded.md).
> Do not use it to select, queue, or execute CCFG-26 work.

## Status

Accepted direction and formal design resolution for CCFG-26, dated 2026-07-19.
This is design-only evidence. It preserves CCFG-26 and COR-009, supersedes the
unimplemented CCFG-26B runway, clears its queue entry, and selects no successor.

## Accepted Direction

- CCFG-26 must establish one canonical structured owner for intra-batch
  execution progression, attempts, interruption visibility, and deterministic
  continuation.
- Agents produce bounded semantic decisions. Strict YAML remains acceptable for
  agent responses; changing YAML to JSON is not an objective by itself.
- Code parses and validates agent decisions, derives mechanical facts, applies
  state transitions, persists runtime state and receipts, and renders durable
  human-facing artifacts.
- Durable runtime state and process receipts use structured JSON. Markdown may
  explain or project state but must not become runtime transition authority.
- Planning State remains the sole owner of canonical selected, queued, and
  active currentness. The execution-state owner must not create a second queue.
- Public `work-batch` retains semantic execution ownership. A deep runner or
  execution-state module may own deterministic transition mechanics without
  becoming a second public command owner.
- The next implementation plan must be a smallest useful vertical tracer through
  the new seam. A standalone uncalled kernel is insufficient unless its first
  consumer and behavior proof are in the same bounded batch.
- Implementation quality is a first-class acceptance concern. The execution
  owner must be a deep module with a small typed interface, cohesive functions,
  injected effectful dependencies, interface-level tests, and internal seams
  that do not leak filesystem, lock, schema, or receipt mechanics to callers.
  `plan-batch` may use multiple semantic slices rather than forcing the module
  and its real integration into one rushed monolithic change.

## Formal Design Resolution

The design gate is resolved by:

- `../notes/ccfg-26-execution-state-design-contract.md`;
- `../notes/ccfg-26-execution-state-design-review.md`;
- `../../../../adr/0003-canonical-batch-execution-state.md`; and
- the canonical execution vocabulary in root `CONTEXT.md`.

The accepted decisions are:

- one batch-stable JSON execution state, separate from run-scoped Run State;
- `work-batch` semantic ownership, a deep transition/store mechanical owner,
  `ledger-store` finding mutation, and Planning State currentness mutation;
- compare-to-absence initialization, revision CAS, idempotency, short portable
  inter-process serialization, and fail-closed process-crash behavior;
- `reserved` / `in_flight` attempts with exactly one completed, blocked, or
  failed resolution in version 1;
- code-derived `next_action`, canonical execution-transition receipts, derived
  manifests, and generated Markdown;
- an explicit batch-stable path below a project-policy or execution-input
  run-artifact root resolved once and propagated across flights, never latest-run
  discovery or a per-slice human prompt;
- one manual-continuation acceptance tracer through the real runner `execute`
  caller and public `work-batch`, followed by automatic successful continuation
  as a separately reviewed required CCFG-26 milestone before normal use or
  closeout;
- one fresh coordinator and at most one Slice per Execution Flight, with an outer
  process-lifecycle loop validating a strict action-free Execution Flight Result,
  deriving `continue_same_batch` from canonical state, and stopping on ambiguity,
  blocked/failed state, or the finalization boundary;
- recovery, finalization, closeout, and successor selection remain outside the
  first tracer;
- no planner-compaction prerequisite and no runtime authority for
  `planning-runway/v1.slices[].status`.

Operational execution must still refresh strict identities and resolve the exact
run-artifact root once from authorized project policy or explicit execution
input. A bounded generated-only implementation or acceptance invocation supplies
an explicit absolute temporary root allocated through the host platform's
temporary-directory facility. Reusable code and planning artifacts do not
hard-code `/tmp` or any platform-specific temporary path. Normal longer-lived
use requires an authorized local/external project policy. Concrete lock-library
selection is a bounded implementation choice tested on Windows, macOS, and
Linux, not an open design decision.

## Planning Gate

The amended design gate is satisfied after a fresh clean independent review.
Keep the program idle and do not invoke `work-batch`. Only a later explicit
`plan-batch` request may select the first bounded CCFG-26 execution-foundation
batch. It must end in one independently useful state through the real candidate
runner/`work-batch` seam. Automatic continuation remains a CCFG-26 completion
requirement, but belongs to this first batch only if planning proves that its
semantic, validation, and rollback boundary is proportionate. The planner must
derive the slice count from those boundaries, refresh strict identities, resolve
the exact runtime root from authorized policy or execution input, queue exactly
one batch, and stop before implementation. This design pass selected no batch.
