# Decision Register

## Purpose

This register separates accepted target decisions from deferred ideas, rejected
approaches, superseded decisions, and questions that still require explicit
human input.

Priority order for redesign work:

```text
accepted decisions in this register
-> current migration phase contract
-> stable behavior contract IDs
-> target ownership model
-> ledger work item linked from 07-implementation-ledger-intake.md
-> selected implementation dispatch and runway
-> repository source evidence
-> GitHub issues and historical plans
-> conversation transcripts
```

An agent must not silently resolve an `open` decision, revive a rejected
approach, or follow a superseded decision because it appears in historical
source material.

## Status Values

```yaml
status_values:
  - accepted
  - open
  - deferred
  - rejected
  - superseded
```

## Accepted Decisions

### DEC-001 — Human command owners are the target workflow owners

```yaml
id: DEC-001
status: accepted
decision: >-
  add-to-ledger owns intake, plan-batch owns planning, and work-batch owns
  execution plus same-batch closeout.
consequences:
  - architecture-program-runway is decomposed and deleted
  - batch-runway is split and deleted
  - command owners may remain concise but must own semantic decisions
```

### DEC-002 — Delegation is allowed; duplicate ownership is not

```yaml
id: DEC-002
status: accepted
decision: >-
  Command owners may delegate diagnostics, state application, path resolution,
  schema validation, worker execution, review, and commit mechanics. A delegated
  support surface may not independently reinterpret the same human workflow.
```

### DEC-003 — `planning-state` is a narrow state-machine authority

```yaml
id: DEC-003
status: accepted
decision: >-
  planning-state owns normalized diagnostics, lifecycle invariants, explicit
  transition validation, revision checks, serialization, and receipts. It does
  not select findings, shape batches, design slices, choose recovery actions, or
  select successors.
```

### DEC-004 — `planning-artifacts` owns structure, not lifecycle

```yaml
id: DEC-004
status: accepted
decision: >-
  planning-artifacts owns canonical paths, artifact types, co-location, lineage,
  and archives. Lifecycle transitions and semantic workflow decisions live
  elsewhere.
```

### DEC-005 — Architecture Program Runway has no final target role

```yaml
id: DEC-005
status: accepted
decision: >-
  architecture-program-runway is a source implementation to decompose, not a
  target program-level owner or permanent compatibility wrapper.
removal_target: skills/architecture-program-runway
```

### DEC-006 — Batch Runway is split by workflow ownership and deleted

```yaml
id: DEC-006
status: accepted
decision: >-
  Runway specification and validation selection move to plan-batch. Execution,
  recovery, finalization, and closeout move to work-batch. Surviving narrow
  references move under those owners, then skills/batch-runway is deleted.
removal_target: skills/batch-runway
```

### DEC-007 — The dispatch remains a separate durable artifact

```yaml
id: DEC-007
status: accepted
decision: >-
  Keep a separate dispatch between ledger selection and runway specification.
rationale: >-
  It records the stable selection and scope decision, supports fresh-session
  handoff and revision binding, and does not require a separate workflow owner.
```

### DEC-008 — Contract-first hybrid Markdown is the initial representation

```yaml
id: DEC-008
status: accepted
decision: >-
  Skills and active planning artifacts use one versioned embedded YAML contract
  block plus concise Markdown procedure, rationale, and context.
source_proposals:
  - GitHub issue #48
  - GitHub issue #50
```

### DEC-009 — Skill contracts do not move into frontmatter

```yaml
id: DEC-009
status: accepted
decision: >-
  Preserve minimal discovery frontmatter and place the operational skill contract
  under a stable `## Contract` heading.
```

### DEC-010 — Structured machine facts are canonical

```yaml
id: DEC-010
status: accepted
decision: >-
  Each machine-relevant fact has one canonical structured owner. Prose may
  explain or summarize but may not independently redefine operational values.
consequences:
  - duplicate status and dependency definitions are invalid
  - derived artifacts declare source artifact and revision
  - SQLite remains derived and rebuildable
```

### DEC-011 — No permanent parallel skill directory

```yaml
id: DEC-011
status: accepted
decision: >-
  Do not create permanent skills-v2, skills-next, or version-suffixed human
  commands. Develop target skills at final skills/<name>/ paths in an isolated
  candidate checkout with a separate CODEX_HOME.
