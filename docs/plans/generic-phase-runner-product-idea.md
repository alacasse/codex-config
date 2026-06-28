# Generic Phase Runner Product Idea

## Summary

Explore whether the current architecture program runner can evolve into a standalone, tool-agnostic open-source project.

The generic project would not be a coding agent and would not be tied to
Codex. It would be a small phase-based workflow runner for long-running work
where each phase can be executed by a disposable worker that returns either a
validated phase result or a runner error. Compact durable receipts can preserve
evidence for completed phase results.

Contract reference:
`docs/plans/generic-phase-runner-workflow-contract.md` is the current boundary
document for mapping this product idea to the `codex-config` runner. Keep this
file as product positioning and examples; keep generic-vs-integration contract
language in the contract document.

## Core thesis

Long-running workflows should not depend on one long-lived process, one giant model context, or one vendor-specific agent session.

Instead:

- break the workflow into bounded phases;
- run each phase with the best available worker;
- persist state outside the worker;
- keep compact durable evidence for completed phase results;
- stop on explicit safety or completion conditions;
- resume from durable artifacts.

## Generic value proposition

A phase runner for resumable long-running workflows.

Potential tagline:

> Run disposable workers through durable, auditable workflow phases.

Or, for agent-oriented positioning:

> Run coding agents, shell jobs, and automation workers as phase workers while keeping workflow state durable, auditable, and resumable.

## Concepts

This section is a non-normative product summary. The workflow contract is the
authoritative boundary for generic runner behavior.

### Workflow

A named set of phases, transitions, stop conditions, and artifact rules.

### Phase

One bounded unit of work.

A phase has:

- an id;
- inputs;
- a worker definition;
- an expected phase-result shape;
- receipt/evidence rules for completed results;
- allowed outputs;
- transition rules;
- stop conditions.

### Worker

Anything that can execute a phase and return a validated phase result or runner
error.

Possible worker types:

- shell command;
- Python script;
- Codex exec;
- Claude Code;
- HTTP webhook;
- GitHub Actions workflow;
- queue worker;
- manual human step;
- future cloud agent provider.

### Receipt

Compact durable evidence for one completed phase result.

Receipts should be compact, machine-readable, and durable. They are not the
worker result contract, transcripts, or logs.

### State

The durable progress record used for resume and next-phase decisions.

### Artifact

Any file or external evidence produced by a phase, such as reports, manifests, validation output, or logs.

## Why this is broader than coding agents

The current use case came from Codex and Batch Runway, but the abstraction is not Codex-specific.

The same model can apply to:

- data migrations;
- report/export pipelines;
- release workflows;
- validation workflows;
- long-running refactors;
- AI-assisted ticket processing;
- incident follow-up workflows;
- compliance evidence collection;
- backend batch processing.

## Example generic workflow

This YAML is an illustrative product sketch, not a generic runner core
requirement or committed file-shape contract.

```yaml
name: report-export
state_path: .phase-runs/report-export/run-state.json

phases:
  - id: snapshot
    worker:
      type: shell
      command: python scripts/create_snapshot.py
    receipt: receipts/snapshot.json
    next: validate_snapshot

  - id: validate_snapshot
    worker:
      type: shell
      command: python scripts/validate_snapshot.py
    receipt: receipts/validate_snapshot.json
    next: generate_report

  - id: generate_report
    worker:
      type: shell
      command: python scripts/generate_report.py
    receipt: receipts/generate_report.json
    next: done
```

## Example agent workflow

This YAML is an illustrative Codex-oriented product example. Prompt paths and
`output_schema` fields are provider/integration details, not generic runner
core semantics.

