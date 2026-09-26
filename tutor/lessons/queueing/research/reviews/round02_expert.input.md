You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a server that does ten milliseconds of work for each request.
> When it's eighty percent busy, a request takes fifty milliseconds on average, from arrival to reply.
> Add an eighth more traffic, so it's ninety percent busy, and requests take a hundred milliseconds.
> You might expect a little more traffic to mean a little more delay. Instead, the response time doubled.
> Why? And where do the other forty milliseconds come from, when the work only takes ten?

*Screen:* a server box with requests (dots) arriving and leaving; "work: 10 ms per request, on average". A panel: "80% busy → 50 ms", then "90% busy → 100 ms" with "+12.5% traffic" under the first arrow and "2× response time" under the second. A small "simulated server" label. Title: "Why Busy Servers Get Slow".

### 2. Waiting, not working

> A request's response time has two parts: the time the server spends working on it, and the time it spends waiting for the server to be free.
> The work takes ten milliseconds, however busy the server is.
> So at eighty percent busy, a request waits forty milliseconds in a queue, four times longer than it's worked on. At ninety percent, it waits ninety.
> The question is really about queues. Why do they get so long, when the server still has time to spare?

*Screen:* a response-time bar split into a grey "waiting" part and an amber "work" part: 40 + 10 at 80%, 90 + 10 at 90%, to scale.

### 3. Where queues come from

> Suppose requests arrived evenly spaced, and every one took exactly ten milliseconds.
> At ninety percent busy, ten milliseconds of work fills ninety percent of the gap between requests, so a new one arrives about every eleven milliseconds.
> It finds the server already done with the last one. Nobody ever waits, and every response takes ten milliseconds, even at ninety percent busy.
> Real traffic varies in two ways. Requests arrive at random, so sometimes several come close together. And some requests need much more work than others.
> When a clump arrives, the server can only work on one at a time, and the rest wait in a queue.
> So queues come from variability. What decides how long they last?

*Screen:* a timeline: evenly spaced arrivals every 11.1 ms, each 10 ms work block ending before the next arrival; queue counter stays 0; "response: 10 ms". Then random arrivals and random work lengths on the same timeline: a clump arrives, blocks stack into a queue; queue counter rises.

### 4. Spare capacity

> A queue only shrinks while the server works faster than new work arrives.
> At eighty percent busy, new work fills eighty percent of the server's time. The other twenty percent is its spare capacity, and spare capacity is what clears the queue.
> At ninety percent busy, the spare capacity is only ten percent. The same queue takes twice as long to clear, and more requests pile on while that happens.
> Here's the same random stream of requests at both loads. At ninety percent, the queue builds higher and lasts longer.

*Screen:* a bar of the server's time split into "new work 80%" and "spare capacity 20%", then "90% / 10%". Then two panels, requests in the system over time, the same random draws at 80% and 90% busy (400 requests, simulated): the 90% panel's queue is higher and longer-lived.

### 5. The curve

> The fraction of time a server is busy is called its utilization.
> For the simplest case, queueing theory gives the exact average response time. The case is one server, requests arriving independently at random, and work times that vary just as randomly: mostly short, sometimes several times longer.
> The answer is the work time divided by the spare capacity: ten milliseconds divided by one minus the utilization.
> At fifty percent busy, that's twenty milliseconds. At eighty, fifty. At ninety, a hundred. At ninety-five, two hundred.
> A simulation of twenty million requests at each load lands on the curve.
> It's almost flat at first, then steep. From eighty to ninety percent, the spare capacity halves, and the response time doubles. From ninety to ninety-five, it halves and doubles again.

*Screen:* axes: utilization (0-100%) and average response time (ms). The curve drawn left to right, labelled "response time = work time ÷ spare capacity" and, smaller, "T = S / (1 − ρ)" with "S: work time, ρ: utilization"; points at 50/80/90/95% with their values; simulated points (dots) on the curve. Caption: "one server; Poisson arrivals (independent, at random); exponential work times". Then the 80 → 90 → 95 steps highlighted with "spare 20% → 10% → 5%" and "50 → 100 → 200 ms".

### 6. The answer

> So that's where the other forty milliseconds went: not into work, but into waiting. A little more traffic halved the spare capacity, from twenty percent to ten, and doubled the time requests spend waiting for it.
> Burstier traffic makes this worse. Bigger clumps build bigger queues, and the same spare capacity takes longer to clear them, so bursty traffic needs more spare capacity for the same response time.
> That's why capacity plans leave headroom. Decide how slow requests may get, and read the load limit off the curve for your traffic. On this curve, if a request may take five times its work time on average, keep the server below eighty percent busy.
> These are averages, and some requests take several times longer. The slowest requests are the next lesson.
> And never plan to run a server at a hundred percent busy. With no spare capacity, nothing clears the queue, and it keeps growing.

*Screen:* the curve again; 80% and 90% marked with spare 20% and 10% bars under the axis; the waiting part of the 50 ms and 100 ms bars from chapter 2. A second curve above it, dashed, "burstier traffic (illustrative)". "5× work time → below 80%" read off the curve with guide lines. End card: T = S / (1 − ρ): mean response time for one server with Poisson arrivals and exponential work times (the M/M/1 queue); "many servers sharing one queue stay flat for longer, then turn up the same way (M/M/c)"; references: Harchol-Balter, Performance Modeling and Design of Computer Systems: Queueing Theory in Action (2013); Kleinrock, Queueing Systems, Volume I: Theory (1975).


## Evidence

| Claim | Source |
|---|---|
| M/M/1 mean response time T = S/(1 − ρ) (Kleinrock's T, Harchol-Balter's E[T]; Kleinrock's W is the waiting part only); stable only for ρ < 1 | Kleinrock, Queueing Systems Vol. 1 (1975), ch. 3; Harchol-Balter, Performance Modeling and Design of Computer Systems (2013) |
| 20 / 50 / 100 / 200 ms at 50 / 80 / 90 / 95% with S = 10 ms | Arithmetic from the formula; simulation (sim.py, 20 million requests per load): 20.0 / 50.0 / 100.5 / 199.1 ms |
| 80% → 90% is an eighth more traffic (+12.5%) | 0.9 / 0.8 = 1.125 |
| Evenly spaced arrivals with fixed 10 ms work never wait below 100% busy | Arithmetic: at 90% a request arrives every 11.1 ms; sim.py D/D/1 gives 10.0 ms at every load below 100% |
| Variability, not utilization alone, causes queueing; burstier arrivals or more variable work make it worse (bigger queues at the same utilization) | Kingman (1961) heavy-traffic approximation for G/G/1: Wq ≈ ((Ca² + Cs²)/2) · ρ/(1 − ρ) · S; Harchol-Balter (2013) |
| End card: many servers sharing one queue stay flat for longer, then turn up | M/M/c (Erlang C); sim.py with 8 servers (20 million requests per load): 10.1 / 12.9 / 18.8 / 31.1 ms at 50 / 80 / 90 / 95% |
| Below 80% busy keeps the average response time within 5× the work time | 1/(1 − 0.8) = 5 |
| At 100% busy the queue keeps growing | M/M/1 is unstable for ρ ≥ 1 (Kleinrock 1975) |
| These are averages; some requests take several times longer | M/M/1 response time is exponentially distributed with mean S/(1 − ρ), so its p99 is ln(100) × the mean ≈ 4.6 × the mean (Harchol-Balter 2013) |

