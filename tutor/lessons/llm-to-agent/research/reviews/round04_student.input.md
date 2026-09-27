You are this particular viewer:

Background

- Works in industry and wants lessons "useful in the industry day to day". Picked queueing, tail latency, and idempotency with retries from a list of practical topics.
- Keeps a personal library of prompts and references on software architecture, data systems, performance, observability and LLM agents. Likely a software, data or ML engineer. Their exact role and years of experience are unknown.
- Has watched two lessons in this series: UMAP (an earlier session) and external merge sort (version 2, 6:25).
- Assume they know: programming, how web services, APIs and databases are built and called, averages and percentiles as everyday terms, Big-O.
- Unknown: how comfortable they are with probability beyond the everyday (distributions, independence, expected value), and how much formula they want on screen.


Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.


 You have not studied this topic. Stay in role: if the script does not explain something, you do not know it. Below is the script of a short narrated video, with a note of what is on screen at each moment. Go through it once, in order, as if watching. (1) List every point where you would be confused or lose the thread, quoting the line: a term used before it is explained, a step that does not follow, a number with no meaning attached, a sentence hard to follow when heard. (2) List the questions you would ask afterwards. (3) Without looking back, write what you learned in about 150 words. (4) Answer: what is the one main idea; which numbers do you remember and what do they mean; what question did the video start with, and what was its answer? (5) Rate how much the opening made you want the answer (1-5) and how often you felt lost (never / once / a few times / often).


---

## Script

Audience for every reviewer: this lesson is made for non-technical to somewhat technical viewers who remember ChatGPT arriving in late 2022, later noticed AI started doing things, and have not studied how it works. Judge it for that audience.

### 1. The question

> In late 2022, ChatGPT arrived. You typed a message, and it wrote back. It could talk, and that was all.
> Now there are AI agents that do things. Give one a bug in some code, and it reads the files, runs the tests that check the code, and fixes the bug.
> Underneath, it's the same kind of model as the one in the chat. And a model like that only writes text.
> So what sits in between? How do you get from a model that writes text, to an agent that fixes a bug?

*Screen:* the chip "1 · THE QUESTION" top left. Top row, labelled "Nov 2022 · ChatGPT": a small text card "your message" → a box labelled "model" → a text card "its reply". Bottom row, labelled "today · an agent": the same "model" box → an empty dashed box with a "?" → three action chips, "read files", "run tests", "fix the bug". For "same kind of model", the two LLM boxes pulse together; for "only writes text", the bottom box's output is a small text card that stops at the dashed box. For the question, the dashed box is outlined in white and the "?" grows. The dashed box stays on screen at the end of the chapter.

### 2. What an LLM is

> Start with the model. It's called an LLM, a large language model, and it does one thing: it predicts the next word, or sometimes a piece of a word.
> Give a small, freely available model the words "I made a cup of". It gives every word it knows a probability. "Tea" gets thirty-one percent. "Coffee", nineteen. Everything else is far behind.
> Pick one of the likely words, and add it to the text. Then predict again: "tea", then "and", then "I". Over and over, one word at a time. That's all writing is, for an LLM.
> It works only from the text in front of it. That text is called its context. The model keeps no memory from one use to the next.
> So keep two facts in mind. What comes out of an LLM is text. It learned a lot in training. But about your task, it knows only what's in its context.

*Screen:* the fixed picture begins. The "LLM" box in the upper middle; to its left, a tall panel (the context) holding the text "I made a cup of"; an arrow from the panel into the box. To the right of the box, five horizontal bars appear, one per candidate, with the word and its probability (data/next_word.json, GPT-2): tea 31%, coffee 19%, soup 1.5%, the 1.3%, this 1.2%. The label "a small, freely available model (GPT-2)" sits small under the bars. "tea" moves from its bar into the panel's text; then "and" (18%) and "I" (8%) each appear as a single chosen word and move into the text: "I made a cup of tea and I". The box's label changes from "model" to "LLM · large language model" when the narration names it; the label "context" appears over the panel when the narration names it. For "pick one of the likely words", the tea bar is outlined, tagged "picked". For the two facts, two short tags: "out: text" at the box's output, "knows: its context" on the panel.

### 3. Text that is an action

> Here's a task. A small shop's billing code stops with an error: no price for "gadget".
> You might picture the model reaching into the files itself. So ask a model on its own to fix it: not the small one, but a large model, like the ones behind chat assistants. In one try, it wrote that it would explore the project, and even wrote out a request to run a command. But nothing was there to carry it out, and the tests still failed.
> Text on its own doesn't do anything. So put a program next to the model, to watch what it writes.
> Then give the model a format for requests, described at the top of its context. A line that starts "search:", then some words. Or "open file:", then a file name. Real agents use a stricter format, but the idea is the same.
> Now the model writes a line: search, "no price for". The program spots the request, and searches the project's files for those words.
> Each thing the program can do for the model is called a tool: search, open a file, edit a file, run the tests.
> Notice who did the searching. The model only wrote a line of text. The program did the work.

