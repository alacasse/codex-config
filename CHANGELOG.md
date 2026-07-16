# Changelog

## Unreleased

### Exact-commit command-owner acceptance

Problem: aggregate reports recursively launched one pytest process per evidence
node, reevaluated the full catalog, and treated individual test-function source
hashes as acceptance authority.

Decision: add one private exact-clean-commit acceptance execution, run all
marked evidence nodes in one sanitized pytest process, reuse immutable catalog
evaluations within a process, and write its report-digest-bound minimal result
plus JSON/text reports from the accepted in-memory report. Regular reporting
remains explicitly unobserved. Remove per-function source hashes and AST
body-preservation checks.

Expected effect: fast validation avoids disposable runtime work, final
acceptance rejects stale inputs and every non-pass outcome, and report
formatting launches no pytest process. The harness remains non-installed and
does not transfer command ownership or perform cutover.

### Non-installed command-owner scenario evidence

Add the repo-local behavioral scenario catalog, disposable cutover fixtures,
and deterministic aggregate evidence report. The harness is not installed and
does not transfer workflow ownership, switch a generation, remove a live
route, or implement work reserved for CCFG-24 and later.

### Candidate skill-authoring feature

Problem: the accepted `skill-authoring` core, planning reference, and trial
catalogs were repo-local source only, so the candidate generation had no single
installable authoring surface that also carried the canonical validator and
schema.

Decision: register one agent-facing `skill-authoring` feature at `1.0.0` with
exact links to `skills/skill-authoring`, `scripts/skill_contract.py`, and
`schemas/skill-contract-v1.schema.json`. Keep it outside every command-owner and
support/runtime feature's requirements.

Expected effect: the candidate generation can install and validate the complete
contract-first authoring surface as one feature without turning it into a
primary human command, adding a runtime dependency, or changing the stable
generation.

### Recoverable planning-selection transaction prototype

Problem: the planning stores could persist individual current-state and
artifact writes, but there was no durable owner for resuming the four-step
dispatch-to-queued selection sequence after a process interruption.

Decision: add a closed-world `planning-selection-transaction/v1` record and a
fixture-driven prototype that binds the initial intent, appends validated stage
evidence, uses the existing current and artifact store primitives, and resumes
from every durable boundary without deleting evidence.

Expected effect: tests can now prove exact replay, reused-ID rejection,
unexplained-state-movement rejection, and recovery after dispatch, selected
state, runway, and queued-state interruptions. This slice does not integrate
the prototype into `plan-batch` or mutate live planning state.

### Repo-local skill contract validation

Problem: command-owner redesigns had no closed, machine-checkable contract for
skill ownership and dependencies, and no deterministic before/after proof that
a migration actually moved ownership instead of retaining broad dependencies,
duplicating durable facts, or only renaming a skill.

Decision: add the closed-world `skill-contract/v1` schema, one repo-owned
validator and CLI, explicit audience and graph policies, and a versioned
migration-policy input for fixture-backed before/after comparisons.

Expected effect: repository tests can now prove structural contracts, catalog
ownership, dependency/reference integrity, and migration outcomes without
parsing prose or depending on installed runtime state. This boundary is
intentionally repo-local: current skills, `codex-features.json`, and installed
state are unchanged. CCFG-22 owns the future runtime-consumer and installation
decision.

### Stable cross-checkout pre-creation support

Problem: strict `cross-checkout-context/v1` validation requires the candidate
repository and candidate Codex home to exist, so it cannot safely authorize a
later session to create those exact absent paths.

Decision: add a separate temporary `cross-checkout-precreation/v1` interface to
the existing Batch Runway-installed `cross_checkout_context.py` helper, keep
that helper as the single mechanical owner, and propagate the new facts through
`plan-batch`, `work-batch`, Batch Runway, `runway_worker`, and
`runway_reviewer`. The strict interface remains the unchanged post-creation
contract and requires a validated transition before later implementation. This
temporary ownership remains scheduled for removal at CCFG-29 final integration.

Expected effect: after the stable configuration is installed and Codex is
reloaded in a fresh session, the workflow can fail closed on absent-path intent,
exact creation authority, and transition identity without weakening strict
post-creation validation. This release does not install or reload the changed
control surface in the current session and does not create candidate paths.

### Stable cross-checkout control bootstrap

Problem: a future command-owner migration must keep one loaded toolchain
generation in control while canonical planning and candidate implementation
live in different repositories. The stable command and agent contracts had no
installed owner for validating those roots, revisions, write scopes, or
delegated generation identity before work began.

Decision: install the temporary `cross-checkout-context/v1` helper through the
existing `batch-runway` manifest feature, and make `plan-batch`, `work-batch`,
Batch Runway, `runway_worker`, and `runway_reviewer` consume that owner only for
explicitly cross-checkout work. Require fail-closed validation and handoff
propagation before delegation, add nullable verified identity to the v2 worker
and reviewer results, and retain all lifecycle decisions with the coordinator.
The temporary bridge remains scheduled for removal at CCFG-29 final
integration.

Expected effect: fresh stable generations can reject missing, mismatched, or
wrong-generation cross-checkout work before writes or delegation, while normal
single-root batches remain unchanged and candidate paths, installation state,
and the default Codex home are not mutated by this bootstrap.

### Custom agent role contracts

Problem: four registered agents still depended on caller assumptions for scope,
authority, stopping conditions, evidence, and failure reporting. Worker and
reviewer schemas were also copied into Batch Runway references, while clean
report line caps could suppress material information.

Decision: strengthen `spark`, `runway_worker`, `runway_reviewer`, and
`import_topology_reviewer` around explicit role boundaries, lifecycle authority,
evidence standards, structured status values, and completion criteria. Keep
their existing model assignments, make each agent TOML the canonical owner of
its current result contract, and leave Batch Runway responsible for triggers,
task handoffs, coordinator lifecycle, and coordinator receipts. Preserve named
v1 contract interpretation for existing specs and introduce Standard Execution
Contract v2 plus Registered Agent Result Contract v2 for new work.

Expected effect: delegated work should stop safely on ambiguity or stale
evidence, preserve unrelated work and unchanged contracts, report every material
finding regardless of length, and avoid schema drift between agent definitions
and workflow prompts.

### Codebase investigator agent contract

Problem: the read-only support agent was framed as a fast, vague exploration
role, which could encourage shallow file inventories and incomplete findings
instead of answering a bounded technical question with supported evidence.

Decision: give the registered role a clean `codebase_investigator` identity,
set its model to `gpt-5.6-terra` with low reasoning effort, and make it the sole
owner of the YAML investigation contract. Keep Batch Runway responsible only
for decision-oriented briefs, coordinator lifecycle, and compact downstream
handoffs, with no compatibility alias.

Expected effect: delegated investigations should distinguish evidence,
inference, and uncertainty; return partial or blocked results when necessary;
and reduce coordinator context without replacing implementation or review
agents.

### Project-owned Python validation tools

Problem: agents could run ambient `pytest` or discover that `python -m ruff`
was unavailable, then treat missing local tooling as normal validation noise.

Decision: add `pytest` and `ruff` to the locked dev dependency group, keep
`basedpyright` as the project type checker instead of adding `mypy`, and
document the `uv run --frozen` validation commands.

Expected effect: future validation uses reproducible project-owned tools, and
missing ambient packages should no longer be accepted as a normal state.

