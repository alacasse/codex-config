# CCFG-33 Acceptance Execution Simplification Dispatch

## Selection

- Batch ID: `ccfg-33-acceptance-execution-simplification`
- Source ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-33, Simplify CCFG-23 acceptance execution.
- Source packet:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/execution-retrospective.md`
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`
- CCFG-23 remains closed. CCFG-24 through CCFG-29 remain unselected.

## Selection Decision

Select the user-requested CCFG-33 row. Planning State reports no selected
dispatch, queued runway, active runway, or blocker. CCFG-33 is the canonical
ledger's recommended next command-owner-redesign work and CCFG-24 waits for it.

The vague-row guard passes after applying the source retrospective and a
focused dead-surface audit. The batch has two explicit semantic boundaries:

1. migrate the non-installed CCFG-23 harness from reporter-owned recursive
   pytest to one exact-commit acceptance run and validated receipt while
   preserving all COR-006 behavior; then
2. remove or migrate three test functions that preserve exact prose and runtime
   topology only after their behavioral obligations are mapped to the green
   scenario harness.

The first boundary is a behavior-preserving harness migration. The second is a
separate destructive test-cleanup boundary with its own approval and rollback
gate. Production command-owner transfer, real cutover, and bridge deletion are
not part of this batch.

## Goal And Owner Seam

Make the accepted CCFG-23 evidence practical to run repeatedly without letting
the report self-certify its own pytest evidence:

- one acceptance owner launches all declared evidence nodes in one pytest
  process for one immutable candidate commit;
- one validated receipt binds the candidate commit, environment, input
  digests, exclusive pytest result, duration, and process/evaluation evidence;
- report formatting consumes validated observed evidence without launching
  pytest;
- schema, mapping, pure comparison, and negative-shape checks form a fast gate;
- runtime evidence, disposable Git/install behavior, negative runtime outcomes,
  and end-to-end observed reporting form the acceptance gate;
- repeated JSON/text determinism checks reuse one validated immutable report;
  and
- the six COR-006 keys, six aliases, 31 contracts, 17 families, 69 scenarios,
  provenance checks, and every negative-runtime rejection remain green.

Primary owner: `scripts/command_owner_scenarios.py` and its four focused
scenario test modules. The aggregate-evidence node declarations remain in the
scenario catalog. No production command-owner skill or installed feature is an
implementation surface.

## Batch Kind, Risk, And Approval

- Batch kind: `mixed-risk`.
- Slice 1 risk: `migration`.
  - Approval authority: the canonical CCFG-33 ledger row plus a later explicit
    `work-batch` request.
  - Required evidence: Planning State still identifies this queued runway;
    candidate baseline remains the closed CCFG-23 commit lineage; all work stays
    inside the non-installed harness; and focused receipt/anti-self-certification
    tests are green before commit.
- Slice 2 risk: `destructive-cleanup`.
  - Approval authority: the canonical CCFG-33 ledger row plus a later explicit
    `work-batch` request.
  - Required evidence: Slice 1 is committed and reviewed; a fresh
    `dead-surface-audit` still classifies each removed assertion as
    `delete-now` or `migrate-tests-first`; every retained semantic obligation is
    mapped to green behavioral evidence; and no test classified `keep`,
    `keep-thin-entrypoint`, or `human-contract-decision` is deleted.

## Dead-Surface Evidence

The current candidate manifest suite has exactly three known-red tests: 18
other tests and 202 subtests pass. Each failure is caused by exact prose or
runtime-owner topology assertions while the underlying command-owner behavior
is represented in the accepted scenario catalog.

| Surface | Caller and contract evidence | Status | Required action |
|---|---|---|---|
| `test_executable_work_source_boundary_is_explicit` | Test-only exact Markdown phrasing; intake/planning source behavior belongs to INTAKE/PLAN scenario contracts | `migrate-tests-first` | Preserve the behavior in scenario evidence, then remove exact prose coupling |
| `test_plan_batch_command_owner_runtime_boundaries_are_explicit` | Test-only manifest dependency and support-owner topology plus exact prose; CCFG-23 planning and topology-independent evidence is authoritative | `migrate-tests-first` | Keep behavioral planning boundaries, delete runtime-topology preservation |
| `test_work_batch_reconciles_same_batch_closeout` | Test-only dependency/prose checks; `closeout-same-batch-no-successor` and fault scenarios protect observable closeout behavior | `migrate-tests-first` | Keep observable closeout evidence, delete exact prose/topology preservation |

