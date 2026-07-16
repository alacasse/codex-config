# CCFG-24B Intake Ownership Cutover Runway

## Purpose

Complete the cutover prepared by CCFG-24A: remove obsolete intake migration
residue, remove APR intake and normal ledger-mutation ownership, make
`legacy-removal` evidence-only, reconcile the candidate installation, and close
CCFG-24 with complete COR-007 evidence.

## Authority

- Finding: CCFG-24, entering this batch as `Prepared`.
- Dispatch: `dispatch.md`.
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Two-batch boundary:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`.
- Bounded command decisions:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`.
- Controlling preparation evidence:
  `../ccfg-24a-intake-owner-preparation/closeout.md`.

Use the CCFG-24A closeout inventory as the normal read path. Reopen its runway,
worker history, or broad redesign sources only for a named contradiction.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1, Remove obsolete CCFG-23 intake residue: `destructive-cleanup`.
- Slice 2, Remove APR intake and normal mutation ownership:
  `contract-narrowing`.
- Slice 3, Make `legacy-removal` evidence-only: `contract-narrowing`.
- Slice 4, Reconcile installation and final acceptance: `migration`.

`slice_shape`: four slices.

- `1 -> 2`: test-fixture deletion has a separate caller-evidence and rollback
  boundary from public ownership narrowing.
- `2 -> 3`: APR and `legacy-removal` retain different future responsibilities and
  require independent preservation proofs.
- `3 -> 4`: installation, routing convergence, and exact acceptance must consume
  the complete narrowed topology.

## Baseline

