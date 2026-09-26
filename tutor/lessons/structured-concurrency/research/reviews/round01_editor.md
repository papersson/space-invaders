# Script Review

## Test 1 — Opening/closing callback
**Opening:** "The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"
**Closing:** "So why was the handler's work still running after it returned? ... Give every task an owner, and 'returned' means 'done'."
Clean, direct callback — the closing line literally reuses the opening's phrasing. **No finding here.**

## Test 2 — One-sentence chain, joined by but/therefore/and then
1. A handler fans out with `gather` and the orders call fails fast while the user call keeps running unseen, so we ask why "returned" doesn't mean "done."
2. **Therefore** we check what a plain sequential call guarantees — one way in, one way out — **but** that's slow.
3. **Therefore** we run the calls concurrently, **but** starting a task splits control and nothing brings the second path back, so `gather`'s failure path (and one-at-a-time awaiting) both leave work orphaned.
4. **Therefore** we recognize this as the `goto` problem again, and **therefore** the fix is a block tasks can't outlive.
5. **Therefore** we rewrite the handler in a task group and measure the three guarantees holding.
6. **But** the block can only ask a task to stop, so cooperation, scope, and shared state remain real limits.
7. **And then** the same rule/convention shows up in other languages, Go included.
8. **Therefore**, the answer: give every task an owner, and returned means done.

Only **one "and then"** (step 6→7). Flagged below (SHOULD FIX) — it's the one joint in the film that's additive rather than causal.

## Test 3 — Ideas announced vs. derived
Mostly derived well: the wrong model is stated then broken on screen (ch2→ch3), the three guarantees are each shown measured before being named (ch5), and "structured concurrency" is named only after the block concept is derived by analogy (ch4). One exception:

- **SHOULD FIX.** *"raises the error in the handler, wrapped in an exception group, because more than one task can fail."* — In this run only one task actually fails (orders); fetch_user is cancelled, not independently "failed." The justification given doesn't match the demonstrated case, so it reads as an assertion bolted onto the demo rather than something the demo earned.
  **Rewrite:** "...raises the error in the handler. A task group always wraps it in an exception group — even one error — because in general more than one task can fail at once."

## Test 4 — Setups/payoffs
Strong pairing overall: "error goes nowhere" (ch1) → resolved in ch5; "1,000 tasks still running" (ch1) → "tasks still running: 0" (ch5); the 0.50s give-up demo in ch3 (`create_task`) is mirrored exactly in ch5's `cancel_taskgroup`. These are the film's best beats — don't touch them.

- **SHOULD FIX.** Ch6 names three limits ("cooperation," "only tasks started inside," "not about shared data") but only the cooperation limit gets a code+timeline demonstration (the retry loop). The other two are payoffs without a setup/demo — just on-screen labels with no shown example.
  **Rewrite:** Either cut the two undemonstrated limits down to a single spoken sentence each (already close to what exists) and stop implying they got the same treatment, or add one line of concrete grounding, e.g. for "only tasks started inside": "The retry loop's `create_task` calls off to the side aren't covered — the group only watches what it started." For shared data, a one-line example (two tasks incrementing the same counter) would do more than the current bare label.

## Test 5 — Terms before explanation / dual names
- "task group / nursery / scope" — explicitly presented as synonyms across ecosystems, not a hidden dual-naming problem. Fine.
- **NIT.** "exception group" (ch5) is used before being explained beyond the shaky justification above — see Test 3 finding, same fix covers this.
- The screen annotations "(amber)" / "(ICE)" — presumably color codes for the animator rather than viewer-facing captions, but if any of this leaks onto screen as literal text, "ICE" is never glossed anywhere and won't read as intelligible to a viewer. **NIT:** confirm these are internal-only annotations; if any becomes on-screen text, replace with a plain word ("clean"/"resolved").

