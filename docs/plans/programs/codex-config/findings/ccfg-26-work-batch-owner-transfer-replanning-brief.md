# CCFG-26 Work-Batch Owner-Transfer Replanning Brief

## Status And Consumer Contract

This is the bounded source contract for the next explicit
`plan-batch CCFG-26` invocation. It is not a selected dispatch, queued runway,
implementation authorization, or execution artifact.

The future planner must start from live Planning State, the CCFG-26 ledger row,
this brief, and current candidate code. It must not require a fresh agent to
reload the full interrogation report unless one of this brief's claims is
contradicted or a named evidence question cannot otherwise be resolved.

The planning result is exactly one newly identified CCFG-26 dispatch/runway pair
plus an independent exact-draft review. The replacement may be queued only from
idle Planning State after a clean review. Planning stops before implementation
and selects no successor.

## Evidence Snapshot

The supersession decision was made against these observed identities:

| Role | Root | Branch | Revision |
|---|---|---|---|
| Stable controller and canonical planning | `/home/alacasse/projects/codex-config` | `master` | `27c2ada4ce095ac42b102592d4d16237527c931d` |
| Candidate implementation | `/home/alacasse/projects/codex-config-command-owner-redesign` | `implementation/command-owner-redesign` | `5c5ec9d52dd9033daa45f3a200031c152363b62c` |

The future planner must resolve and report fresh stable and candidate identities
before drawing implementation conclusions. It must validate the complete strict
`cross-checkout-context/v1` planning snapshot with the installed stable helper
and preserve it in the new runway. Snapshot revisions are historical planning
evidence, not live execution leases.

Detailed evidence is retained in:

- `../notes/ccfg-26-plan-gap-interrogation.md`;
- `../notes/stable-runway-dogfooding-policy.md`;
- `../findings/command-owner-redesign-planning-execution-carry-forward.md`;
- `../findings/slice-shape-policy-direction.md`;
- `../batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`.

The superseded execution-state foundation, CCFG-26B, ADR 0003, issues #59 and
#61, and CCFG-26C through CCFG-26E are historical evidence only. They are not an
accepted implementation sequence, parity gate, or source of current authority.

## Goal And Required End State

Preserve CCFG-26 and COR-009: one installed human-facing `work-batch` command
must own the complete same-batch decision flight for one already queued or
active batch. After CCFG-26 it must:

1. use Planning State `current` and `validate` as the sole semantic currentness
   gate;
2. decide proceed or stop;
3. derive the next incomplete slice from accepted artifacts;
4. delegate implementation to registered `runway_worker` and independent review
   to registered `runway_reviewer`;
5. validate collaborator results and configured validation results;
6. accept or reject exact Git movement, commit, and receipt evidence;
7. recover validation failures, review findings, missing or stale evidence,
   commit-before-receipt failures, and interruptions without changing slice;
8. retain completed-slice evidence and continue the same batch;
9. run final validation and required final review;
10. produce one lineage-bound `planning-closeout/v1` artifact;
11. reconcile exactly that batch into `LEDGER.md` and `CURRENT.md` through the
    existing planning-contract stores;
12. recover closeout or reconciliation partial effects idempotently; and
13. return reconciled idle state without selecting or preparing a successor.

The installed semantic path must be:

```text
human or compatible runner
  -> installed work-batch skill
  -> work-batch/v1 deterministic owner + registered collaborators
  -> Planning State and planning-contract mechanisms
  -> one same-batch result
```

Planning State remains the semantic currentness authority. Planning-contract
read, compare-and-swap, immutable-artifact, lineage, and receipt functions remain
mechanisms. Git remains material-integrity evidence. None may independently
decide workflow progression, acceptance, recovery, closeout disposition,
reconciliation, or successor selection.

## Preserved Boundaries And Explicit Non-Goals

The replacement plan must preserve:

- ADR 0004's single-generation development boundary: stable controls the real
  CCFG-26 batch and candidate never controls its own implementation;
- the completed CCFG-26A vertical-planning behavior and issue #66 slice-shape
  correction without reopening either batch;
- the temporary stable-runway dogfooding policy until CCFG-29;
- serialized runner phase identities through CCFG-26;
- CCFG-27 ownership of runner public phase-model decisions;
- CCFG-28 ownership of physical Batch Runway/APR deletion and final legacy-owner
  cleanup; and
- CCFG-29 ownership of integration, default-home rebinding, bridge removal, and
  temporary-policy removal.

