# Script Review

## 1. Opening question → ending callback
**Pass.** Ch1 ends: *"The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"* Ch8 opens: *"So why was the handler's work still running after it returned?"* and closes: *"Give every task an owner, and 'returned' means 'done.'"* Near-verbatim callback, correctly earned by the intervening argument.

## 2. Segment chain, "but/therefore/and then"
The author's own Chain already does this. Literal count of **"and then": 0** — good, no filler joins.

One weak link: step 7's **"but"** ("But this isn't a Python quirk...") isn't a real contrast with step 6 (the limits of task groups) — it's a lateral move to a new topic (cross-language generality) wearing a "but."
- **NIT** — Quote: *"But this isn't a Python quirk: the same handler in Go..."*
- Rewrite: *"And the same shape shows up outside Python: ..."* (own the additive move instead of dressing it as a rebuttal), or bridge it explicitly: *"The limits are Python's. The problem isn't — here's the same handler in Go."*

## 3. Ideas announced vs. derived
Mostly derived cleanly: the three-part spec in ch3 ("wait for every task... cancel the rest... cancel them all") is extracted directly from the shown failures, and ch4's "block" solution is introduced only after that spec exists, so it lands as fulfillment, not assertion. One exception:

- **SHOULD FIX** — "exception group" is introduced by definition rather than by a shown need: *"It arrives inside an exception group, a container that can hold the errors of several tasks."* In this run only one task fails, so the container's actual reason for existing (multiple simultaneous errors) is asserted, not seen.
- Rewrite: either trigger a second, simultaneous failure in the demo run so two errors land in one group, or cut the generality claim: *"It arrives wrapped in an ExceptionGroup — Python's container for an error, in case more than one task fails at once."* (make the hedge explicit rather than a flat claim of capability never exercised).

## 4. Setups without payoffs / payoffs without setups
Strong overall — the 1,000-request counter, the gather gap, and the create_task/await-one-at-a-time gap all get explicit task-group payoffs in ch5.

- **NIT** — Ch6 states three limits (cooperative cancellation, only-tasks-inside-the-block, not-data-races) but only the first gets a demonstrated failure (the retry loop). The other two are asserted, not shown. This is already acknowledged in the Deviations note as a deliberate cut, so it's a NIT rather than SHOULD FIX — but worth a sentence marking them as assertions rather than letting them sit at the same evidentiary weight as the demoed one, e.g. *"...and two more limits, unproven here: ..."*

- **NIT** — Sústrik's attribution is a payoff with no setup and no follow-through: *"That rule is called structured concurrency, a name Martin Sústrik had given it two years earlier."* Nothing before or after uses this name or this person. See Test 11 — candidate for deletion.

## 5. Terms before explained / multiple names
Generally clean — gather, CancelledError, errgroup, and context are each glossed at first use. The multi-name risk flagged in the Argument section ("task group / nursery / scope") does **not** leak into the actual script — the script sticks to "block" and "task group" consistently. No fix needed there.

## 6. Numbers
All numbers: 1 s (user service), 0.10 s / "a tenth of a second" (orders failure), 1,000 (concurrent requests), 1.10 s (sequential total, and the defeated retry loop), 0.50 s (client timeout), 0.12 s (ch1 counter), 1968 / 2016 / 2018 (attributions), Python 3.11.

