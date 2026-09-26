# Share Memory, or Pass Messages?

Status: locked after review round 6

## Argument

**Question.** Two cash machines deposit $50 each, at the same moment, into an account holding $100. Sometimes the balance ends at $150: a deposit vanished. Programs coordinate concurrent work in different ways: threads that share memory and use locks, or parts that share nothing and pass messages (actors, channels). Go's documentation says: "Do not communicate by sharing memory; instead, share memory by communicating." Does passing messages make bugs like the vanishing deposit go away?

**Answer.** Partly. The deposit vanishes because two threads interleave read-add-write on shared memory (a data race). A lock makes the three steps one, but it only protects code that takes it, and two locks taken in opposite orders can deadlock. Message passing gives the balance a single owner (an actor with a mailbox, or a process receiving from a channel) that handles one request at a time, so there is no data race on the balance, by the structure of the program. But a check-then-act spread over two messages still races, and processes that wait on each other can still deadlock. Every model leaves two decisions to the programmer: which steps must happen as one, and how to keep waits from forming a cycle.

**Takeaway.** Passing messages rules out data races on state that has one owner. It doesn't rule out race conditions or deadlock: in every model you still choose what happens as one step, and keep waits from forming a cycle.

**Wrong model.** Actors and channels remove concurrency bugs; message passing is simply the safe model and shared memory the unsafe one.

**Objectives.**
1. Explain the lost update: how two read-add-write sequences interleave, and what a data race is.
2. Explain how a lock fixes it, and how two locks can deadlock; name lock ordering as the standard fix.
3. Describe an actor and a channel (CSP): what each guarantees about the state it owns, and how the two differ.
4. Show that message passing still allows a race condition (check, then act) and a deadlock, and fix the race by making the check and the action one message.
5. Say what each model makes automatic and what it leaves to the programmer.

## Chain

1. The question: two deposits, one vanishes. Go says pass messages. Does that make such bugs go away?
2. The deposit is read, add, write; two interleaved sequences lose an update. That's a data race, and it happens: a shared counter comes out millions short.
3. Therefore a lock makes the three steps one. But it only protects code that takes it, and a transfer needs two locks, which can deadlock; the fix is one fixed lock order everywhere.
4. Therefore, the message-passing alternative: give the balance one owner. An actor handles one message at a time from its mailbox, so deposits can't interleave; no lock, no data race.
5. CSP channels reach the same place: a process owns the balance and receives from a channel; the sender waits for the receiver. Same idea, different plumbing.
6. But a withdrawal checked with one message and made with another still races: a race condition without a data race. Therefore the check and the action must be one message.
7. But processes that wait on each other still deadlock, without a single lock. Real Go code has more hanging bugs from message passing than from shared memory.
8. Therefore the answer: one owner per piece of state rules out data races by structure; in every model you still decide what happens as one step and keep waits from forming a cycle. Neither model is more powerful; use whichever makes the code simplest.

Deviation from the canonical progression: condition synchronization (producer-consumer) is left out; the research lists it as standard in textbooks but not needed to answer this question. The shared counter from OSTEP ch. 26 is used only as the measured evidence for the bank example.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1-3 | Narrated animation | Interleaving is order over time: two timelines of read, add, write, with the shared balance changing between them; a wait-for cycle closing. |
| 4-5 | Narrated animation | A mailbox draining one message at a time, and a rendezvous where the sender waits for the receiver: both are motion. |
| 6-7 | Narrated animation | The same timelines as chapter 2, one level up (messages instead of memory steps). |
| 8 | Narrated animation | Payoff: the table of what each model rules out and what it leaves. |
| (not built) | Hands-on exercise | "Play the scheduler": step two threads by hand to find the interleaving that loses a deposit, then run the Go programs from this lesson with the race detector and watch the deadlock hang. The research names doing as the way nondeterminism is believed; offered, not added, since the learner wants only the video on the page. |
| (not built) | Reading | The per-language guarantees (what Erlang, Akka, Go, Rust and Swift each enforce, and which are conventions). Reference detail with many qualifiers; better read than heard. |

## Ledgers

