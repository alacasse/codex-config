# Changelog

## Unreleased

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
