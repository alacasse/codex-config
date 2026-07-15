# Planning Ledger

## Store Metadata

```yaml
interface: ledger-store/v1
store_revision: 2
replay_records: []
```

## Derived Index

```yaml
interface: planning-derived-index/v1
source_artifact: one-finding-change.md
source_revision: 2
findings:
- id: CCFG-1
  revision: 2
  title: First finding
  status: closed
- id: CCFG-2
  revision: 1
  title: Second finding
  status: open
```

## Finding CCFG-1

```yaml
schema: planning-finding/v1
id: CCFG-1
revision: 2
title: First finding
provenance:
  source_id: SRC-1
  source_commit: "1111111111111111111111111111111111111111"
  source_section: source.md#one
lifecycle:
  status: closed
dependencies: []
scope:
  summary: First scope.
  included:
  - first
  excluded: []
evidence:
  pointers: []
next_action:
  command: plan-batch
  condition: explicit_request
producer:
  toolchain_generation: stable
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: planning-finding/v1
```

## Finding CCFG-2

```yaml
schema: planning-finding/v1
id: CCFG-2
revision: 1
title: Second finding
provenance:
  source_id: SRC-2
  source_commit: "2222222222222222222222222222222222222222"
  source_section: source.md#two
lifecycle:
  status: open
dependencies:
- CCFG-1
scope:
  summary: Second scope.
  included:
  - second
  excluded: []
evidence:
  pointers: []
next_action:
  command: plan-batch
  condition: explicit_request
producer:
  toolchain_generation: stable
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: planning-finding/v1
```
