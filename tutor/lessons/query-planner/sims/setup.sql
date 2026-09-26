-- Orders for 100,000 customers; customer 1 is a big reseller with 30% of all orders.
DROP TABLE IF EXISTS orders, customers;
SELECT setseed(0.42);
CREATE TABLE customers (id int PRIMARY KEY, city text NOT NULL);
INSERT INTO customers
SELECT g, CASE WHEN g % 1000 = 0 THEN 'Tromsø' ELSE 'Oslo' END FROM generate_series(1, 100000) g;
CREATE TABLE orders (id bigint PRIMARY KEY, customer_id int NOT NULL, amount numeric(10,2) NOT NULL);
INSERT INTO orders
SELECT g,
       CASE WHEN random() < 0.30 THEN 1 ELSE 2 + floor(random() * 99999)::int END,
       round((5 + random() * 195)::numeric, 2)
FROM generate_series(1, 2000000) g;
CREATE INDEX orders_customer ON orders (customer_id);
ALTER TABLE orders SET (autovacuum_enabled = false);
ANALYZE customers; ANALYZE orders;
