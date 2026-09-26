## 1. Points of confusion (quoted)

- **"the server cancels it: it asks the code to stop, and the call it's waiting on stops too."** — Cancellation is introduced here for the first time, packed into a sentence about something else (what a call promises). I don't yet know *how* a stop request is delivered, so this reads as an assertion, not an explained mechanism.
- **"gather... waits for both results, and when both requests succeed, it does."** — The "it does" dangling at the end made me reread the sentence to figure out what "does" refers to.
- **"it doesn't cancel the other task"** followed immediately by the quoted Python docs sentence — two sources of the same fact stacked back to back; I wasn't sure if the doc quote was adding new information or just restating.
- **"it arrives inside an exception group, a container for errors... the handler catches it with except star, not a plain except."** — `except*` is new syntax dropped in one clause. I'm told what it's *for* (multiple errors) but not really shown why a normal `except` couldn't do the same job — I'll just have to trust it works differently.
- **"The request arrives at the task's next await. It arrives as an exception, called CancelledError."** — Two new facts in one breath: cancellation is delivered *at an await point*, and it's *implemented as an exception*. Either one alone I could track; together, back to back, I had to stop and separate them.
- **"With an error group, none are left. The first error cancels the context, and here each goroutine checks the context and returns."** — In two sentences I get errgroup, context, and "checks the context" as a new mechanism, without it being said what "checking the context" looks like in code (unlike the Python examples, which showed the actual lines).
- **"Sústrik had given it two years earlier"** — I have to do date math (2018 minus two = 2016) to place this in the timeline; a bare "in 2016" would have been easier to hold onto while listening.

## 2. Questions I'd ask afterward

- When exactly does a cancellation request get delivered if the code inside the task never hits another `await`? Does it just never get cancelled?
- Why does catching cancellation with a bare `except` "count" as catching `CancelledError` — is `CancelledError` just a normal Python exception under the hood?
- What actually happens to the *thousand* stuck tasks in the gather/goroutine case — do they eventually get garbage collected, or do they leak memory/connections forever?
- Is `except*` only usable with task groups, or is it a general Python 3.11 feature I'd reach for elsewhere?
- If two tasks in the same group can still race on a variable, does structured concurrency give me *any* tool for that, or is it a completely separate problem I need a different pattern for?

## 3. What I learned (written without looking back, ~150 words)

When you fire off two network calls at once and one fails fast, the code often returns an error immediately — but the *other* call is still running in the background, unowned, and if it fails too, nobody ever finds out. This happens because "starting a task" (as opposed to calling a function normally) splits control flow into two paths, and nothing guarantees the second path gets joined back. The common tool for waiting on multiple tasks, `gather`, doesn't fix this: it waits for results but doesn't own or cancel the tasks. The fix is called "structured concurrency": wrap task-starting in a block (in Python, `TaskGroup`) that can't finish until every task inside it is done, and that cancels everything else the moment one task fails. This isn't Python-specific — Go, Swift, Java, and Kotlin all have their own version of the same idea, because the same leaking-task problem shows up everywhere.

## 4. Direct answers

- **One main idea:** starting a background task splits control flow in two, and nothing guarantees the "other half" ever finishes or gets checked — structured concurrency fixes this by putting every task inside a block that owns it and can't exit until it's done.
- **Numbers I remember:** 0.1 seconds (orders service fails), 1.0 second (user service normally takes), 1,000 requests all leaving background tasks behind with plain `gather`, vs. 0 left over with a task group; 1968 (Dijkstra/goto), 2018 (Nathaniel Smith's essay).
- **Question it started with:** why is a task's work still running after the function that started it has already returned — and what would make "returned" actually mean "done"?
- **Its answer:** give every task an owner — a block (task group / errgroup / etc.) that can't end until its tasks have, that cancels the rest on failure and propagates the error, and that cancels everything if the caller itself is cancelled.

## 5. Ratings

- **Pull of the opening (1-5):** 4 — the concrete "1,000 tasks still running and nobody knows" hook made me want to know the fix.
- **How often I felt lost:** a few times — mostly around the `except*`/exception-group syntax and the Go section, where several new terms landed in quick succession.
