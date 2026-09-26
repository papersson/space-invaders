# Review

## Test 1 — Opening question / closing callback
Opening (Ch.1): *"So what is an LLM agent, that taking away one tool leaves it sure of something false?"*
Closing (Ch.9): *"So why did one missing tool leave run B sure of something false? Because an agent is a model that picks each next step from its context..."*
This is a clean, near-verbatim callback — the strongest structural element in the script. **Pass, no finding.**

## Test 2 — One-sentence-per-segment chain; report every "and then"
Reconstructed chain (chapter-level):
1. Two runs, same everything; A says Fixed+passes, B says Fixed+fails, 3/3, only difference is B lacks run_tests — question posed.
2. Therefore start with the model alone: it reads/writes text, but nothing executes what it writes.
3. Therefore code runs tools and feeds results back, but one call isn't enough — a second tool call goes unhandled.
4. Therefore a loop: call/run/add/call until no tool call — that's the agent; walk run A up to the pause-and-predict.
5. But the test fails (KeyError), therefore the model reads sales.csv, finds the BOM, fixes it, and the test passes — an agent, not a workflow.
6. But the model remembered nothing — every call re-reads the whole context (18,537 tokens over 9 calls) — therefore the context is its only memory.
7. Therefore run B: same loop minus run_tests; its context never receives a test result, so its "Fixed" stands — first failure mode.
8. But there's a second failure mode: context only grows, and every call re-reads all of it (Claude Code: 11,597 → 123,192).
9. Therefore the answer.

Every link is "but"/"therefore" — literal "and then" count: **0**. No filler sequencing found. **Pass.**