### Absolute runway reference path guidance

Problem: Batch Runway create-spec guidance could lead generated runways to
embed local absolute paths for reusable repo-owned skill references, making
portable planning artifacts look machine-specific.

Decision: prefer repo-relative or skill-relative Batch Runway reference paths
in generated runway guidance, add an active-artifact guard for queued or active
runways, and preserve legitimate absolute runtime handoffs and project-specific
local values.

Expected effect: new selected, queued, or active runways should keep reusable
skill references portable without rewriting completed historical evidence.

### Deletion-test vocabulary ownership

Problem: generated dispatches and runways could invent deletion-test labels
such as `no-op`, `sediment`, `obsolete skill surface`, or `deletion-safe
evidence` without a canonical vocabulary owner or local definition.

Decision: make `dead-surface-audit` the canonical deletion-test evidence
vocabulary owner, define `legacy-removal`, `architecture-program-runway`, and
`batch-runway` as consumers of those terms, and require generated artifacts to
use canonical statuses or locally define non-canonical labels.

Expected effect: future CCFG-11-style planning can reject unsupported
deletion-test categories unless they are explicitly local labels with clear
non-canonical status; residue-style labels also need a concrete reason and a
removal condition or follow-up owner.

### Vague ledger row split guard

Problem: vague or mixed-risk ledger rows could be expanded into selected
dispatches and concrete runways that combined evidence gathering,
classification, decisions, migration, demotion, destructive cleanup, or
contract narrowing without a bounded owner, risk, and acceptance shape.

Decision: require `plan-batch` and `architecture-program-runway` to split,
block, or narrow vague mixed-risk rows before selected dispatch and runway
creation, and record CCFG-11's displaced deletion-test runway as superseded
planning evidence under that guard.

Expected effect: future CCFG-11 planning cannot resume from the old displaced
artifact unless it first produces a bounded split, explicit block, or narrowed
evidence-only/characterization-only dispatch.

### Closeout commit placeholder guard

Problem: final closeout artifacts can be committed by the same commit they need
to reference, which let unresolved coordinator-commit placeholder wording
survive in active batch artifacts.

Decision: require ordinary slice rows to record exact commit hashes while
self-referential final closeout rows use `this closeout commit`; add an active
batch stale-placeholder guard for closeout/runway artifacts.

Expected effect: future batch closeouts cannot report closure while active
artifacts still contain unresolved coordinator or commit placeholders.

### Work-batch same-batch closeout reconciliation

Problem: `work-batch` treated post-closeout program reconciliation as a
separate explicit user request, so completed batches could leave stale program
queue, `CURRENT.md`, or `LEDGER.md` state.

Decision: make same-batch program reconciliation part of `work-batch` closeout:
after `batch-runway execute-spec` creates concrete closeout evidence,
`work-batch` routes to `architecture-program-runway closeout-runway` for the
just-completed batch only, then stops.

Expected effect: agents can complete runway execution and clear completed-batch
program state without selecting, dispatching, refreshing, creating, or preparing
successor work. Successor planning still requires an explicit `plan-batch`
request.

### Plan-batch command contract

Problem: `plan-batch` was installed as a command-owner skill, but its
caller-visible contract did not fully spell out selected, queued, active, and
ledger-only states.

Decision: deepen the `plan-batch` skill around ledger-only selection,
selected-state handling, one-spec output, and stop-before-implementation
behavior while keeping Architecture Program Runway and Batch Runway as
agent-facing runtime owners.

Expected effect: agents can answer "create the next specs batch" from current
planning state without scanning external sources, replacing queued work, or
starting implementation.

### Single codex-config planning ledger

Problem: codex-config planning had two active program ledgers, making pickup
ambiguous between runner work and planning-state/skill cleanup work.

Decision: consolidate actionable APR and PST backlog into
`docs/plans/programs/codex-config/LEDGER.md` with neutral `CCFG-N` IDs, keep
only `codex-config` active in `docs/plans/CURRENT.md`, and archive the old APR
and PST ledger snapshots as evidence.

Expected effect: future agents start from one active codex-config ledger, while
closed APR/PST history remains findable without acting as a parallel backlog.

### Retire repository-root plans directory

Problem: the repository-root `plans/` directory still held historical
compatibility artifacts from a closed batch, making it look like a semi-active
planning location beside `docs/plans/`.

Decision: move the closed extraction-prep dispatch and runway under
`docs/plans/archive/compatibility/root-plans/`, remove the root `plans/`
directory, and document that agents must not recreate or use it.

Expected effect: `docs/plans/` is the only active planning root, while the
closed compatibility artifacts remain findable in the archive.

### Block external implement skill

Problem: the external `implement` skill can take over ordinary spec-based
repo work and impose workflow steps such as review delegation and commits that
may not match this repo's command-owner routing.

Decision: remove `implement` from the external skills lock, remove it from the
workflow guide's shaping-skill examples, and add regression coverage so it is
not treated as an installed external workflow here.

Expected effect: future agents should route implementation requests through
repo instructions and command-owner workflows instead of invoking the Matt
Pocock `implement` skill automatically.

### Workflow usage guide

Problem: external engineering skills and repo-owned command-owner skills could
still be read as competing ways to create executable work.

Decision: add a concise workflow guide that explains external shaping sources,
`add-to-ledger` ingestion, ledger-driven batch planning, runway execution, and
the agent-facing support skill boundary.

Expected effect: agents and humans can route vague ideas, GitHub tickets,
ADRs, CONTEXT follow-ups, and review findings into the canonical ledger path
without treating those sources as parallel active backlogs.

### Executable work source boundary

Problem: external engineering skills, GitHub issues, ADRs, specs, review notes,
and chat transcripts can all contain candidate work, but agents should not
treat them as parallel executable backlogs for `plan-batch`.

Decision: define `add-to-ledger` as the explicit ingestion boundary for named
external/candidate sources and keep the program ledger as the only normal
executable backlog source for `plan-batch`.

Expected effect: agents may ingest external tickets or skill outputs when
explicitly requested, but planning remains ledger-driven and avoids broad
source hunting.

### Command-owner input contract

Problem: command-owner routing was clarified, but command input semantics
remained ambiguous; agents could still treat `plan-batch` as allowed to invent
or add ledger work.

Decision: add a command input contract distinguishing fresh user-provided work
text, existing ledger work, and queued/active runway execution.

Expected effect: agents use `add-to-ledger` for new work text, `plan-batch` for
existing ledger work, and `work-batch` for queued/active runway execution.

### Command-owner bridge routing contract

Problem: command-owner skills were installed, but agents could still confuse
human intent ownership with runtime procedure ownership.

Decision: add `docs/skill-routing-contract.md` with routing, conflict, stop,
and bridge-state rules, then point the command-owner skills at it.

Expected effect: future agents choose the command-owner skill for user intent,
then use runtime/support skills only as selected procedures.

### Command-owner support boundary completion

Problem: the new command-owner skills were installed, but old runtime skill
entrypoints and UI prompts still read like direct commands, leaving the
migration halfway between the old names and the new command set.

Decision: demote `batch-runway`, `architecture-program-runway`,
`legacy-removal`, and `dead-surface-audit` in their skill frontmatter and UI
prompts, replace copy-first bridge wording with stable agent-facing support
boundaries, and add regression coverage for the catalog split.