The replacement must not add or restore:

- `execution-state.json`, a run database, a canonical execution-state model, or
  another persistent state/store/schema;
- reservation, attempt, flight, or manifest state from rejected CCFG-26 designs;
- cross-generation runtime calls, synchronization, or shared execution state;
- a second hybrid-skill schema or `skill-authoring` runtime dependency;
- Graphify, graph outputs, or tool-specific repository exploration authority;
- physical deletion of Batch Runway/APR in CCFG-26;
- runner phase-model redesign, default-generation cutover, candidate merge, or
  successor preparation; or
- telemetry thresholds, changed-line limits, token totals, or compaction
  metrics as execution prerequisites.

## Deterministic-Code Rule

The future dispatch must require the accepted command-owner design corpus to
record this repository-authoritative rule before the first implementation slice
is accepted:

> If a workflow result can be derived deterministically from explicit inputs and
> accepted policy, production code owns that derivation. Skills and agents may
> invoke, supply evidence to, or explain the code result; they may not duplicate
> the algorithm in prose or independently reinterpret it.

Apply the rule to `work-batch` as one composite deep module:

- the skill retains human intent, registered-agent invocation, genuinely
  ambiguous correction judgment, and concise explanation;
- Python owns structured parsing, currentness consumption, progression,
  validation capture, evidence acceptance, Git/receipt checks, replay, closeout,
  reconciliation, and no-successor guards;
- workers own implementation judgment;
- reviewers own independent review judgment; and
- mechanisms apply already accepted deterministic effects only.

Markdown, TOMLs, schemas, and tests may declare or verify an invariant, but must
not carry a second executable interpretation of it.

## Required Hybrid Owner And Module Shape

The future plan must target this minimum production shape:

### `skills/work-batch/SKILL.md`

- concise Markdown procedure;
- exactly one valid `skill-contract/v1` YAML block;
- no duplicate machine facts in prose;
- no manual deterministic state machine;
- direct invocation of the private JSON adapter; and
- direct registered worker/reviewer calls only when the returned action requests
  that judgment.

`skill-authoring` may author or audit this file but is not installed as a
runtime dependency of work-batch.

### `scripts/work_batch.py`

- thin stdin/stdout JSON adapter only;
- closed-world request parsing and result serialization;
- construction of the real runtime dependency adapter; and
- no progression, acceptance, recovery, closeout, or reconciliation policy.

### `scripts/work_batch_owner.py`

Expose one external interface:

```python
execute_work_batch(
    request: WorkBatchRequest,
    runtime: WorkBatchRuntime,
) -> WorkBatchResult
```

The external request/result contract must be a versioned closed union. Each call
re-derives the next action from Planning State and accepted durable artifacts.
An optional observation may contain exactly one raw worker result, validation
result, reviewer result, commit/receipt result, or store-apply result. The
caller does not select the transition.

The result union must be able to request or report:

- worker delegation;
- configured validation;
- reviewer delegation;
- commit and receipt recording;
- continuation of the same batch;
- finalization;
- same-batch reconciliation;
- reconciled completion; or
- a typed fail-closed stop with exact replay inputs.

Organize implementation behind the interface by cohesive responsibility:

- currentness and artifact-only progression;
- structured collaborator/result acceptance;
- validation and Git/receipt integrity;
- finalization and closeout production; and
- ordered reconciliation and replay.

Do not organize modules by runway slice or historical owner. Do not add
speculative ports/classes. Only subprocess validation, Git observation/effects,
filesystem/artifact I/O, and store application belong behind the injected
runtime unless a second real adapter proves another seam. Parsing and policy
evaluation remain ordinary implementation.

### Format Ownership

- YAML: the single skill contract and compact closed-world LLM
  handoffs/results;
- JSON: private skill-to-script transport, canonical hashing, subprocess facts,
  machine actions/results, and receipts; and
- Markdown plus YAML: durable Git-reviewable planning artifacts.

Python must parse the exact raw collaborator YAML. Reject prose-wrapped,
duplicate-key, extra-field, malformed, wrong-version, wrong-lineage, stale, or
contradictory YAML/JSON before any acceptance or write.

## Artifact-Only Progression And Failure Evidence

Production progression must be re-derived on every call from:

- Planning State current and validation results;
- the immutable selected runway and batch identity;
- accepted `completed-slices.md` rows;
- the batch-local `execution-report.md` when present;
- immutable closeout and action receipts; and
- exact Git repository, revision, diff, and commit evidence.

