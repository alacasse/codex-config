# CCFG-26 Execution-State Foundation Dispatch

## Selection

- Batch ID: `ccfg-26-execution-state-foundation`
- Source program ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: `CCFG-26. Transfer Execution and Closeout Ownership to
  work-batch`
- Batch kind: `migration`
- Owner seam: candidate `work-batch` execution intent plus the canonical Batch
  Execution State module consumed by the real candidate runner `execute` caller.
- Validation class: project-harness production behavior, focused process/crash
  tests, strict cross-checkout validation, installation proof, exact scenario
  acceptance, and independent review.
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-26-execution-state-foundation/runway.md`

Planning State was valid and idle before selection. No dispatch, runway, or
successor was selected. This dispatch selects only the first bounded CCFG-26
execution-foundation batch authorized by the accepted design contract.

## Goal

End in one independently useful candidate state through the real runner and
public `work-batch` seam:

1. one deep, batch-stable execution-state owner applies validated transitions
   under portable process serialization, expected-state compare-and-swap, and
   exact replay; and
2. one fresh public `work-batch` coordinator advances exactly one accepted
   Slice through that owner, returns an action-free Execution Flight Result,
   and leaves a later fresh invocation the exact next Slice without chat
   history or Markdown progression authority.

The one-flight milestone deliberately maps `continue_same_batch` to the
existing compatible stopped Phase Result with
`stop_reason=manual_continuation_required`. Automatic Same-Batch Continuation
is deferred because it adds a distinct outer process loop, flight-result
aggregation, one-final-receipt rule, crash-between-flights behavior, and a
separate rollback boundary. It remains required before CCFG-26 normal use or
closeout.

## Included Scope

- Implement the accepted `batch-execution-state/v1` state, event, result,
  receipt, projection, CAS, idempotency, path, lock, and crash contracts in the
  candidate checkout behind a small typed interface.
- Exercise that interface through an executable generated-only acceptance path,
  not uncalled source scaffolding.
- Add the first real candidate runner/public `work-batch` one-flight tracer.
- Preserve the serialized phase identities `select-dispatch`, `create-spec`,
  `execute`, and `closeout`.
- Add focused Linux process/crash evidence and a repository-owned
  Ubuntu/macOS/Windows matrix gate for the portable lock contract.
- Update only candidate installation, manifests, target documentation, and
  behavioral fixtures required by this bounded result.

## Explicitly Deferred

- Automatic Same-Batch Continuation.
- Recovery or relaunch of ambiguous `in_flight` attempts.
- Final validation/finalization transitions.
- Closeout, program-ledger reconciliation, Planning State completion, and
  successor selection in the target implementation.
- Displaced-owner narrowing beyond the exact one-flight tracer caller.
- CCFG-26C through CCFG-26E, whose old names remain conceptual evidence only.
- CCFG-27 serialized-protocol decisions, CCFG-28 deletion/cutover, and CCFG-29
  integration/bridge removal.
- Any stable implementation edit, default-generation switch, or stable-home
  install.

## Slice Shape

The batch has two vertical implementation slices.

1. `execution-state-owner`: one public apply/query interface owns state,
   persistence, locking, receipts, projections, and replay end to end. Splitting
   its reducer, store, lock, schema, and receipt renderer into separate slices
   was rejected because each smaller state would expose internal coordination
   and leave no independently usable accepted interface.
2. `one-flight-work-batch-tracer`: the real candidate runner and public
   `work-batch` consume the Slice 1 interface. Separating skill wording, runner
   launch, result validation, or stopped-result mapping would leave a
   contradictory production route or silent Batch Runway fallback.

The `1 -> 2` split is valid because Slice 1 leaves an executable, tested public
state interface with its own dependency and rollback boundary; Slice 2 consumes
that exact interface and can be reverted without deleting the state owner.

## Migration Matrix

| Scenario or caller | Current owner | Future owner after this batch | Status | Reason | Removal slice or condition |
|---|---|---|---|---|---|
| Generated-only execution-state acceptance | no canonical Batch Execution State owner | candidate deep execution-state module | pending | Prove the accepted interface, crash, CAS, replay, receipt, and projection behavior before production integration | Slice 1 |
| Candidate runner serialized `execute` caller for the first tracer | Batch Runway public execution route | runner process lifecycle plus public `work-batch`; execution-state module owns progression | pending | Establish the real one-flight production seam without changing the phase identity | Slice 2 |
| Public candidate `work-batch` one-flight execution | Batch Runway support is the normal semantic route | `work-batch` owns proceed, reserve, launch, acceptance, resolution, and stop decisions | pending | Transfer only the first tracer path; no silent fallback | Slice 2 |
| Automatic successful continuation | no accepted automatic outer loop | later CCFG-26 batch or reviewed milestone | pending | Distinct lifecycle, receipt, crash, validation, and rollback boundary | Later explicit `plan-batch`; required before CCFG-26 normal use/closeout |
| Unmigrated execution/recovery/finalization/closeout scenarios | existing Batch Runway/APR support routes | later CCFG-26 work | pending | They are outside the first tracer and may remain only with exact caller/reason/removal evidence | Relevant later accepted batch |

## Required Execution Context

- Interface: `cross-checkout-context/v1`
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`
- Stable toolchain/planning revision:
  `93fa9109e35719d4f36dd75edc97bf0df584c1da`
