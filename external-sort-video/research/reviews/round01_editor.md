# Script Review — External Merge Sort Explainer

Overall this is a well-built script — the derivation logic and the concrete-before-abstract ordering are genuinely strong. Most findings below are **SHOULD FIX** polish items clustered in Section 5; there are no **BLOCKING** breaks.

---

## 1. One question

**Pass, with a nit.** The opening asks a compound-but-unified question ("what are those files, and how does it work") and the ending calls back explicitly: *"That's how sort handled a file far bigger than its memory: twelve runs, one merge, two passes."* Good tight loop.

- **NIT** — The mystery is actually resolved in two installments (files→runs in §3, mechanism in §4), so by the literal ending there's no suspense left, only recap. That's a legitimate structure (specific answer mid-film, principle + recap at the end), not a flaw — just note it's a recap-callback, not a reveal-callback.

## 2. But/therefore chain

Sections 2–4 chain cleanly ("but... so... and..."). Section 5 breaks the pattern:

> *"A laptop... can combine sixteen thousand runs. Two passes can sort... hundreds of terabytes. Real systems... usually finish in two or three. In symbols... Aggarwal and Vitter proved in 1988... Databases do the same thing... PostgreSQL reports it..."*

- **SHOULD FIX** — This is four separate "and also" facts (scale example → caveat → formula → citation → database example) with no causal connectors between them. It reads as a list, not an argument.
- **Rewrite:** "A laptop with sixteen gigabytes of memory, in one-megabyte blocks, can merge about sixteen thousand runs at once — so two passes are enough for hundreds of terabytes. That's not just a laptop trick: PostgreSQL, doing exactly this, calls it 'external merge' in its query plans." (Cut the 1988 citation and the formula sentence out of narration entirely — see §11.)

## 3. Derive, don't reveal

Strong overall — I/O, run, and "external merge sort" are all named *after* the mechanism is shown, not before.

- **NIT** — *"Aggarwal and Vitter proved in 1988 that... no algorithm can do asymptotically better"* is asserted, not derived — there's no intuition for *why* two passes is near-optimal, it's just cited. Low priority given it's a one-line credibility beat, but if kept, one clause of intuition ("you can't do better because you still have to touch every block twice") would convert it from revealed to derived.

## 4. Setups and payoffs

The **twelve** motif is the spine of the piece and mostly pays off well (§1 mystery → §3 "that's what the twelve files were" → §4 capture → §6 recap). But:

> *"Here's heapsort on a file **twelve times bigger** than memory..."* (§2) — spoken well before *"Sort filled its memory **twelve times**, and wrote out **twelve runs**"* (§3).

