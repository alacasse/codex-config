# Architecture Program Runner Phase Contract Catalog Runway

## Purpose

Give **Phase Contract** a clear concept owner so runner-launched phase
obligations are testable independently of prompt layout while preserving the
public **Runner Facade** behavior.

This spec executes the `phase-contract-catalog` batch selected by
`plans/dispatch/phase-contract-catalog-dispatch.md`.

## Current Baseline

- Baseline commit: `510f407 Close architecture runner transition allowance batch`.
- Source program ledger:
  `plans/codex-config-architecture-program-runner-findings.md`.
- Dispatch packet:
  `plans/dispatch/phase-contract-catalog-dispatch.md`.
- Included finding: APR-19.
- Primary concept language: `CONTEXT.md`.
- Runner Facade: `scripts/architecture_program_runner.py`.
- Current prompt/command owner:
  `scripts/architecture_program_runner_command.py`.
- Existing concept owners:
  - `scripts/architecture_program_runner_state.py`
  - `scripts/architecture_program_runner_validation.py`
  - `scripts/architecture_program_runner_command.py`
  - `scripts/architecture_program_runner_artifacts.py`
  - `scripts/architecture_program_runner_environment.py`
  - `scripts/architecture_program_runner_transition.py`
  - `scripts/architecture_program_runner_change_allowance.py`
- Current focused tests:
  - `tests/test_architecture_program_runner_command.py`
  - `tests/test_architecture_program_runner_environment.py`
  - `tests/test_architecture_program_runner_transition.py`
  - `tests/test_architecture_program_runner_change_allowance.py`
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_protocol.py`
  - `tests/test_architecture_program_runner.py`
  - `tests/test_codex_owner.py`

## Assumptions

- `plans/` is the current planning location until APR-22 migrates the
  **Planning Root**.
- **Phase Contract** means normative obligations and allowed outputs for one
  runner-launched phase. It is rendered into prompt text, but it is not the
  prompt text itself.
- **Phase Environment** remains the source of supplied facts and settings:
  paths, artifact facts, batch-limit labels, sandbox/model choices, env
  override key labels, and expected receipt/input-inventory paths.
- The expected concept-owner home is
  `scripts/architecture_program_runner_phase_contract.py`. Workers may choose a
  clearer local name only if the concept language remains explicit and
  compatibility exports are preserved.
- No live nested Codex run is required for this batch.
- The integration harness is the dry-run runner smoke that exercises CLI
  parsing, prompt construction, command display, direct script execution, and
  imports without launching nested Codex.

## Non-Goals

- Do not change CLI arguments, defaults, phase sequence, model handling,
  sandbox behavior, env override handling, command flags, or dry-run semantics.
- Do not change phase-result schema, required receipt fields, receipt equality,
  expected receipt paths, expected input inventory paths, artifact layout, or
  final **Run Summary** shape.
- Do not move **Phase Environment** facts into the contract owner.
- Do not move schema validation, expected next-phase validation, or receipt
  equality out of `scripts/architecture_program_runner_validation.py`.
- Do not implement exact Codex session JSONL discovery for APR-20.
- Do not implement **Input Inventory** schema validation for APR-21.
- Do not migrate the **Planning Root** or **Plan Archive** for APR-22.
- Do not add Graphify-specific validation, cache, package-manager, network, or
  ledger-parsing logic.

## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports,
slice summaries, commit receipts, and ledger notes.
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about
suspicious coordinator or subagent-lifecycle behavior.
Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is produced.
Use Batch Runway Standard Ledger Retention v1.
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execute-slice-core-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/execution-contract-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/reporting-contracts-v1.md`
- `/home/alacasse/projects/codex-config/skills/batch-runway/references/ledger-retention-v1.md`

Overrides:
- Treat this file creation session as `create-spec`; implementation starts in a
  later `execute-spec` session from the first pending active-ledger row.
- Use lean-runway density with explicit prompt, contract/environment, and
  validation-owner guardrails because the intended change is behavior-preserving
  concept ownership, not public behavior redesign.

## Validation Profile

Selected profile:
`/home/alacasse/projects/codex-config/skills/batch-runway/references/validation-profiles/mechanical-production-refactor.md`

Focused validation commands:
- For each slice, run the new or touched focused test modules plus the runner
  integration tests that cover the moved behavior.
- Expected focused runner subset as the batch grows:
  `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- For slices before `tests/test_architecture_program_runner_phase_contract.py`
  exists, omit that path and run touched tests plus the remaining focused runner
  subset.
- Use the repo-proven lint path:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check <touched production/test files>`
- `git diff --check`

