# Command Owner

## Contract

```yaml
schema: skill-contract/v1
identity:
  name: command-owner
  audience: human-command-owner
producer:
  toolchain_generation: candidate
  toolchain_commit: "4444444444444444444444444444444444444444"
  schema_version: skill-contract/v1
purpose: Own the migrated workflow decision through a narrower interface.
owns:
  decisions:
    - selection_decision
  durable_facts: []
reads:
  required:
    - explicit_request
  conditional: []
writes:
  - selected_result
requires:
  mechanisms:
    - support-mechanism
  evidence_skills: []
delegates: []
forbids:
  - implicit_selection
outputs:
  one_of:
    - selected_result
stops_when:
  - request_is_ambiguous
references: []
```
