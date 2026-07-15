# CCFG-22 Skill Authoring v1 Dispatch

## Batch Identity

- Batch ID: `ccfg-22-skill-authoring-v1`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-22, Finalize and Validate `skill-authoring` v1
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/runway.md`
- Successor selected: no

## Selection Decision

Select the user-requested CCFG-22 row now. CCFG-20 and CCFG-21 are closed, so
the accepted `skill-contract/v1` validator and every planning schema needed by
the conditional planning-artifact reference exist in the candidate checkout.
The ledger records no selected dispatch, queued runway, active runway, or
blocker before this selection.

The vague-row guard passes after reading only the ledger-linked accepted design
snapshot and completed dependency evidence. The accepted contract defines one
authoring-support owner, one core path and contract version, a conditionally
loaded planning reference, two bounded trial classes, deterministic migration
guards, and nine exit keys. The trials are fixture-only authoring proofs; they
do not migrate live `dead-surface-audit`, `plan-batch`, or any other current
skill. CCFG-24 through CCFG-29 retain live command-owner migration, cutover, and
convergence ownership.

CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11 remain deferred because the
user requested CCFG-22 and those rows are unrelated, conditional, or require
fresh replanning. CCFG-23 through CCFG-29 remain separate redesign findings
with their existing dependency chain.

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
  commit: 0546e06f5ab18d777b0db557ac6bcacdd6bb0def
  codex_home: /home/alacasse/.codex
  worktree_before_planning: clean
  install_status: passed_with_manifest_version_drift
  install_dry_run: passed_without_writes
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  commit: 596fc7e5e153bb1a89a94010d272efa4ce4ce0ce
  upstream_ahead_behind: 0/0
  worktree_before_planning: clean
  codex_home: /home/alacasse/.codex-command-owner-redesign
  install_status: passed_at_exact_manifest_versions
  install_dry_run: passed_without_writes
accepted_lineage:
  accepted_design_snapshot: caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c
  ccfg_20_status: closed
  ccfg_21_status: closed
  skill_authoring_decision: DEC-024
  layered_single_version_decision: DEC-031
strict_context:
  interface: cross-checkout-context/v1
  installed_helper: /home/alacasse/.codex/scripts/cross_checkout_context.py
  helper_resolves_to: /home/alacasse/projects/codex-config/scripts/cross_checkout_context.py
  payload_validation: passed
  canonical_planning_write_scope_validation: passed
  intended_implementation_write_scope_validation: passed
focused_baseline:
  skill_contract_suite: 42_passed
  planning_schema_suite: 25_passed
  cross_checkout_and_agent_contracts: 33_passed_187_subtests
  focused_manifest_subset: 4_passed_17_deselected_34_subtests
  full_manifest: known_red_3_failed_18_passed_202_subtests
```

## Batch Kind And Risk

- Batch kind: `migration`.
- Slices 1, 2, and 4 risk: `migration`.
- Slice 3 risk: `none`; it adds fixture-only trials and tests without changing
  a supported runtime surface.
- Authorized migration: establish one authoritative candidate
  `skill-authoring` owner, add its conditional planning reference, register its
  existing schema/validator prerequisites with the feature, document the
  agent-facing surface, and install it only into the isolated candidate home.
- Live skill migration, command-owner ownership transfer, and stable-home
  installation: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such slice
  is authorized.
- Candidate-checkout and candidate-home filesystem approval may be required at
  execution time. Approval authorizes access only and does not widen scope.

## Goal

Create one complete authoritative authoring-support workflow that:

- extracts one explicit `skill-contract/v1` contract from accepted source
  behavior and decisions;
- reports ownership conflicts and unresolved ambiguity instead of silently
  resolving them;
- separates procedure, branches, rationale, and conditional references;
- applies deterministic before/after migration guards through the existing
  `scripts/skill_contract.py` owner;
- keeps generic skill-writing mechanics outside its contract-first ownership;
- conditionally loads one planning-artifact authoring reference that declares
  exact supported schema versions and blocks unsupported schemas;
- proves one narrow evidence-skill trial and one branching command-like trial
  through fixture-only authored outputs;
- installs the skill, schema, and validator only into the isolated candidate
  generation; and
- leaves every command owner free of a runtime dependency on
  `skill-authoring`.

## Owner Seam And Validation Class

- Canonical core: `skills/skill-authoring/SKILL.md`.
- Conditional planning reference:
  `skills/skill-authoring/references/planning-artifact-authoring.md`.
- Existing read-only contract owners:
  - `schemas/skill-contract-v1.schema.json`
  - `scripts/skill_contract.py`
- Fixture-only trial catalog: `tests/fixtures/skill-authoring/`.
- Focused behavioral contract tests: `tests/test_skill_authoring.py`.
- Candidate feature registration and installation evidence:
  `codex-features.json`, `tests/test_codex_features_manifest.py`, and the
  candidate home at `/home/alacasse/.codex-command-owner-redesign`.
