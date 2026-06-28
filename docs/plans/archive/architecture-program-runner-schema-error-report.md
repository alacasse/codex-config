# Architecture Program Runner Schema Error Report

## Summary

On 2026-06-26, running the local architecture program runner against the
Graphify install-sandbox architecture ledger failed before the first runner
phase could start.

The runner attempted to launch a fresh `codex exec` process for the
`select-dispatch` phase with `--output-schema` pointing at
`skills/architecture-program-runway/references/local-runner-phase-result.schema.json`.
Codex rejected that schema at request-validation time because it contains a
top-level `allOf`, which is not accepted by the current OpenAI structured output
schema subset used by `codex exec --output-schema`.

No architecture batch was selected, no dispatch packet was written, no Batch
Runway spec was created, no code was executed, and no closeout happened.

## Intended Operation

The invoking Graphify request was to run the first selected architecture program
batch from:

```text
/home/alacasse/projects/graphify/my-docs/plans/install-sandbox-architecture-findings.md
```

The command invoked was:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

Expected runner flow:

```text
select-dispatch -> create-spec -> execute -> closeout
```

For this ledger, the selected work was expected to be the first queued batch:

```text
Catalog boundary reassessment
```

with the existing concrete spec path:

```text
my-docs/plans/install-sandbox-catalog-boundary-runway.md
```

Because `--execute-batches` was set, the runner was expected to create or
refresh the dispatch packet, create or confirm the concrete Batch Runway spec,
execute that spec through `$batch-runway execute-spec`, then reconcile closeout
evidence back into the architecture findings ledger.

## What Actually Happened

The runner entered the first phase, `select-dispatch`, and launched `codex exec`
with:

```text
--output-schema /home/alacasse/projects/codex-config/skills/architecture-program-runway/references/local-runner-phase-result.schema.json
--output-last-message <tmp-result>
```

The nested `codex exec` process exited with status `1` before the agent phase
could execute. The API rejected the schema:

```text
invalid_request_error
code: invalid_json_schema
message: Invalid schema for response_format 'codex_output_schema':
In context=(), 'allOf' is not permitted.
param: text.format.schema
status: 400
```

The runner then failed closed, wrote its JSON state, and printed a final summary
with no active batch artifacts:

```json
{
  "active_batch": null,
  "batches_completed": 0,
  "commit_range": null,
  "dispatch_path": null,
  "last_receipt_path": null,
  "review_summary": null,
  "spec_path": null,
  "state_path": "/home/alacasse/projects/graphify/my-docs/plans/architecture-program-run-state.json",
  "validation_summary": null
}
```

The persisted state file currently records:

```json
{
  "active_phase": "select-dispatch",
  "batches_completed": 0,
  "dispatch_path": null,
  "execute_batches": true,
  "last_phase_status": "failed",
  "last_receipt_path": null,
  "max_batches": 1,
  "program_ledger": "my-docs/plans/install-sandbox-architecture-findings.md",
  "spec_path": null
}
```

## Impact

- The runner did not make semantic progress on the architecture program.
- No Graphify code changes were made.
- No dispatch packet, spec receipt, validation result, review result, or commit
  range exists for this attempted run.
- The Graphify worktree remained clean after the failed attempt.
- The codex-config worktree was also clean before writing this report.
- The failure blocks every local runner phase because all phases use the same
  `--output-schema` file.

This is not a Graphify install-sandbox issue. It is a codex-config runner
contract bug between:

- `scripts/architecture_program_runner.py`
- `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`
- the current `codex exec --output-schema` structured-output schema subset

## Relevant Code And Contract

The runner builds every phase command in
`scripts/architecture_program_runner.py` by passing the schema directly to
Codex:

```python
command = [
    "codex",
    "exec",
    "--cd",
    str(config.project),
    "--sandbox",
    config.sandbox,
    "--output-schema",
    str(SCHEMA_PATH),
    "--output-last-message",
    str(output_last_message),
]
```

`SCHEMA_PATH` points at:

```text
skills/architecture-program-runway/references/local-runner-phase-result.schema.json
```

That schema currently ends with a top-level `allOf` containing conditional
validation rules:

```json
"allOf": [
  {
    "if": { "properties": { "status": { "const": "stopped" } } },
    "then": { "properties": { "next_phase": { "const": "stopped" } } }
  },
  {
    "if": { "properties": { "status": { "const": "failed" } } },
    "then": { "properties": { "next_phase": { "const": "stopped" } } }
  },
  {
    "if": { "properties": { "status": { "const": "completed" } } },
    "then": {
      "not": {
        "properties": { "next_phase": { "const": "stopped" } }
      }
    }
  }
]
```

The Python runner already enforces these status and transition invariants after
receiving the phase result:

```python
if status in {"stopped", "failed"} and next_phase != "stopped":
    raise RunnerError(f"status={status} must use next_phase=stopped")
if status == "completed" and next_phase == "stopped":
    raise RunnerError("status=completed must not use next_phase=stopped")
```

It also validates the expected next phase against runner state:

```python
expected = expected_next_phases(result["phase"], state)
if result["next_phase"] not in expected:
    raise RunnerError(...)
```

So the `allOf` conditional block is duplicating Python-side runner validation.
It is useful as JSON Schema documentation, but it is not required for runner
safety.

## Root Cause

The local runner schema was written as draft-07 JSON Schema, but
`codex exec --output-schema` uses a stricter structured-output schema subset
that does not allow `allOf` at the root.

