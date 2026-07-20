# CCFG-26 Public Work-Batch Owner

## Status And Sequence

- Candidate batch ID: `ccfg-26-public-work-batch-owner`.
- Parent finding: CCFG-26 / COR-009.
- Sequence: first of two descriptive CCFG-26 child batches.
- Planning state: not selected, not dispatched, not queued, and not authorized
  for implementation.
- Next action: a later explicit stable
  `plan-batch ccfg-26-public-work-batch-owner` may plan this batch only.

Together with
[`ccfg-26-installed-caller-cutover.md`](ccfg-26-installed-caller-cutover.md),
this document supersedes the one-batch decomposition in
[`ccfg-26-work-batch-owner-transfer-replanning-brief.md`](ccfg-26-work-batch-owner-transfer-replanning-brief.md)
as active planning direction. The reviewed brief and its
[`exact review`](ccfg-26-work-batch-owner-transfer-replanning-brief-review.md)
remain historical evidence; they are not a dispatch or runway for either new
batch.

## Observed Intake Snapshot

| Role | Root | Branch | Revision |
|---|---|---|---|
| Stable controller and canonical planning | `/home/alacasse/projects/codex-config` | `master` | `cdf6a0990e804723dc39c8126bc9a33cfea275e5` |
| Candidate implementation | `/home/alacasse/projects/codex-config-command-owner-redesign` | `implementation/command-owner-redesign` | `5c5ec9d52dd9033daa45f3a200031c152363b62c` |

The stable strict `cross-checkout-context/v1` preflight was `ready` for these
identities when this intake document was written. A future planner must refresh
and report both identities and must treat this table as historical intake
evidence, not as a live execution lease.

## Goal

Create one installed public `work-batch` command that owns an already queued or
active batch from semantic currentness through reconciled idle state:

```text
public work-batch
  -> decide and derive the next incomplete slice
  -> delegate, validate, review, commit, and record receipts
  -> recover or resume without changing slice
  -> finalize and produce one closeout
  -> reconcile LEDGER then CURRENT
  -> return idle with no successor
```

This is the deep owner boundary. It must be usable through the public installed
command before normal runner and Goal Runner callers are migrated.

## Ownership Outcome

| Caller or decision | Before this batch | Required result after this batch |
|---|---|---|
| Public installed `work-batch` | Routes execution to Batch Runway and reconciliation to APR | Sole decision owner through reconciliation for the direct public command |
| Worker and reviewer | Registered collaborators whose results are accepted by legacy orchestration | Remain judgment collaborators; Python validates and accepts their structured results |
| Planning State | Semantic currentness authority | Unchanged sole semantic currentness authority |
| Planning-contract stores | Apply-only mechanisms | Unchanged apply-only mechanisms |
| Runner `execute` and `closeout` | Legacy Batch Runway/APR routes | Explicitly deferred to the caller-cutover batch; no fallback from the migrated direct command |
| Goal Runner | Legacy Batch Runway/APR route | Explicitly deferred to the caller-cutover batch |
| Physical Batch Runway/APR files | Installed legacy support and decision surfaces | May remain physically present; physical deletion remains CCFG-28 |

## Required Planning Inputs

Before a dispatch or runway is accepted, the planner must:

1. run Planning State `current` and `validate` and require idle selected,
   queued, and active pointers;
