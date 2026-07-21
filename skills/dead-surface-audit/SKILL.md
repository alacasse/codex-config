---
name: dead-surface-audit
description: Audit code surfaces that appear alive only because tests assert imports, aliases, topology, or compatibility rather than externally observable behavior.
---

# Dead Surface Audit

Determine whether tests are protecting useful behavior or merely keeping an
obsolete surface present. This skill produces evidence; it does not authorize
deletion or implement cleanup.

## Evidence statuses

Use exactly these project-neutral statuses:

- `keep`: a supported external contract or deep module still needs the surface;
- `delete-now`: no supported caller or contract exists;
- `migrate-tests-first`: behavior tests can move to the canonical owner;
- `keep-thin-entrypoint`: a real external entrypoint needs a narrow adapter;
- `human-contract-decision`: external compatibility may matter, but evidence is
  ambiguous.

Labels invented by a local project are not substitutes for these statuses.

## Workflow

### 1. Establish the intended contract

Read user-facing documentation, entrypoints, relevant decisions, production
callers, and public compatibility commitments. Treat tests as evidence, not
automatic proof of support.

### 2. Inventory suspect surfaces

List the modules, functions, aliases, wrappers, re-exports, fallback branches,
and path mutations under review. Look closely at surfaces described as legacy,
compatibility, deprecated, facade, wrapper, or temporary.

### 3. Split caller evidence

Separate callers into:

- production/runtime code;
- public CLI or module entrypoints;
- generated or serialized external contracts;
- current documentation;
- tests;
- historical migration notes.

Use static search first and verify dynamic import behavior with focused checks.

### 4. Run the dual deletion test

Ask twice:

1. With tests excluded, would deletion break supported behavior or move real
   complexity into production callers?
2. With tests included, do failures only assert importability, alias identity,
   wrapper shape, path existence, or topology?

If only topology-oriented tests fail, the surface is deletion-biased unless a
named compatibility contract says otherwise.

### 5. Classify preserving tests

- `behavioral`: proves user-visible output, file effects, API behavior, state,
  or another observable contract;
- `compatibility-contract`: protects a documented old path still used outside
  the repository;
- `migration-retention`: temporarily preserves an old owner during movement;
- `topology-assertion`: protects imports, aliases, wrappers, or module shape
  without behavior.

### 6. Report the decision evidence

For each suspect surface report files, caller evidence, test class, deletion
test result, status, uncertainty, and the smallest justified next action.
Require a named caller or contract before recommending `keep`. Require a
decision owner when using `human-contract-decision`.

## Report shape

Lead with findings ordered by deletion confidence, then include a compact table:

```text
Surface | Production callers | Test-only callers | Contract evidence | Status | Next action
```

Do not create queues, execution state, cleanup protocols, or compatibility
wrappers as part of the audit.
