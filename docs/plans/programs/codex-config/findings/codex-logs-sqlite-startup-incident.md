# Codex `logs_2.sqlite` Growth and VS Code Startup Incident

Investigation date: 2026-07-09

## Executive Finding

The preserved `logs_2.sqlite` is a Codex-owned diagnostic log database, not a
repository artifact and not a database written by `codex-config` Python code.
It reached 3,272,642,560 bytes (3.05 GiB) through two mechanisms:

1. Codex persisted exceptionally verbose runtime tracing. The surviving rows
   contain 1,238,120,454 estimated logical bytes, 83.7% of them at `TRACE`.
   Four transport/runtime targets account for about 89.7% of those bytes.
2. Codex continuously pruned retained rows but did not reclaim the database's
   high-water allocation. The WAL-consistent snapshot has 375,526 free pages,
   or 1,538,154,496 bytes (1.43 GiB, 47.0% of all pages), inside the main file.

The surviving ID range contains 668,157 rows but spans 103,769,525 IDs. About
103.1 million IDs (99.36% of the range) are absent, consistent with extreme
insert/delete churn from retention and per-partition pruning. The database is
healthy (`PRAGMA integrity_check` returned `ok`); the preserved WAL is only
1.72 MiB, and both schema migrations had completed when the database was first
created. Corruption, a large surviving WAL, and an in-progress migration are
therefore not supported as the incident's primary cause.

The extension starts a bundled `codex app-server` and waits for its
`initialize` response. Codex synchronously opens and migrates `logs_2.sqlite`,
deletes logs older than ten days, and issues a passive WAL checkpoint before
state-runtime initialization returns. Local extension logs show a 1.190-second
four-row log insert and one app-server launch that produced no initialize
response before another launch 4.718 seconds later. Moving only the log
database aside was followed by an 8-millisecond initialize response. This is
strong evidence that pathological log-database I/O or lock contention was in
the startup critical path, although the available logs do not identify the
exact SQLite statement that blocked the failed launch.

`codex-config` activity contributed to retained volume but is not the primary
root cause. Matching surviving thread IDs to immutable Codex state metadata
attributes about 300.8 MB (24.3%) of retained estimated bytes to threads whose
working directory was this repository: 169.9 MB from subagents and 130.8 MB
from VS Code user threads. The known architecture program runner execution was
on June 26, four days before the oldest surviving log row, so the backup cannot
directly attribute retained rows to that run. Its design can amplify Codex use
through one fresh `codex exec` per attempted phase, unbounded manual resumes,
and execute-phase subagents, but it does not write `logs_2.sqlite` or persist
successful raw subprocess output in repository artifacts.

**Root-cause assessment:** an upstream Codex diagnostic-logging and retention
failure is the primary cause. Heavy multi-agent work, including work in
`codex-config`, increased event volume. The architecture runner is a plausible
historical workload amplifier, but available evidence does not show it caused
most of this database's high-water growth.

## Incident Scope

- Product: OpenAI Codex VS Code extension.
- Extension: `openai.chatgpt` version `26.707.31428`.
- Bundled runtime: `codex-cli 0.144.0-alpha.4`.
- Platform: native Linux x86_64.
- Preserved database: `/home/alacasse/.codex/backup/logs_2.sqlite`.
- Recreated active database: `/home/alacasse/.codex/logs_2.sqlite`.
- Repository under investigation: `/home/alacasse/projects/codex-config`.
- Installed app-server command:

  ```text
  codex -c features.code_mode_host=true app-server --analytics-default-enabled
  ```

This investigation did not inspect authentication data. Sensitive runtime
values were processed locally only where needed for bounded classification,
hashing, joins, and aggregate counts. No raw log bodies, prompts,
conversations, tool output, thread IDs, process UUIDs, or unrelated sensitive
source content are included in this report.

## Confirmed Findings

### Database identity and file metadata

File metadata was captured at 2026-07-09 21:37 EDT. Allocated sizes are
filesystem block counts multiplied by 512 bytes.

| File | Logical size | Allocated size | Birth time (EDT) | Modified time (EDT) | Change time at initial snapshot (EDT) |
| --- | ---: | ---: | --- | --- | --- |
| Backup main | 3,272,642,560 B | 3,272,638,464 B | 2026-04-09 11:37:47 | 2026-07-09 19:16:33 | 2026-07-09 19:23:59.541 |
| Backup WAL | 1,804,592 B | 1,806,336 B | 2026-07-09 15:50:24 | 2026-07-09 19:23:33 | 2026-07-09 19:23:59.543 |
| Backup SHM | 32,768 B | 32,768 B | 2026-07-09 15:50:24 | 2026-07-09 19:23:33 | 2026-07-09 19:23:59.542 |
| Active main | 11,030,528 B | 11,030,528 B | 2026-07-09 19:24:32 | 2026-07-09 21:36:54 | 2026-07-09 21:36:54 |
| Active WAL | 4,869,872 B | 4,870,144 B | 2026-07-09 21:26:32 | 2026-07-09 21:37:54 | 2026-07-09 21:37:54 |
| Active SHM | 32,768 B | 32,768 B | 2026-07-09 21:26:32 | 2026-07-09 21:37:54 | 2026-07-09 21:37:54 |

