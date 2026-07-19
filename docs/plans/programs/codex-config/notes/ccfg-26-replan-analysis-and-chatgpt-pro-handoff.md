# CCFG-26 Replan Analysis and ChatGPT Pro Handoff

## Purpose

This is the durable record and planning handoff for the completed CCFG-26
design pass. It captures the verified repository facts, the useful conclusions from the
ChatGPT Pro discussion, corrections to that discussion, the target ownership
direction, the questions sent to ChatGPT Pro, and their verified formal
disposition before another CCFG-26 batch is planned.

It is deliberately not a dispatch, runway, batch selection, or authorization to
implement. A fresh agent should be able to begin here without reconstructing the
preceding chat or treating the superseded CCFG-26B bundle as current direction.

## Canonical State After This Amendment

- Parent finding: CCFG-26 / COR-009, still open and now `Ready` for a later
  explicit `plan-batch`; the formal design gate is satisfied.
- Queued batch: `None`.
- Selected dispatch: `None`.
- Active runway: `None`.
- Active execution: `None`.
- Superseded before implementation:
  `batches/ccfg-26b-fresh-slice-flight/`.
- Latest closeout remains:
  `batches/ccfg-26-slice-shape-policy-correction/closeout.md`.
- CCFG-26C, CCFG-26D, and CCFG-26E remain unselected conceptual evidence only;
  they are not a promised successor chain.
- No successor was selected by this amendment.
- Post-amendment `planning_state.py current` reports selected dispatch, queued
  batch, and active runway all as `None`; `planning_state.py validate` passes
  with no errors, blockers, or obligations. Its only warning is the pre-existing
  retired-ledger redirect warning.

## Verified Checkout Baseline

The following identities were observed immediately before this amendment on
2026-07-19:

| Role | Root | Branch | Revision |
|---|---|---|---|
| Canonical planning and stable controller | `/home/alacasse/projects/codex-config` | `master` | `b604134564594e8eeb4f265206c044d06e9d2a77` |
| Candidate implementation | `/home/alacasse/projects/codex-config-command-owner-redesign` | `implementation/command-owner-redesign` | `5c5ec9d52dd9033daa45f3a200031c152363b62c` |
| Stable Codex home | `/home/alacasse/.codex` | stable generation | resolved by the strict cross-checkout contract |
| Candidate Codex home | `/home/alacasse/.codex-command-owner-redesign` | candidate generation | resolved by the strict cross-checkout contract |

These revisions are a pickup baseline, not a permanent lease. Every later
design, planning, or implementation pass must re-run Planning State diagnostics
and re-resolve the strict stable/candidate identities before drawing current
conclusions. Canonical planning comes from the stable checkout; target behavior
comes from the candidate checkout. Graphify remains suspended for this work.

## Why CCFG-26B Was Superseded

CCFG-26B was reviewed and queued but never implemented. Its directory contained
nine planning and review artifacts totaling 3,692 lines:

| Artifact | Lines | Role |
|---|---:|---|
| `dispatch.md` | 197 | initial bounded selection |
| `runway.md` | 973 | initial execution plan |
| `review.md` | 129 | initial independent review |
| `amendment.md` | 978 | two-slice correction |
| `amendment-review.md` | 257 | amendment review and corrections |
| `progression-authority-correction.md` | 394 | positive completion authority |
| `progression-authority-review.md` | 127 | correction review |
| `progression-attempt-barrier-correction.md` | 523 | unresolved-attempt barrier |
| `progression-attempt-barrier-review.md` | 114 | barrier review |

The growth exposed an architectural seam problem rather than merely excessive
prose:

1. The original plan and amendment still could not let a fresh process
   determine completed slices, the next slice, or an invalid progression.
2. A correction therefore made `completed-slices.md` the mutable positive
   completion authority, with a strict embedded grammar.
3. That still could not distinguish a never-started slice from a launched but
   interrupted attempt.
4. A second correction therefore added a negative attempt barrier in
   `batch-manifest.json.execute_flights`, written before the subprocess launch.
5. The plan simultaneously prohibited a new execution store or lifecycle state.
   One state machine was consequently distributed across two artifacts with
   different roles and update moments.

This is the central reason to stop. Adding another amendment would continue
encoding execution mechanics in immutable planning prose rather than giving
those mechanics one executable owner.

