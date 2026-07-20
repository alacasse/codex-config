# CCFG-26 Master Authority Recovery Plan

## Status And Authority

- Status: approved recovery direction; implementation has not started.
- Artifact type: durable supporting plan. This file is not a selected dispatch,
  queued Batch Runway, runway amendment, or execution authority.
- Immediate execution scope: authoritative `master` planning and instruction
  surfaces only.
- Candidate scope: read-only verification only. Do not edit, install, commit, or
  clean the candidate checkout while executing this recovery plan.
- Queue boundary: do not use `plan-batch` and do not queue a replacement CCFG-26
  runway during the master-authority recovery. Fresh CCFG-26 planning is a
  separate follow-on invocation after this plan's acceptance criteria pass.
- User decision: the stable checkout coordinates development and the candidate
  checkout is the implementation target; they are not cooperating runtimes.

## Verified Starting Point

The plan was written against these observed identities:

```yaml
stable:
  root: /home/alacasse/projects/codex-config
  branch: master
  revision: 4a168e9181e2e66ad1bce4ec7a83fc3575842e12
  worktree: clean
candidate:
  root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  revision: 5c5ec9d52dd9033daa45f3a200031c152363b62c
  worktree: clean
```

Planning State `current` and `validate` pass. The current queue still points to:

```text
docs/plans/programs/codex-config/batches/
  ccfg-26-execution-state-foundation/runway.md
```

The current next safe action incorrectly requires a cross-platform anchored
filesystem mechanism and Windows validation. Revalidate all identities and
Planning State before making changes; do not assume the revisions above remain
current.

## Problem To Correct

Master currently turns a development-checkout arrangement into an apparent
two-runtime product architecture:

1. Stable planning coordinates work performed in a separate candidate checkout.
2. Active CCFG-26 documents describe the stable controller and candidate caller
   as if they must cooperate at runtime.
3. Development progress across explicit agent invocations is promoted into a
   new canonical Batch Execution State product.
4. An independent review adds a hostile namespace-substitution threat model.
5. `CURRENT.md` and `LEDGER.md` elevate that review conclusion into the next
   mandatory implementation action.

This sends every compliant fresh agent toward shared status JSON, interprocess
coordination, symlink/TOCTOU hardening, and POSIX/Win32 filesystem backends even
though COR-009 only requires transferring execution and closeout ownership to
`work-batch`.

## Correct Operating Model

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

## Desired End State

After this recovery plan:

- the rejected execution-state foundation is unambiguously superseded;
- CCFG-26 remains open and is ready for fresh planning;
- no selected dispatch, queued batch, or active runway exists;
- Planning State directs the next agent to plan CCFG-26 from COR-009 and the
  actual candidate implementation seam;
- active authority contains the single-generation development boundary;
- execution-state and adversarial-filesystem material remains available only as
  historical evidence;
- the candidate checkout remains unchanged; and
- CCFG-27 through CCFG-29 remain unselected and blocked by their existing
  dependency order.

## Work Package 1: Establish The Boundary Decision

### Goal

Create one concise architectural authority that says what stable/candidate
separation means and, equally importantly, what it does not mean.

### Write Scope

- `docs/adr/0004-single-generation-command-owner-development-boundary.md` (new)
- `AGENTS.md`
- `docs/plans/programs/codex-config/notes/stable-runway-dogfooding-policy.md`

### Required Changes

1. Add ADR 0004 with the operating model and six governing rules above.
2. State that the decision applies to CCFG-18 through CCFG-29 until final
   integration removes the split checkout topology.
3. State explicitly that cross-checkout validation is a development integrity
   boundary, not a product runtime interface.
4. State that a batch building a future controller remains controlled by the
   stable mechanism until cutover; the controller under construction does not
   control its own implementation batch.
5. Add the same negative runtime boundary, in compact form, to the command-owner
   topology section of `AGENTS.md` so it is read before planning or coding.
6. Clarify in the dogfooding policy that one-Slice-per-invocation progress uses
   existing planning and Git evidence. It adds no candidate runtime state and no
   stable/candidate communication.

### Non-Goals

- Do not redesign `work-batch`.
- Do not choose a replacement persistence model.
- Do not weaken exact repository identity or write-scope validation.
- Do not change the candidate checkout.
- Do not queue CCFG-26.

### Commit

```text
docs(ccfg-26): establish the single-generation development boundary
```

## Work Package 2: Retire The Misleading Active Authority

### Goal

Remove the rejected execution-state foundation from the live pickup path while
preserving its documents as historical evidence.

### Write Scope

- `docs/adr/0003-canonical-batch-execution-state.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/superseded.md` (new)
- `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-contract.md`
- `docs/plans/programs/codex-config/notes/ccfg-26-execution-state-design-review.md`
- `docs/plans/programs/codex-config/findings/ccfg-26-execution-state-authority-direction.md`
- root `docs/plans/CURRENT.md` only if its compact active-program handoff must
  change to remain consistent with the program `CURRENT.md`

### Required Changes

1. Mark ADR 0003 superseded by ADR 0004. Preserve its body as historical
   rationale; do not silently rewrite it into the new decision.
