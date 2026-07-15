# CCFG-22 Skill Authoring v1 Runway

## Purpose

Implement and validate one authoritative `skill-authoring` v1 workflow in the
candidate checkout. The workflow owns contract-first hybrid-skill authoring,
not generic writing or workflow execution. It includes one conditionally loaded
planning-artifact reference, two fixture-only authoring trials, and
candidate-only feature installation.

This runway covers CCFG-22 only. Closeout may mark CCFG-22 `Closed` only when
all nine COR-005 acceptance keys and the migration-program aggregate gate are
green. Otherwise preserve the exact blocker and stop without selecting a
successor.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slice 1 risk: `migration`; it establishes a new authoritative authoring owner.
- Slice 2 risk: `migration`; it adds the conditional planning-artifact contract
  surface under the same owner and version.
- Slice 3 risk: `none`; it adds fixture-only trials and validation without
  changing a supported runtime surface.
- Slice 4 risk: `migration`; it registers and installs the new candidate-only
  feature without changing the default generation.
- Authorized migration: add one candidate authoring-support skill, one
  conditional reference, deterministic trial fixtures/tests, manifest
  registration, candidate-only installation, and adjacent documentation.
- Live skill migration and command-owner ownership transfer: forbidden.
- Stable-home installation and default-generation switch: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such slice
  is authorized.
- Candidate-checkout and candidate-home filesystem approval may be required at
  execution time. It authorizes only the paths and installer action named here.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Planning-state `current` and `validate` pass with no blockers and only the two
  known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable checkout: `/home/alacasse/projects/codex-config`, branch `master`,
  exact `HEAD` `0546e06f5ab18d777b0db557ac6bcacdd6bb0def`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, exact `HEAD`
  `596fc7e5e153bb1a89a94010d272efa4ce4ce0ce`, aligned with its upstream.
- Both worktrees were clean before planning. Planning performs no candidate
  write.
- Stable Codex home: `/home/alacasse/.codex`. Its installed helper resolves to
  the stable checkout. Status exits successfully with known manifest-version
  drift and dry-run reports only stable-owned links without writing.
- Candidate Codex home: `/home/alacasse/.codex-command-owner-redesign`. Status
  reports exact candidate manifest versions and dry-run reports only
  candidate-owned links without writing.
- `skill-authoring`, installed `skill_contract.py`, and the installed schema are
  absent from both Codex homes before this batch.
- CCFG-20 is closed with the accepted closed-world
  `schemas/skill-contract-v1.schema.json` and the single deterministic
  `scripts/skill_contract.py` validator/catalog/migration owner.
- CCFG-21 is closed with accepted v1 schemas for current, finding, dispatch,
  runway, closeout, and selection-transaction artifacts.
- DEC-024 requires `skill-authoring` before command-owner migration. DEC-031
  requires one complete core, one contract version, and a conditionally loaded
  planning reference under that same owner.
- The candidate has no `skills/skill-authoring/`, no authoring trial catalog,
  no focused authoring test module, and no manifest feature for the new skill.
- Existing command-owner and support skills are still bridge-state runtime
  topology. They are read-only evidence for this batch and are not trial
  migration targets.
- Current required-green baselines are 42 skill-contract tests, 25 planning
  schema tests, 33 cross-checkout/custom-agent tests with 187 subtests, and 4
  focused manifest tests with 34 subtests.
- The full manifest is a known-red diagnostic: 3 failed and 18 passed in the
  exact unrelated wording assertions recorded by CCFG-20 and CCFG-21.

The queued stable planning artifacts are expected dirty coordination state. Do
not copy them into the candidate checkout. The persisted context below is a
planning snapshot, not a live execution lease. If either repository `HEAD`
moves, preserve the snapshot and use the canonical ready/blocked preflight or
refresh procedure before delegation.

## Batch Non-Goals

- Do not migrate, rewrite, or add contract blocks to live command-owner,
  evidence, support, or runtime skills.
- Do not modify `schemas/skill-contract-v1.schema.json`,
  `scripts/skill_contract.py`, any planning schema, or
  `scripts/planning_contract.py`.
- Do not create another authoring skill path, another contract version, a
  per-command dialect, or project-specific behavior in the reusable skill.
