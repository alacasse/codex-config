# Legacy Owner

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: legacy-owner
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: "4444444444444444444444444444444444444444"
  schema_version: skill-contract/v1
purpose: Own the pre-migration workflow decision.
owns:
  decisions:
    - selection_decision
  durable_facts: []
reads:
  required: []
  conditional: []
writes:
  - legacy_selection
requires:
  mechanisms: []
  evidence_skills: []
delegates: []
forbids: []
outputs:
  one_of:
    - legacy_result
stops_when: []
references: []
```
