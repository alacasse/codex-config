---
name: fixture-branching-command
description: Fixture-only human command with bounded route selection.
---

# Fixture Branching Command

Choose one bounded route from an explicit request after consuming mechanical
inspection facts from the fixture-local support mechanism.

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: fixture-branching-command
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: 23db635dba08d7d1641fccfa0652ff5d3df0d2f6
  schema_version: skill-contract/v1
purpose: >-
  Own one bounded route-selection decision for an explicit fixture request.
owns:
  decisions:
    - bounded_route_selection
  durable_facts: []
reads:
  required:
    - explicit_request
  conditional:
    - alternate_route_requested
    - blocking_constraint
writes: []
requires:
  mechanisms:
    - fixture-route-inspector
  evidence_skills: []
delegates:
  - responsibility: route_inspection
    target: fixture-route-inspector
forbids:
  - planning_state_mutation
  - unbounded_work_selection
  - support_mechanism_route_selection
outputs:
  one_of:
    - normal_route_selected
    - alternate_route_selected
    - blocked_route_result
stops_when:
  - missing_explicit_request
  - blocking_constraint
references: []
```

## Normal Procedure

1. Require one explicit request and its bounded route options.
2. Delegate only `route_inspection` to `fixture-route-inspector`.
3. Apply the returned mechanical facts to the branch rules below.
4. Return one route-selection result without executing that route.

## Branches

- Normal: when the request is complete and no alternate or blocker applies,
  return `normal_route_selected`.
- Alternate: when the request explicitly selects the allowed alternate and no
  blocker applies, return `alternate_route_selected`.
- Blocked: when the request is missing or inspection reports a blocking
  constraint, return `blocked_route_result` without selecting a route.

## Stop Conditions

Stop on `missing_explicit_request` or `blocking_constraint`. The command does
not broaden the request, execute a selected route, or let the support mechanism
make `bounded_route_selection`.
