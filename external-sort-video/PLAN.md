# Bigger Than Memory: external merge sort in 5 minutes

**Working title:** *Bigger Than Memory: How to Sort a File That Doesn't Fit*
**Length:** ~5:00 (narration draft: 766 words ≈ 4:35 spoken, plus ~25 s of silent holds on the hero shots)
**Audience:** undergrad CS students who have seen merge sort, heaps and big-O,
but not the memory hierarchy or the I/O model.
**Format:** voice-over (Kokoro TTS) over animated diagrams. Every "real" number
on screen comes from a real run or a simulation, not an illustration.

## The canonical example, and why

**External merge sort**: sort a file much larger than RAM by (1) cutting it into
memory-sized sorted *runs*, then (2) merging many runs at once.

- It is *the* textbook example: the centerpiece of Aggarwal & Vitter's I/O model
  (1988) and of Knuth Vol. 3 §5.4.
- It starts from merge sort, which the audience already knows, so the new idea is
  the only new thing.
- It makes the one big lesson visible: **count block transfers, not operations**,
  and the payoff is a logarithm with a huge base (M/B instead of 2).
- It is what real systems actually run: GNU `sort`, database `ORDER BY`,
  MapReduce/Spark shuffles, LSM-tree compaction.

Alternatives considered: B-trees (searching; a great counterpart, so they get a
cameo in the "you've seen this" segment), blocked matrix multiply (a cache-level
story, less intuitive than "a file bigger than RAM"), and external BFS (too
advanced for 5 minutes).

## Learning objectives

After watching, a viewer can:

1. Explain why RAM-model complexity misleads once data exceeds memory: the cost is
   the number of trips to disk, and random access is the enemy.
2. State the I/O model's three numbers (N, M, B) and what a scan costs (N/B).
3. Walk through external merge sort's two phases and count their transfers.
4. Explain why merging ~M/B runs at once collapses the number of passes, and work
   out the numbers for a realistic machine.
5. Recognize the pattern in real systems (databases, big-data shuffles, LSM trees,
   B-trees, and cache vs. RAM).

## The through-line

**Your desk and a warehouse across town.** Memory is the desk: small, but anything
on it is instant. Disk is the warehouse: it holds everything, but every trip is
slow, and a trip costs about the same whether you bring back one item or a whole
crate (a block).

This becomes the video's fixed diagram: a small bright **memory tray** at the top,
a long dim **disk strip** at the bottom, and a **trip counter** in the top-right
corner. Once it appears in segment 2, the counter never leaves the screen: it ticks once per block
moved and is the only "cost" the video ever shows. When something is free (sorting
inside memory), the counter is visibly frozen.

## Running examples

| Example | Numbers | Used for |
|---|---|---|
| **The hook** | a 100 GB file, a laptop with 16 GB of RAM | cold open, scale-up math |
| **The toy** | N = 48 numbered cards, B = 4 cards per block, M = 16 cards (4 blocks) | every step-by-step animation |
| **The simulation** | N = 2¹⁸ keys, M = N/16, B = 256, LRU cache | the heapsort vs. merge sort race and the final scoreboard |
| **The real machine** | M = 16 GiB, B = 1 MiB → fan-in 16,383 | "how many passes", the quarter-petabyte line |

The toy is sized so memory is used exactly: the three runs of 16 cards need three
input blocks plus one output block, which is exactly 4 blocks = M. Phase 1 costs
24 transfers, the 3-way merge costs 24 more, 48 in total. The 2-way alternative
takes two rounds and 40 merge transfers instead of 24.

## Outline

