SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
SET enable_indexscan = off; SET enable_bitmapscan = off;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242;
RESET enable_indexscan; RESET enable_bitmapscan;
SET enable_seqscan = off; SET enable_bitmapscan = off;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
