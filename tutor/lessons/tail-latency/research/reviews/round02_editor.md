# Script Review

**1. Opening question ↔ ending answer.** PASS. Opens with "How often is the page slow?"; closes with "the page was slow sixty-three percent of the time because it waited on a hundred servers" — direct callback, both in number and in mechanism.

**2. Chain (but/therefore/and then).**
1. Question: 1-in-100 hiccup, page waits on 100 calls → how often slow?
2. **Therefore** multiply: 0.99¹⁰⁰≈37%, so 63% slow.
3. **But** the average looks healthy. **Therefore** watch percentiles.
4. **But** why not fix the 1%? Because causes are many/brief. **Therefore** tolerate.
5. **Therefore** hedge. **But** hedge too early doubles load.
6. **Therefore** the answer.

"and then" count: **0**. Clean causal chain, no padding connective used.

**3. Ideas announced vs. derived.** Mostly derived. One soft spot — NIT: "large systems are built to tolerate them, the way they tolerate machines that fail" is an analogy dropped in rather than earned; nothing on screen shows this comparison. Not load-bearing, but it's asserted, not shown.

**4. Setups/payoffs.**
- SHOULD FIX (setup without payoff): "Hedging suits reads. A copy of a write, like a payment, could happen twice, and making that safe is the next lesson." This opens a new problem (write-safety) one line before the video's actual resolution, with no payoff in this video. It's a forward-reference to a different lesson landing right at the climax beat.
  - *Rewrite:* Cut it, or self-close it: "Hedging suits reads, where a repeat is harmless — a write, like a payment, isn't, which is why you only hedge reads."
- Good, matched pair (no fix needed): independence (seg. 2) → "the copy goes to a server on a different machine" (seg. 5); queueing (seg. 4) → "busier servers answer more slowly" (seg. 5).

**5. Terms before explanation / double names.**
- NIT: "hiccup" (1,4), "slow call" (2,3), and "stall/stalled" (5) all name the same event without being explicitly equated. A careful listener may briefly wonder if "stall" is a new, different failure mode.
  - *Rewrite:* first use in seg. 5 as "stalled — hit its hiccup —" to anchor it back to the established word.
- Percentile, 99th percentile, and "tail latency" all land in segment 3 within a few sentences — not wrong, but dense (see test 12).

**6. Numbers.** Full list: 10 ms, 1-in-100, 1 s, 100 calls, 0.99¹⁰⁰≈0.37, 63%, ~20 ms avg, median 10 ms, 99th pct≈1 s, {1,10,50,100 calls→1%,9.6%,39.5%,63.4%}, 95th pct, ≤5%, 63%→1% (sim), 1,000 keys/100 servers, 10 ms trigger, 1.8 s→74 ms, 2%, 2013.

Worth remembering: **63%** (the headline shock), **99th percentile** (what to watch), **95th percentile** (the hedge trigger).

- SHOULD FIX: the Google stat crams four new numbers into one metric your video hasn't used (99.9th-percentile *time*, not "share of slow pages") right after you already delivered your own payoff (63%→1%). It also hedges "after ten milliseconds" — a flat time, not "the 95th percentile" you just built as the rule — with no acknowledgment of the switch. This risks the viewer wondering which number is the "real" answer and whether the rule just changed.
  - *Rewrite:* "Google measured the same trade at a different scale — a thousand values fanned out per request. Hedging cut their slowest requests by 96 percent for two percent more load: the same shape of result, on a system where the danger is even bigger."

**7. Abstraction before concrete case.** PASS. Every abstraction (percentile, formula, "technique") follows a worked concrete number first.

**8. Wrong intuition.** Named indirectly ("sounds rare enough to live with") and shown failing twice: quantitatively (63%) and structurally (the dashboard would say "healthy" while most pages are slow). Effective, no fix needed.

**9. Examples named but not understood.**
- SHOULD FIX: "BigTable" is name-dropped with no explanation of what it is, and "a thousand values from a hundred servers" is a new configuration that doesn't map cleanly onto the video's running example (100 calls, not 1,000). The example is cited, not built — it functions as an authority stamp ("Google measured...") rather than something the viewer can follow.
  - *Rewrite:* drop "BigTable" (irrelevant to the point) and rescale the comparison so it reads as the same experiment, bigger: see rewrite in #6.

**10. On-screen text vs. narration / pictures vs. line.**
- NIT: screen text "independent: one server's hiccup doesn't make another's more likely" nearly repeats the spoken clause verbatim, as does "≤5% more requests" next to "at most five percent more requests." Low cost, but could carry more information instead (e.g., show two correlated servers crossed out).
- NIT: the "tolerate them, the way they tolerate machines that fail" line (seg. 4) has no supporting visual — the screen is still the stall timeline, which illustrates causes, not the fault-tolerance analogy.

**11. Deletable lines.**
- "That's why this is called tail latency." — deletable; pure naming aside, argument doesn't depend on the term reappearing.
- "Hedging suits reads... the next lesson." — deletable (see #4/#9's fix).
- The Google-benchmark paragraph is optional for the *logic* (the simulated 63%→1% already delivers objective 3's payoff) — keep for credibility, but tighten per #6/#9 rather than cut outright.

**12. Hard-to-follow sentences / pacing.**
- SHOULD FIX: "Each call is fast ninety-nine times out of a hundred. If the servers' hiccups are independent, so that one server stalling doesn't make another more likely to stall, the calls are like separate rolls of a hundred-sided die." — the payoff clause ("like separate rolls of a hundred-sided die") is stranded after a long embedded qualifier; hard to hold by ear.
  - *Rewrite:* "Each call is fast ninety-nine times out of a hundred — like a hundred-sided die landing on 'fast.' That only works if the servers' hiccups are independent: one stalling doesn't make another more likely to."
- SHOULD FIX: "Hedging after ten milliseconds cut the 99.9th percentile from 1.8 seconds to 74 milliseconds, and cost only two percent more requests." — four numbers in one breath; the on-screen direction already splits this into three labelled parts, but the narration doesn't match that pacing.
  - *Rewrite:* "Hedge after ten milliseconds. The slowest requests — the 99.9th percentile — dropped from 1.8 seconds to 74 milliseconds. And it cost two percent more traffic."
- Segment 3 is slightly rushed: three new terms (percentile, 99th percentile, tail latency) land back-to-back. Not padded elsewhere; overall pacing is otherwise brisk and appropriate.

---

No item here breaks the core chain, contradicts the math, or leaves the opening question unanswered — the issues are clarity/density fixes concentrated around the Google-benchmark beat and one sentence each in segments 2 and 5.

VERDICT: PASS