**Setups and payoffs.**
- The vanishing deposit (ch. 1) is explained in ch. 2, fixed with a lock in ch. 3 and with one owner in ch. 4.
- The three steps "read, add, write" (ch. 2) return as "which steps must happen as one" (ch. 3, 6, 8).
- The lock deadlock (ch. 3) returns without locks in ch. 7.
- Go's slogan (ch. 1) is answered in ch. 8, with Go's own advice.
- "Data race" vs "race condition" (ch. 2) pays off in ch. 6: a race condition with no data race.

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| race condition | ch. 2 | a bug where the result depends on the timing of concurrent steps |
| data race | ch. 2 | two threads access the same memory, at least one writing, with nothing forcing an order between them |
| lock | ch. 3 | something only one thread can hold at a time; others that want it wait |
| deadlock | ch. 3 | each of a group waits for something another holds, so none can go on |
| actor | ch. 4 | a part of a program with private state and a mailbox; handles one message at a time |
| mailbox | ch. 4 | the queue of messages waiting for an actor |
| channel | ch. 5 | a connection that processes send values into and receive them from |
| CSP | ch. 5 | communicating sequential processes: Hoare's model of processes that share nothing and communicate |

**Numbers to remember.** Three: the vanished deposit ($150 instead of $200); the shared counter ends millions short of twenty million; in real Go projects, most of the bugs that hang came from message passing (49 of 85).

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Two cash machines deposit into the same bank account at the same moment: fifty dollars each, into a balance of one hundred.
> The balance should end at two hundred. Sometimes it ends at one hundred and fifty. One deposit has vanished.
> A program that does several things at once has to coordinate them. There are two broad families of ways to do it; there are others, but these are the two you'll meet most.
> In one, threads share memory, and take turns with locks. In the other, nothing is shared, at least in the code you write: parts of the program pass messages instead.
> Go's documentation puts it as a slogan: "Do not communicate by sharing memory; instead, share memory by communicating."
> The hope is that if nothing is shared, bugs like the vanishing deposit can't happen. So does passing messages make them go away?

*Screen:* an account box "balance $100"; two cash machines A and B on either side, each sending "+$50". The balance flickers and lands on "$150" in coral, with "expected $200" beside it. Then two columns: "share memory: threads + locks" and "pass messages: actors, channels". The Go slogan in quotes, attributed to Effective Go. The question as a title card.

### 2. The lost update

> Here is how a deposit vanishes.
> A deposit takes three steps: read the balance, add fifty, write the result back.
> Machine A reads one hundred. Before A writes, machine B also reads one hundred.
> A writes one hundred and fifty. Then B writes one hundred and fifty, over A's result.
> A's deposit is gone. This is called a lost update.
> Only two orders of the six steps are safe: one machine's whole deposit finishes before the other's starts. In any other order, a deposit is lost. Usually the two deposits don't overlap at all, so the bug shows up only now and then.
> A bug whose result depends on the timing of concurrent steps is called a race condition.
> This bug is also what's called a data race. Two threads use the same memory. At least one of them writes. And nothing forces an order between them.
> The two names describe different things. "Race condition" is about the result. "Data race" is about how the memory is used. Here, both apply.
> A lost update is the mild outcome. For a program with a data race, C and C++ promise nothing at all, not even that a read returns a value some thread actually wrote.
> And when the steps do overlap often, it isn't rare. In a small C program, two threads each add one to a shared counter ten million times, so it should end at twenty million. In five runs on this machine, it ended between about ten point one and eleven point seven million, a different number each time.

*Screen:* two timelines, A above and B below, time running right; the shared balance in the middle. A: "read 100", "add 50 → 150", "write 150"; B: "read 100" slotted between A's read and write, then "write 150". The balance box shows 100, then 150, then 150 again; A's write is crossed out in coral: "lost update". A small tag on the timelines: "race condition". Then three checkmarks appear on the diagram as each condition is spoken: "same balance", "at least one writes", "no order", tagged "data race". Then the counter run: a line at 20,000,000 ("expected") and five bars that stop short of it, labelled 10.2 M, 10.3 M, 11.7 M, 11.0 M, 10.1 M (data/runs.txt). A two-column tag: "race condition: the result" | "data race: the memory".

### 3. Locks

