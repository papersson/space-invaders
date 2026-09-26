# Review

I went through the script claim-by-claim against the evidence table and canonical sources (JCIP, the Go memory model, Hoare 1978, Lauer & Needham, Tu et al. 2019). The arithmetic all checks out exactly against `data/runs.txt`, and the core technical content (data race vs. race condition, lost update, lock ordering/deadlock, actor mailbox semantics, CSP rendezvous, the Tu et al. numbers) is sound and well-sourced. My objections are all precision/caveat issues, not factual errors.

### SHOULD FIX

**1. "Go, its best-known descendant."** (§5)
CSP's direct, formal descendant is Occam, built by Hoare's own group specifically to implement the CSP calculus. Go is influenced by CSP indirectly, through Pike's earlier languages (Newsqueak, Alef, Limbo), and Go also permits shared memory, which pure CSP does not. Calling Go a "descendant" overstates the lineage.
Fix: *"Go, the language most people associate with it"* or *"the CSP-influenced language most people know."*

**2. "Neither model can do anything the other can't."** (§8)
This states the Lauer–Needham duality thesis as an unqualified fact. The thesis is about expressive power / mutual simulation (a lock can be encoded as a permission-granting process, a channel as a locked queue), not about performance, ergonomics, or behavior under real constraints (distribution, real-time). Stated bare, it invites the inference that the choice never matters, which the very next sentence (use whichever is simplest) then has to walk back.
Fix: *"Neither model can express anything the other can't — you can build one out of the other. That doesn't mean they're equally convenient."*

**3. "Two decisions are left in every model."** (§8)
"Every model" reaches beyond the three mechanisms actually discussed (locks, actors, channels) to imply a law over all concurrency paradigms — including ones the video never examines (STM, dataflow), where atomicity and cycle-freedom are handled differently (e.g., STM resolves conflicts by retry, not by the programmer avoiding a cycle).
Fix: *"Two decisions are left in each of these models."*

**4. Data races are only illustrated as "lost updates."** (§2, throughout)
The video's running consequence of a data race is a stale/overwritten value — true and well-chosen for the example, but it leaves the impression that a data race's worst case is "the counter is off by a bit." JCIP and the Go memory model are explicit that an unsynchronized data race gives no behavioral guarantee at all (torn reads on multi-word values, effects of compiler/CPU reordering, etc.), not just an occasional lost increment.
Fix: add one clause, e.g. *"...and that's the mild case — with no synchronization at all, the language doesn't promise you'll even read a whole, valid value."*

### NIT

**5. "In five runs on this machine it ended between ten and thirteen million."** (§2)
The five values are 11,856,624 / 10,850,072 / 10,662,642 / 10,780,763 / 12,988,652 — the true minimum is ~10.66M, not 10M. The round bounds are a defensible narration simplification, but if you want it exact: *"between about ten point seven and thirteen million."*

**6. Citation year: "Lauer & Needham... (1978)."** (references)
The paper was presented at a 1978 symposium but is most commonly cited by its Operating Systems Review publication, April 1979. Either is defensible; worth picking deliberately rather than by default.

### Nothing essential missing, nothing peripheral overweighted
The two-way shared-memory/message-passing framing (§1) is a legitimate, standard high-level split even though the cited Butcher book covers seven models — the video is explicit about its own scope, so this doesn't need a caveat. The Erlang/Akka "private state by convention" distinction, the check-then-act race without a data race (§6), and the "message passing trades data races for hangs" result from Tu et al. (§7) are the three most important ideas in the script and are all given correct, undiluted treatment — good.

VERDICT: PASS
