# CCFG-26 Work-Batch Owner Transfer Dispatch

## Selection

- Batch ID: `ccfg-26-work-batch-owner-transfer`
- Selection outcome: `selected for exact planning review`
- Queue target: exactly one `queued` runway after a clean independent review
- Covered finding: CCFG-26, Transfer Execution and Closeout Ownership to
  `work-batch`
- Finding state entering the batch: `Ready`
- Source program ledger: `../../LEDGER.md`
- Expected runway path: `runway.md`
- Planning root: `../../../..`
- Canonical planning repository:
  `/home/alacasse/projects/codex-config`
- Candidate implementation target:
  `/home/alacasse/projects/codex-config-command-owner-redesign`

Planning State `current` and `validate` reported an idle, valid program with no
selected dispatch, queued batch, active runway, blocker, or obligation. This
explicit `plan-batch CCFG-26` request selects only CCFG-26. CCFG-27 through
CCFG-29 and every older open row remain unselected.

## Authoritative Sources

- CCFG-26 and its batch queue in `../../LEDGER.md`.
- COR-009 at accepted design snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- `../../../../../adr/0004-single-generation-command-owner-development-boundary.md`.
- `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- `../../findings/slice-shape-policy-direction.md`.
- `../../notes/stable-runway-dogfooding-policy.md`.
- `../ccfg-26-slice-shape-policy-correction/closeout.md` and
  `../ccfg-26-slice-shape-policy-correction/post-closeout-correction.md`.
- Direct candidate inspection at
  `5c5ec9d52dd9033daa45f3a200031c152363b62c`.

The superseded CCFG-26 execution-state foundation, CCFG-26B, ADR 0003, and
their design/review artifacts are historical evidence only. They do not select
the batch, prescribe the target architecture, authorize a resume, or define
the slice sequence.

## Current Candidate Seam

At the inspected candidate commit:

- `skills/work-batch/SKILL.md` owns user intent and stop boundaries but routes
  execution through `skills/batch-runway/` and reconciliation through
  `skills/architecture-program-runway/`.
- Batch Runway owns slice execution, recovery, validation/review loops, commits,
  receipts, execution-ledger updates, completed-slice movement, and finalization.
- Architecture Program Runway owns closeout disposition and same-batch program
  reconciliation.
- `agents/runway_worker.toml` and `agents/runway_reviewer.toml` own their exact
  result schemas but still name Batch Runway and retain a Batch Runway v1 path.
- `codex-features.json` makes installed `work-batch` depend on both broad legacy
  owners.
- The topology-independent execution, currentness, closeout, and fault scenarios
  exist only through fixture adapters; there is no installed
  `scripts/work_batch.py` owner.
- `scripts/planning_contract.py` and `scripts/planning_state.py` already provide
  narrow artifact/store and closeout-evidence mechanisms. CCFG-26 consumes them;
  it does not create another planning store or canonical Batch Execution State.

## Goal

Make installed `work-batch` the sole owner of:

- Planning State-gated execution currentness;
- proceed, stop, delegation, recovery, and resume decisions;
- validation execution and acceptance;
- independent review coordination and exact review bases;
- commits and receipts;
- execution-ledger and completed-slice progression;
- final validation and closeout artifact production; and
- same-batch program reconciliation with no successor selection.

Remove normal `work-batch` dependencies on Batch Runway execution ownership and
Architecture Program Runway closeout ownership in the same batch. Preserve
narrow reusable planning-contract, Planning State, Planning Artifacts, strict
cross-checkout, and registered-agent mechanisms without copying their rules.

The candidate implementation proves the target owner in fixtures and isolated
candidate installations. Under ADR 0004, the stable generation still controls
and closes this real development batch; the candidate controller does not
control its own implementation batch and does not mutate canonical planning.

## Batch Kind, Slice Risk, And Approval

- Batch kind: `migration`.
- Slice 1 risk: `migration`.
- Slice 2 risk: `migration`.
- Slice 3 risk: `migration`.
- Slice 4 risk: `migration`.
- Selected shape for every slice: `vertical`; no project-policy override is
  used.
- Approval gate: COR-009, the canonical `Ready` CCFG-26 row, ADR 0004, the
  completed slice-shape behavior, and this explicit user request authorize the
  ownership transfer and removal of displaced execution/closeout ownership.
- The gate does not authorize a new execution-state database/file, cross-
  generation runtime communication, a candidate canonical write, a default-
  generation switch, physical deletion owned by CCFG-28, bridge deletion owned
  by CCFG-29, or successor selection.

## Proportionality

```yaml
proportionality:
  observed_failure: >-
    work-batch remains a thin router while Batch Runway owns execution and
    Architecture Program Runway owns closeout reconciliation. The installed
    candidate has no deterministic work-batch owner even though target behavior
    scenarios and narrow planning mechanisms already exist.
  minimum_viable_change: >-
    Add one installed work-batch/v1 owner, migrate one complete accepted-slice
    scenario, extend that owner through recovery and finalization, then transfer
    same-batch reconciliation and remove normal callers of both displaced owners.
  proposed_change: >-
    Four vertical slices, each leaving an independently usable workflow state:
    accepted clean execution; recovery/currentness; finalization and closeout
    production; same-batch reconciliation and caller cutover.
  smaller_alternatives_rejected:
    - Wrapping Batch Runway and APR behind work-batch leaves duplicate semantic owners.
    - Rebinding fixture scenarios without an installed owner proves no command boundary.
    - Documentation or path moves alone leave behavior under the old owners.
    - A new execution-state file duplicates runway, completed-slice, closeout, and receipt facts.
    - Three slices couple closeout production with partial-reconciliation recovery and weaken rollback isolation.
    - Horizontal worker, validator, reviewer, commit, and documentation slices produce no independently usable workflow checkpoint.
  larger_alternatives_rejected:
    - Physical APR and Batch Runway deletion belongs to CCFG-28.
    - Runner phase-model migration belongs to CCFG-27.
    - Cross-checkout bridge deletion and final integration belong to CCFG-29.
  verdict: proportionate
