# Local Architecture Program Runner Plan

## Summary

Build a repo-owned local runner that drives architecture-program batches without
a long-lived Codex thread. The runner launches fresh `codex exec` processes for
each phase:

```text
select-dispatch -> create-spec -> execute -> closeout
```

The runner stays intentionally dumb. It never parses or edits the program
ledger directly. It advances only from CLI arguments, JSON state,
schema-valid phase results, receipt paths, known artifact paths, process exit
status, simple filesystem checks, and simple `git status` checks.
Domain phase details live in the phase-written receipts, not in runner-created
ledger interpretations or synthetic domain summaries.

The main design correction from the `/goal` experiment is that selecting a
batch and creating a full Batch Runway spec must be separate fresh Codex runs.
This reduces coordinator context growth and gives clean resume boundaries.

## Scope

Implement only:

- `skills/architecture-program-runway/references/local-runner-v1.md`
- `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`
- `scripts/architecture_program_runner.py`
- runner tests
- feature version and changelog updates
- installed feature metadata refresh after the version bump

Do not implement a local daemon, scheduler, UI, YAML state, ledger parser, or
domain-specific Graphify runner in v1.

## Interfaces

### Runner CLI

Add:

```bash
scripts/architecture_program_runner.py \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 2 \
  --execute-batches \
  --state my-docs/plans/architecture-program-run-state.json
```

Arguments:

- `--project`: required path passed to `codex exec --cd`.
- `--program-ledger`: required project-relative ledger path.
- `--max-batches`: optional positive integer, default `1`.
- `--execute-batches`: optional flag, default false.
- `--state`: optional project-relative or absolute JSON state path. If omitted,
  default to `<program-ledger-dir>/architecture-program-run-state.json`.
- `--sandbox`: optional Codex sandbox value, default `workspace-write`.
- `--model`: optional pass-through to `codex exec --model`.
- `--dry-run`: print planned phase commands and prompts without launching Codex
  or writing state.
- `--resume`: load the existing state file and resume from `active_phase`.
- `--stop-after-phase`: one of `select-dispatch`, `create-spec`, `execute`,
  `closeout`. This means run and complete the named phase, persist the phase
  receipt and runner state, then stop before launching the next phase. It does
  not mean stop before the named phase.

Use fresh `codex exec` processes. Do not use `/goal`. Do not use
`codex exec resume` by default.

### JSON State

Use JSON state for v1. No PyYAML dependency.

```json
{
  "schema_version": 1,
  "runner_version": "local-runner-v1",
  "project": "/home/alacasse/projects/graphify",
  "program_ledger": "my-docs/plans/install-sandbox-architecture-findings.md",
  "max_batches": 2,
  "execute_batches": true,
  "batches_completed": 0,
  "active_phase": "select-dispatch",
  "active_batch_id": null,
  "dispatch_path": null,
  "spec_path": null,
  "last_receipt_path": null,
  "last_codex_session": null,
  "last_phase_status": null,
  "stop_reason": null,
  "updated_at": null
}
```

Rules:

- `active_phase` enum: `select-dispatch`, `create-spec`, `execute`, `closeout`.
- `batches_completed` increments only after a successful `closeout`.
- `execute succeeded != batch completed`.
- `closeout succeeded = batch completed`.
- State writes are atomic: write to a temporary sibling file, then replace.

### Phase Result Schema

Add `local-runner-phase-result.schema.json`.

Required enum fields:

- `status`: `completed`, `stopped`, or `failed`.
- `phase`: `select-dispatch`, `create-spec`, `execute`, or `closeout`.
- `next_phase`: `select-dispatch`, `create-spec`, `execute`, `closeout`,
  `done`, or `stopped`.

Required core fields:

- `status`
- `phase`
- `next_phase`
- `stop_reason`
- `program_ledger`
- `batch_id`
- `dispatch_path`
- `spec_path`
- `receipt_path`
- `commit_range`
- `validation_summary`
- `review_summary`
- `evidence_paths`

Keep the required field set stable, but allow nullable values when a field is
not applicable or a phase stops before creating the corresponding artifact:

```json
{
  "stop_reason": null,
  "batch_id": null,
  "dispatch_path": null,
  "spec_path": null,
  "commit_range": null,
  "validation_summary": null,
  "review_summary": null,
  "evidence_paths": []
}
```

