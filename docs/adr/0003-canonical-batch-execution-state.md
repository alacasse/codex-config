# Canonical Batch Execution State

## Status

Superseded by
[ADR 0004: Single-Generation Command-Owner Development Boundary](0004-single-generation-command-owner-development-boundary.md).

This ADR is retained as historical rationale for the rejected execution-state
direction. It is not current CCFG-26 architecture or planning authority.

## Context

CCFG-26 must transfer execution and same-batch closeout ownership to
`work-batch`. The superseded CCFG-26B plan exposed one execution state machine
through `completed-slices.md`, a batch manifest, and runner state with different
lifecycles. The existing **Run State** is scoped to one runner run, while the
required slice and attempt authority is scoped to one **Batch** and must survive
fresh coordinator processes.

## Decision

Use one canonical **Batch Execution State** JSON document, separate from
`run-state.json`, for accepted slice order, completed-prefix progression,
reservations, active attempts, resolutions, revision, and idempotency facts.
`work-batch` remains the semantic workflow owner; a deep execution-state module
validates and applies events, performs expected-state compare-and-swap, and
derives the next action. Planning State remains the only selected/queued/active
currentness owner, and Run State may point to Batch Execution State but may not
redefine it.

The state path is batch-stable under an explicitly supplied run-artifact root:

```text
<run-artifact-root>/batch-executions/<program-slug>/<batch-id>/execution-state.json
```

No latest-run search, Git fact, Markdown artifact, or per-run directory may
select a different canonical state document. Project policy or an explicit
execution input resolves the root once and every flight receives that exact
value. Bounded tests and acceptance receive an explicit absolute temporary root
allocated through the host platform's temporary-directory facility; reusable
code and planning artifacts do not hard-code `/tmp` or any other
platform-specific temporary path. This ADR does not install runtime state or
choose a machine-local literal path for codex-config.

Every mutation is serialized by an operating-system-neutral inter-process
locking implementation and an expected-state compare-and-swap: absence for
initialization, then a monotonic revision. The public module
interface exposes normalized transition outcomes, not lock backends or
platform-specific exceptions. Version 1 supports a single host with a local
filesystem on Windows, macOS, and Linux; unsupported storage or a weaker silent
fallback fails closed without writes. The lock is short-lived and never
represents an active attempt or spans an external process.

The runner launches the fresh public `work-batch` coordinator as process
lifecycle only. Inside that running coordinator, the execution-state store
reserves the exact slice and persists `in_flight` immediately before the
effectful worker launch. The runner does not make execution-acceptance or
attempt-resolution decisions. Before cutover, this real caller and the new
behavior are implemented and validated in the candidate generation. The stable
controller may orchestrate the accepted batch through its existing mechanisms,
but it does not load candidate code as its own runtime authority.

`next_action` is derived from canonical state and the accepted result. Agents do
not author it, and it is not duplicated as mutable state. Transition receipts,
manifests, and Markdown are immutable or generated projections of applied state
events.

The execution-state implementation is a deep module. Its external interface
must keep file layout, schema migration, locking, compare-and-swap, idempotency,
atomic replacement, receipt repair, and projection repair behind a small set of
typed operations. Internal classes, pure functions, and adapters are chosen for
cohesion and testability rather than minimized to force the first tracer into
one implementation slice. A future runway may use multiple semantically useful
slices when that produces a cleaner interface, independently testable behavior,
and narrower rollback boundaries.

One Execution Flight still advances at most one Slice. The first end-to-end
flight may stop deliberately to prove fresh-process recovery, but manual human
relaunch is not the accepted normal experience. Before CCFG-26 closes, an outer
execution loop inside the serialized `execute` phase must validate an
action-free typed Execution Flight Result against canonical state, consume the
code-derived `continue_same_batch` outcome, and launch the next fresh
`work-batch` coordinator automatically. The loop is bounded by the accepted
immutable slice order, stops on any ambiguous, blocked, or failed attempt, stops
at the finalization boundary, and never selects successor work. It emits one
Phase Result/receipt when the execute loop stops rather than overwriting that
phase's current single receipt path for every flight.

The run-artifact root is resolved once from explicit project policy or execution
input and propagated to every flight. A human is not asked to choose the path
between slices. Reusable workflow code still cannot invent a project-specific
default.

## Considered Options

- Extending `run-state.json` was rejected because its identity and lifecycle are
  one runner run, not one batch execution across fresh or replacement callers.
- Keeping completion in Markdown and interruption barriers in manifests was
  rejected because it creates dual authority and makes crash recovery depend on
  projections.
- Choosing `fcntl`, `msvcrt`, `filelock`, or `portalocker` in the architecture
  decision was rejected. The observable cross-platform locking contract is the
  decision; the package is a bounded implementation choice.
- A per-run batch state path was rejected because two independent runner runs
  could create two canonical states for the same batch.

## Consequences

- The first implementation milestone is a one-flight vertical tracer with the
  real runner `execute` caller and public `work-batch`. Reaching that milestone
  may require multiple semantically independent implementation slices; a
  standalone uncalled framework remains insufficient.
- The initial flight may stop for manual continuation as acceptance evidence.
  Automatic successful continuation is a separate required CCFG-26 milestone
  before normal use or CCFG-26 closeout, not an unconditional acceptance gate
  for the first implementation batch. A future plan may combine it with the
  initial tracer only when their semantic, validation, and rollback boundary is
  proven proportionate. Recovery of ambiguous in-flight attempts,
  finalization, closeout, and successor selection remain outside the initial
  tracer.
- Process-crash behavior is specified for local filesystems. Power-loss
  durability, shared/network filesystems, distributed leases, and multi-host
  fencing are not version-1 guarantees.
- The detailed state, event, crash, ownership, and validation contract is
  recorded in
  `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-contract.md`.
