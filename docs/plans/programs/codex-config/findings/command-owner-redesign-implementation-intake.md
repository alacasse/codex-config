# Command-Owner Redesign Implementation Intake

## Source

- Source identity: `COR-001` through `COR-012`
- Source branch: `architecture/command-owner-redesign`
- Source commit: `b3f31c44a1fc3287c33dd2955489f194afef66f6`
- Authoritative packet:
  [07-implementation-ledger-intake.md](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md)
- Accepted decisions:
  [decisions.md](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/decisions.md)
- Migration program:
  [04-migration-program.md](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/04-migration-program.md)
- State when ingested: every item is `Open` and unselected

## Intake Boundary

This note preserves the implementation packet as twelve individually
addressable program findings. It is not a batch map, dispatch, runway, slice
list, or implementation plan. A future `plan-batch` invocation retains
authority to select, split, narrow, group, block, or defer at most one eligible
item from current ledger state.

Every item inherits these constraints:

- use the accepted decisions and phase order from the redesign package;
- preserve behavior contracts rather than legacy skill topology;
- keep the stable generation in control of canonical state before cutover;
- finalize `skill-authoring` v1 before migrating a target command owner;
- remove corresponding legacy ownership in the same ownership-transfer work;
- name every temporary bridge and its deletion condition;
- stop after same-batch closeout without selecting successor work;
- do not add permanent parallel commands, `skills-v2`, or parallel execution.

## Ledger Mapping

| Source item | Ledger finding | Dependencies |
|---|---|---|
| `COR-001` | `CCFG-18` | None |
| `COR-002` | `CCFG-19` | `CCFG-18` (`COR-001`) |
| `COR-003` | `CCFG-20` | `CCFG-19` (`COR-002`) |
| `COR-004` | `CCFG-21` | `CCFG-19` (`COR-002`) |
| `COR-005` | `CCFG-22` | `CCFG-20`, `CCFG-21` (`COR-003`, `COR-004`) |
| `COR-006` | `CCFG-23` | `CCFG-21`, `CCFG-22` (`COR-004`, `COR-005`) |
| `COR-007` | `CCFG-24` | `CCFG-22`, `CCFG-23` (`COR-005`, `COR-006`) |
| `COR-008` | `CCFG-25` | `CCFG-24` (`COR-007`) |
| `COR-009` | `CCFG-26` | `CCFG-25` (`COR-008`) |
| `COR-010` | `CCFG-27` | `CCFG-26` (`COR-009`) |
| `COR-011` | `CCFG-28` | `CCFG-27` (`COR-010`) |
| `COR-012` | `CCFG-29` | `CCFG-28` (`COR-011`) |

<a id="cor-001"></a>
## CCFG-18 / COR-001 — Establish Stable and Candidate Generations

- Exact source:
  [COR-001](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-001--establish-stable-and-candidate-generations)
- Purpose: create a proven control boundary before modifying skills that are
  actively used to plan and execute the migration.
- Included: identify the stable checkout and default `CODEX_HOME`; create a
  separate candidate clone and candidate `CODEX_HOME`; prove generation and
  source identity in fresh sessions; prove the stable toolchain edits the
  candidate without self-mutation; document switching and rollback; inspect
  selected, queued, active, and resumable state; evaluate a worktree only as an
  optional bounded experiment.
- Excluded: target skill rewrites, schema implementation, ledger-format
  migration, candidate-generation canonical-state mutation, and cutover.
- Dependencies: none.
- Decisions: `DEC-011`, `DEC-025`, `DEC-026`.
- Behavior contracts: `STATE-DIAG-001`, `STATE-TRANSITION-002`,
  `STATE-HISTORY-004`.

Acceptance evidence:

