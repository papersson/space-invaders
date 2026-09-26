No web access granted, so I'll answer from established knowledge and flag anything I'm not fully certain of rather than guess.

## 1. Canonical worked example

**External (multiway) merge sort** is the flagship example in essentially every treatment of this topic — Aggarwal & Vitter's foundational paper (1988) uses sorting as the central problem, and Vitter's survey *"External Memory Algorithms and Data Structures: Dealing with Massive Data,"* ACM Computing Surveys 33(2), 2001, and his book-length treatment *Algorithms and Data Structures for External Memory* (Foundations and Trends in Theoretical Computer Science, 2008) both build the whole subject around it.

The **competing standard example is the B-tree** (external search structure), canonically from CLRS, *Introduction to Algorithms*, chapter "B-Trees" (ch. 18 in the 3rd edition; I'm not 100% certain of the exact chapter number in the 4th edition — treat that number as uncertain). CLRS frames B-trees explicitly as "algorithms for disk-based data structures."

Which is more common for an undergrad "external memory algorithms" lesson: **external merge sort**, because it's the cleanest illustration of *computing* on data that doesn't fit in RAM (the topic you named), whereas B-trees are usually taught inside a database/data-structures unit as the answer to "how do we *search* out-of-core data." If your course frames this topic as "databases and indexing," B-trees become the primary example instead.

## 2. Standard progression

1. **Motivate the failure of the RAM model**: standard Big-O analysis assumes uniform-cost memory access; this breaks when N ≫ M, because disk access is ~10⁵–10⁶× slower than RAM and is paid per *block*, not per element.
2. **Introduce the two-level I/O model** (below) with N, M, B (and sometimes D for multiple disks).
3. **Simplest primitive first: scanning** — reading/writing an array costs Θ(N/B) I/Os, not Θ(N). This is the "free lunch" fact everything else builds on.
4. **Simple external sort first: two-way (binary) external merge sort** — repeatedly merge pairs of runs, doubling run length each pass. This gives Θ(log₂(N/M)) passes and is shown as the naive/simple version.
5. **Generalize to k-way (multiway) merge sort** — use nearly all of memory as merge buffers so the fan-in k ≈ M/B, cutting the number of passes to Θ(log_{M/B}(N/B)). This is presented as *the* improvement the model is designed to expose (more RAM ⇒ fewer, not just faster, passes).
6. **State the matching lower bound** for sorting and permuting (Aggarwal & Vitter 1988).
7. **Transfer the idea to search structures**: B-trees, with node fan-out ≈ B, giving O(log_B N) I/Os per search — the data-structure analogue of the same "pay per block, so make the branching factor = B" principle.
8. *(Often, historically first)* Many courses note that this is a modernization of **Knuth's tape-based external sorting** (Donald Knuth, *The Art of Computer Programming, Vol. 3: Sorting and Searching*, §5.4, 1973/1998), which covers balanced/polyphase merge and *replacement selection* (a technique for producing initial runs of average length ≈2M instead of exactly M). Courses that want historical grounding introduce Knuth's tape model before the Aggarwal–Vitter disk model.

## 3. Model and notation

The standard model is the **Aggarwal–Vitter I/O model**, also called the **Disk Access Machine (DAM)** or **Parallel Disk Model (PDM)** when generalized to multiple disks (Aggarwal & Vitter, *"The Input/Output Complexity of Sorting and Related Problems,"* Communications of the ACM 31(9), 1988; extended to multiple disks by Vitter & Shriver, 1994).

Parameters (all counted in units of elements unless noted):
- **N** — number of elements in the problem instance
- **M** — number of elements that fit in internal (main) memory, M < N
- **B** — number of elements that fit in one disk block/page
- **D** — number of independent parallel disks (D = 1 in the basic single-disk model)

**What is counted**: the number of **block I/Os** — transfers of one block (B elements) between disk and memory. Internal (CPU) computation is treated as free/unlimited; only data movement between the two memory levels is charged. This is the key conceptual shift from RAM-model Big-O.

## 4. Key results with exact formulas

- **Scanning** N elements: `scan(N) = Θ(N/B)` I/Os.
- **Sorting** (Aggarwal & Vitter 1988): `sort(N) = Θ( (N/B) · log_{M/B}(N/B) )` I/Os.
- **Multiway external merge sort achieves this bound**:
  - Pass 1: form ⌈N/M⌉ sorted runs of length M (or longer with replacement selection), cost Θ(N/B).
  - Merge phase: merge with fan-in k = Θ(M/B) (one block of memory reserved per input run plus one output buffer), so the number of runs shrinks by a factor of Θ(M/B) each pass.
  - Number of merge passes: `Θ(log_{M/B}(N/M))`, each costing Θ(N/B) I/Os ⇒ total `Θ((N/B) log_{M/B}(N/B))`.
- **Permuting**: `Θ(min(N, (N/B) log_{M/B}(N/B)))` I/Os — same asymptotic bound as sorting, also from Aggarwal & Vitter 1988.
- **B-tree search** (CLRS, "B-Trees" chapter): height `Θ(log_B N)` (more precisely `log_t n` for minimum degree t ≈ B/2), so a search/insert/delete costs **O(log_B N)** I/Os.
- **Lower bound** (Aggarwal & Vitter 1988): sorting requires `Ω((N/B) log_{M/B}(N/B))` I/Os. This is proved under the **indivisibility assumption** — elements are atomic tokens that can be copied/moved/compared but not split into pieces and reassembled (rules out bit-trick shortcuts like radix sort exploiting structure across element boundaries). The bound also assumes the natural range `B ≤ M/2` (or similar; I'm not fully certain of the exact constant used in every presentation) so that a meaningful multi-pass regime exists.

## 5. Standard numeric worked example

This is the one place I'd flag real uncertainty: unlike, say, CLRS's recursion-tree examples, there isn't one single numeric example that's reproduced verbatim across all standard sources — Vitter's survey/book, and various course slides (e.g., CMU, Duke, KIT/Sanders' course), each construct their own illustrative numbers (e.g., sorting on the order of N=10⁹–10¹² elements with M in the 10⁶–10⁸ range and B a few KB, to show that log_{M/B}(N/B) comes out to roughly 2–4 passes, versus tens of passes for binary merging). I don't want to fabricate a specific textbook's exact figures and attribute them as verbatim quotes — for the video, I'd recommend constructing your own clean illustrative numbers (e.g., "1 TB of data, 1 GB of RAM, 8 KB blocks ⇒ ~3 merge passes with multiway merge vs. ~17 passes with binary merge") rather than presenting it as "the textbook example," since no single canonical one exists the way it does for, e.g., Dijkstra's algorithm's graph.

## 6. Standard misconceptions and how the canonical treatment corrects them

- **"Big-O from the RAM model still tells you what's fast."** Corrected by showing that an O(N log N)-comparison algorithm can be I/O-catastrophic (e.g., naive quicksort/heapsort touches memory in a pattern with poor locality) while a "worse" comparison count can have far fewer I/Os. The model explicitly decouples CPU cost from I/O cost.
- **"Virtual memory / OS paging already solves this."** The canonical treatment notes that OS page replacement (typically LRU-like) is *algorithm-agnostic* — it doesn't know the program's future access pattern, so naive algorithms thrash. External-memory algorithms are *designed* to control their own access pattern.
- **"You just do binary (2-way) merging until it's sorted."** This is presented deliberately as the naive first step, then corrected: because I/O cost is dominated by *number of passes*, and each pass costs Θ(N/B) regardless of fan-in, you should merge with the **largest fan-in memory allows** (Θ(M/B) instead of 2), which is the single biggest idea in the lesson.
- **"More I/O = only about disk seeks."** The model counts *block transfers*, not seeks per se; the correction is that B is chosen to amortize seek/rotational latency, and the model is about minimizing the number of such block transfers, not modeling seek time directly.
- **"The lower bound holds no matter what you do to the data."** Corrected by pointing out the **indivisibility assumption**: for special-case inputs (e.g., small-integer keys), external counting/radix-style approaches can beat the comparison-based bound, just as in the RAM model.

## 7. For a 5-minute video

**Essential:**
- Why RAM-model analysis fails (I/O time ≫ CPU time; disk access is a bottleneck).
- The model: N, M, B and "cost = number of block transfers."
- Scanning is (almost) free: Θ(N/B).
- External merge sort: create runs of size M, merge with fan-in ≈ M/B.
- The punchline formula: Θ((N/B) log_{M/B}(N/B)) I/Os, and why bigger M/B (more RAM, or a smart merge tree) means dramatically fewer passes.

**Common extra (include if time allows, cut first if not):**
- B-trees as the search-structure analogue, O(log_B N).
- One real-world example (see #8).

**Leave out:**
- Formal lower-bound proof (indivisibility argument).
- Parallel disks (D parameter), replacement selection, polyphase merge.
- Cache-oblivious algorithms, buffer trees, distribution sort as an alternative to merge sort.

## 8. Real systems canonically cited

- **B+-trees for database indexes** — virtually every RDBMS (canonically cited: standard textbooks Silberschatz/Korth/Sudarshan *Database System Concepts*, and Garcia-Molina/Ullman/Widom *Database Systems: The Complete Book*). Mechanism: index nodes sized to one disk page (fan-out ≈ B), giving O(log_B N) I/O lookups.
- **External sort-merge** in DBMS query processing — used for `ORDER BY`, `GROUP BY`, and sort-merge joins when data exceeds the buffer pool; this is the textbook DB-systems presentation of exactly the merge-sort algorithm above (same two references as above, chapter on query processing/external sorting).
- **Unix/GNU `sort`** — the classic systems example of external merge sort used on files larger than RAM (widely cited in course notes, though I don't have a single canonical academic citation for this — it's more of a "well-known fact" reference).
- **LSM-trees** (Log-Structured Merge-trees, O'Neil et al., *"The Log-Structured Merge-Tree (LSM-Tree),"* Acta Informatica, 1996) — used in BigTable, LevelDB, Cassandra, RocksDB. Mechanism: buffer writes in an in-memory table, flush as a sorted run (SSTable) to disk, and periodically merge (compact) runs — a direct application of run-generation + merging from external sort.

## 9. Claims commonly overstated or subtly wrong

- **"External memory algorithms are just RAM algorithms with disk instead of RAM."** Understates the point: the model changes what "efficient" means (block transfers, not operations), which changes which algorithm is optimal.
- **"SSDs make this topic obsolete because there's no seek penalty."** Overstated — SSDs still have a large but smaller random-vs-sequential and per-I/O-operation cost gap, and the block/page transfer model (and B-tree/LSM design principles) still governs real database and filesystem performance; only the *constants* changed, not the model's relevance.
- **"The Ω((N/B) log_{M/B}(N/B)) sorting bound is unconditional."** It relies on the indivisibility assumption; violate it (e.g., exploit key structure as in radix sort) and better bounds are possible in special cases.
- **"This is only a disk-vs-RAM story."** The same two-level analysis was later shown to generalize directly to the **CPU-cache-vs-RAM** gap via **cache-oblivious algorithms** (Frigo, Leiserson, Prokop, Ramachandran, *"Cache-Oblivious Algorithms,"* FOCS 1999), which is often mentioned as the modern extension but is advanced/out of scope for a 5-minute intro.

**Uncertainty flags recap:** exact CLRS chapter number in the 4th edition, and any single "the" canonical numeric worked example with fixed N/M/B figures — I did not find these reliable enough to state as fact rather than construct my own illustrative numbers.
