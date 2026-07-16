# CCFG-33 Acceptance Execution Simplification Runway

## Purpose

Execute the selected CCFG-33 finding in the redesign candidate checkout while
keeping canonical planning in stable. Replace reporter-owned recursive pytest
with one exact-commit acceptance run and validated receipt, separate fast and
acceptance gates by behavior, remove or migrate obsolete preserving tests, and
record before/after duration and process evidence without changing COR-006
semantics or reopening CCFG-23.

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

## Batch Kind And Slice Risk

- Batch kind: `mixed-risk`.
- Slice 1: `migration`; move accepted evidence execution behind one
  exact-commit acceptance-run/receipt boundary.
- Slice 2: `destructive-cleanup`; delete or migrate preserving test assertions
  only after their behavioral obligations are protected by Slice 1 and the
  accepted scenario catalog.

### Slice 1 Approval Gate

Approval authority is the canonical CCFG-33 ledger row plus a later explicit
`work-batch` request. Before delegation:

- Planning State must identify this runway as the only queued or active batch;
- the first strict live-lease preflight must return `ready` for the same selected
  scope;
- candidate `HEAD` must descend from the closed CCFG-23 baseline and the
  candidate worktree must be clean;
- the slice must remain inside the non-installed scenario harness and its
  focused tests; and
- no production command-owner, installed generation, or bridge surface may be
  changed.

### Slice 2 Approval Gate

Approval authority is the canonical CCFG-33 ledger row plus a later explicit
`work-batch` request. Before delegation:

- Slice 1 must be committed, focused validation green, and independently
  reviewed;
- the coordinator must refresh the dispatch's focused `dead-surface-audit` and
  classify every assertion proposed for deletion as `delete-now` or
  `migrate-tests-first`;
- each retained semantic obligation must map to a named green scenario,
  contract, or focused behavioral test;
- no `keep`, `keep-thin-entrypoint`, or `human-contract-decision` surface may be
  deleted; and
- the three-test known-red manifest baseline must still be exact before Slice 2
  changes it.

## Current Baseline And Assumptions

- Planning State `current` and `validate` passed with no blockers before this
  runway was created. The two redirect-ledger warnings are known and unrelated.
- Stable `master` was clean at
  `dded8097c947a745b63dbc44a4501d9b702b9f68`.
- Candidate `implementation/command-owner-redesign` was clean at
  `e8d07a785581e26ffb202b13ae43a0a83173205b`.
- The four focused scenario modules pass 123 tests at the baseline commit. The
  accepted final run took 814.32 seconds.
- One observed report launches 13 pytest processes and evaluates the full
  catalog four times. The full focused suite evaluates it 35 times.
- One instrumented catalog evaluation launched 1,175 subprocesses; the
  retrospective estimates approximately 41,125 process executions for the
  baseline suite shape.
- The full candidate manifest baseline was reconfirmed during planning: exactly
  three failed, 18 passed, and 202 subtests passed. The failures are the three
  preserving tests listed in the dispatch.
- The harness is non-installed CCFG-23 evidence. Its six keys, six aliases, 31
  immutable contracts, 17 families, and 69 scenario semantics are the behavior
  contract for this batch.
- The explicit generated-output root is
  `/tmp/codex-config-ccfg-33-acceptance/`. Receipt summaries and digests are
  persisted in execution/closeout Markdown; raw receipt JSON is not Planning
  State.

## Non-Goals

- Do not transfer production ownership to `add-to-ledger`, `plan-batch`, or
  `work-batch`.
- Do not change stable source, stable installed links, either Codex home, real
  default-generation state, or temporary cross-checkout bridge code.
- Do not delete scenario adapters or fixture models reserved for CCFG-24 through
  CCFG-29 replacement.
- Do not change accepted scenario meanings, contract IDs, family membership,
  evidence keys, aliases, provenance checks, or negative-runtime semantics.
- Do not expose a public raw observed-outcomes argument or let a caller claim
  acceptance without an exact validated receipt.
- Do not optimize through arbitrary test-count thresholds or a universal
  timeout.
- Do not add cache state or receipts to the repository, active planning state,
  or installed homes.
- Do not restore old prose, runtime dependencies, owner topology, aliases,
  paths, or helper names to satisfy preserving tests.

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
- `skills/dead-surface-audit/SKILL.md`

