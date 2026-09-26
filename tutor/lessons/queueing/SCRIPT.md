# Why busy servers get slow

Status: locked after review round 6

## Argument

**Question.** A server does 10 ms of work per request. At 80% busy, requests take 50 ms from arrival to reply; at 90% busy, 100 ms. An eighth more traffic doubled the response time. Why, and where do the other 40 ms come from?

**Answer.** The extra time is waiting in a queue. Queues form because requests arrive at random and need varying amounts of work; only the server's spare time clears them. Going from 80% to 90% busy halves the spare time, from 20% to 10%, so queues take twice as long to clear and the response time doubles. For one server with Poisson arrivals and exponential work times, response time = work time ÷ (1 − utilization).

**Takeaway.** Response time is set by spare capacity, not by load: halve the spare capacity and you double the response time. Leave headroom, and choose it from the latency you can afford.

**Wrong model.** Latency grows in proportion to load, so 90% busy is only a little worse than 80%.

**Objectives.**
1. Explain why requests wait even when the server is not fully busy.
2. Explain why going from 80% to 90% busy doubles the response time.
3. Use response time = work ÷ (1 − utilization) to predict response time at a given load, and say what it assumes.
4. Choose a utilization limit from a latency budget, and explain why burstier traffic needs more headroom.

## Chain

1. The question: 10 ms of work takes 50 ms at 80% busy and 100 ms at 90%.
2. But the work doesn't change with load, so the rest is waiting. Therefore the question is about queues.
3. But evenly spaced requests with fixed work never wait, even at 90%. Therefore queues come from variability, and something else decides how long they last.
4. Therefore look at what clears a queue: spare time. At 90% there is half as much as at 80%, so the same queue lasts twice as long.
5. Therefore the whole curve: response time = work ÷ spare capacity, flat and then steep; a simulation lands on it.
6. Therefore the answer and the practice: the other 40 ms is waiting, doubled because spare capacity halved; burstier traffic needs more spare capacity; choose headroom from the latency budget.

Deviation from the canonical progression: Little's Law usually comes right after the intuition. It answers a different question (how many requests are in flight, and so how many threads or connections a service needs) and this lesson doesn't need it, so it is left for another lesson.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1-4 | Narrated animation | Timing and queues building and draining are processes over time; animation shows them directly. |
| 5 | Narrated animation | The curve and simulated points are a chart that builds up. |
| 6 | Narrated animation | Short payoff; the curve from chapter 5 is reused. |
| (not built) | Interactive simulator | A utilization slider with a live queue would let the learner feel the nonlinearity. The learner asked for only the video on the page, so this is offered, not added. |

## Ledgers

**Setups and payoffs.**
- The 50 ms and 100 ms (ch. 1) are split into work and waiting (ch. 2), explained by spare capacity (ch. 4), land on the curve (ch. 5), and are answered (ch. 6).
- The evenly spaced foil (ch. 3) pays off in ch. 5: variability is what the formula's assumptions describe, and more of it makes the curve worse.
- "Spare capacity" (ch. 4) is the denominator of the formula (ch. 5) and the answer (ch. 6).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| work time | ch. 1 | time the server spends processing one request: 10 ms on average (queueing texts: service time) |
| response time | ch. 1 | time from a request's arrival to its reply: waiting + work |
| busy / utilization | ch. 1 | fraction of time the server is working; said "80% busy", written "utilization" in the formula |
| queue | ch. 2 | requests that have arrived and wait for the server |
| spare capacity | ch. 4 | the fraction of time the server is not needed: 1 − utilization |

**Numbers to remember.** 80% → 50 ms, 90% → 100 ms (10 ms of work); spare capacity 20% vs 10%.

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a server that does ten milliseconds of work per request, on average.
> Send it eighty requests a second, and it's working eighty percent of the time: it's eighty percent busy. A request then takes fifty milliseconds on average, from arrival to reply.
> Send it ninety requests a second, an eighth more traffic, and it's ninety percent busy. Requests now take a hundred milliseconds.
> You might expect a little more traffic to mean a little more delay. Instead, the response time doubled.
> Why? And even at eighty percent, where do forty of those fifty milliseconds come from, when the work only takes ten?

