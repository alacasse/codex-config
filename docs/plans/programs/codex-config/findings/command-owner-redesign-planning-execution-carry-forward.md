# Command-Owner Redesign Planning And Execution Carry-Forward

## Authority And Scope

The accepted command-owner redesign snapshot at
`caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` remains immutable. This document is
the live implementation amendment on `master` for existing CCFG-23 through
CCFG-29 work; it is not a new finding.

CCFG-21 has completed the candidate planning-artifact and selection-transaction
contracts. Stable master has also completed the semantic slice correction from
GitHub #54 and the cross-checkout currentness correction from CCFG-32 / GitHub
#55. The target command-owner generation must carry those decisions forward as
behavior and ownership, without preserving stable-only helper topology.

## CCFG-23 — Topology-Independent Behavioral Harness

Add observable target-behavior scenarios for the following requirements.

### Planning quality

- A cohesive one-slice plan is valid, and planning begins from the minimum
  viable change.
- Every multi-slice boundary has a semantic reason; filler slices are rejected
  or merged.
- Source-proposed implementation topology can be narrowed when it is not an
  authoritative contract.
- Unjustified expansion blocks before queue mutation. Residual material
  complexity requires explicit, narrowly scoped user approval.
- The default command owner invokes `batch_planner` and
  `batch_plan_reviewer` independently. The planner cannot invoke, frame
  evidence for, or approve its own reviewer.
- Stale drafts and unresolved user decisions cannot become executable queue
  state.

### Execution currentness

- Planning State `current` and `validate` are the sole semantic authority for
  selected, queued, and active batch currentness. Stale or invalid Planning
  State stops before mechanical helper invocation.
- Git is used only for material execution integrity: exact diff bases, accepted
  commits, rollback, and movement during lease preparation.
- Git history, changed-path sets, fingerprints, ancestry, and dirty files are
  not interpreted as batch lifecycle or queue-transaction semantics.
- Green Planning State plus an unchanged implementation baseline can refresh
  live context even when stable planning or toolchain `HEAD` advanced.
- Unexpected implementation movement and movement during live-context
  preparation block.
- Fresh per-handoff leases, result echo, write-scope validation, receipts, and
  exact reviewer diff bases remain protected.

### Cutover lifecycle

- Before candidate cutover, the candidate generation can operate the minimum
  temporary bridge needed for the post-cutover path while master remains the
  canonical planning authority.
- After final integration, the bridge is physically absent and no target
  behavior depends on its legacy topology.

These scenarios must test target behavior. They must not require old APR,
Batch Runway, exact prompt prose, stable-only paths, or historical helper
topology.

## CCFG-25 — Planning Ownership Transfer

CCFG-21 has resolved the planning artifact and selection transaction
dependency. CCFG-25 waits on CCFG-24 and consumes the completed CCFG-21
contracts and transaction owner; it must not invent another planning store,
queue transaction, or executable draft format.

CCFG-25 must:

- implement the substantive requirements from GitHub #51, #52, and #54;
- keep the default `plan-batch` command agent as the only queue mutator;
- invoke a registered `batch_planner` directly and invoke a separate registered
  read-only `batch_plan_reviewer` directly;
- prevent the planner from invoking, framing evidence for, or approving its own
  reviewer;
- require compact proportionality evidence before queue mutation;
- treat proposed source mechanics as evidence rather than mandatory topology
  unless explicitly approved as a contract;
- derive slice count from semantic boundaries, starting from one slice;
- preserve non-executable draft evidence on findings or blocked review; and
- remove APR planning ownership and Batch Runway create-spec ownership in the
  same transfer.

GitHub #54 is complete on stable master, but its target planning semantics
remain CCFG-25 acceptance. GitHub #51 and #52 remain open until CCFG-25
implements and validates them.

## CCFG-26 — Execution And Closeout Ownership Transfer

CCFG-26 must implement:

- Planning State `current` and `validate` as the sole semantic execution
  currentness gate;
- `work-batch` ownership of proceed, stop, recovery, delegation, validation,
  review, commit, receipt, closeout, and same-batch reconciliation decisions;
- Git as material-integrity evidence only, with no Git-log, path-set,
  fingerprint, ancestry, or dirty-file inference of batch lifecycle or queue
  semantics;
- first-handoff implementation-baseline validation;
- exact accepted-action movement and refreshed leases for later handoffs;
- exact reviewer diff bases;
- ordinary target-policy handling for branch checks and ordinary
  scope-conflict handling for dirty files; and
- removal of dependencies on APR closeout and Batch Runway execute-spec
  ownership in the same transfer.

These are required behaviors and ownership boundaries. The stable helper's
current internal topology is not the prescribed permanent target.

## CCFG-27 — Cutover Preparation And Rehearsal

Candidate readiness requires the candidate generation to contain the minimum
temporary cross-checkout bridge functionality needed after cutover. Master
remains the canonical planning authority until CCFG-29.

The rehearsal must prove:

- candidate-installed helper and workflow wiring validate the explicit
  master-planning / candidate-implementation topology;
- candidate agents and result contracts carry the required strict identity;
- the candidate can perform a read-only or fixture-owned post-cutover
  cross-checkout workflow;
- no stable legacy command owner is required for candidate-controlled target
  execution;
- the bridge remains explicitly temporary and owned for deletion by CCFG-29;
  and
- no extra compatibility layer or parallel bridge version is introduced.

This is a future target requirement. This amendment does not port the bridge
now; CCFG-27 owns that later candidate-readiness work.

## CCFG-28 — Final Cutover

The final switch requires all of the following:

- CCFG-27 temporary bridge parity and rehearsal remain green;
- the clean candidate installation includes the temporary bridge surfaces
  needed for the post-cutover path to CCFG-29;
- a fresh candidate-bound diagnostic proves it can read master canonical
  planning state without making an unauthorized canonical write; and
- the candidate can execute the later CCFG-29 convergence workflow.

The switch must not occur if any gate fails. The temporary bridge is not a
permanent target owner and remains present only until CCFG-29 deletes it.

## CCFG-29 — Convergence And Final Integration

CCFG-29 must:

- merge the candidate implementation into the latest authoritative master,
  rather than relying on ad hoc cherry-picks of stable-control history;
- preserve the target behaviors introduced through CCFG-23, CCFG-25, and
  CCFG-26;
- verify integrated master contains one contract-first planning and execution
  dialect;
- remove the temporary strict and pre-creation bridge helpers, workflow
  references, feature wiring, tests, and installation routes after they are no
  longer needed;
- remove both retained temporary live-context APIs,
  `preflight_cross_checkout_live_lease(...)` and
  `prepare_cross_checkout_context_refresh(...)`, with the bridge;
- rebind the default Codex home to integrated master; and
- leave no candidate/stable compatibility wrapper solely to preserve CCFG-30,
  CCFG-31, or CCFG-32 topology.

## Planning State

- Selected dispatch: `None`
- Queued batch: `None`
- Active runway: `None`
- Successor selected: no
- Next eligible command-owner redesign work under existing dependencies:
  CCFG-22, still unselected

This amendment changes future acceptance and sequencing context only. It does
not select, dispatch, queue, activate, implement, close, or prepare any work.
