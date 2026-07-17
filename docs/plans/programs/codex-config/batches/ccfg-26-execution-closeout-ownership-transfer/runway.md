# CCFG-26 Execution And Closeout Ownership Transfer Runway

Status: `queued`

## Purpose

Transfer the complete execution and same-batch closeout flight to `work-batch`,
remove displaced Batch Runway and Architecture Program Runway semantic ownership
in the same work, preserve only classified no-owner compatibility/mechanical
shells, and prove the final candidate through isolated installation and exact
COR-009 acceptance.

This runway implements exactly CCFG-26. It does not select, prepare, or implement
CCFG-27 through CCFG-29.

## Source Contract

- Selected dispatch: `dispatch.md`.
- Canonical ledger: `../../LEDGER.md`, CCFG-26 only.
- Accepted COR-009 snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Live execution boundary:
  `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- Accepted prior closeout:
  `../ccfg-25-planning-ownership-transfer/closeout.md`.
- Command-owner domain and ADR:
  `../../../../../../CONTEXT.md` and
  `../../../../../adr/0002-human-facing-command-owner-skills.md`.

These compact sources are the normal execution read path. Reopen broad design
history or older runways only for a named contradiction.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1, Make `work-batch` the complete owner: `migration`.
- Slice 2, Remove displaced execution and closeout ownership:
  `contract-narrowing`.
- Slice 3, Converge installation and exact acceptance: `migration`.

Slice 2 approval is the explicit same-work removal in CCFG-26, COR-009, and the
live carry-forward amendment. It permits removal of semantic execution and
closeout ownership only. It does not permit physical deletion of Batch Runway or
Architecture Program Runway, changes to the four serialized runner phase
identities, bridge deletion, or any new protocol or compatibility layer.

`slice_shape`: three slices.

`1 -> 2`: Slice 1 creates an independently exercisable complete replacement
owner, copied surviving contracts, focused behavioral proof, and a rollback
point before any old owner is narrowed.

`2 -> 3`: Slice 2 establishes the final semantic topology and caller wiring.
Slice 3 is a distinct environment, exact-commit acceptance, and final review
boundary.

No extra documentation, test, manifest, or closeout slice is justified. Those
surfaces travel with the behavior and installation boundary they support.

## Current Baseline And Assumptions

- Stable toolchain and canonical planning repository:
  `/home/alacasse/projects/codex-config` at
  `92c9952d047a2dfda5edfb91ec77bcabd058c99a`.
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`.
- Candidate implementation repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign` at clean commit
  `89671eceb9103039e7e6660e73837827c167a3a1`.
- Candidate branch: `implementation/command-owner-redesign`.
- Stable Codex home: `/home/alacasse/.codex`.
- Fixed isolated candidate Codex home:
  `/home/alacasse/.codex-command-owner-redesign`.
- Planning State `current` and `validate` passed before selection with no
  selected dispatch, queued batch, active runway, blocker, or obligation.
- Program `CURRENT.md` SHA-256 before planning:
  `26bf13bcfd2f37b226eb6a920a79b39892b4ac93d9a203def24b8a887654d86e`.
- Program `LEDGER.md` SHA-256 before planning:
  `c3f292905cd77587d6ae1c29658166cf605cb776000cc14fe5a09ec70ccfe2b6`.
- CCFG-25 closed COR-008 at candidate `89671ec`, left stable installation
  unchanged, and selected no successor.
- `work-batch` is currently a human-facing router. Batch Runway still owns
  execution/recovery/finalization semantics and Architecture Program Runway
  still owns closeout/reconciliation semantics.
- Candidate feature metadata currently makes `work-batch` depend on both broad
  runtime owners; registered worker/reviewer fallback paths still name Batch
  Runway references.
- The runner phase contract currently routes `execute` to Batch Runway and
  `closeout` to Architecture Program Runway.
- One declared CCFG-26 manifest assertion and one focused lifecycle-guard prose
  assertion are red at the exact candidate baseline. Both are owned by this
  runway and classified below.
- Existing tests and contracts are evidence, not authority for preserving
  displaced topology.

## Whole-Batch Non-Goals

- No CCFG-27 cutover rehearsal or public runner-protocol migration/removal
  decision.
- No CCFG-28 physical legacy-source deletion or default-generation switch.
- No CCFG-29 candidate integration, stable-home rebind, or bridge deletion.
- No change to the serialized identities or transition graph for
  `select-dispatch`, `create-spec`, `execute`, and `closeout`.
- No new command, script, helper, schema, store, transaction, lifecycle state,
  persistent execution store, compatibility layer, or alternate runner protocol.
- No Planning State, planning schema, DEC-038, intake, selection, projection, or
  `ledger-store/v1` semantic change.
- No candidate write to canonical planning state during implementation.
- No stable-home installation and no candidate merge.

## Planning Snapshot

This is the immutable plan-time `cross-checkout-context/v1` planning snapshot.
It is historical planning evidence, not a live execution lease. Do not rewrite
it when the containing planning commit or later repositories advance. Before the
first delegated execution handoff, `work-batch` must confirm this exact runway
and selected scope through Planning State, pass the ready/blocked preflight, and
acquire a fresh live lease. Every later worker and reviewer handoff requires a
new refreshed live lease and separately validated write scope.

Installed helper:

```text
/home/alacasse/.codex/scripts/cross_checkout_context.py
```

Resolved helper:

```text
/home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
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
  toolchain_commit: 92c9952d047a2dfda5edfb91ec77bcabd058c99a
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 92c9952d047a2dfda5edfb91ec77bcabd058c99a
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 89671eceb9103039e7e6660e73837827c167a3a1
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Plan-time validation receipt:

