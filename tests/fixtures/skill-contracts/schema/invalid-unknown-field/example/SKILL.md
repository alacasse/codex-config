---
name: example
description: Fixture containing an unknown v1 field.
---

# Example

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: example
  audience: human-command-owner
  display_name: Unknown v1 field
producer:
  toolchain_generation: candidate
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: skill-contract/v1
purpose: Reject this fixture.
owns:
  decisions: []
  durable_facts: []
reads:
  required: []
  conditional: []
writes: []
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids: []
outputs:
  one_of:
    - blocked_result
stops_when: []
references: []
```