`evidence_paths` defaults to an empty array when no evidence paths apply.
`receipt_path` remains required and should be a non-null path for every
schema-valid phase result. A stopped or failed phase should still write a
receipt explaining the stop or failure in compact machine-readable form.

Status and `next_phase` must be consistent:

- `status=completed` may advance to the normal next phase for the current
  state or to `done`.
- `status=stopped` must use `next_phase=stopped`.
- `status=failed` must use `next_phase=stopped`.
- Contradictory combinations are malformed phase results and must stop safely.

Invalid examples:

```json
{
  "status": "failed",
  "next_phase": "execute"
}
```

```json
{
  "status": "stopped",
  "next_phase": "closeout"
}
```

The runner stops safely on missing, malformed, contradictory,
schema-invalid, or nonzero-exit phase output.

### Phase Receipts

The Codex phase writes the phase receipt file. The Codex phase returns the
same JSON object as its final schema-valid result and writes that object to the
receipt file.

The receipt file content must also validate against
`local-runner-phase-result.schema.json`. The runner validates both the captured
final phase result and the receipt file content with the same schema. Do not
add a separate receipt schema in v1.

The runner validates that `receipt_path` exists. It may store, copy, or
reference the receipt path in runner state, but it must not invent domain
receipt content itself. The runner only validates paths, schemas, exit status,
and state transitions.

## Phase Behavior

### select-dispatch

Prompt uses `$architecture-program-runway`.

Required behavior:

- Read the program ledger.
- Select exactly one next executable batch.
- Create or refresh one compact dispatch packet.
- Do not create a Batch Runway spec.
- Do not execute code.
- Write a compact machine-readable receipt.

Expected output:

- `batch_id`
- `dispatch_path`
- `next_phase=create-spec` when completed

Allowed dirty paths:

- dispatch artifact path returned by the phase
- runner receipt path
- runner state path

### create-spec

Prompt uses `$architecture-program-runway` in `create-next-runway` mode.

Required behavior:

- Read the dispatch packet as the primary input.
- Read only minimum ledger context needed for status and evidence.
- Create exactly one concrete `$batch-runway` spec.
- Do not execute code.
- Write a compact machine-readable receipt.

Expected output:

- same `batch_id` as state
- same `dispatch_path` as state
- `spec_path`
- `next_phase=execute` if `execute_batches=true`
- `next_phase=done` if `execute_batches=false`

Allowed dirty paths:

- expected spec path returned by the phase
- runner receipt path
- runner state path

### execute

Prompt uses `$batch-runway execute-spec`.

Required behavior:

- Read and execute exactly the generated spec.
- Preserve normal `runway_worker` and `runway_reviewer` delegation.
- Stop on validation, review, missing project values, dirty-file conflict, or
  active spec stop conditions.
- Write a compact machine-readable receipt.

Expected output:

- same `batch_id`
- same `spec_path`
- `commit_range`, `validation_summary`, `review_summary`, and `evidence_paths`
  when available
- `next_phase=closeout` when completed

Do not increment `batches_completed` after execute.

Allowed dirty paths:

- the active spec ledger/archive if the spec writes progress
- generated validation artifacts that the project explicitly allows
- no unrelated uncommitted code changes after a successful execution phase

### closeout

Prompt uses `$architecture-program-runway closeout-runway`.

Required behavior:

- Reconcile compact execution evidence back into the program ledger.
- Do not paste execution logs into the ledger.
- Update runner telemetry receipt.
- Write a compact machine-readable receipt.

Expected output:

- same `batch_id`
- program ledger path
- closeout receipt path
- `next_phase=select-dispatch` if more batches are allowed and the ledger has
  a next ready batch
- `next_phase=done` if `max_batches` is reached or no next batch is ready
- `next_phase=stopped` if blocked

Increment `batches_completed` only when `status=completed`.

Allowed dirty paths:

- program ledger path
- closeout receipt path
- runner state path

## Safety Model

### Preflight Worktree Check

Before every phase, run:

```bash
git status --porcelain
```

Stop before launching the phase if dirty files are unrelated to the current
phase or cannot be confidently classified as expected for the current phase.
Prefer stopping safely over guessing.

