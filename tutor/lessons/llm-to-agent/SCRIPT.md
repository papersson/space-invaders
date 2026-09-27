# From LLM to Agent

Status: revised after round 1, before review round 2

## Argument

**Audience.** Non-technical to somewhat technical people. They remember ChatGPT arriving in late 2022 as "AI", and later noticed that AI started doing things, not only talking. They have not studied how any of it works, and know no programming terms beyond everyday ones ("file", "code", "a bug").

**Question.** In 2022, ChatGPT could only talk. Now AI agents do things: given a bug, one reads the code's files, runs its tests and fixes it. Underneath is the same kind of model, and it only writes text. What sits in between? How do you get from a model that writes text to an agent that fixes a bug?

**Answer.** An LLM predicts the next word from the text in front of it (its context), over and over; what comes out is text, and what it knows about the task is what is in its context. On its own, a model asked to fix the bug writes that it will explore the project and even writes out a command, but nothing runs it. So a program is put beside it: a format for requests is described at the top of the context ("search: ...", "open file: ..."), and when the model writes a request, the program carries it out with one of its tools. The model can't see the result until the program pastes it into its context and runs it again; then it continues with information it could not have had (web search in chat assistants, from 2023, is this step). Repeat until the model replies with no request, and you have an agent: in a real run, the agent searched for the error message, opened files, fixed the lookup, ran the tests, saw them fail on Ben's bill, found the discount mistake, fixed it, and saw them pass, in twelve requests nobody planned in advance. Early loops (2023) mostly failed because small mistakes add up (95% a step gives about one chance in three of twenty clean steps); what changed is models trained to work in the loop (99% a step gives about four in five), tasks with feedback that catches mistakes (the failing test), and agents that search for what they need step by step (as Claude Code does). The LLM is the model; everything around it, the starting instructions, the tools, the program, the loop, permission checks and context trimming, is the harness. The model still only predicts the next word; the harness turns its text into actions and feeds the results back, and the loop turns single steps into a whole job.

**Takeaway.** An agent is an LLM plus a harness. The model only ever writes text; the harness carries out the requests in that text, puts the results back into the model's context, and loops, so single steps add up to a whole job.

**Wrong model.** The AI that does things is a new, smarter kind of AI that acts on its own: the model itself reads the files and runs the tests, and it simply "learned to act".

**Objectives.**
1. Say what an LLM does (predicts the next word from its context, over and over), and the two facts that follow: its output is text, and what it knows about a task is what is in its context.
2. Explain how text becomes an action and how the result reaches the model: an agreed request format, a program that carries out requests with tools, and the result pasted back into the context.
3. Describe the agent loop, and follow a real run of it, including a failing test that changes the next step.
4. Explain why agents took until recently (small mistakes add up; models trained for the loop, feedback, searching step by step), and name the harness's parts: agent = LLM + harness.

## Chain

1. The question: ChatGPT (2022) could only talk; agents now read files, run tests and fix bugs, with the same kind of model underneath, which only writes text. What sits in between?
2. Therefore start with the model: it predicts the next word from its context, over and over ("tea", 31%). Two facts follow: its output is text, and what it knows about the task is what's in its context.
3. But text doesn't do anything: asked on its own to fix the bug, the model writes out a command, and nothing runs it. Therefore agree on a request format and put a program beside the model that carries out requests (tools).
4. But the model can't see the search result (fact two). Therefore the program pastes the result into the context and runs the model again, and the model continues with information it couldn't have had (web search in chat, 2023).
5. But one step won't fix a bug. Therefore repeat until the model replies without a request: a loop, and that is an agent. A real run: twelve requests, a failing test that changes the next step, and a pass.
6. But if the loop is that simple, why did 2023's agents get stuck? Because small mistakes add up (95% a step: about a third of twenty-step runs go clean). Therefore what changed: models trained for the loop (99%: about four in five), feedback that catches mistakes (the failing test), and searching step by step (Claude Code).
7. Therefore name the parts: the LLM is the model, everything around it is the harness; agent = LLM + harness.
8. Therefore the answer: the model still only predicts the next word; the harness turns its text into actions and feeds results back, and the loop turns steps into a job.

