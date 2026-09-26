# Review

I checked every timing/count against the evidence table, the described asyncio/Go/JVM semantics against what I know of the actual APIs, and the citations against known publication facts. The script is unusually well-grounded — nearly every number traces to a cited real run rather than an invented example, and the framing (gather doesn't own its children; a task group does; cancellation is cooperative and only covers what's inside the block) is accurate and correctly scoped, without overclaiming that structured concurrency prevents races or deadlocks. Two issues need attention before this ships.

---

**BLOCKING — unverified/likely-wrong JEP citation**
> "JEP 505/533 and JEP 543, Structured Concurrency"

I can't confirm these numbers, and they don't match the sequence I know for this feature (428 incubator/JDK 19, 437 second incubator/JDK 20, 453 preview/JDK 21, 480 third preview/JDK 24, 499 fourth preview/JDK 25). It's plausible that later preview rounds for JDK 26/27 and a JDK 28 finalization proposal exist with new numbers, but I have no way to verify that from here, and the "505/533" pairing (with a slash, as if they're alternatives) reads like a possible mix-up rather than a deliberate "Nth preview + finalization" pair. A wrong JEP number on an end card is exactly the kind of citation error a professor would flag immediately, and it's trivially checkable. **Fix:** before finalizing, look up the current JEP index at openjdk.org and cite the exact preview JEP live for JDK 27 plus the finalization JEP (if JEP 543 really is it, keep it, but drop the "505/533" pairing or make clear what each one is, e.g. "JEP 499 (Fourth Preview) ... JEP 543 (proposed to finalize in JDK 28)").

**SHOULD FIX — on-screen citation only supports half the spoken claim**
> "But when one fails, gather passes that error on immediately, and doesn't cancel the other task. Python's own documentation says so."
> *Screen:* "...the docstring quoted small beneath it... 'the first raised exception will be immediately propagated'."

The quoted docstring line backs only "passes that error on immediately." The "doesn't cancel the other task" half is backed by a different source per the evidence table (the prose docs: "Other awaitables in the aws sequence won't be cancelled and will continue to run"), which never appears on screen. Since the narration explicitly says "documentation says so" for both halves of the claim, a viewer fact-checking against the screen only sees proof of one. **Fix:** add the second quote beneath the first, or split them so each spoken clause has its matching on-screen text.

---

Everything else checked out:
- All Python/Go timings and arithmetic (0.1 s, 1.0 s, 1.1 s, 0.5 s, the retry's 0.1 + 1.0 = 1.1 s, "fifty years" 1968→2018, 1,000-request counts) are internally consistent and match the cited runs.
- The gather/create_task/TaskGroup semantics (immediate propagation without cancelling siblings; cancelling the awaited task in a manual create_task pair while the other runs on; TaskGroup's immediate cancel-and-wait plus ExceptionGroup wrapping even for a single exception; bare `except:` catching `CancelledError` because it's a `BaseException` since Python 3.8, unlike `except Exception:`) are all correct and precisely worded.
- The claim that a failed, unretrieved gather-child exception is neither raised nor logged (unlike a normal orphaned task, which does log "Task exception was never retrieved") is a genuinely subtle, correct, and well-verified point — good that it's kept in.
- Historical/citation content (Dijkstra 1968 CACM, Sústrik's 2016 coinage, Smith's exact 2018 essay title, TaskGroup in 3.11, SE-0304, the Kotlin doc title) all check out against what I know.
- Caveats in chapter 6 (task-group scope is lifetime not data-safety; only tasks started via the group are covered; cancellation is cooperative) are appropriately placed and not overstated elsewhere.
- The Go section's hedging ("no task group in the language, but... a convention") and the "Java's is still a preview feature" caveat are correctly calibrated, not overclaiming portability.

VERDICT: REVISE