```yaml
stable_checkout_unchanged: true
stable_generation_identity_proven: true
candidate_checkout_isolated: true
candidate_codex_home_isolated: true
candidate_generation_identity_proven: true
stable_can_edit_candidate_without_self_mutation: true
selected_old_generation_dispatch: null
queued_old_generation_runway: null
active_old_generation_runway: null
resumable_old_runner_state: false
rollback_documented: true
```

Stop/planning boundary: a separate clone is the default. `plan-batch` may split
environment creation from validation only when one runway would mix unrelated
machine setup and repository verification; it must not assume worktree support.

<a id="cor-002"></a>
## CCFG-19 / COR-002 — Verify Source Contracts and Resolve Blocking Decisions

- Exact source:
  [COR-002](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-002--verify-source-contracts-and-resolve-blocking-decisions)
- Purpose: verify that accepted behavior contracts and target ownership are
  complete enough to guide implementation without preserving accidental
  topology.
- Included: review current skills, tests, manifests, agents, state tooling, and
  active artifacts against the source behavior contracts and target ownership
  model; classify tests; identify accidental structure and duplicate rule
  ownership; resolve blocking decisions; leave non-blocking naming and
  presentation decisions open.
- Excluded: target skill rewrites, parser/schema implementation, active ledger
  mutation beyond same-item closeout, and later-phase implementation.
- Dependencies: `CCFG-18` (`COR-001`).
- Decisions: `DEC-001` through `DEC-010`, `DEC-013` through `DEC-020`,
  `DEC-022` through `DEC-026`, and `OPEN-001` through `OPEN-003`.
- Behavior contracts: every contract in `01-source-behavior-contracts.md`.

Acceptance evidence:

```yaml
external_behavior_contracts_have_ids: true
each_target_decision_has_one_owner: true
accidental_source_structure_identified: true
test_classification_complete_enough_for_harness: true
blocking_open_decisions_resolved_or_explicitly_gated: true
```

Stop/planning boundary: `plan-batch` may narrow this item to one blocking
decision or evidence gap when full verification would require unresolved
implementation discovery.

<a id="cor-003"></a>
## CCFG-20 / COR-003 — Implement `skill-contract/v1` Schema and Validators

- Exact source:
  [COR-003](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-003--implement-skill-contractv1-schema-and-validators)
- Purpose: create the mechanically enforceable contract foundation for hybrid
  skills and `skill-authoring` v1.
- Included: define and parse the canonical `skill-contract/v1` block; validate
  required fields, ownership, delegation, dependencies, writes, forbids,
  outputs, stop conditions, and references; detect duplicate ownership,
  unknown targets, cycles, retired-owner dependencies, and cosmetic
  migrations; add malformed and ownership-focused tests; emit actionable
  errors.
- Excluded: command-owner migrations, planning-artifact parsing, and
  candidate-generation control of real work.
- Dependencies: `CCFG-19` (`COR-002`).
- Decisions: `DEC-001`, `DEC-002`, `DEC-008`, `DEC-009`, `DEC-010`,
  `DEC-015`, `DEC-024`.
- Behavior contracts: `STATE-CANONICAL-003` plus ownership implications across
  intake, planning, execution, and closeout contracts.

Acceptance evidence:

```yaml
skill_contract_v1_parseable: true
required_field_validation: green
ownership_conflict_detection: green
dependency_and_reference_validation: green
retired_owner_dependency_detection: green
cosmetic_migration_detection: green
```

Stop/planning boundary: parser/schema work may be split from repository-wide
ownership checks only when the seams are independently testable; the working
schema and core validator must still precede `skill-authoring`.

<a id="cor-004"></a>
## CCFG-21 / COR-004 — Implement Planning Artifact Schemas and Validators

- Exact source:
  [COR-004](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-004--implement-planning-artifact-schemas-and-validators)
- Purpose: make active dispatch, runway, execution-evidence, and closeout facts
  canonical structured contracts inside readable Markdown artifacts.
