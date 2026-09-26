You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** The same SQL query, `SELECT count(*), sum(amount) FROM orders WHERE customer_id = ?`, takes fifteen microseconds for one customer and 135 milliseconds for another, on the same table, on the same machine. Nothing in the query says how to run it. So who decides, and why is the same query sometimes fast and sometimes slow?

**Answer.** SQL is declarative: you say what rows you want, not how to find them. The database's query planner considers the ways it could run the query (read every page of the table, or use an index to read only the pages that hold matching rows; for a join, which table first and which join method), estimates the cost of each from statistics it keeps about the data (how many rows, how common each value is), and runs the cheapest estimate. For a rare customer, the index means reading ten pages instead of 12,739, and forcing a full scan is thousands of times slower. For a customer with 30% of the rows, those rows are on every page, so every plan reads the whole table: the index saves nothing, and no plan is fast. The same goes for joins: a few matching customers suit a nested loop of index lookups, and almost all of them suit a hash join. The plan is only as good as the estimate: when the statistics are out of date, the planner can pick a plan that is thousands of times slower, and `ANALYZE` fixes it. So the same query is fast or slow depending on the data it touches and on what the planner believes about that data.

**Takeaway.** You say what; the planner decides how, by estimating how many rows each step will touch. Fast or slow depends on the data and on the planner's estimate of it. When a query is slow, compare the estimated rows with the actual rows in `EXPLAIN ANALYZE`.

**Wrong model.** The database runs the query the way it's written, the same way every time; an index always makes it faster; and if it's slow, add an index.

**Objectives.**
1. Contrast a declarative query with a hand-written loop, and say what the database is free to choose.
2. Describe the two basic ways to find rows (a full scan, an index) in terms of pages read, and when the index saves work.
3. Explain how the planner chooses: estimated rows from statistics, estimated cost, cheapest estimate.
4. Explain how a join's method depends on how many rows match (nested loop vs hash join).
5. Explain how stale statistics lead to a bad plan, how to see it (estimated vs actual rows), and how `ANALYZE` fixes it.


## Chain

1. The question: one query, fifteen microseconds for one customer, 135 ms for another. Who decides how it runs?
2. Because SQL is declarative: the query says what, not how. The database is free to choose, and must.
3. Therefore two ways to find a customer's orders: read every page, or use the index to read only the pages with matching rows. The index saves work only if those rows are on few pages, which depends on the customer.
4. Therefore the planner estimates: from statistics it knows how common each customer is, estimates rows and cost for each plan, and picks the cheapest. Real plans: ten pages for the rare customer (a full scan forced: nearly 5,000 times slower); every page for the common one (a full scan forced: no faster).
5. Therefore joins, too: nested loop or hash join, depending on how many rows match (real: 5 ms for Tromsø; 721 ms for Oslo, and 2 s with a nested loop forced).
6. But the estimate can be wrong: statistics are a snapshot. After the data changed, the planner expected 420,000 rows, found 294, and took 137 ms; after ANALYZE, 0.061 ms. No index was added.
7. Therefore the answer.

Deviation from the canonical progression: join order search (dynamic programming over subsets) and the cost model's formulas are left out; the research lists them as the textbook core, but the practitioner question is answered by scan choice, join method and estimates. Random versus sequential access is left out too: every run here has the data in memory, and the page count carries the argument. The declarative-vs-imperative contrast is kept short.


## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a table of two million orders, and one query: count a customer's orders, and add up the amounts.
> For customer four thousand two hundred and forty-two, it takes fifteen microseconds.
> For customer one, it takes a hundred and thirty-five milliseconds. About nine thousand times longer.
> Same query, same table, same machine. And nothing in the query says how to run it.
> So who decides? And why is the same query sometimes fast, and sometimes slow?

*Screen:* the query in a code card: `SELECT count(*), sum(amount) FROM orders WHERE customer_id = ?`. Two runs from data/runs.txt (median of seven): "customer 4242 → 0.015 ms" and "customer 1 → 135.4 ms", with a bar of each (log scale noted). Caption: "PostgreSQL 16.9 · 2,000,000 orders · data in memory · median of 7 runs". The question.

