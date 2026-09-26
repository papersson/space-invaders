No web access available in this session, so I'll answer from domain knowledge and flag genuine uncertainties rather than guess at page numbers. This is well-trodden canonical material, so I'm confident in the substance.

# Concurrency Models: Shared Memory, Actors, CSP — Canonical Treatment

## 1. The canonical worked example

There are two competing standard examples, and they teach different things:

- **Dining Philosophers** (Dijkstra, 1965, unpublished note *EWD123*; popularized in Hoare's 1978 CSP paper and in most OS textbooks) is the canonical example for **deadlock, starvation, and resource-ordering** under shared state. It's the standard vehicle in OS courses (Silberschatz, *Operating System Concepts*, ch. on synchronization) and in CSP itself — Hoare uses it in his 1978 CACM paper "Communicating Sequential Processes."
- **Bank account transfer** (move money between two accounts) is the more common example for comparing *shared-memory-with-locks* vs. *message-passing* directly, because it has an obvious "critical section" (the transfer must be atomic) and an obvious "just send a message instead" alternative. This is the example used in Rob Pike's talk **"Concurrency Is Not Parallelism"** (Heroku/Waza 2012) and in the Go blog post **"Share Memory By Communicating"** (Andrew Gerrand, 2010, go.dev/blog/codelab-share) — both canonical sources for the Go/CSP-style pedagogy, and both explicitly contrast a mutex-protected counter with a channel-based version of the same problem.

**Which is more common for this specific lesson (shared memory vs. actors vs. CSP)**: the **producer–consumer / bounded-buffer problem** is arguably the most universal single example, because it has a natural rendering in all three models — shared queue + lock + condition variable; actor mailbox; CSP channel — and appears that way in Herlihy & Shavit's *The Art of Multiprocessor Programming* (shared memory side) and in Hoare's original CSP paper and Pike's talks (message-passing side). If you want one example that survives translation into all three models without distortion, use **producer–consumer**; use **dining philosophers** specifically when the point is deadlock; use **bank transfer** specifically when the point is "same bug, two idioms."

## 2. The standard pedagogical progression

The textbook/course order (Silberschatz OS ch. 5–7; Goetz *Java Concurrency in Practice* ch. 1–5; MIT 6.005/6.033; CMU 15-410) is:

1. **Single shared mutable variable, no synchronization** → show the race (lost update on a counter). This establishes *why* you need anything at all.
2. **Mutual exclusion primitives**: locks/mutexes → then condition variables/semaphores for waiting, not just excluding. Dijkstra's semaphore (1965) is introduced before monitors (Hoare 1974, "Monitors: An Operating System Structuring Concept," CACM; also Brinch Hansen 1973) because semaphores are lower-level and monitors are presented as "structured locking."
3. **Higher-level shared-memory abstractions**: monitors → then lock-free/atomic operations (compare-and-swap) as the "advanced" topic, per Herlihy & Shavit.
4. **Only after** shared-memory pain (deadlock, forgotten unlocks, races on shared state) is established do courses pivot to **message passing** as an alternative discipline, usually framed with Pike's slogan (itself a Go-community rephrasing of a *Newsqueak*/Limbo era idea, attributed by Pike to their heritage in Hoare's CSP): *"Do not communicate by sharing memory; instead, share memory by communicating."*
5. Message passing then splits into:
   - **CSP** (synchronous, anonymous channels, decoupled from process identity) — introduced via Hoare's original process-algebra framing, then concretized with Go's channels or occam.
   - **Actors** (asynchronous mailboxes, addressed by actor identity) — introduced via Hewitt's 1973 model, then concretized with Erlang/Akka.

The simpler-before-full-version pattern shows up in two places specifically:
- **Semaphores before monitors** (raw signaling before structured, language-enforced mutual exclusion).
- **Unbuffered/synchronous channel before buffered/asynchronous channel** in CSP-style teaching (Go tour and *The Go Programming Language*, Donovan & Kernighan, ch. 8, do exactly this: unbuffered channel first, "rendezvous," then buffered channels as the relaxation).
- In actor teaching, **single-actor request/reply before supervision trees** (Armstrong's thesis and *Programming Erlang* introduce a single `receive` loop before OTP's `gen_server` and supervisor hierarchies).

## 3. Models and terminology

**Shared memory with locks.** Concurrent threads/processes share an address space; mutual exclusion and visibility are managed with explicit synchronization primitives (mutexes, semaphores, condition variables, monitors). Guarantee: *if used correctly*, mutual exclusion on critical sections and (with condition variables/memory barriers) visibility of writes across threads. It guarantees nothing about deadlock-freedom, liveness, or correct composition — those are the programmer's job. Canonical reference: Herlihy & Shavit, *The Art of Multiprocessor Programming* (2008/2020), and Goetz et al., *Java Concurrency in Practice* (2006), esp. ch. 2–4 on thread safety and the Java Memory Model.

