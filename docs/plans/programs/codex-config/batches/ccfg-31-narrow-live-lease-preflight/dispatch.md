# CCFG-31 Narrow Live-Lease Preflight Dispatch

## Selection

- Batch ID: `ccfg-31-narrow-live-lease-preflight`
- Source ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-31, Narrow ready/blocked live-lease preflight.
- Source packet:
  `docs/plans/programs/codex-config/findings/github-issue-53-narrow-live-lease-preflight.md`
- Authoritative external evidence:
  [GitHub issue #53](https://github.com/alacasse/codex-config/issues/53),
  open and labeled `ready-for-agent` when selected on 2026-07-14.
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-31-narrow-live-lease-preflight/runway.md`

## Goal And Owner Seam

Replace the broad CCFG-30 startup protocol with one mechanical live-lease
preflight whose normal coordinator-visible result is exactly `ready` or
`blocked`. Preserve strict parsing, fresh per-handoff leases, post-lease
movement rejection, write-scope validation, result echo, and honest receipts.

`scripts/cross_checkout_context.py` owns mechanical identity and movement
proof. `work-batch` owns planning currentness and every proceed, stop, recovery,
delegation, commit, receipt, and closeout decision. The temporary shared bridge
contract remains canonical until CCFG-29 deletes the bridge.

## Batch Boundary

- Batch kind: `mixed-risk`.
- Slice 1 risk: `migration`; introduce and behaviorally prove the narrow
  mechanical preflight while preserving the existing strict per-handoff helper.
- Slice 2 risk: `contract-narrowing`; migrate consumers and delete the broad
  classification, path-review, prose, and topology-test protocol.
- Approval gate: GitHub issue #53 is the repo-owner-authored deletion and
  simplification authorization and is labeled `ready-for-agent`. Before
  execution, Planning State must still report this exact runway as the sole
  queued or active batch and no amendment, supersession, abandonment, or issue
  change may have withdrawn that authorization.
- Dependencies: none.
- Validation class: `project-harness-production` using temporary Git repository
  tests, lifecycle guards, manifest/installation routing checks, Ruff,
  basedpyright, and `git diff --check`.
- Execution topology: ordinary single-root work in this repository. Editing the
  temporary bridge contract does not make this batch a strict cross-checkout
  handoff and does not require a planning snapshot.

## Slice Shape

`slice_shape`: two slices. `1 -> 2` is a producer/consumer boundary: Slice 1
adds the narrow helper preflight beside the still-required strict per-handoff
refresh operation and proves it in temporary repositories, leaving a valid and
testable intermediate. Slice 2 consumes that preflight, removes the old broad
protocol and test-retained topology, and updates the installed surfaces. No
third boundary is justified; this stays within the issue's explicit maximum.

## Guardrails

- Keep the normal result to exactly three fields: `status: ready | blocked`,
  diagnostic `reason`, and `live_context`, which contains a strictly parsed
  context for `ready` and is `null` for `blocked`.
- Remove the three movement classifications, general compatible-range review,
  broad controlled-path derivation, startup reconciliation as a separate
  lifecycle concept, duplicated full lifecycle prose, and non-behavioral
  wording/topology assertions.
- Do not weaken the strict parser, fresh worker/reviewer lease rule,
  post-preparation movement rejection, result echo, write-scope validation, or
  accepted-action receipt evidence.
- Do not add a parallel bridge version, compatibility taxonomy, repository
  scanner, public command, agent, lifecycle state, durable planning artifact,
  planning schema, or generalized future-change engine.
- Historical CCFG-30 artifacts are read-only. CCFG-21 through CCFG-29, the
  command-owner redesign candidate, installation mutation, generation switch,
  and bridge deletion are excluded.
- CCFG-29 remains the sole bridge-removal owner.
- Preserve unrelated dirty files and exclude them from staging, cleanup,
  rewrites, and commits.

## Deferred Findings

- CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11 remain open or backlog work
  outside this batch.
- CCFG-21 through CCFG-28 remain sequenced redesign work outside this stable
  simplification.
- CCFG-29 alone owns final bridge removal and integration.
- CCFG-30 remains closed historical evidence and must not be reopened or
  rewritten.

## Stop Conditions

Stop before implementation if the selected scope is stale; the deletion
approval is withdrawn; the work needs more than the two declared boundaries;
strict per-handoff safety would weaken; arbitrary movement could become
`ready`; a second bridge or compatibility path appears; project-specific values
would enter reusable skills; or historical/candidate/out-of-scope paths would
need modification.