The backup main file's change time is 2026-07-09 19:23:59 EDT, which is the
move into `backup/`. Its content modification time remained 19:16:33. The WAL
and main-file modification/change timestamps did not change during inspection.

Forensic caveat: the first WAL-aware Python `sqlite3` connection used
`mode=ro` and `PRAGMA query_only=ON`. SQLite still updated the existing backup
SHM file's read-mark state, changing that file's modification and change time
to 2026-07-09 21:43:04 EDT. It did not change the backup main database or WAL.
All later backup queries used `immutable=1`, which does not touch the SQLite
sidecars. This is a limitation of the initial inspection procedure and should
be disclosed with any evidence derived from the backup.

### SQLite properties

The WAL-consistent backup snapshot reported:

| Property | Value |
| --- | ---: |
| Page size | 4,096 B |
| Page count | 798,985 |
| Freelist count | 375,526 |
| Freelist bytes | 1,538,154,496 B |
| Journal mode | `wal` |
| Auto-vacuum | `2` (`INCREMENTAL`) |
| User version | 0 |
| Application ID | 0 |
| Schema version | 14 |
| Integrity status | `ok` |

The main-image-only freelist count observed with immutable access was 375,572;
the 46-page difference is accounted for by the preserved WAL snapshot. Both
measurements put free internal space at 47.0% of the main file.

The backup sidecars were small at preservation time. WAL accumulation was not
a material part of the preserved 3.05 GiB footprint.

### Schema

The database contains three tables, four explicit indexes, and one SQLite
automatic index. It has no views, triggers, or foreign keys.

Tables:

- `_sqlx_migrations(version, description, installed_on, success, checksum,
  execution_time)`
- `logs(id, ts, ts_nanos, level, target, feedback_log_body, module_path,
  file, line, thread_id, process_uuid, estimated_bytes)`
- `sqlite_sequence(name, seq)`

Indexes:

- `idx_logs_ts` on descending timestamp and ID.
- `idx_logs_thread_id` on thread ID.
- `idx_logs_thread_id_ts` on thread ID and descending timestamp/ID.
- `idx_logs_process_uuid_threadless_ts`, a partial index for threadless rows.
- `sqlite_autoindex__sqlx_migrations_1` for the migration primary key.

Migrations 1 (`logs`) and 2 (`logs feedback log body`) both completed
successfully at 2026-04-09 15:37:47 UTC. Migration 2 rewrites the old logs table
and rebuilds indexes, but it was not pending during this incident.

### Storage distribution

`dbstat` against the WAL-consistent snapshot reported:

| Object | Allocated bytes | Pages | Payload bytes | Unused bytes |
| --- | ---: | ---: | ---: | ---: |
| `logs` | 1,599,766,528 | 390,568 | 1,310,114,761 | 279,139,927 |
| `idx_logs_thread_id_ts` | 68,272,128 | 16,668 | 37,959,391 | 28,108,254 |
| `idx_logs_thread_id` | 34,959,360 | 8,535 | 27,942,711 | 4,909,762 |
| `idx_logs_ts` | 24,719,360 | 6,035 | 14,025,622 | 8,616,851 |
| Threadless-process index | 2,756,608 | 673 | 1,522,032 | 1,160,834 |
| Schema/migration bookkeeping | 16,384 | 4 | 1,484 | 14,715 |

The live B-trees occupy about 1.61 GiB. The four explicit indexes occupy about
124.7 MiB. Free internal pages occupy about 1.43 GiB. Remaining pages are
consistent with pointer-map and SQLite structural overhead.

The 3.05 GiB therefore represents a combination of:

- about 1.15 GiB of Codex-estimated retained content;
- SQLite record and B-tree overhead;
- about 124.7 MiB of indexes;
- about 266 MiB of unused space within currently allocated `logs` pages;
- about 1.43 GiB of wholly free pages on the freelist;
- a negligible preserved WAL relative to the main file.

It is not primarily corruption or a large WAL.

### Rows and logical content

