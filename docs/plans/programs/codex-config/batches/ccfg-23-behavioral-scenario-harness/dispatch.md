# CCFG-23 Topology-Independent Behavioral Scenario Harness Dispatch

## Batch Identity

- Batch ID: `ccfg-23-behavioral-scenario-harness`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-23, Build the Topology-Independent Behavioral
  Scenario Harness
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/runway.md`
- Successor selected: no

## Selection Decision

Select the user-requested CCFG-23 row now. CCFG-21 and CCFG-22 are closed, so
the candidate has the accepted planning contracts, selection transaction, and
skill-authoring prerequisite. Planning State reports no selected dispatch,
queued runway, active runway, blocker, or conflicting pending finding.

The vague-row guard passes after reading the ledger-linked COR-006 source and
the live CCFG-23 carry-forward amendment. The work has one evidence owner: a
non-installed, topology-independent scenario contract, harness, catalog, and
coverage report. The accepted source gives six exact exit keys and a closed set
of scenario families. The live amendment adds precise planning-quality,
execution-currentness, and cutover-lifecycle behavior. No production command
owner, live planning state, installed generation, or legacy route must change
to complete this characterization batch.

CCFG-24 through CCFG-29 remain separate findings. In particular, CCFG-24 owns
intake transfer, CCFG-25 owns production planning transfer, CCFG-26 owns
execution/closeout transfer, CCFG-27/28 own real cutover work, and CCFG-29 owns
temporary bridge deletion and final convergence. Older open CCFG rows remain
deferred because the user requested CCFG-23.

## Gate Evidence

```yaml
planning_state:
  root: /home/alacasse/projects/codex-config/docs/plans
  current: passed
  validate: passed
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  blockers: []
  warnings:
    - two known redirect-ledger warnings
stable_control:
  repository_root: /home/alacasse/projects/codex-config
  branch: master
  commit: 3fbec1ba80884e4f35bd10c3fdf4f90578358011
  codex_home: /home/alacasse/.codex
  worktree_before_planning: clean
  install_status: passed_with_manifest_version_drift
  install_dry_run: passed_without_writes
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  commit: 2f3995060a309b27ba22d8d7e80f7d07d0b4a34f
  worktree_before_planning: clean
  codex_home: /home/alacasse/.codex-command-owner-redesign
  install_status: passed_at_exact_manifest_versions
  install_dry_run: passed_without_writes
accepted_lineage:
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
  ccfg_19_contract_mapping: closed
  ccfg_21_planning_contracts: closed
  ccfg_22_skill_authoring: closed
strict_context:
  interface: cross-checkout-context/v1
  installed_helper: /home/alacasse/.codex/scripts/cross_checkout_context.py
  helper_resolves_to: /home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
  payload_validation: passed
  planning_and_candidate_write_scope_validation: passed
focused_baseline:
  planning_state_cross_checkout_and_agent_contracts: 309_passed_187_subtests
  cross_checkout_precreation: 32_passed_39_subtests
  focused_manifest_subset: 4_passed_17_deselected_34_subtests
  full_manifest: known_red_3_failed_18_passed_202_subtests
