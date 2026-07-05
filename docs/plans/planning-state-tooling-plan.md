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
- JSON state ownership is project-specific. A project may choose committed
  companion state, ignored-local state, external state, generated-only proof, or
  no durable state. Reusable workflow code must resolve that policy from
  project instructions, local overlays, active specs, or explicit user
  direction.
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
python scripts/planning_state.py validate --root <planning-root> --require-project-policy <state-file|projection|all>
python scripts/planning_state.py validate --root <planning-root> --projection-target <planning-state.sqlite>
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
- `project_policy`: resolved project-owned state/projection policy facts, or
  `null` when no policy is declared for read-only Markdown checks.
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

## Project State Policy

Planning-state tooling is reusable workflow code. It must not assume that every
project can commit planning state beside its source files. `codex-config` owns
its workflow docs, while Graphify-style work may use ignored local overlays, and
future projects may choose different state locations.

Projects should be able to declare these values through project instructions,
local overlays, root/program `CURRENT.md`, active specs, or explicit user
direction:

- `planning_root`: human-readable planning artifacts.
- `run_artifact_root`: runner-owned JSON state, receipts, manifests, and
  telemetry.
- `output_root`: generated reports and projections.
- `state_file_policy`: `generated-only`, `committed`, `ignored-local`,
  `external`, or `none`.
- `state_file_path`: required when the policy selects a durable project-owned
  state file.
- `projection_policy`: `generated-only`, `ignored-local`, `external`, or
  `none`; committed projection files require an explicit project exception.
- `projection_path`: required when the policy selects a durable projection
  target.
- `update_authority`: `command`, `ask-first`, or `read-only`.

`state_file_path` is required for `committed`, `ignored-local`, and `external`
state-file policies and must be absent for `generated-only` and `none`.
`projection_path` is required for `ignored-local`, `external`, and any explicit
committed-projection exception and must be absent for `generated-only` and
`none`.

Read-only commands such as `current` and `validate` should continue to work for
Markdown-only projects. Commands that write durable JSON state or projections
must require compatible project policy. When policy is missing, stdout and
caller-provided temporary proof output remain valid, but durable writes should
stop with a stable blocker. Read-only `validate` can preflight that boundary
with `--require-project-policy state-file`, `projection`, or `all`, which
reports missing or incompatible durable policy without writing state or
projection data. `--projection-target` checks a concrete future projection
target before the SQLite rebuild command exists; stdout and explicit `/tmp`
proof targets remain valid for generated-only or missing policy, while
committed, ignored-local, and external targets must match the declared project
policy path.

The contract is a discovery contract, not a default layout. Reusable workflow
code must resolve these facts from the current project context and must not
hard-code `codex-config` committed planning paths, Graphify ignored local
overlay paths, or a universal state/projection location.

Example policies:

- `codex-config` owns committed workflow planning documentation under
  `docs/plans/`. Durable companion JSON state may be committed only when a
  future spec declares that path and the command validates it against
  `state_file_policy: committed`. SQLite remains a generated projection unless
  an explicit project exception selects a committed projection path.
- A Graphify-style local overlay can keep personal planning coordination under
  an ignored root such as `my-docs/plans/`. Durable JSON state or SQLite output
  for that workflow must use `ignored-local` or `external` policy and must not
  be copied into the upstream repository by generic tooling.

SQLite work must consume the resolved project policy before choosing any state
file or projection target. The projection batch may define schema, rebuild, and
report behavior, but it must reject durable outputs that are not allowed by the
project's declared state-file and projection policy.

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
2. Move batch selection, artifact registration, cross-batch obligations, and
   closeout evidence checks behind explicit command/file protocols.
3. Bootstrap tool state from existing `CURRENT.md` files, program ledgers, and
   co-located batch artifacts with `bootstrap-state`.
4. Validate migrated state fixtures with `current` and `validate --state-file`
   before any runner or reporting layer consumes them.
5. Keep `CURRENT.md`, `LEDGER.md`, dispatches, runways, closeouts, and
   completed-slices archives as the human-readable coordination state. Bootstrap
   output is companion JSON state and must not rewrite those Markdown files.
6. Choose durable state-file and projection locations only through explicit
   project policy. Until then, write migration fixtures only to stdout,
   caller-provided temp paths, or other explicit non-planning-root targets.
7. Add SQLite reporting only after canonical Markdown/JSON state and project
   state/projection policy have stable round-trip evidence.

The migration pilot proved the bootstrap boundary without selecting a durable
state-file location. `bootstrap-state` now emits a `planning-state-tool-state`
version `1` fixture from Layout v1 Markdown, preserves root/program
`CURRENT.md` active-first precedence, registers existing co-located batch
artifacts, and leaves redirect ledgers or historical flat files as warnings or
compatibility evidence. `current --state-file` and `validate --state-file`
cross-check migrated fixtures against live Markdown facts so future runner
preflights can reject drift instead of silently trusting stale JSON.

Existing Markdown-only workflows must keep working during migration. A project
without `.planning-state/state.json` or equivalent tool state should still be
usable through current Planning Artifact Layout v1 rules.

## SQLite Projection Boundary

SQLite now helps answer operational questions that are awkward to answer by
recursively scanning receipts and telemetry while keeping Markdown and JSON
canonical. The implemented projection workflow is explicit:

```text
python scripts/planning_state.py rebuild-projection --root <planning-root> --database <state.sqlite> [--state-file <state.json>] [--program <slug>] [--runner-artifact <artifact.json>] [--runner-artifact-manifest <manifest.json>]
python scripts/planning_state.py report-projection --root <planning-root> --database <state.sqlite> --report <pending-batches|missing-closeout-evidence|batch-evidence|runner-latest-run|runner-failed-phases|runner-context-pressure> [--state-file <state.json>] [--program <slug>] [--batch-id <batch-id>] [--format text|json]
```

`rebuild-projection` replaces only the explicit `--database` target after a
successful rebuild. It validates source identity, schema metadata, optional
state fixture identity, optional program scope, project projection policy, and
bounded runner source hashes. The database target can be a caller-provided temp
proof path, or a durable path only when the resolved project policy allows that
exact projection target. A database under the planning root, an undeclared
durable location, a path escape, a directory, or another policy-incompatible
target is rejected before the projection becomes workflow state.

`--runner-artifact` accepts an explicit compact runner artifact JSON file.
`--runner-artifact-manifest` accepts an explicit compact manifest JSON file that
lists runner artifact paths. Both are optional projection inputs. Missing or
stale runner artifacts block runner-specific reports that depend on them but do
not make ordinary planning reports require runner data.

The supported report names are:

- `pending-batches`;
- `missing-closeout-evidence`;
- `batch-evidence` with `--batch-id`;
- `runner-latest-run`;
- `runner-failed-phases`;
- `runner-context-pressure`.

SQLite must be:

- optional;
- rebuildable from canonical artifacts;
- safe to delete;
- hidden behind tool/report commands;
- limited to paths, metadata, compact summaries, statuses, and hashes.
- written only to targets allowed by resolved project policy.

Deleting the SQLite database is safe: rebuild it from Markdown planning
artifacts, explicit JSON state fixtures, closeout evidence indexes, runner
artifacts or manifests, and commits. Existing `current`, `validate`,
`bootstrap-state`, transition, and closeout commands do not require a database,
and agents should use `report-projection` output rather than SQL.

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
- SQLite reporting works without changing the canonical Markdown/JSON contract.
