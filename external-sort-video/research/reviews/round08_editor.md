# Script Review

## 1. One question

The opening asks a tight, two-faced question ("what are those files, and how does sort get away with it?") and both faces get answered — the files explicitly at the end of §3 ("that's what sort's twelve files were"), the mechanism recapped in §6 ("twelve runs, one merge, two passes"). The callback to "twelve times bigger" is explicit.

- **NIT** — The ending never re-uses the words "get away with it," so the callback is thematic, not verbatim. Quote: *"That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."* Rewrite: *"That's how sort got away with it: twelve runs, one merge, two passes — on a file twelve times bigger than its memory."*

## 2. But/therefore chain

Macro chain (one sentence per beat), joined:

Python OOMs on a 12×-memory file, **but** sort finishes, leaving twelve vanishing files unexplained. **Therefore** try the obvious fix — virtual memory — **but** disks fetch whole costly blocks, so I/O count dominates once data exceeds memory. **Therefore** test it: heapsort and merge sort, simulated under VM — heapsort has slightly more comparisons **but** vastly more I/Os, **because** its access is scattered while merge sort's is sequential. **Therefore** merge sort is the base, measured in passes. Plain merge sort needs 18 passes, **but** the first 14 passes' pieces already fit in memory, **so** sort them in place as "runs," cutting 18→5 — and that's the twelve files. The runs are sorted **but** unmerged; naive two-way merging wastes memory, **so** give every run a block and merge all at once, cutting 5→2 — external merge sort, exactly what sort did. Twelve runs was easy, **but** how far does this scale — one run per memory block, thousands available, **so** sort's 16-run cap is generous; a huge file needs more runs than blocks, **so** it needs extra passes, **but** each pass divides run count by thousands, **so** even vast files need 2-3 passes — which is why databases use this too. **Therefore**: count I/Os not comparisons, work sequentially, cut passes with big runs and wide merges.

The chain holds almost entirely on but/therefore — this is a strength of the script.

- **NIT** — *"And that's what sort's twelve files were."* The connector is a bare "And" standing in for what is actually a payoff/therefore. Rewrite: *"So that's what sort's twelve files were."*
- **NIT** — *"Sorting programs read runs in big blocks, often a megabyte, to cut down on fetches, and a laptop's memory still holds thousands of those."* Two separate facts glued by "and" rather than a causal link. Rewrite: split into two sentences: *"Sorting programs read runs in big blocks — often a megabyte — to cut down on fetches. A laptop's memory still holds thousands of those blocks."*

## 3. Derive, don't reveal

Most ideas are properly derived: I/O (shown right after the block-fetch problem), runs (derived from noticing 14 of 18 passes are sub-memory-size), multiway merge (derived from watching idle memory in a two-way merge), the merge heap (derived from the scanning-cost problem at scale). This is the script's strongest test result.

- **SHOULD FIX** — The heapsort-vs-mergesort comparison reveals the result before the mechanism: *"Heapsort made about twice as many comparisons as merge sort, and more than twenty times as many I/Os. Heapsort compares items that sit far apart in its array..."* The number arrives before the viewer has any way to predict it. (The screen direction actually shows the far-apart-access image *before* the race, so narration and picture are out of sync here — see also Test 10.) Rewrite: state the mechanism first, then let the numbers confirm it: *"Heapsort compares items that sit far apart in its array — under virtual memory, that array lives on disk, so every comparison risks a fresh block. Merge sort never leaves the block it's already reading. We simulated both... heapsort made only about twice as many comparisons as merge sort, but more than twenty times as many I/Os."*

## 4. Setups and payoffs

| Setup | Payoff |
|---|---|
| File 12× memory, /tmp files appear/vanish (§1) | Twelve runs named (§3), files vanish on screen (§4), recap (§6) |
| Python OOM (§1) | "Python tried to hold the whole file in memory at once" (§6) |
| Virtual memory "obvious fix" (§2) | Shown failing in the same section |
| Heapsort's heap-over-whole-file (§2) | Explicitly contrasted with the merge heap (§4) |
| "Pass" defined (§2) | Used as the running currency (18→5→2) through the end |
| 18 doublings / 18 passes (§3) | Reduced to 5 (§3), then 2 (§4) |
| Sixteen-run merge cap (§5) | "Plenty for twelve" — immediate payoff |

- **SHOULD FIX** — Payoff with no setup: the end card asserts *"optimal for sorts that move items as indivisible units"* — a claim and a piece of jargon ("indivisible units") that nothing in the narrated video prepares. Since it's reference-only text, either cut it or gloss it in one clause: *"optimal among sorts that move whole records at a time (Aggarwal & Vitter, 1988)."*
- **NIT** — Setup with thin payoff: the simulation's block size ("blocks of 256 items," §2 caption) is never reconciled with the real-world block size used later ("often a megabyte," §5). A viewer may think these are the same unit. Rewrite (§5 narration): *"Real sorting programs use much bigger blocks than our toy simulation did — often a megabyte — so a laptop's memory still holds thousands of them."*

## 5. One vocabulary

