# Review

I checked every numerical claim against the evidence table (all arithmetic verifies, including the non-obvious combinatorial claim about the six-step interleaving — see below), the terminology against standard sources (JCIP, the Go memory model, Regehr's race-condition/data-race distinction, Hoare 1978, Hewitt et al. 1973, Tu et al. 2019), and the historical/attribution claims. This is an unusually careful script — I did not find any BLOCKING errors. Below are the smaller issues worth fixing before production.

**Verified correct and worth noting (no action needed, since I initially suspected these might be wrong):**
- "Only two orders of the six steps are safe" (§2) is exactly right: of the C(6,3)=20 valid interleavings of the two 3-step sequences, only the two fully-sequential orderings avoid a lost update — I re-derived this from scratch and it holds.
- All simulation figures (counter runs, lock/deadlock counts, race-condition counts, Tu et al. ratios) match the evidence table and the spoken rounding ("about seventeen hundred" for 1,703; "about one in five" for 17/86 ≈ 19.8%; "more than half" for 49/85 ≈ 57.6%) is accurate.
- The data-race vs. race-condition distinction, the C/C++ UB claim, and the Erlang/Akka/Go enforcement-vs-convention nuance are all correctly scoped and hedged — none overclaim generality.

**SHOULD FIX**

1. Quote: *"In Akka, a library for Java and Scala, keeping an actor's state private is up to the programmer."*
   Issue: Akka is standardly described as a toolkit/framework (it bundles a runtime, scheduler, clustering, persistence, etc.), not a "library" — Akka's own docs call it "a toolkit for building highly concurrent, distributed, and resilient message-driven applications."
   Corrected wording: *"In Akka, a toolkit for Java and Scala, keeping an actor's state private is up to the programmer."*

2. Quote: *"The account becomes a process that owns the balance, and receives deposits from a channel, one at a time... Go also lets its goroutines, its lightweight threads, share memory."*
   Issue: "process" is used here in the generic CSP sense, but the term switches to "goroutine" two sentences later without a bridge. Since §4 used the concrete term "actor" for the analogous role, a viewer could momentarily read "process" as an OS process rather than the CSP abstraction Go's goroutines implement.
   Corrected wording: *"The account becomes a process — in Go, a goroutine — that owns the balance, and receives deposits from a channel, one at a time."*

**NIT**

3. Quote: *"In Akka, a library for Java and Scala..."*
   Akka moved to the Business Source License in 2022; the Apache-licensed continuation is Pekko. This doesn't affect the concurrency lesson at all, but if the video is meant to reflect current practice, a passing mention (or swapping the example to Pekko/Erlang only) keeps it from looking dated.

4. Quote: *"Go also lets its goroutines, its lightweight threads, share memory."*
   "Lightweight threads" is a common simplification but glosses over the M:N scheduling (goroutines are multiplexed onto OS threads by the Go runtime). Fine for this audience level; flagging only because it's the one place the script is slightly looser than its otherwise careful terminology elsewhere.

None of these affect correctness of the concurrency content, the numbers, or the citations — they're polish items.

VERDICT: PASS
