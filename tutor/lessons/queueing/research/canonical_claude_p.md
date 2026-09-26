# Queueing in Services — Canonical Treatment

## 1. Canonical worked example

Two competing standard examples exist:

- **Single-server queue as a web/app server or DB connection** — this is the CS/software-engineering-canonical version. **Mor Harchol-Balter, *Performance Modeling and Design of Computer Systems: Queueing Theory in Action* (Cambridge, 2013), Ch. 1–4**, frames the entire book around a server processing jobs and derives the M/M/1 response-time curve as the opening result. This is the version cited/reused in most modern software-engineering talks and blog posts about "why response time explodes near saturation."
- **Bank teller / supermarket checkout line** — the classic intro-probability/operations-research example (used in **Arnold O. Allen, *Probability, Statistics, and Queueing Theory with Computer Science Applications*, 2nd ed. (1990), Ch. 1–7**, and in operations management texts like **Hopp & Spearman, *Factory Physics*, Ch. 8**). It's the more common example for building raw intuition before any formulas.
- Historically first (and still canonical in telecom/OR): **Erlang's telephone trunk-line problem (A.K. Erlang, 1917)**, origin of queueing theory and the Erlang-C staffing formula, still the standard example in call-center capacity planning.

**Most common today for a software audience: the single-server M/M/1 model of a server**, with the checkout-line as the plain-language analogy used to introduce it.

## 2. Standard progression

1. **Intuition first**: informal — "if a checkout line is busy, new customers wait; the closer to 100% busy, the longer the wait, and it's not linear." (Used before any math in nearly every source, including Harchol-Balter Ch.1 and Neil Gunther's talks.)
2. **Little's Law** (L = λW) — introduced as the one assumption-free relationship that holds regardless of arrival/service distributions (Little, 1961). Almost always taught immediately after the intuition, before any distributional assumptions.
3. **Utilization law**: ρ = λ/μ = λS, defining "how busy."
4. **Simplified/deterministic case** shown first as a foil: if service time were constant and arrivals perfectly spaced, there'd be no queueing at all below ρ=1 — used to show that *variability*, not utilization alone, causes queueing (this contrast appears explicitly in Harchol-Balter Ch.1 and in Cary Millsap's talks).
5. **M/M/1 queue** — the canonical first full model (Poisson arrivals, exponential service, one server), with derivation via birth-death Markov chain (Kleinrock, *Queueing Systems Vol. 1*, 1975, Ch. 2; Harchol-Balter Ch. 3–4).
6. **Response-time-vs-utilization curve** ("hockey stick") as the payoff visual.
7. Only afterward, if time allows: general G/G/1 and Kingman's heavy-traffic approximation, multi-server M/M/c / Erlang-C, and networks of queues (Jackson's theorem).

## 3. Model and notation

- **Kendall notation** A/S/c/K/N/D (Kendall, 1953) describes a queue by arrival process / service process / #servers / capacity / population / discipline. M/M/1 = Markovian (Poisson) arrivals, Markovian (exponential) service, 1 server, infinite capacity, FCFS.
- Parameters: **λ** = arrival rate, **μ** = service rate, **S = 1/μ** = mean service time, **ρ = λ/μ** = utilization (traffic intensity).
- Measured quantities: **L** = mean number in system, **Lq** = mean number waiting, **W** = mean sojourn/response time (wait + service), **Wq** = mean wait time.
- Terminology differences across fields:
  - Telecom/OR: traffic intensity measured in **Erlangs**; "offered load" vs "carried load."
  - CS systems performance (Gunther, Gregg): **N** = concurrency, **X** = throughput, **R** = response time, used in the Universal Scalability Law and in Brendan Gregg's *Systems Performance* (2013/2020), Ch. 2 ("Methodology")/Ch. 6.
  - "Response time" (CS) = "sojourn time" (queueing theory) = wait + service time; often confused with "service time" alone.

## 4. Key results, formulas, assumptions, limits

- **Little's Law**: L = λW (Little, 1961, *Operations Research* 9(3)). Holds for **any** stable queueing system in steady state — no distributional assumptions needed. Breaks only if the system isn't stationary/stable (λ ≥ service capacity, unbounded growth).
- **M/M/1 results** (Kleinrock 1975 Ch.2; Harchol-Balter Ch.3):
  - Stability requires ρ < 1.
  - P(n in system) = (1−ρ)ρⁿ
  - L = ρ/(1−ρ)
  - **W = S/(1−ρ)** ← the central "hockey stick" formula
  - Wq = ρS/(1−ρ)
  - Assumptions: Poisson arrivals, exponential (memoryless) service, single server, infinite queue, FCFS. Stops holding when service times aren't exponential, arrivals aren't Poisson (real traffic is bursty/self-similar — Leland et al., "On the Self-Similar Nature of Ethernet Traffic," *IEEE/ACM ToN*, 1994), there are multiple servers, or the queue is bounded (timeouts/rejections instead of unbounded wait).
- **Kingman's formula** (Kingman, "The single server queue in heavy traffic," *Math. Proc. Cambridge Phil. Soc.*, 1961) generalizes to G/G/1:
  Wq ≈ ((Ca² + Cs²)/2) · (ρ/(1−ρ)) · S
  where Ca², Cs² are squared coefficients of variation of interarrival/service times. Shows variability (not just ρ) drives delay; it's a heavy-traffic (ρ→1) approximation, not exact.