Deviations from the canonical progression: both research reports give the same order (next-word prediction, a single tool call, the loop, then refinements), and the script follows it. It uses a plain-text request format ("search: ...") instead of the structured JSON tool calls real products use, as ReAct-style tutorials do, because this audience reads a line of text more easily than JSON; the example agent really used this format. The workflow-versus-agent distinction gets one sentence ("Nobody wrote them down in advance"), since the approved outline keeps everything but the LLM-to-agent path small. Left out on purpose: how a raw model becomes a chat assistant, most of the history, a separate chapter on why coding came first, retrieval beyond one sentence, benchmark numbers, and jargon (tokens, embeddings, RAG, ReAct, function calling). "Next word" stands for "token"; the example's candidates are all whole words, so it is exact there.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1 | Narrated animation | The question is a picture with a gap in it: the same model box in 2022 (text out) and today (actions out), with an empty box between them that chapter 7 fills. |
| 2 | Narrated animation with real numbers | A small open model's real probabilities for the next word, as bars; the words then added one at a time. |
| 3-5 | Narrated animation replaying real runs | One diagram built up piece by piece (context, model, request, program and tools, the result arrow, the loop), and a real agent run replayed through it. |
| 6 | Narrated animation with arithmetic | Twenty steps as a row of dots; the arithmetic on screen as it is said. |
| 7 | Narrated animation | The finished diagram with the harness drawn around it, then a glossary card. |
| 8 | Narrated animation | Payoff, on the same diagram. |
| (not built) | Exercise | Run sims/agent.py on sims/project, change the task or remove the "run tests" tool, and read the context it builds. Writing or running a small loop is the way to feel how it works; offered, not added to the page. |
| (not built) | Reading | Anthropic, "Building effective agents" (2024); Claude Code docs, "How Claude Code works". |

## Ledgers

**Setups and payoffs.**
- The empty box between the model and the actions (ch. 1) is filled by the program (ch. 3), the result arrow (ch. 4) and the loop (ch. 5), and named the harness (ch. 7).
- "It only writes text" (ch. 1) is shown with next-word probabilities (ch. 2), fails visibly with the model on its own (ch. 3), and returns in the answer (ch. 8).
- Fact one, the output is text (ch. 2), is why a request format is needed (ch. 3).
- Fact two, it knows only its context (ch. 2), is why the result must be pasted back (ch. 4), and why the program sends the whole context each time (ch. 4).
- The request format at the top of the context (ch. 3) returns as the starting instructions (ch. 7).
- "Search" as the first tool (ch. 3) returns as searching step by step (ch. 6).
- The program doing the work (ch. 3) is named as part of the harness (ch. 7).
- The failing test on Ben's bill (ch. 5) returns as feedback that catches mistakes (ch. 6).
- "Nobody wrote them down in advance" (ch. 5) returns as "the loop turns single steps into a whole job" (ch. 8).
- "ChatGPT could only talk" (ch. 1) returns as "an agent is still talking" (ch. 8).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| LLM (large language model) | ch. 2 | the model: predicts the next word from the text in front of it |
| context | ch. 2 | the text in front of the model: all it sees |
| tests | ch. 1 | checks that come with the code, and say whether it works |
| request | ch. 3 | a line in the agreed format ("search: ...") |
| tool | ch. 3 | something the program can do for the model when it asks |
| result | ch. 4 | what a tool returns, pasted into the context |
| agent | ch. 5 | a model working in a loop, using tools |
| harness | ch. 7 | everything around the model: starting instructions, tools, the program, the loop, permission checks, context trimming |

The code being fixed is always "the code" or "the project"; "the program" is always the harness's program.

**Numbers to remember.** Ninety-five percent a step over twenty steps: about one in three runs go clean; at ninety-nine percent, about four in five. Supporting: "tea" 31%, "coffee" 19%; twelve requests; Ben's bill 37.00 expected, 39.50 computed.

