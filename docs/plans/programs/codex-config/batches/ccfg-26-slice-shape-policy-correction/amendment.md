# CCFG-26 Slice-Shape Policy Planning Amendment

## Status

- Status: accepted bounded planning amendment.
- Applies to: `dispatch.md` and `runway.md` in this batch.
- Source: user decision after independent review of the queued plan.
- Scope: planning correction only; implementation has not started.
- Precedence: when this document conflicts with the queued dispatch or runway, this amendment controls.
- CCFG-26A remains completed historical evidence.
- CCFG-26B through CCFG-26E remain unselected.

The original dispatch and runway remain preserved as the exact reviewed planning
snapshot. This amendment narrows and clarifies execution without rewriting that
historical snapshot.

## Configuration Format Decision

The project-owned policy is a directly parseable YAML configuration file:

```text
docs/plans/programs/codex-config/notes/slice-shape-policy.yaml
```

YAML is selected for human-maintained project configuration. JSON remains the
preferred canonical transport and result encoding between scripts and agents.

The initial configuration remains deliberately small:

```yaml
schema: slice-shape-policy/v1
default_shape: vertical
allow_override: true
require_override_reason: true
```

Do not place this payload inside Markdown and do not implement Markdown code-block
extraction.

## Exact Discovery And Resolution Contract

`docs/plans/programs/codex-config/CURRENT.md` must contain exactly one
project-policy reference using this field:

```text
- Slice-shape policy path: notes/slice-shape-policy.yaml
```

`plan-batch` owns resolution of this reference for the active program:

1. read exactly one non-empty repo-relative value from the declared field;
2. resolve it relative to the active program root;
3. reject an absolute path, `..` escape, symlink escape, missing file,
   non-regular file, duplicate declaration, unreadable UTF-8, invalid YAML, or
   schema-invalid payload;
4. parse with a safe YAML loader into one mapping;
5. require exactly `schema`, `default_shape`, `allow_override`, and
   `require_override_reason`;
6. validate the parsed mapping against
   `schemas/slice-shape-policy-v1.schema.json`;
7. provide no implicit or hard-coded fallback when resolution fails.

The reusable skill must not hard-code the codex-config path. Planning State may
report the declared reference and validation status, but it does not become a
generic configuration framework or shape-decision owner.

## Policy Identity And Agent Transport

The human-authored source remains YAML. The resolved policy supplied to agents
and deterministic validation is the parsed mapping encoded as canonical JSON:

- UTF-8;
- mapping keys sorted;
- no insignificant whitespace;
- SHA-256 over those canonical JSON bytes.

The evidence packet and deterministic request must bind:

- the repo-relative policy path;
- SHA-256 of the exact YAML source bytes;
- SHA-256 of the canonical parsed payload;
- the complete parsed policy object.

`batch_planner`, `batch_plan_reviewer`, deterministic queue validation, and
artifact validation must receive the same path, digests, and payload. Any
missing or mismatched identity blocks before queue mutation.

This is a private planning mechanism, not a new public configuration API.

## Required Configuration Behavior

The corrected plan must prove all supported values rather than only the initial
codex-config instance.

### Default vertical

```yaml
default_shape: vertical
allow_override: true
require_override_reason: true
```

A selected vertical slice is accepted with:

```yaml
shape:
  selected: vertical
  override_reason: null
```

### Default horizontal

```yaml
default_shape: horizontal
allow_override: true
require_override_reason: true
```

A selected horizontal slice is accepted with:

```yaml
shape:
  selected: horizontal
  override_reason: null
```

Following the configured default is not an override.

### Required override reason

With a vertical default and `require_override_reason: true`, selecting
`horizontal` requires a non-empty reason. Missing, null, blank, or whitespace-only
reasons are rejected.

### Optional override reason

With a vertical default and `require_override_reason: false`, selecting
`horizontal` is accepted with a null reason when overrides are allowed.

### Disabled overrides

When `allow_override: false`, any selected shape different from
`default_shape` is rejected regardless of whether a reason is present.

The deterministic boundary checks these mechanical conditions only. Independent
planning review decides whether a supplied reason is architecturally persuasive.

## Required Resolution Failure Tests

Focused acceptance must also prove that planning blocks before planner
invocation or queue mutation for:

- missing policy reference;
- duplicate policy reference;
- absolute or escaping policy path;
- missing or non-regular policy file;
- invalid UTF-8 or YAML;
- non-mapping YAML;
- unknown, missing, or mistyped fields;
- unsupported `schema` or `default_shape`;
- policy source hash, canonical payload hash, or payload mismatch between owners.

No fallback may silently recreate the vertical default.

## Migration Evidence Clarification

`migration_evidence` preserves the migration safeguards introduced by CCFG-26A.
It does not define the final general semantics of vertical or horizontal slices.

The retained fields and coexistence-consistent `migration_matrix` remain required
only for `risk: migration`, independently of selected shape. Their preservation
must not be interpreted as deciding which fields a future general vertical-slice
contract should require.

That broader design remains deferred until after the command-owner refactor and
additional dogfooding.

## Path And Scope Corrections

Every occurrence of the planned project policy path in live execution scope must
use:

```text
docs/plans/programs/codex-config/notes/slice-shape-policy.yaml
```

The `.md` path in the original immutable plan-time snapshot is superseded for
execution by this amendment. Do not create both files.

The existing candidate write-path ceiling remains unchanged except for the
configuration source format. No additional owner, framework, policy hierarchy,
profile catalog, compatibility reader, or artifact identity is authorized.

## Amended Acceptance Criteria

The original acceptance criteria remain in force with these additions and
clarifications:

1. YAML configuration is resolved through the exact active-program reference
   contract above, with no fallback.
2. Both vertical and horizontal configured defaults are supported and tested.
3. `require_override_reason: false` is supported and tested.
4. Resolution and identity failures block before planner invocation and queue
   mutation.
5. `migration_evidence` is documented and tested as retained migration
   protection, not the final general slice-shape model.
6. The current schema is replaced directly; historical runways are neither
   migrated nor accepted through compatibility machinery.

## Execution And Review Boundary

Before the first implementation handoff, `work-batch` must:

- read this amendment together with `dispatch.md`, `runway.md`, and `review.md`;
- obtain a fresh strict lease whose canonical planning scope names the `.yaml`
  path;
- stop if any handoff still authorizes or creates
  `notes/slice-shape-policy.md`;
- keep the existing one-slice boundary unless the measured diff becomes clearly
  oversized and a smaller reviewed alternative is produced.

A fresh independent planning review must bind the original dispatch, original
runway, this amendment, and the unchanged source direction before implementation
starts.
