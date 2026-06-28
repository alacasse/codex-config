# Architecture Program Runner Execute Validation Block Report

## Summary

On 2026-06-26, after the local architecture program runner schema issues were
fixed enough for phases to start, the runner successfully advanced through:

```text
select-dispatch -> create-spec -> execute
```

It then stopped during the `execute` phase for the Graphify install-sandbox
catalog-boundary batch. This was not a structured-output schema failure. The
runner reached the Batch Runway execution phase, made test-only changes, and
then stopped because canonical validation using `uv run --frozen` could not
resolve dependencies due to unavailable network/DNS.

The execute receipt reports:

```text
.venv focused pytest 24 passed; .venv ruff passed; git diff --check passed;
uv run --frozen pytest/ruff blocked by DNS fetching setuptools>=68
```

No batch closeout happened and no commit was created.

## Intended Operation

The user asked to try the runner again after prior schema failures.

The command invoked was:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

Expected complete flow:

```text
select-dispatch -> create-spec -> execute -> closeout
```

Expected selected batch:

```text
catalog-boundary-reassessment
```

Expected dispatch:

```text
my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md
```

Expected spec:

```text
my-docs/plans/install-sandbox-catalog-boundary-runway.md
```

Because `--execute-batches` was set, the runner was expected to execute the
generated Batch Runway spec, validate it, commit successful code changes, and
then close out the architecture program ledger.

## What Actually Happened

The runner got past both prior schema blockers and completed the first two
phases:

- `select-dispatch` selected `catalog-boundary-reassessment`.
- `create-spec` produced or confirmed
  `my-docs/plans/install-sandbox-catalog-boundary-runway.md`.

The persisted runner state after `create-spec` showed:

```json
{
  "active_batch_id": "catalog-boundary-reassessment",
  "active_phase": "execute",
  "batches_completed": 0,
  "dispatch_path": "my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md",
  "last_phase_status": "completed",
  "last_receipt_path": "my-docs/plans/receipts/architecture-program-create-spec-catalog-boundary.json",
  "spec_path": "my-docs/plans/install-sandbox-catalog-boundary-runway.md"
}
```

The runner then entered `execute`. The execution agent edited two test files:

```text
tests/install_sandbox/test_install_target_harness_policy.py
tests/install_sandbox/test_install_target_selection.py
```

The execution phase stopped with this receipt:

```json
{
  "status": "stopped",
  "phase": "execute",
  "next_phase": "stopped",
  "stop_reason": "validation blocked: canonical uv run --frozen focused pytest and ruff cannot fetch setuptools>=68 because network/DNS is unavailable",
  "program_ledger": "my-docs/plans/install-sandbox-architecture-findings.md",
  "batch_id": "catalog-boundary-reassessment",
  "dispatch_path": "my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md",
  "spec_path": "my-docs/plans/install-sandbox-catalog-boundary-runway.md",
  "receipt_path": "my-docs/plans/receipts/architecture-program-execute-catalog-boundary.json",
  "commit_range": null,
  "validation_summary": ".venv focused pytest 24 passed; .venv ruff passed; git diff --check passed; uv run --frozen pytest/ruff blocked by DNS fetching setuptools>=68",
  "review_summary": null,
  "evidence_paths": [
    "my-docs/plans/install-sandbox-catalog-boundary-runway.md",
    "tests/install_sandbox/test_install_target_selection.py",
    "tests/install_sandbox/test_install_target_harness_policy.py"
  ]
}
```

The final runner summary was:

```json
{
  "active_batch": "catalog-boundary-reassessment",
  "batches_completed": 0,
  "commit_range": null,
  "dispatch_path": "my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md",
  "last_receipt_path": "my-docs/plans/receipts/architecture-program-execute-catalog-boundary.json",
  "review_summary": null,
  "spec_path": "my-docs/plans/install-sandbox-catalog-boundary-runway.md",
  "state_path": "/home/alacasse/projects/graphify/my-docs/plans/architecture-program-run-state.json",
  "stop_reason": "validation blocked: canonical uv run --frozen focused pytest and ruff cannot fetch setuptools>=68 because network/DNS is unavailable",
  "validation_summary": ".venv focused pytest 24 passed; .venv ruff passed; git diff --check passed; uv run --frozen pytest/ruff blocked by DNS fetching setuptools>=68"
}
```

