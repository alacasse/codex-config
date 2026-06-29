# Execute-Spec Mode

Enforce the spec. Do not create a new plan unless the spec is ambiguous, stale,
or missing required execution details.

For routine slice execution, prefer `execute-slice-core-v1.md` plus the selected
profile file under `validation-profiles/`. Use this file as the routing surface
for compatibility questions, non-routine execution, recovery, and finalization.

## Coordinator Preflight

1. Read project instructions, local overlays, and the full spec.
2. For routine slices, read `execute-slice-core-v1.md` and only the selected
   validation profile file.
3. Read the full Batch Runway reference files named by the spec only when the
   spec is full-runway, the slice is non-routine, compatibility needs auditing,
   or canonical contract semantics are being changed.
4. Check the worktree and identify dirty-file risks.
5. Identify:
   - active validation profile
   - pending ledger rows
   - stop conditions
   - commit strategy
   - whether this is `lean-runway` or `full-runway`
   - current compact convergence fields
   - active ledger rows versus completed slice archive
6. Confirm subagent tooling is available.
7. Prefer `runway_worker` for coding and `runway_reviewer` for review.
8. Use `fast_explorer` for optional read-only side investigations when broad
   source, test, memory, prior-spec, or architecture exploration would otherwise
   enter coordinator context. Prefer one batch-scoped investigation for related
   adjacent slices, then pass only compact findings, selected per-slice notes, or
   artifact paths to workers and reviewers.
9. Identify or create the spec's compact `orchestration_anomalies` location for
   suspicious coordinator or subagent-lifecycle behavior. Do not use it for
   routine command output, normal validation logs, clean reviews, or
   implementation chronology.
   Include unexpected `HEAD` or diff movement and stale review evidence here
   when they affect execution confidence.
10. If required custom agents are unavailable because Codex has not reloaded
   configuration yet, stop and ask for a restart or new thread rather than
   falling back to main-agent implementation.

## Per-Slice Loop

Use `execute-slice-core-v1.md` for the normal version of this loop.

1. Spawn a coding subagent with `agent_type="runway_worker"`.
2. In lean mode, pass the absolute spec path, repo cwd, slice number, slice
   anchor, allowed files, dirty-file constraints, slice-specific overrides, and
   a role-scoped contract capsule or the relevant Batch Runway reference path.
   The capsule must say the spawned worker is already the required coding
   subagent, must implement only its assigned slice, and must not spawn,
   delegate to, or wait on additional subagents. Do not paste the full slice
   unless needed.
3. Require the coding result to follow `Compact Report Contract v1`.
4. Run or verify focused validation from the coordinator session when practical.
5. Apply the active validation profile.
6. If the slice is test-only and uses `test-only-topology`, do not run the
   project-specific integration harness per slice unless the slice changes
   harness execution behavior, direct-runner coverage, runtime import/path
   assumptions, or the spec requires it.
7. If the slice touches production code or behavior that the active project
   profile marks as harness-affecting, run the project-specific integration
   harness for that slice before review and before commit unless the validation
   profile explicitly defers it.
8. Treat module moves, runtime import cleanup, compatibility facade changes,
   report or summary generation changes, runtime path handling, artifact-shape
   handling, and changes to code imported by project harness entrypoints as
   harness-affecting when the active project profile says so.
9. Use an explicit fresh harness output path whenever the project-specific
   harness writes artifacts.
10. Before doing broad coordinator exploration, delegate read-only discovery to
    one batch-scoped `fast_explorer` and retain only compact findings, unless
    this is recovery, blocker analysis, finalization, stale-spec analysis,
    subagent-report verification, or uncertainty that prevents safe delegation.
    Use multiple explorers only for independent questions where parallel speedup
    is worth duplicated read context. Do not pass live support-agent handles to
    workers or reviewers.
11. If focused validation fails, read `execute-recovery-v1.md`.
12. Re-run validation after in-scope fixes.
13. Stop only when the failure is ambiguous, out of scope, repeatedly
    unresolved, or indicates a dirty-file conflict.
14. Spawn a separate review subagent with `agent_type="runway_reviewer"`.
15. In lean mode, pass the absolute spec path, repo cwd, slice number, slice
    anchor, exact diff basis, task-scoped diff context, review focus, any
    explicit test quality review setting, and a short contract capsule or
    relevant Batch Runway reference path. Require reviewer YAML to include the
    inspected `diff_basis`. Do not paste the full slice unless needed.
16. If review finds issues, read `execute-recovery-v1.md`.
17. Commit only the files intentionally changed for that slice once validation
    and review are clean.
18. Record any orchestration anomalies using `Orchestration Anomaly Log v1`.
19. Immediately report a YAML commit receipt using `Compact Report Contract v1`.
20. Include compact convergence in routine commit receipts. Use the expanded
    convergence template only when scope is expanding, significant uncertainty
    exists, blockers are present, or final batch reporting is being produced.
21. Update the active ledger with only the state needed for remaining work. Move
    completed slice audit references to the completed slice archive.
22. Close completed subagents before continuing to avoid thread-limit failures.
23. Continue directly to the next pending ledger row.

## Finalization

Read `finalize-batch-v1.md` before closing the batch.

After the last completed slice:

1. Run the spec's final validation.
2. Run any project-required graph or index refresh after code changes.
3. Report completed commits, validation results, skipped slices, remaining risks,
   `orchestration_anomalies`, and expanded final `Convergence Assessment`.
4. If final validation uses a project-specific integration harness, read the
   required summary artifact before reporting the final harness result.