The two planned implementation slices were also too broad for architectural
discovery. Each combined ownership transfer, runner calling, validation,
transition, receipt, manifest, routing, fixture, and test changes. They were
vertical in scenario shape, but not small enough to isolate and validate the new
state seam safely.

## Verified Current Architecture

### Stable runner

The production runner has useful foundations:

- durable JSON `run-state.json`;
- atomic temporary-write plus `os.replace` persistence;
- structured phase receipts;
- deterministic validation and transition code;
- fresh phase subprocess boundaries.

Its persistent lifecycle currently knows only four global phases:

1. `select-dispatch`;
2. `create-spec`;
3. `execute`;
4. `closeout`.

It does not yet model a slice order, reserved flight, active attempt, attempt
resolution, completed prefix, or execution `next_action`. Atomic replacement is
present, but an explicit execution-state revision/CAS contract for these new
concepts has not yet been designed.

### Candidate ownership

The candidate public `work-batch` skill expresses execution intent but still
routes important mechanics to Batch Runway and closeout reconciliation to
Architecture Program Runway. The candidate contracts also contain a boundary
contradiction that must be resolved formally:

- `work-batch` says Architecture Program Runway owns update mechanics for
  `CURRENT.md`, `LEDGER.md`, selection, and queue fields;
- Architecture Program Runway says it does not mutate selected dispatch or queue
  state.

Planning State must remain the sole mechanical currentness owner. CCFG-26 should
clarify the semantic caller and the mechanical transition API instead of moving
queue authority to another skill.

### Planner and reviewer representation

The candidate planner and reviewer use strict YAML responses. The problem is not
YAML itself. They are asked to return and review large, nearly complete planning
objects, including facts the code already knows or can derive. Python then
duplicates field lists and validates those full artifacts.

The useful representation rule is:

```text
agent -> compact strict YAML decision -> parsed Python object
      -> deterministic validation and derivation
      -> JSON runtime state and receipts
      -> code-rendered Markdown/YAML planning artifacts
```

Strict JSON would be appropriate where the runtime provides schema-constrained
Structured Outputs, but replacing an equally large YAML payload with JSON would
not solve the token or ownership problem.

## Conclusions Accepted From the ChatGPT Pro Discussion

### Preserve

- Keep `add-to-ledger`, `plan-batch`, and `work-batch` as the three public
  semantic command owners.
- Keep Planning State as the sole owner of canonical selected, queued, and active
  currentness, with deterministic mechanics rather than semantic selection.
- Keep stable/candidate isolation and strict explicit roots and revisions.
- Keep fresh subprocesses, separate worker/reviewer roles, structured receipts,
  atomic persistence, idempotency, and the no-successor-at-closeout invariant.
- Preserve CCFG-26 and COR-009. The failed object is the queued CCFG-26B plan,
  not the goal of transferring execution and closeout ownership.
- Do not rebuild or mass-rebase the candidate branch as a response to this
  planning failure.
- Do not add a finite-state-machine library now. The hard problems are durable
  reservation, persistence, CAS, idempotency, crash recovery, receipts, and
  ownership. A small pure Python reducer plus explicit store is easier to audit.
- Property-based state-machine tests may become useful after the state and event
  model exists, especially for reserve/crash/replay/accept sequences.

### Change

- Give intra-batch progression and attempts one canonical structured runtime
  owner.
- Have agents return bounded semantic choices rather than full rendered
  dispatches, runways, state machines, or repeated mechanical context.
- Let code derive paths, identities, revisions, digests, boilerplate, allowed
  transitions, continuation, and rendered planning artifacts.
- Keep runtime state and receipts in JSON; keep Markdown explanatory or
  projective, never authoritative for runtime transitions.
- Begin the next implementation with the smallest independently useful
  end-to-end behavior through this seam.

## Corrections and Qualifications

The following suggestions from the initial ChatGPT Pro answer are not accepted
as project decisions:

- YAML does not need to be replaced by JSON for agent responses. Issue #44 may
  remain unchanged. Payload size and responsibility are the problem.
- DEC-008 does not automatically need immediate supersession. Python already
  renders some planning contracts, and existing hybrid artifacts may remain
  compatible while runtime authority moves out of Markdown. Any decision change
  must be based on the actual live ADR and callers.
- DEC-010 should remain: each machine fact needs one canonical structured owner.
- A compact planner-decision interface may be valuable, but it may belong to a
  CCFG-25 follow-up rather than the critical path for CCFG-26. The dependency
  must be proven before scheduling it.