Expected effect: users invoke `add-to-ledger`, `plan-batch`, `work-batch`, or
`port-by-contract` for normal work, while old runtime surfaces remain installed
only as support dependencies behind those commands.

### Human-facing command-owner skills

Problem: the main ledger and batch workflows were exposed through historical
runtime skill names like `architecture-program-runway` and `batch-runway`, which
made it unclear which skills the user should invoke directly and which were
agent-facing support.

Decision: accept `add-to-ledger`, `plan-batch`, and `work-batch` as the
human-facing command-owner migration target, keep `port-by-contract` as a
direct user command, and complete a copy-first migration batch that preserves
the existing runtime skills as current workflow surfaces rather than the target
user interface.

Expected effect: users can invoke the main workflow commands by name, while
planning-state, planning-artifacts, test-quality review, and legacy prevention
remain narrow agent-facing support or default workflow obligations.

### Default-agent subagent delegation

Problem: the global subagent-delegation instruction allowed main agents and
workflow orchestrators to delegate, but did not explicitly name the normal
default/principal Codex agent.

Decision: clarify that the default/principal agent is included in the standing
delegation permission and may orchestrate configured subagents as needed, while
still acknowledging that higher-priority runtime tool policy can require fresh
user permission.

Expected effect: normal Codex sessions carry the user's default preference for
subagent orchestration without introducing a separate `orchestrator` custom
agent or weakening narrower worker and reviewer role boundaries.

### Discovery skill role boundaries

Problem: specialized discovery skills could read as parallel planning systems
that produce durable program ledgers, queue state, or selected-batch state by
default.

Decision: define Legacy Removal role selection before durable ledgers and make
Dead Surface Audit an evidence-only auxiliary skill, with feature metadata
bumped for both reusable workflow surfaces.

Expected effect: discovery skills can produce evidence and dispatch handoff
material without bypassing program-level selection, grouping, queueing, or
Batch Runway execution ownership.

### Planning-state projection language and migration

Problem: projection-backed reporting was implemented and wired into consumers,
but agent-facing wording still made supported reports sound merely optional and
existing Layout v1 projects lacked a reusable adoption checklist.

Decision: describe projection reports as the policy-gated normal route for
supported history/reporting questions, add portable adoption guidance for
generated-only and ignored-local projection policies, and bump affected
installable workflow features.

Expected effect: fresh agents use `current` and `validate` for SQLite-free
active-state pickup, then use command-level projection reports before broad
historical scans when project policy permits, without hard-coding downstream
paths or durable database defaults.

### Architecture-program Pending finding update rules

Problem: Pending architecture findings could be controlled by selected,
queued, or active batch artifacts while later source-ledger edits silently
changed the finding scope.

Decision: require explicit closeout evidence, supersession, abandonment, split,
named amendments, or follow-up findings for Pending scope changes, with focused
regression coverage and a feature version bump.

Expected effect: Architecture Program Runway ledgers keep cut batch scope
stable and make post-selection scope changes visible before agents continue.

### Batch-runway create-spec override contract

Problem: Batch Runway create-spec guidance could let session-local planning
mode notes appear in durable execution `Overrides`, making future execution
contracts carry artifact-creation context.

Decision: limit create-spec `Overrides` to durable execution-contract
deviations, add focused regression coverage for the guidance and PST-18 queued
runway, and bump the installable Batch Runway feature version.

Expected effect: generated runway specs keep create-spec session context in
baseline, assumptions, purpose, handoff, or active-state prose instead of
future execution `Overrides`.

### Legacy-removal projection report routing

Problem: Legacy Removal used planning-state diagnostics for Layout v1 active
state, but supported history/reporting questions could still fall back to broad
historical scans before checking projection policy.

Decision: route supported Legacy Removal history/reporting questions through
planning-state projection-reporting guidance and policy-compatible
`report-projection` output while preserving Legacy Removal ownership of old and
canonical model definition, evidence inventory, compatibility decisions,
cleanup-residue classification, and handoff decisions.

Expected effect: Legacy Removal agents use projection reports as read-only
planning-state context for locating planning evidence, never as proof that a
legacy surface is live, dead, removable, public, or deferred.

### Architecture-program projection report routing

Problem: Architecture Program Runway used planning-state diagnostics for active
state, but program history/reporting and runner-summary questions could still
fall back to broad historical scans before checking projection policy.

Decision: route supported Architecture Program history/reporting questions
through planning-state projection-reporting guidance and policy-compatible
`report-projection` output while preserving program ledger, selected dispatch,
grouping, sequencing, and closeout ownership.

Expected effect: Architecture Program agents keep active-state pickup
SQLite-free and treat missing, blocked, stale, or policy-incompatible
projection reports as explicit blockers, warnings, or fallback decisions.

### Batch-runway projection report routing

Problem: Batch Runway used the shared planning-state diagnostic for active
pickup, but history/reporting questions could still fall back to broad
historical scans without first checking projection policy.

Decision: route supported Batch Runway history/reporting questions through
planning-state projection-reporting guidance and policy-compatible
`report-projection` output while keeping create-spec and execute-spec pickup on
`current` and `validate`.

Expected effect: Batch Runway agents keep active pickup SQLite-free and stop or
record an explicit fallback when projection policy is missing or incompatible.

### Planning-state projection routing guidance

Problem: the planning-state skill documented projection commands, but did not
clearly route history/reporting questions through policy-compatible projection
reports before broad historical scans.

Decision: update the skill entrypoint and target/projection references to
distinguish active-state `current`/`validate` from optional projection-backed
reporting, including `projection_usage` and `projection_rebuild_authority`
prerequisites.

Expected effect: agents keep active-state pickup SQLite-free while bounded
history/reporting workflows stop on missing or incompatible projection policy
instead of silently scraping historical planning files.

### Planning-state projection usage policy

Problem: project policy could say where a projection database may be written,
but not whether projection reports are expected or who may rebuild them.

Decision: add `projection_usage` and `projection_rebuild_authority` to
planning-state policy parsing, validation, and current/validate output while
preserving old policy blocks through conservative defaults.

Expected effect: agents can distinguish disabled, caller-directed, optional,
and expected projection reports without treating projection target paths as
usage guidance.

### Ledger pickup before knowledge graphs

Problem: in projects that also have a knowledge graph, agents could treat a
ledger pickup or "next task" request as a codebase graph query and inspect
generated graph context before reading the active `CURRENT.md` and program
ledger.

Decision: add a named `planning-state` Diagnostic-First Pickup rule for
next-task, next-batch/spec, selected-dispatch, and queued-work requests. The
consumer skills now point at that rule instead of each restating the full
knowledge-graph/search ordering.

Expected effect: fresh agents select or resume ledger work from root/program
`CURRENT.md` and the active ledger first, then use graph/search tools only for
specific evidence questions raised by the selected work.

### Planning-state consumer install dependencies

Problem: Batch Runway, Architecture Program Runway, and Legacy Removal now call
the shared `planning-state` diagnostic interface, but their feature metadata
still installed only the Layout v1 placement skill.

Decision: add `planning-state` as an install dependency for those consumers
while keeping `planning-artifacts` because they still consume placement
conventions directly.

Expected effect: installing any rewired consumer feature installs
`planning-artifacts`, then `planning-state`, then the consumer without creating
a dependency cycle.

### Legacy-removal planning-state diagnostics

Problem: Legacy Removal could start Layout v1 ledger or selected-dispatch work
from active files or historical planning docs without first using the shared
planning-state diagnostic interface.