- Documentation and decision history: `README.md` and `CHANGELOG.md`.
- Existing schema, validator, command-owner skill, and planning-contract source
  files remain read-only.
- Validation profile: `project-harness-production` because the final slice
  changes candidate installation metadata and an installed agent workflow.
- Runway density: `full-runway` because the batch combines contract-first
  authoring semantics, supported-schema blocking, manifest registration, and an
  isolated installed-generation proof.
- Run artifact root: `None`.
- Output root: `None`; test temporary paths and installer stdout are ephemeral.
- Test quality review: `delta-only` for every test-changing slice.

## Included Source Scope

- COR-005 / CCFG-22 in accepted snapshot
  `caf343a14bf8dae5ba3bfda6d8ab974929bb4c7c`.
- The accepted `skill-authoring` representation, ownership, prerequisites,
  reference rule, and trial classes in
  `docs/design/command-owner-redesign/03-contract-first-formats.md`.
- CCFG-22 dependency, required-work, and exit-gate detail in
  `docs/design/command-owner-redesign/04-migration-program.md`.
- Contract-first trial scenarios in
  `docs/design/command-owner-redesign/05-behavioral-test-matrix.md`.
- DEC-024 and DEC-031 in
  `docs/design/command-owner-redesign/decisions.md`.
- Closed CCFG-20 and CCFG-21 schemas, validators, tests, fixtures, and closeout
  evidence as implementation prerequisites, not as mutable scope.

## Deferred And Excluded

- Migrating or rewriting any live command-owner, support, evidence, or runtime
  skill under the new authoring workflow.
- Modifying `schemas/skill-contract-v1.schema.json`,
  `scripts/skill_contract.py`, any planning schema, or
  `scripts/planning_contract.py`.
- Adding per-command contract dialects, another authoring path, another schema
  version, or project-specific behavior to the generic authoring skill.
- Integrating `skill-authoring` as a runtime requirement of `add-to-ledger`,
  `plan-batch`, `work-batch`, or any support skill.
- Implementing CCFG-23 scenario-harness ownership or CCFG-24 through CCFG-29
  migration, cutover, deletion, or convergence work.
- Installing into `/home/alacasse/.codex`, switching the default generation,
  changing credentials, or allowing a candidate process to mutate canonical
  planning state.
- Fixing the three known-red manifest wording assertions, broadening their
  scope, or absorbing unrelated installer/version drift.

## Suggested Slice Shape

1. Add the authoritative core skill and focused core-contract tests.
2. Add the conditional planning-artifact reference and exact supported-schema
   blocking tests.
3. Add and validate one narrow evidence-skill and one branching command-like
   fixture trial through the finalized core.
4. Register and document the agent-facing feature, install it only into the
   isolated candidate home, and prove command owners have no runtime dependency.

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
  toolchain_commit: 0546e06f5ab18d777b0db557ac6bcacdd6bb0def
  canonical_planning_repository_root: /home/alacasse/projects/codex-config
  canonical_planning_commit_before: 0546e06f5ab18d777b0db557ac6bcacdd6bb0def
  implementation_target_root: /home/alacasse/projects/codex-config-command-owner-redesign
  implementation_commit_before: 596fc7e5e153bb1a89a94010d272efa4ce4ce0ce
  codex_home: /home/alacasse/.codex
  generation_role: stable
  canonical_state_mutation_allowed: true
```

The installed stable helper parsed the payload and validated the exact four
canonical planning paths plus the seven intended candidate paths or file areas
named by the runway. Planning performed no candidate write.

## Stop Conditions

- Stop if the selected CCFG-22 scope no longer matches this dispatch.
- Stop if the first execution-flight ready/blocked preflight does not return a
  fresh strict context for this selected scope.
- Stop if the candidate worktree is not clean before Slice 1 or contains
  changes outside the active slice allowlist.
- Stop if implementation modifies or duplicates the accepted
  `skill-contract/v1` schema or validator instead of consuming them.
- Stop if the core silently resolves an ownership ambiguity, executes the
  workflow it is authoring, mutates planning state, or claims generic
  skill-writing ownership.
- Stop if the planning reference omits its exact supported schema versions,
  accepts an unsupported schema, or redefines core ownership/canonicality.
- Stop if either trial modifies a live skill or becomes evidence for beginning
  CCFG-23 through CCFG-29.
- Stop if any command owner gains a runtime dependency on `skill-authoring`.
- Stop if installation targets the stable home, mixes stable and candidate
  links, copies credentials, or grants candidate canonical-write authority.
- Stop if work expands into the known-red manifest assertions or unrelated
  installer/version drift.
- Stop closeout before selecting, refreshing, dispatching, or preparing a
  successor batch.