- Do not let `skill-authoring` execute authored workflows, mutate planning
  state, silently settle ownership ambiguity, or own generic skill prose and
  scaffolding.
- Do not add `skill-authoring` as a runtime requirement of `add-to-ledger`,
  `plan-batch`, `work-batch`, or any support mechanism.
- Do not begin CCFG-23 behavioral-harness ownership or CCFG-24 through CCFG-29
  migration, cutover, deletion, and convergence work.
- Do not install into `/home/alacasse/.codex`, switch the default generation,
  copy credentials, or grant candidate canonical-write authority.
- Do not fix or weaken the three known-red manifest wording assertions, update
  unrelated feature versions, or absorb unrelated installer drift.

## Acceptance Key Map

COR-005 closes only with these exact keys:

```yaml
core_complete: true
one_skill_path: true
one_contract_version: true
narrow_skill_trial_green: true
branching_command_trial_green: true
planning_reference_declares_supported_schemas: true
unsupported_schema_blocks: true
candidate_only_installation_green: true
runtime_dependency_from_command_owners: false
```

The implementation evidence must also satisfy the migration-program aggregate
gate:

```yaml
skill_authoring_core_complete: true
single_skill_path_and_contract_version: true
narrow_skill_trial_green: true
branching_command_trial_green: true
planning_reference_blocks_on_unsupported_schema: true
runtime_dependency_from_command_owners: false
candidate_only_installation_green: true
```

Closeout must map focused tests, catalog/CLI validation, installer evidence,
link identity, and independent review to every key rather than treating one
aggregate test result as acceptance.

## Required Strict Execution Context

Mode: explicit `cross-checkout-context/v1`.

Installed helper path used for planning validation:

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

Planning loaded the installed stable helper, verified that it resolves under
the declared toolchain root, parsed the complete payload, and called
`validate_write_scope` with these four canonical planning paths:

- `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/dispatch.md`
- `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/runway.md`
- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`

It also validated these seven intended candidate paths or file areas:

- `skills/skill-authoring/`
- `tests/fixtures/skill-authoring/`
- `tests/test_skill_authoring.py`
- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `README.md`
- `CHANGELOG.md`

Validation passed. Planning performed no candidate write.

Before the first worker or reviewer delegation, the coordinator must follow
`skills/batch-runway/references/cross-checkout-context-v1.md` and call the
canonical ready/blocked preflight with this immutable planning snapshot. Before
every later delegation, prepare a fresh live execution lease, validate the
active slice's exact write scope, and pass the live context, canonical planning
root, absolute helper path, and write-bearing/read-only mode. Every explicit
cross-checkout agent result must carry matching non-null
`verified_cross_checkout_context` evidence.

Candidate-home installation in Slice 4 is a separately assigned project
integration action. The strict helper validates candidate-repository writes;
it does not widen write authority to the stable Codex home or any other path.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-22-skill-authoring-v1/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`; pytest temporary paths and installer stdout/stderr are
  ephemeral.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway`.
- Integration harnesses:
  - existing `scripts/skill_contract.py` CLI over the core and trial catalogs;
  - focused pytest for authoring, schema compatibility, manifest ownership, and
    cross-checkout result contracts;
  - candidate installer status, dry-run, feature install, and exact link
    identity under `/home/alacasse/.codex-command-owner-redesign`;
  - stable installer status, dry-run, and absence checks under
    `/home/alacasse/.codex`.
- Harness output: stdout/stderr and pytest temporary directories only; no
  durable generated output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index/generated-doc refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus a
  separate stable planning-ledger receipt after each candidate hash exists.
- Dirty-file constraints: candidate starts clean and may change only active
  slice files; stable changes are limited to this batch's planning artifacts
  and same-batch reconciliation.
- Test quality review: `delta-only` for every test-changing slice and for the
  final exact candidate range.

## Authoring Interface And Slice Handoff

The canonical owner is `skills/skill-authoring/SKILL.md`. Its one
`skill-contract/v1` block must use the `authoring-support` audience and own only
these accepted decisions:

- `contract_extraction`
- `skill_structure_design`
- `ownership_conflict_reporting`
- `reference_split_recommendations`

The producer identity records the exact candidate generation and commit used to
author the document; it does not attempt a self-referential containing-commit
hash. The core must forbid workflow execution, planning-state mutation, silent
ownership resolution, unapproved schema fields, source-prose preservation by
default, and YAML presence as migration success.

The core procedure must make these stages explicit:

1. collect accepted behavior, ownership, audience, migration, and output facts;
2. extract one closed-world contract without inventing decisions;
3. report conflicts and unresolved ambiguity before authoring;
4. separate procedure, branches, rationale, and conditional references;
5. validate the contract and catalog with the existing validator;
6. validate before/after migration guards when migration is requested; and
7. return the authored/audited result without executing the authored workflow.

Generic prose, scaffolding, examples, and presentation mechanics remain outside
this contract-first owner. The core must name that boundary without hard-coding
a vendor-owned skill or project-specific authoring mechanism into reusable
workflow text.

Slice 1 establishes the independently valid core with no conditional reference.
Slice 2 adds the planning reference under the same v1 and updates the core's
single canonical `references` list. Slice 3 consumes that finalized owner to
produce fixture-only trials. Slice 4 registers the existing skill, validator,
and schema as one candidate feature without making command owners depend on it.

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
Use the expanded convergence template only for expanding scope, significant
uncertainty, blockers, or final batch reporting.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/cross-checkout-context-v1.md`
- `skills/batch-runway/references/test-quality-review.md`
- `skills/test-quality-review/SKILL.md`

