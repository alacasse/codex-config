# CCFG-21 Planning Artifact Contracts Runway

## Purpose

Implement the accepted planning artifact schemas, revisioned stores, lineage
validators, and DEC-038 selection-transaction prototype as one deep repo-local
module in the candidate checkout. This runway covers CCFG-21 only. It proves the
target contracts against explicit fixtures without migrating live planning
documents or integrating any workflow command owner.

Closeout may mark CCFG-21 `Closed` only when all six COR-004 acceptance keys and
the more detailed migration-program exit gate are green. Otherwise preserve the
exact blocker and stop without selecting a successor.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slices 1 through 4 risk: `migration`.
- Authorized migration: add the target closed-world schemas, one planning
  contract module, fixture-only compatibility readers, deterministic stores,
  transaction prototype, tests, fixtures, and changelog entry.
- Live planning-artifact migration: forbidden.
- Workflow ownership transfer or integration: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such slice
  is authorized.
- Candidate-checkout filesystem approval may be required at execution time.
  That approval authorizes access only and does not widen scope.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Planning-state `current` and `validate` pass with no blockers and only the two
  known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable checkout: `/home/alacasse/projects/codex-config`, branch `master`,
  exact `HEAD` `b2a04a32d5871c96ebb5e93ccf4056a32f2db07b`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, exact `HEAD`
  `3e54155964e92d3a4dced8268cc683baaab9be1c`, aligned with its upstream.
- Both worktrees were clean before planning. Planning performs no candidate
  write.
- The installed strict-context helper resolves to the stable checkout. Installer
  status reports linked feature-version drift but correct stable ownership;
  dry-run performs no write. This batch does not install or refresh features.
- CCFG-19 and CCFG-20 are closed. DEC-036 accepts closed-world reader-first v1
  evolution and producer identity. DEC-037 accepts apply-only whole-ledger CAS.
  DEC-038 resolves OPEN-003 with an append-only four-stage selection saga.
- The accepted target is one operational YAML block near the beginning of each
  active artifact, one canonical block per ledger finding, a mechanically
  validated derived index, and prose that cannot redefine machine facts.
- Per-finding ledger blocks remain the accepted default. A global-block change
  requires blocking prototype evidence and a separate accepted decision.
- Candidate PyYAML and jsonschema dependencies already exist from CCFG-20;
  `.venv` contains the locked test, lint, and type tools.
- The candidate contains `scripts/planning_state.py`, JSON state fixtures, and
  transition characterization, but no target planning schema, planning contract
  store, target transaction record, or target fixture catalog.
- Existing `planning_state.py` adjacent-temp writes lack the complete target
  expected-revision/hash, reread-validation, and receipt-recovery guarantees.
  That behavior is evidence, not the target implementation seam.
- Current required-green baselines are 42 skill-contract tests, 8 focused
  Planning State transition tests, 33 broader Planning State contract tests,
  33 cross-checkout/custom-agent tests with 187 subtests, and 3 manifest schema
  tests with 31 subtests.
- The full manifest is a known-red diagnostic: 3 failed and 18 passed in the
  same unrelated exact-wording assertions closed CCFG-20 recorded.
- `basedpyright scripts/planning_state.py` is a known-red diagnostic with 225
  current errors. CCFG-21 must not absorb that broad cleanup.

The queued stable planning artifacts are expected dirty coordination state. Do
not copy them into the candidate checkout. The persisted context below is a
planning snapshot, not a live execution lease. If either repository `HEAD`
moves, `work-batch` must preserve the snapshot and use the canonical
ready/blocked preflight or refresh procedure before delegation.

## Batch Non-Goals

- Do not migrate stable or candidate `CURRENT.md`, `LEDGER.md`, dispatch,
  runway, closeout, archived, or historical documents.
- Do not change `scripts/planning_state.py` or integrate the target module into
  current commands.
- Do not implement or modify `add-to-ledger`, `plan-batch`, `work-batch`, APR,
  Batch Runway, or the local architecture-program runner.
- Do not implement CCFG-22 authoring guidance, CCFG-23 scenario harnesses, or
  CCFG-24 through CCFG-29 ownership transfer, cutover, or convergence.
- Do not register an installed feature, edit `codex-features.json`, install the
  candidate, or switch the default generation.
