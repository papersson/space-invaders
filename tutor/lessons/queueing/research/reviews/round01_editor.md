## Test 1 — Opening question / ending callback

The opening asks two things: *why* did response time double, and *where do the other forty milliseconds come from*. The ending answers "why" (spare capacity halved) but never revisits "the other forty milliseconds" — the specific number and image from the opening just evaporates.

**SHOULD FIX** — Quote (§6): *"So a little more traffic doubled the response time because it halved the spare capacity, from twenty percent to ten."*
Rewrite: *"So a little more traffic doubled the response time because it halved the spare capacity, from twenty percent to ten — that's where the other forty milliseconds went: not into work, into waiting for spare time that wasn't there anymore."*

## Test 2 — Chain / "and then" audit

The script matches the author's own chain almost exactly:
1. Puzzle stated → **therefore** it's about waiting, not work (§2).
2. **But** evenly-spaced traffic never queues → **therefore** queues come from variability (§3).
3. **Therefore** look at spare capacity: halved 20%→10% (§4).
4. **Therefore** the general curve, confirmed by simulation (§5).
5. **Therefore** the practical rule (§6).

Zero instances of "and then" in the narration — this is a genuine but/therefore chain, not a list. Passes cleanly.

## Test 3 — Ideas announced vs. derived

Two ideas arrive without a visible problem generating them, both stapled onto the end of §5:
- "Burstier traffic... makes the queues longer" — asserted, not shown.
- "With many servers sharing one queue, it stays flat for longer" — asserted, not shown.

**SHOULD FIX** — Quote: *"Burstier traffic, or more variable work, makes the queues longer, so the curve climbs sooner. With many servers sharing one queue, it stays flat for longer, but it still turns up as they fill."*
Rewrite: cut the multi-server sentence entirely (see Test 4/11), and for burstiness, ground it in something already on screen: *"Burstier traffic — bigger clumps for the same average load — eats into that same spare capacity faster, so the curve climbs sooner."* This at least ties it back to the spare-capacity mechanism instead of asserting a new unexplained variable.

## Test 4 — Setups without payoffs, payoffs without setups

- **Objective 4 explicitly promises**: *"say why burstier traffic needs more headroom."* The script only asserts that it does, never says why. **BLOCKING** — a stated objective goes unmet.
  Quote: *"Burstier traffic, or more variable work, makes the queues longer, so the curve climbs sooner."*
  Rewrite: *"Burstier traffic means bigger clumps arrive together even at the same average load — and a bigger clump needs more spare time to clear, so the same twenty percent spare capacity buys less headroom."*
- The multi-server aside (**"8 servers, one queue"**) is a setup with no payoff anywhere in the script and no connection to any objective — a dangling thread. **SHOULD FIX**, see Test 11 for the cut.
- Everything else pays off cleanly: the §1 "simulated server" label is paid off by §4's simulated panels and §5's 20-million-request simulation; §3's "what decides how long they last?" is paid off by §4's spare-capacity answer.

## Test 5 — Terms before explained / multiple names for one concept

"Busy" is used consistently in narration through §1–4. In §5, the formula switches to **ρ** and the on-screen axis says **"utilization"** — but the narration never says the word "utilization" or ties it to "busy." A viewer has to infer silently that busy% = utilization = ρ.

**SHOULD FIX** — Quote (§5 screen note): *axis "utilization (0-100%)"* with narration that never uses the word.
Rewrite: add one clause, e.g. *"— what we've been calling 'busy' is properly called utilization, ρ —"* right before the formula is shown.

Minor: "spare time" (§4) and "spare capacity" (§4 title, §5 narration) are used interchangeably for the same quantity. **NIT** — pick one term and keep it throughout.

## Test 6 — Numbers

Full list: 10 ms work, 80%, 50 ms, +12.5% traffic, 90%, 100 ms, 40 ms wait, 90 ms wait, 11 ms arrival gap, 20% spare, 10% spare, 50%→20ms, 80%→50ms, 90%→100ms, 95%→200ms, 20,000,000 simulated requests, 8 servers, 5× work time / below 80%.

**Worth remembering:** 10 ms work time (the unit), the 80%→50ms / 90%→100ms doubling (the hook), and "below 80% busy keeps you under 5× work time" (the actionable rule).

**Numbers doing no work:**
- "8 servers" — arbitrary, never explained why 8, attached to the undeveloped pooling aside. **SHOULD FIX** (cut with the sentence, Test 11).
- "twenty million requests" — flavor/credibility only, doesn't change the argument. **NIT**, harmless as is.

