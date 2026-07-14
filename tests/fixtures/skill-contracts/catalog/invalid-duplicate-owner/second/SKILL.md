# Second Command Owner

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: second-command
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: "2222222222222222222222222222222222222222"
  schema_version: skill-contract/v1
purpose: Conflict with another command owner.
owns:
  decisions:
    - candidate_selection
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
  one_of: []
stops_when: []
references: []
```
