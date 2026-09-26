# Script Review

## Test 1 — Opening/ending callback
**Pass, strongly.** Ch.1 asks "does passing messages make bugs like the vanishing deposit go away?" Ch.8 opens its answer with the identical phrase — "So does passing messages make the vanishing deposit go away? Yes" — and the screen direction literally restages the ch.1 visual (two deposits, now landing correctly at $200). This is as tight a callback as you'll get.

## Test 2 — Chain as one sentence per segment, joined by but/therefore/and-then
The author's chain mostly holds together causally. One joint is weaker than the rest:

- Seg 4→5 ("give the balance one owner... An actor handles one message at a time" → "CSP channels reach the same place... Same idea, different plumbing") is not a **but** or **therefore** — it's an **and then**: channels don't advance the stakes, they restate the same conclusion through different plumbing. That's fine per Objective 3 (you do need to describe both), but it's the one place the throughline pauses rather than tightens.
- Literal "and then" in the script text: exactly one instance — ch.7, "It sends a request, and then won't handle anything else until the reply lands." This is a real temporal sequence, not a weak causal stand-in, so it's not a problem.

**SHOULD FIX** — Ch.5's transition. *Quote:* "CSP channels reach the same place: a process owns the balance and receives from a channel; the sender waits for the receiver. Same idea, different plumbing." *Rewrite:* Give it a "but" hook tied to the next chapter instead of a flat restatement, e.g. "The actor got there without ever making the sender wait — but what if the sender needs to know its message landed?" — this turns ch.5 into the setup for ch.6's motivating question rather than a parallel aside.

## Test 3 — Ideas announced vs. derived from a shown problem
Derived well: single-owner (posed as a question right after the "forgot the lock" failure), lock ordering (after the deadlock demo), one-message check+act fix (after the overdraw demo), helper-goroutine fix (after the channel-deadlock demo).

**SHOULD FIX** — the reason channels exist is asserted, not shown failing. *Quote:* "because an actor's send doesn't wait, a cash machine never learns when its request was taken." No bug or visible cost of this is ever demonstrated (unlike every other transition in the script, which follows a shown failure). *Rewrite:* Add one concrete beat — e.g., "The mailbox took the message. Did the deposit already land, or is it still queued? The actor never says." — so the motivation is a shown gap, not a stated one.

## Test 4 — Setups without payoffs / payoffs without setups
- Payoff with setup, done well: the Go slogan (ch.1) → returned to and complicated in ch.8 ("Even the Go documentation that gives the slogan adds that it can be taken too far").
- **NIT** — dangling setup: "There are two broad families of ways to do it; there are others, but these are the two you'll meet most." "Others" is never named or returned to. Cuttable (see Test 11).

## Test 5 — Terms used before explained / concepts with two names
All key terms (data race, race condition, CSP, goroutines) are defined at first use. The video is explicitly careful about "race condition" vs. "data race" being two different things applied to the same bug — that's a strength, not a flaw.

**NIT** — the check-then-act pattern demonstrated in ch.6 is a textbook-named idea (TOCTOU / check-then-act) that's never given a name on screen or in narration, despite the video naming everything else it introduces ("lost update," "data race," "deadlock"). Naming it would make it as memorable as the others. *Rewrite (add one clause):* "...still races: a race condition without a data race — the classic check-then-act."

## Test 6 — Numbers
All numbers: $50/$50 deposits, $100 start, $150 actual, $200 expected; 10M increments ×2 = 20M expected, 5 runs (10.2M/10.3M/11.7M/11.0M/10.1M); locked run = 20M ×3; deadlock test 1000 runs, 989 stuck → 0; withdrawal test 100,000 runs, ~1,703 overdrawn → 0; channel-deadlock test 1,000 runs, ~482 stuck → 0; Tu et al. study: 171 bugs, wrong-results 86 (shared 69 / messages 17), hangs 85 (shared 36 / messages 49).

