# GitHub Issue 31: Deletion-Test Vocabulary Ownership

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/31
- Title: CCFG root cause 3: define canonical deletion-test vocabulary ownership
- State when ingested: open
- Created: 2026-07-09
- Source identity: GitHub issue #31, authored by `alacasse`

## Summary

CCFG-11 exposed that deletion-test vocabulary is not clearly owned or enforced
across the workflow skills. The displaced CCFG-11 dispatch/runway used terms
such as `no-op`, `sediment`, `obsolete skill surface`, and
`deletion-safe evidence`, but those exact concepts are not governed by a clear
canonical vocabulary owner.

The risk is semantic drift during planning: generated dispatch or runway text
can invent, reinterpret, or invert deletion-test labels before evidence has
proved whether a surface should be deleted, migrated, narrowed, kept, or sent
to a human contract decision.

## Analysis

Existing guidance has adjacent but incomplete ownership:

- `dead-surface-audit` is an agent-facing evidence producer. It classifies
  test-retained surfaces and defines statuses such as `keep`, `delete-now`,
  `migrate-tests-first`, `keep-thin-entrypoint`, and
  `human-contract-decision`.
- `legacy-removal` consumes dead-surface evidence for exceptional obsolete
  surfaces, stale names, wrappers, aliases, and compatibility paths, but says
  `dead-surface-audit` answers evidence questions, not planning questions.
- `architecture-program-runway` and `batch-runway` consume findings, dispatch
  packets, and evidence while creating or executing batches, but they should
  not invent deletion categories or make evidence labels behave like approval
  gates.

Issue #31 therefore belongs in the codex-config skill-cleanup ledger as a
bounded vocabulary-ownership finding. It should be resolved before CCFG-11 is
replanned unless the future CCFG-11 dispatch explicitly avoids all ambiguous
deletion-test terminology.

## Proposed Plan

1. Define the canonical owner for deletion-test vocabulary used by generated
   dispatch/runway artifacts.
2. Decide whether the canonical definitions live in `dead-surface-audit`, a
   separate reference under an owner skill, or another explicitly named support
   contract.
3. Clarify consumer boundaries for `legacy-removal`,
   `architecture-program-runway`, and `batch-runway`: they may consume
   canonical evidence labels, but must not silently redefine deletion-test
   categories.
4. Require generated artifacts to use canonical deletion-test terms or mark
   local labels as non-canonical evidence labels with a local definition.
5. Add focused regression coverage so a CCFG-11-like dispatch/runway cannot
   invent unsupported deletion categories such as ambiguous `no-op` or
   `sediment` labels.

## Acceptance Criteria To Preserve

- Canonical definitions exist for deletion-test terms used by generated
  dispatch/runway artifacts.
- Generated runways either use canonical terms or explicitly define local terms
  as non-canonical evidence labels.
- `dead-surface-audit`, `legacy-removal`, `batch-runway`, and
  `architecture-program-runway` agree on who owns vocabulary versus who
  consumes evidence.
- A focused test prevents generated CCFG-like runways from inventing
  unsupported deletion categories.
- CCFG-11 can be replanned without ambiguous deletion-test terminology.

## CCFG-11 Relationship

CCFG-11 remains open skill-cleanup work. The displaced CCFG-11 dispatch/runway
is superseded planning evidence only and must not be executed directly.

Before CCFG-11 is replanned, this finding should either be completed or the
future selected dispatch should explicitly narrow CCFG-11 to evidence-only work
that avoids non-canonical deletion-test terminology.

## Non-Goals

- Do not only reword the displaced CCFG-11 `no-op` definition.
- Do not make `dead-surface-audit` the batch owner unless the owner contract
  explicitly says so.
- Do not execute deletion-test cleanup until terminology ownership is resolved
  or the current CCFG-11 runway is superseded by a safe, narrowed plan.
- Do not turn this into broad skill-system redesign or project-specific
  downstream guidance.
