# Script Review

## 1. One question

The opening asks a concrete question ("What are those files, and how does sort get away with it?"). The specific answer ("twelve runs... that's what sort's twelve files were") actually lands in **§3**, a full two sections before the video's real ending. By §6 the narration has moved on to restating the general takeaway rule and doesn't say the word "files" again — the loop is closed visually (screen direction replays the capture) but not verbally.

- **SHOULD FIX** — Quote: *"That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."*
  Rewrite: *"Those twelve files that flashed through /tmp and vanished were the twelve runs — made in one pass, merged in one more. That's how sort handled a file about twelve times bigger than its memory."* This puts "files" and "vanish" back in the closing sentence so the ending quotes the opening, not just the middle.

## 2. But/therefore chain

Section-level chain (works cleanly through §4):

1. Sort finishes on a huge file, Python doesn't, twelve files flash and vanish — **therefore** we test the obvious fix, virtual memory.
2. **But** disks move whole blocks and I/Os cost hundreds–thousands of times more than memory access, so heapsort's scattered accesses lose to merge sort's sequential ones — **therefore** we adopt merge sort, measured in passes.
3. **But** plain merge sort takes 18 passes, and **but** most of those passes sort pieces already smaller than memory — **therefore** sort each piece as a "run" (12 of them, in one pass), cutting 18→5.
4. **But** merging runs pairwise wastes memory — **therefore** merge all runs at once (multiway merge), cutting 5→2. This is external merge sort, and it's what sort did.

Section 5 is where the chain slips into "and then":

- **SHOULD FIX** — Quote: *"Real sorting programs read much bigger blocks... GNU sort is more cautious by default: it merges at most sixteen runs at a time, trading some speed for less memory."* There's no "but" or "therefore" signaling the contrast (could merge thousands → chooses only 16), and the tradeoff claim isn't earned (see §3 below). Rewrite: *"So real sorting programs could merge thousands of runs at once. GNU sort doesn't — it caps itself at sixteen, trading merge width for a smaller memory footprint. Twelve runs was comfortably inside that."*
- **SHOULD FIX** — Quote: *"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."* This silently switches from the 16-run cap just stated to an implied branching factor of ~14,000, with no bridge. It reads as "and then" — a new number pair with no visible arithmetic connecting it to anything just said. Rewrite: *"Say a program with room for fourteen thousand blocks meets a file with a hundred thousand runs: one merge pass — one block per run — cuts that to seven; one more merges those seven into the finished file."*

## 3. Derive, don't reveal

Mostly excellent — "run," "external merge sort," and "multiway merge" are all named only after the problem they solve is shown. One reversal:

- **SHOULD FIX** — Quote: *"Once data doesn't fit in memory, the number of I/Os typically dominates the running time."* This is asserted, then proven by the heapsort/merge-sort race two sentences later — rule before evidence. Rewrite: move this sentence to after the race ("...its I/Os take more than a minute. The I/Os decide. That's the rule once data doesn't fit in memory: count I/Os, not comparisons.")
- **NIT** — GNU sort's 16-run cap "trading some speed for less memory" is announced as a fact, not derived — the video never explains why fewer runs per merge saves memory (each run's block still has to be held). If keeping the line, add the one-clause reason: *"...trading merge width for a smaller memory footprint"* rather than the unexplained "speed for memory."

## 4. Setups and payoffs

Well-threaded overall (12x → 12 files → 12 runs; N log N → equal comparisons; heapsort's "whole-file heap" → explicitly contrasted with the merge's "small heap that stays in memory"; pass tally 18→5→2 fully resolved). Two problems:

- **SHOULD FIX** — Setup with weak payoff: *"Ask PostgreSQL how it ran a query... it reports an external merge."* with screen detail *"Sort Method: external merge Disk: 107696kB"*. The number is shown but never interpreted (how many runs? how many passes?) — see also Test 9.
- **SHOULD FIX** — Payoff without a firm setup: the "hundred thousand runs → seven" example (Test 2 finding) pays off "merging many at once cuts passes fast," but the setup for *what* branching factor is in play is too thin to support it.

## 5. One vocabulary

Every core term (*block*, *I/O*, *pass*, *run*, *multiway merge*, *external merge sort*) is defined at first use — no term arrives before its explanation. One overlap, self-flagged by the script:

- **NIT** — "Heap" is used for two different structures (heapsort's whole-array heap vs. the multiway merge's small in-memory heap of run-fronts). The line *"Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time"* handles it, but consider naming the second one differently on screen (e.g. "merge heap") to avoid relying on a spoken disclaimer alone.

## 6. Number budget

The three numbers worth remembering are clearly **12** (times bigger / runs made), **18** (naive pass count), and **2** (final pass count) — the video repeats this trio enough that they'll stick, and narration keeps most other numbers rounded ("twice," "twenty times," "three per item") while precise figures (8.6M vs 4.4M, 837,090 vs 36,720) are screen-only, which is the right split.

- **SHOULD FIX** — Section 5 introduces a cluster of numbers that do no lasting work: *sixteen, thousands, a hundred thousand, seven*. None of these reinforce the 12/18/2 spine, and "seven" in particular is unreachable by mental math in real time (flagged already under Tests 2/4). Consider cutting to one scaling example instead of two ("sixteen" cap *and* "hundred-thousand-runs" hypothetical), to protect the number budget.

## 7. Concrete before abstract

Good discipline generally — the formula card is reference-only at the very end, after every concrete case is worked. The one exception is the Test 3 finding: the abstract claim "I/Os typically dominate" precedes its own concrete proof (the heapsort/merge-sort race). Same fix as Test 3 (reorder).

## 8. Wrong model

The wrong model — "comparisons decide speed, virtual memory handles the disk" — is confronted directly and shown failing with real numbers: equal-ish comparison counts (8.6M vs 4.4M) but wildly unequal I/Os (837,090 vs 36,720), converted into human time (0.86s vs 84s). This is the strongest beat in the script — no finding needed.

## 9. Depth over breadth

- **SHOULD FIX** — Quote: *"Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."* with the raw `Disk: 107696kB` line. This is a named-but-not-understood example — it shows a real tool uses the technique but never connects the shown number back to runs or passes. Either cut it (the takeaway doesn't need a third example after sort and the scaling discussion) or spend one more clause: *"...and it reports an external merge, having spilled 107 MB of runs to disk in the process."*

## 10. Words and pictures

- **NIT** — Quote/screen: narration says *"Heapsort and merge sort are both N log N sorts"* while the screen shows *"N log N" under both names* — a caption restating the spoken term. Low-stakes (it's a label, not a full sentence), but could be swapped for something additive, e.g. showing the actual comparison counts already ticking up.
- No other narration/screen mismatches found — the "1+4" and "1+1" pass-tally overlays add information (the decomposition) rather than repeat the line, and §6 explicitly avoids on-screen rule text.

## 11. Deletion test

- **SHOULD FIX** — The GNU-sort-caps-at-16 paragraph and the PostgreSQL line could both be cut without weakening the takeaway — all four stated objectives are already satisfied by the end of §4 (I/O cost model, run formation, multiway merge cutting passes, explaining sort's twelve files). If pacing is tight, cut PostgreSQL first (least developed, per Test 9) and keep the batch-size fact only if trimmed per Test 2's rewrite.
- Nothing in §1–§4 is a deletion candidate — each line does load-bearing work in the chain traced in Test 2.

## 12. For the ear and pacing

- **SHOULD FIX** — Quote: *"With thousands of runs, scanning every front for the smallest item would be slow, so keep a small heap with one entry per run. Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time. Say run three's front item is the smallest: it goes to the output block. When the output block fills, it's written to disk. When run three's block runs dry, its next block comes in from disk."* Five mechanism beats back to back (heap, contrast with heapsort, selection, output flush, input refill) with no pause — the densest paragraph in the script, and the one most likely to lose the viewer the round-1 student review already flagged. Consider splitting into two beats with a screen-direction pause between "selection into the output" and "flush/refill," giving the multiway-merge mechanic room to breathe.
- **SHOULD FIX** — Quote: *"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."* Rushed: requires hidden division the viewer can't do live (same finding as Tests 2/6).
- **NIT** — Quote: *"We simulated both under virtual memory, on a quarter of a million items, with memory for a twelfth of them, roughly the same proportions as sort's file."* Four clauses in one breath; consider splitting after "virtual memory."

---

VERDICT: PASS