- Do not make a global ledger block canonical, add a legacy-format writer,
  infer machine facts from prose, make SQLite canonical, rewrite archives, or
  preserve permanent compatibility.
- Do not introduce a second parser, validator, store, transaction owner module,
  or structural field table parallel to the canonical JSON Schemas.

## Acceptance Key Map

COR-004 closes only with these exact keys:

```yaml
current_schema_and_atomicity_green: true
finding_schema_and_multi_item_atomicity_green: true
per_finding_default_confirmed_or_superseded: true
dispatch_runway_closeout_schemas_green: true
lineage_generation_validation_green: true
fault_injection_green: true
```

The implementation evidence must also satisfy the migration-program detail:

```yaml
current_schema_green: true
finding_schema_green: true
dispatch_schema_green: true
runway_schema_green: true
closeout_schema_green: true
current_atomicity_and_rollback_green: true
ledger_multi_item_atomicity_green: true
per_finding_default_confirmed_or_superseded_by_decision: true
lineage_and_generation_validation_green: true
```

The closeout must map test, CLI, fault-injection, and review evidence to every
key rather than treating aggregate test success as acceptance.

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
  toolchain_commit: b2a04a32d5871c96ebb5e93ccf4056a32f2db07b
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: b2a04a32d5871c96ebb5e93ccf4056a32f2db07b
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 3e54155964e92d3a4dced8268cc683baaab9be1c
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Planning loaded the installed stable helper, verified that it resolves under
the declared toolchain root, parsed the complete payload, and called
`validate_write_scope` with these four canonical planning paths:

- `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/dispatch.md`
- `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/runway.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`

It also validated these thirteen intended candidate paths or file areas:

- `schemas/planning-current-v1.schema.json`
- `schemas/planning-finding-v1.schema.json`
- `schemas/planning-dispatch-v1.schema.json`
- `schemas/planning-runway-v1.schema.json`
- `schemas/planning-closeout-v1.schema.json`
- `schemas/planning-selection-transaction-v1.schema.json`
- `scripts/planning_contract.py`
- `tests/test_planning_contract_schema.py`
- `tests/test_planning_contract_store.py`
- `tests/test_planning_contract_artifacts.py`
- `tests/test_planning_transaction.py`
- `tests/fixtures/planning-contracts/`
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

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-21-planning-artifact-contracts/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway`.
- Integration harness: repo-local `scripts/planning_contract.py` CLI over
  explicit valid, invalid, representation-comparison, and transaction fixtures.
- Harness output: stdout/stderr and CLI-owned temporary directories only; no
  durable generated output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus a
  separate stable planning-ledger receipt after each candidate hash exists.
- Dirty-file constraints: candidate starts clean and may change only active
  slice files; stable changes are limited to this batch's planning artifacts
  and same-batch reconciliation.
- Test quality review: `delta-only` for every slice.

## Module Interface And Slice Handoff

The seam is `scripts/planning_contract.py`. It owns operational-block
extraction, duplicate-key-safe YAML loading, JSON Schema application,
deterministic rendering and diagnostics, explicit compatibility reading,
compare-and-swap persistence, receipt construction/recovery, artifact lineage,
transaction-record validation, fault injection, and a thin CLI adapter.

Expose one `validate_planning_contracts(...)` catalog interface plus narrow
public operations for:

- reading and applying one canonical current-state document;
- reading and applying `ledger-store/v1` caller decisions to a whole ledger;
- writing one revisioned dispatch, runway, or closeout artifact; and
- resuming one DEC-038 selection transaction from its append-only record.

The store operations accept explicit paths, expected logical revisions,
expected full-file hashes, producer identity, caller decisions, and idempotency
keys. They return immutable parsed results, before/after revisions, touched
finding IDs where relevant, deterministic diagnostics, and receipts. They do
not choose semantic actions, paths, batches, scope, closeout meaning, or
successors.

Slice 1 establishes the canonical schemas, parser, renderer, validator, and
read-only compatibility boundary. Slices 2 through 4 must extend and consume
that same module and schema registry. They may not add parallel current, ledger,
artifact, transaction, parser, schema, receipt, or CLI owners.

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
- The target schemas, module, and fixtures remain repo-local in CCFG-21.
  Candidate installation and manifest registration are forbidden even if all
  tests are green.
- Workers use the existing locked candidate `.venv`. They may not install
  ambient packages, update the dependency lock, or run installer commands.
- Every test-changing slice receives `test-quality-review` in `delta-only`
  mode. Actionable findings enter the normal reviewer fix/block loop; clean
  output is recorded compactly.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

### Current Required-Green Baseline

Run from the candidate checkout:

- Planning State target-characterization subset:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state.py -k 'state_fixture_schema or receipt_fixture_schema or register_artifact or select_batch or queue_batch or bootstrap_state'
  ```

  Result: 33 passed and 145 deselected.

