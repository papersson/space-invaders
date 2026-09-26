You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** We gave an LLM (Claude) a small Python project with one failing test, and the same request twice: fix report.py so that the test passes. Same model, same files, same request, same code around the model. Both runs took the same first four steps and made the same fix. Run A then took four more steps and replied "Fixed. ... All tests now pass." Run B replied "Fixed" right after its fix, saying its code now matched the test's expected values. We ran the test ourselves: after A it passes; after B it still fails. Three runs of each gave the same split. B's only difference was one missing tool, a way to run the test. What is an LLM agent, that taking away one tool leaves it sure of something false?

**Answer.** An agent is a model, some tools, and a loop. The model only reads text and writes text: on each call it reads its whole context (instructions, the request, and every tool call and tool result so far) and writes the next reply. When the reply is a tool call, the code around the model, not the model, runs the tool and adds the result to the context, then calls the model again; it stops when the model replies without a tool call. The model keeps nothing between calls (in run A, nine calls read from 1,423 up to 2,745 tokens each, 18,537 in all), so the context is its only memory of the task: it still knows what it learned in training (what a byte order mark is), but what it has tried and what came back, it knows only from the context. Run A's context received ground truth, the test's answer, a KeyError caused by an invisible byte order mark in the data file, and the next call acted on it: it read the data file, fixed the second bug, and the test passed. Run B's context never received a test result, so its own fix was the last word, and its "Fixed" was a reasonable conclusion from a context with no evidence against it. That is why agents work (each step can put ground truth into the context) and where they break down: where nothing checks the work, the model's guess stands, and in a longer task later steps build on it (compounding errors); and the context only grows (Claude Code, a production agent, read 11,597 tokens on its first call and 123,192 over nine calls on the same task; longer contexts recall worse, which researchers call context rot).

**Takeaway.** An LLM agent is a model that picks each next step from its context, in a loop that runs those steps and writes the results back; about the task, it remembers nothing else. It can be trusted as far as ground truth reaches that context: before you trust an agent's "done", ask what would have told it that it was wrong.

**Wrong model.** The agent is a smart model that remembers what it has done and knows when it has succeeded; a better model makes a better agent, and the code around it is plumbing.

**Objectives.**
1. Describe an LLM agent as a model, tools and a loop, and say who does what: the model writes tool calls; the code around it runs them and adds the results to the context.
2. Explain why the context is the model's only memory of the task, and what that costs as the context grows (every call reads all of it).
3. Judge when an agent's "done" can be trusted: when a tool result in its context checked the work.
4. Name the two ways agents break down (nothing checks the work, so a wrong guess stands and later steps build on it; the context grows), and tell an agent from a workflow.


## Chain

1. The question: two runs, same model; A says "Fixed" and the test passes; B says "Fixed" and the test fails, three times out of three. B lacked one tool. What is an agent, that one missing tool leaves it sure of something false?
2. Therefore start from the model alone: it reads a context and writes text. But nothing runs text: its reply even contains a shell command, and nothing happens.
3. Therefore our code runs tools the model asks for, and adds each tool result to the context. But one tool call isn't enough: the model asks for a second, and our code has stopped.
4. Therefore a loop: call, run, add the result, call again, until the model replies without a tool call. That is the agent. Run A reads, finds the bug and fixes it; will the test pass? (pause and predict)
5. But the test fails with a KeyError. Therefore, reading that result, the model looks at the data file, finds the invisible mark, fixes it, and the test passes. The model chose those steps: an agent, not a workflow.
6. But the model remembered nothing: every call re-read the whole context, 18,537 tokens over nine calls. Therefore the context is its only memory of the task.
7. Therefore run B: the same loop without run_tests. Its context never received the test's answer, so its "Fixed" stood. Therefore agents work where each step can put ground truth into the context, and break down where nothing checks the work (a wrong guess stands, and later steps build on it).
8. But there is a second way to break down: the context only grows, and every call reads all of it (Claude Code: 11,597 tokens on its first call, 123,192 over nine calls; context rot).
9. Therefore the answer.

