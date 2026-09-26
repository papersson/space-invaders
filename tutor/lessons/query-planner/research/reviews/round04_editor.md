# Script Review

## Test 1 — opening question / closing answer
**Pass.** Ch.1 asks "who decides? And why is the same query sometimes fast, and sometimes slow?" Ch.7 opens with "So who decides how a query runs? The query planner..." and closes by literally reusing the same fast/slow framing, plus the screen recalls the exact two numbers (0.015 ms / 135.4 ms) from the opening. Tight callback, no note needed.

## Test 2 — one-sentence chain, count the "and then"s
Rebuilding the chain from the script itself (not just the author's own Chain section):
1. Same query, 15µs vs 135ms — who decides?
2. **Because** SQL is declarative (says what, not how), the database must choose.
3. **Therefore** two ways to find rows exist (scan vs index), and the index only pays off if matches are rare.
4. **Therefore** the planner estimates cost from statistics and picks the cheapest — which is why 4242 is fast and customer 1 isn't.
5. **Therefore** the same logic governs joins (few matches → nested loop, many → hash join).
6. **But** the estimate can be wrong, because statistics are a snapshot — stale stats → bad plan → ANALYZE fixes it.
7. **Therefore**, the planner decides, driven by data and its belief about the data.

**Zero "and then"s required.** Every beat is causally forced by the one before it — no filler transitions. This is a genuine strength; flag it as such rather than a defect.

## Test 3 — announced vs. derived ideas
No clear violations. Each abstraction ("SQL is declarative," "the planner keeps statistics," "the plan is only as good as the estimate") is stated and then immediately cashed out with the concrete numbers in the same breath, consistently across chapters. Ch.5's transition into joins ("Everything so far read one table. Now ask...") is a flagged scope-change rather than an unmotivated announcement. Nothing to fix here.

## Test 4 — setups without payoffs
**SHOULD FIX.** The ch.1 screen caption carries two load-bearing but never-spoken terms:
> *Caption:* "PostgreSQL 16.9 · 2,000,000 orders · **data in memory** · **parallel query off** · execution time (planning excluded), median of 7 runs."

The author's own argument notes admit "data in memory" is what lets page-count carry the whole argument — but the viewer only ever sees this as a silent caption. A careful viewer is left wondering what these two caveats mean and whether they matter, and it's never resolved.
**Rewrite:** Cut "parallel query off" from the caption (it does no explanatory work for this audience), and give "data in memory" one clause of narration in ch.1 — e.g. end the opening with "...same machine, same data sitting in memory both times" — so the caveat has a spoken anchor before it starts doing invisible work in every later page-count comparison.

## Test 5 — terms before explanation / concepts with two names
**SHOULD FIX.** "Bitmap scan" gets an explicit spoken bridge to its on-screen label ("PostgreSQL calls that a bitmap scan"), but "full scan" does not — it appears on screen twice as **Seq Scan** (ch.4, ch.5) with no narrated equivalence:
> *Screen:* "customer 4242, full scan forced (**Seq Scan**): 72.0 ms"

A viewer pausing on the plan tree has no way to know Seq Scan *is* the full scan just described in narration.
**Rewrite:** "Force a full scan — PostgreSQL's plan calls it a Seq Scan — for the same customer, and it takes seventy-two milliseconds..."

(Terms otherwise behave well: "pages"/"blocks" in ch.3 is a deliberate one-time gloss that pays off later when "Heap Blocks" appears on screen in ch.4/6 — that's a setup, not a naming conflict, so it's left alone.)

## Test 6 — numbers: which 2–3 matter, which do no work
Full inventory checked for internal consistency (all rounding — "9,000x," "nearly 5,000x," "no faster," "nearly 3x," "more than 2,000x" — verifies correctly against the raw figures in data/runs.txt; no arithmetic errors found).

**Worth remembering:** (1) 0.015 ms vs. 135.4 ms — the whole video's spine; (2) 10 pages vs. 12,739 pages — the mechanism; (3) 137 ms → 0.061 ms after `ANALYZE` — the takeaway punchline.

**NIT:** "PostgreSQL 16.9" and the on-screen exact Oslo count "99,900" do no narrative work — narration already says "almost all of the hundred thousand," so the precise digit is decoration, not memory-worthy content. Harmless; no rewrite needed, just noting it per the checklist.

## Test 7 — abstraction before the concrete case
No violation. Every abstract claim (two ways to find rows, the planner's cost estimate, "the plan is only as good as the estimate") is grounded with real numbers inside the same chapter, and this abstract→concrete-immediately pattern is consistent across ch.3, 4, 5, 6 — it reads as house style, not a lapse.

## Test 8 — wrong intuition confronted and shown failing
**Pass, and worth calling out as a strength.** All three wrong-model claims are directly shown failing on screen: "runs it the same way every time" is refuted by the forced-plan comparisons in ch.4/5; "index always faster" is refuted by customer 1's forced full scan being "no faster"; "if slow, add an index" is refuted explicitly in ch.6 ("nobody added one here... the planner just didn't expect it to help"). Nothing to fix.

## Test 9 — examples named but not understood
Overlaps with Test 5's Seq Scan gap — the only named-but-unbridged example. Tromsø/Oslo, bitmap scan, nested loop, and hash join are all given mechanism before name, so those are fine.

## Test 10 — on-screen text repeating narration / mismatched pictures
**NIT.** The ch.7 recap card echoes narration almost verbatim:
> *Narration:* "A rare customer gets the index, and ten pages. For a common one, every page has to be read, whatever the plan."
> *Screen:* "rare → index → 10 pages", "common → every page, whatever the plan."

This is a defensible end-card device, but if you want the screen to add rather than restate, split the labor: screen states the *what* (arrows/labels), narration gives the *why*, rather than the same words twice.

No picture/line mismatches found elsewhere — the screen directions are unusually well-fitted to what's being said throughout (ch.2's lighting-up loop vs. WHERE clause, ch.5's lookup/stream animation, ch.6's scan arrow).

## Test 11 — lines deletable without breaking anything
**Pass.** No line could be cut without losing either setup, payoff, or the causal chain — this is an unusually tight script. Closest candidate, "About nine thousand times longer" (ch.1), is never mechanically resolved later, but it earns its place rhetorically (raw ms values alone underplay the magnitude), so it's not a real cut candidate.

## Test 12 — hard to follow aloud / rushed or padded beats
**NIT.** Ch.5 briefly drops the concrete frame right at the naming moment:
> "That's a nested loop: **for each row on one side, look up its matches on the other.**"

Swapping to generic "row"/"side" language right after the concrete Tromsø walkthrough is a beat where a listener can lose track of which side is which.
**Rewrite:** "That's a nested loop: for each customer, look up their orders." — keep it concrete; let on-screen text carry the generic definition if needed.

No beat is rushed or padded relative to the stated ~150 wpm model — ch.4 carries the most concepts per chapter (statistics, cost, bitmap scan naming, two worked examples) but its word count gives it room; it's dense, not rushed.

---

**Summary of findings:** 2 SHOULD FIX (unspoken caption caveats; unbridged "Seq Scan"), 3 NIT (decorative numbers, recap-card echo, generic-language wobble in ch.5). No BLOCKING items — the causal chain is airtight (zero "and then"s), the wrong model is directly confronted three times, and the script is already unusually tight.

VERDICT: PASS
