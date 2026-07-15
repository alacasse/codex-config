# CCFG-23 Topology-Independent Behavioral Scenario Harness Runway

## Purpose

Implement and validate one non-installed behavioral scenario harness in the
candidate checkout. The harness owns scenario records, observation comparison,
catalog validation, and deterministic coverage reporting. It proves accepted
source and target behavior without owning or migrating the command workflows
being observed.

This runway covers CCFG-23 only. Closeout may mark CCFG-23 `Closed` only when
all six COR-006 keys, their migration-program aliases, and every live
carry-forward scenario are green. Otherwise preserve the exact blocker and
stop without selecting a successor.

## Batch Kind And Slice Risk Contract

- Batch kind: `characterization`.
- Slice 1 risk: `evidence-only`; it creates the scenario contract, harness,
  catalog skeleton, and self-tests without changing a supported workflow.
- Slice 2 risk: `evidence-only`; it binds fixture-owned workflow behavior and
  planning-quality scenarios without transferring command ownership.
- Slice 3 risk: `evidence-only`; it binds Planning State, Git-integrity, strict
  handoff, and fault scenarios in isolated repositories.
- Slice 4 risk: `evidence-only`; it proves generation/cutover/absence behavior
  in disposable fixtures without touching an installed generation.
- Authorized evidence work: one schema-backed harness, fixture catalogs and
  adapters, focused tests, ephemeral coverage output, and one changelog entry.
- Production ownership transfer, live planning migration, contract narrowing,
  destructive cleanup, real installation, default switching, and bridge
  deletion: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such
  operation is authorized.
- Candidate-checkout filesystem approval may be required at execution time. It
  authorizes only the validated candidate paths and no external mutation.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Planning-state `current` and `validate` passed with no blockers and only the
  two known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable checkout: `/home/alacasse/projects/codex-config`, branch `master`,
  plan-time `HEAD` `3fbec1ba80884e4f35bd10c3fdf4f90578358011`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, exact `HEAD`
  `2f3995060a309b27ba22d8d7e80f7d07d0b4a34f`.
- Both worktrees were clean before planning. Planning performs no candidate
  write.
- Stable Codex home: `/home/alacasse/.codex`. The installed strict-context
  helper resolves to the stable checkout. Status succeeds with known manifest
  version drift; dry-run reports stable-owned links without writing.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
  Status reports exact candidate manifest versions and dry-run reports only
  candidate-owned links without writing.
- Accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c` is present in candidate ancestry.
- CCFG-19 closed the immutable 31-contract source mapping and required
  decisions. CCFG-21 closed the planning artifacts and selection-transaction
  contracts. CCFG-22 closed the candidate-only skill-authoring prerequisite.
- The candidate has no behavioral scenario schema, scenario harness owner,
  command-owner scenario fixture catalog, or focused scenario test module.
- `scripts/planning_contract.py`, `scripts/planning_state.py`, and
  `scripts/cross_checkout_context.py` expose useful public behavior seams but
  remain read-only and do not become the harness owner.
- The candidate strict helper intentionally does not own the stable-only live
  refresh/preflight topology. Scenarios must assert ready/blocked outcomes and
  material integrity rather than copying those helper names.
- Existing required-green baseline: 309 planning, Planning State,
  strict-context, and agent-contract tests plus 187 subtests; 32 pre-creation
  tests plus 39 subtests; and 4 focused manifest tests plus 34 subtests.
- The full manifest remains a known-red diagnostic with exactly 3 unrelated
  failures, 18 passes, and 202 subtests.

The queued stable planning artifacts are expected dirty coordination state. Do
not copy them into the candidate checkout. The persisted context below is a
planning snapshot, not a live execution lease. Repository movement requires a
fresh ready/blocked preflight or later lease renewal; it must not rewrite this
snapshot.

## Batch Non-Goals

- Do not edit, migrate, or reimplement `add-to-ledger`, `plan-batch`,
  `work-batch`, Architecture Program Runway, Batch Runway, or their ownership
  dependencies.
- Do not modify the closed skill, planning, transaction, or authoring schemas,
  validators, fixtures, tests, skills, or feature registration.
- Do not make Planning State a command decision owner or make Git history,
  fingerprints, ancestry, dirty files, or changed paths into queue semantics.
- Do not expand `scripts/planning_contract.py`, `scripts/planning_state.py`,
  `scripts/cross_checkout_context.py`, or installer code into the new harness
  owner.
- Do not execute arbitrary scenario `command` strings. They are stable semantic
  invocation labels consumed by fixture-owned adapters.
- Do not count a declared but unbound future production interface as green
  production implementation. Report binding state honestly.
- Do not require old APR/Batch Runway names, paths, modes, exact prompt prose,
  dependency lists, compatibility aliases, or historical helper topology.
- Do not install or mutate either Codex home, mutate canonical planning state
  from the candidate, switch the default generation, delete a live route, or
  remove the temporary bridge.
- Do not fix or weaken the three known-red manifest assertions, update unrelated
  versions, or absorb installer drift.

## Acceptance Key Map

COR-006 closes only with these exact keys:

```yaml
source_characterization_green: true
target_interfaces_green: true
bootstrap_cutover_green: true
fault_injection_green: true
contract_coverage_complete: true
legacy_topology_not_required: true
```

The migration-program aliases must also be emitted and green:

```yaml
source_characterization_green: true
target_interface_scenarios_green: true
bootstrap_and_cutover_scenarios_green: true
fault_injection_scenarios_green: true
contract_id_coverage_report_complete: true
legacy_skill_names_not_required_except_migration_fixtures: true
```

Closeout must map catalog validation, scenario observations, focused tests,
coverage JSON, fixture isolation, and independent review to every key. One
aggregate pytest result is insufficient.

The report must separately enumerate and prove the live carry-forward groups:

- planning quality: cohesive one-slice validity, semantic multi-slice reasons,
  minimum viable scope, non-authoritative topology narrowing, pre-queue
  expansion blocking, explicit narrowly scoped user approval for residual
  material complexity, direct independent invocation of registered
  `batch_planner` and `batch_plan_reviewer` roles, a prohibition on the planner
  invoking or framing evidence for its reviewer, and no executable stale or
  undecided draft;
- execution currentness: Planning State-only semantic currentness, Git-only
  material integrity, permitted stable/toolchain movement, blocked unexpected
  implementation movement, blocked movement during preparation, and protected
  handoff leases/results/scopes/receipts/reviewer bases; and
- cutover lifecycle: minimum temporary pre-cutover bridge operation under
  canonical master planning plus synthetic final bridge absence with no target
  behavior dependency on legacy topology.

## Required Strict Execution Context

Mode: explicit `cross-checkout-context/v1`.

Installed helper path used for planning validation:

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

Planning loaded the installed helper, verified that it resolves under the
declared toolchain root, parsed the complete payload, and called
`validate_write_scope` with these four canonical planning paths:

- `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/dispatch.md`
- `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/runway.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`

It also validated these eight intended candidate paths or file areas:

- `schemas/command-owner-scenario-v1.schema.json`
- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_currentness.py`
- `tests/test_command_owner_scenario_cutover.py`
- `CHANGELOG.md`

Validation passed. Planning performed no candidate write.

Before the first worker or reviewer delegation, the coordinator must follow
`skills/batch-runway/references/cross-checkout-context-v1.md` and call the
canonical ready/blocked preflight with this immutable planning snapshot. Before
every later delegation, prepare a fresh live execution lease, validate the
active slice's exact write scope, and pass the live context, canonical planning
root, absolute helper path, and write-bearing/read-only mode. Every explicit
cross-checkout agent result must carry matching non-null
`verified_cross_checkout_context` evidence.

Disposable repositories and install roots created under pytest temporary paths
are candidate test artifacts, not new control-plane roots and not authorization
to touch a real Codex home.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`; report JSON, pytest temporary paths, isolated Git roots,
  and disposable install roots are ephemeral.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway`.
- Integration harnesses:
  - the implementation-created `scripts/command_owner_scenarios.py` validation
    and report commands;
  - focused pytest for scenario contract, workflow, currentness, fault, and
    cutover behavior;
  - existing planning, Planning State, strict-context, pre-creation, and
    focused manifest tests;
  - read-only stable/candidate installer status and dry-run controls.
- Harness output: stdout JSON and pytest temporary paths only; no durable
  generated output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index/generated-doc refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus a
  separate stable planning-ledger receipt after each candidate hash exists.
- Dirty-file constraints: candidate starts clean and may change only active
  slice files; stable changes remain limited to this batch's planning artifacts
  and same-batch reconciliation.
- Test quality review: `delta-only` for every test-changing slice and the final
  exact candidate range.

## Scenario Interface And Ownership

`scripts/command_owner_scenarios.py` is the only harness owner. It must remain
project-local and non-installed. It owns:

