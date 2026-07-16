# CCFG-33 Acceptance Execution Simplification Runway

## Purpose

Execute CCFG-33 in the redesign candidate checkout while canonical planning
remains on stable `master`. Replace reporter-owned recursive pytest with one
exact-commit acceptance execution, reuse one immutable scenario evaluation per
process/input identity, make report formatting pure, remove per-test-function
source hashes as acceptance authority, separate fast and runtime gates, and
record before/after cost evidence without changing COR-006 behavior.

## Identity And State

- Batch ID: `ccfg-33-acceptance-execution-simplification`
- Covered finding: CCFG-33.
- Source dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/dispatch.md`
- Canonical planning repository:
  `/home/alacasse/projects/codex-config`
- Implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Baseline implementation commit:
  `e8d07a785581e26ffb202b13ae43a0a83173205b`
- Execution ledger: this file.
- Completed-slice archive:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/completed-slices.md`
- Closeout:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/closeout.md`
- CCFG-23 remains closed. CCFG-24 through CCFG-29 remain open and unselected.

## Amended Batch Kind And Risk

- Batch kind: `migration`.
- Slice 1 risk: `migration`.
- No destructive-cleanup or contract-narrowing slice is authorized.

The previously planned Slice 2 was removed because the three known-red manifest
tests belong to future command-owner transfers, not to scenario-harness
execution cost. They remain read-only diagnostic evidence.

### Approval Gate

Approval authority is the queued CCFG-33 ledger row plus a later explicit
`work-batch` request. Before delegation:

- Planning State identifies this runway as the only queued or active batch;
- first strict live-lease preflight returns `ready` for this scope;
- candidate `HEAD` descends from the closed CCFG-23 baseline and its worktree is
  clean;
- intended writes are limited to the non-installed harness allowlist; and
- the exact known-red manifest diagnostic is unchanged.

## Current Baseline

- Stable plan-time snapshot commit:
  `dded8097c947a745b63dbc44a4501d9b702b9f68`.
- Candidate baseline commit:
  `e8d07a785581e26ffb202b13ae43a0a83173205b`.
- Four focused scenario modules: 123 passed in 814.32 seconds.
- One observed report: approximately 92.20 seconds.
- One observed report launches 13 pytest processes and performs four full
  catalog evaluations.
- The suite performs 35 full catalog evaluations. One instrumented evaluation
  launched 1,175 subprocesses, implying approximately 41,125 process
  executions at the recorded suite shape.
- Full manifest diagnostic: exactly three failed, 18 passed, and 202 subtests
  passed.
- The harness is non-installed evidence covering six keys, six aliases, 31
  immutable contracts, 17 families, and 69 scenario meanings.

## Scope Correction For Known-Red Manifest Tests

CCFG-33 must not edit `tests/test_codex_features_manifest.py` or promote its
full suite to required-green. The three failures are deferred as follows:

- `test_executable_work_source_boundary_is_explicit`: intake/planning ownership
  transfer under CCFG-24 and CCFG-25;
- `test_plan_batch_command_owner_runtime_boundaries_are_explicit`: planning
  ownership transfer under CCFG-25;
- `test_work_batch_reconciles_same_batch_closeout`: execution/closeout ownership
  transfer under CCFG-26.

During CCFG-33 the full manifest remains `known-red-baseline`. Final validation
must reproduce the same failure identities and the same 18-pass/202-subtest
green remainder. Do not restore old prose or owner topology to change this
baseline.

## Non-Goals

- Do not transfer production ownership to `add-to-ledger`, `plan-batch`, or
  `work-batch`.
- Do not change stable source, stable installed links, Codex homes, generation
  state, installer, bridge, production skill text, workflow docs, manifest
  dependencies, or `tests/test_codex_features_manifest.py`.
- Do not delete scenario adapters or fixture models reserved for CCFG-24 through
  CCFG-29 replacement.
- Do not change accepted scenario meanings, contract IDs, family membership,
  keys, aliases, or provenance semantics.
- Do not expose a public raw observed-outcome mapping.
- Do not add a permanent acceptance-receipt schema, committed receipt, durable
  cache, general benchmark subsystem, or GitHub Actions workflow.
- Do not optimize by arbitrary test count or a universal timeout.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2.
Use Batch Runway Compact Report Contract v1 for coordinator receipts and other
non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1.
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

Overrides:

- The final live acceptance gate is coordinator-owned. Worker and reviewer must
  not independently rerun it.
- A green generated receipt may be reused only for read-only review of the exact
  same clean commit and matching input identity.
- Candidate movement invalidates the receipt and requires one new final
  acceptance execution after the next committed fix.

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
  toolchain_commit: dded8097c947a745b63dbc44a4501d9b702b9f68
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: dded8097c947a745b63dbc44a4501d9b702b9f68
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: e8d07a785581e26ffb202b13ae43a0a83173205b
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

This is immutable plan-time evidence. At execution startup, `work-batch` must
confirm the selected scope through Planning State and obtain a fresh ready
preflight. Every worker/reviewer handoff requires a newly prepared strict live
lease and separately validated write scope.

## Implementation Contract

### 1. One Acceptance Execution Owner

Add one internal acceptance owner in `scripts/command_owner_scenarios.py` that:

- resolves all declared aggregate-evidence nodes;
- invokes them together in exactly one pytest process and one JUnit/output
  observation;
- rejects zero tests, failures, errors, skips, xfail/xpass, deselection, missing
  nodes, foreign interpreter, stale commit, changed inputs, and raw outcome
  substitution; and
- derives the aggregate report only from verified runtime evidence.

### 2. One Evaluation Per Immutable Input

Within one Python/pytest process, repeated consumers of the same immutable
catalog and source identity must reuse one evaluation result rather than
rebuilding all 69 scenarios. The reuse must be process-local or session-local:

- no committed cache;
- no cross-commit cache;
- no reuse after catalog, schema, adapter, evidence-test, interpreter, or
  environment movement; and
- no public caller-controlled green result.

Evidence-node tests that currently rebuild the full catalog should consume a
shared immutable evaluation or evaluate only their declared scenario subset.

### 3. Pure Report Formatting

`report` formatting must not launch pytest. It may:

- render an explicit unobserved/non-green report; or
- consume a fully validated generated result for the exact current commit.

JSON/text determinism tests must format the same report repeatedly rather than
run acceptance repeatedly.

### 4. Minimal Generated Acceptance Result

The generated result is private validation evidence, not a new stable public
contract. Keep it minimal:

- exact clean candidate commit;
- identity/digest of schema, catalog, adapters, and selected evidence tests;
- exact evidence nodes;
- candidate interpreter/environment identity;
- exclusive pytest outcome summary;
- accepted report or verified report digest;
- wall duration; and
- evidence-pytest process count, which must be one.

A small internal interface/version tag is permitted. Do not create a separate
schema file or generalized receipt framework. Measure detailed child-process
counts externally during final benchmarking rather than adding instrumentation
to the permanent harness.

### 5. Remove Per-Function Source-Hash Authority

Remove `source_sha256` for individual pytest functions from acceptance
ownership:

- update `schemas/command-owner-scenario-v1.schema.json`;
- update the live catalog;
- delete or simplify AST/source-extraction and hash-comparison code;
- delete or migrate tests that exist only to preserve exact function bodies,
  decorators, or source hashes; and
- bind the overall exact input identity through the generated acceptance result
  instead.

Retain runtime proof against skip, xfail/xpass, deselection, zero tests,
failure, error, foreign interpreter, and evidence-node substitution.

## Allowed Files

- `schemas/command-owner-scenario-v1.schema.json`
- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_currentness.py`
- `tests/test_command_owner_scenario_cutover.py`
- `pyproject.toml`
- `CHANGELOG.md`

