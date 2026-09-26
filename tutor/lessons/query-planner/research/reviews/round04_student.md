## Watching as the reviewer

### 1. Where I'd be confused or lose the thread

- **"data in memory · parallel query off"** — caption only, no narration. I don't know why parallel query being off matters, or whether I should worry that my own database doesn't behave like this.
- **"about a hundred and sixty rows each"** (pages) — first time "page" is used as a storage concept. It's explained well enough to move on, but there's a beat where I'm not sure if "page" is a general DB term or specific to this table.
- **"Its cost for using the index comes to about a hundred and thirty; for a full scan, about thirty-eight thousand."** — I'm told a paragraph earlier that "cost" is "a number for comparing plans rather than a time," which is a good save, but then the specific numbers (130 vs 38,000) don't map onto anything I can sanity-check — I just have to trust the ratio.
- **Chapter 5, back to back:** "That's a nested loop... About five milliseconds." then "That's a hash join. About seven hundred milliseconds, for almost two million rows." then "Force a nested loop for Oslo instead, and it takes two seconds." Three new numbers and two new algorithm names inside about four sentences — this is the spot where I'd lose the thread and have to replay it, because nested loop and hash join both arrive with their own example and their own timing almost simultaneously.
- **"It passes about one point four million other rows first."** — where does 1.4 million come from? I can guess it's "2 million minus something," but the script never derives it, so it lands as a number with no visible arithmetic behind it.
- **"Run ANALYZE, which refreshes the statistics"** — fine as a definition, but this is also the first time I hear that statistics can go stale *silently* (nobody has to break anything for this to happen), and that lands quickly right before a 2000x number, so I absorb the number better than the mechanism.

### 2. Questions I'd ask afterward

- How does the planner actually compute "cost" — is it purely page-count-based, or does it factor in CPU work too?
- How often does ANALYZE run automatically in a real production database, and how would I notice it hasn't run recently?
- For the Oslo/Tromsø example, how does the planner decide the *cutoff* between "few enough rows for a nested loop" and "too many, use a hash join"? Is there a threshold I could look up?
- If EXPLAIN ANALYZE shows estimated vs. actual rows are far apart, what do I actually type to fix it — is it always just `ANALYZE tablename`, or are there cases where that's not enough?
- Does this generalize to other databases (MySQL, etc.) or is this all PostgreSQL-specific behavior?

### 3. What I learned (written without looking back, ~150 words)

The same SQL query can run in microseconds or milliseconds depending on which customer you filter by, because SQL just says *what* you want, not *how* to get it — a component called the query planner decides how, every time. It picks between a full table scan (read every page) and using an index (jump straight to the relevant pages), based on estimates of how many rows will match, drawn from statistics it keeps about the table. If very few rows match, the index wins by a huge margin; if a large fraction of rows match, every page has to be touched regardless of plan, so the index doesn't help. The same logic extends to joining two tables — a nested loop when few rows match, a hash join when many do. When the planner's statistics are stale (out of date with the real data), it can pick a badly wrong plan; running ANALYZE refreshes the stats and can fix a slow query without adding any index at all.

### 4. Direct answers

- **One main idea:** SQL only specifies *what* to retrieve, so a query planner has to decide *how* to execute it, choosing a strategy based on estimated row counts — and that choice, not the query text, is what determines whether it's fast or slow.
- **Numbers I remember and what they mean:** 15 microseconds vs. 135 milliseconds — same query, rare customer vs. common customer; "nearly five thousand times slower" for forcing a full scan on the rare customer; 2,000,000 orders across ~12,700 pages; the 60-microsecond-vs-137-millisecond pair (over 2000x) from the stale-statistics example, fixed by running ANALYZE.
- **Starting question / answer:** "Who decides how a query runs, and why is the same query sometimes fast and sometimes slow?" Answer: the query planner decides, weighing possible execution strategies by estimated rows/pages touched using table statistics — so speed depends on how many rows actually match and how accurate the planner's statistics are.

### 5. Ratings

- **Pull of the opening (1–5):** 4 — a 9000x gap between two runs of the *identical* query on the *same* data is a genuinely surprising hook, and "who decides?" is a question I want answered.
- **How often I felt lost:** a few times — mainly the cluster of new numbers/algorithms in the join section, and the ungrounded "1.4 million rows" figure in the stale-statistics section.