Decision: route Layout v1 legacy ledger and dispatch intake through
`planning-state` current/validate diagnostics while preserving Legacy Removal
ownership of old/canonical model definition, evidence inventory, compatibility
decisions, cleanup-residue classification, and handoff to Architecture Program
Runway or Batch Runway.

Expected effect: fresh legacy-removal agents start from validated
planning-state facts before Layout v1 ledger work, and use target-policy or
projection guidance only when durable/generated state or reports are needed.

### Architecture-program planning-state diagnostics

Problem: Architecture Program Runway could start Layout v1 pickup or closeout
from active files, historical plans, or generated outputs without first using
the shared planning-state diagnostic interface.

Decision: route Layout v1 active-state pickup and closeout evidence through
`planning-state` current/validate diagnostics while preserving Architecture
Program ownership of program selection, grouping, queue state, dispatch packets,
handoff to Batch Runway, and closeout reconciliation.

Expected effect: fresh architecture-program agents start from validated
planning-state facts before broader planning reads without moving placement
policy out of `planning-artifacts` or embedding downstream project defaults.

### Batch-runway planning-state diagnostics

Problem: Batch Runway could consume Layout v1 active-state files, selected
dispatches, queued specs, or target policy without first using the shared
planning-state diagnostic interface.

Decision: route create-spec and execute-spec guidance through
`planning-state` current/validate diagnostics, carrying compact facts into
Batch Runway while leaving spec creation, execution orchestration, validation,
subagent routing, ledger updates, and commits owned by Batch Runway.

Expected effect: fresh Batch Runway agents start from validated planning-state
handoff facts before broad Layout v1 scans without embedding downstream project
paths or moving placement policy out of `planning-artifacts`.

### Planning-state install metadata

Problem: the new planning-state skill existed in the repository, but the
manifest did not expose it as an installable repo-owned feature or identify the
command boundary it depends on.

Decision: add a `planning-state` feature that installs the skill and
`scripts/planning_state.py`, depends on `planning-artifacts`, and extend focused
manifest and ownership tests for the new links.

Expected effect: agents can install or inspect the shared planning-state
interface through the normal codex-config feature metadata without wiring
consumer skills to depend on it yet.

### Planning-state projection and closeout references

Problem: the planning-state skill pointed agents at optional projection and
closeout workflows, but the detailed guidance for report sequencing, closeout
evidence, and runner-artifact inputs was missing.

Decision: add focused references for projection reports, pointer-first closeout
evidence, and optional runner artifacts, and route the entrypoint to load them
only when those workflows are requested.

Expected effect: agents can use report commands and closeout checks without
querying SQLite directly, requiring runner data for ordinary reports, or
embedding long logs and downstream project paths in reusable workflow guidance.

### Planning-state fixture and target-policy references

Problem: the new planning-state skill named state-fixture and target-policy
surfaces, but agents still had to infer command sequencing and safe write
targets from CLI behavior.

Decision: add focused planning-state references for JSON fixtures, transition
receipts, and policy-driven target selection across stdout, `/tmp`,
generated-only, committed, ignored-local, external, and none policies.

Expected effect: agents can load the extra guidance only when they need
fixtures or target decisions, while reusable workflow code continues to resolve
project policy instead of hard-coding a downstream planning layout.

### Planning-state skill entrypoint

Problem: agents had planning-state commands and Layout v1 conventions, but no
single skill entrypoint for safe read-only discovery and validation before
ledger-driven workflows consumed state.

Decision: add a `planning-state` skill entrypoint that routes through
`scripts/planning_state.py`, delegates Layout v1 placement to
`planning-artifacts`, and requires explicit policy or temporary proof targets
before durable JSON state or SQLite projection writes.

Expected effect: fresh agents can run the planning-state diagnostic hot path
without importing script internals, querying SQLite directly, scraping historical
filenames, or baking downstream project paths into generic workflow guidance.

### Planning-state skill-interface backlog

Problem: planning-state commands and Layout v1 rules existed, but there was no
single skill-level interface for agents to discover, validate, bootstrap,
project, and report planning state before other ledger-dependent skills consume
it.

Decision: add ordered ledger findings and candidate batches for a
`planning-state` skill interface followed by consumer-skill integration, keeping
layout ownership in `planning-artifacts` and operational state/projection
workflow in the future shared skill.

Expected effect: future work can first create the deep Planning State Diagnostic
skill, then wire `architecture-program-runway`, `batch-runway`, and
`legacy-removal` to use it without duplicating active-state or SQLite setup.

### Planning-state runner artifact projection reports

Problem: projection reports could answer planning-state questions but could not
summarize compact runner outputs without agents inspecting runner artifacts by
hand.

Decision: let `planning_state rebuild-projection` and `report-projection` accept
explicit compact runner artifact JSON files or manifests, and add reports for
latest runs, failed phases by reason, and context pressure by phase.

Expected effect: agents can include bounded runner summaries in generated
projection databases while missing runner artifacts remain optional and
unrelated planning reports continue to pass; reports reject stale runner
summaries when projected runner artifacts or manifests change or disappear.

### Planning-state SQLite projection reports

Problem: agents could rebuild a bounded SQLite projection but still had no
compact command interface for common operational questions without touching SQL.

Decision: add `planning_state report-projection` for pending batches, missing
closeout evidence, and batch evidence lookup, with text and JSON output plus
projection identity, schema, stale-source, state-file, and policy blockers.
Closeout evidence indexes used for projected report facts are included in source
identity, and batch evidence reports preserve each commit evidence row.

Expected effect: agents can query generated projection databases safely while
Markdown/JSON planning artifacts remain canonical and reports stay read-only.

### Planning-state SQLite projection rebuild

Problem: agents needed a bounded SQLite projection but no command existed to
rebuild it from canonical planning facts without choosing a durable database
location.

Decision: add `planning_state rebuild-projection` with an explicit `--database`
target, project-policy target checks, source identity metadata, and bounded
projection tables for planning-state report facts.

Expected effect: report slices can consume a generated, delete-safe SQLite
projection while existing Markdown/JSON planning-state commands remain
independent of SQLite.

### Planning-state SQLite projection contract

Problem: SQLite projection work needed a stable, bounded contract before adding
commands that rebuild or query a database.

Decision: define the projection schema metadata, source identity, stale-database
blocker code, allowed report facts, and bounded row validation without selecting
or writing a durable database location.

Expected effect: later projection rebuild/report slices can validate generated
SQLite content against canonical Markdown/JSON state without storing Markdown,
prompts, transcripts, or long logs in the projection.

### Planning-state write-target policy enforcement

Problem: planning-state write helpers accepted explicit JSON state targets
without checking whether the target matched the project-owned state/projection
policy.

Decision: enforce resolved policy for state-file writes and closeout state-file
inputs, keep stdout and `/tmp` proof targets available for generated-only or
missing policy, and add `--projection-target` preflight checks before SQLite
projection writing exists.

Expected effect: durable state or projection commands stop with target-specific
diagnostics instead of silently writing to undeclared committed or local paths.

### Planning-state project policy reporting

Problem: read-only planning-state reports could validate Layout v1 Markdown but
did not expose the project-owned state/projection policy that future durable
state and projection writes must honor.

Decision: have `current` and `validate` resolve declared project policy into
text and JSON output, and add a read-only `--require-project-policy` preflight
for durable state-file or projection checks.