| Measure | Value |
| --- | ---: |
| Retained log rows | 668,157 |
| Oldest retained timestamp | 2026-06-30 00:14:29 UTC |
| Newest retained timestamp | 2026-07-09 23:23:33 UTC |
| Minimum ID | 132,407,214 |
| Maximum ID | 236,176,738 |
| Distinct process UUIDs | 32 |
| Distinct thread IDs | 2,421 |
| Threadless rows | 21,890 |
| Sum of `estimated_bytes` | 1,238,120,454 B |
| Sum of SQLite text lengths | 1,199,666,395 characters |
| Average estimated bytes per row | 1,853 B |
| Average SQLite text length per row | 1,796 characters |

The ID range spans 103,769,525 possible IDs. Only 0.64% remain. An ID gap alone
does not prove a committed row was later deleted: failed or rolled-back inserts
and allocation behavior can also consume IDs. Combined with Codex's documented
delete paths, the 47% freelist, and exact partition caps, the gap is strong
circumstantial evidence of very high insert/delete churn.

### Log levels

| Level | Rows | Estimated bytes | Share of rows | Share of bytes |
| --- | ---: | ---: | ---: | ---: |
| TRACE | 529,575 | 1,035,910,157 | 79.3% | 83.7% |
| DEBUG | 73,838 | 121,745,304 | 11.1% | 9.8% |
| INFO | 57,533 | 73,798,385 | 8.6% | 6.0% |
| WARN | 7,174 | 6,600,654 | 1.1% | 0.5% |
| ERROR | 37 | 65,954 | less than 0.1% | less than 0.1% |

### Largest targets

| Target | Rows | Estimated bytes | Average bytes/row | Maximum bytes/row |
| --- | ---: | ---: | ---: | ---: |
| `codex_api::endpoint::responses_websocket` | 1,913 | 520,160,991 | 271,909 | 1,022,758 |
| `log` | 264,707 | 258,679,177 | 977 | 48,737 |
| `codex_api::sse::responses` | 197,259 | 203,630,910 | 1,032 | 1,096 |
| `codex_core::stream_events_utils` | 84,117 | 128,256,212 | 1,525 | 60,870 |
| `codex_mcp::connection_manager` | 50,089 | 40,594,505 | 810 | not material |
| `feedback_tags` | 22,151 | 33,269,007 | 1,502 | not material |

The first four targets account for approximately 1.111 GB, or 89.7% of all
estimated retained bytes. The 1,913 WebSocket rows alone account for 42.0%.
This is raw runtime transport/stream tracing, not compact command metadata.

Structural names and bounded aggregate content fingerprints strongly indicate
that bodies can contain request/response stream payloads and copied context.
They are not limited to a one-line diagnostic message. No full payload was
emitted during the investigation.

### Growth over the surviving retention window

| UTC day | Rows retained | Estimated bytes | Distinct processes | Distinct threads |
| --- | ---: | ---: | ---: | ---: |
| Jun 30 | 120,437 | 638,237,027 | 10 | 372 |
| Jul 1 | 68,552 | 79,519,541 | 2 | 225 |
| Jul 2 | 135,686 | 149,142,998 | 3 | 489 |
| Jul 3 | 27,869 | 28,717,479 | 5 | 87 |
| Jul 4 | 77,997 | 87,248,746 | 2 | 293 |
| Jul 5 | 97,080 | 106,272,905 | 4 | 384 |
| Jul 6 | 38,156 | 39,775,156 | 5 | 157 |
| Jul 7 | 12,832 | 14,379,534 | 1 | 64 |
| Jul 8 | 11,926 | 12,230,826 | 3 | 38 |
| Jul 9 | 77,622 | 82,596,242 | 10 | 354 |

June 30 holds 51.5% of surviving logical bytes. This is not necessarily the
date of the database's physical high-water mark: rows before June 30 had
already been removed, and free pages preserve only their allocation, not their
producer metadata.

### Retention and pruning behavior

Installed binary strings and current first-party source agree on these rules:

- logs older than ten days are deleted during startup;
- thread-associated logs are capped at 10 MiB and 1,000 rows per thread;
- threadless logs are capped separately per process UUID;
- each insert transaction checks affected partitions and deletes old rows with
  window-function queries when a cap is exceeded;
- startup then runs `PRAGMA wal_checkpoint(PASSIVE)`;
- the database is configured for incremental auto-vacuum;
- startup does not run `PRAGMA incremental_vacuum`.

The local data independently confirms the caps: no thread exceeds 1,000 rows or
10 MiB; 274 retained threads sit exactly at the 1,000-row cap, and the largest
thread has 10,484,900 estimated bytes. The median retained thread has 44 rows
and 34,499 estimated bytes; p95 is 1.88 MB and p99 is 7.03 MB.

Retention bounds logical content per partition but not the total number of
threads, physical file high-water mark, or amount of free space retained in
the file. It also causes continuing write amplification through insert,
multi-index update, windowed delete, WAL write, and checkpoint operations.

## What the Database Stores

Confirmed from schema, target names, source code, and aggregates:

- Codex CLI and app-server diagnostic logs;
- VS Code app-server runtime logs;
- WebSocket response payload tracing;
- SSE response-event tracing;
- stream-event processing logs;
- MCP connection/service logs;
- session/turn handler events;
- plugin/model-cache warnings and diagnostics;
- thread and process attribution metadata;
- feedback-export bodies.

The database can therefore contain bounded portions of prompts, responses,
tool-call traffic, streamed rollout events, errors, and other context carried
inside transport logs. It is not a canonical conversation database; canonical
rollout/session state is stored elsewhere. It does not have dedicated command
stdout or stderr columns, although subprocess/tool output may appear when it is
embedded in traced runtime payloads.

The generic `log` target and transport targets demonstrate that this is not a
VS Code-extension-only store. All Codex processes using the same `CODEX_HOME`
can write to it, including app-server, interactive CLI, `codex exec`, and
subagent activity.

## Producer Attribution

### Process shape

The largest retained process partitions are long-lived and contain many
threads. The largest has 208,118 retained rows, 227.9 MB, 725 distinct threads,
and spans about 57 hours. Other major partitions span hours or days and contain
110 to 340 threads. This shape is strongly consistent with persistent
app-server/interactive coordinator processes, not a single short `codex exec`
phase.

Every major process contains Codex app-server targets. The four largest also
contain most of the giant WebSocket payload rows. Process identifiers were
hashed during analysis and are intentionally omitted here.

### Thread-source attribution

Thread IDs in the backup were joined in memory to immutable
`state_5.sqlite` metadata. Only source category and whether the working
directory equaled this repository were retained in output.

| Origin | Working directory class | Threads | Rows | Estimated bytes |
| --- | --- | ---: | ---: | ---: |
| Subagent | Other repositories | 369 | 253,520 | 552,794,245 |
| VS Code user thread | Other repositories | 115 | 108,094 | 310,869,348 |
| Subagent | `codex-config` | 340 | 146,214 | 169,930,096 |
| VS Code user thread | `codex-config` | 99 | 86,609 | 130,820,521 |
| Unmatched historical thread | Unknown | 1,498 | 51,830 | 70,133,658 |

This accounts for all thread-associated estimated bytes. Threadless rows add a
small remainder.

Confirmed conclusions from this join:

- subagent activity is the largest surviving logical producer class;
- persistent VS Code/app-server activity is the next largest class;
- threads working in `codex-config` account for about 300.8 MB, 24.3% of all
  retained estimated bytes;
- no matched retained thread is classified as a standalone `exec` origin;
- surviving metadata does not assign the 1.43 GiB freelist to any producer.

Aggregate body searches found references to `codex-config`, `codex exec`, and
the architecture runner in hundreds of megabytes of rows. Those matches are
not producer attribution: large WebSocket payload logs copy conversation and
prompt context, so one reference can recur in many transport records and in
threads whose working directory is another repository.

## `codex-config` Code-Path Analysis

### Normal process count

The runner is sequential. `CodexExecWorker.run_phase()` creates one blocking
`codex exec` subprocess per attempted phase. A normal executed batch has four
runner-owned launches:

```text
select-dispatch -> create-spec -> execute -> closeout
```

Planning-only mode uses two. `N` fully executed batches normally use `4N`
launches; an additional final select can make it `4N + 1` when no safe batch
remains. Runner-owned maximum concurrency is one.

Execute-phase Batch Runway behavior can create many Codex subagent threads
inside one execute phase: at least one worker and one independent reviewer per
slice, plus optional investigators, specialists, and recovery passes. Those
are Codex-runtime threads, not additional subprocesses launched directly by
the Python runner.

### Retry and resume

The runner has no automatic retry around `subprocess.run`. A failed subprocess
stops the run. A later external `--resume` invocation reruns the persisted
active phase and creates another Codex process/session. There is no cumulative
attempt count, retry cap, phase timeout, output cap, token hard stop,
all-batches iteration ceiling, or concurrent-run lock.

The documented June 26 Graphify run used at least eight runner invocations and
at least ten phase subprocess launches: three select attempts, one create-spec,
at least five execute attempts, and one closeout. The exact count is
report-derived because canonical run manifests are no longer present.

### Prompt and output behavior

The runner's phase prompt is a compact control prompt containing paths, phase
facts, result obligations, and references to the program ledger, dispatch,
spec, receipts, manifests, and telemetry. It does not directly concatenate all
planning artifacts into the command. The phase agent may still read broad
artifacts, and the archived telemetry identifies execute as the context hot
path.