Overrides:

- Candidate implementation commits and stable planning-ledger receipt commits
  are distinct cross-repository commits. Record both hashes per slice.
- Workers use the existing locked candidate `.venv`. They may not install
  ambient packages, update `pyproject.toml` or `uv.lock`, or run installer
  mutations.
- Candidate-home installation is coordinator-owned and occurs only after Slice
  4 source validation and review establish the exact feature link set.
- Every test-changing slice receives `test-quality-review` in `delta-only`
  mode. Actionable findings enter the normal reviewer fix/block loop; clean
  output is recorded compactly.
- Stable-home status/dry-run and absence checks are coordinator-owned. No
  command in this runway may install, unlink, refresh, or mutate the stable
  home.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

### Current Required-Green Baseline

Run from the candidate checkout unless a command names the stable checkout:

- Existing skill-contract suite:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py
  ```

  Status: `required-green`. Current result: 42 passed.

- Existing planning-schema suite:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_planning_contract_schema.py
  ```

  Status: `required-green`. Current result: 25 passed.

- Cross-checkout and registered-agent contracts:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py
  ```

  Status: `required-green`. Current result: 33 passed and 187 subtests passed.

- Focused manifest ownership subset:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'manifest_links_point_to_repo_sources or manifest_feature_requirements_are_valid or direct_request_prompts_preserve_command_owner_boundary or agent_facing_support_skills_are_not_ui_commands'
  ```

  Status: `required-green`. Current result: 4 passed, 17 deselected, and 34
  subtests passed.

- Stable installer read-only controls, run from the stable checkout:

  ```sh
  ./install.sh --status
  ./install.sh --dry-run
  ```

  Status: `required-green`. Both exit successfully. Status has known committed
  manifest-version drift; dry-run reports stable-owned links and no write.

- Candidate installer read-only controls:

  ```sh
  ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
  ./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
  ```

  Status: `required-green`. Status reports exact candidate manifest versions;
  dry-run reports candidate-owned links and no write.

### Implementation-Created Commands

Slice 1 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_authoring.py -k 'core or contract or structure or ambiguity or generic_boundary'
.venv/bin/ruff check --no-cache tests/test_skill_authoring.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/skill-authoring/SKILL.md
git diff --check
```

Slice 2 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_authoring.py -k 'planning_reference or supported_schema or unsupported_schema'
.venv/bin/ruff check --no-cache tests/test_skill_authoring.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . skills/skill-authoring/SKILL.md
git diff --check
```

