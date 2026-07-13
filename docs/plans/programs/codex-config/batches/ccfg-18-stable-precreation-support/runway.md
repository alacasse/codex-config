# CCFG-18 Stable Pre-Creation Support Runway

## Purpose

Implement and validate the temporary `cross-checkout-precreation/v1` stable
control surface that authorizes only the later creation of two exact absent
candidate paths. Preserve strict `cross-checkout-context/v1` as the unchanged
post-creation contract, wire the new mechanical facts through existing stable
consumers, expose them through the existing manifest-driven installation, and
stop before installation, reload, or candidate creation.

This runway covers the bounded stable-support amendment to CCFG-18 only. It
does not close CCFG-18 and does not select CCFG-19.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`.
- Slice 1 risk: `migration`.
- Slice 2 risk: `migration`.
- Slice 3 risk: `migration`.
- Destructive cleanup: forbidden.
- Contract narrowing: forbidden.
- Approval gates: none required because no slice may delete, demote, narrow, or
  remove a supported contract.

The migration adds a separate temporary interface and consumer path. Existing
strict-context behavior must remain green and unchanged.

## Current Baseline And Assumptions

- Planning Artifact Layout v1 is active at `docs/plans/`.
- Program root:
  `docs/plans/programs/codex-config/`.
- Selected dispatch: `None` before this planning pass.
- Queued batch: `None` before this planning pass.
- Active runway: `None` before this planning pass.
- `planning_state.py current` and `validate` pass; validation reports only the
  two known redirect-ledger warnings.
- Stable checkout: `/home/alacasse/projects/codex-config` on `master` at
  `20b792888481dd9db1e3fa4b90831500eda509f1`.
- Origin identity: `https://github.com/alacasse/codex-config.git`.
- Installed feature versions match `codex-features.json`, and repo-owned links
  resolve to the stable checkout.
- Intended candidate repository:
  `/home/alacasse/projects/codex-config-command-owner-redesign`; absent.
- Intended candidate `CODEX_HOME`:
  `/home/alacasse/.codex-command-owner-redesign`; absent.
- Existing strict-context tests pass with `21 passed, 31 subtests passed`.
- Focused existing cross-checkout consumer/agent tests pass with
  `4 passed, 27 deselected, 52 subtests passed`.
- Full custom-agent contract tests pass with
  `10 passed, 136 subtests passed`.
- Focused touched-file Ruff and basedpyright pass with zero errors.
- `./install.sh --status` and `./install.sh --dry-run` pass; dry-run writes no
  installed state.
- Full `tests/test_codex_features_manifest.py` has a known unrelated baseline
  of `3 failed, 18 passed, 81 subtests passed`; the three failures are wording
  expectations outside this batch's pre-creation scope.
- Batch Runway create-spec and lifecycle guards pass with
  `21 passed, 208 subtests passed`.

This is an ordinary single-root stable-control runway. It does not carry a
`cross-checkout-context/v1` or `cross-checkout-precreation/v1` execution
payload because the batch does not act in the absent candidate root. The new
pre-creation contract is implementation output for a later fresh session, not
the control context for this runway.

Expected pre-existing dirty files at planning time:

- `docs/plans/programs/codex-config/CURRENT.md`
- `docs/plans/programs/codex-config/LEDGER.md`
- `docs/plans/programs/codex-config/findings/command-owner-redesign-bootstrap-decisions.md`
- `docs/plans/programs/codex-config/findings/command-owner-redesign-implementation-intake.md`

Those edits are classified source and planning input. Workers must preserve
them and must not stage or commit them. The coordinator may update only this
batch's active ledger, completed-slice archive, closeout, and the program's
same-batch queue/closeout fields.

## Project Values

