# Issue 12 Phase Runner Repo Split Plan

## Issue

GitHub issue: <https://github.com/alacasse/codex-config/issues/12>

Evaluate whether to create a separate `phase-runner` repo earlier than planned
and use `codex-config` as the first dogfooding consumer.

## Recommendation

Decide the split direction now: the long-term target is an external OSS Go
runner. The next work should still be contract-first. Do not create a repo
skeleton or move runtime behavior until the shared protocol is explicit enough
for `codex-config` and the Go runner to interoperate through files, schemas,
commands, fixtures, and exit codes.

The current **Runner Facade** has enough concept ownership to make the split
worth planning. It is not yet shaped as a generic `phase-runner` **Module**.
Its public **Interface** is still architecture-program and Codex-specific:
fixed `select-dispatch -> create-spec -> execute -> closeout` **Phases**,
`--program-ledger`, `--execute-batches`, Batch Runway language, Codex prompts,
Codex output-schema constraints, sandbox/model flags, and skill references.

## Current State

Generic-looking **Modules**:

- **Run State**: resumable progress, artifact paths, active batch, stop reason.
- **Phase Result** and **Phase Receipt**: schema-valid result and persisted
  equality check.
- **Phase Transition**: consumes a valid result and updates **Run State**.
- **Phase Observation**: records runner-observed launch and attribution facts.
- **Input Inventory**: records phase-consumed context evidence.
- Run and batch artifact manifests, telemetry, atomic JSON writes, and final
  **Run Summary**.

Still `codex-config`-specific:

- The **Runner Facade** CLI vocabulary is architecture-program vocabulary.
- The fixed **Phase** sequence is not a generic workflow definition.
- **Phase Contract** content names `architecture-program-runway` and
  `batch-runway`.
- **Phase Environment** points at repo skill references and Codex schema files.
- The production `codex exec` path now crosses an internal worker **Seam**
  through `CodexExecWorker`, and `ShellCommandWorker` proves the same
  validation, receipt, and transition rules without Codex prompts.
- Active planning now lives under `docs/plans/`; **Planning Root** and
  **Plan Archive** are recorded in ADR 0001. The closed extraction-prep runway
  spec and dispatch remain under `plans/` as historical compatibility
  artifacts; future active dispatch/spec work should be created under
  `docs/plans/`.

## Post-Prep Reassessment

Evidence from `phase-runner-extraction-prep`:

- APR-22: `docs/plans/` is the active **Planning Root** and
  `docs/plans/archive/` is the **Plan Archive**, recorded by ADR 0001.
- APR-23: `docs/plans/generic-phase-runner-workflow-contract.md` maps
  **Workflow**, **Phase**, **Worker**, **Receipt**, **State**, and
  **Artifact** while keeping Codex and Batch Runway policy out of the generic
  boundary.
- APR-24: `execute_codex_phase` now routes through `CodexExecWorker` and
  `execute_phase_with_worker` without changing the **Runner Facade**.
- APR-25: `ShellCommandWorker` tests prove a shell-only phase can use existing
  result validation, receipt equality, and state transition rules without
  Codex command construction or Batch Runway prompt language.

Next action: create a bounded contract-first business-logic extraction batch
for APR-26 using `docs/plans/phase-runner-business-logic-contract.md`. That
batch should define Go package basics and protocol boundaries first, then move
only the generic workflow, state, result, receipt, worker, transition, artifact,
telemetry, input inventory, change-allowance, and planning-state interop
contracts if the facade compatibility tests stay green.

`scripts/planning_state.py` should remain separate from the runner core. It can
provide a documented preflight or adapter protocol for Planning Artifact Layout
v1 facts, but the Go runner should not import Python internals, duplicate
`codex-config` Markdown heuristics, or infer selected work from old filenames
when root/program `CURRENT.md` files exist.

## Wait Condition

Split after these conditions are true:

1. APR-22 is closed: active planning moved to `docs/plans/`, the
   **Plan Archive** exists at `docs/plans/archive/`, and an ADR records the
   planning-root decision.
2. A generic workflow model exists in code, not only in
   `docs/plans/generic-phase-runner-product-idea.md`: **Workflow**, **Phase**,
   **Worker**, **Receipt**, **State**, and **Artifact**.
3. A real worker **Adapter** **Seam** exists with at least two adapters,
   initially `shell` and `codex-exec`. One adapter is only a hypothetical seam.
4. `codex-config` consumes the generic core through a Codex adapter/example
   layer while keeping `architecture-program-runway`, `batch-runway`, personal
   plans, and Graphify workflow state in `codex-config`.
5. Package basics are defined for the new Go repo, extraction branch, or
   in-repo generic package: module name, CLI/API entrypoint, tests, lint/type
   command, CI, license stance, and Docker only if dogfooding proves it is
   needed.
6. Planning-state interop is defined as a command/file protocol with JSON
   shape, warning/error shape, exit-code meaning, and golden fixtures.

## Smallest Useful Extraction Prep Batch

Goal: make the generic **Interface** visible without moving code to a new repo.

1. Record the **Planning Root** ADR and migrate active planning to
   `docs/plans/` with completed material under `docs/plans/archive/`.
2. Add a generic workflow contract document beside the product idea. It should
   map current runner concepts to generic names and explicitly name what stays
   in `codex-config`.
3. Introduce a minimal internal generic worker **Seam** in the current runner:
   a shell worker contract plus the existing Codex execution as a Codex
   **Adapter**. Keep the **Runner Facade** behavior unchanged.
4. Add tests that prove a simple shell-only workflow can pass through the same
   **State**, **Receipt**, and **Transition** rules without Batch Runway skill
   language.
5. Reassess issue #12 after that batch. If the shell workflow and Codex adapter
   both cross the same seam cleanly and planning-state interop is explicit,
   create the Go repo skeleton and move only the generic core.

## Deepening Opportunities

1. **Worker Adapter Seam**

   - Files: `scripts/architecture_program_runner.py`,
     `scripts/architecture_program_runner_command.py`, future generic workflow
     tests.
   - Problem: `phase_executor` is a useful test seam, but production execution
     is Codex-only. The **Interface** is still the command-building details.
   - Solution: introduce a small worker **Seam** that can run a shell command
     or Codex phase and return a **Phase Result**.
   - Benefits: higher **Leverage** because workflow execution stops depending
     on Codex command construction; better **Locality** because provider quirks
     live in adapters.

2. **Generic Workflow Contract**

   - Files: `docs/plans/generic-phase-runner-product-idea.md`,
     `docs/plans/generic-phase-runner-workflow-contract.md`,
     `skills/architecture-program-runway/references/local-runner-v1.md`.
   - Problem: the product idea names generic concepts, but the executable
     runner still treats the architecture-program sequence as the only shape.
   - Solution: document and then code a generic workflow shape while mapping
     the current architecture program onto it.
   - Benefits: better **Depth** at the workflow **Interface** and easier tests
     that do not need Codex, Batch Runway, or a project ledger.

3. **Planning Root Cleanup**

   - Files: `docs/plans/programs/codex-config/LEDGER.md`,
     `docs/plans/`, `docs/plans/archive/`, ADR 0001.
   - Problem: a new public repo would inherit current planning-location churn.
   - Solution: close APR-22 before extraction.
   - Benefits: better **Locality** for active plans versus archives, and a
     cleaner dogfooding story for `codex-config` as the first consumer.

## Decision

Create the protocol-extraction batch as the next candidate, not a direct repo
skeleton or file move. The eventual repo should be an OSS Go runner. Split only
the generic kernel after shared contracts and fixtures exist, and keep the
Codex skills, architecture-program workflow integration, local planning policy,
planning-state Markdown diagnostics, and Graphify-specific validation outside
the new repo.
