# Architecture Program Runner Summary Schema Error Report

## Summary

On 2026-06-26, after the initial `allOf` schema blocker was moved past, the
local architecture program runner was retried against the Graphify
install-sandbox architecture ledger. The runner still failed before the first
`select-dispatch` phase could execute.

This second failure is a different structured-output schema incompatibility.
`codex exec --output-schema` now rejects the permissive `validation_summary`
field definition in:

```text
skills/architecture-program-runway/references/local-runner-phase-result.schema.json
```

The current schema allows `validation_summary` and `review_summary` to be a
string, object, array, or null:

```json
"validation_summary": {
  "type": ["string", "object", "array", "null"]
},
"review_summary": {
  "type": ["string", "object", "array", "null"]
}
```

Codex structured outputs require object schemas to be fully specified, including
`additionalProperties: false`. Because `validation_summary` permits a generic
object without defining its properties, the request is rejected before any
runner phase agent starts.

No architecture batch was selected, no dispatch packet was written, no Batch
Runway spec was executed, and no closeout happened.

## Intended Operation

The user asked to try again using the local architecture program runner.

The retry used the persisted failed runner state from the first attempt:

```text
/home/alacasse/projects/graphify/my-docs/plans/architecture-program-run-state.json
```

The command invoked was:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

Expected runner flow remained:

```text
select-dispatch -> create-spec -> execute -> closeout
```

The runner was expected to resume at `select-dispatch`, select the first
executable architecture batch from the ledger, then continue through spec
creation, execution, and closeout because `--execute-batches` was set.

For the active Graphify ledger, the expected first queued batch is:

```text
Catalog boundary reassessment
```

with expected concrete spec path:

```text
my-docs/plans/install-sandbox-catalog-boundary-runway.md
```

## What Actually Happened

The runner resumed correctly from its JSON state and launched the first phase:

```text
Current phase: select-dispatch
```

It invoked nested `codex exec` with:

```text
--output-schema /home/alacasse/projects/codex-config/skills/architecture-program-runway/references/local-runner-phase-result.schema.json
--output-last-message <tmp-result>
```

The nested process exited with status `1` before phase execution. Codex rejected
the schema with this error:

```text
invalid_request_error
code: invalid_json_schema
message: Invalid schema for response_format 'codex_output_schema':
In context=('properties', 'validation_summary', 'type', '1'),
'additionalProperties' is required to be supplied and to be false.
param: text.format.schema
status: 400
```

The runner failed closed and printed a final summary with no phase artifacts:

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

The persisted runner state now records:

```json
{
  "active_batch_id": null,
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

- The runner still cannot start the first phase.
- No architecture-program progress was made.
- No `select-dispatch` agent ran.
- No dispatch packet, phase receipt, spec path, validation result, review
  result, or commit range was produced.
- Graphify tracked status remained clean after the retry.
- codex-config tracked status remained clean after the retry.
- The failure blocks every runner phase because all phases use the same output
  schema before the phase agent starts.

This is still a codex-config runner contract bug, not a Graphify install-sandbox
bug.

## Relevant Schema

The current phase-result schema is intentionally simpler than the first failed
version: the top-level `allOf` block is no longer present.

The remaining incompatible fields are:

```json
"validation_summary": {
  "type": ["string", "object", "array", "null"]
},
"review_summary": {
  "type": ["string", "object", "array", "null"]
}
```

The API error identifies the object branch of `validation_summary`:

```text
('properties', 'validation_summary', 'type', '1')
```

Given the type array order:

```json
["string", "object", "array", "null"]
```

index `1` is:

```text
object
```

The next likely blocker after fixing `validation_summary` is `review_summary`,
because it has the same permissive schema. The array branch may also be too
underspecified for Codex structured outputs unless it defines a fully supported
`items` schema.

## Root Cause

The runner phase-result schema still uses broad JSON Schema expressiveness for
fields that are semantically flexible:

```text
validation_summary: string | object | array | null
review_summary: string | object | array | null
```

That is acceptable for the runner's Python-side validator:

```python
if value is not None and not isinstance(value, (str, dict, list)):
    raise RunnerError(...)
