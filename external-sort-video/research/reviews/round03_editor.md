# Script Review — External Merge Sort

## 1. One question
**Pass**, with a NIT.
Opening: *"What are those files, and how does sort get away with it?"* Ending: *"That's how sort handled a file far bigger than its memory: twelve runs, one merge, two passes."* The mystery is explicitly resolved and the mechanism named — the callback works because §3 and §4 already equated "twelve files" with "twelve runs."

- **NIT** — the very last line drops the word "files," relying on the viewer to remember the earlier equivalence.
  - Quote: *"twelve runs, one merge, two passes."*
  - Rewrite: *"twelve runs — its twelve files — one merge, two passes."*

## 2. But/therefore
The chain mostly holds (§5 was already repaired per the review log). One soft joint remains.

- **NIT** — §3 ends on the "twelve files" payoff, then §4 opens with a flat restart rather than a therefore.
  - Quote: *"...wrote out twelve runs. Now the runs have to be merged."*
  - Rewrite: *"...wrote out twelve runs. Those runs still aren't sorted **relative to each other** — so now they have to be merged."*

## 3. Derive, don't reveal
Strong overall — I/O, run, and external merge sort are all named only after the problem they solve is shown. No undereived ideas found.

## 4. Setups and payoffs
Full table of major items; only one broken pair found.

- **SHOULD FIX** — the memory cap is given as two different numbers for what should be the same figure: §1 sets up *"1 GB vs 88 MB"* / *"88 MB cap"*, but §3's screen caption pays it off as *"1 GB ≈ 12 × 84 MB."* A viewer doing the arithmetic along with the video will notice the mismatch right at the moment "twelve" is being proven.
  - Rewrite: use 88 MB in both places, or make the §3 caption `"1 GB ≈ 12 × 88 MB (≈1.06 GB)"`.
- **NIT** — the simulation's ratio ("quarter million items, memory for a twelfth") is presented as *coincidentally* matching the real sort demo's ratio: *"Its file was about twelve memories long too."* That "too" reads as luck, not design, which slightly undercuts confidence that the simulation models the real capture.
  - Rewrite: cut the redundant middle sentence — *"And that's what sort's twelve files were: it filled its memory twelve times and wrote out twelve runs."*

All other setups (twelve files, the question-mark freeze, eighteen passes, the four-pass two-way baseline, sixteen) pay off cleanly, several of them twice.

## 5. One vocabulary
- **SHOULD FIX** — "multiway merge" is a stated learning objective ("describe run formation and the multiway merge") but the term is never actually spoken; only "give every run its own block" is said. The concept is taught, the name is not.
  - Rewrite: add one clause in §4 — *"So give every run its own block of memory, and merge them all at once — a multiway merge."*
- **NIT** — after naming "run" the script reverts to "piece": *"...called a run. Then the next piece, and the next."*
  - Rewrite: *"...called a run. Then the next run, and the next."*

## 6. Number budget
Roughly 15+ distinct numbers are spoken (quarter million, a twelfth, three, a twentieth, two-to-the-eighteenth, eighteen, twenty-two thousand, fourteen, twelve, five, four, six, three, two, one, sixteen, thousands, two-or-three, two). Each is individually justified (per round 1's fix), but the aggregate is dense for a 5–6 minute video.

- The three worth remembering: **twelve** (files = runs), **sixteen** (merge width, explains why 12 fits and generalizes the mechanism), **two** (final passes). These are the ones repeated at the close.
- **SHOULD FIX** — offload some derivation arithmetic to screen-only text rather than narration, e.g. "two to the eighteenth" and "twenty-two thousand items" could be captions while the spoken line just says "about eighteen passes" / "roughly memory-sized." This keeps the ear tracking three numbers instead of a dozen.

## 7. Concrete before abstract
- **SHOULD FIX** — in §5 the general rule is stated before the concrete instance: *"One per block of memory, less one for the output. Sort itself stops at sixteen by default..."*
  - Rewrite: *"Sort itself stops at sixteen runs per merge by default — one per block of memory, less one for the output — which was plenty for twelve."*

## 8. Wrong model
Confronted and shown failing, not just asserted: the heapsort/merge-sort race under virtual memory, with matching N log N comparisons but wildly different I/O counts (~3/item vs <1/20th), directly disproves both halves of "comparisons decide speed, VM handles the disk." This is the strongest part of the script.

## 9. Depth over breadth
No violation — only one application (PostgreSQL EXPLAIN) is named, and it's shown concretely (a real EXPLAIN line), not listed alongside others.

## 10. Words and pictures
- **NIT** — screen text *"~N log N comparisons"* in §2 nearly duplicates the spoken line verbatim.
  - Rewrite: show the simulation's actual measured comparison counts for both algorithms instead of restating the formula.

## 11. Deletion test
Script is tight; only one line is genuinely cuttable (see §4 finding above: *"Its file was about twelve memories long too"*). No other lines found that could be cut without weakening a later beat or the takeaway.

## 12. For the ear
- Narration word count is **804** words against a stated target of "about 750" (within the 900-word/6-minute ceiling, but ~7% over target) — trim slightly, e.g. via the §6 number-budget cut above.
- **NIT** — *"cuts the number of runs by that same factor of thousands"* is awkward to say/parse (unusual plural "factor of thousands").
  - Rewrite: *"cuts the number of runs by that same factor — thousands at a time."*

---

**VERDICT: PASS**

(No item breaks the argument or leaves the wrong model unconfronted; the SHOULD FIX items are polish — a screen-caption number mismatch, one unspoken key term, and light number-density trimming.)
