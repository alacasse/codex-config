# Execute-Spec Mode

Enforce the spec. Do not create a new plan unless the spec is ambiguous, stale,
or missing required execution details.

## Coordinator Preflight

1. Read project instructions, local overlays, and the full spec.
2. Read the Batch Runway reference files named by the spec.
3. Check the worktree and identify dirty-file risks.
4. Identify:
   - active validation profile
   - pending ledger rows
   - stop conditions
   - commit strategy
   - whether this is `lean-runway` or `full-runway`
   - current compact convergence fields
   - active ledger rows versus completed slice archive
5. Confirm subagent tooling is available.
6. Prefer `runway_worker` for coding and `runway_reviewer` for review.
7. If required custom agents are unavailable because Codex has not reloaded
   configuration yet, stop and ask for a restart or new thread rather than
   falling back to main-agent implementation.

## Per-Slice Loop

1. Spawn a coding subagent with `agent_type="runway_worker"`.
2. In lean mode, pass the absolute spec path, repo cwd, slice number, slice
   anchor, allowed files, dirty-file constraints, slice-specific overrides, and
   a short contract capsule or the relevant Batch Runway reference path. Do not
   paste the full slice unless needed.
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
10. If focused validation fails, inspect the failure and delegate a follow-up fix
    to a coding subagent when the fix is within slice scope and does not require
    a human decision.
11. Re-run validation after in-scope fixes.
12. Stop only when the failure is ambiguous, out of scope, repeatedly
    unresolved, or indicates a dirty-file conflict.
13. Spawn a separate review subagent with `agent_type="runway_reviewer"`.
14. In lean mode, pass the absolute spec path, repo cwd, slice number, slice
    anchor, task-scoped diff context, review focus, any explicit test quality
    review setting, and a short contract capsule or relevant Batch Runway
    reference path. Do not paste the full slice unless needed.
15. If review finds issues, delegate follow-up fixes to a coding subagent unless
    the fix is only a ledger or commit-message adjustment.
16. Commit only the files intentionally changed for that slice once validation
    and review are clean.
17. Immediately report a YAML commit receipt using `Compact Report Contract v1`.
18. Include compact convergence in routine commit receipts. Use the expanded
    convergence template only when scope is expanding, significant uncertainty
    exists, blockers are present, or final batch reporting is being produced.
19. Update the active ledger with only the state needed for remaining work. Move
    completed slice audit references to the completed slice archive.
20. Close completed subagents before continuing to avoid thread-limit failures.
21. Continue directly to the next pending ledger row.

## Finalization

After the last completed slice:

1. Run the spec's final validation.
2. Run any project-required graph or index refresh after code changes.
3. Report completed commits, validation results, skipped slices, remaining risks,
   and expanded final `Convergence Assessment`.
4. If final validation uses a project-specific integration harness, read the
   required summary artifact before reporting the final harness result.