- Existing skill-contract suite:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py
  ```

  Result: 42 passed.

- Cross-checkout and registered-agent contracts:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py
  ```

  Result: 33 passed and 187 subtests passed.

- Manifest schema subset:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'manifest_feature_requirements_are_valid or manifest_catalog_distinguishes_user_and_agent_facing_skills or custom_agent_toml_files_are_valid'
  ```

  Result: 3 passed, 18 deselected, and 31 subtests passed.

### Implementation-Created Commands

Slice 1 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_schema.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/schema/valid
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/schema/invalid-unknown-field; status=$?; test "$status" -eq 1'
```

Slice 2 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_store.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_store.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py compare-ledger-layouts --toolchain-root . --per-finding tests/fixtures/planning-contracts/ledger/per-finding-valid --global tests/fixtures/planning-contracts/ledger/global-equivalent
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/ledger/invalid-derived-index; status=$?; test "$status" -eq 1'
```

Slice 3 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_artifacts.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_artifacts.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/artifacts/valid-lineage
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/artifacts/invalid-lineage; status=$?; test "$status" -eq 1'
```

Slice 4 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_transaction.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_transaction.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/complete
.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/recover-after-selected-cas
sh -c '.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/invalid-reused-id; status=$?; test "$status" -eq 1'
```

After each creating slice, its commands become required-green for later slices.
Every slice also runs `git diff --check` from the candidate checkout.

### Known-Red And Diagnostic-Only Commands

- Full manifest:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
  ```

  Baseline: 3 failed and 18 passed in unrelated exact-wording assertions:
  `test_executable_work_source_boundary_is_explicit`,
  `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
  `test_work_batch_reconciles_same_batch_closeout`. It is diagnostic-only and
  cannot block or expand CCFG-21.

- Existing Planning State type check:

  ```sh
  .venv/bin/basedpyright scripts/planning_state.py
  ```

  Baseline: 225 errors. It is diagnostic-only. CCFG-21 does not modify that
  module or absorb its typing cleanup.

### Conditional Commands

- `./install.sh --status` and `./install.sh --dry-run` run only if an unexpected
  diff touches installed-feature metadata. Such a diff is a scope violation and
  stops the batch; no candidate installation follows.
- No worker may run a full project suite, installer mutation, generated-doc
  refresh, graph/index refresh, or final validation.

## Shared Worker And Reviewer Briefs

Worker brief for every slice:

- You are the already-required `runway_worker`. Implement only the active slice
  from this runway; do not spawn, delegate to, or wait on another agent.
- Independently validate the fresh strict cross-checkout live lease before
  acting, then write only inside the candidate checkout and only to the active
  slice's allowed files.
- Keep stable planning files, accepted history, `scripts/planning_state.py`, and
  unrelated candidate files read-only.
- Extend the single `scripts/planning_contract.py` owner. Do not add a parallel
  parser, renderer, store, receipt, artifact, saga, or CLI module.
- Reuse the locked PyYAML/jsonschema environment. Do not add packages or update
  `pyproject.toml` or `uv.lock`.
- Do not migrate live artifacts, integrate command owners, register installed
  features, edit the manifest, or implement later findings.
- Run only the focused validation assigned to the slice and return the
  registered v2 worker result with matching
  `verified_cross_checkout_context`.

Reviewer brief for every slice:

- The coordinator supplies the exact candidate commit hash or task-scoped
  candidate worktree diff basis. Echo it as `diff_basis` in the registered v2
  reviewer result.
- Independently validate a fresh strict cross-checkout live lease before review.
- Verify accepted-schema fidelity, closed-world failure, duplicate-key safety,
  deterministic rendering and diagnostics, compare-and-swap correctness,
  receipt recovery, lineage, and absence of prose inference or legacy writes.
- Review tests through public module operations and CLI-visible behavior, not
  private helper topology.
- Run `test-quality-review` in `delta-only` mode and include its compact YAML
  output.
- Reject duplicated structural owners, a second planning module, semantic
  decisions in `ledger-store/v1`, hidden current-state migration, or installed
  surface drift.
- Return matching `verified_cross_checkout_context` and a clear
  accept/fix/block verdict.

## Active Ledger

| Slice | Risk | Status | Candidate commit | Stable receipt | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|---|
| 2. Current and ledger stores | migration | pending | | | | | CAS, receipts, derived index, and per-finding default | |
| 3. Artifact lineage writes | migration | pending | | | | | Dispatch/runway/closeout persistence and lineage | |
| 4. Selection saga and fault matrix | migration | pending | | | | | DEC-038 exact replay and recovery | |

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Slice Shape

- `1 -> 2`: Slice 1 creates a green closed-world schema/parser/renderer API;
  Slice 2 consumes it to add stateful current and ledger persistence. The
  intermediate read-only validator is independently useful and testable.
- `2 -> 3`: Slice 2 creates green compare-and-swap, atomic replacement, reread,
  idempotency, and receipt primitives; Slice 3 applies the same primitives to
  batch artifact lineage. The intermediate current/ledger store is valid and
  does not depend on dispatch/runway/closeout writes.
- `3 -> 4`: Slice 3 creates green revisioned dispatch and runway operations;
  Slice 4 composes those exact operations with state CAS into DEC-038's saga.
  The intermediate artifact layer is independently reviewable and the saga's
  larger fault surface receives its own commit and rollback boundary.

Four slices are required by semantic producer/consumer and fault-risk
boundaries, not by a target count.

## Slice 1: Establish Closed-World Schemas And Read-Only Validation

Risk: `migration`.

Scope:

- Add the five accepted planning artifact JSON Schemas.
- Add `scripts/planning_contract.py` with one deep catalog validation interface,
  canonical-block parsing/rendering, deterministic diagnostics, and a thin
  `validate` CLI.
- Add schema tests and valid/invalid fixture catalogs, including explicit
  read-only compatibility fixtures for current active old-format Markdown.

Allowed files:

- `schemas/planning-current-v1.schema.json`
- `schemas/planning-finding-v1.schema.json`
- `schemas/planning-dispatch-v1.schema.json`
- `schemas/planning-runway-v1.schema.json`
- `schemas/planning-closeout-v1.schema.json`
- `scripts/planning_contract.py`
- `tests/test_planning_contract_schema.py`
- `tests/fixtures/planning-contracts/schema/**`
- `tests/fixtures/planning-contracts/compatibility/**`

Non-goals:

- No write operations, atomic store, receipts, transaction record, or saga.
- No live artifact migration or current command integration.

Acceptance criteria:

- New-format artifacts contain exactly one supported operational YAML block in
  the accepted location; zero, multiple, duplicate-key, unknown-version, and
  unknown-field cases fail with deterministic path-qualified diagnostics.
- Each schema is closed-world Draft-07 and owns structural fields. Procedural
  code does not duplicate required/allowed field tables.
- `producer.toolchain_generation`, `producer.toolchain_commit`, and
  `producer.schema_version` are required and validated against explicit caller
  expectations when provided. Cwd is never identity evidence.
- `planning-current/v1` owns ledger, selected-dispatch, queued-runway,
  active-runway, latest-closeout, blocker, program, and logical revision facts.
  Prose may explain but cannot duplicate or override them.
- `planning-finding/v1` owns identity, revision, provenance, lifecycle,
  dependencies, scope, evidence pointers, and next action.
- Dispatch, runway, and closeout schemas enforce their accepted batch, source,
  execution, reconciliation, and producer shapes without yet writing files.
- Derived data declares its source artifact and source revision. A second
  machine-fact owner or derived-index contradiction fails.
- The compatibility reader activates only through an explicit caller mode when
  the target block is absent. It is read-only, caller-scoped, does not scan
  archives, does not infer arbitrary prose semantics, and cannot render or write
  old format.
- CLI validation exits `0` for the valid catalog and `1` for deterministic
  contract findings; usage errors remain distinct. The expected-failure command
  asserts exit `1` and itself returns `0`.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_schema.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/schema/valid
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/schema/invalid-unknown-field; status=$?; test "$status" -eq 1'
git diff --check
```

Test quality review: `delta-only`.

Commit message: `feat: add planning artifact schema validator`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
compare every schema with the accepted format and DEC-036 and prove that the
compatibility boundary cannot write.

Stop conditions:

- Stop if schema behavior requires a hand-written YAML parser, duplicated field
  tables, or a second planning module.
- Stop if old-format compatibility requires a writer, archive scan, or prose
  interpretation.
- Stop if implementation touches live artifacts, `planning_state.py`, current
  skills, or installed feature metadata.

## Slice 2: Add Revisioned Current And Ledger Stores

Risk: `migration`.

Scope:

- Extend the Slice 1 module with expected revision and full-file-hash checks,
  deterministic rendering, adjacent atomic replacement, reread validation,
  idempotency, and recoverable before/after receipts for current documents and
  ledgers.
- Implement DEC-037's apply-only `ledger-store/v1` boundary.
- Validate derived indexes and compare per-finding blocks with one global block
  through explicit fixture catalogs.
- Add store tests and current/ledger fault-injection fixtures.

Allowed files:

- `scripts/planning_contract.py`
- `tests/test_planning_contract_store.py`
- `tests/fixtures/planning-contracts/current/**`
- `tests/fixtures/planning-contracts/ledger/**`

Non-goals:

- No dispatch, runway, or closeout writes.
- No selection saga.
- No semantic duplicate, merge, selection, scope, closeout, or successor
  decisions inside the store.

Acceptance criteria:

- Current and ledger writes require both the caller's expected logical revision
  and expected full-file hash. Any mismatch rejects before writing.
- The module parses and applies in memory, renders deterministically, writes an
  adjacent temporary file, atomically replaces, rereads, revalidates, and emits
  immutable before/after receipts.
- Failure before replacement preserves the original file. Failure after
  replacement but before receipt emission is recoverable through exact
  idempotency evidence without reapplying the mutation.
- Exact idempotency-key and payload replay returns the same result. Reusing the
  key with a different payload or ambiguous evidence blocks.
- `ledger-store/v1` reads the whole ledger and applies one explicit caller
  decision with whole-file CAS and touched-finding revision checks. It does not
  choose action or meaning.
- Multi-finding changes are all-or-nothing and one receipt names every touched
  finding.
- The derived index equals the structured finding blocks and has no semantic
  authority.
- The comparison proves equal semantic/projection output for per-finding and
  global fixtures while measuring duplicate detection, diff locality, error
  locality, and revision behavior. Per-finding remains the default. Any
  blocking counterevidence stops rather than silently changing the default.
- CLI comparison exits `0` only for equivalent fixtures. Invalid derived-index
  validation exits `1`, and the expected-failure wrapper returns `0`.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py tests/test_planning_contract_store.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_schema.py tests/test_planning_contract_store.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py compare-ledger-layouts --toolchain-root . --per-finding tests/fixtures/planning-contracts/ledger/per-finding-valid --global tests/fixtures/planning-contracts/ledger/global-equivalent
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/ledger/invalid-derived-index; status=$?; test "$status" -eq 1'
git diff --check
```

Test quality review: `delta-only`.

Commit message: `feat: add revisioned planning stores`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
trace the DEC-037 input/output/CAS/idempotency contract and inspect fault tests
for observable pre/post file and receipt behavior.

Stop conditions:

- Stop if the store chooses semantic caller decisions or mutates more than the
  declared current/ledger file.
- Stop if receipt recovery can reapply a mutation or if ambiguous partial
  evidence is treated as success.
- Stop if the per-finding comparison produces blocking evidence. Record the
  blocker; do not adopt a global default in this batch.

## Slice 3: Add Revisioned Artifact Lineage Writes

Risk: `migration`.

Scope:

- Extend the shared store primitives to write dispatch, runway, and closeout
  artifacts.
- Enforce exact source revisions, immutable lineage, producer generation
  identity, canonical path containment, and same-batch closeout fields.
- Add artifact persistence tests and valid/invalid lineage fixtures.

Allowed files:

- `scripts/planning_contract.py`
- `tests/test_planning_contract_artifacts.py`
- `tests/fixtures/planning-contracts/artifacts/**`

Non-goals:

- No planning-state transition CAS or four-stage saga.
- No live dispatch/runway/closeout migration or command integration.

Acceptance criteria:

- Dispatch writes bind program, finding IDs, ledger path/revision, selection
  scope, batch kind/risk, approval gates, dependencies, expected runway path,
  explicit execution roots, stop conditions, and producer identity.
- Runway writes require the exact validated dispatch revision and bind batch,
  queued state, result contract, branch/dirty-worktree policy, implementation
  root, slice contracts, final review gate, same-batch closeout, and producer.
- Closeout writes bind the same batch and lineage, implementation commits,
  validation/review evidence, finding mutations, cleared post-closeout pointers,
  `successor_selected: false`, execution roots, and producer identity.
- A foreign program, finding, batch, root, generation, path, source revision, or
  predecessor hash rejects before writing.
- Artifact writes reuse Slice 2's expected revision/hash, adjacent replace,
  reread, idempotency, and receipt-recovery behavior.
- Lineage is immutable after acceptance; retry with an exact payload returns the
  same result and any lineage mismatch blocks.
- CLI validation exits `0` for the complete valid lineage and `1` for invalid
  lineage; the expected-failure wrapper itself returns `0`.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_planning_contract_artifacts.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_planning_contract_artifacts.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/artifacts/valid-lineage
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/artifacts/invalid-lineage; status=$?; test "$status" -eq 1'
git diff --check
```

Test quality review: `delta-only`.

Commit message: `feat: add planning artifact lineage store`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
trace dispatch-to-runway-to-closeout lineage and verify that stable/candidate
generation and path mismatches fail before persistence.

Stop conditions:

- Stop if artifact validation requires state transition ownership or command
  semantics from CCFG-24 through CCFG-26.
- Stop if artifact writes bypass the Slice 2 store or create a second receipt
  implementation.
- Stop if any fixture path escapes its explicit temporary planning root.

## Slice 4: Implement The DEC-038 Selection Saga And Fault Matrix

Risk: `migration`.

Scope:

- Add the closed-world planning selection transaction-record schema.
- Extend the shared module with the append-only DEC-038 transaction record and
  resumable four-stage saga over Slice 2 state CAS and Slice 3 artifact writes.
- Add every accepted fault checkpoint, exact replay/recovery scenario, invalid
  mismatch scenario, and CLI simulation fixture.
- Add the CCFG-21 changelog entry.

Allowed files:

- `schemas/planning-selection-transaction-v1.schema.json`
- `scripts/planning_contract.py`
- `tests/test_planning_transaction.py`
- `tests/fixtures/planning-contracts/transactions/**`
- `CHANGELOG.md`

Non-goals:

- No `plan-batch` integration, ownership transfer, or real canonical planning
  mutation.
- No deletion or rollback hiding of durable transaction evidence.

Acceptance criteria:

- Before Stage 1, the append-only record binds one transaction/idempotency ID,
  program/finding/batch identity, exact initial ledger and state revision, idle
  expectation, dispatch path/payload/hash, intended runway path, command/schema
  versions, and the exact four-stage plan. It does not claim future values.
- Stage 1 writes and validates dispatch, then appends the observed revision and
  validation result.
- Stage 2 first appends exact idle-to-selected CAS input, applies the transition,
  persists/reconstructs its receipt, and appends observed state/receipt revisions
  and validation.
- Stage 3 first appends the exact runway payload/hash and dispatch/selected-state
  lineage, writes and validates the runway, then appends the observed revision
  and validation.
- Stage 4 first appends exact selected-to-queued CAS input, applies the
  transition, persists/reconstructs its receipt, and appends observed
  state/receipt revisions and validation.
- Prior transaction fields are immutable. Each extension is legal only from the
  exact next state with every prior artifact, receipt, revision, payload, and
  lineage binding matched.
- Exact retry resumes at the first incomplete stage and never duplicates an
  artifact write or CAS effect. Reused IDs with different payload/state/lineage,
  ambiguous partial evidence, and unexplained movement block.
- Fault injection covers before/after dispatch write, dispatch validation,
  selected CAS, selected receipt, runway input persistence, runway write,
  runway validation, queued CAS, queued receipt, and transaction-record append.
- Durable partial evidence remains visible. Recovery may append a blocker or
  reconstructed receipt but cannot delete transaction, artifact, transition, or
  receipt evidence.
- The complete and recover-after-selected-CAS CLI fixtures exit `0`. The reused
  ID mismatch fixture exits `1`, and the expected-failure wrapper returns `0`.
- All COR-004 keys are green: current schema/atomicity, finding schema/multi-item
  atomicity, per-finding default, dispatch/runway/closeout schemas,
  lineage/generation validation, and fault injection.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_planning_contract_artifacts.py tests/test_planning_transaction.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_planning_contract_artifacts.py tests/test_planning_transaction.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/complete
.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/recover-after-selected-cas
sh -c '.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/invalid-reused-id; status=$?; test "$status" -eq 1'
git diff --check
```

Test quality review: `delta-only`.

Commit message: `feat: add planning selection transaction prototype`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
map every DEC-038 checkpoint to observable before/after artifact, state,
transaction-record, and receipt assertions and reject mock-only proof.

Stop conditions:

- Stop if saga implementation requires command-owner selection, scope, proceed,
  closeout, or successor decisions.
- Stop if a retry can reapply a completed effect or if recovery hides/deletes
  partial evidence.
- Stop if all fault checkpoints cannot be made deterministic in fixture-owned
  temporary roots.
- Stop if any integration touches real stable or candidate planning artifacts.

## Final Validation

Run from the candidate checkout after all four candidate commits and before
same-batch closeout:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_planning_contract_artifacts.py tests/test_planning_transaction.py tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py
.venv/bin/ruff check --no-cache scripts/planning_contract.py tests/test_planning_contract_schema.py tests/test_planning_contract_store.py tests/test_planning_contract_artifacts.py tests/test_planning_transaction.py
.venv/bin/basedpyright scripts/planning_contract.py
.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/schema/valid
.venv/bin/python scripts/planning_contract.py compare-ledger-layouts --toolchain-root . --per-finding tests/fixtures/planning-contracts/ledger/per-finding-valid --global tests/fixtures/planning-contracts/ledger/global-equivalent
.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/artifacts/valid-lineage
.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/complete
.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/recover-after-selected-cas
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/schema/invalid-unknown-field; status=$?; test "$status" -eq 1'
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/ledger/invalid-derived-index; status=$?; test "$status" -eq 1'
sh -c '.venv/bin/python scripts/planning_contract.py validate --toolchain-root . tests/fixtures/planning-contracts/artifacts/invalid-lineage; status=$?; test "$status" -eq 1'
sh -c '.venv/bin/python scripts/planning_contract.py simulate-selection --toolchain-root . tests/fixtures/planning-contracts/transactions/invalid-reused-id; status=$?; test "$status" -eq 1'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'manifest_feature_requirements_are_valid or manifest_catalog_distinguishes_user_and_agent_facing_skills or custom_agent_toml_files_are_valid'
git diff --check 3e54155964e92d3a4dced8268cc683baaab9be1c..HEAD
```

Then:

- inspect the exact candidate range from
  `3e54155964e92d3a4dced8268cc683baaab9be1c..HEAD`;
- confirm the diff contains only the thirteen validated candidate paths or file
  areas;
- obtain an independent final `runway_reviewer` review over that exact range;
- run `test-quality-review` in `delta-only` mode over the complete changed-test
  set and resolve actionable findings through the normal fix/review loop;
- record the exact known-red manifest diagnostic without treating it as a gate;
- update `completed-slices.md`, write `closeout.md`, and reconcile CCFG-21 only;
  and
- stop before successor selection.

## Stop Conditions

- Stop if Planning State no longer identifies this same queued runway and
  selected CCFG-21 scope as current.
- Stop on any blocked strict-context preflight, root/repository/generation
  mismatch, unexplained repository movement, or live-lease write-scope failure.
- Stop if the candidate worktree is not clean before Slice 1 or contains changes
  outside the active allowlist before any later slice.
- Stop if the five accepted schemas or the selection-transaction record acquire
  unknown-field tolerance, prose fallback, or incompatible producer identity.
- Stop if implementation changes `planning_state.py`, command-owner skills,
  current planning documents, the manifest, installed state, or later finding
  surfaces.
- Stop if `ledger-store/v1` or the saga owns a semantic workflow decision.
- Stop if the per-finding default cannot be confirmed without a new decision.
- Stop if receipt recovery is ambiguous, can duplicate an effect, or can hide
  durable partial evidence.
- Stop on unresolved validation failure, actionable review findings, or dirty
  file conflict.
- Stop same-batch closeout before selecting, refreshing, dispatching, creating,
  or preparing CCFG-22 or any other successor.
