SELECT setseed(0.42);
CREATE TABLE records(k text, payload text);
INSERT INTO records
SELECT left(md5(random()::text), 10),
       left(md5(random()::text) || md5(random()::text) || md5(random()::text), 88)
FROM generate_series(1, 1000000);
VACUUM ANALYZE records;
SELECT count(*), pg_size_pretty(pg_table_size('records')) AS table_size,
       avg(length(k)) AS avg_k_len, avg(length(payload)) AS avg_payload_len
FROM records;
SELECT * FROM records LIMIT 3;