- The physical state file is unresolved. Extending the existing
  `run-state.json` may avoid a cross-store transaction; a separate batch
  execution state may make the module deeper. Do not choose from naming alone.
- A standalone state-kernel batch may recreate horizontal preparation work. The
  first accepted batch needs a real caller and observable vertical behavior, or
  an explicit reason why the preparatory state is independently useful.
- The existing CCFG-26C/D/E labels describe useful concerns, not an accepted
  future batch map. Their boundaries and order must be revisited after the state
  model is decided.
- Creating a new topic branch, tag, or branch hierarchy is not authorized or
  required by the current strict topology. Preserve the existing candidate
  branch unless a later explicit Git decision says otherwise.

## Formal Disposition Of The ChatGPT Pro Response

The response was processed on 2026-07-19 against stable
`357fb5b638137233fdf966be328630625435a7d4` and candidate
`5c5ec9d52dd9033daa45f3a200031c152363b62c`. The strict
`cross-checkout-context/v1` helper accepted those roots and revisions, both
worktrees were clean, and Planning State remained valid and idle.

The formal decision set is recorded in:

- `ccfg-26-execution-state-design-contract.md` for the full CCFG-26 ownership,
  state/event, crash, path, tracer, compatibility, and test contracts;
- `ccfg-26-execution-state-design-review.md` for the clean independent review;
- `../../../../adr/0003-canonical-batch-execution-state.md` for the durable
  architecture decision;
- root `CONTEXT.md` for the canonical vocabulary.

The following conclusions are now project decisions rather than open questions:

- one batch-stable `Batch Execution State` document owns intra-batch slice and
  attempt progression; it is separate from run-scoped Run State;
- `work-batch` owns semantic execution decisions, the execution-state module
  owns deterministic transitions, `ledger-store` applies finding mutations,
  and Planning State alone applies queue/currentness transitions;
- accepted slice order is snapshotted from the exact runway; completed-prefix,
  active-attempt, revision, and idempotency facts are canonical JSON;
- `next_action` is derived by code, excluded from agent result contracts, and
  recorded only in transition outcomes/receipts;
- attempts are `reserved` or `in_flight` until exactly one `completed`,
  `blocked`, or `failed` resolution; interruption is initially a diagnostic for
  an unresolved `in_flight` attempt;
- initialization uses compare-to-absence and later mutations use
  expected-revision CAS under one short, platform-neutral inter-process
  serialization contract on a single host/local filesystem;
- Windows, macOS, and Linux are required observable platforms. No `fcntl`,
  `msvcrt`, concrete lock package, or silent weak fallback is part of the public
  contract;
- execution receipts, manifests, and Markdown are projections of canonical
  applied events and cannot advance state;
- the execution-state owner is a deep module with a small typed interface;
  implementation may span multiple semantic slices rather than compressing
  state, persistence, locking, and real integration into one monolithic change;
- the first acceptance tracer executes exactly one slice through public
  `work-batch` and returns the existing compatible stopped phase result with
  `manual_continuation_required` to prove fresh-process resumption;
- manual human relaunch is not the accepted normal experience. A separately
  reviewed automatic-successful-continuation milestone must launch one fresh
  coordinator per remaining slice before CCFG-26 is normally usable or may
  close, while recovery, finalization, closeout, and successor selection remain
  separate;
- each coordinator returns an action-free typed Execution Flight Result. The
  runner validates its exact state/receipt reference and derives continuation;
  the serialized `execute` phase still emits only one final Phase Result/receipt
  when its internal flight loop stops;
- planner compaction is not a CCFG-26 prerequisite, and
  `planning-runway/v1.slices[].status` is plan-time/presentation compatibility
  data rather than a live runtime owner.

The live-code verification also corrected three overstatements in the response:

1. the stable runner's current phase receipt is written before its phase-state
   transition; state-first execution-transition receipts are a new CCFG-26
   contract only;
2. the project currently has no selected `run_artifact_root`; the design fixes a
   deterministic batch-stable path beneath an explicitly provided root but does
   not pretend a machine-local literal already exists; and
3. process-crash behavior on a single-host local filesystem is in scope, while
   power-loss durability, shared/network filesystems, distributed leases, and
   multi-host fencing are not version-1 guarantees.

Concrete lock-library selection and the exact generated-only runtime root used
by a future acceptance run remain bounded implementation/operation inputs, not
architecture questions. Project policy or explicit execution input resolves the
root once and propagates it across flights; a human is not prompted between
slices, and a reusable skill may not guess a project-specific default.