2. Add `superseded.md` recording:
   - the user-directed cancellation;
   - the category error described in this plan;
   - the exact stable and candidate revisions observed at cancellation;
   - that no candidate implementation from the rejected foundation is retained;
   - that the runway, amendment, reviews, report, and retrospective are
     historical and must not be executed, resumed, amended, or used to infer
     current queue state; and
   - that no replacement runway is selected by the supersession.
3. Add compact historical-status banners to the execution-state design contract,
   its review, and the execution-state authority direction. Point to ADR 0004
   and `superseded.md`.
4. In program `CURRENT.md`:
   - set queued batch to `None`;
   - keep selected dispatch and active runway at `None`;
   - remove the anchored-filesystem, namespace-substitution, Win32, and
     candidate-WIP preservation instructions;
   - describe CCFG-26 as ready for a fresh planning-only invocation;
   - make the next safe action `plan-batch CCFG-26` from COR-009, ADR 0004, and
     current candidate code; and
   - prohibit implementation or successor selection until that fresh runway is
     independently reviewed and queued.
5. In `LEDGER.md`:
   - keep parent CCFG-26 open;
   - change the execution-state foundation batch from `blocked` to
     `superseded`;
   - replace its filesystem blocker with the supersession reason;
   - stop listing ADR 0003 and the execution-state design as active CCFG-26
     architectural authority;
   - retain links to the failed attempt as historical evidence; and
   - keep CCFG-27 through CCFG-29 waiting on CCFG-26.
6. Do not move historical files during this correction. Active-state links and
   explicit status are sufficient; physical archive migration can be separate
   cleanup if later desired.

### Commit

```text
docs(ccfg-26): retire the execution-state foundation runway
```

## Work Package 3: Remove Canonical Vocabulary And Add Regression Guards

### Goal

Prevent future agents and reviewers from recreating the same product architecture
from canonical vocabulary or live pickup output.

### Write Scope

- `CONTEXT.md`
- `tests/test_stable_runway_dogfooding_policy.py`
- `tests/test_ccfg_26_development_boundary.py` (new, preferred)
- documentation changed by a test only when needed to express the intended
  semantic contract

### Required Changes

1. Remove the following from canonical domain vocabulary and relationships:
   - Execution Flight;
   - Execution Attempt;
   - Flight Reservation;
   - Attempt Resolution;
   - Completed Slice Prefix as a Batch Execution State concept;
   - Batch Execution State;
   - Execution Transition Receipt;
   - Execution Flight Result;
   - Execution Next Action; and
   - Automatic Same-Batch Continuation.
2. Do not replace them with a second speculative vocabulary. Retain established
   `Batch`, `Slice`, Planning State, Run State, Phase Result, receipts, and
   command-owner terms already supported by live behavior.
3. Extend the dogfooding policy test to protect the explicit absence of candidate
   runtime state and cross-generation communication.
4. Add one focused project-policy regression test that reads active authority
   rather than scanning all history. It must prove:
   - program `CURRENT.md` has no selected dispatch, queued batch, or active
     runway after recovery;
   - the next safe action names fresh CCFG-26 planning from COR-009 and does not
     authorize implementation;
   - ADR 0004 and `AGENTS.md` state the single-generation/no-runtime-bridge
     boundary;
   - the execution-state foundation is marked superseded in the ledger and its
     `superseded.md` exists;
   - ADR 0003 is superseded; and
   - active CCFG-26 instructions do not require Batch Execution State,
     automatic continuation, anchored filesystem, namespace substitution, or a
     Win32/NT backend.
5. Limit negative-term assertions to active authority and the new boundary
   contract. Historical reports and superseded documents are allowed to retain
   the rejected terminology.

### Commit

```text
test(ccfg-26): guard the development and runtime boundary
```

## Validation For The Master-Authority Recovery

