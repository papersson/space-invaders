SET max_parallel_workers_per_gather = 0;   -- one process per query, so plans and times are easy to read
-- Warm up: read the table and index once, so every timing below is with the data in memory.
\o /dev/null
SELECT count(*), sum(amount) FROM orders;
SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
SELECT count(*) FROM customers;
\o
-- median_ms(q): run EXPLAIN ANALYZE on q seven times and return the median execution time in ms.
CREATE OR REPLACE FUNCTION pg_temp.median_ms(q text) RETURNS numeric LANGUAGE plpgsql AS $f$
DECLARE j json; ts numeric[] := '{}';
BEGIN
  FOR i IN 1..7 LOOP
    EXECUTE 'EXPLAIN (ANALYZE, FORMAT JSON) ' || q INTO j;
    ts := ts || (j->0->>'Execution Time')::numeric;
  END LOOP;
  RETURN (SELECT round(percentile_cont(0.5) WITHIN GROUP (ORDER BY x)::numeric, 3) FROM unnest(ts) x);
END $f$;
\echo === 0. the size of the orders table, in pages
SELECT relpages FROM pg_class WHERE relname = 'orders';
\echo === 1. the same query, a rare customer (customer 4242) and a common one (customer 1, about 30% of orders)
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242;
SELECT pg_temp.median_ms($q$SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242$q$) AS median_ms_of_7_runs;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
SELECT pg_temp.median_ms($q$SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1$q$) AS median_ms_of_7_runs;
\echo === 2. the rare customer with a full scan forced (index and bitmap scans off)
SET enable_indexscan = off; SET enable_bitmapscan = off;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242;
SELECT pg_temp.median_ms($q$SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242$q$) AS median_ms_of_7_runs;
RESET enable_indexscan; RESET enable_bitmapscan;
\echo === 3. the common customer with a full scan forced (index and bitmap scans off)
SET enable_indexscan = off; SET enable_bitmapscan = off;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1;
SELECT pg_temp.median_ms($q$SELECT count(*), sum(amount) FROM orders WHERE customer_id = 1$q$) AS median_ms_of_7_runs;
RESET enable_indexscan; RESET enable_bitmapscan;
\echo === 4. a join: 100 customers in Tromsø, 99,900 in Oslo
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Tromsø';
SELECT pg_temp.median_ms($q$SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Tromsø'$q$) AS median_ms_of_7_runs;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Oslo';
SELECT pg_temp.median_ms($q$SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Oslo'$q$) AS median_ms_of_7_runs;
\echo === 4b. Oslo with a nested loop forced (hash and merge joins off)
SET enable_hashjoin = off; SET enable_mergejoin = off;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Oslo';
SELECT pg_temp.median_ms($q$SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Oslo'$q$) AS median_ms_of_7_runs;
RESET enable_hashjoin; RESET enable_mergejoin;
\echo === 5. stale statistics: gathered while customer 1 had 30% of orders; then their older orders were archived
DROP TABLE IF EXISTS orders_s;
CREATE TABLE orders_s (LIKE orders INCLUDING ALL) WITH (autovacuum_enabled = false);
INSERT INTO orders_s SELECT * FROM orders;
ANALYZE orders_s;
DELETE FROM orders_s WHERE customer_id = 1 AND id < 1999000;
VACUUM orders_s;
EXPLAIN (ANALYZE, SUMMARY) SELECT id, amount FROM orders_s WHERE customer_id = 1 ORDER BY id LIMIT 10;
SELECT pg_temp.median_ms($q$SELECT id, amount FROM orders_s WHERE customer_id = 1 ORDER BY id LIMIT 10$q$) AS median_ms_of_7_runs;
\echo === 6. after ANALYZE
ANALYZE orders_s;
EXPLAIN (ANALYZE, SUMMARY) SELECT id, amount FROM orders_s WHERE customer_id = 1 ORDER BY id LIMIT 10;
SELECT pg_temp.median_ms($q$SELECT id, amount FROM orders_s WHERE customer_id = 1 ORDER BY id LIMIT 10$q$) AS median_ms_of_7_runs;
\echo === 7. counts
SELECT count(*) AS orders, count(*) FILTER (WHERE customer_id = 1) AS customer_1, count(*) FILTER (WHERE customer_id = 4242) AS customer_4242 FROM orders;
SELECT city, count(*) FROM customers GROUP BY city ORDER BY city;
SELECT version();