*Screen:* on the right, the project: four file chips (invoice.py, prices.py, orders.csv, test_invoice.py) and a red badge "tests: fail". The context panel clears and shows the task card, abridged from the real task: "… stops with this error: LookupError: no price for 'gadget' …". For "reaching into the files itself", a faint arrow from the LLM box toward the files, which fades. For "not the small one", the GPT-2 tag fades and the LLM box gets a new small tag, "a large model (Claude)", which stays for the rest of the video. For the model on its own (captures/bare_1.json), the LLM box writes to its right, in blue: "I'll start by exploring the project structure to find the relevant code." and under it, in small mono, "Tool: bash · find … -type f …"; a dashed arrow from that text toward the project stops short with a small grey cross; the badge stays red. That text fades. A card "starting instructions" slides in at the top of the context panel, listing the four request forms as the real instructions give them: "search: TEXT", "open file: NAME", "edit file: NAME …", "run tests". The model writes the first real request of the run (captures/run_1.json): "search: no price for". A box labelled "program" appears below and between the model and the project; a bracket from the program spots the request line; the program's "search" chip lights, and an arrow runs from the program to the project; the file chips flash in turn and prices.py stays lit, with a small tag "line 8". The program's four tool chips (search, open file, edit file, run tests) are labelled "tools" when the narration names them. For the last lines, the LLM box dims and the program box and its arrow to the project brighten.

### 4. The result goes back in

> The search found something. But the model can't see it. Remember: it knows only what's in its context.
> So the program pastes the result into the context. One match: line eight of a file called prices.py. Then it runs the model again, on the whole context, because the model remembers nothing.
> Now the model continues with the result in view. It knows something it couldn't have known before: where the error comes from. So it writes its next request: open that file.
> You've probably seen this already. In 2023, the popular chat assistants started searching the web. It's the same trick. The model writes a search, a program runs it, and the results are pasted into the context. Then the model answers, with those pages in view.

*Screen:* the result waits at the program as a small green card: `prices.py:8: raise LookupError(f"no price for {product!r}")` (the real result, shown in mono). For the second line, an arrow from the program back to the bottom of the context panel appears and the green card travels along it into the panel, under the blue request line; the arrow is labelled "result". An arrow from the context panel into the LLM box lights and a light band sweeps down the whole panel (the whole context sent again). The model writes, in blue, "open file: prices.py"; its line joins the panel. For the web-search lines, a small labelled inset replaces the project for a moment: "2023 · chat assistants", with the same four parts in the same places, relabelled: the context holds "a question", the model writes "search: …", the program's chip reads "web search", a green card "results from web pages" goes back into the context, and the model writes "an answer, with sources". Generic labels, not a real transcript. The inset fades and the project returns.

### 5. The loop

> One step won't fix a bug. So repeat. The model writes a request, the program carries it out, and the result goes into the context. Then again.
> This goes on until the model writes a reply with no request in it. That's its answer, and the loop stops.
> A model working in a loop like this, using tools, is called an agent.
> Here's how the whole run went. After the search and the file you've seen, it searches for where that code is used, and opens that file too.
> The price list spells it "Gadget", with a capital G. So it edits the lookup: now "gadget" finds "Gadget". Then it runs the tests.
> They fail. Ben's bill should come to thirty-seven. It comes to thirty-nine fifty.
> That failure goes into the context, like any other result, and it changes the next step. The model looks at the test and at Ben's orders, and finds a second mistake. The bulk discount only kicked in at eleven items. It should start at ten.
> It edits that, and runs the tests again. This time they pass. It writes its answer, and the loop stops.
> That was twelve requests. Nobody wrote them down in advance. Each one followed from the results before it.

*Screen:* the four arrows (context → LLM → request → program → context) light in turn and a dot runs round them twice; the label "the loop" sits inside the cycle. For "no request in it", a grey reply card leaves the model, the program's bracket finds no request, and the dot stops. The label "agent" appears over the whole cycle when the narration names it. Then the real run (captures/run_1.json) replays from its first request: the context panel is a column of one-line cards, blue for each request as the model wrote it (first line only) and green for each result (a short excerpt), newest at the bottom, older ones scrolling up and shrinking; a small counter "requests" at the top right of the panel counts 1 to 12. In order: search: no price for → "prices.py:8 …"; open file: prices.py → "PRICES = {"Widget": 2.50, "Gadget": 10.00, …}"; search: price_of → "invoice.py:16 …"; open file: invoice.py → "if quantity > BULK: …"; edit file: prices.py → "edited prices.py", with a small diff tag "gadget → Gadget"; run tests → a red card "FAILED: 39.5 != 37.0", and the project's badge stays red, with a callout "Ben: expected 37.00, got 39.50"; edit file: prices.py, tagged "no real change" (it only added blank lines; not narrated); open file: test_invoice.py; search: quantity; open file: orders.csv → "Ben,Widget,10"; edit file: invoice.py → "edited invoice.py", with the diff tag "quantity > BULK → quantity >= BULK" and the label "discount from 10, not 11"; run tests → a green card "OK", and the badge turns green, "tests: pass". Then a grey reply card, abridged from the real reply ("… Tests now pass."), and the dot stops. For the last line, the twelve blue request cards are outlined together, with "12 requests" beside them.