`execution-report.md` is evidence, not state. For an unresolved failure it must
name the batch and slice, last accepted stage, failure class, exact evidence
pointers, replay key, and no-successor result. It may not authorize the next
action; the Python owner re-derives that action from all accepted inputs.

Slice 1 must define a durable fail-closed result for validation failure, review
findings, missing/stale evidence, repository movement, commit-before-receipt
failure, and interruption. Slice 2 must consume that exact result. No migrated
path may invoke Batch Runway recovery as a fallback.

## Cross-Checkout Lease Mechanism

The candidate target must expose the stable bridge's narrow mechanical behavior
through `scripts/cross_checkout_context.py`:

- `preflight_cross_checkout_live_lease(...)` for the first handoff from the
  immutable planning snapshot; and
- `prepare_cross_checkout_context_refresh(...)` before later worker/reviewer
  handoffs.

Planning State alone decides whether the queued/active batch is current. The
helper validates identity, generation, revisions, movement, and scope; it does
not choose proceed, recovery, delegation, acceptance, closeout, or successor
behavior. Every worker and reviewer receives a freshly prepared strict lease,
and every accepted receipt records that exact lease.

If the prototype shows that the existing candidate helper cannot support an
equivalent mechanism without a new state model, public protocol, platform
dependency, or cross-generation runtime call, stop for a reviewed semantic
amendment.

## Agent Contract Compatibility

New work-batch handoffs use registered v2 worker/reviewer result contracts.

Temporarily retain v1 result compatibility without a Batch Runway ownership
dependency by moving its shared contract to
`agents/runway-result-contract-v1.md`, updating both registered TOMLs, and
installing that reference with the custom-agent feature. Name its exact caller,
reason, and CCFG-28 removal condition. No new work-batch path may emit or prefer
v1.

## Ordered Reconciliation Contract

Reconciliation is an ordered forward-recovery saga over existing mechanisms,
not a compound atomic transaction and not a new state model:

1. validate or exact-replay the lineage-bound closeout;
2. apply or exact-replay the exact CCFG-26 `LEDGER.md` decision first;
3. only after accepted ledger evidence, clear the same batch's selected,
   queued, and active `CURRENT.md` pointers and set `latest_closeout`; and
4. return a result binding both per-document receipts and no successor.

On restart, derive the next action from the closeout, both documents, and their
receipts:

| Observed state | Required action |
|---|---|
| neither store applied | apply LEDGER, then CURRENT |
| LEDGER applied, CURRENT pending | exact-replay LEDGER, then apply CURRENT |
| both applied | exact-replay both and return reconciled |
| CURRENT cleared before LEDGER | repair only when exact closeout and CURRENT receipt prove the same batch and expected predecessor; otherwise stop fail-closed |
| foreign, missing, stale, or contradictory receipt | stop fail-closed |

After the first accepted canonical store effect, rollback means exact forward
recovery from the same closeout, not reverting Git. A reconciliation result may
aggregate the two receipt identities in its machine output, but must not add a
new persistent compound store.

## Complete Caller Migration Matrix

The new dispatch and runway must classify every row below with current owner,
future owner, exact caller, migration slice, retained reason, forbidden
fallback, and removal condition.

| Caller or surface | Required CCFG-26 disposition |
|---|---|
| public installed `work-batch` | sole execution through reconciliation owner |
| public/direct Batch Runway entrypoint | fail closed for candidate product decisions; physical removal in CCFG-28 |
| public/direct APR entrypoint | fail closed for candidate product reconciliation; physical removal in CCFG-28 |
| registered worker/reviewer v2 | retained collaborator protocol, never acceptance owner |
| registered worker/reviewer v1 | relocated under agent-owned reference; temporary compatibility; CCFG-28 removal decision |
| old-format active-state readers | inventory every reader; allow read-only interpretation only when it cannot decide progression, otherwise refuse fail closed; name CCFG-28 removal or an earlier proven zero-live-state deletion condition |
| Planning State | retained sole semantic currentness diagnostic |
| planning-contract reads/stores | retained apply-only mechanisms |
| runner `execute` | invoke one public work-batch flight |
| runner `closeout` | observation-only over already reconciled work-batch result |
| goal-runner | invoke public work-batch only; remove APR follow-up call |
| outer-runner `next_phase=select-dispatch` | distinguish process looping from in-command successor selection; public protocol decision deferred to CCFG-27 |
| APR-hosted runner schemas/references | retained compatibility hosting only; relocation/deletion deferred to CCFG-27/28 |
| feature manifest and installer | link work-batch skill and both Python files; remove work-batch requirements on legacy owners after counterfactual proof |
| strict bridge | retained temporary mechanical development support; CCFG-29 removal |

