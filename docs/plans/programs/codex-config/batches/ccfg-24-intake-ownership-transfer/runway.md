# CCFG-24 Intake Ownership Transfer Runway

## Purpose

Transfer intake and canonical ledger-mutation decision ownership to the
human-facing `add-to-ledger` feature, prove the accepted intake contracts
through the existing apply-only planning store, remove the corresponding APR,
`legacy-removal`, and disposable CCFG-23 ownership paths in the same batch, and
leave CCFG-25 through CCFG-29 unselected.

This is a future execution spec. Planning created it without changing the
candidate implementation, either installed generation, or any slice status.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1, Establish production `add-to-ledger/v1` ownership: `migration`.
- Slice 2, Rebind and prune CCFG-23 intake scenarios: `destructive-cleanup`.
- Slice 3, Remove APR intake and normal ledger mutation: `contract-narrowing`.
- Slice 4, Make `legacy-removal` evidence-only: `contract-narrowing`.
- Slice 5, Reconcile installation, metadata, docs, and migration proof:
  `migration`.

Destructive and contract-narrowing slices remain blocked until their explicit
approval gates below are satisfied with current evidence.

## Current Baseline And Assumptions

- Planning State validation passes at Planning Artifact Layout v1 root
  `docs/plans/`; before this runway the program had no selected dispatch,
  queued batch, active runway, blockers, or obligations.
- Canonical stable planning repository:
  `/home/alacasse/projects/codex-config`, branch `master`, plan-time `HEAD`
  `d739bd5660165fe321981ae0219a61c56667560b`.
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, plan-time `HEAD`
  `b38570bcd97b2584f3828abcd395b0f45ed91e58`, aligned with its upstream.
