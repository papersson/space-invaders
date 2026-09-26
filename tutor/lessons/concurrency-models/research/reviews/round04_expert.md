Reviewed the whole script line-by-line against the evidence table: re-derived the interleaving count (C(6,3)=20, only 2 safe) myself, re-checked every percentage and rounded figure against the raw numbers in the evidence table, and checked every named model/definition against its canonical source. Findings below, ordered by appearance.

---

**1. BLOCKING — Section 5**
> "Go also lets its goroutines, its lightweight processes, share memory."

What's wrong: throughout sections 4–5 the script uses "process" specifically to mean *an isolated unit that does not share memory* — "In Erlang, processes don't share memory by default" (§4), "Processes share nothing, and talk over channels" (§5). Calling a goroutine a "process" in the very sentence that says it *does* share memory contradicts the meaning the script itself just assigned to that word — a viewer who was tracking "process = no shared memory" will read this as a contradiction, not a caveat. It's also non-canonical on its own terms: Go's documentation (A Tour of Go) calls a goroutine "a lightweight thread managed by the Go runtime," and Effective Go — already quoted verbatim in §1 — explicitly says the name "goroutine" was chosen *to avoid* the connotations of "threads, coroutines, processes, and so on." So the script both misuses its own established vocabulary and contradicts the source it quotes elsewhere.

Corrected wording: "Go also lets its goroutines, its lightweight threads, share memory." (or drop the appositive entirely: "Go also lets its goroutines share memory.")

**2. SHOULD FIX — Section 5, closing line**
> "A channel is its own object, passed around between processes, and a send waits for the receiver."

What's wrong: two sentences earlier the script correctly says a buffered channel's send "waits only when the buffer is full." This closing generalization drops that qualifier, so as stated it's false for buffered channels — only the unbuffered (default) case blocks the sender until a receiver takes the value.

Corrected wording: "A channel is its own object, passed around between processes, and a send to an unbuffered channel waits for the receiver."

**3. NIT — Section 4**
> "A message is copied to the receiver."

True as the general/default description, but BEAM refcounts binaries larger than 64 bytes rather than copying them on send — sharing without copying, safe only because such binaries are immutable. Doesn't affect the argument (immutability, not copying per se, is what rules out the race), so it's a footnote-level precision gap, not an error.

**4. NIT — Sections 4–5**
"Process" is reused for three different things across the video — an Erlang process (an actor), a CSP/Go "process" that owns a channel, and (only by omission/contrast) an OS process — without ever flagging that it's the same word for different things. A single clause acknowledging the overload (e.g., when introducing Erlang's processes) would preempt confusion, especially given finding #1.

**5. NIT (optional) — Section 3**
The video's shared-memory "fix" for the counter example is a full mutex; it never mentions a lock-free atomic increment/CAS, which is the far more common real-world answer to exactly the plain-counter case shown (a mutex is the right call for the multi-step balance example, less so for a bare counter). This is a defensible scope choice given the video's explicit two-family framing, so it's low priority, but worth a single clause if room allows.

---

Everything else checked out: the six-step interleaving count (2 safe of 20, confirmed by hand-derivation), all percentage/count claims (10.1–11.7M counter runs, 20M with lock, 989/1000 and 0/1000 lock-ordering, 1,703/100,000 and 0/100,000 check-then-act, 482/1000 and 0/1000 channel deadlock, 17/86≈1-in-5 and 49/85>half from Tu et al.), the race-condition/data-race distinction, the C/C++ undefined-behavior claim (correctly scoped to those languages only), the Erlang/Akka/Go ownership-enforcement caveats, the CSP/actor lineage claims, and all citations (Hoare 1978, Hewitt et al. 1973, Goetz et al. 2006, Tu et al. 2019, Lauer & Needham 1979, Butcher 2014 chapter mapping) are accurate and appropriately hedged — no overclaiming about optimality or generality found elsewhere.

VERDICT: REVISE