## Read-Only Files

- `tests/test_codex_features_manifest.py`
- `codex-features.json`
- production skills and workflow documentation
- installer, bridge, and scenario adapter implementations

## Validation Profile

Profile: `project-harness-production`.

### Recorded Baselines — Do Not Rerun Unchanged

Scenario baseline:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py
```

Status: `required-green`; recorded result 123 passed in 814.32 seconds.

Manifest diagnostic:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
```

Status: `known-red-baseline`; expected result exactly the same three failures,
18 passes, and 202 passing subtests.

### Implementation-Created Gates

The worker may choose markers, explicit selectors, or a small focused module,
but must prove a complete semantic partition.

Fast gate requirements:

- schema/catalog validation;
- aggregate mapping and exact observation comparison;
- generated-result validation and tamper/staleness rejection;
- pure JSON/text formatting;
- negative shape/input tests;
- no disposable Git repository setup, installer/cutover execution, or nested
  pytest.

Acceptance gate requirements:

- all declared runtime evidence nodes in one pytest process;
- disposable Git/Planning State/install/cutover behavior;
- all negative runtime outcomes and provenance checks;
- one exact-commit generated result and accepted report.

Implementation-created command examples may be added to this runway's execution
ledger after Slice 1 code chooses the concrete interface. Do not invent
nonexistent selectors as pre-existing required-green commands.

