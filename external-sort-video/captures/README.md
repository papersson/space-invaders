# Real captures for the external-merge-sort video

Captured in a Linux container: Ubuntu 24.04, 4 cores, 16 GB RAM, no swap. Versions: GNU
coreutils `sort` 9.4, Python 3.11.15, PostgreSQL 16.13. The scripts that made each file are
in `scripts/`. The big inputs (1 GB records file, sort output, temp dirs, Postgres cluster)
were deleted afterwards.

Caveat for timings: with 16 GB of RAM the 1 GB input sat in the page cache, and temp files
and output went through the page cache too. The *shape* is real (run count, run sizes,
merge phase, memory ceiling). The speeds are faster than a cold disk would give.

## Version 2 captures (2026-09-26): `gnu_sort_tmp.json`, `python_memoryerror.json`

Re-captured so the demo's numbers line up exactly, in decimal units throughout. GNU sort keeps
a pointer structure for every line inside its `-S` buffer, so with short records the runs come
out much smaller than the buffer (100-byte records: a 160 MiB buffer made 86 MB runs). With
10,000-byte records that bookkeeping is about 1%, and the file-to-memory ratio predicts the run
count directly.

- **Input:** `python3 scripts/gen_records.py records.txt 100000 20260926 9988` writes
  100,000 records × 10,000 bytes = 1,000,000,000 bytes (10 random `A-Z` key characters, a
  space, 9,988 random `[A-Za-z0-9]` characters, `\n`).
- **Sort:** `python3 scripts/capture_gnu_sort.py <workdir> 86000000b gnu_sort_tmp.json` runs
  `LC_ALL=C sort -S 86000000b -T sort-tmp records.txt -o sorted.txt` (86,000,000 bytes of
  buffer, default `--parallel`, 4 threads). The file is 11.6 buffers long. Result: 12 temp
  files, 11 × 85,180,000 B and 1 × 63,020,000 B; one 12-way merge while `sorted.txt` grows
  from 4.2 s; all temp files deleted at the end; exit at 8.74 s; peak RSS 87,380 kB.
- **Python:** `python3 scripts/capture_python_oom.py <workdir> 83984 python_memoryerror.json`
  runs `bash -c "ulimit -v 83984; exec python3 -c \"lines = sorted(open('records.txt'))\""`:
  83,984 KiB = 86,000,000 bytes, the same as sort's buffer. Result: a real `MemoryError`
  after 0.078 s (return code 1). Two samples fit before it died (RSS 53,788 kB, VmSize
  59,960 kB); the failing allocation was the one that would have crossed the cap.
- An intermediate version 2 attempt used 1000-byte records and `-S 88M` (88 MiB). It also made
  12 runs, but 1 GB is only 10.8 times 88 MiB, and mixing decimal and binary units made the
  on-screen arithmetic inconsistent, so it was replaced.

## Version 1 captures (2026-09-25, replaced)

The first versions used 100-byte records, `sort -S 160M` (12 runs of 85.6 MB, one 12-way
merge, 6.9 s, peak RSS 167,416 kB) and Python under a 600,000 kB cap (`MemoryError` at
586,176 kB RSS after 0.57 s). They are in git history. The two sections below still describe
files from that session.

## `gnu_sort_tmp_S80M_batch16_evidence.json` (extra, version 1 input)

This is the version 1 capture (100-byte records) with `-S 80M`. It is the empirical check of the default `--batch-size`:

- **Runs:** sort wrote 24 runs, 23 × 42,799,000 B and 1 × 15,623,000 B.
- **Intermediate merge:** a 25th file (`sortlo9qU6`) appeared and grew to 684,784,000 B,
  which is exactly 16 × 42,799,000. The 16 runs it merged were then deleted.
- **Final merge:** 9 inputs, the 8 leftover runs plus the merged file.
- **Totals:** peak RSS 85,540 kB, duration 6.04 s.
- **Control run (not saved):** the same command with `--batch-size=32`. It had 24 temp
  files, none larger than 42,799,000 B, so there was no intermediate merge.

**Default `--batch-size` = 16.** The coreutils 9.4 manual (`/usr/share/info/coreutils.info.gz`,
read with `zcat` because the `info` program is not installed) says: "The default value is
currently 16, but this is implementation-dependent". The run above confirms it.

**Temp file names:** `sort` plus 6 random alphanumeric characters (a mkstemp template
`sortXXXXXX`), created directly in the `-T` directory. Examples: `sortluWSiI`, `sortVmDXbr`,
`sort8InJy0`.

A first trial at `-S 80M` took 16.4 s instead of 6.0 s, with the same file pattern. That was
probably disk writeback, and that run was not kept.

## `postgres_explain.txt`

This is a throwaway PostgreSQL 16.13 cluster. The setup, exact SQL and verbatim `psql -e`
output are in the file (`scripts/pg_load.sql`, `scripts/pg_explain.sql`).

- **Cluster:** `initdb --locale=C --encoding=UTF8`, run as user `postgres`, port 54329,
  unix socket only. Otherwise default settings.
- **Table:** 1,000,000 rows from `generate_series` + `md5(random()::text)` with `setseed(0.42)`:
  a 10-char key and an 88-char payload, 128 MB.
- **RUN 1, `work_mem = '4MB'` (default):** the planner chose a parallel plan (Gather Merge,
  2 workers). `Sort Method: external merge  Disk: 40328kB`, plus
  `Worker 0:  Sort Method: external merge  Disk: 30048kB` and
  `Worker 1:  Sort Method: external merge  Disk: 37472kB`.
- **RUN 2, `work_mem = '1GB'`:** `Sort Method: quicksort  Memory: 149577kB`, a serial Sort.
- **RUN 3 (extra), 4MB with `max_parallel_workers_per_gather = 0`:**
  `Sort Method: external merge  Disk: 107696kB`.
- **RUN 4 (extra), RUN 3 with `trace_sort = on`:** 38 runs were written. A merge pass over
  15 tapes left 3 runs, and a 3-way final merge ran on the fly. The log reports
  13462 disk blocks, which is the same 107,696 kB.

Deviation: the data dir and socket were in `/tmp/pgcapture-54329`, not in the scratch dir.
There were two reasons:

- The scratch dir's parent `/tmp/claude-0` is root-only, mode 700, and was automatically
  reset to 700 when I opened it. So the `postgres` user could not reach a data dir there.
- The socket path under scratch was longer than the 107-byte unix-socket limit.

The server was stopped and that directory was deleted.