## Script

Audience for every reviewer: this lesson is made for non-technical to somewhat technical viewers who remember ChatGPT arriving in late 2022, later noticed AI started doing things, and have not studied how it works. Judge it for that audience.

### 1. The question

> In late 2022, ChatGPT arrived. You typed a message, and it wrote back. It could talk, and that was all.
> Now there are AI agents that do things. Give one a bug in some code, and it reads the files, runs the tests that check the code, and fixes the bug.
> Underneath, it's the same kind of model as the one in the chat. And a model like that only writes text.
> So what sits in between? How do you get from a model that writes text, to an agent that fixes a bug?

*Screen:* the chip "1 · THE QUESTION" top left. Top row, labelled "Nov 2022 · ChatGPT": a small text card "your message" → a box labelled "LLM" → a text card "its reply". Bottom row, labelled "today · an agent": the same "LLM" box → an empty dashed box with a "?" → three action chips, "read files", "run tests", "fix the bug". For "same kind of model", the two LLM boxes pulse together; for "only writes text", the bottom box's output is a small text card that stops at the dashed box. For the question, the dashed box is outlined in white and the "?" grows. The dashed box stays on screen at the end of the chapter.

### 2. What an LLM is

> Start with the model. It's called an LLM, a large language model, and it does one thing: it predicts the next word, or sometimes a piece of a word.
> Give a small, freely available model the words "I made a cup of". It gives every word it knows a probability. "Tea" gets thirty-one percent. "Coffee", nineteen. Everything else is far behind.
> Pick a likely word, here the likeliest, add it to the text, and predict again: "tea", then "and", then "I". Over and over, one word at a time. That's all writing is, for an LLM.
> It works only from the text in front of it. That text is called its context. The model keeps no memory from one use to the next.
> So keep two facts in mind. What comes out of an LLM is text. And it learned a lot in training, but about your task, it knows only what's in its context.

*Screen:* the fixed picture begins. The "LLM" box in the upper middle; to its left, a tall panel (the context) holding the text "I made a cup of"; an arrow from the panel into the box. To the right of the box, five horizontal bars appear, one per candidate, with the word and its probability (data/next_word.json, GPT-2): tea 31%, coffee 19%, soup 1.5%, the 1.3%, this 1.2%. The label "a small, freely available model (GPT-2)" sits small under the bars. "tea" moves from its bar into the panel's text; then "and" (18%) and "I" (8%) each appear as a single chosen word and move into the text: "I made a cup of tea and I". The label "context" appears over the panel when the narration names it; "LLM · large language model" under the box. For the two facts, two short tags: "out: text" at the box's output, "knows: its context" on the panel.

### 3. Text that is an action

> Here's a task. A small shop's billing code stops with an error: no price for "gadget".
> You might picture the model reaching into the files itself. So ask a model on its own to fix it. In one try, it wrote that it would explore the project, and even wrote out a command to do it. But nothing was there to run the command, and the tests still failed.
> Text on its own doesn't do anything. So put a program next to the model, to watch what it writes.
> Then give the model a format for requests, described at the top of its context. A line that starts "search:", then some words. Or "open file:", then a file name. Real agents use a stricter format, but the idea is the same.
> Now the model writes a line: search, "no price for". The program spots the request, and searches the project's files for those words.
> Each thing the program can do for the model is called a tool: search, open a file, edit a file, run the tests.
> Notice who did the searching. The model only wrote a line of text. The program did the work.

