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
| **Worker** | The internal `PhaseWorker` seam with `CodexExecWorker` for the production Codex path and `ShellCommandWorker` as the shell-only proof adapter |
| **Receipt** | **Phase Receipt**, which persists exactly one schema-valid **Phase Result** and must match it exactly |
| **State** | **Run State**, the resumable record for one architecture-program run |
| **Artifact** | **Run Artifact** and **Batch Artifact**, including receipts, manifests, telemetry, dispatch packets, and generated runway evidence |

The current architecture-program sequence is one valid `codex-config`
workflow. It is not the only possible generic workflow.

## External Go Runner Boundary

The intended long-term direction is a separate OSS Go runner that implements
the generic workflow contract without depending on `codex-config` internals.
Keep interoperability at file, schema, and CLI boundaries:

- versioned workflow/run-state/result/receipt/input-inventory schemas;
- declared artifact layout for runs, batches, receipts, telemetry, and
  manifests;
- stable exit-code and validation semantics;
- golden fixtures that both the Python dogfooding runner and the Go runner can
  read and write;
- adapter-owned provider behavior such as `codex exec`, shell commands, or
  future providers.

Do not make the Go project import Python modules, reuse the Python file split,
or depend on `codex-config` planning policy. Do not make `codex-config` import
the Go implementation as a library during early extraction. The safe first
integration is command/file interop: one side writes contract artifacts, the
other validates or consumes them.

`scripts/planning_state.py` is a diagnostic/protocol checker for Planning
Artifact Layout v1 roots. It should remain independent of the runner core. A
runner may call an external planning-state command or consume its schemas later,
but the generic runner should not embed `codex-config` planning-root discovery,
Graphify fixtures, or Markdown editing rules.

## Proven Internal Adapters

The extraction-prep batch proved the worker boundary with two internal
adapters:

- `CodexExecWorker`: preserves the existing `codex exec` command, prompt,
  environment, output-last-message, and phase-observation behavior behind the
  worker seam.
- `ShellCommandWorker`: runs an argv-based command with `shell=False`, reads a
  compact phase-result JSON file, and lets existing validation, receipt, and
  transition code handle the result.

These adapters are evidence for extraction planning, not a public package API
or user-facing workflow definition.

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
- Do not define Go package layout.
- Do not make `planning_state` part of the runner core.
- Do not require either implementation to import the other.
- Do not require SQLite, CI, Docker, GitHub, or network services.
- Do not turn transcripts, session logs, or telemetry into receipts.
- Do not make Batch Runway execution rules part of the generic runner core.