Integration harness:
- Dry-run smoke, no nested Codex:
  `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`

Harness output:
- The dry-run smoke writes no expected project artifact. If tests introduce
  temporary state or artifact paths, keep them inside test temp directories or
  ignored generated paths.

Summary artifact:
- No generated summary artifact is required for the dry-run smoke. Report the
  command status and concise stdout/stderr signal needed to prove the smoke.

Index refresh:
- None required for this repo after these Python/test edits.

Commit requirements:
- Commit after each clean, focused slice.
- Use a concise imperative subject. No special trailers are required.
- Commit only files in the slice scope and the spec ledger/archive update for
  that slice.

Dirty-file constraints:
- Preserve unrelated dirty files.
- Planning files under `plans/` may be local planning artifacts.
- Do not revert or commit unrelated user changes outside the active slice.

## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1. Characterize Phase Contract obligations | completed | slice commit | `pytest` 39 passed; `uvx ruff` passed; `git diff --check` passed | clean | Introduce contract owner from characterized obligations | Characterization coverage added without production behavior changes. |
| 2. Introduce Phase Contract owner | completed | slice commit | `pytest` 35 passed; dry-run smoke passed; `uvx ruff` passed; `git diff --check` passed | clean | Route prompt rendering through contract owner | Added structured `PhaseContract` owner and compatibility exports without behavior changes. |
| 3. Route prompt rendering through contract owner | pending | | | | Tighten tests and facade compatibility | |
| 4. Tighten contract tests and compatibility | pending | | | | Final validation and closeout | |

## Orchestration Anomalies

orchestration_anomalies: []

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1. Characterize Phase Contract obligations | slice commit | Added focused characterization tests for shared single-level, result, env-override, and per-phase obligations; no production behavior changed. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check tests/test_architecture_program_runner_phase_contract.py`, `git diff --check` |
| 2. Introduce Phase Contract owner | slice commit | Added `scripts/architecture_program_runner_phase_contract.py`; command prompt helpers consume owner-produced obligations while environment and validation ownership remain separate. | Worker: success; reviewer: clean; validation: `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`, dry-run smoke, `UV_CACHE_DIR=/tmp/codex-config-uv-cache UV_TOOL_DIR=/tmp/codex-config-uv-tools uvx ruff check scripts/architecture_program_runner_phase_contract.py scripts/architecture_program_runner_command.py scripts/architecture_program_runner.py tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner.py`, `git diff --check` |

## Slice 1. Characterize Phase Contract Obligations

Scope:
- Add focused characterization coverage for current **Phase Contract**
  obligations before moving production ownership.
- Prefer `tests/test_architecture_program_runner_phase_contract.py` for
  obligation catalog tests, while leaving rendered prompt assertions in
  `tests/test_architecture_program_runner_command.py` until later slices.
- Name the boundary between contract obligations and **Phase Environment** facts
  in test names and fixtures.

Allowed files/areas:
- `tests/test_architecture_program_runner_phase_contract.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/architecture_program_runner_test_support.py`
- This spec ledger/archive rows

Non-goals:
- Do not change production code in this slice unless a tiny test-support import
  compatibility fix is required.
- Do not change prompt wording, command construction, receipt paths, dry-run
  output, or phase-result validation behavior.
- Do not introduce the new owner API yet unless characterization tests cannot
  be written without a named test helper.

Acceptance criteria:
- Tests characterize shared single-level phase obligations:
  - do not run nested `codex exec`
  - do not launch the local runner recursively
  - do not probe nested Codex availability or create temporary `CODEX_HOME`
    workarounds
- Tests characterize shared result obligations:
  - return schema-valid JSON as the final response
  - write the same JSON object to a compact phase receipt
  - return the receipt path in `receipt_path`
  - use compact string or null validation/review summaries
  - do not parse or edit runner state directly
- Tests characterize phase-specific obligations and allowed next phases for
  `select-dispatch`, `create-spec`, `execute`, and `closeout`.
- Tests characterize env-override validation obligations as contract text while
  proving env override keys and values remain **Phase Environment** inputs.
- Tests do not duplicate path, sandbox, model, artifact, batch-limit, or schema
  path derivation assertions from environment-owner tests.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include touched tests and:
  `python -m pytest tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run ruff through `uvx` on touched tests.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Characterize architecture runner phase contracts`

Coding subagent brief:
- Implement only Slice 1 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 1 scope, characterization coverage, contract/environment
  separation, validation-owner boundaries, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if current behavior cannot be characterized without changing production
  behavior.
- Stop if tests make **Phase Environment** facts part of the **Phase Contract**
  catalog.

## Slice 2. Introduce Phase Contract Owner

Scope:
- Introduce a **Phase Contract** concept owner, expected at
  `scripts/architecture_program_runner_phase_contract.py`.
- Define a small structured API for deriving contract obligations from a
  **Phase**. Suggested names are `PhaseContract` and
  `build_phase_contract`, but the worker may choose clearer names if the
  concept remains explicit.
- Move pure contract knowledge behind this owner: phase skill routing,
  single-level phase boundary obligations, shared result obligations,
  env-override validation obligations, and phase-specific requirements.
- Keep compatibility wrappers in existing modules when needed for current tests
  and users.

Allowed files/areas:
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner_phase_contract.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner.py`
- This spec ledger/archive rows

