# Review

## BLOCKING

**Quote:** "Give a small, freely available model the words 'I made a cup of'." (Ch. 2, paired with the on-screen label "a small, freely available model (GPT-2)") followed later by, with no acknowledgment of a switch, "Here's a task... So ask a model on its own to fix it." (Ch. 3), and every subsequent reference to "the model" through Ch. 5–8.

**What's wrong:** The evidence table confirms Ch. 2's demo runs on GPT-2 (124M parameters, 2019, not instruction-tuned), while the agent demo in Ch. 3–5 runs on a current Claude model. The script never tells the viewer this is a different, vastly more capable model — the narration just keeps saying "the model" as if it's the same character throughout. A 124M-parameter base GPT-2 model cannot follow a request-format system prompt, search a codebase, or fix a bug; if a lay viewer walks away believing the toy model that predicted "tea" is the one later reading files and editing code, the video has taught something false. This also undercuts Ch. 6's own argument — that training improvements were one of three reasons agents started working — since nothing earlier established that a categorically stronger model was needed at all.

**Fix:** Add one explicit sentence at the start of Ch. 3, e.g.: "From here on we'll watch a current, much larger model — the toy model was only to show the mechanism." Or, cheaper: change the Ch. 2 on-screen label to something like "a small model, just to see the mechanism (GPT-2, 2019)" and open Ch. 3 with an on-screen label naming/dating the model actually used, so the two are visibly not the same entity.

## SHOULD FIX

**Quote:** "And a context has a size limit. When it fills up, the harness trims it, for example by summarizing older steps." (Ch. 7)

**What's wrong:** Two issues. (1) The standard, canonical term for this is "context window" — the script discusses the concept at length (Ch. 2's "context," Ch. 7's size limit) but never once names it, which is odd given it happily introduces other jargon (harness, tool, agent). (2) Per the cited source (Claude Code docs), the harness's actual first move is clearing/dropping older tool outputs, with summarization as the fallback "if needed" — the script picks summarization as its sole example, which is the secondary mechanism, not the primary one.

**Fix:** "And a context — its context window — has a size limit. When it fills up, the harness trims it: first by dropping old tool outputs, then, if it still needs to, by summarizing older steps."

## NIT

**Quote:** "It's called an LLM, a large language model, and it does one thing: it predicts the next word, or sometimes a piece of a word." (Ch. 2)

**What's wrong:** The standard term here is "token," which every cited source (GPT-2 paper, Anthropic docs) uses. The script defines "context," "tool," "harness," and "agent" as vocabulary but conspicuously avoids this one, even though "word, or sometimes a piece of a word" is literally describing tokenization. Not wrong, just an inconsistent choice given the lesson's own five-word glossary ambition.

**Fix (optional):** "...it predicts the next token — usually a word, sometimes a piece of one." Then it could sit as a sixth glossary word or at least be named once so viewers who later encounter "tokens" elsewhere aren't stranded.

---

Everything else checked out: the GPT-2 probabilities and rounding (tea 31%, coffee 19%, "and" 18%, "I" 8%) match `data/next_word.json`; the compounding-probability arithmetic (0.95²≈90%, 0.95²⁰≈36%, 0.99²⁰≈82%) is correct and properly caveated on-screen as illustrative, not measured; the 12-request replayed run matches `captures/run_1.json`/`data/runs.txt` step-for-step, including Ben's bill ($39.50 vs. $37.00) and the off-by-one bulk-discount threshold; the "harness" and "agent = LLM + harness" framing is drawn directly and correctly from the Claude Code docs and Anthropic's "Building effective agents"; the AutoGPT/2023 and Claude Code indexing-vs-search claims are accurately and appropriately hedged against their cited sources; and the reference list is canonical for this topic.

VERDICT: REVISE
