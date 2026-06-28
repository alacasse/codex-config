# Architecture Program Runner Nested Validation Block Report

## Summary

On 2026-06-26, the Graphify architecture program runner was resumed after the
generic `--env KEY=VALUE` pass-through remediation. The runner did pass the
`UV_CACHE_DIR` override key into the nested `execute` phase prompt, and the
dirty-file resume blocker was fixed enough for the nested phase to start.

The run still stopped in `execute`. The nested Batch Runway phase again reported
that canonical `uv run --frozen` validation could not resolve
`setuptools>=68` from PyPI because DNS was unavailable. Fallback validation
through the local `.venv` passed, but the runner correctly refused to commit or
close out from fallback-only validation.

The issue is now narrower than the earlier env-pass-through bug:

- env pass-through exists at the runner subprocess boundary;
- stopped receipt evidence paths are accepted for resume;
- outer-shell canonical `uv` validation works with
  `UV_CACHE_DIR=/tmp/graphify-uv-cache`;
- nested `codex exec --sandbox workspace-write` validation still behaves as if
  it must resolve dependencies over DNS.

## Current State

Graphify runner state:

```json
{
  "active_batch_id": "catalog-boundary-reassessment",
  "active_phase": "execute",
  "batches_completed": 0,
  "dispatch_path": "my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md",
  "execute_batches": true,
  "last_phase_status": "stopped",
  "last_receipt_path": "my-docs/plans/receipts/architecture-program-execute-catalog-boundary.json",
  "max_batches": 1,
  "program_ledger": "my-docs/plans/install-sandbox-architecture-findings.md",
  "spec_path": "my-docs/plans/install-sandbox-catalog-boundary-runway.md",
  "stop_reason": "validation_failed"
}
```

Graphify dirty files left by the stopped execute phase:

```text
M tests/install_sandbox/test_install_target_harness_policy.py
M tests/install_sandbox/test_install_target_selection.py
```

Current execute receipt summary:

```text
canonical uv pytest and ruff blocked resolving setuptools>=68 from PyPI due DNS;
fallback .venv pytest 24 passed, .venv ruff passed, git diff --check passed;
env override keys: UV_CACHE_DIR;
dirty files remain:
tests/install_sandbox/test_install_target_harness_policy.py,
tests/install_sandbox/test_install_target_selection.py
```

No Graphify commit was created. Closeout did not run.

## What Was Tried

### 1. Resume With `UV_CACHE_DIR`

Command shape:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --env UV_CACHE_DIR=/tmp/graphify-uv-cache
```

Result:

- the original conservative worktree gate rejected the two dirty test files;
- this exposed a second runner recovery gap: the runner did not classify the
  previous stopped execute receipt's `evidence_paths` as expected dirty files
  for the same active phase.

### 2. Patch Stopped-Receipt Evidence Resume

The runner was patched in codex-config so a stopped receipt for the same active
phase contributes its `evidence_paths` to expected dirty paths.

Regression validation:

```bash
python3 -m unittest tests/test_architecture_program_runner.py
```

Observed result:

```text
42 tests passed
```

This allowed the runner to reach the nested `execute` phase instead of stopping
at preflight.

### 3. Resume Again With `UV_CACHE_DIR`

The runner reached nested `execute`, but the execute receipt still reported DNS
while resolving `setuptools>=68`.

Important evidence:

- the receipt included `env override keys: UV_CACHE_DIR`, so the phase prompt
  knew the runner was invoked with the override key;
- the receipt did not prove that nested shell commands actually inherited
  `UV_CACHE_DIR` or used the intended value;
- validation still failed at canonical `uv run --frozen`, not at tests or ruff
  behavior.

### 4. Prewarm Outer Canonical Validation

The same focused canonical commands were run from the outer shell with the
Graphify cache path:

```bash
UV_CACHE_DIR=/tmp/graphify-uv-cache uv run --frozen pytest \
  tests/install_sandbox/test_install_target_selection.py \
  tests/install_sandbox/test_install_target_harness_policy.py -q

UV_CACHE_DIR=/tmp/graphify-uv-cache uv run --frozen ruff check \
  tests/install_sandbox/test_install_target_selection.py \
  tests/install_sandbox/test_install_target_harness_policy.py
```

Observed result:

```text
24 passed
All checks passed
```

This proves the Graphify checkout can validate with the cache path from the
outer execution environment. It does not prove nested Codex tool commands see or
can use that path.

### 5. Resume After Cache Prewarm

The runner was resumed again with the same `--env UV_CACHE_DIR=...` override.

Result:

```text
stop_reason: validation_failed
validation_summary: canonical uv pytest and ruff blocked resolving
setuptools>=68 from PyPI due DNS
```

Cache prewarm did not change the nested result.

### 6. Try `--sandbox danger-full-access`

The next documented recovery option was attempted:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --env UV_CACHE_DIR=/tmp/graphify-uv-cache \
  --sandbox danger-full-access
```

The approval reviewer rejected this because it materially broadens the nested
Codex sandbox beyond the current explicit approval. The run was not performed.

## Current Best Diagnosis

The remaining blocker is not Graphify test failure and not the original
codex-config schema/env-pass-through issue.

The most likely remaining causes are:

1. **Nested Codex tool commands do not inherit arbitrary runner environment
   overrides.** The runner passes `UV_CACHE_DIR` into the `codex exec`
   subprocess, but the nested agent's shell tool may run with a sanitized
   environment or a separate shell snapshot. The receipt can name the key
   because the prompt names it, but that is not proof that `uv` saw the value.