Expected effect: runner and workflow adapters can inspect stable policy facts
and missing/malformed policy blockers before implementing durable writes,
without forcing Markdown-only projects to declare state files.

### Planning-state project policy contract

Problem: future durable JSON state and projection work needed a reusable policy
boundary that did not assume every project commits planning state or uses the
same ignored local paths.

Decision: define project-owned state/projection policy vocabulary in Planning
Artifact Layout v1 and add schema tests for committed, ignored-local, external,
generated-only, none, missing, and unsupported policy cases.

Expected effect: later planning-state write and SQLite slices can require
compatible project policy before durable writes without hard-coding
`codex-config`, Graphify, or a universal state-file location.

### Planning-state migration pilot handoff

Problem: the migration pilot needed a durable handoff that explains how
bootstrap JSON state coexists with Markdown planning artifacts and prevents
agents from jumping straight to SQLite reporting.

Decision: document the migration workflow as companion state bootstrapping,
advance the planning-state program to migration-pilot closeout, and require
validation, review, and closeout evidence before marking PST-5 closed.

Expected effect: future agents can consume or build on the completed
migration-pilot evidence, keep `CURRENT.md` and ledgers human-readable, and
leave PST-6 deferred until the user requests the reporting projection batch.

### Planning-state migrated fixture validation

Problem: generated Layout v1 state fixtures could be schema-valid while still
drifting from active Markdown pickup state or missing registered artifact facts.

Decision: make `current` and `validate --state-file` cross-check migrated state
fixtures against active root/program `CURRENT.md` facts, registered active batch
pointers, duplicate artifact registrations, active-state contradictions, and
obligation record shape with stable blocker codes.

Expected effect: migration pilots can immediately validate generated state files
without closing or queueing batches, requiring live downstream project access,
or breaking Markdown-only planning roots.

### Planning-state bootstrap generation

Problem: agents could define the Layout v1 bootstrap contract but still had to
hand-write explicit JSON state fixtures from Markdown planning roots.

Decision: add `planning_state bootstrap-state` to generate a validated
`planning-state-tool-state` v1 fixture from root/program `CURRENT.md` files and
existing co-located batch artifacts, printing by default and writing only to an
explicit JSON target outside the planning root.

Expected effect: migration pilots can produce runner-consumable state fixtures
without rewriting live planning Markdown or inferring active batches from
historical flat files.

### Planning-state migration bootstrap contract

Problem: future bootstrap work needed an explicit boundary for which Layout v1
Markdown facts can become JSON state and which stale planning files remain only
compatibility evidence.

Decision: extend `planning-state-tool-state` version `1` with optional
bootstrap contract metadata that keeps root/program `CURRENT.md` active-first,
allows registered artifact and obligation facts in JSON, and forbids Markdown
writes from bootstrap fixtures.

Expected effect: migration generation can target a stable v1 fixture contract
without inferring queued batches from historical flat files or rewriting live
planning Markdown.

### Planning-state closeout workflow

Problem: future agents could validate or render closeout artifacts without a
compact handoff rule for when a batch is actually closed and what evidence a
human should inspect.

Decision: document closeout Markdown as a bounded pointer-first evidence index,
render this batch's closeout from explicit registered facts, and advance the
planning-state program handoff to PST-5 while keeping PST-6 deferred.

Expected effect: completed batches have a small evidence index instead of
transcripts or long logs, and the next planning-state work starts with migration
planning rather than SQLite projection or implicit state rewrites.

### Planning-state closeout rendering

Problem: closeout evidence indexes could be validated but still had to be
handwritten, which made required pointers and obligation evidence easy to miss.

Decision: add `planning_state render-closeout` to build bounded `closeout.md`
Markdown from explicit registered artifacts, evidence summaries, commits,
obligation facts, and cleanup classification. The command prints to stdout by
default and writes only to the registered batch closeout path when `--target`
is supplied.

Expected effect: runners and agents can produce compact closeout evidence
without transcript dumps or live planning-state mutation.

### Planning-state closeout validation

Problem: completed batches had a closeout evidence-index contract but no
runner-friendly preflight that checked a named `closeout.md` against explicit
state, artifact, and obligation facts.

Decision: add `planning_state validate-closeout` for registered closeout
artifacts, required closeout pointers, commit/validation/review evidence, and
closed-obligation evidence using compact blocker codes.

Expected effect: future closeout rendering and runner handoff slices can fail
early on missing evidence without parsing transcripts or mutating planning
Markdown.

### Planning-state obligations

Problem: batch selection and queue receipts could carry artifact facts but not
the cross-batch obligations that later closeout work must prove with bounded
evidence.

Decision: add first-class obligation records to explicit planning-state
fixtures and diagnostics, including IDs, owners, source batches, target batches
or close conditions, status, and evidence paths. `current` and `validate` can
load obligations with `--state-file`, and transition receipts include the
batch-relevant obligation facts.

Expected effect: future runner preflight and closeout work can consume
obligations from JSON protocol fields without parsing Markdown prose or
inferring closure from historical logs.

### Planning-state batch transitions

Problem: runners and agents could register dispatch/runway artifacts but had no
explicit command/file protocol for selecting a dispatch or queueing a runway
without editing Markdown.

Decision: add `planning_state select-batch` and `queue-batch` helpers that
validate explicit state fixtures, registered artifacts, same-batch paths, active
state conflicts, and optional ledger batch rows before writing state and JSON
transition receipts.

Expected effect: future runner preflight can consume transition receipts as an
explicit file protocol while existing `current` and `validate` diagnostics stay
read-only and Markdown-compatible.

### Planning-state artifact registration

Problem: agents still had to hand-allocate Layout v1 batch paths and could not
validate artifact registration facts before state-transition rendering exists.

Decision: add `planning_state allocate-batch` and `register-artifact` helpers
that compute canonical co-located batch artifact paths, validate registration
paths, and optionally write explicit JSON state fixtures without touching live
planning Markdown.

Expected effect: future write-transition slices can use deterministic path
facts for dispatch, runway, closeout, completed-slices, receipt, and output
artifacts while preserving existing `current` and `validate` behavior.

### Planning-state facts protocol

Problem: future runner adapters needed stable planning-state facts without
depending on Python imports, Markdown filename inference, or the default
human-readable diagnostics.

Decision: add an opt-in `--format json` protocol for `planning_state current`
and `planning_state validate`, with version negotiation, root/program facts,
warnings, blockers, validation messages, and exit-code semantics. Define
minimal future state and receipt fixture schema guards for write-transition
tests.

Expected effect: runners and fixtures can consume explicit command/file
protocols while existing text output remains compatible.

### Go runner interoperability boundary

Problem: future phase-runner work could treat the planned OSS Go runner as a
direct translation of the current Python files, or accidentally fold
`planning_state` diagnostics into the runner core.

Decision: document the contract-first boundary across runner and planning-state
plans. The future Go runner should interoperate through versioned schemas,
files, command protocols, fixtures, and exit codes, while `codex-config`
retains Codex prompts, planning policy, Graphify fixture policy, and
planning-state Markdown diagnostics.

Expected effect: future extraction batches should define shared protocols and
compatibility fixtures before repo skeleton work, package moves, or runner
integration.

### Planning-state read-only diagnostics

