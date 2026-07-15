# Current State With Duplicate-Key Shadow

## Operational Contract

```yaml
schema: planning-current/v1
program: codex-config
revision: 3
ledger: docs/plans/programs/codex-config/LEDGER.md
selected_dispatch: null
queued_runway: null
active_runway: null
latest_closeout: null
blockers: []
producer:
  toolchain_generation: stable
  toolchain_commit: 0123456789abcdef0123456789abcdef01234567
  schema_version: planning-current/v1
```

## Shadow State

```yaml
program: another-program
program: duplicate-program
```
