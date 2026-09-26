Verified: `sort --help` on this system (coreutils 9.4, matching the script's on-screen label exactly) confirms `--batch-size=NMERGE` exists with the description "merge at most NMERGE inputs at once; for more use temp files" — consistent with the script's claim. (No man page available to independently confirm the default value of 16, which I'm relying on training knowledge for.)

I worked through every numerical claim in the script by hand — the 261,120/21,760/256 simulation parameters, the 18→5→2 pass-count derivation, the comparison/I/O ratios, and the end-card formula's substitution against Ramakrishnan & Gehrke's standard cost formula — and all of it is internally consistent and correct. This is an unusually well fact-checked script. Findings below are the residual issues.

---

**SHOULD FIX**

Quote: *"Heapsort compares items that sit far apart in its array."*
Problem: Overgeneralized. In an array-based binary heap, a node at index *i* and its child at *2i* are only far apart for large *i* (deep in the tree); near the root (*i*=1 vs 2, or *i*=2 vs 4) they're adjacent or close. The claim is true in aggregate — across a full heapsort, enough comparisons touch large-index pairs to dominate I/O — but stated flatly it implies every comparison is non-local, which isn't so.
Fix: *"Heapsort's comparisons jump between array positions that are far apart whenever the node index is large — and across a full sort, enough of them are large that the heap has no useful sequential structure."*

Quote: *"every fetch takes hundreds to thousands of times longer than reading memory, even on a fast SSD."*
Problem: DRAM latency is ~100 ns; a fast NVMe SSD's random-read latency is commonly ~10–20 μs, which is roughly a 100–300x gap, not solidly into "thousands." "Thousands" only applies to slower SATA SSDs or spinning disks. As worded, the "even on a fast SSD" clause reads as asserting the high end of the range still holds for fast SSDs.
Fix: *"every fetch takes at least a hundred times longer than reading memory — into the thousands for a spinning disk, still tens to hundreds even on a fast SSD."*

**NIT**

Quote: *"Eighteen doublings take you from one item to a quarter of a million"*
Problem: The simulation's actual N is 261,120 (needed for the exact 1/12 and 256-item-block divisibility used later), about 4.4% above a literal quarter million. Harmless as a spoken rounding since the screen caption gives the exact figure, but worth a tighter phrase given how exact everything else in the script is.
Fix: *"...from one item to about 260,000"* (or leave as is if the imprecision is judged acceptable for narration).

Quote: *"treat the disk as memory: let the operating system keep the parts it used recently in memory, fetching the rest from disk as needed"*
Problem: This describes demand paging in general terms that blur swap-backed virtual memory and memory-mapped/page-cache file access — mechanically similar (both fetch on demand, evict on pressure) but not the same thing, and a precise database-systems framing would distinguish them.
Fix: acceptable as a simplification for the intended audience; if tightening, say *"...fetching the rest from disk, whether from swap or straight from the file, as needed."*

Quote: *"Ask PostgreSQL how it ran a query that sorts more than fits in its memory, and it reports an external merge."*
Problem: Stated as a flat rule. Postgres's tuplesort reports "external sort" (no caveat) only in the degenerate case where sorting produces a single run (no merge needed); anything producing more than one run — the normal case once data exceeds `work_mem`, and certainly the twelve-run case just shown — reports "external merge." The claim is very likely correct in the common case demonstrated, but stated unconditionally.
Fix: *"...and it typically reports an external merge"* — small hedge, no other change needed.

Quote: *"Ramakrishnan & Gehrke, Database Management Systems, 3rd ed., ch. 13"* and *"Mehlhorn & Sanders, The Basic Toolbox, §5.7"*
Problem: I can't verify exact chapter/section numbers against the physical editions from this environment. My recollection supports both (R&G 3rd ed. ch. 13 = External Sorting; Mehlhorn & Sanders' external-sorting material sits in their Sorting chapter, plausibly §5.7), but a citation on an end card should be checked against the actual book before airing, since a wrong number is an easy, embarrassing catch for anyone who owns the book.
Fix: confirm both citations against the physical/PDF editions before final production; no change needed if confirmed.

---

No claim, definition, or piece of arithmetic in the script is actually wrong, non-canonical, or overstated in a way that would make a domain expert object outright — the I/O model, the definitions of run/pass/external merge sort, the multiway-merge mechanics, the GNU sort and Postgres specifics, and the Aggarwal–Vitter/R&G attributions all hold up, and the pass-count arithmetic (18 → 5 → 2) and the end-card formula are exactly self-consistent with the simulation's stated parameters.

VERDICT: PASS