| Time | Segment | What it covers |
|---|---|---|
| 0:00 | Cold open | Python runs out of memory sorting a 100 GB file; GNU `sort` finishes, and temp files pile up and vanish. "Those files are the whole trick." |
| 0:28 | The memory wall | Desk and warehouse. If memory = 1 s, then SSD ≈ 15 min and hard disk > 1 day. Trips, not operations. Heapsort vs. merge sort access-pattern race. |
| 1:25 | The I/O model | N, M, B. Computation is free; only block transfers count. A scan costs N/B. |
| 1:50 | Phase 1: runs | Fill memory, sort for free, write a run. Noise becomes a sawtooth. Cost: 2 scans. |
| 2:18 | Phase 2: the wide merge | 2-way merging leaves most of the desk empty. One buffer per run plus a small heap merges them all at once. Fan-in ≈ M/B, which is 16,383 on a real machine. |
| 3:28 | How many passes | Log base M/B instead of 2. 10 TB: 10 rounds vs 1. Two passes sort ~¼ PB. Optimal (Aggarwal & Vitter). Scoreboard. |
| 4:01 | You've seen this | Postgres "external merge", MapReduce/Spark shuffle, LSM compaction, B-trees, and cache vs. RAM. |
| 4:38 | Recap | Noise, then sawtooth, then gradient. Three rules. |

## Segment by segment

Narration is a first draft written for the ear. Parameter names are spoken as
words ("M over B") and formulas are described in words, never read aloud.

### 1. Cold open (0:00–0:28)

> Here's a hundred-gigabyte file, and a laptop with sixteen gigabytes of memory.
> Ask Python to sort it, and it runs out of memory. Ask the Unix sort command, and
> it just… finishes. While it works, files pile up in the temp folder, and then
> they vanish. Those files are the whole trick. This is how you compute on data
> that's bigger than your memory.

**Visuals.** A split terminal. On the left, `sorted(open("records.txt"))` with a RAM
gauge that climbs into the red, then `MemoryError`. On the right,
`sort records.txt -o sorted.txt`: its RAM gauge stays flat, and a `/tmp` panel below
fills with `sortXXXXXX` files that all grow to the same size, then disappear while
`sorted.txt` grows. Freeze on the pile of temp files, then the title card.

**Real data.** A scaled-down capture: a ~8 GB file with `sort -S 256M`, sampling
`ls -l /tmp` every 0.5 s and replaying it as a clean animated UI rather than a
screen recording. The Python failure is captured under a memory cap.

### 2. The memory wall (0:28–1:25)

> Picture memory as your desk, and the disk as a warehouse across town. The desk
> is small, but anything on it is instant. The warehouse holds everything, but
> every trip is slow. How slow? If reaching into memory took one second, a read
> from a fast SSD would take about fifteen minutes. A seek on a spinning hard
> drive: more than a day.
>
> There's one saving grace. A trip costs about the same whether you bring back one
> item or a whole crate. So what matters isn't how many operations you do. It's
> how many trips you make.
>
> On paper, heapsort and merge sort are both n log n. But heapsort hops all over
> the file, and makes about four trips for every item it sorts. Merge sort sweeps
> through in long, straight lines, and needs dozens of times fewer. And bigger
> crates only widen the gap.

**Visuals.**
1. A drawn desk and warehouse morph into the fixed diagram (tray, strip, road
   between them). The trip counter appears.
2. **Latency ladder:** a timeline that zooms out: memory 1 s → SSD ~15 min →
   hard disk ~28 h, drawn as a clock whose hand spins faster and faster.
3. **The crate:** a truck carries one card, then a full block, and the trip timer
   reads the same both times.
4. **Access-pattern race (hero shot):** two panels plotting *time* against
   *position in the file*. Heapsort is scattered dust and its counter spins;
   merge sort is clean diagonal sweeps, one per pass. The counters end at
   **978,178** vs **36,864**.

**Real data.** `iosim.py` (in this folder) records the access traces and LRU miss
counts. Quicksort is deliberately *not* the villain: its partitioning streams
through the data, so it behaves far better than heapsort on disk, and using it
would muddy the point.

### 3. The I/O model (1:25–1:50)

> Computer scientists turned this into a model with three numbers. N: how many
> items you have. M: how many fit in memory. B: how many come in one crate, called
> a block. Then one bold simplification: computation is free. The only cost is
> the number of blocks moved between disk and memory. Reading the whole file once
> costs N over B. That's our yardstick, and it's called a scan.

