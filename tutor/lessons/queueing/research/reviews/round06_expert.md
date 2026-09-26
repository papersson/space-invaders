I reviewed the script line by line, re-derived every number from T = S/(1−ρ), and cross-checked it against the evidence table. The physics/math is sound throughout and the pedagogical sequencing (show the phenomenon → build informal intuition → state the exact formula *with* its assumptions) is well done — it correctly avoids claiming the exact formula before the Poisson/exponential assumptions are disclosed in §5. I attempted to verify one citation via web search but the tool wasn't authorized in this session, so that one item rests on memory rather than a checked source — flagged accordingly below.

## Findings

**SHOULD FIX** — *"the M/M/1 queue; derived in Harchol-Balter ch. 13"*
What's wrong: I could not verify this via search (tool access was denied), and my recollection of the book's structure is that M/M/1's mean response time is derived earlier, in the material building up from birth–death chains / continuous-time Markov chains (roughly the chapters just before or after where I'd place "ch. 13"), not necessarily at exactly chapter 13. I'm not confident enough to assert it's wrong, but I'm not confident it's right either, and this is the one claim in the script that's trivially falsifiable by a viewer with the book in hand — getting it wrong on an end card is the kind of error that quietly damages credibility.
Correction: Before shipping, check your own copy of Harchol-Balter (2013) and confirm the chapter number against the table of contents. If there's any doubt, a safer edit is to drop the specific chapter number and cite just "(Harchol-Balter 2013)" or point to the relevant Part rather than a pinpoint chapter.

**NIT** — end card: *"T = S / (1 − ρ) ... 'S: work time'"*
What's wrong: In the queueing literature S conventionally denotes the (random) service-time variable, with E[S] its mean — and the script itself establishes that work time varies randomly ("mostly short, sometimes several times longer"). Labeling S flatly as "work time" slightly blurs the variable/mean distinction for a viewer who goes looking at a textbook afterward.
Correction: Label it "S: mean work time per request" (or use E[S] in the on-screen formula) to make the mean vs. random-variable distinction explicit.

**NIT** — *"Call that twenty percent the spare capacity"*
What's wrong: "Spare capacity" for 1 − ρ isn't standard queueing-theory terminology (the standard object is just "1 − ρ," or, for M/M/1, the idle probability P₀ = 1 − ρ). This isn't a problem — it's a clear, harmless pedagogical coinage, and the script doesn't misrepresent it as textbook jargon — but it's worth a one-line acknowledgment so a student doesn't later search a textbook index for "spare capacity" and find nothing.
Correction: Optionally add, on first use, a small on-screen note like "(this is just 1 − ρ, sometimes called the idle probability)."

I checked in particular, and confirmed correct: the utilization arithmetic (80/90 req/s × 10 ms = 80%/90%); "an eighth more" (90/80 = 1.125); T = S/(1−ρ) giving 20/50/100/200 ms at 50/80/90/95%; the D/D/1 zero-wait argument (11.1 ms interarrival > wait); the Wq = T − S decomposition (40 ms, 90 ms); the halving-spare-capacity-doubles-response-time pattern from 80→90→95%; the "5× work time ⇒ ρ ≤ 80%" readoff (1/(1−0.8) = 5); the M/M/1 instability claim at ρ = 1; and the qualitative M/M/c pooling claim on the end card. All match the formula and the supplied simulation data, and every hedge about generality ("a first estimate," "usually need more headroom," "illustrative") is appropriately non-absolute — I found no overstated claims of optimality or universality.

VERDICT: PASS
