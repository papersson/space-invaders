# Review

## BLOCKING

**Quote:** *"End card: W = S / (1 − ρ) with S = work time, ρ = utilization, for one server with random arrivals and work (M/M/1)"* (and the smaller in-scene label in §5, "W = S / (1 − ρ)")

**Problem:** This labels the *total* response time (waiting + service) as "W." But the video's own cited source, Kleinrock's *Queueing Systems, Vol. 1* (1975), reserves W specifically for the mean *queueing* (waiting-only) time, and uses T for the mean time in system (response time): T = W + S̄. Under Kleinrock's own notation, the quantity this video computes (S/(1−ρ)) is his T, and his W would instead be ρS/(1−ρ) — the 40 ms / 90 ms wait numbers shown in §2. A student who opens the cited textbook to check the formula will find "W" defined as something else there. This is exactly the kind of citation/notation mismatch a professor would flag as wrong, not just sloppy, because the end card presents itself as the authoritative symbolic summary of the whole video.

**Fix:** Rename the symbol. Use R (response time) or T (matching Kleinrock's own T), and if you want to keep "W" for something, use it for the queueing-only time (40/90 ms), consistent with the cited source. E.g.: "R = S / (1 − ρ), the mean time in system, for M/M/1." If Harchol-Balter's text uses W differently, note that explicitly rather than relying on it silently.

## SHOULD FIX

**Quote:** *"Queueing theory gives the exact answer for the simplest case: one server, requests arriving at random, and a random amount of work for each."*

**Problem:** The formula W=S/(1−ρ) is exact only when service times are exponentially distributed (M/M/1) — it is not exact for "a random amount of work" in general. A deterministic work time with the same mean gives half the queueing delay (Pollaczek–Khinchine, Cs²=0 vs. 1); a heavy-tailed one gives much more. The on-screen caption correctly says "random (exponential) work," but the narration doesn't, and this creates a real internal contradiction two sentences later when the script says "more variable work... makes the queues longer" — that claim only makes sense if the baseline case already fixed a specific variability level (exponential), which the narration never states.

**Fix:** Say "...and each request's work time drawn from the same kind of random spread as the arrivals (exponentially distributed)" or similar, so the narration matches the screen caption and doesn't imply the formula is exact for arbitrary randomness.

**Quote:** *"That's why capacity plans leave headroom. Decide how slow requests may get, and read the load limit off the curve."*

**Problem:** This presents the mean-response-time curve as sufficient for real capacity planning. Every number in the video is explicitly an average, but real capacity planning is almost always driven by tail latency (p99/p999), which degrades far worse than the mean near saturation, plus other factors (burst headroom, failover capacity) not modeled here. As written, a viewer could walk away thinking "stay under 80%" is the whole story for real systems.

**Fix:** Add one line, e.g.: "This is the average — some requests wait much longer, especially near saturation, so real systems usually plan around a slow-request threshold (like p99), not the mean." This also better matches the honest "average" framing used everywhere else in the script.

**Quote (Evidence table):** *"M/M/c (Erlang C); sim.py with 8 servers: 10.1 / 12.8 / 18.6 / 30.1 ms at 50 / 80 / 90 / 95%"*

**Problem:** I recomputed the exact M/M/8 (Erlang C) values for S=10 ms: 50%→10.15 ms, 80%→12.86 ms, 90%→18.77 ms, 95%→31.10 ms (cross-checked via the Erlang-B recursion, C(8,7.6)≈0.844). The first three match the claimed simulated values almost exactly (within simulation noise). The 95% value (30.1 vs. theoretical 31.1, a ~3.5% gap) is a noticeably larger discrepancy than the pattern at the other three loads, which is where you'd expect the *most* simulation variance (heaviest tail), not less agreement than 90%. Worth confirming this isn't a sim.py bug or an under-sampled run before it's baked into the rendered curve.

**Fix:** Re-run/verify the 8-server, 95%-utilization data point in sim.py; expect ≈31.1 ms if using S=10 ms, M/M/8.

## NIT

- *"Response time follows the spare capacity, not the load."* — Spare capacity is just 1 − load, so this is a rhetorical contrast, not an independence claim. More precise: "Response time is a steep, nonlinear function of load, best read off the spare capacity it leaves." (Fine as pop-sci phrasing if you want to keep it, but flagging since a precise viewer could object.)
- *"a new request would arrive every eleven milliseconds"* — 10/0.9 = 11.1 ms, which the on-screen text correctly shows; narration rounds to "eleven." Say "about eleven" to match.
- End-card citations drop subtitles: Harchol-Balter's book is *Performance Modeling and Design of Computer Systems: Queueing Theory in Action*; Kleinrock's is *Queueing Systems, Volume I: Theory*. Minor, but easy to fix for citation completeness.
- *"a second, left-shifted curve labelled 'burstier'"* — Kingman's formula scales Wq by a multiplicative constant (Ca²+Cs²)/2; it's a vertical scaling of the curve, not a horizontal shift. Visually, on a fixed y-axis, a scaled-up curve does cross any given threshold at a lower utilization, so "climbs sooner" is a fair description of what a viewer sees — but "left-shifted" as a technical description overstates it. Already marked "qualitative, dashed," so low stakes.

## What's not a problem (double-checked)

All core arithmetic is correct: W=S/(1−ρ) gives 20/50/100/200 ms at 50/80/90/95%; wait times 40 ms and 90 ms at 80%/90%; 0.9/0.8 = 1.125 ("an eighth more"); D/D/1 zero-wait claim; the 5× threshold at ρ=0.8 (1/(1−0.8)=5); instability at ρ=1. The Kingman/G/G/1 formula is stated correctly and appropriately hedged as an approximation.

VERDICT: REVISE
