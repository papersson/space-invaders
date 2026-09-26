# Script Review

## 1. One question

**Opening:** "What are those files, and how does sort get away with it?"
**Closing line:** "That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes."

The ratio ("twelve times bigger than its memory") is echoed verbatim — good callback. But the noun switches from "files" to "runs" and is never reunified at the very end (the files=runs equation is made once, mid-script, in §3: "And that's what sort's twelve files were").

- **NIT** — Quote: *"twelve runs, one merge, two passes."*
  Rewrite: *"twelve files, twelve runs, one merge, two passes."* (costs three words, closes the loop on the exact noun the cold open used)

## 2. But/therefore chain

Condensed chain (segment → connective):

1. File is 12x memory. Python OOMs. Sort finishes. Files appear, then vanish. **[question]**
2. Obvious fix = virtual memory, **but** disks fetch whole blocks slowly → I/Os dominate. Heapsort/mergesort are both N log N, **so** comparisons alone predict heapsort ~2x slower, **but** heapsort's scattered access blows up I/Os while mergesort's sequential access doesn't; measured: 2x comparisons **but** 20x I/Os. **Therefore** I/Os decide, **so** measure in passes.
3. Doubling gives 18 passes, **but** the first 14 pieces are smaller than memory, **so** sort them in memory as runs — 12 runs in one pass, **so** 18 passes become 5. **And that's** the twelve files.
4. Runs still need merging (4 passes two-at-a-time), **but** most of memory sits idle during a two-way merge, **so** give every run a block and merge all at once; **so** 5 passes become 2. That's external merge sort — **and that's** what sort did.
5. One merge can only take as many runs as memory has blocks, **but** a huge file needs more runs than that, **so** you need extra passes — **but** each extra pass multiplies capacity by thousands, so real files still finish in 2-3 passes. **That's why** databases do this too.
6. Recap.

The chain is unusually clean — almost every join is causal. Flagged "and"/"then" spots that are additive rather than causal:

- **NIT** — Quote: *"Then do the same with the next part of the file, and the next."*
  This is a repeated action, not an argument step — fine as written, but it's the one place a viewer could mentally check out. Rewrite: *"Repeat until the file is gone."*
- **SHOULD FIX** — Quote: *"GNU sort is more cautious by default: it merges at most sixteen runs at a time, trading some speed for less memory."*
  This sentence follows a paragraph establishing that memory could hold *thousands* of run-blocks — it's a hidden contrast, not a neutral fact, and reads as a flat "and" where a "but" belongs.
  Rewrite: *"But GNU sort is more cautious than that: it merges at most sixteen runs at a time, trading some speed for headroom."*
- **NIT** — Quote: *"...often a megabyte, to cut down on fetches, and a laptop's memory still holds thousands of those."*
  Two facts stapled with "and" where the second is actually the consequence of the first (bigger blocks → fewer of them needed → thousands still fit).
  Rewrite: *"...often a megabyte, to cut down on fetches — so even then, a laptop's memory holds slots for thousands of them."*

## 3. Derive, don't reveal

Every major idea is earned: virtual memory (shown failing before being replaced), I/O as a unit (named right after the block-fetch problem is shown), runs (derived from noticing early pieces fit in memory), multiway merge (derived from noticing idle memory in a two-way merge), the in-memory heap (derived from "scanning every front would be slow").

One exception:

- **NIT** — Quote: *"GNU sort is more cautious by default: it merges at most sixteen runs at a time."*
  This is announced as trivia, not derived from a shown problem (unlike everything else in the script). It works because it's short and immediately tied back to "twelve," but it's the one fact-drop in an otherwise derive-everything script.

## 4. Setups and payoffs

| Setup | Payoff |
|---|---|
| File bar vs. memory bar, to scale | Returns in §6 with pass count overlaid |
| Twelve files appear/vanish, question mark freeze | "Appear" answered in §3 (runs), "vanish" answered in §4 (merged & deleted) |
| Python OOM vs. sort finishing | Explicitly contrasted again in §6 |
| Virtual memory as "obvious fix" | Shown failing via heapsort/mergesort simulation in §2 |
| Heapsort's scattered heap | Called back by contrast in §4 ("Unlike heapsort's heap...") |
| "measure in passes" | Running pass tally 18→5→2 threaded through §3, §4, §6 |
| "twelve times bigger" | Explains the "12 runs" arithmetic in §3 caption; echoed verbatim in closing line |
| GNU sort's batch-size of 16 | Weak payoff — only "That was plenty for our twelve," which doesn't add information already established |

- **NIT** — no true orphaned setups or unearned payoffs found. The batch-size-16 fact is the weakest link (see §11 below, deletion candidate).

## 5. One vocabulary

