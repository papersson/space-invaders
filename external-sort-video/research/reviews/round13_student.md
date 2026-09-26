## 1. Points of confusion (quoted)

- **"By comparisons alone, heapsort would be at most about twice as slow."** — Twice as slow as what factor, and why two? It's asserted, not derived. I know heapsort and merge sort are both N log N, but I don't see where the constant "2" comes from just from that.
- **"Heapsort made about twice as many comparisons as merge sort, but more than twenty times as many I/Os: about three for every item it sorts."** — Three separate numbers (2x, 20x, 3 per item) in one sentence. Listening (not reading), I lost track of which number attached to which claim.
- **"For the first fourteen passes, every piece is smaller than memory."** — Where does "fourteen" come from? I can guess it's related to memory size vs. doubling piece size, but the arithmetic isn't spoken, only shown on screen.
- **"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."** — I had to do 18 − 14 + 1 = 5 in my head on the fly; by the time I worked it out I'd missed the next sentence.
- **"a laptop's memory still holds about sixteen thousand of those [blocks]"** — This is presumably 16 GB ÷ 1 MB, but that division is only on screen ("16 GB ÷ 1 MB ≈ 16,000"), not said aloud, so listening alone I'd just have to take "sixteen thousand" on faith.
- **"Merging sixteen thousand at a time, one pass cuts them to seven, and one more makes them one file."** — Same issue: 100,000 ÷ 16,000 ≈ 6.25 → 7 isn't walked through verbally.
- **End card: "passes = 1 + ⌈log_{(M/B) − 1} ⌈N/M⌉⌉"** — Flashed at the very end with citation names (Ramakrishnan & Gehrke, Aggarwal & Vitter). Dense notation, no time to parse it, and it uses B/M for buffer pages vs. the video's own M/B terms, which the caption itself admits is a mismatch — confusing rather than clarifying.

## 2. Questions for the lecturer

- Where exactly does the "heapsort does about twice as many comparisons as merge sort" number come from?
- Can you walk through the arithmetic for "fourteen passes fit in memory" and "eighteen becomes five" step by step?
- In the multiway merge, when an item leaves the heap and a new block arrives for that run, how does the heap get fixed back up? (You mentioned heaps but not how they're maintained here.)
- Why does merging fewer runs at once (GNU sort's default of 16) save memory — is it just "one block held per run, so fewer runs = fewer blocks in memory at once"?
- What happens if the file size isn't a clean multiple of memory size — do the "twelve runs" still come out evenly?
- Could you show the general passes formula from the end card worked through with our actual numbers (N=261,120, M=21,760, B=256)?

## 3. What I learned, in my own words (~150 words)

If a file is way bigger than your RAM, sorting it isn't about picking a smarter sorting algorithm — it's about minimizing trips to disk, because each disk fetch grabs a whole chunk of data ("block") and is hugely slower than touching RAM. Heapsort looks fine on paper (same N log N as merge sort) but it jumps around memory unpredictably, so under virtual memory it triggers tons of disk fetches. Merge sort, by contrast, reads and writes in straight sweeps, so every block it touches gets fully used.

The trick real tools use ("external merge sort") is: first, fill RAM with as much of the file as fits, sort that chunk in memory, and dump it to disk as a "run." Do this repeatedly until the whole file is chopped into sorted runs. Then merge ALL the runs simultaneously in one pass, using one small heap to always pick the smallest current item — as long as memory has one buffer per run, this needs just one more pass. So a huge file gets sorted in something like two passes total, not dozens.

## 4. Main idea, numbers, question/answer

**One main idea:** When data doesn't fit in memory, count disk I/Os (not comparisons) as the real cost, and minimize passes by (a) making sorted chunks ("runs") as big as memory allows, then (b) merging as many runs at once as memory has room for buffers.

**Numbers I remember:** twelve (file is 12x memory size, and produces twelve runs); eighteen (naive pass count if you just doubled pieces one merge at a time) shrinking down to two passes with the real technique; sixteen / sixteen thousand (GNU sort's default merge width, and roughly how many 1MB blocks fit in a laptop's memory); "three I/Os per item" for heapsort vs. merge sort's much lower count.

**Question it started with:** Why does Unix `sort` succeed (creating and then deleting twelve mysterious temp files) on a file 12x bigger than the memory limit, while a naive Python script just crashes from running out of memory?

**Answer:** Those twelve files were sorted "runs," one memory-load's worth each. `sort` filled memory twelve times, sorted and wrote out each chunk (pass 1), then merged all twelve at once using one memory buffer per run (pass 2), so it only ever touched disk in two full passes instead of loading the whole file at once.

## 5. Ratings

- **Pull of the opening (1–5): 4.** The vanishing/reappearing temp files framed as a mystery ("what are those files, and how does sort get away with it?") made me want the payoff.
- **How often I felt lost: a few times** — mainly around the passage-count arithmetic (fourteen/eighteen/five) and the block-count numbers (sixteen thousand, seven runs after a pass), which relied on quick mental math or on-screen-only calculations that don't come through when just listening.