```yaml
interface: cross-checkout-receipt/v1
caller: plan-batch
reason: CCFG-26 selection and queue transition
strict_parse: passed
generation_role: stable
canonical_state_mutation_allowed: true
canonical_planning_root: /home/alacasse/projects/codex-config/docs/plans
repository_revisions:
  toolchain_commit: 92c9952d047a2dfda5edfb91ec77bcabd058c99a
  canonical_planning_commit_before: 92c9952d047a2dfda5edfb91ec77bcabd058c99a
  implementation_commit_before: 89671eceb9103039e7e6660e73837827c167a3a1
planning_paths:
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-closeout-ownership-transfer/dispatch.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-closeout-ownership-transfer/runway.md
  - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-26-execution-closeout-ownership-transfer/review.md
implementation_paths:
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/work-batch
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/batch-runway
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/architecture-program-runway
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/runway_worker.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/agents/runway_reviewer.toml
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_phase_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner_command.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/docs/skill-routing-contract.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/docs/workflow-guide.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/README.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/codex-features.json
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codex_features_manifest.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_phase_contract.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_custom_agent_contracts.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_batch_lifecycle_guards.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_routing_rule_ownership.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_scenario_catalog.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_protocol.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner_run_loop.py
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/legacy-removal/SKILL.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/planning-artifacts/SKILL.md
  - /home/alacasse/projects/codex-config-command-owner-redesign/skills/test-quality-review/SKILL.md
deletion_condition: CCFG-29 final integration
```

The receipt validates an upper scope, not automatic authority to edit every
listed path. The conditional ceiling below remains binding.

## Project Values

- Planning Artifact Layout: Planning Artifact Layout v1.
- Planning location: this batch directory.
- Program root: `docs/plans/programs/codex-config`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`; use explicit temporary outputs under `/tmp`.
- Output root: `None`; use explicit temporary outputs under `/tmp`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Integration harness: `scripts/command_owner_scenarios.py accept` with explicit
  result, JSON report, and text report paths.
- Summary artifact: generated text report and result JSON from the exact
  acceptance invocation.
- Index refresh: none.
- Candidate commit requirement: one focused candidate commit per clean slice.
- Canonical planning receipts and final same-batch closeout are separate stable
  commits; self-referential final closeout fields use `this closeout commit`.
- Candidate and stable worktrees were clean at planning time. Preserve unrelated
  dirt and stop on task-scope overlap.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2; registered agent TOMLs own
their exact result schemas.
Use Batch Runway Compact Report Contract v1 for coordinator receipts and its
non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordination or
subagent-lifecycle behavior only.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.
Use the strict cross-checkout context v1 consumer contract for every handoff.

Reference files in the controlling stable toolchain:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/execute-recovery-v1.md`
- `skills/batch-runway/references/finalize-batch-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`

Overrides:

- Execution occurs only in the candidate repository. Canonical planning writes
  remain coordinator-owned in the stable repository.
- The first fresh lease must prove candidate baseline `89671ec`. Later leases
  accept movement only when it is the exact coordinator-accepted action.
