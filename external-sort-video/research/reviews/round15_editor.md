# Script Notes

## 1. One question

The opening asks two things: "What are those files, and how does sort get away with it?" Both get answered — "files" explicitly in §3 ("that's what sort's twelve files were") and "how" in §6 (the two-pass summary) — but the two answers land in different sections, and the very last lines (§6) never say the word "files" again.

- **SHOULD FIX** — Quote: *"That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."*
  Rewrite: *"That's what those twelve files were, and how sort got away with it: twelve runs, one merge, two passes."* — closes the loop with the exact noun the hook used.

## 2. But/therefore chain

Segment-level chain:
1. Sort finishes a 12x-oversized file; mystery files appear and vanish.
   **but**
2. Virtual memory looks like the fix, **but** disk I/O is so expensive that access pattern beats comparison count — demonstrated on heapsort vs. merge sort.
   **therefore**
3. Since I/Os dominate, measure in passes; merge sort's early passes only combine pieces smaller than memory, **so** those pieces can be pre-sorted in memory as runs — sort's twelve files.
   **but**
4. Runs are sorted internally **but** not against each other, **so** they still need merging; two-way merging wastes memory, **so** merge all runs at once (multiway merge) — two passes total.
   **but**
5. **But** how far does this scale? — real merge widths are in the thousands, **so** even huge files take only 2-3 passes; Postgres confirms this in practice.
   **therefore**
6. **Therefore**: count I/Os, sweep sequentially, maximize run size and merge width — which is exactly what sort did.

No "and-then" joints at the segment level — the chain is causal throughout. No finding.

## 3. Derive, don't reveal

Every major idea is problem-first: I/O cost (disk fetches whole blocks), passes (I/Os decide), runs ("watch the size of the pieces… so do exactly that"), multiway merge ("the rest of memory sits idle… so give every run its own block"), the in-memory heap (scanning would be slow, so keep a heap). This is the strongest section of the script.

One idea is asserted rather than derived:

- **NIT** — Quote: *"GNU sort merges up to sixteen at a time by default, a cautious setting that trades some speed for less memory."*
  No problem is shown that this trade-off solves — the viewer can't reconstruct why a smaller merge width would ever be chosen. Rewrite: cut the clause, or derive it: *"...a conservative default, since each extra run held open costs a block of memory you might want elsewhere."*

## 4. Setups and payoffs

Nearly every setup pays off: twelve files → twelve runs (§3, §4, §6); 12x file/memory ratio → threaded through to the close; N log N claim → measured comparison/I/O race; eighteen passes → 5 → 2 tally; GNU sort default of 16 → "that was plenty for twelve"; Postgres EXPLAIN → validates the whole mechanism.

One setup never pays off:

- **NIT** — Quote: *"1 GB of 10,000-byte records vs 86 MB, labelled"* (screen direction, §1)
  The 10,000-byte figure is never used again (the simulation switches to unitless "items"). Either drop it or use it once, e.g. tie it to block size later ("blocks of 256 items" could be recast as "~2.5 MB").

## 5. One vocabulary

Terms are defined at first use and never renamed: block → I/O → pass → run → multiway merge → external merge sort, each named right after being explained. Strong.

- **SHOULD FIX** — The stated learning objective says the viewer should "say why cost is counted in **block transfers**," but the script never uses that phrase — it says "I/O" throughout. Rewrite: either change the objective to say "I/Os," or add one line syncing the terms, e.g. in §2: *"Moving one block between disk and memory is called an I/O — a block transfer."*

## 6. Number budget

The three numbers worth remembering: **12x** (file vs. memory, the whole premise), **two passes** (the punchline), and **~1000x** (I/O vs. comparison cost, the reason counting I/Os matters). These are the ones repeated and reinforced; good discipline.

- **NIT** — Quote: *"1 GB of 10,000-byte records"* — does no work (see #4).
- **SHOULD FIX** — Quote: *"Heapsort made about twice as many comparisons as merge sort, but more than twenty times as many I/Os: about three for every item it sorts."*
  Three ratios land in one breath (2x, 20x, 3-per-item). Cut the last clause or give it its own sentence/beat — it's redundant with the 20x figure and crowds the number the scene is actually selling (20x).

## 7. Concrete before abstract

Passes cleanly. The only formula in the whole piece — `passes = 1 + ⌈log_(M/B)−1⌈N/M⌉⌉` — is quarantined to the end card, after the full concrete argument (GNU sort demo → simulation → toy tray → real Postgres output). No finding.

## 8. Wrong model

Wrong model ("comparisons decide speed; virtual memory handles the disk") is named explicitly as "the obvious fix," then shown failing concretely: heapsort wins on comparisons (predicted ~2x slower, actually competitive) but loses catastrophically on wall-clock (0.86s vs. 84s) because of I/O pattern. This is a clean, textbook execution. No finding.

## 9. Depth over breadth

Only one applied example (Postgres) is used, and it's shown working (real EXPLAIN ANALYZE output), not just name-dropped. No list of unexamined applications. No finding.

## 10. Words and pictures

Mostly complementary (numeric tallies reinforce spoken counts rather than restating sentences). One spot is a near-verbatim duplicate:

- **NIT** — Quote (screen direction): *"GNU sort: at most 16 runs per merge, by default"* beside narration *"GNU sort merges up to sixteen at a time by default."*
  Rewrite screen text to a number/diagram only, e.g. "≤16 runs/merge," or show the block-slot diagram instead of a restated sentence.

## 11. Deletion test

- **NIT** — *"a cautious setting that trades some speed for less memory"* (§5) — cuttable; nothing downstream depends on it (see #3).
- **NIT** — *"Then do the same with the next part of the file, and the next."* (§3) — could be trimmed to "...and repeat" without loss.

Everything else earns its place — even the seemingly small aside "Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time" is doing real work (it's the payoff of the earlier heapsort-heap comparison).

## 12. For the ear and pacing

- **SHOULD FIX** — Quote: *"So each extra merge pass lets the file grow by that same factor of sixteen thousand."*
  Awkward to parse by ear (what "grows," by what factor, is ambiguous mid-sentence). Rewrite: *"So each extra pass multiplies the file size you can handle by sixteen thousand."*
- **SHOULD FIX** — The §2 sentence bundling three ratios (2x comparisons / 20x I/Os / 3-per-item) is a rushed beat — the ear needs a break between "the wrong-model number" (2x) and "the right number" (20x). Split into two sentences with a beat (cut) between them.
- **NIT** — §4's mechanism run ("keep a small heap… Unlike heapsort's heap… Say run three has the smallest front item… When the output fills… When run three runs dry…") stacks four new mechanical facts with no pause. Consider a half-second hold on the heap diagram before the worked example starts.

---

VERDICT: PASS
