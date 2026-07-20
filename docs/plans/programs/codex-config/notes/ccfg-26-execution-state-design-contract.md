# CCFG-26 Execution-State Design Contract

> **Historical evidence.** This rejected design was superseded by
> [ADR 0004](../../../../adr/0004-single-generation-command-owner-development-boundary.md)
> and the
> [execution-state foundation supersession](../batches/ccfg-26-execution-state-foundation/superseded.md).
> Do not use it as current CCFG-26 architecture or execution authority.

## Status And Scope

Accepted initially on 2026-07-19 after the clean independent review recorded in
`ccfg-26-execution-state-design-review.md`. Amended later that day by explicit
user direction to require deep-module quality, semantically derived
implementation slices, project-resolved runtime placement, and automatic
successful continuation before normal use. The amended contract passed a fresh
clean independent review recorded in the same review artifact.

This document resolves the design questions that blocked CCFG-26 after the
unimplemented CCFG-26B runway was superseded. It is a design contract, not a
dispatch, runway, queue transition, or implementation authorization. The
program remains idle until a later explicit `plan-batch` request.

The decision is also recorded at
`docs/adr/0003-canonical-batch-execution-state.md`. That ADR owns the durable
architecture choice; this document owns the CCFG-26 state, event, crash,
ownership, compatibility, tracer, and validation detail.

## Verified Baseline

The design pass used the strict `cross-checkout-context/v1` identities below:

| Role | Root | Branch | Revision |
|---|---|---|---|
| Stable controller and canonical planning | `/home/alacasse/projects/codex-config` | `master` | `357fb5b638137233fdf966be328630625435a7d4` |
| Candidate implementation | `/home/alacasse/projects/codex-config-command-owner-redesign` | `implementation/command-owner-redesign` | `5c5ec9d52dd9033daa45f3a200031c152363b62c` |

The installed stable helper resolves to the stable checkout, and the installed
stable and candidate `work-batch` skills resolve to their respective source
roots. These are design-time observations, not a future execution lease.

Planning State reported no selected dispatch, queued batch, active runway,
blocker, or obligation. Validation passed with only the existing retired-ledger
redirect warning. Graphify was not used.

Verified implementation facts:

- stable Run State has only the serialized `select-dispatch`, `create-spec`,
  `execute`, and `closeout` phases;
- `run-state.json` is scoped to one runner run and bare `--resume` may select the
  lexically latest run-state path;
- stable JSON replacement is atomic per file through an adjacent temporary file
  and `os.replace`, but there is no cross-file transaction, fsync contract,
  execution revision, compare-and-swap, inter-process lock, slice order, active
  attempt, or completed prefix;
- current phase receipts are written and validated before the runner applies its
  phase transition; state-first execution-transition receipts are a new design,
  not an existing capability;
- the existing phase-result contract already permits
  `status=stopped`, `next_phase=stopped`, and an explicit stop reason; a stopped
  execute result leaves the active compatibility phase at `execute`, so manual
  continuation does not require a new serialized phase label;
- the live project policy has no selected `run_artifact_root`; the stable runner
  separately has a program-local per-run default;
- candidate `work-batch` still routes execution mechanics to Batch Runway and
  closeout reconciliation to Architecture Program Runway, while the latter
  explicitly forbids selected-dispatch and queue-state mutation;
- the accepted target model already assigns execution and reconciliation
  decisions to `work-batch`, planning currentness mechanics to Planning State,
  and ledger mutations to `ledger-store`;
- `planning-runway/v1` carries ordered slice IDs and a `status` presentation
  field. No live candidate production caller mutates or reads that field as
  runtime authority; runtime progression must not be inferred from it after
  Batch Execution State is initialized.

## Response Classification

