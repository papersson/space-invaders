Reviewed against the standard sources (Aggarwal–Vitter I/O model notation N/M/B; Ramakrishnan & Gehrke's external-sort chapter; Knuth vol. 3 §5.4; real GNU coreutils `sort` and PostgreSQL behavior). The arithmetic in sections 3–6 all checks out exactly (18→5→2 passes, 12→6→3→2→1, the end-card formula algebraically reduces to R&G's ⌈log_{B−1}(N/B)⌉+1 under the stated variable remapping). The remaining problems are the ones below.

## BLOCKING

**Quote:** "So as long as memory has a block for every run, the whole merge is a single pass" (§4) and "then merge as many runs as memory holds blocks" (§6, the final stated rule).

**What's wrong:** Off-by-one. A multiway merge needs one input block per run *plus one more block for the output buffer*. "A block for every run" / "as many runs as memory holds blocks" describes a merge with zero output buffer, which cannot run. Section 5 does state the correct version once ("one run per block of memory, less one for the output"), but that correction never gets folded back into §4's claim or into §6's closing "rule" — the two places a student is most likely to quote back on an exam state the wrong bound. This is exactly the class of statement the round-1 expert already flagged and asked to be fixed ("a single pass, however many runs there are" → the current wording); the fix is incomplete, it just moved the off-by-one rather than removing it.

**Fix:**
- §4: "So as long as memory has a block for every run, plus one more for the output, the whole merge is a single pass."
- §6: "then merge as many runs as memory holds blocks, less one for the output."

## SHOULD FIX

**Quote:** "Fill memory with the start of the file, sort it right there, and write it back as one sorted piece, called a run."

**What's wrong:** "Write it back" reads as writing the sorted piece back over the same location in the original file. That's not what happens (as the screen direction itself shows — the runs land in `/tmp` as new `sortXXXXXX` files, and the original input is never touched). "Back" should describe returning data to disk, not to its original spot.

**Fix:** "...sort it right there, and write it out as one sorted piece, called a run."

---

**Quote:** "This file is about twelve times bigger than the memory..." (§1) vs. "a file twelve times bigger than its memory" (§6 closing line).

**What's wrong:** 1000 MB ÷ 86 MB ≈ 11.6, correctly hedged with "about" the first time it's said. The closing recap drops the hedge and states it as an exact "twelve," which is inconsistent with the film's own careful arithmetic elsewhere (it even puts "≈ 11.6" on screen).

**Fix:** "That's how sort handled a file about twelve times bigger than its memory..."

---

**Quote:** "blocks of B items" (end-card formula description), and throughout, "blocks of 256," "16 GB ÷ 1 MB ≈ 16,000 blocks."

**What's wrong:** The whole block/pass accounting silently assumes fixed-size records (B items per block, always). The real capture in §1/§3/§5 is GNU `sort` on what is presumably a text file of variable-length lines — real `sort` fills its buffer to a byte budget, not a fixed record count, so "B" there is an average, not a constant. This matters because every "twelve runs" / "two passes" claim about the *real* capture is being justified with a model that technically only holds exactly for fixed-length records. Nothing in the script flags this gap between the idealized (simulation) numbers and the real (text-file) numbers.

**Fix:** Add one clause, e.g. in §2 or as a footnote on the end card: "we're treating every record as the same size; real files — like lines of text — vary, so a block really holds a variable, average number of items."

---

**Quote:** "let the operating system keep the most recently used parts in memory, fetching the rest from disk as needed."

**What's wrong:** States OS page replacement as if it's exact LRU. Real virtual memory systems only approximate LRU (clock/second-chance, etc.); exact LRU is rarely implemented because of its bookkeeping cost.

**Fix:** "...let the operating system approximate this by keeping the most recently used parts in memory..."

## NIT

- **Quote:** "Ask the Unix sort command" (§1) vs. "GNU sort: at most 16 per merge (--batch-size)" (§5 caption). Pick one name consistently, or say explicitly once that "sort" throughout means GNU coreutils' `sort`, since the `--batch-size`/NMERGE=16 default is GNU-specific, not universal to "Unix sort."

- **Quote:** "every fetch takes hundreds of times longer than reading memory, even on a fast SSD." DRAM-vs-SSD random-access latency ratios are commonly cited in the (low) thousands, not hundreds; "hundreds" is defensible as a conservative lower bound but could be softened to "hundreds to thousands" for accuracy.

- **Quote:** "Ramakrishnan & Gehrke, Database Management Systems, 3rd ed., ch. 13; Mehlhorn & Sanders, The Basic Toolbox, §5.7." Both citations match my recollection of the editions' structure, but chapter/section numbers on a permanent end card are a cheap, embarrassing place to be wrong — verify both against the physical books before finalizing, rather than trusting memory (mine included).

- **Quote:** "passes = 1 + ⌈log_{M/B − 1}(N/M)⌉". As typeset, the subscript "M/B − 1" can be misread as a single fraction M/(B−1). Render as "log_{(M/B) − 1}(N/M)" so the base is unambiguous.

- No mention that memory-sized runs are the *simple* case of run formation. Classical treatments (Knuth vol. 3 §5.4) also cover replacement selection, which produces runs of average length ~2M and further cuts the run count. This is legitimately peripheral given the runtime budget and the fact that GNU `sort` itself doesn't do this, so it's fine to omit — flagging only in case the professor wants a one-clause acknowledgment that memory-sized runs aren't the only/best option.

VERDICT: REVISE