- Included: define `planning-dispatch/v1`, `planning-runway/v1`, and
  `planning-closeout/v1`; parse embedded blocks; validate identity, lineage,
  revisions, lifecycle, dependencies, risks, approvals, write scopes,
  validation classes, results, recovery, and closeout; enforce canonical fact
  ownership; prototype a synthetic vertical chain; define read-only
  compatibility for active old-format artifacts.
- Excluded: historical-archive migration, parallel execution, canonical
  SQLite state, and workflow-ownership transfers.
- Dependencies: `CCFG-19` (`COR-002`).
- Decisions: `DEC-007`, `DEC-008`, `DEC-010`, `DEC-016`, `DEC-022`,
  `DEC-023`, and `OPEN-001` through `OPEN-005`.
- Behavior contracts: `PLAN-DISPATCH-005`, `PLAN-RUNWAY-006`,
  `PLAN-RISK-007`, `EXEC-RESUME-002`, `EXEC-VALIDATE-004`,
  `EXEC-REVIEW-005`, `EXEC-COMMIT-006`, `CLOSE-FINAL-001`,
  `CLOSE-RECONCILE-002`, `STATE-TRANSITION-002`, `STATE-CANONICAL-003`.

Acceptance evidence:

```yaml
planning_dispatch_v1_parseable: true
planning_runway_v1_parseable: true
planning_closeout_v1_parseable: true
canonicality_validation: green
lineage_and_dependency_validation: green
synthetic_vertical_chain: green
old_format_compatibility_policy: explicit_and_read_only
```

Stop/planning boundary: dispatch, runway, and closeout schema work may be split
only while preserving compatible versioning and the required vertical
prototype.

<a id="cor-005"></a>
## CCFG-22 / COR-005 — Finalize and Validate `skill-authoring` v1

- Exact source:
  [COR-005](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-005--finalize-and-validate-skill-authoring-v1)
- Purpose: provide the repository-specific authoring workflow before any
  target command owner is migrated.
- Included: create the skill at its canonical path; make it authoritative for
  hybrid structure, ownership contracts, canonicality, procedure/decision/
  rationale separation, ambiguity reporting, migration rules, and reference
  splitting; define its boundary with generic guidance; invoke validators;
  block cosmetic migration and silent conflict resolution; validate on
  `port-by-contract` or an equivalent skill; install only in the candidate
  `CODEX_HOME` before cutover.
- Excluded: command-owner migrations, runtime dependency from command owners,
  and hidden inheritance/include systems.
- Dependencies: `CCFG-20`, `CCFG-21` (`COR-003`, `COR-004`).
- Decisions: `DEC-008`, `DEC-009`, `DEC-010`, `DEC-024`, `DEC-026`.
- Behavior contracts: `STATE-CANONICAL-003` plus target ownership implications
  across all command contracts.

Acceptance evidence:

```yaml
skill_authoring_v1_complete: true
skill_authoring_v1_schema_valid: true
generic_authoring_boundary_documented: true
ambiguity_and_conflict_reporting: green
cosmetic_migration_guard: green
representative_skill_trial: green
installed_only_in_candidate_codex_home: true
canonical_state_mutation_during_trial: false
```

Stop/planning boundary: a representative trial may be narrowed, but no target
command-owner migration may be selected before the full v1 completion standard
is met.

<a id="cor-006"></a>
## CCFG-23 / COR-006 — Build the Topology-Independent Behavioral Scenario Harness

- Exact source:
  [COR-006](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-006--build-the-topology-independent-behavioral-scenario-harness)
- Purpose: prove workflow behavior independently from legacy skill names,
  prose, modes, and dependency topology.
- Included: isolated planning-root fixtures for intake, selection, scope,
  dispatch, runway, execution, validation, review, commit, recovery, resume,
  closeout, reconciliation, and no-successor behavior; assert canonical initial
  facts, public command, transitions, writes, forbidden writes, stops, and
  evidence; characterize source behavior and define the target interface; keep
  candidate scenarios away from canonical planning state.