Non-goals:
- Do not move **Phase Environment** facts or formatting into the contract owner.
- Do not change prompt wording or phase-specific requirements.
- Do not change `RunnerConfig`, state JSON shape, validation schema, receipt
  checks, artifact paths, or command construction.
- Do not remove compatibility exports from the Runner Facade.

Acceptance criteria:
- A single contract-owner API can produce shared obligations and phase-specific
  obligations for all four fixed phases.
- `phase_skill_instruction` delegates to the contract owner or remains a thin
  compatibility wrapper over it.
- Existing prompt construction can consume the contract owner without changing
  rendered text.
- Tests prove unknown phases still fail with `RunnerError`.
- The contract owner has no dependency on supplied **Phase Environment** facts
  such as paths, sandbox values, batch-limit labels, or env override values.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke because runner entrypoint imports and prompt rendering
  may be touched.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Add architecture runner phase contract owner`

Coding subagent brief:
- Implement only Slice 2 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 2 scope, owner/API clarity, behavior preservation,
  import-mode compatibility, contract/environment separation, validation-owner
  boundaries, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if the owner would need to derive **Phase Environment** facts to satisfy
  tests.
- Stop if compatibility wrappers obscure which API owns **Phase Contract**
  obligations.
- Stop if direct script execution and importlib-based tests cannot both be
  preserved.

## Slice 3. Route Prompt Rendering Through Contract Owner

Scope:
- Update `build_prompt` to consume the **Phase Contract** owner for shared
  obligations and per-phase requirements.
- Keep **Phase Environment** as the source for supplied facts, expected paths,
  artifact facts, sandbox/model choices, batch-limit label, and env override key
  labels.
- Preserve prompt wording and ordering unless a tiny rendering adjustment is
  required by the new structured owner and current tests are updated to prove no
  behavior-significant change.

Allowed files/areas:
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner_phase_contract.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner_environment.py`
- `tests/test_architecture_program_runner_protocol.py`
- `tests/test_architecture_program_runner.py`
- `CHANGELOG.md`
- This spec ledger/archive rows

Non-goals:
- Do not change command construction, dry-run command display, CLI parsing, or
  subprocess env handling except for imports needed by prompt rendering.
- Do not move phase-result schema validation, expected next-phase validation, or
  receipt equality into the contract owner.
- Do not implement APR-20, APR-21, or APR-22.

Acceptance criteria:
- `build_prompt` uses the contract owner for:
  - skill instruction
  - single-level phase boundary rules
  - shared result/receipt obligations
  - conditional env-override validation obligations
  - phase-specific requirements and allowed `next_phase` guidance
- Prompt tests still prove the expected contract text is rendered for all four
  phases.
- Environment tests remain the authority for path, artifact, sandbox, env-key,
  and batch-limit facts.
- Dry-run output remains behavior-preserving and still hides env override
  values.
- `CHANGELOG.md` is updated if this slice introduces the production concept
  owner used by prompt rendering and the earlier slice did not already do so.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Route architecture runner prompts through phase contracts`

Coding subagent brief:
- Implement only Slice 3 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 3 scope, prompt behavior preservation, contract/environment
  separation, validation-owner boundaries, changelog need, and dirty-file
  leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if prompt rendering changes phase obligations, allowed next-phase text,
  receipt path instructions, env override secrecy, or dry-run semantics.
- Stop if the contract owner starts consuming state or config facts that belong
  to **Phase Environment**.

## Slice 4. Tighten Contract Tests And Compatibility

Scope:
- Move remaining obligation assertions out of broad command/facade tests into
  contract-owner tests where practical.
- Keep command tests focused on rendering integration between **Phase Contract**
  and **Phase Environment**.
- Keep Runner Facade tests focused on compatibility exports and thin integration
  behavior.
- Remove temporary duplication introduced during the earlier slices.

Allowed files/areas:
- `scripts/architecture_program_runner_phase_contract.py`
- `scripts/architecture_program_runner_command.py`
- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner_phase_contract.py`
- `tests/test_architecture_program_runner_command.py`
- `tests/test_architecture_program_runner_environment.py`
- `tests/test_architecture_program_runner_run_loop.py`
- `tests/test_architecture_program_runner_protocol.py`
- `tests/test_architecture_program_runner.py`
- `tests/architecture_program_runner_test_support.py`
- `CHANGELOG.md`
- This spec ledger/archive rows

