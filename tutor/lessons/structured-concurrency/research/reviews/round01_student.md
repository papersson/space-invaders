Watching as the persona described — here's my run-through.

## 1. Where I lost the thread (quoting)

- **"So the handler returns an error at a tenth of a second. That part is right."** — Right compared to what alternative? Nothing established yet that this *could* have been wrong.
- **"And if the caller is cancelled, the call it's waiting on is cancelled too."** (Ch. 2) — "Cancelled" gets used here like I already know what it means. I later learn in Ch. 6 that cancellation is "a request delivered at an await," but by then I'd already had to just accept the word on faith for four chapters.
- **"Start both, await the user request, and let the client give up after half a second. The request being awaited is cancelled. The other one runs on to the end."** (Ch. 3) — Two new things land in one breath: (a) a "client" appears out of nowhere — is that the browser/caller of the whole handler? — and (b) I'm supposed to track which of two tasks is "the one being awaited" vs. "the other one" without a label to hang onto.
- **"raises the error in the handler, wrapped in an exception group, because more than one task can fail."** — "Exception group" is defined in the same breath it's used, which is fine, but it's a brand-new vocabulary word slipped in right as three other new claims (cancels, waits, raises) are stacking up in the same sentence.
- **"The leftover work became a wait. Work can't escape the block any more, so a stubborn task holds the block open instead."** — This is the one place I'd have to rewind. "The leftover work became a wait" reads like a riddle — I get it eventually (the handler now blocks until the retrying task finishes), but it doesn't land on first listen.
- **"The rule also covers only tasks started inside the block. create_task still sits right next to it."** — "Sits right next to it" — next to *what*, physically or logically? I think it means "a `create_task` call written inside the `async with` block is still NOT protected," but the sentence doesn't say that plainly.
- **"Go has no such block, but it has a convention: an error group with a shared context."** — "Context" is doing a lot of unexplained work here (Go's `context.Context` is its own concept), and I only sort-of infer its role from the later line "each goroutine checks the context and returns."

## 2. Questions I'd ask afterward

- When exactly does a task actually get to "notice" it's cancelled — only at an `await`? What if a task is doing CPU work with no awaits at all — does it ever stop?
- What is an "exception group" mechanically — is it just a list of exceptions, or a new kind of object I'd need to catch differently in code?
- In the gather example, when the first request's error propagates immediately, where does the *second* task's eventual result or error actually go if nobody's `await`ing it anymore — silently dropped, or does it crash the process?
- Is a task group only a Python thing conceptually, or is "structured concurrency" a rule that every one of these languages enforces the same way, just with different syntax?
- What does "shared context" mean in Go — is that the same idea as the task group's block, or a weaker, manual version of it?

## 3. What I learned (written without looking back, ~150 words)

When you fire off two API calls at once with something like `asyncio.gather`, and one of them fails, the function can return an error while the *other* request is technically still running in the background — nobody's waiting for it, so if it errors too, that error just vanishes, and it's still eating up a thread/socket somewhere. Do that a thousand times and you've got a thousand zombie requests. The fix is a structured block — a "task group" — that owns every task you start inside it: the block literally cannot finish until all its tasks have finished, and if one task fails, the block cancels the rest and surfaces one combined error. The historical hook was surprisingly cool: this is basically the old "goto considered harmful" problem, except the "goto" is starting a task instead of jumping code, and the fix is the same shape — enforce single entry/exit.

## 4. Direct answers

- **Main idea:** A concurrent task needs an "owner" (a block/scope) that guarantees it can't outlive the code that started it — so "the function returned" actually means "all its work is done," not "some of its work vanished into the background."
- **Numbers I remember:** 1 second (user service), a tenth of a second (orders service failing), 1,000 simultaneous requests leaving 1,000 orphaned tasks with plain `gather`, vs. 0 leftover tasks with a task group; half a second as the client giving up.
- **Opening question / answer:** "Why is a task's work still running after the function that started it already returned, and what would make 'returned' actually mean 'done'?" → Answer: because starting a task splits control into two paths with nothing forcing the second to rejoin; wrapping tasks in a structured block (task group) forces every task to finish, fail, or get cancelled before the block itself can return.

## 5. Ratings

- **Hook strength (how much the opening made me want the answer): 4/5** — the "returned but still running, a thousand times over" framing is a genuinely unsettling bug to leave dangling, good motivator.
- **How often I felt lost: a few times** — mainly around the cancellation vocabulary being used before it was defined, and the two denser sentences in Ch. 3 and Ch. 6 that packed multiple new facts together.
