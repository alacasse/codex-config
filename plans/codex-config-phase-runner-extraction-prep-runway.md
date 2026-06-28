# Phase Runner Extraction Prep Runway

## Purpose

Prepare `codex-config` for a future standalone `phase-runner` extraction
decision without creating the new repository yet. This runway closes the
planning-root wait condition from issue #12, makes the generic workflow
interface explicit, and introduces a minimal internal worker adapter seam with
both `codex-exec` and `shell` workers.

## Baseline And Assumptions

- Current Program Ledger:
  `docs/plans/codex-config-architecture-program-runner-findings.md`
- Dispatch packet:
  `plans/dispatch/phase-runner-extraction-prep-dispatch.md`
- Issue #12 decision note:
  `docs/plans/phase-runner-repo-split-issue-12-plan.md`
- Active planning now lives under `docs/plans/`; the current executing runway
  spec and dispatch remain under `plans/` only to avoid mid-batch recovery
  ambiguity.
- The current **Runner Facade** is
  `scripts/architecture_program_runner.py`.
- Current concept owners include state, validation, command, artifacts, phase
  environment, phase contract, phase transition, change allowance, phase
  observation, and input inventory.
- The production phase execution path is still Codex-specific through
  `execute_codex_phase`; `phase_executor` is a test seam, not a production
  worker adapter seam.

## Non-Goals

- Do not create a new `phase-runner` repository.
- Do not package or publish a generic runner.
- Do not change the architecture-program CLI, default phase sequence, phase
  result schema, receipt equality rule, artifact layout, or final Run Summary.
- Do not make GitHub issue bodies, Graphify validation policy, Batch Runway
  execution rules, or personal plans part of the generic workflow core.
- Do not migrate runtime Codex state, cache files, logs, sessions, or ignored
  local artifacts.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding,
significant uncertainty exists, blockers are present, or final batch reporting
is being produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:

- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:

- This is a full-runway spec because later slices touch runner phase execution
  behavior.
- Documentation-only slices may use `docs-only` validation overrides.
- If the planning-root migration moves this active spec, the coordinator must
  preserve the active spec path in its own orchestration notes and update any
  runner state or ledger references before continuing. Prefer leaving this
  active spec in `plans/` until closeout if moving it would make recovery
  ambiguous.

## Validation Profile

Primary profile: `project-harness-production`.

Profile reference:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/project-harness-production.md`

Repo-specific validation ladder:

- Focused pytest for touched runner seams, typically:
  `python -m pytest tests/test_architecture_program_runner*.py -q`
- Dry-run smoke after planning-root migration:
  `python scripts/architecture_program_runner.py --project . --program-ledger docs/plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- Ruff on touched Python surfaces:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
- `git diff --check`

For docs-only slices, use `git diff --check` plus targeted readback and path
reference audit instead of running Python tests.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1 | completed | this commit | `git diff --check`; targeted path audit/readback | clean | Generic workflow contract maps current runner accurately | Active Program Ledger moved to `docs/plans/`; active spec/dispatch intentionally remain in `plans/` until closeout |
| 2 | pending | | | | Generic workflow contract maps current runner accurately | Docs-only override allowed |
| 3 | pending | | | | Codex execution routes through adapter with unchanged facade behavior | Production refactor |
| 4 | pending | | | | Shell worker uses same state/receipt/transition rules | Production behavior shield |
| 5 | pending | | | | Issue #12 and Program Ledger show the next decision clearly | Docs plus final validation |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1 | this commit | Planning Root ADR created; active Program Ledger moved to `docs/plans/`; completed/superseded plans archived under `docs/plans/archive/`; current executing spec/dispatch kept under `plans/` as a temporary compatibility exception. | `docs/adr/0001-planning-root-and-plan-archive.md`; `docs/plans/README.md`; `docs/plans/codex-config-architecture-program-runner-findings.md`; review: clean |

## Slice 1 - Planning Root ADR And Archive Migration

Scope:

- Create the project documentation root needed for planning:
  `docs/plans/` and `docs/plans/archive/`.
- Create an ADR for the planning-root decision. If there is no existing ADR
  convention, use `docs/adr/0001-planning-root-and-plan-archive.md`.
- Move or copy active planning coordination to `docs/plans/` so future runner
  invocations can use that path.
- Classify completed or superseded planning files under `docs/plans/archive/`
  without rewriting their historical content beyond necessary path/readability
  updates.
- Update `CONTEXT.md`, the active Program Ledger, and issue #12 plan references
  that point at the active planning root.

Allowed files or areas:

- `docs/`
- `plans/`
- `CONTEXT.md`
- `README.md` only if it already names the old planning root
- `CHANGELOG.md` only if the migration changes workflow behavior

