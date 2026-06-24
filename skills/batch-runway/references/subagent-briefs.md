# Subagent Brief Rules

Coding and review briefs should include only the context needed for the current
slice. Prefer absolute paths and stable anchors over pasted spec content.

## Lean Coding Brief

Use this compact brief when the subagent can read the spec file directly:

```text
Use agent_type="runway_worker".

Implement slice <N> from <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Read the full slice and applicable execution contract in the spec.
Batch Runway reference, if needed: <absolute path to relevant reference file>.
Use Compact Report Contract v1.
Allowed files/areas: <repeat exact allowed files if needed for safety>.
Dirty-file constraints: preserve unrelated dirty files; do not touch generated output except allowed validation output.
Return YAML only. No implementation history, reasoning narrative, or chronological work log.
```

Only paste the full slice content into the subagent brief when the subagent
cannot reliably read the spec path, the slice has subtle non-goals, the slice has
unusual stop conditions, the work touches high-risk production behavior, or
previous compact attempts were insufficient.

## Lean Review Brief

Use this compact brief when the reviewer can read the spec file directly:

```text
Use agent_type="runway_reviewer".

Review slice <N> against <absolute spec path>.
Repo cwd: <absolute repository path>.
Slice anchor: <heading text or line number>.
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
If the slice requests test quality review, invoke $test-quality-review in the requested mode and include compact YAML findings.
Batch Runway reference, if needed: <absolute path to relevant reference file>.
Use Compact Report Contract v1 reviewer format. Return YAML only. Do not modify files.
```

Only paste full acceptance criteria when the reviewer cannot reliably read the
spec path or when the review boundary is subtle.

## Support-Only Custom Agents

- Use `fast_explorer` only for read-only side investigations that do not replace
  required coding or review subagents.
- Use `fast_explorer` when broad source, test, memory, prior-spec, or
  architecture exploration would otherwise enter coordinator context.
- Prefer one batch-scoped `fast_explorer` investigation for related adjacent
  slices. Use multiple explorers only for independent questions where parallel
  speedup is worth duplicated read context.
- The coordinator owns support-agent lifecycle. Do not pass live support-agent
  handles to workers or reviewers; pass only compact findings, selected
  per-slice notes, or artifact paths.
- Require compact YAML with `status`, `question_answered`, `files_checked`,
  `findings`, optional `per_slice_notes`, `risks`, and `suggested_next_read`.
- Do not allow raw logs, long excerpts, implementation plans, or chronological
  work logs in support-agent output.
- Use `spark` only for lightweight, low-risk iteration.
- Do not use `spark` for required Batch Runway review, security review, broad
  refactors, or ambiguous validation failure recovery.
