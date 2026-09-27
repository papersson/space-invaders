# Frame Review: "From LLM to Agent"

Reviewed all 125 sentence frames across chapters 1–8 against `timings.json`, `script.md`'s screen directions, and the evidence table, cross-checked with `data/next_word.json`, `data/compound.json`, and `data/screen_code_check.txt`.

## MUST FIX

**s3_03** (t=114.1, "You might picture the model reaching into the files itself.") — The project panel (the four file chips `invoice.py`/`prices.py`/`orders.csv`/`test_invoice.py` and the red `tests: fail` badge) is completely absent from the frame. This is exactly the sentence that talks about "the files" — the one moment they most need to be on screen — yet they're missing. Compare to s3_02 and s3_04, where the same panel is present. **Fix:** keep the project panel visible continuously through chapter 3 (it should never be dropped once introduced in s3_01).

**s3_07** (t=136.3, "Text on its own doesn't do anything.") — Same bug recurs: the project panel and badge vanish again here, then reappear at s3_08 when the "program" box arrives. Nothing in the narration calls for hiding it, and the flicker (present → absent → present) reads as a rendering glitch rather than a deliberate cut. **Fix:** same as above — make the project panel a persistent element from s3_01 onward, or if it's a state used only for a transition, apply it deliberately instead of dropping out for one frame.

## SHOULD FIX

**s3_05 / s3_06** (t=127.2–131.7, "In one try, it wrote that it would explore the project...") — The bare-attempt model output ("I'll start by exploring the project structure to find the relevant code." / "Tool: bash · find … -type f …") is rendered in neutral grey/white, not the blue used everywhere else for "the model and what it writes" (e.g. the real request "search: no price for" in blue at s3_13, s4_09, s8_04). Since grey is later established as meaning "the model's final answer with no request in it" (chapter 5), reusing it here for a different kind of model output blurs the color key. **Fix:** render this text in blue (optionally with a distinct border/tag like "failed attempt" to mark it as inert) rather than a different hue.

**s5_23 / s5_24** (t=320.9–323.2, "That was twelve requests.") — The screen direction calls for outlining the twelve blue request cards together with a "12 requests" label. In the rendered frames, only the two currently-visible request lines ("edit file: invoice.py", "run tests") get an outline — the rest are already scrolled into the shrunk/illegible history strip — and no "12 requests" text callout appears; the only cue is the counter in the header, which has read "12" since s5_20 and isn't freshly tied to this line. The specific number the narration calls out isn't visually reinforced. **Fix:** add an explicit "12 requests" annotation (or briefly re-expand/highlight all twelve) when this sentence plays.

## NIT

- **s7_10** — The equation "agent = LLM + harness" appears at the top of the frame; the script calls for it "at the bottom." No factual issue, just a staging deviation.
- **s8_06–s8_08** — The chapter-1 recap diagram fills nearly the whole frame; the script says it should return "small at the top left." Likely an intentional choice for the ending beat, but it doesn't match the spec.
- **s7_04** ("The harness writes the starting instructions...") — No distinct new callout appears for "starting instructions" beyond the pre-existing generic "instructions" header used since chapter 3. Minor since the audience already understands that card by this point.

FRAMES: FIX