- Excluded: command-owner migration, exact-prose preservation, retired-owner
  installation requirements, and active planning-root mutation.
- Dependencies: `CCFG-21`, `CCFG-22` (`COR-004`, `COR-005`).
- Decisions: `DEC-015`, `DEC-018`, `DEC-019`, `DEC-020`, `DEC-026`.
- Behavior contracts: every contract in `01-source-behavior-contracts.md`.

Acceptance evidence:

```yaml
source_characterization_scenarios_green: true
target_scenario_interface_defined: true
expectations_independent_of_legacy_skill_names: true
negative_write_assertions_present: true
active_planning_root_untouched: true
```

Stop/planning boundary: the harness may be split by command family only when
fixtures and validation stay composable and the eventual deletion test covers
the complete workflow.

<a id="cor-007"></a>
## CCFG-24 / COR-007 — Transfer Intake Ownership to `add-to-ledger`

- Exact source:
  [COR-007](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-007--transfer-intake-ownership-to-add-to-ledger)
- Purpose: make `add-to-ledger` the sole owner of intake semantics and
  canonical ledger mutation.
- Included: use `skill-authoring` v1; preserve source identity, individual
  addressability, idempotence, and revision-checked mutation; implement or
  complete a narrow ledger store; remove APR intake and normalization
  authority, the `legacy-removal` program-owner escape hatch, APR command
  dependency for intake, and topology tests that preserve APR intake ownership.
- Excluded: batch selection, dispatch/runway creation, and planning/execution
  ownership migration.
- Dependencies: `CCFG-22`, `CCFG-23` (`COR-005`, `COR-006`).
- Decisions: `DEC-001`, `DEC-002`, `DEC-014`, `DEC-015`, `DEC-016`,
  `DEC-019`, `DEC-024`.
- Behavior contracts: `INTAKE-SOURCE-001`, `INTAKE-IDENTITY-002`,
  `INTAKE-NORMALIZE-003`, `INTAKE-MUTATE-004`, `INTAKE-STOP-005`,
  `STATE-TRANSITION-002`.

Acceptance evidence:

```yaml
add_to_ledger_owns_intake_decisions: true
add_to_ledger_broad_workflow_dependencies: 0
add_to_ledger_contract_validates: true
apr_intake_decisions_owned: 0
legacy_removal_program_owner_escape_hatch: false
intake_behavior_scenarios: green
```

Stop/planning boundary: split only when the ledger-store mechanism is a
separately useful prerequisite; no split may leave APR and `add-to-ledger` as
two normal owners.

<a id="cor-008"></a>
## CCFG-25 / COR-008 — Transfer Planning Ownership to `plan-batch`

- Exact source:
  [COR-008](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-008--transfer-planning-ownership-to-plan-batch)
- Purpose: make `plan-batch` the sole owner of selection, scope shaping,
  dispatch, runway specification, risk, and validation-profile decisions.
- Included: use `skill-authoring` v1; move planning references under
  `plan-batch`; produce hybrid dispatch and runway artifacts; replace APR and
  Batch Runway planning dependencies with narrow mechanisms; remove APR
  grouping, prioritization, selection, dispatch, and normal queue authority;
  remove Batch Runway create-spec, slice-design, and validation-selection
  authority; remove topology tests; retain only caller-scoped read-only active
  artifact compatibility.
- Excluded: slice execution, closeout transfer, runner cutover, and historical
  archive migration.
- Dependencies: `CCFG-24` (`COR-007`).
- Decisions: `DEC-001`, `DEC-002`, `DEC-005`, `DEC-006`, `DEC-007`,
  `DEC-014`, `DEC-015`, `DEC-016`, `DEC-024`, `DEC-025`.
- Behavior contracts: `PLAN-SOURCE-001`, `PLAN-ACTIVE-002`,
  `PLAN-SELECT-003`, `PLAN-SCOPE-004`, `PLAN-DISPATCH-005`,
  `PLAN-RUNWAY-006`, `PLAN-RISK-007`, `PLAN-STOP-008`, `STATE-DIAG-001`,
  `STATE-TRANSITION-002`.

