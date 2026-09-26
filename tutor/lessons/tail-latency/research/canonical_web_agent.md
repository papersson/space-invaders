# Tail latency at scale: the canonical treatment (research notes)

How this was checked. Every item is tied to a source I fetched and read in full or in the relevant part, unless it is marked **(uncertain)** or **(my computation / my judgment)**. DDIA wording was checked against a complete chapter translation ([Vonng/ddia](https://github.com/Vonng/ddia), editions 1 and 2), not the English print text, because O'Reilly's pages returned 403.

## Core sources (short keys used below)

| Key | Source | What it contributes |
|---|---|---|
| **[DB13]** | J. Dean & L. A. Barroso, "The Tail at Scale," *CACM* 56(2):74–80, Feb 2013, [doi:10.1145/2408776.2408794](https://doi.org/10.1145/2408776.2408794) ([PDF](https://www.barroso.org/publications/TheTailAtScale.pdf)) | The primary source. It gives the hypothetical fan-out example, Google measurements, and the catalogue of "tail-tolerant" techniques. |
| **[Dean12]** | J. Dean, "Achieving Rapid Response Times in Large Online Services," Berkeley AMPLab Cloud Seminar, 26 Mar 2012 ([slides](https://research.google.com/pubs/archive/44875.pdf)) | The talk version. The terms and some numbers differ from [DB13]. |
| **[DDIA1]** | M. Kleppmann, *Designing Data-Intensive Applications*, O'Reilly 2017, Ch. 1 → "Scalability" → "Describing Performance" (plus the sidebar "Percentiles in Practice") | The standard practitioner textbook. It introduces the term "tail latency amplification". |
| **[DDIA2]** | M. Kleppmann & C. Riccomini, *DDIA* 2nd ed., O'Reilly 2026 ([announcement](https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html)), Ch. 2 "Defining Nonfunctional Requirements" → "Describing Performance" (the subsections are roughly "Latency and Response Time", "Average, Median, and Percentiles" and "Use of Response Time Metrics"; the English heading wording is **uncertain** because I read it through the translation) | The updated treatment. It adds a sceptical sidebar on user-impact statistics. |
| **[SRE16]** | Beyer et al., *Site Reliability Engineering*, O'Reilly 2016. Ch. 4 "Service Level Objectives" (§Aggregation) ([online](https://sre.google/sre-book/service-level-objectives/)). Ch. 6 "Monitoring Distributed Systems" (§"The Four Golden Signals"; §"Worrying About Your Tail (or, Instrumentation and Performance)") ([online](https://sre.google/sre-book/monitoring-distributed-systems/)) | The operations framing: distributions not averages, and histogram buckets. |
| **[Dynamo07]** | DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store," SOSP 2007 ([PDF](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)) | The origin of "SLAs at the 99.9th percentile". |
| **[Tene]** | G. Tene: "#LatencyTipOfTheDay: MOST page loads will experience the 99%'lie server response," 28 Jun 2014 ([post](http://latencytipoftheday.blogspot.com/2014/06/latencytipoftheday-most-page-loads.html)); "Coordinated Omission," mechanical-sympathy list, 3 Aug 2013 ([post](https://groups.google.com/g/mechanical-sympathy/c/icNZJejUHfE/m/BfDekfBEs_sJ)); talk "How NOT to Measure Latency" (QCon/Strange Loop 2013–2015) | The page-view framing and the measurement pitfalls. |
| Queueing | M. Harchol-Balter, *Performance Modeling and Design of Computer Systems*, CUP 2013 (Ch. 20 "Tales of Tails", Ch. 23 "The M/G/1 Queue and the Inspection Paradox"); L. Flatto & S. Hahn, *SIAM J. Appl. Math.* 44, 1984; R. Nelson & A. N. Tantawi, *IEEE Trans. Computers* 37(6), 1988 ([doi](https://doi.org/10.1109/12.2213)) | The formal model: fork-join queues. |

Course usage I verified: MIT 6.1800 (2025) assigns [DB13] as a recitation reading. The course describes it as the bridge from single-machine systems to multi-machine systems, and asks: what is latency, why does the tail matter and who experiences it, and name one mitigation ([6.1800 recitation page](https://web.mit.edu/6.1800/2025/wwwdocs/recitations/06-tail.shtml)). I did not check other syllabi.

---

## 1. The canonical worked example

**A. The standard example: the Dean & Barroso fan-out calculation.** Quoting [DB13, §"Component-Level Variability Amplified By Scale"]:

- Each server "typically responds in 10ms but with a 99th-percentile latency of one second."
- With one server, 1 request in 100 is slow.
- If a request "must collect responses from 100 such servers in parallel, then 63% of user requests will take more than one second."
- Even if only 1 in 10,000 requests is slow per server, "a service with 2,000 such servers will see almost one in five user requests taking more than one second."
- A figure plots P(service latency > 1 s) against the number of servers (1 to 2,000) for per-server outlier rates of 1/100, 1/1,000 and 1/10,000. It marks the 0.63 and 0.18 points.

Right after the hypothetical, the paper gives its **empirical companion, Table 1**: a real Google fan-out tree (root → intermediate servers → leaves), measured at the root. The 99th-percentile latency is 10 ms for one random leaf, 70 ms for 95% of the leaves and 140 ms for all leaves. Hence "waiting for the slowest 5% of the requests to complete is responsible for half of the total 99%-percentile latency."

Why this example is the standard one:
- It comes from the paper that framed the topic and named the techniques.
- It needs only independence and the complement rule.
- Its round numbers give a result that feels wrong at first (1% becomes 63%).
- It maps directly onto a real architecture (web-search fan-out).
- It is the citation DDIA uses for "tail latency amplification" ([DDIA1] ref. 24; [DDIA2] ref. 26), and it is the reading MIT 6.1800 assigns.

The talk version [Dean12] uses the same example ("touch 1 of these: 1% of requests take ≥1 sec; touch 100 of these: 63%…"). See §9 for a numeric slip in the talk version.

**B. The competing framing: "a user page makes many requests".** Gil Tene's version says the chance that a page view avoids a server's p99 is 0.99^N. With N ≥ 69 requests per page, most page loads see the p99. His table gives amazon.com 190 requests → 85.2%, CNN 279 → 93.9% and google.com 31 → 26.7% [Tene 2014]. Related forms:
- [DDIA1]: a user who issues several requests, or a page with many resources, has a much greater than 50% chance that at least one of them is slower than the median.
- [SRE16 Ch. 6]: "the 99th percentile of one backend can easily become the median response of your frontend."
- [DDIA] Fig. 1-5 (1st ed.) / Fig. 2-6 (2nd ed.) shows the same idea qualitatively: one slow backend call slows the whole user request.

**Which is more common:** A is more common in papers, textbooks and courses. B is more common in practitioner talks and blog posts. **(my judgment; I did not count occurrences)**

## 2. The standard progression

**[DB13] order** (the section headings as they appear in the paper):
1. Motivation: interfaces feel fluid under about 100 ms (Card et al. 1991).
2. "Why Variability Exists?": shared resources, daemons, global resource sharing, maintenance activities (log compaction, GC), queueing, power limits, SSD garbage collection, energy management.
3. "Component-Level Variability Amplified By Scale": the hypothetical (1 server → 100 → 2,000 servers), then the real measurement (Table 1).
4. "Reducing Component Variability": service classes and higher-level queuing, reducing head-of-line blocking (time-slicing long queries), managing background activity, synchronized disruption. Caching "do[es] not directly address tail latency."
5. "Living with Latency Variability", split into two groups:
   - "Within Request Short-Term Adaptations": hedged requests, then deferred hedging, then tied requests, then probe-first as a weaker alternative, then the erasure-coded variant.
   - "Cross-Request Long-Term Adaptations": micro-partitions, then selective replication, then latency-induced probation.
6. "Large Information Retrieval Systems": good-enough results and canary requests.
7. "Mutations": quorum algorithms are "inherently tail-tolerant".
8. Hardware trends.
9. Conclusion: tail-tolerance is analogous to fault-tolerance.

**[Dean12] talk order:**
"Faster is better" → large fan-out services → "Why does fanout make things harder?" (1 vs 100 servers) → "Squash all variability" is not tenable at scale → shared environment → basic techniques → synchronized disruption → tolerating faults vs tolerating variability → cross-request adaptation → within-request adaptation (canary, backup requests, backup requests with cross-server cancellation and their "bad case", tainted partial results) → hardware trends.

**[DDIA1/2] order:**
1. Response time vs latency definitions.
2. Latency as a distribution: a 100-request bar chart (Fig. 1-4 / 2-5).
3. Mean, then median/p50, then p95/p99/p999.
4. Why the tail matters: Amazon's p99.9; p99.99 judged too expensive.
5. SLOs/SLAs.
6. Queueing delay and head-of-line blocking, so measure at the client.
7. The load generator must send requests independently of responses.
8. Tail latency amplification.
9. Computing percentiles: histograms; never average percentiles.

(In the 1st edition, amplification sits inside the "Percentiles in Practice" sidebar. In the 2nd edition it opens "Use of Response Time Metrics".)

**Simpler versions shown before full ones:**
- mean → median → high percentiles ([DDIA], [SRE16 Ch. 4])
- one server → N servers ([DB13])
- idealized independent model → measured tree with intermediate levels ([DB13] Table 1)
- naive hedging (which "add[s] unacceptable additional load") → hedging deferred to the p95 → tied requests with cross-server cancellation ([DB13])
- in the talk: "Backup Requests" → "…w/ Cross-Server Cancellation" → "Bad Case" (both servers start the request) → fix with a small delay ([Dean12])

A queueing-theory course would go M/M/1 → M/G/1 (variability) → fork-join (K=2 exact → approximations) (Harchol-Balter 2013; Nelson & Tantawi 1988). **(uncertain whether any course pairs this sequence with [DB13])**

## 3. Model, parameters, what is measured, notation

**Standard model.**
- A root (aggregator) fans a request out to **N** leaves in parallel and must wait for **all** of them.
- Leaf latency L_i has CDF F. In the simple model the L_i are i.i.d.
- End-to-end latency is T = max_i L_i.
- Parameters: N (fan-out); the per-leaf percentile p, or the exceedance probability q = 1 − p; a latency threshold t.
- Extended versions add:
  - tree depth ([DB13] Table 1 has intermediate servers);
  - serial chains, where latencies add rather than take the max ([Brooker 2021](https://brooker.co.za/blog/2021/04/19/latency.html));
  - waiting for only k of N (quorums, [Dynamo07] §4.5);
  - queueing at each leaf (fork-join queue: Poisson arrivals, K servers, a job leaves when all K tasks finish).

**What is measured.**
- Per-request response time, observed where the waiting happens: at the root or client.
- Percentiles are taken over requests (not users, not time) within a window.
- [DB13] Table 1 is "measured from root node of the tree". The hedging benchmark measures the time to retrieve *all* 1,000 values ([Dean12]: "until data for last key arrives").
- [DDIA] insists on client-side measurement because queueing delay is not part of service time.
- [SRE16 Ch. 6] separates the latency of successful requests from the latency of failed requests.

**Notation and terminology that varies between sources:**

| Concept | Variants (source) |
|---|---|
| Percentiles | p50/p95/p99/**p999** = 99.9th ([DDIA]); "99%ile" ([DB13] tables; [Dean12]); "p99.9" ([AWS Builders' Library](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/developer-tools/approved/pdfs/timeouts-retries-and-backoff-with-jitter.pdf)); "TP99" as Amazon jargon **(uncertain; no primary source checked)** |
| Latency vs response time | [DDIA]: *response time* is what the client sees (service time + queueing + network); *latency* is the time a request is latent, waiting. [DB13] and [SRE16] use "latency" for the whole response time. Queueing theory: response or **sojourn** time T = waiting time T_Q + service time S |
| The amplification effect | "component-level variability amplified by scale" ([DB13]); "tail latency amplification" ([DDIA]); "fan-out" ([Dean12]); **Partition/Aggregate** with an "all-up SLA" plus **incast** (networking: [DCTCP, SIGCOMM 2010](https://people.csail.mit.edu/alizadeh/papers/dctcp-sigcomm10.pdf)); **fork-join queue** / join synchronization (queueing theory); **stragglers** (batch processing: [MapReduce OSDI 2004 §3.6](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf)) |
| Duplicate-request technique | "backup requests" ([Dean12]; Finagle) = "hedged requests" ([DB13]) = "speculative retry" / rapid read protection (Cassandra) = "request hedging" (Envoy, gRPC) = "redundancy"/replication ([Vulimiri et al., CoNEXT 2013](https://arxiv.org/pdf/1306.3707)) = "reissues" ([Kwiken, SIGCOMM 2013](https://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p219.pdf)) = "backup tasks" (MapReduce, for batch jobs) |
| With cancellation | "tied requests" ([DB13]) = "backup requests w/ cross-server cancellation" ([Dean12]); close relative: Sparrow's "late binding" ([SOSP 2013](https://people.eecs.berkeley.edu/~matei/papers/2013/sosp_sparrow.pdf)) |
| Partial answers | "good enough" ([DB13]) = "tainted partial results" ([Dean12]) = "incompleteness"/partial results (Kwiken) |
| Queueing symbols | λ arrival rate, μ service rate, ρ = λ/μ utilization; Kendall A/S/c ([Li et al., "Tales of the Tail," SoCC 2014](https://drkp.net/papers/latency-tr14.pdf)); H_K harmonic numbers |
| Plots | percentile-over-time lines on a log y-axis ([SRE16] Fig. 4-1); CCDF P[X ≥ x] on log–log axes ([Li et al. 2014] Fig. 1) |

## 4. Key results, assumptions, and where they stop holding

**Fan-out (i.i.d., wait for all N).** This is standard probability; [DB13] uses it without writing it down.
- P(T > t) = 1 − F(t)^N.
- At the leaf's p-th percentile: **P(T > t_p) = 1 − p^N ≈ 1 − e^(−Nq) ≈ Nq when Nq ≪ 1.**
- Fan-out percentile: **T_p = F⁻¹(p^(1/N)) ≈ F⁻¹(1 − q/N).** For N = 100, the fan-out p99 equals the leaf's **p99.99** (0.99^(1/100) = 0.9999).
- The leaf p-th percentile becomes the fan-out *median* when N = ln 2 / (−ln p). That is N ≈ 69 for p99 and ≈ 693 for p99.9 **(my computation)**. This matches Tene's "69 or more".

**How much the tail grows depends on the shape of the leaf distribution (my computation, standard order statistics).**

| Leaf distribution | Leaf p50 | Leaf p99 | Fan-out (N=100) p50 | Fan-out (N=100) p99 |
|---|---|---|---|---|
| Exponential, mean 1 | 0.69 | 4.6 | 5.0 | 9.2 |
| Pareto α=2, x_m=1 | 1.41 | 10 | 12 | ≈100 |
| Google, measured ([DB13] Table 1) | 1 ms | 10 ms | 40 ms | 140 ms |

- Exponential leaves: E[max] = H_N/μ ≈ (ln N + 0.577)/μ, so the tail grows logarithmically. The variant with K identical exponential sub-tasks is stated in [Varki & Merchant](https://www.cs.unh.edu/~varki/publication/2002-nov-open.pdf).
- Pareto leaves: quantiles grow like N^(1/α).
- Bimodal "hiccup" leaves, as in the canonical example, turn a rare mode into the common case.

**Single-server queueing (why utilization drives the tail).**
- M/M/1 (Poisson arrivals, exponential service, FCFS): response time T ~ Exp(μ − λ), as stated and used in [Vulimiri 2013, Thm 1 proof].
- E[T] = 1/(μ − λ) = E[S]/(1 − ρ), and T_p = −ln(1 − p)·E[T]. So **p99 ≈ 4.6 × mean** and p99.9 ≈ 6.9 × mean.
- In units of mean service time, p99 is ≈ 9 at ρ = 0.5 and ≈ 46 at ρ = 0.9 **(my computation)**.
- M/G/1, Pollaczek–Khinchine: **E[T_Q] = ρ/(1−ρ) · E[S²]/(2E[S]).** Service-time variability (E[S²]) directly scales queueing delay (Harchol-Balter 2013, Ch. 23).
- The qualitative facts in [Li et al. 2014 §2]:
  - arrival burstiness alone creates a tail even with constant service times;
  - a higher utilization gives a longer tail;
  - more workers can shorten the tail at equal utilization;
  - the queueing discipline matters.

**Fork-join queues (the formal version of fan-out with queueing).**
- K = 2 exact (Flatto & Hahn 1984): **E[T_2] = (12 − ρ)/8 · 1/(μ − λ).**
- K > 2 (Nelson & Tantawi 1988): **E[T_K] ≈ [H_K/H_2 + (4/11)(1 − H_K/H_2)ρ] · E[T_2]**, with error under 5% for K ≤ 32 ([IBM abstract](https://research.ibm.com/publications/approximate-analysis-of-forkjoin-synchronization-in-parallel-queues); formula as reproduced in [arXiv:1707.08860](https://arxiv.org/pdf/1707.08860)).
- Why exact results are hard: the sub-task response times are *positively associated*, because all queues share the same arrivals. So **P(max ≤ t) ≥ ∏ P(X_i ≤ t)**: the independent model gives an **upper bound** H_K/(μ − λ) (same source).

**Mitigation results.**
- **Deferred hedging:** send the second copy only after the p95 of expected latency, which "limits the additional load to approximately 5%" [DB13]. In general, extra load ≈ 1 − x for a hedge fired at the x-th percentile. Finagle builds its API on this: the backup fires at percentile 100·(1 − maxExtraLoad) ([Finagle MethodBuilder](https://twitter.github.io/finagle/guide/MethodBuilder.html)).
  - With independent replicas, hedged latency is min(L1, d + L2). For t ≥ d, P(> t) = P(L1 > t)·P(L2 > t − d). **(my derivation; standard)**
- **Immediate duplication under load:** with i.i.d. exponential service, replicating each request to 2 servers improves mean latency **iff load < 33%**. Vulimiri et al. conjecture, with evidence, that the threshold always lies between 25% and 50% whatever the distribution, provided client-side overhead is small ([Vulimiri et al. 2013](https://arxiv.org/pdf/1306.3707), Thm 1).
- **k-of-N:** waiting for only the fastest k responses makes latency the k-th order statistic, which is far less sensitive to the tail. Dynamo sets R and W below N "to provide better latency" ([Dynamo07] §4.5). Quorum protocols such as Paxos "must commit to only three to five replicas, they are inherently tail-tolerant" [DB13 §Mutations].
- **Retries compound across layers:** 3 tries at each of 5 layers gives 243× the load on the database ([AWS Builders' Library, Brooker](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/developer-tools/approved/pdfs/timeouts-retries-and-backoff-with-jitter.pdf)).

**Where these results stop holding.**
- **Correlation.** Common-cause slowness (a shared switch, synchronized GC, a single "query of death") breaks independence.
  - Positive association makes 1 − p^N an *over*-estimate of the slow fraction (fork-join bound above). This is the mechanism behind [DB13]'s advice to *synchronize* background activity.
  - The same correlation *defeats hedging*: the techniques are "effective only when the phenomena that causes variability does not tend to simultaneously affect multiple request replicas" [DB13].
- **Non-identical leaves.** Hot partitions, heterogeneous or thermally throttled machines ([DB13] §Cross-Request). Under non-identical leaves the product ∏F_i(t) still holds, but the i.i.d. forms (p^N, "p99.99 per leaf") do not.
- **Slowness inherent in the request.** When slowness is data-dependent, as with Amazon's customers with long histories ([Dynamo07] §2.2), hedging cannot help. Only reducing head-of-line blocking or changing the work can.
- **Feedback.** Hedges and retries add load, which raises utilization and therefore the tail. At high load, duplication hurts ([Vulimiri 2013]). Retry storms can make overload self-sustaining: metastable failure ([Bronson et al., HotOS 2021](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf), cited in [DDIA2]).
- **Heavy tails or non-stationary load.** Logarithmic growth gives way to polynomial growth. FCFS is near tail-optimal for light-tailed job sizes but far from optimal for heavy-tailed ones ([Wierman & Zwart, *Oper. Res.* 60(5), 2012](https://doi.org/10.1287/opre.1120.1086)). [Li et al. 2014]'s "FIFO gives the lowest tail" holds only within their model.
- **Measurement artefacts.** Closed-loop load generators hide the tail (coordinated omission, §6).

## 5. Standard numeric examples as they appear in the sources

| Source | Numbers |
|---|---|
| [DB13] hypothetical | 10 ms typical, p99 = 1 s → 1 server: 1% slow; 100 servers: **63%**; 1-in-10,000 outliers with 2,000 servers: "almost one in five" (0.18) |
| [DB13] Table 1 (real Google fan-out tree) | p50/p95/p99. One random leaf: **1/5/10 ms**. 95% of leaves: **12/32/70 ms**. All leaves: **40/87/140 ms** |
| [DB13] hedged requests | BigTable, 1,000 keys spread over 100 servers. Hedge after 10 ms → p99.9 for all values **1,800 ms → 74 ms** with **2% more requests**. Deferring to the p95 bounds extra load at ≈5% |
| [DB13] Table 2 (tied requests after 1 ms; BigTable reads from the file system, 3 replicas) | Idle cluster, p50/p90/p99/p99.9: **19/38/67/98 → 16/29/42/61 ms**. With a concurrent terasort: **24/56/108/159 → 19/38/67/108 ms**. Disk-utilization overhead **< 1%**. "Nearly identical" to the idle cluster without ties |
| [DB13] cross-request | ~20 partitions per machine → shed load in ~5% steps. BigTable: 20–1,000 tablets per machine. A given leaf holds the best result for "less than one in 1,000 queries" |
| [Dean12] (differs from paper) | "Server with **1 ms avg.** but 1 sec 99%ile." Backup-request table (avg / σ / p95 / p99 / p99.9): none **33 / 1524 / 24 / 52 / 994 ms**; after 10 ms **14 / 4 / 20 / 23 / 50 ms** (<5% extra); after 50 ms **16 / 12 / 57 / 63 / 68 ms** (<1% extra). Tied variant "wait 2 ms", "~1% extra disk reads". "Search 99.9% of docs in 200 ms better than 100% in 1000 ms" |
| [Dynamo07] §2.2, §6 | Example SLA: **300 ms for 99.9%** of requests at a peak of 500 req/s. A page calls **>150 services**. p99.9 ≈ **200 ms**, "an order of magnitude higher than the averages". Write buffer of 1,000 objects cut p99.9 **5×** |
| [DDIA1/2] | Median 200 ms example. "p95 = 1.5 s" means 5 in 100 requests take ≥ 1.5 s. Amazon uses p99.9; p99.99 is "too expensive". 2nd-ed. SLO example: median < 200 ms, p99 < 1 s, ≥ 99.9% non-error |
| [SRE16] Ch. 6 | Mean 100 ms at 1,000 req/s, yet "1% of requests might easily take 5 seconds". Histogram buckets **0–10, 10–30, 30–100, 100–300 ms** (≈×3). Ch. 4, Fig. 4-1: typical request ≈ 50 ms, "5% of requests are 20 times slower" |
| [Tene 2014] | 0.99^N; N ≥ 69 → majority. Amazon 190 → 85.2%; CNN 279 → 93.9%; google.com 31 → 26.7%. He adds the caveat "no strong time-correlation" |
| [Facebook memcache, NSDI 2013](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf) §3.1 | A popular page fetches **521** distinct items on average (p95 1,740). Batches average **24 keys** (p95 95) |
| [Li et al. 2014] | Memcached at 75% utilization: naive p50 **33 µs** / p99.9 **14 ms** → tuned **11 µs / 32 µs** |
| [MapReduce 2004] §3.6 | Backup tasks cost "no more than a few percent". Sort takes **44% longer** without them |
| [AWS Builders' Library] | Pick a false-timeout rate (0.1%), then set the timeout at the downstream **p99.9**. 3 retries × 5 layers = **243×** |

## 6. Misconceptions practitioners bring, and the canonical correction

1. **"The mean (plus standard deviation) summarizes latency."**
   - The distribution is skewed and multimodal.
   - Amazon found mean and median SLAs "not good enough if the goal is to build a system where all customers have a good experience" ([Dynamo07] §2.2).
   - [SRE16 Ch. 4]: "A simple average can obscure these tail latencies."
   - [SRE16 Ch. 6, footnote]: if 1% of requests are 50× the mean, the rest are about 2× faster than the mean.
2. **"p99 affects only 1% of users."** It is 1% of *requests*. Fan-out and multi-request pages multiply exposure ([DB13]; [Tene 2014]; [DDIA]).
3. **"Parallelizing over more servers makes requests faster."** Per-leaf work shrinks, but the max over leaves grows with N ([DB13]; [Dean12] "touching more machines increases likelihood of delays").
4. **"You can average p99s across hosts or time windows."** "Mathematically meaningless"; the right way is to add histograms ([DDIA1/2], citing [Schwartz 2016](https://orangematter.solarwinds.com/2016/11/18/why-percentiles-dont-work-the-way-you-think/)).
5. **"Server-side timing is what users see."** Queueing and head-of-line blocking happen before service starts, so measure at the client ([DDIA]).
6. **"My load test measured the tail."** A closed-loop tester waits for slow responses and so skips sending during stalls. The result is "only omitting the 'very bad results'" ([Tene 2013], coordinated omission). The fix is an open-loop load generator ([DDIA]) or correction as in HdrHistogram's `recordValueWithExpectedInterval()` ([HdrHistogram](https://github.com/HdrHistogram/HdrHistogram)).
7. **"Slow requests are slow because they are expensive."** Often the cause is interference, not the request. That is why hedging works ([DB13]: "the source of latency is often not inherent in the particular request"). Data-dependent slowness exists too ([Dynamo07]).
8. **"Eliminate every source of variability."** This is infeasible in shared environments. Design to be tail-tolerant, as with fault tolerance ([DB13] key insights and conclusion).
9. **"Add a cache" / "just retry on timeout."** Caching does not directly address the tail ([DB13]). Retries multiply load ([AWS]). Hedging with a budget is different from retrying on failure ([Finagle]; [Envoy docs](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_routing): use retry budgets "to avoid retry storms").
10. **"Randomize background jobs so they don't collide."** For fan-out services this is "actually a very bad idea": "one synchronized blip [is] better than unsynchronized" ([Dean12]; [DB13]).
11. **"Removing capacity under load can only hurt."** Latency-induced probation of a slow machine "actually improves latency" ([DB13]).

## 7. For a short lesson

**Essential**
- Latency is a distribution, and a percentile is taken over requests. Why the mean misleads.
- Fan-out waits for the slowest leaf. Show 1 − p^N with the 1 server → 100 servers → 63% example.
- The inverse view: for N = 100, each leaf must meet its p99.99 to deliver a service-level p99.
- One real measurement ([DB13] Table 1) to show the effect is real.
- Causes in one line: interference, queueing, background work, GC.
- The two families of fixes: reduce variability, and tolerate it.
- Hedged requests deferred to the p95 (≈5% extra load, with the BigTable numbers). Tied requests as the refinement.
- Good-enough / partial results.
- Caveat: independence is assumed. Hedging only helps when slowness is uncorrelated and the operation is safe to repeat.

**Common extras**
- Details of tied requests.
- Micro-partitions, selective replication, latency-induced probation, canary requests, synchronized disruption.
- Measurement hygiene: histograms, no averaging of percentiles, coordinated omission.
- The queueing view: utilization drives the tail; M/M/1 p99 ≈ 4.6 × mean.
- SLOs at p99/p99.9 ([Dynamo07]) and timeouts set from the downstream p99.9 ([AWS]).
- Power-of-two-choices / adaptive replica selection.
- Retry budgets.

**Leave out**
- Fork-join formulas (Flatto–Hahn, Nelson–Tantawi).
- Extreme-value theory.
- Tail-optimal scheduling theory.
- Internals of quantile sketches (t-digest, DDSketch).
- The erasure-coded tied-request variant.
- Data-center transport (DCTCP, incast).
- Hardware-trend speculation.
- Business-impact statistics (see §9).

## 8. Real systems canonically cited, and their mechanisms

| System | Mechanism | Source |
|---|---|---|
| Google web search | Root → intermediate → leaf fan-out tree (Table 1). Time-slicing expensive queries to reduce head-of-line blocking. Selective replication of important documents, and language-biased micro-partitions. "Good-enough" results when enough of the corpus has been searched; skipping slow ads or spelling results. Canary requests to 1–2 leaves before fanning out | [DB13] |
| BigTable | Hedged-request benchmark. Tablets as micro-partitions (20–1,000 per machine) | [DB13] |
| Google cluster file system | Shallow OS disk queues with the server's own priority queues. Tied requests with cross-server cancellation (Table 2) | [DB13]; [Dean12] |
| MapReduce | Backup tasks for stragglers near job completion | [MapReduce OSDI 2004 §3.6](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf) |
| Amazon Dynamo | SLAs at p99.9. R, W < N so latency is set by the slowest of R (or W), not N. The write coordinator is the node that replied fastest to the preceding read. In-memory write buffer (p99.9 improved 5×). Client-driven coordination | [Dynamo07] §2.2, §4.5, §5, §6.1, §6.4 |
| AWS services (Builders' Library) | Timeout at the downstream p99.9. Retry at a single layer. Capped exponential backoff with jitter | [Brooker, AWS](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/developer-tools/approved/pdfs/timeouts-retries-and-backoff-with-jitter.pdf) |
| Amazon S3 (client guidance) | "Aggressively retrying slower operations": retry small (<512 KB) GET or PUT after 2 s; retry the slowest 5% (large variable-size requests) or slowest 1% (fixed size); use a new connection and a fresh DNS lookup | [S3 docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html) |
| Apache Cassandra | `speculative_retry` (rapid read protection). Default `99PERCENTILE`. Also `Yms`, `ALWAYS`, and `MIN`/`MAX` hybrids, because "a percentile setting can backfire" when a dead host pushes the percentile up. Introduced in 2.0.2 per the DataStax blog title **(uncertain: I did not read the blog)** | [Cassandra 4.0 CQL DDL docs](https://cassandra.apache.org/doc/4.0/cassandra/cql/ddl.html) |
| C3 / Elasticsearch | Adaptive replica selection that ranks replicas by EWMAs of queue size, service time and response time. C3 reports up to 3× better p99.9. Elasticsearch has had it since 6.1, on by default since 7.0 | [Suresh et al., NSDI 2015](https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/suresh); [Elastic blog 2018](https://www.elastic.co/blog/improving-response-latency-in-elasticsearch-with-adaptive-replica-selection) |
| Twitter Finagle | `BackupRequestFilter` / `idempotent(maxExtraLoad)`: backup fires at percentile 100·(1 − maxExtraLoad) of windowed latency, capped by a retry budget | [Finagle MethodBuilder](https://twitter.github.io/finagle/guide/MethodBuilder.html) |
| gRPC | `hedgingPolicy` (maxAttempts, hedgingDelay, nonFatalStatusCodes) plus `retryThrottling`. Only for methods safe to run more than once. The proposal header lists hedging as not implemented in Go or C-core | [gRFC A6](https://github.com/grpc/proposal/blob/master/A6-client-retries.md) |
| Envoy | Request hedging on per-try timeout: races upstream requests and returns the first acceptable response. Retry budgets | [Envoy routing docs](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_routing) |
| Facebook memcache | 521-item pages. DAG-based batching (24 keys per batch). Client sliding window against incast congestion | [Nishtala et al., NSDI 2013](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf) |
| Microsoft Bing | Partition/aggregate with an all-up SLA of 230–300 ms and worker deadlines of 10–100 ms (DCTCP). Kwiken combines reissues, partial results and catch-up: p99 improves by >50% with 0.1% partial responses | [DCTCP 2010](https://people.csail.mit.edu/alizadeh/papers/dctcp-sigcomm10.pdf); [Kwiken 2013](https://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p219.pdf) |
| Sparrow scheduler | Batch sampling (power of two choices, d = 2) plus late binding. The scheduling analogue of tied requests | [Ousterhout et al., SOSP 2013](https://people.eecs.berkeley.edu/~matei/papers/2013/sosp_sparrow.pdf); [Mitzenmacher, IEEE TPDS 2001] (cited in [DB13]) |

## 9. Claims that are commonly overstated or subtly wrong

1. **"1 ms average but 1 s p99"** ([Dean12] slide) is impossible. If 1% of requests take ≥ 1 s, the mean is at least 10 ms. The paper rewords it as "typically responds in 10ms". Teach the paper's version.
2. **"63% of requests are slow" as a general law.** It is a hypothetical: i.i.d. leaves, all leaves waited on, and a bimodal hiccup distribution.
   - Correlated (positively associated) leaves make 1 − p^N an overestimate.
   - Smooth light tails grow only about logarithmically: with exponential leaves, the fan-out p99 is ≈ 2× the leaf p99, not a jump to the outlier mode (§4 table).
3. **"If you depend on several backends, one backend's p99 becomes your median"** ([SRE16 Ch. 6]). Under independence this needs about 69 calls. With 5 backends only ≈ 5% of requests touch a p99 **(my computation)**.
4. **"Most users see the p99"** ([Tene]).
   - Tene himself notes the assumption that there is "no strong time-correlation".
   - A page's resources come from different servers with different distributions, and many resources are not on the critical path of the page load **(my inference)**.
5. **"Hedging costs only 2–5%."** That holds when the trigger percentile is stable and slowness is uncorrelated.
   - During incidents the percentile or fixed-ms trigger can fire for most requests. That is why Cassandra warns percentile triggers can backfire, and why Finagle and Envoy add budgets.
   - Hedging also requires idempotent or safe operations ([gRFC A6]).
6. **"Redundancy always helps."** It helps only below a threshold load (33% for exponential service; conjectured 25–50%) and only when client overhead is small ([Vulimiri 2013]). It does not help against correlated slowness ([DB13]).
7. **"Tail at Scale invented hedging."** MapReduce backup tasks (2004) and D-SPTF cross-server cancellation (Lumb & Golding 2004, cited in [DB13]) came earlier. [DB13] *named* hedged and tied requests; Finagle's docs say "popularized".
8. **Business-impact figures** ("Amazon: +100 ms → −1% sales"; "Google: +500 ms → −20% traffic").
   - These come from talk slides and blog summaries ([DDIA1] cites Linden's 2006 slides).
   - [DDIA2] drops the Amazon figure and adds a sidebar saying that some often-cited figures are unreliable (paraphrased from the translation). It notes Google's own 2009 experiment found +400 ms → −0.6% searches ([Brutlag 2009](https://services.google.com/fh/files/blogs/google_delayexp.pdf)), and that the Akamai "+100 ms → −7% conversions" study confounds page content with page speed.
9. **"FIFO minimizes tail latency."** This holds for light-tailed service times. It is false for heavy-tailed ones ([Wierman & Zwart 2012]).
10. **"Percentile-based SLAs make Amazon ignore everyone else."** Dynamo's rationale is that the slowest requests are the most *valuable* customers (long histories) ([Dynamo07] §2.2). The p99.99 was rejected on cost-benefit grounds, not because it didn't matter.

## 10. Animation vs doing vs reading

(This section is my pedagogical judgment. It draws on general learning-science findings: animation helps when it is *congruent* with a process that changes over time and is paced so it can be *apprehended* ([Tversky, Morrison & Bétrancourt, *IJHCS* 57, 2002](https://hci.stanford.edu/courses/cs448b/papers/Tversky_AnimationFacilitate_IJHCS02.pdf)), and exploratory interactive simulations help ([Wieman, Adams & Perkins, *Science* 322:682, 2008](https://phet.colorado.edu/publications/PhET_Simulations_That_Enhance_Learning.pdf)).)

| Mode | Best for | Why |
|---|---|---|
| **Narrated animation** | (1) A request fanning out to N leaves, with the root waiting for the last bar to finish. (2) The P(slow) curve rising as N sweeps from 1 to 100 to 2,000, like the [DB13] figure. (3) Message-sequence timelines for hedged, tied and "bad case" requests; [Dean12]'s slides are already built frame by frame. (4) Head-of-line blocking in a queue. (5) Synchronized vs randomized background blips across a grid of machines | These are processes that unfold in time, so motion maps directly onto the concept. Narration can carry the "why" while the eye follows the timeline |
| **Doing** (simulation, code, exercise) | (1) Compute 1 − p^N, then invert it to find the per-leaf percentile needed. (2) Monte Carlo: pick a leaf distribution (bimodal, exponential, lognormal, Pareto) and N, and read off the fan-out p50/p99. (3) Add correlation and watch the i.i.d. formula overestimate. (4) Hedging: vary the delay d and see p99 against the extra-load fraction; raise utilization until duplication stops helping. (5) Measurement lab: average per-host p99s vs merge histograms; closed-loop vs open-loop load generation (coordinated omission) | The quantitative intuitions are counterintuitive and depend on parameters: the effect of shape, the cost/benefit crossover, correlation. Predicting first and then observing exposes wrong intuitions. Exercises (1)–(2) take minutes; (4)–(5) need a sandbox |
| **Reading** | Assumptions and failure conditions (independence, idempotency, correlated slowness). The catalogue of systems and their mechanisms (§8). SLO and measurement practice. Exact formulas and numbers for reference. The 7-page [DB13] paper itself | This is conditional, declarative knowledge that learners come back to and look up. It does not change over time, so animating it adds little |

## Not verified or uncertain (summary)

- The section number of the "tail-tolerance" material in Barroso, Hölzle & Ranganathan, *The Datacenter as a Computer* (2nd ed. 2013 / 3rd ed. 2018). I believe it covers [DB13]'s techniques, but I could not open the text.
- DDIA English wording and headings: checked only through a full translation.
- "TP99" as Amazon terminology.
- The Cassandra version that introduced speculative retry.
- Which example (A or B in §1) is "more common": my judgment.
- Course adoption beyond MIT 6.1800.
- Tene's talk slides: I verified only his 2014 blog post and 2013 list post, not the slide numbers.
