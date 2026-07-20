# CCFG-26 Installed-Caller Cutover

## Status And Sequence

- Candidate batch ID: `ccfg-26-installed-caller-cutover`.
- Parent finding: CCFG-26 / COR-009.
- Sequence: second of two descriptive CCFG-26 child batches.
- Dependency: exact accepted closeout of
  [`ccfg-26-public-work-batch-owner`](ccfg-26-public-work-batch-owner.md).
- Planning state: deferred candidate; not selected, not dispatched, not queued,
  and not ready for planning until the first batch closes.

Together with the public-owner batch, this document supersedes the one-batch
decomposition in
[`ccfg-26-work-batch-owner-transfer-replanning-brief.md`](ccfg-26-work-batch-owner-transfer-replanning-brief.md)
as active planning direction. The old brief and its
[`exact review`](ccfg-26-work-batch-owner-transfer-replanning-brief-review.md)
remain historical source evidence.

## Goal

Move every normal installed caller to the accepted public `work-batch` owner,
retire Batch Runway/APR decision authority from those paths, and close COR-009
without changing the runner phase model, physically deleting legacy source, or
selecting a successor.

The starting condition is a candidate-installed public command that already
owns direct execution through reconciled idle state. This batch is caller
cutover and authority retirement, not another execution-owner implementation.

## Required Handoff From The First Batch

Planning must start from live Planning State and the compact exact closeout of
`ccfg-26-public-work-batch-owner`. The handoff must identify:

- accepted candidate commit, installed owner version, and exact interface;
- complete green direct-command and reconciliation evidence;
- every retained normal caller and legacy entrypoint;
- exact runner and Goal Runner prompts/call sites;
- manifest dependencies and installed links;
- temporary v1 worker/reviewer compatibility and its callers;
- old-format active-state readers and their current behavior;
- observed validation, installation, and review runtimes; and
- any blocker or contract change that would invalidate this batch boundary.

If the first closeout is missing, contradictory, not exact, or does not leave a
complete reconciled public owner, stop instead of reconstructing the result from
historical planning prose.

## Included Outcome

This batch owns the normal-caller migration and final COR-009 convergence:

- runner `execute` invokes the public installed `work-batch` flight;
- runner `closeout` becomes observation-only over an already reconciled result;
- Goal Runner invokes public `work-batch` and performs no APR follow-up call;
- exact pre-execute, post-execute, and observation change allowances cover only
  the required CURRENT, LEDGER, closeout, completed-slice, and receipt paths;
- `work-batch` no longer requires Batch Runway/APR as installed decision-owner
  features;
- registered v1 result compatibility is relocated under the agent-owned
  temporary reference, with exact callers and a CCFG-28 removal decision;
- old-format active-state readers are inventoried and either remain read-only
  with no progression authority or fail closed;
- direct Batch Runway/APR product-decision entrypoints fail closed or redirect
  to the one public owner without carrying a second algorithm;
- routing, manifests, installer behavior, docs, scenarios, and acceptance tests
  describe the new owner; and
- a fresh legacy-free candidate installation completes the public command
  flight with no successor selection.

Physical presence is not authority. Legacy files and compatibility hosting may
remain where CCFG-27 or CCFG-28 still owns their phase-model decision or physical
deletion.

## Counterfactual Acceptance

The future runway must include required-green evidence that:

- a production `CodexExecWorker` path using a fake `codex` executable fails if
  Batch Runway or APR appears in the execution prompt;
- runner closeout cannot mutate planning stores or choose a successor;
- Goal Runner cannot invoke APR after public `work-batch` returns;
- poisoned direct legacy decision routes are unreachable from normal callers;
- malformed or stale compatibility results fail before effects;
- another Ready finding remains untouched;
- a legacy-free fresh installation contains and invokes the complete public
  owner; and
- exact final validation and review bind the accepted candidate commit.

## Acceptance Boundary

This batch may close CCFG-26 / COR-009 only when:

1. public `work-batch` is the sole installed execution, recovery, validation
   acceptance, review coordination, commit, finalization, closeout, and
   reconciliation decision owner;
2. runner and Goal Runner normal paths invoke that owner and no legacy fallback;
3. retained compatibility has an exact caller, reason, non-authoritative role,
   and removal owner/condition;
4. fresh candidate and legacy-free installations converge;
5. the complete affected acceptance matrix and exact-range reviews are green;
6. Planning State reconciles to idle for exactly CCFG-26; and
7. CCFG-27 and every other successor remain unselected and unprepared.

If implementation or review exposes additional owner work behind the public
interface, reopen CCFG-26 as `Prepared` or record a bounded follow-up under the
same parent. Do not hide new owner semantics inside caller rewiring.

## Explicit Deferrals

- Serialized runner phase identity or public phase-model changes remain CCFG-27.
- Physical Batch Runway/APR deletion and final compatibility cleanup remain
  CCFG-28.
- Default-home rebinding, branch integration, strict bridge removal, and
  temporary dogfooding-policy removal remain CCFG-29.
- This batch must not restore a persistent execution-state model, a
  cross-generation runtime protocol, or rejected CCFG-26B/C/D/E sequencing.

## Stop Conditions

Stop planning or execution if:

- the public-owner closeout is absent or does not prove reconciled direct-command
  behavior;
- caller cutover requires changing the accepted owner interface instead of
  extending or adapting callers to it;
- a normal route can still make a Batch Runway/APR decision or silently fall
  back to one;
- full acceptance would require CCFG-27, CCFG-28, or CCFG-29 scope;
- candidate code would mutate canonical stable planning during its own
  development batch; or
- closeout selects, dispatches, queues, refreshes, or prepares a successor.

## Linked Evidence

- [First child batch source](ccfg-26-public-work-batch-owner.md)
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
