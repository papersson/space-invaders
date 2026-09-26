# Script Review

## 1. One question

**Opening:** "What are those files, and how does sort get away with it?"
**Ending:** "That's how sort handled a file twelve times bigger than its memory: twelve runs, one merge, two passes."

This passes — the ending explicitly answers both halves (files = runs, mechanism = one merge). But the full answer is actually delivered twice: section 3 already says "that's what sort's twelve files were," and section 4 already says "It's exactly what sort did at the end." By the time section 6 recaps, the mystery has been resolved for two full sections. The ending is a recap of an already-answered question, not the payoff moment itself.

- **SHOULD FIX** — Quote: *"And that's what sort's twelve files were. It filled its memory twelve times, and wrote out twelve runs."* (end of §3)
  This spends the answer to half the hook with two sections still to go, so §6's "twelve runs" lands as confirmation, not revelation.
  **Rewrite:** Hold back the explicit naming here — "Our file is twelve memories long, so this makes twelve runs, in a single pass" — and let §6 be the first place the words "twelve files" and "twelve runs" are put side by side.

- **SHOULD FIX** — the opening dramatizes *Python failing*, but nothing in the script ever explains why Python fails, even though it's the contrasting case that makes sort's behavior remarkable.
  **Quote:** *"Ask Python to sort it, and it runs out of memory."*
  **Rewrite (add to §6):** "Python's sort tried to hold the whole file in memory at once. GNU sort never did — that's the twelve runs." One sentence closes a thread the cold open opened.

## 2. But/therefore chain

One sentence per section, joined:

1. Sort finishes a 12x-oversized file while Python OOMs, and twelve mystery files flash by — **but** what are they?
2. The obvious fix is virtual memory, **but** disks move whole blocks at huge latency, so I/Os — not comparisons — dominate; **therefore** we simulate heapsort vs. merge sort, and heapsort's scattered access needs ~20x more I/Os, **so** merge sort is the candidate, measured in passes.
3. Merge sort takes 18 passes, **but** the first 14 produce pieces smaller than memory, and merging doesn't care how a piece got sorted, **so** sort those in memory directly as "runs," collapsing 18→5 — **and that's** the twelve files.
4. The remaining passes just merge runs, **but** a two-way merge leaves memory mostly idle, **so** give every run its own block and merge all of them at once (a heap picks the next-smallest), collapsing 5→2 — external merge sort, **and that's** what sort did.
5. **But** how many runs fit in one merge — sort caps at 16, and in general it's blocks-in-memory-minus-one, which is thousands, **so** even huge files need only one extra pass, **therefore** databases (Postgres) sort this way too.
6. **Therefore**: count I/Os, sort in order, merge as many runs as memory allows — that's the twelve-runs-one-merge-two-pass trick.

No hard "and then" breaks in the section-to-section spine — every join is a genuine complication or consequence. One internal soft spot:

- **NIT** — §4: *"Sort memory-sized runs, then merge them from disk: that's external merge sort. Merging as many runs at once as memory allows keeps the passes to a minimum."* Two restatement sentences back to back, joined by "and" rather than a real step.
  **Rewrite:** "Sort memory-sized runs, then merge as many of them at once as memory allows — that's external merge sort, and it's what keeps the passes to a minimum."

## 3. Derive, don't reveal

Well-executed overall (runs and the multiway merge are textbook derivations — a visible waste or limit is shown right before the fix). Two gaps:

- **SHOULD FIX** — Quote: *"So let's count their I/Os instead. […] So merge sort is our starting point. Let's measure it in passes."*
  "Passes" is declared as a unit rather than derived from a problem with counting I/Os directly (e.g., that a raw I/O count doesn't tell you how many times you touched the disk end-to-end, or doesn't compare across file sizes).
  **Rewrite:** "Raw I/O counts won't tell us how to fix things — what we need is how many times we touch the whole file. Call that a pass."

- **SHOULD FIX** — Quote: *"At each step, a heap with one entry per run picks the smallest item at the front of any run."*
  The heap is handed to the viewer before the problem it solves (scanning thousands of fronts for a minimum is slow) is ever shown — that problem only surfaces in §5. As written, a viewer could reasonably ask "why not just scan the fronts?"
  **Rewrite:** Plant the scale earlier — "since a run could be one of thousands, we don't want to scan every front for the smallest each step, so give each run a heap entry" — or move a one-line preview of scale into §4.

## 4. Setups and payoffs

| Setup | Payoff |
|---|---|
| Twelve files in /tmp, question mark freeze (§1) | "That's what sort's twelve files were" (§3), replayed capture (§6) |
| Virtual memory as "obvious fix" (§2) | Shown failing same section (block I/O, counter) |
| Heapsort vs. merge sort race (§2) | 3 I/Os/item vs. <1/20th (§2); not reused later — fine, contrast served its purpose |
| 18 passes / doubling (§3) | 18→5 (§3), 5→2 (§4), final tally (§6) |
| Two-way merge's idle memory (§4) | Multiway merge (§4) |
| Sort's cap of 16 (§5) | "plenty for twelve" — closes immediately |
| File is "12 memories long" (§3, §1) | 12 runs, reinforced by the 11.6→12 caption |
| Python OOM (§1) | **No payoff** — never explained or referenced again |
| PostgreSQL EXPLAIN ANALYZE (§5) | Illustrative only, no return — acceptable as a single closing example, not a dangling thread |

Only real gap: **Python's failure has no payoff** (see finding under Test 1).

## 5. Vocabulary