- Planning location:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-precreation-support/`.
- Run artifact root: `None`; no runner JSON or telemetry is created.
- Output root: `None`; validation output is command stdout only.
- Integration harness: `./install.sh --dry-run`.
- Harness output: stdout; no generated artifact.
- Summary evidence: `./install.sh --status` before implementation and dry-run
  output after manifest changes.
- Index or generated-doc refresh: none.
- Commit strategy: one focused commit after each independently green and
  reviewed slice, then one self-referential closeout commit if required.

## Non-Goals

- Do not create the candidate repository or candidate `CODEX_HOME`.
- Do not create the candidate branch, merge accepted design history, or
  validate real candidate lineage.
- Do not use the new interface to control real work in the loaded session.
- Do not install or reload changed stable control.
- Do not weaken, alias, or replace `cross-checkout-context/v1`.
- Do not add a second helper, installer path, human-facing command, or broad
  workflow owner when the existing owner can stay deep.
- Do not modify planning-state implementation or schemas.
- Do not select CCFG-19 or any successor work.

## Execution Contract

Use Batch Runway Standard Execution Contract v2.
Use Batch Runway Registered Agent Result Contract v2. Registered agent TOMLs
own worker and reviewer result schemas.
Use Batch Runway Compact Report Contract v1 only for coordinator receipts and
its non-agent reporting rules under the v2 compatibility statement.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for suspicious coordinator or
subagent-lifecycle behavior only.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/validation-profiles/project-harness-production.md`

Overrides: none.

Execution boundaries for this batch:

- The main agent coordinates; every implementation slice is delegated to
  `runway_worker`, and a separate `runway_reviewer` reviews the exact diff
  before commit.
- Workers do not run the full test suite, real installation, planning-state
  writes, candidate-path operations, final validation, or commits.
- The coordinator owns focused/final validation, review delegation, ledger and
  archive updates, commits, and same-batch closeout.
- Because the selected `project-harness-production` profile treats installed
  helper and consumer changes as harness-affecting, the coordinator runs
  `./install.sh --dry-run` after every slice; workers never run it.
- Changed stable control must not be installed, reloaded, or used for real
  coordination during this batch.

## Validation Profile

Selected profile: `project-harness-production`.

Focused validation commands:

- `python scripts/planning_state.py current --root docs/plans`
  - Status class: `required-green`.
  - Baseline: passed with no blockers.
- `python scripts/planning_state.py validate --root docs/plans`
  - Status class: `required-green`.
  - Baseline: passed with two known redirect-ledger warnings.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_cross_checkout_context.py`
  - Status class: `required-green`.
  - Baseline: `21 passed, 31 subtests passed`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_cross_checkout_precreation.py`
  - Status class: `implementation-created`.
  - Slice 1 creates this focused behavior module before promotion to
    `required-green`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_custom_agent_contracts.py`
  - Status class: `required-green`.
  - Baseline: `10 passed, 136 subtests passed`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_codex_features_manifest.py -k 'cross_checkout or runway_worker or runway_reviewer'`
  - Status class: `required-green`.
  - Baseline: `4 passed, 27 deselected, 52 subtests passed`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_batch_runway_create_spec_contract.py tests/test_batch_lifecycle_guards.py`
  - Status class: `required-green`.
  - Baseline: `21 passed, 208 subtests passed`.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_codex_features_manifest.py`
  - Status class: `known-red-baseline`.
  - Baseline: `3 failed, 18 passed, 81 subtests passed` in unrelated existing
    wording expectations. This command is diagnostic and must not hide new
    failures in cross-checkout or version assertions touched by this batch.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline ruff check scripts tests`
  - Status class: `required-green`.
  - Baseline for the existing helper and tests: passed.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline basedpyright scripts/cross_checkout_context.py`
  - Status class: `required-green`.
  - Baseline: zero errors, warnings, or notes.
- `./install.sh --status`
  - Status class: `required-green` before implementation.
  - Baseline: installed feature versions match the manifest and repo-owned
    links resolve to the stable checkout.
- `./install.sh --dry-run`
  - Status class: `required-green`.
  - Baseline: passed; execution must remain dry-run only.
- `python -m json.tool codex-features.json`
  - Status class: `required-green`.
- `git diff --check`
  - Status class: `required-green`.

The project has no separate generated-output refresh for this scope. The full
pytest suite is not a slice gate; focused behavioral, consumer-contract,
agent-contract, manifest, lint, type, and install dry-run evidence owns this
batch.

## Active Ledger

