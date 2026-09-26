SET max_parallel_workers_per_gather = 0;
DROP TABLE IF EXISTS orders_s;
CREATE TABLE orders_s (LIKE orders INCLUDING ALL) WITH (autovacuum_enabled = false);
INSERT INTO orders_s SELECT * FROM orders;
ANALYZE orders_s;                                               -- statistics: customer 1 has ~30% of orders
DELETE FROM orders_s WHERE customer_id = 1 AND id < 1999000;    -- then customer 1's older orders are archived
VACUUM orders_s;                                                -- space reclaimed; column statistics not refreshed
EXPLAIN (ANALYZE, SUMMARY) SELECT id, amount FROM orders_s WHERE customer_id = 1 ORDER BY id LIMIT 10;
ANALYZE orders_s;
EXPLAIN (ANALYZE, SUMMARY) SELECT id, amount FROM orders_s WHERE customer_id = 1 ORDER BY id LIMIT 10;
