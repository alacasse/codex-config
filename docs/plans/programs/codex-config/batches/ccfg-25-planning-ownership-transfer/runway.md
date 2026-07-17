# CCFG-25 Planning Ownership Transfer Runway

## Execution Status

- Planning transition: `completed; same-batch closeout reconciled`
- Artifact role: completed Batch Runway retained as execution evidence
- Selected dispatch: `dispatch.md`
- Queue currentness authority: Planning State `current` and `validate`
- Candidate Slice 3 static convergence commit:
  `89671eceb9103039e7e6660e73837827c167a3a1`
- Resolved blocker report: `slice-3-blocker-report.md`
- Closeout: `closeout.md`

All three slices are complete. Slice 3 final validation, fresh and isolated
installation, stable-home comparison, exact acceptance, and all exact-range
reviews are green at `89671eceb9103039e7e6660e73837827c167a3a1`. The bare
configured-project audit remains a non-regressing known-red baseline diagnostic.
CCFG-25 is closed, and no successor was selected or prepared.

## Purpose

Implement the complete candidate `plan-batch` command owner, including delegated
planning, independent planning review, proportionality and approval gates, and the
existing DEC-038 selection transaction. Migrate target planning behavior to the
installed owner, remove Architecture Program Runway planning ownership and Batch
Runway `create-spec` ownership, converge the isolated candidate installation, and
close CCFG-25 without beginning CCFG-26.

## Authority

- Finding: CCFG-25, controlled by the selected `dispatch.md`.
- Accepted source: COR-008 at
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Planning-quality amendment:
  `../../findings/ccfg-25-planning-quality-amendment.md`.
- Planning/execution carry-forward:
  `../../findings/command-owner-redesign-planning-execution-carry-forward.md`.
- Resolved artifact and selection transaction:
  `../ccfg-21-planning-artifact-contracts/closeout.md`.
- Target behavioral proof:
  `../ccfg-23-behavioral-scenario-harness/closeout.md`.
- Current retained-owner inventory:
  `../ccfg-24b-intake-ownership-cutover/closeout.md`.

Use these compact sources as the normal read path. Reopen broad design history,
old runways, or raw execution logs only for a named contradiction.

## Batch Kind And Slice Risk Contract

- Batch kind: `mixed-risk`.
- Slice 1, Implement the installed `plan-batch` owner: `migration`.
- Slice 2, Remove displaced planning ownership: `contract-narrowing`.
- Slice 3, Converge installation and final acceptance: `migration`.

`slice_shape`: three slices.

- `1 -> 2`: Slice 1 produces an independently exercisable installed replacement
  owner and a rollback point while legacy planning owners remain physically
  present. Slice 2 can then remove only the displaced planning routes against
  current caller and replacement evidence.
- `2 -> 3`: Slice 2 produces the final semantic owner topology. Slice 3 has a
  distinct clean-install, exact-commit acceptance, and range-wide review boundary.

A separate planner/reviewer scaffolding slice is forbidden. Those roles have no
supported standalone outcome and must land with the complete command owner.
Generic docs, metadata, tests, and closeout work remain with the behavior or final
environment they validate.

## Baseline

- Stable toolchain and canonical planning checkout:
  `/home/alacasse/projects/codex-config`, branch `master`.
- Stable planning baseline before initial dispatch:
  `31d228d4ef9b94e2ccad0f5260670593ea9469f9`.
- Candidate implementation checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`.
- Candidate implementation baseline:
  `91179e84c7cfed666be224575db7000ca0ea01b3`.
- Stable Codex home: `/home/alacasse/.codex`.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`.
- Accepted design snapshot:
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- `scripts/planning_contract.py`, the six planning schemas, and DEC-038 are the
  accepted mechanical planning store and transaction. They are read-only for
  semantic changes in this batch.
- CCFG-24B exact acceptance reported 69 scenarios, 31 contracts, 17 families, six
  evidence keys, and six aliases green.
- Candidate manifest baseline has three assigned failures:
  - `test_executable_work_source_boundary_is_explicit` — CCFG-25 Slice 1;
  - `test_plan_batch_command_owner_runtime_boundaries_are_explicit` — CCFG-25
    Slice 2;
  - `test_work_batch_reconciles_same_batch_closeout` — CCFG-26, deferred.

At execution startup, reproduce the exact candidate baseline, these three failure
identities, and the exact scenario acceptance baseline. Any new or reclassified
failure blocks instead of widening scope.

## Project Values

- Planning artifact layout: Planning Artifact Layout v1.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None` for durable state; final acceptance outputs use fresh
  `/tmp/ccfg-25-*` directories only.
- Output root: `None` for committed outputs.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway`.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus stable
  same-batch planning receipts after each candidate commit.
- Dirty-file policy: preserve unrelated files; candidate writes are limited to the
  active slice; stable writes are limited to this batch's planning artifacts and
  same-batch reconciliation.
- Test-quality review: `delta-only` for every test-changing slice and the final
  exact candidate range.

## Initial Plan Repair And Queue Gate

The initial runway could become queued only when one local `plan-batch` pass proved
all of the following in order:

1. resolve `/home/alacasse/.codex/scripts/cross_checkout_context.py` from the active
   stable Codex home and prove it resolves under the declared toolchain root;
2. parse and validate the complete payload in **Planning Snapshot** below,
   including the canonical planning root and exact intended planning and
   implementation write scopes;
3. invoke an independent planning reviewer against the selected `dispatch.md`, all
   authoritative sources and user constraints, current Planning State facts, the
   proportionality record, and the exact amended draft hash;
4. require `status: clean`, no unresolved user decision, and no unapproved residual
   complexity; and
5. apply DEC-038 to transition this exact selected scope to one queued runway.

This gate is retained as historical queue evidence. The live Slice 2 amendment
does not repeat DEC-038 or queue mutation. A current live execution preflight does
not replace this plan-time validation record.

## Planning Snapshot

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
  toolchain_commit: 4dfcc6418fca62b59e17ae4803e28a377b306f4e
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 4dfcc6418fca62b59e17ae4803e28a377b306f4e
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 91179e84c7cfed666be224575db7000ca0ea01b3
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

Plan-time validation:

