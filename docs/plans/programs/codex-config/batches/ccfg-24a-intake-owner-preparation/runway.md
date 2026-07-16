# CCFG-24A Intake Owner Preparation Runway

## Purpose

Implement and candidate-install the bounded `add-to-ledger/v1` owner from the
accepted decision amendment, bind the relevant intake scenarios to that exact
installed owner, and collect the evidence needed for a later separately planned
cutover reassessment.

This runway replaces the blocked planning attempt preserved as
`blocked-runway.md`. It does not resume the blocked Slice 1. The old decision
slice is resolved by `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`.

## Source And Authority

- Finding: CCFG-24, still `Pending`.
- Dispatch: `dispatch.md`.
- Accepted source: COR-007 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Preparation/cutover boundary:
  `../../findings/ccfg-24-two-batch-execution-amendment.md`.
- Accepted semantic decisions:
  `../../findings/ccfg-24a-add-to-ledger-v1-decision-amendment.md`.
- Historical failure evidence: `execution-report.md`, `blocked-dispatch.md`, and
  `blocked-runway.md`.

The decision amendment controls semantic implementation. DEC-037 controls
mechanical apply replay. `ledger-store/v1` remains unchanged.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slice 1, Implement and candidate-install the bounded owner: `migration`.
- Slice 2, Bind scenarios and measure preparation evidence: `migration`.
- No contract-narrowing or destructive-cleanup slice is authorized.

`slice_shape`: two slices.

- `1 -> 2`: Slice 1 produces a directly tested and candidate-installed owner
  over temporary ledgers. Slice 2 consumes that exact installed command in the
  broader behavioral harness and produces an independently reviewable
  integration/evidence commit.

The intermediate state is valid and rollback-safe: old intake paths are
unchanged, the stable home is untouched, and the candidate owner has no
canonical mutation authority.

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
- Existing `scripts/planning_contract.py` implements accepted apply-only
  `ledger-store/v1` mechanics and is read-only for this batch.
- CCFG-33 provides the exact-commit acceptance owner with one evidence-pytest
  process.

Execution refreshes all live revisions and exact scopes. The immutable planning
snapshot below is historical selection evidence, not a live lease.

## Batch Non-Goals

- No public digest, idempotency key, request ID, or replay token.
- No store, planning-schema, or planning-state semantic change.
- No APR, `legacy-removal`, Batch Runway, `plan-batch`, or `work-batch`
  ownership narrowing.
- No intake fixture/helper deletion or topology cleanup.
- No canonical planning write by candidate code or tests.
- No stable-home install, refresh, unlink, rebind, or default switch.
- No final CCFG-24 cutover, CCFG-24B planning, or CCFG-25 work.

## Allowed Candidate Areas

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `codex-features.json`, limited to the target owner and neutral
  `planning-contracts` registration
- focused installation metadata for those two features
- `tests/test_add_to_ledger.py`
- intake-only CCFG-23 catalog, workflow-case, adapter, and scenario tests
- focused source fixtures required by the accepted adapters
- `CHANGELOG.md`
- compact preparation evidence produced under the current batch directory when
  closeout is written by the canonical coordinator

## Read-Only Candidate Areas

- `scripts/planning_contract.py`
- `tests/test_planning_contract_store.py`, except that it may be executed
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

Workers implement one slice only and do not delegate. The coordinator owns
validation, review, candidate installation, execution-ledger updates, commits,
and same-batch closeout. Every test-changing slice receives independent review
followed by delta-only test-quality review.

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

This snapshot was validated with the installed helper and an exact planning
write scope before the replacement artifacts were written. Preserve it
verbatim after this planning commit advances stable HEAD. At startup,
`work-batch` must confirm this exact queued scope through Planning State, obtain
a fresh `ready` live-lease preflight, and validate each handoff's exact write
scope. A stale or blocked preflight stops before delegation.

## Context Control

The execution coordinator reads current Planning State, this dispatch and
runway, the accepted decision amendment, the active slice, and compact prior
receipts. It reopens historical failure evidence or broad design material only
for a named contradiction.

- Soft execute budget: 120,000 input tokens.
- Hard warning: 180,000 input tokens.
- Stop when context pressure coincides with a new semantic decision or scope
  expansion.

## Validation Profile And Status Classes

- Runway density: `full-runway`.
- Profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Existing planning-store, skill-contract, scenario catalog, cross-checkout,
  installer, Ruff, BasedPyright, and whitespace checks are `required-green`.
- New owner tests and installed-owner scenarios are `implementation-created`
  until their owning slice makes them `required-green`.
- The existing manifest diagnostic retains its recorded
  `known-red-baseline`; only the already assigned CCFG-24/25, CCFG-25, and
  CCFG-26 identities may remain red.
- Stable-interpreter dependency collection failures remain `diagnostic-only`
  and do not authorize package installation.

Every concrete execution command must be recorded with one status class before
it gates acceptance.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Implement and candidate-install bounded owner | Pending | migration | None | Not run | Pending | Consume accepted amendment; unchanged apply-only store; temporary ledgers only |
| 2. Bind scenarios and measure preparation evidence | Pending | migration | None | Not run | Pending | Installed owner behavior, retained-surface inventory, and measured evidence |

