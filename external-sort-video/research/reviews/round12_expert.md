Reviewed the script and cross-checked every number in the evidence table against the narration and on-screen text (recomputed all the pass-count and I/O arithmetic independently). The script is unusually well fact-checked — I did not find a single arithmetic or terminology error that would make a claim false. My findings are all precision/clarity issues.

## Findings

**SHOULD FIX** — *"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."*
This example implicitly uses a fan-in of ~16,000 (from "a laptop's memory still holds thousands of those [megabyte blocks]," two sentences earlier), but it comes right after the video has just stated GNU sort's *actual* default fan-in of **sixteen** ("it merges at most sixteen runs at a time"). A viewer anchoring on the number just spoken ("sixteen") rather than the visual ("≈16,000 blocks") would get this wrong: with a 16-way fan-in, one pass reduces 100,000 runs to ⌈100,000/16⌉ = 6,250, not 7, and full merging would take 5 passes, not 2. The on-screen caption disambiguates it, but the audio alone does not.
Fix: make the assumption explicit in the narration, e.g. *"Say a file needed a hundred thousand runs. With sixteen thousand blocks of memory to merge from, one pass cuts them to seven, and one more makes them one file."*

**NIT** — *"This file is about twelve times bigger than the memory we'll let our programs use."*
1,000,000,000 / 86,000,000 ≈ 11.6, not 12. The later caption correctly shows "≈ 11.6, so 12 runs" — the two don't quite line up. "About twelve" is a defensible rounding, but a more exact "just under twelve times" would avoid the tension with the later precise figure.

**NIT** — *"That one pass covers everything the first fourteen did, so only the last four remain."*
This is true but slightly overclaims equivalence: 14 doubling-passes reach piece size 2¹⁴ = 16,384, while the actual run size is M = 21,760 — the single run-formation pass does *more* than 14 doubling-passes would, not merely "the same." The final pass count (5, then 2) is independently correct from the run-count arithmetic, so this doesn't propagate an error, but the phrasing invites a false "exact match" reading.
Fix: *"One pass gets you at least as far as those fourteen doublings would — in fact further, since a run holds more than fourteen doublings' worth."*

**NIT** — *"optimal among sorts that move whole records at a time: Aggarwal & Vitter, CACM 1988"*
The standard term in the I/O-model literature is the **indivisibility assumption** (records are atomic — comparable and movable but not decomposable), and the result is an asymptotic (Θ) bound, not exact optimality for every N, M, B.
Fix: *"asymptotically optimal, in number of I/Os, among algorithms that treat records as indivisible units (the indivisibility assumption) — Aggarwal & Vitter, CACM 1988."*

**NIT** — *"(Ramakrishnan & Gehrke write B for buffer pages, this video's M/B, and N for pages, this video's N/B)"*
Grammatically terse to the point of being hard to parse on a freeze-frame.
Fix: *"(Ramakrishnan & Gehrke's B is the number of buffer pages — this video's M/B — and their N is the number of pages in the file — this video's N/B.)"*

**NIT** — *"Each extra pass lets the file be thousands of times bigger."*
With the ~16,000-way fan-in used in this section, the multiplier per extra pass is closer to "ten thousand times" than "thousands of times."
Fix: *"tens of thousands of times bigger"* (or just say "roughly the merge fan-in bigger," tying it back to the ≈16,000 figure already on screen).

**NIT** — *"every fetch takes hundreds to thousands of times longer than reading memory, even on a fast SSD."*
Stated as a flat fact rather than flagged as typical/representative (the evidence table itself labels the 100 ns / 100 µs figures "typical values").
Fix: add "typically": *"typically takes hundreds to thousands of times longer."*

None of these affect the correctness of the core argument (I/O cost model, why virtual memory doesn't rescue heapsort, run formation, multiway merge, pass-count formula) — every number I recomputed from the evidence table matched the script exactly, including the less-obvious internal consistency checks (e.g. 18 passes × 2,040 I/Os/pass = 36,720 matching the naive merge-sort I/O count; 21,760/256 = 85 blocks of memory; the end-card formula reproducing "2 passes" when plugged with N=261,120, M=21,760, B=256).

VERDICT: PASS
