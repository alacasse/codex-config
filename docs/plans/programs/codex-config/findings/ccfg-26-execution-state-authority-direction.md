# CCFG-26 Execution-State Authority Direction

## Status

Accepted direction amendment for CCFG-26, dated 2026-07-19. This is planning
direction only. It preserves CCFG-26 and COR-009, supersedes the unimplemented
CCFG-26B runway, clears its queue entry, and selects no successor.

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

## Decisions Still Required

Before a new CCFG-26 runway is planned, formalize:

- the physical execution-state location and its relationship to `run-state.json`,
  batch manifests, immutable receipts, and the currently unset run-artifact root;
- the event and terminal-resolution model for reserved, completed, blocked,
  failed, interrupted, and replayed attempts;
- whether `next_action` is entirely code-derived or an agent proposal validated
  and normalized by code;
- revision, compare-and-swap, lease, idempotency, and crash-boundary semantics;
- the exact ownership matrix for slice order, completed prefix, active attempt,
  queue currentness, receipts, manifests, and Markdown projections;
- the smallest end-to-end first tracer and its rollback boundary;
- whether the conceptual CCFG-26C, CCFG-26D, and CCFG-26E sequence remains useful
  after the new state seam is accepted;
- whether compact planner payloads and code-rendered planning artifacts are a
  prerequisite for CCFG-26 or a separate CCFG-25 follow-up.

## Planning Gate

Use `../notes/ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md` to process the
next ChatGPT Pro response and verify every proposal against the live stable and
candidate implementations. Do not invoke `plan-batch` or `work-batch` for
CCFG-26 until the decisions above are recorded in a reviewed, implementation-
ready project artifact. A later explicit `plan-batch` request may then select
exactly one bounded batch.