2. refresh the strict stable/candidate identity and write-scope evidence;
3. complete both disposable feasibility gates from the historical
   [replanning brief](ccfg-26-work-batch-owner-transfer-replanning-brief.md#mandatory-pre-slice-feasibility-gates):
   - the installed owner handshake and artifact-only progression proof; and
   - the two-document ordered-reconciliation fault proof;
4. obtain the required architecture review of the proposed public interface,
   responsibility allocation, dependency direction, and replay behavior; and
5. derive scenario-complete slices from the proven interface rather than
   preserving the historical slice count.

The feasibility work is planning evidence, not a separate product batch. Stop
before dispatch/runway approval if either proof requires a new persistent
state/store/schema, cross-generation runtime communication, a new platform
boundary, or scope owned by CCFG-27 through CCFG-29.

## Included Outcome

The future runway may shape the work into as many scenario-complete slices as
the reviewed interface requires, but the batch as a whole owns:

- the concise hybrid `skills/work-batch/SKILL.md` contract;
- the thin private JSON adapter and one deterministic
  `execute_work_batch(...)` owner interface;
- Planning State currentness and artifact-only progression;
- exact worker/reviewer handoffs and closed-world result parsing;
- validation, Git movement, commit, receipt, and replay acceptance;
- durable fail-closed results for validation, review, stale evidence,
  repository movement, commit-before-receipt failure, and interruption;
- same-slice recovery and resume with refreshed strict leases;
- final validation, final review, immutable closeout production, and exact
  closeout replay;
- LEDGER-first then CURRENT ordered reconciliation, fault recovery, and
  forbidden CURRENT-first handling; and
- a reconciled idle result that cannot select or prepare a successor.

The implementation must be exercised through the public installed command.
Fixture adapters and direct mechanism calls are supporting evidence only.

## Acceptance Boundary

This batch is complete only when a candidate-installed public `work-batch`
invocation can take one disposable queued batch through implementation,
recovery, finalization, closeout, reconciliation, and idle state while:

- poisoned Batch Runway/APR decision paths are never invoked by the migrated
  direct command;
- malformed, duplicate, extra, stale, foreign, or contradictory collaborator
  and machine results fail before effects;
- real Git and receipt counterfactuals are green;
- every reconciliation fault is replayed forward or stops fail-closed;
- another Ready finding remains untouched; and
- no successor is selected, dispatched, queued, or prepared.

The stable generation still controls and closes the real development batch
under ADR 0004. Candidate code proves the future public owner only through
disposable fixtures and isolated candidate installation; it does not control
its own implementation batch.

## Required Closeout Handoff

Closeout must leave CCFG-26 `Prepared`, Planning State idle, and
`ccfg-26-installed-caller-cutover` unselected. It must give the later planner a
compact exact inventory of:

- accepted candidate commit and exact review basis;
- installed public request/result/error/replay contract;
- validation and counterfactual results;
- reconciliation receipts and fault-matrix evidence;
- retained runner, Goal Runner, manifest, v1-agent, old-reader, and legacy
  entrypoints with exact callers and removal conditions; and
- measured validation, installation, and review costs relevant to cutover.

Closing this batch must not automatically plan, select, dispatch, or queue the
caller-cutover batch.

## Explicit Deferrals

- Runner and Goal Runner caller migration, manifest dependency convergence,
  v1 compatibility relocation, normal legacy-entrypoint disablement, and the
  final legacy-free installation belong to
  [`ccfg-26-installed-caller-cutover`](ccfg-26-installed-caller-cutover.md).
- Runner public phase-model decisions remain CCFG-27.
- Physical Batch Runway/APR deletion remains CCFG-28.
- Default-home rebinding, bridge removal, branch integration, and temporary
  dogfooding-policy removal remain CCFG-29.

## Stop Conditions

Stop planning or execution if:

- the public command cannot reach reconciled idle state without legacy
  decision fallback;
- an intermediate result lacks an exact current public consumer and an owned
  failure path;
- the two-document reconciliation contract remains assertion-only;
- the candidate generation would control the real CCFG-26 development batch;
- CCFG-27, CCFG-28, or CCFG-29 scope is pulled into this batch; or
- planning selects or prepares the caller-cutover batch or another successor.

## Linked Evidence

- [Accepted single-generation development boundary](../../../../adr/0004-single-generation-command-owner-development-boundary.md)
- [Command-owner planning and execution carry-forward](command-owner-redesign-planning-execution-carry-forward.md)
- [Temporary stable-runway dogfooding policy](../notes/stable-runway-dogfooding-policy.md)
- [Detailed plan-gap interrogation](../notes/ccfg-26-plan-gap-interrogation.md)
- [Planning-instruction root-cause analysis](../notes/ccfg-26-planning-instruction-root-cause-analysis.md)
- [Historical reviewed one-batch replanning brief](ccfg-26-work-batch-owner-transfer-replanning-brief.md)
- [Historical exact review of that brief](ccfg-26-work-batch-owner-transfer-replanning-brief-review.md)
- [CCFG-24 two-batch ownership-transfer precedent](ccfg-24-two-batch-execution-amendment.md)
- [Slice-shape policy direction](slice-shape-policy-direction.md)
- [Slice-shape correction authority evidence](../batches/ccfg-26-slice-shape-policy-correction/post-closeout-correction.md)