*Screen:* a server box with requests (dots) arriving and leaving; "work: 10 ms per request, on average". A panel: "80 requests/s × 10 ms = 80% busy → 50 ms", then "90 requests/s → 90% busy → 100 ms" with "+12.5% traffic" under the first arrow and "2× response time" under the second. A small "simulated server" label. Title: "Why Busy Servers Get Slow".

### 2. Waiting, not working

> A request's response time has two parts: the time the server spends working on it, and the time it spends waiting for the server to be free.
> The work takes ten milliseconds on average, however busy the server is.
> So at eighty percent busy, a request waits forty milliseconds in a queue, four times the average work. At ninety percent, it waits ninety.
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

> A queue shrinks only when the server finishes work faster than new work arrives.
> At eighty percent busy, new work keeps arriving at eighty percent of what the server can do. So while there's a queue, only the other twenty percent of its effort actually shrinks it. Call that twenty percent the spare capacity: it's what clears the queue.
> At ninety percent busy, the spare capacity is only ten percent. On average, the same queue takes about twice as long to clear, and more requests pile on while that happens. That's the intuition; the exact answer comes next.
> Here's the same random stream of requests at both loads. At ninety percent, the queue builds higher and lasts longer.

*Screen:* a bar of what the server can do, split into "new work arriving 80%" and "spare capacity 20%: shrinks the queue", then "90% / 10%". Then two panels, requests in the system over time, the same random draws at 80% and 90% busy (400 requests, simulated): the 90% panel's queue is higher and longer-lived.

### 5. The curve

> The fraction of time a server is busy is called its utilization.
> For the simplest case, queueing theory gives the exact average response time. The case is one server, requests arriving at random, each unrelated to the others, and work times that vary just as randomly: mostly short, sometimes several times longer.
> The answer is the work time divided by the spare capacity: ten milliseconds divided by one minus the utilization.
> At fifty percent busy, that's twenty milliseconds. At eighty, fifty. At ninety, a hundred. At ninety-five, two hundred.
> A simulation of twenty million requests at each load lands on the curve.
> It's almost flat at first, then steep. From eighty to ninety percent, the spare capacity halves, and the response time doubles. From ninety to ninety-five, it halves and doubles again.

*Screen:* axes: utilization (0-100%) and average response time (ms). The curve drawn left to right, labelled "response time = work time ÷ spare capacity" and, smaller, "T = S / (1 − ρ)" with "S: work time, ρ: utilization"; points at 50/80/90/95% with their values; simulated points (dots) on the curve. Caption: "one server; Poisson arrivals (independent, at random); exponential work times (mostly short, some several times longer)". Then the 80 → 90 → 95 steps highlighted with "spare 20% → 10% → 5%" and "50 → 100 → 200 ms".

### 6. The answer

> So that's where the forty milliseconds went: not into work, but into waiting. A little more traffic halved the spare capacity, from twenty percent to ten, and the response time doubled with it, from fifty milliseconds to a hundred.
> Burstier traffic, or more variable work, makes this worse. Bigger clumps of requests, or a few very long ones, build bigger queues, and the same spare capacity takes longer to clear them. So they need more spare capacity for the same response time.
> That's why capacity plans leave headroom. Decide how slow requests may get, and read a first estimate of the load limit off the curve. On this curve, if a request may take five times its work time on average, keep the server at or below eighty percent busy. Real systems, with burstier traffic and more than one busy resource, usually need more headroom than this curve says.
> These are averages, and some requests take several times longer. The slowest requests are the next lesson.
> And never plan to run a server at a hundred percent busy. With no spare capacity, nothing clears the queue, and it keeps growing.

*Screen:* the curve again; 80% and 90% marked with spare 20% and 10% bars under the axis; the waiting part of the 50 ms and 100 ms bars from chapter 2. A second curve above it, dashed: burstier arrivals (interarrival times three times as variable as Poisson), simulated points with Kingman's approximation drawn through them. "5× work time → at most 80% busy" read off the curve with guide lines. End card: T = S / (1 − ρ): mean response time for one server with Poisson arrivals and exponential work times (the M/M/1 queue; derived in Harchol-Balter ch. 13); "many servers sharing one queue stay flat for longer, then eventually turn up much the same way (M/M/c)"; references: Harchol-Balter, Performance Modeling and Design of Computer Systems: Queueing Theory in Action (2013); Kleinrock, Queueing Systems, Volume I: Theory (1975).

