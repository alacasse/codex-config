# Planning-State Tooling Plan

## Purpose

Move fragile planning coordination out of agent memory and ad hoc Markdown
editing into a small tool-owned state layer. The tool should let agents ask
workflow-level questions and perform workflow-level transitions without
manually inferring active state from filenames, historical plans, or broad file
searches.

This is planning work for a future implementation batch. It does not replace
the existing architecture-program runner, Batch Runway, or Planning Artifact
Layout v1.

It also does not become the runner. The long-term runner direction is a
separate OSS Go implementation behind shared workflow contracts. Planning-state
tooling should stay interoperable through explicit command/file protocols,
schemas, and fixtures rather than by becoming an imported dependency of the
runner core.

## Source Context

- GitHub issue #22: tool-owned planning state behind workflow-level commands.
- GitHub issue #8: optional SQLite operational index for runner artifacts.
- GitHub issue #10: generic phase-runner product idea.
- GitHub issue #12: phase-runner repo split and dogfooding boundary.
- Planning Artifact Layout v1 in `skills/planning-artifacts/SKILL.md`.
- Planning-state tooling ledger:
  `docs/plans/programs/planning-state-tooling/LEDGER.md`.
- Architecture Program Runway guidance in
  `skills/architecture-program-runway/SKILL.md`.
- Current runner state, receipt, artifact, telemetry, and input-inventory owners
  under `scripts/architecture_program_runner*.py`.
- First real active-state fixture: Graphify local planning root at
  `/home/alacasse/projects/graphify/my-docs/plans/`, where root/program
  `CURRENT.md` files are authoritative while old flat files, redirect ledgers,
  and stale pickup notes remain as compatibility context.

## Source-Of-Truth Model

Markdown and JSON remain canonical.

- Markdown stays the human and agent-readable coordination surface:
  `CURRENT.md`, `LEDGER.md`, `dispatch.md`, `runway.md`, `closeout.md`, and
  `completed-slices.md`.
- JSON state is allowed for tool-owned active state because it is explicit,
  strict, easy to validate, and easy to render back into Markdown.
- SQLite, if added, is an optional rebuildable projection for reporting and
  queries. It is not canonical storage.
- If the SQLite database is deleted, the workflow must still be understandable
  and recoverable from Markdown, JSON state, runner receipts, manifests,
  telemetry, and commits.

Agents should use commands and rendered summaries, not SQL or direct database
mutation.

## Model-Facing Command Surface

The first useful tool is intentionally small. The read-only commands are
available as direct script subcommands:

```text
python scripts/planning_state.py current --root <planning-root>
python scripts/planning_state.py validate --root <planning-root>
python scripts/planning_state.py current --root <planning-root> --format json
python scripts/planning_state.py validate --root <planning-root> --format json
python scripts/planning_state.py validate --root <planning-root> --state-file <state.json>
```

The first write-transition helpers are path and fixture oriented. They do not
render or rewrite Markdown:

```text
python scripts/planning_state.py allocate-batch --root <planning-root> --program <slug> --batch-id <batch-id>
python scripts/planning_state.py register-artifact --root <planning-root> --program <slug> --batch-id <batch-id> --type <dispatch|runway|closeout|completed-slices|receipt|output> --path <path> [--state-file <state.json>] [--dry-run]
python scripts/planning_state.py select-batch --root <planning-root> --program <slug> --batch-id <batch-id> --dispatch <dispatch.md> --state-file <state.json> [--receipt-file <receipt.json>]
python scripts/planning_state.py queue-batch --root <planning-root> --program <slug> --batch-id <batch-id> --dispatch <dispatch.md> --runway <runway.md> --state-file <state.json> [--receipt-file <receipt.json>]
```

`allocate-batch` returns the canonical Layout v1 co-located batch directory and
Markdown artifact paths under
`<planning-root>/programs/<program>/batches/<batch-id>/`. `register-artifact`
validates ownership, co-location, collisions, path escapes, absolute paths, and
supported artifact types. Without `--state-file`, or with `--dry-run`, it emits
the same registration facts without writing a fixture.

`select-batch` and `queue-batch` mutate only an explicit JSON state file and
optionally write an explicit transition receipt. They validate registered
dispatch/runway artifacts, same-batch co-location, existing artifact files,
single active state per program, and known ledger batch rows when the ledger has
batch rows. A rejected transition leaves the state file unchanged and returns a
receipt with structured blockers; an applied transition writes the new
selected/queued state and the same receipt shape.

Future write commands remain planned, not implemented:

```text
planning-state create-program <slug> --title "<title>"
planning-state close-batch <batch-id> --status completed
planning-state render-current
planning-state render-ledger
```

The exact CLI shape can change during implementation, but the tool contract
should preserve these behaviors:

- Resolve active programs, selected batch, queued runway, latest closeout, and
  allowed next actions.