> The shared-memory fix is a lock.
> A thread takes the lock before it reads the balance, and releases it after it writes. While one thread holds the lock, any other thread that wants it waits.
> So the three steps happen as one, with nothing in between. With a lock around it, the counter reaches twenty million on every run.
> But a lock only protects code that takes it. Nothing stops one forgotten code path from touching the balance without it, and then the race is back.
> Locks also bring a new failure. A transfer from account A to account B has to lock both accounts.
> Say each transfer locks the paying account first, then the receiving account.
> One thread transfers from A to B. It locks A, then waits for B. At the same moment, another thread transfers from B to A. It locks B, then waits for A.
> Each is waiting for a lock the other holds, and neither will let go. That's a deadlock.
> The standard fix is to take locks in one fixed order everywhere, say, the lower account number first. Then a cycle of waiting can't form.
> Running both transfers at once, a thousand times: the first version got stuck almost every time, the fixed order never.
> But every piece of code that takes these locks has to follow that order, including code someone else wrote.

*Screen:* the chapter 2 timelines with a lock icon: A takes the lock, B's read waits (a grey bar "waiting") until A releases; balance 100 → 150 → 200. "with a lock: 20,000,000 · 20,000,000 · 20,000,000". A dashed code path bypassing the lock, labelled "forgot the lock". Then two accounts, A and B, each with a lock; thread 1 holds A's lock and an arrow "waits for B"; thread 2 holds B's lock and an arrow "waits for A"; the two arrows close into a cycle, coral: "deadlock". Then the fix: both threads lock A first (lower number); the cycle can't close. Caption: "1,000 runs, both transfers at once (each does a little work between its two locks): stuck in 989 → 0 with a fixed order".

### 4. One owner

> A lock can be forgotten because every thread can still reach the balance. What if nothing else could reach it at all? Then there would be no lock to forget.
> That's where message passing starts. Give the balance a single owner, and let nothing else touch it.
> In the actor model, that owner is an actor: a part of the program with its own private state, and a mailbox.
> The cash machines never read the balance. They send the actor a message, "deposit fifty", and it goes into the mailbox.
> The actor takes one message at a time, and finishes it before starting the next.
> So the two deposits can't interleave. The actor adds the first fifty, then the second, and the balance ends at two hundred.
> There's no lock, and no data race on the balance, because only the actor ever touches it.
> Sending doesn't wait: a machine drops its message in the mailbox and carries on.
> How firmly "nothing else" holds depends on the system. In Erlang, processes don't share memory by default. A message is copied to the receiver. Shared tables exist, but a process has to opt in. In Akka, a toolkit for Java and Scala, keeping an actor's state private is up to the programmer.

*Screen:* the account becomes an actor: a circle with "balance $100" inside (private) and a mailbox slot; the chapter 3 "forgot the lock" path is shown hitting the circle's wall and stopping. Machines A and B send "deposit 50" envelopes into the mailbox; they queue; the actor takes one (balance 150), then the other (balance 200). Then two small labels under the actor: "Erlang: default" and "Akka: convention".

### 5. Channels

> But because an actor's send doesn't wait, a cash machine never learns when its request was taken. The mailbox has the deposit. Has the actor applied it yet, or is it still in the queue? The machine can't tell.
> The other message-passing family is built the opposite way: a send waits for a receiver.
> It comes from Tony Hoare's communicating sequential processes, or CSP, and Go's channels come out of this tradition.
> Processes share nothing, and talk over channels. A channel is a connection that processes send values into and receive them from.
> A Go channel made without a buffer, which is the default, makes a send wait until a receiver takes the value. So when a send finishes, the sender knows its value was taken.
> The account becomes a process that owns the balance, and receives deposits from a channel, one at a time. Again, no data race on the balance.
> Go also lets its goroutines, its lightweight threads, share memory. So in Go, one owner is a habit the programmer keeps, as in Akka.
> Actors and channels differ in the plumbing. An actor has an address and a mailbox, and sending doesn't wait. A channel is its own object, passed around between processes, and by default a send waits for the receiver.

*Screen:* the account as a process box "balance" with a channel (a pipe) entering it. Side by side with the chapter 4 actor: on the left, machine A drops an envelope in the mailbox and walks on; on the right, machine A's send stops (a "waiting" bar) until the account takes the value, then both move on together. Label: "Go: goroutines + channels". Then a side-by-side of two short labels: "actor: send, move on" and "channel: send waits".

