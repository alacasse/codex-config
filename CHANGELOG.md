# Changelog

## Unreleased

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
phase.

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
for findings intake, batch grouping, next-batch selection, concrete runway
creation, runway closeout, and reprioritization. The skill keeps execution
contracts in `batch-runway` and adds a compact program-ledger template for
batch queues and finding statuses. The selected batch now has an explicit
brief/dispatch packet so a fresh `batch-runway create-spec` session can consume
bounded context instead of re-reading the raw findings document or re-deriving
the whole program. Multi-batch programs should store that dispatch packet in a
separate linked file, and ledgers should retain only compact closeout evidence.
The ledger template keeps the selected-dispatch section as a pointer by default
and moves the full YAML shape into a dispatch-packet template.

Expected effect: future architecture review documents should stay durable
across multiple batches without encouraging one oversized runway or losing
deferred findings, while each batch can start from a compact handoff artifact
without overloading a fresh spec-creation agent.

### Batch-runway orchestration anomalies

Problem: during Batch Runway execution, suspicious coordinator or
subagent-lifecycle behavior could be noticed only by rereading execution
details, making workflow friction easy to miss after the slice moved on.

Decision: add a compact `orchestration_anomalies` log to the Batch Runway
execution, reporting, finalization, and ledger contracts. The log captures
accidental extra agent spawns, wrong roles, unusable support output, malformed
subagent reports, confusing controls, ambiguous or flaky validation, escalation
friction, and near contract violations, while excluding routine logs, clean
reviews, and implementation chronology. Final batch reports always print an
`Orchestration Anomalies` section, using `orchestration_anomalies: []` when none
were recorded.

Expected effect: future executions should preserve easy telemetry for improving
the workflow without expanding the routine slice record into a transcript.

### Batch-runway cross-slice seam handoffs

Problem: create-spec output could name adjacent architectural slices but leave
their dependency implicit, allowing a later slice to create a parallel seam or
duplicated implementation instead of consuming the boundary introduced by an
earlier slice.

Decision: require specs to make producer/consumer handoffs explicit when
adjacent slices introduce and then consume a shared seam, owner module,
projection API, or compatibility facade. The producing slice should name the
single owner/API, downstream slices should consume it, and acceptance or stop
conditions should fail bypasses or duplicate implementations.

Expected effect: future runway specs should preserve independent slice
testability while making cross-slice architectural invariants executable.

### Batch-runway worker role boundary

Problem: spawned `runway_worker` agents could read coordinator-facing Batch
Runway delegation rules and conclude they needed to spawn another coding
subagent before implementing their assigned slice.

Decision: make the execution contract and compact worker briefs explicitly
role-scoped. A spawned `runway_worker` is already the required coding subagent,
must implement only its assigned slice, and must not spawn, delegate to, or wait
on additional subagents. Validation, review delegation, ledger updates, commits,
and subagent lifecycle remain coordinator-owned.

Expected effect: routine slice workers should stop blocking on recursive
delegation while the coordinator-only workflow and separate reviewer requirement
remain intact.

### Batch-runway coordinator read discipline

Problem: after reference-loading and compact-reporting optimizations, routine
Batch Runway executions could still grow orchestrator context through broad
coordinator-side memory, source, test, prior-spec, and architecture exploration.

Decision: make execute-mode coordinator read limits explicit and restore
`fast_explorer` to the routine hot path as the optional read-only investigation
agent. The coordinator should carry active orchestration state, compact
validation outputs, compact subagent reports, and commit receipts; broad
exploration should normally be delegated and retained only as compact,
file-referenced YAML findings.

Expected effect: long-running executions keep the main agent focused on
orchestration while preserving a safe escape hatch for read-only discovery,
reducing avoidable coordinator context growth without reloading the full
subagent-brief reference for routine slices.

Follow-up: refine `fast_explorer` as a batch-scoped read amortization tool.
Prefer one support investigation for related adjacent slices, pass workers and
reviewers only compact findings or artifact paths, and keep live support-agent
handles under coordinator ownership.

### Batch-runway execution hot path

Problem: normal `batch-runway` slice execution still loaded the full execution
contract, reporting contract, ledger policy, validation catalog, and subagent
brief references even when the slice was routine and clean.

Decision: add `execute-slice-core-v1.md` as a hot-path projection of the
canonical contracts, split recovery and finalization into separate references,
and split validation profiles into per-profile files. Keep the full references
canonical for contract changes, compatibility audits, planning, and non-routine
execution.

Expected effect: routine execution can load the project values reference, the
execution core, and only the selected validation profile while preserving
coordinator-only execution, compact reporting, commit receipts, ledger recovery,
and compatibility with existing specs.

### Batch-runway progressive disclosure

Problem: `batch-runway` had become a single large skill file containing the
dispatcher, execution contract, reporting contract, ledger policy, validation
profiles, mode procedures, and subagent prompt templates. That made every skill
invocation pay for details that only some modes needed.

Decision: shrink `SKILL.md` into a mode dispatcher and context-discipline guide,
then move detailed standard contracts, reporting rules, ledger retention,
validation profiles, create/execute procedures, subagent briefs, and
test-quality integration into one-level `references/` files. Lean specs now
carry reference paths or compact contract capsules when subagents need them.

Expected effect: future Batch Runway invocations should load less context by
default while preserving the same coordinator-only execution contract,
per-slice validation, separate review, compact reporting, and resume behavior.

### Generic batch-runway project values

Problem: `batch-runway` carried Graphify-specific defaults for plan storage,
installer sandbox validation, summary artifacts, and graph refresh even though
the skill should be reusable across repositories.

