# Planning-State Read-Only Core Dispatch

```yaml
batch_id: planning-state-readonly-core
status: selected
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-1
    title: Planning state is inferred from Markdown and filenames
excluded_findings:
  - id: PST-2
    reason: Write transitions must wait until read-only state discovery is stable.
  - id: PST-3
    reason: Obligation mutation depends on the state model introduced by PST-1/PST-2.
  - id: PST-4
    reason: Closeout rendering should consume the read-only model first.
  - id: PST-5
    reason: Migration should wait until validation can prove source artifacts.
  - id: PST-6
    reason: SQLite is a projection and should wait until canonical state is stable.
goal: Add a read-only planning-state diagnostic that reports active planning state and validates existing artifacts without broad planning-tree scans.
owner_seam: scripts/planning_state.py as the first planning-state facade, with small owner modules only if the first slice proves they are needed.
validation_class: focused Python unit tests plus dry-run CLI checks; no GitHub or network access.
primary_fixture:
  project: Graphify
  planning_root: /home/alacasse/projects/graphify/my-docs/plans/
  expected_resolution:
    - Read root `CURRENT.md`.
    - Read only listed program `CURRENT.md` files before program ledgers.
    - Report both active programs as having no selected dispatch, active runway, or queued batch when their program `CURRENT.md` files say `None`.
    - Follow old flat ledger redirect files to the program `LEDGER.md` files.
    - Ignore historical flat dispatch/runway filenames for active selection.
    - Warn when historical pickup notes or compatibility files claim queued work that contradicts root/program `CURRENT.md` state.
secondary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Report Planning Artifact Layout v1 from `docs/plans/CURRENT.md`.
    - Report both active programs from the root `CURRENT.md`.
    - Follow old flat ledger redirects to program `LEDGER.md` files.
    - Treat historical archive files and closed compatibility paths as non-active.
guardrails:
  - Markdown and JSON remain canonical.
  - SQLite is out of scope.
  - Tool output is semantic and agent-facing; no SQL or backing-store details.
  - No Graphify-specific paths or validation commands in generic code; Graphify is fixture data for project-neutral behavior.
  - Existing Markdown-only workflows remain valid when no tool state exists.
  - Prefer root/program `CURRENT.md` over pickup notes, redirect ledgers, old flat dispatch/runway files, generated graph outputs, and historical filenames.
dependencies_satisfied:
  - Planning Artifact Layout v1 exists.
  - Architecture Program Runway active-state fast path exists.
  - Runner already has JSON state, receipts, manifests, telemetry, and input inventory owners.
  - Graphify has root and program `CURRENT.md` files plus migrated program ledgers for the current local workflow.
dependencies_blocking:
  - None for read-only validation.
suggested_slices:
  - Define the read-only state model and fixture set from Graphify `my-docs/plans/` plus codex-config `docs/plans/`.
  - Implement `planning-state current` for roots, active programs, selected dispatch, active/queued runway, latest closeout, and allowed next actions.
  - Implement `planning-state validate` for `CURRENT.md`, program ledgers, redirect ledgers, selected batch directories, and stale active-state contradictions.
  - Document fallback behavior for Markdown-only roots and update user-facing workflow guidance.
stop_conditions:
  - The batch would need to write canonical state or rendered Markdown.
  - The batch would need SQLite.
  - The batch would need Graphify-specific path rules in generic code.
  - The batch would need recursive historical archive classification or bulk migration.
  - Active-state rules conflict with Planning Artifact Layout v1.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-readonly-core/runway.md
```