| ChatGPT Pro statement | Classification | Disposition |
|---|---|---|
| CCFG-26B distributed one state machine across Markdown and manifest facts | verified repository fact | accepted |
| Stable Run State has four phases and no slice/attempt model | verified repository fact | accepted |
| A distinct batch execution document should own progression | proposed project decision | accepted by ADR 0003 |
| `work-batch` is semantic owner and code derives transitions | proposed project decision consistent with accepted target model | accepted |
| `next_action` should be code-derived | proposed project decision | accepted and strengthened: agents may not return it |
| `fcntl.flock` is sufficient | platform-specific implementation option | rejected |
| A platform-neutral lock provider is required | proposed project decision | accepted as an internal store contract |
| `filelock` or `portalocker` should be used | implementation option | deferred to bounded implementation evidence |
| State CAS precedes execution-transition receipt and projections | proposed project decision | accepted for the new execution store only; not described as current runner behavior |
| The literal run-artifact root already exists | unresolved assumption contradicted by live policy | rejected; an explicit root remains a required caller/project value |
| Planner compaction blocks the first tracer | unresolved assumption | rejected; the accepted runway already supplies the needed ordered slice facts |
| Existing slice `status` is runtime authority | unresolved assumption | rejected; it remains plan-time/presentation compatibility data |

## Decision Set

### D1. One batch execution owner

One versioned Batch Execution State document is the canonical structured owner
of intra-batch progression and attempt facts. It is physically separate from
Run State but is the only semantic execution store.

Run State owns runner invocation and compatibility-phase facts. It may contain
the exact Batch Execution State path and observation summaries, but a Run State
transition cannot complete a slice or resolve an attempt. Planning State remains
the only owner of selected, queued, and active planning currentness.

### D2. Batch-stable path contract

The canonical state path is:

```text
<run-artifact-root>/batch-executions/<program-slug>/<batch-id>/execution-state.json
```

Sibling artifacts are:

```text
execution-state.json.lock
receipts/<revision>-<event-id>.json
results/<attempt-id>.json
manifest.json
```

`run_artifact_root`, `program_slug`, and `batch_id` are explicit validated
inputs. The root is never found through globbing, latest-run discovery, Git,
chat context, or a per-run timestamp. Project policy or an explicit execution
input resolves it once for the batch, and every runner-launched or direct
`work-batch` flight receives that exact value. A human is not prompted to choose
the path between slices. Reusable workflow code may not invent a project-specific
default.

A future implementation or acceptance invocation supplies an explicit
generated-only absolute temporary root allocated through the host platform's
temporary-directory facility, or uses an authorized project policy for the
longer-lived local/external runtime root. Reusable code and planning artifacts
do not hard-code `/tmp` or any platform-specific temporary path. This design
pass does not create runtime files or choose a machine-local literal root.

The separate batch-stable namespace is intentional. Placing canonical state in
the existing per-run `batches/<batch-id>/` directory would allow two runner runs
to create two state owners for one batch.

### D3. Deep execution-state module

The external seam is a small store/transition interface. Its conceptual shape
is:

```python
apply(
    state_path: Path,
    event: BatchExecutionEvent,
    *,
    expected_state: Absent | Revision,
) -> TransitionOutcome
```

The module hides schema validation, state loading, revision checks,
idempotency, locking, pure reduction, atomic replacement, reread validation,
and projection reconciliation. Callers do not coordinate individual files or
lock primitives. External subprocess launch and agent work remain outside the
critical section and outside the pure reducer.

The locking adapter, filesystem calls, and deterministic test adapters are
internal seams. Backend-specific exceptions are normalized before returning to
`work-batch`.

This module is accepted only if it is deep: callers learn the state path, one
typed event, one tagged expected state, and one normalized transition outcome,
not the schema fields, lock backend, temporary-file protocol, receipt repair, or
projection ordering. Domain values replace growing positional parameter lists.
Pure state reduction remains separate from effectful persistence. Stateful
classes are appropriate where they encapsulate injected filesystem or locking
lifetimes; pure functions remain appropriate for deterministic transitions.
Class count is not a quality measure.

Implementation functions remain short and cohesive, errors are normalized at
the module interface, and dependencies are injected rather than discovered in
the reducer. Internal seams may support production and deterministic test
adapters without becoming new public interfaces. Tests exercise observable
behavior through the same external interface as callers and replace superseded
shallow tests instead of layering topology assertions over them.

The implementation is not required to compress this module, its persistence,
and its first real runner integration into one slice or one large file. A future
`plan-batch` derives slice count from independently useful behavior, test and
rollback boundaries. Every slice must leave a usable state through the accepted
interface and a real consumer or acceptance path; uncalled class scaffolding,
speculative ports, and horizontal file-by-file slices are insufficient.

### D4. State model version 1

The minimum canonical facts are:

