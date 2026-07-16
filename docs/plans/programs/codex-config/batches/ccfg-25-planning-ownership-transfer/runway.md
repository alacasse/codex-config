# CCFG-25 Planning Ownership Transfer Runway

## Purpose

Implement the complete candidate `plan-batch` command owner, including delegated
planning, independent planning review, proportionality and approval gates, and the
existing DEC-038 selection transaction. Migrate target planning behavior to the
installed owner, remove Architecture Program Runway planning ownership and Batch
Runway `create-spec` ownership, converge the isolated candidate installation, and
close CCFG-25 without beginning CCFG-26.

## Authority

- Finding: CCFG-25, entering this batch as `Open`.
- Dispatch: `dispatch.md`.
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

- `1 -> 2`: Slice 1 produces a complete installed replacement owner and green
  target-behavior evidence. Slice 2 can therefore narrow and delete legacy
  planning surfaces against a valid rollback point and current caller inventory.
- `2 -> 3`: Slice 2 produces the final semantic owner topology. Slice 3 has an
  independent environment and acceptance boundary: isolated installation,
  exact-commit scenario evaluation, manifest convergence, and range-wide review.

A separate planner/reviewer scaffolding slice is forbidden. Those roles have no
supported standalone outcome and must land with the complete command owner.
Generic docs, metadata, tests, or closeout work remain with the behavior or final
environment they validate.

## Baseline

- Stable toolchain and canonical planning checkout:
  `/home/alacasse/projects/codex-config`, branch `master`.
- Stable planning baseline before dispatch:
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
- CCFG-24B final exact acceptance reported 69 scenarios, 31 contracts, 17
  families, six evidence keys, and six aliases green.
- The candidate full manifest diagnostic has exactly three assigned failures at
  baseline. CCFG-25 owns:
  - `test_executable_work_source_boundary_is_explicit`;
  - `test_plan_batch_command_owner_runtime_boundaries_are_explicit`.
  CCFG-26 owns `test_work_batch_reconciles_same_batch_closeout`.

At execution startup, reproduce the exact candidate baseline, the two CCFG-25
manifest failures, the one deferred CCFG-26 failure, and the exact scenario
acceptance baseline before delegation. Any new or reclassified failure blocks
instead of widening scope.

## Project Values

