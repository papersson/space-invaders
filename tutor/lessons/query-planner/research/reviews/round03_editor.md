# Script Review

## Test 1 — Opening question / ending callback
**Pass, strong.** Opening asks "who decides?" and "why fast/sometimes slow?" over the 0.015 ms / 135.4 ms pair. Section 7 answers "who decides" in its first line, restates the same two numbers plus their page counts, and closes the wrong-model loop explicitly ("don't just add an index"). No issue.

## Test 2 — Segment chain / "and then" count
Chain holds as a causal spine (question → because → therefore → therefore → therefore → but → therefore) with **zero "and then" joins** at the macro level — every transition is causal or contrastive, not merely sequential. This is a structural strength worth preserving; don't let future edits soften a "therefore" into an "and then."

## Test 3 — Announced vs. derived ideas
- NIT: "There are two basic ways to find one customer's orders" (§3) and "SQL is declarative" (§2) are asserted as topic sentences rather than surfaced from a felt gap, though both are immediately demonstrated. Not a real problem — flagging only because the rest of the script (bitmap scan, nested loop, hash join, ANALYZE) earns its terms by showing mechanism first; these two are the exceptions.

## Test 4 — Setups/payoffs
**SHOULD FIX** — quote: *"turns that into a cost, a number for comparing plans rather than a time"* (§4). This draws a cost-vs-time distinction but the script never shows an actual cost number — every figure that follows (15 µs, 72 ms, 135 ms…) is a time. The setup is never paid off, and worse, it primes the viewer to expect a "cost" figure that never arrives.
Rewrite: delete the clause — *"estimates the rows and pages it would touch, and picks the cheapest plan"* — or pay it off by putting a real `cost=0.29..8.31` style figure on screen.

All other setups (rare/common customer, Tromsø/Oslo, stale stats) are cleanly paid off, including the wrong-model's three components (see Test 8).

## Test 5 — Terms before explanation / duplicate names
**SHOULD FIX** — narration consistently says "page" and "full scan," but on-screen labels show Postgres's own vocabulary ("Heap Blocks," "Seq Scan"). The script bridges this once for "bitmap scan" ("PostgreSQL calls that a bitmap scan") but never does the equivalent for page/block or scan/Seq Scan, so those on-screen labels are left unglossed technical synonyms.
Rewrite: either add one bridge line where "page" is first used — *"(PostgreSQL's plans call this a Seq Scan, and call a page a block — you'll see both on screen)"* — or relabel the captions to match narration ("pages" instead of "Heap Blocks").

## Test 6 — Numbers
Full count: ~25+ distinct figures across 7 sections. **The two or three worth remembering**: (1) 0.015 ms vs 135.4 ms — the hook, correctly recalled at the end; (2) 137 ms → 0.061 ms via ANALYZE — the actionable takeaway; (3) 10 pages vs 12,739 pages — the conceptual core.
**SHOULD FIX** — numbers that do no work: *"ninety-nine thousand nine hundred"* (§5) adds false precision where "almost all hundred thousand" would do — the exact digit isn't used for any later comparison.
Rewrite: *"Now ask for customers in Oslo: almost all hundred thousand of them."*

## Test 7 — Abstraction before the concrete case
No violations found — the script is disciplined about showing mechanism before naming it (bitmap scan, nested loop, hash join all named after being shown). The one abstraction that arrives and is never grounded is "cost" (see Test 4), which is the same finding, not a new one.

## Test 8 — Wrong intuition, shown failing
All three components of the stated wrong model are explicitly confronted:
1. "runs it the same way every time" — refuted by the forced-plan experiments.
2. "index always makes it faster" — refuted in §4: "Force a full scan instead, and it's no faster."
3. "if it's slow, add an index" — refuted explicitly in §6: "nobody added one here... the one on customer number was there all along."
**NIT**: #2 is disproved but never voiced as a belief first, unlike #3 which gets an explicit "the usual fix is..." setup.
Rewrite: before *"Force a full scan instead, and it's no faster"* add — *"You'd expect the index to win here too. It doesn't."*

## Test 9 — Named but not understood
**NIT** — quote: *"Here's a copy of the orders table"* / on-screen *"orders_s"*. The `_s` suffix appears repeatedly in screen text (`orders_s_pkey`, `orders_s_customer_id_idx`) but is never glossed in narration or caption.
Rewrite: caption footnote — *"orders_s — a copy of orders, kept stale on purpose."*

## Test 10 — On-screen text vs. narration; unsupported pictures
No mismatched pictures found — visuals track narration closely throughout (a genuine strength). **NIT**: the §7 recap card ("rare → index → 10 pages," "common → every page, whatever the plan," "stale statistics → wrong plan → ANALYZE") paraphrases the narration almost verbatim in the same breath. Likely intentional reinforcement for a closing summary, but if trimming, cut to nouns only and let the voiceover carry the full clauses.

## Test 11 — Deletable lines
- The cost/time clause in §4 (see Test 4) is the cleanest candidate — removing it loses nothing else in the argument.
- Weaker candidate: the absolute count "Customer one has about six hundred thousand orders" (§3) — the density (3 in 10 per page) is what does the work; the raw count is scale-setting flavor, not load-bearing. Not urgent enough to cut on its own.

## Test 12 — Hard-to-follow sentences / rushed or padded beats
**SHOULD FIX** — §6 stacks four large numbers across four short sentences (420,000 → ten → 1.4 million → 137 ms) in one breath, the densest stretch in the script.
Rewrite: move the "420,000 estimated" figure to the caption only and drop it from narration: *"The planner still believes customer one is everywhere. So it walks through the orders by order number, expecting to run into ten of theirs almost at once. Instead it passes about one point four million other rows first. A hundred and thirty-seven milliseconds."*
**NIT** — §5 (joins) covers two full strategies plus a forced comparison in its most terse paragraph, brisker than §4's equivalent treatment of scans, though the closing line ("Same query shape. A different plan, because a different number of rows match.") does supply the generalization, so this is pacing, not a structural gap.

---

No finding rises to BLOCKING: the causal chain is intact, the callback lands, the wrong model is confronted three times, and setups/payoffs mostly match. The fixable items are the orphaned "cost" concept, the unglossed page/block and full-scan/Seq-Scan label pairs, and the numeric density in §6.

VERDICT: PASS