| Slice | Status | Risk class | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|
| 1. Pre-creation owner and transition evidence | pending | migration | | | | Focused helper behavior and strict regression tests green | Candidate paths remain absent |
| 2. Stable consumer and agent propagation | pending | migration | | | | Consumer and agent contract tests green | Reusable text remains project-neutral |
| 3. Manifest and release wiring | pending | migration | | | | Manifest, dry-run, final validation, and review green | Stop before real install or reload |

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|

## Slice 1: Pre-Creation Owner And Transition Evidence

Risk class: `migration`.

Scope:

- Extend `scripts/cross_checkout_context.py` as the single mechanical owner of
  both separate interfaces without changing strict `cross-checkout-context/v1`
  semantics.
- Add an exact `cross-checkout-precreation/v1` parser and validator for stable
  control, candidate intent, and creation authority.
- Validate existing stable repository roots and revisions, stable generation
  binding, absolute intended candidate paths, absent candidate repository and
  candidate `CODEX_HOME`, base repository identity, full base revision,
  explicit branch name, accepted design snapshot, and the two exact authorized
  creation roots.
- Reject protected-root overlap, relative or duplicate targets, unexpected
  existing state, revision drift, and authority broader than the declared
  intent before any caller hook.
- Add versioned transition-receipt data that can later prove the created
  repository/environment match the pre-creation intent and the validated
  strict context. The helper remains apply-free and decision-free.
- Create focused positive and negative tests using temporary repositories and
  paths only; retain the existing strict-context suite as a regression gate.

Allowed files or areas:

- `scripts/cross_checkout_context.py`
- `tests/test_cross_checkout_precreation.py`
- `tests/test_cross_checkout_context.py` only for strict non-regression
  assertions that cannot live in the new focused module

Non-goals:

- Do not wire skills, agents, or manifest versions yet.
- Do not create real candidate paths or perform repository/environment
  creation through the helper.
- Do not infer workflow lifecycle decisions from mechanical validation.
- Do not permit an empty existing candidate target to masquerade as the
  declared `absent` v1 state.

Acceptance criteria:

- The new parser accepts exactly the versioned three-part pre-creation shape
  and rejects missing, extra, mistyped, relative, overlapping, or stale facts.
- Only the exact intended repository and candidate-home targets are authorized;
  parent roots, siblings, descendants, and undeclared targets are rejected.
- Stable toolchain and canonical planning repository identity and revisions are
  revalidated before a caller hook.
- Transition evidence binds pre-creation identity, actual created candidate
  identity, and the strict context without claiming that this batch performed
  a real transition.
- Existing strict-context tests remain unchanged-green.
- Focused tests, Ruff, basedpyright, and `git diff --check` pass.

Validation:

- Promote the pre-creation test command to `required-green`.
- Run the existing strict-context test module.
- Run touched-file Ruff and basedpyright.
- Have the coordinator run `./install.sh --dry-run` after focused validation.
- Run `git diff --check`.

Test quality review: required for the new negative-path and transition
assertions; tests must prove externally observable fail-closed behavior rather
than private topology.

Commit message:

`Add cross-checkout precreation contract`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 1, do not spawn, delegate to, or wait on additional agents, do not
touch planning state or either candidate path, preserve the strict interface,
and return the task-scoped diff plus focused validation; do not commit.

Review subagent brief:

Review the exact task-scoped diff basis supplied by the coordinator. Confirm
separate interface identity, fail-closed ordering before caller hooks, exact
creation authority, stable/revision validation, strict-context non-regression,
behavioral test strength, and absence of workflow authority or real candidate
writes. Echo `diff_basis` in compact YAML.

Stop conditions:

- Stop if supporting pre-creation requires weakening strict repository or
  revision checks.
- Stop if a network lookup or a real candidate path is required for tests.
- Stop if the helper would create paths, clone repositories, install state, or
  accept execution/closeout.

## Slice 2: Stable Consumer And Agent Propagation

Risk class: `migration`.

Scope:

- Add a reusable
  `skills/batch-runway/references/cross-checkout-precreation-v1.md` consumer
  contract that resolves and validates the installed helper, preserves the
  complete payload, distinguishes pre-creation from strict post-creation work,
  and requires the versioned transition before later implementation continues.
- Update `plan-batch` so a later explicitly pre-creation dispatch can validate
  absent intended targets without creating them during planning.