- loading and validating `command-owner-scenario/v1` records;
- rejecting duplicate IDs, unknown contracts, unknown fields, unsafe paths,
  malformed observations, and unsupported versions;
- comparing a fixture adapter's observed transition, writes, forbidden writes,
  stop reason, root/generation facts, and validation evidence to expectations;
- refusing to execute the record's semantic `command` label;
- distinguishing `declared`, `bound`, `green`, `blocked`, and `unavailable`
  evidence without counting unbound declarations as green; and
- emitting deterministic human-readable validation and JSON coverage reports.

The fixture catalog owns project-specific contract IDs, scenario families,
semantic command labels, expected observations, and adapter bindings. The
harness script must not hard-code codex-config paths, CCFG IDs, legacy skill
names, stable-only helper APIs, or validation commands.

The accepted 31 contract IDs are immutable source identity. The committed
catalog may copy those IDs with accepted snapshot provenance so runtime
coverage does not require Git history. Tests and independent review must verify
the catalog is exact: no missing, extra, renamed, or duplicate ID.

Fixture adapters may call existing public Python/CLI seams or operate on
temporary Layout v1/Git/install roots. Shared scenario assertions must depend
only on the scenario contract and observed effects. A legacy runner adapter is
allowed only for source characterization and must not leak its phases, modes,
result fields, paths, or dependency topology into shared expectations.

Slices 2 through 4 consume the Slice 1 harness contract. They must not widen or
redefine it. If a missing generic capability is discovered, stop and amend the
same slice explicitly rather than silently coupling a scenario to topology.

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
Use the expanded convergence template only for expanding scope, significant
uncertainty, blockers, or final batch reporting.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/test-quality-review.md`
- `skills/test-quality-review/SKILL.md`

Overrides:

- Candidate implementation commits and stable planning-ledger receipt commits
  are distinct cross-repository commits. Record both hashes per slice.
- Workers use the existing locked candidate `.venv`. They may not install
  packages or modify `pyproject.toml` or `uv.lock`.
- No worker or coordinator may install a feature, mutate a real Codex home,
  change the default binding, or write canonical planning state from the
  candidate. Read-only status/dry-run controls are coordinator-owned.
- Every slice receives `test-quality-review` in `delta-only` mode. Actionable
  findings enter the normal reviewer fix/block loop; clean output is recorded
  compactly.
- Final independent review must reject topology-only assertions and verify that
  fixture absence is not reported as real bridge deletion.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

### Current Required-Green Baseline

Run from the candidate checkout unless a command names the stable checkout.

- Planning, state, strict-context, and agent contracts:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py tests/test_planning_contract_artifacts.py tests/test_planning_transaction.py tests/test_planning_contract_store.py tests/test_planning_state.py tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py
  ```

  Status: `required-green`. Current result: 309 passed and 187 subtests passed.

- Pre-creation isolation contracts:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_precreation.py
  ```

  Status: `required-green`. Current result: 32 passed and 39 subtests passed.

- Focused manifest ownership subset:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'manifest_links_point_to_repo_sources or manifest_feature_requirements_are_valid or direct_request_prompts_preserve_command_owner_boundary or agent_facing_support_skills_are_not_ui_commands'
  ```

  Status: `required-green`. Current result: 4 passed, 17 deselected, and 34
  subtests passed.

- Stable installer read-only controls, run from the stable checkout:

  ```sh
  ./install.sh --status
  ./install.sh --dry-run
  ```

  Status: `required-green`. Both exit successfully. Status has known manifest
  version drift; dry-run reports stable-owned links and no write.

- Candidate installer read-only controls:

  ```sh
  ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
  ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
  ```

  Status: `required-green`. Both exit successfully with exact candidate-owned
  links and no write.

- Shared per-slice diff gate:

  ```sh
  git diff --check
  ```

  Status: `required-green`. Current result: passed. Re-run after every slice;
  whitespace errors block review and commit.

### Implementation-Created Commands

Slice 1 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/command_owner_scenarios.py report tests/fixtures/command-owner-scenarios --format json
.venv/bin/ruff check --no-cache scripts/command_owner_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/basedpyright scripts/command_owner_scenarios.py
```

Slice 2 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/command_owner_scenarios.py report tests/fixtures/command-owner-scenarios --format json
.venv/bin/ruff check --no-cache tests/test_command_owner_behavioral_scenarios.py
```

