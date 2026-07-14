# CCFG-30 Cross-Flight Execution Leases Dispatch

## Batch Identity

- Batch ID: `ccfg-30-cross-flight-execution-leases`
- Source program ledger:
  `docs/plans/programs/codex-config/LEDGER.md`
- Included finding: CCFG-30, Separate Planning Snapshots from Live Execution
  Leases
- Source note:
  `docs/plans/programs/codex-config/notes/cross-flight-execution-baseline-plan.md`
- Dispatch state: queued through the co-located concrete runway
- Expected runway:
  `docs/plans/programs/codex-config/batches/ccfg-30-cross-flight-execution-leases/runway.md`

## Selection Decision

Select CCFG-30 now because the user requested that existing ledger row, CCFG-20
is closed, and the source note defines one bounded cross-flight execution
lifecycle change. The vague-row guard passes: the note names the semantic owner
(`work-batch`), mechanical owner (`scripts/cross_checkout_context.py`), exact
startup classifications, implementation surfaces, ten regression scenarios,
acceptance criteria, non-goals, and fail-closed stop conditions.

CCFG-21 through CCFG-29 remain unselected because this request names CCFG-30
and must not accelerate command-owner transfer, candidate cutover, or final
integration. CCFG-2 through CCFG-6 and CCFG-9 through CCFG-11 remain open and
outside this batch.

## Gate Evidence

```yaml
planning_state:
  root: /home/alacasse/projects/codex-config/docs/plans
  current: passed
  validate: passed
  selected_dispatch: null
  queued_runway: null
  active_runway: null
  blockers: []
  warnings:
    - two known redirect-ledger warnings
stable_control:
  repository_root: /home/alacasse/projects/codex-config
  branch: master
  planning_baseline: 7220a2e78a7ad50550cd7bc7ffcfd328301d8e7f
  worktree_before_planning: clean
  codex_home: /home/alacasse/.codex
  helper_owner: codex-config batch-runway 1.5.1
  helper_link_status: linked
  install_status: passed
  install_dry_run: passed
candidate_generation:
  repository_root: /home/alacasse/projects/codex-config-command-owner-redesign
  branch: implementation/command-owner-redesign
  commit: 3e54155964e92d3a4dced8268cc683baaab9be1c
  role_in_this_batch: read-only deferred evidence
focused_baseline:
  cross_checkout_context: 21_passed_31_subtests
  batch_lifecycle_guards: 5_passed
  focused_cross_checkout_manifest: 3_passed_18_deselected_137_subtests
  static_checks: passed
  full_manifest: known_red_3_failed_18_passed_202_subtests
```

## Batch Kind And Risk

- Batch kind: `migration`.
- Slices 1 through 4 risk: `migration`.
- The batch migrates the temporary bridge from one persisted strict payload to
  distinct planning-snapshot, startup-reconciliation, live-lease, and receipt
  semantics while preserving exact handoff validation.
- Contract narrowing: forbidden.
- Destructive cleanup: forbidden.
- Approval gates: none, because no destructive or contract-narrowing slice is
  authorized.
- Runway density: `full-runway` because the work changes installed workflow
  behavior, cross-repository lifecycle semantics, and a fail-closed helper.

## Goal

Make a queued plan commit and reviewed compatible between-flight commits normal
inputs to `work-batch` startup without weakening exact root, generation,
revision, Codex-home, or write-scope validation for worker and reviewer
handoffs.

The queued runway remains the sole selected scope. A live execution lease is
prepared only after the coordinator classifies intervening movement, and every
write-bearing or review handoff continues to use exact live revisions.

## Owner Seam And Execution Topology

- Human-facing lifecycle owner: `skills/work-batch/SKILL.md`.
- Mechanical refresh owner: `scripts/cross_checkout_context.py`, through
  `prepare_cross_checkout_context_refresh(...)`.
- Shared bridge contract:
  `skills/batch-runway/references/cross-checkout-context-v1.md`.
- Planning-snapshot producers: `skills/plan-batch/SKILL.md` and
  `skills/batch-runway/references/create-spec.md`.
- Execution routing consumers: `execute-spec.md`,
  `execute-slice-core-v1.md`, and `execute-recovery-v1.md`.
- Implementation repository: the stable control checkout
  `/home/alacasse/projects/codex-config`.
- Execution mode for this batch: ordinary single-root. This dispatch does not
  name `cross-checkout-context/v1` as its own execution mode and does not
  declare separate implementation roots. The strict interface is the subject
  of the change, not the mechanism used to implement this batch.
- The redesign candidate remains read-only. Candidate code or helpers must not
  control canonical state before CCFG-29 cutover.

## Included Source Scope

- CCFG-30 and its complete source note.
- The installed stable helper and current cross-checkout consumer contracts.
- Current linked feature metadata for `plan-batch`, `work-batch`, and
  `batch-runway`.
- Focused helper, lifecycle, and manifest contract tests named by the source
  note.
- Workflow-guide and changelog updates required to make the new flight boundary
  discoverable and auditable.

## Deferred And Excluded

- Any implementation from CCFG-21 through CCFG-29.
- Candidate checkout edits, installation, reload, generation switching,
  cutover, branch retirement, or cross-checkout bridge deletion.
- Weakening `parse_cross_checkout_context` to accept ancestry or stale
  revisions.
- Letting the helper classify compatibility, select work, authorize execution,
  or own closeout.
- Automatically accepting arbitrary between-flight commits.
- Rewriting queued runway revision fields to chase `HEAD`.
- Remediating the three unrelated known-red manifest wording assertions.
- Adding project-specific paths, commands, or policy to reusable skill logic.

## Suggested Slice Shape

1. Add helper-owned refresh preparation while preserving exact strict parsing.
2. Define planning-snapshot semantics and forbid self-referential refreshes.
3. Add startup classification, live-lease regeneration, and recovery routing.
4. Prove the integrated lifecycle, update feature versions and user docs, and
   verify linked installed state.

## Validation Class

- Profile:
  `skills/batch-runway/references/validation-profiles/project-harness-production.md`.
- Required-green current baselines: focused cross-checkout tests, lifecycle
  guards, the focused cross-checkout manifest subset, Ruff, basedpyright,
  installed-state status, and installer dry-run.
- Implementation-created proof: temporary-repository tests covering planning
  snapshot, queue commit, compatible advancement, refreshed lease, and
  post-lease fail-closed behavior.
- Known-red diagnostic: full `tests/test_codex_features_manifest.py` remains at
  the exact three-failure baseline unless separately owned remediation lands.
- Test-changing slices require `test-quality-review: delta-only`.

## Stop Conditions

- Stop if implementation would target the redesign candidate or make candidate
  code control canonical state.
- Stop if the helper acquires compatibility classification, selection,
  execution acceptance, or closeout authority.
- Stop if any delegation-time strict check is weakened from exact live identity.
- Stop if startup reconciliation can silently broaden or replace queued scope.
- Stop if controlled paths are hard-coded into reusable skills instead of
  being derived from active state, the queued runway, manifest ownership, and
  slice allowlists.
- Stop if an intervening range cannot be classified from concrete commits and
  changed paths.
- Stop if any slice touches the candidate checkout, CCFG-20 artifacts, or
  implementation owned by CCFG-21 through CCFG-29.
- Stop closeout before selecting, refreshing, dispatching, or preparing a
  successor batch.
