# Decision Register

## Purpose

This register separates accepted target decisions from deferred ideas, rejected
approaches, and questions that still require explicit human input.

Priority order for redesign work:

```text
accepted decisions in this register
-> current migration phase contract
-> stable behavior contract IDs
-> target ownership model
-> selected implementation dispatch and runway
-> repository source evidence
-> GitHub issues and historical plans
-> conversation transcripts
```

An agent must not silently resolve an `open` decision or revive a rejected
approach because it appears in historical source material.

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
rationale: >-
  These commands match user intent and allow support components to become narrow
  mechanisms rather than alternate workflow owners.
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
rationale: >-
  The architectural problem is broad alternate ownership, not short command
  skills or technical delegation.
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
rationale: >-
  This keeps deterministic state behavior executable without hiding a new broad
  workflow owner behind a narrow name.
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
rationale: >-
  This keeps machine facts parseable and human reasoning readable in one Git-
  reviewable artifact without introducing a companion-file drift problem.
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
rationale: >-
  Full workflow contracts would overload integration frontmatter, especially for
  ownership, outputs, and references.
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
  commands. Develop target skills at final paths in an isolated branch or
  worktree with a separate CODEX_HOME.
rationale: >-
  Parallel catalogs create routing ambiguity and compatibility sediment.
```

### DEC-012 — Use stable and candidate installation lanes

```yaml
id: DEC-012
status: accepted
decision: >-
  The stable checkout and default CODEX_HOME perform and review migration work.
  The candidate branch or worktree and separate CODEX_HOME test target skills in
  fresh sessions.
rationale: >-
  Installed features are symlinked to source paths; in-place mutation could make
  one workflow session consume multiple generations of its own contract.
```

### DEC-013 — Use `port-by-contract` only for extraction and target design during bootstrap

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

### DEC-021 — The skill-authoring meta-skill is implemented last

```yaml
id: DEC-021
status: accepted
decision: >-
  GitHub issue #49 is implemented only after skill-contract/v1 and planning
  artifact v1 formats are validated on the target owners.
rationale: >-
  Creating the meta-skill first would risk codifying an unproven schema or
  encouraging cosmetic migrations.
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
reason: >-
  It avoids a second durable source while keeping the current handoff artifact
  human-readable. The implementation must prove atomic revision-checked updates.
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
reason: >-
  A single block simplifies revision checks and duplicate identity validation,
  but diff readability and merge behavior must be prototyped.
blocks:
  - ledger-store format
  - intake mutation implementation
```

### OPEN-003 — Exact transaction boundary for multi-artifact planning

```yaml
id: OPEN-003
status: open
question: >-
  How should plan-batch atomically or recoverably apply dispatch creation, runway
  creation, and selected-to-queued transitions across Markdown artifacts?
options:
  - staged writes plus transition receipts and recovery
  - temporary files plus atomic renames within one filesystem
  - explicit selected state followed by separately recoverable queued transition
recommended_option: explicit selected state followed by recoverable queue transition
reason: >-
  The dispatch is already a meaningful durable intermediate state.
blocks:
  - final plan-batch state mutation protocol
```

### OPEN-004 — Strictness of one-commit-per-slice

```yaml
id: OPEN-004
status: open
question: >-
  Is one focused commit per accepted slice a universal execution contract or a
  default execution profile that may be overridden explicitly?
recommended_option: default profile with explicit override support
reason: >-
  The behavior is useful and currently relied upon, but a versioned profile is
  more honest than treating it as a universal workflow law.
blocks:
  - planning-runway/v1 final execution fields
```

### OPEN-005 — Exact slice-count rule

```yaml
id: OPEN-005
status: open
question: >-
  Should 3-5 slices remain a hard schema constraint, a planning warning, or only
  a documented heuristic?
recommended_option: warning-level heuristic
reason: >-
  Bounded, testable, independently committable work is the durable contract; the
  exact count is current implementation guidance.
blocks:
  - planning-runway/v1 validation severity
```

### OPEN-006 — Final names for narrow Python modules

```yaml
id: OPEN-006
status: open
question: >-
  What final module split should implement diagnostics, transitions, ledger
  mutation, artifact parsing, schemas, closeout validation, and projections?
recommended_option: decide from behavior seams during implementation design
reason: >-
  The design fixes interfaces and forbidden responsibilities, not accidental
  package names.
blocks: []
```

### OPEN-007 — Worker and reviewer names

```yaml
id: OPEN-007
status: open
question: >-
  Should runway_worker and runway_reviewer be renamed after Batch Runway deletion?
recommended_option: defer renaming
reason: >-
  Their authority contracts are useful and the names do not block ownership
  transfer if path and dependency references are removed.
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
reason: >-
  Any prototype directory must be non-installed, non-canonical, and deleted after
  selection.
blocks: []
```

## Deferred Decisions and Ideas

### FUTURE-001 — Conservative parallel slice scheduling

```yaml
id: FUTURE-001
status: deferred
topic: conservative parallel slice scheduling
enabled_by:
  - explicit slice dependencies
  - declared read and write scopes
  - stable result contracts
  - isolated worktrees or equivalent execution boundaries
excluded_from_current_program: true
```

### FUTURE-002 — Generated Markdown views

```yaml
id: FUTURE-002
status: deferred
topic: generate human-readable Markdown from structured canonical sources
reason: >-
  Embedded hybrid artifacts should be proven before adding generator ownership,
  regeneration policy, and review workflow.
```

### FUTURE-003 — Stronger transaction store

```yaml
id: FUTURE-003
status: deferred
topic: replace file-level transition coordination with a stronger transaction store
reason: >-
  The current program should first prove explicit revisions and recoverable file
  transitions. SQLite must not become canonical by accident.
```

## Rejected Approaches

### REJECT-001 — Permanent `skills-v2/` catalog

```yaml
id: REJECT-001
status: rejected
approach: permanent parallel skill directory or version-suffixed human commands
reason: >-
  Creates dual routing, duplicate ownership, install ambiguity, and compatibility
  sediment.
```

### REJECT-002 — Modernize APR and Batch Runway in place as final owners

```yaml
id: REJECT-002
status: rejected
approach: >-
  Rewrite architecture-program-runway and batch-runway into contract-first
  formats while retaining their current broad ownership.
reason: >-
  Improves representation but reinforces the transitional architecture.
```

### REJECT-003 — Central replacement workflow service behind command aliases

```yaml
id: REJECT-003
status: rejected
approach: >-
  Replace APR with another broad workflow service while keeping command skills as
  thin aliases.
reason: >-
  Conflicts with the accepted command-owner intent and recreates the same owner
  problem under a new name.
```

### REJECT-004 — Companion YAML as the initial artifact default

```yaml
id: REJECT-004
status: rejected
approach: Markdown artifact plus independently edited companion YAML
reason: >-
  Creates two files that can drift, move, or be reviewed separately before the
  format and transaction model are proven.
```

### REJECT-005 — Preserve every current test unchanged

```yaml
id: REJECT-005
status: rejected
approach: treat all current tests as target compatibility contracts
reason: >-
  Many current tests intentionally protect bridge topology and prose rather than
  externally meaningful behavior.
```

### REJECT-006 — Implement the entire redesign as one giant batch

```yaml
id: REJECT-006
status: rejected
approach: single rewrite and deletion batch
reason: >-
  Prevents controlled ownership transfer, weakens rollback, and makes behavior
  equivalence and compatibility expiry difficult to prove.
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
