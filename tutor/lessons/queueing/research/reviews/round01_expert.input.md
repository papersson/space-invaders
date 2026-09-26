You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a server that does ten milliseconds of work for each request.
> When it's eighty percent busy, a request takes fifty milliseconds on average, from arrival to reply.
> Add an eighth more traffic, so it's ninety percent busy, and requests take a hundred milliseconds.
> The traffic grew a little. The response time doubled.
> Why? And where do the other forty milliseconds come from, when the work only takes ten?

*Screen:* a server box with requests (dots) arriving and leaving; "work: 10 ms per request (on average)". A dashboard-style panel: "80% busy → 50 ms", then "90% busy → 100 ms", with "+12.5% traffic" and "×2 response time". "simulated server" label. Title: "Why Busy Servers Get Slow".

### 2. Waiting, not working

> A request's response time has two parts: the time the server spends working on it, and the time it spends waiting for the server to be free.
> The work takes ten milliseconds, however busy the server is.
> So at eighty percent busy, a request waits forty milliseconds in a queue, four times longer than it's worked on. At ninety percent, it waits ninety.
> The question is really about queues. Why do they get so long, when the server still has time to spare?

*Screen:* a response-time bar split into a grey "waiting" part and an amber "work" part: 40 + 10 at 80%, 90 + 10 at 90%, to scale.

### 3. Where queues come from

> Suppose requests arrived evenly spaced, and every one took exactly ten milliseconds.
> At ninety percent busy, a new request would arrive every eleven milliseconds, and find the server already done with the last one.
> Nobody would ever wait. Every response would take ten milliseconds, even at ninety percent.
> Real traffic isn't like that. Requests arrive at random, so sometimes several arrive close together. And some requests need more work than others.
> When a clump arrives, the server can only work on one at a time, and the rest wait in a queue.
> So queues come from variability. What decides how long they last?

*Screen:* a timeline: evenly spaced arrivals every 11.1 ms, each 10 ms work block ending before the next arrival; queue counter stays 0; "response: 10 ms". Then random arrivals and random work lengths on the same timeline: a clump arrives, blocks stack into a queue; queue counter rises.

### 4. Spare capacity

> A queue only shrinks while the server works faster than new work arrives.
> At eighty percent busy, new work fills eighty percent of the server's time. The other twenty percent is spare, and that spare time is what clears the queue.
> At ninety percent busy, only ten percent is spare. The same queue takes twice as long to clear, and more requests arrive and join it while it does.
> Here's the same random stream of requests at both loads. At ninety percent, the queue builds higher and lasts longer.

*Screen:* a bar of the server's time split into "new work 80%" and "spare 20%", then "90% / 10%". Then two panels, requests in the system over time, the same random draws at 80% and 90% busy (400 requests, simulated): the 90% panel's queue is higher and longer-lived.

### 5. The curve

> Queueing theory gives the exact answer for the simplest case: one server, requests arriving at random, and a random amount of work for each.
> The average response time is the work time divided by the spare capacity.
> At fifty percent busy, that's twenty milliseconds. At eighty, fifty. At ninety, a hundred. At ninety-five, two hundred.
> A simulation of twenty million requests at each load lands on the curve.
> It's almost flat at first, then it climbs steeply, because each step toward a hundred percent takes a bigger share of the spare capacity that's left.
> Burstier traffic, or more variable work, makes the queues longer, so the curve climbs sooner. With many servers sharing one queue, it stays flat for longer, but it still turns up as they fill.

*Screen:* axes: utilization (0-100%) and average response time (ms). The curve W = 10 ms ÷ (1 − utilization) drawn left to right, labelled "response time = work time ÷ spare capacity" and, smaller, "W = S / (1 − ρ)"; points at 50/80/90/95% with their values; simulated points (dots) on the curve. "one server, random (Poisson) arrivals, random (exponential) work". Then a second, left-shifted curve labelled "burstier" (qualitative, dashed) and a flatter one "8 servers, one queue" (simulated).

### 6. The answer

> So a little more traffic doubled the response time because it halved the spare capacity, from twenty percent to ten.
> Response time follows the spare capacity, not the load.
> That's why capacity plans leave headroom. Decide how slow requests may get, and read the load limit off the curve. If a request may take five times its work time, keep the server below eighty percent busy.
> And never plan to run a server at a hundred percent. With no spare time, nothing clears the queue, and it keeps growing.

*Screen:* the curve again; 80% and 90% marked with spare 20% and 10% bars under the axis; "5× work time → below 80%" read off the curve with guide lines. End card: W = S / (1 − ρ) with S = work time, ρ = utilization, for one server with random arrivals and work (M/M/1); references: Harchol-Balter, Performance Modeling and Design of Computer Systems (2013); Kleinrock, Queueing Systems Vol. 1 (1975).


## Evidence

| Claim | Source |
|---|---|
| M/M/1 mean response time W = S/(1 − ρ); stable only for ρ < 1 | Kleinrock, Queueing Systems Vol. 1 (1975), ch. 3; Harchol-Balter, Performance Modeling and Design of Computer Systems (2013) |
| 20 / 50 / 100 / 200 ms at 50 / 80 / 90 / 95% with S = 10 ms | Arithmetic from the formula; simulation (sim.py, 20 million requests per load) |
| 80% → 90% is an eighth more traffic (+12.5%) | 0.9 / 0.8 = 1.125 |
| Evenly spaced arrivals with fixed 10 ms work never wait below 100% busy | Arithmetic: at 90% a request arrives every 11.1 ms; sim.py D/D/1 gives 10.0 ms at every load below 100% |
| Variability, not utilization alone, causes queueing; more variability makes it worse | Kingman (1961) heavy-traffic approximation for G/G/1: Wq ≈ ((Ca² + Cs²)/2) · ρ/(1 − ρ) · S; Harchol-Balter (2013) |
| Many servers sharing one queue: flatter for longer, still turns up | M/M/c (Erlang C); sim.py with 8 servers: 10.1 / 12.8 / 18.6 / 30.1 ms at 50 / 80 / 90 / 95% |
| Below 80% busy keeps the average response time within 5× the work time | 1/(1 − 0.8) = 5 |
| At 100% busy the queue keeps growing | M/M/1 is unstable for ρ ≥ 1 (Kleinrock 1975) |

