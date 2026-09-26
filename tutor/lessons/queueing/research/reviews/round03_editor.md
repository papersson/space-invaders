# Script Review — "Why Busy Servers Get Slow"

## 1. Opening question → ending callback
**Pass.** The cold open asks "where do forty of those fifty milliseconds come from?" and §6 answers it in almost the same words: "that's where the forty milliseconds went: not into work, but into waiting." Direct, clean callback.

## 2. Chain (one sentence per segment, but/therefore/and then)
The author's own chain holds up against the script — every link is "but" or "therefore," never "and then":

1. 10 ms work → 50 ms at 80%, 100 ms at 90%.
2. **But** work doesn't change with load, **therefore** the extra time is queueing.
3. **But** evenly-spaced fixed-length requests never queue, **therefore** queues come from variability.
4. **Therefore** what clears a queue is spare time, which halves 80→90%, so queue-clearing time doubles.
5. **Therefore** the general curve T = S/(1−ρ), confirmed by simulation.
6. **Therefore** the answer + the practical rule (headroom, burstiness).

**"and then" count: 0.** No arbitrary sequencing anywhere — every beat is causally forced by the previous one. This is the strongest part of the script.

## 3. Ideas announced vs. derived
- NIT — the exact formula itself is asserted rather than built: *"queueing theory gives the exact average response time... The answer is the work time divided by the spare capacity."* Everything up to this point was derived from a visible mechanism (queue draining rate); the formula's precise form (division, not e.g. an exponential) just appears. It's immediately backed by a 20M-request simulation matching the curve, which mostly earns the assertion — but a viewer paying close attention will notice this is the one place the video tells rather than shows. No rewrite needed given the simulation payoff; flagging so it isn't cut in a future pass.

## 4. Setups/payoffs
- SHOULD FIX — the burstiness payoff in §6 is thinner than everything around it and breaks the video's own rigor pattern. Every other claim in the script gets a mechanism and a simulated confirmation; burstiness gets an assertion and a curve explicitly labelled *"(illustrative)"*.
  **Quote:** *"Burstier traffic makes this worse. Bigger clumps build bigger queues, and the same spare capacity takes longer to clear them, so bursty traffic needs more spare capacity for the same response time."*
  **Rewrite:** give it one concrete instance the way §3 did for ordinary variability, e.g. *"Imagine the same ninety percent utilization, but requests now arrive in clumps of five instead of one at a time. The queue that clump creates is five times as deep, and it still only drains at ten percent capacity — so it takes five times as long to clear. That's why bursty traffic needs more headroom for the same response time."* Even without a full simulation, this gives the assertion a mechanism instead of leaving it as a stated fact.
- Everything else pays off: the 12% traffic number is paid off by the "wrong model" contrast at the end; the "clump" setup in §3 is paid off in §4 and again in §6; the 5×-work-time headroom rule in §6 is a direct callback to the 80%→50ms point already on the curve, not a new number. Little's Law and "slowest requests" are deliberately deferred, not broken payoffs.

## 5. Terms before explanation / concepts with two names
No real violations. "Utilization" is named in §5 only after four sections of plain "80% busy" — that's the right order (concrete before label), not a premature term. "Poisson arrivals" / "exponential work times" get a plain-English gloss before the jargon appears on screen. One minor looseness:
- NIT — §1 says *"a little more delay"* where the rest of the script says "response time" or "wait." Harmless, but if you want one vocabulary, swap "delay" for "response time" even in the cold open.

## 6. Numbers
All numbers in order: 10 ms work · 80% busy · 50 ms · ~12.5% more traffic · 90% busy · 100 ms · 40 ms wait · "4× the work" · 90 ms wait · ~11 ms inter-arrival · 20%/10% spare capacity · 400 requests (simulated, on-screen only) · 50%→20ms, 80%→50ms, 90%→100ms, 95%→200ms · 20,000,000 simulated requests · 5× work-time → 80% rule.

**Worth remembering: 80%→50ms, 90%→100ms, and 20%→10% spare capacity.** Those three carry the entire argument; everything else is in service of them.

- NIT — **400** and **20,000,000** do no conceptual work; they're methodology credentials, not something the takeaway depends on. Fine to keep for trust, but don't mistake them for numbers the viewer needs to retain.

## 7. Abstraction before the concrete case
**Pass.** Utilization, the formula, and the M/M/1 label all arrive after the concrete 10ms/80%/90% case is fully built. This is the one area where the script's discipline is airtight.

## 8. Wrong intuition
Named in the brief as "latency grows in proportion to load, so 90% is only a little worse than 80%," and shown failing directly in §1: *"You might expect a little more traffic to mean a little more delay. Instead, the response time doubled."* Confronted and shown failing — pass.

## 9. Examples named but not understood
- NIT — M/M/1 and M/M/c are named in the end card with only a phrase each ("derivable from Little's Law," "stay flat for longer, then turn up the same way"). That's appropriate for a deliberately-deferred teaser, but worth confirming that's the intent rather than a compressed explanation that got cut for time.

## 10. On-screen text vs. narration / pictures vs. lines
- NIT — §1's on-screen "+12.5% traffic" / "2× response time" repeats the narrated numbers verbatim. Acceptable as reinforcement in a numbers-heavy explainer; flagging per the test, not recommending a cut.
- SHOULD FIX — the burstiness curve is drawn "dashed... illustrative" right after two sections that leaned hard on "simulation lands exactly on the curve" as proof. The visual language (dashed, no dots) does correctly signal "not measured," but it sits directly under a curve whose whole selling point was measured precision — a careful viewer may wonder whether it's actually true or just plausible-looking. Consider labelling it on screen ("qualitative, not to scale") rather than trusting "illustrative" alone to carry that distinction.

## 11. Deletable lines
- NIT — *"These are averages, and some requests take several times longer. The slowest requests are the next lesson."* This is the only line in the script that isn't required by the chain — it's a legitimate caveat and a fair teaser, but it could be cut with zero damage to this video's own argument. Keep if you want the caveat on record; cut if you want the ending to land purely on the takeaway.

## 12. Hard-to-follow-aloud sentences / pacing
- SHOULD FIX — §5 is the densest beat in the script relative to its likely runtime: it introduces the term "utilization," states the formula, gives four data points, cites a 20M-request simulation, and describes the curve's shape (flat-then-steep) with a doubling argument run twice (80→90, 90→95) — all in roughly 130 words (~50 seconds at 150 wpm), while the screen has to reveal axes, curve draw-in, formula + subscript labels, four labelled points, simulated dots, a two-part caption, and then a second highlighted overlay of the 80/90/95 steps. Recommend either splitting §5 into two beats (curve + assumptions, then the 80→90→95 walkthrough) or cutting one data point (50%/20ms is the least load-bearing) to give the visual room to breathe.
- NIT — *"At ninety percent busy, ten milliseconds of work fills ninety percent of the gap between requests, so a new one arrives about every eleven milliseconds."* This asks the ear to do a division mid-sentence. **Rewrite:** *"At ninety percent busy, requests arrive on average every eleven milliseconds — just a hair after the ten milliseconds each one takes to handle."* Leads with the number the viewer needs, then explains it, instead of making them derive it from "fills ninety percent of the gap."

---

VERDICT: PASS
