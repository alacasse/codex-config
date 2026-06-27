# Local Architecture Program Runner v1

Use this reference for the repo-owned local runner that drives one bounded
architecture-program pass through fresh `codex exec` processes.

The phase order is fixed:

```text
select-dispatch -> create-spec -> execute -> closeout
```

The runner is intentionally dumb. It does not parse or edit the program ledger,
does not infer domain correctness from diffs, and does not reconcile Git
history. It advances only from CLI arguments, JSON state, schema-valid phase
results, receipt paths, known artifact paths, process exit status, direct path
existence checks, and conservative `git status --porcelain` checks.

The runner is project-neutral. It does not know project-specific validation
tools, package managers, caches, network expectations, or fallback commands.
Projects that need environment variables for nested validation may pass them
explicitly with repeated `--env KEY=VALUE` arguments.

## Local Runner Invocation Rule

When the user asks to run the local architecture program runner, do not
manually perform runner phases in the current conversation. Invoke the local
runner CLI instead.

The runner is responsible for launching fresh `codex exec` processes for each
phase:

```text
select-dispatch -> create-spec -> execute -> closeout
```

The current conversation should only launch the runner and report the runner's
final summary after it stops.

## How To Use It

Skills are instruction bundles. They do not launch this runner by themselves,
but `$architecture-program-runway` defines the agent behavior for local runner
requests. The runner is the executable interface:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --max-batches 1
```

Run a dry preview first:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --dry-run \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --all-batches
```

Through the skill, minimal user prompts default to all executable batches unless
the user gives a count:

```text
Use $architecture-program-runway. Run the local runner on <program-ledger-path>.
```

```text
Use $architecture-program-runway and run the local architecture program runner
on this ledger: <program-ledger-path>
```

Direct CLI usage remains conservative: without `--all-batches` or an explicit
`--max-batches`, it runs at most one completed closeout. This is the only
default difference between direct CLI use and skill-mediated use.

Create the next spec for one batch but do not execute code:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --max-batches 1
```

Create, execute, and close out one batch:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --max-batches 1 \
  --execute-batches
```

When execute phases must create Batch Runway commits but the default sandbox
cannot write Git metadata, keep the base sandbox narrow and broaden only the
execute phase:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --max-batches 1 \
  --execute-batches \
  --sandbox workspace-write \
  --execute-sandbox danger-full-access
```

Treat `--execute-sandbox danger-full-access` as an explicit local workflow
escalation for commit-capable Batch Runway execution. Do not use it as a
general default for planning, spec creation, or closeout phases.

Create, execute, and close out every currently executable batch until no safe
next batch remains or a stop condition is hit:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --all-batches \
  --execute-batches
```

Resume with the same control arguments used for the original run:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --all-batches \
  --execute-batches
```

New runs store runner-owned artifacts under the program ledger directory:

```text
<ledger-dir>/architecture-program-runs/<ledger-stem>/<run-id>/
  run-state.json
  run-manifest.json
  telemetry/
    run-telemetry.json
    phases/
      01-select-dispatch.telemetry.json
  receipts/
    01-select-dispatch.json
  batches/
    <batch-id>/
      batch-manifest.json
      index.md
      receipts/
        02-create-spec.json
        03-execute.json
        04-closeout.json
