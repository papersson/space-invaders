# Script Review

## 1. One question

The opening ("This file is about twelve times bigger than the memory... What are those files, and how does sort get away with it?") is a genuine single question with two clauses that resolve together. The ending mirrors the exact number ("a file about twelve times bigger than its memory") and gives the mechanism ("twelve runs, one merge, two passes"), but the *identity* payoff — "those files were the runs" — was already delivered in Section 3, not restated in the actual closing line. A viewer who forgot Section 3 doesn't get the "files = runs" answer repeated at the moment the video says "the answer."

- **SHOULD FIX** — Quote: *"That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."*
  Rewrite: *"That's what those twelve files in /tmp were: the runs. That's how sort handled a file about twelve times bigger than its memory — twelve runs, one merge, two passes — while Python tried to hold it all at once."*

## 2. But/therefore chain

Compressed chain (each section as one sentence):

1. Python OOMs, sort finishes, twelve files appear then vanish — **question**.
2. Virtual memory looks like the fix, **but** disk I/O is what's expensive, **therefore** measure in I/Os/passes, not comparisons.
3. Merge sort needs 18 passes, **but** the first 14 passes' pieces already fit in memory, **therefore** sort those in place as "runs" — cutting 18→5, and that's the twelve files.
4. Two-way merging leaves memory idle, **therefore** give every run a block and merge all at once with a heap, cutting 5→2.
5. Twelve runs was easy, **but** what about huge files — sort caps a merge at 16, **but** bigger files need multiple merges, **therefore** passes still stay at 2-3, **therefore** databases do the same.
6. Recap and callback.

Almost the whole script chains cleanly with explicit "but/so/therefore." One real "and then" gap:

- **SHOULD FIX** — Quote: *"Once data doesn't fit in memory, the number of I/Os dominates the running time.[¶] Heapsort and merge sort are both N log N sorts. We simulated both..."*
  The jump from "I/Os dominate" straight to a simulation reads as sequence, not consequence — there's no stated question the simulation answers.
  Rewrite: *"...the number of I/Os dominates. So does it matter which N log N sort you use? Heapsort and merge sort are both N log N — we simulated both under virtual memory..."*

## 3. Derive, don't reveal

This is the script's strongest test. I/O, block, pass, run, multiway merge, and external merge sort are all named *after* the problem that motivates them is shown (idle memory → multiway merge; slow scanning of many fronts → heap; sub-memory pieces → runs). No findings — this test passes cleanly.

## 4. Setups and payoffs

Nearly everything set up pays off (twelve files → runs → deleted at the end; 18 passes → 5 → 2; the wrong model → shown failing → explicitly named in the recap). One setup creates a payoff that reads as a quiet retraction:

- **SHOULD FIX** — Quote: *"With thousands of runs, scanning every front for the smallest item would be slow, so keep a heap with one entry per run."* ... later, Section 5: *"Sort itself caps a merge at sixteen runs by default."*
  Said this way, "thousands of runs" sounds like what sort actually does, then Section 5 quietly corrects it to 16. Frame it as hypothetical up front so Section 5 confirms rather than corrects.
  Rewrite: *"If a merge ever had to juggle thousands of runs, scanning every front for the smallest would be slow — so keep a heap with one entry per run instead."*

## 5. One vocabulary

I/O, block, pass, run, multiway merge, external merge sort — each defined at first use, none renamed later. One cross-document mismatch:

- **NIT** — The stated learning objective says viewers should explain "why cost is counted in **block transfers**," but the script only ever says **I/O**. Not a viewer-facing problem (the term is consistent within the script), but worth aligning the objectives doc to the script's actual word.

## 6. Number budget

