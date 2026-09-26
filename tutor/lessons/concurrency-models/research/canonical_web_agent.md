# Concurrency models: share memory or pass messages? How the canonical sources teach it

Research notes for a short explainer. **[U]** means uncertain: from memory, or I could not check it against the source. Anything not marked was checked against the cited source (web, Sept 2026).

---

## 1. The canonical worked example

There are two competing standard examples. A third is standard for coordination.

**A. The shared counter, grown into a bank account ("lost update").** This is the most common through-line in modern courses and practitioner books.
- **Counter form:**
  - OSTEP ch. 26: two threads each run `counter = counter + 1` ten million times and print e.g. `19345221` instead of `20000000`. It then traces the load/add/store instructions step by step.
  - Butcher, *Seven Concurrency Models in Seven Weeks* (2014), ch. 2, Day 1 "Our First Lock".
  - Goetz et al., *Java Concurrency in Practice* (JCIP, 2006), ch. 2: "read-modify-write" and "check-then-act".
  - Rust Book §16.3: 10 threads share an `Arc<Mutex<i32>>`.
  - Kotlin coroutines guide, "Shared mutable state and concurrency": 100 coroutines × 1000 increments, fixed in turn by volatile (which fails), atomics, thread confinement and `Mutex`. Versions up to at least 1.6.4 also had an `actor` fix; the current docs dropped it.
  - Magee & Kramer, *Concurrency: State Models & Java Programs*, ch. 4, "Ornamental Garden" (two turnstiles update one counter).
- **Bank-account form:**
  - MIT 6.005/6.031 Reading 19 "Concurrency": cash machines deposit to and withdraw from a shared balance. The same bank is then rebuilt with message passing.
  - Regehr, "Race Condition vs. Data Race" (2011): `transfer1`–`transfer4`.
  - JCIP §10.1.2: `transferMoney`.
  - Peyton Jones, "Beautiful Concurrency" (2007), and Harris et al., "Composable Memory Transactions" (PPoPP 2005): account transfer as the motivating example for STM.
- **Why it is standard:**
  - It is the smallest program whose result depends on the interleaving.
  - Each model has an obvious version: a lock around the update, an actor or process that owns the balance, or a goroutine that receives deposit messages on a channel.
  - The bank version leads straight to the two bugs that message passing still allows:
    - a check-then-act race across messages. MIT R19/R22: two cash machines "both fooled into thinking they can safely withdraw the last dollar".
    - deadlock when a transfer needs two accounts (JCIP §10.1.2).

**B. Dining philosophers.** Dijkstra set it in 1965 as an exam problem; Hoare gave it its name.
- **Sources:**
  - Hoare, "Communicating Sequential Processes", CACM 21(8), 1978, §5.3.
  - Hoare, *CSP* (1985), §2.5: §2.5.3 "Deadlock!", the footman fix (credited to Scholten), §2.5.4 "Proof of absence of deadlock", and §2.5.5 "Infinite overtaking", which is starvation.
  - Butcher ch. 2, Day 1 "Multiple Locks", plus the Day 2 `tryLock` and condition-variable versions.
  - Magee & Kramer ch. 6.
  - Ben-Ari, *Principles of Concurrent and Distributed Programming* (2nd ed. 2006), solutions with semaphores and with monitors.
- **Why it is standard:** it is the universal deadlock and starvation example. Hoare's 1985 preface says that even in "a single hour's seminar it is possible … to get as far as the edifying tale of the five dining philosophers."
- **Why it matters for this lesson:** it deadlocks *under message passing too*. Hoare 1978 §5.3 says of his own CSP solution: "does not prevent all five philosophers from entering the room, each picking up his left fork, and starving to death because he cannot pick up his right fork."

