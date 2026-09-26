# Review

## Test 1 — Opening question / closing answer
Pass. Ch1 ends on a single, sharp question ("What is an LLM agent, that taking away one tool leaves it sure of something false?"). Ch9 opens by restating it almost verbatim ("So why did one missing tool leave run B sure of something false?") before answering. Clean callback, no finding.

## Test 2 — Segment chain, connector audit
The author's own Chain (9 items) uses only "But"/"Therefore" — I count zero "and then" occurrences. That's a pass on the connector-discipline test; every step reads as a consequence or a complication of the one before it, never a mere sequel.

## Test 3 — Ideas announced vs. derived
Mostly derived (ch2→ch3→ch4 each grows out of the previous step's visible failure — text that doesn't run, a tool call that isn't answered). One soft spot, folded into the Test 9 finding below: ch8's three closing concepts (superlinear cost, context rot, compaction) are asserted with citations rather than derived from something the video shows breaking.

## Test 4 — Setups/payoffs
Well matched overall (ground truth → reused ch7/9; "3 of 3" → reused ch7; the unexplained card colors in ch1 → named in ch9; ch3's "model never executes" → paid off in ch7's "chapter three again"). One payoff arrives without a real setup — see Finding 1.

## Test 5 — Terms before explanation / duplicate names
Terms are consistently defined at first use (context, tool call, ground truth, workflow, compounding errors, context rot, compaction — all named right after being shown, not before). One minor double-naming:

**NIT** — *"It's the world's answer, not the model's guess: what Anthropic's guide to agents calls ground truth."* Two labels for one idea in one breath. Rewrite: "not the model's guess, but what Anthropic's guide to agents calls ground truth: the world's actual answer" — makes clear which term to keep.

## Test 6 — Numbers
Full list: 1,423 / 2,745 / 18,537 (run A tokens); 9 calls; "3 of 3"; 20 (call cap); 11,597 / 123,192 (Claude Code); ~1,180 / ~240 (screen-only split); U+FEFF.

Worth remembering: **18,537** (cost, in tokens, of a two-line fix), **11,597 → 123,192** (Claude Code's growth over 9 calls), **3-of-3** (this is reproducible, not luck).

**SHOULD FIX** — *"Stop when it replies without a tool call, or after twenty calls, in case it never does."* No run in the video comes close to 20 (9, ~5, 9). The number is introduced and never referenced again. Rewrite: cut it ("Stop when it replies without a tool call") or de-number it ("...or after too many calls, in case it never does") so no dead number lands in the viewer's memory.

## Test 7 — Abstraction before the concrete case
No violations. The model→tool→loop buildup is scrupulously bottom-up, each abstraction introduced only after its concrete failure is shown (bare model can't act → one tool call isn't enough → loop).

## Test 8 — Wrong intuition, shown failing
The stated wrong model ("remembers what it's done and knows when it's succeeded") is explicitly named and refuted twice: ch6 ("It looks as if the model worked through the problem, remembering what it had tried. It didn't.") and ch7 ("It looks as if the model knew it had succeeded. It didn't."), each backed by a concrete run. Strong, no finding.

## Test 9 — Examples named but not understood
**SHOULD FIX** — Ch8 lands three concepts in quick succession — superlinear reading cost, context rot, compaction — and two of them are explicitly flagged on-screen as unshown ("Our runs are far too short to show it"; compaction's visual is "a picture of the idea, not a run"). Coming right before the finale, this risks the ending feeling like cited caveats rather than resolved argument, in a script that otherwise earns every concept through a run. 

Rewrite direction: cut "context rot" to a citation-free gesture your own footage supports ("past a certain size that reading gets less reliable too") or drop it, and fold compaction into a direct callback to run B rather than a new unshown mechanism: *"...production agents summarize a long context to keep it in check — but that's the same gap as run B, just moved one level up: whatever the summary drops, the model no longer knows it."*

## Test 10 — On-screen text vs. narration, picture support
Generally strong — screen text mostly adds information (token splits, citations, "scripted (not run)" tags) rather than repeating lines. One conventional exception:

**NIT** — The ch9 end card showing "the takeaway" risks displaying the same sentence that's simultaneously spoken. Rewrite: show only the compressed half-sentence ("Ask what would have told it that it was wrong") on the card while narration carries the fuller thought.

## Test 11 — Deletable lines
Script is tight; few true deletions found beyond the 20-calls clause (Finding above).

**NIT** — *"It replies with text, of course."* — "of course" is a throwaway beat. Cut to "It replies with text."

## Test 12 — Hard-to-follow sentences / pacing
**NIT** — *"Each new call re-reads everything before it, so twice the calls means more than twice the reading."* Vague relative claim ("more than twice"), hard to picture aloud, in a script that otherwise favors concrete anchors. Rewrite by anchoring to numbers already on screen rather than a new abstract ratio, e.g.: "so the last call already reads twice what the first one added — and a run twice as long reads far more than twice the total."

Pacing: chapters 1–7 are unhurried and well-matched to their content; **chapter 8 is comparatively rushed** — three distinct ideas in under ten sentences, which is likely *why* they end up asserted rather than demonstrated (same root cause as the Test 9 finding). Recommend either slowing ch8 down to properly earn one of the three ideas, or cutting to two.

---

## Summary of concrete findings

1. **SHOULD FIX** — Ch8's cluster of named-but-unshown concepts (context rot, compaction) lands too fast right before the finale; ground each in the video's own evidence or cut.
2. **SHOULD FIX** — The 20-call cap is a number that does no work; cut it or de-number it.
3. **NIT** — "the world's answer" / "ground truth" double-naming in one sentence.
4. **NIT** — Vague "more than twice the reading" claim; anchor to an already-shown number.
5. **NIT** — End card risks repeating narration verbatim; show the compressed half-line only.
6. **NIT** — "of course" filler in ch2.

None of these threaten the spine of the piece — the opening question is answered and called back cleanly, the wrong intuition is named and shown failing twice, and the core mechanism (ground truth entering or failing to enter the context) is demonstrated rather than asserted throughout chapters 1–7.

**VERDICT: PASS**