Slice 3 creates and then promotes to required-green:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_authoring.py -k 'narrow_trial or branching_trial or trial_catalog'
.venv/bin/ruff check --no-cache tests/test_skill_authoring.py
.venv/bin/python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-authoring/narrow-evidence tests/fixtures/skill-authoring/branching-command
git diff --check
```

Slice 4 creates and then promotes to required-green before installation:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_skill_authoring.py tests/test_codex_features_manifest.py -k 'skill_authoring or manifest_links_point_to_repo_sources or manifest_feature_requirements_are_valid or direct_request_prompts_preserve_command_owner_boundary'
.venv/bin/ruff check --no-cache tests/test_skill_authoring.py tests/test_codex_features_manifest.py
git diff --check
```

After Slice 4 review accepts the exact feature link set, the coordinator runs
this implementation-created candidate-only install:

```sh
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature skill-authoring --dry-run
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --feature skill-authoring
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --status
./install.sh --codex-home /home/alacasse/.codex-command-owner-redesign --dry-run
test "$(readlink -f /home/alacasse/.codex-command-owner-redesign/skills/skill-authoring)" = "/home/alacasse/projects/codex-config-command-owner-redesign/skills/skill-authoring"
test "$(readlink -f /home/alacasse/.codex-command-owner-redesign/scripts/skill_contract.py)" = "/home/alacasse/projects/codex-config-command-owner-redesign/scripts/skill_contract.py"
test "$(readlink -f /home/alacasse/.codex-command-owner-redesign/schemas/skill-contract-v1.schema.json)" = "/home/alacasse/projects/codex-config-command-owner-redesign/schemas/skill-contract-v1.schema.json"
```

Status: `implementation-created` until Slice 4 registers the feature. After the
install, all three commands are required-green and the installed skill,
validator, and schema links must resolve only to the candidate checkout.

### Known-Red And Diagnostic-Only Commands

- Full manifest:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py
  ```

  Status: `known-red-baseline`. Current result: 3 failed, 18 passed, and 202
  subtests passed in these unrelated exact-wording assertions:
  `test_executable_work_source_boundary_is_explicit`,
  `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
  `test_work_batch_reconciles_same_batch_closeout`. CCFG-22 must not modify
  their implicated files, change their expected baseline, or treat them as an
  execution gate.

### Conditional Commands

- No basedpyright command is assigned because this batch changes no Python
  production module. If a worker proposes a production Python edit, stop for
  scope drift rather than adding a type-check exception.
- No full project pytest suite, generated-doc refresh, graph/index refresh,
  package install, or default-home installation is part of per-slice worker
  work.
- Candidate installer mutation runs only in Slice 4 after focused source tests
  and review accept the feature. Any earlier installer mutation is a stop.
- After candidate installation, stable-home absence is a required-green
  coordinator check:

  ```sh
  test ! -e /home/alacasse/.codex/skills/skill-authoring
  test ! -e /home/alacasse/.codex/scripts/skill_contract.py
  test ! -e /home/alacasse/.codex/schemas/skill-contract-v1.schema.json
  ```

## Shared Worker And Reviewer Briefs

Worker brief for every slice:

- You are the already-required `runway_worker`. Implement only the active slice
  from this runway; do not spawn, delegate to, or wait on another agent.
- Independently validate the fresh strict cross-checkout live lease before
  acting, then write only inside the candidate checkout and only to the active
  slice's allowed files.
- Keep stable planning files, accepted history, the existing skill/planning
  schemas and validators, live skills, and unrelated candidate files read-only.
- Preserve one `skills/skill-authoring/SKILL.md` owner and one
  `skill-contract/v1` dialect. Do not add a second parser, validator, authoring
  owner, schema version, or project-specific branch.
- Do not migrate current skills, integrate command owners, start later
  findings, install features, or mutate either Codex home.
- Run only the focused validation assigned to the slice and return the
  registered v2 worker result with matching
  `verified_cross_checkout_context`.

Reviewer brief for every slice:

- The coordinator supplies the exact candidate commit hash or task-scoped
  candidate worktree diff basis. Echo it as `diff_basis` in the registered v2
  reviewer result.
- Independently validate a fresh strict cross-checkout live lease before review.
- Review against COR-005, DEC-024, DEC-031, the accepted authoring contract,
  and the active slice's acceptance criteria.
