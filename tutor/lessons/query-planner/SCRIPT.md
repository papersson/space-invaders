# Same Query, Different Plan

Status: locked after review round 4

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

Deviation from the canonical progression: join order search (dynamic programming over subsets) and the cost model's formulas are left out; the research lists them as the textbook core, but the practitioner question is answered by scan choice, join method and estimates. Merge join, PostgreSQL's third join method, is left out (a small caption in chapter 5 says so). Random versus sequential access is left out too: every run here has the data in memory, and the page count carries the argument. The declarative-vs-imperative contrast is kept short.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1-2 | Narrated animation | A query card, two timings; the same query written as a loop. |
| 3-4 | Narrated animation with real output | A table as a grid of pages, a scan sweeping all of them, an index lighting only the pages it needs; plan trees, page counts and timings from real `EXPLAIN ANALYZE` runs. |
| 5 | Narrated animation with real output | Two join plans side by side. |
| 6 | Narrated animation with real output | Estimated vs actual rows, before and after `ANALYZE`. |
| 7 | Narrated animation | Payoff. |
| (not built) | Hands-on exercise | Run `EXPLAIN ANALYZE` on your own tables; sweep a filter value and watch the plan flip; run a query before and after `ANALYZE`. The research names doing as the way plan flips are understood; offered, not added. |
| (not built) | Reading | Join-order search, the cost model's parameters, extended statistics for correlated columns, plan caching. |

## Ledgers