### 2. Say what, not how

> In ordinary code, you'd write the search yourself: loop over every order, and keep the ones for this customer. The code says exactly how.
> SQL is declarative. The query says what rows you want, and nothing about how to find them.
> That leaves the database free to choose how. And it has to choose, every time the query runs.

*Screen:* a loop in code: `for order in orders: if order.customer_id == 4242: …` beside the SQL card. The loop's steps light up one by one ("how"); the SQL's WHERE clause lights up alone ("what"). A small "?" over the gap between the SQL and the data: "how?".

### 3. Two ways to find the rows

> The table is stored in pages, blocks of about a hundred and fifty rows each. This one has about twelve thousand seven hundred pages.
> There are two basic ways to find one customer's orders.
> One is a full scan: read every page, and keep the rows that match. That's the same work whoever the customer is.
> The other is an index: a sorted list of customer numbers, each pointing to where that customer's rows are. Find the customer in the list, collect where their rows are, and read only those pages, each once.
> Customer four thousand two hundred and forty-two has ten orders, on ten pages. Through the index, that's ten pages instead of twelve thousand seven hundred.
> Customer one has six hundred thousand orders, and they're spread over every page of the table. Now the index can't skip anything. Every page has to be read anyway.
> So whether the index saves work depends on how many rows match. And that depends on the customer.

*Screen:* the table as a long strip of small pages (12,739, drawn as a grid with the count "12,739 pages · ~157 rows each", from part 0 of data/runs.txt). A full scan sweeps every page. Then the index: a sorted column of customer numbers on the left; customer 4242's entry points to ten pages, which light up (ICE); a counter "10 of 12,739 pages". Then customer 1's entry: pages light up until every page is lit; counter "12,739 of 12,739 pages".

### 4. The planner estimates

> The choice between them is made by the query planner.
> The planner keeps statistics about each table: how many rows it has, and for each column, which values are most common, and how common.
> For each way it could run the query, it estimates the rows and pages it would touch, turns that into a cost in its own units, and picks the cheapest.
> For customer four thousand two hundred and forty-two, the statistics say rare. The planner estimates thirty-three rows; the real number is ten, close enough to choose well. It picks the index, read the way we just saw: collect the rows' locations, then read each of their pages once. PostgreSQL calls that a bitmap scan. Ten pages, fifteen microseconds.
> Force a full scan for the same customer, and it takes seventy-two milliseconds: nearly five thousand times slower. The choice matters.
> For customer one, the statistics say about three in ten orders. The planner estimates about six hundred thousand rows, and picks the same kind of bitmap scan. But this time the pages it reads are all of them. A hundred and thirty-five milliseconds. Force a full scan instead, and it's no faster.
> When the rows you want are on every page, the index doesn't help, and no plan is fast.

*Screen:* a statistics card for orders.customer_id: "customer 1: ~30% of rows (most common value)"; "others: ~33 rows each (estimated)". Then two real plans from data/runs.txt, as small trees: (a) customer 4242: `Bitmap Index Scan on orders_customer` → `Bitmap Heap Scan`, "estimated 33 rows · actual 10 · Heap Blocks: 10 · 0.015 ms"; the name "bitmap scan" appears under the ten lit pages from chapter 3. Then "customer 4242, full scan forced (Seq Scan): 72.0 ms" (coral). (b) customer 1: the same two nodes, "estimated 591,533 · actual 600,698 · Heap Blocks: 12,739 · 135.4 ms"; then "customer 1, full scan forced: 135.6 ms" (grey, "no faster").

### 5. Joins

> Everything so far read one table. Now ask for the orders of every customer in Tromsø. Two tables have to meet, and the planner has to choose how to match their rows.
> A hundred customers live in Tromsø, out of a hundred thousand.
> The planner finds those hundred customers, then, for each one, looks up its orders in the index. That's a nested loop: for each row on one side, look up its matches on the other. Five milliseconds.
> Now ask for customers in Oslo: ninety-nine thousand nine hundred of them. This time the planner builds a lookup table from the Oslo customers, and streams all two million orders through it, once. That's a hash join. Seven hundred milliseconds, for almost two million rows.
> Force a nested loop for Oslo instead, and it takes two seconds: nearly three times as long.
> Same query shape. A different plan, because a different number of rows match.

