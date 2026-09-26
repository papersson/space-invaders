# Share Memory, or Pass Messages?

Status: in review round 2

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
> A program that does several things at once has to coordinate them, and there are two broad ways to do it.
> In one, threads share memory, and take turns with locks. In the other, nothing is shared: parts of the program pass messages instead.
> Go's documentation puts it as a slogan: "Do not communicate by sharing memory; instead, share memory by communicating."
> So does passing messages make bugs like the vanishing deposit go away?

*Screen:* an account box "balance $100"; two cash machines A and B on either side, each sending "+$50". The balance flickers and lands on "$150" in coral, with "expected $200" beside it. Then two columns: "share memory: threads + locks" and "pass messages: actors, channels". The Go slogan in quotes, attributed to Effective Go. The question as a title card.

### 2. The lost update

> Here is how a deposit vanishes.
> A deposit takes three steps: read the balance, add fifty, write the result back.
> Machine A reads one hundred. Before A writes, machine B also reads one hundred.
> A writes one hundred and fifty. Then B writes one hundred and fifty, over A's result.
> A's deposit is gone. This is called a lost update.
> Most orders of the six steps are fine. Only some lose a deposit. A bug whose result depends on the timing of concurrent steps is called a race condition.
> This bug is also what's called a data race. Two threads use the same memory. At least one of them writes. And nothing forces an order between them.
> A lost update is the mild outcome. For a program with a data race, languages like C and C++ promise nothing at all about what happens.
> And it isn't rare. Two threads each add one to a shared counter ten million times, so it should end at twenty million. In five runs on this machine, it ended between about ten point seven and thirteen million, a different number each time.

*Screen:* two timelines, A above and B below, time running right; the shared balance in the middle. A: "read 100", "add 50 → 150", "write 150"; B: "read 100" slotted between A's read and write, then "write 150". The balance box shows 100, then 150, then 150 again; A's write is crossed out in coral: "lost update". A small tag on the timelines: "race condition". Then three checkmarks appear on the diagram as each condition is spoken: "same balance", "both write", "no order", tagged "data race". Then the counter run: a line at 20,000,000 ("expected") and five bars that stop short of it, labelled 11.9 M, 10.9 M, 10.7 M, 10.8 M, 13.0 M (data/runs.txt).

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

*Screen:* the chapter 2 timelines with a lock icon: A takes the lock, B's read waits (a grey bar "waiting") until A releases; balance 100 → 150 → 200. "with a lock: 20,000,000 · 20,000,000 · 20,000,000". A dashed code path bypassing the lock, labelled "forgot the lock". Then two accounts, A and B, each with a lock; thread 1 holds A's lock and an arrow "waits for B"; thread 2 holds B's lock and an arrow "waits for A"; the two arrows close into a cycle, coral: "deadlock". Then the fix: both threads lock A first (lower number); the cycle can't close. Caption: "1,000 runs, both transfers at once (each does a little work between its two locks): stuck in 992 → 0 with a fixed order".

### 4. One owner

> A lock can be forgotten because every thread can still reach the balance. What if nothing else could reach it at all? Then there would be no lock to forget.
> That's where message passing starts. Give the balance a single owner, and let nothing else touch it.
> In the actor model, that owner is an actor: a part of the program with its own private state, and a mailbox.
> The cash machines never read the balance. They send the actor a message, "deposit fifty", and it goes into the mailbox.
> The actor takes one message at a time, and finishes it before starting the next.
> So the two deposits can't interleave. The actor adds the first fifty, then the second, and the balance ends at two hundred.
> There's no lock, and no data race on the balance, because only the actor ever touches it.
> Sending doesn't wait: a machine drops its message in the mailbox and carries on.
> How firmly "nothing else" holds depends on the system. In Erlang, processes can't share variables at all: a message is copied to the receiver. In Akka, a library for Java and Scala, keeping an actor's state private is up to the programmer.

