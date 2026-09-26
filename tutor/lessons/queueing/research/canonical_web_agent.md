# Queueing in services: the canonical treatment (web-verified research notes)

Lesson: *how a server's response time depends on how busy it is, and why a service that looks fine at moderate load degrades badly near full load.*

**How to read this.** An item with a link is one I checked against the linked source: the author's own PDF or page, the publisher's chapter page, or the paper itself. **(uncertain)** marks things I could not verify online, usually because the book is paywalled or the author's server was down. Those come from memory, or I inferred them. Numbers marked **(derived)** are my own arithmetic from the standard formulas; I checked them in Python.

Short names for the sources cited most often:

- **HB**: Harchol-Balter, *Performance Modeling and Design of Computer Systems: Queueing Theory in Action*, Cambridge UP, 2013 ([TOC](https://www.cs.cmu.edu/~harchol/PerformanceModeling/book.html), [Ch. 1 PDF](https://www.cs.cmu.edu/~harchol/PerformanceModeling/chpt1.pdf)).
- **QSP**: Lazowska, Zahorjan, Graham, Sevcik, *Quantitative System Performance*, Prentice-Hall, 1984 ([free online](https://homes.cs.washington.edu/~lazowska/qsp/)).
- **B&G**: Bertsekas & Gallager, *Data Networks*, 2nd ed., 1992, Ch. 3 "Delay Models in Data Networks" ([author PDF](https://web.mit.edu/dimitrib/www/Queueing_Data_Nets.pdf)).
- **Kleinrock**: *Queueing Systems, Vol. 1: Theory*, Wiley, 1975 ([publisher](https://www.wiley.com/en-us/Queueing+Systems,+Volume+I-p-9780471491101)).
- **Jain**: *The Art of Computer Systems Performance Analysis*, Wiley, 1991 ([TOC](https://www.cse.wustl.edu/~jain/books/perf_toc.htm); the server returned 503 to me, so I confirmed chapter titles only through search snippets).
- **HB&S**: Harchol-Balter & Scully, "The most common queueing theory questions asked by computer systems practitioners," *ACM SIGMETRICS PER* 49(4):3–7, 2022 (TeaPACS/IFIP Performance 2021) ([ACM](https://dl.acm.org/doi/abs/10.1145/3543146.3543148), [PDF](https://www.performance2021.deib.polimi.it/www.performance2021.deib.polimi.it/wp-content/uploads/2021/10/p1_Harchol-Balter.pdf)).

---

## 1. The canonical worked example

**The standard example is a single-server queue, usually M/M/1, with a plot of mean response time against utilization.** The server is one CPU, disk, web server or router, or in everyday framing a bank teller or checkout line. Requests arrive at random at rate λ and each needs on average S seconds of service. Utilization is ρ = λS. The plot follows R = S/(1−ρ): it is almost flat at first, then rises steeply as ρ → 1. In practitioner writing this is the "hockey-stick curve."

Where it appears:
- **QSP §1.2.1 "Single Service Centers," Figs. 1.2a/b.** Arrivals at 0.5/s with a service demand of 1.25 s give utilization .625, residence time 3.33 s and queue length 1.67. The text says that "as the service center approaches saturation, small increases in arrival rate result in dramatic increases in residence time" ([Ch. 1](https://homes.cs.washington.edu/~lazowska/qsp/Images/Chap_01.pdf)).
- **B&G §3.3 "The M/M/1 Queueing System," Fig. 3.7**, which plots average number in system against utilization factor ([PDF](https://web.mit.edu/dimitrib/www/Queueing_Data_Nets.pdf)).
- **HB Ch. 1, Design Example 1**: "a single CPU that serves a queue of jobs in FCFS order," with λ = 3 and µ = 5 jobs/s. HB Ch. 13 is "M/M/1 and PASTA" (§13.1 The M/M/1 Queue, §13.2 Examples Using an M/M/1 Queue; [Cambridge](https://www.cambridge.org/core/books/performance-modeling-and-design-of-computer-systems/mm1-and-pasta/6C64155B137E6C72BAC0E6D98338F144)). HB's opening also uses the bank-teller and supermarket framing ([Ch. 1](https://www.cs.cmu.edu/~harchol/PerformanceModeling/chpt1.pdf)).
- **Practitioner sources**:
  - Baron Schwartz calls it "the so-called hockey-stick curve… the most famous queueing theory picture of all time" (*The Essential Guide to Queueing Theory*, VividCortex ebook, [LaTeX source](https://github.com/VividCortex/ebooks/blob/master/queueing-theory.tex); publication year uncertain, c. 2016).
  - Dan Slimmon, "The most important thing to understand about queues" (2016), [blog](https://blog.danslimmon.com/2016/08/26/the-most-important-thing-to-understand-about-queues/).
  - Marc Brooker, "Latency Sneaks Up On You" (2021), [blog](https://brooker.co.za/blog/2021/08/05/utilization.html).
  - Brendan Gregg, *Systems Performance*, §2.6.5 "Queueing Theory." The index entry "M/D/1 mean response time vs. [utilization], 64–65" appears in the [1st-ed. sample](https://ptgmedia.pearsoncmg.com/images/9780133390094/samplepages/0133390098.pdf).

**Why it is the standard:**
- It is the smallest model that has a closed-form answer and still shows the nonlinearity.
- One dimensionless knob, ρ, controls everything, and the headline formula 1/(1−ρ) is easy to remember.
- Every later model is presented as a change to it: M/G/1 adds variability, M/M/k adds servers, and closed systems cap the number of users.

**The competing standard example is pooling: one shared line versus separate lines, or one fast server versus k slow ones.** Sources:
- B&G Ex. 3.9, "Statistical Multiplexing Compared with Time- and Frequency-Division Multiplexing": splitting a link into m sub-channels makes delay "m times larger."
- B&G Ex. 3.10: with m slow channels versus one fast one, the slow version is about m× worse at light load and the ratio is "close to 1" at heavy load.
- HB Ch. 1 Design Example 3, "One Machine or Many?", and Ch. 14 "Server Farms: M/M/k and M/M/k/k" ([Cambridge](https://www.cambridge.org/core/books/abs/performance-modeling-and-design-of-computer-systems/server-farms-mmk-and-mmkk/8E04B51455F14BAADE184D81B5AA2BC3)).
- HB&S §2.3 "Pooling Resources."
- Historically, Erlang's telephone-exchange work (1909, 1917; [MacTutor](https://mathshistory.st-andrews.ac.uk/Biographies/Erlang/)).
- Popular versions: John D. Cook's bank teller ([2008](https://www.johndcook.com/blog/2008/10/21/what-happens-when-you-add-a-new-teller/)), Schwartz's airport security line, and Brooker's "Surprising Economics of Load-Balanced Systems" ([2020](https://brooker.co.za/blog/2020/08/06/erlang.html)).

**Which is more common.** The single-server curve is the usual *opening* example for "latency versus load." Pooling is almost always the *second* example. It explains why many-core or many-worker services can run hotter. This is my judgment from the sources above, not a count.

**A third recurring example is scaling.** Double both the arrival rate and the service rate and mean response time *halves*. This is HB Ch. 1 Design Example 1, which explains it with "Federation time vs Klingon time," and B&G Ex. 3.8, "Increasing the Arrival and Transmission Rates by the Same Factor."

## 2. The standard progression

There are three recognizable orders.

**(a) Computer-systems performance tradition: operational laws first.**
- **QSP**: Ch. 1 shows the single-service-center curve as motivation. Ch. 3 "Fundamental Laws" covers the utilization law, Little's law, the response-time law and the forced-flow law. Ch. 5 "Bounds on Performance" covers asymptotic bounds for closed systems. Ch. 6 solves open and closed models, including R = D/(1−U) (§6.4.1).
- **HB**: Ch. 1 motivating examples → Ch. 2 terminology (open vs closed) → Chs. 3–5 probability → Ch. 6 "Little's Law and Other Operational Laws" → Ch. 7 closed-system what-ifs → Markov chains → Ch. 11 exponential and Poisson → Ch. 13 M/M/1 → Ch. 14 M/M/k → Ch. 15 capacity provisioning / square-root staffing → Part VI variability (heavy tails; Ch. 23 M/G/1 and the inspection paradox) → Part VII scheduling.
- HB's CMU course 15-857 lists topics in the same order, starting with "Operational Laws—Little's Law, response-time law, asymptotic bounds" ([course page](https://csd-web-01.andrew.cmu.edu/course/15857/f25)).

**(b) Classical OR and networking tradition: stochastic models first.**
- **Kleinrock Vol. 1**: queueing systems → important random processes → Ch. 3 "Birth-Death Queueing Systems in Equilibrium" (M/M/1 and its variants) → Ch. 4 Markovian queues → Ch. 5 M/G/1 → G/M/m → G/G/1. Chapter titles are confirmed via catalog listings; section numbers are **(uncertain)**.
- **B&G Ch. 3**: §3.1 multiplexing (motivation) → §3.2 Little's theorem → §3.3 M/M/1 → §3.4 M/M/m, M/M/∞, M/M/m/m → §3.5 M/G/1 (Pollaczek–Khinchine) → networks and Jackson's theorem.
- **Jain**: Ch. 30 "Introduction to Queueing Theory" (Kendall notation, Little's law) → Ch. 31 "Analysis of a Single Queue" → Ch. 32 (queueing networks; exact title **uncertain**) → Ch. 33 "Operational Laws" → Ch. 34 "Mean Value Analysis and Related Techniques." The titles of Chs. 30, 31, 33 and 34 are from search snippets of Jain's TOC page; section contents are **(uncertain)**.

**(c) Practitioner articles and talks: intuition, then the curve, then formulas.**
- Schwartz's ebook runs: why queueing is tricky (nonlinearity, the hockey stick) → why queueing happens (grocery store) → framework and Little's law → Kendall notation → M/M/1 formulas → Erlang C → approximations → "Many Queues or One Combined Queue?" → cost vs QoS → applying it in practice.
- Millsap's "Thinking Clearly About Performance" runs: queueing delay → the knee → relevance of the knee → capacity planning → random arrivals → coherency delay ([slides](https://liudanking.com/wp-content/uploads/2014/04/Thinking-Clearly-about-Performance-Cary-Millsap-PPT.pdf); ACM Queue/CACM 2010, [Queue](https://queue.acm.org/detail.cfm?id=1854041)).

**Simpler-before-full choices common to all three:**
1. **Deterministic before random.**
   - Schwartz: 1 shopper/min and 45 s service means the cashier is busy 75% of the time, "so no one has to wait… right?" In reality people do wait.
   - Millsap: 6 arrivals in 30 s with S = 3 s gives R = 3.000 s for evenly spaced arrivals and R = 4.267 s for random ones. "With deterministic arrivals, you can run up to 100% utilization."
2. **One server before k servers** (M/M/1 → M/M/k).
3. **Exponential service before general service** (M/M/1 → M/G/1 → G/G/1 via Kingman).
4. **Means before distributions and percentiles.**
5. **Open single queue before closed systems and networks.**

## 3. Model, parameters, what is measured, notation

**The model.** An open single-station queue in Kendall notation A/S/c. Kendall 1953 introduced three fields ([Ann. Math. Stat. 24(3):338–354](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-24/issue-3/Stochastic-Processes-Occurring-in-the-Theory-of-Queues-and-their/10.1214/aoms/1177728975.full)). The notation was later extended to A/S/c/K/N/D. Omitted fields default to K = ∞, N = ∞ and FIFO ([Wikipedia](https://en.wikipedia.org/wiki/Kendall%27s_notation); who added K, N and D is **(uncertain)**). M means Markovian (Poisson arrivals or exponential service), D deterministic, G general.

**Parameters.**
- λ, the arrival rate.
- E[S] = 1/µ, the mean service time.
- c, the number of servers.
- ρ = λE[S]/c, utilization or "traffic intensity."
- In telephony, offered load A = λE[S] in *Erlangs*, not divided by c (Schwartz).

**What is measured.** QSP §3.2 gives operational definitions over an observation window of length T:
- arrival rate λ = A/T and throughput X = C/T;
- utilization U = B/T, where B is busy time;
- mean service requirement S = B/C;
- therefore U = XS, the utilization law.

**Response time** is measured from *arrival* until completion: waiting in queue plus service. HB Ch. 1: "the time from when a job arrives until it completes service, a.k.a. sojourn time." Two practical traps:
- Service time is often not directly observable. Schwartz: "I found it impossible to measure service times."
- A load generator that measures from actual send time rather than *intended* send time under-reports queueing ("coordinated omission"; see §6 and §9).

**Notation and terminology that differ between sources** (all verified unless marked):

| Concept | HB (CS) | B&G / Kleinrock (networking) | Little 1961 / OR texts | QSP | Engineering usage |
|---|---|---|---|---|---|
| Time in system | T, "response time a.k.a. sojourn time" | T, "average delay per customer (waiting time in queue plus service time)" (B&G §3.3) | **W**, "mean time spent by a unit in the system" ([Little 1961](https://pubsonline.informs.org/doi/10.1287/opre.9.3.383)) | R, "residence time" / response time | latency, response time |
| Time in queue only | T_Q (from memory, **uncertain**). HB&S call T−S the job's "delay (D)… a.k.a. its queueing time" | **W**, "average waiting time in queue" (B&G). Kleinrock is said to use the same W/T convention **(uncertain)** | W_q (Gross–Harris style; **uncertain**, book not accessible) | (part of R) | wait, queueing delay |
| Number in system | N | N | L | Q, "queue length," which *includes* the job in service | concurrency, in-flight |
| Number waiting | N_Q | N_Q | L_q | – | queue depth |

Collisions to warn viewers about:
- **"W"** means time *in system* in Little's L = λW, but time *in queue* in B&G, and probably Kleinrock.
- **"Delay"** means total time in B&G but queueing time only in HB&S.
- **"Queue length"** includes the job in service in QSP but excludes it in L_q.
- **"Load"** can mean ρ, λ, or N (closed systems).
- **"Latency"** usually means response time, but sometimes only the wait. Gregg's exact definition is **(uncertain)**.
- **Open vs closed.** In an open system arrivals are exogenous. In a closed system a new job arrives only after a completion plus a think time Z, with N users. This distinction changes results qualitatively ([Schroeder, Wierman, Harchol-Balter, NSDI 2006](https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf); HB&S §5).

## 4. Key results, assumptions, and where they stop holding

1. **Utilization law, U = X·S** (QSP §3.2). This is an identity on measured data. QSP calls it a special case of Little's law.

2. **Little's law, L = λW** (or N = XR).
   - Little proved it in 1961 for stationary processes with finite means ([Oper. Res. 9(3):383–387](https://pubsonline.informs.org/doi/10.1287/opre.9.3.383)).
   - Per [Little 2011, *Oper. Res.* 59(3):536–549](https://pubsonline.informs.org/doi/10.1287/opre.1110.0940) ([reprint summary](https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/)), it needs no particular queue discipline or distribution.
   - **Limits:** it relates *averages only*. The distributional forms need restrictive conditions. Over a finite window, end effects matter unless the system is empty at both ends (QSP §3.3). It must be applied with consistent system boundaries.

3. **M/M/1** (Poisson arrivals, exponential service, one FCFS server, infinite buffer, ρ < 1, steady state) (B&G §3.3; HB Ch. 13):
   - P(N = n) = (1−ρ)ρⁿ
   - E[N] = ρ/(1−ρ)
   - **E[T] = 1/(µ−λ) = E[S]/(1−ρ)**
   - E[T_Q] = ρE[S]/(1−ρ)
   - N_Q = ρ²/(1−ρ)
   - The time in system is **exponentially distributed** (B&G §3.3, Problem 3.11b), so the p-th percentile is −ln(1−p)·E[T]. That gives p50 ≈ 0.69·E[T], p90 ≈ 2.3·E[T], p99 ≈ 4.6·E[T] **(derived)**. Schwartz gives the rule-of-thumb versions, e.g. R₉₀ ≈ 7/3·R.

4. **Open queueing network centre** (QSP §6.4.1, Algorithm 6.1): R_k = D_k/(1−U_k), which tends to D_k as U_k → 0 and grows without bound as U_k → 1. Processing capacity is λ_sat = 1/D_max.

5. **M/G/1, the Pollaczek–Khinchine formula** (Pollaczek 1930, *Math. Z.* 32:64–100; Khintchine 1932, *Mat. Sbornik* 39(4):73–84; [overview](https://en.wikipedia.org/wiki/Pollaczek%E2%80%93Khinchine_formula)):
   - E[T_Q] = λE[S²]/(2(1−ρ)) = [ρ/(1−ρ)]·[(1+C_S²)/2]·E[S], where C_S² = Var(S)/E[S]² (B&G §3.5).
   - **M/D/1** (constant service): the queueing wait is exactly half of M/M/1. *Response time* is only halved in the limit ρ → 1 (B&G §3.5).
   - **Limits:** it needs Poisson arrivals, FCFS order and finite E[S²]. With heavy-tailed service, the mean wait blows up with E[S²] (HB Part VI).
   - HB Ch. 23, "The M/G/1 Queue and the Inspection Paradox," derives it by tagging a job ([Cambridge](https://www.cambridge.org/core/books/abs/performance-modeling-and-design-of-computer-systems/mg1-queue-and-the-inspection-paradox/D78FBA4A6A08631C626E919CA1DB4E5D)).
   - Under processor sharing instead of FCFS, M/G/1/PS has E[T] = E[S]/(1−ρ) for any service distribution. HB Ch. 1 notes the doubling result also holds for PS. The exact chapter or section in HB for the PS formula is **(uncertain)**.

6. **G/G/1, Kingman's heavy-traffic approximation** ([Kingman 1961, *Proc. Camb. Phil. Soc.* 57:902–904](https://doi.org/10.1017/S0305004100036094)), as HB&S state it:
   - **E[Delay] ≈ [ρ/(1−ρ)] · [(C_S² + C_A²)/2] · E[S]**
   - Its three factors are utilization × variability × service time. Hopp & Spearman's *Factory Physics* calls it the "VUT equation"; the chapter number there is **(uncertain)**.
   - **Limits:** it is an approximation, accurate as ρ → 1 and rougher at light load.

7. **M/M/c, Erlang C**:
   - P(wait) = C(c, A), and E[T_Q] = C(c, A)/(cµ − λ).
   - Pooled delay for jobs that queue = (1/(kλ))·ρ/(1−ρ), which falls roughly as 1/k at fixed ρ (HB&S §2.3, citing HB p. 270).
   - More servers let you run at higher ρ for the same delay. Brooker 2020: 5 servers at half load serve 87% of requests with no queueing; 10 servers at the same utilization serve 96.4%. Square-root staffing: HB Ch. 15; Halfin & Whitt 1981, [*Oper. Res.* 29(3):567–588](https://doi.org/10.1287/opre.29.3.567).

8. **Scaling result**: multiplying both λ and µ by K divides E[T] by K and leaves ρ and E[N] unchanged (B&G Ex. 3.8, "quite general, even applying to networks of queues"; HB Ch. 1).

9. **Closed interactive systems** (N users, think time Z, total demand D, bottleneck demand D_max) (QSP Ch. 5):
   - X(N) ≤ min(1/D_max, N/(D+Z))
   - max(D, N·D_max − Z) ≤ R(N)
   - Knee population N* = (D+Z)/D_max.
   - Past saturation, response time grows *linearly* in N, not hyperbolically.
   - Closed systems are much less sensitive to service variability (HB&S §5, Fig. 7).

**Where results stop holding:**
- **ρ ≥ 1:** there is no steady state. Queues grow roughly linearly in time; the formulas give no finite answer.
- **Finite buffers or timeouts:** you get drops or errors instead of infinite waits.
- **Closed clients:** see result 9.
- **Non-Poisson, bursty or correlated arrivals:** Paxson & Floyd 1995 found Poisson "valid only for modeling the arrival of user sessions," not packets ([IEEE/ACM ToN 3(3):226–244](https://web.stanford.edu/class/cs244/papers/paxson1995.pdf)).
- **Heavy-tailed service** (see result 5).
- **Transients and short windows.**
- **Contention and coherency costs** that grow with load, which are outside queueing models. AWS attributes part of the latency rise it measures to the Universal Scalability Law ([Yanacek, "Using load shedding to avoid overload"](https://d1.awsstatic.com/builderslibrary/pdfs/using-load-shedding-to-avoid-overload.pdf)).

## 5. Standard numeric examples as they appear in the sources

- **QSP §1.2.1**: λ = 0.5/s, S = 1.25 s gives U = .625, R = 3.33 s, queue length 1.67, X = 0.5/s. It saturates at 0.8/s.
- **QSP §3.2**: a disk serving 40 req/s at .0225 s each is 90% utilized.
- **HB Ch. 1**: λ = 3/s, µ = 5/s. If λ doubles, how much faster must the CPU be to keep E[T] the same? The answer is "less than double." Under M/M/1, E[T] = 0.5 s at (3, 5), and µ = 8 restores it at λ = 6 **(derived)**.
- **The M/M/1 multiplier ladder** R/S = 1/(1−ρ) **(derived; the shape shown in QSP Fig. 1.2 and B&G Fig. 3.7)**:

| ρ | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 0.95 | 0.99 |
|---|---|---|---|---|---|---|---|
| M/M/1 mean R/S | 2 | 2.5 | 3.3 | 5 | 10 | 20 | 100 |
| M/D/1 mean R/S | 1.5 | 1.75 | 2.2 | 3 | 5.5 | 10.5 | 50.5 |
| M/M/1 p99/S | 9.2 | 11.5 | 15.4 | 23 | 46 | 92 | 460 |

- **Schwartz**: with S = 0.25, R is 0.5 at 50%, 1.0 at 75% and 2.0 at 87.5%. "Halve the idle capacity, double the response time." Grocery example: 1 shopper/min with 45 s service (75% busy). Airport: 240 people/h, 15 s per check, 2 agents gives 20 s combined vs 30 s with separate lines. At 4× traffic with 4× agents it is 15.24 s vs 30 s.
- **Cook 2008**: λ = 5.8/h and 10-min service (ρ ≈ 0.97). One teller gives "nearly five hours" average wait; two tellers give "about 3 minutes" (I get 4.8 h and 3.0 min **(derived)**).
- **Brooker 2021**: E[N] = ρ/(1−ρ) is 1 at ρ = 0.5 and 99 at ρ = 0.99.
- **Slimmon 2016**: a simulation with one task/s capacity. Things "start to get a little crazy around 80%," and at 96% "average wait times are already 20 seconds."
- **Millsap's knee table** for M/M/m. He defines the knee as the ρ that minimizes R/ρ. Knees are 1→50%, 2→57%, 4→66%, 8→74%, 16→81%, 32→86%, 64→89%, 128→92%. I recomputed these with Erlang C and they agree within rounding (64→0.90, 128→0.93).
- **Gregg, *Systems Performance*** (M/D/1): "Beyond 60% utilization, the average response time doubles. By 80%, it has tripled." Verified only via a [Goodreads quote](https://www.goodreads.com/author/quotes/54982.Brendan_Gregg); the exact page is **(uncertain)**. Exact M/D/1 gives 1.75× at 60%, 2× at ≈67% and 3× at 80% **(derived)**.
- **Dean & Barroso, "The Tail at Scale," *CACM* 56(2), 2013** ([PDF](https://www.barroso.org/publications/TheTailAtScale.pdf)):
  - Servers that normally answer in 10 ms but have a 1 s p99, fanned out 100 ways, make 63% of requests take over 1 s.
  - With 2,000 servers each slow 1-in-10,000 times, "almost one in five" requests are slow.
  - Table 1: p99 is 10 ms for one leaf, 70 ms for 95% of leaves and 140 ms for all leaves.
  - Hedged requests cut p99.9 from 1,800 ms to 74 ms for 2% extra requests.
- **Little's law in services** (Yanacek, "Avoiding insurmountable queue backlogs," [AWS](https://d1.awsstatic.com/builderslibrary/pdfs/avoiding-insurmountable-queue-backlogs.pdf)): 100 msg/s at 100 ms uses about 10 threads. If latency rises to 10 s, that becomes about 1,000 threads.
- **Variability in practice** (HB&S §1): Google Borg jobs have C_S² = 23,000, and the largest 1% of jobs make up 99% of the load.
- **Jain Example 31.x** (M/M/1 gateway: 125 packets/s, 2 ms service, ρ = 0.25, buffer-overflow probability ρⁿ) is **(uncertain)**. This is from memory; I could not open Jain's book or slides.

## 6. Misconceptions practitioners bring, and the canonical correction

| Misconception | Canonical correction | Source |
|---|---|---|
| "No queue until we're over capacity." | Random arrivals and variable service create queues well below 100%. "Queueing happens even when there's more than enough capacity." | Schwartz §"Why Does Queueing Happen?"; Millsap's random-arrivals slides |
| "Latency grows roughly linearly with load." | It grows as 1/(1−ρ): each step closer to 100% costs more than the last. "Human intuition is linear… Queueing systems are nonlinear." | Schwartz; QSP §1.2.1 |
| "Low utilization means low delay." | Delay ≈ ρ/(1−ρ) × variability × S. High C_S² can dominate at low ρ. This is HB&S's question (i): "My system utilization is very low, so why are job delays so high?" | HB&S §1 (Kingman) |
| "If load doubles and capacity doubles, latency stays the same." | Latency halves. So less than double the capacity is needed. | HB Ch. 1 Ex. 1; B&G Ex. 3.8 |
| "Adding one server to a saturated service helps proportionally." | Near saturation it helps enormously (5 h → 3 min) because of the nonlinearity. | Cook 2008 |
| "Separate queues per worker are as good as one shared queue." | Pooling cuts delay sharply at the same ρ. | B&G Ex. 3.9; HB&S §2.3; Schwartz airport |
| "There is a safe utilization, e.g. 70–80%." | The knee depends on the number of servers, variability and the SLO. "The knee depends on the configuration." "There is no response time knee; only service level agreements." | Millsap table; Schwartz; [Gunther 2008](http://perfdynamics.blogspot.com/2008/03/watching-your-knees-and-queues.html) |
| "My dashboard says 70% CPU, so I'm fine." | Averages over seconds or minutes "can hide short bursts of 100% utilization." Queue length measures saturation. | [Gregg, USE Method](https://www.brendangregg.com/usemethod.html) |
| "A load test with N threads shows production behavior." | A closed-loop generator caps concurrency and hides queueing. Measuring from actual rather than intended send time causes coordinated omission: in the wrk2 README, p99 of 6.04 ms vs a corrected 1.27 s. | Schroeder et al. 2006; [wrk2 README](https://github.com/giltene/wrk2); Gil Tene, "How NOT to Measure Latency" (QCon/Strange Loop talks, 2013–15) |
| "Speeding up a server always improves response time." | In closed systems a faster non-bottleneck can do "not really" anything. | HB Ch. 1 Design Example 2; QSP Ch. 5 bounds |
| "The average is what users feel." | With fan-out, users see the maximum of many leaves, so tails dominate. Brooker counters: mean latency is right for *efficiency*, and percentiles are a leading indicator of overload. | Tail at Scale; Brooker 2021 |
| "Bigger buffers and queues improve reliability." | Standing queues add delay without adding throughput (bufferbloat). A backlogged queue flips a system into a slow "bimodal" mode. Retries amplify overload. | [Nichols & Jacobson, "Controlling Queue Delay," ACM Queue 10(5), 2012](https://dl.acm.org/doi/10.1145/2209249.2209264); Yanacek (AWS); [Google SRE book Ch. 22](https://sre.google/sre-book/addressing-cascading-failures/) |

## 7. For a short lesson

**Essential:**
- The setup: arrivals, one server, a line; response time = wait + service; utilization = arrival rate × service time, i.e. the fraction of time busy.
- *Why* waits happen below 100%: bursts of arrivals and occasional long jobs, plus lost idle time that can never be recovered (Schwartz's three reasons).
- The curve R = S/(1−ρ) with the ladder 2× at 50%, 5× at 80%, 10× at 90%, 20× at 95%.
- The consequence: the last few percent of capacity are the most expensive, and a service at "moderate" average load can be one burst away from the steep part.
- What happens at or above 100%: the backlog grows until timeouts or errors, and it takes time to drain.

**Common extras (pick one or two):**
- Little's law, as "in-flight = throughput × latency," for sizing thread pools.
- The effect of variability (M/D/1 vs M/M/1; Kingman).
- Multiple servers and pooling, which move the knee right (Millsap table, Brooker 2020).
- Tail latency: M/M/1 p99 ≈ 4.6 × mean, and fan-out.
- Open vs closed load testing.
- Mitigations: headroom, load shedding, CoDel/LIFO, concurrency limits.

**Leave out:**
- Markov-chain and birth–death derivations, PASTA, transforms.
- Full Kendall notation beyond "M/M/1."
- Algebra of the Erlang C formula; Jackson and BCMP networks; MVA.
- Scheduling theory (SRPT, Gittins); heavy-traffic diffusion limits; the Universal Scalability Law.

## 8. Real systems canonically cited, with mechanism

- **Telephone exchanges and call centers.** Erlang (1909 Poisson traffic; 1917 loss and waiting-time formulas, i.e. Erlang B and C; [MacTutor](https://mathshistory.st-andrews.ac.uk/Biographies/Erlang/)). Staffing uses the Erlang C / Halfin–Whitt square-root rule (HB Ch. 15).
- **Disks and CPUs.**
  - Disk I/O is non-preemptible, so queueing becomes "noticeable" above about 70% utilization. CPU saturation shows up as run-queue length ([Gregg, USE Method](https://www.brendangregg.com/usemethod.html); Gregg *Systems Performance* §2.6.5, M/D/1).
  - QSP uses disks as the utilization-law example.
- **Packet networks and routers.**
  - Statistical multiplexing versus TDM/FDM (B&G §3.1, Ex. 3.9).
  - CoDel active queue management (Nichols & Jacobson 2012) drops packets based on *sojourn time* above a target (5 ms) over an interval (100 ms), to remove "standing queues" (bufferbloat).
- **Facebook.** In "Fail at Scale" (Maurer, [ACM Queue 13(8), 2015](https://queue.acm.org/detail.cfm?id=2839461); [summary](https://blog.acolyer.org/2015/11/19/fail-at-scale-controlling-queue-delay/)), servers use CoDel-style queue timeouts (M = 5 ms, N = 100 ms) plus **adaptive LIFO**: FIFO normally, switching to LIFO once a queue forms. They also use concurrency control.
- **Google.**
  - Tail at Scale: hedged and tied requests; keep low-level OS disk queues shallow and use their own priority queues.
  - SRE book Ch. 22 (Ulrich): queues at most about 50% of the thread-pool size; "queueless" Gmail servers that fail over to other tasks when threads are full; LIFO or CoDel; return 503 above a limit on in-flight requests; "randomized exponential backoff" on retries.
- **Load balancers.** Power of two choices ([Mitzenmacher 2001, *IEEE TPDS* 12(10):1094–1104](https://www.eecs.harvard.edu/~michaelm/postscripts/tpds2001.pdf)). Envoy's least-request balancer picks 2 random hosts and sends to the one with fewer active requests ([Envoy docs](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers)). Dean & Barroso also cite Mitzenmacher.
- **Netflix concurrency-limits** ([GitHub](https://github.com/Netflix/concurrency-limits)):
  - The limit follows Little's law: Limit = RPS × latency.
  - The TCP-Vegas-style estimator uses queue ≈ L(1 − minRTT/sampleRTT) to adjust the limit.
  - Excess requests are rejected with 429 / UNAVAILABLE rather than queued.
- **AWS (Builders' Library, Yanacek).**
  - Load shedding protects *goodput*. When median latency reaches the client timeout, availability is 50%.
  - Deadlines are propagated between hops.
  - Queue backlogs are "bimodal," so AWS sidelines old traffic, drops messages by TTL and uses LIFO-ish ordering.
- **Metastable failures.** Retry and backlog feedback loops keep a system overloaded after the trigger is gone (Bronson et al., [HotOS 2021](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf); Huang et al., [OSDI 2022](https://www.usenix.org/system/files/osdi22-huang-lexiang.pdf): 21 incidents; at least 4 of 15 major AWS outages).

## 9. Claims that are commonly overstated or subtly wrong

1. **"Response time goes to infinity at 100%."** This holds only for the steady-state *open* model with an infinite buffer. In reality you get drops or timeouts (finite K). With closed-loop clients R grows *linearly* in N (QSP Ch. 5). Over a finite window the backlog grows roughly linearly in time.
2. **"The knee is at 70/75/80%."** There is no universal knee. Millsap's is a chosen criterion (min R/ρ), gives 50% for one server and 92% for 128. Gunther calls knees an "optical illusion" of axis scaling. Schwartz: "this folklore is wrong."
3. **"Utilization X gives response time Y"** applies only under stated assumptions. 1/(1−ρ) is the M/M/1 special case. Deterministic service halves the wait; high C_S² multiplies it (P-K, Kingman). Multiple servers flatten the curve. Gregg's "doubles beyond 60%" is an M/D/1 figure, and even there the exact doubling point is ≈67%.
4. **"Little's law needs Poisson/FIFO/M/M/1."** False: it is distribution-free (Little 2011). The opposite overreach is also wrong. It says nothing about percentiles, and it must use time *in system*. Slimmon's "by Little's Law… average *service* time is directly proportional to queue size" should say time in system.
5. **"Pooling / one fast server is always better."** Pooling a shared queue beats separate queues. But "one fast vs k slow" *depends*: with high job-size variability and non-preemptible jobs, many slow servers can win (HB Ch. 1 Ex. 3). At heavy load the fast-vs-slow gap shrinks toward 1 (B&G Ex. 3.10).
6. **"p99 = constant × mean."** Only for exponential sojourn times (M/M/1 FCFS: about 4.6×). It does not hold in general.
7. **"Real traffic isn't Poisson, so the theory doesn't apply."** This is overstated in the other direction. Session and user arrivals are close to Poisson; packet-level traffic is not (Paxson & Floyd). The qualitative lessons (nonlinearity, variability, pooling) survive through Kingman and P-K.
8. **"Never look at average latency."** Brooker argues the mean is the right efficiency metric, with percentiles as early-warning signals.
9. **"The latency hockey stick in load tests is pure queueing."** Part of it is contention, context switching and GC (USL), per AWS's own load-test explanation.
10. **"Little's law sizes the pool."** It gives the *average* concurrency. Peaks need headroom ("on average, so it could be more in practice," Yanacek).

## 10. Animation, doing, or reading?

Parts of this section are my pedagogical judgment. The general evidence I rely on: instructional animation beats static pictures on average (d = 0.37), more so when it is representational (d = 0.40) ([Höffler & Leutner 2007, *Learning and Instruction* 17(6):722–738](https://www.sciencedirect.com/science/article/abs/pii/S0959475207001077)). Interactive simulations help learners build models through exploration ([Wieman, Adams & Perkins 2008, *Science* 322:682](https://phet.colorado.edu/publications/PhET_Simulations_That_Enhance_Learning.pdf)).

**Best as a narrated animation** (dynamic mechanisms that are hard to picture from a formula):
- Random arrivals clumping and a line forming at 60–75% utilization, versus evenly spaced arrivals with no line. This is Millsap's 3.000 s vs 4.267 s example, which is naturally a timeline.
- Idle time being "lost forever."
- The queue at 95% ballooning and draining slowly.
- The same run drawn side by side as the hockey-stick curve.
- Shared line versus separate lines.
- The cumulative arrivals/departures staircase, where the area between the curves is Little's law (QSP Fig. 3.2; B&G Fig. 3.1).
- Fan-out turning rare slow leaves into common slow requests.

**Best by doing: an interactive simulation or code** (build intuition by predicting, then checking):
- A utilization slider that shows mean and p99 latency. Learners predict the latency at 90% before revealing it.
- Knobs for service-time variability (constant / exponential / heavy-tailed) and number of servers, to see the knee move.
- A load-test exercise comparing open (constant-rate) with closed (fixed-threads) clients and fixing coordinated omission.
- Computing Little's law from a request log.
- Caveat: near ρ → 1, simulations converge slowly and vary a lot between runs. Slimmon's 96% run shows about 20 s against 24 s in theory **(derived)**. Short runs mislead, and that is itself worth showing.
- Schwartz links interactive plots, and Brooker validates with Monte Carlo, so this format is established.

**Best by reading** (precision and reference):
- Exact formulas with their assumptions, and where they break (§4).
- The notation-clash table (§3).
- The numeric ladder and the Millsap knee table.
- Operational definitions of what to measure.
- Mitigation patterns and their sources (§8).
- These are needed later for lookup and are too dense for narration.

---

**Unverified or uncertain items, collected:**
- Kleinrock's exact symbols and section numbers.
- HB's T_Q symbol and the chapter for the PS formula.
- Jain's section contents and the gateway example.
- Gross–Harris L_q/W_q (standard, but not checked).
- Who extended Kendall notation.
- The Factory Physics chapter number.
- The exact page of the Gregg quote and his definition of "latency."
- The Schwartz ebook's publication year.
