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
You are already the required coding subagent for this slice. Do not spawn,
delegate to, or wait on additional subagents. Implement only this slice.
The coordinator handles validation, review delegation, concrete execution-ledger
updates, completed-slice archives, and commits.
Do not run project-level integration harnesses, index/search/graph refreshes,
generated-doc refreshes, final validation, or cleanup commands unless this handoff
explicitly assigns them.
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
Diff basis: <commit hash or task-scoped worktree diff paths>.
Inspect only the task-scoped diff and relevant files.
Check scope, acceptance criteria, validation evidence, dirty-file leakage, and behavior preservation.
Flag new or remaining cleanup residue that lacks a concrete reason, removal condition, or follow-up owner.
Classify review lenses before the verdict and include `lenses_applied`.
Include compact specialist-review findings already gathered by the coordinator.
Batch Runway reference, if needed: <absolute path to relevant reference file>.
Use Compact Report Contract v1 reviewer format. Return YAML only, including `diff_basis`. Do not modify files.
```

Only paste full acceptance criteria when the reviewer cannot reliably read the
spec path or when the review boundary is subtle.

## Trigger-Based Review Routing

The coordinator owns review routing. Specialist reviewers are support reviewers:
they inspect one triggered risk lens, return compact YAML, and do not replace the
final `runway_reviewer` verdict. Reviewers must not spawn, delegate to, or wait
on other reviewers.

Registered specialist reviewers may be invoked by the coordinator when
triggered. Non-registered review lenses are handled by the final
`runway_reviewer` and must not be treated as spawnable agent names.

Always run the final `runway_reviewer`. Invoke specialist support only when the
task-scoped diff triggers it:

```yaml
review_routing:
  always:
    - runway_reviewer

  triggers:
    tests_changed:
      - test-quality-review

    local_import_topology_changed:
      - import_topology_reviewer

    legacy_or_compatibility_cleanup:
      - dead-surface-audit
```

Use `import_topology_reviewer` when the diff changes project-local imports,
module entry behavior, path manipulation, direct-script fallback handling, or
tests that preserve import topology. It should distinguish project-local import
fallback from legitimate optional third-party dependency imports. A local import
topology change alone should not trigger broader legacy-management review.

Use `dead-surface-audit` only when legacy, compatibility, cleanup-candidate,
cleanup-residue, historical-evidence marker, test-retention,
absence/importability/topology-test, alias, wrapper, facade, or
migration-retention evidence suggests a surface may be kept alive by tests or
compatibility logic.

Deleting unsupported fallback paths is normally progress. Do not let cleanup
candidate inventories become permanent contracts: a reviewer may flag a cleanup
candidate that overlaps a supported entrypoint, but should not require a stable
list of unsupported candidates to remain forever.

Tests that only assert absence, import topology, alias identity, facade shape,
or wrapper retention are suspicious unless they protect a documented external
contract.

Unsupported legacy preservation is a default implementation and review defect.
Do not keep compatibility, aliases, wrappers, facades, migration scaffolding, or
old paths merely because they existed before or because tests assert their
shape. Keep them only with a named external contract, explicit user instruction,
or temporary removal condition.

Cleanup residues such as test-only compatibility markers, historical-evidence
buckets, migration guards, old-vocabulary taxonomy, aliases, facades, or
temporary scaffolding must be removed, kept with a named reason, or deferred
with a removal condition. Reviewers should treat unclassified residue as a
finding, not as harmless historical context.

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
