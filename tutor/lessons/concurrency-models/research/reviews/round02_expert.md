Reviewed against the evidence table and canonical sources (Hewitt et al., Hoare, Lauer & Needham, JCIP, Tu et al. 2019, Go docs/wiki, Erlang/OTP). Arithmetic and the sim/study numbers all check out (counter totals, 992/0, 1683/0, 497/1000, 86/85=171). Findings below.

---

**BLOCKING**

> "In Erlang, processes can't share variables at all: a message is copied to the receiver."

This is categorically false as stated, and it's exactly the kind of claim an Erlang course would immediately correct: ETS tables (and, less commonly, Mnesia and `persistent_term`) are a standard, heavily used mechanism for processes to share *mutable* state without going through message copying — this isn't an obscure corner case, it's core OTP material. Ordinary process-local data isn't shared, but "can't … at all" overclaims. (There's a second-order nuance too: binaries over 64 bytes are refcounted off-heap and shared by reference rather than copied, though immutability keeps the no-shared-*mutable*-state property intact for that case.)

Corrected wording: *"In Erlang, processes don't share memory by default — a message is copied to the receiver — though a process can opt into shared mutable storage via ETS tables."*

---

**SHOULD FIX**

> "In one, threads share memory, and take turns with locks. In the other, nothing is shared: parts of the program pass messages instead."

This sets up a clean dichotomy that the script itself later undercuts: chapter 8 says "a Go channel is built with a lock inside," i.e. message passing is commonly implemented *with* shared memory under the hood. The claim is true at the level of what the programmer touches, not literally. Scope it now to avoid the later line reading as a contradiction.

Corrected wording: *"...nothing is shared at the level the programmer writes: parts of the program pass messages instead."*

> "Go also lets threads share memory, so there, one owner is a habit the programmer keeps, as in Akka."

Wrong noun for Go specifically. Go's own documentation is insistent that goroutines are not OS threads (M:N multiplexed by the runtime scheduler), and the script gets this right everywhere else, including the caption directly above this line ("Go: goroutines + channels"). Using "threads" here is a drafting inconsistency, not a deliberate simplification.

Corrected wording: *"Go also lets goroutines share memory, so there, one owner is a habit the programmer keeps, as in Akka."*

> "Neither model can express anything the other can't."

Overstates the Lauer–Needham duality result. That paper's duality is specifically about equivalent ways to structure synchronization/coordination (monitors/procedure calls vs. message-passing kernels) on a single machine — it is not a claim that locks and actors are interchangeable for everything actor systems are actually used for in practice, e.g. location-transparent distribution or fault isolation via supervision trees (Erlang/Akka), which a local lock has no analogue for. As written, a viewer could reasonably take this as "there's no practical reason to prefer one," which the video's own earlier material (Erlang enforcement, Akka's ask-deadlock discussion) doesn't support.

Corrected wording: *"Neither model can coordinate access to shared state in a way the other can't"* (or add "for the patterns here" to scope it to the lock/deadlock/data-race discussion just given).

---

**NIT**

- Go wiki paraphrase "Go's own advice is to use whichever makes the code simplest" drops the wiki's actual "most expressive and/or most simple" — minor, doesn't change the point, but if precision matters here too, consider restoring "expressive."

---

VERDICT: REVISE