V1 classification is conservative and path-based:

- `select-dispatch`: only dispatch artifacts, runner receipts, and runner state.
- `create-spec`: only expected spec path, runner receipts, and runner state.
- `execute`: proceed only from a clean or phase-consistent state.
- `closeout`: only program ledger, closeout receipt, and runner state.

If classification is unclear, stop safely.

The runner should not become a smart git reconciliation tool. Do not infer
semantic ownership from diffs, parse commits to classify uncommitted changes,
or edit the program ledger directly to compensate for dirty state.

After `execute`, require project code changes to have been committed by the
Batch Runway workflow. Allow only explicitly expected uncommitted
evidence, receipt, or runner-state files. If execution leaves unexpected dirty
project files, stop before `closeout`.

Before `closeout`, prefer committed execution changes and compact evidence:
commit range, validation summary, review summary, spec path, receipt paths,
and other explicit evidence paths from the phase result.

### Resume And Idempotence

With `--resume`:

- If the expected artifact already exists and matches current state, continue
  to the next phase.
- If the expected artifact is missing, rerun the current phase.
- If the artifact exists but contradicts runner state, stop safely.
- If state says a phase completed but required receipt is missing or malformed,
  stop safely.
- If a dispatch already exists for `active_batch_id`, do not create a different
  dispatch for the same batch unless the prior phase explicitly marked it stale.
- If a spec already exists for `active_batch_id`, do not create a different spec
  for the same batch unless the prior phase explicitly marked it stale.

The runner does not inspect program ledger contents to decide correctness.
Domain correctness remains in `architecture-program-runway` and `batch-runway`.

## Prompt Generation

The script should generate prompts internally for each phase.

Every prompt must include:

- project path
- program ledger path
- state path
- current phase
- expected artifact paths from state when known
- output schema path
- instruction to return schema-valid JSON as the final response
- instruction to write a compact receipt and return `receipt_path`

Use `codex exec --output-schema <schema> --output-last-message <tmp-result>`.
Prefer `--json` only for diagnostics; the runner should use the final
schema-valid result as the phase contract.

## Tests

Add tests for:

- CLI defaults.
- JSON state load/save.
- Prompt generation for all four phases.
- Phase transitions.
- `status` / `next_phase` consistency.
- `--stop-after-phase`.
- `--max-batches`.
- Invalid `status`.
- Invalid `phase`.
- Invalid `next_phase`.
- Nullable execution evidence fields.
- Nullable stopped or early-phase artifact fields.
- Missing required schema fields.
- `batches_completed` increments only after successful `closeout`.
- Preflight dirty-worktree stop behavior.
- Post-execute unexpected dirty project files stop before `closeout`.
- Resume with matching existing artifact.
- Resume with missing artifact.
- Resume with contradictory artifact/state.
- Missing receipt stops safely.
- Malformed receipt stops safely.
- Receipt path exists and receipt content is schema-valid.
- Nonzero `codex exec` exit stops safely.

Validation commands:

```bash
python3 -m unittest
python3 -m json.tool codex-features.json >/dev/null
python3 -m json.tool skills/architecture-program-runway/references/local-runner-phase-result.schema.json >/dev/null
git diff --check
scripts/architecture_program_runner.py --dry-run \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1
```

## Implementation Order

1. Add `local-runner-v1.md` protocol reference.
2. Add `local-runner-phase-result.schema.json`.
3. Add runner state and schema helpers in `scripts/architecture_program_runner.py`.
4. Add dry-run prompt generation.
5. Add phase execution through `codex exec`.
6. Add preflight worktree checks.
7. Add resume/idempotence checks.
8. Add tests.
9. Update `CHANGELOG.md`.
10. Bump `architecture-program-runway` in `codex-features.json`.
11. Refresh installed feature metadata.

## Implementation Risk

- Dirty-worktree classification is the main risk. Keep v1 conservative.
- `codex exec` output may be malformed despite `--output-schema`; fail closed.
- Existing ignored planning files may not appear in `git status`; use direct
  path existence checks for expected artifacts.
- Execution phases may commit code, so post-execute state should rely on
  schema-valid receipts and commit evidence rather than dirty diff inspection
  alone.