```

The program ledger, selected dispatch packet, and generated Batch Runway spec
remain canonical files in their normal planning locations. The run directory
contains operational state, receipts, manifests, and browseable backlinks; it
does not snapshot or duplicate long-lived planning documents.

Structured runs also write runner-owned telemetry beside receipts instead of
expanding the phase receipt schema. Phase telemetry records direct runner
measurements such as start/end timestamps, elapsed seconds, model, sandbox,
exit code when observable, prompt bytes, artifact sizes, context-budget status,
and token summaries when an exact Codex session JSONL path is available. When
session token data is not attributable, token fields use `status=missing`
instead of reconstructed guesses. `run-telemetry.json` aggregates phase
telemetry paths, elapsed time, max context pressure, and final stop reason.

Structured phase prompts also provide an expected input inventory path. When
that path is present, the phase agent must write a compact JSON object there
and include the same project-relative path in `evidence_paths`. The runner
validates the file before phase transition and before manifest writes.

For structured runs, the runner provides an exact expected receipt path in each
phase prompt and rejects phase results that return a different `receipt_path`.
The first `select-dispatch` receipt is run-scoped because the batch ID is not
known before selection; later phase receipts are batch-local once the selected
batch exists. Additional `select-dispatch` receipts in an all-batches run use
the next run-scoped selection number instead of overwriting earlier selections.

`--resume` without `--state` looks for the latest structured run for the
program ledger, then falls back to the legacy flat
`architecture-program-run-state.json` if no structured run exists. Use
`--state <path>` to resume a specific run, including an old flat stopped run.

## Input Inventory Contract

Input Inventory is phase-agent reported context evidence. It records what the
phase consumed; the runner does not reconstruct it from transcripts, command
logs, session JSONL, prompt text, or newest files.

The inventory file is a compact JSON object with:

- `schema_version`: integer, currently `1`
- `phase`: the active phase name
- `primary_inputs`: array
- `broad_reads`: array
- `large_file_reads`: array
- `subagent_reports`: array

Arrays may be empty. Entries use compact project-relative paths and short
reasons, with optional command, byte-count, or role fields where relevant. The
inventory path itself is evidence: the final phase result must list it in
`evidence_paths` whenever the runner prompt names an expected inventory path.

Input Inventory is separate from receipts, phase observations, and telemetry.
Receipts remain exactly the phase-result JSON object. Phase observations and
telemetry record runner-measured process and artifact metadata. Manifests and
telemetry may link the inventory path and byte size, but must not embed raw
inventory content.

Pass project-supplied environment variables to every nested `codex exec` phase
when the validation environment requires them:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project <project-path> \
  --program-ledger <project-relative-ledger-path> \
  --max-batches 1 \
  --execute-batches \
  --env TOOL_CACHE_DIR=/tmp/project-tool-cache
```

Use one `--env KEY=VALUE` per variable. The runner preserves the current
process environment and applies these overrides only to the launched phase
processes. Dry-run diagnostics show override keys, not values.

When env overrides are present, phases that depend on them must verify the
keys from the phase coordinator shell before running validation. The probe
should record only whether each key is present and, for path-like values,
whether the path exists and is readable; it must not print or store override
values. Canonical validation commands that depend on these overrides must run
from the execute coordinator shell. Subagent-only validation output is useful
evidence, but it is not canonical proof for the local runner when env overrides
are involved.

Environment pass-through is not a validation bypass. Canonical project
validation must still pass inside the `execute` phase before Batch Runway can
commit and before the architecture runner can proceed to `closeout`.

## Batch Count Intent

When a user asks through `$architecture-program-runway`, infer the batch bound
before invoking the CLI:

- `run one batch` or `run 1 batch`: pass `--max-batches 1`.
- `run two batches`, `run 2 batches`, or `run max 2 batches`: pass
  `--max-batches 2`.
- `run 3 batches` or `run max 3 batches`: pass `--max-batches 3`.
- `run all batches`, `run the whole executable program`, or no explicit count:
  pass `--all-batches`.

`--all-batches` means continue while the ledger can produce a safe executable
next batch and the runner has not hit a stop condition. It does not mean force
all findings to `Closed`.

Use the skill manually instead of the runner when you want to stay in the
current conversation, inspect the ledger, select one batch, create one spec, or
close out one already-finished runway without launching nested `codex exec`
processes.

## Final Summary Contract

When the runner stops, it prints a final JSON summary. The invoking agent should
report that summary instead of reconstructing fields from conversation memory.

The summary contains:

- `state_path`
- `artifact_root`
- `run_telemetry_path`
- `last_phase_telemetry_path`
- `last_receipt_path`
- `stop_reason`
- `batches_completed`
- `active_batch`
- `dispatch_path`
- `spec_path`
- `commit_range`
- `validation_summary`
- `review_summary`

## Phase Contract

Every phase runs in a fresh `codex exec` process with
`--output-schema local-runner-phase-result.schema.json` and
`--output-last-message <tmp-result>`.