Current Graphify tracked dirty files:

```text
 M tests/install_sandbox/test_install_target_harness_policy.py
 M tests/install_sandbox/test_install_target_selection.py
```

Current diff summary:

```text
2 files changed, 109 insertions(+), 50 deletions(-)
```

## Impact

- The architecture runner is now past the prior structured-output schema
  blockers.
- The selected batch reached actual Batch Runway execution.
- The execution phase made test-only changes but stopped before commit.
- Closeout did not run.
- The architecture findings ledger was not reconciled.
- `batches_completed` remains `0`.
- Graphify now has uncommitted tracked test changes from the stopped execution.
- The runner cannot safely resume to closeout because the execute phase did not
  complete and did not produce a commit range.

This is no longer a pure codex-config schema issue. It is an orchestration and
validation-environment issue at the boundary between:

- codex-config's local architecture runner,
- Graphify's Batch Runway validation contract,
- nested `codex exec` sandbox/network behavior,
- and Graphify's `uv run --frozen` dependency availability.

## Root Cause

The Batch Runway execution phase attempted the canonical Graphify validation
commands using `uv run --frozen`. In this environment, the nested execution
could not resolve `setuptools>=68` because DNS/network access was unavailable.

The execution agent used a fallback validation path through the local `.venv`,
and that fallback passed:

```text
.venv focused pytest 24 passed
.venv ruff passed
git diff --check passed
```

However, the project-local Graphify rules require canonical `uv run --frozen`
validation for runner work. The execution phase correctly stopped instead of
committing and closing out from fallback-only validation.

## Why This Matters

The local runner can now launch nested Codex phases, but successful execution
depends on the nested phase having a validation environment equivalent to the
normal project workflow.

For Graphify install-sandbox work, that means:

- `uv run --frozen pytest ...` must be able to use an available cache or network.
- `uv run --frozen ruff check ...` must be able to use the same dependency set.
- Later install-sandbox production batches may also need Docker socket access.

If the runner cannot supply or preserve those capabilities in nested phases,
execution can repeatedly stop after editing files but before committing,
requiring manual cleanup or manual validation.

## Genericity Requirement

The codex-config fix should not hard-code Graphify, `uv`, or
`/tmp/graphify-uv-cache` into the local architecture runner. This runner is a
cross-project workflow tool and should stay project-neutral.

The generic runner responsibility is to let projects supply execution
environment details at invocation time or through a project-local ignored config
file. Graphify can then provide `UV_CACHE_DIR=/tmp/graphify-uv-cache` from its
local instructions, while another project might provide `PIP_CACHE_DIR`,
`NPM_CONFIG_CACHE`, `CARGO_HOME`, Docker-related variables, or nothing.

Graphify's `UV_CACHE_DIR` is evidence for why the capability is needed; it is
not the capability itself.

## Diagnosis Notes

Ranked hypotheses:

1. The nested runner phase lacked network/DNS for canonical `uv run --frozen`
   dependency resolution. Confirmed by the execute receipt naming DNS while
   fetching `setuptools>=68`.
2. The nested phase did not inherit the known Graphify workaround
   `UV_CACHE_DIR=/tmp/graphify-uv-cache`, or that cache did not contain the
   needed dependency. Plausible; the receipt does not show cache configuration.
3. The runner's `--sandbox workspace-write` setting is too restrictive for
   Graphify execution validation when dependencies are not already cached.
   Plausible; the current run used the default runner sandbox.
4. The code changes themselves caused validation failure. Not supported by the
   receipt: fallback `.venv` pytest and ruff passed.
5. The runner should have committed because fallback validation passed. Rejected:
   project rules require canonical `uv run --frozen` validation, so stopping was
   the safer behavior.

## Recommended Fix Options

### Option A: Add Generic Environment Pass-Through

Teach `scripts/architecture_program_runner.py` to accept and pass through
project-supplied environment variables needed by nested phases.

Possible CLI shape:

```bash
scripts/architecture_program_runner.py \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --env UV_CACHE_DIR=/tmp/graphify-uv-cache
```