### Shared Checks

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache schemas/command-owner-scenario-v1.schema.json scripts/command_owner_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py
.venv/bin/basedpyright scripts/command_owner_scenarios.py
git diff --check e8d07a785581e26ffb202b13ae43a0a83173205b
```

If Ruff does not accept the JSON schema path, lint only changed Python files and
validate the schema through the catalog validator. Do not widen scope to tooling
configuration solely for that command shape.

## Slice Shape

`slice_shape`: one slice.

The acceptance execution owner, process-local evaluation reuse, pure formatting,
source-hash removal, focused tests, directly associated configuration/changelog,
and final validation share one owner, migration risk, rollback boundary, and
acceptance contract. No valid independently shippable second slice remains.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Simplify exact-commit acceptance execution | Pending | migration | — | — | — | One owner; known-red manifest remains unchanged diagnostic evidence |

## Slice 1: Simplify Exact-Commit Acceptance Execution

### Scope

Implement the five-part Implementation Contract above. During implementation:

- use the smallest affected tests rather than the full acceptance gate;
- remove redundant harness-internal topology/source-hash tests in the same diff
  as the mechanism they preserve;
- classify any failing test before restoring code;
- preserve behavior and named compatibility contracts, but delete or migrate
  migration-retention/topology assertions with no external contract; and
- prefer deletion and direct data flow over a generalized cache, receipt, or
  reporting framework.

### Acceptance Criteria

- One acceptance execution launches exactly one evidence-pytest process.
- The scenario catalog is evaluated once per immutable process/input identity.
- Report formatting launches no pytest.
- Raw caller outcomes cannot make aggregate evidence green.
- Per-function source hashes and their preserving validator/tests are removed or
  no longer authoritative.
- Fast and acceptance gates are behaviorally complete and disjoint.
- All six keys, six aliases, 31 contracts, 17 families, 69 scenario meanings,
  negative-runtime outcomes, and provenance checks remain green.
- The exact known-red manifest diagnostic is unchanged.
- Combined schema/harness/test implementation should be net-negative in lines;
  any net growth requires reviewer evidence that it is essential rather than a
  new generalized machine.
- Focused tests, fast gate, catalog validation, Ruff, BasedPyright, and range
  whitespace pass before commit.

### Validation And Review

- Run focused tests and the fast gate before worker completion.
- Do not run final live acceptance from worker or reviewer.
- Test-quality review: `delta-only`, focused on anti-self-certification,
  semantic gate partition, failure coverage, evaluation reuse, and whether new
  machinery is proportional.
- Independent review must verify the exact task-scoped diff, allowlist,
  source-hash deletion, unchanged COR-006 behavior, unchanged manifest baseline,
  and absence of production/cutover drift.

### Worker Brief

The spawned `runway_worker` is the coding subagent. Read this runway from the
stable planning checkout, implement only Slice 1 in the candidate checkout, and
do not spawn or wait on another subagent. Do not run final live acceptance,
install anything, edit stable planning, edit read-only files, add CI, or create a
permanent receipt/cache framework. Return the required v2 compact result with
exact changed paths and verified strict context.

### Reviewer Brief

The separate `runway_reviewer` reviews the coordinator-provided exact worktree
diff. Verify single-pytest ownership, process-local reuse, minimal generated
evidence, pure formatting, source-hash authority removal, semantic gate
partition, unchanged COR-006 meanings, unchanged known-red manifest baseline,
allowlist compliance, and proportional deletion-first implementation. Echo
`diff_basis` and verified strict context in the v2 result.

### Commit

`refactor: simplify command-owner acceptance execution`

### Slice Stop Conditions

- Stop if the implementation introduces a permanent generalized cache, schema,
  CI workflow, or public raw outcome seam.
- Stop if one acceptance run uses multiple evidence-pytest processes or report
  formatting launches pytest.
- Stop if reuse crosses input/commit/environment movement.
- Stop if source-hash topology is preserved as acceptance authority.
- Stop if any COR-006 or negative-runtime/provenance behavior weakens.
- Stop if read-only manifest/production/cutover files must change.

## Final Validation

Final validation occurs after the slice commit and a clean candidate worktree.

1. Confirm Planning State still identifies CCFG-33 and strict preflight is
   `ready`; record exact stable and candidate revisions.
2. Run the fast gate, focused harness suite, catalog validation, Ruff,
   BasedPyright, and candidate-range `git diff --check`.
3. Run the exact-commit acceptance command once and validate its generated
   result.
4. Render JSON and text from the same validated result and prove formatting
   starts no pytest process.
5. Confirm all 69 scenario meanings, 31 contracts, 17 families, six keys, six
   aliases, negative-runtime outcomes, and provenance checks remain green.
6. Run the full manifest diagnostic and require the exact same three failure
   identities, 18 passes, and 202 passing subtests.
7. Record final wall duration, evidence-pytest process count, full-catalog
   evaluation count, and available externally measured child-process counts.
8. Compare with the recorded 814.32-second, 13-pytest-per-report,
   35-evaluation, approximately 41,125-process baseline by cause and ratio.
9. Run final exact-range `delta-only` test-quality review and independent review
   over `e8d07a785581e26ffb202b13ae43a0a83173205b..<final-candidate-commit>`.
10. Verify both worktrees clean and every committed path inside scope.
11. Write `completed-slices.md` and `closeout.md`; close CCFG-33, clear queued
    state, and select no successor.

## Batch Stop Conditions

- Stop if Planning State identifies another scope or strict context/write-scope
  validation fails.
- Stop on unexpected repository movement, dirty conflict, or path outside the
  allowlist.
- Stop if acceptance is not bound to a clean exact candidate commit.
- Stop if reporter formatting launches pytest, more than one evidence-pytest
  process is required, or raw outcomes self-certify.
- Stop if a persistent generalized machine replaces the simpler direct flow.
- Stop if COR-006 behavior, evidence identity, negative-runtime rejection,
  provenance, or topology independence weakens.
- Stop if the manifest known-red baseline changes or any read-only file is
  modified.
- Stop if cost evidence is missing or guessed.
- Stop if execution touches production ownership transfer, real cutover,
  installed homes, bridge code, or CCFG-24 through CCFG-29 scope.
- Stop closeout before selecting or preparing any successor.