### 6. A race without shared memory

> So it looks like the slogan wins: give each piece of state one owner, and the vanishing deposit can't happen. For deposits, that's true. Now try withdrawals.
> A machine should only pay out if there's enough money. With messages, that takes two: first "what's the balance?", then "withdraw one hundred".
> The balance is one hundred. Machine A asks, and hears one hundred. Machine B asks, and also hears one hundred.
> Both send "withdraw one hundred". The account handles them one at a time, just as promised, and the balance ends at minus one hundred.
> There's no data race here: only the account ever touched the balance. But the result still depended on timing. It's a race condition, between messages instead of between memory steps.
> In a test of a hundred thousand runs, the account was overdrawn in about seventeen hundred.
> The fix is to make the check and the withdrawal one message: "withdraw one hundred if the balance allows it". The owner does both in one step. In the same test, the account was never overdrawn.
> Locks raised the same question: which steps have to happen as one? Messages don't answer it for you.

*Screen:* the chapter 2 timelines again, one level up: A: "balance?" → "100"; B: "balance?" → "100"; A: "withdraw 100"; B: "withdraw 100"; the account's balance 100 → 0 → −100 in coral. Label: "no data race · still a race condition". Results: "check, then withdraw (two messages): overdrawn in 1,703 of 100,000 runs"; then one message "withdraw 100 if balance ≥ 100": "0 of 100,000".

### 7. Waiting in a circle

> Messages can deadlock too.
> Make each account its own process, with a channel. To transfer, an account sends "credit thirty" to the other account, and waits until the other account takes it.
> Start a transfer from A to B, and one from B to A, at the same moment. A is waiting for B to take its message. B is waiting for A to take its message. Neither is listening, because each is stuck in its own send.
> It's the lock deadlock again: a cycle of waiting, without a single lock. In a thousand runs, both accounts got stuck in about half.
> The fix follows the same rule as for locks: break the cycle. Here, the account hands the send to a helper, a separate goroutine that waits in its place. The account itself keeps listening, instead of waiting in the middle of a transfer. Now nothing inside the account is ever stuck in a send. In the same test, nothing got stuck.
> Sending to an actor never waits. But often an actor needs an answer, not just delivery. It sends a request, and then won't handle anything else until the reply lands in its mailbox. If two actors do that to each other at the same moment, each waits on the other forever.
> Real code shows the same pattern. A study of real concurrency bugs in six widely used Go projects sorted them two ways.
> Among the bugs that gave wrong results, message passing caused only about one in five. But among the bugs where code hung, it caused more than half.

*Screen:* two account processes A and B, each with an incoming channel. A's send arrow to B's channel, and B's send arrow to A's channel, both stalled halfway with "waiting" bars; the arrows close into the same cycle shape as chapter 3, coral: "deadlock, no locks". Caption: "1,000 runs: stuck in 482". Then the fix: each account's send moves to a small helper (a dotted box) while the account keeps listening; the cycle opens; "stuck in 0 of 1,000". Then two actors: each sends "request" (the envelope lands in the other's mailbox), then shows "waiting for reply"; the replies never come. Then the study (Tu et al., ASPLOS 2019; 171 bugs in Docker, Kubernetes, etcd, CockroachDB, gRPC, BoltDB): two stacked bars, "wrong results (86): shared memory 69, message passing 17" and "hangs (85): shared memory 36, message passing 49". Spoken ratios as labels: "17 of 86 ≈ 1 in 5", "49 of 85 > half".

### 8. The answer

> So does passing messages make the vanishing deposit go away? Yes. Give the balance one owner, and that bug can't happen.
> But its cousins remain: a check and an action split across two messages, and processes waiting on each other in a circle.
> So one owner per piece of state rules out data races on it: by the structure of the program, not by everyone remembering a lock. That holds wherever the language enforces the ownership. It's a real gain, and it's why the slogan exists.
> Two decisions are left in each of these models. You still choose which steps must happen as one: what a lock covers, or what one message does. And you still have to keep waits from forming a cycle.
> So neither model is simply the safe one. They differ in what each makes easy, and what each makes easy to forget.
> Even the Go documentation that gives the slogan adds that it can be taken too far. Go's advice is to use whichever is most expressive, or simplest, for the job: channels to hand work or data from one part of a program to another, and a lock to guard a piece of shared state.

