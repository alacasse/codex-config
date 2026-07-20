# 0004: Single-Generation Command-Owner Development Boundary

## Status

Accepted.

## Context

During the command-owner redesign, the stable checkout holds canonical planning
and coordinates implementation work performed in a separate candidate checkout.
That development topology must not be interpreted as two product runtimes that
cooperate to execute a batch.

This decision applies to CCFG-18 through CCFG-29 until final integration removes
the split checkout topology.

## Decision

Use the following development model:

```text
stable master checkout
  - canonical planning and handoff documents
  - stable workflow used to coordinate development
  - exact identity and write-scope verification
                    |
                    | implementation edits
                    v
candidate checkout
  - target source code
  - target tests and validation
  - candidate implementation commits
```

The vertical arrow represents development work performed against another
checkout. It is not a runtime protocol.

The governing rules are:

1. One real batch is controlled by one toolchain generation.
2. Stable and candidate do not import, invoke, synchronize with, or share
   runtime execution state with one another.
3. The temporary cross-checkout bridge owns repository identity, revision,
   generation, Codex-home, and write-scope validation only.
4. Stable dogfooding records and explicit human relaunches are development
   bookkeeping. They are not candidate product behavior.
5. CCFG-26 does not assume a new canonical Batch Execution State. New durable
   state requires a concrete product behavior that existing state and receipts
   cannot satisfy, plus a separate approved design decision.
6. The v1 environment is a normal user-controlled local filesystem. Ordinary
   validation, concurrency, crash consistency, and atomicity may be required by
   an actual implementation seam. Resistance to a hostile same-user process
   performing late namespace substitution is not an implicit requirement.

Cross-checkout validation is therefore a development integrity boundary, not a
product runtime interface. A batch that builds a future controller remains
controlled by the stable mechanism until cutover. The controller under
construction does not control its own implementation batch.

## Consequences

- Exact repository identity, revision, generation, Codex-home, and write-scope
  checks remain required development safeguards.
- Stable planning artifacts, receipts, and Git evidence may coordinate later
  explicit development invocations without creating candidate runtime state or
  cross-generation communication.
- New product runtime state or filesystem guarantees require demonstrated
  product behavior and a separate approved decision; the split development
  topology does not justify them by itself.
- Final integration may remove this temporary topology. Until then, candidate
  code can implement and validate the future controller but cannot control the
  batch that is building it.