Overrides:

- The full live acceptance gate is coordinator-owned final validation. Workers
  and reviewers must not launch it unless a recovery handoff explicitly assigns
  one exact candidate commit and receipt path.
- A green exact-commit receipt may be reused for read-only same-commit review.
  Any candidate movement or input-digest mismatch invalidates reuse.
- If a material fix changes candidate `HEAD`, final acceptance runs again for
  that new exact commit; this is a new necessary gate, not an unchanged rerun.

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

This planning snapshot is immutable historical evidence, not a live execution
lease. Do not rewrite it after the containing planning commit or later
between-flight commits advance stable `HEAD`. At execution startup,
`work-batch` must confirm this selected scope through Planning State and call
the installed helper's ready/blocked preflight. Every later worker/reviewer
handoff requires a newly prepared strict live lease, separately validated write
scope, the canonical planning root, and the installed helper path.

Planning validated these canonical paths:

- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- this dispatch and runway
- this batch's future `completed-slices.md` and `closeout.md`

Planning validated these candidate paths:

- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- the four `tests/test_command_owner_*scenario*.py` focused modules named in
  the dispatch
- `tests/test_codex_features_manifest.py`
- `pyproject.toml`
- `CHANGELOG.md`

## Acceptance Receipt Contract

Slice 1 must create an internal acceptance owner that runs all declared evidence
nodes in one pytest process and emits one versioned receipt for one immutable
candidate commit. The exact internal type and serialization layout may be
chosen by the worker, but acceptance requires all of these facts:

- interface/version identifier;
- exact candidate repository root and 40-character commit;
- candidate Python/pytest environment identity and provenance;
- catalog digest, adapter-source digests, evidence-test source digests, and the
  exact selected evidence nodes;
- exact pytest command and JUnit/output digest;
- start/end or wall duration;
- collected, passed, failed, error, skipped, xfailed, xpassed, and deselected
  outcomes sufficient to reject every non-exclusive pass and zero-test result;
- evidence-pytest process count;
- full-catalog evaluation count;
- available child-process counts grouped at least by Git, candidate Python, and
  Planning State when the harness can observe them without faking execution;
- the six key and six alias results; and
- a receipt digest used by pure report formatting and same-commit review.

The acceptance owner must reject stale commit, foreign interpreter, changed
catalog/adapter/test inputs, missing nodes, deselection, skip, xfail/xpass,
failure, error, zero tests, and caller-provided raw outcome substitution. Report
formatting must never launch pytest.

## Validation Profile

Profile: `project-harness-production`.

### Baseline Commands

- Full scenario baseline, accepted green at the exact baseline commit:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py
  ```

  Status: `required-green`. Current recorded result: 123 passed in 814.32s.
  Do not rerun this unchanged baseline during execution.

- Full manifest:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
  ```

  Status: `known-red-baseline`. Current result: exactly three failed, 18 passed,
  and 202 subtests passed. Slice 2 owns remediation and promotion to
  `required-green`.

### Implementation-Created Gates

- Fast gate:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider -m 'not command_owner_acceptance' tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py
  ```

  Status: `implementation-created`. Slice 1 registers the marker, proves the
  fast/acceptance partition is complete and disjoint, and promotes this to
  `required-green` before its commit.

- Focused receipt and partition tests:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_command_owner_scenario_catalog.py tests/test_command_owner_scenario_cutover.py -k 'acceptance_runner or acceptance_receipt or fast_and_acceptance_markers or report_formatting_reuses_receipt'
  ```

  Status: `implementation-created`. Slice 1 creates the named behavior and
  promotes this to `required-green` before its commit.

- Exact-commit acceptance run:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/command_owner_scenarios.py accept tests/fixtures/command-owner-scenarios --receipt-root /tmp/codex-config-ccfg-33-acceptance --format json --durations 20
  ```

  Status: `implementation-created`. Slice 1 creates it. The coordinator runs it
  only in final validation from a clean exact candidate commit. The command must
  run all evidence nodes through one pytest process and write the receipt under
  a commit-keyed path below the explicit receipt root.

- Receipt-backed pure report:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/command_owner_scenarios.py report tests/fixtures/command-owner-scenarios --receipt-root /tmp/codex-config-ccfg-33-acceptance --format json
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/command_owner_scenarios.py report tests/fixtures/command-owner-scenarios --receipt-root /tmp/codex-config-ccfg-33-acceptance --format text
  ```

  Status: `implementation-created`. Slice 1 creates it. Both commands must reuse
  the exact current-commit receipt, emit the same accepted evidence, and launch
  no pytest process.