| Term | First use | Notes |
|---|---|---|
| I/O | §2, defined immediately after the block-fetch problem | clean |
| block | §2, used before formally named but intuitively clear | fine given audience |
| pass | §2, defined at first use | clean |
| run | §3, defined at first use ("called a run") | clean |
| multiway merge | §4, defined at first use | clean |
| external merge sort | §4, named only after the mechanism is fully built | clean, good "derive don't reveal" ordering |
| heap (as merge structure) | §4, explicitly distinguished from heapsort's heap | good — same word, explicitly disambiguated, not a silent double-naming |
| "file" vs. "run" | §1 vs. §3 | equated explicitly once in §3 ("that's what sort's twelve files were... wrote out twelve runs") — no violation, but see Test 1 |

No terms are used before being explained, and no concept is silently given two names.

## 6. Number budget

Full list: 12 (ratio/files/runs), 1 GB / 86 MB, "hundreds to thousands of times slower," ~2x (comparison bound), 261,120 items / 21,760 items / 256-item blocks (screen only), 2x comparisons vs. 20x I/Os / ~3 I/Os per item, 8.6M vs 4.4M comparisons, 837,090 vs 36,720 I/Os, <1s vs >1min, 18 passes (2¹⁸≈262,144), first 14 passes, 18→5, twelve-then-six-three-two-one (4 passes), 5→2, 18→2, ~1 MB blocks, thousands of blocks, 16 (GNU sort batch-size), 100,000 runs → 7 → 1, "thousands of times bigger" per pass, 2-3 passes in practice, 107,696 kB (Postgres).

**The 2-3 to remember:** 12 (the file-to-memory ratio that frames the whole story), 18 → 2 (the pass reduction, the actual payoff), and the I/O-vs-comparison contrast (20x I/Os, or <1s vs >1min — pick one, not both).

Numbers doing no work:

- **SHOULD FIX** — Quote: *"one merge pass cuts them to seven, and one more makes them one file"*
  100,000 → 7 is an oddly specific figure with no shown derivation, and it doesn't reconcile with the "sixteen" merge factor just given two sentences earlier — a viewer who does the mental math (100,000/16 ≈ 6,250, not 7) will stumble.
  Rewrite: *"one merge pass cuts them to a few dozen, and one more finishes the file."*
- **NIT** — Quote: *"8.6 M vs 4.4 M... 837,090 vs 36,720"* (screen caption)
  These exact counts are screen-only and add precision the narration's rounder "twice / twenty times" already covers — fine as an authenticity detail, but cut if the frame feels busy.

## 7. Concrete before abstract

No violations found. The end-card formula is correctly held back until after the concrete case is fully built, and is explicitly framed as bonus reference material, not part of the taught argument. "N log N" is invoked as known prior knowledge (per the stated audience), not taught as new abstraction, so it doesn't need concrete grounding first.

## 8. Wrong model

Wrong model: *"comparison counts decide speed, and virtual memory takes care of the disk."*
It is shown failing concretely and numerically: heapsort has only ~2x the comparisons of mergesort but ~20x the I/Os, and the time breakdown (<1s of comparisons vs. >1min of I/Os) makes the failure undeniable rather than asserted. This test is satisfied.

## 9. Depth over breadth

No shallow list of named-but-unexplained applications. Databases are represented by one worked example (Postgres `EXPLAIN ANALYZE` with an actual disk figure), not a list of logos. This test is satisfied.

## 10. Words and pictures

Mostly complementary (screen gives exact figures, narration gives rounded takeaways). One soft duplication:

- **NIT** — Quote: screen shows *"N log N"* under both animations at the same moment narration says *"Heapsort and merge sort are both N log N sorts."*
  Minor; the label is short enough that it reads as a tag, not a duplicated sentence. Consider holding the on-screen label half a beat so it lands as confirmation rather than caption.

## 11. Deletion test

- **NIT** — Quote: *"That was plenty for our twelve."*
  Doesn't add new information — the twelve-fits-in-one-merge point was already made in §4. Could be cut without losing anything.
- **NIT** — Quote: *"Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."*
  Nice-to-have relevance beat, not required by any stated objective; cuttable if runtime is tight, though it's a good "so what" and I'd keep it if there's room.

## 12. For the ear and pacing

- **SHOULD FIX** — Quote: *"Say run three's front item is the smallest: it goes to the output block. When the output block fills, it's written to disk. When run three's block runs dry, its next block comes in from disk."*
  Three uses of "block" in different senses ("output block," "run three's block," "next block") plus two references to "run three" packed into one breath — dense enough to lose a listener who's only hearing it once.
  Rewrite: *"Say run three has the smallest front item — it moves to the output. When the output fills, that block goes to disk. When run three runs dry, its next block gets pulled in."*
- **SHOULD FIX** — Quote: *"one merge pass cuts them to seven, and one more makes them one file"*
  Same line flagged in Test 6 — also a pacing problem, since it asks the listener to accept an unexplained arithmetic leap right after a different, un-reconciled number ("sixteen") was just given. Slow this beat down or round it off (see rewrite above).
- **NIT** — Quote: *"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."*
  One long sentence carrying three clauses; not wrong, just a candidate for a breath-split if the voiceover feels rushed on the recording pass.

---

VERDICT: PASS
