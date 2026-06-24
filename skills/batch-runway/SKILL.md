---
name: batch-runway
description: Create and execute multi-slice runway specs with per-slice scope, validation, ledger updates, commits, and mandatory coding/review subagent delegation. Use when the user asks to create a batch runway spec, execute a runway spec, streamline sequential slices, work from project-local plans, commit after each slice, or keep the main agent as coordinator only while subagents implement and review.
---

# Batch Runway

Use this skill for a controlled sequence of small, independently committable slices.

Modes:

- `create-spec`: write a runway spec for a future execution session.
- `execute-spec`: execute an existing runway spec one slice at a time.

Spec density modes:

- `full-runway`: maximum explicitness. Specs may include full contracts, full commands, and full subagent briefs.
- `lean-runway`: token-efficient. Specs reference standard contracts, validation profiles, and compact subagent briefs.

Default to `lean-runway` for mechanical refactors, test topology splits, import cleanup, docs-local planning, compatibility facade cleanup, and behavior-preserving module moves.

Default to `full-runway` for production behavior changes, installer lifecycle changes, YAML schema changes, sandbox execution behavior, public CLI behavior, risky migrations, or ambiguous ownership boundaries.

If the user does not name a mode, infer it from the request. "Create", "spec", "plan", "next runway", or "upcoming work" means `create-spec`. "Execute", "run", "implement", "work through", or a specific spec path means `execute-spec`.

## Project Values Required

This skill is generic. Before creating or executing a spec, resolve the
project-specific values from repository instructions, local overlays, the active
spec, or explicit user direction.

Required values:

- `planning_location`: where local runway specs belong.
- `validation_profiles`: named validation profiles available in this repo.
- `focused_validation_commands`: how to run focused tests, linters, or checks.
- `integration_harness`: any project-specific sandbox, integration harness, or
  end-to-end validation command.
- `harness_output`: where generated validation artifacts should be written.
- `summary_artifact`: any command or file that must be read before reporting a
  harness result.
- `index_refresh`: any graph, search index, generated docs, or metadata refresh
  required after edits.
- `commit_requirements`: trailers, signing, branch rules, or commit-message
  conventions.
- `dirty_file_constraints`: files or directories that are expected dirty,
  generated, ignored, or forbidden to touch.

Stop instead of guessing when:

- no planning location is discoverable in `create-spec` mode
- a spec references a validation profile not defined by the spec, repository
  instructions, or local overlay
- a required harness command, output path, or summary artifact is named but not
  concretely specified
- focused validation targets cannot be identified safely from the slice scope
- project instructions conflict and the priority order is not clear

When stopping, report the missing project value and the exact source checked.

## Standard Execution Contract v1

Use this contract unless the spec explicitly overrides it. Treat named standard contracts as versioned and stable: do not reinterpret an existing spec's `Standard Execution Contract v1` reference using later contract semantics. If this contract needs incompatible changes, create `Standard Execution Contract v2` and keep v1 available for older specs.

- The main agent is coordinator only.
- The main agent must not implement code changes directly except for updating the ledger and making commits.
- Each slice implementation must be delegated to a coding subagent.
- Each completed slice must be reviewed by a separate review subagent before commit.
- Use `runway_worker` for coding subagents and `runway_reviewer` for review subagents when available.
- If subagent tooling is unavailable, stop and report that execution cannot proceed under this workflow.
- Do not fall back to main-agent implementation.
- Commit after each clean, focused slice.
- After each commit, report a commit receipt with:
  - commit hash and subject
  - files changed
  - validation result
  - sandbox result, when applicable
  - review result
  - exact inspection commands, usually `git show --stat <hash>` and `git show <hash>`
- Update the ledger after each slice with status, commit hash, focused validation, review result, review commands, and notes.
- After reporting a commit receipt, continue to the next pending slice unless the user explicitly asks to stop or a stop condition remains active.
- If execution is interrupted by an approval request, permission issue, transient infrastructure blocker, context transition, or user clarification, resume from the next incomplete ledger row as soon as the blocker is resolved.
- Do not stop after a successful slice commit merely because a commit receipt was reported.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Stop on scope drift, unresolved ambiguity, repeatedly unresolved validation failure, dirty-file conflict, missing subagent support, or a stop condition from the spec.

New specs should pair this execution contract with:

- `Compact Report Contract v1`
- `Compact Convergence Assessment v1`
- `Standard Ledger Retention v1`

