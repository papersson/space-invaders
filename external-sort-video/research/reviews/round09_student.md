## 1. Points where I'd lose the thread

- **"Ask the Unix sort command, with the same memory, and it just finishes."** — I don't really know what "Unix sort command" is other than some command-line tool; I'll take it on faith it's comparable to the Python script.

- **"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."** — This is thrown at me fast. I don't know how operating systems manage memory, so I have to trust this definition without being sure I've got it right.

- **"But watch the size of the pieces. For the first fourteen passes, every piece is smaller than memory."** — Where does *fourteen* come from? I can kind of tell it's tied to memory size vs. piece size doubling, but by ear alone this number just appears.

- **"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."** — This is mental arithmetic (18 − 14 = 4, plus 1 = 5) delivered in one breath. I'd have to rewind to actually verify it.

- **"Add the pass that made the runs, and eighteen passes have become two."** — Now I have to remember *both* that it was "eighteen becomes five" earlier *and* "four passes become one" from the merge section, and combine them. That's a lot to hold in my head just from listening.

- **"Sort itself caps a merge at sixteen runs by default, a conservative limit, and plenty for our twelve."** — Why sixteen specifically? It feels like an arbitrary number dropped in with no derivation.

- **"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."** — I have no idea how we get from 100,000 to seven. There must be a "how many runs fit in memory" number behind this, but it's not spoken, only (apparently) shown on screen.

- **"At typical speeds (~10 ns per comparison, ~100 µs per I/O)"** — these numbers are just asserted as "typical" with no source given.

## 2. Questions for the lecturer

1. How exactly did we get "fourteen" passes as the cutoff for "smaller than memory"? Is there a simple formula I could redo myself?
2. Can you walk through the 18 → 5 → 2 pass arithmetic on the board, slower?
3. Where does the "100,000 runs → seven after one pass" number come from? What's the actual formula being used at the end?
4. Why does GNU sort cap merges at sixteen runs specifically? Is that just a historical/empirical choice, or is there a reason?
5. Is virtual memory something every program uses automatically, or does a programmer have to opt in?
6. Are the 10ns/100µs timing numbers something I should just memorize as "typical," or do they vary a lot in practice?

## 3. What I learned (in my own words, ~150 words)

Normal sorting algorithms assume everything fits in memory. If your file is way bigger than memory — say twelve times bigger — a naive Python script just crashes, but the Unix `sort` command doesn't, because it's smart about disk access. The key insight is that once data lives on disk, what actually costs you time isn't comparisons, it's "I/Os" — fetching whole blocks from disk — because each one is enormously slower than an in-memory comparison. That's why heapsort, despite being N log N just like merge sort, is much worse here: it jumps around the array, causing tons of scattered disk fetches, while merge sort reads and writes in order. The trick `sort` uses: first, sort memory-sized chunks of the file in memory and write each one out as a sorted "run" (that's what those mysterious temp files were). Then merge all the runs at once in a single pass, using a small heap to track the smallest front item. So instead of many passes over the disk, you only need two: one to make runs, one to merge them.

## 4. Answers

- **One main idea:** When sorting data too big for memory, minimize disk I/Os (not comparisons) by working in as few full passes over the file as possible — do this by sorting memory-sized "runs," then merging all of them at once.
- **Numbers I remember:** *twelve* (the file is twelve times bigger than memory, and twelve runs get created); *eighteen down to two* (the number of passes merge sort would naively need vs. what the run-based approach actually takes); *sixteen* (the default cap on how many runs `sort` merges at once) — though I couldn't independently reconstruct where the fourteen, five, or seven numbers came from.
- **Opening question / answer:** It started with: what are the twelve files that appear and vanish in `/tmp` when Unix `sort` handles a file too big for memory, and how does it avoid running out of memory the way a naive script does? The answer: those files are sorted "runs" — one per memory-load of the file — and `sort` merges all twelve at once in a second pass, so the whole job only takes two passes over the disk instead of many.

## 5. Ratings

- **Desire to know the answer after the opening (1–5):** 4 — the vanishing/reappearing files in `/tmp` is a genuinely intriguing hook, concrete and visual.
- **How often I felt lost:** A few times — mainly around the pass-count arithmetic (18→14→5, and 18→2) and the unexplained "sixteen" and "hundred-thousand-runs-to-seven" numbers, which relied on visuals or quick mental math I couldn't fully do just by listening.