**Visuals.** The fixed diagram gets labels: N along the strip, M on the tray, B on
one block. A card reads "cost = blocks transferred" with the citation *Aggarwal &
Vitter, 1988*. One sweep across the strip ticks the counter to N/B, and the label
"1 scan" is stamped under it.

### 4. Phase 1: sorted runs (1:50–2:18)

> The classic algorithm is external merge sort, and it works in two phases. Phase
> one: fill memory, sort it right there, which is free, and write it back to disk
> as a sorted chunk called a run. Repeat until you've been through the whole
> file. It still isn't sorted, but now it's made of sorted runs. Every block was
> read once and written once: two scans.

**Visuals.**
1. **Toy:** 48 numbered cards, colored by value, in 12 blocks of 4. Four blocks
   fly up (+4), the cards slide into order inside the tray while the counter stays
   frozen with a "free" tag, and four blocks fly down as Run 1 (+4). Runs 2 and 3
   play in fast motion. The counter reaches 24.
2. **At scale (hero shot):** the file as millions of 1-pixel color columns.
   Random keys look like noise, and after Phase 1 they become a **sawtooth** of
   smooth ramps. Real keys, real run boundaries.

### 5. Phase 2: the wide merge (2:18–3:28), the centerpiece

> Phase two: merge the runs. You already know how to merge two sorted lists:
> compare the fronts, take the smaller, repeat. Merge the runs in pairs, then
> pairs of pairs, until one is left, and every round reads and writes the whole
> file.
>
> But look at memory while that happens. To merge two runs, you only need the
> front block of each, plus one block for the output. The rest of the desk sits
> empty.
>
> So use it. Give every run its own one-block buffer and merge them all at once.
> A small heap tracks which run has the smallest item at its front. Move that item
> to the output buffer. When the output block fills, write it out in one trip.
> When an input buffer runs dry, fetch that run's next block. Every block still
> makes exactly one trip in and one trip out.
>
> How many runs fit at once? About one per block of memory: M over B. With sixteen
> gigabytes of memory and one-megabyte blocks, that's over sixteen thousand runs,
> merged in a single pass.

**Visuals.**
1. **2-way merge (toy):** two input slots and one output slot light up. The fourth
   slot is grayed out and pulses "idle". Two rounds play quickly, 40 transfers.
2. **3-way merge (hero shot):** the three runs are conveyor belts on the disk
   strip. The tray holds three input blocks and one output block, and a 3-node
   heap above the input fronts highlights the current minimum. Cards move one at a
   time into the output. The output block flushes down (+1), an empty input slot
   pulls the next block of its run up (+1). The counter ends at 48 (24 + 24) and
   the strip ends as one smooth gradient.
3. **Scale-up:** the fan-in counter rolls from 3 to **16,383**, and the camera
   pulls back to thousands of hair-thin belts converging on one tray.

**How it's built.** A small instrumented implementation of the toy writes an
event log (load block, heap pop, flush, refill). The animation replays that log,
so every card move and counter tick is correct by construction.

### 6. How many passes (3:28–4:01)

> So the number of passes is still a logarithm, but its base is M over B instead
> of two, and that base is enormous. To sort ten terabytes on this laptop,
> two-way merging needs ten rounds over the data. The wide merge needs one. In
> fact, one pass to form runs plus one pass to merge can sort about a quarter of
> a petabyte. And it's optimal: in 1988, Aggarwal and Vitter proved that no
> comparison sort can do asymptotically fewer transfers. In our simulation, that's
> the difference between almost a million trips, and about four thousand.

**Visuals.**
1. **Passes chart:** x is data size from 16 GB to 1 PB (log scale), y is merge
   passes. The 2-way line climbs a staircase while the wide merge stays flat at 1
   until ~256 TiB. Mark "10 TB: 10 vs 1".
