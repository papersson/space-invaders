# Review

## BLOCKING

**Quote:** "Most orders of the six steps are fine. Only some lose a deposit."

**What's wrong:** This is backwards, and checkably so. Label the six steps Ar,Ac,Aw (A's read/add/write) and Br,Bc,Bw, with only the per-thread order fixed. There are C(6,3) = 20 valid interleavings. A result is correct only when one thread's whole read‑add‑write finishes before the other's begins — that's exactly 2 of the 20 (A entirely before B, or B entirely before A). Every other interleaving (18 of 20, i.e. 90%) loses an update, because whichever thread writes last did so from a read that preceded the other thread's write. So the *minority* of orderings are safe, not the majority. This isn't just an imprecision — it's the reverse of the true count, and it directly undercuts the very next beat of the script ("it isn't rare," ~1M of 20M increments lost empirically), which only makes sense if bad interleavings dominate.

**Corrected wording:** "Only two of these orderings are fine — when one machine's whole read-add-write finishes before the other one starts. Every other order of the six steps loses a deposit."

---

**Quote (screen direction):** "Then three checkmarks appear on the diagram as each condition is spoken: 'same balance', 'both write', 'no order', tagged 'data race'."

**What's wrong:** This checklist is meant to visually confirm the general definition just spoken: "Two threads use the same memory. At least one of them writes. And nothing forces an order between them." The middle checkmark should track "at least one of them writes," but it's labeled "both write." As a stand-in for the general condition, "both write" is false: a data race only requires one write plus a concurrent, unsynchronized access (a read-write race is the more common real-world case, e.g. one thread reading a flag another thread writes without synchronization). Labeling the general condition "both write" teaches viewers an incorrect, over-restrictive definition, even though it happens to be true of this specific deposit example.

**Corrected wording:** Change the on-screen tag to "at least one writes" (or "a write happens"), not "both write."

## SHOULD FIX

**Quote:** "By default, a send on a Go channel waits until a receiver takes the value. So when a send finishes, the sender knows its value was taken."

**What's wrong:** This is only true of unbuffered channels. A send on a *buffered* Go channel returns as soon as there's room in the buffer — it does not wait for a receiver, and the sender does *not* know its value was taken. "By default" is doing a lot of unstated work here (relying on the fact that `make(chan T)` with no capacity argument is unbuffered); as phrased, a viewer will reasonably generalize this to "Go channel sends wait for the receiver," which is false for the buffered channels they'll meet in real code. The later side-by-side comparison correctly appends "(unbuffered)," but this first, definitional statement doesn't.

**Corrected wording:** "An unbuffered Go channel — the default if you don't give it a buffer size — blocks the sender until a receiver takes the value. So when a send on one finishes, the sender knows its value was taken."

---

**Quote (screen direction, section 8 table):** "Data race: ... 'ruled out for the actor's own state' / 'ruled out for the owner's state'."

**What's wrong:** This contradicts the correctly hedged narration from the same script two sections earlier: "How firmly 'nothing else' holds depends on the system... In Akka... keeping an actor's state private is up to the programmer" — meaning a data race on an actor's state is still possible in Akka if the convention is broken. Section 8's own narration gets this right ("That holds wherever the language enforces the ownership"), but the summary table drops the caveat and states "ruled out" unconditionally, overclaiming generality for a property that's language/runtime-dependent.

**Corrected wording:** Add the same hedge to the table cells, e.g. "ruled out — where the language enforces privacy (e.g. Erlang; not guaranteed in Akka)."

---

**Quote:** "A program that does several things at once has to coordinate them, and there are two broad ways to do it."

**What's wrong:** Presented as an exhaustive dichotomy. Shared-memory-with-locks and message-passing are the two dominant, classical paradigms and the right choice for this video's scope, but they aren't the only concurrency-coordination models (software transactional memory, lock-free/wait-free algorithms, dataflow, CRDTs). Given the video's own bibliography includes Butcher's *Seven Concurrency Models in Seven Weeks*, a one-clause caveat costs little and avoids overclaiming.

**Corrected wording:** "...there are two broad families for doing it, among others we won't cover here."

## NIT

- **"With a lock around it, the counter reaches twenty million on every run"** paired with on-screen "20,000,000 · 20,000,000 · 20,000,000" (3 runs) vs. five runs shown for the unlocked case. Not wrong, just an unexplained asymmetry in the demo that a careful viewer may notice; consider running the locked case five times too, or note "3 runs" to match the framing of the unlocked demo.
- **"It comes from Tony Hoare's communicating sequential processes, or CSP, and Go's channels come out of this tradition."** Correct but elides that Go's channels descend through Pike's earlier languages (Newsqueak, Alef, Limbo) rather than directly from Hoare's original 1978 process-naming formulation (which didn't use free-standing channel objects). The hedge "come out of this tradition" already covers this adequately; only flagging for completeness, not required.
- Section 7's citation of the Tu et al. results glosses the paper's own bug categories ("blocking"/"non-blocking") as "hung"/"wrong results." This is a reasonable, defensible paraphrase (blocking bugs manifest as hangs; non-blocking bugs manifest as wrong results or crashes) but is worth a final pass against the paper's own tables before the numbers go on screen, since they're quoted to the exact count.

## Not flagged but verified

Arithmetic and empirical figures throughout (150/200, 20M counter target, 10.1M–11.7M range, 989/0 and 482/0 deadlock trial counts, 1,703/0 overdraft counts, 171 = 86+85, 86=69+17, 85=36+49) all check out internally and against the evidence table. Citations (Hoare 1978, Hewitt/Bishop/Steiger 1973, Goetz et al. 2006, Tu et al. ASPLOS 2019, Lauer & Needham 1979, Effective Go's slogan) are correctly attributed. The race-condition/data-race distinction (Regehr-style) is used correctly and consistently, including the (well-executed) check-then-act example in Section 6 that has a race condition with no data race. The lock-ordering deadlock and its fix, and the channel-rendezvous deadlock and its fix, are canonical and correctly described. The duality claim in Section 8 is appropriately scoped ("for coordinating access to shared state") rather than an unqualified equivalence claim.

VERDICT: REVISE
