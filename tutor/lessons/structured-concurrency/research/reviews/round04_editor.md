# Script Review

## 1. Opening question → ending callback

**PASS.** Opening: *"The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"* Ending: *"So why was the handler's work still running after it returned? … Give every task an owner, and 'returned' means 'done.'"* Tight, direct callback, same vocabulary both times. No finding.

## 2. Chain test

1. The handler returns an error at 0.10 s but its request runs on to 1.00 s, and 1,000 requests leave 1,000 tasks running — why, and what would make "returned" mean "done"?
2. Therefore look at what a plain sequential call promises (one way in, one way out) — but it's slow (1.10 s).
3. Therefore start tasks instead — but starting a task splits control and nothing brings the second path back, so `gather` leaves the failed-over task running and awaiting one-at-a-time lets a cancellation miss the other.
4. Therefore this is `goto` again, and structured programming fixed it with blocks — therefore structured concurrency fixes tasks with a block they can't outlive.
5. Therefore the same handler in a task group delivers three guarantees, measured.
6. But the block can only *ask* — cancellation needs cooperation, and it covers only tasks started inside it, not shared data.
7. But this isn't a Python quirk — Go leaves goroutines behind without a group, none with one; Kotlin/Swift/Java have it built in.
8. Therefore the answer.

**No "and then" appears anywhere in the chain or in the script's connective tissue** — every joint is causal ("therefore") or a genuine complication ("but"). That's a clean result; nothing to report here.

## 3. Announced vs. derived ideas

**SHOULD FIX.** The block/task-group solution arrives by analogy, not by derivation from the two failure modes just shown.
> *"That rule is called structured concurrency… In Python's asyncio, the block is a task group."*

