SET max_parallel_workers_per_gather = 0;
-- statistics were gathered when customer 1 had 30% of orders; then their orders were archived
BEGIN;
DELETE FROM orders WHERE customer_id = 1 AND id > 20;
EXPLAIN (ANALYZE, SUMMARY) SELECT id, amount FROM orders WHERE customer_id = 1 ORDER BY id LIMIT 10;
ANALYZE orders;
EXPLAIN (ANALYZE, SUMMARY) SELECT id, amount FROM orders WHERE customer_id = 1 ORDER BY id LIMIT 10;
ROLLBACK;
