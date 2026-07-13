# CCFG-18 Runway: Stable Control Bootstrap

## Purpose

Implement and wire the stable `cross-checkout-context/v1` mechanism required to
control later command-owner migration work across separate stable planning and
candidate implementation roots. Finish with a committed, validated stable
bootstrap, then stop before installing, reloading, or using that changed control
for real work.

This runway prepares CCFG-18 but does not complete it. Same-batch closeout must
leave the finding `Prepared`; a later explicit `plan-batch` under the fresh
stable generation owns the remaining candidate-generation scope.

## Batch Kind And Slice Risk Contract

- Batch kind: `migration`
- Density: `full-runway`
- Owner seam: temporary `cross-checkout-context/v1` mechanism.
- Deletion condition: CCFG-29 final integration.
- Slice 1 risk: `migration`.
- Slice 2 risk: `migration`.
- Slice 3 risk: `migration`.
- Destructive cleanup: not authorized.
- Contract narrowing: not authorized.
- Mandatory destructive/contract-narrowing approval gate: none.

The mechanism owns root binding, repository identity, write-scope validation,
generation identity capture, and cross-repository receipt format only. It must
not decide intake, selection, scope, runway content, execution acceptance,
closeout meaning, or successor selection.

## Current Baseline And Assumptions

- Planning layout: Planning Artifact Layout v1.
- Planning root: `docs/plans/`.
- Program root: `docs/plans/programs/codex-config/`.
- Selected dispatch:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/dispatch.md`.
- Queued runway:
  `docs/plans/programs/codex-config/batches/ccfg-18-stable-control-bootstrap/runway.md`.
- Controlling generation role: stable.
- Loaded toolchain commit:
  `c0615f63060e07e79101089b5599c8eff05f77f8`.
- Toolchain source root:
  `/home/alacasse/projects/codex-config`.
- Canonical planning repository root:
  `/home/alacasse/projects/codex-config`.
- Canonical planning root:
  `/home/alacasse/projects/codex-config/docs/plans`.
- Current default `CODEX_HOME`:
  `/home/alacasse/.codex`.
- Future implementation target root:
  `/home/alacasse/projects/codex-config-command-owner-redesign`.
- Future candidate `CODEX_HOME`:
  `/home/alacasse/.codex-command-owner-redesign`.
- Both future candidate paths are absent and must remain absent in this batch.
- All 24 repo-owned installed links resolve to the stable checkout; candidate
  links are zero.
- `planning_state.py current` and `validate` passed with only the two known
  redirect-ledger warnings.
- No selected, queued, active, or resumable runner state existed before this
  dispatch/runway pair was created.
- `./install.sh --dry-run` passed and reported only stable-checkout sources.
- Focused existing tests passed with `22 passed`.
- Custom-agent contract tests passed with `9 passed`.
- Planning-state tests passed with `178 passed`.
- Full pytest is a known-red baseline: `16 failed, 398 passed, 484 subtests
  passed` in unrelated command-owner wording, deletion-vocabulary, and
  projection-routing expectations.
- Full `basedpyright scripts` is a known-red baseline with `311 errors`; new or
  already-green touched modules must not add type errors.
- `ruff check scripts tests` passed through the repo-owned offline uv toolchain.

## Required Execution Context

The implementation must define and validate this versioned shape:

```yaml
interface: cross-checkout-context/v1
execution_context:
  toolchain_source_root: absolute-path
  toolchain_commit: full-sha
  canonical_planning_repository_root: absolute-path
  canonical_planning_commit_before: full-sha
  implementation_target_root: absolute-path
  implementation_commit_before: full-sha
  codex_home: absolute-path
  generation_role: stable | candidate
  canonical_state_mutation_allowed: true | false
