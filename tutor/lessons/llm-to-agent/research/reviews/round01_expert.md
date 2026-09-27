Reviewed against the evidence table and my own domain knowledge (web verification wasn't available in this session, so a few secondary citations are flagged as unverified rather than confirmed). Overall the script is careful and unusually well-sourced for a pop explainer — no outright factual or arithmetic errors survive scrutiny — but several precision and generalization issues would bother a professor reading closely.

## Findings

**SHOULD FIX** — "It's called an LLM, a large language model, and it does one thing: it predicts the next word." (repeated in Ch. 2, Ch. 8, and the glossary card: "LLM · predicts the next word")
The canonical unit an LLM predicts is a *token*, not a word — many tokens are sub-word pieces (byte-pair-encoding fragments), and this matters for anyone who goes on to read a tokenizer's output. The script never says "token" once, even in the glossary that's meant to nail down precise terms. The specific example ("tea", "coffee", "and", "I") is honestly chosen so token = word here, which is good practice, but the general statement "predicts the next word" is stated as an unqualified definition, not as a simplification of "token." Fix: add one clarifying clause the first time, e.g. "it predicts the next *token* — usually a word, sometimes a piece of one — we'll just say 'word'," and keep "word" thereafter. Minimal cost, closes the gap.

**SHOULD FIX** — "At ninety-nine percent a step, the same twenty steps all go right about four times in five."
This sentence directly follows a claim backed by real citations ("models were trained to work in this loop"), and 99% is never explicitly re-marked as hypothetical the way the 95% figure was ("Say each step goes right..."). A viewer could easily read this as "trained models now measurably succeed 99% of the time per step," which nobody has actually measured or claimed anywhere in the evidence. Fix: keep the hypothetical framing explicit on the second pass too, e.g. "Suppose training gets that to ninety-nine in a hundred — then the same twenty steps..." and make sure the "if independent, and no mistake is caught" caveat is visibly present on screen for the 99% row too, not just the 95% row.

**SHOULD FIX** — "Ask a model on its own to fix it, and it even writes out a command to explore the project. But nothing runs the command, and the tests still fail."
Per the evidence table this is drawn from a single call (`bare_1.json`, "one call"). The main agent demo is honestly hedged elsewhere with "3 of 3 passed," but this baseline claim is presented with the same flat confidence as if it were the model's typical behavior, from one sample. Fix: hedge lightly, e.g. "Ask a model on its own, and in this attempt it even writes out a command..." — a one-word change that keeps it honest without breaking the narrative flow.

**SHOULD FIX** — the request-format vocabulary itself ("A line that starts 'search:', then some words. Or 'open file:'...") is never distinguished from how real production systems like Claude Code actually pass tool calls.
Since Claude Code is invoked by name later ("Claude Code works its way around a codebase like that"), a viewer could reasonably conclude that real coding agents literally parse plain-text lines like "search: TEXT" out of the model's reply. In practice, production harnesses use structured tool-calling APIs (the model emits a schema'd function call, e.g. JSON, not a free-text line a program greps for). This script's plain-text protocol is a fine pedagogical stand-in and is disclosed as this video's own construction in the evidence table, but that disclosure never reaches the narration. Fix: one aside is enough, e.g. in Ch. 3 or Ch. 7: "Real systems usually use a stricter format than a text line — but the idea is the same: the model asks, the program listens."

**NIT** — "In 2023, chat assistants started searching the web."
True for mainstream consumer chat products (Bing Chat, Feb 2023), but retrieval-augmented, search-then-answer LLM systems predate this (e.g., WebGPT, Dec 2021). The claim is scoped to "chat assistants," which is defensible, but a professor would want "started" read as "became mainstream in," not "were invented in."

**NIT** — "Everything around it is called the harness" and the term throughout.
"Harness" is Claude Code's own house term (correctly sourced to Claude Code docs), but it isn't yet universal industry vocabulary — other sources say "agent framework," "scaffold," or "orchestrator." Not wrong, just worth knowing it's presented as more standardized than it currently is across the field.

**NIT** — citation "OpenAI, 'Introducing ChatGPT', 30 Nov 2022 (via TechCrunch, 30 Nov 2025)."
The TechCrunch date (2025) three years after the primary source is unusual for a launch citation — plausibly a retrospective/anniversary piece, but worth a final human check before publishing, since I couldn't verify it (no web access in this review pass).

## What's not a problem (checked and clean)
- All percentages (31%, 19%, 1.5%, 1.3%, 1.2%, 17.9%, 7.9%) and both compounding calculations (0.95²⁰≈0.36, 0.99²⁰≈0.82) check out arithmetically against the data files.
- The 12-request replay (search → open → search → open → edit → fail → edit → open → search → open → edit → pass) matches the evidence table step-for-step, including the un-narrated no-op edit — good practice, not cherry-picked.
- Ben's bill arithmetic (39.50 vs. 37.00, the >10 vs. ≥10 bulk-discount bug) is internally consistent with the assertion error text.
- The agent/harness/tool/context definitions track Anthropic's own "Building effective agents" and Claude Code docs framing appropriately scoped to LLM coding agents (not overreaching into general robotics/AI-agent literature).
- GPT-2 parameter count (124,439,808) and framing as "a small open model" are accurate.

VERDICT: PASS
