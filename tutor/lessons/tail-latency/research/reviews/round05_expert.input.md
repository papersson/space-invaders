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
> Each call is fast ninety-nine times out of a hundred. Assume the hiccups are independent: one server hitting a hiccup doesn't make another more likely to. Then the hundred calls are like a hundred separate coin flips, each coin weighted to come up fast ninety-nine times in a hundred.
> The chance that all hundred come up fast is ninety-nine percent, times ninety-nine percent, a hundred times over.
> That comes to about thirty-seven percent.
> So sixty-three percent of pages wait at least a second.
> For one server, a slow call was the rare case. For the page, it's the usual case.

*Screen:* the 10 × 10 grid; twenty pages play in quick succession, each lighting its hundred calls, with the rare slow call in coral; a tally of slow pages climbs toward about 13 of 20. Then "0.99 × 0.99 × … (100 times) = 0.99¹⁰⁰ ≈ 0.37" and "1 − 0.37 = 63% of pages slow", with "independent: one server's hiccup doesn't make another's more likely".

### 3. What the dashboard shows

> A dashboard of each server's average response time wouldn't warn you. Ninety-nine calls at ten milliseconds and one at a second average out to about twenty milliseconds, which looks healthy.
> The slow calls show up in the percentiles. The ninety-ninth percentile is the time that ninety-nine percent of calls finish within. For these servers, it's about a second.
> Those rare, slow calls make up the long tail of each server's latency distribution. That's why this is called tail latency.
> Most pages that wait on a hundred servers include a call from their slowest one percent. So with a hundred calls, the typical page is as slow as the servers' ninety-ninth percentile, not their average. With more calls per page, an even rarer, slower percentile decides.
> Turn that around. For the page itself to be slow only one time in a hundred, each of its hundred servers would have to be slow only one time in ten thousand.

*Screen:* a latency distribution of one server (simulated, a million calls): a tall spike near 10 ms and a small bump at 1 s, on a log time axis, the bump labelled "the tail". Markers: "average 20 ms = (99 × 10 ms + 1 × 1,000 ms) ÷ 100", "median 10 ms", "99th percentile ≈ 1 s". Then the fraction of slow pages against the number of calls per page (1, 10, 50, 100): 1.0%, 9.6%, 39.5%, 63.4%. Then the converse: "page slow 1 in 100 → each server slow 1 in 10,000".

### 4. Why not fix the slow calls?

> Why not just find the slow one percent and fix it?
> Because hiccups have many causes, and most are brief. A burst of traffic builds a queue. A garbage collector pauses the program. A background job, or another program on the same machine, borrows the disk or the processor for a moment.
> Each one is short, and lands on whichever calls happen to be running. You can remove some causes and make hiccups rarer, but in a large system you can't make them all go away.
> So large systems are built to tolerate them, the way they tolerate machines that fail.

*Screen:* one server's timeline with brief stalls labelled "queue after a burst", "garbage collection pause", "background job", "neighbour on the same machine"; calls that overlap a stall stretch out.

### 5. Hedged requests

> One standard technique is the hedged request.
> Send the call to one server. If it hasn't answered by the ninety-fifth percentile, the time that ninety-five percent of calls finish within, send a copy to a second server that holds the same data. Use whichever answer comes back first.
> A call that hit a hiccup is usually rescued by the copy, as long as the two servers don't hit a hiccup at the same moment. So the copy goes to a server on a different machine, where the same hiccup is unlikely to reach it.
> The cost is small. Only calls slower than the ninety-fifth percentile get a copy, so the servers see about five percent more requests.
> In our simulation, hedging cut the share of slow pages from sixty-three percent to about one percent.
> Google measured hedging on a real system. In one benchmark, each request read a thousand values from a hundred servers. Across many of these requests, hedging after a fixed ten milliseconds cut the 99.9th percentile, the time that 99.9 percent of them finish within, from 1.8 seconds to 74 milliseconds. It cost only two percent more requests.
> But hedge too early, and every call gets a copy. That's twice the load, and more load means longer queues, so busier servers answer more slowly. Waiting for the ninety-fifth percentile keeps the extra load small.
> Hedging suits reads. A copy of a write, like a payment, could happen twice, and making that safe is the next lesson.