| Term | First use | Notes |
|---|---|---|
| I/O | §2, defined immediately before use | Clean |
| block | §2, defined inline | Clean |
| pass | §2, defined at first use, before §3 relies on it | Clean (motivation is the weak point, see Test 3) |
| run | §3, defined at coining ("called a run") | Clean |
| multiway merge | §4, named after the mechanism is shown | Good — concrete before term |
| external merge sort | §4, named after both halves (runs + multiway merge) are built | Good |

No term is used before being explained, and nothing is called by two different names in the narration. The end-card's aside that "database textbooks write B for buffer pages" is correctly confined to the reference card rather than spoken, so it doesn't create a synonym problem in the narration itself.

## 6. Number budget

Every number: 12 (ratio/files/runs, ~10 occurrences), 86 MB, 1 GB, "hundreds of times" (I/O latency), N log N, ~250,000 items, a twelfth, 3 I/Os/item, <1/20th, 18 doublings/passes, 2¹⁸≈262,144, 261,120 / 21,760 / 256 (caption), 14 passes, 12→6→3→2→1 / four passes, 5→2, 16 (sort's cap), "one block per run, less one," thousands of blocks, 16GB÷1MB≈16,000, "thousands" (scaling), two or three passes (real files), 107696kB (Postgres).

**The 2–3 to keep:** **12** (why the files/runs are twelve), **2** (final pass count — the actual "how"), and **thousands** (the scaling factor that makes this practical beyond the toy example). These three carry the objectives.

- **NIT** — Quote: *"Sort Method: external merge Disk: 107696kB"*
  This exact figure does no work — it's never referenced or compared to anything. It's there purely for authenticity, which is a fine reason to keep it, but flagging since a rounder or redacted number ("~100 MB") would do the same job with less noise.

- **NIT** — the caption stack in §2 (261,120 / 21,760 / 256) is more precision than the narration ever uses ("a quarter of a million," "a twelfth"); harmless since it's screen-only, but it's decoration a viewer can't act on.

## 7. Concrete before abstract

No violations found. The abstraction that would most tempt a script into this trap — the passes formula — is deliberately parked on the silent end-card, after the concrete derivation, labeled "for reference." Every named mechanism (I/O, run, multiway merge, external merge sort) is introduced only after its concrete instance is on screen.

## 8. Wrong model

**Wrong model:** "comparison counts decide speed, and virtual memory takes care of the disk."
**Shown failing:** Yes, on both halves — the VM half is shown failing via the block-fetch animation and I/O counter; the comparison-count half is shown failing via the simulated race, where heapsort and merge sort have comparably-ordered comparison counts but wildly different I/O counts and wall-clock behavior. This is a genuine empirical disproof, not just an assertion. No finding here.

## 9. Depth over breadth

No padded lists of applications. The one external example (PostgreSQL) is grounded in a real EXPLAIN ANALYZE line rather than name-dropped alongside a string of other systems. Passes.

- **NIT** — Quote: screen-only *"GNU sort: at most 16 per merge (--batch-size)"*
  The flag name appears on screen but is never explained even briefly in narration — a curious viewer is left to wonder what it is. Low stakes since it's a caption, not spoken.

## 10. Words and pictures

- **SHOULD FIX** — Quote: *"Heapsort compares items that sit far apart in its array."*
  Screen direction only shows the resulting race/counter, not the actual far-apart comparison that causes it. The picture supports the *consequence* (I/O count climbing) but not the *claim* (why heapsort's access pattern is scattered).
  **Rewrite (screen):** briefly highlight two array positions (i and 2i) lighting up on the file bar during a heap comparison, before cutting to the race.

- **NIT** — the recurring "Pass tally 18 → 5" / "5 → 2" on-screen text closely mirrors the just-spoken numbers with no added information. Defensible as a running visual motif for continuity, but it is the clearest example in this script of screen and narration saying the same thing.

## 11. Deletion test

The script is already tight (visible from the round-1 cuts). Nothing narratively necessary is missing its function, and I don't find a line that could be deleted without leaving a hole. The closest candidate is the restatement flagged in Test 2 (§4's two summary sentences), which is combinable but not deletable outright — the "cut the passes" rule needs to be stated somewhere before §6 recaps it.

## 12. For the ear and pacing

- **SHOULD FIX** — Quote: *"Two at a time, twelve runs become six, then three, then two, then one: those are the four passes."*
  Four numbers in one breath, then a count-back ("those are the four") — by ear alone this is easy to lose even though the screen's four rows carry it. **Rewrite:** "Two at a time: twelve runs, six, three, two, one. Four passes." (shorter clauses, a natural beat between the count and the label).

- **SHOULD FIX** — the multiway merge's actual operation — *"At each step, a heap with one entry per run picks the smallest item at the front of any run. When the output block fills, write it out. When a run's block runs dry, fetch its next one."* — is the mechanical heart of the "how," but it's three separate mechanisms compressed into three short sentences with no single concrete trace to hang onto. This is the moment objective (2) lives or dies on; it's the most rushed beat in the script relative to its importance.
  **Rewrite:** ground it in the toy example already on screen — "Say run 3's front card is smallest — take it, and if run 3's tray runs dry, fetch its next block from disk. That's the whole loop, and it never has to look further than what's already at the front."

- **NIT** — "twelve" appears roughly ten times across the script. This is a deliberate, previously-litigated choice (round 1) that reinforces the Test-1 callback, but by the final section it risks feeling comic/heavy rather than emphatic. Worth a final read-aloud pass to see if 1–2 instances (e.g., the caption math "11.6, so 12 runs" plus the narrated "twelve memories long") can be trimmed without losing the thread.

---

VERDICT: PASS
