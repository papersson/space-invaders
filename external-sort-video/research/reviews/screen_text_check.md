# Screen-text check of the rendered video

A fresh-context reviewer compared every on-screen text and number in the first full render (one frame near the end of every sentence, plus full-resolution frames) with the locked script's narration and evidence table. The script itself was not under review. Verdict: nothing blocking; seven should-fix items and some layout nits. Every item and what was done:

| Where | On screen | Finding | Done |
|---|---|---|---|
| s1_03 | "memory budget (-S): 86 MB, the same cap" | `-S` sets sort's buffer; only Python ran under an enforced cap (sort's peak RSS was about 89 MB) | Now "sort's memory budget (-S): 86 MB, same as Python's cap" |
| s1_02 | Python gauge ending at "86 MB" | The gauge was forced to the cap; the measured peak RSS was 77,660 KiB, about 80 MB | The gauge now stops at the measured peak, against the 86 MB cap line |
| s1_05 | "0 temp files" above the ghosted rows | Header contradicts the rows shown | Now "12 temp files, now deleted" |
| s1_02 | "cap 86 MB" on the panel border | Layout | Moved beside the cap line; gauge narrowed |
| s2_03 | "hundreds to thousands of times a memory read" | Missing comparison word | "...times slower than a memory read" |
| s2_09 | "soon every step needs a block that isn't in memory" | Stronger than the narration ("keeps needing") | "...so it keeps needing blocks that aren't in memory" |
| s2_09, s2_10 | Counters "4" (heapsort) then "12" (merge sort) | Read without the narration, merge sort looks worse | Each counter now says what it counted: "4 I/Os for 6 items", "12 I/Os for all 72 items" |
| s2_11 | "time →" under equal-width panels | Each panel's axis is that sort's own access count, so equal widths imply equal durations | "each sort, start to finish →" |
| s3_10 | "12 blocks read + 12 written: one pass" | Appears as the narration says "twelve runs"; two different twelves | "toy: every block read once, written once = one pass" |
| s3_13 | "run 12 · partly full" past the panel border | Layout | Panel widened |
| s4_08 | "heap" beside the left child's tag | Reads as "heap run 1" | Moved beside the root |
| s5_04, s5_05 | "runs per merge = blocks of memory − 1", "RUNS PER MERGE 15,999" | Same name as GNU sort's configured "16 runs per merge" a sentence earlier; this one is a maximum | "most runs per merge", "MOST RUNS PER MERGE" |
| s5_08 | "16,000 per merge" after "15,999" | NIT: rounding; results unchanged | Kept: the narration says "sixteen thousand" and the screen shows "≈ 16,000 blocks" |
| s5_13 | "= sorted runs on disk, then merges" past the terminal border | Layout | "= runs on disk, then merges" |
| s6_01 | "18 passes" / "18 → 5 → 2" under records.txt | 18 is the simulated file's count; records.txt (100,000 records) would need 17 plain merge sort passes; 5 and 2 hold for both | Caption now says the row is the simulated file, same proportions |
| End card | R&G notation note too faint | Legibility | Raised contrast |