```yaml
schema: batch-execution-state/v1
revision: integer
program_slug: string
batch_id: string
runway:
  path: exact path
  sha256: exact digest
  slice_order: [unique slice IDs]
initial_candidate_baseline: exact commit
completed_slices:
  - slice_id: string
    attempt_id: string
    result_sha256: exact digest
    candidate_before: exact commit
    candidate_after: exact commit
active_attempt: null | {attempt_id, slice_id, state, candidate_before, reservation_revision}
execution_status: running | blocked | failed | implementation_complete
terminal_resolution: null | {attempt_id, slice_id, outcome, result_sha256}
applied_events:
  - event_id: string
    request_sha256: exact digest
    from_revision: absent | integer
    to_revision: integer
    receipt: canonical transition receipt payload
    outcome_sha256: exact digest
```

`active_attempt.state` is only `reserved` or `in_flight`. `completed_slices`
must be a contiguous prefix of the immutable `slice_order`. The expected
candidate baseline for the next attempt is the initial baseline or the prior
completed slice's `candidate_after`. A `blocked` or `failed` resolution is
referenced by `terminal_resolution`; its immutable result does not become an
unreferenced side file. Every applied event retains the exact canonical receipt
payload needed for deterministic replay and projection. Attempt IDs are checked
against active, completed, terminal, and applied-event records before reuse.

`next_action` is deliberately absent. It is derived from canonical state and
recorded in the transition outcome/receipt for the applied revision.

### D5. Event and resolution model version 1

The first event vocabulary is:

- `initialize_execution`: exclusively creates revision 0 from one accepted
  runway path/digest, ordered unique slice IDs, and exact candidate baseline
  when `expected_state=absent`;
- `reserve_attempt`: binds one new attempt ID to the first incomplete slice;
- `authorize_launch`: changes that exact attempt from `reserved` to
  `in_flight` immediately before the coordinator launches the effectful worker;
- `resolve_attempt`: accepts exactly one immutable result for the active attempt
  with outcome `completed`, `blocked`, or `failed`.

`completed` advances the prefix by exactly one slice. `blocked` and `failed`
resolve the attempt without advancing the prefix, set the corresponding
execution status, and bind the exact terminal result reference.

For version 1:

- `interrupted` is a diagnostic for an `in_flight` attempt without an accepted
  resolution, not a resolution that authorizes relaunch;
- `replayed` is a command outcome (`applied`, `exact_replay`, or `rejected`), not
  a state;
- cancellation and recovery events are deferred to the bounded recovery
  contract;
- finalization and closeout transitions are outside the first tracer.

### D6. Result and next-action authority

Worker and reviewer agents return bounded semantic evidence. The `work-batch`
coordinator decides whether validation, review, and commit evidence are
acceptable and chooses the attempt outcome `completed`, `blocked`, or `failed`.

Across the coordinator-process seam, one flight returns a strict
`execution-flight-result/v1` observation containing only the exact batch, slice,
attempt, Batch Execution State path, resolved revision, transition-receipt path,
and coordinator status. It does not contain `next_action`. Runner code reloads
the exact state, verifies the referenced transition receipt and identities, and
derives the action through the execution-state module before deciding process
lifecycle.

```yaml
schema: execution-flight-result/v1
status: completed | blocked | failed
batch_id: string
slice_id: string
attempt_id: string
execution_state_path: exact path
resolved_revision: integer
transition_receipt_path: exact path
```

The result is closed-world and code-validated. Additional diagnostics belong in
referenced immutable evidence, not in a growing coordinator interface.

Agents do not return `next_action`. Their strict result contracts reject that
field. The reducer derives:

```text
completed + slices remain   -> continue_same_batch
completed + no slice remains -> finalize_same_batch
blocked or failed           -> require_user
reserved                    -> authorize_launch
in_flight without accepted result -> require_user
```

This removes the possibility of an enum-valid but state-invalid agent proposal.
The transition receipt freezes the derived value for that exact revision; a
current-state query may derive it again from the versioned policy.

### D7. Portable serialization, expected-state CAS, and idempotency

Version 1 supports one host with a local filesystem on Windows, macOS, and
Linux. Every mutation uses an operating-system-neutral inter-process locking
implementation and an expected-state check: absence for initialization, then a
monotonic revision. The lock is a stable companion resource, not
`execution-state.json` itself, because the JSON file is replaced.

The critical section is exactly:

