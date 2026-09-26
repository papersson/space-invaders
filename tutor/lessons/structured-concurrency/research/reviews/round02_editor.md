# Script Review

## 1. Opening question / closing callback
**Pass, cleanly.** Ch1 ends: *"The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"* Ch8 opens by repeating it near-verbatim and closes with *"Give every task an owner, and 'returned' means 'done.'"* Direct lexical callback, no drift. Nothing to fix.

## 2. Segment chain (but / therefore / and then)
The author's own Chain section already does this exercise, and it holds up:
1. Question → 2. Therefore (sequential is correct **but** slow) → 3. Therefore (tasks split control) → 4. Therefore (this is goto; the fix is a block) → 5. Therefore (task group demo) → 6. But (limits: cooperation, scope, races) → 7. But (not just Python) → 8. Therefore (answer).

**"and then" count: zero.** Every joint is "but" or "therefore" — good, no padding-by-sequence.

- **NIT** — Step 7's connector is labeled "but," but the content isn't a contrast to step 6, it's a generalization ("this pattern recurs elsewhere"). Quote: *"But this isn't a Python quirk"*. A truer connector is "and": the limits (6) and the cross-language recurrence (7) are both consequences of the same rule, not opposed to each other. Rewrite: *"And it isn't a Python quirk either: …"*

## 3. Ideas announced vs. derived
- **SHOULD FIX** — *"It arrives wrapped in an exception group, a bundle of errors, because in general more than one task can fail."* Nothing in the video ever shows two tasks failing at once — the demo has exactly one failure (orders) plus one cancellation (user). The justification is asserted, not derived, and it's actually undercut by the visible screen text: *"ExceptionGroup: ConnectionError"* — a singular error in a "group." Either cut the "in general" clause, or add a beat where both calls fail simultaneously so the group genuinely has two members on screen.
- **NIT** — Go's `errgroup`/context mechanism (ch7) is asserted ("Go's standard way of telling goroutines to stop") rather than built up the way the task group was. Acceptable given the explicit scope-limiting note in Deviations, but it's the one idea in the video taken on faith rather than shown mechanically.

## 4. Setups without payoffs / payoffs without setups
- **SHOULD FIX** — Setup: *"if it had failed, its error would go nowhere. Nothing raises it, and nothing logs it"* (ch1, about the user-service call). This is never explicitly paid off — no later demo shows the user call itself failing under a task group and its error actually surfacing. Ch5's demo only ever fails the orders call. Fix: either swap which call fails in the ch5 demo, or add one beat where the user call is the one that errors, to close this specific loop.
- **Payoff without setup** — same item as in #3: the ExceptionGroup "bundle of errors" concept pays off nothing that was set up.
- Everything else pairs correctly: the sequential-await cancellation gap (ch3) is paid off by `cancel_taskgroup` (ch5); the retry-loop setup (ch6) carries its own payoff in the same beat.

## 5. Terms before explanation / multiple names for one concept
- **SHOULD FIX** — "ICE" appears twice in screen notes (ch5, ch7) as an unglossed state/color label, unlike "amber," which is explicitly defined at first use (*"turns amber: 'still running'"*). Nowhere does the script say what ICE means or stands for. Whoever builds the timeline graphics will hit the same wall a viewer would. Fix: define it at first use the same way amber is defined, or replace with a plain word ("blue: clean exit").
- **SHOULD FIX** — Attribution is split across channels: narration (ch4) credits Nathaniel Smith (2018) with the fix and the essay title; on-screen text separately credits *"the term: Martin Sústrik, 2016"* with no narrated link between the two names. A viewer has to reconcile, unaided, who coined the term vs. who wrote the essay driving the video's argument. Fix: give Sústrik one spoken clause ("Smith wasn't first to name it — Martin Sústrik had, two years earlier — but his essay is what made the argument"), or drop Sústrik from on-screen text and leave him to the end-card references only.
- **NIT** — "task group / nursery / scope" are given together in one aside (Argument, and again ch4 screen) and clearly flagged as per-language synonyms; this is handled well and shouldn't be pared further.

## 6. Numbers
All numbers, in order: 1 s (user latency) · 0.10 s (orders failure) · 1,000 (requests) · 1,000 (tasks left running) · 0.12 s (real-run counter) · 1.4 s (timeline axis) · 1.00 s (TimeoutError variant) · 1.10 s (sequential total, and again for the retry loop) · 0.50 s (client timeout, used twice) · 1968 / 2018 / 2016 (dates) · 3.11 (Python version) · 1.2 s (Go, used twice).

