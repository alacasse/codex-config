# Changelog

## Unreleased

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
