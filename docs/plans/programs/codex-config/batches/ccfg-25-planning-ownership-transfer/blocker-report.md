# CCFG-25 Slice 2 Blocker Report

## Status

```yaml
batch: ccfg-25-planning-ownership-transfer
slice: 2
status: resolved
blocker_class: required-green-validation-command-contract
stable_planning_commit: 24f5ab9b66bb0e0060df5b8483597cbb5c5146d9
candidate_head: 12f70727f7496e2aa2d5fff9b748ee97e19e63a2
candidate_diff_sha256: 815c4ad7b15e9143cb95e3f5790440021416ccb28bd8120731ac92314c8b023e
candidate_commit_created: true
independent_planning_review: clean
independent_implementation_review: clean
closeout_created: false
successor_selected: false
```

## Executive Summary

This report is retained as historical blocker evidence. The user authorized the
command-only amendment, exact independent planning review was clean, both
single-document structural commands passed, and the preserved diff was committed
unchanged as `12f70727f7496e2aa2d5fff9b748ee97e19e63a2`. Slice 2 is complete;
Slice 3 remains pending, with no closeout or successor selected.

The second bounded amendment resolved the runner safety blocker inside the exact
authorized two-file ceiling. The compatibility `create-spec` allowance now
accepts only canonical artifacts bound to the immediately preceding completed
`plan-batch` transaction, and independent review confirms the forged-transaction
case is rejected.

Slice 2 is still stopped because the exact user-mandated required-green command
is not a structural two-file validation. With two inputs, `skill_contract.py`
automatically validates them as a relationship catalog. Both contracts truthfully
require `planning-artifacts` and `planning-state`, but those mechanisms are not
members of the two-path catalog and the CLI exposes no external-mechanism policy.
The command therefore exits `1` with four
`catalog.unknown_required_mechanism` diagnostics.

## Exact Failing Gate

```sh
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/architecture-program-runway/SKILL.md \
  skills/legacy-removal/SKILL.md
```

Observed diagnostics:

- `architecture-program-runway` requires external mechanisms
  `planning-artifacts` and `planning-state`;
- `legacy-removal` requires the same two external mechanisms; and
- neither mechanism is present in the explicit two-document catalog or allowed
  by a CLI policy.

Each skill validates cleanly when invoked alone. The existing catalog and
migration tests also pass and retain relationship-level proof. The failure is
therefore the combined command's catalog semantics, not a malformed contract.

## Why The Candidate Must Remain Uncommitted

- This command is explicitly classified as required-green in the reviewed
  runway.
- Removing the two truthful `requires.mechanisms` lists would falsify the skill
  contracts and violate their preserved layout/Planning State responsibilities.
- `scripts/skill_contract.py` is outside the exact Slice 2 ceiling, and changing
  it would be a validator behavior expansion rather than this command-only fix.
- Replacing or reclassifying the exact command contradicts the current explicit
  authorization and requires a newly reviewed amendment.

## Resolved Runner Safety Correction

The newly authorized Change Allowance implementation and focused test are
complete but uncommitted. They now:

- use canonical planning-contract validators and readers;
- bind the completed transaction producer, canonical sibling `CURRENT.md`,
  configured ledger, batch, dispatch, runway, queued state, and observed
  revisions and SHA-256 hashes;
- accept only exact transaction-owned `CURRENT.md`, dispatch, runway, and
  selection-transaction paths;
- reject parent planning directories, arbitrary evidence paths, arbitrary
  Markdown, unrelated planning files, and unrelated project files; and
- leave execute and closeout allowances unchanged.

The positive regression executes a real complete `plan-batch` transaction. The
negative regression proves that a schema-valid transaction attempting to
substitute `README.md` as `CURRENT.md` does not expand the allowance.

## Validation Evidence

- Exact Slice 2 matrix: `181 passed, 241 subtests passed`.
- Filtered manifest: `21 passed, 1 deselected, 210 subtests passed`.
- Filtered legacy/projection gate: `7 passed, 18 deselected, 20 subtests passed`.
- Scenario catalog: `69 scenarios` valid.
- Five required skill quick-validations: clean.
- Ruff: clean.
- BasedPyright: `0 errors, 0 warnings`.
- `git diff --check`: clean.
- Full manifest retains only the named CCFG-26 failure.
- The six broad legacy diagnostic failures remain a subset of the 12 failures at
  the exact candidate baseline.
- Independent Change Allowance re-review: prior safety finding resolved.
- Exact combined skill-contract command: failed with the four diagnostics above.

## Smallest Authorization Needed To Resume

Authorize a validation-command-only amendment that replaces the combined
invocation with two required-green structural invocations:

```sh
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/architecture-program-runway/SKILL.md
.venv/bin/python scripts/skill_contract.py validate \
  --toolchain-root . \
  skills/legacy-removal/SKILL.md
```

Keep the existing catalog, migration, routing, and quick-validation gates for
relationship proof. This correction requires no candidate code change, no new
implementation path, no validator change, and no scope widening. Before resuming
the same preserved Slice 2 diff, update the exact runway command and obtain a
fresh independent planning review.

That authorization has now been applied. CCFG-25 remains active with Slice 2
complete and Slice 3 pending. Slice 1 stays closed, CCFG-26 responsibilities
remain preserved, and no closeout or successor was created.
