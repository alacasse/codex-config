# CCFG-24A Intake Owner Preparation Runway

## Purpose

Implement and candidate-install the bounded `add-to-ledger/v1` owner defined by
the accepted decision amendment, bind the relevant intake scenarios to that
installed owner, and collect compact evidence for a later cutover reassessment.

The failed decision attempt remains historical evidence in `execution-report.md`
and commits `33f7adf`, `c087024`, and `199f4a9`. It must not be resumed.

## Source And Authority

- Finding: CCFG-24, still `Pending`.
- Dispatch: `dispatch.md`.
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Preparation/cutover boundary:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`.
- Accepted implementation decisions:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`.

The decision amendment controls command semantics. DEC-037 controls mechanical
apply replay. `ledger-store/v1` remains unchanged.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slice 1, Implement and candidate-install the bounded owner: `migration`.
- Slice 2, Bind scenarios and measure preparation evidence: `migration`.
- No decision-only, contract-narrowing, or destructive-cleanup slice is
  authorized.

`slice_shape`: two slices.

- `1 -> 2`: Slice 1 produces a directly tested and candidate-installed owner
  over temporary ledgers. Slice 2 consumes that exact installed owner in the
  behavioral harness and produces a separately reviewable integration/evidence
  commit.

The intermediate state is valid: old intake routes remain available, the stable
home is untouched, and the candidate owner has no canonical mutation authority.

## Current Baseline And Assumptions