- Update `work-batch` and Batch Runway create/execute contracts so pre-creation
  facts are revalidated and propagated until the strict-context transition;
  ordinary single-root and strict cross-checkout behavior stay unchanged.
- Extend registered worker/reviewer result contracts with explicit nullable
  pre-creation verification facts. The coordinator rejects missing or
  mismatched facts for an explicit pre-creation handoff and retains all
  lifecycle decisions.
- Add focused consumer-neutrality, routing, transition, and agent-result
  contract tests.

Allowed files or areas:

- `skills/plan-batch/SKILL.md`
- `skills/work-batch/SKILL.md`
- `skills/batch-runway/SKILL.md`
- `skills/batch-runway/references/cross-checkout-precreation-v1.md`
- `skills/batch-runway/references/project-values.md`
- `skills/batch-runway/references/create-spec.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/subagent-briefs.md`
- `agents/runway_worker.toml`
- `agents/runway_reviewer.toml`
- `tests/test_custom_agent_contracts.py`
- `tests/test_codex_features_manifest.py`

Non-goals:

- Do not make pre-creation a step for ordinary single-root work.
- Do not reinterpret pre-creation verification as strict-context verification.
- Do not embed codex-config paths, CCFG identifiers, feature versions, or local
  cache commands in reusable skills or references.
- Do not add a new human-facing command or duplicate lifecycle owner.

Acceptance criteria:

- Explicit pre-creation planning can preserve a complete validated payload
  while candidate targets are absent; it still cannot create those targets.
- Execution revalidates the installed pre-creation owner before applicable
  worker/reviewer handoffs and requires independent agent verification.
- After candidate creation in a future batch, a versioned transition receipt
  and green strict context are mandatory before further implementation.
- Strict `cross-checkout-context/v1` routing and ordinary single-root routing
  remain unchanged.
- Generic reusable surfaces contain no project-specific identity or paths.
- Focused consumer and agent-contract tests pass.

Validation:

- Run the pre-creation and strict helper tests.
- Run full custom-agent contract tests.
- Run focused manifest consumer tests with the existing `-k` expression.
- Run Batch Runway create-spec and lifecycle guard tests.
- Have the coordinator run `./install.sh --dry-run` after focused validation.
- Run touched-file Ruff and `git diff --check`.

Test quality review: required for changed contract tests; assertions must prove
routing, nullability, mismatch rejection, project neutrality, and transition
requirements rather than preserving incidental prose layout.

Commit message:

`Propagate cross-checkout precreation control`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 2, do not spawn or delegate, consume the Slice 1 owner instead of
copying validation, preserve strict and ordinary routing, keep reusable text
project-neutral, and return the task-scoped diff plus focused validation; do
not commit.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm all consumers use the installed
mechanical owner, agent results distinguish pre-creation from strict identity,
the transition gate is enforceable, coordinator lifecycle ownership remains
intact, generic surfaces stay project-neutral, and focused contract tests are
behavioral. Echo `diff_basis` in compact YAML.

Stop conditions:

- Stop if consumers must duplicate helper validation rules.
- Stop if a v1 strict-context result can satisfy a pre-creation handoff or vice
  versa without an explicit validated transition.
- Stop if the agent schema change would silently reinterpret an existing field
  instead of adding an explicit mechanical fact.

## Slice 3: Manifest And Release Wiring

Risk class: `migration`.

Scope:

- Keep `scripts/cross_checkout_context.py` installed only through the existing
  `batch-runway` feature link; do not add a second helper or installer path.
- Bump the affected `plan-batch`, `work-batch`, `batch-runway`, and
  `custom-agents` feature versions once, and update exact manifest expectations.
- Extend focused manifest assertions for the separate pre-creation reference,
  consumer set, agent fields, helper ownership, and project-neutral surfaces.
- Add an Unreleased changelog entry with problem, decision, expected effect,
  temporary ownership, and the fresh-session installation boundary.
- Run manifest JSON validation, installation status/dry-run, final focused
  validation, final review, and same-batch closeout. Do not perform a real
  install.

Allowed files or areas:

- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `CHANGELOG.md`
- This batch's `runway.md`, `completed-slices.md`, and `closeout.md` for
  coordinator-owned execution evidence only