The runner assumed that a locally valid draft-07 schema would also be accepted
by `codex exec --output-schema`. That assumption is false.

The immediate incompatible keyword is:

```json
"allOf"
```

The nested conditional keywords `if`, `then`, and `not` may also be risky for
the structured-output subset even if `allOf` is removed, but the observed hard
failure names `allOf` specifically.

## Why Tests Did Not Catch This

The existing runner tests validate Python behavior and prompt construction, but
they do not verify that the schema file is acceptable to the actual
`codex exec --output-schema` interface.

The implementation plan listed:

```bash
python3 -m json.tool skills/architecture-program-runway/references/local-runner-phase-result.schema.json >/dev/null
```

That only proves the file is syntactically valid JSON. It does not prove the
schema is valid for Codex structured outputs.

The tests also rely on Python-side `validate_phase_result`, which does enforce
the status/next-phase consistency rules. That made the conditional schema block
feel safe, but did not exercise the external schema-acceptance boundary.

## Diagnosis Notes

Ranked hypotheses considered after the failure:

1. The schema contains a keyword unsupported by Codex structured outputs.
   Prediction: the API error will name a JSON Schema keyword before any phase
   agent work starts. Confirmed by the `allOf is not permitted` error.
2. The runner passed the wrong schema path.
   Prediction: the schema path in the nested prompt would be missing or point
   outside codex-config. Not supported; the path points to the expected schema.
3. The phase agent returned malformed JSON.
   Prediction: the failure would occur after an agent response and runner-side
   `read_json_object` or `validate_phase_result`. Not supported; the API
   rejected the request before phase execution.
4. The Graphify ledger or worktree blocked select-dispatch.
   Prediction: the runner would report a worktree or ledger stop. Not
   supported; the stop reason is a schema request error.

## Recommended Fix

Split the runner result contract into two layers:

1. A Codex-output-compatible schema used only with `codex exec --output-schema`.
2. Python-side semantic validation in `validate_phase_result`, which already
   enforces the cross-field and state-dependent invariants.

For v1, the smallest fix is:

- Remove the top-level `allOf` block from
  `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`.
- Keep the simple object shape: `type`, `additionalProperties`, `required`,
  primitive field types, enums, arrays, and nullable fields.
- Keep the existing Python-side checks for:
  - `status=stopped` requiring `next_phase=stopped`
  - `status=failed` requiring `next_phase=stopped`
  - `status=completed` forbidding `next_phase=stopped`
  - phase-specific next-phase transitions from runner state
- Update `local-runner-v1.md` and/or comments to say the JSON schema is
  intentionally limited to the Codex structured-output subset, while semantic
  validation lives in the runner.
- Add a regression test that fails if unsupported structured-output keywords
  are added to the schema.

Potential unsupported-keyword denylist for a local unit test:

```python
UNSUPPORTED_CODEX_OUTPUT_SCHEMA_KEYS = {
    "allOf",
    "anyOf",
    "oneOf",
    "not",
    "if",
    "then",
    "else",
}
```

The exact denylist should match the current Codex/OpenAI structured-output
contract. The observed required entry is `allOf`.

## Better Fix

Add a helper in the runner or tests that loads the schema and enforces a
deliberately conservative "Codex output schema subset" contract before the
runner can invoke `codex exec`.

Example test intent:

```text
test_phase_result_schema_uses_codex_output_subset
```

Expected assertions:

- no root-level composition keywords such as `allOf`
- no conditional schema keywords such as `if`/`then`/`else`
- no `not`
- required fields remain stable
- Python-side validation still rejects contradictory status/next-phase pairs

This would catch the exact failure without requiring a live API call in normal
unit tests.

## Validation After Fix

Run in `/home/alacasse/projects/codex-config`:

```bash
python3 -m unittest
python3 -m json.tool skills/architecture-program-runway/references/local-runner-phase-result.schema.json >/dev/null
git diff --check
scripts/architecture_program_runner.py --dry-run \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

Then run the real external-boundary smoke from Graphify:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --stop-after-phase select-dispatch
```

Success criteria for the smoke:

- `codex exec` accepts the output schema.
- `select-dispatch` completes or stops for a domain reason, not schema
  rejection.
- `my-docs/plans/architecture-program-run-state.json` records a dispatch path
  and `active_phase=create-spec` on success.
- The phase receipt exists and matches the final phase JSON.

After that, resume the original one-batch run:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

If the failed state is considered stale, use a fresh `--state` path rather than
editing runner state by hand.

## Cleanup Considerations

The failed run wrote this ignored Graphify runner state file:

```text
/home/alacasse/projects/graphify/my-docs/plans/architecture-program-run-state.json
```

That state records `last_phase_status=failed` and `active_phase=select-dispatch`.
It can be reused with `--resume` after the schema fix, or superseded by a fresh
state path. Do not commit it.

## Codex-Config Follow-Up Checklist

- [ ] Remove unsupported structured-output schema keywords from
      `local-runner-phase-result.schema.json`.
- [ ] Preserve equivalent semantic validation in
      `scripts/architecture_program_runner.py`.
- [ ] Add a unit test for the Codex output schema subset.
- [ ] Update `skills/architecture-program-runway/references/local-runner-v1.md`
      if the schema/semantic-validation split needs to be explicit.
- [ ] Update `CHANGELOG.md` because this is a meaningful workflow behavior fix.
- [ ] Reinstall or refresh the repo-owned `architecture-program-runway` feature
      if the live `~/.codex` symlink/metadata needs updating.
- [ ] Re-run the Graphify first-batch runner command after the fix.