- **SHOULD FIX** — Reusing "twelve" for an unrelated quantity (the heapsort demo's size ratio) right before the number becomes the answer to the video's central question dilutes the payoff — an attentive viewer may (wrongly) assume the two twelves are the same fact, or feel the reveal is coincidental rather than earned.
- **Rewrite:** Change the heapsort demo to any other ratio — *"Here's heapsort on a file eight times bigger than memory..."* — so "twelve" is spent exactly once, on the real answer.

Other setups all pay off cleanly: the /tmp folder, the pass tally (18→5→2), the idle-memory shot in the two-way merge, the block/I-O vocabulary. No orphaned setups found.

## 5. One vocabulary

Terms are consistently defined at first use, in order (I/O → block → pass → run → multiway merge → external merge sort). One gap:

> *"...with the operating system doing the **paging**."*

- **SHOULD FIX** — "Paging" is dropped once, undefined, for an audience explicitly said to know "not much about disks." It does no narrative work here (virtual memory was already explained a sentence earlier) and can simply be cut: *"Here's heapsort on a file twelve times bigger than memory, under virtual memory."*

## 6. Number budget

Roughly 18 distinct numbers appear in ~700 words. The three that should survive as memorable: **1,000× (disk vs. memory latency, motivates the whole rule)**, **the 18→5→2 pass arc (the mechanism)**, and **twelve (files/runs, the answer)**. Two numbers do no lasting work and compete for attention:

- **SHOULD FIX** — *"Aggarwal and Vitter proved in 1988..."* — the date is pure trivia; cut it or fold the fact in without the year.
- **SHOULD FIX** — *"Real systems... usually finish in two or three [passes]."* — this caveat directly undercuts the crisp "two passes" the whole video builds toward and repeats in the closing line. Either cut it, or move the caveat before the "two passes" payoff line so the ending stays clean.

## 7. Concrete before abstract

**Clean pass, no violations.** The formula in §5 arrives only after three concrete numbers (16 GB, 1 MB blocks, 16,000 runs); "run" and "external merge sort" are named only after being shown. This is the script's strongest craft element — no changes needed.

## 8. Wrong model

The wrong model ("comparisons decide speed, VM handles the disk") is confronted and shown failing via the heapsort/merge-sort race (3.2 I/Os per item vs. >20× fewer). Good.

- **SHOULD FIX** — The kill shot is implicit: the script never says heapsort and merge sort do the *same* number of comparisons, which is the actual fact that falsifies the wrong model. Without it, a viewer could believe merge sort just "does less work," missing the point.
- **Rewrite:** insert before the race: *"Heapsort and merge sort do the same amount of comparing — order n log n, either way. The difference is entirely in how they touch the disk."*

## 9. Depth over breadth

No real violation — the video stays on one worked example throughout. The PostgreSQL line and the Aggarwal–Vitter citation are single-sentence real-world/authority nods, not an unexplored list, so this test doesn't flag them on its own — but see §11, since they're the same material flagged there for pacing.

## 10. Words and pictures

- **NIT** — Pass-tally captions ("18 → 5 → 2") appear on screen at the same moment narration speaks the same numbers, in three separate sections. Mildly redundant but standard/helpful for retention — low priority.
- **NIT** — The PostgreSQL screen literally shows the words "external merge" while narration says "reports it as an external merge" — exact text duplication. Fine to leave, since it's a real captured artifact (authenticity value), but flagging per the test's letter.

## 11. Deletion test

The back half of Section 5 is the main casualty:

> *"In symbols... Aggarwal and Vitter proved in 1988... Databases do the same thing... PostgreSQL reports it..."*

- **SHOULD FIX** — None of this is required for the stated takeaway rule (§6 states the rule in plain English without referencing the formula or the citation). Recommend cutting the formula from narration (keep it as a screen-only card, silently reinforcing "concrete before abstract" from §7) and compressing the citation + Postgres line into the one sentence given in the §2 rewrite above. This also directly fixes the "and then" list problem from Test 2 and trims two "no-work" numbers from Test 6.

## 12. For the ear

Total narration: **709 words** ≈ 4:44 at 150 wpm — within the 5-minute budget, no cut needed on length.

- **SHOULD FIX** — *"In symbols: with N items, memory for M, and blocks of B, the number of passes grows as a logarithm of N over M, in base M over B."* This is very hard to parse by ear alone (nested "of... in base..." prepositions, three single-letter variables spoken aloud). Per §11, better handled as a silent screen card than as narration.
- **NIT** — *"A laptop with **sixteen** gigabytes of memory and one-megabyte blocks holds about **sixteen** thousand blocks, so one merge can combine **sixteen** thousand runs."* Three uses of "sixteen" for two different units and a run count risks the ear conflating them.
- **Rewrite:** *"A laptop with sixteen gigabytes of memory, in one-megabyte blocks, can hold about sixteen thousand of them — enough to merge that many runs in a single pass."*

---

### Summary of action items (priority order)
1. Change the heapsort demo's ratio away from "twelve" (§4/§6 finding) — protects the central payoff.
2. Trim Section 5's back half: cut the 1988 date, move the formula to a screen-only beat, cut or relocate the "two or three passes in practice" caveat, and tighten the database/citation material into one sentence (§2/§6/§9/§11/§12).
3. Add one explicit sentence stating heapsort and merge sort share comparison complexity, to complete the wrong-model kill shot (§8).
4. Cut the undefined "paging" reference (§5).

VERDICT: PASS
