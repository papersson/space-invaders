You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** A server does 10 ms of work per request. At 80% busy, requests take 50 ms from arrival to reply; at 90% busy, 100 ms. An eighth more traffic doubled the response time. Why, and where do the other 40 ms come from?

**Answer.** The extra time is waiting in a queue. Queues form because requests arrive at random and need varying amounts of work; only the server's spare time clears them. Going from 80% to 90% busy halves the spare time, from 20% to 10%, so queues take twice as long to clear and the response time doubles. For random arrivals and random work on one server, response time = work time ÷ (1 − utilization).

**Takeaway.** Response time is set by spare capacity, not by load: halve the spare capacity and you double the response time. Leave headroom, and choose it from the latency you can afford.

**Wrong model.** Latency grows in proportion to load, so 90% busy is only a little worse than 80%.

**Objectives.**
1. Explain why requests wait even when the server is not fully busy.
2. Explain why going from 80% to 90% busy doubles the response time.
3. Use response time = work ÷ (1 − utilization) to predict response time at a given load, and say what it assumes.
4. Choose a utilization limit from a latency budget, and say why burstier traffic needs more headroom.


## Chain

1. The question: 10 ms of work takes 50 ms at 80% busy and 100 ms at 90%.
2. But the work doesn't change with load, so the rest is waiting. Therefore the question is about queues.
3. But evenly spaced requests with fixed work never wait, even at 90%. Therefore queues come from variability, and something else decides how long they last.
4. Therefore look at what clears a queue: spare time. At 90% there is half as much as at 80%, so the same queue lasts twice as long.
5. Therefore the whole curve: response time = work ÷ spare capacity, flat and then steep; a simulation lands on it; burstier traffic makes it worse.
6. Therefore the answer and the practice: the step from 80% to 90% halved the spare capacity; choose headroom from the latency budget.

Deviation from the canonical progression: Little's Law usually comes right after the intuition. It answers a different question (how many requests are in flight, and so how many threads or connections a service needs) and this lesson doesn't need it, so it is left for another lesson.


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

