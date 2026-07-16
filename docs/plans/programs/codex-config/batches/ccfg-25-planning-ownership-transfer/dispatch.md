# CCFG-25 Planning Ownership Transfer Dispatch

## Selection

- Batch ID: `ccfg-25-planning-ownership-transfer`
- Batch state: `queued`
- Covered finding: CCFG-25, Transfer Planning Ownership to `plan-batch`
- Finding state entering the batch: `Open`
- Accepted source: COR-008 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`
- Planning-quality amendment:
  `../../findings/ccfg-25-planning-quality-amendment.md`
- Planning/execution carry-forward:
  `../../findings/command-owner-redesign-planning-execution-carry-forward.md`
- Planning-contract evidence:
  `../ccfg-21-planning-artifact-contracts/closeout.md`
- Behavioral-harness evidence:
  `../ccfg-23-behavioral-scenario-harness/closeout.md`
- Intake-cutover evidence:
  `../ccfg-24b-intake-ownership-cutover/closeout.md`
- Current runway: `runway.md`

## Selection Result

CCFG-24 is closed, the DEC-038 selection transaction is resolved, and no selected,
queued, or active batch exists. The explicit user request authorizes selection of
exactly CCFG-25. CCFG-26 through CCFG-29 remain deferred by dependency.

This dispatch was produced by the predecessor planning workflow because the target
`plan-batch` owner, `batch_planner`, and `batch_plan_reviewer` do not exist yet.
The batch must bootstrap those boundaries without preserving the predecessor
planning owners as permanent dependencies.

## Goal

Make `plan-batch` the sole owner of selection, scope shaping, dispatch, runway,
risk, approvals, validation-profile choice, and queue mutation. The default agent
must invoke a registered `batch_planner` and a separate read-only
`batch_plan_reviewer` directly, then apply the existing DEC-038 planning
transaction only after proportionality, currentness, approval, and independent
review gates are satisfied.

Remove Architecture Program Runway planning ownership and Batch Runway
`create-spec` semantic ownership in the same batch. Stop before implementation of
the newly queued runway and before CCFG-26 selection.

## Authoritative Invariants

- The default `plan-batch` command agent is the only queue mutator.
- `batch_planner` produces and corrects a non-executable draft only.
- `batch_plan_reviewer` is independently invoked, read-only, and cannot edit,
  select, queue, implement, or spawn agents.
- The planner cannot invoke, frame evidence for, or approve the reviewer.
- Every new or materially amended runway receives independent planning review.
- Queue mutation consumes the existing CCFG-21 artifact contracts and DEC-038
  transaction; no parallel store, transaction, queue, command, or executable draft
  format is introduced.
- Planning begins from the minimum viable change. Source-proposed mechanics are
  evidence, not mandatory topology unless explicitly approved as a contract.
- Slice count is derived from semantic boundaries. Filler decomposition is merged
  or rejected.
- A stale draft, unresolved user decision, blocked review, or unapproved residual
  complexity remains non-executable and cannot mutate queue state.
- Planning State `current` and `validate` remain the semantic source of selected,
  queued, and active currentness.
- Planning stops before implementation and closeout never selects a successor.

## Proportionality

```yaml
proportionality:
  observed_failure: >-
    plan-batch is only a thin human-facing router; APR still owns selection,
    dispatch, and queue preparation, while Batch Runway owns create-spec planning.
    The candidate has no installed planner/reviewer gate or command-owned use of
    the resolved selection transaction.
  invariants:
    - one human-facing plan-batch command owner
    - one queue mutator
    - independent planner and reviewer roles
    - existing planning artifact schemas and DEC-038 transaction
    - topology-independent behavioral proof
    - stop before implementation
    - same-work removal of replaced planning owners
  minimum_viable_change: >-
    Add one installed plan-batch command boundary that accepts current ledger and
    Planning State facts, invokes the two registered planning roles, validates
    proportionality and review results, and applies the existing selection
    transaction; then remove the displaced APR and Batch Runway planning routes.
  proposed_change: >-
    Implement the minimum owner boundary, migrate behavioral scenarios and callers
    to it, remove legacy planning ownership, and converge candidate installation
    and COR-008 acceptance.
  additions_beyond_minimum:
    - >-
      Two registered agent TOMLs are required by the accepted independent-role
      contract; they introduce no new lifecycle or persistent planning store.
    - >-
      One command-owned deterministic script boundary is required to validate
      collaborator results and invoke the existing transaction without moving
      semantic decisions into planning-contract storage.
  simpler_alternatives_rejected:
    - >-
      Prose-only skill changes cannot prove queue ownership, stale-draft refusal,
      fault recovery, or installed-owner behavior.
    - >-
      Keeping APR or Batch Runway as a hidden planning service would violate the
      zero-legacy-owner acceptance condition.
    - >-
      A separate preparation slice for agent scaffolding was rejected because the
      roles have no independently supported outcome outside the complete owner
      boundary and would create transient machinery.
  verdict: proportionate
