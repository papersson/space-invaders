# Script Review

## 1. One question
**PASS.** Opening: "What are those files, and how does sort get away with it?" Section 6 closes with an explicit callback: "a file about twelve times bigger than its memory: twelve runs, one merge, two passes" — same numbers, same framing.

- NIT: the actual reveal ("that's what sort's twelve files were") happens in section 3, and the "how it gets away with it" (deletion) happens in section 4. Section 6 is a recap, not a reveal, so the ending's emotional payoff is muted by the time it arrives. Not a fix, just a pacing tradeoff worth being aware of.

## 2. But/therefore chain
Chain mostly holds (§1→§4 read as one but/therefore spine). Two breaks:

- **SHOULD FIX** — "Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time." This is inserted mid-derivation of the multiway-merge heap with no connective; it's a valuable callback but reads as an aside dropped into the chain.
  Rewrite: fold it into the "so" clause — "...so keep a small heap with one entry per run — but unlike heapsort's heap, which lived on disk a block at a time, this one is small enough to sit in memory the whole time."

- **SHOULD FIX** — "In practice, even enormous files sort in two or three passes. That's why databases sort this way." The jump from "few passes" to "databases use it" is an *and then*, not a therefore — nothing established why fewness-of-passes is what databases specifically need.
  Rewrite: "...even enormous files sort in two or three passes — cheap enough that any system with more data than memory, a database included, can afford it. Ask PostgreSQL..."

## 3. Derive, don't reveal
Strong overall — runs and multiway merge are the model derivations in the script. One real problem:

- **BLOCKING** — "Sort itself caps a merge at sixteen runs by default, a conservative limit, and plenty for our twelve." This is announced as a bare fact, and it contradicts the just-taught rule ("merge as many runs at once as memory allows") without explanation — the tray visual moments earlier showed thousands of blocks fitting in memory. A viewer paying attention will ask "then why only sixteen?" and the script never answers it, which undercuts trust in the rule itself.
  Rewrite: give it one clause of reason — "Sort itself defaults to merging only sixteen runs at a time — real memory has other jobs too, so implementations leave themselves headroom rather than spend it all on one merge — plenty for our twelve." Or cut the cap entirely and just say sort had room for all twelve at once.

## 4. Setups and payoffs
Well-built — twelve files/twelve runs, 18→5→2 passes, and the heapsort-heap callback all pay off cleanly across sections.

- Same issue as #3 recurs here as an unpaid setup: "sixteen" is set up twice (narration + on-screen "--batch-size") but never resolved against the "merge as many as memory allows" rule. One fix covers both findings.
- No orphaned payoffs found.

## 5. One vocabulary
Clean. I/O, block, pass, run, and multiway merge are each named right after being described, never before. External merge sort is named only once the full mechanism is built. The textbook's alternate B/M/N notation is confined to the (unnarrated) end card, so it never collides with the video's own terms.

- NIT: "virtual memory" gets no technical definition, only a functional one. Fine given it's being retired as the wrong model, not built as a tool — no fix needed.

## 6. Number budget
The three numbers worth remembering: **twelve** (files=runs, tied to the file/memory ratio), the pass sequence **18 → 5 → 2**, and the I/O-vs-comparison time gap (**fraction of a second vs. over a minute**). These recur and are reinforced well.

Numbers doing no real work:
- **NIT** — "10,000-byte records" (on-screen only, §1): never reused in any later calculation. Cut it, or connect it to block size later to earn its place.
- **NIT** — "107696kB" (Postgres EXPLAIN line, §5): pure flavor/authenticity, not meant to be remembered — fine to keep but don't linger on it.
- **NIT** — "256 items per block" (simulation caption): screen-only detail that never resurfaces; harmless but could be dropped.

## 7. Concrete before abstract
Generally good — the end-card formula is explicitly deferred to silent reference material, which is exactly right.

- **SHOULD FIX** — In §4, the heap mechanism is stated abstractly first, then illustrated: "...keep a small heap with one entry per run. Unlike heapsort's heap... Say run three's front item is the smallest..." The general claim precedes the concrete walkthrough, inverting the script's own principle.
  Rewrite: lead with the concrete case — "Say run three's front item is currently the smallest of all twelve fronts: it goes to the output block next. To find that smallest item quickly among thousands of runs, keep a small heap with one entry per run..."

## 8. Wrong model
**PASS.** "If comparisons decided speed, they would run about equally fast" is stated as the prediction of the wrong model, then explicitly falsified by the timed race (0.09s of comparisons vs. minutes of I/O). This is the strongest part of the script.

## 9. Depth over breadth
**PASS.** Only one running example (the file / GNU sort / the simulation) carries the whole video; PostgreSQL appears once as corroborating evidence, not as a list of "also used by X, Y, Z." No breadth-without-understanding problem.

## 10. Words and pictures
- **SHOULD FIX** — "1,000 MB ÷ 86 MB ≈ 11.6, so 12 runs" appears on screen at almost the exact moment the narration says "Our file is twelve memories long, so this makes twelve runs." This is the video's central "aha," and having the caption state the conclusion in words at the same time as the narrator flattens it.
  Rewrite: trim the caption to just the arithmetic — "1,000 MB ÷ 86 MB ≈ 11.6" — and let the narration alone deliver "so this makes twelve runs."
- NIT: "N log N" labeled on screen under both algorithm names at the same instant the narrator says "both N log N sorts" is a mild duplication, though defensible as a chyron/label rather than prose repetition.

## 11. Deletion test
- **SHOULD FIX** — "Real sorting programs read much bigger blocks than our simulation did, often a megabyte, to cut down on fetches, and a laptop's memory still holds thousands of those." Removable without weakening anything downstream; it's calibration trivia that also feeds the unresolved "why cap at 16" tension (#3). Cut it or fold its one useful fact (blocks are bigger in practice) into the sixteen-cap fix.
- NIT: the PostgreSQL sentence is technically removable (the takeaway doesn't depend on it) but earns its place by broadening relevance beyond one Unix tool — keep it, don't cut.

## 12. For the ear and pacing
- **SHOULD FIX** — "We simulated both under virtual memory, on a quarter of a million items, with memory for a twelfth of them, roughly the same proportions as sort's file." Three clauses stacked in one breath; hard to track by ear on first listen.
  Rewrite: "We simulated both under virtual memory. A quarter of a million items, memory for a twelfth of them — the same proportions as sort's file."
- **NIT** — "Each extra pass lets the file be thousands of times bigger" is compressed enough to require a re-listen.
  Rewrite: "So each extra pass buys a factor of thousands in file size."
- **SHOULD FIX (pacing)** — §4's heap mechanism (new concept, new data structure use, new vocabulary) is dispatched in about four sentences with a single worked example, the densest beat in the script for an audience that hasn't seen heaps used this way. Consider one more beat: hold on the "run three's front item" example a moment longer before generalizing to "every block is still read once and written once."

---

VERDICT: REVISE
