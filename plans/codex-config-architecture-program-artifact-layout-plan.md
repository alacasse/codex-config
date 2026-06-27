# Codex Config Architecture Program Artifact Layout Plan

## Problem

The local architecture program runner currently leaves run artifacts in a layout that is technically valid but hard to navigate:

- `my-docs/plans/architecture-program-run-state.json`
- `my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md`
- `my-docs/plans/receipts/architecture-program-select-dispatch-catalog-boundary.json`
- `my-docs/plans/receipts/architecture-program-create-spec-catalog-boundary.json`
- `my-docs/plans/receipts/architecture-program-execute-catalog-boundary.json`
- `my-docs/plans/receipts/architecture-program-closeout-catalog-boundary-runner-failed.json`

The receipt JSON includes `program_ledger`, `batch_id`, `dispatch_path`, `spec_path`, and `receipt_path`, so the data is not lost. The problem is that the filesystem does not show the run boundary or the batch boundary. A user must open JSON to answer:

- Which program ledger did this run belong to?
- Which selected batch did these receipts belong to?
- Which dispatch packet and concrete runway spec produced this execution?
- Which files are current active state versus historical evidence?

That is especially confusing because `my-docs/plans/` already contains long-lived human planning files, generated semantic graph files, dispatch packets, runner state, and phase receipts.

## Current Contract Observations

Current runner behavior in `codex-config`:

- `scripts/architecture_program_runner.py` computes the default state path as `<program-ledger-dir>/architecture-program-run-state.json`.
- Phase agents choose and return `receipt_path`; the runner validates that the receipt file content exactly matches the final phase JSON.
- The prompt tells the phase to write a compact phase receipt but does not provide a deterministic receipt path.
- Dirty-worktree classification allows state, last receipt, and phase-specific expected artifacts by path.
- Tests encode examples such as `my-docs/plans/receipts/<phase>.json`.

Current local runner reference behavior:

- The phase model is `select-dispatch -> create-spec -> execute -> closeout`.
- The runner is intentionally dumb and advances from state, receipt paths, known artifact paths, process status, and path existence checks.
- Compact evidence belongs in receipts and referenced files; detailed execution history should not be pasted into the program ledger.

## Design Goal

Make runner artifacts self-locating from the filesystem while preserving the existing architecture-program boundaries:

- Program ledger remains the long-lived program coordination document.
- Dispatch packet remains the selected-batch input contract.
- Batch Runway spec remains the concrete execution plan.
- Runner state and receipts become run-scoped operational artifacts.
- Every generated receipt package traces back to both the selected batch dispatch and the concrete runway spec without requiring broad ledger rereads.

## Proposed Layout

Use a runner-owned artifact root under the program ledger directory:

```text
my-docs/plans/
  install-sandbox-architecture-findings.md
  dispatch/
    catalog-boundary-reassessment-dispatch.md
  install-sandbox-catalog-boundary-runway.md
  architecture-program-runs/
    install-sandbox-architecture-findings/
      run-20260626-204812-catalog-boundary-reassessment/
        run-state.json
        run-manifest.json
        receipts/
          01-select-dispatch.json
        batches/
          catalog-boundary-reassessment/
            batch-manifest.json
            index.md
            receipts/
              02-create-spec.json
              03-execute.json
              04-closeout.json
```

The stable source documents stay in their existing locations:

- Program ledger: `my-docs/plans/install-sandbox-architecture-findings.md`
- Dispatch packet: `my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md`
- Concrete spec: `my-docs/plans/install-sandbox-catalog-boundary-runway.md`

The generated runner files move under a run-scoped directory:

- `run-state.json` replaces the top-level `architecture-program-run-state.json` for new runs.
- `run-manifest.json` identifies the whole bounded runner pass.
- `batch-manifest.json` identifies the selected batch inside the run.
- `index.md` is a short human-readable backlink page for users browsing files.
- `receipts/` is run-local for batch selection receipts because the batch ID is
  unknown before `select-dispatch` completes. Later phase receipts are
  batch-local and phase-ordered.

## Manifest Shape

`run-manifest.json` should be compact and machine-readable:

```json
{
  "schema_version": 1,
  "runner_version": "local-runner-v1",
  "run_id": "run-20260626-204812-catalog-boundary-reassessment",
  "project": "/home/alacasse/projects/graphify",
  "program_ledger": "my-docs/plans/install-sandbox-architecture-findings.md",
  "state_path": "my-docs/plans/architecture-program-runs/install-sandbox-architecture-findings/run-20260626-204812-catalog-boundary-reassessment/run-state.json",
  "max_batches": 1,
  "execute_batches": true,
  "batches": [
    {
      "batch_id": "catalog-boundary-reassessment",
      "batch_artifact_root": "my-docs/plans/architecture-program-runs/install-sandbox-architecture-findings/run-20260626-204812-catalog-boundary-reassessment/batches/catalog-boundary-reassessment",
      "dispatch_path": "my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md",
      "spec_path": "my-docs/plans/install-sandbox-catalog-boundary-runway.md",
      "last_receipt_path": "my-docs/plans/architecture-program-runs/install-sandbox-architecture-findings/run-20260626-204812-catalog-boundary-reassessment/batches/catalog-boundary-reassessment/receipts/04-closeout.json",
      "status": "failed"
    }
  ]
}
```

