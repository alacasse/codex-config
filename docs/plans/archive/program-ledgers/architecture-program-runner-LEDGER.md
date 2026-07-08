# Codex Config Architecture Program Runner Program Ledger

## Purpose

Keep architecture-program runner findings visible across batches without
requiring future agents to replay stale runway specs or block reports. This is
the active **Program Ledger** under the **Planning Root** at `docs/plans/`.

## Glossary Anchor

Use `CONTEXT.md` as the terminology source for this ledger. In particular:

- Start new runner redesign work with **Phase Environment**.
- Treat `scripts/architecture_program_runner.py` as the **Runner Facade**:
  externally visible behavior must keep working, but internal code shape is
  open to redesign.
- Use **Concept Owner**, not "owner module", when describing the responsible
  home for a runner concept.
- Use **Phase Observation**, not telemetry, for runner-recorded phase facts.
- Use **Change Allowance**, not dirty-worktree policy, for allowed changed
  paths at a phase.
- Treat stale completed plans and reports as **Plan Archive** material,
  not active coordination.

## Current Direction

- Keep `architecture-program-runway` responsible for program selection,
  dispatch, and closeout; keep `batch-runway` responsible for concrete
  implementation slices.
- Keep the runner project-neutral. Do not add Graphify-specific validation,
  cache, package-manager, network, or ledger-parsing logic.
- Preserve the fixed **Phase** sequence:
  `select-dispatch -> create-spec -> execute -> closeout`.
- Preserve the **Runner Facade** behavior: CLI arguments, phase-result schema,
  receipt-path checks, direct script execution, dry-run smoke behavior, final
  **Run Summary**, and structured artifact layout.
- Make concept ownership deeper before adding new features. The next
  production refactor should start with **Phase Environment** because launch
  context and prompt context are currently spread across CLI config, command
  construction, env override handling, sandbox selection, and prompt assembly.
- Use `docs/plans/` as the active **Planning Root**, with **Plan Archive** at
  `docs/plans/archive/`; see ADR 0001.
- Treat the long-term split target as an external OSS Go runner, but do not
  move code by translating the Python file split. Extract versioned workflow,
  state, result, receipt, artifact, telemetry, input-inventory, and
  planning-state interop contracts first.
- Keep `scripts/planning_state.py` as a separate diagnostic/protocol surface.
  The runner may consume explicit planning-state facts later, but the generic
  core must not depend on `codex-config` Markdown heuristics or Python imports.

## Current Active Surfaces

- Glossary: `CONTEXT.md`
- Current Program Ledger:
  `docs/plans/programs/architecture-program-runner/LEDGER.md`
- Runner Facade: `scripts/architecture_program_runner.py`
- Current concept-owner files:
  - `scripts/architecture_program_runner_state.py`
  - `scripts/architecture_program_runner_validation.py`
  - `scripts/architecture_program_runner_command.py`
  - `scripts/architecture_program_runner_artifacts.py`
  - `scripts/architecture_program_runner_phase_observation.py`
