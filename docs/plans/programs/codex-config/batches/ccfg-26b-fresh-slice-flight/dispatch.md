# CCFG-26B Fresh Slice Flight Dispatch

## Selection

- Batch ID: `ccfg-26b-fresh-slice-flight`
- Selection outcome: `selected for exact planning review`
- Queue target: exactly one `queued` runway after a clean independent review
- Covered finding: CCFG-26 / COR-009 happy-path execution flight
- Finding state entering the batch: `Prepared`
- Source program ledger: `../../LEDGER.md`
- Expected runway path: `runway.md`
- Planning root: `../../../..`
- Implementation target:
  `/home/alacasse/projects/codex-config-command-owner-redesign`

Planning State `current` and `validate` reported an idle, valid program with no
selected dispatch, queued batch, active runway, blocker, or obligation. This
explicit stable `plan-batch` request selects only CCFG-26B. CCFG-26A and the
slice-shape correction remain completed historical evidence. CCFG-26C through
CCFG-26E and CCFG-27 through CCFG-29 remain unselected.

## Authoritative Sources

- CCFG-26 and `ccfg-26b-fresh-slice-flight` in `../../LEDGER.md`.
- `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- `../../findings/github-issue-62-stable-runway-dogfooding-bootstrap.md`.
- `../../notes/stable-runway-dogfooding-policy.md`.
- CCFG-26A closeout at
  `../ccfg-26a-permanent-vertical-runway-contract/closeout.md`.
- Slice-shape correction and semantic-authority evidence at
  `../ccfg-26-slice-shape-policy-correction/closeout.md` and
  `../ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`.
- [GitHub issue #61](https://github.com/alacasse/codex-config/issues/61), with
  issue #59 recovery work explicitly deferred to CCFG-26C and issue #60
  planning behavior already completed by CCFG-26A plus the correction.
- COR-009 at accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.

## Goal

Move one complete happy-path implementation scenario to the permanent candidate
`work-batch` owner:

```text
current queued multi-slice runway
  -> Planning State current and validate confirm the same scope
  -> fresh coordinator process invokes public work-batch
  -> work-batch executes exactly the next pending implementation slice
  -> runway_worker implements
  -> coordinator accepts focused validation
  -> runway_reviewer independently accepts the exact diff
  -> coordinator commits and archives the slice evidence
  -> schema-valid batch-execution-flight/v1 receipt is durable
  -> next_action=continue_same_batch names the next slice
  -> the current process ends
  -> the launcher may start a new work-batch process for that same batch only