```

## Batch Kind And Risk

- Batch kind: `characterization`.
- Every slice risk: `evidence-only`.
- Authorized work: add one closed-world scenario record contract, one
  non-installed harness owner, fixture-owned scenario catalogs/adapters,
  deterministic coverage reporting, focused tests, and a compact changelog
  entry.
- Production ownership transfer, live migration, contract narrowing,
  destructive cleanup, real installation, default-generation switching, and
  bridge deletion: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such
  operation is authorized.
- Candidate-checkout filesystem approval may be required during execution. It
  authorizes only the candidate paths named below and does not widen scope.

## Goal

Create one topology-independent scenario harness that:

- represents the accepted scenario record as a closed-world v1 contract;
- treats scenario commands as semantic invocation labels rather than shell or
  legacy skill paths;
- compares observed transitions, writes, stops, roots/generation facts, and
  validation evidence without executing arbitrary command strings;
- catalogs the immutable 31 source contract IDs and proves deterministic
  scenario coverage without reading Git history at runtime;
- characterizes public intake, planning, execution, closeout, state, and
  evidence behavior through fixture-owned adapters;
- proves the live planning-quality and Planning State/Git currentness rules;
- proves residual material complexity requires explicit narrowly scoped user
  approval, and that the default command owner directly invokes registered
  `batch_planner` and separate `batch_plan_reviewer` roles without allowing the
  planner to invoke, frame evidence for, or approve its reviewer;
- protects ready/blocked handoffs, fresh leases, result echo, write scope,
  receipts, and exact reviewer diff bases through observable outcomes;
- proves cutover, rollback, physical-absence, and archive-readability behavior
  only in disposable fixtures; and
- reports the six COR-006 exit keys without requiring old APR, Batch Runway,
  exact prompt prose, stable-only paths, or historical helper topology.

Unavailable future production bindings must be reported honestly. A fixture
or reference-interface scenario can prove the accepted target contract, but it
must not claim that CCFG-24 through CCFG-29 production migration already
exists.

## Owner Seam And Validation Class

- Scenario schema: `schemas/command-owner-scenario-v1.schema.json`.
- Harness owner: `scripts/command_owner_scenarios.py`.
- Fixture catalog: `tests/fixtures/command-owner-scenarios/`.
- Focused tests:
  - `tests/test_command_owner_scenario_catalog.py`
  - `tests/test_command_owner_behavioral_scenarios.py`
  - `tests/test_command_owner_scenario_currentness.py`
  - `tests/test_command_owner_scenario_cutover.py`
- Existing planning, Planning State, strict-context, pre-creation, installer,
  and runner code are read-only behavior sources or fixture mechanisms.
- Validation profile: `project-harness-production` because the batch adds a
  schema-backed executable test harness and aggregate report.
- Runway density: `full-runway` because the harness spans state transitions,
  fault injection, three-root identity, and cutover/rollback evidence.
- Run artifact root: `None`.
- Output root: `None`; coverage JSON, pytest temporary roots, and disposable
  install sandboxes are ephemeral.
- Test quality review: `delta-only` for every slice and the final exact
  candidate range.

## Accepted Evidence And Exit Keys

The immutable COR-006 source requires:

```yaml
source_characterization_green: true
target_interfaces_green: true
bootstrap_cutover_green: true
fault_injection_green: true
contract_coverage_complete: true
legacy_topology_not_required: true
```

The migration-program aliases must also be green:

```yaml
source_characterization_green: true
target_interface_scenarios_green: true
bootstrap_and_cutover_scenarios_green: true
fault_injection_scenarios_green: true
contract_id_coverage_report_complete: true
legacy_skill_names_not_required_except_migration_fixtures: true
```

The live carry-forward additionally requires every planning-quality,
execution-currentness, and cutover-lifecycle scenario under
`docs/plans/programs/codex-config/findings/command-owner-redesign-planning-execution-carry-forward.md`
to have explicit green evidence.

## Included Source Scope

- COR-006 / CCFG-23 and the 31 behavior contract IDs in accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- The canonical scenario record and family matrix in accepted
  `docs/design/command-owner-redesign/05-behavioral-test-matrix.md`.
- The closed CCFG-19 source-contract mapping and decisions as evidence, not as
  mutable scope.
- The completed CCFG-21 planning schemas, artifact stores, selection
  transaction, and fault checkpoints as read-only public seams.
- The completed CCFG-22 skill-authoring output as a prerequisite, not as a
  harness dependency or mutable surface.
- The live CCFG-23 carry-forward amendment named by the ledger row.

## Deferred And Excluded

- Editing `add-to-ledger`, `plan-batch`, `work-batch`, their skills, runtime
  dependencies, installed links, or production ownership.
- Modifying the closed CCFG-20/21/22 schemas, validators, skills, tests, or
  feature registration.
- Expanding `scripts/planning_contract.py` or `scripts/planning_state.py` into
  the scenario-harness owner.
- Porting stable-only helper function names, lease-preparation topology,
  prompt prose, APR/Batch Runway modes, or legacy dependency lists into target
  assertions.
- Actual canonical planning mutation from the candidate, real default-home or
  candidate-home installation, atomic switch, rollback, route deletion, or
  bridge removal.
- Treating synthetic final bridge absence as evidence that CCFG-29 is done.
- Fixing the three known-red manifest assertions or unrelated installer/version
  drift.

## Suggested Slice Shape

1. Add the closed-world scenario contract, non-installed harness owner,
   deterministic contract/scenario coverage report, full catalog skeleton, and
   self-tests.
2. Bind fixture-owned source and target workflow scenarios for intake,
   planning, execution, closeout, queue guards, semantic plan quality, and
   no-successor behavior.
3. Add Planning State-first currentness, Git material-integrity, strict
   handoff/lease, reviewer-basis, and planning/commit/closeout fault scenarios
   using isolated repositories and temporary Layout v1 roots.
4. Add disposable generation/install/cutover/rollback/physical-absence/archive
   scenarios, then prove the aggregate six-key gate and topology independence.

## Required Strict Execution Context

Mode: explicit `cross-checkout-context/v1`.

Installed helper used for planning validation:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated planning snapshot payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 3fbec1ba80884e4f35bd10c3fdf4f90578358011
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 3fbec1ba80884e4f35bd10c3fdf4f90578358011
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 2f3995060a309b27ba22d8d7e80f7d07d0b4a34f
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The installed stable helper parsed this payload and validated the exact four
canonical planning paths plus the eight intended candidate paths/file areas in
the runway. Planning performed no candidate write.

## Stop Conditions

- Stop if the selected CCFG-23 scope no longer matches this dispatch.
- Stop if the first execution-flight ready/blocked preflight does not return a
  fresh strict context for this selected scope.
- Stop if the candidate worktree is not clean before Slice 1 or a slice diff
  escapes its allowlist.
- Stop if target scenarios can turn green only by changing production command
  owners, live planning state, stable-only helper topology, or real cutover
  state.
- Stop if unbound future interfaces are counted as implemented production
  behavior rather than reported honestly.
- Stop if any test requires an APR/Batch Runway path, mode, exact prompt,
  dependency presence, compatibility alias, or historical helper name.
- Stop if an installer/cutover/deletion scenario touches a real Codex home,
  canonical planning root, default binding, or live legacy route.
- Stop if work modifies CCFG-24+ owners, deletes the temporary bridge, or
  treats fixture absence as CCFG-29 completion.
- Stop on changed known-red baseline, unexpected repository movement, failed
  focused validation, unresolved review, or scope drift.
- Stop closeout before selecting, refreshing, dispatching, or preparing a
  successor batch.
