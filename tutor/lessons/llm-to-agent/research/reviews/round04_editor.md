# Script Review

## 1. Opening question → ending callback
**Pass.** Ch1 asks "How do you get from a model that writes text, to an agent that fixes a bug?" and Ch8 opens with the near-identical "how do you get from a model that only writes text to an agent that fixes a bug?" — reinforced visually (the dashed "?" box from Ch1 returns filled with "harness"). Clean, deliberate callback. No finding.

## 2. One-sentence-per-segment chain, "and then" count
Reconstructing the chain from the actual script (not the author's own summary) confirms it holds:
1. Q: ChatGPT (2022) only talked; agents now act using the same text-only model — what's in between?
2. Therefore: the model just predicts the next word from its context, so it only outputs text and only knows its context.
3. But text alone doesn't act (bare model writes a command nobody runs) — therefore add a program + request format.
4. But the model can't see results (fact 2) — therefore paste results back and rerun (2023 web search = same trick).
5. But one step won't fix a bug — therefore loop until no request = agent; a real run took 12 steps, redirected by a failing test.
6. But why did 2023 agents stall — because small errors compound (95%→~1/3 over 20 steps) — therefore: loop-trained models (99%→~4/5), feedback, step-by-step search.
7. Therefore: LLM = model, rest = harness; agent = LLM + harness.
8. Therefore, back to the question: same model, harness turns text into action, loop turns steps into a job.

**"And then" count: 0.** Every joint is "but" or "therefore." No finding.

## 3. Ideas announced vs. derived
- **SHOULD FIX** — *"Its developers first tried building an index of the code in advance. But code keeps changing, and an index goes out of date. They've said searching worked better."* This is asserted on authority, not shown failing like every other claim in the video (contrast with Ch3's bare-model demo, which *shows* the wrong intuition breaking). Rewrite: cut to one line that doesn't claim a demonstrated fact — *"Claude Code's own team tried indexing the code ahead of time first, and moved to searching instead."* — or add a one-beat visual of a stale index actually causing a miss.
- **NIT** — Permission checks and context trimming (Ch7: *"A real harness does two more things"*) are appended as facts rather than problems solved. Low stakes since it's explicitly framed as a short addendum, not a core beat.

## 4. Setups without payoffs / payoffs without setups
- **SHOULD FIX** — The Ch5 replay includes *"edit file: prices.py, tagged 'no real change' (it only added blank lines; not narrated)"*. A visible, unexplained wasted step in the middle of the hero example risks a puzzled "wait, why did it do that?" from an attentive viewer, right in the video's centerpiece sequence. Either cut this beat from the replay or give it one clause: *"one edit did nothing — even real runs have dead ends."*
- **SHOULD FIX** — Ch3 tags the model *"a large model (Claude)"*; Ch6 later says *"Claude Code, a coding agent, works that way"* and implies the 12-step demo run exemplifies this. But the demo was never labeled as Claude Code specifically — only "Claude." A viewer may assume the whole video's running example *is* Claude Code, then feel the rug pulled when Claude Code is introduced as if new in Ch6. Rewrite: tag the demo agent clearly in Ch3 (e.g., "a large model, running inside a harness like Claude Code") so Ch6's reference is a payoff, not a fresh introduction.
- **NIT** — Ch7's permission-check gate is introduced with no setup; the Ch5 replay showed every edit landing instantly. Not damaging, but a sharp viewer may ask why the replay never paused for permission.

## 5. Terms before explanation / concepts with two names
- **SHOULD FIX** — "Program" (from Ch3 on) and "harness" (Ch7) risk reading as the same box renamed rather than part-to-whole. The script does state the relationship (*"It holds the tools, and the program that carries out each request, and it runs the loop"*), but it arrives after four chapters of calling the box simply "the program." Add one explicit line at the top of Ch7: *"That program you've been watching? It's one part of something bigger: the harness."* This turns a potential renaming-confusion into a clean zoom-out.
- No other term is used before being explained; "LLM," "context," "tool," "agent," and "harness" are each defined at or near first use. Good discipline.

## 6. Numbers: full list, 2–3 to remember, dead numbers
Full list: late 2022; tea 31%, coffee 19%, soup/the/this (background only); "and" 18%, "I" 8%; $37 vs $39.50 (Ben); discount at 10 vs 11 items; twelve requests; 95% and ~1/3 (36/100); 99% and ~4/5 (82/100); twenty steps; a hundred runs; five words.
**Worth remembering:** (1) *tea 31%* — the mechanism itself; (2) *twelve requests* — scale of unsupervised action; (3) *95%→~1/3 vs 99%→~4/5* — the whole "why now" argument in two numbers.
**Numbers doing no real work:** coffee 19% and the three background bars (soup/the/this) are visual-only clutter around the one number that matters (tea). **NIT** — fine as texture, but consider dimming/shrinking them further so "31%" is unmistakably the takeaway, not one of five competing figures.

## 7. Abstraction before the concrete case
**SHOULD FIX** — Ch5 states the abstract loop definition (*"repeat... until the model replies with no request... that is an agent"*) as a compact rule before showing the full concrete 12-step run. Elsewhere the video rigorously earns abstraction from something just shown (Ch2: tea example → "two facts"; Ch3: bare-model failure → program). Here the definition is stated first and only then illustrated at length. Fix: front-load one more clause of concreteness before naming it, e.g. *"Search, then open — two steps already. Do that again and again until the model has nothing left to ask for. That's the whole loop. Here's what a real one looks like: twelve of those steps, back to back."* Minor since it's immediately grounded, but worth tightening given the rest of the script's discipline.

## 8. Wrong intuition — confronted and shown failing?
**Pass.** *"You might picture the model reaching into the files itself... it wrote that it would explore the project, and even wrote out a request to run a command. But nothing was there to carry it out, and the tests still failed."* Directly names the wrong model and shows it failing on screen. No finding.

## 9. Examples named but not understood
No violations found. Ben's bill, the Gadget/gadget bug, the bulk-discount threshold, 2023 web search, and Claude Code's search-vs-index choice are all given at least one sentence of causal explanation, not just named.

## 10. On-screen text repeating narration / pictures not supporting the line
- **SHOULD FIX** — Ch4's *"2023 · chat assistants"* inset is explicitly generic (*"Generic labels, not a real transcript"*) while every other example in the video (Ben's bill, the Gadget bug, the 95/99% math) is drawn from a real captured run or real data file. Nothing on screen signals this one inset is illustrative rather than real, which is an inconsistent evidentiary standard right after the video has trained viewers to trust its on-screen text as literal. Add a small "illustrative" tag, or replace with a real captured example.
- **NIT** — The "12 requests" on-screen counter/callout at the end of Ch5 exactly doubles the spoken line *"That was twelve requests."* Harmless as a graphic emphasis, but could instead show something the line doesn't say (e.g., wall-clock time, or how many were "wasted") to add information rather than mirror it.

## 11. Deletable lines
- **NIT** — *"Real agents use a stricter format, but the idea is the same."* (Ch3) is a hedge for technical viewers; could be cut with no loss for the target audience, though it does preempt an objection, so low priority.
- No other lines found to be pure filler — the script is unusually tight; most sentences carry setup, payoff, or a needed number.

## 12. Hard-to-say-aloud sentences / rushed or padded beats
- **SHOULD FIX** — *"Say each step goes right ninety-five times in a hundred, whatever happened before, and nothing catches a mistake."* Two trailing qualifying clauses stacked after the main clause are hard to parse by ear. Rewrite: *"Say each step goes right ninety-five times in a hundred — and say that's true no matter what happened before, with nothing to catch a mistake."*
- **SHOULD FIX** — Chapter 6 is the densest beat in the video (two twenty-dot compounding rows, three numbered diagram markers, a Claude Code anecdote, three explanatory claims) but has the least narration per idea of any chapter. Given "no length target," this is the one place worth slowing down rather than compressing — consider splitting the compounding-math payoff from the "three things changed" list into two beats so neither is rushed.
- **NIT** — *"So ask a model on its own to fix it: not the small one, but a large model, like the ones behind chat assistants."* The colon plus a "not X, but Y, like Z" chain is a little tangled for read-aloud delivery. Rewrite: *"So let's ask a model to fix it on its own — not the small one this time, but a large model, like the ones behind chat assistants."*

---

VERDICT: PASS