Acceptance evidence:

```yaml
plan_batch_owns_candidate_selection: true
plan_batch_owns_scope_shaping: true
plan_batch_owns_dispatch_definition: true
plan_batch_owns_runway_specification: true
plan_batch_owns_validation_profile_selection: true
plan_batch_apr_dependency: false
plan_batch_batch_runway_dependency: false
apr_planning_decisions_owned: 0
batch_runway_create_spec_callers: 0
target_planning_scenarios: green
```

Stop/planning boundary: preparatory mechanism work may be selected separately
only when the dispatch names the immediate ownership transfer still required;
the item is not complete while a legacy owner remains an equally valid route.

<a id="cor-009"></a>
## CCFG-26 / COR-009 — Transfer Execution and Closeout Ownership to `work-batch`

- Exact source:
  [COR-009](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-009--transfer-execution-and-closeout-ownership-to-work-batch)
- Purpose: make `work-batch` the sole owner of execution lifecycle, recovery,
  acceptance, finalization, closeout, and same-batch reconciliation.
- Included: use `skill-authoring` v1; move execution, recovery, finalization,
  and retention references under `work-batch`; retain narrow independent worker
  and reviewer roles; produce hybrid receipts and closeouts; remove Batch
  Runway execute-spec, recovery, finalization, and commit-workflow authority;
  remove APR closeout and reconciliation authority; preserve no-successor
  behavior; replace topology tests; complete or explicitly migrate active
  old-format execution state before cutover.
- Excluded: intake, successor planning, runner installation cutover, and
  immediate physical deletion of every legacy directory.
- Dependencies: `CCFG-25` (`COR-008`).
- Decisions: `DEC-001`, `DEC-002`, `DEC-006`, `DEC-014`, `DEC-015`,
  `DEC-016`, `DEC-018`, `DEC-019`, `DEC-020`, `DEC-024`.
- Behavior contracts: `EXEC-CURRENT-001`, `EXEC-RESUME-002`,
  `EXEC-WORKER-003`, `EXEC-VALIDATE-004`, `EXEC-REVIEW-005`,
  `EXEC-COMMIT-006`, `EXEC-RECOVER-007`, `EXEC-STOP-008`,
  `CLOSE-FINAL-001`, `CLOSE-RECONCILE-002`, `CLOSE-NEXT-003`,
  `STATE-TRANSITION-002`.

Acceptance evidence:

```yaml
work_batch_owns_execution_lifecycle: true
work_batch_owns_recovery: true
work_batch_owns_closeout: true
work_batch_owns_same_batch_reconciliation: true
work_batch_apr_dependency: false
work_batch_batch_runway_dependency: false
batch_runway_execute_spec_callers: 0
apr_closeout_decisions_owned: 0
target_execution_and_closeout_scenarios: green
```

Stop/planning boundary: execution seams may be split only when each batch
removes a named legacy decision and any remaining dual ownership is explicitly
blocked from normal use.

<a id="cor-010"></a>
## CCFG-27 / COR-010 — Cut Over Runner, Manifest, Agents, and Installation

- Exact source:
  [COR-010](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-010--cut-over-runner-manifest-agents-and-installation)
- Purpose: make installed surfaces consume only public target commands and
  safely switch the default toolchain to the candidate generation.
- Included: remove legacy owners from command-owner feature dependencies;
  separate runner installation from APR; replace old-mode runner instructions
  with public plan/work protocols; update active docs, feature descriptions,
  agents, and installation; run candidate fixture workflows; prove rollback;
  prove no old-generation active or resumable state; switch installation as the
  final action; finish the stable controlling session unchanged; start a fresh
  candidate diagnostic.
- Excluded: runner-owned backlog selection, runner-owned slice design, and
  deletion of all legacy directories before the target generation is current.
