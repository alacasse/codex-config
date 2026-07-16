# CCFG-24A Intake Owner Preparation Runway

## Purpose

Implement and candidate-install the bounded `add-to-ledger/v1` owner, bind the
relevant intake scenarios to that installed owner, and collect compact evidence
for a later cutover reassessment.

Historical failure evidence is in `execution-report.md` and commits `33f7adf`,
`c087024`, and `199f4a9`. It must not be resumed.

## Authority

- Finding: CCFG-24, still `Pending`.
- Dispatch: `dispatch.md`.
- Source: COR-007 at `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Split boundary: `../../findings/ccfg-24-two-batch-execution-amendment.md`.
- Semantic decisions:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`.

The decision amendment owns command semantics. DEC-037 owns mechanical apply
replay. `ledger-store/v1` remains unchanged.

## Batch And Slice Shape

- Batch kind: `migration`.
- Slice 1: `migration` — implement, prove, register, and candidate-install the
  bounded owner.
- Slice 2: `migration` — bind scenarios and measure preparation evidence.

`slice_shape`: two slices.

`1 -> 2`: Slice 1 produces a reviewed installed owner over temporary ledgers.
Slice 2 consumes that exact owner in the broader harness. Old intake paths remain
unchanged, so the intermediate state is rollback-safe.

## Baseline

- Stable planning/toolchain checkout:
  `/home/alacasse/projects/codex-config` on `master`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign` on
  `implementation/command-owner-redesign`.
- Candidate baseline: `b38570bcd97b2584f3828abcd395b0f45ed91e58`.
- Stable home: `/home/alacasse/.codex`.
- Candidate home: `/home/alacasse/.codex-command-owner-redesign`.
- `scripts/planning_contract.py` is the read-only apply-only store.
- CCFG-33 owns exact-commit scenario acceptance with one evidence-pytest process.

Execution refreshes all live revisions and exact write scopes.

## Scope

Allowed candidate areas:

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `codex-features.json` and focused install metadata for `add-to-ledger` and
  `planning-contracts` only
- `tests/test_add_to_ledger.py`
- intake-only CCFG-23 scenario/catalog/adapter/test surfaces
- focused `plain_text` and `github_issue` fixtures
- `CHANGELOG.md`

Read-only except execution:

- `scripts/planning_contract.py`
- `tests/test_planning_contract_store.py`
- planning schemas and Planning State
- APR, `legacy-removal`, `plan-batch`, `work-batch`, and Batch Runway support

Non-goals:

- no public digest, request ID, replay token, or user-supplied idempotency key;
- no adapter beyond `plain_text` and `github_issue`;
- no cross-source merge, secondary provenance, fuzzy matching, generic ticket
  framework, or file ingestion;
- no store/schema/state semantic change;
- no old-owner narrowing or fixture deletion;
- no canonical planning write by candidate code or tests;
- no stable-home change, final cutover, CCFG-24B artifact, or CCFG-25 work.

A required change outside this scope stops execution for replan.

## Execution Contract

Use:

- Batch Runway Standard Execution Contract v2;
- Registered Agent Result Contract v2;
- Compact Report, Compact Convergence, Orchestration Anomaly Log, Standard Ledger
  Retention, and Execute Slice Core v1;
- `skills/batch-runway/references/cross-checkout-context-v1.md`;
- `skills/test-quality-review/SKILL.md`.

Workers implement one slice only and do not delegate. The coordinator owns
validation, independent review, candidate installation, commits, execution
ledger updates, and same-batch closeout.

## Planning Snapshot

Interface: `cross-checkout-context/v1`.

Helper: `/home/alacasse/.codex/scripts/cross_checkout_context.py`

Canonical planning root:
`/home/alacasse/projects/codex-config/docs/plans`

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

This is historical planning evidence, not a live lease. At startup and every
handoff, confirm current Planning State, obtain a fresh `ready` strict preflight,
and validate the exact delegated scope.

## Context Control

Read only:

1. current Planning State facts;
2. `dispatch.md`, this runway, and the decision amendment;
3. the active slice;
4. compact prior-slice receipts and reviews.

Open the historical report or broad redesign material only for a named
contradiction. Do not paste subagent transcripts into coordinator context.

- Soft execute budget: 100,000 input tokens.
- Hard warning: 150,000 input tokens.
- Stop when context pressure coincides with a new semantic choice or scope
  expansion.

## Validation Contract

Profile:
`skills/batch-runway/references/validation-profiles/project-harness-production.md`

- Existing planning-store, schema, contract, scenario, strict-context, installer,
  Ruff, BasedPyright, and whitespace checks: `required-green` or their explicitly
  recorded current baseline class.
- New owner tests and installed scenarios: `implementation-created`, promoted to
  `required-green` by their owning slice.
- Existing assigned manifest failures only: `known-red-baseline`.
- Stable-interpreter dependency collection failures: `diagnostic-only`.

Every test-changing slice receives independent review and delta-only
`test-quality-review`. Slice 1 and final range receive
`import_topology_reviewer`; Slice 2 receives `dead-surface-audit` for inventory
only.

## Execution Ledger

| Slice | Status | Risk | Commit | Validation | Review |
|---|---|---|---|---|---|
| 2. Bind scenarios and measure | Pending | migration | None | Not run | Pending |

Accepted results move to `completed-slices.md`.

## Slice 1: Implement And Install The Bounded Owner

### Work

- Implement the installed skill/script boundary from the decision amendment.
- Support only `plain_text` and `github_issue`.
- Implement create, same-source update, same-source no-op, block, complete-snapshot
  allocation, private key derivation, and compact results.
- Block explicit-target cross-source merge.
- Add direct tests against temporary schema-valid ledgers for multi-create,
  unsupported/ambiguous input, malformed namespace, stale CAS, exact prepared
  retry, later reevaluation, and canonical-write rejection.
- Register and install only `planning-contracts` and `add-to-ledger` in the
  candidate home after clean review.

### Acceptance

- No public mechanical identity is required.
- Both adapters produce deterministic identity and provenance.
- Supported mutations are atomic; blocked/stale cases write nothing.
- Exact retry reaches store replay; later invocation reevaluates current state.
- Store, schemas, stable home, and old intake routes have no semantic diff.

### Required-Green Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_planning_contract_store.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check
```