- Program `CURRENT.md` and `LEDGER.md` during same-batch closeout only

Non-goals:

- Do not change `scripts/install_codex_config.py` or installer mechanics.
- Do not perform a real install, reload Codex, or mutate default `CODEX_HOME`.
- Do not create either candidate path.
- Do not close CCFG-18 or select successor work.

Acceptance criteria:

- One installed helper remains the owner of both separate interfaces.
- Every changed installed feature has one correct version bump, and focused
  manifest expectations match those versions and dependencies.
- `./install.sh --dry-run` exposes only stable-checkout sources and writes no
  installed state.
- The changelog accurately distinguishes the pre-creation addition from the
  unchanged strict contract and names the later removal condition at CCFG-29.
- Candidate paths remain absent after final validation.
- Closeout leaves CCFG-18 `Blocked` on stable installation and fresh-session
  reload, clears only this queued batch, keeps the candidate-generation
  remainder under CCFG-18, and selects no successor.

Validation:

- Run all required-green focused commands and compare the known-red full
  manifest diagnostic with its baseline.
- Run `python -m json.tool codex-features.json`.
- Run `./install.sh --status` before version changes and
  `./install.sh --dry-run` after them; do not run real install.
- Run planning-state `current` and `validate` before closeout.
- Run `git diff --check`.

Test quality review: required for changed manifest assertions; tests must prove
single-owner installation, dependency expansion, exact versions, and consumer
availability without asserting accidental file topology beyond the public
manifest contract.

Commit message:

`Install stable precreation support`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 3, do not spawn or delegate, do not alter installer code, do not run
a real install or create candidate paths, keep the changelog factual, and
return the task-scoped diff plus focused validation; do not commit or perform
same-batch closeout.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm manifest ownership and version
bumps, focused test quality, installer dry-run-only behavior, factual release
documentation, strict-interface preservation, absence of candidate/default-home
mutation, and no successor selection. Echo `diff_basis` in compact YAML.

Stop conditions:

- Stop if installer code or a second feature owner is required.
- Stop if any installed link resolves outside the stable checkout.
- Stop if changed stable code would be installed, reloaded, or consumed in the
  same session.

## Final Validation

Required-green:

- Planning-state `current` and `validate`.
- Existing strict-context and new pre-creation helper tests.
- Full custom-agent contract tests.
- Focused cross-checkout/agent manifest tests.
- Batch Runway create-spec and lifecycle guards.
- Ruff over `scripts` and `tests` through the offline repo toolchain.
- Basedpyright over `scripts/cross_checkout_context.py`.
- `./install.sh --dry-run` with no installed-state write.
- `python -m json.tool codex-features.json`.
- `git diff --check`.
- Independent final `runway_reviewer` verdict over the batch commit range.

Known-red diagnostic:

- Full `tests/test_codex_features_manifest.py`: baseline
  `3 failed, 18 passed, 81 subtests passed` in unrelated wording assertions.
  No new failure or changed cross-checkout/version assertion is acceptable.

Final closeout must record the controlling stable commit, changed stable commit
range, helper and consumer validation, dry-run evidence, candidate-path
absence, zero real candidate writes, and the required install/reload handoff.
It must leave CCFG-18 `Blocked` on stable installation and fresh-session
reload, clear only this batch, preserve the candidate-generation remainder,
and stop without selecting CCFG-19.

## Stop Conditions

- Stop if selected, queued, active, or resumable state changes outside this
  batch.
- Stop if strict `cross-checkout-context/v1` is weakened, aliased, or replaced.
- Stop if a stable helper resolves from candidate source.
- Stop if implementation creates or writes the candidate repository or
  candidate `CODEX_HOME`.
- Stop if reusable skill/reference text receives project-specific paths,
  identities, commands, caches, planning layout, or CCFG policy.
- Stop if the pre-creation owner gains semantic workflow authority.
- Stop if work reaches CCFG-19 or later command-owner migration scope.
- Stop if changed stable control is installed, reloaded, or used for real
  coordination in this batch.
- Stop if default `CODEX_HOME` would be mutated or force-installed.
- Stop if closeout would mark CCFG-18 `Closed`, select CCFG-19, or prepare a
  successor dispatch or runway.
