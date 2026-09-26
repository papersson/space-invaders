# Script Review — External Merge Sort Explainer

## 1. One question
**Finding (NIT).** The mystery is resolved two-thirds of the way through rather than held for the ending.
> "And that's what sort's twelve files were. It filled its memory twelve times, and wrote out twelve runs." (§3)

The true ending (§6) then re-answers it ("twelve runs, one merge, two passes"), which works as a synthesis but softens the reveal — by the time you get there, the answer is already known, so the ending is confirming, not revealing.
**Rewrite:** Hold the line "that's what sort's twelve files were" out of §3 and move it into §6, right after "Python tried to hold the whole file in memory at once. Sort never held more than a memory's worth." Let §3 end on the mechanism ("Eighteen passes become five") without naming the payoff yet.

Otherwise: PASS. The ending explicitly calls back to "twelve times bigger" and "twelve files/runs" from the opening.

## 2. But/therefore chain
Chain holds together well end to end (obvious-fix-fails → measure in passes → runs collapse passes → multiway merge collapses passes further → how far it scales → recap). One explicit violation:

**Finding (SHOULD FIX).**
> "A big enough file needs even more runs than that, **and then** it takes more than one merge pass."

This is actually a therefore (more runs → more passes needed), not an "and then." Using "and then" here makes a causal step read as a mere sequence.
**Rewrite:** "A big enough file needs even more runs than that — so it takes more than one merge pass."

**Finding (NIT).** The Postgres beat at the end of §5 is joined to the rest of the section only by "That's why databases sort this way," which is a generic gesture rather than a specific but/therefore link to the preceding claim about pass counts. See also Test 9/11.

## 3. Derive, don't reveal
This is the script's strongest dimension — I/Os, passes, runs, and the multiway merge are all derived from a visible problem (idle memory, wasted comparisons, blocks smaller than memory, etc.), not announced.

**Finding (NIT).** The multi-pass-for-huge-files idea in §5 is asserted by arithmetic rather than shown failing/succeeding the way earlier ideas were:
> "A big enough file needs even more runs than that... Each extra pass lets the file be thousands of times bigger."

No failure case is shown (e.g., "if you only had one merge pass with 16,000-way fan-in, a file needing 200,000 runs simply couldn't finish in one pass"). It's told, not derived.
**Rewrite:** Add one concrete failing case before the fix: "Give a merge 16,000 runs and it's fine. Give it 200,000, and no single merge can take them all in — you need a second pass first." Then state the "thousands of times bigger per pass" payoff.

## 4. Setups and payoffs
Mostly clean — twelve files/runs, the 86 MB memory bar, and the pass tally (18→5→2) are all set up and paid off with care.

**Finding (SHOULD FIX): payoff with no setup.**
> "Real sorting programs read much bigger blocks than our simulation did, often a megabyte... a laptop's memory still holds about sixteen thousand of those."

This jumps to a new scale (1 MB blocks, 16,000 of them) without bridging from the simulation's own numbers (256-item blocks, 21,760-item memory). A viewer trying to reconcile the two will lose the thread.
**Rewrite:** "Our simulation used 256-item blocks. Real sort uses much bigger ones — often a megabyte — so a laptop's 16 GB holds about sixteen thousand of them, not twelve."

**Finding (NIT): setup with no payoff.** "GNU coreutils sort 9.4" is labelled on screen in §1 and never referenced again.
**Rewrite:** Drop the version label, or pay it off later ("this is the exact behavior of coreutils 9.4's --batch-size default").

## 5. One vocabulary
Terms are defined at first use throughout (I/O, block, pass, run, multiway merge, external merge sort) — solid discipline.

**Finding (NIT): one term, two referents.** "Heap" names both heapsort's whole-file heap (§2) and the small in-memory run-pointer heap (§4). The script does disambiguate inline ("Unlike heapsort's heap, which was the whole file...") so it's not confusing, but it's worth a rename to avoid relying on that aside.
**Rewrite:** Call the new structure a "selection heap" or "merge heap" throughout §4 instead of reusing "heap" bare.

**Finding (SHOULD FIX): screen introduces unspoken jargon.**
> Screen: "GNU sort: at most 16 per merge (--batch-size)"

Narration never says "batch-size," so the viewer reads a flag name that's never spoken or explained.
**Rewrite:** Either narrate it ("...sixteen at a time by default — sort calls this its batch size") or drop the flag text from the screen direction.

## 6. Number budget
The script separates "remember this" numbers (narrated, rounded: "twice as many comparisons," "twenty times as many I/Os," "under a second" vs "more than a minute") from "prove this" numbers (screen-only, exact: 8.6M vs 4.4M, 837,090 vs 36,720) — good design.

