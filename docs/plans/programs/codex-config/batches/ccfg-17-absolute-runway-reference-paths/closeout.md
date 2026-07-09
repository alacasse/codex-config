# CCFG-17 Absolute Runway Reference Paths Closeout

## Result

CCFG-17 is ready for coordinator closeout. The batch changed Batch Runway
generated-artifact guidance so reusable repo-owned skill references use
repo-relative or skill-relative paths, then added focused tests and an
active-artifact guard for selected, queued, or active runway files.

## Evidence

- Slice 1 commit `bc4175c`: replaced local absolute Batch Runway reference
  examples in create-spec guidance while preserving legitimate absolute
  runtime handoffs.
- Slice 2 commit `70324f8`: added focused contract tests that keep generated
  Batch Runway reference examples relative.
- Slice 3 commit `29b06e5`: added an active-runway guard that checks live
  selected, queued, or active artifacts without failing completed historical
  runways.
- Slice 4 updates Batch Runway release metadata and changelog evidence for the
  guidance change.

## Validation

- `python -m pytest tests/test_batch_runway_create_spec_contract.py -q`: passed,
  16 tests.
- `python -m pytest tests/test_codex_features_manifest.py -q`: known-red
  diagnostic baseline, 15 passed and 3 failed in unrelated command-owner
  wording expectations.
- `python -m json.tool codex-features.json`: passed.
- `python -m ruff check tests/test_batch_runway_create_spec_contract.py`:
  failed/unavailable with `/usr/bin/python: No module named ruff`, matching the
  known-red ruff-unavailability baseline.
- `git diff --check`: passed.

## Remaining Risks

- No known remaining CCFG-17 risks.
- No historical completed runway artifacts were rewritten.
- Program `CURRENT.md` and `LEDGER.md` still need coordinator-owned closeout
  reconciliation after this concrete closeout evidence is committed.
