# The tail at scale

Status: locked after review round 5

## Argument

**Question.** Each backend server answers in about 10 ms, but one request in a hundred hits a hiccup and takes a full second. A page calls a hundred of these servers at once and waits for all of them. How often is the page slow?

**Answer.** 63% of the time. A page is fast only if all 100 calls are fast, and 0.99 multiplied by itself 100 times is 0.37. With fan-out, the servers' rare slow case (their 99th percentile) becomes the page's usual case, and the servers' average hides it. The causes of hiccups are many and brief, so large systems tolerate them instead of eliminating them: a hedged request sends a second copy after the 95th-percentile wait, which rescues almost all slow calls for about 5% more requests.

**Takeaway.** When a request fans out, its latency is set by the backends' tail, not their average. Watch the 99th percentile, and design the fan-out to tolerate slow calls.

**Wrong model.** If only 1% of requests are slow, only about 1% of users notice; the average describes what users experience.

**Objectives.**
1. Compute how often a request that fans out to N servers hits at least one slow call, and say what that calculation assumes.
2. Explain why a dashboard of server averages can look healthy while most pages are slow, and what percentile to watch instead.
3. Explain how a hedged request works, why it waits until the 95th percentile, and what it costs.

## Chain

1. The question: 1 slow call in 100; a page makes 100 calls and waits for all. How often is the page slow?
2. Therefore multiply: all 100 fast has probability 0.99¹⁰⁰ ≈ 37%, so 63% of pages are slow.
3. But the servers' average (about 20 ms) looks healthy. Therefore watch percentiles: the page feels the backends' 99th percentile, and more so the more servers it calls.
4. But why not fix the slow 1%? Because hiccups have many brief causes that can't all be removed. Therefore tolerate them.
5. Therefore hedged requests: a second copy after the 95th-percentile wait rescues slow calls for about 5% more load; Google measured the same effect. But hedging too early doubles the load, and busier servers are slower.
6. Therefore the answer: the page was slow because it waited on a hundred servers; watch the tail, and tolerate it.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1-3 | Narrated animation | The fan-out and the multiplication are best seen: a grid of calls with slow ones lighting up, pages turning slow. |
| 4 | Narrated animation | A short list of causes; one picture per cause. |
| 5 | Narrated animation | A request timeline with the hedge firing; a timing diagram. |
| 6 | Narrated animation | Payoff. |
| (not built) | Interactive | Sliders for the number of calls and the slow fraction, recomputing the slow-page rate live. Offered, not added: the learner wants only the video on the page. |

## Ledgers

**Setups and payoffs.**
- "One in a hundred" and "a hundred servers" (ch. 1) → 63% (ch. 2) → answered (ch. 6).
- The healthy-looking average (ch. 3) pays off the wrong model; the 99th percentile (ch. 3) is what the answer tells you to watch (ch. 6).
- The 95th percentile (ch. 5) is defined with the 99th (ch. 3).
- "Busier servers are slower" (ch. 5) calls back to the previous lesson (queueing); it is stated so that it stands on its own.
- The write caveat (ch. 5) sets up the next lesson (idempotency).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| backend server | ch. 1 | one of the servers a page calls |
| fan out | ch. 2 | one request calling many servers in parallel and waiting for all |
| percentile (99th, 95th) | ch. 3 | the time that 99% (95%) of requests finish within |
| tail | ch. 3 | the slowest few percent of requests |
| hiccup | ch. 1 | a brief stall that makes one call slow |
| hedged request | ch. 5 | a second copy of a call, sent to another server holding the same data if the first hasn't answered by the 95th-percentile time |

**Numbers to remember.** 1 in 100 slow; 100 calls → 63% of pages slow; hedge at the 95th percentile for about 5% more requests.

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

## Review log

**Round 1:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking: "tail" was attributed to the fan-out effect; the term names the long tail of one server's latency distribution. Chapter 3 now says so, and derives why the page feels the 99th percentile.
- Expert: hedging silently assumed uncorrelated hiccups; chapter 5 now says the copy goes to a different machine so the same hiccup is unlikely to reach both. "The standard technique" → "one standard technique". The load cost is now "at most five percent", which holds by construction of the 95th-percentile threshold. Slow-page fractions shown consistently (1%, 9.6%, 39.5%, 63.4%). Reads versus writes noted, which sets up the next lesson.
- Student: why multiply was never explained (chapter 2 now states independence in plain words: one server stalling doesn't make another more likely to); the 20 ms average was asserted (now derived); "about one" (now "about one percent"); the Google sentence carried five numbers (now split, with trigger, result and cost labelled on screen); "busier servers are slower" (now tied to longer queues).
- Checked against the web research pass (research/canonical_web_agent.md, quoting the paper): the 10 ms / 1 s / 63% example, the BigTable benchmark (1,000 keys on 100 servers, hedge after 10 ms, 99.9th percentile 1,800 → 74 ms, +2% requests) and "limits the additional load to approximately 5%" for deferral to the 95th percentile. The same pass flagged that 63% is "most", not "almost all", pages: chapter 3 now says "most pages".

**Round 2:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking: the answer called a 63% event "almost certain"; now "more likely than not".
- Expert: "Google measured the same effect" tied the paper's benchmark to our simulation; now "Google measured hedging on a real system". The load cost follows the paper's wording, "about five percent" (round 1's "at most" overstated the precision). A correlation caveat now closes chapter 6. Google's real fan-out measurement (Table 1: 10 ms → 140 ms at the 99th percentile) now backs the amplification in chapter 3, so the core claim has real data, not only the hypothetical. "Bigtable" spelled as Google spells it.
- Student: the 99.9th percentile arrived undefined; now defined where it's used.
- Not taken: "straggler" as an alternative term (not needed to follow the lesson); one-decimal values on the chapter 3 chart stay (all four are shown at the same precision; the narration says 63%).

**Round 3:** editor PASS, expert REVISE, student retold the answer correctly.
- Expert, blocking: Google's real fan-out measurement reused "10 ms" as a 99th percentile, thirty seconds after 10 ms meant the typical call; it is now introduced as a different, faster service, labelled on screen.
- Expert: "the typical page is as slow as the 99th percentile" holds because N (100) ≈ 1/p (100); now tied to a hundred calls, with more calls pointing to a rarer percentile. The 99.9th percentile is defined without reusing "a thousand". The independence image is now weighted coin flips. "Can't make them go away" softened to "can't make them all go away".
- Not changed: the forward reference to the next lesson (idempotency), which exists in this series.

**Round 4:** expert PASS, editor PASS, student retold the question and answer correctly. The gate is passed; the should-fix items are applied once, and round 5 decides the lock.
- Editor: two Google citations competed, and Table 1 (added in round 2 as the expert's optional suggestion) drew findings in rounds 3 and 4 (a clash with the running example's 10 ms, an unknown fan-out size, a missing middle row). Cut; the Bigtable benchmark carries the real-data evidence.
- Expert: the converse now ends chapter 3 in its place (a page slow 1 time in 100 needs each server slow 1 time in 10,000), which makes chapter 4's "why not fix the slow calls?" quantitative.
- Editor: the independence sentence is split for listening; "stall" is replaced by "hiccup" throughout the narration; "tail latency" is paid off in the answer; the Google benchmark now says it hedged after "a fixed" ten milliseconds, so it isn't read as the 95th-percentile rule.
- Not taken: the editor's nit on chapter 4 labels.

**Round 5 (final):** expert PASS, editor PASS, student retold the question and answer correctly. Locked; remaining should-fix notes stay in research/reviews/round05_*.md as revision candidates for the learner's feedback round.
