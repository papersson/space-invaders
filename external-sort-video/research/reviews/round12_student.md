## 1. Points where I'd lose the thread

- **"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."** — I've heard the term "virtual memory" before but never studied OS. This one sentence is my entire understanding of it; I'm not confident I could explain it back.

- **"By comparisons alone, heapsort would be at most about twice as slow."** — Where does "twice" come from? No derivation given, just asserted.

- **"Heapsort made about twice as many comparisons as merge sort, but more than twenty times as many I/Os: about three for every item it sorts."** — Three numbers in one breath (2x, 20x, 3 per item). Heard once, I couldn't hold all three.

- **"For the first fourteen passes, every piece is smaller than memory."** — Fourteen just appears. I can't tell where it comes from without pausing to do log math myself.

- **"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."** — This requires me to compute 18 − 14 = 4, then +1 = 5, in my head, in real time, while listening.

- **"Two at a time: twelve runs, then six, three, two, one. Four passes."** — Going from three runs to two isn't a clean halving like the rest of the sequence; it's not explained why.

- **"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."** — Seven comes out of nowhere. I don't know what fan-in (runs merged at once) is assumed here.

- **The end-card formula, "passes = 1 + ⌈log_{(M/B) − 1} ⌈N/M⌉⌉"** — flashed as text with no narration; too dense to parse from a single watch.

## 2. Questions for the lecturer

- How exactly do you get "fourteen" passes as the threshold where pieces are still smaller than memory?
- Why is heapsort "at most about twice as slow" in comparisons — what's that bound based on?
- In the 100,000-run example, what merge fan-in gets you down to seven runs in one pass?
- When you have an odd number of runs (like 3) in a two-way merge, what actually happens to the leftover one?
- Could you walk through the final formula term by term?
- Does GNU sort ever need more than one merge pass in practice, and when does its 16-way default become the bottleneck?

## 3. What I learned (in my own words, ~150 words)

Normal sorting assumes everything fits in memory. When the data is way bigger than memory — like a file twelve times the size — comparisons stop being what's slow; fetching blocks from disk (I/Os) is. Heapsort jumps around in memory, so under virtual memory it triggers tons of disk fetches, even though it does roughly the same number of comparisons as merge sort. Merge sort only reads and writes in order, so it wastes way fewer I/Os.

The trick "sort" uses: fill memory, sort what fits, dump it to disk as a "run," repeat — so a twelve-times-too-big file becomes twelve sorted runs in one pass. Then, instead of merging two runs at a time (which wastes most of memory), merge all the runs at once, since memory can hold one block from each run simultaneously. That's "external merge sort" — instead of ~18 passes over the data, you do it in about 2.

## 4. Answers

- **Main idea:** When data doesn't fit in memory, minimize disk I/Os (not comparisons) by working in ordered passes and merging as many sorted runs as possible at once.
- **Numbers I remember:** twelve (how much bigger the file was than memory, and the number of runs it got split into), eighteen (passes needed the naive doubling way), two (passes external merge sort actually took), sixteen (GNU sort's default number of runs merged at once).
- **Opening question:** What are the twelve files that appear and disappear in /tmp while `sort` runs, and how does it avoid running out of memory? **Answer:** they're sorted memory-sized chunks ("runs"); sort creates twelve of them, then merges all twelve at once in a single final pass — total of two passes over the data.

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — the side-by-side terminals plus the vanishing mystery files were a strong hook.
- **How often I felt lost:** a few times — mostly around the unexplained numbers (14, 18→5, the "seven" example) that needed mental math I couldn't do fast enough while just listening.
