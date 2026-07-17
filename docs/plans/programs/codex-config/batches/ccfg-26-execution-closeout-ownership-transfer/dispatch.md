# CCFG-26 Execution And Closeout Ownership Transfer Dispatch

## Selection

- Batch ID: `ccfg-26-execution-closeout-ownership-transfer`
- Selection outcome: `selected`
- Queue target: exactly one `queued` runway
- Covered finding: CCFG-26, Transfer Execution and Closeout Ownership to
  `work-batch`
- Finding state entering the batch: `Open`
- Source program ledger: `../../LEDGER.md`
- Expected runway path: `runway.md`
- Planning root: `../../../..`
- Implementation target:
  `/home/alacasse/projects/codex-config-command-owner-redesign`

Planning State `current` and `validate` reported an idle, valid program with no
selected dispatch, queued batch, active runway, blocker, or obligation. The
explicit `plan-batch` invocation selects exactly CCFG-26. CCFG-27 through CCFG-29
remain deferred and unselected.

## Authoritative Sources

- CCFG-26 in `../../LEDGER.md`.
- COR-009 at accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- `../ccfg-25-planning-ownership-transfer/closeout.md`.
- `../../../../../../CONTEXT.md` and
  `../../../../../adr/0002-human-facing-command-owner-skills.md`.

## Goal

Make `work-batch` the sole semantic owner of one complete execution and
same-batch closeout flight: currentness, proceed/stop, recovery, delegation,
validation acceptance, implementation review, commits, receipts, finalization,
closeout, program reconciliation, and the no-successor stop.

Remove Batch Runway `execute-spec`, recovery, and finalization ownership and
Architecture Program Runway closeout/reconciliation ownership in the same work.
Keep only explicitly classified, no-owner compatibility or mechanical shells
until their scheduled physical deletion. Converge the isolated candidate
installation without changing the stable home or default generation.

## Batch Kind And Approval

- Batch kind: `mixed-risk`.
- Slice 1: `migration`.
- Slice 2: `contract-narrowing`.
- Slice 3: `migration`.

The CCFG-26 ledger row, pinned COR-009, and accepted carry-forward amendment
explicitly authorize Slice 2 to remove the displaced semantic owners in the same
work. That approval is limited to execution and closeout ownership. It does not
authorize physical deletion of Batch Runway or Architecture Program Runway,
removal or migration of the four serialized runner phase identities, bridge
deletion, a new protocol, or a default-generation switch.

No other residual material complexity or destructive action is approved. Any
such discovery blocks for an amendment and fresh independent planning review.

## Authoritative Invariants

- Planning State `current` and `validate` are the sole semantic authority for
  selected, queued, and active currentness.
- `work-batch` owns all execution and same-batch closeout decisions.
- Git is material-integrity evidence only. History, path sets, fingerprints,
  ancestry, and dirty files do not decide lifecycle or queue semantics.
- First handoff validates the exact implementation baseline. Later handoffs use
  exact accepted-action movement and fresh live leases.
- Every worker and reviewer handoff receives a fresh validated strict context;
  reviewers receive the exact diff basis they review.
- Worker and reviewer roles remain separate, registered, and v2-result bound.
- Branch checks use ordinary target policy. Dirty files use ordinary
  task-scope conflict handling.
- Partial execution and partial closeout recover the same batch without
  duplicate effects or successor selection.
- `select-dispatch`, `create-spec`, `execute`, and `closeout` remain the exact
  serialized compatibility identities through CCFG-26. CCFG-27 owns their
  migration/removal decision.
- Physical legacy-owner deletion is deferred to CCFG-28. Temporary strict and
  pre-creation bridge deletion is deferred to CCFG-29.
- Stable installation, canonical planning authority, and the default generation
  remain unchanged.

## Proportionality

```yaml
proportionality:
  observed_failure: >-
    work-batch is still a thin router while Batch Runway owns execution,
    recovery, validation acceptance, review, commits, receipts, ledgers, and
    finalization, and Architecture Program Runway owns closeout reconciliation.
    Active runner, role, documentation, and manifest callers preserve those
    broad owner dependencies. Two focused ownership assertions are red at the
    exact CCFG-25 candidate closeout baseline.
  invariants:
    - one complete human-facing work-batch command owner
    - Planning State as the sole semantic currentness gate
    - Git as material-integrity evidence only
    - preserved worker/reviewer separation and strict cross-checkout safety
    - exact commit, receipt, recovery, and reviewer-diff integrity
    - same-work removal of replaced execution and closeout owners
    - preserved four serialized runner phase identities through CCFG-26
    - classified no-owner shells until CCFG-28 and bridge retention until CCFG-29
    - unchanged stable installation and default generation
    - no successor selection
  minimum_viable_change: >-
    Move complete semantic execution and same-batch closeout ownership into
    work-batch and remove those decisions from Batch Runway and Architecture
    Program Runway.
  proposed_change: >-
    Establish the complete replacement owner and behavioral proof, narrow only
    the displaced semantic owners while rebinding active callers and retaining
    classified shells, then converge clean candidate installations and exact
    COR-009 acceptance.
  additions_beyond_minimum:
    - addition: focused currentness, old-format active-state, lease, result, recovery, commit, receipt, and no-successor tests
      prevents: ownership existing only in prose or regressing strict execution safety
      why_minimum_is_insufficient: >-
        An owner text move alone cannot mechanically prove the transferred
        decisions, negative legacy behavior, or partial-flight recovery.
    - addition: runner phase, role, routing, documentation, and manifest rebinding
      prevents: installed callers continuing to route semantic decisions through displaced owners
      why_minimum_is_insufficient: >-
        Changing only work-batch leaves live consumers and installation metadata
        on the old topology.
    - addition: fresh and fixed candidate installation convergence with exact acceptance and final reviews
      prevents: worktree-only success, stale links, stable-home mutation, or unreviewed cross-slice drift
      why_minimum_is_insufficient: >-
        Focused owner tests cannot prove installed topology or the complete final
        candidate range.
  simpler_alternatives_rejected:
    - alternative: edit only work-batch prose
      reason: Batch Runway, APR, runner, roles, manifest, and tests would retain broad owner dependencies.
    - alternative: delete Batch Runway, APR, or the strict bridge now
      reason: physical legacy deletion belongs to CCFG-28 and bridge deletion belongs to CCFG-29.
    - alternative: add a new coordinator helper, script, schema, store, transaction, lifecycle state, or compatibility protocol
      reason: that duplicates ownership instead of transferring it.
    - alternative: defer the two known-red owner assertions
      reason: COR-009 requires the transferred owner boundary green before CCFG-27.
  verdict: proportionate
```

