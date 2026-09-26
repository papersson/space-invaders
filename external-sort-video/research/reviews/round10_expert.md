## Review

### BLOCKING

**Quote:** "Heapsort and merge sort are both N log N sorts. If comparisons decided speed, they would run about equally fast."
**What's wrong:** This teaches the classic false equivalence "same big-O class ⇒ same speed." The video's own simulation contradicts it two sentences later: heapsort makes ~8.6M comparisons vs merge sort's ~4.4M — a ~2× constant-factor gap. Even restricting attention to comparisons alone, they would *not* run "about equally fast"; heapsort would already be ~2× slower before I/O is considered. A professor would flag this as exactly the misconception courses try to inoculate against.
**Fix:** "Heapsort and merge sort are both N log N sorts — same order of growth. By comparisons alone, heapsort is only about twice as slow as merge sort. Comparisons alone don't explain what's coming."

**Quote:** "every fetch takes hundreds to thousands of times longer than reading memory, even on a fast SSD" — contrasted with the later figures used in the same section: "~10 ns per comparison, ~100 µs per I/O"
**What's wrong:** 100 µs / 10 ns = 10,000×, which is an order of magnitude past the "hundreds to thousands" ceiling the narration just asserted. The script's own worked numbers contradict its own stated bound within the same section.
**Fix:** Either change the spoken bound to "thousands to tens of thousands of times longer" or adjust the "typical" figures (e.g., use a comparison cost that reflects true memory-access latency, ~100 ns, giving a consistent ~1000× ratio) so the general claim and the concrete numbers agree.

### SHOULD FIX

**Quote:** Header note — "Word target: about 750 (5 minutes at about 150 words per minute of finished video)."
**What's wrong:** I counted the spoken narration lines verbatim (the `>` blocks only, excluding all *Screen:* directions): 1,039 words. At 150 wpm that's ~6.9 minutes, not 5 — a 39% overage. This matters here specifically because round 1's fix ("every number now carries its reason") added the length, and numeral-dense narration typically needs to be read *slower* than 150 wpm for comprehension, not faster — so the real runtime is likely closer to 7–7.5 minutes.
**Fix:** Either trim ~35% of the narration to hit the stated budget, or update the target to reflect the actual word count/runtime (e.g., "~1040 words, ~7 minutes at 150 wpm") so production timing isn't set incorrectly.

**Quote:** "GNU sort is more cautious by default: it merges at most sixteen runs at a time, trading some speed for less memory."
**What's wrong:** I could not verify this online in this session (no search access), so flagging with appropriate hedging rather than asserting it's wrong: my recollection of the coreutils documentation is that the default cap on simultaneous merge inputs (`--batch-size`/NMERGE, default 16) is motivated primarily by avoiding exhaustion of open file descriptors during the merge (each run being merged needs an open file handle), with memory being a secondary, related concern — not "memory" as the primary trade-off. Worth the scriptwriters double-checking the actual man page/source comment before final cut, since a systems-savvy viewer may know the file-descriptor reasoning.
**Fix (if confirmed):** "GNU sort is more cautious by default: it merges at most sixteen runs at a time — partly to avoid running out of open file handles, partly to save memory."

### NIT

**Quote:** "Eighteen doublings take you from one item to a quarter of a million" / "on a quarter of a million items"
**What's wrong:** The simulated file is 261,120 items, about 4.4% above 250,000. The doubling arithmetic itself (2¹⁸≈262,144, so 18 passes) is correct and matches the exact count, but calling 261,120 "a quarter of a million" is a slightly loose rounding for narration precision, though harmless since the exact figure is given on screen.
**Fix:** Optional — "about a quarter of a million" (adds one word of hedging), or none needed given the on-screen caption already states the exact number.

**Quote:** "Each extra pass lets the file be thousands of times bigger."
**What's wrong:** The screen's own figure for this scenario is a fan-in of "16 GB ÷ 1 MB ≈ 16,000 blocks," i.e. each extra pass multiplies capacity by ~16,000 — better described as "tens of thousands of times bigger" than "thousands."
**Fix:** "Each extra pass lets the file be tens of thousands of times bigger."

**Quote:** Whole section on runs/run-formation (section 3).
**What's wrong (missing, not false):** The video presents run formation purely as "fill memory, sort, write" — which is in fact accurate for GNU sort's actual algorithm, so nothing stated is wrong. But this omits replacement selection (covered in the cited R&G ch. 13), the classical technique that produces runs averaging ~2× memory size and thus fewer runs to merge. Since it's peripheral to the video's chosen worked example (which correctly reflects real GNU sort behavior) and a 5-minute budget is already tight, this is optional, not a defect — flagging only so the omission is a deliberate choice rather than an oversight.
**Fix:** None required; optionally a single clause: "(real systems can do better still with replacement selection, which we won't cover here)."

---

Everything else checked out cleanly and is worth noting as correctly done: the I/O-vs-comparison counts (8.6M/4.4M, 837,090/36,720, "about twice," "more than twenty times," "about three per item") are internally consistent and match exactly (18 passes × 1020 blocks × 2 = 36,720); the 14/4/5 and 12/6/3/2/1 pass arithmetic is exact; the end-card formula correctly translates R&G's B/N (buffer pages/pages) into the video's M/B and N/B, and the worked substitutions (85 blocks, 12 runs → 2 passes; 100,000 runs, ~16,000 fan-in → 7 → 1) check out; the Aggarwal–Vitter optimality claim is properly scoped to the indivisibility assumption; the GNU sort NMERGE=16 default and PostgreSQL "external merge" EXPLAIN output are accurate; R&G ch. 13 is indeed "External Sorting."

VERDICT: REVISE