Non-goals:
- Do not weaken existing integration coverage for direct script execution,
  importlib-based tests, CLI defaults, dry-run output, or env override secrecy.
- Do not remove compatibility exports unless a previous slice deliberately
  introduced replacement compatibility and tests prove existing callers still
  work.
- Do not implement APR-20, APR-21, or APR-22.

Acceptance criteria:
- Contract-owner tests are the primary home for shared and per-phase
  obligations.
- Command tests assert that prompts render contract obligations together with
  environment facts without duplicating the full catalog.
- Runner Facade compatibility tests include any new public helper exports added
  for the contract owner.
- Direct script execution and importlib-based tests both still work.
- No temporary compatibility path or duplicate contract list remains unless it
  is intentionally named and covered.

Validation:
- Use the selected mechanical-production-refactor profile.
- Focused commands must include:
  `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Run the dry-run smoke.
- Run ruff through `uvx` on touched production and test files.
- Run `git diff --check`.

Test quality review:
- None.

Commit message:
- `Tighten architecture runner contract tests`

Coding subagent brief:
- Implement only Slice 4 from this spec.
- You are already the required coding subagent for this slice. Do not spawn,
  delegate to, or wait on additional subagents.
- The coordinator handles validation, review delegation, ledger updates, and
  commits.
- Return compact YAML only.

Review subagent brief:
- Review only Slice 4 scope, test ownership, compatibility coverage,
  prompt/contract behavior preservation, changelog need, and dirty-file leakage.
- Return compact YAML only. Do not modify files.

Stop conditions:
- Stop if test cleanup weakens coverage for any phase-specific obligation.
- Stop if broad command or facade tests still carry the contract catalog because
  the contract owner is not yet authoritative.

## Final Validation

Run after Slice 4 and before final closeout:

- Full focused runner subset:
  `python -m pytest tests/test_architecture_program_runner_phase_contract.py tests/test_architecture_program_runner_command.py tests/test_architecture_program_runner_environment.py tests/test_architecture_program_runner_transition.py tests/test_architecture_program_runner_change_allowance.py tests/test_architecture_program_runner_state.py tests/test_architecture_program_runner_validation.py tests/test_architecture_program_runner_artifacts.py tests/test_architecture_program_runner_run_loop.py tests/test_architecture_program_runner_worktree.py tests/test_architecture_program_runner_protocol.py tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`
- Dry-run smoke:
  `python scripts/architecture_program_runner.py --project . --program-ledger plans/codex-config-architecture-program-runner-findings.md --dry-run --stop-after-phase select-dispatch`
- Lint touched production and test files:
  `UV_CACHE_DIR=/tmp/codex-config-uv-cache uvx ruff check <touched production/test files>`
- `git diff --check`

After successful final validation, update
`plans/codex-config-architecture-program-runner-findings.md`:

- Mark APR-19 `Closed` with commit evidence and focused validation.
- Mark `phase-contract-catalog` `Closed`.
- Refresh **Selected Batch Brief** to the next recommended batch only if a safe
  next batch is ready; otherwise state that no selected batch is active.
- Keep APR-20, APR-21, and APR-22 visible with their deferred rationale.

## Batch Stop Conditions

- Stop on any behavior change to CLI arguments, command flags, prompt
  obligations, phase-specific next-phase requirements, dry-run output, receipt
  path handling, phase-result schema behavior, or final **Run Summary** shape.
- Stop if **Phase Contract** starts owning **Phase Environment** facts.
- Stop if validation-owner behavior moves into the contract owner.
- Stop if implementation drifts into **Phase Observation** attribution,
  **Input Inventory** validation, or **Planning Root** migration.
- Stop if direct script execution cannot be preserved.
- Stop if subagent support is unavailable during execution; do not fall back to
  main-agent implementation.