```

### DEC-013 — Limit `port-by-contract` during redesign bootstrap

```yaml
id: DEC-013
status: accepted
decision: >-
  Use intake-source, distill-contract, and design-target reasoning. Do not use
  create-port-runway during redesign bootstrap because the current runway skills
  are source implementation being replaced.
```

### DEC-014 — Migration phases must remove legacy ownership

```yaml
id: DEC-014
status: accepted
decision: >-
  A migration phase is incomplete if it only adds a target surface while the old
  owner remains an equally valid normal path. Each transfer phase removes or
  narrows named legacy decisions in the same phase.
```

### DEC-015 — Behavior tests outrank topology tests

```yaml
id: DEC-015
status: accepted
decision: >-
  Preserve externally meaningful behavior, schema, state, file effects, and
  workflow integration. Rewrite or delete tests that only preserve old skills,
  modes, dependency lists, phrases, aliases, or wrappers.
```

### DEC-016 — Temporary compatibility must expire

```yaml
id: DEC-016
status: accepted
decision: >-
  Every temporary bridge or legacy parser names a caller, reason, owner, allowed
  scope, and measurable deletion condition. Coexistence is not completion.
```

### DEC-017 — The runner orchestrates public commands

```yaml
id: DEC-017
status: accepted
decision: >-
  The runner may invoke plan-batch and work-batch, enforce explicit loop bounds,
  and own process, sandbox, telemetry, and stop-policy concerns. It does not own
  selection semantics, slice design, execution acceptance, or closeout meaning.
```

### DEC-018 — Same-batch closeout never selects a successor

```yaml
id: DEC-018
status: accepted
decision: >-
  work-batch reconciles only the completed batch and stops. A later explicit
  plan-batch request or runner loop iteration owns successor planning.
```

### DEC-019 — Specialized review skills remain evidence producers

```yaml
id: DEC-019
status: accepted
decision: >-
  legacy-removal, dead-surface-audit, and test-quality-review do not own normal
  queue, selection, execution, commit, or closeout state.
consequences:
  - remove the legacy-removal program-owner escape hatch
  - retain dead-surface canonical evidence vocabulary
  - retain independent test-quality evidence
```

### DEC-020 — Worker and reviewer authority separation is preserved

```yaml
id: DEC-020
status: accepted
decision: >-
  Implementation and independent review remain separate delegated roles. The
  worker cannot review or commit its own work; the reviewer remains read-only;
  work-batch owns lifecycle coordination.
```

### DEC-022 — Historical artifacts are not rewritten by default

```yaml
id: DEC-022
status: accepted
decision: >-
  Clearly archived historical artifacts may retain old names and formats. Active
  pickup state and new artifacts must use the target contracts. Legacy readers
  are temporary and read-only.
```

### DEC-023 — Parallel execution is not part of this program

```yaml
id: DEC-023
status: accepted
decision: >-
  Schemas may represent explicit slice dependencies and write scopes so future
  conservative parallel scheduling remains possible, but this migration does not
  implement parallel execution, worktree scheduling, locking, or merge policy.
source_proposal: GitHub issue #50
```

### DEC-024 — Finalize `skill-authoring` v1 before command-owner migrations

```yaml
id: DEC-024
status: accepted
supersedes:
  - DEC-021
decision: >-
  Define, implement, validate, and treat skill-authoring v1 as authoritative in
  phase 2 before add-to-ledger, plan-batch, or work-batch are migrated. Use it to
  guide those migrations, then perform a final convergence audit after dogfooding.
rationale: >-
  The first target skills must not invent separate hybrid dialects or rely only on
  generic narrative-first skill guidance. Flexibility is preserved through
  versioning and later compatible refinements, not through an incomplete guide.
phase_2_completion_requires:
  - skill-contract/v1 schema accepted
  - validators implemented
  - skill-authoring v1 complete and schema-valid
  - generic authoring guidance boundary documented
  - validated on port-by-contract or an equivalent representative skill
  - installed only in the candidate CODEX_HOME until cutover
dogfood_phases:
  - phase-4-add-to-ledger-transfer
  - phase-5-plan-batch-transfer
  - phase-6-work-batch-transfer
final_convergence_phase: phase-9-contract-first-authoring-convergence
versioning_policy:
  stable_early:
    - ownership semantics
    - canonicality rules
    - required contract sections
    - migration and ambiguity guards
  refinable_compatibly:
    - optional fields
    - report presentation
    - size heuristics
    - reference-loading guidance
