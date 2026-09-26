# Review

Overall this is an unusually well-sourced script — the arithmetic checks out throughout (I re-derived nearly every number: I/O and comparison counts, pass counts 18→5→2, the run-count math, the endcard formula's correspondence to Ramakrishnan & Gehrke's notation, and the Aggarwal–Vitter attribution), and the heapsort/mergesort locality argument is a legitimate, standard pedagogical device. I found no outright factual errors. My findings below are about precision, attribution, and one notable omission.

---

**SHOULD FIX** — Quote: *"Ask the Unix sort command, with the same memory, and it just finishes."*
What's wrong: The behaviors the video documents in detail — the default merge fan-in of 16 (`--batch-size`), the `sortXXXXXX` temp-file naming, the exact deletion behavior — are GNU coreutils specifics, not properties of "the Unix sort command" in general. Other implementations (BSD/macOS `sort`, illumos, etc.) are not guaranteed to behave identically. The on-screen label ("GNU coreutils sort 9.4") mitigates this, but the spoken claim generalizes past what's demonstrated.
Fix: "Ask GNU's sort command, with the same memory, and it just finishes." (and keep "GNU sort" rather than "Unix sort" at every subsequent generic mention).

**SHOULD FIX** — Quote: *"Fill memory with the start of the file, sort it right there, and write it out to disk as one sorted piece, called a run."*
What's wrong: This presents load‑sort‑write as if it were simply *the* way runs are formed. The classic technique covered in the very textbook cited at the end (Ramakrishnan & Gehrke ch. 13; also Knuth vol. 3) is replacement selection, which on average produces runs about twice the size of memory (and can exceed memory entirely on favorably-ordered input), directly changing the "twelve runs" story's generality. Presenting only the naive method as if it's the standard leaves a first-understanding gap a DB instructor would want closed.
Fix: Add one hedge sentence, e.g., "(There's a cleverer way to build runs, called replacement selection, that gets runs bigger than memory on average — we're showing the simplest version here.)"

**SHOULD FIX** — Quote: *"Real sorting programs read much bigger blocks than our simulation did, often a megabyte, to cut down on fetches"*
What's wrong: Unlike virtually every other quantitative claim in the script, this one has no supporting measurement or citation in the evidence table — it's asserted as a typical figure. Real I/O granularity for external sorts varies widely (DB pages are commonly 8–64 KB; sequential read-ahead can be much larger), so "often a megabyte" reads as more precise/settled than it is, inconsistent with the rigor shown elsewhere.
Fix: Soften to "often hundreds of kilobytes to a few megabytes" or mark it explicitly as a rough illustrative figure rather than an empirical typical value.

**NIT** — Quote: *"Heapsort and merge sort are both N log N sorts."*
What's wrong: Informal — no comparison-count qualifier or asymptotic notation. Harmless as spoken narration, but a stickler would want "Θ(N log N) comparisons."
Fix (optional): "Heapsort and merge sort both make about N log N comparisons."

**NIT** — Quote: *"Eighteen doublings take you from one item to a quarter of a million"*
What's wrong: 2¹⁸ = 262,144, about 5% above a literal "quarter of a million" (250,000). The on-screen caption shows the exact figure, so it's not misleading, just loose phrasing.
Fix (optional): "...to about a quarter of a million" — already implied by "about," so minor.

**NIT** — Quote: *"Its I/Os take more than a minute."*
What's wrong: Measured value is ≈84 s (~1 min 24 s); "more than a minute" is true but noticeably less precise than the rest of the script's number-forward style.
Fix (optional): "about a minute and a half."

---

No BLOCKING issues found — every load-bearing numerical and conceptual claim I checked (I/O and comparison counts, the 18→5→2 pass reduction, the run-count derivation, the fan-in/passes formula and its mapping to Ramakrishnan & Gehrke's B/N notation, and the Aggarwal–Vitter optimality caveat) is internally consistent and correctly attributed.

VERDICT: PASS