- Both worktrees were clean before planning.
- Stable Codex home: `/home/alacasse/.codex`; all default installed links
  resolve to the stable checkout. Status succeeds with known manifest-version
  drift; dry-run performs no write.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`; status
  and dry-run report exact candidate versions and links. The installed
  `add-to-ledger` still routes real ledger work through APR and
  `legacy-removal`.
- `skills/add-to-ledger/SKILL.md` is currently a thin caller-visible command
  contract with no `skill-contract/v1` block or production executable intake
  owner.
- The only executable intake semantics are disposable CCFG-23 fixture helpers:
  `observe_intake`, `_run_intake`, and `_new_finding` in
  `tests/fixtures/command-owner-scenarios/workflow_adapters.py`.
- CCFG-21 already implemented `ledger-store/v1` through
  `scripts/planning_contract.py::read_ledger_document` and
  `apply_ledger_decision`, with `planning-finding/v1`, whole-ledger CAS,
  touched-finding revisions, exact replay, deterministic rendering, atomic
  replacement, reread validation, and receipt recovery.
- The planning-contract mechanism and schema family are not yet installed as a
  neutral feature. This batch names that feature `planning-contracts`.
- CCFG-22 made `skill-authoring` v1 authoritative for contract-first hybrid
  skill migration. It is authoring support only and must not become a runtime
  dependency.
- CCFG-23 established stable intake scenario and contract IDs. CCFG-33 made the
  complete acceptance path practical and left fixture adapters for CCFG-24
  through CCFG-29 to replace as real owners become authoritative.
- The full manifest diagnostic currently reports exactly three failures, 18
  passes, and 202 passing subtests. Its failures are assigned to CCFG-24/25,
  CCFG-25, and CCFG-26 respectively; this batch may migrate only the intake half
  of the shared source-boundary test.

## Batch Non-Goals

- Do not select, plan, implement, or prepare CCFG-25 through CCFG-29.
- Do not transfer `plan-batch` planning ownership or `work-batch`
  execution/closeout ownership.
- Do not delete APR grouping, ranking, selection, dispatch, queue preparation,
  closeout, or reconciliation paths still assigned to CCFG-25 or CCFG-26.
- Do not delete the APR or Batch Runway directories, retire their installed
  features globally, switch the default generation, or merge the candidate to
  master.
- Do not change candidate/stable root topology, cross-checkout bridge
  semantics, Planning State currentness, live planning artifact format, or the
  canonical stable ledger.
- Do not add a second ledger store, public general workflow engine, durable
  intake queue, duplicate planning database, public request schema, or
  candidate-controlled canonical planning writer.
- Do not make `skill-authoring`, APR, `legacy-removal`, `plan-batch`, or
  `work-batch` a runtime mechanism for `add-to-ledger`.
- Do not change the accepted apply-only `ledger-store/v1` semantics or
  `planning-finding/v1` schema unless a focused failing proof exposes a
  mechanical contract gap; stop for replan before widening that owner.
- Do not repair the CCFG-25 plan-batch prose coupling or the CCFG-26 work-batch
  closeout failure.
- Do not install into, refresh, unlink, or rebind `/home/alacasse/.codex`.

## Accepted Ownership And Implementation Contract

### `add-to-ledger/v1`

The production owner is one installed feature consisting of:

- `skills/add-to-ledger/SKILL.md`, authored as one contract-first
  `skill-contract/v1` human command owner; and
- `scripts/add_to_ledger.py`, an internal implementation surface installed by
  the same feature and tested through explicit fixture planning roots.

Together they own:

- intake eligibility for one or more explicit source requests;
- source type, external identifier, title, URL or path, and compact evidence
  identity;
- normalization into individually addressable `planning-finding/v1` records;
- create, update, merge, or no-op meaning, including semantic duplicate and
  source-conflict decisions;
- the exact caller decision and idempotency key passed to `ledger-store/v1`;
  and
- the success/blocked result returned to the human command.

The internal implementation must distinguish:

- semantic duplicate/update/merge/no-op decisions made by the command owner;
- exact same-key/same-payload replay handled mechanically by the store;
- same-key/different-payload rejection;
- stale whole-ledger revision or file-hash refusal; and
- duplicate source identities inside one multi-item request, which block the
  whole request without partial write.

Outputs are canonical finding identities plus the existing store receipt, or a
blocked result naming the failed source/revision/identity condition. Do not
invent a new durable receipt or public schema when the existing store receipt
is sufficient.

Every success and blocked path must prove no selected dispatch, queued runway,
active runway, closeout, implementation, successor, or second ledger is
created.

### Neutral `planning-contracts` Mechanism

Register one new agent-facing manifest feature named `planning-contracts` that
installs the existing `scripts/planning_contract.py` and its existing closed
planning schema family. Its description and tests must classify it as a narrow
mechanism with no intake, duplicate, merge, selection, scope, closeout,
successor, or workflow ownership.

`add-to-ledger` may require `planning-artifacts`, `planning-state`, and
`planning-contracts`. It must no longer require APR or `legacy-removal`.
`skill-authoring` is used during implementation validation but remains absent
from runtime `requires`.

The neutral feature exists so later CCFG-25 and CCFG-26 work can consume the
same planning mechanisms without depending on another command owner. This
batch must not integrate those later commands.

### CCFG-23 Intake Scenario Migration

Preserve the scenario and contract identities:

- `intake-fresh-atomic`;
- `intake-multi-atomic`;
- `intake-duplicate-idempotent`;
- `intake-stale-blocked`;
- `INTAKE-SOURCE-001` through `INTAKE-STOP-005`.

Rebind their observations to the production `add-to-ledger/v1` owner operating
against temporary schema-valid ledgers. Add direct conflicting-source-identity,
same-key/different-payload, receipt-recovery, and no-state-effect coverage.
Delete `_run_intake`, `_new_finding`, and intake-only preserving tests only
after no scenario or non-migration caller uses them.

Do not require APR/Batch Runway topology, exact skill prose, a real canonical
planning write, or another command owner to keep the scenarios green.

### APR Narrowing

Remove from active APR skill/reference/metadata surfaces:

- broad finding intake and review-note normalization claims;
- `intake-findings` mode and ordinary create/update/merge/no-op decisions;
- the normal ledger mutation route used by `add-to-ledger`; and
- the runtime dependency from `add-to-ledger` to APR.

Preserve explicitly for later batches:

- CCFG-25: grouping, ranking, selection, dispatch, and queue preparation;
- CCFG-26: closeout interpretation and same-batch reconciliation.

No test may restore intake wording or dependency merely to preserve the old
shape.

### `legacy-removal` Evidence-Only Boundary

Remove its ability to act as an explicitly selected program owner, create or
update program queue state, select a dispatch, hand off directly to concrete
execution, reconcile lifecycle state, or own closeout.

Preserve evidence production for:

- legacy classification;
- canonical-model and compatibility evidence;
- cleanup-residue classification;
- dead-surface/deletion-test evidence consumption; and
- compact handoff findings to the actual command owner.

Add a behavioral `legacy-evidence-no-state-writes` proof that forbids selection,
queue mutation, lifecycle mutation, execution, reconciliation, and closeout.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker, reviewer, specialist, investigator, and Spark result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its other non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/test-quality-review/SKILL.md`
- `skills/dead-surface-audit/SKILL.md` for the legacy/compatibility cleanup
  trigger in Slices 2 through 4 and the final exact-range residue review

Overrides:

- Candidate installation is coordinator-owned and occurs only after Slice 5
  source validation and reviews accept the final exact feature/link set.
- Final exact-commit command-owner acceptance is coordinator-owned and runs
  once after a clean final candidate commit. Workers and reviewers must not run
  it independently.
- Every test-changing slice receives delta-only test-quality review after the
  normal independent review.
