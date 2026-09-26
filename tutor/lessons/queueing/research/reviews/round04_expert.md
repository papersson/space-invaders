I reviewed the script's numbers and framing against M/M/1 queueing theory. The arithmetic and formulas check out exactly; my findings are mostly about citation accuracy and one pedagogical imprecision. (Note: I attempted to verify the Harchol-Balter chapter number via web search but the tool wasn't authorized in this session, so that one finding rests on my own recollection of the book rather than a fresh check — flagged accordingly.)

## Findings

**1. BLOCKING (pending verification) — likely wrong chapter citation**
> "T = S / (1 − ρ): mean response time for one server with Poisson arrivals and exponential work times (the M/M/1 queue; derived in Harchol-Balter ch. 13)"

What's wrong: My recollection of Harchol-Balter's *Performance Modeling and Design of Computer Systems* (2013) is that the M/M/1 derivation is in the chapter titled "The M/M/1 and PASTA," which I recall as **Chapter 14**, not 13 — Markov chain machinery (DTMCs/CTMCs) occupies the chapters immediately before it. I'm not 100% certain without the book in hand, but confident enough that this needs a check before it goes on screen — an on-screen citation error is exactly the kind of thing a viewer with the book will catch.
Correction: verify against the actual table of contents; if it's ch. 14, change "ch. 13" to "ch. 14."

**2. SHOULD FIX — mechanism in "spare capacity" framing is a metaphor, not the actual mechanism**
> "At eighty percent busy, new work fills eighty percent of the server's time. The other twenty percent is time it would otherwise sit idle. Call it spare capacity: it's what clears the queue... On average, the same queue takes about twice as long to clear"

What's wrong: 1−ρ is a long-run *time-average* idle fraction. During an actual busy period (i.e., while a queue exists), the server is working 100% of the time, not "80%" or "90%" — there's no idle time to speak of until the busy period ends. So framing spare capacity as the literal real-time rate at which an existing backlog drains is not how M/M/1 dynamics actually work; the true reason response time scales as S/(1−ρ) comes from queueing balance (Little's Law / the birth-death argument in ch. 5), not from a literal "clearing rate." The final numbers you get by this reasoning happen to come out right by dimensional analogy, but the causal story is a simplification a queueing-theory professor would want flagged.
Correction: soften the claim to make clear it's intuition, not derivation, e.g. "Think of it this way: ..." and let section 5 carry the actual derivation, or add a line like "that's the intuition — the exact reason takes a bit more math, coming up next."

**3. NIT — "read the load limit off the curve for your traffic" is ambiguous about which curve**
> "Decide how slow requests may get, and read the load limit off the curve for your traffic. On this curve, if a request may take five times its work time..."

What's wrong: Right after establishing that burstier/more-variable traffic needs a *different, higher* curve, "the curve for your traffic" could be read as "whichever curve matches your traffic's burstiness," but the very next sentence quietly switches to "this curve" (the plain M/M/1 one) for the concrete 80%-rule example. A viewer whose traffic is bursty may take the 80% number as directly applicable to them.
Correction: "Read the load limit off this curve if your traffic looks like this one — Poisson-ish arrivals, unpredictable-but-not-extreme work sizes. Burstier traffic needs more headroom than this curve says."

**4. NIT — informal description of Poisson independence**
> "Requests arrive at random, so sometimes several come close together... each unrelated to the others"

What's wrong: "unrelated to the others" is a loose gloss for the defining property (independent increments / memoryless interarrival times) of a Poisson process. Not incorrect, just imprecise — acceptable given the on-screen caption already says "Poisson arrivals (independent, at random)," so this is a nit, not a fix that's strictly necessary.
Correction: optional — "each arrival independent of when the last one happened."

## What's correct and doesn't need touching
Every numerical claim checks out exactly: 80/90 req/s → 80%/90% utilization, +12.5% traffic, T=S/(1−ρ) giving 20/50/100/200 ms at 50/80/90/95%, the 40 ms and 90 ms wait decompositions, the D/D/1 zero-wait argument (11.1 ms spacing), the 1/(1−0.8)=5 capacity-planning rule, the ln(100)≈4.6× tail-latency note (correctly kept out of the narration and saved for "the next lesson"), and the qualitative M/M/c claim (flatter-then-turns-up) are all textbook-correct and match your evidence table. Kleinrock's title/year and the Lazowska utilization law are correctly cited. The stability caveat (never run at 100%) is present and correctly placed at the end.

VERDICT: REVISE
