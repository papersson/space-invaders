\timing off
-- Q: the same query for a rare customer and a common one
EXPLAIN (ANALYZE, COSTS, TIMING, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242;
EXPLAIN (ANALYZE, COSTS, TIMING, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
-- forced the other way
SET enable_indexscan = off; SET enable_bitmapscan = off;
EXPLAIN (ANALYZE, COSTS, TIMING, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242;
RESET enable_indexscan; RESET enable_bitmapscan;
SET enable_seqscan = off;
EXPLAIN (ANALYZE, COSTS, TIMING, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
RESET enable_seqscan;