`subprocess.run` captures complete stdout and stderr in memory. On success, the
runner persists only byte counts, exit status, optional session attribution,
and compact telemetry. It does not write raw successful streams into its
repository artifacts. On failure, full stderr is copied into the exception,
state stop reason, phase telemetry, terminal error, and final summary. This is
a real runner-side duplication path but is separate from Codex's independent
SQLite tracing.

The same final result also exists in a temporary `--output-last-message` file,
a durable receipt, and compact state/manifest fields. This duplicates small
result metadata, not the multi-gigabyte SQLite contents.

### Recursive content and nested execution

Phase prompts explicitly prohibit nested `codex exec` and recursive runner
launches. The prohibition is instructional only. The Python code does not set
a nesting marker, inspect descendants, intercept `codex` resolution, or enforce
a process-tree limit. Archived evidence confirms one closeout phase attempted
forbidden nested Codex work. Nested activity is therefore possible, but the
surviving database does not prove it was a major producer.

The runner's later phase prompts refer to compact prior artifacts; it does not
automatically feed raw subprocess output or `logs_2.sqlite` records into later
prompts. Agents can nevertheless reread broad plans or copied context.

### Hooks

The configured global Stop hook can run one notification script per completed
Codex execution. That script performs bounded Git probes and notification work.
It does not write `logs_2.sqlite` directly. If Stop hooks run for each
`codex exec`, they add process/event volume, but no `SubagentStop` hook is
configured in the checked-in hook file.

### Attribution conclusion

The runner is a workload multiplier, not the logging implementation. It causes
Codex processes and subagent work, and its unbounded manual resume semantics can
multiply attempts. However:

- its known June 26 run predates the backup's oldest surviving row;
- the live attribution window is dominated by persistent VS Code threads and
  subagents;
- it does not use Python `sqlite3` against Codex state;
- successful raw subprocess output is not persisted by the runner;
- the physical freelist retains no source attribution.

`codex-config` contributed meaningful workload volume, but the abnormal growth
mechanism belongs primarily to Codex's persistent TRACE logging and incomplete
space reclamation.

## Incident Timeline

All extension times below are local EDT. Database row times are UTC.

| Time | Event | Evidence and confidence |
| --- | --- | --- |
| Apr 9 11:37 | Original log database created; migrations 1 and 2 complete. | File birth time and migration table; high confidence. |
| Jun 26 18:55-21:10 | Known architecture runner logical run repeatedly resumed. | Archived reports and candidate session files; high confidence for sequence, medium for exact phase-session mapping. |
| Jun 30 00:14 UTC | Oldest surviving backup row. | Direct database query; high confidence. |
| Jun 30 | Largest surviving growth day, 638.2 MB estimated content. | Direct daily aggregate; high confidence. |
| Jul 9 15:42:57 | Extension app-server initializes in 0.862 s. | VS Code extension log; high confidence. |
| Jul 9 15:44:17 | Extension app-server initializes in 1.784 s. | VS Code extension log; high confidence. |
| Jul 9 15:44:24 | Four-row SQLite log insert takes 1.190 s. | VS Code extension warning; high confidence. |
| Jul 9 15:44:49 | App-server spawn has no recorded initialize response before another spawn 4.718 s later. | VS Code extension log; high confidence for symptom, not exact cause. |
| Jul 9 15:44:55 | Replacement app-server initializes after 1.949 s. | VS Code extension log; high confidence. |
| Jul 9 15:50:23 | App-server initializes after about 2.0 s. | VS Code extension log; high confidence. |
| Jul 9 19:16:33 | Last logged successful pre-reset app-server initialize occurs in 0.470 s; backup main mtime is 0.342 s later. This does not prove the extension UI became usable. | Extension log and file metadata; high confidence. |
| Unknown | User-reported onset and duration of persistent extension unavailability. | No surviving timestamp identifies the onset; unresolved. |
| Jul 9 19:23:54 | App-server receives SIGTERM during recovery. | Extension log; high confidence. |
| Jul 9 19:23:59 | Old main/WAL/SHM moved into backup. | File change times and recovery action; high confidence. |
| Jul 9 19:24:32 | Fresh active database created. | Active file birth time; high confidence. |
| Jul 9 19:24:33 | Replacement app-server receives initialize response in 8 ms. | Extension log; high confidence. |
| Jul 9 21:43 | Fresh database has 5,721 rows, 7.31 MB estimated content, and about 12.5 MB main-file pages after roughly 2h18m of mixed extension/forensic-session use. | Read-only snapshot; high confidence, not a controlled benchmark. |

The exact historic file-size curve is unavailable. The high ID sequence and
freelist prove extensive prior churn, but deleted pages cannot reveal when or
which workload produced their former rows.

## Startup-Failure Mechanism

### Confirmed startup path

The extension activates on `onStartupFinished`, spawns the bundled app-server,
sends JSON-RPC `initialize`, and does not consider the connection initialized
until response ID 1 arrives.

