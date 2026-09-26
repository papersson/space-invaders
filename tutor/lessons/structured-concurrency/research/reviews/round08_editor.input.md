You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** A Python request handler asks two services at once, with `asyncio.gather`: the user service takes one second, and the orders service fails after a tenth of a second. The handler returns an error at 0.10 s, but its request to the user service runs on until 1.00 s; if that request fails, its error goes nowhere, not even to a log. Serve 1,000 requests at once, and all 1,000 handlers return within about a tenth of a second while 1,000 tasks are still running. The function returned. Why is its work still running, and what would make "returned" mean "done"?

**Answer.** Starting a task splits control into two paths, and nothing makes the second one come back. `gather` waits for results, but it doesn't own the tasks: on the failure path it passes the first error on at once and leaves the other task running. Plain sequential calls get "returned means done" from their structure: one way in, one way out. That is Dijkstra's argument against `goto`, and Smith's against the "go statement". Structured concurrency restores it: tasks are started inside a block (a task group in asyncio, a nursery in Trio, a scope elsewhere), and the block can't end until every task in it has finished. Three guarantees follow: the block waits for its tasks; when one fails, the others are cancelled and the error reaches the caller; cancelling the caller cancels its tasks. Measured: with a task group the user request is cancelled at 0.10 s, and after 1,000 requests no tasks are left. Its limits: cancellation is a request that a task must reach an `await` to receive (a retry loop with a bare `except` held the block open until 1.10 s); only tasks started inside the block are covered; and it says nothing about data races or deadlocks. The same rule exists in Kotlin, Swift and Java (in preview), and in Go as a convention (errgroup with a context: 1,000 goroutines left behind with bare goroutines, none with the group).

**Takeaway.** Give every task an owner: start concurrent work inside a block that waits for it, cancels it when something fails, and hands you its errors. Then a function that has returned is really done.

**Wrong model.** If my function waits for all the tasks it starts (with `gather`, or by awaiting each one), its concurrent work behaves like a function call: when it returns, the work is done and every error has reached me.