```yaml
validation:
  helper_resolves_to: /home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
  strict_parse: passed
  canonical_planning_root: passed
  write_scope: passed
  receipt_interface: cross-checkout-receipt/v1
  caller: plan-batch
  reason: CCFG-25 Plan Repair Gate and queue transition
  repository_revisions:
    toolchain_commit: 4dfcc6418fca62b59e17ae4803e28a377b306f4e
    canonical_planning_commit_before: 4dfcc6418fca62b59e17ae4803e28a377b306f4e
    implementation_commit_before: 91179e84c7cfed666be224575db7000ca0ea01b3
  planning_paths:
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/CURRENT.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/LEDGER.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/dispatch.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/runway.md
    - /home/alacasse/projects/codex-config/docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/review.md
  implementation_paths:
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/plan-batch
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/plan_batch.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/agents/batch_planner.toml
    - /home/alacasse/projects/codex-config-command-owner-redesign/agents/batch_plan_reviewer.toml
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/architecture-program-runway
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills/batch-runway
    - /home/alacasse/projects/codex-config-command-owner-redesign/scripts/architecture_program_runner.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/codex-features.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/skills-lock.json
    - /home/alacasse/projects/codex-config-command-owner-redesign/docs/skill-routing-contract.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/docs/workflow-guide.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/README.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/CHANGELOG.md
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_plan_batch.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_architecture_program_runner.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_codex_features_manifest.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_routing_rule_ownership.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_catalog.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_skill_contract_migration.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_planning_state_consumer_projection_routing.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_deletion_test_vocabulary_ownership.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_behavioral_scenarios.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/test_command_owner_scenario_catalog.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/catalog.yaml
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/workflow-cases.yaml
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/command-owner-scenarios/workflow_adapters.py
    - /home/alacasse/projects/codex-config-command-owner-redesign/tests/fixtures/plan-batch
  deletion_condition: CCFG-29 final integration
```

This immutable planning snapshot is historical plan-time evidence, not a live
execution lease or a promise about later live `HEAD`. Do not rewrite it when the
containing planning change or later between-flight commits advance stable `HEAD`.

After valid queue mutation, `work-batch` must still run a fresh ready/blocked
preflight at execution startup and prepare a fresh live lease before every worker
and reviewer handoff. Every strict agent result must carry matching non-null
`verified_cross_checkout_context` evidence.

## Slice 2 Bounded Amendment

The user authorized one bounded amendment to the active CCFG-25 Slice 2 after the
owner/caller audit recorded in `execution-report.md`. The original ceiling allowed
the runner facade but omitted the sibling module that owns its planning phase
contract and four active support-skill planning handoffs. This amendment changes no
batch identity, slice shape, planning protocol, store, transaction, state version,
wrapper, command owner, or CCFG-26 responsibility.

The first amendment's additional candidate ceiling was exactly:

- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_state.py`
- `scripts/architecture_program_runner_validation.py`
- `scripts/architecture_program_runner_command.py`
- `skills/planning-artifacts/SKILL.md`
- `skills/legacy-removal/SKILL.md`
- `skills/port-by-contract/SKILL.md`
- `skills/dead-surface-audit/SKILL.md`
- existing focused tests directly covering those modules and skill-routing
  contracts

This was an upper path ceiling, not a mandatory edit list. The second bounded
amendment retains `architecture_program_runner_phase_contract.py` as the completed
semantic change but makes `state.py`, `validation.py`, and `command.py` read-only.
Stop if a focused failing test or direct invariant proves one would need an edit.
Do not introduce a new harness or generalized runner abstraction.

Preserve the serialized phase identities `select-dispatch`, `create-spec`,
`execute`, and `closeout`, their receipts, and the current transition graph.
`select-dispatch` and `create-spec` are temporary compatibility labels during
CCFG-25. One complete public `plan-batch` invocation owns selection, independent
planning review, and DEC-038. `create-spec` may only observe that completed result
and advance compatibility state; it must not invoke Batch Runway planning, create
another draft, repeat planning decisions, or act as a second planner.

CCFG-27 owns the migration or removal decision for those two serialized labels as
part of its accepted runner-public-protocol and old-mode-removal scope. If CCFG-27
retains them, final physical cleanup is required no later than CCFG-29.

The four support skills route planning handoffs to public `plan-batch` while
retaining their current evidence, layout, classification, and contract-distillation
responsibilities. They receive no queue, dispatch, runway, or lifecycle mutation
authority.

A new independent planning review must bind the exact amended dispatch and runway
hashes, this authorization, current Planning State facts, and the proportionality
record. After a clean review, resume Slice 2 under a freshly prepared strict lease
whose implementation revision is exactly
`5aa5add1251d1e4b3630a9678fdec244949cf691`. Stop if another live planning caller
or runner semantic owner exists outside this amended ceiling; do not widen it.

## Slice 2 Second Bounded Amendment

The user authorized a second bounded amendment after final implementation review
proved that `scripts/architecture_program_runner_change_allowance.py` is the live
Change Allowance owner for the compatibility `create-spec` preflight. This is a
required runner-safety correction, not a general runner expansion. The additional
candidate ceiling is exactly:

- `scripts/architecture_program_runner_change_allowance.py`; and
- `tests/test_architecture_program_runner_change_allowance.py`.

The correction must permit `create-spec` preflight to accept only the canonical
planning artifacts owned by the immediately preceding successful complete
`plan-batch` transaction: its `CURRENT.md`, exact dispatch, exact runway/spec, and
exact selection-transaction artifact as applicable. Derive or validate those
paths from authoritative Run State and the exact completed planning transaction or
receipt.

Do not permit the complete planning root, arbitrary prior-phase `evidence_paths`,
arbitrary Markdown files, or unrelated project files. Focused regression coverage
must prove the successful serialized `select-dispatch` to compatibility
`create-spec` transition, acceptance of the exact transaction-owned paths,
rejection of unrelated planning and project files, and unchanged execution and
closeout allowances.

Preserve `select-dispatch`, `create-spec`, `execute`, and `closeout` as the exact
serialized identities. Do not change the Run State version, transition graph,
receipt schema, or resume compatibility. Do not edit
`architecture_program_runner_state.py`,
`architecture_program_runner_validation.py`, or
`architecture_program_runner_command.py`; stop if a focused test proves one is
required.

The required-green skill-contract checks use separate single-document structural
validations for the two contract-bearing changed skills. Existing catalog,
migration, routing, and quick-validation checks remain unchanged and own
relationship and ownership-transfer validation.

After a new independent review is clean against the exact second-amended dispatch
and runway, resume the preserved candidate diff under a fresh strict lease whose
implementation revision is exactly
`5aa5add1251d1e4b3630a9678fdec244949cf691`. All CCFG-26 preservation and existing
no-new-protocol, no-new-wrapper, no-new-store, no-closeout, and no-successor
constraints remain unchanged.

## Target Ownership Boundary

### Human command owner

The default agent and `skills/plan-batch/SKILL.md` own all semantic decisions:

1. consume Planning State `current` and `validate` facts;
2. resolve exactly one existing ledger finding or current selected dispatch;
3. assemble the selected dispatch, authoritative source evidence, explicit user
   constraints and approvals, and the minimum viable change record;
4. invoke `batch_planner` directly;
5. invoke `batch_plan_reviewer` directly with independently supplied evidence, the
   selected dispatch identity, and the exact draft;
6. return named findings to `batch_planner` only through the default agent;
7. stop on a repeated material finding, expanding architecture, stale evidence, or
   an unrecorded user choice;
8. invoke the deterministic command boundary to validate the exact accepted
   draft/review and apply DEC-038; and
9. report at most one queued runway and stop before implementation.

The script must not spawn or invoke agents. The planner must not invoke or select
evidence for the reviewer. The reviewer remains read-only.

### Deterministic command boundary

Implement one installed `scripts/plan_batch.py` boundary, following the established
`add-to-ledger` stdin/stdout pattern where useful. It owns only deterministic
validation and transaction application:

- validate explicit generation, root, current-state, ledger, selected-dispatch,
  source, draft, proportionality, reviewer, approval, and idempotence inputs;
- reject unsupported sources, missing current/validate facts, stale selected
  dispatch or draft identity, mismatched reviewer basis, unresolved decisions,
  unapproved residual complexity, non-clean review, duplicate queue state, and
  forbidden paths;
- validate exactly one `planning-dispatch/v1` and one `planning-runway/v1` contract,
  semantic slice boundaries, and one selected validation profile;
- call the existing `simulate_selection_transaction(...)` or its accepted public
  equivalent without copying store or saga logic;
- return compact result and transaction receipt facts; and
- perform no planning choice, agent invocation, implementation, commit, closeout,
  or successor selection.

Do not add a schema, persistent draft store, second transaction, queue wrapper,
public retry token, new lifecycle state, or permanent proportionality artifact.
Blocked draft and review evidence remains non-executable caller output or uses an
already-authorized ephemeral run-artifact location; it must never look queued to
`work-batch`.

### Planner result semantics

The registered `batch_planner` TOML owns its exact result schema. It must emit
machine-readable output containing at least:

- status and exact selected-dispatch, source, and currentness basis;
- one non-executable dispatch/runway draft or a blocking result;
- included and deferred finding IDs;
- batch kind, risk classes, approvals, validation profile, stop conditions, and
  semantic `slice_shape` rationale;
- the compact proportionality record;
- unresolved user decisions and named corrections; and
- no queue, mutation, implementation, review, or delegation authority.

### Planning reviewer result semantics

The registered `batch_plan_reviewer` TOML owns its exact result schema and returns
only fields equivalent to:

```yaml
status: clean | findings | blocked
review_basis: string
minimum_viable_alternative: string
unjustified_additions: []
slice_shape_findings: []
scope_leaks: []
user_decisions: []
required_fixes: []
```

`review_basis` must bind all of the following:

- selected dispatch path, finding IDs, revision or canonical content hash;
- source/currentness facts and Planning State diagnostic identity;
- explicit user constraints and approvals;
- proportionality record; and
- byte-stable or canonical hash of the reviewed draft.

A corrected dispatch or draft invalidates the prior review and requires a fresh
direct reviewer invocation.

## Batch Scope

Allowed candidate areas across the batch, restricted further by each slice:

- `skills/plan-batch/**`
- `scripts/plan_batch.py`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `skills/architecture-program-runway/**`
- `skills/batch-runway/**`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_change_allowance.py`
- `skills/planning-artifacts/SKILL.md`
- `skills/legacy-removal/SKILL.md`
- `skills/port-by-contract/SKILL.md`
- `skills/dead-surface-audit/SKILL.md`
- `scripts/cross_checkout_context.py` only for unchanged-link ownership evidence;
  semantic edits require replanning
- `codex-features.json`
- `skills-lock.json`
- `docs/skill-routing-contract.md`
- `docs/workflow-guide.md`
- `README.md`
- `CHANGELOG.md`
- `tests/test_plan_batch.py`
- `tests/test_architecture_program_runner.py`
- `tests/test_architecture_program_runner_change_allowance.py`
- `tests/test_codex_features_manifest.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_deletion_test_vocabulary_ownership.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/fixtures/command-owner-scenarios/workflow-cases.yaml`
- `tests/fixtures/command-owner-scenarios/workflow_adapters.py`
- focused new fixtures under `tests/fixtures/plan-batch/`

Read-only except for execution-owned use:

- `scripts/architecture_program_runner_state.py`,
  `scripts/architecture_program_runner_validation.py`, and
  `scripts/architecture_program_runner_command.py`; a required semantic edit is a
  stop condition
- `scripts/planning_contract.py`
- `schemas/planning-*.schema.json`
- planning contract tests
- `skills/planning-state/**` and `scripts/planning_state.py`, except focused
  manifest ownership of the unchanged helper link
- `skills/add-to-ledger/**` and `scripts/add_to_ledger.py`
- `skills/work-batch/**`
- execution agents and execution contracts retained for CCFG-26
- installer implementation except focused manifest/lock consumption

A required semantic edit in a read-only area blocks for replanning. Moving the
unchanged temporary helper installation link from Batch Runway to the existing
`planning-state` feature is installation ownership only. It must not change helper
behavior or give Planning State new semantic authority. Duplicating the link,
adding a shared feature, or creating a bridge version is forbidden.

## CCFG-26 Preservation Contract

CCFG-25 removes planning ownership only. Until CCFG-26 closes, preserve all current
surfaces supporting:

- proceed and stop decisions;
- worker and reviewer delegation;
- recovery and resume;
- validation execution and acceptance;
- implementation review coordination;
- commits and commit receipts;
- execution-ledger state and per-slice evidence;
- finalization and closeout artifact production;
- same-batch program reconciliation and no-successor enforcement; and
- strict cross-checkout execution safety.

Current owner distribution may span APR, Batch Runway, `work-batch`, agents,
references, runner phases, tests, and manifest links. A surface may be removed only
when current caller evidence proves it is planning-only. If ownership is mixed or
ambiguous, preserve it and block for CCFG-26 or explicit replanning.

## Batch Non-Goals

- No CCFG-26 execution or closeout ownership transfer.
- No planning schema or DEC-038 semantic change.
- No live migration of canonical Markdown to candidate v1 operational blocks.
- No default-generation switch, candidate merge, cutover rehearsal, or bridge
  deletion.
- No new source adapter, intake behavior, ledger-store behavior, planning
  projection, or runner protocol.
- No lexical ban on legacy vocabulary. Tests prove absence of behavioral and
  runtime dependencies; historical and negative assertions may name old surfaces.
- No new permanent planner/reviewer framework beyond the two registered roles.
- No successor selection.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2.
Use Batch Runway Compact Report Contract v1 for coordinator receipts.
Use Batch Runway Compact Convergence Assessment v1 for routine status.
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
- `skills/dead-surface-audit/SKILL.md`

Workers implement one slice only and do not delegate. The coordinator owns
validation, specialist and independent review, candidate installation, commits,
execution-ledger updates, and same-batch closeout.

Overrides:

- Preserve the complete CCFG-26 contract above even when surrounding planning
  sections are narrowed.
- Remove no legacy planning surface without current caller evidence and replacement
  behavioral proof.
- Candidate implementation and stable planning receipt commits remain distinct.

## Validation Contract

Profile:
`skills/batch-runway/references/validation-profiles/project-harness-production.md`.

Status classes:

- Candidate unit, schema/store/transaction, scenario/catalog, skill-contract,
  routing, strict-context, installer, Ruff, exact configured-project
  changed-script BasedPyright, and whitespace gates: `required-green`, except
  commands explicitly classified below.
- New `tests/test_plan_batch.py` and focused fixtures: `implementation-created` by
  Slice 1, then `required-green`.
- Slice 1 manifest:
  - `test_executable_work_source_boundary_is_explicit`: `required-green`;
  - `test_plan_batch_command_owner_runtime_boundaries_are_explicit`:
    `known-red-baseline`, owned by Slice 2;
  - `test_work_batch_reconciles_same_batch_closeout`: `known-red-baseline`, owned
    by CCFG-26.
- After Slice 2 and at final validation, the complete manifest is
  `known-red-baseline` with exactly the one CCFG-26 failure; a filtered command
  excluding that node is `required-green`.
- Full broad legacy/projection suite: `known-red-baseline`; preserve only the
  reproduced preclassified non-CCFG-25 failures and accept no new failure.
- Final exact scenario acceptance: `required-green`, one evidence-pytest process,
  exact clean candidate commit, all required scenario meanings, 31 contracts, 17
  families, six keys, and six aliases.

Every test-changing slice receives delta-only `test-quality-review`. Slices 1 and
2 receive import-topology review. Slice 2 and the final exact range receive
`dead-surface-audit`.

## Execution Ledger

| Slice | Status | Commit | Review | Notes |
|---|---|---|---|---|
| 1. Implement installed `plan-batch` owner | Completed | `5aa5add1251d1e4b3630a9678fdec244949cf691` | Clean | Installed owner, exact planning-quality gates, DEC-038 recovery, isolated install, import-topology, and delta-only test-quality proof are green. |
| 2. Remove displaced planning ownership | Completed | `12f70727f7496e2aa2d5fff9b748ee97e19e63a2` | Clean | Exact reviewed binary diff `815c4ad7b15e9143cb95e3f5790440021416ccb28bd8120731ac92314c8b023e`; 181 tests and 241 subtests passed, both single-document structural validations passed, specialist reviews and final independent review clean. |
| 3. Converge installation and final acceptance | Completed | `89671eceb9103039e7e6660e73837827c167a3a1` | Clean | Core pytest: 244 passed and 18 subtests; filtered gates, 69-scenario catalog, structural checks, Ruff, exact three-script BasedPyright, and diff-check green. Fresh and isolated installations converged without stable-home change; exact acceptance and all final exact-range reviews passed. |

## Execution Startup Evidence

```yaml
runway: docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/runway.md
planning_state: passed
strict_preflight:
  status: ready
  reason: current repository facts satisfy first-handoff integrity
  live_context:
    interface: cross-checkout-context/v1
    generation_role: stable
    toolchain_source_root: /home/alacasse/projects/codex-config
    toolchain_commit: 29853cc291c4a3e2c900c0e6e1aa6e7a96203cb2
    canonical_planning_repository_root: /home/alacasse/projects/codex-config
    canonical_planning_commit_before: 29853cc291c4a3e2c900c0e6e1aa6e7a96203cb2
    implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
    implementation_commit_before: 91179e84c7cfed666be224575db7000ca0ea01b3
    codex_home: /home/alacasse/.codex
    canonical_state_mutation_allowed: true
baseline:
  candidate_commit: 91179e84c7cfed666be224575db7000ca0ea01b3
  manifest: 18 passed, exactly 3 assigned failures
  scenario_acceptance: 69 scenarios, 31 contracts, 17 families, one pytest process
```

## Orchestration Anomalies

```yaml
orchestration_anomalies:
  - id: slice-2-interrupted-worker-late-completion
    impact: low
    evidence: interrupted worker completed two in-scope edits after interruption
    reconciliation: >-
      Exact authorship and the valid strict lease were reconciled; the retry
      worker stopped on overlap, then resumed only after coordinator approval.
    lost_or_unknown_changes: false
  - id: slice-3-repository-wide-typecheck-baseline
    impact: low
    evidence: bare configured-project BasedPyright reproduced 311 historical errors and 16 warnings
    reconciliation: >-
      Execution stopped before installation; the gate was reclassified through
      an independently reviewed validation-only amendment without policy or
      unchanged-owner edits.
    lost_or_unknown_changes: false
  - id: slice-3-explicit-file-scope-expansion
    impact: low
    evidence: first amendment analyzed out-of-project tests and a fixture and returned 120 errors and 3 warnings
    reconciliation: >-
      Independent planning review rejected the command before execution. The
      second authorized amendment aligned the gate to the three changed scripts
      in the configured project and received a fresh clean review.
    lost_or_unknown_changes: false
```

## Slice 1: Implement The Installed `plan-batch` Owner

### Scope

Implement, register, install, and prove the complete replacement planning path
while leaving APR and Batch Runway planning surfaces physically present as a
rollback baseline for Slice 2.

Primary allowed areas:

- `skills/plan-batch/**`
- `scripts/plan_batch.py`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `codex-features.json` and `skills-lock.json` for the owner, agents, planning
  contracts, Planning State, and unchanged helper-link ownership
- `tests/test_plan_batch.py`
- `tests/fixtures/plan-batch/**`
- planning and planning-quality scenario/catalog/adapter/test surfaces
- focused manifest and routing-owner tests
- `CHANGELOG.md`

Planning-contract code/schemas, APR, Batch Runway, `work-batch`, and
`add-to-ledger` are read-only in this slice.

### Work

- Replace the thin `plan-batch` router with the complete command-owner procedure
  and explicit direct planner/reviewer orchestration.
- Add registered `batch_planner` and `batch_plan_reviewer` TOMLs with disjoint
  capabilities and exact machine-readable result contracts.
- Implement `scripts/plan_batch.py` as the deterministic validation and DEC-038
  application boundary.
- Make the candidate `plan-batch` feature install its script and require only
  planning contracts, Planning Artifacts, Planning State, and registered agents.
- Move only the unchanged helper installation link to the existing Planning State
  feature so `plan-batch` does not depend on Batch Runway for mechanical context.
- Bind planning and planning-quality scenarios to the installed owner. Keep
  collaborator injection only where it proves direct independent-role input.
- Prove current/validate guards, selected/queued/active refusal, one finding only,
  minimum viable scope, semantic slices, approval scope, direct role invocation,
  correction routing, repeated-finding stop, stale-draft and unresolved-decision
  rejection, dispatch/draft review-basis binding, atomic queue gating, partial
  failure recovery, exact replay, and stop-before-implementation.

Do not remove or rewire APR, Batch Runway, or architecture runner callers in this
slice. Slice 1 changes the `plan-batch` feature dependency list; Slice 2 owns
system-wide legacy caller rewiring and removal of the helper link from Batch
Runway.

### Acceptance

- Candidate-installed `plan-batch` provides one complete end-to-end replacement
  planning path and has no semantic or runtime dependency on APR or Batch Runway.
- The default command owner directly invokes both registered roles; neither role
  invokes the other or mutates state.
- Exact selected-dispatch and draft lineage, clean review, proportionality, and
  approval gates are mandatory before DEC-038 application.
- Cohesive one-slice and justified producer/consumer plans queue successfully;
  filler decomposition and unjustified expansion block without queue mutation.
- Blocked and stale drafts remain non-executable and invisible as queued/active to
  Planning State and `work-batch`.
- Interrupted DEC-038 stages resume exactly and replay without duplicate effects.
- The installed owner writes only authorized current, dispatch, runway, and
  transaction paths.
- Legacy owners remain physically present and may still have unchanged legacy
  callers until Slice 2; Slice 1 does not claim sole system-wide ownership.
- No semantic change exists in planning contracts, Planning State, APR, Batch
  Runway, `work-batch`, or `add-to-ledger`.

### Required-Green Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_planning_contract_schema.py \
  tests/test_planning_contract_store.py \
  tests/test_planning_contract_artifacts.py \
  tests/test_planning_transaction.py \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_catalog.py \
  tests/test_skill_routing_rule_ownership.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py \
  -k 'not test_plan_batch_command_owner_runtime_boundaries_are_explicit and not test_work_batch_reconciles_same_batch_closeout'
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache scripts/plan_batch.py tests/test_plan_batch.py tests/fixtures/command-owner-scenarios
.venv/bin/basedpyright scripts/plan_batch.py tests/test_plan_batch.py
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature plan-batch
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature plan-batch --dry-run
git diff --check
```

### Known-Red Manifest Diagnostic

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
```

Expected after Slice 1: exactly
`test_plan_batch_command_owner_runtime_boundaries_are_explicit` and
`test_work_batch_reconciles_same_batch_closeout` may fail. No other failure is
accepted.

### Worker Brief

The spawned `runway_worker` is the coding subagent. Read this runway and the
selected dispatch from the stable planning checkout, implement only Slice 1 in the
candidate checkout, and do not spawn, delegate to, or wait on other agents. Do not
edit APR, Batch Runway, `work-batch`, planning contracts/schemas, Planning State
semantics, or stable planning state. Return the required v2 result with exact
changed paths and verified strict context.

### Reviewer Brief

The separate `runway_reviewer` receives the exact candidate commit or task-scoped
worktree diff from the coordinator. Verify the end-to-end installed owner,
planner/reviewer independence, selected-dispatch and exact-draft lineage,
transaction gating, scope, tests, manifest classifications, and absence of legacy
removal. Echo the coordinator-provided `diff_basis` and verified strict context in
the v2 result.

Reviews: independent `runway_reviewer`, `import_topology_reviewer`, and delta-only
`test-quality-review`.

Commit: `feat: make plan-batch the planning command owner`

### Stop Conditions

- Stop on a new schema, store, queue transaction, lifecycle state, persistent draft
  store, retry token, source adapter, or compatibility wrapper.
- Stop if agent invocation moves into the script or role independence is prose-only.
- Stop if queue writes can occur before exact clean review and approval gates.
- Stop if target scenarios still execute only a fixture owner.
- Stop on semantic edits to planning contracts, Planning State, APR, Batch Runway,
  `work-batch`, `add-to-ledger`, or helper behavior.
- Stop if Slice 1 removes system-wide legacy planning routes or claims sole
  system-wide ownership before Slice 2.

## Slice 2: Remove Displaced Planning Ownership

### Approval Gate

Slice 1 is committed, candidate-installed, green, and independently reviewed.
The exact bounded amendment above must also have a clean independent review before
the Slice 2 worker handoff. The first fresh strict lease must name candidate commit
`5aa5add1251d1e4b3630a9678fdec244949cf691`.
Before narrowing any surface, the coordinator records a current owner/caller matrix
proving:

- all selection, grouping, prioritization, dispatch, runway, risk, approval,
  validation-profile, and queue routes resolve to `plan-batch`;
- target planning scenarios have no runtime or behavioral dependency on APR, Batch
  Runway, `create-spec`, exact prompt prose, stable-only paths, or fixture-only
  ownership; historical and negative vocabulary remains allowed;
- every CCFG-26 proceed/stop, delegation, recovery, validation, review, commit,
  receipt, execution-ledger, finalization, closeout, same-batch reconciliation, and
  strict execution-safety surface remains identified and preserved; and
- the architecture program runner invokes the public command-owner path and does
  not reimplement selection, proportionality, review, or queue semantics.

Removal requires targeted dead-surface evidence and independent review agreement.
Ambiguous, mixed planning/execution, or unclassified surfaces block.

### Scope

Primary allowed areas:

- `skills/architecture-program-runway/**`
- `skills/batch-runway/**`
- `scripts/architecture_program_runner.py`
- `scripts/architecture_program_runner_phase_contract.py` as the expected semantic
  edit
- `scripts/architecture_program_runner_change_allowance.py` only for the exact
  transaction-owned compatibility `create-spec` allowance correction
- `skills/planning-artifacts/SKILL.md`, `skills/legacy-removal/SKILL.md`,
  `skills/port-by-contract/SKILL.md`, and `skills/dead-surface-audit/SKILL.md` only
  for their planning-handoff routes
- `skills/plan-batch/**` only for replacement-consumer corrections
- focused manifest, lock, routing, workflow, runner, skill-contract, migration,
  projection-routing, scenario, and deletion-evidence tests
- `tests/test_architecture_program_runner_change_allowance.py` for the required
  path-specific regression; no new harness
- `codex-features.json`, `skills-lock.json`, and `CHANGELOG.md`

Read-only runner modules:

- `scripts/architecture_program_runner_state.py`
- `scripts/architecture_program_runner_validation.py`
- `scripts/architecture_program_runner_command.py`

Stop if a focused failing test or direct invariant proves one requires an edit.

The new owner implementation, planning contracts/schemas, Planning State semantics,
`work-batch`, execution agents, and helper behavior are read-only.

### Work

- Remove APR grouping, ranking, prioritization, selection, selected-dispatch,
  create-next-runway, queue-preparation, and `plan-batch` handoff ownership from its
  skill, agent metadata, templates, runner prompts, feature description, and tests.
- Preserve any APR closeout or reconciliation support and every mixed surface named
  by the CCFG-26 Preservation Contract, with caller, reason, owner, and removal
  condition.
- Remove Batch Runway `create-spec` mode, create-spec guidance, planning
  project-value ownership, `plan-batch` handoff claims, and planning-only tests.
- Preserve Batch Runway proceed/stop, delegation, recovery, validation acceptance,
  implementation review, commit and receipt handling, execution-ledger state,
  finalization, closeout support, and cross-checkout execution safety.
- Rewire the architecture program runner's existing planning phase to the public
  `plan-batch` command contract without a new protocol or embedded planner. Leave
  execution and closeout behavior unchanged.
- Permit compatibility `create-spec` preflight to accept only the exact canonical
  `CURRENT.md`, dispatch, runway/spec, and selection-transaction paths owned by
  the immediately preceding successful complete `plan-batch` transaction. Keep
  unrelated planning and project paths rejected.
- Preserve all four serialized phase identities, receipts, and transitions. Make
  the existing planning path one complete `plan-batch` invocation. Keep
  `create-spec` only as a compatibility observation/advance step with no Batch
  Runway planning invocation, draft creation, repeated decision, or planner role.
- Rewire the four named support skills to public `plan-batch` without changing
  their evidence, layout, classification, contract-distillation, or mutation
  boundaries.
- Remove the remaining `plan-batch` manifest dependencies on APR and Batch Runway
  only if not already removed in Slice 1, and remove the helper link from Batch
  Runway only after the unchanged link is installed through Planning State.
- Delete or rewrite fixture helpers and topology assertions that preserve displaced
  planning owners. Keep legitimate target-behavior adapters with current callers.
- Rewrite tests to assert structural ownership and runtime absence, not exact legacy
  wording or blanket vocabulary absence.

### Acceptance

- Runtime and semantic dependencies from `plan-batch` to APR, Batch Runway, and
  `create-spec` are zero.
- APR exposes no planning lifecycle or queue authority.
- Batch Runway exposes no planning or `create-spec` authority.
- APR, Batch Runway, `work-batch`, agents, contracts, and runner retain the complete
  CCFG-26 Preservation Contract; no mixed surface is narrowed by inference.
- The architecture runner uses `plan-batch` and contains no duplicate planning
  decision rules.
- The compatibility `create-spec` Change Allowance accepts the exact completed
  transaction-owned planning paths and no planning-root, arbitrary evidence-path,
  Markdown, or unrelated-project wildcard.
- `select-dispatch`, `create-spec`, `execute`, and `closeout` remain the exact
  serialized phase identities with receipt and transition compatibility intact;
  the first two are temporary labels owned for migration/removal by CCFG-27 and
  final cleanup by CCFG-29 at the latest.
- One complete `plan-batch` invocation owns selection, independent planning
  review, and DEC-038; `create-spec` owns no planning behavior.
- The four support skills hand planning to public `plan-batch` and retain no
  queue, dispatch, runway, or lifecycle mutation authority.
- No production or scenario caller reaches a removed planning surface.
- Target behavior is topology-independent; legacy terms may remain only in
  historical, negative, migration, or removal assertions that do not bind behavior.
- The full manifest retains only the one named CCFG-26 failure.

### Required-Green Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_architecture_program_runner.py \
  tests/test_architecture_program_runner_phase_contract.py \
  tests/test_architecture_program_runner_change_allowance.py \
  tests/test_batch_runway_create_spec_contract.py \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_catalog.py \
  tests/test_skill_routing_rule_ownership.py \
  tests/test_skill_contract_catalog.py \
  tests/test_skill_contract_migration.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py \
  -k 'not test_work_batch_reconciles_same_batch_closeout'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_planning_state_consumer_projection_routing.py \
  tests/test_deletion_test_vocabulary_ownership.py \
  -k 'legacy_removal or legacy_evidence_no_state_writes or parallel_planning_systems'
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/architecture-program-runway/SKILL.md
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/legacy-removal/SKILL.md
python /home/alacasse/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/batch-runway
python /home/alacasse/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/plan-batch
python /home/alacasse/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/planning-artifacts
python /home/alacasse/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/port-by-contract
python /home/alacasse/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/dead-surface-audit
.venv/bin/ruff check --no-cache scripts/architecture_program_runner.py scripts/architecture_program_runner_phase_contract.py scripts/architecture_program_runner_state.py scripts/architecture_program_runner_validation.py scripts/architecture_program_runner_command.py scripts/plan_batch.py tests
.venv/bin/basedpyright scripts/architecture_program_runner.py scripts/architecture_program_runner_phase_contract.py scripts/architecture_program_runner_change_allowance.py scripts/plan_batch.py
git diff --check
```

### Known-Red Diagnostics

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py
```

The manifest may fail only
`test_work_batch_reconciles_same_batch_closeout`. The broad legacy/projection
suite may retain only reproduced, preclassified non-CCFG-25 failures; no new or
CCFG-25-owned failure is accepted.

### Worker Brief

The spawned `runway_worker` is the coding subagent. Resume only Slice 2 in the
candidate checkout and do not spawn, delegate to, or wait on other agents. Use the
coordinator-supplied caller inventory. Remove only planning-owned surfaces; retain
every CCFG-26 surface and stop on mixed or ambiguous ownership. Do not change the
new owner, Planning State semantics, `work-batch`, execution agents/contracts, or
helper behavior. Preserve the existing candidate diff and make only the focused
Change Allowance correction and regression authorized by the second amendment.
Do not edit state, validation, or command modules. Preserve the serialized phase
identities and transition graph, and stop on any owner/caller outside the exact
second-amended ceiling. Return exact changed paths and verified strict context.

### Reviewer Brief

The separate `runway_reviewer` receives the coordinator-provided exact Slice 2
commit or task-scoped diff. Verify each deletion against caller and replacement
evidence, structural absence of planning ownership, complete CCFG-26 preservation,
runner rewiring without a second planner, manifest classification, and scope. Echo
`diff_basis` and verified strict context in the v2 result.

Reviews: targeted `dead-surface-audit`, `import_topology_reviewer`, independent
`runway_reviewer`, and delta-only `test-quality-review`.

Commit: `refactor: remove legacy planning ownership`

### Stop Conditions

- Stop if removal lacks current caller and replacement evidence.
- Stop if any CCFG-26 proceed/stop, delegation, recovery, validation, review,
  commit, receipt, execution-ledger, finalization, closeout, reconciliation, or
  strict execution-safety behavior would be removed or altered.
- Stop if the runner needs a new public protocol, bridge, or duplicate planner.
- Stop if helper behavior or Planning State semantic authority changes.
- Stop if `select-dispatch`, `create-spec`, `execute`, or `closeout`, their receipts,
  or their transition graph would be renamed, removed, versioned, or migrated.
- Stop if another live planning caller or runner semantic owner is discovered
  outside the exact second-amended ceiling.
- Stop if the Change Allowance repair admits the whole planning root, arbitrary
  evidence paths, arbitrary Markdown, or unrelated project files.
- Stop if a focused test proves that state, validation, or command modules require
  edits.
- Stop on a test that can turn green only by preserving obsolete topology or by
  banning legitimate historical/negative vocabulary.

## Slice 3: Converge Installation And Final Acceptance

### Scope

Reconcile the final candidate generation and prove complete CCFG-25 acceptance.
Allowed areas are the batch scope, limited to corrections required by final
installation, exact acceptance, documentation, and review. No new semantic design
is allowed.

### Work

- Converge manifest, lock, installed skill/script/agent links, versions, routing
  docs, workflow guide, README, and changelog around the final owner topology.
- Perform a real all-feature install into a fresh empty temporary Codex home and
  converge the fixed isolated candidate home. Verify every managed link resolves to
  candidate source and both installs are dry-run clean afterward.
- Verify stable Codex home status is byte-for-byte unchanged before and after.
- Run the exact CCFG-33 acceptance CLI once from the clean final candidate commit,
  using explicit fresh result, JSON report, and text report paths.
- Read and validate the generated outputs and record both SHA-256 hashes.
- Prove every COR-008 and planning-quality key, both CCFG-25 manifest failures green,
  the one CCFG-26 failure unchanged, and zero behavioral/runtime dependency on
  displaced planning topology.
- Perform final exact-range independent, import-topology, dead-surface, and
  delta-only test-quality reviews.
- Record files changed, additions/deletions, diff bytes, focused and exact
  acceptance time, pytest process count, and context usage when available.

### Acceptance

```yaml
planning_quality:
  default_agent_is_only_queue_mutator: true
  registered_batch_planner: true
  registered_batch_plan_reviewer: true
  planner_cannot_invoke_reviewer: true
  reviewer_receives_independent_source_evidence: true
  reviewer_receives_selected_dispatch_identity: true
  every_new_or_amended_runway_reviewed: true
  proportionality_required_before_queue: true
  source_mechanics_can_be_narrowed: true
  minimum_viable_change_recorded: true
  residual_complexity_requires_user_approval: true
  fixed_slice_count_required: false
  filler_slices_rejected: true
  stale_draft_rejected: true
  blocked_review_preserves_non_executable_draft: true
  legacy_planning_owner_dependencies: 0
cor_008:
  resolved_planning_transaction: true
  exactly_one_runnable_runway: true
  stale_lineage_and_partial_failure_recovery: true
  no_broad_owner_dependency: true
  planning_stops_before_implementation: true
```

Additional final conditions:

- `plan-batch` installs and operates without APR or Batch Runway dependencies.
- Target scenarios and production callers do not invoke or depend on displaced
  planning owners, paths, modes, or fixture-only behavior. Historical and negative
  assertions may still name them.
- The serialized `select-dispatch` and `create-spec` labels remain compatibility
  observations only and do not count as displaced planning owners while their
  migration/removal decision remains assigned to CCFG-27 and cleanup deadline to
  CCFG-29.
- APR and Batch Runway retained surfaces satisfy the complete CCFG-26 Preservation
  Contract with named callers and deletion conditions.
- Candidate code cannot mutate canonical planning state during fixture or isolated
  installation validation.
- Stable/default generation remains unchanged.

### Required-Green Core Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_planning_contract_schema.py \
  tests/test_planning_contract_store.py \
  tests/test_planning_contract_artifacts.py \
  tests/test_planning_transaction.py \
  tests/test_architecture_program_runner.py \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_catalog.py \
  tests/test_skill_routing_rule_ownership.py \
  tests/test_skill_contract_catalog.py \
  tests/test_skill_contract_migration.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_codex_features_manifest.py \
  -k 'not test_work_batch_reconciles_same_batch_closeout'
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_planning_state_consumer_projection_routing.py \
  tests/test_deletion_test_vocabulary_ownership.py \
  -k 'legacy_removal or legacy_evidence_no_state_writes or parallel_planning_systems'
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/architecture-program-runway/SKILL.md
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/legacy-removal/SKILL.md
.venv/bin/ruff check --no-cache .
.venv/bin/basedpyright \
  scripts/architecture_program_runner_change_allowance.py \
  scripts/architecture_program_runner_phase_contract.py \
  scripts/plan_batch.py
git diff --check 91179e84c7cfed666be224575db7000ca0ea01b3
```

The BasedPyright command above must exit `0` with zero errors and zero warnings.
Do not add another Python path merely because it appears in the Git diff. Changed
tests and scenario fixtures remain outside the repository-configured `scripts`
project and are covered by the existing pytest and Ruff gates.

### Real Candidate Installation And Stable-Home Comparison

```sh
fresh_candidate_home="$(mktemp -d /tmp/ccfg-25-codex-home.XXXXXX)"
stable_status_before="$(mktemp /tmp/ccfg-25-stable-before.XXXXXX)"
stable_status_after="$(mktemp /tmp/ccfg-25-stable-after.XXXXXX)"

./install.sh --codex-home /home/alacasse/.codex --status >"$stable_status_before"
./install.sh --codex-home "$fresh_candidate_home" --all
./install.sh --codex-home "$fresh_candidate_home" --status
./install.sh --codex-home "$fresh_candidate_home" --all --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --all
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --all --dry-run
./install.sh --codex-home /home/alacasse/.codex --status >"$stable_status_after"
cmp "$stable_status_before" "$stable_status_after"
```

All commands above are `required-green`. Installation must perform real writes only
to the fresh temporary home and the isolated candidate home, never the stable home.

### Exact-Commit Acceptance With Explicit Outputs

Run from a clean final candidate commit:

```sh
acceptance_root="$(mktemp -d /tmp/ccfg-25-acceptance.XXXXXX)"
COMMAND_OWNER_CANDIDATE_CODEX_HOME=/home/alacasse/.codex-command-owner-redesign \
PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python scripts/command_owner_scenarios.py accept \
  tests/fixtures/command-owner-scenarios \
  --result-output "$acceptance_root/acceptance-result.json" \
  --json-report-output "$acceptance_root/report.json" \
  --text-report-output "$acceptance_root/report.txt"

python -m json.tool "$acceptance_root/acceptance-result.json" >/dev/null
python -m json.tool "$acceptance_root/report.json" >/dev/null
test -s "$acceptance_root/report.txt"
cat "$acceptance_root/report.txt"
sha256sum \
  "$acceptance_root/acceptance-result.json" \
  "$acceptance_root/report.json"
```

Status: `required-green`. The acceptance command must launch exactly one evidence
pytest process and bind the generated evidence to the clean exact candidate commit.
The coordinator reads the text report and records the generated-result and canonical
report hashes in closeout.

### Known-Red Diagnostics

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_state_consumer_projection_routing.py tests/test_deletion_test_vocabulary_ownership.py
.venv/bin/basedpyright
```

- Manifest status: `known-red-baseline`; exactly
  `test_work_batch_reconciles_same_batch_closeout` may fail.
- Broad legacy/projection status: `known-red-baseline`; only reproduced,
  preclassified non-CCFG-25 failures may remain. No new or CCFG-25 failure is
  accepted.
- Repository-wide BasedPyright status: `known-red-baseline`. It is acceptable
  only when the corrected three-script required-green command exits `0` with
  zero errors and zero warnings, the bare audit introduces no new diagnostic
  relative to baseline `91179e84c7cfed666be224575db7000ca0ea01b3`, the
  candidate total is no worse than the recorded 314 errors and 16 warnings,
  and no unchanged module is edited merely to reduce historical diagnostics.
  Candidate `89671eceb9103039e7e6660e73837827c167a3a1` records 311 errors and
  16 warnings and removes three baseline diagnostics.

### Worker Brief

The spawned `runway_worker` is the coding subagent. Implement only bounded final
convergence corrections in the candidate checkout and do not spawn, delegate to,
or wait on other agents. Do not run final exact acceptance, perform final reviews,
mutate stable planning, change CCFG-26 behavior, or introduce a new design. Return
exact changed paths and verified strict context.

### Reviewer Brief

The final `runway_reviewer` receives the exact range
`91179e84c7cfed666be224575db7000ca0ea01b3..89671eceb9103039e7e6660e73837827c167a3a1` plus validation,
installation, acceptance-output, and diagnostic evidence. Verify complete COR-008
behavior, selected-dispatch lineage, no lexical proxy for topology, complete
CCFG-26 preservation, stable-home immutability, allowed paths, and proportionality.
Echo that exact `diff_basis` and verified strict context in the v2 result.

Reviews: final exact-range `runway_reviewer`, `import_topology_reviewer`, targeted
`dead-surface-audit`, and delta-only `test-quality-review`.

Commit: `chore: complete plan-batch ownership transfer`

### Stop Conditions

- Stop on any new semantic decision, schema, bridge, compatibility wrapper, public
  mode, helper behavior, runner protocol, or owner not authorized by this runway.
- Stop if exact acceptance requires preserving legacy planning topology or exact
  prompt prose, or if tests rely on blanket absence of legacy words.
- Stop if stable-home state changes, candidate code writes canonical planning
  state, strict context is not ready, or candidate HEAD moves unexpectedly.
- Stop if the manifest contains a new failure or any CCFG-25 failure.
- Stop if any CCFG-26 responsibility is narrowed.
- Stop if CCFG-25 cannot close while CCFG-26 remains unselected.

## Final Closeout

After all slices are committed and every final gate is satisfied:

1. write `completed-slices.md` and `closeout.md` in this batch directory;
2. record exact candidate range, stable planning receipts, transaction recovery,
   installed links, removed/preserved surface inventory, validation, acceptance
   output hashes, reviews, and cost evidence;
3. mark CCFG-25 `Closed` in the program ledger;
4. clear selected dispatch, queued runway, and active runway for this batch;
5. set latest closeout to this batch;
6. leave CCFG-26 through CCFG-29 open and unselected; and
7. stop without selecting or preparing a successor.
