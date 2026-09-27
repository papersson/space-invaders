# Script Review

## 1. Opening/closing question test
Opens: *"So what sits in between? How do you get from a model that writes text, to an agent that fixes a bug?"* (dashed "?" box, held on screen).
Closes: *"So, how do you get from a model that only writes text to an agent that fixes a bug?"* — then the ch.1 picture returns with the "?" box filled with "harness."

**Pass.** Literal restatement + explicit visual callback (word fills the box). This is about as clean as this test gets.

## 2. Chain (one sentence per segment, but/therefore/and then)
1. Question: ChatGPT (2022) only talked; agents now act; same model; model only writes text — **but** what's in between?
2. **Therefore** start with the model: predicts next word from context, repeatedly — two facts follow (text out, context in).
3. **But** text alone does nothing (bare model writes a dead command) — **therefore** agree a request format + a program beside the model.
4. **But** the model can't see results (fact 2) — **therefore** the program pastes results back and reruns the model.
5. **But** one step won't fix a bug — **therefore** loop until no request = agent; real run of 12 requests, a failing test that changes course.
6. **But** why did 2023 agents get stuck? **Because** small errors compound (95%→~1/3 over 20 steps) — **therefore** three fixes: trained-for-loop models (99%→~4/5), feedback, step-by-step search.
7. **Therefore** name the parts: LLM = model, everything else = harness.
8. **Therefore** the answer: model still only predicts words; harness converts text→action and feeds results back; loop turns steps into a job.

**"And then" count: zero.** No segment relies on bare sequencing — every joint is causal. This is a genuine strength; say so explicitly rather than just noting it in passing.

## 3. Ideas announced vs. derived
Mostly well-derived (request format and the program both follow directly from a shown failure: model writes a command, nothing runs, tests stay red). Two exceptions:

- **SHOULD FIX** — Quote: *"Three things changed. First, models were trained to work in this loop... Second, tasks like coding come with feedback... Third, agents find what they need by searching..."* Only the first item (compounding math) is grounded in something visible; items 2 and 3 are asserted as historical facts rather than shown failing/succeeding. **Rewrite:** tie #2 directly back to the run just shown — *"Second: the run you just watched had feedback built in — the failing test is what caught the discount mistake. Without it, that bug ships."* — and tie #3 to a one-beat contrast (a hard-coded index gets stale; searching doesn't), rather than a bare claim.

- **NIT** — Quote: *"A real harness does more. It checks permission before an edit or a command... And a context has a size limit..."* These are announced additions with no visible problem behind them (no near-miss shown, no context overflow shown). Fine as a "by the way," but if you want it to land, show one frame of it happening rather than stating it.

## 4. Setups/payoffs
- **Setup→payoff, clean:** ch.1 "?" box → ch.8 filled with "harness." Ben's bill (37 vs 39.50) → discount off-by-one found and fixed → tests pass.
- **SHOULD FIX** — payoff without setup: Quote: *"Its developers have said that worked better than building an index of the code in advance."* Nobody has mentioned "an index of the code" before this line; it answers a question the viewer never had. **Rewrite:** cut it, or set it up one beat earlier in the same sentence: *"...instead of pre-building a map of the whole codebase — Claude Code's developers found that searching as you go works better than that."*
- **SHOULD FIX** — setup without clear payoff: AutoGPT is set up as "got stuck, going round in circles" but the payoff (why) arrives only as generic math, never re-anchored to AutoGPT itself. See #9 below.

## 5. Terms before explanation / duplicate names
- **SHOULD FIX** — Quote: *"it even writes out a command to explore the project"* (ch.3, bare model) vs. two sentences later, *"the model writes a line: search, 'no price for'"* called a **request**. "Command" and "request" both mean "text asking for an action," introduced back-to-back for two different things (one inert, one functional) — a viewer can easily read them as synonyms and miss that the whole point of the chapter is that only one of them does anything. **Rewrite:** don't call the bare model's output a "command" at all — *"the model even writes out, in plain English, what it would do next"* — reserving "request" for the one term that matters.
- All other terms (context, LLM, tool, loop, agent, harness) are introduced at or before first substantive use, or are the video's own mystery term (agent, used loosely in ch.1, formally defined ch.5) — that's a legitimate device, not a violation.
- "Next word" for "token" is a deliberate, disclosed simplification — fine, not a violation.

## 6. Numbers
Full list: 31/19/1.5/1.3/1.2% (word probabilities); 18%, 8% (and, I); 2022, 2023 (dates); $37.00 vs $39.50; 10 vs 11 items; 12 requests; 95%, 20 steps, ≈36% (~1 in 3); 99%, ≈82% (~4 in 5).

**Worth remembering (pick 3):** (1) 95%→~1/3 vs 99%→~4/5 clean-run odds — the actual explanation for "why now"; (2) 12 requests — proof the loop wasn't scripted; (3) 37.00/39.50 and 10/11 — the concrete bug, the thing viewers will retell.

