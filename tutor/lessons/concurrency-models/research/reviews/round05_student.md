# Watching through

## 1. Where I lost the thread

- **"parts of the program pass messages instead... at least in the code you write"** — that qualifier snuck in and I wasn't sure what it was hedging against. Message-passing under the hood might still use shared memory? Left me slightly unmoored right at the setup.
- **"Do not communicate by sharing memory; instead, share memory by communicating."** — cute, but backwards-sounding on first hearing. Only clicked a beat later once "share memory by communicating" mapped onto messages.
- **"Only two orders of the six steps are safe"** — I had to stop and reconstruct "six" myself (3 steps × 2 machines) while the narration had already moved on.
- **"For a program with a data race, C and C++ promise nothing at all, not even that a read returns a value some thread actually wrote."** — this came out of nowhere. Why these two languages specifically, and what does "promise nothing" even cash out to? Felt like a dropped-in fact I couldn't place.
- The five counter numbers (**10.2M, 10.3M, 11.7M, 11.0M, 10.1M**) went by too fast to actually hold onto individually — I retained "landed short of 20M, different each time" but not the specific figures in real time.
- **"Then a cycle of waiting can't form."** — "cycle" is doing real work here (it's the deadlock condition) but it's used like a term I should already have, right after the account-locking example, not before it.
- **"A channel is its own object, passed around between processes, and by default a send waits for the receiver."** — two new facts stacked in one sentence (channel = object vs. actor = address; send waits vs. doesn't) right after I'd just absorbed the actor version. Had to mentally replay it.
- **"an account can hand the send to a helper, a separate goroutine that waits in its place, and keep listening"** — I didn't follow *why* this breaks the cycle. It sounds like the waiting just moved to a different piece of code, not disappeared.
- **"It sends a request, and then won't handle anything else until the reply lands in its mailbox. If two actors do that to each other at the same moment, each waits on the other forever."** — a whole new deadlock scenario introduced in two rushed sentences right before the study numbers, no diagram time to settle.

## 2. Questions I'd ask afterward

- What actually is "undefined behavior" in C/C++ — what does it mean for a program to "promise nothing"?
- The helper-goroutine fix: where did the waiting actually go? Isn't something still blocked?
- Is there a general way to avoid these waiting-cycles, or is "pick one fixed order" the only tool we have, for both locks and channels?
- If message passing still allows race conditions and deadlocks, what's the actual size of the practical win — just that one class of bug (data races) is gone "by construction"?
- How different in practice is "enforced by the language" (Erlang) versus "by convention" (Akka, Go) — does the convention actually get broken often enough to matter?

## 3. What I learned (without looking back, ~150 words)

The video asks whether message-passing (actors, channels) fixes the classic bug where two bank deposits happen at once and one gets lost — a "lost update," which is a race condition and, since it's shared memory with no enforced order, also a "data race." With locks, you fix it by locking around the read-add-write, but locks can deadlock if two threads grab two locks in opposite order — fixed by always locking in a fixed order. Message-passing instead gives a piece of state a single owner (an actor or a process behind a channel), so nothing else can even touch it — that specific bug is gone. But two problems return in new clothes: a race condition when a "check" and an "action" are split into two messages (so both withdrawals can pass a balance check before either executes), and deadlock, when processes or actors wait on each other in a circle over sends or replies.

## 4. Direct answers

- **One main idea:** Giving a piece of state a single owner (message passing) eliminates data races on it by construction — but race conditions and deadlocks aren't automatically solved by either locks or messages; both still require you to decide what happens atomically and to avoid circular waiting.
- **Numbers I remember:** $150 instead of $200 (the opening vanished deposit); ~10–11.7M instead of 20M in the lock-free counter test, fixed to exactly 20M with a lock; 989/1000 deadlocked without a fixed lock order vs. 0/1000 with one; ~1,700 of 100,000 overdrawn with a two-message check-then-withdraw vs. 0 of 100,000 with one combined message; ~482/1000 deadlocked over channels vs. 0/1000 with the helper trick; and from the bug study, message-passing caused about 1-in-5 wrong-result bugs but more than half of hang bugs.
- **Starting question / answer:** Does passing messages make a bug like the vanishing deposit go away? Yes, for that exact bug — but its cousins (split check-then-act, and circular waiting) come back in new forms, so neither model is simply "the safe one."

## 5. Ratings

- **Hook strength (want-the-answer):** 4/5 — the ATM/bank scenario is concrete and I immediately wanted to know how it's normally prevented.
- **How often I felt lost:** a few times — mostly at dense back-to-back-fact sentences (channel vs. actor comparison, the helper-goroutine fix) and the unexplained C/C++ aside.
