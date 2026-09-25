# Real captures for the external-merge-sort video

All captured 2026-09-25 in a Linux container: Ubuntu 24.04, 4 cores, 16 GB RAM, no swap.
Versions: GNU coreutils `sort` 9.4, Python 3.11.15, PostgreSQL 16.13. The scripts that made
each file are in `scripts/`. The big inputs (1 GB records file, sort output, temp dirs,
Postgres cluster) were deleted afterwards.

Caveat for timings: with 16 GB of RAM the 1 GB input sat in the page cache, and temp files
and output went through the page cache too. The *shape* is real (run count, run sizes,
merge phase, memory ceiling). The speeds are faster than a cold disk would give.

## Input: `records.txt` (not kept)

`python3 scripts/gen_records.py records.txt 10000000 20260925` writes 10,000,000 records
× 100 bytes = 1,000,000,000 bytes. Each record is 10 random uppercase letters `A-Z`, a
space, 88 random `[A-Za-z0-9]` characters, and `\n`. The generator is `random.Random(20260925)`
with rejection sampling so every character is uniform. It took 17.7 s.

## `gnu_sort_tmp.json`

`python3 scripts/capture_gnu_sort.py <workdir> 160M gnu_sort_tmp.json` runs
`LC_ALL=C sort -S 160M -T sort-tmp records.txt -o sorted.txt`. It uses the default
`--parallel`, which here is 4 threads. The run exited 0, and `sort -c` confirmed the output.

- **Sampler:** every 0.1 s it records the temp dir listing (name, bytes), the output size,
  and `VmRSS` from `/proc/<pid>/status`. It also records the process state from
  `/proc/<pid>/stat`, an extra `state` field.
- **Kept samples:** a sample is kept when anything changed, and at least every 0.5 s.
  The last sample is taken after exit (`state: "exited"`, `sort_rss_kb: 0`).
- **Extra top-level fields:** `sort_peak_rss_kb_vmhwm`, `sort_peak_rss_kb_ru_maxrss`
  (from `wait4`), `temp_file_names_in_order_seen`, `returncode`, `stderr`, `nproc`.
- **Buffer size:** I tuned `-S`. At `-S 80M` the run made 24 runs, which is more than 16
  and forces an intermediate merge (see below). `-S 160M` gives 12.

Result:

| | |
|---|---|
| Temp files | 12: 11 × 85,598,000 B (855,980 records each) + 1 × 58,422,000 B |
| Run phase | 0.2 s to 3.9 s. Files appear one at a time, each empty at first, then growing to full size. |
| Final merge | One 12-way merge, 3.9 s to 6.5 s. Output grows 0 to 1 GB and all temp files vanish at the end. |
| Exit | 6.90 s. The process sat in state `D` for about 0.4 s after the output was complete. |
| Peak RSS | 167,416 kB (VmHWM); `ru_maxrss` 167,092 kB. The `-S` value is 160 MiB = 163,840 kB. |

## `gnu_sort_tmp_S80M_batch16_evidence.json` (extra)

This is the same capture with `-S 80M`. It is the empirical check of the default `--batch-size`:

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

## `python_memoryerror.json`

`python3 scripts/capture_python_oom.py <workdir> 600000 python_memoryerror.json` runs
`bash -c "ulimit -v 600000; exec python3 -c \"lines = sorted(open('records.txt'))\""`. The
`exec` makes the sampled PID the Python process itself; the first sample, at t = 0.001 s,
is still bash. The sampler reads `VmRSS` every 0.05 s, plus `VmSize` in an extra
`vmsize_kb` field.

- **Result:** a real `MemoryError`, not a kill. The return code is 1 and stderr is:
  `Traceback (most recent call last):\n  File "<string>", line 1, in <module>\nMemoryError\n`
- **Memory:** RSS climbed about 1.3 GB/s to a peak of 586,176 kB (VmHWM = ru_maxrss).
  VmPeak was 599,972 kB, just under the 600,000 kB cap. The last two samples (380 MB,
  then 114 MB) show Python freeing the partial list after the exception.
- **Timing:** the process exited at 0.569 s, which leaves only 12 samples.
- **How far it got:** I also ran a variant with the same cap (a loop that appends lines and
  catches the error), not saved. It died after 3,505,991 lines, about 35% of the file.
- **Earlier run:** one run was made while another CPU-heavy process (the video's TTS job)
  was running. It took 2.76 s and was replaced. The saved run was on an idle machine and
  matches an earlier run (0.59 s).

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