- Slice 1 and the final exact range require triggered
  `import_topology_reviewer` review because the batch adds an installed Python
  owner and imports the neutral planning-contract mechanism.
- Slices 2 through 4 and the final exact range require triggered
  `dead-surface-audit` support because they delete fixture, legacy-owner,
  compatibility, and test-retention surfaces. Its evidence informs but does not
  replace the final `runway_reviewer` verdict.
- Exact-range review for Slices 3 and 4 must verify both removed authority and
  explicitly preserved CCFG-25/26 or evidence-only responsibilities.

## Required Planning Snapshot

Interface: `cross-checkout-context/v1`.

Installed helper:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Canonical planning root:

```text
/home/alacasse/projects/codex-config/docs/plans
```

Complete validated plan-time payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: d739bd5660165fe321981ae0219a61c56667560b
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: d739bd5660165fe321981ae0219a61c56667560b
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: b38570bcd97b2584f3828abcd395b0f45ed91e58
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

This immutable planning snapshot is historical evidence, not a live execution
lease. At startup, `work-batch` must confirm this same runway and selected scope
through Planning State and obtain a fresh ready preflight. Immediately before
every worker/reviewer handoff it must prepare a fresh strict live lease,
validate the exact planning/implementation write scope, and propagate the live
context, canonical planning root, installed helper path, and write-bearing or
read-only role. Reject null or mismatched verified identity.

Do not rewrite this snapshot when the containing planning commit or later
between-flight commits advance stable `HEAD`.

## Project Values