**Worth remembering (2–3):** $150 vs. $200 (the whole video's anchor image); the Go study's "1 in 5" vs. "more than half" (the actual takeaway — message passing shifts bug type, doesn't remove it); arguably the 989→0 or 1,703→0 pair as the one concrete "here's what a fix buys you" number, but only one of the three needs to stick.

**NIT** — numbers that do no work: the five individual counter-run values (10.2M, 10.3M, 11.7M, 11.0M, 10.1M) are spoken as a range anyway ("between about ten point one and eleven point seven million"); the five precise on-screen bar labels add visual precision the argument doesn't need. Three bars, or the range only, would do the same job with less clutter.

## Test 7 — Abstraction before the concrete case
No violations found. Ch.1 leads with the concrete deposit before naming "two broad families." Ch.4's "single owner" abstraction is posed as a question growing directly out of the concrete forgotten-lock failure. Ch.8's synthesis abstraction correctly comes last, after all concrete cases.

## Test 8 — Wrong intuition: named, and shown failing?
Wrong intuition per the brief: "message passing is simply the safe model." It is **shown failing** convincingly — the overdraft race (ch.6), the channel deadlock and actor request-reply deadlock (ch.7), and the Tu et al. stats all directly refute it, and ch.8 states the refutation plainly ("neither model is simply the safe one").

**SHOULD FIX** — the misconception itself is never stated on-screen; it's only implied via the Go slogan and a question. *Quote:* "So does passing messages make bugs like the vanishing deposit go away?" *Rewrite:* Consider one added clause making the naive belief explicit before the question, e.g. "Say goodbye to shared memory, the thinking goes, and you say goodbye to this class of bug entirely. Does it?" — gives the video a clearer thing to knock down.

## Test 9 — Named but not understood examples
Erlang and Akka are both given enough mechanism to be understood, not just named. 

**NIT** — the six Go projects (Docker, Kubernetes, etcd, CockroachDB, gRPC, BoltDB) are named on screen but none is individually grounded with even one concrete bug; they function as an authority/scale signal rather than understood examples. Either drop the full list in favor of "six widely used Go projects" (already said in narration) or pick one concrete bug from one project to make the study land as a story, not just a citation.

## Test 10 — On-screen text repeating narration / pictures not supporting the line
**SHOULD FIX** — a recurring pattern: chapters 2, 4, 5, and 8 each close with an on-screen caption that closely paraphrases the sentence just spoken (e.g., ch.4's "Erlang: by default... / Akka: by convention" right after narration says the same in full sentences; ch.5's "actor: address + mailbox, send doesn't wait / channel: ... send waits for the receiver" mirroring the preceding two sentences almost verbatim). Individually minor, but as a pattern across four chapters it's worth trimming — captions should carry the *term*, not restate the *sentence* (e.g., just "Erlang: default" / "Akka: convention").

**SHOULD FIX** — unclear annotation. *Quote (ch.8 screen direction):* "the chapter 1 scene: two deposits into the actor, balance $200 (ICE)." "(ICE)" is undefined anywhere in the script and reads like a leftover shorthand (a color note? an abbreviation?) rather than a finished direction. Whoever builds the visual needs this resolved or it risks producing an unintended image for the video's final payoff shot.

## Test 11 — Deletable lines
- "There are two broad families of ways to do it; there are others, but these are the two you'll meet most." (ch.1) — never paid off; cuttable (see Test 4).
- **SHOULD FIX** — "A lost update is the mild outcome. For a program with a data race, C and C++ promise nothing at all, not even that a read returns a value some thread actually wrote." (ch.2). This introduces two languages (C, C++) that never appear again in a script otherwise built entirely on Go/Erlang/Akka. It's true and interesting but a pure digression from the throughline; the counter-run evidence right after it already makes the "this is a real, severe bug" point on its own. Cut it, or fold the "no guarantees at all" idea into a single clause about the counter example instead of a separate aside.

## Test 12 — Sentences hard to follow aloud / pacing
**SHOULD FIX** — numeric overload in the central race-condition demo. *Quote (ch.6):* "The balance is one hundred. Machine A asks, and hears one hundred. Machine B asks, and also hears one hundred. Both send 'withdraw one hundred'." Four consecutive "one hundred"s referring to two different things (balance vs. withdrawal amount) risk blurring by ear even with on-screen support, in the chapter carrying Objective 4's key demonstration. *Rewrite:* change the withdrawal amount to a different number (e.g., "withdraw seventy") so balance and request are acoustically distinct throughout.

**NIT** — a dense, clause-heavy sentence. *Quote (ch.7):* "Here, an account can hand the send to a helper, a separate goroutine that waits in its place, and keep listening, instead of waiting in the middle of a transfer." *Rewrite:* split — "Here, the account hands the send to a helper — a separate goroutine that waits in its place. The account itself keeps listening instead of waiting in the middle of a transfer."

**SHOULD FIX** — abrupt segue. *Quote (ch.7):* "...each waits on the other forever. A study of real concurrency bugs in six widely used Go projects sorted them two ways." The jump from the actor request-reply example straight into the Tu et al. citation has no bridge; it reads like two adjacent facts rather than one building on the other. *Rewrite:* "This isn't a hypothetical: a study of real concurrency bugs in six widely used Go projects found exactly this pattern at scale."

Pacing otherwise: chapter length tracks argument weight reasonably well; the three parallel "buggy-rate → 0" empirical beats (lock/counter, withdrawal, channel deadlock) are a deliberate and effective repeated structure, not padding.

---

VERDICT: PASS
