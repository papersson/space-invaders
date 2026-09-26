# Script Review

## Test 1 — Opening question / closing answer

**Pass, and a strong one.** The open ("Same query, same table, same machine... So who decides? And why is the same query sometimes fast, and sometimes slow?") is answered almost word-for-word at the close ("So who decides how a query runs? The query planner... That's why the same query can be fast or slow"), and the screen direction explicitly reuses the two cards from chapter 1. No note needed.

## Test 2 — Segment chain, report every "and then"

The author's own chain checks out against the script: each section is causally linked (Because → Therefore → Therefore → Therefore → But → Therefore), not just sequenced. I searched the narration for "and then" specifically — **zero occurrences**. The closest sequencing words are plain "then" (section 3: "Find the customer in the sorted list, then fetch just those rows") which is a step inside one action, not a scene transition, so it doesn't count as padding. Good — this script doesn't limp along on "and then."

## Test 3 — Announced vs. derived ideas

Mostly derived. One weak spot:

- **NIT** — Section 5's opening, *"With more than one table, the planner has more to choose: which table to read first, and how to match rows between them"* — arrives as a topic sentence rather than a felt problem. Every other section transition is pulled forward by a concrete number (the 151ms/0.16ms gap, the "which way is faster" cliffhanger). Joins get a plain announcement instead. Rewrite: *"Everything so far was one table. Ask for orders of customers in a city, and now two tables have to meet — which one does the planner touch first?"* — poses the question before answering it, matching the rest of the video's rhythm.

## Test 4 — Setups/payoffs

