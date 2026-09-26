# Script Review

Overall this is an unusually well-built script — the core derivation (runs → multiway merge → two passes) is genuinely earned, not announced, and the wrong model is shown failing with real numbers. Findings below are mostly SHOULD FIX/NIT polish; I did not find anything that breaks the argument.

## 1. One question
**Pass, with a nit.** The opening asks two things ("what are those files, and how does sort get away with it?"); the ending answers both ("twelve runs, one merge, two passes"), and the files=runs equation is paid off explicitly in §3–4. 

- **NIT** — The final line answers with "runs," not "files." A viewer who's been holding "files" in mind since the cold open gets no final use of that word.
  > "That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."
  **Rewrite:** "That's how sort handled a file about twelve times bigger than its memory: those twelve files were twelve runs, merged once, in two passes total."

## 2. But/therefore chain
Chain holds section-to-section: question →(but)→ virtual memory fails →(therefore)→ measure in passes →(therefore)→ runs discovered →(therefore)→ multiway merge discovered →(weak link)→ generalization →(therefore)→ rule. One real seam:

- **SHOULD FIX** — The turn into §5 is late. The section opens by re-confirming things worked ("That was plenty for twelve"), and only *after* two more sentences does it ask the actual pivoting question.
  > "Our file needed only twelve runs, and GNU sort merges up to sixteen at a time by default, a cautious setting that trades some speed for less memory. That was plenty for twelve. But how many runs could one merge take?"
  **Rewrite:** Lead with the "but": "But we got lucky: twelve runs fit in one merge. What if a file needed more runs than memory has blocks for?" — then fold in the GNU-sort-16 fact as the answer's first data point.

- **NIT** — §2 ends "let's measure it in passes," and §3 opens by just re-describing merge sort's mechanics with no connective. It reads as a restart rather than a continuation.
  > "So merge sort is our starting point... let's measure it in passes." / "Merge sort merges single items into pairs, then pairs into fours..."
  **Rewrite:** Open §3 with "So watch what a pass actually costs: merge sort merges single items into pairs, then pairs into fours..."

## 3. Derive, don't reveal
**Strong — this is the script's best feature.** Runs are derived from noticing pass 1–14 pieces are sub-memory-sized; multiway merge is derived from noticing idle memory during a 2-way merge; the run-heap is derived from "scanning every front would be slow." No ideas are announced ahead of their motivating problem.

## 4. Setups and payoffs
- Twelve files (§1) → paid off as runs (§3, §4). ✅
- Python OOM vs sort finishing (§1) → paid off (§6). ✅
- Simulation params (261,120 items / 21,760 memory) → reused consistently through §3. ✅
- Heapsort's heap → contrasted with multiway merge's heap (§4). ✅

- **SHOULD FIX** — dangling setup, no payoff:
  > "GNU sort merges up to sixteen at a time by default, **a cautious setting that trades some speed for less memory.**"
  This implies a tradeoff (why not merge wider = faster?) but never resolves it, leaving a live question hanging right before the video's generalizing move.
  **Rewrite:** Either cut the clause, or resolve it: "...merges up to sixteen at a time by default — it keeps one block of overhead per run small, at the cost of needing an extra pass sooner on huge inputs."

## 5. One vocabulary
Terms are defined at first use throughout (I/O, block, pass, run, multiway merge, external merge sort). 

- **NIT** — "heap" is reused for two different-sized structures (heapsort's heap = the whole file; the merge's heap = one entry per run). The script does disambiguate it in-line ("Unlike heapsort's heap, which was the whole file..."), so it's handled, but it's still asking the ear to hold two meanings of the same word back to back.
  **Rewrite (optional):** Call the merge structure a "run-selector" or "tournament" on first mention, then note "some call this a heap too, but a tiny one that never leaves memory."

## 6. Number budget
Numbers to remember: **twelve** (runs, and the file/memory ratio), **two** (final pass count), and the **~1000x gap** between memory access and an I/O (100 ns vs 100 µs) — that gap is *why* the whole argument works.

- **SHOULD FIX** — screen shows far more precision than narration uses, risking a mismatch that reads as noise:
  > Narration: "more than twenty times as many I/Os: about three for every item." Screen: "837,090 vs 36,720."
  **Fix:** Either round the on-screen numbers to match the spoken ratios, or keep exact figures but caption them "(exact count)" so the mismatch reads as intentional rigor, not clutter.

- **NIT** — "10,000-byte records" (screen only) does no work anywhere later.
  **Fix:** Cut it, or replace with something that pays off (e.g., use it to justify the 1 GB / 86 MB figures on screen).

## 7. Concrete before abstract
Clean ordering throughout — the end-card formula and the Aggarwal & Vitter optimality claim both arrive only after every mechanism has been built concretely, and are explicitly marked "for reference." No violations.

## 8. Wrong model
Confronted directly ("comparison counts decide speed, and virtual memory takes care of the disk") and shown failing concretely: heapsort has *fewer* extra comparisons than expected penalty but *20x* the I/Os, with an actual timing race (0.86s vs 84s) proving I/O dominates. This is a clean pass.

## 9. Depth over breadth
No violation — only one real-world application is cited (PostgreSQL), and it's backed by an actual EXPLAIN ANALYZE artifact rather than just named and dropped.

## 10. Words and pictures
- **SHOULD FIX** — on-screen text repeats the spoken line almost verbatim instead of showing the mechanism:
  > Narration: "GNU sort merges up to sixteen at a time by default..." Screen: *"GNU sort: at most 16 runs per merge, by default"*
  **Rewrite (screen direction):** Show it, don't caption it — sixteen slots with twelve lit and four empty, no text, so the "plenty of headroom" point lands visually instead of being read twice.

- Elsewhere (pass tallies "1 + 4", "1 + 1") the on-screen text adds a visual proof form rather than repeating words — that's fine, not a violation.
- §6's screen direction explicitly drops rule text because "the narration carries the words" — good practice, worth keeping as the model for the fix above.

## 11. Deletion test
- The "10,000-byte records" detail (§1, screen) — cuttable, does nothing later.
- The "cautious setting that trades some speed for less memory" aside (§5) — as currently unresolved, cuttable (see §4 finding); better to resolve than delete.
- The PostgreSQL beat (§5) is technically cuttable without breaking the core argument, but it's doing real work for the "this generalizes beyond `sort`" objective — keep it; flagged only so you know it's the one truly optional beat in the video.

## 12. For the ear and pacing
- **SHOULD FIX — rushed beat.** The multiway-merge mechanics land in one dense breath with three separate moving parts (select, flush, refill) and a mid-sentence example that a first-time listener has to context-switch into:
  > "With thousands of runs, scanning every front for the smallest item would be slow, so keep a small heap with one entry per run. Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time. Say run three has the smallest front item: it moves to the output. When the output fills, that block goes to disk. When run three runs dry, its next block comes in from disk."
  **Rewrite (split into two beats, one idea each):**
  "With thousands of runs, checking every front for the smallest item would be slow — so keep a small heap with one entry per run, small enough to live in memory the whole time, unlike heapsort's heap of the whole file.
  [beat] Say run three's front item is smallest: it moves to the output. Fill a block of output, and it goes to disk. Empty a run's block, and its next one comes in from disk."

- **NIT — dense phrasing for the ear:**
  > "So each extra merge pass lets the file grow by that same factor of sixteen thousand."
  **Rewrite:** "So every extra pass multiplies how big a file you can sort by another sixteen thousand."

---

VERDICT: PASS