- Planning artifact layout: Planning Artifact Layout v1.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-25-planning-ownership-transfer/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`.
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

## Planning Snapshot

Interface: `cross-checkout-context/v1`.

Installed helper expected at execution:
`/home/alacasse/.codex/scripts/cross_checkout_context.py`.

Canonical planning root:
`/home/alacasse/projects/codex-config/docs/plans`.

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 31d228d4ef9b94e2ccad0f5260670593ea9469f9
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 31d228d4ef9b94e2ccad0f5260670593ea9469f9
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 91179e84c7cfed666be224575db7000ca0ea01b3
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

This connector-backed planning session could not execute the installed local
helper. The immutable payload is assembled from the authoritative master revision
and CCFG-24B candidate closeout and is not a live execution lease. At `work-batch`
startup, pass it to the installed ready/blocked preflight. Proceed only on `ready`.
Before every worker and reviewer handoff, prepare a fresh live lease, validate the
active slice's exact write scope, and require matching non-null
`verified_cross_checkout_context` evidence.

## Target Ownership Boundary

### Human command owner

The default agent and `skills/plan-batch/SKILL.md` own all semantic decisions:

1. consume Planning State `current` and `validate` facts;
2. resolve exactly one existing ledger finding or current selected dispatch;
3. assemble authoritative source evidence, explicit user constraints and
   approvals, and the minimum viable change record;
4. invoke `batch_planner` directly;
5. invoke `batch_plan_reviewer` directly with independently supplied evidence and
   the exact draft;
6. return named findings to `batch_planner` only through the default agent;
7. stop on a repeated material finding, expanding architecture, stale evidence, or
   an unrecorded user choice;
8. invoke the deterministic command-owned boundary to validate the exact accepted
   draft/review and apply DEC-038;
9. report at most one queued runway and stop before implementation.

The script must not spawn or invoke agents. The planner must not invoke or select
evidence for the reviewer. The reviewer remains read-only.

### Deterministic command boundary

Implement one installed `scripts/plan_batch.py` boundary, following the established
`add-to-ledger` stdin/stdout pattern where useful. It owns only deterministic
validation and transaction application:

- validate explicit generation, root, current-state, ledger, source, draft,
  proportionality, reviewer, approval, and idempotence inputs;
- reject unsupported sources, missing current/validate facts, stale source or draft
  identity, mismatched reviewer basis, unresolved decisions, unapproved residual
  complexity, non-clean review, duplicate queue state, and forbidden paths;
- validate that the draft contains exactly one `planning-dispatch/v1` and one
  `planning-runway/v1` contract with semantic slice boundaries and one selected
  validation profile;
- call the existing `simulate_selection_transaction(...)` or its accepted public
  equivalent without copying store or saga logic;
- return compact result and transaction receipt facts;
- perform no planning choice, agent invocation, implementation, commit, closeout,
  or successor selection.

Do not add a schema, persistent draft store, second transaction, queue wrapper,
public retry token, new lifecycle state, or permanent proportionality artifact.
Blocked draft and review evidence remains non-executable caller output or uses an
already-authorized run-artifact location; it must never look queued to
`work-batch`.

### Planner result semantics

The registered `batch_planner` TOML owns its exact result schema. It must emit
machine-readable output containing at least:

- status and exact source/currentness basis;
- one non-executable dispatch/runway draft or a blocking result;
- included and deferred finding IDs;
- batch kind, risk classes, approvals, validation profile, stop conditions, and
  semantic `slice_shape` rationale;
- the full compact proportionality record from the CCFG-25 amendment;
- unresolved user decisions and named corrections;
- no queue, mutation, implementation, review, or delegation authority.

### Planning reviewer result semantics

The registered `batch_plan_reviewer` TOML owns its exact result schema and returns
only the accepted fields equivalent to:

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

The exact `review_basis` must bind the source/currentness facts, user constraints,
proportionality record, and byte-stable or canonical hash of the reviewed draft.
A corrected draft invalidates the prior review and requires a fresh direct reviewer
invocation.

## Batch Scope

Allowed candidate areas across the batch, restricted further by each slice:

- `skills/plan-batch/**`
- `scripts/plan_batch.py`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `skills/architecture-program-runway/**`
- `skills/batch-runway/**`
- `scripts/architecture_program_runner.py`
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
- `tests/test_codex_features_manifest.py`
- `tests/test_skill_routing_rule_ownership.py`
- `tests/test_skill_contract_catalog.py`
- `tests/test_skill_contract_migration.py`
- `tests/test_planning_state_consumer_projection_routing.py`
- `tests/test_command_owner_behavioral_scenarios.py`
- `tests/test_command_owner_scenario_catalog.py`
- `tests/fixtures/command-owner-scenarios/catalog.yaml`
- `tests/fixtures/command-owner-scenarios/workflow-cases.yaml`
- `tests/fixtures/command-owner-scenarios/workflow_adapters.py`
- focused new fixtures under `tests/fixtures/plan-batch/`

Read-only except for execution-owned use:

- `scripts/planning_contract.py`
- `schemas/planning-*.schema.json`
- `tests/test_planning_contract_schema.py`
- `tests/test_planning_contract_store.py`
- `tests/test_planning_contract_artifacts.py`
- `tests/test_planning_transaction.py`
- `skills/planning-state/**`
- `scripts/planning_state.py`
- `skills/add-to-ledger/**`
- `scripts/add_to_ledger.py`
- `skills/work-batch/**`
- execution agents and Batch Runway execution contracts retained for CCFG-26
- installer implementation except focused manifest/lock consumption

A required semantic edit in a read-only area blocks for replanning. Moving the
unchanged temporary cross-checkout helper link from Batch Runway to the existing
`planning-state` feature is allowed only as installation ownership, so
`plan-batch` can drop its Batch Runway dependency while `work-batch` continues to
receive the same helper through an already-required neutral feature. Do not change
helper behavior or give Planning State new semantic authority. A new shared
feature or bridge version is forbidden.

## Batch Non-Goals

- No CCFG-26 execution, recovery, validation acceptance, implementation review,
  commit, finalization, closeout, or same-batch reconciliation transfer.
- No planning schema or DEC-038 semantic change.
- No live migration of canonical Markdown to candidate v1 operational blocks.
- No default-generation switch, candidate merge, cutover rehearsal, or bridge
  deletion.
- No new source adapter, intake behavior, ledger-store behavior, or planning
  projection.
- No exact prompt-prose acceptance tests. Tests prove behavior and ownership.
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

- The execution coordinator must preserve CCFG-26-owned APR and Batch Runway
  execution/closeout surfaces even when their surrounding planning sections are
  narrowed.
- No legacy planning surface may be removed without a current caller inventory and
  replacement behavioral evidence.

## Validation Contract

Profile:
`skills/batch-runway/references/validation-profiles/project-harness-production.md`.

Status classes:

- Candidate baseline unit, schema/store/transaction, scenario/catalog, skill
  contract, routing, strict-context, installer, Ruff, BasedPyright, and whitespace
  gates: `required-green` or their explicitly reproduced baseline class.
- New `tests/test_plan_batch.py` and focused fixtures: `implementation-created` by
  Slice 1, then `required-green`.
- Full manifest before final convergence: `known-red-baseline`, exactly the three
  failures recorded by CCFG-24B.
- After Slice 1: both CCFG-25 manifest failures may remain red only when Slice 2
  explicitly owns their legacy-removal assertion; no new failure is allowed.
- After Slice 2: the full manifest may remain red only for
  `test_work_batch_reconciles_same_batch_closeout`, owned by CCFG-26.
- Broad legacy/projection diagnostics: preserve the exact preclassified identities;
  promote only CCFG-25 planning-owner nodes. No unrelated remediation is allowed.
- Final exact scenario acceptance: `required-green`, one evidence-pytest process,
  exact candidate commit, all 69 baseline scenarios plus any necessary CCFG-25
  replacement bindings, all 31 contracts, 17 families, six keys, and six aliases.

Every test-changing slice receives delta-only `test-quality-review`. Slices 1 and
2 receive import-topology review. Slice 2 and the final exact range receive
`dead-surface-audit`.

## Execution Ledger

| Slice | Status | Commit | Review | Notes |
|---|---|---|---|---|
| 1. Implement installed `plan-batch` owner | Pending | None | Pending | Complete command owner, registered planning roles, transaction gate, and installed-owner scenarios. |
| 2. Remove displaced planning ownership | Pending | None | Pending | Narrow APR and Batch Runway planning only after replacement evidence. |
| 3. Converge installation and final acceptance | Pending | None | Pending | Exact candidate installation, manifests, scenario acceptance, and COR-008 evidence. |

## Active Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Slice 1: Implement The Installed `plan-batch` Owner

### Scope

Implement, register, install, and prove the complete target planning owner while
leaving legacy planning surfaces physically present for rollback and deletion
evidence.

Primary allowed areas:

- `skills/plan-batch/**`
- `scripts/plan_batch.py`
- `agents/batch_planner.toml`
- `agents/batch_plan_reviewer.toml`
- `codex-features.json` and `skills-lock.json` for focused owner, agent, planning
  contract, Planning State, and temporary helper installation only
- `tests/test_plan_batch.py`
- `tests/fixtures/plan-batch/**`
- planning and planning-quality scenario/catalog/adapter/test surfaces
- focused manifest and routing-owner tests
- `CHANGELOG.md`

`scripts/planning_contract.py`, planning schemas, APR, Batch Runway, work-batch,
and `add-to-ledger` are read-only in this slice.

### Work

- Replace the thin plan-batch router with the complete human command-owner
  procedure and explicit direct planner/reviewer orchestration.
- Add registered `batch_planner` and `batch_plan_reviewer` TOMLs with disjoint
  capabilities and machine-readable result contracts.
- Implement `scripts/plan_batch.py` as the deterministic validation and DEC-038
  application boundary described above.
- Make the candidate `plan-batch` feature install its script and require only
  planning contracts, Planning Artifacts, Planning State, and registered custom
  agents. Do not use APR or Batch Runway as a semantic or runtime planning owner.
- Move only the unchanged temporary cross-checkout helper installation link to the
  existing `planning-state` feature when needed to remove the Batch Runway
  dependency. Preserve its behavior and deletion condition.
- Bind all planning and planning-quality CCFG-23 scenarios to the installed
  `plan-batch` owner rather than fixture-only selection behavior. Keep collaborator
  injection only where it proves direct independent-role inputs without becoming
  a second owner.
- Prove current/validate guards, existing selected/queued/active refusal, one
  finding only, minimum viable scope, semantic slices, approval scope, direct role
  invocation, correction routing, repeated-finding stop, stale-draft rejection,
  unresolved-decision rejection, exact review-basis binding, atomic queue gating,
  partial failure recovery, exact replay, and stop-before-implementation.

### Acceptance

- Candidate-installed `plan-batch` is the sole normal planning decision and queue
  mutation route.
- The default command owner directly invokes both registered roles; neither role
  can invoke the other or mutate state.
- A clean exact-draft reviewer result and proportionate or explicitly approved
  residual complexity are mandatory before DEC-038 application.
- One cohesive slice and one justified producer/consumer split queue successfully;
  filler decomposition and unjustified expansion block without queue mutation.
- Blocked and stale drafts remain non-executable and do not appear selected,
  queued, or active to Planning State or work-batch.
- Interrupted DEC-038 stages resume exactly and replay without duplicate effects.
- The installed owner writes only the canonical current, dispatch, runway, and
  selection-transaction paths authorized by the request.
- No semantic change exists in planning contracts, Planning State, APR, Batch
  Runway, work-batch, or add-to-ledger.

### Focused Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_planning_contract_schema.py \
  tests/test_planning_contract_store.py \
  tests/test_planning_contract_artifacts.py \
  tests/test_planning_transaction.py \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_catalog.py \
  tests/test_codex_features_manifest.py \
  tests/test_skill_routing_rule_ownership.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/ruff check --no-cache scripts/plan_batch.py tests/test_plan_batch.py tests/fixtures/command-owner-scenarios
.venv/bin/basedpyright scripts/plan_batch.py tests/test_plan_batch.py
.venv/bin/python scripts/install_codex_config.py --manifest codex-features.json --feature plan-batch --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
git diff --check
```

All commands are `required-green` after the new files exist. The full manifest is
also run as a diagnostic and must contain no new failure beyond the explicitly
assigned CCFG-25/26 baseline.

Reviews: independent `runway_reviewer`, `import_topology_reviewer`, and delta-only
`test-quality-review`.

Commit: `feat: make plan-batch the planning command owner`

### Stop Conditions

- Stop on a new schema, store, queue transaction, lifecycle state, persistent draft
  store, retry token, source adapter, or compatibility wrapper.
- Stop if agent invocation moves into the script or planner/reviewer independence
  becomes prose-only.
- Stop if any queue write can occur before exact clean review and approval gates.
- Stop if target scenarios still execute only a fixture owner.
- Stop on any semantic edit to planning contracts, Planning State, APR, Batch
  Runway, work-batch, add-to-ledger, or cross-checkout helper behavior.

## Slice 2: Remove Displaced Planning Ownership

### Approval Gate

Slice 1 is committed, candidate-installed, green, and independently reviewed.
Before narrowing any surface, the coordinator records a current owner/caller
matrix proving:

- every `plan-batch` selection, grouping, prioritization, dispatch, runway, risk,
  approval, validation-profile, and queue route resolves to the new owner;
- CCFG-23 target planning scenarios have zero dependency on APR, Batch Runway,
  `create-spec`, exact prompt prose, or fixture-only planning ownership;
- APR responsibilities retained for CCFG-26 are exactly closeout and same-batch
  reconciliation support;
- Batch Runway responsibilities retained for CCFG-26 are exactly execution,
  recovery, validation, implementation review, commits, finalization, and execution
  ledger support;
- the local architecture program runner invokes the public command-owner path for
  planning and does not reimplement selection or create-spec semantics.

The coordinator may approve removal only when targeted dead-surface evidence and
an independent review agree. Ambiguous or unclassified surfaces block.

### Scope

Primary allowed areas:

- `skills/architecture-program-runway/**`
- `skills/batch-runway/**`
- `scripts/architecture_program_runner.py`
- `skills/plan-batch/**` only for replacement-consumer corrections
- focused manifest, lock, routing, workflow, runner, skill-contract, migration,
  projection-routing, scenario, and deletion-evidence tests
- `codex-features.json`, `skills-lock.json`, and `CHANGELOG.md`

The new owner implementation, planning contracts/schemas, Planning State behavior,
work-batch, execution agents, and cross-checkout helper behavior are read-only.

### Work

- Remove APR grouping, ranking, prioritization, selection, selected-dispatch,
  create-next-runway, queue-preparation, and plan-batch handoff ownership from its
  skill, agent metadata, templates, local-runner prompts, feature description, and
  tests.
- Preserve only explicitly named CCFG-26 closeout/reconciliation support. Mark each
  retained temporary surface with current callers, reason, CCFG-26 owner, and
  removal condition.
- Remove Batch Runway `create-spec` mode, create-spec semantic guidance, planning
  project-value ownership, plan-batch handoff claims, and obsolete references or
  tests. Preserve execute-spec, recovery, validation, review, finalization,
  execution contracts, and cross-checkout execution safety for CCFG-26.
- Rewire the architecture program runner's planning phase to the public
  `plan-batch` command contract without embedding a second planner. Leave execution
  and closeout phases unchanged except for references required by the new planning
  handoff.
- Remove plan-batch manifest dependencies on APR and Batch Runway and remove the
  helper installation link from Batch Runway after the unchanged link is available
  through Planning State.
- Delete or rewrite CCFG-23 fixture helpers and topology assertions that exist only
  to preserve the replaced planning owners. Keep legitimate target-behavior
  adapters with a named installed-owner caller.
- Rewrite skill/routing/migration tests to assert structural ownership and absence
  of legacy planning routes rather than exact wording.

### Acceptance

- Runtime and semantic dependencies from `plan-batch` to APR, Batch Runway, and
  `create-spec` are zero.
- APR exposes no planning lifecycle or queue authority and retains only named
  CCFG-26 support.
- Batch Runway exposes no planning or create-spec authority and retains only named
  CCFG-26 execution support.
- The architecture program runner uses `plan-batch` as its planning command owner
  and contains no duplicate selection, proportionality, review, or queue rules.
- No production or scenario caller reaches a removed planning surface.
- No CCFG-26-owned behavior is narrowed.
- The full manifest retains only the one named CCFG-26 failure.

### Focused Validation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_plan_batch.py \
  tests/test_architecture_program_runner.py \
  tests/test_command_owner_behavioral_scenarios.py \
  tests/test_command_owner_scenario_catalog.py \
  tests/test_codex_features_manifest.py \
  tests/test_skill_routing_rule_ownership.py \
  tests/test_skill_contract_catalog.py \
  tests/test_skill_contract_migration.py \
  tests/test_planning_state_consumer_projection_routing.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/skill_contract.py validate --root .
.venv/bin/ruff check --no-cache scripts/architecture_program_runner.py scripts/plan_batch.py tests
.venv/bin/basedpyright scripts/architecture_program_runner.py scripts/plan_batch.py
git diff --check
```

All focused commands: `required-green`. The full manifest diagnostic may remain red
only for `test_work_batch_reconciles_same_batch_closeout`.

Reviews: targeted `dead-surface-audit`, `import_topology_reviewer`, independent
`runway_reviewer`, and delta-only `test-quality-review`.

Commit: `refactor: remove legacy planning ownership`

### Stop Conditions

- Stop if any proposed removal lacks a current caller inventory and replacement
  evidence.
- Stop if CCFG-26 execution, closeout, recovery, review, commit, or reconciliation
  behavior would be removed or altered.
- Stop if the runner needs a new public protocol, bridge, or duplicate planning
  implementation.
- Stop if helper behavior or Planning State semantic authority would change.
- Stop on a migration guard that can turn green only by preserving obsolete names,
  imports, or topology.

## Slice 3: Converge Installation And Final Acceptance

### Scope

Reconcile the final candidate generation and prove complete CCFG-25 acceptance.
Allowed areas are the batch scope, limited to corrections required by final
installation, exact acceptance, documentation, and review. No new semantic design
is allowed.

### Work

- Converge `codex-features.json`, `skills-lock.json`, installed skill/script/agent
  links, versions, routing docs, workflow guide, README, and changelog around the
  final owner topology.
- Install the complete candidate generation into an isolated candidate Codex home
  from a clean target and verify every managed link resolves to candidate source.
- Verify stable Codex home status is byte-for-byte unchanged before and after the
  candidate installation.
- Run the exact-commit CCFG-33 acceptance path with one evidence-pytest process.
- Prove every COR-008 and planning-quality key, the two former CCFG-25 manifest
  failures green, the one CCFG-26 failure still classified and unchanged, and zero
  forbidden target topology in target scenarios.
- Perform final exact-range independent, import-topology, dead-surface, and
  delta-only test-quality reviews.
- Record cost evidence: files changed, additions/deletions, diff bytes, focused and
  exact acceptance time, pytest process count, and context usage when available.

### Acceptance

```yaml
planning_quality:
  default_agent_is_only_queue_mutator: true
  registered_batch_planner: true
  registered_batch_plan_reviewer: true
  planner_cannot_invoke_reviewer: true
  reviewer_receives_independent_source_evidence: true
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
- Target planning scenarios contain none of the forbidden legacy terms as required
  by their topology-independent contract.
- APR and Batch Runway retained surfaces are only the exact CCFG-26 temporary
  responsibilities with named deletion conditions.
- Candidate code cannot mutate canonical planning state during fixture or isolated
  installation validation.
- Stable/default generation remains unchanged.

### Final Validation

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
  tests/test_codex_features_manifest.py \
  tests/test_skill_routing_rule_ownership.py \
  tests/test_skill_contract_catalog.py \
  tests/test_skill_contract_migration.py \
  tests/test_planning_state_consumer_projection_routing.py
.venv/bin/python scripts/command_owner_scenarios.py validate tests/fixtures/command-owner-scenarios
.venv/bin/python scripts/skill_contract.py validate --root .
.venv/bin/ruff check --no-cache .
.venv/bin/basedpyright
.venv/bin/python scripts/install_codex_config.py --manifest codex-features.json --all-features --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
git diff --check
```

Then run the repository's CCFG-33 exact-commit acceptance command against the final
candidate commit with one evidence-pytest process. Preserve its canonical report
hash and generated report hash. Run the complete manifest diagnostic and broad
legacy/projection diagnostic; only the exact preclassified CCFG-26 identities may
remain red.

All final gates are `required-green` except the explicitly retained CCFG-26
`known-red-baseline`.

Reviews: final exact-range `runway_reviewer`, `import_topology_reviewer`, targeted
`dead-surface-audit`, and delta-only `test-quality-review`.

Commit: `chore: complete plan-batch ownership transfer`

### Stop Conditions

- Stop on any new semantic decision, schema, bridge, compatibility wrapper, public
  mode, or owner not already authorized by this runway.
- Stop if exact acceptance requires preserving legacy planning topology or exact
  prompt prose.
- Stop if stable-home state changes, candidate code writes canonical planning
  state, strict context is not ready, or candidate HEAD moves unexpectedly.
- Stop if the final manifest contains a new failure or any CCFG-25 failure.
- Stop if CCFG-25 cannot close while CCFG-26 remains unselected.

## Final Closeout

After all slices are committed and every final gate is satisfied:

1. write `completed-slices.md` and `closeout.md` in this batch directory;
2. record exact candidate range, stable planning receipts, transaction recovery,
   installed links, removed/preserved surface inventory, validation, reviews, and
   cost evidence;
3. mark CCFG-25 `Closed` in the program ledger;
4. clear selected dispatch, queued runway, and active runway for this batch;
5. set latest closeout to this batch;
6. leave CCFG-26 through CCFG-29 open and unselected;
7. stop without selecting or preparing a successor.
