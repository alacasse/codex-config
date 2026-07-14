# Reference Cycle Second

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: reference-cycle-second
  audience: authoring-support
producer:
  toolchain_generation: candidate
  toolchain_commit: "5555555555555555555555555555555555555555"
  schema_version: skill-contract/v1
purpose: Form the other side of a structured reference cycle.
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
  one_of: []
stops_when: []
references:
  - path: ../first/SKILL.md
    load_when:
      - cycle_probe
```
