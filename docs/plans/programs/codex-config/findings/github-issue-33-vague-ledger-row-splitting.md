# GitHub Issue 33: Vague Ledger Row Splitting

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/33
- Title: CCFG root cause 5: split vague deletion-test ledger rows before 3-5
  slice expansion
- State when ingested: open
- Created: 2026-07-09
- Source identity: GitHub issue #33, authored by `alacasse`

## Summary

CCFG-11 exposed that an imprecise ledger row can expand into a mixed-scope
Batch Runway plan. The original row asked for deletion-test evidence, but the
generated runway included inventory, vocabulary/classification, test creation,
one cleanup decision, and closeout.

The root issue is not only CCFG-11 wording. `plan-batch` and
`architecture-program-runway` need a durable guard that blocks or narrows vague
rows before they become 3-5 slice implementation runways.

## Analysis

This issue builds on CCFG-13 and CCFG-14:

- CCFG-13 added validation-command status classification.
- CCFG-14 added batch-kind, slice-risk, and approval-gate requirements.
- GitHub issue #33 applies those concepts earlier, at ledger-row selection and
  dispatch shaping time.

The unsafe shape is a row that mixes evidence gathering, classification,
decision-making, destructive cleanup, migration, demotion, or contract
narrowing without enough source precision to decide whether one bounded runway
is safe.

When that shape appears, the planning workflow should not silently produce a
normal implementation batch. It should split, block, or narrow the work before
`batch-runway create-spec` receives a selected dispatch.

## Proposed Plan

1. Add reusable `plan-batch` / `architecture-program-runway` guidance for vague
   or mixed-risk ledger rows.
2. Require split/block/narrow rationale before creating a selected dispatch
   from a vague row.
3. Prefer characterization-only or evidence-only dispatches when source rows
   mention deletion, demotion, migration, or cleanup but lack precise owner,
   risk, and acceptance boundaries.
4. Require destructive cleanup, migration, demotion, or contract-narrowing
   discoveries during planning to become explicit follow-up findings unless the
   source row already authorized that risk.
5. Add focused contract tests or fixture examples proving that a CCFG-11-like
   row cannot expand directly into mixed evidence, decision, and destructive
   cleanup slices.

## Acceptance Criteria To Preserve

- Planning guidance identifies ledger rows that are too imprecise for direct
  3-5 slice expansion.
- Mixed evidence/decision/destructive cleanup rows are split, blocked, or
  narrowed before runway creation.
- Generated selected dispatches record split or narrow-scope rationale when
  the source row was vague.
- Contract tests or fixture examples cover CCFG-11-like vague-row handling.
- Planning state stays coherent: no execution starts from semantically unsafe
  queued runways.

## CCFG-11 Relationship

CCFG-11 remains open skill-cleanup work. The displaced CCFG-11 runway is
superseded planning evidence only and must not be executed directly.

After this issue is handled, CCFG-11 should be replanned as a narrower
evidence-only batch or explicitly split into separate findings before any
cleanup, deletion, migration, demotion, or contract-narrowing work.

## Non-Goals

- Do not merely rewrite the existing CCFG-11 runway to look narrower.
- Do not close CCFG-11 because planning artifacts exist.
- Do not execute the displaced CCFG-11 runway.
- Do not turn vague-row handling into codex-config-only project guidance; the
  reusable workflow skills should own the generic planning rule.

