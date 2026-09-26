-- Which pages (blocks) hold the rows of customer 4242 and of customer 1; run after setup.sql (the data is seeded, so it is the same every run).
\echo === block (page) number of each order of customer 4242: (ctid::text::point)[0]
SELECT id, (ctid::text::point)[0]::int AS page FROM orders WHERE customer_id = 4242 ORDER BY page;
\echo === pages holding at least one order of customer 1, out of all pages
SELECT count(DISTINCT (ctid::text::point)[0]) AS pages_with_customer_1, (SELECT relpages FROM pg_class WHERE relname = 'orders') AS relpages FROM orders WHERE customer_id = 1;
