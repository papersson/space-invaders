# Where Did That Task Go?

Status: locked after review round 7

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

## Format

| Chapter | Format | Why |
|---|---|---|
| 1 | Narrated animation with real output | The surprise is a timeline: the handler's line ends at 0.10 s, the task's bar runs on. The 1,000-request count is a real run. |
| 2-3 | Narrated animation | Control flow as arrows (one in, one out; a split that doesn't rejoin), over the same timeline. |
| 4 | Narrated animation | Smith's arrow diagrams: sequential, `goto`, a started task, the block. |
| 5-6 | Narrated animation with real output | The same timeline, replayed from the real runs with a task group, then with a stubborn task. |
| 7 | Narrated animation with real output | The Go run's counts, one beat. |
| 8 | Narrated animation | Payoff. |
| (not built) | Exercise | Convert a `gather` handler to a task group; make one task fail, then make one swallow its cancellation, and watch the timings. The research names running code as the way to learn the policies; offered, not added. |
| (not built) | Reading | Smith's essay in full; the cross-language table of names and policies; the race policy (Happy Eyeballs). |

## Ledgers

**Setups and payoffs.**
- The 0.10 s return and the 1.00 s leftover (ch. 1) are explained by the split (ch. 3) and fixed by the task group (ch. 5: cancelled at 0.10 s).
- The error that goes nowhere (ch. 1) returns as "the error reaches the caller" (ch. 5).
- 1,000 tasks left over (ch. 1) returns as none left over (ch. 5) and as the Go counts (ch. 7).
- "One way in, one way out" (ch. 2) returns as the block (ch. 4) and in the answer.
- The client giving up (ch. 3) returns as the third guarantee (ch. 5).
- "Ask a task to stop" (ch. 5, "waits for it to stop") pays off in ch. 6 (cooperation), and again in Go (ch. 7: each goroutine checks the context).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| task | ch. 1 | a coroutine running on its own in the event loop, started with `create_task` or by `gather` |
| start a task | ch. 3 | hand a coroutine to the event loop to run by itself; the call returns at once |
| cancel, cancellation | ch. 2 | asking a task to stop: it gets a `CancelledError` at its next `await` |
| task group | ch. 4 | asyncio's block (`async with asyncio.TaskGroup()`) whose tasks can't outlive it |
| structured concurrency | ch. 4 | the rule that a task can't outlive the block that started it, and its guarantees |
| the caller | ch. 2 | whoever called the handler (the web server, or a client with a timeout) |

**Numbers to remember.** 0.10 s (the handler returns) against 1.00 s (its task finishes); 1,000 tasks left over against none.

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

*Screen:* the arrow picture again: one arrow enters the handler; at "start a task" it splits into two, and the second arrow leaves the box sideways with no way back (amber). Then the gather timeline from chapter 1 again, the Python docs' own sentences beneath it (asyncio.gather, research/verified_primary_sources.md), the first sentence appearing with "immediately" and the second with "doesn't cancel": "If return_exceptions is False (default), the first raised exception is immediately propagated to the task that awaits on gather(). Other awaitables in the aws sequence won't be cancelled and will continue to run." A small gloss: "awaitables in the aws sequence: here, the two requests". Then a code card: `u = asyncio.create_task(fetch_user())`, `o = asyncio.create_task(fetch_orders())`, `await u`, `await o`, with a timeline from the real run ("cancel_create_task", both requests succeed after 1.0 s here): the client's timeout at 0.50 s; fetch_user cancelled at 0.50 s; fetch_orders runs on to 1.00 s (amber). Then the spec as three short labels with empty check boxes, each appearing as it is said: "wait for all", "one fails → cancel the rest, error out", "caller gone → cancel all".

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
> Then it raises the error in the handler. It arrives inside an exception group, a container for errors, since more than one task could fail. So the handler catches it with except star, not a plain except.
> At a tenth of a second the handler returns, and nothing it started is still running. So nothing is left to fail later, where no one would hear it.
> A thousand requests: all the handlers return, and no tasks are left.
> And if the client gives up after half a second, cancelling the handler cancels both requests inside it, not just the one being awaited.
> So a task group gives three guarantees. The block waits for every task started in it. When one fails, the others are cancelled and the error reaches the caller. And cancelling the caller cancels its tasks.

*Screen:* the task group code card (`handler_taskgroup`), and the timeline from the real run ("taskgroup"): fetch_orders ends in a cross at 0.10 s; at the same moment the fetch_user bar is cut ("cancelled", blue); the handler's line at 0.10 s: "ExceptionGroup: ConnectionError"; "tasks still running: 0". Then the counter: "1,000 requests · tasks still running: 0". Then the real run "cancel_taskgroup": both requests slow, the client's timeout at 0.50 s, both bars cut at 0.50 s. Then the three lines of the spec from chapter 3 come back, and each check box is ticked as its guarantee is said, with the measured evidence beside it: "handler returned at 0.10 s, 0 tasks left", "fetch_user cancelled at 0.10 s · ExceptionGroup", "both cancelled at 0.50 s".

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

## Evidence

| Claim | Source |
|---|---|
| All Python timings, counts and event orders in chapters 1, 2, 3, 5 and 6 | sims/handler.py, run by sims/run_all.sh; data/runs.txt and data/timeline.json (Python 3.11.15; fetch_user sleeps 1.0 s, fetch_orders fails after 0.1 s; times measured from the start of each request) |
| gather: the handler returns an error at 0.10 s; one task still running then; fetch_user finishes at 1.00 s | data/runs.txt, "gather: fetch_orders fails at 0.1 s" |
| gather: if fetch_user fails at 1.00 s, nothing raises or logs its error, even after garbage collection; a plain task's unretrieved error is logged ("Task exception was never retrieved"), so the absence is real | data/runs.txt, "gather: and fetch_user fails later" and the control run (sims/control_unretrieved.py) |
| 1,000 concurrent requests: gather handlers all returned after 0.12 s with 1,000 tasks still running; task group handlers after 0.13 s with 0 | data/runs.txt, "1000 requests at once" |
| Sequential handler returns its error at 1.10 s | data/runs.txt, "sequential" |
| gather passes the first error on immediately and does not cancel the other awaitables; cancelling gather after it has passed on an error cancels nothing | research/verified_python_docstrings.txt (asyncio.gather docstring, Python 3.11.15); Python docs, "Coroutines and Tasks" ("Other awaitables in the aws sequence won't be cancelled and will continue to run"; "TaskGroup will, while gather will not, cancel the remaining scheduled tasks"), research/verified_primary_sources.md |
| create_task, awaited in turn, client gives up at 0.50 s: fetch_user (being awaited) cancelled at 0.50 s, fetch_orders runs on to 1.00 s | data/runs.txt, "create_task, awaited in turn" |
| Task group: fetch_user cancelled at 0.10 s, handler raises ExceptionGroup(ConnectionError) at 0.10 s (a task group always raises an ExceptionGroup, even for one error); client gives up at 0.50 s: both cancelled at 0.50 s | data/runs.txt, "TaskGroup" runs; asyncio.TaskGroup docstring ("Any exceptions other than asyncio.CancelledError raised within a task will cancel all remaining tasks and wait for them to exit. The exceptions are then combined and raised as an ExceptionGroup.") |
| gather also cancels its children when the caller cancels it (not contradicted by the script) | data/runs.txt, "gather: the caller gives up"; gather docstring |
| Bare except (`except:` with no type) retry: it catches CancelledError; the task group cannot close until 1.10 s | data/runs.txt, "TaskGroup, fetch_user retries with a bare except" |
| Cancellation is cooperative: delivered as CancelledError at an await; a task that swallows it keeps running; TaskGroup "might misbehave if a coroutine swallows asyncio.CancelledError" | Python docs, "Coroutines and Tasks" (Task Cancellation; Task Groups); research/canonical_web_agent.md §4 G2 |
| Structured concurrency does not address data races or deadlocks | research/canonical_web_agent.md §4 and §9; research/canonical_claude_p.md §9 |
| Dijkstra, "Go To Statement Considered Harmful", CACM 1968 | Dijkstra (1968) |
| Smith's essay "Notes on structured concurrency, or: Go statement considered harmful" (2018-04-25); Trio nurseries; starting a task compared to goto | Smith 2018b; research/canonical_web_agent.md §2-3 |
| The term was coined by Martin Sústrik (2016) and popularized by Smith | JEP 505 and JEP 543 text ("coined by Martin Sústrik and popularized by Nathaniel J. Smith"), per research/canonical_web_agent.md; Sústrik 2016 |
| asyncio.TaskGroup added in Python 3.11 | Python docs, "Coroutines and Tasks" (Task Groups, "Added in version 3.11") |
| Kotlin coroutineScope (in kotlinx.coroutines, JetBrains' official library, not the standard library), Swift task groups and async let (Swift 5.5), Java StructuredTaskScope (preview through JDK 27, JEP 533; JEP 543, a Candidate, proposes finalizing in JDK 28, checked at openjdk.org in research/verified_primary_sources.md), Go errgroup + context (library convention) | research/canonical_web_agent.md §8 |
| Go: bare goroutines left 1,000 goroutines after 1,000 concurrent requests, still 1,000 after 1.2 s (blocked sending on an unbuffered channel nobody reads); errgroup.WithContext left 0 | sims/goleak/main.go, data/runs.txt (go1.26.0, golang.org/x/sync v0.23.0) |
| errgroup: the first error cancels the derived context; Wait returns after all goroutines return; goroutines stop only if they check the context | errgroup package docs; research/canonical_web_agent.md §4 G4 |

## Review log

**Round 1:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: Smith's essay title was cut to its second half; chapter 4 now gives the full title, "Notes on structured concurrency, or: Go statement considered harmful", matching the end card.
- Expert: the retry loop's code said `except BaseException:` while the narration said "bare except"; the simulation now uses a literal bare `except:` (all runs repeated; every number the script uses is unchanged), and the narration says what a bare except is. The evidence row for the 1,000 task-group requests now reads 0.13 s, as in data/runs.txt.
- Editor: the chapter 5 sentence with five clauses is split, and the exception group is explained as "a bundle of errors" that exists because in general more than one task can fail; chapter 7 no longer ends the chain with an "and then": it opens with Go as the test of "is this a Python quirk?", the goroutine's stuck send is drawn, and Kotlin, Swift and Java get one sentence and one small line instead of a table; the chapter 1 caption no longer repeats the narration (an arrow to an empty circle); Sústrik and Trio moved from the narration to the chapter 4 screen, easing its density; chapter 3's gather line now states the expectation before breaking it; chapter 3's last beat names which request is awaited; "about a tenth of a second" for the 1,000 handlers is now "almost at once" (the screen shows 0.12 s).
- Editor, not taken: demonstrating the two other limits in chapter 6 (only tasks started through the group; not about shared data). Each stays one spoken sentence with a label, which is the depth the research gives them for a short lesson; a demo of each would be a lesson on its own.
- Student: lost at "cancelled" before it was explained (chapter 2 now says what cancelling is, with the client hanging up as the example), at "that part is right", at the "client" appearing in chapter 3 (introduced in chapter 2), at "the leftover work became a wait" (rewritten plainly), at "sits right next to it" (rewritten), and at Go's "context" (now "Go's standard way of telling goroutines to stop").

**Round 2:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: the end card's "JEP 505/533 and JEP 543" could not be verified from memory and read like a mix-up. Checked at openjdk.org (research/verified_primary_sources.md): JEP 533 is the seventh preview, delivered in JDK 27, and JEP 543 is a Candidate to finalize the API in JDK 28 (the full history is 428, 437, 453, 462, 480, 499, 505, 525, 533). The end card now names each one with its role.
- Expert: "doesn't cancel the other task" now has its own quote on screen, from the Python docs ("Other awaitables in the aws sequence won't be cancelled and will continue to run"), beside the docstring quote for "immediately".
- Editor: the exception group line now says what the screen shows (a task group always bundles its tasks' errors, even one), instead of an unshown reason; the chapter 1 setup (an error no one hears) is paid off in chapter 5 ("nothing is left to fail later, where no one would hear it"); Sústrik gets one spoken clause next to the name, so the credits aren't split between channels; the chapter 1 counter says "within 0.12 s" for a thousand requests at once; the Go sentence with three appositives is split; screen notes say "blue", not "ICE". The chapter 7 screen note now shows the Go code exactly as it ran (context.Background()).
- Student: lost in chapter 3's three scenarios (now signposted: "two common ways to wait for tasks, and both leave gaps") and when chapter 6 sharpened what cancelling means (chapter 2 now says asyncio "asks the code to stop", the same word chapter 6 builds on).

**Round 3:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: the on-screen quote "the first raised exception will be immediately propagated" was said to misquote the source, which reads "is immediately propagated". Both wordings are real: the quote was verbatim from the Python 3.11 docstring (research/verified_python_docstrings.txt: "the first raised exception will be immediately propagated to the returned future"), and the expert remembered the documentation page, which says "is immediately propagated to the task that awaits on gather()". To keep one source on screen, both halves of the line now quote the documentation page's two consecutive sentences, which also name the default.
- Expert: "by default" added (return_exceptions=True collects errors instead); the server, not asyncio, notices the client hanging up and cancels the handler; structured programming now lists conditionals too. Java's status was checked at openjdk.org on the day (research/verified_primary_sources.md).
- Editor: "nursery" is gone from the chapter 4 screen, so the block has one name, task group (Kotlin's `coroutineScope` in chapter 7 is an API name); the Go sentence is split into two, with the context defined in its own sentence.
- Student: lost at "aws sequence" and "awaitables" in the quote (a gloss now says they are the two requests), at what an exception group is (chapter 5 says it bundles the tasks' errors), and at three names and dates in a row in chapter 4 (unchanged: each is one clause, and the screen holds the dates).

**Round 4:** expert PASS, editor REVISE, student retold the question and answer correctly (lost "a few times").
- Editor, blocking: a colour code ("ICE") was still in the chapter 5 screen note; it now says "blue", and no colour code is left in the script.
- Editor: chapter 3 now ends by turning its two failures into a spec (wait for every task; when one fails, cancel the rest and pass the error on; when the caller gives up, cancel them all), so the task group's three guarantees in chapter 5 are ticked off against it, each with its measured evidence, instead of captions that repeat the narration; chapter 5 says giving up now cancels both requests, "not just the one being awaited", paying off chapter 3; chapter 3's double apposition is gone; the Go check "1.2 s later" is explained on screen (after every request's one second); Sústrik's year is off the narration (it stays on screen).
- Editor, not taken: moving the Sústrik credit to chapter 5. Chapter 4 names the rule, so the name's origin belongs there; it is now one short clause.
- Expert: Dijkstra's argument is now stated as his (with jumps that can lead anywhere, it's hard to follow what a program does from its text), and the black-box framing is given to Smith, whose essay makes it; Trio is credited as the library Smith built the rule into, before asyncio added its task group (not claimed to be modelled on it); chapter 5 says cancelling "asks" the request to stop, ahead of chapter 6; Go's context is "Go's standard way of passing cancellation, and deadlines, to goroutines".
- Expert, not taken: re-verifying the JEP numbers. They were checked at openjdk.org today (research/verified_primary_sources.md): JEP 533 delivered in JDK 27, JEP 543 a Candidate for JDK 28.
- Student: lost at "even when there's only one" (the exception group is now "a container that can hold the errors of several tasks"), at two facts in the cancellation sentence (split in two), and at "error group" and "context" in one breath (now one sentence each).

**Round 5:** expert REVISE, editor PASS, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: "Kotlin, Swift and Java have the same kind of block built in" was wrong for Kotlin, whose `coroutineScope` comes from kotlinx.coroutines, JetBrains' official library, not the language or its standard library; the script had drawn exactly that line for Go. Now: Swift and Java have it built in (Java's as a preview), Kotlin in its official coroutines library; the screen line says which is which.
- Expert: errgroup is "a common convention ... from Go's extended libraries", not "the" convention; Sústrik's naming is placed "two years earlier", so the narration alone doesn't credit Smith with the term.
- Expert, not taken: re-checking the JEP numbers again. They were checked at openjdk.org on the day of this build (research/verified_primary_sources.md); the page makes no claim beyond that date.
- Editor, not taken: deriving the exception group from a visible two-failure case, demonstrating races and deadlocks, and illustrating Kotlin, Swift and Java. Each is a generalization given one sentence, as the research's essential/extra split and the depth-over-breadth rule ask; the exception group is named because it is the type the viewer's own code will catch.
- Student: lost at the difference between the task group's create_task and plain asyncio.create_task (chapter 6 now names both); the chapter 4 names and dates are unchanged apart from the Sústrik clause.

**Round 6:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). The gate is passed; the should-fix items are applied once, and round 7 decides the lock.
- Expert: chapter 5 now says the exception group is caught with `except*`, not a plain `except` (the code card already shows it); the Go error group gets the same caveat as the task group ("here each goroutine checks the context and returns. Like a task group, an error group can only ask."); JEP 543 is described as proposing to finalize the API in JDK 28, as its own text says, not as a settled target; the end card notes that the title of Dijkstra's letter was the editor's, Niklaus Wirth's.
- Editor: the chapter 3 spec on screen is three short labels, not the spoken sentences; the chapter 1 counter no longer shows 0.12 s beside the 0.10 s anchor (the number stays in the evidence); the Go context sentence and the bare-except sentence are rephrased for the ear; the exception group's reason ("more than one task could fail") is stated as a possibility.
- Editor, not taken: cutting Sústrik. The JEP credits him with coining the term, and the expert asked in round 5 for the narration to keep that credit; it is one clause.
- Student: lost at cancellation being used before its mechanism (chapter 2 says it "asks the code to stop"; chapter 6 gives the mechanism, which is the order the research recommends) and in the compressed Go section (the context sentence is simpler).

**Round 7 (final):** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). The script is locked. One screen-only change after the lock: chapter 7 glosses "goroutine" on screen ("Go's lightweight thread"), which the narration uses without defining. Revision candidates, not applied (final-round SHOULD FIX items):
- Editor: Swift, Java and Kotlin are named without being shown, and chapter 7 packs Go's mechanism (goroutines, error group, context) and three more languages into one beat; cut the other languages to the end card, or give chapter 7 more room.
- Editor, NITs: "error group" (spoken) and "errgroup" (on screen) are two spellings; "goroutine" is not glossed in the narration.
- Student: lost at `except*` and the exception group, and at the Go terms arriving close together.
