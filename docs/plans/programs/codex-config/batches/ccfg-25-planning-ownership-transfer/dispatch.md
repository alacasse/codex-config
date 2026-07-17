# CCFG-25 Planning Ownership Transfer Dispatch

## Selection

- Batch ID: `ccfg-25-planning-ownership-transfer`
- Batch state: `selected`
- Planning gate: `blocked-before-queue`
- Covered finding: CCFG-25, Transfer Planning Ownership to `plan-batch`
- Finding state entering the batch: `Open`
- Source program ledger: `../../LEDGER.md`
- Expected runway path: `runway.md`
- Current runway status: non-executable amended draft

CCFG-24 is closed and the explicit user request selects exactly CCFG-25. CCFG-26
through CCFG-29 remain deferred by dependency. Queue mutation is blocked until the
strict planning context is validated with the installed helper and an independent
planning reviewer returns `clean` against the exact amended draft.

## Authoritative Sources

- COR-008 at `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- `../../findings/ccfg-25-planning-quality-amendment.md`.
- `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- `../ccfg-21-planning-artifact-contracts/closeout.md`.
- `../ccfg-23-behavioral-scenario-harness/closeout.md`.
- `../ccfg-24b-intake-ownership-cutover/closeout.md`.

## Goal

Make `plan-batch` the sole owner of selection, scope shaping, dispatch, runway,
risk, approvals, validation-profile choice, and queue mutation. The default agent
must directly invoke a registered `batch_planner` and an independent read-only
`batch_plan_reviewer`, then apply the existing DEC-038 transaction only after
currentness, proportionality, approval, exact-draft review, and lineage gates pass.

Remove Architecture Program Runway planning ownership and Batch Runway
`create-spec` ownership in the same batch. Preserve every execution and closeout
responsibility reserved for CCFG-26. Stop before implementation of any newly
queued runway and before successor selection.

## Authoritative Invariants

- The default `plan-batch` command agent is the only queue mutator.
- `batch_planner` produces and corrects a non-executable draft only.
- `batch_plan_reviewer` is directly and independently invoked, read-only, and
  cannot edit, select, queue, implement, delegate, or spawn agents.
- The planner cannot invoke, select evidence for, frame, or approve the reviewer.
- Every new or materially amended runway receives independent planning review.
- Queue mutation consumes the existing CCFG-21 schemas, artifact writers, and
  DEC-038 transaction; no parallel store, queue, transaction, or executable draft
  format is introduced.
- Planning begins from the minimum viable change and derives slice count from
  semantic boundaries.
- Stale drafts, unresolved user decisions, blocked review, and unapproved residual
  complexity remain non-executable.
- Planning State `current` and `validate` remain the semantic currentness authority.
- Planning stops before implementation; closeout selects no successor.

## Proportionality

```yaml
proportionality:
  observed_failure: >-
    plan-batch is a thin router while Architecture Program Runway still owns
    selection, dispatch, and queue preparation and Batch Runway owns create-spec
    planning. The candidate lacks an installed command owner and independent
    planner/reviewer gate over the resolved DEC-038 transaction.
  invariants:
    - one human-facing plan-batch command owner
    - one queue mutator
    - independent planner and reviewer roles
    - existing planning artifact schemas and DEC-038 transaction
    - topology-independent behavioral proof
    - same-work removal of replaced planning owners
    - preservation of all CCFG-26 execution and closeout behavior
    - stop before implementation and successor selection
  minimum_viable_change: >-
    Add one installed plan-batch command boundary that consumes current ledger and
    Planning State facts, directly invokes the two registered planning roles,
    validates proportionality and exact-draft review results, applies the existing
    selection transaction, and then removes the displaced APR and Batch Runway
    planning routes.
  proposed_change: >-
    Implement that owner boundary, migrate planning scenarios and existing callers
    to it, remove only displaced planning ownership, and converge candidate
    installation and COR-008 acceptance.
  additions_beyond_minimum:
    - addition: two registered agent TOMLs
      prevents: planner self-review and ambiguous role authority
      why_minimum_is_insufficient: >-
        The accepted contract requires independently registered planner and reviewer
        roles; prose or one shared role cannot prove independent invocation.
    - addition: one deterministic scripts/plan_batch.py boundary
      prevents: semantic decisions leaking into the apply-only store and queue writes before exact review
      why_minimum_is_insufficient: >-
        The default agent needs one mechanically testable boundary for result,
        lineage, approval, and DEC-038 input validation without copying store logic.
    - addition: transfer the unchanged cross-checkout helper installation link to the existing planning-state feature
      prevents: plan-batch retaining Batch Runway solely to receive a mechanical helper
      why_minimum_is_insufficient: >-
        Both plan-batch and work-batch already require Planning State. Leaving the
        link with Batch Runway preserves a forbidden planning dependency; duplicating
        it or adding a new shared feature would create more topology.
    - addition: rewire the existing architecture program runner planning phase to the public plan-batch command
      prevents: the runner remaining a second selection and create-spec owner
      why_minimum_is_insufficient: >-
        Removing APR prose alone leaves a live caller bypass. Reusing the existing
        public command path removes that bypass without adding a protocol or planner.
  simpler_alternatives_rejected:
    - Prose-only edits cannot prove installed ownership, stale-draft refusal, fault recovery, or queue gating.
    - Keeping APR or Batch Runway as a hidden planning service violates the zero-legacy-owner acceptance boundary.
    - Duplicating the helper link or adding a shared bridge feature creates more installation ownership than moving the unchanged link once.
    - A separate planner/reviewer scaffolding slice has no independently supported outcome.
  verdict: proportionate
```

