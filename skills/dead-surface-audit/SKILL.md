---
name: dead-surface-audit
description: Agent-facing evidence audit for code surfaces that appear alive only because tests assert imports, aliases, topology, or compatibility rather than externally observable behavior.
---

# Dead Surface Audit

Agent-facing evidence support for finding Modules that are dead or obsolete but
hidden behind tests that keep asserting the old surface exists.

Core rule: tests are not automatically liveness evidence. A test can be the only thing keeping a shallow Module present.

Role boundary: this skill is an evidence producer only for exceptional residue
or test-retained surface investigations. It may feed `legacy-removal` or public
`plan-batch` handoffs, but it does not create durable program ledgers, program
queue state, selected-batch state, dispatch packets, batch runways, lifecycle
mutations, commits, closeout records, or a human-facing cleanup command.
This deletion-liveness evidence handoff grants no queue, dispatch, runway, or
lifecycle mutation authority.

Deletion-test evidence vocabulary owner: this skill owns the canonical
project-neutral evidence statuses used when reporting deletion-test results:
`keep`, `delete-now`, `migrate-tests-first`, `keep-thin-entrypoint`, and
`human-contract-decision`. Treat generated labels such as `no-op`, `sediment`,
`obsolete skill surface`, and `deletion-safe evidence` as non-canonical
deletion-test evidence categories unless a specific local artifact explicitly
defines them as non-canonical labels. Do not use this vocabulary ownership as
authority to select program work, queue batches, execute cleanup, or approve
deletions.

## Workflow

### 1. Establish the Intended Contract

Read the relevant project instructions, domain glossary, ADRs, user-facing docs, CLI/module entrypoints, generated artifact contracts, and public import commitments.

Record which surfaces are truly supported externally. Treat repo-local tests as evidence to classify, not as proof of support.

### 2. Inventory Suspect Surfaces

List files, Modules, functions, classes, aliases, exported names, and invocation paths under review.

Prioritize surfaces with names or comments like `compatibility`, `facade`, `legacy`, `deprecated`, `wrapper`, `alias`, `re-export`, `root topology`, `historical evidence`, `cleanup residue`, or old domain vocabulary. Also inspect tiny helpers, aggregate modules, and root files that only import from owner packages.

### 3. Split Caller Evidence

Build a caller map split into these buckets:

- production/runtime code
- CLI or module entrypoints
- generated artifacts or serialized contracts
- docs or ADRs
- tests
- historical plans or migration notes

Use static search first (`rg`, import graph, AST scans). Verify dynamic imports with focused commands.

### 4. Run the Dual Deletion Test

Apply the deletion test twice:

1. With tests excluded: would deleting the surface move real complexity into production/runtime callers or break a supported external contract?
2. With tests included: do failures come only from tests that assert importability, identity, alias presence, path existence, or topology?

If only tests break, the surface is likely dead, transitional, or supported only by an explicit compatibility decision.

### 5. Classify the Tests

Classify each test that preserves the surface:

- `behavioral`: proves externally observable behavior such as CLI output, file effects, persisted state, report fields, API responses, or generated artifacts
- `compatibility-contract`: protects a documented public old path that users still rely on
- `migration-retention`: keeps a temporary facade/wrapper/import path around after owner Modules already exist
- `topology-assertion`: asserts module presence, absence, identity aliases, `find_spec`, `__all__`, or import shape without proving behavior

Flag `migration-retention` and `topology-assertion` tests as suspect when no external contract exists.

### 6. Decide the Surface Status

Use these statuses:

- `keep`: supported external contract or deep Module; deletion would spread real complexity
- `delete-now`: no production/runtime/docs contract and tests only preserve old shape
- `migrate-tests-first`: ordinary behavior tests import the old surface but can move to owner Modules
- `keep-thin-entrypoint`: true CLI/module entrypoint; keep parse/delegate behavior and move implementation behind owner seams
- `human-contract-decision`: evidence suggests external compatibility may matter, but support is undocumented or ambiguous

Do not keep compatibility just because a test asserts it. Require a named caller, document, invocation path, generated artifact, or explicit ADR.
For test-only cleanup residues or historical-evidence markers, require a named
reason when suggesting `keep` or `keep-thin-entrypoint`. Require a removal
condition or follow-up decision owner when suggesting temporary or deferred
retention such as `migrate-tests-first` or `human-contract-decision`.

## Report Format

Lead with findings, ordered by deletion confidence. Keep reports as evidence
handoff material; do not turn them into program selection, queue, or concrete
execution state.

```markdown
## Findings

### 1. <surface> is kept alive only by <test class>

- Files: ...
- Status: delete-now | migrate-tests-first | keep | keep-thin-entrypoint | human-contract-decision
- Caller evidence: production/runtime ..., tests ..., docs/entrypoints ...
- Dead-test signal: why the tests preserve shape rather than behavior
- Deletion test: what breaks without tests, what breaks with tests
- Suggested action: delete, migrate tests, narrow entrypoint, or ask for contract decision
```

Then include a compact inventory table: `Surface | Production callers | Test-only callers | Contract evidence | Status | Next action`.

## Heuristics

- A facade with owner Modules and no production callers is deletion-biased.
- A root file must earn its place as an entrypoint, deep seam, or root-owned asset.
- `__all__`, alias identity, and importability tests usually prove compatibility shape, not behavior.
- A compatibility test is valid only when it names the old path and the reason it remains supported.
- If deleting a Module only requires deleting or rewriting tests, call that out directly.
- When unsure, propose the smallest characterization slice that separates external contracts from test-retained shape.