```

but it is too loose for `codex exec --output-schema`. The structured-output
schema subset requires any object branch to be closed and explicit:

```json
"additionalProperties": false
```

and, in practice, it is safest to avoid arbitrary object or array summary
payloads in the model-facing schema.

The runner conflates two contracts:

1. The model-facing structured-output contract required by `codex exec`.
2. The runner-facing semantic contract validated by Python after the phase
   result is captured.

The model-facing contract must be narrower and more explicit than the internal
semantic contract.

## Why The Previous Fix Was Not Enough

The previous failure named the top-level `allOf` block:

```text
'allOf' is not permitted
```

Removing or bypassing that block allowed Codex to continue validating the
schema and reveal the next unsupported shape. This is a normal multi-step
schema compatibility failure: the first rejected keyword hid later rejected
field definitions.

The second retry proves that the whole schema must be audited against the Codex
structured-output subset, not patched one error message at a time.

## Diagnosis Notes

Ranked hypotheses after the retry:

1. `validation_summary` permits a generic object without a closed object schema.
   Prediction: the API error will point at the object branch of the
   `validation_summary` type union. Confirmed.
2. `review_summary` has the same problem and will fail next after
   `validation_summary` is fixed. Prediction: the next API error will point at
   `review_summary` or at an array branch if arrays are also too loose.
3. Flexible union fields are too broad for Codex structured outputs.
   Prediction: narrowing summaries to `string | null` should move schema
   validation past these fields while preserving useful receipt summaries.
4. The Graphify program ledger or resume state caused the failure.
   Prediction: the failure would be a dirty-state or domain stop. Not supported;
   the API rejects the schema before the phase starts.

## Recommended Fix

For v1, narrow phase-result summary fields to model-output-friendly strings:

```json
"validation_summary": {
  "type": ["string", "null"]
},
"review_summary": {
  "type": ["string", "null"]
}
```

Then update the runner prompt/reference so phases write compact text summaries,
not arbitrary JSON structures, in these fields.

If structured summaries are still desired later, introduce explicit closed
objects, for example:

```json
"validation_summary": {
  "type": ["object", "null"],
  "additionalProperties": false,
  "required": ["status", "details"],
  "properties": {
    "status": { "type": "string" },
    "details": { "type": "string" }
  }
}
```

However, that is unnecessary for v1. The runner final summary can still print a
compact text receipt, and detailed evidence belongs in `evidence_paths`, commit
range, spec logs, and phase receipts rather than arbitrary nested JSON.

## Required Code Changes

- Update
  `skills/architecture-program-runway/references/local-runner-phase-result.schema.json`
  so `validation_summary` and `review_summary` use a Codex-compatible schema.
- Update `scripts/architecture_program_runner.py` if `validate_summary` should
  become stricter and match the model-facing contract.
- Update tests in `tests/test_architecture_program_runner.py` that currently
  expect dict/list summaries to be accepted, or split tests between
  model-facing schema compatibility and internal receipt parsing.
- Add a regression test that walks the schema and fails on generic object
  branches without `additionalProperties: false`.
- Consider adding a broader "Codex output schema subset" test that catches:
  - composition keywords already seen to fail, such as `allOf`
  - conditional keywords such as `if` and `then`
  - object schemas without `additionalProperties: false`
  - ambiguous free-form object or array branches
- Update `CHANGELOG.md` because this fixes live runner behavior.

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

Then run the live schema-boundary smoke:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --stop-after-phase select-dispatch
```

Success criteria:

- `codex exec` accepts the schema.
- The failure mode, if any, changes from schema validation to a real
  architecture-program domain stop.
- On success, runner state records:
  - `active_phase=create-spec`
  - non-null `active_batch_id`
  - non-null `dispatch_path`
  - non-null `last_receipt_path`
- The receipt path exists and contains the same JSON object returned by the
  phase.

After that smoke passes, resume the full first-batch run:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

## Cleanup Considerations

The retry reused and updated this ignored Graphify runner state file:

```text
/home/alacasse/projects/graphify/my-docs/plans/architecture-program-run-state.json
```

It still points at `active_phase=select-dispatch` and can be used with
`--resume` after the schema fix. If the state is considered noisy after repeated
schema failures, use a fresh `--state` path rather than hand-editing the state.

## Codex-Config Follow-Up Checklist

- [ ] Narrow or explicitly structure `validation_summary`.
- [ ] Narrow or explicitly structure `review_summary`.
- [ ] Align Python-side `validate_summary` with the chosen model-facing
      contract.
- [ ] Add schema-subset regression coverage for object branches.
- [ ] Re-run the local runner through `--stop-after-phase select-dispatch`.
- [ ] Update `CHANGELOG.md`.
- [ ] Re-run the full Graphify first-batch runner after the schema boundary
      smoke passes.