```

The durable result is one independently usable happy-path execution flight.
It must not absorb recovery, final validation/finalization, same-batch closeout,
or successor selection.

## Included And Deferred Ownership

Included now:

- public `work-batch` owns currentness, proceed/stop, delegation, focused
  validation acceptance, independent review acceptance, commit/receipt,
  execution-ledger update, and completed-slice archival for one happy-path
  implementation flight;
- a `batch-execution-flight/v1` result contract owned and linked by
  `work-batch` persists exact batch/slice identity, `completed | blocked |
  failed` status, before/after candidate revisions, validation/review/commit
  summaries, anomalies, the bounded fresh-flight input manifest, per-flight
  telemetry, and one typed `continue_same_batch | finalize_same_batch |
  closeout_same_batch | require_user` next action;
- the temporary serialized `execute` runner phase invokes public `work-batch`
  and treats the flight result as evidence; it remains a launcher and does not
  regain semantic execution authority;
- a successful `continue_same_batch` result ends the current coordinator process
  and launches a later fresh process from canonical durable state.

Deferred:

- CCFG-26C: blocker classification, the bounded read-only recovery advisor,
  reviewed amendments, and same-slice recovery under a fresh lease;
- CCFG-26D: last-slice transition, final validation, installation, exact
  acceptance, and finalization flight;
- CCFG-26E: closeout/reconciliation flight, partial-closeout recovery, final
  displaced-owner removal, and no-successor proof;
- CCFG-27: any migration or removal decision for serialized
  `select-dispatch`, `create-spec`, `execute`, and `closeout` labels;
- CCFG-28 and CCFG-29: physical deletion, default-generation switch, bridge
  removal, and final integration.

## Batch Kind, Slice Risk, And Shape

- Batch kind: `migration`.
- Slice 1 risk: `migration`.
- Selected shape: `vertical`; no override is used.
- Approval gate: none beyond the existing CCFG-26/COR-009 scope and issue #61;
  the slice preserves supported execution behavior while moving one scenario to
  its permanent owner. Any contract narrowing or destructive cleanup requires a
  reviewed amendment and is not authorized here.

## One-Slice Decision

The command-owner contract, flight artifact, serialized execute caller,
transition/receipt mechanics, and behavioral proof form one vertical scenario.
Splitting schema declaration, authoring, runner consumption, or transition
would leave an inert or contradictory intermediate state that cannot complete
and resume one slice safely. Recovery, finalization, and closeout are separate
vertical scenarios with different start states and stop conditions, so they
remain later child batches.

Before implementation review, record a smaller-alternative analysis against
the actual diff. Stop for a reviewed amendment if the happy-path boundary grows
to include recovery, finalization, closeout, public phase-label migration, or
unrelated runner architecture.

## Scope Ceiling

Canonical planning surfaces:

- `../../CURRENT.md`
- `../../LEDGER.md`
- this batch's `dispatch.md`, `runway.md`, `review.md`,
  `completed-slices.md`, `execution-report.md`, and `closeout.md`

Candidate implementation surfaces:

- `skills/work-batch/**`
- `skills/batch-runway/**` remains read-only support in CCFG-26B; its displaced
  semantic ownership is narrowed only in CCFG-26E
- local-runner compatibility references under
  `skills/architecture-program-runway/references/`
- the exact runner launch, state, validation, transition, receipt/artifact, and
  phase-contract modules required for repeated fresh execute flights
- `skills/work-batch/references/batch-execution-flight-v1.schema.json`
- focused work-batch, runner, command-owner scenario, lifecycle, routing, and
  manifest tests and fixtures
- `docs/skill-routing-contract.md`, `docs/workflow-guide.md`, and `README.md`
  only when required to describe the migrated happy-path owner
- `codex-features.json`
- `CHANGELOG.md`

The exact allowed paths in the validated planning snapshot are the upper
ceiling, not a requirement to touch every path. No broad runner rewrite is
authorized.

## Validation Class

Use `project-harness-production`. Per-slice validation must prove the complete
queued-runway-to-durable-flight scenario, including a real fresh subprocess
boundary or a deterministic injected-process proof at that boundary. The
durable profile override keeps installed exact-commit acceptance final-only,
because it must bind a clean accepted commit; the per-slice substitute is the
implementation-created two-flight behavioral test plus the required-green
command-owner catalog validator. Candidate installation, stable-home comparison,
exact acceptance, and final independent review remain final batch gates.

## Cross-Checkout Contract

This batch explicitly uses `cross-checkout-context/v1` with stable toolchain and
canonical planning roots and the existing candidate implementation root. The
runway must preserve the complete helper-validated planning snapshot and exact
canonical planning root. It is historical plan-time evidence, not a live lease.

## Stop Conditions

- Stop if Planning State is not the sole semantic currentness gate.
- Stop if Git history, ancestry, fingerprints, path sets, or dirty files become
  queue or lifecycle authority instead of material-integrity evidence.
- Stop if `work-batch` does not own every proceed/stop and acceptance decision
  inside the happy-path flight.
- Stop if the runner, Batch Runway, or Architecture Program Runway can silently
  take back or bypass that decision ownership.
- Stop if the runner infers a slice result or next action rather than validating
  and mechanically consuming the exact `work-batch` flight result.
- Stop if one coordinator process executes more than one implementation slice.
- Stop if a fresh coordinator reloads full prior-slice chronology, raw logs,
  worker transcripts, or already accepted review detail outside the bounded
  input manifest.
- Stop if the durable receipt cannot determine the exact same-batch next action
  without chat history.
- Stop if per-flight token/compaction, diff-size, validation-breadth, support-
  agent/review-lens, duration, or blocker/recovery-transition evidence is
  overwritten or omitted rather than recorded with explicit nulls or empties.
- Stop if issue #59 recovery/advisor behavior, finalization, closeout,
  reconciliation, or successor selection enters this batch.
- Stop if the serialized phase identities change or a parallel runner/launcher,
  execution store, compatibility dialect, or fallback owner is introduced.
- Stop if CCFG-26C through CCFG-26E or later findings are selected, prepared,
  queued, or begun.
- Stop on any path outside the validated ceiling, unrelated dirt, failed strict
  cross-checkout validation, or a clearly oversized boundary without a reviewed
  smaller alternative.