Problem: agents still had to infer active planning state from `CURRENT.md`
files, ledgers, redirects, and historical filenames before deciding what work
was actually selected or safe.

Decision: add the read-only `planning_state` `current` and `validate` workflow
for Layout v1 planning roots, keeping Markdown and JSON canonical while leaving
write transitions and SQLite deferred.

Expected effect: future agents can run compact diagnostics before broad
planning-tree scans and see active programs, next safe actions, stale-context
warnings, and validation errors without mutating planning artifacts.

### Planning CURRENT.md migration

Problem: `codex-config` had adopted Planning Artifact Layout v1 in reusable
workflow guidance, but its own active planning docs still relied on flat ledger
filenames and inline dispatch drafts for pickup.

Decision: add root and program `CURRENT.md` handoff files under `docs/plans/`,
move active ledgers into program-local `LEDGER.md` files, leave compact
redirects at the old flat paths, and promote the planning-state read-only core
dispatch into a co-located batch directory.

Expected effect: future agents can resolve active work from `CURRENT.md` first,
then read one program ledger or selected dispatch without scanning old flat
plans or archive files.

### Active-state batch planning fast path

Problem: after Planning Artifact Layout v1 migration, a fresh batch-planning
agent could still spend most of its context budget reading historical planning
files, generated reports, source modules, old redirect ledgers, and recent
commits before checking the active `CURRENT.md` handoff files.

Decision: make active-state pickup a reusable workflow rule across
`planning-artifacts`, `architecture-program-runway`, and Batch Runway
`create-spec` guidance. For ledger-driven next-batch/spec requests under Layout
v1, agents now read root and program `CURRENT.md` files first, honor existing
selected dispatches, active runways, and queued batches before selecting more
work, and broaden into ledgers or source packets only for a named unresolved
question.

Expected effect: future next-batch planning should usually need only the
instructions, root active state, relevant program active state, one ledger, and
one selected source packet instead of rediscovering active work from the whole
planning tree.

### Cleanup residue closeout

Problem: cleanup batches could leave test-only historical markers, migration
guards, old-vocabulary taxonomy, aliases, facades, or temporary scaffolding in
an ambiguous state when they were not obviously production compatibility paths.

Decision: add a generic cleanup-residue rule to `legacy-removal`,
`dead-surface-audit`, and Batch Runway reporting/review guidance. Residue must
now be removed, kept with a named reason, or deferred with a removal condition
and follow-up owner; final Batch Runway reports include cleanup residue
classification alongside remaining compatibility paths.

Expected effect: future agents should notice temporary cleanup aids before
closeout and avoid letting transitional test or taxonomy markers become
permanent by accident.

### Planning artifact layout

Problem: durable planning state could accumulate in flat `plans/` or
`planning/` directories, mixing ledgers, selected dispatch packets, Batch
Runway specs, closeouts, runner JSON receipts, and generated outputs in ways
that forced fresh agents to infer active state from filenames or memory.

Decision: add a reusable `planning-artifacts` skill with Planning Artifact
Layout v1. The convention requires each project to declare its planning root in
repo instructions, a local overlay such as `AGENTS.md`, an active spec, or
explicit user direction; then it defines program/workstream roots, program and
batch `CURRENT.md` handoff files, co-located batch directories, runner artifact
roots, generated-output roots, program-local archives, state vocabulary, naming
rules, and active-first migration guidance for roots that already contain a live
ledger plus substantial history. Wire `legacy-removal`,
`architecture-program-runway`, and `batch-runway` to read and follow the
convention when project instructions select it, while preserving existing
project-specific layouts as explicit compatibility rules. The installer now
expands manifest `requires` entries so installing one of those consumer features
also installs the shared `planning-artifacts` skill.

Expected effect: future workflow artifacts should have visible lineage from
program ledger to dispatch packet to runway spec to closeout, while raw runner
state and generated outputs stay outside durable planning docs.

### Agent completion notifications

Problem: terminal-only Codex work on Linux has no built-in mobile handoff path
when the Codex App host/mobile remote setup is unavailable, and generic alerts
do not say which project, branch, or final result needs attention.

Decision: add an opt-in `agent-notifications` feature with a principal-agent
`Stop` hook script, repo-owned global hook registration, example merge snippet,
and setup notes for ntfy, Pushover, or Apprise. The script reads Codex hook JSON
from stdin, derives project context from the session `cwd`, and keeps
notification tokens and private topics in environment variables instead of repo
files. Subagent completion hooks are intentionally not registered.

Expected effect: future Codex sessions can send phone-friendly completion
alerts for the principal agent that include project, branch, dirty count, cwd,
host, model, session, turn, and final-message context without sending separate
subagent completion noise.

### Default subagent delegation permission

Problem: main agents and workflow orchestrators could treat subagent use as
requiring fresh user permission even when configured subagent roles already
exist for implementation, review, exploration, or context management.

Decision: add a global instruction that main agents and workflow orchestrators
may use configured subagents without per-task permission when delegation is
useful, while preserving spawned worker, reviewer, and explorer role boundaries
that forbid recursive delegation.

Expected effect: future Codex sessions can route work through configured
subagents by default without the user having to restate that permission, and
without weakening role-specific Batch Runway constraints.

### Architecture-program legacy-removal dispatch

Problem: active legacy-removal programs can lose their removal intent between
program planning, selected dispatch, generated Batch Runway specs, review, and
closeout, which lets agents preserve legacy or add cleanup scaffolding by
inertia.

Decision: add a compact `architecture-program-runway` guardrail and optional
ledger/dispatch fields for classifying legacy surfaces, naming forbidden
scaffolding, stopping on unclassified legacy discoveries, and keeping deferred
or unreconciled legacy visible at closeout. Discovery and scoping remain with
`legacy-removal`; concrete slice execution remains with `batch-runway`; no
runner logic or new reference file was added.

Expected effect: future legacy-removal dispatch packets carry enough policy for
workers to execute classified removals and reviewers to flag unclassified
preservation without turning the workflow into a larger framework.

### Batch Runway review routing

Problem: the general `runway_reviewer` can miss specialized smells unless the
coordinator explicitly asks for the right review lens, and cleanup inventories
can accidentally become permanent contracts.

Decision: add trigger-based specialist review routing to Batch Runway guidance,
extend `runway_reviewer` reports with `lenses_applied`, and add an
`import_topology_reviewer` support agent for project-local import fallback,
direct-entrypoint, `sys.path`, and topology-only test risks. A local import
topology change routes only to that registered reviewer unless separate
legacy/dead-surface or test-retention evidence is present, and non-registered
contract, validation, and security lenses remain part of the final
`runway_reviewer` check. Specialist reviewers remain coordinator-owned support
reviewers; the final `runway_reviewer` verdict still gates the slice.

Expected effect: future slices can get targeted import-topology review when the
diff warrants it without turning every slice into a multi-reviewer committee or
preserving unsupported cleanup candidates as stable contracts.

### Legacy removal skill

Problem: legacy cleanup requests can jump directly to deletion or concrete
runway planning before obsolete behavior, compatibility requirements, canonical
owners, and batch boundaries are evidenced.

