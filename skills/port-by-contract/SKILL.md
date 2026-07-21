---
name: port-by-contract
description: Extract implementation-neutral contracts before porting or rewriting software across languages, frameworks, runtimes, or product boundaries. Use when asked to migrate an implementation, prepare a rewrite, or specify behavior for a fresh target without direct file-by-file translation.
---

# Port By Contract

Use this skill to preserve intended behavior while allowing the target design to
change. Extract contracts before proposing target structure or implementation.

## Core rule

Do not translate files directly by default. Source layout, helper names, and
language-specific control flow are evidence, not target requirements. Preserve
them only when they express a supported public or operational contract.

If the user explicitly wants line-by-line translation, explain that this skill
is contract-first. Continue under this skill only if contract extraction is
still wanted.

## Modes

- `intake-source`: map the current implementation and its evidence.
- `distill-contract`: write implementation-neutral behavior contracts. This is
  the default for a requested port or rewrite.
- `design-target`: propose a target architecture that satisfies the contracts.
- `review-target`: compare an implementation with the accepted contracts.

Choose the narrowest useful mode. State unresolved source scope, target, or
validation authority instead of inventing it.

## Source intake

Read repository instructions, domain documentation, supported entrypoints,
tests, schemas, fixtures, and current code. Capture:

- user-facing purpose and supported interfaces;
- state transitions, lifecycle, idempotence, and recovery behavior;
- inputs, outputs, files, schemas, and configuration;
- side effects, provider boundaries, external commands, and environment rules;
- error handling, stop conditions, privacy, and validation behavior;
- tests that prove externally observable behavior;
- implementation details that must not constrain the target.

Prefer current behavior and tests when older documents disagree. Mark intent
that is not implemented as `proposed`, not `current`.

## Contract output

For non-trivial work, write compact repository-local contracts using the
project's existing documentation conventions. Link evidence instead of copying
large source excerpts or logs.

A contract item should identify:

- `id`: stable short identifier;
- `status`: `current`, `proposed`, `target-only`, `deprecated`, or `unknown`;
- `source evidence`: code, test, document, or observed command;
- `contract`: the implementation-neutral rule;
- `target implication`: what must remain or may change;
- `validation`: how the target behavior will be proved.

Cover only relevant surfaces: behavior, state, interface, artifacts, providers,
failure handling, telemetry, validation, and regression tests.

## Target design

Design from contract responsibilities rather than source filenames. For each
target component, record the contract IDs it satisfies, data it owns,
interfaces it exposes, dependencies it calls, failures it surfaces, and tests
that protect it.

Mark deliberate divergences explicitly with rationale and validation. Do not
freeze accidental compatibility, aliases, wrappers, or internal topology.

## Review target

Compare target behavior to every accepted contract ID and classify each as
`satisfied`, `changed`, `deferred`, or `rejected`, with target-side evidence.
Report unresolved gaps directly. Do not turn them into a new task framework or
execution protocol.

## Non-goals

- direct line-by-line translation;
- preserving private source structure;
- inventing missing product decisions;
- producing giant design documents;
- prescribing how Codex plans, delegates, reviews, or integrates the work.