The runner would pass this environment into the subprocess call that launches
`codex exec`.

This keeps codex-config generic: the runner owns `--env KEY=VALUE` mechanics,
while each project owns which variables it passes. For Graphify, the local
invocation would pass `UV_CACHE_DIR=/tmp/graphify-uv-cache` if validation
dependencies are already cached under that path.

A later extension could add a project-local env file without making the runner
project-specific:

```bash
scripts/architecture_program_runner.py \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --runner-env-file my-docs/runner.env
```

That file should live in the project and can be ignored/local when the values
are machine-specific.

### Option B: Run Execution With A Less Restrictive Codex Sandbox

Resume with a runner sandbox value that gives nested Codex more access:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --sandbox danger-full-access
```

This may allow dependency/network access depending on the outer environment and
Codex approval model. It is more powerful than needed if the only missing piece
is a cache path, but it may also be required for future Docker-backed
install-sandbox validation.

### Option C: Prewarm The Graphify Validation Cache

Run canonical Graphify validation once outside the nested runner, with the
known cache workaround and network access, so later nested `uv run --frozen`
commands do not need DNS:

```bash
UV_CACHE_DIR=/tmp/graphify-uv-cache uv run --frozen pytest <focused targets>
UV_CACHE_DIR=/tmp/graphify-uv-cache uv run --frozen ruff check <focused targets>
```

This is operationally simple but does not fix the runner contract. It may need
to be repeated after dependency changes or cache cleanup.

### Option D: Improve Stop Receipts For Validation Environment Failures

Have Batch Runway execution receipts include:

- exact canonical validation commands attempted,
- whether `UV_CACHE_DIR` was set,
- whether the failure was DNS, cache miss, permission, or lockfile mismatch,
- whether fallback validation was used,
- whether uncommitted files remain.

The current receipt is good enough to understand the failure, but a little more
environment detail would make automated recovery safer.

## Recommended Next Step

Do not close out this batch yet. The execution phase stopped before commit and
left tracked changes.

The safest next sequence is:

1. Preserve or inspect the current two-file diff.
2. Make canonical validation possible, preferably by passing
   `UV_CACHE_DIR=/tmp/graphify-uv-cache` or using an appropriate runner sandbox.
3. Resume the runner from `execute`.
4. Let the Batch Runway execution phase complete validation, review, and commit.
5. Let the runner proceed to `closeout`.

If the current stopped execution cannot be resumed cleanly, either use a fresh
runner state after intentionally handling the dirty test changes, or manually
complete the active Batch Runway spec and then run architecture closeout.

## Validation After Fix

From Graphify, after making canonical validation available:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches
```

Success criteria:

- `execute` completes instead of stopping.
- The receipt has `status=completed` and `next_phase=closeout`.
- `commit_range` is non-null after execution or closeout evidence identifies
  the commit.
- No unexpected tracked code changes remain uncommitted after execute.
- `closeout` updates
  `my-docs/plans/install-sandbox-architecture-findings.md`.
- `batches_completed` becomes `1`.

## Cleanup Considerations

The current stopped run left these tracked files modified:

```text
tests/install_sandbox/test_install_target_harness_policy.py
tests/install_sandbox/test_install_target_selection.py
```

Do not discard them casually. They are the execution phase's in-progress work
for the catalog-boundary batch.

The current runner state remains:

```text
/home/alacasse/projects/graphify/my-docs/plans/architecture-program-run-state.json
```

It points to `active_phase=execute` and can be resumed after fixing validation
environment access.

## Codex-Config Follow-Up Checklist

- [ ] Decide whether the runner should support environment pass-through such as
      `--env UV_CACHE_DIR=/tmp/graphify-uv-cache`.
- [ ] Decide whether Graphify runner invocations should default to or document
      `--sandbox danger-full-access` for execution phases that may need network
      or Docker.
- [ ] Add a runner test for environment pass-through if implemented.
- [ ] Update `skills/architecture-program-runway/references/local-runner-v1.md`
      with validation-environment guidance.
- [ ] Update `CHANGELOG.md` for any codex-config workflow behavior change.
- [ ] Resume the Graphify runner only after canonical validation can run.