Slice 3 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py tests/test_command_owner_scenario_currentness.py tests/test_planning_state.py -k 'command_owner_scenario or current_and_validate_json_agree or missing_program_current or historical_batch_artifacts or select_batch or queue_batch'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_cross_checkout_precreation.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/command_owner_scenarios.py report tests/fixtures/command-owner-scenarios --format json
.venv/bin/ruff check --no-cache tests/test_command_owner_scenario_currentness.py
```

Slice 4 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/command_owner_scenarios.py report tests/fixtures/command-owner-scenarios --format json
.venv/bin/ruff check --no-cache scripts/command_owner_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py
.venv/bin/basedpyright scripts/command_owner_scenarios.py
```

### Known-Red And Diagnostic-Only Commands

- Full manifest:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
  ```

  Status: `known-red-baseline`. Current candidate result remains exactly 3
  failed, 18 passed, and 202 subtests passed in these unrelated assertions:
  `test_executable_work_source_boundary_is_explicit`,
  `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
  `test_work_batch_reconciles_same_batch_closeout`.

- Accepted-design source comparison and static legacy-name scans are
  `diagnostic-only` until the focused scenario tests turn their exact expected
  catalog/allowlist into required-green evidence. They must not read archives
  as active state or make historical names into target requirements.

### Conditional Commands

- No full project pytest suite, package install, generated-doc refresh,
  graph/index refresh, feature install, default-home mutation, or live cutover
  harness is part of per-slice work.
- If a slice changes only fixture YAML and its focused Python test, it need not
  re-run unrelated project modules beyond the commands assigned above.
- If a proposed change touches any production workflow owner, installed
  feature, existing schema/validator, installer, or stable helper, stop for
  scope drift rather than adding a validation exception.

## Shared Worker And Reviewer Briefs

Worker brief for every slice:

- You are the already-required `runway_worker`. Implement only the active slice
  from this runway; do not spawn, delegate to, or wait on another agent.
- Independently validate the fresh strict cross-checkout live lease before
  acting, then write only inside the candidate checkout and only to the active
  slice's allowed files.
- Keep stable planning files, accepted design history, closed CCFG-19/21/22
  outputs, existing command owners, Planning State, planning-contract owners,
  strict helpers, installers, manifests, and Codex homes read-only.
- Preserve one non-installed harness owner and one
  `command-owner-scenario/v1` dialect. Do not add a parallel parser, schema,
  harness, command path, or installed feature.
- Use fixture-owned semantic adapters and observable file/state effects. Do not
  execute scenario labels or preserve legacy topology in shared assertions.
- Run only the focused validation assigned to the slice and return the
  registered v2 worker result with matching
  `verified_cross_checkout_context`.

Reviewer brief for every slice:

- The coordinator supplies the exact candidate commit hash or task-scoped
  candidate worktree diff basis. Echo it as `diff_basis` in the registered v2
  reviewer result.
- Independently validate a fresh strict cross-checkout live lease before review.
- Review against COR-006, DEC-015, the immutable behavior contracts/matrix, the
  live CCFG-23 amendment, and the active slice's acceptance criteria.
- Verify behavior through scenario records, observed transitions/file effects,
  fixture isolation, and deterministic reports rather than old paths, modes,
  prompt prose, dependencies, or helper names.
- Run `test-quality-review` in `delta-only` mode for the changed-test delta and
  include its compact result.
- Reject command-owner migration, live planning mutation, real install/cutover,
  arbitrary command execution, false green unbound interfaces, or fixture
  absence represented as real bridge deletion.
- Return matching `verified_cross_checkout_context` and a clear
  accept/fix/block verdict.

## Active Ledger

| Slice | Risk | Status | Candidate commit | Stable receipt | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|---|
| 3. Currentness and protected handoffs | evidence-only | pending | | | | | Planning State/Git/lease/fault evidence green | |
| 4. Disposable cutover and aggregate gate | evidence-only | pending | | | | | Six COR-006 keys and aliases green | |

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Slice Shape

- `1 -> 2`: Slice 1 creates the closed-world scenario contract, adapter
  boundary, validation/report CLI, and exact 31-contract catalog. Slice 2
  consumes that stable owner to bind workflow behavior. The unbound but honest
  catalog is a valid, green intermediate state and cannot falsely satisfy the
  target exit keys.
- `2 -> 3`: Slice 2 uses planning-contract stores and fixture workflow adapters
  for intake/planning/execution/closeout behavior. Slice 3 moves to the separate
  Planning State and strict cross-checkout owner seams, isolated Git roots, and
  material-movement fault model. The Slice 2 workflow evidence remains valid
  independently of live-lease mechanics.
