## 1. Points where I'd lose the thread

- **"if it had failed, its error would go nowhere. Nothing raises it, and nothing logs it."** — Is that a general fact about orphaned asyncio tasks, or just true because this particular handler happens not to have a log line? I can't tell if "nothing logs it" is a guarantee or an assumption about the example.
- **"Control splits into two paths, and nothing makes the second one come back."** — This is the moment the video shifts to metaphor (arrows splitting) rather than code. I followed it because of the diagram, but on audio alone this sentence wouldn't have landed for me.
- **"Other awaitables in the aws sequence won't be cancelled and will continue to run."** — Reading the raw docs sentence with "awaitables" and "aws sequence" is dense even with the gloss underneath. I had to consciously translate "awaitables in the aws sequence" back to "the two requests."
- **"That rule is called structured concurrency, a name Martin Sústrik gave it in 2016."** — Third name/date dropped in a row (Dijkstra 1968, then Smith 2018, then Sústrik 2016) — and out of order, since Sústrik's 2016 comes *before* Smith's 2018 essay but is mentioned *after* it. I lost track of who did what.
- **"It arrives wrapped in an exception group: a task group always bundles its tasks' errors, even when there's only one."** — Why bundle a single error at all? The "even when there's only one" phrase raised a question it doesn't answer.
- **"The request arrives at the task's next await, as an exception."** — Two new facts in one sentence: cancellation is delivered *at an await point*, and it's delivered *as an exception*. Either one alone I could follow; together, back to back, I had to stop and unpack it.
- **"Its convention is an error group, used together with a context."** — Two unexplained Go-specific terms ("error group," "context") introduced in the same breath, right after I'd just gotten comfortable with "task group."

## 2. Questions I'd ask afterward

- Is not-cancelling-the-other-task in `gather` a deliberate design choice, or something more like an oversight/legacy behavior?
- What actually is an "exception group" as a data structure — a list of exceptions? How do you catch just one kind of error out of it?
- What does a task that "never awaits" look like in real code — is that common, or a corner case (e.g., a tight CPU loop)?
- The video says task groups are "about lifetimes, not shared data" and races/deadlocks are "still possible" — so what *do* you use to fix those? Is that a totally different tool?
- Does using a task group cost anything (extra waiting, always wrapping in exception groups) compared to `gather` when everything succeeds?
- In Go's errgroup, does `g.Wait()` behave exactly like awaiting a task group, or are there differences?

## 3. What I learned (written without looking back, ~150 words)

A web handler fires off two requests at once. One fails fast, the handler returns an error immediately — but the other request is still running in the background, orphaned, and if it fails too, nobody hears about it. Do this for a thousand requests and you get a thousand leaked background tasks. The reason: starting a task is like a `goto` — control forks and nothing guarantees the forked path comes back, which is the same problem Dijkstra flagged with `goto` in 1968. The fix is a "block" that owns every task started inside it: it can't finish until they're all done, a failure cancels the others and surfaces the error, and cancelling the block cancels everything inside it. Python calls this a task group; Go has no built-in version but gets similar behavior from errgroup+context. It only manages *when tasks end*, not shared-data bugs like races.

## 4. Direct answers

- **One main idea:** give every started task an "owner" (a block/task group) that can't exit until its tasks do — that's what makes "the function returned" actually mean "the work is done."
- **Numbers I remember:** the orders call fails at **0.1s**, the user call takes **1.0s** (sequential version takes **1.1s** total), a client that gives up does so at **0.5s**, and the demo scales to **1,000** requests — with `gather`, 1,000 tasks are still running after return; with a task group, 0.
- **Question the video started with:** the handler returned an error, so why is the other request still running — and what would make "returned" actually mean "done"?
- **Its answer:** because starting a task splits control with no path guaranteed to return; structured concurrency (a task-group block) fixes that by owning every task's lifetime, so failure/cancellation propagates and nothing is left running when the block exits.

## 5. Ratings

- **Pull of the opening (1–5):** 4 — a concrete, relatable bug ("the handler returned but work is still running, unlogged, at scale") hooked me quickly.
- **How often I felt lost:** a few times — mainly around the historical-names cluster (section 4) and the two dense mechanism sentences (exception groups, cancellation-as-exception).
