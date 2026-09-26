## 1. Points of confusion (quoted)

- **"treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."** — I get the gist, but I don't actually know *how* the OS decides what to keep. It's explained just enough to move on, not enough to picture the mechanism.
- **"Heapsort made about twice as many comparisons as merge sort, and more than twenty times as many I/Os."** — These numbers land before I know why the I/O gap is so much bigger than the comparison gap. I had to hold them in my head until the next sentence explained it.
- **"Eighteen doublings take you from one item to a quarter of a million, so that's eighteen passes."** — I can't check 2¹⁸ ≈ 250,000 in my head while listening; I just have to trust "eighteen."
- **"For the first fourteen passes, every piece is smaller than memory."** — Where does *fourteen* come from? It's never tied back to the memory size number out loud — I'd have to pause and do log₂(21,760) myself to see why fourteen and not some other number.
- **"Sorting programs read runs in big blocks, often a megabyte... and a laptop's memory still holds thousands of those."** — Wait, is this the same "block" as before (256 items in the simulation), or a totally different real-world size? It's not said whether these are the same concept at different scale or something new.
- **"each merge pass divides the number of runs by thousands."** — This is asserted quickly; I can infer it's because memory holds "thousands" of blocks, but the link isn't spelled out in the sentence itself.

## 2. Questions for the lecturer

- How does the OS actually decide which blocks stay in memory during virtual memory access?
- Can you show the actual arithmetic for why it's fourteen passes where pieces stay smaller than memory?
- Is the "block" in the real-world section (a megabyte) the same idea as the "block of 256 items" from the simulation, just bigger, or something different?
- Why did GNU sort's authors pick 16 as the merge cap instead of just using however many blocks memory allows?
- Is the "one entry per run" heap in the multiway merge implemented totally differently from a heapsort heap, or just used differently?

## 3. What I learned (in my own words, ~150 words)

Normal virtual memory doesn't save you when sorting huge files, because disks move data in whole blocks, not single items, and each block fetch is really slow. So what actually matters isn't how many comparisons your algorithm does, it's how many disk fetches (I/Os) it needs. Heapsort jumps around a big array constantly, so it triggers tons of I/Os. Merge sort reads and writes in order, so it wastes nothing. The trick "external merge sort" uses: first, chop the file into pieces that fit in memory, sort each piece in RAM, and write it back out as a "run." Then merge all those sorted runs together at once, giving every run its own little slice of memory, using a small heap to always grab the smallest current item. That turns what would be many, many passes over the file into basically two passes total — one to make the runs, one to merge them.

## 4. Main idea / numbers / question–answer

- **One main idea:** When data doesn't fit in memory, count disk I/Os instead of comparisons, and design the algorithm to read/write sequentially in as few full passes over the data as possible.
- **Numbers I remember:** twelve (the file was twelve memories big, and sort made twelve runs), eighteen (theoretical merge-sort passes without the trick), five and then two (after the run-forming trick, then after the multiway merge), and sixteen (GNU sort's default max runs per merge). I don't remember exactly why fourteen showed up.
- **Question it started with:** Why does a Python script run out of memory sorting a big file, while Unix `sort` just finishes — and what are those twelve temporary files it creates and deletes?
- **Answer:** `sort` never loads the whole file at once. It fills memory, sorts what fits, and writes that out as a "run" (that's the twelve files) — then merges all twelve runs at once in a single pass, using memory to track just the front of each run, so it only ever needs two total passes over the data.

## 5. Ratings

- **Hook strength (how much I wanted the answer):** 4/5 — the Python-fails-but-sort-succeeds setup with the mysterious appearing/vanishing files is a strong, concrete puzzle.
- **How often I felt lost:** a few times — mainly around the "fourteen passes" number and the shift in what "block" means between the simulation and the real-world section.
