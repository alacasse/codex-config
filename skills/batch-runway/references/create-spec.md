# Create-Spec Mode

Write one local plan file. Do not implement code.

Steps:

1. Read applicable project instructions and local overlays first.
2. If the project uses Planning Artifact Layout v1 or another ledger-driven
   planning root, read `../../planning-state/SKILL.md` and invoke its
   Diagnostic-First Pickup Interface. Carry forward only compact Planning State
   Diagnostic facts: planning root, current and validate status, active
   programs, selected dispatch, queued batch, active runway, blockers, warnings,
   and project policy.
3. For Planning Artifact Layout v1, consume those diagnostic facts before
   reading the root `CURRENT.md`, relevant program `CURRENT.md`, historical
   planning files, generated reports, recent commits, or source modules.
4. If a selected dispatch, active runway, or queued batch already exists in the
   diagnostic or active-state files, do not
   select a second batch. Report or use that path according to the request.
5. If no batch is selected, inspect only the relevant program ledger and the
   source packet or finding note named by the selected ledger row before
   broadening context.
   For pending-batch inventory, missing closeout evidence, bounded
   backlog/history reports, or other supported history/reporting questions,
   read `../../planning-state/references/projection-reporting.md` and use
   policy-compatible `report-projection` command output as the normal route
   before broad historical scans. If `projection_usage` or
   `projection_rebuild_authority` is missing or incompatible, stop with that
   blocker or record an explicit fallback decision before scanning; do not
   query SQLite directly or silently scrape historical planning files.
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
- batch kind and slice risk contract
- current baseline and assumptions
- non-goals for the whole batch
- execution contract reference
- compact report contract reference
- compact convergence assessment reference
- orchestration anomaly log reference
- ledger retention strategy reference
- validation profile and focused validation commands with status classes
- execution ledger
- 3-5 slice sections
- final validation
- stop conditions

Every generated dispatch or runway artifact must declare exactly one batch
kind before execution:

- `characterization`: collects evidence or characterizes existing behavior
  without cleanup, deletion, narrowing, demotion, migration, or ownership
  changes.
- `decision`: evaluates keep, remove, migrate, or defer outcomes and records a
  decision without performing destructive cleanup in the same slice unless the
  artifact is explicitly `mixed-risk`.
- `migration`: moves, rewires, or changes ownership while preserving the
  supported public contract.
- `destructive-cleanup`: deletes, disables, demotes, or intentionally removes an
  existing surface.
- `mixed-risk`: combines evidence, decision, migration, contract-narrowing, or
  destructive cleanup work. Name the risky slices and their approval gates.

Every generated slice that can change an existing surface, ownership boundary,
or supported contract must declare one slice risk class:

- `none`: no deletion, narrowing, migration, demotion, or contract change.
- `evidence-only`: gathers evidence without changing supported surfaces.
- `decision-only`: records a keep, remove, migrate, or defer decision without
  performing the selected cleanup.
- `migration`: changes topology or ownership while preserving supported
  behavior.
- `contract-narrowing`: removes or narrows an exposed or depended-on surface,
  supported behavior, command, schema field, documented workflow, compatibility
  path, or other relied-on contract.
- `destructive-cleanup`: deletes, disables, demotes, or intentionally removes an
  existing surface.

Destructive or contract-narrowing slices require an explicit approval gate in
the generated artifact before execution. The gate must name who or what can
approve the work and what evidence must exist before the slice runs. A
`characterization` batch or an `evidence-only` slice must not include
destructive cleanup or contract narrowing. If a batch combines evidence-only or
decision-only work with destructive cleanup, contract narrowing, or migration,
declare the batch kind as `mixed-risk`, name the risky slices, and list the
approval gate for each risky slice.

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

Use `Overrides` only for durable execution-contract deviations that future
execution sessions must obey. Do not use `Overrides` for session-local
create-spec context, artifact creation history, or mode reminders such as
"treat this session as create-spec" or "implementation starts later"; those
claims describe the planning session, not an execution-contract deviation.
Place create-spec task context in the current baseline, assumptions, purpose,
handoff notes, or active-state prose where it explains how the artifact was
created without changing the future execution contract.

For lean specs, do not repeat full command blocks in every slice if a validation
profile covers them. Reference the selected profile file under
`references/validation-profiles/` and list only slice-specific commands or
overrides. For test-only or docs-only slices, explicitly state that project-level
integration harnesses, index/search/graph refreshes, generated-doc refreshes,
package installs, and final validation are not part of per-slice worker work
unless the slice deliberately assigns them.

Every focused validation command in a generated runway must declare exactly one
status class before execution:

- `required-green`: the command is expected to pass now, or the slice explicitly
  owns the remediation that makes it pass before it can gate later work. Use this
  only with a current passing result, or with a named slice-owned remediation path
  and acceptance criteria that prove the command becomes green.
- `known-red-baseline`: the command currently fails. It can be retained as
  diagnostic evidence or remediation scope, but cannot block execution until a
  named slice fixes the failure and promotes it with green evidence.
- `implementation-created`: the command targets a test, file, fixture, tool, or
  artifact that does not exist yet. Name the slice that creates it before the
  command can become a required gate.
- `conditional`: the command runs only when named files, artifacts, metadata, or
  project areas change. State the trigger condition precisely enough that an
  executor can decide whether to run it.
- `diagnostic-only`: the command informs planning, review, or risk assessment,
  but is not an execution gate unless a later slice explicitly promotes it.

Do not silently promote a known-red command, a missing future-created command, or
a diagnostic command to `required-green`. Promotion requires explicit evidence
that the command is now green, or an explicitly named slice-owned remediation
path that makes it green before it gates downstream work.

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
