## 1. Points where I'd lose the thread

- **"The obvious fix is virtual memory: treat the disk as memory, and let the operating system move data in and out as needed."** — I know the phrase "virtual memory" vaguely, but this doesn't tell me *how* the OS decides what to move in and out. It's treated as already understood.

- **"We simulated both on about a quarter of a million items, with memory for a twelfth of them, running under virtual memory."** — two numbers ("quarter of a million" and "a twelfth") stacked in one sentence, by ear. I lost track of which one was the file size and which was the memory size for a second.

- **"A quarter of a million is about two to the eighteenth, so that takes eighteen passes."** — this is mental math (250,000 ≈ 2¹⁸) delivered as a fact. I can't verify it while listening, I just have to trust it.

- **"But memory holds about twenty-two thousand items, and for the first fourteen passes, every piece is smaller than that."** — where did twenty-two thousand come from (I'd have computed 250,000/12 ≈ 20,800, close but not exactly what's said), and where does fourteen come from? Nobody walks through log₂(22,000) ≈ 14.4 out loud.

- **"Eighteen passes become five: one to make the runs, and the last four to merge them."** — at this point in the script, the "four" hasn't been justified yet — the halving 12→6→3→2→1 that explains it only shows up in the *next* section. So this claim doesn't yet follow from anything I've been told.

- **"With even more runs than that, you merge in rounds, and each round cuts the number of runs by that same factor of thousands."** — is a "round" the same thing as a "pass," or something different? Introducing a new word here for something that sounds identical to what was already called a pass threw me.

- **"So the number of passes grows only logarithmically, in a base of thousands."** — I know what a log is from Big-O, but "logarithmically, in a base of thousands" as a spoken phrase is hard to turn into a mental picture without seeing the formula.

- The end-card formula, **passes = 1 + ⌈log_{M/B − 1}(N/M)⌉** — this is on-screen only, and I don't know ceiling-function or subscript-log-base notation well enough to parse it in the few seconds it's up.

## 2. Questions for the lecturer

- Can you actually walk through where 22,000 and fourteen come from, step by step, instead of stating them?
- Is a "round" (section 5) the same thing as a "pass" (used everywhere else), or is it genuinely different?
- Before you explained the 12→6→3→2→1 halving, you already said merging takes four passes — can you show that math *before* using the number?
- In the multiway merge, is the heap over the "fronts of all runs" literally the same min-heap data structure I already know, just with one entry per run? How many items are in it at once?
- Why exactly does heapsort's access pattern land on far-apart blocks — could you show the array indices and which block they fall into?
- Does the run size always divide evenly like this, or was 12 runs a convenient made-up number for the example?

## 3. What I learned, in my own words (~150 words)

When a file is way bigger than your program's memory, the thing that actually costs you time isn't the number of comparisons anymore — it's how many times you have to fetch a chunk of data from disk, because disk always hands you a whole block, not just the one number you wanted, and that's way slower than memory. Heapsort jumps around a big array constantly, so it keeps needing new blocks — bad. Merge sort reads and writes in order, so every block it grabs is fully used — good. The trick is: first, sort chunks that already fit in memory and write each one back as a sorted "run" — no disk cost there. Then merge all those runs together in one go, using one block of memory per run, picking the smallest front item each time. If you have a block for every run, that merge is just one more pass. Fewer passes over the whole file = the whole speedup.

## 4. Direct answers

**One main idea:** When data doesn't fit in memory, count disk fetches (I/Os), not comparisons — and the way to minimize I/Os is to always read/write data in sequential passes, first packing memory-sized sorted "runs," then merging as many runs at once as memory allows.

**Numbers I remember:** twelve runs, sixteen as the default max runs sort merges at once, two passes total at the end, and "three I/Os per item" for heapsort vs. "less than a twentieth" of that for merge sort. I'm shakier on the exact 250,000/22,000/fourteen/eighteen numbers — those blurred together.

**Question it started with / answer it gave:** It started with "what are those twelve temporary files sort makes, and how does it sort a file bigger than memory without running out?" The answer: sort split the file into twelve memory-sized sorted runs (one pass), then merged all twelve at once using one memory block per run (a second pass) — two passes total instead of the eighteen a naive merge sort would need.

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — the disappearing/reappearing twelve files was a genuinely good hook.
- **How often I felt lost:** a few times — mostly around the spoken arithmetic (18, 22,000, 14) and the "four merge passes" claim showing up before its justification.