- Stable toolchain and canonical planning checkout:
  `/home/alacasse/projects/codex-config`, branch `master`.
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`.
- Candidate implementation baseline:
  `b38570bcd97b2584f3828abcd395b0f45ed91e58`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
- `scripts/planning_contract.py` supplies the accepted apply-only store and is
  read-only for this batch.
- CCFG-33 supplies exact-commit scenario acceptance with one evidence-pytest
  process.

Execution must refresh all live revisions and exact scopes. The planning
snapshot below is historical selection evidence, not a live execution lease.

## Batch Non-Goals

- No public digest, idempotency key, request ID, or replay token.
- No adapter beyond `plain_text` and `github_issue`.
- No cross-source merge, secondary-source provenance, fuzzy matching, generic
  ticket framework, or file ingestion.
- No store, planning-schema, or planning-state semantic change.
- No APR, `legacy-removal`, Batch Runway, `plan-batch`, or `work-batch`
  ownership narrowing.
- No fixture/helper deletion or topology cleanup.
- No canonical planning write by candidate code or tests.
- No stable-home install, refresh, unlink, rebind, or default switch.
- No final CCFG-24 cutover, CCFG-24B planning, or CCFG-25 work.

## Allowed Candidate Areas

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `codex-features.json`, limited to `add-to-ledger` and `planning-contracts`
- focused installation metadata for those two features
- `tests/test_add_to_ledger.py`
- intake-only CCFG-23 scenario catalog, workflow-case, adapter, and test surfaces
- focused `plain_text` and `github_issue` fixtures
- `CHANGELOG.md`

## Read-Only Candidate Areas

- `scripts/planning_contract.py`
- `tests/test_planning_contract_store.py`, except execution
- `schemas/planning-*-v1.schema.json`
- `scripts/planning_state.py`
- `scripts/skill_contract.py`
- `skills/architecture-program-runway/**`
- `skills/legacy-removal/**`
- `skills/plan-batch/**`
- `skills/work-batch/**`
- `skills/batch-runway/**`

Any required semantic change in a read-only area stops execution for replan.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious lifecycle behavior.
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
validation, independent review, candidate installation, execution-ledger
updates, commits, and same-batch closeout.

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

Validated plan-time payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 199f4a9cd86edf7e80a13b174b162ce6798c18af
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 199f4a9cd86edf7e80a13b174b162ce6798c18af
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: b38570bcd97b2584f3828abcd395b0f45ed91e58
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Preserve this payload as historical evidence. At startup, `work-batch` must
confirm the current queued scope through Planning State, obtain a fresh `ready`
live-lease preflight, and validate every delegated write scope.

## Context Control

The coordinator reads, in order:

1. current Planning State facts;
2. `dispatch.md` and this runway;
3. the accepted decision amendment;
4. the active slice only;
5. compact prior-slice receipts and reviews.

Do not read the historical report or broad redesign documents unless a named
contradiction requires them. Do not paste worker/reviewer transcripts into the
coordinator context.

- Soft execute budget: 100,000 input tokens.
- Hard warning: 150,000 input tokens.
- Stop when context pressure coincides with a new semantic decision or scope
  expansion.

## Validation Profile And Status Classes

- Runway density: `full-runway`.
- Profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Existing planning-store, skill-contract, scenario catalog, cross-checkout,
  installer, Ruff, BasedPyright, and whitespace checks are `required-green` or
  retain their explicitly recorded current baseline class.
- New owner tests and installed-owner scenarios are `implementation-created`
  until their owning slice makes them `required-green`.
- The existing manifest diagnostic retains its `known-red-baseline`; only the
  already assigned CCFG-24/25, CCFG-25, and CCFG-26 identities may remain red.
- Stable-interpreter dependency collection failures remain `diagnostic-only`
  and do not authorize package installation.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Implement and candidate-install bounded owner | Pending | migration | None | Not run | Pending | Two adapters, unchanged store, temporary ledgers only |
| 2. Bind scenarios and measure preparation evidence | Pending | migration | None | Not run | Pending | Installed-owner behavior and retained-surface inventory |

Accepted results move to `completed-slices.md`.

## Slice 1: Implement And Candidate-Install The Bounded Owner

### Scope

- Implement `scripts/add_to_ledger.py` and the installed skill boundary from the
  accepted decision amendment.
- Support only `plain_text` and `github_issue`.
- Implement exact create, same-source update, same-source no-op, unsupported or
  ambiguous block, complete-snapshot ID allocation, internal key derivation,
  and compact results.
- Explicit-target cross-source merge blocks in v1.
- Add focused direct tests against temporary schema-valid ledgers, including
  atomic multi-create, stale CAS, exact prepared-operation retry, and later
  independent reevaluation.
- Register only `planning-contracts` and `add-to-ledger`.
- After clean validation and review, install those features only into the
  candidate Codex home and verify exact links.

Old intake routes remain unchanged.

### Acceptance Criteria

- Human interaction requires no public mechanical identity.
- Both supported adapters construct deterministic identity and provenance.
- Create and multi-create allocate from one complete snapshot.
- Same-source unchanged content no-ops; accepted intake-owned changes update.
- Unsupported sources, explicit cross-source merge, ambiguous mapping, malformed
  namespace, and stale CAS write nothing.
- Candidate-installed execution rejects canonical mutation.
- Exact prepared-operation retry reaches store exact replay; a later human
  invocation reevaluates current state.
- Store, schemas, stable home, and old intake routes have no semantic diff.

### Focused Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_store.py
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check
```

Coordinator-owned candidate installation:

```sh
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature planning-contracts
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature add-to-ledger
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
```

### Reviews And Commit

- Independent owner/store/authority/failure-path review.
- `import_topology_reviewer`.
- Delta-only `test-quality-review`.
- Commit: `feat: prepare bounded add-to-ledger owner`.

### Stop Conditions

Stop on an unclosed decision, a third adapter, cross-source merge implementation,
store/schema change, public replay identity, canonical candidate write,
stable-home mutation, hidden APR semantics, or generalized ingestion framework.

## Slice 2: Bind Scenarios And Measure Preparation Evidence

### Approval Gate

Slice 1 is committed; direct and store tests are green; candidate links are
exact; independent, import-topology, and test-quality reviews are clean.

### Scope

- Rebind relevant CCFG-23 intake scenarios to the candidate-installed owner.
- Prove both source adapters, create, atomic multi-create, semantic no-op,
  accepted update, unsupported/ambiguous block, stale CAS, exact retry, and no
  downstream planning effects.
- Ensure every installed-owner scenario uses a fresh temporary or fixture ledger
  with canonical mutation disabled.
- Inventory every retained CCFG-23 intake helper/caller, APR intake route, and
  `legacy-removal` intake/lifecycle route.
- Record caller, reason, final CCFG-24 removal owner, and final-cutover removal
  condition for every retained surface.
- Record duration, coordinator context when available, evidence-pytest process
  count, changed-file count, line delta, and diff size.

### Acceptance Criteria

- Scenarios traverse `scripts/add_to_ledger.py` and do not bypass the installed
  owner.
- One atomic intake applies all supported mutations or writes nothing.
- Semantic no-op is distinct from mechanical exact replay.
- No candidate process can write canonical planning state.
- Old paths are unchanged and no longer the primary acceptance path for migrated
  intake scenarios.
- Every retained surface has a complete caller/reason/owner/condition entry.
- Exact acceptance preserves the current CCFG-23 contract and scenario counts
  with one evidence-pytest process.

### Focused Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
git diff --check
```

From a clean exact candidate commit, run CCFG-33 acceptance once with fresh
`/tmp/ccfg-24a-*` outputs.

### Reviews And Commit

- Independent installed-owner scenario review.
- `dead-surface-audit` for classification only.
- Delta-only `test-quality-review`.
- Final exact-range independent, import-topology, dead-surface, and test-quality
  reviews.
- Commit: `test: bind intake scenarios to installed owner`.

### Stop Conditions

Stop if scenarios bypass the installed owner, use canonical planning state,
require cleanup, omit a retained caller, regress non-intake behavior, add a
deferred adapter, implement cross-source merge, or expand into cutover.

## Final Validation

1. Confirm Planning State identifies only this CCFG-24A runway.
2. Run all required-green slice commands and strict cross-checkout checks.
3. Prove the store, schemas, and old intake paths have no semantic diff.
4. Reproduce the recorded manifest known-red identities without a new failure.
5. Run exact-commit acceptance once and validate its outputs.
6. Verify candidate links and unchanged stable links.
7. Record commit range, changed files, line delta, diff size, durations, context
   when available, process count, and retained-surface inventory.
8. Obtain clean exact-range reviews.
9. Write `completed-slices.md` and `closeout.md`; mark CCFG-24 `Prepared`; clear
   same-batch state; stop without selecting CCFG-24B or CCFG-25.

## Batch Stop Conditions

- Stop on Planning State mismatch, blocked strict preflight, repository movement,
  or dirty-file conflict.
- Stop on candidate canonical planning access or stable-home write.
- Stop if semantic decisions move into the store or another support owner.
- Stop if work exceeds the two supported adapters or implements cross-source
  merge.
- Stop if old intake paths, APR, `legacy-removal`, or fixtures must be removed or
  narrowed.
- Stop if CCFG-24 would be `Closed`.
- Stop if CCFG-24B or CCFG-25 is selected, dispatched, queued, or prepared.
- Stop after same-batch closeout with CCFG-24 `Prepared`.