Decision: add a repo-owned `legacy-removal` skill for project-agnostic discovery
and scoping. The skill requires a compact Legacy Removal Ledger with evidence,
findings, canonical-model decisions, compatibility decisions, batch candidates,
and an optional selected dispatch packet, while leaving multi-batch program
management to `architecture-program-runway` and concrete execution specs to
`batch-runway`. The skill can now optionally load `dead-surface-audit` for
narrow evidence about test-retained surfaces, import topology, aliases, facades,
wrappers, or old module shape without absorbing that skill's workflow. It now
also states that tests are evidence, not authority, and requires legacy-removal
test evidence to be classified before preserving obsolete code to satisfy old
tests.

Expected effect: future cleanup work can distinguish unsupported internal
legacy behavior from required compatibility before agents create a concrete
runway spec or preserve old paths by inertia.

### Reusable workflow ownership guardrail

Problem: agents could treat a single project observation as a reason to add
project-name branches or hard-coded project paths directly into repo-owned
skills.

Decision: make the global instructions and repo instructions explicit that
repo-owned skills are reusable workflow code. Project-specific names, paths,
validation commands, cache locations, issue policy, and local planning layout
must come from project instructions, overlays, active specs, or repo-owned
reference docs instead.

Expected effect: future skill edits should generalize project needs into
discoverable project values or stop when those values are missing, instead of
adding branches such as `if project == graphify`.

### Batch Runway worker validation boundaries

Problem: test-only Batch Runway workers could infer that broad project refresh
commands belonged in their local validation because repository instructions may
say to refresh project indexes after code changes. That made narrow test slices
slower even when the coordinator later ran the correct validation.

Decision: tighten the generic Batch Runway contracts so project-level
integration harnesses, index/search/graph refreshes, generated-doc refreshes,
package installs, cleanup commands, and final validation are coordinator-owned
unless a worker handoff explicitly assigns them. The test-only profile now
forbids those per-slice costs by default and requires specs to opt in when a
project genuinely needs them.

Expected effect: future test-only and docs-only slices should stay focused and
fast while production slices can still run project-specific refresh and harness
commands when the spec or coordinator assigns them.

### Batch Runway workspace reconciliation

Problem: when a Batch Runway execution hit cross-slice worktree drift, an
unexpected commit, and stale review evidence, the recovery contract did not make
the coordinator's allowed cleanup actions explicit enough. That made manual
reverse patches look like implementation, even when the intent was to isolate
the slice before validation and review.

Decision: add a workspace-reconciliation lane to `execute-recovery-v1.md`.
Recovery now freezes commits until `HEAD`, status, staged files, unstaged files,
and the task-scoped diff basis are reconciled; tracked content cleanup must be
delegated to `runway_worker` or stopped for user direction. Review briefs and
compact reviewer reports now include the inspected `diff_basis`, and the
anomaly contract names unexpected `HEAD` movement, cross-slice drift,
coordinator content edits, and stale review evidence as first-class categories.

Expected effect: future executions should resolve dirty-file and stale-review
incidents through a visible recovery lane, without blurring the coordinator-only
boundary or accepting review evidence that does not match the current diff.

### Dead surface audit skill

Problem: shallow compatibility facades and legacy wrappers can look alive when
repo-local tests assert importability, alias identity, or module topology after
production callers have already moved to owner modules.

Decision: move the new `dead-surface-audit` skill into this repo and register it
as a repo-owned Codex feature. The skill requires agents to split caller
evidence into production, entrypoint, generated-artifact, documentation, and
test-only buckets, then apply the deletion test with and without tests before
classifying compatibility surfaces.

Expected effect: future architecture and test-quality reviews can identify code
kept alive only by migration-retention or topology-assertion tests, then decide
whether to delete, migrate tests first, keep a thin entrypoint, or ask for an
explicit compatibility contract decision.

### Port-by-contract skill

Problem: cross-language or product rewrites can accidentally preserve source
file layout, helper boundaries, and language-specific structure when what is
needed is an implementation-neutral behavior contract.

Decision: add a repo-owned `port-by-contract` skill. The skill rejects direct
translation as the default strategy, defines intake, contract distillation,
target design, runway handoff, and closeout modes, and documents the Python
architecture-program runner as an example source scope without hardcoding a
target product name. The skill now treats direct line-by-line translation as
outside the workflow, requires domain/context documents such as `CONTEXT.md`
during source intake, requires durable repo-local contract artifacts for
non-trivial ports, and requires agents to load and follow the selected runway
skill before creating a bounded handoff.

Expected effect: future rewrite planning can extract compact source contracts
first, then hand implementation work to `architecture-program-runway` or
`batch-runway` without asking a fresh agent to copy the source shape.

### GitHub issue writing policy

Problem: GitHub issue/comment bodies can become large Markdown design dumps, which makes them noisy and harder for agents to create, update, and review reliably.

Decision: add a global instruction to keep GitHub issues and comments compact and actionable. Detailed designs, schema sketches, long rationale, and logs should live in repo-owned planning or reference documents, with GitHub linking or naming those files instead.

Expected effect: future issue creation and comments stay GitHub-friendly while preserving detailed design work in versioned repo artifacts.

### Architecture-program-runway local runner

Problem: the accepted split-phase local runner design needed an implementation
that could drive architecture-program batches without keeping one long-lived
Codex thread or teaching the runner to parse program ledgers.

