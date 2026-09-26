## 1. Points of confusion (quoting as I heard them)

- **"By comparisons alone, heapsort would be at most about twice as slow."** — stated with no derivation yet; I have nothing to hang "twice" on until much later when the measured numbers show up.
- **"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."** — I don't really know how an OS does this "automatically"; I can follow the gloss but I'm not sure how much is being hidden here.
- **"Eighteen doublings take you from one item to a quarter of a million, so that's eighteen passes."** — this requires me to silently verify 2^18 ≈ 250,000; by ear I just have to trust it.
- **"For the first fourteen passes, every piece is smaller than memory."** — another number (fourteen) dropped without me being able to check it against memory size in my head while listening.
- **"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."** — this is arithmetic (18 − 14 + 1 = 5) done live in the narration; I lost the thread here and had to just accept the result.
- **"Add the pass that made the runs, and eighteen passes have become two."** — this calls back to "eighteen" from much earlier, and by now I'd half-forgotten that number.
- **"Say a file needed a hundred thousand runs: one merge pass cuts them to seven"** — I don't see how 100,000 runs becomes seven. It seems to assume a much wider merge than the "sixteen at a time" GNU sort default mentioned one sentence earlier, but that's never reconciled out loud.

## 2. Questions for the lecturer

- Where does the "heapsort ≈ 2x the comparisons of merge sort" number actually come from — is that a general fact or specific to this experiment?
- Is `sort` actually using OS-level virtual memory internally, or does it manage its own disk I/O directly and virtual memory was just the "obvious but wrong" strawman?
- In the 100,000-runs example, what merge width are you assuming to get down to seven runs in one pass — is that a thousands-wide merge, not the 16-way default you just mentioned?
- Why does GNU sort cap merges at 16 by default instead of using a much wider merge (since you said memory can hold thousands of blocks)?
- How exactly do you decide "the first fourteen passes are smaller than memory" — is it just log2(memory size in items)?

## 3. What I learned (in my own words, ~150 words)

When a file is too big for RAM, what actually kills performance isn't the number of comparisons — it's how many times you have to fetch data from disk, since each disk fetch grabs a whole block and is much slower than touching RAM. Heapsort is bad here because it jumps all over the array; merge sort is good because it reads and writes in order, so every block it loads gets fully used. The trick is: fill memory with a chunk of the file, sort that chunk in RAM, and write it back out as a sorted "run." Do that repeatedly to turn the whole file into a small number of runs. Then merge all the runs at once — one memory block per run, plus a small heap to pick the next-smallest item — in a single pass. That's how the real `sort` command finishes a file way bigger than memory, instead of crashing like naive Python.

## 4. Direct answers

- **One main idea:** When data doesn't fit in memory, count disk I/Os instead of comparisons, and minimize passes by sorting memory-sized chunks into runs, then merging as many runs at once as memory allows.
- **Numbers I remember:** twelve (how much bigger the file is than memory, and the number of runs/temp files it creates), two (total passes `sort` needs — one to make runs, one to merge them all), sixteen (GNU sort's default cap on runs merged at once). I'm fuzzy on the "eighteen" and "fourteen" — those came and went too fast to stick.
- **Starting question / answer:** It started with: what are the twelve temp files Unix `sort` creates and deletes, and how does it avoid running out of memory? Answer: those files are sorted "runs," one per memory-full of the input; `sort` builds twelve of them, then merges all twelve at once in a single pass, so the whole sort takes just two total passes over the disk.

## 5. Ratings

- **Desire to know the answer after the opening (1-5): 4** — the disappearing/reappearing twelve files is a concrete, weird hook.
- **How often I felt lost: a few times** — mostly around the pass-count arithmetic in section 3 (eighteen → fourteen → five) and the "cuts them to seven" jump in section 5.
