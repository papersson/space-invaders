Playing the role of the viewer described, going through the script once, in order.

## 1. Points of confusion

- **"it asks two services at the same time, with asyncio.gather."** — I know Python and async/await from other languages, but I don't actually know what `gather` promises. The script uses it as if its behavior is obvious, then only explains what it actually does in chapter 3. Until then I'm just trusting the timeline picture.
- **"if the caller gives up, say the client hangs up, the server cancels it: it asks the code to stop, and the call it's waiting on stops too."** — "asks the code to stop" is vague. Stop how? This is stated as a fact about plain function calls, but the actual mechanism (an exception called `CancelledError`, delivered at an `await`) isn't given until chapter 6. For four chapters I'm holding an unexplained black box called "cancellation."
- **"gather by default passes that error on immediately, and doesn't cancel the other task."** — okay, but I still don't know *why* it doesn't cancel the other task — is that a design choice, a bug, a tradeoff? It's just stated as documented fact.
- **"That rule is called structured concurrency, a name Martin Sústrik had given it two years earlier."** — "two years earlier" than what — Smith's 2018 essay? I have to do the subtraction myself (2016) instead of just being told the year. Minor, but it's an unnecessary bit of mental arithmetic in the middle of a sentence about something else.
- **"A task started with plain asyncio.create_task is on its own again."** — this sentence uses "create_task" twice in nearby lines for two different things (`tg.create_task` inside the group vs. bare `asyncio.create_task`), and the distinction is exactly the kind of subtle API detail I'd need to pause and reread the code card for, not just hear once.
- **"Two tasks in the same group can still race on a variable, or deadlock."** — "race" and "deadlock" are dropped in with no definition, at the very end of a chapter, right after a much bigger claim ("it's about lifetimes, not shared data"). Two new ideas in one breath.
- **"Here's the same handler in Go, with plain goroutines."** — I don't write Go day to day. It's implied a goroutine is "like a task" but that equivalence is never stated outright, so I have to infer it from the diagrams.
- **"An error group works with a context, Go's standard way of passing cancellation, and deadlines, to goroutines."** — three new nouns (error group, context, deadlines) landing in one sentence about a language I'm already unsure of.

## 2. Questions I'd ask afterward

- What actually triggers a cancellation signal — is it always "the client disconnected," or can a handler cancel itself for other reasons (e.g. a timeout it sets itself)?
- If a task ignores cancellation (like the retry example), is there any way to force-kill it, or are you just stuck waiting?
- Does a task group add any latency overhead in the normal, all-succeeds case compared to `gather`?
- Is `TaskGroup` the *recommended* default in modern Python now, or is `gather` still used for cases where you *want* to keep going even if one call fails?
- The "races and deadlocks still possible" line at the end of chapter 6 — is there a follow-up concept (locks? actors?) that structured concurrency doesn't solve, that I should learn next?

## 3. What I learned (written without looking back, ~150 words)

A web handler fired off two requests at once. One failed quickly and the handler returned an error — but the other request kept running in the background, invisibly, even though the function had already "returned." Do that with a thousand requests and you get a thousand orphaned background tasks. The cause: starting a task (as opposed to calling a function) splits control flow into two paths, and nothing guarantees the second path ever rejoins. The tool people use for this, `gather`, waits for results but doesn't actually own the tasks it started, so a failure doesn't cancel siblings. The fix, called "structured concurrency," is to run tasks inside a block (Python's `TaskGroup`) that cannot exit until every task inside it is finished — so a failure cancels the others, and the caller giving up cancels everything too. It's compared to Dijkstra's old argument against "goto": once you let control jump out and not come back, you can't reason about the code from its text anymore.

## 4. Direct answers

- **One main idea:** give every background task an "owner" — a block that can't finish until all its tasks have — so that a function returning actually means its work is done.
- **Numbers I remember:** the failing call took a tenth of a second (0.1s), the slow call took a full second (1.0s); with plain `gather` the handler returns at 0.1s but the other task keeps running until 1.0s; with a thousand simultaneous requests, a thousand tasks were left running with `gather` versus zero with a task group.
- **Question it started with / answer:** "The function returned. Why is its work still running, and what would make 'returned' mean 'done'?" Answer: because starting a task, not just calling one, splits control flow without guaranteeing it rejoins — and wrapping tasks in a structured block (a task group) closes that gap.

## 5. Ratings

- **Pull of the opening (1–5): 4** — the "returned but the request is still running, and errors from it go nowhere" hook is concrete and slightly alarming in a way I recognize from real production bugs, so I wanted the explanation.
- **How often I felt lost: a few times** — mainly around cancellation being used loosely for three chapters before its mechanism (`CancelledError` at an await) was actually defined, and in the compressed Go section at the end.
