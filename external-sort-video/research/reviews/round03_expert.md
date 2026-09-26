# Review

## BLOCKING

**Quote:** *"Two terminals replaying the real runs; memory gauges with the same 88 MB cap"* (§1) vs. *"beside the bars '1 GB ≈ 12 × 84 MB'"* (§3)

**Problem:** These two captions describe the same real captured demonstration (one file, one memory cap, twelve runs), but they give two different values for the memory cap — 88 MB in §1, 84 MB in §3. They can't both be the true figure from the actual capture. As written, an attentive student who screenshots both frames will conclude the numbers were invented rather than measured, which undercuts the video's entire premise that these are real captured runs, not toy numbers.

**Fix:** Use one value throughout. Either change §3's card to "1 GB ≈ 12 × 88 MB" or change §1's cap (and gauges) to 84 MB — whichever matches the actual capture.

## SHOULD FIX

**Quote:** *"That's why databases sort this way. When a query sorts more than fits in its memory, PostgreSQL reports an external merge."*

**Problem:** This is very likely accurate (PostgreSQL's `EXPLAIN ANALYZE` does print `Sort Method: external merge` for disk-based sorts), but I can't certify the exact literal string against the currently shipping version without checking a live plan. Since the screen shows this as a verbatim `EXPLAIN` line, a single wrong character (e.g., if some version prints "external sort" instead) would be an embarrassing, easily-checked error in a frame that's presented as a direct capture.

**Fix:** Before final render, capture a real `EXPLAIN ANALYZE ... ORDER BY ...` on a query forced to spill, and use that literal output rather than a remembered/typed string.

**Quote:** *"Ramakrishnan & Gehrke ch. 13"*

**Problem:** Chapter numbering for "External Sorting" is specific to an edition of *Database Management Systems*. Citing without an edition risks pointing students at the wrong chapter if they have a different printing.

**Fix:** "Ramakrishnan & Gehrke, *Database Management Systems*, 3rd ed., ch. 13."

## NIT

**Quote:** *"Mehlhorn & Sanders §5.7"*

**Problem:** I'm not fully confident the external-sorting material sits at exactly §5.7 in *Algorithms and Data Structures: The Basic Toolbox* from memory alone — worth a direct check against the book's table of contents before it goes on an end card, since a wrong section number is a small but visible citation error.

**Fix:** Confirm the section number against the actual book before finalizing the end card.

**Quote:** *"Make runs, then merge them, as many at a time as memory allows: that's external merge sort."*

**Problem:** Minor compression — "as many at a time as memory allows" is the *optimization* (maximizing fan-in to minimize passes), not part of the definition of external merge sort itself; the unoptimized 2-way version shown earlier in the same section is also external merge sort. This mirrors Ramakrishnan & Gehrke's own progression (2-way external merge sort → external merge sort with full fan-in), so it's a defensible compression for time, not an error — flagging only because a sharp student could momentarily think the 2-way version they just watched "doesn't count" as external merge sort.

**Fix (optional, low priority):** "...sort in memory, then merge from disk — that's external merge sort. Merging as many runs at once as memory allows keeps it to the fewest possible passes."

**Quote:** *"cut the passes: make runs as big as memory, then merge as many runs as memory holds blocks."* (§6 recap)

**Problem:** Drops the "less one, for the output buffer" caveat that §5 correctly established ("One per block of memory, less one for the output"). Harmless as a compressed recap since the precise version was already given once, but worth noting it's not literally restating the formula.

**Fix:** No change needed if time is tight; if there's room, "...merge as many runs at once as memory holds blocks for, minus one."

---

Everything else checks out: the I/O-vs-comparison framing, the pass-doubling arithmetic (18 → 5 → 2, verified two independent ways and internally consistent), the 12-runs/4-merge-passes count, the fan-in formula (which I verified translates exactly to Ramakrishnan & Gehrke's `1 + ⌈log_{B-1}(N/B)⌉` once B/N are remapped from pages to items), the GNU `sort --batch-size` default of 16, and the Aggarwal–Vitter attribution (CACM 1988, correctly scoped to the indivisibility model) are all accurate and canonically stated.

VERDICT: REVISE