## Standard Ledger v1

Use this legacy ledger shape only for specs that already reference it directly.
For new specs, use `Standard Ledger Retention v1`.

```md
## Execution Ledger

| Slice | Status | Commit | Focused validation | Review | Review commands | Notes |
|---|---|---|---|---|---|---|
| 1 | pending | | | | | |
| 2 | pending | | | | | |
| 3 | pending | | | | | |
```

## Standard Ledger Retention v1

Use this ledger strategy for new specs unless the spec explicitly overrides it.
Keep the active orchestration state small; preserve detailed audit data through
commits, validation artifacts, review artifacts, ADRs, or task files on disk.

Recommended shape:

```md
## Active Ledger

| Slice | Status | Commit | Validation | Review | Next proof | Notes |
|---|---|---|---|---|---|---|
| 1 | pending | | | | | |
| 2 | pending | | | | | |
| 3 | pending | | | | | |

## Completed Slice Archive

| Slice | Commit | Outcome | Audit references |
|---|---|---|---|
| 1 | `abc1234` | success | `git show --stat abc1234`; sandbox output `<path>` |
```

Rules:

- The active ledger keeps only facts needed to choose and execute remaining work.
- Completed rows move to the archive after commit.
- Completed archive rows should fit on one line where practical.
- Store commit hash, outcome, and audit references; do not store implementation chronology.
- Summarize validation as `pytest 75 passed; ruff passed; sandbox PASS` instead of pasting full commands repeatedly.
- Store detailed commands, transcripts, logs, and generated reports in commits or artifacts.
- Keep unresolved risks, blockers, compatibility paths, and next-proof requirements in the active ledger until resolved.
- Do not repeatedly paste completed slice details into future subagent prompts.

## Compact Convergence Assessment v1

Use compact convergence for routine slice reports, commit receipts, ledger
updates, and status reporting. Progress is not the same as convergence, but the
routine convergence signal should be small enough to carry forward across many
slices.

Routine output format:

```yaml
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Validate ownership resolution in sandbox"
```

Fields:

- `phase`: `discovery | convergence | closure`
- `scope_trend`: `shrinking | stable | expanding`
- `new_unknowns`: compact list of newly discovered unknowns, or `[]`
- `blockers`: compact list of blockers, or `[]`
- `next_proof`: the next concrete proof needed to increase confidence

Use the expanded convergence template only when:

- scope is expanding
- significant uncertainty exists
- blockers are present
- final batch reporting is being produced

Expanded output format:

```md
## Convergence Assessment

### Phase
`discovery | convergence | closure`

### Scope trend
`shrinking | stable | expanding`

### Closed this slice
- ...

### Newly discovered
- ...

### Deferred out of scope
- ...

### Remaining unknowns
- ...

### Temporary compatibility paths
- ...

### Blockers
- ...

### Completion forecastable
`yes | no`

### Forecast
- ...

### Evidence
- ...

### Next proof required
- ...
```

Definitions:

- `discovery`: the runway is still revealing new scope, hidden coupling, unclear behavior, missing test coverage, or architectural uncertainty. Do not forecast completion.
- `convergence`: the direction is stable, new discoveries are decreasing, uncertainty is localized, and slices are reducing the unknown space.
- `closure`: remaining work is explicitly bounded, mostly known, and expected to close known items rather than reveal major new ones.
- `shrinking`: the slice closed more uncertainty than it introduced.
- `stable`: the slice made progress, but open uncertainty stayed roughly the same.
- `expanding`: the slice discovered more unknowns, blockers, or required follow-ups than it closed.

Forecastability rules:

- Use `completion forecastable: no` if the runway is in `discovery`.
- Use `completion forecastable: no` if remaining work is not bounded.
- Use `completion forecastable: no` if new unknowns are appearing faster than they are being closed.
- Use `completion forecastable: yes` only when remaining work can be enumerated as bounded slices.
- Forecast remaining work in bounded slices, not calendar time.
- Do not say or imply that work is almost done unless remaining work is explicitly enumerated, no major new unknowns were introduced in the latest slice, temporary compatibility logic is removed or intentionally documented, follow-up work is separated from blocking work, and the next slice is expected to close known items rather than discover new ones.

## Compact Report Contract v1

Use this shared contract for `runway_worker`, `runway_reviewer`, and coordinator
commit receipts. Optimize reports for machine consumption, future recovery, and
long-term retention. Prefer YAML whenever possible.

Global rules:

- Return structured results only.
- Do not return implementation history.
- Do not narrate reasoning.
- Do not explain chronological work performed.
- Do not paste command transcripts or long logs.
- Clean worker reports should be 12 lines or fewer.
- Clean reviewer reports should be 10 lines or fewer.
- Expanded output is allowed only when findings exist, blockers exist, validation failed, or escalation is required.

Worker report:

```yaml
status: success
files_changed:
  - path/to/file.py
behavior_changed: false
validation:
  passed:
    - pytest: "75 passed"
risks: []
follow_up: []
notes_for_next_slice: []
```

Reviewer report:

```yaml
status: clean
findings: []
residual_risks: []
required_fixes: []
```

If a slice requests test quality review, include the compact YAML findings from
`$test-quality-review` in the reviewer report.

Commit receipt:

```yaml
slice: 2
commit: abc1234
subject: Extract module owner
status: committed
files_changed:
  - src/module_owner.py
validation: "pytest 75 passed; ruff passed; harness PASS 48 passed"
review: clean
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Move runtime entrypoint off compatibility facade imports"
inspect:
  - git show --stat abc1234
  - git show abc1234
```

## Information Lifetime Rules

Classify information before carrying it forward.

Permanent:

- commits
- durable architecture decisions
- unresolved risks
- ADR-worthy decisions
- compatibility paths that remain after the batch

Batch-scoped:

- remaining slices
- stop conditions
- active validation strategy
- active dirty-file constraints
- unresolved review or validation findings
- current convergence phase and next proof

Slice-scoped:

- implementation notes
- review findings
- validation details
- failure/recovery loops
- sandbox output paths for the current slice

Disposable after task completion:

- implementation chronology
- repeated clean-review prose
- command transcripts
- repetitive validation details
- repeated explanations of already-closed slices

## Test Quality Review Integration

A slice may explicitly request:

```md
Test quality review: none | delta-only | focused | full-audit
```

Default to `none` when the field is omitted. Existing behavior must remain
unchanged for specs that do not request test quality review.

If a slice requests `delta-only`, `focused`, or `full-audit`, invoke
`$test-quality-review` using the requested mode and include its compact YAML
findings in the review output.

Treat test-quality-review findings as review information only. Do not
automatically modify execution flow, create issues, update the ledger, block
execution, run full-audit orchestration, generate ADRs, or create remediation
plans unless the existing review rules or the spec already require that action.

## Validation Profiles

Specs should reference validation profiles instead of repeating long command blocks when practical. Slice-specific commands and overrides still belong in the spec when the profile is not precise enough.

### `docs-only`

Use for local plans, docs-only edits, and non-code artifacts.

Per-slice validation:

- `git diff --check`
- project-specific doc checks only when the touched docs require them

Do not run test suites, linters, integration harnesses, or index refresh
commands unless the spec or project instructions explicitly require them.

### `test-only-topology`

Use for moving, splitting, or reorganizing tests without production code changes.

Per-slice validation:

- focused pytest for touched test modules
- ruff on touched test modules
- `git diff --check`

Final validation:

- full relevant test subset
- broader pytest if the spec requires it
- project-specific integration harness only at final validation unless the slice
  changes harness execution behavior, direct-runner coverage, runtime
  import/path assumptions, or the spec requires earlier harness validation
- project-specific index refresh only if project instructions require it after
  test topology changes

### `mechanical-production-refactor`

Use for behavior-preserving production module moves, facade slimming, import cleanup, and ownership extraction.

Per-slice validation:

- focused pytest covering touched behavior
- ruff on touched production and test files
- `git diff --check`
- project-specific index refresh when project instructions require it

Integration harness policy:

- Run the project-specific integration harness per slice if the touched code can
  affect harness execution.
- Treat module moves, runtime import cleanup, compatibility facade changes,
  report or summary generation changes, runtime path handling, artifact-shape
  handling, and changes to code imported by the harness entrypoints as
  harness-affecting even when the intended behavior is preserving.
- Otherwise run the project-specific integration harness at final validation
  when the project or spec requires it.

### `project-harness-production`

Use for production behavior that directly affects a project-specific integration
harness, lifecycle, target selection, harness policy, schema normalization,
report/summary output, public CLI behavior, or generated harness artifacts.

Per-slice validation:

- focused pytest
- ruff
- project-specific integration harness command with an explicit fresh output
  path when the harness writes artifacts
