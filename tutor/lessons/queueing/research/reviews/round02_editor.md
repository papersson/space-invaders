# Review

## Test-by-test

**1. Opening question / ending answer.** Passes. Opens on "where do the other forty milliseconds come from" (§1) and closes with "So that's where the other forty milliseconds went: not into work, but into waiting" (§6) — explicit callback, same number, same phrase.

**2. One-sentence chain, report "and then."** Rebuilt from the script:
1→2: *but* work stays 10ms, *so* the rest is waiting *therefore* it's a queueing question.
2→3: *but* evenly-spaced fixed-work traffic never queues, even at 90%, *therefore* queues come from variability.
3→4: *therefore* what governs queue duration is spare capacity — halved from 20%→10%, so clearing time doubles.
4→5: *therefore* this generalizes to a curve, work÷spare, confirmed by simulation.
5→6: *therefore* the answer (waiting, not work) and the practice (headroom, burstiness).

**Zero "and then" instances** — every joint is causal, not sequential. This is a genuinely argued chain, not a list of facts.

**3. Announced vs. derived ideas.** Mostly derived. Minor exception: §5's "queueing theory gives the exact average response time" reads as an appeal to authority rather than a derivation — but it lands right after §4 has already informally derived the work/spare relationship, so the formula formalizes something the viewer has already reasoned to. NIT, not a real gap.

**4. Setups/payoffs.** All core setups pay off (work-vs-wait split, two kinds of variability, spare capacity, the curve). Two deliberate non-payoffs are explicitly flagged as future lessons (Little's Law, slowest requests) — correct practice. One under-flagged case: M/M/c in the end card (see #9).

**5. Terms before explanation / double names.** "Busy %" and "utilization" are the same concept under two names; the bridge sentence in §5 ("The fraction of time a server is busy is called its utilization") is late relative to four sections of saying "busy." Not confusing, but worth tightening. "Poisson arrivals" / "exponential work times" appear only on screen as captions, paired with plain-language narration — handled correctly, no violation.

**6. Numbers.** Full list: 10ms work; 80%→50ms; 90%→100ms; +12.5% ("an eighth") traffic; 40ms and 90ms waiting; "four times longer"; ~11ms interval; 20%/10% spare; 400 simulated requests (screen only); 50%→20ms, 80%→50ms, 90%→100ms, 95%→200ms; 20 million simulated requests; "5× work time → below 80%."

Worth remembering: **(a)** 80%→50ms vs. 90%→100ms — the phenomenon; **(b)** 20%→10% spare — the mechanism; **(c)** "below 80% if you can tolerate 5× work time" — the actionable rule.

Doing no work: "twenty million" (precision adds nothing over "millions"); "four times longer than it's worked on" (duplicates the bar chart already on screen).

**7. Abstraction before concrete case.** No violations — every abstraction (work/wait split, spare capacity, the formula) is introduced only after its concrete numeric case. This is a structural strength of the script.

**8. Wrong intuition confronted and shown failing.** Stated verbally ("You might expect... Instead...") and refuted *numerically* (doubling) and *implicitly* by the flat-then-steep curve shape, but never refuted *visually* side-by-side — no naive/linear line is ever drawn against the real curve. SHOULD FIX (below).

**9. Named-not-understood examples.** M/M/c in the end card is named but not unpacked — acceptable as a references-style teaser, but inconsistent with how the script elsewhere explicitly labels deferred material ("the next lesson"). NIT.

**10. On-screen text vs. narration; unsupportive pictures.** No violations found — screen numbers reinforce spoken numbers rather than repeating full sentences, and every visual (bar splits, timelines, dashed second curve) does distinct work.

**11. Deletable lines.** "four times longer than it's worked on" (§2) can be cut — the number and the bar chart already carry it.

**12. Hard-to-follow-aloud / pacing.** §5's four-point list ("At fifty percent... At eighty... At ninety... At ninety-five...") is dense and elliptical; screen support saves it, but it would benefit from one breath and a framing clause before the list. §6 stacks five distinct closing beats (recap, burstiness, headroom rule, averages caveat, 100%-warning) — not padded exactly, but reads as a checklist rather than one closing thought.

---

## Findings

1. **SHOULD FIX** — Wrong model is stated but never visually refuted.
   Quote: *"You might expect a little more traffic to mean a little more delay. Instead, the response time doubled."* (§1), with no return contrast at the curve reveal in §5.
   Rewrite: at the curve reveal, add a dashed straight line through the 50%/20ms point labeled "if delay just tracked load," with one line: *"If delay just tracked load, it would look like this. It doesn't."* Then continue into the flat-then-steep description.

2. **NIT** — Redundant ratio duplicating the visual.
   Quote: *"So at eighty percent busy, a request waits forty milliseconds in a queue, four times longer than it's worked on."*
   Rewrite: *"So at eighty percent busy, a request waits forty milliseconds in a queue. At ninety percent, it waits ninety."*

3. **NIT** — Decorative precision number.
   Quote: *"A simulation of twenty million requests at each load lands on the curve."*
   Rewrite: *"A simulation of millions of requests at each load lands on the curve."*

4. **NIT** — Dense numeric list, easy to rush aloud.
   Quote: *"At fifty percent busy, that's twenty milliseconds. At eighty, fifty. At ninety, a hundred. At ninety-five, two hundred."*
   Rewrite: *"At fifty percent busy, that's twenty milliseconds — barely more than the work itself. Then it climbs: eighty percent, fifty milliseconds. Ninety, a hundred. Ninety-five, two hundred."*

5. **NIT** — Concept has two names, bridged a little late.
   Quote: *"The fraction of time a server is busy is called its utilization."* (§5, after four sections of "busy.")
   Rewrite: fold the term in earlier, e.g. in §1: *"...eighty percent busy — call that its utilization —..."*

6. **NIT** — M/M/c named without being understood, unlike other deferred material.
   Quote: *"many servers sharing one queue stay flat for longer, then turn up the same way (M/M/c)"*
   Rewrite: *"...the same way — that's a topic for another lesson (M/M/c)."*

7. **NIT** — §6 stacks five distinct closing beats, feels list-like.
   Quote: entire §6.
   Rewrite: fold the averages caveat into the headroom sentence: *"...keep the server below eighty percent busy — remembering these are averages; some requests take far longer, which is the next lesson."*

VERDICT: PASS