`batch-manifest.json` should be the local trace anchor:

```json
{
  "schema_version": 1,
  "batch_id": "catalog-boundary-reassessment",
  "program_ledger": "my-docs/plans/install-sandbox-architecture-findings.md",
  "dispatch_path": "my-docs/plans/dispatch/catalog-boundary-reassessment-dispatch.md",
  "spec_path": "my-docs/plans/install-sandbox-catalog-boundary-runway.md",
  "receipts": {
    "select-dispatch": "receipts/01-select-dispatch.json",
    "create-spec": "receipts/02-create-spec.json",
    "execute": "receipts/03-execute.json",
    "closeout": "receipts/04-closeout.json"
  },
  "commit_range": "7b845fa5^..c20e8c9d",
  "validation_summary": "UV_CACHE_DIR present/readable; final pytest 363 passed; ruff passed; sandbox PASS 50/50; agent_summary PASS; graphify update passed; diff-check passed.",
  "review_summary": "All slices reviewed clean after fix loops; Slice 4 direct worker commit recorded as accepted anomaly.",
  "status": "failed"
}
```

`index.md` should be short and browseable:

```markdown
# catalog-boundary-reassessment Runner Artifacts

- Program ledger: ../../../../install-sandbox-architecture-findings.md
- Dispatch packet: ../../../../dispatch/catalog-boundary-reassessment-dispatch.md
- Runway spec: ../../../../install-sandbox-catalog-boundary-runway.md
- Run state: ../../run-state.json
- Receipts: receipts/
```

## Runner Contract Changes

Add deterministic artifact path ownership to the Python runner instead of leaving receipt location fully up to phase agents.

1. Add `run_id` and `artifact_root` to runner state.
2. Default new state path to:

```text
<ledger-dir>/architecture-program-runs/<ledger-stem>/<run-id>/run-state.json
```

3. Keep `--state` as an escape hatch for explicit paths and old state resumes.
4. Add state fields:

```json
{
  "run_id": "run-...",
  "artifact_root": "my-docs/plans/architecture-program-runs/<ledger-stem>/<run-id>",
  "active_batch_artifact_root": "my-docs/plans/architecture-program-runs/<ledger-stem>/<run-id>/batches/<batch-id>",
  "run_manifest_path": "my-docs/plans/architecture-program-runs/<ledger-stem>/<run-id>/run-manifest.json",
  "batch_manifest_path": "my-docs/plans/architecture-program-runs/<ledger-stem>/<run-id>/batches/<batch-id>/batch-manifest.json"
}
```

5. During prompt construction, include a runner-provided expected receipt path:

```text
Expected receipt path for this phase:
my-docs/plans/architecture-program-runs/<ledger-stem>/<run-id>/batches/<batch-id>/receipts/03-execute.json
```

6. Validate that `result["receipt_path"]` equals the expected receipt path for phases where the batch is known.
7. For `select-dispatch`, allow the selected batch ID to be unknown before the phase runs, but require the returned receipt to use the runner-provided run-scoped path. After `batch_id` is known, move future phase receipts into the batch-local root. Do not silently move already-written selection receipts.
8. Write or refresh `run-manifest.json` after every phase result.
9. Write or refresh `batch-manifest.json` and `index.md` once `batch_id` exists.

## Backward Compatibility

Do not break existing stopped runs.

Required compatibility behavior:

- `--resume --state <old-state-path>` should continue to load old top-level state files.
- If an old state has no `artifact_root`, the runner should preserve existing paths and avoid relocating already-written receipts.
- The final summary should include both `state_path` and `artifact_root` when available.
- The runner should accept old flat `last_receipt_path` values during validation.
- New runs should use the structured layout by default.

Optional migration:

- Add a later `--migrate-artifacts` command only if manual cleanup becomes common.
- Do not silently move old receipts on ordinary resume; that risks hiding evidence from a failed run.

## Batch Boundary Rules

The new structure should not copy long-lived planning files into the run directory by default. Copying creates duplicate sources of truth.

Instead, manifests and `index.md` should reference the canonical files:

- `program_ledger`
- `dispatch_path`
- `spec_path`
- phase `receipt_path`
- phase `evidence_paths`

If a future workflow needs immutable snapshots, add explicit `snapshots/` support with clear names:

```text
snapshots/
  dispatch.md
  runway-spec.md
```

That should be a deliberate feature, not part of the first layout fix.

## Dirty Worktree Policy

Update expected dirty-path classification so structured artifacts are expected during runner phases:

- `artifact_root/`
- `run-state.json`
- `run-manifest.json`
- current `batch-manifest.json`
- current `index.md`
- current phase receipt

The runner should still reject unrelated dirty project files before planning or closeout. The layout change should not loosen code-safety behavior.

## Tests

Add focused tests in `codex-config/tests/test_architecture_program_runner.py`:

- New runs default state under `architecture-program-runs/<ledger-stem>/<run-id>/run-state.json`.
- `run_id` is stable across resume and does not change per phase.
- Prompt generation includes the expected phase receipt path.
- Phase result validation rejects receipts outside the expected run or batch artifact directory for new structured runs.
- `select-dispatch` can return a batch ID and initialize the batch artifact root.
- `create-spec`, `execute`, and `closeout` use batch-local ordered receipt paths.
- `run-manifest.json` is written after phase completion and contains program ledger, state path, batch ID, dispatch path, spec path, and last receipt path.
- `batch-manifest.json` is written once a batch exists and links to dispatch and spec.
- Dirty-worktree classification allows structured runner artifacts but still rejects unrelated project files.
- Old flat-state resume remains supported.

Update local runner reference tests to assert the documented artifact layout.

## Implementation Slices

### Slice 1: Path Model And Documentation

Add path helpers to the runner:

- `default_artifact_root(project, program_ledger, run_id)`
- `new_run_id(initial_batch_id=None)`
- `phase_receipt_path(state, phase)`
- `batch_artifact_root(state, batch_id)`
- `run_manifest_path(state)`
- `batch_manifest_path(state, batch_id)`

Update `local-runner-v1.md` with the structured artifact layout and the rule that phase agents use runner-provided receipt paths.

Validation:

```bash
pytest tests/test_architecture_program_runner.py -q
```

### Slice 2: Structured State For New Runs

Initialize new runs with `run_id`, `artifact_root`, `run_manifest_path`, and the new default `state_path`.

Keep explicit `--state` and old state resume behavior.

Validation:

```bash
pytest tests/test_architecture_program_runner.py -q
```

### Slice 3: Deterministic Receipt Paths

Teach prompt generation to provide an expected phase receipt path. Validate that phase results use it for structured runs.

For `select-dispatch`, use a run-level receipt path if the batch ID is unknown before the phase:

```text
<artifact-root>/receipts/01-select-dispatch.json
```

After a batch ID is known, subsequent receipts should be batch-local:

```text
<artifact-root>/batches/<batch-id>/receipts/02-create-spec.json
```

Do not move the `select-dispatch` receipt after the batch is known. For multi-batch runs, use the next run-scoped selection number so later selections do not overwrite earlier receipts.

Validation:

```bash
pytest tests/test_architecture_program_runner.py -q
```

### Slice 4: Manifests And Human Index

Write `run-manifest.json` after every phase. Write `batch-manifest.json` and `index.md` after `batch_id` exists.

Keep manifests compact. They are trace anchors, not execution logs.

Validation:

```bash
pytest tests/test_architecture_program_runner.py -q
```

### Slice 5: Integration Rehearsal

Run a dry or stopped single-batch rehearsal against a throwaway fixture project or a safe local sample to verify the visible file tree.

Expected evidence:

- `run-state.json` in the run directory.
- `run-manifest.json` in the run directory.
- batch-local manifest and index.
- ordered receipts.
- final summary includes `artifact_root`.
- old flat state can still resume when explicitly passed with `--state`.

Validation:

```bash
pytest tests/test_architecture_program_runner.py -q
ruff check scripts/architecture_program_runner.py tests/test_architecture_program_runner.py
```

## Non-Goals

- Do not change the phase-result JSON schema unless deterministic paths require a new optional field.
- Do not make the runner parse or edit program ledgers beyond existing phase-agent responsibilities.
- Do not copy or snapshot dispatch/spec files by default.
- Do not change Batch Runway execution semantics.
- Do not broaden sandbox defaults.
- Do not try to clean up old flat artifacts automatically during normal resume.

## Acceptance Criteria

- New architecture-program runner invocations no longer dump state and receipts directly into `my-docs/plans/`.
- A user can browse from `architecture-program-runs/<ledger-stem>/<run-id>/batches/<batch-id>/` to the program ledger, dispatch packet, concrete runway spec, and phase receipts.
- Receipts are phase-ordered and batch-local where possible.
- Final summaries name `artifact_root`.
- Old stopped runs can still resume with explicit old state paths.
- Tests cover path generation, prompt instructions, receipt validation, manifests, dirty-worktree classification, and old-state compatibility.
