I checked the script line-by-line, re-derived every number in it, and verified the standard formula and citations against what I know of the sources. It is unusually careful — the internal arithmetic (261,120 / 21,760 = 12; 4,438,017 ≈ 4.4M comparisons matches the exact worst-case merge-sort formula N⌈log₂N⌉ − 2^⌈log₂N⌉ + 1; the end-card formula reduces correctly from Ramakrishnan & Gehrke's `1 + ⌈log_{B−1}⌈N/B⌉⌉` under the video's own variable substitution) all checks out. I found no factual errors that a professor would call wrong. I do have a few precision/clarity notes below, plus one citation I could not independently verify (my web-search tool was denied permission this session).

**SHOULD FIX** — `"GNU sort is more cautious by default: it merges at most sixteen runs at a time... Say a file needed a hundred thousand runs: one merge pass cuts them to seven"`
The "seven" is only correct if you silently switch from GNU sort's real merge width (16) to the earlier hypothetical "~16,000 blocks in memory" capacity (100,000/~16,000 → 7). Read back to back, a numerate viewer will reflexively check 100,000/16 = 6,250 and conclude the numbers don't add up. Fix: restate the assumed capacity in the same sentence, e.g. "Say a file needed a hundred thousand runs, and memory again holds thousands of blocks: one merge pass cuts them to seven."

**SHOULD FIX** — `"Ramakrishnan & Gehrke, Database Management Systems, 3rd ed., ch. 13"`
I believe this is correct (External Sorting is ch. 13 in the 3rd edition, opening Part 3 on query evaluation), but I could not confirm it against a live source this session (web search tool access was denied). This is a citation that will be on screen verbatim, so have someone check it against a physical/PDF copy before final cut rather than trusting my memory alone.

**NIT** — `"With thousands of runs, scanning every front for the smallest item would be slow, so keep a small heap with one entry per run."`
Fine as a simplification, but the source you cite for this exact technique (Mehlhorn & Sanders §5.7) actually presents it via a **loser tree** (tournament tree), not a plain binary min-heap — that's the standard structure in that book and in Knuth vol. 3. Not wrong to say "heap" for a first pass, but if you want the on-screen citation to match what's actually in that section, say "small tournament tree / heap" or just don't lean on the M&S citation for this specific detail.

**NIT** — `"optimal among sorts that move whole records at a time: Aggarwal & Vitter, CACM 1988"`
Technically accurate but the result is an asymptotic (Θ) lower bound, not constant-optimal. Consider "asymptotically optimal among sorts that move whole records at a time" if you want to preempt a sharp-eyed viewer.

**NIT** — `"Eighteen doublings take you from one item to a quarter of a million"`
261,120 is being rounded to "a quarter of a million" (250,000, a 4.5% rounding) purely for spoken cadence; the exact figure is correctly shown on screen throughout, so this is fine, just flagging that it's a rounding, not a fact.

**NIT** — `"Say a file needed a hundred thousand runs... In practice, even enormous files sort in two or three passes."`
The hypothetical (100,000 runs of memory-sized runs, at the stated 16GB/1MB-block capacity) implies a file on the order of an exabyte — far beyond any real sort job — right before a claim about real "enormous files." The general point (few passes suffice) is correct and standard, but the hypothetical's scale is disconnected from real practice; consider softening the hypothetical's framing ("in principle...") or picking a more realistic run count.

**NIT** — Two independent "twelve"s (261,120/21,760 = 12 exactly, in the simulation; and ⌈1,000MB/86MB⌉ = 12, in the real captured demo) are used interchangeably across sections to reinforce one narrative thread. Both are individually correct and the captions do show the arithmetic, but since one is exact and the other is a rounded 11.6, a viewer who is tracking numbers closely could momentarily wonder if it's the same file. Not an error, just worth a beat of narration (or a screen caption) making explicit that these are two separate demonstrations.

**NIT** (optional, not essential) — The run-formation step ("fill memory, sort it, write it out as a run") is the basic method; it omits replacement selection, the standard technique (Knuth vol. 3) for producing runs averaging ~2M rather than exactly M. This is legitimately out of scope for a 5-minute overview and I would not hold up production for it, but if you ever expand this into a longer treatment, it belongs there.

Everything else — the I/O-vs-comparison argument, the heapsort/mergesort locality contrast, the pass-count chain (18 → 5 → 2), the multiway-merge mechanics, the buffer-count rule (blocks = runs + 1 for output), the GNU sort NMERGE=16 default and `--batch-size` flag, the PostgreSQL "external merge" EXPLAIN output, and the closing formula — is correct, canonical, and appropriately scoped.

VERDICT: PASS
