# Review

## BLOCKING

**Quote:** *"Our file is twelve memories long, so that makes twelve runs, in a single pass."* (Section 3)

**Problem:** Section 1 establishes "memory" visually as 160 MB against a 1 GB file — a ratio of ~6.4, not 12. The real reconciliation (that GNU sort's *effective* per-run capacity is only ~86 MB, roughly half the `-S 160M` buffer, because of per-line pointer overhead) exists only as a silent 4-second screen footnote in Section 3, never spoken. Any viewer who does the arithmetic that the video itself invited them to do in Section 1 (1 GB vs. 160 MB, drawn to scale) will get 6–7, not 12, and conclude the video's numbers don't add up. A caveat that resolves a real inconsistency but is never narrated is, functionally, an uncorrected error for anyone who doesn't freeze-frame the footnote.

**Fix:** Narrate the reconciliation explicitly, e.g.: *"Sort's buffer is 160 megabytes, but half of that goes to a pointer for every line, so each run is only about 86 megabytes of data — and a 1‑gigabyte file is twelve of those."* Or simplify by introducing the 160 MB figure in Section 1 already as "160 MB of sort buffer, about half of which becomes actual sorted data" so the twelve-runs claim in Section 3 doesn't contradict what was shown earlier.

## SHOULD FIX

**Quote:** *"Heapsort and merge sort do the same amount of comparing: N log N."*

**Problem:** This is true only up to asymptotic order. Heapsort makes roughly 2N log₂N comparisons (build-heap plus N sift-downs); merge sort makes roughly N log₂N. Saying "the same amount" (not "the same order," "the same asymptotically") teaches students that the counts are equal, when only their growth rate is.

**Fix:** *"Heapsort and merge sort both do about N log N comparisons — the same asymptotic order, though heapsort's constant is roughly twice as large."*

---

**Quote:** *"Runs, then one multiway merge: this is external merge sort."*

**Problem:** This defines "external merge sort" as specifically the two-pass case. The general algorithm is: form sorted runs, then merge runs (in one or more passes, however many the available fan-in requires) — Section 5 immediately shows multi-round merging is sometimes needed. As worded, a student would reasonably conclude "external merge sort" *means* one merge pass, which is wrong in general.

**Fix:** *"Runs, then merging them down to one — in this case a single multiway merge, since twelve runs all fit in one pass. That's external merge sort."*

---

**Quote (screen):** *"passes ≈ 1 + ⌈log_{M/B}(N/M)⌉"*

**Problem:** The merge fan-in is really M/B − 1, not M/B: one block of memory must be held back for the output buffer (this is exactly why the multiway-merge screen direction shows "one block for the output" separately from the per-run input blocks). The evidence table itself cites the two-pass condition as N ≤ B(B−1) — i.e., it does include the −1 — so the on-screen formula is inconsistent with the video's own cited source (Ramakrishnan & Gehrke).

**Fix:** Either write the base as (M/B) − 1, or add a one-line spoken/on-screen caveat: "one block of that memory is reserved for output, so the true fan-in is one less than M/B — negligible when M/B is in the thousands, but this is where that −1 in the two-pass formula on the reference slide comes from."

---

**Quote:** *"and two passes can sort hundreds of terabytes."*

**Problem:** This is a pure I/O-pass-count bound, not a claim about what a real laptop can do — a laptop is unlikely to have hundreds of terabytes of attached storage, and even if it did, two "passes" over that much data at real disk/SSD bandwidth would take a very long time. Stated flatly, it reads as a real-system performance claim.

**Fix:** *"...which means two passes are, in principle, enough I/O-wise to sort hundreds of terabytes — assuming you had that much disk attached and the time to move it."*

## NIT

- **Quote:** *"each round divides the number of runs by thousands."* — With fan-in ≈ 16,000, "tens of thousands" is more accurate than "thousands." Fix: *"...by tens of thousands each round."*

- **Quote:** *"even on a fast SSD, hundreds of times slower than memory."* — The cited figures (≈100 ns vs. 50–100 µs) span 500×–1000×, brushing against "a thousand times." Fix: *"hundreds to a thousand times slower."*

- **Quote:** *"the number of I/Os decides the running time."* — Slightly too absolute; comparisons still take nonzero time. Fix: *"...dominates the running time."*

- **Quote:** *"memory holds about twenty thousand items"* — M = 21,760; "about twenty-two thousand" rounds tighter. Doesn't affect any downstream conclusion, so low priority.

- **Quote:** *"A quarter of a million is about two to the eighteenth"* — actual N = 261,120, about 4.4% above 250,000. Consider "a bit over a quarter million" for tighter agreement with 2¹⁸ = 262,144.

- **Quote:** *"Fill memory with the start of the file, sort it right there, and write it back as one sorted piece, called a run."* — Worth a half-sentence noting that this simple method isn't the only way to form runs; replacement selection (not covered here) can produce runs averaging about twice the size of memory. Optional given time budget, but a viewer who looks further will encounter it as "the standard" technique and may wonder why the video's runs are capped at exactly M.

VERDICT: REVISE