This classification does not authorize restoring a phrase, dependency, helper,
alias, or removed owner solely to make the old tests pass.

## Baseline And Cost Evidence

- Candidate repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`
- Baseline candidate commit:
  `e8d07a785581e26ffb202b13ae43a0a83173205b`
- Baseline scenario suite: 123 passed in 814.32 seconds.
- One observed report: approximately 92.20 seconds.
- One observed report launches 13 pytest processes and performs four complete
  catalog evaluations.
- The focused suite performs 35 complete catalog evaluations; one instrumented
  evaluation launched 1,175 subprocesses, implying approximately 41,125
  process executions at the recorded suite shape.
- Full manifest baseline reconfirmed at the same candidate commit: exactly
  three failed, 18 passed, and 202 subtests passed.

Closeout must compare the final exact-commit acceptance receipt with this
baseline by cause and ratio. It must record duration, evidence-pytest process
count, catalog-evaluation count, and available child-process evidence without
inventing a universal timeout or arbitrary pass threshold.

## Validation Class And Artifacts

- Validation profile: `project-harness-production`.
- Runway density: `full-runway` because the batch changes acceptance evidence
  ownership, retains anti-self-certification, uses strict cross-checkout
  execution, and includes destructive test cleanup.
- Test-quality review: `delta-only` for both slices and the final exact
  candidate range.
- Harness output root for this batch:
  `/tmp/codex-config-ccfg-33-acceptance/`.
- The acceptance receipt is generated output, not Planning State. The exact
  receipt summary and digest belong in completed-slice/closeout evidence; raw
  JSON must not become active planning state.
- No install, default-generation switch, index refresh, or generated-doc
  refresh is required.

## Included Implementation Surfaces

- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_currentness.py`
- `tests/test_command_owner_scenario_cutover.py`
- `tests/test_codex_features_manifest.py`
- `pyproject.toml`
- `CHANGELOG.md`

## Deferred And Excluded

- Changes to production `add-to-ledger`, `plan-batch`, or `work-batch`
  ownership; CCFG-24 through CCFG-26 own those migrations.
- Real candidate installation, default-generation switching, rehearsal,
  cutover, rollback, or bridge deletion; CCFG-27 through CCFG-29 own them.
- Deleting CCFG-23 scenario adapters or fixture models that CCFG-24 through
  CCFG-29 are assigned to replace.
- Changing the 69 scenario semantics, 31 immutable contract identities, 17
  families, six keys, or six aliases.
- Exposing a public caller-controlled raw observed-outcome mapping.
- Adding a universal duration threshold or optimizing by arbitrary test count.
- Restoring removed runtime owners, dependencies, aliases, paths, or prose to
  satisfy topology/migration-retention tests.
- Changing stable installed files or the stable Codex home.

## Slice Shape

`slice_shape`: two slices.

- `1 -> 2`: Slice 1 produces a valid reviewed acceptance-run/receipt boundary
  with green fast validation. Slice 2 consumes that boundary to remove or
  migrate preserving tests. The split is required because the owner seam,
  risk class, approval gate, rollback boundary, and acceptance evidence differ.
- Cost evidence and changelog text stay with the behavior they report; they do
  not form filler slices.

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

The installed helper parsed this payload and validated six canonical planning
paths plus the nine candidate implementation paths listed above. This payload
is an immutable planning snapshot, not a live execution lease. Do not rewrite
it after the containing plan commit advances stable `HEAD`.

## Stop Conditions

- Stop if Planning State no longer identifies this selected/queued batch.
- Stop if strict live-lease preflight is blocked or a worker/reviewer handoff
  lacks newly validated exact context and write scope.
- Stop if the candidate worktree is dirty before Slice 1 or a slice diff
  escapes its allowlist.
- Stop if reporter formatting still launches pytest or acceptance requires more
  than one evidence-pytest process for one exact commit.
- Stop if a caller-controlled raw outcome map can make the aggregate green.
- Stop if any COR-006 key, alias, contract, family, scenario, provenance check,
  negative-runtime rejection, or topology-independent behavior weakens.
- Stop if obsolete test cleanup lacks canonical dead-surface evidence or would
  delete a `keep`, `keep-thin-entrypoint`, or `human-contract-decision` surface.
- Stop if implementation restores removed production code or old topology to
  satisfy a preserving test.
- Stop if execution touches stable production files, installed homes, CCFG-24+
  owners, real cutover state, or the temporary bridge.
- Stop if final closeout lacks exact-commit duration and process evidence.
- Stop closeout before selecting or preparing CCFG-24 or any other successor.
