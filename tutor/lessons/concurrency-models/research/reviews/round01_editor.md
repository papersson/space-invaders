# Script Review

## Test 1 — Opening question / ending answer

The bookend works at the literal level: Ch1 asks *"So does passing messages make bugs like the vanishing deposit go away?"* and Ch8 opens *"So does passing messages make the bugs go away? Some of them."* — same question, echoed almost verbatim.

**SHOULD FIX.** The callback drops the concrete image (cash machines, the vanished $50, the $150) and answers only the abstract version. The opening spent real time building a specific picture; the ending should cash that out by name, not just gesture at "the bugs."

> Quote: *"So does passing messages make the bugs go away? Some of them."*

Rewrite: *"So does passing messages make the vanishing deposit go away? Yes — give the balance one owner, and that exact bug can't happen. But some of its cousins remain."*

## Test 2 — Segment chain, report every "and then"

Reconstructing the chain in but/therefore form matches the author's own Chain section, and it holds together with **zero "and then"s** — every joint is a real "but" or "therefore."

**SHOULD FIX (structural, ties to Test 12).** Ch4 and Ch5 (actor, then channel) are joined by neither connective in substance — Ch5 restates Ch4's point ("same idea, different plumbing") rather than complicating it. Functionally this pair reads as "and then here's another mechanism," even though it's dressed as continuation. Two full segments making the same point ("one owner, no data race") risks a pacing lull right before the video's real pivot in Ch6. Consider compressing the channel/actor comparison into fewer beats, or adding a forward-pointing line at the end of Ch5 to keep momentum (e.g., a hint that ownership alone hasn't finished the job).

## Test 3 — Ideas announced vs. derived

**BLOCKING.** The single most important "therefore" in the whole video — the pivot from the shared-memory half to the message-passing half — is asserted, not derived. Ch3 ends by exposing exactly *why* locks are fragile: *"it only protects code that takes it... nothing stops one forgotten code path from touching the balance without it."* Ch4 then opens cold: *"Message passing starts from a different idea. Give the balance a single owner, and let nothing else touch it."* The connection between "a lock can be forgotten" and "so make it impossible to forget by removing all other access" is real and strong — but the script never states it. The viewer has to supply the link themselves at the exact moment the argument changes models.

> Quote: *"Message passing starts from a different idea. Give the balance a single owner, and let nothing else touch it."*

Rewrite: *"What if nothing else could touch the balance at all — no forgotten lock, because there's no lock to forget? Message passing starts from that idea. Give the balance a single owner, and let nothing else touch it."*

Minor/lower stakes: the lock fix itself ("The shared-memory fix is a lock") and the "messages can deadlock too" opener in Ch7 are also announced rather than derived, but both get their payoff demonstrated within the same breath, so they don't rise above a NIT.

## Test 4 — Setups without payoffs, payoffs without setups

- Setup *"Erlang and Akka are built on actors"* (Ch4) — never paid off; see Test 9.
- Setup *"This is called a rendezvous"* (Ch5) — named, never reused. Low stakes, but if it's not going to do work later, it doesn't need a name.
- Payoff *"Actors don't block on a send. But as soon as an actor sends a request and waits for the reply..."* (Ch7) correctly pays off the send-doesn't-wait vs. send-waits distinction set up in Ch4/Ch5. Good.
- The Ch3 "forgotten code path" setup is the one that never gets its explicit payoff — already flagged as BLOCKING above.

## Test 5 — Terms before explanation / double-naming

No real violations. "Race condition" and "data race" are both defined at first use, in the right order (behavior, then name). "CSP," "rendezvous," and "deadlock" are likewise named at the moment they're explained. No concept is given two competing names that could confuse ("actor" and "process" are two different roles, explicitly distinguished, not synonyms).

## Test 6 — Numbers

Full list: $50/$50, $100, $200, $150; 10,000,000×2, 20,000,000 (expected); five raw run results (11,856,624 · 10,850,072 · 10,662,642 · 10,780,763 · 12,988,652); 20,000,000×3 (locked); 1,000 runs / 992 stuck / 0 stuck; 100,000 runs / ~1,683 overdrawn / 0 overdrawn; 1,000 runs / ~497 stuck; 171 bugs, 69 vs. 17, 36 vs. 49, "forty-nine of eighty-five"; 1978.

**Worth remembering: $150** (the emblem of the whole video), the **1,683 → 0** contrast (proves the fix works), and **49 of 85** (the one number that actually proves the takeaway — message passing shifts bug type rather than eliminating bugs).

