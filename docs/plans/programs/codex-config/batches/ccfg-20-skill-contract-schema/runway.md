# CCFG-20 Skill Contract Schema Runway

## Purpose

Implement the accepted `skill-contract/v1` schema and deterministic validators
as one deep, repo-local module in the candidate checkout. This runway covers
CCFG-20 only. It proves the schema and validator against explicit fixture
catalogs without migrating current skills or installing a new runtime feature.

Closeout may mark CCFG-20 `Closed` only when all five COR-003 acceptance keys
are green. Otherwise preserve the exact blocker and stop without selecting a
successor.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slices 1 through 4 risk: `migration`.
- Authorized migration: add the target structural schema, repo-local validator,
  dependency lock, tests, fixture catalogs, and changelog entry.
- Existing skill migration: forbidden.
- Workflow ownership transfer: forbidden.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Destructive or contract-narrowing approval gates: none, because no such
  slice is authorized.
- Candidate-checkout filesystem approval may be required at execution time.
  That approval authorizes access only and does not widen scope.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at
  `/home/alacasse/projects/codex-config/docs/plans`.
- Planning-state `current` and `validate` pass with no blockers and only the two
  known redirect-ledger warnings.
- Selected dispatch, queued runway, and active runway were all `None` before
  this planning pass.
- Stable checkout: `/home/alacasse/projects/codex-config`, branch `master`,
  exact `HEAD` `7c1c02756d76baf65ac9f981bbcbb37ed807d1ba`.
- Candidate checkout:
  `/home/alacasse/projects/codex-config-command-owner-redesign`, branch
  `implementation/command-owner-redesign`, exact `HEAD`
  `13d7f63d258c82760a330a9a61e62ea99d7a493f`.
- Both worktrees were clean before planning. Planning performs no candidate
  write.
- Stable installer status and dry-run pass; the installed strict-context helper
  resolves to the stable checkout.
- CCFG-19 is closed. DEC-036 accepts closed-world v1 evolution, explicit
  compatibility exceptions, named migration conditions, and producer identity.
- The accepted format defines one `## Contract` YAML block, required structural
  fields, four audience profiles, catalog ownership/dependency rules, explicit
  reference loading, and four deterministic migration guards.
- The older required-field list omits `producer`, but DEC-036 is later accepted
  authority. The v1 schema must require `producer` and require
  `producer.schema_version: skill-contract/v1`.
- The candidate has no PyYAML or jsonschema runtime dependency, no
  `skill-contract/v1` schema, and no validator module.
- Current skills have not migrated to the new contract, so fixture catalogs are
  the required-green validation surface in this batch.
- Current focused baseline is green: 33 cross-checkout/custom-agent tests and
  3 manifest schema tests pass. The full manifest remains at its documented
  known-red baseline of 3 failures and 18 passes in unrelated exact-wording
  assertions.

The queued stable planning artifacts are expected dirty coordination state.
Do not copy them into the candidate checkout. If either repository `HEAD`
moves, regenerate and revalidate the strict context before delegation.

## Batch Non-Goals

- Do not add Contract blocks to `skills/*/SKILL.md`.
- Do not require the current whole skills directory to validate as v1.
- Do not add planning-artifact schemas, ledger-store, planning transactions, or
  command-owner behavior.
- Do not implement or modify `skill-authoring`.
- Do not register an installed feature, edit `codex-features.json`, install the
  candidate, or switch the default generation.
- Do not preserve old workflow owners through aliases, compatibility readers,
  or topology tests.
- Do not infer ownership, reference, or migration facts from arbitrary prose.
- Do not hand-write a YAML parser or duplicate JSON Schema structural rules in
  procedural validator code.

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

Planning loaded the installed stable helper, verified that it resolves under
the declared toolchain root, parsed the complete payload, and called
`validate_write_scope` with the exact four canonical planning paths and nine
intended candidate file areas. Validation passed.

