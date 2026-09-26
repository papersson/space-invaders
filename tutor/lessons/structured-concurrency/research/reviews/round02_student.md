# Student Review: "Structured Concurrency" Script

## (1) Points of confusion, quoted

- **"asks two services at the same time, with asyncio.gather"** — I don't know what `asyncio.gather` does yet; I have to infer it from context as the video goes.
- **"The user service takes one second. The orders service fails after a tenth of a second."** — fine, but then: **"So the handler returns an error at a tenth of a second."** — this is asserted as obvious ("so far, that's what you'd want") but I don't yet know *why* one failure makes the whole thing return early rather than waiting for both. It's presented as self-evidently correct behavior before I have a model of gather.
- **"And if it had failed, its error would go nowhere. Nothing raises it, and nothing logs it."** — a new claim (errors from orphaned tasks vanish) dropped in without explanation of the mechanism. Why would an error "go nowhere"? I'd want to know where errors normally go.
- **"Each call has one way in and one way out."** — clear enough, but then: **"if the caller gives up, say the client hangs up, asyncio cancels it: it tells the code to stop, and the call it's waiting on stops too."** — two new ideas in one sentence: (a) what "the caller gives up" / "hangs up" means mechanically, and (b) how cancellation propagates through a chain of calls. I'd lose the thread here — is cancellation automatic in *all* Python code, or specific to asyncio calls?
- **"Starting a task is different from calling a function. The start returns at once, and the task runs on by itself."** — okay, but immediately: **"Control splits into two paths, and nothing makes the second one come back."** — "control splits into two paths" is a visual/spatial metaphor I haven't been given a definition for; I get it from the diagram, but purely from narration this would lose me.
- **"gather passes that error on immediately, and doesn't cancel the other task. Python's own documentation says so."** — appeal to authority without stating *why* the designers chose this behavior. Feels like an arbitrary fact to memorize.
- **"If the client gives up after half a second, the user request... is cancelled. The orders request isn't, and runs on to the end."** — this is the third distinct failure mode presented in this chapter (gather-with-immediate-fail, gather... wait no, this is the sequential-await case). By this point three variants of "which task keeps running" are stacked up and I'd have trouble keeping straight which code pattern causes which leftover-task behavior.
- **"In 1968, Edsger Dijkstra argued against the go to statement... Fifty years later, in 2018, Nathaniel Smith pointed out that starting a task is the same kind of jump."** — the analogy is stated as a fact ("is the same kind of jump") rather than argued; I'd want the one sentence connecting *why* a goto and a spawned task are structurally alike, not just "these two people noticed a similar thing."
- **"It arrives wrapped in an exception group, a bundle of errors, because in general more than one task can fail."** — new term ("exception group") defined in the same breath it's used; workable, but it's one more thing to hold.
- **"cancellation... The request arrives at the task's next await, as an exception."** — this retroactively changes my understanding of cancellation from chapter 2/3 ("asyncio cancels it, it stops") into something more like "a request delivered later, only at an await point, as a catchable exception." This is a meaningfully different (more accurate) model arriving late — I felt mildly misled by the earlier simplification.
- **"a bare except, an except with no type, which catches everything, cancellation included."** — fine, defined inline, no issue.
- **"Go has no task group in the language, but it has a convention: an error group, with a context, Go's standard way of telling goroutines to stop."** — "context" is a Go-specific term used and only loosely glossed ("Go's standard way of telling goroutines to stop"); I don't code in Go, so I'm trusting this rather than understanding it.
- **Numbers with no attached meaning until later**: "0.10 s", "1.00 s", "0.12 s" fly by fast in chapter 1 before I know what a "task" or "gather" even is — I'm pattern-matching a timeline diagram rather than following the sentence.

## (2) Questions I'd ask afterward

1. Why does `gather` choose to propagate the first error immediately instead of waiting for/cancelling the rest — was that a deliberate design tradeoff, and what's the argument for it?
2. Is cancellation only ever delivered at an `await`? What happens if a task is doing CPU-bound work with no awaits — can it never be cancelled?
3. When two tasks in the same task group both fail, do I get both errors, or just the first, wrapped together? How would I handle each one differently?
4. Is a task group's cancellation "waiting" possibly unbounded — if a task ignores cancellation forever (like the retry example), can a task group hang forever waiting for it?
5. Are there real cases where you *want* a gather-style "fire and let it run" pattern, or is a task group strictly better in every scenario shown?
6. The video says task groups are "about lifetimes, not shared data" — so races/deadlocks are still my problem. What's the recommended tool for that (locks? something else)?

## (3) What I learned (~150 words, written without looking back)

When you start concurrent work with `asyncio.gather`, the function can return before everything it started has actually finished — if one of two parallel requests fails, gather immediately raises that error to the caller, but the other request keeps running in the background, unmonitored, and any error it eventually produces is silently lost. This happens because starting a task splits execution into two independent paths, and nothing guarantees the second path is ever waited on again — unlike a normal function call, which always returns to its caller. This is essentially the concurrent version of the old "goto" problem: uncontrolled jumps that don't structurally return. The fix is "structured concurrency" — wrapping task starts in a block (Python's `TaskGroup`) that cannot exit until every task inside it has finished, and that cancels all sibling tasks and propagates the error properly if one of them fails.

## (4) Answers

- **One main idea:** Give every started task an "owner" — a block (task group) that cannot finish until all its tasks finish — so that a function returning actually means all its work is done; ad-hoc concurrency (gather, bare goroutines, plain create_task) breaks this guarantee.
- **Numbers I remember and their meaning:** "0.1 seconds" = how fast the failing orders service fails; "1.0 second" = how long the user-service call takes, and thus how long the orphaned task keeps running after the handler already returned; "1,000 requests → 1,000 leftover tasks still running" = the same single-request bug multiplied to show it's a real production-scale leak, not a one-off curiosity.
- **What question did it start with, and what was the answer?** It started with: "The function returned. Why is its work still running, and what would make 'returned' mean 'done'?" The answer: because starting a task doesn't guarantee anyone waits for it; wrapping tasks in a structured-concurrency block (task group) guarantees the block won't finish until every task inside it does, so "returned" finally does mean "done."

## (5) Ratings

- **Want-the-answer pull of the opening:** 4/5 — the "still running after it returned, and nobody notices" hook is genuinely unsettling and made me want to know the mechanism, especially the "1,000 tasks still running" scale-up.
- **How often I felt lost:** a few times — mainly in chapter 3 (stacking three different leftover-task scenarios back to back) and at the cancellation redefinition in chapter 6, where the earlier simplified model ("asyncio cancels it, it stops") got quietly upgraded to "delivered at the next await, as an exception."
