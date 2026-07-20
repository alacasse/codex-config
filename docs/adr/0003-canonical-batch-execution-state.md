# Canonical Batch Execution State

## Status

Superseded on 2026-07-19 by
`0004-extraction-first-batch-local-execution.md`.

This ADR is retained as historical evidence for the execution-state approach
that produced the superseded `ccfg-26-execution-state-foundation` plan. It is not
live authority for future CCFG-26 planning or implementation.

## Historical Decision

The original decision introduced a batch-stable JSON execution state separate
from `run-state.json`, a separate caller-supplied run-artifact root, revision CAS,
idempotency, portable inter-process locking, transition receipts, and a one-flight
`work-batch` tracer.

That direction correctly identified several useful ideas:

- runtime progression should have one structured owner;
- accidental concurrent writers must be serialized;
- stale writes and exact replay require explicit handling;
- agents should not author `next_action`;
- process crashes must leave readable state.

The original decision also made three assumptions that are no longer accepted:

1. batch-specific runtime state required a separate `run_artifact_root` rather
   than living with the batch;
2. codex-config's stable/candidate installation topology could shape the product
   design and bootstrap path;
3. version 1 needed protection against hostile same-user filesystem namespace
   substitution at the final system-call boundary.

Those assumptions expanded the plan into a storage-security and dogfooding
architecture that was disproportionate to the intended extractable local tool.
The resulting Slice 1 remained uncommitted and was rejected in final review.

## Current Authority

Future work must use:

- ADR 0004 for the product, storage, dogfood, portability, threat-model, and
  feasibility boundaries;
- `docs/plans/programs/codex-config/findings/ccfg-26-product-dogfood-reset.md`
  for the CCFG-26 reset and preserved-worktree disposition;
- the original COR-009 user outcome for execution and same-batch closeout goals.

The original full ADR text remains available in Git history and through the
superseded planning evidence. It must not be copied into a replacement runway as
an implementation requirement.