Physical presence is not authority. Every legacy entrypoint retained after a
slice must be unreachable from normal migrated callers or fail closed before a
decision. Redirect-only behavior is acceptable only when it forwards to the
single work-batch owner without carrying a second algorithm.

## Mandatory Pre-Slice Feasibility Gates

Complete both disposable proofs before final dispatch/runway drafting and exact
planning review. Use host-native temporary planning roots and real temporary Git
repositories. Do not edit candidate production code or create persistent
artifacts during these proofs.

### Gate A: Installed Owner Handshake And Artifact-Only Progression

Prototype and record:

- the exact `work-batch/v1` request, action, result, error, replay, and compact
  progress fields;
- the two-file Python boundary and internal responsibility map;
- closed YAML worker/reviewer handoff fields and raw-result parsing;
- pickup of the next incomplete slice from accepted artifacts only;
- clean progression and all Slice 1 fail-closed results;
- restart of the same slice without `execution-state.json`;
- real Git HEAD movement, wrong repository, unrelated commit content, missing
  commit, commit-success/receipt-failure, and exact receipt replay; and
- a candidate-only/legacy-absent installed dry run.

Obtain an architecture review of interface depth, locality, dependency
direction, error modeling, and extension behavior. Record exact prototype
files, commands, runtimes, findings, and the resulting production module map in
the new dispatch/runway.

### Gate B: Two-Document Reconciliation

Prototype and record:

- closeout validation and exact replay;
- LEDGER-first then CURRENT ordering;
- faults before either write, after LEDGER and before CURRENT, after both, and a
  manufactured forbidden CURRENT-first state;
- restart and exact forward recovery from the same closeout;
- foreign/stale/missing receipt rejection;
- preservation of another `Ready` finding; and
- proof that no successor is selected or prepared.

If either gate requires a new persistent state/store/schema, public protocol
beyond COR-009, cross-generation runtime communication, a new platform boundary,
or movement of CCFG-27/28/29 scope into CCFG-26, stop before drafting an
executable runway and request a reviewed design decision.

## Slice-Shaping Rules

Derive slice count from the proven interface and complete callable authority
states. Five slices are the evidence-backed minimum, not a target or ceiling.
Add a slice when the prototype exposes another independently usable boundary or
when one coordinator context cannot implement and review the proposed change
reliably.

Never compress work to preserve a fixed count. Never create horizontal
models/helpers/tests/docs slices without a production caller. Every production
slice must name a starting scenario, durable result, owner before/after,
migrated callers, focused validation, independently usable state, rollback or
forward-recovery boundary, temporary residue, and removal condition.

### Minimum Slice 1: Installed Clean Owner And Fail-Closed Boundary

Complete scenario: installed work-batch selects one clean slice, delegates,
validates, obtains independent review, accepts exact Git movement and receipt,
records completed-slice evidence, and stops at the next slice boundary.

Before acceptance:

- install candidate work-batch and run its public entrypoint;
- prove all not-yet-recoverable validation/review/receipt/interruption branches
  return the exact durable fail-closed result;
- poison old recovery, finalizer, and reconciler routes;
- prove malformed YAML/JSON fails before effects; and
- run real-Git counterfactuals.

Rollback restores the previous candidate code before canonical program effects.
Old recovery/finalization/reconciliation may remain physically present but may
not be reachable as fallback.

### Minimum Slice 2: Recovery, Resume, And Currentness

Complete scenario: the installed owner consumes Slice 1's exact blocked result,
refreshes currentness and leases, corrects validation/review failures, accepts
exact evidence, and resumes the same slice after interruption.

Bind behavior to the immutable runway, completed-slices archive,
`execution-report.md`, receipts, Planning State, and real Git. Require separate
fresh worker/reviewer leases and contradictory-helper fail-closed tests. Remove
all migrated calls to Batch Runway recovery/resume.

Rollback must return to Slice 1's fail-closed behavior, never the legacy
recovery engine.

### Minimum Slice 3: Finalization And Closeout Production

