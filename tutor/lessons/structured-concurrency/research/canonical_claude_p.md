I don't have web search access in this session, so I'll answer from my own knowledge and explicitly flag anything I'm not fully certain about rather than guess at exact numbers.

# Structured Concurrency — Canonical Lesson Content

## 1. Canonical worked example

Two examples compete, at different scope:

- **The "leaked/orphaned task" bug example.** A function spawns a background task (thread, goroutine, callback, `Promise`) and returns before it finishes. The task keeps running unsupervised — nobody can wait for it, cancel it, or observe its errors. This is the *motivating* example in the essay that popularized the term: Nathaniel J. Smith, **"Notes on structured concurrency, or: Go statement considered harmful"** (njs blog, April 2018). It's the pun on Dijkstra's 1968 "Go To Statement Considered Harmful," and it's the single most-cited source for the concept in general (non-language-specific) treatments.
- **The "fan-out, cancel siblings on first failure" example.** A parent concurrently starts two or more child operations (e.g., "fetch user info" + "fetch order info"), waits for all of them, and if one fails, the others are cancelled instead of continuing pointlessly. This is the example every mainstream implementation uses in its own docs: Java's `StructuredTaskScope.ShutdownOnFailure` Javadoc/JEP examples, Kotlin's `coroutineScope` docs, and Swift's `TaskGroup` docs.