Almost everything pays off (4242 and customer-1 numbers from section 1 are cashed in section 4; the index-cost tradeoff from section 3 pays off in section 4's forced-scan experiment). But one payoff actively fights its own setup:

- **BLOCKING** — Section 4: *"...it takes a hundred and fifty milliseconds, and nothing can make it much faster: six hundred thousand rows have to be read."* is flatly contradicted two sentences later: *"a plain index scan for customer one, forced by hand, actually ran a little faster than the planner's plan."* If a different plan ran faster, then something *could* make it faster — the "nothing can make it much faster" claim, which is the whole point of that beat, is undercut by the video's own data. See Test 8 for why this is worse than it looks, and a rewrite below.

## Test 5 — Terms before explanation / multiple names for one concept

- **SHOULD FIX** — "cost" is used in narration ("picks the cheapest," then explicitly "The planner decides by estimated cost, not by the clock") but its actual nature — an abstract unit tuned for disk I/O, not milliseconds — is only stated in the on-screen caption *"cost is an estimate in abstract units, tuned for disk."* An audio-only or half-attentive viewer hears "cost" and reasonably assumes "time," which makes the next sentence ("Its costs assume data read from disk... ran a little faster") baffling. Fold the caption into narration: *"That cost isn't a millisecond count — it's the planner's own yardstick for how much work a plan will do, tuned for reading from disk."*

- **SHOULD FIX** — One concept, three names. The "read every row in storage order" plan is called "full scan" (section 3), then "reads them in the order they're stored on disk" (section 4, term dropped), then "sequential read" (section 7 recap), while the screen the whole time labels it "Seq Scan" (section 5). Four labels for one idea risks the viewer thinking these are different plans. Standardize on "full scan" throughout narration and have the on-screen node read "Seq Scan (full scan)" the first time it appears (section 3 or 5).

## Test 6 — Numbers: which 2–3 matter, which do no work

Numbers worth remembering: **0.16 ms vs 151 ms** (the whole video's spine, correctly bookended), and **1,000x faster after ANALYZE** (the payoff of the takeaway). A reasonable third is **600,000 rows have to be read** (the idea that some slowness is irreducible) — but see below, that claim is exactly what gets undercut.

Numbers that do no work or actively hurt:
- **BLOCKING (ties to Test 4)** — "112.7 ms" (forced index scan for customer 1). It doesn't illustrate the lesson; it contradicts it.
- **NIT** — "1,346 rows" (Tromsø join result) is on-screen only, never narrated, and adds nothing the viewer needs — the count of matching customers (100 vs 99,900) already carries the point. Fine to drop from the screen card.

## Test 7 — Abstraction before the concrete case

No real violations — every abstract claim is a one-sentence signpost immediately grounded in customer 4242 / customer 1 / Tromsø / Oslo numbers. This is a strength of the script, not a problem.

## Test 8 — Wrong intuition, shown failing?

Wrong model has three parts: (a) runs the same way every time, (b) an index always makes it faster, (c) if slow, add an index.

- (a) is shown failing well — the opening's 1000x gap for "the same query" *is* the demonstration.
- (c) is asserted in the closing line ("don't just add an index") but never dramatized as failing. Section 6's stale-statistics fix actually *does* demonstrate this — the customer_id index already existed the whole time; ANALYZE didn't add an index, it just let the planner trust the one already there. The script never says this out loud, so the strongest evidence against wrong-model claim (c) is left implicit.
  - **SHOULD FIX** — Add one clause to section 6: *"Notice: nobody added an index. The index on customer_id was there all along — ANALYZE just told the planner the truth about the data, and it started using the index it had been ignoring."*
- (b) is the **BLOCKING** problem. The section that should confront "an index always makes it faster" is the forced-full-scan-on-4242 demo — but that demo shows the *opposite* case (forcing the scan the planner didn't pick makes things *worse*, i.e. it supports "index=faster," it doesn't confront it). The one place that could confront (b) directly — forcing an index scan on the *common* customer, where an index should plausibly be worse — instead shows the index winning ("a little faster"). So the video never actually shows an index failing to help. As written, wrong-model claim (b) is stated but not refuted by evidence.

**Concrete rewrite for the Test 4/8 BLOCKING item** — simplest fix is to cut the memory/disk aside entirely, since it's the only place the demo contradicts the thesis and it's removable without breaking anything (see Test 11):

> "The choice matters. Force a full scan for the rare customer, and it takes eighty-four milliseconds instead of a sixth of one: five hundred times slower. The planner picks the cheapest estimate, and for the rare customer, that estimate points the right way by a factor of five hundred."

If the editor wants to keep a disk/memory caveat, it needs new data: a forced index scan on the *common* customer that is actually slower than the planner's plan (the expected, disk-bound result), not a run that happens to be faster in memory.

## Test 9 — Examples named but not understood

- **SHOULD FIX** — "Bitmap Index Scan" / "Bitmap Heap Scan" appear on screen (section 4) but "bitmap" is never spoken or explained. A curious viewer is left with an unexplained label. Either drop to the simpler on-screen label "Index Scan," or add one clause: *"...looks them up in the index — first the matching row locations, then the rows themselves — and finds ten."*

## Test 10 — On-screen text vs. narration/pictures

- Covered above: the "cost is abstract units, tuned for disk" caption carries load-bearing content the narration never says (Test 5).
- Otherwise pictures track narration well (the scan-arrow crawl in section 6, the 10-lookups-vs-hash-stream animation in section 5).

## Test 11 — Deletable lines

- **The section 4 disk/memory aside** (*"The planner decides by estimated cost, not by the clock... actually ran a little faster than the planner's plan"*) can be deleted outright without breaking anything before or after it — the paragraph reads cleanly straight from "five hundred times slower" to a closing line about the estimate. Given it's also the source of the BLOCKING contradiction, deletion is the cheapest fix.

## Test 12 — Hard-to-follow sentences / pacing

- **NIT** — Section 6: *"expecting to hit ten of customer one's almost at once"* is awkward heard aloud. Rewrite: *"expecting to find its ten rows almost immediately."*
- **SHOULD FIX (pacing)** — Section 4 is the densest beat in the script: two customers' statistics, two real plans, a forced-scan experiment, a 500x claim, and the disk/memory caveat, all in one section. Cutting the caveat (Test 11) also fixes the pacing — the section was carrying one more idea than it needed.

---

**Summary of must-fix items:** the forced-index-scan-on-customer-1 aside in section 4 contradicts the section's own claim ("nothing can make it much faster") and undermines the one moment that should confront the "index always faster" myth instead of confirming it. Cutting it (Test 11's suggested rewrite) resolves the Test 4, 6, 8, and 12 findings simultaneously.

VERDICT: REVISE
