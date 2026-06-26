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

## Phase Contract

Every phase runs in a fresh `codex exec` process with
`--output-schema local-runner-phase-result.schema.json` and
`--output-last-message <tmp-result>`.

Every phase must:

- write a phase receipt file;
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

`closeout` uses `$architecture-program-runway closeout-runway` to reconcile
compact execution evidence into the program ledger. It does not paste logs into
the ledger. `batches_completed` increments only after successful closeout.

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