Complete scenario: after the last accepted slice, work-batch runs final gates,
validates complete evidence, produces one immutable lineage-bound closeout, and
exact-replays a partial closeout write.

Add an installed-owner closeout-production-only scenario. Do not use a fixture
that immediately reconciles. Reject incomplete slice evidence, foreign identity,
unresolved placeholders, stale final review, and successor-bearing closeout.
Old Batch Runway finalization/closeout production must be poisoned.

The independently usable result is a complete unreconciled closeout whose sole
next semantic owner is the later work-batch reconciliation slice. Do not claim
APR is a temporary apply owner.

### Minimum Slice 4: Public Reconciliation Owner

Complete scenario: public installed work-batch applies or replays the same
closeout through the ordered reconciliation contract, returns idle, and leaves
all successor work untouched.

Prove every fault-matrix state, contradictory APR results, another Ready
finding, and exact restart. Direct runner/goal-runner compatibility calls may
remain fail-closed until Slice 5, but may not apply reconciliation or fall back
to their legacy owners.

After the first canonical store receipt, recovery is forward-only from the same
closeout.

### Minimum Slice 5: Runner And Installed-Caller Cutover

Complete scenario: runner execute invokes public work-batch, runner closeout is
observation-only, goal-runner makes no APR follow-up call, work-batch no longer
requires legacy-owner features, v1 agent compatibility has its classified
temporary home, direct legacy entrypoints fail closed, and a legacy-free fresh
installation runs the complete public command flight.

Correct pre-execute, post-execute-as-closeout, and observation-phase change
allowances for exact CURRENT, LEDGER, closeout, completed-slice, and receipt
paths while rejecting arbitrary siblings. Test the production `CodexExecWorker`
path with a fake `codex` executable that fails if Batch Runway or APR appears in
the prompt.

This slice does not redesign serialized phase identities or decide the outer
runner's later-batch loop protocol.

## Counterfactual Acceptance Matrix

The new runway must make these required-green before their owning slice or final
gate is accepted:

| Authority | Required counterfactual |
|---|---|
| hybrid skill | direct target validation and before/after ownership comparison fail when contract is absent, duplicated, or inconsistent |
| structured transport | malformed/extra/duplicate/stale YAML or JSON fails before effects |
| clean execution | work-batch passes without installed Batch Runway/APR; poisoned old clean path is never reached |
| recovery | exact fail-closed result resumes same slice; poisoned legacy recovery is never reached |
| currentness/leases | contradictory Planning State/helper facts and movement during preparation stop before delegation |
| Git/receipt | real repository movement, foreign repo/content, missing commit, and commit-before-receipt are detected and exactly recoverable where authorized |
| finalization | poisoned old finalizer, incomplete evidence, stale review, placeholders, and foreign completed rows reject |
| closeout | installed owner produces and exact-replays closeout without direct fixture reconciliation |
| reconciliation | APR contradiction is irrelevant; every inter-store fault rolls forward or fails closed; another Ready finding stays untouched |
| runner | production subprocess path records only public work-batch invocation; observation performs no APR mutation |
| no successor | APR or another finding may propose a successor, but work-batch reconciles only the current batch and stops |
| legacy residue | old files may remain, but no normal manifest, skill, runner, goal-runner, agent, documentation, or acceptance caller reaches their decision logic |

Existing fixture execution/currentness/closeout scenarios remain mechanism
characterization until rebound through the installed owner. Topology, prose,
schema, and link assertions alone are not ownership proof.

## Validation And Cost Contract

Classify each command in the new runway as `required-green`,
`known-red-baseline`, `implementation-created`, `conditional`, or
`diagnostic-only` before execution.

Current planning evidence classifies:

- Planning State `current` and `validate`: required-green;
- command-owner scenario catalog validation: required-green mechanism baseline;
- focused execution/currentness/closeout fixture nodes: required-green mechanism
  baseline, not target-owner proof;
- the four-file lifecycle suite: known-red until the runner/caller cutover
  promotes its single topology failure;
- direct `skill_contract.py validate ... skills/work-batch/SKILL.md`: known-red
  until the clean-owner slice; and
- `tests/test_work_batch.py`: implementation-created.

Use exact focused nodes during correction loops. Reserve the current slow
four-file suite for its promotion slice and final validation.

For every proposed slice, the new runway must record:

- exact expected files or a narrow enumerated directory subset;
- expected production surfaces;
- prototype-derived line range, or explicit `unknown` plus a measurement gate;
- exact required/conditional commands and one current runtime sample;
- installation cadence and measured install/dry-run time;
- expected worker, reviewer, architecture, test-quality, import-topology, and
  dead-surface review calls; and
