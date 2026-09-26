# Script Review

## Test-by-test

**1. Opening question → closing answer.** Clean callback. Opens with "who decides? And why is the same query sometimes fast, and sometimes slow?" and section 7 closes with "So who decides how a query runs? The query planner... That's why the same query can be fast or slow." Direct echo, not just thematic. **Pass.**

**2. One-sentence chain, connectors.** Reconstructed: mystery (15μs vs 135ms) → *therefore* SQL is declarative, DB must choose → *therefore* two ways to find rows, index only helps if matches cluster → *therefore* planner estimates cost from stats and picks cheapest → *therefore* joins follow the same logic (nested loop vs hash join) → *but* the estimate can be wrong when stats are stale → *therefore* the answer. **Zero "and then"s** — every internal "then"/"collect... then read" is describing an algorithm step, not stitching narrative beats together. This is unusually disciplined; no finding here.

**3. Announced vs. derived ideas.** Declarative-vs-imperative, scan-vs-index, and stale-statistics are all derived from the immediately preceding concrete tension. The joins section (5) is the one idea that's more *announced* than derived — see Finding F below.

**4. Setups/payoffs.** Mostly matched. One payoff lacks a setup: the "nobody added an index" line in section 6 pays off the *doc's* "wrong model" (add an index) but that belief is never voiced in the script itself. See Finding A.

**5. Terms before explanation / dual naming.** Clean. "Page," "bitmap scan," "nested loop," "hash join" are all defined at first use, concrete case first. "Full scan" (narration) / "Seq Scan" (screen) is a deliberate, labeled translation, not confusing dual-naming.

**6. Numbers.** Roughly 20 distinct figures appear. The three worth remembering: **15μs vs 135ms** (the whole hook), **10 pages vs 12,739 pages** (why the index does or doesn't help), and **137ms → 0.061ms after ANALYZE** (the actionable takeaway). Numbers doing no real work: see Findings C and D.

**7. Abstraction before concrete case.** No violation — the video leads with a concrete puzzle (section 1) before any concept is named, and each subsequent abstraction (declarative, scan/index, planner, joins) is instantiated immediately with real numbers.

**8. Wrong intuition, shown failing.** Three components of the stated wrong model: "runs it the same way every time" — falsified by the opening pair of numbers itself. "Index always helps" — falsified concretely in section 3/4 (customer 1: forcing a full scan is "no faster," the index bought nothing). "If it's slow, add an index" — technically shown failing (section 6 reveals the index was already there) but weakly staged; see Finding A.

**9. Examples named but not understood.** "Bitmap scan," "nested loop," "hash join" are all named *and* explained. One gap: **"autovacuum off"** appears as a screen caption in section 6 with no explanation of why it matters (i.e., that autovacuum would normally have re-run ANALYZE on its own) — see Finding B.

**10. On-screen text vs. narration / pictures vs. line.** No redundant captions found — screen elements (plan trees, page grids, counters) supplement rather than restate the voiceover. The section 7 recap lines ("rare → index → 10 pages" etc.) restate the takeaway, but that's a conventional, load-bearing end-card, not filler.

**11. Deletable lines.** The script is lean; the only trimmable material is over-precise numbers (Findings C, D) — no narrative lines are pure filler.

**12. Hard-to-follow sentences / pacing.** Density and pacing are even across sections (~150–180 words per beat, two worked examples each in 3–5). One recurring friction: spelling out "customer four thousand two hundred and forty-two" in full, four separate times, is heavier to say aloud than it needs to be after the first mention — see Finding E. No section reads as rushed or padded.

## Findings

**A. SHOULD FIX** — payoff without a spoken setup.
Quote: *"Nobody added an index. The one on customer number was there all along. The planner just didn't expect it to help."*
This confronts the "just add an index" instinct, but that instinct is never voiced anywhere in the script (only in the author's private "wrong model" notes) — a viewer who doesn't already hold that belief won't feel the reveal.
Rewrite: *"The obvious fix would be to add an index on customer number. But there already is one — nobody added anything; the planner just didn't expect it to help."*

**B. SHOULD FIX** — named but unexplained term.
Screen text: *"orders_s: a copy of orders, statistics gathered before the archiving (autovacuum off)"*
"Autovacuum off" is dropped in without saying why it's relevant; an attentive viewer may wonder why Postgres didn't just refresh the stats itself, which undercuts the mystery instead of deepening it.
Rewrite (caption only, no narration change needed): *"orders_s: a copy of orders — autovacuum off, so nothing re-ran ANALYZE after the archiving."*

**C. NIT** — numbers doing no work.
Quotes: *"A hundred customers live in Tromsø, out of a hundred thousand."* / *"ninety-nine thousand nine hundred of them."*
The beat only needs "few" vs. "almost all"; the precise denominators add cognitive load without being used again.
Rewrite: *"A hundred customers live in Tromsø."* / *"Now ask for customers in Oslo: almost all hundred thousand of them."*

**D. NIT** — unused on-screen figure.
Screen text: *"1,346 rows · 5.1 ms"* (Tromsø plan card).
The row count is never narrated or compared to anything; only the timing does work.
Rewrite: drop to just *"5.1 ms."*

**E. NIT** — spoken friction from repetition.
Quote (recurs across sections 1, 3, 4, 7): *"customer four thousand two hundred and forty-two."*
Fine on first use; saying it in full four times is heavier than needed.
Rewrite after first mention: *"that same rare customer"* or *"customer 4242"* spoken as digits.

**F. NIT** — mildly announced pivot.
Quote: *"Everything so far read one table. Now ask for the orders of every customer in Tromsø."*
Honest about being a new case, but arrives as a topic change rather than a consequence of section 4's logic.
Rewrite: *"The same estimate-and-choose logic has to work across two tables too. Ask for the orders of every customer in Tromsø."*

No BLOCKING issues: the opening/closing callback is explicit, the argument chain has no "and then" padding, terms are defined before use, and all three wrong-model beliefs are demonstrated failing with real numbers, not just asserted.

**VERDICT: PASS**