*Screen:* on the right, the project: four file chips (invoice.py, prices.py, orders.csv, test_invoice.py) and a red badge "tests: fail". The context panel clears and shows the task card, abridged from the real task: "… stops with this error: LookupError: no price for 'gadget' …". For "reaching into the files itself", a faint arrow from the LLM box toward the files, which fades. For the model on its own (captures/bare_1.json), the LLM box writes to its right, in blue: "I'll start by exploring the project structure to find the relevant code." and under it, in small mono, "Tool: bash · find … -type f …"; a dashed arrow from that text toward the project stops short with a small grey cross; the badge stays red. That text fades. A card "starting instructions" slides in at the top of the context panel, listing the four request forms as the real instructions give them: "search: TEXT", "open file: NAME", "edit file: NAME …", "run tests". The model writes the first real request of the run (captures/run_1.json): "search: no price for". A box labelled "program" appears below and between the model and the project; a bracket from the program spots the request line; the program's "search" chip lights, and an arrow runs from the program to the project; the file chips flash in turn and prices.py stays lit, with a small tag "line 8". The program's four tool chips (search, open file, edit file, run tests) are labelled "tools" when the narration names them. For the last lines, the LLM box dims and the program box and its arrow to the project brighten.

### 4. The result goes back in

> But the search found something, and the model can't see it. Remember: it knows only what's in its context.
> So the program pastes the result into the context. One match: line eight of a file called prices.py. Then it runs the model again, on the whole context, because the model remembers nothing.
> Now the model continues with the result in view. It knows something it couldn't have known before: where the error comes from. So it writes its next request: open that file.
> You've probably seen this already. In 2023, the popular chat assistants started searching the web. It's the same trick. The model writes a search, a program runs it, and the results are pasted into the context. Then the model answers, with those pages in view.

*Screen:* the result waits at the program as a small green card: `prices.py:8: raise LookupError(f"no price for {product!r}")` (the real result, shown in mono). For the second line, an arrow from the program back to the bottom of the context panel appears and the green card travels along it into the panel, under the blue request line; the arrow is labelled "result". An arrow from the context panel into the LLM box lights and a light band sweeps down the whole panel (the whole context sent again). The model writes, in blue, "open file: prices.py"; its line joins the panel. For the web-search lines, a small labelled inset replaces the project for a moment: "2023 · chat assistants", with the same four parts in the same places, relabelled: the context holds "a question", the model writes "search: …", the program's chip reads "web search", a green card "results from web pages" goes back into the context, and the model writes "an answer, with sources". Generic labels, not a real transcript. The inset fades and the project returns.

### 5. The loop

> One step won't fix a bug. So repeat. The model writes a request, the program carries it out, and the result goes into the context. Then again.
> This goes on until the model writes a reply with no request in it. That's its answer, and the loop stops.
> A model working in a loop like this, using tools, is called an agent.
> Here's an agent fixing the shop's bug. It searches for the error message, and opens the file it finds. Then it searches for where that code is used, and opens that file too.
> The price list spells it "Gadget", with a capital G. So it edits the lookup, so that "gadget" finds "Gadget". Then it runs the tests.
> They fail. Ben's bill should come to thirty-seven. It comes to thirty-nine fifty.
> That failure goes into the context, like any other result, and it changes the next step. The model looks at the test and at Ben's orders, and finds a second mistake. The bulk discount starts at eleven items, not ten.
> It edits that, and runs the tests again. This time they pass. It writes its answer, and the loop stops.
> That was twelve requests. Nobody wrote them down in advance. Each one followed from the results before it.

*Screen:* the four arrows (context → LLM → request → program → context) light in turn and a dot runs round them twice; the label "the loop" sits inside the cycle. For "no request in it", a grey reply card leaves the model, the program's bracket finds no request, and the dot stops. The label "agent" appears over the whole cycle when the narration names it. Then the real run (captures/run_1.json) replays from its first request: the context panel is a column of one-line cards, blue for each request as the model wrote it (first line only) and green for each result (a short excerpt), newest at the bottom, older ones scrolling up and shrinking; a small counter "requests" at the top right of the panel counts 1 to 12. In order: search: no price for → "prices.py:8 …"; open file: prices.py → "PRICES = {"Widget": 2.50, "Gadget": 10.00, …}"; search: price_of → "invoice.py:16 …"; open file: invoice.py → "if quantity > BULK: …"; edit file: prices.py → "edited prices.py", with a small diff tag "gadget → Gadget"; run tests → a red card "FAILED: 39.5 != 37.0", and the project's badge stays red, with a callout "Ben: expected 37.00, got 39.50"; edit file: prices.py (a change of blank lines only; shown, not narrated); open file: test_invoice.py; search: quantity; open file: orders.csv → "Ben,Widget,10"; edit file: invoice.py → "edited invoice.py", with the diff tag "quantity > BULK → quantity >= BULK" and the label "discount from 10, not 11"; run tests → a green card "OK", and the badge turns green, "tests: pass". Then a grey reply card, abridged from the real reply ("… Tests now pass."), and the dot stops. For the last line, the twelve blue request cards are outlined together, with "12 requests" beside them.