**Setups and payoffs.**
- 15 µs vs 135 ms (ch. 1) is explained in ch. 3-4: ten pages vs every page.
- "Nothing in the query says how" (ch. 1) is declarativeness (ch. 2).
- Pages (ch. 3) return in every plan: 10, 12,739, 1,346, 7.
- The estimate of 33 against 10 actual (ch. 4, "close enough") sets up the estimate that is far off (ch. 6).
- The index (ch. 3) returns in ch. 6: it was there all along.

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| declarative | ch. 2 | saying what result you want, not how to compute it |
| page | ch. 3 | the block a table is stored in, about 150 rows here; the unit a scan reads |
| full scan | ch. 3 | reading every page of the table (PostgreSQL's plan node: Seq Scan) |
| index | ch. 3 | a sorted list of one column's values, each pointing to its rows |
| query planner | ch. 4 | the part of the database that chooses how to run a query |
| statistics | ch. 4 | the planner's summary of the data: row counts, common values and how common they are |
| cost | ch. 4 | the planner's estimate of a plan's work, in its own units, from the pages and rows it expects to touch |
| bitmap scan | ch. 4 | PostgreSQL's way of using an index for more than a few rows: collect the row locations, sort them by page, read each page once |
| plan | ch. 4 | the chosen way to run a query: which scans, which join methods, in what order |
| nested loop / hash join | ch. 5 | for each row of one table, look up matches in the other / build a lookup table from one side, then stream the other through it |
| ANALYZE | ch. 6 | the command that refreshes the statistics |

**Numbers to remember.** 15 µs vs 135 ms for the same query: 10 pages vs all 12,739. With stale statistics, 137 ms; after ANALYZE, 0.061 ms.

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a table of two million orders, and one query: count a customer's orders, and add up the amounts.
> For customer 4242, it takes fifteen microseconds to execute.
> For customer one, it takes a hundred and thirty-five milliseconds. About nine thousand times longer.
> Same query, same table, same machine. And nothing in the query says how to run it.
> So who decides? And why is the same query sometimes fast, and sometimes slow?

*Screen:* the query in a code card, run twice with a literal value: `SELECT count(*), sum(amount) FROM orders WHERE customer_id = 4242`, then the same with `= 1`. Two runs from data/runs.txt (median of seven): "customer 4242 → 0.015 ms" and "customer 1 → 135.4 ms", with a bar of each (log scale noted). Caption: "PostgreSQL 16.9 · 2,000,000 orders · data in memory · parallel query off · execution time (planning excluded), median of 7 runs". The question.

### 2. Say what, not how

> In ordinary code, you'd write the search yourself: loop over every order, and keep the ones for this customer. The code says exactly how.
> SQL is declarative. The query says what rows you want, and nothing about how to find them.
> That leaves the database free to choose how. And it has to choose, every time the query runs.

*Screen:* a loop in code: `for order in orders: if order.customer_id == 4242: …` beside the SQL card. The loop's steps light up one by one ("how"); the SQL's WHERE clause lights up alone ("what"). A small "?" over the gap between the SQL and the data: "how?".

### 3. Two ways to find the rows

> The table is stored in pages, blocks of about a hundred and sixty rows each. Two million orders fill about twelve thousand seven hundred of them.
> There are two basic ways to find one customer's orders.
> One is a full scan: read every page, and keep the rows that match. It reads the same pages whoever the customer is.
> The other is an index: a sorted list of customer numbers, each pointing to where that customer's rows are. Find the customer in the list, collect where their rows are, and read only the pages that hold them.
> Customer 4242 has ten orders, on ten pages. Through the index, that's ten pages instead of twelve thousand seven hundred.
> Customer one has about six hundred thousand orders. Orders are stored in the order they arrived, not by customer, so on every page, about three rows in ten are customer one's. Now the index can't skip anything. Every page has to be read anyway.
> So whether the index saves work depends on how many rows match. And that depends on the customer.

*Screen:* the table as a long strip of small pages (12,739, drawn as a grid with the count "12,739 pages · ~157 rows each", from part 0 of data/runs.txt). A full scan sweeps every page. Then the index: a sorted column of customer numbers on the left; customer 4242's entry points to ten pages, which light up (ICE); a counter "10 of 12,739 pages". Then customer 1's entry: pages light up until every page is lit; counter "12,739 of 12,739 pages".

### 4. The planner estimates

> The choice between them is made by the query planner.
> The planner keeps statistics about each table: how many rows it has, and for each column, which values are most common, and how common.
> For each way it could run the query, it estimates the rows and pages it would touch, turns that into a cost, a number for comparing plans rather than a time, and picks the cheapest.
> For customer 4242, the statistics say rare. The planner estimates thirty-three rows; the real number is ten, close enough to choose well. Its cost for using the index comes to about a hundred and thirty; for a full scan, about thirty-eight thousand. So it picks the index, read the way we just saw: collect the rows' locations, sort them by page, then read each of those pages once. PostgreSQL calls that a bitmap scan, shown as two steps: one reads the index, the other reads the pages. Ten pages, fifteen microseconds.
> Force a full scan for the same customer, and it takes seventy-two milliseconds: nearly five thousand times slower. The choice matters.
> For customer one, the statistics say about three in ten orders. The planner estimates about six hundred thousand rows, and picks the same kind of bitmap scan. But this time the pages it reads are all of them. A hundred and thirty-five milliseconds. Force a full scan instead, and it's no faster: it reads the same pages, and still has six hundred thousand rows to add up.
> When the rows you want are on every page, the index doesn't help, and no plan is fast.

*Screen:* a statistics card for orders.customer_id: "customer 1: ~30% of rows (most common value)"; "others: ~33 rows each (estimated)". The two costs for customer 4242, from data/runs.txt: "index (bitmap scan): cost 132" and "full scan: cost 37,739" ("in the planner's units, not ms"). Then two real plans from data/runs.txt, as small trees: (a) customer 4242: `Bitmap Index Scan on orders_customer` → `Bitmap Heap Scan`, "estimated 33 rows · actual 10 · Heap Blocks (pages): 10 · 0.015 ms"; the name "bitmap scan" appears under the ten lit pages from chapter 3. Then "customer 4242, full scan forced (Seq Scan): 72.0 ms" (coral). (b) customer 1: the same two nodes, "estimated 591,533 · actual 600,698 · Heap Blocks (pages): 12,739 · 135.4 ms"; then "customer 1, full scan forced: 135.6 ms" (grey, "no faster").

### 5. Joins

> Everything so far read one table. Now ask for the orders of every customer in Tromsø. Two tables have to meet, and the planner has to choose how to match their rows.
> A hundred customers live in Tromsø, out of a hundred thousand.
> The planner finds those hundred customers, then, for each one, looks up its orders in the index. That's a nested loop: for each row on one side, look up its matches on the other. About five milliseconds.
> Now ask for customers in Oslo: almost all of the hundred thousand. This time the planner builds a lookup table from the Oslo customers, and streams all two million orders through it, once. That's a hash join. About seven hundred milliseconds, for almost two million rows.
> Force a nested loop for Oslo instead, and it takes two seconds: nearly three times as long.
> Same query shape. A different plan, because a different number of rows match.

*Screen:* two plans from data/runs.txt side by side. Tromsø: `Nested Loop` over `Seq Scan on customers (100 rows)` and `Bitmap Heap Scan on orders` per customer (100 loops, 13 rows each), "5.1 ms". Oslo: `Hash Join` of `Seq Scan on orders (2,000,000)` ("Seq Scan = full scan") with `Hash` of `Seq Scan on customers (99,900)`, "1,998,654 rows · 721 ms". An animation of each: 100 small index lookups vs one hash table and a stream. Then "Oslo, nested loop forced: 2,024 ms" (coral). A small caption: "PostgreSQL has a third join method, merge join, not covered here".

### 6. When the estimate is wrong

> The plan is only as good as the estimate, and the statistics are a snapshot.
> Here's a copy of the orders table. Its statistics were gathered while customer one still had three in ten orders. Since then, their older orders were archived, and just two hundred and ninety-four are left, all of them recent.
> Now ask for customer one's first ten orders, by order number.
> The planner still believes customer one is everywhere: about four hundred and twenty thousand rows. So it walks through the orders by order number, expecting to run into ten of theirs almost at once. But all of theirs are at the very end. It passes about one point four million other rows first. A hundred and thirty-seven milliseconds.
> Run ANALYZE, which refreshes the statistics, and the planner now expects about three hundred and thirty rows. It looks them up in the index, sorts them, and keeps the first ten. Sixty microseconds: more than two thousand times faster, for the same query.
> The usual fix for a slow query is to add an index. But nobody added one here: the one on customer number was there all along. The planner just didn't expect it to help.
> That's how to read a slow plan. EXPLAIN ANALYZE shows, for each step, the rows the planner expected and the rows it actually got. Where the two are far apart, the plan was chosen for data that isn't there.

*Screen:* a caption "orders_s: a copy of orders · autovacuum off, so nothing re-ran ANALYZE after the archiving". data/runs.txt, part 5: `Limit` → `Index Scan using orders_s_pkey`, "estimated 419,506 rows · actual 10 · Rows Removed by Filter: 1,398,620 · 136.8 ms" (coral). A scan arrow crawling down the order numbers past almost everything. Then `ANALYZE orders_s;` and part 6: `Limit` → `Sort (top-N)` → `Bitmap Heap Scan` via `orders_s_customer_id_idx`, "estimated 327 · actual 294 · Heap Blocks: 7 · 0.061 ms" (ICE). Then an EXPLAIN ANALYZE line with "rows=419506" and "actual … rows=10" circled side by side: "estimate vs reality".

### 7. The answer

> So who decides how a query runs? The query planner, because SQL only says what you want.
> It weighs the ways it could run the query by how many rows and pages each step will touch, using statistics about your data. A rare customer gets the index, and ten pages. For a common one, every page has to be read, whatever the plan. A few matches, with an index to look them up, get a nested loop; many get a hash join.
> That's why the same query can be fast or slow: it depends on the data it touches, and on what the planner believes about that data.
> When a query is slow, don't guess, and don't just add an index. Run EXPLAIN ANALYZE, and compare the rows the planner expected with the rows it got.

*Screen:* the two cards from chapter 1 again (0.015 ms, 135.4 ms) with their page counts underneath (10 pages, 12,739 pages). Three lines: "rare → index → 10 pages", "common → every page, whatever the plan", "stale statistics → wrong plan → ANALYZE". An EXPLAIN ANALYZE line with its estimated and actual rows highlighted. End card with the takeaway and references: Selinger et al., "Access Path Selection in a Relational Database Management System", SIGMOD (1979); PostgreSQL documentation, §14.1 "Using EXPLAIN" and §14.2 "Statistics Used by the Planner"; Kleppmann, Designing Data-Intensive Applications (2017), ch. 2; Winand, Use The Index, Luke; Leis et al., "How Good Are Query Optimizers, Really?", PVLDB (2015).

## Evidence

| Claim | Source |
|---|---|
| Timings, plans, estimated and actual rows, pages read for every query in the lesson | sims/setup.sql, sims/queries.sql, sims/run_all.sh, data/runs.txt (PostgreSQL 16.9 from Nixpkgs 24.11 revision 50ab793786d9; 2,000,000 orders, customer 1 has 600,698, customer 4242 has 10; 100 customers in Tromsø, 99,900 in Oslo; parallel workers off for readable plans; the table and index are read once before any timing, so every run is in memory; each timing quoted is the median of seven EXPLAIN ANALYZE runs, printed under the plan) |
| The orders table is 12,739 pages (about 157 rows per page); customer 4242's rows are on 10 pages, customer 1's on all 12,739 | data/runs.txt, part 0 (`relpages`) and parts 1 (`Heap Blocks: exact=10`, `exact=12739`) |
| Customer 4242's ten orders sit on ten different pages (1, 2602, 3274, 3331, 3334, 5694, 6164, 8024, 8179, 10615); customer 1's orders are on all 12,739 pages (shown in chapter 3) | sims/pages.sql, data/pages.txt (block number from each row's ctid) |
| SQL is declarative: requests are stated without reference to access paths; the optimizer chooses indexes, join methods and order | Selinger et al. (1979), abstract; Kleppmann, DDIA (2017), ch. 2 ("Query Languages for Data") |
| Full scan vs index; which is cheaper depends on how many rows match (selectivity) | PostgreSQL docs §14.1 (tenk1: unique1 < 7000 → Seq Scan; < 100 → Bitmap; = 42 → Index Scan); Winand, Use The Index, Luke, ch. 1 and "Slow Indexes" |
| A bitmap scan takes row locations from the index, sorts them into physical order, and reads each needed page once; not all pages have to be visited | PostgreSQL docs §14.1 ("the upper plan node sorts the row locations identified by the index into physical order before reading them … The 'bitmap' mentioned in the node names is the mechanism that does the sorting") |
| The planner keeps statistics (row counts, most common values and their frequencies) and estimates rows and cost; picks the cheapest estimated plan | PostgreSQL docs §14.2 "Statistics Used by the Planner" and §51.5; Selinger et al. (1979) |
| Cost is in arbitrary units, based mostly on pages and rows expected to be touched; costs are relative, not absolute times | PostgreSQL docs §14.1 and §19.7.2 (planner cost constants: seq_page_cost, random_page_cost, cpu_tuple_cost); Selinger (1979): "costs predicted … often not accurate in absolute value" |
| Forced plans: 4242 with a full scan 72.0 ms; customer 1 with a full scan 135.6 ms (vs 135.4 ms for the planner's bitmap scan); Oslo with a nested loop 2,024 ms (vs 721 ms hash join) | data/runs.txt, parts 2, 3 and 4b (enable_indexscan, enable_bitmapscan, enable_hashjoin, enable_mergejoin set off for that query only) |
| The planner's estimated costs for customer 4242: 132.23 for the bitmap scan plan, 37,739.18 for a forced full scan (total cost of the top Aggregate node) | data/runs.txt, parts 1 and 2 |
| Nested loop for few matching rows, hash join for many | PostgreSQL docs §14.1 (join examples); Momjian, "Explaining the Postgres Query Optimizer"; data/runs.txt, part 4 |
| Statistics are a snapshot refreshed by ANALYZE (and autovacuum); stale statistics can produce bad plans | PostgreSQL docs, ANALYZE and §24.1.3 "Updating Planner Statistics" |
| Stale statistics: estimated 419,506 rows, 10 returned (294 matching), 1,398,620 rows removed by filter, 136.8 ms; after ANALYZE: estimated 327, 7 pages, 0.061 ms | data/runs.txt, parts 5 and 6 (orders_s is a copy of orders with autovacuum off, so its statistics stay stale) |
| Cardinality misestimates are the main cause of bad plans | Leis et al., PVLDB 2015; Lohman, SIGMOD blog (2014) |
| EXPLAIN ANALYZE shows estimated and actual rows per plan node | PostgreSQL docs §14.1 |

## Review log

**Round 1:** expert REVISE, editor REVISE, student retold the question and answer correctly (lost "a few times").
- Expert and editor, blocking: "nothing can make it much faster" was contradicted by the forced index scan two sentences later, and the "one jump per row" picture didn't match the bitmap scan PostgreSQL actually ran. New measurements settled it. Customer 1's rows are on all 12,739 pages of the table (Heap Blocks: exact=12739), so every plan reads every page, and a forced full scan is no faster (135.6 vs 135.4 ms). Customer 4242's are on 10. Chapters 3 and 4 are rebuilt on pages: the index reads only the pages it needs, which PostgreSQL does as a bitmap scan (named in chapter 4, after the mechanism is shown). The disk-versus-memory aside is cut; random versus sequential access is listed as a deviation.
- Measurement: every timing is now the median of seven runs with the data in memory (the queries warm the cache first), so the numbers changed. 15 µs vs 135 ms in the hook; the forced full scan for 4242 is nearly 5,000 times slower; stale statistics 137 ms, after ANALYZE 0.061 ms.
- Expert: the hash table is built from the Oslo customers; the stale-statistics table is named on screen as a copy of orders; "about one point four million rows"; the loop's literal is 4242.
- Editor: the join chapter opens by posing the problem; "cost" is defined aloud (the planner's own units, from the rows and pages it expects to touch); "full scan" is the one narration term (Seq Scan only on screen); chapter 6 says aloud that nobody added an index; the forced nested loop for Oslo (2 s vs 721 ms) now backs "lookups would be slow" with a measurement.
- Student: lost at "jumps" without a mechanism (now pages), the 33-vs-10 estimate (now "close enough to choose well", which sets up chapter 6), the forced-index contradiction (gone) and the unexplained bitmap labels (now explained).

**Round 2:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times"). The expert's list has no BLOCKING item, so by the reviewers' own rule it is a pass: the gate is passed, the should-fix items are applied once, and round 3 decides the lock.
- Expert: "about six hundred thousand"; the query card shows literal values, not `?` (which suggests a prepared statement and PostgreSQL's cached generic plans); the caption says execution time, planning excluded; the recap says a nested loop needs an index to look the matches up; "about a hundred and sixty rows" and "about three hundred and thirty" match the numbers on screen.
- Editor: the "just add an index" instinct is said aloud before chapter 6 knocks it down; the autovacuum caption says why it matters; the unused 1,346-row figure is off the Tromsø card; 4242 is written as digits (spoken "forty-two forty-two") after the numbers are introduced.
- Student: lost at "cost in its own units" (now "a number for comparing plans rather than a time"), at why customer one's rows are on every page (orders are stored as they arrived, not by customer), and at two page numbers back to back (now one follows from the other).

**Round 3 (meant as the final round):** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times"). The gate failed on one blocking item, so it is fixed and round 4 runs.
- Expert, blocking: "the same work whoever the customer is" was contradicted by the video's own forced full scans (72.0 ms for 4242, 135.6 ms for customer 1): the pages are the same, but adding up 600,698 rows costs more than adding up 10. Chapter 3 now says the full scan "reads the same pages whoever the customer is", and chapter 4 says the forced full scan for customer 1 "reads the same pages, and still has six hundred thousand rows to add up".
- Expert: "each once" belongs to the bitmap scan, not to every index, so chapter 3 says only "the pages that hold them" and chapter 4 adds "sort them by page"; the caption says parallel query was off; the hook says "to execute", so the ratio isn't taken for end-to-end latency; "about five" and "about seven hundred" milliseconds; the bitmap scan's two plan nodes are explained ("one reads the index, the other reads the pages").
- Editor: "cost" is paid off with the real costs for customer 4242 (about 130 for the index, about 38,000 for a full scan, in the planner's units); "Heap Blocks (pages)" and "Seq Scan (full scan)" are glossed on screen; "almost all of the hundred thousand" replaces 99,900; chapter 6 says the remaining orders are all at the very end before the 1.4 million.
- Student: lost at "cost" (now shown with numbers) and at the order-number scan in chapter 6 (now explained).

**Round 4:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). The gate holds again after the final round's blocking fix, so the script is locked. Screen-only changes after the lock: "Seq Scan = full scan" beside the Oslo plan, a caption in chapter 5 naming merge join as a third join method not covered (also added to the deviations), and the planner's costs for customer 4242 added to the evidence table. Revision candidates, not applied (final-round SHOULD FIX items):
- Expert: the recap's "a few matches get a nested loop; many get a hash join" reads as if there were only two join methods (merge join is the third); "for each way it could run the query" overstates plan enumeration (the planner prunes).
- Editor: "parallel query off" and "planning excluded" are caption-only, never spoken; "full scan" and Seq Scan are never bridged aloud as "bitmap scan" is.
- Student: lost in the join chapter's cluster of numbers and at the 1.4 million in chapter 6.
