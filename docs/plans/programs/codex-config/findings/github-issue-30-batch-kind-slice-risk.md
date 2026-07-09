# GitHub Issue 30: Batch Kind And Destructive-Slice Risk Gates

## Source

- GitHub issue: https://github.com/alacasse/codex-config/issues/30
- Title: CCFG root cause 2: define batch kind and destructive-slice risk gates
- State when ingested: open
- Created: 2026-07-09
- Source identity: GitHub issue #30, authored by `alacasse`

## Summary

Generated dispatch and runway artifacts do not have a durable batch-kind field
or per-slice risk classification for deletion, narrowing, migration, or other
destructive cleanup work.

CCFG-11 exposed the gap. Its displaced runway is framed as deletion-test
evidence, but it also contains a later slice that may delete a proven no-op
surface, narrow an entrypoint, migrate a stale test, or record a keep decision.
The spec has local stop conditions for some high-risk outcomes, but the
reusable Batch Runway create-spec contract does not require a generated artifact
to declare whether the whole batch is characterization, decision, migration, or
destructive cleanup, nor does it require slice-level risk metadata before
execution.

## Local Evidence

Read-only planning-state diagnostics passed:

- `python scripts/planning_state.py current --root docs/plans`
- `python scripts/planning_state.py validate --root docs/plans`

Focused issue checks:

- `skills/batch-runway/references/create-spec.md` requires validation-command
  status classes, but its generated-spec checklist does not require batch kind
  or slice risk class metadata.
- `tests/test_batch_runway_create_spec_contract.py` covers validation-command
  status classes, reusable guidance loading, session-mode hygiene, and
  project-neutrality, but has no contract coverage for batch kind or
  destructive-slice gates.
- `skills/architecture-program-runway/SKILL.md` mentions grouping by risk,
  dependency, validation profile, and migration shape, but does not define a
  reusable taxonomy for evidence-only, decision, migration, destructive-cleanup,
  or mixed-risk batches.
- `docs/plans/programs/codex-config/batches/ccfg-11-skill-deletion-tests/runway.md`
  has evidence and test slices followed by one cleanup-decision slice. The
  artifact now has validation-command statuses from CCFG-13, but it still has
  no durable batch-kind declaration or per-slice destructive-risk gate.

## Recommended Ledger Finding

Add one new codex-config ledger finding for a Batch Runway create-spec contract
fix. Keep it separate from CCFG-11 and CCFG-13:

- CCFG-11 is the skill deletion-test work.
- CCFG-13 fixed validation-command status classification.
- This finding should prevent future generated runways from mixing
  characterization/evidence work with destructive cleanup or contract narrowing
  without explicit artifact metadata and approval gates.

Suggested finding title:

`CCFG-14. Batch kind and destructive-slice risk gates`

Suggested source:

`GitHub issue #30; docs/plans/programs/codex-config/findings/github-issue-30-batch-kind-slice-risk.md`

Suggested next action:

Add durable Batch Runway create-spec guidance and focused contract tests so
generated dispatch/runway artifacts declare batch kind and classify risky
slices before execution.

## Acceptance Criteria To Preserve

- Generated dispatch/runway artifacts declare a batch kind.
- Each slice declares a risk class when the work could delete, narrow, demote,
  migrate, or otherwise contract an existing surface.
- Evidence-only or characterization batches cannot include destructive cleanup
  slices unless the artifact is explicitly mixed-risk and approval-gated.
- Destructive or contract-narrowing slices require an explicit approval gate
  before execution.
- Contract tests reject destructive cleanup slices in evidence-only batches
  unless the required approval/risk metadata exists.

## Non-Goals

- Do not fix this by only removing or rewriting CCFG-11 Slice 3.
- Do not execute the displaced CCFG-11 runway while this root-cause boundary is
  unresolved.
- Do not turn the taxonomy into project-specific guidance; reusable Batch
  Runway contracts should define portable metadata and gate semantics.