Accepted results move to `completed-slices.md`.

## Slice 1: Implement And Candidate-Install The Bounded Owner

### Allowed Areas

- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `codex-features.json`, only target-owner and `planning-contracts` entries
- focused target-owner fixtures and `tests/test_add_to_ledger.py`
- `CHANGELOG.md`

### Non-Goals

- No CCFG-23 scenario migration yet.
- No edit to the store, schemas, planning-state, old intake owners, stable home,
  canonical planning artifacts, or cutover state.

### Scope

- Implement `scripts/add_to_ledger.py` and the human-facing skill boundary from
  the accepted decision amendment.
- Support only `github_issue`, structured `external_ticket`, `plain_text`,
  `git_file`, and `file_snapshot` adapters.
- Bind explicit invocation authority, complete-snapshot allocation, exact
  duplicate/update/controlled-merge/no-op/block behavior, prepared-operation
  key derivation, and command receipts.
- Add focused direct tests against temporary schema-valid ledgers, including
  interrupted retry of the same prepared operation and later independent
  reevaluation.
- Register only the neutral `planning-contracts` mechanism and target
  `add-to-ledger` feature links required by the owner.
- After validation and clean reviews, coordinator-install those two features
  only into the candidate Codex home and verify exact link ownership.

Old intake routes and installed support surfaces remain unchanged.

### Acceptance Criteria

- The human command accepts source material without public replay identity.
- Create and atomic multi-create allocate from one complete CAS-bound snapshot.
- Same-source unchanged content is semantic no-op; same-source accepted changes
  update; compatible explicit target merges only exact supported evidence;
  ambiguity blocks.
- Empty, malformed, mixed, concurrent, and stale allocation cases follow the
  accepted decision exactly.
- Git-bound files are verified at exact commit/path; standalone snapshots claim
  no Git provenance.
- Candidate-installed execution uses temporary or fixture ledgers only and
  rejects canonical mutation.
- Exact prepared-operation retry reaches store exact replay; a later human
  invocation reevaluates current state.
- `ledger-store/v1`, DEC-037, planning schemas, and old intake paths are
  unchanged.

### Focused Validation

Implementation-created, promoted to `required-green` by this slice:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/add-to-ledger/SKILL.md
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py
.venv/bin/basedpyright scripts/add_to_ledger.py
git diff --check
```

Existing `required-green` store regression:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_store.py
```

Coordinator-owned candidate installation after source validation and review:

```sh
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature planning-contracts
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature add-to-ledger
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
```

### Reviews

- Independent ownership, store-boundary, source, allocation, and failure-path
  review over the exact current diff.
- `import_topology_reviewer` for one semantic owner and narrow store imports.
- Delta-only `test-quality-review` for real file effects, negative paths, retry,
  and canonical-write rejection.

### Agent Briefs

- Worker: read this runway, the accepted decision amendment, and only the Slice
  1 candidate areas. The spawned `runway_worker` is already the required coding
  worker, implements this slice directly, uses the fresh strict live lease and
  exact candidate write scope, and must not spawn, delegate to, or wait on any
  additional agent. It must return the v2 result with verified cross-checkout
  identity and stop on any unclosed semantic choice.
- Reviewer: the coordinator supplies the exact task-scoped worktree diff before
  commit. The independent `runway_reviewer` stays read-only, validates the
  decision/store/authority/failure boundaries and permitted files, echoes
  `diff_basis` in its v2 result, and reports `clean`, `findings`, or `blocked`.

### Commit

`feat: prepare bounded add-to-ledger owner`

### Stop Conditions

- Stop on any decision not closed by the accepted amendment.
- Stop on store/schema semantic change, public replay identity, canonical
  candidate write, stable-home mutation, hidden APR semantics, or generalized
  source ingestion.

## Slice 2: Bind Scenarios And Measure Preparation Evidence

### Approval Gate

Slice 1 is committed; direct and store tests are green; candidate links are
exact; independent, import-topology, and test-quality reviews are clean.

### Allowed Areas

- `tests/test_add_to_ledger.py`, only integration additions not owned by Slice 1
- intake-only CCFG-23 scenario catalog, workflow-case, adapter, and scenario
  test surfaces
- focused intake source fixtures
- `CHANGELOG.md`
- current batch `completed-slices.md` and `closeout.md`, coordinator-owned only

### Non-Goals

- No owner/store/schema redesign.
- No fixture deletion, APR or `legacy-removal` narrowing, manifest cutover,
  stable-home mutation, canonical candidate write, CCFG-24B artifact, or
  CCFG-25 work.

### Scope

- Rebind the relevant CCFG-23 intake scenarios to the candidate-installed owner.
- Prove create, atomic multi-create, semantic no-op, accepted update,
  controlled merge/block behavior, stale CAS, unsupported source, exact retry,
  and no downstream planning effects.
- Ensure all candidate-installed scenario calls use fresh temporary or fixture
  ledgers and canonical mutation false.