- Dependencies: `CCFG-26` (`COR-009`).
- Decisions: `DEC-011`, `DEC-016`, `DEC-017`, `DEC-018`, `DEC-026`.
- Behavior contracts: `PLAN-STOP-008`, `EXEC-CURRENT-001`, `CLOSE-NEXT-003`,
  `STATE-DIAG-001`, `STATE-TRANSITION-002`, `STATE-HISTORY-004`.

Acceptance evidence:

```yaml
command_owner_manifest_legacy_dependencies: 0
runner_prompts_using_old_modes: 0
runner_installation_owned_by_apr_feature: false
candidate_full_fixture_workflow: green
no_old_generation_active_state: true
rollback_to_stable: proven
fresh_candidate_generation_diagnostic: green
default_toolchain_generation: candidate
```

Stop/planning boundary: preparatory manifest/runner work may be split from the
final switch; the switch must remain a bounded rollback-capable batch with no
active old-generation state.

<a id="cor-011"></a>
## CCFG-28 / COR-011 — Delete Architecture Program Runway and Batch Runway

- Exact source:
  [COR-011](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-011--delete-architecture-program-runway-and-batch-runway)
- Purpose: physically remove retired broad owners and migration-only topology
  after the target generation is current.
- Included: delete both legacy skill directories after moving surviving
  references; delete old modes and direct-command metadata, topology tests,
  expired transition fixtures, and expired parsers; remove duplicate rules and
  vocabulary; preserve clearly archived history; rerun target scenarios after
  physical deletion.
- Excluded: replacement compatibility wrappers, historical archive rewrites,
  and behavior narrowing without an accepted decision.
- Dependencies: `CCFG-27` (`COR-010`).
- Decisions: `DEC-005`, `DEC-006`, `DEC-014`, `DEC-015`, `DEC-016`,
  `DEC-022`.
- Behavior contracts: every target behavior contract plus
  `STATE-HISTORY-004`.

Acceptance evidence:

```yaml
architecture_program_runway_directory_exists: false
batch_runway_directory_exists: false
active_old_mode_references: 0
tests_requiring_old_owner_presence: 0
active_legacy_artifacts: 0
target_behavioral_scenarios: green
```

Stop/planning boundary: deletion may be split by owner only when the remaining
owner has no normal caller and has an immediate measurable deletion condition.

<a id="cor-012"></a>
## CCFG-29 / COR-012 — Perform Contract-First Authoring Convergence

- Exact source:
  [COR-012](https://github.com/alacasse/codex-config/blob/architecture/command-owner-redesign/docs/design/command-owner-redesign/07-implementation-ledger-intake.md#cor-012--perform-contract-first-authoring-convergence)
- Purpose: audit completed target skills and refine the already-authoritative
  `skill-authoring` v1 after dogfooding.
- Included: audit `port-by-contract`, `add-to-ledger`, `plan-batch`, and
  `work-batch`; collect migration findings; integrate compatible optional-field,
  report-layout, size-heuristic, reference-loading, and non-breaking validation
  refinements; remove temporary authoring exceptions and per-skill dialects;
  record semantic changes as explicit schema decisions.
- Excluded: recreating retired owners, unrelated workflow redesign, and silent
  `skill-contract/v2` semantics.
- Dependencies: `CCFG-28` (`COR-011`).
- Decisions: `DEC-008`, `DEC-009`, `DEC-010`, `DEC-024`.
- Behavior contracts: `STATE-CANONICAL-003` plus all command-owner contracts
  as audit evidence.

Acceptance evidence:

```yaml
contract_first_target_skills_consistent: true
temporary_authoring_exceptions: 0
per_skill_contract_dialects: 0
skill_authoring_v1_convergence_audit: passed
```

Stop/planning boundary: audit and compatible cleanup may be split, but semantic
contract changes require a separate explicit ledger item and accepted decision.