Codex state-runtime initialization performs these operations before returning:

1. Open/migrate `state_5.sqlite`.
2. Open/migrate `logs_2.sqlite`.
3. Open/migrate goals and memories databases.
4. Run state post-initialization queries.
5. Delete log rows older than ten days.
6. Run `PRAGMA wal_checkpoint(PASSIVE)`.

SQLite connections use WAL, normal synchronous mode, a five-second busy
timeout, incremental auto-vacuum, and a pool of up to five connections.

### Supported failure mechanisms

- The startup retention delete is indexed by timestamp, but deleting many rows
  still updates the main table and four indexes and writes pages to WAL.
- The passive checkpoint copies checkpointable WAL frames into the main
  database before initialization returns. Only 1.72 MiB of WAL survived
  preservation, so the checkpoint cost and WAL size at the failed launch are
  unknown.
- Concurrent Codex processes can contend for SQLite writer access and consume
  the five-second busy timeout or pool capacity.
- Normal inserts can trigger partition aggregate checks and window-function
  deletes. One local four-row insert already exceeded one second.
- Nearly half the main file is free but unreclaimed. Incremental auto-vacuum is
  configured, but no incremental vacuum occurs on startup, so retention cannot
  shrink the high-water file.
- Body-substring searches use a full table scan, though no evidence shows such
  a search was part of this startup.

### Mechanisms ruled out or not established

- **Corruption:** ruled out by full WAL-aware `integrity_check: ok`.
- **Pending schema migration:** ruled out; both migrations completed April 9.
- **Large preserved WAL:** ruled out; the WAL was 1.72 MiB.
- **Index rebuild during the observed startup:** not supported.
- **Memory exhaustion or disk saturation:** not measured.
- **Specific lock holder at the failed startup:** not recoverable.
- **Exact failing SQLite statement:** not logged.
- **A consistent startup timeout:** not established; the same large database
  sometimes initialized in under two seconds, including 0.470 s at 19:16.

The evidence supports intermittent pathological I/O/lock behavior rather than
the simplistic claim that reading any 3.05 GiB SQLite file always prevents
startup. The causal recovery experiment still strongly implicates this
database path: moving only the log DB aside produced immediate recovery while
state, goals, memories, sessions, and configuration were left intact.

## Backup Versus Recreated Database

At the 21:43 snapshot:

| Property | Backup | Active replacement |
| --- | ---: | ---: |
| Schema and migrations | Current, versions 1-2 | Identical |
| Main-file pages | 798,985 | 3,052 |
| Freelist pages | 375,526 | 291 |
| Rows | 668,157 | 5,721 |
| Estimated bytes | 1,238,120,454 | 7,312,310 |
| SQLite body text length (characters) | 1,199,666,395 | 6,733,174 |
| Retained time span | About 10 days | About 2h18m |

The schema hashes and migration records match. The active database grew at
about 3.2 MB of estimated content per hour during mixed extension and current
investigation activity, but this is not a controlled rate and should not be
projected. No controlled `codex exec` was launched because doing so would have
modified active files under `.codex`, contrary to the investigation's safety
constraint.

Consequently, exact bytes per interactive session, standalone `codex exec`,
runner phase, and runner batch cannot be measured safely from this incident.
Per-thread retained estimated bytes have a median of 34.5 KB, p95 of 1.88 MB,
p99 of 7.03 MB, and a cap near 10 MiB, but those threads mix user sessions,
subagents, and differently sized workloads.

The 3.05 GiB size is abnormal for diagnostic state. It is not simply expected
ten-day retention: retained content is about 1.15 GiB while another 1.43 GiB is
free internal space. Both high-volume TRACE payload persistence and failure to
reclaim pruned pages are required to explain the physical size.

## Strong Inferences

- **High confidence:** production-level Codex runtime tracing, especially raw
  WebSocket/SSE and stream events, caused most logical log volume.
- **High confidence:** retention and per-partition cap deletes caused massive
  churn and the 1.43 GiB freelist, while missing incremental vacuum/rotation
  left the file at its high-water mark.
- **High confidence:** subagent-heavy and long-lived app-server usage amplified
  volume; persistent processes, not only short `codex exec` invocations,
  dominate surviving rows.
- **High confidence:** work performed in `codex-config` contributed material
  retained volume (about 24.3%) but did not own the logging implementation.
- **Medium-high confidence:** the large/churned log DB caused intermittent
  startup-critical SQLite I/O or contention. The reset/recovery correlation,
  slow insert, and stalled handshake support this; the exact statement is
  unknown.
- **Medium confidence:** the architecture runner likely increased historical
  logging through repeated phase attempts and subagents, but it was not the
  main cause of the 3.05 GiB physical file.

## Unresolved Questions