2. **Formula card (≤ 4 s):** transfers = 2 · (N/B) · (1 + ⌈log_{M/B}(N/M)⌉), which
   settles into Θ((N/B) · log_{M/B}(N/B)).
3. **Scoreboard:** three counters from the same simulation: heapsort 978,178,
   merge sort 36,864, external merge sort ~4,096.

### 7. You've seen this before (4:01–4:38)

> Once you know this pattern, you see it everywhere. When a database has to sort
> more rows than its memory budget, Postgres reports "external merge" and spills
> runs to disk. Big-data shuffles in MapReduce and Spark sort chunks, spill them,
> and merge. Storage engines like RocksDB write sorted files and keep merging them
> in the background. Searching gets the same treatment: a B-tree gives each node
> hundreds of children, so any of a billion keys is three or four trips away. And
> the desk and warehouse are relative: the same model describes cache versus RAM,
> and GPU memory versus the rest of the machine.

**Visuals.** Five quick cards, each reusing the tray-and-strip diagram:
1. **Postgres:** a real `EXPLAIN ANALYZE` capture with the line
   `Sort Method: external merge  Disk: …kB` highlighted.
2. **Shuffle:** mappers spill sorted runs, and reducers merge them.
3. **LSM tree:** the memtable flushes sorted files (runs), and compaction merges them.
4. **B-tree:** three levels with fan-out ~500. A search path lights up three nodes
   and the counter ticks +3.
5. **The hierarchy:** a pyramid (registers, cache, RAM, SSD, disk) with the "desk"
   and "warehouse" labels sliding up one level.

### 8. Recap (4:38–5:00)

> So, when data outgrows memory: count trips, not operations. Stream through the
> data instead of hopping around it. Build runs as big as memory, then merge as
> many as memory allows. That's external merge sort: a logarithm with a huge
> base, which is why sorting a file bigger than your RAM usually takes just two
> passes.

**Visuals.** A reprise of noise → sawtooth → gradient with the three rules
appearing beside it, then the end card with references.

## Visual build list

| # | Visual | Source | Tool |
|---|---|---|---|
| V1 | Split terminal + temp-folder panel | real capture (GNU `sort`, Python under a memory cap) | Python replay → Manim |
| V2 | Desk/warehouse → tray/strip diagram, trip counter | drawn | Manim |
| V3 | Latency ladder / clock | published latencies | Manim |
| V4 | Access-pattern race (hero) | `iosim.py` traces | matplotlib → Manim |
| V5 | I/O model labels, "1 scan" sweep | drawn | Manim |
| V6 | Toy run formation | toy event log | Manim |
| V7 | Noise → sawtooth → gradient strip (hero) | real keys, real runs | numpy + matplotlib |
| V8 | 2-way merge with idle slot | toy event log | Manim |
| V9 | 3-way merge with heap and buffers (hero) | toy event log | Manim |
| V10 | Fan-in roll-up and belt pull-back | computed | Manim |
| V11 | Passes vs data size chart | computed | matplotlib |
| V12 | Scoreboard | `iosim.py` | Manim |
| V13 | Five "seen it before" cards | Postgres capture, drawn diagrams | Manim |
| V14 | Recap strip and end card | reuses V7 | Manim |

The rest of the pipeline is unchanged from the UMAP video: Kokoro TTS narration
with per-line timings in `timings.json`, and ffmpeg for assembly.

## Style rules

- **Fixed geography:** memory is always at the top and bright, disk always at the
  bottom and dim. Reads move up, writes move down.
- **Blocks are atomic:** nothing crosses between disk and memory except whole
  blocks. A single card never travels alone. That is the model, so the visuals
  enforce it.
- **Values are color *and* number:** one perceptually uniform sequential colormap,
  so sorted reads as a smooth gradient and unsorted as noise. Toy cards also
  print their number, so color is never the only cue.
- **One accent for cost:** amber for every transfer arrow and counter tick; gray
  for idle memory. No red/green pairs.
- **The counter is honest:** it ticks only on block transfers and never on work
  done inside memory.