## Test 6 — Numbers
All numbers: 1.00s (user latency), 0.10s (orders failure / correct return time), 1,000 (concurrent requests), 1.10s (sequential total *and*, recurring, the retry-loop's regressed total), 0.50s (client give-up), 1.2s (Go leftover-check delay), 0.12s (measured screen counter), 1968/2018/2016 (Dijkstra/Smith/Sústrik), Python 3.11, JDK 27/28.

**Worth remembering:** 0.10s, 1.00s (the gap that is the whole problem), and 1.10s — which is the strongest number in the script because it recurs: it's what plain sequential code costs (ch2) *and* what the retry-loop failure regresses back to (ch6). That callback is worth foregrounding, not just showing on a timeline.

**Doing no work — flag for cutting:**
- **NIT.** "0.12 s" (screen counter) — narration says "about a tenth of a second," so this is close enough to be fine, but if read literally it looks like a contradiction of the "0.10s" claimed elsewhere. **Rewrite (narration):** "within about 0.12 s" to match the actual measured figure, or round the counter to "~0.10 s" to match narration.
- **NIT.** "2016" (Sústrik) — pure attribution trivia, does no comprehension work.
- **NIT.** "(preview in JDK 27; JEP 543 proposes it final for JDK 28)" — over-precise versioning nobody needs to retain; "still a preview feature" already carries the point.

## Test 7 — Abstraction before concrete case
Order is sound: the concrete broken example (ch1) precedes every abstraction (ch2's "one way in, one way out," ch4's goto analogy). No finding.

## Test 8 — Wrong intuition, shown failing
The wrong model ("if I wait for everything with gather, it behaves like a function call") is stated in ch2 ("you can treat it as a black box") and then explicitly shown failing in ch3 ("But when one fails, gather passes that error on immediately, and doesn't cancel the other task"), backed by the actual timeline. **Passes**, though it could be sharpened by naming the expectation more directly before breaking it:
**NIT rewrite for ch3 opener:** "So you'd expect `gather` to behave exactly like the calls we just saw — and when both requests succeed, it does."

## Test 9 — Examples named but not understood
- **SHOULD FIX.** Ch7's table — "Kotlin: coroutineScope · Swift: task groups, async let · Java: StructuredTaskScope" — these three are named with zero demonstration, in a chapter that otherwise earns its Go comparison with actual code and a measured run. This is a credibility list, not an argument beat, and it's also the segment tied to the script's one "and then" (Test 2).
  **Rewrite:** Cut to one sentence with no table: "Kotlin, Swift, and a preview API in Java all have the same kind of block." Keep the screen real estate for Go, which is the only cross-language example that's actually shown working.
- **SHOULD FIX.** "a thousand goroutines are left, stuck for good, each waiting to hand over a result that nobody will read" — asserts a specific mechanism (blocked channel send) that is never visualized; the screen only shows a leftover counter, not why goroutines get stuck. Either simplify the claim to what's shown ("a thousand goroutines never finish") or add a one-frame diagram of the blocked send.

## Test 10 — On-screen text vs. narration/pictures
- **SHOULD FIX.** *"TimeoutError: raised to no one, logged nowhere"* (ch1 screen) is a near-verbatim restatement of the narration line spoken seconds earlier ("its error would go nowhere. Nothing raises it, and nothing logs it."). Pick one job for each channel.
  **Rewrite (screen only):** show just the exception type and a red "→ ∅" glyph; let narration carry the explanation.
- **SHOULD FIX.** Ch7's table (Kotlin/Swift/Java line) is on-screen text that does nothing but restate the sentence being spoken — see Test 9 finding, same fix.
- Ch4's name/date list ("Dijkstra 1968 · Sústrik 2016 · Smith 2018...") repeats spoken dates, but this is standard/acceptable documentary practice for facts a viewer can't rewind to catch — not flagged.

## Test 11 — Deletable lines
- "Martin Sústrik named it in 2016, and Smith's library, Trio, built it in." — cuttable without any loss to the argument (NIT).
- The Kotlin/Swift/Java sentence in ch7 (see Test 9) — cuttable to one clause.
- The JDK 27/28 parenthetical (see Test 6) — cuttable.

## Test 12 — Sentences hard to follow aloud / pacing
- **SHOULD FIX.** *"The task group cancels the user request at once, waits for it to stop, and raises the error in the handler, wrapped in an exception group, because more than one task can fail."* — five clauses stacked in one breath, and it's also the sentence carrying the weakest logic (Test 3). Split it.
  **Rewrite:** "The task group cancels the user request at once and waits for it to stop. Then it raises the error in the handler — wrapped in an exception group, since more than one task can fail at once."
- **Pacing risk (SHOULD FIX).** Chapter 4 packs two historical citations (Dijkstra, Smith), a naming citation (Sústrik/Trio), a concept introduction, a code card, and a four-part name list into roughly a minute of narration. Nothing here is wrong, but it's the densest chapter in the script for both facts-per-second and visual-changes-per-second. Cutting the Sústrik/Trio aside (already flagged as deletable) buys the rest of the chapter room to breathe.
- No chapter reads as padded; ch1 and ch5 are dense but each sentence maps to a distinct screen beat, so the density is earned.

---

## Findings summary

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | SHOULD FIX | Ch5, "wrapped in an exception group, because more than one task can fail" | Justification doesn't match the single-failure case actually shown |
| 2 | SHOULD FIX | Ch6, "only tasks started inside" / "not about shared data" | Asserted as labels, never demonstrated, unlike the cooperation limit |
| 3 | SHOULD FIX | Ch7, Kotlin/Swift/Java table | Named but not understood — no demo, breaks the chapter's one "and then" into pure list |
| 4 | SHOULD FIX | Ch7, "stuck for good, each waiting to hand over a result nobody will read" | Mechanism asserted, not visualized |
| 5 | SHOULD FIX | Ch1 screen, "TimeoutError: raised to no one, logged nowhere" | On-screen text repeats narration verbatim |
| 6 | SHOULD FIX | Ch5, "cancels...waits...raises...wrapped...because" sentence | Five clauses in one breath; also carries finding #1 |
| 7 | SHOULD FIX | Ch4 overall density | Sústrik/Trio aside adds facts-per-second without narrative payoff; cutting it eases pacing |
| 8 | NIT | Ch1 screen counter "0.12 s" vs. narrated "a tenth of a second" | Minor imprecision, easy one-word fix |
| 9 | NIT | "Sústrik...2016", JDK 27/28 parenthetical | Trivia doing no narrative work, safely cuttable |
| 10 | NIT | Ch3, "Start both, await the user request, and let the client give up..." | Slight voice/tense shift, mildly awkward aloud |

No BLOCKING items — the causal chain holds together end to end, the callback is clean, and the wrong intuition is genuinely shown failing rather than just asserted. The fixes above are tightening, not structural surgery.

VERDICT: PASS
