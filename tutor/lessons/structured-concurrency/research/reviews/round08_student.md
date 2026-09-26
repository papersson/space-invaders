Playing the role of the student-reviewer, here's my pass through the script.

## 1. Points where I'd lose the thread

- **"it asks two services at the same time, with asyncio.gather"** — this is dropped in the very first sentence, before anything explains what `gather` does. I only understood it retroactively once chapter 3 got to it.
- **"And if it had failed, its error would go nowhere. Nothing raises it, and nothing logs it."** — plausible-sounding but I'm being asked to accept a claim about error handling before I've seen any code showing *why* that's true.
- **"If the caller gives up, say the client hangs up, the server cancels it: it asks the code to stop, and the call it's waiting on stops too."** — three different things (finish / fail / caller-gives-up) land in one sentence. I had to replay it mentally to separate them.
- **"the error arrives after one point one seconds"** — I had to do the addition myself (1.0 + 0.1) to see where 1.1s came from; it isn't stated.
- **"If the client gives up after half a second"** — where does 0.5s come from? It's a new scenario (client timeout) introduced with a specific number and no setup for why that number, or why we're suddenly talking about the client instead of the orders service failing.
- **"It arrives inside an exception group, a container for errors... The handler catches it with except star, which looks inside the group."** — two new pieces of Python-specific vocabulary (`exception group`, `except*`) arrive back to back in the same breath. I know what a `try/except` is, but this syntax was unfamiliar and went by fast.
- **"A task started with plain asyncio.create_task is on its own again."** — this is a fine distinction from `tg.create_task` mentioned a moment earlier; the two names are similar enough that I could easily conflate them.
- **"Two tasks in the same group can still race on a variable, or deadlock."** — "race" and "deadlock" are used as if already defined; they aren't, in this script.
- **"a name Martin Sústrik had given it two years earlier"** — I had to hold three names and two years (2016, 2018) in my head at once; a bit of a juggling act for a side-note.

## 2. Questions I'd ask afterward

- What actually *is* `asyncio.gather`, mechanically — does it start the tasks itself, or just wait on ones already started?
- Why 0.5 seconds for the client-gives-up example — is that just an arbitrary illustrative number?
- What's the actual difference between `tg.create_task` and `asyncio.create_task` — is it just "which object you call it on," or is something structurally different happening?
- What is an exception group in Python, concretely — is it a list of exceptions? Can `except*` catch just one type out of the group and let others propagate?
- Is "structured concurrency" a Python-only fix, or a general concept independent of any one language? (The Go/Swift/Java/Kotlin section suggests the latter, but I wasn't sure until then.)
- Practically, when I write my own request handler tomorrow, what's the one-line rule of thumb — "always use TaskGroup instead of gather"?

## 3. What I learned (written without looking back, ~150 words)

A web handler used `asyncio.gather` to call two services at once. One failed fast (0.1s) so the handler returned an error quickly — but the other call (1s) kept running in the background even after the handler was done, and if it later failed, nobody would ever see that error. Multiply by a thousand requests and you get a thousand orphaned background tasks.

The reason: starting a task is different from calling a function — a function returns when it's done, but a task keeps running independently once started, and nothing forces it to "come back." `gather` waits for results but doesn't own the tasks it's waiting on.

The fix is called "structured concurrency": wrap tasks in a block (Python's `TaskGroup`) that can't finish until every task inside it has finished, and that cancels the others if one fails. This is compared to Dijkstra's old objection to `goto` — jumps you can't trace. Other languages (Go's errgroup, Swift, Java, Kotlin) have similar mechanisms.

## 4. Direct answers

- **One main idea:** Starting a background task creates an execution path that nothing guarantees will ever "come back"; you need a structural guarantee (a block/task group) that owns every task it starts, so that when the block exits, all its tasks are genuinely done — not just "gather returned."
- **Numbers I remember:** 1 second (user service), 0.1 second (orders service, fails), 1.1 seconds (sequential total), 1,000 requests / 1,000 leftover tasks (the "before" scaled-up problem) vs. 0 leftover tasks (the "after," with TaskGroup). I also recall a 0.5-second client-timeout number, though I wasn't sure why that particular value was chosen.
- **Question the video started with:** "The function returned. Why is its work still running? And what would make 'returned' mean 'done'?"
- **Its answer:** Because starting a task splits control into two paths and nothing forces the second path back; the fix is structured concurrency — a block (task group) that can't end until every task started in it has finished, cancels siblings on failure, and propagates cancellation from the caller — so that "returned" really does mean "done."

## 5. Ratings

- **Want-the-answer pull from the opening:** 4/5 — the "the function returned, so why is work still running?" hook, plus the "1,000 tasks still running" counter, made me want to know the fix.
- **How often I felt lost:** a few times — mainly around the `except*`/exception-group moment in chapter 5, and the unexplained 0.5-second client-timeout number in chapter 3.
