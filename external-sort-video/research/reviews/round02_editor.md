# Script Review — External Merge Sort Explainer

## 1. One question

**Finding (NIT).** The opening asks two things: *what are the twelve files* and *how does sort get away with it*. Both are explicitly answered — but the actual reveals land mid-video ("**And that's what sort's twelve files were**," §3; "**It's exactly what sort did at the end**," §4), so by the time §6 recaps ("twelve runs, one merge, two passes"), the ending is a summary of an already-resolved mystery, not the moment of payoff. It still explicitly calls back, so this passes, but the "aha" is spent early.
> Rewrite: hold back one reveal — e.g., cut "And that's what sort's twelve files were" from §3 and move it to §6, so the ending delivers the file-count answer for the first time alongside the rule.

## 2. But/therefore chain

Segment-by-segment, joined:

Python OOMs **but** sort finishes and drops twelve mystery files — **therefore** what are they? **But** the obvious fix (virtual memory) doesn't save you, because disk fetches whole slow blocks, **so** I/O count, not comparisons, decides speed — **therefore** measure algorithms in passes. Merge sort needs 18 passes, **but** the first 14 fit entirely in memory, **so** presort those into runs — **therefore** 18 passes become 5, **and that's** sort's twelve files. Merging is still 4 passes, **but** two-way merge wastes memory, **so** give every run its own block and merge all at once — **therefore** 5 passes become 2.

**Finding (SHOULD FIX).** §5 breaks the chain. It's stitched with "**and then**"-style additions rather than causal links: default batch size → "**and then** rounds when there are more runs than fit → **and then** Aggarwal-Vitter proved it's optimal → **and then** databases do this too." None of these facts is forced by a felt problem; they're appended.
> Rewrite: cut to one consequence: "So how many runs fit? As many as memory holds blocks for — on a real machine, thousands, which is why two passes usually suffice even for huge files. That's why database engines sort exactly this way." Drop the rounds/logarithm aside and the citation (see §9, §11).

## 3. Derive, don't reveal

Good derivations: I/O cost (from "a disk fetches a whole block, slowly"), runs (from "the first 14 passes fit in memory — so do exactly that"), multiway merge (from "the rest of memory sits idle — so give every run a block").

**Finding (SHOULD FIX).** The passes formula is revealed, not derived.
> Quote: *"Silent formula card (4 seconds): passes ≈ 1 + ⌈log_{M/B}(N/M)⌉"*
> It appears right after a hand-waved "divides by thousands" line with no worked example. Rewrite: cut the card. If you want the audience to leave with the shape of the idea, say it in words only ("each merge round divides the run count by however many fit in memory at once — that's why the pass count barely grows even for huge files") and skip the symbolic formula entirely.

**Finding (NIT).** "Aggarwal and Vitter... proved" is an announced fact (see §9) — no derivation offered, just a citation.

## 4. Setups and payoffs

| Setup | Payoff |
|---|---|
| 1 GB file / 160 MB memory (§1) | Never explicitly reconciled with "twelve" — see BLOCKING finding below |
| Twelve `sortXXXXXX` files, frozen with "?" (§1) | §3 "sort's twelve files" ✓, §4 "exactly what sort did" ✓, §6 recap ✓ (paid off three times — see §1 finding) |
| N log N (§2) | Contrasted with I/O costs in same beat ✓ |
| 3 I/Os/item (heapsort) vs <1/20 (merge sort) (§2) | Justifies choosing merge sort ✓ |
| 18 passes (§3) | Reduced to 5, then 2 ✓ |
| "quarter million items / memory for a twelfth" simulation (§2–3) | Internally consistent (≈12 runs, 18≈2^18) but **never reconciled with the real 1GB/160MB demo** |
| 86 MB run size footnote (§3, screen-only) | Meant to explain why 160 MB memory yields runs smaller than itself — but unspoken |
| Default batch-size 16 (§5) | "plenty for twelve" — resolved same sentence ✓ |
| Aggarwal-Vitter optimality (§5) | **No payoff** — asserted and dropped |

**Finding (BLOCKING).** The opening's real numbers (1 GB file, 160 MB memory) imply a ratio of ~6.4, not twelve. The video's central numeric payoff — "our file is twelve memories long, so that makes twelve runs" — only reconciles with the demo's actual numbers via an unspoken screen footnote ("each run is about 86 MB, because sort also keeps a pointer to every line"). A viewer doing the obvious mental math (1024/160 ≈ 6) will find the "twelve" claim doesn't check out, right at the moment it's supposed to be the satisfying payoff of the opening question.
> Rewrite: narrate the reconciliation instead of hiding it in a caption. Insert into §3: *"Sort spends part of that 160 megabytes on bookkeeping — a pointer to every line — so each run only holds about 86 megabytes. That's why our 1-gigabyte file makes twelve runs, not six."* Alternatively, simplify by choosing demo numbers that divide evenly (e.g., a memory cap where run size and total match without an overhead footnote) if the pointer-overhead detail isn't worth the airtime.

## 5. One vocabulary

Terms defined at first use, correctly: *I/O*, *block*, *pass*, *run*, *external merge sort*. Good discipline overall.

**Finding (SHOULD FIX).** Same concept, two names between screen and narration.
> Quote: narration "**eighteen passes**" (§3) vs. screen note "merge sort's **eighteen sweeps** from the race, numbered" (§3 screen direction).
> Rewrite: change the screen label to "eighteen passes."

**Finding (NIT).** "buffer pages" is introduced as an alternate name for "block" in a footnote (§5) — the script already flags this deliberately as an aside for textbook-readers, so it's handled gracefully, but worth a second look at whether it's needed at all given the number/time crunch in §5.

