# Review

## BLOCKING

**Quote 1:** "But a disk never fetches one number. It fetches a whole block, thousands of bytes…" (Section 2)
**Quote 2:** "…a laptop's memory holds thousands of blocks." + screen caption "16 GB ÷ 1 MB ≈ 16,000 blocks" (Section 5)

**What's wrong:** The video defines a "block" once, generically, as "thousands of bytes" (consistent with a real disk sector/page, ~512 B–4 KB). Section 5 then silently computes "thousands of blocks" in 16 GB by dividing by **1 MB**, a block three orders of magnitude larger than the one just defined. Divide 16 GB by an actual "thousands of bytes" block (say 4 KB) and you get **millions** of blocks, not thousands. This is a self-contradiction on the video's own load-bearing unit — the entire argument for why sort's 16-way cap is "conservative" rests on this number, and the two definitions of "block" given in the same script don't agree by a factor of ~250–1000×.

**Fix:** Pick one consistent block size and use it in both places, or explicitly flag the range: e.g. change "a laptop's memory holds thousands of blocks" to "a laptop's memory holds millions of blocks" and update the caption to "16 GB ÷ 4 KB ≈ 4,000,000 blocks" — or, if you want to keep the larger 1 MB figure (defensible as a *sequential-read buffer* size rather than a raw sector size), add a line in Section 2 acknowledging that "block," as used here, means whatever chunk a sort reads at once — anywhere from a few KB (a disk sector) up to a megabyte (a buffered sequential read) — so the two scenes aren't quietly using incompatible numbers for the same word.

## SHOULD FIX

**Quote:** "So give every run its own block of memory, and merge them all at once... With thousands of runs, scanning every front for the smallest item would be slow, so keep a heap with one entry per run."

**What's wrong:** Section 2 spent its whole argument blaming heapsort's poor I/O behavior on the fact that it's built on a heap ("Heapsort compares items that sit far apart in its array... heapsort keeps needing blocks that aren't in memory"). Section 4 then reintroduces a heap, with no acknowledgment of why *this* heap doesn't have the same problem. The two heaps are utterly different in scale: heapsort's heap has one entry per *item* and spans the whole disk-resident file; the merge heap has one entry per *run* (at most a few thousand, since even a huge file needs relatively few runs) and is always small enough to live entirely in memory — it never touches disk on its own. A sharp student is left to resolve this apparent contradiction unaided.

**Fix:** Add one clause, e.g.: "…so keep a heap with one entry per run — a handful to a few thousand values, small enough to sit in memory the whole time, unlike the item-sized heap that got heapsort into trouble."

---

**Quote:** "Under virtual memory that array lives on disk, block by block, so heapsort keeps needing blocks that aren't in memory: about three I/Os for every item it sorts."

**What's wrong:** "About three I/Os per item" is an artifact of this specific experiment's memory-to-file ratio (memory = 1/12 of the file); it is not a general property of heapsort. A viewer could easily walk away treating "~3 I/Os per item" as a constant fact about heapsort, the way "O(N log N) comparisons" is. It isn't — with less memory relative to N it would be worse, with more it would be better.

**Fix:** "…so heapsort keeps needing blocks that aren't in memory: in this run, about three I/Os for every item it sorts."

---

**Quote:** "Ask Python to load it and sort it, and it runs out of memory just reading it in."

**What's wrong:** This reads as a claim about the Python language/runtime rather than about the naive algorithm (load the whole file into a list, then call sort). Python is perfectly capable of external sorting (chunked reads, `heapq.merge`, etc.); the real point is that the *straightforward* approach fails, which is what the rest of the narration is building toward. As written it borders on the "overstated real-system claim" the instructions ask to watch for.

**Fix:** "Ask a simple Python script — read every line into a list, then sort it — and it runs out of memory just reading the file in."

---

**Quote:** "Once data doesn't fit in memory, the number of I/Os dominates the running time."

**What's wrong:** Stated as an unconditional fact; standard treatments (e.g., R&G, Aggarwal–Vitter) present this as the typical/dominant regime, not an absolute law (pathological CPU-heavy comparators aside).

**Fix:** "…the number of I/Os typically dominates the running time."

## NIT

- **Quote:** "Mehlhorn & Sanders, The Basic Toolbox, §5.7." — I can't independently confirm external sorting sits at exactly §5.7 in that text. Worth a citation check against the actual copy before this goes on screen, since a wrong section number in a citation card is exactly the kind of thing an expert viewer will catch.

- **Quote:** "on a quarter of a million items" for N = 261,120 — fine as spoken shorthand (off by ~4%), just flagging that it's an approximation, which the screen labels correctly ("2¹⁸ ≈ 262,144") but the narration doesn't.

- Not mentioned anywhere: replacement selection (building longer-than-memory-sized runs during run formation). This is optional for a 5-minute intro and I wouldn't spend the runtime on it, but if a version of this script ever grows a "how it's really done" appendix, it belongs there — real external sort implementations (and Knuth Vol. 3) use it to shrink the run count below the naive ⌈N/M⌉.

VERDICT: REVISE