- project-specific summary artifact command or summary file read, when required
- project-specific index refresh, when required
- `git diff --check`

Final validation:

- full relevant harness test subset
- broader project tests when practical
- project-specific integration harness with an explicit fresh output path when
  the harness writes artifacts
- read the project-specific summary artifact before reporting the final harness
  result, when required

## Create-Spec Mode

Write one local plan file. Do not implement code.

1. Read applicable project instructions and local overlays first.
2. Inspect the current goal, existing local plans, recent commits, current ledger state, and the last completed task enough to identify the next related work.
3. Pick 3-5 tightly related slices that can execute sequentially.
4. Keep each slice independently testable and committable.
5. Store the spec in the project's local planning location.
6. Prefer `lean-runway` unless the work touches high-risk production behavior.

The spec must include:

- title and purpose
- current baseline and assumptions
- non-goals for the whole batch
- execution contract reference
- compact report contract reference
- compact convergence assessment reference
- ledger retention strategy reference
- validation profile
- execution ledger
- 3-5 slice sections
- final validation
- stop conditions

For lean specs, do not paste the full standard execution contract. Reference it:

```md
## Execution Contract

Use Batch Runway Standard Execution Contract v1.
Use Batch Runway Compact Report Contract v1.
Use Batch Runway Compact Convergence Assessment v1 for routine status reports, slice summaries, commit receipts, and ledger notes.
Use the expanded convergence template only when scope is expanding, significant uncertainty exists, blockers are present, or final batch reporting is being produced.
Use Batch Runway Standard Ledger Retention v1.

Overrides:
- <only list deviations from the standard contract>
```

For lean specs, do not repeat full command blocks in every slice if a validation profile covers them. Reference the profile and list only slice-specific commands or overrides.

Each slice must include:

- scope
- allowed files or file areas
- non-goals
- acceptance criteria
- validation profile or focused validation overrides
- test quality review setting, when explicitly requested
- commit message
- coding subagent brief reference or compact brief
- review subagent brief reference or compact brief
- stop conditions

### Lean Coding Brief Format

Use this compact brief when the subagent can read the spec file directly:

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Read the full slice and applicable execution contract in the spec.
Use Compact Report Contract v1.
Allowed files/areas: <repeat exact allowed files if needed for safety>.
Dirty-file constraints: preserve unrelated dirty files; do not touch generated output except allowed validation output.
Return YAML only. No implementation history, reasoning narrative, or chronological work log.
```

Only paste the full slice content into the subagent brief when the subagent cannot reliably read the spec path or when the slice is unusually risky.

### Lean Review Brief Format

Use this compact brief when the reviewer can read the spec file directly:

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
If the slice requests test quality review, invoke $test-quality-review in the requested mode and include compact YAML findings.
Use Compact Report Contract v1 reviewer format. Return YAML only. Do not modify files.
```

Only paste full acceptance criteria when the reviewer cannot reliably read the spec path or when the review boundary is subtle.

## Execute-Spec Mode

Enforce the spec. Do not create a new plan unless the spec is ambiguous, stale, or missing required execution details.

Coordinator preflight:

1. Read project instructions, local overlays, and the full spec.
2. Check the worktree and identify dirty-file risks.
3. Identify:
   - active validation profile
   - pending ledger rows
   - stop conditions
   - commit strategy
   - whether this is `lean-runway` or `full-runway`
   - current compact convergence fields
   - active ledger rows versus completed slice archive
4. Confirm subagent tooling is available.
5. Prefer `runway_worker` for coding and `runway_reviewer` for review.
6. If required custom agents are unavailable because Codex has not reloaded configuration yet, stop and ask for a restart or new thread rather than falling back to main-agent implementation.

For each slice:

1. Spawn a coding subagent with `agent_type="runway_worker"`.
2. In lean mode, pass the absolute spec path, repo cwd, slice number, slice anchor, allowed files, dirty-file constraints, and slice-specific overrides. Do not paste the full slice unless needed.
3. Require the coding result to follow `Compact Report Contract v1`.
4. Run or verify focused validation from the coordinator session when practical.
5. Apply the active validation profile.
6. If the slice is test-only and uses `test-only-topology`, do not run the project-specific integration harness per slice unless the slice changes harness execution behavior, direct-runner coverage, runtime import/path assumptions, or the spec requires it.
7. If the slice touches production code or behavior that the active project profile marks as harness-affecting, run the project-specific integration harness for that slice before review and before commit unless the validation profile explicitly defers it.
8. Treat module moves, runtime import cleanup, compatibility facade changes, report or summary generation changes, runtime path handling, artifact-shape handling, and changes to code imported by project harness entrypoints as harness-affecting when the active project profile says so.
9. Use an explicit fresh harness output path whenever the project-specific harness writes artifacts.
10. If focused validation fails, inspect the failure and delegate a follow-up fix to a coding subagent when the fix is within slice scope and does not require a human decision.
11. Re-run validation after in-scope fixes.
12. Stop only when the failure is ambiguous, out of scope, repeatedly unresolved, or indicates a dirty-file conflict.
13. Spawn a separate review subagent with `agent_type="runway_reviewer"`.
14. In lean mode, pass the absolute spec path, repo cwd, slice number, slice anchor, task-scoped diff context, review focus, and any explicit test quality review setting. Do not paste the full slice unless needed.
15. If review finds issues, delegate follow-up fixes to a coding subagent unless the fix is only a ledger or commit-message adjustment.
16. Commit only the files intentionally changed for that slice once validation and review are clean.
17. Immediately report a YAML commit receipt using `Compact Report Contract v1`.
18. Include compact convergence in routine commit receipts. Use the expanded convergence template only when scope is expanding, significant uncertainty exists, blockers are present, or final batch reporting is being produced.
19. Update the active ledger with only the state needed for remaining work. Move completed slice audit references to the completed slice archive.
20. Close completed subagents before continuing to avoid thread-limit failures.
21. Continue directly to the next pending ledger row.

After the last completed slice:

1. Run the spec's final validation.
2. Run any project-required graph or index refresh after code changes.
3. Report completed commits, validation results, skipped slices, remaining risks, and expanded final `Convergence Assessment`.
4. If final validation uses a project-specific integration harness, read the required summary artifact before reporting the final harness result.

## Hard Rules

- Do not let the main agent become the implementer in `execute-spec` mode.
- Stop if the next slice depends on unresolved failures from the prior slice.
- After a resolved interruption, approval, permission issue, context transition, or clarification, resume the same runway at the next incomplete ledger row.
- Do not stop after a successful slice commit merely because a commit receipt was reported.
- Try to resolve validation or review failures by delegating in-scope follow-up fixes before stopping.
- Stop on scope drift, ambiguity, repeatedly unresolved validation failure, dirty-file conflict, or missing subagent support.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Keep commits aligned to one slice and one ownership boundary.
- Prefer focused tests after each slice and broad validation once at the end.
- Use lean specs and lean subagent briefs when they preserve safety.
- Use full explicit specs when risk, ambiguity, or missing subagent file access makes compact references unsafe.
- Report convergence separately from progress; passing tests, clean review, and committed slices are not enough to claim closure.
- Use compact YAML reports for routine worker results, reviewer results, commit receipts, and ledger updates.
- Do not retain implementation chronology, command transcripts, repeated clean-review prose, or repetitive validation detail in live orchestration context.
- Do not mark a runway as `closure` while major unknowns remain.
- Do not mark completion forecastable while scope is still expanding.
- Do not say or imply that work is almost done unless remaining work is bounded, known, explicitly enumerated, and supported by the latest convergence evidence.

## Subagent Brief Rules

Coding subagent briefs should include only the context needed for that slice.

Prefer compact briefs:

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Read the full slice and applicable execution contract in the spec.
Allowed files/areas: ...
Dirty-file constraints: ...
Use Compact Report Contract v1 worker format.
Return YAML only. No implementation history, reasoning narrative, or chronological work log.
```

Use full briefs only when:

- the subagent may not be able to read the spec file
- the slice has subtle non-goals
- the slice has unusual stop conditions
- the work touches high-risk production behavior
- previous attempts showed the compact brief was insufficient

Review subagent briefs should be independent but compact:

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Inspect only the task-scoped diff and relevant files.
Check: scope, acceptance criteria, validation evidence, behavior changes, dirty-file leakage.
If the slice requests test quality review, invoke $test-quality-review in the requested mode and include compact YAML findings.
Use Compact Report Contract v1 reviewer format. Return YAML only. Do not modify files.
```

## Support-Only Custom Agents

- Use `fast_explorer` only for read-only side investigations that do not replace required coding or review subagents.
- Use `spark` only for lightweight, low-risk iteration.
- Do not use `spark` for required Batch Runway review, security review, broad refactors, or ambiguous validation failure recovery.