**Worth remembering: 0.10 s, 1.00 s/1.10 s, and 1,000.** These three are the ones the ending actually calls back to ("The request fails at a tenth of a second, and at a tenth of a second nothing is left running").

- **SHOULD FIX** — *"1,000 requests · all handlers returned after 0.12 s"* (ch1 screen). Every other beat in the video treats the failure time as a clean "a tenth of a second" (0.10 s); this one real-run counter reports 0.12 s with no acknowledgment of the discrepancy. A careful viewer will wonder whether the ending's tidy "0.10 s" is rounded or wrong. Fix: either round the counter's label to "≈0.10 s" or have the narration briefly note the real-world jitter.
- **NIT** — The Go section's "1.2 s" doesn't match Python's "1.10/1.00 s" pairing, with no line explaining why the equivalent demo runs slightly longer. Low stakes since it's a different program, but it's an unexplained number sitting right next to numbers that are supposed to rhyme.

## 7. Abstraction before the concrete case
**Passes.** Three full chapters of concrete handler/timeline (ch1–3) run before "structured concurrency" is named in ch4, and ch4 itself earns the abstraction with side-by-side arrow diagrams rather than asserting it. No fix needed.

## 8. Wrong intuition — confronted and shown failing?
**Yes, cleanly.** The Wrong Model ("waiting for all my tasks behaves like a function call") is stated in ch2 as true for the sequential case, then explicitly extended to `gather` in ch3 ("So you'd expect gather to behave like those calls…") and immediately shown false on the timeline and via the quoted docstring. This bait-and-switch is the strongest structural move in the script — no note needed.

## 9. Examples named but not understood
- Covered under #5: Sústrik is named but not explained.
- **NIT** — Kotlin/Swift/Java (preview) are named only in a single closing line with zero mechanics, per the Deviations note's explicit scope limit. Fine as a coda, but worth flagging so it's a deliberate choice and not an oversight if a reviewer asks "why no Kotlin demo."

## 10. On-screen text vs. narration; pictures that don't support the line
- **NIT** — Ch5 screen: *"the fetch_user bar is cut ('cancelled', ICE)"* at the exact moment narration says "The task group cancels the user request at once." The caption is a near-verbatim echo of the line being spoken; could be cut or replaced with something the narration doesn't already say (e.g., the wall-clock delta).
- The ch1 "gather_late" variant (arrow from a TimeoutError cross to an empty circle) is a good example of a picture *doing work the narration doesn't* — it visualizes "the error goes nowhere" without the line needing to say it twice. No fix; flagging as the model other beats should follow.

## 11. Lines that could be deleted without breaking anything
- **NIT** — *"You can treat it as a black box"* (ch2). A fine phrase, but it's never picked up again by name (the ending re-earns the concept without the words), so it's a one-off metaphor rather than a planted callback. Either cut it, or better, reuse "black box" once in ch8 for a tighter terminological close: *"…and the function is a black box again."*
- The ExceptionGroup justification clause (already flagged in #3/#4) is also deletable without the argument losing anything — a second, independent reason to cut it rather than fix it with a new demo, if the simpler edit is preferred.

## 12. Hard-to-follow-aloud sentences / pacing
- **SHOULD FIX** — Ch7: *"Go has no task group in the language, but it has a convention: an error group, with a context, Go's standard way of telling goroutines to stop."* Three stacked appositives in one breath; on a first listen it's ambiguous whether "Go's standard way…" modifies "a context" or the whole clause. Rewrite: *"Go has no task group in the language, but it has a convention for the same job: an error group. Paired with a context, it's Go's standard way of telling goroutines to stop."*
- **NIT** — Ch3: *"the user request, the one being awaited, is cancelled"* — the mid-sentence appositive is a small stumble aloud. Rewrite: *"the user request — the one being awaited — is cancelled."* (or split into two sentences).
- **Pacing** — Ch7 compresses an entire second language (Go) plus a name-check of three more (Kotlin/Swift/Java) into the shortest chapter in the script. This is explicitly licensed by the Deviations note, so it reads as an intentional choice, not an oversight — flagging only so it's confirmed deliberate rather than a beat that ran out of room.

---

No finding here rises to a level that breaks the chain, misdirects the audience about the core mechanism, or leaves the opening question unanswered — the two SHOULD FIX items worth prioritizing before the rest are the **0.12 s/0.10 s mismatch** and the **ExceptionGroup justification without a matching demo**, since those are the two places a sharp viewer could catch the video contradicting its own evidence.

**VERDICT: PASS**