### 6. Why it took until now

> If the loop is that simple, why did agents only start working recently?
> People tried, in 2023. They ran models in loops like this one, and the loops often got stuck, going round in circles.
> Part of the problem is that small mistakes add up. Say each step goes right ninety-five times in a hundred, whatever happened before, and nothing catches a mistake. Start a hundred runs. About ninety-five get the first step right. Of those, ninety-five percent get the second step right too: about ninety. Every step keeps ninety-five percent of the runs still on track. After twenty steps, that's about thirty-six of the hundred. About a third.
> Three things changed. First, models were trained to work in this loop, so each step became more reliable. Suppose that lifts each step to ninety-nine in a hundred. Then about eighty-two of the hundred runs get all twenty steps right: about four in five.
> Second, tasks like coding come with feedback. A failing test catches a mistake, as it caught the discount, and the next step can fix it.
> Third, agents find what they need by searching, step by step, as that run did. Claude Code, a coding agent, works that way. Its developers first tried building an index of the code in advance. But code keeps changing, and an index goes out of date. They've said searching worked better.

*Screen:* the diagram shrinks to the upper half, unchanged. Under it, the label "2023 · early agents", and a loop arrow with a small dot circling it over and over. Then a row of twenty dots, "step 1 … step 20", with "95% each" at the left and "100 runs" above the first dot. Under each dot, how many of the hundred runs still have every step right after that step, filled in from left to right as the narration goes (data/compound.json, rounded): 95, 90 (circled when "the second step" is said), 86, 81, … 36 at step 20, with "about 1 in 3" beside it. The caveat sits small under the row: "assuming each step's chance is the same whatever came before, and no mistake is caught". For ninety-nine in a hundred, a second row under the first, "99% each (suppose)": 99, 98, 97, … 82 at step 20, "about 4 in 5". Then three numbered markers point into the diagram above: "1 · trained for the loop" at the LLM box; "2 · feedback" at the "run tests" tool, with the red failing-test card from chapter 5 reappearing briefly beside it; "3 · search step by step" at the "search" tool, with the tag "Claude Code", and beside it a small card "index built in advance" that fades to grey with the tag "out of date".

### 7. The harness

> Now put names on the whole picture.
> The LLM is the model. Everything around it is called the harness.
> The harness writes the starting instructions, with the request format. It holds the tools, and the program that carries out each request, and it runs the loop.
> A real harness does two more things. Before an edit, like the one to the price lookup, it can check permission, sometimes by asking you. And every result makes the context longer, but a context can only hold so much. When it fills up, the harness trims it, by dropping old results or summarizing older steps.
> So an agent is an LLM plus a harness.
> That's five words to keep: LLM, context, tool, harness, and agent.

*Screen:* the diagram at full size. "LLM" is labelled on its box. A dashed green outline is drawn around everything except the LLM box (the context panel, the program, the tools, the arrows), and labelled "harness". Its parts are labelled one at a time as the narration names them: "starting instructions" on the top card of the context; "tools" on the chips; "program" on the program box; "loop" on the arrows. Then two new parts appear: a small gate on the arrow from the program to the project, labelled "permission check", with the blue request "edit file: prices.py" pausing at it; and in the context panel, result cards stack up until they reach the panel's bottom edge, then old result cards disappear and older cards squeeze into one card labelled "summary", tagged "trim the context". Then the equation "agent = LLM + harness" at the bottom. Then a glossary card replaces the diagram, its five rows appearing as the five words are said, and held for a few seconds: "LLM · predicts the next word"; "context · the text in front of it: all it sees"; "tool · something the program does when the model asks"; "harness · everything around the model"; "agent · LLM + harness".

### 8. The answer

> So, how do you get from a model that only writes text to an agent that fixes a bug?
> The model still does one thing. It predicts the next word, one at a time.
> The harness turns some of that text into actions, and pastes the results back into the context. And the loop turns single steps into a whole job.
> ChatGPT in 2022 could only talk. An agent is still talking. The difference is the harness: a program that listens to what the model writes, and acts on it.

*Screen:* the finished diagram, with the harness outline. On "predicts the next word", the LLM box shows the "tea" bars from chapter 2 for a moment. On "turns some of that text into actions", the request line → program → project arrows light; on "pastes the results back", the result arrow lights; on "the loop", the dot runs round the cycle once. For the last line, the chapter 1 picture returns small at the top left, its dashed "?" box now filled with the word "harness". End card: the takeaway, "An agent is an LLM plus a harness. The model only writes text; the harness carries out its requests and feeds the results back, in a loop.", and the references: Anthropic, "Building effective agents" (Schluntz and Zhang, 2024); Claude Code docs, "How Claude Code works"; Latent Space, "Claude Code: Anthropic's Agent in Your Terminal" (2025); Weng, "LLM Powered Autonomous Agents" (2023); Radford et al., "Language Models are Unsupervised Multitask Learners" (GPT-2, 2019).