### Shared Focused Checks

- Catalog validation:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
  ```

  Status: `required-green` at the baseline commit.

- Lint and type checks:

  ```sh
  .venv/bin/ruff check --no-cache scripts/command_owner_scenarios.py tests/test_command_owner_scenario_catalog.py tests/test_command_owner_behavioral_scenarios.py tests/test_command_owner_scenario_currentness.py tests/test_command_owner_scenario_cutover.py tests/test_codex_features_manifest.py
  .venv/bin/basedpyright scripts/command_owner_scenarios.py
  ```

  Status: `required-green` at the baseline commit.

- Candidate range whitespace:

  ```sh
  git diff --check e8d07a785581e26ffb202b13ae43a0a83173205b
  ```

  Status: `required-green`.

Project-level installs, stable/candidate generation switches, index refreshes,
and generated-doc refreshes are not worker validation.

## Slice Shape

`slice_shape`: two slices.

- `1 -> 2`: Slice 1 creates the acceptance-run/receipt boundary consumed by
  Slice 2's behavior-preserving test cleanup. The intermediate candidate is
  valid, fast-green, independently reviewable, and rollback-safe. Slice 2 has a
  different owner seam, destructive risk, approval gate, and validation
  promotion, so combining it with Slice 1 would hide the deletion decision.
- The final exact-commit acceptance receipt, cost comparison, and closeout are
  batch-level evidence rather than filler slices.

## Execution Ledger

| Slice | Status | Risk | Commit | Focused validation | Review | Notes |
|---|---|---|---|---|---|---|
| 1. Migrate acceptance execution to one exact-commit receipt | Pending | migration | — | — | — | Creates fast/acceptance boundary; does not run final live acceptance |
| 2. Remove or migrate obsolete preserving tests | Pending | destructive-cleanup | — | — | — | Requires refreshed dead-surface evidence and promotes full manifest to green |

## Slice 1: Migrate Acceptance Execution

### Scope

- Introduce one acceptance execution owner in
  `scripts/command_owner_scenarios.py` that launches all declared evidence nodes
  in one pytest process and produces the Acceptance Receipt Contract above.
- Make report rendering pure with respect to pytest. A report may consume only
  a fully validated current-commit receipt or remain explicitly unobserved/non-
  green.
- Register and apply a semantic `command_owner_acceptance` marker. Keep schema,
  mapping, pure comparison, serialization, and negative-shape behavior in the
  fast gate; keep runtime evidence, disposable Git/install behavior,
  negative-runtime outcomes, and end-to-end observed reporting in acceptance.
- Evaluate the catalog once per immutable acceptance input. Narrow evidence-node
  tests to their declared scenario subsets where they currently rebuild all 69
  scenarios.
- Replace four live observed-report CLI executions in determinism testing with
  one acceptance execution plus repeated pure formatting of one immutable
  validated report.
- Update catalog evidence-source hashes only where the changed evidence tests
  require it.

### Allowed Files

- `scripts/command_owner_scenarios.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_currentness.py`
- `tests/test_command_owner_scenario_cutover.py`
- `pyproject.toml`

### Non-Goals

- Do not change scenario semantics, accepted keys/aliases/contracts/families,
  adapters, production skills, manifests, installed features, or cutover state.
- Do not use a public raw outcome mapping, a caller-supplied green flag, or a
  receipt that is valid across candidate movement or input changes.
- Do not launch the full live acceptance gate from the worker or reviewer.

### Acceptance Criteria

- All declared aggregate evidence nodes execute in one pytest process for one
  acceptance run.
- The receipt binds the exact candidate commit, environment provenance, input
  digests, exclusive results, duration, process/evaluation evidence, and
  accepted aggregate evidence.
- Stale or foreign receipts and every non-pass/zero/deselection condition fail
  closed.
- Report formatting launches no pytest and cannot self-certify from raw caller
  outcomes.
- Fast and acceptance selections are semantic, complete, disjoint, and
  documented by tests.
- Repeated JSON/text determinism checks reuse one immutable report object or
  validated receipt.
- Focused receipt/partition tests, fast gate, catalog validation, Ruff,
  BasedPyright, and candidate `git diff --check` pass.

### Validation And Review

- Promote and run the focused receipt/partition tests and fast gate.
- Run catalog validation, Ruff, BasedPyright, and candidate range whitespace.
- Do not run the final live acceptance command in this slice.
- Test-quality review: `delta-only`, with special attention to anti-self-
  certification, marker completeness, failure-path coverage, and fixture cost.
- Independent review must use the exact task-scoped worktree diff before commit
  and echo its `diff_basis`.

### Worker Brief

The spawned `runway_worker` is already the required coding subagent. Read this
runway from
`/home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-33-acceptance-execution-simplification/runway.md`,
implement only Slice 1 in the candidate checkout, and do not spawn, delegate to,
or wait on any additional subagent. Do not run the final live acceptance gate,
install anything, switch generations, or edit stable planning files. Return the
required v2 compact result with exact changed paths and verified strict context.

### Reviewer Brief

The separate `runway_reviewer` reads this runway and reviews the coordinator-
provided exact worktree diff basis. Verify the Acceptance Receipt Contract,
single-pytest ownership, anti-self-certification, semantic gate partition,
unchanged COR-006 meanings, allowlist, and absence of production/cutover drift.
Echo `diff_basis` and verified strict context in the v2 compact result.

### Commit

`refactor: simplify command-owner acceptance execution`

### Slice Stop Conditions

- Stop if one acceptance run still launches evidence nodes in separate pytest
  processes or report formatting launches pytest.
- Stop if caching/receipt reuse can cross commit, catalog, adapter, test-source,
  interpreter, or environment movement.
- Stop if the fast gate omits behavior without assigning it to acceptance, or
  acceptance is defined by arbitrary count instead of runtime semantics.
- Stop if a COR-006 behavior, negative-runtime rejection, provenance check, or
  topology-independent boundary weakens.

## Slice 2: Remove Or Migrate Obsolete Preserving Tests

### Scope

- Re-run the focused dead-surface classification from the dispatch against the
  committed Slice 1 state.
- For each of the three known-red manifest tests, map every semantic obligation
  to a named green scenario/contract/focused test, migrate any missing behavior
  first, then remove exact prose, manifest dependency, and runtime-owner
  topology preservation.
- Delete the old test functions when their behavior is already protected;
  otherwise retain only the smallest behavior-level assertion with no exact
  prose/topology coupling.
- Promote the full manifest command from `known-red-baseline` to
  `required-green` with no restoration of removed code or old dependency shape.
- Add a compact candidate `CHANGELOG.md` entry covering the acceptance-runner
  simplification and removal/migration of preserving tests.

### Allowed Files

- `tests/test_codex_features_manifest.py`
- `CHANGELOG.md`
- The four focused scenario tests and catalog only when a named missing
  behavioral obligation must be migrated before deletion.

`scripts/command_owner_scenarios.py` and `pyproject.toml` are read-only unless
review finds a Slice 1 defect. Any such defect enters recovery and receives a
new worker/review/commit cycle before final acceptance.

### Non-Goals

- Do not change production skills, workflow docs, manifest dependencies, old
  runtime owners, installed features, or bridge code to make preserving tests
  pass.
- Do not delete scenario adapters/fixtures assigned to CCFG-24 through CCFG-29.
- Do not weaken behavior coverage merely to make the manifest suite green.

### Acceptance Criteria

- Every deleted assertion has `delete-now` or `migrate-tests-first` evidence and
  a named green behavioral replacement.
- No exact phrase, Markdown line break, manifest dependency list, support-owner
  presence, import path, alias, or historical topology acts as behavioral
  acceptance unless a named external contract requires it.
- The full manifest suite passes; the former exact three-test known-red baseline
  is gone because tests were migrated/deleted, not because old code was
  restored.
- The fast gate, catalog validation, Ruff, and candidate range whitespace pass.
- Test-quality and independent reviews are clean.

### Validation And Review

- Run the full manifest suite and promote it to `required-green`.
- Run the fast gate, catalog validation, Ruff, and candidate range whitespace.
- Do not run the final live acceptance command in this slice.
- Test-quality review: `delta-only`, focused on lost behavioral protection,
  assertion strength, and topology/prose coupling.
- Independent review must use the exact task-scoped worktree diff before commit,
  verify every dead-surface mapping, and echo its `diff_basis`.

### Worker Brief

The spawned `runway_worker` is already the required coding subagent. Read this
runway, implement only Slice 2 in the candidate checkout, and do not spawn,
delegate to, or wait on another subagent. Consume the coordinator's refreshed
dead-surface evidence. Do not restore production code/topology, run final live
acceptance, install anything, or edit stable planning files. Return the required
v2 compact result with exact changed paths and verified strict context.

### Reviewer Brief

The separate `runway_reviewer` reviews the exact task-scoped worktree diff.
Verify the canonical dead-surface status and named behavioral replacement for
every deleted assertion, full-manifest promotion without restoration, unchanged
CCFG-23 semantics, allowlist, and no CCFG-24+ drift. Echo `diff_basis` and
verified strict context in the v2 compact result.

### Commit

`test: remove obsolete command-owner topology assertions`

### Slice Stop Conditions

- Stop if any proposed deletion is `keep`, `keep-thin-entrypoint`, or
  `human-contract-decision`, or lacks a named behavioral replacement.
- Stop if manifest green requires changing production skills, docs, dependencies,
  owner topology, installed links, aliases, or historical compatibility.
- Stop if cleanup weakens a scenario, contract, key, alias, negative-runtime
  case, or provenance check.

## Final Validation

Final validation occurs only after both slice commits exist and the candidate
worktree is clean.

1. Confirm Planning State still identifies this batch and strict preflight is
   `ready`; capture the exact stable and candidate revisions.
2. Run the fast gate, full manifest, catalog validation, Ruff, BasedPyright, and
   candidate range `git diff --check`.
3. Run the exact-commit `accept` command once. Reuse an already green receipt
   only when its commit, environment, and every input digest exactly match.
4. Validate the receipt and run JSON/text report formatting against it. Prove
   these formatting commands launch no pytest.
5. Confirm all 69 scenarios, 31 contracts, 17 families, six keys, six aliases,
   negative-runtime outcomes, and provenance checks remain green.
6. Record the final duration, evidence-pytest process count, catalog-evaluation
   count, available child-process counts, receipt digest, command, environment,
   and candidate commit.
7. Compare final evidence with the 814.32-second, 13-pytest-per-report,
   35-catalog-evaluation, approximately 41,125-process baseline by cause and
   ratio. Explain any regression or missing measurement; do not invent data or
   impose an arbitrary timeout.
8. Run final exact-range `delta-only` test-quality review and independent
   runway review over
   `e8d07a785581e26ffb202b13ae43a0a83173205b..<final-candidate-commit>`.
9. Verify stable and candidate worktrees are clean and all committed paths are
   inside the validated scope.
10. Write `completed-slices.md` and `closeout.md`, then reconcile CCFG-33 only:
    mark it Closed, clear selected/queued/active state, record the exact
    candidate range and receipt evidence, and select no successor.

## Batch Stop Conditions

- Stop if Planning State identifies a different selected/queued/active scope or
  currentness is blocked.
- Stop if strict context or intended write scope fails validation before any
  worker/reviewer handoff.
- Stop on unexpected repository movement, dirty-file conflict, or changed path
  outside the slice allowlist.
- Stop if final acceptance is not bound to a clean exact candidate commit.
- Stop if reporter formatting launches pytest, more than one evidence-pytest
  process is needed for one acceptance run, or raw outcomes can self-certify.
- Stop if COR-006 behavior, evidence identity, negative-runtime rejection,
  provenance, or topology independence weakens.
- Stop if a preserving test causes restoration of old production code, owner
  topology, dependencies, aliases, paths, or prose.
- Stop if cost evidence is missing, guessed, or compared by an arbitrary
  threshold rather than cause and ratio.
- Stop if execution touches production command-owner transfer, real cutover,
  installed homes, the temporary bridge, or CCFG-24 through CCFG-29 scope.
- Stop closeout before selecting, dispatching, refreshing, or preparing any
  successor batch.
