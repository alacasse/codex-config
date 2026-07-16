# GitHub Issue #56 — CCFG-23 Harness Simplification And Deletion-First Migration

## Source

- GitHub issue: #56, `Simplify CCFG-23 acceptance execution and delete test-retained harness topology`
- Evidence:
  `docs/plans/programs/codex-config/batches/ccfg-23-behavioral-scenario-harness/execution-retrospective.md`
- Affected candidate surface:
  `implementation/command-owner-redesign`
- Existing closed source finding: CCFG-23 / COR-006

## Finding

CCFG-23 correctly produced a topology-independent behavioral oracle, but the
acceptance execution model is disproportionate and risks becoming a permanent
parallel implementation:

- the report command starts pytest recursively;
- one observed report starts 13 pytest processes;
- evidence and determinism tests repeatedly rebuild all 69 scenarios;
- the focused 123-test suite takes about 13 minutes 34 seconds and performs an
  estimated 35 full catalog evaluations;
- individual pytest-function source hashes preserve test topology without
  creating an independent trust boundary; and
- fixture workflow models will become duplicate owners unless CCFG-24 through
  CCFG-29 delete them as real command owners take over.

CCFG-23 remains closed. This finding changes acceptance execution and
migration-retention surfaces only; it does not weaken or reinterpret COR-006.

## Required Contract

Preserve:

- all 31 immutable contract identities;
- the required behavior families;
- the meaning of all six COR-006 acceptance keys and required aliases;
- fail-closed rejection of skip, xfail/xpass, deselection, zero-test
  collection, assertion failure, setup error, missing or foreign interpreter,
  repository movement, wrong roots or generation, and unauthorized writes;
- exact stable/candidate provenance and topology-independent target behavior.

Do not preserve merely because a test asserts it:

- exact scenario or test counts;
- scenario IDs, test names, or file paths that are not accepted contracts;
- hashes of individual pytest function bodies;
- reporter-owned pytest execution;
- adapter, import, module, or fixture topology; or
- migration-retention models after a real command owner supplies the behavior.

Tests are evidence to classify, not automatic liveness evidence. A failing
`topology-assertion` or `migration-retention` test must be deleted or migrated
unless it protects a named external compatibility contract.

## Required Design

### Exact-commit acceptance receipt

One explicit acceptance command must:

1. verify a clean candidate worktree and exact candidate commit;
2. bind catalog, schema, harness, adapter, and evidence-test source digests;
3. run all declared evidence nodes in one pytest process and one JUnit result;
4. reject every non-exclusive pass, including skip, xfail/xpass, deselection,
   zero tests, failure, and error;
5. evaluate each immutable scenario at most once per process/input identity;
6. record interpreter provenance, counts, JUnit digest, and wall duration; and
7. emit one immutable acceptance report inside the receipt.

`report` must not start pytest. It may render an unobserved report or verify and
render a matching exact-commit receipt. JSON and text rendering must be pure
functions over one report object.

### Fast and acceptance gates

The fast gate covers schema/YAML validation, mappings, exact observation
comparison, receipt validation, aggregate derivation, and pure rendering. It
must not create Git repositories, invoke installers, or start nested pytest.

The acceptance gate covers runtime evidence, disposable Git/Planning State/
install/cutover behavior, false-green rejection, exact-commit receipt
production, and the final report.

A green receipt may be reused by worker, coordinator, and reviewer only for the
same immutable commit and matching digests. Any repository or input movement
invalidates it.

### Deletion-first test migration

For every failing test during the reduction, classify it as `behavioral`,
`compatibility-contract`, `migration-retention`, or `topology-assertion`.

- Repair the implementation only for lost behavior or a named compatibility
  contract.
- Migrate ordinary behavior tests to the new owner.
- Delete topology/import/identity tests that only preserve the removed
  mechanism.
- Never restore removed code solely to make such a test green.

The combined harness-and-test diff must be net negative. Do not add a wrapper,
alias, public API, cache layer, or permanent schema whose purpose is to preserve
old topology.

## CCFG-24 Through CCFG-29 Carry-Forward

CCFG-23 is an oracle, not a permanent parallel owner.

- CCFG-24 rebinds intake scenarios to `add-to-ledger` and deletes replaced
  intake adapters and migration-retention tests.
- CCFG-25 rebinds planning scenarios to `plan-batch` and deletes the fixture
  planning state machine plus replaced APR/Batch Runway ownership tests.
- CCFG-26 rebinds execution and closeout scenarios to `work-batch` and deletes
  duplicate fixture worker, validator, reviewer, committer, and closeout logic.
- CCFG-27 and CCFG-28 replace synthetic readiness/cutover paths where real
  candidate behavior becomes authoritative, retaining only fault fixtures that
  still prove a real boundary.
- CCFG-29 removes all remaining migration-retention adapters, bridge/wrapper
  topology, and their preserving tests.

Every temporarily retained surface must name its caller, reason, owner, and
removal condition.

## Acceptance

Behavioral:

- all six COR-006 keys and aliases retain the same meaning and are green;
- all 31 contracts and required families remain covered; and
- every existing false-green class remains rejected.

Structural:

- `report` contains no pytest subprocess launch;
- one acceptance run uses one pytest invocation for all evidence nodes;
- each immutable scenario is evaluated at most once per process/input identity;
- the suite has one end-to-end acceptance execution;
- JSON/text determinism reuses one report object;
- per-function `source_sha256` is absent from authoritative acceptance evidence;
- removed symbols and paths are absent, with preserving tests deleted or
  migrated; and
- the implementation and test diff is net negative.

Performance, measured old versus new on the same machine and exact commit:

- at least 70 percent fewer subprocesses;
- at least 60 percent lower complete acceptance wall time;
- target 3–5 minutes or better for the acceptance gate; and
- target below one minute for the fast gate.

These are comparative goals, not universal hard timeouts.

## Scope And Sequencing

- New ledger identity: CCFG-33.
- Recommended before CCFG-24.
- CCFG-23 remains closed.
- No production command-owner transfer, real cutover, default-generation
  switch, or bridge deletion belongs to CCFG-33.
- `plan-batch` must derive semantic boundaries from the actual change and must
  not force a fixed slice count.
- Closeout stops without selecting a successor.
