Here's my pass through the script, staying in "haven't studied OS/DB/external-memory algorithms" mode.

## 1. Where I'd lose the thread

- **"The obvious fix is virtual memory: treat the disk as memory, and let the operating system keep the parts it used recently in memory..."** — I don't really know how the OS decides what to keep vs. evict. It's stated fast, like something I should already know.
- **"By comparisons alone, heapsort would be at most about twice as slow."** — Twice as slow, based on what? No derivation is given for that factor.
- **"Even if every comparison cost as much as a memory access, heapsort's comparisons would take under a second. Its I/Os take more than a minute."** — I later see this was based on ~100ns/comparison and ~100µs/I/O, but those numbers are only *on screen*, never spoken. Hearing the line alone, I can't check the math.
- **"For the first fourteen passes, every piece is smaller than memory."** — Where does "fourteen" come from? I'd have to freeze the screen and compare powers of two to the memory line myself; it isn't derived out loud.
- **"That one pass covers everything the first fourteen did, so only the last four remain. Eighteen passes become five."** — This is the biggest jump for me. I don't clearly see *why* one pass of "sort each memory-load in place" does the same job as fourteen passes of pairwise merging. It's asserted, not walked through.
- **"GNU sort merges up to sixteen at a time by default, a cautious setting..."** — Right after this we learn memory could support ~16,000-way merges. So why is the real default only 16? "Cautious" doesn't really explain the huge gap.
- **"Ask PostgreSQL how it ran a query... it reports an external merge."** — I don't know databases, so "PostgreSQL" and "EXPLAIN ANALYZE" are just unfamiliar names I have to take on faith.
- **The end-card formula**, `passes = 1 + ⌈log_(M/B)−1 ⌈N/M⌉⌉`, plus the note that another textbook uses B and N to mean different things than this video — that's dense notation-juggling I could not follow by ear at all.

## 2. Questions for the lecturer

- Where does the "heapsort is at most twice as slow by comparisons" bound actually come from?
- Can you show more concretely why 14 merge-passes get "replaced" by one run-forming pass — is that exact or approximate?
- Why does real `sort` default to only 16-way merges if memory could apparently handle a much bigger fan-in?
- How does the OS actually decide what to keep in memory under virtual memory (the "recently used" part)?
- Is the end-card formula something we're expected to derive, or purely a citation/reference?

## 3. In my own words (~150 words)

There's a neat trick `sort` uses on files way bigger than RAM. The obvious idea — just let the OS swap pieces to disk — fails because disk only gives you data in whole chunks ("blocks"), and each chunk takes ages to fetch compared to RAM. If your algorithm jumps around memory randomly (like heapsort), you rack up tons of these slow fetches even though it's not doing many more comparisons than merge sort. The fix: split the file into memory-sized chunks, sort each one entirely in RAM, and write it to disk as a "run." Then merge all the runs together at once — not two at a time — by keeping one block of each run in memory plus a small heap tracking the smallest front item, streaming blocks in and out as needed. That's "external merge sort," and it turns what could be many passes over the disk into basically just two: one to build runs, one to merge them.

## 4. Direct answers

- **One main idea:** When data doesn't fit in memory, what matters is minimizing disk fetches (I/Os), not comparisons — so you sort by making memory-sized sorted runs, then merging all of them at once in a single pass.
- **Numbers I remember:** the file being 12x memory (→ 12 runs); heapsort doing ~2x the comparisons but ~20x the I/Os of merge sort; and the pass count collapsing 18 → 5 → 2.
- **Starting question:** What are the temporary files Unix `sort` creates, and how does it sort a file 12x bigger than memory without running out of memory?
- **Answer:** Those files are sorted "runs" — the file split into memory-sized chunks, each sorted independently. `sort` then merges all twelve at once (multiway merge) instead of pairwise, finishing the whole job in about two passes over the disk.

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — the vanishing-files mystery plus the live Python-vs-`sort` demo was a strong hook.
- **How often I felt lost:** A few times — mainly around the pass-count derivation (18→5→2) and the notation in the end-card formula.