Decision: replace those hard-coded defaults with a generic project-values gate.
Agents must resolve planning location, validation profiles, harness commands,
artifact paths, summary reads, index refreshes, commit rules, and dirty-file
constraints from the current repo's instructions, local overlays, the spec, or
explicit user direction. Missing required values now stop execution instead of
being guessed.

Expected effect: `batch-runway` remains portable while still preserving strict
per-project behavior when a repo defines the concrete values locally.

### Minimal test-quality review integration

Problem: `test-quality-review` should be usable inside `batch-runway` without
turning every slice review into a broader audit or adding automatic blocking,
issue creation, ledger state, ADR generation, or remediation planning.

Decision: add an optional per-slice `Test quality review: none | delta-only |
focused | full-audit` setting to `batch-runway`. Omitted settings default to
`none`; explicit requests invoke `$test-quality-review` in the requested mode
and include compact YAML findings in reviewer output. Add compact YAML output
guidance to `test-quality-review` for automation/reviewer use.

Expected effect: runway specs can opt into qualitative test review where useful
while preserving current execution behavior and keeping future disposition,
issue-tracking, full-audit, and ADR workflows out of the minimal integration.

### Test-quality-review skill

Problem: agents reviewing tests needed a reusable way to judge confidence from
behavioral protection, regression coverage, assertion strength, mocking quality,
fixture complexity, and test friction without reducing quality to coverage
percentages or tying the workflow to `batch-runway`.

Decision: add a standalone `test-quality-review` skill with delta-only,
focused, and full-audit modes, explicit finding criteria, design-signal
analysis, scope limits, and a fixed report format. Declare it as its own
repo-owned feature in `codex-features.json`.

Expected effect: future reviewers, architects, implementation agents, and
automation can evaluate test quality consistently while keeping findings
actionable and independent from multi-slice runway execution.

### Batch-runway compact reporting and retention

Problem: `batch-runway` needed convergence discipline, but routine slice
reports, commit receipts, ledger rows, and subagent responses could accumulate
too much narrative context across long multi-batch refactors.

Decision: replace routine full convergence reporting with a compact YAML
convergence block, add `Compact Report Contract v1` for workers, reviewers, and
commit receipts, add `Standard Ledger Retention v1`, and document explicit
information lifetime rules. The full convergence template is retained only for
expanding scope, significant uncertainty, blockers, or final batch reports.

Expected effect: future runway executions should preserve coordination quality,
audit references, and recovery points while carrying much less historical
implementation detail in orchestrator context.

### Batch-runway agent output limits

Problem: the `runway_worker` and `runway_reviewer` roles could satisfy their
tasks with human-readable prose, which made clean subagent reports larger than
the coordinator needed.

Decision: update both agent prompts to return structured YAML, forbid
implementation history and reasoning narrative, and cap clean worker/reviewer
reports at 12 and 10 lines respectively. Expanded output is reserved for
findings, blockers, failed validation, or escalation.

Expected effect: coding and review subagents remain bounded to their role while
the coordinator receives predictable, compact state for long-term retention.

### Lean batch-runway contracts

Problem: `batch-runway` specs repeated the full execution contract, validation
commands, and subagent briefs in every runway, increasing token use while still
needing strict coordinator-only, sandbox, and commit discipline.

Decision: add lean/full runway density modes, versioned standard contract and
ledger references, reusable validation profiles, compact subagent brief formats
with absolute spec paths, explicit fresh install-sandbox output guidance, and
move the skill UI metadata from the legacy root `openai.yaml` path to
`agents/openai.yaml`.

Expected effect: future runway specs can stay smaller for mechanical work while
preserving the agent behavior that matters: coordinator-only execution,
separate coding/review agents, per-slice commits, guarded sandbox validation,
stable interpretation of older contract references, and current skill metadata
layout.

### Declared vs installed Codex ownership

Problem: `scripts/codex_owner.py` treated any path matching a feature manifest
entry as owned by this repository, even when the runtime `~/.codex` path was a
standalone copy instead of the expected symlink.

Decision: split manifest declaration from active installation state. The owner
report now includes `manifest_owner`, `installed_owner`, `status`, and `reason`,
with non-linked targets classified as `missing`, `unlinked_copy`,
`wrong_symlink`, `conflict_file`, or `conflict_directory`.

Expected effect: agents no longer get a false signal that editing a copied
runtime path will update codex-config. They can see when a feature is declared
by this repository but not currently linked from `~/.codex`.

### Linked config ownership detection

Problem: repo-owned files can be edited through their installed `~/.codex`
symlink while the agent is working in another project, making it easy to miss
the codex-config changelog and git status expectations.

Decision: add `scripts/codex_owner.py` and global instructions for checking
whether a `~/.codex` path resolves to this repo. Repo-owned links now carry a
clear expectation to update `CHANGELOG.md` for meaningful workflow changes and
report this repo's git status.

Expected effect: agents can safely tune linked skills, agents, rules, and
instructions from any project while still treating the edit as codex-config
work.

### Vendor-owned Graphify skill

Problem: `graphify` is vendor-owned and should not be represented as a local
override in this repo's feature manifest.

Decision: remove the local `graphify` feature from `codex-features.json`; the
vendor installer remains responsible for `~/.codex/skills/graphify`.

Expected effect: this repository owns only its explicit linked features, while
vendor-owned skills can manage themselves in the final `~/.codex` directory.

### Versioned feature installer

Problem: `install.sh` was a set of hard-coded symlinks, which made it easy for
the live Codex layout to drift from the repository and hard to add new workflow
features deliberately.

Decision: add a manifest-driven installer. `codex-features.json` now defines
versioned Codex features and their links, while `install.sh` delegates to a
Python installer that supports listing, dry runs, selective installs, conflict
detection, and installed-version state.

Expected effect: new skills, agents, rules, and instruction bundles can be
versioned as features and installed reproducibly without rewriting installer
logic each time.