- Validate that active Markdown files and tool-owned JSON state agree.
- Later, allocate or validate canonical batch/artifact paths.
- Later, register artifacts without agents hand-editing state tables.
- Later, close a batch only when closeout evidence and required obligations are
  reconciled.
- Later, render compact Markdown views for humans and future agents.

Closeout workflow is intentionally bounded and pointer-first. A completed batch
should have an explicit `closeout.md` evidence index that points to the source
dispatch, runway, completed-slices archive, commit or commit range, validation
evidence, review evidence, transition or runner receipts when present, closed
obligation evidence, open/deferred obligations, and cleanup residue
classification. It must not embed transcripts, long validation logs, or session
reconstruction prose.

The closeout command surface is explicit-file oriented:

```text
python scripts/planning_state.py validate-closeout --root <planning-root> --program <slug> --batch-id <batch-id> --closeout <closeout.md> --state-file <state.json>
python scripts/planning_state.py render-closeout --root <planning-root> --program <slug> --batch-id <batch-id> --state-file <state.json> --completed-slices-summary "<summary>" --validation-artifact <path> --validation-summary "<summary>" --review-artifact <path> --review-summary "<summary>" --cleanup-classification <none|intentional|deferred> [--target <closeout.md>]
```

`render-closeout` prints Markdown to stdout unless `--target` is supplied. A
target write is valid only for the registered closeout path for that batch. The
command does not rewrite root/program `CURRENT.md`, ledgers, dispatches,
runways, selected/queued state, or migration fixtures. Closeout rendering and
validation consume explicit registered artifact facts and obligation facts; they
do not infer evidence from old filenames, commit history scans, SQLite, or long
runner transcripts.

When a planning root has Layout v1 `CURRENT.md` files, agents should run the
read-only diagnostics before broad planning tree scans or historical filename
searches. `current` reports the root/program active state and stale-context
warnings; `validate` checks the same state without mutating Markdown, JSON,
SQLite, or downstream project files.

Text output remains the default human and agent-facing format. JSON output is
an opt-in machine-readable protocol for runner adapters and fixtures. Consumers
must treat the command invocation and written artifact files as the integration
boundary; they should not import `scripts.planning_state` as a runtime library,
scrape Markdown filenames, or depend on private Python helper names.

The current JSON protocol is `planning-state-facts` version `1`. Its document
contains:

- `protocol`: name, version, and command.
- `exit`: returned code, compact meaning, and exit-code semantics.
- `root`: planning root facts and active program pointers.
- `programs`: resolved program facts and artifact pointers.
- `obligations`: explicit obligation records loaded from `--state-file`, or an
  empty array when no state fixture is supplied.
- `warnings`: stale context and redirect evidence.
- `blockers`: fatal validation messages.
- `validation_messages`: all info, warning, and error validation messages.

Exit code `0` means the command completed; for `validate`, it also means no
blockers were found. Exit code `1` is used by `validate` when blockers were
found. Exit code `2` means command usage or protocol negotiation failed.

Future write-transition fixtures use explicit JSON objects rather than inferred
Markdown filenames. Tool-owned state fixtures use
`planning-state-tool-state` version `1` with a planning `root` and `programs`
array. Transition receipt fixtures use
`planning-state-transition-receipt` version `1` with `root`, `transition`,
`status`, `program`, `batch_id`, `artifacts`, `warnings`, `blockers`, and
structured `messages`.

Migration/bootstrap fixtures may include a `bootstrap` contract object while
remaining `planning-state-tool-state` version `1`. The bootstrap source is
Layout v1 Markdown, and selection precedence is root/program `CURRENT.md`
active-first. JSON state may safely carry `root`, program slugs, program
`CURRENT.md` paths, ledgers, selected/active/queued batch pointers, latest
closeout pointers, registered artifact facts, and obligations. Markdown remains
the owned surface for human-readable `CURRENT.md`, `LEDGER.md`, `dispatch.md`,
`runway.md`, `closeout.md`, and `completed-slices.md` content. Redirect
ledgers, stale pickup notes, and historical flat batch files are compatibility
evidence and warnings; they must not become selected, active, or queued JSON
state.

State fixtures may also include an `obligations` array. Each obligation has an
`id`, `owner`, `source_batch`, optional `target_batch`, optional
`close_condition`, `status`, and optional `evidence_path`. `validate` reports
open and closed obligation facts when invoked with `--state-file`, and flags
duplicate IDs, missing owners, missing target/close conditions, missing
evidence for closed obligations, and source batches that are not registered in
the state fixture. Transition receipts include the obligations for the selected
or queued batch so closeout work can require bounded evidence without parsing
Markdown prose.

## Runner Interoperability Boundary

Planning-state tooling and the phase runner should remain separate but
interoperable.

- `planning_state` answers "what planning state exists and is it structurally
  valid?"