*Screen:* the account becomes an actor: a circle with "balance $100" inside (private) and a mailbox slot; the chapter 3 "forgot the lock" path is shown hitting the circle's wall and stopping. Machines A and B send "deposit 50" envelopes into the mailbox; they queue; the actor takes one (balance 150), then the other (balance 200). Then two small labels under the actor: "Erlang: enforced (messages are copied)" and "Akka: by convention".

### 5. Channels

> The other message-passing family comes from Tony Hoare's communicating sequential processes, or CSP. Go's channels come out of this tradition.
> Processes share nothing, and talk over channels. A channel is a connection that processes send values into and receive them from.
> By default, a send on a Go channel waits until a receiver takes the value.
> The account becomes a process that owns the balance, and receives deposits from a channel, one at a time. Again, no data race on the balance.
> Go also lets threads share memory, so there, one owner is a habit the programmer keeps, as in Akka.
> Actors and channels differ in the plumbing. An actor has an address and a mailbox, and sending doesn't wait. A channel is its own object, passed around between processes, and a send waits for the receiver.

*Screen:* the account as a process box "balance" with a channel (a pipe) entering it. Machine A's send: A stops (a "waiting" bar) until the account takes the value; then both move on together. Label: "Go: goroutines + channels". Then a side-by-side: "actor: address + mailbox, send doesn't wait" vs "channel: a separate object, send waits for the receiver (unbuffered)".

### 6. A race without shared memory

> So it looks like the slogan wins: give each piece of state one owner, and the vanishing deposit can't happen. For deposits, that's true. Now try withdrawals.
> A machine should only pay out if there's enough money. With messages, that takes two: first "what's the balance?", then "withdraw one hundred".
> The balance is one hundred. Machine A asks, and hears one hundred. Machine B asks, and also hears one hundred.
> Both send "withdraw one hundred". The account handles them one at a time, just as promised, and the balance ends at minus one hundred.
> There's no data race here: only the account ever touched the balance. But the result still depended on timing. It's a race condition, between messages instead of between memory steps.
> In a test of a hundred thousand runs, the account was overdrawn in about seventeen hundred.
> The fix is to make the check and the withdrawal one message: "withdraw one hundred if the balance allows it". The owner does both in one step. In the same test, the account was never overdrawn.
> It's the question the lock raised, in another form: which steps have to happen as one? Messages don't answer it for you.

*Screen:* the chapter 2 timelines again, one level up: A: "balance?" → "100"; B: "balance?" → "100"; A: "withdraw 100"; B: "withdraw 100"; the account's balance 100 → 0 → −100 in coral. Label: "no data race · still a race condition". Results: "check, then withdraw (two messages): overdrawn in 1,683 of 100,000 runs"; then one message "withdraw 100 if balance ≥ 100": "0 of 100,000".

### 7. Waiting in a circle

> Messages can deadlock too.
> Make each account its own process, with a channel. To transfer, an account sends "credit thirty" to the other account, and waits until the other account takes it.
> Start a transfer from A to B, and one from B to A, at the same moment. A is waiting for B to take its message. B is waiting for A to take its message. Neither is listening, because each is stuck in its own send.
> It's the lock deadlock again: a cycle of waiting, without a single lock. In a thousand runs, both accounts got stuck in about half.
> Sending to an actor never waits. But often an actor needs an answer. It sends a request, then waits for the reply to arrive in its mailbox. If two actors do that to each other at the same moment, both wait forever.
> A study of a hundred and seventy-one real concurrency bugs in six large Go projects sorted them two ways. Of the eighty-six bugs that gave wrong results, only seventeen came from message passing. Of the eighty-five where code hung, forty-nine did.

