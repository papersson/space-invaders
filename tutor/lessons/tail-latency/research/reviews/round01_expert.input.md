You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Your backend servers are fast. A typical request takes ten milliseconds.
> But about one request in a hundred hits a hiccup, and takes a full second.
> One slow request in a hundred sounds rare enough to live with.
> Now a user's page calls a hundred of these servers at once, and waits until every one has answered.
> How often is the page slow?

*Screen:* one backend: a stream of calls as short ticks (10 ms), with an occasional long bar (1 s) in coral, about 1 in 100. Then a page box fanning out to a 10 × 10 grid of backend servers, all lines converging back to the page. Title: "The Tail at Scale".

### 2. One in a hundred, a hundred times

> The page is fast only if all hundred calls are fast.
> Each call is fast ninety-nine times out of a hundred. For all hundred to be fast, multiply those chances together: zero point nine nine, a hundred times over.
> That comes to about thirty-seven percent.
> So sixty-three percent of pages wait at least a second.
> For one server, a slow call was the rare case. For the page, it's the usual case.

*Screen:* the 10 × 10 grid; twenty pages play in quick succession, each lighting its hundred calls, with the rare slow call in coral; a tally of slow pages climbs toward about 13 of 20. Then "0.99 × 0.99 × … (100 times) = 0.99¹⁰⁰ ≈ 0.37" and "1 − 0.37 = 63% of pages slow". A small line: "assumes the servers' hiccups are independent".

### 3. What the dashboard shows

> A dashboard of each server's average response time wouldn't warn you. With one call in a hundred taking a second, the average is about twenty milliseconds, and it looks healthy.
> The slow calls show up in the percentiles. The ninety-ninth percentile is the time that ninety-nine percent of calls finish within. For these servers, it's about a second.
> A page that waits on many servers feels their ninety-ninth percentile, not their average. The more servers a page calls, the more its users see the servers' slowest calls, which is why they're called the tail.

*Screen:* a latency distribution of one server (simulated, a million calls): a tall spike near 10 ms and a small bump at 1 s, on a log time axis. Markers: "average 20 ms", "median 10 ms", "99th percentile ≈ 1 s". Then the fraction of slow pages against the number of calls per page (1, 10, 50, 100): 1%, 10%, 39%, 63%.

### 4. Why not fix the slow calls?

> Why not just find the slow one percent and fix it?
> Because hiccups have many causes, and most are brief. A burst of traffic builds a queue. A garbage collector pauses the program. A background job, or another program on the same machine, borrows the disk or the processor for a moment.
> Each one is short, and lands on whichever calls happen to be running. You can make hiccups rarer, but in a large system you can't make them go away.
> So large systems are built to tolerate them, the way they tolerate machines that fail.

*Screen:* one server's timeline with brief stalls labelled "queue after a burst", "garbage collection pause", "background job", "neighbour on the same machine"; calls that overlap a stall stretch out.

### 5. Hedged requests

> The standard technique is the hedged request.
> Send the call to one server. If it hasn't answered by the ninety-fifth percentile, the time that ninety-five percent of calls finish within, send a copy to a second server that holds the same data. Use whichever answer comes back first.
> A call that hit a hiccup is usually rescued by the copy, because the second server is rarely stalled at the same moment.
> The cost is small. Only the slowest five percent of calls get a copy, so the servers see about five percent more work.
> In our simulation, hedging cut the share of slow pages from sixty-three percent to about one.
> Google measured the same effect. Reading a thousand values spread over a hundred servers, hedging after ten milliseconds cut the slowest tenth of a percent of reads from 1.8 seconds to 74 milliseconds, and sent only two percent more requests.
> But hedge too early, and every call gets a copy: twice the load, and busier servers are slower servers. Waiting for the ninety-fifth percentile keeps the extra load small.

*Screen:* a timing diagram: page → server A; a timer runs to the 95th-percentile mark (about 15 ms in our simulation); A is stalled (coral); a copy goes to server B, which answers at about 25 ms; A's call is dropped. A load meter: "+5% requests". Then two bars: "slow pages: 63% → 1% (simulated)". Then the Google numbers as a quoted result: "BigTable benchmark, 1,000 keys on 100 servers: 99.9th percentile 1,800 ms → 74 ms, +2% requests (Dean & Barroso, 2013)".

### 6. The answer

> So the page was slow sixty-three percent of the time because it waited on a hundred servers, and a one-in-a-hundred hiccup is almost certain to hit at least one of them.
> When a request fans out, watch your servers' ninety-ninth percentile, not their average. And instead of hunting every hiccup, design the fan-out to tolerate them.

*Screen:* the 10 × 10 grid with one coral call holding up the page, then the hedge rescuing it. End card: P(page fast) = p^N with p = the chance one call is fast and N = the calls per page, assuming independent calls; reference: Dean & Barroso, "The Tail at Scale", Communications of the ACM 56(2), 2013.


## Evidence

| Claim | Source |
|---|---|
| The example: servers that typically answer in 10 ms with a 99th percentile of 1 s; one server → 1 request in 100 slow; 100 servers in parallel → 63% of user requests take more than a second | Dean & Barroso, "The Tail at Scale", CACM 56(2), 2013 |
| 0.99¹⁰⁰ ≈ 0.366; 1 − 0.366 = 63.4% | Arithmetic; sim.py: 63.2% of 200,000 simulated pages |
| Slow-page fraction at 1 / 10 / 50 / 100 calls: 1% / 9.6% / 39.5% / 63.4% | 1 − 0.99^N |
| One server's average ≈ 20 ms, median 10 ms, 99th percentile ≈ 1 s | sim.py (a million calls: mean 20.4 ms, median 10.0 ms, p99 1,005 ms) |
| Causes of variability: shared resources, daemons and background jobs, garbage collection, queueing, and others | Dean & Barroso 2013, "Why Variability Exists?" |
| Hedged requests: send a secondary request after the first has been outstanding longer than the 95th-percentile expected latency; limits extra load to about 5% | Dean & Barroso 2013, "Within-request short-term adaptations" |
| Hedging in our simulation: slow pages 63% → 1.0%, +5.0% requests | sim.py (independent backends; hedge at the backend's p95, 15.5 ms) |
| Google BigTable benchmark: 1,000 keys over 100 servers; hedging after 10 ms cut the 99.9th-percentile latency from 1,800 ms to 74 ms with 2% more requests | Dean & Barroso 2013 |
| Busier servers are slower | M/M/1: response time = S/(1 − ρ) (Kleinrock 1975) |

