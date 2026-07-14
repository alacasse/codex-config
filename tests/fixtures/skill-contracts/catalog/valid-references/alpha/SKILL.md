# Reference Alpha

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: reference-alpha
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: "4444444444444444444444444444444444444444"
  schema_version: skill-contract/v1
purpose: Validate explicit dependencies and structured references.
owns:
  decisions:
    - alpha_decision
  durable_facts: []
reads:
  required: []
  conditional: []
writes: []
requires:
  mechanisms:
    - reference-beta
  evidence_skills: []
delegates:
  - responsibility: beta_operation
    target: reference-beta
forbids: []
outputs:
  one_of: []
stops_when: []
references:
  - path: references/details.md
    load_when:
      - ../beta/SKILL.md
```
