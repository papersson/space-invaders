SET max_parallel_workers_per_gather = 0;
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Tromsø';
EXPLAIN (ANALYZE, SUMMARY) SELECT count(*), sum(o.amount) FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Oslo';