- Which exact SQLite operation blocked the user-visible failed startup: open,
  pool acquisition, retention delete, checkpoint, or another log query?
- Was another Codex process holding a conflicting read/write lock at that
  moment?
- What rows occupied the 1.43 GiB now on the freelist, and which producer made
  them? SQLite deletion removed that attribution.
- How large was the database and WAL at earlier dates? No historical size
  samples remain.
- How much did the June 26 architecture runner run contribute before its rows
  aged out of the ten-day retention window?
- Why does the same 3.05 GiB DB initialize quickly in some recorded launches
  and stall in another?
- When did the user-visible persistent startup failure begin, and did the
  app-server's successful 19:16 initialize correspond to a usable extension
  UI?
- Does the installed persistent logger honor any supported verbosity setting?
  The local database and multiple upstream reports show TRACE persistence, but
  no controlled setting experiment was performed here.
- What are reliable bytes-per-phase and bytes-per-batch rates? Existing session
  attribution is incomplete and a controlled run was disallowed by the safety
  constraints.

## Root-Cause Assessment

| Conclusion | Assessment | Confidence |
| --- | --- | --- |
| Primary cause | Codex persisted high-volume TRACE transport/runtime payloads into a shared SQLite diagnostic store and pruned without reclaiming the physical high-water allocation. | High |
| Growth mechanism | WebSocket/SSE/stream tracing plus subagent-heavy use produced large rows and high event rates; only 0.64% of IDs in the surviving interval remain, while pruning and retention produced a 47% freelist. | High |
| Startup mechanism | Synchronous log DB open/migration/retention/checkpoint work, likely amplified by write contention or slow pruning, delayed app-server initialize and made extension startup unreliable. | Medium-high |
| Corruption contribution | None found. | High |
| WAL contribution at preservation | Small; not a major physical-size contributor. Earlier WAL history is unknown. | High for preserved state |
| `codex-config` contribution | Material workload contributor: about 24.3% of retained logical bytes are directly attributed to its VS Code/subagent threads. | High |
| Architecture runner contribution | Plausible amplifier through fresh phases, resumes, and subagents, but not directly measurable in surviving rows and not established as primary. | Medium |
| Primary ownership | Upstream Codex runtime retention/logging behavior, not repository artifact generation. | High |

## Recommendations

No fixes were implemented during this investigation.

### Immediate containment

1. Monitor main, WAL, allocated blocks, page count, freelist count, row count,
   and estimated bytes without opening the live database in a way that mutates
   SHM. Alert on both physical size and freelist ratio.
2. Treat `logs_2.sqlite` as rebuildable diagnostic state, but retain a documented
   stop-backup-reset-restart procedure that never touches auth, sessions,
   `state_5.sqlite`, goals, or memories.
3. Preserve file metadata and extension logs before reset when future incidents
   occur. Capture active process holders and SQLite lock state first.
4. Avoid sustained high-volume multi-agent batches until an upstream logging
   fix or supported verbosity control is confirmed.
5. Keep incident backups outside the active `.codex` directory after evidence
   preservation so Codex does not discover or contend with them.

### Permanent fixes in `codex-config`

1. Record exact Codex session ID, source category, runner run ID, phase,
   attempt number, process start/end, and `logs_2.sqlite` byte/page deltas for
   every runner-owned phase. Do not store log bodies.
2. Add a hard per-phase timeout, cumulative attempt budget, and explicit retry
   count. Make resume distinguish logical phase from attempt.
3. Add a runtime preflight warning based on log DB logical size, allocated size,
   WAL size, and freelist ratio. Keep it read-only and non-repairing.
4. Enforce the single-level boundary with an environment/process marker rather
   than prompt text alone.
5. Add a single-flight lock to prevent concurrent runner instances for one
   program state.
6. Stream or cap subprocess stdout/stderr rather than buffering both without
   bounds. Truncate/summarize failure stderr before duplicating it into state,
   telemetry, and terminal summaries.
7. Keep phase prompts pointer-based and measure prompt bytes. Prevent raw prior
   subprocess output or broad telemetry logs from becoming later-phase input.
8. Promote context-pressure thresholds from observational labels to explicit
   stop/review gates where justified.

These changes reduce workload amplification and improve attribution. They do
not replace the required upstream logging fix.

### Upstream Codex concerns

1. Do not persist TRACE-level transport payloads by default in production.
2. Provide a documented persistent-log verbosity control that applies to the
   SQLite sink.
3. Add global physical-size and WAL caps, not only per-thread logical caps.
4. Rotate/recreate diagnostic logs or incrementally reclaim free pages when a
   bounded threshold is exceeded.
5. Move retention deletes and checkpoints out of the initialize handshake or
   enforce a short non-fatal maintenance budget.