```

The implementation must reject missing, relative, overlapping, or
wrong-repository roots; mismatched full SHAs; unsupported generation roles;
planning writes outside the canonical planning root; and implementation writes
outside the declared implementation root before writes or delegation.

## Non-Goals

- Do not create the candidate clone, implementation branch, or candidate
  `CODEX_HOME`.
- Do not merge the accepted design history into a candidate branch.
- Do not launch candidate sessions or produce real cross-repository operation
  receipts.
- Do not rehearse pre-cutover rollback.
- Do not install, reload, or use changed stable control for real coordination
  in this batch.
- Do not redesign the architecture-program runner protocol.
- Do not change planning-state schemas, ledger storage, or planning formats.
- Do not implement command-owner ownership transfer or select CCFG-19.
- Do not change default `CODEX_HOME` or use installer force mode.
- Do not hard-code these codex-config project paths into reusable generic skill
  logic; project-specific values belong in this runway and its execution
  context.

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
Use the expanded convergence template for final batch reporting.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `skills/batch-runway/references/execute-slice-core-v1.md`
- `skills/batch-runway/references/execution-contract-v2.md`
- `skills/batch-runway/references/agent-result-contract-v2.md`
- `skills/batch-runway/references/reporting-contracts-v1.md`
- `skills/batch-runway/references/ledger-retention-v1.md`
- `skills/batch-runway/references/validation-profiles/project-harness-production.md`

Overrides:

- The controller remains the already-loaded stable generation at
  `c0615f63060e07e79101089b5599c8eff05f77f8` through same-batch closeout.
- Source tests may execute the new helper as code under test, but no agent,
  runner, installer, or real workflow may reload or consume changed stable
  control in this batch.
- Every commit in this batch is created in the stable checkout. Candidate paths
  must not be created or written.
- Final closeout marks CCFG-18 `Prepared`, preserves its deferred scope, clears
  this queue, and stops. It must not select successor work.
- The next session must be fresh, must verify all installed repo-owned links
  resolve to the new exact master commit, and must invoke a later explicit
  `plan-batch` for remaining CCFG-18 work.

## Validation Profile

Selected profile: `project-harness-production`

Profile reference:
`skills/batch-runway/references/validation-profiles/project-harness-production.md`

Focused validation commands:

- `python scripts/planning_state.py current --root docs/plans --format json`
  - Status class: `required-green`.
  - Baseline: passed with no blockers.
- `python scripts/planning_state.py validate --root docs/plans --format json`
  - Status class: `required-green`.
  - Baseline: passed with no blockers and two redirect-ledger warnings.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_cross_checkout_context.py`
  - Status class: `implementation-created`.
  - Slice 1 creates the test module before this becomes required-green.
- `python -m pytest tests/test_codex_owner.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_change_allowance.py -q`
  - Status class: `required-green`.
  - Baseline: passed with `22 passed`.
- `python -m pytest tests/test_custom_agent_contracts.py -q`
  - Status class: `required-green`.
  - Baseline: passed with `9 passed`.
- `python -m pytest tests/test_codex_features_manifest.py -q`
  - Status class: `known-red-baseline`.
  - Baseline: `3 failed, 37 passed` in unrelated existing command-owner
    wording expectations.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline pytest -q tests/test_codex_features_manifest.py -k cross_checkout`
  - Status class: `implementation-created`.
  - Slice 3 adds the focused manifest/installation assertion before this
    command becomes required-green.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline ruff check scripts tests`
  - Status class: `required-green`.
  - Baseline: passed.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline basedpyright scripts/cross_checkout_context.py scripts/architecture_program_runner_environment.py`
  - Status class: `implementation-created`.
  - Slice 1 creates the new module; the existing environment module currently
    passes with zero errors.
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uv run --offline basedpyright scripts`
  - Status class: `known-red-baseline`.
  - Baseline: `311 errors`; use diagnostically and do not hide or increase the
    baseline in touched files.
- `./install.sh --dry-run`
  - Status class: `required-green`.
  - Baseline: passed; execution must remain dry-run only.
- `python -m json.tool codex-features.json`
  - Status class: `required-green`.
  - Baseline: passed.
- `git diff --check`
  - Status class: `required-green`.

Per-slice workers must not run the full pytest suite, perform a real install,
create candidate paths, run package installation, or change planning state.
The coordinator owns planning-state diagnostics, final validation, ledger
updates, and commits.

## Active Ledger

No implementation slices remain. Final validation and same-batch closeout are
recorded in `closeout.md`.

| Slice | Status | Risk class | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|---|

## Orchestration Anomalies

```yaml
orchestration_anomalies: []
```

## Completed Slice Archive

Completed rows move to `completed-slices.md` after each focused commit.

## Slice 1: Context Contract And Root Validation

Risk class: `migration`

Scope:

- Create `scripts/cross_checkout_context.py` as the single temporary owner of
  `cross-checkout-context/v1` parsing and validation.
