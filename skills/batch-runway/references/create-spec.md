# Create-Spec Mode

Write one local plan file. Do not implement code.

Steps:

1. Read applicable project instructions and local overlays first.
2. If the project uses Planning Artifact Layout v1 or another ledger-driven
   planning root, read `../../planning-state/SKILL.md`, run its current and
   validate hot path, and carry forward compact Planning State Diagnostic facts:
   planning root, current and validate status, active programs, selected
   dispatch, queued batch, active runway, blockers, warnings, and project
   policy.
3. For Planning Artifact Layout v1, read the root `CURRENT.md` and the relevant
   program `CURRENT.md` files named by the diagnostic before scanning
   historical local plans, old dispatch/runway filenames, generated reports,
   recent commits, or source modules.
4. If a selected dispatch, active runway, or queued batch already exists in the
   diagnostic or active-state files, do not
   select a second batch. Report or use that path according to the request.
5. If no batch is selected, inspect only the relevant program ledger and the
   source packet or finding note named by the selected ledger row before
   broadening context.
   For pending-batch inventory, missing closeout evidence, bounded
   backlog/history reports, or other supported history/reporting questions,
   read `../../planning-state/references/projection-reporting.md` and use
   policy-compatible `report-projection` command output before broad historical
   scans. If `projection_usage` or `projection_rebuild_authority` is missing or
   incompatible, stop with that blocker or record an explicit fallback decision;
   do not silently scrape historical planning files.
6. Pick 3-5 tightly related slices that can execute sequentially.
7. Keep each slice independently testable and committable.
8. Store the spec in the project's local planning location.
9. Prefer `lean-runway` unless the work touches high-risk production behavior or
   subagent file access is unreliable.

After the Planning State Diagnostic handoff, Batch Runway still makes the
semantic planning decision: whether to create a spec, report an existing queued
or active spec, choose 3-5 slices, select validation, and define subagent briefs.
Do not move those decisions into `planning-state`.

When the project uses Planning Artifact Layout v1, store the concrete spec at:

```text
<program-root>/batches/<batch-id>-<batch-slug>/runway.md
```

Keep the selected dispatch packet, runway spec, closeout report, and
completed-slice archive co-located in that batch directory. Do not create a
loose runway spec directly under generic `plans/` or `planning/` unless a
project instruction, local overlay, or active compatibility exception explicitly
allows it.

When adjacent slices create and then consume a new seam, owner module, projection
API, compatibility facade, or other shared boundary, make that handoff explicit
in the spec. Name the single owner/API in the producing slice, require later
slices to consume that same owner/API, and add acceptance criteria or stop
conditions that fail the plan if a downstream slice bypasses, duplicates, or
reimplements the boundary.

The spec must include:

- title and purpose
- current baseline and assumptions
- non-goals for the whole batch
- execution contract reference
- compact report contract reference
- compact convergence assessment reference
- orchestration anomaly log reference
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
Use Batch Runway Orchestration Anomaly Log v1 for compact telemetry about suspicious coordinator or subagent-lifecycle behavior.
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
overrides. For test-only or docs-only slices, explicitly state that project-level
integration harnesses, index/search/graph refreshes, generated-doc refreshes,
package installs, and final validation are not part of per-slice worker work
unless the slice deliberately assigns them.

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

Review subagent briefs should require the execution coordinator to provide the
exact commit hash or task-scoped worktree diff basis being reviewed, and the
reviewer should echo that `diff_basis` in compact YAML output.

Only paste full acceptance criteria or full brief text when the subagent cannot
reliably read the spec path, the review boundary is subtle, or the slice is
unusually risky.
