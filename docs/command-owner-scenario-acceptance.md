# Command-Owner Scenario Acceptance

## Purpose

The command-owner scenario catalog is a behavioral migration oracle. It is not
an installed runtime owner and must not become a permanent parallel
implementation beside `add-to-ledger`, `plan-batch`, or `work-batch`.

The acceptance workflow separates fast structural checks from exact-commit
runtime evidence. Reporting never launches pytest.

## Fast Gate

Run the schema, catalog, mapping, comparison, receipt-shape, and pure rendering
checks during implementation:

```bash
uv run --frozen pytest tests/test_command_owner_scenario_catalog.py -q
```

The fast gate must not create disposable Git repositories, run installation or
cutover fixtures, or launch nested pytest.

Use the smallest directly affected runtime test when changing an adapter. Do
not rerun the complete acceptance flight after every edit.

## Exact-Commit Acceptance Gate

Acceptance requires a clean committed candidate worktree and a receipt path
outside the repository:

```bash
uv run --frozen python scripts/command_owner_scenarios.py \
  accept tests/fixtures/command-owner-scenarios \
  --receipt /tmp/command-owner-acceptance.json \
  --format json
```

The acceptance command:

- records the exact candidate commit and verifies a clean worktree;
- binds the catalog, schema, harness, fixture, adapter, and evidence-test source
  set;
- validates the candidate `.venv` interpreter and Python safe-path mode;
- runs every declared aggregate-evidence node in one pytest process and one
  JUnit result;
- rejects skip, xfail/xpass, deselection, zero tests, assertion failure, setup
  error, and missing declared evidence functions;
- evaluates each immutable scenario at most once per process and source
  identity;
- records test counts, JUnit digest, and wall duration; and
- stores the accepted report in the exact-commit receipt.

The receipt is evidence, not repository state. Do not commit it.

## Pure Reporting And Receipt Reuse

Render an unobserved report without executing pytest:

```bash
uv run --frozen python scripts/command_owner_scenarios.py \
  report tests/fixtures/command-owner-scenarios \
  --format json
```

Its aggregate keys intentionally remain false because declarations and test
names cannot self-certify acceptance.

Render a previously accepted report after verifying the current commit and
source identity:

```bash
uv run --frozen python scripts/command_owner_scenarios.py \
  report tests/fixtures/command-owner-scenarios \
  --receipt /tmp/command-owner-acceptance.json \
  --format text
```

Worker, coordinator, and reviewer may reuse the same green receipt only while:

- the candidate commit is unchanged;
- the worktree is clean;
- catalog and source digests match;
- the declared evidence-node set matches; and
- the candidate interpreter identity still matches.

Any movement invalidates the receipt and requires a new acceptance flight.
JSON and text determinism must be tested by rendering the same report object,
not by rerunning acceptance.

## Deletion-First Test Handling

When simplification or ownership transfer breaks a test, classify the test
before changing production code:

- `behavioral`: preserve the externally observable outcome;
- `compatibility-contract`: preserve only when a named supported caller or
  documented old path exists;
- `migration-retention`: migrate to the new owner and delete the old fixture or
  adapter;
- `topology-assertion`: delete when it only checks imports, aliases, identity,
  module presence, paths, or old ownership shape.

Never restore removed code solely to make a migration-retention or
 topology-assertion test green. The test must move or disappear with the
mechanism it protected.

Individual pytest-function source hashes are deprecated migration metadata and
are not acceptance authority. Exact commit, clean source identity, runtime
collection, JUnit evidence, and independent review form the trust boundary.

## Owner-Transfer Cleanup

As real command owners become authoritative:

- CCFG-24 deletes replaced intake adapters and tests;
- CCFG-25 deletes the fixture planning state machine and replaced planning-owner
  tests;
- CCFG-26 deletes duplicate worker, validator, reviewer, committer, recovery,
  receipt, and closeout fixture logic;
- CCFG-27 and CCFG-28 replace synthetic readiness and cutover paths where real
  candidate behavior supplies the evidence; and
- CCFG-29 deletes every remaining migration-retention adapter, bridge wrapper,
  alias, and topology-preserving test.

A temporary surface may remain only with a named caller, reason, owner, and
removal condition.

## Performance Evidence

The CCFG-23 retrospective records the baseline focused suite at 814.32 seconds,
one observed report at about 92.20 seconds, and an estimated 35 complete catalog
evaluations per run. A CCFG-33 closeout must compare the new exact-commit gate on
the same machine and record:

- complete wall duration;
- receipt-reported evidence duration;
- subprocess count or an equivalent measured profile;
- fast-gate duration; and
- the exact candidate commit.

The comparative goals are at least 70 percent fewer subprocesses and at least
60 percent lower acceptance time, with targets of 3–5 minutes or better for
acceptance and less than one minute for the fast gate. These are evidence goals,
not universal hard timeouts.