```text
acquire exclusive lock
-> read and validate current state, or confirm that it is absent
-> check event ID, canonical request digest, and original expected state
   -> return exact recorded outcome when all three match
   -> reject an event-ID collision when they do not
-> for a new initialize event, require expected_state=absent and no state file
-> for any other new event, require expected_state=revision(current)
-> apply pure transition
-> atomically replace one state file
-> reread and validate
-> release lock
```

It never spans a coordinator, worker, reviewer, validation command, commit, or
other external process. The durable `active_attempt`, not lock possession,
blocks a second reservation.

The canonical request identity includes the event payload and its requested
expected state. Idempotency rules are:

```text
same event ID + same canonical request digest -> exact replay
same event ID + different digest              -> reject without write
new initialize + state already exists         -> reject without write
new non-initialize + absent state              -> reject without write
new event ID + stale expected revision         -> reject without write
```

An exact replay is checked before comparing the original expected state to the
now-current revision. It therefore returns the recorded outcome after a
successful prior transition instead of being misclassified as stale.

Initialization uses the same companion lock before `execution-state.json`
exists. The first accepted initializer creates revision 0 with
`from_revision=absent`. A concurrent initializer waits for the lock, then either
returns exact replay for the same event ID/digest/expected-absence request or
rejects because state already exists. It never overwrites an existing state.
If the initializer dies before atomic replacement, the state remains absent and
the same request may retry; if it dies after replacement, exact replay uses the
recorded initialization event and repairs its receipt.

Lock timeout, backend unavailability, unsupported storage, or an implicit
downgrade to a weaker locking mode returns a normalized fail-closed outcome
with `state_changed: false`. The public workflow never depends on `fcntl`,
`msvcrt`, platform detection, or backend-specific errors.

The concrete package is not an architectural decision. A bounded implementation
comparison may choose one only after real multi-process tests on Windows,
macOS, and Linux. Shared/network filesystems, multi-host access, distributed
leases, and fencing are unsupported without a separately accepted backend.
Power-loss durability and filesystem corruption are also outside the initial
process-crash guarantee because the current design does not add an fsync
protocol.

The accepted lock implementation must release ownership when its process dies.
A later process must be able to acquire the companion lock, read either the old
or atomically replaced valid state, and then apply the normal idempotency/CAS
rules. A backend that can leave an unrecoverable stale lock fails acceptance.

### D8. State, result, receipt, manifest, and Markdown ordering

An attempt result is written atomically to its exact immutable result path. The
store validates its identity and digest before resolving the attempt.

The state CAS records the applied event, original expected state, request
digest, resulting revision, exact canonical receipt payload, outcome digest,
and durable result reference. Completed results remain in `completed_slices`;
blocked/failed results remain in `terminal_resolution`. The
execution-transition receipt is then rendered from the canonical applied-event
record. An exact replay atomically creates a missing receipt or verifies an
existing byte-equivalent receipt. A conflicting receipt blocks.

Only after canonical state and its transition receipt agree may code refresh the
manifest or Markdown projection. Manifests are derived JSON indexes;
`completed-slices.md` is a generated human projection. Orphan results, receipts,
manifests, or Markdown never advance state.

This ordering applies to the new Batch Execution State transitions. It does not
claim that the stable runner's existing phase receipts already use this order.

### D9. Automatic successful continuation before CCFG-26 closeout

One Execution Flight remains one fresh public `work-batch` coordinator that may
advance at most one Slice. This invariant isolates agent context and external
effects; it does not require a human to start every flight.

The initial one-flight tracer deliberately maps one verified Execution Flight
Result to the existing compatible stopped Phase Result to prove that a fresh
process can resume from canonical state. That manual stop is an acceptance
milestone, not the accepted normal user experience. Before CCFG-26 is usable
normally or may close, a separate reviewed vertical milestone must add an outer
execution loop inside the serialized `execute` phase that:

1. receives the exact transition outcome from one completed flight;
2. automatically launches a new fresh `work-batch` coordinator only when the
   derived action is `continue_same_batch`;
3. passes the same exact batch identity and Batch Execution State path;
4. permits the new coordinator to reserve only the first incomplete slice under
   the normal CAS rules;
5. repeats within the finite immutable accepted slice order; and
6. stops before finalization, on `require_user`, on any blocked/failed or
   unresolved `in_flight` attempt, on an invalid/conflicting receipt, or when
   canonical state no longer matches the requested batch.

