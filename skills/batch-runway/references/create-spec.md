# Create-Spec Mode

Write one local plan file. Do not implement code.

Steps:

1. Read applicable project instructions and local overlays first.
2. Inspect the current goal, existing local plans, recent commits, current ledger
   state, and the last completed task enough to identify the next related work.
3. Pick 3-5 tightly related slices that can execute sequentially.
4. Keep each slice independently testable and committable.
5. Store the spec in the project's local planning location.
6. Prefer `lean-runway` unless the work touches high-risk production behavior or
   subagent file access is unreliable.

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
Use Batch Runway Execute Slice Core v1 for routine slice execution.

Reference files:
- `<absolute path to batch-runway>/references/execute-slice-core-v1.md`
- `<absolute path to batch-runway>/references/execution-contract-v1.md`
- `<absolute path to batch-runway>/references/reporting-contracts-v1.md`
- `<absolute path to batch-runway>/references/ledger-retention-v1.md`

Overrides:
- <only list deviations from the standard contract>
```

For lean specs, do not repeat full command blocks in every slice if a validation
profile covers them. Reference the selected profile file under
`references/validation-profiles/` and list only slice-specific commands or
overrides.

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

Coding subagent briefs must be role-scoped. State that the spawned
`runway_worker` is already the required coding subagent for that slice, must
implement only that slice, and must not spawn, delegate to, or wait on
additional subagents. Coordinator-owned validation, review, ledger, and commit
work should stay out of the worker role.

Only paste full acceptance criteria or full brief text when the subagent cannot
reliably read the spec path, the review boundary is subtle, or the slice is
unusually risky.
