Playing the role: here's my reaction as that industry viewer, going through the script once, in order.

## 1. Where I'd lose the thread

- **"it asks two services at the same time, with asyncio.gather"** — I know async/await from building services, but `asyncio.gather` is just named here, not explained. I'm trusting it means "run both and wait," but its actual behavior (what happens on partial failure) isn't given until chapter 3 — so for two chapters I'm holding an unexplained term.
- **"Starting a task is different from calling a function. The start returns at once, and the task runs on by itself. Control splits into two paths, and nothing makes the second one come back."** — This is the pivot of the whole video and it's delivered as a metaphor (arrows splitting) rather than a mechanism. I don't actually know *what code* "starts a task" vs. "calls a function" — is `await fetch_user()` a call and `create_task(fetch_user())` a start? I have to infer that from the later code card, not from this sentence.
- **"the first raised exception will be immediately propagated" ... "Other awaitables in the aws sequence won't be cancelled"** — "aws sequence" reads exactly like "AWS" (Amazon Web Services) on first hearing/reading. Even setting that aside, "awaitables" is dropped without a definition — I know "await" as a keyword, not "awaitable" as a noun for a thing you can await.
- **"It arrives wrapped in an exception group: a task group always bundles its tasks' errors, even when there's only one."** — I don't know what an exception group actually *is* structurally (a list of errors? a new exception type you catch differently?). It's named and asserted, not shown.
- **"The request arrives at the task's next await, as an exception."** — Why "at the next await" specifically? Nothing explains that asyncio only switches between tasks at await points, so this rule lands as an arbitrary fact rather than a consequence of something I understand.
- **"a name Martin Sústrik gave it in 2016"** mentioned right after "Fifty years later, in 2018" — three names and three years (1968, 2018, 2016) arrive in quick succession and out of chronological order. I'd have to replay this to keep Dijkstra/Smith/Sústrik straight.
- **Screen note on the "gather_late" variant**: "an arrow from it to an empty circle" — this visual isn't narrated at all, so I don't know what the empty circle means (an error being swallowed? a listener that's gone?).
- **"Its convention is an error group, together with a context, which is Go's standard way of telling goroutines to stop."** — "context" is doing a lot of work here with zero explanation of what it actually contains or how a goroutine "checks" it.

## 2. Questions I'd ask afterward

- What line of code, concretely, is the difference between "calling" and "starting a task"? (await vs. create_task?)
- What does an exception group actually look like when you catch it — is it iterable, does `except ValueError` still work inside one?
- Why is cancellation only delivered at an `await`? What if a task is doing CPU work with no awaits — is it just unkillable?
- Is `gather` ever *safe* to use, or should I basically never reach for it now that TaskGroup exists?
- Does a bare `except:` catching `CancelledError` break anything else in asyncio, or is retry-loops-catching-cancellation a narrow gotcha?
- In Go, does *every* goroutine need to manually check `ctx.Done()`, or is that automatic once you use errgroup?

## 3. What I learned (written without looking back, ~150 words)

A web handler kicks off two requests at once with `asyncio.gather`. One fails fast, the handler returns an error — but the other request keeps running in the background, unseen, because `gather` waits for results but doesn't actually own the tasks it started. Multiply by a thousand requests and you get a thousand orphaned tasks. This is compared to Dijkstra's old argument against `goto`: once control can jump somewhere and never come back, you can't reason about code as a self-contained block. The fix, called "structured concurrency," is to run tasks inside a block (Python's `TaskGroup`) that can't finish until every task it started has finished — if one fails, the rest get cancelled and the error surfaces to the caller. But it only cancels at the task's next `await`, only applies to tasks started inside that block, and doesn't prevent shared-data races. Go, Kotlin, Swift, and Java all have versions of the same fix.

## 4. Direct answers

- **One main idea:** give every concurrent task an "owner" (a block that must wait for it) so that a function returning actually means all the work it started is done.
- **Numbers I remember:** a tenth of a second (0.1s) for the failing request, one second (1.0s) for the slow one, and 1,000 requests → 1,000 leftover tasks with plain `gather`/goroutines vs. 0 leftover with a task group/errgroup. I don't remember the exact 0.12s or 1.2s figures precisely — those blurred together.
- **Starting question:** why is the handler's work still running after the handler already returned an error? **Answer:** because starting a task splits control into two paths and nothing forces the second path back before the function returns — fixed by wrapping the tasks in a block that owns their whole lifetime.

## 5. Ratings

- **Want-the-answer pull of the opening:** 4/5 — the "returned but still running, and nothing hears the error" hook was concrete and unsettling in a way I recognize from production incidents.
- **How often I felt lost:** a few times — mainly around "aws sequence"/"awaitables," the undefined mechanics of "exception group," and the rapid-fire Dijkstra/Sústrik/Smith date sequence.
