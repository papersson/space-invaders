## 1. Points where I'd lose the thread

- **"turns that into a cost, a number for comparing plans rather than a time, and picks the cheapest."** — Three new ideas land in one sentence: estimate rows/pages, convert to a "cost," then pick cheapest. I don't know what a cost actually *is* (dollars? abstract units? milliseconds-ish?) or how rows-and-pages becomes a single number. It's waved off as "not a time" but never replaced with anything concrete.

- **"PostgreSQL calls that a bitmap scan."** — A label gets dropped onto a mechanism I'd just watched (collect locations, read each page once). Fine as naming, but I don't know if "bitmap" means anything I should track later, or if it's just trivia.

- **"the planner builds a lookup table from the Oslo customers, and streams all two million orders through it, once. That's a hash join."** — Called a "lookup table" first, then relabeled "hash join." Why hash specifically? Is a lookup table the same thing as a hash table? The name arrives disconnected from the description.

- **"So it walks through the orders by order number, expecting to run into ten of theirs almost at once."** — This is where I actually lost the thread. Nothing earlier told me the query cares about order number at all — I thought the query was just "find customer one's orders." Suddenly the scan is organized by a completely different axis (order number, not customer), and I can't reconstruct why that's the relevant way to search. This confusion carries into the next line too: **"Instead it passes about one point four million other rows before it finds them."** I believe the number, but not the setup.

- **"blocks of about a hundred and sixty rows each. Two million orders fill about twelve thousand seven hundred of them."** — 2,000,000 / 160 doesn't land near 12,700 (it's closer to 12,500). Small thing, but when a video invites me to do the mental arithmetic, a mismatch makes me doubt the round numbers instead of trusting them.

## 2. Questions I'd ask afterward

- What is "cost" actually measured in, and how do estimated rows/pages turn into that number?
- Why did the "customer one, first ten orders" query get scanned by *order number* — what in the request made order number the relevant axis instead of customer id?
- What makes a join a "hash" join specifically — is the "lookup table" a hash table, and if so what's different about that from the sorted list used for the index?
- Is there a rule of thumb for when the planner switches from nested loop to hash join, or is it purely cost-estimate-driven with no simple cutoff?
- Do I need to run ANALYZE manually on a schedule, or does the database normally keep statistics fresh on its own (the on-screen note about autovacuum being off wasn't said aloud)?

## 3. What I learned (written without looking back, ~150 words)

A SQL query doesn't say how to run itself — the database's query planner decides, and it can decide differently for the exact same query depending on which values you ask for. It keeps statistics on how common each value in a column is, and uses that to guess how many rows/pages a plan would touch, then picks a plan based on that guess. If a value is rare, it uses an index and only reads a handful of pages — fast. If a value is common, basically every page has data for it anyway, so an index doesn't help and nothing is fast. Joins work the same way: few matching rows get looked up one at a time (nested loop), lots of matching rows get funneled through a lookup table built once (hash join). The statistics can go stale, though — if the real data has shifted, the planner's guess is wrong and it picks a bad plan. You check for that mismatch with EXPLAIN ANALYZE, comparing expected vs. actual rows, and fix it with ANALYZE — not by blindly adding an index.

## 4. Direct answers

- **One main idea:** the query planner picks a plan based on estimated row/page counts from statistics, not on what the query "says" — so the same query's speed depends entirely on the data it touches and how well the planner's guess matches reality.
- **Numbers I remember:** ~15 microseconds vs. ~135 milliseconds for the same query on different customers (~9000x); 10 pages read out of ~12,700 total for the rare customer; and the ANALYZE fix taking a query from ~137ms down to ~60 microseconds (2000x) just by refreshing statistics, no new index.
- **Question the video started with:** why does the same query, on the same table and machine, sometimes take microseconds and sometimes take 100+ milliseconds — who decides how it runs? **Answer:** the query planner decides, using row-count statistics and estimated cost, and it can be fast, slow, or *wrong* depending on how well its statistics reflect the actual data.

## 5. Ratings

- **Want-the-answer pull from the opening:** 4/5 — the 9000x gap on an identical query with just a different literal value is a genuinely surprising hook.
- **How often I felt lost:** a few times — mainly the "cost" black box and the order-number scan in chapter 6, which arrived without enough setup to follow the mechanism.
