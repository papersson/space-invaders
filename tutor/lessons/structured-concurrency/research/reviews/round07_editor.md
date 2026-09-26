# Script Review

## Test 1 — Opening question / closing answer
**Pass, strong.** Ch.1 closes: *"The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"* Ch.8 opens: *"So why was the handler's work still running after it returned?"* and closes: *"Give every task an owner, and 'returned' means 'done.'"* Near-verbatim callback, both clauses of the question answered. No note.

## Test 2 — Chain in but/therefore/and-then
1. Handler fans out with `gather`; returns an error at 0.10s **but** its user-service call runs on to 1.00s unheard, and at scale 1,000 tasks are left running — why, and what would make "returned" mean "done"?
2. **Therefore** consider plain sequential calls: one-way-in-one-way-out means returning = done, **but** sequential is slow (1.10s).
3. **Therefore** start tasks concurrently, **but** starting a task splits control into two paths that don't rejoin (`gather` waits on results not tasks; awaiting one-at-a-time misses the untracked task) — **therefore** a fix must wait for every task, cancel the rest on failure, cancel all on caller give-up.
4. **Therefore** name the principle: Dijkstra's `goto` problem again; Smith's fix is the same as structured programming's — a block tasks can't outlive.
5. **Therefore** rewrite with `TaskGroup` and measure: guarantees hold.
6. **But** the block can only ask, not force (cooperative cancellation, bare-except escape; only covers tasks it started; not shared-data races).
7. **But** it isn't Python-specific: Go/errgroup, Swift/Java/Kotlin build the same rule in.
8. **Therefore**: the answer.

**"And then" count: 0.** No meandering additive links — the whole script is causally chained. Notable strength.

## Test 3 — Announced vs. derived ideas
Pass. "Structured concurrency" and "task group" are both derived (the block mechanism is described in prose in ch.4 *before* being named), and `except*`/exception-group is justified with a "since" clause. No idea in the core argument (chs. 1–6) is asserted without a visible problem driving it.

## Test 4 — Setups/payoffs
Pass. "Black box" (ch.2) is explicitly paid off in ch.4 ("you can no longer treat a function as a black box"). The `gather_late` variant pays off "if it had failed, its error would go nowhere." The retry-loop pays off "cancellation needs the task's cooperation." One weak payoff below (see Test 9/11).

## Test 5 — Terms before explanation / double names
- **NIT.** "error group" (spoken) vs. `errgroup` (on-screen identifier) for the same thing — trivial but worth a one-word gloss the first time it's on screen, e.g. have the narration say "an error group — Go calls the package `errgroup`."
- **NIT.** "goroutine" (ch.7) is used cold, without being anchored to the already-established term "task." *Rewrite:* "Here's the same handler in Go, with plain goroutines — Go's version of a task."

## Test 6 — Numbers
All numbers: 1 s, 0.10 s, 1.00 s, 1,000, 1.10 s, 0.50 s, 1968, 2018, 2016, Python 3.11, 1.2 s, (end-card only: JEP 533/543, JDK 27/28).

**Worth remembering: 0.10 s, 1.00 s, 1,000** — these three carry the entire before/after contrast and are the exact numbers the closing line calls back to.

- **NIT.** 2016 ("a name Martin Sústrik had given it two years earlier") is precise citation trivia that does no argumentative work — it's there to avoid over-crediting Smith, not to be remembered. Fine to keep for accuracy but flagging per the test.
- **NIT.** "1.2 s later" (Go check) is an arbitrary buffer; "checked again after every request's second had passed" would say the same thing without a number nobody needs to retain.

## Test 7 — Abstraction before concrete case
Pass. Concrete handler/timelines precede every abstraction (task-splitting, then goto, then structured concurrency). Correct order throughout.

## Test 8 — Wrong intuition, shown failing
Pass, strong. Wrong model = "gather, or awaiting each one, behaves like a function call." **Both halves are shown failing on screen**: the `gather` timeline (amber tail past return) plus the `gather_late` variant (error → empty circle) for the first half; the `cancel_create_task` timeline (orders bar runs to completion after cancellation) for the second half.

## Test 9 — Named but not understood
- **SHOULD FIX.** Swift, Java, and Kotlin are named twice (ch.4 end-labels, ch.7 closing sentence) with no code, no timeline, no mechanism — unlike Go, which gets the full treatment (code, goroutine-leak count, errgroup fix, measured "0 left over"). As written, three of the five comparison languages are just trivia.
  *Quote:* "Swift and Java have the same kind of block built in, Java's still as a preview feature. Kotlin has it in its official coroutines library."
  *Rewrite:* either cut the sentence (Go alone already proves "not just Python" and the convention-vs-built-in point), or give it one concrete grip, e.g.: "Swift's `async let` and task groups, Java's `StructuredTaskScope`, and Kotlin's `coroutineScope` all refuse to return until their children do — the same block, three syntaxes." That at least shows the *rule*, not just a name-drop.

## Test 10 — Redundant on-screen text / unsupported pictures
Pass overall — screen notes are diagram/timeline labels (necessarily naming what's drawn) rather than caption-repeats-narration. No picture found that fails to support its line; the cancel_create_task / cancel_taskgroup pairing is a nice deliberate visual echo (only-one-cancelled vs. both-cancelled).

## Test 11 — Deletable lines
- **NIT.** The ch.7 closing language-list sentence (see Test 9) could be deleted outright without weakening the argument at all — it's the one line in the script that doesn't feed the chain, a setup/payoff, or a number worth remembering. Either cut it or upgrade it per the Test 9 rewrite.

## Test 12 — Hard-to-say sentences / pacing
- **SHOULD FIX (pacing).** Chapter 7 compresses more new material into one beat than any other chapter — full Go mechanism (goroutines, errgroup, context) *plus* three more languages — after five chapters spent on the Python case alone. It reads as rushed relative to the rest of the script's rigor. Recommend either trimming the Swift/Java/Kotlin tail (per Test 9/11) to let the Go beat breathe on its own as the sole "not just Python" proof, or giving the language list its own short beat with one concrete detail each.
- No sentence is un-sayable aloud; the longest (the Smith essay title, the Python docs quote) are both justified — a title and a verbatim quote read naturally as quotations.

---

**Summary of actionable items:** one SHOULD FIX (Swift/Java/Kotlin tail is named-not-understood and rushes ch.7's pacing — cut or strengthen it), plus four NITs (errgroup/error-group naming, unglossed "goroutine," the 2016 date's non-work, the arbitrary 1.2s). Everything structural — the question/answer frame, the chain, the wrong-model-shown-failing, concrete-before-abstract ordering, and the number discipline — is unusually solid.

VERDICT: PASS
