---
name: example
description: Fixture for the accepted skill contract schema.
---

# Example

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: example
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: skill-contract/v1
purpose: >-
  Validate the closed-world skill contract fixture.
owns:
  decisions:
    - example_decision
  durable_facts: []
reads:
  required:
    - explicit_input
  conditional: []
writes:
  - explicit_output
requires:
  mechanisms: []
  evidence_skills: []
delegates:
  - responsibility: path_resolution
    target: planning-artifacts
forbids:
  - implicit_input_discovery
outputs:
  one_of:
    - validated_result
stops_when:
  - invalid_contract
references:
  - path: references/details.md
    load_when:
      - detailed_validation
```

## Procedure

1. Validate explicit inputs.