- `3 -> 4`: Slice 3 proves semantic currentness and protected handoffs before
  Slice 4 enters disposable installer/switch/rollback/physical-absence
  fixtures. The install-sandbox boundary has different side-effect controls,
  review risk, and rollback proof even though no real installation is allowed.

Four slices are required by producer/consumer, owner-seam, execution-environment,
and side-effect boundaries, not by a target count. Documentation and metadata
stay with Slice 4 and do not become filler slices.

## Slice 1: Establish The Scenario Contract And Harness

Risk: `evidence-only`.

Test quality review: `delta-only`.

Scope:

- Add the closed-world `command-owner-scenario/v1` schema.
- Add one non-installed harness owner with pure catalog validation,
  expectation/observation comparison, and deterministic text/JSON reporting.
- Add the immutable 31-contract ID catalog, accepted scenario-family skeleton,
  binding/evidence status fields, and self-test fixtures.
- Add focused tests for schema closure, duplicate/unknown rejection, safe paths,
  semantic labels, deterministic output, honest unavailable reporting, and
  exact source-contract identity.

Allowed files:

- `schemas/command-owner-scenario-v1.schema.json`
- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/`
- `tests/test_command_owner_scenario_catalog.py`

Non-goals:

- No workflow, currentness, fault, installer, cutover, or deletion adapter yet.
- No edit to accepted design, existing schemas/scripts/tests, manifest,
  installer, README, changelog, or installed home.
- No shell execution of scenario command labels.

Acceptance criteria:

- The schema is closed-world and versioned exactly
  `command-owner-scenario/v1`; missing, duplicate, unknown, malformed, and
  unsupported content fails deterministically.
- The scenario record preserves the accepted fields for contracts, initial
  artifacts, semantic command, expected transition/writes/forbidden writes,
  expected stop, roots/generation, and validation evidence.
- Observation comparison is exact and pure. It cannot write files, invoke a
  workflow, execute the command label, or silently normalize a mismatch green.
- Catalog/report output distinguishes declared, bound, green, blocked, and
  unavailable. Only bound green observations count toward acceptance.
- The contract catalog contains exactly the immutable 31 accepted IDs with
  accepted-snapshot provenance and no runtime Git dependency.
- The family skeleton covers every immutable matrix family and the live
  planning/currentness/cutover groups without requiring legacy topology.
- Unknown contract IDs, duplicate scenario IDs, uncovered required families,
  unsafe fixture paths, and target assertions naming forbidden topology fail.
- Focused tests, validate/report CLI, ruff, basedpyright, diff check,
  independent review, and delta-only test-quality review are green.

Validation:

- Run the Slice 1 implementation-created commands.
- Re-run the existing 25-test planning schema module to protect closed-world
  schema conventions.

Commit message: `feat: add command owner scenario harness contract`.

Worker brief:

- Follow the shared worker brief. Build the smallest complete harness owner and
  honest unbound catalog; stop before workflow adapters.

Reviewer brief:

- Follow the shared reviewer brief. Confirm the interface is deterministic,
  non-executing, project-neutral at the harness layer, exact over 31 contract
  IDs, and incapable of false green unavailable bindings.

Stop conditions:

- Stop if the harness needs to import a command-owner skill, legacy runner
  phase, installed path, or stable-only helper to validate a record.
- Stop if exact accepted contract identity cannot be represented without
  changing the immutable source.

## Slice 2: Bind Workflow And Planning-Quality Scenarios

Risk: `evidence-only`.

Test quality review: `delta-only`.

Scope:

- Add fixture adapters and scenarios for intake, planning, execution,
  validation, review, commit, recovery, resume, closeout, reconciliation, and
  no successor.
- Consume CCFG-21 public stores/transactions for planning artifact lineage,
  idempotence, partial planning recovery, and queue guards.
- Add every live planning-quality scenario, including semantic slice reasons,
  minimum viable scope, explicit narrowly scoped approval for residual material
  complexity, direct independent invocation of registered `batch_planner` and
  `batch_plan_reviewer` roles, and non-executable stale or undecided drafts.
- Add focused behavior tests and update catalog binding/coverage evidence.

Allowed files:

- `tests/fixtures/command-owner-scenarios/`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`, only for the execution
  amendment below.

Execution amendment after the first focused validation:

- Slice 1 correctly proved that an entirely unbound intermediate catalog was
  honest, but its focused test encoded `0` green scenarios and all `17`
  families unavailable as a permanent live-catalog invariant.
