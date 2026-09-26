## Review

Overall this script is unusually careful — nearly every headline number (18 passes, 14, 5, 12, 4, 2, the formula, the 84/12 arithmetic) checks out exactly once you trace it through, and the two‑phase narrative (naive merge sort → runs → multiway merge) matches the canonical external‑sort story. I did not find anything that is arithmetically wrong. The issues below are places where wording could mislead a sharp student or where the reference material isn't quite precise enough to survive a student going to the cited textbook.

---

**SHOULD FIX** — *"passes = 1 + ⌈log_{(M/B) − 1}(N/M)⌉"*
What's wrong: `N/M` is the number of initial runs only when it happens to be an integer (it is, in the video's own example — 12 exactly). In general the run count is `⌈N/M⌉`, and the formula as written omits that inner ceiling. This matters because it's presented as a standalone reference card, exactly the kind of thing a student will screenshot and compare against Ramakrishnan & Gehrke, where the formula does carry the inner ceiling.
Fix: `passes = 1 + ⌈log_{(M/B) − 1} ⌈N/M⌉ ⌉`

**SHOULD FIX** — *"database textbooks write B for buffer pages"*
What's wrong: this is trying to reconcile the script's own `B` (items per block) with the textbook's `B`, but as written a reader can easily misread it as "this means the same thing." It's also stated as if all database textbooks agree on this symbol (R&G does; others, e.g. Garcia‑Molina/Ullman/Widom, use different letters).
Fix: "(Ramakrishnan & Gehrke use B for the number of buffer pages — this script's M/B — and N for pages in the file — this script's N/B.)"

**SHOULD FIX** — *"blocks of 256"*
What's wrong: every other quantity in the video is unit-labeled (items, MB), but this caption isn't. Given the endcard formula explicitly defines "blocks of B items," a viewer can't tell if this is 256 items, bytes, or KB.
Fix: "blocks of 256 items"

**SHOULD FIX** — *"Sort itself stops at sixteen by default, which was plenty for twelve."*
What's wrong: placed right after the derivation that fan‑in is bounded by memory ("a laptop's memory holds thousands of blocks"), this leaves the impression that 16 is a memory-derived number. It isn't — GNU sort's default `NMERGE`/`--batch-size` cap of 16 is a conservative default (chiefly to bound simultaneously‑open temp files), far below what memory would actually allow. Worth one clause so students don't conflate "sort's default" with "the memory-based bound just derived."
Fix: "Sort itself defaults to a conservative cap of sixteen — well under what memory would allow, chosen partly to limit simultaneously open temp files — which was plenty for our twelve."

**SHOULD FIX** — *"Ask Python to sort it, and it runs out of memory."*
What's wrong: as phrased, this can read as "Python's sort algorithm is bad at this," but the actual cause is that reading the whole file into a list already exceeds memory before any sorting happens — it has nothing to do with Timsort specifically. Any naive "load fully, then sort" approach in any language fails the same way; the contrast being drawn is naive-in-memory vs. purpose-built-external, not Python vs. Unix.
Fix: "Ask Python to load and sort it, and it runs out of memory just reading the file in." (or similar — attribute the failure to loading, not to Python's sort)

**SHOULD FIX / NIT** — *"That one pass replaces the first fourteen, and the last four stay."*
What's wrong: this is presented as an exact substitution, but it isn't quite one. Fourteen doublings of naive merge sort produce runs of 16,384 items; direct run formation produces runs of 21,760 items (memory-sized) — larger, not the same size. The final pass count (five) still comes out right only because both `⌈log₂(261,120/16,384)⌉` and `⌈log₂(12)⌉` happen to equal 4 — the equivalence is in the *pass count*, not in the intermediate run size. Not wrong, but overprecise as stated.
Fix: "That one pass does at least as much work as the first fourteen, and the last four stay" — or drop "exactly" framing implied by "replaces."

**NIT** — *"Mehlhorn & Sanders, The Basic Toolbox, §5.7"*
Verify this section number against the actual book before it goes on screen; from memory this is plausible but I can't confirm it precisely without the text in hand.

**NIT** — *"1 GB of 10,000-byte records vs 86 MB"* vs. later *"1,000 MB ÷ 86 MB ≈ 11.6"*
The intro uses "1 GB," the later caption uses "1,000 MB" — implicitly decimal GB. It doesn't change the "twelve" outcome (ceil(1024/86) and ceil(1000/86) both give 12), but pick one convention and state it once to avoid a viewer doing the binary-GB math and being confused about which was meant.

**NIT** — omission of replacement selection. The video's run-formation method (fill memory, sort, write) is exactly what GNU sort does, so it's not wrong to skip replacement selection (the classic technique for producing runs averaging ~2× memory size). Not essential for a first correct understanding, but a curious student may ask "can runs be bigger than memory?" — worth a half-sentence pointer if room allows, not required.

**NIT** — the I/O-count model (as used throughout, correctly, to match Aggarwal–Vitter) charges every block transfer equally regardless of position. That's the right simplification for this video, but real spinning disks additionally pay a seek-time penalty for the non-sequential access heapsort produces, meaning heapsort's real disadvantage vs. merge sort is if anything understated by pure I/O counts. Optional aside, not a correction.

---

Nothing here reflects a false numerical claim, a misapplied law, or a genuinely non-canonical definition — the arithmetic (18→5→2 passes, N/M=12, (M/B)−1=84, the AV-scoped optimality claim, GNU sort's real `--batch-size` default, the Postgres `EXPLAIN ANALYZE` string) all check out. The fixes above are precision/caveat issues a professor would want tightened before this goes out, not blocking errors.

**VERDICT: PASS**