**Terminology note**: "lock" (general), "mutex" (binary lock, often OS-level, has ownership semantics), "semaphore" (counting, no ownership, Dijkstra's P/V), "monitor" (lock + condition variables bundled with the data, Hoare 1974 / Hansen 1973 — Java's `synchronized` + `wait/notify` is a monitor). These are used inconsistently across languages: POSIX calls it `pthread_mutex_t`; Java calls the same idea `synchronized`; C# calls it `lock`. Be explicit that "mutex" and "lock" are near-synonyms but "semaphore" is not interchangeable (no ownership, can be signaled by a different thread than the one that waited — this is the classic point of confusion, made explicit in Downey's *The Little Book of Semaphores*, 2016).

**CSP (Communicating Sequential Processes).** Concurrent, independent sequential processes with **no shared state**, communicating exclusively via **synchronous, rendezvous-style channels**: a send blocks until a matching receive occurs (and vice versa). Originated in Hoare's 1978 CACM paper and formalized in his 1985 book *Communicating Sequential Processes* (Prentice Hall) — a full process algebra with traces/failures/divergence semantics. Guarantee: no shared mutable state means no data races on shared memory by construction; a channel operation is a well-defined synchronization point. It does **not** guarantee deadlock-freedom (two processes can each block waiting to send/receive on channels the other never services) or liveness. Real-world realization: Go's channels (unbuffered = true CSP rendezvous; buffered = a relaxation toward asynchronous mailboxes), and occam (the language built directly on CSP for transputers).

**Actor model.** Independent units of computation ("actors"), each with private state and a **mailbox**; actors communicate by **asynchronous** message sends (fire-and-forget, no blocking, no guaranteed delivery order across senders); on receiving a message an actor can: send messages to other actors, create new actors, and decide its behavior for the next message. Originated with Hewitt, Bishop, and Steiger, "A Universal Modular ACTOR Formalism for Artificial Intelligence Intelligence" (IJCAI 1973), formalized by Gul Agha, *Actors: A Model of Concurrent Computation in Distributed Systems* (MIT Press, 1986). Guarantee: no shared mutable state (like CSP) and, unlike CSP, the sender is **never blocked** by the receiver's readiness — this is the defining difference from CSP. It guarantees message delivery is not lost within a reliable-transport actor system but does **not** guarantee ordering between messages from different senders, nor does it guarantee an actor processes messages promptly (mailbox growth / backpressure is not automatic). Real-world realization: Erlang/OTP processes (Armstrong, PhD thesis 2003, and *Programming Erlang*, 2007/2013), Akka (JVM, explicitly modeled on Erlang/Hewitt).

**Cross-model terminology traps** worth flagging on camera:
- "Message passing" is sometimes used loosely to mean *either* CSP or actors; they are not the same (synchronous/anonymous-channel vs. asynchronous/addressed-mailbox).
- "Channel" in Go is CSP-style (synchronous by default); "channel" in some actor libraries (e.g., Akka Streams) means something closer to a buffered async pipe — same word, different guarantee.
- Go's channels are **not pure CSP**: Go also has shared memory and a mutex library (`sync.Mutex`), and its buffered channels are asynchronous up to capacity — Go is a hybrid, not a CSP-only language. This is worth being explicit about since Go is the go-to CSP example.

## 4. Key results/guarantees and where they stop holding

- **Mutual exclusion via locks** guarantees safety (no two threads in critical section simultaneously) *only if every access path to the shared data goes through the lock* — one missed lock anywhere in the codebase breaks the guarantee globally. This is the central point of Goetz's "thread safety" framing (*Java Concurrency in Practice*, ch. 2–4): safety is a property of the *whole program*, not of a single class.
- **Coffman conditions for deadlock** (Coffman, Elphick, Shoshani, 1971, "System Deadlocks," ACM Computing Surveys): deadlock requires all four of mutual exclusion, hold-and-wait, no preemption, circular wait. This is the standard reference for *why* lock-ordering discipline (breaking circular wait) is the standard fix, taught alongside dining philosophers.
- **CSP's "no shared state" guarantee rules out data races by construction**, but explicitly does **not** rule out deadlock — a cycle of processes each blocked sending/receiving to the next is a direct channel analogue of circular wait, and this is demonstrated in Go with a "channel deadlock" example (goroutine sends on unbuffered channel with no receiver → whole program deadlocks, detected at runtime by the Go scheduler when *all* goroutines are blocked).
- **Actors rule out data races on shared memory** (same argument as CSP — no shared mutable state) **and additionally avoid the specific CSP-style deadlock pattern of blocking sends**, because sends never block. But they introduce their own failure modes the model does not rule out: **mailbox overflow / unbounded queuing** (no backpressure by default), **message reordering across senders**, and **actor-level deadlock via circular `call` (synchronous request/reply) patterns** — Akka's `ask` pattern or Erlang's synchronous `gen_server:call` reintroduces blocking and thus reintroduces the possibility of a wait-cycle, so "actors can't deadlock" is an overstatement for any system that layers request/reply on top of raw async messaging (see §9).
- **None of the three models guarantees liveness or absence of livelock**, and none guarantees exactly-once/ordered delivery unless the specific runtime adds it (Erlang guarantees ordering only for messages between the *same* sender/receiver pair, not globally).