Each fresh coordinator returns an Execution Flight Result, not a full runner
Phase Result. The loop validates that result against canonical Batch Execution
State and its unique revision/event receipt. Only when the loop reaches a stop
or finalization boundary does the runner render and persist one existing Phase
Result and one phase receipt for the serialized `execute` phase. It does not
repeat or overwrite the current single execute-phase receipt path, add a new
serialized phase label, infer an action from generic `evidence_paths`, or accept
an agent-authored action.

The outer loop owns process lifecycle only. It cannot choose a slice, accept a
result, mutate queue currentness, recover an ambiguous attempt, add work to the
runway, or select a successor. If it dies after one completed flight and before
the next launch, a resumed runner derives the same `continue_same_batch` action
from canonical state and may restart the loop without repeating the completed
slice.

The temporary stable-runway policy still applies: each individual `work-batch`
invocation completes at most one implementation slice and returns before another
slice begins. Automatic continuation creates a later fresh invocation; it does
not turn one coordinator into an open-ended multi-slice agent session.

## Ownership Matrix

| Fact or action | Semantic owner | Mechanical owner | Durable representation |
|---|---|---|---|
| Accepted slice order | `plan-batch` through the accepted runway | execution initializer validates and snapshots | runway path/digest and ordered IDs in Batch Execution State |
| Permission to proceed | `work-batch` | Planning State diagnostic plus command policy | command input and receipt |
| Current slice | accepted order; `work-batch` authorizes progression but does not choose an arbitrary ID | reducer selects the first slice outside the completed prefix | derived and bound to the reservation |
| Completed prefix | `work-batch` accepts exact result evidence | reducer/store | Batch Execution State |
| Coordinator process launch | explicit runner `execute` invocation | runner | Run State observation; no attempt authority |
| Flight reservation | running public `work-batch` coordinator asks to proceed after diagnostics | store CAS | active attempt `reserved` plus receipt |
| Worker launch authorization | running `work-batch` policy | store CAS, then coordinator launches the worker | active attempt `in_flight` plus receipt/observation |
| Active attempt | no agent may redefine it | execution-state store | Batch Execution State |
| Attempt resolution | `work-batch` accepts `completed`, `blocked`, or `failed` | reducer/store | state plus immutable transition receipt |
| Worker proposal | fresh worker | strict parser/validator | immutable result evidence |
| Review acceptance | `work-batch` using independent reviewer evidence | strict parser/validator | immutable review evidence |
| Execution Flight Result | fresh `work-batch` coordinator reports exact identities and receipt reference only | runner validates against the execution-state module | strict `execution-flight-result/v1`; no next action |
| `next_action` | accepted `work-batch` policy | pure reducer derivation | transition outcome/receipt, not mutable state |
| Automatic successful continuation | derived `continue_same_batch` only; no agent chooses it | outer runner execution loop launches the next fresh `work-batch` coordinator | runner observation plus unchanged canonical Batch Execution State path |
| Manifest | no semantic owner | renderer | derived JSON index |
| Markdown projection | no semantic owner | renderer | generated human view |
| Queue currentness | explicit `plan-batch` or same-batch `work-batch` decision | Planning State | canonical Planning State artifacts |
| Finding reconciliation | `work-batch` from closeout evidence | `ledger-store` | canonical program ledger mutation |
| Finalization | `work-batch` | future execution transition | future state/receipt |
| Closeout | `work-batch` | execution-state, ledger-store, and Planning State mechanisms under their existing scopes | closeout and reconciliation receipts |
| No-successor stop | `work-batch` | no successor transition is requested | absence of successor selection |
| Later successor | later explicit `plan-batch` only | Planning State transaction | later selection/queue state |

Architecture Program Runway is not a queue-mutation or execution owner. Its
candidate contradiction is resolved by moving same-batch semantic decisions to
`work-batch`, finding mutations to `ledger-store`, and currentness transitions
to Planning State.

Batch Runway may remain temporarily available only for unmigrated scenarios.
The new tracer route must not expose or silently fall back to Batch Runway as
its public or semantic owner. Any temporary retained call must name its exact
caller, reason, future owner, and removal condition; CCFG-26 cannot close while
the target `work-batch -> Batch Runway` forbidden dependency remains.

## Crash And Concurrency Contract

