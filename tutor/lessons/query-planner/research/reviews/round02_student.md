# Watching as the student reviewer

## 1. Points where I lost the thread (quoting the line)

- **"SQL is declarative. The query says what rows you want, and nothing about how to find them."** — the word "declarative" itself is never defined, just illustrated by contrast with the loop. I could follow it from context, but if I didn't already know the term I'd be stuck on the label even though the *idea* landed fine.

- **"The table is stored in pages, blocks of about a hundred and fifty rows each. This one has about twelve thousand seven hundred pages."** — two new numbers back to back (150 rows/page, 12,700 pages) right after a brand-new term ("pages"). I had to pause and do the multiplication myself to believe the second number followed from the first.

- **"Customer one has six hundred thousand orders, and they're spread over every page of the table."** — this is asserted, not explained. Why would one customer's rows land on *every* page instead of being clustered together? I'm guessing it's because rows are stored in insertion/order-number order rather than by customer, but the script never says that, so this felt like a fact dropped on me rather than a conclusion I could reach.

- **"For each way it could run the query, it estimates the rows and pages it would touch, turns that into a cost in its own units, and picks the cheapest."** — "cost in its own units" is a phrase with no meaning attached. Units of what? Time? An abstract number? It's never tied back to the millisecond numbers we actually see, so it feels like a hand-wave at the one moment I most wanted a concrete mechanism.

- **"The planner still believes customer one is everywhere: about four hundred and twenty thousand rows. So it walks through the orders by order number, expecting to run into ten of theirs almost at once."** — this is the densest step in the video. I had to reconstruct, unprompted, that the query must be sorted by order number with a limit, and that "believes customer one is everywhere" is *why* scanning in that order seemed cheap. It's two inferences stacked in one sentence, and I only barely kept up.

- On screen, "**Heap Blocks: 10**" and "**Bitmap Index Scan → Bitmap Heap Scan**" appear as two separate steps, but the narration only ever says "bitmap scan" as one thing. If I'd been watching closely I'd have wondered why there are two boxes for one concept.

## 2. Questions I'd ask afterward

- What are the planner's "cost units" actually measured in — is it estimated time, estimated I/O operations, something else? How do I know if a cost number is "high"?
- Why does a common customer's rows end up scattered across every page instead of stored together? Is that just how tables usually work, or specific to this example?
- In the stale-statistics example, what exactly was the query? I inferred `ORDER BY order_number LIMIT 10` but it was never spelled out.
- Bitmap Index Scan vs Bitmap Heap Scan — is that a meaningful distinction I should know, or just internal naming I can ignore?
- How often should I be running ANALYZE in a real system — is this a manual thing I need to remember, or does Postgres do it automatically most of the time?

## 3. What I learned (written without looking back, ~150 words)

A database query doesn't say *how* to run itself — SQL just says what rows you want, and something called the query planner decides the actual strategy every time the query runs. It does this using statistics about the table: how many rows, which values are common or rare. If you're asking for a rare value, the planner can use an index and only touch a handful of pages, so the query is extremely fast. If you're asking for a value that's common — spread across most of the table — an index doesn't help, because you basically have to read everything anyway, and the query is slow no matter what plan is chosen. The same logic applies when joining two tables: a few matches favor looking things up one at a time, many matches favor building a lookup structure and streaming through everything once. The other big risk is that the statistics can go stale — if the data changes, the planner can pick a bad plan even though a good index exists, because it doesn't know the world has changed. Refreshing the statistics fixes this instantly. The tool for diagnosing all of this is something called EXPLAIN ANALYZE, which shows what the planner *expected* versus what actually happened.

## 4. Direct answers

- **One main idea:** the query planner — not the query text, not the table structure alone — decides how a query executes, by estimating how many rows/pages each possible plan would touch using statistics, and picking the cheapest; the same query is fast or slow depending on how common the matched value is and how accurate those statistics are.
- **Numbers I remember:** 15 microseconds vs. 135 milliseconds for the same query (~9000x difference) depending on which customer; ~12,700 pages in the full table but only 10 pages needed for a rare customer; forcing a full scan for the rare customer costs 72ms (~5000x slower than the index path); a hash join for a common value (Oslo) took 700ms vs. 2 seconds if forced into a nested loop; and after stale statistics were refreshed with ANALYZE, a query went from 137ms to about 60 microseconds — a 2000x speedup with no new index.
- **Starting question / answer:** "Who decides how a query runs, and why is the same query sometimes fast and sometimes slow?" Answer: the query planner decides, based on estimated row/page counts from table statistics — it's fast when the matched value is rare (index, few pages) and slow when the value is common (every page must be read regardless) or when the statistics are outdated and mislead the planner into the wrong strategy.

## 5. Ratings

- **Hook strength (want-the-answer):** 4/5 — "same query, same table, same machine, ~9000x difference" is a genuinely compelling mystery with a concrete, unexplained number right up front.
- **How often I felt lost:** a few times — mainly at "cost in its own units," the unexplained claim that customer 1's rows are scattered across every page, and the compressed reasoning in the stale-statistics example.