The local runner uses a single-level phase model. The outer Python runner is
the only process that launches phase-level `codex exec` commands. Once a phase
agent is running, it is already inside the runner-launched phase process.
Do not run `codex exec`, do not launch the local architecture program runner,
and do not probe nested Codex availability from inside any phase. Use existing
state, receipt, ledger, and evidence files only.

The phase-result JSON schema is intentionally limited to the Codex structured
output subset: object shape, required fields, primitive types, enums, arrays,
nullable fields, and `additionalProperties: false`. Cross-field and
state-dependent semantics live in the Python runner validation, not in schema
composition or conditional keywords.

`validation_summary` and `review_summary` are compact strings or `null`. Put
detailed structured evidence in referenced files and list those paths in
`evidence_paths`.

Every phase must:

- write a phase receipt file;
- use the exact runner-provided expected receipt path when the prompt names one;
- return the same JSON object as its final schema-valid result;
- include `receipt_path` in that JSON object;
- write that exact object to `receipt_path`;
- validate against `local-runner-phase-result.schema.json`.

There is no separate receipt schema in v1. The runner validates both the
captured final result and the receipt file content with the same phase-result
schema, then checks that they are the same object.

Required fields keep a stable shape, but stopped or early phases may use `null`
for fields that are not applicable, including `stop_reason`, `batch_id`,
`dispatch_path`, `spec_path`, `commit_range`, `validation_summary`, and
`review_summary`. `evidence_paths` defaults to `[]` when no evidence applies.

`status` and `next_phase` must be consistent:

- `status=completed` advances to the expected next phase for the runner state,
  or to `done` where the current mode permits it.
- `status=stopped` uses `next_phase=stopped`.
- `status=failed` uses `next_phase=stopped`.
- Any contradiction is malformed output and stops the runner safely.

## Phase Responsibilities

`select-dispatch` uses `$architecture-program-runway` to select exactly one
next executable batch and create or refresh one compact dispatch packet. It
does not create a Batch Runway spec or execute code.

`create-spec` uses `$architecture-program-runway` in `create-next-runway` mode.
It reads the dispatch packet as primary input, reads only minimum ledger
context, creates exactly one concrete `$batch-runway` spec, and does not
execute code.

`execute` uses `$batch-runway execute-spec` on exactly the generated spec. It
preserves normal `runway_worker` and `runway_reviewer` delegation. Execution
success does not increment `batches_completed`.

When `execute` stops on validation, receipts should summarize the canonical
command lines attempted, whether runner env override keys were present in the
command environment, whether path-like override values existed and were readable
without disclosing values, whether fallback validation was attempted and passed,
the likely failure class such as DNS/cache/permission/lockfile/test failure,
and any dirty files remaining.

`closeout` uses `$architecture-program-runway closeout-runway` to reconcile
compact execution evidence into the program ledger. It does not paste logs into
the ledger. Closeout telemetry is file-based closeout telemetry: write compact
ledger, receipt, or evidence-file updates directly, without launching another
Codex process, probing runtime availability, or creating a temporary
`CODEX_HOME`. `batches_completed` increments only after successful closeout.

## Worktree Safety

Before every phase, the runner runs:

```bash
git status --porcelain
```

It stops before launching the phase when dirty files are unrelated to the
current phase or cannot be confidently classified as expected. V1
classification is conservative and path-based.

After `execute`, project code changes must have been committed by the Batch
Runway workflow. Only explicitly expected uncommitted evidence, receipt, or
runner-state files may remain. Unexpected dirty project files stop the runner
before `closeout`.

Before `closeout`, use compact evidence: commit range, validation summary,
review summary, spec path, receipt paths, and explicit evidence paths from the
phase result. The runner must not become a smart Git reconciliation tool.

## Control Semantics

`--stop-after-phase <phase>` means run and complete the named phase, persist the
phase receipt and runner state, then stop before launching the next phase. It
does not mean stop before the named phase.

`--resume` loads JSON state and resumes from `active_phase`. If an expected
artifact is missing or contradicts state, stop safely instead of guessing.

Use JSON state for v1. Do not add YAML state, a daemon, a scheduler, a UI, a
ledger parser, or a domain-specific project runner.
