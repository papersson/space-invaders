You are this particular viewer:

Background

- Works in industry and wants lessons "useful in the industry day to day". Picked queueing, tail latency, and idempotency with retries from a list of practical topics.
- Keeps a personal library of prompts and references on software architecture, data systems, performance, observability and LLM agents. Likely a software, data or ML engineer. Their exact role and years of experience are unknown.
- Has watched two lessons in this series: UMAP (an earlier session) and external merge sort (version 2, 6:25).
- Assume they know: programming, how web services, APIs and databases are built and called, averages and percentiles as everyday terms, Big-O.
- Unknown: how comfortable they are with probability beyond the everyday (distributions, independence, expected value), and how much formula they want on screen.


Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.


 You have not studied this topic. Stay in role: if the script does not explain something, you do not know it. Below is the script of a short narrated video, with a note of what is on screen at each moment. Go through it once, in order, as if watching. (1) List every point where you would be confused or lose the thread, quoting the line: a term used before it is explained, a step that does not follow, a number with no meaning attached, a sentence hard to follow when heard. (2) List the questions you would ask afterwards. (3) Without looking back, write what you learned in about 150 words. (4) Answer: what is the one main idea; which numbers do you remember and what do they mean; what question did the video start with, and what was its answer? (5) Rate how much the opening made you want the answer (1-5) and how often you felt lost (never / once / a few times / often).


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a table of two million orders, and one query: count a customer's orders, and add up the amounts.
> For customer four thousand two hundred and forty-two, it takes about a sixth of a millisecond.
> For customer one, it takes a hundred and fifty milliseconds. Nearly a thousand times longer.
> Same query, same table, same machine. And nothing in the query says how to run it.
> So who decides? And why is the same query sometimes fast, and sometimes slow?

*Screen:* the query in a code card: `SELECT count(*), sum(amount) FROM orders WHERE customer_id = ?`. Two runs from data/runs.txt: "customer 4242 → 0.156 ms" and "customer 1 → 151.3 ms", with a bar of each (log scale noted). Caption: "PostgreSQL 16.9, 2,000,000 orders". The question.

### 2. Say what, not how

> In ordinary code, you'd write the search yourself: loop over every order, and keep the ones for this customer. The code says exactly how.
> SQL is declarative. The query says what rows you want, and nothing about how to find them.
> That leaves the database free to choose how. And it has to choose, every time the query runs.

*Screen:* a loop in code: `for order in orders: if order.customer_id == 42: …` beside the SQL card. The loop's steps light up one by one ("how"); the SQL's WHERE clause lights up alone ("what"). A small "?" over the gap between the SQL and the data: "how?".

### 3. Two ways to find the rows

> There are two basic ways to find one customer's orders.
> One is a full scan: read every row of the table, and keep the ones that match. For two million rows, that takes the same time whoever the customer is.
> The other is an index: a sorted list of customer numbers, each pointing to where that customer's orders are stored. Find the customer in the sorted list, then fetch just those rows.
> Looking up ten rows through the index is almost free. But each row fetched through the index costs a jump to wherever that row happens to be stored. For a handful of rows, that's nothing. For hundreds of thousands, the jumps add up, and reading the whole table in order can be cheaper.
> So which way is faster depends on how many rows match. And that depends on the customer.

*Screen:* the table as a strip of pages, each holding rows. A scan sweeps left to right over all pages (a counter "2,000,000 rows read"). Then an index: a sorted column of customer numbers on the left with arrows into scattered pages; customer 4242's ten arrows land on ten pages. Then customer 1: 600,698 arrows spraying across every page ("a jump per row").

### 4. The planner estimates

> This choice is made by the query planner.
> The planner keeps statistics about each table: how many rows it has, and for each column, which values are most common, and how common.
> Its statistics say customer four thousand two hundred and forty-two is rare. It estimates thirty-three rows, looks them up in the index, and finds ten. A sixth of a millisecond.
> For customer one, the statistics say about three in ten orders. The planner estimates about six hundred thousand rows, and picks a plan that reads them in the order they're stored on disk. It takes a hundred and fifty milliseconds, and nothing can make it much faster: six hundred thousand rows have to be read.
> The choice matters. Force a full scan for the rare customer, and it takes eighty-four milliseconds instead of a sixth of one: five hundred times slower.
> The planner decides by estimated cost, not by the clock. Its costs assume data read from disk. Here, everything is in memory, and a plain index scan for customer one, forced by hand, actually ran a little faster than the planner's plan. For the rare customer, the estimate points the right way by a factor of five hundred.

