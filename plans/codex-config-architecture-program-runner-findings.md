# Codex Config Architecture Program Runner Findings

## Purpose

Keep the architecture-program runner findings visible across multiple future
runways. This ledger sits above individual Batch Runway specs and reconciles
the older runner block reports with the current code state.

## Current Direction

- Keep `architecture-program-runway` responsible for program selection,
  dispatch, and closeout; keep `batch-runway` responsible for concrete
  execution.
- Keep the Python runner project-neutral. Do not add Graphify-specific
  validation, cache, or ledger parsing logic.
- Preserve the single-level phase model: the outer runner launches phase-level
  `codex exec`; phase agents must not launch nested Codex or recursively run
  the local runner.
- Preserve structured run artifacts under the program ledger directory:
  `architecture-program-runs/<ledger-stem>/<run-id>/`.
- Keep phase receipts compact and put telemetry or input evidence beside them.

## Source Context

- Current baseline: `bad11cf Add telemetry support for structured runs in architecture program runner`
- Main code: `scripts/architecture_program_runner.py` (1700 lines)
- Main tests: `tests/test_architecture_program_runner.py` (1286 lines)
- Secondary code: `scripts/codex_owner.py` and `tests/test_codex_owner.py`
- Protocol reference: `skills/architecture-program-runway/references/local-runner-v1.md`
- Prior design plans:
  - `plans/local-architecture-program-runner.md`
  - `plans/codex-config-architecture-program-artifact-layout-plan.md`
  - `plans/codex-config-architecture-program-telemetry-recommendations.md`
- Prior block reports:
  - `plans/architecture-program-runner-schema-error-report.md`
  - `plans/architecture-program-runner-summary-schema-error-report.md`
  - `plans/architecture-program-runner-execute-validation-block-report.md`
  - `plans/architecture-program-runner-nested-validation-block-report.md`
  - `plans/architecture-program-runner-env-pass-through-remediation-report.md`
  - `plans/architecture-program-runner-commit-block-report.md`
  - `plans/codex-config-closeout-nested-codex-issue.md`

## Findings Ledger

| Finding | Status | Covered by | Next action | Notes |
|---|---|---|---|---|
| APR-1. Unsupported Codex output schema composition | Closed | `6a00343`, `0cfeeda`; `tests/test_architecture_program_runner.py::test_phase_result_schema_uses_codex_output_subset` | None | Prior reports show `if`/`then`/`else` schema keywords blocked `codex exec --output-schema`; current tests enforce the supported subset. |
| APR-2. Phase summaries needed compact string/null shape | Closed | `0cfeeda`; phase schema and validation tests | None | Current schema keeps `validation_summary` and `review_summary` compact strings or null, avoiding nested summary objects. |
| APR-3. All-batches and direct CLI batch bounds needed stable semantics | Closed | `f657019`; runner tests for unbounded mode and terminal states | None | Current CLI distinguishes direct one-batch default from skill-mediated all-batches behavior. |
| APR-4. Environment/cache pass-through was unclear for nested validation | Closed | `f5b284c`, `8755f86`, `d1ae6ef`; env override tests and prompt checks | None | Runner now accepts repeated `--env`, preserves base env, hides values, and asks phases for coordinator-shell env probes. |
| APR-5. Stopped execute runs could not resume with their own evidence paths | Closed | `8755f86`; dirty-worktree tests for stopped receipt evidence paths | None | Current dirty-file classifier allows evidence paths from stopped receipts for the same active phase. |
| APR-6. Execute phases that must commit need a separate sandbox control | Closed | `58ebd36`; `--execute-sandbox` tests and docs | None | Current runner can broaden only `execute` for Git metadata writes without broadening planning or closeout. |
| APR-7. Closeout phase could launch nested Codex and fail in managed sandboxes | Closed | `196c359`; prompt/reference tests for single-level phase model | None | Current prompts explicitly forbid nested `codex exec`, local-runner recursion, runtime probes, and temp `CODEX_HOME` workarounds. |
| APR-8. Flat runner artifacts hid run and batch boundaries | Closed | `01111f5`, `b3aaeca`; structured artifact tests | None | New runs use run-scoped state, ordered receipts, run/batch manifests, and batch indexes under `<ledger-dir>/architecture-program-runs/...`. |
| APR-9. Runner telemetry needed direct resource measurements | Prepared | `bad11cf`; telemetry tests and `codex-config-architecture-program-telemetry-recommendations.md` | Create a follow-up attribution batch after the runner boundary batch | Current code writes phase and run telemetry, but exact Codex session JSONL discovery remains missing unless a path is supplied. |
| APR-10. Input inventory is prompt guidance only | Open | Prompt text in `build_prompt`; no schema or enforcement | Add an input-inventory contract batch after attribution is stable | Prompts ask phases to write inventories for broad reads, large files, and subagent reports, but the runner does not validate existence, shape, or manifest linkage. |
| APR-11. `architecture_program_runner.py` concentrates too many responsibilities | Ready | None | Next selected batch: split runner internals into seam-owned modules while preserving CLI behavior | The script mixes CLI/config, path/state, phase-result validation, prompt construction, subprocess execution, Git dirty policy, artifact manifests, and telemetry. This increases edit risk and context cost. |
| APR-12. Tests mirror the large runner file as one broad suite | Open | None | Split tests along the same owner seams as production modules | `tests/test_architecture_program_runner.py` is 1286 lines and exercises many unrelated behaviors in one file. |
| APR-13. Structured failure paths do not refresh manifests consistently | Closed | Runner boundary Slice 4; `tests/test_architecture_program_runner_artifacts.py` malformed-result failure-path regression | None | Structured `RunnerError` paths now refresh manifests when active batch state exists, preserve validation errors for malformed results, and attribute phase telemetry/manifests through `active_batch_id`. |
| APR-14. Prior planning docs are useful but stale as coordination state | Prepared | This ledger | Use this ledger as the coordination surface; leave older reports as evidence | Artifact layout and telemetry plans still describe proposed work that has since partially landed. Future agents should not re-derive current state from all raw reports. |
| APR-15. `codex_owner.py` is small and currently not the architecture hotspot | Deferred | `tests/test_codex_owner.py` passing | Revisit only when ownership behavior changes | Current code is 221 lines with focused tests; no broad refactor is justified now. |