```

### DEC-025 — Implementation enters through ledger intake, not a prebuilt batch map

```yaml
id: DEC-025
status: accepted
decision: >-
  Convert the accepted design into individually addressable work items in
  07-implementation-ledger-intake.md, ingest all items together through
  add-to-ledger, and leave them unselected. plan-batch then selects and shapes at
  most one eligible item per invocation, and work-batch executes only that runway.
rationale: >-
  The current workflow intentionally separates multi-item intake from one-batch
  planning and execution. Predefining runnable batches in a design session would
  bypass plan-batch ownership and reduce its ability to split, block, narrow, or
  group work using current ledger state.
required_contracts:
  - INTAKE-SOURCE-001
  - INTAKE-NORMALIZE-003
  - INTAKE-STOP-005
  - PLAN-SOURCE-001
  - PLAN-SELECT-003
  - PLAN-SCOPE-004
  - PLAN-STOP-008
  - EXEC-CURRENT-001
  - CLOSE-NEXT-003
consequences:
  - 07-implementation-ledger-intake.md is not a dispatch, runway, or batch map
  - one add-to-ledger invocation may create or update all program rows
  - no row becomes selected during intake
  - dependencies and source-section links remain durable in the ledger
  - phase boundaries guide eligibility but do not predetermine slice structure
```

### DEC-026 — Stable skills bootstrap and control the candidate generation

```yaml
id: DEC-026
status: accepted
supersedes:
  - DEC-012
decision: >-
  Use the untouched stable checkout and default CODEX_HOME as the control plane
  for canonical intake, planning, and migration execution against a separate
  candidate checkout. Candidate skills use a separate CODEX_HOME and remain
  validation-only until an explicit cutover gate is satisfied.
rationale: >-
  The system is rewriting skills that it actively uses. Loading and modifying the
  same installed source during one workflow could mix generations of ownership,
  recovery, review, and closeout rules.
candidate_checkout_policy:
  default: separate_clone
  worktree: allowed_only_after_explicit_isolation_validation
session_generation_record:
  required_fields:
    - toolchain_generation
    - toolchain_source_checkout
    - target_repository_checkout
    - codex_home
    - canonical_planning_state_mutation_allowed
stable_generation_may:
  - mutate_canonical_ledger
  - create_real_dispatch_and_runway
  - execute_migration_batches_against_candidate_checkout
candidate_generation_before_cutover_may:
  - run_schema_tests
  - run_behavioral_fixtures
  - run_controlled_skill_trials
candidate_generation_before_cutover_forbids:
  - mutate_canonical_ledger
  - select_or_execute_real_migration_work
  - switch_generation_mid_command
cutover_requires:
  - no_selected_old_generation_dispatch
  - no_queued_old_generation_runway
  - no_active_old_generation_runway
  - no_resumable_old_generation_runner_state
  - target_behavioral_scenarios_green
  - rollback_to_stable_installation_documented
```

## Superseded Decisions

### DEC-012 — Use stable and candidate installation lanes

```yaml
id: DEC-012
status: superseded
superseded_by: DEC-026
previous_decision: >-
  The stable checkout and default CODEX_HOME perform and review migration work.
  The candidate branch or worktree and separate CODEX_HOME test target skills in
  fresh sessions.
reason_for_change: >-
  The original decision did not define which generation may mutate canonical
  state, did not prevent one command from mixing generations, and treated a
  worktree as equally assumed despite it not yet being proven in this workflow.
```

### DEC-021 — The skill-authoring meta-skill is implemented last

```yaml
id: DEC-021
status: superseded
superseded_by: DEC-024
previous_decision: >-
  Implement skill-authoring only after all target command owners and planning
  artifact formats have been validated.
reason_for_change: >-
  This left the first hybrid skill migrations without an authoritative
  repository-specific authoring workflow and could produce incompatible or
  cosmetic migrations.
```

## Open Decisions

### OPEN-001 — Canonical storage of current lifecycle pointers

```yaml
id: OPEN-001
status: open
question: >-
  Should selected, queued, and active pointers be canonical in a structured block
  embedded in program CURRENT.md, or in a separate structured state file with
  CURRENT.md as a generated human view?
recommended_option: embedded structured block in CURRENT.md
blocks:
  - final planning-state write interface
  - final current-state schema
