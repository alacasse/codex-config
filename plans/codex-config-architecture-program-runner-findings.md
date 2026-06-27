# Codex Config Architecture Program Runner Program Ledger

## Purpose

Keep architecture-program runner findings visible across batches without
requiring future agents to replay stale runway specs or block reports. This is
the active **Program Ledger** until the **Planning Root** migration moves active
planning to `docs/plans/`.

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
- Treat stale completed plans and reports as future **Plan Archive** material,
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
- Defer the **Planning Root** migration to a separate batch. The target is
  `docs/plans/`, with **Plan Archive** at `docs/plans/archive/`; create an ADR
  when that migration batch is specified.

## Current Active Surfaces

- Glossary: `CONTEXT.md`
- Current Program Ledger: `plans/codex-config-architecture-program-runner-findings.md`
- Runner Facade: `scripts/architecture_program_runner.py`
- Current concept-owner files:
  - `scripts/architecture_program_runner_state.py`
  - `scripts/architecture_program_runner_validation.py`
  - `scripts/architecture_program_runner_command.py`
  - `scripts/architecture_program_runner_artifacts.py`
- Current focused tests:
  - `tests/test_architecture_program_runner_state.py`
  - `tests/test_architecture_program_runner_validation.py`
  - `tests/test_architecture_program_runner_command.py`
  - `tests/test_architecture_program_runner_artifacts.py`
  - `tests/test_architecture_program_runner_run_loop.py`
  - `tests/test_architecture_program_runner_worktree.py`
  - `tests/test_architecture_program_runner_protocol.py`
  - `tests/test_architecture_program_runner.py`
- Behavioral runner reference:
  `skills/architecture-program-runway/references/local-runner-v1.md`

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
| APR-19. **Phase Contract** facts are embedded in prompt string construction | In runway | `plans/dispatch/phase-contract-catalog-dispatch.md`; `plans/codex-config-architecture-program-runner-phase-contract-catalog-runway.md` | Execute the `phase-contract-catalog` runway | Separate normative phase obligations from rendered prompt text and supplied **Phase Environment** facts. |
| APR-20. **Phase Observation** attribution is incomplete | Candidate | APR-9 evidence; current artifact tests | Schedule after concept owners settle | Exact Codex session JSONL discovery is still missing unless a path is supplied. |
| APR-21. **Input Inventory** has no enforced contract | Candidate | APR-10 evidence; prompt guidance | Schedule after APR-20 or after Phase Environment if needed | Runner prompts mention inventories, but existence, shape, and manifest linkage are not validated. |
| APR-22. **Planning Root** and **Plan Archive** are not implemented | Candidate | `CONTEXT.md` | Create ADR and migration batch when selected | Target active root is `docs/plans/`; target archive is `docs/plans/archive/`; current repo still uses `plans/`. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| runner-boundary-split | APR-11, APR-12, APR-13 | Closed | First split of the monolithic Runner Facade and broad tests | None | Focused unit tests plus dry-run smoke | `plans/dispatch/runner-boundary-split-dispatch.md` | `plans/codex-config-architecture-program-runner-boundary-split-runway.md` |
| phase-environment-ownership | APR-16 | Closed | Establishes the first new **Concept Owner** from `CONTEXT.md` and clarifies launch/prompt context before contract and observation work | Refreshed ledger and `CONTEXT.md` | Focused command/config/env tests plus dry-run smoke | `plans/dispatch/phase-environment-ownership-dispatch.md` | `plans/codex-config-architecture-program-runner-phase-environment-runway.md` |
| phase-transition-change-allowance | APR-17, APR-18 | Closed | Both reduce run-loop state/path policy knowledge after environment context is clearer | APR-16 satisfied | Run-loop and changed-path tests plus dry-run smoke | `plans/dispatch/phase-transition-change-allowance-dispatch.md` | `plans/codex-config-architecture-program-runner-phase-transition-change-allowance-runway.md` |
| phase-contract-catalog | APR-19 | In runway | Separates normative **Phase Contract** facts from rendered prompt text | APR-16 satisfied; APR-17/APR-18 satisfied | Contract/command tests plus dry-run smoke | `plans/dispatch/phase-contract-catalog-dispatch.md` | `plans/codex-config-architecture-program-runner-phase-contract-catalog-runway.md` |
| phase-observation-attribution | APR-20 | Candidate | Reframes telemetry attribution as **Phase Observation** work | APR-16, APR-19 preferred | Artifact tests with synthetic session logs; optional live runner rehearsal | TBD | TBD |
| input-inventory-contract | APR-21 | Candidate | Gives **Input Inventory** an enforced shape and artifact linkage | APR-16; APR-20 preferred but not mandatory | Unit tests with synthetic inventories and prompt checks | TBD | TBD |
| planning-root-archive-migration | APR-22 | Candidate | Moves active planning under `docs/plans/` and creates `docs/plans/archive/` with an ADR | None, but do separately from runner behavior work | Markdown/readback plus path-reference audit | TBD | TBD |

## Selected Batch Brief

- Batch: `phase-contract-catalog`
- Dispatch: `plans/dispatch/phase-contract-catalog-dispatch.md`
- Spec:
  `plans/codex-config-architecture-program-runner-phase-contract-catalog-runway.md`
- Status: Spec created; implementation pending
- Goal: Give **Phase Contract** a clear concept owner so phase obligations are
  testable independently of prompt layout while preserving Runner Facade
  behavior.
- Guardrails:
  - Preserve current CLI behavior and direct script execution.
  - Preserve prompt obligations, command flags, phase-result schema, expected
    receipt path behavior, and dry-run output semantics.
  - Keep **Phase Environment** facts in the environment concept owner.
  - Keep phase-result schema validation, expected next-phase validation, and
    receipt equality in the validation concept owner.
  - Do not implement **Phase Observation** attribution, **Input Inventory**
    validation, or **Planning Root** migration in this batch.
- Suggested slices:
  1. Characterize current **Phase Contract** obligations in focused tests.
  2. Introduce a **Phase Contract** owner for shared and per-phase obligations.
  3. Route prompt rendering through the contract owner while continuing to
     consume **Phase Environment** facts separately.
  4. Tighten tests so contract tests own obligations, command tests own
     rendering, and facade tests preserve compatibility exports.

## Recommended Work Order

Completed:
- `phase-environment-ownership`: clarified launch and prompt context first.
- `phase-transition-change-allowance`: removed state/path policy knowledge from
  the run loop after environment context is named.

Active:
- `phase-contract-catalog`: spec created; implementation pending.

Remaining:
1. `phase-observation-attribution`: improve exact session/path attribution.
2. `input-inventory-contract`: enforce consumed-input evidence.
3. `planning-root-archive-migration`: move active planning to `docs/plans/`,
   create `docs/plans/archive/`, and record the ADR.

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
