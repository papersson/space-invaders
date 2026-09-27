Here's my run-through, staying in the reviewer role.

## (1) Where I'd lose the thread

- **"Pick a likely word, add it to the text, and predict again"** — likely by what rule? Does it always take the top probability (tea, 31%), or sometimes pick something lower down? The example conveniently always shows the top word chosen ("tea", "and", "I"), so I can't tell if that's a rule or a coincidence.
- **"a small open model (GPT-2)"** — "open" isn't explained. Open-source? Open-weights? I can guess from context but it's never defined.
- **"Then twenty steps in a row all go right only about a third of the time."** — this is the big one. I'm told each step is 95% reliable, and then suddenly 20 steps in a row drops to ~36%. The jump from "95% per step" to "36% for 20 steps" assumes I know you multiply probabilities together, and that the steps are independent — a word that appears only as small on-screen text ("if each step is independent and no mistake is caught"), never spoken. I don't have a strong enough grip on probability to derive 0.95²⁰ myself, so this lands as an assertion, not something I followed.
- **"At ninety-nine percent a step, the same twenty steps all go right about four times in five."** — same issue repeats; if I didn't follow the first compounding claim, this one doesn't help me catch up, it just restates the pattern with different numbers.
- **"Its developers have said that worked better than building an index of the code in advance."** — brief, but it's a claim about a comparison ("index" vs. "search step by step") I'm given no detail on — I'll take it on faith rather than understand it.

Everything else — LLM, context, tool, program, loop, harness — is introduced and then reinforced with the recurring diagram, so those landed fine.

## (2) Questions I'd ask afterward

- Why does 95% reliability per step turn into only ~36% over 20 steps — what's the actual math, and what does "independent" mean here?
- When the model writes a request line, does the harness require exact formatting ("search: ...")? What happens if the model writes it slightly wrong?
- How does the harness decide *when* the context is "full" and what actually gets summarized versus dropped?
- Is "12 requests" typical for a bug fix, or could a harder bug take 50? Is there a limit?
- Does the model always pick the single most likely next word, or is there randomness in the choice?

## (3) What I learned (written without looking back)

ChatGPT in 2022 could only produce text in reply to text. An "LLM" just predicts the next word repeatedly, based only on the text in front of it — its "context" — with no memory between runs. To make it act, you define a text format for requests (like "search: ..."), and a separate program — the "harness" — watches for these requests, actually performs them (searching, opening files, editing, running tests), and pastes the result back into the context. Then the whole context is fed to the model again, and it continues. Repeating this is a "loop," and it stops when the model replies without issuing a new request. An "agent" is just this loop: LLM plus harness. Real harnesses also check permissions and trim the context when it gets too big.

## (4) Main idea / numbers / question and answer

- **Main idea**: An agent isn't a smarter model — it's the same text-predicting LLM wrapped in a "harness" that turns some of its output into real actions and feeds the results back in a loop.
- **Numbers I remember**: tea 31% / coffee 19% (next-word prediction example); 12 requests to fix the shop's billing bug; the 95%→36% and 99%→82% reliability-over-20-steps figures (though I couldn't reproduce how they got there).
- **Starting question**: "How do you get from a model that writes text, to an agent that fixes a bug?"
- **Answer given**: The harness — a program that reads the model's text, carries out the parts that are requests, and puts the results back in, in a loop.

## (5) Ratings

- **Want-the-answer pull from the opening**: 4/5 — the bug-fixing demo up front was a concrete, compelling hook.
- **How often I felt lost**: a few times — mainly the two probability-compounding claims in section 6; the rest of the script built up its vocabulary carefully enough that I could follow it.