## User-Directed Quality And Continuation Amendment

After reviewing the human-readable consequences of the accepted design, the
user made two additional decisions on 2026-07-19:

1. prefer more implementation effort when it produces clean extensible code,
   cohesive classes/functions, few parameters, and an interface that can grow;
   allow multiple semantic slices rather than forcing a rushed one-slice module;
2. reject manual per-slice relaunch as the normal user experience. Preserve one
   fresh coordinator per flight internally, but require automatic successful
   same-batch continuation before CCFG-26 is normally usable or may close.

The design contract and ADR incorporate those decisions. The one-flight manual
stop remains a bounded acceptance milestone because it proves durable
fresh-process resumption. It is not the target steady-state workflow. Exact
class count, source filenames, and lock package remain implementation choices;
the reviewed interface, behavior, testability, and rollback properties are the
acceptance surface.

## Pre-Response Working Ownership Model

This table is retained as the working model that produced the questions. The
canonical resolved matrix is now in
`ccfg-26-execution-state-design-contract.md`; `decision required` below records
former uncertainty and is not a current blocker.

| Fact or action | Semantic owner | Mechanical owner | Durable representation |
|---|---|---|---|
| Finding selection and batch shape | `plan-batch` | planning transaction code | compact agent decision plus rendered planning artifacts |
| Selected, queued, active currentness | calling public workflow | Planning State | canonical Layout v1 state |
| Slice order for one accepted runway | accepted plan | plan renderer / execution initializer | decision required: immutable execution-state input or referenced runway fact |
| Flight reservation | `work-batch` policy | execution-state transition module | canonical JSON state plus immutable receipt/index |
| Active attempt | accepted execution event | execution-state store | canonical JSON state |
| Worker result proposal | fresh worker agent | strict result parser/validator | bounded structured response, then immutable JSON receipt |
| Review acceptance | independent reviewer | strict review parser/validator | immutable structured receipt |
| Completed-slice prefix | accepted flight result | execution-state reducer | canonical JSON state; Markdown only as projection |
| Next action | `work-batch` policy | decision required: derived or proposal-plus-validation | canonical JSON state/result |
| Runner process launch | accepted reservation | runner/orchestrator | observation and receipt paths |
| Batch manifest | no semantic authority beyond its contract | artifact/index renderer | derived JSON index |
| Closeout intent | `work-batch` | closeout transition and Planning State APIs | receipts plus canonical Planning State reconciliation |
| Successor selection | later explicit `plan-batch` only | Planning State transaction | never part of CCFG-26 closeout |

The desired module is deep: callers should ask for a small set of operations and
receive validated outcomes, rather than coordinating file formats and partial
state themselves. A working hypothesis is a pure transition core such as:

```python
transition(
    state: BatchExecutionState,
    event: BatchExecutionEvent,
    *,
    expected_revision: int,
) -> TransitionOutcome
```

The store would separately perform compare-and-swap persistence and immutable
receipt writes. External process effects remain outside the reducer. This is a
design hypothesis, not yet an approved interface.

One concrete option raised in the discussion, preserved here for evaluation
rather than acceptance, is a state object containing:

- schema/interface version and monotonic revision;
- batch ID and immutable runway revision;
- current stage and accepted slice order;
- completed slice IDs as a contiguous prefix;
- at most one active attempt with attempt ID, kind, slice ID, and candidate
  baseline;
- a validated or code-derived `next_action`.

The minimal proposed event vocabulary was `reserve_flight`,
`accept_flight_result`, `record_blocked_result`, and `record_failed_result`.
Under that option, canonical execution state is authoritative, flight-result
receipts are immutable, the batch manifest is a derived index, and
`completed-slices.md` is a generated human projection. The formal design
selected a separate batch-stable execution state, treats interruption as an
unresolved `in_flight` diagnostic in version 1, and defers cancellation and
reviewed recovery events.

## Compatibility Decisions Reconciled

