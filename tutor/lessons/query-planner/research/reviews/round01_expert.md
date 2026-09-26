# Review

## BLOCKING

**1. Self-contradiction: "nothing can make it much faster" is refuted two sentences later**

Quote (Ch. 4): *"It takes a hundred and fifty milliseconds, and nothing can make it much faster: six hundred thousand rows have to be read."*

Quote (Ch. 4, same section, next paragraph): *"a plain index scan for customer one, forced by hand, actually ran a little faster than the planner's plan"* (112.7 ms vs. 151.3 ms — a 25% improvement, per the screen data).

This is an internal contradiction, not just an overstatement: the script asserts no plan can meaningfully beat 151.3 ms, then immediately presents a plan (forced plain Index Scan) that beats it. "Nothing can make it much faster" is also not something a professor would want stated as a general truth — the demo explicitly runs with parallel workers disabled and no covering index, so the 150 ms figure reflects one plan under one configuration, not an inherent floor. A parallel seq/bitmap scan, an index-only scan (covering index on `(customer_id) INCLUDE (amount)`), or a maintained per-customer summary table could all cut it further.

**Fix:** Drop the absolute claim. E.g., *"It takes a hundred and fifty milliseconds: for this plan, all six hundred thousand rows have to be examined."* Let the next paragraph's finding (forced index scan beats the planner's own choice) stand as the actual point about non-optimality, without contradicting a claim you made moments earlier.

**2. The "two ways" model and the "jump per row" visual don't match the actual plan shown on screen**

Quote (Ch. 3): *"each row fetched through the index costs a jump to wherever that row happens to be stored… For hundreds of thousands, the jumps add up"* — with the on-screen visual showing **600,698 individual arrows**, one per matching row for customer 1.

But the plan actually run for customer 1 (Ch. 4 screen note) is a **Bitmap Heap Scan**, not a plain per-row Index Scan. A Bitmap Heap Scan's entire purpose is to sort matching TIDs by physical page location and visit each heap page once, regardless of how many matching rows it holds — that's precisely what distinguishes it from the naive "index scan" model described in Ch. 3. At 30% selectivity, most pages hold several matches each, so the real number of page visits is a small fraction of 600,698 (roughly the page count, not the row count). The chapter never names Bitmap Index/Heap Scan at all, despite it appearing twice on screen (Ch. 4's two plan trees), so viewers who run `EXPLAIN` themselves will see a node type the narration gave them no model for — and the model they were given (one jump per row) actively overstates that node's cost mechanism.

**Fix:** Either (a) name Bitmap Index/Heap Scan explicitly and describe it as a third, hybrid strategy — "the planner marks the matching rows first, then visits each page holding a match once" — with a visual of arrows-per-page rather than arrows-per-row, or (b) if keeping the simple two-way model, pick example queries whose real plans are plain Index Scan / Seq Scan (not Bitmap variants) so the taught model matches the evidence actually shown.

## SHOULD FIX

**3. "Five hundred times" understates the measured ratio by ~8%**

Quotes: *"it takes eighty-four milliseconds instead of a sixth of one: five hundred times slower"* and *"the estimate points the right way by a factor of five hundred."*

84.3 ⁄ 0.156 ≈ 540, not 500. The rest of the script is careful with directional qualifiers where a number is rounded ("nearly a thousand times," "more than a thousand times faster") — this is the one place a rounded number is stated flatly and in the wrong direction (down, when the true value is higher).

**Fix:** *"…roughly 540 times slower"* / *"…by a factor of over five hundred."*

**4. Hash join build side misdescribed**

Quote (Ch. 5): *"the planner builds a lookup table from all the customers, and streams all two million orders through it, once."*

Per the screen data, the `Hash` node is built from `Seq Scan on customers` **after** the Oslo filter (99,900 rows), not from all 100,000 customers. This matters especially here because the whole point of the chapter is that plan choice tracks how many rows match — saying the hash table is built from "all the customers" undercuts that exact point, even though the two figures happen to be numerically close in this example.

**Fix:** *"builds a lookup table from the matching (Oslo) customers."*

**5. Chapter 6 may silently switch tables**

The on-screen plan nodes use `orders_s_pkey` / `orders_s_customer_id_idx`, not the `orders` table's usual index names used in chapters 1–5, and the row count implied by "almost one and a half million rows" scanned (with customer 1 still at ~30% per stale stats) is consistent with a table smaller than the 2,000,000-row `orders` table used earlier. If `orders_s` is in fact a separate demo table (as the evidence table's parenthetical — "autovacuum off on the demo table" — suggests), the narration *"Here's what happens when the data changes after the snapshot"* implies continuity with the same dataset from Chapter 1 that isn't actually there.

**Fix:** Either confirm on screen this is a distinct table set up to hold stale statistics, or use the same `orders` table throughout so the row counts are traceable across chapters.

**6. Rounding overstates the scanned-row count**

Quote: *"reads through almost one and a half million rows before it finds them"* against an evidenced *"Rows Removed by Filter ≈ 1.4 million."*

"Almost one and a half million" reads as closer to 1.45–1.49M; the evidence says ≈1.4M.

**Fix:** *"reads through about 1.4 million rows"* or *"close to a million and a half"* only if the underlying figure actually rounds that way.

## NIT

**7.** The pseudocode `for order in orders: if order.customer_id == 42: …` uses customer **42**, while the actual example used throughout the video is customer **4242**. Change the literal to `4242` for consistency.

**8.** *"A hundred thousand separate lookups would be slow"* rounds the just-stated 99,900 up to 100,000 in the very next sentence. Negligible numerically, but reads as sloppy right after citing the precise figure — consider keeping "ninety-nine thousand, nine hundred."

---

VERDICT: REVISE