Non-goals:

- Do not migrate runtime runner artifacts under `architecture-program-runs/`.
- Do not edit GitHub issues.
- Do not create the generic worker seam in this slice.

Acceptance criteria:

- ADR names `docs/plans/` as **Planning Root** and
  `docs/plans/archive/` as **Plan Archive**.
- Active Program Ledger has a discoverable path under `docs/plans/`.
- Completed/superseded plans are either archived or explicitly left in place
  with a short rationale.
- Path references that future agents will follow no longer point to stale
  active planning locations.
- The old `plans/` location is not treated as the future active planning root.

Validation:

- `git diff --check`
- Read back the ADR, active Program Ledger, and issue #12 plan.
- Run a targeted path audit such as:
  `rg -n "plans/|docs/plans|Plan Archive|Planning Root" CONTEXT.md docs plans README.md`
  and classify any remaining `plans/` references as historical, current active
  spec/dispatch, or intentional compatibility.

Commit message:

`Document planning root migration`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only the planning-root ADR/archive migration. Do not spawn,
delegate to, or wait on additional subagents. Keep historical files readable
and avoid runtime state. Leave a compact note for the next slice identifying
the final active Program Ledger path.

Review subagent brief:

Review the migration for path consistency, archival clarity, and accidental
runtime-state movement. Confirm that future agents can find the active ledger
without reading stale historical plans.

Stop conditions:

- Stop if the migration would require moving ignored runtime state, cache,
  sessions, logs, or generated validation output.
- Stop if the active spec path becomes ambiguous for the coordinator.

## Slice 2 - Generic Workflow Contract

Scope:

- Add a generic workflow contract document under the active planning root,
  expected as `docs/plans/generic-phase-runner-workflow-contract.md` after
  Slice 1.
- Map current runner concepts to generic names:
  **Workflow**, **Phase**, **Worker**, **Receipt**, **State**, and
  **Artifact**.
- Name what remains `codex-config`-specific: architecture-program phases,
  Codex prompts, Batch Runway skill language, local personal plans, and
  repo-owned Codex configuration.
- Update `docs/plans/generic-phase-runner-product-idea.md` or its migrated
  equivalent only enough to point to the contract and avoid divergent language.

Allowed files or areas:

- `docs/plans/`
- `docs/plans/generic-phase-runner-product-idea.md`
- `CONTEXT.md` only for glossary cross-reference
- Active Program Ledger

Non-goals:

- Do not implement the worker adapter seam.
- Do not define a public package API.
- Do not create YAML workflow loading.

Acceptance criteria:

- Contract states the generic boundary and the `codex-config` integration
  boundary separately.
- Contract explicitly says a worker adapter executes one phase and returns a
  validated phase result or runner error.
- Contract states that receipts remain compact durable evidence, not
  transcripts.
- Contract preserves the current architecture-program sequence as one
  `codex-config` workflow, not the only possible workflow.

Validation:

- `git diff --check`
- Read back the contract and issue #12 plan.
- Targeted audit for divergent terminology:
  `rg -n "generic|Workflow|Worker|Adapter|phase-runner|Batch Runway|Codex" docs plans CONTEXT.md`

Commit message:

`Document generic phase runner contract`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement the contract documentation only. Do not spawn, delegate to, or
wait on additional subagents. Keep it compact enough that future code slices
can treat it as an interface reference.

Review subagent brief:

Review for boundary clarity: generic runner concepts must not absorb
`codex-config`-specific skills or personal workflow policy.

Stop conditions:

- Stop if the contract cannot clearly distinguish generic worker behavior from
  architecture-program prompt semantics.

## Slice 3 - Codex Worker Adapter Seam

Scope:

- Introduce a minimal internal worker adapter seam for phase execution.
- Route current Codex phase execution through a `codex-exec` adapter while
  preserving `execute_codex_phase` compatibility and existing tests.
- Keep command construction, prompt construction, phase environment, execution
  observation, env override handling, and output-last-message behavior
  unchanged unless the adapter boundary requires a narrow relocation.

Allowed files or areas:

- `scripts/architecture_program_runner.py`
- New or existing runner worker owner file, expected:
  `scripts/architecture_program_runner_workers.py`
- `scripts/architecture_program_runner_command.py` only for adapter consumption
  of existing command helpers
- `tests/test_architecture_program_runner.py`
- New focused worker tests if useful
- `CHANGELOG.md`

Non-goals:

- Do not add shell execution yet except for test fakes needed to define the
  seam.
- Do not change CLI arguments.
- Do not change result schema or receipt validation.
- Do not add generic workflow YAML loading.

Acceptance criteria:

- There is one explicit internal worker adapter API for running a phase and
  returning a phase result dictionary.