- Slice 2 necessarily binds that same catalog, so its required-green catalog
  module cannot retain the transitional count assertion.
- This amendment authorizes only replacing that assertion with
  progression-aware checks: all required contracts remain declared, only bound
  green observations count, unavailable families remain honestly unavailable,
  and the report cannot infer green from declarations.
- The worker must not change the schema, harness owner, accepted 31-contract
  identity, unavailable-status semantics, or any other Slice 1 test contract.

Read-only behavior sources:

- `scripts/planning_contract.py`
- `tests/fixtures/planning-contracts/`
- legacy runner test support only for source-characterization mechanics that do
  not leak into shared assertions

Non-goals:

- No harness/schema redefinition, Planning State currentness or lease mechanics,
  installer/cutover fixture, production command-owner edit, or live queue write.
- No assertion of old skill routes, phase/mode names, prompt text, or dependency
  topology.

Acceptance criteria:

- Each workflow family drives a fixture-owned adapter and produces observable
  transition, file-effect, stop, and validation evidence.
- Fresh/multi-item/duplicate/stale intake is atomic and idempotent, and intake
  stops before planning.
- Planning selects at most one eligible ledger item, honors existing
  selected/queued/active state, blocks missing/vague/destructive/unapproved
  work, creates at most one runway, and stops before implementation.
- A cohesive one-slice plan is accepted. Every multi-slice plan has a semantic
  boundary; filler splits and unjustified expansion block before queue mutation.
- Residual material complexity cannot proceed without explicit, narrowly scoped
  user approval recorded as an observable decision.
- The default command owner directly invokes the registered `batch_planner` and
  a separate registered `batch_plan_reviewer`. The planner cannot invoke the
  reviewer, frame its evidence, approve its result, or satisfy both roles.
- Stale drafts and unresolved user decisions remain non-executable.
- Execution/review/commit/recovery/resume and same-batch closeout/no-successor
  observations match the accepted contracts without claiming ownership transfer.
- Partial selection and closeout faults retry idempotently without duplicate
  artifacts or lost batch identity.
- Focused tests, catalog validation/report, ruff, diff check, independent
  review, and delta-only test-quality review are green.

Validation:

- Run the Slice 2 implementation-created commands.
- Re-run planning-contract schema/store/artifact/transaction tests.

Commit message: `test: bind command workflow behavior scenarios`.

Worker brief:

- Follow the shared worker brief. Bind only fixture workflow behavior to the
  Slice 1 contract; keep currentness and cutover families unavailable.

Reviewer brief:

- Follow the shared reviewer brief. Confirm every green is an observed behavior,
  planning quality reflects semantic rather than numeric slicing, and no
  CCFG-24/25/26 production ownership is implied.

Stop conditions:

- Stop if a scenario requires editing a command owner, queue owner, planning
  schema/store, or legacy runtime to become green.
- Stop if a shared expectation depends on APR/Batch Runway topology.

## Slice 3: Prove Currentness, Protected Handoffs, And Faults

Risk: `evidence-only`.

Test quality review: `delta-only`.

Scope:

- Add fixture scenarios using temporary Layout v1 roots and isolated Git
  repositories for Planning State currentness, Git material integrity, strict
  identity/write scope, fresh handoffs, receipts, and exact reviewer bases.
- Add planning/commit/closeout fault and movement cases that belong to those
  seams.
- Update binding/coverage evidence and add focused currentness tests.

Allowed files:

- `tests/fixtures/command-owner-scenarios/`
- `tests/test_command_owner_scenario_currentness.py`

Read-only behavior sources:

- `scripts/planning_state.py`
- `scripts/cross_checkout_context.py`
- `tests/fixtures/planning-contracts/`
- existing Planning State, strict-context, and pre-creation test support

Non-goals:

- No edit to Planning State, strict/pre-creation helpers, agent contracts,
  installed helpers, workflow owners, or canonical planning state.
- No stable-only helper API name or refresh topology in shared scenario records.
- No installer, switch, rollback, deletion, or bridge-absence fixture yet.

Acceptance criteria:

- Planning State `current` and `validate` alone determine selected/queued/active
  semantic currentness. Stale or invalid state blocks before mechanical helper
  invocation.
- Git evidence is limited to exact diff bases, accepted commits, rollback, and
  movement during lease preparation; history, changed paths, fingerprints,
  ancestry, and dirt do not decide lifecycle state.
