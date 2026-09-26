Playing the role: here's my pass through the script as that industry-engineer viewer, in order.

## 1. Where I'd lose the thread

- **"This bug is also what's called a data race."** — I just got "race condition" defined a few seconds earlier, and now a second term lands immediately after with its own three-part checklist (same memory, one writer, no order). I can't tell if a data race *is* a race condition, a special case of one, or a separate thing that happens to look similar. Nothing ties the two words together explicitly.
- **"By default, a send on a Go channel waits until a receiver takes the value."** — This directly follows the actor section's "**Sending doesn't wait**: a machine drops its message in the mailbox and carries on." Two message-passing models, introduced back to back, with opposite behavior on the exact same point (does sending block?). I'd have to rewind to be sure which one I'm looking at.
- **"Of the eighty-six bugs that gave wrong results, only seventeen came from message passing. Of the eighty-five where code hung, forty-nine did."** — Four numbers (171, 86/17, 85/49) in two breaths, right after the 171 was mentioned. Without staring at the bar chart I lose which count is "out of" which.
- **"A lock can be built as a process: send it 'may I?'... And a Go channel is built with a lock inside."** — This is asserting the two models are equivalent under the hood, but it's said as a throwaway line. I don't know what to *do* with that fact — does it mean my earlier takeaway (messages avoid the lock-forgetting problem) is undercut?
- Milder one: **"It's the question the lock raised, in another form: which steps have to happen as one?"** — leans on me remembering a specific framing from two chapters back; I caught it, but only just.

## 2. Questions I'd ask afterward

- Is every data race a race condition, or are these just two separate labels for overlapping situations?
- If a Go channel send blocks until received, how is that actually less risky than a lock in practice — isn't blocking-until-someone-acts basically the same shape of risk?
- Why did message-passing code have *fewer* wrong-result bugs but *more* hangs in that study — is that inherent to the model, or just that Go programmers lean on channels for things locks wouldn't even be used for?
- Is there a rule of thumb for deciding what has to be "one message" (like the withdrawal check) versus when splitting across messages is safe?
- The lock-as-process / channel-with-a-lock-inside equivalence — does that mean the choice between them is basically just style, with no correctness difference?

## 3. What I learned (~150 words, not looking back)

Concurrent programs coordinating shared state can lose updates — two ATMs each deposit $50 into a $100 balance, but timing makes it read-add-write in an interleaved way so one deposit disappears, ending at $150 instead of $200. This is a race condition, and when it's caused by unsynchronized shared memory it's called a data race. Locks fix it by making the three steps atomic, but locks can be forgotten, and locking multiple things in inconsistent order causes deadlock (two transfers each holding one lock, waiting on the other). The alternative is message passing — actors or channels — giving each piece of state a single owner so nothing else touches it directly, which does eliminate data races. But it doesn't eliminate everything: splitting a check-then-act (like "check balance, then withdraw") across two messages reintroduces the same race in a new form, and processes can still deadlock waiting on each other in a circle.

## 4. Direct answers

- **One main idea:** Giving a piece of state a single owner (message passing) structurally rules out data races on it, but it doesn't rule out race conditions (multi-step operations split across messages) or deadlocks (cyclic waiting) — those require the same discipline as with locks, just applied differently.
- **Numbers I remember:** $100 balance + two $50 deposits → should be $200, sometimes landed at $150. A counter test expected 20,000,000 but landed around 10.7–13 million without a lock, and hit 20,000,000 every time with one. A deadlock test got stuck ~992 out of 1,000 runs with inconsistent lock order, 0 out of 1,000 with a fixed order. A two-message withdrawal check was overdrawn roughly 1,700 times out of 100,000; a single combined message brought that to 0. A bug study of 171 real Go bugs split wrong-results (86, of which 17 message-passing) vs hangs (85, of which 49 message-passing).
- **Starting question / answer:** "Does passing messages make bugs like the vanishing deposit go away?" Answer: yes, for that specific bug (data races) — but its relatives, race conditions and deadlocks, remain, just in message form instead of memory form.

## 5. Ratings

- **Want-to-know-the-answer at the open:** 4/5 — the vanishing-$50 scenario is concrete and relatable, and framing it as "which of two whole programming philosophies actually fixes this" is a strong hook.
- **How often I felt lost:** a few times — mainly the data-race-vs-race-condition naming, the actor-vs-channel "does sending wait" flip, and the dense bug-count sentence near the end.