## 6. Number budget

Numbers introduced: 1 GB, 160 MB, twelve, "hundreds of times slower," 250,000, a twelfth, N log N, 3 I/Os/item, 1/20, 2^18, eighteen, 20,000, fourteen, five, 86 MB, four, two, 16 GB, 16,000 blocks, hundreds of terabytes, sixteen (default), 1988, two-or-three. That's over twenty distinct numbers in a 5-minute video.

**Finding (SHOULD FIX).** Far too many numbers to retain; the ones that matter (**twelve**, **two passes**, and arguably **sixteen** — sort's default fan-in, which is *why* twelve runs merge in one shot) get buried under §5's cluster of six new numbers in ~53 seconds (16 GB, 16,000 blocks, "hundreds of terabytes," 1988, "two or three").
> Rewrite: in §5, keep only the default-16 fact (it directly explains the "two passes" payoff) and cut "sixteen thousand one-megabyte blocks... hundreds of terabytes" and the 1988 citation — none of these resurface in the closing recap.

## 7. Concrete before abstract

Mostly well-ordered (concrete simulation before naming "I/O"; concrete idle-memory observation before naming "multiway merge").

**Finding (SHOULD FIX, ties to #3).** The passes formula card arrives right after a vague verbal generalization ("divides by thousands... grows like a logarithm") rather than after a worked concrete second example. Same fix as in test 3: cut the card, keep it verbal, or add one concrete worked round.

## 8. Wrong model

Stated wrong model: *"comparison counts decide speed, and virtual memory takes care of the disk."* The first half is well confronted — the heapsort/merge-sort race shows identical N log N comparisons producing wildly different runtimes, which directly disproves "comparisons decide speed."

**Finding (SHOULD FIX).** The second half — "virtual memory takes care of the disk" — is argued (disk fetches are slow, whole blocks) but never actually *shown failing*. Nothing in the script runs a program under virtual memory and shows it crawl or thrash; the opening Python failure is an in-memory OOM crash, not a virtual-memory demo. Test 8 asks for the wrong model to be shown failing, not just reasoned against.
> Rewrite: add one beat to §2 — e.g., a caption/line: *"Turn on swap for Python's sort and it won't crash — it'll just take [dramatically longer], fetching one slow block at a time."* Even a single supered number (real or illustrative) makes the failure concrete instead of inferred.

## 9. Depth over breadth

**Finding (SHOULD FIX).** "Aggarwal and Vitter... proved that no sort that treats items as indivisible can do asymptotically better" is a named-but-unexplained credential drop — the viewer is told a proof exists but sees no hint of why, and it isn't in the stated objectives.
> Rewrite: cut it, or replace with a plain-language claim that carries the rhetorical weight without the unexplained citation: *"This isn't just a good trick — for data this size, you provably can't do fewer I/Os."*

The PostgreSQL example is a single concrete instance, not a breadth-list — fine as is.

## 10. Words and pictures

**Finding (SHOULD FIX, cross-ref §5).** Screen "sweeps" vs. narrated "passes" — a genuine mismatch a viewer will notice and wonder about.

**Finding (SHOULD FIX, cross-ref §3/§7).** The silent, unnarrated formula card puts dense symbolic math on screen with no spoken guide, in the middle of a fast 150-wpm video — attention is aural, and this beat asks for close reading instead.

**Finding (NIT).** The pass-tally captions ("18 → 5 written as '1 + 4'", "5 → 2 written as '1 + 1'") repeat the narration's numbers verbatim as on-screen text. Given these are exactly the numbers you want retained (test 6), this redundancy is probably fine — but note it's technically the pattern this test flags.

## 11. Deletion test

Lines that could be cut without weakening the takeaway or breaking anything downstream:
- *"Aggarwal and Vitter, who defined this I/O model, proved that no sort that treats items as indivisible can do asymptotically better."* (§5) — supports nothing in the four stated objectives.
- *"With even more runs, you merge in rounds, and each round divides the number of runs by thousands. So the number of passes grows like a logarithm with an enormous base."* (§5) — generalization beyond the objectives; the silent formula card that follows depends on it, so cutting both together is clean.
- The extrapolation clause *"...and two passes can sort hundreds of terabytes"* (§5) — a nice flex but does no work toward the takeaway rule and adds to the §6 number-budget problem.

## 12. For the ear

Overall length is right on budget: narration totals ≈750 words against the stated ~750-word/5-minute target — good pacing at the aggregate level.

**Finding (SHOULD FIX).** Stacked prepositional clauses are hard to track by ear.
> Quote: *"Here's what each one costs in I/Os, simulated on a quarter of a million items, with memory for a twelfth of them, under virtual memory."* (37 words, four stacked modifiers)
> Rewrite: *"Here's what each one costs in I/Os. We simulated both on a quarter million items, with memory for a twelfth of them, running under virtual memory."*

**Finding (SHOULD FIX, cross-ref §9).** *"Aggarwal and Vitter, who defined this I/O model, proved that no sort that treats items as indivisible can do asymptotically better."* — unfamiliar proper nouns immediately followed by a dense abstract clause ("treats items as indivisible") is difficult to parse purely by listening. Cutting this line (per §11) solves both problems at once.

---

**VERDICT: REVISE**

(One BLOCKING item: the 1 GB/160 MB opening numbers don't arithmetically reconcile with the "twelve runs" payoff without an unspoken screen footnote — the central numeric reveal needs to be narrated, not hidden in caption text.)