| Boundary | Canonical observation | Only permitted next action |
|---|---|---|
| Before initialization | no state document | initialize under companion lock with `expected_state=absent` |
| Two initializers race | one state is created at revision 0 | same request is exact replay; different request is rejected |
| Initializer dies before replace | state remains absent | replay the same initialization request |
| Initializer dies after replace, before receipt | initialized state contains applied event | exact replay regenerates/verifies receipt |
| After initialization, before reservation | no active attempt | reserve the derived next slice at revision 0 |
| After reservation, before launch authorization | attempt is `reserved` | exact `authorize_launch` replay; no new reservation |
| After launch authorization, before spawn | attempt is `in_flight`; launch is ambiguous | fail closed for explicit recovery; no automatic relaunch |
| After spawn, before result | attempt is `in_flight` | stop for explicit recovery |
| After immutable result write, before validation | `in_flight` plus unreferenced result | validate that exact result; do not relaunch |
| After validation, before resolution CAS | `in_flight` plus valid result | replay exact resolution event with expected revision |
| After resolution CAS, before transition receipt | resolved state with applied event record | regenerate/verify receipt from canonical state |
| After receipt, before manifest/Markdown | canonical state and receipt agree | regenerate projections |
| Exact event replay | event ID and digest already applied | return the same outcome; no second external effect |
| Stale expected revision | state unchanged | reload and re-evaluate; no partial write |
| Lock timeout or unsupported backend | state unchanged | normalized fail-closed result |
| Process dies while holding the lock | old or atomically replaced state remains | a later process reacquires, validates state, then applies replay/CAS rules |
| Orphan file not referenced by state | state unchanged | report or quarantine; never infer progression |
| Second process during long external work | it can lock and read `in_flight` | reject a new reservation and release lock |

The `reserved -> in_flight` CAS occurs inside the already-running public
`work-batch` coordinator immediately before it launches the effectful worker.
This deliberately prefers an ambiguous visible attempt over a silent double
execution. The runner's earlier coordinator-process launch is process lifecycle,
not an accepted attempt or execution result.

## Incremental Implementation And First Vertical Milestones

The first CCFG-26 implementation plan must optimize for a coherent extensible
module, not for the fewest slices or the smallest apparent diff. `plan-batch`
may select one bounded batch with multiple semantic slices when the deep module,
persistence, and real caller integration have independently useful behavior or
distinct test/rollback boundaries. The first bounded batch must end in one
independently useful state through the real candidate runner/`work-batch` seam.
Automatic successful continuation remains a CCFG-26 completion requirement, but
belongs to that first batch only when planning proves that combining it with the
initial tracer has a proportionate semantic, validation, and rollback boundary.

The one-flight tracer below is the first end-to-end milestone, not a requirement
to implement every supporting responsibility in one large slice or commit. Any
earlier slice must still exercise the accepted interface through a real consumer
or executable acceptance path; source-file scaffolding alone is not vertical.

### Starting scenario

- The public tracer fixture or acceptance runway contains at least two ordered
  Slices so `continue_same_batch` can be observed. This does not impose a
  minimum Slice count on the CCFG-26 implementation runway itself.
- Planning State identifies exactly one queued runway for that scenario.
- No Batch Execution State exists for that program/batch path.
- The future runway provides an explicit generated-only run-artifact root.
- Stable/candidate roots, branches, revisions, and homes are freshly validated;
  the candidate HEAD is exact and clean.

### Public caller and behavior

At the one-flight milestone, the serialized `execute` phase remains named
`execute` and the real candidate runner caller under validation invokes one
fresh public `work-batch/v1` coordinator instead of the Batch Runway public
route. “Real caller” means the candidate implementation or its executable
runner fixture exercises the production seam. It does not authorize modifying
the stable controller to load candidate code as runtime authority before
cutover. The stable controller may orchestrate the batch only through its
existing mechanisms. The launched coordinator begins with no accepted
implementation effect and owns the later reserve/authorize decisions.

The one-flight behavior is:

1. the runner launches exactly one fresh public `work-batch` coordinator for
   the existing serialized `execute` phase;
2. the coordinator validates Planning State and initializes Batch Execution
   State from the exact accepted runway;
3. the coordinator reserves the first slice under expected-revision CAS;
4. it persists `reserved -> in_flight` immediately before launching the worker;
5. it executes exactly that slice through the existing worker, focused validation,
   independent reviewer, and commit obligations under `work-batch` ownership;
