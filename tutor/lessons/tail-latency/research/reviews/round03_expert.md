Reviewed the full script and evidence table against the source material and the arithmetic. Findings below, ordered by severity.

## BLOCKING

**Quote:** *"Google measured this in a real system. For one server's call, the ninety-ninth percentile was ten milliseconds. For a request that waited on all of its servers, it was a hundred and forty."*

**Problem:** This is presented as a continuation of the running example (10 ms typical, 1 s p99, 100 servers, 63% slow), but per the evidence table it's actually a *different* real measurement from a different service (cited to "Table 1" specifically, while the toy example is cited more loosely to the paper generally). As written, "10 ms" now means something different than it did thirty seconds earlier in the same script — there it was the *typical/fast* latency, here it's the *99th percentile*. And "all of its servers" invites the viewer to assume this is still the same 100-server fan-out, when the real measurement likely has an unstated (and possibly different) server count. A viewer paying attention will think the numbers contradict what was just said.

**Fix:** Explicitly mark this as a separate, different real-world example before reusing "10 ms," e.g.: *"Google measured the same effect on a different, real service. There, a single server's own ninety-ninth percentile was much lower — just ten milliseconds. But a request that waited on all of that service's servers still had a ninety-ninth percentile of a hundred and forty milliseconds."* If the paper gives the actual leaf count for this example, state it instead of "all of its servers."

## SHOULD FIX

**Quote:** *"So the typical page is as slow as the servers' ninety-ninth percentile, not their average."*

**Problem:** This equivalence (typical/majority page latency ≈ component p99) is a coincidence of this example, where fan-out N (100) ≈ 1/p (100). It doesn't hold in general — for a much larger fan-out you'd need to look at the 99.9th or higher percentile, and for a small fan-out a lower percentile already dominates. Stated flatly, it teaches a rule that's only true at this specific N.

**Fix:** Tie the claim to the example, e.g.: *"In this example, the typical page is about as slow as the servers' 99th percentile, not their average — and the more servers a page calls, the higher a percentile you need to watch."* (The next line already gestures at this generalization; just don't let the sentence before it stand alone as a general law.)

**Quote:** *"Hedging after ten milliseconds cut the 99.9th percentile, the time all but one request in a thousand finish within, from 1.8 seconds to 74 milliseconds."*

**Problem:** The sentence just before it establishes "a thousand values" per request. Reusing "a thousand" here for a different population (1-in-1000 *whole requests*, not 1-in-1000 of the *1000 keys already mentioned*) is genuinely ambiguous on a single listen. A viewer can easily parse this as "1 of the 1000 keys is slow," which is not what's measured — it's the tail across many complete 1000-key requests.

**Fix:** Disambiguate, e.g.: *"...cut the 99.9th percentile — across many such thousand-key requests, the time all but one in a thousand of them finish within — from 1.8 seconds to 74 milliseconds."*

## NIT

**Quote:** *"the calls are like separate rolls of a hundred-sided die"*

A weighted-coin analogy (99% fast, 1% slow, flipped 100 times) conveys an asymmetric Bernoulli probability more directly than a hundred-sided die, which more naturally suggests 100 equally-likely outcomes. Not wrong, just a slightly less standard framing.

**Quote:** *"You can make hiccups rarer, but in a large system you can't make them go away."*

Slightly absolute — you can and do eliminate specific known causes (e.g., tuning away a GC pause). The real point, consistent with the paper, is that at scale some component is statistically almost always mid-hiccup from one of many independent causes. Consider "you can't make them go away everywhere at once" or similar.

**Quote:** *"Hedging suits reads. A copy of a write, like a payment, could happen twice, and making that safe is the next lesson."*

Fine content-wise, but it's a forward reference to material not shown here. Confirm the next lesson actually exists and covers this, or make the line self-contained.

## Verified as correct (no issue)
- The core setup, the 0.99¹⁰⁰ ≈ 0.366 → 63.4% arithmetic, the 1/10/50/100-server table (1.0%, 9.6%, 39.5%, 63.4%), the 20 ms average calculation, and the "average looks healthy / percentiles reveal the tail" framing all check out against the paper and against direct recomputation.
- The hedged-request description (trigger at p95, ~5% extra load, different-machine replica) matches the paper's "Within-request short-term adaptations" section precisely, including the 1,800 ms → 74 ms / 2% Bigtable benchmark figures.
- The closing independence caveat correctly reflects the paper's own limitation on these techniques.
- Citation (Dean & Barroso, CACM 56(2), 2013) is correct.

VERDICT: REVISE