- `work-batch` owns the complete flight and must not delegate semantic
  execution/closeout decisions to Batch Runway or APR merely because the stable
  orchestration contract references still use those historical file paths.
- The runner's compatibility `execute` phase invokes the complete `work-batch`
  flight. The compatibility `closeout` phase may observe and validate the exact
  completed receipt only; it cannot make another closeout or reconciliation
  decision.
- After each test-changing slice, run delta-only `test-quality-review`.
- After Slice 2 and final validation, run `dead-surface-audit` for retained
  shells. Trigger import-topology review when role/reference/runner imports or
  installed path topology changes.

## Validation Profile And Status Classes

Selected profile: `project-harness-production`.

Every command below uses exactly one status class.

### Planning Baselines

1. Declared CCFG-26 ownership assertion:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
     tests/test_codex_features_manifest.py::CodexFeaturesManifestTests::test_work_batch_reconciles_same_batch_closeout
   ```

   Status: `known-red-baseline`. It currently fails because the old
   `work-batch` command does not state the complete successor-ownership boundary.
   Slice 1 owns the target-behavior rewrite/remediation and must promote this
   exact test to `required-green` with green evidence before its review.

2. Focused APR lifecycle guard:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
     tests/test_batch_lifecycle_guards.py::BatchLifecycleGuardTests::test_architecture_program_closeout_rejects_dispatch_runway_only_evidence
   ```

   Status: `known-red-baseline`. It is a brittle exact-prose assertion over the
   current APR closeout owner. Slice 2 owns replacement with target structural or
   behavioral proof and must promote the resulting test to `required-green`.

3. New complete `work-batch` owner tests and any old-format active-state fixture:

   Status: `implementation-created` by Slice 1, then `required-green` before
   Slice 1 review.