- Green Planning State plus unchanged implementation baseline permits a fresh
  context when planning/toolchain `HEAD` advanced.
- Unexpected implementation movement and movement during preparation block.
- Every worker/reviewer handoff uses a fresh exact lease, matching result echo,
  validated write scope, durable receipt, and exact reviewer diff basis.
- Wrong-root writes, wrong generation, mixed generation, stale review basis,
  missing commit/receipt, unrelated commit content, and partial reconciliation
  fail closed with deterministic evidence.
- The report proves all execution-currentness carry-forward scenarios and all
  applicable planning/commit/closeout fault scenarios.
- Focused tests, existing currentness/strict-context suites, catalog report,
  ruff, diff check, independent review, and delta-only test-quality review are
  green.

Validation:

- Run the Slice 3 implementation-created commands.
- Re-run the 309-test baseline if focused selectors reveal shared behavior
  movement.

Commit message: `test: prove planning currentness and handoff integrity`.

Worker brief:

- Follow the shared worker brief. Use isolated roots and observable ready/blocked
  outcomes; never port the stable helper call graph into the candidate catalog.

Reviewer brief:

- Follow the shared reviewer brief. Confirm Planning State/Git ownership is
  exact, movement fails closed, and the scenario interface protects leases and
  receipts without legacy topology.

Stop conditions:

- Stop if a scenario can pass only by changing Planning State, strict helper
  behavior, production execution ownership, or a real repository baseline.
- Stop if fixture setup writes outside pytest temporary roots.

## Slice 4: Prove Disposable Cutover And Close The Aggregate Gate

Risk: `evidence-only`.

Test quality review: `delta-only`.

Scope:

- Add fixture-only three-root/generation, candidate write-rejection, branch
  lineage, child-generation, install, partial-install, stale-link, switch,
  rollback, quiescence, physical-absence, and archive-readability scenarios.
- Prove minimum pre-cutover bridge operation and synthetic final bridge absence
  without asserting legacy topology.
- Emit and test the final six-key COR-006 report and migration-program aliases.
- Add a compact candidate `CHANGELOG.md` entry for the non-installed harness.

Allowed files:

- `tests/fixtures/command-owner-scenarios/`
- `tests/test_command_owner_scenario_cutover.py`
- `CHANGELOG.md`
- `schemas/command-owner-scenario-v1.schema.json`
- `scripts/command_owner_scenarios.py`

Same-slice amendment after the clean Slice 4 pre-edit stop:

- The Slice 1 harness report exposes only generic contract/family booleans and
  the closed-world schema has no catalog-owned aggregate evidence map. It
  therefore cannot emit the six exact COR-006 keys, six migration aliases, or
  their concrete scenario/test evidence as Slice 4 requires.
- Add one generic closed-world catalog capability that maps caller-owned
  acceptance keys and aliases to concrete scenario IDs and test evidence.
  `build_report()` must compute each result from the referenced evaluated
  scenarios; it must reject missing, duplicate, unknown, or non-green evidence
  and must not hard-code CCFG, COR, project paths, or key names.
- The schema and harness change is part of Slice 4, not a new slice. Tests for
  the generic capability belong in the Slice 4 focused module. Existing report
  fields and Slice 1-3 behavior remain unchanged.

Read-only behavior sources:

- `scripts/install_codex_config.py`
- `scripts/cross_checkout_context.py`
- `scripts/planning_state.py`
- accepted design and closed CCFG-19/21/22 evidence

Non-goals:

- No edit to prior test modules. Harness/schema edits are limited to the
  generic aggregate-evidence capability authorized by the same-slice amendment
  above; any wider change requires another stop and normal fix/re-review loop.
- No real install, candidate-home/stable-home mutation, default switch,
  canonical candidate write, route deletion, bridge removal, or archive move.
- No claim that synthetic absence closes CCFG-28 or CCFG-29.

Acceptance criteria:

- All installer/switch/rollback/deletion effects occur under disposable pytest
  roots with exact before/after evidence and no external write.
- Three explicit roots and one generation are preserved; candidate canonical
  writes, mixed generation, stale links, and partial installs fail closed.
- Fixture switch and rollback demonstrate atomic visible generation semantics;
  pre-cutover quiescence and post-switch stable-controller boundaries remain
  explicit.
- Pre-cutover bridge scenarios prove only the minimum fixture/reference path
  needed while canonical planning remains master-owned.
- Synthetic final fixtures contain no bridge and no target assertion/import
  depends on old APR, Batch Runway, exact prompt prose, stable-only paths,
  helper names, aliases, or dependency topology.
