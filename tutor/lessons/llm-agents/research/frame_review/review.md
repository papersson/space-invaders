# Frame Review Findings

I read all 9 chapters' pages (s1–s9) plus sentences.txt, script_and_evidence.md, runs.txt, overhead.txt, and screen_code_check.txt. Overall the frames track the script and evidence tightly — numbers, quoted replies, code lines, and citations all check out against runs.txt/overhead.txt/screen_code_check.txt. Below are the discrepancies I found.

---

**MUST FIX — s8_09 to s8_12: promised "twice the calls" visualization is missing**
What I see: Across four consecutive sentences (s8_09 "a longer task means more reading than its length suggests," s8_10 "twice the calls means more than twice the reading," s8_11 "the reading has a price beyond time," s8_12 "models get worse at recalling what's in it"), the frame is pixel-for-pixel identical to s8_08 — the same Claude Code staircase (11,597→15,620), the same "123,192 tokens read" bracket, the same mini run-A chart.
What's wrong: script_and_evidence.md explicitly calls for "run A's staircase with a second copy of its rows stacked on top, each longer" to illustrate the superlinear-growth claim in s8_10. That visual never appears — the key quantitative argument of the chapter (doubling calls more than doubles reading) is asserted in narration with no supporting image, over a four-sentence stretch.
Fix: add the doubled/stacked staircase (or equivalent growth comparison) so it's visible by s8_10, and give s8_09/s8_11/s8_12 at least a minor visual change (highlight, label) so the frame isn't static across four different claims.

---

**SHOULD FIX — s3_06–s3_08: no visible mechanism linking "our code" to the tool call/result**
What I see: sentence "Our code reads the tool call, runs the tool, and adds its output to the context" (s3_07) shows the blue `list_files` card and green result card on the strip, with "our code" sitting alone above, unconnected by any arrow.
What's wrong: script calls for "an arrow carries it to 'our code', which touches the project; a green card comes back." No arrow is present, so the frame doesn't show *who* ran the tool — the exact point of this sentence — until chapter 4 introduces the loop arrows.
Fix: add the arrow model→our code→project→result for s3_06–s3_08, consistent with the loop diagram used from chapter 4 onward.

**SHOULD FIX — red used for two unrelated meanings**
What I see: a small red dot marks the byte-order-mark on "read csv" cards (chapters 1, 5, 6, 7, 9), separate from the red ✗ used on failing-test result cards.
What's wrong: the established convention is "red = a failing test." Reusing red (even as a dot vs. a cross) for an unrelated, non-failure fact (an invisible character in a successfully-read file) risks a viewer reading the BOM marker as an error indicator, especially in chapter 1 (s1_07 onward) where it appears before chapter 5 ever explains it.
Fix: give the byte-order-mark indicator its own colour (e.g., amber, since it's data/token-related) instead of red, or hold off showing it until chapter 5 introduces it.

**SHOULD FIX — s7_30/s7_31: "our code" annotation lags its sentence by one frame**
What I see: s7_30 ("Our loop saw no tool call, took the reply as final, and stopped") shows only the red "FAIL" tag; the "our code" box with "no tool call found → done" doesn't appear until s7_31 ("That failure wasn't the model's").
What's wrong: the mechanism being described in s7_30 isn't labeled until the next sentence.
Fix: bring the "our code / no tool call found → done" label in one frame earlier, at s7_30.

---

**NIT — s3_02/s3_03: full JSON call syntax shown before narration introduces the JSON format**
The tool-list box already shows complete `{"tool": "write_file", "path": "report.py", "content": "..."}`-style lines at s3_02–03, while the narration at that point only says "list the files, read a file, write a file, and run the tests" — the JSON format isn't explained until s3_04. Consider showing plain tool names first, then revealing the JSON form at s3_04 as scripted.

**NIT — Chapter 8's new teal/cyan bar colour**
The Claude Code staircase (s8_06 on) uses a plain grey+teal bar instead of the grey/blue/green card colours used in chapter 6's staircase for the same kind of token-growth chart. Understandable given Claude Code's context can't be split into our tool-call/result granularity, but it's a seventh colour outside the stated palette — consider using amber (already "tokens read") instead of introducing teal.

**NIT — Inconsistent abridgement of Run B's quoted reply**
Chapter 1 (s1_10) abridges Run B's reply as "Fixed. The bug was that revenue was being computed with `+` … now returns the correct totals…"; chapter 7's "RUN B'S REPLY" callout (s7_09 on) cuts it differently ("Fixed. The bug was that revenue was being computed with `+` instead of `*`\n…\nmatching the expected values…"). Both are faithful to the real quote, just trimmed at different points — align them for consistency.

**NIT — Chapter 9 legend wording**
s9_01 legend labels the blue swatch "the model's writing"; script_and_evidence.md's chapter 9 note specifies "the model's replies." Not wrong, just an unnecessary wording drift at the one place colours are formally named.

---

## Summary
- MUST FIX: 1
- SHOULD FIX: 3
- NIT: 4

**FRAMES: FIX**