- The current Codex behavior is implemented by a Codex adapter that reuses the
  existing prompt, command, env, and observation helpers.
- Existing public helper reexports remain compatible or are deliberately
  reexported from the new owner.
- Existing runner integration tests continue to pass.
- `CHANGELOG.md` notes the worker seam and expected behavior preservation.

Validation:

- `python -m pytest tests/test_architecture_program_runner.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_phase_observation.py -q`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
- `git diff --check`

Commit message:

`Introduce architecture runner worker seam`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement the smallest Codex worker adapter seam and route the existing
Codex execution through it. Do not spawn, delegate to, or wait on additional
subagents. Preserve the existing facade and tests.

Review subagent brief:

Review for accidental behavior changes in command construction, subprocess
environment, output-last-message parsing, and phase execution observation.

Stop conditions:

- Stop if the seam requires changing CLI flags, phase-result fields, receipt
  validation, or artifact layout.

## Slice 4 - Shell Worker Adapter And Generic Workflow Shield

Scope:

- Add a shell worker adapter that can run a configured shell command for a phase
  and return a phase result from a compact JSON output file.
- Add tests proving a shell-only phase can use the same state, phase-result
  validation, receipt equality, and transition rules without Codex, Batch
  Runway, or architecture-program prompt language.
- Keep shell adapter behavior internal and minimal; it exists to prove the
  worker seam, not to expose a public generic CLI.

Allowed files or areas:

- `scripts/architecture_program_runner_workers.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner*.py`
- `tests/architecture_program_runner_test_support.py`
- `CHANGELOG.md`

Non-goals:

- Do not expose a user-facing shell workflow CLI.
- Do not add YAML workflow parsing.
- Do not use network, GitHub, or live Codex for shell worker tests.

Acceptance criteria:

- Shell adapter tests execute a local command/script fixture and load a phase
  result JSON object.
- The returned shell result is validated by existing phase-result and receipt
  validation code.
- A shell-only test advances state through existing transition logic.
- Tests prove no Batch Runway skill prompt or Codex command is required for the
  shell worker path.
- Codex adapter behavior remains covered.

Validation:

- `python -m pytest tests/test_architecture_program_runner*.py -q`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
- `git diff --check`

Commit message:

`Add shell phase worker coverage`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Implement only the internal shell adapter proof and focused tests. Do
not spawn, delegate to, or wait on additional subagents. Keep public runner
behavior unchanged.

Review subagent brief:

Review for over-generalization, accidental public API expansion, shell quoting
risks, and tests that bypass the real validation/transition path.

Stop conditions:

- Stop if shell execution needs a public workflow definition or a phase-result
  schema change.
- Stop if tests become dependent on live Codex, network, or external services.

## Slice 5 - Reassessment And Final Ledger Closeout

Scope:

- Update issue #12 planning docs with the post-prep decision evidence.
- Update the Program Ledger with compact closeout evidence for APR-22 through
  APR-25.
- Keep APR-26 deferred or promote it to the next candidate based on the actual
  evidence from the worker seam and shell adapter tests.
- Update `CHANGELOG.md` if not already updated for workflow behavior changes.
- Run final validation.

Allowed files or areas:

- Active Program Ledger under `docs/plans/`
- Issue #12 plan, migrated or archived equivalent
- Generic workflow contract
- `CHANGELOG.md`
- Current runway spec ledger/archive rows

Non-goals:

- Do not create the separate repo.
- Do not open or update GitHub issue #12 unless explicitly asked after this
  batch.

Acceptance criteria:

- Ledger records compact evidence for planning-root migration, generic
  contract, Codex adapter seam, shell adapter test, and final validation.
- Issue #12 plan says whether the next action is repo skeleton creation,
  another internal prep batch, or deferral.
- Remaining deferred work is visible without requiring future agents to
  reconstruct it from transcripts.

Final validation:

- `python -m pytest tests/test_architecture_program_runner*.py tests/test_codex_owner.py -q`
- `python scripts/architecture_program_runner.py --project . --program-ledger docs/plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check scripts tests`
- `git diff --check`

Commit message:

`Close phase runner extraction prep`

Coding subagent brief:

The spawned `runway_worker` is already the required coding subagent for this
slice. Update planning and ledger evidence only, then run final validation. Do
not spawn, delegate to, or wait on additional subagents. Do not create the new
repo.

Review subagent brief:

Review final evidence for truthfulness, compactness, path consistency, and
whether the repo-split decision is actually supported by the completed work.

Stop conditions:

- Stop if final validation fails.
- Stop if the evidence does not support a clear next repo-split decision.
- Stop if the Program Ledger path is ambiguous after migration.
