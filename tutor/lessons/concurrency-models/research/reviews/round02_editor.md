# Script Review

## Test 1 — Opening question / closing callback
**Pass.** Segment 1 asks "does passing messages make bugs like the vanishing deposit go away?" Segment 8 opens with "So does passing messages make the vanishing deposit go away? Yes" and the screen direction explicitly returns to "the chapter 1 scene: two deposits into the actor, balance $200" — the same account, now fixed. Clean callback.

## Test 2 — One-sentence-per-segment chain, report every "and then"
Chain holds together on but/therefore, with one lateral "and" (channels, segment 5, presented explicitly as "same idea, different plumbing" rather than a consequence of anything). See Test 3/7 below for why that lateral move is worth a second look.

Literal "and then" found once in the narration itself:

- **NIT** — *"Nothing stops one forgotten code path from touching the balance without it, and then the race is back."* (Segment 3) — functions causally, not as filler, but tightens cleanly. Rewrite: *"Nothing stops one forgotten code path from touching the balance without it — so the race is back."*

## Test 3 — Ideas announced vs. derived from a visible problem
Everything is derived from a shown failure **except** the move into CSP:

- **SHOULD FIX** — *"The other message-passing family comes from Tony Hoare's communicating sequential processes, or CSP."* (Segment 5) — the actor already solved the on-screen problem (data race); channels aren't introduced because actors visibly failed at something, just as "the other family." Since two mechanisms doing the same job is itself worth teaching, ground the transition in a real difference that matters (e.g., actors give you no way to know a message arrived; CSP's blocking send does), so the segment answers a question instead of adding an item to a list.

## Test 4 — Setups without payoffs, payoffs without setups
- **SHOULD FIX** — Locks get a demonstrated fix for deadlock (fixed ordering, tested 992→0 in segment 3), but the message-passing deadlock in segment 7 (*"stuck in about half"*) gets no analogous fix or test, even though the two deadlock beats are visually built as parallel (same cycle diagram, same "1,000 runs" framing). A viewer trained by segment 3 to expect "...and here's the standard fix" gets a payoff-less setup. Either show the analogous fix (e.g., ordered requests) tested the same way, or add one line acknowledging why none is given — that this is the open half of the takeaway, not a solved problem.
- Erlang/Akka ("enforced" vs. "by convention," segment 4) does get a quiet payoff in segment 8's *"at least where the language enforces it"* — thin but present, not a violation.

## Test 5 — Terms before explanation / duplicate names
No violations found. "Race condition" and "data race" are introduced in the correct order and kept distinct throughout (the harder case, "race condition without a data race," is explicitly flagged as such in segment 6). "CSP," "actor," "mailbox," "process," "channel" are each defined at first use, and the actor/CSP terms are never allowed to blur into synonyms.

## Test 6 — Numbers: which 2–3 matter, which do no work
All numbers: $50/$100/$150/$200 · 20,000,000 expected vs. five runs (11.9M/10.9M/10.7M/10.8M/13.0M) · 20M×3 with lock · 1,000 runs, 992→0 (lock deadlock fix) · 100,000 runs, 1,683→0 (withdrawal race fix) · 1,000 runs, 497 (message deadlock) · 171 bugs / 86 wrong-results (17 message-passing) / 85 hangs (49 message-passing).

**Worth remembering:** the counter contrast (~11–13M vs. 20M, fixed by a lock) and the Tu et al. split (17-of-86 vs. 49-of-85) — the latter is the single number that actually carries the takeaway's asymmetry claim.

- **NIT** — the five individual run values shown on screen (11.9M, 10.9M, 10.7M, 10.8M, 13.0M) do more precision-work than the narration uses (*"between about ten point seven and thirteen million"*); with six separate numeric experiments already in the video, this is a candidate to simplify visually.

## Test 7 — Abstraction before the concrete case
Mostly fine — the ATM example precedes the shared-memory/message-passing taxonomy in segment 1, and actor/CSP definitions each follow a motivated concrete need. One exception:

- **SHOULD FIX** — *"Neither model can express anything the other can't."* (Segment 8) is a strong abstract claim that arrives with only a sketch ("a lock built as a process... a channel with a lock inside"), not a worked, tested case — the only claim in the script not backed by a demo or numbers, unlike every other assertion in the video. Either cut it to a lighter aside, or give it the same treatment as everything else: one concrete instance actually traced through.

## Test 8 — Wrong intuition confronted and shown failing
**Pass.** Stated wrong model: "message passing is the safe model." It's shown failing twice with numbers: the withdrawal race (1,683/100,000 overdrawn with two messages) and the message deadlock (497/1,000 stuck). This is the strongest part of the script.

## Test 9 — Examples named but not understood
No violations. Erlang, Akka, CSP, and the Tu et al. study are each given at least one substantive, specific claim, not just name-dropped. The six project names (Docker, Kubernetes, etc.) are on-screen citation only and don't need individual treatment.

## Test 10 — Redundant on-screen text / unsupporting pictures
- **NIT** — the three tags *"same balance," "both write," "no order"* (segment 2) land as a near-verbatim restatement of the spoken definition, clause for clause. Consider shortening to icon-labels or delaying them slightly so they confirm rather than duplicate.
- No pictures found that fail to support their line — the diagrams (interleaved timelines, lock-wait cycles, mailbox queue, table in segment 8) all track the narration directly.

## Test 11 — Deletable lines
Script is tight; no clearly disposable lines found. The closest candidate, *"Go also lets threads share memory, so there, one owner is a habit the programmer keeps, as in Akka"* (segment 5), earns its place by paying off the enforced-vs-convention thread from segment 4 — keep it.

## Test 12 — Hard-to-follow-aloud / pacing
- **SHOULD FIX** — *"So one owner per piece of state rules out data races on it, by the structure of the program instead of everyone remembering a lock, at least where the language enforces it."* (Segment 8) stacks three trailing qualifiers; a listener will lose the thread by the third. Rewrite: *"So one owner per piece of state rules out data races on it — by the structure of the program, not by everyone remembering a lock. That's true, at least, wherever the language enforces the ownership."*
- **SHOULD FIX** — *"A study of a hundred and seventy-one real concurrency bugs in six large Go projects sorted them two ways. Of the eighty-six bugs that gave wrong results, only seventeen came from message passing. Of the eighty-five where code hung, forty-nine did."* Five numbers in two sentences, with the last sentence's verb elided ("forty-nine did"), is hard to track by ear alone. Rewrite: *"...Of the eighty-six bugs that gave wrong results, only seventeen came from message passing. But of the eighty-five where code hung, forty-nine came from message passing — more than half."*
- **SHOULD FIX (pacing)** — segment 5 is comparatively rushed: CSP, "process," "channel," blocking sends, and the actor/channel plumbing contrast all land in six sentences with no dedicated visual beat (unlike segment 4's mailbox animation). Consider a beat that shows the blocking send stalling, mirrored against the actor's non-blocking send.

---

**Summary:** the core chain, the opening/closing symmetry, and the central refutation (message passing still races and deadlocks) are all sound and well-evidenced. The findings above are about tightening a transition (channels), balancing a demonstrated payoff (message deadlock has no fix, unlike lock deadlock), grounding the one un-demonstrated claim (duality), and two dense sentences that need breathing room aloud. None of these break the argument or mislead the viewer.

VERDICT: PASS