6. write and validate one immutable result;
7. resolve the exact attempt as `completed` under CAS;
8. persist completed prefix `[slice-1]` and derive
   `continue_same_batch`;
9. write/verify transition receipt and projections; and
10. return the existing compatible phase result
    `status=stopped`, `next_phase=stopped`, and
    `stop_reason=manual_continuation_required`.

The runner persists that stop while leaving its active phase at `execute`. A
later exact resume invokes a fresh `work-batch` coordinator against the same
Batch Execution State path. No new serialized phase identity is introduced.
This deliberate stop proves the seam before the required automatic-continuation
milestone replaces human relaunch in normal use.

### Independently useful result

At the first milestone, the candidate can safely execute one slice, reject a
concurrent attempt, keep an interrupted launch visible, avoid repeating a
completed slice, and hand a fresh later invocation the exact next slice without
chat history.

At the required automatic-continuation milestone, the same batch can execute
successive slices without human relaunch while still using one fresh coordinator
and one CAS-governed attempt per slice. CCFG-26 is not normally usable and cannot
close until both milestones are proven.

### Explicit exclusions

- no automatic continuation inside the initial one-flight milestone; it remains
  a separate required CCFG-26 milestone;
- no recovery or relaunch of an ambiguous `in_flight` attempt;
- no final validation/finalization flight;
- no closeout or Planning State completion transition;
- no successor selection;
- no planner/reviewer payload compaction prerequisite;
- no finite-state-machine library;
- no shared-filesystem or multi-host coordination.

### Rollback boundary

Each implementation slice must name its own interface-level usable result and
rollback boundary. Before real candidate runtime state exists, revert only the
bounded candidate commits and remove acceptance-fixture artifacts. After a real
Batch Execution State exists, code and state schema must be rolled back together;
changing a symlink alone is insufficient.

## Compatibility Disposition

- DEC-008 remains accepted. Hybrid planning artifacts are compatible because
  runtime authority moves to structured execution state rather than out of all
  Markdown.
- DEC-010 is strengthened: Batch Execution State is the single owner of each
  runtime progression fact and projections name their source revision.
- CCFG-21 through CCFG-25 planning formats remain readable and unchanged.
- Strict YAML remains acceptable for agent responses; issue #44 is not changed.
- COR-009 and CCFG-26 retain their identities and acceptance goal.
- The serialized `select-dispatch`, `create-spec`, `execute`, and `closeout`
  labels remain until CCFG-27 decides their migration/removal.
- Existing `planning-runway/v1.slices[].status` values are plan-time or
  presentation facts. They are not runtime progression authority after
  initialization. A later live caller that mutates them as runtime state would
  require explicit migration evidence rather than dual writes.
- CCFG-26B artifacts remain historical evidence and create no compatibility
  format or fallback.
- Planner compaction is not a CCFG-26 prerequisite. Any measured follow-up
  remains separate CCFG-25-related work.

## Concern Dependencies After The Tracer

These are semantic concerns, not accepted batch IDs or a promised sequence:

```text
deep execution-state module through semantically useful slices
    -> one-flight manual acceptance tracer
    -> automatic successful continuation required for normal use
    -> bounded interrupted/blocked/failed recovery
    -> final validation and finalization
    -> closeout plus ledger/Planning State reconciliation
    -> final displaced-owner narrowing
```

Automatic continuation and recovery both consume the state module but remain
separate semantics: successful continuation is required before CCFG-26 is
normally usable or closed, but it is not an unconditional gate on the first
execution-foundation batch. The first tracer and automatic continuation may be
combined only when planning proves a proportionate shared semantic, validation,
and rollback boundary. Ambiguous-attempt recovery remains a later fail-closed
concern. Finalization requires a complete prefix and no active attempt. Closeout
requires finalization evidence and idempotent partial-closeout recovery.
Legacy-owner narrowing occurs only after every supported caller has migrated.

CCFG-26C, CCFG-26D, and CCFG-26E remain unselected conceptual evidence. Their
old labels do not force the dependency graph above.

## Test Contract

Reducer tests cover initialization, duplicate slice rejection, reservation,
launch authorization, exact one-slice advancement, blocked/failed non-advance,
contiguous-prefix enforcement, identity mismatches, derived next action, and no
successor derivation.