Chapter 3 shows two independently-failing fixes (`gather` doesn't cancel the sibling; sequential awaiting lets one task escape a cancellation). The video never explicitly states what a real fix would need to guarantee before invoking Dijkstra — it jumps straight to "this is goto, here's a block." The three guarantees in ch. 5 read as things the tool happens to give you, not as the spec the two failed attempts implied.

*Rewrite:* After the `create_task` example, add one line that turns the two failures into a spec: *"So a fix needs three things: it has to wait for every task, cancel the rest when one fails, and get the error out. That's exactly what Dijkstra's blocks did for jumps — here's the same block, for tasks."* Then ch. 5's three guarantees read as promises kept, not new information.

## 4. Setups / payoffs

Mostly clean — "still running" → 0 left, "error goes nowhere" → surfaced via ExceptionGroup, "1,000 tasks running" → "0" are all paid off with matching numbers.

**NIT.** The `cancel_create_task` setup (ch. 3: orders task keeps running after the client cancels the user request) is never verbally contrasted with its payoff (ch. 5's `cancel_taskgroup`, where both are cancelled). The screen carries the payoff; the narration doesn't point at it.
*Rewrite:* add to ch. 5: *"And this time, giving up cancels both — not just the one we happened to be awaiting."*

## 5. Terms explained once / dual names

**SHOULD FIX.** `ICE` appears in the ch. 5 screen direction with zero definition anywhere in the document:
> *"at the same moment the fetch_user bar is cut ('cancelled', ICE)"*
This reads as either a leftover internal label or an unexplained acronym landing at the video's central demonstration (the moment cancellation actually works). If it's meant for viewers, it needs a gloss; if it's a production note, it needs to be removed before it renders on screen.
*Rewrite:* drop `ICE`, or replace with the plain label already used elsewhere: *"the fetch_user bar is cut ('cancelled')"*.

**NIT.** "Exception group" is introduced and explained in one clause (ch. 5) and never touched again — no mention of how the caller actually unwraps it (`except*`). Fine as a passing detail, but if a viewer pauses on "ExceptionGroup: ConnectionError" they have no path to "what do I write to catch this." Consider one clause acknowledging it's out of scope, or cut the term and just say "the error."

## 6. Numbers

Full list: 1.00 s, 0.10 s, 1,000, 1.10 s, 1968, 2018, 2016, Python 3.11, 0.50 s, 0.12 s, 1.10 s (retry), 1.2 s (Go), JDK 27/28.

**Worth remembering: 0.10 s, 1.00 s, 1,000.** These are the ones the script deliberately recurs to and pays off (0.10 s = when things should stop; 1.00 s = the straggler; 1,000 = the scale that makes it matter, not a toy case).

**SHOULD FIX — a number doing unclear work:**
> *"bare goroutines: 1,000 left over; 1.2 s later: 1,000"* / *"errgroup + context: 0; 1.2 s later: 0"*
Every Python measurement is an instantaneous snapshot right after the handler returns. The Go section suddenly checks "1.2 s later" — a new number that doesn't map to the 0.10 s/1.00 s vocabulary already trained into the viewer, and it's never said why 1.2 s is the check point. A viewer may wonder if Go's services run on a different clock.
*Rewrite:* Either match the established cadence ("still running after the handlers returned") or state why: *"— checked a second later, so nothing was just mid-flight."*

**NIT.** "a name Martin Sústrik gave it in 2016" — the date does no work (unlike "fifty years later" for Smith, which *does* do work, showing the gap). Could cut to "…a name Martin Sústrik gave it" without loss.

## 7. Abstraction vs. concrete

**PASS.** The concrete handler is established in ch. 1 before any abstraction; ch. 2's "one way in, one way out" is paired with the concrete sequential code on screen, not asserted alone; the goto analogy in ch. 4 lands only after two concrete failures are already on screen. No finding.

## 8. Wrong intuition, shown failing

**PASS.** The stated wrong model covers both `gather` and "awaiting each one" — and the script shows *both* failing concretely (ch. 3's docs quote for `gather`; the `cancel_create_task` timeline for sequential awaiting). Well executed, no finding.

## 9. Named but not understood

**NIT.**
> *"Kotlin, Swift and Java have the same kind of block built in. Java's is still a preview feature."*
No code, no behavior shown — pure name-drop, unlike Go which gets a full concrete demonstration. This is probably fine as a deliberate footnote (objectives don't ask for depth here), but if trimmed further it could just be cut to the end-card references instead of getting a spoken sentence that promises little and delivers less.

## 10. On-screen text vs. narration / pictures vs. line

**SHOULD FIX.** Ch. 5's caption plan:
> *"the three guarantees as three short labels, each appearing as it is said: 'waits', 'failure cancels the rest · error reaches the caller', 'cancel the caller → cancel its tasks'"*
This is narration restated verbatim as captions at the exact moment it's spoken — the clearest instance of text repeating the line rather than adding to it.
*Rewrite:* Have each label point at the timeline instead of restating the sentence — e.g. an arrow from "waits" to the point where the block's own line extends past 0.10 s, rather than printing the clause again.

Everything else (citation cards, Go's construct names, ch. 6's limit tags) either adds information not in the narration (actual API names) or is a standard, low-cost citation convention — not flagged.

## 11. Deletable lines

- *"a name Martin Sústrik gave it in 2016"* → trim to *"a name Martin Sústrik gave it"* (see #6).
- *"even when there's only one"* (ch. 5, re: exception group) — a clarifying aside that could go without loss if #5's exception-group trim is taken.

Nothing else is safely cuttable — the script is otherwise lean; most lines carry a setup or a payoff.

## 12. Hard to say aloud / pacing

**SHOULD FIX.**
> *"If the client gives up after half a second, the user request, the one being awaited, is cancelled."*
Double-nested apposition ("the user request, the one being awaited,") is a stumble waiting to happen read aloud.
*Rewrite:* *"If the client gives up after half a second, the request being awaited — the user one — is cancelled."* or simpler: *"…the user request is cancelled, because that's the one being awaited."*

**SHOULD FIX — rushed beat.** Chapter 4 packs four citations (Dijkstra 1968, Smith 2018 + full essay title, Sústrik 2016, TaskGroup/3.11) plus the core rule statement into one short paragraph — the highest fact-density-per-second in the script, right at the moment the video's central abstraction is supposed to land.
*Rewrite:* move the Sústrik naming credit to ch. 5, attached to the words "task group" when they're demonstrated concretely, so ch. 4 can slow down on just Dijkstra → Smith → the rule.

---

**Summary of severities:** 1 BLOCKING (undefined "ICE" on screen at the key payoff), remainder SHOULD FIX / NIT covering the analogy-not-derivation gap for the block's introduction, the Go section's unexplained "1.2 s" check, verbatim-narration captions in ch. 5, one hard-to-parse sentence in ch. 3, and rushed pacing in ch. 4.

VERDICT: REVISE
