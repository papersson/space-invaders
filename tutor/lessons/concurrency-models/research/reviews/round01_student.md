## 1. Points where I'd lose the thread

- **"race condition" vs "data race" back-to-back** — *"A bug whose result depends on the timing of concurrent steps is called a race condition. This one has a more specific name... That's a data race."* Two similar-sounding terms introduced in consecutive sentences. I can repeat both definitions but I'm not 100% sure of the relationship — is data race a subset of race condition, or a separate cousin? The word "more specific" implies subset, but it goes by fast.

- **The dense data-race definition itself** — *"Two threads use the same memory, at least one of them writes, and nothing forces an order between them."* Three conditions in one breath (shared memory + a write + no ordering). I'd have to replay this to actually check a case against it.

- **"A lock can be written as a process that hands out permission"** — in the wrap-up. This is asserted as if obvious, but nothing earlier showed a lock built out of message-passing. I'd nod along but couldn't explain it back.

- **The "ask" pattern for actors** — *"as soon as an actor sends a request and waits for the reply, two actors asking each other can wait forever."* Earlier I was told actors never block on send ("sending doesn't wait"). Now an actor is "waiting for the reply" — that sounds like blocking. I can't tell if "ask" is a different, new mechanism or a contradiction of the earlier rule.

- **"forty-nine of eighty-five"** — I never heard where 85 came from. (I can see on screen it's 36+49, but if I were only listening, that denominator arrives with no stated meaning.)

- Similarly, the study cites "171 bugs" up front, but the breakdown numbers (69/17 and 36/49) are never added back up to 171 in the narration — I'd have to trust it adds up rather than hear it confirmed.

## 2. Questions I'd ask afterward

- Is every data race a race condition, or are they just overlapping categories?
- If locks and channels can each simulate the other, is there ever a *correctness* reason to pick one over the other, or is it purely a style/readability choice?
- What exactly is "ask" for actors — is it a built-in wait-for-reply primitive, or something people bolt on themselves?
- In the Go bug study, were "hangs" and "wrong results" the only two bug categories, or are there others not shown?
- Does a fixed lock-ordering rule scale when the number of shared resources gets large (hundreds of accounts), or is that where it stops being practical?

## 3. What I learned (written without looking back)

Concurrent programs can corrupt shared state when two threads read-modify-write without coordination — a "lost update." Locks fix this by making a sequence atomic, but locks can deadlock if two threads grab shared resources in opposite orders; the fix is a fixed acquisition order. The alternative is message passing (actors, or channels/CSP from Hoare), where a single owner holds the state and processes messages one at a time, which structurally rules out data races on that state. But message passing doesn't rule out race conditions — you can still read-then-act across two messages and get a stale answer (e.g., an overdrawn withdrawal), fixed by combining check-and-act into one message. And message passing can still deadlock if two owners wait on each other. A real bug study found message-passing systems had fewer "wrong result" bugs but more "hang" bugs than lock-based ones.

## 4. Main idea / numbers / question-answer

- **One main idea**: giving a piece of state a single owner (lock or actor/channel) prevents data races by construction, but neither approach eliminates the two harder design decisions — what counts as "one atomic step," and how to avoid a waiting cycle (deadlock).
- **Numbers I remember**: the two-machines-$50-each example landing at $150 instead of $200; the shared counter test landing around 10–13 million instead of 20 million; withdrawals overdrawn in about 1,700 of 100,000 runs with check-then-act, vs 0 with one combined message; deadlocks in ~992 of 1,000 runs without ordered locks, 0 with ordering.
- **Opening question**: does passing messages instead of sharing memory make concurrency bugs like the vanishing deposit go away?
- **Answer**: partially — it eliminates data races on owned state, but race conditions (stale reads across messages) and deadlocks (waiting cycles) can still happen; you still have to decide what's atomic and make sure waits can't cycle.

## 5. Ratings

- **Want-the-answer after the opening**: 4/5 — the vanishing $50 is a concrete, surprising hook.
- **How often I felt lost**: a few times — mainly the data-race/race-condition naming, the "ask" blocking contradiction, and the unexplained "85" in the bug-study numbers.