## Included Scope

- Complete `work-batch` execution and same-batch closeout ownership.
- Surviving execution contracts moved beneath the command owner; registered
  worker/reviewer contracts no longer depend on Batch Runway paths.
- Focused target behavior for currentness, old-format active state, first and
  later handoffs, exact review bases, recovery, commits, receipts, finalization,
  reconciliation, and no-successor enforcement.
- Batch Runway and Architecture Program Runway narrowed to explicitly
  classified no-owner compatibility or mechanical shells only.
- The runner phase contract rebound to one `work-batch` flight while preserving
  serialized phase observations and transitions.
- Active role, routing, workflow, README, manifest, and changelog surfaces.
- Candidate-only installation convergence and complete COR-009 acceptance.

## Deferred And Preserved Scope

- CCFG-27 cutover preparation and the public runner-protocol decision.
- CCFG-28 physical deletion of legacy-owner source directories and final switch.
- CCFG-29 candidate integration, default-home rebind, and bridge deletion.
- Any new command, schema, store, transaction, lifecycle state, helper behavior,
  compatibility layer, persistent execution store, or runner protocol.
- Planning, intake, selection, DEC-038, `ledger-store/v1`, projection, or
  Planning State semantic changes.
- Stable-home installation, candidate merge, default-generation switching, and
  canonical writes from the candidate.

## Implementation Write-Path Ceiling

Required areas:

- `skills/work-batch/**`
- `skills/batch-runway/**`
- `skills/architecture-program-runway/**`
- `agents/runway_worker.toml`
- `agents/runway_reviewer.toml`
- `scripts/architecture_program_runner_phase_contract.py`
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `README.md`
- `codex-features.json`
- `CHANGELOG.md`
- `tests/test_codex_features_manifest.py`
- `tests/test_architecture_program_runner_phase_contract.py`
- `tests/test_custom_agent_contracts.py`
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/fixtures/command-owner-scenarios/**`
- `tests/test_command_owner_scenario_catalog.py`

Conditional only after a focused failing test or direct caller proof:

- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner.py`
- `tests/test_architecture_program_runner_protocol.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `skills/legacy-removal/SKILL.md`
- `skills/planning-artifacts/SKILL.md`
- `skills/test-quality-review/SKILL.md`

The exact proof and reason must be recorded before a conditional path is edited.
Any other path requires an amended dispatch and fresh independent planning
review.

## Slice Shape

- Slice 1 — `migration`: establish the complete `work-batch` owner, relocate
  surviving execution contracts below it, and bind the focused behavior.
- Slice 2 — `contract-narrowing`: remove displaced Batch Runway and APR semantic
  ownership, rebind active callers, and retain only classified no-owner shells.
- Slice 3 — `migration`: converge installation and exact acceptance.

`1 -> 2`: Slice 1 creates an independently exercisable replacement owner and
rollback point before contract narrowing.

`2 -> 3`: Slice 2 creates the final semantic topology; Slice 3 validates that
topology across clean environments and an exact independently reviewed range.

## Queue Gate

Queue mutation is allowed only after:

1. the installed stable cross-checkout helper validates the complete planning
   snapshot and exact write scopes in `runway.md`;
2. the planner result is `batch-plan-draft/v1` with `status: ready`, one finding,
   proportional scope, and no unresolved decision or implementation start;
3. an independently invoked reviewer receives the exact sources, user
   constraints, Planning State facts, proportionality record, approval scope,
   dispatch, and runway and returns `batch-plan-review/v1` with `verdict: clean`
   against the exact hashes; and
4. the same immutable basis still matches immediately before the queue update.

## Stop Conditions

- Stop on missing or mismatched strict-context validation or Planning State
  currentness.
- Stop if the implementation baseline differs from
  `89671eceb9103039e7e6660e73837827c167a3a1` at first execution handoff.
- Stop if a new script, helper, schema, store, transaction, lifecycle state,
  compatibility layer, or runner protocol is required.
- Stop if semantic execution or closeout ownership remains in Batch Runway or
  Architecture Program Runway after Slice 2.
- Stop if retained shells make lifecycle, acceptance, closeout, reconciliation,
  or successor decisions.
- Stop if any of the four serialized runner phase identities is changed before
  CCFG-27, or if a legacy directory or bridge is physically deleted early.
- Stop on stable-home mutation, candidate canonical write, default-generation
  switch, candidate merge, or successor selection.
- Stop if Git or dirty-file facts are reintroduced as lifecycle authority.
- Stop on an edit outside the exact required or evidence-activated conditional
  ceiling.
