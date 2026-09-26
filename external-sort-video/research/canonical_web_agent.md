# Canonical treatment: web-checked report (fresh-context subagent)

Produced by a subagent that had not seen the script, from the neutral prompt in
`canonical_prompt.md`, with web access to textbook slides, course notes and system source.
Condensed here to the points the script depends on; items the agent could not verify are marked.

## Canonical example and progression

- External (multiway) merge sort is the standard example in database and algorithms teaching:
  Ramakrishnan & Gehrke, *Database Management Systems* 3e, Ch. 13 "External Sorting";
  Silberschatz, Korth & Sudarshan 7e §15.4; Garcia-Molina, Ullman & Widom, *Database System
  Implementation* §2.3.4 "Two-Phase, Multiway Merge-Sort"; CMU 15-445; Berkeley CS186 note 8;
  Mehlhorn & Sanders, *The Basic Toolbox* §5.7; MIT 6.046 (2015) lecture 24; Knuth TAOCP Vol. 3 §5.4.
- Mehlhorn & Sanders: "Scanning data is fast in external memory and mergesort is based on
  scanning. We therefore take mergesort as the starting point."
- Database progression: "Why not just use QuickSort? (i.e., simply map disk pages to virtual
  memory)"; count page I/Os; two-way external merge sort (3 buffers, however much memory there
  is); general external merge sort (runs of B pages, merge B-1 at a time); refinements.
- Theory progression (Vitter; Mehlhorn & Sanders; MIT 6.046): memory hierarchy; EM model
  (N, M, B); scanning Θ(N/B); searching; sorting: RAM sort under paging, then binary merge sort
  with runs of size M, Θ((N/B) log₂(N/M)), then M/B-way merge sort, Θ((N/B) log_{M/B}(N/B));
  the Aggarwal-Vitter lower bound.

## Model and results

- Aggarwal & Vitter, CACM 31(9):1116-1127, 1988. N records, M records fit in memory, B records
  per block. Count I/Os (block transfers); computation is free.
- Notation trap: B is the block size in theory texts but the number of buffer pages in
  R&G / CMU / CS186; M counts items in theory but blocks in database books.
- Scan(N) = Θ(N/B). Sort(N) = Θ((N/B) log_{M/B}(N/B)), optimal in the comparison model /
  under indivisibility. Mehlhorn & Sanders eq. 5.1: 2(n/B)(1 + ⌈log_{M/B}(n/M)⌉) I/Os.
- Two passes suffice when N ≤ M²/B items (R&G: N ≤ B(B-1) pages). Real systems: "2-3 passes"
  (R&G); memory is shared between concurrent queries.
- Vitter §4.1: a RAM algorithm under paging can incur Ω(N log n) I/Os.

## Misconceptions (canonical corrections)

- CPU comparisons are the cost → count block I/Os.
- Virtual memory will handle it → paging does not fix a bad access pattern.
- The log base does not matter → the log base is the number of passes (30 vs 4 in R&G's table).
- Two-way merge sort on disk is fine → it uses only 3 buffers; multiway fan-in fixes it.
- "External sorting always takes two passes" is overstated.

## Real systems

- PostgreSQL tuplesort.c: sorts in memory until work_mem (default 4 MB), then writes sorted runs
  and does a balanced k-way merge; EXPLAIN reports "external merge".
- GNU sort: -S buffer, -T temp dir, --batch-size default 16 ("merge at most NMERGE inputs at once").
- SQLite, MySQL filesort, Hadoop spills (io.sort.factor = 10), Spark ExternalSorter, LSM-tree
  compaction. B-trees are the canonical search-structure counterpart (Θ(log_B N)).