**SHOULD FIX** — the five full-precision counter results do no extra work over "several million short, and different every time"; reading eight-digit numbers aloud/on-screen five times in a row is padding.

> Quote: *"11,856,624 · 10,850,072 · 10,662,642 · 10,780,763 · 12,988,652"*

Rewrite: keep two, e.g. *"11.9 million, 13.0 million — short by different amounts each run"* (round; cut to two or three data points).

**NIT** — *"first published in 1978"* is trivia doing no argumentative work; safe to cut from narration and leave in the citation card.

## Test 7 — Abstraction before the concrete case

No real violations. The video is disciplined about concrete-before-abstract throughout: the bank example precedes the Go slogan, the interleaving precedes "data race," the lock example precedes "lock ordering," the closing table is appropriately the last, most abstract beat.

## Test 8 — Wrong intuition, shown failing?

The wrong model ("message passing removes concurrency bugs") is never voiced as a claim — it's implied by the framing question and then, importantly, *reinforced* for two full chapters (Ch4, Ch5 both show message passing succeeding) before being punctured in Ch6. The puncture itself is good: *"So is the vanishing money solved? For deposits, yes. Now try withdrawals."* — that line does the real work of staging the wrong intuition right before breaking it.

**SHOULD FIX.** Sharpen the moment right before the break so the wrong intuition is explicit rather than inferred, since Ch4–5 spent real time making it look true.

> Quote: *"So is the vanishing money solved? For deposits, yes. Now try withdrawals."*

Rewrite: *"So it looks like the slogan wins: give every piece of state one owner, and the bugs disappear. For deposits, that's true. Now try withdrawals."*

## Test 9 — Examples named but not understood

**SHOULD FIX.** *"Erlang and Akka are built on actors."* — named, dropped, never used again. Either cut it, or spend one sentence making it do work (e.g., what differs between a language with actors built in vs. a library that only offers them by convention — the on-screen note already has this content, but it's never spoken).

**SHOULD FIX.** *"Docker and Kubernetes among them"* — named for credibility but no concrete bug from either is ever walked through; the study is used purely as an aggregate statistic. Given the video's otherwise strict concrete-before-abstract discipline, this is the one place real systems are invoked without being made concrete.

Rewrite: either drop the project names from narration (keep them in the citation card only) — *"A study of real concurrency bugs in six large Go codebases found..."* — or add one line grounding a specific bug.

## Test 10 — On-screen text vs. narration; pictures vs. line

**SHOULD FIX.** In Ch2, the captions *"race condition: the result depends on timing"* and *"data race: same memory, one writes, no order"* restate the spoken definitions almost verbatim, right as they're spoken. This wastes the visual channel at the video's first key definitional moment — the diagram alone (with a short label) would let the eye and ear carry different information.

Elsewhere, pictures support the line well throughout (the timelines, the lock/waiting bars, the deadlock cycle, the closing table) — no other mismatches found. Note the reverse issue in Ch4/Ch5: the on-screen notes about Erlang/Akka and "Go also allows shared memory" add content the narration never says — not wrong, but orphaned; folds into the Test 9 fix.

## Test 11 — Deletable lines

- *"Erlang and Akka are built on actors."* — deletable without loss (see Test 9).
- *"first published in 1978"* — deletable (see Test 6).
- Everything else earns its place against the stated objectives; nothing else is pure filler.

## Test 12 — Hard to follow aloud / rushed or padded beats

**NIT.** *"Two threads use the same memory, at least one of them writes, and nothing forces an order between them. That's a data race."* — three conditions in one breath. Split it: *"Two threads use the same memory. At least one writes. And nothing forces an order between them. That's a data race."*

**NIT.** *"Say each transfer locks the account it pays from, then the one it pays into."* — the antecedent of "the one" is a beat late for audio. Rewrite: *"Say each transfer locks the paying account first, then the receiving account."*

**SHOULD FIX (rushed).** *"A lock can be written as a process that hands out permission, and channels are built with locks inside."* — this is the most surprising claim in the whole video (the two models are equally powerful) and it gets one dense sentence with no dedicated visual before the script moves on to the closing recommendation. It deserves either more room or its own beat in the closing table.

**SHOULD FIX (padded, cross-ref Test 2).** Ch4–Ch5 together spend two full segments establishing the same point ("one owner ⇒ no data race") with different vocabulary. Not wrong, but the pacing sags right before the video's actual complication in Ch6.

---

**Summary of severities:** 1 BLOCKING, 8 SHOULD FIX, 4 NIT.

VERDICT: REVISE