Candidate installation: dry-run, install `planning-contracts`, install
`add-to-ledger`, status, then convergence dry-run against
`/home/alacasse/.codex-command-owner-redesign`.

Reviews: independent owner/store/failure review, `import_topology_reviewer`, and
delta-only test-quality review.

Commit: `feat: prepare bounded add-to-ledger owner`

Stop on a third adapter, cross-source merge implementation, store/schema change,
public replay identity, canonical candidate write, stable-home mutation, hidden
APR semantics, or generalized ingestion framework.

## Slice 2: Bind Scenarios And Measure

### Gate

Slice 1 is committed; direct/store tests are green; candidate links are exact;
all Slice 1 reviews are clean.

### Work

- Rebind relevant CCFG-23 intake scenarios to the candidate-installed owner.
- Prove both adapters, create, multi-create, semantic no-op, update,
  unsupported/ambiguous block, stale CAS, exact retry, and no downstream effects.
- Use fresh temporary or fixture ledgers with canonical mutation disabled.
- Inventory every retained CCFG-23 intake helper/caller, APR intake route, and
  `legacy-removal` intake/lifecycle route with caller, reason, final CCFG-24
  removal owner, and removal condition.
- Record duration, context when available, evidence-pytest process count,
  changed-file count, line delta, and diff size.

### Acceptance

- Scenarios traverse `scripts/add_to_ledger.py` through the installed owner.
- Atomic intake applies all supported changes or writes nothing.
- Semantic no-op and mechanical exact replay remain distinct.
- Candidate processes cannot mutate canonical planning state.
- Old paths are unchanged and no longer primary acceptance for migrated intake.
- Retained-surface inventory is complete.
- Exact acceptance preserves current CCFG-23 scenario/contract counts with one
  evidence-pytest process.

### Required-Green Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
git diff --check
```

Run CCFG-33 exact-commit acceptance once from a clean candidate commit with fresh
`/tmp/ccfg-24a-*` outputs.

Reviews: independent installed-owner review, inventory-only dead-surface audit,
delta-only test-quality review, and final exact-range specialist reviews.

Commit: `test: bind intake scenarios to installed owner`

Stop if scenarios bypass the installed owner, use canonical planning state,
require cleanup, omit a retained caller, add a deferred adapter, implement
cross-source merge, regress non-intake behavior, or enter cutover.

## Final Validation And Closeout

1. Confirm only this CCFG-24A runway is queued or active.
2. Run both slices' required-green commands and strict cross-checkout validation.
3. Prove store, schemas, stable links, and old intake paths have no semantic diff.
4. Reproduce only the recorded manifest known-red identities.
5. Run exact-commit acceptance once and validate its outputs.
6. Record commits, changed files, line delta, diff size, durations, context when
   available, process count, installed links, and retained-surface inventory.
7. Obtain clean exact-range reviews.
8. Write `completed-slices.md` and `closeout.md`; mark CCFG-24 `Prepared`; clear
   same-batch state; stop without selecting CCFG-24B or CCFG-25.

## Batch Stop Conditions

Stop on Planning State mismatch, blocked preflight, repository movement, dirty
conflict, canonical candidate mutation, stable-home write, store ownership drift,
a third adapter, cross-source merge, required cleanup, CCFG-24 closure, or any
CCFG-24B/CCFG-25 selection. Stop after same-batch closeout with CCFG-24
`Prepared`.