Run from the stable checkout after all three work packages:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/planning_state.py current --root docs/plans
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/planning_state.py validate --root docs/plans
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_stable_runway_dogfooding_policy.py tests/test_ccfg_26_development_boundary.py
git diff --check
git status --short
```

Read the `current` output. Do not treat a zero exit code alone as sufficient.
It must report:

```yaml
selected_dispatch: None
queued_batch: None
active_runway: None
```

Its next safe action must direct a later agent to fresh CCFG-26 planning. It must
not direct implementation, execution-state repair, filesystem mechanism
selection, candidate-WIP preservation, CCFG-26B resumption, or successor work.

Verify the candidate remained unchanged:

```bash
git -C /home/alacasse/projects/codex-config-command-owner-redesign branch --show-current
git -C /home/alacasse/projects/codex-config-command-owner-redesign rev-parse HEAD
git -C /home/alacasse/projects/codex-config-command-owner-redesign status --short
```

The expected branch is `implementation/command-owner-redesign`. The final
revision may differ from the starting revision only if the user separately
authorized candidate work; otherwise stop and report the unexpected movement.

## Master-Authority Recovery Acceptance Criteria

- ADR 0004 is accepted and states the complete development/runtime boundary.
- ADR 0003 and the execution-state design artifacts are explicitly historical.
- The execution-state foundation has a durable supersession record.
- Planning State `current` and `validate` pass.
- Selected dispatch, queued batch, and active runway are all `None`.
- CCFG-26 is open and ready for fresh planning, not implementation.
- No active next action contains the rejected filesystem or shared-state work.
- Canonical vocabulary no longer presents the rejected runtime model as an
  established domain fact.
- The focused policy regression tests pass.
- The candidate checkout has no changes caused by this recovery.
- No successor has been selected.

## Stop Conditions

Stop the recovery and report instead of improvising if:

- stable or candidate roots, branches, revisions, or worktree status contradict
  the verified cross-checkout identities;
- another selected, queued, or active batch appears;
- existing uncommitted stable changes overlap the declared write scope;
- removing the queue would abandon an implementation commit or other candidate
  work not represented in the clean starting point;
- a proposed correction retains the old runway plus another amendment instead
  of superseding it;
- the correction invents another shared status document, launcher, symlink
  engine, filesystem backend, or cross-generation protocol;
- CCFG-27 cutover or CCFG-29 integration work enters the scope;
- a test requires deleting or rewriting historical evidence merely because it
  contains superseded vocabulary; or
- Graphify is invoked or its output is treated as authority.

## Follow-On: Fresh CCFG-26 Planning

Fresh planning is a separate invocation after the master-authority recovery is
committed and accepted.

### Entry Preconditions

- all recovery acceptance criteria above pass;
- Planning State has an empty queue;
- stable and candidate identities are freshly verified;
- candidate code is inspected directly at its current revision; and
- the agent reads the temporary stable-runway dogfooding policy.

### Source Hierarchy

Use, in this order:

1. COR-009 in
   `findings/command-owner-redesign-implementation-intake.md`;
2. ADR 0004;
3. current candidate `work-batch`, runner, recovery, receipt, validation,
   finalization, and closeout behavior;
4. the stable-runway dogfooding policy; and
5. narrow historical evidence only when a concrete behavior question remains.

Do not use ADR 0003, the execution-state design, or either superseded CCFG-26
runway as target architecture.

### Required Fresh-Runway Properties

- Transfer existing execution, recovery, validation acceptance, review
  coordination, commit, finalization, closeout, and reconciliation ownership to
  `work-batch` as required by COR-009.
- Start from the actual candidate seam. Do not design a replacement runtime
  before inspecting current behavior.
- Reuse existing state and receipts when they satisfy the observable contract.
- Require new durable state only for a demonstrated missing product behavior,
  never to remember the progress of the CCFG-26 development batch itself.
- Derive Slice count from independently useful ownership and rollback
  boundaries; do not choose it in advance.
- Let each stable `work-batch` invocation implement exactly one candidate Slice
  and stop according to the temporary policy.
- Treat later explicit human invocation as development coordination, not
  candidate automatic continuation.
- Keep candidate code from controlling, selecting, reserving, launching,
  resolving, or resuming the real CCFG-26 batch that is building it.

### Explicit Non-Goals

- no Batch Execution State engine;
- no shared stable/candidate runtime state;
- no self-hosting;
- no automatic fresh-process launcher;
- no cross-checkout runtime bridge;
- no hostile namespace-substitution guarantee;
- no POSIX descriptor-relative or Win32/NT handle-relative backend;
- no CCFG-27 cutover or CCFG-29 integration work; and
- no successor selection.

### Required Planning Review Questions

The independent planner review must answer all of these explicitly:

1. Does any requirement make stable and candidate communicate at runtime?
2. Does any new state exist primarily to remember development progress?
3. Does the runway expand COR-009 beyond execution and closeout ownership
   transfer without a separate accepted decision?
4. Does it introduce a filesystem threat model absent from ADR 0004?
5. Does it pull cutover, bridge, or integration work forward from CCFG-27 through
   CCFG-29?
6. Can a fresh agent explain the development topology without describing two
   cooperating runtimes?
7. Does the runway remain useful if implementation Slices are manually resumed
   through later explicit stable `work-batch` invocations?

Any `yes` answer to questions 1 through 5, or any `no` answer to questions 6
through 7, requires correction before queueing.

The later `plan-batch CCFG-26` invocation must stop after writing, reviewing,
validating, and queueing exactly one fresh runway. It must not implement it.

## Agent Pickup Brief

An agent asked to execute this recovery plan should:

1. work from `/home/alacasse/projects/codex-config` on `master`;
2. run Planning State `current` and `validate` before edits;
3. verify both checkout identities and preserve unrelated changes;
4. keep the candidate checkout read-only;
5. implement Work Packages 1 through 3 in order with the declared commit
   boundaries;
6. run the complete recovery validation and read the resulting pickup output;
7. report exact stable commits, changed paths, validation results, final queue
   state, and unchanged candidate identity; and
8. stop before `plan-batch`, candidate implementation, installation, or
   successor selection.

The handoff after successful recovery is one explicit next action:

```text
plan-batch CCFG-26 from COR-009, ADR 0004, and current candidate code
```
