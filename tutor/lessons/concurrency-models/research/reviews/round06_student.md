Watching through once, playing the industry-engineer-who-hasn't-studied-this role:

## 1. Where I'd lose the thread

- **"In the other, nothing is shared, at least in the code you write: parts of the program pass messages instead."** — that qualifier "at least in the code you write" is dropped in and never explained at that point. Is memory secretly shared underneath? I'm left guessing until much later (the Go goroutines line in section 5) that this hedge mattered.
- **"Only two orders of the six steps are safe: one machine's whole deposit finishes before the other's starts."** — I can't verify "six steps" or "two orders" in my head fast enough; it's asserted as a fact, not shown. I just have to take it on faith.
- **"A bug whose result depends on the timing of concurrent steps is called a race condition. This bug is also what's called a data race."** — two named concepts arrive back-to-back for the same example. The follow-up (result vs. memory-use) explains it, but on first hearing I momentarily thought "race condition" and "data race" were just two words for the same thing, then had to backtrack.
- **"For a program with a data race, C and C++ promise nothing at all, not even that a read returns a value some thread actually wrote."** — what does a *language* "promising" something mean here? Why C/C++ specifically and not the others? This sounds like it's gesturing at a bigger concept (I'd later learn this is "undefined behavior") that's never named.
- **"A Go channel made without a buffer, which is the default, makes a send wait until a receiver takes the value."** — "buffer" is used as if I already know what a buffered channel is; I can infer roughly what it means from context, but it's never actually defined, just contrasted implicitly.
- **The study numbers in section 7** ("wrong results (86)... hangs (85)... shared memory 36, message passing 49") — right before this, the example was specifically about *deadlocks*. The study talks about "hangs" broadly. I couldn't tell if "hangs" means "deadlocks" or something broader, and the narration doesn't say.

## 2. Questions I'd ask afterward

- Is "data race" always a subset of "race condition," or can you have one without the other in some other example?
- What actually happens when C/C++ code has a data race, concretely — does it crash, give garbage, or something worse?
- What's a "buffer" on a channel, and what changes if you add one?
- In the Go bug study, does "hangs" mean deadlocks specifically, or other kinds of freezes too?
- If both locks and messages leave "which steps are atomic" and "no waiting cycles" up to the programmer, is either model actually *safer* in practice, or just differently shaped?

## 3. What I learned (written without looking back, ~150 words)

Concurrent programs can lose data when two threads read-modify-write the same value without coordination — like two ATM deposits where one just vanishes because both machines read the old balance before either writes back. This is called a race condition, and when it involves shared memory being written without ordering, it's specifically a data race. Locks fix this by serializing access, but locking multiple resources in different orders across threads can cause deadlock, where each side waits on a lock the other holds. Message-passing (actors, channels) avoids data races by giving each piece of state a single owner that processes messages one at a time — but it doesn't remove race conditions (e.g., check-then-act sequences split across two messages) or deadlocks (two processes waiting to send to each other). Neither model eliminates the underlying design questions; they just change where you have to think about them.

## 4. Direct answers

- **Main idea:** Giving a piece of shared state a single owner (via message passing) eliminates data races on that state by construction, but it does *not* eliminate race conditions (like check-then-act bugs) or deadlocks — those require separate design discipline no matter which model you use.
- **Numbers I remember:** the two-ATM example (100 → should be 200, ends at 150); the counter test (expected 20 million, actual runs landed around 10–11.7 million without a lock, exactly 20 million with one); the withdrawal race (overdrawn ~1,700 out of 100,000 runs with two messages, 0 out of 100,000 with one combined message); and the real-bug study, where message passing caused about 1 in 5 wrong-result bugs but over half of hang bugs.
- **Question it started with / answer:** "Does passing messages make concurrency bugs like the vanishing deposit go away?" Answer: yes for that specific bug (lost updates/data races on owned state), but no for its relatives (race conditions and deadlocks) — those persist in a different form.

## 5. Ratings

- **Pull of the opening (1-5): 4** — a concrete, relatable bug (money vanishing from a bank account) with a clear "why did this happen" hook made me want the explanation.
- **How often I felt lost:** a few times — mainly around the race-condition/data-race distinction landing too fast, the unexplained "six steps" claim, and the undefined "buffer"/"promise nothing" jargon.