- the stop condition before coordinator context loss makes the acceptance basis
  unreliable.

Every candidate slice requires `git diff --check`, focused validation,
independent exact-diff review, and a focused candidate commit. Test-changing
slices trigger delta-only `test-quality-review`; import/legacy-route changes
trigger only the specialist reviews required by actual diff facts.

Final acceptance must include affected work-batch, scenario, currentness,
lifecycle, manifest, routing, agent-contract, planning-contract, Planning State,
runner phase/command/change-allowance, and skill-contract tests; scenario catalog
validation; fresh candidate and legacy-free installations; exact-commit
acceptance with fresh output paths; configured Ruff/BasedPyright; final
`git diff --check`; test-quality review; and independent exact-range review.

## Future Plan-Batch Procedure

A later explicit `plan-batch CCFG-26` must:

1. run Planning State `current` and `validate` and require selected, queued, and
   active pointers to be empty;
2. resolve the CCFG-26 ledger row and this brief as the selected source;
3. verify stable/candidate identities and current candidate behavior;
4. complete both disposable feasibility gates and their architecture review;
5. choose a new batch identity and directory; suggested slug:
   `ccfg-26-work-batch-owner-transfer-replan`;
6. author a new dispatch and full runway from the proven interfaces, caller
   matrix, scenario boundaries, costs, and required counterfactuals;
7. preserve the old `ccfg-26-work-batch-owner-transfer` package unchanged as
   superseded evidence;
8. obtain an independent exact-draft review whose evidence reconstruction
   covers callers, failure states, feasibility, counterfactuals, slice
   alternatives, and cost;
9. bind exact dispatch/runway/review digests through the normal idle-state
   planning transaction; and
10. stop with one queued replacement, no active runway, no implementation, and
    no selected successor.

The planner must not treat the suggested slug or minimum five slices as
authority if live evidence requires a different unique slug or additional
scenario-complete boundaries. It must record why any deviation remains inside
this brief's goal and stop conditions.

## Planning Review Contract

The independent exact-draft reviewer must reconstruct rather than repeat:

- current and future semantic owners;
- the complete normal-caller set;
- every reachable intermediate failure state and its next owner;
- feasibility proof for the installed handshake, artifact-only progression,
  real Git/receipt recovery, and two-document reconciliation;
- counterfactuals that fail on bypass;
- independently usable and rollback/forward-recoverable slice boundaries;
- smaller scenario-complete alternatives for every broad slice; and
- expected files, validation/runtime multipliers, installations, and review
  cost.

A bare `pass` table is insufficient. The review must cite pinned file/symbol or
command evidence for every semantic approval and bind the exact dispatch and
runway SHA-256 digests. Any content change requires another exact review.

## Stop Conditions

Stop before queueing or execution if:

- Planning State is non-idle when replacement selection begins;
- stable/candidate identity or strict context is missing, ambiguous, or
  contradictory;
- a decisive primitive remains fixture-only or unproved;
- any failure branch can silently invoke Batch Runway/APR;
- the Python/skill/agent/mechanism responsibility matrix is incomplete;
- a slice has no complete callable scenario or fail-closed handoff;
- reconciliation ordering or partial-state recovery is still described as
  compound atomicity;
- a normal caller or legacy entrypoint lacks a terminal classification;
- acceptance relies only on topology/prose/schema assertions;
- a new persistent state/store/schema, cross-generation runtime communication,
  or new platform dependency is required;
- CCFG-27/28/29 scope is pulled into CCFG-26;
- Graphify becomes required evidence or workflow authority;
- CCFG-26A, CCFG-26B, CCFG-26C/D/E, ADR 0003, issue #59, or issue #61 is revived
  as an accepted implementation sequence; or
- the plan selects, prepares, or queues a successor.

## Acceptance For Replanning

The planning task is complete only when one fresh CCFG-26 dispatch/runway pair:

- is based on live stable/candidate evidence and both feasibility gates;
- makes the external interface and internal ownership division explicit;
- classifies every caller and intermediate failure state;
- uses scenario-complete slices with measured execution/review cost;
- makes displaced-owner counterfactuals required-green;
- has a clean independent evidence-backed exact-draft review;
- is the sole queued batch in canonical Planning State; and
- records that implementation has not started and no successor was selected.
