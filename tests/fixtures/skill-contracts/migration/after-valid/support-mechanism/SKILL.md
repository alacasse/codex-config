# Support Mechanism

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: support-mechanism
  audience: support-mechanism
producer:
  toolchain_generation: candidate
  toolchain_commit: "4444444444444444444444444444444444444444"
  schema_version: skill-contract/v1
purpose: Provide the narrow mechanism required by the command owner.
owns:
  decisions: []
  durable_facts:
    - resolved_input
reads:
  required:
    - explicit_request
  conditional: []
writes: []
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids: []
outputs:
  one_of:
    - resolved_input
stops_when: []
references: []
```
