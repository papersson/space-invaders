# Structured concurrency: the canonical treatment (research report)

Checked against primary sources on 2026-09-26. Quotes are copied from the sources. Items marked **[uncertain]** could not be checked against a primary source in this pass.

## Source keys (primary sources)

| Key | Source |
|---|---|
| **Sústrik 2016** | Martin Sústrik, "Structured Concurrency", 250bpm blog, 2016. The original URL `250bpm.com/blog:71` now returns 404. The text was republished on 2024-06-29 at https://www.250bpm.com/p/structured-concurrency. The exact month in 2016 is **[uncertain]**. The companion C library is libdill. |
| **Smith 2018a** | Nathaniel J. Smith, "Timeouts and cancellation for humans", 2018-01-11, https://vorpus.org/blog/timeouts-and-cancellation-for-humans/ |
| **Smith 2018b** | Nathaniel J. Smith, "Notes on structured concurrency, or: Go statement considered harmful", 2018-04-25, https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/ |
| **Smith PyCon 2018** | "Trio: Async concurrency for mere mortals", PyCon 2018. Happy Eyeballs is the motivating example and is live-coded at the end (https://github.com/python-trio/trio-talks). |
| **Elizarov 2018** | Roman Elizarov, "Structured concurrency", Medium, 2018-09-12, announcing kotlinx.coroutines 0.26.0. Medium blocked direct fetch, so the content was checked only through search snippets and his tweet: `loadAndCombine` example, recommends Smith 2018b. Also his talk at Hydra 2019 (Speaker Deck). |
| **Baker 2019 / Niebler 2020** | Lewis Baker, "Structured Concurrency: Writing Safer Concurrent Code with Coroutines and Algorithms", CppCon 2019. Eric Niebler, "Structured Concurrency", 2020-11-08, https://ericniebler.com/2020/11/08/structured-concurrency/ |
| **Swift** | SE-0304 "Structured concurrency" (Implemented, Swift 5.5). SE-0317 "async let" (Swift 5.5). SE-0381 "DiscardingTaskGroups" (Swift 5.9). WWDC21 session 10134, "Explore structured concurrency in Swift". *The Swift Programming Language* (TSPL), chapter "Concurrency". The `TaskGroup.swift` doc comments in the stdlib. |
| **JEP** | JEP 428 and 437 (incubator, JDK 19–20). JEP 453 (preview, JDK 21). JEPs 462, 480 and 499 (JDK 22–24). JEP 505 (JDK 25). JEP 525 (JDK 26). JEP 533 (7th preview, JDK 27, "Closed / Delivered"). **JEP 543** ("Candidate", created 2026-08-05): "We here propose to finalize Structured Concurrency in JDK 28, without further change." Also the JDK 27 `StructuredTaskScope` Javadoc. |
| **Python** | Python docs, "Coroutines and Tasks" (3.14.7, plus 3.15.0rc2 docs). PEP 654 (ExceptionGroup, Python 3.11). |
| **Trio / AnyIO** | Trio docs (tutorial, reference-core, design). AnyIO docs, "Creating and managing tasks". |
| **Kotlin** | kotlinlang.org pages: "Coroutines basics", "Composing suspending functions", "Cancellation and timeouts", "Coroutine exceptions handling". API docs for `GlobalScope` and `coroutineScope`. |
| **C++** | P2300R10 `std::execution`, adopted for C++26 in St. Louis, June 2024. P3149R11 `async_scope` (`counting_scope`), plenary-approved for C++26 in Sofia, June 2025. Herb Sutter, "C++26 is done!", 2026-03-29. |
| **Go / Rust** | `golang.org/x/sync/errgroup` package docs. `sync.WaitGroup.Go` docs. Rust `std::thread::scope` docs. Tokio `JoinSet` docs. |

---

## 1. The canonical worked example

**Standard example A, and the more common one: fan out, then fan in, with a failure.** One operation starts two (or a few) independent sub-operations concurrently and then combines their results. The teaching point is what happens when one of them fails.

- **Java (JEPs 428 through 543).** A server method `handle()` calls `findUser()` and `fetchOrder()` concurrently and returns `new Response(user, order)`. This is the version closest to the audience's day job.
- **Kotlin docs.** `concurrentSum()` uses `async { doSomethingUsefulOne() }` and `async { doSomethingUsefulTwo() }`. Its failing twin, `failedConcurrentSum()`, shows the failure case. Elizarov 2018 uses `loadAndCombine(name1, name2)`, which runs two `loadImage` calls and then `combineImages`. The `coroutineScope` API doc uses `downloadAndCompareTwoFiles()`.
- **Swift.** SE-0304 and SE-0317 use `makeDinner()`: chop vegetables, marinate meat and preheat the oven concurrently. WWDC21 uses `fetchOneThumbnail`, where `async let` fetches the image and its metadata. TSPL downloads three photos with `async let`.
- **Python and Trio.** Python's `TaskGroup` example uses `some_coro` and `another_coro`. Smith 2018b uses `myfunc` and `anotherfunc`. The Trio tutorial uses `parent`, `child1` and `child2`.

**Why this example is the standard one.**
1. The sequential version is short and obviously correct. The JEP presents the single-threaded `handle()` as the model: "An invoked method cannot outlive the method that invoked it".
2. The naive concurrent version works on the happy path. It fails only on the error path, and the error path is exactly where structured concurrency matters. The JEP lists the naive version's three failure modes: a thread leak, interruption that does not propagate, and unnecessary waiting (details in §5).
3. It matches a real service handler that fans out to backends.

**Standard example B: a race, where the first success wins and the rest are cancelled.**
- Smith 2018b and the PyCon 2018 talk use **Happy Eyeballs (RFC 8305)**: "you race several connection attempts against each other, with a staggered start". Smith contrasts Twisted's implementation, "almost 600 lines of Python" with "at least one logic bug", against Trio's version, "more than 15x shorter".
- The JEP includes `race()` using `Joiner.anySuccessfulOrThrow()`, described as "useful in, e.g., server applications that require a result from any one of a collection of redundant services".
- Example B is less common. Sources usually introduce it second, as a policy variant of A. It is the only one of the two that shows *cancellation on success*.

A minor third example is the **server accept loop** (Smith 2018b). It shows dynamic spawning and the escape hatch.

**Recommendation.** Lead with A, told as "handle a request by calling two services", and add B as the extension.

## 2. The standard progression

Almost every canonical source follows the same arc:

1. **Sequential code first.** It is correct, but slow.
2. **Naive concurrency.** Spawn tasks and join them via futures, `create_task` or `GlobalScope.async`. It is fast and looks right.
3. **The failure path.** Show a leaked task, a lost error, or waiting that serves no purpose. This is the problem statement: the task/subtask relationship "exist[s] only in our minds" (JEP).
4. **The principle,** stated by analogy to structured programming. Smith gives Dijkstra's goto letter and the "black box rule". Sústrik, the JEP ("As with structured programming techniques…") and Niebler all use the same analogy.
5. **The scoped construct.** The lifetime of the block equals the lifetime of the children. "Call stack morphs into a call tree" (Sústrik 2016).
6. **Consequences.** The parent waits at the end of the block. A child error cancels its siblings and is rethrown in the parent. Cancelling the parent propagates downward.
7. **Cancellation is cooperative.** Timeouts and deadlines apply to a whole scope.
8. **Policies and variants.** Race or any-success, supervisors, and collect-all.
9. **Escape hatches.** Unstructured tasks, or passing a longer-lived scope.
10. **Observability and extras.**

How each source orders these ideas, and which simpler version it shows before the full one:

| Source | Order | Simpler version shown first |
|---|---|---|
| Smith 2018b | A survey of "go statements" (the `go` statement, `pthread_create`, `threading.Thread`, `asyncio.create_task`, callbacks), then the history of goto, then "go statement considered harmful" (it breaks abstraction, cleanup and error handling), then nurseries, then their consequences, then Happy Eyeballs. | `run_concurrently([myfunc, anotherfunc])`, which takes a fixed list of thunks, before the nursery with dynamic `start_soon`. |
| JEP 505/533/543 | Unstructured `ExecutorService` `handle()`, then "Task structure should reflect code structure" (the single-threaded `handle()`), then the definition, then `StructuredTaskScope.open()`, then cancellation, then Joiners (`race`, `allSuccessfulOrThrow`), then custom Joiners, then exceptions, then configuration and timeouts, then observability. | The zero-argument `open()` default policy before Joiners. |
| WWDC21 (Swift) | Sequential async, then `async let`, then the task tree, then cancellation, then task groups, then unstructured `Task {}`, then `Task.detached`. | `async let` (a fixed number of children) before `TaskGroup` (a dynamic number). The same order appears in TSPL and in SE-0304 plus SE-0317. |
| Kotlin docs, "Composing suspending functions" | Sequential by default, then concurrent with `async`, then async-style functions with `GlobalScope` ("strongly discouraged"), then "Structured concurrency with async" (`concurrentSum`, `failedConcurrentSum`). | `async` inside a scope before the failure demo. |
| Python docs | `create_task`, then `TaskGroup`, then a comparison with `gather` ("stronger safety guarantees"). | |

## 3. Definitions and terminology

**Standard definitions.**
- **Sústrik 2016:** "structured concurrency prevents lifetime of green thread B launched by green thread A to exceed lifetime of A".
- **Smith 2018b:** "every time our control splits into multiple concurrent paths, we want to make sure that they join up again"; "the nursery block doesn't exit until all the tasks inside it have exited".
- **JEP 505/543:** "If a task splits into concurrent subtasks then they all return to the same place, namely the task's code block." The power of the approach comes from "two ideas": well-defined entry and exit points, and "the lifetimes of operations are nested in a way that mirrors their syntactic nesting in the code".
- **SE-0304:** "a function that creates a child task must wait for it to end before returning". Its primary rule is "a *child task* cannot live longer than the *parent task* (or scope) in which it was created".
- **Kotlin docs:** "coroutines form a tree hierarchy of parent and child tasks with linked lifecycles"; "new coroutines can only be launched in a `CoroutineScope`".
- **Niebler 2020:** "child operations are guaranteed to complete before their parents, just the way a function is guaranteed to complete before its caller."

**Who named it.** The JEP says the term "was coined by Martin Sústrik and popularized by Nathaniel J. Smith". Smith 2018b's footnote lists prior art: parallel composition in CSP and occam, fork/join, Erlang supervisors, Sústrik and libdill, and Rust's `crossbeam::scope` and `rayon::scope`.

**The invariant versus the policies.** The *core invariant* everywhere is nested lifetimes. The following are **policies** that most implementations attach to that invariant, and they vary between systems:
- error propagation to the parent;
- cancelling siblings when one fails;
- downward cancellation;
- deadlines applied to a subtree.

**Terminology across systems.**

| Concept | Trio / AnyIO | asyncio | Kotlin | Swift | Java | C++26 | Go | Rust |
|---|---|---|---|---|---|---|---|---|
| Scope | nursery / task group | `TaskGroup` | `CoroutineScope`, `coroutineScope {}` | task group, `async let`, task tree | `StructuredTaskScope` | `counting_scope` | `errgroup.Group` | `thread::scope` |
| Spawn | `start_soon`, `start` | `create_task` | `launch`, `async` | `addTask`, `async let` | `fork` (returns `Subtask`) | `spawn`, `spawn_future` | `Go` | `Scope::spawn` |
| Child is called | child task | task | child coroutine | child task | subtask (the parent is the "owner thread") | — | goroutine | scoped thread |
| Cancel | cancel scope, `Cancelled`, "checkpoints" | `CancelledError` | `CancellationException`, "suspension points" | cooperative, `CancellationError` | *interrupt*; "cancel the scope" (JDK 21–24 said "shut down": `ShutdownOnFailure` / `ShutdownOnSuccess`) | stop token, `request_stop` | `context` cancellation | none |
| Opt-out | pass the nursery | plain `create_task` | `GlobalScope`, `SupervisorJob` / `supervisorScope` | "unstructured task" `Task {}`, "detached task" `Task.detached` | `ExecutorService` | `start_detached` | a bare `go` statement | `thread::spawn` |

**Other terms.**
- Policy names: Java uses "Error handling with short-circuiting" and, in JEP 453, "invoke all" / "invoke any". SE-0381 uses "one for all, and all for one". Kotlin uses "supervision".
- libdill: `go()`, `bundle()`, `bundle_go()`, `bundle_wait()`, `hclose()`. These names were checked in `libdill.h`.

## 4. Key guarantees, their assumptions, and where they stop holding

**G1. Lifetime containment.** When the scope exits, every child has finished. There are no orphans.
- Java: "All of the subtasks' threads are guaranteed to have terminated once the scope is closed, and no thread is left behind when the block exits."
- Swift: "A group *always* waits for all of its child tasks to complete before it returns."
- *It stops holding* when code uses an escape hatch: `Task {}` or `Task.detached`, `GlobalScope`, raw threads or executors, or a nursery passed to a longer-lived owner. In the last case, Smith notes that spawned tasks are "still bound by the lifetime of the nursery that was passed in".
- Enforcement differs by system:
  - Java enforces the rules at run time: forking from a non-owner thread fails, and `StructureViolationException` is thrown.
  - Swift and Kotlin enforce them partly at compile time. An `async let` cannot escape. `launch` needs a scope. `GlobalScope` requires `@OptIn(DelicateCoroutinesApi::class)`.
  - asyncio is opt-in only: `create_task` sits right next to `TaskGroup`.

**G2. The scope exits only after cleanup finishes, because cancellation is cooperative.**
- Trio: "We never terminate a task without giving it a chance to run cleanup handlers."
- Swift: "Marking a task as canceled does not stop the task" (WWDC21).
- Kotlin: "If a coroutine doesn't suspend for a long time, it also doesn't stop when it's canceled."
- *Assumption:* children reach checkpoints, suspension points or interruptible calls.
- *Failure mode:* Java says "Subtasks that do not respond to interrupts … may delay the closing of a scope indefinitely". Python says `TaskGroup` and `timeout()` "might misbehave if a coroutine swallows `asyncio.CancelledError`". In short, a leak turns into a **hang**.

**G3. Errors are not lost.** An unhandled failure in a child reaches the parent: "exceptions propagate up this call tree" (Smith 2018b). How errors are aggregated varies by system:
- Python and Trio collect all of them in an `ExceptionGroup` (PEP 654 exists largely for this).
- Kotlin: "the first exception wins" and later ones are attached as suppressed exceptions.
- Java throws `ExecutionException` whose cause is the exception from one failed subtask.
- Go's errgroup returns "the first non-nil error".
- Rust's `thread::scope` panics if any child panicked.
- *Exceptions to G3:*
  - Supervisor scopes (`supervisorScope`, `SupervisorJob`) deliberately do not propagate child failures.
  - In Swift's `withThrowingTaskGroup`, a child error that the body never consumes is dropped: "nothing is canceled and the group doesn't throw an error" (TaskGroup.swift doc comment).

**G4. Fail-fast: siblings are cancelled when one child fails, and cancellation flows down the tree.** This is the default in Trio, asyncio, Kotlin `coroutineScope` and Java `open()`.
- *Not universal:*
  - Swift `TaskGroup` cancels only when an error is thrown *out of the body*: "Throwing an error in one of the child tasks of a task group doesn't immediately cancel the other tasks". `DiscardingTaskGroup` (SE-0381) does cancel immediately.
  - Go's errgroup cancels only its derived `Context`, and only goroutines that check that context actually stop.
  - Rust's `thread::scope` has no cancellation at all.
- Cancellation only ever flows *downward*, never upward to the parent (SE-0304).

**G5. Local reasoning, cleanup and borrowing work again.**
- "When a function does return, you know it's really done" (Smith 2018b), so `with` blocks and RAII are safe.
- Scoped threads "can borrow non-`'static` data, as the scope guarantees all threads will be joined" (Rust docs).
- Niebler: "it is perfectly safe to pass local variables by reference to child tasks that are immediately awaited."

**G6. Observability.** A runtime tree of tasks. Java's JSON thread dump (`jcmd <pid> Thread.dump_to_file -format=json`) shows scopes and their threads as a hierarchy.

**G7. Memory visibility (Java).** Actions of a subtask *happen-before* the owner thread returns from `join()` with the outcome (JDK 27 Javadoc).

**What none of these guarantees cover** (no canonical source claims them):
- **Data races and deadlocks.** Swift prevents data races with separate machinery (`Sendable` and actors). SE-0304 even shows mutation of a captured `var` being rejected by `@Sendable` checking, not by the structure.
- **Remote side effects.** Cancelling a local subtask does not undo a request that has already reached another service. This is my teaching caveat, not a quote from a source.

## 5. Standard concrete examples as they appear in the sources

**Java, the "before" version (JEP).** It uses `executor.submit(() -> findUser())`, `executor.submit(() -> fetchOrder())`, `user.get()`, `order.get()`. The JEP names three problems:
1. If `findUser()` throws, "`fetchOrder()` will continue to run in its own thread. This is a *thread leak*".
2. If the thread running `handle()` is interrupted, "the interruption will not propagate to the subtasks".
3. If `fetchOrder()` fails while `findUser()` is slow, `handle()` "will wait unnecessarily".

**Java, the "after" version (JDK 27 form, unchanged in JEP 543):**
```java
Response handle() throws ExecutionException, InterruptedException {
    try (var scope = StructuredTaskScope.open()) {
        Subtask<String> user = scope.fork(() -> findUser());
        Subtask<Integer> order = scope.fork(() -> fetchOrder());
        scope.join();   // Join subtasks, propagating exceptions
        return new Response(user.get(), order.get());
    }
}
```
The race variant uses `StructuredTaskScope.open(Joiner.<T>anySuccessfulOrThrow())`, then `tasks.forEach(scope::fork)` and `return scope.join()`.

**Kotlin.**
```kotlin
suspend fun concurrentSum(): Int = coroutineScope {
    val one = async { doSomethingUsefulOne() }
    val two = async { doSomethingUsefulTwo() }
    one.await() + two.await()
}
```
The failing version prints "Second child throws an exception / First child was cancelled / Computation failed with ArithmeticException". The anti-pattern is `GlobalScope.async`: "`somethingUsefulOneAsync` still running in the background, even though the operation that initiated it was aborted."

**Python.**
```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(some_coro(...))
    task2 = tg.create_task(another_coro(...))
print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
```
The docs contrast this with `gather`: "Other awaitables in the *aws* sequence won't be cancelled and will continue to run."

**Trio.** `async with trio.open_nursery() as nursery: nursery.start_soon(myfunc); nursery.start_soon(anotherfunc)`. The accept-loop version runs `while True: conn = await server_socket.accept(); nursery.start_soon(handler, conn)`.

**Swift.** `async let veggies = chopVegetables()`, `async let meat = marinateMeat()`, `async let oven = preheatOven(temperature: 350)`. An `async let` that is never awaited is implicitly cancelled and then awaited when its scope exits (SE-0317). The task-group version of `makeDinner` narrates the failure case: "an incident with the kitchen knife" throws, and "any child tasks that have not yet completed … will be automatically cancelled."

**Rust.** Inside `thread::scope(|s| { s.spawn(|| …); s.spawn(|| …); })` the child threads borrow `a` and `x` from the enclosing function. After the scope, `a.push(4)`.

## 6. Misconceptions practitioners bring, and how the canonical treatment corrects them

1. **"async/await is structured concurrency."** SE-0304 says async/await "does not introduce concurrency *per se*". `create_task`, `Task {}` and `GlobalScope.launch` are unstructured even inside async code. *Correction:* sources separate suspension, meaning `await`, from lifetime, meaning scope.
2. **"Waiting for all the futures is enough."** A sequence of `Future.get()` calls, `gather`, or a `WaitGroup` gives joins without the failure policy. *Correction:* the JEP's three failure modes and the Python docs' comparison of `gather` with `TaskGroup` both teach through the failure path, not the happy path.
3. **"Cancel means kill."** *Correction:* every source teaches cooperative cancellation. Java uses interruption, Trio uses checkpoints, and Kotlin and Swift use suspension points or explicit checks. The scope waits until cleanup has finished.
4. **"Fire-and-forget is harmless."** The Python docs warn that a task nobody references "may get garbage collected at any time, even before it's done", and that its exception is only logged. *Correction:* give every task an owner.
5. **"Structured concurrency forbids background work."** *Correction:* background work is allowed, but a named owner must bound it. Options: pass a nursery (Smith's "There is an escape"), use a scope tied to a component's lifecycle (Kotlin `GlobalScope` docs), use `TaskGroup.cancel()` (new in Python 3.15), or use unstructured tasks deliberately (Swift: "you're also completely responsible for their correctness").
6. **"Only mature, production code needs this."** Elhage (2026 blog post) argues from the opposite end: when writing new code, "dumb bugs" in a crashed child "have a bad habit of turning into deadlocks" because the parent waits forever. This is a secondary source.
7. **"It's the same as Erlang supervision."** *Correction:* they are related but not the same. The JEP says Erlang supervisors "inform the design of error handling". Smith shows that a supervisor can be one nursery-like *policy*, not the model itself.

## 7. For a short lesson

**Essential.**
- The problem: spawn-and-forget, the "go statement", hides lifetimes, errors and cancellation. Show this with the fan-out handler.
- The rule: children cannot outlive the block that started them. The call stack becomes a call tree, and "when a function does return, you know it's really done".
- The three consequences: the parent waits at the closing brace; a child failure cancels its siblings and is rethrown to the parent; cancellation propagates down the tree.
- Cancellation is cooperative, so scope exit means request, then wait.
- One real API on screen. Java `StructuredTaskScope` or Python `TaskGroup` suits this audience best.

**Common extras.**
- The race / any-success policy (Happy Eyeballs, redundant services).
- Timeouts as scopes (Trio cancel scopes, `asyncio.timeout`, Java `withTimeout`).
- Escape hatches and unstructured tasks.
- Supervisor scopes.
- `ExceptionGroup`.
- The Dijkstra/goto analogy.
- Thread-dump observability.

**Leave out.**
- Java preview API churn (`ShutdownOnFailure` → Joiner, `FailedException` → `ExecutionException`).
- C++ senders and receivers.
- The libdill C API.
- Swift priority escalation and task-locals.
- Trio `nursery.start` / `task_status`.
- Kotlin `Job` wiring.
- Rust's async-scope debates.
- Smith's unpublished claim that nurseries have "equivalent expressive power" to go statements.

## 8. Languages, libraries and systems: mechanism and status (as of 2026-09-26)

| System | Mechanism | Status and version |
|---|---|---|
| **libdill (C)**, Sústrik | Coroutine handles from `go()`, plus bundles. `hclose` cancels a coroutine. Blocking calls return `ECANCELED`. | Library. The project's website domain (`libdill.org`) now redirects to an unrelated domain. Whether the project is still maintained is **[uncertain]**. |
| **Trio (Python)** | Nurseries, cancel scopes and checkpoints. No spawn primitive exists outside a nursery. | Library, 0.34.0 (PyPI, 2026-08-11). |
| **AnyIO** | Trio-style task groups that run on top of asyncio or Trio. | Library, 4.15.1 (2026-09-05). |
| **Python asyncio** | `TaskGroup` (3.11+), `asyncio.timeout` (3.11+), `ExceptionGroup` / `except*` (PEP 654, 3.11). Coexists with unstructured `create_task`. | Stable in the stdlib. Current docs are for 3.14.7. `TaskGroup.cancel()` is "Added in version 3.15"; 3.15.0 is in RC2 with final release scheduled for 2026-10-01 (PEP 790). |
| **Kotlin** | `CoroutineScope` / `Job` tree. `launch` and `async` need a scope. `coroutineScope`, `supervisorScope`. `GlobalScope` is a delicate API. | Official JetBrains library (kotlinx.coroutines), not the language itself. Structured since 0.26.0 (Sept 2018). Current 1.11.0 (Maven, May 2026). |
| **Swift** | Language feature: `async let`, `TaskGroup` / `ThrowingTaskGroup` / `DiscardingTaskGroup`, and the task tree. Unstructured `Task {}` and `Task.detached` also exist. | Stable since Swift 5.5 (SE-0304, SE-0317). `DiscardingTaskGroup` since 5.9. swift.org lists 6.4.0 as current; its release date was not checked. |
| **Java** | `java.util.concurrent.StructuredTaskScope`. One thread per subtask (virtual threads by default). Interrupt-based cancellation. Joiner policies. Try-with-resources. Runtime enforcement of structure. JSON thread dumps. `ScopedValue` inheritance (JEP 506 is final in JDK 25). | **Still preview** in JDK 27 (GA 2026-09-15; JEP 533, 7th preview; needs `--enable-preview`). JEP 543 (Candidate) proposes making it final in **JDK 28** "without further change". JDK 28 is not yet released. |
| **C++26** | `std::execution` senders and receivers (P2300R10), plus `counting_scope`, `spawn`, `spawn_future` and `join` (P3149R11). Cancellation through stop tokens. | In the C++26 draft. Technical work finished in March 2026; the ISO DIS ballot opened 2026-07-31 and the standard is **not yet published**. Standard-library implementation status is **[uncertain]**. Sutter notes the feature "lacks great documentation". |
| **Go** | No language-level construct. `errgroup` (`Go`, `Wait`, `WithContext`, `SetLimit`) combined with `context` cancellation. `sync.WaitGroup.Go` (Go 1.25) is a join helper only. | Library outside the stdlib (`x/sync` v0.23.0). Go 1.27.1 is current. It is a convention, not enforced. |
| **Rust** | `std::thread::scope`: OS threads, automatic join, panics propagated, borrowing allowed, no cancellation. For async, Tokio `JoinSet` aborts its tasks when it is dropped. | `thread::scope` stable since 1.63.0 (2022); current Rust is 1.98.1. There is no standard *async* scope. Calling `JoinSet` (tokio 1.53.1) "structured" is my characterization. |

## 9. Claims that are commonly overstated or subtly wrong

- **"It guarantees no leaks."** Only for code that stays inside the discipline. Escape hatches exist in every system, and a child that does not cooperate turns a leak into an indefinite hang (JEP).
- **"A child failure always cancels its siblings."** False for Swift `TaskGroup` unless the body rethrows, false for supervisor scopes, false for Go errgroup goroutines that ignore `ctx`, and false for Rust `thread::scope`.
- **"You get every error."** It depends on the system: an `ExceptionGroup` (Python) versus first-wins with suppressed exceptions (Kotlin) versus a single cause (Java, Go).
- **"It prevents data races and deadlocks."** No source claims this in general. Sutter's C++ claim is hedged: it "makes it easier" to write programs that are "data-race-free by construction".
- **"Java has structured concurrency."** It has been preview-only through JDK 27. Many tutorials show dead APIs: `new StructuredTaskScope.ShutdownOnFailure()`, `throwIfFailed()`, `FailedException`.
- **"Smith invented it" / "Elizarov invented it independently."** The JEP credits Sústrik (coined) and Smith (popularized). Elizarov's post recommends Smith's essay. Whether the Kotlin design was developed independently is **[uncertain]**.
- **"The go statement is harmful, so Go is broken."** The title is polemical. Smith's own conclusion needs new frameworks "from scratch". In Go practice the pattern is errgroup plus context.
- **"Structured concurrency requires coroutines or virtual threads."** Rust's `thread::scope` and Java's `ThreadFactory` option both work with ordinary threads. The JEP calls virtual threads a "great match", not a requirement.
- **Smith 2018b's line that Rust "discards the error"** when a background thread panics is dated. Since 1.63, `thread::scope` propagates panics.
- **"`ExecutorService` in try-with-resources is structured concurrency."** It gives lifetime containment only. There is no cancellation on failure and no enforcement of ownership. The JEP explains why a structured `ExecutorService` was rejected.

## 10. Which medium suits which part (my pedagogical judgment, not from the sources)

**Narrated animation.** Use it for anything that unfolds over *time and shape*:
- the call stack turning into a call tree;
- Smith's arrow diagrams: sequential flow, goto, go, and the nursery ("one arrow going in the top and one coming out the bottom");
- a timeline of the fan-out handler in which one call fails, the leaked thread keeps running in the unstructured version, and in the structured version the sibling is cancelled, the parent waits at the brace, and the error is rethrown;
- cancellation flowing *down* the tree and a timeout covering a whole subtree.

The sources themselves rely on these diagrams (Smith, Sústrik, and the WWDC21 task-tree animations).

**Doing.** Use an interactive simulation or runnable code for the *policy and timing* rules, which are counterintuitive until someone tries them:
- choose which child fails and when;
- make a child ignore cancellation and watch scope exit stall;
- compare `gather` with `TaskGroup`;
- switch between the all-must-succeed and any-success policies.

Running Python `asyncio.TaskGroup` needs only the stdlib (3.11+), so it is the easiest runnable version. Good exercises are converting an `ExecutorService` or `gather` handler, and writing a small race or Happy Eyeballs.

**Reading.** Use reference material for:
- the cross-language terminology table;
- status and versions;
- differences in error aggregation;
- escape-hatch APIs;
- the full goto argument (Smith 2018b), which is an essay best read in full.

## Not verified / uncertain

- The exact 2016 month of Sústrik's article.
- The full text of Elizarov 2018 (Medium blocked access; checked through snippets only).
- Whether libdill is still maintained.
- The Swift 6.4.0 release date.
- Standard-library support for C++26 `std::execution`.
- The contents of Chen & You, "Structured Concurrency: A Review" (ICPP Workshops 2022; access was refused).
- The Brockbernd et al. ECOOP 2024 study of Kotlin coroutine bugs: only the abstract was read. It reports that data races, deadlocks and coroutine-specific misconceptions persist, but its individual findings were not checked.