## 5. Standard concrete examples as they appear canonically

- **Lost update on a shared counter** (`counter++` from two threads without a lock) — appears in essentially every OS/concurrency textbook as the first race-condition example (Silberschatz ch. 5; Goetz ch. 2).
- **Dining philosophers** — Dijkstra 1965; shown with five philosophers/forks, canonical fix = resource ordering or a waiter/arbitrator process.
- **Producer–consumer / bounded buffer** — shown with a shared queue + mutex + two condition variables (not-full/not-empty) in the shared-memory version; directly re-shown with a buffered channel in the CSP version (this side-by-side is exactly the structure of the Go blog's "Share Memory By Communicating" codelab).
- **Bank account transfer** — Pike's CSP-vs-mutex talk example; also a classic example in transaction/database courses for atomicity.
- **Erlang "ping-pong" processes** and **the `gen_server` counter** — canonical minimal actor examples in *Programming Erlang* (Armstrong) and the Erlang official "Getting Started" docs.
- **Go's unbuffered-channel handoff ("goroutine gymnastics")** — canonical minimal CSP example in *The Go Programming Language* ch. 8 and the Go Tour.

## 6. Misconceptions and how the canonical treatment corrects them

- *"Message passing avoids concurrency bugs entirely."* Corrected by showing channel deadlock (CSP) and mailbox-overflow/ordering bugs (actors) — message passing changes **which** bugs are possible, it doesn't eliminate bugs (this is the explicit thesis of Pike's talk: it's about a different *default*, not a magic fix).
- *"Locks and message passing are fundamentally different mechanisms."* Corrected by pointing out message passing over a channel/mailbox is *implemented internally* using locks and condition variables — the model changes the **programmer-visible discipline**, not the underlying hardware reality (this point is made explicitly in Herlihy & Shavit and in Pike's talk — channels are a higher-level abstraction built on the same primitives).
- *"Actors and CSP are the same thing (both are 'message passing')."* Corrected by contrasting the blocking-send (CSP, rendezvous) vs. non-blocking-send (actors, mailbox) semantics directly — this is the single most important terminological correction in this lesson.
- *"More synchronization is always safer."* Corrected via the deadlock/lock-ordering material — excess or careless synchronization is precisely what *causes* deadlock and reduces liveness, not just an efficiency cost.
- *"Immutability solves concurrency."* Common practitioner over-claim not fully addressed by the three models directly, but worth a caveat: immutable data removes *write* races but doesn't remove logical races (e.g., stale reads, ordering of independent operations) — best flagged, not deep-dived, in a short lesson.

## 7. For a short lesson: essential / extra / cut

**Essential:**
- The single motivating race (lost update) to show why *any* discipline is needed.
- Three-way definition contrast: shared+locks (mutual exclusion, shared address space) vs. CSP (no shared state, synchronous rendezvous channels) vs. actors (no shared state, async mailboxes).
- One deadlock example (dining philosophers *or* channel deadlock — pick one, not both) to show every model still allows some class of bug.
- Pike's "share memory by communicating" framing as the memorable one-liner tying it together.

**Common extra (include if time allows, cut if tight):**
- Semaphores vs. monitors distinction.
- Coffman's four deadlock conditions by name.
- Real language mapping table (§8 below) — even a 15-second visual pass adds a lot of "this is real, not academic" credibility.

**Leave out for a short lesson:**
- CSP's formal process-algebra semantics (traces/failures/divergences) — that's a semester, not a scene.
- Software transactional memory, linearizability, and lock-free/wait-free algorithm proofs (Herlihy & Shavit's real focus) — worth a "there's a whole other world here" mention at most.
- Supervision trees / OTP "let it crash" philosophy — a great follow-up lesson, not this one.
- Distributed-systems-specific actor concerns (at-least-once delivery, network partitions) — out of scope unless the lesson is explicitly about distributed actors.

## 8. Real languages/systems canonically cited per model

| Model | Canonical language/system | Specific mechanism |
|---|---|---|
| Shared memory + locks | POSIX threads (pthreads), Java, C++ (`std::mutex`), C# | `pthread_mutex_t`, `synchronized`/`java.util.concurrent`, `std::mutex`/`std::condition_variable` |
| CSP | Go, occam (historical, built directly for transputers on CSP) | Goroutines + unbuffered channels (`chan`), `select` |
| Actors | Erlang/OTP, Akka (Scala/Java) | Lightweight process + mailbox, `!`/`send`/`receive`, `gen_server` |

Worth noting on camera: **Rust** is a canonical *fourth* data point for a different axis (compile-time enforcement) — `Send`/`Sync` traits statically rule out data races rather than relying on runtime discipline, and Rust's `std::sync::mpsc` channels are also a shared-memory-language's take on message passing. Useful as a "bonus" beat, not a fourth full model.

## 9. Commonly overstated or subtly wrong claims

- **"CSP/actors eliminate deadlock."** False — both can deadlock (channel deadlock; actor circular synchronous calls). Only *data races on shared memory* are ruled out, not deadlock or livelock in general.
- **"Actors can't deadlock because sends are async."** True only for pure fire-and-forget messaging; as soon as a system layers synchronous request/reply on top (very common in practice — Erlang's `call`, Akka's `ask`), circular waits reappear.
- **"Go is a CSP language."** Overstated — Go supports CSP-style channels *and* full shared-memory/mutex concurrency side by side; it is a hybrid, and idiomatic Go code uses both depending on the situation (the standard library's own internals use mutexes extensively).
- **"Message passing has no shared state, therefore no synchronization overhead."** Wrong at the implementation level — channels and mailboxes are implemented with locks/atomics/memory barriers under the hood; the benefit is a better *programming discipline* (harder to reach around it), not zero-cost coordination.
- **"The actor model was invented by Erlang/Akka."** Overstated — Hewitt's 1973 formalism predates Erlang (Ericsson, late 1980s) by over a decade; Erlang and Akka are implementations/popularizations, not the origin.
- **"Locks are inherently more error-prone than message passing."** Partly a value judgment rather than a proven result — what's actually established is that locks require *global* discipline across a codebase (any missed lock breaks safety everywhere) whereas channel/mailbox-based designs tend to localize the discipline to the boundary of communication; this is a real difference in *failure mode locality*, not a proof that one is strictly "safer" in all cases.

## 10. Best learned by animation vs. doing vs. reading

- **Narrated animation is best for:** the core mental model shift itself — showing two threads' program counters both mid-way through `counter++` (interleaved read-modify-write) to make the race *visible*; showing the rendezvous handshake of a CSP channel (sender and receiver literally meeting) vs. an actor mailbox filling up asynchronously. These are fundamentally about **timing and causality that text can't show as viscerally as motion** — this is exactly why Pike's own talks and most concurrency courses (e.g., MIT 6.005 lecture slides) lean on step-by-step interleaving diagrams.
- **Best learned by doing (interactive sim / running code):** deadlock. Reading about the dining philosophers doesn't build intuition the way *causing* a deadlock yourself does — flipping lock-acquisition order in a small interactive sim and watching the program hang is the standard "aha" (this is why OS courses universally pair the lecture with a lab assignment implementing dining philosophers or producer-consumer with real threads). Also best by doing: the "channel deadlock" and "mutex vs. channel" code contrast (Go's own codelab is literally structured as runnable-then-broken-then-fixed code).
- **Best learned by reading:** the precise terminology/definitions (mutex vs. semaphore vs. monitor; CSP vs. actor blocking semantics) and the named results (Coffman conditions) — these are discrete facts best absorbed as text/reference material a viewer can pause on and revisit, not narrated at video pace. This matches how Goetz's book and Herlihy & Shavit structure their early chapters: crisp boxed definitions before any code.

---

**Uncertain/flag for verification** (no web access this session to confirm exact citation details):
- Exact page/section numbers for Herlihy & Shavit and Silberschatz references above — I'm confident on chapter *topics* and book identity, less certain of edition-specific numbering.
- Whether Dijkstra's dining philosophers note is precisely EWD123 vs. a different EWD number — the 1965 date and Dijkstra attribution are solid; the exact note number I'd verify before putting on screen.
- The precise year/venue of Rob Pike's "Concurrency Is Not Parallelism" talk (I recall Heroku Waza 2012; there's also a related 2010 talk) — verify before citing an exact date on screen.