**Numbers that do no work:** none egregious — 19/1.5/1.3/1.2% are shown, not narrated, and exist only to make the bar chart's tail visible; they're not asked to be remembered, so this is fine. No flag needed here beyond noting it.

## 7. Abstraction-before-concrete
Not violated — this is a strength worth calling out. Every abstraction (context, tool, loop, harness) is preceded by its concrete instance in the same or prior chapter, and "harness" — the most abstract term in the piece — is deliberately held until ch.7, after four chapters of watching the concrete pieces work. Keep this ordering; it's doing real work.

## 8. Wrong intuition
Named: *"the model itself reads the files and runs the tests... it simply 'learned to act.'"* Shown failing: yes, concretely — ch.3's bare-model demo (writes a command, dashed arrow stops at a grey cross, badge stays red). Refuted again at the close: *"ChatGPT in 2022 could only talk. An agent is still talking."*

**NIT** — the misconception is shown failing but never voiced as a misconception ("you might think the AI is doing this on its own") before the demo corrects it, so a viewer who already holds the wrong model may not clock the ch.3 demo as aimed at them. **Rewrite,** add one clause before the demo: *"It's tempting to think the AI itself just goes and does this. Watch what actually happens when you ask it to."*

## 9. Named but not understood
- **SHOULD FIX** — AutoGPT: named, given a fate ("got stuck, going round in circles"), but never shown failing and never reconnected to the compounding-mistakes explanation that follows. It reads as color, not evidence. **Rewrite:** either give it one concrete beat ("it would search for a file, not find it, and try the same search again") or drop the name and keep only "early attempts in 2023."
- **SHOULD FIX** — Claude Code: named once in ch.6 with an unsupported comparative claim (#4 above). If the worked example in ch.3–5 is in fact a Claude Code transcript (the references suggest it is), the script never says so — meaning the name-drop in ch.6 doesn't collect on the concrete demonstration the viewer already trusts. **Rewrite:** state the connection when the run starts, e.g. ch.3: *"Here's a real run — recorded from Claude Code, an agent built this way"* — so ch.6's callback pays off something the viewer already watched work, instead of introducing a fourth unexplained name.

## 10. On-screen text vs. narration / picture-line mismatch
No picture actively contradicts or fails to support its line. But several on-screen texts are near-verbatim duplicates of the narration, spent on the recap in ch.7 especially:

- **SHOULD FIX** — Quote (narration): *"The LLM predicts the next word. The context is all it sees. A tool is something the harness does when the model asks. The harness runs the tools and the loop. And together, the LLM and the harness are the agent."* Screen: *"a glossary card... one row per term as it is said."* Full duplication across both channels back-to-back at the point where pacing matters most (the takeaway beat). **Rewrite:** let the glossary card carry the definitions silently/already-visible, and have narration do something the text can't — e.g. point at each row rather than re-reading it: *"Five words. You've met them all."* (then a beat of silence over the card).
- **NIT** — ch.1's three action chips ("read files," "run tests," "fix the bug") echo the sentence almost word-for-word; acceptable as a label but redundant. No rewrite needed, just be aware it's not adding information.

## 11. Deletable lines
- **NIT** — *"They drew a lot of attention, and..."* (ch.6) — "drew a lot of attention" does no argumentative work; cut to *"Projects like AutoGPT ran models in loops like this one, and often got stuck going round in circles."*
- **SHOULD FIX** — *"Its developers have said that worked better than building an index of the code in advance."* (ch.6) — deletable as-is per #4/#9; either cut or set up properly.

## 12. Hard-to-follow sentences / rushed or padded beats
- **SHOULD FIX** — Quote: *"That's five words to keep. The LLM predicts the next word. The context is all it sees. A tool is something the harness does when the model asks. The harness runs the tools and the loop. And together, the LLM and the harness are the agent."* Five definitions in one unbroken breath, at the video's emotional high point, while the screen simultaneously prints the same five lines — doubled load, likely to feel rushed on delivery. **Rewrite:** split across two breaths with a pause where the equation lands: *"Five words. The LLM predicts the next word. The context is all it sees. [beat] A tool is something the harness does when it's asked. The harness runs the tools and the loop. [beat] LLM plus harness: that's the agent."*
- **NIT** — ch.6 is the densest chapter (a historical example + two probability results + three causal factors) versus every other chapter's single-idea focus. Not blocking given the strong visual scaffolding described, but worth a pacing check in edit — consider whether AutoGPT and the math need to share a breath or could get one more beat of space.
- **NIT** — *"Text on its own doesn't do anything. So agree on a format for requests..."* — "agree on" has no stated agent (agree — who?). Minor spoken-clarity wobble. **Rewrite:** *"So the model and the program need a shared format for requests."*

---

VERDICT: PASS