Numbers present: 12 (files/runs), ~12x (file:memory ratio), 18 (doublings/passes), ¼ million / 261,120 (items), 21,760 (memory items), 256 (block size), 14 (passes < memory), 5 (passes after run formation), 2x comparisons / 20x I/Os (8.6M vs 4.4M; 837,090 vs 36,720), ~3 I/Os per item, 4 (merge passes), 16 (sort's default run cap), 16,000 (blocks in 16GB), 2-3 (passes at scale), 107,696kB (Postgres example).

**Should remember:** 12 (why sort made twelve files), 2 (final pass count — the payoff), and the 20x-vs-2x mismatch (the proof that I/Os, not comparisons, decide speed). Everything else is scaffolding.

- **NIT** — The exact figures 8.6M/4.4M, 837,090/36,720, and 107,696kB do no work beyond what the spoken ratios already carry ("twice as many comparisons," "twenty times as many I/Os," "external merge"). Fine as screen captions for credibility, but none needs to land as a number the viewer retains — worth confirming they stay caption-only and are never asked to be recalled.

## 7. Concrete before abstract

Well-ordered throughout: "run," "multiway merge," and "external merge sort" are all named after the concrete mechanism is shown; the formula card is explicitly held to the very end as a silent reference. No findings.

## 8. Wrong model

Wrong model: "comparison counts decide speed, and virtual memory takes care of the disk." Both halves are shown failing — virtual memory's fetch-a-whole-block cost, and heapsort's catastrophic I/O count under it. But the disproof of the *comparisons* half is left for the viewer to compute:

- **SHOULD FIX** — Quote: *"Heapsort made about twice as many comparisons as merge sort, and more than twenty times as many I/Os."*
  The logic ("2x comparisons can't explain 20x I/Os, so comparisons aren't the bottleneck") is never stated — it's implicit. Also worth checking against the review log, which claims an "equal-comparisons line" was added to sharpen this; the current text still shows a 2x gap, not equal, so either the log is stale or the promised line didn't make it in.
  Rewrite: *"Heapsort made about twice as many comparisons as merge sort — but more than twenty times as many I/Os. Twice the comparisons doesn't explain twenty times the I/Os. The disk does."*

## 9. Depth over breadth

Only one outside application is named (PostgreSQL), and it's given real depth (an actual `EXPLAIN ANALYZE` line, tied to the same "more data than memory" condition), not a name-dropped list. No findings.

## 10. Words and pictures

Screen direction is unusually well matched to narration throughout (e.g., the two-way-merge tray lighting exactly the blocks the line describes). Two spots where the caption just re-says the sentence in numeric form:

- **NIT** — Quote (caption): *"1,000 MB ÷ 86 MB ≈ 11.6, so 12 runs"* next to narration *"Our file is twelve memories long, so this makes twelve runs."* Let the caption carry only the arithmetic; drop its "so 12 runs" since the narration already delivers that line.
- **NIT** — Same pattern for *"2¹⁸ ≈ 262,144"* beside "Eighteen doublings... quarter of a million... eighteen passes."

## 11. Deletion test

Script is tight; little pure filler. One candidate that could be cut without weakening the core argument or breaking a later payoff:

- **NIT** — Quote: *"Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."*
  Nice generalizing touch, but the central question (what were sort's twelve files) is fully answered without it. Keep if time allows; first thing to cut if the 750-word budget is tight.

## 12. For the ear and pacing

The formula and the Ramakrishnan/Gehrke notation note are correctly kept off narration (silent end card) — good call. Two spots:

- **NIT** — Quote: *"One per block of memory, less one for the output, and a laptop's memory holds thousands of blocks."* "Less one for the output" is awkward read aloud.
  Rewrite: *"One run per block of memory — minus one held back for the output — and a laptop's memory holds thousands of blocks."*
- **SHOULD FIX (pacing)** — Section 2 is the densest beat in the script: virtual memory's failure, the I/O definition, an N log N reminder, and two different simulation ratios (comparisons, I/Os) plus a per-item I/O count all land within a few sentences. This is the section the review log already flagged students getting lost in once; the fix (numbers "carrying their reason") helps but the section still stacks three separate numeric claims back to back. Consider a beat (a held shot, or the bridging question from Finding #2 above) between naming "I/O" and firing the simulation numbers.

---

No finding here rises to breaking the argument or falsifying the takeaway — the script's own prior revision round already removed the one true blocking issue (the false "single pass" claim). The remaining items are polish: sharpen the comparisons/I/Os disproof, add one bridging sentence, soften the "thousands of runs" vs. "caps at 16" tension, and trim two redundant captions.

VERDICT: PASS