- **PASTA** — Poisson Arrivals See Time Averages (Wolff, 1982) — justifies why an arriving job's view of the system equals the time-average view, used to derive M/M/1 results cleanly.
- **Erlang-C** (M/M/c) — multi-server waiting-probability formula, canonical in call-center staffing (Erlang, 1917; standard modern reference: Gross, Shortle, Thompson & Harris, *Fundamentals of Queueing Theory*, 5th ed., 2018, Ch. 2).
- **Universal Scalability Law** (Gunther, *Guerrilla Capacity Planning*, 2007) extends beyond queueing delay to include contention and coherency-delay terms, explaining why real systems degrade even worse than pure M/M/1 predicts at scale.

## 5. Standard numeric examples

Harchol-Balter's canonical illustration (Ch. 1, normalizing S=1) tabulates W = 1/(1−ρ):
ρ=0.5 → W=2S; ρ=0.8 → 5S; ρ=0.9 → 10S; ρ=0.95 → 20S; ρ=0.99 → 100S.
*(Exact numbers as commonly reproduced in course slides derived from this book; I'm confident in the formula, moderately confident these exact figures are Harchol-Balter's own table rather than a common derivative of it.)*
Kleinrock (1975) uses telephone-trunk numeric examples (e.g., trunk groups sized at ρ≈0.7–0.8) to show acceptable blocking probabilities — a parallel canonical numeric tradition from the telecom side.

## 6. Misconceptions and how the canonical treatment corrects them

- **"Response time scales roughly linearly with load."** Corrected by the explicit 1/(1−ρ) curve — nearly flat until ~70–80% utilization, then diverges.
- **"A system running at, say, 90% CPU is basically fine if it was fine at 50%."** Corrected by showing W(0.9) is 5× W(0.5), not 1.8×.
- **"Average response time tells the whole story."** Corrected by pointing at tail latency; Dean & Barroso, "The Tail at Scale," *CACM* 56(2), 2013, shows how queueing plus component variability amplifies p99/p99.9 far more than the mean.
- **"Poisson/exponential is realistic for internet traffic."** Corrected by Leland et al. (1994) on self-similar, bursty real traffic — real queueing is often worse than M/M/1 predicts.
- **"Adding one more server/thread linearly helps."** Corrected by USL's contention/coherency terms (Gunther, 2007).
- Confusing **service time** (S) with **response time** (W = wait + S) — a very common practitioner error the model explicitly separates.

## 7. For a short lesson: essential vs. extra vs. omit

- **Essential**: utilization ρ=λ/μ; Little's Law as the one universal relationship; the M/M/1 response-time formula W=S/(1−ρ) and its hockey-stick shape; the intuition that *variability*, not just average load, causes the divergence.
- **Common extra** (include only if time permits): PASTA, Erlang-C, Kingman's G/G/1 approximation.
- **Leave out**: Markov-chain derivation details, M/M/c and network-of-queues (Jackson network) math, self-similarity/heavy-tail statistics, full USL derivation.

## 8. Real systems canonically cited

- **Connection/thread pool sizing** via Little's Law — e.g. HikariCP's pool-sizing documentation explicitly cites L=λW.
- **Bufferbloat** — Gettys & Nichols, "Bufferbloat: Dark Buffers in the Internet," *ACM Queue*, 2011: oversized network buffers add queueing delay invisible to naive utilization monitoring.
- **Google's tail-latency mitigation** — Dean & Barroso (2013): hedged/tied requests specifically to counter queueing-induced tail blowup in fan-out services.
- **Call-center staffing** — Erlang-C formula, still the industry-standard tool (telecom operations, Gross et al. 2018).
- **Capacity planning at scale** — Gunther's USL used by companies for headroom planning (Gunther, 2007).
- **SRE overload handling** — Google SRE book (Beyer et al., *Site Reliability Engineering*, O'Reilly 2016), chapter on "Handling Overload," discusses load shedding as systems approach saturation — directly motivated by this queueing behavior. *(Uncertain of exact chapter number without checking; content is correct.)*

## 9. Commonly overstated or subtly wrong claims

- "Queueing theory formulas (M/M/1) predict your production server's latency accurately" — overstated; real service-time and arrival distributions violate the memoryless assumption, often substantially (heavy tails from GC pauses, lock contention, etc.).
- "Little's Law requires Poisson/exponential assumptions" — wrong; it's distribution-free, this is exactly why it's used so widely as a sanity-check tool.
- "As long as ρ<1 you're safe" — technically true for stability, but ignores that variance and tail latency can be operationally unacceptable well before ρ approaches 1.
- "Queueing delay is a network/hardware problem, not a software design problem" — subtly wrong; scheduling discipline, batching, and thread-pool sizing are all queueing-design decisions.

## 10. Best learning modality per part

- **Narrated animation**: the response-time-vs-utilization "hockey stick" curve and the intuition for *why* variability (not just mean load) causes queueing — visual, dynamic, hard to get from static text (this is the single most animation-friendly idea in the whole topic).
- **Interactive simulation / running code**: building a small M/M/1 simulator and sweeping ρ from 0.1→0.99 to watch mean/p99 wait times diverge — this cements the nonlinearity experientially and lets the learner see variance effects Kingman's formula only gestures at.
- **Reading**: the formal derivations (birth-death Markov chain for M/M/1, Little's Law proof, Kingman's approximation) — precise, notation-heavy content better absorbed at reading pace, e.g. Harchol-Balter Ch. 3–4 or Kleinrock Ch. 2.