6. Make a slow, locked, oversized, or damaged log DB non-fatal to app startup.
7. Identify `logs_2.sqlite` explicitly in diagnostics and offer a safe reset
   action that preserves user state.
8. Avoid logging full WebSocket/SSE request/response payloads into diagnostic
   storage, or aggressively redact/sample them.

### Upstream bug-report evidence

The best existing upstream issue is
[openai/codex#27741](https://github.com/openai/codex/issues/27741), which already
describes app-server startup failure on a large `logs_2.sqlite`. A useful local
data point can include:

- Linux x86_64, extension `26.707.31428`, bundled CLI `0.144.0-alpha.4`;
- main DB 3,272,642,560 bytes; WAL 1,804,592 bytes;
- 668,157 retained rows; 1,238,120,454 estimated bytes;
- page size 4,096; page count 798,985; freelist 375,526 (47.0%);
- `integrity_check: ok`; migrations 1 and 2 complete;
- TRACE 529,575 rows and 1,035,910,157 estimated bytes;
- WebSocket response target 520,160,991 estimated bytes in only 1,913 rows;
- one four-row insert took 1.190 seconds;
- one launch had no initialize response before replacement 4.718 seconds later;
- reset to a fresh log DB was followed by an 8-ms initialize response;
- no raw prompts, bodies, IDs, unrelated source paths, or authentication data
  should be included in the proposed upstream report.

Related upstream reports include
[openai/codex#31142](https://github.com/openai/codex/issues/31142) for ongoing
TRACE/WAL churn and the related issues linked from #27741.

## Commands and Evidence Used

The following command shapes were used. Python's standard SQLite module was
necessary because the `sqlite3` CLI was not installed. Sensitive columns were
never printed.

```bash
stat --printf='...' \
  /home/alacasse/.codex/backup/logs_2.sqlite \
  /home/alacasse/.codex/backup/logs_2.sqlite-wal \
  /home/alacasse/.codex/backup/logs_2.sqlite-shm \
  /home/alacasse/.codex/logs_2.sqlite \
  /home/alacasse/.codex/logs_2.sqlite-wal \
  /home/alacasse/.codex/logs_2.sqlite-shm

python -c 'sqlite3.connect("file:.../backup/logs_2.sqlite?mode=ro", uri=True); ...'
python -c 'sqlite3.connect("file:.../backup/logs_2.sqlite?immutable=1", uri=True); ...'
```

Read-only SQL categories:

```sql
PRAGMA page_size;
PRAGMA page_count;
PRAGMA freelist_count;
PRAGMA journal_mode;
PRAGMA auto_vacuum;
PRAGMA user_version;
PRAGMA application_id;
PRAGMA integrity_check;

SELECT type, name, tbl_name, sql
FROM sqlite_schema
ORDER BY type, name;

SELECT name, SUM(pgsize), COUNT(*), SUM(payload), SUM(unused)
FROM dbstat
GROUP BY name
ORDER BY SUM(pgsize) DESC;

SELECT level, COUNT(*), SUM(estimated_bytes),
       SUM(length(COALESCE(feedback_log_body, '')))
FROM logs
GROUP BY level;

SELECT target, COUNT(*), SUM(estimated_bytes),
       AVG(estimated_bytes), MAX(estimated_bytes)
FROM logs
GROUP BY target
ORDER BY SUM(estimated_bytes) DESC;
```

Other evidence:

- installed extension `package.json` and bundled executable version;
- installed extension bundle launch/initialize code;
- VS Code logs under
  `~/.config/Code/logs/20260709*/window1/exthost/openai.chatgpt/Codex.log`;
- current OpenAI source at commit
  `1f0566d3f59298d1bb88820a0d35294f1eeb07ea`, especially
  `codex-rs/state/src/runtime.rs` and `runtime/logs.rs`;
- `scripts/architecture_program_runner.py` and its command, environment,
  worker, phase-observation, transition, artifact, and validation modules;
- archived architecture runner incident and telemetry reports under
  `docs/plans/archive/`;
- immutable aggregate joins against `state_5.sqlite` and rollout first-record
  metadata; no rollout bodies were emitted;
- repository Git history and surviving artifact timestamps.

## Final Assessment

The database became pathological because Codex's production runtime persisted
large volumes of TRACE transport data, continuously deleted it under retention
caps, and retained the freed pages in the main file. Heavy VS Code and subagent
use supplied the workload; `codex-config` was one material workload among
several. The architecture runner has real amplification risks, but it is not
proven to have produced most of the incident database.

The extension failure is best described as an upstream startup-resilience bug:
a rebuildable diagnostic log store is opened and maintained synchronously on
the app-server initialization path, and a pathological store can delay or
prevent the handshake. The exact blocking SQL operation remains the most
important unresolved incident detail.