- **Math:** at most one formula on screen at a time, for ≤ ~4 s. The narration
  says it in words.

## Fact-check list

| Claim | Status / source |
|---|---|
| Memory ~100 ns, NVMe 4 KB random read ~50–100 µs, HDD seek + rotation ~8–12 ms → "1 s / ~15 min / > 1 day" | check against current datasheets and the "latency numbers" tables (Dean; Scott). 100 µs gives 16.7 min, 10 ms gives 27.8 h. |
| GNU `sort` spills to `$TMPDIR` as `sortXXXXXX` files and merges at most 16 at once by default | `--batch-size` exists in coreutils 9.4 here. Confirm the default of 16 and the temp-file lifecycle in the real capture. Needs about the file's size in free temp space. |
| Heapsort ≈ 4 trips per item; merge sort "dozens of times fewer" | simulated: N = 2¹⁸, M = N/16. With B = 256: 978,178 vs 36,864 (26.5×). With B = 64: 7×. The narration's "dozens" holds from about B ≥ 200. The external sort's 4,096 is from the formula, so simulate the actual algorithm next. |
| Fan-in M/B − 1 = 16,383 for 16 GiB / 1 MiB; two passes sort M·(M/B − 1) ≈ 256 TiB | computed |
| 10 TB with 16 GB runs → 625 runs → ⌈log₂ 625⌉ = 10 two-way rounds | computed |
| Aggarwal & Vitter, "The input/output complexity of sorting and related problems," *CACM* 31(9), 1988; Θ((N/B) log_{M/B}(N/B)) | the lower bound is for comparison-based sorting (and for permuting under the indivisibility assumption), so the narration says "comparison sort" |
| Postgres prints `Sort Method: external merge  Disk: NkB` when a sort exceeds `work_mem` (default 4 MB) | capture real output |
| Spark's default shuffle is sort-based and spills sorted data, then merges | worded loosely on purpose ("sort chunks, spill them, and merge") |
| B-tree fan-out ~500 → a billion keys in 3–4 levels | log₅₀₀(10⁹) = 3.33 |

## Risks and open questions

- **The heapsort ratio depends on B.** The "dozens of times" line depends on the
  block size chosen for the simulation. The honest framing, which the script
  already uses, is that heapsort's trips don't shrink with bigger blocks while
  merge sort's do. If you want a single dramatic number, use B = 512 (4 KB pages of
  8-byte keys) and quote whatever the simulation gives.
- **Real-world timing claims are avoided.** The cold open says `sort` "just
  finishes", not how long it takes, because that depends on the disk.
- **SSDs complicate "computation is free".** On fast NVMe, a well-tuned external
  sort can become CPU-bound. The model still counts the right thing, but I kept
  this caveat out of the narration. Say if you'd rather have one line on it.
- **Length:** the UMAP narration ran 720 words → 4:18 at Kokoro 0.92× with its
  pauses. At the same settings this 766-word script should land around 4:35, and
  ~25 s of holds (title card, the race, the sawtooth, the merge, the end card)
  bring it to ~5:00. Segment times above are estimated from word counts until
  the audio exists.

## If it can run longer

- **Replacement selection and Knuth's snowplow:** runs average 2M on random input,
  and already-sorted input becomes a single run.
- **Double buffering:** overlap disk and CPU, and trade fan-in for bigger reads.
- **Distribution sort:** the mirror image, which splits into ~M/B buckets using
  sampled pivots.
- **The permuting surprise:** in external memory, just rearranging data into a
  known order can cost as much as sorting it.
- **Cache-oblivious algorithms:** funnelsort is optimal without knowing M or B.
- **Blocked matrix multiply:** the same idea one level up, for cache.

## Suggested next steps

1. Render the narration with Kokoro and check its length.
2. Concept art for the four hero shots: the access-pattern race (V4), noise →
   sawtooth → gradient (V7), the 3-way merge tray (V9) and the passes chart (V11).
3. A shot-by-shot storyboard pinned to the narration timings.