### 6. Why it took until now

> If the loop is that simple, why did agents only start working recently?
> People tried, in 2023. They ran models in loops like this one, and the loops often got stuck, going round in circles.
> Part of the problem is that small mistakes add up. Say each step goes right ninety-five times in a hundred, and nothing catches a mistake. Then two steps in a row go right about ninety times in a hundred. Each step takes its cut. After twenty steps, only about a third of the runs are still on track.
> Three things changed. First, models were trained to work in this loop, so each step became more reliable. Suppose that lifts each step to ninety-nine in a hundred. Then about four runs in five get through all twenty steps.
> Second, tasks like coding come with feedback. A failing test catches a mistake, as it caught the discount, and the next step can fix it.
> Third, agents find what they need by searching, step by step, as that run did. Claude Code, a coding agent, works that way. Its developers first tried building an index of the code in advance, and have said searching worked better.

*Screen:* the diagram shrinks to the upper half, unchanged. Under it, the label "2023 · early agents (AutoGPT and others)", and a loop arrow with a small dot circling it over and over. Then a row of twenty dots, "step 1 … step 20", with "95% each" at the left. Under each dot, the chance that the run is still on track after that step, filled in from left to right as the narration goes (data/compound.json): 0.95, 0.90 (circled when "two steps" is said), 0.86, … 0.36 at step 20, with "about 1 in 3" beside it. The caveat sits small under the row: "if steps are independent and no mistake is caught". For ninety-nine in a hundred, a second row under the first, "99% each (suppose)": 0.99, 0.98, … 0.82 at step 20, "about 4 in 5", with the same caveat. Then three numbered markers point into the diagram above: "1 · trained for the loop" at the LLM box; "2 · feedback" at the "run tests" tool, with the red failing-test card from chapter 5 reappearing briefly beside it; "3 · search step by step" at the "search" tool, with the tag "Claude Code", and beside it a small crossed-out card "index built in advance".

### 7. The harness

> Now put names on the whole picture.
> The LLM is the model. Everything around it is called the harness.
> The harness writes the starting instructions, with the request format. It holds the tools, and the program that carries out each request. And it runs the loop.
> A real harness does more. It checks permission before an edit or a command, sometimes by asking you. And a context has a size limit. When it fills up, the harness trims it, for example by summarizing older steps.
> So an agent is an LLM plus a harness.
> That's five words to keep: LLM, context, tool, harness, and agent.

*Screen:* the diagram at full size. "LLM" is labelled on its box. A dashed green outline is drawn around everything except the LLM box (the context panel, the program, the tools, the arrows), and labelled "harness". Its parts are labelled one at a time as the narration names them: "starting instructions" on the top card of the context; "tools" on the chips; "program" on the program box; "loop" on the arrows. Then two new parts appear: a small gate on the arrow from the program to the project, labelled "permission check"; and at the top of the context panel, older cards squeeze into one card labelled "summary", tagged "trim the context". Then the equation "agent = LLM + harness" at the bottom. Then a glossary card replaces the diagram, its five rows appearing as the five words are said, and held for a few seconds: "LLM · predicts the next word"; "context · the text in front of it: all it sees"; "tool · something the program does when the model asks"; "harness · everything around the model (also called a scaffold)"; "agent · LLM + harness".

### 8. The answer