- Candidate implementation revision:
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`
- Stable Codex home: `/home/alacasse/.codex`
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`
- Explicit generated-only run-artifact root allocated through the host
  temporary-directory facility: `/tmp/tmp.nAyp7HeqwO`
- Exact canonical state path for this batch:
  `/tmp/tmp.nAyp7HeqwO/batch-executions/codex-config/ccfg-26-execution-state-foundation/execution-state.json`

The runtime root is a caller-supplied execution input for this batch, not a
project default or a reusable hard-coded path. The exact state path must be
absent before Slice 2 initializes the real tracer. Slice 1 tests use separate
fresh fixture roots and must not create this path. Every real flight receives
this same root; no latest run, glob, Git, chat, or per-run timestamp may replace
it.

## Dependencies

Satisfied:

- CCFG-34 stable-runway dogfooding bootstrap is closed.
- CCFG-26A and the issue #66 slice-shape correction are closed.
- CCFG-26B is superseded historical evidence and is not resumed.
- ADR 0003 and the CCFG-26 execution-state design contract are accepted and
  independently reviewed clean.
- Planning State is valid and idle.
- The strict stable/candidate context is current and validated.
- The candidate install is converged at the baseline.

Execution-created gate:

- Slice 1 must add a focused Ubuntu/macOS/Windows matrix workflow. Final batch
  acceptance requires green evidence for the exact candidate commit. If the
  workflow cannot be published or observed within the later execution's
  authority, keep the batch active and stop; do not downgrade the platform
  contract to Linux-only evidence.

## Guardrails And Stops

- Apply the temporary stable-runway dogfooding policy.
- One `work-batch` invocation advances at most one implementation Slice.
- Stable planning is write-bearing; stable source and candidate planning are
  read-only; candidate implementation is write-bearing only under a fresh live
  lease.
- Stop if either repository identity, branch, revision, home, helper binding,
  canonical planning root, or explicit runtime root is missing or mismatched.
- Slice 1 tests and acceptance must use distinct fresh caller-supplied fixture
  roots and must leave this batch's exact canonical state path absent.
- Stop if this batch's canonical state path exists before Slice 2 initializes
  the real one-flight tracer.
- Stop if any target caller derives progression from Markdown, Git, Run State,
  a per-run manifest, or agent-authored `next_action`.
- Stop if the target tracer exposes or silently falls back to Batch Runway as
  its public or semantic owner.
- Stop if automatic continuation, ambiguous recovery, finalization, closeout,
  successor selection, a new serialized phase, or default-generation switching
  enters scope.
- Stop if a concrete lock dependency cannot prove fail-closed behavior and
  killed-holder reacquisition without leaking backend details through the
  public interface.
- Stop if cross-platform matrix evidence is weakened, simulated, or inferred
  from one host.
- Stop if Graphify is invoked or its outputs become authority.
- Stop before implementation in this `plan-batch` invocation.