## Test 7 — Abstraction before the concrete case

No violation. The video earns the general formula in §5 only after the concrete 80%/90% case and the mechanism (§2–4) are fully built. Good ordering.

## Test 8 — Wrong intuition confronted

Named wrong model: *"Latency grows in proportion to load, so 90% busy is only a little worse than 80%."* The script never states this intuition aloud — it only lets the 12.5%-traffic/100%-latency-increase contrast in §1 imply it. That's a workable implicit technique, but the "wrong idea" itself is never given to the viewer to hold and then have broken.

**SHOULD FIX** — Quote (§1): *"The traffic grew a little. The response time doubled."*
Rewrite: *"You'd expect a little more traffic to mean a little more waiting. Instead the response time doubled."* — this makes the naive model explicit before knocking it down, rather than relying on the viewer to supply it.

## Test 9 — Examples named but not understood

- "Queueing theory" — named, but its assumptions are stated (random arrivals, random work), so the usage is grounded even if the theory itself isn't derived. Fine.
- "Burstier traffic" and "many servers sharing one queue" — named, not understood (repeat of Test 3/4 finding).

## Test 10 — On-screen text vs. narration; pictures vs. line

- §1 dashboard ("+12.5% traffic", "×2 response time") closely mirrors the sentence *"The traffic grew a little. The response time doubled."* Reinforcing the two key numbers is defensible, but it's a near-verbatim echo. **NIT**.
- §6's "5× work time → below 80%" on screen matches the rule stated verbatim in narration. **NIT** — acceptable as a visual anchor for the one rule you want retained.
- The "burstier" (dashed, qualitative) and "8 servers" curves in §5 illustrate ideas the narration doesn't actually explain — the picture is ahead of the explanation. Covered under Test 3/4; not a separate defect once that's fixed.

## Test 11 — Deletable lines

**SHOULD FIX** — this line can be cut with no loss to the chain or any objective:
Quote: *"With many servers sharing one queue, it stays flat for longer, but it still turns up as they fill."* (and its screen counterpart, "8 servers, one queue")
Rewrite: delete. If the author wants to flag it as future material the way Little's Law was deferred, add one clause instead: *"— that's a question for another lesson."*

## Test 12 — Spoken clarity / pacing

- Awkward when heard aloud: *"The same queue takes twice as long to clear, and more requests arrive and join it while it does."* The trailing "while it does" is a weak referent. **NIT**.
  Rewrite: *"...and more requests pile on while that's happening."*
- Awkward: *"because each step toward a hundred percent takes a bigger share of the spare capacity that's left."* **NIT**.
  Rewrite: *"because near a hundred percent, every extra step eats a bigger fraction of the little spare capacity that's left."*
- **Pacing**: §5 is the densest section (formula, four data points, a 20M-request simulation, curve-shape reasoning) and then, in its last two sentences, crams in two more unexplained ideas (burstiness, pooling) right before the video pivots to the conclusion. This is a rushed beat. **SHOULD FIX** — resolved by the Test 3/4/11 cut; once the pooling sentence is removed and burstiness is given one grounded clause, the section's ending stops feeling rushed. Sections 1–4 and 6 are well-paced.

---

### Consolidated findings

1. **BLOCKING** — Objective 4 ("say why burstier traffic needs more headroom") is asserted, not explained. §5, *"Burstier traffic, or more variable work, makes the queues longer, so the curve climbs sooner."* → ground it in spare capacity (see Test 3/4 rewrite).
2. **SHOULD FIX** — Multi-server aside is an unexplained, unpaid-off tangent tied to no objective; cut it. §5, *"With many servers sharing one queue, it stays flat for longer, but it still turns up as they fill."*
3. **SHOULD FIX** — "Busy" (§1–4) and "utilization/ρ" (§5) are the same concept under two names, never explicitly linked.
4. **SHOULD FIX** — The wrong intuition is never spoken aloud, only implied; make it explicit in §1 before the reveal.
5. **SHOULD FIX** — Ending doesn't call back to the opening's specific "other forty milliseconds" framing.
6. **NIT** — "Spare time" vs. "spare capacity" used interchangeably in §4/§5.
7. **NIT** — Two sentences are awkward read aloud (§4 "...while it does"; §5 "...that's left"); rewrites given above.
8. **NIT** — §1 dashboard text near-verbatim echoes the "little/doubled" line.
9. **NIT** — "Twenty million requests" and "8 servers" are numbers that mostly do no argumentative work.

VERDICT: REVISE