## Test 3 — Ideas announced vs. derived from a visible problem
Nearly everything is derived on-screen from a shown failure (context from ch.2's dead command; tool call from ch.2's problem; loop from ch.3's stuck-after-one-call). Two exceptions:
- **"Compounding errors"** (Ch.7) is asserted about a hypothetical longer task, not shown happening in either run.
- **"Context rot"** (Ch.8) is explicitly flagged by the script itself as unshown ("Our runs are far too short to show it").
See findings below.

## Test 4 — Setups without payoffs / payoffs without setups
- Card colors (grey/blue/green) planted unexplained in Ch.1, paid off in Ch.9 — good long-range payoff.
- Pause-and-predict (Ch.4) paid off immediately in Ch.5 — good.
- **`max_calls=20`** (Ch.4) is a setup that never pays off — no run comes close to 20 calls.
- "Compounding errors" is effectively a payoff (a named, consequential idea) without an on-screen setup instance — see Test 3.

## Test 5 — Terms before explanation / concepts with two names
All jargon (context, tool call, ground truth, workflow, BOM, compounding errors, context rot) is defined at first use — good discipline. One real collision:
- **"Request"** is used for two different things: the user's original task (Ch.2: *"our request"*) and the model's tool call (Ch.3: *"That request is called a tool call... Our code reads the request"*). Flagged below.

## Test 6 — Numbers: worth remembering vs. dead weight
Worth remembering: **3 of 3** (reproducibility), **18,537 tokens over 9 calls** (cost of a 2-line fix), **123,192 vs 11,597** (Claude Code growth).
Numbers doing no work: **"twenty calls"** cap (never hit). Also a consistency snag: **"9 calls · 10 tool calls"** for Claude Code contradicts the run-A pattern established in Ch.6 ("eight tool calls, then the final reply" over nine calls) — flagged below.

## Test 7 — Abstraction before the concrete case
No violations found. The script consistently shows a problem (dead command, stuck loop) before naming the mechanism that fixes it. This is a genuine strength.

## Test 8 — The wrong intuition, and is it shown failing
Wrong model: *"the agent... remembers... knows when it has succeeded... a better model makes a better agent... code is plumbing."*
- "Remembers/knows it succeeded" is confronted concretely and repeatedly (Ch.1's reveal, Ch.6, Ch.7 verbatim: *"It looks as if the model knew it had succeeded. It didn't."*). Strong.
- "A better model would fix this" is only asserted once, in passing, never demonstrated (Ch.9: *"A smarter model might read more carefully. But it still can't see a test result that never arrives."*). This is the one sub-claim of the named wrong intuition that gets a rebuttal without evidence, in a script that otherwise earns every claim with a captured run. Flagged below.
- "Code is plumbing" is implicitly addressed (the code's tool list determined the whole outcome) but never explicitly named/rebutted the way the other two are — minor.

## Test 9 — Examples named but not understood
BOM: named and fully explained (shown, causally tied to the KeyError). Good.
- **Context rot**: named, cited, explicitly not demonstrated. Flagged (ties to Test 3/8).
- **Claude Code's token count**: named with a rough cause ("instructions, tool descriptions, our request") but never broken down proportionally the way run A's overhead was in Ch.6. Minor.

## Test 10 — On-screen text vs. narration; pictures vs. line
Screen direction is unusually disciplined — almost everything shown is real captured data, not decorative repetition. One exception:
- Ch.7's on-screen label **"nothing checks the work"** lands right after the narration says the identical clause — pure duplication rather than added information. Flagged below.

## Test 11 — Lines that could be deleted
Surprisingly little fat. The closest candidates (Anthropic-documentation citations in Ch.3/Ch.6) each back a distinct claim and generalize the toy example to the real API/agent — I would not actually cut them. No line meets the bar for deletion.

## Test 12 — Hard-to-follow sentences; rushed or padded beats
- Ch.8: *"Twice the calls means more than twice the reading, because each new call re-reads everything before it"* compresses a superlinear-growth idea into one breath — the densest idea-per-word moment in the script. Minor pacing flag.
- Ch.1 carries a lot of visual information (two strips, real quotes, "3 of 3") in a short narrated span, but the screen direction explicitly holds the strips on screen, which mitigates it.
- No beat reads as padded.

---

## Findings

**SHOULD FIX** — Overloaded term "request"
> Ch.2: *"some instructions and our request."* Ch.3: *"That request is called a tool call... Our code reads the request, runs it."*
Same word names both the user's original task and the model's tool-call message. Rewrite: keep "request" for the task only ("some instructions and the task: fix report.py"), and name the model's output something else ("That message is called a tool call... Our code reads the tool call, runs it").

**SHOULD FIX** — Numeric inconsistency in Claude Code example
> Ch.8 narration: *"found both bugs in nine calls, like run A."* Screen: *"9 calls · 10 tool calls."*
Ch.6 established run A as 8 tool calls across 9 calls (last call has no tool call). "10 tool calls" in 9 calls breaks that pattern for an attentive viewer. Rewrite: correct the count, or add a half-line clarifying why it differs, e.g. "nine calls, one of them asking for two tools at once."

**SHOULD FIX** — Unshown rebuttal of "a better model would fix this"
> Ch.9: *"A smarter model might read more carefully. But it still can't see a test result that never arrives."*
This is the one piece of the named wrong intuition that's asserted rather than demonstrated, in a script that otherwise earns every claim with a captured run. Rewrite: either cut it, or make it evidence — "We reran run B with Anthropic's strongest model available. It still said 'Fixed.'"

**SHOULD FIX** — "Compounding errors" named without an on-screen instance
> Ch.7: *"And in a longer task, later steps would build on that guess... That's called compounding errors."*
Valid inference from established mechanics, but presented with the same confidence as demonstrated claims elsewhere, unlike context rot which is honestly flagged as unshown. Rewrite: mark it explicitly as inference — "and if this were one step in a longer task, the next call would read that guess as fact and build on it — nothing here would catch it either."

**NIT** — Dead setup: the 20-call cap
> Ch.4: *"Stop when it replies without one, or after twenty calls, in case it never does."*
Never exercised by any shown run. Cut from narration (keep only in the on-screen code) or drop entirely: "Call the model. If its reply is a tool call, run the tool, add the result, and call the model again. Stop when it replies without one."

**NIT** — On-screen text duplicates narration
> Narration and screen label both read essentially *"nothing checks the work"* (Ch.7).
Replace the label with something additive — e.g. point at the empty slot where a test result would have gone, labeled "no ground truth arrives here."

**NIT** — Workflow counterfactual is illustrative, not a real capture
> Ch.5: *"Suppose we had scripted the steps instead... Ours would have stopped at the key error."*
Everything else in the video is a real capture; this branch is a diagram. Consider labeling it on screen as illustrative so it isn't mistaken for another data point.

**NIT** — Claude Code token count isn't broken down like run A's
> Ch.8: *"its instructions, its tool descriptions, and our one request."*
Ch.6 gave run A's overhead a proportional split (~1,180 / ~240); Claude Code's 11,597 gets only a qualitative list. Add rough proportions for parity.

**NIT** — Dense sentence, superlinear growth in one breath
> Ch.8: *"Twice the calls means more than twice the reading, because each new call re-reads everything before it."*
Consider splitting: "Twice the calls costs more than twice the reading. Each new call re-reads everything that came before, so the total grows faster than the task does."

---

VERDICT: PASS
