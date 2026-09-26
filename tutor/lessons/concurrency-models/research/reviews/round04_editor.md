# Script Review

## 1. Opening question answered at the end, with callback

Ch1 asks: *"So does passing messages make bugs like the vanishing deposit go away?"* Ch8 opens by repeating that exact question and answering it ("Yes... that bug can't happen"), and the screen literally replays the ch1 scene (two deposits into the actor, landing on $200 instead of $150). Clean, explicit callback — **passes**.

## 2. Chain test ("but"/"therefore"/"and then")

The author's own Chain section already does this (steps 1–8, joined only by "therefore" and "but"). I searched the script prose itself for "and then" — **zero literal occurrences found**. Nothing to report here.

## 3. Ideas announced vs. derived from a visible problem

Most transitions are earned: the lock (ch3) is derived from the shown lost-update; "one owner" (ch4) is derived from the shown "forgotten lock" path; the race condition in ch6 is derived from a shown withdrawal failure. Two exceptions:

- **SHOULD FIX** — *"But because an actor's send doesn't wait, a cash machine never learns when its request was taken."* (ch5 opening) This motivates channels via a claimed shortcoming of actors that is never shown mattering — no scenario where "not knowing" causes a problem. It reads as an asserted transition, not a derived one.
  **Rewrite:** Motivate it from the deadlock side instead, since that's where it actually pays off later: *"Actors guarantee delivery, not confirmation. The other message-passing family is built so a sender can know its message was received."*

- **SHOULD FIX** — *"Go's own advice is to use whichever is most expressive, or simplest, for the job: channels to hand work or data from one part of a program to another, and a lock to guard shared state, like a cache."* (ch8, final lines) This is a new criterion (expressiveness/simplicity) and a new unexplained example (cache) that arrives after the argument has already concluded, not derived from anything shown. See #11.

## 4. Setups without payoffs / payoffs without setups

- **Setup without payoff (SHOULD FIX)** — *"A channel can also be given a buffer; then a send waits only when the buffer is full."* (ch5). Buffering is never used again — ch7's deadlock and ch8's table both rely only on unbuffered "send waits for receiver." It's a fact introduced and dropped.
  **Rewrite:** cut the sentence; it adds nothing the rest of the video needs.

- **Payoff without setup (SHOULD FIX)** — *"It sends a request, then waits for the reply to arrive in its mailbox."* (ch7). Ch4 established actors by "Sending doesn't wait" as a defining property. This reuses the word "wait" for a different thing (the actor's own handling blocks on its mailbox) without flagging the distinction, right before using it to build a deadlock claim.
  **Rewrite:** *"But often an actor needs an answer, not just delivery. It sends a request and then pauses its own turn — it won't handle anything else until the reply lands in its mailbox. If two actors do that to each other at once, each is paused waiting on the other."*

## 5. Terms before explanation / concepts with two names

Handled well overall — "data race" vs. "race condition" is explicitly taught as two names for two different things (ch2), and CSP, goroutines, mailbox are all defined at first use. No findings.

## 6. Numbers: which 2–3 matter, which do no work

**Worth remembering:**
- $150 vs. $200 (the hook and the ch8 callback)
- 989→0 of 1,000 deadlocked runs, with vs. without fixed lock ordering (ch3)
- Message passing causes ~1 in 5 wrong-result bugs but >half of hang bugs (ch7 study) — the empirical crux of the takeaway

**Numbers doing no work:**
- **NIT** — *"Only two orders of the six steps are safe"* (ch2). Adds combinatorial precision ("six steps," "two orders") that's never enumerated or used again — false precision.
  **Rewrite:** *"The deposit is only safe if one machine's whole read-add-write finishes before the other's starts — interleave them any other way, and a deposit is lost."*
- **NIT** — five separately labelled counter-run bars (10.2M/10.3M/11.7M/11.0M/10.1M) on screen, when the spoken line already compresses this to a range. Three bars would make the same point with less clutter.

## 7. Abstraction before the concrete case

Mostly good (ch1 shows the concrete deposit bug before naming the two families). One inversion:

- **NIT** — *"It comes from Tony Hoare's communicating sequential processes, or CSP... Processes share nothing, and talk over channels. A channel is a connection..."* (ch5). The historical label arrives before the concrete definition of what a channel does.
  **Rewrite:** *"Processes share nothing, and talk over channels: a channel is a connection that processes send values into and receive them from. This comes from Tony Hoare's communicating sequential processes, or CSP — Go's channels come out of that tradition."*

## 8. The wrong intuition — is it shown failing?

Wrong model: "message passing is simply the safe model." Ch6 states it plainly ("it looks like the slogan wins... For deposits, that's true. Now try withdrawals") and then shows it failing concretely with run counts (1,703/100,000 overdrawn), and ch7 does the same for deadlock (482/1,000 stuck). This is well executed — **passes**.

## 9. Examples named but not understood

Erlang and Akka are named *and* given a distinguishing one-liner each ("messages are copied, shared tables opt-in" vs. "by convention"), which pays off again in the ch8 table. No findings.

## 10. On-screen text vs. narration; pictures vs. lines

- **NIT** — the ch2 checkmarks ("same balance," "at least one writes," "no order") closely mirror the spoken sentence clause-for-clause rather than adding independent information.
  **Rewrite:** compress to bare terms ("shared · write · unordered"), or replace the text checklist with the timeline itself lighting up the two unordered accesses.

Elsewhere (ch3's "989→0" caption, ch7's fraction labels) the screen adds precision the narration doesn't state aloud — good complementary use, no issue.

## 11. Deletable lines

- **NIT** — *"there are others, but these are the two you'll meet most"* (ch1) — a hedge that could be cut to *"There are two broad families of ways to do it."*
- **NIT** — *"It's a real gain, and it's why the slogan exists."* (ch8) — restates what the prior sentence already established.
- **SHOULD FIX** — the entire final "Go's own advice..." sentence (ch8). The argument already closed the loop on ch1 and delivered the takeaway table one beat earlier; this coda reopens with an unearned new criterion and an unexplained "cache" example.
  **Rewrite:** end on: *"...and keep waits from forming a cycle. Not a safe model and a risky one — two different sets of decisions to get right."*

## 12. Hard-to-say sentences / rushed or padded beats

No individual sentence is unspeakable, but **ch5 is the most crowded segment**: CSP/Hoare attribution, unbuffered channel behavior, the (unpaid) buffered aside, the Go-goroutines-share-memory caveat, and the actor-vs-channel plumbing comparison all land in one chapter. Cutting the buffered-channel aside (#4 above) is the cheapest fix and would ease the pacing here. No beat felt padded except the ch8 coda already flagged.

---

**Summary of findings:**
- SHOULD FIX (4): unpaid buffered-channel aside; tacked-on Go-advice coda; unexplained actor "waits for reply"; ch5 channel-motivation asserted rather than derived
- NIT (6): "six steps/two orders" framing; CSP-before-definition ordering; ch2 checkmark redundancy; ch1 hedge clause; ch8 filler line; five-bar visual clutter

None break the opening/ending callback, the wrong-intuition confrontation, or the objectives — all SHOULD FIX items are tightening notes, not structural breaks.

VERDICT: PASS
