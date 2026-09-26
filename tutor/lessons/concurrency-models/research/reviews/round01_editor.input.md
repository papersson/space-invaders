You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

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
> This one has a more specific name. Two threads use the same memory, at least one of them writes, and nothing forces an order between them. That's a data race.
> It isn't rare. Two threads each add one to a shared counter ten million times, so it should end at twenty million. In five runs on this machine it ended between ten and thirteen million, a different number each time.

*Screen:* two timelines, A above and B below, time running right; the shared balance in the middle. A: "read 100", "add 50 → 150", "write 150"; B: "read 100" slotted between A's read and write, then "write 150". The balance box shows 100, then 150, then 150 again; A's write is crossed out in coral: "lost update". Caption as defined: "race condition: the result depends on timing" then, separately, "data race: same memory, one writes, no order". Then the counter run: "2 threads × 10,000,000 increments (expected 20,000,000)" and the five results from data/runs.txt: 11,856,624 · 10,850,072 · 10,662,642 · 10,780,763 · 12,988,652.

### 3. Locks

> The shared-memory fix is a lock.
> A thread takes the lock before it reads the balance, and releases it after it writes. While one thread holds the lock, any other thread that wants it waits.
> So the three steps happen as one, with nothing in between. With a lock around it, the counter reaches twenty million on every run.
> But a lock only protects code that takes it. Nothing stops one forgotten code path from touching the balance without it, and then the race is back.
> Locks also bring a new failure. A transfer from account A to account B has to lock both accounts.
> Say each transfer locks the account it pays from, then the one it pays into.
> One thread transfers from A to B. It locks A, then waits for B. At the same moment, another thread transfers from B to A. It locks B, then waits for A.
> Each is waiting for a lock the other holds, and neither will let go. That's a deadlock.
> The standard fix is to take locks in one fixed order everywhere, say, the lower account number first. Then a cycle of waiting can't form.
> Running both transfers at once, a thousand times: the first version got stuck almost every time, the fixed order never.
> But every piece of code that takes these locks has to follow that order, including code someone else wrote.

*Screen:* the chapter 2 timelines with a lock icon: A takes the lock, B's read waits (a grey bar "waiting") until A releases; balance 100 → 150 → 200. "with a lock: 20,000,000 · 20,000,000 · 20,000,000". A dashed code path bypassing the lock, labelled "forgot the lock". Then two accounts, A and B, each with a lock; thread 1 holds A's lock and an arrow "waits for B"; thread 2 holds B's lock and an arrow "waits for A"; the two arrows close into a cycle, coral: "deadlock". Then the fix: both threads lock A first (lower number); the cycle can't close. Caption: "1,000 runs, both transfers at once (each does a little work between its two locks): stuck in 992 → 0 with a fixed order".

### 4. One owner

> Message passing starts from a different idea. Give the balance a single owner, and let nothing else touch it.
> In the actor model, that owner is an actor: a part of the program with its own private state, and a mailbox.
> The cash machines never read the balance. They send the actor a message, "deposit fifty", and it goes into the mailbox.
> The actor takes one message at a time, and finishes it before starting the next.
> So the two deposits can't interleave. The actor adds the first fifty, then the second, and the balance ends at two hundred.
> There's no lock, and no data race on the balance, because only the actor ever touches it.
> Sending doesn't wait: a machine drops its message in the mailbox and carries on.
> Erlang and Akka are built on actors.

*Screen:* the account becomes an actor: a circle with "balance $100" inside (private) and a mailbox slot. Machines A and B send "deposit 50" envelopes into the mailbox; they queue; the actor takes one (balance 150), then the other (balance 200). A note: "Erlang: processes share no variables; messages are copied. Akka: private state by convention."

### 5. Channels

> The other message-passing family comes from Tony Hoare's communicating sequential processes, or CSP, first published in 1978.
> Here too, processes share nothing. Go, its best-known descendant, has them talk over channels. A channel is a connection that processes send values into and receive them from.
> By default, a send on a Go channel waits until a receiver takes the value. Sender and receiver meet, and the value changes hands. This is called a rendezvous.
> The account becomes a process that owns the balance, and receives deposits from a channel, one at a time. Again, no data race on the balance.
> So actors and channels share the key idea: one owner for each piece of state. They differ in the plumbing. An actor has an address and a mailbox, and sending doesn't wait. A channel is its own object, passed around between processes, and a send waits for the receiver.

*Screen:* the account as a process box "balance" with a channel (a pipe) entering it. Machine A's send: A stops (a "waiting" bar) until the account takes the value; then both move on together ("rendezvous"). Label: "Go: goroutines + channels (Go also allows shared memory)". Then a side-by-side: "actor: address + mailbox, send doesn't wait" vs "channel: a separate object, send waits for the receiver (unbuffered)".

### 6. A race without shared memory

> So is the vanishing money solved? For deposits, yes. Now try withdrawals.
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
> Actors don't block on a send. But as soon as an actor sends a request and waits for the reply, two actors asking each other can wait forever in the same way.
> A study of real bugs in six large Go projects, Docker and Kubernetes among them, found message passing behind far fewer of the bugs that give wrong results. But it was behind more of the bugs where code hangs: forty-nine of eighty-five.

*Screen:* two account processes A and B, each with an incoming channel. A's send arrow to B's channel, and B's send arrow to A's channel, both stalled halfway with "waiting" bars; the arrows close into the same cycle shape as chapter 3, coral: "deadlock, no locks". Caption: "1,000 runs: stuck in 497". Then two actors with "ask" arrows each waiting for a reply. Then the study (Tu et al., ASPLOS 2019, 171 bugs in Docker, Kubernetes, etcd, CockroachDB, gRPC, BoltDB): two bars per kind, "wrong results: shared memory 69, message passing 17" and "hangs: shared memory 36, message passing 49".

### 8. The answer

> So does passing messages make the bugs go away? Some of them.
> Giving each piece of state one owner rules out data races on it, by the structure of the program, not by everyone remembering a lock. That's a real gain, and it's why the slogan exists.
> Two decisions are left in every model. You still choose which steps must happen as one: what a lock covers, or what one message does. And you still have to keep waits from forming a cycle.
> Neither model can do anything the other can't. A lock can be written as a process that hands out permission, and channels are built with locks inside.
> Go's own advice is to use whichever makes the code simplest: channels to hand work or data from one part of a program to another, and a lock to guard shared state, like a cache.

*Screen:* a table, rows "data race", "race condition (check, then act)", "deadlock"; columns "threads + locks", "actors", "channels". Data race: "only if every access takes the lock" / "ruled out for the actor's own state" / "ruled out for the owner's state". Race condition: "allowed" in all three. Deadlock: "allowed" in all three. Then the two decisions as two lines: "which steps happen as one", "no cycle of waits". End card with the takeaway and references: Butcher, Seven Concurrency Models in Seven Weeks (2014), ch. 2, 5, 6; Hoare, "Communicating Sequential Processes", CACM (1978); Hewitt, Bishop & Steiger, IJCAI (1973); Goetz et al., Java Concurrency in Practice (2006), ch. 2 and 10; Tu et al., "Understanding Real-World Concurrency Bugs in Go", ASPLOS (2019); Lauer & Needham, "On the Duality of Operating System Structures" (1978); Go wiki, "Use a sync.Mutex or a channel?".