## Evidence

| Claim | Source |
|---|---|
| M/M/1 mean response time T = S/(1 − ρ) (Kleinrock's T, Harchol-Balter's E[T]; Kleinrock's W is the waiting part only); stable only for ρ < 1 | Kleinrock, Queueing Systems Vol. 1 (1975), ch. 3; Harchol-Balter, Performance Modeling and Design of Computer Systems (2013) |
| 20 / 50 / 100 / 200 ms at 50 / 80 / 90 / 95% with S = 10 ms | Arithmetic from the formula; simulation (sim.py, 20 million requests per load): 20.0 / 50.0 / 100.5 / 199.1 ms |
| 80 → 90 requests/s is an eighth more traffic (+12.5%); utilization = arrival rate × average work time | 90 / 80 = 1.125; utilization law U = X·S (Lazowska et al., Quantitative System Performance, 1984, §3.2) |
| Evenly spaced arrivals with fixed 10 ms work never wait below 100% busy | Arithmetic: at 90% a request arrives every 11.1 ms; sim.py D/D/1 gives 10.0 ms at every load below 100% |
| Variability, not utilization alone, causes queueing; burstier arrivals or more variable work make it worse (bigger queues at the same utilization) | Kingman (1961) heavy-traffic approximation for G/G/1: Wq ≈ ((Ca² + Cs²)/2) · ρ/(1 − ρ) · S; Harchol-Balter (2013) |
| End card: many servers sharing one queue stay flat for longer, then turn up | M/M/c (Erlang C); sim.py with 8 servers (20 million requests per load): 10.1 / 12.9 / 18.8 / 31.1 ms at 50 / 80 / 90 / 95% |
| At or below 80% busy keeps the average response time within 5× the work time | 1/(1 − 0.8) = 5 |
| Burstier arrivals raise the curve: interarrival times 3× as variable (squared coefficient of variation 3) give 28 / 88 / 191 ms at 50 / 80 / 90% busy, close to Kingman's 30 / 90 / 190 ms | sim_bursty.py (5 million requests per load, two-phase hyperexponential arrivals); Kingman (1961) |
| At 100% busy the queue keeps growing | M/M/1 is unstable for ρ ≥ 1 (Kleinrock 1975) |
| These are averages; some requests take several times longer | M/M/1 response time is exponentially distributed with mean S/(1 − ρ), so its p99 is ln(100) × the mean ≈ 4.6 × the mean (Harchol-Balter 2013) |

## Review log

**Round 1:** expert REVISE, editor REVISE, student retold the answer correctly (felt lost "a few times").
- Expert, blocking: "W" names the waiting-only time in Kleinrock, the cited source; the formula is now T = S/(1 − ρ), matching Kleinrock's T and Harchol-Balter's E[T].
- Editor, blocking: objective 4 (why burstier traffic needs more headroom) was asserted, not explained. Chapter 6 now derives it from the spare-capacity mechanism of chapter 4.
- Expert: the narration said "a random amount of work" while the formula needs exponential work times. Chapter 5 now describes the case in words (arriving independently at random; work times that vary just as randomly, mostly short, sometimes several times longer) with the technical names on screen.
- Expert: capacity planning by the average alone overstates the rule. Chapter 6 now says these are averages and some requests take several times longer, and points to the next lesson (tail latency).
- Expert: the 8-server 95% point was under-sampled; sim.py now runs 20 million requests per load and gives 31.1 ms, matching Erlang C.
- Editor and student: "busy" and "utilization" never linked (now defined in chapter 5); the wrong intuition was implied, not stated (now stated in chapter 1); the ending didn't return to "the other forty milliseconds" (it does now); "spare time" and "spare capacity" both used (now only "spare capacity"); the 11 ms gap appeared without derivation (now derived); the two kinds of variability shared one sentence (now two); the "bigger share of what's left" sentence was abstract (replaced by 80 → 90 → 95 halving and doubling).
- Editor: the many-servers sentence was an unexplained aside tied to no objective. It moves to the end card as reference; declined deleting it outright because the audience runs multi-worker services and would otherwise over-apply the one-server numbers.
- Editor, nit: the chapter 1 panel echoes the narration. Kept: those two numbers are the ones to remember.

**Round 2:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking: the ending said the waiting time doubled, but chapter 2 shows 40 → 90 ms (2.25×); it is the response time that doubles (50 → 100 ms). Fixed.
- Expert: "below eighty percent" → "at or below" (T = 5S exactly at 80%); "spare capacity" is plain language, not a term of art, so it is now introduced as a name for the idle time; the drain argument is now marked as an average ("on average, about twice as long"), with chapter 5 giving the exact result; "four times longer than" → "four times as long as"; Little's Law named on the end card.
- Student: "the other forty milliseconds" came right after the 100 ms case and seemed to refer to it; now "even at eighty percent, where do forty of those fifty milliseconds come from"; "an eighth" cost a mental conversion, now "about twelve percent" (screen: +12.5%); "exponential" is glossed on screen.
- Not taken: explaining Poisson and exponential in narration (the plain description in chapter 5 carries the meaning; the names are on screen for lookup).

**Round 3:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking: "the work takes ten milliseconds" read as a constant, contradicting chapter 3's variable work; now "on average" in chapters 1 and 2, and "four times the average work".
- Expert: "about twelve percent" against "+12.5%" on screen; the traffic is now given as requests per second (80 → 90, an eighth more), which also answers the student's question of why 12.5% more traffic adds 10 points of busy (busy = requests per second × average work). The end card no longer claims the formula follows from Little's Law alone. More variable work now joins burstier traffic in chapter 6 (Kingman's (Ca² + Cs²)/2). The M/M/c note and the queue-shrinking sentence are tightened.
- Student: "independently" read as a technical term; now "each unrelated to the others".
- Not taken: explaining Poisson and exponential in narration (same reason as round 2).

**Round 4:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking, declined: the expert recalled the M/M/1 chapter of Harchol-Balter as ch. 14 and asked for a check. The web research pass read the book's table of contents: ch. 13 is "M/M/1 and PASTA" (§13.1 The M/M/1 Queue), so "ch. 13" stays.
- Expert: "spare capacity clears the queue" read as idle time during a busy period. Chapter 4 now states the net rate (new work keeps arriving at 80% of what the server can do, so only the other 20% of its effort shrinks a queue), which is correct as stated, and marks the doubling as intuition before chapter 5's exact result.
- Expert: "the curve for your traffic" was ambiguous right after the burstier curve; chapter 6 now reads the limit off "this curve" and adds that burstier traffic needs more headroom than it says.
- Not taken: rewording "each unrelated to the others" (the expert marked it optional; the screen says Poisson).

**Round 5:** expert PASS, editor PASS, student retold the question and the answer correctly (spare capacity halves, response time doubles). The gate is passed; the should-fix items are applied once, and round 6 decides the lock.
- Expert: the load limit read off the curve is now "a first estimate", and chapter 6 says real systems (burstier traffic, more than one busy resource) usually need more headroom.
- Expert, declined again: the chapter 13 citation. The research pass read the published table of contents (ch. 13, "M/M/1 and PASTA"); the reviewer has no web access and could not confirm or refute it.

**Round 6 (final):** expert PASS, editor PASS, student retold the question and answer correctly (80 → 90% halves the spare capacity from 20% to 10%, doubling the response time). Locked.
- Editor, should fix, applied on screen only: the burstier curve was hand-drawn next to a simulated one. Production now simulates burstier arrivals (interarrival times three times as variable as Poisson, a two-phase hyperexponential) and draws Kingman's approximation through the simulated points, labelled as such. The narration is unchanged.
- Editor, should fix, not applied: "more than one busy resource" lacks a setup. The expert asked for it in round 5 so that the one-server curve isn't read as a sizing procedure; the two reviewers disagree, and the clause names a limit rather than teaching a new idea.
- Expert, should fix, declined (third time): the chapter 13 citation, verified against the book's table of contents by the research pass.
- Editor, nit: ρ is screen-only already; the narration never says it.