- Planning artifact layout: Planning Artifact Layout v1.
- Planning location: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-24-intake-ownership-transfer/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`; pytest temporary directories and `/tmp/ccfg-24-*`
  acceptance artifacts are ephemeral.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: CCFG-33 exact-commit command-owner acceptance owner.
- Harness outputs:
  - `/tmp/ccfg-24-command-owner-result.json`
  - `/tmp/ccfg-24-command-owner-report.json`
  - `/tmp/ccfg-24-command-owner-report.txt`
- Summary artifacts: the accepted generated report, this runway,
  `completed-slices.md`, and `closeout.md`.
- Index/generated-doc refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus
  stable coordinator planning receipts that record candidate commit hashes.
- Dirty-file constraints: candidate writes only within the allowlist below;
  stable writes only active batch coordination artifacts and same-batch
  closeout state.

## Allowed Candidate Files And Areas

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
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
- `tests/test_add_to_ledger.py`
- `tests/fixtures/skill-contracts/migration/ccfg-24-intake-ownership/**`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/fixtures/command-owner-scenarios/workflow-cases.yaml`
- `tests/fixtures/command-owner-scenarios/workflow_adapters.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_deletion_test_vocabulary_ownership.py`
- `tests/test_codex_features_manifest.py`

## Read-Only Candidate Files Unless A Proven Mechanical Gap Blocks The Batch

- `scripts/planning_contract.py`
- `schemas/planning-current-v1.schema.json`
- `schemas/planning-finding-v1.schema.json`
- `schemas/planning-dispatch-v1.schema.json`
- `schemas/planning-runway-v1.schema.json`
- `schemas/planning-closeout-v1.schema.json`
- `schemas/planning-selection-transaction-v1.schema.json`
- `scripts/skill_contract.py`
- `schemas/skill-contract-v1.schema.json`
- `scripts/planning_state.py`
- `scripts/command_owner_scenarios.py`
- `skills/plan-batch/**`
- `skills/work-batch/**`
- `skills/batch-runway/**`
- cross-checkout helper, installer implementation, agent TOMLs, and stable
  planning artifact schemas

If a focused failure requires one of these files to change semantically, stop
and amend/replan rather than widening a worker handoff.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

Run candidate commands from
`/home/alacasse/projects/codex-config-command-owner-redesign` with its
`.venv/bin/python`. The stable checkout `.venv` currently lacks PyYAML for
planning/skill contract suites; those stable-interpreter collection errors are
`diagnostic-only`, not product failures or a dependency-install authorization.

### Current Required-Green Baselines

- Planning schema/store core:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py tests/test_planning_contract_store.py
  ```

  Status: `required-green`. Recorded result: 51 passed.

- Skill-contract schema/catalog/migration:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py
  ```

  Status: `required-green`. Recorded result: 42 passed.

- Current command-owner behavioral/catalog suite:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
  ```

  Status: `required-green`. Recorded result: 24 passed.

- Routing ownership:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_routing_rule_ownership.py
  ```

  Status: `required-green`. Recorded result: 5 passed.

- Strict cross-checkout and registered-agent contracts:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py
  ```

  Status: `required-green`. Recorded result: 33 passed and 187 subtests passed.

- Focused manifest mechanics:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'manifest_links_point_to_repo_sources or manifest_feature_requirements_are_valid or direct_request_prompts_preserve_command_owner_boundary or agent_facing_support_skills_are_not_ui_commands'
  ```

  Status: `required-green`. Recorded result: 4 passed, 17 deselected, and 34
  subtests passed.

- Candidate installer status and dry-run:

  ```sh
  ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
  ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
  ```

  Status: `required-green`. Recorded result: all current candidate features and
  links are exact; dry-run wrote no state.

### Known-Red Baselines

- Full manifest diagnostic:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
  ```

  Status: `known-red-baseline`. Recorded result: exactly 3 failed, 18 passed,
  and 202 subtests passed. After CCFG-24, the intake assertions must be green,
  while `test_executable_work_source_boundary_is_explicit` may remain red only
  for its named CCFG-25 plan-batch remainder. The two other failure identities
  remain CCFG-25 and CCFG-26. No additional failure is allowed.

- Broad legacy/projection diagnostic:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py
  ```

  Status: `known-red-baseline`. Recorded result: 12 failed, 19 passed, and 50
  subtests passed. CCFG-24 promotes only rewritten nodes that exercise APR
  intake removal and `legacy-removal` evidence-only behavior. Do not make the
  entire unrelated diagnostic a gate unless every baseline failure is
  explicitly classified and remediated inside this batch.

### Implementation-Created Then Required-Green Gates

Slice 1 creates focused `add-to-ledger/v1` tests and promotes them:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check
```

Slice 2 promotes the intake scenario migration:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
git diff --check
```

Slice 3 promotes APR intake-removal and ownership-migration proof:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_routing_rule_ownership.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py tests/test_codex_features_manifest.py -k 'add_to_ledger or architecture_program or command_owner_input_contracts'
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md skills/architecture-program-runway/SKILL.md
git diff --check
```

Run the shared
`test_executable_work_source_boundary_is_explicit` separately as
`known-red-baseline` and confirm its remaining failure concerns only the named
CCFG-25 plan-batch migration, not `add-to-ledger` or APR intake ownership.

Slice 4 promotes evidence-only legacy behavior:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py -k 'legacy_removal or legacy_evidence_no_state_writes or parallel_planning_systems'
git diff --check
```

Slice 5 promotes complete manifest/routing/install source state before the
coordinator mutates the candidate home:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_skill_routing_rule_ownership.py tests/test_codex_features_manifest.py -k 'not test_executable_work_source_boundary_is_explicit and not test_plan_batch_command_owner_runtime_boundaries_are_explicit and not test_work_batch_reconciles_same_batch_closeout'
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md skills/architecture-program-runway/SKILL.md
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py tests/test_skill_routing_rule_ownership.py tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py tests/test_codex_features_manifest.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check b38570bcd97b2584f3828abcd395b0f45ed91e58
```

The executor may narrow a `-k` expression when a named test does not exist yet,
but it must record the implementation-created test node and make the final
combined command concrete before closing the slice.

## Slice Shape

`slice_shape`: five slices.

- `1 -> 2`: Slice 1 creates one production owner with focused atomicity,
  identity, replay, CAS, and no-planning proof. Slice 2 consumes that owner from
  the behavioral catalog and may then remove the disposable adapter. This is a
  valid producer/consumer boundary with green intermediate behavior.
- `2 -> 3`: after intake behavior no longer depends on APR, contract narrowing
  can remove APR intake without combining behavioral migration and legacy
  deletion into one review/rollback boundary.
- `3 -> 4`: APR and `legacy-removal` retain different deferred responsibilities;
  their narrowing gates and tests must be reviewed independently.
- `4 -> 5`: installation and complete migration comparison must observe the
  accepted final semantic topology, so metadata/install reconciliation follows
  the owner-specific changes.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Establish production `add-to-ledger/v1` ownership | Pending | migration | None | Not run | Pending | Produce one contract-first owner and consume apply-only store |
| 2. Rebind and prune CCFG-23 intake scenarios | Pending | destructive-cleanup | None | Not run | Pending | Approval gate: replacement scenarios green and caller inventory zero |
| 3. Remove APR intake and normal ledger mutation | Pending | contract-narrowing | None | Not run | Pending | Preserve CCFG-25 planning and CCFG-26 closeout seams |
| 4. Make `legacy-removal` evidence-only | Pending | contract-narrowing | None | Not run | Pending | Preserve evidence vocabulary; remove state authority |
| 5. Reconcile installation, metadata, docs, and migration proof | Pending | migration | None | Not run | Pending | Candidate-only install after source review |

Detailed accepted slice results move to `completed-slices.md`; keep only active
or blocked rows here.

## Slice 1: Establish Production `add-to-ledger/v1` Ownership

### Scope

- Migrate `skills/add-to-ledger/SKILL.md` through `skill-authoring` v1 into one
  valid `skill-contract/v1` human command owner.
- Add the internal `scripts/add_to_ledger.py` implementation and focused tests.
- Make the command owner decide intake eligibility, source identity,
  normalization, duplicate/update/merge/no-op meaning, and exact store action.
- Consume only Planning State diagnostics, Planning Artifact placement, and the
  neutral `ledger-store/v1` mechanism.
- Use schema-valid temporary ledgers to prove fresh, multi-item, duplicate,
  conflict, replay, stale-revision, receipt-recovery, and stop behavior.
- Add before/after skill-contract migration fixtures and a policy proving the
  decisions move from APR/legacy routes to `add-to-ledger` without duplication.

### Allowed Files

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `tests/test_add_to_ledger.py`
- `tests/fixtures/skill-contracts/migration/ccfg-24-intake-ownership/**`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `CHANGELOG.md`

### Non-Goals

- Do not edit APR, `legacy-removal`, manifest installation, scenario adapters,
  planner/executor owners, or read-only store/schema semantics yet.
- Do not create a general public source-request schema or CLI framework beyond
  the narrow internal owner required by the installed skill.

### Acceptance Criteria

- Exactly one `skill-contract/v1` command owner claims the five intake
  decisions and no broad owner dependency.
- Multi-item intake applies atomically in one ledger transaction or writes
  nothing.
- Source identity conflicts block before mutation; duplicate, update, merge,
  no-op, exact replay, and mismatched replay are distinct.
- Stale ledger revision/hash and touched-finding revision mismatches write
  nothing.
- Successful retry after receipt interruption recovers the same receipt without
  applying twice.
- Every path creates no selected/queued/active/closeout/successor state.
- `ledger-store/v1` remains apply-only and schema/store baselines stay green.
- The intermediate source state is green while old callers remain temporarily
  present for Slice 2/3 migration.

### Validation And Review

- Test quality review: `delta-only`.
- Run Slice 1 implementation-created gates plus planning/skill-contract core
  baselines.
- Normal independent review checks exact contract ownership, source identity,
  CAS/replay behavior, and absence of a second store.
- Triggered `import_topology_reviewer` checks that the new production module
  imports only neutral mechanisms, has no APR/legacy command-owner dependency,
  and does not create a parallel owner path.
- Delta-only test-quality review checks atomicity assertions, negative paths,
  anti-self-certification, and fixture realism.

### Worker Brief

The spawned `runway_worker` is already the required coding subagent. Read this
runway from the stable planning checkout, implement only Slice 1 in the
candidate checkout, and do not spawn, delegate to, or wait on additional
agents. Do not run final acceptance, install either generation, edit stable
planning, or touch APR/legacy cleanup. Return the v2 compact result with exact
changed paths and verified strict context.

### Reviewer Brief

Review the exact task-scoped diff supplied by the coordinator. Verify the new
owner makes semantic decisions and the store only applies them, all failure
paths are non-mutating, and no public framework or later-command ownership was
introduced. Echo `diff_basis` and verified strict context in the v2 result.

### Commit

`feat: establish add-to-ledger intake ownership`

### Slice Stop Conditions

- Stop if the accepted owner/interface or neutral store boundary cannot be
  expressed without inventing a broad public protocol.
- Stop if `planning_contract.py` or a schema semantic change appears necessary.
- Stop if tests can pass without observing real ledger effects and receipts.
- Stop if the command owner selects or creates downstream work.

## Slice 2: Rebind And Prune CCFG-23 Intake Scenarios

### Approval Gate

Authority: COR-007 plus green Slice 1 replacement behavior.

Before deletion, the coordinator must record:

- all four stable intake scenario IDs execute through the production owner;
- direct source-conflict, replay, stale-CAS, and no-state-effect tests are green;
- a repository caller inventory finds no non-migration caller of `_run_intake`
  or `_new_finding`; and
- the remaining CCFG-23 contracts/families stay topology-independent.

If any fact is missing, keep the helpers temporarily with named caller, reason,
owner, and removal condition, block Slice 2, and do not continue to Slice 3.

### Scope

- Rebind catalog intake scenarios and workflow cases to production
  `add-to-ledger/v1` observations.
- Preserve scenario/contract IDs and aggregate acceptance mappings.
- Add or migrate behavioral assertions for identity conflict, semantic
  duplicate versus exact replay, multi-item atomicity, stale refusal, and
  no-planning effects.
- Delete `_run_intake`, `_new_finding`, and tests that only preserve their
  topology after the gate is satisfied.

### Allowed Files

- `scripts/add_to_ledger.py`
- `tests/test_add_to_ledger.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/fixtures/command-owner-scenarios/workflow-cases.yaml`
- `tests/fixtures/command-owner-scenarios/workflow_adapters.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `CHANGELOG.md`

### Non-Goals

- Do not change non-intake scenario meanings, accepted aggregate keys, report
  semantics, planner/executor adapters, or source-hash authority already removed
  by CCFG-33.
- Do not change APR or `legacy-removal` yet.

### Acceptance Criteria

- Four stable intake scenarios observe the production owner and schema-valid
  temporary ledger effects.
- All five intake contracts remain green without APR/Batch Runway topology or
  exact prose.
- Disposable intake adapter logic and its preserving tests are absent after the
  gate, or Slice 2 is explicitly blocked with a named retained caller/reason.
- Non-intake behavioral/catalog tests remain green.
- The complete diff has delta-only test-quality approval.

### Validation And Review

- Test quality review: `delta-only`.
- Triggered specialist: `dead-surface-audit` for the exact adapter/helper/test
  deletion candidates and caller evidence.
- Run Slice 2 gates and the current complete behavioral/catalog suite.
- Independent review verifies scenario meaning, failure coverage, and deletion
  evidence.
- Delta-only test-quality review verifies the new tests protect behavior rather
  than the new module/topology.

### Worker Brief

The spawned `runway_worker` must implement only Slice 2, must not delegate, and
must not change APR, `legacy-removal`, manifest, or installation. Delete only
fixture logic whose caller inventory and replacement evidence satisfy the gate.
Do not run final acceptance. Return exact paths and v2 verified context.

### Reviewer Brief

Review the supplied exact diff. Reject any self-certifying fixture replacement,
loss of scenario meaning, deletion without caller proof, or new dependency on
legacy topology. Echo `diff_basis` and verified context.

### Commit

`test: bind intake scenarios to add-to-ledger`

### Slice Stop Conditions

- Stop if a stable intake scenario cannot run through the production owner.
- Stop if deleting an adapter would remove the only proof of an accepted
  behavior.
- Stop on changes to non-intake behavior or aggregate acceptance semantics.

## Slice 3: Remove APR Intake And Normal Ledger Mutation

### Approval Gate

Authority: DEC-001, DEC-005, DEC-037, and COR-007.

The coordinator may unlock this slice only when Slice 2 intake scenarios are
green through the production owner and the intended diff preserves APR's named
CCFG-25 planning plus CCFG-26 closeout responsibilities.

### Scope

- Remove APR intake/normalization, `intake-findings`, create/update/merge/no-op,
  and normal ledger mutation authority from active skill/reference/metadata
  surfaces.
- Remove the `add-to-ledger -> architecture-program-runway` runtime dependency.
- Update routing tests and the CCFG-24 half of the shared executable-work source
  boundary.
- Preserve the explicit planner and closeout support seams for CCFG-25/26.

### Allowed Files

- `skills/add-to-ledger/**`
- `skills/architecture-program-runway/SKILL.md`
- `skills/architecture-program-runway/agents/openai.yaml`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `codex-features.json`
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `tests/test_codex_features_manifest.py`
- `CHANGELOG.md`

### Non-Goals

- Do not remove APR selection, grouping, ranking, dispatch, queue, closeout, or
  reconciliation support.
- Do not change `plan-batch` or `work-batch` source/prose to make manifest tests
  green.
- Do not delete the APR feature or runner script.

### Acceptance Criteria

- No active APR contract, mode, prompt, reference, manifest description, or
  routing rule owns intake/normalization/normal ledger mutation.
- `add-to-ledger` has no APR dependency and remains green through neutral
  mechanisms.
- Migration comparison proves the five semantic decisions moved exactly once.
- CCFG-25 planning and CCFG-26 closeout support remain explicit and testable.
- The shared executable-work-source test contains no old add-to-ledger/APR
  preservation claim; any remaining red assertion is clearly assigned to the
  CCFG-25 planner migration.

### Validation And Review

- Test quality review: `delta-only`.
- Triggered specialist: `dead-surface-audit` for APR intake modes, routing
  fallbacks, and topology-preserving tests.
- Run Slice 3 gates plus focused command-owner intake tests.
- Independent review verifies exact ownership removal and named preservation.
- Delta-only test-quality review checks migration tests do not preserve APR
  topology or exact wording.

### Worker Brief

The spawned `runway_worker` implements only APR intake narrowing. Do not delete
the APR feature, runner, planning, or closeout paths; do not delegate; do not
install. Return v2 verified context and exact paths.

### Reviewer Brief

Review the exact supplied diff and migration catalog. Reject retained intake
authority, duplicated semantic decisions, or accidental CCFG-25/26 deletion.
Echo `diff_basis` and verified context.

### Commit

`refactor: remove APR intake ownership`

### Slice Stop Conditions

- Stop if target intake tests are not green before narrowing.
- Stop if APR planning or closeout responsibility would be lost.
- Stop if the diff merely renames intake modes or preserves a fallback route.

## Slice 4: Make `legacy-removal` Evidence-Only

### Approval Gate

Authority: DEC-019, COR-007, and green deletion/dead-surface evidence
vocabulary.

The coordinator may unlock this slice only when a focused
`legacy-evidence-no-state-writes` test exists and the intended diff preserves
classification/evidence handoff while removing lifecycle authority.

### Scope

- Remove `legacy-removal` program-owner selection, queue, selected dispatch,
  concrete-runway handoff, execution, reconciliation, and closeout escape
  hatches.
- Update Planning Artifact consumer wording and APR ledger template references
  that still grant those routes.
- Rewrite/delete topology tests that preserve legacy state authority.
- Preserve evidence classification, canonical-model/compatibility decisions,
  cleanup residue, and dead-surface/deletion-test status consumption.

### Allowed Files

- `skills/legacy-removal/SKILL.md`
- `skills/planning-artifacts/SKILL.md`
- `skills/architecture-program-runway/references/program-ledger-template.md`
- `codex-features.json`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_deletion_test_vocabulary_ownership.py`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `CHANGELOG.md`

### Non-Goals

- Do not delete `legacy-removal`, `dead-surface-audit`, deletion-test evidence
  statuses, classification guidance, or evidence handoff.
- Do not move lifecycle authority into another support/evidence skill.

### Acceptance Criteria

- `legacy-removal` cannot select, queue, dispatch, execute, reconcile, close, or
  mutate lifecycle state.
- Evidence outputs remain consumable by the actual command owner.
- `legacy-evidence-no-state-writes` is green.
- No parallel planning system, direct Batch Runway handoff, or program-owner
  exception remains.
- Deletion/dead-surface vocabulary tests remain behaviorally meaningful.

### Validation And Review

- Test quality review: `delta-only`.
- Triggered specialist: `dead-surface-audit` for program-owner escape hatches,
  compatibility residue, and tests that retain lifecycle authority.
- Run Slice 4 focused promoted nodes and migration tests.
- Independent review verifies evidence stays while state authority disappears.
- Delta-only test-quality review checks assertions protect the evidence/state
  boundary instead of old headings or topology.

### Worker Brief

The spawned `runway_worker` implements only the evidence-only narrowing and
must not delegate, delete the skill, or change plan/work ownership. Return v2
verified context and exact paths.

### Reviewer Brief

Review the exact supplied diff. Reject any surviving lifecycle escape hatch or
loss of required evidence vocabulary. Echo `diff_basis` and verified context.

### Commit

`refactor: make legacy removal evidence only`

### Slice Stop Conditions

- Stop if evidence behavior is deleted rather than separated from state
  authority.
- Stop if another support skill becomes a program owner.
- Stop if unrelated broad known-red tests are pulled into scope.

## Slice 5: Reconcile Installation, Metadata, Docs, And Migration Proof

### Scope

- Register neutral `planning-contracts` with the existing planning contract
  script and schema family.
- Register the final `add-to-ledger` production script/link set and update
  feature versions for all meaningfully changed installed features.
- Make final `requires` and descriptions reflect one command owner plus neutral
  mechanisms and evidence-only support.
- Reconcile routing docs, workflow guide, README, changelog, authoring migration
  guards, and focused manifest tests.
- After source validation and normal plus test-quality reviews are clean, have
  the coordinator install/update only the candidate Codex home.
- Prove stable default-home ownership remains unchanged.

### Allowed Files

- all allowed batch files needed for final consistency
- `codex-features.json`
- `README.md`
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `CHANGELOG.md`
- focused manifest/routing/migration tests and fixtures

### Non-Goals

- Do not mutate stable installed state, switch defaults, install a fresh global
  generation, delete APR/Batch Runway features, or begin CCFG-25.
- Do not make `planning-contracts` a workflow owner or `skill-authoring` a
  runtime dependency.

### Acceptance Criteria

- `planning-contracts` installs one neutral script and the existing schema
  family, with no workflow decisions.
- `add-to-ledger` installs its skill and internal production implementation and
  requires only narrow mechanisms.
- APR and `legacy-removal` installed metadata contain no intake/lifecycle
  authority removed by prior slices.
- Candidate status/dry-run/install/status are exact; all relevant installed
  links resolve only to the candidate checkout.
- Stable status/dry-run and link ownership remain equivalent to baseline; no
  stable install/write occurs.
- Complete skill migration validation proves one owner, no retained broad-owner
  dependency, no duplicated durable fact, and meaningful contract change.
- Focused source validation, Ruff, BasedPyright, manifest/routing tests,
  complete-range independent review, and complete-range delta-only test-quality
  review are clean.

### Candidate Installation Commands

Coordinator-owned after source review:

```sh
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature planning-contracts
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature add-to-ledger
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature architecture-program-runway
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature legacy-removal
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
```

If the installer cannot safely converge partial feature updates into the exact
manifest state, use one candidate-only full install after review. Never install
or refresh the stable home.

### Validation And Review

- Test quality review: `delta-only`.
- Run Slice 5 combined gates and candidate installer checks.
- Verify installed link targets exactly, including `scripts/add_to_ledger.py`,
  `scripts/planning_contract.py`, and the declared schemas.
- Independent exact-range review verifies COR-007, DEC-037, CCFG-25/26
  preservation, and no candidate canonical write.
- Triggered exact-range `import_topology_reviewer` verifies the installed
  module/link/import graph has one command owner, one neutral store mechanism,
  and no legacy fallback edge.
- Triggered exact-range `dead-surface-audit` verifies no unclassified APR,
  `legacy-removal`, fixture-adapter, compatibility, or test-retention residue
  survives the CCFG-24 ownership transfer.
- Delta-only exact-range test-quality review verifies behavioral confidence and
  no topology-preserving regressions.

### Worker Brief

The spawned `runway_worker` performs source/metadata/docs/test consistency only,
must not install either home, must not delegate, and must not edit stable
planning. Return v2 verified context and exact paths. Candidate installation is
coordinator-owned after review.

### Reviewer Brief

Review the exact task/range diff supplied by the coordinator. Verify one owner,
neutral mechanism installation, no broad dependency, exact feature links,
stable-home non-mutation, and no CCFG-25+ work. Echo `diff_basis` and verified
context.

### Commit

`feat: complete add-to-ledger ownership transfer`

### Slice Stop Conditions

- Stop if manifest/install topology leaves APR required for intake mechanics.
- Stop if `planning-contracts` gains semantic workflow ownership.
- Stop if candidate install would touch the stable home or default binding.
- Stop if final migration guards or exact-range reviews are not clean.

## Final Validation

After all five slice commits and candidate installation:

1. Confirm Planning State still identifies this same queued/active CCFG-24
   scope and no successor; obtain a fresh strict lease and validate final
   read-only review scope.
2. Run complete required-green planning-store, skill-contract, intake,
   behavioral/catalog, routing, focused legacy-evidence, cross-checkout,
   manifest, Ruff, BasedPyright, installer-status/dry-run, and candidate-range
   whitespace gates.
3. Run the full manifest diagnostic and verify no new failure. Any remaining
   failures must be only the explicitly deferred CCFG-25/26 identities and
   reasons; no CCFG-24 intake assertion may remain red.
4. From a clean exact candidate commit, run once:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/command_owner_scenarios.py accept tests/fixtures/command-owner-scenarios --result-output /tmp/ccfg-24-command-owner-result.json --json-report-output /tmp/ccfg-24-command-owner-report.json --text-report-output /tmp/ccfg-24-command-owner-report.txt
   ```

5. Read and validate the generated result and both reports. Confirm one
   evidence-pytest process, all 69 scenario meanings, 31 contracts, 17
   families, six keys, six aliases, negative-runtime outcomes, provenance, and
   the migrated intake family are green.
6. Prove the candidate installed `add-to-ledger` and `planning-contracts` links
   resolve only to the candidate; prove every default stable-home link still
   resolves only to stable.
7. Verify exact implementation range and no unauthorized file, generated
   artifact, credential, canonical planning write, package install, default
   switch, or CCFG-25+ change.
8. Obtain clean complete-range independent, triggered import-topology, and
   delta-only test-quality reviews.
9. Write `completed-slices.md` and `closeout.md`, reconcile only CCFG-24, clear
   selected/queued/active state, and stop before successor selection.

## Batch Stop Conditions

- Stop if Planning State no longer reports this selected scope or reports
  another queued/active batch.
- Stop if strict cross-checkout preflight, live lease, verified agent identity,
  or exact write scope fails.
- Stop on unexpected repository movement, dirty-file conflict, or candidate
  writes outside the allowlist.
- Stop if any candidate process mutates canonical planning state.
- Stop if semantic intake decisions move into `ledger-store/v1` or another
  support skill.
- Stop if production ownership remains prose-only or fixture-only.
- Stop if a destructive/contract-narrowing approval gate is not satisfied.
- Stop if fixture adapter deletion precedes green replacement behavior.
- Stop if APR planning/closeout seams reserved for CCFG-25/26 are removed.
- Stop if `legacy-removal` evidence vocabulary is lost or another evidence
  skill gains lifecycle authority.
- Stop if installed feature convergence requires a stable-home mutation or
  default-generation switch.
- Stop if final acceptance, exact-range review, or test-quality review is not
  clean.
- Stop after same-batch CCFG-24 closeout with no successor selected.
