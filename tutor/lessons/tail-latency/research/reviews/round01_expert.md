Verified the core arithmetic (0.99¹⁰⁰≈0.366, 1−0.366=63.4%, mean≈19.9ms) and cross-checked the script against my knowledge of Dean & Barroso, "The Tail at Scale" (CACM 56(2), 2013). Findings below.

## Findings

**BLOCKING**

- **Quote:** "The more servers a page calls, the more its users see the servers' slowest calls, which is why they're called the tail." (Section 3)
  **Problem:** This misattributes the origin of the term "tail latency." The name comes from the shape of a *single* server's latency distribution — the long right tail of rare, extreme response times — not from the fan-out amplification effect. A server has "tail latency" even with zero fan-out; what fan-out does is make hitting that tail *likely*, which is a distinct point the script has already made correctly in Section 2. As written, a viewer would walk away thinking "tail" is defined by the multi-server effect, which is the opposite of how the source paper (and the field) uses the term, and is exactly the kind of definitional slip a professor teaching this paper would flag.
  **Corrected wording:** "This is what's meant by *tail latency* — the rare, long response times in the tail of each server's own latency distribution. The more servers a page calls, the more likely it is to be dragged down by one of these tail events."

**SHOULD FIX**

- **Quote:** "A call that hit a hiccup is usually rescued by the copy, because the second server is rarely stalled at the same moment." (Section 5), read together with Section 4's causes: "A background job, or another program on the same machine, borrows the disk or the processor for a moment."
  **Problem:** The hedging benefit silently re-invokes the independence assumption that Section 2 flagged in fine print, but Section 4 just finished describing causes (shared machines, shared racks/network gear) that are precisely the kind of thing that *correlates* hiccups across servers. The paper itself explicitly warns about this (correlated latency undermines hedging, and recommends routing hedges to replicas that don't share the failure domain). Leaving this out lets viewers conclude hedging always rescues a stalled call, which isn't true when the stall is systemic (a congested rack switch, a synchronized GC pause across colocated processes, a datacenter-wide event).
  **Corrected wording:** Add after that sentence: "This assumes the two servers' hiccups aren't correlated — hedging to a replica sharing the same rack or network path won't help if the whole rack is congested."

- **Quote:** "The standard technique is the hedged request." (Section 5)
  **Problem:** Overstates hedged requests as *the* technique. The source paper presents hedged requests as one of several named techniques for tolerating tail latency (alongside tied requests, micro-partitioning, canary requests, selective replication, and cross-request adaptations like latency-induced probation). Calling it "the standard technique" implies it's the field's singular go-to fix rather than one well-known tool among several.
  **Corrected wording:** "One standard technique is the hedged request."

- **Quote:** "Only the slowest five percent of calls get a copy, so the servers see about five percent more work." (Section 5)
  **Problem:** The paper's own claim is "fewer than 5% of requests trigger a hedged request" — an upper bound, not an approximate midpoint. "About five percent" reads as a point estimate and slightly overstates the cost.
  **Corrected wording:** "...so the servers see well under five percent more work."

- **Quote:** on-screen fraction-of-slow-pages table: "1%, 10%, 39%, 63%" (Section 3), vs. the evidence table's computed values "1% / 9.6% / 39.5% / 63.4%"
  **Problem:** Inconsistent rounding convention: 39.5%→39% and 63.4%→63% are truncated down, but 9.56%→10% rounds up, breaking the pattern and slightly overstating the N=10 case (true value 9.6%).
  **Corrected wording:** Show "1%, 9.6%, 39.5%, 63.4%" (or truncate all four consistently to "1%, 9%, 39%, 63%").

**NIT**

- **Quote:** "send a copy to a second server that holds the same data" (Section 5)
  **Problem:** Implicitly scopes hedging to idempotent reads (fine), but never states this — a viewer could assume hedging applies unchanged to writes, where duplicate execution needs dedup/idempotency handling. Worth a half-clause given how load-bearing this technique is to the video's conclusion.
  **Corrected wording:** "...send a copy to a second server that holds the same data (this works cleanly for reads; writes need separate handling to avoid double effects)."

- **Quote:** "reading a thousand values spread over a hundred servers, hedging after ten milliseconds cut the slowest tenth of a percent of reads from 1.8 seconds to 74 milliseconds, and sent only two percent more requests" (Section 5)
  **Problem:** Not incorrect as far as I can verify from recollection of the paper, but this is the single most load-bearing external citation in the script and I could not run a live check against the primary source in this pass (no search access available). Flagging so it gets a source-page check (CACM 56(2), 2013, "Within-request short-term adaptations" / hedged requests discussion) before production.

## Not flagged (checked and fine)
- 0.99¹⁰⁰ ≈ 0.366, 1−0.366 = 63.4% — arithmetic correct.
- Average ≈ 19.9ms ≈ 20ms from 0.99×10 + 0.01×1000 — correct.
- Percentile definitions (p99, p95) — standard and correctly stated.
- Paper title, authors, venue, volume/issue — correct.
- "Busier servers are slower" / M/M/1 queueing aside — standard, correctly used as informal caveat, not overclaimed.
- End-card model P(page fast) = pᴺ with explicit independence caveat — appropriately scoped.

VERDICT: REVISE
