## Review

**Word count / pacing** — SHOULD FIX
> "Word target: about 750 (5 minutes at about 150 words per minute of finished video)."

The spoken narration (excluding all screen directions) runs **1,029 words**, not ~750 — 37% over target. At 150 wpm that's 6:52 of finished video, not 5:00; hitting 5:00 would require ~206 wpm, too fast for clear narration over this much simultaneous on-screen detail. Fix: cut ~280 words (candidates: the "twice as many comparisons... more than twenty times as many I/Os" para in §2 and the fan-in paragraph in §5 both restate numbers already shown on screen) or state an honest target ("~1,000 words, ~7 minutes").

**Ratio inconsistency between the qualitative and quantitative disk/memory claims** — SHOULD FIX
> "every fetch takes hundreds to thousands of times longer than reading memory, even on a fast SSD"
> ... later: "~10 ns per comparison, ~100 µs per I/O"

100 µs / 10 ns = 10,000×, which is outside the stated "hundreds to thousands" range by almost an order of magnitude. Since the video puts both figures on screen, an attentive viewer can do this division. Fix: either widen the qualitative claim ("hundreds to tens of thousands of times longer") or note that the 10 ns figure is specific to this small simulated working set fitting in CPU cache, not a generic memory-access time.

**Overstated "equally fast" given the video's own numbers** — SHOULD FIX
> "Heapsort and merge sort are both N log N sorts. If comparisons decided speed, they would run about equally fast."

The simulation two lines later reports heapsort makes ~2× merge sort's comparisons (8.6M vs 4.4M), so a comparison-only model predicts heapsort is noticeably *slower*, not "about equally fast." Fix: "If comparisons decided speed, both would still finish in a fraction of a second" — this is the actual point being set up (both are fast; only I/O separates them), and it doesn't overclaim parity.

**Unsignposted jump from GNU sort's real cap to a hypothetical fan-in** — SHOULD FIX
> "Sort itself caps a merge at sixteen runs by default, a conservative limit, and plenty for our twelve. But a big enough file needs more runs than memory has blocks. Then you need more than one merge pass. Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."

The 100,000-runs example implicitly uses the *memory-derived* fan-in (~16,000, from the "16 GB ÷ 1 MB" screen note), not sort's actual hard-coded 16. Used literally, sort's real cap of 16 would take ~5 merge passes for 100,000 runs, not 2 — a viewer who just heard "sort caps at sixteen" has no signal that the next example switches assumptions. Fix: add a bridging clause, e.g. "Sort's own limit of sixteen is a deliberate, non-memory-related choice — file descriptors, not capacity. A system that used its full capacity could fan in thousands at once. Say a file needed a hundred thousand runs..."

**Missing canonical term "fan-in"** — SHOULD FIX
> "Our file needed only twelve runs. How many could one merge take? One per block of memory, less one for the output."

This is precisely the textbook quantity usually named "fan-in" (R&G, Mehlhorn & Sanders, Vitter all use this word). The script describes the concept correctly but never names it, which will leave students unable to connect the video to the assigned reading. Fix: "...less one for the output. That number is the merge's fan-in."

**Citation needs verification before publication** — SHOULD FIX
> "Mehlhorn & Sanders, The Basic Toolbox, §5.7."

I can't confirm from memory that external/memory-hierarchy sorting sits at exactly §5.7 in that book's chapter 5 ("Sorting and Selection") — the section numbering there is easy to misremember. Fix: check the actual table of contents against the edition being cited and correct the section number if it's off; a wrong pinpoint citation is worse than a chapter-level one ("ch. 5") if unverified.

**Omission (not blocking, worth a line)** — NIT
Replacement selection (generating runs averaging ~2M rather than exactly M) is the standard next-step optimization in every source cited here and isn't mentioned even in passing. Not needed for a first correct understanding, but given the video already carries a citations end-card, a single added phrase ("real systems often make runs larger than memory itself, via replacement selection — see the readings") would close the most obvious gap for a viewer who goes to the sources.

**Everything else checks out.** I verified independently: the 12× file/memory framing (1000/86≈11.6→12) and its consistency with the simulation's exact 261,120/21,760=12; the comparison counts (4.4M ≈ N log₂N − N for N=261,120; 8.6M ≈ 2N log₂N, both textbook-consistent); the I/O counts (36,720 = 18 passes × 2×1020 blocks, exact); the derived time bar (8.6M×10ns=0.086s, 837,090×100µs=83.7s); the pass arithmetic throughout (18→5→2, and independently the 1+⌈log_{(M/B)−1}⌈N/M⌉⌉ formula reproduces both R&G's original with the stated B/N remapping and this video's own numbers); the 12-run 2-way-merge halving (12→6→3→2→1, four passes); the 100,000-run example (÷16,000→7→1); GNU coreutils sort's actual default NMERGE/batch-size of 16 and its `sortXXXXXX` temp-file naming; the Aggarwal–Vitter CACM 1988 citation and its correct scoping to the indivisibility ("whole records") model; and the PostgreSQL `EXPLAIN ANALYZE` "Sort Method: external merge  Disk: ...kB" output format. No claim of unqualified optimality, universality, or general real-system behavior beyond what's supportable was found.

VERDICT: PASS
