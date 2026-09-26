# Script Review

## Test 1 — Opening question / closing callback
Opens: *"The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"* Closes: *"So why was the handler's work still running after it returned? ... Give every task an owner, and 'returned' means 'done'."* Near-verbatim echo, one question, one answer. This works well — no finding.

## Test 2 — Chain in one sentence per segment, "and then" count
1. The handler returns at 0.10s but its user-service call runs to 1.00s, and 1,000 requests leave 1,000 tasks running — why, and what would make "returned" mean "done"?
2. A plain call has one way in and one way out so returning means done, **but** doing it sequentially is slow (1.10s).
3. **Therefore** we start tasks concurrently, **but** starting a task splits control and neither `gather` nor await-one-at-a-time brings the second path back, **so** a fix must wait for every task, cancel the rest on failure, and cancel all on giveup.
4. **Therefore** this is `goto` again, and the fix is the same: a block tasks can't outlive.
5. **Therefore** the same handler in a task group meets all three guarantees, measured.
6. **But** the block can only ask — cancellation needs cooperation, covers only tasks started inside it, and says nothing about shared data.
7. **But** this isn't Python-specific — Go's convention (errgroup) gets the same result; Kotlin/Swift/Java build it in.
8. **Therefore** the answer.

**"and then" count: 0.** The whole chain runs on "therefore/but," which is exactly the causal (not additive) spine this test is checking for. No finding.

## Test 3 — Ideas announced vs. derived
Most ideas are earned (the three-part spec in ch.3 is derived from two visibly-failing waiting strategies before the fix is named). One exception: **the exception group** in ch.5 is introduced as "a container that can hold the errors of several tasks" when the demo only ever produces one error — the idea is announced, not motivated by anything visible on screen. See finding #1.

## Test 4 — Setups/payoffs
Working pairs: "two common ways to wait, both leave gaps" → both shown failing; three-item spec (ch.3) → three ticked checkboxes with measured evidence (ch.5); "you can treat it as a black box" (ch.2) → "you can no longer treat a function as a black box" (ch.4); 1.10s (ch.2, naive sequential) → 1.10s again (ch.6, defeated cancellation) — a genuinely nice numeric rhyme.
Weak spot: "a task that never awaits ... keeps running" (ch.6) introduces a second failure mode that's never demonstrated (only the catch-and-retry case is shown). See finding #8.

## Test 5 — Terms before explanation / multiple names
Handled carefully: the script consistently narrates only "task group" (the multi-name spread — nursery/scope — lives in the Argument prose, not the script itself). Terms are explained same-beat they're introduced (`CancelledError`, `errgroup`, `context`). No blocking issue; the exception-group case is more an unmotivated-idea problem (test 3) than a naming problem.

## Test 6 — Numbers
All numbers: 1.00s, 0.10s, 1,000, 1.10s (×2), 0.50s (×2), 1968, 2018, 2016, Python 3.11, 1.2s, JDK 27/28.
**Worth remembering:** 0.10s (what "done" should look like), 1,000→0 (the at-scale proof), 1.10s (the recurring "you're back to sequential" regression number).
**Does no work:** 2016 (Sústrik's coinage year) — a bare citation date, unlike 1968/2018 which earn the "fifty years later" callback. See finding #7.

## Test 7 — Abstraction before the concrete case
Order is correct throughout: the concrete failure (ch.1–3) precedes the `goto` abstraction (ch.4), and the abstraction is immediately re-grounded in code. No finding.

## Test 8 — Wrong intuition
Named directly in the brief: "gather / awaiting each task behaves like a function call — return means done, errors arrive." It is **shown failing concretely**, twice: the 0.10s/1.00s split in ch.1, and again via the Python docs quote and the await-one-at-a-time gap in ch.3. Well executed — no finding.

## Test 9 — Examples named but not understood
Go gets a full worked demo (bare goroutines vs. errgroup, both measured). **Kotlin, Swift and Java get none** — just API names dropped in a closing line and an end-card list, with no illustration of how they deliver the same guarantee. See finding #3.

## Test 10 — On-screen text vs. narration / picture mismatches
Ch.5's ticked checkboxes pair narration with *new* information (measured numbers) — good. Ch.6's three closing labels merely restate the sentence just spoken, adding nothing new. See finding #4. No picture/line mismatches found elsewhere.

## Test 11 — Deletable lines
"a name Martin Sústrik gave it" (ch.4) is attribution trivia that doesn't aid understanding and duplicates the on-screen name list. See finding #5.

## Test 12 — Hard-to-follow sentences / pacing
The bare-except sentence in ch.6 stacks three appositives and is hard to say/parse aloud. See finding #6. Pacing: the third limit in ch.6 (shared-data races/deadlocks) gets one sentence and one label versus full code+timeline treatment for the other two limits — an uneven, slightly rushed beat. See finding #2.

---

## Findings

**1. SHOULD FIX** — Exception group is announced, not derived from a visible problem.
> "It arrives inside an exception group, a container that can hold the errors of several tasks."
Rewrite: cut the unearned claim — *"It arrives wrapped in an exception group, Python's container for a task's error."* — or add a beat where both calls fail together so "several tasks" is actually shown.

**2. SHOULD FIX** — The races/deadlocks limit is asserted, not demonstrated, unlike its two siblings.
> "And it's about lifetimes, not shared data. Two tasks in the same group can still race on a variable, or deadlock."
Rewrite: flag it explicitly as an intentional boundary rather than a rushed aside — *"That's a separate problem, for a separate video: two tasks in the same group can still race on a variable, or deadlock."*

**3. SHOULD FIX** — Kotlin/Swift/Java are named but not understood; no illustration, unlike Go.
> "Kotlin, Swift and Java have the same kind of block built in. Java's is still a preview feature."
Rewrite: tie the names to the mechanism already proven — *"Kotlin's coroutineScope, Swift's task groups, Java's preview StructuredTaskScope: same promise, the block doesn't return until its tasks do."*

**4. NIT** — Ch.6's closing labels restate narration verbatim, adding nothing (contrast with ch.5's checkboxes, which add measured numbers).
> "cancellation: a request, delivered at an await" / "only tasks started inside" / "not about shared data..."
Rewrite: swap at least one for new information, e.g. *"retry loop: handler returns at 1.10 s, not 0.10 s."*

**5. NIT** — Deletable attribution clause.
> "That rule is called structured concurrency, a name Martin Sústrik gave it."
Rewrite: *"That rule is called structured concurrency."* (keep Sústrik on screen only.)

**6. NIT** — Sentence stacks three appositives, hard to say aloud.
> "Here's a retry loop with a bare except, an except with no type, which catches everything, cancellation included."
Rewrite: *"Here's a retry loop with a bare except — no exception type named, so it catches everything, including cancellation."*

**7. NIT** — A number that does no work.
> On-screen: "Sústrik 2016"
Rewrite: drop the year from the on-screen line; it earns no callback the way 1968/2018 do.

**8. NIT** — Setup without a shown payoff.
> "A task that never awaits, or that catches that exception and carries on, keeps running."
Rewrite: cut the "never awaits" clause — it's asserted but never demonstrated; keep the sentence focused on the retry case that is actually shown.

---

VERDICT: PASS