4. The CCFG-25 broad deletion/projection diagnostic:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
     tests/test_planning_state_consumer_projection_routing.py \
     tests/test_deletion_test_vocabulary_ownership.py
   ```

   Status: `known-red-baseline`. Only the six preclassified CCFG-28/deletion-
   vocabulary failures may remain. Any additional failure blocks.

5. Bare configured-project BasedPyright:

   ```sh
   .venv/bin/basedpyright
   ```

   Status: `known-red-baseline`: 311 errors and 16 warnings at candidate
   `89671ec`. It is diagnostic only for non-regression. Slice-specific exact
   changed-file type checks are separate `required-green` commands.

### Required And Conditional Gates

- Focused pytest for every touched behavior: `required-green` after each owning
  slice.
- Scenario catalog validation and focused target-behavior cases:
  `required-green` after each owning slice.
- Quick structural validation of every changed skill: `required-green`.
- Ruff for changed Python files: `conditional`; run when a slice changes Python.
- Configured-project BasedPyright for changed Python files: `conditional`; run
  when a slice changes typed Python.
- Exact runner protocol/run-loop tests: `conditional`; run when the focused
  proof activates a runner command/facade path.
- Candidate installation: `conditional` for Slice 1 if installed wiring changes,
  and `required-green` for Slice 3.
- `git diff --check`: `required-green` after every slice and at final validation.
- Project exact-commit acceptance: `required-green` in Slice 3 and final
  validation.
- Stable-home before/after comparison: `required-green` in Slice 3.

Do not promote a known-red or implementation-created command without explicit
green evidence. Do not let unchanged known-red diagnostics gate execution.

## Implementation Write-Path Ceiling

Required candidate paths:

- `skills/work-batch/**`
- `skills/batch-runway/**`
- `skills/architecture-program-runway/**`
- `agents/runway_worker.toml`
- `agents/runway_reviewer.toml`
- `scripts/architecture_program_runner_phase_contract.py`
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `README.md`
- `codex-features.json`
- `CHANGELOG.md`
- `tests/test_codex_features_manifest.py`
- `tests/test_architecture_program_runner_phase_contract.py`
- `tests/test_custom_agent_contracts.py`
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/fixtures/command-owner-scenarios/**`
- `tests/test_command_owner_scenario_catalog.py`

Conditional candidate paths, activated only by a focused failing test or direct
caller proof recorded in the execution ledger before the edit:

- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner.py`
- `tests/test_architecture_program_runner_protocol.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `skills/legacy-removal/SKILL.md`
- `skills/planning-artifacts/SKILL.md`
- `skills/test-quality-review/SKILL.md`

No other candidate path is authorized. The canonical planning paths in the
planning snapshot remain coordinator-only.

## Execution Ledger

| Slice | Status | Commit | Review | Notes |
|---|---|---|---|---|
| 1. Make `work-batch` the complete owner | Pending | None | Pending | Establish replacement owner and focused behavior before narrowing old owners. |
| 2. Remove displaced execution and closeout ownership | Pending | None | Pending | Source-authorized contract narrowing; preserve classified shells and phase identities. |
| 3. Converge installation and exact acceptance | Pending | None | Pending | Final candidate topology, exact acceptance, and reviews. |

Move completed rows to `completed-slices.md` after each clean focused candidate
commit. The active ledger keeps only pending or active work.

## Slice 1 — Make `work-batch` The Complete Owner

### Scope

- Expand `skills/work-batch/**` from a router into the complete human-facing
  execution and same-batch closeout owner.
- Copy the surviving execution, recovery, result, receipt, retention,
  validation, strict-context, finalization, and closeout contracts below the
  `work-batch` owner. Do not invent a neutral third owner or new protocol.
- Define one complete command flight:
  - Planning State `current` and `validate` decide semantic currentness;
  - first handoff proves the planning-snapshot scope and exact candidate
    implementation baseline;
  - every worker and reviewer receives a fresh strict live lease and validated
    scope;
  - accepted coordinator actions are the only permitted repository movement;
  - reviewers receive and echo exact diff bases;
  - `work-batch` owns proceed/stop, recovery, validation/review acceptance,
    commits, receipts, execution ledger, finalization, closeout, reconciliation,
    and no-successor stop.
- Add target behavioral proof, including old-format active-state policy,
  queued-runway protection, partial execution and closeout recovery, exact
  replay, ordinary target-policy/dirty-scope handling, and rejection of Git
  lifecycle inference.
- Rewrite the declared manifest assertion as target behavior and promote it
  from its known-red baseline.

### Allowed Files

- `skills/work-batch/**`
- `tests/test_codex_features_manifest.py`
- `tests/test_custom_agent_contracts.py`
- `tests/test_batch_lifecycle_guards.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/fixtures/command-owner-scenarios/**`
- `tests/test_command_owner_scenario_catalog.py`

Batch Runway, APR, runner, role, documentation, feature, and lock surfaces are
read-only in this slice. They remain the rollback baseline until Slice 2.

### Non-Goals

- No removal or narrowing of an old owner.
- No runner, agent TOML, feature manifest, or installed-route rebind.
- No new script, helper, schema, store, transaction, lifecycle state, or
  compatibility layer.
- No physical legacy deletion, bridge change, phase identity change, switch,
  merge, canonical write, or successor selection.

### Acceptance Criteria

- One `work-batch` invocation visibly owns every COR-009 execution and closeout
  decision and stops after same-batch reconciliation.
- Planning State is the only semantic currentness gate; Git and dirty files are
  constrained to material integrity and ordinary scope-conflict evidence.
- First and later handoff rules, exact movement, fresh leases, exact reviewer
  bases, v2 result identity, worker/reviewer separation, commit/receipt
  integrity, recovery, finalization, and no-successor behavior are explicit and
  mechanically covered.
- Surviving contract files exist below `skills/work-batch/**` and do not add a
  third owner or protocol.
- The old-format active-state fixture/test is created and green.
- The declared CCFG-26 manifest test is rewritten around target behavior and
  green; it does not preserve the old delegated owner chain.
- No Slice 2 file changed.

### Focused Validation

Run focused tests for changed owner, contract, agent-contract, lifecycle, and
scenario behavior, then the catalog validator, quick skill validation, and
`git diff --check`. Every command is `required-green` after the named
implementation-created tests exist. Run delta-only `test-quality-review` for
the changed tests before review.

### Commit

`refactor(work-batch): own execution and closeout flight`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 1. Revalidate the fresh strict context, implement only Slice 1 in the
candidate repository, and return the exact v2 result. Do not spawn, delegate to,
or wait on additional agents. Do not edit any Slice 2 surface. Do not run the
project-wide acceptance harness or installation unless the coordinator
explicitly assigns a focused check.

### Reviewer Brief

Independently review the exact task-scoped worktree diff or candidate commit
provided by the coordinator. Echo `diff_basis` and verified strict identity.
Verify complete owner semantics, behavioral proof, status-class promotion,
scope, and absence of old-owner narrowing. Do not edit files or spawn agents.

### Slice Stop Conditions

- Stop if complete ownership needs a new helper, script, protocol, schema,
  store, transaction, lifecycle state, or compatibility layer.
- Stop if the replacement owner cannot be established without narrowing an old
  owner in this slice.
- Stop on missing old-format, currentness, lease, result, recovery, commit,
  receipt, finalization, reconciliation, or no-successor proof.
- Stop on a change outside the Slice 1 allowed files.

## Slice 2 — Remove Displaced Execution And Closeout Ownership

### Approval Gate

Proceed only under the source authorization recorded in `dispatch.md`: remove
Batch Runway and APR semantic execution/closeout ownership while preserving
classified no-owner compatibility or mechanical shells until CCFG-28. Any
broader narrowing, physical deletion, phase migration, or bridge change is not
approved and blocks.

### Scope

- Remove Batch Runway `execute-spec`, recovery, validation acceptance, review,
  commit, receipt, execution-ledger, and finalization decision ownership.
- Remove Architecture Program Runway closeout disposition, lifecycle decision,
  and same-batch reconciliation ownership.
- Leave only exact, classified compatibility observations or apply-only
  mechanics with named callers, reason, no semantic authority, and CCFG-28
  deletion condition. Retained shells must not be normal human commands or
  broad dependencies.
- Rebind `runway_worker` and `runway_reviewer` contracts away from Batch Runway
  paths without changing their role separation or v2 result behavior.
- Rebind `scripts/architecture_program_runner_phase_contract.py` so the
  compatibility `execute` phase invokes one complete `work-batch` flight and
  the compatibility `closeout` phase observes/validates the exact completed
  receipt only. Preserve all four serialized phase identities, receipts, and
  transitions.
- Rebind routing, workflow, README, feature, and changelog surfaces to the
  final ownership topology. Remove broad `work-batch` dependencies on Batch
  Runway and APR.
- Replace the brittle APR lifecycle-guard wording assertion with structural or
  behavioral target proof and promote it to required green.
- Use conditional paths only after recording the exact focused proof.

### Allowed Files

- All required candidate paths in the Implementation Write-Path Ceiling.
- A conditional path only after its focused activation evidence is recorded.

### Non-Goals

- No physical deletion of Batch Runway or APR source directories.
- No phase identity, transition graph, runner public-protocol, bridge, helper,
  default generation, or canonical planning change.
- No new wrapper, compatibility layer, neutral execution-owner skill, script,
  store, or lifecycle state.
- No unrelated support-skill semantic change.

### Acceptance Criteria

- `work-batch` is the only execution and same-batch closeout semantic owner.
- Batch Runway and APR make no proceed/stop, delegation, recovery, acceptance,
  review, commit, receipt, finalization, closeout, reconciliation, or successor
  decision.
- Worker/reviewer contracts no longer depend on Batch Runway paths.
- Retained shells have exact callers, reason, owner, and CCFG-28 removal
  condition; dead-surface review finds no unclassified preservation.
- The runner uses one complete `work-batch` flight while all serialized phase
  identities and transitions remain byte-for-byte compatible at the protocol
  level.
- `work-batch` feature metadata has no broad APR or Batch Runway dependency; all
  installed links resolve to the intended candidate source.
- Both known-red CCFG-26 focused assertions are now green target-behavior tests.
- Conditional paths are either untouched or have recorded direct proof.
- No successor is selected or prepared.

### Focused Validation

Run the complete focused ownership, manifest, routing, agent, lifecycle, runner
phase-contract, and scenario set; structural skill validations; Ruff and exact
changed-file BasedPyright when Python changes; `git diff --check`; delta-only
test-quality review; dead-surface review; and import-topology review when role,
reference, runner, or installed path topology changes. All focused acceptance
commands are `required-green` after the owned baseline promotions.

### Commit

`refactor(work-batch): remove displaced execution owners`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 2. Revalidate the fresh strict context and source approval, implement
only the authorized contract narrowing, preserve the four phase identities and
classified shells, and return the exact v2 result. Do not spawn, delegate to, or
wait on additional agents. Do not run final installation or project acceptance.

### Reviewer Brief

Independently review the exact diff basis and echo it with verified strict
identity. Verify sole `work-batch` ownership, no broad owner dependency,
source-limited narrowing, retained-shell classification, phase compatibility,
known-red promotion, conditional-path evidence, and no premature deletion,
switch, merge, or successor action. Do not edit files or spawn agents.

### Slice Stop Conditions

- Stop if any semantic execution or closeout owner remains outside `work-batch`.
- Stop if removing ownership requires physical directory deletion, a phase
  migration, bridge change, or a new compatibility layer.
- Stop if a retained shell makes a semantic decision or lacks caller, reason,
  owner, and removal condition.
- Stop if a conditional path is needed without exact direct proof.
- Stop on stable-home mutation, canonical candidate write, or a change outside
  the validated upper scope.

## Slice 3 — Converge Installation And Exact Acceptance

### Scope

- Align final skill metadata, agent metadata, manifest, routing,
  documentation, README, and changelog around the accepted Slice 2 topology.
- Run a real all-feature install into a fresh empty temporary Codex home and
  converge the fixed isolated candidate home.
- Prove both candidate installations have the same managed feature versions and
  links, all links resolve to candidate source, and post-install dry runs are
  clean.
- Prove the stable home is byte-identical before and after candidate installs.
- Run complete focused and broader practical validation, exact-commit acceptance
  with one evidence pytest process and explicit outputs, and all triggered final
  exact-range reviews.
- Repair only in-ceiling convergence defects. Any new semantic behavior or
  scope expansion requires recovery and fresh review.

### Allowed Files

- Required candidate paths already changed by Slices 1 and 2.
- No conditional path may be newly activated solely for convergence.

### Non-Goals

- No new owner behavior, compatibility topology, protocol, phase identity,
  bridge, generation switch, stable install, merge, canonical write, physical
  legacy deletion, or successor work.

### Acceptance Criteria

- Full focused tests, manifest, catalog, routing, role, lifecycle, runner,
  strict-context, installer, Ruff, exact changed-file BasedPyright, and
  whitespace gates are green, except the explicitly retained broad known-red
  diagnostics with no new failure.
- Fresh and fixed candidate installations converge and are dry-run clean.
- Stable-home status and link fingerprints are unchanged.
- Exact acceptance binds the final clean candidate commit and reports all
  required contracts, scenarios, evidence keys, aliases, and COR-009 behavior
  through one evidence pytest process.
- Final exact-range implementation review, import-topology review,
  dead-surface audit, and delta-only test-quality review are clean.
- No broad owner dependency, candidate canonical write, default-generation
  switch, merge, or successor selection exists.

### Candidate Installation Commands

```sh
ccfg26_fresh_home="$(mktemp -d /tmp/ccfg-26-codex-home.XXXXXX)"
ccfg26_stable_before="$(mktemp /tmp/ccfg-26-stable-before.XXXXXX)"
ccfg26_stable_after="$(mktemp /tmp/ccfg-26-stable-after.XXXXXX)"

./install.sh --codex-home /home/alacasse/.codex --status >"$ccfg26_stable_before"
./install.sh --codex-home "$ccfg26_fresh_home" --all
./install.sh --codex-home "$ccfg26_fresh_home" --status
./install.sh --codex-home "$ccfg26_fresh_home" --all --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --all
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --all --dry-run
./install.sh --codex-home /home/alacasse/.codex --status >"$ccfg26_stable_after"
cmp "$ccfg26_stable_before" "$ccfg26_stable_after"
```

Status: `required-green`. Real writes are limited to the fresh temporary home and
fixed isolated candidate home. The stable home command is status-only.

### Exact-Commit Acceptance Commands

Run from a clean final candidate commit:

```sh
ccfg26_acceptance_root="$(mktemp -d /tmp/ccfg-26-acceptance.XXXXXX)"
COMMAND_OWNER_CANDIDATE_CODEX_HOME=/home/alacasse/.codex-command-owner-redesign \
PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python scripts/command_owner_scenarios.py accept \
  tests/fixtures/command-owner-scenarios \
  --result-output "$ccfg26_acceptance_root/acceptance-result.json" \
  --json-report-output "$ccfg26_acceptance_root/report.json" \
  --text-report-output "$ccfg26_acceptance_root/report.txt"

python -m json.tool "$ccfg26_acceptance_root/acceptance-result.json" >/dev/null
python -m json.tool "$ccfg26_acceptance_root/report.json" >/dev/null
test -s "$ccfg26_acceptance_root/report.txt"
cat "$ccfg26_acceptance_root/report.txt"
sha256sum \
  "$ccfg26_acceptance_root/acceptance-result.json" \
  "$ccfg26_acceptance_root/report.json"
```

Status: `required-green`. The coordinator must read the text report and record
the output paths, file hashes, canonical report hash, evidence-process count,
exact candidate commit, and reported counts in closeout.

### Commit

`chore(work-batch): converge COR-009 acceptance`

### Worker Brief

You are the registered `runway_worker` and already the required coding subagent
for Slice 3. Revalidate the fresh strict context, perform only in-ceiling
convergence edits assigned by the coordinator, and return the exact v2 result.
Do not spawn, delegate to, or wait on additional agents. Do not switch the
default generation, install to stable, merge, write canonical planning state,
delete the bridge or legacy directories, or select successor work.

### Reviewer Brief

Independently review the exact final candidate range and echo the coordinator's
`diff_basis` and strict identity. Verify COR-009 ownership, installation,
acceptance, stable-home comparison, retained-shell classification, known-red
non-regression, no broad owner dependency, and all deferred boundaries. Do not
edit files or spawn agents.

### Slice Stop Conditions

- Stop on any candidate/stable identity mismatch or unexpected movement.
- Stop if installation would write to the stable home.
- Stop if acceptance is not bound to one clean exact candidate commit or starts
  more than one evidence pytest process.
- Stop on a new failure, unclassified known-red change, review finding, scope
  expansion, bridge/phase change, switch, merge, canonical write, or successor
  action.

## Final Validation

From the clean final candidate commit:

1. Run focused pytest for all changed owner, role, routing, manifest, lifecycle,
   runner, strict-context, installer, and scenario surfaces.
2. Run broader practical candidate tests named by the final changed path set.
3. Validate the scenario catalog and every changed skill structurally.
4. Run Ruff and exact configured-project BasedPyright over changed Python.
5. Run `git diff --check 89671eceb9103039e7e6660e73837827c167a3a1`.
6. Reproduce the retained broad known-red diagnostics and reject any new or
   changed failure.
7. Converge fresh and fixed candidate installations and compare stable-home
   status before/after.
8. Run the exact-commit acceptance command once and read its summary.
9. Run final exact-range implementation review and triggered import-topology,
   dead-surface, and delta-only test-quality reviews.

All required-green gates must pass. Known-red baselines remain diagnostic only
and must not regress.

## Batch Stop Conditions

- Stop if Planning State no longer names this exact queued or active runway.
- Stop if strict preflight is blocked, the selected scope differs, or the first
  candidate baseline is not `89671ec`.
- Stop on unexplained repository movement or movement during lease preparation.
- Stop if Git, ancestry, fingerprints, path sets, or dirty files are treated as
  lifecycle or queue authority.
- Stop on a new command, helper, script, schema, store, transaction, lifecycle
  state, persistent execution store, compatibility layer, or runner protocol.
- Stop if `work-batch` delegates any semantic execution or closeout decision to
  Batch Runway or APR after Slice 2.
- Stop if a retained shell is an active owner, normal route, or unclassified
  compatibility surface.
- Stop if any serialized phase identity or transition changes before CCFG-27,
  if legacy directories are deleted before CCFG-28, or if the bridge is changed
  or deleted before CCFG-29.
- Stop on stable-home mutation, candidate canonical write, default-generation
  switch, merge, physical legacy cleanup, or successor selection.
- Stop on an edit outside the required ceiling or an unproven conditional path.
- Stop on unresolved validation, review, dirty-file conflict, or scope drift.

## Closeout Contract

After all three candidate commits and final validation/reviews are clean:

1. write `completed-slices.md`, `closeout.md`, and any required execution report
   in this batch directory;
2. record the exact candidate range, stable planning receipts, live-lease and
   scope identities, worker/reviewer receipts, validation, known-red
   non-regression, installation paths, stable-home comparison, acceptance output
   hashes/counts, final reviews, retained-shell inventory, and cost evidence;
3. reconcile only CCFG-26 in program `CURRENT.md` and `LEDGER.md`;
4. mark CCFG-26 closed only from complete implementation, validation, review,
   receipt, finalization, and reconciliation evidence; and
5. clear selected/queued/active state and stop with CCFG-27 through CCFG-29 still
   open and unselected.

Closeout must not select, dispatch, queue, refresh, create, or prepare a
successor. Self-referential final stable closeout fields use
`this closeout commit`.
