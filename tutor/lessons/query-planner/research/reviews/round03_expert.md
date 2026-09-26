# Review

## BLOCKING

**Quote (Ch. 3):** *"One is a full scan: read every page, and keep the rows that match. That's the same work whoever the customer is."*

**Problem:** This is contradicted by the video's own numbers two chapters later. Forcing a full scan gives **72.0 ms** for customer 4242 but **135.6 ms** for customer 1 — a ~1.9× difference, for scans of the *same* 12,739 pages on the *same* table. The claim as stated ("same work") is false: page I/O is customer-independent, but the aggregation (`count`/`sum`) is not — summing ~600,698 matching rows costs meaningfully more CPU than summing 10. Nothing later in the script reconciles this, so an attentive viewer who remembers "same work whoever the customer is" and then sees 72 ms vs. 135.6 ms will reasonably conclude the video contradicted itself.

**Fix:** Narrow the claim to what's actually invariant — the pages touched, not total work, e.g.: *"One is a full scan: read every page, and keep the rows that match. It touches the same pages whoever the customer is — though tallying more matches then costs a little more too, as we'll see."* This also sets up rather than undercuts the later 72 ms vs. 135.6 ms comparison.

## SHOULD FIX

**Quote (Ch. 3):** *"Find the customer in the list, collect where their rows are, and read only those pages, each once."*

**Problem:** Stated as a general property of "an index," but reading each qualifying page exactly once is specifically what a **bitmap heap scan** guarantees (it sorts collected TIDs into physical order before reading). A plain (non-bitmap) Index Scan visits heap pages in index-key order and can revisit the same page more than once if matches aren't physically clustered. Since Ch. 4 later names "bitmap scan" as the specific mechanism producing exactly this behavior, Ch. 3 is quietly describing that mechanism before naming it — fine as foreshadowing, but as written it reads as a universal fact about indexes, which it isn't.

**Fix:** Either soften ("...and, since PostgreSQL sorts those locations first, read each needed page only once") or defer the "each once" guarantee explicitly to Ch. 4's bitmap-scan reveal.

---

**Missing caveat:** All timings were measured with parallel query workers disabled ("parallel workers off for readable plans" — per the evidence table), but this is never disclosed on screen or in narration (the Ch. 1 caption lists version, row count, in-memory data, and "planning excluded," but not this). A viewer who reproduces the full-scan numbers on a stock, modern PostgreSQL install (parallel seq scan on by default for a 2M-row table) could get a substantially faster full scan and conclude the video's comparisons don't hold.

**Fix:** Add "parallel query off" to the Ch. 1 caption alongside the other methodology notes.

---

**Quote (Ch. 1 caption):** *"execution time (planning excluded), median of 7 runs"*

**Problem:** This caveat is only ever shown visually, never spoken, yet the entire hook of the video — "about nine thousand times longer" — depends on it. For a query this fast (15 µs execution), planning time for a literal-value, non-prepared statement is not obviously negligible next to execution time; excluding it is defensible for isolating the planner's *choice*, but the headline ratio is specifically an execution-time ratio, not an ratio of what a client would actually observe end-to-end. Leaving this only in small on-screen print risks the "nine thousand times" number being remembered as real-world latency.

**Fix:** Have the narration say it once, e.g. in Ch. 1: *"...fifteen microseconds to execute, not counting planning..."*, so the scope of the claim survives even for a listener not reading the caption.

## NIT

**Quote (Ch. 5):** *"Seven hundred milliseconds, for almost two million rows."*

Actual value is 721 ms (≈3% off), stated as a bare number while comparable roundings elsewhere ("about six hundred thousand rows," "about four hundred and twenty thousand rows") are flagged with "about." Same for "Five milliseconds" (actual 5.1 ms). Cosmetic only — consider "about seven hundred milliseconds" for internal consistency.

**Quote (Ch. 4):** *"PostgreSQL calls that a bitmap scan."*

EXPLAIN actually names two separate nodes, "Bitmap Index Scan" and "Bitmap Heap Scan"; "bitmap scan" is common informal shorthand (used by Winand and others) but not the literal terminology. Consider: *"PostgreSQL runs that as a bitmap index scan plus a bitmap heap scan — a bitmap scan, for short."*

---

Everything else checked out: all arithmetic (ratios, rounding, page counts, row counts) is internally consistent and matches the evidence table; the declarative/procedural framing, cost-vs-time distinction, nested-loop/hash-join descriptions, statistics/ANALYZE mechanics, and the stale-statistics walkthrough in Ch. 6 are all canonical and precisely argued; citations (Selinger 1979, PostgreSQL §14.1/14.2, Kleppmann ch. 2, Winand, Leis et al. 2015) are correctly attributed and on-topic.

VERDICT: REVISE
