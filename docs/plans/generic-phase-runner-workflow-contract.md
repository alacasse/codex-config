# Generic Phase Runner Workflow Contract

## Purpose

This contract defines the generic workflow boundary that the current
architecture-program runner can prove inside `codex-config` before any separate
`phase-runner` repository exists.

It is not a public package API, YAML workflow schema, or extraction plan. It is
the interface reference for the internal worker-adapter slices that follow.

## Generic Boundary

A generic phase runner owns these concepts:

- **Workflow**: a named sequence or graph of **Phases**, transition rules, stop
  conditions, and artifact rules.
- **Phase**: one bounded workflow step with declared inputs, an assigned
  **Worker**, expected **Receipt** shape, allowed outputs, transition rules, and
  stop conditions.
- **Worker**: an adapter-backed executor that runs one **Phase** and returns a
  validated phase result or a runner error. A worker may be a shell command,
  local script, `codex-exec` process, webhook, human approval step, or future
  provider adapter.
- **Receipt**: compact durable evidence for one completed phase result.
  Receipts are machine-readable control-plane evidence, not transcripts, logs,
  prompt text, or telemetry dumps.
- **State**: the durable progress record used to resume the workflow and choose
  the next phase.
- **Artifact**: a workflow-owned file or external evidence item produced around
  a run or phase, including receipts, manifests, validation output, reports, and
  logs when a workflow chooses to keep them.

The generic runner may validate phase results, compare receipts, update state,
apply transition rules, and record artifact locations. It must not require a
specific coding agent, prompt format, issue tracker, project ledger, or personal
workflow convention.

## Current Runner Mapping

The current architecture-program runner maps into the generic contract this
way:

| Generic concept | Current `codex-config` concept |
|---|---|
| **Workflow** | One architecture-program runner invocation around a Program Ledger and the fixed `select-dispatch -> create-spec -> execute -> closeout` sequence |
| **Phase** | The existing **Phase** concept from `CONTEXT.md` |
| **Worker** | Today, the production Codex execution path behind `execute_codex_phase`; future slices introduce explicit `codex-exec` and `shell` adapters |
| **Receipt** | **Phase Receipt**, which persists exactly one schema-valid **Phase Result** and must match it exactly |
| **State** | **Run State**, the resumable record for one architecture-program run |
| **Artifact** | **Run Artifact** and **Batch Artifact**, including receipts, manifests, telemetry, dispatch packets, and generated runway evidence |

The current architecture-program sequence is one valid `codex-config`
workflow. It is not the only possible generic workflow.

## `codex-config` Integration Boundary

These remain `codex-config`-specific integration details:

- architecture-program phase names and their fixed order;
- Program Ledger and Dispatch Packet semantics;
- Codex prompts, output-schema constraints, sandbox/model flags, and
  `codex exec` command construction;
- Batch Runway and architecture-program-runway skill language;
- repo-owned Codex configuration and owner checks;
- local personal plans, ignored workflow overlays, and Graphify-specific
  validation policy;
- GitHub issue language used to coordinate this repository.

Generic worker behavior stops at executing one phase and returning a validated
phase result or runner error. Architecture-program prompt semantics, skill
instructions, and project-planning policy stay on the `codex-config`
integration side of the boundary.

## Non-Goals For This Contract

- Do not define a public Python API.
- Do not define YAML workflow loading.
- Do not require SQLite, CI, Docker, GitHub, or network services.
- Do not turn transcripts, session logs, or telemetry into receipts.
- Do not make Batch Runway execution rules part of the generic runner core.