```

### OPEN-002 — Ledger structured representation

```yaml
id: OPEN-002
status: open
question: >-
  Should the canonical ledger use one structured block for all findings, one
  structured block per finding, or a separate structured index plus narrative
  sections?
recommended_option: one structured canonical ledger block with compact finding records
blocks:
  - ledger-store format
  - intake mutation implementation
```

### OPEN-003 — Transaction boundary for multi-artifact planning

```yaml
id: OPEN-003
status: open
question: >-
  How should plan-batch recoverably apply dispatch creation, runway creation, and
  selected-to-queued transitions across Markdown artifacts?
recommended_option: explicit selected state followed by recoverable queue transition
blocks:
  - final plan-batch state mutation protocol
```

### OPEN-004 — Strictness of one-commit-per-slice

```yaml
id: OPEN-004
status: open
question: >-
  Is one focused commit per accepted slice universal or a default execution
  profile with explicit overrides?
recommended_option: default profile with explicit override support
```

### OPEN-005 — Exact slice-count rule

```yaml
id: OPEN-005
status: open
question: >-
  Should 3-5 slices remain a hard schema constraint, a planning warning, or only
  a documented heuristic?
recommended_option: warning-level heuristic
```

### OPEN-006 — Final names for narrow Python modules

```yaml
id: OPEN-006
status: open
question: >-
  What final module split should implement diagnostics, transitions, ledger
  mutation, artifact parsing, schemas, closeout validation, and projections?
recommended_option: decide from behavior seams during implementation design
blocks: []
```

### OPEN-007 — Worker and reviewer names

```yaml
id: OPEN-007
status: open
question: >-
  Should runway_worker and runway_reviewer be renamed after Batch Runway deletion?
recommended_option: defer renaming
blocks: []
```

### OPEN-008 — Prototype directory retention

```yaml
id: OPEN-008
status: open
question: >-
  Should representation experiments live temporarily in prototypes/contract-first
  or only in test fixtures and design documents?
recommended_option: use prototypes only when comparison requires reviewable artifacts
blocks: []
```

## Deferred Decisions and Ideas

### FUTURE-001 — Conservative parallel slice scheduling

```yaml
id: FUTURE-001
status: deferred
enabled_by:
  - explicit slice dependencies
  - declared read and write scopes
  - stable result contracts
excluded_from_current_program: true
```

### FUTURE-002 — Generated Markdown views

```yaml
id: FUTURE-002
status: deferred
reason: >-
  Embedded hybrid artifacts should be proven before adding generator ownership,
  regeneration policy, and review workflow.
```

### FUTURE-003 — Stronger transaction store

```yaml
id: FUTURE-003
status: deferred
reason: >-
  First prove explicit revisions and recoverable file transitions. SQLite must
  not become canonical by accident.
```

## Rejected Approaches

```yaml
rejected:
  - id: REJECT-001
    approach: permanent skills-v2 catalog or version-suffixed human commands
    reason: creates dual routing and compatibility sediment
  - id: REJECT-002
    approach: modernize APR and Batch Runway as final broad owners
    reason: improves representation while preserving the wrong ownership model
  - id: REJECT-003
    approach: central replacement workflow service behind command aliases
    reason: recreates the same broad owner under a new name
  - id: REJECT-004
    approach: independently edited companion YAML as the initial default
    reason: creates two files that can drift
  - id: REJECT-005
    approach: preserve every current test unchanged
    reason: many tests protect bridge topology and prose rather than behavior
  - id: REJECT-006
    approach: implement the redesign as one giant batch
    reason: weakens rollback and behavior-equivalence proof
  - id: REJECT-007
    approach: precompute implementation batches before ledger intake
    reason: bypasses add-to-ledger and plan-batch ownership boundaries
  - id: REJECT-008
    approach: let candidate skills control their own real migration before cutover
    reason: risks mixed-generation planning, execution, recovery, and closeout
```

## Decision Change Procedure

To change an accepted decision:

1. add a new decision record;
2. mark the old record `superseded` rather than rewriting history silently;
3. name affected contract IDs, phases, scenarios, and deletion conditions;
4. state whether the change broadens, narrows, or preserves behavior;
5. require explicit human approval for ownership changes or supported behavior
   narrowing;
6. update all authoritative design files before implementation proceeds.