*Screen:* a statistics card for orders.customer_id: "customer 1: ~30% of rows (most common value)"; "others: ~20 rows each". Then two real plans from data/runs.txt, as small trees: (a) customer 4242: `Bitmap Index Scan on orders_customer` → `Bitmap Heap Scan`, "estimated 33 rows · actual 10 · 0.156 ms"; (b) customer 1: `Bitmap Heap Scan`, "estimated 594,067 · actual 600,698 · 151.3 ms". Then the forced alternatives: "customer 4242, full scan forced: 84.3 ms" (coral), "customer 1, index scan forced: 112.7 ms". A caption: "cost is an estimate in abstract units, tuned for disk".

### 5. Joins

> With more than one table, the planner has more to choose: which table to read first, and how to match rows between them.
> Say we want the orders of customers in Tromsø. A hundred customers live there, out of a hundred thousand.
> The planner finds those hundred customers, then, for each one, looks up its orders in the index. That's a nested loop: for each row on one side, look up its matches on the other. Ten milliseconds.
> Now ask for customers in Oslo: ninety-nine thousand nine hundred of them. A hundred thousand separate lookups would be slow. So the planner builds a lookup table from all the customers, and streams all two million orders through it, once. That's a hash join. Seven hundred milliseconds, for almost two million rows.
> Same query shape. A different plan, because a different number of rows match.

*Screen:* two plans from data/runs.txt side by side. Tromsø: `Nested Loop` over `Seq Scan on customers (100 rows)` and `Bitmap Heap Scan on orders` per customer (100 loops, 13 rows each), "1,346 rows · 10.2 ms". Oslo: `Hash Join` of `Seq Scan on orders (2,000,000)` with `Hash` of `Seq Scan on customers (99,900)`, "1,998,654 rows · 722 ms". An animation of each: 100 small index lookups vs one hash table and a stream.

### 6. When the estimate is wrong

> The plan is only as good as the estimate, and the statistics are a snapshot.
> Here's what happens when the data changes after the snapshot. When the statistics were gathered, customer one had three in ten orders. Since then, their older orders were archived, and just two hundred and ninety-four are left, all of them recent.
> Now ask for customer one's first ten orders, by order number.
> The planner still believes customer one is everywhere, about four hundred and twenty thousand rows. So it walks through all orders by order number, expecting to hit ten of customer one's almost at once. Instead it reads through almost one and a half million rows before it finds them. A hundred and ninety-four milliseconds.
> Run ANALYZE, which refreshes the statistics, and the planner now expects fifteen rows. It looks them up in the index, sorts them, and takes the first ten. A tenth of a millisecond: more than a thousand times faster, for the same query.
> That's how to read a slow plan. EXPLAIN ANALYZE shows, for each step, the rows the planner expected and the rows it actually got. Where the two are far apart, the plan was chosen for data that isn't there.

*Screen:* data/runs.txt, part 5: `Limit` → `Index Scan using orders_s_pkey`, "estimated 420,532 rows · actual 10 · Rows Removed by Filter ≈ 1.4 million · 193.5 ms" (coral). A scan arrow crawling down the primary key past almost everything. Then `ANALYZE orders_s;` and part 6: `Limit` → `Sort (top-N)` → `Bitmap Heap Scan` via `orders_s_customer_id_idx`, "estimated 15 · actual 294 · 0.112 ms" (ICE). Then an EXPLAIN ANALYZE line with "rows=420532" and "actual … rows=10" circled side by side: "estimate vs reality".

### 7. The answer

> So who decides how a query runs? The query planner, because SQL only says what you want.
> It weighs the ways it could run the query by how many rows each step will touch, using statistics about your data. A rare customer gets an index lookup; a common one, a big sequential read. A few matches get a nested loop; many get a hash join.
> That's why the same query can be fast or slow: it depends on the data it touches, and on what the planner believes about that data.
> When a query is slow, don't guess, and don't just add an index. Run EXPLAIN ANALYZE, and compare the rows the planner expected with the rows it got.

*Screen:* the two cards from chapter 1 again (0.156 ms, 151.3 ms) with their plans underneath. Three lines: "rare → index lookup", "common → read in order", "stale statistics → wrong plan → ANALYZE". An EXPLAIN ANALYZE line with its estimated and actual rows highlighted. End card with the takeaway and references: Selinger et al., "Access Path Selection in a Relational Database Management System", SIGMOD (1979); PostgreSQL documentation, §14.1 "Using EXPLAIN" and §14.2 "Statistics Used by the Planner"; Kleppmann, Designing Data-Intensive Applications (2017), ch. 2; Winand, Use The Index, Luke; Leis et al., "How Good Are Query Optimizers, Really?", PVLDB (2015).