Before every worker or reviewer delegation, the coordinator must follow
`skills/batch-runway/references/cross-checkout-context-v1.md`, revalidate the
then-current payload and intended paths, and pass the payload, canonical
planning root, absolute helper path, and write-bearing/read-only mode. Every
explicit cross-checkout agent result must carry matching non-null
`verified_cross_checkout_context` evidence.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/`.
- Planning artifact layout: Planning Artifact Layout v1.
- Program root: `docs/plans/programs/codex-config/`.
- Selected batch directory:
  `docs/plans/programs/codex-config/batches/ccfg-20-skill-contract-schema/`.
- Program archive root: `docs/plans/archive/`.
- Run artifact root: `None`.
- Output root: `None`.
- Validation profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Runway density: `full-runway`.
- Integration harness: repo-local validator CLI over explicit valid and invalid
  fixture catalogs.
- Harness output: stdout/stderr only; no generated durable output.
- Summary artifacts: this runway, `completed-slices.md`, and `closeout.md`.
- Index refresh: none.
- Commit requirements: one focused candidate commit per accepted slice plus a
  separate stable planning-ledger receipt after each candidate hash exists.
- Dirty-file constraints: candidate starts clean and may change only active
  slice files; stable changes are limited to this batch's planning artifacts
  and same-batch reconciliation.
- Test quality review: not requested.

## Module Interface And Slice Handoff

The seam is `scripts/skill_contract.py`. It owns Contract-block extraction,
YAML loading, JSON Schema application, catalog validation, explicit graph
checks, comparison guards, deterministic diagnostics, and the CLI adapter.

Expose `validate_skill_contracts(...)` as the one deep validation interface. It
accepts explicit contract document paths, an explicit toolchain root, expected
producer identity when the caller has it, and optional explicit before/after
catalogs plus migration policy. It returns parsed contracts and
deterministically sorted diagnostics. Keep parsing, schema-library details,
graph traversal, and diagnostic assembly private.

Slice 1 establishes this interface and the canonical JSON Schema. Slices 2
through 4 must extend and consume the same interface; they may not add parallel
parsers, audience validators, graph validators, migration modules, or private
schema copies.

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

Overrides:

- Candidate implementation commits and stable planning-ledger receipt commits
  are distinct cross-repository commits. Record both hashes per slice.
- The validator and schema remain repo-local in CCFG-20. Candidate installation
  and manifest registration are forbidden even if tests are green.
- Workers may use the locked repo-owned `uv` environment for assigned focused
  validation. They may not install ambient packages or run installer commands.

## Validation Profile And Status Classes

Profile: `project-harness-production`.

Environment prefix for repo-owned validation:

```text
UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools
```

Current required-green baseline commands, already passed from the candidate
checkout using the stable locked environment:

- `PYTHONDONTWRITEBYTECODE=1 /home/alacasse/projects/codex-config/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cross_checkout_context.py tests/test_custom_agent_contracts.py`
  - Result: 33 passed and 187 subtests passed.
- `PYTHONDONTWRITEBYTECODE=1 /home/alacasse/projects/codex-config/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_codex_features_manifest.py -k 'manifest_feature_requirements_are_valid or manifest_catalog_distinguishes_user_and_agent_facing_skills or custom_agent_toml_files_are_valid'`
  - Result: 3 passed, 18 deselected, and 31 subtests passed.

Implementation-created commands:

- Slice 1 creates and then promotes to required-green:
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen pytest -q tests/test_skill_contract_schema.py`
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen ruff check scripts/skill_contract.py tests/test_skill_contract_schema.py`
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen basedpyright scripts/skill_contract.py`
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/schema/valid`
  - `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/schema/invalid-unknown-field; status=$?; test "$status" -eq 1'`
- Slice 2 creates and then promotes to required-green:
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen pytest -q tests/test_skill_contract_catalog.py`
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/valid-ownership`
  - `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/invalid-duplicate-owner; status=$?; test "$status" -eq 1'`
- Slice 3 creates and then promotes to required-green:
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/valid-references`
  - `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/invalid-reference-cycle; status=$?; test "$status" -eq 1'`
- Slice 4 creates and then promotes to required-green:
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen pytest -q tests/test_skill_contract_migration.py`
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py compare --toolchain-root . --policy tests/fixtures/skill-contracts/migration/policy.json tests/fixtures/skill-contracts/migration/before tests/fixtures/skill-contracts/migration/after-valid`
  - `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py compare --toolchain-root . --policy tests/fixtures/skill-contracts/migration/policy.json tests/fixtures/skill-contracts/migration/before tests/fixtures/skill-contracts/migration/after-retained-owner; status=$?; test "$status" -eq 1'`

Required-green after their creating slices:

- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen pytest -q tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen ruff check scripts/skill_contract.py tests/test_skill_contract_schema.py tests/test_skill_contract_catalog.py tests/test_skill_contract_migration.py`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen basedpyright scripts/skill_contract.py`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/schema/valid`
- `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/schema/invalid-unknown-field; status=$?; test "$status" -eq 1'`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/valid-ownership`
- `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/invalid-duplicate-owner; status=$?; test "$status" -eq 1'`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/valid-references`
- `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/invalid-reference-cycle; status=$?; test "$status" -eq 1'`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py compare --toolchain-root . --policy tests/fixtures/skill-contracts/migration/policy.json tests/fixtures/skill-contracts/migration/before tests/fixtures/skill-contracts/migration/after-valid`
- `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py compare --toolchain-root . --policy tests/fixtures/skill-contracts/migration/policy.json tests/fixtures/skill-contracts/migration/before tests/fixtures/skill-contracts/migration/after-retained-owner; status=$?; test "$status" -eq 1'`
- `git diff --check`

Known-red-baseline command:

- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen pytest -q tests/test_codex_features_manifest.py`
  - Baseline: 3 failed and 18 passed in unrelated exact-wording assertions.
  - Expected failures:
    `test_executable_work_source_boundary_is_explicit`,
    `test_plan_batch_command_owner_runtime_boundaries_are_explicit`, and
    `test_work_batch_reconciles_same_batch_closeout`.
  - Role: diagnostic only. This batch must not silently promote it or absorb
    command-owner prose remediation.

Conditional commands:

- `./install.sh --status` and `./install.sh --dry-run` run only if an unexpected
  diff touches installed-feature metadata. Such a diff is a scope violation and
  stops the batch; no candidate installation follows.

No per-slice worker may run a full project suite, installer mutation, generated
docs refresh, graph/index refresh, or final validation.

## Shared Worker And Reviewer Briefs

Worker brief for every slice:

- You are the already-required `runway_worker`. Implement only the active slice
  from this runway; do not spawn, delegate to, or wait on another agent.
- Independently validate the strict cross-checkout context before acting, then
  write only inside the candidate checkout and only to the active slice's
  allowed files.
- Keep stable planning files, accepted history, and unrelated candidate files
  read-only.
- Extend the single `scripts/skill_contract.py` interface. Do not add parallel
  parser, schema, graph, migration, or CLI owner modules.
- Do not migrate current skills, register installed features, edit the manifest,
  change command-owner behavior, or implement later findings.
- Run only the focused validation assigned to the slice and return the
  registered v2 worker result with matching
  `verified_cross_checkout_context`.

Reviewer brief for every slice:

- The coordinator supplies the exact candidate commit hash or task-scoped
  candidate worktree diff basis. Echo it as `diff_basis` in the registered v2
  reviewer result.
- Independently validate the strict cross-checkout context before review.
- Verify accepted-schema fidelity, fail-closed behavior, deterministic sorted
  diagnostics, root containment, and absence of arbitrary prose inference.
- Reject duplicated structural owners, hand-written YAML, project-specific
  migration names, hidden current-skill migration, or installed-surface drift.
- Review tests through the public module interface and CLI, not private helper
  topology. Return matching `verified_cross_checkout_context` and a clear
  accept/fix/block verdict.

## Active Ledger

| Slice | Risk | Status | Candidate commit | Stable receipt | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|---|
| 1. Schema and interface | migration | pending | | | | | Schema tests, Ruff, basedpyright, independent review | |
| 2. Ownership and profiles | migration | pending | | | | | Catalog tests and independent review | |
| 3. Delegation and references | migration | pending | | | | | Graph/root cases and independent review | |
| 4. Migration guards and integration | migration | pending | | | | | Migration tests, CLI proof, final validation | |

## Completed Slice Archive

| Slice | Risk | Candidate commit | Stable planning receipt | Outcome | Audit references |
|---|---|---|---|---|---|

## Slice 1: Establish Closed-World Schema And Interface

Risk: `migration`.

Scope:

- Add `schemas/skill-contract-v1.schema.json` as the canonical Draft-07
  structural schema.
- Add `scripts/skill_contract.py` with one deep validation interface and a thin
  CLI adapter.
- Add PyYAML and jsonschema runtime dependencies to `pyproject.toml` and lock
  them in `uv.lock`.
- Add schema-focused tests and small valid/invalid fixture catalogs.

Allowed files:

- `schemas/skill-contract-v1.schema.json`
- `scripts/skill_contract.py`
- `tests/test_skill_contract_schema.py`
- `tests/fixtures/skill-contracts/schema/**`
- `pyproject.toml`
- `uv.lock`

Non-goals:

- No cross-document ownership, dependency, reference, or migration comparison
  behavior beyond interface placeholders needed for later slices.
- No current skill migration or manifest registration.

Acceptance criteria:

- Exactly one `## Contract` fenced YAML block is required; zero or multiple
  blocks fail with deterministic path-qualified diagnostics.
- The schema requires the accepted fields plus `producer`, rejects unknown
  versions, and recursively rejects unknown v1 object fields except through an
  explicit schema-specific accepted compatibility policy.
- Audience is one of `human-command-owner`, `support-mechanism`,
  `evidence-skill`, or `authoring-support`.
- Producer generation is `stable` or `candidate`, producer commit is a full
  SHA, and producer schema version equals `skill-contract/v1`. A caller may
  provide expected producer identity for equality validation; cwd is never
  inferred.
- PyYAML parses accepted YAML and jsonschema applies the canonical schema; the
  module does not implement a second structural schema in code.
- Diagnostics are stable and sorted.
- The public interface and CLI validate explicit fixture paths only.
- CLI validation exits `0` for a valid catalog and `1` for deterministic
  validation findings; usage errors remain distinct. Expected-failure harness
  commands must assert exit `1` and themselves return `0`.

Validation:

- Run the Slice 1 implementation-created commands, then `git diff --check`.

Commit message: `feat: add skill contract schema validator`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
compare the JSON Schema to the accepted format and DEC-036 producer rules.

Stop conditions:

- Stop if the dependency lock cannot be generated reproducibly.
- Stop if schema behavior requires a hand-written YAML parser or duplicated
  structural field tables.
- Stop if implementation touches current skills or installed feature metadata.

## Slice 2: Validate Catalog Ownership And Audience Profiles

Risk: `migration`.

Scope:

- Extend the Slice 1 interface with catalog-wide ownership and audience-profile
  validation.
- Add focused catalog tests and fixtures.

Allowed files:

- `scripts/skill_contract.py`
- `tests/test_skill_contract_catalog.py`
- `tests/fixtures/skill-contracts/catalog/**`

Non-goals:

- No dependency/reference cycles or migration comparison yet.
- No semantic duplicate detection beyond controlled identifiers.

Acceptance criteria:

- Reject a contract that both owns and forbids the same controlled decision or
  write.
- Reject duplicate command-owner decisions and duplicate durable facts unless
  an explicit shared-mechanism policy input authorizes the named fact.
- Reject support mechanisms that own human workflow decisions.
- Reject evidence skills that own selection, queue, execution, or closeout
  state using accepted controlled identifiers only.
- Reject unknown delegated targets at catalog validation time.
- Do not invent constraints for `authoring-support` beyond accepted structured
  rules.
- All diagnostics are deterministic, sorted, and path-qualified.

Validation:

- Run the schema and catalog tests, the Slice 2 valid/invalid CLI commands,
  Ruff over both test modules and the owner, basedpyright over the owner, then
  `git diff --check`.
- Slice-local CLI harness commands:
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/valid-ownership`
  - `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/invalid-duplicate-owner; status=$?; test "$status" -eq 1'`

Commit message: `feat: validate skill contract ownership`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
exercise each audience profile and explicit shared-mechanism exception.

Stop conditions:

- Stop if an audience rule cannot be tied to accepted structured evidence.
- Stop if catalog validation needs project names or prose interpretation.

## Slice 3: Validate Delegation, Dependencies, And References

Risk: `migration`.

Scope:

- Extend the same module interface with delegation, required-mechanism, and
  structured-reference graph validation.
- Add missing-target, dependency-cycle, reference-cycle, and root-containment
  cases to the catalog test/fixture surface.

Allowed files:

- `scripts/skill_contract.py`
- `tests/test_skill_contract_catalog.py`
- `tests/fixtures/skill-contracts/catalog/**`

Non-goals:

- No graph edges inferred from prose or arbitrary Markdown links.
- No installer dependency reuse or coupling to installer lifecycle semantics.

Acceptance criteria:

- Delegation and required-mechanism targets resolve against the explicit
  catalog or an explicit allowed external-mechanism policy.
- Dependency and reference cycles are rejected with stable cycle diagnostics.
- Only `references[*].path` creates a reference edge; `load_when` remains the
  canonical trigger data and prose creates no edge.
- Missing references, non-files, and paths outside the explicit toolchain root
  fail closed.
- Symlink and `..` escapes are rejected after strict resolution.
- The implementation may reuse the repository's visited/visiting DFS pattern
  conceptually but does not import installer-private helpers.

Validation:

- Run schema and catalog tests, the Slice 3 valid/invalid reference CLI
  commands, Ruff, basedpyright, and `git diff --check`.
- Slice-local CLI harness commands:
  - `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/valid-references`
  - `sh -c 'UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --frozen python scripts/skill_contract.py validate --toolchain-root . tests/fixtures/skill-contracts/catalog/invalid-reference-cycle; status=$?; test "$status" -eq 1'`

Commit message: `feat: validate skill contract references`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
inspect actual resolved fixture paths and verify every edge is structured.

Stop conditions:

- Stop if root containment is inferred from cwd.
- Stop if cycle detection requires scanning unstructured prose.

## Slice 4: Add Migration Guards And Integration Proof

Risk: `migration`.

Scope:

- Extend the same interface with explicit before/after catalog comparison and
  controlled migration policy inputs.
- Add migration tests and fixtures.
- Complete CLI validation and comparison commands over explicit fixtures.
- Update `CHANGELOG.md` with the problem, decision, expected effect, and
  intentionally repo-local boundary.

Allowed files:

- `scripts/skill_contract.py`
- `tests/test_skill_contract_migration.py`
- `tests/fixtures/skill-contracts/migration/**`
- `CHANGELOG.md`

Non-goals:

- No hard-coded APR, Batch Runway, codex-config, or project-specific owner names.
- No installation, manifest registration, or current skill migration.

Acceptance criteria:

- Explicit policy inputs name retired broad owners and expected ownership
  transfers; the validator never guesses them.
- Before/after comparison deterministically reports retained broad-owner
  dependencies, expected ownership that did not move, duplicated durable facts,
  and a rename without contract change.
- Same key/different policy or ambiguous catalog identity fails rather than
  silently selecting a comparison.
- CLI success and failure exit codes are stable and exercise the same deep
  module interface as tests.
- The final evidence proves:
  `schema_green`, `ownership_conflict_tests_green`,
  `delegation_reference_tests_green`, `schema_compatibility_tests_green`, and
  `deterministic_migration_guard_green`.
- `codex-features.json` remains unchanged and the changelog names CCFG-22 as the
  future runtime-consumer/install decision owner.

Validation:

- Run all three skill-contract test modules, Ruff, basedpyright, the two current
  required-green baseline commands, and the exact Slice 1 through 4 CLI
  success/expected-failure commands listed above, then `git diff --check`.
- Run the known-red manifest command diagnostically and confirm it does not
  gain new failures.

Commit message: `feat: guard skill contract migrations`.

Subagent briefs: use the shared worker and reviewer briefs. The reviewer must
compare every migration diagnostic to explicit before/after evidence and policy.

Stop conditions:

- Stop if a guard needs arbitrary prose understanding or a project-specific
  owner name.
- Stop if the full manifest gains a failure or its known-red set changes.
- Stop if CLI behavior bypasses the module interface.

## Final Validation And Closeout

After Slice 4 review and commit:

1. Revalidate the strict context and exact candidate/stable revisions.
2. Run all required-green commands in this runway from the candidate checkout.
3. Run the known-red manifest command diagnostically and compare exact failures
   to the baseline.
4. Run `git diff --check` over the complete candidate range.
5. Verify the candidate range changes only the nine intended candidate areas
   and never changes `codex-features.json` or existing skills.
6. Obtain independent final review over the exact candidate commit range and
   task-scoped stable planning diff.
7. Create `completed-slices.md` and `closeout.md`, then reconcile CCFG-20 and
   the program queue under `work-batch` same-batch closeout ownership.
8. Stop before selecting or preparing CCFG-21.

Close CCFG-20 only when all five COR-003 acceptance keys are true with command,
fixture, commit, and review evidence.

## Global Stop Conditions

- Stop on strict-context mismatch, unexpected `HEAD` movement, or candidate
  worktree conflict.
- Stop on changes outside active slice allowlists.
- Stop if a current skill, installed feature, command owner, planning artifact
  schema, or later finding enters scope.
- Stop if validation relies on ambient packages, arbitrary prose semantics, or
  cwd-inferred roots/identity.
- Stop if deterministic diagnostics depend on filesystem enumeration order.
- Stop on repeated validation failure, stale review basis, or missing registered
  worker/reviewer support.
- Stop closeout before successor selection.

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Convergence Assessment

- Phase: queued.
- Scope trend: fixed to one schema/validator module and fixture catalogs.
- Closed: none.
- Deferred: current skill migration and CCFG-21 through CCFG-29.
- Temporary bridge: strict cross-checkout context retained through CCFG-29.
- Cleanup residue: none created; installed surface intentionally absent.
- Blockers: none.
- Completion forecastable: yes, four bounded slices and five exit keys.
- Next proof required: Slice 1 schema/interface implementation with green
  focused validation and independent review.