## Batch Queue

| Batch | Findings | Status | Why grouped | Depends on | Validation class | Dispatch | Spec |
|---|---|---|---|---|---|---|---|
| runner-boundary-split | APR-11, APR-12, APR-13 | Ready | Shared owner seam around runner internals and tests; creates safer boundaries for future telemetry/input work | None | Focused unit tests plus runner dry-run smoke where practical | `plans/dispatch/runner-boundary-split-dispatch.md` | `plans/codex-config-architecture-program-runner-boundary-split-runway.md` |
| telemetry-session-attribution | APR-9 | Candidate | Exact session/path harvesting and token parsing should sit behind a telemetry seam after extraction | runner-boundary-split | Unit tests with synthetic session logs; optional live runner rehearsal | TBD | TBD |
| input-inventory-contract | APR-10 | Candidate | Input inventory needs its own schema/validation and manifest linkage after telemetry paths settle | runner-boundary-split, telemetry-session-attribution preferred | Unit tests with synthetic inventories and prompt checks | TBD | TBD |
| planning-doc-closeout | APR-14 | Deferred | Documentation cleanup is lower risk and should not block runner seams | runner-boundary-split | Markdown/readback only | TBD | TBD |

## Selected Batch Brief

- Batch: `runner-boundary-split`
- Dispatch: `plans/dispatch/runner-boundary-split-dispatch.md`
- Status: `Ready`
- Notes: Start by extracting runner seams without changing the CLI, receipt schema, artifact layout, or phase semantics.

## Recommended Work Order

1. `runner-boundary-split`: reduce the 1700-line runner and 1286-line test file
   into seam-owned modules/tests while preserving behavior.
2. `telemetry-session-attribution`: once telemetry helpers have a clear owner,
   improve exact session JSONL discovery and attribution.
3. `input-inventory-contract`: add a schema and validation path for the
   phase-reported input inventory.
4. `planning-doc-closeout`: mark or archive stale proposal docs after the
   functional seams are stable.

## Closeout Rules

- Mark `APR-11` closed only after the runner internals are split, focused tests
  pass, and the CLI remains runnable from `scripts/architecture_program_runner.py`.
- Mark `APR-12` prepared if only new tests are split; close it only when the
  large test file no longer owns unrelated runner behavior.
- Mark `APR-13` closed only if failure-path manifests are refreshed or if a
  documented decision explicitly keeps manifests success-only.
- Keep `APR-9` and `APR-10` open unless the selected batch directly implements
  session attribution or inventory validation.

## Validation Snapshot

- `python -m pytest tests/test_architecture_program_runner.py tests/test_codex_owner.py -q`: `64 passed in 0.36s`
- `python -m ruff check ...`: blocked locally because `/usr/bin/python` has no
  `ruff` module installed.