- Create `tests/test_cross_checkout_context.py`.
- Validate required fields, absolute paths, non-overlapping root roles,
  full-length Git revisions, generation role, repository identities, and
  canonical mutation permission.
- Fail closed before writes or delegation.
- Keep semantic workflow decisions outside the mechanism.

Allowed files or areas:

- `scripts/cross_checkout_context.py`
- `tests/test_cross_checkout_context.py`

Non-goals:

- Do not integrate the mechanism into skills, agents, runner control, or
  installation yet.
- Do not read or write real canonical planning state.
- Do not create either future candidate path.

Acceptance criteria:

- The exact `cross-checkout-context/v1` required context is represented and
  validated deterministically.
- Missing, relative, overlapping, wrong-repository, invalid-SHA, and invalid-role
  inputs fail closed with actionable errors.
- The mechanism has no API for selection, scope shaping, runway design,
  execution acceptance, closeout, or successor decisions.
- Focused tests and touched-file type/lint checks pass.

Validation:

- Promote the implementation-created context test command to required-green.
- Run touched-file ruff.
- Run touched-file basedpyright.
- Run `git diff --check`.

Commit message:

`Add cross-checkout context contract`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 1, do not spawn, delegate to, or wait on additional agents, and do
not touch planning state or candidate paths. Return the task-scoped diff and
focused validation evidence to the coordinator; do not commit.

Review subagent brief:

Review the exact task-scoped diff basis supplied by the coordinator. Confirm
fail-closed root/repository validation, exact interface fields, absence of
semantic workflow authority, no candidate writes, and focused green evidence.
Echo `diff_basis` in compact YAML.

Stop conditions:

- Stop if correct validation requires a planning-state or ledger-store change.
- Stop if the interface would infer roots only from current working directory.

## Slice 2: Write Scope, Generation, And Receipts

Risk class: `migration`

Scope:

- Extend the single owner in `scripts/cross_checkout_context.py` with explicit
  write-scope checks, generation identity capture, and the versioned
  cross-repository receipt shape.
- Extend `tests/test_cross_checkout_context.py` with positive and negative
  behavior for planning and implementation boundaries.
- Require receipts to distinguish toolchain, planning-before, and
  implementation-before revisions and to record caller, reason, allowed scope,
  generation role, and the CCFG-29 deletion condition.
- Block root/generation mismatch before writes or delegation.

Allowed files or areas:

- `scripts/cross_checkout_context.py`
- `tests/test_cross_checkout_context.py`

Non-goals:

- Do not perform writes, commits, installs, or delegation through this helper.
- Do not create a candidate repository or validate against real candidate state.
- Do not add workflow decision methods.

Acceptance criteria:

- Planning writes outside the canonical planning root are rejected.
- Implementation writes outside the declared implementation root are rejected.
- Stable and candidate generation identities are mechanically distinguishable.
- Receipt data cannot collapse planning and implementation revisions into one
  ambiguous value.
- Focused negative tests prove mismatches block before write/delegation hooks.

Validation:

- Run the context test module.
- Run touched-file ruff and basedpyright.
- Run `git diff --check`.

Commit message:

`Enforce cross-checkout generation boundaries`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 2, do not delegate, preserve the Slice 1 owner, and keep the helper
apply-free and decision-free. Return the task-scoped diff and validation; do not
commit.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm write-scope checks run before
write/delegation hooks, receipt revisions remain distinct, generation identity
is mechanical, and no semantic workflow decision enters the helper. Echo
`diff_basis` in compact YAML.

Stop conditions:

- Stop if the helper would need authority to accept execution or closeout.
- Stop if the receipt format omits exact repository or generation identity.

## Slice 3: Stable Consumer And Installation Wiring

Risk class: `migration`

Scope:

- Update stable command/runtime guidance only enough to require propagation and
  validation of `cross-checkout-context/v1` for an explicitly cross-checkout
  runway.
- Update registered worker and reviewer contracts so results report verified
  generation and repository identity without gaining lifecycle authority.
- Register the new helper through existing manifest-driven symlink installation
  rather than adding parallel installer mechanics.
- Add focused manifest and agent-contract tests.
- Update `CHANGELOG.md` and affected feature versions for the stable bootstrap.
- Run installation dry-run and final validation, reconcile this batch as
  CCFG-18 `Prepared`, then stop.

Allowed files or areas:

- `skills/plan-batch/`
- `skills/work-batch/`
- `skills/batch-runway/`
- `agents/runway_worker.toml`
- `agents/runway_reviewer.toml`
- `codex-features.json`
- `tests/test_codex_features_manifest.py`
- `tests/test_custom_agent_contracts.py`
- `CHANGELOG.md`
- This batch's `runway.md`, `completed-slices.md`, and `closeout.md`
- Program `CURRENT.md` and `LEDGER.md` during same-batch closeout only

Non-goals:

- Do not change `scripts/install_codex_config.py`; the existing manifest link
  mechanism is the installation owner.
- Do not redesign architecture-program runner protocol or successor logic.
- Do not add a new human-facing command or broad runtime owner.
- Do not perform a real install or mutate default `CODEX_HOME`.
- Do not mark CCFG-18 `Closed`.

Acceptance criteria:

- Cross-checkout consumers propagate explicit context and reject missing or
  mismatched validation before worker/reviewer delegation.
- Worker/reviewer outputs report repository and generation identity while
  lifecycle decisions remain coordinator-owned.
- Manifest-driven dry-run exposes the helper only from the stable checkout.
- No candidate path exists after final validation.
- Changelog states the problem, decision, and expected effect.
- Closeout preserves remaining CCFG-18 scope and selects no successor.

Validation:

- Run focused context, existing runner/control, custom-agent, and new
  manifest-selection tests.
- Run `ruff check scripts tests`.
- Run touched-file basedpyright; retain full-repo basedpyright as known-red
  diagnostic evidence only.
- Run `./install.sh --dry-run`; do not run a real install.
- Run `python -m json.tool codex-features.json`.
- Run planning-state `current` and `validate` before closeout.
- Run `git diff --check`.

Commit message:

`Bootstrap stable cross-checkout control`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent. Implement
only Slice 3, do not spawn or delegate, do not install changed control, do not
create candidate paths, and keep project-specific absolute paths in this runway
rather than reusable skills. Return the task-scoped diff and validation; do not
commit.

Review subagent brief:

Review the exact task-scoped diff basis. Confirm the bridge stays narrow and
temporary, consumers do not gain duplicate ownership, agent results expose
mechanical identity, manifest wiring uses the existing installer, no candidate
or default-home mutation occurred, and release metadata is accurate. Echo
`diff_basis` in compact YAML.

Stop conditions:

- Stop if installer changes beyond manifest registration are required.
- Stop if any consumer must load candidate source.
- Stop if changed stable control would be installed or used in this session.

## Final Validation

Required-green:

- Context tests created by Slice 1.
- Focused existing runner/control tests (`22 passed` baseline).
- Custom-agent contract tests (`9 passed` baseline).
- New focused manifest/installation test created by Slice 3.
- `ruff check scripts tests` through the offline repo toolchain.
- Touched-file basedpyright for the new helper and any previously green changed
  module.
- `./install.sh --dry-run`.
- `python -m json.tool codex-features.json`.
- Planning-state `current` and `validate`.
- `git diff --check`.

Known-red diagnostics that do not gate this batch:

- Full pytest: `16 failed, 398 passed, 484 subtests passed` baseline.
- Full `tests/test_codex_features_manifest.py`: `3 failed, 37 passed` baseline.
- Full `basedpyright scripts`: `311 errors` baseline.

Final closeout must record the controlling commit, all declared roots, changed
stable commit range, validation/review evidence, absence of candidate paths,
zero real candidate writes, and the fresh-session handoff. It must mark CCFG-18
`Prepared`, clear only this queued batch, and stop without selecting CCFG-19.

## Stop Conditions

- Stop if selected, queued, active, or resumable state changes unexpectedly.
- Stop if any installed repo-owned link resolves outside the stable master
  checkout.
- Stop if the bridge acquires semantic workflow authority.
- Stop if a stable helper resolves from candidate source.
- Stop if implementation requires creating or writing either future candidate
  path.
- Stop if work reaches CCFG-19 or later command-owner migration scope.
- Stop if changed stable control is installed, reloaded, or used for real
  coordination in this batch.
- Stop if default `CODEX_HOME` would be mutated or force-installed.
- Stop if archived planning evidence becomes executable authority.
- Stop if closeout would mark CCFG-18 `Closed`, select CCFG-19, or prepare a
  successor dispatch/runway.
