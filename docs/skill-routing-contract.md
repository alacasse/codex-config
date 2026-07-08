# Skill Routing Contract

This document defines how agents route human workflow intent to command-owner,
runtime, and support skills during the command-owner skill migration.

The current command-owner skills own human intent, routing, and stop
conditions. Older runtime skills own detailed procedures. Support skills
provide diagnostics, layout rules, review support, evidence classification, or
validation guidance.

This is a transitional bridge state created by the copy-first migration. It is
not the final architecture. A later migration may rewrite command-owner skills
into true end-to-end owners, but that is not the current state.

## Skill Audiences

- **Human-facing command-owner skill**: the primary skill that owns the user's
  workflow intent, routing choice, and stopping point.
- **Runtime workflow skill**: an agent-facing skill that owns a detailed
  procedure after a command-owner skill selects it.
- **Agent-facing support skill**: a narrow diagnostic, layout, review,
  evidence, or validation helper used inside another workflow.
- **Default workflow obligation**: a rule normal implementation or review work
  must enforce without requiring a separate user command.
- **Transitional bridge skill**: a command-owner skill that currently routes to
  runtime skills while the migration is copy-first.

## Routing Table

| User intent | Primary command-owner skill | Runtime/support skills |
| --- | --- | --- |
| Capture a finding, issue, cleanup need, or work request in a durable ledger | `add-to-ledger` | `planning-state`, `planning-artifacts`, `architecture-program-runway`; `legacy-removal` only for evidence-backed legacy scoping |
| Plan the next bounded batch/spec from current ledger state | `plan-batch` | `planning-state`, `planning-artifacts`, `architecture-program-runway`, then `batch-runway` in `create-spec` mode |
| Execute the current queued or active batch runway | `work-batch` | `planning-state`, `planning-artifacts`, then `batch-runway` in `execute-spec` mode |
| Extract behavior contracts before a rewrite, migration, or port | `port-by-contract` | `batch-runway` or `architecture-program-runway` only after contract artifacts exist |

## Conflict Rule

When a human-facing command-owner skill and an older runtime skill both appear
applicable, the command-owner skill owns the user request. The runtime skill may
be used only as the detailed procedure after the command-owner skill routes to
it.

## Stop Rule

If the agent cannot name the user intent, primary command-owner skill,
runtime/support skills, and stopping point, it must stop before editing files.

## Bridge-State Rule

The current command-owner skills are bridge-state command owners. They are
allowed to route to runtime skills. They must not be treated as final
autonomous implementations, and the runtime skills must not be treated as
deprecated merely because command-owner skills exist.

## Anti-Patterns

- Invoking `batch-runway` directly for a human "work on the batch" request
  unless the command-owner route has selected it.
- Reselecting a program batch during `work-batch`.
- Using `port-by-contract` as a general skill rewrite excuse before contracts
  exist.
- Preserving old runtime names forever by accident.
- Marking the migration complete without stating whether it is
  interface-complete or architecture-complete.
