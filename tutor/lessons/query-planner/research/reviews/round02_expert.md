I reviewed the script line by line against the evidence table and standard references (Selinger 1979, PostgreSQL docs, DDIA, Use The Index Luke, Leis et al. 2015). The arithmetic all checks out (9,000x, 4,800x, 2,240x, etc. all verified), and the technical mechanics (bitmap scan, hash join build/probe side, nested loop, ANALYZE staleness) are canonical and internally consistent with the cited runs. Findings below.

## Findings

**SHOULD FIX** — Chapter 3
> "Customer one has six hundred thousand orders, and they're spread over every page of the table."

Stated as if exact; actual is 600,698 (evidence). Every other approximate figure in the script ("about twelve thousand seven hundred pages," "about a hundred and fifty rows") is hedged with "about." This one isn't, which reads as a precise count rather than a rounding and breaks the script's own convention.
Fix: "Customer one has about six hundred thousand orders, and..."

**SHOULD FIX** — Chapter 2
> "That leaves the database free to choose how. And it has to choose, every time the query runs."

The screen shows the query with a `?` placeholder, which visually signals a prepared/parameterized statement. For a genuinely reused prepared statement, PostgreSQL switches from a per-execution custom plan to a cached generic plan after five executions (if the generic plan's estimated cost is competitive) — at that point it does *not* replan, and does not necessarily pick a different plan per customer, which is in tension with the video's central claim. Since chapter 4 later shows different plans for different customers, a sharp viewer could ask "wait, doesn't PostgreSQL cache the plan?" The `?` is presumably just shorthand for "whichever customer" and the runs were literal-value EXPLAIN ANALYZE, not a single reused PREPARE — but the script never says so.
Fix: either replace `?` with a literal placeholder that doesn't suggest a prepared statement (e.g. `customer_id = 4242`), or add one clause: "...and it has to choose, each time it plans the query" plus a caption note that each run substitutes a literal value.

**SHOULD FIX** — Chapter 7
> "A few matches get a nested loop; many get a hash join."

This states row count as the sole determinant. In reality a nested loop is only competitive when there's a usable index on the inner side's join key (which is exactly what makes chapter 5's Tromsø case work) — with no such index, few matches would still make nested loop disastrous. The sentence, standing as the lesson's takeaway, overgeneralizes past what was actually shown.
Fix: "A few matches, with an index to look them up, get a nested loop; many get a hash join."

**SHOULD FIX** — Chapter 1 screen direction
> "customer 4242 → 0.015 ms" and "customer 1 → 135.4 ms" ... "median of 7 runs"

At the 15-microsecond scale, planning time can be comparable to or larger than execution time, and EXPLAIN ANALYZE reports them separately. Nothing in the script or caption says whether the quoted numbers are execution time alone or include planning. This matters most exactly where the video's punchline number is smallest and most impressive.
Fix: add to the caption, e.g., "execution time (EXPLAIN ANALYZE), planning time excluded."

**NIT** — Chapter 3
> "blocks of about a hundred and fifty rows each"

2,000,000 / 12,739 ≈ 157, which the on-screen caption correctly shows ("~157 rows each"). "About a hundred and fifty" is a defensible round-to-nearest-50, but it sits oddly next to the more precise caption on the same beat. Consider "about a hundred and sixty" for tighter agreement with what's on screen.

**NIT** — Chapter 4
> "The planner estimates about six hundred thousand rows, and picks the same kind of bitmap scan."

The actual estimate is 591,533, and actual matches are 600,698 (evidence part 1). For customer 4242 the script explicitly contrasts estimate vs. real ("estimates thirty-three; the real number is ten") — doing the same here would reinforce, rather than blur, the point that this estimate happens to be a good one (setting up the contrast with chapter 6's bad estimate). As written it just says "about six hundred thousand" once, losing that parallel.

**NIT** — Chapter 6
> "the planner now expects about three hundred rows"

Estimate is 327 (evidence part 6). "About three hundred" is defensible rounding to the nearest hundred but is looser than everywhere else in this chapter, which quotes fairly precise figures (294, 1.4 million, 137 ms, 60 microseconds). "About three hundred thirty" would match the chapter's own precision level.

**NIT** — Chapter 5
> "Seven hundred milliseconds, for almost two million rows."

Actual is 721 ms. Fine as a rounding, just flagging for consistency with the otherwise fairly tight numbers used elsewhere in this chapter.

## What's not a problem (checked and correct)
- All ratios/arithmetic (≈9,027x, ≈4,800x, ≈2.8x, ≈2,243x) are correct.
- Bitmap scan mechanics ("collect locations, read each page once") match PostgreSQL's own documentation language.
- Hash join described correctly as building the table from the smaller side (Oslo customers, 99,900) and streaming the larger side (orders, 2M) through it once.
- The stale-statistics story in chapter 6 is internally consistent down to the numbers: the scan having to pass ~1.4M rows lines up with customer 1's remaining (recent, high-order_id) rows being archival survivors, not an arbitrary flourish.
- Citations (Selinger 1979 SIGMOD, PostgreSQL docs §14.1/§14.2, Kleppmann DDIA ch. 2, Winand, Leis et al. PVLDB 2015) are all real, correctly attributed, and on-topic.
- No claim overstates the planner as finding a truly optimal plan — language stays correctly scoped to "estimates" and "cheapest by its own cost model," never "fastest possible."

VERDICT: REVISE
