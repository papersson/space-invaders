# Review

## BLOCKING

**Quote:** "Our file is twelve memories long, so this makes twelve runs, in a single pass."

**Problem:** This states as fact that the file is exactly twelve times the size of memory. It isn't — the file is 1,000 MB against 86 MB of memory, a ratio of ≈11.6, and the video's own caption in the same section says so ("1,000 MB ÷ 86 MB ≈ 11.6, so 12 runs"). Twelve runs come from *rounding up* 11.6 (the last run is a partial one, 63.02 MB vs. 85.18 MB for the others — see the evidence table), not from the file being an exact multiple of memory. Stating it as "is twelve memories long" contradicts the video's own correct arithmetic elsewhere and would visibly clash with the on-screen fraction.

**Fix:** "Our file is a little under twelve memories long — round up, and that's twelve runs, in a single pass."

---

**Quote:** "Real sorting programs read much bigger blocks than our simulation did, often a megabyte, to cut down on fetches, and a laptop's memory still holds about sixteen thousand of those. … So each extra merge pass lets the file grow by that same factor of sixteen thousand. In practice, even enormous files sort in two or three passes."

**Problem:** This immediately follows, and is easy to hear as still describing, GNU sort — which the previous two sentences just said caps its fan-in at 16 runs per merge *by default*, regardless of how much memory is free. A merge with fan-in capped at 16 needs ⌈log₁₆(runs)⌉ passes, not ⌈log₁₆,₀₀₀(runs)⌉ passes: for the hypothetical 100,000-run file the script uses as its example, GNU sort's actual default would take ⌈log₁₆(100,000)⌉ = 5 merge passes (plus the run-forming pass = 6 total), not "two or three." The "2–3 passes for enormous files" claim (correctly attributed to Ramakrishnan & Gehrke) describes a merge whose fan-in scales with memory — i.e., a differently-tuned sort, or a database engine — not the sort command's default just described. As written, a careful viewer is left believing the demoed tool, unmodified, will always finish huge files in 2–3 passes; that's false under the setting the script itself just gave.

**Fix:** Add an explicit pivot, e.g.: "That's more runs than sort's default of sixteen will merge at once — reaching two or three passes on a file that size needs a fan-in that grows with memory, the way database sort implementations (and sort with a larger `--batch-size`) do it." Then continue with the 16,000-at-a-time example as describing that idealized/tunable case, not GNU sort's default.

## SHOULD FIX

**Quote:** "By comparisons alone, heapsort would be at most about twice as slow."

**Problem:** "At most" claims a proven bound; what's actually being invoked is the well-known asymptotic constant (heapsort ≈ 2N log₂N comparisons, merge sort ≈ N log₂N), which the measured ratio (1.97×) supports as "roughly," not as a guaranteed ceiling for all N and all implementations.

**Fix:** "By comparisons alone, heapsort would be about twice as slow."

---

**Quote:** "That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."

**Problem:** The arithmetic (5 total) is correct, but the reasoning glosses over a real substitution. Continuing the doubling schedule for 14 passes produces ⌈261,120/16,384⌉ = 16 pieces of size 16,384; filling memory and sorting once instead produces 12 pieces of size 21,760. These are different run counts from different constructions — it's a coincidence (both happen to need ⌈log₂(runs)⌉ = 4 more two-way merges) that the total still comes out to 5. The script's phrasing ("the last four remain") implies the same four passes carry over unchanged, which isn't quite what happens.

**Fix:** "Replacing those fourteen passes with one leaves twelve runs instead of sixteen pieces — but merging twelve runs two at a time still takes four more passes, so eighteen passes become five: one to make the runs, four to merge them."

---

**Quote:** "Merge sort merges single items into pairs, then pairs into fours, doubling the pieces every pass."

**Problem:** This describes bottom-up (iterative, natural) merge sort specifically. Most undergraduates first learn top-down recursive merge sort, which doesn't have this same clean "doubling per pass over the whole array" structure (though its total work is equivalent). Not naming the variant risks a mismatch with what students already know.

**Fix:** Add "(this is bottom-up merge sort: instead of recursing, just keep merging same-size pieces left to right)" at first mention.

## NIT

**Quote:** "We simulated both under virtual memory on a quarter of a million items."

261,120 is about 4.4% above 250,000; "roughly a quarter of a million" would be more accurate than the flat "a quarter of a million," though the exact figure appears on screen regardless.

**Quote:** "Heapsort and merge sort are both N log N sorts."

Minor terminology looseness — "Θ(N log N) comparison sorts" would be more precise given the very next sentences are all about counting comparisons.

---

VERDICT: REVISE