- Inventory every retained CCFG-23 intake helper/caller, APR intake route, and
  `legacy-removal` intake/lifecycle route.
- Record caller, reason, final CCFG-24 removal owner, and final-cutover removal
  condition for every retained surface.
- Record slice and final duration, coordinator context when available,
  evidence-pytest process count, changed-file count, line delta, and diff size.
- Produce compact CCFG-24B reassessment evidence without creating a dispatch or
  runway.

### Acceptance Criteria

- Installed-owner scenarios cover every required positive and negative intake
  path without bypassing `scripts/add_to_ledger.py`.
- One atomic intake either applies all requested mutations or writes nothing.
- Semantic no-op is distinct from mechanical exact replay in observed results.
- No test or candidate process can write canonical planning state.
- Stable intake behavior remains green; old paths are unchanged and no longer
  the primary acceptance path for migrated scenarios.
- All retained surfaces have complete caller/reason/owner/condition entries.
- Exact acceptance preserves all 69 scenarios, 31 contracts, 17 families, six
  keys, and six aliases with one evidence-pytest process.

### Focused Validation

Implementation-created, promoted to `required-green` by this slice:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache scripts/add_to_ledger.py tests/test_add_to_ledger.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_catalog.py tests/fixtures/command-owner-scenarios/workflow_adapters.py
git diff --check
```

From a clean exact candidate commit, the coordinator runs CCFG-33 acceptance
once with fresh `/tmp/ccfg-24a-*` outputs:

```sh
.venv/bin/python scripts/command_owner_scenarios.py accept tests/fixtures/command-owner-scenarios --result-output /tmp/ccfg-24a-acceptance-result.json --json-report-output /tmp/ccfg-24a-report.json --text-report-output /tmp/ccfg-24a-report.txt
```

### Reviews

- Independent installed-owner scenario and behavior review.
- `dead-surface-audit` for retained-surface classification only.
- Delta-only `test-quality-review`.
- Final exact-range independent, import-topology, dead-surface, and test-quality
  reviews.

### Agent Briefs

- Worker: read this runway, Slice 1 commit receipt, and the installed-owner
  scenario boundary. The spawned `runway_worker` is already the required coding
  worker, implements only Slice 2, uses temporary or fixture ledgers with the
  fresh strict lease and exact candidate scope, and must not spawn, delegate to,
  or wait on another agent. It returns the v2 result and the complete retained-
  surface inventory without deleting or narrowing any surface.
- Reviewer: the coordinator supplies the exact Slice 2 task-scoped diff and
  installed-owner evidence. The independent `runway_reviewer` stays read-only,
  verifies that scenarios traverse the installed owner and that evidence and
  inventory are complete, echoes `diff_basis`, and reports `clean`, `findings`,
  or `blocked`.

### Commit

`test: bind intake scenarios to installed owner`

### Stop Conditions

- Stop if scenarios bypass the installed owner, use canonical planning state,
  require cleanup to pass, omit a retained caller, regress non-intake behavior,
  or expand into cutover.

## Final Validation

1. Confirm Planning State identifies only this queued/active CCFG-24A runway and
   no conflicting batch or successor.
2. Obtain a fresh strict read-only review lease for the exact final range.
3. Run all Slice 1 and Slice 2 required-green commands plus strict context,
   candidate installer status/dry-run, Ruff, BasedPyright, and whitespace gates.
4. Prove `scripts/planning_contract.py`, planning schemas, and old intake paths
   have no semantic diff.
5. Reproduce the exact recorded manifest known-red identities without a new
   failure.
6. Run the exact-commit acceptance command once and validate its three outputs.
7. Verify all candidate links resolve under the candidate source root and all
   stable links remain stable-owned without a stable write.
8. Record commit range, changed files, line delta, diff size, durations, context
   when available, evidence-pytest process count, and retained-surface inventory.
9. Obtain clean exact-range independent and specialist reviews.
10. Write `completed-slices.md` and `closeout.md`; mark CCFG-24 `Prepared`; clear
    same-batch state; stop without selecting CCFG-24B or CCFG-25.

## Closeout Result Contract

Successful closeout means the bounded owner is candidate-installed and
behaviorally exercised against non-canonical ledgers, the unchanged apply-only
store remains the sole mutation mechanism, all retained paths are classified,
CCFG-24 is `Prepared`, and final cutover remains unplanned.

## Batch Stop Conditions

- Stop on Planning State mismatch, conflicting selected/active state, blocked
  strict preflight, repository movement, or dirty-file conflict.
- Stop on candidate canonical planning access for mutation or stable-home write.
- Stop if semantic decisions move into the store or another support owner.
- Stop if any accepted source, allocation, duplicate, merge, or retry rule is
  still ambiguous.
- Stop if old intake paths, APR, `legacy-removal`, or fixtures must be deleted or
  narrowed.
- Stop if CCFG-24 would be `Closed`.
- Stop if CCFG-24B or CCFG-25 is selected, dispatched, queued, or prepared.
- Stop after same-batch closeout with CCFG-24 `Prepared`.