> So, how do you get from a model that only writes text to an agent that fixes a bug?
> The model still does one thing. It predicts the next word, one at a time.
> The harness turns some of that text into actions, and pastes the results back into the context. And the loop turns single steps into a whole job.
> ChatGPT in 2022 could only talk. An agent is still talking. The difference is the harness: a program that listens to what the model writes, and acts on it.

*Screen:* the finished diagram, with the harness outline. On "predicts the next word", the LLM box shows the "tea" bars from chapter 2 for a moment. On "turns some of that text into actions", the request line → program → project arrows light; on "pastes the results back", the result arrow lights; on "the loop", the dot runs round the cycle once. For the last line, the chapter 1 picture returns small at the top left, its dashed "?" box now filled with the word "harness". End card: the takeaway, "An agent is an LLM plus a harness. The model only writes text; the harness carries out its requests and feeds the results back, in a loop.", and the references: Anthropic, "Building effective agents" (Schluntz and Zhang, 2024); Claude Code docs, "How Claude Code works"; Latent Space, "Claude Code: Anthropic's Agent in Your Terminal" (2025); Weng, "LLM Powered Autonomous Agents" (2023); Radford et al., GPT-2 (2019).

## Evidence

| Claim | How it was checked | Value |
|---|---|---|
| Next-word probabilities for "I made a cup of" | sims/next_word.py: GPT-2 (the 124M-parameter version, 124,439,808 parameters; transformers 5.17, CPU), softmax of the last position's logits, no temperature; data/next_word.json | tea 0.308, coffee 0.191, soup 0.015, the 0.013, this 0.012 (all whole words with a leading space); then, adding the most likely each time: "and" 0.179, "I" 0.079 |
| The shop project and its two bugs | sims/project/: prices.py looks up product names exactly (PRICES has "Gadget"); orders.csv has "gadget" on one row; invoice.py gives the 10% bulk discount only when quantity > 10; test_invoice.py expects Ada 20.00 and Ben 37.00 (2 × 7.25 + 10 × 2.50 less 10%). Running `python3 invoice.py orders.csv` ends `LookupError: no price for 'gadget'` | as stated |
| The model on its own, asked to fix it | captures/bare_1.json (sims/bare.py): one call, same model and command-line tool with its tools switched off, no request format; it replied "I'll start by exploring the project structure to find the relevant code." followed by a made-up "Tool: bash" block with a `find` command; nothing ran it; the tests afterwards: FAILED (errors=1) | as stated |
| The example agent and its request format | sims/agent.py: the model (Claude, the claude command-line tool's default model on 2026-09-27) is called with that tool's own tools switched off, once per step, with the starting instructions and the whole context; the program spots one request per reply (search:, open file:, edit file: with replace/with/end edit, run tests) and carries it out itself; a reply with no request ends the loop (at most 20 calls) | the instructions are in captures/run_1.json, "system" |
| The replayed run: requests in order and results | captures/run_1.json; data/runs.txt. 1 search: no price for → prices.py:8; 2 open file: prices.py; 3 search: price_of → invoice.py:5, invoice.py:16, prices.py:6; 4 open file: invoice.py; 5 edit file: prices.py (key = product.strip().title()); 6 run tests → FAILED (failures=1), "AssertionError: 39.5 != 37.0 within 7 places (2.5 difference)" on Ben's line; 7 edit file: prices.py (adds two blank lines only); 8 open file: test_invoice.py; 9 search: quantity; 10 open file: orders.csv; 11 edit file: invoice.py (quantity > BULK → quantity >= BULK); 12 run tests → OK; then a reply with no request ending "Tests now pass." Our own check afterwards: tests OK; `python3 invoice.py orders.csv` prints Ada: 20.00, Ben: 37.00 | 12 requests, 13 model calls |
| Run 1 was chosen for the replay before any run was made; two more runs of the same setup | sims/run_all.sh (comment); data/runs.txt: run 2 and run 3 each took 8 requests (two searches, open, edit, run tests → FAILED on Ben's bill, open invoice.py, edit, run tests → OK) and passed; two earlier pilot runs, used to fix the edit format and to leave file names out of the task, are not replayed | 3 of 3 passed; each ran the tests, saw them fail on the discount, and fixed it |
| "At the top of the context" the program describes the format | captures/run_1.json, "system": sent before the task on every call, as the system prompt | as stated |
| The program sends the whole context on every call; the model keeps nothing between calls | sims/agent.py, call_model() sends render(context) each time; each call is a fresh process | as stated |
| Compounding: 20 steps at 95% each all go right with probability 0.95^20 (95% is an illustration, not a measurement) | sims/compound.py; data/compound.json. Assumes independent steps and no mistake caught | two steps 0.9025 ("about ninety in a hundred"); twenty steps 0.3585 ("about a third") |
| At 99% a step (a supposed figure, not a measurement) | same | 0.99^20 = 0.8179, "about four in five" |
| ChatGPT launched in late 2022 and at first only talked | OpenAI, "Introducing ChatGPT", 30 Nov 2022 (via TechCrunch, 30 Nov 2025); research/verified_primary_sources.md | 30 Nov 2022 |
| Chat assistants began searching the web in 2023, with this mechanism | Microsoft, 7 Feb 2023 (Bing reviews web results and cites sources); Ribas, "Building the New Bing", 21 Feb 2023 (the model generates internal queries, and reasons over the data Bing provides); TechCrunch, 23 Mar 2023 (ChatGPT's browsing plugin) | 2023 |
| In 2023, people ran models in loops like this (AutoGPT and others), and the loops often got stuck going round in circles | AutoGPT README v0.2.1 (Apr 2023): "May not perform well in complex, real-world business scenarios"; Weng (23 Jun 2023): "quite a lot of reliability issues ... a cool proof-of-concept demo"; Wikipedia's AutoGPT article citing the New York Times (10 Jun 2023): "tendency to get stuck in infinite loops" | 2023 |
| Models were trained to work in this loop | OpenAI, 13 Jun 2023: models "fine-tuned to both detect when a function needs to be called ... and to respond with JSON"; Anthropic, 6 Jan 2025: "training Claude 3.5 Sonnet to be excellent at agentic coding"; OpenAI o3 and o4-mini system card, 16 Apr 2025: trained with large-scale reinforcement learning, and "use tools in their chains of thought" | as stated |
| Coding gives feedback that catches mistakes | Anthropic, "Building effective agents" (2024): "Code solutions are verifiable through automated tests; Agents can iterate on solutions using test results as feedback"; and the replayed run (request 6) | as stated |
| Claude Code finds code by searching step by step; its developers first tried an index of the code built in advance, and said searching worked better | Claude 3.7 Sonnet and Claude Code announcement (24 Feb 2025): "can search and read code"; Latent Space (7 May 2025), Boris Cherny: early versions "indexed the code base", then "we landed on just agentic search", "glob, grep", "it outperformed everything. By a lot." (mostly internal impressions, some internal benchmarks); Anthropic, "Effective context engineering" (29 Sep 2025): glob and grep "retrieve files just-in-time, effectively bypassing the issues of stale indexing" | as stated |
| "Harness" names the layer around the model; it provides the tools and manages the context | Claude Code docs, "How Claude Code works": "Claude Code is the layer around the model that provides the tools and manages the context the model sees. This surrounding layer is what the term agentic harness refers to." | as stated |
| Permission checks, sometimes by asking you | Claude Code docs: "Manual: Claude asks before file edits and shell commands"; "Auto: a classifier reviews most actions in the background and blocks the risky ones instead of asking you" | as stated |
| A context has a size limit; when it fills, the harness trims it, e.g. by summarizing | Claude Code docs: "As you work, context fills up"; "It clears older tool outputs first, then summarizes the conversation if needed"; Anthropic, "Effective context engineering" (2025), compaction | as stated |
| Real agents use a stricter, structured format for requests than a line of text | Claude API docs, "How tool use works" (read 2026-09-26, lessons/llm-agents/research/verified_primary_sources.md): "The model never executes anything on its own. It emits a structured request, your code (or Anthropic's servers) runs the operation, and the result flows back into the conversation."; OpenAI function calling (2023): "respond with JSON that adheres to the function signature" | as stated |
| Agents are LLMs using tools in a loop | Anthropic, "Building effective agents" (2024): "They are typically just LLMs using tools based on environmental feedback in a loop." | as stated |

## Review log

**Before round 1.** Research: two fresh passes (research/canonical_web_agent.md, research/canonical_claude_p.md) agree with the approved outline's order (next-word prediction, one tool call, the loop, refinements), on the misconception it targets (the model itself acts), on compounding error as the usual explanation of unreliable long runs (flagged by both as a heuristic that assumes independent steps and no correction), and on "harness" or "scaffold" for the software around the model. Dates, the Claude Code search claim and the harness definition were checked against primary sources (research/verified_primary_sources.md). Refinements of the approved outline, all within its bounds: (1) the chapter 3 problem is made visible with a real run of the model on its own (it writes out a command that nothing runs); (2) the request format is described "at the top of the context", which chapter 7 names as the starting instructions; (3) the worked example is a new real run of a small agent whose request format is exactly the one chapter 3 teaches ("search: ...", "open file: ..."), on a small billing project where the reported error must be searched for and the second bug only shows up when the tests run; the run chosen for the replay was fixed before any run was made; (4) chapter 6's three changes each point at a part of the diagram (the model, the run-tests tool, the search tool), and the second calls back to the failing test in chapter 5; (5) the chapter 1 picture has an empty box between the model and the actions, which chapter 8 fills with "harness".

**Round 1:** expert PASS, editor PASS; student retold the question and answer correctly but was lost at the compounding arithmetic ("lands as an assertion"), and its retelling covered neither the failing test nor why agents took until recently (objectives 3 and 4). The gate is not met, so round 2 is not the final round.
- Expert, should fix, taken: "next word" is now glossed once, in passing, as "or sometimes a piece of a word" (the approved outline allows this when a reviewer insists; the example's candidates are all whole words). The 99% is now explicitly supposed ("Suppose that lifts each step to ninety-nine in a hundred"), with the caveat on screen under both rows. The model-on-its-own result is now told as one try ("In one try, it wrote ..."). One sentence says real agents use a stricter format than a line of text.
- Expert, NITs: "chat assistants" is now "the popular chat assistants" (WebGPT and others came earlier); "harness" gets "(also called a scaffold)" on the glossary card only. Not taken: re-checking the TechCrunch citation; it is a third-anniversary article dated 30 Nov 2025, read in this session, and OpenAI's page itself answers 403 here.
- Student: the compounding step is now shown one multiplication at a time: two steps in a row go right about ninety times in a hundred, each step takes its cut, and after twenty only about a third of runs are still on track; on screen, the running chance is filled in under each of the twenty dots. "Open model" is now "a small, freely available model"; "pick a likely word" now says "here the likeliest". The failing test's role is spoken ("it changes the next step").
- Editor, should fix, taken: the index comparison is now set up before it is used ("Its developers first tried building an index of the code in advance, and have said searching worked better"), and Claude Code is glossed as "a coding agent". "Agree on a format" had no agent: the program now arrives first, and the model is given the format. The glossary is no longer read out definition by definition over a card that shows the same words: the narration names the five words, and the card holds the definitions. AutoGPT, named but not understood, is now only an on-screen label; the narration says "people ran models in loops like this one". The misconception is voiced before the demonstration ("You might picture the model reaching into the files itself").
- Editor, not taken: saying the replayed run was "recorded from Claude Code". It wasn't: it is a small harness written for this example (sims/agent.py), and saying otherwise would be false; Claude Code appears once, softly, as the approved outline asks. Renaming the model-on-its-own "command": it is literally a command, and the difference from a request (nothing is there to run it) is now said outright. Showing a permission check or a trim happening: both are one sentence in the harness's definition, and each gets its own picture (a gate, a summary card).
