# Execute Slice Core v1

Use this reference for routine execution of one normal slice. It is a hot-path
projection of the canonical Batch Runway contracts, not an independent contract.

## Contents

- Source Map
- Routine Preconditions
- Coordinator Invariants
- Normal Slice Loop
- Worker Handoff
- Reviewer Handoff
- Support Investigation Handoff
- Commit Receipt
- Ledger Update
- Compact Convergence Fields
- Escalation Pointers

## Source Map

Coordinator invariants:

- `execution-contract-v1.md`

Reporting contracts:

- `reporting-contracts-v1.md`

Ledger rules:

- `ledger-retention-v1.md`

Worker/reviewer handoffs:

- `subagent-briefs.md`

Full contracts remain canonical. Make semantic changes in the canonical
references first, then update this projection to match.

## Routine Preconditions

Use this core only when the slice is routine:

- normal coding slice
- normal reviewer
- no active blocker
- no failed validation
- no reviewer-requested fix loop yet
- no explicit test-quality-review request
- no escalation
- no final batch closeout

If any condition is false, read `execute-recovery-v1.md`,
`test-quality-review.md`, or `finalize-batch-v1.md` as appropriate.

## Coordinator Invariants

- Keep the main agent coordinator-only.
- Do not implement code directly except ledger updates and commits.
- Delegate implementation to `runway_worker`.
- Delegate review to a separate `runway_reviewer`.
- Keep coordinator reads limited to orchestration state for routine slices.
- Delegate broad read-only investigation to `fast_explorer` and carry forward
  only its compact findings.
- Prefer one batch-scoped `fast_explorer` investigation for related adjacent
  slices; use multiple explorers only for independent questions where parallel
  speedup is worth duplicated read context.
- Do not pass live support-agent handles to workers or reviewers. The
  coordinator owns support-agent lifecycle and passes only compact findings,
  selected per-slice notes, or artifact paths.
- Preserve unrelated dirty files.
- Do not revert or commit files outside the slice scope.
- Commit after the slice is clean, validated, and reviewed.

## Normal Slice Loop

1. Read the active spec, current ledger, selected slice, dirty-file constraints,
   allowed files, stop conditions, commit strategy, and selected validation
   profile.
2. If broad source, test, memory, prior-spec, or architecture exploration would
   otherwise be needed in coordinator context, spawn one batch-scoped
   `fast_explorer` with the compact support handoff below. Reuse its compact
   findings across related adjacent slices.
3. Spawn `runway_worker` with the compact coding handoff below.
4. Require compact YAML from the worker.
5. Run or verify focused validation and selected-profile validation.
6. Spawn `runway_reviewer` with the compact review handoff below.
7. Require compact YAML from the reviewer.
8. Commit only the intended slice files once validation and review are clean.
9. Report the compact commit receipt.
10. Update the active ledger with only remaining-work state.
11. Move completed-slice audit references to the completed archive.
12. Close completed subagents.
13. Continue to the next pending slice unless a stop condition remains active or
    the user explicitly asks to stop.

## Worker Handoff

Clean worker reports should be 12 lines or fewer. Do not paste command
transcripts or long logs.

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Allowed files/areas: <slice allowed files>.
Dirty-file constraints: <constraints>.
Validation profile: <selected profile path or expanded profile>.
Read the full slice in the spec. Return YAML only.
No implementation history, reasoning narrative, or chronological work log.
```

Worker YAML:

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

## Reviewer Handoff

Clean reviewer reports should be 10 lines or fewer. Do not paste command
transcripts or long logs.

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
Return YAML only. Do not modify files.
```

Reviewer YAML:

```yaml
status: clean
findings: []
residual_risks: []
required_fixes: []
```

## Support Investigation Handoff

Use `fast_explorer` only for optional read-only exploration that would otherwise
inflate coordinator context. It does not replace required coding or review
subagents. Prefer one batch-scoped support investigation for related adjacent
slices.

```text
Use agent_type="fast_explorer".

Investigate this read-only question for the active batch or slice <N>: <question>.
Repo cwd: <absolute repository path>.
Spec path: <absolute spec path>.
Slice anchors: <heading text or line numbers>.
Do not edit files. Return YAML only.
No raw logs, long excerpts, implementation plan, chronological work log, or
live-agent handoff instructions.
```

Support YAML:

```yaml
status: success
question_answered: true
files_checked:
  - path/to/file.py
findings:
  - "Relevant behavior is owned by path/to/file.py:42"
per_slice_notes:
  1:
    - "Use this only if it affects orchestration or the worker handoff."
risks: []
suggested_next_read: []
```

## Commit Receipt

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

## Ledger Update

- Keep active ledger state limited to remaining-work facts.
- Summarize validation; do not paste logs or transcripts.
- Move completed rows to the completed slice archive after commit.
- Archive only commit hash, outcome, and audit references.
- Keep unresolved risks, blockers, compatibility paths, and next proof in the
  active ledger until resolved.

## Compact Convergence Fields

Use compact convergence for routine receipts and ledger notes:

```yaml
convergence:
  phase: convergence
  scope_trend: shrinking
  new_unknowns: []
  blockers: []
  next_proof: "Validate next boundary"
```

Allowed values:

- `phase`: `discovery | convergence | closure`
- `scope_trend`: `shrinking | stable | expanding`

## Escalation Pointers

- Validation failed: read `execute-recovery-v1.md`.
- Review found issues: read `execute-recovery-v1.md`.
- Blocker, ambiguity, dirty-file conflict, or approval issue: read
  `execute-recovery-v1.md`.
- Explicit test-quality-review request: read `test-quality-review.md`.
- Last slice completed or final report requested: read `finalize-batch-v1.md`.