- The runner answers "given an explicit workflow/work-unit input, how do phases
  execute, persist receipts, transition state, and stop safely?"
- The future Go runner should consume planning facts through a documented
  adapter or preflight protocol, not by reimplementing `codex-config` Markdown
  heuristics, inferring active state from Markdown filenames, or importing
  Python internals.
- A runner preflight can consume `select-batch` or `queue-batch` by invoking the
  command with explicit `--state-file` and `--receipt-file` paths, then reading
  only the JSON receipt status, artifacts, obligations, warnings, and blockers.
  The receipt is the file protocol; private Python helpers and Markdown
  rendering are not part of the runner boundary.
- The Python dogfooding runner and future Go runner should share golden
  Planning Artifact Layout v1 fixtures for active `CURRENT.md` precedence,
  redirects, stale historical files, selected/queued/active batch pointers, and
  validation error boundaries.

Future write-transition work should therefore define machine-readable outputs
for planning-state facts before wiring them into runner workflows. A useful
interop contract should name the command invocation, JSON shape, warning/error
shape, and exit-code meaning. Until that exists, keep `planning_state` as an
independent diagnostic command that future agents run before broad planning
tree scans.

## State Boundaries

The tool should own:

- active program registry;
- selected, queued, active, completed, blocked, and deferred batch state;
- canonical artifact paths for dispatch, runway, closeout, receipts, run
  artifacts, and generated outputs;
- cross-batch obligations with IDs, owners, and close conditions;
- latest closeout pointers and allowed next actions;
- validation that rendered `CURRENT.md` files match state.

The tool should not own:

- architecture decisions;
- finding prioritization;
- runner phase execution, state transition, receipts, telemetry, or worker
  adapters;
- Batch Runway slice design;
- implementation code changes;
- worker/reviewer delegation;
- project-specific validation commands;
- Graphify-specific paths, cache settings, or local overlays;
- full transcripts, long logs, or prompt/session reconstruction.

## Migration Approach

Migrate active pickup safety before historical neatness.

1. Use read-only `current` and `validate` diagnostics over the Graphify
   active-state fixture and the codex-config Layout v1 plus redirect
   compatibility fixture.
2. Bootstrap tool state from existing `CURRENT.md` files and program ledgers.
3. Render `CURRENT.md` from tool state, then validate round trips.
4. Move batch selection and artifact registration behind tool commands.
5. Add cross-batch obligations and closeout evidence checks.
6. Pilot write transitions on `docs/plans/` only after the read-only Graphify
   fixture proves active-state precedence and stale-context warnings.
7. Add SQLite reporting only after state and rendering are stable.

Existing Markdown-only workflows must keep working during migration. A project
without `.planning-state/state.json` or equivalent tool state should still be
usable through current Planning Artifact Layout v1 rules.

## SQLite Projection Boundary

SQLite can help answer operational questions that are awkward to answer by
recursively scanning receipts and telemetry:

- latest run for a program;
- failed phases by reason;
- context pressure by phase;
- batch to dispatch/spec/receipt/commit-range lookup;
- pending executable batches;
- missing closeout evidence.

SQLite must be:

- optional;
- rebuildable from canonical artifacts;
- safe to delete;
- hidden behind tool/report commands;
- limited to paths, metadata, compact summaries, statuses, and hashes.

SQLite must not store canonical program ledgers, dispatch packet prose, Batch
Runway specs, closeout decisions, full prompts, long logs, or transcripts.

## Non-Goals

- Do not create a new `phase-runner` repository in this workstream.
- Do not implement the future OSS Go runner in this workstream.
- Do not make downstream runners depend on Python `planning_state` internals.
- Do not require SQLite for active-state resolution.
- Do not expose SQL to normal agent workflows.
- Do not replace human-readable Markdown planning artifacts.
- Do not make downstream projects depend on Graphify-specific paths or
  assumptions.
- Do not implement a full orchestration runner as part of planning-state v1.
- Do not change Batch Runway execution semantics.

## Initial Success Criteria

- A fresh agent can run one command to see active program state and allowed next
  actions.
- A fresh agent can run one command to validate whether state, `CURRENT.md`,
  ledgers, batch directories, and runner artifacts agree.
- A future runner implementation can consume planning facts through explicit
  schemas or command output instead of scraping historical filenames.
- For the Graphify fixture, active state resolves from root/program
  `CURRENT.md` files and warns about stale pickup notes or historical flat files
  without treating them as selected work.
- For the codex-config fixture, active state resolves from `docs/plans/CURRENT.md`
  and old flat ledger paths are treated as redirects, not active sources.
- Batch and artifact paths are allocated or checked by code.
- Cross-batch obligations cannot disappear into old closeout prose.
- Completed batches have bounded closeout evidence indexes.
- SQLite reporting can be added later without changing the canonical contract.