*Screen:* a timing diagram: page → server A; a timer runs to the 95th-percentile mark (about 15 ms in our simulation); A is stalled (coral); a copy goes to server B on another machine, which answers at about 25 ms; A's call is dropped. A load meter: "≈ 5% more requests". Then two bars: "slow pages: 63% → 1% (simulated)". Then the Google result laid out as three labelled parts: "trigger: hedge after 10 ms", "result: 99.9th percentile 1,800 ms → 74 ms", "cost: +2% requests" (Dean & Barroso, 2013; Bigtable, 1,000 keys on 100 servers).

### 6. The answer

> So the page was slow sixty-three percent of the time because it waited on a hundred servers, and a one-in-a-hundred hiccup is more likely than not to hit at least one of them.
> When a request fans out, watch your servers' ninety-ninth percentile, their tail latency, not their average. And instead of hunting every hiccup, design the fan-out to tolerate them.
> All of this assumes the hiccups are independent. When one cause hits many servers at once, like a network blip, the arithmetic changes, and a hedge's copy may be slow too.

*Screen:* the 10 × 10 grid with one coral call holding up the page, then the hedge rescuing it. End card: P(page fast) = p^N with p = the chance one call is fast and N = the calls per page, assuming independent calls; reference: Dean & Barroso, "The Tail at Scale", Communications of the ACM 56(2), 2013.


## Evidence

| Claim | Source |
|---|---|
| The example: servers that typically answer in 10 ms with a 99th percentile of 1 s; one server → 1 request in 100 slow; 100 servers in parallel → 63% of user requests take more than a second | Dean & Barroso, "The Tail at Scale", CACM 56(2), 2013 |
| 0.99¹⁰⁰ ≈ 0.366; 1 − 0.366 = 63.4% | Arithmetic; sim.py: 63.2% of 200,000 simulated pages |
| Slow-page fraction at 1 / 10 / 50 / 100 calls: 1% / 9.6% / 39.5% / 63.4% | 1 − 0.99^N |
| Average ≈ 20 ms from 99 calls at 10 ms and 1 at 1,000 ms | (99 × 10 + 1,000) / 100 = 19.9 ms |
| "Tail latency" names the long tail of a single server's latency distribution | Dean & Barroso 2013 |
| One server's average ≈ 20 ms, median 10 ms, 99th percentile ≈ 1 s | sim.py (a million calls: mean 20.4 ms, median 10.0 ms, p99 1,005 ms) |
| Causes of variability: shared resources, daemons and background jobs, garbage collection, queueing, and others | Dean & Barroso 2013, "Why Variability Exists?" |
| Hedged requests: send a secondary request after the first has been outstanding longer than the 95th-percentile expected latency; "limits the additional load to approximately 5%" | Dean & Barroso 2013, "Within-request short-term adaptations" |
| Hedging relies on uncorrelated hiccups; send the copy where the same cause can't reach it | Dean & Barroso 2013 (tied requests and replica choice discussion) |
| Hedging duplicates the request, so it suits reads; duplicated writes need idempotency | Dean & Barroso 2013 discuss hedging for reads (e.g., BigTable); idempotency: Kleppmann, DDIA ch. 11 |
| Hedging in our simulation: slow pages 63% → 1.0%, +5.0% requests | sim.py (independent backends; hedge at the backend's p95, 15.5 ms) |
| Google Bigtable benchmark: 1,000 keys over 100 servers; hedging after 10 ms cut the 99.9th-percentile latency (for all values to arrive) from 1,800 ms to 74 ms with 2% more requests | Dean & Barroso 2013, verified in research/canonical_web_agent.md |
| For the page to be slow 1 time in 100 with 100 calls, each call must be slow about 1 time in 10,000 | 1 − (1 − p)¹⁰⁰ = 0.01 → p ≈ 0.0001 |
| Correlated hiccups change the arithmetic and defeat hedging | Dean & Barroso 2013: techniques are "effective only when the phenomena that causes variability does not tend to simultaneously affect multiple request replicas" |
| Busier servers are slower | M/M/1: response time = S/(1 − ρ) (Kleinrock 1975) |