- Verify behavior through the existing public validator/catalog/CLI and
  installer-visible outcomes, not through accidental helper or prose topology.
- Run `test-quality-review` in `delta-only` mode for each changed-test delta and
  include its compact result.
- Reject silent ownership decisions, generic writing takeover, workflow
  execution, planning mutation, unsupported-schema acceptance, live-skill
  trial migration, command-owner runtime dependency, stable-home mutation, or
  unrelated known-red remediation.
- Return matching `verified_cross_checkout_context` and a clear
  accept/fix/block verdict.

## Active Ledger

| Slice | Risk | Status | Candidate commit | Stable receipt | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|---|
| 2. Conditional planning reference | migration | Pending | — | — | Pending | Pending | Supported-schema gate green | — |
| 3. Fixture-only trials | none | Pending | — | — | Pending | Pending | Both trial classes green | — |
| 4. Candidate registration and install | migration | Pending | — | — | Pending | Pending | Candidate-only links and no runtime dependency | — |

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Slice Shape

- `1 -> 2`: Slice 1 creates a complete, independently valid authoring core that
  does not require planning schemas. Slice 2 consumes the closed CCFG-21 schema
  family to add the conditional reference and update the core's canonical
  reference list. The core-only intermediate state is valid and testable.
- `2 -> 3`: Slice 2 finalizes the supported authoring dialect and schema gate;
  Slice 3 uses that exact owner to create two fixture-only trials. This keeps
  authoring contract changes separate from evidence about representative
  outputs and gives the trials an immutable producer boundary.
- `3 -> 4`: Slice 3 proves both required trial classes before Slice 4 changes
  installation metadata or external candidate-home state. The uninstalled
  skill is a valid repo-local intermediate, while installation receives an
  independent review and rollback boundary.

Four slices are required by producer/consumer, evidence, and installer-risk
boundaries, not by a target count.

## Slice 1: Establish The Authoritative Core

Risk: `migration`.

Test quality review: `delta-only`.

Scope:

- Add `skills/skill-authoring/SKILL.md` with minimal discovery frontmatter and
  exactly one canonical `skill-contract/v1` block.
- Implement the accepted contract extraction, ambiguity reporting, structured
  authoring procedure, branch/rationale/reference separation, deterministic
  validation, and migration-guard workflow.
- Add agent-facing UI metadata without advertising a direct human workflow
  command.
- Add focused tests for the core contract and observable authoring boundaries.

Allowed files:

- `skills/skill-authoring/SKILL.md`
- `skills/skill-authoring/agents/openai.yaml`
- `tests/test_skill_authoring.py`

Non-goals:

- No planning reference yet; the core's canonical reference list remains empty
  and valid until Slice 2.
- No trial fixtures, manifest registration, README/changelog edit, or install.
- No schema, validator, live-skill, or command-owner edit.

Acceptance criteria:

- Frontmatter and contract identity both name `skill-authoring`; the audience
  is exactly `authoring-support` and the contract version is exactly
  `skill-contract/v1`.
- Producer identity records the exact candidate generation and pre-slice commit
  supplied by the live lease; no placeholder or self-referential containing
  commit remains.
- The core owns only the four accepted authoring decisions and no durable
  planning or workflow facts.
- The six accepted prohibitions are explicit and deterministic validation uses
  only the existing schema/validator owner.
- Procedure, branch rules, rationale, and reference-loading semantics are
  distinct; examples cannot become a second canonical contract.
- Ownership conflicts and missing decisions return an ambiguity/block result;
  they are never silently resolved.
- The generic writing boundary is explicit and project-neutral. The core does
  not hard-code a vendor skill, downstream project, planning path, cache, or
  validation command.
- Migration work requires explicit before/after catalogs and accepted policy;
  YAML presence alone cannot be reported as success.
- Agent UI metadata is agent-facing and does not contain `Use
  $skill-authoring`.
- Focused tests, CLI validation, ruff, diff check, independent review, and
  delta-only test-quality review are green.

Validation:

- Run the Slice 1 implementation-created commands.
- Re-run the 42-test existing skill-contract suite.

Commit message: `feat: add authoritative skill authoring core`.

Worker brief:

- Follow the shared worker brief. Build one deep core in the allowed files and
  stop before the planning reference or fixtures.

Reviewer brief:

- Follow the shared reviewer brief. Confirm one owner/version, exact accepted
  decisions/prohibitions, real ambiguity blocking, and no generic-writing or
  runtime-execution takeover.

Stop conditions:

- Stop if the accepted core cannot be represented without changing the closed
  CCFG-20 schema or validator.
- Stop if a second contract block, authoring path, schema version, or silent
  decision rule appears.
- Stop if the implementation begins Slice 2 through 4 scope.

## Slice 2: Add The Conditional Planning-Artifact Reference

Risk: `migration`.

Test quality review: `delta-only`.

Scope:

- Add
  `skills/skill-authoring/references/planning-artifact-authoring.md` under the
  same `skill-authoring` v1 owner.
- Update the core's one canonical `references` entry with the exact relative
  path and a machine-readable `load_when` trigger for creating or modifying a
  supported planning artifact.
- Declare exact support for these accepted schemas:
  `planning-current/v1`, `planning-finding/v1`, `planning-dispatch/v1`,
  `planning-runway/v1`, `planning-closeout/v1`, and
  `planning-selection-transaction/v1`.
- Add deterministic tests that supported versions load and any unlisted or
  unsupported version blocks.

Allowed files:

- `skills/skill-authoring/SKILL.md`
- `skills/skill-authoring/references/planning-artifact-authoring.md`
- `tests/test_skill_authoring.py`

Non-goals:

- No redefinition of core ownership, canonicality, migration, or reference
  semantics inside the conditional reference.
- No change to planning schemas, planning validator/store, or live planning
  artifacts.
- No trial fixtures, manifest registration, docs/changelog, or install.

Acceptance criteria:

- The planning reference declares the six exact schema names and versions it
  supports in one deterministic support list.
- The reference loads only for a task that creates or modifies one of those
  supported planning artifacts; ordinary hybrid-skill authoring does not load
  it.
- Missing schema identity, unknown schema name, and unsupported version block
  before authoring or mutation.
- The reference consumes Planning Artifact Layout and schema rules without
  redefining core authoring ownership or creating a second contract dialect.
- The core still has exactly one canonical contract block, one path, and one
  version after its reference list changes.
- Producer identity is updated to the exact pre-slice candidate commit from the
  fresh live lease used to author the Slice 2 revision; no self-reference or
  stale placeholder remains.
- Focused authoring tests, 25 planning-schema tests, CLI validation, ruff, diff
  check, independent review, and delta-only test-quality review are green.

Validation:

- Run the Slice 2 implementation-created commands.
- Re-run the complete authoring test module and the 25-test planning-schema
  suite.

Commit message: `feat: add planning artifact authoring reference`.

Worker brief:

- Follow the shared worker brief. Extend the same core and add only the
  conditional reference and focused tests.

Reviewer brief:

- Follow the shared reviewer brief. Verify exact supported versions,
  fail-closed unsupported behavior, and absence of core redefinition.

Stop conditions:

- Stop if a supported schema is not present and green in the closed CCFG-21
  implementation.
- Stop if the reference becomes unconditional, accepts an unknown version, or
  redefines core ownership/canonicality.
- Stop if implementation begins trial, registration, or installation scope.

## Slice 3: Prove The Two Fixture-Only Authoring Trials

Risk: `none`.

Test quality review: `delta-only`.

Scope:

- Use the finalized `skill-authoring` core to author one narrow evidence-skill
  fixture with no planning-state writes or workflow decisions.
- Author one branching human-command-owner fixture with normal procedure,
  multiple branch outcomes, explicit stop conditions, and delegation to a
  fixture-local support mechanism.
- Add the fixture-local support skill required to make the branching catalog
  mechanically complete without depending on live runtime skills.
- Validate both trial catalogs through the existing public validator and add
  focused behavioral assertions.

Allowed files:

- `tests/fixtures/skill-authoring/narrow-evidence/**`
- `tests/fixtures/skill-authoring/branching-command/**`
- `tests/test_skill_authoring.py`

Non-goals:

- No edit to the authoritative core or planning reference.
- No migration or copying of live `dead-surface-audit`, `plan-batch`,
  `add-to-ledger`, `work-batch`, APR, or Batch Runway text.
- No manifest, README, changelog, or installation change.

Acceptance criteria:

- The narrow trial has audience `evidence-skill`, owns only its evidence
  classification/output, forbids state mutation and workflow decisions, and
  validates as a standalone catalog.
- The branching trial has audience `human-command-owner`, owns one bounded
  human decision, contains normal/alternate/blocked branches, names stop
  conditions, and delegates only a mechanical responsibility to the
  fixture-local support skill.
- The support fixture has audience `support-mechanism` and does not own the
  command decision.
- Both trials use the same `skill-contract/v1` and the exact candidate producer
  identity supplied before Slice 3.
- The public catalog validator reports no missing target, duplicate owner,
  ownership conflict, reference error, or unsupported version.
- Tests assert observable contract, branch, stop, delegation, and no-write
  outcomes rather than private validator helper topology.
- Focused trial tests, CLI catalog validation, ruff, diff check, independent
  review, and delta-only test-quality review are green.

Validation:

- Run the Slice 3 implementation-created commands.
- Re-run the complete authoring test module and the 42-test existing
  skill-contract suite.

Commit message: `test: validate skill authoring trials`.

Worker brief:

- Follow the shared worker brief. Treat the committed core as input and write
  only fixture/test outputs; do not modify live or authoritative skill text.

Reviewer brief:

- Follow the shared reviewer brief. Confirm that both trial classes are real,
  bounded, behavior-oriented authoring proofs and not hidden live migrations.

Stop conditions:

- Stop if a trial needs a live skill edit, a second contract dialect, or a
  command-owner runtime dependency.
- Stop if fixture tests preserve accidental source topology instead of the
  accepted owner/branch/output behavior.
- Stop if implementation begins registration or installation scope.

## Slice 4: Register And Install The Candidate-Only Feature

Risk: `migration`.

Test quality review: `delta-only`.

Scope:

- Register `skill-authoring` version `1.0.0` as an agent-facing candidate
  feature in `codex-features.json`.
- Link the one skill directory, existing `scripts/skill_contract.py`, and
  existing `schemas/skill-contract-v1.schema.json` under that feature.
- Add focused manifest tests for the exact link set, candidate-only audience,
  and absence from every command owner's runtime requirements.
- Document the agent-facing authoring surface in `README.md` and record the
  decision/effect in `CHANGELOG.md`.
- After source validation and review, have the coordinator install only that
  feature into `/home/alacasse/.codex-command-owner-redesign` and prove exact
  candidate link identity.

Allowed candidate files:

- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `README.md`
- `CHANGELOG.md`

Assigned external state:

- `/home/alacasse/.codex-command-owner-redesign` only, through the exact
  `--feature skill-authoring` installer command after accepted review.

Non-goals:

- No edit to the skill core, planning reference, trials, existing validator,
  schema, installer implementation, feature versions, or command-owner
  dependency lists except the new feature's own entry.
- No stable-home install or mutation, default-generation switch, credential
  copy, candidate canonical write, or fresh CCFG-23 harness ownership.
- No remediation of the known-red manifest wording tests.

Acceptance criteria:

- The manifest contains exactly one `skill-authoring` feature at `1.0.0` with
  links to `skills/skill-authoring`, `scripts/skill_contract.py`, and
  `schemas/skill-contract-v1.schema.json` and no unrelated dependency.
- The feature and README classify `skill-authoring` as agent-facing authoring
  support, not a primary human command.
- `add-to-ledger`, `plan-batch`, and `work-batch` do not require
  `skill-authoring`; no support/runtime skill gains that dependency either.
- Candidate source validation and independent review are green before any
  candidate-home mutation.
- Candidate-only installation succeeds; status reports `skill-authoring 1.0.0`
  and dry-run reports all three links as `ok` with targets under the candidate
  checkout.
- Stable status/dry-run output remains equivalent to the pre-slice baseline,
  stable `skill-authoring` and installed `skill_contract.py` remain absent, and
  all default links still resolve only to the stable checkout.
- The candidate remains unable to mutate canonical planning state and no
  credential is copied or linked.