**C. Coordination: producer–consumer / bounded buffer.**
- **Sources:** Dijkstra's semaphores came out of this problem (OSTEP ch. 30). It also appears in Hoare's monitors (CACM 1974) **[U: exact section]**, Hoare 1978 §5.1 and JCIP §5.3 (`BlockingQueue`).
- **Why it matters:** with channels it becomes trivial ("This is exactly what Go's buffered channels provide", from the Go port of Hoare's paper, github.com/thomas11/csp).

**Which is more common:**
- A (counter/bank) is the more common spine in a "share memory vs pass messages" lesson.
- B dominates the formal/CSP tradition (Hoare, Ben-Ari, Magee & Kramer) and is *the* deadlock example.
- The usual pattern is A for races and B for deadlock.

## 2. The standard progression

**Consensus order:**
- OSTEP Part II (ch. 26–33).
- JCIP Part I, then ch. 10.
- Butcher ch. 2 (threads & locks), ch. 5 (actors), ch. 6 (CSP).
- Andrews, *Foundations of Multithreaded, Parallel, and Distributed Programming* (2000): Part 1 shared-variable programming, then Part 2 message passing, RPC and rendezvous.
- Ben-Ari 2006: interleaving, then critical section, semaphores, monitors, channels, spaces.
- Magee & Kramer: ch. 4 shared objects, ch. 5 monitors, ch. 6 deadlock, ch. 10 message passing.

**Steps:**
1. **Concurrency ≠ parallelism, and the interleaving model.**
   - Butcher ch. 1, "Concurrent or Parallel?".
   - Pike, "Go Concurrency Patterns" (Google I/O 2012): "If you have only one processor, your program can still be concurrent but it cannot be parallel."
   - Pike, "Concurrency is not Parallelism" (Heroku Waza, 2012).
2. **Shared memory: an unsynchronized counter races.**
3. **Critical section, then a lock/mutex:** the counter is fixed.
4. **(Often) visibility and reordering.** Butcher "Mysterious Memory", JCIP ch. 3, MIT R19 "Reordering".
5. **Condition synchronization:** producer–consumer with condition variables, semaphores or monitors.
6. **Deadlock.**
   - Two locks, then dining philosophers.
   - Then the four Coffman conditions, then lock ordering and timeouts.
   - Sources: OSTEP ch. 32; JCIP ch. 10; Butcher Days 1–2.
7. **Message passing as the alternative.**
   - Magee & Kramer order: synchronous *channel*, then asynchronous *port*, then *rendezvous* (entry).
   - Butcher puts actors (ch. 5) before CSP (ch. 6).
   - Pike 2012: goroutine, channel, buffered channel, `select`, timeout, patterns (fan-in, quit channel, Google Search).
8. **Close:** message passing still has races and deadlocks.
   - MIT 6.031 "Queues and Message-Passing".
   - Hoare 1978 §5.3.
   - Tu et al., ASPLOS 2019.

**Variant (MIT 6.005/6.031):**
- Both models are introduced on day one with the same bank example (R19).
- Then thread-safety strategies: confinement, immutability, thread-safe types, synchronization (R20).
- Then message passing with `BlockingQueue` (R22), then locks and deadlock (R23).

**Simpler version shown before the full one:**
- Counter: unsynchronized, then locked, then atomic (Butcher Day 1 → Day 2; Kotlin).
- Locks: one lock, then two locks (deadlock), then ordered locks (JCIP 10.1.1–10.1.2).
- Philosophers: naive (deadlocks), then fixed with a footman/waiter, resource ordering, or `tryLock`.
- CSP: Hoare 1978 lets processes name each other directly (`producer?x`) with no buffering. Named channels came later (1985 book, occam, Go).
- Channels: unbuffered first, then buffered (Pike's slide "An Aside About Buffered Channels"). In the 1985 book, "if buffering is required on a channel, this is achieved by interposing a buffer process".
- Actors (Butcher ch. 5): spawn/send/receive, then stateful actor via recursion, then links and supervisors ("let it crash"), then distribution.

## 3. The models and their terminology

**Model definitions and guarantees:**

| Model | Standard definition | What it guarantees | What it does not |
|---|---|---|---|
| **Shared memory + locks** ("threads and locks"; Rust "shared-state concurrency"; Lauer & Needham's "procedure-oriented" systems; Hoare 1974 / Brinch Hansen *monitors*) | MIT R19: "Concurrent modules interact by reading and writing shared objects in memory." A mutex allows at most one thread in a critical section. A monitor is "encapsulated data + access procedures, mutual exclusion + condition synchronization" (Magee & Kramer ch. 5). | Mutual exclusion among code holding the *same* lock. Unlock happens-before the next lock of that mutex, so if *every* shared access is protected the program is data-race-free and, by DRF-SC, appears sequentially consistent. | Atomicity of anything larger than one critical section. Freedom from deadlock and starvation. Composition (Harris et al. 2005). |
| **Actors** (Hewitt, Bishop & Steiger, IJCAI 1973; Agha, *Actors*, MIT Press 1986) | An actor has private state and an address (mailbox). On receiving a message it can: "send a finite number of messages to other actors; create a finite number of new actors; designate the behavior to be used for the next message it receives". Sends are asynchronous and go to a named actor. | One message at a time per actor. Butcher ch. 5: "handles messages sequentially … We only have to worry about concurrency when sending messages." Akka's "actor subsequent processing rule". Swift SE-0306: "no data races on actor-isolated mutable state." | Pure model: "no requirement on order of message arrival". Erlang/Akka give FIFO per sender–receiver pair only, and delivery is at-most-once or "unreliable" (Armstrong 2003). No atomicity across actors or across a request/reply. No deadlock freedom once actors wait for replies. |
| **CSP** (Hoare, CACM 1978; *CSP* book 1985; Roscoe, *Theory and Practice of Concurrency* 1997) | Sequential processes with no shared variables. Input and output are primitives. Communication is a synchronous rendezvous: sender and receiver both wait. A guarded alternative (occam `ALT`, Go `select`) chooses among ready communications. In 1978 processes name each other and there is no buffering; from 1985, named channels. | Each communication is also a synchronization point. Go memory model: "A send on a channel is synchronized before the completion of the corresponding receive". The semantics are mathematical (traces, failures, divergences), so deadlock freedom can be proved (1985 §2.5.4) or model-checked (FDR). | Deadlock freedom (see the philosophers). In Go, isolation is not enforced: you can send a pointer and keep using it. |

**Actor vs CSP.** Wikipedia's CSP article, "Comparison with the actor model", lists three differences:
- CSP processes are anonymous; actors have identities.
- CSP uses explicit channels; actors send to named destinations.
- CSP communication is a rendezvous; actor messaging is asynchronous.

Two sources explain or refine this:
- **Armstrong's reason for going asynchronous** (thesis, 2003, §2.4.3): "If process communication is synchronous then a software error in the receiver of a message could indefinitely block the sender … destroying the property of isolation."
- **Pike 2012** ("History"/"Distinction" slides): "Erlang is closer to the original CSP, where you communicate to a process by name rather than over a channel."

**Terms that differ across fields and sources:**
- **Data race vs race condition.**
  - A *data race* is two concurrent accesses to the same location, at least one a write, not ordered by synchronization (Regehr 2011; Rustonomicon "Races"; Go memory model; C++11; JLS §17.4).
  - A *race condition* is when "the correctness of a computation depends on the relative timing or interleaving" (JCIP §2.2.1; MIT R19).
  - Other names for the second kind:
    - Rust: "general race condition"/"resource race".
    - Lu et al. 2008: "atomicity violation" and "order violation".
    - Swift SE-0306: "'high level' kinds of races".
- **"Process"** means three different things: an OS process, a CSP process (an abstract sequential component), and an Erlang process (a lightweight actor; see Butcher's box "Actor or Process?").
- **"Monitor":**
  - Hoare/Brinch Hansen: mutual exclusion plus condition variables. Java's per-object "monitor"/intrinsic lock is the same idea.
  - Erlang `monitor`: a one-way *failure notification* (a `'DOWN'` message).
- **"Actor":**
  - Hewitt actor.
  - Lee/Ptolemy "actor-oriented" dataflow components (Lee 2006) are a different thing.
- **Channel / port / mailbox / entry** (Magee & Kramer ch. 10):
  - *channel*: synchronous, one-to-one.
  - *port*: asynchronous, many-to-one queue.
  - *entry*: rendezvous with call/accept/reply, as in Ada.
  - A Go "channel" may be buffered, i.e. asynchronous up to its capacity. An actor's "mailbox" is normally an unbounded queue owned by the receiver.
- **"Synchronous/asynchronous":**
  - Message passing: does the sender wait for the receiver?
  - async/await: non-blocking I/O with continuations.
  - RPC: a "synchronous" call means request/response.
- **"Message passing":**
  - Smalltalk-style OO "message send" is really a method call. Armstrong (erlang-questions, 2014): "Erlang is *not* a implementation of the Actor model", and in Erlang "we really do send a message to an object".
  - In HPC it means MPI.
- **"Deadlock":**
  - *Resource* vs *communication* deadlock (Chandy, Misra & Haas, ACM TOCS 1983).
  - Related liveness failures: *livelock*, and *starvation* (Hoare calls it "infinite overtaking").
- **"Thread-safe"** (JCIP §2.1): a class is thread-safe if it behaves correctly under any interleaving without extra coordination by callers.

## 4. Key results and guarantees: assumptions and where they stop holding

1. **Interleaving semantics** (Ben-Ari ch. 2; OSTEP ch. 26). A concurrent program is correct only if it is correct for *every* interleaving.
   - *Assumes* sequential consistency.
   - *Stops holding* on real hardware and compilers for racy programs (MIT R19 "Reordering"; Butcher "Mysterious Memory").
2. **DRF-SC** (Adve & Hill, "Weak ordering—a new definition", ISCA 1990; Java memory model, Manson/Pugh/Adve, POPL 2005; C++11, Boehm & Adve, PLDI 2008; Go memory model). Programs without data races behave as if sequentially consistent.
   - *Assumes* all synchronization goes through the language's primitives.
   - *Stops holding* for racy programs:
     - C/C++: undefined behaviour.
     - Go: "races on multiword data structures … can in turn lead to arbitrary memory corruption."
     - "Benign" races can be miscompiled (Boehm, HotPar 2011).
   - It says **nothing** about race conditions.
3. **Coffman conditions** (Coffman, Elphick & Shoshani, "System Deadlocks", ACM Computing Surveys 3(2), 1971). The four conditions are mutual exclusion, hold-and-wait, no preemption and circular wait. They are *necessary*, so breaking one prevents deadlock. Lock ordering breaks circular wait (OSTEP §32.3).
   - *Assumes* exclusive, non-preemptible resources.
   - *Stops holding:*
     - Lock ordering needs global knowledge and "is not modular" (MIT R23). Lee 2006: "no method signature in any widely used programming language indicates what locks the method acquires".
     - Lock order can depend on arguments (JCIP `transferMoney`).
     - Calling "alien methods" while holding a lock breaks it (Butcher; JCIP §10.1.3–10.1.4 "open calls").
     - Communication deadlocks follow a different model (Chandy et al. 1983). The same wait-for-cycle picture still applies (MIT 6.031: "an edge from A to B if module A is blocked waiting for module B").
4. **Locks do not compose** (Harris, Marlow, Peyton Jones & Herlihy, PPoPP 2005; Peyton Jones 2007): "taking too few locks … too many … the wrong locks … in the wrong order". Two correct lock-based operations do not make a correct combined operation.
5. **Duality** (Lauer & Needham, "On the Duality of Operating System Structures", 1978; reprinted in OSR 13(2) 1979). Message-oriented and procedure-oriented systems "are duals of each other"; "neither model is inherently preferable", and the choice depends on the machine architecture, not the application.
   - Hoare 1978 shows the same point in miniature: §5.2 builds a semaphore *as a process*, and §4.x represents data structures as processes.
   - The Go memory model notes a buffered channel "can be used like a counting semaphore".
   - *Assumes* the paper's canonical models.
   - The lesson: **the models differ in defaults and discipline, not in expressive power.**
6. **Actor isolation.** Per-actor sequential processing means no data races on actor-private state.
   - *Assumes:*
     - Messages are immutable or copied. Akka: "Messages should be immutable, this is to avoid the shared mutable state trap."
     - State is not closed over in futures or callbacks (Akka docs, "Akka and the Java Memory Model").
     - No shared side-channels.
   - *Stops holding:*
     - Erlang's ETS tables and process registry (Christakis & Sagonas, PADL 2010: the "shared nothing" slogan "is an oversimplification").
     - Reentrancy at `await`. Swift SE-0306: execution "may 'interleave' at suspension points"; "every suspension point must be carefully inspected".
   - *Ordering:*
     - Pure model: none.
     - Erlang: order preserved per sender–receiver pair, but "S1 may still be lost".
     - Akka: "at-most-once delivery" and "message ordering per sender–receiver pair". This is *not transitive*: if A→C directly and A→B→C, the messages can arrive in either order.
7. **CSP synchronization and verifiability.** A rendezvous orders the two processes (Go memory model rules for unbuffered and buffered channels). Deadlock freedom is a provable, checkable property (Hoare 1985 §2.5.4; FDR).
   - Known design rules give deadlock freedom by construction, e.g. client–server and I/O-PAR (Welch et al. 1993; Martin 1996 thesis) **[U: exact citations]**.
   - *Stops holding* without such discipline: a cycle of blocked sends/receives, or full buffers.
8. **Determinism of Kahn process networks** (Kahn, IFIP 1974). Processes that communicate only by blocking reads on FIFO channels (no emptiness test, no `select`) compute a deterministic result regardless of scheduling.
   - Lee 2006 uses this to argue threads are "wildly nondeterministic" and that we should "start with deterministic, composable mechanisms".
   - *Stops holding* once you add `select`/`ALT`, timeouts or multiple writers.
9. **Language-level guarantees:**
   - Safe Rust has no data races (ownership plus `Send`/`Sync`). But "Rust does not prevent general race conditions", and `Mutex<T>` "comes with the risk of creating deadlocks" (Rustonomicon; Rust Book §16.3).
   - Pony: "data-race free … deadlock free. This one is easy, because Pony has no locks at all!" (Pony tutorial).
10. **Empirical results:**
    - **Lu, Park, Seo & Zhou, ASPLOS 2008** (via OSTEP ch. 32): 105 bugs in MySQL, Apache, Mozilla and OpenOffice. 74 were non-deadlock bugs, of which 97% were atomicity or order violations; 31 were deadlocks.
    - **Tu, Liu, Song & Zhang, ASPLOS 2019** ("Understanding Real-World Concurrency Bugs in Go"): 171 bugs from Docker, Kubernetes, etcd, gRPC, CockroachDB and BoltDB.
      - Blocking bugs: 49 of 85 (~58%) were caused by message passing and 36 by shared memory. "Contrary to the common belief that message passing is less error-prone, more blocking bugs … are caused by wrong message passing."
      - Non-blocking bugs: 17 from message passing vs 69 from shared memory. "When used correctly, message passing can be less prone to non-blocking bugs."
      - Tooling: Go's built-in deadlock detector caught 2 of 21 reproduced blocking bugs, and the race detector caught 10 of 20 non-blocking bugs.

**Summary for the lesson: what each model rules out and what it still allows.**

| Bug class | Threads + locks | Actors | CSP channels |
|---|---|---|---|
| Data race on shared variable | Prevented only by discipline (every access under the right lock). Rust enforces it. | Ruled out for actor-private state. Enforced by copying in Erlang and by the compiler in Swift/Pony; by convention in Akka/Kotlin. | Ruled out if values are handed off and not touched after send. Convention in Go; enforced by ownership in Rust. |
| Atomicity violation (check-then-act across operations or messages) | Allowed | Allowed (MIT bank; Erlang `whereis`/`register`) | Allowed |
| Order/interleaving nondeterminism | Allowed | Allowed: arrival order across senders, reentrancy | Allowed: `select` picks arbitrarily |
| Deadlock | Allowed (lock cycles) | Allowed when actors wait for replies (Erlang `gen_server:call` cycles, Orleans grains, Akka `ask` + block) | Allowed (Hoare §5.3; blocked send/receive cycles) |
| Starvation / livelock | Allowed | Allowed | Allowed (Hoare §2.5.5) |
| Unbounded queue growth | n/a | Typical risk with unbounded mailboxes | Bounded channels give backpressure instead, and can block or deadlock **[my synthesis]** |

## 5. Standard concrete examples as they appear in the sources

**Counter race** (OSTEP ch. 26):
```c
static volatile int counter = 0;
void *mythread(void *arg) { for (int i = 0; i < 1e7; i++) counter = counter + 1; return NULL; }
// main: done with both (counter = 19345221)   -- expected 20000000
```
The chapter then shows a trace table for `mov 0x8049a1c,%eax; add $0x1,%eax; mov %eax,0x8049a1c`: two threads both load 50 and both store 51.

**Dynamic lock-order deadlock** (JCIP Listing 10.2): `transferMoney(from, to, amt)` does `synchronized(from){ synchronized(to){…} }`. Thread A runs transfer(x,y) while thread B runs transfer(y,x). The fix (Listing 10.3) orders the locks by `System.identityHashCode`, with a tie-breaking lock.

**Race under message passing** (MIT R19/R22):
- The account becomes a module that receives messages.
- A cash machine sends `get-balance`, sees 1, then sends `withdraw(1)`. Two machines can interleave these messages.
- The fix is a better atomic operation: "`withdraw-if-sufficient-funds` would be a better operation than just `withdraw`."

**Deadlock under message passing** (MIT 6.031 Sp20, "Queues and Message-Passing"): a client fills the server's bounded queue and blocks. The server then fills the client's queue and blocks. Each now waits for the other.

**Bounded buffer as a CSP process** (Hoare 1978 §5.1; transcription **[U: exact glyphs]**):
```
X:: buffer:(0..9)portion; in,out:integer; in:=0; out:=0;
*[ in < out+10; producer?buffer(in mod 10) → in := in+1
 □ out < in; consumer?more() → consumer!buffer(out mod 10); out := out+1 ]
```
Other examples in the same paper: §5.2 integer semaphore, §5.3 dining philosophers, §6.1 the prime sieve (which became Go's classic "concurrent prime sieve" **[U: exact location on go.dev]**), §6.2 matrix multiplication.

**Go's "share memory by communicating":**
- Effective Go: "Do not communicate by sharing memory; instead, share memory by communicating."
- Gerrand, Go blog/codelab 2010: a URL poller written first with a `sync.Mutex`-protected `Resources` struct, then with channels.
- Pike 2012 patterns: generator, fan-in, `select`, timeout, quit channel, daisy-chain, "Google Search 1.0 → 3.0".

**Goroutine leak** (Tu et al. 2019, Fig. 1, from Kubernetes):
```go
ch := make(chan ob)            // fix: make(chan ob, 1)
go func() { result := fn(); ch <- result }()   // blocks forever if parent already left
select { case result = <-ch: return result
         case <-time.After(timeout): return nil }
```

**Erlang race without shared variables** (Christakis & Sagonas 2010):
```erlang
case whereis(Name) of undefined -> Pid = spawn(...), register(Name, Pid); Pid -> true end
```
Two processes can both see `undefined`, and the second `register` then crashes. ETS `public` tables give similar read-modify-write races.

**Actor deadlock** (Microsoft Orleans docs, "Request scheduling"):
- `await Task.WhenAll(a.CallOther(b), b.CallOther(a))` on non-reentrant grains "might deadlock, depending on the non-deterministic timing"; Orleans resolves it by timeout.
- Enabling reentrancy removes the deadlock but reintroduces interleaving: "Incorrect use can lead to race conditions".
- Swift SE-0306 makes the same trade-off. Reentrancy "all but eliminates the potential for deadlocks" at the cost of high-level races.
- Erlang: `gen_server:call` to itself hangs (`calling_self`), and the default call timeout is 5000 ms.

**Other standard examples:**
- **Observer-pattern deadlock** (Lee, "The Problem with Threads", IEEE Computer 2006):
  - `synchronized setValue` calls listeners while holding the lock.
  - Lee reports a Ptolemy II deadlock that went undetected for four years despite 100% coverage tests.
  - Same idea as Butcher's "The Perils of Alien Methods".
- **Actors in Elixir** (Butcher ch. 5 Day 1): a `Talker` with `receive do {:greet, name} -> … end`, and a stateful counter actor built with recursion.
- **Rust** (Book §16.2): `tx.send(val)` moves `val`, so using it afterwards is a compile error. Channels are "similar to single ownership" (§16.3).

## 6. Misconceptions practitioners bring, and how the canonical treatment corrects them

1. **"Actors or channels mean no race conditions."**
   - Correction: they remove *data races on encapsulated state* only.
   - The standard teaching move is to rerun the same bank race with messages (MIT R19/R22). Also Christakis & Sagonas 2010; Swift SE-0306 "high-level races".
2. **"Message passing can't deadlock."**
   - Correction: Hoare's own philosophers deadlock (1978 §5.3; 1985 §2.5.3). Also MIT 6.031 (full queues), Orleans (call cycles), and Tu 2019 (58% of Go blocking bugs).
3. **"A race condition and a data race are the same thing."**
   - Correction: Regehr 2011 builds a 2×2 matrix with the bank transfer. "Freedom from data races is a very weak property that is neither necessary nor sufficient".
4. **"If every method is `synchronized`, or every type is thread-safe, the program is thread-safe."**
   - Correction: compound actions such as check-then-act and put-if-absent need a larger atomic unit (JCIP §2.2, §4.4, §5.1.1).
   - MIT's corrective: design operations like "withdraw-if-sufficient-funds" as a single operation.
5. **"`volatile` or atomics fix it."**
   - JCIP §3.1.4: volatile does not make `count++` atomic.
   - Kotlin guide: "Volatiles are of no help".
   - Atomics fix one variable, not an invariant across two.
6. **"It passed the tests."**
   - Correction: MIT R19, "Concurrency is hard to test and debug". Lee 2006: a deadlock appeared four years into production use, and "testing may never reveal all the problems".
7. **"Code runs in the order I wrote it."**
   - Correction: MIT R19 "Reordering" (`answer = 42; ready = true`); Butcher "Mysterious Memory"; JCIP ch. 3.
8. **"async/await or single-threaded event loops have no races."**
   - OSTEP ch. 33, "Why Simpler? No Locks Needed", holds only on one CPU with no blocking inside a handler.
   - Python ships `asyncio.Lock` "to guarantee exclusive access to a shared resource".
   - Orleans and Swift show interleaving at `await`.
9. **"Concurrency = parallelism"** (Pike 2012).
10. **"Benign data races are harmless"** (Boehm 2011; C/C++ undefined behaviour; Go multiword corruption).
11. **"Go forces you to use channels; the slogan means never use a mutex."**
    - Correction: Effective Go says "This approach can be taken too far". The Go wiki (MutexOrChannel) says "Use whichever is most expressive and/or most simple"; channels suit passing ownership, distributing work and async results, while mutexes suit caches and state.

## 7. For a short lesson

**Essential:**
- The two families and the Go slogan.
- Interleaving: the counter or bank lost update.
- Data race vs race condition.
- Locks fix the data race but can deadlock (two accounts, or philosophers).
- Lock ordering as the standard fix.
- Actor = private state + mailbox + one message at a time, so no data races on its state.
- CSP = processes + channels + rendezvous.
- **What is still allowed in every model:** check-then-act across messages, and deadlock as a cycle of waits.
- The "rules out / still allows" table (§4).

**Common extras:**
- Visibility and reordering; DRF-SC.
- The four Coffman conditions.
- Buffered vs unbuffered channels; `select`.
- Supervision and "let it crash".
- Actor reentrancy (Swift/Orleans).
- Rust `Send`/`Sync`; STM (Clojure, Haskell).
- Lauer–Needham duality.
- The Tu 2019 / Lu 2008 statistics.
- Concurrency vs parallelism.

**Leave out:**
- Process-algebra formalism (traces, failures, FDR); π-calculus.
- The Hewitt–Hoare "unbounded nondeterminism" debate.
- Lock-free algorithms, linearizability, consensus numbers.
- Memory-model internals (acquire/release, out-of-thin-air).
- Peterson's algorithm and the banker's algorithm.
- Distributed deadlock detection (Chandy–Misra–Haas).
- Readers–writers variants; tuple spaces (Linda).
- GPU / data parallelism.
- Distributed actor clustering.
- The "Erlang is/isn't Hewitt actors" history.

## 8. Languages and systems canonically cited

**Threads + locks:**
- **Java:**
  - `synchronized` intrinsic monitor locks and `wait`/`notify` (JLS ch. 17).
  - `java.util.concurrent`: `ReentrantLock`, `AtomicInteger`, `BlockingQueue`.
  - Sources: JCIP, Butcher ch. 2, MIT.
- **C/C++:**
  - pthread mutex and condition variables (OSTEP).
  - C++11 `std::mutex`/`std::atomic`; a data race is undefined behaviour.
- **Go:** `sync.Mutex`, `RWMutex`, `WaitGroup`, `sync/atomic`.
- **Rust:** `Mutex<T>` owns the data it guards, and `Arc<T>` shares it; the compiler rejects unsynchronized sharing (`Send`/`Sync`).
- **Databases:** transactions (MIT R23 "Concurrency in practice").

**Actors:**
- **Erlang/Elixir (BEAM):**
  - Lightweight processes, pids, `!`/`send`, and `receive` with selective receive.
  - FIFO per pair.
  - Links and monitors; OTP `gen_server` `call`/`cast`; supervisors.
  - Isolation by copy semantics, with ETS as the shared escape hatch.
  - Sources: Armstrong 2003 thesis; Butcher ch. 5.
- **Akka (JVM):** `ActorRef`, `tell`/`ask`, mailboxes, supervision, at-most-once delivery and per-pair ordering.
- **Orleans (.NET):** virtual actors ("grains"); single-threaded, turn-based, non-reentrant by default; call timeouts.
- **Swift actors (SE-0306):** compiler-checked isolation and `Sendable`; reentrant at `await`.
- **Pony:** reference capabilities, no locks.
- **Kotlin:** the `actor {}` coroutine builder (older guide).

**CSP:**
- **occam** (INMOS transputer, 1983): point-to-point synchronous channels, `PAR`, `ALT`. The compiler forbids shared writable variables in `PAR` **[U]**.
- **Go:**
  - goroutines, `chan` (unbuffered or buffered), `select`, `close`.
  - Shared memory is also allowed.
  - Tools: `-race` detector; runtime "all goroutines are asleep – deadlock!" for global deadlock only.
  - Lineage (Pike 2012): Newsqueak, Alef, Limbo; "distinguished by first-class channels".
- **Clojure core.async:** `go` blocks, `chan`, `alts!` (Butcher ch. 6).
- **Kotlin coroutines:** `Channel`.
- **Rust:** `std::sync::mpsc` (send moves ownership).
- **Ada:** rendezvous (entry/`accept`/`select`), CSP-like but two-way.
- **FDR:** the CSP model checker.

## 9. Claims that are commonly overstated or subtly wrong

1. **"Message passing / actors eliminate races."** They eliminate *data races*, and only when isolation is enforced: Erlang by copying, Swift/Pony/Rust by the compiler. In Akka, Kotlin and Go it holds only by convention.
   - Effective Go's own "Data races cannot occur, by design" is conditional on the discipline. Tu 2019 found 69 shared-memory non-blocking bugs in Go code.
2. **"Message passing is deadlock-free" / "Actors can't deadlock."** False in general (§5, §6).
   - Pony's "deadlock free" means *no lock-based deadlock* because nothing blocks. A protocol can still stall waiting for a message that never comes. **[my inference; not stated in Pony docs]**
3. **"Rust's fearless concurrency means no concurrency bugs."** The Rust Book says code is "free of subtle bugs". The Rustonomicon is precise: data races are prevented; deadlocks and race conditions are considered "safe".
4. **"Erlang shares nothing."** Christakis & Sagonas 2010 call this "an oversimplification": ETS, the registry and other built-ins share data.
5. **"Actor messages arrive in order."** Only per sender–receiver pair (Erlang, Akka). Not in Hewitt's model, and not transitively (Akka docs).
6. **"The Coffman conditions are necessary and sufficient."** Coffman et al. give them as necessary conditions. Some texts say "necessary & sufficient" (Magee & Kramer slides), which holds only under single-instance resource assumptions **[U: exact scope]**. They also describe *resource* deadlock, not communication deadlock.
7. **"Lock ordering solves deadlock."** Only if every lock is known globally. It is non-modular (MIT R23; Lee 2006; JCIP's alien methods and open calls).
8. **"One model is more powerful, or inherently faster."** Lauer & Needham's duality says no; each model can simulate the other (Hoare §5.2; Go's semaphore-channel rule).
9. **"Go is CSP" / "CSP vs actors = sync vs async."**
   - Hoare's 1978 CSP named processes and had no buffering.
   - Go adds buffered, first-class channels and allows shared memory.
   - Pike himself says Erlang is closer to 1978 CSP on naming.
   - Sync vs async is only one of three differences, and buffered channels blur it.
10. **"Erlang implements Hewitt's actor model."** Armstrong (2014): "Erlang is *not* a implementation of the Actor model … It was purely pragmatic."
11. **"Message passing is less error-prone."** Tu 2019: fewer non-blocking bugs but *more* blocking bugs in Go.
12. **"An event loop needs no synchronization."** True only when no critical region spans an `await` or blocking call (OSTEP ch. 33; asyncio; Swift/Orleans reentrancy).

## 10. What to learn by watching, by doing, and by reading

**Watch a narrated animation** for things that are about *order over time*, where the narrator can freeze the critical instant:
- **Lost update:** two threads step through load/add/store. OSTEP's trace table is already a storyboard.
- **The same bank race redone with messages:** the reply arrives, then another request is interleaved before `withdraw`.
- **Deadlock:** a wait-for cycle forming (two accounts, or five forks). Then lock ordering breaks the cycle.
- **Communication styles:** an actor mailbox draining one message at a time, compared with a CSP rendezvous where the sender waits until the receiver arrives.
- **Actor reentrancy:** the state changes across an `await`.
- **Precedent:** Danyliuk, "Visualizing Concurrency in Go" (GopherCon 2016). Hoare's preface: "Each example presents a little drama which can be acted".
- **Avoid** animating memory reordering. It is hard to depict faithfully and easy to mislead.

**Learn by doing (simulation, running code, exercises),** because nondeterminism and "correct for all interleavings" are only believed once experienced:
- **Play the scheduler** to force a bad interleaving: The Deadlock Empire (deadlockempire.github.io), where you break C# programs by stepping threads.
- **Run the counter many times** and get different wrong answers (OSTEP homework). Run `go run -race`.
- **Try to share a counter across threads in Rust** without `Mutex` and read the compiler's refusal.
- **Deadlock the philosophers, then fix them** with lock ordering or a footman.
- **Deadlock Go on purpose** to see "all goroutines are asleep". Then a partial deadlock the runtime *doesn't* detect (Tu Fig. 1).
- **Spawn, send and receive in an Erlang/Elixir REPL.**
- **Model-check with LTSA** (Magee & Kramer) or FDR, for advanced learners.

**Read** for precise definitions and conditional guarantees, where qualifiers matter and learners will come back for reference:
- **Definitions:** data race vs race condition; DRF-SC; the Coffman conditions.
- **Per-platform guarantees:** Erlang ordering and loss; Akka at-most-once and pairwise ordering; the Go memory model's channel rules; Rust `Send`/`Sync`.
- **Evidence and arguments:** Lauer–Needham, Lee 2006, and the empirical studies (Lu 2008, Tu 2019). These are nuanced, and narration moves too fast for their caveats.

---

### Key sources (all cited inline above)

- **Textbooks and courses:**
  - OSTEP ch. 26/30/32/33 (pages.cs.wisc.edu/~remzi/OSTEP)
  - MIT 6.005 Fa15 Readings 19, 22, 23; 6.031 Sp20 "Queues and Message-Passing"
  - Butcher 2014 (TOC and actors excerpt, pragprog.com)
  - JCIP 2006
  - Magee & Kramer 2nd ed. (course handouts)
  - Ben-Ari 2006
  - Andrews 2000
  - Hoare 1978 (CACM 21(8):666–677) and *CSP* 1985 (usingcsp.com)
  - Rust Book ch. 16 and Rustonomicon "Races"
- **Language and platform docs:**
  - Effective Go; Go memory model; Go wiki MutexOrChannel; Gerrand 2010; Pike 2012 slides
  - Akka "Message Delivery Reliability" and "Akka and the JMM"
  - Erlang reference manual "Processes"; `gen_server` docs
  - Orleans "Request scheduling"; Swift SE-0306; Pony tutorial
  - Kotlin "Shared mutable state and concurrency"; Python asyncio-sync
- **Papers, theses and essays:**
  - Armstrong thesis 2003 and erlang-questions post (June 2014)
  - Lauer & Needham 1978/79
  - Coffman et al. 1971; Chandy, Misra & Haas 1983
  - Adve & Hill 1990; Boehm 2011
  - Lee 2006; Harris et al. 2005; Peyton Jones 2007
  - Regehr 2011
  - Lu et al. 2008; Tu et al. 2019
  - Christakis & Sagonas 2010; Claessen et al., ICFP 2009 (QuickCheck/PULSE races in Erlang)
  - Akka bug studies (Hedden & Zhao 2018; Bagherzadeh et al., OOPSLA 2020) **[U: details not read]**
- **Other:** Wikipedia "Communicating sequential processes", "Actor model", "Dining philosophers problem".