*Screen:* two account processes A and B, each with an incoming channel. A's send arrow to B's channel, and B's send arrow to A's channel, both stalled halfway with "waiting" bars; the arrows close into the same cycle shape as chapter 3, coral: "deadlock, no locks". Caption: "1,000 runs: stuck in 497". Then two actors: each sends "request" (the envelope lands in the other's mailbox), then shows "waiting for reply"; the replies never come. Then the study (Tu et al., ASPLOS 2019; 171 bugs in Docker, Kubernetes, etcd, CockroachDB, gRPC, BoltDB): two stacked bars, "wrong results (86): shared memory 69, message passing 17" and "hangs (85): shared memory 36, message passing 49".

### 8. The answer

> So does passing messages make the vanishing deposit go away? Yes. Give the balance one owner, and that bug can't happen.
> But its cousins remain: a check and an action split across two messages, and processes waiting on each other in a circle.
> So one owner per piece of state rules out data races on it, by the structure of the program instead of everyone remembering a lock, at least where the language enforces it. That's a real gain, and it's why the slogan exists.
> Two decisions are left in each of these models. You still choose which steps must happen as one: what a lock covers, or what one message does. And you still have to keep waits from forming a cycle.
> Neither model can express anything the other can't. A lock can be built as a process: send it "may I?", wait for "yes", and send "done" when finished. And a Go channel is built with a lock inside.
> That doesn't make them equally convenient. Go's own advice is to use whichever makes the code simplest: channels to hand work or data from one part of a program to another, and a lock to guard shared state, like a cache.

*Screen:* the chapter 1 scene: two deposits into the actor, balance $200 (ICE). Then a table, rows "data race", "race condition (check, then act)", "deadlock"; columns "threads + locks", "actors", "channels". Data race: "only if every access takes the lock" / "ruled out for the actor's own state" / "ruled out for the owner's state". Race condition: "possible" in all three. Deadlock: "possible" in all three. Then the two decisions as two lines: "which steps happen as one", "no cycle of waits". Then the duality: a lock drawn as a process with "may I?" → "yes" → "done" messages; a channel drawn as a box opened to show a lock inside. End card with the takeaway and references: Butcher, Seven Concurrency Models in Seven Weeks (2014), ch. 2, 5, 6; Hoare, "Communicating Sequential Processes", CACM (1978); Hewitt, Bishop & Steiger, IJCAI (1973); Goetz et al., Java Concurrency in Practice (2006), ch. 2 and 10; Tu et al., "Understanding Real-World Concurrency Bugs in Go", ASPLOS (2019); Lauer & Needham, "On the Duality of Operating System Structures", Operating Systems Review (1979); Go wiki, "Use a sync.Mutex or a channel?".

## Evidence

| Claim | Source |
|---|---|
| Go's slogan, "Do not communicate by sharing memory; instead, share memory by communicating." | Effective Go, "Share by communicating" |
| A deposit or increment is read, add, write; interleavings lose updates (lost update) | OSTEP ch. 26 (counter trace table); MIT 6.031 Reading 19 (bank, cash machines); JCIP §2.2 read-modify-write |
| Race condition: correctness depends on timing or interleaving | JCIP §2.2.1; MIT 6.031 R19 |
| A program with a data race has undefined behaviour in C and C++ | C11 §5.1.2.4; C++11 [intro.multithread]; Boehm & Adve, PLDI 2008 |
| Data race: two accesses to the same memory, at least one a write, not ordered by synchronization | Go memory model; Rustonomicon "Races"; Regehr, "Race Condition vs. Data Race" (2011) |
| Counter: 2 threads × 10,000,000 unlocked increments ended at 11,856,624 / 10,850,072 / 10,662,642 / 10,780,763 / 12,988,652; with a lock, 20,000,000 in 3 of 3 runs | sims/counter.c, data/runs.txt (gcc 13.3 -O2, 4 CPUs) |
| A lock protects only code that takes it; thread safety is a whole-program property | JCIP ch. 2-4 |
| Transfer locking from-account then to-account deadlocks when run in opposite directions; fixed lock order prevents it | JCIP §10.1.2 (transferMoney), OSTEP ch. 32; Coffman et al. (1971), circular wait |
| 1,000 runs of opposite transfers with a little work between the two locks: stuck in 992; with lower-number-first: 0 | sims/locks, data/runs.txt |
| Lock ordering must be followed by all code that takes the locks; not modular | MIT 6.031 R23; JCIP §10.1.3-10.1.4 (alien methods, open calls) |
| Actor: private state, mailbox, asynchronous sends, one message at a time | Hewitt, Bishop & Steiger (1973); Agha (1986); Butcher (2014) ch. 5 |
| Erlang processes share no variables and messages are copied; Akka's private state is by convention | Armstrong thesis (2003); Akka docs ("Messages should be immutable"); Butcher ch. 5 |
| CSP: Hoare, 1978; processes share nothing and communicate; Go's channels come out of this tradition (via Newsqueak, Alef, Limbo); an unbuffered Go send waits for the receiver | Hoare, CACM 21(8), 1978; Go FAQ, "Why build concurrency on the ideas of CSP?"; Pike, "Go Concurrency Patterns" (2012); Go memory model, channel rules |
| Go also allows shared memory | Go memory model; `sync` package; Go wiki MutexOrChannel |
| Actor vs channel differences: identity/mailbox vs separate channel; asynchronous vs rendezvous | Wikipedia "Communicating sequential processes", comparison with the actor model; Butcher ch. 5-6 |
| Check-then-act over messages races; fix with a "withdraw if sufficient funds" operation | MIT 6.031 R19/R22 |
| Two messages: overdrawn in 1,683 of 100,000 runs; one message: 0 of 100,000 | sims/race, data/runs.txt (Go 1.24.7) |
| Channel deadlock between two account processes: stuck in 497 of 1,000 runs | sims/deadlock, data/runs.txt |
| Actors deadlock when they wait for replies (request/reply cycles) | Erlang gen_server:call docs; Orleans "Request scheduling"; Akka ask |
| Go study: 171 bugs, six projects; hanging (blocking) bugs 49 message passing vs 36 shared memory; non-blocking 17 vs 69 | Tu, Liu, Song & Zhang, ASPLOS 2019, Tables 6 and 9, Observation 3 (checked, research/verified_tu2019.md) |
| Neither model is inherently preferable; each can be built from the other | Lauer & Needham, Operating Systems Review 13(2), 1979 (presented 1978); Hoare 1978 §5.2 (semaphore as a process); Go runtime: `hchan` holds a `lock mutex` (runtime/chan.go, Go 1.24.7) |
| Go advice: use whichever is most expressive and/or simplest; channels for passing ownership and distributing work, mutexes for caches and state | Go wiki, "Use a sync.Mutex or a channel?" |

## Review log

**Round 1:** expert PASS, editor REVISE, student retold the question and answer correctly (lost "a few times").
- Editor, blocking: the move from locks to message passing was announced, not derived. Chapter 4 now opens from chapter 3's weakness: a lock can be forgotten because every thread can still reach the balance; if nothing else could reach it, there would be no lock to forget.
- Editor: the ending now answers the opening's concrete question (the vanishing deposit can't happen with one owner) before naming the cousins that remain; the wrong intuition is voiced just before it breaks ("it looks like the slogan wins"); the Erlang/Akka line now does work (enforced vs convention), and Go's shared memory is tied to it; "first published in 1978" and the unused name "rendezvous" are cut; the study's project names left narration (kept on screen); the five eight-digit counter results became rounded bars; the chapter 2 captions no longer restate the narration (checkmarks on the diagram instead); the duality claim gets its own beat and picture; "the paying account first, then the receiving account".
- Expert: "Go, its best-known descendant" overstated the lineage (occam is the direct descendant; Go comes via Newsqueak, Alef, Limbo); now "Go's channels come out of this tradition". "Neither model can do anything the other can't" is now about expressiveness, followed by "that doesn't make them equally convenient". "Every model" is now "each of these models". A lost update is now called the mild outcome of a data race (C and C++ promise nothing). The counter range is "about ten point seven and thirteen million". Lauer & Needham cited as Operating Systems Review, 1979.
- Student: race condition and data race are now separated, and the data race's three conditions are three short sentences with a checkmark each; an actor waiting for a reply is now explained (sending never waits, but an actor that needs an answer waits for the reply in its mailbox); the study's denominators are spoken (86 wrong results, 85 hangs, 171 in all).
- Student question, not taken as a change: whether every data race is a race condition. Chapter 6 shows the two differ (a race condition with no data race); the full relationship (Regehr's 2×2) is reading, not narration.
