# Review

Overall this is an unusually well‑sourced script — the arithmetic checks out throughout (I independently recomputed 0.95²⁰ ≈ 0.3585 and 0.99²⁰ ≈ 0.8179, both match the stated figures), the GPT‑2 percentages match the cited data file, the 12‑request replay is internally consistent with `run_1.json`, and the hedging around the illustrative compounding math and the Claude Code search‑vs‑index claim is careful. I did not find anything I'd call flatly wrong. Below are the precision/completeness issues I'd still want fixed.

---

**SHOULD FIX** — "*Three things changed.*"
This reads as a closed, exhaustive causal account. The three factors given (training for tool use, feedback from tests, search instead of indexing) are real and well-sourced, but they aren't the complete story of why agentic coding got reliable circa 2024–25 — general model capability gains, longer context windows, and cheaper/faster inference (allowing many steps per task) all mattered too and aren't mentioned. As written it slightly overstates completeness.
Corrected wording: *"Here are three big things that changed"* or *"Three things that mattered:"* — signals a partial list rather than a full explanation.

**SHOULD FIX** — Evidence table, Ben's total: *"test_invoice.py expects Ada 20.00 and Ben 37.00 (2 × 7.25 + 10 × 2.50 less 10%)"*
This formula is arithmetically misleading if applied literally: 2×7.25 + 10×2.50 = 39.50, and 39.50 less 10% = 35.55, not 37.00. The actual invoice logic (per the script and code description) applies the bulk discount only to the 10‑unit line, i.e. 2×7.25 + (10×2.50)×0.9 = 14.50 + 22.50 = 37.00. The numbers actually spoken in the script ("thirty‑seven," "thirty‑nine fifty," "eleven items," "should start at ten") are all correct — but if whoever builds the on-screen diff/callout art trusts this formula note verbatim, they'll draw the wrong math.
Corrected wording: *"(2 × 7.25, plus 10 × 2.50 with 10% off just that line)"*

**NIT** — "*Everything around it is called the harness.*"
Presented as the settled term of art. It's accurate for Anthropic/Claude Code's own vocabulary (correctly cited), but other parts of the field use "scaffold"/"scaffolding" or "agent framework" for the same layer. Not wrong, just narrower than "the" name.
Corrected wording (optional aside): *"— some people call this a 'scaffold' instead —"*

**NIT** — "*it predicts the next word, or sometimes a piece of a word*"
Good simplification for this audience, but the standard term "token" never appears anywhere in the script, including the glossary. Since viewers who go on to read anything else about LLMs will hit "token" immediately, one aside would future-proof this without adding jargon burden.
Corrected wording: *"...or sometimes just a piece of a word — that piece is called a token."*

**NIT** — "*that's about thirty-six of the hundred. About a third.*"
35.85% rounds fine to "about thirty-six," but calling that "about a third" (33.3%) is a bit generous — it's closer to "over a third." Low stakes given this is explicitly a hypothetical illustration, not a measurement.
Corrected wording: *"...about thirty-six of the hundred — just over a third."*

---

No canonicity or terminology problems in the LLM/context/tool/agent definitions, no misrepresentation of ChatGPT's 2022 launch or the 2023 web-search/AutoGPT history, and the "same model, resent whole context each call, no persistent memory" mechanic — the trickiest thing to get right in this kind of explainer — is stated correctly and unambiguously in both narration and visuals.

VERDICT: PASS