Deviations from the canonical progression: the research gives plain call, then a single tool call (the function-calling round trip), then the loop (ReAct's Thought, Action, Observation), then workflows against agents, then failure modes. This script keeps that order, but replaces the standard weather-lookup and question-answering examples with one coding task run for real, because a coding task has a test, which lets the video show the loop's feedback working (run A) and missing (run B) with the same model. The loop is written with a plain-text tool-call format (a line of JSON), as in ReAct, instead of the API's structured tool_use blocks; the screen says so. Planning, long-term memory stores, multi-agent systems, how models are trained to call tools, and benchmark numbers are left out; the last chapter says so.


## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. Two runs

> Here's a small Python project with one failing test. We set up an LLM agent, a program that lets a model work on a task step by step, and asked it to fix the test, twice.
> Same model, same files, same request. And both runs began the same way. They listed the files, read the test, read the code, and fixed the same bug.
> Then they split. Run A took four more steps. Its last reply began "Fixed", and ended "All tests now pass."
> Run B stopped right there. Its reply also began "Fixed", and said its code now matched the values the test expects.
> So we ran the test ourselves. After run A, it passes. After run B, it still fails.
> That wasn't luck. We ran each version three times. Every run like A passed. Every run like B said "Fixed", and failed.
> Run B was missing one thing: a way to run the test. The model was the same. So what is an LLM agent, that taking away one tool leaves it sure of something false?

*Screen:* the project at top right as three file cards, report.py, test_report.py and sales.csv, with a red cross on test_report.py (the test fails). Two strips of cards along the bottom half, labelled "run A" and "run B", built card by card in step with the narration from the real runs (captures/loop_1.json, captures/no_tests_1.json): a grey card, then a white card (the request), then pairs of cards, a blue card naming the tool the model asked for ("list", "read test_report.py", "read report.py", "write report.py") and a green card for what came back. The four pairs appear in both strips at once. Then run A's strip grows four more pairs ("run tests", with a small red cross on its green card; "read sales.csv"; "write report.py"; "run tests", with a small check on its green card) and ends in a blue card "Fixed."; run B's ends in a blue card "Fixed." right after its fourth pair. Beside each final card, the real reply, abridged: A: "Fixed. The test was failing for two reasons … All tests now pass."; B: "Fixed. … now returns the correct totals per region, matching the expected values in test_report.py." Then our own test run after each (captures, "test_after"): A: a check and "OK"; B: a red cross and "KeyError: 'region'". Then "3 of 3" beside each (data/runs.txt). No explanation of the colours yet. The strips stay on screen.

### 2. A model on its own

> To see what's going on, build it up from the start: a model on its own.
> An LLM reads text and writes text. You send it some, and it writes what comes next.
> Everything it reads on one call is called its context. Here, that's some instructions and our request.
> It replies with text, of course. It even writes out a shell command it would like to run.
> But nothing runs text. The command never ran, the model never saw a single file, and the test still fails.
> For anything to change, something else has to act on what the model writes.

*Screen:* the strips from chapter 1 slide down and fade to a faint outline, keeping their place. A box labelled "model" appears top centre, with a small tag under it: "claude -p, tools off". Along the bottom, a new strip starts: a grey card "instructions" and a white card "request". The model box reads the strip: a light band sweeps it from left to right. Then a blue card drops from the model onto the end of the strip, and opens into the real reply (captures/bare_1.json): "I'll look at the test and the report.py file to understand what's failing." then "Tool: bash" and `{"command":"find /home/user/space-invaders -maxdepth 3 -iname '*report*' …}`, the command in a mono box. A dashed line from the command toward the project cards stops short; the project doesn't change, and the red cross on test_report.py stays.

### 3. One tool call

> So let's act for it. We add a list of tools to the instructions: list the files, read a file, write a file, and run the tests. Each is ordinary code, written by us.
> We also tell the model how to ask for one: reply with one line of JSON that names the tool. That request is called a tool call.
> Now the model's first reply is a tool call: list the files.
> Our code reads the request, runs it, and adds the output to the context. That's the tool result.
> Notice who ran it. Not the model. It only wrote a request. Anthropic's documentation puts it plainly: the model never executes anything on its own.
> Then we call the model again, and it asks for a second tool: read the test. But our code stops here. It was written for one tool call.
> The model can't know in advance how many steps it will need. So our code shouldn't decide that either.

*Screen:* the bare strip clears back to its grey card, which widens as four tool names appear on it one by one (list_files, read_file, write_file, run_tests); the format line appears in the grey card, as the system prompt gives it: `{"tool": "read_file", "path": "report.py"}`. A box labelled "our code" appears between the model and the project. The real run (captures/one_tool_1.json): the band sweeps the strip; a blue card `{"tool": "list_files"}` drops onto the strip, and an arrow carries it to "our code", which touches the project; a green card comes back and joins the strip, opening briefly to show "report.py sales.csv test_report.py". The band sweeps again, and a blue card `{"tool": "read_file", "path": "test_report.py"}` drops onto the strip; "our code" stays still; the card's outline pulses, unanswered.

### 4. The loop

> Therefore, a loop. Call the model. If its reply is a tool call, run the tool, add the result to the context, and call the model again. Stop when it replies without one, or after twenty calls, in case it never does.
> That loop, with a model and some tools, is the whole agent. One common definition says just that: an LLM agent runs tools in a loop to achieve a goal.
> Here's run A, one call at a time. It lists the files, reads the test, and reads the code. And it spots a bug: the code adds the units to the price, where it should multiply them.
> It rewrites that line, then asks to run the test.
> Pause here, and make a prediction. The model found a real bug, and fixed it. Will the test pass?

*Screen:* "our code" turns into a loop: an arrow from the model's card down to "our code", on to the project, back into the strip, and up to the model. Beside it, the code card, exactly as in sims/agent.py (`def agent(task, tools, max_calls=20):` and its body: build the context from the task; for each call, call the model with the context, append its reply, parse a tool call; if there is none, return; otherwise run the tool and append its result), with a small note under it: "the model's tool call is a line of JSON; APIs give it a structured form". Then the replay of run A (captures/loop_1.json) on the strip, one call per pair of cards, the band sweeping before each blue card: list_files, read_file test_report.py, read_file report.py (its green card opens on the line `... + int(row["units"]) + float(row["unit_price"])`, the second plus highlighted), write_file report.py (the card opens on the same line with `*`). Then a blue card `{"tool": "run_tests"}` drops onto the strip, and everything stops: the arrow to "our code" waits. The pause holds for about three seconds.

### 5. The test answers

> It doesn't. The test fails with a key error: there's no column called "region".
> That result goes into the context, like any other. It's the world's answer, not the model's guess: what Anthropic's guide to agents calls ground truth.
> And on the next call, the model reads it, and changes course: it asks to see the data file.
> The file begins with an invisible character, called a byte order mark, glued to the front of the word "region". The code was only half the problem.
> The model changes how the file is opened, so the mark is skipped. It runs the test again, and this time it passes. Then it replies with no tool call, and the loop ends.
> Notice who decided to look at the data file. Not our code: it only ran what was asked. Nobody wrote that step in advance.
> Suppose we had scripted the steps instead: read, then fix, then test. That kind of program is called a workflow. Ours would have stopped at the key error, with no step for what came next.
> In an agent, the model picks each next step from what's in its context. Here, that included ground truth from the test.

*Screen:* the run_tests card goes to "our code", the project's test runs, and a green card with a red cross joins the strip; it opens on the real output's last lines (captures/loop_1.json): `KeyError: 'region'` and `FAILED (errors=1)`. The band sweeps; the blue card `{"tool": "read_file", "path": "sales.csv"}`; the green card opens on the file's first line, `region,product,units,unit_price`, with a small red marker drawn just before "region" (the byte order mark, U+FEFF, which prints as nothing), labelled "byte order mark". Then write_file report.py (opening on `open(path, newline="", encoding="utf-8-sig")`, the encoding highlighted), run_tests (green card with a check, "OK"), and the final blue card "Fixed." The red cross on test_report.py turns into a check. Then above the strip, the scripted path as three grey chips, "read", "fix", "test", ending in a red cross, and under it the real path as the blue cards' names, the chips after the first test run highlighted.

### 6. What the model remembers

> Run A called the model nine times: eight tool calls, then the final reply.
> It looks as if the model worked through the problem, remembering what it had tried. It didn't. Each of those calls started from nothing.
> The model keeps nothing between calls. So our loop sends it the whole context every time: the instructions, the request, and every tool call and result so far.
> Here's how much it read on each call, counted in tokens, the chunks of text a model reads. The first call read about fourteen hundred.
> Most of that is fixed text: our instructions, and notes that the command-line tool we call the model through adds to every call.
> The ninth read about twenty-seven hundred: everything the first call read, and everything since.
> Together, the nine calls read about eighteen and a half thousand tokens, to change two lines of code.
> This isn't a quirk of our code. Anthropic's documentation says the same of its Messages API: it's stateless, so you always send the full conversation.
> The model still knows what it learned in training. That's how it knew what a byte order mark was.
> But what it has tried in this task, and what came back, it knows only from its context. The context is its only memory of the task.

*Screen:* the strip's cards keep their order and colours but change width to the number of tokens each adds (captures/loop_1.json: each call's context minus the one before; within a call's addition, split between the model's card and the tool result's card by characters), so the grey instructions block, most of the first call, becomes the widest; it splits into two shades, a wide one labelled "notes added by claude -p ≈1,180" and a narrow one "our instructions + request ≈240" (data/overhead.txt). Then the strip is copied upward once per call, each copy cut at that call's length, making a staircase of nine rows: row n is what call n read. Beside each row, its count in amber: 1,423 for the first, 2,745 for the ninth, the others smaller and fainter. A band sweeps each row from the left as its count appears. Then an amber total under the staircase: 18,537 tokens read. The green card with the red cross (the KeyError) is outlined in every row from the sixth call on.

### 7. Run B

> Now run B makes sense. It's the same loop and the same model. The only difference is the tool list: there's no run tests.
> Its first four steps match run A's. Then, where run A asked to run the test, run B had nothing to ask for.
> So it replied. Look at its context when it did: its own fix, and nothing after it. No tool result could have told it the fix was incomplete.
> It looks as if the model knew it had succeeded. It didn't. It only knew that nothing in its context said otherwise.
> Its "Fixed" wasn't a lie. It was a reasonable conclusion, from a context with no evidence against it.
> It could have read the data file. It had the tool. But nothing in its context gave it a reason to.
> So this is why agents work, and the first way they break down. Each step can put ground truth into the context. Where nothing checks the work, the model's own guess has the last word.
> And in a longer task, later steps would build on that guess, because it stays in the context and is read on every call. That's called compounding errors.

*Screen:* the staircase folds back into run A's single strip of cards, which moves up; run B's strip is built beneath it card by card, cards aligned (captures/no_tests_1.json). B's grey card shows its tool list with run_tests missing. B's first four pairs line up under A's. At the fifth position, A's `run_tests` card and its green card with the red cross are outlined; under them, B's final blue card, "Fixed.", and then empty space where A's strip goes on. B's reply opens in full above its card (the real text, as in chapter 1). Then B's final card and the empty space are bracketed, and a small label appears: "nothing checks the work". For the last line, B's "Fixed." card is outlined in red and the label "compounding errors" appears under the first.

### 8. The context grows

> The second way agents break down is in the staircase: the context only grows. Every step adds to it, and every call reads all of it.
> Here's the same task, run once by Claude Code, Anthropic's coding agent, with its tools narrowed to match ours: read, edit, and run the test.
> Its first call read about eleven thousand six hundred tokens: its instructions, its tool descriptions, and our one request.
> It found both bugs in nine calls, like run A. But it read those instructions again on every call, so in all it read over a hundred and twenty thousand tokens.
> And a longer task costs more than its length suggests. Twice the calls means more than twice the reading, because each new call re-reads everything before it.
> Reading more isn't only slower and costlier. As a context grows, models get worse at recalling what's in it. Researchers call this context rot. Our runs are far too short to show it.

*Screen:* the label "the context grows" at the top left. Run A's staircase from chapter 6, then its strip in token widths, at the chapter 6 scale; then Claude Code's first-call context (captures/claude_code_1.parsed.json) drawn at the same scale as a grey block that runs off the right edge; the view zooms out until it fits, and run A's whole strip becomes a short bar beside it. Its per-call counts as a staircase of nine rows (11,597 to 15,620, in amber; "9 calls · 10 tool calls"), the grey part of every row outlined, and the amber total, 123,192. For "twice the calls", run A's staircase with a second copy of its rows stacked on top, each longer, and the area beside it. Then the label "context rot · Hong, Troynikov and Huber (Chroma), 2025".

### 9. The answer

> So why did one missing tool leave run B sure of something false? Because an agent is a model that picks each next step from its context.
> And a loop that runs those steps, and writes the results back in. About the task, the model remembers nothing else.
> Run A's context held ground truth from the test. Run B's held only its own fix. Same model, different context.
> A smarter model might read more carefully. But it still can't see a test result that never arrives.
> That's also why coding suits agents so well, as Anthropic's guide points out. Code comes with tests: an answer the agent can check its work against at every step.
> We've skipped a lot here: planning, memory that lasts between tasks, and teams of agents. But each of those still reaches the model the same way: through its context.
> So when you build an agent, or hand one a task, don't only ask how clever the model is. Ask what will tell it that it's wrong.

*Screen:* the two strips from chapter 1, as cards, now with their colours named once, small: grey "instructions", blue "the model's replies", green "tool results". A's green card with the red cross is outlined; the matching place in B's strip is empty. Then the loop picture from chapter 4 (model, our code, project, strip) settles in the middle. End card: the takeaway, and references: Anthropic, "Building effective agents" (Schluntz and Zhang, 2024); Anthropic, "Effective context engineering for AI agents" (2025); Claude API documentation, "How tool use works" and "Using the Messages API"; Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022); Willison, "I think 'agent' may finally have a widely enough agreed upon definition to be useful jargon now" (2025); Hong, Troynikov and Huber, "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (Chroma, 2025).

