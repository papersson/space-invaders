## Review

**Overall**: This is a careful, well-sourced script — nearly every number I checked against the evidence table reconciles correctly (comparison/I/O ratios, pass counts, the end-card formula against Ramakrishnan & Gehrke's own notation, the PostgreSQL and coreutils facts). The issues below are the ones I'd actually stop the recording for.

---

**BLOCKING**

- Quote: *"optimal among sorts that move whole records at a time: Aggarwal & Vitter, CACM 1988"* (end card)
 What's wrong: Aggarwal–Vitter prove a Θ(·) **lower bound** on I/Os under what the literature calls the *indivisibility assumption*, and multiway merge sort with maximal fan-in **matches it up to constant factors** — it is *asymptotically* optimal, not optimal in an unqualified sense. An end card is exactly the kind of citation students screenshot and repeat, so bare "optimal" overstates the result in a way a professor would mark down (this is precisely the "overstated optimality" failure mode to guard against).
 Fix: *"asymptotically optimal (matches the lower bound up to constant factors) among sorts that treat records as indivisible units — Aggarwal & Vitter, CACM 1988."*

---

**SHOULD FIX**

- Quote: *"Our file is twelve memories long, so this makes twelve runs, in a single pass."*
 What's wrong: At this point the narration is (correctly, if you track the surrounding numbers) talking about the *simulation* (261,120 items ÷ 21,760 = exactly 12), but nothing in the spoken line signals that — it lands right after other real-demo material and right before "And that's what **sort's** twelve files were." The real captured file is only ≈11.6 memories, not 12 (rightly shown as "≈ 11.6, so 12 runs" on screen). A viewer going only by narration will come away thinking sort's actual file was exactly 12× memory.
 Fix: *"Our simulated file is exactly twelve memories long, so this makes twelve runs, in a single pass."* — and re-anchor the following sentence with something like "Back in the real recording, sort's twelve files were the same idea…".

- Quote: *"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."*
 What's wrong: This reads as "remaining passes = 18 − 14," but that isn't a valid general derivation — the true remaining count is ⌈log₂(number of runs)⌉ = ⌈log₂ 12⌉ = 4, a separate computation that only coincides with 18−14 for this specific N and M. Counterexample: N=200, M=100 → naive doubling needs ⌈log₂200⌉=8 passes, the first ⌊log₂100⌋=6 produce pieces ≤ memory, so this style of reasoning predicts 1+(8−6)=3 total passes — but the true optimum is 1 run-creation pass + ⌈log₂⌈200/100⌉⌉=1 merge pass = **2**. The script's answer (5) is correct for *its* numbers, but the justification given doesn't generalize and shouldn't be presented as if it were the reason.
 Fix: Derive the "four" from the run count, not from subtraction: *"Twelve runs need ⌈log₂12⌉ = 4 more two-way merge passes. Add the pass that made the runs: eighteen passes become five."*

- Quote: *"When run three runs dry, its next block comes in from disk."*
 What's wrong: "runs dry" reads as "run three is entirely exhausted" (a one-time event at the end), but the intended meaning is that run three's *currently buffered block* is used up — which happens repeatedly, once per block, throughout the merge.
 Fix: *"When run three's buffered block empties, its next block comes in from disk."*

- Quote: *"So give every run its own block of memory, and merge them all at once… One per block of memory, less one for the output."*
 What's wrong: The script fully describes fan-in (max runs merged at once = memory blocks − 1) in two places and even builds the end-card formula around it, but never names it, even though "fan-in" is the standard term in the cited Ramakrishnan & Gehrke chapter for exactly this quantity. This makes it harder for a student to connect the video to the textbook they're pointed to.
 Fix: Add one naming line, e.g. *"That number — one block per run, less one for output — is called the merge's fan-in."*

---

**NIT**

- Quote: *"Heapsort and merge sort are both N log N sorts."*
 Informal shorthand for Θ(N log N) worst-case time/comparisons. Fine for a video, but consider *"both run in Θ(N log N) time"* for precision.

- Quote: *"on a quarter of a million items"*
 N = 261,120 is ~4.4% above 250,000. Harmless, but *"roughly a quarter of a million"* or *"about 260,000"* would be tighter.

---

VERDICT: REVISE
