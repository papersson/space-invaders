# Script Review — External Merge Sort Explainer

## 1. One question
**Opening:** "What are those files, and how does sort get away with it?"
**Ending:** "That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."

The callback is explicit and reuses the opening's own numbers ("twelve times bigger... its memory"). This test passes cleanly.

One structural side-effect worth naming: the question is actually answered twice before the ending — section 3 says "that's what sort's twelve files were" and section 4 says "it's exactly what sort did at the end." By the time you reach section 6, the mystery is already resolved twice over, so the "ending" is a recap, not a reveal. Not a violation of the test as written (NIT), but it does mean the emotional payoff of the callback is spent early.

## 2. But/therefore chain
One sentence per segment:

1. Sort finishes a 12x-memory file and leaves behind twelve vanishing files; Python can't. What are they?
2. **Therefore** — the obvious fix (virtual memory) fails because disk I/O is block-granular and slow, **so** what matters is I/O count, not comparisons; **therefore** measure passes.
3. **But** merge sort still needs 18 passes; **however**, the first 14 produce pieces smaller than memory, **so** presort those directly as "runs," collapsing 18 passes to 5. (These are sort's twelve files.)
4. **But** the remaining passes two-way-merge and waste memory; **therefore** give every run a block and multiway-merge with a heap, collapsing 5 passes to 2. (This is what sort did at the end.)
5. **And then** — how far does this scale? Sort caps at 16; in general a merge can absorb thousands of runs, so huge files still take 2-3 passes; **therefore** databases use this.
6. **Therefore**, recap: count I/Os, sweep sequentially, merge as many runs as memory allows.

**Finding (SHOULD FIX):** Section 5 is the one real "and then." By the end of section 4 the opening question is fully answered — nothing forces the viewer toward "how many runs can one merge take?" It reads as an appended epilogue rather than a consequence.
> Quote: *"So how many runs can one merge take? Sort itself stops at sixteen by default, which was plenty for twelve."*
> Rewrite: *"Our file only needed twelve runs. But what if a file needed more runs than memory has blocks for? Sort itself caps a merge at sixteen runs by default — enough for our twelve, but what happens past that?"* — this converts the segue into a "but," forcing the extension.

## 3. Derive, don't reveal
Every major idea is built from a visible problem before being named: I/O (disk fetches whole blocks, not single numbers) → pass (merge sort "sweeps" the file) → run (pieces smaller than memory don't need disk-based merging) → multiway merge (two-way merge leaves memory idle) → heap-for-merge (scanning thousands of fronts would be slow) → external merge sort (named only after both halves — runs, multiway merge — are built). No ideas are announced without a preceding problem. This test passes without a finding.

## 4. Setups and payoffs
| Setup | Payoff |
|---|---|
| Twelve files appear/vanish (opening) | "That's what sort's twelve files were" (§3); "the runs disappear" (§4) |
| 86 MB memory / 1 GB file, "twelfth" | "quarter of a million... memory holds a twelfth" (§2), "twelve memories long" (§3) |
| Heapsort 3.2 I/Os per item | Justifies "merge sort is our starting point" (§2) |
| "less than a twentieth" of I/Os | Same |
| 18 doublings / passes | "first fourteen... eighteen passes become five" (§3) |
| Pass tally 5 | "five passes become two" (§4) |
| "thousands of runs" (mentioned mid-§4) | Concretized as "thousands of blocks" in §5 |
| Sixteen (sort's default cap) | Explained same beat in §5 — fine |

No unpaid setups or unearned payoffs of note. One near-miss: the toy demo's heap is described on screen as "three-node" while narration in the same beat says "with thousands of runs" — the payoff for that "thousands" line doesn't land until §5, so for a few seconds the picture (3 nodes) and the claim (thousands) don't match scale. See Test 10.

## 5. One vocabulary
| Term | First use | Notes |
|---|---|---|
| I/O | Defined before naming: "fetches a whole block... called an I/O" | Clean |
| block | Defined in same sentence as I/O | Clean |
| pass | "measure it in passes, where one pass reads and writes every block once" | Clean, but see below |
| run | "write it out to disk as one sorted piece, called a run" | Clean |
| multiway merge | Named after being built | Clean |
| heap | Assumed prior knowledge (per audience) | Fine |
| external merge sort | Named only after both halves exist | Clean |

**Finding (NIT):** "sweeps" and "passes" are used for the same concept one clause apart: *"It sweeps through the whole file again and again, so let's measure it in passes."* Low risk since they're adjacent, but a viewer could wonder if "sweep" is a distinct term. Rewrite: *"It reads and writes the whole file again and again — count those as passes."*

## 6. Number budget
Numbers spoken: twelve (ratio), hundreds-to-thousands (I/O latency), quarter of a million (items), a twelfth (memory ratio), three I/Os/item, a twentieth, eighteen (doublings/passes), fourteen, twelve (runs), five, six/three/two/one (merge halving), four, two, sixteen (cap), thousands (blocks/runs).

That's well over a dozen distinct figures, several arriving in tight clusters — e.g., "Our file is twelve memories long, so this makes twelve runs, in a single pass. That one pass replaces the first fourteen, and the last four stay. Eighteen passes become five" packs five numbers into three sentences.

**Finding (SHOULD FIX):** too many numbers compete for retention; the load-bearing ones are **12** (ties question to answer) and **2** (final pass count) — arguably a third, **"one merge absorbs thousands of runs"** (why this scales in the real world). Everything else (14, 18, 4, 5, 6, 3, 1, 16, 107696kB) is derivation scaffolding that doesn't need to survive in memory.
Rewrite (add before or in §6): *"Forget the running tally — the two numbers to keep are twelve, the runs sort made, and two, the passes it took to merge them."*

## 7. Concrete before abstract
**Finding (SHOULD FIX):** the abstraction arrives before its evidence.
> Quote: *"Heapsort and merge sort both do on the order of N log N comparisons. So let's count their I/Os instead. We simulated both... on a quarter of a million items."*

The general claim ("same order of comparisons") is asserted before the concrete measured comparison counts (which only appear as a screen caption moments later). This is precisely the beat meant to disprove "comparisons decide speed" — it lands harder if the concrete numbers come first.
Rewrite: *"We measured it: on this file, heapsort and merge sort make close to the same number of comparisons. So comparisons aren't what's separating them — let's count I/Os instead."*

Milder second instance: the general rule "a block for every run, plus one for the output" (§4) is stated before any number confirms 86 MB actually holds enough blocks for 12 runs — it's only retroactively grounded once §5 gives "thousands of blocks." Low severity, self-resolves.

## 8. Wrong model
Wrong model: "comparisons decide speed; virtual memory handles the disk." Both halves are shown failing, not just asserted: the "obvious fix" (virtual memory) is introduced and then broken concretely by the heapsort simulation (3.2 I/Os/item, ~20x worse than merge sort) despite similar comparison counts. This is a well-executed disproof — test passes, modulo the ordering note in Test 7.

## 9. Depth over breadth
No shallow list of applications. The single real-world example (PostgreSQL's `EXPLAIN ANALYZE`) is shown with actual output, not just name-dropped. No finding here beyond noting it's a small aside — see Test 11 for whether it's load-bearing.

## 10. Words and pictures
Screen text mostly complements rather than duplicates narration (e.g., screen shows exact simulation parameters — 261,120 items, 21,760 memory — while narration says the rounder "quarter of a million" and "a twelfth"). Good practice throughout.

**Finding (NIT):** scale mismatch between picture and line. Narration: *"With thousands of runs, scanning every front... would be slow, so keep a heap."* Screen (same beat): *"three-node heap over the fronts."* The toy necessarily shows few runs, but the claim is about thousands — for a moment the picture undercuts the stated motivation.
Rewrite: add one clause to bridge scale — *"With thousands of runs — far more than our twelve — scanning every front for the smallest item would be slow, so keep a heap."*

**Finding (NIT):** the closing recap card ("the three rules") appears to restate the spoken takeaway lines verbatim. Intentional reinforcement is defensible for a rule the viewer should retain, but if the card is literally the same sentences, consider shortening the on-screen text to keyword form (e.g., "Count I/Os · Sweep in order · Merge more runs") so screen and voice aren't saying identical full sentences simultaneously.

## 11. Deletion test
Candidates that could be cut without breaking anything downstream or weakening the takeaway:
- *"That's why databases sort this way. When a query sorts more than fits in its memory, PostgreSQL's EXPLAIN ANALYZE reports an external merge."* — nice real-world grounding, but nothing later depends on it and the takeaway (the three rules) doesn't need it. Lowest-cost cut if time is tight. (NIT — keep if word budget allows; it's the only external-validity beat in the piece.)
- On-screen-only trivia ("GNU coreutils sort 9.4" version label) — decorative, no narrative weight either way.

Nothing else is safely removable — the numeric chain (12→18→14→5→2) is load-bearing for the derivation, and the "run three" example in §4 earns its place by making the heap mechanism concrete (Test 7's own preference).

## 12. For the ear and pacing
**Finding (SHOULD FIX):** two compression claims land back-to-back and are easy to lose by ear alone:
> Quote: *"So as long as memory has a block for every run, plus one for the output, the whole merge is a single pass: the four merge passes collapse into one. Five passes become two: one to make the runs, one to merge them."*

Two different "collapse" events (4→1, then 5→2) in consecutive sentences risk blurring which count refers to what.
Rewrite: *"So as long as memory has a block for every run, plus one for the output, the merge happens in a single pass. That folds the four merge passes into one. Add back the pass that built the runs, and eighteen passes have become two."*

**Finding (NIT):** "I/O," spoken as "eye-oh," recurs roughly a dozen times across the script (*"count their I/Os," "I/Os dominate," "I/Os per item," "twentieth of heapsort's I/Os," "every I/O a dot," "count I/Os, not comparisons"*). It's a written abbreviation, not a natural spoken word, and repeating it this often can feel clipped aloud. Also worth noting: the stated learning objective uses "block transfers," while the script consistently says "I/O" — if the spoken term is meant to be the memorable one, picking a single spoken phrase (e.g., "disk fetch" for the first couple of uses, "I/O" once it's established as shorthand) may read more naturally aloud than repeating the abbreviation throughout.

**Finding (SHOULD FIX):** the numeric run in §3 — *"Our file is twelve memories long, so this makes twelve runs, in a single pass. That one pass replaces the first fourteen, and the last four stay. Eighteen passes become five."* — asks the ear to hold five numbers (12, 12, 14, 4, 18, 5) in about ten seconds. The screen's pass tally ("18 → 5, written as 1+4") helps, but consider giving this beat one more second per number, or cutting one of the restatements (e.g., drop "and the last four stay" since it's recoverable from 18−14=4 and not needed again until §4's "four merge passes").

---

No finding rises to the level of undermining the core argument, breaking a later payoff, or leaving the takeaway unsupported — the script already shows evidence of a prior revision pass (per the review log) that fixed the more serious issues (false single-pass claim, unmotivated numbers, wrong-model disproof). Remaining items are polish: one abstraction/evidence ordering fix, one unmotivated segue, one number-budget signpost, and a couple of pacing/vocabulary tightenings.

VERDICT: PASS