No residual material complexity currently requires user approval. Any new state,
schema, public mode, compatibility layer, second transaction, or materially larger
runner/helper redesign is outside this verdict and blocks for replanning.

## Included Scope

- Complete installed `plan-batch` command owner, deterministic transaction gate,
  and registered planner/reviewer roles.
- Exact selected-dispatch and draft/review lineage, proportionality, approval,
  currentness, stale-draft, correction-loop, and unresolved-decision gates.
- Target planning and planning-quality scenarios bound to the installed owner.
- Removal of APR grouping, ranking, prioritization, selection, dispatch, runway,
  and queue-preparation ownership.
- Removal of Batch Runway `create-spec` mode and semantic planning ownership.
- Existing architecture program runner planning-phase rewiring to `plan-batch`.
- One unchanged helper-link ownership transfer to Planning State, with no helper
  semantic change.
- Candidate feature/agent installation and complete COR-008 acceptance.

## Deferred And Preserved Scope

CCFG-26 remains unselected and owns the future transfer of all proceed/stop,
recovery, delegation, validation acceptance, implementation review, commit,
receipt, finalization, closeout, and same-batch reconciliation decisions.

Until CCFG-26 closes, this batch must preserve:

- APR closeout and same-batch program reconciliation support;
- Batch Runway proceed/stop, slice delegation, recovery, validation, review,
  commit and receipt handling, execution-ledger maintenance, finalization,
  closeout support, and cross-checkout execution safety;
- `work-batch`, execution agents, execution contracts, and same-batch no-successor
  behavior.

Also deferred:

- CCFG-27 through CCFG-29, default-generation switching, candidate merge, cutover
  rehearsal, and bridge deletion;
- planning schema, DEC-038, `ledger-store/v1`, Planning State semantic, intake, or
  projection changes;
- any new command, lifecycle state, persistent draft store, retry identity,
  compatibility layer, or successor artifact.

## Slice Shape

- Slice 1 — `migration`: implement and install the complete replacement owner and
  bind target planning scenarios while legacy owners remain available only as a
  rollback baseline.
- Slice 2 — `contract-narrowing`: remove displaced APR and Batch Runway planning
  ownership, rewire the existing runner, and preserve the complete CCFG-26
  inventory above.
- Slice 3 — `migration`: converge the final installation and exact acceptance.

`1 -> 2`: Slice 1 creates an independently exercisable installed planning path and
rollback point before contract narrowing.

`2 -> 3`: Slice 2 creates the final semantic topology; Slice 3 validates a clean
installation and exact final commit through a distinct environment/review gate.

## Queue Gate

Queue mutation is forbidden until all of the following are true:

1. the installed `/home/alacasse/.codex/scripts/cross_checkout_context.py` helper
   validates the complete strict payload and canonical planning root recorded in
   the amended runway;
2. the selected dispatch identity and content hash remain current;
3. the independent planning reviewer receives this selected dispatch, source
   evidence, user constraints, Planning State facts, proportionality record, and
   exact amended draft and returns `clean`;
4. no unresolved user decision or unapproved residual complexity remains; and
5. DEC-038 atomically transitions the same selected scope to exactly one queued
   runway.

The current `runway.md` is draft evidence only. It is not executable by
`work-batch` while this gate is blocked.

## Stop Conditions

- Stop on missing or mismatched strict-context validation.
- Stop if the amended plan review is not clean or is bound to another dispatch or
  draft hash.
- Stop if target scenarios depend behaviorally on APR, Batch Runway,
  `create-spec`, exact prompt prose, stable-only paths, or fixture-only ownership.
  Historical or negative vocabulary alone is not a dependency.
- Stop if any CCFG-26 responsibility named above would be removed or narrowed.
- Stop if work needs a new schema, store, transaction, command, lifecycle state,
  persistent draft store, compatibility layer, helper behavior, or runner protocol.
- Stop on stable-home mutation, candidate canonical write, unexpected repository
  movement, or unclassified dirty-file conflict.
- Stop if CCFG-25 cannot close without selecting or entering CCFG-26 through
  CCFG-29.
