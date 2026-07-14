# CCFG-20 Skill Contract Schema Dispatch

## Batch Identity

- Batch ID: `ccfg-20-skill-contract-schema`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-20, Implement `skill-contract/v1` Schema and
  Validators
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/runway.md`

## Selection Decision

Select CCFG-20 now. CCFG-19 is closed with DEC-036 accepted, the source row is
the first dependency-ready command-owner redesign implementation finding, and
its five exit keys fit one schema-and-validator module.

The vague-row guard passes because COR-003 and the accepted CCFG-19 decision
record define one owner seam, deterministic acceptance criteria, and a
non-destructive boundary. The batch may add the repo-local schema, validator,
fixture catalogs, dependencies, tests, and changelog entry. It may not migrate
current skills, transfer workflow ownership, install a new feature, or begin
CCFG-21 through CCFG-29.

CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11 wait because their ledger
directions are conditional, backlog-oriented, or require fresh replanning.
CCFG-21 through CCFG-29 wait on the accepted redesign dependency chain.

## Gate Evidence

```yaml
planning_state:
  root: /home/alacasse/projects/codex-config/docs/plans
  current: passed
  validate: passed
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  blockers: []
  warnings:
    - two known redirect-ledger warnings
stable_control:
  repository_root: /home/alacasse/projects/codex-config
  branch: master
  commit: 7c1c02756d76baf65ac9f981bbcbb37ed807d1ba
  codex_home: /home/alacasse/.codex
  worktree_before_planning: clean
  install_status: passed
  install_dry_run: passed
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  commit: 13d7f63d258c82760a330a9a61e62ea99d7a493f
  worktree_before_planning: clean
accepted_lineage:
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
  ccfg_19_status: closed
  schema_evolution_decision: DEC-036
strict_context:
  interface: cross-checkout-context/v1
  installed_helper: /home/alacasse/.codex/scripts/cross_checkout_context.py
  helper_resolves_to: /home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
  payload_validation: passed
  canonical_planning_write_scope_validation: passed
  intended_implementation_write_scope_validation: passed
focused_baseline:
  cross_checkout_and_agent_contracts: 33_passed_187_subtests
  manifest_schema_subset: 3_passed_18_deselected_31_subtests
  full_manifest: known_red_3_failed_18_passed
```

## Batch Kind And Risk

- Batch kind: `migration`.
- Slices 1 through 4 risk: `migration`.
- The migration risk is limited to adding the target schema mechanism and its
  deterministic validator. It does not authorize migration of existing skill
  documents or workflow ownership.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such
  slice is authorized.
- Candidate-checkout write access remains subject to execution-time filesystem
  approval. Approval does not widen the allowed files or finding scope.

## Goal

Implement one deep, repo-local `skill-contract/v1` validation module that:

- extracts exactly one structured Contract block from a hybrid skill document;
- validates the accepted closed-world structural schema and audience profiles;
- validates ownership, delegation, dependencies, and explicit references over
  a catalog;
- rejects missing, cyclic, or toolchain-root-escaping structured references;
- enforces DEC-036 schema evolution and producer identity rules; and
- compares explicit before/after catalogs using policy inputs for the four
  accepted deterministic migration guards.

## Owner Seam And Validation Class

- Module seam: `scripts/skill_contract.py`.
- Structural schema owner: `schemas/skill-contract-v1.schema.json`.
- Module interface: `validate_skill_contracts(...)`, one catalog validation
  entry point that returns parsed contracts plus deterministically sorted
  diagnostics; optional explicit before/after catalogs and migration policy
  activate comparison guards.
- CLI: a thin adapter in the same module over that interface.
- Runtime dependencies: PyYAML and jsonschema, locked through `uv`.
- Installed surface: none in CCFG-20. `codex-features.json` remains unchanged;
  CCFG-22 owns the first runtime consumer and any later neutral installation.
- Validation profile: `project-harness-production` with fixture-catalog CLI
  runs as the project-local integration harness.
- Runway density: `full-runway` because this adds a versioned YAML schema and
  migration validator.
- Run artifact root: `None`.
- Output root: `None`.

## Included Source Scope

- COR-003 / CCFG-20 in accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- Accepted `skill-contract/v1` shape in
  `docs/design/command-owner-redesign/03-contract-first-formats.md`.
- Accepted CCFG-20 migration boundary in
  `docs/design/command-owner-redesign/04-migration-program.md`.
- DEC-036 and the joined CCFG-19 evidence in
  `docs/design/command-owner-redesign/10-ccfg-19-contract-verification-and-decisions.md`.
- Existing fail-closed object, path-containment, dependency-traversal, and
  deterministic-diagnostic patterns as implementation evidence only.

## Deferred And Excluded

- Adding Contract blocks to existing skills or validating the current whole
  skills directory as a required-green catalog.
- Planning-artifact schemas, ledger-store, or transaction work from CCFG-21.
- `skill-authoring` implementation and trials from CCFG-22.
- Behavioral harness work from CCFG-23.
- Intake, planning, execution, or closeout ownership transfer.
- Installer links, manifest registration, candidate installation, or default
  generation changes.
- Compatibility aliases, prose-semantic inference, project-name-specific
  migration rules, and a hand-written YAML parser.

## Suggested Slice Shape

1. Establish the closed-world schema and one deep validation interface.
2. Add catalog ownership and audience-profile validation.
3. Add delegation, dependency, and explicit-reference graph validation.
4. Add before/after migration guards, CLI integration proof, and changelog.

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

Complete validated payload:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: /home/alacasse/projects/codex-config
  toolchain_commit: 7c1c02756d76baf65ac9f981bbcbb37ed807d1ba
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 7c1c02756d76baf65ac9f981bbcbb37ed807d1ba
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 13d7f63d258c82760a330a9a61e62ea99d7a493f
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The installed stable helper parsed the payload and validated the exact four
canonical planning paths plus the nine intended candidate file areas named by
the runway. Planning performed no candidate write.

## Stop Conditions

- Stop if the strict context, canonical planning root, installed helper,
  stable revision, candidate revision, generation, or root identity changes.
- Stop if the candidate worktree is not clean before Slice 1 or contains
  changes outside the active slice allowlist.
- Stop if structural facts are duplicated between JSON Schema and validator
  code instead of keeping one canonical source.
- Stop if implementation requires a hand-written YAML dialect, arbitrary prose
  interpretation, or project-specific migration names.
- Stop if a current skill must be migrated for fixture-catalog validation to
  pass; that work belongs to CCFG-22 and later ownership-transfer findings.
- Stop if any slice touches `codex-features.json`, installed Codex state, or a
  CCFG-21 through CCFG-29 owner surface.
- Stop closeout before selecting, refreshing, dispatching, or preparing a
  successor batch.