Store tests use temporary local files and real processes for stale revision,
two concurrent initializers, two concurrent writers, exact replay, event-ID
collision, lock timeout,
exception before replace, killed lock holder followed by reacquisition, process
crash around replace, reread validation, corrupt state, path escape, and ignored
orphan results.

Fault-injection tests stop after reservation CAS, launch CAS, result write,
result validation, resolution CAS, receipt projection, and manifest projection.
Initialization tests also stop before and after the first atomic replace. Each
case starts a new process and verifies the crash table.

Public tracer tests prove exactly one coordinator, worker, reviewer, commit,
completed slice, and `continue_same_batch`; they also prove no second
coordinator, finalization, closeout, or successor. Negative tests cover wrong
slice, wrong attempt, candidate mismatch, missing exact state path, orphan
result, and a Batch Runway public fallback.

Automatic-continuation tests start from an accepted test fixture or acceptance
runway with at least two Slices and prove that the outer loop launches one fresh
coordinator per Slice without human input, never reuses coordinator context,
never overlaps attempts, validates one action-free Execution Flight Result and
unique transition receipt per flight, emits only one final execute Phase
Result/receipt, and stops at the finalization boundary after the finite accepted
Slice order. The fixture requirement does not constrain the number of Slices in
the CCFG-26 implementation runway.
They also prove fail-closed stop on blocked/failed results, unresolved
`in_flight` state, receipt conflict, state-path mismatch, and loop-process crash
between completed flights; no case may recover an ambiguous attempt or select a
successor.

Real multi-process locking tests run on `ubuntu-latest`, `macos-latest`, and
`windows-latest`. A platform/backend matrix is observable acceptance, not an
OS-specific implementation embedded in the contract. Property-based transition
tests may follow after the reducer stabilizes; neither Hypothesis nor an FSM
package is a first-tracer prerequisite.

## Formal Design Gate

The design questions are resolved as follows:

- [x] canonical runtime owner: Batch Execution State store;
- [x] queue/currentness owner: Planning State only;
- [x] bounded v1 state and event models;
- [x] compare-to-absence initialization, expected-revision CAS, idempotency, and
  process-crash rules;
- [x] state/receipt/manifest/Markdown derivation without dual authority;
- [x] code-derived `next_action` with no agent-authored field;
- [x] deep-module quality and semantic-slice rules prevent a forced monolithic
      tracer or uncalled horizontal scaffolding;
- [x] one real runner caller and independently useful one-flight result;
- [x] manual relaunch limited to the first acceptance milestone and automatic
      successful continuation required before normal use or CCFG-26 closeout;
- [x] recovery, finalization, and closeout remain separate from the first tracer;
- [x] CCFG-21 through CCFG-25 and CCFG-27 compatibility preserved;
- [x] old CCFG-26C/D/E sequence reshaped as unselected concerns;
- [x] temporary stable-runway dogfooding policy applied;
- [x] no successor selected.
- [x] fresh clean independent review of the user-directed amendment.

Operational execution still requires a fresh strict cross-checkout lease and an
exact run-artifact root resolved once from project policy or explicit execution
input. Those are per-run inputs, not open architecture decisions. A later
explicit `plan-batch` may select the first bounded CCFG-26 execution-foundation
batch, whose slice count follows semantic interface, behavior, test, and rollback
boundaries and whose outcome is independently useful through the real candidate
runner/`work-batch` seam. Automatic continuation belongs to that batch only when
planning proves the combined boundary proportionate. This design pass does not
select it.

## Evidence

- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/notes/ccfg-26-replan-analysis-and-chatgpt-pro-handoff.md`
- `docs/plans/programs/codex-config/findings/ccfg-26-execution-state-authority-direction.md`
- `docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md`
- `scripts/architecture_program_runner_state.py`
- `scripts/architecture_program_runner_transition.py`
- `scripts/architecture_program_runner_validation.py`
- candidate `skills/work-batch/SKILL.md`
- candidate `skills/architecture-program-runway/SKILL.md`
- candidate `skills/batch-runway/SKILL.md`
- candidate `schemas/planning-runway-v1.schema.json`
- candidate `docs/design/command-owner-redesign/02-target-ownership-model.md`
- candidate `docs/design/command-owner-redesign/decisions.md`
- candidate `docs/design/command-owner-redesign/07-implementation-ledger-intake.md`
