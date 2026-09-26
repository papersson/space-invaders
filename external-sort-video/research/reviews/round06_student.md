Going through this once, as a listener rather than a reader.

## 1. Points of confusion (quoted)

- **"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed."** — I haven't studied OS, so this is a compressed explanation of a whole concept I don't really have footing for. I can follow it just enough to continue, but I'm not confident I could explain virtual memory back.

- **"Eighteen doublings take you from one item to a quarter of a million, so that's eighteen passes."** — "eighteen" lands with no obvious reason when just heard. I'd have to silently do 2^18 ≈ 262,144 to check it, and by the time I finish that the video has moved on.

- **"For the first fourteen passes, every piece is smaller than memory."** — same issue, a new precise number (14) that requires comparing 2^14 against the memory size (21,760) in my head, on the fly.

- **"That one pass replaces the first fourteen, and the last four stay. Eighteen passes become five."** — four numbers (18, 14, 4, 5) in two sentences. By ear I lost the thread here and had to trust the conclusion rather than verify it myself.

- **"Two at a time: twelve runs, then six, three, two, one. Four passes."** — five numbers said quickly; on a single listen I wasn't sure if that was 4 steps or 5 without counting on fingers.

- **"PostgreSQL's EXPLAIN ANALYZE reports an external merge."** — "EXPLAIN ANALYZE" is dropped in as if I'd know it. I don't know databases, so this is just a label to me, not something I understand.

- **"Sort itself stops at sixteen by default"** / the on-screen `--batch-size` — never explained why 16 specifically, feels like a loose thread.

## 2. Questions for the lecturer

- Can you walk through the heap-based multiway merge step by step with actual numbers — what's in the heap, what happens when a run's block runs dry?
- Why did GNU sort pick 16 as the default merge fan-in — is it about memory, or something else like file descriptor limits?
- Is a "block" the same as what an OS calls a page, or a different, bigger unit? Who decides its size?
- What happens if the file size isn't a clean multiple of memory size — do you get one smaller run at the end, and does that break anything?
- Could you re-derive the end-card formula slowly with the video's own numbers (261,120 items, memory 21,760, block 256)?

## 3. What I learned (in my own words, ~150 words)

When a file is way bigger than RAM, the thing that matters isn't how many comparisons your sort does — it's how many times you touch the disk, since disk gives you data back in whole chunks ("blocks") and each chunk is much slower to fetch than reading RAM. Heapsort jumps around its array randomly, so it constantly needs new blocks from disk. Merge sort reads and writes in order, so it wastes far less. The actual trick, "external merge sort," works like this: fill memory, sort that chunk in RAM, dump it to disk as a sorted "run," repeat until the whole file is chopped into runs. Then merge all the runs at once (not two at a time) using a small heap to always pick the smallest front item across every run. As long as memory has room for one block per run plus one for output, that whole merge is a single pass over the disk.

## 4. Direct answers

- **One main idea:** when data doesn't fit in memory, minimize disk passes (not comparisons) by sorting memory-sized chunks into runs, then merging all the runs at once in a single multiway pass instead of two-at-a-time.
- **Numbers I remember:** the file was 12x bigger than memory → 12 runs; sort caps a merge at 16 runs by default; the whole thing finished in 2 passes total (1 to make runs, 1 to merge). The 18→14→5 pass-counting sequence I remember existed but not the exact reasoning behind each number.
- **Question it started with:** what are the twelve files that appear and vanish in `/tmp` while Unix `sort` handles a file Python can't even load, and how does `sort` get away with it?
- **Answer:** those twelve files were sorted "runs" (one per memory-full); `sort` merged all twelve at once via a heap-based multiway merge, so the entire job only ever needed two passes over the disk.

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — files silently appearing and disappearing while a command "just finishes" is a genuinely good hook.
- **How often I felt lost:** a few times — specifically the arithmetic-heavy stretch in section 3 (18, 14, 4, 5) and the run-count halving in section 4, plus the unexplained "EXPLAIN ANALYZE" aside.
