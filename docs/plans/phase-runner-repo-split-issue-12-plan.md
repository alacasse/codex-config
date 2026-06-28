# Issue 12 Phase Runner Repo Split Plan

## Issue

GitHub issue: <https://github.com/alacasse/codex-config/issues/12>

Evaluate whether to create a separate `phase-runner` repo earlier than planned
and use `codex-config` as the first dogfooding consumer.

## Recommendation

Decide the split direction now, but wait to extract code into a new repo until
one extraction-prep batch is complete.

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
- The only real execution **Adapter** is `codex exec`; the test seam accepts a
  fake executor, but there are not yet two production **Adapters** at a generic
  worker **Seam**.
- Active planning now lives under `docs/plans/`; **Planning Root** and
  **Plan Archive** are recorded in ADR 0001. The active extraction-prep runway
  spec and dispatch remain under `plans/` only as a temporary compatibility
  exception until that batch closes.

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
5. Package basics are defined for the new repo or extraction branch: CLI
   entrypoint, tests, ruff/type command, CI, and Docker only if dogfooding
   proves it is needed.

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
   both cross the same seam cleanly, create the `phase-runner` repo skeleton
   and move only the generic core.

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
     `skills/architecture-program-runway/references/local-runner-v1.md`, future
     `docs/plans/` reference.
   - Problem: the product idea names generic concepts, but the executable
     runner still treats the architecture-program sequence as the only shape.
   - Solution: document and then code a generic workflow shape while mapping
     the current architecture program onto it.
   - Benefits: better **Depth** at the workflow **Interface** and easier tests
     that do not need Codex, Batch Runway, or a project ledger.

3. **Planning Root Cleanup**

   - Files: `docs/plans/codex-config-architecture-program-runner-findings.md`,
     `docs/plans/`, `docs/plans/archive/`, ADR 0001.
   - Problem: a new public repo would inherit current planning-location churn.
   - Solution: close APR-22 before extraction.
   - Benefits: better **Locality** for active plans versus archives, and a
     cleaner dogfooding story for `codex-config` as the first consumer.

## Decision

Do not create the separate repo as the next coding step. Do the extraction-prep
batch first. After that, split only the generic kernel and keep the Codex skills
and architecture-program workflow integration in `codex-config`.
