# Execute-Spec Mode

Enforce the spec. Do not create a new plan unless the spec is ambiguous, stale,
or missing required execution details.

For routine slice execution, prefer `execute-slice-core-v1.md` plus the selected
profile file under `validation-profiles/`. Use this file as the routing surface
for compatibility questions, non-routine execution, recovery, and finalization.

## Coordinator Preflight

1. Read project instructions, local overlays, and the full spec.
2. If the spec is Layout v1 or otherwise ledger-driven, read
   `../../planning-state/SKILL.md` and invoke its Diagnostic-First Pickup
   Interface. Carry forward only compact Planning State Diagnostic facts:
   planning root, current and validate status, active programs, selected
   dispatch, queued batch, active runway, blockers, warnings, and project
   policy.
3. Consume active-state files, selected dispatches, queued specs, active
   runways, blockers, and target policy only after that diagnostic handoff.
   Batch Runway still owns execution orchestration, pending-row selection,
   validation profile handling, subagent routing, concrete execution-ledger
   updates, completed-slice archives, and commits.
   When execution needs pending-batch inventory, missing closeout evidence,
   batch evidence, runner summaries, or bounded backlog/history reports beyond
   the active diagnostic, read
   `../../planning-state/references/projection-reporting.md` and use
   policy-compatible `report-projection` command output as the normal route
   before broad historical scans. Missing or incompatible `projection_usage` or
   `projection_rebuild_authority` is a bounded blocker or explicit fallback
   decision before scanning, not permission for silent Markdown archaeology or
   direct SQLite reads.
4. For routine slices, read `execute-slice-core-v1.md` and only the selected
   validation profile file.
5. Read the full Batch Runway reference files named by the spec only when the
   spec is full-runway, the slice is non-routine, compatibility needs auditing,
   or canonical contract semantics are being changed.
6. Check the worktree and identify dirty-file risks.
7. Identify:
   - active validation profile
   - pending ledger rows
   - stop conditions
   - commit strategy
   - whether this is `lean-runway` or `full-runway`
   - current compact convergence fields
   - active ledger rows versus completed slice archive
8. Confirm subagent tooling is available.
9. Prefer `runway_worker` for coding and `runway_reviewer` for review.
10. Classify likely review triggers from the spec and current diff. Always keep
   `runway_reviewer` as the final review gate. Invoke specialist support
   reviewers only when triggered by task-scoped changes, using
   `subagent-briefs.md` for routing.
11. Use the registered `codebase_investigator` for optional read-only support
   investigations when broad source, test, memory, prior-spec, or architecture
   reading would otherwise enter coordinator context. Prefer one batch-scoped
   investigation for related adjacent slices, then pass only compact findings,
   selected per-slice notes, or artifact paths to workers and reviewers.
12. Identify or create the spec's compact `orchestration_anomalies` location for
   suspicious coordinator or subagent-lifecycle behavior. Do not use it for
   routine command output, normal validation logs, clean reviews, or
   implementation chronology.
   Include unexpected `HEAD` or diff movement and stale review evidence here
   when they affect execution confidence.
13. If required custom agents are unavailable because Codex has not reloaded
   configuration yet, stop and ask for a restart or new thread rather than
   falling back to main-agent implementation.

## Routine Slice Routing

For routine slice execution, use `execute-slice-core-v1.md` and the selected
validation profile file. That core owns the normal worker handoff, focused
validation, selected-profile validation, triggered specialist-review check,
final reviewer handoff, commit receipt, concrete ledger/archive update,
orchestration anomaly logging, subagent closure, and continuation to the next
pending ledger row.

Keep using this file only to decide whether the slice is still routine. Read the
deeper owner references when the active spec is full-runway, the slice is
non-routine, compatibility needs auditing, or canonical contract semantics are
being changed.

## Non-Routine Triggers

Read `execute-recovery-v1.md` when validation fails, review finds issues,
blockers appear, workspace state or review evidence stops matching the expected
diff, escalation is required, or execution otherwise leaves the normal path.

Use `subagent-briefs.md` for triggered specialist-review routing, full brief
variants, support-agent guidance, or non-routine subagent prompting. Contract,
validation, and security concerns are non-registered review lenses handled by
the final `runway_reviewer`, not spawnable specialist reviewers.

Apply the selected validation profile for routine validation. Run project-level
harnesses or generated/index refreshes per slice only when the active profile,
spec, or changed surface requires them; use explicit fresh output paths when a
harness writes artifacts.

Use the expanded convergence template only when scope is expanding, significant
uncertainty exists, blockers are present, or final batch reporting is being
produced.

## Finalization

Read `finalize-batch-v1.md` before closing the batch.

After the last completed slice:

1. Run the spec's final validation.
2. Run any project-required graph or index refresh after code changes.
3. Report completed commits, validation results, skipped slices, remaining risks,
   cleanup residues classified as removed, kept with reason, or deferred with a
   removal condition, `orchestration_anomalies`, and expanded final
   `Convergence Assessment`.
4. If final validation uses a project-specific integration harness, read the
   required summary artifact before reporting the final harness result.
