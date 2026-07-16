# CCFG-33 Acceptance Execution Simplification Dispatch

## Selection

- Batch ID: `ccfg-33-acceptance-execution-simplification`
- Source ledger: `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-33, Simplify CCFG-23 acceptance execution.
- Source packet:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/execution-retrospective.md`
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`
- CCFG-23 remains closed. CCFG-24 through CCFG-29 remain unselected.

## Amended Selection Decision

Select CCFG-33 as the only queued batch, but keep it bounded to the work named by
the source retrospective: optimize the CCFG-23 scenario-harness execution model
without changing production command ownership or unrelated manifest contracts.

The original plan split a second destructive-cleanup slice around three existing
known-red manifest tests. That was scope expansion. Those tests exercise
command-owner source, planning-owner, and closeout-owner boundaries; they do not
cause the CCFG-23 nested-pytest multiplier. They remain diagnostic until the
corresponding real ownership transfers:

- `test_executable_work_source_boundary_is_explicit`: CCFG-24/CCFG-25;
- `test_plan_batch_command_owner_runtime_boundaries_are_explicit`: CCFG-25;
- `test_work_batch_reconciles_same_batch_closeout`: CCFG-26.

CCFG-33 must not edit, delete, promote, or make green those tests. It must
preserve the exact known-red manifest baseline unless an unrelated baseline
change blocks execution.

The batch therefore has one semantic boundary: replace recursive acceptance
execution and its harness-internal preserving tests with a smaller exact-commit
acceptance path, then validate and close the same cohesive migration.

## Goal And Owner Seam

Make the accepted CCFG-23 evidence practical to run repeatedly:

- launch all declared evidence nodes in one pytest process for one immutable
  candidate commit;
- evaluate each scenario at most once per immutable input within that process;
- make JSON/text report formatting consume already validated evidence and never
  launch pytest;
- separate fast structural tests from runtime acceptance by behavior;
- replace repeated full report executions with pure formatting checks;
- remove per-test-function source hashes as acceptance authority, together with
  validator/tests that preserve that topology;
- preserve the six COR-006 keys, six aliases, 31 contracts, 17 families, 69
  scenario meanings, provenance checks, and all negative-runtime rejection
  classes; and
- record comparable before/after duration and process evidence.

Primary owner: `scripts/command_owner_scenarios.py`, its scenario schema/catalog,
and the four focused scenario test modules. No production command-owner skill,
manifest dependency, installed feature, or bridge is an implementation surface.

## Batch Kind And Risk

- Batch kind: `migration`.
- Slice risk: `migration`.
- Approval authority: the canonical queued CCFG-33 row plus an explicit later
  `work-batch` request.
- Required evidence before delegation:
  - Planning State still identifies this runway as the only queued or active
    batch;
  - strict first-handoff preflight is `ready`;
  - candidate `HEAD` descends from the closed CCFG-23 baseline and its worktree
    is clean;
  - all writes remain inside the non-installed harness allowlist; and
  - the known-red manifest baseline remains diagnostic and untouched.

No destructive-cleanup or contract-narrowing slice is authorized.

## Baseline And Cost Evidence

- Candidate repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Baseline candidate commit:
  `e8d07a785581e26ffb202b13ae43a0a83173205b`
- Four-module scenario suite: 123 passed in 814.32 seconds.
- One observed report: approximately 92.20 seconds.
- One observed report launches 13 pytest processes and performs four complete
  catalog evaluations.
- The suite performs 35 complete catalog evaluations; one instrumented
  evaluation launched 1,175 subprocesses, implying approximately 41,125
  process executions at the recorded suite shape.
- Full manifest diagnostic: exactly three failed, 18 passed, and 202 subtests
  passed. This is unrelated known-red evidence and is not CCFG-33 remediation.

Closeout must compare the final exact-commit acceptance path with this baseline
by cause and ratio. Benchmark instrumentation belongs to validation/closeout,
not to the permanent receipt contract.

## Acceptance Evidence Boundary

The acceptance result is private generated evidence, not a new public protocol
or durable repository schema. It must minimally bind:

- exact clean candidate commit;
- digest/identity of the schema, catalog, adapters, and selected evidence tests;
- exact selected evidence nodes;
- candidate interpreter/environment identity;
- one exclusive pytest result that rejects zero tests, failure, error, skip,
  xfail/xpass, and deselection;
- accepted aggregate report or its verified digest;
- wall duration; and
- proof that exactly one evidence-pytest process was used.

Do not add a permanent receipt schema file, public raw-observed-outcome API,
cross-run cache, or general CI framework. Child Git/Python/Planning State counts
may be measured externally for the before/after benchmark; they are not required
fields of the runtime receipt.

## Included Implementation Surfaces

- `schemas/command-owner-scenario-v1.schema.json`
- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_currentness.py`
- `tests/test_command_owner_scenario_cutover.py`
- `pyproject.toml`
- `CHANGELOG.md`

## Read-Only Diagnostic Surface

- `tests/test_codex_features_manifest.py`
- production skills, workflow docs, `codex-features.json`, installer and bridge
  code
- scenario adapters and fixture models reserved for CCFG-24 through CCFG-29

## Deferred And Excluded

- The three existing known-red manifest tests and their production-owner
  contracts.
- Production ownership transfer to `add-to-ledger`, `plan-batch`, or
  `work-batch`.
- Real installation, generation switching, rehearsal, cutover, rollback, or
  bridge deletion.
- Changing accepted scenario meanings, contract IDs, family membership,
  evidence keys, aliases, or provenance semantics.
- Persistent caching, committed receipts, a new stable receipt schema, or a
  GitHub Actions workflow.
- Restoring removed owners, dependencies, aliases, paths, or prose to satisfy a
  preserving test.

## Slice Shape

`slice_shape`: one slice.

The acceptance owner, session-local evaluation reuse, pure report rendering,
removal of per-function source-hash authority, directly associated tests,
validation, and changelog share one owner seam, migration risk, rollback
boundary, and acceptance contract. A second cleanup slice would either be
filler or improperly consume CCFG-24 through CCFG-26 scope.

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
  toolchain_commit: dded8097c947a745b63dbc44a4501d9b702b9f68
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: dded8097c947a745b63dbc44a4501d9b702b9f68
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: e8d07a785581e26ffb202b13ae43a0a83173205b
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

This remains immutable plan-time evidence. Execution must obtain fresh live
leases and separately validate write scope; do not rewrite this snapshot to the
commit containing this amendment.

## Stop Conditions

- Stop if Planning State no longer identifies this queued batch.
- Stop if strict preflight or any worker/reviewer lease/write-scope validation
  is blocked.
- Stop on candidate dirt or a diff outside the allowlist.
- Stop if report formatting launches pytest or one acceptance run needs more
  than one evidence-pytest process.
- Stop if per-function source hashes remain acceptance authority rather than
  being removed or demoted from the schema/catalog/validator/tests.
- Stop if a persistent cache, public outcome injection seam, permanent receipt
  schema, CI workflow, or committed generated receipt is introduced.
- Stop if any COR-006 behavior or negative-runtime/provenance protection weakens.
- Stop if `tests/test_codex_features_manifest.py`, production skills/docs,
  manifest dependencies, installed homes, bridge code, or CCFG-24+ ownership is
  changed.
- Stop if the exact three-failure manifest diagnostic changes without a named
  external cause.
- Stop if closeout lacks exact-commit duration and process evidence.
- Stop closeout before selecting or preparing any successor.