2. **The nested `workspace-write` sandbox cannot read or use the outer
   `/tmp/graphify-uv-cache` contents.** Even if `UV_CACHE_DIR` is set, the
   nested sandbox may see a different `/tmp`, lack required files, or be unable
   to hardlink/copy from the cache shape that outer `uv` used.
3. **The nested validation command still requires network despite the cache.**
   The cache may contain enough for the outer focused validation but not enough
   for the nested phase's exact command, Python selection, build isolation, or
   package install path.
4. **The nested phase is not actually running the same canonical command shape
   that was prewarmed.** The receipt is compact and does not include exact
   command lines, so it may be attempting a broader or subtly different
   `uv run --frozen` command.
5. **`danger-full-access` may be required for this local runner execution
   class.** This remains plausible, but it should be tested after a narrower
   environment-propagation probe, or run only with explicit user approval.

## What To Try Next

### Step 1: Run A Minimal Nested Environment Probe

Before rerunning the full architecture program, run a tiny `codex exec` probe
with the same project, same sandbox, and same env override.

Goal: determine whether nested Codex shell commands see the env value and can
read the cache directory.

Suggested probe:

```bash
UV_CACHE_DIR=/tmp/graphify-uv-cache codex exec \
  --cd /home/alacasse/projects/graphify \
  --sandbox workspace-write \
  'Run exactly:
   python - <<'"'"'PY'"'"'
   import os
   from pathlib import Path
   value = os.environ.get("UV_CACHE_DIR")
   print("UV_CACHE_DIR_SET", bool(value))
   print("UV_CACHE_DIR_VALUE", value or "")
   if value:
       path = Path(value)
       print("UV_CACHE_DIR_EXISTS", path.exists())
       print("UV_CACHE_DIR_IS_DIR", path.is_dir())
       print("UV_CACHE_DIR_SAMPLE_COUNT", len(list(path.rglob("*"))) if path.exists() else 0)
   PY'
```

Interpretation:

- If `UV_CACHE_DIR_SET` is false, runner env pass-through reaches the
  `codex exec` process but not nested tool commands. The runner needs a
  project-neutral way to expose non-secret env overrides to phase prompts or
  command execution policy.
- If the variable is set but the path is missing or empty, the next fix is
  cache visibility/mounting, not runner prompt behavior.
- If the variable is set and the cache is visible, compare the exact nested
  `uv` command against the prewarmed command.

### Step 2: Run A Minimal Nested `uv` Probe

If the env/path probe passes, run a nested probe that executes the same focused
canonical validation directly, outside the architecture runner:

```bash
UV_CACHE_DIR=/tmp/graphify-uv-cache codex exec \
  --cd /home/alacasse/projects/graphify \
  --sandbox workspace-write \
  'Run exactly:
   uv run --frozen pytest tests/install_sandbox/test_install_target_selection.py tests/install_sandbox/test_install_target_harness_policy.py -q
   uv run --frozen ruff check tests/install_sandbox/test_install_target_selection.py tests/install_sandbox/test_install_target_harness_policy.py'
```

Interpretation:

- If this fails with the same DNS error, the problem is nested sandbox/cache
  access rather than Batch Runway orchestration.
- If this passes, the Batch Runway execute phase is likely running a different
  command or losing the env through subagent/tool routing.

### Step 3: Improve Execute Receipt Detail

The current receipt is good enough to know the failure class, but not enough to
separate env propagation, cache visibility, and command mismatch.

Consider updating the local runner execute prompt or Batch Runway recovery
guidance so stopped validation receipts include:

- exact canonical command lines attempted;
- whether `UV_CACHE_DIR` was present in the command environment;
- whether the cache path existed and was readable from the nested phase;
- whether the command used the project `.venv`, `uv` managed env, or another
  Python path;
- first DNS/cache error line from `uv`.

Do not include secret env values by default. For explicitly non-secret local
paths, either allow opt-in value disclosure or report only booleans and path
classification.

### Step 4: Retry With Explicit Approval For `danger-full-access`

If the nested probes show that `workspace-write` is the real blocker, ask for
explicit approval to rerun the architecture program with:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --env UV_CACHE_DIR=/tmp/graphify-uv-cache \
  --sandbox danger-full-access
```

This should be treated as a deliberate local workflow escalation, not a generic
default.

## Non-Recommendations

Do not manually mark the batch executed or run architecture closeout from the
current fallback-only state. The runner correctly requires canonical validation
before commit and closeout.

Do not encode `/tmp/graphify-uv-cache` as a codex-config default. The env
override should remain project-supplied.

Do not change Graphify installer behavior, test expectations, YAML schema, or
public CLI behavior to work around this validation environment issue.

## Recommended Immediate Next Action

Run the minimal nested environment probe. It is the smallest test that can
distinguish between:

- `UV_CACHE_DIR` not reaching nested shell tools;
- cache path not visible inside nested `workspace-write`;
- cache visible but nested `uv` command still needing network;
- Batch Runway execute running a different command than expected.

That result should determine whether the next fix belongs in:

- codex-config runner env/prompt behavior;
- Codex sandbox invocation mode;
- Batch Runway stopped-validation receipt detail;
- Graphify local cache prewarming;
- or an explicitly approved `danger-full-access` runner resume.
