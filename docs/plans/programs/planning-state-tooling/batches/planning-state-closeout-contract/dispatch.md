# Planning-State Closeout Contract Dispatch

```yaml
batch_id: planning-state-closeout-contract
status: queued
source_program_ledger: docs/plans/programs/planning-state-tooling/LEDGER.md
included_findings:
  - id: PST-4
    title: Batch closeout lacks a bounded evidence-index contract
excluded_findings:
  - id: PST-5
    reason: Migration bootstrap should wait until closeout evidence can prove completed batches without archaeology.
  - id: PST-6
    reason: SQLite remains a rebuildable projection after canonical closeout artifacts are stable.
goal: Add a bounded closeout evidence-index contract for completed batches, with validation and explicit rendering from registered artifacts, receipts, completed-slice summaries, and obligations.
owner_seam: scripts/planning_state.py remains the workflow facade; add small owner helpers only if closeout schema, parsing, or rendering would otherwise make the facade hard to review.
validation_class: focused closeout contract tests, planning-state CLI checks, Markdown fixture round-trip checks, and ruff on touched Python files.
primary_fixture:
  project: codex-config
  planning_root: docs/plans/
  expected_resolution:
    - Read root and program `CURRENT.md` before ledgers or historical plans.
    - Treat this dispatch/runway pair as the queued planning-state batch.
    - Validate closeout examples against registered dispatch, runway, closeout, completed-slices, receipt, output, and obligation facts.
secondary_fixture:
  project: Graphify-style Layout v1 fixture
  planning_root: test temp root
  expected_resolution:
    - Use project-neutral Layout v1 paths and state fixtures.
    - Do not require Graphify-specific production branches, cache paths, validation commands, or local overlays.
closeout_contract:
  - Closeout Markdown is a compact pointer-first evidence index, not an execution transcript.
  - Required facts include batch ID, status, source dispatch, runway, completed-slices archive, commits or commit range, validation evidence, review evidence, runner or transition receipts when present, closed obligations, open/deferred obligations, and cleanup residue classification.
  - Validation must reject missing required pointers, unbounded logs, missing evidence for closed obligations, unknown batch IDs, and closeout paths outside the registered batch directory.
  - Rendering may write only to an explicit target path or stdout; it must not rewrite `CURRENT.md`, `LEDGER.md`, or live closeout files implicitly.
guardrails:
  - Markdown and JSON remain canonical, human-readable, and diffable.
  - SQLite is out of scope.
  - No live planning Markdown is rewritten from tool state except an explicitly targeted closeout artifact requested by the command caller.
  - Transition state writes still require explicit `--state-file` and receipt paths.
  - Existing Markdown-only roots must keep working when no planning-state JSON exists.
  - Closeout output stays bounded; long logs, transcripts, and large schema dumps belong in referenced artifacts, not `closeout.md`.
dependencies_satisfied:
  - PST-1 read-only `current` and `validate` diagnostics exist.
  - PST-2 path allocation and artifact registration commands exist.
  - PST-3 obligation facts exist in explicit state fixtures and transition receipts.
  - PST-7 command/file protocol boundary exists for runner interop.
dependencies_blocking:
  - None for a closeout contract built on explicit artifacts and fixtures.
suggested_slices:
  - Define the closeout evidence-index contract and fixture helpers.
  - Add closeout validation that consumes registered artifacts and obligation facts.
  - Add explicit closeout rendering for stdout or caller-provided target paths.
  - Document the closeout workflow and update active planning state after execution.
stop_conditions:
  - The batch would need SQLite or a durable query store.
  - The batch would need to rewrite root/program `CURRENT.md`, program ledgers, dispatches, or runways from tool state.
  - The batch would need hidden inference from historical filenames instead of explicit registered artifacts.
  - The batch would need Graphify-specific production paths or validation commands.
  - The closeout document would become a transcript or long log dump instead of a bounded evidence index.
expected_spec_path: docs/plans/programs/planning-state-tooling/batches/planning-state-closeout-contract/runway.md
```