| Surface | Current disposition |
|---|---|
| DEC-010 single structured authority | Preserve; it directly supports one execution-state owner. |
| DEC-008 hybrid active artifacts | Preserve. Runtime JSON is a separate operational category, so compatible rendered planning artifacts need no amendment. |
| GitHub issue #44 YAML validation | Preserve. Strict YAML agent responses remain acceptable. |
| GitHub issues #48 and #50 representation exploration | No change in this pass. Compact decisions remain useful follow-up evidence, not a CCFG-26 prerequisite. |
| GitHub issue #61 / CCFG-26 execution transfer | Preserve the goal and acceptance; replace the superseded CCFG-26B implementation path. |
| GitHub issues #59 and #60 | Preserve their permanent candidate behaviors and verify exact requirements before planning. |
| CCFG-26C/D/E candidate rows | Preserve as unselected concerns; the old labels no longer define a promised sequence. |
| Git branch topology | Preserve strict stable/candidate topology; no mass rebase, reconstruction, tag, or topic branch is authorized by this amendment. |

## Accepted Minimum State Invariants

The formal design contract accepts these invariants:

1. At most one unresolved attempt exists for a batch.
2. A launch requires a durable reservation written before the external effect.
3. No new reservation is allowed while a prior attempt is unresolved.
4. Completed slices form a contiguous prefix of the accepted slice order.
5. A result must name and match the exact reserved attempt, slice, runway
   revision, candidate baseline, and expected state revision.
6. Exact replay is idempotent; reuse of an attempt ID with different content is
   rejected.
7. A stale expected revision is rejected without partial writes.
8. An interruption remains durably visible after process loss.
9. `blocked` and `failed` do not automatically relaunch unless a later reviewed
   recovery contract explicitly authorizes it.
10. Queue currentness is never reconstructed from execution-state files.
11. Runtime continuation is never inferred from Markdown or Git topology.
12. No closeout transition selects a successor.
13. Initialization exclusively creates revision 0 under a companion lock and
    compare-to-absence; concurrent initialization cannot overwrite state.
14. Every mutation is serialized through a platform-neutral inter-process
    locking implementation and expected-state check.
15. Lock ownership is never durable execution state and never spans an external
    effect.
16. Version 1 supports a single host with a local filesystem on Windows, macOS,
    and Linux; shared/network filesystems require a separately accepted backend.
17. One Execution Flight advances at most one Slice, but a code-owned outer loop
    automatically starts later fresh flights on `continue_same_batch` before
    CCFG-26 is considered normally usable.
18. Automatic successful continuation never implies automatic recovery,
    finalization, closeout, queue mutation, or successor selection.

## Questions Sent To ChatGPT Pro

These questions are retained as provenance for the response disposition above.
Their accepted answers are canonical only through the linked design contract,
not through the original external response.

### 1. Smallest vertical tracer

What is the smallest end-to-end behavior that proves the new seam without
building recovery, automatic continuation, finalization, and closeout at once?
It must name the starting scenario, public caller, state transition, one external
effect boundary, durable result, focused validation, rollback boundary, and why
the result is independently useful.

### 2. Exact ownership matrix

Who semantically chooses and who mechanically owns each of: accepted slice
order, current slice, completed prefix, flight reservation, active attempt,
attempt resolution, `next_action`, immutable receipts, manifest projection,
queue currentness, finalization, closeout, and no-successor reconciliation?

### 3. One store or two

Should intra-batch execution state extend the runner's existing `run-state.json`
or live in a separate batch execution-state document? Compare both against:

- atomicity across reservation and phase transition;
- restart lookup and the currently unset run-artifact root;
- coupling between global runner phases and batch execution;
- schema/version evolution;
- reuse by `work-batch` outside this runner;
- risk of a cross-store transaction or duplicated currentness.

Conclude with a recommended owner and path contract, not merely a filename.

### 4. Crash and recovery table

Define observable state and permitted next action after crashes:

- before reservation;
- after reservation but before subprocess launch;
- after launch but before any result;
- after result write but before validation;
- after validation but before state CAS;
- after state CAS but before receipt/index projection;
- during exact replay;
- with a stale revision;
- with an orphan file not referenced by canonical state.

### 5. Result and `next_action` authority

Which fields must an agent decide, which may it propose, and which must code
derive? In particular, should the agent return `next_action`, should code derive
it entirely, or should code validate and normalize an agent proposal? Show how
an invalid but schema-valid proposal is rejected.

### 6. Attempt resolution model

What are the minimal states/events for reserved, launched, completed, blocked,
failed, interrupted, cancelled, and replayed work? Which distinctions are
necessary now, which should be deferred, and what durable evidence resolves an
attempt exactly once?

### 7. CAS and concurrency boundary