**The 2–3 numbers worth remembering:** (1) 12× — file vs. memory, and 12 runs; (2) 18 → 2 — the pass count collapse; (3) the ~100 ns vs ~100 µs (≈1000×) gap between a comparison and an I/O.

**Finding (SHOULD FIX): number does no work.**
> "A real PostgreSQL EXPLAIN ANALYZE line: 'Sort Method: external merge  Disk: 107696kB'"

107696kB is never connected to memory size, run count, or anything else — it's decoration.
**Rewrite:** Either cut the number ("Sort Method: external merge" alone proves the point) or connect it ("more than the few hundred MB of work_mem it was given").

**Finding (NIT):** "GNU coreutils sort 9.4" (see Test 4).

## 7. Concrete before abstract
Passes clean. The end-card formula and the general takeaway rule both arrive only after every concrete case has run — correct ordering throughout.

## 8. Wrong model
Best-executed section. "Comparisons decide speed / virtual memory handles the disk" is stated, then made to fail visibly: heapsort beats merge sort on comparisons but loses by >20× on I/Os, dramatized as 0.86 s vs. 84 s. This is a textbook confront-and-fail. No finding.

## 9. Depth over breadth
Only one real-world example (PostgreSQL) is used, not a list — so this mostly passes. But that one example is thin:

**Finding (SHOULD FIX).**
> "Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."

Named but not connected to any of the video's own numbers (its runs, its pass count, its memory ratio) — it's asserted as relevant rather than shown working the same way. Combined with the dangling 107696kB (Test 6), this reads as breadth tacked onto a depth-focused script.
**Rewrite:** Either cut it (see Test 11) or tie it back explicitly: "...the same shape as our twelve runs and one merge, just at database scale."

## 10. Words and pictures
Mostly well-differentiated (screen carries exact digits, narration carries rounded claims — genuinely complementary, not redundant).

**Finding (SHOULD FIX):** the --batch-size screen text (Test 5) is a words/pictures mismatch — the eye gets a term the ear never receives.

**Finding (NIT):** "N log N under both names" on screen while narration says "Heapsort and merge sort are both N log N sorts" — mild same-thing-twice, low cost since it's just anchoring a label, not a full sentence duplicated.

## 11. Deletion test
**Finding (SHOULD FIX): cuttable without loss.**
> "Our file needed only twelve runs, and GNU sort merges up to sixteen at a time by default, a cautious setting that trades some speed for less memory. That was plenty for twelve. ... Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."

None of objectives 1–4 depend on GNU's specific batch-size default or the Postgres aside — both are colour, not argument, and both introduce unexplained numbers (16, 107696kB) that this review flags elsewhere as doing no work.
**Rewrite:** Cut the batch-size aside and the Postgres line; end §5 on "In practice, even enormous files sort in two or three passes," which already delivers the "how far it goes" payoff cleanly.

**Finding (NIT):** "GNU coreutils sort 9.4" screen label (Test 4) — cuttable, no payoff.

## 12. For the ear and pacing
**Finding (SHOULD FIX): overstuffed sentence.**
> "We simulated both under virtual memory, on a quarter of a million items, with memory for a twelfth of them, roughly the same proportions as sort's file."

Three quantities and a comparison stacked in one breath is hard to track by ear alone.
**Rewrite:** "We simulated both under virtual memory: a quarter of a million items, with memory for only a twelfth of them — the same proportions as sort's own file."

**Finding (SHOULD FIX): rushed beat.**
> "Say a file needed a hundred thousand runs. Merging sixteen thousand at a time, one pass cuts them to seven, and one more makes them one file. Each extra pass lets the file be thousands of times bigger."

Four numbers and a generalization land in three sentences with no pause for the arithmetic to register, and "thousands of times bigger" isn't derived from the numbers just given.
**Rewrite:** Split into two beats: "Say a file needed a hundred thousand runs. One pass, merging sixteen thousand at a time, cuts that to seven. One more pass finishes it. [beat] That's the pattern: each extra pass multiplies what you can sort by sixteen thousand — which is why even enormous files take only two or three passes."

**Finding (NIT):** §4's callback "Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time" asks the viewer to recall a detail from several minutes earlier; low risk given the screen direction reinforces it, but worth a beat of pause when read aloud.

---

**Summary of severities:** 0 BLOCKING, 9 SHOULD FIX, 6 NIT. The core structure — question, derivation chain, wrong-model confrontation, concrete-before-abstract ordering — is sound and well-executed; the weak spots cluster in §5 (pacing, an under-derived multi-pass claim, a breadth-y unexplained Postgres example) and a few decorative numbers/terms that do no work.

VERDICT: PASS
