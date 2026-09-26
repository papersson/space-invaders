# Script Review

## Test 1 — Opening question / ending callback
**PASS.** Ch.1 ends: *"The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"* Ch.8 opens: *"So why was the handler's work still running after it returned?"* and closes: *"Give every task an owner, and 'returned' means 'done'."* Tight, verbatim callback. No finding.

## Test 2 — One-sentence chain, connectors
1. The handler's request keeps running after it returns, and its errors go nowhere — **therefore**, what does a normal call promise?
2. A sequential call is "one way in, one way out," so returning means done, **but** it's slow — **therefore** we start tasks concurrently.
3. Starting a task splits control and neither `gather` nor manual awaiting brings the second path back — **therefore** this is the same problem as `goto`, and the fix is a block tasks can't outlive.
4. **Therefore** here's the same handler in a task group, with its three guarantees measured.
5. **But** the block can only *ask* — cooperation, scope, and shared data are all still open problems.
6. **But** this isn't Python-specific — Go without a convention leaks goroutines, with one it doesn't, and other languages build the rule in.
7. **Therefore**, the answer.

Zero "and then"s — every joint is causal (*therefore*/*but*), not merely sequential. This is a genuine strength; worth preserving under future edits.

## Test 3 — Ideas announced vs. derived
Mostly derived cleanly (see chain above). One exception:

- **NIT.** *"It arrives wrapped in an exception group: a task group always bundles its tasks' errors, even when there's only one."* This is an implementation fact asserted at the argument's emotional payoff beat (the moment the ch.1 "errors go nowhere" setup resolves), not derived from anything shown. It risks diluting a clean beat with a Python quirk.
  **Rewrite:** Move the exception-group detail to on-screen text only; keep narration to *"Then it raises the error in the handler — the one that never got a chance to arrive before."*

## Test 4 — Setups/payoffs
All major setups pay off: "errors go nowhere" (ch.1) → resolved ch.5; "await one at a time" gap (ch.3) → resolved by `cancel_taskgroup` run (ch.5); "plain `create_task` is on its own" (ch.6) callback to ch.3. No orphaned setups or unearned payoffs found.

## Test 5 — Terms before explanation / multiple names
- **SHOULD FIX.** The block has three names in play — *task group* (spoken), *nursery* (on-screen only, ch.4), and *scope* (mentioned in the Argument doc but **absent from the script entirely**). The on-screen "nursery" note has no spoken support, and "scope" is dropped between doc and script — an inconsistency a viewer relying on narration alone won't get, and one the doc/script drifted apart on.
  **Rewrite:** Add one spoken clause in ch.4: *"— other languages call the same block a nursery, or a scope; the name changes, the rule doesn't."*

## Test 6 — Numbers
All numbers: 1 s, 0.10 s, 1,000, 1.10 s, 1968, 2018, 2016, Python 3.11, 0.50 s, 1.2 s, 150 wpm, JEP 533/543.
**Worth remembering:** 0.10 s (the return moment), 1.00 s (the runaway task), 1,000 (why it matters at scale).
- **NIT.** *"a name Martin Sústrik gave it in 2016"* — this date does no argumentative work (unlike 1968→2018, which sets up the "fifty years later" beat). Candidate for cut from narration, kept on-screen/end-card only.

## Test 7 — Abstraction before concrete case
No violation. Concrete handler (ch.1) → concrete sequential case (ch.2) → concrete task-splitting mechanism (ch.3) → historical abstraction (ch.4), immediately re-grounded in the concrete `TaskGroup` block. Correct order throughout.

## Test 8 — Wrong intuition, shown failing
Two wrong intuitions are named and shown failing:
1. *"You'd expect [gather] to behave like those calls"* → shown failing via docstring quote + amber timeline.
2. Awaiting tasks one at a time → shown failing via `cancel_create_task` run (orders task runs on past the 0.50 s cancel).
Both satisfy the test. No finding.

## Test 9 — Examples named but not understood
- **NIT.** *"Kotlin, Swift and Java have the same kind of block built in. Java's is still a preview feature."* The three constructs (`coroutineScope`, task groups, `StructuredTaskScope`) appear as on-screen names only, never explained even at the one-sentence level narration gives Go's `context`/`errgroup`. Consistent with the author's stated scope limit, but still a pure name-drop.
  **Rewrite (optional):** *"Kotlin's coroutineScope, Swift's task groups, and Java's still-preview StructuredTaskScope all enforce the same rule: no task outlives its block."*

## Test 10 — On-screen text vs. narration; pictures vs. line
Diagrams are consistently well-matched to narration (ch.2's one-arrow-in/one-arrow-out, ch.3's splitting arrow). One repeated pattern:
- **NIT.** Ch.4/5/6 each show "labels, each appearing as it is said" — condensed restatements of the exact spoken guarantees. Low severity (standard retention technique) but technically redundant per the test.
  **Rewrite:** Replace ch.5's guarantee labels with the mechanism, not the words — e.g. `await tg:` blocks until all done / on failure → cancel siblings / cancel outer → cancel tg — so the screen adds information rather than echoing it.

## Test 11 — Deletable lines
- **NIT.** *"His essay was called 'Notes on structured concurrency, or: Go statement considered harmful'."* — citation flavor, already in the end-card references; cutting it from narration loses nothing.
- **NIT.** *"a name Martin Sústrik gave it in 2016"* — same, prunable (see Test 6).
Nothing else in the script reads as filler; it's unusually lean.

## Test 12 — Hard to follow aloud / rushed or padded
- **SHOULD FIX.** *"Its convention is an error group, together with a context, which is Go's standard way of telling goroutines to stop."* Two new terms land in one breath with a trailing explanatory clause — hard to parse on a single listen.
  **Rewrite:** *"Go's convention pairs two things: a context, the standard way to tell goroutines to stop, and an error group, which wires that context to every goroutine it starts."*
- **NIT.** Ch.1's *"a thousand handlers... a thousand tasks... a thousand requests"* triple repetition is deliberate anaphora for the scaling point — effective, but flag in case a read-aloud pass finds it rushed.

---

No BLOCKING items. The chain is causally sound end-to-end with zero "and then" joints, the opening/closing callback is exact, the wrong intuition is named and shown failing twice, and concrete-before-abstract ordering holds throughout. Findings above are polish: a naming inconsistency between doc and script (task group/nursery/scope), one dense Go sentence, a couple of prunable citation dates, and mildly redundant recap text.

VERDICT: PASS