**Objectives.**
1. Explain why starting a task breaks "returned means done", with its symptoms: work left running, errors that go nowhere, cancellation that doesn't reach every task.
2. State the rule of structured concurrency (a task can't outlive the block that started it) and its three guarantees.
3. Rewrite a `gather` fan-out with `asyncio.TaskGroup`, and predict what happens when one call fails or the caller gives up.
4. Name its limits: cancellation needs the task's cooperation; only tasks started inside the block are covered; data races and deadlocks are a separate problem.


## Chain

1. The question: the handler returned an error at 0.10 s, but its request ran on until 1.00 s, and 1,000 requests left 1,000 tasks running. Why, and what would make "returned" mean "done"?
2. Therefore look at what a plain call promises: one way in, one way out, so when it returns it's done, its error reached you, and cancelling you cancels it. But one call after the other is slow (1.10 s).
3. Therefore we start tasks, but starting a task splits control and nothing brings the second path back: `gather` waits for results, not tasks, so on the failure path it leaves the other one running (and awaiting tasks one at a time lets a cancellation miss the other). Therefore a fix must wait for every task, cancel the rest when one fails and pass the error on, and cancel them all when the caller gives up.
4. Therefore the principle: this is `goto` again; structured programming fixed jumps with blocks, and structured concurrency fixes tasks with a block they can't outlive.
5. Therefore the same handler in a task group: the three requirements met, measured.
6. But the block can only ask: cancellation needs the task's cooperation (a bare `except` held the block open until 1.10 s), and it covers only tasks started inside, not shared data.
7. But this isn't a Python quirk: the same handler in Go leaves 1,000 goroutines behind with bare goroutines and none with an error group, Go's convention for the same block; Kotlin, Swift and Java have it built in.
8. Therefore the answer.

Deviations from the canonical progression: the canonical worked example (a handler that fans out to two services, one of which fails) is kept, told in Python rather than Java, because `asyncio.TaskGroup` is stable in the standard library and runnable here, while Java's `StructuredTaskScope` is still a preview API. The race policy (first success wins, as in Happy Eyeballs), supervisor scopes, timeouts as scopes, and escape hatches beyond one sentence are left out; the research lists them as common extras.


## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Here's a web request handler, written in Python. It needs a user and that user's orders, so it asks two services at the same time, with asyncio.gather.
> The user service takes one second. The orders service fails after a tenth of a second.
> So the handler returns an error at a tenth of a second. So far, that's what you'd want.
> But the request to the user service is still running. It finishes a full second after the request began, long after anyone was waiting for it.
> And if it had failed, its error would go nowhere. Nothing raises it, and nothing logs it.
> Now serve a thousand requests at once. All thousand handlers return almost at once, and a thousand tasks are still running.
> The function returned. Why is its work still running? And what would make "returned" mean "done"?

*Screen:* a code card (sims/handler.py, `handler_gather`): `user, orders = await asyncio.gather(fetch_user(), fetch_orders())` inside a `try`. Below it, a timeline from 0 to 1.4 s (data/timeline.json, "gather"): a bar "fetch_user" from 0 to 1.00 s and a bar "fetch_orders" from 0 to 0.10 s ending in a red cross; a vertical line at 0.10 s, "handler returned an error". The part of the fetch_user bar after that line turns amber: "still running". Then the variant run ("gather_late"): the bar ends at 1.00 s in a cross labelled "TimeoutError", with an arrow from it to an empty circle. Then a counter from the real run: "1,000 requests at once · all handlers returned · tasks still running: 1,000". The question.

### 2. What a call promises

> Start with plain code: fetch the user, then fetch the orders, one after the other.
> Each call has one way in and one way out. When fetch_user returns, it's finished. If it fails, the error comes back to the caller. And if the caller gives up, say the client hangs up, the server cancels it: it asks the code to stop, and the call it's waiting on stops too.
> So when the handler returns, everything it started is done. You can treat it as a black box.
> But it's slow. The calls wait for each other, so the error arrives after one point one seconds.
> That's why we start the two requests at the same time.

*Screen:* the sequential handler as a code card (`user = await fetch_user()` then `orders = await fetch_orders()`). Control drawn as one arrow entering the top of the handler box, passing through fetch_user and fetch_orders, and leaving at the bottom: "one way in, one way out". The real run ("sequential") as a timeline: fetch_user 0 to 1.00 s, then fetch_orders 1.00 to 1.10 s with a cross; the handler's line at 1.10 s. Label "1.10 s".

### 3. Starting a task

> Starting a task is different from calling a function. The start returns at once, and the task runs on by itself. Control splits into two paths, and nothing makes the second one come back.
> There are two common ways to wait for tasks, and both leave gaps.
> The first is gather. You'd expect it to behave like those calls. It waits for both results, and when both requests succeed, it does.
> But when one fails, gather by default passes that error on immediately, and doesn't cancel the other task. Python's own documentation says so.
> That's the request left running in the opening. gather waited for results. It never owned the tasks.
> The second way is to start both requests, then await them one at a time, the user request first. If the client gives up after half a second, the user request is cancelled, because it's the one being awaited. The orders request isn't, and runs on to the end.
> So a real fix has to do three things. Wait for every task it starts. When one fails, cancel the rest and pass the error on. And when the caller gives up, cancel them all.

*Screen:* the arrow picture again: one arrow enters the handler; at "start a task" it splits into two, and the second arrow leaves the box sideways with no way back (amber). Then the gather timeline from chapter 1 again, the Python docs' own sentences beneath it (asyncio.gather, research/verified_primary_sources.md), the first sentence appearing with "immediately" and the second with "doesn't cancel": "If return_exceptions is False (default), the first raised exception is immediately propagated to the task that awaits on gather(). Other awaitables in the aws sequence won't be cancelled and will continue to run." A small gloss: "awaitables in the aws sequence: here, the two requests". Then a code card: `u = asyncio.create_task(fetch_user())`, `o = asyncio.create_task(fetch_orders())`, `await u`, `await o`, with a timeline from the real run ("cancel_create_task"), tagged on screen "this run: both requests take 1.0 s, neither fails": the client's timeout at 0.50 s; fetch_user cancelled at 0.50 s; fetch_orders runs on to 1.00 s (amber). Then the spec as three short labels with empty check boxes, each appearing as it is said: "wait for all", "one fails → cancel the rest, error out", "caller gone → cancel all".

### 4. Go to, again

> This problem is older than concurrency. In 1968, Edsger Dijkstra argued against the go to statement. With jumps that can lead anywhere, it becomes hard to follow what a program is doing from its text.
> The fix was structured programming: blocks, conditionals, loops and function calls, where control goes in at the top and comes out at the bottom.
> Fifty years later, in 2018, Nathaniel Smith pointed out that starting a task is the same kind of jump. Control goes in, and part of it never has to come out, so you can no longer treat a function as a black box. His essay was called "Notes on structured concurrency, or: Go statement considered harmful".
> The fix is the same too: a block. Tasks started inside it can't outlive it. The block doesn't end until every task in it has finished.
> That rule is called structured concurrency, a name Martin Sústrik had given it two years earlier. Smith built it into his own library, Trio, and Python's asyncio later added the same kind of block, the task group, in version three point eleven.

*Screen:* four small arrow diagrams side by side, drawn in turn (after Smith 2018): "sequential" (one arrow in, one out); "goto" (an arrow that jumps out of its box); "start a task" (an arrow that splits, one branch leaving the box); "block" (an arrow that splits inside a box and rejoins before the bottom edge). The block's box is labelled "task group". Then the code: `async with asyncio.TaskGroup() as tg:` with two indented `tg.create_task(...)` lines, and a bracket on the `async with` block: "tasks can't outlive this block". Names on screen: "Dijkstra 1968 · Sústrik 2016 · Smith 2018 · asyncio.TaskGroup: Python 3.11".

### 5. The same handler, in a task group

> Here's the handler again, with both requests started inside a task group.
> The orders service fails at a tenth of a second. At once, the task group cancels the user request, which asks it to stop, and waits until it has.
> Then it raises the error in the handler. It arrives inside an exception group, a container for errors, since more than one task could fail. So a plain except ConnectionError won't match it. The handler catches it with except star, which looks inside the group.
> At a tenth of a second the handler returns, and nothing it started is still running. So nothing is left to fail later, where no one would hear it.
> A thousand requests: all the handlers return, and no tasks are left.
> And if the client gives up after half a second, cancelling the handler cancels both requests inside it, not just the one being awaited.
> So a task group gives three guarantees. The block waits for every task started in it. When one fails, the others are cancelled and the error reaches the caller. And cancelling the caller cancels its tasks.

*Screen:* the task group code card (`handler_taskgroup`, ending `except* Exception as eg:` with a log line: `return` is not allowed inside an `except*` block), and the timeline from the real run ("taskgroup"): fetch_orders ends in a cross at 0.10 s; at the same moment the fetch_user bar is cut ("cancelled", blue); the handler's line at 0.10 s: "handler raised ExceptionGroup: [ConnectionError] (0.10 s)"; below the axis, "except ConnectionError: no match · except* ConnectionError: matches" (data/except_check.txt), then "tasks still running: 0". Then the counter: "1,000 requests · tasks still running: 0". Then the real run "cancel_taskgroup", tagged "this run: both requests take 1.0 s, neither fails": the client's timeout at 0.50 s, both bars cut at 0.50 s. Then the three lines of the spec from chapter 3 come back, and each check box is ticked as its guarantee is said, with the measured evidence beside it: "handler returned at 0.10 s, 0 tasks left", "fetch_user cancelled at 0.10 s · ExceptionGroup", "both cancelled at 0.50 s".

### 6. What it doesn't promise

> A task group can only ask a task to stop. The request arrives at the task's next await. It arrives as an exception, called CancelledError. A task that never awaits, or that catches that exception and carries on, keeps running.
> Here's a retry loop with a bare except: an except with no exception type, so it catches everything, cancellation included. When the orders service fails, the user request catches its cancellation and tries again.
> The task group has to wait for it. The handler returns after one point one seconds, instead of a tenth.
> Before, the stubborn work ran on after the handler returned. Now it can't escape the block, so the handler waits for it instead.
> And the rule covers only tasks started through the task group, with its own create_task. A task started with plain asyncio.create_task is on its own again.
> And it's about lifetimes, not shared data. Two tasks in the same group can still race on a variable, or deadlock.

*Screen:* a code card for the retrying fetch_user: `for attempt in (1, 2):`, `try: await asyncio.sleep(1.0) ...`, `except:  # a bare except: it catches CancelledError too`, with `retry` (sims/handler.py, `fetch_user_retrying`). The real run ("retrying"): fetch_orders' cross at 0.10 s; the cancellation arrow hits fetch_user at 0.10 s, "caught CancelledError, retrying" (amber), and its bar continues to 1.10 s; the handler's line moves out to 1.10 s. Then three small labels: "cancellation: a request, delivered at an await", "only tasks started inside", "not about shared data: races and deadlocks still possible".

### 7. Not just Python

> But this isn't a quirk of Python. Here's the same handler in Go, with plain goroutines. After a thousand requests, a thousand goroutines are left, and they never finish: each is waiting to hand its result to a handler that has already returned.
> Go has no task group in the language. A common convention is an error group, from Go's extended libraries: the closest thing Go has to a task group.
> An error group works with a context: Go's standard way of passing cancellation and deadlines to goroutines.
> With an error group, none are left. The first error cancels the context, and here each goroutine checks the context and returns. Like a task group, an error group can only ask.
> Swift and Java have the same kind of block built in, Java's still as a preview feature. Kotlin has it in its official coroutines library.

*Screen:* the real Go run (sims/goleak, data/runs.txt): the bare-goroutine handler reduced to its key lines (`go func() { u, _ := fetchUser(context.Background()); users <- u }()` and its twin for fetchOrders) and a small picture of one goroutine holding a result at a channel whose other end, the handler, is gone; then the count "bare goroutines: 1,000 left over" and, checked again 1.2 s later, after every request's one second has passed, "still 1,000" (amber). Then the errgroup handler's key lines (`g, ctx := errgroup.WithContext(...)`, `g.Go(func() error { _, err := fetchUser(ctx); return err })`) and "errgroup + context: 0 left over; 1.2 s later: 0" (blue). Last, one small line of names: "Swift: task groups (built in) · Java: StructuredTaskScope (built in, preview) · Kotlin: coroutineScope (kotlinx.coroutines library)".

### 8. The answer

> So why was the handler's work still running after it returned? Because starting a task split control into two paths, and nothing made the second one come back. gather waited for the results, but it didn't own the tasks.
> Structured concurrency gives every task an owner: a block that can't end until its tasks have. When one fails, the rest are cancelled and the error comes back. When the caller is cancelled, so are its tasks.
> The request fails at a tenth of a second, and at a tenth of a second nothing is left running.
> Give every task an owner, and "returned" means "done".

*Screen:* the chapter 1 timeline and the chapter 5 timeline stacked: gather (fetch_user runs on to 1.00 s, amber) above, task group (cut at 0.10 s) below; the counters "1,000 still running" and "0". Then the block diagram from chapter 4. End card with the takeaway and references: Smith, "Notes on structured concurrency, or: Go statement considered harmful" (2018); Sústrik, "Structured Concurrency" (2016); Dijkstra, "Go To Statement Considered Harmful" (title by the editor, Niklaus Wirth), CACM (1968); Python documentation, "Coroutines and Tasks" (Task Groups); JEP 533, Structured Concurrency (Seventh Preview, JDK 27), and JEP 543 (Candidate, proposing to finalize it in JDK 28); Kotlin documentation, "Composing suspending functions"; SE-0304, Structured concurrency (Swift).

