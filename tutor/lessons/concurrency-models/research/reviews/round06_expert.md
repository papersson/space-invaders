I reviewed the script and evidence table line by line — arithmetic, terminology, attributions, and internal consistency between narration and the sourced numbers. I attempted to independently verify the Tu et al. (2019) statistics via web search but wasn't granted tool permission; I'm relying on the evidence file's own verification note for that one item. Findings below.

## SHOULD FIX

**Quote:** *"It comes from Tony Hoare's communicating sequential processes, or CSP, and Go's channels come out of this tradition. Processes share nothing, and talk over channels. A channel is a connection that processes send values into and receive them from."*

**Problem:** This attributes the channel-as-a-first-class-object idea to Hoare's 1978 CSP directly. It isn't — Hoare's original CSP has no channel objects; processes communicate by naming each other explicitly in input/output commands (`P?x`, `Q!v`). The separate "channel" construct that Go's channels resemble was introduced later, by occam (1983), an INMOS language descended from CSP. What *is* correctly attributable to Hoare 1978 is the rendezvous property itself (a send/receive pairs up synchronously) — that part is fine.

**Fix:** Either soften the attribution ("Go's channels come out of this tradition, by way of languages like occam that gave CSP's rendezvous a first-class channel object") or drop the "channel is a connection..." sentence's implicit claim that this is Hoare's own formulation.

---

**Quote:** *"In Erlang, processes don't share memory by default. A message is copied to the receiver."*

**Problem:** True as a simplification, but incomplete: binaries larger than 64 bytes in Erlang are reference-counted and shared, not copied, on the BEAM. Since the very next sentence ("Shared tables exist, but a process has to opt in") shows the script is willing to note exceptions to "share nothing," omitting this one is an inconsistency in how much precision is applied.

**Fix:** Either leave as-is with a brief acknowledgment ("large binaries are the exception, shared by reference") or don't raise the ETS exception either, for symmetry. As written it applies the caveat selectively.

---

**Quote:** *"A bug whose result depends on the timing of concurrent steps is called a race condition."*

**Problem:** Minor terminology looseness: a race condition is standardly defined as a *condition/property* of the program (correctness depends on interleaving), not "a bug" per se — a race condition can exist without ever manifesting as an observed bug. This is nitpicky but the script is otherwise careful to distinguish "race condition" from "data race" as two precise, different things in the very next lines, so blurring "condition" into "bug" undercuts that precision.

**Fix:** "A property of a program, where the result depends on the timing of concurrent steps, is called a race condition."

## NIT

- **"the account was overdrawn in about seventeen hundred"** (1,703/100,000) and **"got stuck in about half"** (482/1,000) — both fine, rounding is honest and doesn't overstate.
- The Tu et al. 2019 breakdown (86 wrong-result bugs split 69/17, 85 hang bugs split 36/49, totaling 171) is a precise, quotable stat from a well-known paper. The evidence table says it was checked against the source (`research/verified_tu2019.md`); I could not re-verify it myself this pass since WebSearch wasn't authorized. Given how exact these numbers are and how easy transcription errors are, I'd want a second pass confirming Table 6/9 and the Observation-3 wording directly against the PDF before this ships, even though I have no specific reason to doubt it.
- "Say each transfer locks the paying account first, then the receiving account" followed later by "every piece of code that takes these locks has to follow that order, including code someone else wrote" gestures at JCIP's "alien method" / open-call problem without naming it. That's fine for an intro audience — just flagging that the citation (JCIP §10.1.3–10.1.4) is for a slightly more specific concept than what's spoken.

## What I checked and found solid
- The bank-account arithmetic throughout (100+50+50=200, 100−100−100=−100, C(6,3)=20 orderings with exactly 2 safe, 20,000,000 expected counter total) is all correct.
- Every "screen" number matches its "evidence" source value (10.1–11.7M range, 989→0, 1,703/0, 482→0, 17/86≈1-in-5, 49/85>half).
- The data-race / race-condition distinction, the C/C++ UB claim, the actor-model description, Go's unbuffered-channel-as-default and rendezvous semantics, the lock-ordering deadlock fix, and the final comparison table are all accurate and appropriately hedged — no overstated optimality or generality claims anywhere (the script is careful to say "where enforced," "by convention," "possible in all three").
- Citations (Hewitt 1973, Hoare 1978, Lauer & Needham 1979, Coffman et al. 1971, JCIP, OSTEP, Effective Go) are all real and correctly matched to the claims they support.

None of the above rises to BLOCKING — the substance is right throughout; the issues are attribution precision and one unverified-by-me numeric citation.

VERDICT: PASS
