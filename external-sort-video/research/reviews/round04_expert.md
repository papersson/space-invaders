I don't have web access in this session, so I'll rely on domain knowledge and flag confidence levels explicitly where verification would help. Here is the review.

---

## Findings

**1. BLOCKING — Inconsistent definition of "GB" makes two on-screen calculations mutually incompatible**

Quote (§3 screen): *"1 GB ÷ 88 MB ≈ 11.4, so 12 runs"*
Quote (§5 screen): *"16 GB ÷ 1 MB = 16,384 blocks"*

The first calculation only works if GB = 1000 MB (decimal/SI): 1000/88 ≈ 11.4. The second only works if GB = 1024 MB (binary/GiB): 16 × 1024 = 16,384. The same unit is used with two different conversion factors in the same video. This is exactly the kind of GB-vs-GiB sloppiness that a systems course would mark as wrong, and it also weakens the cold open: under the binary convention, 1 GB (1024 MB) ÷ 88 MB ≈ 11.6, which rounds to "twelve" honestly (nearest-integer), whereas 11.4 rounds to eleven — so the intro's "about twelve times bigger" is currently supported only by the ceiling used for run-count purposes, not by ordinary rounding.

Fix: pick one convention (binary is the natural choice, since it makes the memory-sizing example in §5 come out to a clean 16,384) and use it everywhere. Change the §3 caption to "1 GB ÷ 88 MB ≈ 11.6" (or state explicitly that GB here means 1024 MB), so it's consistent with §5 and makes "about twelve times bigger" a genuine round-to-nearest statement rather than a silent ceiling.

**2. BLOCKING — Overstates what plain PostgreSQL `EXPLAIN` shows**

Quote: *"When a query sorts more than fits in its memory, PostgreSQL reports an external merge."*
Screen: *"A real PostgreSQL EXPLAIN line: 'Sort Method: external merge'."*

`Sort Method:` (and the `Disk:`/`Memory:` line) only appears in the output of `EXPLAIN ANALYZE`, because it reports what actually happened during execution, not the planner's estimate. Plain `EXPLAIN` never executes the query and never prints a Sort Method line at all. As written, this claims real system behavior that isn't accurate for the tool named.

Fix: say "EXPLAIN ANALYZE" in both the narration and the caption, e.g. narration: *"...PostgreSQL's EXPLAIN ANALYZE reports an external merge"*; caption: *"A real PostgreSQL EXPLAIN ANALYZE line: 'Sort Method: external merge'."*

**3. SHOULD FIX — Screen figure doesn't match the number the narration implies**

Quote (narration, §2): *"Memory holds a twelfth of them"* — for 250,000 items, that's ≈ 20,833.
Quote (screen, §3): *"a line at memory size (21,760)"*

These are presented as the same quantity but differ by about 4%. A student who does the "N/12" arithmetic by ear and checks it against the screen will get a different number. This doesn't change the pass-count conclusion (both values fall between 2¹⁴=16,384 and 2¹⁵=32,768), but it's a factual mismatch as displayed.

Fix: either make the caption's memory-size figure equal to 250,000/12 (≈20,833), or add a word in the caption noting it's rounded to a whole number of blocks, so the two numbers are visibly reconcilable.

**4. SHOULD FIX — "the same proportions as sort's file" is not quite true**

Quote: *"Memory holds a twelfth of them, the same proportions as sort's file."*

Sort's actual file:memory ratio is ≈11.4–11.6 (depending on the GB convention — see finding 1), not exactly 12. "A twelfth" and "the same proportions" together assert an exact match that isn't there.

Fix: "roughly the same proportions," or retune the simulation to use the file's actual ratio rather than a clean 1/12.

**5. NIT — Verify the citation's section number before it airs**

Quote: *"Mehlhorn & Sanders, The Basic Toolbox, §5.7"*

I can't independently confirm from memory that external (memory) sorting sits at exactly §5.7 in this text rather than a neighboring subsection (e.g. one on parallel sorting appears nearby in that chapter in some editions). Since this appears as text on a citation card that students may look up, it's worth a direct check against the actual table of contents rather than trusting recall.

---

Everything else checked out as canonical and correctly caveated: the I/O-model terminology, the heap-based k-way merge description, the "block per run, minus one for output" fan-in bound, the pass-count derivations (18, 14, 5, 4, 2 all check out arithmetically against log₂ of the stated item counts), the Aggarwal–Vitter attribution and its "indivisible items" caveat, the GNU coreutils default merge order of 16 (`--batch-size`), and the general shape of the end-card formula relative to the standard Ramakrishnan–Gehrke / Garcia-Molina–Ullman–Widom presentation (correctly flagged as using a different meaning for B than the textbooks).

VERDICT: REVISE