*Screen:* two plans from data/runs.txt side by side. Tromsø: `Nested Loop` over `Seq Scan on customers (100 rows)` and `Bitmap Heap Scan on orders` per customer (100 loops, 13 rows each), "1,346 rows · 5.1 ms". Oslo: `Hash Join` of `Seq Scan on orders (2,000,000)` with `Hash` of `Seq Scan on customers (99,900)`, "1,998,654 rows · 721 ms". An animation of each: 100 small index lookups vs one hash table and a stream. Then "Oslo, nested loop forced: 2,024 ms" (coral).

### 6. When the estimate is wrong

> The plan is only as good as the estimate, and the statistics are a snapshot.
> Here's a copy of the orders table. Its statistics were gathered while customer one still had three in ten orders. Since then, their older orders were archived, and just two hundred and ninety-four are left, all of them recent.
> Now ask for customer one's first ten orders, by order number.
> The planner still believes customer one is everywhere: about four hundred and twenty thousand rows. So it walks through the orders by order number, expecting to run into ten of theirs almost at once. Instead it passes about one point four million other rows before it finds them. A hundred and thirty-seven milliseconds.
> Run ANALYZE, which refreshes the statistics, and the planner now expects about three hundred rows. It looks them up in the index, sorts them, and keeps the first ten. Sixty microseconds: more than two thousand times faster, for the same query.
> Nobody added an index. The one on customer number was there all along. The planner just didn't expect it to help.
> That's how to read a slow plan. EXPLAIN ANALYZE shows, for each step, the rows the planner expected and the rows it actually got. Where the two are far apart, the plan was chosen for data that isn't there.

*Screen:* a caption "orders_s: a copy of orders, statistics gathered before the archiving (autovacuum off)". data/runs.txt, part 5: `Limit` → `Index Scan using orders_s_pkey`, "estimated 419,506 rows · actual 10 · Rows Removed by Filter: 1,398,620 · 136.8 ms" (coral). A scan arrow crawling down the order numbers past almost everything. Then `ANALYZE orders_s;` and part 6: `Limit` → `Sort (top-N)` → `Bitmap Heap Scan` via `orders_s_customer_id_idx`, "estimated 327 · actual 294 · Heap Blocks: 7 · 0.061 ms" (ICE). Then an EXPLAIN ANALYZE line with "rows=419506" and "actual … rows=10" circled side by side: "estimate vs reality".

### 7. The answer

> So who decides how a query runs? The query planner, because SQL only says what you want.
> It weighs the ways it could run the query by how many rows and pages each step will touch, using statistics about your data. A rare customer gets the index, and ten pages. For a common one, every page has to be read, whatever the plan. A few matches get a nested loop; many get a hash join.
> That's why the same query can be fast or slow: it depends on the data it touches, and on what the planner believes about that data.
> When a query is slow, don't guess, and don't just add an index. Run EXPLAIN ANALYZE, and compare the rows the planner expected with the rows it got.

*Screen:* the two cards from chapter 1 again (0.015 ms, 135.4 ms) with their page counts underneath (10 pages, 12,739 pages). Three lines: "rare → index → 10 pages", "common → every page, whatever the plan", "stale statistics → wrong plan → ANALYZE". An EXPLAIN ANALYZE line with its estimated and actual rows highlighted. End card with the takeaway and references: Selinger et al., "Access Path Selection in a Relational Database Management System", SIGMOD (1979); PostgreSQL documentation, §14.1 "Using EXPLAIN" and §14.2 "Statistics Used by the Planner"; Kleppmann, Designing Data-Intensive Applications (2017), ch. 2; Winand, Use The Index, Luke; Leis et al., "How Good Are Query Optimizers, Really?", PVLDB (2015).