- Current focused tests:
  - `tests/test_architecture_program_runner_state.py`
  - `tests/test_architecture_program_runner_validation.py`
  - `tests/test_architecture_program_runner_command.py`
  - `tests/test_architecture_program_runner_artifacts.py`
  - `tests/test_architecture_program_runner_phase_observation.py`
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_worktree.py`
  - `tests/test_architecture_program_runner_protocol.py`
  - `tests/test_architecture_program_runner.py`
- Behavioral runner reference:
  `skills/architecture-program-runway/references/local-runner-v1.md`
- Repo-split decision note:
  `docs/plans/phase-runner-repo-split-issue-12-plan.md`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| APR-1. Unsupported Codex output schema composition | Closed | `6a00343`, `0cfeeda`; schema subset tests | None | Historical schema blocker; keep as evidence only. |
| APR-2. Phase summaries needed compact string/null shape | Closed | `0cfeeda`; validation and schema tests | None | Historical schema-shape blocker; keep as evidence only. |
| APR-3. All-batches and direct CLI batch bounds needed stable semantics | Closed | `f657019`; unbounded-mode tests | None | Batch-bound behavior is now part of **Runner Invocation**. |
| APR-4. Environment/cache pass-through was unclear for nested validation | Closed | `f5b284c`, `8755f86`, `d1ae6ef`; env override prompt/subprocess tests | Use APR-16 for concept ownership | Behavior exists; concept ownership is still shallow under **Phase Environment**. |
| APR-5. Stopped execute runs could not resume with their own evidence paths | Closed | `8755f86`; changed-path tests for stopped receipt evidence | Use APR-18 for concept ownership | Behavior exists; future work should express it through **Change Allowance**. |
| APR-6. Execute phases that must commit need a separate sandbox control | Closed | `58ebd36`; execute-sandbox tests and docs | Use APR-16 for concept ownership | Execute-only sandbox is a **Phase Environment** fact. |
| APR-7. Closeout phase could launch nested Codex and fail in managed sandboxes | Closed | `196c359`; prompt/reference tests | Use APR-19 for concept ownership | Behavior exists; future work should express it as **Phase Contract**. |
| APR-8. Flat runner artifacts hid run and batch boundaries | Closed | `01111f5`, `b3aaeca`; structured artifact tests | None | **Run Artifact** and **Batch Artifact** layout exists. |
| APR-9. Runner telemetry needed direct resource measurements | Superseded | `bad11cf`; telemetry tests and recommendations doc | Use APR-20 | Reframed as **Phase Observation** attribution. |
| APR-10. Input inventory is prompt guidance only | Superseded | Prompt text in command concept owner | Use APR-21 | Reframed as **Input Inventory** contract work. |
| APR-11. `architecture_program_runner.py` concentrates too many responsibilities | Closed | Runner boundary split slices 1-4 | None | Historical driver for the first split; do not reopen as a generic "large file" concern. |
| APR-12. Tests mirror the large runner file as one broad suite | Closed | Runner boundary split Slice 5 | None | Focused test topology exists; future tests should follow **Concept Owner** language. |
| APR-13. Structured failure paths do not refresh manifests consistently | Closed | Runner boundary split Slice 4; malformed-result regression | None | Failure-path manifest refresh behavior exists. |
| APR-14. Prior planning docs are useful but stale as coordination state | Superseded | This refreshed ledger and `CONTEXT.md` | Use APR-22 | Reframed as **Planning Root** and **Plan Archive** migration. |
| APR-15. `codex_owner.py` is small and not the architecture hotspot | Deferred | `tests/test_codex_owner.py` | Revisit only when ownership behavior changes | Still outside the runner concept-ownership program. |
| APR-16. **Phase Environment** lacks a concept owner | Closed | `950ddf9`, `82e8c8e`, `556b6bd`, `e00f667`; `scripts/architecture_program_runner_environment.py`; focused tests and dry-run smoke | None | **Phase Environment** now owns runner-supplied launch and prompt context while **Phase Contract** rendering remains in command tests. |
| APR-17. **Phase Transition** is expressed as run-loop state-key mutation | Closed | `c6d7705`, `19d6b8a`, `6cb9e20`; `scripts/architecture_program_runner_transition.py`; focused tests and dry-run smoke | None | **Phase Transition** now consumes a valid **Phase Result** and updates **Run State** without owning validation, execution, or observation writing. |
| APR-18. **Change Allowance** is still encoded as dirty-path helpers in the Runner Facade | Closed | `c6d7705`, `a69eb40`, `6cb9e20`; `scripts/architecture_program_runner_change_allowance.py`; focused tests and dry-run smoke | None | **Change Allowance** now owns dirty-path classification and worktree checks while preserving conservative rejection behavior. |
| APR-19. **Phase Contract** facts are embedded in prompt string construction | Closed | `22f2c72`, `81a6b70`, `ba04d7a`, `97a0faf`; `scripts/architecture_program_runner_phase_contract.py`; focused tests and dry-run smoke | None | **Phase Contract** now owns skill instructions, single-level boundary rules, shared result/receipt duties, env-override validation duties, and per-phase requirements while prompt rendering consumes those obligations separately from **Phase Environment** facts. |
| APR-20. **Phase Observation** attribution is incomplete | Closed | `04efa20`, `cd84b00`, `adad417`, this closeout commit; `docs/plans/archive/dispatch/phase-observation-attribution-dispatch.md`; `docs/plans/archive/codex-config-architecture-program-runner-phase-observation-attribution-runway.md`; `scripts/architecture_program_runner_phase_observation.py`; final validation: focused runner pytest subset 89 passed, dry-run smoke passed, `uvx ruff` passed, `git diff --check` passed | None | **Phase Observation** now records exact runner-launched session ids and uniquely matched session JSONL paths when directly discoverable, keeps missing, ambiguous, or filesystem-error attribution non-fatal, does not persist env override values, and leaves token persistence in artifact telemetry. |
| APR-21. **Input Inventory** has no enforced contract | Closed | `4331cd4`, `87e20b4`, `0857612`, this closeout commit; `scripts/architecture_program_runner_input_inventory.py`; `docs/plans/archive/dispatch/input-inventory-contract-dispatch.md`; `docs/plans/archive/codex-config-architecture-program-runner-input-inventory-contract-runway.md`; final validation: focused runner pytest subset 129 passed, dry-run smoke passed, `uvx ruff` passed, `git diff --check` passed | None | **Input Inventory** now has a project-neutral owner, compact JSON shape validation, expected evidence-path enforcement for structured phases, prompt/protocol documentation, and manifest/telemetry path exposure without transcript or session-log reconstruction. |
| APR-22. **Planning Root** and **Plan Archive** are not implemented | Closed | `c60bdc3`; `docs/adr/0001-planning-root-and-plan-archive.md`; `docs/plans/README.md`; `docs/plans/archive/README.md` | None | Active planning root is `docs/plans/`; archive is `docs/plans/archive/`; the old `plans/` path is only a temporary compatibility location for the now-closing extraction-prep spec and dispatch. |
| APR-23. Generic workflow contract is only product prose | Closed | `d1cd512`; `docs/plans/generic-phase-runner-workflow-contract.md`; `docs/plans/generic-phase-runner-product-idea.md` | None | Contract maps **Workflow**, **Phase**, **Worker**, **Receipt**, **State**, and **Artifact** while keeping Codex prompts, Batch Runway policy, personal plans, GitHub coordination, and Graphify validation outside the generic boundary. |
| APR-24. Worker adapter seam is Codex-only in production | Closed | `ec58657`; `scripts/architecture_program_runner_workers.py`; `scripts/architecture_program_runner.py`; focused worker tests | None | Production Codex phase execution now routes through `CodexExecWorker` and `execute_phase_with_worker` while preserving `execute_codex_phase` compatibility and **Runner Facade** behavior. |
| APR-25. Shell-only workflow regression coverage is missing | Closed | `7a375b4`; `ShellCommandWorker`; `tests/test_architecture_program_runner.py` | None | Shell worker coverage proves an argv-based command can produce a compact phase result that existing validation, receipt equality, and **Phase Transition** rules consume without Codex or Batch Runway prompt language. |
| APR-26. Separate `phase-runner` repository split is premature | Candidate | `docs/plans/phase-runner-repo-split-issue-12-plan.md`; `docs/plans/phase-runner-business-logic-contract.md`; APR-22 through APR-25 closeout evidence | Create a bounded contract-first business-logic extraction batch | The target direction is an external OSS Go runner, but the next safe step is still protocol extraction: package basics, shared schemas, planning-state interop, golden fixtures, and facade compatibility before moving code or creating a repo skeleton. |
| APR-27. Local runner has no branch-per-batch isolation mode | Open | GitHub issue #11 | Design after APR-26 clarifies the generic runner boundary | `--batch-branch-mode none|create|require`, deterministic batch branch naming, state/receipt branch metadata, and closeout commit-range evidence remain unimplemented. Keep this separate from repo-split work and PR automation. |
| APR-28. Runner extraction lacks a contract-drift review skill | Open | GitHub issue #14; `docs/plans/phase-runner-business-logic-contract.md`; APR/PBC sources | Create a focused `contract-drift-review` skill when extraction work begins to drift across boundaries | The requested skill does not exist. It should compare runner extraction changes against APR/PBC contracts, facade compatibility, generic-core boundaries, and stale-plan/archive risks without duplicating the full contract text. |
| APR-29. Future runner adapters lack authoring guidance | Open | GitHub issue #16; APR-24 worker seam evidence | Create a `runner-adapter-authoring` skill after APR-26 fixes the generic worker/runtime boundary | `CodexExecWorker` and `ShellCommandWorker` prove the seam, but provider-adapter authoring guidance does not exist. Keep provider quirks out of generic runner core and cover result, receipt, transition, artifact, observation, and input-inventory boundaries. |
| APR-30. Baton dogfood CLIs are unimplemented | Open | GitHub issues #17, #18, #19 | Sequence after APR-26 unless a diagnostic need blocks extraction | `baton-context-map`, `baton-doctor`, and `baton-receipt-inspector` do not exist. Treat them as dogfood diagnostics/reporting surfaces over planned batch context, repo readiness, and runner receipts rather than chat-transcript reconstruction. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| runner-boundary-split | APR-11, APR-12, APR-13 | Closed | First split of the monolithic Runner Facade and broad tests | None | Focused unit tests plus dry-run smoke | `docs/plans/archive/dispatch/runner-boundary-split-dispatch.md` | `docs/plans/archive/codex-config-architecture-program-runner-boundary-split-runway.md` |
| phase-environment-ownership | APR-16 | Closed | Establishes the first new **Concept Owner** from `CONTEXT.md` and clarifies launch/prompt context before contract and observation work | Refreshed ledger and `CONTEXT.md` | Focused command/config/env tests plus dry-run smoke | `docs/plans/archive/dispatch/phase-environment-ownership-dispatch.md` | `docs/plans/archive/codex-config-architecture-program-runner-phase-environment-runway.md` |
| phase-transition-change-allowance | APR-17, APR-18 | Closed | Both reduce run-loop state/path policy knowledge after environment context is clearer | APR-16 satisfied | Run-loop and changed-path tests plus dry-run smoke | `docs/plans/archive/dispatch/phase-transition-change-allowance-dispatch.md` | `docs/plans/archive/codex-config-architecture-program-runner-phase-transition-change-allowance-runway.md` |
| phase-contract-catalog | APR-19 | Closed | Separates normative **Phase Contract** facts from rendered prompt text | APR-16 satisfied; APR-17/APR-18 satisfied | Contract/command tests plus dry-run smoke | `docs/plans/archive/dispatch/phase-contract-catalog-dispatch.md` | `docs/plans/archive/codex-config-architecture-program-runner-phase-contract-catalog-runway.md` |
| phase-observation-attribution | APR-20 | Closed | Reframes telemetry attribution as **Phase Observation** work | APR-16, APR-19 satisfied | Artifact and observation tests with synthetic session logs plus dry-run smoke; no live nested Codex required | `docs/plans/archive/dispatch/phase-observation-attribution-dispatch.md` | `docs/plans/archive/codex-config-architecture-program-runner-phase-observation-attribution-runway.md` |
| input-inventory-contract | APR-21 | Closed | Gives **Input Inventory** an enforced shape and artifact linkage | APR-16; APR-20 satisfied | Unit tests with synthetic inventories and prompt checks plus dry-run smoke | `docs/plans/archive/dispatch/input-inventory-contract-dispatch.md` | `docs/plans/archive/codex-config-architecture-program-runner-input-inventory-contract-runway.md` |
| phase-runner-extraction-prep | APR-22, APR-23, APR-24, APR-25 | Closed | Closed the issue #12 wait condition before any repo split: planning root/archive, generic workflow contract, Codex adapter seam, and shell-worker proof | Closed concept-owner batches; issue #12 decision note | Project-harness production with docs-only overrides for planning slices | `plans/dispatch/phase-runner-extraction-prep-dispatch.md` | `plans/codex-config-phase-runner-extraction-prep-runway.md` |
| phase-runner-business-logic-extraction | APR-26 | Candidate | Define the implementation-neutral runner contracts, Go/OSS package boundary, and planning-state interop protocol before repo/package moves | APR-22 through APR-25 closed; issue #12 reassessment; `docs/plans/phase-runner-business-logic-contract.md` | Contract tests for workflow/state/result/receipt/worker/artifact behavior, planning-state interop fixture tests, focused facade compatibility tests, dry-run smoke, ruff, `git diff --check` | TBD under `docs/plans/programs/architecture-program-runner/batches/phase-runner-business-logic-extraction/dispatch.md` | TBD under `docs/plans/programs/architecture-program-runner/batches/phase-runner-business-logic-extraction/runway.md` |
| branch-per-batch-isolation | APR-27 | Future candidate | Adds reviewable batch isolation after the generic/extraction boundary is clearer | APR-26 preferred | Focused runner state/receipt/worktree tests, branch command tests, dry-run smoke, ruff, `git diff --check` | TBD | TBD |
| runner-contract-review-skills | APR-28, APR-29 | Future candidate | Adds support skills for extraction drift review and future provider adapter authoring | APR-26 preferred | Skill owner checks, manifest tests, focused docs/reference tests, and contract-source grep checks | TBD | TBD |
| baton-dogfood-diagnostics | APR-30 | Future candidate | Groups context-map, doctor, and receipt-inspector CLIs because all read runner/planning artifacts and produce compact operational diagnostics | APR-26 preferred; split if one diagnostic becomes urgent | Focused CLI tests over fixture planning roots and runner artifacts, no transcript reconstruction, ruff, `git diff --check` | TBD | TBD |

## Selected Next Candidate

- Batch: `phase-runner-business-logic-extraction`
- Dispatch:
  `docs/plans/programs/architecture-program-runner/batches/phase-runner-business-logic-extraction/dispatch.md`
  when selected
- Spec:
  `docs/plans/programs/architecture-program-runner/batches/phase-runner-business-logic-extraction/runway.md`
  after dispatch selection
- Active ledger: `docs/plans/programs/architecture-program-runner/LEDGER.md`
- Status: candidate; create a dispatch/spec before coding
- Contract source:
  `docs/plans/phase-runner-business-logic-contract.md`
- Goal: extract the runner business logic through implementation-neutral
  contracts first, choose Go module/repo/package basics explicitly, define
  planning-state interop as a command/file protocol, then move only the generic
  control-plane kernel if facade compatibility tests stay green.
- Guardrails:
  - Preserve current CLI arguments, direct script execution, phase order, Run
    Summary shape, phase-result schema, receipt equality, and structured
    artifact layout.
  - Keep Codex skills, architecture-program phase prompts, personal planning
    policy, and Graphify-specific validation in `codex-config`.
  - Keep Batch Runway, architecture-program phase prompts, personal planning
    policy, and Graphify-specific validation out of the generic core.
  - Keep `planning_state` outside the runner core; consume planning facts only
    through explicit schemas, command output, exit codes, and fixtures.
  - Define CLI/API entrypoint, tests, ruff/type command, CI expectations, and
    Docker stance before moving code or creating a repo skeleton.
- Suggested slices:
  - Confirm Go package/runtime basics, target module/repo name, OSS license
    stance, and compatibility promise.
  - Build target contracts and tests for workflow, state, result, receipt,
    transition, and workers without Codex prompt construction.
  - Add provider-neutral artifact, telemetry, input inventory, and change
    allowance contracts.
  - Define planning-state interop fixtures and command/file protocol tests.
  - Add the `codex-config` adapter/facade compatibility layer and move generic
    code only when the existing Runner Facade remains green.

## Recommended Work Order

Completed:
- `phase-environment-ownership`: clarified launch and prompt context first.
- `phase-transition-change-allowance`: removed state/path policy knowledge from
  the run loop after environment context is named.
- `phase-contract-catalog`: made phase obligations testable independently of
  prompt layout.
- `input-inventory-contract`: enforced consumed-input evidence without changing
  the phase-result schema or adding transcript reconstruction.

Remaining:
1. `phase-runner-business-logic-extraction`: use the port-by-contract artifact
   to define package basics, target contracts, and a facade compatibility layer
   before any repo skeleton or runtime move.
2. `branch-per-batch-isolation`: revisit issue #11 after APR-26 clarifies
   whether branch policy belongs in `codex-config`, Baton, or an adapter.
3. `runner-contract-review-skills`: create issue #14/#16 support skills only
   after the contract source map is stable enough to keep the skills compact.
4. `baton-dogfood-diagnostics`: create issue #17/#18/#19 CLIs as dogfood
   diagnostics once runner artifacts and planning-state interop are stable.

## Closeout Rules

- Mark APR-16 closed only after a concept owner owns both launch context and
  prompt context facts, focused tests pass, and the Runner Facade behavior is
  unchanged.
- Mark APR-17 closed only after **Phase Transition** is testable as the place
  that consumes a valid **Phase Result** and updates **Run State**.
- Mark APR-18 closed only after **Change Allowance** can be understood without
  reading Runner Facade orchestration.
- Mark APR-19 closed only after **Phase Contract** facts can be tested without
  depending on unrelated prompt layout.
- Mark APR-20 closed only when exact session/path attribution is implemented or
  an explicit decision says missing attribution is acceptable.
- Mark APR-21 closed only when **Input Inventory** existence, shape, and
  manifest linkage are enforced or explicitly rejected.
- Mark APR-22 closed only after the ADR exists, paths are migrated, and stale
  plans/reports have a clear **Plan Archive** home.
- Mark APR-23 closed only after a generic workflow contract maps the current
  runner to **Workflow**, **Phase**, **Worker**, **Receipt**, **State**, and
  **Artifact**, while naming what remains `codex-config`-specific.
- Mark APR-24 closed only after production Codex phase execution routes through
  an explicit worker adapter seam without changing **Runner Facade** behavior.
- Mark APR-25 closed only after a shell worker test proves the same state,
  receipt, validation, and transition rules without Codex or Batch Runway
  prompt language.
- Promote APR-26 only when extraction-prep evidence supports a repo-split
  decision, and keep Go package basics, protocol schemas, planning-state
  interop, and facade compatibility explicit before moving code.
- Mark APR-27 closed only after branch mode parsing, deterministic branch
  create/reuse, require-mode refusal, state/receipt branch metadata, and
  closeout branch/commit-range evidence are covered without changing default
  runner behavior.
- Mark APR-28 closed only after `contract-drift-review` exists, names its
  APR/PBC sources, distinguishes generic-core drift from `codex-config`
  integration drift, and validates without duplicating the full contract text.
- Mark APR-29 closed only after `runner-adapter-authoring` exists, points to
  the current worker seam and APR/PBC contract sources, and covers adapter
  boundary, test-pattern, limitation, and failure-mode guidance.
- Mark APR-30 closed only after the requested Baton dogfood diagnostics either
  exist with fixture-backed CLI tests or are split with explicit rationale; none
  may reconstruct execution from chat transcripts as canonical evidence.

## Validation Snapshot

- Last closed runner-boundary batch reported 71 focused runner tests passing,
  dry-run smoke passing, `uvx ruff check` passing with a non-fatal Python
  symlink warning, and `git diff --check` passing.
- Phase Environment closeout passed 78 focused runner tests, dry-run smoke,
  `uvx ruff check` with the known non-fatal Python symlink warning, and
  `git diff --check`.
- Phase Transition and Change Allowance closeout passed 80 focused runner tests,
  dry-run smoke, `uvx ruff check` with the known non-fatal Python symlink
  warning, and `git diff --check`.
- Input Inventory closeout passed 129 focused runner tests, dry-run smoke,
  `uvx ruff check scripts tests` with the known non-fatal Python symlink
  warning, and `git diff --check`.
- Phase Runner Extraction Prep closeout passed 132 focused runner/owner tests,
  dry-run smoke, `uvx ruff check scripts tests` with the known non-fatal Python
  symlink warning, and `git diff --check`.
