# Script Review

## 1. Opening question → ending answer, with callback
**PASS.** Opening (Ch.1): *"So what is an LLM agent, that taking away one tool leaves it sure of something false?"* Ending (Ch.9): *"So why did one missing tool leave run B sure of something false? Because an agent is a model that picks each next step from its context..."* — same phrase ("sure of something false") recurs verbatim. Clean callback, no fix needed.

## 2. Chain test (one sentence per segment, joined by but/therefore/and then)
The author's own Chain section already does this cleanly, one step per chapter:
1. Question → 2. Therefore model alone, **but** nothing runs text → 3. Therefore code runs tools, **but** one call isn't enough → 4. Therefore a loop → 5. **But** test fails, therefore model corrects → 6. **But** model remembers nothing → 7. Therefore run B breaks / more-capable model, therefore two failure modes → 8. **But** second failure mode (growth) → 9. Therefore the answer.

**"And then" count: 0.** Every joint is causal (but/therefore), never merely sequential. This is a real strength — flag it as something to protect during any rewrite, since the temptation in editing is to soften a "but" into an "and then" for flow.

## 3. Ideas announced vs. derived
Mostly derived from a shown problem (context → tool call → loop are each forced by the previous chapter's dead end). Two exceptions:
- **NIT** — "compounding errors" (Ch.7) is introduced through a hypothetical ("*If* that guess were one step in a longer task...") rather than a shown case. Honestly hedged with "if," so low severity, but it's the one concept in the video argued rather than demonstrated.
- **SHOULD FIX** — "compaction" (Ch.8) is stated as a general fact about production agents with a screen note admitting *"a picture of the idea, not a run."* Unlike context rot, the narration never verbally flags this as illustrative, so it reads as another observed result when it isn't. See #7/#10 below for the fix.

## 4. Setups without payoffs / payoffs without setups
**BLOCKING** — The third run of "the more capable model" (Ch.7) is a payoff without a home. Narration: *"The third time, it asked for the data file in a format our code didn't recognise. Our loop saw no tool call, and stopped."* This is immediately followed by *"So this is why agents work, and the first way they break down"* — but a parsing mismatch that silently halts the loop is neither "nothing checks the work" nor "the context grows." It's a third, unnamed failure mode, shown but never reconciled with the video's stated two-part taxonomy (Objective 4, restated at the very end of Ch.7's own chain step and in Ch.9). A viewer who's paying attention is left asking "wait, isn't that a third way?" right before the takeaway locks in "two ways."

*Concrete rewrite* — either tie it back explicitly to the model/code boundary established in Ch.3:
> "That's not a new way to fail — it's chapter three again. The model can only ask; when our code doesn't recognize what it's asking for, nothing happens. The loop stops, not because the model was wrong, but because it asked for something we hadn't built."

or, if that beat isn't worth the extra complexity, cut the third run from Ch.7 entirely and keep only the two successful more-capable-model runs, which cleanly support the point being made.

## 5. Terms before explanation / concepts with two names
No blocking issues. "Context" and "memory" are used side by side in Ch.6 ("What the model remembers... the context is its only memory") — but this is the deliberate point (there is no memory, only context), not accidental duplication, so it's fine as is.

## 6. Numbers
All spoken numbers: 3-of-3 (twice), 1,423 / 2,745 / 18,537 (run A tokens), ~1,180 / ~240 (overhead split), 11,597 / 123,192 (Claude Code tokens), nine calls (x2), twenty calls (max_calls cap).

**Worth remembering:** 18,537 vs. 123,192 (the same 9-call task, ~7x the reading — this is the whole "context only grows" payoff) and "3 of 3" (establishes the split isn't noise, which the entire argument leans on).

- **NIT** — "twenty calls" (Ch.4, the max_calls safety cap) is mentioned once and never invoked, referenced, or paid off. It does no narrative work; consider cutting it or replacing with something that matters later (it doesn't need to be dramatized since it never triggers).
- **NIT** — the 1,180/240 overhead split (Ch.6) is more granular than the argument needs; the point ("most of the first call is fixed overhead") doesn't require exact numbers to land.

## 7. Abstraction before concrete case
Mostly fine — the video runs concrete-first throughout (Ch.1's real runs precede all the built-up theory). One exception:

**SHOULD FIX** — Compaction (Ch.8) arrives as a general abstraction with only a staged/schematic visual standing in for a real case, right after a chapter otherwise built entirely from two real captured runs (run A vs. Claude Code). Since the objectives don't actually require explaining compaction in detail (only "whatever the summary drops, the model no longer knows"), consider trimming to that one sentence and dropping the fabricated visual, or explicitly say in narration that it's illustrative rather than observed — matching the honesty of the context-rot line ("our runs are far too short to show it").

## 8. Wrong intuition — shown failing?
**PASS**, well-executed. All three clauses of the stated wrong model are explicitly confronted and shown false:
- "remembers what it has done" → Ch.6: *"It looks as if the model worked through the problem, remembering what it had tried. It didn't."*
- "knows when it has succeeded" → Ch.7: *"It looks as if the model knew it had succeeded. It didn't."*
- "code around it is plumbing" → Ch.7's third more-capable-model run shows code (the loop's parsing) determining the outcome independent of model quality — though see the Test 4 finding above, this beat needs a cleaner landing.

## 9. Examples named but not understood
- **SHOULD FIX** — "a more capable model" (Ch.7) is never named. It's used as real evidence (2 of 3 runs supporting the thesis) but the viewer can't place it, weight it, or look it up. Either name it or give a reason for withholding the name (e.g., "we're not naming it — the point isn't which model, it's the mechanism").
- Everything else named (Claude Code, byte order mark, Anthropic's docs) is explained enough to be understood, not just namedropped.

## 10. On-screen text vs. narration / pictures vs. line
- The verbatim reply cards in Ch.1 (echoing "Fixed... All tests now pass") are evidence, not redundant captioning — fine.
- **SHOULD FIX** — same compaction issue as #3/#7: the screen note *"a picture of the idea, not a run"* is admitted only in the production note, not to the viewer. If the frame looks like all the other captured-run visuals, viewers have no way to tell this one is staged. Either mark it visually as a diagram (different visual register from the real capture strips) or say so in narration.

## 11. Deletable lines
- **NIT** — Ch.3: *"Anthropic's documentation puts it plainly: the model never executes anything on its own."* This restates a point the line right before it already made ("Notice who ran it. Not the model."). Cuttable without losing anything; the citation is better spent at the end-card references, which already lists this source.

## 12. Hard-to-follow sentences / pacing
- **SHOULD FIX** — Ch.6 and Ch.8 both pack dense, multi-layered visuals (a 9-row staircase with shaded splits; a zoom-out comparison plus a second stacked staircase plus a compaction squeeze) against comparatively short narration. Flag both for a timing pass in edit — the sentences read fine on the page, but there's a real risk the visuals need more seconds than the voiceover gives them.
- **NIT** — Ch.9: *"an agent is a model that picks each next step from its context, not from steps written in advance, as a workflow would"* — the trailing "as a workflow would" clause is a bit backloaded for spoken delivery. Consider: *"...picks each next step from its context. A workflow picks its steps in advance; an agent doesn't."*

---

**VERDICT: REVISE**

The one BLOCKING item (Test 4/#7's unresolved third failure mode threatening the "two ways agents break down" takeaway) is a real structural risk to the ending's payoff and should be fixed before this locks. Everything else is SHOULD FIX/NIT polish on an otherwise tightly-argued script — the causal chain, the callback, and the wrong-intuition confrontation are all well executed.