*Screen:* the chapter 1 scene: two deposits into the actor, balance $200 in the pale-blue "correct" colour. Then a table, rows "data race", "race condition (check, then act)", "deadlock"; columns "threads + locks", "actors", "channels". Data race: "only if every access takes the lock" / "ruled out for the actor's own state, where enforced (Erlang); by convention in Akka" / "ruled out for the owner's state, by convention in Go". Race condition: "possible" in all three. Deadlock: "possible" in all three. Then the two decisions as two lines: "which steps happen as one", "no cycle of waits". End card with the takeaway and references: Butcher, Seven Concurrency Models in Seven Weeks (2014), ch. 2, 5, 6; Hoare, "Communicating Sequential Processes", CACM (1978); Hewitt, Bishop & Steiger, IJCAI (1973); Goetz et al., Java Concurrency in Practice (2006), ch. 2 and 10; Tu et al., "Understanding Real-World Concurrency Bugs in Go", ASPLOS (2019); Lauer & Needham, "On the Duality of Operating System Structures", Operating Systems Review (1979); Go wiki, "Use a sync.Mutex or a channel?".

## Evidence

| Claim | Source |
|---|---|
| Go's slogan, "Do not communicate by sharing memory; instead, share memory by communicating." | Effective Go, "Share by communicating" |
| A deposit or increment is read, add, write; interleavings lose updates (lost update) | OSTEP ch. 26 (counter trace table); MIT 6.031 Reading 19 (bank, cash machines); JCIP §2.2 read-modify-write |
| Race condition: correctness depends on timing or interleaving | JCIP §2.2.1; MIT 6.031 R19 |
| Two 3-step deposits have C(6,3) = 20 orderings; only the 2 where one finishes before the other starts keep both deposits | counted: a deposit is lost unless one write precedes the other read (OSTEP ch. 26 trace table shows one losing order) |
| A program with a data race has undefined behaviour in C and C++ | C11 §5.1.2.4; C++11 [intro.multithread]; Boehm & Adve, PLDI 2008 |
| Data race: two accesses to the same memory, at least one a write, not ordered by synchronization | Go memory model; Rustonomicon "Races"; Regehr, "Race Condition vs. Data Race" (2011) |
| Counter: 2 threads × 10,000,000 unlocked increments ended at 10,205,576 / 10,282,771 / 11,714,006 / 10,959,423 / 10,149,830; with a lock, 20,000,000 in 3 of 3 runs | sims/counter.c, data/runs.txt (gcc 13.3 -O2, 4 CPUs) |
| A lock protects only code that takes it; thread safety is a whole-program property | JCIP ch. 2-4 |
| Transfer locking from-account then to-account deadlocks when run in opposite directions; fixed lock order prevents it | JCIP §10.1.2 (transferMoney), OSTEP ch. 32; Coffman et al. (1971), circular wait |
| 1,000 runs of opposite transfers with a little work between the two locks: stuck in 989; with lower-number-first: 0 | sims/locks, data/runs.txt |
| Lock ordering must be followed by all code that takes the locks; not modular | MIT 6.031 R23; JCIP §10.1.3-10.1.4 (alien methods, open calls) |
| Actor: private state, mailbox, asynchronous sends, one message at a time | Hewitt, Bishop & Steiger (1973); Agha (1986); Butcher (2014) ch. 5 |
| Erlang processes share no memory by default and messages are copied; ETS tables are opt-in shared storage; Akka's private state is by convention | Armstrong thesis (2003); Akka docs ("Messages should be immutable"); Butcher ch. 5 |
| CSP: Hoare, 1978; processes share nothing and communicate; Go's channels come out of this tradition (via Newsqueak, Alef, Limbo); an unbuffered Go send waits for the receiver | Hoare, CACM 21(8), 1978; Go FAQ, "Why build concurrency on the ideas of CSP?"; Pike, "Go Concurrency Patterns" (2012); Go memory model, channel rules |
| Go also allows shared memory | Go memory model; `sync` package; Go wiki MutexOrChannel |
| Actor vs channel differences: identity/mailbox vs separate channel; asynchronous vs rendezvous | Wikipedia "Communicating sequential processes", comparison with the actor model; Butcher ch. 5-6 |
| Check-then-act over messages races; fix with a "withdraw if sufficient funds" operation | MIT 6.031 R19/R22 |
| Two messages: overdrawn in 1,703 of 100,000 runs; one message: 0 of 100,000 | sims/race, data/runs.txt (Go 1.24.7) |
| Channel deadlock between two account processes: stuck in 482 of 1,000 runs; with the send handed to a helper goroutine: 0 of 1,000 | sims/deadlock, data/runs.txt |
| Message-passing deadlocks are fixed by breaking the cycle of waits (e.g. not blocking on a send while others wait on you) | sims/deadlock; JCIP §10.1.4 (open calls: don't block on others while holding what they need); MIT 6.031 "Queues and Message-Passing" (deadlock with full queues) |
| Actors deadlock when they wait for replies (request/reply cycles) | Erlang gen_server:call docs; Orleans "Request scheduling"; Akka ask |
| Go study: 171 bugs, six projects; hanging (blocking) bugs 49 message passing vs 36 shared memory; non-blocking 17 vs 69 | Tu, Liu, Song & Zhang, ASPLOS 2019, Tables 6 and 9, Observation 3 (checked, research/verified_tu2019.md) |
| Neither model is inherently preferable; each can be built from the other | Lauer & Needham, Operating Systems Review 13(2), 1979 (presented 1978); Hoare 1978 §5.2 (semaphore as a process); Go runtime: `hchan` holds a `lock mutex` (runtime/chan.go, Go 1.24.7) |
| Go advice: "Use whichever is most expressive and/or most simple"; channels for passing ownership and distributing work, mutexes for caches and state; Effective Go: "This approach can be taken too far." | Go wiki, "Use a sync.Mutex or a channel?" |

## Review log

**Round 1:** expert PASS, editor REVISE, student retold the question and answer correctly (lost "a few times").
- Editor, blocking: the move from locks to message passing was announced, not derived. Chapter 4 now opens from chapter 3's weakness: a lock can be forgotten because every thread can still reach the balance; if nothing else could reach it, there would be no lock to forget.
- Editor: the ending now answers the opening's concrete question (the vanishing deposit can't happen with one owner) before naming the cousins that remain; the wrong intuition is voiced just before it breaks ("it looks like the slogan wins"); the Erlang/Akka line now does work (enforced vs convention), and Go's shared memory is tied to it; "first published in 1978" and the unused name "rendezvous" are cut; the study's project names left narration (kept on screen); the five eight-digit counter results became rounded bars; the chapter 2 captions no longer restate the narration (checkmarks on the diagram instead); the duality claim gets its own beat and picture; "the paying account first, then the receiving account".
- Expert: "Go, its best-known descendant" overstated the lineage (occam is the direct descendant; Go comes via Newsqueak, Alef, Limbo); now "Go's channels come out of this tradition". "Neither model can do anything the other can't" is now about expressiveness, followed by "that doesn't make them equally convenient". "Every model" is now "each of these models". A lost update is now called the mild outcome of a data race (C and C++ promise nothing). The counter range is "about ten point seven and thirteen million". Lauer & Needham cited as Operating Systems Review, 1979.
- Student: race condition and data race are now separated, and the data race's three conditions are three short sentences with a checkmark each; an actor waiting for a reply is now explained (sending never waits, but an actor that needs an answer waits for the reply in its mailbox); the study's denominators are spoken (86 wrong results, 85 hangs, 171 in all).
- Student question, not taken as a change: whether every data race is a race condition. Chapter 6 shows the two differ (a race condition with no data race); the full relationship (Regehr's 2×2) is reading, not narration.

**Round 2:** editor PASS, expert REVISE, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: Erlang processes "can't share variables at all" was false: ETS tables let processes share mutable state. Now "don't share memory by default … shared tables exist only for a process that opts in".
- Expert: "nothing is shared" is now "at least in the code you write" (chapter 8 shows a channel has a lock inside); "Go also lets goroutines share memory" (not threads); the duality is scoped to coordinating access to shared state; Go's advice quotes "most expressive, or simplest".
- Editor: channels are now introduced by the difference that motivates them (an actor's sender never knows when its message was taken; a channel send tells you); the channel deadlock now gets a tested fix like the lock deadlock (hand the send to a helper and keep listening: 0 of 1,000 stuck), which needed a rerun of every simulation, so all numbers in the script now come from the new data/runs.txt; the duality line now says what to do with it (what differs is what each makes easy, and easy to forget); the qualifier-stacked sentence is split; the study sentence says "forty-nine came from message passing: more than half".
- Student: the two race terms are now tied together (race condition is about the result, data race about how memory is used; here both apply); the actor-vs-channel "does sending wait" contrast is now shown side by side rather than stated in consecutive chapters only.
- Not taken: a fourth chapter-5 beat animating CSP further (the side-by-side send now carries it).

**Round 3:** editor PASS, expert REVISE, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: "most orders of the six steps are fine" was backwards: of the 20 orderings, only the 2 where one deposit finishes before the other starts are safe. Now said so, with the reason the bug is still intermittent (the deposits usually don't overlap). The data-race checkmark now reads "at least one writes", matching the definition.
- Expert: channel sends wait only on an unbuffered channel (the default); now spoken, with what a buffer changes. The chapter 8 table's "ruled out" is hedged (enforced in Erlang; convention in Akka and Go). "Two broad families … there are others". Not taken: running the locked counter five times (it would change every other number; the screen says 3 runs).
- Editor: channels are introduced by what actors leave open (a sender never learns when its request was taken); the hand-off fix says why it works; the duality aside is cut from the ending, which now lands on "neither model is simply the safe one"; the study is spoken as ratios (about one in five; more than half), with counts on screen; "goroutines" is glossed; the Erlang sentence is split.
- Student: "promise nothing" now says what it means (not even that a read returns a value some thread wrote); the counter test is named as a small C program; "unbuffered" is spoken and explained.

**Round 4:** editor PASS, expert REVISE, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: goroutines were glossed as "lightweight processes", contradicting the script's own use of "process" (shares nothing) and Go's docs ("a lightweight thread managed by the Go runtime"). Now "lightweight threads". The closing actor-vs-channel line now says "by default a send waits".
- Editor: the buffered-channel aside is cut (never used again; "made without a buffer, which is the default" keeps the precision); an actor waiting for a reply now says it won't handle anything else until the reply lands; the Go advice now follows from the slogan (Effective Go itself says it "can be taken too far"), and "like a cache" is gone.
- Editor, not taken: motivating channels as "actors guarantee delivery, not confirmation" (actor delivery isn't guaranteed in Erlang or Akka, so the sentence would be wrong); cutting the Go advice entirely (it answers the chapter 1 slogan with its own source's caveat).
- Student: the channel-deadlock fix now says what the helper is (a separate goroutine that waits in the account's place).

**Round 5:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). The gate is passed; the should-fix items are applied once, and round 6 decides the lock.
- Expert: Akka is "a toolkit", not a library.
- Editor: the misconception is now said aloud before the question ("the hope is that if nothing is shared…"); the channel motivation now has a concrete gap (the mailbox has the deposit; has the actor applied it yet?); a bridge into the bug study ("real code shows the same pattern"); the helper sentence is split; captions that restated the narration are trimmed to terms; the "(ICE)" colour shorthand is spelled out.
- Editor, not taken: cutting the C/C++ "promise nothing" line (the expert asked for the data race's worst case in round 1, and the next line's counter program is in C); cutting "there are others" (the expert asked for that scope in round 3); changing the withdrawal to a different amount so "one hundred" isn't repeated (the simulation and its numbers are built on $100 against $100, and the screen shows which is which).

**Round 6 (final):** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). Locked.
- Applied after lock, screen only: the chapter 5 tag "channel: rendezvous" named a term the narration no longer uses; now "channel: send waits" (and "actor: send, move on").
- Logged as revision candidates for the learner's notes, not applied, per the stopping rule:
  - Expert: CSP attribution could be tighter (Hoare's 1978 processes named each other; channels came with the 1985 book and occam).
  - Editor: Go's "channels for handing data, a lock for guarding state" split arrives only in the last line; the actor request/reply deadlock is the one claim without a measured run; chapter 2's move from "machine" to "thread" has no bridge.
  - Student: lost at the race-condition/data-race distinction, the "six steps" count, and "buffer"/"promise nothing".
