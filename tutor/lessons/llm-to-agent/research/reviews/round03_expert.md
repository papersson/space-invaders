I reviewed the script against the evidence table line by line — arithmetic, terminology, source attributions, and internal consistency across chapters. Overall it's unusually well-sourced (every number traces to a specific simulation or citation, caveats are attached where the script hedges into hypotheticals). I found no factual errors that rise to BLOCKING. Below are the precision/completeness issues worth fixing before production.

## Findings

**SHOULD FIX — missing the standard term**
Quote: *"It's called an LLM, a large language model, and it does one thing: it predicts the next word, or sometimes a piece of a word."*
The unit is canonically called a **token**, and the script never uses that word anywhere, including the glossary card in chapter 7 (which lists LLM, context, tool, harness, agent but not token). For an audience described as "somewhat technical," who may go on to read about context-window sizes, pricing, or rate limits — all measured in tokens — this is a real gap, not just simplification.
Fix: add one clause, e.g. *"That unit is called a token — usually a word, or a piece of one."* Then the glossary card can optionally carry it too.

**SHOULD FIX — greedy decoding is presented without the caveat that reconciles it with the later demo**
Quote: *"Pick a likely word, here the likeliest, add it to the text, and predict again: 'tea', then 'and', then 'I'."*
This models generation as picking the top-probability token every time (greedy decoding). But the evidence table shows the same agent task run three times with different outcomes (run 1: 12 requests; runs 2–3: 8 requests each) — which only makes sense if the actual model calls involve sampling, not always taking the top choice. The script never states this, so an attentive viewer has no way to reconcile "the model always picks the likeliest word" (ch. 2) with "the same task took a different number of steps each time" (ch. 5/6 evidence, though the variation itself isn't narrated on screen). As written, ch. 2 teaches a mental model that predicts determinism the rest of the video's own data contradicts.
Fix: add a line in chapter 2, e.g. *"It doesn't have to pick the top word every time — it can pick among the likely ones. That's one reason the same task can go a little differently each time you run it."*

**SHOULD FIX — ambiguous phrasing risks flipping the fact**
Quote: *"The model looks at the test and at Ben's orders, and finds a second mistake. The bulk discount starts at eleven items, not ten."*
The intended meaning (confirmed by the code: `quantity > BULK` → `quantity >= BULK`, and by the screen note "discount from 10, not 11") is: the buggy code currently starts the discount at 11 items; it should start at 10. But "X starts at eleven, not ten" is also readable as asserting eleven is the (newly discovered) correct threshold — the opposite of the fix. This is exactly the kind of sentence a professor would want tightened before it airs.
Fix: *"The bulk discount was only kicking in at eleven items — it should start at ten."*

**NIT — the loop's safety valve isn't mentioned where "the loop" is defined**
Quote: *"This goes on until the model writes a reply with no request in it. That's its answer, and the loop stops."*
The actual harness in the demo caps at 20 calls (per the evidence table), and real harnesses always have some iteration/turn/cost limit — this is arguably as much a defining feature of "the harness runs the loop" as permission checks or context-trimming, both of which chapter 7 does mention. Not required, but if chapter 7 is meant to be the complete list of "what a real harness also does," an iteration cap belongs alongside permission checks and trimming.

**NIT — end-card citation is a shorthand, not a title**
Quote: *"Radford et al., GPT-2 (2019)."*
The paper's actual title is "Language Models are Unsupervised Multitask Learners." Fine for a fast-moving end card, but if the other four references get full titles, this one reads inconsistently truncated.

## What checked out (worth noting since I was asked to be exacting)

- All arithmetic verified independently: 0.95²⁰ = 35.85% ("about thirty-six... about a third"), 0.99²⁰ = 81.79% ("about eighty-two... about four in five"), and the intermediate steps (90, 86, 81 / 98, 97) all round correctly.
- GPT-2 probabilities (tea 30.8%→"thirty-one," coffee 19.1%→"nineteen") round correctly.
- Ben's billing arithmetic (2×7.25 + 10×2.50 less 10% = 37.00; buggy total 39.50; difference 2.50) is internally consistent and matches the >BULK vs >=BULK bug exactly.
- Every hedge the numbers need is already present on screen ("95% is an illustration, not a measurement," "assuming each step's chance is the same whatever came before, and no mistake is caught," "Real agents use a stricter format," "Generic labels, not a real transcript").
- The single-run anecdote in chapter 3 ("In one try...") and chapter 5 ("That was twelve requests") are both honestly scoped as single demonstrations, not overgeneralized into universal claims about model or agent behavior.
- "Harness," "tool," "context," "agent" all match their cited primary sources (Claude Code docs, Anthropic's "Building effective agents") without overclaiming universality beyond that framing.
- The claim that Claude Code favors search over pre-built indexing is correctly attributed as a reported engineering choice ("They've said..."), not asserted as a general CS truth.

VERDICT: PASS
