Playing the reviewer role, going through in order:

## (1) Where I'd lose the thread

- **"or sometimes a piece of a word"** (§2) — introduces a new idea (sub-word chunks) in passing and never comes back to it. I don't know what a "piece of a word" is technically, and it's never used again, so I'm left wondering if I missed something important.
- **"Pick a likely word, here the likeliest, add it to the text, and predict again: 'tea', then 'and', then 'I'. Over and over, one word at a time."** (§2) — three actions (pick, add, predict) plus three example words land in one breath. On a single listen I'd need a beat to realize "tea," "and," "I" are three separate rounds of the same loop, not one step.
- **"Of those, about ninety get the second step right too."** (§6) — this is the moment I'd actually get lost. It just states the number; it never says "multiply 95% by 95%" or explains *why* the successes shrink like that. I can follow that mistakes "add up," but the mechanism (each step's success depending only on itself, and probabilities compounding) is never spelled out loud — I'd have to reverse-engineer it from the numbers on screen.
- The independence caveat — *"assuming each step's chance is the same whatever came before, and no mistake is caught"* — is described as tiny on-screen text, not something the narrator says. If I'm listening more than reading, I'd miss the one line that would have explained the math I was just confused by.
- **"Then about eighty-two of the hundred runs get all twenty steps right: about four in five."** (§6) — same issue repeated with 99%. Since I never got the multiplication rule the first time, this second number lands just as unexplained as the first.
- **"And since a context has a size limit, it trims the context when it fills up..."** (§7) — "since a context has a size limit" is stated as an established fact, but nothing earlier told me the context has a limit at all. It's a new premise smuggled into a dependent clause.

## (2) Questions I'd ask afterward

- Why does getting one step right make the *next* step more likely to be right too — is it just multiplication, or something more?
- Is 95%/99% "per step" a real measured number, or a made-up illustration?
- Why does the context have a size limit in the first place — is that a cost thing, a memory thing?
- When the harness "summarizes older steps," who or what does the summarizing — another model call?
- Is "piece of a word" something I need to understand, or is "word" close enough for how this all works?

## (3) What I learned (written without looking back)

ChatGPT in 2022 could only produce text — it had no way to act. An LLM just predicts the next word based on the text in front of it (called its "context"), and it forgets everything between uses. To make an agent, you put a program (a "harness") next to the model that watches for special request lines like "search:" or "open file:", carries them out, and pastes the result back into the context so the model can keep going. Repeating that — request, action, result, request again — is the "loop," and a model doing this is an "agent." Agents only started working well recently because models got trained specifically to work this way, tasks like coding give feedback (failing tests), and searching step-by-step beats using a stale prebuilt index. So: agent = LLM + harness.

## (4)

- **Main idea:** An agent is just an LLM (which only outputs text) plus a "harness" — a program that turns certain text into real actions and feeds the results back into the model's context, in a loop.
- **Numbers I remember:** 31% and 19% (probabilities for "tea" and "coffee" as next-word guesses); 95% vs 99% per-step accuracy, leading to roughly 1-in-3 vs 4-in-5 success after 20 steps; twelve total requests in the demo run; the bill amounts $37 vs $39.50 that exposed the second bug.
- **Question it started with:** How do you get from a model that only writes text (ChatGPT, 2022) to an agent that can fix a bug by reading files and running tests?
- **Its answer:** The model itself never changes — it still just predicts text. The harness is what's new: it interprets the model's text as requests, executes them, and loops the results back in.

## (5)

- **Want-the-answer rating (opening):** 4/5 — the side-by-side "2022 chat / today's agent" framing with the dashed "?" box made me want to know what fills that gap.
- **How often I felt lost:** A few times — mainly during the probability-compounding section (§6), where numbers appeared without the underlying rule being stated aloud.