```

No residual material complexity requires user approval at planning time. Any new
state, schema, public mode, compatibility layer, or second transaction discovered
during execution is outside this verdict and blocks for explicit replanning.

## Explicitly Included

1. One installed `plan-batch` owner boundary that:
   - consumes current Planning State facts and one existing ledger row or current
     selected state;
   - directly invokes registered `batch_planner` and `batch_plan_reviewer` roles;
   - validates exact draft/review provenance, proportionality, user approvals,
     stale lineage, and unresolved decisions;
   - applies the existing planning artifact writers and DEC-038 transaction only
     after the gate is clean;
   - produces at most one runnable queued runway and stops before implementation.
2. Target-behavior migration for all CCFG-23 planning and planning-quality
   scenarios, including partial-failure recovery and exact replay.
3. Removal of APR grouping, ranking, selection, dispatch, and queue-preparation
   ownership and every normal `plan-batch` dependency on it.
4. Removal of Batch Runway `create-spec` mode and semantic planning ownership while
   preserving CCFG-26 execution, recovery, validation, review, finalization, and
   closeout support.
5. Candidate feature wiring, installed agent registration, focused docs/tests, and
   final COR-008 plus planning-quality acceptance.

## Explicitly Deferred

- CCFG-26 execution and closeout ownership transfer.
- Removal of Batch Runway `execute-spec` or APR same-batch closeout/reconciliation
  support still owned by CCFG-26.
- Default-generation switch, cutover rehearsal, bridge deletion, candidate merge,
  and CCFG-27 through CCFG-29.
- Any new planning schema, transaction version, persistent draft store,
  proportionality artifact type, complexity score, retry identity, or lifecycle
  state.
- Any new intake capability or change to `add-to-ledger/v1` or `ledger-store/v1`.
- Any successor dispatch or runway.

## Batch Kind And Slice Shape

- Batch kind: `mixed-risk`.
- Slice 1: `migration` — implement and candidate-install the complete
  `plan-batch` owner, registered planning roles, independent review gate, and
  DEC-038 queue transaction; bind target planning scenarios to the installed
  owner.
- Slice 2: `contract-narrowing` — remove APR planning ownership and Batch Runway
  `create-spec` ownership, migrate remaining callers and tests, and preserve only
  CCFG-26 responsibilities.
- Slice 3: `migration` — converge feature wiring, isolated installation, exact
  behavioral acceptance, docs, and final COR-008 evidence.

`1 -> 2`: Slice 1 creates a valid installed replacement owner with green behavioral
proof before public planning ownership is physically removed. This is the required
rollback and deletion-evidence boundary.

`2 -> 3`: Slice 2 establishes the final owner topology. Slice 3 uses a different
validation environment and acceptance boundary: clean candidate installation,
full exact-commit scenario evidence, manifest convergence, and range-wide review.

## Approval Gates

- Slice 1 must not queue fixture work until planner/reviewer result contracts,
  independent invocation evidence, proportionality, stale-draft refusal, and exact
  DEC-038 recovery are green.
- Slice 2 may narrow or delete a legacy planning surface only after a current
  caller inventory names its replacement, preserves every CCFG-26 responsibility,
  and proves target scenarios no longer depend on APR, Batch Runway, `create-spec`,
  or fixture-only planning ownership.
- Any newly discovered unclassified deletion, contract narrowing, schema change,
  public mode, or compatibility bridge blocks the affected slice for replanning.

## Cross-Checkout Context

- Interface: `cross-checkout-context/v1`
- Stable toolchain and canonical planning repository:
  `/home/alacasse/projects/codex-config`
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Stable Codex home: `/home/alacasse/.codex`
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`
- Stable planning baseline: `31d228d4ef9b94e2ccad0f5260670593ea9469f9`
- Candidate implementation baseline:
  `91179e84c7cfed666be224575db7000ca0ea01b3`

Every execution startup and delegated handoff requires a fresh ready strict
preflight and exact write scope. Candidate code and installed candidate agents
must not mutate canonical planning state.

## Validation And Review

- Runway density: `full-runway` because this changes command ownership, public
  workflow routing, installed agents, and destructive legacy boundaries.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`
- Every slice receives independent `runway_reviewer` review.
- Every test-changing slice receives delta-only `test-quality-review`.
- Slices 1 and 2 receive `import_topology_reviewer` review.
- Slice 2 and the final range receive targeted `dead-surface-audit` evidence.
- Final acceptance must use the CCFG-33 single evidence-pytest process and exact
  candidate commit.

## Closeout Contract

Successful closeout must:

- prove all COR-008 and planning-quality acceptance keys;
- mark CCFG-25 `Closed`;
- leave `plan-batch` as the only planning decision and queue owner;
- leave zero runtime or semantic dependency on APR planning ownership or Batch
  Runway `create-spec`;
- leave APR and Batch Runway only with named CCFG-26 responsibilities and removal
  conditions;
- record exact removed and preserved surfaces, candidate range, installation
  links, transaction recovery, scenario evidence, reviews, and cost evidence;
- clear selected, queued, and active same-batch state;
- stop without selecting, dispatching, or preparing CCFG-26.

## Stop Conditions

- Stop if the work needs a new planning schema, store, transaction, executable
  draft format, queue owner, public command, lifecycle state, or compatibility
  layer.
- Stop if planner and reviewer independence cannot be proven from direct default
  agent invocation and independently supplied evidence.
- Stop if queue mutation can occur before a clean exact-draft review and resolved
  proportionality/user-decision gate.
- Stop if target scenarios retain APR, Batch Runway, `create-spec`, exact prompt
  prose, stable-only paths, or fixture-only planning ownership.
- Stop if APR or Batch Runway CCFG-26 execution/closeout responsibilities would be
  removed or narrowed.
- Stop on stable-home mutation, candidate canonical write, strict-context mismatch,
  unexpected implementation movement, or unclassified dirty-file conflict.
- Stop if CCFG-25 cannot close without entering CCFG-26 through CCFG-29.
