## 1. Points where I'd be confused or lose the thread

- **"Add an eighth more traffic"** — I had to stop and convert "an eighth" to 12.5% in my head before the on-screen label caught up. A stumble, even if brief.
- **"where do the other forty milliseconds come from"** (end of Section 1) — This lands right after the *90%-busy / 100ms* example, so I expected "forty" to relate to 100. It doesn't (100 − 10 = 90, not 40). It's actually foreshadowing the *80%-busy / 50ms* case from two sentences earlier. Two numbers were just thrown at me (50 and 100) and "forty" doesn't cleanly map to either — I noticed the mismatch and it nagged at me until Section 2 quietly resolved it.
- **"fills ninety percent of the gap... so a new one arrives about every eleven milliseconds"** — I had to do 10/0.9 ≈ 11.1 myself; it's not shown as a calculation, just stated as a conclusion.
- **"work times that vary just as randomly: mostly short, sometimes several times longer"** then later caption **"exponential work times"** — the word "exponential" is dropped in as a label but never actually explained. I know the everyday word, not what makes a distribution "exponential" or why it matters for the formula.
- **"queueing theory gives the exact average response time"** — named but not explained; I just have to trust it.
- **Section 6: "doubled the time requests spend waiting for it"** — but waiting went from 40ms to 90ms, which is more than double (2.25x). Only the *total response time* (50→100) doubled exactly. This felt like a small sleight of hand — did I mishear something, or is the line just loose?
- **"the M/M/1 queue"** / **"M/M/c"** on the end card — unexplained jargon, though it's an end-card credit, not narrated, so lower stakes.

## 2. Questions I'd ask afterward

- Why does "exponential" work-time variability specifically matter — would the formula look different if work times were more uniform?
- What does "arrive independently at random" (Poisson) actually mean mathematically, beyond "sometimes clumps happen"?
- Where does T = S/(1−ρ) come from — is there an intuitive derivation, or do I just have to accept it?
- How does this change with multiple servers sharing a queue (M/M/c) — is it a completely different formula or just a shifted curve?
- How far off is my real, non-Poisson/non-exponential traffic likely to be from this curve in practice?
- Waiting time went from 40 to 90ms (not doubling) while total response time went from 50 to 100 (exactly doubling) — which one should I actually care about when capacity planning?

## 3. What I learned (written without looking back, ~150 words)

A server doing 10ms of work per request gets much slower as it gets busier — not because the work changes, but because requests start queueing. At 80% utilization average response time is 50ms; at 90% it's 100ms, even though traffic only rose a little. The extra time is all waiting, not work. Queues build up because real traffic is random — requests clump together, and some need more work than others — and the server can only clear the backlog using its leftover "spare capacity" (the fraction of time it isn't busy). As utilization climbs, spare capacity shrinks fast (20% → 10% → 5%), and queues take proportionally longer to drain, so response time rises steeply, not gently. There's a formula, response time = work time ÷ spare capacity, that predicts this exactly for the simplest case. The takeaway: always leave headroom, and never run a server at 100% utilization, or the queue never clears.

## 4. Direct answers

- **One main idea:** Response time blows up as utilization approaches 100% because shrinking spare capacity takes exponentially longer to clear the queues that random traffic creates — it's a waiting-time problem, not a working-time problem.
- **Numbers I remember:** 10ms work per request; 80% busy → 50ms response; 90% busy → 100ms response (traffic up only ~12.5%, response time doubled); spare capacity 20% → 10% → 5% going from 80% → 90% → 95% busy, with response time 50 → 100 → 200ms.
- **Question it started with / answer:** Why does a small traffic increase (80%→90% busy) double response time, and where do the extra 40ms come from if work is only 10ms? Answer: the extra time is queueing/waiting time, driven by shrinking spare capacity, formalized as response time = work time ÷ (1 − utilization).

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — the "traffic up 12.5%, response time doubles" hook is genuinely surprising and made me want the explanation.
- **How often I felt lost:** A few times — mainly the "forty milliseconds" referent mismatch at the very start, the unexplained "exponential" label, and the doubling-vs-90ms wrinkle in Section 6.