**Which is more common:** the "leaked task" framing is the standard one for *introducing why the problem exists* (it's what nearly every talk opens with), while the "fan-out with join/cancel" example is the standard one for *showing the mechanism in code*. A good short lesson uses both, in that order — bug first, fix second.

## 2. Standard progression across sources

1. **Show ordinary sequential code** and note it has an implicit invariant: a function's effects (including errors) are fully "finished" when it returns to its caller.
2. **Introduce unstructured concurrency** — spawning a thread/goroutine/task with a bare "go" statement or `Thread.start()`/detached `Task {}` — and show that this invariant breaks: the spawning function can return while the child is still running.
3. **Show the concrete failure modes**: (a) resource/task leaks — nothing ever joins the child; (b) swallowed exceptions — an error in the child has nowhere to propagate to; (c) unbounded lifetime — cancelling the parent doesn't cancel the child.
4. **Introduce the fix as a scoping rule**: a construct (nursery / scope / task group) that cannot exit until every task started inside it has finished, and that propagates cancellation and errors between siblings and to the parent. This is presented as restoring the same call/return discipline that structured programming (Dijkstra) gave to control flow — Smith's essay makes this analogy explicit, and also explicitly credits **Ada's tasking model (1983)** and CSP/Occam as prior art where this was already true.
5. **Only after that**, sources layer on the "advanced" behaviors: partial-failure policies (fail-fast vs. collect-all vs. first-success), cancellation propagation semantics, and timeouts as a special case of cancellation.
6. Language docs (Kotlin, Swift) typically show the **simple sequential-looking version first** (`async`/`await` inside a plain function, no explicit scope object visible) before showing the **explicit scope/nursery/TaskGroup version** that fans out truly concurrently — i.e., "structured concurrency" is introduced as the thing that makes concurrent code look and behave like sequential code, not as a new syntax to learn first.

## 3. Definitions and terminology

**Canonical definition** (paraphrasing Smith 2018, echoed by Kotlin/Swift/Java docs): *A concurrent task's lifetime is nested inside the lifetime of the scope (function call, block) that created it — a child task cannot outlive its parent scope, and the parent cannot proceed past that scope until all its children have completed.* This makes concurrency composable with ordinary control-flow constructs (blocks, exceptions, function return).

What it **guarantees**, precisely:
- **Completion containment**: when the enclosing block/scope exits, every task started inside it has already finished (successfully, with an error, or cancelled) — no "still running in the background" state escapes the scope.
- **Error propagation**: an unhandled exception in a child is not silently dropped; it propagates out through the scope to the parent (exactly one path out, mirroring normal exception propagation).
- **Cancellation propagation**: cancelling/erroring the parent (or one sibling, in most implementations' default policy) cancels the other children still running in that scope.

Terminology varies by ecosystem, naming the same scoping construct:
| Source | Term |
|---|---|
| Trio (Python), Smith's essay | **nursery** (`trio.open_nursery()`) |
| Kotlin coroutines | **CoroutineScope**, `coroutineScope { }` / `supervisorScope { }` |
| Swift concurrency (SE-0304) | **task group** (`withTaskGroup`, `withThrowingTaskGroup`), and `async let` for the fixed-arity case |
| Java (JEP 428/437/453 lineage) | **StructuredTaskScope** |
| C++ | no standard term yet; `std::jthread`'s join-on-destruction is a partial/degenerate case; the proposed `std::execution` (P2300) scoped-task work uses "scope" informally |

Uncertain: I'm not fully certain of every exact JEP number in the Java preview sequence beyond the first ("Structured Concurrency (Incubator)" was JEP 428 in JDK 19; it went through multiple incubator/preview rounds in subsequent JDK releases) — treat the specific numbers for the later rounds as approximate rather than verified.

## 4. Key guarantees, their assumptions, and where they break

- **"No orphaned tasks" guarantee** assumes *every* concurrent operation is spawned through the scoping API (nursery/scope/TaskGroup), never through a raw, unscoped primitive (`Thread.start()`, `setTimeout`, a detached `Task { }` in Swift, a bare `go` in Go). Mixing raw primitives back in breaks the guarantee immediately — this is the single most common real-world violation.
- **Error propagation** assumes the scope's failure policy actually surfaces the error rather than swallowing it (e.g., a badly written `supervisorScope`/`ShutdownOnSuccess` misuse can mask failures) and that the task itself doesn't itself catch-and-discard exceptions internally.
- **Cancellation propagation** assumes the child task is *cooperative* — it periodically checks a cancellation flag/token or is at an interruption point (a suspend point in Kotlin, an `await`/checked cancellation in Swift, an interrupt check in Java). Structured concurrency does not make blocking, non-cooperative code cancellable; a child stuck in an uninterruptible native call will not stop just because its scope was cancelled.
- **Boundary conditions**: the guarantee holds only within one process; it does not, by itself, address distributed calls (an RPC to another service isn't "cancelled" server-side just because the client-side task tree is cancelled — you need explicit deadline/cancellation propagation over the wire, e.g., gRPC deadlines).

## 5. Standard concrete examples as they appear in canonical sources

- **Trio** (Smith's essay / Trio docs): 
  ```python
  async def parent():
      async with trio.open_nursery() as nursery:
          nursery.start_soon(child1)
          nursery.start_soon(child2)
      # both children guaranteed done here
  ```
- **Kotlin** (kotlinlang.org, "Coroutines basics" → "Structured concurrency" section):
  ```kotlin
  suspend fun doWorld() = coroutineScope {
      launch { delay(1000L); println("World!") }
      println("Hello")
  }
  ```
  and the exception-propagation example in "Cancellation and exceptions" showing that a failing child cancels its siblings in `coroutineScope`.
- **Swift** (SE-0304 / Swift docs, "Concurrency" chapter): the `withThrowingTaskGroup` example fetching multiple images/photos concurrently and collecting results, plus `async let` for a fixed small number of concurrent children.
- **Java** (JEP 428/…/453 examples, and the `StructuredTaskScope` Javadoc): the canonical `handle()` method that forks "fetch user" and "fetch order" with `ShutdownOnFailure`, calls `scope.join()`, then `scope.throwIfFailed()`.
- **Go (counter-example, not an implementation)**: `errgroup.Group` (`golang.org/x/sync/errgroup`) is frequently cited as the closest thing Go has to structured concurrency in idiomatic use, contrasted with a bare `go func(){}()` which is exactly the anti-pattern Smith's title refers to.

## 6. Misconceptions and how the canonical treatment corrects them

- **"Structured concurrency just means using `async`/`await`."** Correction: `async`/`await` is about *syntax* for sequencing a single chain of asynchronous work; structured concurrency is about the *lifetime and error-propagation discipline* for multiple concurrent children. You can have async/await with zero structured concurrency (e.g., a detached `Task {}` in Swift, or a bare Promise you never await in JS).
- **"`Promise.all` / `Task.WhenAll` already gives me this."** Correction: waiting on a collection you already hold is not the same guarantee — nothing stops code elsewhere from creating a promise/task and never registering it in that collection; the language doesn't *enforce* nesting. True structured-concurrency APIs make the scope the only way to spawn.
- **"Supervision trees (Erlang/OTP) are the same idea."** Correction: OTP supervisors are about *fault recovery* (restart strategies) across a long-lived process tree, not about a caller blocking until children finish within a lexical scope — related philosophy (bounded, hierarchical task lifetimes) but a different guarantee and a different canonical source (Armstrong's Erlang/OTP design, not Smith's essay).
- **"Cancellation is instantaneous."** Correction: cancellation is cooperative signaling, not preemption; canonical docs (Kotlin's cancellation docs, Swift's `Task.checkCancellation()`) stress that children must check/respond to it.
- **"This is a new invention."** Correction: canonical essays explicitly note it's a return to how Ada tasking, Occam, and CSP already worked in the 1970s–80s; what's "new" is reintroducing it into languages/runtimes (threads, then async/await) that had regressed to unstructured, callback- or thread-based concurrency.

## 7. For a short lesson: essential / extra / omit

- **Essential**: the leaked-task problem; the core guarantee (child can't outlive parent scope; errors propagate; scope exit implies all children done); one fan-out/cancel-on-error code example in one language.
- **Common extra** (include if time permits): the fail-fast vs. supervisor (survive-one-failure) policy distinction (`coroutineScope` vs `supervisorScope`; `ShutdownOnFailure` vs `ShutdownOnSuccess`); timeouts as "cancel after a deadline."
- **Leave out** of a short lesson: the full cross-language survey; C++ senders/receivers (P2300) and its standardization status; the detailed history/succession of Java's JEP preview rounds; distributed/cross-process cancellation; the cactus-stack/memory-model formalism from Smith's essay (interesting but not needed to use the feature).

## 8. Languages/libraries/systems and current status

| Ecosystem | Mechanism | Status (as of my knowledge, Jan 2026 cutoff) |
|---|---|---|
| Python (Trio) | `nursery` | Library-only, stable; the original reference implementation |
| Python (asyncio) | `asyncio.TaskGroup` | Stable in standard library since Python 3.11 |
| Kotlin | `CoroutineScope`, `coroutineScope`/`supervisorScope` | Stable (kotlinx.coroutines) |
| Swift | `TaskGroup`/`async let` (SE-0304) | Stable since Swift 5.5 |
| Java | `StructuredTaskScope` | Went through multiple JDK preview/incubator rounds starting JEP 428 (JDK 19); **exact final/stable JEP number and version I'm not certain of — verify before citing precisely** |
| Go | no language construct; `errgroup.Group` idiom | Library-only convention, not enforced by the language |
| C++ | `std::jthread` (partial: join-on-destruction only); `std::execution`/P2300 | `jthread` stable since C++20; P2300 not yet a shipped structured-concurrency solution — **status uncertain, verify current standardization state** |
| Rust | no std mechanism; experimental crates (e.g., `moro`), `tokio::join!` for fixed fan-in | Library-only / experimental, no consensus stdlib solution |
| .NET/C# | no dedicated construct; `Task.WhenAll` + linked `CancellationTokenSource` as manual pattern | Library/pattern-only, not enforced |

## 9. Claims that are commonly overstated or subtly wrong

- "Structured concurrency prevents deadlocks" — it doesn't; it only prevents *lifetime/leak/error-swallowing* bugs, not resource-ordering deadlocks.
- "Structured concurrency makes concurrent code as safe as sequential code" — overstated; it removes a specific class of bugs (orphaned tasks, lost errors) but not data races, ordering bugs, or logic errors from concurrent mutation of shared state.
- "It's a Kotlin/Swift/Java invention" — the term and rigorous treatment are recent (Sústrik 2016 blog posts predate Smith's more famous 2018 essay; both are sometimes conflated or the earlier one is omitted from language marketing material), and the underlying idea is decades older (Ada, CSP/Occam).
- "Cancellation = immediate stop" — overstated; it's cooperative in every mainstream implementation.
- "Go doesn't need this because it has channels" — channels solve communication, not task-lifetime containment; `errgroup` exists precisely because raw goroutines don't give you structured concurrency.

## 10. Animation vs. doing vs. reading

- **Animation (best for the spatial/scoping model)**: the box/scope-nesting diagram — a rectangle representing the parent's lifetime, child tasks as bars that must end before the rectangle closes, contrasted with a bar poking out the side (the leak). This is exactly the visual Smith's essay itself uses in prose form, and it's the part that's genuinely hard to grasp from text alone but obvious once animated. Also good for animating cancellation propagating from a failing child to its siblings.
- **Doing (best for the cooperative/cancellation subtlety and for belief-formation)**: running actual code — e.g., a Kotlin/Swift/Java/Trio snippet where one child throws and you observe the sibling get cancelled, versus the same scenario built with raw threads/goroutines where the sibling keeps running silently. An interactive "spawn 3, fail 1, watch what happens" sandbox makes the guarantee concrete rather than asserted.
- **Reading (best for exact semantics/citation-grade precision)**: the precise wording of guarantees and the fail-fast-vs-supervisor policy differences (`ShutdownOnFailure` vs `ShutdownOnSuccess`, `coroutineScope` vs `supervisorScope`) — these are easy to get subtly wrong from memory of a video, and the source docs/JEP text are the thing to point viewers to afterward.

---
**Flagged uncertainties** (don't treat as settled without checking primary sources): exact JEP numbers/versions for every Java structured-concurrency preview round beyond JEP 428; current standardization status of C++ P2300; whether Java's `StructuredTaskScope` has exited preview by JDK 25 or later. Since I had no web access this session to verify these against current documentation, confirm them directly against openjdk.org/jeps before putting a specific number on screen.