What revision or lease is checked at reservation and acceptance? Is one active
writer assumed, and if so, how is accidental parallel invocation rejected?
Specify idempotency keys and the ordering of state and receipt writes.

### 8. Run-artifact placement

Planning State currently reports no run-artifact root. What project-local or
runner-provided root should own runtime execution artifacts, how is it discovered
without globbing or chat context, and what is the bootstrap path for the first
run?

### 9. Planner compaction dependency

Does the first execution-state tracer actually require compact planner/reviewer
payloads and code-rendered artifacts, or can it consume an already accepted
runway contract? Identify the concrete blocking caller or schema. If no blocker
exists, treat planner compaction as a separate CCFG-25 follow-up.

### 10. Compatibility and decisions

Can the design preserve the delivered CCFG-21 through CCFG-25 planning formats,
DEC-010, issue #44 YAML validation, COR-009 identity, historical artifacts, and
the serialized identities reserved for CCFG-27? Include COR-009's old-format
active-state policy, partial-closeout recovery, and absence of dependencies on
legacy Batch Runway paths. Identify any actual decision or contract that must
change and cite its live caller.

### 11. CCFG-26C/D/E disposition

After choosing the state seam, which concerns remain separate semantic
boundaries: bounded recovery, automatic continuation, final validation,
finalization, closeout, reconciliation, and legacy-owner narrowing? Do not force
the old B/C/D/E sequence; derive dependencies from independently useful states.

### 12. Test strategy

Which deterministic unit, integration, crash-injection, and property-based tests
provide enough confidence for the first tracer? State which tests protect public
behavior and which merely test the reducer. Do not make a new FSM dependency a
prerequisite.

## Protocol Used To Process The Response

The response was processed with this protocol:

1. Run `python scripts/planning_state.py current --root docs/plans` and
   `python scripts/planning_state.py validate --root docs/plans`.
2. Confirm the program is idle and CCFG-26 is design-blocked at pickup; stop if
   a batch was selected, queued, or activated unexpectedly. After the accepted
   contract and clean review, reconcile the row to `Ready` without queueing.
3. Resolve the exact stable and candidate roots, branches, revisions, and Codex
   homes through the strict cross-checkout evidence. Read canonical planning only
   from stable and target behavior only from candidate.
4. Read this analysis, the short direction amendment, COR-009, the temporary
   dogfooding policy, CCFG-26A closeout, the slice-shape correction, and the
   superseded CCFG-26B evidence needed for the claim being evaluated.
5. Classify every ChatGPT Pro statement as one of:
   - verified repository fact;
   - proposed project decision;
   - implementation option;
   - unresolved assumption.
6. Verify repository-fact claims against live code or active contracts. Do not
   accept a design choice merely because it sounds plausible.
7. Build one contradiction-free ownership matrix and one state/crash model.
   Record rejected alternatives and why.
8. Reconcile the candidate `work-batch` / Architecture Program Runway boundary
   with Planning State currentness ownership.
9. Produce a reviewed formal design artifact or ADR-sized decision set. Update
   this note only with links and final dispositions; do not layer another runway
   amendment onto CCFG-26B.
10. Keep CCFG-26 idle until the user explicitly requests `plan-batch`. That later
    invocation selects exactly one bounded vertical batch and stops before
    implementation.

## Formal Decision Gate Before Planning

The response disposition satisfies this design gate. A future `plan-batch` must
still refresh live identities and provide the exact runtime root it intends to
use:

- [x] One canonical runtime execution-state owner is named.
- [x] Planning State remains the sole queue/currentness owner.
- [x] The state and event schemas or equivalent contracts are bounded.
- [x] Reservation, CAS, idempotency, and process-crash behavior are explicit.
- [x] The state/receipt/manifest/projection relationship has no dual authority.
- [x] `next_action` authorship and validation are explicit.
- [x] Deep-module quality and semantic-slice rules prevent a forced monolithic
      implementation or uncalled horizontal scaffolding.
- [x] The first batch has one real caller and one independently useful vertical
      result.
- [x] Manual relaunch is limited to the first acceptance milestone; automatic
      successful continuation is required before normal use or CCFG-26 closeout.
- [x] The first batch does not silently absorb recovery, finalization, and
      closeout.
- [x] Stable/candidate roots and exact revisions were freshly verified for this
      design pass; execution must refresh them again.
- [x] Existing CCFG-21 through CCFG-25 contracts and reserved CCFG-27 identities
      are preserved or formally amended with live-caller evidence.
