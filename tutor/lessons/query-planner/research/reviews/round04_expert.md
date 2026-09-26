Reviewed the script and cross-checked every number against the evidence table (arithmetic, rounding, terminology, and canonical sources). It's unusually careful — I did not find anything actually wrong. My objections are all missing caveats/precision, not errors.

## Findings

**SHOULD FIX** — Join methods presented as an exhaustive binary choice.
> "A few matches, with an index to look them up, get a nested loop; many get a hash join."

This is the video's stated general takeaway, but PostgreSQL has a third canonical join strategy, merge join, which every standard reference (including the cited Selinger 1979 paper and PG §14.1) treats as one of the three basic algorithms. The evidence table itself shows `enable_mergejoin` was explicitly toggled off when forcing the nested-loop plan for Oslo — meaning merge join was a live candidate the planner actually considered and rejected, not a hypothetical. Leaving it out entirely, in the segment framed as "the answer," risks teaching an incomplete taxonomy.
Corrected wording: add a half-sentence acknowledging it, e.g. "...many get a hash join — or, when both sides are already sorted, a merge join, PostgreSQL's third join strategy, which this lesson doesn't cover."

**NIT** — Overgeneralized description of plan enumeration.
> "For each way it could run the query, it estimates the rows and pages it would touch, turns that into a cost... and picks the cheapest."

True for every example actually shown (single table, two-way joins), but stated as a description of "the planner" in general. Above PostgreSQL's `geqo_threshold` (default 12 relations), the planner switches to a genetic algorithm and does not enumerate every join order. Since the video never exceeds two tables, this doesn't corrupt anything it shows, but a viewer could over-extend the claim. Low priority — could add "(for the small number of tables here)" if there's room, but not required.

**NIT** — Index entries described as one-per-customer rather than one-per-row.
> "a sorted list of customer numbers, each pointing to where that customer's rows are"

A non-unique B-tree has one entry per row (duplicate keys repeated), not one entry per distinct key value fanning out to multiple locations. The follow-up sentence ("collect where their rows are") correctly implies gathering multiple entries, so the mental model recovers itself, and this phrasing matches the canonical Winand-style "book index" analogy used in the cited source. Flagging only for precision, not correctness.

**NIT** — Same rounded phrase used for two different numbers.
> "The planner estimates about six hundred thousand rows" (591,533) vs. earlier "Customer one has about six hundred thousand orders" (600,698)

These are legitimately different quantities (estimate vs. actual) that happen to round to the same phrase. Harmless here since the numbers are close, but chapter 6's entire point is that estimate-vs-actual gaps are the diagnostic signal — so a slightly sharper phrasing here (e.g., "the planner estimates close to six hundred thousand — not far from the true count") would reinforce rather than blur that theme.

## Everything else checks out
All ratios (≈9000×, ≈4800×, >2000×, ≈2.8×), all page/row counts (12,739 pages, ~157 rows/page, 10 vs. 12,739 heap blocks, 33 vs. 10, 419,506 vs. 10/294, 327 vs. 294), all costs (132 vs. 37,739), and all timing figures match `data/runs.txt` exactly under reasonable spoken rounding. The declarative/imperative framing, cost-as-relative-not-time framing, bitmap-scan mechanics, and the "add an index" red herring in chapter 6 are all precisely stated and correctly cited (Selinger 1979, Kleppmann ch. 2, PG §14.1/§14.2, Winand, Leis et al. 2015 — titles, venues, and years all correct). The video also avoids the common trap of overstating optimality (it correctly frames the planner as picking cheapest *estimated* cost, not the actual fastest plan) and appropriately scopes its claims to the stated environment (PG 16.9, in-memory, parallel query off, literals not bind parameters).

VERDICT: PASS
