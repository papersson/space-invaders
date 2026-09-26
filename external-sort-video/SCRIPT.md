# Script: Bigger Than Memory (version 2)

**Status: locked after review round 15** (expert PASS, editor PASS, simulated student's retelling covers every objective), with inputs checked to contain only what each reviewer should see. The review log at the end records every round.

## The argument

- **Audience:** undergraduates who know Big-O, merge sort, heapsort and heaps, and not much about disks.
- **Question (opening):** GNU sort finishes a file much bigger than its memory while Python runs out.
  Twelve files appear in a temporary folder and then vanish. What are those files, and how does that work?
- **Answer (ending):** external merge sort. Sort memory-sized pieces into runs (the twelve files), then
  merge all the runs at once with one block of memory each. Two passes over the data.
- **Takeaway rule:** when data doesn't fit in memory, count I/Os, not comparisons; work in long sequential
  passes; cut passes by making runs as big as memory and merging as many runs as memory holds blocks.
- **Wrong model to dislodge:** "comparison counts decide speed, and virtual memory takes care of the disk."
- **Objectives:** the viewer can (1) say why cost is counted in block transfers and why access order matters,
  (2) describe run formation and the multiway merge, (3) explain why merging many runs at once cuts passes,
  (4) explain what sort's twelve files were.

## The chain

1. Sort succeeds where Python fails, leaving twelve files that vanish. *What are they?*
2. **But** the obvious fix, virtual memory, fails: disks move whole blocks and each move is slow, so cost is
   I/Os, and heapsort under paging pays for them. Merge sort reads and writes in order.
   **Therefore** start from merge sort, and count its cost in passes.
3. **But** merge sort takes 18 passes, and the first 14 merge pieces smaller than memory.
   **Therefore** sort memory-sized pieces in memory: one pass makes runs. 18 passes become 5. The twelve files were runs.
4. **But** merging runs two at a time costs 4 more passes and leaves memory idle.
   **Therefore** give each run one block and merge them all at once. 5 passes become 2. The files vanished after that merge.
5. **Therefore** one merge takes one run per block of memory: sort stops at 16, a laptop could take thousands.
   More runs than that means rounds, each dividing the runs by thousands, so passes grow logarithmically in a
   base of thousands: two or three in practice. **That's why** databases sort this way.
6. Recap, and the answer to the opening question.

## Ledgers

**Setups and payoffs**

| Setup | Payoff |
|---|---|
| Twelve files appear and vanish (1) | They are runs (3); they are merged at once, then deleted (4); "twelve runs, one merge, two passes" (6) |
| Python runs out of memory (1) | Virtual memory as the obvious fix, shown failing (2) |
| Blocks and I/Os (2) | Every later count; the recap (6) |
| Merge sort reads and writes in order (2) | Starting point (3) |
| Pass, defined (2) | 18 → 5 → 2 (3, 4); the formula (5) |
| Idle memory in a two-way merge (4) | One block per run (4); "one per block of memory" (5) |
| The simulated file is twelve memories long (2) | Twelve runs, like sort's (3) |

**Vocabulary** (first use; no synonyms afterwards)

- *memory* (never "RAM"), *disk*, *virtual memory* (2)
- *block* (2): the fixed-size chunk a disk moves
- *I/O* (2): moving one block between disk and memory
- *pass* (2): reading and writing every block of the file once
- *run* (3): a sorted piece, as big as memory
- *two-way merge*, *multiway merge* (4); *external merge sort* (4)
- *heap* (4), known to the audience

**Numbers to remember:** twelve runs; 18 → 5 → 2 passes. Everything else is on screen or supports these.

## Script

No length target: the length follows the argument (about 150 words per minute of finished video).

### 1. The question

> This file is about twelve times bigger than the memory we'll let our programs use.
> Ask a simple Python script to read every line into a list and sort it, and it runs out of memory just reading the file in.
> Ask the Unix sort command, with the same memory, and it just finishes.
> While it works, twelve files appear in a temporary folder, and then they vanish.
> What are those files, and how does sort get away with it?

*Screen:* file bar next to a memory bar, to scale (1 GB of 10,000-byte records vs 86 MB, labelled; "GNU coreutils sort 9.4"). Two terminals replaying the real
runs; memory gauges with the same 86 MB cap; the /tmp folder filling with twelve `sortXXXXXX` files, then
emptying. Freeze on the twelve files with a question mark. Title.

### 2. Why the obvious fix fails

> The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed.
> But a disk never fetches one number. It fetches a whole block, thousands of bytes at least, and every fetch takes hundreds to thousands of times longer than reading memory, even on a fast SSD.
> Moving one block between disk and memory is called an I/O. Once data doesn't fit in memory, the number of I/Os typically dominates the running time.
> Heapsort and merge sort are both N log N sorts. By comparisons alone, heapsort would be at most about twice as slow.
> But heapsort compares items that sit far apart in its array. Under virtual memory that array lives on disk, block by block, so heapsort keeps needing blocks that aren't in memory. Merge sort reads its input from front to back, and writes its output from front to back, so every block it fetches gets used completely.
> We simulated both under virtual memory on a quarter of a million items. Memory held a twelfth of them, roughly the proportions of sort's file. Heapsort made about twice as many comparisons as merge sort, but more than twenty times as many I/Os: about three for every item it sorts.
> Even if every comparison cost as much as a memory access, heapsort's comparisons would take under a second. Its I/Os take more than a minute. The I/Os decide.
> So merge sort is our starting point. It sweeps through the whole file again and again, so let's measure it in passes, where one pass reads and writes every block of the file once.

*Screen:* a disk handing over a whole block for one requested number; the I/O counter appears. "N log N" under both names. Heapsort's comparisons lighting up array positions i and 2i far apart on the file bar, beside merge sort's cursor streaming along it. Then the race: two panels of position-in-file against time, every I/O a dot,
counters running (heapsort 3.2 I/Os per item; merge sort's clean diagonal passes). Measured counts under each name: comparisons 8.6 M vs 4.4 M, I/Os 837,090 vs 36,720. Caption with the simulation's exact parameters: 261,120 items, memory 21,760 items (1/12), blocks of 256 items. Then a time bar at typical speeds (~100 ns per comparison, the cost of a memory access, and ~100 µs per I/O, labelled typical): heapsort's comparisons 0.86 s against its I/Os 84 s.

### 3. Runs

> Merge sort merges single items into pairs, then pairs into fours, doubling the pieces every pass. Eighteen doublings take you from one item to a quarter of a million, so that's eighteen passes.
> But watch the size of the pieces. For the first fourteen passes, every piece is smaller than memory. Merging only needs sorted pieces. It doesn't matter how they got sorted, so each of those pieces could have been sorted without touching the disk.
> So do exactly that. Fill memory with the start of the file, sort it right there, and write it out to disk as one sorted piece, called a run. Then do the same with the next part of the file, and the next.
> Our simulated file is exactly twelve memories long, so this makes twelve runs, in a single pass. That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five.
> And that's what sort's twelve files were: one run for each memory-full of its file, the last one only partly full.

*Screen:* merge sort's eighteen passes from the race, numbered, with "2¹⁸ ≈ 262,144"; piece size doubling under them
(1, 2, 4 … 16,384) against a line at memory size (21,760); the first fourteen bracketed "smaller than memory". Toy: cards fill the memory tray, sort in place
(counter frozen: no I/O), go back as a run. Pass tally 18 → 5 written as "1 + 4". Cut to the /tmp folder at its
fullest, each file labelled "run 1" to "run 12", beside "1,000 MB ÷ 86 MB ≈ 11.6, so 12 runs".

### 4. The multiway merge

> Each run is sorted, but not against the others, so the runs still have to be merged. Two at a time: twelve runs, then six, three, two, one. Four passes.
> Watch memory during a two-way merge. It holds the front block of each run, and one block for the output. The rest of memory sits idle.
> So give every run its own block of memory, and merge them all at once: a multiway merge.
> With thousands of runs, scanning every front for the smallest item would be slow, so keep a small heap with one entry per run. Unlike heapsort's heap, which was the whole file, this one sits in memory the whole time. Say run three has the smallest front item: it moves to the output. When the output fills, that block goes to disk. When run three runs dry, its next block comes in from disk.
> Every block is still read once and written once. So as long as memory has a block for every run, plus one for the output, the merge happens in a single pass. That folds the four merge passes into one. Add the pass that made the runs, and eighteen passes have become two.
> Sort memory-sized runs, then merge them from disk: that's external merge sort. Merging as many runs at once as memory allows keeps the passes to a minimum.
> It's exactly what sort did at the end. It read all twelve runs at once while the sorted file grew, and then deleted them.

*Screen:* the halving 12 → 6 → 3 → 2 → 1 as four rows. Toy tray in a two-way merge: two input blocks and the output
lit, the rest grey. Then one block per run, a three-node heap over the fronts, cards moving to the output, flushes
and refills. Pass tally 5 → 2 written as "1 + 1". Cut to the capture: sorted.txt growing while all twelve runs are
read; the runs disappear.

### 5. How far it goes

> Our file needed only twelve runs, and GNU sort merges up to sixteen at a time by default, a cautious setting that trades some speed for less memory. That was plenty for twelve.
> But how many runs could one merge take? One per block of memory, less one for the output. Real sorting programs read much bigger blocks than our simulation did, often a megabyte, to cut down on fetches, and a laptop's memory still holds about sixteen thousand of those.
> A big enough file needs even more runs than that, so it takes more than one merge pass. Say a file needed a hundred thousand runs. Merging sixteen thousand at a time, one pass cuts them to seven. One more pass makes them one file. So each extra merge pass lets the file grow by that same factor of sixteen thousand. In practice, even enormous files sort in two or three passes.
> That's why databases sort this way. Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge: the same runs, then merges.

*Screen:* "GNU sort: at most 16 runs per merge, by default" beside its twelve runs. Then the tray widening to thousands of block
slots ("16 GB ÷ 1 MB ≈ 16,000 blocks"), thin lines from thousands of runs converging. Merge passes: 100,000 runs →
7 → 1, with "16,000 per merge" on the arrows. A real PostgreSQL EXPLAIN ANALYZE output with the line "Sort Method: external merge" highlighted and the rest dimmed.

### 6. The answer

> So, when data doesn't fit in memory, count I/Os, not comparisons.
> Work in passes that read and write in order, so every block you fetch gets used.
> And cut the passes: make runs as big as memory, then merge as many runs at once as memory has blocks to spare.
> Python tried to hold the whole file in memory at once. Sort never held more than a memory's worth.
> That's how sort handled a file about twelve times bigger than its memory: twelve runs, one merge, two passes.

*Screen:* no rule text (the narration carries the words): the opening's file and memory bars return with the pass count 18 → 5 → 2 across them; the capture replayed once more with "pass 1: twelve runs" and "pass 2: one merge" over it.
End card, for reference: passes = 1 + ⌈log_{(M/B) − 1} ⌈N/M⌉⌉ with N items, memory M items, blocks of B items
(Ramakrishnan & Gehrke write B for buffer pages, this video's M/B, and N for pages, this video's N/B); "asymptotically optimal: it matches the lower bound, up to constant factors, for sorts that move records as indivisible units (Aggarwal & Vitter, CACM 1988)";
Ramakrishnan & Gehrke, Database Management Systems, 3rd ed., ch. 13; Mehlhorn & Sanders, The Basic Toolbox, §5.7.

## Evidence

| Claim | Source |
|---|---|
| Python fails and sort succeeds with the same memory; file 11.6 memories long; twelve temp files (11 × 85.18 MB + 63.02 MB); one twelve-way merge; files deleted at the end | Real runs here (captures/, version 2): GNU sort 9.4, 1,000,000,000 bytes of 10,000-byte records, `-S 86000000b`; Python under an 86,000,000-byte address-space cap, `MemoryError` after 0.08 s |
| Heapsort ≈ 3.2 I/Os per item (837,090 for 261,120 items); merge sort 36,720 (heapsort 22.8× more); comparisons 8,591,468 vs 4,369,072 (1.97×) | iosim.py: LRU paging, 261,120 items, memory 21,760 items (file = 12 memories), 256-item blocks |
| 18 → 5 → 2 passes | iosim.py: plain merge sort ⌈log₂ 261,120⌉ = 18 passes, of which the first 14 produce pieces ≤ 16,384 ≤ M; 12 runs + ⌈log₂ 12⌉ = 4 two-way passes = 5; 12 runs + one 12-way merge = 2 (4,080 I/Os) |
| Heapsort's comparisons < 1 s and its I/Os ≈ 84 s at typical speeds | 8,591,468 × ~100 ns (a memory access, generous for a comparison) = 0.86 s; 837,090 × ~100 µs = 84 s (typical values, labelled as such); ratio of the two costs 1,000×, matching "hundreds to thousands" |
| 100,000 runs → 7 after one merge pass | ⌈100,000 / 16,383⌉ = 7 |
| SSD read hundreds of times slower than memory | Typical values: memory ~100 ns, NVMe random read ~50-100 µs (labelled typical) |
| A laptop's memory holds thousands of blocks (16 GB / 1 MB ≈ 16,000) | Arithmetic, decimal units as everywhere else in the video |
| Real systems: 2-3 passes | Ramakrishnan & Gehrke Ch. 13 |
| Optimal for sorts that treat items as indivisible | Aggarwal & Vitter, CACM 1988 |
| GNU sort merges at most 16 inputs at once by default, trading merge speed for memory | coreutils 9.4 manual, --batch-size: "a small value of NMERGE may reduce memory requirements and I/O at the expense of temporary storage consumption and merge performance ... The default value is currently 16"; confirmed by the -S 80M capture |
| Memory ≈ 22,000 items; first 14 passes have pieces ≤ 16,384 | iosim.py parameters: M = 21,760 |
| PostgreSQL EXPLAIN ANALYZE prints "Sort Method: external merge" | Real EXPLAIN (ANALYZE, COSTS OFF) output, PostgreSQL 16.13, work_mem 4 MB (captures/) |
| Mehlhorn & Sanders §5.7 is external sorting | Checked against the book PDF by the web-research agent (research/canonical_web_agent.md) |

## Review log

**Round 1** (fresh-context reviewers; expert REVISE, editor PASS, student lost "a few times").
- Expert, blocking: "a single pass, however many runs there are" is false beyond one block per run. Fixed: "as long as memory has a block for every run", and section 5 asks how many that is.
- Expert: GNU sort caps a merge at 16 by default, so the scale-up no longer implies sort merges thousands. The formula card notes the database-textbook meaning of B. SSD speed now "hundreds of times". Optimality scoped to sorts that treat items as indivisible.
- Student: lost on 18, 14, 1, 5 by ear and on the spoken formula. Every number now carries its reason (two to the eighteenth; pieces under twenty thousand; twelve, six, three, two, one), the formula is a silent card, and "more runs than blocks" became the step that derives it.
- Editor: section 5 was an "and then" list, now a chain (how many fit, then rounds, then optimal, then why databases do it). Added the equal-comparisons line that makes the race disprove the wrong model. Cut "paging". Fewer "sixteen"s.
- Not taken: the editor asked to change the simulated file's ratio so "twelve" is used once. Kept, and made explicit instead: a file twelve memories long makes twelve runs, which is why sort wrote twelve files.

**Round 2** (expert REVISE, editor REVISE, student lost "a few times").
- Both, blocking: the hook showed 1 GB against 160 MB (a ratio of about 6) but sort made twelve runs, because sort spent half its buffer on per-line bookkeeping; the only explanation was a screen footnote. Fixed at the source: re-captured with 1000-byte records and `-S 88M`, where runs are 84 MB and the file really is about twelve memories long, and Python re-captured under the same 88 MiB cap. Section 3 now says so.
- Expert: "the same amount of comparing" became "on the order of N log N"; external merge sort is defined generally ("as many at a time as memory allows"); "hundreds of terabytes" replaced by the canonical "two or three passes in practice"; "decides" became "dominates".
- Editor and student: the silent formula card and the Aggarwal and Vitter line moved to the end card (both flagged them as undecodable in passing); the rounds argument stays, in words, because it answers the student's round-1 question about more runs than blocks; "sweeps" renamed "passes" on screen; the stacked simulation sentence split.
- Student: added why heapsort thrashes under virtual memory (it compares items far apart; the array lives on disk block by block) and why presorting is allowed (merging only needs sorted pieces).

**Round 3** (expert REVISE on a screen label, editor PASS, student lost "a few times").
- Expert, blocking: the screen showed an 88 MB memory and "1 GB ≈ 12 × 84 MB" side by side (both real: runs are 84 MB because sort keeps line pointers). The card now states the narrated claim, "1 GB ÷ 88 MB ≈ 11.4, so 12 runs". Added the edition to the R&G citation. The Postgres line is already a verbatim capture.
- Student: every spoken derivation number moved to the screen ("two to the eighteenth", "twenty-two thousand"); "the last four" is now justified where it is said (fourteen replaced, four stay); "rounds" became "merge passes"; "logarithmically, in a base of thousands" became "thousands of times more data costs just one more pass"; the virtual memory line says what the OS keeps (recently used parts); the heap has "one entry per run".
- Editor: "multiway merge" is now spoken; a therefore joins sections 3 and 4 (runs are not sorted against each other); section 5 gives the concrete sixteen before the general rule; the definition of external merge sort separates the algorithm from the fan-in optimization (expert's nit too); the hook states the twelve-times ratio so the simulation matches sort's file by design, and the ending calls back to it.

**Round 4** (expert REVISE, editor PASS, student below).
- Expert, blocking: GB vs GiB. The file was 10^9 bytes but `-S 88M` is 88 MiB, so the real ratio was 10.8, not "about twelve", and the screen mixed decimal (1 GB ÷ 88 MB) with binary (16 GB ÷ 1 MB = 16,384). Re-captured with 10,000-byte records and an 86,000,000-byte buffer: 11.6 memories long, twelve runs of 85 MB, Python failing under the same cap. All units are decimal now.
- Expert, blocking: the Sort Method line appears only under EXPLAIN ANALYZE; narration and caption say so (the capture already used ANALYZE).
- Expert: "the same proportions" became "roughly the same proportions"; the screen gives the simulation's exact parameters so "a twelfth" and 21,760 reconcile.
- Student (retell fully correct; still lost on two spots): "eighteen passes" now carries its reason (eighteen doublings from one item to a quarter million); the crux gets its own beat ("the four merge passes collapse into one"); "a twentieth" is anchored to heapsort's count; "three I/Os per item" is marked as the simulation's figure.

**Round 5** (expert REVISE, editor PASS, student retell correct).
- Expert, blocking: the fan-in off-by-one survived in section 4 and in the closing rule. Now "a block for every run, plus one for the output" and "as many runs at once as memory has blocks to spare".
- Expert: "write it back" became "write it out to disk" (runs are new files); the ending keeps "about twelve"; the OS "keeps the parts it used recently" (real systems approximate LRU); "hundreds to thousands of times"; the end-card base is (M/B) − 1; the screen names GNU coreutils sort and the fixed 10,000-byte records, so the block arithmetic applies to the real run.
- Editor: passes are motivated (merge sort sweeps the whole file again and again); the heap is introduced as the fix for scanning thousands of fronts; the merge loop is walked through one concrete step; the halving is split into short phrases; the ending closes the Python thread (it tried to hold the whole file). The screen shows heapsort's far-apart comparisons before the race.
- Not taken, again: holding "that's what sort's twelve files were" until the ending. Confirming the viewer's inference at the moment it forms is the better teaching move; the ending still restates it.

**Round 6** (expert PASS, editor PASS, student retell covers every objective; still loses some spoken arithmetic, which the screen carries).
Polish applied before a final verification round: the formula card gets its inner ceiling and a precise note on R&G's notation; "blocks of 256 items"; sort's default of sixteen is called a conservative cap below the memory bound; Python fails "just reading it in"; "covers everything the first fourteen did" instead of "replaces"; section 5 opens with a "but" (a big enough file needs more runs than memory has blocks); the race states measured counts first (twice the comparisons, more than twenty times the I/Os); the two collapses are separated and end on "eighteen passes have become two"; "EXPLAIN ANALYZE" is said in plain words (ask PostgreSQL how it ran the query).

**Round 7** (expert REVISE, editor PASS, student retell correct).
- Expert, blocking: a block was "thousands of bytes" in section 2 but a megabyte in section 5's count. Section 2 now says "thousands of bytes at least", and section 5 says sorting programs read runs in big blocks, often a megabyte, to cut down on fetches.
- Expert: the merge's heap is contrasted with heapsort's (one entry per run, in memory the whole time); "three I/Os per item" is marked as the simulation's; the Python claim is about the naive script, not the language; "typically dominates".

**Round 8** (expert PASS, editor REVISE, student retell correct).
- Editor, blocking: heapsort was worse on both counts, so the race did not by itself disprove "comparisons decide speed". Added the time at typical speeds (comparisons a fraction of a second, I/Os more than a minute: "The I/Os decide"), and reordered section 2 so the mechanism comes before the measured numbers, matching the screen.
- Editor: the multi-pass claim is anchored in a worked case (a hundred thousand runs: seven after one pass, one after two); section 5 says real programs use bigger blocks than the simulation; the end card glosses "indivisible" as "whole records"; the closing screen shows 18 → 5 → 2 on the opening's bars instead of repeating the spoken rules.

**Round 9** (expert PASS, editor REVISE, student retell correct).
- Editor, blocking: "sort caps a merge at sixteen" contradicted the just-taught rule without a reason. The coreutils manual gives the trade-off (a small merge width reduces memory at the expense of merge performance), so the line now says sort is more cautious by default, trading some speed for less memory.

**Round 10** (expert REVISE, editor PASS, student retell correct).
- Expert, blocking (both introduced by the round-8 edit): "they would run about equally fast" taught "same big-O, same speed"; it now says comparisons alone would make heapsort at most about twice as slow, which the measured 1.97× confirms. The time estimate used 10 ns per comparison against a "hundreds to thousands" memory-to-disk ratio; it now charges each comparison a full memory access (~100 ns, 0.86 s total) against ~100 µs per I/O, a consistent 1,000×.

**Round 11:** expert PASS, editor PASS; the student's retelling answers the opening question and covers all four objectives. The student still reports losing some spoken arithmetic (eighteen, fourteen, seven), which the screen shows as it is said. Script locked.

**Harness fix before round 12.** SCRIPT.md had the round-1 review log between the script and the evidence table, and the extraction for reviewers used section boundaries that assumed the opposite order. From round 3 to round 11 the student and the editor therefore also saw the round-1 log, and the expert received no evidence table (it checked the claims independently). The file is now ordered argument, chain, ledgers, script, evidence, review log, and round 12 reruns all three reviewers on correctly extracted inputs.

**Round 12** (clean inputs): expert PASS, editor PASS, student retell correct. Both the expert and the editor flagged the same should-fix: "a hundred thousand runs, seven after one pass" came right after the spoken "sixteen", so a listener would divide by sixteen. Section 5 now gives sort's sixteen first, then the memory bound, and the example says "merging sixteen thousand at a time". The merge walkthrough no longer uses "block" in three senses in one breath.

**Round 13:** expert REVISE (blocking: the end card said "optimal"; Aggarwal and Vitter give a lower bound that multiway merge sort matches up to constant factors, for indivisible records, so it now says "asymptotically optimal" with that scope), editor PASS, student retell correct. The lock conditions were already met in round 12, so this round's should-fix items are applied once, and a final round decides: section 5's "and then" became "so"; the unspoken --batch-size flag left the screen; the Postgres line ties back to runs and merges and the screen highlights only the Sort Method line; the stacked simulation sentence is split; "each extra pass lets the file grow by that same factor of sixteen thousand" is derived from the numbers just given. Not taken: cutting GNU sort's sixteen and the Postgres line (the expert required the sixteen so the scale-up does not imply sort merges thousands; the Postgres line is the one real-system payoff).

**Round 14:** expert REVISE (blocking: "our file is twelve memories long" read as sort's file, which is 11.6 memories long; it meant the simulated file, which is exactly twelve), editor PASS, student retell correct. Section 3 now says "our simulated file is exactly twelve memories long", and sort's twelve files are "one run for each memory-full of its file, the last one only partly full".

**Round 15 (final):** expert PASS, editor PASS, student retell correct (remembers twelve runs, twice the comparisons against twenty times the I/Os, and 18 → 5 → 2). Locked. Stopping rule from here: no further edits to the narration; remaining should-fix items stay logged in the reviews.