Decision: add a stdlib-only `architecture_program_runner.py` CLI, a local
runner protocol reference, and a phase-result JSON schema. The runner launches
fresh `codex exec` phases for `select-dispatch`, `create-spec`, `execute`, and
`closeout`; validates the final result and receipt with the same schema; keeps
JSON state; applies conservative dirty-worktree checks; and increments
`batches_completed` only after successful closeout. The
`architecture-program-runway` feature now also installs the runner script.
The skill documentation now separates skill invocation from CLI execution and
shows how to run the installed runner directly or ask an agent to run it.
Local runner invocation is now a protocol rule instead of prompt boilerplate:
skill-mediated requests default to `--all-batches` unless the user gives a
count, direct CLI defaults remain one batch, and the runner prints a final JSON
summary for agents to report. The phase-result schema now stays within the Codex
structured-output subset, including text-only compact validation/review
summaries; status/next-phase and state-dependent semantics remain enforced by
the Python runner so `codex exec --output-schema` accepts the schema before each
phase. The runner now accepts repeated `--env KEY=VALUE` arguments and passes
those overrides into every nested `codex exec` phase while preserving the base
environment; dry-run and phase prompts expose only override keys so projects can
provide validation-environment settings without making the runner
project-specific or bypassing canonical validation.
Stopped-phase resume now also recognizes evidence paths recorded in the last
stopped receipt for the same active phase, so a validation-blocked execute can
resume with its own in-progress code/test changes instead of being rejected by
the conservative worktree gate.
Execute-phase prompts and the local-runner protocol now require a
coordinator-shell probe for runner env override keys, coordinator-shell
canonical validation when env overrides are involved, and stopped-validation
receipts that name exact canonical commands plus env/cache visibility booleans
without disclosing override values.
The runner now also accepts `--execute-sandbox` so commit-capable Batch Runway
execute phases can use a broader nested Codex sandbox without broadening
select-dispatch, create-spec, or closeout phases.
Phase prompts and the local-runner protocol now enforce a single-level phase
model: phase agents must not run nested `codex exec`, recursively launch the
local runner, probe nested Codex availability, or create temporary `CODEX_HOME`
workarounds. Closeout telemetry is now explicitly file-based ledger, receipt,
or evidence updates.
New local-runner invocations now place state, receipts, manifests, and
browseable batch indexes under
`architecture-program-runs/<ledger-stem>/<run-id>/` by default. The runner
provides exact expected receipt paths to phase agents, rejects mismatched
receipt locations for structured runs, writes compact run and batch manifests
after successful phases, and includes `artifact_root` in the final summary.
`--resume` without `--state` now finds the latest structured run for the ledger
before falling back to the old flat state file, while explicit old `--state`
paths remain supported.
The artifact root is derived from the parent directory of `--program-ledger`,
not from a project-specific planning folder such as Graphify's `my-docs/`.
Structured runs now also write runner-owned telemetry under
`telemetry/run-telemetry.json` and `telemetry/phases/*.telemetry.json`.
Telemetry records direct runner measurements such as timestamps, elapsed time,
sandbox/model, observable exit code, prompt bytes, artifact sizes, context
budget status, and token summaries when an exact session JSONL path is
available; unattributed token data is marked missing instead of reconstructed.
Phase prompts now ask agents to write compact input inventories when broad
reads, large files, or subagent reports explain context growth.
The runner now names **Phase Environment** as the concept owner for
runner-supplied launch and prompt context. Prompt construction, command
construction, sandbox selection, env override labels, expected receipt/input
inventory paths, and artifact path facts now consume a single environment
object while preserving the Runner Facade and existing command behavior.
The runner now also names **Phase Transition** and **Change Allowance** as
concept owners. State advancement and terminal-state checks moved behind the
transition owner, while dirty-path parsing, expected-path calculation, prefix
matching, and worktree checks moved behind the allowance owner. The Runner
Facade keeps compatibility exports, and focused owner tests now carry the
concept behavior while broad runner tests retain thin integration coverage.
The runner now also names **Phase Contract** as the concept owner for
phase-prompt obligations. Prompt rendering consumes the contract catalog for
skill instructions, single-level boundary rules, shared receipt/result duties,
env-override validation duties, and per-phase next-phase requirements while
leaving launch facts, artifact paths, sandbox choices, and env-key labels with
Phase Environment.
Contract-owner tests now assert exact phase obligation catalogs, while command
tests focus on prompt integration between Phase Contract and Phase Environment.
The runner now also names **Phase Observation** as the concept owner for
observed execution metadata and runner-launched session attribution. It discovers
exact session JSONL paths only when they are uniquely identifiable; missing,
ambiguous, or errored attribution stays non-fatal; env override values are never
persisted; and artifact telemetry remains the owner for persistence and token
summary reporting.
The runner now enforces and documents **Input Inventory** as required
phase-agent reported context evidence for structured phases. Prompts require the
expected inventory path in `evidence_paths`, manifests and telemetry expose
inventory paths and sizes without embedding content, and the protocol clarifies
that the runner validates reported compact inventory files instead of
reconstructing consumed context from transcripts or session logs.
The runner now routes Codex phase execution through an internal **Worker**
adapter seam. The initial `codex-exec` worker keeps the existing prompt,
command, environment override, output-last-message, and observation behavior
unchanged while giving future worker types a single phase-result API.
The worker seam now also has an internal shell-command adapter proof that loads
a compact JSON phase result through the same validation, receipt, and transition
rules without exposing a public shell workflow CLI.

Expected effect: future architecture-program passes can be resumed from disk
artifacts and bounded by phase/state transitions while preserving the existing
`architecture-program-runway` versus `batch-runway` responsibility boundary.

### Architecture-program-runway goal runner prompt

Problem: the bounded `/goal` orchestration prompt was useful but lived only in
chat, making it hard to reuse, version, review, or tune as part of the
`architecture-program-runway` workflow.

Decision: add `references/goal-runner-v1.md` as the versioned reusable runner
protocol for `/goal`, automation, or local-runner experiments. The skill now
loads that reference for bounded runner use, keeping the actual `/goal` prompt
short while the loop, stop conditions, source-of-truth model, and telemetry
requirements live in the repo-backed skill.

Expected effect: future `/goal` trials can use a stable prompt file with
`program_ledger`, `max_batches`, and `execute_batches` inputs, then produce
comparable goal-run evaluation telemetry for tuning.

### Architecture-program-runway goal-run telemetry

Problem: `/goal` and future local runner experiments need evidence for tuning
the program-level loop, but ordinary finding closeout only records batch
outcomes and not whether the runner respected dispatch packets, bounded
execution, context discipline, and skill responsibility boundaries.

Decision: add a compact goal-run evaluation receipt to
`architecture-program-runway` and its program-ledger template. Runner-driven
passes now record the run ID, bounds, selected/started/completed batches, stop
reason, source-of-truth checks, responsibility checks, context observations,
orchestration anomalies, and tuning notes without pasting transcripts or logs
into the program ledger.

Expected effect: bounded `/goal`, automation, or local-runner experiments
produce enough telemetry to tune the orchestration workflow after real runs
while keeping the durable program ledger compact.

### Architecture-program-runway skill

Problem: broad architecture findings documents can contain multiple unrelated
or partially related workstreams, but `batch-runway` is intentionally scoped to
one concrete 3-5 slice execution batch. Agents needed a reusable layer for
maintaining the overarching ledger, grouping findings, selecting the next batch,
and reconciling findings after a runway closes.

Decision: add an `architecture-program-runway` skill with program-level modes
for intake, grouping, next-batch selection, concrete runway creation, closeout,
and reprioritization. Add a reusable program ledger template. The skill now
requires compact selected-batch dispatch packets, explicit agent-model
boundaries, context compression rules, and a batch queue with dispatch/spec
paths. It also normalizes closeout statuses to use `Open` instead of the
previous ambiguous `Still open` wording.

Expected effect: broad architecture reviews can become sequenced Batch Runway
work without turning into one giant batch or forcing future agents to re-read
and re-triage the raw findings document.

### Test quality review integration

Problem: `batch-runway` had no built-in way to request test-quality feedback for
specific slices without turning every batch into a full test audit.

Decision: add an optional per-slice `Test quality review` field to
`batch-runway` and compact YAML output support to `test-quality-review`.

Expected effect: future batches can request narrowly scoped test-quality review
when a slice needs it, while the default remains no extra review overhead.

### Context conflict guidance

Problem: project-level AGENTS.md instructions and local personal overlays can
both apply in Graphify, but agents needed a clear precedence rule.

Decision: add global instructions to read Graphify's committed AGENTS.md first,
then its local ignored `my-docs/AGENTS.md` overlay, treating local guidance as
additive and preferring upstream rules for project behavior.

Expected effect: agents should preserve upstream project intent while still
using local personal workflow guidance.

### Codex ownership guidance

Problem: repo-owned Codex config files are symlinked into `~/.codex`, so editing
the runtime path directly can hide the real source-controlled owner.

Decision: add global instructions requiring `scripts/codex_owner.py` before
editing `~/.codex` paths and treating linked repo-owned targets as work in
`/home/alacasse/src/codex-config`.

Expected effect: future edits to live Codex config should update the source repo
and changelog instead of silently mutating installed runtime files.

### Installed feature status

Problem: after the installer moved to repo-owned feature symlinks, there was no
single machine-readable record of which feature versions were installed.

Decision: write `~/.codex/codex-config/installed-features.json` after install and
expose a `--status` command in `scripts/install_codex_config.py`.

Expected effect: future agents can distinguish repo manifest ownership from the
active installed layout before editing Codex runtime files.