```

No residual material complexity requires another user decision. Discovery of a
new public command, store, lifecycle state, schema family, cross-generation
runtime protocol, or broader runner redesign blocks this plan for replanning.

## Semantic Slice Shape

1. Accepted-slice execution through installed `work-batch`.
2. Recovery, currentness, and legacy-state refusal through the same owner.
3. Final validation and durable closeout production through the same owner.
4. Same-batch reconciliation and caller cutover.

`1 -> 2`: Slice 1 creates a valid clean-path owner and rollback checkpoint;
Slice 2 adds the distinct failure/recovery risk without weakening that path.

`2 -> 3`: Slice 2 leaves normal and interrupted slices executable end to end;
Slice 3 consumes their durable receipts and completed-slice evidence to add a
separate batch-finalization boundary.

`3 -> 4`: Slice 3 produces a lineage-bound closeout while APR still applies
reconciliation. Slice 4 transfers the different canonical-current/ledger
mutation boundary and removes the normal legacy callers.

Final installation, exact-commit acceptance, and range review are batch gates,
not a fifth implementation slice.

## Scope Ceiling

Canonical planning surfaces:

- `../../CURRENT.md`
- `../../LEDGER.md`
- this batch's `dispatch.md`, `runway.md`, `review.md`,
  `completed-slices.md`, conditional blocked-slice `execution-report.md`, and
  `closeout.md`

Candidate implementation surfaces:

- `skills/work-batch/**`
- `scripts/work_batch.py`
- `agents/runway_worker.toml`
- `agents/runway_reviewer.toml`
- displaced execution/closeout ownership under `skills/batch-runway/**` and
  `skills/architecture-program-runway/**`
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_change_allowance.py`
- `scripts/command_owner_scenarios.py` only when a focused failing target-owner
  scenario proves the harness entrypoint itself needs adjustment
- `docs/skill-routing-contract.md`, `docs/workflow-guide.md`, and `README.md`
- `codex-features.json` and `CHANGELOG.md`
- the exact focused tests and command-owner fixture adapters listed in
  `runway.md`

`scripts/planning_contract.py`, `scripts/planning_state.py`, planning schemas,
and runner state/transition/validation modules are read-only mechanisms for this
batch. A demonstrated need to change their semantics is a stop condition and
requires reviewed replanning.

## Validation Class

Use `project-harness-production`. Per-slice validation is focused on the
scenario owned by that slice. Exact-commit acceptance, fresh and isolated
candidate installation, stable-home comparison, full relevant validation, and
final independent review remain final batch gates.

The current focused candidate baseline is 70 passed, 16 subtests passed, and
one known-red wording assertion in
`tests/test_batch_lifecycle_guards.py::BatchLifecycleGuardTests::test_architecture_program_closeout_rejects_dispatch_runway_only_evidence`.
Slice 4 owns replacing that transitional APR-topology assertion with target
`work-batch` behavior and promoting the command to required-green.

## Stop Conditions

- Stop on missing or mismatched strict cross-checkout context, canonical
  planning root, implementation baseline, or write scope.
- Stop if the candidate controller controls, executes, finalizes, or closes this
  real CCFG-26 development batch.
- Stop on any new canonical Batch Execution State, production
  `execution-state.json`, cross-generation runtime state, synchronization, or
  self-hosting behavior.
- Stop if Planning State loses sole semantic currentness authority or Git is
  used to infer queue/batch lifecycle.
- Stop if worker/reviewer results still depend on a Batch Runway path after the
  accepted-slice transfer.
- Stop if a displaced Batch Runway or APR semantic owner remains a normal
  `work-batch` dependency after Slice 4.
- Stop if old-format active state is silently mutated by the candidate; stable
  completion or an explicit future migration is required.
- Stop on a path outside the exact canonical planning or candidate ceiling.
- Stop if CCFG-27 through CCFG-29 or any other row is selected, prepared,
  dispatched, queued, or begun.
- Stop if final validation is represented as an implementation slice.