Terms are cleanly defined at first use and not renamed: **virtual memory**, **block**, **I/O**, **pass**, **run**, **multiway merge**, **external merge sort**. The reused term **heap** (heapsort's heap vs. the merge heap) is explicitly disambiguated on-screen ("unlike heapsort's heap, which was the whole file...") — good practice, not a violation.

- **NIT** — The stated learning objective says viewers should "say why cost is counted in **block transfers**," but the script only ever says **I/O**. Not a script-internal problem, but worth reconciling the objectives doc's wording with the script's actual term.

## 6. Number budget

Roughly 20 numbers appear. The two/three that should stick: **12** (the ratio/files/runs, present at open and close), **2** (final pass count — the payoff), and arguably **2–3** (passes even for enormous files — the generalization). Everything else is supporting evidence, appropriately kept off narration and pushed to captions per the review log's fix (rounded speech, exact screen text).

- **NIT** — Numbers doing no conceptual work: *"GNU coreutils sort 9.4"* and the Postgres caption *"Disk: 107696kB"* are flavor/authenticity only. Fine to keep as captions since they're not narrated, but if trimming for pacing, cut first.
- **NIT** — Minor spoken/caption mismatch: narration says *"about three I/Os for every item"* while the caption reads *"3.2."* Harmless rounding, but pick one framing consistently (either round both or state "about three, precisely 3.2" once).

## 7. Concrete before abstract

Clean. The formula, and the term "external merge sort," both arrive only after the concrete mechanism is fully built. The end-card formula is explicitly deferred to reference material. No violations found.

## 8. Wrong model

Wrong model: *"comparison counts decide speed, and virtual memory takes care of the disk."*

The VM half is dislodged cleanly (§2: disks fetch whole blocks, hundreds-to-thousands times slower, I/O dominates).

- **BLOCKING** — The "comparisons decide speed" half is not actually shown failing. Quote: *"Heapsort made about twice as many comparisons as merge sort, and more than twenty times as many I/Os."* Heapsort is worse on **both** metrics, so a viewer holding the wrong model can simply conclude "heapsort is just a worse algorithm here" — nothing forces them to notice that I/O, not comparisons, is what's driving the outcome, since no running time is ever stated to show that speed tracks the 20× gap rather than the 2× gap. (The review log claims an "equal-comparisons line" was added to make this disproof airtight — it isn't present in this draft; this looks like a dropped fix.) Rewrite: *"Heapsort and merge sort are both N log N — if comparisons decided speed, they'd run close to the same. We simulated both under virtual memory... Heapsort made only about twice as many comparisons as merge sort. But it made more than twenty times as many I/Os — and that gap, not the comparisons, is what decides which one finishes first."*

## 9. Depth over breadth

No violation. The one named external example (PostgreSQL) is shown concretely with a real `EXPLAIN ANALYZE` line rather than dropped as an unexplained name in a list.

## 10. Words and pictures

- **SHOULD FIX** — Narration/screen order mismatch in §2: the screen shows the mechanism first (far-apart array access), *then* the race with counters; the narration states the result numbers first, then explains the mechanism. Align narration order to screen order (see Test 3 rewrite).
- **SHOULD FIX** — §6's end card text duplicates the spoken takeaway almost verbatim ("count I/Os, not comparisons... work in passes... cut the passes...") while the narrator says the same three sentences aloud. This is the clearest text/speech redundancy in the script. Rewrite: replace the on-screen bullet text with the visual payoff instead — e.g., the pass-count timeline **18 → 5 → 2** overlaid on the reused file/memory bars from the opening — and let the narration carry the words alone.
- **NIT** — §5's on-screen caption *"GNU sort: at most 16 per merge (--batch-size)"* closely echoes the narrated line *"Sort itself caps a merge at sixteen runs by default"* — a mild but forgivable duplication (reinforcing one real number is defensible).

## 11. Deletion test

- **NIT** — *"Sorting programs read runs in big blocks, often a megabyte, to cut down on fetches, and a laptop's memory still holds thousands of those."* Supports "how far it goes" but the core takeaway is already delivered by end of §4; a tightening pass could compress this.
- **NIT** — *"That's why databases sort this way. Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."* Nice real-world grounding, but nothing later depends on it and the takeaway doesn't need it — a solid candidate to trim if the 750-word budget gets tight.
- Nothing else in §1–4 is safely cuttable; each line sets up a later payoff (see Test 4).

## 12. For the ear and pacing

- **SHOULD FIX** — Rushed logical leap in §5: *"But a big enough file needs more runs than memory has blocks. Then you need more than one merge pass, but each merge pass divides the number of runs by thousands. So thousands of times more data costs just one more pass."* Four abstract clauses back-to-back with no concrete anchor. Rewrite: *"Say you had twelve thousand runs instead of twelve. One pass merges them down to a dozen. One more pass, and they're one file. That's why thousands of times more data costs just one more pass."*
- **NIT** — Comma-stacked sentence, awkward to read aloud: *"Sort itself caps a merge at sixteen runs by default, a conservative limit far below that, and plenty for twelve."* Rewrite: *"Sort itself caps a merge at sixteen runs by default — a conservative limit, and plenty for our twelve."*
- **NIT** — Three clipped "when/say" clauses in a row in §4 (*"Say run three's front item is the smallest... When the output block fills... When run three's block runs dry..."*) read like a procedural list; fine with the toy-tray animation carrying it, but worth a beat of air between clauses when recorded.

---

VERDICT: REVISE
