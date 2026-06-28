# Architecture Program Runner Env Pass-Through Remediation Report

## Summary

On 2026-06-26, the local architecture program runner was updated to address the
execute-phase validation environment blocker described in:

```text
plans/architecture-program-runner-execute-validation-block-report.md
```

The original runner reached the real `execute` phase, then stopped correctly
because canonical project validation could not run in the nested `codex exec`
environment. Fallback validation passed, but fallback-only validation is not
enough for Batch Runway execution or architecture-program closeout.

The codex-config remediation is generic environment pass-through:

```bash
--env KEY=VALUE
```

The runner remains project-neutral. It does not know or default any project
tooling, cache path, package manager, or validation command.

## Issue Addressed

The failed Graphify run showed this boundary:

- `select-dispatch` completed.
- `create-spec` completed.
- `execute` started and made test-only changes.
- `.venv` fallback validation passed.
- canonical validation failed because dependency resolution was blocked by the
  nested phase environment.
- the runner stopped before commit and closeout.

The bug was not that the runner stopped. Stopping was correct. The missing
codex-config capability was a project-neutral way for the outer runner
invocation to supply environment variables required by nested phase processes.

## Implementation

Implemented in commit:

```text
f5b284c feat: add support for environment variable overrides in architecture program runner
```

Current related follow-up on top:

```text
8755f86 feat: enhance architecture program runner to support resuming from stopped phase with evidence paths
```

Changed surfaces:

- `scripts/architecture_program_runner.py`
- `tests/test_architecture_program_runner.py`
- `skills/architecture-program-runway/references/local-runner-v1.md`
- `CHANGELOG.md`
- `codex-features.json`

Feature version:

```text
architecture-program-runway 1.0.8
```

## CLI Behavior

The runner now accepts zero or more repeated env overrides:

```bash
--env KEY=VALUE
```

Validation rules:

- values must contain `=`;
- the key before `=` must be non-empty;
- empty values are allowed;
- repeated keys are accepted, with later subprocess environment assignment
  semantics applying through the final merged environment.

The existing runner phase model is unchanged:

```text
select-dispatch -> create-spec -> execute -> closeout
```

## Subprocess Environment Behavior

For each nested `codex exec` phase, the runner now builds an environment by:

1. copying the current process environment;
2. applying the `--env KEY=VALUE` overrides;
3. passing the merged mapping to `subprocess.run(env=...)`.

This means existing environment variables remain available unless explicitly
overridden. Env override values are not placed on the `codex exec` command line.

Dry-run output and runner phase prompts mention override keys only, not values.

## Receipt Guidance

The execute-phase prompt now asks stopped validation receipts to summarize:

- canonical commands attempted;
- whether fallback validation was attempted;
- whether fallback validation passed;
- likely failure class, such as DNS, cache, permission, lockfile, or test
  failure;
- relevant env override keys, without values;
- dirty files remaining.

This is receipt guidance only. The phase result schema remains compact and
unchanged for this capability.

## Documentation Update

The local runner protocol now states that:

- the runner is project-neutral;
- projects may pass env vars needed by their validation environment;
- env vars are passed into nested `codex exec` phase processes;
- dry-run diagnostics show keys only;
- env pass-through is not a validation bypass;
- canonical validation must still pass before execute can commit and closeout
  can proceed.

The docs use a generic placeholder example:

```bash
--env TOOL_CACHE_DIR=/tmp/project-tool-cache
```

## Tests Added

The runner tests now cover:

- parsing one `--env KEY=VALUE`;
- parsing multiple `--env` values;
- rejecting an env override with no `=`;
- rejecting an empty env key;
- preserving the base environment;
- passing env overrides into the `codex exec` subprocess environment;
- redacting env values from dry-run output;
- preserving the no-env default behavior.

## Validation

Validation commands run for the remediation:

```bash
python3 -m unittest tests.test_architecture_program_runner
python3 -m unittest discover
python3 -m compileall -q scripts tests
python3 -m json.tool codex-features.json
git diff --check
python3 scripts/architecture_program_runner.py --help
```

Observed results:

```text
tests.test_architecture_program_runner: 40 tests passed
unittest discover: 47 tests passed
compileall: passed
codex-features JSON validation: passed
git diff --check: passed
runner --help: showed --env KEY=VALUE
```

## Resume Command For Graphify

After making the Graphify validation environment available, resume the stopped
runner with the project-supplied env override:

```bash
~/.codex/scripts/architecture_program_runner.py \
  --resume \
  --project /home/alacasse/projects/graphify \
  --program-ledger my-docs/plans/install-sandbox-architecture-findings.md \
  --max-batches 1 \
  --execute-batches \
  --env UV_CACHE_DIR=/tmp/graphify-uv-cache
```

This command is a Graphify invocation example, not runner behavior. The runner
only provides generic `--env KEY=VALUE` pass-through.

## Remaining Risk

Environment pass-through does not guarantee validation success. It only gives
nested phases the supplied environment values.

Canonical validation may still stop if:

- the referenced cache is cold or missing required dependencies;
- network/DNS is still needed and unavailable;
- sandbox permissions block cache, process, Docker, or Git access;
- the stopped Graphify worktree has dirty-file conflicts;
- the code changes made during the previous stopped execute phase no longer
  match the current spec or project state.

These are intentional stop conditions. The runner must not proceed to closeout
from fallback-only validation.

## Closeout Status

The codex-config remediation is complete. The Graphify architecture program run
still needs to be resumed separately after its validation environment is
available.
