# 1. Points where I'd lose the thread

> "We simulated both under virtual memory, on a quarter of a million items, with memory for a twelfth of them, roughly the same proportions as sort's file."

Three numbers in one breath (quarter million, a twelfth, "same proportions") — by the time I've done the division in my head, the next sentence has already started.

> "Heapsort keeps needing blocks that aren't in memory: about three I/Os for every item it sorts."

Where does "three" come from? I can see *why* heapsort would need more I/Os than merge sort, but not why the number is 3 and not, say, 10.

> "Eighteen doublings take you from one item to a quarter of a million, so that's eighteen passes."

I'd have to silently check that 2^18 ≈ 262,144 — heard aloud, I just have to take "eighteen" on faith.

> "For the first fourteen passes, every piece is smaller than memory."

Fourteen isn't derived out loud anywhere — I can't tell where it comes from without pausing the video.

> "That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."

18, 14, 4, 1, 5 all in two sentences — this is the moment I'd actually lose count.

> "Two at a time: twelve runs, then six, three, two, one. Four passes."

12→6→3 is halving, but 3→2→1 isn't — an odd run count doesn't obviously halve. I don't see what happens to the "leftover" run.

> "Sort itself caps a merge at sixteen runs by default... each merge pass divides the number of runs by thousands."

These two claims feel like they contradict each other — if the real tool only merges 16 at a time, how does one pass divide runs by *thousands*?

# 2. Questions for the lecturer

- Where does the "~3 I/Os per item" number for heapsort actually come from — is there a formula, or was it just measured?
- If memory can hold blocks for thousands of runs, why does GNU sort's real default cap it at only 16? Doesn't that mean more passes than necessary?
- When you merge 12 runs "two at a time" and get down to 3, how do you handle merging an odd number of things pairwise?
- Is the heap used in the multiway merge literally the same binary heap structure from heapsort, just with one entry per run instead of one per item?
- Can you plug our actual numbers into the end-card formula and show it really spits out "2 passes"?

# 3. What I learned, in my own words

When a file is way bigger than the memory you're allowed to use, comparisons stop mattering and disk fetches (I/Os) become the real cost, because every disk read pulls in a whole block, not one item. Heapsort jumps around in memory, so under these conditions it triggers tons of extra I/Os; merge sort reads and writes sequentially, so every block it touches gets fully used. The trick to make merge sort fast on disk: instead of doing tiny merges pass after pass, fill memory once, sort that chunk in RAM, and write it out as a "run." Do this repeatedly until the whole file becomes a handful of sorted runs. Then merge *all* the runs at once, in one pass, using a heap to always pick the smallest front item across runs. That's why sort only needed two total passes instead of many — one pass to build runs, one pass to merge them all.

# 4. Direct answers

**One main idea:** once your data doesn't fit in memory, minimize disk I/Os (not comparisons) by working in sequential "passes," and cut the number of passes by making runs as large as memory and merging as many runs at once as memory allows.

**Numbers I remember:** 12 (the file is 12x memory, and sort produced 12 runs), 18 (passes plain merge sort would need), 2 (passes external merge sort actually took), 16 (GNU sort's default cap on runs per merge).

**Question the video started with:** What are the twelve temporary files that appear and disappear while Unix `sort` handles a file 12x bigger than memory, and how does it avoid running out of memory the way Python does?

**Its answer:** Those files are sorted "runs" — sort fills memory 12 times, sorts each chunk in place, and writes it to disk as a run; then it merges all 12 runs together in one single multiway merge pass, so the whole file gets sorted in just two total passes over the disk.

# 5. Ratings

- **Pull of the opening (1–5):** 4 — a mystery ("files appear then vanish, what are they?") paired with a concrete, surprising fact (Python crashes, sort just works) is a strong hook.
- **How often I felt lost:** a few times — mainly in section 3 (the 18/14/4/5 pass arithmetic) and once more at the "16 vs. thousands" tension in section 5.
