---
name: fixture-route-inspector
description: Fixture-local mechanical inspection support.
---

# Fixture Route Inspector

Return mechanical request facts to the fixture command without selecting a
route.

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: fixture-route-inspector
  audience: support-mechanism
producer:
  toolchain_generation: candidate
  toolchain_commit: 23db635dba08d7d1641fccfa0652ff5d3df0d2f6
  schema_version: skill-contract/v1
purpose: >-
  Inspect explicit fixture request facts without owning route selection.
owns:
  decisions: []
  durable_facts: []
reads:
  required:
    - explicit_request
  conditional: []
writes: []
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids:
  - bounded_route_selection
  - planning_state_mutation
outputs:
  one_of:
    - route_inspection
stops_when:
  - missing_explicit_request
references: []
```

## Procedure

1. Inspect only whether the explicit request is present, whether the alternate
   was requested, and whether a blocking constraint is present.
2. Return those facts as `route_inspection`.

Do not select a route or mutate state.