- Focused authoring/manifest tests, ruff, diff check, installer proof,
  independent review, and delta-only test-quality review are green.

Validation:

- Run the Slice 4 implementation-created source commands.
- After accepted review, run the exact candidate-only install/status/dry-run
  command block.
- Verify link targets with `readlink -f` for the installed skill, validator, and
  schema.
- From the stable checkout, rerun stable status/dry-run and assert stable
  authoring skill/validator absence.
- Re-run the complete authoring test module and the focused manifest ownership
  subset.

Commit message: `feat: register candidate skill authoring`.

Worker brief:

- Follow the shared worker brief. Change only registration tests and adjacent
  docs; do not run the installer or mutate either Codex home.

Reviewer brief:

- Follow the shared reviewer brief. Verify exact feature links, agent-facing
  classification, zero command-owner runtime dependency, and no unrelated
  manifest/version change before the coordinator installs.

Stop conditions:

- Stop if feature registration requires modifying the accepted validator,
  schema, installer implementation, or existing feature versions.
- Stop before installation on any source validation or review failure.
- Stop if any candidate link resolves outside the candidate checkout or any
  stable link/home state changes.
- Stop if installation requires credentials, default-generation switching, or
  canonical planning writes.

## Final Validation

After Slice 4 is committed and candidate-only installation is green, the
coordinator must:

1. Use a fresh strict live execution lease and validate the exact final
   candidate range and read-only stable planning scope.
2. Run the complete `tests/test_skill_authoring.py` module.
3. Run the 42-test skill-contract suite and 25-test planning-schema suite.
4. Run the focused manifest ownership/registration subset, the 33-test
   cross-checkout/custom-agent subset, ruff on changed Python tests, and
   `git diff --check` over the exact candidate range.
5. Re-run candidate installer status/dry-run and verify the three installed
   `skill-authoring` feature links resolve only to the candidate checkout.
6. Re-run stable status/dry-run and confirm the stable authoring skill and
   installed validator remain absent with no changed default link target.
7. Run the full manifest suite only as a `known-red-baseline` diagnostic. It
   must reproduce exactly the same three unrelated failures and 18 passes; any
   different result is a blocker requiring classification, not silent scope
   expansion.
8. Run independent final review over the exact candidate range and the compact
   candidate/stable installation evidence.
9. Run final exact-range `test-quality-review` in `delta-only` mode.
10. Confirm the candidate diff touches only the seven validated paths or file
    areas, no command owner requires `skill-authoring`, and no CCFG-23+
    implementation began.
11. Write `completed-slices.md` and `closeout.md`, reconcile CCFG-22 only, clear
    selected/queued/active state, and stop before successor selection.

No full project pytest suite, package install, generated-doc refresh,
graph/index refresh, default-home install, or candidate canonical planning
session is authorized.

## Stop Conditions

- Stop if Planning State no longer reports this same queued runway and selected
  scope as current.
- Stop if the canonical first-handoff preflight returns `blocked` or any later
  live lease/write-scope validation fails.
- Stop if the candidate worktree contains unrelated changes before a slice or a
  task-scoped diff escapes its allowlist.
- Stop if implementation changes the closed CCFG-20/21 schemas or validators,
  creates a parallel authoring owner/dialect, or retains a placeholder producer
  identity.
- Stop if ownership ambiguity is silently resolved, generic writing becomes a
  contract-owned decision, or the skill executes/mutates the workflow it
  authors.
- Stop if the planning reference accepts an unsupported schema or redefines the
  core contract.
- Stop if either trial modifies or copies live skills, preserves accidental
  topology, or starts command-owner migration.
- Stop if any command owner or support runtime gains a runtime dependency on
  `skill-authoring`.
- Stop if candidate installation touches the stable home, mixes generation
  links, requires credentials, or enables candidate canonical writes.
- Stop if the known-red manifest baseline changes or work expands to remediate
  its unrelated assertions.
- Stop on failed focused validation, actionable unresolved review,
  test-quality concerns, unexpected repository movement, missing subagent
  support, or scope drift.
- Stop closeout before selecting, refreshing, dispatching, creating, or
  preparing CCFG-23 or any other successor.
