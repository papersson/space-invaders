# Script Review

## 1. One question

**Mostly holds.** The opening asks two things: *what are the files* and *how does sort get away with it*. "What are the files" is explicitly closed in §3 ("And that's what sort's twelve files were"). "How" is closed in §6 ("twelve runs, one merge, two passes"), and the screen direction replays the opening capture. But the final line drops the word "files," so the very last beat doesn't say the two halves of the question together.

- **SHOULD FIX** — Quote: *"That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."*
  Rewrite: *"That's how sort handled a file about twelve times bigger than its memory: those twelve files were runs, merged all at once, in two passes total."*

## 2. But/therefore chain

Section-level chain (mostly holds together):

> Sort finishes, Python doesn't, twelve files vanish — **therefore** try virtual memory — **but** disks move whole blocks, so I/Os dominate — **therefore** test it: heapsort vs. merge sort do similar comparisons **but** wildly different I/Os — **therefore** I/Os decide, measure in passes — **but** 14 of 18 passes just make memory-sized pieces, and merging doesn't care how they got sorted — **therefore** pre-sort each piece as a "run," cutting 18 passes to 5 — **therefore** merge the runs, **but** pairwise merging leaves memory idle — **therefore** give every run a block and merge all at once — **but** scanning every front would be slow — **therefore** keep a small heap of fronts, folding 18 passes to 2 — **therefore** that's external merge sort, and databases use it — **therefore** count I/Os, not comparisons.

Only two joins are genuine "and then"s rather than causal:

- **NIT** — Quote: *"And that's what sort's twelve files were. It filled its memory twelve times, and wrote out twelve runs."* This is a payoff restatement, not a new beat — fine as is, flagging only because it's literally an "and."
- **SHOULD FIX** — Quote: *"Real sorting programs read much bigger blocks than our simulation did, often a megabyte, to cut down on fetches, and a laptop's memory still holds thousands of those."* This is additive, not causal, and sits right before a "but" that actually undercuts it (GNU sort doesn't use those thousands). Rewrite: *"Real sorting programs use much bigger blocks — often a megabyte — so a laptop's memory can hold thousands of them. But GNU sort doesn't use all of that:"* (then continue into the existing sixteen-runs sentence).

## 3. Derive, don't reveal

Strong overall — I/O, pass, run, multiway merge, and the fronts-heap are all preceded by a visible problem (idle memory, slow scanning, wasted passes) before being named. One exception:

- **SHOULD FIX** — Quote: *"GNU sort is more cautious by default: it merges at most sixteen runs at a time, trading some speed for less memory."* This is announced, not derived — "trading... for less memory" isn't obviously true given the immediately preceding claim that memory holds thousands of blocks anyway. It reads as a fact dropped in rather than a consequence shown.
  Rewrite: *"GNU sort doesn't use all of that. By default it caps each merge at sixteen runs — far below what memory could hold — so a single sort never claims more memory than that, whatever else is running on the machine."*

## 4. Setups and payoffs

All major setups pay off: twelve files → twelve runs (§3) → "sort did exactly this" (§4); idle memory in two-way merge (§4) → multiway merge; N log N parity (§2) → race disproves it; 18 passes (§3) → 5 → 2 (§4) → recap (§6); file/memory bars (§1) → return in §6.

No orphaned setups found, and no unearned payoffs — even the PostgreSQL beat is self-contained (introduced and resolved in the same breath). This test passes cleanly.

## 5. One vocabulary

Terms are consistently defined at first use (I/O, block, pass, run, multiway merge, external merge sort all get a definition in the same sentence they're introduced). One collision:

- **SHOULD FIX** — "Heap" is used for two different structures: heapsort's array-as-heap (§2) and the small in-memory selection structure over run-fronts (§4). The script does add a disambiguating clause, but it trails the term instead of leading it.
  Quote: *"...so keep a small heap with one entry per run. Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time."*
  Rewrite: *"...so keep a small structure — a heap, but a tiny one: just one entry per run, not the whole file the way heapsort's heap was."* (disambiguate before the reader has to hold the wrong image for a sentence.)

## 6. Number budget

The three numbers worth remembering: **12** (files = runs, the throughline), **18 → 2** (the pass reduction, the actual result), and the I/O-vs-comparison cost gap (**0.09s vs 84s**, the reason the wrong model fails). Everything else is in service of these.

Numbers doing little work, mostly decorative screen captions:
- **NIT** — "10,000-byte records" (§1 screen) — never referenced again, pure flavor.
- **NIT** — "8.6M vs 4.4M comparisons" and "837,090 vs 36,720 I/Os" (§2 screen) — redundant with the spoken "twice as many / twenty times as many"; the raw digits add rigor-signaling but no new understanding.

One collision that risks real confusion:
- **SHOULD FIX** — "sixteen" (GNU sort's per-merge cap) and "sixteen thousand" (§5's "16 GB ÷ 1 MB ≈ 16,000 blocks") appear within a few sentences of each other with very different meanings. Round 1 already flagged "fewer sixteens" — this pair slipped through.
  Rewrite: state the cap once, then explicitly contrast the scale: *"...merges at most sixteen runs at a time — a small fraction of the thousands of blocks a modern machine could actually hold."*

## 7. Concrete before abstract

No violations. The end-card formula is correctly deferred to a silent, unnarrated reference card after every concrete step has already been walked through. N log N is invoked only as known background, not taught fresh. This test passes cleanly.

## 8. Wrong model

Wrong model — "comparisons decide speed, virtual memory handles the disk" — is stated (§2 opening) and then shown failing concretely: same-order comparisons, 20x+ I/Os, and a real time bar (0.09s vs 84s) that makes the failure undeniable. This is the strongest section of the script; no finding.

## 9. Depth over breadth

Only one external example (PostgreSQL), and it's given real depth — an actual `EXPLAIN ANALYZE` line, not a name-drop. No laundry list of "also used in search engines, MapReduce, etc." No finding.

## 10. Words and pictures

- **NIT** — Quote (screen, §5): *"GNU sort: at most 16 per merge (--batch-size)"* nearly duplicates the spoken line word-for-word (*"it merges at most sixteen runs at a time"*). Rewrite the caption to carry information the voice doesn't: a bar showing 16 blocks lit against thousands greyed out, labelled only `--batch-size=16`.

Elsewhere (§6's "no rule text" choice, the "1+4" / "1+1" pass-tally captions) the script actively avoids duplication and uses the screen to add arithmetic the voice doesn't spell out — good practice.

## 11. Deletion test

- **NIT** — "GNU coreutils sort 9.4" screen label (§1) — cuttable, does no narrative work.
- **NIT** — The detailed digit-dump captions in §2 (8.6M/4.4M, 837,090/36,720) could be cut or simplified to just the ratios already spoken, with no loss.
- The end-card formula/citations are, by design, fully deletable without weakening anything upstream — correctly scoped as bonus material, not a flaw.

No narration lines were found doing nothing — the script is lean; most candidates for cutting live in the screen directions, not the voice track.

## 12. For the ear and pacing

- **SHOULD FIX** — Quote: *"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."* One long breath, three clauses stacked on colons/commas. Rewrite: *"The obvious fix is virtual memory. Treat the disk as extra memory, and let the operating system keep recently used parts in memory, fetching the rest from disk as needed."*
- **SHOULD FIX** — Quote: *"Heapsort made about twice as many comparisons as merge sort, but more than twenty times as many I/Os: about three for every item it sorts."* Three numeric claims in one breath. Rewrite: *"Heapsort made about twice as many comparisons as merge sort. But it made more than twenty times as many I/Os — about three for every item it sorts."*
- **SHOULD FIX** — Quote: *"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."* This is a rushed beat — round 1 fixed exactly this kind of unmotivated jump elsewhere ("every number now carries its reason") but missed this one; by ear, "a hundred thousand" to "seven" has no audible bridge. Rewrite: *"Say a file needed a hundred thousand runs — far more than the thousands of blocks memory holds. One merge pass, using every block, cuts that down to about seven runs. One more pass finishes the job."*
- **NIT** — Quote: *"One per block of memory, less one for the output."* Terse enough to misparse by ear (one *what*?). Rewrite: *"One run per block of memory, minus one block held back for the output."*

---

**VERDICT: PASS**

The structure is sound — one clear question, an explicit derivation for every new idea, the wrong model is confronted and shown failing with real numbers, and setups consistently pay off. Findings are all SHOULD FIX/NIT: tighten the closing line's callback to "files," disambiguate the reused "heap," fix the sixteen/sixteen-thousand collision, and slow down two rushed number beats.
