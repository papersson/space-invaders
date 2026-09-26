Playing the role: industry engineer, knows async/await and APIs at a practical level, hasn't studied structured concurrency theory. Going through once, in order.

## 1. Points where I'd lose the thread

- **"it asks two services at the same time, with asyncio.gather"** — just a name dropped in the opening. I know roughly what it does from using Python, but the video hasn't told me anything about it yet, so I'm taking this on faith.
- **"So the handler returns an error at a tenth of a second... But the request to the user service is still running."** — this is the hook, so it's supposed to be surprising, but on first hearing it's genuinely confusing: if the function returned, what does "still running" even mean? I don't yet have a mental model for how something can outlive the function that started it.
- **"Now serve a thousand requests at once... a thousand tasks are still running."** — the number 1,000 lands with no consequence attached. Still running *so what*? Leaking memory? Holding open connections? I'm told it's bad but not why, yet.
- **"Starting a task is different from calling a function. The start returns at once, and the task runs on by itself."** — asserted, not explained. Why does starting behave this way mechanically? Is this a Python design choice or something fundamental to concurrency? I'm just told to accept the distinction.
- **Section 4, in one breath: "In 1968, Edsger Dijkstra... structured programming... Fifty years later, in 2018, Nathaniel Smith... That rule is called structured concurrency, a name Martin Sústrik gave it."** — three names, two dates, two coined terms arrive almost back to back. I lost track of who gets credit for what — did Sústrik and Smith find this independently, or is Sústrik just naming Smith's idea?
- **"The request arrives at the task's next await."** — stated as fact with no mechanism. Why would cancellation need to wait for an await point? Left me wanting the "why," not just the "what."
- **"asyncio still has plain create_task, and a task started that way is on its own again."** — the task-group code earlier used `tg.create_task`. Nothing in the narration flags that `tg.create_task` and plain `asyncio.create_task` are different calls with different guarantees — I'd have to notice that myself from the code, not the words.
- **"An error group works with a context, Go's standard way of passing cancellation, and deadlines, to goroutines."** — two new concepts (cancellation *and* deadlines) folded into one clause, on top of "goroutines" and "context" both being assumed-known Go jargon.

## 2. Questions I'd ask afterward

- Why does a `CancelledError` only get delivered at an `await` — what's actually happening under the hood there?
- Is `TaskGroup` a totally different mechanism from `gather`, or a wrapper around the same primitives with stricter bookkeeping?
- What's the real-world cost of those "1,000 leftover tasks" — memory, open sockets, what?
- If a task inside a `TaskGroup` never hits an `await` (e.g., pure CPU work or a blocking call), does the whole block just hang waiting for it?
- Did Sústrik and Smith arrive at this independently, or did one build on the other?
- Practically: do I need to rewrite every `gather` call I have, or only ones where a partial failure actually matters?

## 3. What I learned (~150 words, without looking back)

There's a bug pattern in async code where you fire off two requests at once (with something like `gather`), one fails fast, your function returns an error — but the other request is *still running* in the background, unowned, and if it fails too, nobody hears about it. At scale (thousands of requests) this leaves piles of orphaned work. The fix is called "structured concurrency": instead of just starting tasks loosely, you start them inside a block (a "task group") that cannot finish until every task inside it has finished. If one task fails, the block cancels the rest and surfaces the error; if the caller is cancelled, everything inside the block is cancelled too. This is compared to Dijkstra's old argument against `goto` — an unstructured jump you can't reason about — with the task group as the modern "block" that restores the guarantee that when something returns, it's actually done.

## 4. Direct answers

- **One main idea:** give every started task an "owner" — a block that can't complete until its children do — so that a function returning actually means all its work is finished, not just that the fastest failure came back first.
- **Numbers I remember and what they mean:** 1 second = how long the user-service call takes; 0.1 seconds = how fast the orders-service call fails (and where the buggy handler returns early); 1,000 = number of simultaneous requests used to show the leftover-tasks problem at scale; 1968 = Dijkstra's goto paper; 2018 = Smith's structured concurrency essay.
- **Question the video opened with:** the handler already returned — so why is its work still running, and what would make "returned" actually mean "done"?
- **Its answer:** wrap concurrent task-starting in a structured block (a task group) that owns every task it starts, waits for all of them, cancels the rest on failure, and propagates cancellation from the caller — then "returned" really does mean "done."

## 5. Ratings

- **Pull of the opening (1–5): 4** — a concrete, relatable "your code has a bug you can't see" scenario with a real number (1,000 orphaned tasks) is a strong hook for someone who writes this kind of code.
- **How often I felt lost: a few times** — mainly the names-and-dates cluster in section 4, and the unflagged difference between `tg.create_task` and plain `create_task` in section 6.