**Worth remembering: 0.10 s and 1.00 s** (the whole plot is the gap between them) and **1,000** (proves it's not a one-off quirk but a scaling problem).

- **SHOULD FIX** — the ch1 counter says *"all handlers returned within 0.12 s"* while every other beat anchors on "a tenth of a second" / 0.10 s. A viewer who's been told to remember 0.10 s hits a different number at the one moment meant to prove scale. Rewrite: round the displayed counter to "~0.10 s" or add the word "about," e.g. *"1,000 requests at once · handlers returned within about 0.10 s · tasks still running: 1,000."*
- 1968/2016/2018 do real work (chronology of the idea) except 2016 (Sústrik) — flagged above, doing no work on its own.

## 7. Abstraction before the concrete case
No violations — concrete case (ch1) precedes principle (ch2–4), and the historical/abstract chapter 4 is earned by three prior chapters of grounding.

## 8. Wrong intuition — named and shown failing
**Pass.** Ch3: *"You'd expect it to behave like those calls. It waits for both results, and when both requests succeed, it does. But when one fails, gather... doesn't cancel the other task."* This explicitly states the wrong model (gather behaves like a function call) and then shows it fail. Good — matches the stated Wrong Model exactly.

## 9. Examples named but not understood
- **NIT** — Kotlin's `coroutineScope`, Swift's task groups, and Java's `StructuredTaskScope` are named in ch7's closing line with zero demonstration (unlike Go, which gets real code and a measured run). Acceptable as a "breadth" coda, but as written a viewer "knows of" these but doesn't understand any of them. If time allows, one beat of Swift or Kotlin code would upgrade this from name-drop to example; otherwise consider softening the claim to explicitly frame it as a pointer rather than a taught fact: *"...and if you want the built-in version, look up Swift's task groups, Java's StructuredTaskScope, or Kotlin's coroutineScope."*
- Sústrik (see #4/#11) is the clearest case of named-but-not-understood — a person and a term with no content attached.

## 10. On-screen text vs. narration / picture-line mismatch
- **SHOULD FIX** — Ch3: the narration recites the spec verbatim ("Wait for every task it starts. When one fails, cancel the rest and pass the error on. And when the caller gives up, cancel them all.") while the screen shows *"three short lines, the spec, each appearing as it is said"* — i.e. the exact same words, simultaneously. This is pure duplication, the text adds nothing the ear didn't just get.
  - Rewrite: compress the on-screen text to labels/icons rather than full sentences — e.g. "① wait", "② fail → cancel + raise", "③ caller gone → cancel all" — so the checklist is a visual anchor for ch5's payoff, not a subtitle track for ch3.
- The ch5 reappearance of the same checklist, now ticked with measured numbers beside each item, is the opposite case and works well — that's payoff, not duplication. No fix needed there.

## 11. Lines deletable without breaking anything
- **NIT** — *"That rule is called structured concurrency, a name Martin Sústrik had given it two years earlier."* Can be cut entirely; nothing downstream refers to Sústrik or uses the coinage. If kept, it should do more work (e.g., tie to the "not just Python" theme — he coined it for network programming, outside any language's async system).

No other lines look purely decorative — the sequential-handler chapter (ch2), the retry-loop limit (ch6), and the Go chapter (ch7) all carry load the ending later reuses.

## 12. Hard-to-follow sentences / rushed or padded beats
- **SHOULD FIX** — Ch7: *"An error group works with a context, Go's standard way of passing cancellation, and deadlines, to goroutines."* The appositive interrupts subject→verb awkwardly and "and deadlines," dangles mid-clause — hard to read aloud without a stumble.
  - Rewrite: *"An error group works with a context — Go's standard way of passing cancellation and deadlines to goroutines."*
- **NIT** — Ch6: *"Here's a retry loop with a bare except, an except with no type, which catches everything, cancellation included."* Three stacked appositives in one breath.
  - Rewrite: *"Here's a retry loop with a bare except — no exception type — so it catches everything, cancellation included."*
- **SHOULD FIX (pacing)** — Ch4 is the densest chapter per second: Dijkstra (1968) + structured programming, Smith (2018) + essay title, Sústrik (2016) + coinage, Trio, and asyncio 3.11, all in roughly six sentences. Cutting Sústrik (per #11) would give the Dijkstra→Smith analogy — the actual spine of the chapter — more room, rather than competing with a third, undeveloped attribution.

No chapter reads as padded; ch2 is the closest (mostly restates "one way in, one way out" before the timing punchline), but it's short enough not to drag.

---

## Findings summary

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | SHOULD FIX | Ch1 screen counter | "0.12 s" conflicts with the "0.10 s" anchor number used everywhere else |
| 2 | SHOULD FIX | Ch3 screen | On-screen spec checklist duplicates narration verbatim in real time |
| 3 | SHOULD FIX | Ch7 | Awkward appositive sentence on "context" |
| 4 | SHOULD FIX | Ch4 | Sústrik mention adds density without payoff, crowding the chapter's real spine |
| 5 | SHOULD FIX | Ch5 | ExceptionGroup's stated purpose (multiple errors) is never exercised in the demo |
| 6 | NIT | Chain step 7 | "But" marks an additive move, not a real contrast |
| 7 | NIT | Ch6 | Two of three limits are asserted, not demonstrated (one flagged already as deliberate) |
| 8 | NIT | Ch6 | Stacked appositives in the retry-loop sentence |
| 9 | NIT | Ch7 | Kotlin/Swift/Java named but not shown |
| 10 | NIT | Ch4 | Sústrik line is deletable outright |

VERDICT: PASS
