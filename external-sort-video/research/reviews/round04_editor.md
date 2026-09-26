# Script Review

Overall this is a tight, already-revised script (round 1 clearly did real work). I found no BLOCKING problems. Below are findings by test, then verdict.

---

**1. One question**
Opens: *"What are those files, and how does sort get away with it?"* Closes: *"That's how sort handled a file twelve times bigger than its memory: twelve runs, one merge, two passes."* The exact phrase "twelve times bigger" is echoed, and both halves of the opening question (what/how) are named explicitly. No finding — this is the strongest structural element in the script.

**2. But/therefore**
Chain, one sentence per segment:
1. A file 12× memory breaks Python but not `sort`, which mysteriously writes and deletes twelve files. **Therefore** we ask what a naive fix (virtual memory) would do —
2. **but** it fails, because disks move whole blocks at hundreds-of-times latency, so I/O count (not comparisons) dominates, and merge sort turns out to need far fewer I/Os than heapsort. **Therefore**
3. count merge sort's passes: 18 is a lot, **but** the first 14 merge pieces smaller than memory, so those can be pre-sorted in memory as "runs" with no disk at all — 18 becomes 5 (and that's sort's twelve files). **Therefore**
4. the runs still need merging, **but** a two-way merge leaves memory mostly idle, so give every run its own block and merge all at once — 5 becomes 2 (and that's exactly what sort did). **Therefore**
5. how far does this scale? Sort caps at 16, **but** memory holds thousands of blocks, so even huge files take 2-3 passes — **therefore** databases use this. **Therefore**
6. the rule: count I/Os, work in sequential passes, cut passes by sizing runs/merges to memory.

Every joint is "but" or "therefore." No filler "and then" found in the *logical* structure (the two literal "and then"s in the text — files vanishing, runs deleted — are real-time narration of events, not idea-joins, so they don't count against this test). No finding.

**3. Derive, don't reveal**
- I/O and "block": derived (naive VM idea fails because disks fetch whole blocks) → named. Good.
- "run": derived (pieces smaller than memory don't need the disk) → named immediately after. Good.
- "multiway merge": derived (idle memory during 2-way merge) → named. Good.
- NIT — "pass" is defined by assertion rather than derived from a felt gap: *"Let's measure it in passes, where one pass reads and writes every block of the file once."* There's no visible problem this solves yet (it's a unit-of-measure setup, not an idea), so I'd call this an acceptable exception rather than a violation — flagging only so you can confirm that's the intent.

**4. Setups and payoffs**
Everything closes the loop: 12× ratio → 12 runs → 12 files; temp folder filling/vanishing → runs disappearing at merge; virtual-memory idea → shown failing; naive 18 passes → 5 → 2; sixteen-run cap → explains why 12 runs needed only one merge; "N log N comparisons" claim → resolved by the takeaway rule. No orphaned setups or unearned payoffs found.

**5. One vocabulary**
memory, block, I/O, pass, run, multiway merge, external merge sort — each named once, at first use, after being derived. "Piece" (used for the naive merge-sort's growing chunks) narrows into "run" (the intentionally pre-sorted piece) — this is a deliberate specialization, not a synonym drift, since the script never reverts to "piece" afterward. "Buffer pages" (the DB-textbook synonym for "block") is flagged explicitly on the end card rather than smuggled into the narration — correct handling. No finding.

**6. Number budget**
Numbers to remember: **twelve** (runs = the mystery files), **two** (final passes — the punchline), and the **3 vs. 1/20 I/O contrast** (the wrong-model kill shot). Those three carry the whole argument.

- SHOULD FIX — two screen-only numbers do no work and compete with "twelve" and "quarter million" for attention:
  - Quote (screen direction, §3): *"2¹⁸ ≈ 262,144"*
  - Rewrite: cut it — it just restates "a quarter of a million" in a different base; if you want proof-of-work on screen, put it on "18" (2¹ doubling 18 times), not as a redundant total.
  - Quote (screen direction, §3): *"a line at memory size (21,760)"*
  - Rewrite: drop the raw number; label the line "memory size" — it's an axis marker, not a number anyone needs to retain.
- NIT — the pass-count numbers (18, 14, 5, 12, 6, 3, 2, 1, 4, 5, 2, 16) are dense across §3-4. Round 1 already added reasons to each; I'd still call this the single riskiest stretch for a listener (see #12).

**7. Concrete before abstract**
The only formula (`passes = 1 + ⌈log_{M/B−1}(N/M)⌉`) is deliberately parked on the silent end card, after every concrete case (12 runs, the race, the merges) has already landed. No finding — this is exactly the right order.

**8. Wrong model**
Wrong model: *"comparisons decide speed, and virtual memory handles the disk."* Shown failing: virtual memory demo (heapsort still does ~3 I/Os/item despite "the OS handling it"), and the explicit line that heapsort and merge sort have the *same order* of comparisons yet wildly different I/O counts.

- SHOULD FIX — the screen direction undercuts its own disproof slightly: narration says *"Heapsort and merge sort both do on the order of N log N comparisons"* (implying rough parity), but the paired screen caption says *"heapsort about twice as many [comparisons]."* A sharp viewer could wonder whether the 2× comparison gap is doing some of the work that's being attributed to I/Os, muddying the kill shot.
  - Rewrite: *"Heapsort and merge sort both do on the order of N log N comparisons — heapsort needs about twice as many, nothing dramatic. So let's count their I/Os instead."* This pre-empts the objection by naming the 2× and dismissing it before the 60×+ I/O gap lands.

**9. Depth over breadth**
Only one named external application (PostgreSQL), backed by a real `EXPLAIN` capture and fully explained by the preceding four minutes — not a name-dropped list. No finding.

**10. Words and pictures**
- NIT — screen caption near-duplicates the line it sits under:
  - Quote (narration): *"Sort itself stops at sixteen by default"* / Quote (screen): *"GNU sort: at most 16 per merge (--batch-size)"*
  - Rewrite: trim the caption to just `--batch-size = 16` and let narration carry the "stops at... by default" framing alone, so the two channels split the load (screen = verifiable fact, narration = meaning) instead of both saying the same sentence.

**11. Deletion test**
- NIT — two adjacent sentences say the same thing twice: *"Merging only needs sorted pieces. It doesn't matter how they got sorted, so each of those pieces could have been sorted without touching the disk."*
  - Rewrite: *"Merging only needs sorted pieces — it doesn't matter how they got that way, so each one could have been sorted without touching the disk."* (saves ~4 words, no loss of content; also helps #12's word-count problem.)

Nothing else is safely cuttable — every other line sets up a term, a number, or the wrong-model disproof that gets paid off later.

**12. For the ear**
Word count: narration is **837 words** ≈ 5.6 min at 150 wpm — 87 words over the stated 750-word/5-min target, though still under the 900-word/6-min ceiling. SHOULD FIX: trim toward target using #11's combine plus one more merge, e.g. *"That's why databases sort this way. When a query sorts more than fits in its memory, PostgreSQL reports an external merge."* → *"Databases do this too: when a query outgrows memory, PostgreSQL reports an external merge."*

- SHOULD FIX — five bare digits in one breath:
  - Quote: *"Two at a time, twelve runs become six, then three, then two, then one: those are the four passes."*
  - Rewrite: *"Two at a time, the twelve runs halve, and halve again: six, three, two, one — four passes."* (same numbers, but "halve, and halve again" gives the ear an operation to hang them on, not just a countdown.)

- SHOULD FIX — overloaded sentence stacking two unrelated facts on "and":
  - Quote: *"In general, one merge can take one run per block of memory, less one for the output, and a laptop's memory holds thousands of blocks."*
  - Rewrite: *"In general, one merge can take one run per block of memory, minus one block held back for the output. A laptop's memory holds thousands of blocks."*

---

VERDICT: PASS
