# Planning Artifact Authoring

Load this reference only through the core contract's
`create_or_modify_supported_planning_artifact` trigger. It deepens authoring for
the accepted planning artifacts below. It does not redefine the core contract,
ownership, canonicality, migration rules, reference semantics, or stopping
rules.

## Supported Schemas

This is the one deterministic support list:

```yaml
supported_schemas:
  - planning-current/v1
  - planning-finding/v1
  - planning-dispatch/v1
  - planning-runway/v1
  - planning-closeout/v1
  - planning-selection-transaction/v1
```

Schema identity is the complete `schema` value, including its version. Support
does not extend to an unlisted name, another version of a listed name, or an
artifact with no schema identity.

## Loading And Blocking Decision

| Task and schema identity | Decision |
|---|---|
| Create or modify an artifact with one exact supported schema | Load this reference, then continue authoring. |
| Ordinary hybrid-skill authoring | Do not load this reference. |
| Create or modify an artifact with missing schema identity | Block before authoring or mutation. |
| Create or modify an artifact with an unknown schema name | Block before authoring or mutation. |
| Create or modify an artifact with an unsupported schema version | Block before authoring or mutation. |

Never guess a schema identity, coerce an unknown name into a listed family, or
upgrade or downgrade a version. A blocked result names the received identity,
the reason, and the exact support list; it does not author the artifact or
mutate planning state.

## Authoring Procedure

1. Resolve the project's planning root, artifact placement, and update
   authority from its declared Planning Artifact Layout v1 instructions. Stop
   when a required project value is missing; do not supply a project-specific
   default.
2. Read the artifact's explicit `schema` identity before drafting content or
   authorizing any mutation. Apply the loading and blocking decision above.
3. Consume the existing schema and planning validator/store owner for that exact
   identity. Do not copy required fields, atomic-write rules, lifecycle rules,
   or parser behavior into this reference.
4. Follow Planning Artifact Layout v1 for placement and active-artifact shape.
   Keep each machine-relevant fact under its schema-defined structured owner;
   prose may explain but may not redefine it.
5. Validate the explicit artifact through the existing planning contract owner.
   Return the authored result and validation evidence to the caller that owns
   any write or workflow transition.

## Ownership Boundary

This reference consumes Planning Artifact Layout v1 and the six accepted schema
contracts. It owns no planning root, schema, workflow decision, lifecycle fact,
state transition, or mutation. It introduces no second skill contract block,
contract version, support dialect, or reference-loading trigger.

The calling workflow retains placement decisions, write authority, validation
commands, state transitions, and rollback. Project instructions or an active
specification supply concrete paths and commands; this reusable reference does
not embed them.
