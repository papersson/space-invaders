\echo '--- RUN 1: work_mem = 4MB (the PostgreSQL default) ---'
SET work_mem = '4MB';
EXPLAIN (ANALYZE, COSTS OFF) SELECT * FROM records ORDER BY k;
\echo '--- RUN 2: work_mem = 1GB ---'
SET work_mem = '1GB';
EXPLAIN (ANALYZE, COSTS OFF) SELECT * FROM records ORDER BY k;
\echo '--- RUN 3 (supplementary): work_mem = 4MB, parallel query disabled ---'
SET work_mem = '4MB';
SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, COSTS OFF) SELECT * FROM records ORDER BY k;
\echo '--- RUN 4 (supplementary): same as RUN 3, with trace_sort = on (server LOG lines sent to the client) ---'
SET trace_sort = on;
SET client_min_messages = log;
EXPLAIN (ANALYZE, COSTS OFF) SELECT * FROM records ORDER BY k;
