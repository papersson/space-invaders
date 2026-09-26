## 1. Points of confusion (quoted)

- **"While it works, twelve files appear in a temporary folder, and then they vanish."** — Two "twelves" show up close together (12x memory size, and 12 files) before it's said whether they're related. I wasn't sure yet if that was a coincidence or the actual point.
- **"We simulated both under virtual memory, on a quarter of a million items, with memory for a twelfth of them..."** then later **"Heapsort made about twice as many comparisons as merge sort, but more than twenty times as many I/Os: about three for every item it sorts."** — Three numbers (2x, 20x, 3-per-item) land in one breath. Hard to hold all three in my head at once just listening.
- **"For the first fourteen passes, every piece is smaller than memory."** — Where does fourteen come from? It's never stated out loud (it's log₂ of the memory size, which I only saw as a number on screen, 21,760). By ear this number feels like it fell out of the sky.
- **"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."** — This needs me to do 18 − 14 = 4, then +1 = 5 in my head in real time while listening. I lost the thread here for a second.
- **"Say a file needed a hundred thousand runs: one merge pass cuts them to seven, and one more makes them one file."** — I couldn't figure out how "a hundred thousand" turns into "seven." It seems to assume the ~16,000-runs-per-merge number from a sentence earlier, but that connection isn't spoken.
- The end-card formula **"passes = 1 + ⌈log_(M/B)−1 ⌈N/M⌉⌉"** — flashed as "for reference," but with subscripts and nested ceilings I couldn't parse it in the time it's on screen.

## 2. Questions I'd ask afterward

- How do you actually pick the block size in practice — is "often a megabyte" a rule of thumb or does it depend on the disk?
- Why does GNU sort deliberately cap itself at 16 runs per merge instead of using as many as memory allows, if more is supposedly better?
- Is the "one entry per run" heap in the multiway merge basically a heap of size = number of runs, so still O(log(number of runs)) per step? Is that ever a bottleneck?
- The video says "count I/Os, not comparisons" once data doesn't fit in memory — but how do you know in advance whether your data will fit? Is there a rule of thumb?
- Does this same run-then-merge idea apply to anything other than sorting?

## 3. What I learned (in my own words, ~150 words)

Normal sorting algorithms assume you can jump around in memory for free, but once your data is too big for RAM and lives on disk, that assumption breaks — every disk access pulls in a whole chunk of data at once, and those chunks are what actually cost time, not the comparisons. Heapsort jumps all over the place, so it constantly needs new chunks from disk and gets crushed by that cost even though it does the same order of comparisons as merge sort. Merge sort, on the other hand, reads and writes in a straight line, so it wastes way less. The trick "external merge sort" uses: first, sort chunks that fit entirely in memory and dump each one to disk as a sorted "run." Then merge all those runs together at once, reading a little bit of each and writing the combined result — which can be done in basically one more pass over everything. That's literally what the Unix `sort` command does under the hood.

## 4. Direct answers

- **One main idea:** When data doesn't fit in memory, what determines speed is the number of disk block-fetches (I/Os), not the number of comparisons — so you want an algorithm that touches memory in big, sequential sweeps ("passes") rather than jumping around, and you minimize passes by making sorted chunks as large as memory allows and then merging as many of them together at once as memory allows.
- **Numbers I remember:** twelve (the file is 12x memory, so it gets split into 12 sorted "runs"), eighteen (roughly how many merge-sort doubling passes it would take naively), and that it collapses down to two passes total (one to build the runs, one giant merge) — plus that GNU `sort` caps itself at merging 16 runs at once.
- **Starting question / answer:** It opened with "why does `sort` finish fine on a file 12x bigger than memory, and what are those 12 files that appear and disappear in /tmp?" Answer: those are the 12 sorted runs it builds because the file is 12 memory-loads long; it then merges all 12 at once (since memory has room for a block from each) and deletes them — so the whole job only takes two total passes over the disk.

## 5. Ratings

- **How much the opening hooked me:** 4/5 — the two side-by-side terminal runs (Python crashing vs. `sort` just finishing, with files mysteriously appearing/vanishing) is a genuinely compelling "wait, how?" moment.
- **How often I felt lost:** a few times — mainly around the "fourteen passes" number and the "hundred thousand runs → seven" example, where the arithmetic connecting numbers wasn't said out loud.