- Historical artifacts remain readable but cannot become pickup authority.
- The final deterministic report emits all six COR-006 keys and all six aliases
  as true, maps each to concrete scenario/test evidence, covers exactly the 31
  immutable contract IDs, and lists no unavailable required family.
- Aggregate evidence is catalog-owned and mechanically derived from evaluated
  scenario results; changing a declared key, alias, scenario reference, or test
  evidence cannot self-certify a green result.
- The changelog states the harness is non-installed and preserves CCFG-24+
  ownership boundaries.
- Focused tests, final catalog validate/report, ruff, basedpyright, diff check,
  independent review, and delta-only test-quality review are green.

Validation:

- Run the Slice 4 implementation-created commands.
- Re-run the 32-test pre-creation suite, focused manifest subset, and read-only
  candidate/stable installer controls.

Commit message: `test: complete command owner cutover scenario evidence`.

Worker brief:

- Follow the shared worker brief. Keep all external-state behavior disposable
  and close only the aggregate harness evidence, not real cutover work.

Reviewer brief:

- Follow the shared reviewer brief. Inspect fixture isolation, topology
  independence, exact six-key evidence, and the distinction between synthetic
  final absence and CCFG-29 deletion.

Stop conditions:

- Stop before any command targets a real Codex home, default binding, canonical
  planning root, candidate branch, or installed legacy route.
- Stop if any acceptance key is inferred from declarations or test names rather
  than observed green evidence.

## Final Validation

After Slice 4 is committed and every active-ledger row is complete, the
coordinator must:

1. Use a fresh strict live execution lease and validate the exact final
   candidate range plus read-only stable planning scope.
2. Run all four focused scenario test modules and both harness CLI commands.
3. Run the 309-test planning/state/strict-context/agent baseline and the
   32-test pre-creation suite.
4. Run the focused manifest ownership subset, ruff on every changed Python
   file, basedpyright on the harness owner, and `git diff --check` over the
   exact candidate range.
5. Re-run candidate and stable installer status/dry-run. Confirm no new
   installed feature, changed default binding, or real Codex-home mutation.
6. Run the full manifest only as `known-red-baseline`. It must reproduce
   exactly the same three unrelated failures and 18 passes; any different
   result is a blocker requiring classification.
7. Read the final JSON report and map concrete evidence to the six COR-006
   keys, six aliases, 31 immutable contracts, all required families, and every
   live carry-forward scenario.
8. Run independent final review over the exact candidate range and compact
   report/fixture-isolation evidence.
9. Run final exact-range `test-quality-review` in `delta-only` mode.
10. Confirm the candidate diff touches only the eight validated paths/file
    areas and contains no production owner, installed feature, legacy-topology
    assertion, real cutover action, or CCFG-24+ implementation.
11. Write `completed-slices.md` and `closeout.md`, reconcile CCFG-23 only, clear
    selected/queued/active state, and stop before successor selection.

No full project pytest suite, package install, generated-doc refresh,
graph/index refresh, real installation, default switch, live deletion, or
candidate canonical planning session is authorized.

## Stop Conditions

- Stop if Planning State no longer reports this same queued runway and selected
  CCFG-23 scope as current.
- Stop if the canonical first-handoff preflight returns `blocked` or any later
  live lease/write-scope validation fails.
- Stop if the candidate worktree contains unrelated changes before a slice or
  a task-scoped diff escapes its allowlist.
- Stop if implementation changes an existing command owner, planning/state
  contract owner, strict helper, installer, manifest, installed generation, or
  accepted design source.
- Stop if a target scenario can become green only through CCFG-24/25/26
  production ownership, CCFG-27/28 real cutover, or CCFG-29 bridge removal.
- Stop if unbound future interfaces are counted green, scenario labels are
  executed, or a fixture adapter encodes its expected result without observable
  state/file evidence.
- Stop if any target assertion depends on APR/Batch Runway topology, exact
  prompt prose, stable-only paths, historical helper names, aliases, or
  dependency presence.
- Stop if disposable scenarios escape pytest temporary roots or mutate either
  real Codex home, the default binding, canonical planning root, candidate
  branch, or live legacy routes.
- Stop if the known-red manifest baseline changes, focused validation fails,
  review/test-quality findings remain unresolved, repository movement is
  unexpected, required subagent support is unavailable, or scope drifts.
- Stop closeout before selecting, refreshing, dispatching, creating, or
  preparing CCFG-24 or any other successor.
