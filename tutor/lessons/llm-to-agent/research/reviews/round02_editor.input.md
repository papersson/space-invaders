You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

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