- [x] CCFG-26C/D/E have been preserved and reshaped as unselected concerns.
- [x] The temporary stable-runway dogfooding policy is applied.
- [x] No successor is selected as part of design or closeout.
- [x] The user-directed amendment has a fresh clean independent review.

## Conceptual Dependency Direction

This is a reasoning order, not an accepted batch list:

```text
formal execution-state decision
    -> deep module through semantically useful slices
    -> one manually stopped vertical acceptance tracer
    -> fresh automatic continuation required for normal use
    -> bounded recovery semantics
    -> final validation and finalization
    -> closeout and same-batch Planning State reconciliation
    -> displaced-owner narrowing and later CCFG-27 cutover preparation
```

Semantic boundaries should determine the eventual slice and batch count. If a
later design proves two adjacent steps form one small independently useful
vertical result, they may be combined; if one step contains distinct rollback
or validation boundaries, it should be split.

## Recommended Agent Tools and Skills

- Use `planning-state` first for live-state pickup and validation.
- Use `codebase-design` when comparing the execution-state module boundary and
  deciding how deep its interface should be.
- Use `domain-modeling` when fixing the vocabulary for batch, slice, flight,
  attempt, reservation, result, resolution, continuation, finalization, and
  closeout.
- Use `design-an-interface` or a bounded `prototype` only after the ownership and
  crash questions are narrow enough to compare concrete alternatives.
- Use `plan-batch` only after the formal decision gate passes and the user
  explicitly requests selection. Use `work-batch` only after one new runway is
  queued.

Graphify is explicitly suspended for the command-owner redesign and must not be
used for this work.

## Evidence Index

Canonical live state and policy:

- `../CURRENT.md`
- `../LEDGER.md`
- `stable-runway-dogfooding-policy.md`
- `ccfg-26-execution-state-design-contract.md`
- `ccfg-26-execution-state-design-review.md`
- `../../../../adr/0003-canonical-batch-execution-state.md`
- `../findings/ccfg-26-execution-state-authority-direction.md`
- `../findings/command-owner-redesign-planning-execution-carry-forward.md`

Completed predecessors and corrections:

- `../batches/ccfg-26a-permanent-vertical-runway-contract/closeout.md`
- `../batches/ccfg-26-slice-shape-policy-correction/closeout.md`
- `../batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`

Superseded planning evidence:

- `../batches/ccfg-26b-fresh-slice-flight/superseded.md`
- `../batches/ccfg-26b-fresh-slice-flight/dispatch.md`
- `../batches/ccfg-26b-fresh-slice-flight/runway.md`
- `../batches/ccfg-26b-fresh-slice-flight/amendment.md`
- `../batches/ccfg-26b-fresh-slice-flight/progression-authority-correction.md`
- `../batches/ccfg-26b-fresh-slice-flight/progression-attempt-barrier-correction.md`

Stable runner implementation:

- `../../../../../scripts/architecture_program_runner_state.py`
- `../../../../../scripts/architecture_program_runner_transition.py`
- `../../../../../scripts/architecture_program_runner_validation.py`
- `../../../../../scripts/architecture_program_runner_phase_contract.py`

Candidate implementation surfaces to inspect at the freshly resolved candidate
revision:

- `skills/work-batch/SKILL.md`
- `skills/architecture-program-runway/SKILL.md`
- `scripts/plan_batch.py`
- planner and reviewer agent contracts and their schemas.

Accepted redesign identity:

- COR-009 in the immutable redesign snapshot linked from `../LEDGER.md`.
- GitHub issues #59, #60, #61, and #66 as referenced by the active ledger and
  findings. Local repo-owned planning artifacts remain the pickup authority.

## Stop Conditions

- Stop if any agent treats CCFG-26B as queued, executable, resumable, or the
  mandatory predecessor of CCFG-26C.
- Stop if a new correction or amendment is added to the CCFG-26B runway.
- Stop if a design gives runtime transition authority to Markdown, Git state, or
  filesystem globbing.
- Stop if execution state becomes a second owner of selected/queued/active
  Planning State currentness.
- Stop if a new state document duplicates facts without a single writer,
  transition protocol, and derived-projection rule.
- Stop if candidate behavior is inferred from stable code, or canonical planning
  is inferred from candidate-local copies.
- Stop if the first implementation batch is only an uncalled framework without
  an independently useful consumer behavior.
- Stop if planning selects a successor before a later explicit `plan-batch`
  request.