```yaml
name: agentic-refactor

phases:
  - id: select-dispatch
    worker:
      type: codex-exec
      prompt: prompts/select-dispatch.md
      output_schema: schemas/phase-result.json
    next: create-spec

  - id: create-spec
    worker:
      type: codex-exec
      prompt: prompts/create-spec.md
      output_schema: schemas/phase-result.json
    next: execute

  - id: execute
    worker:
      type: codex-exec
      prompt: prompts/execute.md
      output_schema: schemas/phase-result.json
    next: closeout

  - id: closeout
    worker:
      type: codex-exec
      prompt: prompts/closeout.md
      output_schema: schemas/phase-result.json
    next: done
```

## Product boundary

The project should not try to replace Airflow, Temporal, GitHub Actions, or agent platforms.

It should be smaller:

- repo-owned;
- file-first;
- phase-oriented;
- resumable;
- friendly to human/agent/tool hybrid workflows;
- usable locally first;
- open to cloud workers through adapters.

## Differentiation

### Not a coding agent

It does not write code by itself. It runs workers.

### Not an agent framework

It does not impose a multi-agent runtime. It can launch agents as workers, but workers are replaceable.

### Not a distributed workflow engine

It should stay lightweight and local-first in early versions.

### Not a CI/CD platform

It can call CI or shell validation as workers, but it is mainly a durable phase protocol and runner.

## Possible architecture

```text
phase-runner/
  runner/
    cli.py
    workflow.py
    state.py
    receipts.py
    validation.py
    artifacts.py
    telemetry.py
    logs.py
    sqlite_index.py
  providers/
    shell.py
    codex_exec.py
    http.py
    manual.py
  protocols/
    phase-result.schema.json
  examples/
    generic-report-export/
    codex-architecture-program/
  docs/
    concepts.md
    receipts.md
    resume.md
    logging.md
    provider-adapters.md
```

## Provider adapter concept

A provider adapter executes one phase and returns a validated phase result or a
runner error.

Conceptual interface:

```text
run_phase(phase, state, artifacts, environment) -> PhaseResult | RunnerError
```

Initial providers:

- shell command;
- Codex exec.

Later providers:

- HTTP webhook;
- GitHub Actions workflow;
- manual approval;
- cloud agent task provider.

## Source-of-truth model

Keep canonical state inspectable and durable:

- workflow definition;
- run-state file;
- phase receipts;
- artifacts;
- telemetry;
- optional SQLite projection.

SQLite, if used, should be a rebuildable operational index, not the canonical state.

## Enterprise angle

A generic phase runner could be useful in enterprise contexts where teams need durable automation without adopting a heavy distributed workflow system.

Potential use cases:

- backend batch workflows;
- report generation;
- migration orchestration;
- validation gates;
- release checklists;
- AI-assisted internal tooling;
- agentic developer productivity workflows.

## Open-source narrative

The open-source story should be based on the problem, not on a specific tool:

> Coding agents and automation workers are good at bounded tasks. Long-running workflows need explicit phase boundaries, durable state, receipts, telemetry, and safe resume.

The current Codex/Graphify work can be the real-world case study that motivated and validated the approach.

## Extraction strategy

Do not extract too early.

Recommended path:

1. Stabilize the current local architecture program runner in `codex-config`.
2. Use it for real Graphify runs.
3. Identify what is generic versus Codex-specific.
4. Extract only the generic runner/protocol core.
5. Keep Codex skills as examples or optional provider packs.
6. Publish a small README and case study before broadening scope.

## Risks

- Becoming a vague workflow engine.
- Overgeneralizing before the concrete runner stabilizes.
- Competing directly with cloud agent platforms instead of acting as a workflow layer around them.
- Hiding durable state in a database too early.
- Making the project too Codex-specific to be useful elsewhere.

## Initial acceptance criteria for exploration

- Identify the smallest generic core that can be separated from `architecture-program-runway`.
- Sketch one possible workflow file shape as a future product example.
- Sketch one possible receipt/evidence format as a future product example.
- Keep at least one provider non-agentic, such as shell.
- Keep Codex as a provider/example, not as the core abstraction.
- Document how the current runner maps onto the generic model.
- Decide whether extraction should become a new repo, a subpackage, or an experimental branch first.