- Stable toolchain and canonical planning checkout:
  `/home/alacasse/projects/codex-config`, branch `master`.
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`.
- Stable planning baseline at selection: `7d36ef82cd0a72d854db9b268e2c56069606dc3d`.
- Candidate implementation baseline:
  `3b0941af769ef4f4cd184c1b110df3fa2bf48f32`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
- CCFG-24A final exact acceptance: 69 scenarios, 31 contracts, 17 families,
  six keys, six aliases, and one evidence-pytest process.
- Current assigned manifest diagnostic: four failures, of which one CCFG-24
  intake assertion must become green; the remaining three belong only to
  CCFG-25/26.
- Recorded broad legacy/projection diagnostic before CCFG-24B: 12 failures,
  19 passes, and 50 passing subtests. This is diagnostic context, not authority
  to fix unrelated failures.

At execution startup, reproduce the manifest and broad legacy/projection
baselines before delegation. Block on new or reclassified failures instead of
silently widening the batch.

## Batch Non-Goals

- No new source adapter, file ingestion, cross-source merge, fuzzy matching, or
  expansion of `add-to-ledger/v1`.
- No change to DEC-037, `ledger-store/v1`, `scripts/planning_contract.py`, or any
  planning schema.
- No removal of APR grouping, selection, queue, dispatch, planning, execution
  support, closeout, or reconciliation responsibilities reserved for CCFG-25/26.
- No deletion of `legacy-removal`, its evidence vocabulary, compatibility
  decisions, cleanup-residue classification, or dead-surface integration.
- No stable-home mutation, default-generation switch, candidate merge to master,
  bridge deletion, or CCFG-25 through CCFG-29 work.
- No successor selection during closeout.

## Candidate Scope

Allowed across the batch, restricted further by each slice:

- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/fixtures/command-owner-scenarios/workflow-cases.yaml`
- `tests/fixtures/command-owner-scenarios/workflow_adapters.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/agents/openai.yaml`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `skills/legacy-removal/SKILL.md`
- `skills/planning-artifacts/SKILL.md`
- `codex-features.json`
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `README.md`
- `CHANGELOG.md`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_deletion_test_vocabulary_ownership.py`
- `tests/test_codex_features_manifest.py`

Read-only except execution:

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `tests/test_add_to_ledger.py`
- `scripts/planning_contract.py`
- planning and skill schemas
- `scripts/planning_state.py`
- `scripts/command_owner_scenarios.py`
- `skills/plan-batch/**`, `skills/work-batch/**`, and `skills/batch-runway/**`
- installer implementation and cross-checkout helpers

A required semantic edit in a read-only area stops execution for replanning.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status.
Use Batch Runway Orchestration Anomaly Log v1.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/test-quality-review/SKILL.md`

Workers implement one slice only and do not delegate. The coordinator owns
validation, specialist and independent review, candidate installation, commits,
execution-ledger updates, and same-batch closeout.

## Planning Snapshot

Interface: `cross-checkout-context/v1`.

Installed helper:
`/home/alacasse/.codex/scripts/cross_checkout_context.py`

Canonical planning root:
`/home/alacasse/projects/codex-config/docs/plans`

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 7d36ef82cd0a72d854db9b268e2c56069606dc3d
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 7d36ef82cd0a72d854db9b268e2c56069606dc3d
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 3b0941af769ef4f4cd184c1b110df3fa2bf48f32
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

This connector-backed planning session could not execute the installed local
helper. The payload is assembled from the clean CCFG-24A closeout roots and exact
GitHub commits and is not execution authority. At `work-batch` startup, pass this
immutable snapshot to the installed ready/blocked preflight. Proceed only on
`ready`; any parse, root, revision, movement, or scope mismatch blocks before
delegation. Validate exact write scope before every handoff.

## Context Control

The coordinator reads only:

1. current Planning State facts;
2. `dispatch.md`, this runway, and the CCFG-24A closeout inventory;
3. the active slice;
4. compact prior-slice receipts and reviews.

Do not paste source files, broad repository searches, or subagent transcripts
into coordinator context. Delegate fresh caller investigation to a bounded
investigator or dead-surface reviewer.

- Soft execute budget: 100,000 input tokens.
- Hard warning: 150,000 input tokens.
- Stop when context pressure coincides with a new semantic choice or scope
  expansion.

## Validation Contract

Profile:
`skills/batch-runway/references/validation-profiles/project-harness-production.md`

Status classes:

- Existing owner/store, skill-contract, behavioral/catalog, routing,
  strict-context, installer, Ruff, BasedPyright, and whitespace baselines:
  `required-green` or their explicitly recorded baseline class.
- Full manifest before final convergence: `known-red-baseline`, exactly the four
  failures recorded by CCFG-24A.
- Full broad legacy/projection suite: `known-red-baseline`. CCFG-24B promotes only
  the selected `legacy_removal`, `legacy_evidence_no_state_writes`, and
  `parallel_planning_systems` nodes. Other pre-existing failures remain outside
  this batch and no new failure is allowed.
- After Slice 4, the full manifest may remain red only for:
  - `test_executable_work_source_boundary_is_explicit` — CCFG-25 remainder;
  - `test_plan_batch_command_owner_runtime_boundaries_are_explicit` — CCFG-25;
  - `test_work_batch_reconciles_same_batch_closeout` — CCFG-26.
- No CCFG-24 assertion may remain red after Slice 4.

Every test-changing slice receives independent review and delta-only
`test-quality-review`. Slices 1 through 3 receive a targeted dead-surface audit.
Slices 2, 3, and the final range receive import-topology review.

## Execution Ledger

| Slice | Status | Risk | Commit | Validation | Review |
|---|---|---|---|---|---|
| 2. Remove APR intake ownership | Blocked | contract-narrowing | None | Ownership subset: 3 passed; exact two-file skill-contract CLI gate is unsatisfiable because its closed catalog omits three legitimate external mechanisms | Not run; candidate diff frozen |
| 3. Make `legacy-removal` evidence-only | Pending | contract-narrowing | None | Not run | Pending |
| 4. Reconcile and close COR-007 | Pending | migration | None | Not run | Pending |

Accepted results move to `completed-slices.md`.

## Active Recovery

- Slice: 2, Remove APR intake ownership.
- Blocker: the required command
  `.venv/bin/python scripts/skill_contract.py validate --toolchain-root .
  skills/add-to-ledger/SKILL.md
  skills/architecture-program-runway/SKILL.md` supplies a complete two-document
  catalog, so it rejects the legitimate external mechanisms
  `planning_contract_store`, `planning-artifacts`, and `planning-state`.
- Cause: `skill-contract/v1` keeps external-mechanism allowance in the
  validator-call policy; a skill cannot self-authorize it, and
  `--toolchain-root` does not discover manifest dependencies or additional
  contracts.
- Current candidate state: eleven Slice 2 files are modified against candidate
  commit `5cb0e6cfccc2aba6f18a011651619157c637af28`; focused ownership validation
  passed 3 tests with 50 deselected; `git diff --check` passed; no review or
  commit has been accepted.
- Next safe action: amend this validation gate to run the existing focused
  catalog test with `ExternalMechanismPolicy` for exactly the three legitimate
  external mechanisms, then renew the strict execution lease, rerun Slice 2
  validation, and continue the same slice. Do not weaken complete-catalog
  validation, remove legitimate dependency declarations, add fake contract
  identities, start Slice 3, or select successor work.

## Active Orchestration Anomalies

```yaml
orchestration_anomalies:
  - slice: 2
    severity: medium
    category: ambiguous_validation_command
    observed: "The runway's exact two-file CLI command cannot express the external-mechanism policy required by the accepted closed-world contract model."
    impact: "The implementation diff is frozen before review and commit even though focused ownership validation is green."
    action_taken: "Classified the failure through execute-recovery-v1 and stopped before widening scope or weakening validation."
    follow_up: "Amend the gate to use policy-backed focused catalog validation, then resume Slice 2."
```

## Slice 1: Remove Obsolete CCFG-23 Intake Residue

### Approval Gate

Before deletion, record a fresh caller inventory proving:

- `_new_finding` has zero live callers;
- the four intake scenarios still execute the installed owner;
- replacement assertions cover scenario identity and behavioral completeness;
- no proposed deletion removes the only proof of an accepted behavior.

The gate is approved by the coordinator only after dead-surface evidence and a
read-only independent review agree. Missing or ambiguous evidence blocks this
slice without authorizing broader cleanup.

### Work

- Delete `_new_finding` and only other proven zero-caller intake migration residue.
- Replace the temporary exact-69-ID topology/count assertion with assertions that
  preserve required scenario IDs, families, and contracts by behavior rather
  than incidental aggregate shape.
- Remove or rewrite tests that preserve obsolete helper topology.
- Keep installed-owner request builders and scenario adapters when they remain
  legitimate behavioral harness callers; do not delete them merely because they
  originated in CCFG-23.

Allowed files: the five CCFG-23 fixture/scenario files listed in batch scope and
`CHANGELOG.md`.

### Acceptance And Validation

- No zero-caller helper remains.
- Four intake scenarios still traverse the installed owner and preserve create,
  update, multi-create, semantic no-op, exact replay, block, stale-CAS,
  provenance, and no-downstream-effect evidence.
- All non-intake scenarios remain unchanged.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache tests/fixtures/command-owner-scenarios/workflow_adapters.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
git diff --check
```

All commands: `required-green`.

Reviews: targeted `dead-surface-audit`, independent scenario/deletion review, and
delta-only test-quality review.

Commit: `test: remove obsolete intake fixture residue`

Stop on any unproven deletion, scenario behavior loss, owner bypass, or change to
non-intake semantics.

## Slice 2: Remove APR Intake And Normal Mutation Ownership

### Approval Gate

Slice 1 is committed and green. Before narrowing APR, the coordinator records an
owner matrix proving the intended diff preserves:

- grouping, prioritization, and sequencing;
- selected dispatch and queue state;
- CCFG-25 planning handoff;
- CCFG-26 execution/closeout and reconciliation support.

It also proves that all intake decisions and normal ledger mutations are already
owned and tested through `add-to-ledger/v1`.

### Work

- Remove APR intake, normalization, `intake-findings`, create/update/no-op, and
  normal ledger-mutation authority from skill, agent metadata, template, and
  direct ownership tests.
- Remove any remaining `add-to-ledger -> architecture-program-runway` runtime or
  routing dependency.
- Rewrite migration/routing tests so they prove ownership transfer without
  preserving APR wording or topology.
- Preserve all explicitly named CCFG-25/26 responsibilities.

Allowed files:

- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/agents/openai.yaml`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- APR-specific sections of routing/workflow docs and `README.md`
- APR-related catalog, migration, routing, manifest tests
- `codex-features.json` APR metadata and `CHANGELOG.md`

### Acceptance And Validation

- No active APR mode, description, prompt, template, routing rule, or dependency
  owns intake or normal ledger mutation.
- `add-to-ledger` remains independent of APR.
- APR's preserved planning and closeout seams are explicit and tested.
- The executable-work-source manifest test has no CCFG-24 remainder; any failure
  is exclusively the named CCFG-25 planning remainder.

Required-green ownership subset:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_routing_rule_ownership.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py tests/test_codex_features_manifest.py -k 'add_to_ledger or architecture_program or command_owner_input_contracts'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -c 'from pathlib import Path; from scripts.skill_contract import ExternalMechanismPolicy, validate_skill_contracts; result = validate_skill_contracts((Path("skills/add-to-ledger/SKILL.md"), Path("skills/architecture-program-runway/SKILL.md")), toolchain_root=Path("."), external_mechanism_policy=ExternalMechanismPolicy(allowed_mechanisms=frozenset({"planning_contract_store", "planning-artifacts", "planning-state"})), complete_catalog=True); assert result.is_valid, "\n".join(f"{diagnostic.path}:{diagnostic.location}: {diagnostic.code}: {diagnostic.message}" for diagnostic in result.diagnostics)'
git diff --check
```

Separately run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'test_executable_work_source_boundary_is_explicit'
```

Status: `known-red-baseline`. Its only remaining failing assertion may concern
CCFG-25 planning ownership; any CCFG-24/APR-intake assertion must be green.

Reviews: targeted `dead-surface-audit`, independent ownership-preservation review,
`import_topology_reviewer`, and delta-only test-quality review.

Commit: `refactor: remove APR intake ownership`

Stop if the diff merely renames a fallback, retains duplicate intake semantics,
or removes any CCFG-25/26 responsibility.

## Slice 3: Make `legacy-removal` Evidence-Only

### Approval Gate

Slices 1 and 2 are committed and green. A focused test must prove that
`legacy-removal` can produce evidence and classifications without selecting,
queueing, dispatching, executing, reconciling, closing, or mutating lifecycle
state.

### Work

- Remove the selected-program-owner exception and all queue/dispatch/runway/
  closeout or lifecycle-state escape hatches from `legacy-removal`.
- Remove or migrate the two retention tests and planning-placement wording that
  preserve that authority.
- Preserve canonical-model decisions, compatibility decisions, cleanup-residue
  classification, dispatch handoff material as evidence, and consumption of
  dead-surface/deletion-test statuses.
- Keep `legacy-removal` routable as an evidence producer, not a public command or
  parallel planning system.

Allowed files:

- `skills/legacy-removal/SKILL.md`
- legacy-specific sections of `skills/planning-artifacts/SKILL.md`, APR's program
  ledger template, routing/workflow docs, `README.md`, and `codex-features.json`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_deletion_test_vocabulary_ownership.py`
- legacy-related catalog, migration, and routing tests
- `CHANGELOG.md`

### Acceptance And Validation

- `legacy-removal` has no program state or lifecycle mutation authority.
- Evidence, compatibility, residue, and deletion-vocabulary behavior remains.
- No parallel planning system or direct concrete-runway owner exception remains.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py -k 'legacy_removal or legacy_evidence_no_state_writes or parallel_planning_systems'
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/legacy-removal/SKILL.md
git diff --check
```

Selected nodes: `required-green`.

The unfiltered two-file legacy/projection diagnostic remains
`known-red-baseline`; record its failure identities before and after and accept
no new failure. CCFG-24-owned nodes must no longer be among its failures.

Reviews: targeted `dead-surface-audit`, independent evidence/state-boundary
review, `import_topology_reviewer`, and delta-only test-quality review.

Commit: `refactor: make legacy-removal evidence-only`

Stop if evidence semantics are removed, lifecycle authority moves to another
support skill, or a project-owner exception remains.

## Slice 4: Reconcile Installation And Final COR-007 Acceptance

### Gate

Slices 1 through 3 are committed with clean reviews. Source state has one intake
owner, no APR intake route, and no `legacy-removal` state-owner escape hatch.

### Work

- Reconcile remaining manifest, routing, workflow, README, changelog, and
  migration-guard wording against the final topology.
- Update the old add-to-ledger dependency assertion so no CCFG-24 manifest
  failure remains.
- Candidate-install exactly the changed features among `add-to-ledger`,
  `planning-contracts`, `architecture-program-runway`, `legacy-removal`, and
  `planning-artifacts`; do not touch the stable home.
- Run one clean exact-commit acceptance after all final-range reviews.

### Required-Green Validation

Core and ownership suites:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_skill_routing_rule_ownership.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py -k 'legacy_removal or legacy_evidence_no_state_writes or parallel_planning_systems'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'not test_executable_work_source_boundary_is_explicit and not test_plan_batch_command_owner_runtime_boundaries_are_explicit and not test_work_batch_reconciles_same_batch_closeout'
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/fixtures/command-owner-scenarios/workflow_adapters.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_skill_routing_rule_ownership.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py tests/test_codex_features_manifest.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check 3b0941af769ef4f4cd184c1b110df3fa2bf48f32
```

Known-red diagnostics, run separately:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py
```

The manifest may fail only the three named CCFG-25/26 tests. The broad
legacy/projection diagnostic may retain only reproduced, preclassified
non-CCFG-24 failures; no new failure and no CCFG-24-owned failure is accepted.

Candidate installation:

```sh
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature planning-contracts
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature add-to-ledger
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature architecture-program-runway
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature legacy-removal
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature planning-artifacts
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
```

Run CCFG-33 exact-commit acceptance once from the final clean candidate commit
with fresh `/tmp/ccfg-24b-*` outputs and read the generated report before
acceptance.

Reviews: final exact-range independent review, `import_topology_reviewer`,
`dead-surface-audit`, and delta-only test-quality review.

Commit: `refactor: complete add-to-ledger ownership cutover`

Stop if installation requires stable-home writes, an omitted feature, a new
manifest failure, an unclassified legacy/projection failure, or semantic changes
to the owner/store boundary.

## Final Validation And Closeout

1. Confirm only this CCFG-24B runway is queued or active.
2. Confirm all approval gates and retained-surface decisions are recorded.
3. Run all required-green commands and both known-red diagnostics.
4. Prove `add-to-ledger/v1` is the sole intake and mutation-decision owner.
5. Prove APR retains only the responsibilities reserved for CCFG-25/26.
6. Prove `legacy-removal` is evidence-only.
7. Prove candidate links converge and stable links remain unchanged.
8. Run final exact-commit acceptance once and validate its outputs.
9. Record candidate range, removed/preserved surfaces, validation/runtime, diff
   size, installed links, and final reviews.
10. Write `completed-slices.md` and `closeout.md`; mark CCFG-24 `Closed`; clear
    same-batch state; stop without selecting CCFG-25.

## Batch Stop Conditions

Stop on Planning State mismatch, blocked strict preflight, repository movement,
dirty conflict, unclassified deletion, behavior loss, store/schema drift, a new
owner seam, stable-home mutation, CCFG-25/26 responsibility loss, deferred adapter
work, a new or reclassified known-red failure, or any CCFG-25 through CCFG-29
selection. Stop after same-batch closeout with CCFG-24 `Closed` and no successor
selected.
